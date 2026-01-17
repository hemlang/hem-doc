# 内存管理

Hemlock 采用**手动内存管理**，对分配和释放有显式控制。本指南涵盖 Hemlock 的内存模型、两种指针类型以及完整的内存 API。

---

## 内存基础 101

**编程新手？** 从这里开始。如果你已经理解内存管理，可以跳到 [设计理念](#设计理念)。

### 什么是内存管理？

当你的程序需要存储数据（文本、数字、列表）时，它需要空间来放置这些数据。这个空间来自计算机的内存（RAM）。内存管理涉及：

1. **获取空间** - 需要时请求内存
2. **使用空间** - 读写数据
3. **归还空间** - 完成后返还内存

### 为什么重要？

想象一个书籍有限的图书馆：
- 如果你不断借书却从不归还，最终就没有书可借了
- 如果你试图阅读已经归还的书，会产生混乱或问题

内存的工作方式相同。如果你忘记归还内存，程序会逐渐使用越来越多的内存（"内存泄漏"）。如果你在归还后尝试使用内存，会发生糟糕的事情。

### 好消息

**大多数时候，你不需要考虑这些！**

Hemlock 自动清理大多数常见类型：

```hemlock
fn example() {
    let name = "Alice";       // Hemlock 管理这个
    let numbers = [1, 2, 3];  // 还有这个
    let person = { age: 30 }; // 还有这个

    // 函数结束时，所有这些都自动清理！
}
```

### 何时需要考虑

只有在使用以下情况时才需要手动内存管理：

1. **`alloc()`** - 原始内存分配（返回 `ptr`）
2. **`buffer()`** - 当你想提前释放时（可选 - 作用域结束时自动释放）

```hemlock
// 这需要手动清理：
let raw = alloc(100);   // 原始内存 - 你必须释放它
// ... 使用 raw ...
free(raw);              // 必需！否则会有内存泄漏

// 这自动清理（但你可以提前释放）：
let buf = buffer(100);  // 安全 buffer
// ... 使用 buf ...
// free(buf);           // 可选 - 作用域结束时自动释放
```

### 简单规则

> **如果你调用 `alloc()`，你必须调用 `free()`。**
>
> 其他一切都会为你处理。

### 应该使用哪个？

| 场景 | 使用这个 | 原因 |
|-----------|----------|-----|
| **刚开始学习** | `buffer()` | 安全、有边界检查、自动清理 |
| **需要字节存储** | `buffer()` | 安全且简单 |
| **与 C 库交互（FFI）** | `alloc()` / `ptr` | C 互操作必需 |
| **最大性能** | `alloc()` / `ptr` | 无边界检查开销 |
| **不确定** | `buffer()` | 总是更安全的选择 |

### 快速示例：安全与原始

```hemlock
// 推荐：安全 buffer
fn safe_example() {
    let data = buffer(10);
    data[0] = 65;           // 正确
    data[5] = 66;           // 正确
    // data[100] = 67;      // 错误 - Hemlock 阻止你（边界检查）
    free(data);             // 清理
}

// 高级：原始指针（仅在需要时使用）
fn raw_example() {
    let data = alloc(10);
    *data = 65;             // 正确
    *(data + 5) = 66;       // 正确
    *(data + 100) = 67;     // 危险 - 无边界检查，破坏内存！
    free(data);             // 清理
}
```

**从 `buffer()` 开始。只有在特别需要原始指针时才使用 `alloc()`。**

---

## 设计理念

Hemlock 遵循显式内存管理与合理默认值的原则：
- 无垃圾回收（无不可预测的暂停）
- 常见类型的内部引用计数（string, array, object, buffer）
- 原始指针（`ptr`）需要手动 `free()`

这种混合方法在需要时给你完全控制（原始指针），同时防止典型用例的常见错误（引用计数类型在作用域退出时自动释放）。

## 内部引用计数

运行时使用**内部引用计数**来管理对象生命周期。对于大多数引用计数类型的局部变量，清理是自动且确定性的。

### 引用计数处理什么

运行时在以下情况自动管理引用计数：

1. **变量重新赋值** - 旧值被释放：
   ```hemlock
   let x = "first";   // ref_count = 1
   x = "second";      // "first" 内部释放，"second" ref_count = 1
   ```

2. **作用域退出** - 局部变量被释放：
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // 函数返回时 arr 被释放
   ```

3. **容器被释放** - 元素被释放：
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // obj1 和 obj2 的 ref_count 递减
   ```

### 何时需要 `free()` vs 何时自动

**自动（不需要 `free()`）：** 引用计数类型的局部变量在作用域退出时释放：

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... 使用它们 ...
}  // 函数返回时全部自动释放 - 不需要 free()
```

**需要手动 `free()`：**

1. **原始指针** - `alloc()` 没有引用计数：
   ```hemlock
   let p = alloc(64);
   // ... 使用 p ...
   free(p);  // 总是需要 - 否则会泄漏
   ```

2. **提前清理** - 在作用域结束前释放以更早释放内存：
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10MB
       // ... 用完 big ...
       free(big);  // 现在释放，不等函数返回
       // ... 更多不需要 big 的工作 ...
   }
   ```

