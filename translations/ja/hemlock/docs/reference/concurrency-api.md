# 並行性APIリファレンス

Hemlockの非同期/並行性システムの完全なリファレンスです。

---

## 概要

Hemlockは、POSIXスレッド（pthreads）を使用した真のマルチスレッド並列処理を備えた**構造化された並行性**を提供します。各スポーンされたタスクは別のOSスレッドで実行され、複数のCPUコアにわたる実際の並列実行を可能にします。

**主な機能：**
- 真のマルチスレッド並列処理（グリーンスレッドではない）
- 非同期関数構文
- タスクのスポーンと結合
- スレッドセーフなチャネル
- 例外の伝播

**スレッディングモデル：**
- 実際のOSスレッド（POSIX pthreads）
- 真の並列処理（複数のCPUコア）
- カーネルスケジュール（プリエンプティブマルチタスキング）
- スレッドセーフな同期（ミューテックス、条件変数）

---

## 非同期関数

### 非同期関数の宣言

関数を`async`として宣言して、並行実行用に設計されていることを示すことができます。

**構文：**
```hemlock
async fn function_name(params): return_type {
    // 関数本体
}
```

**例：**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Processing:", data);
    return null;
}
```

**動作：**
- `async fn`は非同期関数を宣言
- 同期的に呼び出し可能（現在のスレッドで実行）
- 並行タスクとしてスポーン可能（新しいスレッドで実行）
- スポーン時は独自のOSスレッドで実行

**注意：** `await`キーワードは将来の使用のために予約されていますが、現在は実装されていません。

---

## タスク管理

### spawn

新しい並行タスクを作成して開始します。

**シグネチャ：**
```hemlock
spawn(async_fn: function, ...args): task
```

**パラメータ：**
- `async_fn` - 実行する非同期関数
- `...args` - 関数に渡す引数

**戻り値：** タスクハンドル

**例：**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 単一タスクをスポーン
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// 複数タスクをスポーン（並列実行！）
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// 3つすべてが同時に実行中
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**動作：**
- `pthread_create()`経由で新しいOSスレッドを作成
- すぐに関数の実行を開始
- 後で結合するためのタスクハンドルを返す
- タスクは別のCPUコアで並列実行

---

### join

タスクの完了を待ち、結果を取得します。

**シグネチャ：**
```hemlock
join(task: task): any
```

**パラメータ：**
- `task` - `spawn()`からのタスクハンドル

**戻り値：** タスクの戻り値

**例：**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // タスク完了までブロック
print(result);         // 3628800
```

**動作：**
- タスク完了まで現在のスレッドをブロック
- タスクの戻り値を返す
- タスクが投げた例外を伝播
- 戻り後にタスクリソースをクリーンアップ

**エラーハンドリング：**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Caught:", e);  // "Caught: Task failed!"
}
```

---

### detach

タスクをデタッチします（ファイア・アンド・フォーゲット実行）。

**シグネチャ：**
```hemlock
detach(task: task): null
```

**パラメータ：**
- `task` - `spawn()`からのタスクハンドル

**戻り値：** `null`

**例：**
```hemlock
async fn background_work() {
    print("Working in background...");
    return null;
}

let t = spawn(background_work);
detach(t);  // タスクは独立して実行を継続

