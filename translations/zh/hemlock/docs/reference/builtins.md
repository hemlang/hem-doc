# 内置函数参考

Hemlock v2.0.0 所有内置函数和常量的完整参考。

> **v2.0.0 重大变更：** 63 个内置函数从全局命名空间移至 `@stdlib` 模块。`sin()`、`open()`、`exec()`、`signal()` 等函数以及 `SIGINT`、`AF_INET` 等常量现在需要导入。完整列表请参见[已移至标准库](#已移至标准库模块)。

---

## 全局内置函数（无需导入）

以下函数在任何地方都可用，无需 `import` 语句。

### I/O

| 函数 | 描述 |
|------|------|
| `print(value, ...)` | 将值打印到 stdout 并换行 |
| `write(value)` | 将值打印到 stdout 不换行（立即刷新） |
| `eprint(value, ...)` | 将值打印到 stderr 并换行 |
| `read_line()` | 从 stdin 读取一行；返回 `string` 或 EOF 时返回 `null` |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline（无 \n）
eprint("error!");           // -> stderr
let name = read_line();     // 阻塞直到有输入
```

### 内存管理

| 函数 | 描述 |
|------|------|
| `alloc(size)` | 分配 `size` 字节的原始内存，返回 `ptr` |
| `talloc(type, count)` | 类型感知分配：`talloc(i32, 10)` 分配 10 个 i32 |
| `realloc(ptr, new_size)` | 调整之前分配的内存大小 |
| `free(ptr)` | 释放已分配的内存 |
| `memset(ptr, value, size)` | 将 `size` 字节设置为 `value` |
| `memcpy(dest, src, size)` | 从 `src` 复制 `size` 字节到 `dest` |
| `buffer(size)` | 创建 `size` 字节的边界检查缓冲区 |

```hemlock
let p = alloc(64);       // 原始指针，无边界检查
let b = buffer(64);      // 安全缓冲区，带边界检查
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // 手动清理
```

### 类型系统

| 函数 | 描述 |
|------|------|
| `typeof(value)` | 返回类型名称字符串（`"i32"`、`"string"` 等） |
| `typeid(value)` | 返回类型的整数常量（比 `typeof()` 更快的比较方式） |
| `sizeof(type)` | 返回类型的字节大小（`sizeof(i32)` → 4） |

**类型构造函数**（用于转换和类型化分配）：

`i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`rune`、`ptr`

**类型别名：** `integer` (i32)、`number` (f64)、`byte` (u8)

**TYPEID 常量**（与 `typeid()` 配合使用）：

| 常量 | 值 | 常量 | 值 |
|------|------|------|------|
| `TYPEID_I8` | 0 | `TYPEID_STRING` | 11 |
| `TYPEID_I16` | 1 | `TYPEID_RUNE` | 12 |
| `TYPEID_I32` | 2 | `TYPEID_PTR` | 13 |
| `TYPEID_I64` | 3 | `TYPEID_BUFFER` | 14 |
| `TYPEID_U8` | 4 | `TYPEID_ARRAY` | 15 |
| `TYPEID_U16` | 5 | `TYPEID_OBJECT` | 16 |
| `TYPEID_U32` | 6 | `TYPEID_FILE` | 17 |
| `TYPEID_U64` | 7 | `TYPEID_FUNCTION` | 18 |
| `TYPEID_F32` | 8 | `TYPEID_TASK` | 19 |
| `TYPEID_F64` | 9 | `TYPEID_CHANNEL` | 20 |
| `TYPEID_BOOL` | 10 | `TYPEID_NULL` | 21 |

```hemlock
typeof(42);         // "i32"
typeof("hello");    // "string"
sizeof(i64);        // 8
let n = i32("42");  // 将字符串解析为 i32

// typeid() 返回整数 - 比 typeof() 字符串比较更快
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("integer type");
}
```

### 控制流

| 函数 | 描述 |
|------|------|
| `assert(condition, message?)` | 条件为假时 panic |
| `panic(message)` | 立即不可恢复退出（try/catch 无法捕获） |

```hemlock
assert(x > 0, "x must be positive");
panic("unrecoverable error");
```

### 并发

| 函数 | 描述 |
|------|------|
| `spawn(fn, args...)` | 派生异步任务，返回任务句柄 |
| `spawn_with(options, fn, args...)` | 带每线程配置派生（`stack_size` 字节，`name` 字符串最多 16 字符） |
| `join(task)` | 等待任务完成，返回结果 |
| `detach(task)` | 让任务独立运行（即发即弃） |
| `channel(capacity?)` | 创建通信通道（0 = 无缓冲） |
| `select(channels)` | 在多个通道上等待 |
| `apply(fn, args_array)` | 用参数数组调用函数 |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### 指针 / FFI 辅助函数

这些是全局函数，因为它们是与 `alloc`/`free` 配合使用的底层原语。

| 函数 | 描述 |
|------|------|
| `ptr_offset(ptr, bytes)` | 将指针偏移指定字节 |
| `ptr_null()` | 获取空指针 |
| `ptr_to_buffer(ptr, size)` | 将指针包装在边界检查缓冲区中 |
| `buffer_ptr(buffer)` | 从缓冲区获取原始指针 |

**所有数值类型和 `ptr` 的指针读/写/解引用：**

```
ptr_read_i8, ptr_read_i16, ptr_read_i32, ptr_read_i64
ptr_read_u8, ptr_read_u16, ptr_read_u32, ptr_read_u64
ptr_read_f32, ptr_read_f64, ptr_read_ptr

ptr_write_i8, ptr_write_i16, ptr_write_i32, ptr_write_i64
ptr_write_u8, ptr_write_u16, ptr_write_u32, ptr_write_u64
ptr_write_f32, ptr_write_f64, ptr_write_ptr

ptr_deref_i8, ptr_deref_i16, ptr_deref_i32, ptr_deref_i64
ptr_deref_u8, ptr_deref_u16, ptr_deref_u32, ptr_deref_u64
ptr_deref_f32, ptr_deref_f64, ptr_deref_ptr
```

所有 `ptr_read_*`、`ptr_write_*` 和 `ptr_deref_*` 函数直接接受 `ptr` 和 `buffer` 类型：

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// 也可直接用于缓冲区（无需 buffer_ptr()）
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## 已移至标准库模块

这些内置函数在 v2.0.0 中已移至标准库，现在需要导入。

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**函数：** `sin`、`cos`、`tan`、`asin`、`acos`、`atan`、`atan2`、`sqrt`、`pow`、`exp`、`log`、`log10`、`log2`、`floor`、`ceil`、`round`、`trunc`、`floori`、`ceili`、`roundi`、`trunci`、`div`、`divi`、`abs`、`min`、`max`、`clamp`、`rand`、`rand_range`、`seed`

**常量：** `PI`、`E`、`TAU`、`INF`、`NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**函数：** `getenv`、`setenv`、`unsetenv`、`get_pid`、`exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**函数：** `signal`、`raise`

**常量：** `SIGINT`、`SIGTERM`、`SIGHUP`、`SIGQUIT`、`SIGABRT`、`SIGUSR1`、`SIGUSR2`、`SIGALRM`、`SIGCHLD`、`SIGPIPE`、`SIGCONT`、`SIGSTOP`、`SIGTSTP`、`SIGTTIN`、`SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**函数：** `socket_create`、`dns_resolve`、`poll`

**常量：** `AF_INET`、`AF_INET6`、`SOCK_STREAM`、`SOCK_DGRAM`、`IPPROTO_TCP`、`IPPROTO_UDP`、`SOL_SOCKET`、`SO_REUSEADDR`、`SO_KEEPALIVE`、`SO_RCVTIMEO`、`SO_SNDTIMEO`、`POLLIN`、`POLLOUT`、`POLLERR`、`POLLHUP`、`POLLNVAL`、`POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**函数：** `exec`、`exec_argv`、`fork`、`wait`、`waitpid`、`kill`、`abort`、`exit`、`get_pid`、`getppid`、`getuid`、`geteuid`、`getgid`、`getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**函数：** `open`、`read_file`、`write_file`、`append_file`、`remove_file`、`rename`、`copy_file`、`is_file`、`is_dir`、`file_stat`、`make_dir`、`remove_dir`、`list_dir`、`cwd`、`chdir`、`absolute_path`、`exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**函数：** `now`、`time_ms`、`sleep`、`clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**函数 (i32)：** `atomic_load_i32`、`atomic_store_i32`、`atomic_add_i32`、`atomic_sub_i32`、`atomic_and_i32`、`atomic_or_i32`、`atomic_xor_i32`、`atomic_cas_i32`、`atomic_exchange_i32`

**函数 (i64)：** `atomic_load_i64`、`atomic_store_i64`、`atomic_add_i64`、`atomic_sub_i64`、`atomic_and_i64`、`atomic_or_i64`、`atomic_xor_i64`、`atomic_cas_i64`、`atomic_exchange_i64`

**函数：** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**函数：** `task_debug_info`、`set_stack_limit`、`get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**函数：** `callback`、`callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**函数：** `string_concat_many`

---

## 迁移指南 (v1.x → v2.0.0)

### 修改前 (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### 修改后 (v2.0.0)
```hemlock
import { sin, PI } from "@stdlib/math";
import { get_pid } from "@stdlib/env";
import { signal, SIGUSR1 } from "@stdlib/signal";
import { open } from "@stdlib/fs";
import { exec } from "@stdlib/process";

let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

函数调用本身完全相同——只有导入语句改变了。
