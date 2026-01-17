# 创建包

本指南介绍如何创建、组织和发布 Hemlock 包。

## 概述

hpm 使用 GitHub 作为其包注册表。包通过其 GitHub `owner/repo` 路径标识，版本是 Git 标签。发布只需推送带标签的发布版本。

## 创建新包

### 1. 初始化包

创建新目录并初始化：

```bash
mkdir my-package
cd my-package
hpm init
```

回答提示：

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. 创建项目结构

包的推荐结构：

```
my-package/
├── package.json          # 包清单
├── README.md             # 文档
├── LICENSE               # 许可证文件
├── src/
│   ├── index.hml         # 主入口点（导出公共 API）
│   ├── utils.hml         # 内部工具
│   └── types.hml         # 类型定义
└── test/
    ├── framework.hml     # 测试框架
    └── test_utils.hml    # 测试
```

### 3. 定义你的公共 API

**src/index.hml** - 主入口点：

```hemlock
// Re-export public API
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Direct exports
export fn create(options: Options): Config {
    // Implementation
}

export fn validate(config: Config): bool {
    // Implementation
}
```

### 4. 编写你的 package.json

完整的 package.json 示例：

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## 包命名

### 要求

- 必须是 `owner/repo` 格式
- `owner` 应该是你的 GitHub 用户名或组织
- `repo` 应该是仓库名称
- 多词名称使用小写字母和连字符

### 好的名称

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### 避免

```
my-package          # 缺少 owner
alice/MyPackage     # PascalCase
alice/my_package    # 下划线
```

## 包结构最佳实践

### 入口点

package.json 中的 `main` 字段指定入口点：

```json
{
  "main": "src/index.hml"
}
```

此文件应导出你的公共 API：

```hemlock
// Export everything users need
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Types
export type { Config, Options } from "./types.hml";
```

### 内部与公共

保持内部实现细节私有：

```
src/
├── index.hml          # 公共：导出的 API
├── parser.hml         # 公共：被 index.hml 使用
├── formatter.hml      # 公共：被 index.hml 使用
└── internal/
    ├── helpers.hml    # 私有：仅供内部使用
    └── constants.hml  # 私有：仅供内部使用
```

用户从你的包根目录导入：

```hemlock
// Good - imports from public API
import { parse, Parser } from "yourusername/my-package";

// Also works - subpath import
import { validate } from "yourusername/my-package/validator";

// Discouraged - accessing internals
import { helper } from "yourusername/my-package/internal/helpers";
```

### 子路径导出

支持从子路径导入：

```
src/
├── index.hml              # 主入口
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

用户可以导入：

```hemlock
import { parse } from "yourusername/my-package";           // Main
import { Parser } from "yourusername/my-package/parser";   // Subpath
import { format } from "yourusername/my-package/formatter";
```

## 依赖

### 添加依赖

```bash
# 运行时依赖
hpm install hemlang/json

# 开发依赖
hpm install hemlang/test-utils --dev
```

### 依赖最佳实践

1. **大多数依赖使用插入符范围**：
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **仅在必要时锁定版本**（API 不稳定）：
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **避免过于严格的范围**：
   ```json
   // Bad: too restrictive
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Good: allows compatible updates
   "hemlang/json": "^1.2.3"
   ```

4. **分离开发依赖**：
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## 测试你的包

### 编写测试

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### 运行测试

添加测试脚本：

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

运行：

```bash
hpm test
```

## 发布

### 前提条件

1. 创建与你的包名称匹配的 GitHub 仓库
2. 确保 `package.json` 完整有效
3. 所有测试通过

### 发布流程

发布只需推送 Git 标签：

```bash
# 1. 确保所有内容已提交
git add .
git commit -m "Prepare v1.0.0 release"

# 2. 创建版本标签（必须以 'v' 开头）
git tag v1.0.0

# 3. 推送代码和标签
git push origin main
git push origin v1.0.0
# 或一次推送所有标签
git push origin main --tags
```

### 版本标签

标签必须遵循 `vX.Y.Z` 格式：

```bash
git tag v1.0.0      # 发布版
git tag v1.0.1      # 补丁
git tag v1.1.0      # 次要版本
git tag v2.0.0      # 主要版本
git tag v1.0.0-beta.1  # 预发布
```

### 发布清单

发布新版本之前：

1. **更新** package.json 中的版本
2. **运行测试**：`hpm test`
3. **更新 CHANGELOG**（如果有的话）
4. **更新 README**（如果 API 改变了）
5. **提交更改**
6. **创建标签**
7. **推送到 GitHub**

### 自动化示例

创建发布脚本：

```bash
#!/bin/bash
# release.sh - Release a new version

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Run tests
hpm test || exit 1

# Update version in package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Commit and tag
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Push
git push origin main --tags

echo "Released v$VERSION"
```

## 用户安装你的包

发布后，用户可以安装：

```bash
# 最新版本
hpm install yourusername/my-package

# 特定版本
hpm install yourusername/my-package@1.0.0

# 版本约束
hpm install yourusername/my-package@^1.0.0
```

并导入：

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## 文档

### README.md

每个包都应该有 README：

```markdown
# my-package

A brief description of what this package does.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Usage

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Parses the input string.

### stringify(obj: any): string

Converts object to string.

## License

MIT
```

### API 文档

记录所有公共导出：

```hemlock
/// Parses the input string into a structured Result.
///
/// # Arguments
/// * `input` - The string to parse
///
/// # Returns
/// A Result containing the parsed data or an error
///
/// # Example
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementation
}
```

## 版本指南

遵循[语义化版本](https://semver.org/)：

- **MAJOR**（1.0.0 → 2.0.0）：破坏性更改
- **MINOR**（1.0.0 → 1.1.0）：新功能，向后兼容
- **PATCH**（1.0.0 → 1.0.1）：错误修复，向后兼容

### 何时递增

| 更改类型 | 版本递增 |
|-------------|--------------|
| 破坏性 API 更改 | MAJOR |
| 移除函数/类型 | MAJOR |
| 更改函数签名 | MAJOR |
| 添加新函数 | MINOR |
| 添加新功能 | MINOR |
| 错误修复 | PATCH |
| 文档更新 | PATCH |
| 内部重构 | PATCH |

## 另请参阅

- [包规范](package-spec.md) - 完整的 package.json 参考
- [版本控制](versioning.md) - 语义化版本详情
- [配置](configuration.md) - GitHub 认证
