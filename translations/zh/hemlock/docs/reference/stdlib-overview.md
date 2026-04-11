# 标准库概述

Hemlock 附带 53 个标准库模块，涵盖系统编程、I/O、网络、数据格式、并发等。所有模块使用 `@stdlib/` 前缀导入。

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## 模块分类

### 核心工具

| 模块 | 导入 | 描述 |
|------|------|------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | 用于测试和验证的断言工具 |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap、Queue、Stack、Set、LinkedList、LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | 任务检查和栈管理 |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Printf 风格字符串格式化 |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | 迭代器工具（range、enumerate、zip、chain） |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | 带级别和文件输出的结构化日志记录器 |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | 随机数生成和洗牌 |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | 扩展字符串工具（pad、reverse、lines） |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | BDD 风格测试框架（describe、test、expect） |

### 数学与科学

| 模块 | 导入 | 描述 |
|------|------|------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin、cos、sqrt、pow、rand、PI、E、divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed、to_hex、parse_int、parse_float、StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | 稠密矩阵操作（乘法、转置、行列式、逆） |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | 使用 USearch ANN 的向量相似性搜索 |

### 内存与底层

| 模块 | 导入 | 描述 |
|------|------|------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | 竞技场（bump）内存分配器 |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | 原子操作（load、store、add、CAS、fence） |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | 字节交换、端序转换、缓冲区 I/O |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | 内存映射文件 I/O |

### 文件系统与 I/O

| 模块 | 导入 | 描述 |
|------|------|------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | 文件和目录操作（open、read_file、write_file、list_dir） |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | 通过线程池的非阻塞文件 I/O |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | 文件模式匹配 |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | 路径操作（join、dirname、basename、extname） |

### 并发与异步

| 模块 | 导入 | 描述 |
|------|------|------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool、parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | 进程间通信（管道、消息队列） |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | 信号常量和处理（SIGINT、SIGTERM 等） |

### 网络

| 模块 | 导入 | 描述 |
|------|------|------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | HTTP 客户端（get、post、request 带头部） |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | TCP/UDP 套接字（TcpListener、TcpStream、UdpSocket） |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Unix 域套接字（AF_UNIX 流/数据报） |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | URL 解析和操作 |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | WebSocket 客户端 |

### 数据格式

| 模块 | 导入 | 描述 |
|------|------|------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse、stringify、pretty、path 访问 |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | TOML 解析和生成 |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | YAML 解析和生成 |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | CSV 解析和生成 |

### 编码与加密

| 模块 | 导入 | 描述 |
|------|------|------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64、Base32、hex、URL 编码 |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1、SHA-256、SHA-512、MD5、CRC32、DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | AES 加密、RSA 签名、random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip、gunzip、deflate |

### 文本处理

| 模块 | 导入 | 描述 |
|------|------|------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | 正则表达式（POSIX ERE） |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Jinja2 兼容模板渲染 |

### 日期、时间与版本

| 模块 | 导入 | 描述 |
|------|------|------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | DateTime 类、格式化、解析 |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | 时间戳、sleep、时钟测量 |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | 语义化版本解析和比较 |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | UUID v4 和 v7 生成 |

### 系统与环境

| 模块 | 导入 | 描述 |
|------|------|------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | 命令行参数解析 |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | 环境变量、exit、get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | 平台检测、CPU 数量、主机名 |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork、exec、wait、kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Shell 命令执行和参数转义 |

### 终端与 UI

| 模块 | 导入 | 描述 |
|------|------|------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | ANSI 颜色、样式和光标控制 |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | 原始终端输入和按键检测 |

### 数据库

| 模块 | 导入 | 描述 |
|------|------|------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | SQLite 数据库、query、exec、事务 |

### FFI 与互操作

| 模块 | 导入 | 描述 |
|------|------|------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | FFI 回调管理和类型常量 |

### 工具

| 模块 | 导入 | 描述 |
|------|------|------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | 带指数退避的重试逻辑 |

---

## 快速示例

### 读取和解析配置文件

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connecting to " + db_host);
```

### 带 JSON 的 HTTP 请求

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### 并发处理

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### 哈希和编码

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### 模板渲染

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Home", "About", "Contact"] });
```

---

## 另请参阅

- [内置函数参考](./builtins.md) — 无需导入即可使用的函数
- [迁移指南 (v2.0)](../migration-2.0.md) — v2.0 中移到 stdlib 的内置函数
- 各模块文档在 [`stdlib/docs/`](../../stdlib/docs/)
