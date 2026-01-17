# 控制流

Hemlock 提供熟悉的 C 风格控制流，要求强制使用花括号和显式语法。本指南涵盖条件语句、循环、switch 语句和运算符。

## 概述

可用的控制流特性：

- `if`/`else`/`else if` - 条件分支
- `while` 循环 - 基于条件的迭代
- `for` 循环 - C 风格和 for-in 迭代
- `loop` - 无限循环（比 `while (true)` 更清晰）
- `switch` 语句 - 多路分支
- `break`/`continue` - 循环控制
- 循环标签 - 针对嵌套循环的定向 break/continue
- `defer` - 延迟执行（清理）
- 布尔运算符：`&&`、`||`、`!`
- 比较运算符：`==`、`!=`、`<`、`>`、`<=`、`>=`
- 位运算符：`&`、`|`、`^`、`<<`、`>>`、`~`

## If 语句

### 基本 If/Else

```hemlock
if (x > 10) {
    print("large");
} else {
    print("small");
}
```

**规则：**
- 所有分支都**必须**使用花括号
- 条件必须用括号包围
- 不支持可选花括号（与 C 不同）

### 无 Else 的 If

```hemlock
if (x > 0) {
    print("positive");
}
// 不需要 else 分支
```

### Else-If 链

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

**注意：** `else if` 是嵌套 if 语句的语法糖。以下两种写法等价：

```hemlock
// else if（语法糖）
if (a) {
    foo();
} else if (b) {
    bar();
}

// 等价的嵌套 if
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### 嵌套 If 语句

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

## While 循环

基于条件的迭代：

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**无限循环（旧式）：**
```hemlock
while (true) {
    // ... 执行工作
    if (should_exit) {
        break;
    }
}
```

**注意：** 对于无限循环，推荐使用 `loop` 关键字（见下文）。

## Loop（无限循环）

`loop` 关键字为无限循环提供更清晰的语法：

```hemlock
loop {
    // ... 执行工作
    if (should_exit) {
        break;
    }
}
```

**等价于 `while (true)`，但意图更明确。**

### 带 Break 的基本 Loop

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// 输出：0, 1, 2, 3, 4
```

### 带 Continue 的 Loop

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // 跳过打印 3
    }
    print(i);
}
// 输出：1, 2, 4, 5
```

### 嵌套 Loop

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
// 输出：0, 1, 2, 10, 11, 12
```

### 何时使用 Loop

- **使用 `loop`** - 用于故意的无限循环，通过 `break` 退出
- **使用 `while`** - 当有自然的终止条件时
- **使用 `for`** - 当迭代已知次数或遍历集合时

## For 循环

### C 风格 For

经典的三段式 for 循环：

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**组成部分：**
- **初始化器**：`let i = 0` - 循环开始前运行一次
- **条件**：`i < 10` - 每次迭代前检查
- **更新**：`i = i + 1` - 每次迭代后运行

**作用域：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i 在这里不可访问（循环作用域）
```

### For-In 循环

遍历数组元素：

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // 打印每个元素
}
```

**带索引和值：**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Index: ${i}, Value: ${arr[i]}`);
}
```

## Switch 语句

基于值的多路分支：

### 基本 Switch

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

### 带 Default 的 Switch

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

**规则：**
- `default` 在没有其他 case 匹配时执行
- `default` 可以出现在 switch 体的任何位置
- 只允许一个 default case

### 贯穿行为

没有 `break` 的 case 会贯穿到下一个 case（C 风格行为）。这是**有意的**，可用于分组 case：

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

**显式贯穿示例：**
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

**重要：** 与一些现代语言不同，Hemlock 不需要显式的 `fallthrough` 关键字。除非用 `break`、`return` 或 `throw` 终止，否则 case 会自动贯穿。始终使用 `break` 防止意外贯穿。

### 带 Return 的 Switch

在函数中，`return` 立即退出 switch：

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

### Switch 值类型

