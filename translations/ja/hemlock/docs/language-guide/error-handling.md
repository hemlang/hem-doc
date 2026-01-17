# エラーハンドリング

Hemlockは`try`、`catch`、`finally`、`throw`、`panic`による例外ベースのエラーハンドリングをサポートしています。このガイドでは、例外による回復可能なエラーとpanicによる回復不可能なエラーについて説明します。

## 概要

```hemlock
// 基本的なエラーハンドリング
try {
    risky_operation();
} catch (e) {
    print("Error: " + e);
}

// クリーンアップ付き
try {
    process_file();
} catch (e) {
    print("Failed: " + e);
} finally {
    cleanup();
}

// エラーのスロー
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### 構文

**基本的なtry/catch：**
```hemlock
try {
    // 危険なコード
} catch (e) {
    // エラーを処理、eはスローされた値を含む
}
```

**Try/finally：**
```hemlock
try {
    // 危険なコード
} finally {
    // 例外がスローされても常に実行
}
```

**Try/catch/finally：**
```hemlock
try {
    // 危険なコード
} catch (e) {
    // エラーを処理
} finally {
    // クリーンアップコード
}
```

### Tryブロック

tryブロックは文を順次実行します：

```hemlock
try {
    print("Starting...");
    risky_operation();
    print("Success!");  // 例外がなければ実行
}
```

**動作：**
- 文を順番に実行
- 例外がスローされた場合：`catch`または`finally`にジャンプ
- 例外がない場合：`finally`（存在すれば）を実行して続行

### Catchブロック

catchブロックはスローされた値を受け取ります：

```hemlock
try {
    throw "oops";
} catch (error) {
    print("Caught: " + error);  // error = "oops"
    // errorはここでのみアクセス可能
}
// errorはここではアクセスできない
```

**Catchパラメータ：**
- スローされた値（任意の型）を受け取る
- catchブロックにスコープされる
- 任意の名前を付けられる（慣例として`e`、`err`、または`error`）

**catchでできること：**
```hemlock
try {
    risky_operation();
} catch (e) {
    // エラーをログ
    print("Error: " + e);

    // 同じエラーを再スロー
    throw e;

    // 別のエラーをスロー
    throw "different error";

    // デフォルト値を返す
    return null;

    // 処理して続行
    // （再スローなし）
}
```

### Finallyブロック

finallyブロックは**常に実行されます**：

```hemlock
try {
    print("1: try");
    throw "error";
} catch (e) {
    print("2: catch");
} finally {
    print("3: finally");  // 常に実行
}
print("4: after");

// 出力：1: try, 2: catch, 3: finally, 4: after
```

**finallyが実行されるタイミング：**
- tryブロックの後（例外がない場合）
- catchブロックの後（例外がキャッチされた場合）
- try/catchに`return`、`break`、または`continue`が含まれていても
- 制御フローがtry/catchを抜ける前

**returnとfinally：**
```hemlock
fn example() {
    try {
        return 1;  // finallyの実行後に1を返す
    } finally {
        print("cleanup");  // 戻る前に実行
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // finallyのreturnが上書き - 2を返す
    }
}
```

**制御フローとfinally：**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // finallyの実行後にbreak
        }
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

## Throw文

### 基本的なThrow

任意の値を例外としてスロー：

```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
throw ["error", "details"];
```

**実行：**
1. 式を評価
2. 最も近い囲んでいる`catch`に即座にジャンプ
3. `catch`がない場合、コールスタックを伝播

### エラーのスロー

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "Age cannot be negative";
    }
    if (age > 150) {
        throw "Age is unrealistic";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Validation error: " + e);
}
```

### エラーオブジェクトのスロー

構造化されたエラー情報を作成：

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "File does not exist"
        };
    }
    // ... ファイルを読み込み
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("File not found: " + e.path);
    }
}
```

### 再スロー

エラーをキャッチして再スロー：

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Logging error: " + e);
        throw e;  // 呼び出し元に再スロー
    }
}

try {
    wrapper();
} catch (e) {
    print("Caught in main: " + e);
}
```

## キャッチされない例外

例外がキャッチされずにコールスタックの最上部に伝播した場合：

```hemlock
fn foo() {
    throw "uncaught!";
}

foo();  // クラッシュ：Runtime error: uncaught!
```

