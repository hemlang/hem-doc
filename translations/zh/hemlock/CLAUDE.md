# Hemlock 语言设计理念

> "一门小巧、非安全的语言，用于安全地编写非安全代码。"

本文档记录了 AI 助手在使用 Hemlock 时需要了解的核心设计原则。
如需详细文档，请参阅 `docs/README.md` 和 `stdlib/docs/` 目录。

---

## 核心定位

Hemlock 是一门**系统脚本语言**，具有手动内存管理和显式控制：
- 拥有 C 语言的能力，同时具备现代脚本的便利性
- 内置结构化异步并发
- 无隐藏行为或魔法

**Hemlock 不是：** 内存安全的、带垃圾回收的语言，也不会隐藏复杂性。
**Hemlock 是：** 显式优于隐式、具有教育意义、系统工作的"C 脚本层"。

---

## 设计原则

### 1. 显式优于隐式
- 分号是强制性的（无自动分号插入）
- 手动内存管理（alloc/free）
- 类型注解可选，但在运行时检查

### 2. 默认动态，可选类型
- 每个值都有运行时类型标签
- 字面量推断类型：`42` → i32，`5000000000` → i64，`3.14` → f64
- 可选的类型注解强制执行运行时检查

### 3. 非安全是特性
- 允许指针运算（用户自行负责）
- 原始 `ptr` 无边界检查（使用 `buffer` 获得安全性）
- 允许双重释放导致崩溃

### 4. 结构化并发是一等公民
- 内置 `async`/`await`，基于 pthread 的并行
- 用于通信的 channel
- `spawn`/`join`/`detach` 用于任务管理

### 5. 类 C 语法
- `{}` 块总是必需的
- 注释：`// 行注释` 和 `/* 块注释 */`
- 运算符与 C 一致：`+`、`-`、`*`、`%`、`&&`、`||`、`!`、`&`、`|`、`^`、`<<`、`>>`
- 自增/自减：`++x`、`x++`、`--x`、`x--`（前缀和后缀）
- 复合赋值：`+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`
- `/` 总是返回浮点数（使用 `divi()` 进行整数除法）
- 类型语法：`let x: type = value;`

---

## 快速参考

### 类型
```
有符号：  i8, i16, i32, i64
无符号：  u8, u16, u32, u64
浮点：    f32, f64
其他：    bool, string, rune, array, ptr, buffer, null, object, file, task, channel
别名：    integer (i32), number (f64), byte (u8)
```

**类型提升：** i8 → i16 → i32 → i64 → f32 → f64（浮点总是赢，但 i64/u64 + f32 → f64 以保持精度）

### 字面量
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> i32 最大值)
let hex = 0xDEADBEEF;    // 十六进制字面量
let bin = 0b1010;        // 二进制字面量
let oct = 0o777;         // 八进制字面量
let sep = 1_000_000;     // 允许数字分隔符
let pi = 3.14;           // f64
let half = .5;           // f64 (无前导零)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // 十六进制和 Unicode 转义
let ch = 'A';            // rune
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### 类型转换
```hemlock
// 类型构造函数 - 将字符串解析为类型
let n = i32("42");       // 将字符串解析为 i32
let f = f64("3.14");     // 将字符串解析为 f64
let b = bool("true");    // 将字符串解析为 bool ("true" 或 "false")

// 支持所有数值类型
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// 十六进制和负数
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// 类型别名也适用
let x = integer("100");  // 等同于 i32("100")
let y = number("1.5");   // 等同于 f64("1.5")
let z = byte("200");     // 等同于 u8("200")

// 数值类型之间的转换
let big = i64(42);       // i32 转 i64
let truncated = i32(3.99); // f64 转 i32 (截断为 3)

// 类型注解验证类型（但不解析字符串）
let f: f64 = 100;        // 通过注解将 i32 转为 f64（数值强制转换可行）
// let n: i32 = "42";    // 错误 - 使用 i32("42") 解析字符串
```

