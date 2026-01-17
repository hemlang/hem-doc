# 組み込み関数リファレンス

Hemlockのすべての組み込み関数と定数の完全なリファレンスです。

---

## 概要

Hemlockは、I/O、型イントロスペクション、メモリ管理、並行処理、システムインタラクションのための組み込み関数セットを提供します。すべての組み込み関数はインポートなしでグローバルに利用可能です。

---

## I/O関数

### print

改行付きで値を標準出力に出力します。

**シグネチャ:**
```hemlock
print(...values): null
```

**パラメータ:**
- `...values` - 出力する任意の数の値

**戻り値:** `null`

**例:**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// 複数の値
print("x =", 10, "y =", 20);
```

**動作:**
- すべての値を文字列に変換
- 複数の値をスペースで区切る
- 末尾に改行を追加
- 標準出力をフラッシュ

---

### read_line

標準入力から1行のテキストを読み取ります（ユーザー入力）。

**シグネチャ:**
```hemlock
read_line(): string | null
```

**パラメータ:** なし

**戻り値:**
- `string` - 標準入力から読み取った行（改行は除去済み）
- `null` - EOF（ファイル/入力の終端）の場合

**例:**
```hemlock
// シンプルなプロンプト
print("What is your name?");
let name = read_line();
print("Hello, " + name + "!");

// 数値の読み取り（手動パースが必要）
print("Enter a number:");
let input = read_line();
let num = parse_int(input);  // parse_intについては以下を参照
print("Double:", num * 2);

// EOFの処理
let line = read_line();
if (line == null) {
    print("End of input");
}

// 複数行の読み取り
print("Enter lines (Ctrl+D to stop):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("You said:", line);
}
```

**動作:**
- ユーザーがEnterを押すまでブロック
- 末尾の改行（`\n`）とキャリッジリターン（`\r`）を除去
- EOF時に`null`を返す（Unixでは Ctrl+D、Windowsでは Ctrl+Z）
- 標準入力からのみ読み取り（ファイルからは読み取らない）

**ユーザー入力のパース:**

`read_line()`は常に文字列を返すため、数値入力は手動でパースする必要があります:

```hemlock
// シンプルな整数パーサー
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

// 使用例
print("Enter your age:");
let age = parse_int(read_line());
print("In 10 years you'll be", age + 10);
```

**関連項目:** ファイルからの読み取りについては[ファイルAPI](file-api.md)を参照

---

### eprint

改行付きで値を標準エラー出力に出力します。

**シグネチャ:**
```hemlock
eprint(value: any): null
```

**パラメータ:**
- `value` - 標準エラー出力に出力する単一の値

**戻り値:** `null`

**例:**
```hemlock
eprint("Error: file not found");
eprint(404);
eprint("Warning: " + message);

// 典型的なエラー処理パターン
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Error: config file not found: " + path);
        return null;
    }
    // ...
}
```

**動作:**
- 標準エラー出力（stderr）に出力
- 末尾に改行を追加
- 引数は1つのみ受け付け（`print`とは異なる）
- 通常の出力と混ざるべきでないエラーメッセージに有用

**printとの違い:**
- `print()` → stdout（通常出力、`>`でリダイレクト可能）
- `eprint()` → stderr（エラー出力、`2>`でリダイレクト可能）

```bash
# シェルの例: stdoutとstderrを分離
./hemlock script.hml > output.txt 2> errors.txt
```

---

## 型イントロスペクション

### typeof

値の型名を取得します。

**シグネチャ:**
```hemlock
typeof(value: any): string
```

**パラメータ:**
- `value` - 任意の値

**戻り値:** 型名を文字列として返す

**例:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// 型付きオブジェクト
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// その他の型
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**型名:**
- プリミティブ: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- 複合型: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- 特殊型: `"file"`, `"task"`, `"channel"`
- カスタム型: `define`で定義されたユーザー定義の型名

**関連項目:** [型システム](type-system.md)

---

## コマンド実行

### exec

シェルコマンドを実行し、出力をキャプチャします。

**シグネチャ:**
```hemlock
exec(command: string): object
```

**パラメータ:**
- `command` - 実行するシェルコマンド

**戻り値:** 以下のフィールドを持つオブジェクト:
- `output` (string) - コマンドのstdout
- `exit_code` (i32) - 終了ステータスコード（0 = 成功）

**例:**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// 終了ステータスのチェック
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found:", r.output);
} else {
    print("Pattern not found");
}

// 複数行の出力を処理
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**動作:**
- `/bin/sh`経由でコマンドを実行
- stdoutのみをキャプチャ（stderrはターミナルに出力）
- コマンドが完了するまでブロック
- 出力がない場合は空文字列を返す

**エラー処理:**
```hemlock
try {
    let r = exec("nonexistent_command");
} catch (e) {
    print("Failed to execute:", e);
}
```

**セキュリティ警告:** シェルインジェクションに脆弱です。ユーザー入力は常に検証/サニタイズしてください。

**制限事項:**
- stderrのキャプチャなし
- ストリーミングなし
- タイムアウトなし
- シグナル処理なし

---

### exec_argv

明示的な引数配列でコマンドを実行します（シェル解釈なし）。

**シグネチャ:**
```hemlock
exec_argv(argv: array): object
```

**パラメータ:**
- `argv` - 文字列の配列: `[command, arg1, arg2, ...]`

**戻り値:** 以下のフィールドを持つオブジェクト:
- `output` (string) - コマンドのstdout
- `exit_code` (i32) - 終了ステータスコード（0 = 成功）

**例:**
```hemlock
// シンプルなコマンド
let result = exec_argv(["ls", "-la"]);
print(result.output);

