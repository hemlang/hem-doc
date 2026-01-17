# シグネチャ構文設計

> Hemlockの型システムを関数型、nullable修飾子、型エイリアス、constパラメータ、メソッドシグネチャで拡張する。

**ステータス:** 実装済み (v1.7.0)
**バージョン:** 1.0
**著者:** Claude

---

## 概要

このドキュメントでは、Hemlockの既存インフラストラクチャに基づいて構築する5つの相互接続された型システム拡張を提案します:

1. **関数型注釈** - ファーストクラスの関数型
2. **Nullable型修飾子** - 明示的なnull処理（既存の`nullable`フラグを拡張）
3. **型エイリアス** - 名前付き型の省略形
4. **Constパラメータ** - 不変性契約
5. **Defineでのメソッドシグネチャ** - インターフェースのような動作

これらの機能は以下の哲学を共有します: **暗黙より明示、オプションだが使用時は強制**。

---

## 1. 関数型注釈

### 動機

現在、関数のシグネチャを型として表現する方法がありません:

```hemlock
// 現在: callbackには型情報がない
fn map(arr: array, callback) { ... }

// 提案: 明示的な関数型
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### 構文

```hemlock
// 基本的な関数型
fn(i32, i32): i32

// パラメータ名付き（ドキュメント用のみ、強制されない）
fn(a: i32, b: i32): i32

// 戻り値なし (void)
fn(string): void
fn(string)              // 省略形: `: void`を省略

// Nullable戻り値
fn(i32): string?

// オプションパラメータ
fn(name: string, age?: i32): void

// 残余パラメータ
fn(...args: array): i32

// パラメータなし
fn(): bool

// 高階: 関数を返す関数
fn(i32): fn(i32): i32

// 非同期関数型
async fn(i32): i32
```

### 使用例

```hemlock
// 関数型を持つ変数
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// 関数パラメータ
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// 戻り値型が関数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// 関数の配列
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// オブジェクトフィールド
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### AST変更

```c
// TypeKind列挙型 (include/ast.h)
typedef enum {
    // ... 既存の型 ...
    TYPE_FUNCTION,      // 新規: 関数型
} TypeKind;

// Type構造体 (include/ast.h)
struct Type {
    TypeKind kind;
    // ... 既存のフィールド ...

    // TYPE_FUNCTION用:
    struct Type **param_types;      // パラメータ型
    char **param_names;             // オプションのパラメータ名（ドキュメント用）
    int *param_optional;            // どのパラメータがオプションか
    int num_params;
    char *rest_param_name;          // 残余パラメータ名またはNULL
    struct Type *rest_param_type;   // 残余パラメータ型
    struct Type *return_type;       // 戻り値型（NULL = void）
    int is_async;                   // 非同期関数型
};
```

### パース

関数型は`fn`（または`async fn`）の後にパラメータリストで始まります:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**曖昧さの解消:** 型をパース中に`fn`に遭遇した場合:
- `(`が続く場合、関数型
- そうでなければ、構文エラー（単独の`fn`は有効な型ではない）

### 型互換性

```hemlock
// 関数型には厳密な一致が必要
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// パラメータの反変性（より広い型を受け入れるのはOK）
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// 戻り値の共変性（より狭い型を返すのはOK）
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// アリティは一致する必要がある
let bad: fn(i32): i32 = fn(a, b) { return a; };       // エラー: アリティ不一致

// オプションパラメータは必須と互換
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Nullable型修飾子

### 動機

`?`サフィックスにより、シグネチャでのnull受け入れを明示的にします:

```hemlock
// 現在: nullが有効かどうか不明
fn find(arr: array, val: any): i32 { ... }

// 提案: 明示的なnullable戻り値
fn find(arr: array, val: any): i32? { ... }
```

### 構文

```hemlock
// ?サフィックス付きNullable型
string?           // stringまたはnull
i32?              // i32またはnull
User?             // Userまたはnull
array<i32>?       // arrayまたはnull
fn(i32): i32?     // i32またはnullを返す関数

