# 提案：`@stdlib/vector` — 向量相似性搜索模块

**状态：** 探索 / RFC
**日期：** 2026-02-07

---

## 摘要

添加 `@stdlib/vector` 模块，提供进程内向量相似性搜索（最近邻查找）。这使得基于嵌入向量的搜索、推荐系统和 AI/ML 工作流可以直接从 Hemlock 中进行，无需外部服务器。

---

## 评估的选项

针对以下标准评估了十个向量数据库/库选项：

| 标准 | 权重 | 理由 |
|------|------|------|
| C API 质量 | 关键 | Hemlock FFI 需要 C 链接（`extern fn`）到 `.so` 库 |
| 可嵌入（进程内） | 关键 | Hemlock stdlib 模块是库，不是客户端-服务器协议 |
| 依赖权重 | 高 | 首选最小依赖（像 sqlite 一样——只需一个 `.so`） |
| API 简洁性 | 高 | Hemlock 重视显式、小型 API |
| 性能 | 中 | 对 1M+ 向量足够好；不需要十亿级规模 |
| 持久化 | 中 | 保存/加载索引到磁盘 |
| 许可证 | 中 | 必须是宽松许可（Apache-2.0、MIT、BSD） |

### 结果

| 选项 | C API | 可嵌入 | 依赖 | 性能 | 结论 |
|------|-------|--------|------|------|------|
| **USearch** | C99 一等支持 | 是 | 零 | HNSW + SIMD | **首选** |
| **sqlite-vec** | 通过 SQL | 是 | 零（纯 C） | 暴力搜索 | **备选** |
| hnswlib | 仅 C++ | 是 | 零 | HNSW | 无 C API——跳过 |
| FAISS | C API (faiss_c) | 是 | 需要 BLAS | 最先进 | 太重 |
| pgvector | 不适用 | 否（需要 PG） | PostgreSQL | 好 | 需要服务器——跳过 |
| Qdrant | 无 | 否（服务器） | 重 | 优秀 | 需要服务器——跳过 |
| Milvus | C++ SDK | 否（分布式） | 非常重 | 优秀 | 分布式系统——跳过 |
| Annoy | 仅 C++ | 是 | 零 | 中等 | 过时，无 C API |
| LanceDB | 仅社区 C | 是 | 中等（Rust） | 好 | 无官方 C API |
| ChromaDB | 无 | 有限 | 重 | 中等 | 无 C API |

---

## 推荐：USearch（首选）+ sqlite-vec（轻量替代）

### 为什么不用 pgvector

pgvector 需要运行中的 PostgreSQL 服务器。Hemlock 的 stdlib 模块是通过 FFI（`import "libfoo.so"`）加载的可嵌入库，不是客户端-服务器协议。要求用户安装、配置和运行 PostgreSQL 来进行向量搜索与 stdlib 模式根本不匹配。sqlite 模块之所以可行，恰恰是因为 SQLite 是进程内库，零服务器需求。

### 首选：USearch（`libusearch_c.so`）

