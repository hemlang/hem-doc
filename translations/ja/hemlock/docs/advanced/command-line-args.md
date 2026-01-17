# Hemlockでのコマンドライン引数

Hemlockプログラムは、プログラム起動時に自動的に設定される組み込みの**`args`配列**を通じてコマンドライン引数にアクセスできます。

## 目次

- [概要](#概要)
- [args配列](#args配列)
- [プロパティ](#プロパティ)
- [反復パターン](#反復パターン)
- [一般的な使用ケース](#一般的な使用ケース)
- [引数解析パターン](#引数解析パターン)
- [ベストプラクティス](#ベストプラクティス)
- [完全な例](#完全な例)

## 概要

`args`配列は、Hemlockプログラムに渡されたコマンドライン引数へのアクセスを提供します：

- **常に利用可能** - すべてのHemlockプログラムで組み込みのグローバル変数
- **スクリプト名を含む** - `args[0]`は常にスクリプトのパス/名前を含む
- **文字列の配列** - すべての引数は文字列
- **ゼロインデックス** - 標準的な配列インデックス（0, 1, 2, ...）

## args配列

### 基本構造

```hemlock
// args[0]は常にスクリプトのファイル名
// args[1]からargs[n-1]が実際の引数
print(args[0]);        // "script.hml"
print(args.length);    // 引数の総数（スクリプト名を含む）
```

### 使用例

**コマンド：**
```bash
./hemlock script.hml hello world "test 123"
```

**script.hml内：**
```hemlock
print("Script name: " + args[0]);     // "script.hml"
print("Total args: " + typeof(args.length));  // "4"
print("First arg: " + args[1]);       // "hello"
print("Second arg: " + args[2]);      // "world"
print("Third arg: " + args[3]);       // "test 123"
```

### インデックスリファレンス

| インデックス | 内容 | 例の値 |
|-------|----------|---------------|
| `args[0]` | スクリプトパス/名前 | `"script.hml"`または`"./script.hml"` |
| `args[1]` | 最初の引数 | `"hello"` |
| `args[2]` | 2番目の引数 | `"world"` |
| `args[3]` | 3番目の引数 | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | 最後の引数 | （可変） |

## プロパティ

### 常に存在

`args`は**すべての**Hemlockプログラムで利用可能なグローバル配列です：

```hemlock
// 宣言やインポートは不要
print(args.length);  // すぐに動作
```

### スクリプト名を含む

`args[0]`は常にスクリプトのパス/名前を含みます：

```hemlock
print("Running: " + args[0]);
```

**args[0]の可能な値：**
- `"script.hml"` - ファイル名のみ
- `"./script.hml"` - 相対パス
- `"/home/user/script.hml"` - 絶対パス
- スクリプトの呼び出し方法に依存

### 型：文字列の配列

すべての引数は文字列として格納されます：

```hemlock
// 引数: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42"（文字列、数値ではない）
print(args[2]);  // "3.14"（文字列、数値ではない）
print(args[3]);  // "true"（文字列、ブール値ではない）

// 必要に応じて変換：
let num = 42;  // 必要に応じて手動でパース
```

### 最小長

常に少なくとも1（スクリプト名）：

```hemlock
print(args.length);  // 最小：1
```

**引数なしでも：**
```bash
./hemlock script.hml
```

```hemlock
// script.hml内:
print(args.length);  // 1（スクリプト名のみ）
```

### REPLの動作

REPLでは、`args.length`は0（空配列）です：

```hemlock
# REPLセッション
> print(args.length);
0
```

## 反復パターン

### 基本的な反復

`args[0]`（スクリプト名）をスキップして実際の引数を処理：

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**出力（`./hemlock script.hml foo bar baz`の場合）**
```
Argument 1: foo
Argument 2: bar
Argument 3: baz
```

### For-In反復（スクリプト名を含む）

```hemlock
for (let arg in args) {
    print(arg);
}
```

**出力：**
```
script.hml
foo
bar
baz
```

### 引数数のチェック

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <argument>");
    // exitまたはreturn
} else {
    let arg = args[1];
    // argを処理
}
```

### スクリプト名以外のすべての引数を処理

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Processing: " + arg);
}
```

## 一般的な使用ケース

### 1. シンプルな引数処理

必須引数のチェック：

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Processing file: " + filename);
    // ...ファイルを処理
}
```

**使用方法：**
```bash
./hemlock script.hml data.txt
# 出力: Processing file: data.txt
```

### 2. 複数引数

```hemlock
if (args.length < 3) {
    print("Usage: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Input: " + input_file);
    print("Output: " + output_file);

    // ファイルを処理...
}
```

**使用方法：**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. 可変数の引数

提供されたすべての引数を処理：

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**使用方法：**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. ヘルプメッセージ

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show this help message");
    print("  -v, --verbose  Enable verbose output");
} else {
    // 通常処理
}
```

### 5. 引数の検証

```hemlock
fn validate_file(filename: string): bool {
    // ファイルが存在するかチェック（例）
    return filename != "";
}

if (args.length < 2) {
    print("Error: No filename provided");
} else if (!validate_file(args[1])) {
    print("Error: Invalid file: " + args[1]);
} else {
    print("Processing: " + args[1]);
}
```

## 引数解析パターン

### 名前付き引数（フラグ）

名前付き引数のシンプルなパターン：

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Verbose mode enabled");
}
print("Input: " + input_file);
print("Output: " + output_file);
```

**使用方法：**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### ブールフラグ

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### 値引数

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // 文字列をintにパースする必要がある
        }
    }
    i = i + 1;
}
```

### 位置引数と名前付き引数の混合

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // 位置引数として扱う
        positional.push(args[i]);
    }
    i = i + 1;
}

// 位置引数を割り当て
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### 引数パーサーヘルパー関数

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // 位置引数
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose: " + typeof(opts.verbose));
print("Output: " + opts.output);
print("Files: " + typeof(opts.files.length));
```

## ベストプラクティス

### 1. 常に引数数をチェック

```hemlock
// 良い例
if (args.length < 2) {
    print("Usage: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// 悪い例 - 引数がない場合にクラッシュする可能性
process_file(args[1]);  // args.length == 1の場合エラー
```

### 2. 使用方法情報を提供

```hemlock
fn show_usage() {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show help");
    print("  -v, --verbose  Verbose output");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. 引数を検証

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Error: Missing required argument");
        return false;
    }

    if (args[1] == "") {
        print("Error: Empty argument");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // exitまたはusageを表示
}
```

### 4. 説明的な変数名を使用

```hemlock
// 良い例
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// 悪い例
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. スペースを含むクォート引数を処理

シェルがこれを自動的に処理します：

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. 引数オブジェクトを作成

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Input: " + arguments.input);
```

## 完全な例

### 例1：ファイルプロセッサ

```hemlock
// 使用方法: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Usage: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Processing " + input + " -> " + output);

    // ファイルを処理
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // 処理の例
        f_out.write(processed);

        print("Done!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### 例2：バッチファイルプロセッサ

```hemlock
// 使用方法: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Processing: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // コンテンツを処理...
            print("    " + typeof(content.length) + " bytes");
        } catch (e) {
            print("    Error: " + e);
        }

        i = i + 1;
    }

    print("Done!");
}
```

### 例3：高度な引数パーサー

```hemlock
// 使用方法: ./hemlock app.hml [OPTIONS] <files...>
// オプション:
//   --verbose, -v     詳細出力を有効化
//   --output, -o FILE 出力ファイルを設定
//   --help, -h        ヘルプを表示

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Error: --output requires a value");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Error: Unknown option: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Usage: " + args[0] + " [OPTIONS] <files...>");
    print("Options:");
    print("  --verbose, -v     Enable verbose output");
    print("  --output, -o FILE Set output file");
    print("  --help, -h        Show this help");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Error: No input files specified");
    show_help();
} else {
    if (config.verbose) {
        print("Verbose mode enabled");
        print("Output file: " + config.output);
        print("Input files: " + typeof(config.files.length));
    }

    // ファイルを処理
    for (let file in config.files) {
        if (config.verbose) {
            print("Processing: " + file);
        }
        // ...ファイルを処理
    }
}
```

### 例4：設定ツール

```hemlock
// 使用方法: ./hemlock config.hml <action> [arguments]
// アクション:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Usage: " + args[0] + " <action> [arguments]");
    print("Actions:");
    print("  get <key>         Get configuration value");
    print("  set <key> <value> Set configuration value");
    print("  list              List all configuration");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Error: 'get' requires a key");
        } else {
            let key = args[2];
            print("Getting: " + key);
            // ...設定から取得
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Error: 'set' requires key and value");
        } else {
            let key = args[2];
            let value = args[3];
            print("Setting " + key + " = " + value);
            // ...設定に設定
        }
    } else if (action == "list") {
        print("Listing all configuration:");
        // ...設定をリスト
    } else {
        print("Error: Unknown action: " + action);
        show_usage();
    }
}
```

## まとめ

Hemlockのコマンドライン引数サポートは以下を提供します：

- グローバルに利用可能な組み込み`args`配列
- 引数へのシンプルな配列ベースのアクセス
- `args[0]`にスクリプト名
- すべての引数は文字列
- 配列メソッドが利用可能（.length, .sliceなど）

覚えておくべきこと：
- 要素にアクセスする前に常に`args.length`をチェック
- `args[0]`はスクリプト名
- 実際の引数は`args[1]`から開始
- すべての引数は文字列 - 必要に応じて変換
- ユーザーフレンドリーなツールのために使用方法情報を提供
- 処理前に引数を検証

一般的なパターン：
- シンプルな位置引数
- 名前付き/フラグ引数（--flag）
- 値引数（--option value）
- ヘルプメッセージ（--help）
- 引数検証
