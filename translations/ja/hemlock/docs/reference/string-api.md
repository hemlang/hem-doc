# 文字列APIリファレンス

Hemlockの文字列型と全22個の文字列メソッドの完全なリファレンスです。

---

## 概要

Hemlockの文字列は**UTF-8エンコード、可変、ヒープ割り当て**されるシーケンスであり、完全なUnicodeサポートを提供します。すべての操作は**コードポイント**（文字）で動作し、バイトではありません。

**主な機能：**
- UTF-8エンコーディング（U+0000からU+10FFFF）
- 可変（文字をその場で変更可能）
- コードポイントベースのインデックス
- 22個の組み込みメソッド
- `+`演算子での自動連結

---

## 文字列型

**型：** `string`

**プロパティ：**
- `.length` - コードポイント数（文字数）
- `.byte_length` - UTF-8バイト数

**リテラル構文：** ダブルクォート `"text"`

**例：**
```hemlock
let s = "hello";
print(s.length);        // 5（コードポイント）
print(s.byte_length);   // 5（バイト）

let emoji = "🚀";
print(emoji.length);        // 1（1つのコードポイント）
print(emoji.byte_length);   // 4（4つのUTF-8バイト）
```

---

## インデックス

文字列は`[]`を使用したコードポイントベースのインデックスをサポートします：

**読み取りアクセス：**
```hemlock
let s = "hello";
let ch = s[0];          // rune 'h'を返す
```

**書き込みアクセス：**
```hemlock
let s = "hello";
s[0] = 'H';             // runeで変更（"Hello"になる）
```

**UTF-8の例：**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀'（1つのコードポイント）
print(text[3]);         // '!'
```

---

## 連結

`+`演算子を使用して文字列とruneを連結します：

**文字列 + 文字列：**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**文字列 + Rune：**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Rune + 文字列：**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**複数の連結：**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## 文字列プロパティ

### .length

Unicodeコードポイント（文字）の数を取得します。

**型：** `i32`

**例：**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1（1つのコードポイント）

let text = "Hello 🌍!";
print(text.length);     // 8（7 ASCII + 1絵文字）
```

---

### .byte_length

UTF-8バイト数を取得します。

**型：** `i32`

**例：**
```hemlock
let s = "hello";
print(s.byte_length);   // 5（ASCII文字1つにつき1バイト）

let emoji = "🚀";
print(emoji.byte_length); // 4（絵文字は4 UTF-8バイト）

let text = "Hello 🌍!";
print(text.byte_length);  // 11（7 ASCII + 絵文字4）
```

---

## 文字列メソッド

### 部分文字列とスライス

#### substr

位置と長さで部分文字列を抽出します。

**シグネチャ：**
```hemlock
string.substr(start: i32, length: i32): string
```

**パラメータ：**
- `start` - 開始コードポイントインデックス（0ベース）
- `length` - 抽出するコードポイント数

**戻り値：** 新しい文字列

**例：**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// UTF-8の例
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

範囲で部分文字列を抽出します（終了は含まない）。

**シグネチャ：**
```hemlock
string.slice(start: i32, end: i32): string
```

**パラメータ：**
- `start` - 開始コードポイントインデックス（0ベース）
- `end` - 終了コードポイントインデックス（含まない）

**戻り値：** 新しい文字列

**例：**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// UTF-8の例
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### 検索と検出

#### find

部分文字列の最初の出現位置を見つけます。

**シグネチャ：**
```hemlock
string.find(needle: string): i32
```

**パラメータ：**
- `needle` - 検索する部分文字列

**戻り値：** 最初の出現のコードポイントインデックス、見つからない場合は`-1`

**例：**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1（見つからない）
let pos3 = s.find("l");         // 2（最初の'l'）
```

---

#### contains

文字列が部分文字列を含むかチェックします。

**シグネチャ：**
```hemlock
string.contains(needle: string): bool
```

**パラメータ：**
- `needle` - 検索する部分文字列

**戻り値：** 見つかった場合は`true`、それ以外は`false`

**例：**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### 分割と結合

#### split

区切り文字で文字列を配列に分割します。

**シグネチャ：**
```hemlock
string.split(delimiter: string): array
```

**パラメータ：**
- `delimiter` - 分割する文字列

**戻り値：** 文字列の配列

**例：**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

先頭と末尾の空白を削除します。

**シグネチャ：**
```hemlock
string.trim(): string
```

**戻り値：** 空白が削除された新しい文字列

**例：**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

---

#### trim_start

先頭の空白を削除します。

**シグネチャ：**
```hemlock
string.trim_start(): string
```

**戻り値：** 先頭の空白が削除された新しい文字列

**例：**
```hemlock
let s = "  hello  ";
let clean = s.trim_start();     // "hello  "

