# 制御フロー

Hemlockは、必須のブレースと明示的な構文を備えた、おなじみのCスタイルの制御フローを提供します。このガイドでは、条件分岐、ループ、switch文、演算子について説明します。

## 概要

利用可能な制御フロー機能：

- `if`/`else`/`else if` - 条件分岐
- `while`ループ - 条件ベースの反復
- `for`ループ - Cスタイルとfor-in反復
- `loop` - 無限ループ（`while (true)`よりクリーン）
- `switch`文 - 多方向分岐
- `break`/`continue` - ループ制御
- ループラベル - ネストされたループ向けのターゲット指定break/continue
- `defer` - 遅延実行（クリーンアップ）
- 論理演算子：`&&`、`||`、`!`
- 比較演算子：`==`、`!=`、`<`、`>`、`<=`、`>=`
- ビット演算子：`&`、`|`、`^`、`<<`、`>>`、`~`

## If文

### 基本的なIf/Else

```hemlock
if (x > 10) {
    print("large");
} else {
    print("small");
}
```

**ルール：**
- ブレースはすべてのブランチで**常に必須**
- 条件は括弧で囲む必要がある
- オプションのブレースなし（Cとは異なる）

### Elseなしのif

```hemlock
if (x > 0) {
    print("positive");
}
// elseブランチは不要
```

### Else-Ifチェーン

```hemlock
if (x > 100) {
    print("very large");
} else if (x > 50) {
    print("large");
} else if (x > 10) {
    print("medium");
} else {
    print("small");
}
```

**注意：** `else if`はネストされたif文の糖衣構文です。これらは等価です：

```hemlock
// else if（糖衣構文）
if (a) {
    foo();
} else if (b) {
    bar();
}

// 等価なネストされたif
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### ネストされたIf文

```hemlock
if (x > 0) {
    if (x < 10) {
        print("single digit positive");
    } else {
        print("multi-digit positive");
    }
} else {
    print("non-positive");
}
```

## Whileループ

条件ベースの反復：

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**無限ループ（旧スタイル）：**
```hemlock
while (true) {
    // ... 処理を行う
    if (should_exit) {
        break;
    }
}
```

**注意：** 無限ループには`loop`キーワードを推奨（下記参照）。

## Loop（無限ループ）

`loop`キーワードは無限ループのためのよりクリーンな構文を提供します：

```hemlock
loop {
    // ... 処理を行う
    if (should_exit) {
        break;
    }
}
```

**`while (true)`と等価ですが、意図がより明確です。**

### Breakを使った基本的なLoop

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// 出力：0, 1, 2, 3, 4
```

### Continueを使ったLoop

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // 3の出力をスキップ
    }
    print(i);
}
// 出力：1, 2, 4, 5
```

### ネストされたLoop

```hemlock
let x = 0;
loop {
    if (x >= 2) { break; }
    let y = 0;
    loop {
        if (y >= 3) { break; }
        print(x * 10 + y);
        y = y + 1;
    }
    x = x + 1;
}
// 出力：0, 1, 2, 10, 11, 12
```

### Loopの使用タイミング

- **`loop`を使用** - `break`で終了する意図的な無限ループ
- **`while`を使用** - 自然な終了条件がある場合
- **`for`を使用** - 既知の回数または コレクションを反復する場合

## Forループ

### Cスタイルのfor

古典的な3部構成のforループ：

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**構成要素：**
- **初期化子**：`let i = 0` - ループ前に1回実行
- **条件**：`i < 10` - 各反復前にチェック
- **更新**：`i = i + 1` - 各反復後に実行

**スコープ：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// iはここではアクセスできない（ループスコープ）
```

### For-Inループ

配列要素の反復：

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // 各要素を出力
}
```

**インデックスと値を使用：**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Index: ${i}, Value: ${arr[i]}`);
}
```

## Switch文

値に基づく多方向分岐：

### 基本的なSwitch

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("one");
        break;
    case 2:
        print("two");
        break;
    case 3:
        print("three");
        break;
}
```

