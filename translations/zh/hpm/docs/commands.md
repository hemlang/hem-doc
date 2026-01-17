# 命令参考

所有 hpm 命令的完整参考。

## 全局选项

这些选项适用于任何命令：

| 选项 | 描述 |
|--------|-------------|
| `--help`, `-h` | 显示帮助信息 |
| `--version`, `-v` | 显示 hpm 版本 |
| `--verbose` | 显示详细输出 |

## 命令

### hpm init

创建新的 `package.json` 文件。

```bash
hpm init        # 交互模式
hpm init --yes  # 接受所有默认值
hpm init -y     # 简写形式
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--yes`, `-y` | 对所有提示接受默认值 |

**交互提示：**
- 包名称（owner/repo 格式）
- 版本（默认：1.0.0）
- 描述
- 作者
- 许可证（默认：MIT）
- 主文件（默认：src/index.hml）

**示例：**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

安装依赖或添加新包。

```bash
hpm install                           # 从 package.json 安装所有依赖
hpm install owner/repo                # 添加并安装包
hpm install owner/repo@^1.0.0        # 使用版本约束
hpm install owner/repo --dev         # 作为开发依赖
hpm i owner/repo                      # 简写形式
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--dev`, `-D` | 添加到 devDependencies |
| `--verbose` | 显示详细进度 |
| `--dry-run` | 预览而不安装 |
| `--offline` | 仅从缓存安装（无网络） |
| `--parallel` | 启用并行下载（实验性） |

**版本约束语法：**

| 语法 | 示例 | 含义 |
|--------|---------|---------|
| （无） | `owner/repo` | 最新版本 |
| 精确 | `owner/repo@1.2.3` | 正好是 1.2.3 |
| 插入符 | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| 波浪号 | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| 范围 | `owner/repo@>=1.0.0` | 至少 1.0.0 |

**示例：**

```bash
# 安装所有依赖
hpm install

# 安装特定包
hpm install hemlang/json

# 使用版本约束安装
hpm install hemlang/sprout@^2.0.0

# 安装为开发依赖
hpm install hemlang/test-utils --dev

# 预览将要安装的内容
hpm install hemlang/sprout --dry-run

# 详细输出
hpm install --verbose

# 仅从缓存安装（离线）
hpm install --offline
```

**输出：**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

移除一个包。

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # 简写形式
hpm remove owner/repo      # 替代形式
```

**示例：**

```bash
hpm uninstall hemlang/sprout
```

**输出：**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

将包更新到约束范围内的最新版本。

```bash
hpm update              # 更新所有包
hpm update owner/repo   # 更新特定包
hpm up owner/repo       # 简写形式
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--verbose` | 显示详细进度 |
| `--dry-run` | 预览而不更新 |

**示例：**

```bash
# 更新所有包
hpm update

# 更新特定包
hpm update hemlang/sprout

# 预览更新
hpm update --dry-run
```

**输出：**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

显示已安装的包。

```bash
hpm list              # 显示完整依赖树
hpm list --depth=0    # 仅直接依赖
hpm list --depth=1    # 一级传递依赖
hpm ls                # 简写形式
```

**选项：**

| 选项 | 描述 |
|--------|-------------|
| `--depth=N` | 限制树深度（默认：全部） |

**示例：**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

显示有更新版本的包。

```bash
hpm outdated
```

**输出：**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**：已安装版本
- **Wanted**：符合约束的最高版本
- **Latest**：最新可用版本

---

### hpm run

执行 package.json 中的脚本。

```bash
hpm run <script>
hpm run <script> -- <args>
```

**示例：**

给定以下 package.json：

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

运行脚本：

```bash
hpm run start
hpm run test
hpm run build

# 向脚本传递参数
hpm run test -- --verbose
```

---

### hpm test

`hpm run test` 的简写。

```bash
hpm test
hpm test -- --verbose
```

等同于：

```bash
hpm run test
```

---

### hpm why

解释为什么安装了某个包（显示依赖链）。

```bash
hpm why owner/repo
```

**示例：**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

管理全局包缓存。

```bash
hpm cache list    # 列出缓存的包
hpm cache clean   # 清除所有缓存的包
```

**子命令：**

| 子命令 | 描述 |
|------------|-------------|
| `list` | 显示所有缓存的包及大小 |
| `clean` | 移除所有缓存的包 |

**示例：**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## 命令快捷方式

为方便起见，多个命令有简短别名：

| 命令 | 快捷方式 |
|---------|-----------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**示例：**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## 退出码

hpm 使用特定的退出码来指示不同的错误条件：

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | 依赖冲突 |
| 2 | 包未找到 |
| 3 | 版本未找到 |
| 4 | 网络错误 |
| 5 | 无效的 package.json |
| 6 | 完整性检查失败 |
| 7 | 超出 GitHub 速率限制 |
| 8 | 循环依赖 |

在脚本中使用退出码：

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## 环境变量

hpm 支持以下环境变量：

| 变量 | 描述 |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub API token 用于认证 |
| `HPM_CACHE_DIR` | 覆盖缓存目录位置 |
| `HOME` | 用户主目录（用于配置/缓存） |

**示例：**

```bash
# 使用 GitHub token 获得更高的速率限制
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# 使用自定义缓存目录
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## 另请参阅

- [配置](configuration.md) - 配置文件
- [包规范](package-spec.md) - package.json 格式
- [故障排除](troubleshooting.md) - 常见问题
