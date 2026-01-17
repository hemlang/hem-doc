# 错误处理

Hemlock 通过 `try`、`catch`、`finally`、`throw` 和 `panic` 支持基于异常的错误处理。本指南涵盖了使用异常处理可恢复错误以及使用 panic 处理不可恢复错误的内容。

## 概述

```hemlock
// 基本错误处理
try {
    risky_operation();
} catch (e) {
    print("Error: " + e);
}

// 带清理操作
try {
    process_file();
} catch (e) {
    print("Failed: " + e);
} finally {
    cleanup();
}

// 抛出错误
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### 语法

**基本 try/catch：**
```hemlock
try {
    // 有风险的代码
} catch (e) {
    // 处理错误，e 包含抛出的值
}
```

**Try/finally：**
```hemlock
try {
    // 有风险的代码
} finally {
    // 始终执行，即使抛出异常
}
```

**Try/catch/finally：**
```hemlock
try {
    // 有风险的代码
} catch (e) {
    // 处理错误
} finally {
    // 清理代码
}
```

### Try 块

try 块按顺序执行语句：

```hemlock
try {
    print("Starting...");
    risky_operation();
    print("Success!");  // 仅在没有异常时执行
}
```

**行为：**
- 按顺序执行语句
- 如果抛出异常：跳转到 `catch` 或 `finally`
- 如果没有异常：执行 `finally`（如果存在）然后继续

### Catch 块

catch 块接收抛出的值：

```hemlock
try {
    throw "oops";
} catch (error) {
    print("Caught: " + error);  // error = "oops"
    // error 只能在这里访问
}
// error 在这里无法访问
```

**Catch 参数：**
- 接收抛出的值（任意类型）
- 作用域仅限于 catch 块
- 可以命名为任何名称（通常使用 `e`、`err` 或 `error`）

**在 catch 中可以做的事情：**
```hemlock
try {
    risky_operation();
} catch (e) {
    // 记录错误
    print("Error: " + e);

    // 重新抛出相同错误
    throw e;

    // 抛出不同错误
    throw "different error";

    // 返回默认值
    return null;

    // 处理并继续
    // （不重新抛出）
}
```

### Finally 块

finally 块**始终执行**：

```hemlock
try {
    print("1: try");
    throw "error";
} catch (e) {
    print("2: catch");
} finally {
    print("3: finally");  // 始终运行
}
print("4: after");

// 输出：1: try, 2: catch, 3: finally, 4: after
```

**finally 何时运行：**
- 在 try 块之后（如果没有异常）
- 在 catch 块之后（如果捕获了异常）
- 即使 try/catch 包含 `return`、`break` 或 `continue`
- 在控制流退出 try/catch 之前

**Finally 与 return：**
```hemlock
fn example() {
    try {
        return 1;  // 在 finally 运行后返回 1
    } finally {
        print("cleanup");  // 在返回之前运行
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // finally 的 return 覆盖原值 - 返回 2
    }
}
```

**Finally 与控制流：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // 在 finally 运行后 break
        }
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

## Throw 语句

### 基本 Throw

抛出任意值作为异常：

```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
throw ["error", "details"];
```

**执行过程：**
1. 计算表达式
2. 立即跳转到最近的 `catch`
3. 如果没有 `catch`，向上传播调用栈

### 抛出错误

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "Age cannot be negative";
    }
    if (age > 150) {
        throw "Age is unrealistic";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Validation error: " + e);
}
```

### 抛出错误对象

创建结构化的错误信息：

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "File does not exist"
        };
    }
    // ... 读取文件
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("File not found: " + e.path);
    }
}
```

### 重新抛出

捕获并重新抛出错误：

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Logging error: " + e);
        throw e;  // 重新抛给调用者
    }
}

try {
    wrapper();
} catch (e) {
    print("Caught in main: " + e);
}
```

## 未捕获的异常

如果异常传播到调用栈顶部而未被捕获：