**動作：**
- プログラムがクラッシュ
- stderrにエラーメッセージを出力
- 非ゼロのステータスコードで終了
- スタックトレースは将来のバージョンで追加予定

## Panic - 回復不可能なエラー

### Panicとは？

`panic()`はプログラムを即座に終了させるべき**回復不可能なエラー**用です：

```hemlock
panic();                    // デフォルトメッセージ："panic!"
panic("custom message");    // カスタムメッセージ
panic(42);                  // 非文字列値も出力される
```

**セマンティクス：**
- 終了コード1でプログラムを**即座に終了**
- stderrにエラーメッセージを出力：`panic: <message>`
- try/catchで**キャッチ不可能**
- バグや回復不可能なエラーに使用

### Panic vs Throw

```hemlock
// throw - 回復可能なエラー（キャッチ可能）
try {
    throw "recoverable error";
} catch (e) {
    print("Caught: " + e);  // 正常にキャッチ
}

// panic - 回復不可能なエラー（キャッチ不可能）
try {
    panic("unrecoverable error");  // プログラムは即座に終了
} catch (e) {
    print("This never runs");       // 実行されない
}
```

### Panicを使用するタイミング

**panicを使用する場面：**
- **バグ**：到達不可能なコードに到達した
- **無効な状態**：データ構造の破損が検出された
- **回復不可能なエラー**：重要なリソースが利用不可能
- **アサーション失敗**：`assert()`では不十分な場合

**例：**
```hemlock
// 到達不可能なコード
fn process_state(state: i32) {
    if (state == 1) {
        return "ready";
    } else if (state == 2) {
        return "running";
    } else if (state == 3) {
        return "stopped";
    } else {
        panic("invalid state: " + typeof(state));  // 発生してはならない
    }
}

// 重要なリソースのチェック
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json not found - cannot start");
    }
    // ...
}

// データ構造の不変条件
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() called on empty stack");
    }
    return stack.pop();
}
```

### Panicを使用しないタイミング

**代わりにthrowを使用する場面：**
- ユーザー入力の検証
- ファイルが見つからない
- ネットワークエラー
- 予期されるエラー条件

```hemlock
// 悪い：予期されるエラーにpanic
fn divide(a, b) {
    if (b == 0) {
        panic("division by zero");  // 厳しすぎる
    }
    return a / b;
}

// 良い：予期されるエラーにthrow
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";  // 回復可能
    }
    return a / b;
}
```

## 制御フローとの相互作用

### Try/Catch/Finally内のReturn

```hemlock
fn example() {
    try {
        return 1;  // finallyの実行後に1を返す
    } finally {
        print("cleanup");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // finallyのreturnがtryのreturnを上書き - 2を返す
    }
}
```

**ルール：** finallyブロックの戻り値はtry/catchの戻り値を上書きします。

### Try/Catch/Finally内のBreak/Continue

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // finallyの実行後にbreak
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

**ルール：** Break/continueはfinallyブロックの後に実行されます。

### ネストされたTry/Catch

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Caught: " + e);  // 出力：Caught: inner
        throw "outer";  // 別のエラーを再スロー
    }
} catch (e) {
    print("Caught: " + e);  // 出力：Caught: outer
}
```

**ルール：** ネストされたtry/catchブロックは期待通りに動作し、内側のcatchが先に発生します。

## よくあるパターン

### パターン：リソースクリーンアップ

クリーンアップには常に`finally`を使用：

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Error processing file: " + e);
    } finally {
        if (file != null) {
            file.close();  // エラー時も常にクローズ
        }
    }
}
```

### パターン：エラーラッピング

低レベルのエラーにコンテキストを追加：

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Failed to load config from " + path + ": " + e;
    }
}
```

### パターン：エラーリカバリ

エラー時にフォールバックを提供：

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "division by zero";
        }
        return a / b;
    } catch (e) {
        print("Error: " + e);
        return null;  // フォールバック値
    }
}
```

### パターン：バリデーション

