# 字符串 API 参考

Hemlock 字符串类型及全部 22 个字符串方法的完整参考。

---

## 概述

Hemlock 中的字符串是 **UTF-8 编码、可变、堆分配**的序列，具有完整的 Unicode 支持。所有操作都基于**码点**（字符）而非字节。

**主要特性：**
- UTF-8 编码 (U+0000 到 U+10FFFF)
- 可变（可以原地修改字符）
- 基于码点的索引
- 22 个内置方法
- 使用 `+` 运算符自动连接

---

## 字符串类型

**类型：** `string`

**属性：**
- `.length` - 码点（字符）数量
- `.byte_length` - UTF-8 字节数量

**字面量语法：** 双引号 `"text"`

**示例：**
```hemlock
let s = "hello";
print(s.length);        // 5 (codepoints)
print(s.byte_length);   // 5 (bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (one codepoint)
print(emoji.byte_length);   // 4 (four UTF-8 bytes)
```

---

## 索引

字符串支持使用 `[]` 进行基于码点的索引：

**读取访问：**
```hemlock
let s = "hello";
let ch = s[0];          // Returns rune 'h'
```

**写入访问：**
```hemlock
let s = "hello";
s[0] = 'H';             // Mutate with rune (now "Hello")
```

**UTF-8 示例：**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (one codepoint)
print(text[3]);         // '!'
```

---

## 连接

使用 `+` 运算符连接字符串和 rune：

**字符串 + 字符串：**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**字符串 + Rune：**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Rune + 字符串：**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**多重连接：**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## 字符串属性

### .length

获取 Unicode 码点（字符）数量。

**类型：** `i32`

**示例：**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (one codepoint)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 emoji)
```

---

### .byte_length

获取 UTF-8 字节数量。

**类型：** `i32`

**示例：**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 byte per ASCII char)

let emoji = "🚀";
print(emoji.byte_length); // 4 (emoji is 4 UTF-8 bytes)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 for emoji)
```

---

## 字符串方法

### 子字符串和切片

#### substr

按位置和长度提取子字符串。

**签名：**
```hemlock
string.substr(start: i32, length: i32): string
```

**参数：**
- `start` - 起始码点索引（从 0 开始）
- `length` - 要提取的码点数量

**返回值：** 新字符串

**示例：**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// UTF-8 example
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

按范围提取子字符串（结束位置不包含）。

**签名：**
```hemlock
string.slice(start: i32, end: i32): string
```

**参数：**
- `start` - 起始码点索引（从 0 开始）
- `end` - 结束码点索引（不包含）

**返回值：** 新字符串

**示例：**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// UTF-8 example
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### 搜索和查找

#### find

查找子字符串的第一次出现。

**签名：**
```hemlock
string.find(needle: string): i32
```

**参数：**
- `needle` - 要搜索的子字符串

**返回值：** 第一次出现的码点索引，如果未找到则返回 `-1`

**示例：**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (not found)
let pos3 = s.find("l");         // 2 (first 'l')
```

---

#### contains

检查字符串是否包含子字符串。

**签名：**
```hemlock
string.contains(needle: string): bool
```

**参数：**
- `needle` - 要搜索的子字符串

**返回值：** 如果找到返回 `true`，否则返回 `false`

**示例：**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### 分割和连接

#### split

按分隔符将字符串分割为数组。

**签名：**
```hemlock
string.split(delimiter: string): array
```

**参数：**
- `delimiter` - 分割依据的字符串

**返回值：** 字符串数组

**示例：**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

移除首尾空白字符。

**签名：**
```hemlock
string.trim(): string
```

**返回值：** 移除空白后的新字符串

**示例：**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

---

#### trim_start

移除字符串开头的空白字符。

**签名：**
```hemlock
string.trim_start(): string
```

**返回值：** 移除前导空白后的新字符串

**示例：**
```hemlock
let s = "  hello  ";
let clean = s.trim_start();     // "hello  "

let text = "\n\t  world  \n";
let clean2 = text.trim_start(); // "world  \n"
```

---

#### trim_end

移除字符串末尾的空白字符。

