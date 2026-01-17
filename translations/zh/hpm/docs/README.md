# hpm 文档

欢迎来到 hpm (Hemlock Package Manager) 文档。hpm 是 [Hemlock](https://github.com/hemlang/hemlock) 编程语言的官方包管理器。

## 概述

hpm 使用 GitHub 作为其包注册表，包通过其 GitHub 仓库路径进行标识（例如 `hemlang/sprout`）。这意味着：

- **无中央注册表** - 包存放在 GitHub 仓库中
- **版本标签** - 发布版本通过 Git 标签标识（例如 `v1.0.0`）
- **发布即 git 操作** - 推送标签即可发布新版本

## 文档

### 入门指南

- [安装](installation.md) - 如何安装 hpm
- [快速开始](quick-start.md) - 5 分钟内开始使用
- [项目设置](project-setup.md) - 设置新的 Hemlock 项目

### 用户指南

- [命令参考](commands.md) - 所有 hpm 命令的完整参考
- [配置](configuration.md) - 配置文件和环境变量
- [故障排除](troubleshooting.md) - 常见问题及解决方案

### 包开发

- [创建包](creating-packages.md) - 如何创建和发布包
- [包规范](package-spec.md) - package.json 格式
- [版本控制](versioning.md) - 语义化版本和版本约束

### 参考

- [架构](architecture.md) - 内部架构和设计
- [退出码](exit-codes.md) - CLI 退出码参考

## 快速参考

### 基本命令

```bash
hpm init                              # 创建新的 package.json
hpm install                           # 安装所有依赖
hpm install owner/repo                # 添加并安装一个包
hpm install owner/repo@^1.0.0        # 使用版本约束安装
hpm uninstall owner/repo              # 移除一个包
hpm update                            # 更新所有包
hpm list                              # 显示已安装的包
hpm run <script>                      # 运行包脚本
```

### 包标识

包使用 GitHub `owner/repo` 格式：

```
hemlang/sprout          # Web 框架
hemlang/json            # JSON 工具库
alice/http-client       # HTTP 客户端库
```

### 版本约束

| 语法 | 含义 |
|--------|---------|
| `1.0.0` | 精确版本 |
| `^1.2.3` | 兼容版本 (>=1.2.3 <2.0.0) |
| `~1.2.3` | 补丁更新 (>=1.2.3 <1.3.0) |
| `>=1.0.0` | 至少 1.0.0 |
| `*` | 任意版本 |

## 获取帮助

- 使用 `hpm --help` 获取命令行帮助
- 使用 `hpm <command> --help` 获取特定命令的帮助
- 在 [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues) 报告问题

## 许可证

hpm 基于 MIT 许可证发布。