### 内省
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
"hello".length;          // 5 (字符串长度，按 rune 计)
"hello".byte_length;     // 5 (字符串长度，按字节计)
[1, 2, 3].length;        // 3 (数组长度)
```

### 内存
```hemlock
let p = alloc(64);       // 原始指针
let b = buffer(64);      // 安全缓冲区（边界检查）
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // 需要手动清理
```

### 控制流
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // 无限循环（比 while(true) 更清晰）
switch (x) { case 1: break; default: break; }  // C 风格贯穿
defer cleanup();         // 函数返回时执行

// 循环标签用于嵌套循环中的定向 break/continue
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // 跳出外层循环
        if (i == 3) { continue outer; }  // 继续外层循环
    }
}
```

### 模式匹配
```hemlock
// match 表达式 - 返回值
let result = match (value) {
    0 => "zero",                    // 字面量模式
    1 | 2 | 3 => "small",           // OR 模式
    n if n < 10 => "medium",        // 守卫表达式
    n => "large: " + n              // 变量绑定
};

// 类型模式
match (val) {
    n: i32 => "integer",
    s: string => "string",
    _ => "other"                    // 通配符
}

// 对象解构
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// 带剩余部分的数组解构
match (arr) {
    [] => "empty",
    [first, ...rest] => "head: " + first,
    _ => "other"
}

// 嵌套模式
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

完整文档请参阅 `docs/language-guide/pattern-matching.md`。

### 空值合并运算符
```hemlock
// 空值合并 (??) - 如果左侧非空则返回左侧，否则返回右侧
let name = user.name ?? "Anonymous";
let first = a ?? b ?? c ?? "fallback";

// 空值合并赋值 (??=) - 仅当为空时赋值
let config = null;
config ??= { timeout: 30 };    // config 现在是 { timeout: 30 }
config ??= { timeout: 60 };    // config 不变（非空）

// 适用于属性和索引
obj.field ??= "default";
arr[0] ??= "first";

// 安全导航 (?.) - 如果对象为空则返回 null
let city = user?.address?.city;  // 如果任何部分为空则为 null
let upper = name?.to_upper();    // 安全方法调用
let item = arr?.[0];             // 安全索引
```

### 函数
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // 匿名/闭包

// 表达式体函数（箭头语法）
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // 匿名表达式体

// 参数修饰符
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // 按引用传递
fn print_all(const items: array) { for (i in items) { print(i); } }  // 不可变
```

### 命名参数
```hemlock
// 函数可以使用命名参数调用
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// 位置参数（传统方式）
create_user("Alice", 25, false);

// 命名参数 - 可以任意顺序
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// 通过命名所需参数来跳过可选参数
create_user("David", active: false);  // 使用默认 age=18

// 命名参数必须在位置参数之后
create_user("Eve", age: 21);          // 正确：位置参数在前，命名参数在后
// create_user(name: "Bad", 25);      // 错误：位置参数在命名参数之后
```

**规则：**
- 命名参数使用 `name: value` 语法
- 可以在位置参数之后以任意顺序出现
- 位置参数不能跟在命名参数之后
- 与默认/可选参数配合使用
- 未知参数名会导致运行时错误

### 对象和枚举
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// 对象简写语法（ES6 风格）
let name = "Alice";
let age = 30;
let person = { name, age };         // 等同于 { name: name, age: age }

// 对象展开运算符
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // 复制 defaults，覆盖 size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### 复合类型（交叉/鸭子类型）
```hemlock
// 定义结构类型
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// 复合类型：对象必须满足所有类型
let person: HasName & HasAge = { name: "Alice", age: 30 };

// 带复合类型的函数参数
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

// 三个或更多类型
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// 允许额外字段（鸭子类型）
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // 正确 - 额外字段被忽略
};
```

复合类型提供类似接口的行为，无需单独的 `interface` 关键字，
构建在现有的 `define` 和鸭子类型范式之上。

### 类型别名
```hemlock
// 简单类型别名
type Integer = i32;
type Text = string;

// 函数类型别名
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// 复合类型别名（适合可重用接口）
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// 泛型类型别名
type Pair<T> = { first: T, second: T };

// 使用类型别名
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

类型别名为复杂类型创建命名快捷方式，提高可读性和可维护性。

### 函数类型
```hemlock
// 函数类型注解用于参数
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// 返回函数的高阶函数
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// 异步函数类型
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// 多参数函数类型
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Const 参数
```hemlock
// Const 参数 - 深度不可变性
fn print_all(const items: array) {
    // items.push(4);  // 错误：无法修改 const 参数
    for (item in items) {
        print(item);
    }
}

// 对象的 const - 无法通过任何路径修改
fn describe(const person: object) {
    print(person.name);       // 正确：允许读取
    // person.name = "Bob";   // 错误：无法修改
}

// 允许嵌套读取访问
fn get_city(const user: object) {
    return user.address.city;  // 正确：读取嵌套属性
}
```

