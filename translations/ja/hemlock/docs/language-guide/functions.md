# 関数

Hemlockの関数は、変数に代入したり、引数として渡したり、他の関数から返したりできる**第一級の値**です。このガイドでは、関数の構文、クロージャ、再帰、高度なパターンについて説明します。

## 概要

```hemlock
// 名前付き関数の構文
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// 無名関数
let multiply = fn(x, y) {
    return x * y;
};

// クロージャ
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## 関数宣言

### 名前付き関数

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**構成要素：**
- `fn` - 関数キーワード
- `greet` - 関数名
- `(name: string)` - オプションの型付きパラメータ
- `: string` - オプションの戻り値の型
- `{ ... }` - 関数本体

### 無名関数

名前のない関数で、変数に代入します：

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**名前付き vs. 無名：**
```hemlock
// これらは等価：
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**注意：** 名前付き関数は、無名関数を使った変数代入に脱糖されます。

## パラメータ

### 基本パラメータ

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### 型注釈

パラメータへのオプションの型注釈：

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // 実行時の型チェックでf64に昇格
```

**型チェック：**
- 注釈がある場合、パラメータの型は呼び出し時にチェックされる
- 暗黙の型変換は標準の昇格ルールに従う
- 型の不一致は実行時エラーを引き起こす

### 値渡し

すべての引数は**コピー**されます（値渡し）：

```hemlock
fn modify(x) {
    x = 100;  // ローカルコピーのみを変更
}

let a = 10;
modify(a);
print(a);  // まだ10（変更されていない）
```

**注意：** オブジェクトと配列は参照で渡されます（参照がコピーされる）ので、その内容は変更できます：

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // 元の配列を変更
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99（変更された）
```

## 戻り値

### Return文

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### 戻り値の型注釈

戻り値のオプションの型注釈：

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**型チェック：**
- 戻り値の型は関数が戻るときにチェックされる（注釈がある場合）
- 型変換は標準の昇格ルールに従う

### 暗黙のReturn

戻り値の型注釈がない関数は暗黙的に`null`を返します：

```hemlock
fn print_message(msg) {
    print(msg);
    // 暗黙的にnullを返す
}

let result = print_message("hello");  // resultはnull
```

### 早期Return

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // 早期終了
        }
    }
    return -1;  // 見つからない
}
```

### 値なしのReturn

値なしの`return;`は`null`を返します：

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // nullを返す
    }
    return value * 2;
}
```

## 第一級関数

関数は他の値と同様に、代入、渡し、返すことができます。

### 変数としての関数

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// 再代入
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### 引数としての関数

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### 戻り値としての関数

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## クロージャ

関数は定義環境をキャプチャします（レキシカルスコープ）。

### 基本的なクロージャ

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

**動作の仕組み：**
- 内部関数は外側のスコープから`count`をキャプチャ
- `count`は返された関数の呼び出し間で持続
- `makeCounter()`の各呼び出しは独自の`count`を持つ新しいクロージャを作成

### パラメータを持つクロージャ

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### 複数のクロージャ

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### レキシカルスコープ

関数はレキシカルスコープを通じて外側のスコープ変数にアクセスできます：

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // globalとouter_varにアクセス可能
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

クロージャは変数を参照でキャプチャするため、外側のスコープ変数の読み取りと変更の両方が可能です（上記の`makeCounter`の例を参照）。

## 再帰

関数は自分自身を呼び出すことができます。

### 基本的な再帰

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### 相互再帰

関数は互いを呼び出すことができます：

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### 再帰的データ処理

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**注意：** 末尾呼び出し最適化はまだありません - 深い再帰はスタックオーバーフローを引き起こす可能性があります。

## 高階関数

他の関数を受け取るか返す関数。

### Mapパターン

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Filterパターン

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Reduceパターン

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### 関数合成

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## よくあるパターン

### パターン：ファクトリ関数

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### パターン：コールバック関数

```hemlock
fn process_async(data, callback) {
    // ... 処理を行う
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### パターン：部分適用

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### パターン：メモ化

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // キャッシュによりはるかに高速
```

## 関数のセマンティクス

### 戻り値の型の要件

戻り値の型注釈がある関数は**必ず**値を返す必要があります：

```hemlock
fn get_value(): i32 {
    // エラー：return文がない
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### 型チェック

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // f64に昇格、f64を返す
add("a", "b");     // 実行時エラー：型の不一致
```

### スコープルール

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // アクセス可能：inner_var、outer_var、global
    }

    // アクセス可能：outer_var、global
    // アクセス不可：inner_var
}

