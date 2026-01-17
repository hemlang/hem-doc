# 配置

本指南涵盖 hpm 的所有配置选项。

## 概述

hpm 可以通过以下方式配置：

1. **环境变量** - 用于运行时设置
2. **全局配置文件** - `~/.hpm/config.json`
3. **项目文件** - `package.json` 和 `package-lock.json`

## 环境变量

### GITHUB_TOKEN

用于认证的 GitHub API token。

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**认证的好处：**
- 更高的 API 速率限制（5000 vs 60 请求/小时）
- 访问私有仓库
- 更快的依赖解析

**创建 token：**

1. 前往 GitHub → Settings → Developer settings → Personal access tokens
2. 点击 "Generate new token (classic)"
3. 选择权限范围：
   - `repo` - 用于私有仓库访问
   - `read:packages` - 用于 GitHub Packages（如果使用）
4. 生成并复制 token

### HPM_CACHE_DIR

覆盖默认缓存目录。

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

默认值：`~/.hpm/cache`

**使用场景：**
- 具有自定义缓存位置的 CI/CD 系统
- 跨项目共享缓存
- 隔离构建的临时缓存

### HOME

用户主目录。用于定位：
- 配置目录：`$HOME/.hpm/`
- 缓存目录：`$HOME/.hpm/cache/`

通常由系统设置；仅在需要时覆盖。

### .bashrc / .zshrc 示例

```bash
# GitHub authentication (recommended)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Custom cache location (optional)
# export HPM_CACHE_DIR=/path/to/cache

# Add hpm to PATH (if using custom install location)
export PATH="$HOME/.local/bin:$PATH"
```

## 全局配置文件

### 位置

`~/.hpm/config.json`

### 格式

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### 创建配置文件

```bash
# Create config directory
mkdir -p ~/.hpm

# Create config file
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Secure the file (recommended)
chmod 600 ~/.hpm/config.json
```

### Token 优先级

如果两者都设置，环境变量优先：

1. `GITHUB_TOKEN` 环境变量（最高）
2. `~/.hpm/config.json` 的 `github_token` 字段
3. 无认证（默认）

## 目录结构

### 全局目录

```
~/.hpm/
├── config.json          # 全局配置
└── cache/               # 包缓存
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### 项目目录

```
my-project/
├── package.json         # 项目清单
├── package-lock.json    # 依赖锁定文件
├── hem_modules/         # 已安装的包
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # 源代码
└── test/                # 测试
```

## 包缓存

### 位置

默认：`~/.hpm/cache/`

使用 `HPM_CACHE_DIR` 环境变量覆盖

### 结构

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### 管理缓存

```bash
# 查看缓存的包
hpm cache list

# 清除整个缓存
hpm cache clean
```

### 缓存行为

- 包在首次下载后被缓存
- 后续安装使用缓存版本
- 使用 `--offline` 仅从缓存安装
- 缓存在所有项目间共享

## GitHub API 速率限制

### 无认证

- **每小时 60 个请求**，按 IP 地址计算
- 在同一 IP 上的所有未认证用户间共享
- 在 CI/CD 或有多个依赖时会很快耗尽

### 有认证

- **每小时 5000 个请求**，按认证用户计算
- 个人速率限制，不共享

### 处理速率限制

hpm 自动：
- 使用指数退避重试（1秒、2秒、4秒、8秒）
- 以退出码 7 报告速率限制错误
- 如果被速率限制则建议认证

**速率限制时的解决方案：**

```bash
# 选项 1：使用 GitHub token 认证
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# 选项 2：等待速率限制重置
# （限制每小时重置）

# 选项 3：使用离线模式（如果包已缓存）
hpm install --offline
```

## 离线模式

无网络访问时安装包：

```bash
hpm install --offline
```

**要求：**
- 所有包必须在缓存中
- 锁定文件必须存在且有精确版本

**使用场景：**
- 隔离网络的环境
- 更快的 CI/CD 构建（有热缓存）
- 避免速率限制

## CI/CD 配置

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Install Hemlock (adjust based on your setup)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copy package files first (for layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN hpm install

# Copy source code
COPY . .

# Run application
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## 代理配置

对于代理后面的环境，在系统级别配置：

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## 安全最佳实践

### Token 安全

1. **永远不要提交 token** 到版本控制
2. **在 CI/CD 中使用环境变量**
3. **将 token 权限范围限制**到最小需要
4. **定期轮换 token**
5. **保护配置文件**：
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### 私有仓库

要访问私有包：

1. 创建具有 `repo` 权限范围的 token
2. 配置认证（环境变量或配置文件）
3. 确保 token 有仓库访问权限

```bash
# 测试访问
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## 配置故障排除

### 验证配置

```bash
# 检查 token 是否设置
echo $GITHUB_TOKEN | head -c 10

# 检查配置文件
cat ~/.hpm/config.json

# 检查缓存目录
ls -la ~/.hpm/cache/

# 使用详细输出测试
hpm install --verbose
```

### 常见问题

**"GitHub rate limit exceeded"**
- 使用 `GITHUB_TOKEN` 设置认证
- 等待速率限制重置
- 如果包已缓存，使用 `--offline`

**缓存上的 "Permission denied"**
```bash
# 修复缓存权限
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# 创建配置目录
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## 另请参阅

- [安装](installation.md) - 安装 hpm
- [故障排除](troubleshooting.md) - 常见问题
- [命令](commands.md) - 命令参考
