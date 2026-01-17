# Hemlockでのコマンド実行

Hemlockは、シェルコマンドを実行してその出力をキャプチャするための**`exec()`組み込み関数**を提供します。

## 目次

- [概要](#概要)
- [exec()関数](#exec関数)
- [結果オブジェクト](#結果オブジェクト)
- [基本的な使用方法](#基本的な使用方法)
- [高度な例](#高度な例)
- [エラー処理](#エラー処理)
- [実装の詳細](#実装の詳細)
- [セキュリティ上の考慮事項](#セキュリティ上の考慮事項)
- [制限事項](#制限事項)
- [使用ケース](#使用ケース)
- [ベストプラクティス](#ベストプラクティス)
- [完全な例](#完全な例)

## 概要

`exec()`関数により、Hemlockプログラムは以下のことができます：
- シェルコマンドを実行
- 標準出力（stdout）をキャプチャ
- 終了ステータスコードを確認
- シェル機能（パイプ、リダイレクトなど）を使用
- システムユーティリティと統合

**重要：**コマンドは`/bin/sh`を通じて実行され、完全なシェル機能を提供しますが、セキュリティ上の考慮事項も生じます。

## exec()関数

### シグネチャ

```hemlock
exec(command: string): object
```

**パラメータ：**
- `command`（string）- 実行するシェルコマンド

**戻り値：**2つのフィールドを持つオブジェクト：
- `output`（string）- コマンドのstdout出力
- `exit_code`（i32）- コマンドの終了ステータスコード

### 基本的な例

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## 結果オブジェクト

`exec()`が返すオブジェクトは以下の構造を持ちます：

```hemlock
{
    output: string,      // コマンドのstdout（キャプチャされた出力）
    exit_code: i32       // プロセスの終了ステータス（0 = 成功）
}
```

### outputフィールド

コマンドによってstdoutに書き込まれたすべてのテキストを含みます。

**プロパティ：**
- コマンドが出力を生成しない場合は空文字列
- 改行と空白はそのまま含まれる
- 複数行の出力は保持される
- サイズ制限なし（動的に割り当て）

**例：**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // 改行付きのディレクトリリスト

let r3 = exec("true");
print(r3.output);  // ""（空文字列）
```

### exit_codeフィールド

コマンドの終了ステータスコード。

**値：**
- `0`は通常成功を示す
- `1-255`はエラーを示す（規則はコマンドによって異なる）
- `-1`はコマンドが実行できなかったか、異常終了した場合

**例：**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0（成功）

let r2 = exec("false");
print(r2.exit_code);  // 1（失敗）

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2（ファイルが見つからない、コマンドによって異なる）
```

## 基本的な使用方法

### 単純なコマンド

```hemlock
let r = exec("ls -la");
print(r.output);
print("Exit code: " + typeof(r.exit_code));
```

### 終了ステータスの確認

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found: " + r.output);
} else {
    print("Pattern not found");
}
```

### パイプ付きコマンド

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### 複数コマンド

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### コマンド置換

```hemlock
let r = exec("echo $(date)");
print(r.output);  // 現在の日付
```

## 高度な例

### 失敗の処理

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Command failed with code: " + typeof(r.exit_code));
    print("Error output: " + r.output);  // 注意：stderrはキャプチャされない
}
```

### 複数行出力の処理

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### コマンドチェーン

**&& (AND)の使用：**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup complete");
}
```

**|| (OR)の使用：**
```hemlock
let r = exec("command1 || command2");
// command1が失敗した場合のみcommand2を実行
```

**; (シーケンス)の使用：**
```hemlock
let r = exec("command1; command2");
// 成功/失敗に関係なく両方を実行
```

### パイプの使用

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**複雑なパイプライン：**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### 終了コードパターン

異なる終了コードは異なる状態を示します：

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
} else if (r.exit_code == 1) {
    print("File does not exist");
} else {
    print("Test command failed: " + typeof(r.exit_code));
}
```

### 出力リダイレクト

```hemlock
// シェル内でstdoutをファイルにリダイレクト
let r1 = exec("echo 'test' > /tmp/output.txt");

// stderrをstdoutにリダイレクト（注意：stderrはまだHemlockにキャプチャされない）
let r2 = exec("command 2>&1");
```

### 環境変数

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### 作業ディレクトリの変更

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## エラー処理

### exec()が例外をスローする場合

`exec()`関数はコマンドが実行できない場合に例外をスローします：

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Failed to execute: " + e);
}
```

**例外がスローされる場合：**
- `popen()`が失敗した場合（例：パイプを作成できない）
- システムリソース制限を超えた場合
- メモリ割り当てエラー

### exec()が例外をスローしない場合

```hemlock
// コマンドは実行されるがゼロ以外の終了コードを返す
let r1 = exec("false");
print(r1.exit_code);  // 1（例外ではない）

// コマンドが出力を生成しない
let r2 = exec("true");
print(r2.output);  // ""（例外ではない）

// シェルでコマンドが見つからない
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127（例外ではない）
```

### 安全な実行パターン

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Warning: Command failed with code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Error executing command: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## 実装の詳細

### 動作の仕組み

**内部処理：**
- `popen()`を使用して`/bin/sh`経由でコマンドを実行
- stdoutのみをキャプチャ（stderrはキャプチャされない）
- 出力は動的にバッファリング（4KBから開始、必要に応じて拡張）
- 終了ステータスは`WIFEXITED()`と`WEXITSTATUS()`マクロを使用して抽出
- 出力文字列は適切にnull終端される

**プロセスフロー：**
1. `popen(command, "r")`がパイプを作成してプロセスをフォーク
2. 子プロセスが`/bin/sh -c "command"`を実行
3. 親が成長するバッファにパイプ経由でstdoutを読み取り
4. `pclose()`が子を待機し、終了ステータスを返す
5. 終了ステータスが抽出され、結果オブジェクトに格納

### パフォーマンスの考慮事項

**コスト：**
- 各呼び出しで新しいシェルプロセスを作成（約1-5msのオーバーヘッド）
- 出力は完全にメモリに格納（ストリーミングではない）
- ストリーミングサポートなし（コマンドの完了を待つ）
- 適度な出力サイズのコマンドに適している

**最適化：**
- バッファは4KBで開始し、満杯になると倍増（効率的なメモリ使用）
- 単一の読み取りループでシステムコールを最小化
- 追加の文字列コピーなし

**使用すべき場合：**
- 短時間実行のコマンド（< 1秒）
- 適度な出力サイズ（< 10MB）
- 合理的な間隔のバッチ操作

**使用すべきでない場合：**
- 長時間実行のデーモンやサービス
- ギガバイトの出力を生成するコマンド
- リアルタイムストリーミングデータ処理
- 高頻度実行（> 100回/秒）

## セキュリティ上の考慮事項

### シェルインジェクションのリスク

⚠️ **重要：**コマンドはシェル（`/bin/sh`）によって実行されるため、**シェルインジェクションが可能**です。

**脆弱なコード：**
```hemlock
// 危険 - これをしないでください
let filename = args[1];  // ユーザー入力
let r = exec("cat " + filename);  // シェルインジェクション！
```

**攻撃：**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# 実行される: cat ; rm -rf /; echo pwned
```

### 安全なプラクティス

**1. サニタイズされていないユーザー入力を使用しない：**
```hemlock
// 悪い例
let user_input = args[1];
let r = exec("process " + user_input);  // 危険

// 良い例 - 最初に検証
fn is_safe_filename(name: string): bool {
    // 英数字、ダッシュ、アンダースコア、ドットのみを許可
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Invalid filename");
}
```

**2. 拒否リストではなく許可リストを使用：**
```hemlock
// 良い例 - 厳密な許可リスト
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Invalid command");
}
```

**3. 特殊文字をエスケープ：**
```hemlock
fn shell_escape(s: string): string {
    // シンプルなエスケープ - シングルクォートで囲み、シングルクォートをエスケープ
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. ファイル操作にexec()を使用しない：**
```hemlock
// 悪い例 - ファイル操作にexecを使用
let r = exec("cat file.txt");

// 良い例 - HemlockのファイルAPIを使用
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 権限の考慮事項

コマンドはHemlockプロセスと同じ権限で実行されます：

```hemlock
// Hemlockがrootで実行されている場合、exec()コマンドもrootで実行されます！
let r = exec("rm -rf /important");  // rootで実行している場合は危険
```

**ベストプラクティス：**必要最小限の権限でHemlockを実行してください。

## 制限事項

### 1. stderrキャプチャなし

stdoutのみがキャプチャされ、stderrはターミナルに出力されます：

```hemlock
let r = exec("ls /nonexistent");
// r.outputは空
// エラーメッセージはターミナルに表示され、キャプチャされない
```

**回避策 - stderrをstdoutにリダイレクト：**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// これでエラーメッセージがr.outputに含まれる
```

### 2. ストリーミングなし

コマンドの完了を待つ必要があります：

```hemlock
let r = exec("long_running_command");
// コマンドが終了するまでブロック
// 出力を段階的に処理できない
```

### 3. タイムアウトなし

コマンドは無期限に実行できます：

```hemlock
let r = exec("sleep 1000");
// 1000秒間ブロック
// タイムアウトやキャンセルの方法がない
```

**回避策 - timeoutコマンドを使用：**
```hemlock
let r = exec("timeout 5 long_command");
// 5秒後にタイムアウト
```

### 4. シグナル処理なし

実行中のコマンドにシグナルを送信できません：

```hemlock
let r = exec("long_command");
// コマンドにSIGINT、SIGTERMなどを送信できない
```

### 5. プロセス制御なし

開始後のコマンドとやり取りできません：

```hemlock
let r = exec("interactive_program");
// プログラムに入力を送信できない
// 実行を制御できない
```

## 使用ケース

### 適した使用ケース

**1. システムユーティリティの実行：**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Unixツールでのクイックデータ処理：**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Unique lines: " + r.output);
```

**3. システム状態の確認：**
```hemlock
let r = exec("df -h");
print("Disk usage:\n" + r.output);
```

**4. ファイル存在チェック：**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
}
```

**5. レポートの生成：**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Running instances: " + count);
```

**6. 自動化スクリプト：**
```hemlock
exec("git add .");
exec("git commit -m 'Auto commit'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push failed");
}
```

### 推奨されない使用

**1. 長時間実行のサービス：**
```hemlock
// 悪い例
let r = exec("nginx");  // 永遠にブロック
```

**2. 対話型コマンド：**
```hemlock
// 悪い例 - 入力を提供できない
let r = exec("ssh user@host");
```

**3. 巨大な出力を生成するコマンド：**
```hemlock
// 悪い例 - 出力全体をメモリにロード
let r = exec("cat 10GB_file.log");
```

**4. リアルタイムストリーミング：**
```hemlock
// 悪い例 - 出力を段階的に処理できない
let r = exec("tail -f /var/log/app.log");
```

**5. ミッションクリティカルなエラー処理：**
```hemlock
// 悪い例 - stderrがキャプチャされない
let r = exec("critical_operation");
// 詳細なエラーメッセージを見ることができない
```

## ベストプラクティス

### 1. 常に終了コードを確認

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Command failed!");
    // エラーを処理
}
```

### 2. 必要に応じて出力をトリム

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // 末尾の改行を削除
print(clean);  // "test"（改行なし）
```

### 3. 実行前に検証

```hemlock
fn is_valid_command(cmd: string): bool {
    // コマンドが安全かどうかを検証
    return true;  // 検証ロジック
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. 重要な操作にはtry/catchを使用

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Command failed";
    }
} catch (e) {
    print("Error: " + e);
    // クリーンアップまたはリカバリ
}
```

### 5. exec()よりHemlockのAPIを優先

```hemlock
// 悪い例 - ファイル操作にexecを使用
let r = exec("cat file.txt");

// 良い例 - HemlockのFile APIを使用
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. 必要に応じてstderrをキャプチャ

```hemlock
// stderrをstdoutにリダイレクト
let r = exec("command 2>&1");
// これでr.outputにstdoutとstderrの両方が含まれる
```

### 7. シェル機能を賢く使用

```hemlock
// 効率のためにパイプを使用
let r = exec("cat large.txt | grep pattern | head -n 10");

// コマンド置換を使用
let r = exec("echo Current user: $(whoami)");

// 条件付き実行を使用
let r = exec("test -f file.txt && cat file.txt");
```

## 完全な例

### 例1：システム情報収集

```hemlock
fn get_system_info() {
    print("=== System Information ===");

    // ホスト名
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // アップタイム
    let r2 = exec("uptime");
    print("Uptime: " + r2.output.trim());

    // ディスク使用量
    let r3 = exec("df -h /");
    print("\nDisk Usage:");
    print(r3.output);

    // メモリ使用量
    let r4 = exec("free -h");
    print("Memory Usage:");
    print(r4.output);
}

get_system_info();
```

### 例2：ログ分析

```hemlock
fn analyze_log(logfile: string) {
    print("Analyzing log: " + logfile);

    // 総行数をカウント
    let r1 = exec("wc -l " + logfile);
    print("Total lines: " + r1.output.trim());

    // エラーをカウント
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Errors: " + errors);
    } else {
        print("Errors: 0");
    }

    // 警告をカウント
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Warnings: " + warnings);
    } else {
        print("Warnings: 0");
    }

    // 最近のエラー
    print("\nRecent errors:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Usage: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### 例3：Gitヘルパー

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Error: Not a git repository");
        return;
    }

    if (r.output == "") {
        print("Working directory clean");
    } else {
        print("Changes:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Adding all changes...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Error adding files");
        return;
    }

    print("Committing...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Error committing");
        return;
    }

    print("Committed successfully");
    print(r2.output);
}

// 使用方法
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### 例4：バックアップスクリプト

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Backing up " + source + " to " + dest);

    // バックアップディレクトリを作成
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Error creating backup directory");
        return false;
    }

    // タイムスタンプ付きのtarballを作成
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Creating archive: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Error creating backup:");
        print(r3.output);
        return false;
    }

    print("Backup completed successfully");

    // バックアップサイズを表示
    let r4 = exec("du -h " + backup_file);
    print("Backup size: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Usage: " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## まとめ

Hemlockの`exec()`関数は以下を提供します：

- シンプルなシェルコマンド実行
- 出力キャプチャ（stdout）
- 終了コードチェック
- 完全なシェル機能アクセス（パイプ、リダイレクトなど）
- システムユーティリティとの統合

覚えておくべきこと：
- 常に終了コードを確認
- セキュリティの影響（シェルインジェクション）に注意
- コマンドで使用する前にユーザー入力を検証
- 利用可能な場合はexec()よりHemlockのAPIを優先
- stderrはキャプチャされない（リダイレクトには`2>&1`を使用）
- コマンドは完了するまでブロック
- 長時間実行のサービスではなく、短時間ユーティリティに使用

**セキュリティチェックリスト：**
- サニタイズされていないユーザー入力を使用しない
- すべての入力を検証
- コマンドに許可リストを使用
- 必要に応じて特殊文字をエスケープ
- 最小権限で実行
- シェルコマンドよりHemlockのAPIを優先
