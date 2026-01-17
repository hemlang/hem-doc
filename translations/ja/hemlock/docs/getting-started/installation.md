# インストール

このガイドでは、お使いのシステムにHemlockをビルドしてインストールする方法を説明します。

## クイックインストール（推奨）

Hemlockをインストールする最も簡単な方法は、ワンライナーインストールスクリプトを使用することです：

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

これにより、お使いのプラットフォーム（LinuxまたはmacOS、x86_64またはarm64）向けの最新のビルド済みバイナリがダウンロードおよびインストールされます。

### インストールオプション

```bash
# カスタムプレフィックスにインストール（デフォルト：~/.local）
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# 特定のバージョンをインストール
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# シェルのPATHを自動的に更新してインストール
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

インストール後、動作を確認します：

```bash
hemlock --version
```

---

## ソースからのビルド

ビルド済みバイナリがお使いのシステムで動作しない場合、またはソースからビルドしたい場合は、以下の手順に従ってください。

## 前提条件

### 必要な依存関係

Hemlockのビルドには以下の依存関係が必要です：

- **Cコンパイラ**: GCCまたはClang（C11標準）
- **Make**: GNU Make
- **libffi**: 外部関数インターフェースライブラリ（FFIサポート用）
- **OpenSSL**: 暗号化ライブラリ（ハッシュ関数用：md5、sha1、sha256）
- **libwebsockets**: WebSocketおよびHTTPクライアント/サーバーサポート
- **zlib**: 圧縮ライブラリ

### 依存関係のインストール

**macOS:**
```bash
# Homebrewがまだインストールされていない場合はインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Xcode Command Line Toolsをインストール
xcode-select --install

# Homebrew経由で依存関係をインストール
brew install libffi openssl@3 libwebsockets
```

**macOSユーザーへの注意**: MakefileはHomebrewのインストールを自動的に検出し、正しいinclude/ライブラリパスを設定します。HemlockはIntel（x86_64）とApple Silicon（arm64）の両方のアーキテクチャをサポートしています。

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## ソースからのビルド

### 1. リポジトリをクローン

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Hemlockをビルド

```bash
make
```

これによりHemlockインタプリタがコンパイルされ、実行ファイルがカレントディレクトリに配置されます。

### 3. インストールの確認

```bash
./hemlock --version
```

Hemlockのバージョン情報が表示されるはずです。

### 4. ビルドのテスト

すべてが正しく動作することを確認するためにテストスイートを実行します：

```bash
make test
```

すべてのテストがパスするはずです。失敗がある場合は、issueとして報告してください。

## システム全体へのインストール（オプション）

Hemlockをシステム全体（例：`/usr/local/bin`）にインストールするには：

```bash
sudo make install
```

これにより、フルパスを指定せずにどこからでも`hemlock`を実行できるようになります。

## Hemlockの実行

### インタラクティブREPL

Read-Eval-Print Loopを開始します：

```bash
./hemlock
```

プロンプトが表示され、Hemlockコードを入力できます：

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

REPLを終了するには`Ctrl+D`または`Ctrl+C`を使用します。

### プログラムの実行

Hemlockスクリプトを実行：

```bash
./hemlock program.hml
```

コマンドライン引数付きで実行：

```bash
./hemlock program.hml arg1 arg2 "argument with spaces"
```

## ディレクトリ構造

ビルド後のHemlockディレクトリは次のようになります：

```
hemlock/
├── hemlock           # コンパイル済みインタプリタ実行ファイル
├── src/              # ソースコード
├── include/          # ヘッダーファイル
├── tests/            # テストスイート
├── examples/         # サンプルプログラム
├── docs/             # ドキュメント
├── stdlib/           # 標準ライブラリ
├── Makefile          # ビルド設定
└── README.md         # プロジェクトREADME
```

## ビルドオプション

### デバッグビルド

デバッグシンボル付きで最適化なしでビルド：

```bash
make debug
```

### クリーンビルド

すべてのコンパイル済みファイルを削除：

```bash
make clean
```

スクラッチから再ビルド：

```bash
make clean && make
```

## トラブルシューティング

### macOS: ライブラリが見つからないエラー

ライブラリが見つからないエラー（`-lcrypto`、`-lffi`など）が発生した場合：

1. Homebrewの依存関係がインストールされていることを確認：
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Homebrewのパスを確認：
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Makefileはこれらのパスを自動検出するはずです。検出されない場合は、`brew`がPATHにあることを確認：
   ```bash
   which brew
   ```

### macOS: BSD型エラー（`u_int`、`u_char`が見つからない）

`u_int`や`u_char`のような不明な型名に関するエラーが表示された場合：

1. これはv1.0.0以降で`_POSIX_C_SOURCE`の代わりに`_DARWIN_C_SOURCE`を使用することで修正されています
2. 最新バージョンのコードを使用していることを確認
3. クリーンして再ビルド：
   ```bash
   make clean && make
   ```

### Linux: libffiが見つからない

`ffi.h`や`-lffi`が見つからないエラーが発生した場合：

1. `libffi-dev`がインストールされていることを確認（上記の依存関係を参照）
2. `pkg-config`で見つけられるか確認：
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. 見つからない場合は、`PKG_CONFIG_PATH`を設定する必要があるかもしれません：
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### コンパイルエラー

コンパイルエラーが発生した場合：

1. C11互換のコンパイラがあることを確認
2. macOSでは、Clang（デフォルト）を使用してみてください：
   ```bash
   make CC=clang
   ```
3. Linuxでは、GCCを使用してみてください：
   ```bash
   make CC=gcc
   ```
4. すべての依存関係がインストールされていることを確認
5. スクラッチから再ビルドを試してください：
   ```bash
   make clean && make
   ```

### テストの失敗

テストが失敗した場合：

1. 最新バージョンのコードを使用していることを確認
2. スクラッチから再ビルドを試してください：
   ```bash
   make clean && make test
   ```
3. macOSでは、最新のXcode Command Line Toolsがあることを確認：
   ```bash
   xcode-select --install
   ```
4. GitHubで以下の情報を含めてissueを報告してください：
   - お使いのプラットフォーム（macOSバージョン / Linuxディストリビューション）
   - アーキテクチャ（x86_64 / arm64）
   - テスト出力
   - `make -v`と`gcc --version`（または`clang --version`）の出力

## 次のステップ

- [クイックスタートガイド](quick-start.md) - 最初のHemlockプログラムを書く
- [チュートリアル](tutorial.md) - ステップバイステップでHemlockを学ぶ
- [言語ガイド](../language-guide/syntax.md) - Hemlockの機能を探索
