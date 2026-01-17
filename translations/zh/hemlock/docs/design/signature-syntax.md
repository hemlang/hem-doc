# 签名语法设计

> 用函数类型、可空修饰符、类型别名、const 参数和方法签名扩展 Hemlock 的类型系统。

**状态：**已实现（v1.7.0）
**版本：**1.0
**作者：**Claude

---

## 概述

本文档提出了五个相互关联的类型系统扩展，它们建立在 Hemlock 现有基础设施之上：

1. **函数类型注解** - 一等函数类型
2. **可空类型修饰符** - 显式的 null 处理（扩展现有的 `nullable` 标志）
3. **类型别名** - 命名的类型缩写
4. **Const 参数** - 不可变性契约
5. **Define 中的方法签名** - 类接口行为

这些特性共享相同的理念：**显式优于隐式，可选但使用时强制执行**。

---

## 1. 函数类型注解

### 动机

目前，没有办法将函数的签名表达为类型：

```hemlock
// 当前：callback 没有类型信息
fn map(arr: array, callback) { ... }

// 提议：显式函数类型
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### 语法

```hemlock
// 基本函数类型
fn(i32, i32): i32

// 带参数名（仅用于文档，不强制执行）
fn(a: i32, b: i32): i32

// 无返回值（void）
fn(string): void
fn(string)              // 简写：省略 `: void`

// 可空返回
fn(i32): string?

// 可选参数
fn(name: string, age?: i32): void

// Rest 参数
fn(...args: array): i32

// 无参数
fn(): bool

// 高阶：返回函数的函数
fn(i32): fn(i32): i32

// 异步函数类型
async fn(i32): i32
```

### 使用示例

```hemlock
// 带函数类型的变量
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// 函数参数
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// 返回类型是函数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// 函数数组
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// 对象字段
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### AST 更改

```c
// 在 TypeKind 枚举中（include/ast.h）
typedef enum {
    // ... 现有类型 ...
    TYPE_FUNCTION,      // 新增：函数类型
} TypeKind;

// 在 Type 结构中（include/ast.h）
struct Type {
    TypeKind kind;
    // ... 现有字段 ...

    // 用于 TYPE_FUNCTION：
    struct Type **param_types;      // 参数类型
    char **param_names;             // 可选参数名（文档）
    int *param_optional;            // 哪些参数是可选的
    int num_params;
    char *rest_param_name;          // Rest 参数名或 NULL
    struct Type *rest_param_type;   // Rest 参数类型
    struct Type *return_type;       // 返回类型（NULL = void）
    int is_async;                   // async fn 类型
};
```

### 解析

函数类型以 `fn`（或 `async fn`）开始，后跟参数列表：

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**消歧义：**解析类型时遇到 `fn`：
- 如果后跟 `(`，则是函数类型
- 否则，语法错误（裸 `fn` 不是有效类型）

### 类型兼容性

```hemlock
// 函数类型需要精确匹配
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // 正确

// 参数逆变（接受更宽类型是可以的）
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // 正确：i32 <: any

// 返回协变（返回更窄类型是可以的）
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // 正确：i32 <: any

// 参数数量必须匹配
let bad: fn(i32): i32 = fn(a, b) { return a; };       // 错误：参数数量不匹配

// 可选参数与必需参数兼容
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // 正确
```

---

## 2. 可空类型修饰符

### 动机

`?` 后缀使签名中的 null 接受变得显式：

```hemlock
// 当前：不清楚 null 是否有效
fn find(arr: array, val: any): i32 { ... }

// 提议：显式可空返回
fn find(arr: array, val: any): i32? { ... }
```

### 语法

```hemlock
// 带 ? 后缀的可空类型
string?           // string 或 null
i32?              // i32 或 null
User?             // User 或 null
array<i32>?       // array 或 null
fn(i32): i32?     // 返回 i32 或 null 的函数

// 与函数类型组合
fn(string?): i32          // 接受 string 或 null
fn(string): i32?          // 返回 i32 或 null
fn(string?): i32?         // 两者都可空

// 在 define 中
define Result {
    value: any?;
    error: string?;
}
```

### 实现说明

**已存在：**`Type.nullable` 标志已在 AST 中。此特性主要需要：
1. 对任何类型的 `?` 后缀的解析器支持（验证/扩展）
2. 与函数类型的正确组合
3. 运行时强制执行

### 类型兼容性

```hemlock
// 非空可赋值给可空
let x: i32? = 42;           // 正确
let y: i32? = null;         // 正确

// 可空不能赋值给非空
let z: i32 = x;             // 错误：x 可能是 null

// 空值合并以解包
let z: i32 = x ?? 0;        // 正确：?? 提供默认值

// 可选链返回可空
let name: string? = user?.name;
```

---

## 3. 类型别名

### 动机

复杂类型受益于命名缩写：