`const` 修饰符防止对参数的任何修改，包括嵌套属性。
这为不应修改其输入的函数提供了编译时安全性。

### Ref 参数（按引用传递）
```hemlock
// Ref 参数 - 直接修改调用者的变量
fn increment(ref x: i32) {
    x = x + 1;  // 修改原始变量
}

let count = 10;
increment(count);
print(count);  // 11 - 原始值已修改

// 经典交换函数
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// 混合 ref 和普通参数
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

`ref` 修饰符传递对调用者变量的引用，允许函数直接修改它。
没有 `ref` 时，原始类型按值传递（复制）。当需要在不返回值的情况下
修改调用者状态时，使用 `ref`。

**规则：**
- `ref` 参数必须传递变量，不能是字面量或表达式
- 适用于所有类型（原始类型、数组、对象）
- 与类型注解结合：`ref x: i32`
- 不能与 `const` 结合（它们是对立的）

### Define 中的方法签名
```hemlock
// 带方法签名的 define（接口模式）
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // 必需的方法签名
}

// 对象必须提供必需的方法
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// 使用 ? 表示可选方法
define Serializable {
    fn serialize(): string,        // 必需
    fn pretty?(): string           // 可选方法
}

// Self 类型指向定义类型
define Cloneable {
    fn clone(): Self   // 返回与对象相同的类型
}
```

`define` 块中的方法签名使用逗号分隔（类似 TypeScript 接口），
建立对象必须满足的契约，并通过 Hemlock 的鸭子类型系统实现
类似接口的编程模式。

### 错误处理
```hemlock
try { throw "error"; } catch (e) { print(e); } finally { cleanup(); }
panic("unrecoverable");  // 立即退出，不可捕获
```

### 异步/并发
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // 或 join(task)
detach(spawn(background_work));

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**内存所有权：** 任务接收原始值的副本，但共享指针。如果将 `ptr` 传递给派生任务，
必须确保内存在任务完成前保持有效。在 `free()` 之前使用 `join()`，
或使用 channel 信号通知完成。

### 用户输入
```hemlock
let name = read_line();          // 从 stdin 读取行（阻塞）
print("Hello, " + name);
write("无换行");                  // 输出不带尾部换行
eprint("Error message");         // 输出到 stderr

// read_line() 在 EOF 时返回 null
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Got:", line);
}
```

### 文件 I/O
```hemlock
let f = open("file.txt", "r");  // 模式：r, w, a, r+, w+, a+
let content = f.read();
f.write("data");
f.seek(0);
f.close();
```

### 信号
```hemlock
signal(SIGINT, fn(sig) { print("Interrupted"); });
raise(SIGUSR1);
```

---

## 字符串方法 (19 个)

`substr`、`slice`、`find`、`contains`、`split`、`trim`、`to_upper`、`to_lower`、
`starts_with`、`ends_with`、`replace`、`replace_all`、`repeat`、`char_at`、
`byte_at`、`chars`、`bytes`、`to_bytes`、`deserialize`

模板字符串：`` `Hello ${name}!` ``

**字符串可变性：** 字符串可通过索引赋值修改（`s[0] = 'H'`），但所有字符串方法
返回新字符串而不修改原字符串。这允许在需要时进行原地修改，同时保持方法链的函数式风格。

**字符串长度属性：**
```hemlock
let s = "hello 🚀";
print(s.length);       // 7 (字符/rune 计数)
print(s.byte_length);  // 10 (字节计数 - emoji 是 4 字节 UTF-8)
```

## 数组方法 (23 个)

`push`、`pop`、`shift`、`unshift`、`insert`、`remove`、`find`、`contains`、
`slice`、`join`、`concat`、`reverse`、`first`、`last`、`clear`、`map`、`filter`、`reduce`、
`every`、`some`、`indexOf`、`sort`、`fill`

```hemlock
// every(predicate) - 如果所有元素满足谓词则为 true
let allPositive = [1, 2, 3].every(fn(x) { return x > 0; });  // true

