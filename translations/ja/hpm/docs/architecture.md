# アーキテクチャ

hpmの内部アーキテクチャと設計。このドキュメントは、貢献者およびhpmの動作に興味のある方向けです。

## 概要

hpmはHemlockで書かれており、パッケージ管理の様々な側面を処理するいくつかのモジュールで構成されています:

```
src/
├── main.hml        # CLIエントリポイントとコマンドルーティング
├── manifest.hml    # package.jsonの処理
├── lockfile.hml    # package-lock.jsonの処理
├── semver.hml      # セマンティックバージョニング
├── resolver.hml    # 依存関係解決
├── github.hml      # GitHub APIクライアント
├── installer.hml   # パッケージのダウンロードと展開
└── cache.hml       # グローバルキャッシュ管理
```

## モジュールの責務

### main.hml

CLIアプリケーションのエントリポイント。

**責務:**
- コマンドライン引数の解析
- 適切なハンドラへのコマンドルーティング
- ヘルプとバージョン情報の表示
- グローバルフラグの処理（--verbose、--dry-runなど）
- 適切なコードでの終了

**主要関数:**
- `main()` - エントリポイント、引数を解析してコマンドをディスパッチ
- `cmd_init()` - `hpm init`を処理
- `cmd_install()` - `hpm install`を処理
- `cmd_uninstall()` - `hpm uninstall`を処理
- `cmd_update()` - `hpm update`を処理
- `cmd_list()` - `hpm list`を処理
- `cmd_outdated()` - `hpm outdated`を処理
- `cmd_run()` - `hpm run`を処理
- `cmd_why()` - `hpm why`を処理
- `cmd_cache()` - `hpm cache`を処理

**コマンドショートカット:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

`package.json`ファイルの読み書きを処理。

**責務:**
- package.jsonの読み書き
- パッケージ構造の検証
- 依存関係の管理
- パッケージ指定子（owner/repo@version）の解析

**主要関数:**
```hemlock
create_default(): Manifest           // 空のマニフェストを作成
read_manifest(): Manifest            // ファイルから読み込み
write_manifest(m: Manifest)          // ファイルに書き込み
validate(m: Manifest): bool          // 構造を検証
get_all_dependencies(m): Map         // deps + devDepsを取得
add_dependency(m, pkg, ver, dev)     // 依存関係を追加
remove_dependency(m, pkg)            // 依存関係を削除
parse_specifier(spec): (name, ver)   // "owner/repo@^1.0.0"を解析
split_name(name): (owner, repo)      // "owner/repo"を解析
```

**マニフェスト構造:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

再現可能なインストールのための`package-lock.json`ファイルを管理。

**責務:**
- ロックファイルの作成/読み取り/書き込み
- 解決された正確なバージョンの追跡
- ダウンロードURLと整合性ハッシュの保存
- 孤立した依存関係の削除

**主要関数:**
```hemlock
create_empty(): Lockfile              // 空のロックファイルを作成
read_lockfile(): Lockfile             // ファイルから読み込み
write_lockfile(l: Lockfile)           // ファイルに書き込み
create_entry(ver, url, hash, deps)    // ロックエントリを作成
get_locked(l, pkg): LockEntry?        // ロックされたバージョンを取得
set_locked(l, pkg, entry)             // ロックされたバージョンを設定
remove_locked(l, pkg)                 // エントリを削除
prune(l, keep: Set)                   // 孤立を削除
needs_update(l, m): bool              // 同期が取れているかチェック
```

**ロックファイル構造:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // ダウンロードURL
    integrity: string,    // SHA256ハッシュ
    dependencies: Map<string, string>
};
```

### semver.hml

セマンティックバージョニング2.0.0の完全な実装。

**責務:**
- バージョン文字列の解析
- バージョンの比較
- バージョン制約の解析と評価
- 制約を満たすバージョンの検索

**主要関数:**
```hemlock
// 解析
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// 比較
compare(a, b: Version): int           // -1、0、または1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// 制約
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // vがcに一致するかチェック
max_satisfying(versions, c): Version?      // 最高の一致を見つける
sort(versions): [Version]                  // 昇順ソート

