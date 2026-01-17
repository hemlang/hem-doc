# 型システムリファレンス

Hemlockの型システムの完全なリファレンスです。すべてのプリミティブ型と複合型を含みます。

---

## 概要

Hemlockは実行時型タグとオプションの型注釈を持つ**動的型システム**を使用します。すべての値は実行時型を持ち、型変換は明示的な昇格規則に従います。

**主な機能：**
- 実行時型チェック（インタプリタ）
- コンパイル時型チェック（hemlockc - デフォルトで有効）
- オプションの型注釈
- リテラルの自動型推論
- 明示的な型昇格規則
- 精度を失う暗黙的変換なし

---

## コンパイル時型チェック（hemlockc）

Hemlockコンパイラ（`hemlockc`）には、実行可能ファイル生成前にコードを検証するコンパイル時型チェッカーが含まれています。これにより、プログラムを実行せずに型エラーを早期に発見できます。

### デフォルトの動作

型チェックはhemloccで**デフォルトで有効**です：

```bash
# 型チェックは自動的に行われる
hemlockc program.hml -o program

# エラーはコンパイル前に報告される
hemlockc bad_types.hml
# 出力：1 type error found
```

### コンパイラフラグ

| フラグ | 説明 |
|------|-------------|
| `--check` | 型チェックのみ、コンパイルしない（検証後に終了） |
| `--no-type-check` | 型チェックを無効化（推奨されない） |
| `--strict-types` | より厳格な型警告を有効化 |

**例：**

```bash
# コンパイルせずに型のみ検証
hemlockc --check program.hml
# 出力：program.hml: no type errors

# 型チェックを無効化（注意して使用）
hemlockc --no-type-check dynamic_code.hml -o program

# 暗黙のany型に対する厳格な警告を有効化
hemlockc --strict-types program.hml -o program
```

### 型チェッカーが検証する内容

1. **型注釈** - 代入された値が宣言された型と一致することを保証
2. **関数呼び出し** - 引数の型がパラメータの型と一致することを検証
3. **戻り値の型** - return文が宣言された戻り値の型と一致することをチェック
4. **演算子の使用** - オペランドが互換性があることを検証
5. **プロパティアクセス** - 型付きオブジェクトのオブジェクトフィールドの型を検証

### 許容的な数値変換

型チェッカーはコンパイル時に数値型の変換を許可し、範囲の検証は実行時に行われます：

```hemlock
let x: i8 = 100;      // OK - 100はi8に収まる（実行時に検証）
let y: u8 = 255;      // OK - u8の範囲内
let z: f64 = 42;      // OK - i32からf64は安全
```

### 動的コードのサポート

型注釈のないコードは動的（`any`型）として扱われ、常に型チェッカーを通過します：

```hemlock
let x = get_value();  // 動的 - 注釈なし
process(x);           // OK - 動的な値はどこでも受け入れられる
```

---

## プリミティブ型

### 数値型

#### 符号付き整数

| 型 | サイズ | 範囲 | エイリアス |
|--------|---------|-------------------------------------------|-----------|
| `i8`   | 1バイト | -128から127 | - |
| `i16`  | 2バイト | -32,768から32,767 | - |
| `i32`  | 4バイト | -2,147,483,648から2,147,483,647 | `integer` |
| `i64`  | 8バイト | -9,223,372,036,854,775,808から9,223,372,036,854,775,807 | - |

**例：**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// 型エイリアス
let x: integer = 42;  // i32と同じ
```

#### 符号なし整数

| 型 | サイズ | 範囲 | エイリアス |
|--------|---------|---------------------------|--------|
| `u8`   | 1バイト | 0から255 | `byte` |
| `u16`  | 2バイト | 0から65,535 | - |
| `u32`  | 4バイト | 0から4,294,967,295 | - |
| `u64`  | 8バイト | 0から18,446,744,073,709,551,615 | - |

**例：**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// 型エイリアス
let byte_val: byte = 65;  // u8と同じ
```

