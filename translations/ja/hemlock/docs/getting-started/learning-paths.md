# 学習パス

目標によって必要な知識は異なります。作りたいものに合ったパスを選んでください。

---

## パス1：クイックスクリプトと自動化

**目標：** タスクを自動化し、ファイルを処理し、仕事を片付けるスクリプトを書く。

**生産性までの時間：** 速い - すぐに便利なスクリプトを書き始められます。

### 学ぶこと

1. **[クイックスタート](quick-start.md)** - 最初のプログラム、基本構文
2. **[文字列](../language-guide/strings.md)** - テキスト処理、分割、検索
3. **[配列](../language-guide/arrays.md)** - リスト、フィルタリング、データ変換
4. **[ファイルI/O](../advanced/file-io.md)** - ファイルの読み書き
5. **[コマンドライン引数](../advanced/command-line-args.md)** - ユーザーからの入力を取得

### 今はスキップ

- メモリ管理（スクリプトでは自動）
- 非同期/並行処理（シンプルなスクリプトには過剰）
- FFI（Cインターオペが必要な場合のみ）

### サンプルプロジェクト：ファイルリネーマー

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// すべての.txtファイルを.mdにリネーム
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Renamed: ${file} -> ${new_name}`);
    }
}
```

---

## パス2：データ処理と分析

**目標：** データをパースし、変換し、レポートを生成する。

**生産性までの時間：** 速い - Hemlockの文字列と配列メソッドがこれを簡単にします。

### 学ぶこと

1. **[クイックスタート](quick-start.md)** - 基本
2. **[文字列](../language-guide/strings.md)** - パース、分割、フォーマット
3. **[配列](../language-guide/arrays.md)** - データ変換用のmap、filter、reduce
4. **[オブジェクト](../language-guide/objects.md)** - 構造化データ
5. **標準ライブラリ：**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSONパース
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - CSVファイル
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - ファイル操作

### サンプルプロジェクト：CSVアナライザー

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// 合計売上を計算
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Total sales: $${total}`);

// トップセラーを見つける
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Top sale: ${top.product} - $${top.amount}`);
```

---

## パス3：WebとネットワークプログラミングPath 3: Web & Network Programming

**目標：** HTTPクライアントを構築し、APIを操作し、サーバーを作成する。

**生産性までの時間：** 中程度 - 非同期の基本の理解が必要。

### 学ぶこと

1. **[クイックスタート](quick-start.md)** - 基本
2. **[関数](../language-guide/functions.md)** - コールバックとクロージャ
3. **[エラーハンドリング](../language-guide/error-handling.md)** - ネットワークエラー用のtry/catch
4. **[非同期と並行処理](../advanced/async-concurrency.md)** - spawn、await、channels
5. **標準ライブラリ：**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - HTTPリクエスト
   - **[@stdlib/json](../../stdlib/docs/json.md)** - API用JSON
   - **[@stdlib/net](../../stdlib/docs/net.md)** - TCP/UDPソケット
   - **[@stdlib/url](../../stdlib/docs/url.md)** - URLパース

### サンプルプロジェクト：APIクライアント

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// GETリクエスト
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}: ${user.email}`);
}

// POSTリクエスト
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`Created user with ID: ${parse(result.body).id}`);
```

---

## パス4：システムプログラミング

**目標：** 低レベルコードを書き、メモリを操作し、Cライブラリとインターフェースする。

**生産性までの時間：** 長め - メモリ管理の理解が必要。

### 学ぶこと

1. **[クイックスタート](quick-start.md)** - 基本
2. **[型](../language-guide/types.md)** - i32、u8、ptrなどの理解
3. **[メモリ管理](../language-guide/memory.md)** - alloc、free、バッファ
4. **[FFI](../advanced/ffi.md)** - C関数の呼び出し
5. **[シグナル](../advanced/signals.md)** - シグナルハンドリング

### 主要概念

**メモリ安全性チェックリスト：**
- [ ] すべての`alloc()`に対応する`free()`がある
- [ ] 生の`ptr`が必要でなければ`buffer()`を使用
- [ ] 解放後はポインタを`null`に設定
- [ ] クリーンアップを保証するために`try/finally`を使用

**FFI用の型マッピング：**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long`（64ビット） |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### サンプルプロジェクト：カスタムメモリプール

```hemlock
// シンプルなバンプアロケータ
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool exhausted";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// 使用例
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // すべてのメモリを再利用
pool_destroy();  // クリーンアップ
```

---

## パス5：並列・並行プログラム

**目標：** 複数のCPUコアでコードを実行し、レスポンシブなアプリケーションを構築する。