// some(predicate) - 如果任一元素满足谓词则为 true
let hasEven = [1, 2, 3].some(fn(x) { return x % 2 == 0; });  // true

// indexOf(value) - 查找值的第一个索引，未找到返回 -1
let idx = ["a", "b", "c"].indexOf("b");  // 1

// sort(comparator?) - 原地排序，可选比较器
let nums = [3, 1, 4, 1, 5];
nums.sort();                              // [1, 1, 3, 4, 5]
nums.sort(fn(a, b) { return b - a; });    // 降序

// fill(value, start?, end?) - 用值填充
let arr = [1, 2, 3, 4, 5];
arr.fill(0);        // [0, 0, 0, 0, 0]
arr.fill(9, 2);     // [0, 0, 9, 9, 9]
arr.fill(7, 1, 4);  // [0, 7, 7, 7, 9]
```

类型化数组：`let nums: array<i32> = [1, 2, 3];`

---

## 标准库 (42 个模块)

使用 `@stdlib/` 前缀导入：
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| 模块 | 描述 |
|--------|-------------|
| `arena` | 竞技场内存分配器（bump 分配） |
| `args` | 命令行参数解析 |
| `assert` | 断言工具 |
| `async` | ThreadPool、parallel_map |
| `async_fs` | 异步文件 I/O 操作 |
| `collections` | HashMap、Queue、Stack、Set、LinkedList、LRUCache |
| `compression` | gzip、gunzip、deflate |
| `crypto` | aes_encrypt、rsa_sign、random_bytes |
| `csv` | CSV 解析和生成 |
| `datetime` | DateTime 类、格式化、解析 |
| `encoding` | base64_encode、hex_encode、url_encode |
| `env` | getenv、setenv、exit、get_pid |
| `fmt` | 字符串格式化工具 |
| `fs` | read_file、write_file、list_dir、exists |
| `glob` | 文件模式匹配 |
| `hash` | sha256、sha512、md5、djb2 |
| `http` | http_get、http_post、http_request |
| `ipc` | 进程间通信 |
| `iter` | 迭代器工具 |
| `json` | parse、stringify、pretty、get、set |
| `logging` | 带级别的日志记录器 |
| `math` | sin、cos、sqrt、pow、rand、PI、E |
| `net` | TcpListener、TcpStream、UdpSocket |
| `os` | platform、arch、cpu_count、hostname |
| `path` | 文件路径操作 |
| `process` | fork、exec、wait、kill |
| `random` | 随机数生成 |
| `regex` | compile、test (POSIX ERE) |
| `retry` | 带退避的重试逻辑 |
| `semver` | 语义化版本控制 |
| `shell` | Shell 命令工具 |
| `sqlite` | SQLite 数据库、query、exec、事务 |
| `strings` | pad_left、is_alpha、reverse、lines |
| `terminal` | ANSI 颜色和样式 |
| `termios` | 原始终端输入、按键检测 |
| `testing` | describe、test、expect |
| `time` | now、time_ms、sleep、clock |
| `toml` | TOML 解析和生成 |
| `url` | URL 解析和操作 |
| `uuid` | UUID 生成 |
| `vector` | 向量相似性搜索 (USearch ANN) |
| `websocket` | WebSocket 客户端 |

详细模块文档请参阅 `stdlib/docs/`。

---

## FFI（外部函数接口）

从共享库声明和调用 C 函数：
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hello!");  // 6
let pid = getpid();
```

从模块导出 FFI 函数：
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

动态 FFI（运行时绑定）：
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

类型：`FFI_INT`、`FFI_DOUBLE`、`FFI_POINTER`、`FFI_STRING`、`FFI_VOID` 等。

---

## 原子操作

使用原子操作进行无锁并发编程：

