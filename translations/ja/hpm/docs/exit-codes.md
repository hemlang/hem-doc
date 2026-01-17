# 終了コード

hpmの終了コードとその意味のリファレンス。

## 終了コード一覧

| コード | 名前 | 説明 |
|------|------|-------------|
| 0 | SUCCESS | コマンドが正常に完了 |
| 1 | CONFLICT | 依存関係のバージョン競合 |
| 2 | NOT_FOUND | パッケージが見つからない |
| 3 | VERSION_NOT_FOUND | 要求されたバージョンが見つからない |
| 4 | NETWORK | ネットワークエラー |
| 5 | INVALID_MANIFEST | 無効なpackage.json |
| 6 | INTEGRITY | 整合性チェック失敗 |
| 7 | RATE_LIMIT | GitHub APIレート制限超過 |
| 8 | CIRCULAR | 循環依存を検出 |

## 詳細な説明

### 終了コード0: SUCCESS

コマンドが正常に完了しました。

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### 終了コード1: CONFLICT

2つ以上のパッケージが依存関係の互換性のないバージョンを要求しています。

**例:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**解決策:**
1. どのパッケージが競合しているか確認:
   ```bash
   hpm why hemlang/json
   ```
2. 競合しているパッケージを更新:
   ```bash
   hpm update package-a
   ```
3. package.jsonのバージョン制約を緩和
4. 競合しているパッケージの1つを削除

### 終了コード2: NOT_FOUND

指定されたパッケージがGitHubに存在しません。

**例:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**解決策:**
1. パッケージ名のスペルを確認
2. リポジトリが存在するか確認: `https://github.com/owner/repo`
3. アクセス権を確認（プライベートリポジトリの場合、GITHUB_TOKENを設定）

### 終了コード3: VERSION_NOT_FOUND

指定された制約に一致するバージョンがありません。

**例:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**解決策:**
1. GitHubのリリース/タグで利用可能なバージョンを確認
2. 有効なバージョン制約を使用
3. バージョンタグは`v`で始まる必要あり（例: `v1.0.0`）

### 終了コード4: NETWORK

ネットワーク関連のエラーが発生しました。

**例:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**解決策:**
1. インターネット接続を確認
2. GitHubにアクセスできるか確認
3. ファイアウォールの背後にいる場合はプロキシ設定を確認
4. パッケージがキャッシュされている場合は`--offline`を使用:
   ```bash
   hpm install --offline
   ```
5. 待ってからリトライ（hpmは自動的にリトライ）

### 終了コード5: INVALID_MANIFEST

package.jsonファイルが無効または不正な形式です。

**例:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**解決策:**
1. JSON構文を確認（JSONバリデータを使用）
2. 必須フィールドが存在することを確認（`name`、`version`）
3. フィールド形式を確認:
   - name: `owner/repo`形式
   - version: `X.Y.Z` semver形式
4. 再生成:
   ```bash
   rm package.json
   hpm init
   ```

### 終了コード6: INTEGRITY

パッケージの整合性検証が失敗しました。

**例:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**解決策:**
1. キャッシュをクリアして再インストール:
   ```bash
   hpm cache clean
   hpm install
   ```
2. ネットワーク問題を確認（部分的なダウンロード）
3. パッケージが改ざんされていないか確認

### 終了コード7: RATE_LIMIT

GitHub APIのレート制限を超過しました。

**例:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**解決策:**
1. **GitHubで認証**（推奨）:
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. レート制限がリセットされるのを待つ（毎時リセット）
3. パッケージがキャッシュされている場合はオフラインモードを使用:
   ```bash
   hpm install --offline
   ```

### 終了コード8: CIRCULAR

依存関係グラフで循環依存が検出されました。

**例:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**解決策:**
1. これは通常パッケージ自体のバグ
2. パッケージメンテナーに連絡
3. 循環しているパッケージの1つの使用を避ける

## スクリプトでの終了コードの使用

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## 終了コードによるトラブルシューティング

### クイックリファレンス

| コード | 最初に確認すること |
|------|---------------------|
| 1 | `hpm why <package>`を実行して競合を確認 |
| 2 | GitHubでパッケージ名を確認 |
| 3 | GitHubタグで利用可能なバージョンを確認 |
| 4 | インターネット接続を確認 |
| 5 | package.jsonの構文を検証 |
| 6 | `hpm cache clean && hpm install`を実行 |
| 7 | `GITHUB_TOKEN`環境変数を設定 |
| 8 | パッケージメンテナーに連絡 |

## 参照

- [トラブルシューティング](troubleshooting.md) - 詳細な解決策
- [コマンド](commands.md) - コマンドリファレンス
- [設定](configuration.md) - GitHubトークンの設定
