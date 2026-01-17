# バンドリングとパッケージング

Hemlockは、複数ファイルのプロジェクトを単一の配布可能ファイルにバンドルし、自己完結型の実行ファイルを作成するための組み込みツールを提供します。

## 概要

| コマンド | 出力 | 使用ケース |
|---------|--------|----------|
| `--bundle` | `.hmlc` または `.hmlb` | バイトコードを配布（実行にはHemlockが必要） |
| `--package` | 実行ファイル | スタンドアロンバイナリ（依存関係なし） |
| `--compile` | `.hmlc` | 単一ファイルをコンパイル（インポート解決なし） |

## バンドリング

バンドラーはエントリポイントからすべての`import`文を解決し、単一のファイルにフラット化します。

### 基本的な使用方法

```bash
# app.hmlとそのすべてのインポートをapp.hmlcにバンドル
hemlock --bundle app.hml

# 出力パスを指定
hemlock --bundle app.hml -o dist/app.hmlc

# 圧縮バンドル（.hmlb）を作成 - ファイルサイズが小さい
hemlock --bundle app.hml --compress -o app.hmlb

# 詳細出力（解決されたモジュールを表示）
hemlock --bundle app.hml --verbose
```

### 出力形式

**`.hmlc`（非圧縮）**
- シリアル化されたAST形式
- 読み込みと実行が高速
- デフォルトの出力形式

**`.hmlb`（圧縮）**
- zlib圧縮された`.hmlc`
- ファイルサイズが小さい（通常50-70%削減）
- 解凍のため起動がやや遅い

### バンドルファイルの実行

```bash
# 非圧縮バンドルを実行
hemlock app.hmlc

# 圧縮バンドルを実行
hemlock app.hmlb

# 引数を渡す
hemlock app.hmlc arg1 arg2
```

### 例：マルチモジュールプロジェクト

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # すべての依存関係がバンドルされた状態で実行
```

### stdlibインポート

バンドラーは`@stdlib/`インポートを自動的に解決します：

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

バンドル時、stdlibモジュールは出力に含まれます。

## パッケージング

パッケージングは、バンドルされたバイトコードをHemlockインタープリターのコピーに埋め込むことで、自己完結型の実行ファイルを作成します。

### 基本的な使用方法

```bash
# app.hmlから実行ファイルを作成
hemlock --package app.hml

# 出力名を指定
hemlock --package app.hml -o myapp

# 圧縮をスキップ（起動が速い、ファイルが大きい）
hemlock --package app.hml --no-compress

# 詳細出力
hemlock --package app.hml --verbose
```

### パッケージ化された実行ファイルの実行

```bash
# パッケージ化された実行ファイルは直接実行される
./myapp

# 引数はスクリプトに渡される
./myapp arg1 arg2
```

### パッケージ形式

パッケージ化された実行ファイルはHMLP形式を使用します：

```
[hemlockバイナリ][HMLB/HMLCペイロード][payload_size:u64][HMLPマジック:u32]
```

パッケージ化された実行ファイルが実行されると：
1. ファイル末尾の埋め込みペイロードをチェック
2. 見つかった場合、ペイロードを解凍して実行
3. 見つからない場合、通常のHemlockインタープリターとして動作

### 圧縮オプション

| フラグ | 形式 | 起動 | サイズ |
|------|--------|---------|------|
| （デフォルト） | HMLB | 通常 | 小さい |
| `--no-compress` | HMLC | 速い | 大きい |

起動時間が重要なCLIツールには、`--no-compress`を使用してください。

## バンドルの検査

`--info`を使用してバンドルまたはコンパイル済みファイルを検査できます：

```bash
hemlock --info app.hmlc
```

出力：
```
=== File Info: app.hmlc ===
Size: 12847 bytes
Format: HMLC (compiled AST)
Version: 1
Flags: 0x0001 [DEBUG]
Strings: 42
Statements: 156
```

```bash
hemlock --info app.hmlb
```

出力：
```
=== File Info: app.hmlb ===
Size: 5234 bytes
Format: HMLB (compressed bundle)
Version: 1
Uncompressed: 12847 bytes
Compressed: 5224 bytes
Ratio: 59.3% reduction
```

## ネイティブコンパイル

真のネイティブ実行ファイル（インタープリターなし）には、Hemlockコンパイラを使用します：

```bash
# Cを経由してネイティブ実行ファイルにコンパイル
hemlockc app.hml -o app

# 生成されたCコードを保持
hemlockc app.hml -o app --keep-c

# Cのみを出力（コンパイルしない）
hemlockc app.hml -c -o app.c

# 最適化レベル
hemlockc app.hml -o app -O2
```

コンパイラはCコードを生成し、GCCを呼び出してネイティブバイナリを生成します。以下が必要です：
- Hemlockランタイムライブラリ（`libhemlock_runtime`）
- Cコンパイラ（デフォルトはGCC）

### コンパイラオプション

| オプション | 説明 |
|--------|-------------|
| `-o <file>` | 出力実行ファイル名 |
| `-c` | Cコードのみを出力 |
| `--emit-c <file>` | Cを指定ファイルに書き込む |
| `-k, --keep-c` | コンパイル後に生成されたCを保持 |
| `-O<level>` | 最適化レベル（0-3） |
| `--cc <path>` | 使用するCコンパイラ |
| `--runtime <path>` | ランタイムライブラリへのパス |
| `-v, --verbose` | 詳細出力 |

## 比較

| アプローチ | ポータビリティ | 起動 | サイズ | 依存関係 |
|----------|-------------|---------|------|--------------|
| `.hml` | ソースのみ | パース時間 | 最小 | Hemlock |
| `.hmlc` | Hemlockのみ | 速い | 小 | Hemlock |
| `.hmlb` | Hemlockのみ | 速い | より小さい | Hemlock |
| `--package` | スタンドアロン | 速い | 大きい | なし |
| `hemlockc` | ネイティブ | 最速 | 可変 | ランタイムライブラリ |

## ベストプラクティス

1. **開発**：高速な反復のために`.hml`ファイルを直接実行
2. **配布（Hemlockあり）**：より小さいファイルのために`--compress`でバンドル
3. **配布（スタンドアロン）**：依存関係ゼロのデプロイのためにパッケージ化
4. **パフォーマンス重視**：ネイティブコンパイルに`hemlockc`を使用

## トラブルシューティング

### "Cannot find stdlib"

バンドラーは以下の場所でstdlibを探します：
1. `./stdlib`（実行ファイルからの相対パス）
2. `../stdlib`（実行ファイルからの相対パス）
3. `/usr/local/lib/hemlock/stdlib`

Hemlockが正しくインストールされているか、ソースディレクトリから実行していることを確認してください。

### 循環依存

```
Error: Circular dependency detected when loading 'path/to/module.hml'
```

サイクルを解消するためにインポートをリファクタリングしてください。共通の型には共有モジュールの使用を検討してください。

### パッケージサイズが大きい

- デフォルトの圧縮を使用（`--no-compress`を使用しない）
- パッケージサイズには完全なインタープリターが含まれます（ベース約500KB-1MB）
- 最小サイズには、ネイティブコンパイルに`hemlockc`を使用
