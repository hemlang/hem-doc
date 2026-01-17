# クイックスタート

数分でHemlockを使い始めましょう！

## 最初のプログラム

`hello.hml`というファイルを作成します：

```hemlock
print("Hello, Hemlock!");
```

インタプリタで実行：

```bash
./hemlock hello.hml
```

またはネイティブ実行ファイルにコンパイル：

```bash
./hemlockc hello.hml -o hello
./hello
```

出力：
```
Hello, Hemlock!
```

### インタプリタ vs コンパイラ

Hemlockにはプログラムを実行する2つの方法があります：

| ツール | ユースケース | 型チェック |
|------|----------|---------------|
| `hemlock` | クイックスクリプト、REPL、開発 | 実行時のみ |
| `hemlockc` | 本番バイナリ、より良いパフォーマンス | コンパイル時（デフォルト） |

コンパイラ（`hemlockc`）は実行ファイルを生成する前にコードの型チェックを行い、エラーを早期に発見します。

## 基本構文

### 変数

```hemlock
// 変数は'let'で宣言
let x = 42;
let name = "Alice";
let pi = 3.14159;

// 型注釈はオプション
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**重要**: Hemlockではセミコロンは**必須**です！

### 型

Hemlockには豊富な型システムがあります：

```hemlock
// 整数
let small: i8 = 127;          // 8ビット符号付き
let byte: u8 = 255;           // 8ビット符号なし
let num: i32 = 2147483647;    // 32ビット符号付き（デフォルト）
let big: i64 = 9223372036854775807;  // 64ビット符号付き

// 浮動小数点
let f: f32 = 3.14;            // 32ビット浮動小数点
let d: f64 = 2.71828;         // 64ビット浮動小数点（デフォルト）

// 文字列と文字
let text: string = "Hello";   // UTF-8文字列
let emoji: rune = '🚀';       // Unicodeコードポイント

// 真偽値とnull
let flag: bool = true;
let empty = null;
```

### 制御フロー

```hemlock
// if文
if (x > 0) {
    print("positive");
} else if (x < 0) {
    print("negative");
} else {
    print("zero");
}

// whileループ
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// forループ
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### 関数

```hemlock
// 名前付き関数
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// 匿名関数
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## 文字列の操作

Hemlockの文字列は**ミュータブル**で**UTF-8**です：

```hemlock
let s = "hello";
s[0] = 'H';              // "Hello"になる
print(s);

// 文字列メソッド
let upper = s.to_upper();     // "HELLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "ell"

// 連結
let greeting = "Hello" + ", " + "World!";
print(greeting);  // "Hello, World!"
```

## 配列

混合型の動的配列：

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// 配列メソッド
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// 混合型も可能
let mixed = [1, "two", true, null];
```

## オブジェクト

JavaScriptスタイルのオブジェクト：

```hemlock
// オブジェクトリテラル
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // フィールドを変更

// 'self'を使ったメソッド
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## メモリ管理

Hemlockは**手動メモリ管理**を使用します：

```hemlock
// 安全なバッファ（推奨）
let buf = buffer(64);   // 64バイトを確保
buf[0] = 65;            // 最初のバイトを'A'に設定
print(buf[0]);          // 65
free(buf);              // メモリを解放

// 生ポインタ（上級者向け）
let ptr = alloc(100);
memset(ptr, 0, 100);    // ゼロで埋める
free(ptr);
```

**重要**: `alloc()`したものは`free()`する必要があります！

## エラーハンドリング

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Error: " + e);
} finally {
    print("Done");
}
```

## コマンドライン引数

`args`配列経由でプログラム引数にアクセス：

```hemlock
// script.hml
print("Script:", args[0]);
print(`Arguments: ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  arg ${i}: ${args[i]}`);
    i = i + 1;
}
```

実行：
```bash
./hemlock script.hml hello world
```

出力：
```
Script: script.hml
Arguments: 2
  arg 1: hello
  arg 2: world
```

## ファイルI/O

```hemlock
// ファイルへ書き込み
let f = open("data.txt", "w");
f.write("Hello, File!");
f.close();

// ファイルから読み込み
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Hello, File!"
f2.close();
```

## 次のステップ

基本を学んだので、さらに探索しましょう：

- [チュートリアル](tutorial.md) - 包括的なステップバイステップガイド
- [言語ガイド](../language-guide/syntax.md) - すべての機能の詳細
- [サンプル](../../examples/) - 実世界のサンプルプログラム
- [APIリファレンス](../reference/builtins.md) - 完全なAPIドキュメント

## よくある落とし穴

### セミコロンの忘れ

```hemlock
// ❌ エラー：セミコロンがない
let x = 42
let y = 10

// ✅ 正しい
let x = 42;
let y = 10;
```

### メモリ解放の忘れ

```hemlock
// ❌ メモリリーク
let buf = buffer(100);
// ... bufを使用 ...
// free(buf)を呼び忘れ！

// ✅ 正しい
let buf = buffer(100);
// ... bufを使用 ...
free(buf);
```

### ブレースは必須

```hemlock
// ❌ エラー：ブレースがない
if (x > 0)
    print("positive");

// ✅ 正しい
if (x > 0) {
    print("positive");
}
```

## ヘルプを得る

- [完全なドキュメント](../README.md)を読む
- [サンプルディレクトリ](../../examples/)を確認
- 使用パターンについては[テストファイル](../../tests/)を参照
- GitHubでissueを報告
