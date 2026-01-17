# 字符串

Hemlock 字符串是**UTF-8 优先的可变序列**，具有完整的 Unicode 支持和丰富的文本处理方法。与许多语言不同，Hemlock 字符串是可变的，并且原生支持 Unicode 码点操作。

## 概述

```hemlock
let s = "hello";
s[0] = 'H';             // 使用 rune 修改（现在是 "Hello"）
print(s.length);        // 5（码点数量）
let c = s[0];           // 返回 rune（Unicode 码点）
let msg = s + " world"; // 连接
let emoji = "🚀";
print(emoji.length);    // 1（一个码点）
print(emoji.byte_length); // 4（四个 UTF-8 字节）
```

## 属性

Hemlock 字符串具有以下关键特性：

- **UTF-8 编码** - 完整的 Unicode 支持（U+0000 到 U+10FFFF）
- **可变** - 与 Python、JavaScript 和 Java 的字符串不同
- **基于码点的索引** - 返回 `rune`（Unicode 码点），而非字节
- **堆分配** - 带有内部容量跟踪
- **两个长度属性**：
  - `.length` - 码点数量（字符数）
  - `.byte_length` - 字节数量（UTF-8 编码大小）

## UTF-8 行为

所有字符串操作都使用**码点**（字符），而非字节：

```hemlock
let text = "Hello🚀World";
print(text.length);        // 11（码点）
print(text.byte_length);   // 15（字节，emoji 是 4 字节）

// 索引使用码点
let h = text[0];           // 'H'（rune）
let rocket = text[5];      // '🚀'（rune）
```

**多字节字符计为一个：**
```hemlock
"Hello".length;      // 5
"🚀".length;         // 1（一个 emoji）
"你好".length;       // 2（两个中文字符）
"café".length;       // 4（é 是一个码点）
```

## 字符串字面量

```hemlock
// 基本字符串
let s1 = "hello";
let s2 = "world";

// 带有转义序列
let s3 = "Line 1\nLine 2\ttabbed";
let s4 = "Quote: \"Hello\"";
let s5 = "Backslash: \\";

// Unicode 字符
let s6 = "🚀 Emoji";
let s7 = "中文字符";
```

## 模板字符串（字符串插值）

使用反引号创建带有嵌入表达式的模板字符串：

```hemlock
let name = "Alice";
let age = 30;

// 基本插值
let greeting = `Hello, ${name}!`;           // "Hello, Alice!"
let info = `${name} is ${age} years old`;   // "Alice is 30 years old"

// 插值中的表达式
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// 方法调用
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// 嵌套对象
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lives in ${person.city}`;  // "Bob lives in NYC"

