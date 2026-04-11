# メモリAPIリファレンス

Hemlockのメモリ管理関数とポインタ型の完全なリファレンスです。

---

## 概要

Hemlockは明示的な割り当てと解放による**手動メモリ管理**を提供します。メモリは2つのポインタ型で管理されます：生ポインタ（`ptr`）と安全なバッファ（`buffer`）。

**主な原則：**
- 明示的な割り当てと解放
- ガベージコレクションなし
- ユーザーが`free()`を呼び出す責任がある
- スコープ/再代入の安全性のための内部参照カウント（下記参照）

### 内部参照カウント

ランタイムはスコープを通じてオブジェクトのライフタイムを管理するために、内部的に参照カウントを使用します。ほとんどのローカル変数では、クリーンアップは自動的です。

**自動（`free()`不要）：**
- 参照カウント型（buffer、array、object、string）のローカル変数はスコープ終了時に解放される
- 変数が再代入されると古い値が解放される
- コンテナが解放されるとコンテナ要素が解放される

**手動`free()`が必要：**
- `alloc()`からの生ポインタ - 常に
- スコープ終了前の早期クリーンアップ
- 長寿命/グローバルデータ

詳細は[メモリ管理ガイド](../language-guide/memory.md#内部参照カウント)を参照してください。

---

## ポインタ型

### ptr（生ポインタ）

**型：** `ptr`

**説明：** 境界チェックや追跡なしの生メモリアドレス。

**サイズ：** 8バイト

**使用ケース：**
- 低レベルメモリ操作
- FFI（外部関数インターフェース）
- 最大パフォーマンス（オーバーヘッドなし）

**安全性：** 安全でない - 境界チェックなし、ユーザーがライフタイムを追跡する必要がある

**例：**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer（安全なバッファ）

**型：** `buffer`

**説明：** 境界チェック付きの安全なポインタラッパー。

**構造：** ポインタ + 長さ + 容量 + 参照カウント

**プロパティ：**
- `.length` - バッファサイズ（i32）
- `.capacity` - 割り当て容量（i32）

**使用ケース：**
- ほとんどのメモリ割り当て
- 安全性が重要な場合
- 動的配列

**安全性：** インデックスアクセス時に境界チェック

**参照カウント：** バッファは内部的に参照カウントされます。スコープ終了時または変数再代入時に自動的に解放されます。早期クリーンアップや長寿命データには`free()`を使用してください。

**例：**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // 境界チェックあり
print(b.length);        // 64
free(b);
```

---

## メモリ割り当て関数

### alloc

生メモリを割り当てます。

**シグネチャ：**
```hemlock
alloc(size: i32): ptr
```

**パラメータ：**
- `size` - 割り当てるバイト数

**戻り値：** 割り当てられたメモリへのポインタ（`ptr`）

**例：**
```hemlock
let p = alloc(1024);        // 1KBを割り当て
memset(p, 0, 1024);         // ゼロで初期化
free(p);                    // 終了時に解放

// 構造体用に割り当て
let struct_size = 16;
let p2 = alloc(struct_size);
```

**動作：**
- 初期化されていないメモリを返す
- メモリは手動で解放する必要がある
- 割り当て失敗時は`null`を返す（呼び出し側でチェックが必要）

**関連項目：** より安全な代替として`buffer()`

---

### buffer

境界チェック付きの安全なバッファを割り当てます。

**シグネチャ：**
```hemlock
buffer(size: i32): buffer
```

**パラメータ：**
- `size` - バイト単位のバッファサイズ

**戻り値：** バッファオブジェクト

**例：**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// 境界チェック付きアクセス
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // エラー：範囲外

free(buf);
```

**プロパティ：**
- `.length` - 現在のサイズ（i32）
- `.capacity` - 割り当て容量（i32）

**動作：**
- メモリをゼロで初期化
- インデックスアクセス時に境界チェックを提供
- 割り当て失敗時は`null`を返す（呼び出し側でチェックが必要）
- 手動で解放する必要がある

---

### free

割り当てられたメモリを解放します。

**シグネチャ：**
```hemlock
free(ptr: ptr | buffer): null
```

**パラメータ：**
- `ptr` - 解放するポインタまたはバッファ

**戻り値：** `null`

**例：**
```hemlock
// 生ポインタを解放
let p = alloc(1024);
free(p);

// バッファを解放
let buf = buffer(256);
free(buf);
```

**動作：**
- `alloc()`または`buffer()`で割り当てられたメモリを解放
- 二重解放はクラッシュを引き起こす（ユーザーの責任で回避）
- 無効なポインタの解放は未定義動作

**重要：** 割り当てたら、解放する。自動クリーンアップなし。

---

### realloc

割り当てられたメモリのサイズを変更します。

**シグネチャ：**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**パラメータ：**
- `ptr` - サイズ変更するポインタ
- `new_size` - バイト単位の新しいサイズ

**戻り値：** サイズ変更されたメモリへのポインタ（アドレスが異なる場合がある）

**例：**
```hemlock
let p = alloc(100);
// ... メモリを使用 ...

// より多くの領域が必要
p = realloc(p, 200);        // 200バイトになった
// ... 拡張されたメモリを使用 ...

free(p);
```

**動作：**
- メモリを新しい場所に移動する場合がある
- 既存データを保持（古い/新しいサイズの最小まで）
- 成功したreallocの後は古いポインタは無効（返されたポインタを使用）
- new_sizeが小さい場合、データは切り詰められる
- 割り当て失敗時は`null`を返す（元のポインタは有効なまま）

**重要：** 常に`null`をチェックし、結果でポインタ変数を更新してください。

---

## メモリ操作

### memset

メモリをバイト値で埋めます。

**シグネチャ：**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**パラメータ：**
- `ptr` - メモリへのポインタ
- `byte` - 埋めるバイト値（0-255）
- `size` - 埋めるバイト数

**戻り値：** `null`

**例：**
```hemlock
let p = alloc(100);

// メモリをゼロクリア
memset(p, 0, 100);

// 特定の値で埋める
memset(p, 0xFF, 100);

// バッファを初期化
let buf = alloc(256);
memset(buf, 65, 256);       // 'A'で埋める

free(p);
free(buf);
```

**動作：**
- 範囲内の各バイトにバイト値を書き込む
- バイト値は8ビット（0-255）に切り詰められる
- 境界チェックなし（安全でない）

---

### memcpy

ソースからデスティネーションにメモリをコピーします。

**シグネチャ：**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**パラメータ：**
- `dest` - デスティネーションポインタ
- `src` - ソースポインタ
- `size` - コピーするバイト数

**戻り値：** `null`

**例：**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// ソースを初期化
memset(src, 65, 100);

// デスティネーションにコピー
memcpy(dest, src, 100);

// destはsrcと同じデータを含む

free(src);
free(dest);
```

**動作：**
- srcからdestへバイト単位でコピー
- 境界チェックなし（安全でない）
- オーバーラップする領域は未定義動作（慎重に使用）

---

## 型付きメモリ操作

### sizeof

型のバイト数を取得します。

**シグネチャ：**
```hemlock
sizeof(type): i32
```

**パラメータ：**
- `type` - 型識別子（例：`i32`、`f64`、`ptr`）

**戻り値：** バイト数（i32）

**型サイズ：**

| 型 | サイズ（バイト） |
|------|--------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**例：**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// 配列割り当てサイズを計算
let count = 100;
let total = sizeof(i32) * count; // 400バイト
```

**動作：**
- 不明な型には0を返す
- 型識別子と型文字列の両方を受け付ける

---

### talloc

型付き値の配列を割り当てます。

**シグネチャ：**
```hemlock
talloc(type, count: i32): ptr
```

**パラメータ：**
- `type` - 割り当てる型（例：`i32`、`f64`、`ptr`）
- `count` - 要素数（正の数である必要がある）

**戻り値：** 割り当てられた配列へのポインタ、割り当て失敗時は`null`

**例：**
```hemlock
let arr = talloc(i32, 100);      // 100個のi32の配列（400バイト）
let floats = talloc(f64, 50);    // 50個のf64の配列（400バイト）
let bytes = talloc(u8, 1024);    // 1024バイトの配列

// 常に割り当て失敗をチェック
if (arr == null) {
    panic("allocation failed");
}

// 割り当てられたメモリを使用
// ...

free(arr);
free(floats);
free(bytes);
```

**動作：**
- `sizeof(type) * count`バイトを割り当て
- 初期化されていないメモリを返す
- `free()`で手動解放が必要
- 割り当て失敗時は`null`を返す（呼び出し側でチェックが必要）
- countが正でない場合はパニック

---

## バッファプロパティ

### .length

バッファサイズを取得します。

**型：** `i32`

**アクセス：** 読み取り専用

**例：**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

バッファ容量を取得します。

**型：** `i32`

**アクセス：** 読み取り専用

**例：**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**注意：** 現在、`buffer()`で作成されたバッファでは`.length`と`.capacity`は同じです。

---

## バッファメソッド

### .slice

バッファメモリへのゼロコピービューを作成します。返されたビューは親バッファと同じ基盤メモリを共有します -- 元への変更はビューを通じて見え、その逆も同様です。

**シグネチャ：**
```hemlock
buffer.slice(start: i32, end?: i32): buffer
```

**パラメータ：**
- `start` - 開始バイトオフセット（0ベース、含む）。負の値は0にクランプ。
- `end` - 終了バイトオフセット（含まない）。省略時はデフォルトで`buffer.length`。バッファ長を超える値はクランプ。

**戻り値：** バッファビュー（ゼロコピー）

**例：**
```hemlock
let buf = buffer(10);
for (let i = 0; i < 10; i++) {
    buf[i] = i + 65;  // A=65, B=66, ...
}

// 基本的なスライス
let view = buf.slice(2, 5);
print(view.length);    // 3
print(view[0]);        // 67 (C)
print(view[1]);        // 68 (D)

// ゼロコピーの証明：元の変更がビューに反映
buf[3] = 90;           // D(68)をZ(90)に変更
print(view[1]);        // 90（親の変更を反映）

// 単一引数スライス（startから末尾まで）
let tail = buf.slice(7);
print(tail.length);    // 3

// チェーンされたスライス（スライスのスライス）
let inner = view.slice(1, 3);
print(inner.length);   // 2
```

**動作：**
- ゼロコピービューを返す -- データのためのメモリは割り当てられない
- ビューはルートバッファへの参照を保持（解放後使用を防止）
- チェーンされたスライスは中間ビューではなくルートオーナーを追跡
- 境界チェックはビューの範囲に対して実行
- ビューバッファは`free()`**できない** -- ルートバッファのみを解放すべき

---

## バッファ相互運用

すべての`ptr_read_*`、`ptr_write_*`、`ptr_deref_*`関数は`ptr`型と`buffer`型の両方を直接受け付けます：

```hemlock
let buf = buffer(8);
ptr_write_i32(buf, 42);          // buffer_ptr()不要で直接動作
let val = ptr_read_i32(buf);     // 42

// 生ポインタでも以前通り動作
let p = alloc(8);
ptr_write_i32(p, 99);
let pval = ptr_read_i32(p);     // 99
free(p);
```

これにより型付き読み書き操作ごとに`buffer_ptr()`を呼ぶ必要がなくなり、バッファベースのコードがより簡潔になります。

---

## 型付きバッファ読み書きメソッド

バッファはネットワークパケット、ファイルフォーマット、ワイヤプロトコルなどのバイナリデータ構造の構築とパースのための、エンディアン対応の型付き読み書きメソッドを提供します。これらのメソッドは境界チェックされ、範囲外アクセスは実行時エラーを発生させます。

### 書き込みメソッド

バイトオフセットに型付き値を書き込みます。`_le`と`_be`サフィックスはリトルエンディアンとビッグエンディアンのバイト順序を指定します。

```hemlock
let pkt = buffer(64);
let offset = 0;

// パケットヘッダを構築
pkt.write_u16_be(offset, 0x0800);    // EtherType: IPv4
offset += 2;
pkt.write_u8(offset, 0x45);          // Version + IHL
offset += 1;
pkt.write_u32_be(offset, 0xC0A80001); // ソースIP: 192.168.0.1
offset += 4;

// Float値
pkt.write_f32_le(offset, 3.14);
offset += 4;
pkt.write_f64_be(offset, 2.71828);
offset += 8;
```

**単一バイト書き込み**（`write_u8`、`write_i8`）はバイト順序が単一バイトでは無関係なため、エンディアンサフィックスがありません。

### 読み取りメソッド

バイトオフセットから型付き値を読み取ります。エンディアンサフィックスは書き込みメソッドに対応します。

```hemlock
let pkt = buffer(64);
// ... バッファにデータを充填 ...

// パケットヘッダをパース
let ether_type = pkt.read_u16_be(0);    // 0x0800
let version = pkt.read_u8(2);            // 0x45
let src_ip = pkt.read_u32_be(6);         // 0xC0A80001

// Float値を読み取り
let pi = pkt.read_f32_le(10);
let e = pkt.read_f64_be(14);
```

### バルク操作

```hemlock
let src = buffer(8);
for (let i = 0; i < 8; i++) { src[i] = i + 1; }

let dest = buffer(32);
dest.write_bytes(4, src);          // srcをdestのオフセット4にコピー

let chunk = dest.read_bytes(4, 8); // オフセット4から8バイトを読み取り
print(chunk[0]);                   // 1
```

### 境界チェック

すべての型付き読み書きメソッドは値全体がバッファ内に収まることを検証します。例えば`write_u32_be(offset, val)`は`offset + 4 <= buffer.length`をチェックします。

```hemlock
let buf = buffer(4);
buf.write_u32_be(0, 42);    // OK: 4バイトが収まる
// buf.write_u32_be(2, 42); // エラー: 末尾を超えて書き込み（offset 2 + 4 > 4）
```

### 使用ケース

- **ネットワークプロトコル：** TCP、UDP、DNS、カスタムパケットの構築/パース
- **バイナリファイルフォーマット：** 画像ヘッダ、アーカイブフォーマットの読み書き
- **ワイヤプロトコル：** 構造化バイナリメッセージのシリアライズ/デシリアライズ
- **FFIデータ交換：** Cライブラリ呼び出し用のバッファ準備

---

## 使用パターン

### 基本的な割り当てパターン

```hemlock
// 割り当て
let p = alloc(1024);
if (p == null) {
    panic("allocation failed");
}

// 使用
memset(p, 0, 1024);

// 解放
free(p);
```

### 安全なバッファパターン

```hemlock
// バッファを割り当て
let buf = buffer(256);
if (buf == null) {
    panic("buffer allocation failed");
}

// 境界チェック付きで使用
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// 解放
free(buf);
```

### 動的拡張パターン

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("allocation failed");
}

