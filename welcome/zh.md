# 欢迎使用 Hemlock

> "一门小巧的非安全语言，用于安全地编写不安全的东西。"

**Hemlock** 是一门系统级脚本语言，将 C 语言的强大功能与现代脚本的便捷性相结合。它具有手动内存管理、显式控制以及内置的结构化异步并发。

## 什么是 Hemlock？

Hemlock 专为以下程序员设计：

- **显式控制** 内存和执行流程
- **类 C 语法** 配合现代便捷特性
- **无隐藏行为** 或魔法
- **真正的并行异步**，基于 pthread 的并发

Hemlock 不是一门带有垃圾回收的内存安全语言。相反，它为您提供安全工具（`buffer`、类型注解、边界检查），但不强制您使用它们（`ptr`、手动内存管理、不安全操作）。

## 快速示例

```hemlock
// 你好，Hemlock！
fn greet(name: string): string {
    return `你好，${name}！`;
}

let message = greet("世界");
print(message);

// 手动内存管理
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## 功能概览

| 功能 | 描述 |
|------|------|
| **类型系统** | i8-i64、u8-u64、f32/f64、bool、string、rune、ptr、buffer、array、object |
| **内存** | 使用 `alloc()`、`buffer()`、`free()` 进行手动管理 |
| **异步** | 内置 `async`/`await`，支持真正的 pthread 并行 |
| **FFI** | 直接从共享库调用 C 函数 |
| **标准库** | 40 个模块，包括 crypto、http、sqlite、json 等 |

## 快速入门

准备好开始了吗？以下是开始步骤：

1. **[安装](#getting-started-installation)** - 下载并设置 Hemlock
2. **[快速开始](#getting-started-quick-start)** - 几分钟内编写您的第一个程序
3. **[教程](#getting-started-tutorial)** - 逐步学习 Hemlock

## 文档章节

- **快速入门** - 安装、快速开始指南和教程
- **语言指南** - 深入了解语法、类型、函数等
- **高级主题** - 异步编程、FFI、信号和原子操作
- **API 参考** - 内置函数和标准库的完整参考
- **设计与理念** - 理解 Hemlock 为何如此设计

## 包管理器

Hemlock 自带 **hpm** 包管理器，用于管理依赖：

```bash
hpm init my-project
hpm add some-package
hpm run
```

请参阅 hpm 文档章节了解更多详情。

---

使用左侧导航浏览文档，或使用搜索栏查找特定主题。
