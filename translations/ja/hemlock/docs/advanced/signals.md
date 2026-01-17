# Hemlockでのシグナル処理

Hemlockは、SIGINT（Ctrl+C）、SIGTERM、カスタムシグナルなどのシステムシグナルを管理するための**POSIXシグナル処理**を提供します。これにより、低レベルのプロセス制御とプロセス間通信が可能になります。

## 目次

- [概要](#概要)
- [シグナルAPI](#シグナルapi)
- [シグナル定数](#シグナル定数)
- [基本的なシグナル処理](#基本的なシグナル処理)
- [高度なパターン](#高度なパターン)
- [シグナルハンドラの動作](#シグナルハンドラの動作)
- [安全性の考慮事項](#安全性の考慮事項)
- [一般的な使用ケース](#一般的な使用ケース)
- [完全な例](#完全な例)

## 概要

シグナル処理により、プログラムは以下のことができます：
- ユーザー割り込み（Ctrl+C、Ctrl+Z）に応答
- グレースフルシャットダウンを実装
- 終了リクエストを処理
- プロセス間通信にカスタムシグナルを使用
- アラーム/タイマーメカニズムを作成

**重要：**シグナル処理はHemlockの哲学において**本質的にアンセーフ**です。ハンドラはいつでも呼び出され、通常の実行を中断する可能性があります。ユーザーは適切な同期に責任を持ちます。

## シグナルAPI

### signal(signum, handler_fn)

シグナルハンドラ関数を登録します。

**パラメータ：**
- `signum`（i32）- シグナル番号（SIGINT、SIGTERMなどの定数）
- `handler_fn`（関数またはnull）- シグナル受信時に呼び出す関数、または`null`でデフォルトにリセット

**戻り値：**前のハンドラ関数（なければ`null`）

**例：**
```hemlock
fn my_handler(sig) {
    print("Caught signal: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**デフォルトにリセット：**
```hemlock
signal(SIGINT, null);  // SIGINTをデフォルト動作にリセット
```

### raise(signum)

現在のプロセスにシグナルを送信します。

**パラメータ：**
- `signum`（i32）- 送信するシグナル番号

**戻り値：**`null`

**例：**
```hemlock
raise(SIGUSR1);  // SIGUSR1ハンドラをトリガー
```

## シグナル定数

Hemlockは標準POSIXシグナル定数をi32値として提供します。

### 割り込みと終了

| 定数 | 値 | 説明 | 一般的なトリガー |
|----------|-------|-------------|----------------|
| `SIGINT` | 2 | キーボードからの割り込み | Ctrl+C |
| `SIGTERM` | 15 | 終了リクエスト | `kill`コマンド |
| `SIGQUIT` | 3 | キーボードからの終了 | Ctrl+\ |
| `SIGHUP` | 1 | ハングアップ検出 | ターミナルが閉じられた |
| `SIGABRT` | 6 | アボートシグナル | `abort()`関数 |

**例：**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // killコマンド
signal(SIGHUP, handle_hangup);      // ターミナルが閉じる
```

### ユーザー定義シグナル

| 定数 | 値 | 説明 | 使用ケース |
|----------|-------|-------------|----------|
| `SIGUSR1` | 10 | ユーザー定義シグナル1 | カスタムIPC |
| `SIGUSR2` | 12 | ユーザー定義シグナル2 | カスタムIPC |

**例：**
```hemlock
// カスタム通信に使用
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### プロセス制御

| 定数 | 値 | 説明 | 備考 |
|----------|-------|-------------|-------|
| `SIGALRM` | 14 | アラームクロックタイマー | `alarm()`後 |
| `SIGCHLD` | 17 | 子プロセスステータス変更 | プロセス管理 |
| `SIGCONT` | 18 | 停止していれば続行 | SIGSTOP後に再開 |
| `SIGSTOP` | 19 | プロセスを停止 | **キャッチ不可** |
| `SIGTSTP` | 20 | ターミナル停止 | Ctrl+Z |

**例：**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### I/Oシグナル

| 定数 | 値 | 説明 | 送信されるとき |
|----------|-------|-------------|-----------|
| `SIGPIPE` | 13 | パイプ破損 | 閉じたパイプへの書き込み |
| `SIGTTIN` | 21 | バックグラウンドでターミナルから読み取り | BGプロセスがTTYを読み取り |
| `SIGTTOU` | 22 | バックグラウンドでターミナルに書き込み | BGプロセスがTTYに書き込み |

**例：**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## 基本的なシグナル処理

### Ctrl+Cのキャッチ

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("Caught SIGINT!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// プログラムは実行を継続...
// ユーザーがCtrl+Cを押す -> handle_interrupt()が呼び出される

while (!interrupted) {
    // 作業を実行...
}

print("Exiting due to interrupt");
```

### ハンドラ関数のシグネチャ

シグナルハンドラは1つの引数を受け取ります：シグナル番号（i32）

```hemlock
fn my_handler(signum) {
    print("Received signal: " + typeof(signum));
    // signumにはシグナル番号が含まれる（例：SIGINTの場合は2）

    if (signum == SIGINT) {
        print("This is SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // 複数のシグナルに同じハンドラ
```

### 複数のシグナルハンドラ

異なるシグナルに異なるハンドラ：

```hemlock
fn handle_int(sig) {
    print("SIGINT received");
}

fn handle_term(sig) {
    print("SIGTERM received");
}

fn handle_usr1(sig) {
    print("SIGUSR1 received");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### デフォルト動作へのリセット

ハンドラとして`null`を渡すとデフォルト動作にリセット：

```hemlock
// カスタムハンドラを登録
signal(SIGINT, my_handler);

// 後で、デフォルトにリセット（SIGINTで終了）
signal(SIGINT, null);
```

### シグナルを手動で発生

自分のプロセスにシグナルを送信：

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// ハンドラを手動でトリガー
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## 高度なパターン

### グレースフルシャットダウンパターン

終了時のクリーンアップの一般的なパターン：

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Shutting down gracefully...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// メインループ
while (!should_exit) {
    // 作業を実行...
    // should_exitフラグを定期的にチェック
}

print("Cleanup complete");
```

### シグナルカウンター

受信したシグナルの数を追跡：

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Received " + typeof(signal_count) + " signals");
}

signal(SIGUSR1, count_signals);

// 後で...
print("Total signals: " + typeof(signal_count));
```

### シグナルによる設定リロード

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Reloading configuration...");
    config = load_config();
    print("Configuration reloaded");
}

signal(SIGHUP, reload_config);  // SIGHUPでリロード

// 設定をリロードするためにプロセスにSIGHUPを送信
// シェルから: kill -HUP <pid>
```

### SIGALRMを使用したタイムアウト

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// アラームを設定（Hemlockではまだ実装されていない、例のみ）
// alarm(5);  // 5秒タイムアウト

while (!timed_out) {
    // タイムアウト付きで作業を実行
}
```

### シグナルベースのステートマシン

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("State: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("State: " + typeof(state));
}

signal(SIGUSR1, next_state);  // 状態を進める
signal(SIGUSR2, prev_state);  // 戻る

// ステートマシンを制御：
// kill -USR1 <pid>  # 次の状態
// kill -USR2 <pid>  # 前の状態
```

## シグナルハンドラの動作

### 重要な注意事項

**ハンドラの実行：**
- ハンドラはシグナル受信時に**同期的に**呼び出される
- ハンドラは現在のプロセスコンテキストで実行
- シグナルハンドラは定義された関数のクロージャ環境を共有
- ハンドラは外部スコープの変数（グローバルやキャプチャされた変数など）にアクセスして変更可能

**ベストプラクティス：**
- ハンドラはシンプルで迅速に - 長時間実行の操作を避ける
- 複雑なロジックではなくフラグを設定
- ロックを取る可能性のある関数の呼び出しを避ける
- ハンドラが任意の操作を中断できることに注意

### キャッチできるシグナル

**キャッチして処理できる：**
- SIGINT、SIGTERM、SIGUSR1、SIGUSR2、SIGHUP、SIGQUIT
- SIGALRM、SIGCHLD、SIGCONT、SIGTSTP
- SIGPIPE、SIGTTIN、SIGTTOU
- SIGABRT（ただしハンドラが戻った後にプログラムはアボート）

**キャッチできない：**
- `SIGKILL`（9）- 常にプロセスを終了
- `SIGSTOP`（19）- 常にプロセスを停止

**システム依存：**
- 一部のシグナルはシステムによってデフォルト動作が異なる場合がある
- 詳細はプラットフォームのシグナルドキュメントを確認

### ハンドラの制限

```hemlock
fn complex_handler(sig) {
    // シグナルハンドラでこれらを避ける：

    // 長時間実行の操作
    // process_large_file();

    // ブロッキングI/O
    // let f = open("log.txt", "a");
    // f.write("Signal received\n");

    // 複雑な状態変更
    // rebuild_entire_data_structure();

    // シンプルなフラグ設定は安全
    let should_stop = true;

    // シンプルなカウンタ更新は通常安全
    let signal_count = signal_count + 1;
}
```

## 安全性の考慮事項

シグナル処理はHemlockの哲学において**本質的にアンセーフ**です。

### レースコンディション

ハンドラはいつでも呼び出され、通常の実行を中断する可能性があります：

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // カウンター更新中に呼び出されるとレースコンディション
}

signal(SIGUSR1, increment);

// メインコードもカウンターを変更
counter = counter + 1;  // シグナルハンドラに中断される可能性
```

**問題：**メインコードが`counter`を更新中にシグナルが到着すると、結果は予測不能です。

### 非同期シグナル安全性

Hemlockは非同期シグナル安全性を**保証しません**：
- ハンドラは任意のHemlockコードを呼び出せる（Cの制限された非同期シグナル安全関数とは異なり）
- これは柔軟性を提供するが、ユーザーの注意が必要
- ハンドラが共有状態を変更する場合、レースコンディションが可能

### 安全なシグナル処理のベストプラクティス

**1. アトミックフラグを使用**

シンプルなブール代入は一般的に安全：

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // シンプルな代入は安全
}

signal(SIGINT, handler);

while (!should_exit) {
    // 作業...
}
```

**2. 共有状態を最小化**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // この1つの変数のみを変更
    interrupt_count = interrupt_count + 1;
}
```

**3. 複雑な操作を延期**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // フラグを設定するだけ
}

signal(SIGHUP, signal_reload);

// メインループで：
while (true) {
    if (pending_reload) {
        reload_config();  // ここで複雑な作業を実行
        pending_reload = false;
    }

    // 通常の作業...
}
```

**4. 再入可能性の問題を避ける**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // メインコードが使用中はデータを変更しない
        return;
    }
    // 続行しても安全
}
```

## 一般的な使用ケース

### 1. グレースフルサーバーシャットダウン

```hemlock
let running = true;

fn shutdown(sig) {
    print("Shutdown signal received");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// サーバーメインループ
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Server stopped");
```

### 2. 設定リロード（再起動なし）

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Reloading configuration...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // configを使用...
}
```

### 3. ログローテーション

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // 古いログの名前を変更し、新しいものを開く
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // 通常のロギング...
    log_file.write("Log entry\n");
}
```

### 4. ステータス報告

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Status: " + typeof(requests_handled) + " requests handled");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// シェルから: kill -USR1 <pid>
```

### 5. デバッグモード切り替え

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Debug mode: ON");
    } else {
        print("Debug mode: OFF");
    }
}

signal(SIGUSR2, toggle_debug);

// シェルから: kill -USR2 <pid> で切り替え
```

## 完全な例

### 例1：クリーンアップ付き割り込みハンドラ

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Interrupt detected (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("User signal 1 received");
    }
}

// ハンドラを登録
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// 作業をシミュレート
let i = 0;
while (running && i < 100) {
    print("Working... " + typeof(i));

    // 10回ごとにSIGUSR1をトリガー
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Total signals received: " + typeof(signal_count));
```

### 例2：マルチシグナルステートマシン

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("State: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("State: " + state);
}

fn report_stats(sig) {
    print("State: " + state);
    print("Requests: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // 作業を実行
        request_count = request_count + 1;
    }

    // 各イテレーションでチェック...
}
```

### 例3：ワーカープールコントローラ

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Workers: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Workers: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Shutting down...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// メインループはworker_countに基づいてワーカープールを調整
while (!should_exit) {
    // worker_countに基づいてワーカーを管理
    // ...
}
```

### 例4：タイムアウトパターン

```hemlock
let operation_complete = false;
let timed_out = false;

fn timeout_handler(sig) {
    timed_out = true;
}

signal(SIGALRM, timeout_handler);

// 長い操作を開始
async fn long_operation() {
    // ...作業
    operation_complete = true;
}

let task = spawn(long_operation);

// タイムアウト付きで待機（手動チェック）
let elapsed = 0;
while (!operation_complete && elapsed < 1000) {
    // スリープまたはチェック
    elapsed = elapsed + 1;
}

if (!operation_complete) {
    print("Operation timed out");
    detach(task);  // 待機をあきらめる
} else {
    join(task);
    print("Operation completed");
}
```

## シグナルハンドラのデバッグ

### 診断プリントを追加

```hemlock
fn debug_handler(sig) {
    print("Handler called for signal: " + typeof(sig));
    print("Stack: (not yet available)");

    // ハンドラロジック...
}

signal(SIGINT, debug_handler);
```

### シグナル呼び出しをカウント

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Handler call #" + typeof(handler_calls));

    // ハンドラロジック...
}
```

### raise()でテスト

```hemlock
fn test_handler(sig) {
    print("Test signal received: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// 手動で発生させてテスト
raise(SIGUSR1);
print("Handler should have been called");
```

## まとめ

Hemlockのシグナル処理は以下を提供します：

- 低レベルプロセス制御のためのPOSIXシグナル処理
- 15の標準シグナル定数
- シンプルなsignal()とraise() API
- クロージャサポート付きの柔軟なハンドラ関数
- 複数のシグナルでハンドラを共有可能

覚えておくべきこと：
- シグナル処理は本質的にアンセーフ - 注意して使用
- ハンドラはシンプルで高速に保つ
- 複雑な操作ではなく、状態変更にはフラグを使用
- ハンドラはいつでも実行を中断できる
- SIGKILLやSIGSTOPはキャッチできない
- raise()でハンドラを徹底的にテスト

一般的なパターン：
- グレースフルシャットダウン（SIGINT、SIGTERM）
- 設定リロード（SIGHUP）
- ログローテーション（SIGUSR1）
- ステータス報告（SIGUSR1/SIGUSR2）
- デバッグモード切り替え（SIGUSR2）
