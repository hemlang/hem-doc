# パッケージの作成

このガイドでは、Hemlockパッケージの作成、構造化、公開方法について説明します。

## 概要

hpmはGitHubをパッケージレジストリとして使用します。パッケージはGitHubの`owner/repo`パスで識別され、バージョンはGitタグです。公開は単にタグ付きリリースをプッシュするだけです。

## 新しいパッケージの作成

### 1. パッケージの初期化

新しいディレクトリを作成して初期化:

```bash
mkdir my-package
cd my-package
hpm init
```

プロンプトに答えます:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. プロジェクト構造の作成

パッケージの推奨構造:

```
my-package/
├── package.json          # パッケージマニフェスト
├── README.md             # ドキュメント
├── LICENSE               # ライセンスファイル
├── src/
│   ├── index.hml         # メインエントリポイント（パブリックAPIをエクスポート）
│   ├── utils.hml         # 内部ユーティリティ
│   └── types.hml         # 型定義
└── test/
    ├── framework.hml     # テストフレームワーク
    └── test_utils.hml    # テスト
```

### 3. パブリックAPIの定義

**src/index.hml** - メインエントリポイント:

```hemlock
// パブリックAPIを再エクスポート
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// 直接エクスポート
export fn create(options: Options): Config {
    // 実装
}

export fn validate(config: Config): bool {
    // 実装
}
```

### 4. package.jsonの記述

完全なpackage.jsonの例:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## パッケージの命名

### 要件

- `owner/repo`形式である必要あり
- `owner`はGitHubユーザー名または組織である必要あり
- `repo`はリポジトリ名である必要あり
- 複数単語の名前には小文字とハイフンを使用

### 良い名前

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### 避けるべき名前

```
my-package          # ownerがない
alice/MyPackage     # PascalCase
alice/my_package    # アンダースコア
```

## パッケージ構造のベストプラクティス

### エントリポイント

package.jsonの`main`フィールドがエントリポイントを指定:

```json
{
  "main": "src/index.hml"
}
```

このファイルでパブリックAPIをエクスポート:

```hemlock
// ユーザーが必要とするすべてをエクスポート
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// 型
export type { Config, Options } from "./types.hml";
```

### 内部 vs パブリック

内部実装の詳細をプライベートに保つ:

```
src/
├── index.hml          # パブリック: エクスポートされるAPI
├── parser.hml         # パブリック: index.hmlで使用
├── formatter.hml      # パブリック: index.hmlで使用
└── internal/
    ├── helpers.hml    # プライベート: 内部使用のみ
    └── constants.hml  # プライベート: 内部使用のみ
```

ユーザーはパッケージルートからインポート:

```hemlock
// 良い - パブリックAPIからインポート
import { parse, Parser } from "yourusername/my-package";

// 可能 - サブパスインポート
import { validate } from "yourusername/my-package/validator";

// 非推奨 - 内部へのアクセス
import { helper } from "yourusername/my-package/internal/helpers";
```

### サブパスエクスポート

サブパスからのインポートをサポート:

```
src/
├── index.hml              # メインエントリ
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

ユーザーは以下のようにインポート可能:

```hemlock
import { parse } from "yourusername/my-package";           // メイン
import { Parser } from "yourusername/my-package/parser";   // サブパス
import { format } from "yourusername/my-package/formatter";
```

## 依存関係

### 依存関係の追加

```bash
# ランタイム依存関係
hpm install hemlang/json

# 開発依存関係
hpm install hemlang/test-utils --dev
```

### 依存関係のベストプラクティス

1. **ほとんどの依存関係にキャレット範囲を使用**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **必要な場合のみバージョンを固定**（APIが不安定な場合）:
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **過度に制限的な範囲を避ける**:
   ```json
   // 悪い: 制限しすぎ
   "hemlang/json": ">=1.2.3 <1.2.5"

   // 良い: 互換性のある更新を許可
   "hemlang/json": "^1.2.3"
   ```

4. **開発依存関係を分離**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## パッケージのテスト

### テストの作成

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### テストの実行

テストスクリプトを追加:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

以下で実行:

```bash
hpm test
```

## 公開

### 前提条件

1. パッケージ名に一致するGitHubリポジトリを作成
2. `package.json`が完全で有効であることを確認
3. すべてのテストが合格

### 公開プロセス

公開は単にGitタグをプッシュするだけ:

```bash
# 1. すべてがコミットされていることを確認
git add .
git commit -m "Prepare v1.0.0 release"

# 2. バージョンタグを作成（'v'で始まる必要あり）
git tag v1.0.0

# 3. コードとタグをプッシュ
git push origin main
git push origin v1.0.0
# または一度にすべてのタグをプッシュ
git push origin main --tags
```

### バージョンタグ

タグは`vX.Y.Z`形式に従う必要あり:

```bash
git tag v1.0.0      # リリース
git tag v1.0.1      # パッチ
git tag v1.1.0      # マイナー
git tag v2.0.0      # メジャー
git tag v1.0.0-beta.1  # プレリリース
```

### リリースチェックリスト

新しいバージョンを公開する前に:

1. package.jsonの**バージョンを更新**
2. **テストを実行**: `hpm test`
3. **CHANGELOG**を更新（ある場合）
4. APIが変更された場合は**README**を更新
5. **変更をコミット**
6. **タグを作成**
7. **GitHubにプッシュ**

### 自動化の例

リリーススクリプトを作成:

```bash
#!/bin/bash
# release.sh - 新しいバージョンをリリース

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# テストを実行
hpm test || exit 1

# package.jsonのバージョンを更新
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# コミットとタグ
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# プッシュ
git push origin main --tags

echo "Released v$VERSION"
```

## ユーザーによるパッケージのインストール

公開後、ユーザーは以下でインストール可能:

```bash
# 最新バージョン
hpm install yourusername/my-package

# 特定のバージョン
hpm install yourusername/my-package@1.0.0

# バージョン制約
hpm install yourusername/my-package@^1.0.0
```

そしてインポート:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## ドキュメント

### README.md

すべてのパッケージにはREADMEが必要:

```markdown
# my-package

このパッケージが何をするかの簡単な説明。

## インストール

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## 使用方法

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

入力文字列を解析します。

### stringify(obj: any): string

オブジェクトを文字列に変換します。

## ライセンス

MIT
```

### APIドキュメント

すべてのパブリックエクスポートをドキュメント化:

```hemlock
/// 入力文字列を構造化されたResultに解析します。
///
/// # 引数
/// * `input` - 解析する文字列
///
/// # 戻り値
/// 解析されたデータまたはエラーを含むResult
///
/// # 例
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // 実装
}
```

## バージョニングガイドライン

[セマンティックバージョニング](https://semver.org/)に従う:

- **MAJOR**（1.0.0 → 2.0.0）: 破壊的変更
- **MINOR**（1.0.0 → 1.1.0）: 新機能、後方互換
- **PATCH**（1.0.0 → 1.0.1）: バグ修正、後方互換

### いつバンプするか

| 変更タイプ | バージョンバンプ |
|-------------|--------------|
| 破壊的なAPI変更 | MAJOR |
| 関数/型の削除 | MAJOR |
| 関数シグネチャの変更 | MAJOR |
| 新しい関数の追加 | MINOR |
| 新しい機能の追加 | MINOR |
| バグ修正 | PATCH |
| ドキュメント更新 | PATCH |
| 内部リファクタリング | PATCH |

## 参照

- [パッケージ仕様](package-spec.md) - 完全なpackage.jsonリファレンス
- [バージョニング](versioning.md) - セマンティックバージョニングの詳細
- [設定](configuration.md) - GitHub認証
