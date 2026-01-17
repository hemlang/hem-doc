# オブジェクト

HemlockはJavaScriptスタイルのオブジェクトを実装しており、ヒープ割り当て、動的フィールド、メソッド、ダックタイピングを備えています。オブジェクトはデータと動作を組み合わせた柔軟なデータ構造です。

## 概要

```hemlock
// 無名オブジェクト
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// メソッドを持つオブジェクト
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## オブジェクトリテラル

### 基本構文

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**構文：**
- 波括弧`{}`がオブジェクトを囲む
- キーと値のペアはカンマで区切る
- キーは識別子（引用符不要）
- 値は任意の型

### 空のオブジェクト

```hemlock
let obj = {};  // 空のオブジェクト

// 後でフィールドを追加
obj.name = "Alice";
obj.age = 30;
```

### ネストされたオブジェクト

```hemlock
let user = {
    info: {
        name: "Bob",
        age: 25
    },
    active: true,
    settings: {
        theme: "dark",
        notifications: true
    }
};

print(user.info.name);           // "Bob"
print(user.settings.theme);      // "dark"
```

### 混合型の値

```hemlock
let mixed = {
    number: 42,
    text: "hello",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### 短縮プロパティ構文

変数名がプロパティ名と一致する場合、短縮構文を使用：

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// 短縮：{ name } は { name: name } と等価
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**短縮と通常のプロパティを混合：**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### スプレッド演算子

スプレッド演算子（`...`）は1つのオブジェクトからすべてのフィールドを別のオブジェクトにコピーします：

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**スプレッドで値を上書き：**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark"（上書き）
print(custom.size);   // "medium"（デフォルトから）
print(custom.debug);  // false（デフォルトから）
```

**複数のスプレッド（後のスプレッドが前を上書き）：**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// 後のスプレッドが前を上書き
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**短縮とスプレッドを組み合わせ：**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**設定上書きパターン：**
```hemlock
let defaultConfig = {
    debug: false,
    timeout: 30,
    retries: 3
};

let prodConfig = { ...defaultConfig, timeout: 60 };
let devConfig = { ...defaultConfig, debug: true };

print(prodConfig.timeout);  // 60
print(devConfig.debug);     // true
```

**注意：** スプレッドは浅いコピーを実行します。ネストされたオブジェクトは参照を共有します：
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42（nested.innerと同じ参照）
```

## フィールドアクセス

### ドット記法

```hemlock
let person = { name: "Alice", age: 30 };

// フィールドを読み取り
let name = person.name;      // "Alice"
let age = person.age;        // 30

// フィールドを変更
person.age = 31;
print(person.age);           // 31
```

### 動的フィールド追加

実行時に新しいフィールドを追加：

```hemlock
let person = { name: "Alice" };

// 新しいフィールドを追加
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### フィールド削除

**注意：** フィールド削除は現在サポートされていません。代わりに`null`を設定：

```hemlock
let obj = { x: 10, y: 20 };

// フィールドを削除できない（サポートされていない）
// obj.x = undefined;  // Hemlockには'undefined'がない

// 回避策：nullを設定
obj.x = null;
```

## メソッドと`self`

### メソッドの定義

メソッドはオブジェクトフィールドに格納された関数です：

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
    decrement: fn() {
        self.count = self.count - 1;
    },
    get: fn() {
        return self.count;
    }
};
```

### `self`キーワード

関数がメソッドとして呼び出されると、`self`は自動的にオブジェクトにバインドされます：

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // selfはcounterを参照
    }
};

counter.increment();  // selfはcounterにバインド
print(counter.count);  // 1
```

**動作の仕組み：**
- メソッド呼び出しは関数式がプロパティアクセスかどうかをチェックして検出
- `self`は呼び出し時にオブジェクトに自動的にバインド
- `self`は読み取り専用（`self`自体を再代入できない）

### メソッド呼び出しの検出

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// メソッドとして呼び出し - selfがバインド
print(obj.method());  // 10

// 関数として呼び出し - selfはnull（エラー）
let f = obj.method;
print(f());  // エラー：selfが定義されていない
```

### パラメータを持つメソッド

