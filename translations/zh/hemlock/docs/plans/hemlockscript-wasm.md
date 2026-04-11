# HemlockScript：Hemlock → WASM（通过 Emscripten）

> 可在浏览器中运行的可移植 Hemlock 程序。

## 目标

为 `hemlockc` 添加 WASM 编译目标，使 Hemlock 程序可以在浏览器和其他 WASM 运行时（Node/Deno/Cloudflare Workers）中运行。方法是：编译 Hemlock → C（现有流水线）→ WASM（通过 Emscripten），使用浏览器兼容的运行时 shim 替换仅 POSIX 的内置函数。

**非目标：** 重写编译器或运行时。我们尽可能利用现有的 `hemlockc` C 代码生成和 `libhemlock_runtime`。

---

## 架构

```
Hemlock 源代码 (.hml)
        ↓
   hemlockc（现有前端 + 代码生成）
        ↓
   生成的 C 代码（现有）
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a（WASM 适配运行时）
        ↓
   program.wasm + program.js（加载器/胶水代码）
        ↓
   浏览器 / Node / Deno / WASM 运行时
```

关键洞察：`hemlockc` 已经生成可移植的 C 代码。我们不需要新的后端——我们需要一个 WASM 兼容的运行时库和 Emscripten 构建流水线。

---

## 阶段 1：最小 WASM 构建（仅核心语言）

**成果：** `make wasm` 生成可在浏览器中运行纯计算 Hemlock 程序的 `.wasm` + `.js` 包。

### 1.1 创建 WASM 运行时 shim 层

创建 `runtime/src/wasm_shim.c`，包含 POSIX 依赖函数的桩/替换实现。针对 WASM 目标时，此文件*替代* POSIX 实现编译。

**需要桩（调用时报错）的函数：**
- `fork()`、`execve()`、`waitpid()`、`kill()` — 进程管理
- `signal()`、`raise()` — 信号处理
- `dlopen()`、`dlsym()`、`dlclose()` — 动态库加载（FFI）

**需要适配的函数：**
- `print()` / `eprint()` → Emscripten 的 `printf`/`fprintf(stderr)`（直接工作，因为 Emscripten 映射到 `console.log`/`console.error`）
- `sleep()` → `emscripten_sleep()`（需要 `-sASYNCIFY`）
- `time_ms()` / `now()` → `emscripten_get_now()` 或 `gettimeofday()`（Emscripten 提供）

**需要禁用（用 `#ifdef __EMSCRIPTEN__` 编译排除）的函数：**
- `builtins_socket.c` 全部（TCP/UDP 套接字）
- `builtins_http.c` 全部（基于 libwebsockets 的 HTTP）
- `builtins_process.c` 全部（fork/exec/signals）
- `builtins_ffi.c` 全部（基于 dlopen 的 FFI）
- `builtins_async.c` 中的线程创建（pthread_create）

### 1.2 在运行时添加 `#ifdef __EMSCRIPTEN__` 守卫

用预处理器守卫包裹现有运行时源文件中的仅 POSIX 代码。这优于维护运行时的单独分支。

需要守卫的文件：

| 文件 | 需要守卫的内容 | 替换 |
|------|-------------|------|
| `builtins_process.c` | 整个文件 | `panic("not available in WASM")` 的桩 |
| `builtins_socket.c` | 整个文件 | 桩 |
| `builtins_http.c` | 整个文件 | 桩 |
| `builtins_ffi.c` | `dlopen`/`dlsym`/`ffi_call` | 桩 |
| `builtins_async.c` | `pthread_create`、通道 | 单线程桩（阶段 1） |
| `builtins_io.c` | `open()`、`read()`、`write()` | Emscripten MEMFS（基本 I/O 直接工作） |
| `builtins_time.c` | `clock_gettime`、`nanosleep` | Emscripten 等价物 |
| `builtins_crypto.c` | OpenSSL 调用 | 桩（阶段 1）、Web Crypto API（阶段 3） |
| `atomics.c` | 原子操作 | Emscripten 提供 `<stdatomic.h>`，应该可用 |

### 1.3 创建 WASM 专用 Makefile 目标

添加到 `runtime/Makefile`：

```makefile
# 通过 Emscripten 构建 WASM
wasm: $(BUILD_DIR)/libhemlock_runtime_wasm.a

$(BUILD_DIR)/libhemlock_runtime_wasm.a: $(WASM_OBJS)
	emar rcs $@ $^

$(BUILD_DIR)/wasm_%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	emcc $(WASM_CFLAGS) -c $< -o $@
```

添加到顶层 `Makefile`：

