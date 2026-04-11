# 内存 API 参考

Hemlock 内存管理函数和指针类型的完整参考文档。

---

## 概述

Hemlock 提供**手动内存管理**，具有显式的分配和释放。内存通过两种指针类型管理：原始指针（`ptr`）和安全缓冲区（`buffer`）。

**核心原则：**
- 显式分配和释放
- 无垃圾回收
- 用户负责调用 `free()`
- 内部引用计数用于作用域/重新赋值安全（见下文）

### 内部引用计数

运行时内部使用引用计数来管理对象在作用域中的生命周期。对于大多数局部变量，清理是自动的。

**自动（无需 `free()`）：**
- 引用计数类型（buffer、array、object、string）的局部变量在作用域退出时释放
- 变量重新赋值时释放旧值
- 容器释放时释放容器元素

**需要手动 `free()`：**
- 来自 `alloc()` 的原始指针 - 始终需要
- 作用域结束前的提前清理
- 长期存在/全局数据

详见 [内存管理指南](../language-guide/memory.md#internal-reference-counting)。

---

## 指针类型

### ptr（原始指针）

**类型：** `ptr`

**描述：** 原始内存地址，无边界检查或跟踪。

**大小：** 8 字节

**用例：**
- 底层内存操作
- FFI（外部函数接口）
- 最高性能（无开销）

**安全性：** 不安全 - 无边界检查，用户必须跟踪生命周期

**示例：**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer（安全缓冲区）

**类型：** `buffer`

**描述：** 带边界检查的安全指针包装器。

**结构：** 指针 + 长度 + 容量 + 引用计数

**属性：**
- `.length` - 缓冲区大小 (i32)
- `.capacity` - 已分配容量 (i32)

**用例：**
- 大多数内存分配
- 安全性重要时
- 动态数组

**安全性：** 索引访问时进行边界检查

**引用计数：** 缓冲区内部进行引用计数。作用域退出或变量重新赋值时自动释放。使用 `free()` 进行提前清理或用于长期存在的数据。

**示例：**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // 边界检查
print(b.length);        // 64
free(b);
```

---

## 内存分配函数

### alloc

分配原始内存。

**签名：**
```hemlock
alloc(size: i32): ptr
```

**参数：**
- `size` - 要分配的字节数

**返回值：** 指向已分配内存的指针 (`ptr`)

**示例：**
```hemlock
let p = alloc(1024);        // 分配 1KB
memset(p, 0, 1024);         // 初始化为零
free(p);                    // 完成后释放

// 为结构分配
let struct_size = 16;
let p2 = alloc(struct_size);
```

**行为：**
- 返回未初始化的内存
- 必须手动释放内存
- 分配失败时返回 `null`（调用者必须检查）

**另请参阅：** `buffer()` 作为更安全的替代方案

---

### buffer

分配带边界检查的安全缓冲区。

**签名：**
```hemlock
buffer(size: i32): buffer
```

**参数：**
- `size` - 缓冲区大小（字节）

**返回值：** 缓冲区对象

**示例：**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// 带边界检查的访问
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // 错误：越界

free(buf);
```

**属性：**
- `.length` - 当前大小 (i32)
- `.capacity` - 已分配容量 (i32)

**行为：**
- 将内存初始化为零
- 在索引访问时提供边界检查
- 分配失败时返回 `null`（调用者必须检查）
- 必须手动释放

---

### free

释放已分配的内存。

**签名：**
```hemlock
free(ptr: ptr | buffer): null
```

**参数：**
- `ptr` - 要释放的指针或缓冲区

**返回值：** `null`

**示例：**
```hemlock
// 释放原始指针
let p = alloc(1024);
free(p);

// 释放缓冲区
let buf = buffer(256);
free(buf);
```

**行为：**
- 释放由 `alloc()` 或 `buffer()` 分配的内存
- 双重释放会导致崩溃（用户有责任避免）
- 释放无效指针会导致未定义行为

**重要：** 你分配，你释放。没有自动清理。

---

### realloc

调整已分配内存的大小。

**签名：**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**参数：**
- `ptr` - 要调整大小的指针
- `new_size` - 新大小（字节）

**返回值：** 指向调整大小后内存的指针（可能是不同的地址）

**示例：**
```hemlock
let p = alloc(100);
// ... 使用内存 ...

// 需要更多空间
p = realloc(p, 200);        // 现在是 200 字节
// ... 使用扩展的内存 ...

free(p);
```

**行为：**
- 可能将内存移动到新位置
- 保留现有数据（直到旧/新大小的最小值）
- 成功 realloc 后旧指针无效（使用返回的指针）
- 如果 new_size 更小，数据会被截断
- 分配失败时返回 `null`（原始指针仍然有效）

**重要：** 始终检查 `null` 并用结果更新指针变量。

---

## 内存操作

### memset

用字节值填充内存。

**签名：**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**参数：**
- `ptr` - 指向内存的指针
- `byte` - 要填充的字节值 (0-255)
- `size` - 要填充的字节数

**返回值：** `null`

**示例：**
```hemlock
let p = alloc(100);

// 清零内存
memset(p, 0, 100);

// 用特定值填充
memset(p, 0xFF, 100);

// 初始化缓冲区
let buf = alloc(256);
memset(buf, 65, 256);       // 用 'A' 填充

free(p);
free(buf);
```

**行为：**
- 将字节值写入范围内的每个字节
- 字节值截断为 8 位 (0-255)
- 无边界检查（不安全）

---

### memcpy

从源复制内存到目标。

**签名：**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**参数：**
- `dest` - 目标指针
- `src` - 源指针
- `size` - 要复制的字节数

**返回值：** `null`

**示例：**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// 初始化源
memset(src, 65, 100);

// 复制到目标
memcpy(dest, src, 100);

// dest 现在包含与 src 相同的数据

free(src);
free(dest);
```

**行为：**
- 逐字节从 src 复制到 dest
- 无边界检查（不安全）
- 重叠区域行为未定义（小心使用）

---

## 类型化内存操作

### sizeof

获取类型的字节大小。

**签名：**
```hemlock
sizeof(type): i32
```

**参数：**
- `type` - 类型标识符（例如 `i32`、`f64`、`ptr`）

**返回值：** 字节大小 (i32)

**类型大小：**

| 类型 | 大小（字节）|
|------|--------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`、`integer` | 4 |
| `i64` | 8 |
| `u8`、`byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`、`number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**示例：**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// 计算数组分配大小
let count = 100;
let total = sizeof(i32) * count; // 400 字节
```

**行为：**
- 对未知类型返回 0
- 接受类型标识符和类型字符串

---

### talloc

分配类型化值数组。

**签名：**
```hemlock
talloc(type, count: i32): ptr
```

**参数：**
- `type` - 要分配的类型（例如 `i32`、`f64`、`ptr`）
- `count` - 元素数量（必须为正数）

**返回值：** 指向已分配数组的指针，分配失败时返回 `null`

**示例：**
```hemlock
let arr = talloc(i32, 100);      // 100 个 i32 的数组（400 字节）
let floats = talloc(f64, 50);    // 50 个 f64 的数组（400 字节）
let bytes = talloc(u8, 1024);    // 1024 字节的数组

// 始终检查分配失败
if (arr == null) {
    panic("allocation failed");
}

// 使用已分配的内存
// ...

free(arr);
free(floats);
free(bytes);
```

**行为：**
- 分配 `sizeof(type) * count` 字节
- 返回未初始化的内存
- 必须使用 `free()` 手动释放内存
- 分配失败时返回 `null`（调用者必须检查）
- 如果 count 不是正数则 panic

---

## 缓冲区属性

### .length

获取缓冲区大小。

**类型：** `i32`

**访问：** 只读

**示例：**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

获取缓冲区容量。

**类型：** `i32`

**访问：** 只读

**示例：**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**注意：** 目前，对于使用 `buffer()` 创建的缓冲区，`.length` 和 `.capacity` 相同。

---

## 指针/缓冲区互操作

所有 `ptr_read_*`、`ptr_write_*` 和 `ptr_deref_*` 内置函数直接接受 `ptr` 和 `buffer` 类型。当传入缓冲区时，操作使用缓冲区的底层数据指针。

```hemlock
let buf = buffer(16);

// 直接写入缓冲区（无需先提取 ptr）
ptr_write_i32(buf, 42);
ptr_write_f64(ptr_offset(buffer_ptr(buf), 4), 3.14);

// 直接从缓冲区读取
let val = ptr_read_i32(buf);      // 42
let fval = ptr_deref_i32(buf);    // 42

// 原始指针也同样工作
let p = alloc(8);
ptr_write_i32(p, 99);
let pval = ptr_read_i32(p);      // 99
free(p);
```

这消除了在每次类型化读写操作前调用 `buffer_ptr()` 的需要，使基于缓冲区的代码更简洁。

---

## 缓冲区方法

### .slice

创建缓冲区内存的零拷贝视图。返回的视图与父缓冲区共享相同的底层内存——对原始数据的修改通过视图可见，反之亦然。

**签名：**
```hemlock
buffer.slice(start: i32, end?: i32): buffer
```

**参数：**
- `start` - 起始字节偏移量（从 0 开始，包含）。负值钳位为 0。
- `end` - 结束字节偏移量（不包含）。省略时默认为 `buffer.length`。超过缓冲区长度的值会被钳位。

**返回值：** 缓冲区视图（零拷贝）

**示例：**
```hemlock
let buf = buffer(10);
for (let i = 0; i < 10; i++) {
    buf[i] = i + 65;  // A=65, B=66, ...
}

// 基本切片
let view = buf.slice(2, 5);
print(view.length);    // 3
print(view[0]);        // 67 (C)
print(view[1]);        // 68 (D)
print(view[2]);        // 69 (E)

// 零拷贝证明：修改原始数据通过视图可见
buf[3] = 90;           // 将 D(68) 改为 Z(90)
print(view[1]);        // 90（反映父缓冲区的更改）

// 单参数切片（从 start 到末尾）
let tail = buf.slice(7);
print(tail.length);    // 3

// 链式切片（视图的视图）
let inner = view.slice(1, 3);
print(inner.length);   // 2
print(inner[0]);       // 90 (Z)

// 空切片
let empty = buf.slice(5, 5);
print(empty.length);   // 0
```

**行为：**
- 返回零拷贝视图——不为数据分配内存
- 视图持有对根缓冲区的引用（防止释放后使用）
- 链式切片（视图的视图）跟踪根所有者，而非中间视图
- 边界检查相对于视图的范围执行
- 超范围的 `start`/`end` 值会被钳位到有效边界
- **不能** `free()` 视图缓冲区——只有根缓冲区应被释放
- 释放父缓冲区前将视图设为 `null` 以释放引用

---

## 类型化缓冲区读写方法

缓冲区提供端序感知的类型化读写方法，用于构建和解析二进制数据结构，如网络包、文件格式和线协议。这些方法带有边界检查，越界访问会引发运行时错误。

### 写入方法

在字节偏移量处写入类型化值。`_le` 和 `_be` 后缀分别指定小端和大端字节序。

```hemlock
let pkt = buffer(64);
let offset = 0;

// 构建数据包头
pkt.write_u16_be(offset, 0x0800);    // EtherType: IPv4
offset += 2;
pkt.write_u8(offset, 0x45);          // 版本 + IHL
offset += 1;
pkt.write_u8(offset, 0x00);          // DSCP/ECN
offset += 1;
pkt.write_u16_be(offset, 40);        // 总长度
offset += 2;
pkt.write_u32_be(offset, 0xC0A80001); // 源 IP: 192.168.0.1
offset += 4;

// 浮点值
pkt.write_f32_le(offset, 3.14);
offset += 4;
pkt.write_f64_be(offset, 2.71828);
offset += 8;
```

**单字节写入**（`write_u8`、`write_i8`）没有端序后缀，因为单字节的字节序无关紧要。

### 读取方法

从字节偏移量读取类型化值。端序后缀与写入方法匹配。

```hemlock
let pkt = buffer(64);
// ... 用数据填充缓冲区 ...

// 解析数据包头
let ether_type = pkt.read_u16_be(0);    // 0x0800
let version = pkt.read_u8(2);            // 0x45
let total_len = pkt.read_u16_be(4);      // 40
let src_ip = pkt.read_u32_be(6);         // 0xC0A80001

// 读取浮点值
let pi = pkt.read_f32_le(10);
let e = pkt.read_f64_be(14);
```

### 批量操作

```hemlock
let src = buffer(8);
for (let i = 0; i < 8; i++) { src[i] = i + 1; }

let dest = buffer(32);
dest.write_bytes(4, src);          // 将 src 复制到 dest 的偏移量 4 处

let chunk = dest.read_bytes(4, 8); // 从偏移量 4 读取 8 个字节
print(chunk[0]);                   // 1
```

### 边界检查

所有类型化读写方法都验证整个值是否在缓冲区内。例如，`write_u32_be(offset, val)` 检查 `offset + 4 <= buffer.length`。

```hemlock
let buf = buffer(4);
buf.write_u32_be(0, 42);    // 正确：4 字节放得下
// buf.write_u32_be(2, 42); // 错误：会写入超过末尾（offset 2 + 4 > 4）
```

### 用例

- **网络协议：** 构建/解析 TCP、UDP、DNS 和自定义数据包
- **二进制文件格式：** 读写图像头、归档格式等
- **线协议：** 序列化/反序列化结构化二进制消息
- **FFI 数据交换：** 为 C 库调用准备缓冲区

---

## 使用模式

### 基本分配模式

```hemlock
// 分配
let p = alloc(1024);
if (p == null) {
    panic("allocation failed");
}

// 使用
memset(p, 0, 1024);

// 释放
free(p);
```

### 安全缓冲区模式

```hemlock
// 分配缓冲区
let buf = buffer(256);
if (buf == null) {
    panic("buffer allocation failed");
}

// 带边界检查使用
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// 释放
free(buf);
```

### 动态增长模式

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("allocation failed");
}

