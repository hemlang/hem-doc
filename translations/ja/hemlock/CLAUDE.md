# Hemlock言語設計思想

> 「安全でないことを安全に記述するための、小さく安全でない言語」

このドキュメントは、Hemlockを使用するAIアシスタント向けのコア設計原則を記載しています。
詳細なドキュメントについては、`docs/README.md` と `stdlib/docs/` ディレクトリを参照してください。

---

## コアアイデンティティ

Hemlockは**システムスクリプト言語**であり、手動メモリ管理と明示的な制御を備えています：
- モダンなスクリプト言語の使いやすさを持つCのパワー
- 構造化された非同期並行処理が組み込み
- 隠れた動作やマジックがない

**Hemlockではないもの：** メモリセーフ、GC言語、複雑さを隠すもの
**Hemlockであるもの：** 暗黙より明示、教育的、システム作業のための「Cスクリプト層」

---

## 設計原則

### 1. 暗黙より明示
- セミコロン必須（ASIなし）
- 手動メモリ管理（alloc/free）
- 型注釈はオプションだが実行時にチェック

### 2. デフォルトで動的、選択で型付け
- すべての値は実行時型タグを持つ
- リテラルは型を推論：`42` → i32、`5000000000` → i64、`3.14` → f64
- オプションの型注釈は実行時チェックを強制

### 3. アンセーフは機能
- ポインタ演算が許可（ユーザーの責任）
- 生の`ptr`には境界チェックなし（安全のために`buffer`を使用）
- 二重解放によるクラッシュを許可

### 4. 構造化された並行処理がファーストクラス
- pthreadベースの並列処理を持つ`async`/`await`組み込み
- 通信用チャネル
- タスク管理用の`spawn`/`join`/`detach`

### 5. Cライクな構文
- `{}`ブロックは常に必須
- コメント：`// 行` と `/* ブロック */`
- 演算子はCと同じ：`+`、`-`、`*`、`%`、`&&`、`||`、`!`、`&`、`|`、`^`、`<<`、`>>`
- インクリメント/デクリメント：`++x`、`x++`、`--x`、`x--`（前置と後置）
- 複合代入：`+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`
- `/`は常にfloatを返す（整数除算には`@stdlib/math`の`divi()`を使用）
- 型構文：`let x: type = value;`

---

## クイックリファレンス

### 型
```
符号付き：   i8, i16, i32, i64
符号なし：   u8, u16, u32, u64
浮動小数点： f32, f64
その他：     bool, string, rune, array, ptr, buffer, null, object, file, task, channel
エイリアス： integer (i32), number (f64), byte (u8)
```

**型昇格：** i8 → u8 → i16 → u16 → i32 → u32 → i64 → u64 → f32 → f64（floatが常に優先、ただしi64/u64 + f32 → f64で精度を保持）

### リテラル
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64（> i32 最大値）
let hex = 0xDEADBEEF;    // 16進リテラル
let bin = 0b1010;        // 2進リテラル
let oct = 0o777;         // 8進リテラル
let sep = 1_000_000;     // 数値セパレータ使用可能
let pi = 3.14;           // f64
let half = .5;           // f64（先頭ゼロなし）
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // 16進とUnicodeエスケープ
let ch = 'A';            // rune
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### 型変換
```hemlock
let n = i32("42");       // 文字列をi32にパース
let f = f64("3.14");     // 文字列をf64にパース
let big = i64(42);       // i32からi64へ
let truncated = i32(3.99); // f64からi32へ（3に切り捨て）
let f: f64 = 100;        // 注釈によるi32からf64へ（数値変換OK）
// let n: i32 = "42";    // エラー - 文字列パースにはi32("42")を使用
```

### イントロスペクション
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
"hello".length;          // 5（rune数）
"hello".byte_length;     // 5（バイト数）

