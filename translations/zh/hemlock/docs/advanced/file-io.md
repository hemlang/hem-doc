# Hemlock 文件 I/O

Hemlock 提供**文件对象 API**用于文件操作，具有适当的错误处理和资源管理。

## 目录

- [概述](#概述)
- [打开文件](#打开文件)
- [文件方法](#文件方法)
- [文件属性](#文件属性)
- [错误处理](#错误处理)
- [资源管理](#资源管理)
- [完整 API 参考](#完整-api-参考)
- [常见模式](#常见模式)
- [最佳实践](#最佳实践)

## 概述

文件对象 API 提供：

- **显式资源管理** - 文件必须手动关闭
- **多种打开模式** - 读取、写入、追加、读写
- **文本和二进制操作** - 读写文本和二进制数据
- **定位支持** - 文件内的随机访问
- **全面的错误消息** - 上下文感知的错误报告

**重要：** 文件不会自动关闭。您必须调用 `f.close()` 以避免文件描述符泄漏。

## 打开文件

使用 `open(path, mode?)` 打开文件：

```hemlock
let f = open("data.txt", "r");     // 读取模式（默认）
let f2 = open("output.txt", "w");  // 写入模式（截断）
let f3 = open("log.txt", "a");     // 追加模式
let f4 = open("data.bin", "r+");   // 读写模式
```

### 打开模式

| 模式 | 描述 | 文件必须存在 | 截断 | 位置 |
|------|------|------------|------|------|
| `"r"` | 读取（默认） | 是 | 否 | 开始 |
| `"w"` | 写入 | 否（创建） | 是 | 开始 |
| `"a"` | 追加 | 否（创建） | 否 | 结束 |
| `"r+"` | 读写 | 是 | 否 | 开始 |
| `"w+"` | 读写 | 否（创建） | 是 | 开始 |
| `"a+"` | 读取和追加 | 否（创建） | 否 | 结束 |

### 示例

**读取现有文件：**
```hemlock
let f = open("config.json", "r");
// 或简单地：
let f = open("config.json");  // "r" 是默认值
```

**创建新文件用于写入：**
```hemlock
let f = open("output.txt", "w");  // 创建或截断
```

**追加到文件：**
```hemlock
let f = open("log.txt", "a");  // 如果不存在则创建
```

**读写模式：**
```hemlock
let f = open("data.bin", "r+");  // 现有文件，可读写
```

## 文件方法

### 读取

#### read(size?: i32): string

从文件读取文本（可选的大小参数）。

**不带大小（读取全部）：**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // 从当前位置读取到 EOF
f.close();
```

**带大小（读取指定字节）：**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // 读取最多 1024 字节
let next = f.read(1024);   // 读取下一个 1024 字节
f.close();
```

**返回：** 包含读取数据的字符串，如果在 EOF 则返回空字符串

**示例 - 读取整个文件：**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**示例 - 分块读取：**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // 4KB 块
    if (chunk == "") { break; }  // 到达 EOF
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

读取二进制数据（返回缓冲区）。

**参数：**
- `size` (i32) - 要读取的字节数

**返回：** 包含读取字节的缓冲区

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // 读取 256 字节
print(binary.length);  // 256（如果 EOF 则更少）

// 访问单个字节
let first_byte = binary[0];
print(first_byte);

f.close();
```

### 写入

#### write(data: string): i32

向文件写入文本（返回写入的字节数）。

**参数：**
- `data` (string) - 要写入的文本

**返回：** 写入的字节数 (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Wrote " + typeof(written) + " bytes");  // "Wrote 14 bytes"
f.close();
```

**示例 - 写入多行：**
```hemlock
let f = open("output.txt", "w");
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");
f.close();
```

**示例 - 追加到日志文件：**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Application started\n");
f.write("[INFO] User logged in\n");
f.close();
```

#### write_bytes(data: buffer): i32

写入二进制数据（返回写入的字节数）。

**参数：**
- `data` (buffer) - 要写入的二进制数据

**返回：** 写入的字节数 (i32)

```hemlock
let f = open("output.bin", "w");

// 创建二进制数据
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Wrote " + typeof(bytes) + " bytes");

f.close();
```

### 定位

#### seek(position: i32): i32

移动到指定位置（返回新位置）。

**参数：**
- `position` (i32) - 从文件开头的字节偏移量

**返回：** 新位置 (i32)

```hemlock
let f = open("data.txt", "r");

// 移动到第 100 字节
f.seek(100);

// 从位置 100 读取
let data = f.read(50);

// 重置到开头
f.seek(0);

f.close();
```

**示例 - 随机访问：**
```hemlock
let f = open("records.dat", "r");

// 读取偏移量 1000 处的记录
f.seek(1000);
let record1 = f.read_bytes(100);

// 读取偏移量 2000 处的记录
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

获取文件中的当前位置。

**返回：** 当前字节偏移量 (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0（在开始处）

f.read(100);
let pos2 = f.tell();  // 100（读取 100 字节后）

f.seek(500);
let pos3 = f.tell();  // 500（定位后）

f.close();
```

### 关闭

#### close()

关闭文件（幂等，可以多次调用）。

```hemlock
let f = open("data.txt", "r");
// ... 使用文件
f.close();
f.close();  // 安全 - 第二次关闭不报错
```

**重要说明：**
- 始终在使用完后关闭文件以避免文件描述符泄漏
- 关闭是幂等的 - 可以安全地多次调用
- 关闭后，所有其他操作将报错
- 使用 `finally` 块确保即使出错也能关闭文件

## 文件属性

文件对象有三个只读属性：

### path: string

用于打开文件的文件路径。

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

文件打开时使用的模式。

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

文件是否已关闭。

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**示例 - 检查文件是否打开：**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... 处理内容
}

f.close();

if (f.closed) {
    print("File is now closed");
}
```

## 错误处理

所有文件操作都包含带上下文的适当错误消息。

### 常见错误

**文件未找到：**
```hemlock
let f = open("missing.txt", "r");
// 错误：Failed to open 'missing.txt': No such file or directory
```

**从已关闭的文件读取：**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// 错误：Cannot read from closed file 'data.txt'
```

**向只读文件写入：**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// 错误：Cannot write to file 'readonly.txt' opened in read-only mode
```

**从只写文件读取：**
```hemlock
let f = open("output.txt", "w");
f.read();
// 错误：Cannot read from file 'output.txt' opened in write-only mode
```

### 使用 try/catch

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Error reading file: " + e);
}
```

## 资源管理

### 基本模式

始终显式关闭文件：

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### 带错误处理（推荐）

使用 `finally` 确保即使出错也能关闭文件：

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // 始终关闭，即使出错
}
```

### 多个文件

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### 辅助函数模式

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// 使用：
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## 完整 API 参考

### 函数

| 函数 | 参数 | 返回 | 描述 |
|------|------|------|------|
| `open(path, mode?)` | path: string, mode?: string | File | 打开文件（模式默认为 "r"） |

### 方法

| 方法 | 参数 | 返回 | 描述 |
|------|------|------|------|
| `read(size?)` | size?: i32 | string | 读取文本（全部或指定字节） |
| `read_bytes(size)` | size: i32 | buffer | 读取二进制数据 |
| `write(data)` | data: string | i32 | 写入文本，返回写入的字节数 |
| `write_bytes(data)` | data: buffer | i32 | 写入二进制数据，返回写入的字节数 |
| `seek(position)` | position: i32 | i32 | 定位到位置，返回新位置 |
| `tell()` | - | i32 | 获取当前位置 |
| `close()` | - | null | 关闭文件（幂等） |

### 属性（只读）

| 属性 | 类型 | 描述 |
|------|------|------|
| `path` | string | 文件路径 |
| `mode` | string | 打开模式 |
| `closed` | bool | 文件是否已关闭 |

## 常见模式

### 读取整个文件

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### 写入整个文件

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### 追加到文件

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Event occurred\n");
```

### 读取行

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### 分块处理大文件

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // 4KB 块
            if (chunk == "") { break; }

            // 处理块
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### 二进制文件复制

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### 文件截断

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // "w" 模式截断
    f.close();
}

truncate_file("empty_me.txt");
```

### 随机访问读取

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

## 最佳实践

### 1. 始终使用 try/finally

```hemlock
// 好
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// 不好 - 出错时文件可能不关闭
let f = open("data.txt", "r");
let content = f.read();
process(content);  // 如果这里抛出异常，文件泄漏
f.close();
```

### 2. 操作前检查文件状态

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... 使用内容
}

f.close();
```

### 3. 使用适当的模式

```hemlock
// 只读？使用 "r"
let f = open("config.json", "r");

// 完全替换？使用 "w"
let f = open("output.txt", "w");

// 添加到末尾？使用 "a"
let f = open("log.txt", "a");
```

### 4. 优雅地处理错误

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Warning: Could not read " + path + ": " + e);
        return "";
    }
}
```

### 5. 按打开的相反顺序关闭文件

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... 使用文件
} finally {
    // 按相反顺序关闭
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. 避免完全读取大文件

```hemlock
// 对大文件不好
let f = open("huge.log", "r");
let content = f.read();  // 将整个文件加载到内存
f.close();

// 好 - 分块处理
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## 总结

Hemlock 的文件 I/O API 提供：

- 简单、显式的文件操作
- 文本和二进制支持
- 使用 seek/tell 的随机访问
- 带上下文的清晰错误消息
- 幂等的关闭操作

请记住：
- 始终手动关闭文件
- 使用 try/finally 确保资源安全
- 选择适当的打开模式
- 优雅地处理错误
- 分块处理大文件
