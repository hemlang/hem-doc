# 型システム

Hemlockは**動的型システム**を特徴とし、オプションの型注釈と実行時型チェックを備えています。

---

## 型選択ガイド：どの型を使うべき？

**型に慣れていない方**はここから始めてください。型システムに詳しい方は[設計思想](#設計思想)にスキップできます。

### 簡潔な答え

**Hemlockに任せましょう：**

```hemlock
let count = 42;        // Hemlockはこれが整数だと知っている
let price = 19.99;     // Hemlockはこれが小数だと知っている
let name = "Alice";    // Hemlockはこれがテキストだと知っている
let active = true;     // Hemlockはこれがyes/noだと知っている
```

Hemlockは値に対して自動的に適切な型を選びます。型を指定する*必要*はありません。

### 型注釈を追加するタイミング

以下の場合に型を追加します：

1. **サイズを明確にしたい** - `i8` vs `i64`はメモリやFFIで重要
2. **コードをドキュメント化したい** - 型は関数が何を期待するか示す
3. **早期にミスを検出したい** - Hemlockは実行時に型をチェック

```hemlock
// 型なし（問題なく動作）：
fn add(a, b) {
    return a + b;
}

// 型あり（より明示的）：
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### クイックリファレンス：数値型の選択

| 格納するもの | 推奨型 | 例 |
|---------------------|----------------|---------|
| 通常の整数 | `i32`（デフォルト） | `let count = 42;` |
| 非常に大きな数 | `i64` | `let population = 8000000000;` |
| 負にならないカウント | `u32` | `let items: u32 = 100;` |
| バイト（0-255） | `u8` | `let pixel: u8 = 255;` |
| 小数/分数 | `f64`（デフォルト） | `let price = 19.99;` |
| パフォーマンス重視の小数 | `f32` | `let x: f32 = 1.5;` |

### クイックリファレンス：すべての型

| カテゴリ | 型 | 使用場面 |
|----------|-------|-------------|
| **整数** | `i8`、`i16`、`i32`、`i64` | カウント、ID、年齢など |
| **正の数のみ** | `u8`、`u16`、`u32`、`u64` | バイト、サイズ、配列長 |
| **小数** | `f32`、`f64` | 金額、測定値、数学 |
| **Yes/No** | `bool` | フラグ、条件 |
| **テキスト** | `string` | 名前、メッセージ、あらゆるテキスト |
| **単一文字** | `rune` | 個々の文字、絵文字 |
| **リスト** | `array` | 値のコレクション |
| **名前付きフィールド** | `object` | 関連データのグループ化 |
| **生メモリ** | `ptr`、`buffer` | 低レベルプログラミング |
| **なし** | `null` | 値の不在 |

### 一般的なシナリオ

**「数値が欲しいだけ」**
```hemlock
let x = 42;  // 完了！Hemlockがi32を選ぶ
```

**「小数が必要」**
```hemlock
let price = 19.99;  // 完了！Hemlockがf64を選ぶ
```

**「バイトを扱っている（ファイル、ネットワーク）」**
```hemlock
let byte: u8 = 255;  // 0-255の範囲
```

**「本当に大きな数が必要」**
```hemlock
let big = 9000000000000;  // Hemlockが自動でi64を選ぶ（> i32 最大値）
// または明示的に：
let big: i64 = 9000000000000;
```

**「金額を格納している」**
```hemlock
// オプション1：浮動小数点（シンプルだが精度に限界あり）
let price: f64 = 19.99;

// オプション2：セントで格納（より精密）
let price_cents: i32 = 1999;  // $19.99を整数セントで
```

**「Cコードにデータを渡している（FFI）」**
```hemlock
// C言語の型に正確に合わせる
let c_int: i32 = 100;      // Cの'int'
let c_long: i64 = 100;     // Cの'long'（64ビット環境）
let c_char: u8 = 65;       // Cの'char'
let c_double: f64 = 3.14;  // Cの'double'
```

### 型が混在するとどうなる？

異なる型を組み合わせると、Hemlockは「大きい」型に昇格します：

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // resultはf64（12.5）
// 整数が自動的に小数になった
```

**経験則：** 浮動小数点は常に「勝つ」 - 整数と浮動小数点を混ぜると浮動小数点になります。

### 型エラー

間違った型を使おうとすると、Hemlockは実行時に教えてくれます：

```hemlock
let age: i32 = "thirty";  // エラー：型不一致 - i32を期待、stringを受け取った
```

型を変換するには、型コンストラクタ関数を使用します：

```hemlock
let text = "42";
let number = i32(text);   // 文字列を整数にパース：42
let back = text + "";     // すでに文字列
```

---

## 設計思想

- **デフォルトで動的** - すべての値は実行時型タグを持つ
- **選択で型付け** - オプションの型注釈は実行時チェックを強制
- **明示的な変換** - 暗黙の変換は明確な昇格ルールに従う
- **型について正直** - `typeof()`は常に真実を伝える

## プリミティブ型

### 整数型

**符号付き整数：**
```hemlock
let tiny: i8 = 127;              // 8ビット（-128から127）
let small: i16 = 32767;          // 16ビット（-32768から32767）
let normal: i32 = 2147483647;    // 32ビット（デフォルト）
let large: i64 = 9223372036854775807;  // 64ビット
```

**符号なし整数：**
```hemlock
let byte: u8 = 255;              // 8ビット（0から255）
let word: u16 = 65535;           // 16ビット（0から65535）
let dword: u32 = 4294967295;     // 32ビット（0から4294967295）
let qword: u64 = 18446744073709551615;  // 64ビット
```

**型エイリアス：**
```hemlock
let i: integer = 42;   // i32のエイリアス
let b: byte = 255;     // u8のエイリアス
```

### 浮動小数点型

```hemlock
let f: f32 = 3.14159;        // 32ビット浮動小数点
let d: f64 = 2.718281828;    // 64ビット浮動小数点（デフォルト）
let n: number = 1.618;       // f64のエイリアス
```

### 真偽値型

```hemlock
let flag: bool = true;
let active: bool = false;
```

### 文字列型

```hemlock
let text: string = "Hello, World!";
let empty: string = "";
```

文字列は**可変**、**UTF-8エンコード**、**ヒープ割り当て**です。

詳細は[文字列](strings.md)を参照してください。

### ルーン型

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

ルーンは**Unicodeコードポイント**（U+0000からU+10FFFF）を表します。

詳細は[ルーン](runes.md)を参照してください。

### Null型

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null`は単一の値を持つ独自の型です。

## 複合型

### 配列型

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];  // 混合型も可能
let empty: array = [];
```

詳細は[配列](arrays.md)を参照してください。

### オブジェクト型

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

詳細は[オブジェクト](objects.md)を参照してください。

### ポインタ型

**生ポインタ：**
```hemlock
let p: ptr = alloc(64);
// 境界チェックなし、手動のライフタイム管理
free(p);
```

**安全なバッファ：**
```hemlock
let buf: buffer = buffer(64);
// 境界チェック付き、長さと容量を追跡
free(buf);
```

詳細は[メモリ管理](memory.md)を参照してください。

## 列挙型

列挙型は名前付き定数のセットを定義します：

### 基本的な列挙型

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// 比較
if (c == Color.RED) {
    print("It's red!");
}

// 列挙型でのswitch
switch (c) {
    case Color.RED:
        print("Stop");
        break;
    case Color.GREEN:
        print("Go");
        break;
    case Color.BLUE:
        print("Blue?");
        break;
}
```

### 値を持つ列挙型

列挙型は明示的な整数値を持つことができます：

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### 自動インクリメント値

明示的な値がない場合、列挙型は0から自動インクリメントします：

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// 明示的な値と自動値を混在可能
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### 列挙型の使用パターン

```hemlock
// 関数パラメータとして
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Urgent!");
    }
}

