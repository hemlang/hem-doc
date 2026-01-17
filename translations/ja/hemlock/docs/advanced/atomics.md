# アトミック操作

Hemlockは**ロックフリー並行プログラミング**のためのアトミック操作を提供します。これらの操作により、従来のロックやミューテックスを使用せずに、複数のスレッド間で共有メモリを安全に操作できます。

## 目次

- [概要](#概要)
- [アトミックを使用する場面](#アトミックを使用する場面)
- [メモリモデル](#メモリモデル)
- [アトミックロードとストア](#アトミックロードとストア)
- [フェッチアンドモディファイ操作](#フェッチアンドモディファイ操作)
- [コンペアアンドスワップ (CAS)](#コンペアアンドスワップ-cas)
- [アトミックエクスチェンジ](#アトミックエクスチェンジ)
- [メモリフェンス](#メモリフェンス)
- [関数リファレンス](#関数リファレンス)
- [一般的なパターン](#一般的なパターン)
- [ベストプラクティス](#ベストプラクティス)
- [制限事項](#制限事項)

---

## 概要

アトミック操作は、中断の可能性なく完了する**不可分**な操作です。あるスレッドがアトミック操作を実行している間、他のスレッドはその操作が部分的に完了した状態を観察することはできません。

**主な特徴:**
- すべての操作で**逐次一貫性**（`memory_order_seq_cst`）を使用
- サポートされる型: **i32** と **i64**
- `alloc()`で確保した生ポインタに対して動作
- 明示的なロックなしでスレッドセーフ

**利用可能な操作:**
- Load/Store - アトミックに値を読み書き
- Add/Sub - 古い値を返す算術演算
- And/Or/Xor - 古い値を返すビット演算
- CAS - 条件付き更新のためのコンペアアンドスワップ
- Exchange - アトミックに値を交換
- Fence - 完全なメモリバリア

---

## アトミックを使用する場面

**アトミックを使用すべき場合:**
- タスク間で共有されるカウンタ（例：リクエスト数、進捗追跡）
- フラグとステータスインジケータ
- ロックフリーデータ構造
- 単純な同期プリミティブ
- パフォーマンスが重要な並行コード

**代わりにチャネルを使用すべき場合:**
- タスク間で複雑なデータを渡す場合
- プロデューサー・コンシューマーパターンを実装する場合
- メッセージパッシングセマンティクスが必要な場合

**使用例 - 共有カウンタ:**
```hemlock
// 共有カウンタを確保
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// 複数のワーカーを生成
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// カウンタは正確に3000になる（データ競合なし）
print(atomic_load_i32(counter));

free(counter);
```

---

## メモリモデル

すべてのHemlockアトミック操作は**逐次一貫性**（`memory_order_seq_cst`）を使用し、最も強いメモリ順序保証を提供します：

1. **アトミック性**: 各操作は不可分
2. **全順序付け**: すべてのスレッドが同じ操作順序を観察
3. **リオーダリングなし**: コンパイラやCPUによる操作の並び替えなし

これにより、弱いメモリ順序付けと比較して潜在的なパフォーマンスコストはありますが、並行コードの推論が簡単になります。

---

## アトミックロードとストア

### atomic_load_i32 / atomic_load_i64

メモリから値をアトミックに読み取ります。

**シグネチャ:**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**パラメータ:**
- `ptr` - メモリ位置へのポインタ（適切にアラインされている必要あり）

**戻り値:** メモリ位置の値

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

メモリに値をアトミックに書き込みます。

**シグネチャ:**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**パラメータ:**
- `ptr` - メモリ位置へのポインタ
- `value` - 格納する値

**戻り値:** `null`

**例:**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## フェッチアンドモディファイ操作

これらの操作は値をアトミックに変更し、**古い**（変更前の）値を返します。

### atomic_add_i32 / atomic_add_i64

値にアトミックに加算します。

**シグネチャ:**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**戻り値:** **古い**値（加算前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100（古い値）
print(atomic_load_i32(p));     // 110（新しい値）

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

値からアトミックに減算します。

**シグネチャ:**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**戻り値:** **古い**値（減算前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100（古い値）
print(atomic_load_i32(p));     // 75（新しい値）

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

ビット単位ANDをアトミックに実行します。

**シグネチャ:**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**戻り値:** **古い**値（AND前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 2進数で255: 11111111

let old = atomic_and_i32(p, 0x0F);  // 00001111とAND
print(old);                    // 255（古い値）
print(atomic_load_i32(p));     // 15（0xFF & 0x0F = 0x0F）

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

ビット単位ORをアトミックに実行します。

**シグネチャ:**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**戻り値:** **古い**値（OR前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 2進数で15: 00001111

let old = atomic_or_i32(p, 0xF0);  // 11110000とOR
print(old);                    // 15（古い値）
print(atomic_load_i32(p));     // 255（0x0F | 0xF0 = 0xFF）

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

ビット単位XORをアトミックに実行します。

**シグネチャ:**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**戻り値:** **古い**値（XOR前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 2進数で170: 10101010

let old = atomic_xor_i32(p, 0xFF);  // 11111111とXOR
print(old);                    // 170（古い値）
print(atomic_load_i32(p));     // 85（0xAA ^ 0xFF = 0x55）

free(p);
```

---

## コンペアアンドスワップ (CAS)

最も強力なアトミック操作です。現在の値と期待値をアトミックに比較し、一致する場合は新しい値で置き換えます。

### atomic_cas_i32 / atomic_cas_i64

**シグネチャ:**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**パラメータ:**
- `ptr` - メモリ位置へのポインタ
- `expected` - 期待する値
- `desired` - 期待値と一致した場合に格納する値

**戻り値:**
- `true` - スワップ成功（値が`expected`だったので`desired`になった）
- `false` - スワップ失敗（値が`expected`ではなかったので変更なし）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS成功: 値は100なので999にスワップ
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS失敗: 値は999であり100ではない
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999（変更なし）

free(p);
```

**ユースケース:**
- ロックとセマフォの実装
- ロックフリーデータ構造
- 楽観的並行制御
- アトミックな条件付き更新

---

## アトミックエクスチェンジ

値をアトミックにスワップし、古い値を返します。

### atomic_exchange_i32 / atomic_exchange_i64

**シグネチャ:**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**パラメータ:**
- `ptr` - メモリ位置へのポインタ
- `value` - 格納する新しい値

**戻り値:** **古い**値（交換前）

**例:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100（古い値）
print(atomic_load_i32(p));     // 200（新しい値）

free(p);
```

---

## メモリフェンス

完全なメモリバリアで、フェンス前のすべてのメモリ操作が、フェンス後の操作の前にすべてのスレッドから可視になることを保証します。

### atomic_fence

**シグネチャ:**
```hemlock
atomic_fence(): null
```

**戻り値:** `null`

**例:**
```hemlock
// 以前のすべての書き込みが可視になることを保証
atomic_fence();
```

**注意:** ほとんどの場合、すべてのアトミック操作が既に逐次一貫性を使用しているため、明示的なフェンスは必要ありません。フェンスは非アトミックメモリ操作を同期する必要がある場合に有用です。

---

## 関数リファレンス

### i32操作

| 関数 | シグネチャ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `atomic_load_i32` | `(ptr)` | `i32` | アトミックに値をロード |
| `atomic_store_i32` | `(ptr, value)` | `null` | アトミックに値をストア |
| `atomic_add_i32` | `(ptr, value)` | `i32` | 加算して古い値を返す |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | 減算して古い値を返す |
| `atomic_and_i32` | `(ptr, value)` | `i32` | ビット単位ANDして古い値を返す |
| `atomic_or_i32` | `(ptr, value)` | `i32` | ビット単位ORして古い値を返す |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | ビット単位XORして古い値を返す |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | コンペアアンドスワップ |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | 交換して古い値を返す |

### i64操作

| 関数 | シグネチャ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `atomic_load_i64` | `(ptr)` | `i64` | アトミックに値をロード |
| `atomic_store_i64` | `(ptr, value)` | `null` | アトミックに値をストア |
| `atomic_add_i64` | `(ptr, value)` | `i64` | 加算して古い値を返す |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | 減算して古い値を返す |
| `atomic_and_i64` | `(ptr, value)` | `i64` | ビット単位ANDして古い値を返す |
| `atomic_or_i64` | `(ptr, value)` | `i64` | ビット単位ORして古い値を返す |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | ビット単位XORして古い値を返す |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | コンペアアンドスワップ |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | 交換して古い値を返す |

### メモリバリア

| 関数 | シグネチャ | 戻り値 | 説明 |
|----------|-----------|---------|-------------|
| `atomic_fence` | `()` | `null` | 完全なメモリバリア |

---

## 一般的なパターン

### パターン: アトミックカウンタ

```hemlock
// スレッドセーフなカウンタ
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// 使用法
increment();  // 0を返す（古い値）
increment();  // 1を返す
increment();  // 2を返す
print(get_count());  // 3

free(counter);
```

### パターン: スピンロック

```hemlock
// シンプルなスピンロック実装
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = アンロック、1 = ロック

fn acquire() {
    // ロックを0から1に設定できるまでスピン
    while (!atomic_cas_i32(lock, 0, 1)) {
        // ビジーウェイト
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// 使用法
acquire();
// ... クリティカルセクション ...
release();

free(lock);
```

### パターン: 一度だけの初期化

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = 未初期化、1 = 初期化済み

fn ensure_initialized() {
    // 初期化する側になろうとする
    if (atomic_cas_i32(initialized, 0, 1)) {
        // 競争に勝ったので初期化を実行
        do_expensive_init();
    }
    // そうでなければ、既に初期化済み
}
```

### パターン: アトミックフラグ

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // フラグが既にセットされていればtrueを返す
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### パターン: 境界付きカウンタ

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // 最大値に達している
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // インクリメント成功
        }
        // CAS失敗、他のスレッドが変更 - リトライ
    }
}
```

---

## ベストプラクティス

### 1. 適切なアラインメントを使用

ポインタはデータ型に対して適切にアラインされている必要があります：
- i32: 4バイトアラインメント
- i64: 8バイトアラインメント

`alloc()`からのメモリは通常、適切にアラインされています。

### 2. より高レベルの抽象化を優先

可能な場合は、タスク間通信にチャネルを使用してください。アトミックは低レベルであり、注意深い推論が必要です。

```hemlock
// こちらを優先:
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// 適切な場合は手動のアトミック協調よりも
```

### 3. ABA問題に注意

CASはABA問題の影響を受ける可能性があります：値がAからBに変わり、再びAに戻ります。CASは成功しますが、その間に状態が変わっている可能性があります。

### 4. 共有前に初期化

タスクを生成する前に、常にアトミック変数を初期化してください：

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // 生成前に初期化

let task = spawn(worker, counter);
```

### 5. すべてのタスク完了後に解放

タスクがまだアクセスしている可能性がある間は、アトミックメモリを解放しないでください：

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// これで解放しても安全
free(counter);
```

---

## 制限事項

### 現在の制限

1. **i32とi64のみサポート** - 他の型に対するアトミック操作なし
2. **ポインタアトミックなし** - ポインタをアトミックにロード/ストアできない
3. **逐次一貫性のみ** - 弱いメモリ順序付けは利用不可
4. **アトミック浮動小数点なし** - 必要な場合は整数表現を使用

### プラットフォームに関する注意

- アトミック操作は内部でC11の`<stdatomic.h>`を使用
- POSIXスレッドをサポートするすべてのプラットフォームで利用可能
- モダンな64ビットシステムではロックフリーであることが保証

---

## 関連項目

- [非同期/並行処理](async-concurrency.md) - タスクの生成とチャネル
- [メモリ管理](../language-guide/memory.md) - ポインタとバッファの確保
- [メモリAPI](../reference/memory-api.md) - 確保関数