// 多行（保留换行符）
let multi = `Line 1
Line 2
Line 3`;
```

**模板字符串特性：**
- `${...}` 内的表达式会被求值并转换为字符串
- 可以使用任何有效表达式（变量、函数调用、算术运算）
- 反引号字符串支持与普通字符串相同的转义序列
- 用于构建动态字符串而无需连接操作

### 模板字符串中的转义

要在模板字符串中包含字面量 `${`，请转义美元符号：

```hemlock
let price = 100;
let text = `Price: \${price} or ${price}`;
// "Price: ${price} or 100"

// 字面量反引号
let code = `Use \` for template strings`;
// "Use ` for template strings"
```

### 复杂表达式

模板字符串可以包含任何有效表达式：

```hemlock
// 类三元表达式
let age = 25;
let status = `Status: ${age >= 18 ? "adult" : "minor"}`;

// 数组访问
let items = ["apple", "banana", "cherry"];
let first = `First item: ${items[0]}`;

// 带参数的函数调用
fn format_price(p) { return "$" + p; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: $99.99"

// 链式方法调用
let name = "alice";
let formatted = `Hello, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hello, Alice!"
```

### 模板字符串与连接对比

模板字符串通常比连接更清晰：

```hemlock
// 连接（较难阅读）
let msg1 = "Hello, " + name + "! You have " + count + " messages.";

// 模板字符串（更易阅读）
let msg2 = `Hello, ${name}! You have ${count} messages.`;
```

## 索引和修改

### 读取字符

索引返回 `rune`（Unicode 码点）：

```hemlock
let s = "Hello";
let first = s[0];      // 'H'（rune）
let last = s[4];       // 'o'（rune）

// UTF-8 示例
let emoji = "Hi🚀!";
let rocket = emoji[2];  // '🚀'（码点索引 2 处的 rune）
```

### 写入字符

字符串是可变的 - 可以修改单个字符：

```hemlock
let s = "hello";
s[0] = 'H';            // 现在是 "Hello"
s[4] = '!';            // 现在是 "Hell!"

// Unicode 示例
let msg = "Go!";
msg[0] = '🚀';         // 现在是 "🚀o!"
```

## 连接

使用 `+` 连接字符串：

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// 使用变量
let name = "Alice";
let msg = "Hi, " + name + "!";  // "Hi, Alice!"

// 使用 rune（参见 Runes 文档）
let s = "Hello" + '!';          // "Hello!"
```

## 字符串方法

Hemlock 提供 19 个字符串方法用于全面的文本操作。

### 子字符串和切片

**`substr(start, length)`** - 按位置和长度提取子字符串：
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"（从 6 开始，长度 5）
let first = s.substr(0, 5);     // "hello"

// UTF-8 示例
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"（位置 2，长度 1）
```

**`slice(start, end)`** - 按范围提取子字符串（end 不包含在内）：
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello"（索引 0 到 4）
let slice2 = s.slice(6, 11);    // "world"
```

**区别：**
- `substr(start, length)` - 使用长度参数
- `slice(start, end)` - 使用结束索引（不包含）

### 搜索和查找

**`find(needle)`** - 查找首次出现的位置：
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6（首次出现的索引）
let pos2 = s.find("foo");       // -1（未找到）
let pos3 = s.find("l");         // 2（第一个 'l'）
```

**`contains(needle)`** - 检查字符串是否包含子字符串：
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### 分割和修剪

**`split(delimiter)`** - 分割成字符串数组：
```hemlock
let csv = "apple,banana,cherry";
let parts = csv.split(",");     // ["apple", "banana", "cherry"]

let words = "one two three".split(" ");  // ["one", "two", "three"]

// 空分隔符按字符分割
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - 移除前后空白：
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### 大小写转换

**`to_upper()`** - 转换为大写：
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// 保留非 ASCII 字符
let s2 = "café";
let upper2 = s2.to_upper();     // "CAFÉ"
```

**`to_lower()`** - 转换为小写：
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### 前缀/后缀检查

**`starts_with(prefix)`** - 检查是否以前缀开头：
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - 检查是否以后缀结尾：
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### 替换

**`replace(old, new)`** - 替换首次出现：
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo"（仅第一个）
```

**`replace_all(old, new)`** - 替换所有出现：
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### 重复

**`repeat(count)`** - 重复字符串 n 次：
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### 字符和字节访问

**`char_at(index)`** - 获取指定索引处的 Unicode 码点（返回 rune）：
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h'（rune）

// UTF-8 示例
let emoji = "🚀";
let rocket = emoji.char_at(0);  // 返回 rune U+1F680
```

**`chars()`** - 转换为 rune 数组（码点）：
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']（rune 数组）

// UTF-8 示例
let text = "Hi🚀";
let chars2 = text.chars();      // ['H', 'i', '🚀']
```

**`byte_at(index)`** - 获取指定索引处的字节值（返回 u8）：
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104（'h' 的 ASCII 值）

// UTF-8 示例
let emoji = "🚀";
let first_byte = emoji.byte_at(0);  // 240（第一个 UTF-8 字节）
```

**`bytes()`** - 转换为字节数组（u8 值）：
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]（u8 数组）

// UTF-8 示例
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128]（4 个 UTF-8 字节）
```

**`to_bytes()`** - 转换为 buffer 以进行底层访问：
```hemlock
let s = "hello";
let buf = s.to_bytes();         // 返回包含 UTF-8 字节的 buffer
print(buf.length);              // 5
free(buf);                      // 记得释放
```

## 方法链式调用

所有字符串方法都返回新字符串，支持链式调用：

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## 完整方法参考

| 方法 | 参数 | 返回值 | 描述 |
|--------|-----------|---------|-------------|
| `substr(start, length)` | i32, i32 | string | 按位置和长度提取子字符串 |
| `slice(start, end)` | i32, i32 | string | 按范围提取子字符串（end 不包含在内） |
| `find(needle)` | string | i32 | 查找首次出现的位置（未找到返回 -1） |
| `contains(needle)` | string | bool | 检查是否包含子字符串 |
| `split(delimiter)` | string | array | 分割成字符串数组 |
| `trim()` | - | string | 移除前后空白 |
| `to_upper()` | - | string | 转换为大写 |
| `to_lower()` | - | string | 转换为小写 |
| `starts_with(prefix)` | string | bool | 检查是否以前缀开头 |
| `ends_with(suffix)` | string | bool | 检查是否以后缀结尾 |
| `replace(old, new)` | string, string | string | 替换首次出现 |
| `replace_all(old, new)` | string, string | string | 替换所有出现 |
| `repeat(count)` | i32 | string | 重复字符串 n 次 |
| `char_at(index)` | i32 | rune | 获取指定索引处的码点 |
| `byte_at(index)` | i32 | u8 | 获取指定索引处的字节值 |
| `chars()` | - | array | 转换为 rune 数组 |
| `bytes()` | - | array | 转换为 u8 字节数组 |
| `to_bytes()` | - | buffer | 转换为 buffer（需要释放） |

## 示例

### 示例：文本处理

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // 规范化空白
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### 示例：CSV 解析器

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "apple, banana , cherry";
let fields = parse_csv_line(csv);  // ["apple", "banana", "cherry"]
```