Switch 适用于任何值类型：

```hemlock
// 整数
switch (count) {
    case 0: print("zero"); break;
    case 1: print("one"); break;
}

// 字符串
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// 布尔值
switch (flag) {
    case true: print("on"); break;
    case false: print("off"); break;
}
```

**注意：** Case 使用值相等性进行比较。

## Break 和 Continue

### Break

退出最内层的循环或 switch：

```hemlock
// 在循环中
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // 退出循环
    }
    print(i);
    i = i + 1;
}

// 在 switch 中
switch (x) {
    case 1:
        print("one");
        break;  // 退出 switch
    case 2:
        print("two");
        break;
}
```

### Continue

跳到循环的下一次迭代：

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // 当 i 为 5 时跳过
    }
    print(i);  // 打印 0,1,2,3,4,6,7,8,9
}
```

**区别：**
- `break` - 完全退出循环
- `continue` - 跳到下一次迭代

## 循环标签

循环标签允许 `break` 和 `continue` 针对特定的外层循环，而不仅仅是最内层循环。这在需要从内层循环控制外层循环的嵌套循环中很有用。

### 带标签的 Break

从内层循环退出外层循环：

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // 退出外层 while 循环
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// 输出：0, 1, 2, 10（在 i=1, j=1 处停止）
```

### 带标签的 Continue

跳到外层循环的下一次迭代：

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // 跳过内层循环剩余部分，继续外层循环
        }
        print(i * 10 + j);
    }
}
// 当 i=2, j=1 时：跳到外层循环的下一次迭代
```

### For 循环中的标签

标签适用于所有循环类型：

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

### For-In 循环中的标签

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

### Loop 关键字中的标签

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

### 多重标签

可以在不同嵌套层级使用标签：

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // 跳到中间循环的下一次迭代
            }
            if (a == 1 && b == 1) {
                break outer;      // 退出最外层循环
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### 带标签循环中的无标签 Break/Continue

无标签的 `break` 和 `continue` 仍然正常工作（影响最内层循环），即使外层循环有标签：

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // 只退出内层循环
        }
        print(x * 10 + y);
    }
}
// 输出：0, 1, 10, 11, 20, 21
```

### 标签语法

- 标签是标识符后跟冒号
- 标签必须紧接在循环语句之前（`while`、`for`、`loop`）
- 标签名遵循标识符规则（字母、数字、下划线）
- 常见约定：`outer`、`inner`、`row`、`col`、描述性名称

## Defer 语句

`defer` 语句安排代码在当前函数返回时执行。这对于清理操作很有用，如关闭文件、释放资源或解锁。

### 基本 Defer

```hemlock
fn example() {
    print("start");
    defer print("cleanup");  // 函数返回时运行
    print("end");
}

example();
// 输出：
// start
// end
// cleanup
```

**关键行为：**
- 延迟语句在函数体完成**之后**执行
- 延迟语句在函数返回给调用者**之前**执行
- 即使函数抛出异常，延迟语句也总是执行

### 多个 Defer（LIFO 顺序）

当使用多个 `defer` 语句时，它们按**相反顺序**执行（后进先出）：

```hemlock
fn example() {
    defer print("first");   // 最后执行
    defer print("second");  // 第二个执行
    defer print("third");   // 第一个执行
    print("body");
}

example();
// 输出：
// body
// third
// second
// first
```

这种 LIFO 顺序是有意的 - 它符合嵌套资源清理的自然顺序（在外部资源之前关闭内部资源）。

### 带 Return 的 Defer

延迟语句在 `return` 转移控制之前执行：

```hemlock
fn get_value(): i32 {
    defer print("cleanup");
    print("before return");
    return 42;
}

let result = get_value();
print("result:", result);
// 输出：
// before return
// cleanup
// result: 42
```

### 带异常的 Defer

即使抛出异常，延迟语句也会执行：

