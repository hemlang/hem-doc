# 構文の概要

このドキュメントでは、Hemlockプログラムの基本的な構文規則と構造について説明します。

## コア構文規則

### セミコロンは必須

JavaScriptやPythonとは異なり、セミコロンは文の末尾で**常に必須**です：

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**これはエラーになります：**
```hemlock
let x = 42  // エラー：セミコロンがない
let y = 10  // エラー：セミコロンがない
```

### ブレースは常に必須

すべての制御フローブロックは、単一の文でもブレースを使用する必要があります：

```hemlock
// 正しい
if (x > 0) {
    print("positive");
}

// エラー：ブレースがない
if (x > 0)
    print("positive");
```

### コメント

```hemlock
// これは単一行コメント

/*
   これは
   複数行コメント
*/

let x = 42;  // インラインコメント
```

## 変数

### 宣言

変数は`let`で宣言：

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### 型注釈（オプション）

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hello";
```

### 定数

イミュータブルな値には`const`を使用：

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

constを再代入しようとすると実行時エラーになります：「Cannot assign to const variable」。

## 式

### 算術演算子

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - 加算
print(a - b);   // 7  - 減算
print(a * b);   // 30 - 乗算
print(a / b);   // 3  - 除算（整数）
```

### 比較演算子

```hemlock
print(a == b);  // false - 等しい
print(a != b);  // true  - 等しくない
print(a > b);   // true  - より大きい
print(a < b);   // false - より小さい
print(a >= b);  // true  - 以上
print(a <= b);  // false - 以下
```

### 論理演算子

```hemlock
let x = true;
let y = false;

print(x && y);  // false - AND
print(x || y);  // true  - OR
print(!x);      // false - NOT
```

### ビット演算子

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - ビットAND
print(a | b);   // 14 - ビットOR
print(a ^ b);   // 6  - ビットXOR
print(a << 2);  // 48 - 左シフト
print(a >> 1);  // 6  - 右シフト
print(~a);      // -13 - ビットNOT
```

### 演算子の優先順位

最高から最低：

1. `()` - グループ化
2. `!`、`~`、`-`（単項） - 単項演算子
3. `*`、`/` - 乗算、除算
4. `+`、`-` - 加算、減算
5. `<<`、`>>` - ビットシフト
6. `<`、`<=`、`>`、`>=` - 比較
7. `==`、`!=` - 等価
8. `&` - ビットAND
9. `^` - ビットXOR
10. `|` - ビットOR
11. `&&` - 論理AND
12. `||` - 論理OR

**例：**
```hemlock
let x = 2 + 3 * 4;      // 14（20ではない）
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40（5 << 3）
```

## 制御フロー

### If文

```hemlock
if (condition) {
    // 本体
}

if (condition) {
    // thenブランチ
} else {
    // elseブランチ
}

if (condition1) {
    // ブランチ1
} else if (condition2) {
    // ブランチ2
} else {
    // デフォルトブランチ
}
```

### Whileループ

```hemlock
while (condition) {
    // 本体
}
```

**例：**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Forループ

**Cスタイルfor：**
```hemlock
for (initializer; condition; increment) {
    // 本体
}
```

**例：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in（配列）：**
```hemlock
for (let item in array) {
    // 本体
}
```

**例：**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Switch文

```hemlock
switch (expression) {
    case value1:
        // 本体
        break;
    case value2:
        // 本体
        break;
    default:
        // デフォルト本体
        break;
}
```

**例：**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Monday");
        break;
    case 2:
        print("Tuesday");
        break;
    case 3:
        print("Wednesday");
        break;
    default:
        print("Other");
        break;
}
```

### BreakとContinue

```hemlock
// Break：ループを終了
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue：次の反復にスキップ
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## 関数

### 名前付き関数

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // 本体
    return value;
}
```

**例：**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### 無名関数

```hemlock
let func = fn(params) {
    // 本体
};
```

**例：**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### 型注釈（オプション）

```hemlock
// 注釈なし（型推論）
fn greet(name) {
    return "Hello, " + name;
}

// 注釈付き（実行時にチェック）
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## オブジェクト

### オブジェクトリテラル

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**例：**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### メソッド

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**例：**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### 型定義

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**例：**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## 配列

### 配列リテラル

```hemlock
let arr = [element1, element2, element3];
```

**例：**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];
let empty = [];
```

