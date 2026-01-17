# Hemlock 教程

学习 Hemlock 的全面分步指南。

## 目录

1. [Hello World](#hello-world)
2. [变量和类型](#变量和类型)
3. [算术和运算](#算术和运算)
4. [控制流](#控制流)
5. [函数](#函数)
6. [字符串和字符](#字符串和字符)
7. [数组](#数组)
8. [对象](#对象)
9. [内存管理](#内存管理)
10. [错误处理](#错误处理)
11. [文件 I/O](#文件-io)
12. [综合示例](#综合示例)

## Hello World

让我们从传统的第一个程序开始：

```hemlock
print("Hello, World!");
```

将其保存为 `hello.hml` 并运行：

```bash
./hemlock hello.hml
```

**要点：**
- `print()` 是一个内置函数，输出到标准输出
- 字符串用双引号括起来
- 分号是**必需的**

## 变量和类型

### 声明变量

```hemlock
// 基本变量声明
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### 类型注解

虽然类型默认是推断的，但您可以显式指定：

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### 类型推断

Hemlock 根据值推断类型：

```hemlock
let small = 42;              // i32（适合 32 位）
let large = 5000000000;      // i64（对于 i32 太大）
let decimal = 3.14;          // f64（浮点数默认值）
let text = "hello";          // string
let flag = true;             // bool
```

### 类型检查

```hemlock
// 使用 typeof() 检查类型
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hello"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## 算术和运算

### 基本算术

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3（整数除法）
print(a == b);  // false
print(a > b);   // true
```

### 类型提升

混合类型时，Hemlock 会提升到更大/更精确的类型：

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result 是 f64（10.0 + 3.5 = 13.5）

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### 位运算

```hemlock
let a = 12;  // 二进制 1100
let b = 10;  // 二进制 1010

print(a & b);   // 8  (AND)
print(a | b);   // 14 (OR)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24（左移）
print(a >> 1);  // 6 （右移）
print(~a);      // -13 (NOT)
```

## 控制流

### If 语句

```hemlock
let x = 10;

if (x > 0) {
    print("正数");
} else if (x < 0) {
    print("负数");
} else {
    print("零");
}
```

**注意：** 花括号**始终是必需的**，即使是单个语句也是如此。

### While 循环

```hemlock
let count = 0;
while (count < 5) {
    print(`计数：${count}`);
    count = count + 1;
}
```

### For 循环

```hemlock
// C 风格的 for 循环
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// for-in 循环（数组）
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`项目：${item}`);
}
```

### Switch 语句

```hemlock
let day = 3;

switch (day) {
    case 1:
        print("星期一");
        break;
    case 2:
        print("星期二");
        break;
    case 3:
        print("星期三");
        break;
    default:
        print("其他日子");
        break;
}
```

### Break 和 Continue

```hemlock
// Break：提前退出循环
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// 输出：0, 1, 2, 3, 4

// Continue：跳到下一次迭代
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// 输出：0, 1, 3, 4
```

## 函数

### 命名函数

```hemlock
fn greet(name: string): string {
    return "你好，" + name + "！";
}

let message = greet("Alice");
print(message);  // "你好，Alice！"
```

### 匿名函数

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### 递归

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### 闭包

函数捕获其环境：

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

### 高阶函数

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## 字符串和字符

### 字符串基础

字符串是**可变的**和 **UTF-8** 编码的：

```hemlock
let s = "hello";
print(s.length);      // 5（字符数）
print(s.byte_length); // 5（字节数）

// 修改
s[0] = 'H';
print(s);  // "Hello"
```

### 字符串方法

```hemlock
let text = "  Hello, World!  ";

// 大小写转换
print(text.to_upper());  // "  HELLO, WORLD!  "
print(text.to_lower());  // "  hello, world!  "

// 去除空白
print(text.trim());      // "Hello, World!"

// 子字符串提取
let hello = text.substr(2, 5);  // "Hello"
let world = text.slice(9, 14);  // "World"

// 搜索
let pos = text.find("World");   // 9
let has = text.contains("o");   // true

// 分割
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// 替换
let s = "hello world".replace("world", "there");
print(s);  // "hello there"
```

### 字符（Unicode 码点）

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// 字符 + 字符串连接
let msg = '>' + " 重要";
print(msg);  // "> 重要"

// 字符和整数之间的转换
let code: i32 = ch;     // 65（ASCII 码）
let r: rune = 128640;   // U+1F680（🚀）
```

## 数组

### 数组基础

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// 修改元素
numbers[2] = 99;
print(numbers[2]);  // 99
```

### 数组方法

```hemlock
let arr = [10, 20, 30];

// 在末尾添加/删除
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40，arr 现在是 [10, 20, 30]

// 在开头添加/删除
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5，arr 现在是 [10, 20, 30]

// 在索引处插入/删除
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// 搜索
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// 切片
let slice = arr.slice(0, 2);  // [10, 15]

// 连接为字符串
let text = arr.join(", ");    // "10, 15, 30"
```

### 迭代

```hemlock
let items = ["苹果", "香蕉", "樱桃"];

// for-in 循环
for (let item in items) {
    print(item);
}

// 手动迭代
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## 对象

### 对象字面量

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// 添加/修改字段
person.email = "alice@example.com";
person.age = 31;
```

### 方法和 `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### 类型定义（鸭子类型）

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // 带默认值的可选字段
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // 鸭子类型验证结构

print(typeof(typed));   // "Person"
print(typed.active);    // true（应用默认值）
```

### JSON 序列化

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// 对象到 JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON 到对象
let restored = json.deserialize();
print(restored.name);  // "test"
```

## 内存管理

### 安全缓冲区（推荐）

```hemlock
// 分配缓冲区
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// 设置值（边界检查）
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// 访问值
print(buf[0]);  // 65

// 完成后必须释放
free(buf);
```

### 原始指针（高级）

```hemlock
// 分配原始内存
let ptr = alloc(100);

// 用零填充
memset(ptr, 0, 100);

// 复制数据
let src = alloc(50);
memcpy(ptr, src, 50);

// 释放两者
free(src);
free(ptr);
```

### 内存函数

```hemlock
// 重新分配
let p = alloc(64);
p = realloc(p, 128);  // 调整为 128 字节
free(p);

// 类型化分配（未来功能）
// let arr = talloc(i32, 100);  // 100 个 i32 的数组
```

## 错误处理

### Try/Catch

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "除零错误";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("错误：" + e);
}
// 输出：错误：除零错误
```

### Finally 块

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("错误：" + e);
} finally {
    // 始终运行
    if (file != null) {
        file.close();
    }
}
```

### 抛出对象

```hemlock
try {
    throw { code: 404, message: "未找到" };
} catch (e) {
    print(`错误 ${e.code}：${e.message}`);
}
// 输出：错误 404：未找到
```

### Panic（不可恢复的错误）

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x 必须是非负数");
    }
    return x * 2;
}

validate(-5);  // 程序退出并显示：panic: x 必须是非负数
```

## 文件 I/O

### 读取文件

```hemlock
// 读取整个文件
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// 读取指定字节数
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // 读取 100 字节
f2.close();
```

### 写入文件

```hemlock
// 写入文本
let f = open("output.txt", "w");
f.write("Hello, File!\n");
f.write("第二行\n");
f.close();

// 追加到文件
let f2 = open("output.txt", "a");
f2.write("追加的行\n");
f2.close();
```

### 二进制 I/O

```hemlock
// 写入二进制数据
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// 读取二进制数据
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### 文件属性

```hemlock
let f = open("/path/to/file.txt", "r");

print(f.path);    // "/path/to/file.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## 综合示例

让我们构建一个简单的单词计数程序：

```hemlock
// wordcount.hml - 计算文件中的单词数

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // 按空格分割并计数
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("读取文件错误：" + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// 主程序
if (args.length < 2) {
    print("用法：" + args[0] + " <文件名>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`单词数：${words}`);
    }
}
```

运行：
```bash
./hemlock wordcount.hml data.txt
```

## 下一步

恭喜！您已经学会了 Hemlock 的基础知识。接下来可以探索：

- [异步与并发](../advanced/async-concurrency.md) - 真正的多线程
- [FFI](../advanced/ffi.md) - 调用 C 函数
- [信号处理](../advanced/signals.md) - 进程信号
- [API 参考](../reference/builtins.md) - 完整的 API 文档
- [示例](../../examples/) - 更多真实世界的程序

## 练习题

尝试构建这些程序来练习：

1. **计算器**：实现一个简单的计算器，支持 +、-、*、/
2. **文件复制**：将一个文件复制到另一个文件
3. **斐波那契**：生成斐波那契数列
4. **JSON 解析器**：读取和解析 JSON 文件
5. **文本处理器**：在文件中查找和替换文本

祝您使用 Hemlock 编程愉快！