### 示例：单词计数器

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "The quick brown fox";
let count = count_words(sentence);  // 4
```

### 示例：字符串验证

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## 内存管理

字符串是堆分配的，带有内部引用计数：

- **创建**：在堆上分配，带有容量跟踪
- **连接**：创建新字符串（旧字符串不变）
- **方法**：大多数方法返回新字符串
- **生命周期**：字符串使用引用计数，作用域退出时自动释放

**自动清理：**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // 新分配
}  // 函数返回时 s 和 s2 都自动释放
```

**注意：** 局部字符串变量在超出作用域时自动清理。仅在需要提前清理（作用域结束前）或处理长期存活/全局数据时使用 `free()`。详见 [内存管理](memory.md#internal-reference-counting)。

## 最佳实践

1. **使用码点索引** - 字符串使用码点位置，而非字节偏移
2. **使用 Unicode 测试** - 始终使用多字节字符测试字符串操作
3. **优先使用不可变操作** - 使用返回新字符串的方法，而非直接修改
4. **检查边界** - 字符串索引不进行边界检查（无效时返回 null/错误）
5. **规范化输入** - 对用户输入使用 `trim()` 和 `to_lower()`

## 常见陷阱

### 陷阱：字节与码点混淆

```hemlock
let emoji = "🚀";
print(emoji.length);        // 1（码点）
print(emoji.byte_length);   // 4（字节）

// 不要混用字节和码点操作
let byte = emoji.byte_at(0);  // 240（第一个字节）
let char = emoji.char_at(0);  // '🚀'（完整码点）
```

### 陷阱：修改的意外情况

```hemlock
let s1 = "hello";
let s2 = s1;       // 浅拷贝
s1[0] = 'H';       // 修改 s1
print(s2);         // 仍然是 "hello"（字符串是值类型）
```

## 相关主题

- [Runes](runes.md) - 字符串索引中使用的 Unicode 码点类型
- [数组](arrays.md) - 字符串方法经常返回或使用数组
- [类型](types.md) - 字符串类型详情和转换

## 另请参阅

- **UTF-8 编码**：参见 CLAUDE.md 中的 "Strings" 部分
- **类型转换**：参见 [类型](types.md) 了解字符串转换
- **内存**：参见 [内存](memory.md) 了解字符串分配细节
