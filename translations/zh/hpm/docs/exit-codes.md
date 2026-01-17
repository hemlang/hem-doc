# 退出码

hpm 退出码及其含义的参考。

## 退出码表

| 代码 | 名称 | 描述 |
|------|------|-------------|
| 0 | SUCCESS | 命令成功完成 |
| 1 | CONFLICT | 依赖版本冲突 |
| 2 | NOT_FOUND | 包未找到 |
| 3 | VERSION_NOT_FOUND | 请求的版本未找到 |
| 4 | NETWORK | 网络错误 |
| 5 | INVALID_MANIFEST | 无效的 package.json |
| 6 | INTEGRITY | 完整性检查失败 |
| 7 | RATE_LIMIT | 超出 GitHub API 速率限制 |
| 8 | CIRCULAR | 检测到循环依赖 |

## 详细描述

### 退出码 0: SUCCESS

命令成功完成。

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### 退出码 1: CONFLICT

两个或多个包需要不兼容版本的依赖。

**示例：**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**解决方案：**
1. 检查哪些包有冲突：
   ```bash
   hpm why hemlang/json
   ```
2. 更新冲突的包：
   ```bash
   hpm update package-a
   ```
3. 放宽 package.json 中的版本约束
4. 移除冲突的包之一

### 退出码 2: NOT_FOUND

指定的包在 GitHub 上不存在。

**示例：**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**解决方案：**
1. 验证包名称拼写
2. 检查仓库是否存在：`https://github.com/owner/repo`
3. 验证你有访问权限（对于私有仓库，设置 GITHUB_TOKEN）

### 退出码 3: VERSION_NOT_FOUND

没有版本匹配指定的约束。

**示例：**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**解决方案：**
1. 在 GitHub releases/tags 上检查可用版本
2. 使用有效的版本约束
3. 版本标签必须以 'v' 开头（例如 `v1.0.0`）

### 退出码 4: NETWORK

发生网络相关错误。

**示例：**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**解决方案：**
1. 检查网络连接
2. 检查 GitHub 是否可访问
3. 如果在防火墙后面，验证代理设置
4. 如果包已缓存，使用 `--offline`：
   ```bash
   hpm install --offline
   ```
5. 等待并重试（hpm 会自动重试）

### 退出码 5: INVALID_MANIFEST

package.json 文件无效或格式错误。

**示例：**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**解决方案：**
1. 检查 JSON 语法（使用 JSON 验证器）
2. 确保必需字段存在（`name`、`version`）
3. 验证字段格式：
   - name：`owner/repo` 格式
   - version：`X.Y.Z` semver 格式
4. 重新生成：
   ```bash
   rm package.json
   hpm init
   ```

### 退出码 6: INTEGRITY

包完整性验证失败。

**示例：**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**解决方案：**
1. 清除缓存并重新安装：
   ```bash
   hpm cache clean
   hpm install
   ```
2. 检查网络问题（部分下载）
3. 验证包未被篡改

### 退出码 7: RATE_LIMIT

超出 GitHub API 速率限制。

**示例：**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**解决方案：**
1. **使用 GitHub 认证**（推荐）：
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. 等待速率限制重置（每小时重置）
3. 如果包已缓存，使用离线模式：
   ```bash
   hpm install --offline
   ```

### 退出码 8: CIRCULAR

在依赖图中检测到循环依赖。

**示例：**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**解决方案：**
1. 这通常是包本身的 bug
2. 联系包维护者
3. 避免使用循环包之一

## 在脚本中使用退出码

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## 按退出码故障排除

### 快速参考

| 代码 | 首先检查 |
|------|---------------------|
| 1 | 运行 `hpm why <package>` 查看冲突 |
| 2 | 在 GitHub 上验证包名称 |
| 3 | 在 GitHub 标签上检查可用版本 |
| 4 | 检查网络连接 |
| 5 | 验证 package.json 语法 |
| 6 | 运行 `hpm cache clean && hpm install` |
| 7 | 设置 `GITHUB_TOKEN` 环境变量 |
| 8 | 联系包维护者 |

## 另请参阅

- [故障排除](troubleshooting.md) - 详细解决方案
- [命令](commands.md) - 命令参考
- [配置](configuration.md) - 设置 GitHub token
