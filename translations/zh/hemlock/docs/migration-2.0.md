# 迁移指南：v1.x 到 v2.0.0

## 重大变更：内置函数迁移到标准库

Hemlock 2.0.0 将 63 个全局内置函数移入 `@stdlib` 模块，以减少命名空间污染。使用这些函数但没有导入的代码将会收到"未定义变量"错误。

## 快速修复

为每个函数添加适当的 `import` 语句。下表显示了每个内置函数的新位置。

### 数学函数

```hemlock
// 修改前 (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// 修改后 (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**已移动的函数：** `sin`、`cos`、`tan`、`asin`、`acos`、`atan`、`atan2`、`sinh`、`cosh`、`tanh`、`sqrt`、`cbrt`、`exp`、`log`、`log2`、`log10`、`floor`、`ceil`、`round`、`trunc`、`abs`、`pow`、`fmod`、`min`、`max`、`rand`、`div`、`divi`、`floori`、`ceili`、`roundi`、`trunci`

### 信号处理

```hemlock
// 修改前
signal(SIGINT, handler);

// 修改后
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### 文件系统

```hemlock
// 修改前
let f = open("file.txt", "r");

// 修改后
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### 进程 / 环境

```hemlock
// 修改前
let home = getenv("HOME");
exec("ls");

// 修改后
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### 网络

```hemlock
// 修改前
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// 修改后
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### 原子操作

```hemlock
// 修改前
atomic_store(ptr, 42);

// 修改后
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### FFI 回调

```hemlock
// 修改前
let cb = callback(my_func);

// 修改后
import { callback, callback_free } from "@stdlib/ffi";
```

### 调试 / 栈

```hemlock
// 修改前
let info = task_debug_info(task);

// 修改后
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## 完整模块映射

| 函数 | 新模块 |
|------|--------|
| 数学函数（sin、cos、sqrt 等） | `@stdlib/math` |
| `signal`、`raise`、SIG* 常量 | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`、`exec_argv` | `@stdlib/process` |
| `getenv`、`setenv` | `@stdlib/env` |
| AF_*、SOCK_*、POLL* 常量、`socket_create`、`dns_resolve`、`poll` | `@stdlib/net` |
| `atomic_*` 操作 | `@stdlib/atomic` |
| `callback`、`callback_free`、`ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`、`set_stack_limit`、`get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`、`set_default_stack_size` | `@stdlib/async` |

## 无其他重大变更

所有其他语言特性、语法和 API 保持向后兼容。现有代码只需要添加导入语句。