**签名：**
```hemlock
string.trim_end(): string
```

**返回值：** 移除尾部空白后的新字符串

**示例：**
```hemlock
let s = "  hello  ";
let clean = s.trim_end();       // "  hello"

let text = "\n\t  world  \n";
let clean2 = text.trim_end();   // "\n\t  world"
```

---

### 大小写转换

#### to_upper

将字符串转换为大写。

**签名：**
```hemlock
string.to_upper(): string
```

**返回值：** 大写的新字符串

**示例：**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

将字符串转换为小写。

**签名：**
```hemlock
string.to_lower(): string
```

**返回值：** 小写的新字符串

**示例：**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### 前缀和后缀

#### starts_with

检查字符串是否以指定前缀开始。

**签名：**
```hemlock
string.starts_with(prefix: string): bool
```

**参数：**
- `prefix` - 要检查的前缀

**返回值：** 如果字符串以该前缀开始返回 `true`，否则返回 `false`

**示例：**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

检查字符串是否以指定后缀结束。

**签名：**
```hemlock
string.ends_with(suffix: string): bool
```

**参数：**
- `suffix` - 要检查的后缀

**返回值：** 如果字符串以该后缀结束返回 `true`，否则返回 `false`

**示例：**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### 替换

#### replace

替换子字符串的第一次出现。

**签名：**
```hemlock
string.replace(old: string, new: string): string
```

**参数：**
- `old` - 要替换的子字符串
- `new` - 替换字符串

**返回值：** 替换第一次出现后的新字符串

**示例：**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (only first)
```

---

#### replace_all

替换子字符串的所有出现。

**签名：**
```hemlock
string.replace_all(old: string, new: string): string
```

**参数：**
- `old` - 要替换的子字符串
- `new` - 替换字符串

**返回值：** 替换所有出现后的新字符串

**示例：**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### 重复

#### repeat

将字符串重复 n 次。

**签名：**
```hemlock
string.repeat(count: i32): string
```

**参数：**
- `count` - 重复次数

**返回值：** 重复 count 次后的新字符串

**示例：**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### 字符访问

#### char_at

获取指定索引处的 Unicode 码点。

**签名：**
```hemlock
string.char_at(index: i32): rune
```

**参数：**
- `index` - 码点索引（从 0 开始）

**返回值：** Rune（Unicode 码点）

**示例：**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// UTF-8 example
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (rocket)
```

---

#### chars

将字符串转换为 rune 数组。

**签名：**
```hemlock
string.chars(): array
```

**返回值：** rune（码点）数组

**示例：**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// UTF-8 example
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### 字节访问

#### byte_at

获取指定索引处的字节值。

**签名：**
```hemlock
string.byte_at(index: i32): u8
```

**参数：**
- `index` - 字节索引（从 0 开始，不是码点索引）

**返回值：** 字节值 (u8)

**示例：**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// UTF-8 example
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (first UTF-8 byte)
```

---

#### bytes

将字符串转换为字节数组。

**签名：**
```hemlock
string.bytes(): array
```

**返回值：** u8 字节数组

**示例：**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// UTF-8 example
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 UTF-8 bytes)
```

---

#### to_bytes

将字符串转换为缓冲区。

**签名：**
```hemlock
string.to_bytes(): buffer
```

**返回值：** 包含 UTF-8 字节的缓冲区

**示例：**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// UTF-8 example
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**注意：** 这是一个遗留方法。大多数情况下推荐使用 `.bytes()`。

---

### 原始指针访问

#### byte_ptr

获取指向字符串内部 UTF-8 字节缓冲区的原始指针。这是零分配操作——不进行复制。

**签名：**
```hemlock
string.byte_ptr(): ptr
```

**返回值：** 指向字符串内部 UTF-8 字节的原始指针 (`ptr`)

