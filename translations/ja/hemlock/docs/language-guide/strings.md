# 文字列

Hemlock文字列は、完全なUnicodeサポートとテキスト処理のための豊富なメソッドセットを備えた**UTF-8ファーストクラスのミュータブルシーケンス**です。多くの言語とは異なり、Hemlock文字列はミュータブルで、Unicodeコードポイントとネイティブに連携します。

## 概要

```hemlock
let s = "hello";
s[0] = 'H';             // ルーンで変更（"Hello"になる）
print(s.length);        // 5（コードポイント数）
let c = s[0];           // ルーン（Unicodeコードポイント）を返す
let msg = s + " world"; // 連結
let emoji = "🚀";
print(emoji.length);    // 1（1つのコードポイント）
print(emoji.byte_length); // 4（4つのUTF-8バイト）
```

## プロパティ

Hemlock文字列の主な特徴：

- **UTF-8エンコード** - 完全なUnicodeサポート（U+0000からU+10FFFF）
- **ミュータブル** - Python、JavaScript、Java文字列とは異なる
- **コードポイントベースのインデックス** - バイトではなく`rune`（Unicodeコードポイント）を返す
- **ヒープ割り当て** - 内部容量追跡付き
- **2つのlengthプロパティ**：
  - `.length` - コードポイント数（文字数）
  - `.byte_length` - バイト数（UTF-8エンコーディングサイズ）

## UTF-8の動作

すべての文字列操作はバイトではなく**コードポイント**（文字）で動作：

```hemlock
let text = "Hello🚀World";
print(text.length);        // 11（コードポイント）
print(text.byte_length);   // 15（バイト、絵文字は4バイト）

// インデックスはコードポイントを使用
let h = text[0];           // 'H'（ルーン）
let rocket = text[5];      // '🚀'（ルーン）
```

**マルチバイト文字は1としてカウント：**
```hemlock
"Hello".length;      // 5
"🚀".length;         // 1（1つの絵文字）
"你好".length;       // 2（2つの中国語文字）
"café".length;       // 4（éは1つのコードポイント）
```

## 文字列リテラル

```hemlock
// 基本的な文字列
let s1 = "hello";
let s2 = "world";

// エスケープシーケンス付き
let s3 = "Line 1\nLine 2\ttabbed";
let s4 = "Quote: \"Hello\"";
let s5 = "Backslash: \\";

// Unicode文字
let s6 = "🚀 Emoji";
let s7 = "中文字符";
```

## テンプレート文字列（文字列補間）

埋め込み式のためにバッククォートを使用：

```hemlock
let name = "Alice";
let age = 30;

// 基本的な補間
let greeting = `Hello, ${name}!`;           // "Hello, Alice!"
let info = `${name} is ${age} years old`;   // "Alice is 30 years old"

// 補間内の式
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// メソッド呼び出し
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// ネストされたオブジェクト
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lives in ${person.city}`;  // "Bob lives in NYC"