### Defaultを使ったSwitch

```hemlock
let color = "blue";

switch (color) {
    case "red":
        print("stop");
        break;
    case "yellow":
        print("slow");
        break;
    case "green":
        print("go");
        break;
    default:
        print("unknown color");
        break;
}
```

**ルール：**
- `default`は他のどのcaseにもマッチしない場合にマッチ
- `default`はswitch本体のどこにでも配置可能
- defaultケースは1つのみ許可

### フォールスルー動作

`break`なしのcaseは次のcaseにフォールスルー（Cスタイルの動作）。これは**意図的な**もので、caseをグループ化するために使用できます：

```hemlock
let grade = 85;

switch (grade) {
    case 100:
    case 95:
    case 90:
        print("A");
        break;
    case 85:
    case 80:
        print("B");
        break;
    default:
        print("C or below");
        break;
}
```

**明示的なフォールスルーの例：**
```hemlock
let day = 3;

switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Weekday");
        break;
    case 6:
    case 7:
        print("Weekend");
        break;
}
```

**重要：** 一部のモダンな言語とは異なり、Hemlockは明示的な`fallthrough`キーワードを必要としません。caseは`break`、`return`、または`throw`で終了しない限り自動的にフォールスルーします。意図しないフォールスルーを防ぐために常に`break`を使用してください。

### Returnを使ったSwitch

関数内では、`return`はswitchを即座に終了します：

```hemlock
fn get_day_name(day: i32): string {
    switch (day) {
        case 1:
            return "Monday";
        case 2:
            return "Tuesday";
        case 3:
            return "Wednesday";
        default:
            return "Unknown";
    }
}
```

### Switchの値の型

Switchは任意の値の型で動作します：

```hemlock
// 整数
switch (count) {
    case 0: print("zero"); break;
    case 1: print("one"); break;
}

// 文字列
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// 真偽値
switch (flag) {
    case true: print("on"); break;
    case false: print("off"); break;
}
```

**注意：** caseは値の等価性を使用して比較されます。

## BreakとContinue

### Break

最も内側のループまたはswitchを終了：

```hemlock
// ループ内
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // ループを終了
    }
    print(i);
    i = i + 1;
}

// switch内
switch (x) {
    case 1:
        print("one");
        break;  // switchを終了
    case 2:
        print("two");
        break;
}
```

### Continue

ループの次の反復にスキップ：

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // iが5のとき反復をスキップ
    }
    print(i);  // 0,1,2,3,4,6,7,8,9を出力
}
```

**違い：**
- `break` - ループを完全に終了
- `continue` - 次の反復にスキップ

## ループラベル

ループラベルにより、`break`と`continue`が最も内側のループだけでなく、特定の外側のループをターゲットにできます。ネストされたループで外側のループを内側から制御する必要がある場合に便利です。

### ラベル付きBreak

内側のループから外側のループを終了：

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // 外側のwhileループを終了
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// 出力：0, 1, 2, 10（i=1, j=1で停止）
```

### ラベル付きContinue

外側のループの次の反復にスキップ：

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // 内側ループの残りをスキップし、外側を続行
        }
        print(i * 10 + j);
    }
}
// i=2, j=1のとき：次の外側反復にスキップ
```

### Forループでのラベル

ラベルはすべてのループタイプで動作します：

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 3; y = y + 1) {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
    }
}
```

### For-Inループでのラベル

```hemlock
let arr1 = [1, 2, 3];
let arr2 = [10, 20, 30];

outer: for (let a in arr1) {
    for (let b in arr2) {
        if (a == 2 && b == 20) {
            break outer;
        }
        print(a * 100 + b);
    }
}
```

### Loopキーワードでのラベル

```hemlock
let x = 0;
outer: loop {
    let y = 0;
    loop {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
        y = y + 1;
        if (y >= 3) { break; }
    }
    x = x + 1;
    if (x >= 3) { break; }
}
```

### 複数のラベル