// スペースを含む引数のコマンド（安全！）
let r = exec_argv(["grep", "hello world", "file.txt"]);

// 引数付きでスクリプトを実行
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**execとの違い:**
```hemlock
// exec()はシェルを使用 - ユーザー入力では安全でない
exec("ls " + user_input);  // シェルインジェクションのリスク！

// exec_argv()はシェルをバイパス - 安全
exec_argv(["ls", user_input]);  // インジェクション不可能
```

**使用するタイミング:**
- 引数にスペース、引用符、特殊文字が含まれる場合
- ユーザー入力を処理する場合（セキュリティ）
- 予測可能な引数パースが必要な場合

**関連項目:** シンプルなシェルコマンドには`exec()`を使用

---

## エラー処理

### throw

例外をスローします。

**シグネチャ:**
```hemlock
throw expression
```

**パラメータ:**
- `expression` - スローする値（任意の型）

**戻り値:** 戻りません（制御を移譲）

**例:**
```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
```

**関連項目:** try/catch/finally文

---

### panic

エラーメッセージを出力してプログラムを即座に終了します（回復不能）。

**シグネチャ:**
```hemlock
panic(message?: any): never
```

**パラメータ:**
- `message`（省略可能） - 出力するエラーメッセージ

**戻り値:** 戻りません（プログラムが終了）

**例:**
```hemlock
panic();                          // デフォルト: "panic!"
panic("unreachable code reached");
panic(42);

// 一般的な使用例
fn process_state(state: i32): string {
    if (state == 1) { return "ready"; }
    if (state == 2) { return "running"; }
    panic("invalid state: " + typeof(state));
}
```

**動作:**
- stderrにエラーを出力: `panic: <message>`
- 終了コード1で終了
- try/catchで**キャッチ不可能**
- バグや回復不能なエラーに使用

**panicとthrowの違い:**
- `panic()` - 回復不能なエラー、即座に終了
- `throw` - 回復可能なエラー、キャッチ可能

---

### assert

条件が真であることをアサートするか、エラーメッセージで終了します。

**シグネチャ:**
```hemlock
assert(condition: any, message?: string): null
```

**パラメータ:**
- `condition` - 真偽をチェックする値
- `message`（省略可能） - アサーション失敗時のカスタムエラーメッセージ

**戻り値:** `null`（アサーションが成功した場合）

**例:**
```hemlock
// 基本的なアサーション
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "Array must not be empty");

// カスタムメッセージ付き
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Division by zero");
    return a / b;
}

// 関数引数の検証
fn process_data(data: array) {
    assert(data != null, "data cannot be null");
    assert(data.length > 0, "data cannot be empty");
    // ...
}
```

**動作:**
- 条件が真の場合: `null`を返し、実行を継続
- 条件が偽の場合: エラーを出力し、終了コード1で終了
- 偽の値: `false`, `0`, `0.0`, `null`, `""`（空文字列）
- 真の値: それ以外すべて

**失敗時の出力:**
```
Assertion failed: Array must not be empty
```