// 複数行（改行を保持）
let multi = `Line 1
Line 2
Line 3`;
```

**テンプレート文字列の機能：**
- `${...}`内の式は評価されて文字列に変換される
- 任意の有効な式が使用可能（変数、関数呼び出し、算術）
- バッククォート文字列は通常の文字列と同じエスケープシーケンスをサポート
- 連結なしで動的文字列を構築するのに便利

### テンプレート文字列内のエスケープ

テンプレート文字列にリテラルの`${`を含めるには、ドル記号をエスケープ：

```hemlock
let price = 100;
let text = `Price: \${price} or ${price}`;
// "Price: ${price} or 100"

// リテラルのバッククォート
let code = `Use \` for template strings`;
// "Use ` for template strings"
```

### 複雑な式

テンプレート文字列には任意の有効な式を含めることが可能：

```hemlock
// 三項演算子のような式
let age = 25;
let status = `Status: ${age >= 18 ? "adult" : "minor"}`;

// 配列アクセス
let items = ["apple", "banana", "cherry"];
let first = `First item: ${items[0]}`;

// 引数付き関数呼び出し
fn format_price(p) { return "$" + p; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: $99.99"

// チェーンメソッド呼び出し
let name = "alice";
let formatted = `Hello, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hello, Alice!"
```

### テンプレート文字列 vs 連結

テンプレート文字列は連結より読みやすいことが多い：

```hemlock
// 連結（読みにくい）
let msg1 = "Hello, " + name + "! You have " + count + " messages.";

// テンプレート文字列（読みやすい）
let msg2 = `Hello, ${name}! You have ${count} messages.`;
```

## インデックスと変更

### 文字の読み取り

インデックスは`rune`（Unicodeコードポイント）を返す：

```hemlock
let s = "Hello";
let first = s[0];      // 'H'（ルーン）
let last = s[4];       // 'o'（ルーン）

// UTF-8の例
let emoji = "Hi🚀!";
let rocket = emoji[2];  // '🚀'（コードポイントインデックス2のルーン）
```

### 文字の書き込み

文字列はミュータブル - 個々の文字を変更可能：

```hemlock
let s = "hello";
s[0] = 'H';            // "Hello"になる
s[4] = '!';            // "Hell!"になる

// Unicodeで
let msg = "Go!";
msg[0] = '🚀';         // "🚀o!"になる
```

## 連結

`+`を使用して文字列を連結：

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// 変数で
let name = "Alice";
let msg = "Hi, " + name + "!";  // "Hi, Alice!"

// ルーンと（ルーンのドキュメントを参照）
let s = "Hello" + '!';          // "Hello!"
```

## 文字列メソッド

Hemlockは包括的なテキスト操作のための19個の文字列メソッドを提供します。

### 部分文字列とスライス

**`substr(start, length)`** - 位置と長さで部分文字列を抽出：
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"（6から始めて長さ5）
let first = s.substr(0, 5);     // "hello"

// UTF-8の例
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"（位置2、長さ1）
```

**`slice(start, end)`** - 範囲で部分文字列を抽出（endを含まない）：
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello"（インデックス0から4）
let slice2 = s.slice(6, 11);    // "world"
```

**違い：**
- `substr(start, length)` - 長さパラメータを使用
- `slice(start, end)` - 終了インデックスを使用（含まない）

### 検索

**`find(needle)`** - 最初の出現位置を検索：
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6（最初の出現のインデックス）
let pos2 = s.find("foo");       // -1（見つからない）
let pos3 = s.find("l");         // 2（最初の'l'）
```

**`contains(needle)`** - 文字列が部分文字列を含むかチェック：
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### 分割とトリム

**`split(delimiter)`** - 文字列の配列に分割：
```hemlock
let csv = "apple,banana,cherry";
let parts = csv.split(",");     // ["apple", "banana", "cherry"]

let words = "one two three".split(" ");  // ["one", "two", "three"]

// 空の区切り文字は文字ごとに分割
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - 先頭と末尾の空白を削除：
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### 大文字小文字変換

**`to_upper()`** - 大文字に変換：
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// 非ASCIIを保持
let s2 = "café";
let upper2 = s2.to_upper();     // "CAFÉ"
```

**`to_lower()`** - 小文字に変換：
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### 接頭辞/接尾辞チェック

**`starts_with(prefix)`** - 接頭辞で始まるかチェック：
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - 接尾辞で終わるかチェック：
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### 置換

**`replace(old, new)`** - 最初の出現を置換：
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo"（最初のみ）
```

**`replace_all(old, new)`** - すべての出現を置換：
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### 繰り返し

**`repeat(count)`** - 文字列をn回繰り返す：
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### 文字とバイトアクセス

**`char_at(index)`** - インデックスのUnicodeコードポイントを取得（ルーンを返す）：
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h'（ルーン）

// UTF-8の例
let emoji = "🚀";
let rocket = emoji.char_at(0);  // ルーン U+1F680を返す
```

**`chars()`** - ルーン（コードポイント）の配列に変換：
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']（ルーンの配列）

// UTF-8の例
let text = "Hi🚀";
let chars2 = text.chars();      // ['H', 'i', '🚀']
```

**`byte_at(index)`** - インデックスのバイト値を取得（u8を返す）：
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104（'h'のASCII値）

// UTF-8の例
let emoji = "🚀";
let first_byte = emoji.byte_at(0);  // 240（最初のUTF-8バイト）
```

**`bytes()`** - バイト（u8値）の配列に変換：
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]（u8の配列）

// UTF-8の例
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128]（4つのUTF-8バイト）
```

**`to_bytes()`** - 低レベルアクセス用にバッファに変換：
```hemlock
let s = "hello";
let buf = s.to_bytes();         // UTF-8バイトのバッファを返す
print(buf.length);              // 5
free(buf);                      // 解放を忘れずに
```

## メソッドチェーン

すべての文字列メソッドは新しい文字列を返すため、チェーンが可能：

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## 完全なメソッドリファレンス

| メソッド | パラメータ | 戻り値 | 説明 |
|--------|-----------|---------|-------------|
| `substr(start, length)` | i32, i32 | string | 位置と長さで部分文字列を抽出 |
| `slice(start, end)` | i32, i32 | string | 範囲で部分文字列を抽出（endを含まない） |
| `find(needle)` | string | i32 | 最初の出現を検索（見つからない場合-1） |
| `contains(needle)` | string | bool | 部分文字列を含むかチェック |
| `split(delimiter)` | string | array | 文字列の配列に分割 |
| `trim()` | - | string | 先頭と末尾の空白を削除 |
| `to_upper()` | - | string | 大文字に変換 |
| `to_lower()` | - | string | 小文字に変換 |
| `starts_with(prefix)` | string | bool | 接頭辞で始まるかチェック |
| `ends_with(suffix)` | string | bool | 接尾辞で終わるかチェック |
| `replace(old, new)` | string, string | string | 最初の出現を置換 |
| `replace_all(old, new)` | string, string | string | すべての出現を置換 |
| `repeat(count)` | i32 | string | 文字列をn回繰り返す |
| `char_at(index)` | i32 | rune | インデックスのコードポイントを取得 |
| `byte_at(index)` | i32 | u8 | インデックスのバイト値を取得 |
| `chars()` | - | array | ルーンの配列に変換 |
| `bytes()` | - | array | u8バイトの配列に変換 |
| `to_bytes()` | - | buffer | バッファに変換（解放必須） |

## 例

### 例：テキスト処理

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // 空白を正規化
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### 例：CSVパーサー

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "apple, banana , cherry";
let fields = parse_csv_line(csv);  // ["apple", "banana", "cherry"]
```

