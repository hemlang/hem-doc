# トラブルシューティング

hpmの一般的な問題と解決策。

## インストールの問題

### "hemlock: command not found"

**原因:** HemlockがインストールされていないかPATHにない。

**解決策:**

```bash
# hemlockが存在するか確認
which hemlock

# 見つからない場合、まずHemlockをインストール
# https://github.com/hemlang/hemlock を参照

# インストール後に確認
hemlock --version
```

### "hpm: command not found"

**原因:** hpmがインストールされていないかPATHにない。

**解決策:**

```bash
# hpmがどこにインストールされているか確認
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# カスタム場所を使用している場合、PATHに追加
export PATH="$HOME/.local/bin:$PATH"

# 永続化のため~/.bashrcまたは~/.zshrcに追加
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 必要に応じて再インストール
cd /path/to/hpm
sudo make install
```

### インストール時の"Permission denied"

**原因:** インストールディレクトリへの書き込み権限がない。

**解決策:**

```bash
# オプション1: システム全体のインストールにsudoを使用
sudo make install

# オプション2: ユーザーディレクトリにインストール（sudoが不要）
make install PREFIX=$HOME/.local
```

## 依存関係の問題

### "Package not found"（終了コード2）

**原因:** パッケージがGitHubに存在しない。

**解決策:**

```bash
# パッケージが存在するか確認
# https://github.com/owner/repo をチェック

# スペルを確認
hpm install hemlang/sprout  # 正しい
hpm install hemlan/sprout   # 間違ったowner
hpm install hemlang/spout   # 間違ったrepo

# package.jsonのタイプミスを確認
cat package.json | grep -A 5 dependencies
```

### "Version not found"（終了コード3）

**原因:** バージョン制約に一致するリリースがない。

**解決策:**

```bash
# 利用可能なバージョンをリスト（GitHubのリリース/タグを確認）
# タグは'v'で始まる必要あり（例: v1.0.0）

# 有効なバージョン制約を使用
hpm install owner/repo@^1.0.0

# 最新バージョンを試す
hpm install owner/repo

# GitHubで利用可能なタグを確認
# https://github.com/owner/repo/tags
```

### "Dependency conflict"（終了コード1）

**原因:** 2つのパッケージが依存関係の互換性のないバージョンを要求。

**解決策:**

```bash
# 競合を確認
hpm install --verbose

# 何がその依存関係を要求しているか確認
hpm why conflicting/package

# 解決策:
# 1. 競合しているパッケージを更新
hpm update problem/package

# 2. package.jsonでバージョン制約を変更
# 互換性のあるバージョンを許可するように編集

# 3. 競合しているパッケージの1つを削除
hpm uninstall one/package
```

### "Circular dependency"（終了コード8）

**原因:** パッケージAがBに依存し、BがAに依存。

**解決策:**

```bash
# サイクルを特定
hpm install --verbose

# これは通常パッケージ自体のバグ
# パッケージメンテナーに連絡

# 回避策: 循環しているパッケージの1つの使用を避ける
```

## ネットワークの問題

### "Network error"（終了コード4）

**原因:** GitHub APIに接続できない。

**解決策:**

```bash
# インターネット接続を確認
ping github.com

# GitHub APIにアクセスできるか確認
curl -I https://api.github.com

# 再試行（hpmは自動的にリトライ）
hpm install

# パッケージがキャッシュされている場合はオフラインモードを使用
hpm install --offline

# ファイアウォールの背後にいる場合はプロキシ設定を確認
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded"（終了コード7）

**原因:** 認証なしでAPIリクエストが多すぎる。

**解決策:**

```bash
# オプション1: GitHubトークンで認証（推奨）
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# トークンを作成: GitHub → Settings → Developer settings → Personal access tokens

# オプション2: トークンを設定ファイルに保存
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# オプション3: レート制限のリセットを待つ（毎時リセット）

# オプション4: オフラインモードを使用
hpm install --offline
```

### 接続タイムアウト

**原因:** ネットワークが遅いかGitHub APIの問題。

**解決策:**

```bash
# hpmは指数バックオフで自動的にリトライ

# GitHubに問題がないか確認
# https://www.githubstatus.com を参照

# 後で再試行
hpm install

# キャッシュされたパッケージを使用
hpm install --offline
```

## Package.jsonの問題

### "Invalid package.json"（終了コード5）

**原因:** 不正な形式または必須フィールドの欠落。

**解決策:**

```bash
# JSON構文を検証
cat package.json | python -m json.tool

# 必須フィールドを確認
cat package.json

# 必須フィールド:
# - "name": "owner/repo"形式
# - "version": "X.Y.Z"形式

# 必要に応じて再生成
rm package.json
hpm init
```

### "name"形式エラー

**原因:** パッケージ名が`owner/repo`形式でない。

**解決策:**

```json
// 間違い
{
  "name": "my-package"
}