// ... メモリを使用 ...

// より多くの領域が必要 - 失敗をチェック
let new_p = realloc(p, 200);
if (new_p == null) {
    // 元のポインタはまだ有効、クリーンアップ
    free(p);
    panic("realloc failed");
}
p = new_p;
size = 200;

// ... 拡張されたメモリを使用 ...

free(p);
```

### メモリコピーパターン

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// コピーを作成
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## 安全性に関する考慮事項

**Hemlockのメモリ管理は設計上安全ではありません：**

### よくある落とし穴

**1. メモリリーク**
```hemlock
// 悪い例：メモリリーク
fn create_buffer() {
    let p = alloc(1024);
    return null;  // メモリがリーク！
}

// 良い例：適切なクリーンアップ
fn create_buffer() {
    let p = alloc(1024);
    // ... メモリを使用 ...
    free(p);
    return null;
}
```

**2. 解放後使用**
```hemlock
// 悪い例：解放後使用
let p = alloc(100);
free(p);
memset(p, 0, 100);  // クラッシュ：解放済みメモリを使用

// 良い例：解放後は使用しない
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// この後p2に触れない
```

**3. 二重解放**
```hemlock
// 悪い例：二重解放
let p = alloc(100);
free(p);
free(p);  // クラッシュ：二重解放

