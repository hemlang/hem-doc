# 配列

Hemlockは、データ操作と処理のための包括的なメソッドを備えた**動的配列**を提供します。配列は混合型を保持でき、必要に応じて自動的に拡張されます。

## 概要

```hemlock
// 配列リテラル
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// 混合型を許可
let mixed = [1, "hello", true, null];

// 動的サイズ変更
arr.push(6);           // 自動的に拡張
arr.push(7);
print(arr.length);     // 7
```

## 配列リテラル

### 基本構文

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### 空の配列

```hemlock
let arr = [];  // 空の配列

// 後で要素を追加
arr.push(1);
arr.push(2);
arr.push(3);
```

### 混合型

配列は異なる型を含むことができます：

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3]（ネストされた配列）
```

### ネストされた配列

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### 型付き配列

配列には要素の型を強制する型注釈を付けることができます：

```hemlock
// 型付き配列の構文
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// 実行時の型チェック
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "two", 3]; // 実行時エラー：型の不一致

// ネストされた型付き配列
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**型注釈の動作：**
- 要素は配列に追加される際に型チェックされます
- 型の不一致は実行時エラーを引き起こします
- 型注釈がない場合、配列は混合型を受け入れます

## インデックス

### 要素の読み取り

ゼロインデックスアクセス：

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10（最初の要素）
print(arr[4]);  // 50（最後の要素）

// 範囲外はnullを返す（エラーなし）
print(arr[10]);  // null
```

### 要素の書き込み

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // 既存を変更
arr[1] = 20;
print(arr);     // [10, 20, 3]

// 現在の長さを超えて代入可能（配列を拡張）
arr[5] = 60;    // [10, 20, 3, null, null, 60]を作成
```

### 負のインデックス

**サポートされていません** - 正のインデックスのみを使用：

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // エラーまたは未定義動作

// 最後の要素にはlengthを使用
print(arr[arr.length - 1]);  // 3
```

## プロパティ

### `.length`プロパティ

要素数を返します：

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// 空の配列
let empty = [];
print(empty.length);  // 0

// 変更後
arr.push(6);
print(arr.length);  // 6
```

## 配列メソッド

Hemlockは包括的な操作のための18個の配列メソッドを提供します。

### スタック操作

**`push(value)`** - 末尾に要素を追加：
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - 最後の要素を削除して返す：
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // 5を返し、arrは[1, 2, 3, 4]になる

print(last);           // 5
print(arr.length);     // 4
```

### キュー操作

**`shift()`** - 最初の要素を削除して返す：
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // 1を返し、arrは[2, 3]になる

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - 先頭に要素を追加：
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### 挿入と削除

**`insert(index, value)`** - インデックス位置に要素を挿入：
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // インデックス2に3を挿入：[1, 2, 3, 4, 5]

arr.insert(0, 0);      // 先頭に挿入：[0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - インデックス位置の要素を削除して返す：
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // 3を返し、arrは[1, 2, 4, 5]になる

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### 検索操作

**`find(value)`** - 最初の出現位置を検索：
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2（最初の出現のインデックス）
let idx2 = arr.find(99);     // -1（見つからない）

// 任意の型で動作
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - 配列に値が含まれるか確認：
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### 抽出操作

**`slice(start, end)`** - 部分配列を抽出（endは含まない）：
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]（インデックス1, 2, 3）
let first = arr.slice(0, 2); // [1, 2]

// 元の配列は変更されない
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - 最初の要素を取得（削除せずに）：
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1（削除せずに）
print(arr);                  // [1, 2, 3]（変更なし）
```

**`last()`** - 最後の要素を取得（削除せずに）：
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3（削除せずに）
print(arr);                  // [1, 2, 3]（変更なし）
```

### 変換操作

**`reverse()`** - 配列をその場で反転：
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1]（変更された）
```

**`join(delimiter)`** - 要素を文字列に結合：
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// 混合型でも動作
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - 別の配列と連結：
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]（新しい配列）

// 元の配列は変更されない
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### ユーティリティ操作

**`clear()`** - すべての要素を削除：
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## メソッドチェーン

配列や値を返すメソッドはチェーンが可能です：

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## 完全なメソッドリファレンス

| メソッド | パラメータ | 戻り値 | 変更 | 説明 |
|--------|-----------|---------|---------|-------------|
| `push(value)` | any | void | はい | 末尾に要素を追加 |
| `pop()` | - | any | はい | 最後を削除して返す |
| `shift()` | - | any | はい | 最初を削除して返す |
| `unshift(value)` | any | void | はい | 先頭に要素を追加 |
| `insert(index, value)` | i32, any | void | はい | インデックス位置に挿入 |
| `remove(index)` | i32 | any | はい | インデックス位置を削除して返す |
| `find(value)` | any | i32 | いいえ | 最初の出現位置を検索（見つからない場合-1） |
| `contains(value)` | any | bool | いいえ | 値が含まれるか確認 |
| `slice(start, end)` | i32, i32 | array | いいえ | 部分配列を抽出（新しい配列） |
| `join(delimiter)` | string | string | いいえ | 文字列に結合 |
| `concat(other)` | array | array | いいえ | 連結（新しい配列） |
| `reverse()` | - | void | はい | その場で反転 |
| `first()` | - | any | いいえ | 最初の要素を取得 |
| `last()` | - | any | いいえ | 最後の要素を取得 |
| `clear()` | - | void | はい | すべての要素を削除 |
| `map(callback)` | fn | array | いいえ | 各要素を変換 |
| `filter(predicate)` | fn | array | いいえ | 条件に一致する要素を選択 |
| `reduce(callback, initial)` | fn, any | any | いいえ | 単一の値に畳み込み |

