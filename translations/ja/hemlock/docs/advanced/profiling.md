# プロファイリング

Hemlockには、**CPU時間分析**、**メモリトラッキング**、**リーク検出**のための組み込みプロファイラーが含まれています。プロファイラーは、プログラムのパフォーマンスボトルネックとメモリの問題を特定するのに役立ちます。

## 目次

- [概要](#概要)
- [クイックスタート](#クイックスタート)
- [プロファイリングモード](#プロファイリングモード)
- [出力形式](#出力形式)
- [リーク検出](#リーク検出)
- [レポートの理解](#レポートの理解)
- [フレームグラフ生成](#フレームグラフ生成)
- [ベストプラクティス](#ベストプラクティス)

---

## 概要

プロファイラーは`profile`サブコマンドでアクセスします：

```bash
hemlock profile [OPTIONS] <FILE>
```

**主な機能：**
- **CPUプロファイリング** - 各関数で費やされた時間を測定（自己時間と合計時間）
- **メモリプロファイリング** - ソース位置付きですべての割り当てを追跡
- **リーク検出** - 解放されなかったメモリを特定
- **複数の出力形式** - テキスト、JSON、フレームグラフ互換出力
- **関数ごとのメモリ統計** - どの関数が最もメモリを割り当てているかを確認

---

## クイックスタート

### CPU時間のプロファイル（デフォルト）

```bash
hemlock profile script.hml
```

### メモリ割り当てのプロファイル

```bash
hemlock profile --memory script.hml
```

### メモリリークの検出

```bash
hemlock profile --leaks script.hml
```

### フレームグラフデータの生成

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## プロファイリングモード

### CPUプロファイリング（デフォルト）

各関数で費やされた時間を測定し、以下を区別します：
- **自己時間** - 関数自体のコードを実行するのに費やされた時間
- **合計時間** - 自己時間に呼び出された関数で費やされた時間を加えたもの

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # 明示的
```

**出力例：**
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

### メモリプロファイリング

ソース位置付きですべてのメモリ割り当て（`alloc`、`buffer`、`talloc`、`realloc`）を追跡します。

```bash
hemlock profile --memory script.hml
```

**出力例：**
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

### 呼び出し回数モード

関数呼び出しのみをカウントする最小オーバーヘッドモード（タイミングなし）。

```bash
hemlock profile --calls script.hml
```

---

## 出力形式

### テキスト（デフォルト）

テーブル付きの人間が読みやすい要約。

```bash
hemlock profile script.hml
```

---

### JSON

他のツールとの統合のための機械可読形式。

```bash
hemlock profile --json script.hml
```

**出力例：**
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

### フレームグラフ

[flamegraph.pl](https://github.com/brendangregg/FlameGraph)と互換性のある折りたたみスタック形式を生成します。

```bash
hemlock profile --flamegraph script.hml > profile.folded

# flamegraph.plでSVGを生成
flamegraph.pl profile.folded > profile.svg
```

**折りたたみ出力例：**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## リーク検出

`--leaks`フラグは解放されなかった割り当てのみを表示し、メモリリークの特定を容易にします。

```bash
hemlock profile --leaks script.hml
```

**リークのあるプログラム例：**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // リーク - 解放されない
    let p2 = alloc(200);    // OK - 下で解放
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // 正しく解放
}

leaky();
clean();
```

**--leaksでの出力：**
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

リークレポートは以下を表示します：
- **Leaked** - プログラム終了時に未解放のバイト
- **Total** - このサイトで割り当てられた総バイト数
- **Count** - このサイトでの割り当て回数

---

## レポートの理解

### 関数統計

| 列 | 説明 |
|--------|-------------|
| Function | 関数名 |
| Self | 呼び出し先を除いた関数内の時間 |
| Total | 呼び出されたすべての関数を含む時間 |
| Calls | 関数が呼び出された回数 |
| Alloc | この関数によって割り当てられた総バイト数 |
| Count | この関数による割り当て回数 |
| (%) | プログラム総時間に対する割合 |

### 割り当てサイト

| 列 | 説明 |
|--------|-------------|
| Location | ソースファイルと行番号 |
| Total | この場所で割り当てられた総バイト数 |
| Count | 割り当て回数 |
| Leaked | プログラム終了時にまだ割り当てられているバイト（--leaksのみ） |

### 時間単位

プロファイラーは適切な単位を自動的に選択します：
- `ns` - ナノ秒（< 1us）
- `us` - マイクロ秒（< 1ms）
- `ms` - ミリ秒（< 1s）
- `s` - 秒

---

## コマンドリファレンス

```
hemlock profile [OPTIONS] <FILE>

OPTIONS:
    --cpu           CPU/時間プロファイリング（デフォルト）
    --memory        メモリ割り当てプロファイリング
    --calls         呼び出し回数のみ（最小オーバーヘッド）
    --leaks         未解放の割り当てのみを表示（--memoryを暗黙的に含む）
    --json          JSON形式で出力
    --flamegraph    フレームグラフ互換形式で出力
    --top N         上位N件を表示（デフォルト：20）
```

---

## フレームグラフ生成

フレームグラフは、プログラムが時間を費やしている場所を視覚化し、より広いバーはより多くの時間が費やされていることを示します。

### フレームグラフの生成

1. flamegraph.plをインストール：
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. プログラムをプロファイル：
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. SVGを生成：
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. `profile.svg`をブラウザで開いてインタラクティブな視覚化を確認。

### フレームグラフの読み方

- **X軸**：総時間の割合（幅 = 時間の割合）
- **Y軸**：コールスタックの深さ（下 = エントリポイント、上 = リーフ関数）
- **色**：視覚的区別のためのランダム
- **クリック**：関数にズームインして呼び出し先を確認

---

## ベストプラクティス

### 1. 代表的なワークロードをプロファイル

現実的なデータと使用パターンでプロファイルしてください。小さなテストケースでは実際のボトルネックが明らかにならない場合があります。

```bash
# 良い例：本番環境に近いデータでプロファイル
hemlock profile --memory process_large_file.hml large_input.txt

# あまり有用でない：小さなテストケース
hemlock profile quick_test.hml
```

### 2. 開発中に--leaksを使用

メモリリークを早期に発見するため、定期的にリーク検出を実行：

```bash
hemlock profile --leaks my_program.hml
```

### 3. 前後を比較

最適化の効果を測定するため、最適化前後でプロファイル：

```bash
# 最適化前
hemlock profile --json script.hml > before.json

# 最適化後
hemlock profile --json script.hml > after.json

# 結果を比較
```

### 4. 大きなプログラムには--topを使用

最も重要な関数に焦点を当てるため出力を制限：

```bash
hemlock profile --top 10 large_program.hml
```

### 5. フレームグラフと組み合わせる

複雑なコールパターンでは、フレームグラフがテキスト出力より良い視覚化を提供：

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## プロファイラーオーバーヘッド

プロファイラーはプログラム実行にいくらかのオーバーヘッドを追加します：

| モード | オーバーヘッド | 使用ケース |
|------|----------|----------|
| `--calls` | 最小 | 関数呼び出しのカウントのみ |
| `--cpu` | 低 | 一般的なパフォーマンスプロファイリング |
| `--memory` | 中程度 | メモリ分析とリーク検出 |

最も正確な結果を得るには、複数回プロファイルして一貫したパターンを探してください。

---

## 関連項目

- [メモリ管理](../language-guide/memory.md) - ポインタとバッファ
- [メモリAPI](../reference/memory-api.md) - alloc、free、buffer関数
- [非同期/並行性](async-concurrency.md) - 非同期コードのプロファイリング
