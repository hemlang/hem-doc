# 并发 API 参考

Hemlock 异步/并发系统的完整参考文档。

---

## 概述

Hemlock 使用 POSIX 线程（pthreads）提供**结构化并发**和真正的多线程并行。每个派生的任务都在单独的操作系统线程上运行，支持跨多个 CPU 核心的实际并行执行。

**主要特性：**
- 真正的多线程并行（不是绿色线程）
- 异步函数语法
- 任务派生和加入
- 线程安全通道
- 异常传播

**线程模型：**
- 真正的操作系统线程（POSIX pthreads）
- 真正的并行性（多个 CPU 核心）
- 内核调度（抢占式多任务）
- 线程安全同步（互斥锁、条件变量）

---

## 异步函数

### 异步函数声明

函数可以声明为 `async`，表示它们是为并发执行设计的。

**语法：**
```hemlock
async fn function_name(params): return_type {
    // 函数体
}
```

**示例：**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Processing:", data);
    return null;
}
```

**行为：**
- `async fn` 声明一个异步函数
- 可以同步调用（在当前线程运行）
- 可以作为并发任务派生（在新线程运行）
- 派生时，在自己的操作系统线程上运行

**注意：** `await` 关键字保留供将来使用，但目前未实现。

---

## 任务管理

### spawn

创建并启动一个新的并发任务。

**签名：**
```hemlock
spawn(async_fn: function, ...args): task
```

**参数：**
- `async_fn` - 要执行的异步函数
- `...args` - 传递给函数的参数

**返回值：** 任务句柄

**示例：**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 派生单个任务
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// 派生多个任务（并行运行！）
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// 三个任务同时运行
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**行为：**
- 通过 `pthread_create()` 创建新的操作系统线程
- 立即开始执行函数
- 返回任务句柄供后续加入
- 任务在单独的 CPU 核心上并行运行

---

### join

等待任务完成并获取结果。

**签名：**
```hemlock
join(task: task): any
```

**参数：**
- `task` - 来自 `spawn()` 的任务句柄

**返回值：** 任务的返回值

**示例：**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // 阻塞直到任务完成
print(result);         // 3628800
```

**行为：**
- 阻塞当前线程直到任务完成
- 返回任务的返回值
- 传播任务抛出的异常
- 返回后清理任务资源

**错误处理：**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Caught:", e);  // "Caught: Task failed!"
}
```

---

### detach

分离任务（即发即弃执行）。

**签名：**
```hemlock
detach(task: task): null
```

**参数：**
- `task` - 来自 `spawn()` 的任务句柄

**返回值：** `null`

**示例：**
```hemlock
async fn background_work() {
    print("Working in background...");
    return null;
}

let t = spawn(background_work);
detach(t);  // 任务继续独立运行

// 不能加入已分离的任务
// join(t);  // 错误
```

**行为：**
- 任务继续独立运行
- 不能 `join()` 已分离的任务
- 任务完成时自动清理任务和线程

**用例：**
- 即发即弃的后台任务
- 日志/监控任务
- 不需要返回值的任务

---

## 通道

通道提供任务之间的线程安全通信。

### channel

创建一个缓冲通道。

**签名：**
```hemlock
channel(capacity: i32): channel
```

**参数：**
- `capacity` - 缓冲区大小（值的数量）

**返回值：** 通道对象

**示例：**
```hemlock
let ch = channel(10);  // 容量为 10 的缓冲通道
let ch2 = channel(1);  // 最小缓冲区（同步）
let ch3 = channel(100); // 大缓冲区
```

**行为：**
- 创建线程安全通道
- 使用 pthread 互斥锁进行同步
- 容量在创建时固定

---

### 通道方法

#### send

向通道发送值（如果已满则阻塞）。

**签名：**
```hemlock
channel.send(value: any): null
```

**参数：**
- `value` - 要发送的值（任意类型）

**返回值：** `null`

**示例：**
```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let t = spawn(producer, ch, 5);
```

**行为：**
- 向通道发送值
- 如果通道已满则阻塞
- 线程安全（使用互斥锁）
- 值发送后返回

---

#### recv

从通道接收值（如果为空则阻塞）。

**签名：**
```hemlock
channel.recv(): any
```

**返回值：** 来自通道的值，如果通道已关闭且为空则返回 `null`

**示例：**
```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let t = spawn(consumer, ch, 5);
```

**行为：**
- 从通道接收值
- 如果通道为空则阻塞
- 如果通道已关闭且为空则返回 `null`
- 线程安全（使用互斥锁）

---

#### close

关闭通道（不再允许发送）。

**签名：**
```hemlock
channel.close(): null
```

**返回值：** `null`

**示例：**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // 表示没有更多值
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // 通道已关闭
        }
        print(val);
    }
    return null;
}
```

**行为：**
- 关闭通道
- 不再允许发送
- 通道为空时 `recv()` 返回 `null`
- 线程安全

---

## 完整并发示例

