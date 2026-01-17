# Hemlock 命令执行

Hemlock 提供 **`exec()` 内置函数**来执行 shell 命令并捕获输出。

## 目录

- [概述](#概述)
- [exec() 函数](#exec-函数)
- [结果对象](#结果对象)
- [基本用法](#基本用法)
- [高级示例](#高级示例)
- [错误处理](#错误处理)
- [实现细节](#实现细节)
- [安全考虑](#安全考虑)
- [限制](#限制)
- [用例](#用例)
- [最佳实践](#最佳实践)
- [完整示例](#完整示例)

## 概述

`exec()` 函数允许 Hemlock 程序：
- 执行 shell 命令
- 捕获标准输出（stdout）
- 检查退出状态码
- 使用 shell 特性（管道、重定向等）
- 与系统工具集成

**重要：** 命令通过 `/bin/sh` 执行，提供完整的 shell 功能，但也引入了安全考虑。

## exec() 函数

### 签名

```hemlock
exec(command: string): object
```

**参数：**
- `command` (string) - 要执行的 shell 命令

**返回：** 包含两个字段的对象：
- `output` (string) - 命令的 stdout 输出
- `exit_code` (i32) - 命令的退出状态码

### 基本示例

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## 结果对象

`exec()` 返回的对象具有以下结构：

```hemlock
{
    output: string,      // 命令 stdout（捕获的输出）
    exit_code: i32       // 进程退出状态（0 = 成功）
}
```

### output 字段

包含命令写入 stdout 的所有文本。

**属性：**
- 如果命令没有输出则为空字符串
- 原样包含换行符和空白
- 多行输出保留
- 大小无限制（动态分配）

**示例：**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // 带换行符的目录列表

let r3 = exec("true");
print(r3.output);  // ""（空字符串）
```

### exit_code 字段

命令的退出状态码。

**值：**
- `0` 通常表示成功
- `1-255` 表示错误（约定因命令而异）
- `-1` 如果命令无法执行或异常终止

**示例：**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0（成功）

let r2 = exec("false");
print(r2.exit_code);  // 1（失败）

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2（文件未找到，因命令而异）
```

## 基本用法

### 简单命令

```hemlock
let r = exec("ls -la");
print(r.output);
print("Exit code: " + typeof(r.exit_code));
```

### 检查退出状态

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found: " + r.output);
} else {
    print("Pattern not found");
}
```

### 带管道的命令

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### 多条命令

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### 命令替换

```hemlock
let r = exec("echo $(date)");
print(r.output);  // 当前日期
```

## 高级示例

### 处理失败

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Command failed with code: " + typeof(r.exit_code));
    print("Error output: " + r.output);  // 注意：stderr 未捕获
}
```

### 处理多行输出

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### 命令链

**使用 &&（与）：**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup complete");
}
```

**使用 ||（或）：**
```hemlock
let r = exec("command1 || command2");
// 仅当 command1 失败时运行 command2
```

**使用 ;（顺序）：**
```hemlock
let r = exec("command1; command2");
// 无论成功/失败都运行两者
```

### 使用管道

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**复杂管道：**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### 退出码模式

不同的退出码表示不同的条件：

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
} else if (r.exit_code == 1) {
    print("File does not exist");
} else {
    print("Test command failed: " + typeof(r.exit_code));
}
```

### 输出重定向

```hemlock
// 将 stdout 重定向到文件（在 shell 内）
let r1 = exec("echo 'test' > /tmp/output.txt");

// 将 stderr 重定向到 stdout（注意：Hemlock 仍未捕获 stderr）
let r2 = exec("command 2>&1");
```

### 环境变量

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### 工作目录更改

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## 错误处理

### exec() 何时抛出异常

如果命令无法执行，`exec()` 函数会抛出异常：

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Failed to execute: " + e);
}
```

**抛出异常的情况：**
- `popen()` 失败（如无法创建管道）
- 系统资源限制超出
- 内存分配失败

### exec() 何时不抛出异常

```hemlock
// 命令运行但返回非零退出码
let r1 = exec("false");
print(r1.exit_code);  // 1（不是异常）

// 命令没有输出
let r2 = exec("true");
print(r2.output);  // ""（不是异常）

// shell 找不到命令
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127（不是异常）
```

### 安全执行模式

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Warning: Command failed with code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Error executing command: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## 实现细节

### 工作原理

**底层实现：**
- 使用 `popen()` 通过 `/bin/sh` 执行命令
- 仅捕获 stdout（stderr 未捕获）
- 输出动态缓冲（从 4KB 开始，按需增长）
- 使用 `WIFEXITED()` 和 `WEXITSTATUS()` 宏提取退出状态
- 输出字符串正确以 null 结尾

**进程流程：**
1. `popen(command, "r")` 创建管道并 fork 进程
2. 子进程执行 `/bin/sh -c "command"`
3. 父进程通过管道将 stdout 读入增长的缓冲区
4. `pclose()` 等待子进程并返回退出状态
5. 提取退出状态并存储在结果对象中

### 性能考虑

**开销：**
- 每次调用创建新的 shell 进程（约 1-5ms 开销）
- 输出完全存储在内存中（非流式）
- 不支持流式传输（等待命令完成）
- 适用于输出大小合理的命令

**优化：**
- 缓冲区从 4KB 开始，满时翻倍（高效内存使用）
- 单一读取循环最小化系统调用
- 无额外字符串复制

**何时使用：**
- 短时运行的命令（< 1 秒）
- 中等输出大小（< 10MB）
- 具有合理间隔的批量操作

**何时不使用：**
- 长时运行的守护进程或服务
- 产生 GB 级输出的命令
- 实时流数据处理
- 高频执行（> 100 次/秒）

## 安全考虑

### Shell 注入风险

**关键：** 命令由 shell（`/bin/sh`）执行，这意味着 **shell 注入是可能的**。

**易受攻击的代码：**
```hemlock
// 危险 - 不要这样做
let filename = args[1];  // 用户输入
let r = exec("cat " + filename);  // Shell 注入！
```

**攻击：**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# 执行: cat ; rm -rf /; echo pwned
```

### 安全实践

**1. 永远不要使用未经净化的用户输入：**
```hemlock
// 不好
let user_input = args[1];
let r = exec("process " + user_input);  // 危险

// 好 - 先验证
fn is_safe_filename(name: string): bool {
    // 只允许字母数字、破折号、下划线、点
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Invalid filename");
}
```

**2. 使用白名单，而不是黑名单：**
```hemlock
// 好 - 严格的白名单
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Invalid command");
}
```

**3. 转义特殊字符：**
```hemlock
fn shell_escape(s: string): string {
    // 简单转义 - 用单引号包裹并转义单引号
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. 避免对文件操作使用 exec()：**
```hemlock
// 不好 - 使用 exec 进行文件操作
let r = exec("cat file.txt");

// 好 - 使用 Hemlock 的文件 API
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 权限考虑

命令以与 Hemlock 进程相同的权限运行：

```hemlock
// 如果 Hemlock 以 root 运行，exec() 命令也以 root 运行！
let r = exec("rm -rf /important");  // 如果以 root 运行则危险
```

**最佳实践：** 以所需的最小权限运行 Hemlock。

## 限制

### 1. 无 stderr 捕获

只捕获 stdout，stderr 输出到终端：

```hemlock
let r = exec("ls /nonexistent");
// r.output 为空
// 错误消息出现在终端上，未捕获
```

**变通方法 - 将 stderr 重定向到 stdout：**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// 现在错误消息在 r.output 中
```

### 2. 无流式传输

必须等待命令完成：

```hemlock
let r = exec("long_running_command");
// 阻塞直到命令完成
// 无法增量处理输出
```

### 3. 无超时

命令可以无限期运行：

```hemlock
let r = exec("sleep 1000");
// 阻塞 1000 秒
// 无法超时或取消
```

**变通方法 - 使用 timeout 命令：**
```hemlock
let r = exec("timeout 5 long_command");
// 5 秒后超时
```

### 4. 无信号处理

无法向运行中的命令发送信号：

```hemlock
let r = exec("long_command");
// 无法向命令发送 SIGINT、SIGTERM 等
```

### 5. 无进程控制

启动后无法与命令交互：

```hemlock
let r = exec("interactive_program");
// 无法向程序发送输入
// 无法控制执行
```

## 用例

### 适合的用例

**1. 运行系统工具：**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. 使用 Unix 工具快速处理数据：**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Unique lines: " + r.output);
```

**3. 检查系统状态：**
```hemlock
let r = exec("df -h");
print("Disk usage:\n" + r.output);
```

**4. 文件存在性检查：**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
}
```

**5. 生成报告：**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Running instances: " + count);
```

**6. 自动化脚本：**
```hemlock
exec("git add .");
exec("git commit -m 'Auto commit'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push failed");
}
```

### 不推荐的用例

**1. 长时运行的服务：**
```hemlock
// 不好
let r = exec("nginx");  // 永远阻塞
```

**2. 交互式命令：**
```hemlock
// 不好 - 无法提供输入
let r = exec("ssh user@host");
```

**3. 产生巨大输出的命令：**
```hemlock
// 不好 - 将整个输出加载到内存
let r = exec("cat 10GB_file.log");
```

**4. 实时流式传输：**
```hemlock
// 不好 - 无法增量处理输出
let r = exec("tail -f /var/log/app.log");
```

**5. 关键任务错误处理：**
```hemlock
// 不好 - stderr 未捕获
let r = exec("critical_operation");
// 无法看到详细错误消息
```

## 最佳实践

### 1. 始终检查退出码

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Command failed!");
    // 处理错误
}
```

### 2. 需要时修剪输出

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // 移除尾随换行符
print(clean);  // "test"（无换行符）
```

### 3. 执行前验证

```hemlock
fn is_valid_command(cmd: string): bool {
    // 验证命令是否安全
    return true;  // 你的验证逻辑
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. 对关键操作使用 try/catch

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Command failed";
    }
} catch (e) {
    print("Error: " + e);
    // 清理或恢复
}
```

### 5. 优先使用 Hemlock API 而不是 exec()

```hemlock
// 不好 - 使用 exec 进行文件操作
let r = exec("cat file.txt");

// 好 - 使用 Hemlock 的文件 API
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. 需要时捕获 stderr

```hemlock
// 将 stderr 重定向到 stdout
let r = exec("command 2>&1");
// 现在 r.output 同时包含 stdout 和 stderr
```

### 7. 明智使用 Shell 特性

```hemlock
// 使用管道提高效率
let r = exec("cat large.txt | grep pattern | head -n 10");

// 使用命令替换
let r = exec("echo Current user: $(whoami)");

// 使用条件执行
let r = exec("test -f file.txt && cat file.txt");
```

## 完整示例

### 示例 1：系统信息收集器

```hemlock
fn get_system_info() {
    print("=== System Information ===");

    // 主机名
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // 运行时间
    let r2 = exec("uptime");
    print("Uptime: " + r2.output.trim());

    // 磁盘使用
    let r3 = exec("df -h /");
    print("\nDisk Usage:");
    print(r3.output);

    // 内存使用
    let r4 = exec("free -h");
    print("Memory Usage:");
    print(r4.output);
}

get_system_info();
```

### 示例 2：日志分析器

```hemlock
fn analyze_log(logfile: string) {
    print("Analyzing log: " + logfile);

    // 统计总行数
    let r1 = exec("wc -l " + logfile);
    print("Total lines: " + r1.output.trim());

    // 统计错误数
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Errors: " + errors);
    } else {
        print("Errors: 0");
    }

    // 统计警告数
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Warnings: " + warnings);
    } else {
        print("Warnings: 0");
    }

    // 最近的错误
    print("\nRecent errors:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Usage: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### 示例 3：Git 助手

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Error: Not a git repository");
        return;
    }

    if (r.output == "") {
        print("Working directory clean");
    } else {
        print("Changes:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Adding all changes...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Error adding files");
        return;
    }

    print("Committing...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Error committing");
        return;
    }

    print("Committed successfully");
    print(r2.output);
}

// 用法
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### 示例 4：备份脚本

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Backing up " + source + " to " + dest);

    // 创建备份目录
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Error creating backup directory");
        return false;
    }

    // 创建带时间戳的压缩包
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Creating archive: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Error creating backup:");
        print(r3.output);
        return false;
    }

    print("Backup completed successfully");

    // 显示备份大小
    let r4 = exec("du -h " + backup_file);
    print("Backup size: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Usage: " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## 总结

Hemlock 的 `exec()` 函数提供：

- 简单的 shell 命令执行
- 输出捕获（stdout）
- 退出码检查
- 完整的 shell 特性访问（管道、重定向等）
- 与系统工具的集成

请记住：
- 始终检查退出码
- 注意安全隐患（shell 注入）
- 在命令中使用前验证用户输入
- 可用时优先使用 Hemlock API 而不是 exec()
- stderr 未捕获（使用 `2>&1` 重定向）
- 命令阻塞直到完成
- 用于短时运行的工具，不是长时运行的服务

**安全检查清单：**
- 永远不要使用未经净化的用户输入
- 验证所有输入
- 对命令使用白名单
- 必要时转义特殊字符
- 以最小权限运行
- 优先使用 Hemlock API 而不是 shell 命令
