# Hemlockにおけるメモリ所有権

> 「安全であるためのツールを提供しますが、使用を強制しません。」

このドキュメントでは、Hemlockのメモリ所有権セマンティクスについて説明し、プログラマ管理メモリとランタイム管理値の両方をカバーします。

## 目次

1. [契約](#契約)
2. [プログラマ管理メモリ](#プログラマ管理メモリ)
3. [ランタイム管理値](#ランタイム管理値)
4. [所有権移転ポイント](#所有権移転ポイント)
5. [非同期と並行性](#非同期と並行性)
6. [FFIメモリルール](#ffiメモリルール)
7. [例外安全性](#例外安全性)
8. [ベストプラクティス](#ベストプラクティス)

---

## 契約

Hemlockはメモリ管理責任を明確に分離しています：

| メモリタイプ | 管理者 | クリーンアップ方法 |
|-------------|--------|-------------------|
| 生ポインタ (`ptr`) | **プログラマ** | `free(ptr)` |
| バッファ (`buffer`) | **プログラマ** | `free(buf)` |
| 文字列、配列、オブジェクト | **ランタイム** | 自動（参照カウント） |
| 関数、クロージャ | **ランタイム** | 自動（参照カウント） |
| タスク、チャネル | **ランタイム** | 自動（参照カウント） |

**核心原則：** 明示的に割り当てたものは、明示的に解放します。それ以外は自動的に処理されます。

---

## プログラマ管理メモリ

### 生ポインタ

```hemlock
let p = alloc(64);       // 64バイトを割り当て
memset(p, 0, 64);        // 初期化
// ... メモリを使用 ...
free(p);                 // あなたの責任！
```

**ルール：**
- `alloc()` はあなたが所有するメモリを返す
- 使い終わったら `free()` を呼ぶ必要がある
- 二重解放はクラッシュする（意図的）
- 解放後使用は未定義動作
- ポインタ演算は許可されるが未チェック

### 型付き割り当て

```hemlock
let arr = talloc("i32", 100);  // 100個のi32を割り当て（400バイト）
ptr_write_i32(arr, 0, 42);     // インデックス0に書き込み
let val = ptr_read_i32(arr, 0); // インデックス0から読み取り
free(arr);                      // まだあなたの責任
```

### バッファ（安全な代替）

```hemlock
let buf = buffer(64);    // 境界チェック付きバッファ
buf[0] = 42;             // 安全なインデックスアクセス
// buf[100] = 1;         // ランタイムエラー：範囲外
free(buf);               // 明示的なfreeが必要
```

**主な違い：** バッファは境界チェックを提供、生ポインタは提供しない。

---

## ランタイム管理値

### 参照カウント

ヒープ割り当て値はアトミック参照カウントを使用：

```hemlock
let s1 = "hello";        // 文字列割り当て、refcount = 1
let s2 = s1;             // s2はs1を共有、refcount = 2
// 両方がスコープ外に出ると、refcount → 0、メモリ解放
```

**参照カウントされる型：**
- `string` - UTF-8テキスト
- `array` - 動的配列
- `object` - キー・バリューオブジェクト
- `function` - クロージャ
- `task` - 非同期タスクハンドル
- `channel` - 通信チャネル

### 循環検出

ランタイムはオブジェクトグラフの循環を処理：

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // 循環: a → b → a
// ランタイムは訪問済みセットを使用してクリーンアップ中に循環を検出・破壊
```

---

## 所有権移転ポイント

### 変数バインディング

```hemlock
let x = [1, 2, 3];       // 配列作成、refcount 1
                         // xが参照を所有
```

### 関数戻り値

```hemlock
fn make_array() {
    return [1, 2, 3];    // 配列の所有権が呼び出し元に移転
}
let arr = make_array();  // arrが参照を所有
```

### 代入

```hemlock
let a = "hello";
let b = a;               // 共有参照（refcountインクリメント）
b = "world";             // aはまだ"hello"、bは"world"
```

### チャネル操作

```hemlock
let ch = channel(10);
ch.send("message");      // 値がチャネルバッファにコピー
                         // オリジナルは有効なまま

let msg = ch.recv();     // チャネルから所有権を受け取る
```

### タスクスポーン

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // dataは分離のためディープコピー
data.x = 2;                       // 安全 - タスクは自分のコピーを持つ
let result = join(task);          // resultの所有権が呼び出し元に移転
```

---

## 非同期と並行性

### スレッド分離

スポーンされたタスクはミュータブル引数の**ディープコピー**を受け取る：

```hemlock
async fn worker(data) {
    data.x = 100;        // タスクのコピーのみを変更
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // 安全 - タスクに影響しない
let result = join(task);
print(obj.x);            // 2（タスクによって変更されていない）
print(result.x);         // 100（タスクの変更されたコピー）
```

### 共有コーディネーションオブジェクト

一部の型は参照で共有される（コピーされない）：
- **チャネル** - タスク間通信用
- **タスク** - コーディネーション用（join/detach）

```hemlock
let ch = channel(1);
spawn(producer, ch);     // 同じチャネル、コピーではない
spawn(consumer, ch);     // 両方のタスクがチャネルを共有
```

### タスク結果

```hemlock
let task = spawn(compute);
let result = join(task);  // 呼び出し元が結果を所有
                          // タスクの参照はタスク解放時に解放
```

### デタッチされたタスク

```hemlock
detach(spawn(background_work));
// タスクは独立して実行
// 結果はタスク完了時に自動解放
// join()を呼ばなくてもリークなし
```

---

## FFIメモリルール

### C関数への受け渡し

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlockが所有権を保持
                         // 文字列は呼び出し中有効
                         // C関数は解放してはいけない
```

### C関数からの受け取り

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // Cがこのメモリを割り当てた
free(copy);                   // 解放はあなたの責任
```

### 構造体の受け渡し（コンパイラのみ）

```hemlock
// C構造体レイアウトを定義
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // 値で返され、コピーされる
                                // スタック構造体のクリーンアップ不要
```

### コールバックメモリ

```hemlock
// CがHemlockにコールバックする時：
// - 引数はCが所有（解放しない）
// - 戻り値の所有権はCに移転
```

---

## 例外安全性

### 保証

ランタイムは以下を保証：

1. **正常終了時リークなし** - すべてのランタイム管理値がクリーンアップ
2. **例外時リークなし** - スタックアンワインド中に一時値が解放
3. **例外時もdefer実行** - クリーンアップコードが実行

### 式評価

```hemlock
// 配列作成中にスローした場合：
let arr = [f(), g(), h()];  // 部分的な配列は解放

// 関数呼び出し中にスローした場合：
foo(a(), b(), c());         // 以前に評価された引数は解放
```

### クリーンアップ用Defer

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // returnまたは例外時に実行

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close()は実行される！
    }
    return data;
}
```

---

## ベストプラクティス

### 1. ランタイム管理型を優先

```hemlock
// これを優先：
let data = [1, 2, 3, 4, 5];

// これより（低レベル制御が必要でない限り）：
let data = talloc("i32", 5);
// ... 解放を忘れずに ...
```

### 2. 手動メモリにはDeferを使用

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // 確実なクリーンアップ

    // ... bufを使用 ...
    // 各returnポイントでfreeする必要なし
}
```

### 3. 非同期で生ポインタを避ける

```hemlock
// 間違い - タスク完了前にポインタが解放される可能性
let p = alloc(64);
spawn(worker, p);          // タスクはポインタ値を取得
free(p);                   // おっと！タスクがまだ使用中

// 正しい - チャネルを使うかデータをコピー
let ch = channel(1);
let data = buffer(64);
// ... dataを埋める ...
ch.send(data);             // ディープコピー
spawn(worker, ch);
free(data);                // 安全 - タスクは自分のコピーを持つ
```

### 4. 完了時にチャネルを閉じる

```hemlock
let ch = channel(10);
// ... チャネルを使用 ...
ch.close();                // バッファされた値をドレインして解放
```

### 5. タスクはJoinかDetach

```hemlock
let task = spawn(work);

// オプション1: 結果を待つ
let result = join(task);

// オプション2: Fire and forget
// detach(task);

// してはいけない: joinかdetachせずにタスクハンドルをスコープ外に
// （クリーンアップされるが、結果がリークする可能性）
```

---

## メモリ問題のデバッグ

### ASANを有効化

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### リーク回帰テストを実行

```bash
make leak-regression       # フルスイート
make leak-regression-quick # 包括的テストをスキップ
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## まとめ

| 操作 | メモリ動作 |
|------|-----------|
| `alloc(n)` | 割り当て、あなたが解放 |
| `buffer(n)` | 境界チェック付き割り当て、あなたが解放 |
| `"string"` | ランタイムが管理 |
| `[array]` | ランタイムが管理 |
| `{object}` | ランタイムが管理 |
| `spawn(fn)` | 引数をディープコピー、ランタイムがタスクを管理 |
| `join(task)` | 呼び出し元が結果を所有 |
| `detach(task)` | 完了時にランタイムが結果を解放 |
| `ch.send(v)` | チャネルに値をコピー |
| `ch.recv()` | 呼び出し元が受信値を所有 |
| `ch.close()` | バッファされた値をドレインして解放 |
