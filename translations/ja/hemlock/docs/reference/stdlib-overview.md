# 標準ライブラリ概要

Hemlockにはシステムプログラミング、I/O、ネットワーキング、データフォーマット、並行処理などをカバーする53個の標準ライブラリモジュールが付属しています。すべてのモジュールは`@stdlib/`プレフィックスでインポートします。

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## モジュールカテゴリ

### コアユーティリティ

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | テストと検証のためのアサーションユーティリティ |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap、Queue、Stack、Set、LinkedList、LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | タスク検査とスタック管理 |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | printfスタイルの文字列フォーマット |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | イテレータユーティリティ（range、enumerate、zip、chain） |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | レベルとファイル出力を持つ構造化ロガー |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | 乱数生成とシャッフル |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | 拡張文字列ユーティリティ（pad、reverse、lines） |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | BDDスタイルテストフレームワーク（describe、test、expect） |

### 数学 & 科学

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin、cos、sqrt、pow、rand、PI、E、divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed、to_hex、parse_int、parse_float、StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | 密行列演算（multiply、transpose、determinant、inverse） |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | USearch ANNを使用したベクトル類似性検索 |

### メモリ & 低レベル

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | アリーナ（バンプ）メモリアロケータ |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | アトミック操作（load、store、add、CAS、fence） |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | バイトスワップ、エンディアン変換、バッファI/O |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | メモリマップドファイルI/O |

### ファイルシステム & I/O

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | ファイルとディレクトリ操作（open、read_file、write_file、list_dir） |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | スレッドプール経由のノンブロッキングファイルI/O |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | ファイルパターンマッチング |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | パス操作（join、dirname、basename、extname） |

### 並行処理 & 非同期

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool、parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | プロセス間通信（パイプ、メッセージキュー） |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | シグナル定数とハンドリング（SIGINT、SIGTERMなど） |

### ネットワーキング

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | HTTPクライアント（get、post、ヘッダー付きrequest） |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | TCP/UDPソケット（TcpListener、TcpStream、UdpSocket） |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Unixドメインソケット（AF_UNIXストリーム/データグラム） |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | URLパースと操作 |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | WebSocketクライアント |

### データフォーマット

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSONパース、stringify、pretty、パスアクセス |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | TOMLパースと生成 |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | YAMLパースと生成 |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | CSVパースと生成 |

### エンコーディング & 暗号

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64、Base32、hex、URLエンコーディング |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1、SHA-256、SHA-512、MD5、CRC32、DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | AES暗号化、RSA署名、random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip、gunzip、deflate |

### テキスト処理

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | 正規表現（POSIX ERE） |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Jinja2互換テンプレートレンダリング |

### 日付、時間 & バージョニング

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | DateTimeクラス、フォーマット、パース |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | タイムスタンプ、sleep、クロック計測 |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | セマンティックバージョンパースと比較 |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | UUID v4およびv7生成 |

### システム & 環境

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | コマンドライン引数パース |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | 環境変数、exit、get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | プラットフォーム検出、CPU数、ホスト名 |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork、exec、wait、kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | シェルコマンド実行と引数エスケープ |

### ターミナル & UI

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | ANSIカラー、スタイル、カーソル制御 |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | 生ターミナル入力とキー検出 |

### データベース

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | SQLiteデータベース、query、exec、トランザクション |

### FFI & 相互運用

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | FFIコールバック管理と型定数 |

### ユーティリティ

| モジュール | インポート | 説明 |
|--------|--------|-------------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | 指数バックオフ付きリトライロジック |

---

## クイック例

### 設定ファイルの読み取りとパース

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connecting to " + db_host);
```

### JSONを使用したHTTPリクエスト

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### 並行処理

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### ハッシュとエンコード

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### テンプレートレンダリング

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Home", "About", "Contact"] });
```

---

## 関連項目

- [組み込み関数リファレンス](./builtins.md) -- インポート不要で利用可能な関数
- [移行ガイド (v2.0)](../migration-2.0.md) -- v2.0でstdlibに移動した組み込み関数
- 個別モジュールドキュメントは[`stdlib/docs/`](../../stdlib/docs/)にあります