**生産性までの時間：** 中程度 - async構文は簡単ですが、並列処理の推論には練習が必要。

### 学ぶこと

1. **[クイックスタート](quick-start.md)** - 基本
2. **[関数](../language-guide/functions.md)** - クロージャ（非同期で重要）
3. **[非同期と並行処理](../advanced/async-concurrency.md)** - 完全な詳細解説
4. **[アトミック](../advanced/atomics.md)** - ロックフリープログラミング

### 主要概念

**Hemlockの非同期モデル：**
- `async fn` - 別のスレッドで実行できる関数を定義
- `spawn(fn, args...)` - 実行を開始、タスクハンドルを返す
- `join(task)`または`await task` - 完了を待ち、結果を取得
- `channel(size)` - タスク間でデータを送信するためのキューを作成

**重要：** タスクは値の*コピー*を受け取ります。ポインタを渡す場合、タスクが完了するまでメモリが有効であることを保証する責任があります。

### サンプルプロジェクト：並列ファイルプロセッサ

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// すべてのファイルを並列処理
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// 結果を収集
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}: ${count} lines`);
    total_lines = total_lines + count;
}

print(`Total: ${total_lines} lines`);
```

---

## 最初に学ぶこと（どのパスでも）

目標に関係なく、これらの基本から始めましょう：

### 第1週：コア基本

1. **[クイックスタート](quick-start.md)** - 最初のプログラムを書いて実行
2. **[構文](../language-guide/syntax.md)** - 変数、演算子、制御フロー
3. **[関数](../language-guide/functions.md)** - 関数の定義と呼び出し

### 第2週：データハンドリング

4. **[文字列](../language-guide/strings.md)** - テキスト操作
5. **[配列](../language-guide/arrays.md)** - コレクションとイテレーション
6. **[オブジェクト](../language-guide/objects.md)** - 構造化データ

### 第3週：堅牢性

7. **[エラーハンドリング](../language-guide/error-handling.md)** - try/catch/throw
8. **[モジュール](../language-guide/modules.md)** - import/export、stdlibの使用

### その後：上記からパスを選択

---

## チートシート：他の言語からの移行

### Pythonから

| Python | Hemlock | 備考 |
|--------|---------|-------|
| `x = 42` | `let x = 42;` | セミコロン必須 |
| `def fn():` | `fn name() { }` | ブレース必須 |
| `if x:` | `if (x) { }` | 括弧とブレース必須 |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | Cスタイルforループ |
| `for item in list:` | `for (item in array) { }` | for-inは同じ動作 |
| `list.append(x)` | `array.push(x);` | 異なるメソッド名 |
| `len(s)` | `s.length`または`len(s)` | 両方とも動作 |
| 自動メモリ | `ptr`は手動 | ほとんどの型は自動クリーンアップ |

### JavaScriptから

| JavaScript | Hemlock | 備考 |
|------------|---------|-------|
| `let x = 42` | `let x = 42;` | 同じ（セミコロン必須） |
| `const x = 42` | `let x = 42;` | constキーワードなし |
| `function fn()` | `fn name() { }` | 異なるキーワード |
| `() => x` | `fn() { return x; }` | アロー関数なし |
| `async/await` | `async/await` | 同じ構文 |
| `Promise` | `spawn/join` | 異なるモデル |
| 自動GC | `ptr`は手動 | ほとんどの型は自動クリーンアップ |

### C/C++から

| C | Hemlock | 備考 |
|---|---------|-------|
| `int x = 42;` | `let x: i32 = 42;` | 型はコロンの後 |
| `malloc(n)` | `alloc(n)` | 同じ概念 |
| `free(p)` | `free(p)` | 同じ |
| `char* s = "hi"` | `let s = "hi";` | 文字列は管理される |
| `#include` | `import { } from` | モジュールインポート |
| すべて手動 | ほとんどの型は自動 | `ptr`のみ手動が必要 |

---

## ヘルプを得る

- **[用語集](../glossary.md)** - プログラミング用語の定義
- **[サンプル](../../examples/)** - 完全な動作プログラム
- **[テスト](../../tests/)** - 機能の使い方を見る
- **GitHubのIssue** - 質問やバグ報告

---

## 難易度レベル

ドキュメント全体で以下のマーカーが表示されます：

| マーカー | 意味 |
|--------|---------|
| **初級** | プログラミング経験不要 |
| **中級** | 基本的なプログラミング知識を前提 |
| **上級** | システム概念の理解が必要 |

「初級」とマークされたものが分かりにくい場合は、[用語集](../glossary.md)で用語の定義を確認してください。