```hemlock
// 当前：重复的复合类型
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// 提议：命名别名
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### 语法

```hemlock
// 基本别名
type Integer = i32;
type Text = string;

// 复合类型别名
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// 函数类型别名
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// 可空别名
type OptionalString = string?;

// 泛型别名（如果我们支持泛型类型别名）
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// 数组类型别名
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### 作用域和可见性

```hemlock
// 默认模块作用域
type Callback = fn(Event): void;

// 可导出
export type Handler = fn(Request): Response;

// 在另一个文件中
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### AST 更改

```c
// 新语句类型
typedef enum {
    // ... 现有语句 ...
    STMT_TYPE_ALIAS,    // 新增
} StmtKind;

// 在 Stmt union 中
struct {
    char *name;                 // 别名名称
    char **type_params;         // 泛型参数：<T, U>
    int num_type_params;
    Type *aliased_type;         // 实际类型
} type_alias;
```

### 解析

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**注意：**`type` 是一个新关键字。检查与现有标识符的冲突。

### 解析

类型别名在以下时机解析：
- **解析时：**别名记录在类型环境中
- **检查时：**别名展开为底层类型
- **运行时：**别名是透明的（与底层类型相同）

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32"（不是 "MyInt"）
```

---

## 4. Const 参数

### 动机

在函数签名中表示不可变性意图：

```hemlock
// 当前：不清楚 array 是否会被修改
fn print_all(items: array) { ... }

// 提议：显式不可变性契约
fn print_all(const items: array) { ... }
```

### 语法

```hemlock
// Const 参数
fn process(const data: buffer) {
    // data[0] = 0;        // 错误：不能修改 const
    let x = data[0];       // 正确：允许读取
    return x;
}

// 多个 const 参数
fn compare(const a: array, const b: array): bool { ... }

// 混合 const 和可变
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // 正确：target 是可变的
    }
}

// Const 与类型推断
fn log(const msg) {
    print(msg);
}

// 函数类型中的 const
type Reader = fn(const buffer): i32;
```

### Const 阻止的操作

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // 错误：修改方法
    arr.pop();           // 错误：修改方法
    arr[0] = 5;          // 错误：索引赋值
    arr.clear();         // 错误：修改方法
}

fn ok(const arr: array) {
    let x = arr[0];      // 正确：读取
    let len = len(arr);  // 正确：长度检查
    let copy = arr.slice(0, 10);  // 正确：创建新数组
    for (item in arr) {  // 正确：迭代
        print(item);
    }
}
```

### 修改方法与非修改方法

| 类型 | 修改（被 const 阻止） | 非修改（允许） |
|------|----------------------------|------------------------|
| array | push、pop、shift、unshift、insert、remove、clear、reverse（原地） | slice、concat、map、filter、find、contains、first、last、join |
| string | 索引赋值（`s[0] = 'x'`） | 所有方法（返回新字符串） |
| buffer | 索引赋值、memset、memcpy（目标） | 索引读取、slice |
| object | 字段赋值 | 字段读取 |

### AST 更改

```c
// 在函数表达式中（include/ast.h）
struct {
    // ... 现有字段 ...
    int *param_is_const;    // 新增：1 表示 const，0 表示否
} function;

// 在函数类型的 Type 结构中
struct Type {
    // ... 现有字段 ...
    int *param_is_const;    // 用于 TYPE_FUNCTION
};
```

### 强制执行

**解释器：**
- 在变量绑定中跟踪 const 性
- 在修改操作前检查
- const 违规时运行时错误

**编译器：**
- 在有益时生成 const 限定的 C 变量
- const 违规的静态分析
- 编译时警告/错误

---

## 5. Define 中的方法签名

### 动机

允许 `define` 块指定预期的方法，不仅是数据字段：

```hemlock
// 当前：仅数据字段
define User {
    name: string;
    age: i32;
}

// 提议：方法签名
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // 静态方法
}
```

### 语法

```hemlock
// 方法签名（无方法体）
define Hashable {
    fn hash(): i32;
}

// 多个方法
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// 混合字段和方法
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// 使用 Self 类型
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// 可选方法
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // 可选方法（可能不存在）
}