```hemlock
// 为原子 i32 分配内存
let p = alloc(4);
ptr_write_i32(p, 0);

// 原子加载/存储
let val = atomic_load_i32(p);        // 原子读取
atomic_store_i32(p, 42);             // 原子写入

// 获取并修改操作（返回旧值）
let old = atomic_add_i32(p, 10);     // 加法，返回旧值
old = atomic_sub_i32(p, 5);          // 减法，返回旧值
old = atomic_and_i32(p, 0xFF);       // 按位与
old = atomic_or_i32(p, 0x10);        // 按位或
old = atomic_xor_i32(p, 0x0F);       // 按位异或

// 比较并交换 (CAS)
let success = atomic_cas_i32(p, 42, 100);  // 如果 *p == 42，设置为 100
// 如果交换成功返回 true，否则返回 false

// 原子交换
old = atomic_exchange_i32(p, 999);   // 交换，返回旧值

free(p);

// 可用 i64 变体 (atomic_load_i64, atomic_add_i64, 等)

// 内存屏障（完全屏障）
atomic_fence();
```

所有操作使用顺序一致性（`memory_order_seq_cst`）。

---

## 项目结构

```
hemlock/
├── src/
│   ├── frontend/         # 共享：词法分析器、解析器、AST、模块
│   ├── backends/
│   │   ├── interpreter/  # hemlock：树遍历解释器
│   │   └── compiler/     # hemlockc：C 代码生成器
│   ├── tools/
│   │   ├── lsp/          # 语言服务器协议
│   │   └── bundler/      # 打包/包工具
├── runtime/              # 编译程序运行时 (libhemlock_runtime.a)
├── stdlib/               # 标准库 (42 个模块)
│   └── docs/             # 模块文档
├── docs/                 # 完整文档
│   ├── language-guide/   # 类型、字符串、数组等
│   ├── reference/        # API 参考
│   └── advanced/         # 异步、FFI、信号等
├── tests/                # 625+ 测试
└── examples/             # 示例程序
```

---

## 代码风格指南

### 常量和魔法数字

在向 C 代码库添加数值常量时，请遵循以下准则：

1. **在 `include/hemlock_limits.h` 中定义常量** - 此文件是所有编译时和运行时限制、容量和命名常量的集中位置。

2. **使用 `HML_` 前缀的描述性名称** - 所有常量应以 `HML_` 为前缀以明确命名空间。

3. **避免魔法数字** - 用命名常量替换硬编码的数值。示例：
   - 类型范围限制：`HML_I8_MIN`、`HML_I8_MAX`、`HML_U32_MAX`
   - 缓冲区容量：`HML_INITIAL_ARRAY_CAPACITY`、`HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - 时间转换：`HML_NANOSECONDS_PER_SECOND`、`HML_MILLISECONDS_PER_SECOND`
   - 哈希种子：`HML_DJB2_HASH_SEED`
   - ASCII 值：`HML_ASCII_CASE_OFFSET`、`HML_ASCII_PRINTABLE_START`

4. **包含 `hemlock_limits.h`** - 源文件应包含此头文件（通常通过 `internal.h`）以访问常量。

5. **记录用途** - 添加注释说明每个常量代表什么。

---

## 禁止事项

- 添加隐式行为（ASI、GC、自动清理）
- 隐藏复杂性（魔法优化、隐藏引用计数）
- 破坏现有语义（分号、手动内存、可变字符串）
- 在隐式转换中丢失精度
- 使用魔法数字 - 改为在 `hemlock_limits.h` 中定义命名常量

---

## 测试

```bash
make test              # 运行解释器测试
make test-compiler     # 运行编译器测试
make parity            # 运行对等测试（两者必须匹配）
make test-all          # 运行所有测试套件
```

**重要：** 由于异步/并发问题，测试可能会挂起。运行测试时始终使用超时：
```bash
timeout 60 make test   # 60 秒超时
timeout 120 make parity
```

测试类别：primitives、memory、strings、arrays、functions、objects、async、ffi、defer、signals、switch、bitwise、typed_arrays、modules、stdlib_*

---

## 编译器/解释器架构

Hemlock 有两个共享通用前端的执行后端：

```
源码 (.hml)
    ↓
