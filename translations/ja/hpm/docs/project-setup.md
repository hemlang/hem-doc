# プロジェクトセットアップ

hpmを使ったHemlockプロジェクトのセットアップ完全ガイド。

## 新しいプロジェクトの開始

### 基本セットアップ

ゼロから新しいプロジェクトを作成:

```bash
# プロジェクトディレクトリを作成
mkdir my-project
cd my-project

# package.jsonを初期化
hpm init

# ディレクトリ構造を作成
mkdir -p src test
```

### プロジェクトテンプレート

以下は異なる用途に応じた一般的なプロジェクト構造です:

#### ライブラリパッケージ

再利用可能なライブラリ用:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # メインエントリ、パブリックAPIをエクスポート
│   ├── core.hml           # コア機能
│   ├── utils.hml          # ユーティリティ関数
│   └── types.hml          # 型定義
└── test/
    ├── framework.hml      # テストフレームワーク
    ├── run.hml            # テストランナー
    └── test_core.hml      # テスト
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### アプリケーション

スタンドアロンアプリケーション用:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # アプリケーションエントリポイント
│   ├── config.hml         # 設定
│   ├── commands/          # CLIコマンド
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # 内部ライブラリ
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # データファイル
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Webアプリケーション

Webサーバー用:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # サーバーエントリポイント
│   ├── routes/            # ルートハンドラ
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # ミドルウェア
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # データモデル
│   │   └── user.hml
│   └── services/          # ビジネスロジック
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # 静的ファイル
│   ├── css/
│   └── js/
└── views/                 # テンプレート
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## package.jsonファイル

### 必須フィールド

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### すべてのフィールド

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
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

### フィールドリファレンス

| フィールド | 型 | 説明 |
|-------|------|-------------|
| `name` | string | owner/repo形式のパッケージ名（必須） |
| `version` | string | セマンティックバージョン（必須） |
| `description` | string | 短い説明 |
| `author` | string | 作者名とメール |
| `license` | string | ライセンス識別子（MIT、Apache-2.0など） |
| `repository` | string | リポジトリURL |
| `homepage` | string | プロジェクトホームページ |
| `bugs` | string | イシュートラッカーURL |
| `main` | string | エントリポイントファイル（デフォルト: src/index.hml） |
| `keywords` | array | 検索キーワード |
| `dependencies` | object | ランタイム依存関係 |
| `devDependencies` | object | 開発依存関係 |
| `scripts` | object | 名前付きスクリプト |
| `files` | array | 公開時に含めるファイル |
| `native` | object | ネイティブライブラリ要件 |

## package-lock.jsonファイル

ロックファイルは自動生成され、バージョン管理にコミットする必要があります。再現可能なインストールを保証します。

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### ロックファイルのベストプラクティス

- package-lock.jsonをバージョン管理に**コミット**
- 手動で**編集しない** - 自動生成される
- 変更をプルした後に**`hpm install`を実行**
- 破損した場合は**削除して再生成**:
  ```bash
  rm package-lock.json
  hpm install
  ```

## hem_modulesディレクトリ

インストールされたパッケージは`hem_modules/`に保存されます:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### hem_modulesのベストプラクティス

- **.gitignoreに追加** - 依存関係をコミットしない
- **変更しない** - 変更は上書きされる
- **新しくインストールするには削除**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Hemlockプロジェクトの推奨.gitignore:

```gitignore
# 依存関係
hem_modules/

# ビルド出力
dist/
*.hmlc

# IDEファイル
.idea/
.vscode/
*.swp
*.swo

# OSファイル
.DS_Store
Thumbs.db

# ログ
*.log
logs/

# 環境
.env
.env.local

# テストカバレッジ
coverage/
```

## 依存関係の操作

### 依存関係の追加

```bash
# ランタイム依存関係を追加
hpm install hemlang/json

# バージョン制約付きで追加
hpm install hemlang/sprout@^2.0.0

# 開発依存関係を追加
hpm install hemlang/test-utils --dev
```

### 依存関係のインポート

```hemlock
// パッケージからインポート（"main"エントリを使用）
import { parse, stringify } from "hemlang/json";

// サブパスからインポート
import { Router } from "hemlang/sprout/router";

// 標準ライブラリをインポート
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### インポート解決

hpmは以下の順序でインポートを解決:

1. **標準ライブラリ**: `@stdlib/*`は組み込みモジュールをインポート
2. **パッケージルート**: `owner/repo`は`main`フィールドを使用
3. **サブパス**: `owner/repo/path`は以下をチェック:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## スクリプト

### スクリプトの定義

package.jsonにスクリプトを追加:

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

### スクリプトの実行

```bash
hpm run start
hpm run dev
hpm run build

# testの短縮形
hpm test

# 引数を渡す
hpm run test -- --verbose --filter=unit
```

### スクリプトの命名規則

| スクリプト | 目的 |
|--------|---------|
| `start` | アプリケーションを実行 |
| `dev` | 開発モードで実行 |
| `test` | すべてのテストを実行 |
| `build` | 本番用にビルド |
| `clean` | 生成ファイルを削除 |
| `lint` | コードスタイルをチェック |
| `format` | コードをフォーマット |

## 開発ワークフロー

### 初期セットアップ

```bash
# プロジェクトをクローン
git clone https://github.com/yourusername/my-project.git
cd my-project

# 依存関係をインストール
hpm install

# テストを実行
hpm test

# 開発を開始
hpm run dev
```

### 日常のワークフロー

```bash
# 最新の変更をプル
git pull

# 新しい依存関係をインストール
hpm install

# 変更を加える...

# テストを実行
hpm test

# コミット
git add .
git commit -m "Add feature"
git push
```

### 新機能の追加

```bash
# フィーチャーブランチを作成
git checkout -b feature/new-feature

# 必要に応じて新しい依存関係を追加
hpm install hemlang/new-lib

# 機能を実装...

# テスト
hpm test

# コミットとプッシュ
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## 環境別設定

### 環境変数の使用

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### 設定ファイル

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## 参照

- [クイックスタート](quick-start.md) - すぐに始める
- [コマンド](commands.md) - コマンドリファレンス
- [パッケージの作成](creating-packages.md) - パッケージの公開
- [設定](configuration.md) - hpmの設定