// 関数型との組み合わせ
fn(string?): i32          // stringまたはnullを受け入れる
fn(string): i32?          // i32またはnullを返す
fn(string?): i32?         // 両方nullable

// defineでの使用
define Result {
    value: any?;
    error: string?;
}
```

### 実装上の注意

**既に存在:** `Type.nullable`フラグは既にASTにあります。この機能は主に以下が必要:
1. 任意の型での`?`サフィックスのパーサーサポート（検証/拡張）
2. 関数型との適切な組み合わせ
3. ランタイム強制

### 型互換性

```hemlock
// 非nullableはnullableに代入可能
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// nullableは非nullableに代入不可
let z: i32 = x;             // エラー: xはnullかもしれない

// null合体でアンラップ
let z: i32 = x ?? 0;        // OK: ??がデフォルトを提供

// セーフナビゲーションはnullableを返す
let name: string? = user?.name;
```

---

## 3. 型エイリアス

### 動機

複雑な型は名前付きの省略形から恩恵を受けます:

```hemlock
// 現在: 繰り返しの複合型
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// 提案: 名前付きエイリアス
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### 構文

```hemlock
// 基本エイリアス
type Integer = i32;
type Text = string;

// 複合型エイリアス
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// 関数型エイリアス
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Nullableエイリアス
type OptionalString = string?;

// ジェネリックエイリアス（ジェネリック型エイリアスをサポートする場合）
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// 配列型エイリアス
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### スコープと可視性

```hemlock
// デフォルトでモジュールスコープ
type Callback = fn(Event): void;

// エクスポート可能
export type Handler = fn(Request): Response;

// 別のファイルで
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### AST変更

```c
// 新しい文の種類
typedef enum {
    // ... 既存の文 ...
    STMT_TYPE_ALIAS,    // 新規
} StmtKind;

// Stmtユニオン内
struct {
    char *name;                 // エイリアス名
    char **type_params;         // ジェネリックパラメータ: <T, U>
    int num_type_params;
    Type *aliased_type;         // 実際の型
} type_alias;
```

### パース

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**注:** `type`は新しいキーワードです。既存の識別子との競合をチェックしてください。

### 解決

型エイリアスは以下のタイミングで解決されます:
- **パース時:** エイリアスが型環境に記録される
- **チェック時:** エイリアスが基礎となる型に展開される
- **ランタイム:** エイリアスは透過的（基礎型と同じ）

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32"（"MyInt"ではない）
```

---

## 4. Constパラメータ

### 動機

関数シグネチャで不変性の意図を示します:

```hemlock
// 現在: 配列が変更されるかどうか不明
fn print_all(items: array) { ... }

// 提案: 明示的な不変性契約
fn print_all(const items: array) { ... }
```

### 構文

```hemlock
// Constパラメータ
fn process(const data: buffer) {
    // data[0] = 0;        // エラー: constを変更できない
    let x = data[0];       // OK: 読み取りは許可
    return x;
}

// 複数のconstパラメータ
fn compare(const a: array, const b: array): bool { ... }

// constとmutableの混在
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK: targetは変更可能
    }
}

// 型推論付きconst
fn log(const msg) {
    print(msg);
}

// 関数型でのconst
type Reader = fn(const buffer): i32;
```

### Constが防ぐもの

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // エラー: 変更メソッド
    arr.pop();           // エラー: 変更メソッド
    arr[0] = 5;          // エラー: インデックス代入
    arr.clear();         // エラー: 変更メソッド
}

fn ok(const arr: array) {
    let x = arr[0];      // OK: 読み取り
    let len = len(arr);  // OK: 長さチェック
    let copy = arr.slice(0, 10);  // OK: 新しい配列を作成
    for (item in arr) {  // OK: イテレーション
        print(item);
    }
}
```

### 変更 vs 非変更メソッド

