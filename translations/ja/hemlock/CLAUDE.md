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
- `/`は常にfloatを返す（整数除算には`divi()`を使用）
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

**型昇格：** i8 → i16 → i32 → i64 → f32 → f64（floatが常に優先、ただしi64/u64 + f32 → f64で精度を保持）

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
let emoji = '🚀';        // rune（Unicode）
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### 型変換
```hemlock
// 型コンストラクタ関数 - 文字列を型にパース
let n = i32("42");       // 文字列をi32にパース
let f = f64("3.14");     // 文字列をf64にパース
let b = bool("true");    // 文字列をboolにパース（"true"または"false"）

// すべての数値型をサポート
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// 16進数と負数
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// 型エイリアスも動作
let x = integer("100");  // i32("100")と同じ
let y = number("1.5");   // f64("1.5")と同じ
let z = byte("200");     // u8("200")と同じ

// 数値型間の変換
let big = i64(42);       // i32からi64へ
let truncated = i32(3.99); // f64からi32へ（3に切り捨て）

// 型注釈は型を検証（文字列をパースしない）
let f: f64 = 100;        // 注釈によるi32からf64へ（数値変換OK）
// let n: i32 = "42";    // エラー - 文字列パースにはi32("42")を使用
```

### イントロスペクション
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5（バイト単位の文字列長）
len([1, 2, 3]);          // 3（配列長）
```

### メモリ
```hemlock
let p = alloc(64);       // 生ポインタ
let b = buffer(64);      // 安全なバッファ（境界チェック付き）
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // 手動クリーンアップ必須
```

### 制御フロー
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // 無限ループ（while(true)よりクリーン）
switch (x) { case 1: break; default: break; }  // Cスタイルのフォールスルー
defer cleanup();         // 関数が戻るときに実行

// ネストされたループでの対象指定break/continue用ループラベル
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // 外側ループをbreak
        if (i == 3) { continue outer; }  // 外側ループをcontinue
    }
}
```

### パターンマッチング
```hemlock
// match式 - 値を返す
let result = match (value) {
    0 => "zero",                    // リテラルパターン
    1 | 2 | 3 => "small",           // ORパターン
    n if n < 10 => "medium",        // ガード式
    n => "large: " + n              // 変数バインディング
};

// 型パターン
match (val) {
    n: i32 => "integer",
    s: string => "string",
    _ => "other"                    // ワイルドカード
}

// オブジェクトの分解
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// restを使った配列の分解
match (arr) {
    [] => "empty",
    [first, ...rest] => "head: " + first,
    _ => "other"
}

// ネストされたパターン
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

完全なドキュメントについては`docs/language-guide/pattern-matching.md`を参照してください。

### Null合体演算子
```hemlock
// Null合体（??）- 左がnon-nullなら左を、そうでなければ右を返す
let name = user.name ?? "Anonymous";
let first = a ?? b ?? c ?? "fallback";

// Null合体代入（??=）- nullの場合のみ代入
let config = null;
config ??= { timeout: 30 };    // configは{ timeout: 30 }になる
config ??= { timeout: 60 };    // configは変更されない（nullではない）

// プロパティとインデックスでも動作
obj.field ??= "default";
arr[0] ??= "first";

// 安全なナビゲーション（?.）- オブジェクトがnullならnullを返す
let city = user?.address?.city;  // どの部分がnullでもnull
let upper = name?.to_upper();    // 安全なメソッド呼び出し
let item = arr?.[0];             // 安全なインデックス
```

### 関数
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // 匿名/クロージャ

// 式本体関数（アロー構文）
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // 匿名式本体

// パラメータ修飾子
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // 参照渡し
fn print_all(const items: array) { for (i in items) { print(i); } }  // 不変
```

