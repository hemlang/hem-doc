# 快速开始

5 分钟内开始使用 hpm。

## 安装 hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

更多安装选项请参阅[安装指南](installation.md)。

## 创建新项目

首先创建一个新目录并初始化包：

```bash
mkdir my-project
cd my-project
hpm init
```

系统会提示你输入项目详情：

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

使用 `--yes` 接受所有默认值：

```bash
hpm init --yes
```

## 项目结构

创建基本项目结构：

```
my-project/
├── package.json        # 项目清单
├── src/
│   └── index.hml      # 主入口点
└── test/
    └── test.hml       # 测试文件
```

创建主文件：

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Main entry point
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## 安装依赖

在 GitHub 上搜索包（包使用 `owner/repo` 格式）：

```bash
# 安装一个包
hpm install hemlang/sprout

# 使用版本约束安装
hpm install hemlang/json@^1.0.0

# 安装为开发依赖
hpm install hemlang/test-utils --dev
```

安装后，你的项目结构将包含 `hem_modules/`：

```
my-project/
├── package.json
├── package-lock.json   # 锁定文件（自动生成）
├── hem_modules/        # 已安装的包
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## 使用已安装的包

使用 GitHub 路径导入包：

```hemlock
// Import from installed package
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { middleware } from "hemlang/sprout/middleware";

// Standard library (built-in)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## 添加脚本

在 `package.json` 中添加脚本：

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

使用 `hpm run` 运行脚本：

```bash
hpm run start
hpm run build

# test 的简写形式
hpm test
```

## 常用工作流

### 安装所有依赖

当你克隆一个带有 `package.json` 的项目时：

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### 更新依赖

将所有包更新到约束范围内的最新版本：

```bash
hpm update
```

更新特定的包：

```bash
hpm update hemlang/sprout
```

### 查看已安装的包

列出所有已安装的包：

```bash
hpm list
```

输出显示依赖树：

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### 检查更新

查看哪些包有更新版本：

```bash
hpm outdated
```

### 移除包

```bash
hpm uninstall hemlang/sprout
```

## 示例：Web 应用

这是一个使用 Web 框架的完整示例：

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

运行应用：

```bash
hpm install
hpm run start
```

## 后续步骤

- [命令参考](commands.md) - 学习所有 hpm 命令
- [创建包](creating-packages.md) - 发布你自己的包
- [配置](configuration.md) - 配置 hpm 和 GitHub token
- [项目设置](project-setup.md) - 详细的项目配置
