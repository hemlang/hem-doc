# Hemlock 文档

欢迎来到 Hemlock 编程语言文档！

> 一门小巧、非安全的语言，用于安全地编写非安全代码。

## 目录

### 入门指南
- [安装](getting-started/installation.md) - 构建和安装 Hemlock
- [快速入门](getting-started/quick-start.md) - 你的第一个 Hemlock 程序
- [教程](getting-started/tutorial.md) - Hemlock 基础的逐步指南
- [学习路径](getting-started/learning-paths.md) - 根据你的目标选择学习路线

### 编程新手？
- [术语表](glossary.md) - 编程术语的通俗解释

### 语言指南
- [语法概述](language-guide/syntax.md) - 基本语法和结构
- [类型系统](language-guide/types.md) - 原始类型、类型推断和转换
- [内存管理](language-guide/memory.md) - 指针、缓冲区和手动内存
- [字符串](language-guide/strings.md) - UTF-8 字符串和操作
- [Rune](language-guide/runes.md) - Unicode 码点和字符处理
- [控制流](language-guide/control-flow.md) - if/else、循环、switch 和运算符
- [函数](language-guide/functions.md) - 函数、闭包和递归
- [对象](language-guide/objects.md) - 对象字面量、方法和鸭子类型
- [数组](language-guide/arrays.md) - 动态数组和操作
- [错误处理](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [模块](language-guide/modules.md) - 导入/导出系统和包导入

### 高级主题
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - 通过 Emscripten 在浏览器中运行 Hemlock
- [异步与并发](advanced/async-concurrency.md) - 使用 async/await 的真正多线程
- [打包与封装](advanced/bundling-packaging.md) - 创建 bundle 和独立可执行文件
- [外部函数接口](advanced/ffi.md) - 从共享库调用 C 函数
- [文件 I/O](advanced/file-io.md) - 文件操作和资源管理
- [信号处理](advanced/signals.md) - POSIX 信号处理
- [命令行参数](advanced/command-line-args.md) - 访问程序参数
- [命令执行](advanced/command-execution.md) - 执行 shell 命令
- [性能分析](advanced/profiling.md) - CPU 时间、内存跟踪和泄漏检测

### API 参考
- [类型系统参考](reference/type-system.md) - 完整类型参考
- [运算符参考](reference/operators.md) - 所有运算符和优先级
- [内置函数](reference/builtins.md) - 全局函数和常量
- [字符串 API](reference/string-api.md) - 字符串方法和属性
- [数组 API](reference/array-api.md) - 数组方法和属性
- [内存 API](reference/memory-api.md) - 内存分配和操作
- [文件 API](reference/file-api.md) - 文件 I/O 方法
- [并发 API](reference/concurrency-api.md) - 任务和通道

### 设计与理念
- [设计理念](design/philosophy.md) - 核心原则和目标
- [实现细节](design/implementation.md) - Hemlock 的内部工作原理

### 贡献
- [贡献指南](contributing/guidelines.md) - 如何贡献
- [测试指南](contributing/testing.md) - 编写和运行测试

## 快速参考

### Hello World
```hemlock
print("Hello, World!");
```

### 基本类型
```hemlock
let x: i32 = 42;           // 32-bit signed integer
let y: u8 = 255;           // 8-bit unsigned integer
let pi: f64 = 3.14159;     // 64-bit float
let name: string = "Alice"; // UTF-8 string
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode codepoint
```

### 内存管理
```hemlock
// Safe buffer (recommended)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Raw pointer (for experts)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### 异步/并发
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## 理念

Hemlock **显式优于隐式**，始终如此：
- 分号是强制性的
- 手动内存管理（无 GC）
- 可选的类型注解，运行时检查
- 允许非安全操作（由你负责）

我们给你安全的工具（`buffer`、类型注解、边界检查），但不强制你使用它们（`ptr`、手动内存、非安全操作）。

## 获取帮助

- **源代码**：[GitHub 仓库](https://github.com/hemlang/hemlock)
- **包管理器**：[hpm](https://github.com/hemlang/hpm) - Hemlock 包管理器
- **问题反馈**：报告 bug 和功能请求
- **示例**：参见 `examples/` 目录
- **测试**：参见 `tests/` 目录了解使用示例

## 许可证

Hemlock 基于 MIT 许可证发布。