// 良い例：一度だけ解放
let p2 = alloc(100);
free(p2);
```

**4. バッファオーバーフロー（ptr）**
```hemlock
// 悪い例：ptrでのバッファオーバーフロー
let p = alloc(10);
memset(p, 65, 100);  // クラッシュ：割り当てを超えて書き込み

// 良い例：境界チェックにはbufferを使用
let buf = buffer(10);
// buf[100] = 65;  // エラー：境界チェックが失敗
```

**5. ダングリングポインタ**
```hemlock
// 悪い例：ダングリングポインタ
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // クラッシュ：p2はダングリング

// 良い例：所有権を慎重に追跡
let p = alloc(100);
// ... pを使用 ...
free(p);
// pへの他の参照を保持しない
```

**6. 割り当て失敗のチェック漏れ**
```hemlock
// 悪い例：nullをチェックしない
let p = alloc(1000000000);  // メモリ不足で失敗する可能性
memset(p, 0, 1000000000);   // クラッシュ：pがnull

// 良い例：常に割り当て結果をチェック
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("out of memory");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## 何をいつ使うか

### `buffer()`を使用する場合：
- 境界チェックが必要な場合
- 動的データを扱う場合
- 安全性が重要な場合
- Hemlockを学習中の場合

### `alloc()`を使用する場合：
- 最大パフォーマンスが必要な場合
- FFI/Cとのインターフェース
- 正確なメモリレイアウトを知っている場合
- エキスパートの場合