```hemlock
fn foo() {
    throw "uncaught!";
}

foo();  // 崩溃并显示：Runtime error: uncaught!
```

**行为：**
- 程序崩溃
- 向 stderr 打印错误消息
- 以非零状态码退出
- 堆栈跟踪将在未来版本中添加

## Panic - 不可恢复错误

### 什么是 Panic？

`panic()` 用于**不可恢复的错误**，应立即终止程序：

```hemlock
panic();                    // 默认消息："panic!"
panic("custom message");    // 自定义消息
panic(42);                  // 非字符串值会被打印
```

**语义：**
- **立即退出**程序，退出码为 1
- 向 stderr 打印错误消息：`panic: <message>`
- **无法**通过 try/catch 捕获
- 用于 bug 和不可恢复的错误

### Panic vs Throw

```hemlock
// throw - 可恢复错误（可以被捕获）
try {
    throw "recoverable error";
} catch (e) {
    print("Caught: " + e);  // 成功捕获
}

// panic - 不可恢复错误（无法被捕获）
try {
    panic("unrecoverable error");  // 程序立即退出
} catch (e) {
    print("This never runs");       // 永远不会执行
}
```

### 何时使用 Panic

**使用 panic 的情况：**
- **Bug**：到达了不应该到达的代码
- **无效状态**：检测到数据结构损坏
- **不可恢复错误**：关键资源不可用
- **断言失败**：当 `assert()` 不够用时

**示例：**
```hemlock
// 不可达代码
fn process_state(state: i32) {
    if (state == 1) {
        return "ready";
    } else if (state == 2) {
        return "running";
    } else if (state == 3) {
        return "stopped";
    } else {
        panic("invalid state: " + typeof(state));  // 不应该发生
    }
}

// 关键资源检查
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json not found - cannot start");
    }
    // ...
}

// 数据结构不变量
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() called on empty stack");
    }
    return stack.pop();
}
```

### 何时不使用 Panic

**以下情况使用 throw：**
- 用户输入验证
- 文件未找到
- 网络错误
- 预期的错误条件

```hemlock
// 不好：对预期错误使用 panic
fn divide(a, b) {
    if (b == 0) {
        panic("division by zero");  // 太严厉了
    }
    return a / b;
}

// 好：对预期错误使用 throw
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";  // 可恢复
    }
    return a / b;
}
```

## 控制流交互

### Try/Catch/Finally 中的 Return

```hemlock
fn example() {
    try {
        return 1;  // 在 finally 运行后返回 1
    } finally {
        print("cleanup");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // finally 的 return 覆盖 try 的 return - 返回 2
    }
}
```

**规则：** finally 块的返回值会覆盖 try/catch 的返回值。

### Try/Catch/Finally 中的 Break/Continue

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // 在 finally 运行后 break
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

**规则：** break/continue 在 finally 块之后执行。

### 嵌套 Try/Catch

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Caught: " + e);  // 打印：Caught: inner
        throw "outer";  // 重新抛出不同错误
    }
} catch (e) {
    print("Caught: " + e);  // 打印：Caught: outer
}
```

**规则：** 嵌套的 try/catch 块按预期工作，内层 catch 先执行。

## 常见模式

### 模式：资源清理

始终使用 `finally` 进行清理：

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Error processing file: " + e);
    } finally {
        if (file != null) {
            file.close();  // 即使出错也会关闭
        }
    }
}
```

### 模式：错误包装

用上下文包装底层错误：

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Failed to load config from " + path + ": " + e;
    }
}
```

### 模式：错误恢复

出错时提供回退值：

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "division by zero";
        }
        return a / b;
    } catch (e) {
        print("Error: " + e);
        return null;  // 回退值
    }
}
```

### 模式：验证

