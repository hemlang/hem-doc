# Hemlock 命令行参数

Hemlock 程序可以通过内置的 **`args` 数组**访问命令行参数，该数组在程序启动时自动填充。

## 目录

- [概述](#概述)
- [args 数组](#args-数组)
- [属性](#属性)
- [迭代模式](#迭代模式)
- [常见用例](#常见用例)
- [参数解析模式](#参数解析模式)
- [最佳实践](#最佳实践)
- [完整示例](#完整示例)

## 概述

`args` 数组提供对传递给 Hemlock 程序的命令行参数的访问：

- **始终可用** - 所有 Hemlock 程序中的内置全局变量
- **包含脚本名称** - `args[0]` 始终包含脚本路径/名称
- **字符串数组** - 所有参数都是字符串
- **从零开始索引** - 标准数组索引（0、1、2、...）

## args 数组

### 基本结构

```hemlock
// args[0] 始终是脚本文件名
// args[1] 到 args[n-1] 是实际参数
print(args[0]);        // "script.hml"
print(args.length);    // 参数总数（包括脚本名称）
```

### 使用示例

**命令：**
```bash
./hemlock script.hml hello world "test 123"
```

**在 script.hml 中：**
```hemlock
print("Script name: " + args[0]);     // "script.hml"
print("Total args: " + typeof(args.length));  // "4"
print("First arg: " + args[1]);       // "hello"
print("Second arg: " + args[2]);      // "world"
print("Third arg: " + args[3]);       // "test 123"
```

### 索引参考

| 索引 | 包含 | 示例值 |
|-------|----------|---------------|
| `args[0]` | 脚本路径/名称 | `"script.hml"` 或 `"./script.hml"` |
| `args[1]` | 第一个参数 | `"hello"` |
| `args[2]` | 第二个参数 | `"world"` |
| `args[3]` | 第三个参数 | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | 最后一个参数 | （不定） |

## 属性

### 始终存在

`args` 是**所有** Hemlock 程序中可用的全局数组：

```hemlock
// 无需声明或导入
print(args.length);  // 立即可用
```

### 包含脚本名称

`args[0]` 始终包含脚本路径/名称：

```hemlock
print("Running: " + args[0]);
```

**args[0] 的可能值：**
- `"script.hml"` - 仅文件名
- `"./script.hml"` - 相对路径
- `"/home/user/script.hml"` - 绝对路径
- 取决于脚本的调用方式

### 类型：字符串数组

所有参数都存储为字符串：

```hemlock
// 参数: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42"（字符串，不是数字）
print(args[2]);  // "3.14"（字符串，不是数字）
print(args[3]);  // "true"（字符串，不是布尔值）

// 根据需要转换：
let num = 42;  // 如需要可手动解析
```

### 最小长度

始终至少为 1（脚本名称）：

```hemlock
print(args.length);  // 最小值: 1
```

**即使没有参数：**
```bash
./hemlock script.hml
```

```hemlock
// 在 script.hml 中：
print(args.length);  // 1（仅脚本名称）
```

### REPL 行为

在 REPL 中，`args.length` 为 0（空数组）：

```hemlock
# REPL 会话
> print(args.length);
0
```

## 迭代模式

### 基本迭代

跳过 `args[0]`（脚本名称）并处理实际参数：

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**对于 `./hemlock script.hml foo bar baz` 的输出：**
```
Argument 1: foo
Argument 2: bar
Argument 3: baz
```

### For-In 迭代（包括脚本名称）

```hemlock
for (let arg in args) {
    print(arg);
}
```

**输出：**
```
script.hml
foo
bar
baz
```

### 检查参数数量

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <argument>");
    // 退出或返回
} else {
    let arg = args[1];
    // 处理 arg
}
```

### 处理除脚本名称外的所有参数

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Processing: " + arg);
}
```

## 常见用例

### 1. 简单参数处理

检查必需参数：

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Processing file: " + filename);
    // ... 处理文件
}
```

**用法：**
```bash
./hemlock script.hml data.txt
# 输出: Processing file: data.txt
```

### 2. 多个参数

```hemlock
if (args.length < 3) {
    print("Usage: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Input: " + input_file);
    print("Output: " + output_file);

    // 处理文件...
}
```

**用法：**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. 可变数量的参数

处理所有提供的参数：

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**用法：**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. 帮助信息

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show this help message");
    print("  -v, --verbose  Enable verbose output");
} else {
    // 正常处理
}
```

### 5. 参数验证

```hemlock
fn validate_file(filename: string): bool {
    // 检查文件是否存在（示例）
    return filename != "";
}

if (args.length < 2) {
    print("Error: No filename provided");
} else if (!validate_file(args[1])) {
    print("Error: Invalid file: " + args[1]);
} else {
    print("Processing: " + args[1]);
}
```

## 参数解析模式

### 命名参数（标志）

命名参数的简单模式：

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Verbose mode enabled");
}
print("Input: " + input_file);
print("Output: " + output_file);
```

**用法：**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### 布尔标志

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### 值参数

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // 需要将字符串解析为整数
        }
    }
    i = i + 1;
}
```

### 混合位置参数和命名参数

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // 作为位置参数处理
        positional.push(args[i]);
    }
    i = i + 1;
}

// 分配位置参数
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### 参数解析器辅助函数

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // 位置参数
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose: " + typeof(opts.verbose));
print("Output: " + opts.output);
print("Files: " + typeof(opts.files.length));
```

## 最佳实践

### 1. 始终检查参数数量

```hemlock
// 好的做法
if (args.length < 2) {
    print("Usage: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// 不好的做法 - 如果没有参数可能会崩溃
process_file(args[1]);  // 如果 args.length == 1 会出错
```

### 2. 提供用法信息

```hemlock
fn show_usage() {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show help");
    print("  -v, --verbose  Verbose output");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. 验证参数

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Error: Missing required argument");
        return false;
    }

    if (args[1] == "") {
        print("Error: Empty argument");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // 退出或显示用法
}
```

### 4. 使用描述性变量名

```hemlock
// 好的做法
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// 不好的做法
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. 处理带空格的引号参数

Shell 会自动处理：

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. 创建参数对象

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Input: " + arguments.input);
```

## 完整示例

### 示例 1：文件处理器

```hemlock
// 用法: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Usage: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Processing " + input + " -> " + output);

    // 处理文件
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // 示例处理
        f_out.write(processed);

        print("Done!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### 示例 2：批量文件处理器

```hemlock
// 用法: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Processing: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // 处理内容...
            print("    " + typeof(content.length) + " bytes");
        } catch (e) {
            print("    Error: " + e);
        }

        i = i + 1;
    }

    print("Done!");
}
```

### 示例 3：高级参数解析器

```hemlock
// 用法: ./hemlock app.hml [OPTIONS] <files...>
// 选项:
//   --verbose, -v     启用详细输出
//   --output, -o FILE 设置输出文件
//   --help, -h        显示帮助

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Error: --output requires a value");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Error: Unknown option: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Usage: " + args[0] + " [OPTIONS] <files...>");
    print("Options:");
    print("  --verbose, -v     Enable verbose output");
    print("  --output, -o FILE Set output file");
    print("  --help, -h        Show this help");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Error: No input files specified");
    show_help();
} else {
    if (config.verbose) {
        print("Verbose mode enabled");
        print("Output file: " + config.output);
        print("Input files: " + typeof(config.files.length));
    }

    // 处理文件
    for (let file in config.files) {
        if (config.verbose) {
            print("Processing: " + file);
        }
        // ... 处理文件
    }
}
```

### 示例 4：配置工具

```hemlock
// 用法: ./hemlock config.hml <action> [arguments]
// 操作:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Usage: " + args[0] + " <action> [arguments]");
    print("Actions:");
    print("  get <key>         Get configuration value");
    print("  set <key> <value> Set configuration value");
    print("  list              List all configuration");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Error: 'get' requires a key");
        } else {
            let key = args[2];
            print("Getting: " + key);
            // ... 从配置获取
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Error: 'set' requires key and value");
        } else {
            let key = args[2];
            let value = args[3];
            print("Setting " + key + " = " + value);
            // ... 设置配置
        }
    } else if (action == "list") {
        print("Listing all configuration:");
        // ... 列出配置
    } else {
        print("Error: Unknown action: " + action);
        show_usage();
    }
}
```

## 总结

Hemlock 的命令行参数支持提供：

- 全局可用的内置 `args` 数组
- 简单的基于数组的参数访问
- 脚本名称在 `args[0]`
- 所有参数都是字符串
- 可用的数组方法（.length、.slice 等）

请记住：
- 访问元素前始终检查 `args.length`
- `args[0]` 是脚本名称
- 实际参数从 `args[1]` 开始
- 所有参数都是字符串 - 根据需要转换
- 为用户友好的工具提供用法信息
- 处理前验证参数

常见模式：
- 简单位置参数
- 命名/标志参数（--flag）
- 值参数（--option value）
- 帮助信息（--help）
- 参数验证
