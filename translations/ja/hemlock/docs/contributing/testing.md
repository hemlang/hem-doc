# Hemlockテストガイド

このガイドでは、Hemlockのテスト哲学、テストの書き方、テストスイートの実行方法を説明します。

---

## 目次

- [テスト哲学](#テスト哲学)
- [テストスイートの構造](#テストスイートの構造)
- [テストの実行](#テストの実行)
- [テストの作成](#テストの作成)
- [テストカテゴリ](#テストカテゴリ)
- [メモリリークテスト](#メモリリークテスト)
- [継続的インテグレーション](#継続的インテグレーション)
- [ベストプラクティス](#ベストプラクティス)

---

## テスト哲学

### 核となる原則

**1. テスト駆動開発（TDD）**

機能を実装する**前に**テストを書く:

```
1. 失敗するテストを書く
2. 機能を実装する
3. テストを実行する（合格するはず）
4. 必要に応じてリファクタリング
5. 繰り返す
```

**利点:**
- 機能が実際に動作することを確認
- 回帰を防ぐ
- 期待される動作をドキュメント化
- リファクタリングを安全にする

**2. 包括的なカバレッジ**

成功と失敗の両方のケースをテスト:

```hemlock
// 成功ケース
let x: u8 = 255;  // 動作するはず

// 失敗ケース
let y: u8 = 256;  // エラーになるはず
```

**3. 早期かつ頻繁にテスト**

以下のタイミングでテストを実行:
- コードをコミットする前
- 変更を加えた後
- プルリクエストを提出する前
- コードレビュー中

**ルール:** マージ前にすべてのテストが合格する必要があります。

### テストすべきもの

**常にテストすべきもの:**
- ✅ 基本機能（ハッピーパス）
- ✅ エラー条件（サッドパス）
- ✅ エッジケース（境界条件）
- ✅ 型チェックと変換
- ✅ メモリ管理（リークなし）
- ✅ 並行処理と競合状態

**テストカバレッジの例:**
```hemlock
// 機能: String.substr(start, length)

// ハッピーパス
print("hello".substr(0, 5));  // "hello"

// エッジケース
print("hello".substr(0, 0));  // ""（空）
print("hello".substr(5, 0));  // ""（末尾で）
print("hello".substr(2, 100)); // "llo"（末尾を超える）

// エラーケース
// "hello".substr(-1, 5);  // エラー: 負のインデックス
// "hello".substr(0, -1);  // エラー: 負の長さ
```

---

## テストスイートの構造

### ディレクトリ構成

```
tests/
├── run_tests.sh          # メインのテストランナースクリプト
├── primitives/           # 型システムテスト
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # 型変換テスト
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # ポインタ/バッファテスト
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # 文字列操作テスト
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # 制御フローテスト
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # 関数とクロージャテスト
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # オブジェクトテスト
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # 配列操作テスト
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # ループテスト
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # エラー処理テスト
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # ファイルI/Oテスト
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # 並行処理テスト
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # FFIテスト
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # シグナル処理テスト
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # コマンドライン引数テスト
    └── basic.hml
```

### テストファイルの命名

**規則:**
- 説明的な名前を使用: `method_chaining.hml`ではなく`test1.hml`
- 関連テストをグループ化: `string_substr.hml`、`string_slice.hml`
- 1ファイルに1つの機能領域
- ファイルを焦点を絞った小さなものに保つ

---

## テストの実行

### すべてのテストを実行

```bash
# hemlockルートディレクトリから
make test

# または直接
./tests/run_tests.sh
```

**出力:**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### 特定のカテゴリを実行

```bash
# 文字列テストのみ実行
./tests/run_tests.sh tests/strings/

# 1つのテストファイルのみ実行
./tests/run_tests.sh tests/strings/concat.hml

# 複数のカテゴリを実行
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Valgrindで実行（メモリリークチェック）

```bash
# 単一テストのリークをチェック
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# すべてのテストをチェック（遅い！）
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### 失敗したテストのデバッグ

```bash
# 詳細出力で実行
./hemlock tests/failing_test.hml

# gdbで実行
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # クラッシュした場合
```

---

## テストの作成

### テストファイルの形式

テストファイルは期待出力を持つHemlockプログラムです:

**例: tests/primitives/integers.hml**
```hemlock
// 基本的な整数リテラルをテスト
let x = 42;
print(x);  // 期待: 42

let y: i32 = 100;
print(y);  // 期待: 100

// 算術をテスト
let sum = x + y;
print(sum);  // 期待: 142

// 型推論をテスト
let small = 10;
print(typeof(small));  // 期待: i32

let large = 5000000000;
print(typeof(large));  // 期待: i64
```

**テストの動作:**
1. テストランナーが.hmlファイルを実行
2. stdout出力をキャプチャ
3. 期待出力と比較（コメントまたは別の.outファイルから）
4. 合格/不合格を報告

### 期待出力の方法

**方法1: インラインコメント（シンプルなテストに推奨）**

```hemlock
print("hello");  // 期待: hello
print(42);       // 期待: 42
```

テストランナーは`// 期待: ...`コメントをパースします。

**方法2: 別の.outファイル**

期待出力で`test_name.hml.out`を作成:

**test_name.hml:**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**test_name.hml.out:**
```
line 1
line 2
line 3
```

### エラーケースのテスト

エラーテストは非ゼロステータスでプログラムを終了させるべき:

**例: tests/primitives/range_error.hml**
```hemlock
// これは型エラーで失敗するはず
let x: u8 = 256;  // u8の範囲外
```

**期待される動作:**
- プログラムは非ゼロステータスで終了
- stderrにエラーメッセージを出力

**テストランナーの処理:**
- エラーを期待するテストは別ファイルにすべき
- 命名規則を使用: `*_error.hml`または`*_fail.hml`
- 期待されるエラーをコメントでドキュメント化

### 成功ケースのテスト

**例: tests/strings/methods.hml**
```hemlock
// substrをテスト
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // 期待: world

// findをテスト
let pos = s.find("world");
print(pos);  // 期待: 6

// containsをテスト
let has = s.contains("lo");
print(has);  // 期待: true

// trimをテスト
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // 期待: hello
```

### エッジケースのテスト

**例: tests/arrays/edge_cases.hml**
```hemlock
// 空の配列
let empty = [];
print(empty.length);  // 期待: 0

// 単一要素
let single = [42];
print(single[0]);  // 期待: 42

// 負のインデックス（別のテストファイルでエラーになるはず）
// print(single[-1]);  // エラー

// 末尾を超えるインデックス（エラーになるはず）
// print(single[100]);  // エラー

// 境界条件
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // 期待: []（空）
print(arr.slice(3, 3));  // 期待: []（空）
print(arr.slice(1, 2));  // 期待: [2]
```

### 型システムのテスト

**例: tests/conversions/promotion.hml**
```hemlock
// 二項演算での型プロモーションをテスト

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // 期待: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // 期待: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // 期待: i32
```

### 並行処理のテスト

**例: tests/async/basic.hml**
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

// タスクをスポーン
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// 結果をジョインして出力
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // 期待: 45
print(r2);  // 期待: 190
```

### 例外のテスト

**例: tests/exceptions/try_catch.hml**
```hemlock
// 基本的なtry/catchをテスト
try {
    throw "error message";
} catch (e) {
    print("Caught: " + e);  // 期待: Caught: error message
}

// finallyをテスト
let executed = false;
try {
    print("try");  // 期待: try
} finally {
    executed = true;
    print("finally");  // 期待: finally
}

// 例外伝播をテスト
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // 期待: failure
}
```

---

## テストカテゴリ

### プリミティブテスト

**テストすべきもの:**
- 整数型（i8、i16、i32、i64、u8、u16、u32、u64）
- 浮動小数点型（f32、f64）
- ブール型
- 文字列型
- ルーン型
- Null型

**テスト領域の例:**
- リテラル構文
- 型推論
- 範囲チェック
- オーバーフロー動作
- 型注釈

### 変換テスト

**テストすべきもの:**
- 暗黙の型プロモーション
- 明示的な型変換
- 損失のある変換（エラーになるべき）
- 操作での型プロモーション
- 異なる型間の比較

### メモリテスト

**テストすべきもの:**
- alloc/freeの正確性
- バッファの作成とアクセス
- バッファの境界チェック
- memset、memcpy、realloc
- メモリリーク検出（valgrind）

### 文字列テスト

**テストすべきもの:**
- 連結
- 全18の文字列メソッド
- UTF-8処理
- ルーンインデックス
- 文字列 + ルーン連結
- エッジケース（空文字列、単一文字など）

### 制御フローテスト

**テストすべきもの:**
- if/else/else if
- whileループ
- forループ
- switch文
- break/continue
- return文

### 関数テスト

**テストすべきもの:**
- 関数定義と呼び出し
- パラメータ渡し
- 戻り値
- 再帰
- クロージャとキャプチャ
- ファーストクラス関数
- 無名関数

### オブジェクトテスト

**テストすべきもの:**
- オブジェクトリテラル
- フィールドアクセスと代入
- メソッドとselfバインディング
- ダックタイピング
- オプションフィールド
- JSONシリアライゼーション/デシリアライゼーション
- 循環参照検出

### 配列テスト

**テストすべきもの:**
- 配列作成
- インデックスと代入
- 全15の配列メソッド
- 混合型
- 動的リサイズ
- エッジケース（空、単一要素）

### 例外テスト

**テストすべきもの:**
- try/catch/finally
- throw文
- 例外伝播
- ネストされたtry/catch
- try/catch/finally内でのreturn
- キャッチされない例外

### I/Oテスト

**テストすべきもの:**
- ファイルオープンモード
- 読み書き操作
- seek/tell
- ファイルプロパティ
- エラー処理（ファイルがないなど）
- リソースクリーンアップ

### 非同期テスト

**テストすべきもの:**
- spawn/join/detach
- チャネルsend/recv
- タスク内での例外伝播
- 複数の並行タスク
- チャネルのブロッキング動作

### FFIテスト

**テストすべきもの:**
- dlopen/dlclose
- dlsym
- 様々な型でのdlcall
- 型変換
- エラー処理

---

## メモリリークテスト

### Valgrindの使用

**基本的な使い方:**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**出力例（リークなし）:**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**出力例（リークあり）:**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### 一般的なリークの原因

**1. free()呼び出しの欠落:**
```c
// 悪い
char *str = malloc(100);
// ... strを使用
// 解放を忘れた！

// 良い
char *str = malloc(100);
// ... strを使用
free(str);
```

**2. ポインタの消失:**
```c
// 悪い
char *ptr = malloc(100);
ptr = malloc(200);  // 最初の割り当てへの参照を失った！

// 良い
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. 例外パス:**
```c
// 悪い
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // リーク！
    }
    free(data);
}

// 良い
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### 既知の許容可能なリーク

いくつかの小さな「リーク」は意図的な起動時割り当てです:

**グローバルビルトイン:**
```hemlock
// 組み込み関数、FFI型、定数は起動時に割り当てられ
// 終了時に解放されない（通常〜200バイト）
```

これらは真のリークではなく - プログラムの寿命中持続し、終了時にOSによってクリーンアップされる一度限りの割り当てです。

---

## 継続的インテグレーション

### GitHub Actions（将来）

CIがセットアップされると、すべてのテストは以下で自動的に実行されます:
- mainブランチへのプッシュ
- プルリクエストの作成/更新
- スケジュールされた毎日の実行

**CIワークフロー:**
1. Hemlockをビルド
2. テストスイートを実行
3. メモリリークをチェック（valgrind）
4. 結果をPRに報告

### コミット前チェック

コミット前に実行:

```bash
# 新規ビルド
make clean && make

# すべてのテストを実行
make test

# いくつかのテストでリークをチェック
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## ベストプラクティス

### すべきこと

✅ **最初にテストを書く（TDD）**
```bash
1. tests/feature/new_feature.hmlを作成
2. src/に機能を実装
3. テストが合格するまで実行
```

✅ **成功と失敗の両方をテスト**
```hemlock
// 成功: tests/feature/success.hml
let result = do_thing();
print(result);  // 期待: expected value

// 失敗: tests/feature/failure.hml
do_invalid_thing();  // エラーになるはず
```

✅ **説明的なテスト名を使用**
```
良い: tests/strings/substr_utf8_boundary.hml
悪い: tests/test1.hml
```

✅ **テストを焦点を絞ったものに保つ**
- 1ファイルに1つの機能領域
- 明確なセットアップとアサーション
- 最小限のコード

✅ **難しいテストを説明するコメントを追加**
```hemlock
// クロージャが外部変数を参照でキャプチャすることをテスト
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // クロージャ作成後に変更
    return f();  // 10ではなく20を返すはず
}
```

✅ **エッジケースをテスト**
- 空の入力
- Null値
- 境界値（最小/最大）
- 大きな入力
- 負の値

### すべきでないこと

❌ **テストをスキップしない**
- マージ前にすべてのテストが合格する必要がある
- 失敗するテストをコメントアウトしない
- バグを修正するか機能を削除する

❌ **互いに依存するテストを書かない**
```hemlock
// 悪い: test2.hmlがtest1.hmlの出力に依存
// テストは独立しているべき
```

❌ **テストでランダム値を使用しない**
```hemlock
// 悪い: 非決定論的
let x = random();
print(x);  // 出力を予測できない

// 良い: 決定論的
let x = 42;
print(x);  // 期待: 42
```

❌ **実装の詳細をテストしない**
```hemlock
// 悪い: 内部構造をテスト
let obj = { x: 10 };
// 内部フィールド順序、容量などをチェックしない

// 良い: 動作をテスト
print(obj.x);  // 期待: 10
```

❌ **メモリリークを無視しない**
- すべてのテストはvalgrindクリーンであるべき
- 既知/許容可能なリークをドキュメント化
- マージ前にリークを修正

### テストの保守

**テストを更新すべきとき:**
- 機能の動作が変更された
- バグ修正に新しいテストケースが必要
- エッジケースが発見された
- パフォーマンス改善

**テストを削除すべきとき:**
- 機能が言語から削除された
- テストが既存のカバレッジと重複
- テストが不正確だった

**テストのリファクタリング:**
- 関連テストをグループ化
- 共通のセットアップコードを抽出
- 一貫した命名を使用
- テストをシンプルで読みやすく保つ

---

## テストセッションの例

機能をテストと共に追加する完全な例を示します:

### 機能: `array.first()`メソッドの追加

**1. まずテストを書く:**

```bash
# テストファイルを作成
cat > tests/arrays/first_method.hml << 'EOF'
// array.first()メソッドをテスト

// 基本ケース
let arr = [1, 2, 3];
print(arr.first());  // 期待: 1

// 単一要素
let single = [42];
print(single.first());  // 期待: 42

// 空の配列（エラーになるべき - 別のテストファイル）
// let empty = [];
// print(empty.first());  // エラー
EOF
```

**2. テストを実行（失敗するはず）:**

```bash
./hemlock tests/arrays/first_method.hml
# エラー: Method 'first' not found on array
```

**3. 機能を実装:**

`src/interpreter/builtins.c`を編集:

```c
// array_firstメソッドを追加
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Error: Cannot get first element of empty array\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// 配列メソッドテーブルに登録
// ... 配列メソッド登録に追加
```

**4. テストを実行（合格するはず）:**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# 成功！
```

**5. メモリリークをチェック:**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. 完全なテストスイートを実行:**

```bash
make test
# Total: 252 tests (251 + 新しいもの)
# Passed: 252
# Failed: 0
```

**7. コミット:**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "array.first()メソッドをテストと共に追加"
```

---

## まとめ

**覚えておいてください:**
- 最初にテストを書く（TDD）
- 成功と失敗のケースをテスト
- コミット前にすべてのテストを実行
- メモリリークをチェック
- 既知の問題をドキュメント化
- テストをシンプルで焦点を絞ったものに保つ

**テスト品質はコード品質と同じくらい重要です！**
