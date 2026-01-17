# ファイルAPIリファレンス

HemlockのファイルI/Oシステムの完全なリファレンスです。

---

## 概要

Hemlockは適切なエラーハンドリングとリソース管理を備えた**ファイルオブジェクトAPI**をファイル操作に提供します。ファイルは手動でオープンおよびクローズする必要があります。

**主な機能：**
- メソッド付きファイルオブジェクト
- テキストとバイナリデータの読み書き
- シークと位置決め
- 適切なエラーメッセージ
- 手動リソース管理（RAIIなし）

---

## ファイル型

**型：** `file`

**説明：** I/O操作用のファイルハンドル

**プロパティ（読み取り専用）：**
- `.path` - ファイルパス（string）
- `.mode` - オープンモード（string）
- `.closed` - ファイルがクローズされているか（bool）

---

## ファイルのオープン

### open

読み取り、書き込み、または両方のためにファイルをオープンします。

**シグネチャ：**
```hemlock
open(path: string, mode?: string): file
```

**パラメータ：**
- `path` - ファイルパス（相対または絶対）
- `mode`（オプション）- オープンモード（デフォルト：`"r"`）

**戻り値：** ファイルオブジェクト

**モード：**
- `"r"` - 読み取り（デフォルト）
- `"w"` - 書き込み（既存ファイルを切り詰め）
- `"a"` - 追加
- `"r+"` - 読み取りと書き込み
- `"w+"` - 読み取りと書き込み（切り詰め）
- `"a+"` - 読み取りと追加

**例：**
```hemlock
// 読み取りモード（デフォルト）
let f = open("data.txt");
let f_read = open("data.txt", "r");

// 書き込みモード（切り詰め）
let f_write = open("output.txt", "w");

// 追加モード
let f_append = open("log.txt", "a");

// 読み取り/書き込みモード
let f_rw = open("data.bin", "r+");

// 読み取り/書き込み（切り詰め）
let f_rw_trunc = open("output.bin", "w+");

// 読み取り/追加
let f_ra = open("log.txt", "a+");
```

**エラーハンドリング：**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Failed to open:", e);
    // Error: Failed to open 'missing.txt': No such file or directory
}
```

**重要：** ファイルディスクリプタのリークを避けるため、`f.close()`で手動でクローズする必要があります。

---

## ファイルメソッド

### 読み取り

#### read

ファイルからテキストを読み取ります。

**シグネチャ：**
```hemlock
file.read(size?: i32): string
```

**パラメータ：**
- `size`（オプション）- 読み取るバイト数（省略時はEOFまで読み取り）

**戻り値：** ファイル内容の文字列

**例：**
```hemlock
let f = open("data.txt", "r");

// ファイル全体を読み取り
let all = f.read();
print(all);

// 特定のバイト数を読み取り
let chunk = f.read(1024);

f.close();
```

**動作：**
- 現在のファイル位置から読み取り
- EOFでは空文字列を返す
- ファイル位置を進める

**エラー：**
- クローズされたファイルからの読み取り
- 書き込み専用ファイルからの読み取り

---

#### read_bytes

ファイルからバイナリデータを読み取ります。

**シグネチャ：**
```hemlock
file.read_bytes(size: i32): buffer
```

**パラメータ：**
- `size` - 読み取るバイト数

**戻り値：** バイナリデータを含むバッファ

**例：**
```hemlock
let f = open("data.bin", "r");

// 256バイトを読み取り
let binary = f.read_bytes(256);
print(binary.length);       // 256

// バイナリデータを処理
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**動作：**
- 正確なバイト数を読み取り
- バッファを返す（文字列ではない）
- ファイル位置を進める

---

### 書き込み

#### write

ファイルにテキストを書き込みます。

**シグネチャ：**
```hemlock
file.write(data: string): i32
```

**パラメータ：**
- `data` - 書き込む文字列

**戻り値：** 書き込まれたバイト数（i32）

**例：**
```hemlock
let f = open("output.txt", "w");

// テキストを書き込み
let written = f.write("Hello, World!\n");
print("Wrote", written, "bytes");

// 複数回書き込み
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");

f.close();
```

**動作：**
- 現在のファイル位置に書き込み
- 書き込まれたバイト数を返す
- ファイル位置を進める

**エラー：**
- クローズされたファイルへの書き込み
- 読み取り専用ファイルへの書き込み

---

#### write_bytes

ファイルにバイナリデータを書き込みます。

**シグネチャ：**
```hemlock
file.write_bytes(data: buffer): i32
```

**パラメータ：**
- `data` - 書き込むバッファ

**戻り値：** 書き込まれたバイト数（i32）

**例：**
```hemlock
let f = open("output.bin", "w");

// バッファを作成
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// バッファを書き込み
let written = f.write_bytes(buf);
print("Wrote", written, "bytes");

f.close();
```

**動作：**
- バッファの内容をファイルに書き込み
- 書き込まれたバイト数を返す
- ファイル位置を進める

---

### シーク

#### seek

ファイル位置を特定のバイトオフセットに移動します。

**シグネチャ：**
```hemlock
file.seek(position: i32): i32
```