### 名前付き引数
```hemlock
// 関数は名前付き引数で呼び出し可能
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// 位置引数（従来型）
create_user("Alice", 25, false);

// 名前付き引数 - 任意の順序で指定可能
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// 必要なものだけ名前で指定してオプションパラメータをスキップ
create_user("David", active: false);  // デフォルトage=18を使用

// 名前付き引数は位置引数の後に来る必要がある
create_user("Eve", age: 21);          // OK：位置引数の後に名前付き
// create_user(name: "Bad", 25);      // エラー：名前付きの後に位置引数
```

**ルール：**
- 名前付き引数は`name: value`構文を使用
- 位置引数の後なら任意の順序で使用可能
- 名前付き引数の後に位置引数は使用不可
- デフォルト/オプションパラメータで動作
- 不明なパラメータ名は実行時エラー

### オブジェクトと列挙型
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// オブジェクトショートハンド構文（ES6スタイル）
let name = "Alice";
let age = 30;
let person = { name, age };         // { name: name, age: age }と同等

// オブジェクトスプレッド演算子
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // defaultsをコピーし、sizeをオーバーライド

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### 複合型（交差型/ダック型）
```hemlock
// 構造型を定義
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// 複合型：オブジェクトはすべての型を満たす必要がある
let person: HasName & HasAge = { name: "Alice", age: 30 };

// 複合型を使った関数パラメータ
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

// 3つ以上の型
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// 余分なフィールドは許可（ダック型）
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - 余分なフィールドは無視
};
```

複合型は、別の`interface`キーワードなしでインターフェースのような動作を提供し、
既存の`define`とダック型のパラダイムの上に構築されています。

### 型エイリアス
```hemlock
// シンプルな型エイリアス
type Integer = i32;
type Text = string;

// 関数型エイリアス
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// 複合型エイリアス（再利用可能なインターフェースに最適）
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// ジェネリック型エイリアス
type Pair<T> = { first: T, second: T };

// 型エイリアスの使用
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

型エイリアスは複雑な型に名前付きショートカットを作成し、可読性と保守性を向上させます。

### 関数型
```hemlock
// パラメータ用の関数型注釈
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// 関数を返す高階関数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// 非同期関数型
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// 複数パラメータを持つ関数型
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Constパラメータ
```hemlock
// Constパラメータ - 深い不変性
fn print_all(const items: array) {
    // items.push(4);  // エラー：constパラメータを変更できない
    for (item in items) {
        print(item);
    }
}

// オブジェクトでのconst - どのパスからも変更不可
fn describe(const person: object) {
    print(person.name);       // OK：読み取りは許可
    // person.name = "Bob";   // エラー：変更できない
}

// 読み取り用のネストされたアクセスは許可
fn get_city(const user: object) {
    return user.address.city;  // OK：ネストされたプロパティの読み取り
}
```

`const`修飾子は、ネストされたプロパティを含むパラメータのあらゆる変更を防ぎます。
これにより、入力を変更すべきでない関数のコンパイル時安全性が提供されます。

### Refパラメータ（参照渡し）
```hemlock
// Refパラメータ - 呼び出し元の変数を直接変更
fn increment(ref x: i32) {
    x = x + 1;  // 元の変数を変更
}

let count = 10;
increment(count);
print(count);  // 11 - 元が変更された

// 古典的なswap関数
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// refと通常のパラメータを混在
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

`ref`修飾子は呼び出し元の変数への参照を渡し、関数がそれを直接変更できるようにします。
`ref`がない場合、プリミティブは値渡し（コピー）されます。値を返さずに呼び出し元の
状態を変更する必要がある場合に`ref`を使用します。

**ルール：**
- `ref`パラメータには変数を渡す必要があり、リテラルや式は不可
- すべての型で動作（プリミティブ、配列、オブジェクト）
- 型注釈と組み合わせ可能：`ref x: i32`
- `const`と組み合わせ不可（反対の意味）

### Defineでのメソッドシグネチャ
```hemlock
// メソッドシグネチャを持つdefine（インターフェースパターン）
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // 必須メソッドシグネチャ
}

