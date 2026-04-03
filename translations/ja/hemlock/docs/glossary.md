# 用語集

プログラミングやシステムの概念が初めてですか？この用語集では、Hemlockのドキュメント全体で使用される用語をわかりやすく説明します。

---

## A

### Allocate / Allocation（割り当て）
**意味:** コンピュータに使用するメモリの一部を要求すること。

**例え:** 図書館から本を借りるようなもの - 後で返す必要があるスペースを借りています。

**Hemlockでは:**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### Array（配列）
**意味:** 位置（インデックス）でアクセスされる、一緒に格納された値のリスト。

**例え:** 0、1、2、3...と番号が付いた郵便受けの列のようなもの。2番の郵便受けに何かを入れて、後で2番の郵便受けから取り出せます。

**Hemlockでは:**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Asynchronous（非同期）
**意味:** 他のコードが続行している間に「バックグラウンドで」実行できるコード。Hemlockでは、非同期コードは実際に別のCPUコアで同時に実行されます。

**例え:** 複数の料理を同時に作るようなもの - ご飯を炊いている間に野菜を切ります。両方が同時に進行します。

**Hemlockでは:**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Boolean / Bool（ブーリアン）
**意味:** `true` か `false` のいずれかの値。それ以外はありません。

**名前の由来:** 真偽論理を研究した数学者、George Booleにちなんで名付けられました。

**Hemlockでは:**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Bounds Checking（境界チェック）
**意味:** 割り当てられたメモリの範囲外にアクセスしようとしていないかを自動的に検証すること。クラッシュやセキュリティバグを防ぎます。

**例え:** リクエストされた本が実際に存在するかを、取りに行く前に確認する司書のようなもの。

**Hemlockでは:**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer（バッファ）
**意味:** 既知のサイズを持つ生のバイトの安全なコンテナ。Hemlockはその境界を超えて読み書きしないようにチェックします。

**例え:** 特定の数の仕切りがある金庫のようなもの。どの仕切りも使えますが、金庫に10個しかないのに50番目の仕切りにはアクセスできません。

**Hemlockでは:**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Closure（クロージャ）
**意味:** 作成された場所の変数を「記憶」する関数。そのコードが終了した後でも記憶し続けます。

**例え:** 「渡された数字に5を足す」というメモのようなもの - 「5」がメモに焼き込まれています。

**Hemlockでは:**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Coercion（型強制）
**意味:** 必要に応じて値を自動的に別の型に変換すること。

**例:** 整数と小数を足すと、整数が先に自動的に小数に変換されます。

**Hemlockでは:**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Compile / Compiler（コンパイル / コンパイラ）
**意味:** コードをコンピュータが直接実行できるプログラムに変換すること。コンパイラ（`hemlockc`）は `.hml` ファイルを読み込み、実行可能ファイルを作成します。

**例え:** 本を英語からスペイン語に翻訳するようなもの - 内容は同じですが、スペイン語話者が読めるようになります。

**Hemlockでは:**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Concurrency（並行性）
**意味:** 複数のことが重なり合う時間に起こること。Hemlockでは、これは複数のCPUコアでの実際の並列実行を意味します。

**例え:** 同じキッチンで2人のシェフが同時に異なる料理を作ること。

---

## D

### Defer（遅延実行）
**意味:** 現在の関数が終了するときに後で何かが起こるようにスケジュールすること。クリーンアップに便利です。

**例え:** 「出るときに電気を消す」と自分に言い聞かせるようなもの - 今リマインダーを設定して、後で実行されます。

**Hemlockでは:**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck Typing（ダックタイピング）
**意味:** アヒルのように見えてアヒルのように鳴くなら、アヒルとして扱う。コードでは：オブジェクトが必要なフィールド/メソッドを持っていれば、公式の「型」を気にせずに使います。

**名前の由来:** ダックテスト - 推論の一形式。

**Hemlockでは:**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Expression（式）
**意味:** 値を生成するコード。値が期待される場所ならどこでも使用できます。

