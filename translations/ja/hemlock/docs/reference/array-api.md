# 配列APIリファレンス

Hemlockの配列型と全18個の配列メソッドの完全なリファレンスです。

---

## 概要

Hemlockの配列は**動的でヒープ割り当て**されるシーケンスであり、混合型を保持できます。データ操作と処理のための包括的なメソッドを提供します。

**主な機能：**
- 動的サイズ（自動拡張）
- ゼロインデックス
- 混合型を許可
- 18個の組み込みメソッド
- 容量追跡付きヒープ割り当て

---

## 配列型

**型：** `array`

**プロパティ：**
- `.length` - 要素数（i32）

**リテラル構文：** 角括弧 `[elem1, elem2, ...]`

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// 混合型
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// 空配列
let empty = [];
print(empty.length);   // 0
```

---

## インデックス

配列は`[]`を使用したゼロベースのインデックスをサポートします：

**読み取りアクセス：**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**書き込みアクセス：**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**注意：** 直接インデックスには境界チェックがありません。安全のためにはメソッドを使用してください。

---

## 配列プロパティ

### .length

配列の要素数を取得します。

**型：** `i32`

**例：**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// 長さは動的に変化
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## 配列メソッド

### スタック操作

#### push

配列の末尾に要素を追加します。

**シグネチャ：**
```hemlock
array.push(value: any): null
```

**パラメータ：**
- `value` - 追加する要素

**戻り値：** `null`

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

最後の要素を削除して返します。

**シグネチャ：**
```hemlock
array.pop(): any
```

**戻り値：** 最後の要素（配列から削除される）

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**エラー：** 配列が空の場合は実行時エラー。

---

### キュー操作

#### shift

最初の要素を削除して返します。

**シグネチャ：**
```hemlock
array.shift(): any
```

**戻り値：** 最初の要素（配列から削除される）

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**エラー：** 配列が空の場合は実行時エラー。

---

#### unshift

配列の先頭に要素を追加します。

**シグネチャ：**
```hemlock
array.unshift(value: any): null
```

**パラメータ：**
- `value` - 追加する要素

**戻り値：** `null`

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### 挿入と削除

#### insert

特定のインデックスに要素を挿入します。

**シグネチャ：**
```hemlock
array.insert(index: i32, value: any): null
```

**パラメータ：**
- `index` - 挿入する位置（0ベース）
- `value` - 挿入する要素

**戻り値：** `null`

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// 末尾に挿入
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**動作：** インデックス以降の要素を右にシフトします。

---

#### remove

インデックスの要素を削除して返します。

**シグネチャ：**
```hemlock
array.remove(index: i32): any
```

**パラメータ：**
- `index` - 削除する位置（0ベース）

**戻り値：** 削除された要素

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**動作：** インデックス以降の要素を左にシフトします。

**エラー：** インデックスが範囲外の場合は実行時エラー。

---

### 検索と検出

#### find

値の最初の出現位置を見つけます。

**シグネチャ：**
```hemlock
array.find(value: any): i32
```

**パラメータ：**
- `value` - 検索する値

**戻り値：** 最初の出現のインデックス、見つからない場合は`-1`

**例：**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1（見つからない）

// 最初の重複を見つける
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1（最初の出現）
```

**比較：** プリミティブと文字列には値の等価性を使用します。

---

#### contains

配列が値を含むかチェックします。

**シグネチャ：**
```hemlock
array.contains(value: any): bool
```

**パラメータ：**
- `value` - 検索する値

**戻り値：** 見つかった場合は`true`、それ以外は`false`

**例：**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// 文字列でも動作
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### スライスと抽出

#### slice

範囲で部分配列を抽出します（終了は含まない）。

**シグネチャ：**
```hemlock
array.slice(start: i32, end: i32): array
```

**パラメータ：**
- `start` - 開始インデックス（0ベース、含む）
- `end` - 終了インデックス（含まない）

**戻り値：** [start, end)の要素を含む新しい配列

**変更：** なし（新しい配列を返す）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// 空のスライス
let empty = arr.slice(2, 2); // []
```

---

#### first

最初の要素を削除せずに取得します。

**シグネチャ：**
```hemlock
array.first(): any
```

**戻り値：** 最初の要素

**変更：** なし

**例：**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3]（変更なし）
```

**エラー：** 配列が空の場合は実行時エラー。

---

#### last

最後の要素を削除せずに取得します。

**シグネチャ：**
```hemlock
array.last(): any
```

**戻り値：** 最後の要素

**変更：** なし