```hemlock
fn risky() {
    defer print("cleanup 1");
    defer print("cleanup 2");
    print("before throw");
    throw "error!";
    print("after throw");  // 永远不会执行
}

try {
    risky();
} catch (e) {
    print("Caught:", e);
}
// 输出：
// before throw
// cleanup 2
// cleanup 1
// Caught: error!
```

### 资源清理模式

`defer` 的主要用例是确保资源被清理：

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // 即使出错也总是关闭

    let content = file.read();
    // ... 处理内容 ...

    // 函数返回时文件自动关闭
}
```

**不使用 defer（容易出错）：**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // 如果这里抛出异常，file.close() 永远不会被调用！
    process(content);
    file.close();
}
```

### 带闭包的 Defer

Defer 可以使用闭包来捕获状态：

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Releasing resource");
        release(resource);
    }();  // 注意：立即调用的函数表达式

    use_resource(resource);
}
```

### 何时使用 Defer

**使用 defer 的场景：**
- 关闭文件和网络连接
- 释放分配的内存
- 释放锁和互斥量
- 任何获取资源的函数中的清理

**Defer vs Finally：**
- `defer` 对于单资源清理更简单
- `try/finally` 对于带恢复的复杂错误处理更好

### 最佳实践

1. **获取资源后立即使用 defer：**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... 使用文件 ...
   ```

2. **对多个资源使用多个 defer：**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // 两个文件将按相反顺序关闭
   ```

3. **记住 LIFO 顺序用于依赖资源：**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner 在 outer 之前释放（正确的依赖顺序）
   ```

## 布尔运算符

### 逻辑与 (`&&`)

两个条件都必须为真：

```hemlock
if (x > 0 && x < 10) {
    print("single digit positive");
}
```

**短路求值：**
```hemlock
if (false && expensive_check()) {
    // expensive_check() 永远不会被调用
}
```

### 逻辑或 (`||`)

至少一个条件必须为真：

```hemlock
if (x < 0 || x > 100) {
    print("out of range");
}
```

**短路求值：**
```hemlock
if (true || expensive_check()) {
    // expensive_check() 永远不会被调用
}
```

### 逻辑非 (`!`)

取反布尔值：

```hemlock
if (!is_valid) {
    print("invalid");
}

if (!(x > 10)) {
    // 等同于：if (x <= 10)
}
```

## 比较运算符

### 相等性

```hemlock
if (x == 10) { }    // 等于
if (x != 10) { }    // 不等于
```

适用于所有类型：
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### 关系运算符

```hemlock
if (x < 10) { }     // 小于
if (x > 10) { }     // 大于
if (x <= 10) { }    // 小于等于
if (x >= 10) { }    // 大于等于
```

**类型提升适用：**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true（i32 提升为 i64）
```

## 位运算符

Hemlock 提供用于整数操作的位运算符。这些**只能用于整数类型**（i8-i64、u8-u64）。

### 二元位运算符

**按位与 (`&`)**
```hemlock
let a = 12;  // 二进制 1100
let b = 10;  // 二进制 1010
print(a & b);   // 8 (1000)
```

**按位或 (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**按位异或 (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**左移 (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - 左移 2 位
```