異なるネストレベルにラベルを設定できます：

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // 中間ループの次の反復にスキップ
            }
            if (a == 1 && b == 1) {
                break outer;      // 最外ループを終了
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### ラベル付きループでのラベルなしBreak/Continue

ラベルなしの`break`と`continue`は、外側のループにラベルがあっても通常通り動作します（最も内側のループに影響）：

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // 内側のループのみ終了
        }
        print(x * 10 + y);
    }
}
// 出力：0, 1, 10, 11, 20, 21
```

### ラベルの構文

- ラベルはコロンが続く識別子
- ラベルはループ文（`while`、`for`、`loop`）の直前に置く必要がある
- ラベル名は識別子のルールに従う（文字、数字、アンダースコア）
- 一般的な規約：`outer`、`inner`、`row`、`col`、説明的な名前

## Defer文

`defer`文は、現在の関数が戻るときに実行するコードをスケジュールします。ファイルのクローズ、リソースの解放、ロックの解除などのクリーンアップ操作に便利です。

### 基本的なDefer

```hemlock
fn example() {
    print("start");
    defer print("cleanup");  // 関数が戻るときに実行
    print("end");
}

example();
// 出力：
// start
// end
// cleanup
```

**主な動作：**
- 遅延された文は関数本体が完了した**後**に実行
- 遅延された文は関数が呼び出し元に戻る**前**に実行
- 遅延された文は関数が例外をスローしても常に実行

### 複数のDefer（LIFO順）

複数の`defer`文が使用される場合、**逆順**（後入れ先出し）で実行されます：

```hemlock
fn example() {
    defer print("first");   // 最後に実行
    defer print("second");  // 2番目に実行
    defer print("third");   // 最初に実行
    print("body");
}

example();
// 出力：
// body
// third
// second
// first
```

このLIFO順は意図的なものです - ネストされたリソースのクリーンアップの自然な順序（内側のリソースを外側より先にクローズ）に一致します。

### ReturnとDefer

遅延された文は`return`が制御を移す前に実行されます：

```hemlock
fn get_value(): i32 {
    defer print("cleanup");
    print("before return");
    return 42;
}

let result = get_value();
print("result:", result);
// 出力：
// before return
// cleanup
// result: 42
```

### 例外とDefer

遅延された文は例外がスローされても実行されます：

```hemlock
fn risky() {
    defer print("cleanup 1");
    defer print("cleanup 2");
    print("before throw");
    throw "error!";
    print("after throw");  // 到達しない
}

try {
    risky();
} catch (e) {
    print("Caught:", e);
}
// 出力：
// before throw
// cleanup 2
// cleanup 1
// Caught: error!
```

### リソースクリーンアップパターン

`defer`の主な使用例はリソースのクリーンアップを確実にすること：

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // エラー時も常にクローズ

    let content = file.read();
    // ... コンテンツを処理 ...

    // 関数が戻るときにファイルは自動的にクローズ
}
```

**deferなし（エラーが起きやすい）：**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // これがスローすると、file.close()は呼ばれない！
    process(content);
    file.close();
}
```

### クロージャとDefer

Deferはクロージャを使用して状態をキャプチャできます：

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Releasing resource");
        release(resource);
    }();  // 注意：即時実行関数式

    use_resource(resource);
}
```

### Deferを使用するタイミング

**deferを使用する場面：**
- ファイルとネットワーク接続のクローズ
- 割り当てられたメモリの解放
- ロックとミューテックスの解放
- リソースを取得する関数でのクリーンアップ

**Defer vs Finally：**
- `defer`は単一リソースのクリーンアップにシンプル
- `try/finally`はリカバリを伴う複雑なエラーハンドリングに適している

### ベストプラクティス

1. **リソース取得直後にdeferを配置：**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... ファイルを使用 ...
   ```

2. **複数のリソースには複数のdeferを使用：**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // 両方のファイルは逆順でクローズされる
   ```