```hemlock
let calculator = {
    result: 0,
    add: fn(x) {
        self.result = self.result + x;
    },
    multiply: fn(x) {
        self.result = self.result * x;
    },
    get: fn() {
        return self.result;
    }
};

calculator.add(5);
calculator.multiply(2);
print(calculator.get());  // 10
```

## `define`による型定義

### 基本的な型定義

`define`でオブジェクトの形状を定義：

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// オブジェクトを作成し型付き変数に代入
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // ダックタイピングが構造を検証

print(typeof(typed_p));  // "Person"
```

**`define`が行うこと：**
- 必須フィールドを持つ型を宣言
- ダックタイピング検証を有効に
- `typeof()`用のオブジェクトの型名を設定

### ダックタイピング

オブジェクトは**構造的互換性**を使用して`define`に対して検証されます：

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK：すべての必須フィールドを持つ
let p1: Person = { name: "Alice", age: 30 };

// OK：追加フィールドは許可
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// エラー：必須フィールド'age'がない
let p3: Person = { name: "Carol" };

// エラー：'age'の型が違う
let p4: Person = { name: "Dave", age: "thirty" };
```

**ダックタイピングのルール：**
- すべての必須フィールドが存在する必要がある
- フィールドの型が一致する必要がある
- 追加フィールドは許可され保持される
- 検証は代入時に行われる

### オプションフィールド

フィールドはデフォルト値でオプションにできます：

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // デフォルト値付きオプション
    nickname?: string,   // オプション、デフォルトはnull
}

// 必須フィールドのみのオブジェクト
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true（デフォルトが適用）
print(typed_p.nickname);  // null（デフォルトなし）

// オプションフィールドを上書き可能
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false（上書き）
```

**オプションフィールドの構文：**
- `field?: default_value` - デフォルト付きオプション
- `field?: type` - 型注釈付きオプション、デフォルトはnull
- オプションフィールドはダックタイピング時に欠落していれば追加される

### 型チェック

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // ここで型チェックが行われる

print(typeof(point));  // "Point"
print(typeof(p));      // "object"（元は無名のまま）
```

**型チェックが行われるタイミング：**
- 型付き変数への代入時
- すべての必須フィールドが存在するか検証
- フィールドの型が一致するか検証（暗黙の変換付き）
- オブジェクトの型名を設定

## Defineのメソッドシグネチャ

Defineブロックはメソッドシグネチャを指定でき、インターフェースのような契約を作成：

### 必須メソッド

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // 必須メソッドシグネチャ
}

// オブジェクトは必須メソッドを提供する必要がある
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### オプションメソッド

```hemlock
define Serializable {
    fn serialize(): string;       // 必須
    fn pretty?(): string;         // オプションメソッド（存在しなくてよい）
}
```

### `Self`型

`Self`は定義中の型を参照し、再帰的な型定義を可能に：

```hemlock
define Cloneable {
    fn clone(): Self;  // オブジェクトと同じ型を返す
}

define Comparable {
    fn compare(other: Self): i32;  // パラメータとして同じ型を取る
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### フィールドとメソッドの混合

```hemlock
define Entity {
    id: i32,
    name: string,
    fn validate(): bool;
    fn serialize(): string;
}

let user: Entity = {
    id: 1,
    name: "Alice",
    validate: fn() { return self.id > 0 && self.name != ""; },
    serialize: fn() { return '{"id":' + self.id + ',"name":"' + self.name + '"}'; }
};
```

## 複合型（交差型）

複合型は`&`を使用して、オブジェクトが複数の型定義を満たすことを要求：

### 基本的な複合型

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// 複合型：オブジェクトはすべての型を満たす必要がある
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### 複合型の関数パラメータ

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // 追加フィールドはOK
```

### 3つ以上の型

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### 複合型の型エイリアス

```hemlock
// 複合型の名前付きエイリアスを作成
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**複合型のダックタイピング：** 追加フィールドは常に許可されます - オブジェクトはすべての構成型が要求するフィールドを少なくとも持っていればよいです。

## JSONシリアライゼーション

### JSONへのシリアライズ

オブジェクトをJSON文字列に変換：

```hemlock
// obj.serialize() - オブジェクトをJSON文字列に変換
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// ネストされたオブジェクト
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### JSONからのデシリアライズ