**例：**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3]（変更なし）
```

**エラー：** 配列が空の場合は実行時エラー。

---

### 配列操作

#### reverse

配列をその場で反転します。

**シグネチャ：**
```hemlock
array.reverse(): null
```

**戻り値：** `null`

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

配列からすべての要素を削除します。

**シグネチャ：**
```hemlock
array.clear(): null
```

**戻り値：** `null`

**変更：** はい（配列をその場で変更）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### 配列結合

#### concat

別の配列と連結します。

**シグネチャ：**
```hemlock
array.concat(other: array): array
```

**パラメータ：**
- `other` - 連結する配列

**戻り値：** 両方の配列の要素を含む新しい配列

**変更：** なし（新しい配列を返す）

**例：**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3]（変更なし）
print(b);                    // [4, 5, 6]（変更なし）

// 連結のチェーン
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### 関数型操作

#### map

コールバック関数を使用して各要素を変換します。

**シグネチャ：**
```hemlock
array.map(callback: fn): array
```

**パラメータ：**
- `callback` - 要素を受け取り変換された値を返す関数

**戻り値：** 変換された要素を含む新しい配列

**変更：** なし（新しい配列を返す）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

述語に一致する要素を選択します。

**シグネチャ：**
```hemlock
array.filter(predicate: fn): array
```

**パラメータ：**
- `predicate` - 要素を受け取りboolを返す関数

**戻り値：** 述語がtrueを返した要素を含む新しい配列

**変更：** なし（新しい配列を返す）

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

アキュムレータを使用して配列を単一の値に削減します。

**シグネチャ：**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**パラメータ：**
- `callback` - (アキュムレータ, 要素)を受け取り新しいアキュムレータを返す関数
- `initial` - アキュムレータの初期値

**戻り値：** 最終的な累積値

**変更：** なし

**例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// 最大値を見つける
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### 文字列変換

#### join

区切り文字で要素を文字列に結合します。

**シグネチャ：**
```hemlock
array.join(delimiter: string): string
```

**パラメータ：**
- `delimiter` - 要素間に配置する文字列

**戻り値：** すべての要素を結合した文字列

**例：**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// 混合型でも動作
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// 空の区切り文字
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**動作：** すべての要素を自動的に文字列に変換します。

---

## メソッドチェーン

配列メソッドは簡潔な操作のためにチェーンできます：

**例：**
```hemlock
// sliceとjoinをチェーン
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// concatとsliceをチェーン
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// 複雑なチェーン
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## 完全なメソッド要約

### 変更メソッド

配列をその場で変更するメソッド：

| メソッド | シグネチャ | 戻り値 | 説明 |
|----------|--------------------------|-----------|--------------------------------|
| `push`     | `(value: any)`             | `null`    | 末尾に追加 |
| `pop`      | `()`                       | `any`     | 末尾から削除 |
| `shift`    | `()`                       | `any`     | 先頭から削除 |
| `unshift`  | `(value: any)`             | `null`    | 先頭に追加 |
| `insert`   | `(index: i32, value: any)` | `null`    | インデックスに挿入 |
| `remove`   | `(index: i32)`             | `any`     | インデックスから削除 |
| `reverse`  | `()`                       | `null`    | その場で反転 |
| `clear`    | `()`                       | `null`    | すべての要素を削除 |

### 非変更メソッド

元の配列を変更せずに新しい値を返すメソッド：

| メソッド | シグネチャ | 戻り値 | 説明 |
|----------|--------------------------|-----------|--------------------------------|
| `find`     | `(value: any)`             | `i32`     | 最初の出現を見つける |
| `contains` | `(value: any)`             | `bool`    | 値を含むかチェック |
| `slice`    | `(start: i32, end: i32)`   | `array`   | 部分配列を抽出 |
| `first`    | `()`                       | `any`     | 最初の要素を取得 |
| `last`     | `()`                       | `any`     | 最後の要素を取得 |
| `concat`   | `(other: array)`           | `array`   | 配列を連結 |
| `join`     | `(delimiter: string)`      | `string`  | 要素を文字列に結合 |
| `map`      | `(callback: fn)`           | `array`   | 各要素を変換 |
| `filter`   | `(predicate: fn)`          | `array`   | 一致する要素を選択 |
| `reduce`   | `(callback: fn, initial: any)` | `any` | 単一の値に削減 |

---

## 使用パターン

### スタック使用

```hemlock
let stack = [];

// 要素をプッシュ
stack.push(1);
stack.push(2);
stack.push(3);

// 要素をポップ
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### キュー使用

```hemlock
let queue = [];

// エンキュー
queue.push(1);
queue.push(2);
queue.push(3);

// デキュー
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### 配列変換

```hemlock
// フィルタ（手動）
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// マップ（手動）
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### 配列の構築

```hemlock
let arr = [];

// ループで配列を構築
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## 実装の詳細

**容量管理：**
- 配列は必要に応じて自動的に拡張
- 容量は超過時に2倍になる
- 手動の容量制御なし

**値の比較：**
- `find()`と`contains()`は値の等価性を使用
- プリミティブと文字列で正しく動作
- オブジェクト/配列は参照で比較

**メモリ：**
- ヒープ割り当て
- 自動解放なし（手動メモリ管理）
- 直接インデックスアクセスには境界チェックなし

---

## 関連項目

- [型システム](type-system.md) - 配列型の詳細
- [文字列API](string-api.md) - 文字列join()の結果
- [演算子](operators.md) - 配列インデックス演算子