let text = "\n\t  world  \n";
let clean2 = text.trim_start(); // "world  \n"
```

---

#### trim_end

末尾の空白を削除します。

**シグネチャ：**
```hemlock
string.trim_end(): string
```

**戻り値：** 末尾の空白が削除された新しい文字列

**例：**
```hemlock
let s = "  hello  ";
let clean = s.trim_end();       // "  hello"

let text = "\n\t  world  \n";
let clean2 = text.trim_end();   // "\n\t  world"
```

---

### 大文字小文字変換

#### to_upper

文字列を大文字に変換します。

**シグネチャ：**
```hemlock
string.to_upper(): string
```

**戻り値：** 大文字の新しい文字列

**例：**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

文字列を小文字に変換します。

**シグネチャ：**
```hemlock
string.to_lower(): string
```

**戻り値：** 小文字の新しい文字列

**例：**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### 接頭辞と接尾辞

#### starts_with

文字列が接頭辞で始まるかチェックします。

**シグネチャ：**
```hemlock
string.starts_with(prefix: string): bool
```

**パラメータ：**
- `prefix` - チェックする接頭辞

**戻り値：** 文字列が接頭辞で始まる場合は`true`、それ以外は`false`

**例：**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

文字列が接尾辞で終わるかチェックします。

**シグネチャ：**
```hemlock
string.ends_with(suffix: string): bool
```

**パラメータ：**
- `suffix` - チェックする接尾辞

**戻り値：** 文字列が接尾辞で終わる場合は`true`、それ以外は`false`

**例：**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### 置換

#### replace

部分文字列の最初の出現を置換します。

**シグネチャ：**
```hemlock
string.replace(old: string, new: string): string
```

**パラメータ：**
- `old` - 置換する部分文字列
- `new` - 置換文字列

**戻り値：** 最初の出現が置換された新しい文字列

**例：**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo"（最初のみ）
```

---

#### replace_all

部分文字列のすべての出現を置換します。

**シグネチャ：**
```hemlock
string.replace_all(old: string, new: string): string
```

**パラメータ：**
- `old` - 置換する部分文字列
- `new` - 置換文字列

**戻り値：** すべての出現が置換された新しい文字列

**例：**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### 繰り返し

#### repeat

文字列をn回繰り返します。

**シグネチャ：**
```hemlock
string.repeat(count: i32): string
```

**パラメータ：**
- `count` - 繰り返し回数

**戻り値：** count回繰り返された新しい文字列

**例：**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### 文字アクセス

#### char_at

インデックスのUnicodeコードポイントを取得します。

**シグネチャ：**
```hemlock
string.char_at(index: i32): rune
```

**パラメータ：**
- `index` - コードポイントインデックス（0ベース）

**戻り値：** Rune（Unicodeコードポイント）

**例：**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// UTF-8の例
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680（ロケット）
```

---

#### chars

文字列をruneの配列に変換します。

**シグネチャ：**
```hemlock
string.chars(): array
```

**戻り値：** runeの配列（コードポイント）

**例：**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// UTF-8の例
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### バイトアクセス

#### byte_at

インデックスのバイト値を取得します。

**シグネチャ：**
```hemlock
string.byte_at(index: i32): u8
```

**パラメータ：**
- `index` - バイトインデックス（0ベース、コードポイントインデックスではない）

**戻り値：** バイト値（u8）

**例：**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104（ASCII 'h'）
let byte2 = s.byte_at(1);       // 101（ASCII 'e'）

// UTF-8の例
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240（最初のUTF-8バイト）
```

---

#### bytes

文字列をバイトの配列に変換します。

**シグネチャ：**
```hemlock
string.bytes(): array
```

**戻り値：** u8バイトの配列

**例：**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// UTF-8の例
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128]（4 UTF-8バイト）
```

---

#### to_bytes

文字列をバッファに変換します。

**シグネチャ：**
```hemlock
string.to_bytes(): buffer
```

**戻り値：** UTF-8バイトを含むバッファ

**例：**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// UTF-8の例
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**注意：** これはレガシーメソッドです。ほとんどの場合は`.bytes()`を使用してください。

---

### 生ポインタアクセス

#### byte_ptr

文字列の内部UTF-8バイトバッファへの生ポインタを取得します。これはゼロアロケーション操作で、コピーは作成されません。

**シグネチャ：**
```hemlock
string.byte_ptr(): ptr
```

**戻り値：** 文字列の内部UTF-8バイトへの生ポインタ（`ptr`）

**例：**
```hemlock
let s = "Hello";
let p = s.byte_ptr();
print(typeof(p));              // "ptr"