#### 浮動小数点

| 型 | サイズ | 精度 | エイリアス |
|--------|---------|----------------|----------|
| `f32`  | 4バイト | 約7桁 | - |
| `f64`  | 8バイト | 約15桁 | `number` |

**例：**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// 型エイリアス
let x: number = 2.718;  // f64と同じ
```

---

### 整数リテラルの推論

整数リテラルはその値に基づいて自動的に型付けされます：

**規則：**
- i32範囲（-2,147,483,648から2,147,483,647）内の値：`i32`として推論
- i32範囲外だがi64範囲内の値：`i64`として推論
- 他の型（i8、i16、u8、u16、u32、u64）には明示的な型注釈を使用

**例：**
```hemlock
let small = 42;                    // i32（i32に収まる）
let large = 5000000000;            // i64（> i32最大値）
let max_i64 = 9223372036854775807; // i64（INT64_MAX）
let explicit: u32 = 100;           // u32（型注釈で上書き）
```

---

### ブーリアン型

**型：** `bool`

**値：** `true`、`false`

**サイズ：** 1バイト（内部的に）

**例：**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("working");
}
```

---

### 文字型

#### Rune

**型：** `rune`

**説明：** Unicodeコードポイント（U+0000からU+10FFFF）

**サイズ：** 4バイト（32ビット値）

**範囲：** 0から0x10FFFF（1,114,111）

**リテラル構文：** シングルクォート `'x'`

**例：**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// マルチバイトUTF-8
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// エスケープシーケンス
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Unicodeエスケープ
let emoji = '\u{1F680}';   // 最大6桁の16進数
let max = '\u{10FFFF}';    // 最大コードポイント
```

**型変換：**
```hemlock
// 整数からrune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// runeから整数
let value: i32 = 'Z';       // 90

// runeから文字列
let s: string = 'H';        // "H"

// u8からrune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**関連項目：** 文字列 + rune連結については[文字列API](string-api.md)

---

### 文字列型

**型：** `string`

**説明：** UTF-8エンコード、可変、ヒープ割り当てのテキスト

**エンコーディング：** UTF-8（U+0000からU+10FFFF）

**可変性：** 可変（ほとんどの言語と異なる）

**プロパティ：**
- `.length` - コードポイント数（文字数）
- `.byte_length` - バイト数（UTF-8エンコーディングサイズ）

**リテラル構文：** ダブルクォート `"text"`

**例：**
```hemlock
let s = "hello";
s[0] = 'H';             // 変更（"Hello"になる）
print(s.length);        // 5（コードポイント数）
print(s.byte_length);   // 5（UTF-8バイト数）

let emoji = "🚀";
print(emoji.length);        // 1（1つのコードポイント）
print(emoji.byte_length);   // 4（4つのUTF-8バイト）
```

**インデックス：**
```hemlock
let s = "hello";
let ch = s[0];          // rune 'h'を返す
s[0] = 'H';             // runeで設定
```

**関連項目：** 完全なメソッドリファレンスは[文字列API](string-api.md)

---

### Null型

**型：** `null`

**説明：** null値（値の不在）

**サイズ：** 8バイト（内部的に）

**値：** `null`

**例：**
```hemlock
let x = null;
let y: i32 = null;  // エラー：型の不一致

if (x == null) {
    print("x is null");
}
```

---

## 複合型

### 配列型

**型：** `array`

**説明：** 動的、ヒープ割り当て、混合型の配列

**プロパティ：**
- `.length` - 要素数

**ゼロインデックス：** はい

**リテラル構文：** `[elem1, elem2, ...]`

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// 混合型
let mixed = [1, "hello", true, null];
```

**関連項目：** 完全なメソッドリファレンスは[配列API](array-api.md)

---

### オブジェクト型

**型：** `object`

**説明：** 動的フィールドを持つJavaScriptスタイルのオブジェクト

**リテラル構文：** `{ field: value, ... }`

**例：**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// フィールドを動的に追加
person.email = "alice@example.com";
```