### 配列のインデックス

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // 要素を変更
```

## エラーハンドリング

### Try/Catch

```hemlock
try {
    // 危険なコード
} catch (e) {
    // エラーを処理
}
```

### Try/Finally

```hemlock
try {
    // 危険なコード
} finally {
    // 常に実行
}
```

### Try/Catch/Finally

```hemlock
try {
    // 危険なコード
} catch (e) {
    // エラーを処理
} finally {
    // クリーンアップ
}
```

### Throw

```hemlock
throw expression;
```

**例：**
```hemlock
if (x < 0) {
    throw "x must be positive";
}
```

### Panic

```hemlock
panic(message);
```

**例：**
```hemlock
panic("unrecoverable error");
```

## モジュール（実験的）

### Export文

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Import文

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## 非同期（実験的）

### 非同期関数

```hemlock
async fn function_name(params): return_type {
    // 本体
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### チャネル

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI（外部関数インターフェース）

### 共有ライブラリのインポート

```hemlock
import "library_name.so";
```

### 外部関数の宣言

```hemlock
extern fn function_name(param: type): return_type;
```

**例：**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## リテラル

### 整数リテラル

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // 自動的にi64

// 16進数（0xプレフィックス）
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// 2進数（0bプレフィックス）
let bin = 0b1010;
let bin2 = 0b11110000;

// 8進数（0oプレフィックス）
let oct = 0o777;
let oct2 = 0O123;

// 読みやすさのための数値セパレータ
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### 浮動小数点リテラル

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // 指数表記
let sci2 = 2.5E+3;       // 大文字Eも動作
let no_lead = .5;        // 先頭のゼロなし（0.5）
let sep = 3.14_159_265;  // 数値セパレータ
```

### 文字列リテラル

```hemlock
let s = "hello";
let escaped = "line1\nline2\ttabbed";
let quote = "She said \"hello\"";

// 16進エスケープシーケンス
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Unicodeエスケープシーケンス
let emoji = "\u{1F600}";               // 😀
let heart = "\u{2764}";                // ❤
let mixed = "Hello \u{1F30D}!";        // Hello 🌍!
```

**エスケープシーケンス：**
- `\n` - 改行
- `\t` - タブ
- `\r` - キャリッジリターン
- `\\` - バックスラッシュ
- `\"` - ダブルクォート
- `\'` - シングルクォート
- `\0` - ヌル文字
- `\xNN` - 16進エスケープ（2桁）
- `\u{XXXX}` - Unicodeエスケープ（1-6桁）

### ルーンリテラル

```hemlock
let ch = 'A';
let emoji = '🚀';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### 真偽値リテラル

```hemlock
let t = true;
let f = false;
```

### Nullリテラル

```hemlock
let nothing = null;
```

## スコープルール

### ブロックスコープ

変数は最も近い囲んでいるブロックにスコープされます：

```hemlock
let x = 1;  // 外側のスコープ

if (true) {
    let x = 2;  // 内側のスコープ（外側をシャドウ）
    print(x);   // 2
}

print(x);  // 1
```

### 関数スコープ

関数は独自のスコープを作成します：

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // 外側のスコープを読める
}

foo();
// print(local);  // エラー：'local'はここで定義されていない
```

### クロージャスコープ

クロージャは囲んでいるスコープの変数をキャプチャします：

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // 'count'をキャプチャ
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## 空白とフォーマット

### インデント

Hemlockは特定のインデントを強制しませんが、4スペースを推奨：

```hemlock
fn example() {
    if (true) {
        print("indented");
    }
}
```

### 改行

文は複数行にまたがることができます：

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Loop文

`loop`キーワードは無限ループのためのよりクリーンな構文を提供します：

```hemlock
loop {
    // ... 処理を行う
    if (done) {
        break;
    }
}
```

これは`while (true)`と等価ですが、意図がより明確です。

## 予約キーワード

以下のキーワードはHemlockで予約されています：

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## 次のステップ

- [型システム](types.md) - Hemlockの型システムを学ぶ
- [制御フロー](control-flow.md) - 制御構造の詳細
- [関数](functions.md) - 関数とクロージャをマスター
- [メモリ管理](memory.md) - ポインタとバッファを理解