**使用するタイミング:**
- 関数の事前条件の検証
- 開発中の不変条件のチェック
- プログラマーエラーの早期検出

**assertとpanicの違い:**
- `assert(cond, msg)` - 条件をチェックし、偽の場合に失敗
- `panic(msg)` - 無条件で常に失敗

---

## シグナル処理

### signal

シグナルハンドラを登録またはリセットします。

**シグネチャ:**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**パラメータ:**
- `signum` - シグナル番号（`SIGINT`などの定数を使用）
- `handler` - シグナル受信時に呼び出す関数、またはデフォルトにリセットする場合は`null`

**戻り値:** 以前のハンドラ関数、または`null`

**例:**
```hemlock
fn handle_interrupt(sig) {
    print("Caught SIGINT!");
}

signal(SIGINT, handle_interrupt);

// デフォルトにリセット
signal(SIGINT, null);
```

**ハンドラのシグネチャ:**
```hemlock
fn handler(signum: i32) {
    // signumにはシグナル番号が含まれる
}
```

**関連項目:**
- [シグナル定数](#シグナル定数)
- `raise()`

---

### raise

現在のプロセスにシグナルを送信します。

**シグネチャ:**
```hemlock
raise(signum: i32): null
```

**パラメータ:**
- `signum` - 発生させるシグナル番号

**戻り値:** `null`

**例:**
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

## グローバル変数

### args

コマンドライン引数の配列です。

**型:** 文字列の`array`

**構造:**
- `args[0]` - スクリプトのファイル名
- `args[1..n]` - コマンドライン引数

**例:**
```bash
# コマンド: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// 引数を反復処理
let i = 1;
while (i < args.length) {
    print("Argument", i, ":", args[i]);
    i = i + 1;
}
```

**REPLでの動作:** REPLでは、`args.length`は0（空の配列）

---

## シグナル定数

標準POSIXシグナル定数（i32値）:

### 割り込みと終了

| 定数       | 値    | 説明                                   |
|------------|-------|----------------------------------------|
| `SIGINT`   | 2     | キーボードからの割り込み（Ctrl+C）     |
| `SIGTERM`  | 15    | 終了要求                               |
| `SIGQUIT`  | 3     | キーボードからの終了（Ctrl+\）         |
| `SIGHUP`   | 1     | 制御端末でのハングアップ検出           |
| `SIGABRT`  | 6     | 中止シグナル                           |

### ユーザー定義

| 定数       | 値    | 説明                       |
|------------|-------|----------------------------|
| `SIGUSR1`  | 10    | ユーザー定義シグナル1      |
| `SIGUSR2`  | 12    | ユーザー定義シグナル2      |

### プロセス制御

| 定数       | 値    | 説明                            |
|------------|-------|---------------------------------|
| `SIGALRM`  | 14    | アラームクロックタイマー        |
| `SIGCHLD`  | 17    | 子プロセスのステータス変更      |
| `SIGCONT`  | 18    | 停止中の場合は続行              |
| `SIGSTOP`  | 19    | プロセス停止（キャッチ不可）    |
| `SIGTSTP`  | 20    | 端末停止（Ctrl+Z）              |

### I/O

| 定数       | 値    | 説明                               |
|------------|-------|------------------------------------|
| `SIGPIPE`  | 13    | 壊れたパイプ                       |
| `SIGTTIN`  | 21    | バックグラウンドでの端末読み取り   |
| `SIGTTOU`  | 22    | バックグラウンドでの端末書き込み   |

**例:**
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

**注意:** `SIGKILL`（9）と`SIGSTOP`（19）はキャッチまたは無視できません。

---

## 数学/算術関数

### div

浮動小数点数を返す床除算です。

**シグネチャ:**
```hemlock
div(a: number, b: number): f64
```

**パラメータ:**
- `a` - 被除数
- `b` - 除数

**戻り値:** `a / b`の床を浮動小数点数（f64）として返す

**例:**
```hemlock
let result = div(7, 2);    // 3.0（3.5ではない）
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0（床は負の無限大方向に丸める）
```

**注意:** Hemlockでは、`/`演算子は常に浮動小数点数を返します。整数部分を浮動小数点数として必要な場合は`div()`を、整数結果が必要な場合は`divi()`を使用してください。

---

### divi

整数を返す床除算です。

**シグネチャ:**
```hemlock
divi(a: number, b: number): i64
```

**パラメータ:**
- `a` - 被除数
- `b` - 除数

**戻り値:** `a / b`の床を整数（i64）として返す

**例:**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4（床は負の無限大方向に丸める）
```

**比較:**
```hemlock
print(7 / 2);      // 3.5（通常の除算、常に浮動小数点数）
print(div(7, 2));  // 3.0（床除算、浮動小数点数結果）
print(divi(7, 2)); // 3  （床除算、整数結果）
```

---

## メモリ管理関数

完全なリファレンスについては[メモリAPI](memory-api.md)を参照:
- `alloc(size)` - 生メモリを確保
- `free(ptr)` - メモリを解放
- `buffer(size)` - 安全なバッファを確保
- `memset(ptr, byte, size)` - メモリを埋める
- `memcpy(dest, src, size)` - メモリをコピー
- `realloc(ptr, new_size)` - 確保サイズを変更

### sizeof

型のバイト単位のサイズを取得します。

**シグネチャ:**
```hemlock
sizeof(type): i32
```

**パラメータ:**
- `type` - 型定数（`i32`, `f64`, `ptr`など）または型名の文字列

**戻り値:** バイト単位のサイズを`i32`として返す

**例:**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// 型エイリアスの使用
print(sizeof(byte));     // 1（u8と同じ）
print(sizeof(integer));  // 4（i32と同じ）
print(sizeof(number));   // 8（f64と同じ）

// 文字列形式でも動作
print(sizeof("i32"));    // 4
```

**サポートされる型:**
| 型 | サイズ | エイリアス |
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

**関連項目:** 型付き確保には`talloc()`を使用

---

### talloc

型付き配列用のメモリを確保します（型認識確保）。

**シグネチャ:**
```hemlock
talloc(type, count: i32): ptr
```

**パラメータ:**
- `type` - 型定数（`i32`, `f64`, `ptr`など）
- `count` - 確保する要素数

**戻り値:** 確保されたメモリへの`ptr`、失敗時は`null`

**例:**
```hemlock
// 10個のi32の配列を確保（40バイト）
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// 5個のf64の配列を確保（40バイト）
let float_arr = talloc(f64, 5);

// 100バイトの配列を確保
let byte_arr = talloc(u8, 100);

// 解放を忘れずに！
free(int_arr);
free(float_arr);
free(byte_arr);
```

**allocとの比較:**
```hemlock
// これらは同等:
let p1 = talloc(i32, 10);      // 型認識: 10個のi32
let p2 = alloc(sizeof(i32) * 10);  // 手動計算

// tallocの方が明確でエラーが起きにくい
```

**エラー処理:**
- 確保に失敗した場合は`null`を返す
- countが正でない場合はエラーで終了
- サイズオーバーフロー（count * element_size）をチェック

**関連項目:** `alloc()`, `sizeof()`, `free()`

---

## FFIポインタヘルパー

これらの関数は、生メモリへの型付き値の読み書きを支援し、FFIや低レベルメモリ操作に有用です。

### ptr_null

ヌルポインタを作成します。

**シグネチャ:**
```hemlock
ptr_null(): ptr
```

**戻り値:** ヌルポインタ

**例:**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Pointer is null");
}
```

---

### ptr_offset

ポインタオフセットを計算します（ポインタ演算）。

**シグネチャ:**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**パラメータ:**
- `ptr` - ベースポインタ
- `index` - 要素インデックス
- `element_size` - 各要素のバイト単位のサイズ

**戻り値:** 指定されたインデックスの要素へのポインタ

**例:**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### ポインタ読み取り関数

メモリから型付き値を読み取ります。

| 関数 | シグネチャ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `ptr_read_i8` | `(ptr)` | `i8` | 符号付き8ビット整数を読み取り |
| `ptr_read_i16` | `(ptr)` | `i16` | 符号付き16ビット整数を読み取り |
| `ptr_read_i32` | `(ptr)` | `i32` | 符号付き32ビット整数を読み取り |
| `ptr_read_i64` | `(ptr)` | `i64` | 符号付き64ビット整数を読み取り |
| `ptr_read_u8` | `(ptr)` | `u8` | 符号なし8ビット整数を読み取り |
| `ptr_read_u16` | `(ptr)` | `u16` | 符号なし16ビット整数を読み取り |
| `ptr_read_u32` | `(ptr)` | `u32` | 符号なし32ビット整数を読み取り |
| `ptr_read_u64` | `(ptr)` | `u64` | 符号なし64ビット整数を読み取り |
| `ptr_read_f32` | `(ptr)` | `f32` | 32ビット浮動小数点数を読み取り |
| `ptr_read_f64` | `(ptr)` | `f64` | 64ビット浮動小数点数を読み取り |
| `ptr_read_ptr` | `(ptr)` | `ptr` | ポインタ値を読み取り |

**例:**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### ポインタ書き込み関数

メモリに型付き値を書き込みます。

| 関数 | シグネチャ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | 符号付き8ビット整数を書き込み |
| `ptr_write_i16` | `(ptr, value)` | `null` | 符号付き16ビット整数を書き込み |
| `ptr_write_i32` | `(ptr, value)` | `null` | 符号付き32ビット整数を書き込み |
| `ptr_write_i64` | `(ptr, value)` | `null` | 符号付き64ビット整数を書き込み |
| `ptr_write_u8` | `(ptr, value)` | `null` | 符号なし8ビット整数を書き込み |
| `ptr_write_u16` | `(ptr, value)` | `null` | 符号なし16ビット整数を書き込み |
| `ptr_write_u32` | `(ptr, value)` | `null` | 符号なし32ビット整数を書き込み |
| `ptr_write_u64` | `(ptr, value)` | `null` | 符号なし64ビット整数を書き込み |
| `ptr_write_f32` | `(ptr, value)` | `null` | 32ビット浮動小数点数を書き込み |
| `ptr_write_f64` | `(ptr, value)` | `null` | 64ビット浮動小数点数を書き込み |
| `ptr_write_ptr` | `(ptr, value)` | `null` | ポインタ値を書き込み |

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### バッファ/ポインタ変換

#### buffer_ptr

バッファから生ポインタを取得します。

**シグネチャ:**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**例:**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// pはbufと同じメモリを指す
```

