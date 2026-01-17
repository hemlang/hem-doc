# パターンマッチング

Hemlockは`match`式による強力なパターンマッチングを提供し、値の分解、型のチェック、複数のケースの処理を簡潔に行う方法を提供します。

## 基本構文

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

Match式は`value`を各パターンに順番に評価し、最初にマッチしたアームの式の結果を返します。

## パターンの種類

### リテラルパターン

正確な値にマッチ：

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "one",
    42 => "the answer",
    _ => "other"
};
print(msg);  // "the answer"
```

サポートされるリテラル：
- **整数**：`0`、`42`、`-5`
- **浮動小数点数**：`3.14`、`-0.5`
- **文字列**：`"hello"`、`"world"`
- **真偽値**：`true`、`false`
- **Null**：`null`

### ワイルドカードパターン（`_`）

バインドせずに任意の値にマッチ：

```hemlock
let x = "anything";
let result = match (x) {
    "specific" => "found it",
    _ => "wildcard matched"
};
```

### 変数バインディングパターン

マッチした値を変数にバインド：

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "value is " + n  // nは100にバインド
};
print(result);  // "value is 100"
```

### ORパターン（`|`）

複数の選択肢にマッチ：

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "small",
    4 | 5 | 6 => "medium",
    _ => "large"
};

// 文字列でも動作
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "exiting",
    "help" | "h" | "?" => "showing help",
    _ => "unknown"
};
```

### ガード式（`if`）

パターンに条件を追加：

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negative",
    n if n == 0 => "zero",
    n if n < 10 => "small",
    n if n < 100 => "medium",
    n => "large: " + n
};
print(category);  // "medium"

// 複雑なガード
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "even and greater than 10",
    n if n % 2 == 0 => "even",
    n => "odd"
};
```

### 型パターン

型に基づいてチェックとバインド：

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "integer: " + num,
    str: string => "string: " + str,
    flag: bool => "boolean: " + flag,
    _ => "other type"
};
print(desc);  // "integer: 42"
```

サポートされる型：`i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`string`、`array`、`object`

## 分解パターン

### オブジェクトの分解

オブジェクトからフィールドを抽出：

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "point at " + x + "," + y
};
print(result);  // "point at 10,20"

// リテラルフィールド値を使用
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origin",
    { x: 0, y } => "on y-axis at " + y,
    { x, y: 0 } => "on x-axis at " + x,
    { x, y } => "point at " + x + "," + y
};
print(name);  // "origin"
```

### 配列の分解

配列の構造と要素にマッチ：

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "empty",
    [x] => "single: " + x,
    [x, y] => "pair: " + x + "," + y,
    [x, y, z] => "triple: " + x + "," + y + "," + z,
    _ => "many elements"
};
print(desc);  // "triple: 1,2,3"

// リテラル値を使用
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "both zero",
    [1, x] => "starts with 1, second is " + x,
    [x, 1] => "ends with 1",
    _ => "other"
};
print(result);  // "starts with 1, second is 2"
```

### 配列の残余パターン（`...`）

残りの要素をキャプチャ：

```hemlock
let nums = [1, 2, 3, 4, 5];

// 先頭と残り
let result = match (nums) {
    [first, ...rest] => "first: " + first,
    [] => "empty"
};
print(result);  // "first: 1"

// 最初の2要素
let result2 = match (nums) {
    [a, b, ...rest] => "first two: " + a + "," + b,
    _ => "too short"
};
print(result2);  // "first two: 1,2"
```

### ネストされた分解

複雑なデータのためにパターンを組み合わせ：

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " lives in " + city,
    _ => "unknown"
};
print(result);  // "Alice lives in NYC"

// 配列を含むオブジェクト
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "first: " + first + ", total: " + count,
    _ => "no items"
};
print(result2);  // "first: 1, total: 3"
```

## 式としてのMatch

Matchは値を返す式です：

```hemlock
// 直接代入
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// 文字列連結内
let msg = "Grade: " + match (grade) {
    n if n >= 70 => "passing",
    _ => "failing"
};

// 関数のreturn内
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positive",
        _ => "negative"
    };
}
```

## パターンマッチングのベストプラクティス

1. **順序が重要**：パターンは上から下にチェックされる；具体的なパターンを一般的なパターンの前に配置
2. **網羅性のためにワイルドカードを使用**：すべてのケースがカバーされていると確信がない限り、常に`_`フォールバックを含める
3. **ネストした条件よりガードを優先**：ガードは意図をより明確にする
4. **手動フィールドアクセスより分解を使用**：より簡潔で安全

```hemlock
// 良い：範囲チェックにガード
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "below B"
}

// 良い：フィールドアクセスの代わりに分解
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// 避ける：過度に複雑なネストされたパターン
// 代わりに、複数のmatchに分割するかガードを使用することを検討
```

## 他の言語との比較

| 機能 | Hemlock | Rust | JavaScript |
|---------|---------|------|------------|
| 基本的なマッチング | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| 分解 | はい | はい | 部分的（switchは分解しない） |
| ガード | `n if n > 0 =>` | `n if n > 0 =>` | なし |
| ORパターン | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| 残余パターン | `[a, ...rest]` | `[a, rest @ ..]` | なし |
| 型パターン | `n: i32` | `match`アームで型 | なし |
| 値を返す | はい | はい | いいえ（文） |

## 実装に関する注意

パターンマッチングはインタープリタとコンパイラの両方のバックエンドで完全なパリティを持って実装されています - 両方とも同じ入力に対して同一の結果を生成します。この機能はHemlock v1.8.0以降で利用可能です。
