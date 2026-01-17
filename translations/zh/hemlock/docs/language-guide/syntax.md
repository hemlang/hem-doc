# 语法概述

本文档介绍 Hemlock 程序的基本语法规则和结构。

## 核心语法规则

### 分号是必需的

与 JavaScript 或 Python 不同，语句末尾**必须**使用分号：

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**以下代码会导致错误：**
```hemlock
let x = 42  // 错误：缺少分号
let y = 10  // 错误：缺少分号
```

### 花括号是必需的

所有控制流代码块都必须使用花括号，即使只有单条语句：

```hemlock
// 正确
if (x > 0) {
    print("positive");
}

// 错误：缺少花括号
if (x > 0)
    print("positive");
```

### 注释

```hemlock
// 这是单行注释

/*
   这是
   多行注释
*/

let x = 42;  // 行内注释
```

## 变量

### 声明

使用 `let` 声明变量：

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### 类型注解（可选）

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hello";
```

### 常量

使用 `const` 声明不可变值：

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

尝试重新赋值常量会导致运行时错误："Cannot assign to const variable"。

## 表达式

### 算术运算符

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - 加法
print(a - b);   // 7  - 减法
print(a * b);   // 30 - 乘法
print(a / b);   // 3  - 除法（整数）
```

### 比较运算符

```hemlock
print(a == b);  // false - 等于
print(a != b);  // true  - 不等于
print(a > b);   // true  - 大于
print(a < b);   // false - 小于
print(a >= b);  // true  - 大于等于
print(a <= b);  // false - 小于等于
```

### 逻辑运算符

```hemlock
let x = true;
let y = false;

print(x && y);  // false - 与
print(x || y);  // true  - 或
print(!x);      // false - 非
```

### 位运算符

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - 按位与
print(a | b);   // 14 - 按位或
print(a ^ b);   // 6  - 按位异或
print(a << 2);  // 48 - 左移
print(a >> 1);  // 6  - 右移
print(~a);      // -13 - 按位取反
```

### 运算符优先级

从高到低：

1. `()` - 分组
2. `!`, `~`, `-`（一元）- 一元运算符
3. `*`, `/` - 乘法、除法
4. `+`, `-` - 加法、减法
5. `<<`, `>>` - 位移
6. `<`, `<=`, `>`, `>=` - 比较
7. `==`, `!=` - 相等性
8. `&` - 按位与
9. `^` - 按位异或
10. `|` - 按位或
11. `&&` - 逻辑与
12. `||` - 逻辑或

**示例：**
```hemlock
let x = 2 + 3 * 4;      // 14（不是 20）
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## 控制流

### If 语句

```hemlock
if (condition) {
    // 主体
}

if (condition) {
    // then 分支
} else {
    // else 分支
}

if (condition1) {
    // 分支 1
} else if (condition2) {
    // 分支 2
} else {
    // 默认分支
}
```

### While 循环

```hemlock
while (condition) {
    // 主体
}
```

**示例：**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### For 循环

**C 风格 for：**
```hemlock
for (initializer; condition; increment) {
    // 主体
}
```

**示例：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in（数组）：**
```hemlock
for (let item in array) {
    // 主体
}
```

**示例：**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Switch 语句

```hemlock
switch (expression) {
    case value1:
        // 主体
        break;
    case value2:
        // 主体
        break;
    default:
        // 默认主体
        break;
}
```

**示例：**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Monday");
        break;
    case 2:
        print("Tuesday");
        break;
    case 3:
        print("Wednesday");
        break;
    default:
        print("Other");
        break;
}
```

### Break 和 Continue

```hemlock
// Break：退出循环
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue：跳到下一次迭代
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## 函数

### 命名函数

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // 主体
    return value;
}
```

**示例：**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### 匿名函数

```hemlock
let func = fn(params) {
    // 主体
};
```

**示例：**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### 类型注解（可选）

```hemlock
// 无注解（类型推断）
fn greet(name) {
    return "Hello, " + name;
}

// 有注解（运行时检查）
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## 对象

