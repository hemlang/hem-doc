# 版本控制

hpm 中语义化版本控制的完整指南。

## 语义化版本

hpm 使用[语义化版本 2.0.0](https://semver.org/)（semver）进行包版本管理。

### 版本格式

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**示例：**
```
1.0.0           # 发布版本
2.1.3           # 发布版本
1.0.0-alpha     # 预发布
1.0.0-beta.1    # 带编号的预发布
1.0.0-rc.1      # 候选发布
1.0.0+20231201  # 带构建元数据
1.0.0-beta+exp  # 预发布带构建元数据
```

### 版本组成部分

| 组成部分 | 描述 | 示例 |
|-----------|-------------|---------|
| MAJOR | 破坏性更改 | `1.0.0` → `2.0.0` |
| MINOR | 新功能（向后兼容） | `1.0.0` → `1.1.0` |
| PATCH | 错误修复（向后兼容） | `1.0.0` → `1.0.1` |
| PRERELEASE | 预发布标识符 | `1.0.0-alpha` |
| BUILD | 构建元数据（比较时忽略） | `1.0.0+build123` |

### 何时递增

| 更改类型 | 递增 | 示例 |
|-------------|-----------|---------|
| 破坏性 API 更改 | MAJOR | 移除函数 |
| 重命名公共函数 | MAJOR | `parse()` → `decode()` |
| 更改函数签名 | MAJOR | 添加必需参数 |
| 添加新函数 | MINOR | 添加 `validate()` |
| 添加可选参数 | MINOR | 新的可选 `options` 参数 |
| 错误修复 | PATCH | 修复空指针 |
| 性能改进 | PATCH | 更快的算法 |
| 内部重构 | PATCH | 无 API 更改 |

## 版本约束

### 约束语法

| 语法 | 含义 | 解析为 |
|--------|---------|-------------|
| `1.2.3` | 精确版本 | 仅 1.2.3 |
| `^1.2.3` | 插入符（兼容） | ≥1.2.3 且 <2.0.0 |
| `~1.2.3` | 波浪号（补丁更新） | ≥1.2.3 且 <1.3.0 |
| `>=1.0.0` | 至少 | 1.0.0 或更高 |
| `>1.0.0` | 大于 | 高于 1.0.0 |
| `<2.0.0` | 小于 | 低于 2.0.0 |
| `<=2.0.0` | 最多 | 2.0.0 或更低 |
| `>=1.0.0 <2.0.0` | 范围 | 在 1.0.0 和 2.0.0 之间 |
| `*` | 任意 | 任意版本 |

### 插入符范围 (^)

插入符（`^`）允许不修改最左边非零数字的更改：

```
^1.2.3  →  >=1.2.3 <2.0.0   # 允许 1.x.x
^0.2.3  →  >=0.2.3 <0.3.0   # 允许 0.2.x
^0.0.3  →  >=0.0.3 <0.0.4   # 仅允许 0.0.3
```

**使用场景：** 你希望在主版本内获得兼容更新。

**最常见的约束** - 推荐用于大多数依赖。

### 波浪号范围 (~)

波浪号（`~`）仅允许补丁级别的更改：

```
~1.2.3  →  >=1.2.3 <1.3.0   # 允许 1.2.x
~1.2    →  >=1.2.0 <1.3.0   # 允许 1.2.x
~1      →  >=1.0.0 <2.0.0   # 允许 1.x.x
```

**使用场景：** 你只希望获得错误修复，不要新功能。

### 比较范围

组合比较运算符进行精确控制：

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### 任意版本 (*)

匹配任意版本：

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**警告：** 不推荐用于生产环境。将始终获取最新版本。

## 预发布版本

### 预发布标识符

预发布版本的优先级低于正式发布版本：

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### 常见预发布标签

| 标签 | 含义 | 阶段 |
|-----|---------|-------|
| `alpha` | 早期开发 | 非常不稳定 |
| `beta` | 功能完整 | 测试中 |
| `rc` | 候选发布 | 最终测试 |
| `dev` | 开发快照 | 不稳定 |

### 约束中的预发布

约束默认不匹配预发布版本：

```
^1.0.0    # 不匹配 1.1.0-beta
>=1.0.0   # 不匹配 2.0.0-alpha
```

要包含预发布版本，请明确引用它们：

```
>=1.0.0-alpha <2.0.0   # 包含所有 1.x 预发布版本
```

## 版本比较

### 比较规则

1. 按数值比较 MAJOR、MINOR、PATCH
2. 发布版本 > 相同版本号的预发布版本
3. 预发布版本按字母数字顺序比较
4. 构建元数据被忽略

### 示例

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # 构建元数据被忽略
```

### 排序

版本按升序排序：

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## 版本解析

### 解析算法

当多个包需要同一个依赖时：

1. 收集所有约束
2. 找到所有范围的交集
3. 选择交集中的最高版本
4. 如果没有版本满足所有约束则报错

### 解析示例

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Intersection: >=1.2.0 <1.3.0
Available: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Resolved: 1.2.5 (highest in intersection)
```

### 冲突检测

当没有版本满足所有约束时发生冲突：

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Intersection: (empty)
Result: CONFLICT - no version satisfies both
```

## 最佳实践

### 对于包使用者

1. **大多数依赖使用插入符范围**：
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **关键依赖使用波浪号范围**：
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **仅在必要时锁定版本**：
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **提交锁定文件**以实现可重现的构建

5. **定期更新**以获取安全修复：
   ```bash
   hpm update
   hpm outdated
   ```

### 对于包作者

1. **初始开发从 0.1.0 开始**：
   - API 可能频繁更改
   - 用户预期不稳定

2. **API 稳定后升级到 1.0.0**：
   - 对稳定性的公开承诺
   - 破坏性更改需要递增主版本

3. **严格遵循 semver**：
   - 破坏性更改 = MAJOR
   - 新功能 = MINOR
   - 错误修复 = PATCH

4. **使用预发布版本进行测试**：
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **在 CHANGELOG 中记录破坏性更改**

## 发布版本

### 创建发布

```bash
# Update version in package.json
# Edit package.json: "version": "1.1.0"

# Commit version change
git add package.json
git commit -m "Bump version to 1.1.0"

# Create and push tag
git tag v1.1.0
git push origin main --tags
```

### 标签格式

标签**必须**以 `v` 开头：

```
v1.0.0      ✓ 正确
v1.0.0-beta ✓ 正确
1.0.0       ✗ 不会被识别
```

### 发布工作流

```bash
# 1. Ensure tests pass
hpm test

# 2. Update version in package.json
# 3. Update CHANGELOG.md
# 4. Commit changes
git add -A
git commit -m "Release v1.2.0"

# 5. Create tag
git tag v1.2.0

# 6. Push everything
git push origin main --tags
```

## 检查版本

### 列出已安装版本

```bash
hpm list
```

### 检查更新

```bash
hpm outdated
```

输出：
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current**：已安装版本
- **Wanted**：符合约束的最高版本
- **Latest**：最新可用版本

### 更新包

```bash
# 更新所有
hpm update

# 更新特定包
hpm update hemlang/json
```

## 另请参阅

- [创建包](creating-packages.md) - 发布指南
- [包规范](package-spec.md) - package.json 格式
- [命令](commands.md) - CLI 参考
