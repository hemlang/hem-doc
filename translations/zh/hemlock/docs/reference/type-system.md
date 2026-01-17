# 类型系统参考

Hemlock 类型系统的完整参考，包括所有原始类型和复合类型。

---

## 概述

Hemlock 使用**动态类型系统**，具有运行时类型标签和可选的类型注解。每个值都有运行时类型，类型转换遵循明确的提升规则。

**主要特性：**
- 运行时类型检查（解释器）
- 编译时类型检查（hemlockc - 默认启用）
- 可选类型注解
- 字面量自动类型推断
- 明确的类型提升规则
- 不会隐式转换导致精度损失

---

## 编译时类型检查 (hemlockc)

Hemlock 编译器（`hemlockc`）包含编译时类型检查器，在生成可执行文件之前验证您的代码。这可以在不运行程序的情况下及早发现类型错误。

### 默认行为

类型检查在 hemlockc 中**默认启用**：

```bash
# Type checking happens automatically
hemlockc program.hml -o program

# Errors are reported before compilation
hemlockc bad_types.hml
# Output: 1 type error found
```

### 编译器标志

| 标志 | 描述 |
|------|------|
| `--check` | 仅检查类型，不编译（验证后退出） |
| `--no-type-check` | 禁用类型检查（不推荐） |
| `--strict-types` | 启用更严格的类型警告 |

**示例：**

```bash
# Just validate types without compiling
hemlockc --check program.hml
# Output: program.hml: no type errors

# Disable type checking (use with caution)
hemlockc --no-type-check dynamic_code.hml -o program

# Enable strict warnings for implicit any types
hemlockc --strict-types program.hml -o program
```

### 类型检查器验证的内容

1. **类型注解** - 确保赋值的值与声明的类型匹配
2. **函数调用** - 验证参数类型与参数类型匹配
3. **返回类型** - 检查返回语句与声明的返回类型匹配
4. **运算符使用** - 验证操作数兼容
5. **属性访问** - 验证类型化对象的对象字段类型

### 宽松的数值转换

类型检查器允许在编译时进行数值类型转换，范围验证在运行时进行：

```hemlock
let x: i8 = 100;      // OK - 100 fits in i8 (validated at runtime)
let y: u8 = 255;      // OK - within u8 range
let z: f64 = 42;      // OK - i32 to f64 is safe
```

### 动态代码支持

没有类型注解的代码被视为动态的（`any` 类型），始终通过类型检查器：

```hemlock
let x = get_value();  // Dynamic - no annotation
process(x);           // OK - dynamic values accepted anywhere
```

---

## 原始类型

### 数值类型

#### 有符号整数

| 类型   | 大小    | 范围                                       | 别名      |
|--------|---------|-------------------------------------------|-----------|
| `i8`   | 1 字节  | -128 到 127                               | -         |
| `i16`  | 2 字节  | -32,768 到 32,767                         | -         |
| `i32`  | 4 字节  | -2,147,483,648 到 2,147,483,647           | `integer` |
| `i64`  | 8 字节  | -9,223,372,036,854,775,808 到 9,223,372,036,854,775,807 | - |

**示例：**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Type alias
let x: integer = 42;  // Same as i32
```

#### 无符号整数

| 类型   | 大小    | 范围                      | 别名   |
|--------|---------|---------------------------|--------|
| `u8`   | 1 字节  | 0 到 255                  | `byte` |
| `u16`  | 2 字节  | 0 到 65,535               | -      |
| `u32`  | 4 字节  | 0 到 4,294,967,295        | -      |
| `u64`  | 8 字节  | 0 到 18,446,744,073,709,551,615 | - |

**示例：**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Type alias
let byte_val: byte = 65;  // Same as u8
```

#### 浮点数

| 类型   | 大小    | 精度         | 别名     |
|--------|---------|--------------|----------|
| `f32`  | 4 字节  | 约 7 位数字  | -        |
| `f64`  | 8 字节  | 约 15 位数字 | `number` |

**示例：**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// Type alias
let x: number = 2.718;  // Same as f64
```

---

### 整数字面量推断

整数字面量根据其值自动确定类型：

**规则：**
- 在 i32 范围内的值（-2,147,483,648 到 2,147,483,647）：推断为 `i32`
- 超出 i32 范围但在 i64 范围内的值：推断为 `i64`
- 其他类型（i8、i16、u8、u16、u32、u64）使用显式类型注解

**示例：**
```hemlock
let small = 42;                    // i32 (fits in i32)
let large = 5000000000;            // i64 (> i32 max)
let max_i64 = 9223372036854775807; // i64 (INT64_MAX)
let explicit: u32 = 100;           // u32 (type annotation overrides)
```

---

### 布尔类型

**类型：** `bool`

**值：** `true`、`false`

**大小：** 1 字节（内部）

**示例：**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("working");
}
```

---

### 字符类型

