# Rune 字符

Rune 表示 **Unicode 码点**（U+0000 到 U+10FFFF），作为 Hemlock 中字符操作的独立类型。与字节（u8）不同，rune 是完整的 Unicode 字符，可以表示任何语言的字符或表情符号。

## 概述

```hemlock
let ch = 'A';           // Rune 字面量
let emoji = '🚀';       // 多字节字符作为单个 rune
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // 字符串 + rune 连接
let r = '>' + " msg";   // Rune + 字符串连接
```

## 什么是 Rune？

Rune 是表示 Unicode 码点的 **32 位值**：

- **范围：** 0 到 0x10FFFF（1,114,111 个有效码点）
- **不是数值类型** - 用于字符表示
- **与 u8/char 不同** - Rune 是完整的 Unicode，u8 只是字节
- **字符串索引返回** - `str[0]` 返回 rune，而不是字节

**为什么使用 rune？**
- Hemlock 字符串是 UTF-8 编码的
- 单个 Unicode 字符在 UTF-8 中可能是 1-4 个字节
- Rune 允许处理完整字符，而不是部分字节

## Rune 字面量

### 基本语法

单引号表示 rune 字面量：

```hemlock
let a = 'A';            // ASCII 字符
let b = '0';            // 数字字符
let c = '!';            // 标点符号
let d = ' ';            // 空格
```

### 多字节 UTF-8 字符

Rune 可以表示任何 Unicode 字符：

```hemlock
// 表情符号
let rocket = '🚀';      // 表情符号（U+1F680）
let heart = '❤';        // 心形（U+2764）
let smile = '😀';       // 笑脸（U+1F600）

// CJK 字符
let chinese = '中';     // 中文（U+4E2D）
let japanese = 'あ';    // 平假名（U+3042）
let korean = '한';      // 韩文（U+D55C）

// 符号
let check = '✓';        // 对勾（U+2713）
let arrow = '→';        // 右箭头（U+2192）
```

### 转义序列

特殊字符的常用转义序列：

```hemlock
let newline = '\n';     // 换行符（U+000A）
let tab = '\t';         // 制表符（U+0009）
let backslash = '\\';   // 反斜杠（U+005C）
let quote = '\'';       // 单引号（U+0027）
let dquote = '"';       // 双引号（U+0022）
let null_char = '\0';   // 空字符（U+0000）
let cr = '\r';          // 回车符（U+000D）
```

**可用的转义序列：**
- `\n` - 换行符
- `\t` - 水平制表符
- `\r` - 回车符
- `\0` - 空字符
- `\\` - 反斜杠
- `\'` - 单引号
- `\"` - 双引号

### Unicode 转义

使用 `\u{XXXXXX}` 语法表示 Unicode 码点（最多 6 个十六进制数字）：

```hemlock
let rocket = '\u{1F680}';   // 🚀 通过 Unicode 转义表示的表情符号
let heart = '\u{2764}';     // ❤ 心形
let ascii = '\u{41}';       // 'A' 通过转义表示
let max = '\u{10FFFF}';     // 最大 Unicode 码点

// 前导零是可选的
let a = '\u{41}';           // 与 '\u{0041}' 相同
let b = '\u{0041}';
```

**规则：**
- 范围：`\u{0}` 到 `\u{10FFFF}`
- 十六进制数字：1 到 6 位
- 不区分大小写：`\u{1F680}` 或 `\u{1f680}`
- 超出有效 Unicode 范围的值会导致错误

## 字符串 + Rune 连接

Rune 可以与字符串连接：

```hemlock
// 字符串 + rune
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Text" + '✓';       // "Text✓"

// Rune + 字符串
let prefix = '>' + " Message";      // "> Message"
let bullet = '•' + " Item";         // "• Item"

// 多重连接
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"

// 方法链可以使用
let result = ('>' + " Important").to_upper();  // "> IMPORTANT"
```

**工作原理：**
- Rune 自动编码为 UTF-8
- 在连接过程中转换为字符串
- 字符串连接运算符透明地处理这一点

## 类型转换

Rune 可以与其他类型相互转换。

### 整数 ↔ Rune

在整数和 rune 之间转换以处理码点值：

```hemlock
// 整数到 rune（码点值）
let code: rune = 65;            // 'A'（ASCII 65）
let emoji_code: rune = 128640;  // U+1F680（🚀）

// Rune 到整数（获取码点值）
let r = 'Z';
let value: i32 = r;             // 90（ASCII 值）

let rocket = '🚀';
let code: i32 = rocket;         // 128640（U+1F680）
```

**范围检查：**
- 整数到 rune：必须在 [0, 0x10FFFF] 范围内
- 超出范围的值会导致运行时错误
- Rune 到整数：始终成功（返回码点）

### Rune → 字符串

Rune 可以显式转换为字符串：

```hemlock
// 显式转换
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// 连接时自动转换
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8（字节）→ Rune

任何 u8 值（0-255）都可以转换为 rune：

```hemlock
// ASCII 范围（0-127）
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// 扩展 ASCII / Latin-1（128-255）
let extended: u8 = 200;
let r: rune = extended;         // U+00C8（È）