[USearch](https://github.com/unum-cloud/USearch) 是一个开源（Apache-2.0）向量相似性搜索库，具有一等 C99 API。它使用 HNSW（分层可导航小世界）算法和 SIMD 优化。

**为什么 USearch 适合 Hemlock：**

1. **C99 API 直接映射到 Hemlock FFI。** 模式与 `@stdlib/sqlite` 相同：
   ```hemlock
   import "libusearch_c.so";
   extern fn usearch_init(options: ptr, error: ptr): ptr;
   extern fn usearch_add(index: ptr, key: i64, vector: ptr, kind: i32, error: ptr): void;
   extern fn usearch_search(index: ptr, query: ptr, kind: i32, count: i64,
                            keys: ptr, distances: ptr, error: ptr): i64;
   ```

2. **零强制依赖。** 编译为单个 `.so`，无需 BLAS、LAPACK 或其他外部依赖。

3. **进程内且可持久化。** 内存映射文件支持——索引保存到磁盘，加载时无需全部读入 RAM。

4. **小型、显式 API。** 约 20 个 C 函数，覆盖：init、add、search、remove、save、load、free。符合 Hemlock 的"显式优于隐式"理念。

5. **生产验证。** 被 ScyllaDB 和 YugabyteDB 用于向量索引。截至 2026 年 1 月为 v2.23+。

6. **高性能。** HNSW 算法 + SIMD（AVX-512、NEON）。支持 f32、f64、f16 和 int8 量化。可在进程内处理数百万向量。

### 备选：sqlite-vec（`@stdlib/sqlite` 的扩展）

[sqlite-vec](https://github.com/asg017/sqlite-vec) 是一个 SQLite 扩展，通过 SQL 提供向量搜索。可通过现有 `@stdlib/sqlite` 模块的 `sqlite3_load_extension()` 加载，无需新的 FFI 绑定。

**与 USearch 的权衡：**

| | USearch | sqlite-vec |
|---|---------|-----------|
| 安装 | 新的 `.so` | SQLite 扩展 `.so` |
| API | 专用 Hemlock 函数 | 通过现有 sqlite 模块的 SQL 查询 |
| 算法 | HNSW（近似） | 暴力搜索（精确） |
| 规模 | 数百万向量 | ~100K 向量 |
| 新代码 | 新 stdlib 模块 | 现有 sqlite 模块的小扩展 |
| 召回率 | 近似（可调） | 100% 精确 |

sqlite-vec 对于已有 `@stdlib/sqlite` 的小数据集是好的"开箱即用"选项。USearch 是超出原型规模时的正确选择。

---

## 提议的 API 设计（`@stdlib/vector`）

遵循 `@stdlib/sqlite`（FFI 包装器 + Hemlock 惯用 API）建立的模式：

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// 创建索引
let idx = create_index(dimensions: 384, metric: "cosine");

// 添加向量（键 + 浮点数组）
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// 搜索 k 个最近邻
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// 返回：[{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// 持久化
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// 带过滤的搜索（带谓词）
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;  // 只匹配 key > 100 的
});

// 信息
print(idx.size());       // 向量数量
print(idx.dimensions()); // 维度
print(idx.contains(42)); // 成员检查

// 清理
idx.remove(2);
idx.free();
```

### 模块导出

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // 内存映射，只读

VectorIndex.add(key, vector)
VectorIndex.search(query, k?)
VectorIndex.search_filtered(query, k?, filter)
VectorIndex.remove(key)
VectorIndex.contains(key)
VectorIndex.count()
VectorIndex.size()
VectorIndex.dimensions()
VectorIndex.save(path)
VectorIndex.free()

distance(a, b, metric?)  // 独立距离计算

// 距离度量
METRIC_COSINE
METRIC_L2SQ       // 欧几里得（L2 平方）
METRIC_IP          // 内积（点积）
METRIC_HAMMING
METRIC_JACCARD

// 标量类型
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

### 系统要求

```
# Debian/Ubuntu
sudo apt install libusearch-dev

# 从源代码
git clone https://github.com/unum-cloud/usearch
cd usearch && cmake -B build && cmake --build build
sudo cmake --install build
```

---

## 实施计划

1. **编写 FFI 绑定** — USearch C API 的 `extern fn` 声明（约 20 个函数）
2. **实现 Hemlock 包装器** — `create_index()`、`VectorIndex` define 及方法
3. **处理内存** — 向量数据编组的适当 `alloc`/`free`、错误字符串清理
4. **添加文档** — `stdlib/docs/vector.md`，遵循 sqlite.md 模式
5. **添加测试** — `tests/stdlib_vector/`，基本 CRUD、持久化、搜索准确性
6. **添加对等测试** — 如果使用的 FFI 模式需要编译器支持

预估范围：~400-600 行 Hemlock（与 `sqlite.hml` 的 968 行相当，但 API 表面更简单）。

---

## 待解决问题

1. **模块名称：** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`？
2. **sqlite-vec 集成：** 作为 `@stdlib/sqlite` 的一部分（扩展加载）还是单独模块？
3. **量化 API：** 暴露 USearch 的 int8/f16 量化，还是默认 f32 保持简单？
4. **批量操作：** 添加 `add_batch()` / `search_batch()` 用于批量操作，还是保持单项 API？
5. **索引配置：** 暴露多少 USearch 的 HNSW 调优（connectivity、expansion factors）？