### 例：単語カウンター

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "The quick brown fox";
let count = count_words(sentence);  // 4
```

### 例：文字列検証

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## メモリ管理

文字列は内部参照カウントでヒープ割り当て：

- **作成**：容量追跡付きでヒープに割り当て
- **連結**：新しい文字列を作成（古い文字列は変更されない）
- **メソッド**：ほとんどのメソッドは新しい文字列を返す
- **寿命**：文字列は参照カウントされスコープを抜けると自動的に解放

**自動クリーンアップ：**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // 新しい割り当て
}  // 関数が戻るとsとs2の両方が自動的に解放
```

**注意：** ローカル文字列変数はスコープを抜けると自動的にクリーンアップされます。`free()`はスコープ終了前の早期クリーンアップや長期間存続する/グローバルデータにのみ使用してください。詳細は[メモリ管理](memory.md#internal-reference-counting)を参照してください。

## ベストプラクティス

1. **コードポイントインデックスを使用** - 文字列はバイトオフセットではなくコードポイント位置を使用
2. **Unicodeでテスト** - 常にマルチバイト文字で文字列操作をテスト
3. **イミュータブル操作を優先** - 変更より新しい文字列を返すメソッドを使用
4. **境界をチェック** - 文字列のインデックスは境界チェックしない（無効時はnull/エラー）
5. **入力を正規化** - ユーザー入力には`trim()`と`to_lower()`を使用

## よくある落とし穴

### 落とし穴：バイト vs コードポイントの混乱

```hemlock
let emoji = "🚀";
print(emoji.length);        // 1（コードポイント）
print(emoji.byte_length);   // 4（バイト）

// バイトとコードポイントの操作を混ぜない
let byte = emoji.byte_at(0);  // 240（最初のバイト）
let char = emoji.char_at(0);  // '🚀'（完全なコードポイント）
```

### 落とし穴：変更のサプライズ

```hemlock
let s1 = "hello";
let s2 = s1;       // 浅いコピー
s1[0] = 'H';       // s1を変更
print(s2);         // まだ"hello"（文字列は値型）
```

## 関連トピック

- [ルーン](runes.md) - 文字列インデックスで使用されるUnicodeコードポイント型
- [配列](arrays.md) - 文字列メソッドは配列と連携することが多い
- [型](types.md) - 文字列型の詳細と変換

## 参照

- **UTF-8エンコーディング**：CLAUDE.mdの「Strings」セクションを参照
- **型変換**：文字列変換については[型](types.md)を参照
- **メモリ**：文字列割り当ての詳細は[メモリ](memory.md)を参照
