# 打包与分发

Hemlock 提供内置工具，可将多文件项目打包成单个可分发文件并创建独立的可执行文件。

## 概述

| 命令 | 输出 | 用例 |
|------|------|------|
| `--bundle` | `.hmlc` 或 `.hmlb` | 分发字节码（需要 Hemlock 运行） |
| `--package` | 可执行文件 | 独立二进制文件（无依赖） |
| `--compile` | `.hmlc` | 编译单个文件（无导入解析） |

## 打包

打包器从入口点解析所有 `import` 语句，并将它们展平为单个文件。

### 基本用法

```bash
# 将 app.hml 及其所有导入打包成 app.hmlc
hemlock --bundle app.hml

# 指定输出路径
hemlock --bundle app.hml -o dist/app.hmlc

# 创建压缩包（.hmlb）- 更小的文件大小
hemlock --bundle app.hml --compress -o app.hmlb

# 详细输出（显示解析的模块）
hemlock --bundle app.hml --verbose
```

### 输出格式

**`.hmlc`（未压缩）**
- 序列化的 AST 格式
- 加载和执行速度快
- 默认输出格式

**`.hmlb`（压缩）**
- zlib 压缩的 `.hmlc`
- 文件大小更小（通常减少 50-70%）
- 由于解压缩，启动稍慢

### 运行打包文件

```bash
# 运行未压缩包
hemlock app.hmlc

# 运行压缩包
hemlock app.hmlb

# 传递参数
hemlock app.hmlc arg1 arg2
```

### 示例：多模块项目

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # 运行时所有依赖都已打包
```

### stdlib 导入

打包器自动解析 `@stdlib/` 导入：

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

打包时，stdlib 模块会包含在输出中。

## 封装

封装通过将打包的字节码嵌入 Hemlock 解释器副本来创建独立的可执行文件。

### 基本用法

```bash
# 从 app.hml 创建可执行文件
hemlock --package app.hml

# 指定输出名称
hemlock --package app.hml -o myapp

# 跳过压缩（启动更快，文件更大）
hemlock --package app.hml --no-compress

# 详细输出
hemlock --package app.hml --verbose
```

### 运行封装的可执行文件

```bash
# 封装的可执行文件直接运行
./myapp

# 参数传递给脚本
./myapp arg1 arg2
```

### 封装格式

封装的可执行文件使用 HMLP 格式：

```
[hemlock 二进制文件][HMLB/HMLC 载荷][payload_size:u64][HMLP 魔数:u32]
```

当封装的可执行文件运行时：
1. 检查文件末尾是否有嵌入的载荷
2. 如果找到，解压缩并执行载荷
3. 如果未找到，作为普通 Hemlock 解释器运行

### 压缩选项

| 标志 | 格式 | 启动 | 大小 |
|------|------|------|------|
| （默认） | HMLB | 正常 | 较小 |
| `--no-compress` | HMLC | 更快 | 较大 |

对于启动时间重要的 CLI 工具，使用 `--no-compress`。

## 检查包

使用 `--info` 检查打包或编译的文件：

```bash
hemlock --info app.hmlc
```

输出：
```
=== File Info: app.hmlc ===
Size: 12847 bytes
Format: HMLC (compiled AST)
Version: 1
Flags: 0x0001 [DEBUG]
Strings: 42
Statements: 156
```

```bash
hemlock --info app.hmlb
```

输出：
```
=== File Info: app.hmlb ===
Size: 5234 bytes
Format: HMLB (compressed bundle)
Version: 1
Uncompressed: 12847 bytes
Compressed: 5224 bytes
Ratio: 59.3% reduction
```

## 原生编译

要获得真正的原生可执行文件（无解释器），使用 Hemlock 编译器：

```bash
# 通过 C 编译为原生可执行文件
hemlockc app.hml -o app

# 保留生成的 C 代码
hemlockc app.hml -o app --keep-c

# 仅生成 C（不编译）
hemlockc app.hml -c -o app.c

# 优化级别
hemlockc app.hml -o app -O2
```

编译器生成 C 代码并调用 GCC 产生原生二进制文件。这需要：
- Hemlock 运行时库（`libhemlock_runtime`）
- C 编译器（默认 GCC）

### 编译器选项

| 选项 | 描述 |
|------|------|
| `-o <file>` | 输出可执行文件名 |
| `-c` | 仅生成 C 代码 |
| `--emit-c <file>` | 将 C 写入指定文件 |
| `-k, --keep-c` | 编译后保留生成的 C |
| `-O<level>` | 优化级别（0-3） |
| `--cc <path>` | 使用的 C 编译器 |
| `--runtime <path>` | 运行时库路径 |
| `-v, --verbose` | 详细输出 |

## 比较

| 方法 | 可移植性 | 启动 | 大小 | 依赖 |
|------|----------|------|------|------|
| `.hml` | 仅源码 | 解析时间 | 最小 | Hemlock |
| `.hmlc` | 仅 Hemlock | 快 | 小 | Hemlock |
| `.hmlb` | 仅 Hemlock | 快 | 更小 | Hemlock |
| `--package` | 独立 | 快 | 较大 | 无 |
| `hemlockc` | 原生 | 最快 | 不定 | 运行时库 |

## 最佳实践

1. **开发**：直接运行 `.hml` 文件以快速迭代
2. **分发（有 Hemlock）**：使用 `--compress` 打包以获得更小的文件
3. **分发（独立）**：封装以实现零依赖部署
4. **性能关键**：使用 `hemlockc` 进行原生编译

## 故障排除

### "Cannot find stdlib"

打包器在以下位置查找 stdlib：
1. `./stdlib`（相对于可执行文件）
2. `../stdlib`（相对于可执行文件）
3. `/usr/local/lib/hemlock/stdlib`

确保 Hemlock 已正确安装或从源目录运行。

### 循环依赖

```
Error: Circular dependency detected when loading 'path/to/module.hml'
```

重构你的导入以打破循环。考虑使用共享模块存放公共类型。

### 封装大小过大

- 使用默认压缩（不要使用 `--no-compress`）
- 封装大小包含完整解释器（基础约 500KB-1MB）
- 要获得最小大小，使用 `hemlockc` 进行原生编译