```makefile
# 为 WASM 构建 Hemlock 程序
wasm: compiler runtime-wasm
	@echo "Usage: make wasm-compile FILE=program.hml"

wasm-compile: compiler runtime-wasm
	./hemlockc -c $(FILE) -o /tmp/hemlock_wasm.c
	emcc -O2 -s WASM=1 -s EXPORTED_FUNCTIONS='["_main"]' \
	     -I runtime/include \
	     /tmp/hemlock_wasm.c \
	     runtime/build/libhemlock_runtime_wasm.a \
	     -o $(basename $(FILE)).js
	@echo "Built: $(basename $(FILE)).js + $(basename $(FILE)).wasm"

runtime-wasm:
	$(MAKE) -C $(RUNTIME_DIR) wasm
```

### 1.4 修改 `hemlockc` 以支持 WASM 目标

添加 `--target wasm` 标志到 `hemlockc`：
1. 在生成的 C 代码中定义 `__HEMLOCK_WASM__`（`#define __HEMLOCK_WASM__ 1`）
2. 针对 WASM 时生成 `#include <emscripten.h>`
3. 跳过不支持特性的代码生成（FFI extern 声明、信号）
4. 使用 `emscripten_sleep()` 替代平台 `sleep()`

### 1.5 创建 HTML 测试页面

创建 `wasm/index.html` — 最小测试页面：

```html
<!DOCTYPE html>
<html>
<head><title>HemlockScript</title></head>
<body>
  <pre id="output"></pre>
  <script>
    var Module = {
      print: function(text) {
        document.getElementById('output').textContent += text + '\n';
      },
      printErr: function(text) {
        console.error(text);
      }
    };
  </script>
  <script src="program.js"></script>
</body>
</html>
```

### 阶段 1 交付物
- `make wasm-compile FILE=hello.hml` 生成可在浏览器中运行的输出
- 所有纯计算 Hemlock 特性正常工作：变量、函数、闭包、控制流、模式匹配、对象、数组、字符串、数学、类型系统
- `print()` 输出到浏览器控制台 / HTML 元素
- 不支持的特性（FFI、套接字、进程、信号）以清晰消息 panic

---

## 阶段 2：浏览器 I/O 和标准库

**成果：** Hemlock 程序可以在浏览器中做有用的工作——文件访问（虚拟文件系统）、时间操作，以及可移植的 stdlib 模块正常工作。

### 2.1 Emscripten 虚拟文件系统

Emscripten 默认提供 MEMFS（内存文件系统）。Hemlock 的 `open()`/`read()`/`write()` 调用已通过 libc，因此在阶段 1 中无需更改即可在 MEMFS 上工作。

对于持久存储，添加可选的 IDBFS（IndexedDB 支持）。

### 2.2 移植 22 个已可移植的 stdlib 模块

这些模块是纯 Hemlock，不需要更改：

`arena`、`assert`、`collections`、`csv`、`datetime`、`encoding`、`fmt`、`iter`、`json`、`logging`、`math`、`path`、`random`、`regex`、`retry`、`semver`、`strings`、`testing`、`terminal`、`toml`、`url`、`uuid`

### 2.3 适配时间模块

- `now()` → `emscripten_get_now()`
- `time_ms()` → `gettimeofday()`
- `sleep(ms)` → `emscripten_sleep(ms)`（需要 `-sASYNCIFY`）
- `clock()` → Emscripten 提供 libc 的 `clock()`

### 2.4 适配 env/os/args 模块

- `getenv()`/`setenv()` → Emscripten 提供（内存 env）
- `platform()` → 返回 `"wasm"`
- `arch()` → 返回 `"wasm32"`
- `args` → 可通过 JS 的 `Module.arguments` 设置

---

## 阶段 3：JavaScript 互操作桥接

**成果：** Hemlock WASM 程序可以调用浏览器 API 和 JavaScript 函数，JavaScript 也可以调用 Hemlock 函数。

### 3.1 JavaScript 桥接

创建 JS 到 WASM 互操作层，替代浏览器的 FFI：

```hemlock
// 替代：import "libcrypto.so.6"; extern fn ...
// 使用：import { fetch, setTimeout } from "@wasm/browser";

import { fetch } from "@wasm/browser";
let response = await fetch("https://api.example.com/data");
print(response);
```

### 3.2 导出函数（Hemlock → JS）

允许从 JavaScript 调用 Hemlock 函数：