使用异常进行验证：

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Name is required";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Invalid age";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Invalid email";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "invalid" });
} catch (e) {
    print("Validation failed: " + e);
}
```

### 模式：多种错误类型

使用错误对象区分错误类型：

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Data is null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Expected array" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Array is empty" };
    }

    // ... 处理
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("No data provided");
    } else if (e.type == "TypeError") {
        print("Wrong data type: " + e.message);
    } else {
        print("Error: " + e.message);
    }
}
```

## 最佳实践

1. **对异常情况使用异常** - 不要用于正常控制流
2. **抛出有意义的错误** - 使用带上下文的字符串或对象
3. **始终使用 finally 进行清理** - 确保资源被释放
4. **不要捕获后忽略** - 至少记录错误
5. **适当时重新抛出** - 如果你无法处理，让调用者处理
6. **对 bug 使用 panic** - 对不可恢复的错误使用 panic
7. **文档化异常** - 明确说明哪些函数可能抛出异常

## 常见陷阱

### 陷阱：吞掉错误

```hemlock
// 不好：静默失败
try {
    risky_operation();
} catch (e) {
    // 错误被忽略 - 静默失败
}

// 好：记录或处理
try {
    risky_operation();
} catch (e) {
    print("Operation failed: " + e);
    // 适当处理
}
```

### 陷阱：Finally 覆盖

```hemlock
// 不好：finally 覆盖返回值
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // 返回 0，而不是 42！
    }
}

// 好：不要在 finally 中返回
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // 只做清理，不返回
    }
}
```

### 陷阱：忘记清理

```hemlock
// 不好：出错时文件可能不会关闭
fn process() {
    let file = open("data.txt");
    let content = file.read();  // 可能抛出异常
    file.close();  // 如果出错永远不会到达
}

// 好：使用 finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### 陷阱：对预期错误使用 Panic

```hemlock
// 不好：对预期错误使用 panic
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Config file not found");  // 太严厉了
    }
    return read_file(path);
}

// 好：对预期错误使用 throw
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Config file not found: " + path;  // 可恢复
    }
    return read_file(path);
}
```

## 示例

### 示例：基本错误处理

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Error: " + e);  // 打印：Error: division by zero
}
```

### 示例：资源管理

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("File copied successfully");
    } catch (e) {
        print("Failed to copy file: " + e);
        throw e;  // 重新抛出
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### 示例：嵌套错误处理

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Failed to process user: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Processed: " + typeof(success_count) + " success, " + typeof(error_count) + " errors");
}
```

### 示例：自定义错误类型

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a must be a number", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b must be a number", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Cannot divide by zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### 示例：重试逻辑

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // 成功！
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation failed after " + typeof(max_attempts) + " attempts: " + e;
            }
            print("Attempt " + typeof(attempt) + " failed, retrying...");
        }
    }
}

fn unreliable_operation() {
    // 模拟不稳定的操作
    if (random() < 0.7) {
        throw "Operation failed";
    }
    return "Success";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("All retries failed: " + e);
}
```

## 执行顺序

理解执行顺序：

```hemlock
try {
    print("1: try block start");
    throw "error";
    print("2: never reached");
} catch (e) {
    print("3: catch block");
} finally {
    print("4: finally block");
}
print("5: after try/catch/finally");

// 输出：
// 1: try block start
// 3: catch block
// 4: finally block
// 5: after try/catch/finally
```

## 当前限制

- **没有堆栈跟踪** - 未捕获的异常不显示堆栈跟踪（已计划）
- **某些内置函数会退出** - 某些内置函数仍然使用 `exit()` 而不是抛出异常（待审查）
- **没有自定义异常类型** - 任何值都可以被抛出，但没有正式的异常层次结构

## 相关主题

- [函数](functions.md) - 异常和函数返回
- [控制流](control-flow.md) - 异常如何影响控制流
- [内存](memory.md) - 使用 finally 进行内存清理

## 另请参阅

- **异常语义**：参见 CLAUDE.md 中的"错误处理"部分
- **Panic vs Throw**：不同错误类型的不同用例
- **Finally 保证**：始终执行，即使有 return/break/continue
