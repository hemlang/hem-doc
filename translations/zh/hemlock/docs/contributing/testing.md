# Hemlock 测试指南

本指南解释了 Hemlock 的测试理念、如何编写测试以及如何运行测试套件。

---

## 目录

- [测试理念](#测试理念)
- [测试套件结构](#测试套件结构)
- [运行测试](#运行测试)
- [编写测试](#编写测试)
- [测试类别](#测试类别)
- [内存泄漏测试](#内存泄漏测试)
- [持续集成](#持续集成)
- [最佳实践](#最佳实践)

---

## 测试理念

### 核心原则

**1. 测试驱动开发（TDD）**

在实现功能**之前**编写测试：

```
1. 编写一个失败的测试
2. 实现功能
3. 运行测试（应该通过）
4. 如果需要，进行重构
5. 重复
```

**好处：**
- 确保功能确实有效
- 防止回归
- 记录预期行为
- 使重构更安全

**2. 全面覆盖**

测试成功和失败情况：

```hemlock
// 成功情况
let x: u8 = 255;  // 应该成功

// 失败情况
let y: u8 = 256;  // 应该出错
```

**3. 尽早且频繁地测试**

运行测试：
- 在提交代码之前
- 在进行更改之后
- 在提交 pull request 之前
- 在代码审查期间

**规则：** 合并之前所有测试必须通过。

### 测试什么

**始终测试：**
- 基本功能（正常路径）
- 错误条件（异常路径）
- 边界情况（边界条件）
- 类型检查和转换
- 内存管理（无泄漏）
- 并发和竞态条件

**示例测试覆盖：**
```hemlock
// 功能：String.substr(start, length)

// 正常路径
print("hello".substr(0, 5));  // "hello"

// 边界情况
print("hello".substr(0, 0));  // ""（空）
print("hello".substr(5, 0));  // ""（在末尾）
print("hello".substr(2, 100)); // "llo"（超过末尾）

// 错误情况
// "hello".substr(-1, 5);  // 错误：负索引
// "hello".substr(0, -1);  // 错误：负长度
```

---

## 测试套件结构

### 目录组织

```
tests/
├── run_tests.sh          # 主测试运行脚本
├── primitives/           # 类型系统测试
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # 类型转换测试
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # 指针/缓冲区测试
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # 字符串操作测试
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # 控制流测试
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # 函数和闭包测试
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # 对象测试
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # 数组操作测试
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # 循环测试
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # 错误处理测试
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # 文件 I/O 测试
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # 并发测试
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # FFI 测试
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # 信号处理测试
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # 命令行参数测试
    └── basic.hml
```

### 测试文件命名

**约定：**
- 使用描述性名称：`method_chaining.hml` 而不是 `test1.hml`
- 分组相关测试：`string_substr.hml`、`string_slice.hml`
- 每个文件一个功能区域
- 保持文件专注且小巧

---

## 运行测试

### 运行所有测试

```bash
# 从 hemlock 根目录
make test

# 或直接
./tests/run_tests.sh
```

**输出：**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### 运行特定类别

```bash
# 只运行字符串测试
./tests/run_tests.sh tests/strings/

# 只运行一个测试文件
./tests/run_tests.sh tests/strings/concat.hml

# 运行多个类别
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### 使用 Valgrind 运行（内存泄漏检查）

```bash
# 检查单个测试的泄漏
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# 检查所有测试（很慢！）
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### 调试失败的测试

```bash
# 使用详细输出运行
./hemlock tests/failing_test.hml

# 使用 gdb 运行
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # 如果崩溃
```

---

## 编写测试

### 测试文件格式

测试文件只是带有预期输出的 Hemlock 程序：

**示例：tests/primitives/integers.hml**
```hemlock
// 测试基本整数字面量
let x = 42;
print(x);  // Expect: 42

let y: i32 = 100;
print(y);  // Expect: 100

// 测试算术
let sum = x + y;
print(sum);  // Expect: 142

// 测试类型推断
let small = 10;
print(typeof(small));  // Expect: i32

let large = 5000000000;
print(typeof(large));  // Expect: i64
```

**测试如何工作：**
1. 测试运行器执行 .hml 文件
2. 捕获 stdout 输出
3. 与预期输出比较（从注释或单独的 .out 文件）
4. 报告通过/失败

### 预期输出方法

**方法 1：内联注释（推荐用于简单测试）**

```hemlock
print("hello");  // Expect: hello
print(42);       // Expect: 42
```

测试运行器解析 `// Expect: ...` 注释。

**方法 2：单独的 .out 文件**

创建 `test_name.hml.out` 包含预期输出：

**test_name.hml：**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**test_name.hml.out：**
```
line 1
line 2
line 3
```

### 测试错误情况

错误测试应该导致程序以非零状态退出：

**示例：tests/primitives/range_error.hml**
```hemlock
// 这应该因类型错误而失败
let x: u8 = 256;  // 超出 u8 范围
```

**预期行为：**
- 程序以非零状态退出
- 向 stderr 打印错误消息

**测试运行器处理：**
- 期望出错的测试应该在单独的文件中
- 使用命名约定：`*_error.hml` 或 `*_fail.hml`
- 在注释中记录预期错误

### 测试成功情况

**示例：tests/strings/methods.hml**
```hemlock
// 测试 substr
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Expect: world

// 测试 find
let pos = s.find("world");
print(pos);  // Expect: 6

// 测试 contains
let has = s.contains("lo");
print(has);  // Expect: true

// 测试 trim
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Expect: hello
```

### 测试边界情况

**示例：tests/arrays/edge_cases.hml**
```hemlock
// 空数组
let empty = [];
print(empty.length);  // Expect: 0

// 单个元素
let single = [42];
print(single[0]);  // Expect: 42

// 负索引（应该在单独的测试文件中出错）
// print(single[-1]);  // 错误

// 超出末尾索引（应该出错）
// print(single[100]);  // 错误

// 边界条件
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Expect: []（空）
print(arr.slice(3, 3));  // Expect: []（空）
print(arr.slice(1, 2));  // Expect: [2]
```

### 测试类型系统

**示例：tests/conversions/promotion.hml**
```hemlock
// 测试二元运算中的类型提升

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Expect: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Expect: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Expect: i32
```

### 测试并发

**示例：tests/async/basic.hml**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 生成任务
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// 等待并打印结果
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Expect: 45
print(r2);  // Expect: 190
```

### 测试异常

**示例：tests/exceptions/try_catch.hml**
```hemlock
// 测试基本 try/catch
try {
    throw "error message";
} catch (e) {
    print("Caught: " + e);  // Expect: Caught: error message
}

// 测试 finally
let executed = false;
try {
    print("try");  // Expect: try
} finally {
    executed = true;
    print("finally");  // Expect: finally
}

// 测试异常传播
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // Expect: failure
}
```

---

## 测试类别

### 原始类型测试

**测试什么：**
- 整数类型（i8、i16、i32、i64、u8、u16、u32、u64）
- 浮点类型（f32、f64）
- 布尔类型
- 字符串类型
- Rune 类型
- Null 类型

**示例领域：**
- 字面量语法
- 类型推断
- 范围检查
- 溢出行为
- 类型注解

### 转换测试

**测试什么：**
- 隐式类型提升
- 显式类型转换
- 有损转换（应该出错）
- 运算中的类型提升
- 跨类型比较

### 内存测试

**测试什么：**
- alloc/free 正确性
- Buffer 创建和访问
- 缓冲区边界检查
- memset、memcpy、realloc
- 内存泄漏检测（valgrind）

### 字符串测试

**测试什么：**
- 连接
- 所有 18 个字符串方法
- UTF-8 处理
- Rune 索引
- 字符串 + rune 连接
- 边界情况（空字符串、单字符等）

### 控制流测试

**测试什么：**
- if/else/else if
- while 循环
- for 循环
- switch 语句
- break/continue
- return 语句

### 函数测试

**测试什么：**
- 函数定义和调用
- 参数传递
- 返回值
- 递归
- 闭包和捕获
- 一等函数
- 匿名函数

### 对象测试

**测试什么：**
- 对象字面量
- 字段访问和赋值
- 方法和 self 绑定
- 鸭子类型
- 可选字段
- JSON 序列化/反序列化
- 循环引用检测

### 数组测试

**测试什么：**
- 数组创建
- 索引和赋值
- 所有 15 个数组方法
- 混合类型
- 动态调整大小
- 边界情况（空、单个元素）

### 异常测试

**测试什么：**
- try/catch/finally
- throw 语句
- 异常传播
- 嵌套 try/catch
- try/catch/finally 中的 return
- 未捕获的异常

### I/O 测试

**测试什么：**
- 文件打开模式
- 读/写操作
- Seek/tell
- 文件属性
- 错误处理（缺少文件等）
- 资源清理

### 异步测试

**测试什么：**
- spawn/join/detach
- Channel send/recv
- 任务中的异常传播
- 多个并发任务
- Channel 阻塞行为

### FFI 测试

**测试什么：**
- dlopen/dlclose
- dlsym
- 各种类型的 dlcall
- 类型转换
- 错误处理

---

## 内存泄漏测试

### 使用 Valgrind

**基本用法：**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**示例输出（无泄漏）：**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**示例输出（有泄漏）：**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### 常见泄漏来源

**1. 缺少 free() 调用：**
```c
// 差
char *str = malloc(100);
// ... 使用 str
// 忘记释放！

// 好
char *str = malloc(100);
// ... 使用 str
free(str);
```

**2. 丢失的指针：**
```c
// 差
char *ptr = malloc(100);
ptr = malloc(200);  // 丢失了对第一次分配的引用！

// 好
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. 异常路径：**
```c
// 差
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // 泄漏！
    }
    free(data);
}

// 好
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### 已知可接受的泄漏

一些小的"泄漏"是有意的启动分配：

**全局内置：**
```hemlock
// 内置函数、FFI 类型和常量在启动时分配
// 并且在退出时不释放（通常约 200 字节）
```

这些不是真正的泄漏 - 它们是一次性分配，在程序生命周期内持续存在，并在退出时由操作系统清理。

---

## 持续集成

### GitHub Actions（未来）

一旦设置了 CI，所有测试将自动运行：
- 推送到 main 分支
- Pull request 创建/更新
- 每日定时运行

**CI 工作流程：**
1. 构建 Hemlock
2. 运行测试套件
3. 检查内存泄漏（valgrind）
4. 在 PR 上报告结果

### 提交前检查

在提交之前，运行：

```bash
# 全新构建
make clean && make

# 运行所有测试
make test

# 检查一些测试的泄漏
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## 最佳实践

### 应该做的

**先编写测试（TDD）**
```bash
1. 创建 tests/feature/new_feature.hml
2. 在 src/ 中实现功能
3. 运行测试直到通过
```

**测试成功和失败两种情况**
```hemlock
// 成功：tests/feature/success.hml
let result = do_thing();
print(result);  // Expect: expected value

// 失败：tests/feature/failure.hml
do_invalid_thing();  // 应该出错
```

**使用描述性测试名称**
```
好：tests/strings/substr_utf8_boundary.hml
差：tests/test1.hml
```

**保持测试专注**
- 每个文件一个功能区域
- 清晰的设置和断言
- 最少的代码

**添加解释棘手测试的注释**
```hemlock
// 测试闭包通过引用捕获外部变量
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // 在闭包创建后修改
    return f();  // 应该返回 20，而不是 10
}
```

**测试边界情况**
- 空输入
- Null 值
- 边界值（最小/最大）
- 大输入
- 负值

### 不应该做的

**不要跳过测试**
- 合并前所有测试必须通过
- 不要注释掉失败的测试
- 修复错误或删除功能

**不要编写相互依赖的测试**
```hemlock
// 差：test2.hml 依赖于 test1.hml 的输出
// 测试应该是独立的
```

**不要在测试中使用随机值**
```hemlock
// 差：不确定性
let x = random();
print(x);  // 无法预测输出

// 好：确定性
let x = 42;
print(x);  // Expect: 42
```

**不要测试实现细节**
```hemlock
// 差：测试内部结构
let obj = { x: 10 };
// 不要检查内部字段顺序、容量等

// 好：测试行为
print(obj.x);  // Expect: 10
```

**不要忽略内存泄漏**
- 所有测试应该是 valgrind 清洁的
- 记录已知/可接受的泄漏
- 在合并前修复泄漏

### 测试维护

**何时更新测试：**
- 功能行为更改
- 错误修复需要新的测试用例
- 发现边界情况
- 性能改进

**何时删除测试：**
- 功能从语言中删除
- 测试重复了现有覆盖
- 测试是错误的

**重构测试：**
- 将相关测试分组在一起
- 提取公共设置代码
- 使用一致的命名
- 保持测试简单和可读

---

## 示例测试会话

这是添加带有测试的功能的完整示例：

### 功能：添加 `array.first()` 方法

**1. 先编写测试：**

```bash
# 创建测试文件
cat > tests/arrays/first_method.hml << 'EOF'
// 测试 array.first() 方法

// 基本情况
let arr = [1, 2, 3];
print(arr.first());  // Expect: 1

// 单个元素
let single = [42];
print(single.first());  // Expect: 42

// 空数组（应该出错 - 单独的测试文件）
// let empty = [];
// print(empty.first());  // 错误
EOF
```

**2. 运行测试（应该失败）：**

```bash
./hemlock tests/arrays/first_method.hml
# Error: Method 'first' not found on array
```

**3. 实现功能：**

编辑 `src/interpreter/builtins.c`：

```c
// 添加 array_first 方法
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Error: Cannot get first element of empty array\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// 在数组方法表中注册
// ... 添加到数组方法注册
```

**4. 运行测试（应该通过）：**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# 成功！
```

**5. 检查内存泄漏：**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. 运行完整测试套件：**

```bash
make test
# Total: 252 tests（251 + 新的）
# Passed: 252
# Failed: 0
```

**7. 提交：**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## 总结

**记住：**
- 先编写测试（TDD）
- 测试成功和失败情况
- 在提交前运行所有测试
- 检查内存泄漏
- 记录已知问题
- 保持测试简单和专注

**测试质量与代码质量同样重要！**
