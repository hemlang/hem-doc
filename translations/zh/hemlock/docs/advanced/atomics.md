# 原子操作

Hemlock 提供原子操作用于**无锁并发编程**。这些操作使得在多个线程间安全操作共享内存成为可能，无需传统的锁或互斥锁。

## 目录

- [概述](#概述)
- [何时使用原子操作](#何时使用原子操作)
- [内存模型](#内存模型)
- [原子加载和存储](#原子加载和存储)
- [获取并修改操作](#获取并修改操作)
- [比较并交换 (CAS)](#比较并交换-cas)
- [原子交换](#原子交换)
- [内存栅栏](#内存栅栏)
- [函数参考](#函数参考)
- [常见模式](#常见模式)
- [最佳实践](#最佳实践)
- [限制](#限制)

---

## 概述

原子操作是**不可分割的**操作，完成时不可能被中断。当一个线程执行原子操作时，其他线程无法观察到操作的部分完成状态。

**主要特性：**
- 所有操作使用**顺序一致性**（`memory_order_seq_cst`）
- 支持的类型：**i32** 和 **i64**
- 操作适用于通过 `alloc()` 分配的原始指针
- 无需显式锁即可保证线程安全

**可用操作：**
- Load/Store - 原子读取和写入值
- Add/Sub - 返回旧值的算术操作
- And/Or/Xor - 返回旧值的位运算操作
- CAS - 条件更新的比较并交换
- Exchange - 原子交换值
- Fence - 完整内存屏障

---

## 何时使用原子操作

**使用原子操作的场景：**
- 跨任务共享的计数器（如请求计数、进度跟踪）
- 标志和状态指示器
- 无锁数据结构
- 简单的同步原语
- 性能关键的并发代码

**改用通道的场景：**
- 在任务间传递复杂数据
- 实现生产者-消费者模式
- 需要消息传递语义时

**示例用例 - 共享计数器：**
```hemlock
// 分配共享计数器
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// 生成多个工作者
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// 计数器将恰好是 3000（无数据竞争）
print(atomic_load_i32(counter));

free(counter);
```

---

## 内存模型

所有 Hemlock 原子操作使用**顺序一致性**（`memory_order_seq_cst`），提供最强的内存排序保证：

1. **原子性**：每个操作都是不可分割的
2. **全局排序**：所有线程看到相同的操作顺序
3. **无重排序**：操作不会被编译器或 CPU 重排序

这使得并发代码的推理更简单，但与较弱的内存排序相比可能有一些性能成本。

---

## 原子加载和存储

### atomic_load_i32 / atomic_load_i64

原子地从内存读取值。

**签名：**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**参数：**
- `ptr` - 指向内存位置的指针（必须正确对齐）

**返回：** 内存位置的值

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

原子地向内存写入值。

**签名：**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**参数：**
- `ptr` - 指向内存位置的指针
- `value` - 要存储的值

**返回：** `null`

**示例：**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## 获取并修改操作

这些操作原子地修改值并返回**旧的**（之前的）值。

### atomic_add_i32 / atomic_add_i64

原子地加法。

**签名：**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**返回：** **旧的**值（加法之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100（旧值）
print(atomic_load_i32(p));     // 110（新值）

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

原子地减法。

**签名：**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**返回：** **旧的**值（减法之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100（旧值）
print(atomic_load_i32(p));     // 75（新值）

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

原子地执行按位与。

**签名：**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**返回：** **旧的**值（与运算之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 二进制 255：11111111

let old = atomic_and_i32(p, 0x0F);  // 与 00001111 进行与运算
print(old);                    // 255（旧值）
print(atomic_load_i32(p));     // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

原子地执行按位或。

**签名：**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**返回：** **旧的**值（或运算之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 二进制 15：00001111

let old = atomic_or_i32(p, 0xF0);  // 与 11110000 进行或运算
print(old);                    // 15（旧值）
print(atomic_load_i32(p));     // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

原子地执行按位异或。

**签名：**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**返回：** **旧的**值（异或运算之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 二进制 170：10101010

let old = atomic_xor_i32(p, 0xFF);  // 与 11111111 进行异或运算
print(old);                    // 170（旧值）
print(atomic_load_i32(p));     // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## 比较并交换 (CAS)

最强大的原子操作。原子地将当前值与期望值比较，如果匹配则替换为新值。

### atomic_cas_i32 / atomic_cas_i64

**签名：**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**参数：**
- `ptr` - 指向内存位置的指针
- `expected` - 我们期望找到的值
- `desired` - 如果期望匹配则存储的值

**返回：**
- `true` - 交换成功（值是 `expected`，现在是 `desired`）
- `false` - 交换失败（值不是 `expected`，未改变）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS 成功：值是 100，交换为 999
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS 失败：值是 999，不是 100
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999（未改变）

free(p);
```

**用例：**
- 实现锁和信号量
- 无锁数据结构
- 乐观并发控制
- 原子条件更新

---

## 原子交换

原子地交换值，返回旧值。

### atomic_exchange_i32 / atomic_exchange_i64

**签名：**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**参数：**
- `ptr` - 指向内存位置的指针
- `value` - 要存储的新值

**返回：** **旧的**值（交换之前）

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100（旧值）
print(atomic_load_i32(p));     // 200（新值）

free(p);
```

---

## 内存栅栏

完整的内存屏障，确保栅栏之前的所有内存操作对所有线程可见，然后才执行栅栏之后的任何操作。

### atomic_fence

**签名：**
```hemlock
atomic_fence(): null
```

**返回：** `null`

**示例：**
```hemlock
// 确保之前的所有写入对其他线程可见
atomic_fence();
```

**注意：** 在大多数情况下，你不需要显式的栅栏，因为所有原子操作已经使用顺序一致性。栅栏在需要同步非原子内存操作时很有用。

---

## 函数参考

### i32 操作

| 函数 | 签名 | 返回 | 描述 |
|------|------|------|------|
| `atomic_load_i32` | `(ptr)` | `i32` | 原子加载值 |
| `atomic_store_i32` | `(ptr, value)` | `null` | 原子存储值 |
| `atomic_add_i32` | `(ptr, value)` | `i32` | 加法并返回旧值 |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | 减法并返回旧值 |
| `atomic_and_i32` | `(ptr, value)` | `i32` | 按位与并返回旧值 |
| `atomic_or_i32` | `(ptr, value)` | `i32` | 按位或并返回旧值 |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | 按位异或并返回旧值 |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | 比较并交换 |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | 交换并返回旧值 |

### i64 操作

| 函数 | 签名 | 返回 | 描述 |
|------|------|------|------|
| `atomic_load_i64` | `(ptr)` | `i64` | 原子加载值 |
| `atomic_store_i64` | `(ptr, value)` | `null` | 原子存储值 |
| `atomic_add_i64` | `(ptr, value)` | `i64` | 加法并返回旧值 |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | 减法并返回旧值 |
| `atomic_and_i64` | `(ptr, value)` | `i64` | 按位与并返回旧值 |
| `atomic_or_i64` | `(ptr, value)` | `i64` | 按位或并返回旧值 |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | 按位异或并返回旧值 |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | 比较并交换 |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | 交换并返回旧值 |

### 内存屏障

| 函数 | 签名 | 返回 | 描述 |
|------|------|------|------|
| `atomic_fence` | `()` | `null` | 完整内存屏障 |

---

## 常见模式

### 模式：原子计数器

```hemlock
// 线程安全的计数器
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// 使用
increment();  // 返回 0（旧值）
increment();  // 返回 1
increment();  // 返回 2
print(get_count());  // 3

free(counter);
```

### 模式：自旋锁

```hemlock
// 简单的自旋锁实现
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = 未锁定，1 = 已锁定

fn acquire() {
    // 自旋直到成功将锁从 0 设置为 1
    while (!atomic_cas_i32(lock, 0, 1)) {
        // 忙等待
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// 使用
acquire();
// ... 临界区 ...
release();

free(lock);
```

### 模式：一次性初始化

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = 未初始化，1 = 已初始化

fn ensure_initialized() {
    // 尝试成为初始化者
    if (atomic_cas_i32(initialized, 0, 1)) {
        // 我们赢得了竞争，执行初始化
        do_expensive_init();
    }
    // 否则，已经初始化过了
}
```

### 模式：原子标志

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // 如果标志已经设置则返回 true
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### 模式：有界计数器

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // 已达最大值
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // 成功递增
        }
        // CAS 失败，另一个线程修改了值 - 重试
    }
}
```

---

## 最佳实践

### 1. 使用正确的对齐

指针必须为数据类型正确对齐：
- i32：4 字节对齐
- i64：8 字节对齐

来自 `alloc()` 的内存通常是正确对齐的。

### 2. 优先使用更高级的抽象

如果可能，使用通道进行任务间通信。原子操作是更底层的，需要仔细推理。

```hemlock
// 优先这样：
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// 而不是在适当时使用手动原子协调
```

### 3. 注意 ABA 问题

CAS 可能遭受 ABA 问题：值从 A 变为 B 然后又变回 A。你的 CAS 成功了，但状态可能在中间已经改变。

### 4. 在共享之前初始化

始终在生成访问原子变量的任务之前初始化它们：

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // 在生成之前初始化

let task = spawn(worker, counter);
```

### 5. 在所有任务完成后释放

不要在任务可能仍在访问原子内存时释放它：

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// 现在可以安全释放
free(counter);
```

---

## 限制

### 当前限制

1. **仅支持 i32 和 i64** - 其他类型没有原子操作
2. **没有指针原子操作** - 无法原子地加载/存储指针
3. **仅顺序一致性** - 没有较弱的内存排序可用
4. **没有原子浮点数** - 如果需要请使用整数表示

### 平台说明

- 原子操作底层使用 C11 `<stdatomic.h>`
- 在所有支持 POSIX 线程的平台上可用
- 在现代 64 位系统上保证无锁

---

## 另请参阅

- [异步/并发](async-concurrency.md) - 任务生成和通道
- [内存管理](../language-guide/memory.md) - 指针和缓冲区分配
- [内存 API](../reference/memory-api.md) - 分配函数
