# 包规范

`package.json` 文件格式的完整参考。

## 概述

每个 hpm 包都需要在项目根目录中有一个 `package.json` 文件。此文件定义包元数据、依赖项和脚本。

## 最小示例

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## 完整示例

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
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

## 字段参考

### name（必需）

`owner/repo` 格式的包名称。

```json
{
  "name": "hemlang/sprout"
}
```

**要求：**
- 必须是 `owner/repo` 格式
- `owner` 应该是你的 GitHub 用户名或组织
- `repo` 应该是仓库名称
- 使用小写字母、数字和连字符
- 总共最多 214 个字符

**有效名称：**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**无效名称：**
```
my-package          # 缺少 owner
hemlang/My_Package  # 大写和下划线
hemlang             # 缺少 repo
```

### version（必需）

遵循[语义化版本](https://semver.org/)的包版本。

```json
{
  "version": "1.2.3"
}
```

**格式：** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**有效版本：**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

包的简短描述。

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- 保持在 200 个字符以内
- 描述包做什么，而不是怎么做

### author

包作者信息。

```json
{
  "author": "Your Name <email@example.com>"
}
```

**接受的格式：**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

许可证标识符。

```json
{
  "license": "MIT"
}
```

**常见许可证：**
- `MIT` - MIT 许可证
- `Apache-2.0` - Apache 许可证 2.0
- `GPL-3.0` - GNU 通用公共许可证 v3.0
- `BSD-3-Clause` - BSD 3-Clause 许可证
- `ISC` - ISC 许可证
- `UNLICENSED` - 专有/私有

尽可能使用 [SPDX 标识符](https://spdx.org/licenses/)。

### repository

源仓库链接。

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

项目主页 URL。

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

问题跟踪器 URL。

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

包的入口点文件。

```json
{
  "main": "src/index.hml"
}
```

**默认值：** `src/index.hml`

当用户导入你的包时：
```hemlock
import { x } from "owner/repo";
```

hpm 加载 `main` 中指定的文件。

**导入的解析顺序：**
1. 精确路径：`src/index.hml`
2. 带 .hml 扩展名：`src/index` → `src/index.hml`
3. 索引文件：`src/index/` → `src/index/index.hml`

### keywords

用于可发现性的关键词数组。

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- 使用小写
- 具体且相关
- 如果适当，包含语言（"hemlock"）

### dependencies

包工作所需的运行时依赖。

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**键：** 包名称（`owner/repo`）
**值：** 版本约束

**版本约束语法：**

| 约束 | 含义 |
|------------|---------|
| `1.2.3` | 精确版本 |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | 至少 1.0.0 |
| `>=1.0.0 <2.0.0` | 范围 |
| `*` | 任意版本 |

### devDependencies

仅用于开发的依赖（测试、构建等）。

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

开发依赖是：
- 在开发期间安装
- 当包作为依赖使用时不安装
- 用于测试、构建、检查等

### scripts

可以使用 `hpm run` 运行的命名命令。

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

**运行脚本：**
```bash
hpm run start
hpm run build
hpm test        # 'hpm run test' 的简写
```

**传递参数：**
```bash
hpm run test -- --verbose --filter=unit
```

**常见脚本：**

| 脚本 | 用途 |
|--------|---------|
| `start` | 启动应用程序 |
| `dev` | 带热重载的开发模式 |
| `test` | 运行测试 |
| `build` | 为生产环境构建 |
| `clean` | 移除构建产物 |
| `lint` | 检查代码风格 |
| `format` | 格式化代码 |

### files

安装包时要包含的文件和目录。

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**默认行为：** 如果未指定，包含：
- 仓库中的所有文件
- 排除 `.git/`、`node_modules/`、`hem_modules/`

**用于：**
- 减少包大小
- 从分发中排除测试文件
- 仅包含必要文件

### native

原生库要求。

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

记录必须在系统上安装的原生依赖。

## 验证

hpm 在各种操作中验证 package.json。常见验证错误：

### 缺少必需字段

```
Error: package.json missing required field: name
```

**修复：** 添加必需字段。

### 无效的名称格式

```
Error: Invalid package name. Must be in owner/repo format.
```

**修复：** 使用 `owner/repo` 格式。

### 无效的版本

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**修复：** 使用完整的 semver 格式（`1.0.0`）。

### 无效的 JSON

```
Error: package.json is not valid JSON
```

**修复：** 检查 JSON 语法（逗号、引号、括号）。

## 创建 package.json

### 交互式

```bash
hpm init
```

交互式提示每个字段。

### 使用默认值

```bash
hpm init --yes
```

使用默认值创建：
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### 手动

手动创建文件：

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## 最佳实践

1. **始终指定 main** - 不要依赖默认值
2. **使用插入符范围** - 大多数依赖使用 `^1.0.0`
3. **分离开发依赖** - 将测试/构建依赖放在 devDependencies 中
4. **包含关键词** - 帮助用户找到你的包
5. **记录脚本** - 清晰命名脚本
6. **指定许可证** - 开源项目必需
7. **添加描述** - 帮助用户理解用途

## 另请参阅

- [创建包](creating-packages.md) - 发布指南
- [版本控制](versioning.md) - 版本约束
- [项目设置](project-setup.md) - 项目结构
