# クイックスタート

hpmを5分で使い始めましょう。

## hpmのインストール

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

その他のインストールオプションについては、[インストールガイド](installation.md)を参照してください。

## 新しいプロジェクトの作成

新しいディレクトリを作成してパッケージを初期化:

```bash
mkdir my-project
cd my-project
hpm init
```

プロジェクトの詳細を入力:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

`--yes`を使用してすべてのデフォルトを受け入れる:

```bash
hpm init --yes
```

## プロジェクト構造

基本的なプロジェクト構造を作成:

```
my-project/
├── package.json        # プロジェクトマニフェスト
├── src/
│   └── index.hml      # メインエントリポイント
└── test/
    └── test.hml       # テスト
```

メインファイルを作成:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// メインエントリポイント
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## 依存関係のインストール

GitHub上でパッケージを検索（パッケージは`owner/repo`形式を使用）:

```bash
# パッケージをインストール
hpm install hemlang/sprout

# バージョン制約付きでインストール
hpm install hemlang/json@^1.0.0

# 開発依存関係としてインストール
hpm install hemlang/test-utils --dev
```

インストール後、プロジェクト構造に`hem_modules/`が追加されます:

```
my-project/
├── package.json
├── package-lock.json   # ロックファイル（自動生成）
├── hem_modules/        # インストールされたパッケージ
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## インストールしたパッケージの使用

GitHubパスを使用してパッケージをインポート:

```hemlock
// インストールしたパッケージからインポート
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// サブパスからインポート
import { middleware } from "hemlang/sprout/middleware";

// 標準ライブラリ（組み込み）
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## スクリプトの追加

`package.json`にスクリプトを追加:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

`hpm run`でスクリプトを実行:

```bash
hpm run start
hpm run build

# testの短縮形
hpm test
```

## 一般的なワークフロー

### すべての依存関係をインストール

`package.json`を持つプロジェクトをクローンした場合:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### 依存関係の更新

すべてのパッケージを制約内で最新バージョンに更新:

```bash
hpm update
```

特定のパッケージを更新:

```bash
hpm update hemlang/sprout
```

### インストールされたパッケージの表示

すべてのインストール済みパッケージをリスト:

```bash
hpm list
```

出力に依存関係ツリーが表示されます:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### 更新の確認

新しいバージョンがあるパッケージを確認:

```bash
hpm outdated
```

### パッケージの削除

```bash
hpm uninstall hemlang/sprout
```

## 例: Webアプリケーション

Webフレームワークを使用した完全な例:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

アプリケーションを実行:

```bash
hpm install
hpm run start
```

## 次のステップ

- [コマンドリファレンス](commands.md) - すべてのhpmコマンドを学ぶ
- [パッケージの作成](creating-packages.md) - 独自のパッケージを公開
- [設定](configuration.md) - hpmとGitHubトークンを設定
- [プロジェクトセットアップ](project-setup.md) - 詳細なプロジェクト設定
