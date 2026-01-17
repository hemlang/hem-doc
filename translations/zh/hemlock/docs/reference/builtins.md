# 内置函数参考

Hemlock 所有内置函数和常量的完整参考文档。

---

## 概述

Hemlock 提供了一组内置函数，用于 I/O、类型自省、内存管理、并发和系统交互。所有内置函数全局可用，无需导入。

---

## I/O 函数

### print

将值打印到标准输出并换行。

**签名：**
```hemlock
print(...values): null
```

**参数：**
- `...values` - 任意数量的要打印的值

**返回值：** `null`

**示例：**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// 多个值
print("x =", 10, "y =", 20);
```

**行为：**
- 将所有值转换为字符串
- 多个值之间用空格分隔
- 末尾添加换行符
- 刷新标准输出

---

### read_line

从标准输入读取一行文本（用户输入）。

**签名：**
```hemlock
read_line(): string | null
```

**参数：** 无

**返回值：**
- `string` - 从标准输入读取的行（已去除换行符）
- `null` - 在 EOF（文件结束/输入结束）时

**示例：**
```hemlock
// 简单提示
print("What is your name?");
let name = read_line();
print("Hello, " + name + "!");

// 读取数字（需要手动解析）
print("Enter a number:");
let input = read_line();
let num = parse_int(input);  // 参见下面的 parse_int
print("Double:", num * 2);

// 处理 EOF
let line = read_line();
if (line == null) {
    print("End of input");
}

// 读取多行
print("Enter lines (Ctrl+D to stop):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("You said:", line);
}
```

**行为：**
- 阻塞直到用户按下回车
- 去除尾部的换行符（`\n`）和回车符（`\r`）
- 在 EOF 时返回 `null`（Unix 上为 Ctrl+D，Windows 上为 Ctrl+Z）
- 仅从标准输入读取（不从文件读取）

**解析用户输入：**

由于 `read_line()` 总是返回字符串，你需要手动解析数字输入：

```hemlock
// 简单的整数解析器
fn parse_int(s: string): i32 {
    let result: i32 = 0;
    let negative = false;
    let i = 0;

    if (s.length > 0 && s.char_at(0) == '-') {
        negative = true;
        i = 1;
    }

    while (i < s.length) {
        let c = s.char_at(i);
        let code: i32 = c;
        if (code >= 48 && code <= 57) {
            result = result * 10 + (code - 48);
        } else {
            break;
        }
        i = i + 1;
    }

    if (negative) {
        return -result;
    }
    return result;
}

// 使用
print("Enter your age:");
let age = parse_int(read_line());
print("In 10 years you'll be", age + 10);
```

**另请参阅：** [文件 API](file-api.md) 从文件读取

---

### eprint

将值打印到标准错误并换行。

**签名：**
```hemlock
eprint(value: any): null
```

**参数：**
- `value` - 要打印到标准错误的单个值

**返回值：** `null`

**示例：**
```hemlock
eprint("Error: file not found");
eprint(404);
eprint("Warning: " + message);

