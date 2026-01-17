# Hemlockにおける非同期/並行処理

Hemlockは、async/await構文、タスクの生成、通信用チャネルを備えた**構造化並行処理**を提供します。実装はPOSIXスレッド（pthread）を使用した**真のマルチスレッド並列処理**を実現しています。

## 目次

- [概要](#概要)
- [スレッディングモデル](#スレッディングモデル)
- [非同期関数](#非同期関数)
- [タスクの生成](#タスクの生成)
- [チャネル](#チャネル)
- [例外の伝播](#例外の伝播)
- [実装の詳細](#実装の詳細)
- [ベストプラクティス](#ベストプラクティス)
- [パフォーマンス特性](#パフォーマンス特性)
- [現在の制限事項](#現在の制限事項)

## 概要

**これが意味すること：**
- ✅ **実際のOSスレッド** - 生成された各タスクは別々のpthread（POSIXスレッド）で実行される
- ✅ **真の並列処理** - タスクは複数のCPUコアで同時に実行される
- ✅ **カーネルスケジュール** - OSスケジューラがタスクを利用可能なコアに分散する
- ✅ **スレッドセーフなチャネル** - 同期にpthreadミューテックスと条件変数を使用

**これは以下ではない：**
- ❌ **グリーンスレッドではない** - ユーザー空間の協調的マルチタスクではない
- ❌ **async/awaitコルーチンではない** - JavaScript/Python asyncioのようなシングルスレッドイベントループではない
- ❌ **エミュレートされた並行処理ではない** - 疑似的な並列処理ではない

これは、OSスレッドを使用する際の**C、C++、Rustと同じスレッディングモデル**です。複数のコアにまたがる実際の並列実行が得られます。

## スレッディングモデル

### 1:1スレッディング

Hemlockは**1:1スレッディングモデル**を使用しています：
- 生成された各タスクは`pthread_create()`を介して専用のOSスレッドを作成する
- OSカーネルがスレッドを利用可能なCPUコアにスケジュールする
- プリエンプティブマルチタスク - OSがスレッド間を中断して切り替えることができる
- **GILなし** - Pythonとは異なり、並列処理を制限するグローバルインタプリタロックがない

### 同期メカニズム

- **ミューテックス** - チャネルはスレッドセーフなアクセスに`pthread_mutex_t`を使用
- **条件変数** - ブロッキングsend/recvは効率的な待機に`pthread_cond_t`を使用
- **ロックフリー操作** - タスク状態の遷移はアトミック

## 非同期関数

関数を`async`として宣言して、並行実行用に設計されていることを示すことができます：

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
```

### 重要なポイント

- `async fn`は非同期関数を宣言する
- 非同期関数は`spawn()`を使用して並行タスクとして生成できる
- 非同期関数は直接呼び出すこともできる（現在のスレッドで同期的に実行）
- 生成されると、各タスクは**独自のOSスレッド**で実行される（コルーチンではない！）
- `await`キーワードは将来の使用のために予約されている

### 例：直接呼び出しとスポーンの比較

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 直接呼び出し - 同期的に実行
let result1 = factorial(5);  // 120

// 生成されたタスク - 別のスレッドで実行
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## タスクの生成

`spawn()`を使用して非同期関数を**別のOSスレッドで並列に**実行します：

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// 複数のタスクを生成 - これらは異なるCPUコアで並列に実行される！
let t1 = spawn(factorial, 5);  // スレッド1
let t2 = spawn(factorial, 6);  // スレッド2
let t3 = spawn(factorial, 7);  // スレッド3

// 3つすべてが今同時に計算している！

// 結果を待つ
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### 組み込み関数

#### spawn(async_fn, arg1, arg2, ...)

新しいpthreadで新しいタスクを作成し、タスクハンドルを返します。

**パラメータ：**
- `async_fn` - 実行する非同期関数
- `arg1, arg2, ...` - 関数に渡す引数

**戻り値：** タスクハンドル（`join()`や`detach()`で使用する不透明な値）

**例：**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... 処理ロジック
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

タスクの完了を待ち（スレッドが終了するまでブロック）、結果を返します。

**パラメータ：**
- `task` - `spawn()`から返されたタスクハンドル

**戻り値：** 非同期関数が返した値

**例：**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // compute()が終了するまでブロック
print(result);
```

**重要：** 各タスクは一度だけjoinできます。以降のjoinはエラーになります。

#### detach(task)

ファイアアンドフォーゲット実行（スレッドは独立して実行され、joinは許可されない）。

**パラメータ：**
- `task` - `spawn()`から返されたタスクハンドル

**戻り値：** `null`

**例：**
```hemlock
async fn background_work() {
    // 長時間実行されるバックグラウンドタスク
    // ...
}

let task = spawn(background_work);
detach(task);  // タスクは独立して実行され、joinできない
```

**重要：** デタッチされたタスクはjoinできません。タスクが完了すると、pthreadとTaskの両方の構造体が自動的にクリーンアップされます。

## チャネル

チャネルは、ブロッキングセマンティクスを持つ境界付きバッファを使用して、タスク間のスレッドセーフな通信を提供します。

### チャネルの作成

```hemlock
let ch = channel(10);  // バッファサイズ10のチャネルを作成
```

**パラメータ：**
- `capacity`（i32） - チャネルが保持できる値の最大数

**戻り値：** チャネルオブジェクト

### チャネルメソッド

#### send(value)

チャネルに値を送信します（満杯の場合はブロック）。

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
let task = spawn(producer, ch, 5);
```

**動作：**
- チャネルにスペースがあれば、値はすぐに追加される
- チャネルが満杯の場合、送信者はスペースが利用可能になるまでブロックする
- チャネルが閉じられている場合、例外をスロー

#### recv()

チャネルから値を受信します（空の場合はブロック）。

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
let task = spawn(consumer, ch, 5);
```

**動作：**
- チャネルに値があれば、次の値をすぐに返す
- チャネルが空の場合、受信者は値が利用可能になるまでブロックする
- チャネルが閉じられ空の場合、`null`を返す

#### close()

チャネルを閉じます（閉じられたチャネルでのrecvはnullを返す）。

```hemlock
ch.close();
```

**動作：**
- 以降の`send()`操作を防ぐ（例外をスローする）
- 保留中の`recv()`操作は完了できる
- 空になると、`recv()`は`null`を返す

### select()による多重化

`select()`関数は、複数のチャネルを同時に待機し、いずれかのチャネルでデータが利用可能になったときに返します。

**シグネチャ：**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**パラメータ：**
- `channels` - チャネル値の配列
- `timeout_ms`（オプション） - ミリ秒単位のタイムアウト（-1または省略で無限待機）

**戻り値：**
- `{ channel, value }` - データを持っていたチャネルと受信した値を含むオブジェクト
- `null` - タイムアウト時（タイムアウトが指定されている場合）

**例：**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// プロデューサータスク
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// 最初の結果を待つ（ch2の方が速いはず）
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"

// 2番目の結果を待つ
let result2 = select([ch1, ch2]);
print(result2.value);  // "from channel 1"
```

**タイムアウト付き：**
```hemlock
let ch = channel(1);

// 送信者がいないのでタイムアウトする
let result = select([ch], 100);  // 100msタイムアウト
if (result == null) {
    print("タイムアウトしました！");
}
```

**ユースケース：**
- 複数のデータソースの中で最も速いものを待つ
- チャネル操作にタイムアウトを実装する
- 複数のイベントソースを持つイベントループパターン
- ファンイン：複数のチャネルを1つにマージ

**ファンインパターン：**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // すべてのチャネルが閉じられた
        }
        output.send(result.value);
    }
    output.close();
}
```

### 完全なプロデューサー・コンシューマーの例

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

// バッファサイズ付きでチャネルを作成
let ch = channel(10);

// プロデューサーとコンシューマーを生成
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// 完了を待つ
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### マルチプロデューサー、マルチコンシューマー

チャネルは複数のプロデューサーとコンシューマー間で安全に共有できます：

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// 複数のプロデューサー
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// 複数のコンシューマー
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// すべてを待つ
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## 例外の伝播

生成されたタスクでスローされた例外は、joinされたときに伝播されます：

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "タスクが失敗しました！";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("キャッチ: " + e);  // "キャッチ: タスクが失敗しました！"
}
```

### 例外処理パターン

**パターン1：タスク内で処理**
```hemlock
async fn safe_task() {
    try {
        // リスクのある操作
    } catch (e) {
        print("タスク内でエラー: " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // 例外は伝播されない
```

**パターン2：呼び出し元に伝播**
```hemlock
async fn task_that_throws() {
    throw "エラー";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("タスクからキャッチ: " + e);
}
```

**パターン3：例外を持つデタッチされたタスク**
```hemlock
async fn detached_task() {
    try {
        // 作業
    } catch (e) {
        // 内部で処理する必要がある - 伝播できない
        print("エラー: " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // デタッチされたタスクからは例外をキャッチできない
```

## 実装の詳細

### スレッディングアーキテクチャ

- **1:1スレッディング** - 生成された各タスクは`pthread_create()`を介して専用のOSスレッドを作成する
- **カーネルスケジュール** - OSカーネルがスレッドを利用可能なCPUコアにスケジュールする
- **プリエンプティブマルチタスク** - OSがスレッド間を中断して切り替えることができる
- **GILなし** - Pythonとは異なり、並列処理を制限するグローバルインタプリタロックがない

### チャネルの実装

チャネルはpthread同期を備えた循環バッファを使用します：

```
チャネル構造体：
- buffer[] - 値の固定サイズ配列
- capacity - 要素の最大数
- size - 現在の要素数
- head - 読み取り位置
- tail - 書き込み位置
- mutex - スレッドセーフなアクセス用のpthread_mutex_t
- not_empty - ブロッキングrecv用のpthread_cond_t
- not_full - ブロッキングsend用のpthread_cond_t
- closed - ブール値フラグ
- refcount - クリーンアップ用の参照カウント
```

**ブロッキング動作：**
- 満杯のチャネルでの`send()`: `not_full`条件変数で待機
- 空のチャネルでの`recv()`: `not_empty`条件変数で待機
- 両方とも反対の操作によって適切にシグナルされる

### メモリとクリーンアップ

- **joinされたタスク:** `join()`が返った後に自動的にクリーンアップされる
- **デタッチされたタスク:** タスクが完了すると自動的にクリーンアップされる
- **チャネル:** 参照カウントされ、使用されなくなったときに解放される

## ベストプラクティス

### 1. 常にチャネルを閉じる

```hemlock
async fn producer(ch) {
    // ... 値を送信
    ch.close();  // 重要：これ以上の値がないことを通知
}
```

### 2. 構造化並行処理を使用する

同じスコープ内でタスクを生成してjoinする：

```hemlock
fn process_data(data) {
    // タスクを生成
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // 返す前に常にjoinする
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. 例外を適切に処理する

```hemlock
async fn task() {
    try {
        // リスクのある操作
    } catch (e) {
        // エラーをログに記録
        throw e;  // 呼び出し元が知る必要がある場合は再スロー
    }
}
```

### 4. 適切なチャネル容量を使用する

- **小さい容量（1-10）:** 調整/シグナル用
- **中程度の容量（10-100）:** 一般的なプロデューサー・コンシューマー用
- **大きい容量（100以上）:** 高スループットシナリオ用

```hemlock
let signal_ch = channel(1);      // 調整
let work_ch = channel(50);       // ワークキュー
let buffer_ch = channel(1000);   // 高スループット
```

### 5. 必要な場合のみデタッチする

より良いリソース管理のために`detach()`よりも`join()`を優先する：

```hemlock
// 良い：joinして結果を取得
let task = spawn(work);
let result = join(task);

// 真のファイアアンドフォーゲットにのみdetachを使用
let bg_task = spawn(background_logging);
detach(bg_task);  // 独立して実行される
```

## パフォーマンス特性

### 真の並列処理

- **N個の生成されたタスクがN個のCPUコアを同時に利用できる**
- 実証済みの高速化 - ストレステストではウォール時間に対してCPU時間が8-9倍を示す（複数のコアが動作）
- コア数に応じた線形スケーリング（スレッド数まで）

### スレッドオーバーヘッド

- 各タスクには約8KBのスタック + pthreadオーバーヘッドがある
- スレッド作成コスト：約10-20μs
- コンテキストスイッチコスト：約1-5μs

### asyncを使用するタイミング

**良いユースケース：**
- 並列化可能なCPU集中型計算
- I/Oバウンド操作（ただしI/Oはまだブロッキング）
- 独立したデータの並行処理
- チャネルを使用したパイプラインアーキテクチャ

**理想的でないケース：**
- 非常に短いタスク（スレッドオーバーヘッドが支配的）
- 重い同期を持つタスク（競合オーバーヘッド）
- シングルコアシステム（並列化の利点なし）

### ブロッキングI/Oも安全

1つのタスクでのブロッキング操作は他をブロックしない：

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // このスレッドのみブロック
    let content = f.read();       // このスレッドのみブロック
    f.close();
    return content;
}

// 両方が並行して読み取る（異なるスレッドで）
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## スレッド安全性モデル

Hemlockは、タスクが共有可変状態ではなくチャネル経由で通信する**メッセージパッシング**並行処理モデルを使用します。

### 引数の分離

タスクを生成するとき、データ競合を防ぐために**引数はディープコピー**されます：

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // コピーを変更、元は変更されない
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - 変更されていない！
print(modified.length);  // 4 - 新しい要素がある
```

**ディープコピーされるもの：**
- 配列（およびすべての要素を再帰的に）
- オブジェクト（およびすべてのフィールドを再帰的に）
- 文字列
- バッファ

**共有されるもの（参照が保持される）：**
- チャネル（通信メカニズム - 意図的に共有）
- タスクハンドル（調整用）
- 関数（コードは不変）
- ファイルハンドル（OSが並行アクセスを管理）
- ソケットハンドル（OSが並行アクセスを管理）

**渡せないもの：**
- 生のポインタ（`ptr`） - 代わりに`buffer`を使用

### なぜメッセージパッシングなのか？

これはHemlockの「暗黙より明示」の哲学に従っています：

```hemlock
// 悪い例：共有可変状態（データ競合を引き起こす）
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // 競合！
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // 競合！

// 良い例：チャネル経由のメッセージパッシング
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - 競合条件なし
```

### 参照カウントのスレッド安全性

すべての参照カウント操作は、解放後使用バグを防ぐために**アトミック操作**を使用します：
- `string_retain/release` - アトミック
- `array_retain/release` - アトミック
- `object_retain/release` - アトミック
- `buffer_retain/release` - アトミック
- `function_retain/release` - アトミック
- `channel_retain/release` - アトミック
- `task_retain/release` - アトミック

これにより、値がスレッド間で共有されている場合でも、安全なメモリ管理が保証されます。

### クロージャ環境へのアクセス

タスクは以下のクロージャ環境にアクセスできます：
- 組み込み関数（`print`、`len`など）
- グローバル関数定義
- 定数と変数

クロージャ環境は環境ごとのミューテックスによって保護されており、
並行読み書きがスレッドセーフになります：

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK：クロージャ変数の読み取り（スレッドセーフ）
}

async fn modify_closure() {
    x = 20;  // OK：クロージャ変数への書き込み（ミューテックスで同期）
}
```

**注意：** 並行アクセスは同期されますが、複数のタスクから共有状態を変更すると
論理的な競合条件（非決定論的な順序）が発生する可能性があります。予測可能な動作のためには、
タスク通信にチャネルを使用するか、タスクから値を返してください。

タスクからデータを返す必要がある場合は、戻り値またはチャネルを使用してください。

## 現在の制限事項

### 1. ワークスティーリングスケジューラがない

タスクごとに1スレッドを使用するため、多くの短いタスクでは非効率になる可能性があります。

**現在：** 1000タスク = 1000スレッド（重いオーバーヘッド）

**計画中：** より効率的なワークスティーリング付きスレッドプール

### 3. 非同期I/O統合がない

ファイル/ネットワーク操作はまだスレッドをブロックします：

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // スレッドをブロック
    f.close();
    return content;
}
```

**回避策：** 並行I/O操作には複数のスレッドを使用

### 4. 固定チャネル容量

チャネル容量は作成時に設定され、サイズ変更できません：

```hemlock
let ch = channel(10);
// 動的に20にサイズ変更できない
```

### 5. チャネルサイズは固定

チャネルバッファサイズは作成後に変更できません。

## 一般的なパターン

### 並列マップ

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // ワーカーを生成
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // データを送信
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // 結果を収集
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // ワーカーを待つ
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### パイプラインアーキテクチャ

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// パイプラインを作成
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// 入力をフィード
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// 出力を収集
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### ファンアウト、ファンイン

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // 値を処理
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// ファンアウト：複数のワーカー
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// 作業を送信
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// ファンイン：すべての結果を収集
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// すべてのワーカーを待つ
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## まとめ

Hemlockの非同期/並行処理モデルは以下を提供します：

- ✅ OSスレッドを使用した真のマルチスレッド並列処理
- ✅ シンプルで構造化された並行処理プリミティブ
- ✅ 通信用のスレッドセーフなチャネル
- ✅ タスク間の例外伝播
- ✅ マルチコアシステムでの実証済みパフォーマンス
- ✅ **引数の分離** - ディープコピーによるデータ競合の防止
- ✅ **アトミック参照カウント** - スレッド間での安全なメモリ管理

これによりHemlockは以下に適しています：
- 並列計算
- 並行I/O操作
- パイプラインアーキテクチャ
- プロデューサー・コンシューマーパターン

以下の複雑さを回避しながら：
- 手動スレッド管理
- 低レベル同期プリミティブ
- デッドロックを起こしやすいロックベース設計
- 共有可変状態のバグ
