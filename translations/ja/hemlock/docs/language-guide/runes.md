# ルーン

ルーンはHemlockでの文字操作のために、**Unicodeコードポイント**（U+0000からU+10FFFF）を独自の型として表現します。バイト（u8）とは異なり、ルーンはあらゆる言語の文字や絵文字を表現できる完全なUnicode文字です。

## 概要

```hemlock
let ch = 'A';           // ルーンリテラル
let emoji = '🚀';       // マルチバイト文字を1つのルーンとして
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // 文字列 + ルーンの連結
let r = '>' + " msg";   // ルーン + 文字列の連結
```

## ルーンとは？

ルーンはUnicodeコードポイントを表す**32ビットの値**です：

- **範囲：** 0から0x10FFFF（1,114,111個の有効なコードポイント）
- **数値型ではない** - 文字表現に使用
- **u8/charとは異なる** - ルーンは完全なUnicode、u8はただのバイト
- **文字列のインデックスで返される** - `str[0]`はバイトではなくルーンを返す

**なぜルーンか？**
- Hemlock文字列はUTF-8エンコード
- 1つのUnicode文字はUTF-8で1〜4バイト
- ルーンにより、部分的なバイトではなく完全な文字を扱える

## ルーンリテラル

### 基本構文

シングルクォートでルーンリテラルを表記：

```hemlock
let a = 'A';            // ASCII文字
let b = '0';            // 数字文字
let c = '!';            // 句読点
let d = ' ';            // スペース
```

### マルチバイトUTF-8文字

ルーンはあらゆるUnicode文字を表現可能：

```hemlock
// 絵文字
let rocket = '🚀';      // 絵文字（U+1F680）
let heart = '❤';        // ハート（U+2764）
let smile = '😀';       // 笑顔（U+1F600）

// CJK文字
let chinese = '中';     // 中国語（U+4E2D）
let japanese = 'あ';    // ひらがな（U+3042）
let korean = '한';      // ハングル（U+D55C）

// 記号
let check = '✓';        // チェックマーク（U+2713）
let arrow = '→';        // 右矢印（U+2192）
```

### エスケープシーケンス

特殊文字のための一般的なエスケープシーケンス：

```hemlock
let newline = '\n';     // 改行（U+000A）
let tab = '\t';         // タブ（U+0009）
let backslash = '\\';   // バックスラッシュ（U+005C）
let quote = '\'';       // シングルクォート（U+0027）
let dquote = '"';       // ダブルクォート（U+0022）
let null_char = '\0';   // ヌル文字（U+0000）
let cr = '\r';          // キャリッジリターン（U+000D）
```

**利用可能なエスケープシーケンス：**
- `\n` - 改行（ラインフィード）
- `\t` - 水平タブ
- `\r` - キャリッジリターン
- `\0` - ヌル文字
- `\\` - バックスラッシュ
- `\'` - シングルクォート
- `\"` - ダブルクォート

### Unicodeエスケープ

Unicodeコードポイントには`\u{XXXXXX}`構文を使用（最大6桁の16進数）：

```hemlock
let rocket = '\u{1F680}';   // 🚀 Unicodeエスケープで絵文字
let heart = '\u{2764}';     // ❤ ハート
let ascii = '\u{41}';       // 'A' エスケープで
let max = '\u{10FFFF}';     // 最大Unicodeコードポイント

// 先頭のゼロはオプション
let a = '\u{41}';           // '\u{0041}'と同じ
let b = '\u{0041}';
```

**ルール：**
- 範囲：`\u{0}`から`\u{10FFFF}`
- 16進数桁：1から6桁
- 大文字小文字を区別しない：`\u{1F680}`または`\u{1f680}`
- 有効なUnicode範囲外の値はエラー

## 文字列 + ルーンの連結

ルーンは文字列と連結可能：

```hemlock
// 文字列 + ルーン
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Text" + '✓';       // "Text✓"

// ルーン + 文字列
let prefix = '>' + " Message";      // "> Message"
let bullet = '•' + " Item";         // "• Item"

// 複数の連結
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"

// メソッドチェーンも動作
let result = ('>' + " Important").to_upper();  // "> IMPORTANT"
```

**動作の仕組み：**
- ルーンは自動的にUTF-8にエンコード
- 連結時に文字列に変換
- 文字列連結演算子がこれを透過的に処理

## 型変換

ルーンは他の型との間で変換可能。

### 整数 ↔ ルーン

コードポイント値を扱うために整数とルーンの間で変換：

```hemlock
// 整数からルーン（コードポイント値）
let code: rune = 65;            // 'A'（ASCII 65）
let emoji_code: rune = 128640;  // U+1F680（🚀）

// ルーンから整数（コードポイント値を取得）
let r = 'Z';
let value: i32 = r;             // 90（ASCII値）

let rocket = '🚀';
let code: i32 = rocket;         // 128640（U+1F680）
```

**範囲チェック：**
- 整数からルーン：[0, 0x10FFFF]の範囲内である必要がある
- 範囲外の値は実行時エラー
- ルーンから整数：常に成功（コードポイントを返す）

### ルーン → 文字列

ルーンは明示的に文字列に変換可能：

```hemlock
// 明示的な変換
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// 連結時は自動
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8（バイト） → ルーン

任意のu8値（0-255）はルーンに変換可能：

```hemlock
// ASCII範囲（0-127）
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// 拡張ASCII / Latin-1（128-255）
let extended: u8 = 200;
let r: rune = extended;         // U+00C8（È）