### `realloc()`を使用する場合：
- 割り当てを拡大/縮小する場合
- 動的配列
- データを保持する必要がある場合

---

## 完全な関数要約

| 関数 | シグネチャ | 戻り値 | 説明 |
|-----------|----------------------------------------|----------|----------------------------|
| `alloc`   | `(size: i32)`                          | `ptr`    | 生メモリを割り当て |
| `buffer`  | `(size: i32)`                          | `buffer` | 安全なバッファを割り当て |
| `free`    | `(ptr: ptr \| buffer)`                 | `null`   | メモリを解放 |
| `realloc` | `(ptr: ptr, new_size: i32)`            | `ptr`    | 割り当てサイズを変更 |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`     | `null`   | メモリを埋める |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`     | `null`   | メモリをコピー |
| `sizeof`  | `(type)`                               | `i32`    | 型のバイトサイズを取得 |
| `talloc`  | `(type, count: i32)`                   | `ptr`    | 型付き配列を割り当て |

### バッファメソッド

| メソッド | シグネチャ | 戻り値 | 説明 |
|-----------|----------------------------------------|----------|----------------------------|
| `.slice`  | `(start: i32, end?: i32)`             | `buffer` | バッファへのゼロコピービュー |
| `.write_u8` | `(offset: i32, value: u8)`          | `null`   | 符号なし8ビット整数を書き込み |
| `.write_i8` | `(offset: i32, value: i8)`          | `null`   | 符号付き8ビット整数を書き込み |
| `.write_u16_le` | `(offset: i32, value: u16)`    | `null`   | u16書き込み、リトルエンディアン |
| `.write_u16_be` | `(offset: i32, value: u16)`    | `null`   | u16書き込み、ビッグエンディアン |
| `.write_u32_le` | `(offset: i32, value: u32)`    | `null`   | u32書き込み、リトルエンディアン |
| `.write_u32_be` | `(offset: i32, value: u32)`    | `null`   | u32書き込み、ビッグエンディアン |
| `.write_u64_le` | `(offset: i32, value: u64)`    | `null`   | u64書き込み、リトルエンディアン |
| `.write_u64_be` | `(offset: i32, value: u64)`    | `null`   | u64書き込み、ビッグエンディアン |
| `.write_f32_le` | `(offset: i32, value: f32)`    | `null`   | f32書き込み、リトルエンディアン |
| `.write_f32_be` | `(offset: i32, value: f32)`    | `null`   | f32書き込み、ビッグエンディアン |
| `.write_f64_le` | `(offset: i32, value: f64)`    | `null`   | f64書き込み、リトルエンディアン |
| `.write_f64_be` | `(offset: i32, value: f64)`    | `null`   | f64書き込み、ビッグエンディアン |
| `.write_bytes` | `(offset: i32, src: buffer)`    | `null`   | ソースバッファからバイトをコピー |
| `.read_u8`  | `(offset: i32)`                      | `u8`     | 符号なし8ビット整数を読み取り |
| `.read_i8`  | `(offset: i32)`                      | `i8`     | 符号付き8ビット整数を読み取り |
| `.read_u16_le` | `(offset: i32)`                   | `u16`    | u16読み取り、リトルエンディアン |
| `.read_u16_be` | `(offset: i32)`                   | `u16`    | u16読み取り、ビッグエンディアン |
| `.read_u32_le` | `(offset: i32)`                   | `u32`    | u32読み取り、リトルエンディアン |
| `.read_u32_be` | `(offset: i32)`                   | `u32`    | u32読み取り、ビッグエンディアン |
| `.read_u64_le` | `(offset: i32)`                   | `u64`    | u64読み取り、リトルエンディアン |
| `.read_u64_be` | `(offset: i32)`                   | `u64`    | u64読み取り、ビッグエンディアン |
| `.read_f32_le` | `(offset: i32)`                   | `f32`    | f32読み取り、リトルエンディアン |
| `.read_f32_be` | `(offset: i32)`                   | `f32`    | f32読み取り、ビッグエンディアン |
| `.read_f64_le` | `(offset: i32)`                   | `f64`    | f64読み取り、リトルエンディアン |
| `.read_f64_be` | `(offset: i32)`                   | `f64`    | f64読み取り、ビッグエンディアン |
| `.read_bytes` | `(offset: i32, length: i32)`       | `buffer` | バイトを新しいバッファに読み取り |

---

## 関連項目

- [型システム](type-system.md) - ポインタとバッファ型
- [組み込み関数](builtins.md) - すべての組み込み関数
- [文字列API](string-api.md) - 文字列の`.to_bytes()`メソッド