#### Rune

**类型：** `rune`

**描述：** Unicode 码点 (U+0000 到 U+10FFFF)

**大小：** 4 字节（32 位值）

**范围：** 0 到 0x10FFFF (1,114,111)

**字面量语法：** 单引号 `'x'`

**示例：**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// Multi-byte UTF-8
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// Escape sequences
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Unicode escapes
let emoji = '\u{1F680}';   // Up to 6 hex digits
let max = '\u{10FFFF}';    // Maximum codepoint
```

**类型转换：**
```hemlock
// Integer to rune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// Rune to integer
let value: i32 = 'Z';       // 90

// Rune to string
let s: string = 'H';        // "H"

// u8 to rune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**另请参阅：** [字符串 API](string-api.md) 了解字符串 + rune 连接

---

### 字符串类型

**类型：** `string`

**描述：** UTF-8 编码、可变、堆分配的文本

**编码：** UTF-8 (U+0000 到 U+10FFFF)

**可变性：** 可变（与大多数语言不同）

**属性：**
- `.length` - 码点数（字符数）
- `.byte_length` - 字节数（UTF-8 编码大小）

**字面量语法：** 双引号 `"text"`

**示例：**
```hemlock
let s = "hello";
s[0] = 'H';             // Mutate (now "Hello")
print(s.length);        // 5 (codepoint count)
print(s.byte_length);   // 5 (UTF-8 bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (one codepoint)
print(emoji.byte_length);   // 4 (four UTF-8 bytes)
```

**索引：**
```hemlock
let s = "hello";
let ch = s[0];          // Returns rune 'h'
s[0] = 'H';             // Set with rune
```

**另请参阅：** [字符串 API](string-api.md) 了解完整的方法参考

---

### 空值类型

**类型：** `null`

**描述：** 空值（表示值的缺失）

**大小：** 8 字节（内部）

**值：** `null`

**示例：**
```hemlock
let x = null;
let y: i32 = null;  // ERROR: type mismatch

if (x == null) {
    print("x is null");
}
```

---

## 复合类型

### 数组类型

**类型：** `array`

**描述：** 动态、堆分配、混合类型数组

**属性：**
- `.length` - 元素数量

**从零开始索引：** 是

**字面量语法：** `[elem1, elem2, ...]`

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Mixed types
let mixed = [1, "hello", true, null];
```

**另请参阅：** [数组 API](array-api.md) 了解完整的方法参考

---

### 对象类型

**类型：** `object`

**描述：** JavaScript 风格的动态字段对象

**字面量语法：** `{ field: value, ... }`

**示例：**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// Add field dynamically
person.email = "alice@example.com";
```

**类型定义：**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // Optional field
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### 指针类型

#### 原始指针 (ptr)

**类型：** `ptr`

**描述：** 原始内存地址（不安全）

**大小：** 8 字节

**边界检查：** 无

**示例：**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### 缓冲区 (buffer)

**类型：** `buffer`

**描述：** 带边界检查的安全指针包装器

**结构：** 指针 + 长度 + 容量

**属性：**
- `.length` - 缓冲区大小
- `.capacity` - 分配的容量

**示例：**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Bounds checked
print(b.length);        // 64
free(b);
```

**另请参阅：** [内存 API](memory-api.md) 了解分配函数

---

## 特殊类型

### 文件类型

**类型：** `file`

**描述：** 用于 I/O 操作的文件句柄

**属性：**
- `.path` - 文件路径（字符串）
- `.mode` - 打开模式（字符串）
- `.closed` - 文件是否已关闭（布尔值）

**另请参阅：** [文件 API](file-api.md)

---

### 任务类型

**类型：** `task`

**描述：** 并发任务的句柄

**另请参阅：** [并发 API](concurrency-api.md)

---

### 通道类型

**类型：** `channel`

**描述：** 线程安全的通信通道

**另请参阅：** [并发 API](concurrency-api.md)

---

### 函数类型

**类型：** `function`

**描述：** 一等函数值

**示例：**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Void 类型

**类型：** `void`

**描述：** 表示没有返回值（内部使用）

---

## 类型提升规则

当在操作中混合类型时，Hemlock 会提升到"更高"的类型：

**提升层级：**
```
f64 (highest precision)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (lowest)
```

**规则：**
1. 浮点数始终优先于整数
2. 在相同类别（整数/无符号整数/浮点数）中较大的大小优先
3. 两个操作数都会提升到结果类型
4. **精度保持：** i64/u64 + f32 提升到 f64（而不是 f32）

**示例：**
```hemlock
// Size promotion
u8 + i32    → i32    // Larger size wins
i32 + i64   → i64    // Larger size wins
u32 + u64   → u64    // Larger size wins

