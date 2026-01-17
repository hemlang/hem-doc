# 对象

Hemlock 实现了 JavaScript 风格的对象，具有堆分配、动态字段、方法和鸭子类型。对象是结合数据和行为的灵活数据结构。

## 概述

```hemlock
// 匿名对象
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// 带方法的对象
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## 对象字面量

### 基本语法

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**语法：**
- 花括号 `{}` 包围对象
- 键值对用逗号分隔
- 键是标识符（不需要引号）
- 值可以是任何类型

### 空对象

```hemlock
let obj = {};  // 空对象

// 稍后添加字段
obj.name = "Alice";
obj.age = 30;
```

### 嵌套对象

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

### 混合值类型

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

### 简写属性语法

当变量名与属性名匹配时，使用简写语法：

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// 简写：{ name } 等同于 { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**混合简写和常规属性：**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### 展开运算符

展开运算符（`...`）将一个对象的所有字段复制到另一个对象中：

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**使用展开覆盖值：**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark"（被覆盖）
print(custom.size);   // "medium"（来自 defaults）
print(custom.debug);  // false（来自 defaults）
```

**多个展开（后面的覆盖前面的）：**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// 后面的展开覆盖前面的
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**结合简写和展开：**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**配置覆盖模式：**
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

**注意：** 展开执行浅拷贝。嵌套对象共享引用：
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42（与 nested.inner 相同的引用）
```

## 字段访问

### 点语法

```hemlock
let person = { name: "Alice", age: 30 };

// 读取字段
let name = person.name;      // "Alice"
let age = person.age;        // 30

// 修改字段
person.age = 31;
print(person.age);           // 31
```

### 动态字段添加

在运行时添加新字段：

```hemlock
let person = { name: "Alice" };

// 添加新字段
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### 字段删除

**注意：** 目前不支持字段删除。改为设置为 `null`：

```hemlock
let obj = { x: 10, y: 20 };

// 无法删除字段（不支持）
// obj.x = undefined;  // Hemlock 中没有 'undefined'

// 变通方法：设置为 null
obj.x = null;
```

## 方法和 `self`

### 定义方法

方法是存储在对象字段中的函数：

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

### `self` 关键字

当函数作为方法调用时，`self` 自动绑定到对象：

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self 指向 counter
    }
};

counter.increment();  // self 绑定到 counter
print(counter.count);  // 1
```

**工作原理：**
- 通过检查函数表达式是否为属性访问来检测方法调用
- `self` 在调用时自动绑定到对象
- `self` 是只读的（无法重新赋值 `self` 本身）

### 方法调用检测

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// 作为方法调用 - self 被绑定
print(obj.method());  // 10

// 作为函数调用 - self 为 null（错误）
let f = obj.method;
print(f());  // 错误：self 未定义
```

### 带参数的方法

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

## 使用 `define` 进行类型定义

### 基本类型定义

使用 `define` 定义对象结构：

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// 创建对象并赋值给类型化变量
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // 鸭子类型验证结构

print(typeof(typed_p));  // "Person"
```

**`define` 的作用：**
- 声明具有必需字段的类型
- 启用鸭子类型验证
- 为 `typeof()` 设置对象的类型名称

### 鸭子类型

使用**结构兼容性**验证对象是否符合 `define`：

```hemlock
define Person {
    name: string,
    age: i32,
}

// 正确：具有所有必需字段
let p1: Person = { name: "Alice", age: 30 };

// 正确：允许额外字段
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// 错误：缺少必需字段 'age'
let p3: Person = { name: "Carol" };

// 错误：'age' 类型错误
let p4: Person = { name: "Dave", age: "thirty" };
```

**鸭子类型规则：**
- 所有必需字段必须存在
- 字段类型必须匹配
- 允许额外字段并保留
- 验证发生在赋值时

### 可选字段

字段可以是可选的，带有默认值：

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // 可选，带默认值
    nickname?: string,   // 可选，默认为 null
}

// 只有必需字段的对象
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true（应用默认值）
print(typed_p.nickname);  // null（无默认值）

// 可以覆盖可选字段
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false（被覆盖）
```

**可选字段语法：**
- `field?: default_value` - 可选，带默认值
- `field?: type` - 可选，带类型注解，默认为 null
- 如果缺少可选字段，在鸭子类型检查时添加

### 类型检查

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // 类型检查发生在这里

print(typeof(point));  // "Point"
print(typeof(p));      // "object"（原始对象仍是匿名的）
```

**类型检查发生的时机：**
- 赋值给类型化变量时
- 验证所有必需字段存在
- 验证字段类型匹配（带隐式转换）
- 设置对象的类型名称

## Define 中的方法签名

Define 块可以指定方法签名，创建类似接口的契约：

### 必需方法

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // 必需方法签名
}

// 对象必须提供必需方法
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### 可选方法

```hemlock
define Serializable {
    fn serialize(): string;       // 必需
    fn pretty?(): string;         // 可选方法（可能不存在）
}
```

### `Self` 类型

`Self` 指向正在定义的类型，支持递归类型定义：

```hemlock
define Cloneable {
    fn clone(): Self;  // 返回与对象相同的类型
}

