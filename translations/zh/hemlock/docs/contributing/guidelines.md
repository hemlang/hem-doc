# Hemlock 贡献指南

感谢您有兴趣为 Hemlock 做贡献！本指南将帮助您了解如何有效地贡献代码，同时保持语言的设计理念和代码质量。

---

## 目录

- [开始之前](#开始之前)
- [贡献工作流程](#贡献工作流程)
- [代码风格指南](#代码风格指南)
- [应该贡献什么](#应该贡献什么)
- [不应该贡献什么](#不应该贡献什么)
- [常见模式](#常见模式)
- [添加新功能](#添加新功能)
- [代码审查流程](#代码审查流程)

---

## 开始之前

### 必读文档

在贡献之前，请按顺序阅读以下文档：

1. **`/home/user/hemlock/docs/design/philosophy.md`** - 了解 Hemlock 的核心原则
2. **`/home/user/hemlock/docs/design/implementation.md`** - 学习代码库结构
3. **`/home/user/hemlock/docs/contributing/testing.md`** - 了解测试要求
4. **本文档** - 学习贡献指南

### 前置条件

**所需知识：**
- C 编程（指针、内存管理、结构体）
- 编译器/解释器基础（词法分析、语法分析、AST）
- Git 和 GitHub 工作流程
- Unix/Linux 命令行

**所需工具：**
- GCC 或 Clang 编译器
- Make 构建系统
- Git 版本控制
- Valgrind（用于内存泄漏检测）
- 基本的文本编辑器或 IDE

### 沟通渠道

**在哪里提问：**
- GitHub Issues - 错误报告和功能请求
- GitHub Discussions - 一般问题和设计讨论
- Pull Request 评论 - 特定代码反馈

---

## 贡献工作流程

### 1. 查找或创建 Issue

**在编写代码之前：**
- 检查您的贡献是否已有相关 issue
- 如果没有，创建一个描述您想做什么的 issue
- 在开始大型更改之前等待维护者反馈
- 小的错误修复可以跳过此步骤

**良好的 issue 描述包括：**
- 问题陈述（什么损坏或缺失）
- 建议的解决方案（您计划如何修复）
- 示例（展示问题的代码片段）
- 理由（为什么此更改符合 Hemlock 的理念）

### 2. Fork 和 Clone

```bash
# 首先在 GitHub 上 fork 仓库，然后：
git clone https://github.com/YOUR_USERNAME/hemlock.git
cd hemlock
git checkout -b feature/your-feature-name
```

### 3. 进行更改

遵循以下指南：
- 先编写测试（TDD 方法）
- 实现功能
- 确保所有测试通过
- 检查内存泄漏
- 更新文档

### 4. 测试您的更改

```bash
# 运行完整测试套件
make test

# 运行特定测试类别
./tests/run_tests.sh tests/category/

# 检查内存泄漏
valgrind ./hemlock tests/your_test.hml

# 构建并测试
make clean && make && make test
```

### 5. 提交您的更改

**良好的提交消息：**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**提交消息格式：**
- 第一行：简短摘要（最多 50 个字符）
- 空行
- 详细说明（每行 72 个字符换行）
- 引用 issue 编号

### 6. 提交 Pull Request

**提交之前：**
- 在最新的 main 分支上 rebase
- 确保所有测试通过
- 运行 valgrind 检查泄漏
- 如果添加面向用户的功能，更新 CLAUDE.md

**Pull request 描述应包括：**
- 这解决了什么问题
- 如何解决的
- 破坏性更改（如果有）
- 新语法或行为的示例
- 测试覆盖摘要

---

## 代码风格指南

### C 代码风格

**格式化：**
```c
// 使用 4 个空格缩进（不使用制表符）
// 函数使用 K&R 大括号风格
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // 控制结构大括号在同一行
        do_something();
    }
}

// 行长度：最多 100 个字符
// 运算符周围使用空格
int result = (a + b) * c;

// 指针星号与类型一起
char *string;   // 正确
char* string;   // 避免
char * string;  // 避免
```

**命名约定：**
```c
// 函数：小写加下划线
void eval_expression(ASTNode *node);

// 类型：PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// 常量：大写加下划线
#define MAX_BUFFER_SIZE 4096

// 变量：小写加下划线
int item_count;
Value *current_value;

// 枚举：TYPE_PREFIX_NAME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**注释：**
```c
// 单行注释用于简短解释
// 使用完整的句子和正确的大写

/*
 * 多行注释用于较长的解释
 * 对齐星号以提高可读性
 */

/**
 * 函数文档注释
 * @param node - 要评估的 AST 节点
 * @return 评估后的值
 */
Value eval_expr(ASTNode *node);
```

**错误处理：**
```c
// 检查所有 malloc 调用
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Error: Out of memory\n");
    exit(1);
}

// 在错误消息中提供上下文
if (file == NULL) {
    fprintf(stderr, "Error: Failed to open '%s': %s\n",
            filename, strerror(errno));
    exit(1);
}

// 使用有意义的错误消息
// 差：Error: Invalid value
// 好：Error: Expected integer, got string
```

**内存管理：**
```c
// 始终释放您分配的内存
Value *val = value_create_i32(42);
// ... 使用 val
value_free(val);

// 释放后将指针设置为 NULL（防止双重释放）
free(ptr);
ptr = NULL;

// 在注释中记录所有权
// 此函数获取 'value' 的所有权并将释放它
void store_value(Value *value);

// 此函数不获取所有权（调用者必须释放）
Value *get_value(void);
```

### 代码组织

**文件结构：**
```c
// 1. 包含（系统头文件优先，然后是本地头文件）
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. 常量和宏
#define INITIAL_CAPACITY 16

// 3. 类型定义
typedef struct Foo Foo;

// 4. 静态函数声明（内部辅助函数）
static void helper_function(void);

// 5. 公共函数实现
void public_api_function(void)
{
    // 实现
}

// 6. 静态函数实现
static void helper_function(void)
{
    // 实现
}
```

**头文件：**
```c
// 使用头文件保护
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// 前向声明
typedef struct Value Value;

// 头文件中只放公共 API
void public_function(Value *val);

// 记录参数和返回值
/**
 * 评估表达式 AST 节点
 * @param node - 要评估的 AST 节点
 * @param env - 当前环境
 * @return 结果值
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## 应该贡献什么

### 鼓励的贡献

**错误修复：**
- 内存泄漏
- 段错误
- 不正确的行为
- 错误消息改进

**文档：**
- 代码注释
- API 文档
- 用户指南和教程
- 示例程序
- 测试用例文档

**测试：**
- 现有功能的额外测试用例
- 边界情况覆盖
- 已修复错误的回归测试
- 性能基准测试

**小功能添加：**
- 新的内置函数（如果符合理念）
- 字符串/数组方法
- 实用函数
- 错误处理改进

**性能改进：**
- 更快的算法（不改变语义）
- 减少内存使用
- 基准测试套件
- 性能分析工具

**工具：**
- 编辑器语法高亮
- 语言服务器协议（LSP）
- 调试器集成
- 构建系统改进

### 先讨论

**主要功能：**
- 新的语言结构
- 类型系统更改
- 语法添加
- 并发原语

**如何讨论：**
1. 打开 GitHub issue 或 discussion
2. 描述功能和理由
3. 展示示例代码
4. 解释它如何符合 Hemlock 的理念
5. 等待维护者反馈
6. 在实现之前迭代设计

---

## 不应该贡献什么

### 不鼓励的贡献

**不要添加以下功能：**
- 对用户隐藏复杂性
- 使行为隐式或神奇
- 破坏现有语义或语法
- 添加垃圾回收或自动内存管理
- 违反"显式优于隐式"原则

**被拒绝的贡献示例：**

**1. 自动分号插入**
```hemlock
// 差：这会被拒绝
let x = 5  // 没有分号
let y = 10 // 没有分号
```
原因：使语法模糊，隐藏错误

**2. RAII/析构函数**
```hemlock
// 差：这会被拒绝
let f = open("file.txt");
// 文件在作用域结束时自动关闭
```
原因：隐藏资源释放时间，不够显式

**3. 丢失数据的隐式类型转换**
```hemlock
// 差：这会被拒绝
let x: i32 = 3.14;  // 静默截断为 3
```
原因：数据丢失应该是显式的，不是静默的

**4. 垃圾回收**
```c
// 差：这会被拒绝
void *gc_malloc(size_t size) {
    // 跟踪分配以进行自动清理
}
```
原因：隐藏内存管理，性能不可预测

**5. 复杂的宏系统**
```hemlock
// 差：这会被拒绝
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
原因：太多魔法，使代码难以推理

### 常见拒绝原因

**"这太隐式了"**
- 解决方案：使行为显式并记录它

**"这隐藏了复杂性"**
- 解决方案：暴露复杂性但使其符合人体工程学

**"这破坏了现有代码"**
- 解决方案：找到非破坏性替代方案或讨论版本控制

**"这不符合 Hemlock 的理念"**
- 解决方案：重新阅读 philosophy.md 并重新考虑方法

---

## 常见模式

### 错误处理模式

```c
// 在 Hemlock 代码中对可恢复错误使用此模式
Value *divide(Value *a, Value *b)
{
    // 检查前置条件
    if (b->type != TYPE_I32) {
        // 返回错误值或抛出异常
        return create_error("Expected integer divisor");
    }

    if (b->i32_value == 0) {
        return create_error("Division by zero");
    }

    // 执行操作
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### 内存管理模式

```c
// 模式：分配、使用、释放
void process_data(void)
{
    // 分配
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // 使用
    if (buf && str) {
        // ... 执行工作
    }

    // 释放（按分配的相反顺序）
    free(str);
    free_buffer(buf);
}
```

### 值创建模式

```c
// 使用构造函数创建值
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### 类型检查模式

```c
// 在操作之前检查类型
Value *add_values(Value *a, Value *b)
{
    // 类型检查
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Type mismatch");
    }

    // 可以安全进行
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### 字符串构建模式

```c
// 高效构建字符串
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Error: %s (line %d)", detail, line_number);
}
```

---

## 添加新功能

### 功能添加清单

添加新功能时，请遵循以下步骤：

#### 1. 设计阶段

- [ ] 阅读 philosophy.md 以确保一致性
- [ ] 创建描述功能的 GitHub issue
- [ ] 获得维护者对设计的批准
- [ ] 编写规范（语法、语义、示例）
- [ ] 考虑边界情况和错误条件

#### 2. 实现阶段

**如果添加语言结构：**

- [ ] 在 `lexer.h` 中添加 token 类型（如果需要）
- [ ] 在 `lexer.c` 中添加词法规则（如果需要）
- [ ] 在 `ast.h` 中添加 AST 节点类型
- [ ] 在 `ast.c` 中添加 AST 构造函数
- [ ] 在 `parser.c` 中添加解析规则
- [ ] 在 `runtime.c` 或适当的模块中添加运行时行为
- [ ] 在 AST 释放函数中处理清理

**如果添加内置函数：**

- [ ] 在 `builtins.c` 中添加函数实现
- [ ] 在 `register_builtins()` 中注册函数
- [ ] 处理所有参数类型组合
- [ ] 返回适当的错误值
- [ ] 记录参数和返回类型

**如果添加值类型：**

- [ ] 在 `values.h` 中添加类型枚举
- [ ] 向 Value 联合添加字段
- [ ] 在 `values.c` 中添加构造函数
- [ ] 添加到 `value_free()` 进行清理
- [ ] 添加到 `value_copy()` 进行复制
- [ ] 添加到 `value_to_string()` 进行打印
- [ ] 如果是数字类型，添加类型提升规则

#### 3. 测试阶段

- [ ] 编写测试用例（参见 testing.md）
- [ ] 测试成功情况
- [ ] 测试错误情况
- [ ] 测试边界情况
- [ ] 运行完整测试套件（`make test`）
- [ ] 使用 valgrind 检查内存泄漏
- [ ] 在多个平台上测试（如果可能）

#### 4. 文档阶段

- [ ] 使用面向用户的文档更新 CLAUDE.md
- [ ] 添加解释实现的代码注释
- [ ] 在 `examples/` 中创建示例
- [ ] 更新相关的 docs/ 文件
- [ ] 记录任何破坏性更改

#### 5. 提交阶段

- [ ] 清理调试代码和注释
- [ ] 验证代码风格合规性
- [ ] 在最新的 main 上 rebase
- [ ] 创建带有详细描述的 pull request
- [ ] 响应代码审查反馈

### 示例：添加新运算符

让我们以添加取模运算符 `%` 为例：

**1. 词法分析器（lexer.c）：**
```c
// 在 get_next_token() 的 switch 语句中添加
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. 词法分析器头文件（lexer.h）：**
```c
typedef enum {
    // ... 现有 token
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST（ast.h）：**
```c
typedef enum {
    // ... 现有运算符
    OP_MOD,
    // ...
} BinaryOp;
```

**4. 解析器（parser.c）：**
```c
// 添加到 parse_multiplicative() 或适当的优先级级别
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. 运行时（runtime.c）：**
```c
// 添加到 eval_binary_op()
case OP_MOD:
    // 类型检查
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Error: Modulo by zero\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... 处理其他类型组合
    break;
```

**6. 测试（tests/operators/modulo.hml）：**
```hemlock
// 基本取模
print(10 % 3);  // Expect: 2

// 负数取模
print(-10 % 3); // Expect: -1

// 错误情况（应该失败）
// print(10 % 0);  // Division by zero
```

**7. 文档（CLAUDE.md）：**
```markdown
### 算术运算符
- `+` - 加法
- `-` - 减法
- `*` - 乘法
- `/` - 除法
- `%` - 取模（余数）
```

---

## 代码审查流程

### 审查者关注什么

**1. 正确性**
- 代码是否做了它声称的事情？
- 是否处理了边界情况？
- 是否有内存泄漏？
- 是否正确处理了错误？

**2. 理念一致性**
- 这是否符合 Hemlock 的设计原则？
- 是显式的还是隐式的？
- 是否隐藏了复杂性？

**3. 代码质量**
- 代码是否可读和可维护？
- 变量名是否具有描述性？
- 函数大小是否合理？
- 是否有足够的文档？

**4. 测试**
- 是否有足够的测试用例？
- 测试是否覆盖成功和失败路径？
- 是否测试了边界情况？

**5. 文档**
- 面向用户的文档是否已更新？
- 代码注释是否清晰？
- 是否提供了示例？

### 响应反馈

**应该做的：**
- 感谢审查者的时间
- 如果不理解，请提出澄清问题
- 如果不同意，解释您的理由
- 及时进行请求的更改
- 如果范围更改，更新 PR 描述

**不应该做的：**
- 把批评当作个人攻击
- 防御性地争论
- 忽略反馈
- 在审查评论上强制推送（除非 rebase）
- 向 PR 添加不相关的更改

### 让您的 PR 合并

**合并要求：**
- [ ] 所有测试通过
- [ ] 无内存泄漏（valgrind 清洁）
- [ ] 维护者的代码审查批准
- [ ] 文档已更新
- [ ] 遵循代码风格指南
- [ ] 符合 Hemlock 的理念

**时间线：**
- 小型 PR（错误修复）：通常在几天内审查
- 中型 PR（新功能）：可能需要 1-2 周
- 大型 PR（重大更改）：需要广泛讨论

---

## 其他资源

### 学习资源

**理解解释器：**
- "Crafting Interpreters" by Robert Nystrom
- "Writing An Interpreter In Go" by Thorsten Ball
- "Modern Compiler Implementation in C" by Andrew Appel

**C 编程：**
- "The C Programming Language" by K&R
- "Expert C Programming" by Peter van der Linden
- "C Interfaces and Implementations" by David Hanson

**内存管理：**
- Valgrind 文档
- "Understanding and Using C Pointers" by Richard Reese

### 有用的命令

```bash
# 使用调试符号构建
make clean && make CFLAGS="-g -O0"

# 使用 valgrind 运行
valgrind --leak-check=full ./hemlock script.hml

# 运行特定测试类别
./tests/run_tests.sh tests/strings/

# 生成用于代码导航的 tags 文件
ctags -R .

# 查找所有 TODO 和 FIXME
grep -rn "TODO\|FIXME" src/ include/
```

---

## 有问题？

如果您对贡献有疑问：

1. 查看 `docs/` 中的文档
2. 搜索现有的 GitHub issues
3. 在 GitHub Discussions 中提问
4. 用您的问题打开一个新 issue

**感谢您为 Hemlock 做贡献！**