```hemlock
// math_utils.hml
export fn fibonacci(n: i32): i32 {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

JS 端：
```javascript
const fib = Module.cwrap('hml_fn_fibonacci', 'number', ['number', 'number']);
console.log(fib(0, 10)); // 55
```

### 3.3 适配网络模块到浏览器

| Hemlock API | 浏览器替换 |
|-------------|----------|
| `http_get(url)` | 通过 Asyncify 的 `fetch()` |
| `http_post(url, body)` | 带 POST 的 `fetch()` |
| `WebSocket(url)` | 浏览器 `WebSocket` API |

### 3.4 适配加密模块

用 Web Crypto API 替换 OpenSSL。

---

## 阶段 4：异步和线程（延伸目标）

**成果：** Hemlock 的 `spawn`/`await` 使用 Web Workers 在浏览器中工作。

### 4.1 基于 Web Worker 的任务派生

将 Hemlock 的 `spawn()` 映射到 Web Workers：

```
Hemlock spawn(fn, args)  →  new Worker() + SharedArrayBuffer
Hemlock join(task)       →  Atomics.wait() / 消息传递
Hemlock channel          →  MessagePort 或 SharedArrayBuffer 环形缓冲区
```

### 4.2 阻塞操作的 Asyncify

使用 Emscripten 的 Asyncify 处理阻塞调用。Asyncify 增加约 10% 的代码大小开销，但支持同步风格的代码。

---

## 文件更改摘要

### 新文件
```
runtime/src/wasm_shim.c          — POSIX 函数的 WASM 桩
runtime/src/wasm_bridge.c        — JS 互操作桥接（阶段 3）
wasm/                            — WASM 输出目录
wasm/index.html                  — 测试页面
wasm/hemlock.js                  — 可选 JS 包装器/加载器 API
tests/wasm/                      — WASM 专用测试
tests/wasm/run_wasm_tests.sh     — 测试运行器（使用 Node.js）
```

### 修改的文件
```
Makefile                         — 添加 wasm、wasm-compile、wasm-test 目标
runtime/Makefile                 — 添加使用 emcc/emar 的 wasm 构建目标
src/backends/compiler/main.c     — 添加 --target wasm 标志
src/backends/compiler/codegen_program.c — WASM 前言生成
runtime/src/builtins_process.c   — #ifdef __EMSCRIPTEN__ 守卫
runtime/src/builtins_socket.c    — #ifdef __EMSCRIPTEN__ 守卫
runtime/src/builtins_http.c      — #ifdef __EMSCRIPTEN__ 守卫
runtime/src/builtins_ffi.c       — #ifdef __EMSCRIPTEN__ 守卫
runtime/src/builtins_async.c     — #ifdef __EMSCRIPTEN__ 守卫
runtime/src/builtins_io.c        — #ifdef __EMSCRIPTEN__ 用于 MEMFS/IDBFS
runtime/src/builtins_time.c      — #ifdef 用于 emscripten_sleep
runtime/src/builtins_crypto.c    — #ifdef 用于 Web Crypto 桩
runtime/include/hemlock_runtime.h — WASM 特性检测宏
```

---

## 构建需求

- **Emscripten SDK**（emcc、emar、emconfigure）
- **Node.js**（用于在浏览器外运行 WASM 测试）
- 所有现有构建需求（用于 hemlockc 编译器本身）

编译器（`hemlockc`）仍然原生构建——只有*输出*目标 WASM。

---

## 无需更改即可工作的内容

这些 Hemlock 特性编译为 Emscripten 原生处理的标准 C：

- 所有算术、位、逻辑运算符
- 变量、作用域、闭包
- 函数、递归、表达式体函数
- if/else、while、for、loop、switch、模式匹配
- 对象、数组、字符串（所有 19+23 个方法）
- 类型注解和运行时类型检查
- Try/catch/finally/throw
- Defer
- 模板字符串
- 空值合并（`??`、`?.`、`??=`）
- 命名参数
- 复合类型、类型别名
- `print()`、`eprint()`（通过 Emscripten 的控制台映射）
- `alloc()`/`free()`/`buffer()`（线性内存）
- `typeof()`、`len()`、`sizeof()`
- 数学内置函数（sin、cos、sqrt 等）
- 所有引用计数/内存管理

---

## 每个阶段的预估范围

| 阶段 | 范围 | 依赖 |
|------|------|------|
| **阶段 1** | ~800 行新 C 代码、~200 行 #ifdef 守卫、Makefile 更改 | Emscripten SDK |
| **阶段 2** | ~200 行 C 代码、stdlib 测试、Makefile | 阶段 1 |
| **阶段 3** | ~600 行 C 代码（桥接）、~200 行 Hemlock（stdlib） | 阶段 1 |
| **阶段 4** | ~1000 行 C 代码（Worker 线程）、复杂 | 阶段 1+3 |

推荐顺序：阶段 1 → 阶段 2 → 阶段 3 → 阶段 4

仅阶段 1 就能为计算工作负载提供有用的"浏览器中的 Hemlock"。阶段 2-4 逐步添加 I/O 和互操作。
