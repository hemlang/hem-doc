# コマンドリファレンス

すべてのhpmコマンドの完全なリファレンス。

## グローバルオプション

これらのオプションはどのコマンドでも使用できます:

| オプション | 説明 |
|--------|-------------|
| `--help`, `-h` | ヘルプメッセージを表示 |
| `--version`, `-v` | hpmのバージョンを表示 |
| `--verbose` | 詳細な出力を表示 |

## コマンド

### hpm init

新しい`package.json`ファイルを作成します。

```bash
hpm init        # インタラクティブモード
hpm init --yes  # すべてのデフォルトを受け入れる
hpm init -y     # 短縮形
```

**オプション:**

| オプション | 説明 |
|--------|-------------|
| `--yes`, `-y` | すべてのプロンプトでデフォルト値を受け入れる |

**インタラクティブプロンプト:**
- パッケージ名（owner/repo形式）
- バージョン（デフォルト: 1.0.0）
- 説明
- 作者
- ライセンス（デフォルト: MIT）
- メインファイル（デフォルト: src/index.hml）

**例:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

依存関係をインストールするか、新しいパッケージを追加します。

```bash
hpm install                           # package.jsonからすべてをインストール
hpm install owner/repo                # パッケージを追加してインストール
hpm install owner/repo@^1.0.0        # バージョン制約付きで
hpm install owner/repo --dev         # 開発依存関係として
hpm i owner/repo                      # 短縮形
```

**オプション:**

| オプション | 説明 |
|--------|-------------|
| `--dev`, `-D` | devDependenciesに追加 |
| `--verbose` | 詳細な進捗を表示 |
| `--dry-run` | インストールせずにプレビュー |
| `--offline` | キャッシュのみからインストール（ネットワークなし） |
| `--parallel` | 並列ダウンロードを有効化（実験的） |

**バージョン制約の構文:**

| 構文 | 例 | 意味 |
|--------|---------|---------|
| (なし) | `owner/repo` | 最新バージョン |
| 固定 | `owner/repo@1.2.3` | 正確に1.2.3 |
| キャレット | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| チルダ | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| 範囲 | `owner/repo@>=1.0.0` | 1.0.0以上 |

**例:**

```bash
# すべての依存関係をインストール
hpm install

# 特定のパッケージをインストール
hpm install hemlang/json

# バージョン制約付きでインストール
hpm install hemlang/sprout@^2.0.0

# 開発依存関係としてインストール
hpm install hemlang/test-utils --dev

# インストール内容をプレビュー
hpm install hemlang/sprout --dry-run

# 詳細出力
hpm install --verbose

# キャッシュのみからインストール（オフライン）
hpm install --offline
```

**出力:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

パッケージを削除します。

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # 短縮形
hpm remove owner/repo      # 別名
```

**例:**

```bash
hpm uninstall hemlang/sprout
```

**出力:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

制約内で最新バージョンにパッケージを更新します。

```bash
hpm update              # すべてのパッケージを更新
hpm update owner/repo   # 特定のパッケージを更新
hpm up owner/repo       # 短縮形
```

**オプション:**

| オプション | 説明 |
|--------|-------------|
| `--verbose` | 詳細な進捗を表示 |
| `--dry-run` | 更新せずにプレビュー |

**例:**

```bash
# すべてのパッケージを更新
hpm update

# 特定のパッケージを更新
hpm update hemlang/sprout

# 更新をプレビュー
hpm update --dry-run
```

**出力:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

インストールされているパッケージを表示します。

```bash
hpm list              # 完全な依存関係ツリーを表示
hpm list --depth=0    # 直接依存関係のみ
hpm list --depth=1    # 1レベルの推移的依存関係
hpm ls                # 短縮形
```

**オプション:**

| オプション | 説明 |
|--------|-------------|
| `--depth=N` | ツリーの深さを制限（デフォルト: すべて） |

**例:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

新しいバージョンが利用可能なパッケージを表示します。

```bash
hpm outdated
```

**出力:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: インストールされているバージョン
- **Wanted**: 制約に一致する最高バージョン
- **Latest**: 最新の利用可能なバージョン

---

### hpm run

package.jsonからスクリプトを実行します。

```bash
hpm run <script>
hpm run <script> -- <args>
```

**例:**

このpackage.jsonの場合:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

スクリプトを実行:

```bash
hpm run start
hpm run test
hpm run build

# スクリプトに引数を渡す
hpm run test -- --verbose
```

---

### hpm test

`hpm run test`の短縮形。

```bash
hpm test
hpm test -- --verbose
```

以下と同等:

```bash
hpm run test
```

---

### hpm why

パッケージがインストールされている理由を説明します（依存関係チェーンを表示）。

```bash
hpm why owner/repo
```

**例:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

グローバルパッケージキャッシュを管理します。

```bash
hpm cache list    # キャッシュされたパッケージをリスト
hpm cache clean   # すべてのキャッシュされたパッケージをクリア
```

**サブコマンド:**

| サブコマンド | 説明 |
|------------|-------------|
| `list` | すべてのキャッシュされたパッケージとサイズを表示 |
| `clean` | すべてのキャッシュされたパッケージを削除 |

**例:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## コマンドショートカット

便宜上、いくつかのコマンドには短いエイリアスがあります:

| コマンド | ショートカット |
|---------|-----------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**例:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## 終了コード

hpmは異なるエラー条件を示すために特定の終了コードを使用します:

| コード | 意味 |
|------|---------|
| 0 | 成功 |
| 1 | 依存関係の競合 |
| 2 | パッケージが見つからない |
| 3 | バージョンが見つからない |
| 4 | ネットワークエラー |
| 5 | 無効なpackage.json |
| 6 | 整合性チェック失敗 |
| 7 | GitHubレート制限超過 |
| 8 | 循環依存 |

スクリプトでの終了コードの使用:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## 環境変数

hpmは以下の環境変数を尊重します:

| 変数 | 説明 |
|----------|-------------|
| `GITHUB_TOKEN` | 認証用のGitHub APIトークン |
| `HPM_CACHE_DIR` | キャッシュディレクトリの場所を上書き |
| `HOME` | ユーザーホームディレクトリ（設定/キャッシュ用） |

**例:**

```bash
# より高いレート制限のためにGitHubトークンを使用
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# カスタムキャッシュディレクトリを使用
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## 参照

- [設定](configuration.md) - 設定ファイル
- [パッケージ仕様](package-spec.md) - package.jsonの形式
- [トラブルシューティング](troubleshooting.md) - よくある問題
