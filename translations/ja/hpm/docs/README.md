# hpm ドキュメント

hpm（Hemlock Package Manager）のドキュメントへようこそ。hpmは[Hemlock](https://github.com/hemlang/hemlock)プログラミング言語の公式パッケージマネージャーです。

## 概要

hpmはGitHubをパッケージレジストリとして使用し、パッケージはGitHubリポジトリパスで識別されます（例：`hemlang/sprout`）。これは以下を意味します：

- **中央レジストリなし** - パッケージはGitHubリポジトリに存在します
- **バージョンタグ** - リリースはGitタグです（例：`v1.0.0`）
- **公開はただのgit** - タグをプッシュするだけで新しいバージョンを公開できます

## ドキュメント

### はじめに

- [インストール](installation.md) - hpmのインストール方法
- [クイックスタート](quick-start.md) - 5分で使い始める
- [プロジェクトのセットアップ](project-setup.md) - 新しいHemlockプロジェクトの設定

### ユーザーガイド

- [コマンドリファレンス](commands.md) - すべてのhpmコマンドの完全なリファレンス
- [設定](configuration.md) - 設定ファイルと環境変数
- [トラブルシューティング](troubleshooting.md) - よくある問題と解決策

### パッケージ開発

- [パッケージの作成](creating-packages.md) - パッケージの作成と公開方法
- [パッケージ仕様](package-spec.md) - package.jsonのフォーマット
- [バージョニング](versioning.md) - セマンティックバージョニングとバージョン制約

### リファレンス

- [アーキテクチャ](architecture.md) - 内部アーキテクチャと設計
- [終了コード](exit-codes.md) - CLI終了コードリファレンス

## クイックリファレンス

### 基本コマンド

```bash
hpm init                              # 新しいpackage.jsonを作成
hpm install                           # すべての依存関係をインストール
hpm install owner/repo                # パッケージを追加してインストール
hpm install owner/repo@^1.0.0        # バージョン制約付きでインストール
hpm uninstall owner/repo              # パッケージを削除
hpm update                            # すべてのパッケージを更新
hpm list                              # インストール済みパッケージを表示
hpm run <script>                      # パッケージスクリプトを実行
```

### パッケージの識別

パッケージはGitHubの`owner/repo`形式を使用します：

```
hemlang/sprout          # Webフレームワーク
hemlang/json            # JSONユーティリティ
alice/http-client       # HTTPクライアントライブラリ
```

### バージョン制約

| 構文 | 意味 |
|------|------|
| `1.0.0` | 正確なバージョン |
| `^1.2.3` | 互換性あり (>=1.2.3 <2.0.0) |
| `~1.2.3` | パッチ更新 (>=1.2.3 <1.3.0) |
| `>=1.0.0` | 1.0.0以上 |
| `*` | 任意のバージョン |

## ヘルプの取得

- コマンドラインヘルプには `hpm --help` を使用してください
- コマンド固有のヘルプには `hpm <command> --help` を使用してください
- 問題の報告は [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues) まで

## ライセンス

hpmはMITライセンスの下で公開されています。
