# 文件 API 参考

Hemlock 文件 I/O 系统的完整参考文档。

---

## 概述

Hemlock 提供了一个**文件对象 API**，用于具有适当错误处理和资源管理的文件操作。文件必须手动打开和关闭。

**主要特性：**
- 带有方法的文件对象
- 读写文本和二进制数据
- 定位和位置操作
- 适当的错误消息
- 手动资源管理（无 RAII）

---

## 文件类型

**类型：** `file`

**描述：** 用于 I/O 操作的文件句柄

**属性（只读）：**
- `.path` - 文件路径 (string)
- `.mode` - 打开模式 (string)
- `.closed` - 文件是否已关闭 (bool)

---

## 打开文件

### open

打开文件用于读取、写入或两者兼顾。

**签名：**
```hemlock
open(path: string, mode?: string): file
```

**参数：**
- `path` - 文件路径（相对或绝对）
- `mode`（可选）- 打开模式（默认：`"r"`）

**返回值：** 文件对象

**模式：**
- `"r"` - 读取（默认）
- `"w"` - 写入（截断现有文件）
- `"a"` - 追加
- `"r+"` - 读写
- `"w+"` - 读写（截断）
- `"a+"` - 读取和追加

**示例：**
```hemlock
// 读取模式（默认）
let f = open("data.txt");
let f_read = open("data.txt", "r");

// 写入模式（截断）
let f_write = open("output.txt", "w");

// 追加模式
let f_append = open("log.txt", "a");

// 读写模式
let f_rw = open("data.bin", "r+");

// 读写（截断）
let f_rw_trunc = open("output.bin", "w+");

// 读取/追加
let f_ra = open("log.txt", "a+");
```

**错误处理：**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Failed to open:", e);
    // 错误：Failed to open 'missing.txt': No such file or directory
}
```

**重要：** 文件必须使用 `f.close()` 手动关闭以避免文件描述符泄漏。

---

## 文件方法

### 读取

#### read

从文件读取文本。

**签名：**
```hemlock
file.read(size?: i32): string
```

**参数：**
- `size`（可选）- 要读取的字节数（如果省略，读取到文件末尾）

**返回值：** 包含文件内容的字符串

**示例：**
```hemlock
let f = open("data.txt", "r");

// 读取整个文件
let all = f.read();
print(all);

// 读取指定数量的字节
let chunk = f.read(1024);

f.close();
```

**行为：**
- 从当前文件位置读取
- 在文件末尾返回空字符串
- 前进文件位置

**错误：**
- 从已关闭的文件读取
- 从只写文件读取

---

#### read_bytes

从文件读取二进制数据。

**签名：**
```hemlock
file.read_bytes(size: i32): buffer
```

**参数：**
- `size` - 要读取的字节数

**返回值：** 包含二进制数据的缓冲区

**示例：**
```hemlock
let f = open("data.bin", "r");

// 读取 256 字节
let binary = f.read_bytes(256);
print(binary.length);       // 256

// 处理二进制数据
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**行为：**
- 读取确切数量的字节
- 返回缓冲区（不是字符串）
- 前进文件位置

---

### 写入

#### write

向文件写入文本。

**签名：**
```hemlock
file.write(data: string): i32
```

**参数：**
- `data` - 要写入的字符串

**返回值：** 写入的字节数 (i32)

**示例：**
```hemlock
let f = open("output.txt", "w");

// 写入文本
let written = f.write("Hello, World!\n");
print("Wrote", written, "bytes");

// 多次写入
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");

f.close();
```

**行为：**
- 在当前文件位置写入
- 返回写入的字节数
- 前进文件位置

**错误：**
- 向已关闭的文件写入
- 向只读文件写入

---

#### write_bytes

向文件写入二进制数据。

**签名：**
```hemlock
file.write_bytes(data: buffer): i32
```

**参数：**
- `data` - 要写入的缓冲区

**返回值：** 写入的字节数 (i32)

**示例：**
```hemlock
let f = open("output.bin", "w");

// 创建缓冲区
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// 写入缓冲区
let written = f.write_bytes(buf);
print("Wrote", written, "bytes");

f.close();
```

**行为：**
- 将缓冲区内容写入文件
- 返回写入的字节数
- 前进文件位置

---

### 定位

#### seek

将文件位置移动到指定的字节偏移量。

**签名：**
```hemlock
file.seek(position: i32): i32
```

**参数：**
- `position` - 从文件开头的字节偏移量

**返回值：** 新的文件位置 (i32)