// 典型的错误处理模式
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Error: config file not found: " + path);
        return null;
    }
    // ...
}
```

**行为：**
- 打印到标准错误（stderr）
- 末尾添加换行符
- 只接受一个参数（与 `print` 不同）
- 适用于不应与正常输出混合的错误消息

**与 print 的区别：**
- `print()` → stdout（正常输出，可用 `>` 重定向）
- `eprint()` → stderr（错误输出，可用 `2>` 重定向）

```bash
# Shell 示例：分离 stdout 和 stderr
./hemlock script.hml > output.txt 2> errors.txt
```

---

## 类型自省

### typeof

获取值的类型名称。

**签名：**
```hemlock
typeof(value: any): string
```

**参数：**
- `value` - 任意值

**返回值：** 类型名称字符串

**示例：**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// 类型化对象
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// 其他类型
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**类型名称：**
- 基本类型：`"i8"`、`"i16"`、`"i32"`、`"i64"`、`"u8"`、`"u16"`、`"u32"`、`"u64"`、`"f32"`、`"f64"`、`"bool"`、`"string"`、`"rune"`、`"null"`
- 复合类型：`"array"`、`"object"`、`"ptr"`、`"buffer"`、`"function"`
- 特殊类型：`"file"`、`"task"`、`"channel"`
- 自定义类型：来自 `define` 的用户定义类型名称

**另请参阅：** [类型系统](type-system.md)

---

## 命令执行

### exec

执行 shell 命令并捕获输出。

**签名：**
```hemlock
exec(command: string): object
```

**参数：**
- `command` - 要执行的 shell 命令

**返回值：** 包含以下字段的对象：
- `output` (string) - 命令的标准输出
- `exit_code` (i32) - 退出状态码（0 = 成功）

**示例：**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// 检查退出状态
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found:", r.output);
} else {
    print("Pattern not found");
}

// 处理多行输出
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**行为：**
- 通过 `/bin/sh` 执行命令
- 仅捕获标准输出（标准错误输出到终端）
- 阻塞直到命令完成
- 如果没有输出则返回空字符串

**错误处理：**
```hemlock
try {
    let r = exec("nonexistent_command");
} catch (e) {
    print("Failed to execute:", e);
}
```

**安全警告：** 存在 shell 注入风险。始终验证/清理用户输入。

**限制：**
- 无标准错误捕获
- 无流式处理
- 无超时
- 无信号处理

---

### exec_argv

使用显式参数数组执行命令（无 shell 解释）。

**签名：**
```hemlock
exec_argv(argv: array): object
```

**参数：**
- `argv` - 字符串数组：`[command, arg1, arg2, ...]`

**返回值：** 包含以下字段的对象：
- `output` (string) - 命令的标准输出
- `exit_code` (i32) - 退出状态码（0 = 成功）

**示例：**
```hemlock
// 简单命令
let result = exec_argv(["ls", "-la"]);
print(result.output);

// 包含空格的参数（安全！）
let r = exec_argv(["grep", "hello world", "file.txt"]);

// 带参数运行脚本
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**与 exec 的区别：**
```hemlock
// exec() 使用 shell - 对用户输入不安全
exec("ls " + user_input);  // Shell 注入风险！

// exec_argv() 绕过 shell - 安全
exec_argv(["ls", user_input]);  // 不可能注入
```

**何时使用：**
- 当参数包含空格、引号或特殊字符时
- 处理用户输入时（安全性）
- 当需要可预测的参数解析时

**另请参阅：** 简单 shell 命令使用 `exec()`

---

## 错误处理

### throw

抛出异常。

**签名：**
```hemlock
throw expression
```

**参数：**
- `expression` - 要抛出的值（任意类型）

**返回值：** 永不返回（转移控制权）

**示例：**
```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
```

**另请参阅：** try/catch/finally 语句

---

### panic

立即终止程序并显示错误消息（不可恢复）。

**签名：**
```hemlock
panic(message?: any): never
```

**参数：**
- `message`（可选）- 要打印的错误消息

**返回值：** 永不返回（程序退出）

**示例：**
```hemlock
panic();                          // 默认："panic!"
panic("unreachable code reached");
panic(42);

// 常见用例
fn process_state(state: i32): string {
    if (state == 1) { return "ready"; }
    if (state == 2) { return "running"; }
    panic("invalid state: " + typeof(state));
}
```

**行为：**
- 将错误打印到标准错误：`panic: <message>`
- 以代码 1 退出
- **不能**用 try/catch 捕获
- 用于 bug 和不可恢复的错误

**panic 与 throw 的区别：**
- `panic()` - 不可恢复的错误，立即退出
- `throw` - 可恢复的错误，可以被捕获

---

### assert

断言条件为真，否则终止并显示错误消息。

**签名：**
```hemlock
assert(condition: any, message?: string): null
```

**参数：**
- `condition` - 要检查是否为真的值
- `message`（可选）- 断言失败时的自定义错误消息

**返回值：** `null`（如果断言通过）

**示例：**
```hemlock
// 基本断言
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "Array must not be empty");

// 带自定义消息
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Division by zero");
    return a / b;
}

// 验证函数参数
fn process_data(data: array) {
    assert(data != null, "data cannot be null");
    assert(data.length > 0, "data cannot be empty");
    // ...
}
```

**行为：**
- 如果条件为真：返回 `null`，继续执行
- 如果条件为假：打印错误并以代码 1 退出
- 假值：`false`、`0`、`0.0`、`null`、`""`（空字符串）
- 真值：其他所有值

**失败时的输出：**
```
Assertion failed: Array must not be empty
```

**何时使用：**
- 验证函数前置条件
- 在开发期间检查不变量
- 尽早捕获程序员错误