// オブジェクトは必須メソッドを提供する必要がある
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// ?を使ったオプションメソッド
define Serializable {
    fn serialize(): string,        // 必須
    fn pretty?(): string           // オプションメソッド
}

// Self型は定義型を参照
define Cloneable {
    fn clone(): Self   // オブジェクトと同じ型を返す
}
```

`define`ブロック内のメソッドシグネチャはカンマ区切り（TypeScriptインターフェースのような）を使用し、
オブジェクトが満たすべき契約を確立し、Hemlockのダック型システムでインターフェースのような
プログラミングパターンを可能にします。

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

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**メモリ所有権：** タスクはプリミティブ値のコピーを受け取りますが、ポインタは共有します。スポーンされたタスクに`ptr`を渡す場合、タスクが完了するまでメモリが有効であることを保証する必要があります。`free()`の前に`join()`を使用するか、完了を通知するためにチャネルを使用してください。

### ユーザー入力
```hemlock
let name = read_line();          // stdinから行を読み取り（ブロック）
print("Hello, " + name);
eprint("Error message");         // stderrに出力

// read_line()はEOFでnullを返す
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Got:", line);
}
```

### ファイルI/O
```hemlock
let f = open("file.txt", "r");  // モード：r, w, a, r+, w+, a+
let content = f.read();
f.write("data");
f.seek(0);
f.close();
```

### シグナル
```hemlock
signal(SIGINT, fn(sig) { print("Interrupted"); });
raise(SIGUSR1);
```

---

## 文字列メソッド（19個）

`substr`、`slice`、`find`、`contains`、`split`、`trim`、`to_upper`、`to_lower`、
`starts_with`、`ends_with`、`replace`、`replace_all`、`repeat`、`char_at`、
`byte_at`、`chars`、`bytes`、`to_bytes`、`deserialize`

テンプレート文字列：`` `Hello ${name}!` ``

**文字列の可変性：** 文字列はインデックス代入（`s[0] = 'H'`）で変更可能ですが、すべての文字列メソッドは元を変更せず新しい文字列を返します。これにより、必要な場合のインプレース変更を可能にしながら、メソッドチェーンを関数型に保ちます。

**文字列長プロパティ：**
```hemlock
let s = "hello 🚀";
print(s.length);       // 7（文字/rune数）
print(s.byte_length);  // 10（バイト数 - 絵文字はUTF-8で4バイト）
```

## 配列メソッド（18個）

`push`、`pop`、`shift`、`unshift`、`insert`、`remove`、`find`、`contains`、
`slice`、`join`、`concat`、`reverse`、`first`、`last`、`clear`、`map`、`filter`、`reduce`

型付き配列：`let nums: array<i32> = [1, 2, 3];`

---

## 標準ライブラリ（40モジュール）

`@stdlib/`プレフィックスでインポート：
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| モジュール | 説明 |
|--------|-------------|
| `arena` | アリーナメモリアロケータ（バンプアロケーション） |
| `args` | コマンドライン引数パース |
| `assert` | アサーションユーティリティ |
| `async` | ThreadPool、parallel_map |
| `async_fs` | 非同期ファイルI/O操作 |
| `collections` | HashMap、Queue、Stack、Set、LinkedList、LRUCache |
| `compression` | gzip、gunzip、deflate |
| `crypto` | aes_encrypt、rsa_sign、random_bytes |
| `csv` | CSVパースと生成 |
| `datetime` | DateTimeクラス、フォーマット、パース |
| `encoding` | base64_encode、hex_encode、url_encode |
| `env` | getenv、setenv、exit、get_pid |
| `fmt` | 文字列フォーマットユーティリティ |
| `fs` | read_file、write_file、list_dir、exists |
| `glob` | ファイルパターンマッチング |
| `hash` | sha256、sha512、md5、djb2 |
| `http` | http_get、http_post、http_request |
| `ipc` | プロセス間通信 |
| `iter` | イテレータユーティリティ |
| `json` | parse、stringify、pretty、get、set |
| `logging` | レベル付きLogger |
| `math` | sin、cos、sqrt、pow、rand、PI、E |
| `net` | TcpListener、TcpStream、UdpSocket |
| `os` | platform、arch、cpu_count、hostname |
| `path` | ファイルパス操作 |
| `process` | fork、exec、wait、kill |
| `random` | 乱数生成 |
| `regex` | compile、test（POSIX ERE） |
| `retry` | バックオフ付きリトライロジック |
| `semver` | セマンティックバージョニング |
| `shell` | シェルコマンドユーティリティ |
| `sqlite` | SQLiteデータベース、query、exec、トランザクション |
| `strings` | pad_left、is_alpha、reverse、lines |
| `terminal` | ANSIカラーとスタイル |
| `testing` | describe、test、expect |
| `time` | now、time_ms、sleep、clock |
| `toml` | TOMLパースと生成 |
| `url` | URLパースと操作 |
| `uuid` | UUID生成 |
| `websocket` | WebSocketクライアント |

詳細なモジュールドキュメントについては`stdlib/docs/`を参照してください。

---

## FFI（外部関数インターフェース）

共有ライブラリからC関数を宣言して呼び出し：
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hello!");  // 6
let pid = getpid();
```