| 型 | 変更（constでブロック） | 非変更（許可） |
|------|----------------------------|------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (in-place) | slice, concat, map, filter, find, contains, first, last, join |
| string | インデックス代入 (`s[0] = 'x'`) | すべてのメソッド（新しい文字列を返す） |
| buffer | インデックス代入, memset, memcpy (to) | インデックス読み取り, slice |
| object | フィールド代入 | フィールド読み取り |

### AST変更

```c
// 関数式内 (include/ast.h)
struct {
    // ... 既存のフィールド ...
    int *param_is_const;    // 新規: constなら1、そうでなければ0
} function;

// 関数型用のType構造体内
struct Type {
    // ... 既存のフィールド ...
    int *param_is_const;    // TYPE_FUNCTION用
};
```

### 強制

**インタプリタ:**
- 変数バインディングでconst性を追跡
- 変更操作前にチェック
- const違反でランタイムエラー

**コンパイラ:**
- 有益な場合はconstで修飾されたC変数を生成
- const違反の静的解析
- コンパイル時の警告/エラー

---

## 5. Defineでのメソッドシグネチャ

### 動機

`define`ブロックでデータフィールドだけでなく、期待されるメソッドを指定できるようにします:

```hemlock
// 現在: データフィールドのみ
define User {
    name: string;
    age: i32;
}

// 提案: メソッドシグネチャ
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // 静的メソッド
}
```

### 構文

```hemlock
// メソッドシグネチャ（本体なし）
define Hashable {
    fn hash(): i32;
}

// 複数のメソッド
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// フィールドとメソッドの混在
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Self型の使用
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// オプションメソッド
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // オプションメソッド（存在しない可能性あり）
}

// デフォルト実装付きメソッド
define Ordered {
    fn compare(other: Self): i32;  // 必須

    // デフォルト実装（オーバーライドされなければ継承）
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### `Self`型

`Self`はインターフェースを実装する具象型を参照します:

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// 使用時:
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### 構造的型付け（ダックタイピング）

メソッドシグネチャはフィールドと同じダックタイピングを使用します:

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// to_string()メソッドを持つ任意のオブジェクトはStringifiableを満たす
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// メソッド付き複合型
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### AST変更

```c
// Stmtユニオン内のdefine_objectを拡張
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // フィールド（既存）
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // メソッド（新規）
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // オプションメソッド (fn name?(): type)
    Expr **method_defaults;     // デフォルト実装（シグネチャのみの場合NULL）
    int num_methods;
} define_object;
```

### 型チェック

`value: InterfaceType`をチェックする際:
1. すべての必須フィールドが互換型で存在するかチェック
2. すべての必須メソッドが互換シグネチャで存在するかチェック
3. オプションフィールド/メソッドは不在でも可

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// 有効: compareメソッドを持つ
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// 無効: compareがない
let invalid: Sortable = { value: 10 };  // エラー: メソッド 'compare' がない

// 無効: 間違ったシグネチャ
let wrong: Sortable = {
    compare: fn() { return 0; }  // エラー: (Self): i32が期待される
};
```

---

## 相互作用の例

### すべての機能を組み合わせる

```hemlock
// 複雑な関数型の型エイリアス
type EventCallback = fn(event: Event, context: Context?): bool;

// 複合インターフェースの型エイリアス
type Entity = HasId & HasName & Serializable;

// メソッドシグネチャ付きdefine
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// すべてを一緒に使用
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### 明示的な型を持つコールバック

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Nullable関数型

```hemlock
// オプションのコールバック
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// 関数型からのnullable戻り値
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## 実装ロードマップ

### フェーズ1: コアインフラストラクチャ
1. TypeKind列挙型に`TYPE_FUNCTION`を追加
2. Type構造体に関数型フィールドを拡張
3. コンパイラ型チェッカーに`CHECKED_FUNCTION`を追加
4. `Self`型サポートを追加 (TYPE_SELF)