**右移 (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - 右移 1 位
```

### 一元位运算符

**按位取反 (`~`)**
```hemlock
let a = 12;
print(~a);      // -13（补码）

let c: u8 = 15;   // 二进制 00001111
print(~c);        // 240 (11110000)，u8 类型
```

### 位运算示例

**使用无符号类型：**
```hemlock
let c: u8 = 15;   // 二进制 00001111
let d: u8 = 7;    // 二进制 00000111

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - u8 类型
```

**类型保持：**
```hemlock
// 位运算保持操作数的类型
let x: u8 = 255;
let result = ~x;  // result 是 u8，值为 0

let y: i32 = 100;
let result2 = y << 2;  // result2 是 i32，值为 400
```

**常见模式：**
```hemlock
// 检查位是否设置
if (flags & 0x04) {
    print("bit 2 is set");
}

// 设置位
flags = flags | 0x08;

// 清除位
flags = flags & ~0x02;

// 切换位
flags = flags ^ 0x01;
```

### 运算符优先级

位运算符遵循 C 风格优先级：

1. `~`（一元取反）- 最高，与 `!` 和 `-` 同级
2. `<<`、`>>`（位移）- 高于比较，低于 `+`/`-`
3. `&`（按位与）- 高于 `^` 和 `|`
4. `^`（按位异或）- 在 `&` 和 `|` 之间
5. `|`（按位或）- 低于 `&` 和 `^`，高于 `&&`
6. `&&`、`||`（逻辑）- 最低优先级

**示例：**
```hemlock
// & 优先级高于 |
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// 位移优先级高于位运算符
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// 使用括号提高清晰度
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**重要注意事项：**
- 位运算符只能用于整数类型（不能用于浮点数、字符串等）
- 类型提升遵循标准规则（较小类型提升为较大类型）
- 右移 (`>>`) 对有符号类型是算术移位，对无符号类型是逻辑移位
- 移位量不进行范围检查（大移位量的行为取决于平台）

## 运算符优先级（完整）

从高到低优先级：

1. **一元**：`!`、`-`、`~`
2. **乘除**：`*`、`/`、`%`
3. **加减**：`+`、`-`
4. **位移**：`<<`、`>>`
5. **关系**：`<`、`>`、`<=`、`>=`
6. **相等**：`==`、`!=`
7. **按位与**：`&`
8. **按位异或**：`^`
9. **按位或**：`|`
10. **逻辑与**：`&&`
11. **逻辑或**：`||`

**使用括号提高清晰度：**
```hemlock
// 不清晰
if (a || b && c) { }

// 清晰
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## 常见模式

### 模式：输入验证

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### 模式：范围检查

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("valid score");
}
```

### 模式：状态机

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

### 模式：带过滤的迭代

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 只打印偶数
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // 跳过奇数
    }
    print(arr[i]);
}
```

### 模式：提前退出

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // 提前退出
        }
    }
    return -1;  // 未找到
}
```

## 最佳实践

1. **始终使用花括号** - 即使是单语句块也要（语法强制）
2. **显式条件** - 使用 `x == 0` 而不是 `!x` 以提高清晰度
3. **避免深层嵌套** - 将嵌套条件提取到函数中
4. **使用提前返回** - 用守卫子句减少嵌套
5. **分解复杂条件** - 拆分为命名的布尔变量
6. **switch 中使用 default** - 始终包含 default case
7. **注释贯穿** - 使有意的贯穿明确

## 常见陷阱

### 陷阱：条件中的赋值

```hemlock
// 这是不允许的（条件中不能赋值）
if (x = 10) { }  // 错误：语法错误

// 使用比较代替
if (x == 10) { }  // OK
```

### 陷阱：Switch 中缺少 Break

```hemlock
// 意外贯穿
switch (x) {
    case 1:
        print("one");
        // 缺少 break - 会贯穿！
    case 2:
        print("two");  // 对 1 和 2 都执行
        break;
}

// 修复：添加 break
switch (x) {
    case 1:
        print("one");
        break;  // 现在正确
    case 2:
        print("two");
        break;
}
```

### 陷阱：循环变量作用域

```hemlock
// i 的作用域限于循环
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // 错误：i 在这里未定义
```

## 示例

### 示例：FizzBuzz

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

### 示例：素数检查

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

### 示例：菜单系统

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

## 相关主题

- [Functions](functions.md) - 函数调用和返回的控制流
- [Error Handling](error-handling.md) - 异常的控制流
- [Types](types.md) - 条件中的类型转换

## 另请参阅

- **语法**：参见 [Syntax](syntax.md) 了解语句语法细节
- **运算符**：参见 [Types](types.md) 了解运算中的类型提升