// typeid() - 高速な整数ベースの型検出（文字列割り当てなし）
typeid(42);              // 2 (TYPEID_I32)
if (typeid(val) == TYPEID_I32 || typeid(val) == TYPEID_I64) { ... }
```

**TYPEID定数：** `TYPEID_I8` (0)、`TYPEID_I16` (1)、`TYPEID_I32` (2)、`TYPEID_I64` (3)、`TYPEID_U8` (4)、`TYPEID_U16` (5)、`TYPEID_U32` (6)、`TYPEID_U64` (7)、`TYPEID_F32` (8)、`TYPEID_F64` (9)、`TYPEID_BOOL` (10)、`TYPEID_STRING` (11)、`TYPEID_RUNE` (12)、`TYPEID_PTR` (13)、`TYPEID_BUFFER` (14)、`TYPEID_ARRAY` (15)、`TYPEID_OBJECT` (16)、`TYPEID_FILE` (17)、`TYPEID_FUNCTION` (18)、`TYPEID_TASK` (19)、`TYPEID_CHANNEL` (20)、`TYPEID_NULL` (21)

### メモリ
```hemlock
let p = alloc(64);       // 生ポインタ
let b = buffer(64);      // 安全なバッファ（境界チェック付き）
memset(p, 0, 64); memcpy(dest, src, 64);
free(p);                 // 手動クリーンアップ必須
let view = b.slice(0, 16);  // ゼロコピーバッファビュー
ptr_write_f32(b, 3.14);     // ptr_read/writeはbufferを直接受け付け
```

### 制御フロー
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // 無限ループ
switch (x) { case 1: break; default: break; }  // Cスタイルのフォールスルー
defer cleanup();         // 関数が戻るときに実行

// ネストされたloop でのループラベル
outer: while (cond) {
    for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }
    }
}
```

### パターンマッチング
```hemlock
let result = match (value) {
    0 => "zero",
    1 | 2 | 3 => "small",           // ORパターン
    n if n < 10 => "medium",        // ガード
    n => "large: " + n              // 変数バインディング
};

// 型パターン (n: i32)、オブジェクト/配列分解、
// ネストされたパターン、ワイルドカード (_) もサポート。
```

### Null合体
```hemlock
let name = user.name ?? "Anonymous";     // null合体
config ??= { timeout: 30 };             // null合体代入
let city = user?.address?.city;          // 安全なナビゲーション
```

### 関数
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // 匿名/クロージャ
fn double(x: i32): i32 => x * 2;  // 式本体

// パラメータ修飾子
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // 参照渡し
fn print_all(const items: array) { for (i in items) { print(i); } }  // 不変

// 名前付き引数
create_user(name: "Bob", age: 30);
create_user("David", active: false);  // 位置引数の後に名前付き
```

### オブジェクト、列挙型 & 型
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let person = { name, age };             // ショートハンド構文
let config = { ...defaults, size: "large" }; // スプレッド演算子

// ブラケット記法とキー強制変換（非文字列キーは自動的に文字列に変換）
let map = {};
map[42] = "value";              // 整数キー → "42"
map[true] = "yes";              // boolキー → "true"
map['A'] = "alpha";             // runeキー → "A"
print(map[42]);                 // "value"
print(map.has(42));             // true
map.delete(42);                 // フィールド"42"を削除
let keys = map.keys();          // 文字列キーの配列を返す

enum Color { RED, GREEN, BLUE }

// 複合型（交差型/ダック型）
let p: HasName & HasAge = { name: "Alice", age: 30 };

// 型エイリアス
type Callback = fn(i32): void;
type Person = HasName & HasAge;

// defineでのメソッドシグネチャ
define Comparable { value: i32, fn compare(other: Self): i32 }
```

### エラーハンドリング
```hemlock
try { throw "error"; } catch (e) { print(e); } finally { cleanup(); }
panic("unrecoverable");  // 即座に終了、catchできない
```

### 非同期/並行処理
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // またはjoin(task)
detach(spawn(background_work));
let t = spawn_with({ stack_size: 4194304, name: "worker" }, compute, 42);

