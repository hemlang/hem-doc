# 故障排除

常见 hpm 问题的解决方案。

## 安装问题

### "hemlock: command not found"

**原因：** Hemlock 未安装或不在 PATH 中。

**解决方案：**

```bash
# 检查 hemlock 是否存在
which hemlock

# 如果未找到，请先安装 Hemlock
# 访问：https://github.com/hemlang/hemlock

# 安装后，验证
hemlock --version
```

### "hpm: command not found"

**原因：** hpm 未安装或不在 PATH 中。

**解决方案：**

```bash
# 检查 hpm 安装位置
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# 如果使用自定义位置，添加到 PATH
export PATH="$HOME/.local/bin:$PATH"

# 添加到 ~/.bashrc 或 ~/.zshrc 以持久化
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 如需要重新安装
cd /path/to/hpm
sudo make install
```

### 安装时 "Permission denied"

**原因：** 对安装目录没有写权限。

**解决方案：**

```bash
# 选项 1：使用 sudo 进行系统范围安装
sudo make install

# 选项 2：安装到用户目录（无需 sudo）
make install PREFIX=$HOME/.local
```

## 依赖问题

### "Package not found"（退出码 2）

**原因：** 包在 GitHub 上不存在。

**解决方案：**

```bash
# 验证包是否存在
# 检查：https://github.com/owner/repo

# 验证拼写
hpm install hemlang/sprout  # 正确
hpm install hemlan/sprout   # 错误的 owner
hpm install hemlang/spout   # 错误的 repo

# 检查 package.json 中的拼写错误
cat package.json | grep -A 5 dependencies
```

### "Version not found"（退出码 3）

**原因：** 没有发布版本匹配版本约束。

**解决方案：**

```bash
# 列出可用版本（检查 GitHub releases/tags）
# 标签必须以 'v' 开头（例如 v1.0.0）

# 使用有效的版本约束
hpm install owner/repo@^1.0.0

# 尝试最新版本
hpm install owner/repo

# 在 GitHub 上检查可用标签
# https://github.com/owner/repo/tags
```

### "Dependency conflict"（退出码 1）

**原因：** 两个包需要不兼容版本的依赖。

**解决方案：**

```bash
# 查看冲突
hpm install --verbose

# 检查什么需要该依赖
hpm why conflicting/package

# 解决方案：
# 1. 更新冲突的包
hpm update problem/package

# 2. 更改 package.json 中的版本约束
# 编辑以允许兼容的版本

# 3. 移除冲突的包之一
hpm uninstall one/package
```

### "Circular dependency"（退出码 8）

**原因：** 包 A 依赖 B，B 又依赖 A。

**解决方案：**

```bash
# 识别循环
hpm install --verbose

# 这通常是包中的 bug
# 联系包维护者

# 变通方法：避免使用其中一个包
```

## 网络问题

### "Network error"（退出码 4）

**原因：** 无法连接到 GitHub API。

**解决方案：**

```bash
# 检查网络连接
ping github.com

# 检查 GitHub API 是否可访问
curl -I https://api.github.com

# 重试（hpm 会自动重试）
hpm install

# 如果包已缓存，使用离线模式
hpm install --offline

# 如果在防火墙后面，检查代理设置
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded"（退出码 7）

**原因：** 未认证时 API 请求过多。

**解决方案：**

```bash
# 选项 1：使用 GitHub token 认证（推荐）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# 创建 token：GitHub → Settings → Developer settings → Personal access tokens

# 选项 2：将 token 保存在配置文件中
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# 选项 3：等待速率限制重置（每小时重置）

# 选项 4：使用离线模式
hpm install --offline
```

### 连接超时

**原因：** 网络慢或 GitHub API 问题。

**解决方案：**

```bash
# hpm 会自动使用指数退避重试

# 检查 GitHub 是否有问题
# 访问：https://www.githubstatus.com

# 稍后重试
hpm install

# 使用缓存的包
hpm install --offline
```

## Package.json 问题

### "Invalid package.json"（退出码 5）

**原因：** 格式错误或缺少必需字段。

**解决方案：**

```bash
# 验证 JSON 语法
cat package.json | python -m json.tool

# 检查必需字段
cat package.json

# 必需字段：
# - "name"：owner/repo 格式
# - "version"：X.Y.Z 格式

# 如需要重新生成
rm package.json
hpm init
```

### "name" 格式错误

**原因：** 包名称不是 `owner/repo` 格式。

**解决方案：**

```json
// 错误
{
  "name": "my-package"
}