モジュールからFFI関数をエクスポート：
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

動的FFI（実行時バインディング）：
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

型：`FFI_INT`、`FFI_DOUBLE`、`FFI_POINTER`、`FFI_STRING`、`FFI_VOID`など

---

## アトミック操作

アトミック操作によるロックフリー並行プログラミング：

```hemlock
// アトミックi32用のメモリを確保
let p = alloc(4);
ptr_write_i32(p, 0);

// アトミックload/store
let val = atomic_load_i32(p);        // アトミックに読み取り
atomic_store_i32(p, 42);             // アトミックに書き込み

// fetch-and-modify操作（古い値を返す）
let old = atomic_add_i32(p, 10);     // 加算、古い値を返す
old = atomic_sub_i32(p, 5);          // 減算、古い値を返す
old = atomic_and_i32(p, 0xFF);       // ビット単位AND
old = atomic_or_i32(p, 0x10);        // ビット単位OR
old = atomic_xor_i32(p, 0x0F);       // ビット単位XOR

// Compare-and-swap（CAS）
let success = atomic_cas_i32(p, 42, 100);  // *p == 42なら100に設定
// スワップが成功したらtrue、そうでなければfalseを返す

// アトミック交換
old = atomic_exchange_i32(p, 999);   // スワップ、古い値を返す

free(p);

// i64バリアントも使用可能（atomic_load_i64、atomic_add_i64など）

// メモリフェンス（フルバリア）
atomic_fence();
```

すべての操作はシーケンシャル一貫性（`memory_order_seq_cst`）を使用します。

---

## プロジェクト構造

```
hemlock/
├── src/
│   ├── frontend/         # 共有：lexer、parser、AST、modules
│   ├── backends/
│   │   ├── interpreter/  # hemlock：ツリーウォーキングインタプリタ
│   │   └── compiler/     # hemlockc：Cコードジェネレータ
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # バンドル/パッケージツール
├── runtime/              # コンパイル済みプログラムランタイム（libhemlock_runtime.a）
├── stdlib/               # 標準ライブラリ（40モジュール）
│   └── docs/             # モジュールドキュメント
├── docs/                 # 完全なドキュメント
│   ├── language-guide/   # 型、文字列、配列など
│   ├── reference/        # APIリファレンス
│   └── advanced/         # 非同期、FFI、シグナルなど
├── tests/                # 625+テスト
└── examples/             # サンプルプログラム
```

---

## コードスタイルガイドライン

### 定数とマジックナンバー

Cコードベースに数値定数を追加する際は、以下のガイドラインに従ってください：

1. **`include/hemlock_limits.h`に定数を定義** - このファイルは、すべてのコンパイル時および実行時の制限、容量、名前付き定数の中心的な場所です。