// ユーティリティ
constraints_overlap(a, b: Constraint): bool  // 互換性をチェック
```

**バージョン構造:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // 例: ["beta", "1"]
    build: string?          // 例: "20230101"
};
```

**制約の種類:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0"、"<2.0.0"
    | And(Constraint, Constraint)  // 結合された範囲
    | Any;                     // "*"
```

### resolver.hml

npmスタイルの依存関係解決を実装。

**責務:**
- 依存関係ツリーの解決
- バージョン競合の検出
- 循環依存の検出
- 可視化ツリーの構築

**主要関数:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // メインリゾルバ: 解決されたバージョンを持つすべての依存関係のフラットマップを返す

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // すべての制約を満たすバージョンを見つける

detect_cycles(deps: Map): [Cycle]?
    // DFSを使用して循環依存を見つける

build_tree(lockfile): Tree
    // 表示用のツリー構造を作成

find_why(pkg, lockfile): [Chain]
    // パッケージがインストールされている理由を説明する依存関係チェーンを見つける
```

**解決アルゴリズム:**

1. **制約を収集**: マニフェストと推移的依存関係を走査
2. **各パッケージを解決**: 各パッケージについて:
   - 依存元からのすべてのバージョン制約を取得
   - GitHubから利用可能なバージョンを取得
   - すべての制約を満たす最高バージョンを見つける
   - 満たすバージョンがない場合: 競合
3. **循環を検出**: DFSを実行して循環依存を見つける
4. **フラットマップを返す**: パッケージ名 → 解決されたバージョン情報

**ResolveResult構造:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

パッケージ発見とダウンロード用のGitHub APIクライアント。

**責務:**
- 利用可能なバージョン（タグ）の取得
- リポジトリからのpackage.jsonのダウンロード
- リリースtarballのダウンロード
- 認証とレート制限の処理

**主要関数:**
```hemlock
get_token(): string?
    // 環境変数または設定からトークンを取得

github_request(url, headers?): Response
    // リトライ付きでAPIリクエストを実行

get_tags(owner, repo): [string]
    // バージョンタグを取得（v1.0.0、v1.1.0など）

get_package_json(owner, repo, ref): Manifest
    // 特定のタグ/コミットでpackage.jsonを取得

download_tarball(owner, repo, tag): bytes
    // リリースアーカイブをダウンロード

repo_exists(owner, repo): bool
    // リポジトリが存在するかチェック

get_repo_info(owner, repo): RepoInfo
    // リポジトリメタデータを取得
```

**リトライロジック:**
- 指数バックオフ: 1秒、2秒、4秒、8秒
- 以下でリトライ: 403（レート制限）、5xx（サーバーエラー）、ネットワークエラー
- 最大4回リトライ
- レート制限エラーを明確に報告

**使用するAPIエンドポイント:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

パッケージのダウンロードと展開を処理。

**責務:**
- GitHubからパッケージをダウンロード
- hem_modulesにtarballを展開
- キャッシュされたパッケージのチェック/使用
- パッケージのインストール/アンインストール

**主要関数:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // 単一パッケージをダウンロードしてインストール

install_all(packages: Map, options): InstallResult
    // 解決されたすべてのパッケージをインストール

uninstall_package(name: string): bool
    // hem_modulesからパッケージを削除

get_installed(): Map<string, string>
    // 現在インストールされているパッケージをリスト

verify_integrity(pkg): bool
    // パッケージの整合性を検証

prefetch_packages(packages: Map): void
    // キャッシュへの並列ダウンロード（実験的）
```

**インストールプロセス:**

1. 正しいバージョンで既にインストールされているかチェック
2. キャッシュにtarballがあるかチェック
3. キャッシュにない場合、GitHubからダウンロード
4. 将来の使用のためにキャッシュに保存
5. `hem_modules/owner/repo/`に展開
6. インストールを検証

**作成されるディレクトリ構造:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

グローバルパッケージキャッシュを管理。

**責務:**
- ダウンロードしたtarballの保存
- キャッシュされたパッケージの取得
- キャッシュされたパッケージのリスト
- キャッシュのクリア
- 設定の管理

**主要関数:**
```hemlock
get_cache_dir(): string
    // キャッシュディレクトリを取得（HPM_CACHE_DIRを尊重）