#### ptr_to_buffer

生ポインタの周りにバッファラッパーを作成します。

**シグネチャ:**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**例:**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // 境界チェック付きになる
// 注意: bufを解放すると基底のメモリも解放される
```

---

## ファイルI/O関数

完全なリファレンスについては[ファイルAPI](file-api.md)を参照:
- `open(path, mode?)` - ファイルを開く

---

## 並行処理関数

完全なリファレンスについては[並行処理API](concurrency-api.md)を参照:
- `spawn(fn, args...)` - タスクを生成
- `join(task)` - タスクを待機
- `detach(task)` - タスクを切り離す
- `channel(capacity)` - チャネルを作成

### apply

引数の配列で関数を動的に呼び出します。

**シグネチャ:**
```hemlock
apply(fn: function, args: array): any
```

**パラメータ:**
- `fn` - 呼び出す関数
- `args` - 関数に渡す引数の配列

**戻り値:** 呼び出された関数の戻り値

**例:**
```hemlock
fn add(a, b) {
    return a + b;
}

// 引数の配列で呼び出し
let result = apply(add, [2, 3]);
print(result);  // 5

// 動的ディスパッチ
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

// 可変引数
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

**ユースケース:**
- 実行時の値に基づく動的関数ディスパッチ
- 可変引数リストでの関数呼び出し
- 高階ユーティリティ（map、filterなど）の実装
- プラグイン/拡張システム