## 実装の詳細

### メモリモデル

- **ヒープ割り当て** - 動的容量
- **自動拡張** - 容量を超えると2倍に拡張
- **自動縮小なし** - 容量は減少しない
- **インデックスの境界チェックなし** - 安全のためにはメソッドを使用

### 容量管理

```hemlock
let arr = [];  // 初期容量：0

arr.push(1);   // 容量1に拡張
arr.push(2);   // 容量2に拡張
arr.push(3);   // 容量4に拡張（2倍）
arr.push(4);   // まだ容量4
arr.push(5);   // 容量8に拡張（2倍）
```

### 値の比較

`find()`と`contains()`は値の等価性を使用：

```hemlock
// プリミティブ：値で比較
let arr = [1, 2, 3];
arr.contains(2);  // true

// 文字列：値で比較
let words = ["hello", "world"];
words.contains("hello");  // true

// オブジェクト：参照で比較
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true（同じ参照）
arr2.contains(obj2);  // false（異なる参照）
```

## よくあるパターン

### 関数型操作（map/filter/reduce）

配列には組み込みの`map`、`filter`、`reduce`メソッドがあります：

```hemlock
// map - 各要素を変換
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - 条件に一致する要素を選択
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - 単一の値に畳み込み
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// 関数型操作のチェーン
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### パターン：スタックとしての配列

```hemlock
let stack = [];

// スタックにプッシュ
stack.push(1);
stack.push(2);
stack.push(3);

// スタックからポップ
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### パターン：キューとしての配列

```hemlock
let queue = [];

// エンキュー（末尾に追加）
queue.push(1);
queue.push(2);
queue.push(3);

// デキュー（先頭から削除）
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## ベストプラクティス

1. **直接インデックスよりメソッドを使用** - 境界チェックと明確性
2. **境界をチェック** - 直接インデックスは境界チェックしない
3. **不変操作を優先** - 変更より`slice()`と`concat()`を使用
4. **容量を初期化** - サイズが分かっている場合（現在はサポートされていない）
5. **メンバーシップには`contains()`を使用** - 手動ループより明確
6. **メソッドをチェーン** - ネストされた呼び出しより読みやすい

## よくある落とし穴

### 落とし穴：直接インデックスの範囲外

```hemlock
let arr = [1, 2, 3];

// 境界チェックなし！
arr[10] = 99;  // nullを含むスパース配列を作成
print(arr.length);  // 11（3ではない！）

// 改善：push()を使用するか長さをチェック
if (arr.length <= 10) {
    arr.push(99);
}
```

### 落とし穴：変更 vs. 新しい配列

```hemlock
let arr = [1, 2, 3];

// 元を変更
arr.reverse();
print(arr);  // [3, 2, 1]

// 新しい配列を返す
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1]（変更なし）
print(sub);  // [3, 2]
```

### 落とし穴：参照の等価性

```hemlock
let obj = { x: 10 };
let arr = [obj];

// 同じ参照：true
arr.contains(obj);  // true

// 異なる参照：false
arr.contains({ x: 10 });  // false（異なるオブジェクト）
```

### 落とし穴：長期間存続する配列

```hemlock
// ローカルスコープの配列は自動解放されるが、グローバル/長期間の配列は注意が必要
let global_cache = [];  // モジュールレベル、プログラム終了まで持続

fn add_to_cache(item) {
    global_cache.push(item);  // 無限に拡大
}

// 長期間のデータには、以下を検討：
// - 定期的に配列をクリア：global_cache.clear();
// - 完了時に早期解放：free(global_cache);
```

## 例

### 例：配列の統計

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### 例：配列の重複排除

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### 例：配列のチャンク分割

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### 例：配列のフラット化

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // ネストされた配列 - フラット化
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### 例：ソート（バブルソート）

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // スワップ
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // その場で変更
print(numbers);  // [1, 2, 5, 8, 9]
```

## 制限事項

現在の制限事項：

- **インデックスの境界チェックなし** - 直接アクセスはチェックされない
- **オブジェクトの参照等価性** - `find()`と`contains()`は参照比較を使用
- **配列の分割代入なし** - `let [a, b] = arr`構文はない
- **スプレッド演算子なし** - `[...arr1, ...arr2]`構文はない

**注意：** 配列は参照カウントされ、スコープを抜けると自動的に解放されます。詳細は[メモリ管理](memory.md#internal-reference-counting)を参照してください。

## 関連トピック

- [文字列](strings.md) - 配列メソッドに似た文字列メソッド
- [オブジェクト](objects.md) - 配列もオブジェクトのような性質を持つ
- [関数](functions.md) - 配列での高階関数
- [制御フロー](control-flow.md) - 配列の反復処理

## 参照

- **動的サイズ変更**: 配列は容量を2倍にしながら自動的に拡張
- **メソッド**: map/filter/reduceを含む18個の包括的なメソッド
- **メモリ**: 配列の割り当ての詳細は[メモリ](memory.md)を参照
