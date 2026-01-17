# インストール

このガイドでは、システムにhpmをインストールする方法を説明します。

## クイックインストール（推奨）

1つのコマンドで最新リリースをインストール:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

これは自動的に:
- オペレーティングシステムを検出（Linux、macOS）
- アーキテクチャを検出（x86_64、arm64）
- 適切なビルド済みバイナリをダウンロード
- `/usr/local/bin`にインストール（必要に応じてsudoを使用）

### インストールオプション

```bash
# カスタム場所にインストール（sudoが不要）
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# 特定のバージョンをインストール
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# オプションの組み合わせ
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### サポートされるプラットフォーム

| プラットフォーム | アーキテクチャ | ステータス |
|----------|--------------|--------|
| Linux    | x86_64       | ✓ サポート |
| macOS    | x86_64       | ✓ サポート |
| macOS    | arm64 (M1/M2/M3) | ✓ サポート |
| Linux    | arm64        | ソースからビルド |

## ソースからビルド

ソースからビルドしたい場合、またはビルド済みバイナリでカバーされていないプラットフォームが必要な場合は、以下の手順に従ってください。

### 前提条件

hpmは最初に[Hemlock](https://github.com/hemlang/hemlock)がインストールされている必要があります。続行する前にHemlockのインストール手順に従ってください。

Hemlockがインストールされていることを確認:

```bash
hemlock --version
```

## インストール方法

### 方法1: Make Install

ソースからビルドしてインストール。

```bash
# リポジトリをクローン
git clone https://github.com/hemlang/hpm.git
cd hpm

# /usr/local/binにインストール（sudoが必要）
sudo make install
```

インストール後、動作を確認:

```bash
hpm --version
```

### 方法2: カスタム場所

カスタムディレクトリにインストール（sudoが不要）:

```bash
# リポジトリをクローン
git clone https://github.com/hemlang/hpm.git
cd hpm

# ~/.local/binにインストール
make install PREFIX=$HOME/.local

# または任意のカスタム場所
make install PREFIX=/opt/hemlock
```

カスタムbinディレクトリがPATHに含まれていることを確認:

```bash
# ~/.bashrcまたは~/.zshrcに追加
export PATH="$HOME/.local/bin:$PATH"
```

### 方法3: インストールせずに実行

hpmをインストールせずに直接実行できます:

```bash
# リポジトリをクローン
git clone https://github.com/hemlang/hpm.git
cd hpm

# ローカルラッパースクリプトを作成
make

# hpmディレクトリから実行
./hpm --help

# またはhemlockで直接実行
hemlock src/main.hml --help
```

### 方法4: 手動インストール

独自のラッパースクリプトを作成:

```bash
# 永続的な場所にクローン
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# ラッパースクリプトを作成
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## インストール変数

Makefileは以下の変数をサポート:

| 変数 | デフォルト | 説明 |
|----------|---------|-------------|
| `PREFIX` | `/usr/local` | インストールプレフィックス |
| `BINDIR` | `$(PREFIX)/bin` | バイナリディレクトリ |
| `HEMLOCK` | `hemlock` | hemlockインタプリタへのパス |

カスタム変数を使用した例:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## 仕組み

インストーラはhpmソースコードでHemlockインタプリタを呼び出すシェルラッパースクリプトを作成します:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

このアプローチ:
- コンパイルが不要
- 常に最新のソースコードを実行
- すべてのプラットフォームで確実に動作

## hpmの更新

hpmを最新バージョンに更新するには:

```bash
cd /path/to/hpm
git pull origin main

# パスが変更された場合は再インストール
sudo make install
```

## アンインストール

システムからhpmを削除:

```bash
cd /path/to/hpm
sudo make uninstall
```

または手動で削除:

```bash
sudo rm /usr/local/bin/hpm
```

## インストールの確認

インストール後、すべてが動作することを確認:

```bash
# バージョンを確認
hpm --version

# ヘルプを表示
hpm --help

# 初期化をテスト（空のディレクトリで）
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## トラブルシューティング

### "hemlock: command not found"

HemlockがインストールされていないかPATHにありません。まずHemlockをインストール:

```bash
# hemlockが存在するか確認
which hemlock

# 見つからない場合、https://github.com/hemlang/hemlockからHemlockをインストール
```

### "Permission denied"

システム全体へのインストールにはsudoを使用するか、ユーザーディレクトリにインストール:

```bash
# オプション1: sudoを使用
sudo make install

# オプション2: ユーザーディレクトリにインストール
make install PREFIX=$HOME/.local
```

### インストール後に"hpm: command not found"

PATHにインストールディレクトリが含まれていない可能性があります:

```bash
# hpmがどこにインストールされたか確認
ls -la /usr/local/bin/hpm

# カスタム場所を使用している場合はPATHに追加
export PATH="$HOME/.local/bin:$PATH"
```

## プラットフォーム固有の注意事項

### Linux

標準インストールはすべてのLinuxディストリビューションで動作します。一部のディストリビューションでは以下が必要な場合があります:

```bash
# Debian/Ubuntu: ビルド必須パッケージを確認
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

標準インストールが動作します。Homebrewを使用している場合:

```bash
# Xcodeコマンドラインツールを確認
xcode-select --install
```

### Windows (WSL)

hpmはWindows Subsystem for Linuxで動作します:

```bash
# WSLターミナルで
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## 次のステップ

インストール後:

1. [クイックスタート](quick-start.md) - 最初のプロジェクトを作成
2. [コマンドリファレンス](commands.md) - すべてのコマンドを学ぶ
3. [設定](configuration.md) - hpmを設定