3. **长期存活的数据** - 全局数据或存储在持久结构中的数据：
   ```hemlock
   let cache = {};  // 模块级别，除非释放否则存活到程序退出

   fn cleanup() {
       free(cache);  // 长期存活数据的手动清理
   }
   ```

### 引用计数 vs 垃圾回收

| 方面 | Hemlock 引用计数 | 垃圾回收 |
|--------|---------------------|-------------------|
| 清理时机 | 确定性（ref 为 0 时立即清理） | 非确定性（GC 决定何时） |
| 用户责任 | 必须调用 `free()` | 完全自动 |
| 运行时暂停 | 无 | "停止世界"暂停 |
| 可见性 | 隐藏的实现细节 | 通常不可见 |
| 循环引用 | 通过 visited-set 跟踪处理 | 通过追踪处理 |

### 哪些类型有引用计数

| 类型 | 引用计数 | 备注 |
|------|------------|-------|
| `ptr` | 否 | 总是需要手动 `free()` |
| `buffer` | 是 | 作用域退出时自动释放；手动 `free()` 用于提前清理 |
| `array` | 是 | 作用域退出时自动释放；手动 `free()` 用于提前清理 |
| `object` | 是 | 作用域退出时自动释放；手动 `free()` 用于提前清理 |
| `string` | 是 | 完全自动，不需要 `free()` |
| `function` | 是 | 完全自动（闭包环境） |
| `task` | 是 | 线程安全的原子引用计数 |
| `channel` | 是 | 线程安全的原子引用计数 |
| 基本类型 | 否 | 栈分配，无堆分配 |

### 为什么这样设计？

这种混合方法给你：
- **显式控制** - 你决定何时释放
- **作用域错误安全** - 重新赋值不会泄漏
- **可预测性能** - 无 GC 暂停
- **闭包支持** - 函数可以安全捕获变量

理念保持不变：你在控制，但运行时帮助防止常见错误，如重新赋值时的泄漏或容器中的双重释放。

## 两种指针类型

Hemlock 提供两种不同的指针类型，具有不同的安全特性：

### `ptr` - 原始指针（危险）

原始指针**只是地址**，安全保证最少：

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // 你必须记得释放
```

**特性：**
- 只是一个 8 字节地址
- 无边界检查
- 无长度跟踪
- 用户完全管理生命周期
- 适合专家和 FFI

**使用场景：**
- 底层系统编程
- 外部函数接口（FFI）
- 性能关键代码
- 需要完全控制时

**危险：**
```hemlock
let p = alloc(10);
let q = p + 100;  // 远超分配范围 - 允许但危险
free(p);
let x = *p;       // 悬空指针 - 未定义行为
free(p);          // 双重释放 - 会崩溃
```

### `buffer` - 安全包装（推荐）

Buffer 提供**边界检查访问**，同时仍需要手动释放：

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // 边界检查
print(b.length);        // 64
free(b);                // 仍然是手动的
```

**特性：**
- 指针 + 长度 + 容量
- 访问时边界检查
- 仍需要手动 `free()`
- 大多数代码的更好默认选择

**属性：**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100（当前大小）
print(buf.capacity);    // 100（分配的容量）
```

**边界检查：**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // 正确
buf[100] = 42;    // 错误：索引越界
```

## 内存 API

### 核心分配

**`alloc(bytes)` - 分配原始内存**
```hemlock
let p = alloc(1024);  // 分配 1KB，返回 ptr
// ... 使用内存
free(p);
```

**`buffer(size)` - 分配安全 buffer**
```hemlock
let buf = buffer(256);  // 分配 256 字节 buffer
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - 释放内存**
```hemlock
let p = alloc(100);
free(p);  // 必须释放以避免内存泄漏

let buf = buffer(100);
free(buf);  // 对 ptr 和 buffer 都有效
```

**重要：** `free()` 对 `ptr` 和 `buffer` 类型都有效。

### 内存操作

**`memset(ptr, byte, size)` - 填充内存**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // 将 100 字节清零
memset(p, 65, 10);     // 将前 10 字节填充为 'A'
free(p);
```