┌─────────────────────────────┐
│  共享前端                    │
│  - 词法分析器 (src/frontend/)│
│  - 解析器 (src/frontend/)    │
│  - AST (src/frontend/)       │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│   解释器    │    │   编译器    │
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ 树遍历     │    │ 类型检查   │
│ 求值       │    │ AST → C    │
│            │    │ gcc 链接   │
└────────────┘    └────────────┘
```

### 编译器类型检查

编译器（`hemlockc`）包含编译时类型检查，**默认启用**：

```bash
hemlockc program.hml -o program    # 类型检查，然后编译
hemlockc --check program.hml       # 仅类型检查，不编译
hemlockc --no-type-check prog.hml  # 禁用类型检查
hemlockc --strict-types prog.hml   # 对隐式 'any' 类型发出警告
```

类型检查器：
- 在编译时验证类型注解
- 将无类型代码视为动态（`any` 类型）- 始终有效
- 为拆箱提供优化提示
- 使用宽松的数值转换（范围在运行时验证）

### 目录结构

```
hemlock/
├── src/
│   ├── frontend/           # 共享：词法分析器、解析器、AST、模块
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock：树遍历解释器
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc：C 代码生成器
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # 语言服务器
│   │   └── bundler/        # 打包/包工具
├── runtime/                # 编译程序的 libhemlock_runtime.a
├── stdlib/                 # 共享标准库
└── tests/
    ├── parity/             # 必须通过两个后端的测试
    ├── interpreter/        # 解释器特定测试
    └── compiler/           # 编译器特定测试
```

---

## 对等优先开发

**解释器和编译器必须对相同输入产生相同输出。**

### 开发策略

添加或修改语言特性时：

1. **设计** - 在共享前端定义 AST/语义更改
2. **实现解释器** - 添加树遍历求值
3. **实现编译器** - 添加 C 代码生成
4. **添加对等测试** - 在 `tests/parity/` 中编写带 `.expected` 文件的测试
5. **验证** - 合并前运行 `make parity`

### 对等测试结构

```
tests/parity/
├── language/       # 核心语言特性（控制流、闭包等）
├── builtins/       # 内置函数（print、typeof、memory 等）
├── methods/        # 字符串和数组方法
└── modules/        # import/export、stdlib 导入
```

每个测试有两个文件：
- `feature.hml` - 测试程序
- `feature.expected` - 预期输出（两个后端必须匹配）

### 对等测试结果

| 状态 | 含义 |
|--------|---------|
| `PASSED` | 解释器和编译器都匹配预期输出 |
| `INTERP_ONLY` | 解释器工作，编译器失败（需要修复编译器） |
| `COMPILER_ONLY` | 编译器工作，解释器失败（罕见） |
| `FAILED` | 两者都失败（测试或实现错误） |

### 需要对等的内容

- 所有语言结构（if、while、for、switch、defer、try/catch）
- 所有运算符（算术、位、逻辑、比较）
- 所有内置函数（print、typeof、alloc 等）
- 所有字符串和数组方法
- 类型强制和提升规则
- 运行时错误的错误消息

### 可能不同的内容

- 性能特征
- 内存布局细节
- 调试/堆栈跟踪格式
- 编译错误（编译器可能在编译时捕获更多）

### 添加对等测试

```bash
# 1. 创建测试文件
cat > tests/parity/language/my_feature.hml << 'EOF'
// 测试描述
let x = some_feature();
print(x);
EOF

