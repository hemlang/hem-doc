# Hemlockへの貢献

Hemlockへの貢献にご興味をお持ちいただき、ありがとうございます！このガイドでは、言語の設計哲学とコード品質を維持しながら効果的に貢献する方法を説明します。

---

## 目次

- [始める前に](#始める前に)
- [貢献ワークフロー](#貢献ワークフロー)
- [コードスタイルガイドライン](#コードスタイルガイドライン)
- [貢献すべきもの](#貢献すべきもの)
- [貢献すべきでないもの](#貢献すべきでないもの)
- [共通パターン](#共通パターン)
- [新機能の追加](#新機能の追加)
- [コードレビュープロセス](#コードレビュープロセス)

---

## 始める前に

### 必読ドキュメント

貢献する前に、以下のドキュメントを順番にお読みください:

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Hemlockの核となる原則を理解する
2. **`/home/user/hemlock/docs/design/implementation.md`** - コードベースの構造を学ぶ
3. **`/home/user/hemlock/docs/contributing/testing.md`** - テスト要件を理解する
4. **このドキュメント** - 貢献ガイドラインを学ぶ

### 前提条件

**必要な知識:**
- Cプログラミング（ポインタ、メモリ管理、構造体）
- コンパイラ/インタプリタの基礎（字句解析、構文解析、AST）
- GitとGitHubワークフロー
- Unix/Linuxコマンドライン

**必要なツール:**
- GCCまたはClangコンパイラ
- Makeビルドシステム
- Gitバージョン管理
- Valgrind（メモリリーク検出用）
- 基本的なテキストエディタまたはIDE

### コミュニケーションチャネル

**質問する場所:**
- GitHub Issues - バグ報告と機能リクエスト
- GitHub Discussions - 一般的な質問と設計の議論
- Pull Requestコメント - 具体的なコードフィードバック

---

## 貢献ワークフロー

### 1. Issueを見つけるか作成する

**コードを書く前に:**
- あなたの貢献に関するIssueが存在するか確認
- なければ、何をしたいか説明するIssueを作成
- 大きな変更を始める前にメンテナーのフィードバックを待つ
- 小さなバグ修正はこのステップをスキップ可能

**良いIssue説明には以下を含む:**
- 問題の説明（何が壊れているか、何が欠けているか）
- 提案する解決策（どのように修正するか）
- 例（問題を示すコードスニペット）
- 根拠（この変更がHemlockの哲学に沿う理由）

### 2. フォークとクローン

```bash
# まずGitHub上でリポジトリをフォークし、その後:
git clone https://github.com/YOUR_USERNAME/hemlock.git
cd hemlock
git checkout -b feature/your-feature-name
```

### 3. 変更を行う

以下のガイドラインに従ってください:
- 最初にテストを書く（TDDアプローチ）
- 機能を実装する
- すべてのテストが合格することを確認
- メモリリークをチェック
- ドキュメントを更新

### 4. 変更をテストする

```bash
# 完全なテストスイートを実行
make test

# 特定のテストカテゴリを実行
./tests/run_tests.sh tests/category/

# メモリリークをチェック
valgrind ./hemlock tests/your_test.hml

# ビルドとテスト
make clean && make && make test
```

### 5. 変更をコミットする

**良いコミットメッセージ:**
```
整数型にビット演算子を追加

- &, |, ^, <<, >>, ~ 演算子を実装
- 整数のみの演算を保証する型チェックを追加
- 演算子優先順位テーブルを更新
- すべての演算子に対する包括的なテストを追加

Closes #42
```

**コミットメッセージの形式:**
- 1行目: 簡潔な要約（最大50文字）
- 空行
- 詳細な説明（72文字で折り返し）
- Issue番号を参照

### 6. Pull Requestを提出する

**提出前に:**
- 最新のmainブランチにリベース
- すべてのテストが合格することを確認
- valgrindを実行してリークをチェック
- ユーザー向け機能を追加する場合はCLAUDE.mdを更新

**Pull Request説明には以下を含める:**
- これが解決する問題
- どのように解決するか
- 破壊的変更（ある場合）
- 新しい構文や動作の例
- テストカバレッジの要約

---

## コードスタイルガイドライン

### Cコードスタイル

**フォーマット:**
```c
// 4スペースでインデント（タブなし）
// 関数はK&R括弧スタイル
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // 制御構造では同じ行に括弧
        do_something();
    }
}

// 行の長さ: 最大100文字
// 演算子の周りにスペース
int result = (a + b) * c;

// ポインタのアスタリスクは型と一緒
char *string;   // 良い
char* string;   // 避ける
char * string;  // 避ける
```

**命名規則:**
```c
// 関数: lowercase_with_underscores
void eval_expression(ASTNode *node);

// 型: PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// 定数: UPPERCASE_WITH_UNDERSCORES
#define MAX_BUFFER_SIZE 4096

// 変数: lowercase_with_underscores
int item_count;
Value *current_value;

// 列挙型: TYPE_PREFIX_NAME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**コメント:**
```c
// 簡潔な説明には単一行コメント
// 適切な大文字で完全な文を使用

/*
 * 長い説明には複数行コメント
 * 読みやすさのためにアスタリスクを揃える
 */

/**
 * 関数のドキュメントコメント
 * @param node - 評価するASTノード
 * @return 評価された値
 */
Value eval_expr(ASTNode *node);
```

**エラー処理:**
```c
// すべてのmalloc呼び出しをチェック
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Error: Out of memory\n");
    exit(1);
}

// エラーメッセージにコンテキストを提供
if (file == NULL) {
    fprintf(stderr, "Error: Failed to open '%s': %s\n",
            filename, strerror(errno));
    exit(1);
}

// 意味のあるエラーメッセージを使用
// 悪い: "Error: Invalid value"
// 良い: "Error: Expected integer, got string"
```

**メモリ管理:**
```c
// 割り当てたものは常に解放
Value *val = value_create_i32(42);
// ... valを使用
value_free(val);

// 解放後にポインタをNULLに設定（ダブルフリー防止）
free(ptr);
ptr = NULL;

// コメントで所有権をドキュメント化
// この関数は 'value' の所有権を取得し、解放します
void store_value(Value *value);

// この関数は所有権を取得しません（呼び出し側が解放）
Value *get_value(void);
```

### コード構成

**ファイル構造:**
```c
// 1. インクルード（システムヘッダーが先、次にローカル）
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. 定数とマクロ
#define INITIAL_CAPACITY 16

// 3. 型定義
typedef struct Foo Foo;

// 4. 静的関数宣言（内部ヘルパー）
static void helper_function(void);

// 5. パブリック関数の実装
void public_api_function(void)
{
    // 実装
}

// 6. 静的関数の実装
static void helper_function(void)
{
    // 実装
}
```

**ヘッダーファイル:**
```c
// ヘッダーガードを使用
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// 前方宣言
typedef struct Value Value;

// ヘッダーにはパブリックAPIのみ
void public_function(Value *val);

// パラメータと戻り値をドキュメント化
/**
 * 式ASTノードを評価する
 * @param node - 評価するASTノード
 * @param env - 現在の環境
 * @return 結果値
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## 貢献すべきもの

### ✅ 推奨される貢献

**バグ修正:**
- メモリリーク
- セグメンテーションフォルト
- 不正確な動作
- エラーメッセージの改善

**ドキュメント:**
- コードコメント
- APIドキュメント
- ユーザーガイドとチュートリアル
- サンプルプログラム
- テストケースドキュメント

**テスト:**
- 既存機能の追加テストケース
- エッジケースカバレッジ
- 修正されたバグの回帰テスト
- パフォーマンスベンチマーク

**小規模な機能追加:**
- 新しい組み込み関数（哲学に合う場合）
- 文字列/配列メソッド
- ユーティリティ関数
- エラー処理の改善

**パフォーマンス改善:**
- より高速なアルゴリズム（セマンティクスを変更せずに）
- メモリ使用量の削減
- ベンチマークスイート
- プロファイリングツール

**ツーリング:**
- エディタの構文ハイライト
- 言語サーバープロトコル（LSP）
- デバッガ統合
- ビルドシステムの改善

### 🤔 まず議論すること

**主要な機能:**
- 新しい言語構文
- 型システムの変更
- 構文の追加
- 並行処理プリミティブ

**議論の方法:**
1. GitHub IssueまたはDiscussionを開く
2. 機能と根拠を説明
3. サンプルコードを示す
4. Hemlockの哲学にどう合うか説明
5. メンテナーのフィードバックを待つ
6. 実装前に設計を反復

---

## 貢献すべきでないもの

### ❌ 推奨されない貢献

**以下のような機能を追加しない:**
- ユーザーから複雑さを隠す
- 動作を暗黙的または魔法的にする
- 既存のセマンティクスや構文を壊す
- ガベージコレクションや自動メモリ管理を追加
- 「暗黙より明示」の原則に違反

**却下される貢献の例:**

**1. 自動セミコロン挿入**
```hemlock
// 悪い: これは却下されます
let x = 5  // セミコロンなし
let y = 10 // セミコロンなし
```
理由: 構文を曖昧にし、エラーを隠す

**2. RAII/デストラクタ**
```hemlock
// 悪い: これは却下されます
let f = open("file.txt");
// スコープ終了時にファイルが自動的にクローズ
```
理由: リソースがいつ解放されるか隠す、明示的ではない

**3. データを失う暗黙の型強制**
```hemlock
// 悪い: これは却下されます
let x: i32 = 3.14;  // 黙って3に切り捨て
```
理由: データ損失は暗黙ではなく明示的であるべき

**4. ガベージコレクション**
```c
// 悪い: これは却下されます
void *gc_malloc(size_t size) {
    // 自動クリーンアップのために割り当てを追跡
}
```
理由: メモリ管理を隠す、予測不可能なパフォーマンス

**5. 複雑なマクロシステム**
```hemlock
// 悪い: これは却下されます
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
理由: 魔法が多すぎ、コードの推論が難しくなる

### 一般的な却下理由

**「これは暗黙的すぎる」**
- 解決策: 動作を明示的にしてドキュメント化

**「これは複雑さを隠す」**
- 解決策: 複雑さを露出させつつ人間工学的にする

**「これは既存のコードを壊す」**
- 解決策: 破壊的でない代替案を見つけるか、バージョニングを議論

**「これはHemlockの哲学に合わない」**
- 解決策: philosophy.mdを再読し、アプローチを再検討

---

## 共通パターン

### エラー処理パターン

```c
// Hemlockコードでの回復可能なエラーにはこのパターンを使用
Value *divide(Value *a, Value *b)
{
    // 前提条件をチェック
    if (b->type != TYPE_I32) {
        // エラー値を返すか例外をスロー
        return create_error("Expected integer divisor");
    }

    if (b->i32_value == 0) {
        return create_error("Division by zero");
    }

    // 操作を実行
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### メモリ管理パターン

```c
// パターン: 割り当て、使用、解放
void process_data(void)
{
    // 割り当て
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // 使用
    if (buf && str) {
        // ... 作業を行う
    }

    // 解放（割り当ての逆順で）
    free(str);
    free_buffer(buf);
}
```

### 値作成パターン

```c
// コンストラクタを使用して値を作成
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### 型チェックパターン

```c
// 操作前に型をチェック
Value *add_values(Value *a, Value *b)
{
    // 型チェック
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Type mismatch");
    }

    // 安全に進行
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### 文字列構築パターン

```c
// 効率的に文字列を構築
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Error: %s (line %d)", detail, line_number);
}
```

---

## 新機能の追加

### 機能追加チェックリスト

新機能を追加する際は、以下のステップに従ってください:

#### 1. 設計フェーズ

- [ ] philosophy.mdを読んで整合性を確認
- [ ] 機能を説明するGitHub Issueを作成
- [ ] 設計のメンテナー承認を取得
- [ ] 仕様を書く（構文、セマンティクス、例）
- [ ] エッジケースとエラー条件を検討

#### 2. 実装フェーズ

**言語構文を追加する場合:**

- [ ] `lexer.h`にトークン型を追加（必要に応じて）
- [ ] `lexer.c`にレキサールールを追加（必要に応じて）
- [ ] `ast.h`にASTノード型を追加
- [ ] `ast.c`にASTコンストラクタを追加
- [ ] `parser.c`にパーサールールを追加
- [ ] `runtime.c`または適切なモジュールにランタイム動作を追加
- [ ] ASTフリー関数でクリーンアップを処理

**組み込み関数を追加する場合:**

- [ ] `builtins.c`に関数実装を追加
- [ ] `register_builtins()`で関数を登録
- [ ] すべてのパラメータ型の組み合わせを処理
- [ ] 適切なエラー値を返す
- [ ] パラメータと戻り値型をドキュメント化

**値型を追加する場合:**

- [ ] `values.h`に型列挙型を追加
- [ ] Valueユニオンにフィールドを追加
- [ ] `values.c`にコンストラクタを追加
- [ ] クリーンアップ用に`value_free()`に追加
- [ ] コピー用に`value_copy()`に追加
- [ ] 印刷用に`value_to_string()`に追加
- [ ] 数値の場合は型プロモーションルールを追加

#### 3. テストフェーズ

- [ ] テストケースを書く（testing.mdを参照）
- [ ] 成功ケースをテスト
- [ ] エラーケースをテスト
- [ ] エッジケースをテスト
- [ ] 完全なテストスイートを実行（`make test`）
- [ ] valgrindでメモリリークをチェック
- [ ] 可能であれば複数のプラットフォームでテスト

#### 4. ドキュメントフェーズ

- [ ] ユーザー向けドキュメントでCLAUDE.mdを更新
- [ ] 実装を説明するコードコメントを追加
- [ ] `examples/`に例を作成
- [ ] 関連するdocs/ファイルを更新
- [ ] 破壊的変更をドキュメント化

#### 5. 提出フェーズ

- [ ] デバッグコードとコメントをクリーンアップ
- [ ] コードスタイル準拠を確認
- [ ] 最新のmainにリベース
- [ ] 詳細な説明付きでPull Requestを作成
- [ ] コードレビューフィードバックに対応

### 例: 新しい演算子の追加

例として剰余演算子`%`の追加を見てみましょう:

**1. レキサー (lexer.c):**
```c
// get_next_token()のswitch文に追加
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. レキサーヘッダー (lexer.h):**
```c
typedef enum {
    // ... 既存のトークン
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h):**
```c
typedef enum {
    // ... 既存の演算子
    OP_MOD,
    // ...
} BinaryOp;
```

**4. パーサー (parser.c):**
```c
// parse_multiplicative()または適切な優先順位レベルに追加
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. ランタイム (runtime.c):**
```c
// eval_binary_op()に追加
case OP_MOD:
    // 型チェック
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Error: Modulo by zero\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... 他の型の組み合わせを処理
    break;
```

**6. テスト (tests/operators/modulo.hml):**
```hemlock
// 基本的な剰余
print(10 % 3);  // 期待: 2

// 負の剰余
print(-10 % 3); // 期待: -1

// エラーケース（失敗するはず）
// print(10 % 0);  // ゼロ除算
```

**7. ドキュメント (CLAUDE.md):**
```markdown
### 算術演算子
- `+` - 加算
- `-` - 減算
- `*` - 乗算
- `/` - 除算
- `%` - 剰余（余り）
```

---

## コードレビュープロセス

### レビュアーが確認すること

**1. 正確性**
- コードは主張通りに動作するか？
- エッジケースは処理されているか？
- メモリリークはないか？
- エラーは適切に処理されているか？

**2. 哲学との整合性**
- これはHemlockの設計原則に合っているか？
- 明示的か暗黙的か？
- 複雑さを隠していないか？

**3. コード品質**
- コードは読みやすく保守可能か？
- 変数名は説明的か？
- 関数は適切なサイズか？
- 十分なドキュメントがあるか？

**4. テスト**
- 十分なテストケースがあるか？
- テストは成功と失敗のパスをカバーしているか？
- エッジケースはテストされているか？

**5. ドキュメント**
- ユーザー向けドキュメントは更新されているか？
- コードコメントは明確か？
- 例は提供されているか？

### フィードバックへの対応

**すべきこと:**
- レビュアーの時間に感謝する
- 理解できない場合は明確化の質問をする
- 同意しない場合は理由を説明する
- 要求された変更を迅速に行う
- スコープが変更された場合はPR説明を更新

**すべきでないこと:**
- 批判を個人的に受け取る
- 防御的に議論する
- フィードバックを無視する
- レビューコメントの上に強制プッシュする（リベースを除く）
- PRに無関係な変更を追加する

### PRをマージしてもらう

**マージの要件:**
- [ ] すべてのテストが合格
- [ ] メモリリークなし（valgrindクリーン）
- [ ] メンテナーからのコードレビュー承認
- [ ] ドキュメント更新済み
- [ ] コードスタイルガイドラインに従っている
- [ ] Hemlockの哲学に沿っている

**タイムライン:**
- 小さなPR（バグ修正）: 通常数日以内にレビュー
- 中程度のPR（新機能）: 1-2週間かかる可能性あり
- 大きなPR（主要な変更）: 広範な議論が必要

---

## 追加リソース

### 学習リソース

**インタプリタの理解:**
- "Crafting Interpreters" by Robert Nystrom
- "Writing An Interpreter In Go" by Thorsten Ball
- "Modern Compiler Implementation in C" by Andrew Appel

**Cプログラミング:**
- "The C Programming Language" by K&R
- "Expert C Programming" by Peter van der Linden
- "C Interfaces and Implementations" by David Hanson

**メモリ管理:**
- Valgrindドキュメント
- "Understanding and Using C Pointers" by Richard Reese

### 便利なコマンド

```bash
# デバッグシンボル付きでビルド
make clean && make CFLAGS="-g -O0"

# valgrindで実行
valgrind --leak-check=full ./hemlock script.hml

# 特定のテストカテゴリを実行
./tests/run_tests.sh tests/strings/

# コードナビゲーション用のタグファイルを生成
ctags -R .

# すべてのTODOとFIXMEを見つける
grep -rn "TODO\|FIXME" src/ include/
```

---

## 質問?

貢献について質問がある場合:

1. `docs/`のドキュメントを確認
2. 既存のGitHub Issueを検索
3. GitHub Discussionsで質問
4. 質問を含む新しいIssueを開く

**Hemlockへの貢献ありがとうございます！**