**型定義：**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // オプションフィールド
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### ポインタ型

#### 生ポインタ（ptr）

**型：** `ptr`

**説明：** 生メモリアドレス（安全でない）

**サイズ：** 8バイト

**境界チェック：** なし

**例：**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### バッファ（buffer）

**型：** `buffer`

**説明：** 境界チェック付きの安全なポインタラッパー

**構造：** ポインタ + 長さ + 容量

**プロパティ：**
- `.length` - バッファサイズ
- `.capacity` - 割り当て容量

**例：**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // 境界チェックあり
print(b.length);        // 64
free(b);
```

**関連項目：** 割り当て関数は[メモリAPI](memory-api.md)

---

## 特殊型

### ファイル型

**型：** `file`

**説明：** I/O操作用のファイルハンドル

**プロパティ：**
- `.path` - ファイルパス（string）
- `.mode` - オープンモード（string）
- `.closed` - ファイルがクローズされているか（bool）

**関連項目：** [ファイルAPI](file-api.md)

---

### タスク型

**型：** `task`

**説明：** 並行タスクのハンドル

**関連項目：** [並行性API](concurrency-api.md)

---

### チャネル型

**型：** `channel`

**説明：** スレッドセーフな通信チャネル

**関連項目：** [並行性API](concurrency-api.md)

---

### 関数型

**型：** `function`

**説明：** ファーストクラスの関数値

**例：**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Void型

**型：** `void`

**説明：** 戻り値の不在（内部使用）

---

## 型昇格規則

操作で型を混合する場合、Hemlockは「より高い」型に昇格します：

**昇格階層：**
```
f64（最高精度）
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8（最低）
```

**規則：**
1. 浮動小数点は常に整数に勝つ
2. 同じカテゴリ（int/uint/float）内ではより大きいサイズが勝つ
3. 両方のオペランドが結果の型に昇格される
4. **精度保持：** i64/u64 + f32はf64に昇格（f32ではない）

**例：**
```hemlock
// サイズ昇格
u8 + i32    → i32    // より大きいサイズが勝つ
i32 + i64   → i64    // より大きいサイズが勝つ
u32 + u64   → u64    // より大きいサイズが勝つ

// 浮動小数点昇格
i32 + f32   → f32    // 浮動小数点が勝つ、f32はi32に十分
i64 + f32   → f64    // i64の精度を保持するためf64に昇格
i64 + f64   → f64    // 浮動小数点は常に勝つ
i8 + f64    → f64    // 浮動小数点 + 最大が勝つ
```

**なぜi64 + f32 → f64なのか？**

f32は24ビットの仮数しかなく、2^24（16,777,216）より大きい整数を正確に表現できません。i64は2^63までの値を保持できるため、i64とf32を混合すると深刻な精度損失が発生します。Hemlockは代わりにf64（53ビット仮数）に昇格します。

---

## 範囲チェック

型注釈は代入時に範囲チェックを強制します：

**有効な代入：**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**無効な代入（実行時エラー）：**
```hemlock
let x: u8 = 256;             // エラー：範囲外
let y: i8 = 128;             // エラー：最大は127
let z: u64 = -1;             // エラー：u64は負にできない
```

---

## 型イントロスペクション

### typeof(value)

値の型名を文字列として返します。

**シグネチャ：**
```hemlock
typeof(value: any): string
```

**戻り値：**
- プリミティブ型：`"i8"`、`"i16"`、`"i32"`、`"i64"`、`"u8"`、`"u16"`、`"u32"`、`"u64"`、`"f32"`、`"f64"`、`"bool"`、`"string"`、`"rune"`、`"null"`
- 複合型：`"array"`、`"object"`、`"ptr"`、`"buffer"`、`"function"`
- 特殊型：`"file"`、`"task"`、`"channel"`
- 型付きオブジェクト：カスタム型名（例：`"Person"`）

**例：**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**関連項目：** [組み込み関数](builtins.md#typeof)

---

## 型変換

### 暗黙的変換

Hemlockは型昇格規則に従って算術操作で暗黙的な型変換を行います。

**例：**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // resultはi32（昇格される）
```