set_priority(Priority.HIGH);

// オブジェクト内で
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Fix bug",
    priority: Priority.HIGH
};
```

## 特殊型

### ファイル型

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

開いているファイルハンドルを表します。

### タスク型

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

非同期タスクハンドルを表します。

### チャネル型

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

タスク間の通信チャネルを表します。

### Void型

```hemlock
extern fn exit(code: i32): void;
```

値を返さない関数に使用（FFIのみ）。

## 型推論

### 整数リテラルの推論

Hemlockは値の範囲に基づいて整数型を推論します：

```hemlock
let a = 42;              // i32（32ビットに収まる）
let b = 5000000000;      // i64（> i32 最大値）
let c = 128;             // i32
let d: u8 = 128;         // u8（明示的な注釈）
```

**ルール：**
- i32範囲（-2147483648から2147483647）の値：`i32`と推論
- i32範囲外だがi64範囲内の値：`i64`と推論
- 他の型（i8、i16、u8、u16、u32、u64）には明示的な注釈を使用

### 浮動小数点リテラルの推論

```hemlock
let x = 3.14;        // f64（デフォルト）
let y: f32 = 3.14;   // f32（明示的）
```

### 指数表記

Hemlockは数値リテラルの指数表記をサポートします：

```hemlock
let a = 1e10;        // 10000000000.0（f64）
let b = 1e-12;       // 0.000000000001（f64）
let c = 3.14e2;      // 314.0（f64）
let d = 2.5e-3;      // 0.0025（f64）
let e = 1E10;        // 大文字小文字を区別しない
let f = 1e+5;        // 明示的な正の指数
```

**注意：** 指数表記を使用するリテラルは常に`f64`と推論されます。

### その他の型推論

```hemlock
let s = "hello";     // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## 型注釈

