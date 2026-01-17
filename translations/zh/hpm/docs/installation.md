# 安装

本指南介绍如何在你的系统上安装 hpm。

## 快速安装（推荐）

使用单个命令安装最新版本：

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

这会自动：
- 检测你的操作系统（Linux、macOS）
- 检测你的架构（x86_64、arm64）
- 下载相应的预编译二进制文件
- 安装到 `/usr/local/bin`（如需要会使用 sudo）

### 安装选项

```bash
# 安装到自定义位置（无需 sudo）
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# 安装特定版本
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# 组合选项
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### 支持的平台

| 平台 | 架构 | 状态 |
|----------|--------------|--------|
| Linux    | x86_64       | 支持 |
| macOS    | x86_64       | 支持 |
| macOS    | arm64 (M1/M2/M3) | 支持 |
| Linux    | arm64        | 从源码构建 |

## 从源码构建

如果你希望从源码构建，或需要预编译二进制文件未覆盖的平台，请按以下说明操作。

### 前提条件

hpm 需要先安装 [Hemlock](https://github.com/hemlang/hemlock)。请先按照 Hemlock 安装说明进行操作。

验证 Hemlock 是否已安装：

```bash
hemlock --version
```

## 安装方法

### 方法 1：Make Install

从源码构建并安装。

```bash
# 克隆仓库
git clone https://github.com/hemlang/hpm.git
cd hpm

# 安装到 /usr/local/bin（需要 sudo）
sudo make install
```

安装后，验证是否正常工作：

```bash
hpm --version
```

### 方法 2：自定义位置

安装到自定义目录（无需 sudo）：

```bash
# 克隆仓库
git clone https://github.com/hemlang/hpm.git
cd hpm

# 安装到 ~/.local/bin
make install PREFIX=$HOME/.local

# 或任何自定义位置
make install PREFIX=/opt/hemlock
```

确保你的自定义 bin 目录在 PATH 中：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### 方法 3：不安装直接运行

你可以直接运行 hpm 而无需安装：

```bash
# 克隆仓库
git clone https://github.com/hemlang/hpm.git
cd hpm

# 创建本地包装脚本
make

# 从 hpm 目录运行
./hpm --help

# 或直接通过 hemlock 运行
hemlock src/main.hml --help
```

### 方法 4：手动安装

创建你自己的包装脚本：

```bash
# 克隆到永久位置
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# 创建包装脚本
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## 安装变量

Makefile 支持以下变量：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `PREFIX` | `/usr/local` | 安装前缀 |
| `BINDIR` | `$(PREFIX)/bin` | 二进制文件目录 |
| `HEMLOCK` | `hemlock` | hemlock 解释器路径 |

使用自定义变量的示例：

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## 工作原理

安装程序创建一个 shell 包装脚本，使用 hpm 源代码调用 Hemlock 解释器：

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

这种方法：
- 无需编译
- 始终运行最新源代码
- 在所有平台上可靠运行

## 更新 hpm

要将 hpm 更新到最新版本：

```bash
cd /path/to/hpm
git pull origin main

# 如果路径改变了，重新安装
sudo make install
```

## 卸载

从系统中移除 hpm：

```bash
cd /path/to/hpm
sudo make uninstall
```

或手动移除：

```bash
sudo rm /usr/local/bin/hpm
```

## 验证安装

安装后，验证一切正常：

```bash
# 检查版本
hpm --version

# 查看帮助
hpm --help

# 测试初始化（在空目录中）
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## 故障排除

### "hemlock: command not found"

Hemlock 未安装或不在 PATH 中。请先安装 Hemlock：

```bash
# 检查 hemlock 是否存在
which hemlock

# 如果未找到，从 https://github.com/hemlang/hemlock 安装 Hemlock
```

### "Permission denied"

使用 sudo 进行系统范围安装，或安装到用户目录：

```bash
# 选项 1：使用 sudo
sudo make install

# 选项 2：安装到用户目录
make install PREFIX=$HOME/.local
```

### 安装后 "hpm: command not found"

你的 PATH 可能不包含安装目录：

```bash
# 检查 hpm 安装位置
ls -la /usr/local/bin/hpm

# 如果使用自定义位置，添加到 PATH
export PATH="$HOME/.local/bin:$PATH"
```

## 平台特定说明

### Linux

标准安装适用于所有 Linux 发行版。某些发行版可能需要：

```bash
# Debian/Ubuntu：确保安装构建工具
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

标准安装可用。如果使用 Homebrew：

```bash
# 确保安装 Xcode 命令行工具
xcode-select --install
```

### Windows (WSL)

hpm 在 Windows Subsystem for Linux 中可用：

```bash
# 在 WSL 终端中
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## 后续步骤

安装后：

1. [快速开始](quick-start.md) - 创建你的第一个项目
2. [命令参考](commands.md) - 学习所有命令
3. [配置](configuration.md) - 配置 hpm
