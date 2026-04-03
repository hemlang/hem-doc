# 术语表

编程或系统概念的新手？本术语表用通俗语言解释 Hemlock 文档中使用的术语。

---

## A

### 分配 / 内存分配（Allocate / Allocation）
**含义：** 向计算机申请一块内存来使用。

**类比：** 就像从图书馆借书一样——你借用了一些空间，之后需要归还。

**在 Hemlock 中：**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### 数组（Array）
**含义：** 一组存储在一起的值，通过位置（索引）访问。

**类比：** 就像一排编号为 0、1、2、3... 的邮箱。你可以把东西放进 2 号邮箱，之后再从 2 号邮箱取出。

**在 Hemlock 中：**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### 异步（Async / Asynchronous）
**含义：** 可以在"后台"运行的代码，同时其他代码继续执行。在 Hemlock 中，异步代码实际上在不同的 CPU 核心上同时运行。

**类比：** 就像同时做多道菜——你把饭放上锅，然后趁它煮着的时候切蔬菜。两件事同时进行。

**在 Hemlock 中：**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### 布尔值（Boolean / Bool）
**含义：** 一个只能是 `true` 或 `false` 的值。没有其他可能。

**命名来源：** 以研究真/假逻辑的数学家 George Boole 命名。

**在 Hemlock 中：**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### 边界检查（Bounds Checking）
**含义：** 自动验证你是否试图访问超出已分配内存范围的数据。防止崩溃和安全漏洞。

**类比：** 就像图书管理员在你请求一本书之前先检查它是否真的存在。

**在 Hemlock 中：**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### 缓冲区（Buffer）
**含义：** 一个安全的原始字节容器，具有已知大小。Hemlock 会检查你不会读写超出其边界。

**类比：** 就像一个有固定数量格子的保险柜。你可以使用任何格子，但如果保险柜只有 10 个格子，你不能访问第 50 个格子。

**在 Hemlock 中：**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### 闭包（Closure）
**含义：** 一个"记住"创建它时所在位置的变量的函数，即使那段代码已经执行完毕。

**类比：** 就像一张写着"把你给我的数字加 5"的纸条——"5"被嵌入了纸条中。

**在 Hemlock 中：**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### 强制转换（Coercion，类型强制转换）
**含义：** 在需要时自动将值从一种类型转换为另一种类型。

**示例：** 当你将整数和小数相加时，整数会先自动转换为小数。

**在 Hemlock 中：**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### 编译 / 编译器（Compile / Compiler）
**含义：** 将你的代码翻译成计算机可以直接运行的程序。编译器（`hemlockc`）读取你的 `.hml` 文件并创建可执行文件。

**类比：** 就像把一本书从英语翻译成西班牙语——内容相同，但现在说西班牙语的人可以阅读了。

**在 Hemlock 中：**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### 并发（Concurrency）
**含义：** 多件事在重叠的时间内发生。在 Hemlock 中，这意味着在多个 CPU 核心上实际的并行执行。

**类比：** 两个厨师在同一个厨房里同时做不同的菜。

---

## D

### 延迟（Defer）
**含义：** 安排某件事稍后发生，即当前函数结束时。适用于清理工作。

**类比：** 就像告诉自己"离开时关灯"——你现在设好提醒，之后自动执行。

**在 Hemlock 中：**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### 鸭子类型（Duck Typing）
**含义：** 如果它看起来像鸭子、叫起来像鸭子，就把它当鸭子。在代码中：如果一个对象具有你需要的字段/方法，就直接使用它——不用担心它的正式"类型"。

**命名来源：** 鸭子测试——一种推理形式。

**在 Hemlock 中：**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### 表达式（Expression）
**含义：** 产生值的代码。可以用在任何期望值的地方。

**示例：** `42`、`x + y`、`get_name()`、`true && false`

### 枚举（Enum / Enumeration）
**含义：** 一个具有固定一组可能值的类型，每个值都有名称。

**类比：** 就像一个下拉菜单——你只能从列出的选项中选择。

**在 Hemlock 中：**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### 浮点数（Float / Floating-Point）
**含义：** 一个带小数点的数字。之所以叫"浮点"，是因为小数点可以在不同位置。

**在 Hemlock 中：**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### 释放（Free）
**含义：** 将你用完的内存归还给系统，以便被重新使用。

**类比：** 归还图书馆的书，这样其他人就可以借了。

**在 Hemlock 中：**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### 函数（Function）
**含义：** 一个可重用的代码块，接受输入（参数）并可能产生输出（返回值）。

**类比：** 就像一份食谱——给它食材（输入），按步骤操作，得到一道菜（输出）。

**在 Hemlock 中：**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### 垃圾回收（Garbage Collection，GC）
**含义：** 自动清理内存。运行时定期查找未使用的内存并为你释放。

**为什么 Hemlock 没有它：** GC 可能导致不可预测的暂停。Hemlock 偏好显式控制——由你决定何时释放内存。

**注意：** 大多数 Hemlock 类型（字符串、数组、对象）在离开作用域时会自动清理。只有来自 `alloc()` 的原始 `ptr` 需要手动 `free()`。

---

## H

### 堆（Heap）
**含义：** 用于需要比当前函数更长生命周期的数据的内存区域。你显式地分配和释放堆内存。

**对比：** 栈（自动的、临时的局部变量存储）

**在 Hemlock 中：**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### 索引（Index）
**含义：** 数组或字符串中某个元素的位置。在 Hemlock 中从 0 开始。

