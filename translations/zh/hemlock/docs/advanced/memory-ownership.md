# Hemlock 中的内存所有权

> "我们给你安全的工具，但不强迫你使用它们。"

本文档描述了 Hemlock 中的内存所有权语义，涵盖程序员管理的内存和运行时管理的值。

## 目录

1. [契约](#契约)
2. [程序员管理的内存](#程序员管理的内存)
3. [运行时管理的值](#运行时管理的值)
4. [所有权转移点](#所有权转移点)
5. [异步和并发](#异步和并发)
6. [FFI 内存规则](#ffi-内存规则)
7. [异常安全性](#异常安全性)
8. [最佳实践](#最佳实践)

---

## 契约

Hemlock 对内存管理责任有明确的划分：

| 内存类型 | 管理者 | 清理方法 |
|----------|--------|----------|
| 原始指针 (`ptr`) | **程序员** | `free(ptr)` |
| 缓冲区 (`buffer`) | **程序员** | `free(buf)` |
| 字符串、数组、对象 | **运行时** | 自动（引用计数） |
| 函数、闭包 | **运行时** | 自动（引用计数） |
| 任务、通道 | **运行时** | 自动（引用计数） |

**核心原则：** 如果你显式分配，就显式释放。其他一切都自动处理。

---

## 程序员管理的内存

### 原始指针

```hemlock
let p = alloc(64);       // 分配 64 字节
memset(p, 0, 64);        // 初始化
// ... 使用内存 ...
free(p);                 // 你的责任！
```

**规则：**
- `alloc()` 返回你拥有的内存
- 使用完毕后必须调用 `free()`
- 双重释放会崩溃（故意设计）
- 释放后使用是未定义行为
- 允许指针算术但不检查

### 类型化分配

```hemlock
let arr = talloc("i32", 100);  // 分配 100 个 i32（400 字节）
ptr_write_i32(arr, 0, 42);     // 写入索引 0
let val = ptr_read_i32(arr, 0); // 从索引 0 读取
free(arr);                      // 仍然是你的责任
```

### 缓冲区（安全替代）

```hemlock
let buf = buffer(64);    // 有边界检查的缓冲区
buf[0] = 42;             // 安全的索引访问
// buf[100] = 1;         // 运行时错误：越界
free(buf);               // 仍需要显式 free
```

**关键区别：** 缓冲区提供边界检查，原始指针不提供。

---

## 运行时管理的值

### 引用计数

堆分配的值使用原子引用计数：

```hemlock
let s1 = "hello";        // 字符串分配，refcount = 1
let s2 = s1;             // s2 共享 s1，refcount = 2
// 当两者都离开作用域时，refcount → 0，内存释放
```

**引用计数类型：**
- `string` - UTF-8 文本
- `array` - 动态数组
- `object` - 键值对象
- `function` - 闭包
- `task` - 异步任务句柄
- `channel` - 通信通道

### 循环检测

运行时处理对象图中的循环：

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // 循环: a → b → a
// 运行时使用已访问集合在清理期间检测和打破循环
```

---

## 所有权转移点

### 变量绑定

```hemlock
let x = [1, 2, 3];       // 创建数组，refcount 为 1
                         // x 拥有引用
```

### 函数返回

```hemlock
fn make_array() {
    return [1, 2, 3];    // 数组所有权转移给调用者
}
let arr = make_array();  // arr 现在拥有引用
```

### 赋值

```hemlock
let a = "hello";
let b = a;               // 共享引用（refcount 增加）
b = "world";             // a 仍然是 "hello"，b 是 "world"
```

### 通道操作

```hemlock
let ch = channel(10);
ch.send("message");      // 值复制到通道缓冲区
                         // 原始值仍然有效

let msg = ch.recv();     // 从通道接收所有权
```

### 任务生成

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data 被深拷贝以实现隔离
data.x = 2;                       // 安全 - 任务有自己的副本
let result = join(task);          // result 所有权转移给调用者
```

---

## 异步和并发

### 线程隔离

生成的任务接收可变参数的**深拷贝**：

```hemlock
async fn worker(data) {
    data.x = 100;        // 只修改任务的副本
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // 安全 - 不影响任务
let result = join(task);
print(obj.x);            // 2（未被任务改变）
print(result.x);         // 100（任务修改的副本）
```

### 共享协调对象

某些类型通过引用共享（不复制）：
- **通道** - 用于任务间通信
- **任务** - 用于协调（join/detach）

```hemlock
let ch = channel(1);
spawn(producer, ch);     // 同一个通道，不是副本
spawn(consumer, ch);     // 两个任务共享通道
```

### 任务结果

```hemlock
let task = spawn(compute);
let result = join(task);  // 调用者拥有结果
                          // 任务引用在任务释放时释放
```

### 分离的任务

```hemlock
detach(spawn(background_work));
// 任务独立运行
// 任务完成时结果自动释放
// 即使没人调用 join() 也不会泄漏
```

---

## FFI 内存规则

### 传递给 C 函数

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock 保留所有权
                         // 字符串在调用期间有效
                         // C 函数不应释放它
```

### 从 C 函数接收

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C 分配了这块内存
free(copy);                   // 你有责任释放
```

### 结构体传递（仅编译器）

```hemlock
// 定义 C 结构体布局
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // 按值返回，已复制
                                // 栈上结构体不需要清理
```

### 回调内存

```hemlock
// 当 C 回调到 Hemlock 时：
// - 参数属于 C（不要释放）
// - 返回值所有权转移给 C
```

---

## 异常安全性

### 保证

运行时提供以下保证：

1. **正常退出无泄漏** - 所有运行时管理的值都被清理
2. **异常时无泄漏** - 临时值在栈展开期间释放
3. **异常时 defer 执行** - 清理代码会执行

### 表达式求值

```hemlock
// 如果在数组创建期间抛出：
let arr = [f(), g(), h()];  // 部分数组被释放

// 如果在函数调用期间抛出：
foo(a(), b(), c());         // 之前求值的参数被释放
```

### 用于清理的 Defer

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // 在 return 或异常时运行

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close() 仍会运行！
    }
    return data;
}
```

---

## 最佳实践

### 1. 优先使用运行时管理的类型

```hemlock
// 优先这样：
let data = [1, 2, 3, 4, 5];

// 而不是这样（除非需要底层控制）：
let data = talloc("i32", 5);
// ... 必须记得释放 ...
```

### 2. 对手动内存使用 Defer

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // 保证清理

    // ... 使用 buf ...
    // 不需要在每个返回点释放
}
```

### 3. 在异步中避免原始指针

```hemlock
// 错误 - 指针可能在任务完成前被释放
let p = alloc(64);
spawn(worker, p);          // 任务获得指针值
free(p);                   // 糟糕！任务还在使用它

// 正确 - 使用通道或复制数据
let ch = channel(1);
let data = buffer(64);
// ... 填充 data ...
ch.send(data);             // 深拷贝
spawn(worker, ch);
free(data);                // 安全 - 任务有自己的副本
```

### 4. 完成后关闭通道

```hemlock
let ch = channel(10);
// ... 使用通道 ...
ch.close();                // 排空并释放缓冲的值
```

### 5. Join 或 Detach 任务

```hemlock
let task = spawn(work);

// 选项 1：等待结果
let result = join(task);

// 选项 2：Fire and forget
// detach(task);

// 不要：让任务句柄离开作用域而不 join 或 detach
// （它会被清理，但结果可能泄漏）
```

---

## 调试内存问题

### 启用 ASAN

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### 运行泄漏回归测试

```bash
make leak-regression       # 完整套件
make leak-regression-quick # 跳过全面测试
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## 总结

| 操作 | 内存行为 |
|------|----------|
| `alloc(n)` | 分配，你释放 |
| `buffer(n)` | 带边界检查分配，你释放 |
| `"string"` | 运行时管理 |
| `[array]` | 运行时管理 |
| `{object}` | 运行时管理 |
| `spawn(fn)` | 深拷贝参数，运行时管理任务 |
| `join(task)` | 调用者拥有结果 |
| `detach(task)` | 完成时运行时释放结果 |
| `ch.send(v)` | 复制值到通道 |
| `ch.recv()` | 调用者拥有接收的值 |
| `ch.close()` | 排空并释放缓冲的值 |