// デタッチされたタスクは結合できない
// join(t);  // エラー
```

**動作：**
- タスクは独立して実行を継続
- デタッチされたタスクは`join()`できない
- タスク完了時にタスクとスレッドは自動的にクリーンアップ

**使用ケース：**
- ファイア・アンド・フォーゲットのバックグラウンドタスク
- ロギング/モニタリングタスク
- 値を返す必要がないタスク

---

## チャネル

チャネルはタスク間のスレッドセーフな通信を提供します。

### channel

バッファ付きチャネルを作成します。

**シグネチャ：**
```hemlock
channel(capacity: i32): channel
```

**パラメータ：**
- `capacity` - バッファサイズ（値の数）

**戻り値：** チャネルオブジェクト

**例：**
```hemlock
let ch = channel(10);  // 容量10のバッファ付きチャネル
let ch2 = channel(1);  // 最小バッファ（同期的）
let ch3 = channel(100); // 大きなバッファ
```

**動作：**
- スレッドセーフなチャネルを作成
- 同期にpthreadミューテックスを使用
- 容量は作成時に固定

---

### チャネルメソッド

#### send

チャネルに値を送信します（満杯の場合ブロック）。

**シグネチャ：**
```hemlock
channel.send(value: any): null
```

**パラメータ：**
- `value` - 送信する値（任意の型）

**戻り値：** `null`

**例：**
```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let t = spawn(producer, ch, 5);
```

**動作：**
- チャネルに値を送信
- チャネルが満杯の場合ブロック
- スレッドセーフ（ミューテックス使用）
- 値が送信されると戻る

---

#### recv

チャネルから値を受信します（空の場合ブロック）。

**シグネチャ：**
```hemlock
channel.recv(): any
```

**戻り値：** チャネルからの値、またはチャネルがクローズされ空の場合`null`

**例：**
```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let t = spawn(consumer, ch, 5);
```

**動作：**
- チャネルから値を受信
- チャネルが空の場合ブロック
- チャネルがクローズされ空の場合`null`を返す
- スレッドセーフ（ミューテックス使用）

---

#### close

チャネルをクローズします（これ以上の送信は不可）。

**シグネチャ：**
```hemlock
channel.close(): null
```

**戻り値：** `null`

**例：**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // これ以上値がないことを通知
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // チャネルがクローズ
        }
        print(val);
    }
    return null;
}
```

**動作：**
- チャネルをクローズ
- これ以上の送信は不可
- チャネルが空の場合`recv()`は`null`を返す
- スレッドセーフ

---

## 完全な並行性の例

### プロデューサー・コンシューマーパターン

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Producing:", i);
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        print("Consuming:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// チャネルを作成
let ch = channel(10);

// プロデューサーとコンシューマーをスポーン
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// 完了を待機
join(p);
let total = join(c);
print("Total:", total);  // 0+10+20+30+40 = 100
```

---

## 並列計算

### 複数タスクの例

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 複数タスクをスポーン（並列実行！）
let t1 = spawn(factorial, 5);   // スレッド1
let t2 = spawn(factorial, 6);   // スレッド2
let t3 = spawn(factorial, 7);   // スレッド3
let t4 = spawn(factorial, 8);   // スレッド4

// 4つすべてが同時に計算中！

// 結果を待機
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## タスクライフサイクル

### 状態遷移

1. **作成済み** - タスクがスポーンされたがまだ実行されていない
2. **実行中** - タスクがOSスレッドで実行中
3. **完了** - タスクが終了（結果が利用可能）
4. **結合済み** - 結果が取得され、リソースがクリーンアップ
5. **デタッチ済み** - タスクは独立して継続

### ライフサイクルの例

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. タスクを作成
let t = spawn(work, 21);  // 状態：実行中

// タスクは別スレッドで実行...

// 2. タスクを結合
let result = join(t);     // 状態：完了 → 結合済み
print(result);            // 42

// 結合後にタスクリソースがクリーンアップ
```

### デタッチのライフサイクル

```hemlock
async fn background() {
    print("Background task running");
    return null;
}

// 1. タスクを作成
let t = spawn(background);  // 状態：実行中

// 2. タスクをデタッチ
detach(t);                  // 状態：デタッチ済み

// タスクは独立して実行を継続
// 完了時にOSがリソースをクリーンアップ
```

---

## エラーハンドリング

### 例外の伝播

タスクで投げられた例外は結合時に伝播されます：

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

// 成功するタスク
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// 失敗するタスク
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Caught:", e);  // "Caught: Task failed!"
}
```

### 複数タスクのハンドリング

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task " + typeof(id) + " failed";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // 失敗する
let t3 = spawn(work, 3, 0);

// エラーハンドリング付きで結合
try {
    let r1 = join(t1);  // OK
    print("Task 1:", r1);

    let r2 = join(t2);  // 投げる
    print("Task 2:", r2);  // 到達しない
} catch (e) {
    print("Error:", e);  // "Error: Task 2 failed"
}

// 残りのタスクはまだ結合可能
let r3 = join(t3);
print("Task 3:", r3);
```