### 对象字面量

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**示例：**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### 方法

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**示例：**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### 类型定义

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**示例：**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## 数组

### 数组字面量

```hemlock
let arr = [element1, element2, element3];
```

**示例：**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];
let empty = [];
```

### 数组索引

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // 修改元素
```

## 错误处理

### Try/Catch

```hemlock
try {
    // 可能出错的代码
} catch (e) {
    // 处理错误
}
```

### Try/Finally

```hemlock
try {
    // 可能出错的代码
} finally {
    // 总是执行
}
```

### Try/Catch/Finally

```hemlock
try {
    // 可能出错的代码
} catch (e) {
    // 处理错误
} finally {
    // 清理
}
```

### Throw

```hemlock
throw expression;
```

**示例：**
```hemlock
if (x < 0) {
    throw "x must be positive";
}
```

### Panic

```hemlock
panic(message);
```

**示例：**
```hemlock
panic("unrecoverable error");
```

## 模块（实验性）

### 导出语句

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### 导入语句

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## 异步（实验性）

### 异步函数

```hemlock
async fn function_name(params): return_type {
    // 主体
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### 通道

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI（外部函数接口）

### 导入共享库

```hemlock
import "library_name.so";
```

### 声明外部函数

```hemlock
extern fn function_name(param: type): return_type;
```

**示例：**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## 字面量

### 整数字面量

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // 自动 i64

// 十六进制（0x 前缀）
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// 二进制（0b 前缀）
let bin = 0b1010;
let bin2 = 0b11110000;

// 八进制（0o 前缀）
let oct = 0o777;
let oct2 = 0O123;

// 数字分隔符提高可读性
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### 浮点字面量

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // 科学计数法
let sci2 = 2.5E+3;       // 大写 E 也可以
let no_lead = .5;        // 无前导零 (0.5)
let sep = 3.14_159_265;  // 数字分隔符
```

### 字符串字面量

```hemlock
let s = "hello";
let escaped = "line1\nline2\ttabbed";
let quote = "She said \"hello\"";

// 十六进制转义序列
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Unicode 转义序列
let emoji = "\u{1F600}";               // 😀
let heart = "\u{2764}";                // ❤
let mixed = "Hello \u{1F30D}!";        // Hello 🌍!
```

**转义序列：**
- `\n` - 换行
- `\t` - 制表符
- `\r` - 回车
- `\\` - 反斜杠
- `\"` - 双引号
- `\'` - 单引号
- `\0` - 空字符
- `\xNN` - 十六进制转义（2 位）
- `\u{XXXX}` - Unicode 转义（1-6 位）

### Rune 字面量

```hemlock
let ch = 'A';
let emoji = '🚀';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### 布尔字面量

```hemlock
let t = true;
let f = false;
```

### Null 字面量

```hemlock
let nothing = null;
```

## 作用域规则

### 块作用域

变量的作用域为最近的封闭块：

```hemlock
let x = 1;  // 外部作用域

if (true) {
    let x = 2;  // 内部作用域（遮蔽外部）
    print(x);   // 2
}

print(x);  // 1
```

### 函数作用域

函数创建自己的作用域：

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // 可以读取外部作用域
}

foo();
// print(local);  // 错误：'local' 在此处未定义
```

### 闭包作用域

闭包捕获封闭作用域的变量：

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // 捕获 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## 空白和格式

### 缩进

Hemlock 不强制特定缩进，但建议使用 4 个空格：

```hemlock
fn example() {
    if (true) {
        print("indented");
    }
}
```

### 换行

语句可以跨越多行：

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Loop 语句

`loop` 关键字为无限循环提供更清晰的语法：

```hemlock
loop {
    // ... 执行工作
    if (done) {
        break;
    }
}
```

这等价于 `while (true)`，但意图更明确。

## 保留关键字

以下关键字在 Hemlock 中是保留的：

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## 下一步

- [类型系统](types.md) - 了解 Hemlock 的类型系统
- [控制流](control-flow.md) - 深入了解控制结构
- [函数](functions.md) - 掌握函数和闭包
- [内存管理](memory.md) - 理解指针和缓冲区
