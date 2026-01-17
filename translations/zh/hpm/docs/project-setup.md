# 项目设置

使用 hpm 设置 Hemlock 项目的完整指南。

## 创建新项目

### 基本设置

从头创建新项目：

```bash
# 创建项目目录
mkdir my-project
cd my-project

# 初始化 package.json
hpm init

# 创建目录结构
mkdir -p src test
```

### 项目模板

以下是不同用例的常见项目结构：

#### 库包

用于可复用的库：

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # 主入口，导出公共 API
│   ├── core.hml           # 核心功能
│   ├── utils.hml          # 工具函数
│   └── types.hml          # 类型定义
└── test/
    ├── framework.hml      # 测试框架
    ├── run.hml            # 测试运行器
    └── test_core.hml      # 测试
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### 应用程序

用于独立应用程序：

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # 应用程序入口点
│   ├── config.hml         # 配置
│   ├── commands/          # CLI 命令
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # 内部库
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # 数据文件
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Web 应用程序

用于 Web 服务器：

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # 服务器入口点
│   ├── routes/            # 路由处理器
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # 中间件
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # 数据模型
│   │   └── user.hml
│   └── services/          # 业务逻辑
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # 静态文件
│   ├── css/
│   └── js/
└── views/                 # 模板
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## package.json 文件

### 必需字段

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### 所有字段

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

### 字段参考

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `name` | string | owner/repo 格式的包名称（必需） |
| `version` | string | 语义化版本（必需） |
| `description` | string | 简短描述 |
| `author` | string | 作者姓名和邮箱 |
| `license` | string | 许可证标识符（MIT、Apache-2.0 等） |
| `repository` | string | 仓库 URL |
| `homepage` | string | 项目主页 |
| `bugs` | string | 问题跟踪器 URL |
| `main` | string | 入口点文件（默认：src/index.hml） |
| `keywords` | array | 搜索关键词 |
| `dependencies` | object | 运行时依赖 |
| `devDependencies` | object | 开发依赖 |
| `scripts` | object | 命名脚本 |
| `files` | array | 发布时包含的文件 |
| `native` | object | 原生库要求 |

## package-lock.json 文件

锁定文件自动生成，应提交到版本控制。它确保可重现的安装。

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### 锁定文件最佳实践

- **提交** package-lock.json 到版本控制
- **不要手动编辑** - 它是自动生成的
- **拉取更改后运行 `hpm install`**
- **如果损坏则删除并重新生成**：
  ```bash
  rm package-lock.json
  hpm install
  ```

## hem_modules 目录

已安装的包存储在 `hem_modules/` 中：

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### hem_modules 最佳实践

- **添加到 .gitignore** - 不要提交依赖
- **不要修改** - 更改会被覆盖
- **删除以重新安装**：
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Hemlock 项目推荐的 .gitignore：

```gitignore
# Dependencies
hem_modules/

# Build output
dist/
*.hmlc

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local

# Test coverage
coverage/
```

## 使用依赖

### 添加依赖

```bash
# 添加运行时依赖
hpm install hemlang/json

# 使用版本约束添加
hpm install hemlang/sprout@^2.0.0

# 添加开发依赖
hpm install hemlang/test-utils --dev
```

### 导入依赖

```hemlock
// Import from package (uses "main" entry)
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { Router } from "hemlang/sprout/router";

// Import standard library
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### 导入解析

hpm 按以下顺序解析导入：

1. **标准库**：`@stdlib/*` 导入内置模块
2. **包根目录**：`owner/repo` 使用 `main` 字段
3. **子路径**：`owner/repo/path` 检查：
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## 脚本

### 定义脚本

在 package.json 中添加脚本：

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

### 运行脚本

```bash
hpm run start
hpm run dev
hpm run build

# test 的简写
hpm test

# 传递参数
hpm run test -- --verbose --filter=unit
```

### 脚本命名约定

| 脚本 | 用途 |
|--------|---------|
| `start` | 运行应用程序 |
| `dev` | 以开发模式运行 |
| `test` | 运行所有测试 |
| `build` | 为生产环境构建 |
| `clean` | 移除生成的文件 |
| `lint` | 检查代码风格 |
| `format` | 格式化代码 |

## 开发工作流

### 初始设置

```bash
# 克隆项目
git clone https://github.com/yourusername/my-project.git
cd my-project

# 安装依赖
hpm install

# 运行测试
hpm test

# 开始开发
hpm run dev
```

### 日常工作流

```bash
# 拉取最新更改
git pull

# 安装任何新依赖
hpm install

# 进行更改...

# 运行测试
hpm test

# 提交
git add .
git commit -m "Add feature"
git push
```

### 添加新功能

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 如果需要，添加新依赖
hpm install hemlang/new-lib

# 实现功能...

# 测试
hpm test

# 提交并推送
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## 环境特定配置

### 使用环境变量

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### 配置文件

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## 另请参阅

- [快速开始](quick-start.md) - 快速入门
- [命令](commands.md) - 命令参考
- [创建包](creating-packages.md) - 发布包
- [配置](configuration.md) - hpm 配置
