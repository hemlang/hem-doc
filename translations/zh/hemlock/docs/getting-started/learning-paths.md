# 学习路径

不同的目标需要不同的知识。选择与您想要构建的内容相匹配的路径。

---

## 路径 1：快速脚本和自动化

**目标：** 编写脚本来自动化任务、处理文件并完成工作。

**达到生产力的时间：** 很快 - 您可以立即开始编写有用的脚本。

### 您将学到的内容

1. **[快速入门](quick-start.md)** - 您的第一个程序，基本语法
2. **[字符串](../language-guide/strings.md)** - 文本处理、分割、搜索
3. **[数组](../language-guide/arrays.md)** - 列表、过滤、转换数据
4. **[文件 I/O](../advanced/file-io.md)** - 读写文件
5. **[命令行参数](../advanced/command-line-args.md)** - 获取用户输入

### 暂时跳过

- 内存管理（脚本自动处理）
- 异步/并发（对于简单脚本来说太复杂）
- FFI（只有在需要 C 互操作时才需要）

### 示例项目：文件重命名器

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// 将所有 .txt 文件重命名为 .md
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`已重命名：${file} -> ${new_name}`);
    }
}
```

---

## 路径 2：数据处理与分析

**目标：** 解析数据、转换数据、生成报告。

**达到生产力的时间：** 很快 - Hemlock 的字符串和数组方法使这变得很容易。

### 您将学到的内容

1. **[快速入门](quick-start.md)** - 基础知识
2. **[字符串](../language-guide/strings.md)** - 解析、分割、格式化
3. **[数组](../language-guide/arrays.md)** - map、filter、reduce 用于数据转换
4. **[对象](../language-guide/objects.md)** - 结构化数据
5. **标准库：**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON 解析
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - CSV 文件
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - 文件操作

### 示例项目：CSV 分析器

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// 计算总销售额
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`总销售额：$${total}`);

// 找出最高销售额
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`最高销售：${top.product} - $${top.amount}`);
```

---

## 路径 3：Web 和网络编程

**目标：** 构建 HTTP 客户端、使用 API、创建服务器。

**达到生产力的时间：** 中等 - 需要理解异步基础知识。

### 您将学到的内容

1. **[快速入门](quick-start.md)** - 基础知识
2. **[函数](../language-guide/functions.md)** - 回调和闭包
3. **[错误处理](../language-guide/error-handling.md)** - 网络错误的 try/catch
4. **[异步与并发](../advanced/async-concurrency.md)** - spawn、await、channels
5. **标准库：**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - HTTP 请求
   - **[@stdlib/json](../../stdlib/docs/json.md)** - API 的 JSON
   - **[@stdlib/net](../../stdlib/docs/net.md)** - TCP/UDP 套接字
   - **[@stdlib/url](../../stdlib/docs/url.md)** - URL 解析

### 示例项目：API 客户端

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// GET 请求
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}：${user.email}`);
}

// POST 请求
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`创建的用户 ID：${parse(result.body).id}`);
```

---

## 路径 4：系统编程

**目标：** 编写底层代码、操作内存、与 C 库交互。

**达到生产力的时间：** 较长 - 需要理解内存管理。

### 您将学到的内容

1. **[快速入门](quick-start.md)** - 基础知识
2. **[类型](../language-guide/types.md)** - 理解 i32、u8、ptr 等
3. **[内存管理](../language-guide/memory.md)** - alloc、free、缓冲区
4. **[FFI](../advanced/ffi.md)** - 调用 C 函数
5. **[信号](../advanced/signals.md)** - 信号处理

### 关键概念

**内存安全清单：**
- [ ] 每个 `alloc()` 都有对应的 `free()`
- [ ] 除非需要原始 `ptr`，否则使用 `buffer()`
- [ ] 释放后将指针设置为 `null`
- [ ] 使用 `try/finally` 保证清理

