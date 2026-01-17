# 性能分析

Hemlock 包含一个内置的性能分析器，用于 **CPU 时间分析**、**内存跟踪**和**泄漏检测**。分析器帮助识别程序中的性能瓶颈和内存问题。

## 目录

- [概述](#概述)
- [快速开始](#快速开始)
- [分析模式](#分析模式)
- [输出格式](#输出格式)
- [泄漏检测](#泄漏检测)
- [理解报告](#理解报告)
- [火焰图生成](#火焰图生成)
- [最佳实践](#最佳实践)

---

## 概述

通过 `profile` 子命令访问分析器：

```bash
hemlock profile [OPTIONS] <FILE>
```

**主要特性：**
- **CPU 分析** - 测量每个函数花费的时间（自身时间和总时间）
- **内存分析** - 跟踪所有分配及其源位置
- **泄漏检测** - 识别从未释放的内存
- **多种输出格式** - 文本、JSON 和火焰图兼容的输出
- **每函数内存统计** - 查看哪些函数分配最多内存

---

## 快速开始

### 分析 CPU 时间（默认）

```bash
hemlock profile script.hml
```

### 分析内存分配

```bash
hemlock profile --memory script.hml
```

### 检测内存泄漏

```bash
hemlock profile --leaks script.hml
```

### 生成火焰图数据

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## 分析模式

### CPU 分析（默认）

测量每个函数花费的时间，区分：
- **自身时间** - 执行函数自身代码花费的时间
- **总时间** - 自身时间加上调用的函数花费的时间

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # 显式指定
```

**示例输出：**
```
=== Hemlock Profiler Report ===

Total time: 1.234ms
Functions called: 5 unique

--- Top 5 by Self Time ---

Function                        Self      Total   Calls
--------                        ----      -----   -----
expensive_calc              0.892ms    0.892ms     100  (72.3%)
process_data                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### 内存分析

跟踪所有内存分配（`alloc`、`buffer`、`talloc`、`realloc`）及其源位置。

```bash
hemlock profile --memory script.hml
```

**示例输出：**
```
=== Hemlock Profiler Report ===

Total time: 0.543ms
Functions called: 3 unique
Total allocations: 15 (4.2KB)

--- Top 3 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
allocator                   0.312ms    0.312ms      10      3.2KB         10  (57.5%)
buffer_ops                  0.156ms    0.156ms       5       1KB          5  (28.7%)
main                        0.075ms    0.543ms       1        0B          0  (13.8%)

--- Top 10 Allocation Sites ---

Location                                      Total    Count
--------                                      -----    -----
src/data.hml:42                               1.5KB        5
src/data.hml:67                               1.0KB       10
src/main.hml:15                               512B         1
```

---

### 调用计数模式

最小开销模式，仅计算函数调用（无计时）。

```bash
hemlock profile --calls script.hml
```

---

## 输出格式

### 文本（默认）

带表格的人类可读摘要。

```bash
hemlock profile script.hml
```

---

### JSON

机器可读格式，用于与其他工具集成。

```bash
hemlock profile --json script.hml
```

**示例输出：**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "expensive_calc",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### 火焰图

生成与 [flamegraph.pl](https://github.com/brendangregg/FlameGraph) 兼容的折叠栈格式。

```bash
hemlock profile --flamegraph script.hml > profile.folded

# 使用 flamegraph.pl 生成 SVG
flamegraph.pl profile.folded > profile.svg
```

**折叠输出示例：**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## 泄漏检测

`--leaks` 标志仅显示从未释放的分配，使内存泄漏的识别变得容易。

```bash
hemlock profile --leaks script.hml
```

**有泄漏的示例程序：**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // 泄漏 - 从未释放
    let p2 = alloc(200);    // OK - 下面释放了
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // 正确释放
}

leaky();
clean();
```

**带 --leaks 的输出：**
```
=== Hemlock Profiler Report ===

Total time: 0.034ms
Functions called: 2 unique
Total allocations: 3 (388B)

--- Top 2 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
leaky                       0.021ms    0.021ms       1       300B          2  (61.8%)
clean                       0.013ms    0.013ms       1        88B          1  (38.2%)

--- Memory Leaks (1 site) ---

Location                                     Leaked      Total    Count
--------                                     ------      -----    -----
script.hml:2                                   100B       100B        1
```

泄漏报告显示：
- **Leaked** - 程序退出时当前未释放的字节
- **Total** - 在此位置曾经分配的总字节
- **Count** - 在此位置的分配次数

---

## 理解报告

### 函数统计

| 列 | 描述 |
|------|------|
| Function | 函数名 |
| Self | 函数中花费的时间（不包括被调用者） |
| Total | 包括所有被调用函数的时间 |
| Calls | 函数被调用的次数 |
| Alloc | 此函数分配的总字节数 |
| Count | 此函数的分配次数 |
| (%) | 占程序总时间的百分比 |

### 分配位置

| 列 | 描述 |
|------|------|
| Location | 源文件和行号 |
| Total | 在此位置分配的总字节数 |
| Count | 分配次数 |
| Leaked | 程序退出时仍分配的字节（仅 --leaks） |

### 时间单位

分析器自动选择适当的单位：
- `ns` - 纳秒（< 1微秒）
- `us` - 微秒（< 1毫秒）
- `ms` - 毫秒（< 1秒）
- `s` - 秒

---

## 命令参考

```
hemlock profile [OPTIONS] <FILE>

OPTIONS:
    --cpu           CPU/时间分析（默认）
    --memory        内存分配分析
    --calls         仅调用计数（最小开销）
    --leaks         仅显示未释放的分配（隐含 --memory）
    --json          以 JSON 格式输出
    --flamegraph    以火焰图兼容格式输出
    --top N         显示前 N 条记录（默认：20）
```

---

## 火焰图生成

火焰图可视化程序花费时间的位置，较宽的条表示花费更多时间。

### 生成火焰图

1. 安装 flamegraph.pl：
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. 分析你的程序：
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. 生成 SVG：
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. 在浏览器中打开 `profile.svg` 获得交互式可视化。

### 阅读火焰图

- **X 轴**：总时间的百分比（宽度 = 时间比例）
- **Y 轴**：调用栈深度（底部 = 入口点，顶部 = 叶函数）
- **颜色**：随机，仅用于视觉区分
- **点击**：放大一个函数以查看其被调用者

---

## 最佳实践

### 1. 分析代表性工作负载

使用真实数据和使用模式进行分析。小的测试用例可能无法揭示真正的瓶颈。

```bash
# 好：使用类似生产的数据进行分析
hemlock profile --memory process_large_file.hml large_input.txt

# 不太有用：微小的测试用例
hemlock profile quick_test.hml
```

### 2. 在开发过程中使用 --leaks

定期运行泄漏检测以尽早发现内存泄漏：

```bash
hemlock profile --leaks my_program.hml
```

### 3. 优化前后对比

在优化前后进行分析以测量影响：

```bash
# 优化前
hemlock profile --json script.hml > before.json

# 优化后
hemlock profile --json script.hml > after.json

# 比较结果
```

### 4. 对大型程序使用 --top

限制输出以关注最重要的函数：

```bash
hemlock profile --top 10 large_program.hml
```

### 5. 结合火焰图使用

对于复杂的调用模式，火焰图提供比文本输出更好的可视化：

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## 分析器开销

分析器会给程序执行增加一些开销：

| 模式 | 开销 | 用例 |
|------|------|------|
| `--calls` | 最小 | 仅计算函数调用 |
| `--cpu` | 低 | 一般性能分析 |
| `--memory` | 中等 | 内存分析和泄漏检测 |

为了获得最准确的结果，多次分析并寻找一致的模式。

---

## 另请参阅

- [内存管理](../language-guide/memory.md) - 指针和缓冲区
- [内存 API](../reference/memory-api.md) - alloc、free、buffer 函数
- [异步/并发](async-concurrency.md) - 分析异步代码