define Comparable {
    fn compare(other: Self): i32;  // 接受相同类型作为参数
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### 混合字段和方法

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

## 复合类型（交叉类型）

复合类型使用 `&` 要求对象满足多个类型定义：

### 基本复合类型

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// 复合类型：对象必须满足所有类型
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### 带复合类型的函数参数

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // 允许额外字段
```

### 三个或更多类型

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### 复合类型的类型别名

```hemlock
// 为复合类型创建命名别名
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**复合类型的鸭子类型：** 始终允许额外字段 - 对象只需要至少具有所有组成类型要求的字段。

## JSON 序列化

### 序列化为 JSON

将对象转换为 JSON 字符串：

```hemlock
// obj.serialize() - 将对象转换为 JSON 字符串
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// 嵌套对象
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### 从 JSON 反序列化

将 JSON 字符串解析回对象：

```hemlock
// json.deserialize() - 将 JSON 字符串解析为对象
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### 循环引用检测

循环引用会被检测到并导致错误：

```hemlock
let obj = { x: 10 };
obj.me = obj;  // 创建循环引用

obj.serialize();  // 错误：serialize() 检测到循环引用
```

### 支持的类型

JSON 序列化支持：

- **数字**：i8-i32, u8-u32, f32, f64
- **布尔值**：true, false
- **字符串**：带转义序列
- **Null**：null 值
- **对象**：嵌套对象
- **数组**：嵌套数组

**不支持：**
- 函数（静默省略）
- 指针（错误）
- Buffer（错误）

### 错误处理

序列化和反序列化可能抛出错误：

```hemlock
// 无效 JSON 抛出错误
try {
    let bad = "not valid json".deserialize();
} catch (e) {
    print("Parse error:", e);
}

// 指针无法序列化
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialize error:", e);
}
```

### 往返示例

序列化和反序列化的完整示例：

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// 创建并序列化
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// 反序列化
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## 内置函数

### `typeof(value)`

返回类型名称作为字符串：

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**返回值：**
- 匿名对象：`"object"`
- 类型化对象：自定义类型名称（例如 `"Person"`）

## 实现细节

### 内存模型

- **堆分配** - 所有对象都在堆上分配
- **浅拷贝** - 赋值复制引用，而非对象
- **动态字段** - 存储为名称/值对的动态数组
- **引用计数** - 作用域退出时对象自动释放

### 引用语义

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // 浅拷贝（相同引用）

obj2.x = 20;
print(obj1.x);  // 20（两者指向相同对象）
```

### 方法存储

方法只是存储在字段中的函数：

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method 是存储在 obj.method 中的函数
print(typeof(obj.method));  // "function"
```

## 常见模式

### 模式：构造函数

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

### 模式：对象构建器

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // 支持链式调用
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

### 模式：状态对象

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

### 模式：配置对象

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

## 最佳实践

1. **使用 `define` 定义结构** - 记录预期的对象形状
2. **优先使用工厂函数** - 使用构造函数创建对象
3. **保持对象简单** - 不要嵌套太深
4. **记录 `self` 用法** - 明确方法行为
5. **在赋值时验证** - 使用鸭子类型尽早捕获错误
6. **避免循环引用** - 会导致序列化错误
7. **使用可选字段** - 提供合理的默认值

## 常见陷阱

### 陷阱：引用与值

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // 浅拷贝

obj2.x = 20;
print(obj1.x);  // 20（意外！两者都改变了）

// 避免方法：创建新对象
let obj3 = { x: obj1.x };  // 深拷贝（手动）
```

### 陷阱：非方法调用中的 `self`

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// 有效：作为方法调用
print(obj.method());  // 10

// 错误：作为函数调用
let f = obj.method;
print(f());  // 错误：self 未定义
```

### 陷阱：对象中的原始指针

```hemlock
// 对象会自动释放，但其中的原始指针不会
fn create_objects() {
    let obj = { data: alloc(1000) };  // 原始指针需要手动释放
    // 作用域退出时 obj 自动释放，但 obj.data 泄漏！
}

// 解决方案：在作用域退出前释放原始指针
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... 使用 obj.data ...
    free(obj.data);  // 显式释放原始指针
}  // obj 本身自动释放
```

### 陷阱：类型混淆

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// 错误：缺少必需字段 'y'
let p: Point = obj;
```

## 示例

### 示例：向量数学

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

### 示例：简单数据库

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

### 示例：事件发射器

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

## 限制

当前限制：

- **无深拷贝** - 必须手动复制嵌套对象（展开是浅拷贝）
- **无按值传递** - 对象始终按引用传递
- **无计算属性** - 不支持 `{[key]: value}` 语法
- **`self` 是只读的** - 无法在方法中重新赋值 `self`
- **无属性删除** - 一旦添加字段无法删除

**注意：** 对象使用引用计数，作用域退出时自动释放。详见 [内存管理](memory.md#internal-reference-counting)。

## 相关主题

- [函数](functions.md) - 方法是存储在对象中的函数
- [数组](arrays.md) - 数组也是类对象的
- [类型](types.md) - 鸭子类型和类型定义
- [错误处理](error-handling.md) - 抛出错误对象

## 另请参阅

- **鸭子类型**：参见 CLAUDE.md 中的 "Objects" 部分了解鸭子类型详情
- **JSON**：参见 CLAUDE.md 了解 JSON 序列化详情
- **内存**：参见 [内存](memory.md) 了解对象分配