**パラメータ：**
- `position` - ファイル先頭からのバイトオフセット

**戻り値：** 新しいファイル位置（i32）

**例：**
```hemlock
let f = open("data.txt", "r");

// バイト100にジャンプ
f.seek(100);

// その位置から読み取り
let chunk = f.read(50);

// 先頭にリセット
f.seek(0);

// 先頭から読み取り
let all = f.read();

f.close();
```

**動作：**
- ファイル位置を絶対オフセットに設定
- 新しい位置を返す
- EOF以降へのシークは許可される（書き込み時にファイルにホールを作成）

---

#### tell

現在のファイル位置を取得します。

**シグネチャ：**
```hemlock
file.tell(): i32
```

**戻り値：** ファイル先頭からの現在のバイトオフセット（i32）

**例：**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0（先頭）

f.read(100);
print(f.tell());        // 100（読み取り後）

f.seek(50);
print(f.tell());        // 50（シーク後）

f.close();
```

---

### クローズ

#### close

ファイルをクローズします（冪等）。

**シグネチャ：**
```hemlock
file.close(): null
```

**戻り値：** `null`

**例：**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// 複数回呼び出しても安全
f.close();  // エラーなし
f.close();  // エラーなし
```

**動作：**
- ファイルハンドルをクローズ
- 保留中の書き込みをフラッシュ
- 冪等（複数回呼び出しても安全）
- `.closed`プロパティを`true`に設定

**重要：** ファイルディスクリプタのリークを避けるため、完了したら常にファイルをクローズしてください。

---

## ファイルプロパティ

### .path

ファイルパスを取得します。

**型：** `string`

**アクセス：** 読み取り専用

**例：**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

オープンモードを取得します。

**型：** `string`

**アクセス：** 読み取り専用

**例：**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

ファイルがクローズされているかチェックします。

**型：** `bool`

**アクセス：** 読み取り専用

**例：**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## エラーハンドリング

すべてのファイル操作にはコンテキスト付きの適切なエラーメッセージが含まれます：

### ファイルが見つからない
```hemlock
let f = open("missing.txt", "r");
// Error: Failed to open 'missing.txt': No such file or directory
```

### クローズされたファイルからの読み取り
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Error: Cannot read from closed file 'data.txt'
```

### 読み取り専用ファイルへの書き込み
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Error: Cannot write to file 'readonly.txt' opened in read-only mode
```

### try/catchの使用
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("File error:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## リソース管理パターン

### 基本パターン

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### エラーハンドリング付き

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // エラー時も常にクローズ
}
```

### 安全なパターン

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... コンテンツを処理 ...
} catch (e) {
    print("Error:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## 使用例

### ファイル全体を読み取る

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### テキストファイルを書き込む

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### ファイルに追加する

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Log entry 1");
append_file("log.txt", "Log entry 2");
```

### バイナリファイルを読み取る

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Read", binary.length, "bytes");
```

### バイナリファイルを書き込む

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### ファイルを行ごとに読み取る

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line", i, ":", lines[i]);
    i = i + 1;
}
```

### ファイルをコピーする

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### ファイルをチャンクで読み取る

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // 一度に1KBを読み取り
        if (chunk.length == 0) {
            break;  // EOF
        }

        // チャンクを処理
        print("Processing", chunk.length, "bytes");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## 完全なメソッド要約

| メソッド | シグネチャ | 戻り値 | 説明 |
|---------------|--------------------------|-----------|------------------------------|
| `read`        | `(size?: i32)`           | `string`  | テキストを読み取り |
| `read_bytes`  | `(size: i32)`            | `buffer`  | バイナリデータを読み取り |
| `write`       | `(data: string)`         | `i32`     | テキストを書き込み |
| `write_bytes` | `(data: buffer)`         | `i32`     | バイナリデータを書き込み |
| `seek`        | `(position: i32)`        | `i32`     | ファイル位置を設定 |
| `tell`        | `()`                     | `i32`     | ファイル位置を取得 |
| `close`       | `()`                     | `null`    | ファイルをクローズ（冪等） |

---

## 完全なプロパティ要約

| プロパティ | 型 | アクセス | 説明 |
|-----------|----------|------------|--------------------------|
| `.path`   | `string` | 読み取り専用 | ファイルパス |
| `.mode`   | `string` | 読み取り専用 | オープンモード |
| `.closed` | `bool`   | 読み取り専用 | ファイルがクローズされているか |

---

## 旧APIからの移行

**旧API（削除済み）：**
- `read_file(path)` - `open(path, "r").read()`を使用
- `write_file(path, data)` - `open(path, "w").write(data)`を使用
- `append_file(path, data)` - `open(path, "a").write(data)`を使用
- `file_exists(path)` - 代替なし

**移行例：**
```hemlock
// 旧（v0.0）
let content = read_file("data.txt");
write_file("output.txt", content);

// 新（v0.1）
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## 関連項目

- [組み込み関数](builtins.md) - `open()`関数
- [メモリAPI](memory-api.md) - バッファ型
- [文字列API](string-api.md) - テキスト処理用の文字列メソッド