// 正确
{
  "name": "yourusername/my-package"
}
```

### "version" 格式错误

**原因：** 版本不是 semver 格式。

**解决方案：**

```json
// 错误
{
  "version": "1.0"
}

// 正确
{
  "version": "1.0.0"
}
```

## 锁定文件问题

### 锁定文件不同步

**原因：** package.json 修改后未运行 install。

**解决方案：**

```bash
# 重新生成锁定文件
rm package-lock.json
hpm install
```

### 锁定文件损坏

**原因：** 无效的 JSON 或手动编辑。

**解决方案：**

```bash
# 检查 JSON 有效性
cat package-lock.json | python -m json.tool

# 重新生成
rm package-lock.json
hpm install
```

## hem_modules 问题

### 包未安装

**原因：** 各种可能的问题。

**解决方案：**

```bash
# 清理并重新安装
rm -rf hem_modules
hpm install

# 检查详细输出
hpm install --verbose
```

### Import 不工作

**原因：** 包未正确安装或导入路径错误。

**解决方案：**

```bash
# 验证包已安装
ls hem_modules/owner/repo/

# 检查 package.json 的 main 字段
cat hem_modules/owner/repo/package.json

# 正确的导入格式
import { x } from "owner/repo";          # 使用 main 入口
import { y } from "owner/repo/subpath";  # 子路径导入
```

### "Module not found" 错误

**原因：** 导入路径未解析到文件。

**解决方案：**

```bash
# 检查导入路径
ls hem_modules/owner/repo/src/

# 检查 index.hml
ls hem_modules/owner/repo/src/index.hml

# 验证 package.json 中的 main 字段
cat hem_modules/owner/repo/package.json | grep main
```

## 缓存问题

### 缓存占用太多空间

**解决方案：**

```bash
# 查看缓存大小
hpm cache list

# 清除缓存
hpm cache clean
```

### 缓存权限

**解决方案：**

```bash
# 修复权限
chmod -R u+rw ~/.hpm/cache

# 或移除并重新安装
rm -rf ~/.hpm/cache
hpm install
```

### 使用错误的缓存

**解决方案：**

```bash
# 检查缓存位置
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# 如果不正确，清除环境变量
unset HPM_CACHE_DIR
```

## 脚本问题

### "Script not found"

**原因：** 脚本名称在 package.json 中不存在。

**解决方案：**

```bash
# 列出可用脚本
cat package.json | grep -A 20 scripts

# 检查拼写
hpm run test    # 正确
hpm run tests   # 如果脚本名为 "test" 则错误
```

### 脚本失败

**原因：** 脚本命令中有错误。

**解决方案：**

```bash
# 直接运行命令以查看错误
hemlock test/run.hml

# 检查脚本定义
cat package.json | grep test
```

## 调试

### 启用详细输出

```bash
hpm install --verbose
```

### 检查 hpm 版本

```bash
hpm --version
```

### 检查 hemlock 版本

```bash
hemlock --version
```

### 干运行

预览而不进行更改：

```bash
hpm install --dry-run
```

### 从头开始

重新开始：

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## 获取帮助

### 命令帮助

```bash
hpm --help
hpm install --help
```

### 报告问题

如果遇到 bug：

1. 检查现有问题：https://github.com/hemlang/hpm/issues
2. 创建新问题，包含：
   - hpm 版本（`hpm --version`）
   - Hemlock 版本（`hemlock --version`）
   - 操作系统
   - 重现步骤
   - 错误消息（使用 `--verbose`）

## 退出码参考

| 代码 | 含义 | 常见解决方案 |
|------|---------|-----------------|
| 0 | 成功 | - |
| 1 | 依赖冲突 | 更新或更改约束 |
| 2 | 包未找到 | 检查拼写，验证仓库存在 |
| 3 | 版本未找到 | 在 GitHub 上检查可用版本 |
| 4 | 网络错误 | 检查连接，重试 |
| 5 | 无效的 package.json | 修复 JSON 语法和必需字段 |
| 6 | 完整性检查失败 | 清除缓存，重新安装 |
| 7 | GitHub 速率限制 | 添加 GITHUB_TOKEN |
| 8 | 循环依赖 | 联系包维护者 |

## 另请参阅

- [安装](installation.md) - 安装指南
- [配置](configuration.md) - 配置选项
- [命令](commands.md) - 命令参考