JSON文字列をオブジェクトにパース：

```hemlock
// json.deserialize() - JSON文字列をオブジェクトにパース
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### 循環参照の検出

循環参照は検出されエラーになります：

```hemlock
let obj = { x: 10 };
obj.me = obj;  // 循環参照を作成

obj.serialize();  // エラー：serialize()が循環参照を検出
```

### サポートされる型

JSONシリアライゼーションがサポートする型：

- **数値**：i8-i32、u8-u32、f32、f64
- **真偽値**：true、false
- **文字列**：エスケープシーケンス付き
- **Null**：null値
- **オブジェクト**：ネストされたオブジェクト
- **配列**：ネストされた配列

**サポートされない：**
- 関数（無視される）
- ポインタ（エラー）
- バッファ（エラー）

### エラーハンドリング

シリアライゼーションとデシリアライゼーションはエラーをスローできます：

```hemlock
// 無効なJSONはエラーをスロー
try {
    let bad = "not valid json".deserialize();
} catch (e) {
    print("Parse error:", e);
}

// ポインタはシリアライズできない
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialize error:", e);
}
```

### ラウンドトリップの例

シリアライズとデシリアライズの完全な例：

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// 作成してシリアライズ
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// デシリアライズして復元
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## 組み込み関数

### `typeof(value)`

型名を文字列として返します：

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**戻り値：**
- 無名オブジェクト：`"object"`
- 型付きオブジェクト：カスタム型名（例：`"Person"`）

## 実装の詳細

### メモリモデル

- **ヒープ割り当て** - すべてのオブジェクトはヒープに割り当て
- **浅いコピー** - 代入は参照をコピー、オブジェクトではない
- **動的フィールド** - 名前/値ペアの動的配列として格納
- **参照カウント** - オブジェクトはスコープを抜けると自動的に解放

### 参照セマンティクス

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // 浅いコピー（同じ参照）

obj2.x = 20;
print(obj1.x);  // 20（両方が同じオブジェクトを参照）
```

### メソッドの格納

メソッドはフィールドに格納された関数です：

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// methodはobj.methodに格納された関数
print(typeof(obj.method));  // "function"
```

## よくあるパターン

### パターン：コンストラクタ関数

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

### パターン：オブジェクトビルダー

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // チェーンを有効に
        },

        setAge: fn(a) {
            self.age = a;
            return self;
        },

        build: fn() {
            return { name: self.name, age: self.age };
        }
    };
}

let person = PersonBuilder()
    .setName("Alice")
    .setAge(30)
    .build();
```

### パターン：状態オブジェクト

```hemlock
let state = {
    status: "idle",
    data: null,
    error: null,

    setState: fn(new_status) {
        self.status = new_status;
    },

    setData: fn(new_data) {
        self.data = new_data;
        self.status = "success";
    },

    setError: fn(err) {
        self.error = err;
        self.status = "error";
    }
};
```

### パターン：設定オブジェクト

```hemlock
let config = {
    defaults: {
        timeout: 30,
        retries: 3,
        debug: false
    },

    get: fn(key) {
        if (self.defaults[key] != null) {
            return self.defaults[key];
        }
        return null;
    },

    set: fn(key, value) {
        self.defaults[key] = value;
    }
};
```

## ベストプラクティス

1. **構造には`define`を使用** - 期待されるオブジェクトの形状を文書化
2. **ファクトリ関数を優先** - コンストラクタでオブジェクトを作成
3. **オブジェクトをシンプルに** - 深くネストしすぎない
4. **`self`の使用を文書化** - メソッドの動作を明確に
5. **代入時に検証** - ダックタイピングでエラーを早期にキャッチ
6. **循環参照を避ける** - シリアライゼーションエラーの原因
7. **オプションフィールドを使用** - 適切なデフォルトを提供

## よくある落とし穴

### 落とし穴：参照 vs 値

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // 浅いコピー

obj2.x = 20;
print(obj1.x);  // 20（驚き！両方が変更）