get_config_dir(): string
    // 設定ディレクトリを取得（~/.hpm）

is_cached(owner, repo, version): bool
    // tarballがキャッシュされているかチェック

get_cached_path(owner, repo, version): string
    // キャッシュされたtarballへのパスを取得

store_tarball_file(owner, repo, version, data): void
    // tarballをキャッシュに保存

list_cached(): [CachedPackage]
    // すべてのキャッシュされたパッケージをリスト

clear_cache(): int
    // すべてのキャッシュされたパッケージを削除、解放バイト数を返す

get_cache_size(): int
    // 合計キャッシュサイズを計算

read_config(): Config
    // ~/.hpm/config.jsonを読み込み

write_config(c: Config): void
    // 設定ファイルを書き込み
```

**キャッシュ構造:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## データフロー

### インストールコマンドフロー

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ 引数を解析、cmd_installを呼び出し
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ package.jsonを読み込み、依存関係を追加
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ すべての依存関係を解決
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ バージョンを取得、満たすものを見つける
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ パッケージをダウンロードして展開
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ ダウンロードまたはキャッシュを使用
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ package-lock.jsonを更新
    └──────────┘
```

### 解決アルゴリズムの詳細

```
入力: manifest.dependencies、manifest.devDependencies、既存のロックファイル

1. 初期化:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [直接依存関係]

2. キューが空でない間:
   a. pkg = queue.pop()
   b. pkgが既に解決済みならスキップ
   c. 依存元からpkgのすべての制約を取得
   d. GitHubから利用可能なバージョンを取得（キャッシュ）
   e. すべての制約を満たす最大バージョンを見つける
   f. 見つからない場合: 競合
   g. resolved[pkg] = {version, url, deps}
   h. pkgの依存関係をキューに追加

3. 解決されたグラフで循環を検出
   - 循環が見つかった場合: エラー

4. 解決されたマップを返す
```

## エラー処理

### 終了コード

main.hmlで定義:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### エラー伝播

エラーは戻り値を通じてバブルアップ:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ?が伝播
    // ...
}
```

## テスト

### テストフレームワーク

`test/framework.hml`のカスタムテストフレームワーク:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### テストファイル

- `test/test_semver.hml` - バージョン解析、比較、制約
- `test/test_manifest.hml` - マニフェストの読み書き、検証
- `test/test_lockfile.hml` - ロックファイル操作
- `test/test_cache.hml` - キャッシュ管理

### テストの実行

```bash
# すべてのテスト
make test

# 特定のテスト
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## 将来の改善

### 計画された機能

1. **整合性検証** - 完全なSHA256ハッシュチェック
2. **ワークスペース** - モノレポサポート
3. **プラグインシステム** - 拡張可能なコマンド
4. **監査** - セキュリティ脆弱性チェック
5. **プライベートレジストリ** - セルフホストパッケージホスティング

### 既知の制限

1. **バンドラーバグ** - スタンドアロン実行可能ファイルを作成できない
2. **並列ダウンロード** - 実験的、競合状態の可能性あり
3. **整合性** - SHA256が完全に実装されていない

## 貢献

### コードスタイル

- 4スペースインデント
- 関数は1つのことを行うべき
- 複雑なロジックにコメント
- 新機能にはテストを書く

### コマンドの追加

1. `main.hml`にハンドラを追加:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // 実装
   }
   ```

2. コマンドディスパッチに追加:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. ヘルプテキストを更新

### モジュールの追加

1. `src/newmodule.hml`を作成
2. パブリックインターフェースをエクスポート
3. 必要なモジュールでインポート
4. `test/test_newmodule.hml`にテストを追加

## 参照

- [コマンド](commands.md) - CLIリファレンス
- [パッケージの作成](creating-packages.md) - パッケージ開発
- [バージョニング](versioning.md) - セマンティックバージョニング