バリデーションに例外を使用：

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Name is required";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Invalid age";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Invalid email";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "invalid" });
} catch (e) {
    print("Validation failed: " + e);
}
```

### パターン：複数のエラータイプ

エラーオブジェクトを使用してエラータイプを区別：

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Data is null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Expected array" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Array is empty" };
    }

    // ... 処理
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("No data provided");
    } else if (e.type == "TypeError") {
        print("Wrong data type: " + e.message);
    } else {
        print("Error: " + e.message);
    }
}
```

## ベストプラクティス

1. **例外は例外的なケースに使用** - 通常の制御フローには使用しない
2. **意味のあるエラーをスロー** - コンテキストを含む文字列またはオブジェクト
3. **クリーンアップには常にfinallyを使用** - リソースの解放を確実に
4. **キャッチして無視しない** - 少なくともエラーをログ
5. **適切に再スロー** - 処理できない場合は呼び出し元に処理させる
6. **バグにはpanicを使用** - 回復不可能なエラーにはpanicを使用
7. **例外をドキュメント化** - 関数がスローできるものを明確に

## よくある落とし穴

### 落とし穴：エラーを飲み込む

```hemlock
// 悪い：サイレントな失敗
try {
    risky_operation();
} catch (e) {
    // エラーを無視 - サイレントな失敗
}

// 良い：ログまたは処理
try {
    risky_operation();
} catch (e) {
    print("Operation failed: " + e);
    // 適切に処理
}
```

### 落とし穴：Finallyのオーバーライド

```hemlock
// 悪い：finallyがreturnを上書き
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // 42ではなく0を返す！
    }
}

// 良い：finallyでreturnしない
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // クリーンアップのみ、returnなし
    }
}
```

### 落とし穴：クリーンアップ忘れ

```hemlock
// 悪い：エラー時にファイルがクローズされないかも
fn process() {
    let file = open("data.txt");
    let content = file.read();  // スローするかも
    file.close();  // エラー時は到達しない
}

// 良い：finallyを使用
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### 落とし穴：予期されるエラーにPanicを使用

```hemlock
// 悪い：予期されるエラーにpanic
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Config file not found");  // 厳しすぎる
    }
    return read_file(path);
}

// 良い：予期されるエラーにthrow
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Config file not found: " + path;  // 回復可能
    }
    return read_file(path);
}
```

## 例

### 例：基本的なエラーハンドリング

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Error: " + e);  // 出力：Error: division by zero
}
```

### 例：リソース管理

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("File copied successfully");
    } catch (e) {
        print("Failed to copy file: " + e);
        throw e;  // 再スロー
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### 例：ネストされたエラーハンドリング

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Failed to process user: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Processed: " + typeof(success_count) + " success, " + typeof(error_count) + " errors");
}
```

### 例：カスタムエラータイプ

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a must be a number", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b must be a number", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Cannot divide by zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### 例：リトライロジック

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // 成功！
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation failed after " + typeof(max_attempts) + " attempts: " + e;
            }
            print("Attempt " + typeof(attempt) + " failed, retrying...");
        }
    }
}

fn unreliable_operation() {
    // シミュレートされた不安定な操作
    if (random() < 0.7) {
        throw "Operation failed";
    }
    return "Success";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("All retries failed: " + e);
}
```

## 実行順序

実行順序の理解：

```hemlock
try {
    print("1: try block start");
    throw "error";
    print("2: never reached");
} catch (e) {
    print("3: catch block");
} finally {
    print("4: finally block");
}
print("5: after try/catch/finally");

// 出力：
// 1: try block start
// 3: catch block
// 4: finally block
// 5: after try/catch/finally
```

## 現在の制限事項

- **スタックトレースなし** - キャッチされない例外はスタックトレースを表示しない（計画中）
- **一部の組み込み関数がexit** - 一部の組み込み関数はスローではなく`exit()`する（レビュー予定）
- **カスタム例外タイプなし** - 任意の値をスローできるが、正式な例外階層はない

## 関連トピック

- [関数](functions.md) - 例外と関数のreturn
- [制御フロー](control-flow.md) - 例外が制御フローに与える影響
- [メモリ](memory.md) - メモリクリーンアップにfinallyを使用

## 参照

- **例外のセマンティクス**：CLAUDE.mdの「Error Handling」セクションを参照
- **Panic vs Throw**：異なるエラータイプに対する異なる使用例
- **Finally保証**：return/break/continueがあっても常に実行