**assert 与 panic 的区别：**
- `assert(cond, msg)` - 检查条件，如果为假则失败
- `panic(msg)` - 无条件失败

---

## 信号处理

### signal

注册或重置信号处理程序。

**签名：**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**参数：**
- `signum` - 信号编号（使用 `SIGINT` 等常量）
- `handler` - 收到信号时调用的函数，或 `null` 重置为默认值

**返回值：** 先前的处理程序函数，或 `null`

**示例：**
```hemlock
fn handle_interrupt(sig) {
    print("Caught SIGINT!");
}

signal(SIGINT, handle_interrupt);

// 重置为默认
signal(SIGINT, null);
```

**处理程序签名：**
```hemlock
fn handler(signum: i32) {
    // signum 包含信号编号
}
```

**另请参阅：**
- [信号常量](#信号常量)
- `raise()`

---

### raise

向当前进程发送信号。

**签名：**
```hemlock
raise(signum: i32): null
```

**参数：**
- `signum` - 要发送的信号编号

**返回值：** `null`

**示例：**
```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

raise(SIGUSR1);
raise(SIGUSR1);
print(count);  // 2
```

---

## 全局变量

### args

命令行参数数组。

**类型：** 字符串 `array`

**结构：**
- `args[0]` - 脚本文件名
- `args[1..n]` - 命令行参数

**示例：**
```bash
# 命令：./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// 遍历参数
let i = 1;
while (i < args.length) {
    print("Argument", i, ":", args[i]);
    i = i + 1;
}
```

**REPL 行为：** 在 REPL 中，`args.length` 为 0（空数组）

---

## 信号常量

标准 POSIX 信号常量（i32 值）：

### 中断和终止

| 常量       | 值    | 描述                               |
|------------|-------|----------------------------------------|
| `SIGINT`   | 2     | 来自键盘的中断（Ctrl+C）               |
| `SIGTERM`  | 15    | 终止请求                               |
| `SIGQUIT`  | 3     | 来自键盘的退出（Ctrl+\）               |
| `SIGHUP`   | 1     | 在控制终端上检测到挂断                 |
| `SIGABRT`  | 6     | 中止信号                               |

### 用户定义

| 常量       | 值    | 描述                     |
|------------|-------|--------------------------|
| `SIGUSR1`  | 10    | 用户定义信号 1           |
| `SIGUSR2`  | 12    | 用户定义信号 2           |

### 进程控制

| 常量       | 值    | 描述                          |
|------------|-------|-------------------------------|
| `SIGALRM`  | 14    | 闹钟定时器                    |
| `SIGCHLD`  | 17    | 子进程状态变化                |
| `SIGCONT`  | 18    | 如果停止则继续                |
| `SIGSTOP`  | 19    | 停止进程（不能被捕获）        |
| `SIGTSTP`  | 20    | 终端停止（Ctrl+Z）            |

### I/O

| 常量       | 值    | 描述                           |
|------------|-------|--------------------------------|
| `SIGPIPE`  | 13    | 管道破裂                       |
| `SIGTTIN`  | 21    | 后台从终端读取                 |
| `SIGTTOU`  | 22    | 后台写入终端                   |

**示例：**
```hemlock
fn handle_signal(sig) {
    if (sig == SIGINT) {
        print("Interrupt detected");
    }
    if (sig == SIGTERM) {
        print("Termination requested");
    }
}

signal(SIGINT, handle_signal);
signal(SIGTERM, handle_signal);
```

**注意：** `SIGKILL` (9) 和 `SIGSTOP` (19) 不能被捕获或忽略。

---

## 数学/算术函数

### div

返回浮点数的向下整除。

**签名：**
```hemlock
div(a: number, b: number): f64
```

**参数：**
- `a` - 被除数
- `b` - 除数

**返回值：** `a / b` 的向下取整结果，作为浮点数 (f64)

**示例：**
```hemlock
let result = div(7, 2);    // 3.0（不是 3.5）
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0（向下取整朝向负无穷）
```

**注意：** 在 Hemlock 中，`/` 运算符总是返回浮点数。当需要整数部分作为浮点数时使用 `div()`，或者当需要整数结果时使用 `divi()`。

---

### divi

返回整数的向下整除。

**签名：**
```hemlock
divi(a: number, b: number): i64
```

**参数：**
- `a` - 被除数
- `b` - 除数

**返回值：** `a / b` 的向下取整结果，作为整数 (i64)

**示例：**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4（向下取整朝向负无穷）
```

**比较：**
```hemlock
print(7 / 2);      // 3.5（常规除法，总是浮点数）
print(div(7, 2));  // 3.0（向下整除，浮点数结果）
print(divi(7, 2)); // 3  （向下整除，整数结果）
```

---

## 内存管理函数

参见 [内存 API](memory-api.md) 获取完整参考：
- `alloc(size)` - 分配原始内存
- `free(ptr)` - 释放内存
- `buffer(size)` - 分配安全缓冲区
- `memset(ptr, byte, size)` - 填充内存
- `memcpy(dest, src, size)` - 复制内存
- `realloc(ptr, new_size)` - 调整分配大小

### sizeof

获取类型的字节大小。

**签名：**
```hemlock
sizeof(type): i32
```

**参数：**
- `type` - 类型常量（`i32`、`f64`、`ptr` 等）或类型名称字符串

**返回值：** 字节大小，作为 `i32`

**示例：**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// 使用类型别名
print(sizeof(byte));     // 1（与 u8 相同）
print(sizeof(integer));  // 4（与 i32 相同）
print(sizeof(number));   // 8（与 f64 相同）

// 字符串形式也可以
print(sizeof("i32"));    // 4
```

**支持的类型：**
| 类型 | 大小 | 别名 |
|------|------|---------|
| `i8` | 1 | - |
| `i16` | 2 | - |
| `i32` | 4 | `integer` |
| `i64` | 8 | - |
| `u8` | 1 | `byte` |
| `u16` | 2 | - |
| `u32` | 4 | - |
| `u64` | 8 | - |
| `f32` | 4 | - |
| `f64` | 8 | `number` |
| `ptr` | 8 | - |
| `rune` | 4 | - |
| `bool` | 1 | - |

**另请参阅：** `talloc()` 用于类型化分配

---

### talloc

为类型化数组分配内存（类型感知分配）。

**签名：**
```hemlock
talloc(type, count: i32): ptr
```

**参数：**
- `type` - 类型常量（`i32`、`f64`、`ptr` 等）
- `count` - 要分配的元素数量

**返回值：** 指向已分配内存的 `ptr`，失败时返回 `null`

**示例：**
```hemlock
// 分配 10 个 i32 的数组（40 字节）
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// 分配 5 个 f64 的数组（40 字节）
let float_arr = talloc(f64, 5);

// 分配 100 字节的数组
let byte_arr = talloc(u8, 100);

// 别忘了释放！
free(int_arr);
free(float_arr);
free(byte_arr);
```

**与 alloc 的比较：**
```hemlock
// 这些是等价的：
let p1 = talloc(i32, 10);      // 类型感知：10 个 i32
let p2 = alloc(sizeof(i32) * 10);  // 手动计算

// talloc 更清晰，更不容易出错
```

**错误处理：**
- 分配失败时返回 `null`
- 如果 count 不是正数则退出并报错
- 检查大小溢出（count * element_size）

**另请参阅：** `alloc()`、`sizeof()`、`free()`

---

## FFI 指针辅助函数

这些函数帮助读写原始内存中的类型化值，对 FFI 和底层内存操作很有用。

### ptr_null

创建空指针。

**签名：**
```hemlock
ptr_null(): ptr
```

**返回值：** 空指针

**示例：**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Pointer is null");
}
```

---

### ptr_offset

计算指针偏移（指针算术）。

**签名：**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**参数：**
- `ptr` - 基指针
- `index` - 元素索引
- `element_size` - 每个元素的字节大小

**返回值：** 指向给定索引处元素的指针

**示例：**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### 指针读取函数

从内存读取类型化值。

| 函数 | 签名 | 返回值 | 描述 |
|----------|-----------|---------|-------------|
| `ptr_read_i8` | `(ptr)` | `i8` | 读取有符号 8 位整数 |
| `ptr_read_i16` | `(ptr)` | `i16` | 读取有符号 16 位整数 |
| `ptr_read_i32` | `(ptr)` | `i32` | 读取有符号 32 位整数 |
| `ptr_read_i64` | `(ptr)` | `i64` | 读取有符号 64 位整数 |
| `ptr_read_u8` | `(ptr)` | `u8` | 读取无符号 8 位整数 |
| `ptr_read_u16` | `(ptr)` | `u16` | 读取无符号 16 位整数 |
| `ptr_read_u32` | `(ptr)` | `u32` | 读取无符号 32 位整数 |
| `ptr_read_u64` | `(ptr)` | `u64` | 读取无符号 64 位整数 |
| `ptr_read_f32` | `(ptr)` | `f32` | 读取 32 位浮点数 |
| `ptr_read_f64` | `(ptr)` | `f64` | 读取 64 位浮点数 |
| `ptr_read_ptr` | `(ptr)` | `ptr` | 读取指针值 |

**示例：**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### 指针写入函数

向内存写入类型化值。

| 函数 | 签名 | 返回值 | 描述 |
|----------|-----------|---------|-------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | 写入有符号 8 位整数 |
| `ptr_write_i16` | `(ptr, value)` | `null` | 写入有符号 16 位整数 |
| `ptr_write_i32` | `(ptr, value)` | `null` | 写入有符号 32 位整数 |
| `ptr_write_i64` | `(ptr, value)` | `null` | 写入有符号 64 位整数 |
| `ptr_write_u8` | `(ptr, value)` | `null` | 写入无符号 8 位整数 |
| `ptr_write_u16` | `(ptr, value)` | `null` | 写入无符号 16 位整数 |
| `ptr_write_u32` | `(ptr, value)` | `null` | 写入无符号 32 位整数 |
| `ptr_write_u64` | `(ptr, value)` | `null` | 写入无符号 64 位整数 |
| `ptr_write_f32` | `(ptr, value)` | `null` | 写入 32 位浮点数 |
| `ptr_write_f64` | `(ptr, value)` | `null` | 写入 64 位浮点数 |
| `ptr_write_ptr` | `(ptr, value)` | `null` | 写入指针值 |

**示例：**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### 缓冲区/指针转换

#### buffer_ptr

从缓冲区获取原始指针。

**签名：**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**示例：**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// 现在 p 指向与 buf 相同的内存
```