// アクセス可能：global
// アクセス不可：outer_var、inner_var
```

## ベストプラクティス

1. **型注釈を使用** - エラーのキャッチと意図の文書化に役立つ
2. **関数を小さく保つ** - 各関数は1つのことを行う
3. **純粋関数を優先** - 可能な限り副作用を避ける
4. **関数に明確な名前を付ける** - 説明的な動詞の名前を使用
5. **早期returnを使用** - ガード句でネストを減らす
6. **複雑なクロージャを文書化** - キャプチャされた変数を明確にする
7. **深い再帰を避ける** - 末尾呼び出し最適化がまだない

## よくある落とし穴

### 落とし穴：再帰の深さ

```hemlock
// 深い再帰はスタックオーバーフローを引き起こす可能性がある
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // スタックオーバーフローでクラッシュする可能性
```

### 落とし穴：キャプチャされた変数の変更

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // キャプチャされた変数の読み取りと変更が可能
        return count;
    };
}
```

**注意：** これは機能しますが、すべてのクロージャが同じキャプチャされた環境を共有することに注意してください。

## 例

### 例：関数パイプライン

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### 例：イベントハンドラ

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clicked: " + data);
});

trigger_event("click", "button1");
```

### 例：カスタムコンパレータによるソート

```hemlock
fn sort(arr, compare) {
    // カスタムコンパレータによるバブルソート
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## オプションパラメータ（デフォルト引数）

関数は`?:`構文を使用してデフォルト値を持つオプションパラメータを持つことができます：

```hemlock
fn greet(name, greeting?: "Hello") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Hello Alice"
print(greet("Bob", "Hi"));       // "Hi Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**ルール：**
- オプションパラメータは必須パラメータの後に来る必要がある
- デフォルト値は任意の式でよい
- 省略された引数はデフォルト値を使用

## 可変長引数関数（残余パラメータ）

関数は残余パラメータ（`...`）を使用して可変数の引数を受け取ることができます：

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Starting", "Running", "Done");
// INFO: Starting
// INFO: Running
// INFO: Done
```

**ルール：**
- 残余パラメータは最後のパラメータである必要がある
- 残余パラメータは残りのすべての引数を配列に収集
- 通常のパラメータやオプションパラメータと組み合わせ可能

## 関数型注釈

関数型により、関数パラメータと戻り値に期待される正確なシグネチャを指定できます：

### 基本的な関数型

```hemlock
// 関数型の構文：fn(パラメータの型): 戻り値の型
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### 高階関数型

```hemlock
// 関数を返す関数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### 非同期関数型

```hemlock
// 非同期関数型
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### 関数型エイリアス

```hemlock
// 明確さのために名前付き関数型を作成
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Constパラメータ

`const`修飾子は、関数内でパラメータが変更されることを防ぎます：

### 基本的なConstパラメータ

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // エラー：constパラメータを変更できない
    for (item in items) {
        print(item);   // OK：読み取りは許可
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### 深い不変性

Constパラメータは深い不変性を強制します - いかなるパスからも変更できません：

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK：読み取りは許可
    // person.name = "Bob";   // エラー：変更できない
    // person.address.city = "NYC";  // エラー：深いconst
}
```

### Constが防ぐもの

| 型 | Constでブロックされるもの | 許可されるもの |
|------|-----------------|---------|
| array | push、pop、shift、unshift、insert、remove、clear、reverse | slice、concat、map、filter、find、contains |
| object | フィールド代入 | フィールド読み取り |
| buffer | インデックス代入 | インデックス読み取り |
| string | インデックス代入 | すべてのメソッド（新しい文字列を返す） |

## 名前付き引数

関数は明確さと柔軟性のために名前付き引数で呼び出すことができます：

### 基本的な名前付き引数

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// 位置引数（従来の方法）
create_user("Alice", 25, false);

// 名前付き引数 - 任意の順序で可能
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### 位置引数と名前付き引数の混合

```hemlock
// 必要なものに名前を付けてオプションパラメータをスキップ
create_user("David", active: false);  // デフォルトのage=18を使用

// 名前付き引数は位置引数の後に来る必要がある
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // エラー：名前付き引数の後に位置引数
```

### 名前付き引数のルール

- 名前付き引数には`名前: 値`構文を使用
- 名前付き引数は位置引数の後に任意の順序で指定可能
- 位置引数は名前付き引数の後に来ることはできない
- デフォルト/オプションパラメータと連携
- 不明なパラメータ名は実行時エラーを引き起こす

## 制限事項

現在の制限事項：

- **参照渡しなし** - `ref`キーワードはパースされるが未実装
- **関数のオーバーロードなし** - 1つの名前に1つの関数
- **末尾呼び出し最適化なし** - 深い再帰はスタックサイズで制限

## 関連トピック

- [制御フロー](control-flow.md) - 制御構造での関数の使用
- [オブジェクト](objects.md) - メソッドはオブジェクトに格納された関数
- [エラーハンドリング](error-handling.md) - 関数と例外処理
- [型](types.md) - 型注釈と変換

## 参照

- **クロージャ**：クロージャのセマンティクスについてはCLAUDE.mdの「Functions」セクションを参照
- **第一級の値**：関数は他の値と同様の値
- **レキシカルスコープ**：関数は定義環境をキャプチャ