3. **依存リソースにはLIFO順を考慮：**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // innerがouterより先に解放される（正しい依存順序）
   ```

## 論理演算子

### 論理AND（`&&`）

両方の条件がtrueである必要がある：

```hemlock
if (x > 0 && x < 10) {
    print("single digit positive");
}
```

**短絡評価：**
```hemlock
if (false && expensive_check()) {
    // expensive_check()は呼ばれない
}
```

### 論理OR（`||`）

少なくとも1つの条件がtrueである必要がある：

```hemlock
if (x < 0 || x > 100) {
    print("out of range");
}
```

**短絡評価：**
```hemlock
if (true || expensive_check()) {
    // expensive_check()は呼ばれない
}
```

### 論理NOT（`!`）

真偽値を否定：

```hemlock
if (!is_valid) {
    print("invalid");
}

if (!(x > 10)) {
    // 以下と同等：if (x <= 10)
}
```

## 比較演算子

### 等価性

```hemlock
if (x == 10) { }    // 等しい
if (x != 10) { }    // 等しくない
```

すべての型で動作：
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### 関係

```hemlock
if (x < 10) { }     // より小さい
if (x > 10) { }     // より大きい
if (x <= 10) { }    // 以下
if (x >= 10) { }    // 以上
```

**型の昇格が適用される：**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true（i32がi64に昇格）
```

## ビット演算子

Hemlockは整数操作のためのビット演算子を提供します。これらは**整数型のみ**（i8-i64、u8-u64）で動作します。

### 二項ビット演算子

**ビットAND（`&`）**
```hemlock
let a = 12;  // 2進数で1100
let b = 10;  // 2進数で1010
print(a & b);   // 8（1000）
```

**ビットOR（`|`）**
```hemlock
print(a | b);   // 14（1110）
```

**ビットXOR（`^`）**
```hemlock
print(a ^ b);   // 6（0110）
```

**左シフト（`<<`）**
```hemlock
print(a << 2);  // 48（110000）- 2ビット左にシフト
```

**右シフト（`>>`）**
```hemlock
print(a >> 1);  // 6（110）- 1ビット右にシフト
```

### 単項ビット演算子

**ビットNOT（`~`）**
```hemlock
let a = 12;
print(~a);      // -13（2の補数）

let c: u8 = 15;   // 2進数で00001111
print(~c);        // 240（u8で11110000）
```

### ビット演算の例

**符号なし型での例：**
```hemlock
let c: u8 = 15;   // 2進数で00001111
let d: u8 = 7;    // 2進数で00000111

print(c & d);     // 7（00000111）
print(c | d);     // 15（00001111）
print(c ^ d);     // 8（00001000）
print(~c);        // 240（u8で11110000）
```

**型の保持：**
```hemlock
// ビット演算はオペランドの型を保持
let x: u8 = 255;
let result = ~x;  // resultは値0のu8

let y: i32 = 100;
let result2 = y << 2;  // result2は値400のi32
```

**一般的なパターン：**
```hemlock
// ビットが設定されているか確認
if (flags & 0x04) {
    print("bit 2 is set");
}

// ビットを設定
flags = flags | 0x08;

// ビットをクリア
flags = flags & ~0x02;

// ビットをトグル
flags = flags ^ 0x01;
```

### 演算子の優先順位

ビット演算子はCスタイルの優先順位に従います：

1. `~`（単項NOT）- 最高、`!`と`-`と同レベル
2. `<<`、`>>`（シフト）- 比較より高く、`+`/`-`より低い
3. `&`（ビットAND）- `^`と`|`より高い
4. `^`（ビットXOR）- `&`と`|`の間
5. `|`（ビットOR）- `&`と`^`より低く、`&&`より高い
6. `&&`、`||`（論理）- 最低優先順位