// 避けるには：新しいオブジェクトを作成
let obj3 = { x: obj1.x };  // ディープコピー（手動）
```

### 落とし穴：非メソッド呼び出しでの`self`

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// 動作：メソッドとして呼び出し
print(obj.method());  // 10

// エラー：関数として呼び出し
let f = obj.method;
print(f());  // エラー：selfが定義されていない
```

### 落とし穴：オブジェクト内の生のポインタ

```hemlock
// オブジェクトは自動解放されるが、内部の生のポインタはされない
fn create_objects() {
    let obj = { data: alloc(1000) };  // 生のptrは手動解放が必要
    // スコープを抜けるとobjは自動解放されるが、obj.dataはリーク！
}

// 解決策：スコープを抜ける前に生のポインタを解放
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... obj.dataを使用 ...
    free(obj.data);  // 生のポインタを明示的に解放
}  // obj自体は自動解放
```

### 落とし穴：型の混乱

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// エラー：必須フィールド'y'がない
let p: Point = obj;
```

## 例

### 例：ベクトル数学

```hemlock
fn createVector(x, y) {
    return {
        x: x,
        y: y,

        add: fn(other) {
            return createVector(
                self.x + other.x,
                self.y + other.y
            );
        },

        length: fn() {
            return sqrt(self.x * self.x + self.y * self.y);
        },

        toString: fn() {
            return "(" + typeof(self.x) + ", " + typeof(self.y) + ")";
        }
    };
}

let v1 = createVector(3, 4);
let v2 = createVector(1, 2);
let v3 = v1.add(v2);

print(v3.toString());  // "(4, 6)"
```

### 例：シンプルなデータベース

```hemlock
fn createDatabase() {
    let records = [];
    let next_id = 1;

    return {
        insert: fn(data) {
            let record = { id: next_id, data: data };
            records.push(record);
            next_id = next_id + 1;
            return record.id;
        },

        find: fn(id) {
            let i = 0;
            while (i < records.length) {
                if (records[i].id == id) {
                    return records[i];
                }
                i = i + 1;
            }
            return null;
        },

        count: fn() {
            return records.length;
        }
    };
}

let db = createDatabase();
let id = db.insert({ name: "Alice", age: 30 });
let record = db.find(id);
print(record.data.name);  // "Alice"
```

### 例：イベントエミッター

```hemlock
fn createEventEmitter() {
    let listeners = {};

    return {
        on: fn(event, handler) {
            if (listeners[event] == null) {
                listeners[event] = [];
            }
            listeners[event].push(handler);
        },

        emit: fn(event, data) {
            if (listeners[event] != null) {
                let i = 0;
                while (i < listeners[event].length) {
                    listeners[event][i](data);
                    i = i + 1;
                }
            }
        }
    };
}

let emitter = createEventEmitter();

emitter.on("message", fn(data) {
    print("Received: " + data);
});

emitter.emit("message", "Hello!");
```

## 制限事項

現在の制限事項：

- **ディープコピーなし** - ネストされたオブジェクトは手動でコピーする必要がある（スプレッドは浅い）
- **値渡しなし** - オブジェクトは常に参照で渡される
- **計算プロパティなし** - `{[key]: value}`構文がない
- **`self`は読み取り専用** - メソッド内で`self`を再代入できない
- **プロパティ削除なし** - 一度追加したフィールドを削除できない

**注意：** オブジェクトは参照カウントされ、スコープを抜けると自動的に解放されます。詳細は[メモリ管理](memory.md#internal-reference-counting)を参照してください。

## 関連トピック

- [関数](functions.md) - メソッドはオブジェクトに格納された関数
- [配列](arrays.md) - 配列もオブジェクトのような性質を持つ
- [型](types.md) - ダックタイピングと型定義
- [エラーハンドリング](error-handling.md) - エラーオブジェクトのスロー

## 参照

- **ダックタイピング**：ダックタイピングの詳細はCLAUDE.mdの「Objects」セクションを参照
- **JSON**：JSONシリアライゼーションの詳細はCLAUDE.mdを参照
- **メモリ**：オブジェクトの割り当ては[メモリ](memory.md)を参照