// ポインタを通じてバイトを読み取り
print(ptr_deref_u8(p));                    // 72 ('H')
print(ptr_deref_u8(ptr_offset(p, 1, 1))); // 101 ('e')
print(ptr_deref_u8(ptr_offset(p, 4, 1))); // 111 ('o')

// memcpyで文字列バイトをコピー
let buf = alloc(5);
memcpy(buf, s.byte_ptr(), 5);
print(ptr_deref_u8(buf));  // 72
free(buf);

// .byte_lengthと組み合わせて安全なサイズ追跡
let emoji = "Hello 🚀";
let ep = emoji.byte_ptr();
print(emoji.byte_length);  // 10（バイト操作にはlengthではなくbyte_lengthを使用）
```

**動作：**
- 文字列の内部メモリへのポインタを直接返す（ゼロコピー）
- ポインタは文字列が生存中かつ未変更の間有効
- ポインタを通じてアクセス可能なバイト数を決定するには`.byte_length`（`.length`ではなく）を使用
- `.to_bytes()`と異なり、新しいバッファを割り当てない

**使用ケース：**
- 文字列データへのポインタが必要なFFI呼び出し
- C関数とのゼロコピー相互運用
- アロケーションを回避するパフォーマンス重視のコード

**警告：** `byte_ptr()`呼び出し後に文字列を変更すると（例：インデックス代入）、文字列の内部バッファが再割り当てされた場合にポインタが無効になる可能性があります。

---

### JSONデシリアライズ

#### deserialize

JSON文字列を値にパースします。

**シグネチャ：**
```hemlock
string.deserialize(): any
```

**戻り値：** パースされた値（オブジェクト、配列、数値、文字列、bool、またはnull）

**例：**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**サポートされる型：**
- オブジェクト：`{"key": value}`
- 配列：`[1, 2, 3]`
- 数値：`42`、`3.14`
- 文字列：`"text"`
- ブーリアン：`true`、`false`
- Null：`null`

**関連項目：** オブジェクトの`.serialize()`メソッド

---

## メソッドチェーン

文字列メソッドは簡潔な操作のためにチェーンできます：

**例：**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## 完全なメソッド要約

| メソッド | シグネチャ | 戻り値 | 説明 |
|----------------|----------------------------------------------|-----------|---------------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`  | 位置/長さで部分文字列を抽出 |
| `slice`        | `(start: i32, end: i32)`                     | `string`  | 範囲で部分文字列を抽出 |
| `find`         | `(needle: string)`                           | `i32`     | 最初の出現を見つける（見つからない場合-1）|
| `contains`     | `(needle: string)`                           | `bool`    | 部分文字列を含むかチェック |
| `split`        | `(delimiter: string)`                        | `array`   | 配列に分割 |
| `trim`         | `()`                                         | `string`  | 空白を削除 |
| `trim_start`   | `()`                                         | `string`  | 先頭の空白を削除 |
| `trim_end`     | `()`                                         | `string`  | 末尾の空白を削除 |
| `to_upper`     | `()`                                         | `string`  | 大文字に変換 |
| `to_lower`     | `()`                                         | `string`  | 小文字に変換 |
| `starts_with`  | `(prefix: string)`                           | `bool`    | 接頭辞で始まるかチェック |
| `ends_with`    | `(suffix: string)`                           | `bool`    | 接尾辞で終わるかチェック |
| `replace`      | `(old: string, new: string)`                 | `string`  | 最初の出現を置換 |
| `replace_all`  | `(old: string, new: string)`                 | `string`  | すべての出現を置換 |
| `repeat`       | `(count: i32)`                               | `string`  | 文字列をn回繰り返す |
| `char_at`      | `(index: i32)`                               | `rune`    | インデックスのコードポイントを取得 |
| `byte_at`      | `(index: i32)`                               | `u8`      | インデックスのバイトを取得 |
| `chars`        | `()`                                         | `array`   | runeの配列に変換 |
| `bytes`        | `()`                                         | `array`   | バイトの配列に変換 |
| `to_bytes`     | `()`                                         | `buffer`  | バッファに変換（レガシー） |
| `byte_ptr`     | `()`                                         | `ptr`     | 内部UTF-8バイトへの生ポインタ |
| `deserialize`  | `()`                                         | `any`     | JSON文字列をパース |

---

## 関連項目

- [型システム](type-system.md) - 文字列型の詳細
- [配列API](array-api.md) - split()結果の配列メソッド
- [演算子](operators.md) - 文字列連結演算子