**例:** `42`、`x + y`、`get_name()`、`true && false`

### Enum / Enumeration（列挙型）
**意味:** 固定された可能な値のセットを持つ型で、各値に名前が付いています。

**例え:** ドロップダウンメニューのようなもの - リストされたオプションからしか選べません。

**Hemlockでは:**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Floating-Point（浮動小数点数）
**意味:** 小数点を持つ数。小数点が異なる位置に置けるため「浮動」と呼ばれます。

**Hemlockでは:**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free（解放）
**意味:** 使い終わったメモリをシステムに返して再利用できるようにすること。

**例え:** 図書館の本を返却して他の人が借りられるようにすること。

**Hemlockでは:**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Function（関数）
**意味:** 入力（パラメータ）を受け取り、出力（戻り値）を生成する可能性のある再利用可能なコードブロック。

**例え:** レシピのようなもの - 材料（入力）を渡し、手順に従い、料理（出力）を得ます。

**Hemlockでは:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Garbage Collection（ガベージコレクション / GC）
**意味:** 自動的なメモリクリーンアップ。ランタイムが定期的に未使用のメモリを見つけて解放します。

**Hemlockにない理由:** GCは予測不能な一時停止を引き起こす可能性があります。Hemlockは明示的な制御を好みます - メモリをいつ解放するかはあなたが決めます。

**注意:** ほとんどのHemlock型（文字列、配列、オブジェクト）はスコープを抜けると自動的にクリーンアップされます。`alloc()` からの生の `ptr` のみが手動の `free()` を必要とします。

---

## H

### Heap（ヒープ）
**意味:** 現在の関数より長く存続する必要があるデータのためのメモリ領域。ヒープメモリは明示的に割り当てて解放します。

**対比:** スタック（ローカル変数のための自動的で一時的なストレージ）

**Hemlockでは:**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Index（インデックス）
**意味:** 配列や文字列内のアイテムの位置。Hemlockでは0から始まります。

**Hemlockでは:**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Integer（整数）
**意味:** 小数点のない数。正、負、またはゼロになります。

**Hemlockでは:**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interpreter（インタプリタ）
**意味:** コードを読んで直接実行するプログラム。一行ずつ実行します。

**対比:** コンパイラ（先にコードを変換してから、変換されたものを実行する）

**Hemlockでは:**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Literal（リテラル）
**意味:** コードに直接書かれた値で、計算されたものではありません。

**例:**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Memory Leak（メモリリーク）
**意味:** 割り当てたメモリの解放を忘れること。メモリは予約されたまま使用されず、リソースが無駄になります。

**例え:** 図書館の本を借りて一度も返さないこと。最終的に図書館の本がなくなります。

**Hemlockでは:**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Method（メソッド）
**意味:** オブジェクトや型に紐づけられた関数。

**Hemlockでは:**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex（ミューテックス）
**意味:** 一度に1つのスレッドだけが何かにアクセスすることを保証するロック。複数のスレッドが共有データに触れるときのデータ破損を防ぎます。

**例え:** バスルームの鍵のようなもの - 一度に1人しか使えません。

---

## N

### Null（ヌル）
**意味:** 「何もない」または「値なし」を意味する特別な値。

**Hemlockでは:**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Object（オブジェクト）
**意味:** 名前付きの値（フィールド/プロパティ）をグループ化したコレクション。

**Hemlockでは:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parameter（パラメータ）
**意味:** 関数が呼び出されたときに受け取ることを期待する変数。

**別名:** 引数（Argument）（技術的には、パラメータは定義内で、引数は呼び出し時のもの）

**Hemlockでは:**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Pointer（ポインタ）
**意味:** メモリアドレスを保持する値 - データがどこに格納されているかを「指し示す」もの。

**例え:** 住所のようなもの。住所は家そのものではなく、家がどこにあるかを教えてくれます。