// 带默认实现的方法
define Ordered {
    fn compare(other: Self): i32;  // 必需

    // 默认实现（如果未覆盖则继承）
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

### `Self` 类型

`Self` 指的是实现接口的具体类型：

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// 使用时：
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### 结构类型（鸭子类型）

方法签名使用与字段相同的鸭子类型：

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// 任何有 to_string() 方法的对象都满足 Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// 带方法的复合类型
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### AST 更改

```c
// 扩展 Stmt union 中的 define_object
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // 字段（现有）
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // 方法（新增）
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // 可选方法（fn name?(): type）
    Expr **method_defaults;     // 默认实现（如果仅签名则为 NULL）
    int num_methods;
} define_object;
```

### 类型检查

检查 `value: InterfaceType` 时：
1. 检查所有必需字段存在且类型兼容
2. 检查所有必需方法存在且签名兼容
3. 可选字段/方法可以不存在

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// 有效：有 compare 方法
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// 无效：缺少 compare
let invalid: Sortable = { value: 10 };  // 错误：缺少方法 'compare'

// 无效：签名错误
let wrong: Sortable = {
    compare: fn() { return 0; }  // 错误：期望 (Self): i32
};
```

---

## 交互示例

### 组合所有特性

```hemlock
// 复杂函数类型的类型别名
type EventCallback = fn(event: Event, context: Context?): bool;

// 复合接口的类型别名
type Entity = HasId & HasName & Serializable;

// 带方法签名的 Define
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// 将所有组合在一起使用
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

### 显式类型的回调

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

### 可空函数类型

```hemlock
// 可选回调
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// 函数类型的可空返回
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

## 实现路线图

### 阶段 1：核心基础设施
1. 将 `TYPE_FUNCTION` 添加到 TypeKind 枚举
2. 用函数类型字段扩展 Type 结构
3. 将 `CHECKED_FUNCTION` 添加到编译器类型检查器
4. 添加 `Self` 类型支持（TYPE_SELF）

### 阶段 2：解析
1. 在解析器中实现 `parse_function_type()`
2. 在类型位置处理 `fn(...)`
3. 添加 `type` 关键字和 `STMT_TYPE_ALIAS` 解析
4. 添加 `const` 参数修饰符解析
5. 扩展 define 解析以支持方法签名

### 阶段 3：类型检查
1. 函数类型兼容性规则
2. 类型别名解析和展开
3. Const 参数修改检查
4. define 类型中的方法签名验证
5. Self 类型解析

### 阶段 4：运行时
1. 调用点的函数类型验证
2. Const 违规检测
3. 类型别名透明性

### 阶段 5：一致性测试
1. 函数类型注解测试
2. 可空组合测试
3. 类型别名测试
4. Const 参数测试
5. 方法签名测试

---

## 设计决策

### 1. 泛型类型别名：**是**

类型别名支持泛型参数：

```hemlock
// 泛型类型别名
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// 使用
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Const 传播：**深层**

Const 参数是完全不可变的 - 通过任何路径都不能修改：

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // 错误：不能修改 const 数组
    arr[0] = {};         // 错误：不能修改 const 数组
    arr[0].x = 5;        // 错误：不能通过 const 修改（深层）

    let x = arr[0].x;    // 正确：读取没问题
    let copy = arr[0];   // 正确：创建副本
    copy.x = 5;          // 正确：副本不是 const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // 错误：深层 const 阻止嵌套修改
    obj.items[0] = 1;    // 错误：深层 const 阻止嵌套修改
}
```

**理由：**深层 const 提供更强的保证，对于确保数据完整性更有用。如果需要修改嵌套数据，先复制。

### 3. 独立类型别名中的 Self：**否**

`Self` 仅在 `define` 块内有效，在那里它有明确的含义：

```hemlock
// 有效：Self 指的是定义的类型
define Comparable {
    fn compare(other: Self): i32;
}

// 无效：Self 在这里没有意义
type Cloner = fn(Self): Self;  // 错误：Self 在 define 上下文之外

// 改用泛型：
type Cloner<T> = fn(T): T;
```

### 4. 方法默认实现：**是（仅简单的）**

允许简单/实用方法的默认实现：

```hemlock
define Comparable {
    // 必需：必须实现
    fn compare(other: Self): i32;

    // 默认实现（简单便利方法）
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

    // 默认：委托给必需方法
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// 对象只需实现必需方法
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals、less_than、greater_than 从默认继承
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**默认实现指南：**
- 保持简单（1-3 行）
- 应该委托给必需方法
- 无复杂逻辑或副作用
- 仅限原始类型和直接组合

### 5. 型变：**推断（无显式注解）**

型变根据类型参数的使用方式推断：

```hemlock
// 型变根据位置自动确定
type Producer<T> = fn(): T;           // T 在返回位置 = 协变
type Consumer<T> = fn(T): void;       // T 在参数位置 = 逆变
type Transformer<T> = fn(T): T;       // T 在两个位置 = 不变

// 示例：Dog <: Animal（Dog 是 Animal 的子类型）
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // 正确：协变

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // 正确：逆变
```

**为什么推断？**
- 更少的样板代码（`<out T>` / `<in T>` 增加噪音）
- 遵循"显式优于隐式" - 位置本身就是显式的
- 与大多数语言处理函数类型型变的方式一致
- 违反型变规则时错误清晰

---

## 附录：语法更改

```ebnf
(* 类型 *)
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

(* 语句 *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" 标记可选方法，block 提供默认实现 *)

(* 参数 *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