// 注意：0-127 是 ASCII，128-255 是 Latin-1
```

### 链式转换

类型转换可以链式进行：

```hemlock
// i32 → rune → string
let code: i32 = 128512;         // 笑脸码点
let r: rune = code;             // 😀
let s: string = r;              // "😀"

// 在一个表达式中完成
let emoji: string = 128640;     // 隐式 i32 → rune → string（🚀）
```

## Rune 操作

### 打印

Rune 的显示方式取决于码点：

```hemlock
let ascii = 'A';
print(ascii);                   // 'A'（带引号，可打印 ASCII）

let emoji = '🚀';
print(emoji);                   // U+1F680（非 ASCII 的 Unicode 表示法）

let tab = '\t';
print(tab);                     // U+0009（不可打印字符用十六进制表示）

let space = ' ';
print(space);                   // ' '（可打印）
```

**打印格式：**
- 可打印 ASCII（32-126）：带引号的字符 `'A'`
- 不可打印或 Unicode：十六进制表示法 `U+XXXX`

### 类型检查

使用 `typeof()` 检查值是否为 rune：

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "text";
let ch = s[0];
print(typeof(ch));              // "rune"（索引返回 rune）

let num = 65;
print(typeof(num));             // "i32"
```

### 比较

Rune 可以进行相等性比较：

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// 区分大小写
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// Rune 可以与整数比较（码点值）
print(a == 65);                 // true（隐式转换）
print('🚀' == 128640);          // true
```

**比较运算符：**
- `==` - 相等
- `!=` - 不相等
- `<`、`>`、`<=`、`>=` - 码点顺序

```hemlock
print('A' < 'B');               // true（65 < 66）
print('a' > 'Z');               // true（97 > 90）
```

## 处理字符串索引

字符串索引返回 rune，而不是字节：

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H'（rune）
let rocket = s[5];              // '🚀'（rune）

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// 如果需要可转换为字符串
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "🚀"
```

**重要：** 字符串索引使用码点位置，而不是字节偏移：

```hemlock
let text = "Hi🚀!";
// 码点位置：0='H', 1='i', 2='🚀', 3='!'
// 字节位置：0='H', 1='i', 2-5='🚀', 6='!'

let r = text[2];                // '🚀'（码点 2）
print(typeof(r));               // "rune"
```

## 示例

### 示例：字符分类

```hemlock
fn is_digit(r: rune): bool {
    return r >= '0' && r <= '9';
}

fn is_upper(r: rune): bool {
    return r >= 'A' && r <= 'Z';
}

fn is_lower(r: rune): bool {
    return r >= 'a' && r <= 'z';
}

print(is_digit('5'));           // true
print(is_upper('A'));           // true
print(is_lower('z'));           // true
```

### 示例：大小写转换

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // 转换为大写（减去 32）
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // 转换为小写（加上 32）
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### 示例：字符迭代

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Position " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Hi🚀");
// Position 0: 'H'
// Position 1: 'i'
// Position 2: U+1F680
```

### 示例：从 Rune 构建字符串

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let result = "";
    let i = 0;
    while (i < count) {
        result = result + ch;
        i = i + 1;
    }
    return result;
}

let line = repeat_char('=', 40);  // "========================================"
let stars = repeat_char('⭐', 5);  // "⭐⭐⭐⭐⭐"
```

## 常见模式

### 模式：字符过滤

```hemlock
fn filter_digits(s: string): string {
    let result = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}

let text = "abc123def456";
let digits = filter_digits(text);  // "123456"
```

### 模式：字符计数

```hemlock
fn count_char(s: string, target: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == target) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let text = "hello world";
let l_count = count_char(text, 'l');  // 3
let o_count = count_char(text, 'o');  // 2
```

## 最佳实践

1. **对字符操作使用 rune** - 不要尝试用字节处理文本
2. **字符串索引返回 rune** - 记住 `str[i]` 给你的是 rune
3. **Unicode 感知的比较** - Rune 可以处理任何 Unicode 字符
4. **需要时进行转换** - Rune 可以轻松转换为字符串和整数
5. **用表情符号测试** - 始终用多字节字符测试字符操作

## 常见陷阱

### 陷阱：Rune 与字节混淆

```hemlock
// 不要：将 rune 当作字节
let r: rune = '🚀';
let b: u8 = r;              // 错误：Rune 码点 128640 无法放入 u8

// 要：使用适当的转换
let r: rune = '🚀';
let code: i32 = r;          // 可以：128640
```

### 陷阱：字符串字节索引

```hemlock
// 不要：假设字节索引
let s = "🚀";
let byte = s.byte_at(0);    // 240（第一个 UTF-8 字节，不是完整字符）

// 要：使用码点索引
let s = "🚀";
let rune = s[0];            // '🚀'（完整字符）
let rune2 = s.char_at(0);   // '🚀'（显式方法）
```

## 相关主题

- [字符串](strings.md) - 字符串操作和 UTF-8 处理
- [类型](types.md) - 类型系统和转换
- [控制流](control-flow.md) - 在比较中使用 rune

## 另请参阅

- **Unicode 标准**：Unicode 码点由 Unicode 联盟定义
- **UTF-8 编码**：有关 UTF-8 详细信息，请参阅[字符串](strings.md)
- **类型转换**：有关转换规则，请参阅[类型](types.md)
