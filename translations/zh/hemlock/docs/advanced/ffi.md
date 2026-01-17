# Hemlock 外部函数接口（FFI）

Hemlock 提供 **FFI（外部函数接口）**，可使用 libffi 调用共享库中的 C 函数，实现与现有 C 库和系统 API 的集成。

## 目录

- [概述](#概述)
- [当前状态](#当前状态)
- [支持的类型](#支持的类型)
- [基本概念](#基本概念)
- [导出 FFI 函数](#导出-ffi-函数)
- [用例](#用例)
- [未来发展](#未来发展)
- [FFI 回调](#ffi-回调)
- [FFI 结构体](#ffi-结构体)
- [当前限制](#当前限制)
- [最佳实践](#最佳实践)

## 概述

外部函数接口（FFI）允许 Hemlock 程序：
- 从共享库（.so、.dylib、.dll）调用 C 函数
- 使用现有 C 库而无需编写包装代码
- 直接访问系统 API
- 与第三方原生库集成
- 将 Hemlock 与底层系统功能桥接

**关键能力：**
- 动态库加载
- C 函数绑定
- Hemlock 和 C 类型之间的自动类型转换
- 支持所有原始类型
- 基于 libffi 的实现，具有可移植性

## 当前状态

Hemlock 中的 FFI 支持具有以下特性：

**已实现：**
- 从共享库调用 C 函数
- 支持所有原始类型（整数、浮点数、指针）
- 自动类型转换
- 基于 libffi 的实现
- 动态库加载
- **函数指针回调** - 将 Hemlock 函数传递给 C
- **导出 extern 函数** - 跨模块共享 FFI 绑定
- **结构体传递和返回值** - 按值传递 C 兼容的结构体
- **完整的指针辅助函数** - 读写所有类型（i8-i64, u8-u64, f32, f64, ptr）
- **缓冲区/指针转换** - `buffer_ptr()`、`ptr_to_buffer()`
- **FFI 类型大小** - `ffi_sizeof()` 用于平台感知的类型大小
- **平台类型** - 支持 `size_t`、`usize`、`isize`、`intptr_t`

**开发中：**
- 字符串封送辅助函数
- 错误处理改进

## 支持的类型

### 原始类型

以下 Hemlock 类型可以传递给 C 函数或从 C 函数返回：

| Hemlock 类型 | C 类型 | 大小 | 说明 |
|--------------|--------|------|------|
| `i8` | `int8_t` | 1 字节 | 有符号 8 位整数 |
| `i16` | `int16_t` | 2 字节 | 有符号 16 位整数 |
| `i32` | `int32_t` | 4 字节 | 有符号 32 位整数 |
| `i64` | `int64_t` | 8 字节 | 有符号 64 位整数 |
| `u8` | `uint8_t` | 1 字节 | 无符号 8 位整数 |
| `u16` | `uint16_t` | 2 字节 | 无符号 16 位整数 |
| `u32` | `uint32_t` | 4 字节 | 无符号 32 位整数 |
| `u64` | `uint64_t` | 8 字节 | 无符号 64 位整数 |
| `f32` | `float` | 4 字节 | 32 位浮点数 |
| `f64` | `double` | 8 字节 | 64 位浮点数 |
| `ptr` | `void*` | 8 字节 | 原始指针 |

### 类型转换

**自动转换：**
- Hemlock 整数 -> C 整数（带范围检查）
- Hemlock 浮点数 -> C 浮点数
- Hemlock 指针 -> C 指针
- C 返回值 -> Hemlock 值

**示例类型映射：**
```hemlock
// Hemlock -> C
let i: i32 = 42;         // -> int32_t (4 字节)
let f: f64 = 3.14;       // -> double (8 字节)
let p: ptr = alloc(64);  // -> void* (8 字节)

// C -> Hemlock（返回值）
// int32_t foo() -> i32
// double bar() -> f64
// void* baz() -> ptr
```

## 基本概念

### 共享库

FFI 与编译后的共享库配合使用：

**Linux:** `.so` 文件
```
libexample.so
/usr/lib/libm.so
```

**macOS:** `.dylib` 文件
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** `.dll` 文件
```
example.dll
kernel32.dll
```

### 函数签名

C 函数必须具有已知的签名才能让 FFI 正常工作：

```c
// 示例 C 函数签名
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

一旦加载库并绑定函数，就可以从 Hemlock 调用这些函数。

### 平台兼容性

FFI 使用 **libffi** 实现可移植性：
- 适用于 x86、x86-64、ARM、ARM64
- 自动处理调用约定
- 抽象平台特定的 ABI 细节
- 支持 Linux、macOS、Windows（需要适当的 libffi）

## 导出 FFI 函数

使用 `extern fn` 声明的 FFI 函数可以从模块导出，允许您创建可跨多个文件共享的可重用库包装器。

### 基本导出语法

```hemlock
// string_utils.hml - 包装 C 字符串函数的库模块
import "libc.so.6";

// 直接导出 extern 函数
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// 您也可以在 extern 函数旁边导出包装函数
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### 导入导出的 FFI 函数

```hemlock
// main.hml - 使用导出的 FFI 函数
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hello, World!";
print(strlen(msg));           // 13 - 直接 extern 调用
print(string_length(msg));    // 13 - 包装函数

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### Export Extern 的用例

**1. 平台抽象**
```hemlock
// platform.hml - 抽象平台差异
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. 库包装器**
```hemlock
// crypto_lib.hml - 包装加密库函数
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// 添加 Hemlock 友好的包装器
export fn sha256_string(s: string): string {
    // 使用 extern 函数的实现
}
```

**3. 集中式 FFI 声明**
```hemlock
// libc.hml - libc 绑定的中央模块
import "libc.so.6";

// 字符串函数
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// 内存函数
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// 进程函数
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

然后在整个项目中使用：
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

## 用例

### 1. 系统库

访问标准 C 库函数：

**数学函数：**
```hemlock
// 从 libm 调用 sqrt
let result = sqrt(16.0);  // 4.0
```

**内存分配：**
```hemlock
// 从 libc 调用 malloc/free
let ptr = malloc(1024);
free(ptr);
```

### 2. 第三方库

使用现有的 C 库：

**示例：图像处理**
```hemlock
// 加载 libpng 或 libjpeg
// 使用 C 库函数处理图像
```

**示例：加密**
```hemlock
// 使用 OpenSSL 或 libsodium
// 通过 FFI 进行加密/解密
```

### 3. 系统 API

直接系统调用：

**示例：POSIX API**
```hemlock
// 调用 getpid、getuid 等
// 访问底层系统功能
```

### 4. 性能关键代码

调用优化的 C 实现：

```hemlock
// 使用高度优化的 C 库
// SIMD 操作、向量化代码
// 硬件加速函数
```

## FFI 回调

Hemlock 支持使用 libffi 闭包将函数作为回调传递给 C 代码。这使得能够与期望函数指针的 C API 集成，如 `qsort`、事件循环和基于回调的库。

### 创建回调

使用 `callback()` 从 Hemlock 函数创建 C 可调用的函数指针：

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**参数：**
- `function`：要包装的 Hemlock 函数
- `param_types`：类型名称字符串数组（如 `["ptr", "i32"]`）
- `return_type`：返回类型字符串（如 `"i32"`、`"void"`）

**支持的回调类型：**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - 有符号整数
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - 无符号整数
- `"f32"`, `"f64"` - 浮点数
- `"ptr"` - 指针
- `"void"` - 无返回值
- `"bool"` - 布尔值

### 示例：qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// 整数比较函数（升序）
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// 分配 5 个整数的数组
let arr = alloc(20);  // 5 * 4 字节
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// 创建回调并排序
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// 数组现在已排序：[1, 2, 5, 8, 9]

// 清理
callback_free(cmp);
free(arr);
```

### 指针辅助函数

Hemlock 提供全面的辅助函数用于处理原始指针。这些对于 FFI 回调和直接内存操作至关重要。

#### 整数类型辅助函数

| 函数 | 描述 |
|------|------|
| `ptr_deref_i8(ptr)` | 解引用指针，读取 i8 |
| `ptr_deref_i16(ptr)` | 解引用指针，读取 i16 |
| `ptr_deref_i32(ptr)` | 解引用指针，读取 i32 |
| `ptr_deref_i64(ptr)` | 解引用指针，读取 i64 |
| `ptr_deref_u8(ptr)` | 解引用指针，读取 u8 |
| `ptr_deref_u16(ptr)` | 解引用指针，读取 u16 |
| `ptr_deref_u32(ptr)` | 解引用指针，读取 u32 |
| `ptr_deref_u64(ptr)` | 解引用指针，读取 u64 |
| `ptr_write_i8(ptr, value)` | 向指针位置写入 i8 |
| `ptr_write_i16(ptr, value)` | 向指针位置写入 i16 |
| `ptr_write_i32(ptr, value)` | 向指针位置写入 i32 |
| `ptr_write_i64(ptr, value)` | 向指针位置写入 i64 |
| `ptr_write_u8(ptr, value)` | 向指针位置写入 u8 |
| `ptr_write_u16(ptr, value)` | 向指针位置写入 u16 |
| `ptr_write_u32(ptr, value)` | 向指针位置写入 u32 |
| `ptr_write_u64(ptr, value)` | 向指针位置写入 u64 |

#### 浮点类型辅助函数

| 函数 | 描述 |
|------|------|
| `ptr_deref_f32(ptr)` | 解引用指针，读取 f32 (float) |
| `ptr_deref_f64(ptr)` | 解引用指针，读取 f64 (double) |
| `ptr_write_f32(ptr, value)` | 向指针位置写入 f32 |
| `ptr_write_f64(ptr, value)` | 向指针位置写入 f64 |

#### 指针类型辅助函数

| 函数 | 描述 |
|------|------|
| `ptr_deref_ptr(ptr)` | 解引用指向指针的指针 |
| `ptr_write_ptr(ptr, value)` | 向指针位置写入指针 |
| `ptr_offset(ptr, index, size)` | 计算偏移：`ptr + index * size` |
| `ptr_read_i32(ptr)` | 通过指向指针的指针读取 i32（用于 qsort 回调） |
| `ptr_null()` | 获取空指针常量 |

#### 缓冲区转换辅助函数

| 函数 | 描述 |
|------|------|
| `buffer_ptr(buffer)` | 从缓冲区获取原始指针 |
| `ptr_to_buffer(ptr, size)` | 从指针复制数据到新缓冲区 |

#### FFI 实用函数

| 函数 | 描述 |
|------|------|
| `ffi_sizeof(type_name)` | 获取 FFI 类型的字节大小 |

**`ffi_sizeof` 支持的类型名称：**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - 有符号整数（1, 2, 4, 8 字节）
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - 无符号整数（1, 2, 4, 8 字节）
- `"f32"`, `"f64"` - 浮点数（4, 8 字节）
- `"ptr"` - 指针（64 位系统上 8 字节）
- `"size_t"`, `"usize"` - 平台相关的大小类型
- `"intptr_t"`, `"isize"` - 平台相关的有符号指针类型

### 释放回调

**重要：** 始终在使用完回调后释放它们以防止内存泄漏：

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ... 使用回调 ...
callback_free(cb);  // 使用完后释放
```

程序退出时回调也会自动释放。

### 回调中的闭包

回调捕获其闭包环境，因此可以访问外部作用域变量：

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // 可以访问外部作用域的 'multiplier'
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### 线程安全

回调调用通过互斥锁序列化以确保线程安全，因为 Hemlock 解释器不是完全线程安全的。这意味着：
- 一次只能执行一个回调
- 可以安全地与多线程 C 库一起使用
- 如果回调从多个线程频繁调用，可能影响性能

### 回调中的错误处理

在回调中抛出的异常无法传播到 C 代码。相反：
- 向 stderr 打印警告
- 回调返回默认值（0 或 NULL）
- 异常被记录但不传播

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Something went wrong";  // 打印警告，返回 0
}
```

为了健壮的错误处理，请验证输入并避免在回调中抛出异常。

## FFI 结构体

Hemlock 支持按值向 C 函数传递结构体。当您使用类型注解定义结构体时，结构体类型会自动为 FFI 注册。

### 定义 FFI 兼容的结构体

当所有字段都具有使用 FFI 兼容类型的显式类型注解时，结构体就是 FFI 兼容的：

```hemlock
// FFI 兼容的结构体
define Point {
    x: f64,
    y: f64,
}

// 具有多种字段类型的 FFI 兼容结构体
define Rectangle {
    top_left: Point,      // 嵌套结构体
    width: f64,
    height: f64,
}

// 不是 FFI 兼容的（字段没有类型注解）
define DynamicObject {
    name,                 // 没有类型 - 不能用于 FFI
    value,
}
```

### 在 FFI 中使用结构体

声明使用结构体类型的 extern 函数：

```hemlock
// 定义结构体类型
define Vector2D {
    x: f64,
    y: f64,
}

// 导入 C 库
import "libmath.so";

// 声明接受/返回结构体的 extern 函数
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// 自然地使用它
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### 支持的字段类型

结构体字段必须使用以下 FFI 兼容类型：

| Hemlock 类型 | C 类型 | 大小 |
|--------------|--------|------|
| `i8` | `int8_t` | 1 字节 |
| `i16` | `int16_t` | 2 字节 |
| `i32` | `int32_t` | 4 字节 |
| `i64` | `int64_t` | 8 字节 |
| `u8` | `uint8_t` | 1 字节 |
| `u16` | `uint16_t` | 2 字节 |
| `u32` | `uint32_t` | 4 字节 |
| `u64` | `uint64_t` | 8 字节 |
| `f32` | `float` | 4 字节 |
| `f64` | `double` | 8 字节 |
| `ptr` | `void*` | 8 字节 |
| `string` | `char*` | 8 字节 |
| `bool` | `int` | 可变 |
| 嵌套结构体 | struct | 可变 |

### 结构体布局

Hemlock 使用平台的原生结构体布局规则（匹配 C ABI）：
- 字段按其类型对齐
- 根据需要插入填充
- 总大小填充以对齐最大成员

```hemlock
// 示例：C 兼容布局
define Mixed {
    a: i8,    // 偏移 0，大小 1
              // 3 字节填充
    b: i32,   // 偏移 4，大小 4
}
// 总大小：8 字节（包含填充）

define Point3D {
    x: f64,   // 偏移 0，大小 8
    y: f64,   // 偏移 8，大小 8
    z: f64,   // 偏移 16，大小 8
}
// 总大小：24 字节（不需要填充）
```

### 嵌套结构体

结构体可以包含其他结构体：

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### 结构体返回值

C 函数可以返回结构体：

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### 限制

- **结构体字段必须有类型注解** - 没有类型的字段不是 FFI 兼容的
- **结构体中没有数组** - 改用指针
- **没有联合体** - 仅支持结构体类型
- **回调不能返回结构体** - 回调返回值使用指针

## 当前限制

FFI 有以下限制：

**1. 手动类型转换**
- 必须手动管理字符串转换
- 没有自动的 Hemlock 字符串 <-> C 字符串转换

**2. 有限的错误处理**
- 基本错误报告
- 回调中的异常无法传播到 C

**3. 手动库加载**
- 必须手动加载库
- 没有自动绑定生成

**4. 平台特定代码**
- 库路径因平台而异
- 必须处理 .so vs .dylib vs .dll

## 最佳实践

虽然全面的 FFI 文档仍在开发中，以下是一般的最佳实践：

### 1. 类型安全

```hemlock
// 明确类型
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. 内存管理

```hemlock
// 记住释放分配的内存
let ptr = c_malloc(1024);
// ... 使用 ptr
c_free(ptr);
```

### 3. 错误检查

```hemlock
// 检查返回值
let result = c_function();
if (result == null) {
    print("C function failed");
}
```

### 4. 平台兼容性

```hemlock
// 处理平台差异
// 使用适当的库扩展名（.so、.dylib、.dll）
```

## 总结

Hemlock 的 FFI 提供：

- 从共享库调用 C 函数
- 原始类型支持（i8-i64, u8-u64, f32, f64, ptr）
- 自动类型转换
- 基于 libffi 的可移植性
- 原生库集成基础
- **函数指针回调** - 将 Hemlock 函数传递给 C
- **导出 extern 函数** - 跨模块共享 FFI 绑定
- **结构体传递和返回** - 按值传递 C 兼容的结构体
- **导出 define** - 跨模块共享结构体类型定义（自动全局导入）
- **完整的指针辅助函数** - 读写所有类型（i8-i64, u8-u64, f32, f64, ptr）
- **缓冲区/指针转换** - 用于数据封送的 `buffer_ptr()`、`ptr_to_buffer()`
- **FFI 类型大小** - 平台感知类型大小的 `ffi_sizeof()`
- **平台类型** - 支持 `size_t`、`usize`、`isize`、`intptr_t`、`uintptr_t`

**当前状态：** FFI 功能完备，支持原始类型、结构体、回调、模块导出和完整的指针辅助函数

**未来：** 字符串封送辅助函数

**用例：** 系统库、第三方库、qsort、事件循环、基于回调的 API、可重用的库包装器