# 2. 从解释器生成预期输出
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. 验证对等
make parity
```

---

## 版本

**v1.9.2** - 当前版本特性：
- **编译器未装箱循环计数器修复** - 修复了一个关键的代码生成错误，优化的循环计数器（原生 `int32_t`）被直接用作 `HmlValue` 初始化器而没有装箱。`codegen_is_main_var` 检查错误地阻止了在模块/闭包函数中主级变量遮蔽未装箱循环计数器时 boxing 包装器（`hml_val_i32()`）的发出。修复了 `@stdlib/collections` 和 `@stdlib/encoding` 的编译。
- **`clear()` 对象方法分派** - 编译器现在在非数组类型上调用 `.clear()` 时正确分派到对象方法。之前 `.clear()` 无论接收者类型如何都总是生成 `hml_array_clear()`。
- **`exec()` 导入遮蔽修复** - 编译器的内置 `exec()` 处理器现在在分派到系统 exec 内置函数之前检查导入绑定和模块本地函数。修复了导出自己的 `exec()` 函数的 `@stdlib/sqlite`。

**v1.9.1** - 上一版本特性：
- **`write()` 内置函数** - 不带尾部换行的打印（`write("hello"); write(" world");` 在一行输出）。包含 `fflush(stdout)` 用于即时输出。解释器和编译器完全对等。
- **单参数 `slice()`** - `arr.slice(n)` 和 `str.slice(n)` 现在默认结束位置为长度，匹配 JS/Python 行为。双参数形式不变。
- **rune 数组的 `join()`** - `"hello".chars().join("")` 现在正确产生 `"hello"` 而不是 `"[object][object]..."`。支持惯用字符串反转：`str.chars().reverse().join("")`。
- **HashMap 数字键强制转换** - 不同数值类型的键现在可以匹配（例如，`i32` 键可通过 `i64` 查找找到）。之前 `keys_equal()` 中的 `typeof()` 守卫拒绝了有效的跨类型匹配。
- **HemBench 改进** - 修复了任务定义（L1-M-02 舍入、L2-E-01 精度），停止向 L5/L6 基准测试任务泄露预期输出。
- **完整的 `ptr_read_*` 内置函数** - 添加了 `ptr_read_i8`、`ptr_read_i16`、`ptr_read_i64`、`ptr_read_u8`、`ptr_read_u16`、`ptr_read_u32`、`ptr_read_u64`、`ptr_read_f32`、`ptr_read_f64`、`ptr_read_ptr` 以补充现有的 `ptr_write_*` 函数。修复了 `ptr_read_i32` 为直接解引用（之前是双重解引用）。解释器和编译器完全对等。
- **macOS FFI 库加载** - `dlopen` 现在在 macOS 上搜索 `/usr/local/lib` 和 `/opt/homebrew/lib` 作为回退路径，修复了用户安装的共享库（例如 libusearch_c）的库未找到错误。
- **`@stdlib/vector` USearch v2 修复** - `create_index()` 现在在初始化后调用 `usearch_reserve()`，修复了 USearch v2.24+ 中需要在添加向量之前预分配的段错误。

**v1.9.0** - 上一版本特性：
- **WASM 解释器发布制品** - GitHub 发布中包含预构建的 WASM 解释器，用于浏览器/Node.js 使用
- **编译器内联修复** - 修复了函数内联期间嵌套调用参数损坏和循环计数器的拆箱冲突（修复 hemloco 编译）
- **指针减法** - 编译器类型检查器现在允许 `ptr - integer` 用于指针运算
- **可捕获的 `open()` 异常** - `open()` 现在通过 `hml_throw()` 抛出而不是 `exit(1)`，启用 try/catch 错误处理
- **多参数 print/eprint 修复** - 修复了带多个参数的 `print()` 和 `eprint()` 的编译器代码生成（例如 `print("x:", x, y)`）
- **SSO 字符串修复** - 修复了使用小字符串优化增长字符串时 `hml_string_append_inplace` 中的段错误
- **`@stdlib/termios` 模块** - 跨平台原始终端输入（Linux/macOS）：
  - `enable_raw_mode()` / `disable_raw_mode()` 用于即时按键
  - `read_key()` / `read_key_timeout(ms)` 用于单次按键读取
  - 箭头键、功能键、控制键检测
  - `is_terminal()` 检查 stdin 是否为 TTY
  - 文档位于 `stdlib/docs/termios.md`
- **内存泄漏预防** - 全面修复确保运行时无泄漏：
  - 异常安全的表达式求值（数组、对象、函数调用）
  - join() 时任务结果的正确 retain/release
  - 关闭时的 channel 排空（释放缓冲值）
  - 空值合并常量折叠的优化器清理
  - 泄漏回归测试套件（`make leak-regression`）
  - 内存所有权文档（`docs/advanced/memory-ownership.md`）
- **模式匹配**（`match` 表达式）- 强大的解构和控制流：
  - 字面量、通配符和变量绑定模式
  - OR 模式（`1 | 2 | 3`）
  - 守卫表达式（`n if n > 0`）
  - 对象解构（`{ x, y }`）
  - 带剩余部分的数组解构（`[first, ...rest]`）
  - 类型模式（`n: i32`）
  - 解释器和编译器完全对等
- **编译器辅助注解** - 11 个用于 GCC/Clang 控制的优化注解：
  - `@inline`、`@noinline` - 函数内联控制
  - `@hot`、`@cold` - 分支预测提示
  - `@pure`、`@const` - 副作用注解
  - `@flatten` - 内联函数内的所有调用
  - `@optimize(level)` - 每函数优化级别（"0"、"1"、"2"、"3"、"s"、"fast"）
  - `@warn_unused` - 忽略返回值时警告
  - `@section(name)` - 自定义 ELF 节放置（例如 `@section(".text.hot")`）
- **表达式体函数**（`fn double(x): i32 => x * 2;`）- 简洁的单表达式函数语法
- **单行语句** - 无花括号的 `if`、`while`、`for` 语法（例如 `if (x > 0) print(x);`）
- **类型别名**（`type Name = Type;`）- 复杂类型的命名快捷方式
- **函数类型注解**（`fn(i32): i32`）- 一等函数类型
- **Const 参数**（`fn(const x: array)`）- 参数的深度不可变性
- **Ref 参数**（`fn(ref x: i32)`）- 按引用传递用于直接修改调用者
- **define 中的方法签名**（`fn method(): Type`）- 类似接口的契约（逗号分隔）
- 方法签名中的 **Self 类型** - 指向定义类型
- **loop 关键字**（`loop { }`）- 更清晰的无限循环，替代 `while (true)`
- **循环标签**（`outer: while`）- 嵌套循环的定向 break/continue
- **对象简写**（`{ name }`）- ES6 风格简写属性语法
- **对象展开**（`{ ...obj }`）- 复制和合并对象字段
- **复合鸭子类型**（`A & B & C`）- 结构类型的交叉类型
- 函数调用的**命名参数**（`foo(name: "value", age: 30)`）
- **空值合并运算符**（`??`、`??=`、`?.`）用于安全的空值处理
- **八进制字面量**（`0o777`、`0O123`）
- **数字分隔符**（`1_000_000`、`0xFF_FF`、`0b1111_0000`）
- **块注释**（`/* ... */`）
- 字符串/rune 中的**十六进制转义序列**（`\x41` = 'A'）
- 字符串中的 **Unicode 转义序列**（`\u{1F600}` = 😀）
- **无前导零的浮点字面量**（`.5`、`.123`、`.5e2`）
- hemlockc 中的**编译时类型检查**（默认启用）
- **LSP 集成**，带实时诊断的类型检查
- **复合赋值运算符**（`+=`、`-=`、`*=`、`/=`、`%=`、`&=`、`|=`、`^=`、`<<=`、`>>=`）
- **自增/自减运算符**（`++x`、`x++`、`--x`、`x--`）
- **类型精度修复**：i64/u64 + f32 → f64 以保持精度
- 带拆箱优化提示的统一类型系统
- 完整类型系统（i8-i64、u8-u64、f32/f64、bool、string、rune、ptr、buffer、array、object、enum、file、task、channel）
- 带 19 个方法的 UTF-8 字符串
- 带 23 个方法的数组，包括 map/filter/reduce/every/some/indexOf/sort/fill
- 带 `talloc()` 和 `sizeof()` 的手动内存管理
- 带真正 pthread 并行的 async/await
- 用于无锁并发编程的原子操作
- 42 个 stdlib 模块（+ arena、assert、semver、toml、retry、iter、random、shell、termios、vector）
- C 互操作的 FFI，带 `export extern fn` 用于可重用库包装
- 编译器中的 FFI 结构支持（按值传递 C 结构）
- FFI 指针辅助函数（`ptr_null`、`ptr_read_*`、`ptr_write_*`）
- defer、try/catch/finally/throw、panic
- 文件 I/O、信号处理、命令执行
- [hpm](https://github.com/hemlang/hpm) 包管理器，带基于 GitHub 的注册表
- 编译器后端（C 代码生成），100% 解释器对等
- LSP 服务器，带跳转到定义和查找引用
- AST 优化遍历和 O(1) 查找的变量解析
- apply() 内置函数用于动态函数调用
- 无缓冲 channel 和多参数支持
- 159 个对等测试（100% 通过率）

---

## 理念

> 我们提供安全的工具（`buffer`、类型注解、边界检查），但不强制你使用它们（`ptr`、手动内存、非安全操作）。

**如果你不确定某个特性是否适合 Hemlock，请问自己："这是给程序员更多显式控制，还是隐藏了什么？"**

如果是隐藏，它可能不属于 Hemlock。
