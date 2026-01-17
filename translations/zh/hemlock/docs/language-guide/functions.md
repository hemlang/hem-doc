# 函数

Hemlock 中的函数是**一等公民**，可以赋值给变量、作为参数传递以及从其他函数返回。本指南涵盖函数语法、闭包、递归和高级模式。

## 概述

```hemlock
// 命名函数语法
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// 匿名函数
let multiply = fn(x, y) {
    return x * y;
};

// 闭包
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## 函数声明

### 命名函数

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**组成部分：**
- `fn` - 函数关键字
- `greet` - 函数名
- `(name: string)` - 带可选类型的参数
- `: string` - 可选的返回类型
- `{ ... }` - 函数体

### 匿名函数

没有名称的函数，赋值给变量：

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**命名函数 vs 匿名函数：**
```hemlock
// 这两种方式等价：
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**注意：** 命名函数会被解语法糖为带匿名函数的变量赋值。

## 参数

### 基本参数

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### 类型注解

参数的可选类型注解：

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // 运行时类型检查会提升为 f64
```

**类型检查：**
- 如果有注解，参数类型在调用时检查
- 隐式类型转换遵循标准提升规则
- 类型不匹配会导致运行时错误

### 按值传递

所有参数都是**复制**的（按值传递）：

```hemlock
fn modify(x) {
    x = 100;  // 只修改本地副本
}

let a = 10;
modify(a);
print(a);  // 仍然是 10（未改变）
```

**注意：** 对象和数组按引用传递（引用被复制），因此可以修改它们的内容：

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // 修改原始数组
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99（已修改）
```

## 返回值

### Return 语句

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### 返回类型注解

返回值的可选类型注解：

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**类型检查：**
- 如果有注解，返回类型在函数返回时检查
- 类型转换遵循标准提升规则

### 隐式返回

没有返回类型注解的函数隐式返回 `null`：

```hemlock
fn print_message(msg) {
    print(msg);
    // 隐式返回 null
}

let result = print_message("hello");  // result 是 null
```

### 提前返回

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // 提前退出
        }
    }
    return -1;  // 未找到
}
```

### 无值返回

`return;` 不带值返回 `null`：

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // 返回 null
    }
    return value * 2;
}
```

## 一等函数

函数可以像其他值一样被赋值、传递和返回。

### 函数作为变量

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// 重新赋值
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### 函数作为参数

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### 函数作为返回值

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

## 闭包

函数捕获其定义环境（词法作用域）。

### 基本闭包

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

**工作原理：**
- 内部函数从外部作用域捕获 `count`
- `count` 在返回函数的多次调用间持久化
- 每次调用 `makeCounter()` 都会创建一个带有自己 `count` 的新闭包

### 带参数的闭包

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

### 多个闭包

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

### 词法作用域

函数可以通过词法作用域访问外部作用域变量：

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // 可以读取 global 和 outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

闭包通过引用捕获变量，允许读取和修改外部作用域变量（如上面的 `makeCounter` 示例所示）。

## 递归

函数可以调用自身。

### 基本递归

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### 互递归

函数可以互相调用：

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

### 递归数据处理

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

**注意：** 尚无尾调用优化 - 深度递归可能导致栈溢出。

## 高阶函数

接受或返回其他函数的函数。

### Map 模式

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

### Filter 模式

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

### Reduce 模式

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

### 函数组合

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

## 常见模式

### 模式：工厂函数

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

### 模式：回调函数

```hemlock
fn process_async(data, callback) {
    // ... 处理
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### 模式：部分应用

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

### 模式：记忆化

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
print(fast_fib(10));  // 使用缓存会快很多
```

## 函数语义

### 返回类型要求

带有返回类型注解的函数**必须**返回值：

```hemlock
fn get_value(): i32 {
    // 错误：缺少 return 语句
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### 类型检查

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // 提升为 f64，返回 f64
add("a", "b");     // 运行时错误：类型不匹配
```

### 作用域规则

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // 可以访问：inner_var、outer_var、global
    }

    // 可以访问：outer_var、global
    // 不能访问：inner_var
}

