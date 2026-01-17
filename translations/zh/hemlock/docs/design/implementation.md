# Hemlock 实现细节

本文档描述了 Hemlock 语言的技术实现，包括项目结构、编译流水线、运行时架构和设计决策。

---

## 目录

- [项目结构](#项目结构)
- [编译流水线](#编译流水线)
- [模块化解释器设计](#模块化解释器设计)
- [运行时架构](#运行时架构)
- [值表示](#值表示)
- [类型系统实现](#类型系统实现)
- [内存管理](#内存管理)
- [并发模型](#并发模型)
- [未来计划](#未来计划)

---

## 项目结构

```
hemlock/
├── src/
│   ├── frontend/              # 共享：词法分析器、解析器、AST
│   │   ├── lexer.c            # 词法分析
│   │   ├── parser/            # 递归下降解析器
│   │   ├── ast.c              # AST 节点管理
│   │   └── module.c           # 模块解析
│   ├── backends/
│   │   ├── interpreter/       # hemlock：树遍历解释器
│   │   │   ├── main.c         # CLI 入口点
│   │   │   ├── runtime.c      # 表达式/语句求值
│   │   │   ├── builtins.c     # 内置函数
│   │   │   └── ...
│   │   └── compiler/          # hemlockc：C 代码生成器
│   │       ├── main.c         # CLI、编排
│   │       ├── type_check.c   # 编译时类型检查
│   │       ├── codegen.c      # 代码生成上下文
│   │       ├── codegen_expr.c # 表达式代码生成
│   │       ├── codegen_stmt.c # 语句代码生成
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # 语言服务器协议
│   │   └── bundler/           # 打包/包工具
├── runtime/                   # libhemlock_runtime.a（用于编译后的程序）
├── stdlib/                    # 标准库（39 个模块）
│   └── docs/                  # 模块文档
├── tests/
│   ├── parity/                # 必须在两个后端都通过的测试
│   ├── interpreter/           # 解释器特定测试
│   └── compiler/              # 编译器特定测试
├── examples/                  # 示例程序
└── docs/                      # 文档
```

### 目录组织

**`include/`** - 定义组件间接口的公共 API 头文件：
- 词法分析器、解析器、AST 和解释器之间的清晰分离
- 前向声明以最小化依赖
- 用于在其他程序中嵌入 Hemlock 的公共 API

**`src/`** - 实现文件：
- 顶层文件处理词法分析、解析、AST 管理
- `main.c` 提供 CLI 和 REPL
- 解释器模块化为独立的子系统

**`src/interpreter/`** - 模块化解释器实现：
- 每个模块有单一、清晰的职责
- 内部 API 在 `internal.h` 中定义用于模块间通信
- 模块可以独立编译以加快构建速度

**`tests/`** - 全面的测试套件：
- 按功能区域组织
- 每个目录包含专注的测试用例
- `run_tests.sh` 编排测试执行

---

## 编译流水线

Hemlock 使用传统的编译流水线，具有不同的阶段：

### 阶段 1：词法分析（Lexer）

**输入：**源代码文本
**输出：**Token 流
**实现：**`src/lexer.c`

```
源码: "let x = 42;"
   ↓
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**主要特性：**
- 识别关键字、标识符、字面量、运算符、标点符号
- 处理 UTF-8 字符串字面量和 rune 字面量
- 报告行号用于错误消息
- 单遍，无回溯

### 阶段 2：语法分析（Parser）

**输入：**Token 流
**输出：**抽象语法树（AST）
**实现：**`src/parser.c`

```
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST: LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**主要特性：**
- 递归下降解析器
- 构建程序结构的树表示
- 处理运算符优先级
- 验证语法（大括号、分号等）
- 还没有语义分析（在运行时完成）

**运算符优先级（从低到高）：**
1. 赋值：`=`
2. 逻辑或：`||`
3. 逻辑与：`&&`
4. 按位或：`|`
5. 按位异或：`^`
6. 按位与：`&`
7. 相等：`==`、`!=`
8. 比较：`<`、`>`、`<=`、`>=`
9. 位移：`<<`、`>>`
10. 加法/减法：`+`、`-`
11. 乘法/除法/取模：`*`、`/`、`%`
12. 一元：`!`、`-`、`~`
13. 调用/索引/成员：`()`、`[]`、`.`

### 阶段 3a：解释执行（树遍历）

**输入：**AST
**输出：**程序执行
**实现：**`src/backends/interpreter/runtime.c`

```
AST: LetStmt { ... }
   ↓
执行: 递归求值 AST 节点
   ↓
结果: 创建值为 42 的变量 x
```

**主要特性：**
- 直接 AST 遍历（树遍历解释器）
- 运行时动态类型检查
- 基于环境的变量存储

### 阶段 3b：编译（hemlockc）

**输入：**AST
**输出：**通过 C 代码生成的原生可执行文件
**实现：**`src/backends/compiler/`

```
AST: LetStmt { ... }
   ↓
类型检查: 编译时验证类型
   ↓
C 代码生成: 生成等效的 C 代码
   ↓
GCC: 将 C 编译为原生二进制文件
   ↓
结果: 独立可执行文件
```

**主要特性：**
- 编译时类型检查（默认启用）
- C 代码生成以实现可移植性
- 链接 `libhemlock_runtime.a`
- 比解释器执行速度显著更快

---

## 编译器后端（hemlockc）

Hemlock 编译器从 AST 生成 C 代码，然后使用 GCC 编译为原生可执行文件。

### 编译器架构

```
src/backends/compiler/
├── main.c              # CLI、参数解析、编排
├── codegen.c           # 核心代码生成上下文
├── codegen_expr.c      # 表达式代码生成
├── codegen_stmt.c      # 语句代码生成
├── codegen_call.c      # 函数调用生成
├── codegen_closure.c   # 闭包实现
├── codegen_program.c   # 顶层程序生成
├── codegen_module.c    # 模块/导入处理
├── type_check.c        # 编译时类型检查
└── type_check.h        # 类型检查器 API
```

### 类型检查

编译器包含统一的类型检查系统，可以：

1. **编译时验证类型** - 在执行前捕获类型错误
2. **支持动态代码** - 无类型代码视为 `any`（始终有效）
3. **提供优化提示** - 识别可以拆箱的变量

**类型检查标志：**

| 标志 | 描述 |
|------|-------------|
| （默认） | 启用类型检查 |
| `--check` | 仅类型检查，不编译 |
| `--no-type-check` | 禁用类型检查 |
| `--strict-types` | 对隐式 `any` 类型发出警告 |

**类型检查器实现：**

```c
// type_check.h - 关键结构
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // 优化提示
    // ... 类型环境、定义等
} TypeCheckContext;

// 主入口点
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### 代码生成

代码生成阶段将 AST 节点转换为 C 代码：

**表达式映射：**
```
Hemlock                 →  生成的 C
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  带环境捕获的闭包
```

**运行时集成：**

生成的 C 代码链接 `libhemlock_runtime.a`，它提供：
- `HmlValue` 标记联合类型
- 内存管理（引用计数）
- 内置函数（print、typeof 等）
- 并发原语（任务、通道）
- FFI 支持

### 拆箱优化

类型检查器识别可以使用原生 C 类型而不是装箱 `HmlValue` 的变量：

**可拆箱模式：**
- 已知整数类型的循环计数器
- 循环中的累加器变量
- 带显式类型注解的变量（i32、i64、f64、bool）

```hemlock
// 循环计数器 'i' 可以拆箱为原生 int32_t
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    sum = sum + i;
}
```

---

## 模块化解释器设计

解释器被分割成专注的模块以提高可维护性和可扩展性。

### 模块职责

#### 1. 环境（`environment.c`）- 121 行

**目的：**变量作用域和名称解析

**关键函数：**
- `env_create()` - 创建带可选父级的新环境
- `env_define()` - 在当前作用域定义新变量
- `env_get()` - 在当前或父作用域查找变量
- `env_set()` - 更新现有变量值
- `env_free()` - 释放环境及所有变量

**设计：**
- 链式作用域（每个环境有指向父级的指针）
- HashMap 用于快速变量查找
- 支持闭包的词法作用域

#### 2. 值（`values.c`）- 394 行

**目的：**值构造函数和数据结构管理

**关键函数：**
- `value_create_*()` - 每种值类型的构造函数
- `value_copy()` - 深拷贝/浅拷贝逻辑
- `value_free()` - 清理和内存释放
- `value_to_string()` - 用于打印的字符串表示

**数据结构：**
- 对象（动态字段数组）
- 数组（动态调整大小）
- 缓冲区（ptr + length + capacity）
- 闭包（函数 + 捕获的环境）
- 任务和通道（并发原语）

#### 3. 类型（`types.c`）- 440 行

**目的：**类型系统、转换和鸭子类型

**关键函数：**
- `type_check()` - 运行时类型验证
- `type_convert()` - 隐式类型转换/提升
- `duck_type_check()` - 对象的结构类型检查
- `type_name()` - 获取可打印的类型名称

**特性：**
- 类型提升层次（i8 → i16 → i32 → i64 → f32 → f64，i64/u64 + f32 → f64）
- 数值类型的范围检查
- 对象类型定义的鸭子类型
- 可选字段默认值

#### 4. 内置函数（`builtins.c`）- 955 行

**目的：**内置函数和全局注册

**关键函数：**
- `register_builtins()` - 注册所有内置函数和常量
- 内置函数实现（print、typeof、alloc、free 等）
- 信号处理函数
- 命令执行（exec）

**内置函数类别：**
- I/O：print、open、read_file、write_file
- 内存：alloc、free、memset、memcpy、realloc
- 类型：typeof、assert
- 并发：spawn、join、detach、channel
- 系统：exec、signal、raise、panic
- FFI：dlopen、dlsym、dlcall、dlclose

#### 5. I/O（`io.c`）- 449 行

**目的：**文件 I/O 和 JSON 序列化

**关键函数：**
- 文件对象方法（read、write、seek、tell、close）
- JSON 序列化/反序列化
- 循环引用检测

**特性：**
- 带属性的文件对象（path、mode、closed）
- UTF-8 感知的文本 I/O
- 二进制 I/O 支持
- 对象和数组的 JSON 往返

#### 6. FFI（`ffi.c`）- 外部函数接口

**目的：**从共享库调用 C 函数

**关键函数：**
- `dlopen()` - 加载共享库
- `dlsym()` - 按名称获取函数指针
- `dlcall()` - 调用带类型转换的 C 函数
- `dlclose()` - 卸载库

**特性：**
- 与 libffi 集成用于动态函数调用
- 自动类型转换（Hemlock ↔ C 类型）
- 支持所有原始类型
- 指针和缓冲区支持

#### 7. 运行时（`runtime.c`）- 865 行

**目的：**表达式求值和语句执行

**关键函数：**
- `eval_expr()` - 求值表达式（递归）
- `eval_stmt()` - 执行语句
- 控制流处理（if、while、for、switch 等）
- 异常处理（try/catch/finally/throw）

**特性：**
- 递归表达式求值
- 短路布尔求值
- 方法调用检测和 `self` 绑定
- 异常传播
- break/continue/return 处理

### 模块化设计的好处

**1. 关注点分离**
- 每个模块有一个清晰的职责
- 容易找到特性的实现位置
- 减少更改时的认知负担

**2. 更快的增量构建**
- 只有修改的模块需要重新编译
- 可能进行并行编译
- 开发期间更短的迭代时间

**3. 更容易的测试和调试**
- 模块可以独立测试
- 错误定位到特定子系统
- 可能使用模拟实现进行测试

**4. 可扩展性**
- 新特性可以添加到适当的模块
- 模块可以独立重构
- 每个文件的代码量保持可管理

**5. 代码组织**
- 相关功能的逻辑分组
- 清晰的依赖图
- 新贡献者更容易上手

---

## 运行时架构

### 值表示

Hemlock 中的所有值都由使用标记联合的 `Value` 结构表示：

```c
typedef struct Value {
    ValueType type;  // 运行时类型标签
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**设计决策：**
- **标记联合**用于类型安全同时保持灵活性
- **运行时类型标签**启用带类型检查的动态类型
- **直接值存储**用于原始类型（无装箱）
- **指针存储**用于堆分配类型（字符串、对象、数组）

### 内存布局示例

**整数（i32）：**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- 总大小：约 16 字节（8 字节标签 + 8 字节联合）
- 栈分配
- 不需要堆分配

**字符串：**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // 指向堆的指针
}

堆: "hello\0"（6 字节，以 null 结尾的 UTF-8）
```
- 值在栈上占 16 字节
- 字符串数据是堆分配的
- 必须手动释放

**对象：**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // 指向堆的指针
}

堆: Object {
    type_name: "Person",
    fields: [
        { name: "name", value: Value{TYPE_STRING, "Alice"} },
        { name: "age", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- 对象结构在堆上
- 字段存储在动态数组中
- 字段值是嵌入的 Value 结构

### 环境实现

变量存储在环境链中：

```c
typedef struct Environment {
    HashMap *bindings;           // name → Value
    struct Environment *parent;  // 词法父作用域
} Environment;
```

**作用域链示例：**
```
全局作用域: { print: <builtin>, args: <array> }
    ↑
函数作用域: { x: 10, y: 20 }
    ↑
块作用域: { i: 0 }
```

**查找算法：**
1. 检查当前环境的 hashmap
2. 如果未找到，检查父环境
3. 重复直到找到或到达全局作用域
4. 如果在任何作用域都未找到则报错

---

## 类型系统实现

### 类型检查策略

Hemlock 使用**运行时类型检查**和**可选类型注解**：

```hemlock
let x = 42;           // 无类型检查，推断为 i32
let y: u8 = 255;      // 运行时检查：值必须适合 u8
let z: i32 = x + y;   // 运行时检查 + 类型提升
```

**实现流程：**
1. **字面量推断** - 词法分析器/解析器从字面量确定初始类型
2. **类型注解检查** - 如果存在注解，在赋值时验证
3. **提升** - 二元操作提升到公共类型
4. **转换** - 显式转换按需发生

### 类型提升实现

类型提升遵循固定层次并保持精度：

```c
// 简化的提升逻辑
ValueType promote_types(ValueType a, ValueType b) {
    // f64 始终获胜
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 与 i64/u64 提升到 f64（精度保持）
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // 较大的整数类型获胜
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**类型等级：**
- i8: 0
- u8: 1
- i16: 2
- u16: 3
- i32: 4
- u32: 5
- i64: 6
- u64: 7
- f32: 8
- f64: 9

### 鸭子类型实现

对象类型检查使用结构比较：

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // 检查所有必需字段
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // 缺少字段
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // 类型错误
        }
    }

    return true;  // 所有必需字段存在且类型正确
}
```

**鸭子类型允许：**
- 对象中的额外字段（被忽略）
- 子结构类型（对象可以有比要求更多的）
- 验证后的类型名称分配

---

## 内存管理

### 分配策略

Hemlock 使用**手动内存管理**，有两种分配原语：

**1. 原始指针（`ptr`）：**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }
    return ptr;
}
```
- 直接 malloc/free
- 无跟踪
- 用户负责释放

**2. 缓冲区（`buffer`）：**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- 跟踪大小和容量
- 访问时边界检查
- 仍然需要手动 free

### 堆分配类型

**字符串：**
- 堆上的 UTF-8 字节数组
- 以 null 结尾用于 C 互操作
- 可变（可以原地修改）
- 引用计数（作用域退出时自动释放）

**对象：**
- 动态字段数组
- 字段名和值在堆上
- 引用计数（作用域退出时自动释放）
- 可能存在循环引用（用 visited-set 跟踪处理）

**数组：**
- 动态容量倍增增长
- 元素是嵌入的 Value 结构
- 增长时自动重新分配
- 引用计数（作用域退出时自动释放）

**闭包：**
- 通过引用捕获环境
- 环境是堆分配的
- 闭包环境在不再引用时正确释放

---

## 并发模型

### 线程架构

Hemlock 使用 POSIX 线程（pthreads）的 **1:1 线程**模型：

```
用户任务          操作系统线程          CPU 核心
---------          ---------          --------
spawn(f1) ------>  pthread_create --> Core 0
spawn(f2) ------>  pthread_create --> Core 1
spawn(f3) ------>  pthread_create --> Core 2
```

**主要特征：**
- 每个 `spawn()` 创建一个新的 pthread
- 内核在核心间调度线程
- 真正的并行执行（没有 GIL）
- 抢占式多任务

### 任务实现

```c
typedef struct Task {
    pthread_t thread;        // 操作系统线程句柄
    Value result;            // 返回值
    char *error;             // 异常消息（如果抛出）
    pthread_mutex_t lock;    // 保护状态
    TaskState state;         // RUNNING、FINISHED、ERROR
} Task;
```

**任务生命周期：**
1. `spawn(func, args)` → 创建 Task，启动 pthread
2. 线程用参数运行函数
3. 返回时：存储结果，设置状态为 FINISHED
4. 异常时：存储错误消息，设置状态为 ERROR
5. `join(task)` → 等待线程，返回结果或抛出异常

### 通道实现

```c
typedef struct Channel {
    void **buffer;           // Value* 的循环缓冲区
    size_t capacity;         // 最大缓冲项目数
    size_t count;            // 缓冲区中的当前项目数
    size_t read_index;       // 下一个读取位置
    size_t write_index;      // 下一个写入位置
    bool closed;             // 通道关闭标志
    pthread_mutex_t lock;    // 保护缓冲区
    pthread_cond_t not_full; // 有空间时发信号
    pthread_cond_t not_empty;// 有数据时发信号
} Channel;
```

**发送操作：**
1. 锁定 mutex
2. 如果缓冲区满则等待（cond_wait on not_full）
3. 将值写入 buffer[write_index]
4. 递增 write_index（循环）
5. 信号 not_empty
6. 解锁 mutex

**接收操作：**
1. 锁定 mutex
2. 如果缓冲区空则等待（cond_wait on not_empty）
3. 从 buffer[read_index] 读取值
4. 递增 read_index（循环）
5. 信号 not_full
6. 解锁 mutex

**同步保证：**
- 线程安全的 send/recv（由 mutex 保护）
- 阻塞语义（满时生产者等待，空时消费者等待）
- 有序交付（通道内 FIFO）

---

## 未来计划

### 已完成：编译器后端

编译器后端（`hemlockc`）已实现：
- 从 AST 生成 C 代码
- 编译时类型检查（默认启用）
- 运行时库（`libhemlock_runtime.a`）
- 与解释器完全一致（98% 测试通过率）
- 拆箱优化框架

### 当前重点：类型系统增强

**最近改进：**
- 统一的类型检查和类型推断系统
- 编译时类型检查默认启用
- 用于仅类型验证的 `--check` 标志
- 传递给代码生成的类型上下文用于优化提示

### 未来增强

**可能的添加：**
- 泛型/模板
- 模式匹配
- LSP 集成用于类型感知的 IDE 支持
- 更激进的拆箱优化
- 用于栈分配的逃逸分析

### 长期优化

**可能的改进：**
- 方法调用的内联缓存
- 热代码路径的 JIT 编译
- 用于更好并发的工作窃取调度器
- 配置文件引导的优化

---

## 实现指南

### 添加新特性

实现新特性时，遵循以下指南：

**1. 选择正确的模块：**
- 新值类型 → `values.c`
- 类型转换 → `types.c`
- 内置函数 → `builtins.c`
- I/O 操作 → `io.c`
- 控制流 → `runtime.c`

**2. 更新所有层：**
- 如需要添加 AST 节点类型（`ast.h`、`ast.c`）
- 如需要添加词法分析器 token（`lexer.c`）
- 添加解析器规则（`parser.c`）
- 实现运行时行为（`runtime.c` 或适当的模块）
- 添加测试（`tests/`）

**3. 保持一致性：**
- 遵循现有代码风格
- 使用一致的命名约定
- 在头文件中记录公共 API
- 保持错误消息清晰一致

**4. 彻底测试：**
- 实现前添加测试用例
- 测试成功和错误路径
- 测试边界情况
- 验证没有内存泄漏（valgrind）

### 性能考虑

**当前瓶颈：**
- 变量访问的 HashMap 查找
- 递归函数调用（没有 TCO）
- 字符串连接（每次分配新字符串）
- 每次操作的类型检查开销

**优化机会：**
- 缓存变量位置（内联缓存）
- 尾调用优化
- 用于连接的字符串构建器
- 类型推断以跳过运行时检查

### 调试技巧

**有用的工具：**
- `valgrind` - 内存泄漏检测
- `gdb` - 调试崩溃
- `-g` 标志 - 调试符号
- `printf` 调试 - 简单但有效

**常见问题：**
- 段错误 → 空指针解引用（检查返回值）
- 内存泄漏 → 缺少 free() 调用（检查 value_free 路径）
- 类型错误 → 检查 type_convert() 和 type_check() 逻辑
- 线程崩溃 → 竞争条件（检查 mutex 使用）

---

## 总结

Hemlock 的实现优先考虑：
- **模块化** - 清晰的关注点分离
- **简单性** - 直接的实现
- **显式性** - 没有隐藏的魔法
- **可维护性** - 易于理解和修改

当前的树遍历解释器有意保持简单，以促进快速特性开发和实验。未来的编译器后端将在保持相同语义的同时提高性能。
