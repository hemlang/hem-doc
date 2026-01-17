# Hemlock 模块系统

本文档描述了为 Hemlock 实现的 ES6 风格 import/export 模块系统。

## 概述

Hemlock 支持基于文件的模块系统，使用 ES6 风格的 import/export 语法。模块具有以下特点：
- **单例**：每个模块只加载一次并被缓存
- **基于文件**：模块对应磁盘上的 .hml 文件
- **显式导入**：依赖通过 import 语句声明
- **拓扑执行**：依赖在依赖者之前执行

有关包管理和第三方依赖，请参阅 [hpm (Hemlock 包管理器)](https://github.com/hemlang/hpm)。

## 语法

### Export 语句

**内联命名导出：**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**导出列表：**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**导出 Extern（FFI 函数）：**
```hemlock
import "libc.so.6";

// 导出 FFI 函数供其他模块使用
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

有关导出 FFI 函数的更多详细信息，请参阅 [FFI 文档](../advanced/ffi.md#exporting-ffi-functions)。

**导出 Define（结构体类型）：**
```hemlock
// 导出结构体类型定义
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**重要说明：** 导出的结构体类型在模块加载时全局注册。当你从模块导入任何内容时，它们会自动可用 - 你不需要（也不能）通过名称显式导入它们：

```hemlock
// 正确 - 任何导入后结构体类型自动可用
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // 可以工作！

// 错误 - 不能显式导入结构体类型
import { Vector2 } from "./my_module.hml";  // 错误：未定义变量 'Vector2'
```

有关导出结构体类型的更多详细信息，请参阅 [FFI 文档](../advanced/ffi.md#exporting-struct-types)。

**重新导出：**
```hemlock
// 从另一个模块重新导出
export { add, subtract } from "./math.hml";
```

### Import 语句

**命名导入：**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**命名空间导入：**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**别名：**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## 模块解析

### 路径类型

**相对路径：**
```hemlock
import { foo } from "./module.hml";       // 同一目录
import { bar } from "../parent.hml";      // 父目录
import { baz } from "./sub/nested.hml";   // 子目录
```

**绝对路径：**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**扩展名处理：**
- `.hml` 扩展名可以省略 - 会自动添加
- `./math` 解析为 `./math.hml`

## 特性

### 循环依赖检测

模块系统检测循环依赖并报告错误：

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### 模块缓存

模块只加载一次并被缓存。多次导入同一模块返回相同的实例：

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // 同一实例！
print(count);  // 仍然是 1（共享状态）
```

### 导入不可变性

导入的绑定不能被重新赋值：

```hemlock
import { add } from "./math.hml";
add = fn() { };  // 错误：不能重新赋值导入的绑定
```

## 实现细节

### 架构

**文件：**
- `include/module.h` - 模块系统 API
- `src/module.c` - 模块加载、缓存和执行
- `src/parser.c` 中的解析器支持
- `src/interpreter/runtime.c` 中的运行时支持

**关键组件：**
1. **ModuleCache**：按绝对路径索引维护已加载的模块
2. **Module**：表示带有 AST 和导出的已加载模块
3. **路径解析**：将相对/绝对路径解析为规范路径
4. **拓扑执行**：按依赖顺序执行模块

### 模块加载过程

1. **解析阶段**：对模块文件进行词法分析和语法分析
2. **依赖解析**：递归加载导入的模块
3. **循环检测**：检查模块是否已在加载中
4. **缓存**：按绝对路径将模块存储在缓存中
5. **执行阶段**：按拓扑顺序执行（依赖优先）

### API

```c
// 高级 API
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// 低级 API
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## 测试

测试模块位于 `tests/modules/` 和 `tests/parity/modules/`：

- `math.hml` - 带导出的基本模块
- `test_import_named.hml` - 命名导入测试
- `test_import_namespace.hml` - 命名空间导入测试
- `test_import_alias.hml` - 导入别名测试
- `export_extern.hml` - 导出 extern FFI 函数测试（Linux）

## 包导入（hpm）

安装 [hpm](https://github.com/hemlang/hpm) 后，你可以从 GitHub 导入第三方包：

```hemlock
// 从包根目录导入（使用 package.json 中的 "main"）
import { app, router } from "hemlang/sprout";

// 从子路径导入
import { middleware } from "hemlang/sprout/middleware";

// 标准库（内置于 Hemlock）
import { HashMap } from "@stdlib/collections";
```

包安装到 `hem_modules/` 并使用 GitHub `owner/repo` 语法解析。

```bash
# 安装包
hpm install hemlang/sprout

# 带版本约束安装
hpm install hemlang/sprout@^1.0.0
```

有关完整详细信息，请参阅 [hpm 文档](https://github.com/hemlang/hpm)。

## 当前限制

1. **不支持动态导入**：`import()` 作为运行时函数不受支持
2. **不支持条件导出**：导出必须在顶层
3. **静态库路径**：FFI 库导入使用静态路径（特定于平台）

## 未来工作

- 使用 `import()` 函数的动态导入
- 条件导出
- 模块元数据（`import.meta`）
- Tree shaking 和死代码消除

## 示例

有关模块系统的工作示例，请参阅 `tests/modules/`。

示例模块结构：
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (barrel 模块)
└── utils/
    └── helpers.hml
```

示例用法：
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
