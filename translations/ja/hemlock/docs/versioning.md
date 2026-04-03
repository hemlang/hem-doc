# Hemlockバージョニング

このドキュメントでは、Hemlockのバージョニング戦略について説明します。

## バージョンフォーマット

Hemlockは**セマンティックバージョニング**（SemVer）を使用します：

```
MAJOR.MINOR.PATCH
```

| コンポーネント | インクリメントするタイミング |
|----------------|------------------------------|
| **MAJOR** | 言語セマンティクス、stdlib API、またはバイナリフォーマットへの破壊的変更 |
| **MINOR** | 新機能、後方互換性のある追加 |
| **PATCH** | バグ修正、パフォーマンス改善、ドキュメント |

## 統一バージョニング

すべてのHemlockコンポーネントは**単一のバージョン番号**を共有します：

- **インタプリタ** (`hemlock`)
- **コンパイラ** (`hemlockc`)
- **LSPサーバー** (`hemlock --lsp`)
- **標準ライブラリ** (`@stdlib/*`)

バージョンは `include/version.h` で定義されています：

```c
#define HEMLOCK_VERSION_MAJOR 1
#define HEMLOCK_VERSION_MINOR 8
#define HEMLOCK_VERSION_PATCH 7

#define HEMLOCK_VERSION "1.8.7"
```

### バージョンの確認

```bash
# インタプリタのバージョン
hemlock --version

# コンパイラのバージョン
hemlockc --version
```

## 互換性の保証

### MAJORバージョン内

- `1.x.0` で動作するソースコードは `1.x.y`（任意のパッチ）でも動作します
- `1.0.x` で動作するソースコードは `1.y.z`（任意のマイナー/パッチ）でも動作します
- コンパイル済みの `.hmlb` バンドルは同一MAJORバージョン内で互換性があります
- 標準ライブラリのAPIは安定しています（追加のみ、削除なし）

### MAJORバージョン間

- 破壊的変更はリリースノートに記載されます
- 重要な変更にはマイグレーションガイドが提供されます
- 非推奨の機能は削除前に少なくとも1つのマイナーリリースで警告されます

## バイナリフォーマットのバージョニング

Hemlockはバイナリフォーマットに別個のバージョン番号を使用します：

| フォーマット | バージョン | 場所 |
|-------------|-----------|------|
| `.hmlc` (ASTバンドル) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (圧縮バンドル) | HMLCと同じ | zlib圧縮を使用 |
| `.hmlp` (パッケージ実行ファイル) | マジック: `HMLP` | 自己完結型フォーマット |

バイナリフォーマットのバージョンは、シリアライゼーションの変更時に独立してインクリメントされます。

## 標準ライブラリのバージョニング

標準ライブラリ（`@stdlib/*`）は**メインリリースと共に**バージョニングされます：

```hemlock
// 常にHemlockインストールにバンドルされたstdlibを使用します
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Stdlibの互換性

- 新しいモジュールはMINORリリースで追加される場合があります
- 新しい関数はMINORリリースで既存のモジュールに追加される場合があります
- 関数シグネチャはMAJORバージョン内で安定しています
- 非推奨の関数は削除前にマークおよび文書化されます

## バージョン履歴

| バージョン | 日付 | ハイライト |
|-----------|------|-----------|
| **1.8.7** | 2026 | Fix multi-argument print/eprint in compiler codegen |
| **1.8.6** | 2026 | Fix segfault in hml_string_append_inplace for SSO strings |
| **1.8.5** | 2026 | 5 new array methods (every, some, indexOf, sort, fill), major performance optimizations, memory leak fixes |
| **1.8.4** | 2026 | Graceful handling for reserved keywords (def, func, var, class), fix flaky CI tests |
| **1.8.3** | 2026 | Code polish: consolidate magic numbers, standardize error messages |
| **1.8.2** | 2026 | Memory leak prevention: exception-safe eval, task/channel cleanup, optimizer fixes |
| **1.8.1** | 2026 | Fix use-after-free bug in function return value handling |
| **1.8.0** | 2026 | Pattern matching, arena allocator, memory leak fixes |
| **1.7.5** | 2026 | Fix formatter else-if indentation bug |
| **1.7.4** | 2026 | Formatter improvements: function parameter, binary expr, import, and method chain line breaking |
| **1.7.3** | 2026 | Fix formatter comment and blank line preservation |
| **1.7.2** | 2026 | Maintenance release |
| **1.7.1** | 2026 | Single-line if/while/for statements (braceless syntax) |
| **1.7.0** | 2026 | Type aliases, function types, const params, method signatures, loop labels, named args, null coalescing |
| **1.6.7** | 2026 | Octal literals, block comments, hex/unicode escapes, numeric separators |
| **1.6.6** | 2026 | Float literals without leading zero, fix strength reduction bug |
| **1.6.5** | 2026 | Fix for-in loop syntax without 'let' keyword |
| **1.6.4** | 2026 | Hotfix release |
| **1.6.3** | 2026 | Fix runtime method dispatch for file, channel, socket types |
| **1.6.2** | 2026 | Patch release |
| **1.6.1** | 2026 | Patch release |
| **1.6.0** | 2025 | Compile-time type checking in hemlockc, LSP integration, compound bitwise operators (`&=`, `\|=`, `^=`, `<<=`, `>>=`, `%=`) |
| **1.5.0** | 2024 | Full type system, async/await, atomics, 39 stdlib modules, FFI struct support, 99 parity tests |
| **1.3.0** | 2025 | Proper lexical block scoping (JS-like let/const semantics), per-iteration loop closures |
| **1.2.3** | 2025 | Import star syntax (`import * from`) |
| **1.2.2** | 2025 | Add `export extern` support, cross-platform test fixes |
| **1.2.1** | 2025 | Fix macOS test failures (RSA key generation, directory symlinks) |
| **1.2.0** | 2025 | AST optimizer, apply() builtin, unbuffered channels, 7 new stdlib modules, 97 parity tests |
| **1.1.3** | 2025 | Documentation updates, consistency fixes |
| **1.1.1** | 2025 | Bug fixes and improvements |
| **1.1.0** | 2024 | Unified versioning across all components |
| **1.0.x** | 2024 | Initial release series |

## リリースプロセス

1. `include/version.h` でバージョンをバンプ
2. 変更履歴を更新
3. 完全なテストスイートを実行 (`make test-all`)
4. gitでリリースをタグ付け
5. リリースアーティファクトをビルド

## 互換性の確認

特定のHemlockバージョンでコードが動作するか確認するには：

```bash
# インストールされたバージョンに対してテストを実行
make test

# インタプリタとコンパイラ間のパリティを確認
make parity
```

## 将来: プロジェクトマニフェスト

将来のリリースでは、バージョン制約のためのオプションのプロジェクトマニフェストが導入される可能性があります：

```hemlock
// 仮想的な project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

これはまだ実装されていませんが、ロードマップの一部です。
