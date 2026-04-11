# 提案：`@stdlib/vector` -- ベクトル類似性検索モジュール

**ステータス：** 探索 / RFC
**日付：** 2026-02-07

---

## 概要

インプロセスのベクトル類似性検索（最近傍探索）を提供する`@stdlib/vector`モジュールを追加。外部サーバーを必要とせず、Hemlockから直接、埋め込みベースの検索、推薦システム、AI/MLワークフローを実現する。

---

## 評価したオプション

10個のベクトルデータベース/ライブラリオプションを以下の基準で評価：

| 基準 | 重要度 | 根拠 |
|----------|--------|-----------|
| C API品質 | 必須 | Hemlock FFIはCリンケージ（`extern fn`）で`.so`ライブラリが必要 |
| 埋め込み可能（インプロセス） | 必須 | Hemlock stdlibモジュールはライブラリであり、クライアント-サーバープロトコルではない |
| 依存関係の重さ | 高 | 最小限の依存関係が望ましい（sqliteのように単一の`.so`） |
| APIのシンプルさ | 高 | Hemlockは明示的で小さなAPIを重視 |
| パフォーマンス | 中 | 100万+ベクトルで十分な性能、10億規模は不要 |
| 永続化 | 中 | インデックスのディスク保存/読み込み |
| ライセンス | 中 | パーミッシブ（Apache-2.0、MIT、BSD）が必要 |

### 結果

| オプション | C API | 埋め込み可能 | 依存関係 | パフォーマンス | 結論 |
|--------|-------|------------|------|-------------|---------|
| **USearch** | C99ファーストクラス | はい | ゼロ | HNSW + SIMD | **プライマリ** |
| **sqlite-vec** | SQL経由 | はい | ゼロ（純粋C） | ブルートフォース | **セカンダリ** |
| hnswlib | C++のみ | はい | ゼロ | HNSW | C APIなし -- スキップ |
| FAISS | C API (faiss_c) | はい | BLAS必須 | 最先端 | 重すぎる |
| pgvector | N/A | いいえ（PG必要） | PostgreSQL | 良好 | サーバー必須 -- スキップ |

---

## 推奨：USearch（プライマリ）+ sqlite-vec（軽量代替）

### pgvectorをなぜ選ばないか

pgvectorには実行中のPostgreSQLサーバーが必要。HemlockのstdlibモジュールはFFI（`import "libfoo.so"`）を通じてロードされる埋め込みライブラリであり、クライアント-サーバープロトコルではない。ベクトル検索のためにPostgreSQLのインストール、設定、実行を要求することはstdlibパターンと根本的に合致しない。

### プライマリ：USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch)はファーストクラスのC99 APIを持つオープンソース（Apache-2.0）のベクトル類似性検索ライブラリ。HNSW（Hierarchical Navigable Small World）アルゴリズムとSIMD最適化を使用。

**USearchがHemlockに適合する理由：**

1. **C99 APIがHemlock FFIに直接マッピング。** パターンは`@stdlib/sqlite`と同一。
2. **必須依存関係ゼロ。** BLAS、LAPACK、その他の外部要件なしで単一の`.so`にコンパイル。
3. **インプロセスかつ永続的。** メモリマップドファイルサポート。
4. **小さく明示的なAPI。** init、add、search、remove、save、load、freeをカバーする約20のC関数。
5. **本番実績。** ScyllaDBとYugabyteDBがベクトルインデックスに使用。
6. **パフォーマンス。** SIMD（AVX-512、NEON）対応のHNSWアルゴリズム。f32、f64、f16、int8量子化をサポート。

---

## 提案されるAPIデザイン（`@stdlib/vector`）

`@stdlib/sqlite`で確立されたパターンに従う（Hemlock慣用APIを持つFFIラッパー）：

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// インデックスを作成
let idx = create_index(dimensions: 384, metric: "cosine");

// ベクトルを追加（キー + float配列）
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// k個の最近傍を検索
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// 戻り値: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// 永続化
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// フィルタ付き検索（述語あり）
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;  // キー > 100のみにマッチ
});

// 情報
print(idx.size());       // ベクトル数
print(idx.dimensions()); // 次元数
print(idx.contains(42)); // メンバーシップチェック

// クリーンアップ
idx.remove(2);
idx.free();
```

### モジュールエクスポート

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // メモリマップド、読み取り専用

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

distance(a, b, metric?)  // スタンドアロン距離計算

// 距離メトリクス
METRIC_COSINE
METRIC_L2SQ       // ユークリッド（L2二乗）
METRIC_IP          // 内積（ドット積）
METRIC_HAMMING
METRIC_JACCARD

// スカラー型
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

---

## 実装計画

1. **FFIバインディングの記述** -- USearch C APIの`extern fn`宣言（約20関数）
2. **Hemlockラッパーの実装** -- `create_index()`、メソッド付き`VectorIndex` define
3. **メモリの処理** -- ベクトルデータのマーシャリングのための適切な`alloc`/`free`、エラー文字列のクリーンアップ
4. **ドキュメントの追加** -- sqlite.mdパターンに従う`stdlib/docs/vector.md`
5. **テストの追加** -- 基本的なCRUD、永続化、検索精度の`tests/stdlib_vector/`
6. **パリティテストの追加** -- 使用するFFIパターンにコンパイラサポートが必要な場合

推定規模：約400-600行のHemlock（968行の`sqlite.hml`に匹敵するが、API面はよりシンプル）。

---

## 未解決の質問

1. **モジュール名：** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`？
2. **sqlite-vec統合：** `@stdlib/sqlite`の一部として提供（拡張機能ロード）か、別モジュールか？
3. **量子化API：** USearchのint8/f16量子化を公開するか、f32デフォルトでシンプルに保つか？
4. **バッチ操作：** 一括操作用の`add_batch()` / `search_batch()`を追加するか、単一項目APIを維持するか？
5. **インデックス設定：** USearchのHNSWチューニング（connectivity、expansion factors）をどの程度公開するか？
