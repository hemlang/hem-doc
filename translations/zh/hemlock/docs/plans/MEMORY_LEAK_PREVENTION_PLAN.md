# 内存泄漏预防计划

> 确保 Hemlock 运行时无内存泄漏，并履行与程序员的契约。

**日期：** 2026-01-16
**状态：** 已完成（在 v1.8.3 中实现）
**版本：** 1.0

---

## 执行摘要

Hemlock 的设计理念声明：*"我们提供安全的工具，但不强制你使用它们。"* 这意味着**运行时本身**即使在用户代码使用非安全特性时也必须是无泄漏的。程序员的契约是：

1. **用户分配**（`alloc`、`buffer`）由程序员负责 `free`
2. **运行时内部分配**（字符串、数组、对象、闭包）通过引用计数自动管理
3. **错误和异常**不得泄漏内存
4. **异步任务**具有明确的所有权语义
5. **运行时永远不会向程序员隐藏分配**

本计划识别当前基础设施中的差距，并提出系统性改进方案。

---

## 目录

1. [当前状态评估](#当前状态评估)
2. [已识别的差距](#已识别的差距)
3. [改进方案](#改进方案)
4. [测试策略](#测试策略)
5. [文档需求](#文档需求)
6. [实施阶段](#实施阶段)
7. [成功标准](#成功标准)

---

## 当前状态评估

### 优势

| 组件 | 实现方式 | 位置 |
|------|---------|------|
| 引用计数 | 带 `__ATOMIC_SEQ_CST` 的原子操作 | `src/backends/interpreter/values.c:413-550` |
| 循环检测 | 用于图遍历的 VisitedSet | `src/backends/interpreter/values.c:1345-1480` |
| 线程隔离 | 派生时深拷贝 | `src/backends/interpreter/values.c:1687-1859` |
| 带泄漏检测的分析器 | AllocSite 跟踪 | `src/backends/interpreter/profiler/` |
| ASAN 集成 | 带泄漏检测的 CI 流水线 | `.github/workflows/tests.yml` |
| Valgrind 支持 | 多个 Makefile 目标 | `Makefile:189-327` |
| 综合测试脚本 | 基于类别的测试 | `tests/leak_check.sh` |

### 当前内存所有权模型

```
┌─────────────────────────────────────────────────────────────────┐
│                      程序员责任                                  │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  指针运算 ────────────────────────────────────►  边界安全        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      运行时责任                                  │
├─────────────────────────────────────────────────────────────────┤
│  字符串字面量/操作 ──────────► 引用计数 + 自动释放               │
│  数组字面量/操作 ────────────► 引用计数 + 自动释放               │
│  对象字面量/操作 ────────────► 引用计数 + 自动释放               │
│  函数闭包 ───────────────────► 引用计数 + 环境释放               │
│  任务结果 ───────────────────► join() 后释放                     │
│  通道缓冲区 ─────────────────► close() 时释放                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 已识别的差距

### 差距 1：错误路径清理（高优先级）

**问题：** 当异常在执行过程中发生时，已分配的临时值可能泄漏。

**示例场景：**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // 数组已分配
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // 抛出异常
        return x * 2;
    });
    // 'transformed' 部分分配，'arr' 可能未释放
}
```

**当前状态：** 解释器的异常处理会展开调用栈，但可能不会释放表达式求值过程中创建的所有临时值。

**受影响的文件：**
- `src/backends/interpreter/runtime/evaluator.c`（表达式求值）
- `src/backends/interpreter/runtime/context.c`（异常处理）

### 差距 2：分离任务结果所有权（中优先级）

**问题：** `detach(task)` 允许即发即弃执行，但任务的结果可能永远不会被收集。

**当前行为：**
```hemlock
let task = spawn(compute_something);
detach(task);  // 任务在后台运行
// 任务完成时返回值会怎样？
```

**受影响的文件：**
- `src/backends/interpreter/builtins/concurrency.c:148-165`（任务完成）
- `src/backends/interpreter/values.c:745-780`（task_free）

### 差距 3：通道关闭与排空语义（中优先级）

**问题：** 当通道关闭时仍有缓冲值，这些值是否被正确释放？

**场景：**
```hemlock
let ch = channel(10);
ch.send("a");
ch.send("b");
ch.close();  // "a" 和 "b" 是否被释放？
```

**受影响的文件：**
- `src/backends/interpreter/values.c:850-915`（channel_close、channel_free）

### 差距 4：空值合并 AST 泄漏（已修复）

**问题：** 优化器在编译时已知结果时优化掉了空值合并表达式，但没有释放被丢弃的 AST 节点。

**根因：** 在 `optimizer.c` 中，当 `??` 被优化（例如 `"value" ?? "default"` → `"value"`）时，优化器返回保留的子节点，但没有释放父 `EXPR_NULL_COALESCE` 节点或被丢弃的子节点。

**修复：** 在优化器中添加了适当的清理：
- 保存结果子节点
- 用 `expr_free()` 释放未使用的子节点
- 释放父节点结构
- 返回保存的结果

**修改的文件：**
- `src/frontend/optimizer/optimizer.c`（空值合并优化清理）

### 差距 5：闭包捕获列表粒度（低优先级）

**问题：** 闭包捕获整个环境链而非仅引用的变量，可能不必要地延长了生命周期。

**示例：**
```hemlock
fn outer() {
    let large_data = buffer(1000000);  // 1MB
    let counter = 0;

    return fn() {
        return counter;  // 只使用 'counter'，但 'large_data' 也被捕获
    };
}
let f = outer();  // 'large_data' 在 'f' 释放前一直存活
```

**受影响的文件：**
- `src/backends/interpreter/values.c`（function_new、闭包创建）
- `src/frontend/parser/`（变量捕获分析）

### 差距 6：异步协调中的循环引用（低优先级）

**问题：** 引用通道的任务引用任务可能创建循环。

**场景：**
```hemlock
let ch = channel(1);
let task = spawn(fn() {
    ch.send(task);  // 任务通过通道发送自身
});
```

**当前缓解措施：** 发送时深拷贝防止了这个特定情况，但对象循环是可能的。

### 差距 7：FFI 内存边界文档（文档）

**问题：** 跨 FFI 边界的所有权转移没有正式记录。

**需要澄清的问题：**
- 谁拥有 extern 函数返回的内存？
- 传递给 C 函数的字符串会怎样？
- 回调应该如何处理内存？

---

## 改进方案

### 阶段 1：关键修复（第 1-2 周）

#### 1.1 异常安全的表达式求值

**方法：** 实现一个"临时值栈"，跟踪表达式求值期间的分配。

```c
// 在 evaluator.c 中
typedef struct {
    Value *temps;
    int count;
    int capacity;
} TempStack;

// 在子表达式返回前推入临时值
Value eval_binary_op(Evaluator *e, BinaryExpr *expr) {
    Value left = eval_expr(e, expr->left);
    temp_stack_push(e->temps, left);  // 跟踪

    Value right = eval_expr(e, expr->right);
    temp_stack_push(e->temps, right);  // 跟踪

    Value result = perform_op(left, right);

    temp_stack_pop(e->temps, 2);  // 成功时释放
    return result;
}

// 异常时清理释放所有跟踪的临时值
void exception_cleanup(Evaluator *e) {
    while (e->temps->count > 0) {
        Value v = temp_stack_pop(e->temps, 1);
        value_release(v);
    }
}
```

**测试：**
- 在 `tests/memory/exception_cleanup.hml` 中添加测试
- ASAN 验证异常路径

#### 1.2 分离任务结果清理

**方法：** 分离任务在完成时释放自己的结果。

```c
// 在 concurrency.c 中 - 任务完成处理器
void task_complete(Task *task, Value result) {
    pthread_mutex_lock(task->task_mutex);
    task->result = result;
    value_retain(task->result);  // 任务拥有结果
    task->state = TASK_COMPLETED;

    if (task->detached) {
        // 没有人会 join()，所以现在释放结果
        value_release(task->result);
        task->result = VAL_NULL;
    }
    pthread_mutex_unlock(task->task_mutex);
}
```

**测试：**
- 在 `tests/manual/stress_memory_leak.hml` 中添加分离任务压力测试
- 验证 ASAN 泄漏报告中无增长

#### 1.3 关闭时排空通道

**方法：** `channel_close()` 和 `channel_free()` 必须排空剩余值。

```c
// 在 values.c 中
void channel_free(Channel *ch) {
    pthread_mutex_lock(ch->mutex);

    // 排空缓冲值
    while (ch->count > 0) {
        Value v = ch->buffer[ch->head];
        value_release(v);
        ch->head = (ch->head + 1) % ch->capacity;
        ch->count--;
    }

    pthread_mutex_unlock(ch->mutex);

    // 释放同步原语
    pthread_mutex_destroy(ch->mutex);
    pthread_cond_destroy(ch->not_empty);
    pthread_cond_destroy(ch->not_full);
    pthread_cond_destroy(ch->rendezvous);

    free(ch->buffer);
    free(ch);
}
```

**测试：**
- 添加 `tests/memory/channel_drain.hml`

### 阶段 2：已知问题修复（第 3-4 周）

#### 2.1 空值合并 AST 修复

**方法：** 确保短路表达式的 AST 节点仍被访问以进行清理，或在求值时使用基于值的表示而非 AST 引用。

**需要调查：** 确定 AST 节点应由解析器拥有还是在求值期间复制。

#### 2.2 闭包捕获优化（可选）

**方法：** 分析函数体中的变量引用，创建最小捕获列表。

```c
// 函数解析期间
typedef struct {
    char **captured_names;
    int count;
} CaptureList;

CaptureList *analyze_captures(FunctionExpr *fn, Environment *env) {
    CaptureList *list = capture_list_new();
    visit_expr(fn->body, fn->params, env, list);  // 收集引用的自由变量
    return list;
}
```

**注意：** 这是优化，不是正确性修复。可能延后。

### 阶段 3：测试基础设施加固（第 5-6 周）

#### 3.1 泄漏回归套件

创建专门针对每个差距的泄漏回归测试套件：

```
tests/memory/
├── regression/
│   ├── exception_in_map.hml
│   ├── exception_in_filter.hml
│   ├── exception_in_reduce.hml
│   ├── exception_in_nested_call.hml
│   ├── detached_task_result.hml
│   ├── detached_task_spawn_loop.hml
│   ├── channel_close_with_values.hml
│   ├── channel_gc_stress.hml
│   ├── null_coalesce_literal.hml
│   ├── closure_large_capture.hml
│   └── cyclic_object_channel.hml
```

#### 3.2 持续泄漏监控

**增强 `tests/leak_check.sh`：**

```bash
# 添加基线比较
BASELINE_FILE="tests/memory/baseline_leaks.txt"

check_regression() {
    local current_leaks=$(count_leaks)
    local baseline_leaks=$(cat "$BASELINE_FILE" 2>/dev/null || echo "0")

    if [ "$current_leaks" -gt "$baseline_leaks" ]; then
        echo "LEAK REGRESSION: $current_leaks > $baseline_leaks"
        exit 1
    fi
}
```

#### 3.3 内存安全模糊测试

集成 libFuzzer 或 AFL 进行内存安全模糊测试：

```c
// fuzz_evaluator.c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char *source = malloc(size + 1);
    memcpy(source, data, size);
    source[size] = '\0';

    // 在 ASAN 活跃状态下解析和求值
    AST *ast = parse(source);
    if (ast) {
        ExecutionContext *ctx = ctx_new();
        evaluate(ctx, ast);  // ASAN 会捕获泄漏/UAF
        ctx_free(ctx);
        ast_free(ast);
    }

    free(source);
    return 0;
}
```

### 阶段 4：文档与契约（第 7 周）

#### 4.1 内存所有权文档

创建 `docs/advanced/memory-ownership.md`：

```markdown
# Hemlock 中的内存所有权

## 契约

1. **你分配，你释放**：`alloc()` 和 `buffer()` 返回你拥有的内存。
2. **运行时管理值**：字符串、数组、对象是引用计数的。
3. **异常会清理**：抛出异常不会泄漏（阶段 1 修复后）。
4. **任务复制参数**：派生的任务获得数据的自有副本。
5. **通道转移所有权**：`send()` 转移，`recv()` 接收。

## 所有权转移点

| 操作 | 从 | 到 |
|------|------|------|
| `let x = expr` | 表达式求值 | 变量绑定 |
| `return val` | 函数 | 调用者 |
| `ch.send(val)` | 发送者 | 通道缓冲区 |
| `ch.recv()` | 通道缓冲区 | 接收者 |
| `spawn(fn, args)` | 调用者（复制） | 任务 |
| `join(task)` | 任务 | 调用者 |

## FFI 所有权规则

1. **传递给 C**：除非使用 `move` 限定符，Hemlock 保留所有权
2. **从 C 接收**：Hemlock 接管所有权，引用计数归零时释放
3. **回调**：参数由 C 拥有，返回值由 Hemlock 拥有
```

---

## 测试策略

### 测试类别

| 类别 | 描述 | 工具 |
|------|------|------|
| 单元 | 单个函数泄漏测试 | ASAN |
| 集成 | 多组件场景 | ASAN + Valgrind |
| 压力 | 大量分配/释放循环 | ASAN（leak-check=no） |
| 模糊 | 随机输入内存安全 | libFuzzer + ASAN |
| 回归 | 已知修复的泄漏场景 | ASAN + 基线 |

### CI 流水线增强

```yaml
# .github/workflows/memory.yml
memory-safety:
  runs-on: ubuntu-latest
  steps:
    - name: Build with ASAN
      run: make asan

    - name: Run leak regression suite
      run: make leak-regression

    - name: Compare to baseline
      run: |
        ./tests/leak_check.sh --baseline
        if [ $? -ne 0 ]; then
          echo "::error::Leak regression detected"
          exit 1
        fi

    - name: Fuzz test (5 minutes)
      run: make fuzz-test FUZZ_TIME=300
```

---

## 实施阶段

| 阶段 | 重点 | 时间 | 优先级 |
|------|------|------|--------|
| 1 | 关键修复（异常、分离、通道） | 2 周 | 高 |
| 2 | 已知问题修复（空值合并、捕获） | 2 周 | 中 |
| 3 | 测试基础设施 | 2 周 | 高 |
| 4 | 文档 | 1 周 | 中 |

### 依赖关系

```
阶段 1 ──────► 阶段 3（测试验证修复）
    │
    └──────► 阶段 4（记录新的保证）

阶段 2 ──────► 阶段 3（添加回归测试）
```

---

## 成功标准

### 定量

- [ ] ASAN 在完整测试套件上报告零泄漏
- [ ] Valgrind 在完整测试套件上报告零泄漏
- [ ] 泄漏基线已建立并在 CI 中强制执行
- [ ] 100% 已识别差距已解决或记录为可接受

### 定性

- [ ] 内存所有权记录在 `docs/advanced/memory-ownership.md` 中
- [ ] FFI 所有权规则已记录
- [ ] 每个修复的泄漏都有回归测试
- [ ] 模糊测试集成到 CI 中

### 运行时契约验证

实施后必须满足以下保证：

1. **正常执行无泄漏**：运行任何有效程序并正常退出不会泄漏内存（运行时内部）。

2. **异常无泄漏**：抛出和捕获异常不会泄漏内存。

3. **任务完成无泄漏**：已完成的任务（加入或分离）不会泄漏内存。

4. **通道关闭无泄漏**：关闭通道释放所有缓冲值。

5. **确定性清理**：析构函数调用顺序是可预测的（defer 为 LIFO，对象为拓扑排序）。

---

## 附录：需要修改的文件

| 文件 | 更改 |
|------|------|
| `src/backends/interpreter/runtime/evaluator.c` | 添加 TempStack 用于异常安全求值 |
| `src/backends/interpreter/runtime/context.c` | 异常清理集成 |
| `src/backends/interpreter/builtins/concurrency.c` | 分离任务结果清理 |
| `src/backends/interpreter/values.c` | 通道排空、捕获优化 |
| `tests/leak_check.sh` | 基线比较 |
| `.github/workflows/tests.yml` | 添加内存回归任务 |
| `docs/advanced/memory-ownership.md` | 新文档 |
| `CLAUDE.md` | 更新所有权保证 |

---

## 参考资料

- 当前分析器：`src/backends/interpreter/profiler/profiler.c`
- 引用计数：`src/backends/interpreter/values.c:413-550`
- 任务管理：`src/backends/interpreter/builtins/concurrency.c`
- ASAN 文档：https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck：https://valgrind.org/docs/manual/mc-manual.html