### 変数の注釈

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### 関数パラメータの注釈

```hemlock
fn greet(name: string, age: i32) {
    print("Hello, " + name + "!");
}
```

### 関数戻り値型の注釈

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### オブジェクト型の注釈（ダック型）

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## 型チェック

### 実行時型チェック

型注釈は**実行時**にチェックされ、コンパイル時ではありません：

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // 実行時エラー：型不一致

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "hello");     // 実行時エラー：型不一致
```

### 型クエリ

`typeof()`を使用して値の型をチェックします：

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("hello"));    // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## 型変換

### 暗黙の型昇格

演算で型を混在させると、Hemlockは「上位」の型に昇格します：

**昇格階層（低いから高い）：**
```
i8 → i16 → i32 → u32 → i64 → u64 → f32 → f64
      ↑     ↑     ↑
     u8    u16
```

**浮動小数点が常に勝つ：**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // resultはf64（13.5）
```

**大きいサイズが勝つ：**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sumはi64（300）
```

**精度の保持：** 64ビット整数とf32を混在させると、Hemlockは精度損失を避けるためにf64に昇格します（f32は24ビットの仮数部しかなく、i64/u64には不十分）：
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // resultはf64、f32ではない！
```

**例：**
```hemlock
u8 + i32  → i32
i32 + i64 → i64
u32 + u64 → u64
i32 + f32 → f32    // f32はi32に十分
i64 + f32 → f64    // i64の精度を保持するためにf64が必要
i64 + f64 → f64
i8 + f64  → f64
```

### 明示的な型変換

**整数 ↔ 浮動小数点：**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 → f64（42.0）

let x: f64 = 3.14;
let n: i32 = x;      // f64 → i32（3、切り捨て）
```

**整数 ↔ ルーン：**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 → rune（'A'）

let r: rune = 'Z';
let value: i32 = r;   // rune → i32（90）
```

**ルーン → 文字列：**
```hemlock
let ch: rune = '🚀';
let s: string = ch;   // rune → string（"🚀"）
```

**u8 → ルーン：**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 → rune（'A'）
```

### 型コンストラクタ関数

型名は値を変換またはパースする関数として使用できます：

**文字列を数値にパース：**
```hemlock
let n = i32("42");       // 文字列をi32にパース：42
let f = f64("3.14159");  // 文字列をf64にパース：3.14159
let b = bool("true");    // 文字列をboolにパース：true

// すべての数値型をサポート
let a = i8("-128");      // i8にパース
let c = u8("255");       // u8にパース
let d = i16("1000");     // i16にパース
let e = u16("50000");    // u16にパース
let g = i64("9000000000000"); // i64にパース
let h = u64("18000000000000"); // u64にパース
let j = f32("1.5");      // f32にパース
```

**16進数と負数：**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10（2進数）
```

**型エイリアスも動作：**
```hemlock
let x = integer("100");  // i32("100")と同じ
let y = number("1.5");   // f64("1.5")と同じ
let z = byte("200");     // u8("200")と同じ
```

**数値型間の変換：**
```hemlock
let big = i64(42);           // i32からi64
let truncated = i32(3.99);   // f64からi32（3に切り捨て）
let promoted = f64(100);     // i32からf64（100.0）
let narrowed = i8(127);      // i32からi8
```

