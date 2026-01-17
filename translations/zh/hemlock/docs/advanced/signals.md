# Hemlock 信号处理

Hemlock 提供 **POSIX 信号处理**，用于管理系统信号如 SIGINT（Ctrl+C）、SIGTERM 和自定义信号。这使得底层进程控制和进程间通信成为可能。

## 目录

- [概述](#概述)
- [信号 API](#信号-api)
- [信号常量](#信号常量)
- [基本信号处理](#基本信号处理)
- [高级模式](#高级模式)
- [信号处理器行为](#信号处理器行为)
- [安全考虑](#安全考虑)
- [常见用例](#常见用例)
- [完整示例](#完整示例)

## 概述

信号处理允许程序：
- 响应用户中断（Ctrl+C、Ctrl+Z）
- 实现优雅关闭
- 处理终止请求
- 使用自定义信号进行进程间通信
- 创建警报/定时器机制

**重要：** 按照 Hemlock 的哲学，信号处理**本质上是不安全的**。处理器可以在任何时候被调用，中断正常执行。用户负责适当的同步。

## 信号 API

### signal(signum, handler_fn)

注册信号处理函数。

**参数：**
- `signum` (i32) - 信号编号（如 SIGINT、SIGTERM 常量）
- `handler_fn` (function 或 null) - 接收到信号时调用的函数，或 `null` 重置为默认

**返回：** 之前的处理函数（如果没有则返回 `null`）

**示例：**
```hemlock
fn my_handler(sig) {
    print("Caught signal: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**重置为默认：**
```hemlock
signal(SIGINT, null);  // 将 SIGINT 重置为默认行为
```

### raise(signum)

向当前进程发送信号。

**参数：**
- `signum` (i32) - 要发送的信号编号

**返回：** `null`

**示例：**
```hemlock
raise(SIGUSR1);  // 触发 SIGUSR1 处理器
```

## 信号常量

Hemlock 提供标准 POSIX 信号常量作为 i32 值。

### 中断和终止

| 常量 | 值 | 描述 | 常见触发 |
|------|------|------|----------|
| `SIGINT` | 2 | 键盘中断 | Ctrl+C |
| `SIGTERM` | 15 | 终止请求 | `kill` 命令 |
| `SIGQUIT` | 3 | 键盘退出 | Ctrl+\ |
| `SIGHUP` | 1 | 检测到挂断 | 终端关闭 |
| `SIGABRT` | 6 | 中止信号 | `abort()` 函数 |

**示例：**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // kill 命令
signal(SIGHUP, handle_hangup);      // 终端关闭
```

### 用户定义信号

| 常量 | 值 | 描述 | 用例 |
|------|------|------|------|
| `SIGUSR1` | 10 | 用户定义信号 1 | 自定义 IPC |
| `SIGUSR2` | 12 | 用户定义信号 2 | 自定义 IPC |

**示例：**
```hemlock
// 用于自定义通信
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### 进程控制

| 常量 | 值 | 描述 | 说明 |
|------|------|------|------|
| `SIGALRM` | 14 | 警报时钟定时器 | `alarm()` 后 |
| `SIGCHLD` | 17 | 子进程状态改变 | 进程管理 |
| `SIGCONT` | 18 | 如果停止则继续 | 在 SIGSTOP 后恢复 |
| `SIGSTOP` | 19 | 停止进程 | **无法捕获** |
| `SIGTSTP` | 20 | 终端停止 | Ctrl+Z |

**示例：**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### I/O 信号

| 常量 | 值 | 描述 | 何时发送 |
|------|------|------|----------|
| `SIGPIPE` | 13 | 管道断开 | 写入已关闭的管道 |
| `SIGTTIN` | 21 | 后台从终端读取 | 后台进程读取 TTY |
| `SIGTTOU` | 22 | 后台写入终端 | 后台进程写入 TTY |

**示例：**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## 基本信号处理

### 捕获 Ctrl+C

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("Caught SIGINT!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// 程序继续运行...
// 用户按 Ctrl+C -> 调用 handle_interrupt()

while (!interrupted) {
    // 做工作...
}

print("Exiting due to interrupt");
```

### 处理函数签名

信号处理器接收一个参数：信号编号 (i32)

```hemlock
fn my_handler(signum) {
    print("Received signal: " + typeof(signum));
    // signum 包含信号编号（如 SIGINT 为 2）

    if (signum == SIGINT) {
        print("This is SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // 多个信号使用同一处理器
```

### 多个信号处理器

不同信号使用不同处理器：

```hemlock
fn handle_int(sig) {
    print("SIGINT received");
}

fn handle_term(sig) {
    print("SIGTERM received");
}

fn handle_usr1(sig) {
    print("SIGUSR1 received");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### 重置为默认行为

传递 `null` 作为处理器以重置为默认行为：

```hemlock
// 注册自定义处理器
signal(SIGINT, my_handler);

// 稍后，重置为默认（SIGINT 时终止）
signal(SIGINT, null);
```

### 手动触发信号

向自己的进程发送信号：

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// 手动触发处理器
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## 高级模式

### 优雅关闭模式

终止时清理的常见模式：

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Shutting down gracefully...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// 主循环
while (!should_exit) {
    // 做工作...
    // 定期检查 should_exit 标志
}

print("Cleanup complete");
```

### 信号计数器

跟踪接收的信号数量：

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Received " + typeof(signal_count) + " signals");
}

signal(SIGUSR1, count_signals);

// 稍后...
print("Total signals: " + typeof(signal_count));
```

### 信号重新加载配置

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Reloading configuration...");
    config = load_config();
    print("Configuration reloaded");
}

signal(SIGHUP, reload_config);  // 收到 SIGHUP 时重新加载

// 从 shell 发送 SIGHUP 到进程以重新加载配置
// kill -HUP <pid>
```

### 使用 SIGALRM 的超时

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// 设置警报（Hemlock 中尚未实现，仅示例）
// alarm(5);  // 5 秒超时

while (!timed_out) {
    // 带超时的工作
}
```

### 基于信号的状态机

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("State: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("State: " + typeof(state));
}

signal(SIGUSR1, next_state);  // 前进状态
signal(SIGUSR2, prev_state);  // 后退状态

// 控制状态机：
// kill -USR1 <pid>  # 下一状态
// kill -USR2 <pid>  # 上一状态
```

## 信号处理器行为

### 重要说明

**处理器执行：**
- 处理器在接收到信号时**同步**调用
- 处理器在当前进程上下文中执行
- 信号处理器共享定义它们的函数的闭包环境
- 处理器可以访问和修改外部作用域变量（如全局变量或捕获的变量）

**最佳实践：**
- 保持处理器简单快速 - 避免长时间运行的操作
- 设置标志而不是执行复杂逻辑
- 避免调用可能获取锁的函数
- 注意处理器可以中断任何操作

### 哪些信号可以捕获

**可以捕获和处理：**
- SIGINT、SIGTERM、SIGUSR1、SIGUSR2、SIGHUP、SIGQUIT
- SIGALRM、SIGCHLD、SIGCONT、SIGTSTP
- SIGPIPE、SIGTTIN、SIGTTOU
- SIGABRT（但处理器返回后程序将中止）

**无法捕获：**
- `SIGKILL` (9) - 始终终止进程
- `SIGSTOP` (19) - 始终停止进程

**系统相关：**
- 某些信号的默认行为可能因系统而异
- 查看您平台的信号文档了解详情

### 处理器限制

```hemlock
fn complex_handler(sig) {
    // 在信号处理器中避免这些：

    // ❌ 长时间运行的操作
    // process_large_file();

    // ❌ 阻塞 I/O
    // let f = open("log.txt", "a");
    // f.write("Signal received\n");

    // ❌ 复杂的状态更改
    // rebuild_entire_data_structure();

    // ✅ 简单的标志设置是安全的
    let should_stop = true;

    // ✅ 简单的计数器更新通常是安全的
    let signal_count = signal_count + 1;
}
```

## 安全考虑

按照 Hemlock 的哲学，信号处理**本质上是不安全的**。

### 竞争条件

处理器可以在任何时候被调用，中断正常执行：

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // 如果在 counter 更新期间调用会有竞争条件
}

signal(SIGUSR1, increment);

// 主代码也修改 counter
counter = counter + 1;  // 可能被信号处理器中断
```

**问题：** 如果信号在主代码更新 `counter` 时到达，结果是不可预测的。

### 异步信号安全

Hemlock **不**保证异步信号安全：
- 处理器可以调用任何 Hemlock 代码（不像 C 的受限异步信号安全函数）
- 这提供了灵活性但需要用户谨慎
- 如果处理器修改共享状态，可能出现竞争条件

### 安全信号处理的最佳实践

**1. 使用原子标志**

简单的布尔赋值通常是安全的：

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // 简单赋值是安全的
}

signal(SIGINT, handler);

while (!should_exit) {
    // 工作...
}
```

**2. 最小化共享状态**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // 只修改这一个变量
    interrupt_count = interrupt_count + 1;
}
```

**3. 延迟复杂操作**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // 只设置标志
}

signal(SIGHUP, signal_reload);

// 在主循环中：
while (true) {
    if (pending_reload) {
        reload_config();  // 在这里执行复杂工作
        pending_reload = false;
    }

    // 正常工作...
}
```

**4. 避免重入问题**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // 主代码使用数据时不要修改它
        return;
    }
    // 可以安全继续
}
```

## 常见用例

### 1. 优雅的服务器关闭

```hemlock
let running = true;

fn shutdown(sig) {
    print("Shutdown signal received");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// 服务器主循环
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Server stopped");
```

### 2. 配置重新加载（无需重启）

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Reloading configuration...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // 使用配置...
}
```

### 3. 日志轮转

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // 重命名旧日志，打开新的
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // 正常日志记录...
    log_file.write("Log entry\n");
}
```

### 4. 状态报告

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Status: " + typeof(requests_handled) + " requests handled");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// 从 shell：kill -USR1 <pid>
```

### 5. 调试模式切换

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Debug mode: ON");
    } else {
        print("Debug mode: OFF");
    }
}

signal(SIGUSR2, toggle_debug);

// 从 shell：kill -USR2 <pid> 切换
```

## 完整示例

### 示例 1：带清理的中断处理器

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Interrupt detected (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("User signal 1 received");
    }
}

// 注册处理器
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// 模拟一些工作
let i = 0;
while (running && i < 100) {
    print("Working... " + typeof(i));

    // 每 10 次迭代触发 SIGUSR1
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Total signals received: " + typeof(signal_count));
```

### 示例 2：多信号状态机

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("State: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("State: " + state);
}

fn report_stats(sig) {
    print("State: " + state);
    print("Requests: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // 做工作
        request_count = request_count + 1;
    }

    // 每次迭代检查...
}
```

### 示例 3：工作池控制器

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Workers: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Workers: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Shutting down...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// 主循环根据 worker_count 调整工作池
while (!should_exit) {
    // 根据 worker_count 管理工作者
    // ...
}
```

## 调试信号处理器

### 添加诊断打印

```hemlock
fn debug_handler(sig) {
    print("Handler called for signal: " + typeof(sig));
    print("Stack: (not yet available)");

    // 你的处理器逻辑...
}

signal(SIGINT, debug_handler);
```

### 计数信号调用

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Handler call #" + typeof(handler_calls));

    // 你的处理器逻辑...
}
```

### 使用 raise() 测试

```hemlock
fn test_handler(sig) {
    print("Test signal received: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// 通过手动触发测试
raise(SIGUSR1);
print("Handler should have been called");
```

## 总结

Hemlock 的信号处理提供：

- 用于底层进程控制的 POSIX 信号处理
- 15 个标准信号常量
- 简单的 signal() 和 raise() API
- 灵活的处理函数，支持闭包
- 多个信号可以共享处理器

请记住：
- 信号处理本质上是不安全的 - 谨慎使用
- 保持处理器简单快速
- 使用标志进行状态更改，而不是复杂操作
- 处理器可以在任何时候中断执行
- 无法捕获 SIGKILL 或 SIGSTOP
- 使用 raise() 彻底测试处理器

常见模式：
- 优雅关闭（SIGINT、SIGTERM）
- 配置重新加载（SIGHUP）
- 日志轮转（SIGUSR1）
- 状态报告（SIGUSR1/SIGUSR2）
- 调试模式切换（SIGUSR2）