// 注意：値0-127はASCII、128-255はLatin-1
```

### チェーン変換

型変換はチェーン可能：

```hemlock
// i32 → ルーン → 文字列
let code: i32 = 128512;         // 笑顔のコードポイント
let r: rune = code;             // 😀
let s: string = r;              // "😀"

// 1つの式で全部
let emoji: string = 128640;     // 暗黙のi32 → ルーン → 文字列（🚀）
```

## ルーン操作

### 出力

ルーンの表示方法はコードポイントに依存：

```hemlock
let ascii = 'A';
print(ascii);                   // 'A'（引用符付き、印刷可能ASCII）

let emoji = '🚀';
print(emoji);                   // U+1F680（非ASCIIはUnicode表記）

let tab = '\t';
print(tab);                     // U+0009（非印刷は16進数で）

let space = ' ';
print(space);                   // ' '（印刷可能）
```

**出力形式：**
- 印刷可能ASCII（32-126）：引用符付き文字 `'A'`
- 非印刷またはUnicode：16進表記 `U+XXXX`

### 型チェック

`typeof()`を使用して値がルーンかチェック：

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "text";
let ch = s[0];
print(typeof(ch));              // "rune"（インデックスはルーンを返す）

let num = 65;
print(typeof(num));             // "i32"
```

### 比較

ルーンは等価性で比較可能：

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// 大文字小文字を区別
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// ルーンは整数（コードポイント値）と比較可能
print(a == 65);                 // true（暗黙の変換）
print('🚀' == 128640);          // true
```

**比較演算子：**
- `==` - 等しい
- `!=` - 等しくない
- `<`、`>`、`<=`、`>=` - コードポイント順序

```hemlock
print('A' < 'B');               // true（65 < 66）
print('a' > 'Z');               // true（97 > 90）
```

## 文字列インデックスとの連携

文字列のインデックスはバイトではなくルーンを返す：

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H'（ルーン）
let rocket = s[5];              // '🚀'（ルーン）

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// 必要なら文字列に変換
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "🚀"
```

**重要：** 文字列のインデックスはバイトオフセットではなくコードポイント位置を使用：

```hemlock
let text = "Hi🚀!";
// コードポイント位置：0='H', 1='i', 2='🚀', 3='!'
// バイト位置：      0='H', 1='i', 2-5='🚀', 6='!'

let r = text[2];                // '🚀'（コードポイント2）
print(typeof(r));               // "rune"
```

## 例

### 例：文字分類

```hemlock
fn is_digit(r: rune): bool {
    return r >= '0' && r <= '9';
}

fn is_upper(r: rune): bool {
    return r >= 'A' && r <= 'Z';
}

fn is_lower(r: rune): bool {
    return r >= 'a' && r <= 'z';
}

print(is_digit('5'));           // true
print(is_upper('A'));           // true
print(is_lower('z'));           // true
```

### 例：大文字小文字変換

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // 大文字に変換（32を引く）
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // 小文字に変換（32を足す）
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### 例：文字の反復

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Position " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Hi🚀");
// Position 0: 'H'
// Position 1: 'i'
// Position 2: U+1F680
```

### 例：ルーンから文字列を構築

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let result = "";
    let i = 0;
    while (i < count) {
        result = result + ch;
        i = i + 1;
    }
    return result;
}

let line = repeat_char('=', 40);  // "========================================"
let stars = repeat_char('⭐', 5);  // "⭐⭐⭐⭐⭐"
```

## よくあるパターン

### パターン：文字フィルタ

```hemlock
fn filter_digits(s: string): string {
    let result = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}

let text = "abc123def456";
let digits = filter_digits(text);  // "123456"
```

### パターン：文字カウント

```hemlock
fn count_char(s: string, target: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == target) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let text = "hello world";
let l_count = count_char(text, 'l');  // 3
let o_count = count_char(text, 'o');  // 2
```

## ベストプラクティス

1. **文字操作にはルーンを使用** - テキスト処理でバイトを使おうとしない
2. **文字列のインデックスはルーンを返す** - `str[i]`がルーンを与えることを覚えておく
3. **Unicode対応の比較** - ルーンはあらゆるUnicode文字を処理
4. **必要なら変換** - ルーンは簡単に文字列や整数に変換可能
5. **絵文字でテスト** - 常にマルチバイト文字で文字操作をテスト

## よくある落とし穴

### 落とし穴：ルーン vs バイトの混乱

```hemlock
// やらない：ルーンをバイトとして扱う
let r: rune = '🚀';
let b: u8 = r;              // エラー：ルーンのコードポイント128640はu8に収まらない

// やる：適切な変換を使用
let r: rune = '🚀';
let code: i32 = r;          // OK：128640
```

### 落とし穴：文字列のバイトインデックス

```hemlock
// やらない：バイトインデックスを想定
let s = "🚀";
let byte = s.byte_at(0);    // 240（最初のUTF-8バイト、完全な文字ではない）

// やる：コードポイントインデックスを使用
let s = "🚀";
let rune = s[0];            // '🚀'（完全な文字）
let rune2 = s.char_at(0);   // '🚀'（明示的なメソッド）
```

## 関連トピック

- [文字列](strings.md) - 文字列操作とUTF-8の扱い
- [型](types.md) - 型システムと変換
- [制御フロー](control-flow.md) - 比較でのルーンの使用

## 参照

- **Unicode標準**：UnicodeコードポイントはUnicodeコンソーシアムによって定義
- **UTF-8エンコーディング**：UTF-8の詳細は[文字列](strings.md)を参照
- **型変換**：変換ルールは[型](types.md)を参照