**型注釈は数値変換を行う（文字列パースは行わない）：**
```hemlock
let f: f64 = 100;        // 注釈によるi32からf64へ（OK）
let s: string = 'A';     // 注釈によるルーンから文字列へ（OK）
let code: i32 = 'A';     // 注釈によるルーンからi32へ（コードポイントを取得、OK）

// 文字列パースには明示的な型コンストラクタが必要：
let n = i32("42");       // 文字列パースには型コンストラクタを使用
// let x: i32 = "42";    // エラー - 型注釈は文字列をパースしない
```

**エラー処理：**
```hemlock
// 無効な文字列は型コンストラクタ使用時にエラーをスロー
let bad = i32("hello");  // 実行時エラー："hello"をi32としてパースできない
let overflow = u8("256"); // 実行時エラー：256はu8の範囲外
```

**真偽値のパース：**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("yes");   // 実行時エラー："true"または"false"である必要がある
```

## 範囲チェック

型注釈は代入時に範囲チェックを強制します：

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // エラー：u8の範囲外

let a: i8 = 127;    // OK
let b: i8 = 128;    // エラー：i8の範囲外

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // エラー：u64は負になれない
```

## 型昇格の例

### 混合整数型

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32（30）

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32（300）
```

### 整数 + 浮動小数点

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32（12.5）
```

### 複雑な式

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64（70.0）
// 評価：b * c → f64(60.0)
//       a + f64(60.0) → f64(70.0)
```

## ダック型（オブジェクト）

オブジェクトは**構造型**（ダック型）を使用します：

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK：必要なフィールドをすべて持っている
let p1: Person = { name: "Alice", age: 30 };

// OK：余分なフィールドは許可
let p2: Person = { name: "Bob", age: 25, city: "NYC" };

// エラー：'age'フィールドがない
let p3: Person = { name: "Carol" };

// エラー：'age'の型が違う
let p4: Person = { name: "Dave", age: "thirty" };
```

**型チェックは代入時に行われる：**
- すべての必須フィールドが存在することを検証
- フィールドの型が一致することを検証
- 余分なフィールドは許可され、保持される
- `typeof()`用にオブジェクトの型名を設定

## オプションフィールド

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // デフォルト付きオプション
    timeout?: i32,     // オプション、デフォルトはnull
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false（デフォルト）
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true（オーバーライド）
```

## 型エイリアス

Hemlockは`type`キーワードを使用したカスタム型エイリアスをサポートします：

### 基本的な型エイリアス

```hemlock
// シンプルな型エイリアス
type Integer = i32;
type Text = string;

// エイリアスの使用
let x: Integer = 42;
let msg: Text = "hello";
```

### 関数型エイリアス

```hemlock
// 関数型エイリアス
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// 関数型エイリアスの使用
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### 複合型エイリアス

```hemlock
// 複数のdefineを1つの型に結合
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### ジェネリック型エイリアス

```hemlock
// ジェネリック型エイリアス
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// ジェネリックエイリアスの使用
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**注意：** 型エイリアスは透過的です - `typeof()`はエイリアスではなく基底の型名を返します。

## 型システムの制限

現在の制限：

- **関数のジェネリクスなし** - 関数の型パラメータは未サポート
- **ユニオン型なし** - 「AまたはB」を表現できない
- **Nullable型なし** - すべての型はnullになりうる（明示的なnullabilityには`?`サフィックスを使用）

**注意：** コンパイラ（`hemlockc`）はコンパイル時型チェックを提供します。インタープリタは実行時型チェックのみを行います。詳細は[コンパイラドキュメント](../design/implementation.md)を参照してください。

## ベストプラクティス

### 型注釈を使用するタイミング

**注釈を使用するケース：**
- 正確な型が重要（例：バイト値の`u8`）
- 関数インターフェースのドキュメント化
- 制約の強制（例：範囲チェック）

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // 実装
}
```

**注釈を使用しないケース：**
- リテラルから型が明らか
- 内部実装の詳細
- 不要な形式的記述

```hemlock
// 不要
let x: i32 = 42;

// より良い
let x = 42;
```

### 型安全パターン

**使用前にチェック：**
```hemlock
if (typeof(value) == "i32") {
    // i32として安全に使用可能
}
```

**関数引数の検証：**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "arguments must be integers";
    }
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

**柔軟性のためにダック型を使用：**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## 次のステップ

- [文字列](strings.md) - UTF-8文字列型と操作
- [ルーン](runes.md) - Unicodeコードポイント型
- [配列](arrays.md) - 動的配列型
- [オブジェクト](objects.md) - オブジェクトリテラルとダック型
- [メモリ](memory.md) - ポインタとバッファ型
