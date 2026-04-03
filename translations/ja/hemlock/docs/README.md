# Hemlock ドキュメント

Hemlock プログラミング言語のドキュメントへようこそ!

> 安全でないものを安全に書くための、小さくて安全でない言語。

## 目次

### はじめに
- [インストール](getting-started/installation.md) - Hemlock のビルドとインストール
- [クイックスタート](getting-started/quick-start.md) - 初めての Hemlock プログラム
- [チュートリアル](getting-started/tutorial.md) - Hemlock の基本をステップバイステップで学ぶ
- [学習パス](getting-started/learning-paths.md) - 目標に合わせた学習の道筋を選ぶ

### プログラミング初心者の方へ
- [用語集](glossary.md) - プログラミング用語のわかりやすい定義

### 言語ガイド
- [構文の概要](language-guide/syntax.md) - 基本的な構文と構造
- [型システム](language-guide/types.md) - プリミティブ型、型推論、型変換
- [メモリ管理](language-guide/memory.md) - ポインタ、バッファ、手動メモリ管理
- [文字列](language-guide/strings.md) - UTF-8 文字列と操作
- [ルーン](language-guide/runes.md) - Unicode コードポイントと文字処理
- [制御フロー](language-guide/control-flow.md) - if/else、ループ、switch、演算子
- [関数](language-guide/functions.md) - 関数、クロージャ、再帰
- [オブジェクト](language-guide/objects.md) - オブジェクトリテラル、メソッド、ダックタイピング
- [配列](language-guide/arrays.md) - 動的配列と操作
- [エラーハンドリング](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [モジュール](language-guide/modules.md) - インポート/エクスポートシステムとパッケージインポート

### 上級トピック
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Emscripten 経由でブラウザで Hemlock を実行
- [非同期と並行処理](advanced/async-concurrency.md) - async/await による真のマルチスレッド
- [バンドルとパッケージング](advanced/bundling-packaging.md) - バンドルとスタンドアロン実行ファイルの作成
- [外部関数インターフェース](advanced/ffi.md) - 共有ライブラリから C 関数を呼び出す
- [ファイル I/O](advanced/file-io.md) - ファイル操作とリソース管理
- [シグナルハンドリング](advanced/signals.md) - POSIX シグナルハンドリング
- [コマンドライン引数](advanced/command-line-args.md) - プログラム引数へのアクセス
- [コマンド実行](advanced/command-execution.md) - シェルコマンドの実行
- [プロファイリング](advanced/profiling.md) - CPU 時間、メモリ追跡、リーク検出

### API リファレンス
- [型システムリファレンス](reference/type-system.md) - 完全な型リファレンス
- [演算子リファレンス](reference/operators.md) - すべての演算子と優先順位
- [組み込み関数](reference/builtins.md) - グローバル関数と定数
- [文字列 API](reference/string-api.md) - 文字列のメソッドとプロパティ
- [配列 API](reference/array-api.md) - 配列のメソッドとプロパティ
- [メモリ API](reference/memory-api.md) - メモリの割り当てと操作
- [ファイル API](reference/file-api.md) - ファイル I/O メソッド
- [並行処理 API](reference/concurrency-api.md) - タスクとチャネル

### 設計と哲学
- [設計哲学](design/philosophy.md) - 基本原則と目標
- [実装の詳細](design/implementation.md) - Hemlock の内部動作

### コントリビュート
- [コントリビュートガイドライン](contributing/guidelines.md) - コントリビュートの方法
- [テストガイド](contributing/testing.md) - テストの作成と実行

## クイックリファレンス

### Hello World
```hemlock
print("Hello, World!");
```

### 基本型
```hemlock
let x: i32 = 42;           // 32ビット符号付き整数
let y: u8 = 255;           // 8ビット符号なし整数
let pi: f64 = 3.14159;     // 64ビット浮動小数点数
let name: string = "Alice"; // UTF-8 文字列
let flag: bool = true;     // ブーリアン
let ch: rune = '🚀';       // Unicode コードポイント
```

### メモリ管理
```hemlock
// 安全なバッファ（推奨）
let buf = buffer(64);
buf[0] = 65;
free(buf);

// 生ポインタ（上級者向け）
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### 非同期/並行処理
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## 哲学

Hemlock は常に**暗黙より明示**を重視します:
- セミコロンは必須
- 手動メモリ管理（GC なし）
- オプションの型注釈とランタイムチェック
- 安全でない操作は許可（あなたの責任）

安全であるためのツール（`buffer`、型注釈、境界チェック）を提供しますが、それらの使用を強制はしません（`ptr`、手動メモリ管理、安全でない操作）。

## ヘルプ

- **ソースコード**: [GitHub リポジトリ](https://github.com/hemlang/hemlock)
- **パッケージマネージャ**: [hpm](https://github.com/hemlang/hpm) - Hemlock パッケージマネージャ
- **Issues**: バグ報告と機能リクエスト
- **サンプル**: `examples/` ディレクトリを参照
- **テスト**: 使用例は `tests/` ディレクトリを参照

## ライセンス

Hemlock は MIT ライセンスの下で公開されています。
