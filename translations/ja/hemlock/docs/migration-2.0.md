# 移行ガイド：v1.xからv2.0.0へ

## 破壊的変更：組み込み関数がStdlibに移動

Hemlock 2.0.0は名前空間汚染を削減するため、63個のグローバル組み込み関数を`@stdlib`モジュールに移動しました。これらの関数をインポートなしで使用しているコードは「未定義変数」エラーが発生します。

## クイックフィックス

各関数に適切な`import`文を追加してください。以下のテーブルは各組み込み関数の移動先を示しています。

### 数学関数

```hemlock
// 以前 (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// 以後 (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**移動した関数：** `sin`、`cos`、`tan`、`asin`、`acos`、`atan`、`atan2`、`sinh`、`cosh`、`tanh`、`sqrt`、`cbrt`、`exp`、`log`、`log2`、`log10`、`floor`、`ceil`、`round`、`trunc`、`abs`、`pow`、`fmod`、`min`、`max`、`rand`、`div`、`divi`、`floori`、`ceili`、`roundi`、`trunci`

### シグナルハンドリング

```hemlock
// 以前
signal(SIGINT, handler);

// 以後
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### ファイルシステム

```hemlock
// 以前
let f = open("file.txt", "r");

// 以後
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### プロセス / 環境

```hemlock
// 以前
let home = getenv("HOME");
exec("ls");

// 以後
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### ネットワーキング

```hemlock
// 以前
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// 以後
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### アトミック操作

```hemlock
// 以前
atomic_store(ptr, 42);

// 以後
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### FFIコールバック

```hemlock
// 以前
let cb = callback(my_func);

// 以後
import { callback, callback_free } from "@stdlib/ffi";
```

### デバッグ / スタック

```hemlock
// 以前
let info = task_debug_info(task);

// 以後
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## 完全なモジュールマッピング

| 関数 | 新しいモジュール |
|-------------|-----------|
| 数学関数 (sin, cos, sqrt, etc.) | `@stdlib/math` |
| `signal`、`raise`、SIG*定数 | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`、`exec_argv` | `@stdlib/process` |
| `getenv`、`setenv` | `@stdlib/env` |
| AF_*、SOCK_*、POLL*定数、`socket_create`、`dns_resolve`、`poll` | `@stdlib/net` |
| `atomic_*`操作 | `@stdlib/atomic` |
| `callback`、`callback_free`、`ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`、`set_stack_limit`、`get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`、`set_default_stack_size` | `@stdlib/async` |

## その他の破壊的変更なし

その他のすべての言語機能、構文、APIは後方互換性を維持しています。既存のコードにはインポートの追加のみが必要です。
