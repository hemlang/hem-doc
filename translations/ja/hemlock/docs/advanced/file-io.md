# HemlockでのファイルI/O

Hemlockは、適切なエラー処理とリソース管理を備えたファイル操作のための**Fileオブジェクト API**を提供します。

## 目次

- [概要](#概要)
- [ファイルを開く](#ファイルを開く)
- [ファイルメソッド](#ファイルメソッド)
- [ファイルプロパティ](#ファイルプロパティ)
- [エラー処理](#エラー処理)
- [リソース管理](#リソース管理)
- [完全なAPIリファレンス](#完全なapiリファレンス)
- [一般的なパターン](#一般的なパターン)
- [ベストプラクティス](#ベストプラクティス)

## 概要

FileオブジェクトAPIは以下を提供します：

- **明示的なリソース管理** - ファイルは手動で閉じる必要がある
- **複数のオープンモード** - 読み取り、書き込み、追記、読み書き
- **テキストとバイナリ操作** - テキストとバイナリデータの両方を読み書き
- **シーク対応** - ファイル内でのランダムアクセス
- **包括的なエラーメッセージ** - コンテキスト対応のエラー報告

**重要：**ファイルは自動的に閉じられません。ファイルディスクリプタのリークを避けるために`f.close()`を呼び出す必要があります。

## ファイルを開く

ファイルを開くには`open(path, mode?)`を使用します：

```hemlock
let f = open("data.txt", "r");     // 読み取りモード（デフォルト）
let f2 = open("output.txt", "w");  // 書き込みモード（切り詰め）
let f3 = open("log.txt", "a");     // 追記モード
let f4 = open("data.bin", "r+");   // 読み書きモード
```

### オープンモード

| モード | 説明 | ファイルの存在が必要 | 切り詰め | 位置 |
|------|-------------|----------------|-----------|----------|
| `"r"` | 読み取り（デフォルト） | はい | いいえ | 先頭 |
| `"w"` | 書き込み | いいえ（作成） | はい | 先頭 |
| `"a"` | 追記 | いいえ（作成） | いいえ | 末尾 |
| `"r+"` | 読み書き | はい | いいえ | 先頭 |
| `"w+"` | 読み書き | いいえ（作成） | はい | 先頭 |
| `"a+"` | 読み取りと追記 | いいえ（作成） | いいえ | 末尾 |

### 例

**既存ファイルの読み取り：**
```hemlock
let f = open("config.json", "r");
// または単に：
let f = open("config.json");  // "r"がデフォルト
```

**書き込み用に新しいファイルを作成：**
```hemlock
let f = open("output.txt", "w");  // 作成または切り詰め
```

**ファイルへの追記：**
```hemlock
let f = open("log.txt", "a");  // 存在しない場合は作成
```

**読み書きモード：**
```hemlock
let f = open("data.bin", "r+");  // 既存ファイル、読み書き可能
```

## ファイルメソッド

### 読み取り

#### read(size?: i32): string

ファイルからテキストを読み取り（オプションのサイズパラメータ）。

**サイズなし（すべて読み取り）：**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // 現在位置からEOFまで読み取り
f.close();
```

**サイズ指定（特定バイト数を読み取り）：**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // 最大1024バイト読み取り
let next = f.read(1024);   // 次の1024バイトを読み取り
f.close();
```

**戻り値：**読み取ったデータを含む文字列、またはEOFの場合は空文字列

**例 - ファイル全体の読み取り：**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**例 - チャンクでの読み取り：**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // 4KBチャンク
    if (chunk == "") { break; }  // EOFに到達
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

バイナリデータを読み取り（バッファを返す）。

**パラメータ：**
- `size`（i32）- 読み取るバイト数

**戻り値：**読み取ったバイトを含むバッファ

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // 256バイト読み取り
print(binary.length);  // 256（またはEOFの場合はそれ以下）

// 個々のバイトにアクセス
let first_byte = binary[0];
print(first_byte);

f.close();
```

**例 - バイナリファイル全体の読み取り：**
```hemlock
let f = open("data.bin", "r");
let size = 10240;  // 予想サイズ
let data = f.read_bytes(size);
f.close();

// バイナリデータを処理
let i = 0;
while (i < data.length) {
    let byte = data[i];
    // ...バイトを処理
    i = i + 1;
}
```

### 書き込み

#### write(data: string): i32

ファイルにテキストを書き込み（書き込んだバイト数を返す）。

**パラメータ：**
- `data`（string）- 書き込むテキスト

**戻り値：**書き込んだバイト数（i32）

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Wrote " + typeof(written) + " bytes");  // "Wrote 14 bytes"
f.close();
```

**例 - 複数行の書き込み：**
```hemlock
let f = open("output.txt", "w");
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");
f.close();
```

**例 - ログファイルへの追記：**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Application started\n");
f.write("[INFO] User logged in\n");
f.close();
```

#### write_bytes(data: buffer): i32

バイナリデータを書き込み（書き込んだバイト数を返す）。

**パラメータ：**
- `data`（buffer）- 書き込むバイナリデータ

**戻り値：**書き込んだバイト数（i32）

```hemlock
let f = open("output.bin", "w");

// バイナリデータを作成
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Wrote " + typeof(bytes) + " bytes");

f.close();
```

**例 - バイナリファイルのコピー：**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let data = src.read_bytes(1024);
while (data.length > 0) {
    dst.write_bytes(data);
    data = src.read_bytes(1024);
}

src.close();
dst.close();
```

### シーク

#### seek(position: i32): i32

特定の位置に移動（新しい位置を返す）。

**パラメータ：**
- `position`（i32）- ファイル先頭からのバイトオフセット

**戻り値：**新しい位置（i32）

```hemlock
let f = open("data.txt", "r");

// バイト100に移動
f.seek(100);

// 位置100から読み取り
let data = f.read(50);

// 先頭にリセット
f.seek(0);

f.close();
```

**例 - ランダムアクセス：**
```hemlock
let f = open("records.dat", "r");

// オフセット1000のレコードを読み取り
f.seek(1000);
let record1 = f.read_bytes(100);

// オフセット2000のレコードを読み取り
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

ファイル内の現在位置を取得。

**戻り値：**現在のバイトオフセット（i32）

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0（先頭）

f.read(100);
let pos2 = f.tell();  // 100（100バイト読み取り後）

f.seek(500);
let pos3 = f.tell();  // 500（シーク後）

f.close();
```

**例 - 読み取り量の測定：**
```hemlock
let f = open("data.txt", "r");

let start = f.tell();
let content = f.read();
let end = f.tell();

let bytes_read = end - start;
print("Read " + typeof(bytes_read) + " bytes");

f.close();
```

### クローズ

#### close()

ファイルを閉じる（冪等、複数回呼び出し可能）。

```hemlock
let f = open("data.txt", "r");
// ...ファイルを使用
f.close();
f.close();  // 安全 - 2回目のクローズでエラーなし
```

**重要な注意事項：**
- ファイルディスクリプタのリークを避けるため、常に完了時にファイルを閉じる
- クローズは冪等 - 複数回安全に呼び出し可能
- クローズ後、他のすべての操作はエラーになる
- エラー時でもファイルが閉じられるように`finally`ブロックを使用

## ファイルプロパティ

Fileオブジェクトには3つの読み取り専用プロパティがあります：

### path: string

ファイルを開くために使用されたファイルパス。

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

ファイルが開かれたモード。

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

ファイルが閉じられているかどうか。

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**例 - ファイルが開いているか確認：**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ...コンテンツを処理
}

f.close();

if (f.closed) {
    print("File is now closed");
}
```

## エラー処理

すべてのファイル操作にはコンテキスト付きの適切なエラーメッセージが含まれます。

### 一般的なエラー

**ファイルが見つからない：**
```hemlock
let f = open("missing.txt", "r");
// エラー: Failed to open 'missing.txt': No such file or directory
```

**閉じたファイルからの読み取り：**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// エラー: Cannot read from closed file 'data.txt'
```

**読み取り専用ファイルへの書き込み：**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// エラー: Cannot write to file 'readonly.txt' opened in read-only mode
```

**書き込み専用ファイルからの読み取り：**
```hemlock
let f = open("output.txt", "w");
f.read();
// エラー: Cannot read from file 'output.txt' opened in write-only mode
```

### try/catchの使用

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Error reading file: " + e);
}
```

## リソース管理

### 基本パターン

常にファイルを明示的に閉じる：

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### エラー処理付き（推奨）

エラー時でもファイルが閉じられるように`finally`を使用：

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // エラーでも常に閉じる
}
```

### 複数ファイル

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### ヘルパー関数パターン

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// 使用方法：
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## 完全なAPIリファレンス

### 関数

| 関数 | パラメータ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `open(path, mode?)` | path: string, mode?: string | File | ファイルを開く（モードのデフォルトは"r"） |

### メソッド

| メソッド | パラメータ | 戻り値 | 説明 |
|--------|-----------|---------|-------------|
| `read(size?)` | size?: i32 | string | テキストを読み取り（すべてまたは特定バイト） |
| `read_bytes(size)` | size: i32 | buffer | バイナリデータを読み取り |
| `write(data)` | data: string | i32 | テキストを書き込み、書き込んだバイト数を返す |
| `write_bytes(data)` | data: buffer | i32 | バイナリデータを書き込み、書き込んだバイト数を返す |
| `seek(position)` | position: i32 | i32 | 位置にシーク、新しい位置を返す |
| `tell()` | - | i32 | 現在位置を取得 |
| `close()` | - | null | ファイルを閉じる（冪等） |

### プロパティ（読み取り専用）

| プロパティ | 型 | 説明 |
|----------|------|-------------|
| `path` | string | ファイルパス |
| `mode` | string | オープンモード |
| `closed` | bool | ファイルが閉じられているかどうか |

## 一般的なパターン

### ファイル全体の読み取り

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### ファイル全体の書き込み

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### ファイルへの追記

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Event occurred\n");
```

### 行の読み取り

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### 大きなファイルのチャンク処理

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // 4KBチャンク
            if (chunk == "") { break; }

            // チャンクを処理
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### バイナリファイルコピー

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### ファイルの切り詰め

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // "w"モードは切り詰め
    f.close();
}

truncate_file("empty_me.txt");
```

### ランダムアクセス読み取り

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

### ファイルサイズ

```hemlock
fn file_size(path: string): i32 {
    let f = open(path, "r");
    try {
        // 末尾にシーク
        let end = f.seek(999999999);  // 大きな数
        f.seek(0);  // リセット
        return end;
    } finally {
        f.close();
    }
}

let size = file_size("data.txt");
print("File size: " + typeof(size) + " bytes");
```

### 条件付き読み書き

```hemlock
fn update_file(path: string, condition, new_content: string) {
    let f = open(path, "r+");
    try {
        let content = f.read();

        if (condition(content)) {
            f.seek(0);  // 先頭にリセット
            f.write(new_content);
        }
    } finally {
        f.close();
    }
}
```

## ベストプラクティス

### 1. 常にtry/finallyを使用

```hemlock
// 良い例
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// 悪い例 - エラー時にファイルが閉じられない可能性
let f = open("data.txt", "r");
let content = f.read();
process(content);  // これがスローするとファイルがリーク
f.close();
```

### 2. 操作前にファイル状態を確認

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ...コンテンツを使用
}

f.close();
```

### 3. 適切なモードを使用

```hemlock
// 読み取りのみ？"r"を使用
let f = open("config.json", "r");

// 完全に置換？"w"を使用
let f = open("output.txt", "w");

// 末尾に追加？"a"を使用
let f = open("log.txt", "a");
```

### 4. エラーを優雅に処理

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Warning: Could not read " + path + ": " + e);
        return "";
    }
}
```

### 5. 開いた逆順でファイルを閉じる

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ...ファイルを使用
} finally {
    // 逆順で閉じる
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. 大きなファイルは全体を読み取らない

```hemlock
// 大きなファイルには悪い例
let f = open("huge.log", "r");
let content = f.read();  // ファイル全体をメモリにロード
f.close();

// 良い例 - チャンクで処理
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## まとめ

HemlockのファイルI/O APIは以下を提供します：

- シンプルで明示的なファイル操作
- テキストとバイナリのサポート
- seek/tellによるランダムアクセス
- コンテキスト付きの明確なエラーメッセージ
- 冪等なクローズ操作

覚えておくべきこと：
- 常にファイルを手動で閉じる
- リソース安全のためにtry/finallyを使用
- 適切なオープンモードを選択
- エラーを優雅に処理
- 大きなファイルはチャンクで処理