2. **`HML_`プレフィックスを持つ説明的な名前を使用** - すべての定数は名前空間の明確さのために`HML_`プレフィックスを付ける必要があります。

3. **マジックナンバーを避ける** - ハードコードされた数値をnamed定数に置き換えてください。例：
   - 型範囲制限：`HML_I8_MIN`、`HML_I8_MAX`、`HML_U32_MAX`
   - バッファ容量：`HML_INITIAL_ARRAY_CAPACITY`、`HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - 時間変換：`HML_NANOSECONDS_PER_SECOND`、`HML_MILLISECONDS_PER_SECOND`
   - ハッシュシード：`HML_DJB2_HASH_SEED`
   - ASCII値：`HML_ASCII_CASE_OFFSET`、`HML_ASCII_PRINTABLE_START`

4. **`hemlock_limits.h`をインクルード** - ソースファイルは定数にアクセスするためにこのヘッダー（多くの場合`internal.h`経由）をインクルードする必要があります。

5. **目的を文書化** - 各定数が何を表すかを説明するコメントを追加してください。

---

## やってはいけないこと

❌ 暗黙の動作を追加（ASI、GC、自動クリーンアップ）
❌ 複雑さを隠す（マジック最適化、隠れた参照カウント）
❌ 既存のセマンティクスを破壊（セミコロン、手動メモリ、可変文字列）
❌ 暗黙の変換で精度を失う
❌ マジックナンバーを使用 - 代わりに`hemlock_limits.h`にnamed定数を定義

---

## テスト

```bash
make test              # インタプリタテストを実行
make test-compiler     # コンパイラテストを実行
make parity            # パリティテストを実行（両方が一致する必要がある）
make test-all          # すべてのテストスイートを実行
```

**重要：** 非同期/並行処理の問題によりテストがハングすることがあります。テスト実行時は常にタイムアウトを使用してください：
```bash
timeout 60 make test   # 60秒タイムアウト
timeout 120 make parity
```

テストカテゴリ：primitives、memory、strings、arrays、functions、objects、async、ffi、defer、signals、switch、bitwise、typed_arrays、modules、stdlib_*

---

## コンパイラ/インタプリタアーキテクチャ

Hemlockには共通のフロントエンドを共有する2つの実行バックエンドがあります：

```
ソース（.hml）
    ↓
┌─────────────────────────────┐
│  共有フロントエンド           │
│  - Lexer（src/frontend/）    │
│  - Parser（src/frontend/）   │
│  - AST（src/frontend/）      │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ インタプリタ │    │  コンパイラ │
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ ツリーウォー│    │ 型チェック  │
│ ク評価     │    │ AST → C    │
│            │    │ gccリンク  │
└────────────┘    └────────────┘
```

### コンパイラ型チェック

コンパイラ（`hemlockc`）にはコンパイル時型チェックが含まれており、**デフォルトで有効**です：

```bash
hemlockc program.hml -o program    # 型チェック後、コンパイル
hemlockc --check program.hml       # 型チェックのみ、コンパイルしない
hemlockc --no-type-check prog.hml  # 型チェックを無効化
hemlockc --strict-types prog.hml   # 暗黙の'any'型に警告
```

型チェッカーは：
- コンパイル時に型注釈を検証
- 型注釈のないコードを動的（`any`型）として扱う - 常に有効
- アンボックス化のための最適化ヒントを提供
- 許容的な数値変換を使用（範囲は実行時に検証）

### ディレクトリ構造

```
hemlock/
├── src/
│   ├── frontend/           # 共有：lexer、parser、AST、modules
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock：ツリーウォーキングインタプリタ
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc：Cコードジェネレータ
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # 言語サーバー
│   │   └── bundler/        # バンドル/パッケージツール
├── runtime/                # コンパイル済みプログラム用libhemlock_runtime.a
├── stdlib/                 # 共有標準ライブラリ
└── tests/
    ├── parity/             # 両方のバックエンドでパスする必要があるテスト
    ├── interpreter/        # インタプリタ固有のテスト
    └── compiler/           # コンパイラ固有のテスト
