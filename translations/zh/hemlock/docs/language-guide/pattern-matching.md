# 模式匹配

Hemlock 通过 `match` 表达式提供强大的模式匹配功能，提供了一种简洁的方式来解构值、检查类型和处理多种情况。

## 基本语法

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

match 表达式按顺序将 `value` 与每个模式进行匹配，返回第一个匹配分支的表达式结果。

## 模式类型

### 字面量模式

匹配精确值：

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "one",
    42 => "the answer",
    _ => "other"
};
print(msg);  // "the answer"
```

支持的字面量：
- **整数**：`0`、`42`、`-5`
- **浮点数**：`3.14`、`-0.5`
- **字符串**：`"hello"`、`"world"`
- **布尔值**：`true`、`false`
- **空值**：`null`

### 通配符模式（`_`）

匹配任何值但不绑定：

```hemlock
let x = "anything";
let result = match (x) {
    "specific" => "found it",
    _ => "wildcard matched"
};
```

### 变量绑定模式

将匹配的值绑定到变量：

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "value is " + n  // n 绑定到 100
};
print(result);  // "value is 100"
```

### OR 模式（`|`）

匹配多个替代项：

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "small",
    4 | 5 | 6 => "medium",
    _ => "large"
};

// 也适用于字符串
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "exiting",
    "help" | "h" | "?" => "showing help",
    _ => "unknown"
};
```

### 守卫表达式（`if`）

为模式添加条件：

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negative",
    n if n == 0 => "zero",
    n if n < 10 => "small",
    n if n < 100 => "medium",
    n => "large: " + n
};
print(category);  // "medium"

// 复杂守卫
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "even and greater than 10",
    n if n % 2 == 0 => "even",
    n => "odd"
};
```

### 类型模式

基于类型检查和绑定：

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "integer: " + num,
    str: string => "string: " + str,
    flag: bool => "boolean: " + flag,
    _ => "other type"
};
print(desc);  // "integer: 42"
```

支持的类型：`i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`string`、`array`、`object`

## 解构模式

### 对象解构

从对象中提取字段：

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "point at " + x + "," + y
};
print(result);  // "point at 10,20"

// 带字面量字段值
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origin",
    { x: 0, y } => "on y-axis at " + y,
    { x, y: 0 } => "on x-axis at " + x,
    { x, y } => "point at " + x + "," + y
};
print(name);  // "origin"
```

### 数组解构

匹配数组结构和元素：

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "empty",
    [x] => "single: " + x,
    [x, y] => "pair: " + x + "," + y,
    [x, y, z] => "triple: " + x + "," + y + "," + z,
    _ => "many elements"
};
print(desc);  // "triple: 1,2,3"

// 带字面量值
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "both zero",
    [1, x] => "starts with 1, second is " + x,
    [x, 1] => "ends with 1",
    _ => "other"
};
print(result);  // "starts with 1, second is 2"
```

### 数组剩余模式（`...`）

捕获剩余元素：

```hemlock
let nums = [1, 2, 3, 4, 5];

// 头部和尾部
let result = match (nums) {
    [first, ...rest] => "first: " + first,
    [] => "empty"
};
print(result);  // "first: 1"

// 前两个元素
let result2 = match (nums) {
    [a, b, ...rest] => "first two: " + a + "," + b,
    _ => "too short"
};
print(result2);  // "first two: 1,2"
```

### 嵌套解构

组合模式处理复杂数据：

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " lives in " + city,
    _ => "unknown"
};
print(result);  // "Alice lives in NYC"

// 包含数组的对象
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "first: " + first + ", total: " + count,
    _ => "no items"
};
print(result2);  // "first: 1, total: 3"
```

## Match 作为表达式

Match 是一个返回值的表达式：

```hemlock
// 直接赋值
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// 在字符串连接中
let msg = "Grade: " + match (grade) {
    n if n >= 70 => "passing",
    _ => "failing"
};

// 在函数返回中
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positive",
        _ => "negative"
    };
}
```

## 模式匹配最佳实践

1. **顺序很重要**：模式从上到下检查；将特定模式放在通用模式之前
2. **使用通配符确保完整性**：除非确定所有情况都已覆盖，否则始终包含 `_` 回退
3. **优先使用守卫而非嵌套条件**：守卫使意图更清晰
4. **使用解构而非手动字段访问**：更简洁且更安全

```hemlock
// 好：使用守卫进行范围检查
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "below B"
}

// 好：解构而非访问字段
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// 避免：过于复杂的嵌套模式
// 考虑拆分为多个 match 或使用守卫
```

## 与其他语言的比较

| 特性 | Hemlock | Rust | JavaScript |
|---------|---------|------|------------|
| 基本匹配 | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| 解构 | 是 | 是 | 部分（switch 不解构） |
| 守卫 | `n if n > 0 =>` | `n if n > 0 =>` | 不适用 |
| OR 模式 | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| 剩余模式 | `[a, ...rest]` | `[a, rest @ ..]` | 不适用 |
| 类型模式 | `n: i32` | 通过 `match` 分支的类型 | 不适用 |
| 返回值 | 是 | 是 | 否（语句） |

## 实现说明

模式匹配在解释器和编译器后端都实现了完全一致性 - 两者对相同输入产生相同的结果。该功能在 Hemlock v1.8.0+ 中可用。