#### ptr_to_buffer

围绕原始指针创建缓冲区包装器。

**签名：**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**示例：**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // 现在有边界检查
// 注意：释放 buf 将释放底层内存
```

---

## 文件 I/O 函数

参见 [文件 API](file-api.md) 获取完整参考：
- `open(path, mode?)` - 打开文件

---

## 并发函数

参见 [并发 API](concurrency-api.md) 获取完整参考：
- `spawn(fn, args...)` - 派生任务
- `join(task)` - 等待任务
- `detach(task)` - 分离任务
- `channel(capacity)` - 创建通道

### apply

使用参数数组动态调用函数。

**签名：**
```hemlock
apply(fn: function, args: array): any
```

**参数：**
- `fn` - 要调用的函数
- `args` - 要传递给函数的参数数组

**返回值：** 被调用函数的返回值

**示例：**
```hemlock
fn add(a, b) {
    return a + b;
}

// 使用参数数组调用
let result = apply(add, [2, 3]);
print(result);  // 5

// 动态分派
let operations = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calculate(op: string, args: array) {
    return apply(operations[op], args);
}

print(calculate("add", [10, 5]));  // 15
print(calculate("mul", [10, 5]));  // 50
print(calculate("sub", [10, 5]));  // 5

// 可变参数
fn sum(...nums) {
    let total = 0;
    for (n in nums) {
        total = total + n;
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5];
print(apply(sum, numbers));  // 15
```

**用例：**
- 基于运行时值的动态函数分派
- 调用具有可变参数列表的函数
- 实现高阶工具（map、filter 等）
- 插件/扩展系统

---

### select

等待多个通道的数据，当任一通道有数据时返回。

**签名：**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**参数：**
- `channels` - 通道值数组
- `timeout_ms`（可选）- 超时毫秒数（-1 或省略表示无限等待）

**返回值：**
- `{ channel, value }` - 包含有数据的通道和接收到的值的对象
- `null` - 超时时

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

// 等待第一条消息
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"（先到达）

// 带超时
let result2 = select([ch1, ch2], 1000);  // 等待最多 1 秒
if (result2 == null) {
    print("Timeout - no data received");
} else {
    print("Received:", result2.value);
}

// 连续 select 循环
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("No activity for 5 seconds");
        break;
    }
    print("Got message:", msg.value);
}
```

**行为：**
- 阻塞直到一个通道有数据或超时到期
- 如果通道已有数据则立即返回
- 如果通道已关闭且为空，返回 `{ channel, value: null }`
- 按顺序轮询通道（第一个就绪的通道获胜）

**用例：**
- 多路复用多个生产者
- 在通道操作上实现超时
- 构建具有多个源的事件循环

---

## 总结表

### 函数

| 函数       | 类别            | 返回值       | 描述                            |
|------------|-----------------|--------------|----------------------------------|
| `print`    | I/O             | `null`       | 打印到标准输出                   |
| `read_line`| I/O             | `string?`    | 从标准输入读取行                 |
| `eprint`   | I/O             | `null`       | 打印到标准错误                   |
| `typeof`   | 类型            | `string`     | 获取类型名称                     |
| `exec`     | 命令            | `object`     | 执行 shell 命令                  |
| `exec_argv`| 命令            | `object`     | 使用参数数组执行                 |
| `assert`   | 错误            | `null`       | 断言条件或退出                   |
| `panic`    | 错误            | `never`      | 不可恢复的错误（退出）           |
| `signal`   | 信号            | `function?`  | 注册信号处理程序                 |
| `raise`    | 信号            | `null`       | 向进程发送信号                   |
| `alloc`    | 内存            | `ptr`        | 分配原始内存                     |
| `talloc`   | 内存            | `ptr`        | 类型化分配                       |
| `sizeof`   | 内存            | `i32`        | 获取类型字节大小                 |
| `free`     | 内存            | `null`       | 释放内存                         |
| `buffer`   | 内存            | `buffer`     | 分配安全缓冲区                   |
| `memset`   | 内存            | `null`       | 填充内存                         |
| `memcpy`   | 内存            | `null`       | 复制内存                         |
| `realloc`  | 内存            | `ptr`        | 调整分配大小                     |
| `open`     | 文件 I/O        | `file`       | 打开文件                         |
| `spawn`    | 并发            | `task`       | 派生并发任务                     |
| `join`     | 并发            | `any`        | 等待任务结果                     |
| `detach`   | 并发            | `null`       | 分离任务                         |
| `channel`  | 并发            | `channel`    | 创建通信通道                     |
| `select`   | 并发            | `object?`    | 等待多个通道                     |
| `apply`    | 函数            | `any`        | 使用参数数组调用函数             |

### 全局变量

| 变量       | 类型     | 描述                              |
|------------|----------|-----------------------------------|
| `args`     | `array`  | 命令行参数                        |

### 常量

| 常量       | 类型  | 类别   | 值    | 描述                      |
|------------|-------|--------|-------|---------------------------|
| `SIGINT`   | `i32` | 信号   | 2     | 键盘中断                  |
| `SIGTERM`  | `i32` | 信号   | 15    | 终止请求                  |
| `SIGQUIT`  | `i32` | 信号   | 3     | 键盘退出                  |
| `SIGHUP`   | `i32` | 信号   | 1     | 挂断                      |
| `SIGABRT`  | `i32` | 信号   | 6     | 中止                      |
| `SIGUSR1`  | `i32` | 信号   | 10    | 用户定义 1                |
| `SIGUSR2`  | `i32` | 信号   | 12    | 用户定义 2                |
| `SIGALRM`  | `i32` | 信号   | 14    | 闹钟定时器                |
| `SIGCHLD`  | `i32` | 信号   | 17    | 子进程状态变化            |
| `SIGCONT`  | `i32` | 信号   | 18    | 继续                      |
| `SIGSTOP`  | `i32` | 信号   | 19    | 停止（不可捕获）          |
| `SIGTSTP`  | `i32` | 信号   | 20    | 终端停止                  |
| `SIGPIPE`  | `i32` | 信号   | 13    | 管道破裂                  |
| `SIGTTIN`  | `i32` | 信号   | 21    | 后台终端读取              |
| `SIGTTOU`  | `i32` | 信号   | 22    | 后台终端写入              |

---

## 另请参阅

- [类型系统](type-system.md) - 类型和转换
- [内存 API](memory-api.md) - 内存分配函数
- [文件 API](file-api.md) - 文件 I/O 函数
- [并发 API](concurrency-api.md) - 异步/并发函数
- [字符串 API](string-api.md) - 字符串方法
- [数组 API](array-api.md) - 数组方法
