# 快速入门

几分钟内开始使用 Hemlock！

## 您的第一个程序

创建一个名为 `hello.hml` 的文件：

```hemlock
print("Hello, Hemlock!");
```

使用解释器运行：

```bash
./hemlock hello.hml
```

或编译为原生可执行文件：

```bash
./hemlockc hello.hml -o hello
./hello
```

输出：
```
Hello, Hemlock!
```

### 解释器 vs 编译器

Hemlock 提供两种运行程序的方式：

| 工具 | 用例 | 类型检查 |
|------|------|----------|
| `hemlock` | 快速脚本、REPL、开发 | 仅运行时 |
| `hemlockc` | 生产二进制文件、更好的性能 | 编译时（默认）|

编译器（`hemlockc`）在生成可执行文件之前对代码进行类型检查，可以提前捕获错误。

## 基本语法

### 变量

```hemlock
// 使用 'let' 声明变量
let x = 42;
let name = "Alice";
let pi = 3.14159;

// 类型注解是可选的
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**重要**：分号在 Hemlock 中是**必需的**！

### 类型

Hemlock 拥有丰富的类型系统：

```hemlock
// 整数
let small: i8 = 127;          // 8位有符号
let byte: u8 = 255;           // 8位无符号
let num: i32 = 2147483647;    // 32位有符号（默认）
let big: i64 = 9223372036854775807;  // 64位有符号

// 浮点数
let f: f32 = 3.14;            // 32位浮点
let d: f64 = 2.71828;         // 64位浮点（默认）

// 字符串和字符
let text: string = "Hello";   // UTF-8 字符串
let emoji: rune = '🚀';       // Unicode 码点

// 布尔值和空值
let flag: bool = true;
let empty = null;
```

### 控制流

```hemlock
// if 语句
if (x > 0) {
    print("正数");
} else if (x < 0) {
    print("负数");
} else {
    print("零");
}

// while 循环
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// for 循环
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### 函数

```hemlock
// 命名函数
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// 匿名函数
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## 字符串操作

Hemlock 中的字符串是**可变的**和 **UTF-8** 编码的：

```hemlock
let s = "hello";
s[0] = 'H';              // 现在是 "Hello"
print(s);

// 字符串方法
let upper = s.to_upper();     // "HELLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "ell"

// 连接
let greeting = "Hello" + ", " + "World!";
print(greeting);  // "Hello, World!"
```

## 数组

支持混合类型的动态数组：

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// 数组方法
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// 允许混合类型
let mixed = [1, "two", true, null];
```

## 对象

JavaScript 风格的对象：

```hemlock
// 对象字面量
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // 修改字段

// 使用 'self' 的方法
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## 内存管理

Hemlock 使用**手动内存管理**：

```hemlock
// 安全缓冲区（推荐）
let buf = buffer(64);   // 分配 64 字节
buf[0] = 65;            // 将第一个字节设置为 'A'
print(buf[0]);          // 65
free(buf);              // 释放内存

// 原始指针（高级）
let ptr = alloc(100);
memset(ptr, 0, 100);    // 用零填充
free(ptr);
```

**重要**：您必须 `free()` 您 `alloc()` 的内存！

## 错误处理

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
} finally {
    print("完成");
}
```

## 命令行参数

通过 `args` 数组访问程序参数：

```hemlock
// script.hml
print("脚本：", args[0]);
print(`参数数量：${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  参数 ${i}：${args[i]}`);
    i = i + 1;
}
```

运行：
```bash
./hemlock script.hml hello world
```

输出：
```
脚本：script.hml
参数数量：2
  参数 1：hello
  参数 2：world
```

## 文件 I/O

```hemlock
// 写入文件
let f = open("data.txt", "w");
f.write("Hello, File!");
f.close();

// 读取文件
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Hello, File!"
f2.close();
```

## 接下来学什么？

现在您已经了解了基础知识，可以探索更多内容：

- [教程](tutorial.md) - 全面的分步指南
- [语言指南](../language-guide/syntax.md) - 深入了解所有特性
- [示例](../../examples/) - 真实世界的示例程序
- [API 参考](../reference/builtins.md) - 完整的 API 文档

## 常见陷阱

### 忘记分号

```hemlock
// ❌ 错误：缺少分号
let x = 42
let y = 10

// ✅ 正确
let x = 42;
let y = 10;
```

### 忘记释放内存

```hemlock
// ❌ 内存泄漏
let buf = buffer(100);
// ... 使用 buf ...
// 忘记调用 free(buf)！

// ✅ 正确
let buf = buffer(100);
// ... 使用 buf ...
free(buf);
```

### 花括号是必需的

```hemlock
// ❌ 错误：缺少花括号
if (x > 0)
    print("正数");

// ✅ 正确
if (x > 0) {
    print("正数");
}
```

## 获取帮助

- 阅读[完整文档](../README.md)
- 查看[示例目录](../../examples/)
- 查看[测试文件](../../tests/)了解使用模式
- 在 GitHub 上报告问题
