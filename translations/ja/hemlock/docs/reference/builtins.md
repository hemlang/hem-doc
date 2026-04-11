# 組み込み関数リファレンス

Hemlock v2.0.0のすべての組み込み関数と定数の完全なリファレンスです。

> **v2.0.0 破壊的変更：** 63個の組み込み関数がグローバル名前空間から`@stdlib`モジュールに移動しました。
> `sin()`、`open()`、`exec()`、`signal()`などの関数や`SIGINT`、`AF_INET`などの定数はインポートが必要になりました。
> 完全なリストは[Stdlibに移動した関数](#stdlibモジュールに移動)を参照してください。

---

## グローバル組み込み関数（インポート不要）

これらは`import`文なしでどこでも利用可能です。

### I/O

| 関数 | 説明 |
|----------|-------------|
| `print(value, ...)` | 改行付きでstdoutに値を出力 |
| `write(value)` | 改行なしでstdoutに値を出力（即座にフラッシュ） |
| `eprint(value, ...)` | 改行付きでstderrに値を出力 |
| `read_line()` | stdinから行を読み取り、`string`またはEOFで`null`を返す |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline (\nなし)
eprint("error!");           // -> stderr
let name = read_line();     // 入力まで待機
```

### メモリ管理

| 関数 | 説明 |
|----------|-------------|
| `alloc(size)` | `size`バイトの生メモリを割り当て、`ptr`を返す |
| `talloc(type, count)` | 型対応の割り当て：`talloc(i32, 10)`は10個のi32を割り当て |
| `realloc(ptr, new_size)` | 以前割り当てたメモリのサイズを変更 |
| `free(ptr)` | 割り当てたメモリを解放 |
| `memset(ptr, value, size)` | `size`バイトを`value`に設定 |
| `memcpy(dest, src, size)` | `src`から`dest`に`size`バイトをコピー |
| `buffer(size)` | `size`バイトの境界チェック付きバッファを作成 |

```hemlock
let p = alloc(64);       // 生ポインタ、境界チェックなし
let b = buffer(64);      // 安全なバッファ、境界チェック付き
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // 手動クリーンアップ
```

### 型システム

| 関数 | 説明 |
|----------|-------------|
| `typeof(value)` | 型名を文字列で返す（`"i32"`、`"string"`など） |
| `typeid(value)` | 型を整数定数で返す（`typeof()`より高速） |
| `sizeof(type)` | 型のバイトサイズを返す（`sizeof(i32)` → 4） |

**型コンストラクタ**（変換と型付き割り当てに使用）：

`i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`rune`、`ptr`

**型エイリアス：** `integer` (i32)、`number` (f64)、`byte` (u8)

**TYPEID定数**（`typeid()`と共に使用）：

| 定数 | 値 | 定数 | 値 |
|----------|-------|----------|-------|
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
let n = i32("42");  // 文字列をi32にパース

// typeid()は整数を返す - typeof()の文字列比較より高速
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
```

### 制御フロー

| 関数 | 説明 |
|----------|-------------|
| `assert(condition, message?)` | 条件がfalseの場合パニック |
| `panic(message)` | 即座に回復不能な終了（try/catchで捕捉不可） |

```hemlock
assert(x > 0, "x must be positive");
panic("unrecoverable error");
```

### 並行処理

| 関数 | 説明 |
|----------|-------------|
| `spawn(fn, args...)` | 非同期タスクをスポーン、タスクハンドルを返す |
| `spawn_with(options, fn, args...)` | スレッドごとの設定付きでスポーン（`stack_size`バイト、`name`文字列最大16文字） |
| `join(task)` | タスク完了を待ち、結果を返す |
| `detach(task)` | タスクを独立して実行させる（ファイア・アンド・フォーゲット） |
| `channel(capacity?)` | 通信チャネルを作成（0 = アンバッファード） |
| `select(channels)` | 複数チャネルで待機 |
| `apply(fn, args_array)` | 引数の配列で関数を呼び出し |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### ポインタ / FFIヘルパー

`alloc`/`free`と共に使用される低レベルプリミティブのためグローバルです。

| 関数 | 説明 |
|----------|-------------|
| `ptr_offset(ptr, bytes)` | ポインタをバイト数だけオフセット |
| `ptr_null()` | nullポインタを取得 |
| `ptr_to_buffer(ptr, size)` | ポインタを境界チェック付きバッファにラップ |
| `buffer_ptr(buffer)` | バッファから生ポインタを取得 |

**すべての数値型と`ptr`に対するポインタ読み書き/deref：**

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

すべての`ptr_read_*`、`ptr_write_*`、`ptr_deref_*`関数は`ptr`型と`buffer`型の両方を直接受け付けます：

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
free(p);

// バッファでも直接動作（buffer_ptr()不要）
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Stdlibモジュールに移動

これらの組み込み関数はv2.0.0で移動され、インポートが必要になりました。

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**関数：** `sin`、`cos`、`tan`、`asin`、`acos`、`atan`、`atan2`、`sqrt`、`pow`、`exp`、`log`、`log10`、`log2`、`floor`、`ceil`、`round`、`trunc`、`floori`、`ceili`、`roundi`、`trunci`、`div`、`divi`、`abs`、`min`、`max`、`clamp`、`rand`、`rand_range`、`seed`

**定数：** `PI`、`E`、`TAU`、`INF`、`NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**関数：** `getenv`、`setenv`、`unsetenv`、`get_pid`、`exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**関数：** `signal`、`raise`

**定数：** `SIGINT`、`SIGTERM`、`SIGHUP`、`SIGQUIT`、`SIGABRT`、`SIGUSR1`、`SIGUSR2`、`SIGALRM`、`SIGCHLD`、`SIGPIPE`、`SIGCONT`、`SIGSTOP`、`SIGTSTP`、`SIGTTIN`、`SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**関数：** `socket_create`、`dns_resolve`、`poll`

**定数：** `AF_INET`、`AF_INET6`、`SOCK_STREAM`、`SOCK_DGRAM`、`IPPROTO_TCP`、`IPPROTO_UDP`、`SOL_SOCKET`、`SO_REUSEADDR`、`SO_KEEPALIVE`、`SO_RCVTIMEO`、`SO_SNDTIMEO`、`POLLIN`、`POLLOUT`、`POLLERR`、`POLLHUP`、`POLLNVAL`、`POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**関数：** `exec`、`exec_argv`、`fork`、`wait`、`waitpid`、`kill`、`abort`、`exit`、`get_pid`、`getppid`、`getuid`、`geteuid`、`getgid`、`getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**関数：** `open`、`read_file`、`write_file`、`append_file`、`remove_file`、`rename`、`copy_file`、`is_file`、`is_dir`、`file_stat`、`make_dir`、`remove_dir`、`list_dir`、`cwd`、`chdir`、`absolute_path`、`exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**関数：** `now`、`time_ms`、`sleep`、`clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**関数 (i32)：** `atomic_load_i32`、`atomic_store_i32`、`atomic_add_i32`、`atomic_sub_i32`、`atomic_and_i32`、`atomic_or_i32`、`atomic_xor_i32`、`atomic_cas_i32`、`atomic_exchange_i32`

**関数 (i64)：** `atomic_load_i64`、`atomic_store_i64`、`atomic_add_i64`、`atomic_sub_i64`、`atomic_and_i64`、`atomic_or_i64`、`atomic_xor_i64`、`atomic_cas_i64`、`atomic_exchange_i64`

**関数：** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**関数：** `task_debug_info`、`set_stack_limit`、`get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**関数：** `callback`、`callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**関数：** `string_concat_many`

---

## 移行ガイド（v1.x → v2.0.0）

### 以前 (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### 以後 (v2.0.0)
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

関数呼び出し自体は同一です -- インポートのみが変わります。