// ... 使用内存 ...

// 需要更多空间 - 检查失败
let new_p = realloc(p, 200);
if (new_p == null) {
    // 原始指针仍然有效，清理
    free(p);
    panic("realloc failed");
}
p = new_p;
size = 200;

// ... 使用扩展的内存 ...

free(p);
```

### 内存复制模式

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// 创建副本
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## 安全注意事项

**Hemlock 内存管理设计上是不安全的：**

### 常见陷阱

**1. 内存泄漏**
```hemlock
// 错误：内存泄漏
fn create_buffer() {
    let p = alloc(1024);
    return null;  // 内存泄漏！
}

// 正确：适当清理
fn create_buffer() {
    let p = alloc(1024);
    // ... 使用内存 ...
    free(p);
    return null;
}
```

**2. 释放后使用**
```hemlock
// 错误：释放后使用
let p = alloc(100);
free(p);
memset(p, 0, 100);  // 崩溃：使用已释放的内存

// 正确：释放后不使用
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// 此后不要使用 p2
```

**3. 双重释放**
```hemlock
// 错误：双重释放
let p = alloc(100);
free(p);
free(p);  // 崩溃：双重释放

// 正确：只释放一次
let p2 = alloc(100);
free(p2);
```

**4. 缓冲区溢出（ptr）**
```hemlock
// 错误：ptr 的缓冲区溢出
let p = alloc(10);
memset(p, 65, 100);  // 崩溃：写入超过分配范围

