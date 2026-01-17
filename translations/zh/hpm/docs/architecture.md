# 架构

hpm 的内部架构和设计。本文档面向贡献者和有兴趣了解 hpm 工作原理的人。

## 概述

hpm 使用 Hemlock 编写，由多个模块组成，处理包管理的不同方面：

```
src/
├── main.hml        # CLI 入口点和命令路由
├── manifest.hml    # package.json 处理
├── lockfile.hml    # package-lock.json 处理
├── semver.hml      # 语义化版本
├── resolver.hml    # 依赖解析
├── github.hml      # GitHub API 客户端
├── installer.hml   # 包下载和提取
└── cache.hml       # 全局缓存管理
```

## 模块职责

### main.hml

CLI 应用程序的入口点。

**职责：**
- 解析命令行参数
- 将命令路由到适当的处理器
- 显示帮助和版本信息
- 处理全局标志（--verbose、--dry-run 等）
- 以适当的代码退出

**关键函数：**
- `main()` - 入口点，解析参数并分派命令
- `cmd_init()` - 处理 `hpm init`
- `cmd_install()` - 处理 `hpm install`
- `cmd_uninstall()` - 处理 `hpm uninstall`
- `cmd_update()` - 处理 `hpm update`
- `cmd_list()` - 处理 `hpm list`
- `cmd_outdated()` - 处理 `hpm outdated`
- `cmd_run()` - 处理 `hpm run`
- `cmd_why()` - 处理 `hpm why`
- `cmd_cache()` - 处理 `hpm cache`

**命令快捷方式：**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

处理 `package.json` 文件的读写。

**职责：**
- 读写 package.json
- 验证包结构
- 管理依赖
- 解析包说明符（owner/repo@version）

**关键函数：**
```hemlock
create_default(): Manifest           // 创建空清单
read_manifest(): Manifest            // 从文件读取
write_manifest(m: Manifest)          // 写入文件
validate(m: Manifest): bool          // 验证结构
get_all_dependencies(m): Map         // 获取 deps + devDeps
add_dependency(m, pkg, ver, dev)     // 添加依赖
remove_dependency(m, pkg)            // 移除依赖
parse_specifier(spec): (name, ver)   // 解析 "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // 解析 "owner/repo"
```

**Manifest 结构：**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

管理 `package-lock.json` 文件以实现可重现的安装。

**职责：**
- 创建/读取/写入锁定文件
- 跟踪精确解析的版本
- 存储下载 URL 和完整性哈希
- 清理孤立的依赖

**关键函数：**
```hemlock
create_empty(): Lockfile              // 创建空锁定文件
read_lockfile(): Lockfile             // 从文件读取
write_lockfile(l: Lockfile)           // 写入文件
create_entry(ver, url, hash, deps)    // 创建锁定条目
get_locked(l, pkg): LockEntry?        // 获取锁定版本
set_locked(l, pkg, entry)             // 设置锁定版本
remove_locked(l, pkg)                 // 移除条目
prune(l, keep: Set)                   // 移除孤立项
needs_update(l, m): bool              // 检查是否不同步
```

**Lockfile 结构：**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // 下载 URL
    integrity: string,    // SHA256 哈希
    dependencies: Map<string, string>
};
```

### semver.hml

语义化版本 2.0.0 的完整实现。

**职责：**
- 解析版本字符串
- 比较版本
- 解析和评估版本约束
- 查找满足约束的版本

**关键函数：**
```hemlock
// 解析
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// 比较
compare(a, b: Version): int           // -1、0 或 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// 约束
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // 检查 v 是否匹配 c
max_satisfying(versions, c): Version?      // 查找最高匹配
sort(versions): [Version]                  // 升序排序

// 工具
constraints_overlap(a, b: Constraint): bool  // 检查兼容性
```

**Version 结构：**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // 例如 ["beta", "1"]
    build: string?          // 例如 "20230101"
};
```

**Constraint 类型：**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // 组合范围
    | Any;                     // "*"
```

### resolver.hml

实现 npm 风格的依赖解析。

**职责：**
- 解析依赖树
- 检测版本冲突
- 检测循环依赖
- 构建可视化树

**关键函数：**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // 主解析器：返回所有依赖及解析版本的扁平映射

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // 查找满足所有约束的版本

detect_cycles(deps: Map): [Cycle]?
    // 使用 DFS 查找循环依赖

build_tree(lockfile): Tree
    // 创建用于显示的树结构

find_why(pkg, lockfile): [Chain]
    // 查找解释为什么安装 pkg 的依赖链
```

**解析算法：**

1. **收集约束**：遍历清单和传递依赖
2. **解析每个包**：对于每个包：
   - 从依赖方获取所有版本约束
   - 从 GitHub 获取可用版本
   - 查找满足所有约束的最高版本
   - 如果没有版本满足所有约束则报错（冲突）
3. **检测循环**：运行 DFS 查找循环依赖
4. **返回扁平映射**：包名 → 解析的版本信息

**ResolveResult 结构：**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

用于包发现和下载的 GitHub API 客户端。

**职责：**
- 获取可用版本（标签）
- 从仓库下载 package.json
- 下载发布 tarball
- 处理认证和速率限制