**示例：**
```hemlock
let f = open("data.txt", "r");

// 跳转到第 100 字节
f.seek(100);

// 从该位置读取
let chunk = f.read(50);

// 重置到开头
f.seek(0);

// 从开头读取
let all = f.read();

f.close();
```

**行为：**
- 将文件位置设置为绝对偏移量
- 返回新位置
- 允许定位到文件末尾之后（写入时会在文件中创建空洞）

---

#### tell

获取当前文件位置。

**签名：**
```hemlock
file.tell(): i32
```

**返回值：** 从文件开头的当前字节偏移量 (i32)

**示例：**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0（在开头）

f.read(100);
print(f.tell());        // 100（读取后）

f.seek(50);
print(f.tell());        // 50（定位后）

f.close();
```

---

### 关闭

#### close

关闭文件（幂等）。

**签名：**
```hemlock
file.close(): null
```

**返回值：** `null`

**示例：**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// 可以安全地多次调用
f.close();  // 无错误
f.close();  // 无错误
```

**行为：**
- 关闭文件句柄
- 刷新任何待处理的写入
- 幂等（可以安全地多次调用）
- 将 `.closed` 属性设置为 `true`

**重要：** 完成后始终关闭文件以避免文件描述符泄漏。

---

## 文件属性

### .path

获取文件路径。

**类型：** `string`

**访问：** 只读

**示例：**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

获取打开模式。

**类型：** `string`

**访问：** 只读

**示例：**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

检查文件是否已关闭。

**类型：** `bool`

**访问：** 只读

**示例：**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## 错误处理

所有文件操作都包含带有上下文的适当错误消息：

### 文件未找到
```hemlock
let f = open("missing.txt", "r");
// 错误：Failed to open 'missing.txt': No such file or directory
```

### 从已关闭的文件读取
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// 错误：Cannot read from closed file 'data.txt'
```

### 向只读文件写入
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// 错误：Cannot write to file 'readonly.txt' opened in read-only mode
```

### 使用 try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("File error:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## 资源管理模式

### 基本模式

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### 带错误处理

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // 始终关闭，即使出错
}
```

### 安全模式

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... 处理内容 ...
} catch (e) {
    print("Error:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## 使用示例

### 读取整个文件

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### 写入文本文件

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### 追加到文件

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Log entry 1");
append_file("log.txt", "Log entry 2");
```

### 读取二进制文件

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Read", binary.length, "bytes");
```

### 写入二进制文件

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### 逐行读取文件

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line", i, ":", lines[i]);
    i = i + 1;
}
```

### 复制文件

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### 分块读取文件

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // 每次读取 1KB
        if (chunk.length == 0) {
            break;  // 文件末尾
        }

        // 处理块
        print("Processing", chunk.length, "bytes");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## 完整方法总结

| 方法          | 签名                     | 返回值    | 描述                         |
|---------------|--------------------------|-----------|------------------------------|
| `read`        | `(size?: i32)`           | `string`  | 读取文本                     |
| `read_bytes`  | `(size: i32)`            | `buffer`  | 读取二进制数据               |
| `write`       | `(data: string)`         | `i32`     | 写入文本                     |
| `write_bytes` | `(data: buffer)`         | `i32`     | 写入二进制数据               |
| `seek`        | `(position: i32)`        | `i32`     | 设置文件位置                 |
| `tell`        | `()`                     | `i32`     | 获取文件位置                 |
| `close`       | `()`                     | `null`    | 关闭文件（幂等）             |

---

## 完整属性总结

| 属性      | 类型     | 访问       | 描述                     |
|-----------|----------|------------|--------------------------|
| `.path`   | `string` | 只读       | 文件路径                 |
| `.mode`   | `string` | 只读       | 打开模式                 |
| `.closed` | `bool`   | 只读       | 文件是否已关闭           |

---

## 从旧 API 迁移

**旧 API（已移除）：**
- `read_file(path)` - 使用 `open(path, "r").read()`
- `write_file(path, data)` - 使用 `open(path, "w").write(data)`
- `append_file(path, data)` - 使用 `open(path, "a").write(data)`
- `file_exists(path)` - 暂无替代

**迁移示例：**
```hemlock
// 旧版（v0.0）
let content = read_file("data.txt");
write_file("output.txt", content);

// 新版（v0.1）
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## 另请参阅

- [内置函数](builtins.md) - `open()` 函数
- [内存 API](memory-api.md) - 缓冲区类型
- [字符串 API](string-api.md) - 用于文本处理的字符串方法