**`memcpy(dest, src, size)` - 复制内存**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // 从 src 复制 50 字节到 dst
free(src);
free(dst);
```

**`realloc(ptr, size)` - 调整分配大小**
```hemlock
let p = alloc(100);
// ... 使用 100 字节
p = realloc(p, 200);   // 调整为 200 字节
// ... 使用 200 字节
free(p);
```

**注意：** `realloc()` 后，旧指针可能无效。始终使用返回的指针。

### 类型化分配

Hemlock 提供类型化分配辅助函数以方便使用：

```hemlock
let arr = talloc(i32, 100);  // 分配 100 个 i32 值（400 字节）
let size = sizeof(i32);      // 返回 4（字节）
```

**`sizeof(type)`** 返回类型的字节大小：
- `sizeof(i8)` / `sizeof(u8)` -> 1
- `sizeof(i16)` / `sizeof(u16)` -> 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` -> 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` -> 8
- `sizeof(ptr)` -> 8（64 位系统）

**`talloc(type, count)`** 分配 `count` 个 `type` 类型的元素：

```hemlock
let ints = talloc(i32, 10);   // 40 字节用于 10 个 i32 值
let floats = talloc(f64, 5);  // 40 字节用于 5 个 f64 值
free(ints);
free(floats);
```

## 常见模式

### 模式：分配、使用、释放

内存管理的基本模式：

```hemlock
// 1. 分配
let data = alloc(1024);

// 2. 使用
memset(data, 0, 1024);
// ... 做工作

// 3. 释放
free(data);
```

### 模式：安全 Buffer 使用

优先使用 buffer 进行边界检查访问：

```hemlock
let buf = buffer(256);

// 安全迭代
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### 模式：使用 try/finally 管理资源

即使出错也确保清理：

```hemlock
let data = alloc(1024);
try {
    // ... 风险操作
    process(data);
} finally {
    free(data);  // 即使出错也会释放
}
```

## 内存安全注意事项

### 双重释放

**允许但会崩溃：**
```hemlock
let p = alloc(100);
free(p);
free(p);  // 崩溃：检测到双重释放
```

**预防：**
```hemlock
let p = alloc(100);
free(p);
p = null;  // 释放后设为 null

if (p != null) {
    free(p);  // 不会执行
}
```

### 悬空指针

**允许但未定义行为：**
```hemlock
let p = alloc(100);
*p = 42;      // 正确
free(p);
let x = *p;   // 未定义：读取已释放内存
```

**预防：** 释放后不要访问内存。

### 内存泄漏

**容易创建，难以调试：**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // 忘记释放！
    return;  // 内存泄漏
}
```

**预防：** 始终将 `alloc()` 与 `free()` 配对：
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... 使用 p
    } finally {
        free(p);  // 总是释放
    }
}
```

### 指针算术

**允许但危险：**
```hemlock
let p = alloc(10);
let q = p + 100;  // 远超分配边界
*q = 42;          // 未定义：越界写入
free(p);
```

**使用 buffer 进行边界检查：**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // 错误：边界检查阻止溢出
```

## 最佳实践

1. **默认使用 `buffer`** - 除非特别需要原始 `ptr` 否则使用 `buffer`
2. **匹配 alloc/free** - 每个 `alloc()` 应该有且仅有一个 `free()`
3. **使用 try/finally** - 使用异常处理确保清理
4. **释放后置空** - 释放后将指针设为 `null` 以捕获释放后使用
5. **边界检查** - 使用 buffer 索引进行自动边界检查
6. **记录所有权** - 明确哪些代码拥有并释放每个分配

## 示例

### 示例：动态字符串构建器

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // 调用者必须释放
}

let msg = build_message(5);
// ... 使用 msg
free(msg);
```

### 示例：安全数组操作

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // 填充数组
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // 处理
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // 总是清理
    }
}
```

### 示例：内存池模式

```hemlock
// 简单内存池（简化版）
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool exhausted";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// 使用池
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// 一次性释放整个池
free(pool);
```

## 限制

需要注意的当前限制：

- **原始指针需要手动释放** - `alloc()` 返回没有引用计数的 `ptr`
- **无自定义分配器** - 只有系统 malloc/free

**注意：** 引用计数类型（string, array, object, buffer）在作用域退出时自动释放。只有来自 `alloc()` 的原始 `ptr` 需要显式 `free()`。

## 相关主题

- [字符串](strings.md) - 字符串内存管理和 UTF-8 编码
- [数组](arrays.md) - 动态数组及其内存特性
- [对象](objects.md) - 对象分配和生命周期
- [错误处理](error-handling.md) - 使用 try/finally 进行清理

## 另请参阅

- **设计理念**：参见 CLAUDE.md 中的 "Memory Management" 部分
- **类型系统**：参见 [类型](types.md) 了解 `ptr` 和 `buffer` 类型详情
- **FFI**：原始指针对外部函数接口至关重要
