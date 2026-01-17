# Hemlock 异步/并发编程

Hemlock 提供**结构化并发**，支持 async/await 语法、任务生成和通道通信。实现基于 POSIX 线程（pthreads），实现**真正的多线程并行**。

## 目录

- [概述](#概述)
- [线程模型](#线程模型)
- [异步函数](#异步函数)
- [任务生成](#任务生成)
- [通道](#通道)
- [异常传播](#异常传播)
- [实现细节](#实现细节)
- [最佳实践](#最佳实践)
- [性能特性](#性能特性)
- [当前限制](#当前限制)

## 概述

**这意味着：**
- 真正的操作系统线程 - 每个生成的任务运行在独立的 pthread（POSIX 线程）上
- 真正的并行 - 任务在多个 CPU 核心上同时执行
- 内核调度 - 操作系统调度器将任务分配到可用的核心上
- 线程安全的通道 - 使用 pthread 互斥锁和条件变量进行同步

**这不是：**
- 不是绿色线程 - 不是用户空间的协作式多任务
- 不是 async/await 协程 - 不是像 JavaScript/Python asyncio 那样的单线程事件循环
- 不是模拟并发 - 不是模拟的并行

这与 **C、C++ 和 Rust** 使用操作系统线程时的**线程模型相同**。你可以获得跨多个核心的真正并行执行。

## 线程模型

### 1:1 线程模型

Hemlock 使用 **1:1 线程模型**，其中：
- 每个生成的任务通过 `pthread_create()` 创建专用的操作系统线程
- 操作系统内核在可用的 CPU 核心间调度线程
- 抢占式多任务 - 操作系统可以中断并在线程之间切换
- **无 GIL** - 不像 Python，没有全局解释器锁限制并行性

### 同步机制

- **互斥锁** - 通道使用 `pthread_mutex_t` 实现线程安全访问
- **条件变量** - 阻塞的发送/接收使用 `pthread_cond_t` 实现高效等待
- **无锁操作** - 任务状态转换是原子的

## 异步函数

函数可以声明为 `async`，表示它们设计用于并发执行：

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
```

### 要点

- `async fn` 声明异步函数
- 异步函数可以使用 `spawn()` 作为并发任务生成
- 异步函数也可以直接调用（在当前线程同步运行）
- 生成时，每个任务运行在**自己的操作系统线程**上（不是协程！）
- `await` 关键字保留供将来使用

### 示例：直接调用 vs 生成

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 直接调用 - 同步运行
let result1 = factorial(5);  // 120

// 生成任务 - 在独立线程上运行
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## 任务生成

使用 `spawn()` 在**独立的操作系统线程上并行**运行异步函数：

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 生成多个任务 - 这些在不同的 CPU 核心上并行运行！
let t1 = spawn(factorial, 5);  // 线程 1
let t2 = spawn(factorial, 6);  // 线程 2
let t3 = spawn(factorial, 7);  // 线程 3

// 三个任务现在正在同时计算！

// 等待结果
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### 内置函数

#### spawn(async_fn, arg1, arg2, ...)

在新的 pthread 上创建新任务，返回任务句柄。

**参数：**
- `async_fn` - 要执行的异步函数
- `arg1, arg2, ...` - 传递给函数的参数

**返回：** 任务句柄（与 `join()` 或 `detach()` 一起使用的不透明值）

**示例：**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... 处理逻辑
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

等待任务完成（阻塞直到线程结束），返回结果。

**参数：**
- `task` - 从 `spawn()` 返回的任务句柄

**返回：** 异步函数返回的值

**示例：**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // 阻塞直到 compute() 完成
print(result);
```

**重要：** 每个任务只能 join 一次。后续的 join 将会报错。

#### detach(task)

即发即忘执行（线程独立运行，不允许 join）。

**参数：**
- `task` - 从 `spawn()` 返回的任务句柄

**返回：** `null`

**示例：**
```hemlock
async fn background_work() {
    // 长时间运行的后台任务
    // ...
}

let task = spawn(background_work);
detach(task);  // 任务独立运行，无法 join
```

**重要：** 分离的任务无法 join。当任务完成时，pthread 和 Task 结构都会自动清理。

## 通道

通道使用有界缓冲区和阻塞语义，提供任务间的线程安全通信。

### 创建通道

```hemlock
let ch = channel(10);  // 创建缓冲区大小为 10 的通道
```

**参数：**
- `capacity` (i32) - 通道可容纳的最大值数量

**返回：** 通道对象

### 通道方法

#### send(value)

向通道发送值（如果已满则阻塞）。

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
let task = spawn(producer, ch, 5);
```

**行为：**
- 如果通道有空间，值会立即添加
- 如果通道已满，发送者阻塞直到有空间可用
- 如果通道已关闭，抛出异常

#### recv()

从通道接收值（如果为空则阻塞）。

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
let task = spawn(consumer, ch, 5);
```

**行为：**
- 如果通道有值，立即返回下一个值
- 如果通道为空，接收者阻塞直到有值可用
- 如果通道已关闭且为空，返回 `null`

#### close()

关闭通道（在已关闭的通道上 recv 返回 null）。

```hemlock
ch.close();
```

**行为：**
- 阻止进一步的 `send()` 操作（将抛出异常）
- 允许挂起的 `recv()` 操作完成
- 一旦为空，`recv()` 返回 `null`

### 使用 select() 多路复用

`select()` 函数允许同时等待多个通道，当任何通道有数据可用时返回。

**签名：**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**参数：**
- `channels` - 通道值数组
- `timeout_ms`（可选）- 超时毫秒数（-1 或省略表示无限等待）

**返回：**
- `{ channel, value }` - 包含有数据的通道和接收到的值的对象
- `null` - 超时时（如果指定了超时）

**示例：**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// 生产者任务
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// 等待第一个结果（ch2 应该更快）
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"

// 等待第二个结果
let result2 = select([ch1, ch2]);
print(result2.value);  // "from channel 1"
```

**带超时：**
```hemlock
let ch = channel(1);

// 没有发送者，将超时
let result = select([ch], 100);  // 100ms 超时
if (result == null) {
    print("Timed out!");
}
```

**使用场景：**
- 等待多个数据源中最快的一个
- 在通道操作上实现超时
- 具有多个事件源的事件循环模式
- 扇入：将多个通道合并为一个

**扇入模式：**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // 所有通道已关闭
        }
        output.send(result.value);
    }
    output.close();
}
```

### 完整的生产者-消费者示例

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

// 创建带缓冲区大小的通道
let ch = channel(10);

// 生成生产者和消费者
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// 等待完成
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### 多生产者，多消费者

通道可以在多个生产者和消费者之间安全共享：

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// 多个生产者
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// 多个消费者
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// 等待所有
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## 异常传播

在生成的任务中抛出的异常会在 join 时传播：

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
    print("Caught: " + e);  // "Caught: Task failed!"
}
```

### 异常处理模式

**模式 1：在任务中处理**
```hemlock
async fn safe_task() {
    try {
        // 有风险的操作
    } catch (e) {
        print("Error in task: " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // 没有异常传播
```

**模式 2：传播给调用者**
```hemlock
async fn task_that_throws() {
    throw "error";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("Caught from task: " + e);
}
```

**模式 3：带异常的分离任务**
```hemlock
async fn detached_task() {
    try {
        // 工作
    } catch (e) {
        // 必须在内部处理 - 无法传播
        print("Error: " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // 无法从分离的任务捕获异常
```

## 实现细节

### 线程架构

- **1:1 线程** - 每个生成的任务通过 `pthread_create()` 创建专用的操作系统线程
- **内核调度** - 操作系统内核在可用的 CPU 核心间调度线程
- **抢占式多任务** - 操作系统可以中断并在线程之间切换
- **无 GIL** - 不像 Python，没有全局解释器锁限制并行性

### 通道实现

通道使用带 pthread 同步的循环缓冲区：

```
通道结构：
- buffer[] - 固定大小的 Values 数组
- capacity - 最大元素数
- size - 当前元素数
- head - 读取位置
- tail - 写入位置
- mutex - pthread_mutex_t 用于线程安全访问
- not_empty - pthread_cond_t 用于阻塞 recv
- not_full - pthread_cond_t 用于阻塞 send
- closed - 布尔标志
- refcount - 用于清理的引用计数
```

**阻塞行为：**
- 在满通道上 `send()`：等待 `not_full` 条件变量
- 在空通道上 `recv()`：等待 `not_empty` 条件变量
- 两者都由相反的操作在适当时发出信号

### 内存和清理

- **已 join 的任务：** 在 `join()` 返回后自动清理
- **分离的任务：** 在任务完成时自动清理
- **通道：** 引用计数，不再使用时释放

## 最佳实践

### 1. 始终关闭通道

```hemlock
async fn producer(ch) {
    // ... 发送值
    ch.close();  // 重要：表示没有更多的值
}
```

### 2. 使用结构化并发

在同一作用域中生成任务并 join 它们：

```hemlock
fn process_data(data) {
    // 生成任务
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // 返回前始终 join
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. 适当处理异常

```hemlock
async fn task() {
    try {
        // 有风险的操作
    } catch (e) {
        // 记录错误
        throw e;  // 如果调用者需要知道则重新抛出
    }
}
```

### 4. 使用适当的通道容量

- **小容量（1-10）：** 用于协调/信号
- **中等容量（10-100）：** 用于一般生产者-消费者
- **大容量（100+）：** 用于高吞吐量场景

```hemlock
let signal_ch = channel(1);      // 协调
let work_ch = channel(50);       // 工作队列
let buffer_ch = channel(1000);   // 高吞吐量
```

### 5. 仅在必要时分离

优先使用 `join()` 而不是 `detach()` 以更好地管理资源：

```hemlock
// 好：Join 并获取结果
let task = spawn(work);
let result = join(task);

// 仅对真正的即发即忘使用 detach
let bg_task = spawn(background_logging);
detach(bg_task);  // 将独立运行
```

## 性能特性

### 真正的并行

- **N 个生成的任务可以同时利用 N 个 CPU 核心**
- 经验证的加速 - 压力测试显示 CPU 时间 vs 墙钟时间为 8-9 倍（多核工作）
- 随核心数线性扩展（直到线程数）

### 线程开销

- 每个任务有约 8KB 栈 + pthread 开销
- 线程创建成本：约 10-20 微秒
- 上下文切换成本：约 1-5 微秒

### 何时使用异步

**好的使用场景：**
- 可并行化的 CPU 密集型计算
- I/O 密集型操作（尽管 I/O 仍然是阻塞的）
- 独立数据的并发处理
- 使用通道的流水线架构

**不理想的场景：**
- 非常短的任务（线程开销占主导）
- 有大量同步的任务（竞争开销）
- 单核系统（没有并行性收益）

### 阻塞 I/O 安全

一个任务中的阻塞操作不会阻塞其他任务：

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // 只阻塞此线程
    let content = f.read();       // 只阻塞此线程
    f.close();
    return content;
}

// 两者并发读取（在不同线程上）
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## 线程安全模型

Hemlock 使用**消息传递**并发模型，任务通过通道而不是共享可变状态进行通信。

### 参数隔离

当你生成任务时，**参数会深拷贝**以防止数据竞争：

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // 修改的是副本，不是原始数组
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - 未改变！
print(modified.length);  // 4 - 有新元素
```

**会深拷贝的：**
- 数组（及所有元素递归）
- 对象（及所有字段递归）
- 字符串
- 缓冲区

**会共享的（保留引用）：**
- 通道（通信机制 - 故意共享）
- 任务句柄（用于协调）
- 函数（代码是不可变的）
- 文件句柄（操作系统管理并发访问）
- 套接字句柄（操作系统管理并发访问）

**不能传递的：**
- 原始指针（`ptr`）- 改用 `buffer`

### 为什么使用消息传递？

这遵循 Hemlock 的"显式优于隐式"哲学：

```hemlock
// 不好：共享可变状态（会导致数据竞争）
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // 竞争！
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // 竞争！

// 好：通过通道的消息传递
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - 没有竞争条件
```

### 引用计数线程安全

所有引用计数操作使用**原子操作**以防止释放后使用错误：
- `string_retain/release` - 原子
- `array_retain/release` - 原子
- `object_retain/release` - 原子
- `buffer_retain/release` - 原子
- `function_retain/release` - 原子
- `channel_retain/release` - 原子
- `task_retain/release` - 原子

这确保即使值跨线程共享也能安全地进行内存管理。

### 闭包环境访问

任务可以访问闭包环境：
- 内置函数（`print`、`len` 等）
- 全局函数定义
- 常量和变量

闭包环境由每个环境的互斥锁保护，使并发读写线程安全：

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK：读取闭包变量（线程安全）
}

async fn modify_closure() {
    x = 20;  // OK：写入闭包变量（与互斥锁同步）
}
```

**注意：** 虽然并发访问是同步的，但从多个任务修改共享状态仍可能导致逻辑竞争条件（非确定性顺序）。为了可预测的行为，使用通道进行任务通信或使用任务返回值。

如果需要从任务返回数据，使用返回值或通道。

## 当前限制

### 1. 没有工作窃取调度器

每个任务使用 1 个线程，对于许多短任务可能效率不高。

**当前：** 1000 个任务 = 1000 个线程（开销大）

**计划中：** 带工作窃取的线程池以提高效率

### 3. 没有异步 I/O 集成

文件/网络操作仍然阻塞线程：

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // 阻塞线程
    f.close();
    return content;
}
```

**变通方法：** 使用多线程进行并发 I/O 操作

### 4. 固定通道容量

通道容量在创建时设置，无法调整大小：

```hemlock
let ch = channel(10);
// 无法动态调整到 20
```

### 5. 通道大小固定

通道缓冲区大小在创建后无法更改。

## 常见模式

### 并行 Map

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // 生成工作者
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // 发送数据
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // 收集结果
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // 等待工作者
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### 流水线架构

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// 创建流水线
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// 输入数据
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// 收集输出
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### 扇出，扇入

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // 处理值
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// 扇出：多个工作者
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// 发送工作
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// 扇入：收集所有结果
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// 等待所有工作者
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## 总结

Hemlock 的异步/并发模型提供：

- 使用操作系统线程的真正多线程并行
- 简单的结构化并发原语
- 线程安全的通道通信
- 跨任务的异常传播
- 在多核系统上经验证的性能
- **参数隔离** - 深拷贝防止数据竞争
- **原子引用计数** - 跨线程安全的内存管理

这使 Hemlock 适用于：
- 并行计算
- 并发 I/O 操作
- 流水线架构
- 生产者-消费者模式

同时避免以下复杂性：
- 手动线程管理
- 低级同步原语
- 容易死锁的基于锁的设计
- 共享可变状态错误