```

---

## パリティファースト開発

**インタプリタとコンパイラは、同じ入力に対して同一の出力を生成する必要があります。**

### 開発ポリシー

言語機能を追加または変更する際：

1. **設計** - 共有フロントエンドでAST/セマンティック変更を定義
2. **インタプリタ実装** - ツリーウォーキング評価を追加
3. **コンパイラ実装** - Cコード生成を追加
4. **パリティテスト追加** - `tests/parity/`に`.expected`ファイル付きでテストを記述
5. **検証** - マージ前に`make parity`を実行

### パリティテスト構造

```
tests/parity/
├── language/       # コア言語機能（制御フロー、クロージャなど）
├── builtins/       # 組み込み関数（print、typeof、memoryなど）
├── methods/        # 文字列と配列メソッド
└── modules/        # import/export、stdlibインポート
```

各テストには2つのファイルがあります：
- `feature.hml` - テストプログラム
- `feature.expected` - 期待される出力（両方のバックエンドで一致する必要がある）

### パリティテスト結果

| ステータス | 意味 |
|--------|---------|
| `✓ PASSED` | インタプリタとコンパイラの両方が期待される出力と一致 |
| `◐ INTERP_ONLY` | インタプリタは動作、コンパイラは失敗（コンパイラ修正が必要） |
| `◑ COMPILER_ONLY` | コンパイラは動作、インタプリタは失敗（まれ） |
| `✗ FAILED` | 両方失敗（テストまたは実装のバグ） |

### パリティが必要なもの

- すべての言語構造（if、while、for、switch、defer、try/catch）
- すべての演算子（算術、ビット単位、論理、比較）
- すべての組み込み関数（print、typeof、allocなど）
- すべての文字列と配列メソッド
- 型強制と昇格ルール
- 実行時エラーのエラーメッセージ

### 異なっても良いもの

- パフォーマンス特性
- メモリレイアウトの詳細
- デバッグ/スタックトレースのフォーマット
- コンパイルエラー（コンパイラはコンパイル時により多くをキャッチする可能性がある）

### パリティテストの追加

```bash
# 1. テストファイルを作成
cat > tests/parity/language/my_feature.hml << 'EOF'
// テストの説明
let x = some_feature();
print(x);
EOF