// 可以访问：global
// 不能访问：outer_var、inner_var
```

## 最佳实践

1. **使用类型注解** - 有助于发现错误并记录意图
2. **保持函数小巧** - 每个函数应只做一件事
3. **优先使用纯函数** - 尽可能避免副作用
4. **命名要清晰** - 使用描述性的动词名称
5. **提前返回** - 使用守卫子句减少嵌套
6. **记录复杂闭包** - 明确捕获的变量
7. **避免深度递归** - 尚无尾调用优化

## 常见陷阱

### 陷阱：递归深度

```hemlock
// 深度递归可能导致栈溢出
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // 可能因栈溢出而崩溃
```

### 陷阱：修改捕获的变量

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // 可以读取和修改捕获的变量
        return count;
    };
}
```

**注意：** 这是可行的，但要注意所有闭包共享同一个捕获的环境。

## 示例

### 示例：函数管道

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

### 示例：事件处理器

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

### 示例：自定义比较器排序

```hemlock
fn sort(arr, compare) {
    // 使用自定义比较器的冒泡排序
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

## 可选参数（默认参数）

函数可以使用 `?:` 语法定义带默认值的可选参数：

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

**规则：**
- 可选参数必须在必需参数之后
- 默认值可以是任何表达式
- 省略的参数使用默认值

## 可变参数函数（剩余参数）

函数可以使用剩余参数（`...`）接受可变数量的参数：

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

**规则：**
- 剩余参数必须是最后一个参数
- 剩余参数将所有剩余参数收集到一个数组中
- 可以与普通参数和可选参数组合使用

## 函数类型注解

函数类型允许你为函数参数和返回值指定精确的签名：

### 基本函数类型

```hemlock
// 函数类型语法：fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### 高阶函数类型

```hemlock
// 返回函数的函数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### 异步函数类型

```hemlock
// 异步函数类型
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### 函数类型别名

```hemlock
// 创建命名函数类型以提高清晰度
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Const 参数

`const` 修饰符防止在函数内修改参数：

### 基本 Const 参数

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // 错误：不能修改 const 参数
    for (item in items) {
        print(item);   // OK：允许读取
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### 深度不可变性

Const 参数强制深度不可变性 - 不能通过任何路径进行修改：

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK：允许读取
    // person.name = "Bob";   // 错误：不能修改
    // person.address.city = "NYC";  // 错误：深度 const
}
```

### Const 阻止的操作

| 类型 | 被 Const 阻止 | 允许的 |
|------|--------------|-------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | 字段赋值 | 字段读取 |
| buffer | 索引赋值 | 索引读取 |
| string | 索引赋值 | 所有方法（返回新字符串） |

## 命名参数

函数可以使用命名参数调用以提高清晰度和灵活性：

### 基本命名参数

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// 位置参数（传统方式）
create_user("Alice", 25, false);

// 命名参数 - 可以任意顺序
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### 混合位置参数和命名参数

```hemlock
// 通过命名来跳过可选参数
create_user("David", active: false);  // 使用默认 age=18

// 命名参数必须在位置参数之后
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // 错误：位置参数在命名参数之后
```

### 命名参数规则

- 使用 `name: value` 语法表示命名参数
- 命名参数可以在位置参数之后以任意顺序出现
- 位置参数不能跟在命名参数之后
- 与默认/可选参数配合使用
- 未知的参数名会导致运行时错误

## 限制

需要注意的当前限制：

- **无按引用传递** - `ref` 关键字已解析但未实现
- **无函数重载** - 每个名称只能有一个函数
- **无尾调用优化** - 深度递归受栈大小限制

## 相关主题

- [Control Flow](control-flow.md) - 函数与控制结构的配合使用
- [Objects](objects.md) - 方法是存储在对象中的函数
- [Error Handling](error-handling.md) - 函数和异常处理
- [Types](types.md) - 类型注解和转换

## 另请参阅

- **闭包**：参见 CLAUDE.md 中的"Functions"部分了解闭包语义
- **一等公民**：函数是与其他值一样的值
- **词法作用域**：函数捕获其定义环境