// Float promotion
i32 + f32   → f32    // Float wins, f32 sufficient for i32
i64 + f32   → f64    // Promotes to f64 to preserve i64 precision
i64 + f64   → f64    // Float always wins
i8 + f64    → f64    // Float + largest wins
```

**为什么 i64 + f32 → f64？**

f32 只有 24 位尾数，无法精确表示大于 2^24（16,777,216）的整数。由于 i64 可以保存高达 2^63 的值，将 i64 与 f32 混合会导致严重的精度损失。Hemlock 改为提升到 f64（53 位尾数）。

---

## 范围检查

类型注解在赋值时强制进行范围检查：

**有效赋值：**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**无效赋值（运行时错误）：**
```hemlock
let x: u8 = 256;             // ERROR: out of range
let y: i8 = 128;             // ERROR: max is 127
let z: u64 = -1;             // ERROR: u64 cannot be negative
```

---

## 类型内省

### typeof(value)

以字符串形式返回类型名称。

**签名：**
```hemlock
typeof(value: any): string
```

**返回值：**
- 原始类型：`"i8"`、`"i16"`、`"i32"`、`"i64"`、`"u8"`、`"u16"`、`"u32"`、`"u64"`、`"f32"`、`"f64"`、`"bool"`、`"string"`、`"rune"`、`"null"`
- 复合类型：`"array"`、`"object"`、`"ptr"`、`"buffer"`、`"function"`
- 特殊类型：`"file"`、`"task"`、`"channel"`
- 类型化对象：自定义类型名称（例如 `"Person"`）

**示例：**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**另请参阅：** [内置函数](builtins.md#typeof)

---

## 类型转换

### 隐式转换

Hemlock 在算术运算中按照类型提升规则执行隐式类型转换。

**示例：**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // result is i32 (promoted)
```

### 显式转换

使用类型注解进行显式转换：

**示例：**
```hemlock
// Integer to float
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Float to integer (truncates)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Integer to rune
let code: rune = 65;    // 'A'

// Rune to integer
let value: i32 = 'Z';   // 90

// Rune to string
let s: string = 'H';    // "H"
```

---

## 类型别名

### 内置别名

Hemlock 为常用类型提供内置类型别名：

| 别名      | 实际类型 | 用途           |
|-----------|----------|----------------|
| `integer` | `i32`    | 通用整数       |
| `number`  | `f64`    | 通用浮点数     |
| `byte`    | `u8`     | 字节值         |

**示例：**
```hemlock
let count: integer = 100;       // Same as i32
let price: number = 19.99;      // Same as f64
let b: byte = 255;              // Same as u8
```

### 自定义类型别名

使用 `type` 关键字定义自定义类型别名：

```hemlock
// Simple aliases
type Integer = i32;
type Text = string;

// Function type aliases
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// Compound type aliases
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Generic type aliases
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**使用自定义别名：**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**注意：** 类型别名是透明的 - `typeof()` 返回底层类型名称。

---

## 函数类型

函数类型指定函数值的签名：

### 语法

```hemlock
fn(param_types): return_type
```

### 示例

```hemlock
// Basic function type
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Function parameter
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Higher-order function returning function
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Async function type
fn run_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## 复合类型（交叉类型）

复合类型使用 `&` 来要求多个类型约束：

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Object must satisfy all types
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Three or more types
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## 汇总表

| 类型       | 大小     | 可变 | 堆分配 | 描述                   |
|------------|----------|------|--------|------------------------|
| `i8`-`i64` | 1-8 字节 | 否   | 否     | 有符号整数             |
| `u8`-`u64` | 1-8 字节 | 否   | 否     | 无符号整数             |
| `f32`      | 4 字节   | 否   | 否     | 单精度浮点数           |
| `f64`      | 8 字节   | 否   | 否     | 双精度浮点数           |
| `bool`     | 1 字节   | 否   | 否     | 布尔值                 |
| `rune`     | 4 字节   | 否   | 否     | Unicode 码点           |
| `string`   | 可变     | 是   | 是     | UTF-8 文本             |
| `array`    | 可变     | 是   | 是     | 动态数组               |
| `object`   | 可变     | 是   | 是     | 动态对象               |
| `ptr`      | 8 字节   | 否   | 否     | 原始指针               |
| `buffer`   | 可变     | 是   | 是     | 安全指针包装器         |
| `file`     | 不透明   | 是   | 是     | 文件句柄               |
| `task`     | 不透明   | 否   | 是     | 并发任务句柄           |
| `channel`  | 不透明   | 是   | 是     | 线程安全通道           |
| `function` | 不透明   | 否   | 是     | 函数值                 |
| `null`     | 8 字节   | 否   | 否     | 空值                   |

---

## 另请参阅

- [运算符参考](operators.md) - 运算中的类型行为
- [内置函数](builtins.md) - 类型内省和转换
- [字符串 API](string-api.md) - 字符串类型方法
- [数组 API](array-api.md) - 数组类型方法
- [内存 API](memory-api.md) - 指针和缓冲区操作