// 正确：使用 buffer 进行边界检查
let buf = buffer(10);
// buf[100] = 65;  // 错误：边界检查失败
```

**5. 悬空指针**
```hemlock
// 错误：悬空指针
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // 崩溃：p2 是悬空的

// 正确：仔细跟踪所有权
let p = alloc(100);
// ... 使用 p ...
free(p);
// 不要保留对 p 的其他引用
```

**6. 未检查的分配失败**
```hemlock
// 错误：不检查 null
let p = alloc(1000000000);  // 在低内存时可能失败
memset(p, 0, 1000000000);   // 崩溃：p 是 null

// 正确：始终检查分配结果
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("out of memory");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## 何时使用什么

### 使用 `buffer()` 当：
- 需要边界检查时
- 处理动态数据时
- 安全性重要时
- 学习 Hemlock 时

### 使用 `alloc()` 当：
- 需要最高性能时
- FFI/与 C 接口时
- 知道确切的内存布局时
- 你是专家时

### 使用 `realloc()` 当：
- 增长/缩小分配时
- 动态数组
- 需要保留数据时

---

## 完整函数总结

| 函数      | 签名                                   | 返回值   | 描述                       |
|-----------|----------------------------------------|----------|----------------------------|
| `alloc`   | `(size: i32)`                          | `ptr`    | 分配原始内存               |
| `buffer`  | `(size: i32)`                          | `buffer` | 分配安全缓冲区             |
| `free`    | `(ptr: ptr \| buffer)`                 | `null`   | 释放内存                   |
| `realloc` | `(ptr: ptr, new_size: i32)`            | `ptr`    | 调整分配大小               |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`     | `null`   | 填充内存                   |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`     | `null`   | 复制内存                   |
| `sizeof`  | `(type)`                               | `i32`    | 获取类型字节大小           |
| `talloc`  | `(type, count: i32)`                   | `ptr`    | 分配类型化数组             |

---

## 另请参阅

- [类型系统](type-system.md) - 指针和缓冲区类型
- [内置函数](builtins.md) - 所有内置函数
- [字符串 API](string-api.md) - 字符串 `.to_bytes()` 方法
