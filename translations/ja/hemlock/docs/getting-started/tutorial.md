# Hemlockチュートリアル

Hemlockを学ぶための包括的なステップバイステップガイドです。

## 目次

1. [Hello World](#hello-world)
2. [変数と型](#変数と型)
3. [算術と演算](#算術と演算)
4. [制御フロー](#制御フロー)
5. [関数](#関数)
6. [文字列とRune](#文字列とrune)
7. [配列](#配列)
8. [オブジェクト](#オブジェクト)
9. [メモリ管理](#メモリ管理)
10. [エラーハンドリング](#エラーハンドリング)
11. [ファイルI/O](#ファイルio)
12. [まとめ](#まとめ)

## Hello World

伝統的な最初のプログラムから始めましょう：

```hemlock
print("Hello, World!");
```

これを`hello.hml`として保存し、実行します：

```bash
./hemlock hello.hml
```

**ポイント：**
- `print()`はstdoutに出力する組み込み関数
- 文字列はダブルクォートで囲む
- セミコロンは**必須**

## 変数と型

### 変数の宣言

```hemlock
// 基本的な変数宣言
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### 型注釈

型はデフォルトで推論されますが、明示的にも指定できます：

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### 型推論

Hemlockは値に基づいて型を推論します：

```hemlock
let small = 42;              // i32（32ビットに収まる）
let large = 5000000000;      // i64（i32には大きすぎる）
let decimal = 3.14;          // f64（浮動小数点のデフォルト）
let text = "hello";          // string
let flag = true;             // bool
```

### 型チェック

```hemlock
// typeof()で型をチェック
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hello"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## 算術と演算

### 基本的な算術

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3（整数除算）
print(a == b);  // false
print(a > b);   // true
```

### 型昇格

型を混合すると、Hemlockはより大きい/より精度の高い型に昇格します：

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // resultはf64（10.0 + 3.5 = 13.5）

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### ビット演算

```hemlock
let a = 12;  // 2進数で1100
let b = 10;  // 2進数で1010

print(a & b);   // 8  (AND)
print(a | b);   // 14 (OR)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24（左シフト）
print(a >> 1);  // 6 （右シフト）
print(~a);      // -13 (NOT)
```

## 制御フロー

### if文

```hemlock
let x = 10;

if (x > 0) {
    print("positive");
} else if (x < 0) {
    print("negative");
} else {
    print("zero");
}
```

**注意：** 単一の文でもブレースは**常に必須**です。

### whileループ

```hemlock
let count = 0;
while (count < 5) {
    print(`Count: ${count}`);
    count = count + 1;
}
```

### forループ

```hemlock
// Cスタイルのforループ
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// for-inループ（配列）
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Item: ${item}`);
}
```

### switch文

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
        print("Other day");
        break;
}
```

### breakとcontinue

```hemlock
// break：ループを早期終了
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// 出力：0, 1, 2, 3, 4

// continue：次のイテレーションにスキップ
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// 出力：0, 1, 3, 4
```

## 関数

### 名前付き関数

```hemlock
fn greet(name: string): string {
    return "Hello, " + name + "!";
}

let message = greet("Alice");
print(message);  // "Hello, Alice!"
```

### 匿名関数

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### 再帰

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### クロージャ

関数は環境をキャプチャします：

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

### 高階関数

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## 文字列とRune

### 文字列の基本

文字列は**ミュータブル**で**UTF-8**です：

```hemlock
let s = "hello";
print(s.length);      // 5（文字数）
print(s.byte_length); // 5（バイト数）

// ミューテーション
s[0] = 'H';
print(s);  // "Hello"
```

### 文字列メソッド

```hemlock
let text = "  Hello, World!  ";

// 大文字小文字変換
print(text.to_upper());  // "  HELLO, WORLD!  "
print(text.to_lower());  // "  hello, world!  "

// トリミング
print(text.trim());      // "Hello, World!"

// 部分文字列抽出
let hello = text.substr(2, 5);  // "Hello"
let world = text.slice(9, 14);  // "World"

// 検索
let pos = text.find("World");   // 9
let has = text.contains("o");   // true

// 分割
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// 置換
let s = "hello world".replace("world", "there");
print(s);  // "hello there"
```

### Rune（Unicodeコードポイント）

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Rune + 文字列の連結
let msg = '>' + " Important";
print(msg);  // "> Important"

// runeと整数間の変換
let code: i32 = ch;     // 65（ASCIIコード）
let r: rune = 128640;   // U+1F680（🚀）
```

## 配列

### 配列の基本

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// 要素を変更
numbers[2] = 99;
print(numbers[2]);  // 99
```

### 配列メソッド

```hemlock
let arr = [10, 20, 30];

// 末尾に追加/削除
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40、arrは[10, 20, 30]になる

// 先頭に追加/削除
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5、arrは[10, 20, 30]になる

// インデックスで挿入/削除
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// 検索
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// スライス
let slice = arr.slice(0, 2);  // [10, 15]

// 文字列に結合
let text = arr.join(", ");    // "10, 15, 30"
```

### イテレーション

```hemlock
let items = ["apple", "banana", "cherry"];

// for-inループ
for (let item in items) {
    print(item);
}

// 手動イテレーション
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## オブジェクト

### オブジェクトリテラル

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// フィールドの追加/変更
person.email = "alice@example.com";
person.age = 31;
```

### メソッドと`self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### 型定義（ダック型）

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // デフォルト付きオプション
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // ダック型が構造を検証

print(typeof(typed));   // "Person"
print(typed.active);    // true（デフォルトが適用）
```

### JSONシリアライゼーション

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// オブジェクトからJSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSONからオブジェクト
let restored = json.deserialize();
print(restored.name);  // "test"
```

## メモリ管理

### 安全なバッファ（推奨）

```hemlock
// バッファを確保
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// 値を設定（境界チェック付き）
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// 値にアクセス
print(buf[0]);  // 65

// 完了時に解放必須
free(buf);
```

### 生ポインタ（上級者向け）

```hemlock
// 生メモリを確保
let ptr = alloc(100);

// ゼロで埋める
memset(ptr, 0, 100);

// データをコピー
let src = alloc(50);
memcpy(ptr, src, 50);

// 両方を解放
free(src);
free(ptr);
```

### メモリ関数

```hemlock
// 再確保
let p = alloc(64);
p = realloc(p, 128);  // 128バイトにリサイズ
free(p);

// 型付き確保（将来）
// let arr = talloc(i32, 100);  // 100個のi32の配列
```

## エラーハンドリング

### try/catch

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
}
// 出力：Error: division by zero
```

### finallyブロック

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Error: " + e);
} finally {
    // 常に実行
    if (file != null) {
        file.close();
    }
}
```

### オブジェクトをthrow

```hemlock
try {
    throw { code: 404, message: "Not found" };
} catch (e) {
    print(`Error ${e.code}: ${e.message}`);
}
// 出力：Error 404: Not found
```

### panic（回復不能エラー）

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x must be non-negative");
    }
    return x * 2;
}

validate(-5);  // プログラムは終了：panic: x must be non-negative
```

## ファイルI/O

### ファイルの読み込み

```hemlock
// ファイル全体を読み込み
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// 特定のバイト数を読み込み
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // 100バイト読み込み
f2.close();
```

### ファイルへの書き込み

```hemlock
// テキストを書き込み
let f = open("output.txt", "w");
f.write("Hello, File!\n");
f.write("Second line\n");
f.close();

// ファイルに追記
let f2 = open("output.txt", "a");
f2.write("Appended line\n");
f2.close();
```

### バイナリI/O

```hemlock
// バイナリデータを書き込み
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// バイナリデータを読み込み
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### ファイルプロパティ

```hemlock
let f = open("/path/to/file.txt", "r");

print(f.path);    // "/path/to/file.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## まとめ

シンプルな単語カウンタプログラムを作りましょう：

```hemlock
// wordcount.hml - ファイル内の単語をカウント

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // 空白で分割してカウント
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Error reading file: " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// メインプログラム
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Word count: ${words}`);
    }
}
```

実行：
```bash
./hemlock wordcount.hml data.txt
```

## 次のステップ

おめでとうございます！Hemlockの基本を学びました。次に探索するものはこちらです：

- [非同期と並行処理](../advanced/async-concurrency.md) - 真のマルチスレッド
- [FFI](../advanced/ffi.md) - C関数を呼び出す
- [シグナルハンドリング](../advanced/signals.md) - プロセスシグナル
- [APIリファレンス](../reference/builtins.md) - 完全なAPIドキュメント
- [サンプル](../../examples/) - より実世界のプログラム

## 練習問題

練習のためにこれらのプログラムを作ってみてください：

1. **電卓**: +、-、*、/の簡単な電卓を実装
2. **ファイルコピー**: 1つのファイルを別のファイルにコピー
3. **フィボナッチ**: フィボナッチ数を生成
4. **JSONパーサー**: JSONファイルを読み込んでパース
5. **テキストプロセッサ**: ファイル内のテキストを検索・置換

Hemlockで楽しいコーディングを！