# 2. インタプリタから期待される出力を生成
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. パリティを検証
make parity
```

---

## バージョン

**v1.8.0** - 以下を含む現在のリリース：
- **パターンマッチング**（`match`式）- 強力な分解と制御フロー：
  - リテラル、ワイルドカード、変数バインディングパターン
  - ORパターン（`1 | 2 | 3`）
  - ガード式（`n if n > 0`）
  - オブジェクト分解（`{ x, y }`）
  - restを使った配列分解（`[first, ...rest]`）
  - 型パターン（`n: i32`）
  - インタプリタとコンパイラ間の完全なパリティ
- **コンパイラヘルパー注釈** - GCC/Clang制御用の11の最適化注釈：
  - `@inline`、`@noinline` - 関数インライン化制御
  - `@hot`、`@cold` - 分岐予測ヒント
  - `@pure`、`@const` - 副作用注釈
  - `@flatten` - 関数内のすべての呼び出しをインライン化
  - `@optimize(level)` - 関数ごとの最適化レベル（"0"、"1"、"2"、"3"、"s"、"fast"）
  - `@warn_unused` - 戻り値が無視された場合に警告
  - `@section(name)` - カスタムELFセクション配置（例：`@section(".text.hot")`）
- **式本体関数**（`fn double(x): i32 => x * 2;`）- 簡潔な単一式関数構文
- **単一行文** - ブレースなし`if`、`while`、`for`構文（例：`if (x > 0) print(x);`）
- **型エイリアス**（`type Name = Type;`）- 複雑な型のnamed ショートカット
- **関数型注釈**（`fn(i32): i32`）- ファーストクラス関数型
- **Constパラメータ**（`fn(const x: array)`）- パラメータの深い不変性
- **Refパラメータ**（`fn(ref x: i32)`）- 直接呼び出し元変更用の参照渡し
- **defineでのメソッドシグネチャ**（`fn method(): Type`）- インターフェースのような契約（カンマ区切り）
- メソッドシグネチャでの**Self型** - 定義型を参照
- **Loopキーワード**（`loop { }`）- よりクリーンな無限ループ、`while (true)`を置き換え
- **ループラベル**（`outer: while`）- ネストされたループでの対象指定break/continue
- **オブジェクトショートハンド**（`{ name }`）- ES6スタイルのショートハンドプロパティ構文
- **オブジェクトスプレッド**（`{ ...obj }`）- オブジェクトフィールドのコピーとマージ
- **複合ダック型**（`A & B & C`）- 構造型のための交差型
- 関数呼び出しの**名前付き引数**（`foo(name: "value", age: 30)`）
- 安全なnullハンドリングのための**Null合体演算子**（`??`、`??=`、`?.`）
- **8進リテラル**（`0o777`、`0O123`）
- **数値セパレータ**（`1_000_000`、`0xFF_FF`、`0b1111_0000`）
- **ブロックコメント**（`/* ... */`）
- 文字列/runeでの**16進エスケープシーケンス**（`\x41` = 'A'）
- 文字列での**Unicodeエスケープシーケンス**（`\u{1F600}` = 😀）
- **先頭ゼロなしのfloatリテラル**（`.5`、`.123`、`.5e2`）
- hemlockc での**コンパイル時型チェック**（デフォルトで有効）
- リアルタイム診断用の型チェック付き**LSP統合**
- **複合代入演算子**（`+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`）
- **インクリメント/デクリメント演算子**（`++x`、`x++`、`--x`、`x--`）
- **型精度修正**：i64/u64 + f32 → f64で精度を保持
- アンボックス化最適化ヒント付き統一型システム
- 完全な型システム（i8-i64、u8-u64、f32/f64、bool、string、rune、ptr、buffer、array、object、enum、file、task、channel）
- 19メソッド付きUTF-8文字列
- map/filter/reduceを含む18メソッド付き配列
- `talloc()`と`sizeof()`を使った手動メモリ管理
- 真のpthread並列処理を持つAsync/await
- ロックフリー並行プログラミング用アトミック操作
- 40 stdlibモジュール（+ arena、assert、semver、toml、retry、iter、random、shell）
- 再利用可能なライブラリラッパー用の`export extern fn`を持つCインターオペ用FFI
- コンパイラでのFFI構造体サポート（C構造体を値渡し）
- FFIポインタヘルパー（`ptr_null`、`ptr_read_*`、`ptr_write_*`）
- defer、try/catch/finally/throw、panic
- ファイルI/O、シグナルハンドリング、コマンド実行
- GitHubベースのレジストリを持つ[hpm](https://github.com/hemlang/hpm)パッケージマネージャ
- 100%インタプリタパリティを持つコンパイラバックエンド（Cコード生成）
- go-to-definitionとfind-referencesを持つLSPサーバー
- O(1)ルックアップのためのAST最適化パスと変数解決
- 動的関数呼び出し用apply()ビルトイン
- アンバッファードチャネルと多パラメータサポート
- 159パリティテスト（100%パス率）

---

## 哲学

> 私たちは安全であるためのツール（`buffer`、型注釈、境界チェック）を提供しますが、それらを使用することを強制しません（`ptr`、手動メモリ、安全でない操作）。

**機能がHemlockに適合するかどうかわからない場合は、「これはプログラマにより明示的な制御を与えるか、それとも何かを隠すか？」と問いかけてください。**

隠す場合、それはおそらくHemlockには属しません。