**在 Hemlock 中：**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### 整数（Integer）
**含义：** 没有小数点的整数。可以是正数、负数或零。

**在 Hemlock 中：**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### 解释器（Interpreter）
**含义：** 一个读取你的代码并直接逐行运行它的程序。

**对比：** 编译器（先翻译代码，然后运行翻译后的版本）

**在 Hemlock 中：**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### 字面量（Literal）
**含义：** 直接写在代码中的值，不是通过计算得到的。

**示例：**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### 内存泄漏（Memory Leak）
**含义：** 忘记释放已分配的内存。内存保持被预留但未使用的状态，浪费资源。

**类比：** 借了图书馆的书却从不归还。最终，图书馆会没有书可借。

**在 Hemlock 中：**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### 方法（Method）
**含义：** 附加在对象或类型上的函数。

**在 Hemlock 中：**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### 互斥锁（Mutex）
**含义：** 一种锁，确保同一时间只有一个线程访问某些东西。防止多个线程同时操作共享数据时的数据损坏。

**类比：** 就像卫生间的门锁——同一时间只能有一个人使用。

---

## N

### 空值（Null）
**含义：** 一个特殊值，表示"没有"或"无值"。

**在 Hemlock 中：**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### 对象（Object）
**含义：** 一组命名值（字段/属性）的集合。

**在 Hemlock 中：**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### 参数（Parameter）
**含义：** 函数期望在调用时接收的变量。

**也称为：** 实参（Argument）（技术上说，parameter 在定义中，argument 在调用中）

**在 Hemlock 中：**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### 指针（Pointer）
**含义：** 一个保存内存地址的值——它"指向"数据存储的位置。

**类比：** 就像一个街道地址。地址不是房子——它告诉你在哪里找到房子。

**在 Hemlock 中：**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### 原始类型（Primitive）
**含义：** 基本的、内置的类型，不由其他类型组成。

**在 Hemlock 中：** `i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`、`f32`、`f64`、`bool`、`rune`、`null`

---

## R

### 引用计数（Reference Counting，Refcounting）
**含义：** 跟踪有多少东西在使用某份数据。当没有任何东西使用它时，自动清理。

**在 Hemlock 中：** 字符串、数组、对象和缓冲区在内部使用引用计数。你看不到它，但它防止了最常见类型的内存泄漏。

### 返回值（Return Value）
**含义：** 函数完成时发送回来的值。

**在 Hemlock 中：**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**含义：** 一个 Unicode 字符（码点）。可以表示任何字符，包括表情符号。

**为什么叫"rune"？** 这个术语来自 Go 语言。它强调这是一个完整的字符，而不仅仅是一个字节。

**在 Hemlock 中：**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### 运行时（Runtime）
**含义：** 程序实际运行的时间（相对于"编译时"，即代码被翻译时）。

**也指：** 与程序一起运行的支持代码（例如内存分配器）。

---

## S

### 作用域（Scope）
**含义：** 变量存在并可以使用的代码区域。

**在 Hemlock 中：**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### 栈（Stack）
**含义：** 用于临时、短期数据的内存。自动管理——当函数返回时，其栈空间被回收。

**对比：** 堆（更长生命周期，手动管理）

### 语句（Statement）
**含义：** 一条指令或命令。语句**做事情**；表达式**产生值**。

**示例：** `let x = 5;`、`print("hi");`、`if (x > 0) { ... }`

### 字符串（String）
**含义：** 一个文本字符序列。

**在 Hemlock 中：**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### 结构类型（Structural Typing）
**含义：** 基于结构（存在哪些字段/方法）而非名称的类型兼容性。与"鸭子类型"相同。

---

## T

### 线程（Thread）
**含义：** 一条独立的执行路径。多个线程可以在不同的 CPU 核心上同时运行。

**在 Hemlock 中：** `spawn()` 创建一个新线程。

### 类型（Type）
**含义：** 值所代表的数据种类。决定哪些操作是有效的。

**在 Hemlock 中：**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### 类型注解（Type Annotation）
**含义：** 显式声明一个变量应该具有什么类型。

**在 Hemlock 中：**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**含义：** 一种支持所有世界语言和表情符号的文本编码方式。每个字符可以是 1-4 字节。

**在 Hemlock 中：** 所有字符串都是 UTF-8。

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### 变量（Variable）
**含义：** 一个保存值的命名存储位置。

**在 Hemlock 中：**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## 快速参考：我应该使用什么类型？

| 场景 | 使用类型 | 原因 |
|------|---------|------|
| 只需要一个数字 | `let x = 42;` | Hemlock 自动选择正确的类型 |
| 计数 | `i32` | 对大多数计数来说足够大 |
| 超大数字 | `i64` | 当 i32 不够时 |
| 字节 (0-255) | `u8` | 文件、网络数据 |
| 小数 | `f64` | 精确的小数运算 |
| 是/否值 | `bool` | 只有 `true` 或 `false` |
| 文本 | `string` | 任何文本内容 |
| 单个字符 | `rune` | 一个字母/表情符号 |
| 列表 | `array` | 有序集合 |
| 命名字段 | `object` | 分组相关数据 |
| 原始内存 | `buffer` | 安全的字节存储 |
| FFI/系统工作 | `ptr` | 高级，手动内存 |

---

## 另请参阅

- [快速入门](getting-started/quick-start.md) - 你的第一个 Hemlock 程序
- [类型系统](language-guide/types.md) - 完整类型文档
- [内存管理](language-guide/memory.md) - 理解内存
