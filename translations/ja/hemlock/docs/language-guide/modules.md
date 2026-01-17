# Hemlockモジュールシステム

このドキュメントでは、Hemlockに実装されたES6スタイルのimport/exportモジュールシステムについて説明します。

## 概要

HemlockはES6スタイルのimport/export構文を持つファイルベースのモジュールシステムをサポートしています。モジュールは：
- **シングルトン**：各モジュールは1回だけロードされキャッシュされる
- **ファイルベース**：モジュールはディスク上の.hmlファイルに対応
- **明示的インポート**：依存関係はimport文で宣言
- **トポロジカル実行**：依存関係は依存先より先に実行

パッケージ管理とサードパーティ依存関係については、[hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm)を参照してください。

## 構文

### Export文

**インライン名前付きエクスポート：**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**エクスポートリスト：**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Export Extern（FFI関数）：**
```hemlock
import "libc.so.6";

// 他のモジュールで使用するためにFFI関数をエクスポート
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

FFI関数のエクスポートの詳細については、[FFIドキュメント](../advanced/ffi.md#exporting-ffi-functions)を参照してください。

**Export Define（構造体型）：**
```hemlock
// 構造体型定義をエクスポート
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**重要：** エクスポートされた構造体型は、モジュールがロードされるとグローバルに登録されます。モジュールから何かをインポートすると自動的に利用可能になります - 名前で明示的にインポートする必要はありません（できません）：

```hemlock
// 良い - 構造体型はどのインポート後も自動的に利用可能
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // 動作する！

// 悪い - 構造体型を明示的にインポートできない
import { Vector2 } from "./my_module.hml";  // エラー：未定義の変数 'Vector2'
```

構造体型のエクスポートの詳細については、[FFIドキュメント](../advanced/ffi.md#exporting-struct-types)を参照してください。

**再エクスポート：**
```hemlock
// 別のモジュールから再エクスポート
export { add, subtract } from "./math.hml";
```

### Import文

**名前付きインポート：**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**名前空間インポート：**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**エイリアス：**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## モジュール解決

### パスの種類

**相対パス：**
```hemlock
import { foo } from "./module.hml";       // 同じディレクトリ
import { bar } from "../parent.hml";      // 親ディレクトリ
import { baz } from "./sub/nested.hml";   // サブディレクトリ
```

**絶対パス：**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**拡張子の処理：**
- `.hml`拡張子は省略可能 - 自動的に追加される
- `./math`は`./math.hml`に解決

## 機能

### 循環依存の検出

モジュールシステムは循環依存を検出してエラーを報告します：

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### モジュールキャッシング

モジュールは1回ロードされキャッシュされます。同じモジュールの複数のインポートは同じインスタンスを返します：

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // 同じインスタンス！
print(count);  // まだ1（共有状態）
```

### インポートの不変性

インポートされたバインディングは再代入できません：

```hemlock
import { add } from "./math.hml";
add = fn() { };  // エラー：インポートされたバインディングを再代入できない
```

## 実装の詳細

### アーキテクチャ

**ファイル：**
- `include/module.h` - モジュールシステムAPI
- `src/module.c` - モジュールのロード、キャッシング、実行
- `src/parser.c`のパーササポート
- `src/interpreter/runtime.c`のランタイムサポート

**主要コンポーネント：**
1. **ModuleCache**：絶対パスでインデックスされたロード済みモジュールを維持
2. **Module**：ASTとエクスポートを持つロード済みモジュールを表す
3. **パス解決**：相対/絶対パスを正規パスに解決
4. **トポロジカル実行**：依存順序でモジュールを実行

### モジュールロードプロセス

1. **パースフェーズ**：モジュールファイルをトークン化してパース
2. **依存関係解決**：インポートされたモジュールを再帰的にロード
3. **サイクル検出**：モジュールがすでにロード中かチェック
4. **キャッシング**：絶対パスでキャッシュにモジュールを格納
5. **実行フェーズ**：トポロジカル順序（依存関係が先）で実行

### API

```c
// 高レベルAPI
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// 低レベルAPI
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## テスト

テストモジュールは`tests/modules/`と`tests/parity/modules/`にあります：

- `math.hml` - エクスポートを持つ基本モジュール
- `test_import_named.hml` - 名前付きインポートテスト
- `test_import_namespace.hml` - 名前空間インポートテスト
- `test_import_alias.hml` - インポートエイリアステスト
- `export_extern.hml` - export extern FFI関数テスト（Linux）

## パッケージインポート（hpm）

[hpm](https://github.com/hemlang/hpm)がインストールされていれば、GitHubからサードパーティパッケージをインポートできます：

```hemlock
// パッケージルートからインポート（package.jsonの"main"を使用）
import { app, router } from "hemlang/sprout";

// サブパスからインポート
import { middleware } from "hemlang/sprout/middleware";

// 標準ライブラリ（Hemlockに組み込み）
import { HashMap } from "@stdlib/collections";
```

パッケージは`hem_modules/`にインストールされ、GitHub `owner/repo`構文を使用して解決されます。

```bash
# パッケージをインストール
hpm install hemlang/sprout

# バージョン制約付きでインストール
hpm install hemlang/sprout@^1.0.0
```

詳細は[hpmドキュメント](https://github.com/hemlang/hpm)を参照してください。

## 現在の制限事項

1. **動的インポートなし**：ランタイム関数としての`import()`はサポートされていない
2. **条件付きエクスポートなし**：エクスポートはトップレベルでなければならない
3. **静的ライブラリパス**：FFIライブラリインポートは静的パスを使用（プラットフォーム固有）

## 将来の作業

- `import()`関数による動的インポート
- 条件付きエクスポート
- モジュールメタデータ（`import.meta`）
- ツリーシェイキングとデッドコード除去

## 例

動作するモジュールシステムの例は`tests/modules/`を参照してください。

モジュール構造の例：
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml（バレルモジュール）
└── utils/
    └── helpers.hml
```

使用例：
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml（バレル）
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