**示例：**
```hemlock
let s = "Hello";
let p = s.byte_ptr();
print(typeof(p));              // "ptr"

// 通过指针读取字节
print(ptr_deref_u8(p));                    // 72 ('H')
print(ptr_deref_u8(ptr_offset(p, 1, 1))); // 101 ('e')
print(ptr_deref_u8(ptr_offset(p, 4, 1))); // 111 ('o')

// 使用 memcpy 复制字符串字节
let buf = alloc(5);
memcpy(buf, s.byte_ptr(), 5);
print(ptr_deref_u8(buf));  // 72
free(buf);

// 搭配 .byte_length 进行安全的大小跟踪
let emoji = "Hello 🚀";
let ep = emoji.byte_ptr();
print(emoji.byte_length);  // 10（字节操作使用 byte_length，而非 length）
```

**行为：**
- 返回直接指向字符串内部内存的指针（零拷贝）
- 只要字符串存活且未被修改，指针就有效
- 使用 `.byte_length`（不是 `.length`）来确定可通过指针访问的字节数
- 与 `.to_bytes()` 不同，这不会分配新缓冲区

**用例：**
- 需要字符串数据指针的 FFI 调用
- 与 C 函数的零拷贝互操作
- 避免分配的性能关键代码

**警告：** 调用 `byte_ptr()` 后修改字符串（如索引赋值）可能因字符串内部缓冲区重新分配而使指针失效。

---

### JSON 反序列化

#### deserialize

将 JSON 字符串解析为值。

**签名：**
```hemlock
string.deserialize(): any
```

**返回值：** 解析后的值（对象、数组、数字、字符串、布尔值或 null）

**示例：**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**支持的类型：**
- 对象：`{"key": value}`
- 数组：`[1, 2, 3]`
- 数字：`42`、`3.14`
- 字符串：`"text"`
- 布尔值：`true`、`false`
- 空值：`null`

**另请参阅：** 对象的 `.serialize()` 方法

---

## 方法链

字符串方法可以链接起来进行简洁的操作：

**示例：**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## 完整方法汇总

| 方法           | 签名                                         | 返回值    | 描述                            |
|----------------|----------------------------------------------|-----------|--------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`  | 按位置/长度提取子字符串         |
| `slice`        | `(start: i32, end: i32)`                     | `string`  | 按范围提取子字符串              |
| `find`         | `(needle: string)`                           | `i32`     | 查找第一次出现（未找到返回 -1） |
| `contains`     | `(needle: string)`                           | `bool`    | 检查是否包含子字符串            |
| `split`        | `(delimiter: string)`                        | `array`   | 分割为数组                      |
| `trim`         | `()`                                         | `string`  | 移除空白字符                    |
| `trim_start`   | `()`                                         | `string`  | 移除前导空白                    |
| `trim_end`     | `()`                                         | `string`  | 移除尾部空白                    |
| `to_upper`     | `()`                                         | `string`  | 转换为大写                      |
| `to_lower`     | `()`                                         | `string`  | 转换为小写                      |
| `starts_with`  | `(prefix: string)`                           | `bool`    | 检查是否以前缀开始              |
| `ends_with`    | `(suffix: string)`                           | `bool`    | 检查是否以后缀结束              |
| `replace`      | `(old: string, new: string)`                 | `string`  | 替换第一次出现                  |
| `replace_all`  | `(old: string, new: string)`                 | `string`  | 替换所有出现                    |
| `repeat`       | `(count: i32)`                               | `string`  | 将字符串重复 n 次               |
| `char_at`      | `(index: i32)`                               | `rune`    | 获取指定索引处的码点            |
| `byte_at`      | `(index: i32)`                               | `u8`      | 获取指定索引处的字节            |
| `chars`        | `()`                                         | `array`   | 转换为 rune 数组                |
| `bytes`        | `()`                                         | `array`   | 转换为字节数组                  |
| `to_bytes`     | `()`                                         | `buffer`  | 转换为缓冲区（遗留）            |
| `byte_ptr`     | `()`                                         | `ptr`     | 指向内部 UTF-8 字节的原始指针   |
| `deserialize`  | `()`                                         | `any`     | 解析 JSON 字符串                |

---

## 另请参阅

- [类型系统](type-system.md) - 字符串类型详情
- [数组 API](array-api.md) - split() 结果的数组方法
- [运算符](operators.md) - 字符串连接运算符