### 明示的変換

明示的な変換には型注釈を使用します：

**例：**
```hemlock
// 整数から浮動小数点
let i: i32 = 42;
let f: f64 = i;         // 42.0

// 浮動小数点から整数（切り詰め）
let x: f64 = 3.14;
let y: i32 = x;         // 3

// 整数からrune
let code: rune = 65;    // 'A'

// runeから整数
let value: i32 = 'Z';   // 90

// runeから文字列
let s: string = 'H';    // "H"
```

---

## 型エイリアス

### 組み込みエイリアス

Hemlockは一般的な型の組み込み型エイリアスを提供します：

| エイリアス | 実際の型 | 用途 |
|-----------|-------------|--------------------------|
| `integer` | `i32`       | 汎用整数 |
| `number`  | `f64`       | 汎用浮動小数点 |
| `byte`    | `u8`        | バイト値 |

**例：**
```hemlock
let count: integer = 100;       // i32と同じ
let price: number = 19.99;      // f64と同じ
let b: byte = 255;              // u8と同じ
```

### カスタム型エイリアス

`type`キーワードを使用してカスタム型エイリアスを定義：

```hemlock
// シンプルなエイリアス
type Integer = i32;
type Text = string;

// 関数型エイリアス
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// 複合型エイリアス
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// ジェネリック型エイリアス
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**カスタムエイリアスの使用：**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**注意：** 型エイリアスは透過的です - `typeof()`は基礎となる型名を返します。

---

## 関数型

関数型は関数値のシグネチャを指定します：

### 構文

```hemlock
fn(param_types): return_type
```

### 例

```hemlock
// 基本的な関数型
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// 関数パラメータ
fn apply(f: fn(i32): i32, x: i32): i32 {
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
```

---

## 複合型（交差型）

複合型は`&`を使用して複数の型制約を要求します：

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// オブジェクトはすべての型を満たす必要がある
let person: HasName & HasAge = { name: "Alice", age: 30 };

// 3つ以上の型
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## 要約表

| 型 | サイズ | 可変 | ヒープ割り当て | 説明 |
|------------|----------|---------|----------------|--------------------------------|
| `i8`-`i64` | 1-8バイト | いいえ | いいえ | 符号付き整数 |
| `u8`-`u64` | 1-8バイト | いいえ | いいえ | 符号なし整数 |
| `f32`      | 4バイト | いいえ | いいえ | 単精度浮動小数点 |
| `f64`      | 8バイト | いいえ | いいえ | 倍精度浮動小数点 |
| `bool`     | 1バイト | いいえ | いいえ | ブーリアン |
| `rune`     | 4バイト | いいえ | いいえ | Unicodeコードポイント |
| `string`   | 可変 | はい | はい | UTF-8テキスト |
| `array`    | 可変 | はい | はい | 動的配列 |
| `object`   | 可変 | はい | はい | 動的オブジェクト |
| `ptr`      | 8バイト | いいえ | いいえ | 生ポインタ |
| `buffer`   | 可変 | はい | はい | 安全なポインタラッパー |
| `file`     | 不透明 | はい | はい | ファイルハンドル |
| `task`     | 不透明 | いいえ | はい | 並行タスクハンドル |
| `channel`  | 不透明 | はい | はい | スレッドセーフチャネル |
| `function` | 不透明 | いいえ | はい | 関数値 |
| `null`     | 8バイト | いいえ | いいえ | Null値 |

---

## 関連項目

- [演算子リファレンス](operators.md) - 操作での型の動作
- [組み込み関数](builtins.md) - 型イントロスペクションと変換
- [文字列API](string-api.md) - 文字列型メソッド
- [配列API](array-api.md) - 配列型メソッド
- [メモリAPI](memory-api.md) - ポインタとバッファ操作