**关键函数：**
```hemlock
get_token(): string?
    // 从环境或配置获取 token

github_request(url, headers?): Response
    // 带重试的 API 请求

get_tags(owner, repo): [string]
    // 获取版本标签（v1.0.0、v1.1.0 等）

get_package_json(owner, repo, ref): Manifest
    // 在特定标签/提交处获取 package.json

download_tarball(owner, repo, tag): bytes
    // 下载发布归档

repo_exists(owner, repo): bool
    // 检查仓库是否存在

get_repo_info(owner, repo): RepoInfo
    // 获取仓库元数据
```

**重试逻辑：**
- 指数退避：1秒、2秒、4秒、8秒
- 重试条件：403（速率限制）、5xx（服务器错误）、网络错误
- 最多 4 次重试
- 清晰报告速率限制错误

**使用的 API 端点：**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

处理包的下载和提取。

**职责：**
- 从 GitHub 下载包
- 将 tarball 提取到 hem_modules
- 检查/使用缓存的包
- 安装/卸载包

**关键函数：**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // 下载并安装单个包

install_all(packages: Map, options): InstallResult
    // 安装所有解析的包

uninstall_package(name: string): bool
    // 从 hem_modules 移除包

get_installed(): Map<string, string>
    // 列出当前已安装的包

verify_integrity(pkg): bool
    // 验证包完整性

prefetch_packages(packages: Map): void
    // 并行下载到缓存（实验性）
```

**安装过程：**

1. 检查是否已安装正确版本
2. 检查缓存中的 tarball
3. 如果未缓存，从 GitHub 下载
4. 存储到缓存供将来使用
5. 提取到 `hem_modules/owner/repo/`
6. 验证安装

**创建的目录结构：**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

管理全局包缓存。

**职责：**
- 存储下载的 tarball
- 检索缓存的包
- 列出缓存的包
- 清除缓存
- 管理配置

**关键函数：**
```hemlock
get_cache_dir(): string
    // 获取缓存目录（尊重 HPM_CACHE_DIR）

get_config_dir(): string
    // 获取配置目录（~/.hpm）

is_cached(owner, repo, version): bool
    // 检查 tarball 是否已缓存

get_cached_path(owner, repo, version): string
    // 获取缓存 tarball 的路径

store_tarball_file(owner, repo, version, data): void
    // 将 tarball 保存到缓存

list_cached(): [CachedPackage]
    // 列出所有缓存的包

clear_cache(): int
    // 移除所有缓存的包，返回释放的字节数

get_cache_size(): int
    // 计算缓存总大小

read_config(): Config
    // 读取 ~/.hpm/config.json

write_config(c: Config): void
    // 写入配置文件
```

**缓存结构：**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## 数据流

### Install 命令流程

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ 解析参数，调用 cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ 读取 package.json，添加依赖
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ 解析所有依赖
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ 获取版本，查找满足条件的版本
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ 下载并提取包
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ 下载或使用缓存
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ 更新 package-lock.json
    └──────────┘
```

### 解析算法详情

```
输入：manifest.dependencies、manifest.devDependencies、现有 lockfile

1. 初始化：
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [直接依赖]

2. 当队列不为空时：
   a. pkg = queue.pop()
   b. 如果 pkg 已解析，跳过
   c. 从依赖方获取 pkg 的所有约束
   d. 从 GitHub 获取可用版本（已缓存）
   e. 查找满足所有约束的最高版本
   f. 如果未找到：冲突
   g. resolved[pkg] = {version, url, deps}
   h. 将 pkg 的依赖添加到队列

3. 在解析图中检测循环
   - 如果发现循环：错误

4. 返回解析映射
```

## 错误处理

### 退出码

在 main.hml 中定义：

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### 错误传播

错误通过返回值向上冒泡：

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? 传播错误
    // ...
}
```

## 测试

### 测试框架

`test/framework.hml` 中的自定义测试框架：

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### 测试文件

- `test/test_semver.hml` - 版本解析、比较、约束
- `test/test_manifest.hml` - 清单读写、验证
- `test/test_lockfile.hml` - 锁定文件操作
- `test/test_cache.hml` - 缓存管理

### 运行测试

```bash
# 所有测试
make test

# 特定测试
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## 未来改进

### 计划功能

1. **完整性验证** - 完整的 SHA256 哈希检查
2. **工作区** - Monorepo 支持
3. **插件系统** - 可扩展命令
4. **审计** - 安全漏洞检查
5. **私有注册表** - 自托管包托管

### 已知限制

1. **打包器 bug** - 无法创建独立可执行文件
2. **并行下载** - 实验性，可能有竞态条件
3. **完整性** - SHA256 未完全实现

## 贡献

### 代码风格

- 使用 4 空格缩进
- 函数应该只做一件事
- 注释复杂逻辑
- 为新功能编写测试

### 添加命令

1. 在 `main.hml` 中添加处理器：
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementation
   }
   ```

2. 添加到命令分派：
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. 更新帮助文本

### 添加模块

1. 创建 `src/newmodule.hml`
2. 导出公共接口
3. 在需要它的模块中导入
4. 在 `test/test_newmodule.hml` 中添加测试

## 另请参阅

- [命令](commands.md) - CLI 参考
- [创建包](creating-packages.md) - 包开发
- [版本控制](versioning.md) - 语义化版本