let ch = channel(10);
ch.send(value); let val = ch.recv(); ch.close();
```

**メモリ所有権：** タスクはポインタを共有しますがプリミティブはコピーします。`ptr`を共有する場合は`free()`の前に`join()`を使用してください。

### I/O
```hemlock
let name = read_line();          // stdin（EOFでnullを返す）
print("hello"); write("改行なし"); eprint("stderr");
let f = open("file.txt", "r");  // モード: r, w, a, r+, w+, a+
f.read(); f.write("data"); f.close();
```

---

## 文字列メソッド（22個）

`substr`、`slice`、`find`、`contains`、`split`、`trim`、`trim_start`、`trim_end`、
`to_upper`、`to_lower`、`starts_with`、`ends_with`、`replace`、`replace_all`、
`repeat`、`char_at`、`byte_at`、`chars`、`bytes`、`to_bytes`、`byte_ptr`、`deserialize`

テンプレート文字列：`` `Hello ${name}!` ``

**文字列の可変性：** 文字列はインデックス代入（`s[0] = 'H'`）で変更可能ですが、すべての文字列メソッドは新しい文字列を返します。

## 配列メソッド（28個）

`push`、`pop`、`shift`、`unshift`、`insert`、`remove`、`find`、`findIndex`、`contains`、
`slice`、`join`、`concat`、`reverse`、`first`、`last`、`clear`、`map`、`filter`、`reduce`、
`every`、`some`、`indexOf`、`lastIndexOf`、`sort`、`fill`、`reserve`、`flat`、`serialize`

型付き配列：`let nums: array<i32> = [1, 2, 3];`

---

## 標準ライブラリ（53モジュール）

`@stdlib/`プレフィックスでインポート：`import { sin, cos, PI } from "@stdlib/math";`

| モジュール | 説明 |
|--------|-------------|
| `arena` | アリーナメモリアロケータ（バンプアロケーション） |
| `args` | コマンドライン引数パース |
| `assert` | アサーションユーティリティ |
| `async` | ThreadPool、parallel_map |
| `async_fs` | 非同期ファイルI/O操作 |
| `atomic` | アトミック操作（load、store、add、CAS、fence） |
| `bytes` | バイト順序ユーティリティ（bswap、hton/ntoh、エンディアン対応I/O） |
| `collections` | HashMap、Queue、Stack、Set、LinkedList、LRUCache |
| `compression` | gzip、gunzip、deflate |
| `crypto` | aes_encrypt、rsa_sign、random_bytes |
| `csv` | CSVパースと生成 |
| `debug` | タスク検査とスタック管理 |
| `datetime` | DateTimeクラス、フォーマット、パース |
| `decimal` | to_fixed、to_hex、parse_int、parse_float、StringBuilder |
| `encoding` | base64_encode、hex_encode、url_encode |
| `env` | getenv、setenv、exit、get_pid |
| `ffi` | FFIコールバック管理 |
| `fmt` | 文字列フォーマットユーティリティ |
| `fs` | open、read_file、write_file、list_dir、exists |
| `glob` | ファイルパターンマッチング |
| `hash` | sha1、sha256、sha512、md5、djb2、crc32、adler32 |
| `http` | http_get、http_post、http_request |
| `ipc` | プロセス間通信 |
| `iter` | イテレータユーティリティ |
| `jinja` | Jinja2互換テンプレートレンダリング |
| `json` | parse、stringify、pretty、get、set |
| `logging` | レベル付きLogger |
| `math` | sin、cos、sqrt、pow、rand、PI、E |
| `matrix` | 密行列演算（add、multiply、transpose、determinant、inverse） |
| `mmap` | メモリマップドファイルI/O（mmap、munmap、msync） |
| `net` | TcpListener、TcpStream、UdpSocket |
| `os` | platform、arch、cpu_count、hostname |
| `path` | ファイルパス操作 |
| `process` | fork、exec、wait、kill |
| `random` | 乱数生成 |
| `regex` | compile、test（POSIX ERE） |
| `retry` | バックオフ付きリトライロジック |
| `semver` | セマンティックバージョニング |
| `shell` | シェルコマンドユーティリティ |
| `signal` | シグナル定数（SIGINT、SIGTERMなど） |
| `sqlite` | SQLiteデータベース、query、exec、トランザクション |
| `strings` | pad_left、is_alpha、reverse、lines |
| `terminal` | ANSIカラーとスタイル |
| `termios` | 生ターミナル入力、キー検出 |
| `testing` | describe、test、expect |
| `time` | now、time_ms、sleep、clock |
| `toml` | TOMLパースと生成 |
| `url` | URLパースと操作 |
| `unix_socket` | Unixドメインソケット（AF_UNIXストリーム/データグラム） |
| `uuid` | UUID生成 |
| `vector` | ベクトル類似性検索（USearch ANN） |
| `websocket` | WebSocketクライアント |
| `yaml` | YAMLパースと生成 |

詳細なモジュールドキュメントについては`stdlib/docs/`を参照してください。

---

## FFI（外部関数インターフェース）

```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
let len = strlen("Hello!");  // 6

