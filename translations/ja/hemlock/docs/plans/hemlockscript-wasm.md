# HemlockScript：Hemlock → WASM（Emscripten経由）

> ブラウザで動作するポータブルなHemlockプログラム。

## 目標

`hemlockc`にWASMコンパイルターゲットを追加し、Hemlockプログラムをブラウザやその他のWASMランタイム（Node/Deno/Cloudflare Workers）で実行可能にする。アプローチ：Hemlock → C（既存パイプライン） → WASM（Emscripten経由）、POSIX専用の組み込み関数をブラウザ互換のランタイムシムで置き換える。

**非目標：** コンパイラやランタイムをゼロから書き直すこと。既存の`hemlockc` Cコード生成と`libhemlock_runtime`を可能な限り活用する。

---

## アーキテクチャ

```
Hemlockソース (.hml)
        ↓
   hemlockc (既存フロントエンド + コード生成)
        ↓
   生成されたCコード (既存)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (WASM対応ランタイム)
        ↓
   program.wasm + program.js (ローダー/グルー)
        ↓
   ブラウザ / Node / Deno / WASMランタイム
```

重要なポイント：`hemlockc`はすでにポータブルなCを出力する。新しいバックエンドは不要で、WASM互換のランタイムライブラリとEmscriptenビルドパイプラインが必要。

---

## フェーズ1：最小限のWASMビルド（コア言語のみ）

**成果物：** `make wasm`が`.wasm` + `.js`バンドルを生成し、純粋な計算型Hemlockプログラムをブラウザで実行可能。

### 1.1 WASMランタイムシムレイヤーの作成

POSIX依存関数のスタブ/代替実装を持つ`runtime/src/wasm_shim.c`を作成。WASMをターゲットにする場合、POSIX実装の*代わりに*コンパイルされる。

### 1.2 ランタイムへの`#ifdef __EMSCRIPTEN__`ガードの追加

既存のランタイムソースファイルのPOSIX専用コードをプリプロセッサガードで囲む。

### 1.3 WASM専用Makefileターゲットの作成

### 1.4 WASMターゲットサポートのための`hemlockc`の変更

`--target wasm`フラグを追加。

### 1.5 HTMLテストハーネスの作成

### フェーズ1の成果物
- `make wasm-compile FILE=hello.hml`でブラウザで実行可能な出力を生成
- すべての純粋計算Hemlock機能が動作：変数、関数、クロージャ、制御フロー、パターンマッチング、オブジェクト、配列、文字列、数学、型システム
- `print()`がブラウザコンソール/HTML要素に出力
- 未サポート機能（FFI、ソケット、プロセス、シグナル）は明確なメッセージでパニック

---

## フェーズ2：ブラウザI/O & Stdlib

**成果物：** Hemlockプログラムがブラウザで有用な作業が可能 -- ファイルアクセス（仮想FS）、時間操作、ポータブルなstdlibモジュールが動作。

### 2.1 Emscripten仮想ファイルシステム

### 2.2 既にポータブルな22のstdlibモジュールの移植

### 2.3 時間モジュールの適応

### 2.4 env/os/argsモジュールの適応

---

## フェーズ3：JavaScript相互運用ブリッジ

**成果物：** Hemlock WASMプログラムがブラウザAPIとJavaScript関数を呼び出し可能、JavaScriptがHemlock関数を呼び出し可能。

### 3.1 JavaScriptブリッジ (`hemlock_js_bridge`)

### 3.2 エクスポート関数（Hemlock → JS）

### 3.3 ブラウザ向けネットワーキングモジュールの適応

### 3.4 暗号モジュールの適応

---

## フェーズ4：非同期 & スレッディング（ストレッチ）

**成果物：** Hemlockの`spawn`/`await`がWeb Workersを使用してブラウザで動作。

### 4.1 Web Workerベースのタスクスポーン

### 4.2 ブロッキング操作のためのAsyncify

---

## ファイル変更サマリー

### 新規ファイル
```
runtime/src/wasm_shim.c          — POSIX関数のWASMスタブ
runtime/src/wasm_bridge.c        — JS相互運用ブリッジ（フェーズ3）
wasm/                            — WASM出力ディレクトリ
wasm/index.html                  — テストハーネスHTMLページ
wasm/hemlock.js                  — オプションのJSラッパー/ローダーAPI
tests/wasm/                      — WASM固有テスト
tests/wasm/run_wasm_tests.sh     — テストランナー（Node.js使用）
```

### 変更ファイル
```
Makefile                         — wasm、wasm-compile、wasm-testターゲットの追加
runtime/Makefile                 — emcc/emarを使用したwasmビルドターゲットの追加
src/backends/compiler/main.c     — --target wasmフラグの追加
src/backends/compiler/codegen_program.c — WASMプリアンブル生成
runtime/src/builtins_process.c   — #ifdef __EMSCRIPTEN__ ガード
runtime/src/builtins_socket.c    — #ifdef __EMSCRIPTEN__ ガード
runtime/src/builtins_http.c      — #ifdef __EMSCRIPTEN__ ガード
runtime/src/builtins_ffi.c       — #ifdef __EMSCRIPTEN__ ガード
runtime/src/builtins_async.c     — #ifdef __EMSCRIPTEN__ ガード
runtime/src/builtins_io.c        — MEMFS/IDBFSのための#ifdef __EMSCRIPTEN__
runtime/src/builtins_time.c      — emscripten_sleepのための#ifdef
runtime/src/builtins_crypto.c    — Web Cryptoスタブのための#ifdef
runtime/include/hemlock_runtime.h — WASM機能検出マクロ
```

---

## すぐに動作するもの（変更不要）

これらのHemlock機能は標準Cにコンパイルされ、Emscriptenがネイティブに処理：

- すべての算術、ビット単位、論理演算子
- 変数、スコープ、クロージャ
- 関数、再帰、式本体関数
- if/else、while、for、loop、switch、パターンマッチング
- オブジェクト、配列、文字列（19+23メソッドすべて）
- 型注釈とランタイム型チェック
- try/catch/finally/throw
- defer
- テンプレート文字列
- Null合体（`??`、`?.`、`??=`）
- 名前付き引数
- 複合型、型エイリアス
- `print()`、`eprint()`（Emscriptenのコンソールマッピング経由）
- `alloc()`/`free()`/`buffer()`（リニアメモリ）
- `typeof()`、`len()`、`sizeof()`
- 数学組み込み（sin、cos、sqrtなど）
- すべての参照カウント/メモリ管理

---

## フェーズごとの推定規模

| フェーズ | 規模 | 依存関係 |
|-------|-------|-------------|
| **フェーズ1** | 新規C約800行、#ifdefガード約200行、Makefile変更 | Emscripten SDK |
| **フェーズ2** | C約200行、stdlibテスト、Makefile | フェーズ1 |
| **フェーズ3** | C約600行（ブリッジ）、Hemlock約200行（stdlib） | フェーズ1 |
| **フェーズ4** | C約1000行（Workerスレッディング）、複雑 | フェーズ1+3 |

推奨順序：フェーズ1 → フェーズ2 → フェーズ3 → フェーズ4

フェーズ1だけで計算ワークロード向けの有用な「ブラウザでのHemlock」が得られます。フェーズ2-4はI/Oと相互運用を段階的に追加します。
