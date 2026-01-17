# パッケージ仕様

`package.json`ファイル形式の完全なリファレンス。

## 概要

すべてのhpmパッケージにはプロジェクトルートに`package.json`ファイルが必要です。このファイルはパッケージのメタデータ、依存関係、スクリプトを定義します。

## 最小限の例

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## 完全な例

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

## フィールドリファレンス

### name（必須）

`owner/repo`形式のパッケージ名。

```json
{
  "name": "hemlang/sprout"
}
```

**要件:**
- `owner/repo`形式である必要あり
- `owner`はGitHubユーザー名または組織である必要あり
- `repo`はリポジトリ名である必要あり
- 小文字、数字、ハイフンを使用
- 合計最大214文字

**有効な名前:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**無効な名前:**
```
my-package          # ownerがない
hemlang/My_Package  # 大文字とアンダースコア
hemlang             # repoがない
```

### version（必須）

[セマンティックバージョニング](https://semver.org/)に従うパッケージバージョン。

```json
{
  "version": "1.2.3"
}
```

**形式:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**有効なバージョン:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

パッケージの短い説明。

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- 200文字以下に保つ
- パッケージが何をするかを説明、どのようにではなく

### author

パッケージ作者情報。

```json
{
  "author": "Your Name <email@example.com>"
}
```

**受け入れられる形式:**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

ライセンス識別子。

```json
{
  "license": "MIT"
}
```

**一般的なライセンス:**
- `MIT` - MITライセンス
- `Apache-2.0` - Apache License 2.0
- `GPL-3.0` - GNU General Public License v3.0
- `BSD-3-Clause` - BSD 3条項ライセンス
- `ISC` - ISCライセンス
- `UNLICENSED` - プロプライエタリ/プライベート

可能な限り[SPDX識別子](https://spdx.org/licenses/)を使用してください。

### repository

ソースリポジトリへのリンク。

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

プロジェクトホームページURL。

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

イシュートラッカーURL。

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

パッケージのエントリポイントファイル。

```json
{
  "main": "src/index.hml"
}
```

**デフォルト:** `src/index.hml`

ユーザーがパッケージをインポートするとき:
```hemlock
import { x } from "owner/repo";
```

hpmは`main`で指定されたファイルをロードします。

**インポートの解決順序:**
1. 正確なパス: `src/index.hml`
2. .hml拡張子付き: `src/index` → `src/index.hml`
3. indexファイル: `src/index/` → `src/index/index.hml`

### keywords

発見性のためのキーワード配列。

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- 小文字を使用
- 具体的で関連性のあるものに
- 適切な場合は言語（"hemlock"）を含める

### dependencies

パッケージが動作するために必要なランタイム依存関係。

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**キー:** パッケージ名（`owner/repo`）
**値:** バージョン制約

**バージョン制約の構文:**

| 制約 | 意味 |
|------------|---------|
| `1.2.3` | 正確なバージョン |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | 1.0.0以上 |
| `>=1.0.0 <2.0.0` | 範囲 |
| `*` | 任意のバージョン |

### devDependencies

開発専用の依存関係（テスト、ビルドなど）。

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

開発依存関係は:
- 開発中にインストールされる
- パッケージが依存関係として使用されるときはインストールされない
- テスト、ビルド、リンティングなどに使用

### scripts

`hpm run`で実行できる名前付きコマンド。

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

**スクリプトの実行:**
```bash
hpm run start
hpm run build
hpm test        # 'hpm run test'の短縮形
```

**引数の渡し方:**
```bash
hpm run test -- --verbose --filter=unit
```

**一般的なスクリプト:**

| スクリプト | 目的 |
|--------|---------|
| `start` | アプリケーションを起動 |
| `dev` | ホットリロード付き開発モード |
| `test` | テストを実行 |
| `build` | 本番用にビルド |
| `clean` | ビルド成果物を削除 |
| `lint` | コードスタイルをチェック |
| `format` | コードをフォーマット |

### files

パッケージがインストールされるときに含めるファイルとディレクトリ。

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**デフォルト動作:** 指定されていない場合、以下を含む:
- リポジトリ内のすべてのファイル
- `.git/`、`node_modules/`、`hem_modules/`を除外

**用途:**
- パッケージサイズを削減
- 配布からテストファイルを除外
- 必要なファイルのみを含める

### native

ネイティブライブラリの要件。

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

システムにインストールが必要なネイティブ依存関係をドキュメント化します。

## 検証

hpmは様々な操作でpackage.jsonを検証します。一般的な検証エラー:

### 必須フィールドの欠落

```
Error: package.json missing required field: name
```

**修正:** 必須フィールドを追加。

### 無効なname形式

```
Error: Invalid package name. Must be in owner/repo format.
```

**修正:** `owner/repo`形式を使用。

### 無効なversion

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**修正:** 完全なsemver形式（`1.0.0`）を使用。

### 無効なJSON

```
Error: package.json is not valid JSON
```

**修正:** JSON構文を確認（カンマ、クォート、括弧）。

## package.jsonの作成

### インタラクティブ

```bash
hpm init
```

各フィールドをインタラクティブにプロンプト。

### デフォルト値で

```bash
hpm init --yes
```

デフォルト値で作成:
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### 手動

ファイルを手動で作成:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## ベストプラクティス

1. **常にmainを指定** - デフォルトに頼らない
2. **キャレット範囲を使用** - ほとんどの依存関係には`^1.0.0`
3. **開発依存関係を分離** - テスト/ビルド依存関係はdevDependenciesに
4. **キーワードを含める** - ユーザーがパッケージを見つけやすくする
5. **スクリプトをドキュメント化** - スクリプトに明確な名前を付ける
6. **ライセンスを指定** - オープンソースには必須
7. **説明を追加** - ユーザーが目的を理解しやすくする

## 参照

- [パッケージの作成](creating-packages.md) - 公開ガイド
- [バージョニング](versioning.md) - バージョン制約
- [プロジェクトセットアップ](project-setup.md) - プロジェクト構造