### フェーズ2: パース
1. パーサーに`parse_function_type()`を実装
2. 型位置で`fn(...)`を処理
3. `type`キーワードと`STMT_TYPE_ALIAS`パースを追加
4. `const`パラメータ修飾子パースを追加
5. メソッドシグネチャ用にdefineパースを拡張

### フェーズ3: 型チェック
1. 関数型互換性ルール
2. 型エイリアス解決と展開
3. Constパラメータ変更チェック
4. define型でのメソッドシグネチャ検証
5. Self型解決

### フェーズ4: ランタイム
1. 呼び出しサイトでの関数型検証
2. Const違反検出
3. 型エイリアス透過性

### フェーズ5: パリティテスト
1. 関数型注釈テスト
2. Nullable組み合わせテスト
3. 型エイリアステスト
4. Constパラメータテスト
5. メソッドシグネチャテスト

---

## 設計上の決定

### 1. ジェネリック型エイリアス: **YES**

型エイリアスはジェネリックパラメータをサポート:

```hemlock
// ジェネリック型エイリアス
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// 使用
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Const伝播: **DEEP**

Constパラメータは完全に不変 - どのパスを通しても変更不可:

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // エラー: const配列を変更できない
    arr[0] = {};         // エラー: const配列を変更できない
    arr[0].x = 5;        // エラー: constを通して変更できない（DEEP）

    let x = arr[0].x;    // OK: 読み取りは問題ない
    let copy = arr[0];   // OK: コピーを作成
    copy.x = 5;          // OK: コピーはconstではない
}

fn nested(const obj: object) {
    obj.user.name = "x"; // エラー: ディープconstはネストされた変更を防ぐ
    obj.items[0] = 1;    // エラー: ディープconstはネストされた変更を防ぐ
}
```

**根拠:** ディープconstはより強い保証を提供し、データの整合性を確保するのにより有用です。
ネストされたデータを変更する必要がある場合は、まずコピーを作成してください。

### 3. スタンドアロン型エイリアスでのSelf: **NO**

`Self`は明確な意味を持つ`define`ブロック内でのみ有効:

```hemlock
// 有効: Selfは定義された型を参照
define Comparable {
    fn compare(other: Self): i32;
}

// 無効: ここではSelfに意味がない
type Cloner = fn(Self): Self;  // エラー: defineコンテキスト外のSelf

// 代わりに、ジェネリックを使用:
type Cloner<T> = fn(T): T;
```

### 4. メソッドのデフォルト実装: **YES (シンプルなものに限る)**

シンプル/ユーティリティメソッドにデフォルト実装を許可:

```hemlock
define Comparable {
    // 必須: 実装が必要
    fn compare(other: Self): i32;

    // デフォルト実装（シンプルな便利メソッド）
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // デフォルト: 必須メソッドに委譲
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// オブジェクトは必須メソッドのみ実装すればよい
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_thanはデフォルトから継承
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**デフォルトのガイドライン:**
- シンプルに保つ（1-3行）
- 必須メソッドに委譲すべき
- 複雑なロジックや副作用なし
- プリミティブと単純な合成のみ

### 5. 変性: **推論（明示的注釈なし）**

変性は型パラメータの使用方法から推論されます:

```hemlock
// 変性は位置に基づいて自動
type Producer<T> = fn(): T;           // 戻り値のT = 共変
type Consumer<T> = fn(T): void;       // パラメータのT = 反変
type Transformer<T> = fn(T): T;       // 両方のT = 不変

// 例: Dog <: Animal（DogはAnimalのサブタイプ）
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK: 共変

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK: 反変
```

**なぜ推論？**
- ボイラープレートが少ない（`<out T>` / `<in T>`はノイズを加える）
- 「暗黙より明示」に従う - 位置は明示的
- ほとんどの言語が関数型の変性を処理する方法に一致
- 変性ルールに違反した場合のエラーは明確

---

## 付録: 文法変更

```ebnf
(* 型 *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* 文 *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" はオプションメソッドを示し、block はデフォルト実装を提供 *)

(* パラメータ *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
