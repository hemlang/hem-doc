# 编译器优化

Hemlock 编译器（`hemlockc`）在生成 C 代码时会应用多个优化遍。这些优化是自动的，不需要用户干预，但了解它们有助于理解性能特征。

---

## 概述

```
源代码 (.hml)
    ↓
  解析 → AST
    ↓
  类型检查（可选）
    ↓
  AST 优化遍
    ↓
  C 代码生成（带内联 + 拆箱）
    ↓
  GCC/Clang 编译
```

---

## 表达式级拆箱

Hemlock 的运行时将所有值表示为带标签的 `HmlValue` 结构体。在解释器中，每个算术运算都通过运行时分派进行装箱和拆箱。编译器为已知原始类型的表达式消除了这些开销。

**优化前（朴素代码生成）：**
```c
// x + 1 其中 x 是 i32
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 次装箱调用 + 运行时分派
```

**优化后（带表达式拆箱）：**
```c
// x + 1 其中 x 是 i32
hml_val_i32((x + 1))  // 纯 C 算术，最后只装箱一次
```

### 可拆箱的内容

- 二元算术：`+`、`-`、`*`、`%`
- 位运算：`&`、`|`、`^`、`<<`、`>>`
- 比较运算：`<`、`>`、`<=`、`>=`、`==`、`!=`
- 一元运算：`-`、`~`、`!`
- 带类型注解的变量和循环计数器

### 回退到 HmlValue 的情况

- 函数调用（返回类型可能是动态的）
- 数组/对象访问（编译时元素类型未知）
- 没有类型注解且无法推断类型的变量

### 提示

为热路径变量添加类型注解有助于编译器应用拆箱：

```hemlock
// 编译器可以拆箱整个表达式
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## 多级函数内联

编译器会在调用点内联小函数，用直接代码替代函数调用开销。Hemlock 支持最多 3 级深度的多级内联，即嵌套的辅助函数调用也会被内联。

### 工作原理

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // ep0 和 rotr 都会在此处内联
    // ...
}
```

在第 1 级，`ep0()` 被内联到 `sha256_round()` 中。在第 2 级，`ep0()` 内部的 `rotr()` 调用也被内联。最终结果是一个没有函数调用开销的纯原生算术代码块。

### 内联条件

函数在以下情况下被内联：
- 函数体很小（单个表达式或少量语句）
- 函数不是递归的
- 当前内联深度小于 3

### 使用注解控制内联

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // 不应被复制的复杂函数
    return x;
}
```

---

## While 循环累加器拆箱

对于顶层 while 循环，编译器会检测计数器和累加器变量，并用原生 C 局部变量替代它们，消除每次迭代的装箱/拆箱开销。

### 优化内容

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

编译器检测到 `sum` 和 `i` 是仅在循环内使用的整数累加器，生成原生 `int32_t` 局部变量而非 `HmlValue` 操作。这消除了每次迭代的 retain/release 开销和类型分派。

### 性能影响

这些优化带来的基准测试改进（在典型工作负载上测量）：

| 基准测试 | 优化前 | 优化后 | 改进 |
|-----------|--------|--------|------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## 辅助注解

编译器支持 10 个优化注解，映射到 GCC/Clang 属性：

| 注解 | 效果 |
|------|------|
| `@inline` | 鼓励函数内联 |
| `@noinline` | 阻止函数内联 |
| `@hot` | 标记为频繁执行（分支预测） |
| `@cold` | 标记为很少执行 |
| `@pure` | 函数无副作用（可读取外部状态） |
| `@const` | 函数仅依赖参数（不访问外部状态） |
| `@flatten` | 内联函数内的所有调用 |
| `@optimize(level)` | 每函数优化级别（"0"-"3"、"s"、"fast"） |
| `@warn_unused` | 忽略返回值时发出警告 |
| `@section(name)` | 将函数放在自定义 ELF 节中 |

### 示例

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // 热路径哈希函数
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## 分配池

运行时使用预分配的对象池来避免频繁创建的短生命周期对象的 `malloc`/`free` 开销：

| 池 | 槽数 | 描述 |
|------|------|------|
| 环境池 | 1024 | 闭包/函数作用域环境（每个最多 16 个变量） |
| 对象池 | 512 | 最多 8 个字段的匿名对象 |
| 函数池 | 512 | 捕获函数的闭包结构体 |

池使用空闲列表栈实现 O(1) 的分配和释放。当池耗尽时，运行时回退到 `malloc`。超出池槽大小的对象（例如获得第 9 个字段的对象）会被透明地迁移到堆存储。

### AST 借用参数

闭包直接从 AST 借用参数元数据，而不是深拷贝，消除了每次闭包创建约 6 次 `malloc` + N 次 `strdup` 调用。参数名称哈希在 AST 节点上延迟计算并缓存。

---

## 类型检查

编译器包含编译时类型检查（默认启用）：

```bash
hemlockc program.hml -o program       # 类型检查 + 编译
hemlockc --check program.hml          # 仅类型检查
hemlockc --no-type-check program.hml  # 跳过类型检查
hemlockc --strict-types program.hml   # 对隐式 'any' 类型发出警告
```

未标注类型的代码被视为动态类型（`any` 类型），始终通过类型检查。类型注解提供优化提示，使编译器能够应用拆箱。

---

## 另请参阅

- [辅助注解提案](../proposals/compiler-helper-annotations.md) - 详细的注解参考
- [内存 API](../reference/memory-api.md) - 缓冲区和指针操作
- [函数](../language-guide/functions.md) - 类型注解和表达式体函数
