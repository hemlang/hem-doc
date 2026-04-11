# 编译器辅助注解：分析与提案

**作者：** Claude
**日期：** 2026-01-08
**状态：** 部分实现（阶段 1-2 在 v1.9.0 中完成；阶段 3-5 仍为提案）
**相关：** Issue #TBD

## 目录

1. [执行摘要](#执行摘要)
2. [当前状态分析](#当前状态分析)
3. [提议的注解](#提议的注解)
4. [实施计划](#实施计划)
5. [示例](#示例)
6. [测试策略](#测试策略)
7. [未来考虑](#未来考虑)

---

## 执行摘要

Hemlock 的注解系统为添加编译器提示和指令提供了强大的基础。本提案用 **15 个新编译器辅助注解**扩展当前注解基础设施，分为五个类别：

- **优化提示**（7 个注解）
- **内存管理**（3 个注解）
- **代码生成控制**（2 个注解）
- **错误检查**（2 个注解）
- **FFI/互操作**（1 个注解）

这些注解将使开发者能够向编译器（`hemlockc`）提供显式指导，同时保持与解释器的向后兼容性。

---

## 当前状态分析

### 1. 注解基础设施

注解系统已完全实现，包含三个主要组件：

**解析器**（`src/frontend/parser/statements.c`）：
- 解析 `@name` 和 `@name(args...)` 语法
- 支持位置参数和命名参数
- 将注解附加到声明（let、const、define、enum）

**验证器**（`src/frontend/annotations.c`）：
- 验证注解目标（函数、类型、变量等）
- 检查参数数量和类型
- 对未知或重复注解发出警告

**解析器**（`src/frontend/resolver.c`）：
- 将注解与变量定义一起存储
- 在语义分析期间启用注解查找
- 驱动变量使用时的 `@deprecated` 警告

### 2. 当前已实现的注解

```c
// 安全注解（用于 Tricycle 内存检查器）
@safe       // 函数是内存安全的
@unsafe     // 函数包含非安全操作
@trusted    // 函数尽管有非安全操作也是受信任的

// 编译器优化提示（在 v1.9.0 中实现）
@inline     // 建议内联此函数
@noinline   // 阻止内联此函数
@cold       // 函数很少执行
@hot        // 函数频繁执行
@pure       // 函数无副作用

// 其他注解
@deprecated      // 标记为已弃用，带可选消息
@test, @skip     // 测试框架注解
@author, @since  // 文档注解
```

### 3. 当前限制

**更新（v1.9.0）：** 核心函数级注解（`@inline`、`@noinline`、`@hot`、`@cold`、`@pure`、`@const`、`@flatten`、`@optimize`、`@warn_unused`、`@section`）现已在编译器后端完全实现。下面阶段 3-5 中的剩余提案（循环注解、内存注解）仍未实现。

---

## 提议的注解

### 类别 1：优化提示

#### `@unroll(count?: number)`
**目标：** 循环（for、while）
**参数：** 可选展开因子（默认：编译器决定）

建议对性能关键的紧密循环进行循环展开。

```hemlock
@unroll(4)
for (let i = 0; i < 1024; i++) {
    buffer[i] = buffer[i] * 2;
}
```

---

#### `@simd` / `@nosimd`
**目标：** 函数、循环
**参数：** 无

启用或禁用 SIMD 向量化。

```hemlock
@simd
fn vector_add(a: buffer, b: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        ptr_write_f64(a, i, ptr_read_f64(a, i) + ptr_read_f64(b, i));
    }
}
```

---

#### `@likely` / `@unlikely`
**目标：** if 语句、条件
**参数：** 无

热路径的分支预测提示。

```hemlock
@likely
if (cache.has(key)) {
    return cache.get(key);
}

@unlikely
if (error) {
    handle_error(error);
}
```

---

#### `@const`
**目标：** 函数
**参数：** 无

函数对相同输入始终返回相同结果（比 `@pure` 更强）。

```hemlock
@const
fn square(x: i32): i32 => x * x;
```

**与 `@pure` 的区别：**
- `@pure`：可以读取全局内存，但不修改
- `@const`：甚至不能读取全局内存，只使用参数

---

#### `@tail_call`
**目标：** 函数调用
**参数：** 无

请求尾调用优化（TCO）。

```hemlock
fn factorial_helper(n: i32, acc: i32): i32 {
    if (n <= 1) { return acc; }
    @tail_call
    return factorial_helper(n - 1, n * acc);
}
```

---

#### `@flatten`
**目标：** 函数
**参数：** 无

内联此函数内的所有调用。

```hemlock
@flatten
fn compute_hash(data: buffer, len: i32): u64 {
    let hash = init_hash();
    hash = process_block(hash, data, len);
    return finalize_hash(hash);
}
```

---

#### `@optimize(level: string)`
**目标：** 函数
**参数：** 优化级别（"0"、"1"、"2"、"3"、"s"、"fast"）

为特定函数覆盖全局优化级别。

```hemlock
@optimize("3")
fn matrix_multiply(a: buffer, b: buffer, n: i32) {
    // 性能关键的内循环
}

@optimize("s")
fn rarely_called_error_handler() {
    // 优化大小，而非速度
}
```

---

### 类别 2：内存管理

#### `@stack`
**目标：** 变量（数组、缓冲区）
**参数：** 无

在栈上而非堆上分配（如果可能）。

```hemlock
@stack
let temp_buffer = buffer(1024);  // 栈分配
```

---

#### `@noalias`
**目标：** 函数参数（指针/缓冲区）
**参数：** 无

承诺指针不与其他指针别名。

```hemlock
fn memcpy_fast(@noalias dest: ptr, @noalias src: ptr, n: i32) {
    memcpy(dest, src, n);
}
```

---

#### `@aligned(bytes: number)`
**目标：** 变量（指针、缓冲区）、函数返回值
**参数：** 对齐字节数（必须是 2 的幂）

指定内存对齐要求。

```hemlock
@aligned(64)  // 缓存行对齐
let cache_line_buffer = buffer(64);
```

---

### 类别 3：代码生成控制

#### `@extern(name?: string, abi?: string)`
**目标：** 函数
**参数：**
- `name`：外部符号名（默认：函数名）
- `abi`：调用约定（"C"、"stdcall"、"fastcall"）

标记函数用于外部链接或 FFI 导出。

```hemlock
@extern
fn hemlock_init() {
    print("Library initialized");
}
```

---

#### `@section(name: string)`
**目标：** 函数、全局变量
**参数：** 节名

将符号放在特定的 ELF/Mach-O 节中。

```hemlock
@section(".text.hot")
@hot
fn critical_path() { }
```

---

### 类别 4：错误检查

#### `@bounds_check` / `@no_bounds_check`
**目标：** 数组/缓冲区操作、循环
**参数：** 无

覆盖全局边界检查策略。

```hemlock
@bounds_check
fn safe_array_access(arr: array, idx: i32) {
    return arr[idx];
}

@no_bounds_check
fn trusted_hot_loop(data: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        data[i] = 0;
    }
}
```

---

#### `@warn_unused`
**目标：** 函数返回值
**参数：** 无

调用者忽略返回值时发出警告。

```hemlock
@warn_unused
fn allocate_memory(size: i32): ptr {
    return alloc(size);
}

let p = allocate_memory(1024);  // 正确
allocate_memory(1024);          // 警告：未使用的返回值
```

---

### 类别 5：FFI/互操作

#### `@packed`
**目标：** 类型定义（define）
**参数：** 无

创建无填充的紧凑结构体（用于 C 互操作）。

```hemlock
@packed
define NetworkHeader {
    magic: u32,
    version: u8,
    flags: u8,
    length: u16
}  // 总计：8 字节，无填充
```

---

## 实施计划

### 阶段 1：核心基础设施（第 1 周）

**目标：** 使编译器能够查询和使用注解

1. 在 `src/frontend/annotations.c` 中添加注解查询函数
2. 更新注解规格
3. 添加编译器上下文注解支持

### 阶段 2：函数注解（第 2 周）

**目标：** 实现函数级优化提示

更新函数代码生成，生成 GCC/Clang 属性。

### 阶段 3：循环注解（第 3 周）

**目标：** 支持循环级提示（@unroll、@simd、@likely/@unlikely）

需要**语句级注解**，这是一个新特性。

### 阶段 4：内存注解（第 4 周）

**目标：** 实现 @stack、@noalias、@aligned

### 阶段 5：测试与文档（第 5 周）

**目标：** 全面的测试覆盖和文档

---

## 示例

### 示例 1：高性能向量数学

```hemlock
@simd
@flatten
fn vector_add(a: buffer, b: buffer, result: buffer, n: i32) {
    @unroll(8)
    for (let i = 0; i < n; i++) {
        let av = ptr_read_f64(a, i * 8);
        let bv = ptr_read_f64(b, i * 8);
        ptr_write_f64(result, i * 8, av + bv);
    }
}
```

### 示例 2：缓存优化数据结构

```hemlock
@packed
define CacheLineNode {
    next: ptr,
    data: i64,
    timestamp: u64,
    flags: u32,
    padding: u32
}

@hot
@inline
fn cache_lookup(@aligned(64) cache: ptr, key: u64): ptr {
    @likely
    if (cache == null) {
        return null;
    }
    let node = ptr_read_ptr(cache);
    @unroll(4)
    while (node != null) {
        let node_key = ptr_read_u64(node, 8);
        if (node_key == key) {
            return node;
        }
        node = ptr_read_ptr(node);
    }
    return null;
}
```

### 示例 3：递归尾调用优化

```hemlock
@tail_call
fn sum_range(start: i32, end: i32, acc: i32): i32 {
    if (start > end) {
        return acc;
    }
    @tail_call
    return sum_range(start + 1, end, acc + start);
}
```

### 示例 4：带自定义 ABI 的 FFI 导出

```hemlock
import "libmath.so";
extern fn sqrt(x: f64): f64;

@extern(name: "hemlock_compute_distance")
@warn_unused
fn compute_distance(x1: f64, y1: f64, x2: f64, y2: f64): f64 {
    let dx = x2 - x1;
    let dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}
```

### 示例 5：混合提示的性能关键路径

```hemlock
@optimize("3")
@hot
fn process_frame(@noalias frame_data: buffer, width: i32, height: i32) {
    @stack
    let temp_row = buffer(width * 4);

    @no_bounds_check
    for (let y = 0; y < height; y++) {
        @unroll(4)
        for (let x = 0; x < width; x++) {
            let offset = (y * width + x) * 4;
        }
    }
}

@optimize("s")
@cold
fn handle_error(code: i32, msg: string) {
    eprint("Error ", code, ": ", msg);
    signal(SIGABRT, fn(sig) { panic("Fatal error"); });
}
```

---

## 测试策略

### 1. 验证测试

测试新注解的正确验证：无效参数、冲突注解等。

### 2. 对等测试

确保注解不改变程序行为——解释器和编译器的输出必须相同。

### 3. 编译器特定测试

验证生成的 C 代码包含正确的属性/pragma。

### 4. 性能基准测试

测量实际性能改进：
- SIMD 在 AVX2 系统上预期 2-4 倍加速
- 仅 @unroll 预期 1.5-2 倍加速

---

## 未来考虑

1. **注解继承** - 类型上的注解是否应用于所有实例？
2. **注解组合** - 允许从其他注解创建自定义注解？
3. **编译器标志集成** - 注解是否应覆盖编译器标志？
4. **静态分析集成** - 注解可以驱动静态分析工具
5. **运行时注解访问** - 注解在运行时是否可查询？

---

## 结论

本提案为 Hemlock 添加 **15 个新编译器辅助注解**，使开发者能够在保持语言"显式优于隐式"理念的同时提供显式优化提示。

**关键优势：**

1. **性能：** 关键路径通过 SIMD、展开、内联可获得 2-10 倍加速
2. **控制：** 开发者可以覆盖默认编译器启发式
3. **互操作：** 通过 @extern、@packed、@aligned 更好的 FFI 支持
4. **安全：** 显式 @bounds_check/@no_bounds_check 使安全权衡可见
5. **显式：** 符合 Hemlock 的理念——没有魔法，只有清晰的指令

**实施工作量：** 约 5 周完成完整实现

---

## 附录：完整注解参考表

| 注解 | 目标 | 参数 | 描述 | C 属性 |
|------|------|------|------|--------|
| `@inline` | fn | 0 | 强制内联 | `always_inline` |
| `@noinline` | fn | 0 | 阻止内联 | `noinline` |
| `@cold` | fn | 0 | 很少执行 | `cold` |
| `@hot` | fn | 0 | 频繁执行 | `hot` |
| `@pure` | fn | 0 | 无副作用，可读全局 | `pure` |
| `@const` | fn | 0 | 无副作用，不读全局 | `const` |
| `@flatten` | fn | 0 | 内联函数内所有调用 | `flatten` |
| `@tail_call` | fn | 0 | 请求尾调用优化 | 自定义 |
| `@optimize(level)` | fn | 1 | 覆盖优化级别 | `optimize("OX")` |
| `@unroll(factor?)` | loop | 0-1 | 循环展开提示 | `#pragma unroll` |
| `@simd` | fn, loop | 0 | 启用 SIMD 向量化 | `#pragma omp simd` |
| `@nosimd` | fn, loop | 0 | 禁用 SIMD | 自定义 |
| `@likely` | if | 0 | 分支可能被执行 | `__builtin_expect` |
| `@unlikely` | if | 0 | 分支不太可能被执行 | `__builtin_expect` |
| `@stack` | let | 0 | 栈分配 | 自定义 |
| `@noalias` | param | 0 | 无指针别名 | `noalias` |
| `@aligned(N)` | let, fn | 1 | 内存对齐 | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | 外部链接 | `extern "C"` |
| `@section(name)` | fn, let | 1 | 放在特定节 | `section("X")` |
| `@bounds_check` | fn | 0 | 强制边界检查 | 自定义 |
| `@no_bounds_check` | fn | 0 | 禁用边界检查 | 自定义 |
| `@warn_unused` | fn | 0 | 未使用返回值时警告 | `warn_unused_result` |
| `@packed` | define | 0 | 无结构体填充 | `packed` |

**现有注解（本提案未涵盖）：**
- `@safe`、`@unsafe`、`@trusted`（用于 Tricycle）
- `@deprecated`（已实现）
- `@test`、`@skip`、`@timeout`（测试框架）
- `@author`、`@since`、`@see`（文档）