---

### select

複数のチャネルからのデータを待機し、いずれかがデータを持ったときに戻ります。

**シグネチャ:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**パラメータ:**
- `channels` - チャネル値の配列
- `timeout_ms`（省略可能） - ミリ秒単位のタイムアウト（-1または省略で無限）

**戻り値:**
- `{ channel, value }` - データを持つチャネルと受信した値を含むオブジェクト
- `null` - タイムアウト時

**例:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// プロデューサータスク
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// 最初のメッセージを待機
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"（最初に到着）

// タイムアウト付き
let result2 = select([ch1, ch2], 1000);  // 最大1秒待機
if (result2 == null) {
    print("Timeout - no data received");
} else {
    print("Received:", result2.value);
}

// 継続的なselectループ
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("No activity for 5 seconds");
        break;
    }
    print("Got message:", msg.value);
}
```

**動作:**
- チャネルがデータを持つかタイムアウトになるまでブロック
- チャネルが既にデータを持っている場合は即座に戻る
- チャネルが閉じられて空の場合、`{ channel, value: null }`を返す
- チャネルを順番にポーリング（最初に準備完了したチャネルが勝つ）

**ユースケース:**
- 複数のプロデューサーの多重化
- チャネル操作でのタイムアウトの実装
- 複数のソースを持つイベントループの構築

---

## まとめ表

### 関数

| 関数       | カテゴリ        | 戻り値       | 説明                            |
|------------|-----------------|--------------|----------------------------------|
| `print`    | I/O             | `null`       | 標準出力に出力                   |
| `read_line`| I/O             | `string?`    | 標準入力から行を読み取り         |
| `eprint`   | I/O             | `null`       | 標準エラー出力に出力             |
| `typeof`   | 型              | `string`     | 型名を取得                       |
| `exec`     | コマンド        | `object`     | シェルコマンドを実行             |
| `exec_argv`| コマンド        | `object`     | 引数配列で実行                   |
| `assert`   | エラー          | `null`       | 条件をアサートまたは終了         |
| `panic`    | エラー          | `never`      | 回復不能エラー（終了）           |
| `signal`   | シグナル        | `function?`  | シグナルハンドラを登録           |
| `raise`    | シグナル        | `null`       | プロセスにシグナルを送信         |
| `alloc`    | メモリ          | `ptr`        | 生メモリを確保                   |
| `talloc`   | メモリ          | `ptr`        | 型付き確保                       |
| `sizeof`   | メモリ          | `i32`        | 型サイズをバイトで取得           |
| `free`     | メモリ          | `null`       | メモリを解放                     |
| `buffer`   | メモリ          | `buffer`     | 安全なバッファを確保             |
| `memset`   | メモリ          | `null`       | メモリを埋める                   |
| `memcpy`   | メモリ          | `null`       | メモリをコピー                   |
| `realloc`  | メモリ          | `ptr`        | 確保サイズを変更                 |
| `open`     | ファイルI/O     | `file`       | ファイルを開く                   |
| `spawn`    | 並行処理        | `task`       | 並行タスクを生成                 |
| `join`     | 並行処理        | `any`        | タスク結果を待機                 |
| `detach`   | 並行処理        | `null`       | タスクを切り離す                 |
| `channel`  | 並行処理        | `channel`    | 通信チャネルを作成               |
| `select`   | 並行処理        | `object?`    | 複数チャネルで待機               |
| `apply`    | 関数            | `any`        | 引数配列で関数を呼び出し         |

### グローバル変数

| 変数       | 型       | 説明                              |
|------------|----------|-----------------------------------|
| `args`     | `array`  | コマンドライン引数                |

### 定数

| 定数       | 型    | カテゴリ | 値    | 説明                      |
|------------|-------|----------|-------|---------------------------|
| `SIGINT`   | `i32` | シグナル | 2     | キーボード割り込み        |
| `SIGTERM`  | `i32` | シグナル | 15    | 終了要求                  |
| `SIGQUIT`  | `i32` | シグナル | 3     | キーボード終了            |
| `SIGHUP`   | `i32` | シグナル | 1     | ハングアップ              |
| `SIGABRT`  | `i32` | シグナル | 6     | 中止                      |
| `SIGUSR1`  | `i32` | シグナル | 10    | ユーザー定義1             |
| `SIGUSR2`  | `i32` | シグナル | 12    | ユーザー定義2             |
| `SIGALRM`  | `i32` | シグナル | 14    | アラームタイマー          |
| `SIGCHLD`  | `i32` | シグナル | 17    | 子ステータス変更          |
| `SIGCONT`  | `i32` | シグナル | 18    | 続行                      |
| `SIGSTOP`  | `i32` | シグナル | 19    | 停止（キャッチ不可）      |
| `SIGTSTP`  | `i32` | シグナル | 20    | 端末停止                  |
| `SIGPIPE`  | `i32` | シグナル | 13    | 壊れたパイプ              |
| `SIGTTIN`  | `i32` | シグナル | 21    | バックグラウンド端末読取  |
| `SIGTTOU`  | `i32` | シグナル | 22    | バックグラウンド端末書込  |

---

## 関連項目

- [型システム](type-system.md) - 型と変換
- [メモリAPI](memory-api.md) - メモリ確保関数
- [ファイルAPI](file-api.md) - ファイルI/O関数
- [並行処理API](concurrency-api.md) - 非同期/並行処理関数
- [文字列API](string-api.md) - 文字列メソッド
- [配列API](array-api.md) - 配列メソッド