### 生产者-消费者模式

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Producing:", i);
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        print("Consuming:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// 创建通道
let ch = channel(10);

// 派生生产者和消费者
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// 等待完成
join(p);
let total = join(c);
print("Total:", total);  // 0+10+20+30+40 = 100
```

---

## 并行计算

### 多任务示例

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 派生多个任务（并行运行！）
let t1 = spawn(factorial, 5);   // 线程 1
let t2 = spawn(factorial, 6);   // 线程 2
let t3 = spawn(factorial, 7);   // 线程 3
let t4 = spawn(factorial, 8);   // 线程 4

// 四个任务同时计算！

// 等待结果
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## 任务生命周期

### 状态转换

1. **已创建** - 任务已派生但尚未运行
2. **运行中** - 任务在操作系统线程上执行
3. **已完成** - 任务已完成（结果可用）
4. **已加入** - 结果已获取，资源已清理
5. **已分离** - 任务继续独立运行

### 生命周期示例

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. 创建任务
let t = spawn(work, 21);  // 状态：运行中

// 任务在单独线程上执行...

// 2. 加入任务
let result = join(t);     // 状态：已完成 → 已加入
print(result);            // 42

// 加入后任务资源被清理
```

### 分离生命周期

```hemlock
async fn background() {
    print("Background task running");
    return null;
}

// 1. 创建任务
let t = spawn(background);  // 状态：运行中

// 2. 分离任务
detach(t);                  // 状态：已分离

// 任务继续独立运行
// 完成后由操作系统清理资源
```

---

## 错误处理

### 异常传播

任务中抛出的异常在加入时被传播：

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

// 成功的任务
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// 失败的任务
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Caught:", e);  // "Caught: Task failed!"
}
```

### 处理多个任务

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task " + typeof(id) + " failed";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // 将失败
let t3 = spawn(work, 3, 0);

// 带错误处理的加入
try {
    let r1 = join(t1);  // 正常
    print("Task 1:", r1);

    let r2 = join(t2);  // 抛出异常
    print("Task 2:", r2);  // 永远不会到达
} catch (e) {
    print("Error:", e);  // "Error: Task 2 failed"
}

// 仍然可以加入剩余任务
let r3 = join(t3);
print("Task 3:", r3);
```

---

## 性能特性

### 真正的并行性

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 顺序执行
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// 并行执行
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// 在多核系统上 parallel_time 应该约为 sequential_time 的 50%
```

**已证实的特性：**
- N 个任务可以同时利用 N 个 CPU 核心
- 压力测试显示 CPU 时间与墙钟时间之比为 8-9 倍（并行性的证明）
- 线程开销：每个任务约 8KB 栈 + pthread 开销
- 一个任务中的阻塞操作不会阻塞其他任务

---

## 实现细节

### 线程模型

- **1:1 线程** - 每个任务 = 1 个操作系统线程（`pthread`）
- **内核调度** - 操作系统内核在核心之间分配线程
- **抢占式多任务** - 操作系统可以中断和切换线程
- **无 GIL** - 没有全局解释器锁（与 Python 不同）

### 同步

- **互斥锁** - 通道使用 `pthread_mutex_t`
- **条件变量** - 阻塞的 send/recv 使用 `pthread_cond_t`
- **无锁操作** - 任务状态转换是原子的

### 内存和清理

- **已加入的任务** - `join()` 后自动清理
- **已分离的任务** - 任务完成时自动清理
- **通道** - 引用计数，不再使用时释放

---

## 限制

- 没有用于多路复用多个通道的 `select()`
- 没有工作窃取调度器（每个任务 1 个线程）
- 没有异步 I/O 集成（文件/网络操作会阻塞）
- 通道容量在创建时固定

---

## 完整 API 总结

### 函数

| 函数      | 签名                              | 返回值    | 描述                           |
|-----------|-----------------------------------|-----------|--------------------------------|
| `spawn`   | `(async_fn: function, ...args)`   | `task`    | 创建并启动并发任务             |
| `join`    | `(task: task)`                    | `any`     | 等待任务，获取结果             |
| `detach`  | `(task: task)`                    | `null`    | 分离任务（即发即弃）           |
| `channel` | `(capacity: i32)`                 | `channel` | 创建线程安全通道               |

### 通道方法

| 方法    | 签名            | 返回值  | 描述                           |
|---------|-----------------|---------|--------------------------------|
| `send`  | `(value: any)`  | `null`  | 发送值（如果已满则阻塞）       |
| `recv`  | `()`            | `any`   | 接收值（如果为空则阻塞）       |
| `close` | `()`            | `null`  | 关闭通道                       |

### 类型

| 类型      | 描述                                 |
|-----------|--------------------------------------|
| `task`    | 并发任务的句柄                       |
| `channel` | 线程安全通信通道                     |

---

## 最佳实践

### 应该做的

- 使用通道进行任务之间的通信
- 处理已加入任务的异常
- 发送完成后关闭通道
- 使用 `join()` 获取结果并清理
- 只派生异步函数

### 不应该做的

- 不要在没有同步的情况下共享可变状态
- 不要对同一任务加入两次
- 不要向已关闭的通道发送
- 不要派生非异步函数
- 不要忘记加入任务（除非已分离）

---

## 另请参阅

- [内置函数](builtins.md) - `spawn()`、`join()`、`detach()`、`channel()`
- [类型系统](type-system.md) - 任务和通道类型