**Hemlockでは:**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitive（プリミティブ）
**意味:** 他の型で構成されていない、基本的な組み込み型。

**Hemlockでは:** `i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`rune`、`null`

---

## R

### Reference Counting（参照カウント）
**意味:** あるデータを何がいくつ使用しているかを追跡すること。何も使用しなくなったら、自動的にクリーンアップします。

**Hemlockでは:** 文字列、配列、オブジェクト、バッファは内部的に参照カウントを使用しています。見えませんが、一般的な型のメモリリークを防いでいます。

### Return Value（戻り値）
**意味:** 関数が終了したときに返す値。

**Hemlockでは:**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune（ルーン）
**意味:** 単一のUnicode文字（コードポイント）。絵文字を含むあらゆる文字を表現できます。

**なぜ「ルーン」？** この用語はGoから来ています。これがバイトではなく完全な文字であることを強調しています。

**Hemlockでは:**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Runtime（ランタイム）
**意味:** プログラムが実際に実行されている時間（コードが変換される「コンパイル時」とは対照的に）。

**また:** プログラムと一緒に実行されるサポートコード（例：メモリアロケータ）。

---

## S

### Scope（スコープ）
**意味:** 変数が存在し使用できるコードの領域。

**Hemlockでは:**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Stack（スタック）
**意味:** 一時的で短命なデータのためのメモリ。自動的に管理されます - 関数が戻ると、そのスタックスペースは回収されます。

**対比:** ヒープ（より長寿命、手動管理）

### Statement（文）
**意味:** 単一の命令またはコマンド。文は何かを行います; 式は値を生成します。

**例:** `let x = 5;`、`print("hi");`、`if (x > 0) { ... }`

### String（文字列）
**意味:** テキスト文字の並び。

**Hemlockでは:**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Structural Typing（構造的型付け）
**意味:** 名前ではなく構造（どのフィールド/メソッドが存在するか）に基づく型の互換性。「ダックタイピング」と同じです。

---

## T

### Thread（スレッド）
**意味:** 独立した実行経路。複数のスレッドは異なるCPUコアで同時に実行できます。

**Hemlockでは:** `spawn()` が新しいスレッドを作成します。

### Type（型）
**意味:** 値が表すデータの種類。どの操作が有効かを決定します。

**Hemlockでは:**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Type Annotation（型注釈）
**意味:** 変数がどの型であるべきかを明示的に宣言すること。

**Hemlockでは:**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**意味:** すべての世界の言語と絵文字をサポートするテキストのエンコード方式。各文字は1〜4バイトになります。

**Hemlockでは:** すべての文字列はUTF-8です。

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variable（変数）
**意味:** 値を保持する名前付きの格納場所。

**Hemlockでは:**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## クイックリファレンス: どの型を使うべき？

| 状況 | 使用する型 | 理由 |
|------|-----------|------|
| 数字が必要なだけ | `let x = 42;` | Hemlockが適切な型を選びます |
| 物を数える | `i32` | ほとんどのカウントに十分な大きさ |
| 巨大な数 | `i64` | i32では足りないとき |
| バイト (0-255) | `u8` | ファイル、ネットワークデータ |
| 小数 | `f64` | 正確な小数計算 |
| はい/いいえの値 | `bool` | `true` か `false` のみ |
| テキスト | `string` | あらゆるテキストコンテンツ |
| 単一文字 | `rune` | 1つの文字/絵文字 |
| 物のリスト | `array` | 順序付きコレクション |
| 名前付きフィールド | `object` | 関連データをグループ化 |
| 生のメモリ | `buffer` | 安全なバイトストレージ |
| FFI/システム作業 | `ptr` | 上級者向け、手動メモリ |

---

## 関連項目

- [クイックスタート](getting-started/quick-start.md) - 最初のHemlockプログラム
- [型システム](language-guide/types.md) - 完全な型ドキュメント
- [メモリ管理](language-guide/memory.md) - メモリの理解
