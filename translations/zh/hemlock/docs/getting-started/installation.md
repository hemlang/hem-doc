# 安装指南

本指南将帮助您在系统上构建和安装 Hemlock。

## 快速安装（推荐）

安装 Hemlock 最简单的方法是使用一行安装脚本：

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

这将为您的平台（Linux 或 macOS，x86_64 或 arm64）下载并安装最新的预编译二进制文件。

### 安装选项

```bash
# 安装到自定义前缀（默认：~/.local）
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# 安装特定版本
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# 安装并自动更新 shell PATH
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

安装后，验证是否正常工作：

```bash
hemlock --version
```

---

## 从源代码构建

如果您更喜欢从源代码构建，或者预编译的二进制文件不适用于您的系统，请按照以下说明操作。

## 前置条件

### 必需的依赖项

Hemlock 构建需要以下依赖项：

- **C 编译器**：GCC 或 Clang（C11 标准）
- **Make**：GNU Make
- **libffi**：外部函数接口库（用于 FFI 支持）
- **OpenSSL**：加密库（用于哈希函数：md5、sha1、sha256）
- **libwebsockets**：WebSocket 和 HTTP 客户端/服务器支持
- **zlib**：压缩库

### 安装依赖项

**macOS：**
```bash
# 如果尚未安装，请先安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Xcode 命令行工具
xcode-select --install

# 通过 Homebrew 安装依赖项
brew install libffi openssl@3 libwebsockets
```

**macOS 用户注意**：Makefile 会自动检测 Homebrew 安装并设置正确的 include/library 路径。Hemlock 支持 Intel（x86_64）和 Apple Silicon（arm64）架构。

**Ubuntu/Debian：**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL：**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux：**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## 从源代码构建

### 1. 克隆仓库

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. 构建 Hemlock

```bash
make
```

这将编译 Hemlock 解释器并将可执行文件放在当前目录中。

### 3. 验证安装

```bash
./hemlock --version
```

您应该看到 Hemlock 版本信息。

### 4. 测试构建

运行测试套件以确保一切正常工作：

```bash
make test
```

所有测试都应该通过。如果您看到任何失败，请将其作为问题报告。

## 系统级安装（可选）

要在系统级安装 Hemlock（例如，安装到 `/usr/local/bin`）：

```bash
sudo make install
```

这允许您从任何位置运行 `hemlock` 而无需指定完整路径。

## 运行 Hemlock

### 交互式 REPL

启动读取-求值-打印循环（REPL）：

```bash
./hemlock
```

您将看到一个提示符，可以在其中输入 Hemlock 代码：

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

使用 `Ctrl+D` 或 `Ctrl+C` 退出 REPL。

### 运行程序

执行 Hemlock 脚本：

```bash
./hemlock program.hml
```

带有命令行参数：

```bash
./hemlock program.hml arg1 arg2 "带空格的参数"
```

## 目录结构

构建后，您的 Hemlock 目录将如下所示：

```
hemlock/
├── hemlock           # 编译的解释器可执行文件
├── src/              # 源代码
├── include/          # 头文件
├── tests/            # 测试套件
├── examples/         # 示例程序
├── docs/             # 文档
├── stdlib/           # 标准库
├── Makefile          # 构建配置
└── README.md         # 项目说明
```

## 构建选项

### 调试构建

使用调试符号和无优化进行构建：

```bash
make debug
```

### 清理构建

删除所有编译的文件：

```bash
make clean
```

从头开始重新构建：

```bash
make clean && make
```

## 故障排除

### macOS：找不到库错误

如果您收到关于缺少库的错误（`-lcrypto`、`-lffi` 等）：

1. 确保已安装 Homebrew 依赖项：
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. 验证 Homebrew 路径：
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Makefile 应该会自动检测这些路径。如果没有，请检查 `brew` 是否在您的 PATH 中：
   ```bash
   which brew
   ```

### macOS：BSD 类型错误（`u_int`、`u_char` 未找到）

如果您看到关于未知类型名称（如 `u_int` 或 `u_char`）的错误：

1. 这在 v1.0.0+ 中已通过使用 `_DARWIN_C_SOURCE` 而不是 `_POSIX_C_SOURCE` 修复
2. 确保您拥有最新版本的代码
3. 清理并重新构建：
   ```bash
   make clean && make
   ```

### Linux：找不到 libffi

如果您收到关于缺少 `ffi.h` 或 `-lffi` 的错误：

1. 确保已安装 `libffi-dev`（请参阅上面的依赖项）
2. 检查 `pkg-config` 是否能找到它：
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. 如果未找到，您可能需要设置 `PKG_CONFIG_PATH`：
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### 编译错误

如果遇到编译错误：

1. 确保您有兼容 C11 的编译器
2. 在 macOS 上，尝试使用 Clang（默认）：
   ```bash
   make CC=clang
   ```
3. 在 Linux 上，尝试使用 GCC：
   ```bash
   make CC=gcc
   ```
4. 检查是否已安装所有依赖项
5. 尝试从头开始重新构建：
   ```bash
   make clean && make
   ```

### 测试失败

如果测试失败：

1. 检查您是否拥有最新版本的代码
2. 尝试从头开始重新构建：
   ```bash
   make clean && make test
   ```
3. 在 macOS 上，确保您拥有最新的 Xcode 命令行工具：
   ```bash
   xcode-select --install
   ```
4. 在 GitHub 上报告问题，包括：
   - 您的平台（macOS 版本 / Linux 发行版）
   - 架构（x86_64 / arm64）
   - 测试输出
   - `make -v` 和 `gcc --version`（或 `clang --version`）的输出

## 下一步

- [快速入门指南](quick-start.md) - 编写您的第一个 Hemlock 程序
- [教程](tutorial.md) - 逐步学习 Hemlock
- [语言指南](../language-guide/syntax.md) - 探索 Hemlock 特性