---

## パフォーマンス特性

### 真の並列処理

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 順次実行
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// 並列実行
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// マルチコアシステムではparallel_timeはsequential_timeの約50%になるはず
```

**実証された特性：**
- N個のタスクはN個のCPUコアを同時に使用可能
- ストレステストではウォール時間に対して8-9倍のCPU時間を示す（並列処理の証明）
- スレッドオーバーヘッド：タスクあたり約8KBスタック + pthreadオーバーヘッド
- 1つのタスクのブロッキング操作は他に影響しない

---

## 実装の詳細

### スレッディングモデル

- **1:1スレッディング** - 各タスク = 1 OSスレッド（`pthread`）
- **カーネルスケジュール** - OSカーネルがスレッドをコアに分散
- **プリエンプティブマルチタスキング** - OSがスレッドを中断して切り替え可能
- **GILなし** - グローバルインタプリタロックなし（Pythonとは異なる）

### 同期

- **ミューテックス** - チャネルは`pthread_mutex_t`を使用
- **条件変数** - ブロッキングsend/recvは`pthread_cond_t`を使用
- **ロックフリー操作** - タスク状態遷移はアトミック

### メモリとクリーンアップ

- **結合されたタスク** - `join()`後に自動クリーンアップ
- **デタッチされたタスク** - タスク完了時に自動クリーンアップ
- **チャネル** - 参照カウント、使用されなくなると解放

---

## 制限事項

- 複数チャネルの多重化のための`select()`なし
- ワークスティーリングスケジューラなし（タスクあたり1スレッド）
- 非同期I/O統合なし（ファイル/ネットワーク操作はブロック）
- チャネル容量は作成時に固定

---

## 完全なAPI要約

### 関数

| 関数 | シグネチャ | 戻り値 | 説明 |
|-----------|-----------------------------------|-----------|--------------------------------|
| `spawn`   | `(async_fn: function, ...args)`   | `task`    | 並行タスクを作成して開始 |
| `join`    | `(task: task)`                    | `any`     | タスクを待ち、結果を取得 |
| `detach`  | `(task: task)`                    | `null`    | タスクをデタッチ（ファイア・アンド・フォーゲット） |
| `channel` | `(capacity: i32)`                 | `channel` | スレッドセーフなチャネルを作成 |

### チャネルメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
|---------|-----------------|---------|----------------------------------|
| `send`  | `(value: any)`  | `null`  | 値を送信（満杯ならブロック） |
| `recv`  | `()`            | `any`   | 値を受信（空ならブロック） |
| `close` | `()`            | `null`  | チャネルをクローズ |

### 型

| 型 | 説明 |
|-----------|--------------------------------------|
| `task`    | 並行タスクのハンドル |
| `channel` | スレッドセーフな通信チャネル |

---

## ベストプラクティス

### すべきこと

- タスク間の通信にチャネルを使用
- 結合されたタスクからの例外をハンドル
- 送信完了時にチャネルをクローズ
- 結果の取得とクリーンアップに`join()`を使用
- 非同期関数のみをスポーン

### すべきでないこと

- 同期なしに可変状態を共有しない
- 同じタスクを2回結合しない
- クローズされたチャネルに送信しない
- 非async関数をスポーンしない
- タスクの結合を忘れない（デタッチしない限り）

---

## 関連項目

- [組み込み関数](builtins.md) - `spawn()`、`join()`、`detach()`、`channel()`
- [型システム](type-system.md) - タスクとチャネル型
