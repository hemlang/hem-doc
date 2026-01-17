# HemlockのFFI（Foreign Function Interface）

Hemlockは、libffiを使用して共有ライブラリからC関数を呼び出すための**FFI（Foreign Function Interface）**を提供し、既存のCライブラリやシステムAPIとの統合を可能にします。

## 目次

- [概要](#概要)
- [現在のステータス](#現在のステータス)
- [サポートされている型](#サポートされている型)
- [基本概念](#基本概念)
- [FFI関数のエクスポート](#ffi関数のエクスポート)
- [使用ケース](#使用ケース)
- [将来の開発](#将来の開発)
- [FFIコールバック](#ffiコールバック)
- [FFI構造体](#ffi構造体)
- [構造体型のエクスポート](#構造体型のエクスポート)
- [現在の制限事項](#現在の制限事項)
- [ベストプラクティス](#ベストプラクティス)

## 概要

Foreign Function Interface (FFI)により、Hemlockプログラムは以下のことができます：
- 共有ライブラリ（.so、.dylib、.dll）からC関数を呼び出す
- ラッパーコードを書かずに既存のCライブラリを使用
- システムAPIに直接アクセス
- サードパーティのネイティブライブラリと統合
- Hemlockと低レベルのシステム機能を橋渡し

**主な機能：**
- 動的ライブラリローディング
- C関数バインディング
- HemlockとC型間の自動型変換
- すべてのプリミティブ型のサポート
- ポータビリティのためのlibffiベースの実装

## 現在のステータス

FFIサポートはHemlockで利用可能で、以下の機能があります：

**実装済み：**
- 共有ライブラリからC関数を呼び出す
- すべてのプリミティブ型（整数、浮動小数点、ポインタ）のサポート
- 自動型変換
- libffiベースの実装
- 動的ライブラリローディング
- **関数ポインタコールバック** - Hemlock関数をCに渡す
- **extern関数のエクスポート** - モジュール間でFFIバインディングを共有
- **構造体の受け渡しと戻り値** - C互換の構造体を値で渡す
- **完全なポインタヘルパー** - すべての型の読み書き（i8-i64, u8-u64, f32, f64, ptr）
- **バッファ/ポインタ変換** - `buffer_ptr()`, `ptr_to_buffer()`
- **FFI型サイズ** - プラットフォーム対応の型サイズ用`ffi_sizeof()`
- **プラットフォーム型** - `size_t`, `usize`, `isize`, `intptr_t`のサポート

**開発中：**
- 文字列マーシャリングヘルパー
- エラー処理の改善

**テストカバレッジ：**
- コールバックテストを含むFFIテストがパス
- 基本的な関数呼び出しを検証
- 型変換をテスト
- qsortコールバック統合をテスト

## サポートされている型

### プリミティブ型

以下のHemlock型はC関数との間で受け渡しできます：

| Hemlock型 | C型 | サイズ | 備考 |
|--------------|--------|------|-------|
| `i8` | `int8_t` | 1バイト | 符号付き8ビット整数 |
| `i16` | `int16_t` | 2バイト | 符号付き16ビット整数 |
| `i32` | `int32_t` | 4バイト | 符号付き32ビット整数 |
| `i64` | `int64_t` | 8バイト | 符号付き64ビット整数 |
| `u8` | `uint8_t` | 1バイト | 符号なし8ビット整数 |
| `u16` | `uint16_t` | 2バイト | 符号なし16ビット整数 |
| `u32` | `uint32_t` | 4バイト | 符号なし32ビット整数 |
| `u64` | `uint64_t` | 8バイト | 符号なし64ビット整数 |
| `f32` | `float` | 4バイト | 32ビット浮動小数点 |
| `f64` | `double` | 8バイト | 64ビット浮動小数点 |
| `ptr` | `void*` | 8バイト | 生ポインタ |

### 型変換

**自動変換：**
- Hemlock整数 → C整数（範囲チェック付き）
- Hemlock浮動小数点 → C浮動小数点
- Hemlockポインタ → Cポインタ
- C戻り値 → Hemlock値

**型マッピングの例：**
```hemlock
// Hemlock → C
let i: i32 = 42;         // → int32_t (4バイト)
let f: f64 = 3.14;       // → double (8バイト)
let p: ptr = alloc(64);  // → void* (8バイト)

// C → Hemlock (戻り値)
// int32_t foo() → i32
// double bar() → f64
// void* baz() → ptr
```

## 基本概念

### 共有ライブラリ

FFIはコンパイルされた共有ライブラリで動作します：

**Linux:** `.so`ファイル
```
libexample.so
/usr/lib/libm.so
```

**macOS:** `.dylib`ファイル
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** `.dll`ファイル
```
example.dll
kernel32.dll
```

### 関数シグネチャ

FFIが正しく動作するには、C関数のシグネチャが既知である必要があります：

```c
// C関数シグネチャの例
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

これらは、ライブラリがロードされ、関数がバインドされるとHemlockから呼び出せます。

### プラットフォーム互換性

FFIはポータビリティのために**libffi**を使用します：
- x86、x86-64、ARM、ARM64で動作
- 呼び出し規約を自動的に処理
- プラットフォーム固有のABIの詳細を抽象化
- Linux、macOS、Windows（適切なlibffiを使用）をサポート

## FFI関数のエクスポート

`extern fn`で宣言されたFFI関数はモジュールからエクスポートでき、複数のファイルで共有できる再利用可能なライブラリラッパーを作成できます。

### 基本的なエクスポート構文

```hemlock
// string_utils.hml - C文字列関数をラップするライブラリモジュール
import "libc.so.6";

// extern関数を直接エクスポート
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// extern関数と一緒にラッパー関数もエクスポートできる
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### エクスポートされたFFI関数のインポート

```hemlock
// main.hml - エクスポートされたFFI関数を使用
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hello, World!";
print(strlen(msg));           // 13 - 直接extern呼び出し
print(string_length(msg));    // 13 - ラッパー関数

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### export externの使用ケース

**1. プラットフォーム抽象化**
```hemlock
// platform.hml - プラットフォームの違いを抽象化
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. ライブラリラッパー**
```hemlock
// crypto_lib.hml - 暗号ライブラリ関数をラップ
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Hemlockフレンドリーなラッパーを追加
export fn sha256_string(s: string): string {
    // extern関数を使用した実装
}
```

**3. 集中化されたFFI宣言**
```hemlock
// libc.hml - libcバインディングの中央モジュール
import "libc.so.6";

// 文字列関数
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// メモリ関数
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// プロセス関数
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

プロジェクト全体で使用：
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

### 通常のエクスポートとの組み合わせ

エクスポートされたextern関数と通常の関数エクスポートを混在させることができます：

```hemlock
// math_extended.hml
import "libm.so.6";

// 生のC関数をエクスポート
export extern fn sin(x: f64): f64;
export extern fn cos(x: f64): f64;
export extern fn tan(x: f64): f64;

// それらを使用するHemlock関数をエクスポート
export fn deg_to_rad(degrees: f64): f64 {
    return degrees * 3.14159265359 / 180.0;
}

export fn sin_degrees(degrees: f64): f64 {
    return sin(deg_to_rad(degrees));
}
```

### プラットフォーム固有のライブラリ

extern関数をエクスポートする際、ライブラリ名はプラットフォームによって異なることに注意してください：

```hemlock
// Linux用
import "libc.so.6";

// macOS用（異なるアプローチが必要）
import "libSystem.B.dylib";
```

現在、Hemlockの`import "library"`構文は静的なライブラリパスを使用するため、クロスプラットフォームFFIコードにはプラットフォーム固有のモジュールが必要な場合があります。

## 使用ケース

### 1. システムライブラリ

標準Cライブラリ関数にアクセス：

**数学関数：**
```hemlock
// libmからsqrtを呼び出す
let result = sqrt(16.0);  // 4.0
```

**メモリ割り当て：**
```hemlock
// libcからmalloc/freeを呼び出す
let ptr = malloc(1024);
free(ptr);
```

### 2. サードパーティライブラリ

既存のCライブラリを使用：

**例：画像処理**
```hemlock
// libpngまたはlibjpegをロード
// Cライブラリ関数を使用して画像を処理
```

**例：暗号化**
```hemlock
// OpenSSLまたはlibsodiumを使用
// FFI経由で暗号化/復号化
```

### 3. システムAPI

直接システムコール：

**例：POSIX API**
```hemlock
// getpid、getuidなどを呼び出す
// 低レベルのシステム機能にアクセス
```

### 4. パフォーマンスクリティカルなコード

最適化されたC実装を呼び出す：

```hemlock
// 高度に最適化されたCライブラリを使用
// SIMD操作、ベクトル化コード
// ハードウェアアクセラレーション関数
```

### 5. ハードウェアアクセス

ハードウェアライブラリとのインターフェース：

```hemlock
// 組み込みシステムでのGPIO制御
// USBデバイス通信
// シリアルポートアクセス
```

### 6. レガシーコード統合

既存のCコードベースを再利用：

```hemlock
// レガシーCアプリケーションから関数を呼び出す
// Hemlockへの段階的な移行
// 動作するCコードを保持
```

## 将来の開発

### 計画されている機能

**1. 構造体サポート**
```hemlock
// 将来：C構造体の受け渡し/戻り
define Point {
    x: f64,
    y: f64,
}

let p = Point { x: 1.0, y: 2.0 };
c_function_with_struct(p);
```

**2. 配列/バッファ処理**
```hemlock
// 将来：より良い配列の受け渡し
let arr = [1, 2, 3, 4, 5];
process_array(arr);  // C関数に渡す
```

**3. 関数ポインタコールバック** （実装済み！）
```hemlock
// Hemlock関数をコールバックとしてCに渡す
fn my_compare(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    return va - vb;
}

// C呼び出し可能な関数ポインタを作成
let cmp = callback(my_compare, ["ptr", "ptr"], "i32");

// qsortやコールバックを期待するC関数で使用
qsort(arr, count, elem_size, cmp);

// 完了時にクリーンアップ
callback_free(cmp);
```

**4. 文字列マーシャリング**
```hemlock
// 将来：自動文字列変換
let s = "hello";
c_string_function(s);  // C文字列に自動変換
```

**5. エラー処理**
```hemlock
// 将来：より良いエラー報告
try {
    let result = risky_c_function();
} catch (e) {
    print("FFI error: " + e);
}
```

**6. 型安全性**
```hemlock
// 将来：FFI用の型注釈
@ffi("libm.so")
fn sqrt(x: f64): f64;

let result = sqrt(16.0);  // 型チェック済み
```

### 機能

**v1.0：**
- 基本的なFFIとプリミティブ型
- 動的ライブラリローディング
- 関数呼び出し
- libffiクロージャによるコールバックサポート

**将来：**
- 構造体サポート
- 配列処理の改善
- 自動バインディング生成

## FFIコールバック

Hemlockは、libffiクロージャを使用してコールバックとしてC側にHemlock関数を渡すことをサポートしています。これにより、`qsort`、イベントループ、コールバックベースのライブラリなど、関数ポインタを期待するC APIとの統合が可能になります。

### コールバックの作成

`callback()`を使用してHemlock関数からC呼び出し可能な関数ポインタを作成：

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**パラメータ：**
- `function`：ラップするHemlock関数
- `param_types`：型名文字列の配列（例：`["ptr", "i32"]`）
- `return_type`：戻り値の型文字列（例：`"i32"`, `"void"`）

**サポートされるコールバック型：**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - 符号付き整数
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - 符号なし整数
- `"f32"`, `"f64"` - 浮動小数点
- `"ptr"` - ポインタ
- `"void"` - 戻り値なし
- `"bool"` - ブール値

### 例：qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// 整数用の比較関数（昇順）
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// 5つの整数の配列を割り当て
let arr = alloc(20);  // 5 * 4バイト
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// コールバックを作成してソート
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// 配列はソート済み：[1, 2, 5, 8, 9]

// クリーンアップ
callback_free(cmp);
free(arr);
```

### ポインタヘルパー関数

Hemlockは生ポインタを扱うための包括的なヘルパー関数を提供します。これらはFFIコールバックや直接メモリ操作に不可欠です。

#### 整数型ヘルパー

| 関数 | 説明 |
|----------|-------------|
| `ptr_deref_i8(ptr)` | ポインタをデリファレンスしてi8を読み取り |
| `ptr_deref_i16(ptr)` | ポインタをデリファレンスしてi16を読み取り |
| `ptr_deref_i32(ptr)` | ポインタをデリファレンスしてi32を読み取り |
| `ptr_deref_i64(ptr)` | ポインタをデリファレンスしてi64を読み取り |
| `ptr_deref_u8(ptr)` | ポインタをデリファレンスしてu8を読み取り |
| `ptr_deref_u16(ptr)` | ポインタをデリファレンスしてu16を読み取り |
| `ptr_deref_u32(ptr)` | ポインタをデリファレンスしてu32を読み取り |
| `ptr_deref_u64(ptr)` | ポインタをデリファレンスしてu64を読み取り |
| `ptr_write_i8(ptr, value)` | ポインタ位置にi8を書き込み |
| `ptr_write_i16(ptr, value)` | ポインタ位置にi16を書き込み |
| `ptr_write_i32(ptr, value)` | ポインタ位置にi32を書き込み |
| `ptr_write_i64(ptr, value)` | ポインタ位置にi64を書き込み |
| `ptr_write_u8(ptr, value)` | ポインタ位置にu8を書き込み |
| `ptr_write_u16(ptr, value)` | ポインタ位置にu16を書き込み |
| `ptr_write_u32(ptr, value)` | ポインタ位置にu32を書き込み |
| `ptr_write_u64(ptr, value)` | ポインタ位置にu64を書き込み |

#### 浮動小数点型ヘルパー

| 関数 | 説明 |
|----------|-------------|
| `ptr_deref_f32(ptr)` | ポインタをデリファレンスしてf32（float）を読み取り |
| `ptr_deref_f64(ptr)` | ポインタをデリファレンスしてf64（double）を読み取り |
| `ptr_write_f32(ptr, value)` | ポインタ位置にf32を書き込み |
| `ptr_write_f64(ptr, value)` | ポインタ位置にf64を書き込み |

#### ポインタ型ヘルパー

| 関数 | 説明 |
|----------|-------------|
| `ptr_deref_ptr(ptr)` | ポインタへのポインタをデリファレンス |
| `ptr_write_ptr(ptr, value)` | ポインタ位置にポインタを書き込み |
| `ptr_offset(ptr, index, size)` | オフセットを計算：`ptr + index * size` |
| `ptr_read_i32(ptr)` | ポインタへのポインタ経由でi32を読み取り（qsortコールバック用） |
| `ptr_null()` | nullポインタ定数を取得 |

#### バッファ変換ヘルパー

| 関数 | 説明 |
|----------|-------------|
| `buffer_ptr(buffer)` | バッファから生ポインタを取得 |
| `ptr_to_buffer(ptr, size)` | ポインタからデータを新しいバッファにコピー |

#### FFIユーティリティ関数

| 関数 | 説明 |
|----------|-------------|
| `ffi_sizeof(type_name)` | FFI型のバイトサイズを取得 |

**`ffi_sizeof`でサポートされる型名：**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - 符号付き整数（1, 2, 4, 8バイト）
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - 符号なし整数（1, 2, 4, 8バイト）
- `"f32"`, `"f64"` - 浮動小数点（4, 8バイト）
- `"ptr"` - ポインタ（64ビットでは8バイト）
- `"size_t"`, `"usize"` - プラットフォーム依存のサイズ型
- `"intptr_t"`, `"isize"` - プラットフォーム依存の符号付きポインタ型

#### 例：異なる型での作業

```hemlock
let p = alloc(64);

// 整数の書き込みと読み取り
ptr_write_i8(p, 42);
print(ptr_deref_i8(p));  // 42

ptr_write_i64(ptr_offset(p, 1, 8), 9000000000);
print(ptr_deref_i64(ptr_offset(p, 1, 8)));  // 9000000000

// 浮動小数点の書き込みと読み取り
ptr_write_f64(p, 3.14159);
print(ptr_deref_f64(p));  // 3.14159

// ポインタへのポインタ
let inner = alloc(4);
ptr_write_i32(inner, 999);
ptr_write_ptr(p, inner);
let retrieved = ptr_deref_ptr(p);
print(ptr_deref_i32(retrieved));  // 999

// 型サイズの取得
print(ffi_sizeof("i64"));  // 8
print(ffi_sizeof("ptr"));  // 8（64ビット環境）

// バッファ変換
let buf = buffer(64);
ptr_write_i32(buffer_ptr(buf), 12345);
print(ptr_deref_i32(buffer_ptr(buf)));  // 12345

free(inner);
free(p);
```

### コールバックの解放

**重要：**メモリリークを防ぐため、完了時に常にコールバックを解放してください：

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ...コールバックを使用...
callback_free(cb);  // 完了時に解放
```

コールバックはプログラム終了時にも自動的に解放されます。

### コールバック内のクロージャ

コールバックはクロージャ環境をキャプチャするため、外部スコープの変数にアクセスできます：

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // 外部スコープの'multiplier'にアクセス可能
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### スレッド安全性

コールバック呼び出しはスレッド安全性を確保するためにmutexでシリアライズされます。Hemlockインタープリターは完全にはスレッドセーフではないためです。これは以下を意味します：
- 一度に1つのコールバックのみが実行可能
- マルチスレッドCライブラリでも安全に使用可能
- コールバックが複数のスレッドから非常に頻繁に呼び出される場合、パフォーマンスに影響する可能性

### コールバック内のエラー処理

コールバック内でスローされた例外はCコードに伝播できません。代わりに：
- stderrに警告が出力される
- コールバックはデフォルト値（0またはNULL）を返す
- 例外はログに記録されるが伝播されない

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Something went wrong";  // 警告が出力され、0を返す
}
```

堅牢なエラー処理のために、入力を検証し、コールバック内でのスローを避けてください。

## FFI構造体

Hemlockは構造体を値でC関数に渡すことをサポートしています。構造体型は型注釈付きで定義すると、FFI用に自動的に登録されます。

### FFI互換構造体の定義

構造体がFFI互換となるのは、すべてのフィールドにFFI互換型を使用した明示的な型注釈がある場合です：

```hemlock
// FFI互換構造体
define Point {
    x: f64,
    y: f64,
}

// 複数のフィールド型を持つFFI互換構造体
define Rectangle {
    top_left: Point,      // ネストされた構造体
    width: f64,
    height: f64,
}

// FFI互換でない（型注釈のないフィールド）
define DynamicObject {
    name,                 // 型なし - FFIで使用不可
    value,
}
```

### FFIでの構造体の使用

構造体型を使用するextern関数を宣言：

```hemlock
// 構造体型を定義
define Vector2D {
    x: f64,
    y: f64,
}

// Cライブラリをインポート
import "libmath.so";

// 構造体を取る/返すextern関数を宣言
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// 自然に使用
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### サポートされるフィールド型

構造体フィールドはこれらのFFI互換型を使用する必要があります：

| Hemlock型 | C型 | サイズ |
|--------------|--------|------|
| `i8` | `int8_t` | 1バイト |
| `i16` | `int16_t` | 2バイト |
| `i32` | `int32_t` | 4バイト |
| `i64` | `int64_t` | 8バイト |
| `u8` | `uint8_t` | 1バイト |
| `u16` | `uint16_t` | 2バイト |
| `u32` | `uint32_t` | 4バイト |
| `u64` | `uint64_t` | 8バイト |
| `f32` | `float` | 4バイト |
| `f64` | `double` | 8バイト |
| `ptr` | `void*` | 8バイト |
| `string` | `char*` | 8バイト |
| `bool` | `int` | 可変 |
| ネストされた構造体 | struct | 可変 |

### 構造体レイアウト

Hemlockはプラットフォームのネイティブ構造体レイアウトルール（C ABIに一致）を使用します：
- フィールドは型に応じてアラインメント
- 必要に応じてパディングが挿入
- 合計サイズは最大メンバーにアラインメントするようパディング

```hemlock
// 例：C互換レイアウト
define Mixed {
    a: i8,    // オフセット0、サイズ1
              // 3バイトパディング
    b: i32,   // オフセット4、サイズ4
}
// 合計サイズ：8バイト（パディング込み）

define Point3D {
    x: f64,   // オフセット0、サイズ8
    y: f64,   // オフセット8、サイズ8
    z: f64,   // オフセット16、サイズ8
}
// 合計サイズ：24バイト（パディング不要）
```

### ネストされた構造体

構造体は他の構造体を含むことができます：

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### 構造体の戻り値

C関数は構造体を返すことができます：

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### 制限事項

- **構造体フィールドには型注釈が必要** - 型のないフィールドはFFI互換でない
- **構造体内の配列なし** - 代わりにポインタを使用
- **共用体なし** - 構造体型のみサポート
- **コールバックは構造体を返せない** - コールバック戻り値にはポインタを使用

### 構造体型のエクスポート

`export define`を使用してモジュールから構造体型定義をエクスポートできます：

```hemlock
// geometry.hml
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}

export fn create_rect(x: f32, y: f32, w: f32, h: f32): Rectangle {
    return { x: x, y: y, width: w, height: h };
}
```

**重要：**エクスポートされた構造体型はモジュールがロードされると**グローバルに**登録されます。モジュールから何かをインポートすると自動的に利用可能になります。名前で明示的にインポートする必要は（できません）：

```hemlock
// main.hml

// 良い例 - 構造体型はモジュールからのインポート後に自動的に利用可能
import { create_rect } from "./geometry.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };      // 動作 - Vector2はグローバルに利用可能
let r: Rectangle = create_rect(0.0, 0.0, 100.0, 50.0);  // 動作

// 悪い例 - 構造体型を名前で明示的にインポートできない
import { Vector2 } from "./geometry.hml";  // エラー：未定義の変数 'Vector2'
```

この動作は、構造体型がモジュールのエクスポート環境に値として格納されるのではなく、モジュールロード時にグローバル型レジストリに登録されるためです。型はモジュールからインポートするすべてのコードで利用可能になります。

## 現在の制限事項

FFIには以下の制限事項があります：

**1. 手動型変換**
- 文字列変換を手動で管理する必要がある
- Hemlock文字列 ↔ C文字列の自動変換なし

**2. 限定的なエラー処理**
- 基本的なエラー報告
- コールバック内の例外はCに伝播できない

**3. 手動ライブラリローディング**
- ライブラリを手動でロードする必要がある
- 自動バインディング生成なし

**4. プラットフォーム固有のコード**
- ライブラリパスはプラットフォームによって異なる
- .so vs .dylib vs .dllを処理する必要がある

## ベストプラクティス

包括的なFFIドキュメントはまだ開発中ですが、一般的なベストプラクティスを以下に示します：

### 1. 型安全性

```hemlock
// 型を明示的に指定
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. メモリ管理

```hemlock
// 割り当てられたメモリを解放することを忘れずに
let ptr = c_malloc(1024);
// ...ptrを使用
c_free(ptr);
```

### 3. エラーチェック

```hemlock
// 戻り値をチェック
let result = c_function();
if (result == null) {
    print("C function failed");
}
```

### 4. プラットフォーム互換性

```hemlock
// プラットフォームの違いを処理
// 適切なライブラリ拡張子を使用（.so、.dylib、.dll）
```

## 例

動作する例については、以下を参照してください：
- コールバックテスト：`/tests/ffi_callbacks/` - qsortコールバックの例
- stdlib FFI使用：`/stdlib/hash.hml`、`/stdlib/regex.hml`、`/stdlib/crypto.hml`
- サンプルプログラム：`/examples/`（利用可能な場合）

## ヘルプの取得

FFIはHemlockの新しい機能です。質問や問題については：

1. テストスイートで動作する例を確認
2. 低レベルの詳細についてはlibffiドキュメントを参照
3. プロジェクトのissuesを通じてバグ報告や機能リクエスト

## まとめ

HemlockのFFIは以下を提供します：

- 共有ライブラリからのC関数呼び出し
- プリミティブ型サポート（i8-i64, u8-u64, f32, f64, ptr）
- 自動型変換
- libffiベースのポータビリティ
- ネイティブライブラリ統合の基盤
- **関数ポインタコールバック** - Hemlock関数をCに渡す
- **extern関数のエクスポート** - モジュール間でFFIバインディングを共有
- **構造体の受け渡しと戻り** - C互換構造体を値で渡す
- **defineのエクスポート** - モジュール間で構造体型定義を共有（グローバルに自動インポート）
- **完全なポインタヘルパー** - すべての型の読み書き（i8-i64, u8-u64, f32, f64, ptr）
- **バッファ/ポインタ変換** - データマーシャリング用`buffer_ptr()`、`ptr_to_buffer()`
- **FFI型サイズ** - プラットフォーム対応の型サイズ用`ffi_sizeof()`
- **プラットフォーム型** - `size_t`、`usize`、`isize`、`intptr_t`、`uintptr_t`のサポート

**現在のステータス：**FFIはプリミティブ型、構造体、コールバック、モジュールエクスポート、完全なポインタヘルパー関数で完全な機能を備えています

**将来：**文字列マーシャリングヘルパー

**使用ケース：**システムライブラリ、サードパーティライブラリ、qsort、イベントループ、コールバックベースAPI、再利用可能なライブラリラッパー

## 貢献

FFIドキュメントは拡張中です。FFIで作業している場合：
- 使用ケースをドキュメント化
- サンプルコードを共有
- 問題や制限を報告
- 改善を提案

FFIシステムは、必要な場合に低レベルアクセスを提供しながら、実用的で安全になるよう設計されており、Hemlockの「暗黙より明示」と「unsafeはバグではなく機能」という哲学に従っています。
