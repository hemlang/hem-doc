# 設定

このガイドでは、hpmのすべての設定オプションについて説明します。

## 概要

hpmは以下の方法で設定できます:

1. **環境変数** - ランタイム設定用
2. **グローバル設定ファイル** - `~/.hpm/config.json`
3. **プロジェクトファイル** - `package.json`と`package-lock.json`

## 環境変数

### GITHUB_TOKEN

認証用のGitHub APIトークン。

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**認証の利点:**
- より高いAPIレート制限（60ではなく5000リクエスト/時間）
- プライベートリポジトリへのアクセス
- より高速な依存関係解決

**トークンの作成:**

1. GitHub → Settings → Developer settings → Personal access tokensに移動
2. "Generate new token (classic)"をクリック
3. スコープを選択:
   - `repo` - プライベートリポジトリへのアクセス用
   - `read:packages` - GitHub Packages用（使用する場合）
4. 生成してトークンをコピー

### HPM_CACHE_DIR

デフォルトのキャッシュディレクトリを上書きします。

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

デフォルト: `~/.hpm/cache`

**使用例:**
- カスタムキャッシュ場所を持つCI/CDシステム
- プロジェクト間での共有キャッシュ
- 分離されたビルド用の一時キャッシュ

### HOME

ユーザーホームディレクトリ。以下の場所を特定するために使用:
- 設定ディレクトリ: `$HOME/.hpm/`
- キャッシュディレクトリ: `$HOME/.hpm/cache/`

通常はシステムによって設定されます。必要な場合のみ上書きしてください。

### .bashrc / .zshrcの例

```bash
# GitHub認証（推奨）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# カスタムキャッシュ場所（オプション）
# export HPM_CACHE_DIR=/path/to/cache

# hpmをPATHに追加（カスタムインストール場所を使用する場合）
export PATH="$HOME/.local/bin:$PATH"
```

## グローバル設定ファイル

### 場所

`~/.hpm/config.json`

### 形式

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### 設定ファイルの作成

```bash
# 設定ディレクトリを作成
mkdir -p ~/.hpm

# 設定ファイルを作成
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# ファイルを保護（推奨）
chmod 600 ~/.hpm/config.json
```

### トークンの優先順位

両方が設定されている場合、環境変数が優先されます:

1. `GITHUB_TOKEN`環境変数（最高）
2. `~/.hpm/config.json`の`github_token`フィールド
3. 認証なし（デフォルト）

## ディレクトリ構造

### グローバルディレクトリ

```
~/.hpm/
├── config.json          # グローバル設定
└── cache/               # パッケージキャッシュ
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### プロジェクトディレクトリ

```
my-project/
├── package.json         # プロジェクトマニフェスト
├── package-lock.json    # 依存関係ロックファイル
├── hem_modules/         # インストールされたパッケージ
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # ソースコード
└── test/                # テスト
```

## パッケージキャッシュ

### 場所

デフォルト: `~/.hpm/cache/`

上書き: `HPM_CACHE_DIR`環境変数

### 構造

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### キャッシュの管理

```bash
# キャッシュされたパッケージを表示
hpm cache list

# キャッシュ全体をクリア
hpm cache clean
```

### キャッシュの動作

- パッケージは最初のダウンロード後にキャッシュされる
- 以降のインストールはキャッシュされたバージョンを使用
- キャッシュのみからインストールするには`--offline`を使用
- キャッシュはすべてのプロジェクト間で共有

## GitHub APIレート制限

### 認証なし

- IPアドレスあたり**60リクエスト/時間**
- 同じIP上のすべての非認証ユーザーで共有
- CI/CDや多くの依存関係がある場合、すぐに枯渇

### 認証あり

- 認証ユーザーあたり**5000リクエスト/時間**
- 個人のレート制限、共有なし

### レート制限の処理

hpmは自動的に:
- 指数バックオフでリトライ（1秒、2秒、4秒、8秒）
- 終了コード7でレート制限エラーを報告
- レート制限された場合に認証を提案

**レート制限時の解決策:**

```bash
# オプション1: GitHubトークンで認証（推奨）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# オプション2: レート制限のリセットを待つ
# （制限は毎時リセット）

# オプション3: オフラインモードを使用（パッケージがキャッシュされている場合）
hpm install --offline
```

## オフラインモード

ネットワークアクセスなしでパッケージをインストール:

```bash
hpm install --offline
```

**要件:**
- すべてのパッケージがキャッシュにある必要あり
- 正確なバージョンを持つロックファイルが存在する必要あり

**使用例:**
- エアギャップ環境
- CI/CDビルドの高速化（ウォームキャッシュ時）
- レート制限の回避

## CI/CD設定

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Hemlockをインストール（セットアップに応じて調整）
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# パッケージファイルを最初にコピー（レイヤーキャッシュ用）
COPY package.json package-lock.json ./

# 依存関係をインストール
RUN hpm install

# ソースコードをコピー
COPY . .

# アプリケーションを実行
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## プロキシ設定

プロキシの背後にある環境では、システムレベルで設定:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## セキュリティのベストプラクティス

### トークンのセキュリティ

1. **トークンをバージョン管理にコミットしない**
2. **CI/CDでは環境変数を使用**
3. **トークンスコープを最小限に制限**
4. **定期的にトークンをローテーション**
5. **設定ファイルを保護**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### プライベートリポジトリ

プライベートパッケージにアクセスするには:

1. `repo`スコープを持つトークンを作成
2. 認証を設定（環境変数または設定ファイル）
3. トークンがリポジトリへのアクセス権を持っていることを確認

```bash
# アクセスをテスト
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## 設定のトラブルシューティング

### 設定の確認

```bash
# トークンが設定されているかチェック
echo $GITHUB_TOKEN | head -c 10

# 設定ファイルをチェック
cat ~/.hpm/config.json

# キャッシュディレクトリをチェック
ls -la ~/.hpm/cache/

# 詳細出力でテスト
hpm install --verbose
```

### よくある問題

**"GitHub rate limit exceeded"**
- `GITHUB_TOKEN`で認証を設定
- レート制限のリセットを待つ
- パッケージがキャッシュされている場合は`--offline`を使用

**キャッシュの"Permission denied"**
```bash
# キャッシュの権限を修正
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# 設定ディレクトリを作成
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## 参照

- [インストール](installation.md) - hpmのインストール
- [トラブルシューティング](troubleshooting.md) - よくある問題
- [コマンド](commands.md) - コマンドリファレンス