// 正しい
{
  "name": "yourusername/my-package"
}
```

### "version"形式エラー

**原因:** バージョンがsemver形式でない。

**解決策:**

```json
// 間違い
{
  "version": "1.0"
}

// 正しい
{
  "version": "1.0.0"
}
```

## ロックファイルの問題

### ロックファイルの同期が取れていない

**原因:** package.jsonがinstallを実行せずに変更された。

**解決策:**

```bash
# ロックファイルを再生成
rm package-lock.json
hpm install
```

### 破損したロックファイル

**原因:** 無効なJSONまたは手動編集。

**解決策:**

```bash
# JSONの有効性を確認
cat package-lock.json | python -m json.tool

# 再生成
rm package-lock.json
hpm install
```

## hem_modulesの問題

### パッケージがインストールされない

**原因:** 様々な問題の可能性。

**解決策:**

```bash
# クリーンにして再インストール
rm -rf hem_modules
hpm install

# 詳細出力を確認
hpm install --verbose
```

### インポートが機能しない

**原因:** パッケージが正しくインストールされていないか、インポートパスが間違っている。

**解決策:**

```bash
# パッケージがインストールされているか確認
ls hem_modules/owner/repo/

# package.jsonのmainフィールドを確認
cat hem_modules/owner/repo/package.json

# 正しいインポート形式
import { x } from "owner/repo";          # mainエントリを使用
import { y } from "owner/repo/subpath";  # サブパスインポート
```

### "Module not found"エラー

**原因:** インポートパスがファイルに解決されない。

**解決策:**

```bash
# インポートパスを確認
ls hem_modules/owner/repo/src/

# index.hmlを確認
ls hem_modules/owner/repo/src/index.hml

# package.jsonのmainフィールドを確認
cat hem_modules/owner/repo/package.json | grep main
```

## キャッシュの問題

### キャッシュの容量が大きすぎる

**解決策:**

```bash
# キャッシュサイズを表示
hpm cache list

# キャッシュをクリア
hpm cache clean
```

### キャッシュの権限

**解決策:**

```bash
# 権限を修正
chmod -R u+rw ~/.hpm/cache

# または削除して再インストール
rm -rf ~/.hpm/cache
hpm install
```

### 間違ったキャッシュを使用

**解決策:**

```bash
# キャッシュの場所を確認
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# 間違っている場合は環境変数をクリア
unset HPM_CACHE_DIR
```

## スクリプトの問題

### "Script not found"

**原因:** スクリプト名がpackage.jsonに存在しない。

**解決策:**

```bash
# 利用可能なスクリプトをリスト
cat package.json | grep -A 20 scripts

# スペルを確認
hpm run test    # 正しい
hpm run tests   # スクリプト名が"test"の場合は間違い
```

### スクリプトが失敗

**原因:** スクリプトコマンドにエラー。

**解決策:**

```bash
# コマンドを直接実行してエラーを確認
hemlock test/run.hml

# スクリプト定義を確認
cat package.json | grep test
```

## デバッグ

### 詳細出力を有効化

```bash
hpm install --verbose
```

### hpmバージョンを確認

```bash
hpm --version
```

### hemlockバージョンを確認

```bash
hemlock --version
```

### ドライラン

変更を加えずにプレビュー:

```bash
hpm install --dry-run
```

### クリーンスレート

最初から始める:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## ヘルプを得る

### コマンドヘルプ

```bash
hpm --help
hpm install --help
```

### 問題を報告

バグに遭遇した場合:

1. 既存のIssueを確認: https://github.com/hemlang/hpm/issues
2. 以下を含む新しいIssueを作成:
   - hpmバージョン（`hpm --version`）
   - Hemlockバージョン（`hemlock --version`）
   - オペレーティングシステム
   - 再現手順
   - エラーメッセージ（`--verbose`を使用）

## 終了コードリファレンス

| コード | 意味 | 一般的な解決策 |
|------|---------|-----------------|
| 0 | 成功 | - |
| 1 | 依存関係の競合 | 更新または制約を変更 |
| 2 | パッケージが見つからない | スペルを確認、リポジトリの存在を確認 |
| 3 | バージョンが見つからない | GitHubで利用可能なバージョンを確認 |
| 4 | ネットワークエラー | 接続を確認、リトライ |
| 5 | 無効なpackage.json | JSON構文と必須フィールドを修正 |
| 6 | 整合性チェック失敗 | キャッシュをクリアして再インストール |
| 7 | GitHubレート制限 | GITHUB_TOKENを追加 |
| 8 | 循環依存 | パッケージメンテナーに連絡 |

## 参照

- [インストール](installation.md) - インストールガイド
- [設定](configuration.md) - 設定オプション
- [コマンド](commands.md) - コマンドリファレンス