**FFI 类型映射：**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long`（64位）|
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### 示例项目：自定义内存池

```hemlock
// 简单的 bump allocator
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "内存池已耗尽";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// 使用它
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // 重用所有内存
pool_destroy();  // 清理
```

---

## 路径 5：并行与并发程序

**目标：** 在多个 CPU 核心上运行代码，构建响应式应用程序。

**达到生产力的时间：** 中等 - 异步语法很简单，但并行思维需要练习。

### 您将学到的内容

1. **[快速入门](quick-start.md)** - 基础知识
2. **[函数](../language-guide/functions.md)** - 闭包（对异步很重要）
3. **[异步与并发](../advanced/async-concurrency.md)** - 完整深入讲解
4. **[原子操作](../advanced/atomics.md)** - 无锁编程

### 关键概念

**Hemlock 的异步模型：**
- `async fn` - 定义可以在另一个线程上运行的函数
- `spawn(fn, args...)` - 开始运行它，返回任务句柄
- `join(task)` 或 `await task` - 等待它完成，获取结果
- `channel(size)` - 创建用于在任务之间发送数据的队列

**重要：** 任务接收值的*副本*。如果您传递一个指针，您需要负责确保内存在任务完成之前保持有效。

### 示例项目：并行文件处理器

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// 并行处理所有文件
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// 收集结果
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}：${count} 行`);
    total_lines = total_lines + count;
}

print(`总计：${total_lines} 行`);
```

---

## 任何路径都应该首先学习的内容

无论您的目标是什么，从这些基础知识开始：

### 第 1 周：核心基础
1. **[快速入门](quick-start.md)** - 编写并运行您的第一个程序
2. **[语法](../language-guide/syntax.md)** - 变量、运算符、控制流
3. **[函数](../language-guide/functions.md)** - 定义和调用函数

### 第 2 周：数据处理
4. **[字符串](../language-guide/strings.md)** - 文本操作
5. **[数组](../language-guide/arrays.md)** - 集合和迭代
6. **[对象](../language-guide/objects.md)** - 结构化数据

### 第 3 周：健壮性
7. **[错误处理](../language-guide/error-handling.md)** - try/catch/throw
8. **[模块](../language-guide/modules.md)** - 导入/导出，使用标准库

### 然后：选择您上面的路径

---

## 速查表：来自其他语言

### 来自 Python

| Python | Hemlock | 注意事项 |
|--------|---------|----------|
| `x = 42` | `let x = 42;` | 需要分号 |
| `def fn():` | `fn name() { }` | 需要花括号 |
| `if x:` | `if (x) { }` | 需要括号和花括号 |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | C 风格的 for 循环 |
| `for item in list:` | `for (item in array) { }` | for-in 相同 |
| `list.append(x)` | `array.push(x);` | 方法名不同 |
| `len(s)` | `s.length` 或 `len(s)` | 两者都可以 |
| 自动内存管理 | `ptr` 需要手动管理 | 大多数类型自动清理 |

### 来自 JavaScript

| JavaScript | Hemlock | 注意事项 |
|------------|---------|----------|
| `let x = 42` | `let x = 42;` | 相同（需要分号）|
| `const x = 42` | `let x = 42;` | 没有 const 关键字 |
| `function fn()` | `fn name() { }` | 不同的关键字 |
| `() => x` | `fn() { return x; }` | 没有箭头函数 |
| `async/await` | `async/await` | 相同语法 |
| `Promise` | `spawn/join` | 不同的模型 |
| 自动 GC | `ptr` 需要手动管理 | 大多数类型自动清理 |

### 来自 C/C++

| C | Hemlock | 注意事项 |
|---|---------|----------|
| `int x = 42;` | `let x: i32 = 42;` | 类型在冒号后 |
| `malloc(n)` | `alloc(n)` | 相同概念 |
| `free(p)` | `free(p)` | 相同 |
| `char* s = "hi"` | `let s = "hi";` | 字符串是托管的 |
| `#include` | `import { } from` | 模块导入 |
| 全部手动管理 | 大多数类型自动 | 只有 `ptr` 需要手动 |

---

## 获取帮助

- **[术语表](../glossary.md)** - 编程术语定义
- **[示例](../../examples/)** - 完整的工作程序
- **[测试](../../tests/)** - 查看功能的使用方式
- **GitHub Issues** - 提问、报告错误

---

## 难度级别

在整个文档中，您会看到这些标记：

| 标记 | 含义 |
|------|------|
| **初学者** | 不需要先前的编程经验 |
| **中级** | 假设具有基本的编程知识 |
| **高级** | 需要理解系统概念 |

如果标记为"初学者"的内容让您困惑，请查看[术语表](../glossary.md)了解术语定义。