**例：**
```hemlock
// &は|より優先順位が高い
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// シフトはビット演算子より優先順位が高い
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// 明確さのために括弧を使用
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**重要な注意：**
- ビット演算子は整数型のみで動作（浮動小数点数、文字列などでは動作しない）
- 型の昇格は標準ルールに従う（小さい型は大きい型に昇格）
- 右シフト（`>>`）は符号付き型では算術シフト、符号なし型では論理シフト
- シフト量は範囲チェックされない（大きなシフトの動作はプラットフォーム依存）

## 演算子の優先順位（完全版）

最高から最低への優先順位：

1. **単項**：`!`、`-`、`~`
2. **乗法**：`*`、`/`、`%`
3. **加法**：`+`、`-`
4. **シフト**：`<<`、`>>`
5. **関係**：`<`、`>`、`<=`、`>=`
6. **等価**：`==`、`!=`
7. **ビットAND**：`&`
8. **ビットXOR**：`^`
9. **ビットOR**：`|`
10. **論理AND**：`&&`
11. **論理OR**：`||`

**明確さのために括弧を使用：**
```hemlock
// 不明確
if (a || b && c) { }

// 明確
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## よくあるパターン

### パターン：入力検証

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### パターン：範囲チェック

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("valid score");
}
```

### パターン：状態マシン

```hemlock
let state = "start";

while (true) {
    switch (state) {
        case "start":
            print("Starting...");
            state = "running";
            break;

        case "running":
            if (should_pause) {
                state = "paused";
            } else if (should_stop) {
                state = "stopped";
            }
            break;

        case "paused":
            if (should_resume) {
                state = "running";
            }
            break;

        case "stopped":
            print("Stopped");
            break;
    }

    if (state == "stopped") {
        break;
    }
}
```

### パターン：フィルタリング付き反復

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 偶数のみを出力
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // 奇数をスキップ
    }
    print(arr[i]);
}
```

### パターン：早期終了

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // 早期終了
        }
    }
    return -1;  // 見つからない
}
```

## ベストプラクティス

1. **常にブレースを使用** - 単一文ブロックでも（構文で強制）
2. **明示的な条件** - 明確さのために`!x`ではなく`x == 0`を使用
3. **深いネストを避ける** - ネストした条件を関数に抽出
4. **早期returnを使用** - ガード句でネストを減らす
5. **複雑な条件を分割** - 名前付き真偽値変数に分割
6. **switchでdefault** - 常にdefaultケースを含める
7. **フォールスルーにコメント** - 意図的なフォールスルーを明示

## よくある落とし穴

### 落とし穴：条件内の代入

```hemlock
// これは許可されていない（条件内の代入なし）
if (x = 10) { }  // エラー：構文エラー

// 代わりに比較を使用
if (x == 10) { }  // OK
```

### 落とし穴：switch内のBreak忘れ

```hemlock
// 意図しないフォールスルー
switch (x) {
    case 1:
        print("one");
        // breakがない - フォールスルー！
    case 2:
        print("two");  // 1と2の両方で実行
        break;
}

// 修正：breakを追加
switch (x) {
    case 1:
        print("one");
        break;  // これで正しい
    case 2:
        print("two");
        break;
}
```

### 落とし穴：ループ変数のスコープ

```hemlock
// iはループにスコープされている
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // エラー：iはここで定義されていない
```

## 例

### 例：FizzBuzz

```hemlock
for (let i = 1; i <= 100; i = i + 1) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else if (i % 3 == 0) {
        print("Fizz");
    } else if (i % 5 == 0) {
        print("Buzz");
    } else {
        print(i);
    }
}
```

### 例：素数チェッカー

```hemlock
fn is_prime(n: i32): bool {
    if (n < 2) {
        return false;
    }

    let i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
```

### 例：メニューシステム

```hemlock
fn menu() {
    while (true) {
        print("1. Start");
        print("2. Settings");
        print("3. Exit");

        let choice = get_input();

        switch (choice) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Goodbye!");
                return;
            default:
                print("Invalid choice");
                break;
        }
    }
}
```

## 関連トピック

- [関数](functions.md) - 関数呼び出しとreturnを使った制御フロー
- [エラーハンドリング](error-handling.md) - 例外を使った制御フロー
- [型](types.md) - 条件での型変換

## 参照

- **構文**：文の構文の詳細は[構文](syntax.md)を参照
- **演算子**：演算での型の昇格は[型](types.md)を参照