// 動的FFI
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

詳細なドキュメントについては`docs/advanced/ffi.md`を参照してください。

---

## プロジェクト構造

```
hemlock/
├── src/
│   ├── frontend/         # 共有：lexer、parser、AST、modules
│   ├── backends/
│   │   ├── interpreter/  # hemlock：ツリーウォーキングインタプリタ
│   │   └── compiler/     # hemlockc：Cコードジェネレータ
│   ├── modules/          # ネイティブモジュール実装
│   ├── runtime/          # ランタイム関連Cコード
│   ├── shared/           # 共有ユーティリティ（型昇格など）
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   ├── bundler/      # バンドル/パッケージツール
│   │   └── formatter/    # コードフォーマッタ
├── runtime/              # コンパイル済みプログラムランタイム（libhemlock_runtime.a）
├── stdlib/               # 標準ライブラリ
│   └── docs/             # モジュールドキュメント
├── include/              # Cヘッダファイル（hemlock_limits.hなど）
├── docs/                 # 完全なドキュメント
├── tests/                # 978+テスト
├── examples/             # サンプルプログラム
├── benchmark/            # ベンチマーク
├── editors/              # エディタ統合
└── wasm/                 # WebAssemblyサポート
```

### コンパイラ/インタプリタアーキテクチャ

両方のバックエンドは共通のフロントエンド（lexer、parser、AST）を共有しています。インタプリタはツリーウォーク評価を行い、コンパイラはCコードを生成してGCCでリンクします。詳細については`docs/`を参照してください。

---

## コードスタイルガイドライン

1. **`include/hemlock_limits.h`に定数を定義** - `HML_`プレフィックス付き
2. **マジックナンバーを避ける** - named定数を使用
3. **`hemlock_limits.h`をインクルード** - `internal.h`経由で定数にアクセス

---

## やってはいけないこと

- 暗黙の動作を追加（ASI、GC、自動クリーンアップ）
- 複雑さを隠す（マジック最適化、隠れた参照カウント）
- 既存のセマンティクスを破壊（セミコロン、手動メモリ、可変文字列）
- 暗黙の変換で精度を失う
- マジックナンバーを使用 - 代わりに`hemlock_limits.h`にnamed定数を定義

---

## テスト

```bash
make test              # インタプリタテストを実行
make test-compiler     # コンパイラテストを実行
make parity            # パリティテストを実行（両方が一致する必要がある）
make test-all          # すべてのテストスイートを実行
```

**重要：** テスト実行時は常にタイムアウトを使用してください（非同期テストがハングする可能性があります）：
```bash
timeout 60 make test
timeout 120 make parity
```

---

## パリティファースト開発

**インタプリタとコンパイラは、同じ入力に対して同一の出力を生成する必要があります。**

言語機能を追加または変更する際：
1. 共有フロントエンドでAST/セマンティック変更を設計
2. インタプリタに実装（ツリーウォーキング評価）
3. コンパイラに実装（Cコード生成）
4. `tests/parity/`に`.expected`ファイル付きでパリティテストを追加
5. マージ前に`make parity`を実行

各テストには`feature.hml` + `feature.expected`があります。両方のバックエンドが期待される出力と一致する必要があります。

---

## 哲学

> 私たちは安全であるためのツール（`buffer`、型注釈、境界チェック）を提供しますが、それらを使用することを強制しません（`ptr`、手動メモリ、安全でない操作）。

**機能がHemlockに適合するかどうかわからない場合は、「これはプログラマにより明示的な制御を与えるか、それとも何かを隠すか？」と問いかけてください。**

隠す場合、それはおそらくHemlockには属しません。
