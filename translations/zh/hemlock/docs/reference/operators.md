# 运算符参考

Hemlock 中所有运算符的完整参考，包括优先级、结合性和行为。

---

## 概述

Hemlock 提供 C 风格的运算符，具有明确的优先级规则。所有运算符遵循严格的类型规则，在适用时自动进行类型提升。

---

## 算术运算符

### 二元算术

| 运算符 | 名称   | 示例       | 描述           |
|--------|--------|------------|----------------|
| `+`    | 加法   | `a + b`    | 将两个值相加   |
| `-`    | 减法   | `a - b`    | 从 a 中减去 b  |
| `*`    | 乘法   | `a * b`    | 将两个值相乘   |
| `/`    | 除法   | `a / b`    | 将 a 除以 b    |

**类型提升：**
结果遵循类型提升规则（参见 [类型系统](type-system.md#type-promotion-rules)）。

**示例：**
```hemlock
let a = 10 + 5;        // 15 (i32)
let b = 10 - 3;        // 7 (i32)
let c = 4 * 5;         // 20 (i32)
let d = 20 / 4;        // 5 (i32)

// Float division
let e = 10.0 / 3.0;    // 3.333... (f64)

// Mixed types
let f: u8 = 10;
let g: i32 = 20;
let h = f + g;         // 30 (i32, promoted)
```

**除以零：**
- 整数除以零：运行时错误
- 浮点数除以零：返回 `inf` 或 `-inf`

---

### 一元算术

| 运算符 | 名称 | 示例    | 描述         |
|--------|------|---------|--------------|
| `-`    | 取负 | `-a`    | 对值取负     |
| `+`    | 正号 | `+a`    | 恒等（无操作）|

**示例：**
```hemlock
let a = 5;
let b = -a;            // -5
let c = +a;            // 5 (no change)

let x = -3.14;         // -3.14
```

---

## 比较运算符

| 运算符 | 名称       | 示例       | 返回值   |
|--------|------------|------------|----------|
| `==`   | 等于       | `a == b`   | `bool`   |
| `!=`   | 不等于     | `a != b`   | `bool`   |
| `<`    | 小于       | `a < b`    | `bool`   |
| `>`    | 大于       | `a > b`    | `bool`   |
| `<=`   | 小于或等于 | `a <= b`   | `bool`   |
| `>=`   | 大于或等于 | `a >= b`   | `bool`   |

**类型提升：**
操作数在比较前会进行提升。

**示例：**
```hemlock
print(5 == 5);         // true
print(10 != 5);        // true
print(3 < 7);          // true
print(10 > 5);         // true
print(5 <= 5);         // true
print(10 >= 5);        // true

// String comparison
print("hello" == "hello");  // true
print("abc" < "def");       // true (lexicographic)

// Mixed types
let a: u8 = 10;
let b: i32 = 10;
print(a == b);         // true (promoted to i32)
```

---

## 逻辑运算符

| 运算符 | 名称     | 示例         | 描述                 |
|--------|----------|--------------|----------------------|
| `&&`   | 逻辑与   | `a && b`     | 两者都为真时返回真   |
| `||`   | 逻辑或   | `a || b`     | 任一为真时返回真     |
| `!`    | 逻辑非   | `!a`         | 对布尔值取反         |

**短路求值：**
- `&&` - 遇到第一个假值时停止
- `||` - 遇到第一个真值时停止

**示例：**
```hemlock
let a = true;
let b = false;

print(a && b);         // false
print(a || b);         // true
print(!a);             // false
print(!b);             // true

// Short-circuit
if (x != 0 && (10 / x) > 2) {
    print("safe");
}

if (x == 0 || (10 / x) > 2) {
    print("safe");
}
```

---

## 位运算符

**限制：** 仅适用于整数类型 (i8-i64, u8-u64)

### 二元位运算

| 运算符 | 名称     | 示例       | 描述               |
|--------|----------|------------|--------------------|
| `&`    | 按位与   | `a & b`    | 对每一位进行与运算 |
| `|`    | 按位或   | `a | b`    | 对每一位进行或运算 |
| `^`    | 按位异或 | `a ^ b`    | 对每一位进行异或运算 |
| `<<`   | 左移     | `a << b`   | 向左移动 b 位      |
| `>>`   | 右移     | `a >> b`   | 向右移动 b 位      |

**类型保持：**
结果类型与操作数类型匹配（经过类型提升）。

**示例：**
```hemlock
let a = 12;  // 1100 in binary
let b = 10;  // 1010 in binary

print(a & b);          // 8  (1000)
print(a | b);          // 14 (1110)
print(a ^ b);          // 6  (0110)
print(a << 2);         // 48 (110000)
print(a >> 1);         // 6  (110)
```

**无符号示例：**
```hemlock
let c: u8 = 15;        // 00001111
let d: u8 = 7;         // 00000111

print(c & d);          // 7  (00000111)
print(c | d);          // 15 (00001111)
print(c ^ d);          // 8  (00001000)
```

**右移行为：**
- 有符号类型：算术移位（符号扩展）
- 无符号类型：逻辑移位（零填充）

---

### 一元位运算

| 运算符 | 名称     | 示例    | 描述           |
|--------|----------|---------|----------------|
| `~`    | 按位取反 | `~a`    | 翻转所有位     |

**示例：**
```hemlock
let a = 12;            // 00001100 (i32)
print(~a);             // -13 (two's complement)

let b: u8 = 15;        // 00001111
print(~b);             // 240 (11110000)
```

---

## 字符串运算符

### 连接

| 运算符 | 名称   | 示例       | 描述       |
|--------|--------|------------|------------|
| `+`    | 连接   | `a + b`    | 连接字符串 |

**示例：**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"

// String + rune
let greeting = "Hello" + '!';      // "Hello!"

// Rune + string
let prefix = '>' + " Message";     // "> Message"
```

---

## 赋值运算符

### 基本赋值

| 运算符 | 名称   | 示例       | 描述           |
|--------|--------|------------|----------------|
| `=`    | 赋值   | `a = b`    | 将值赋给变量   |

**示例：**
```hemlock
let x = 10;
x = 20;

let arr = [1, 2, 3];
arr[0] = 99;

let obj = { x: 10 };
obj.x = 20;
```

### 复合赋值

#### 算术复合赋值

| 运算符 | 名称       | 示例       | 等价于             |
|--------|------------|------------|--------------------|
| `+=`   | 加法赋值   | `a += b`   | `a = a + b`        |
| `-=`   | 减法赋值   | `a -= b`   | `a = a - b`        |
| `*=`   | 乘法赋值   | `a *= b`   | `a = a * b`        |
| `/=`   | 除法赋值   | `a /= b`   | `a = a / b`        |
| `%=`   | 取模赋值   | `a %= b`   | `a = a % b`        |

**示例：**
```hemlock
let x = 10;
x += 5;      // x is now 15
x -= 3;      // x is now 12
x *= 2;      // x is now 24
x /= 4;      // x is now 6

let count = 0;
count += 1;  // Increment by 1
```

#### 位运算复合赋值

| 运算符 | 名称           | 示例        | 等价于              |
|--------|----------------|-------------|---------------------|
| `&=`   | 按位与赋值     | `a &= b`    | `a = a & b`         |
| `\|=`  | 按位或赋值     | `a \|= b`   | `a = a \| b`        |
| `^=`   | 按位异或赋值   | `a ^= b`    | `a = a ^ b`         |
| `<<=`  | 左移赋值       | `a <<= b`   | `a = a << b`        |
| `>>=`  | 右移赋值       | `a >>= b`   | `a = a >> b`        |

**示例：**
```hemlock
let flags = 0b1111;
flags &= 0b0011;   // flags is now 0b0011 (mask off upper bits)
flags |= 0b1000;   // flags is now 0b1011 (set a bit)
flags ^= 0b0001;   // flags is now 0b1010 (toggle a bit)

let x = 1;
x <<= 4;           // x is now 16 (shift left by 4)
x >>= 2;           // x is now 4 (shift right by 2)
```

### 自增/自减

| 运算符 | 名称   | 示例    | 描述                 |
|--------|--------|---------|----------------------|
| `++`   | 自增   | `a++`   | 加 1（后缀）         |
| `--`   | 自减   | `a--`   | 减 1（后缀）         |

**示例：**
```hemlock
let i = 0;
i++;         // i is now 1
i++;         // i is now 2
i--;         // i is now 1

// Common in loops
for (let j = 0; j < 10; j++) {
    print(j);
}
```

**注意：** `++` 和 `--` 都是后缀运算符（在自增/自减之前返回值）

---

## 空值安全运算符

### 空值合并 (`??`)

如果左操作数不为空则返回左操作数，否则返回右操作数。

| 运算符 | 名称       | 示例         | 描述                       |
|--------|------------|--------------|----------------------------|
| `??`   | 空值合并   | `a ?? b`     | 如果 a 非空返回 a，否则返回 b |

**示例：**
```hemlock
let name = null;
let display = name ?? "Anonymous";  // "Anonymous"

let value = 42;
let result = value ?? 0;            // 42

// Chaining
let a = null;
let b = null;
let c = "found";
let result2 = a ?? b ?? c;          // "found"

// With function calls
fn get_config() { return null; }
let config = get_config() ?? { default: true };
```

---

### 可选链 (`?.`)

安全地访问可能为空的值的属性或调用方法。

| 运算符 | 名称       | 示例           | 描述                             |
|--------|------------|----------------|----------------------------------|
| `?.`   | 可选链     | `a?.b`         | 如果 a 非空返回 a.b，否则返回 null |
| `?.[`  | 可选索引   | `a?.[0]`       | 如果 a 非空返回 a[0]，否则返回 null |
| `?.(`  | 可选调用   | `a?.()`        | 如果 a 非空调用 a()，否则返回 null |

**示例：**
```hemlock
let user = null;
let name = user?.name;              // null (no error)

let person = { name: "Alice", address: null };
let city = person?.address?.city;   // null (safe navigation)

// With arrays
let arr = null;
let first = arr?.[0];               // null

let items = [1, 2, 3];
let second = items?.[1];            // 2

// With method calls
let obj = { greet: fn() { return "Hello"; } };
let greeting = obj?.greet?.();      // "Hello"

let empty = null;
let result = empty?.method?.();     // null
```

**行为：**
- 如果左操作数为空，整个表达式短路返回 null
- 如果左操作数非空，正常进行访问
- 可以链接用于深层属性访问

---

## 成员访问运算符

### 点运算符

| 运算符 | 名称       | 示例         | 描述           |
|--------|------------|--------------|----------------|
| `.`    | 成员访问   | `obj.field`  | 访问对象字段   |
| `.`    | 属性访问   | `arr.length` | 访问属性       |

**示例：**
```hemlock
// Object field access
let person = { name: "Alice", age: 30 };
print(person.name);        // "Alice"

// Array property
let arr = [1, 2, 3];
print(arr.length);         // 3

// String property
let s = "hello";
print(s.length);           // 5

// Method call
let result = s.to_upper(); // "HELLO"
```

---

### 索引运算符

| 运算符 | 名称   | 示例      | 描述       |
|--------|--------|-----------|------------|
| `[]`   | 索引   | `arr[i]`  | 访问元素   |

**示例：**
```hemlock
// Array indexing
let arr = [10, 20, 30];
print(arr[0]);             // 10
arr[1] = 99;

// String indexing (returns rune)
let s = "hello";
print(s[0]);               // 'h'
s[0] = 'H';                // "Hello"

// Buffer indexing
let buf = buffer(10);
buf[0] = 65;
print(buf[0]);             // 65
```

---

## 函数调用运算符

| 运算符 | 名称       | 示例         | 描述       |
|--------|------------|--------------|------------|
| `()`   | 函数调用   | `f(a, b)`    | 调用函数   |

**示例：**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(5, 3);    // 8

// Method call
let s = "hello";
let upper = s.to_upper();  // "HELLO"

// Builtin call
print("message");
```

---

## 运算符优先级

运算符按从高到低的优先级排列：

| 优先级 | 运算符                       | 描述                           | 结合性     |
|--------|------------------------------|--------------------------------|------------|
| 1      | `()` `[]` `.` `?.`           | 调用、索引、成员访问、可选链   | 从左到右   |
| 2      | `++` `--`                    | 后缀自增/自减                  | 从左到右   |
| 3      | `!` `~` `-` (一元) `+` (一元)| 逻辑非、按位取反、取负         | 从右到左   |
| 4      | `*` `/` `%`                  | 乘法、除法、取模               | 从左到右   |
| 5      | `+` `-`                      | 加法、减法                     | 从左到右   |
| 6      | `<<` `>>`                    | 位移                           | 从左到右   |
| 7      | `<` `<=` `>` `>=`            | 关系运算                       | 从左到右   |
| 8      | `==` `!=`                    | 相等运算                       | 从左到右   |
| 9      | `&`                          | 按位与                         | 从左到右   |
| 10     | `^`                          | 按位异或                       | 从左到右   |
| 11     | `|`                          | 按位或                         | 从左到右   |
| 12     | `&&`                         | 逻辑与                         | 从左到右   |
| 13     | `||`                         | 逻辑或                         | 从左到右   |
| 14     | `??`                         | 空值合并                       | 从左到右   |
| 15     | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | 赋值 | 从右到左   |

---

## 优先级示例

### 示例 1：算术和比较
```hemlock
let result = 5 + 3 * 2;
// Evaluated as: 5 + (3 * 2) = 11
// Multiplication has higher precedence than addition

let cmp = 10 > 5 + 3;
// Evaluated as: 10 > (5 + 3) = true
// Addition has higher precedence than comparison
```

### 示例 2：位运算符
```hemlock
let result1 = 12 | 10 & 8;
// Evaluated as: 12 | (10 & 8) = 12 | 8 = 12
// & has higher precedence than |

let result2 = 8 | 1 << 2;
// Evaluated as: 8 | (1 << 2) = 8 | 4 = 12
// Shift has higher precedence than bitwise OR

// Use parentheses for clarity
let result3 = (5 & 3) | (2 << 1);
// Evaluated as: 1 | 4 = 5
```

### 示例 3：逻辑运算符
```hemlock
let result = true || false && false;
// Evaluated as: true || (false && false) = true
// && has higher precedence than ||

let cmp = 5 < 10 && 10 < 20;
// Evaluated as: (5 < 10) && (10 < 20) = true
// Comparison has higher precedence than &&
```

### 示例 4：使用括号
```hemlock
// Without parentheses
let a = 2 + 3 * 4;        // 14

// With parentheses
let b = (2 + 3) * 4;      // 20

// Complex expression
let c = (a + b) * (a - b);
```

---

## 类型特定的运算符行为

### 除法（始终返回浮点数）

`/` 运算符**始终返回浮点数** (f64)，无论操作数类型：

```hemlock
print(10 / 3);             // 3.333... (f64)
print(5 / 2);              // 2.5 (f64)
print(10.0 / 4.0);         // 2.5 (f64)
print(-7 / 3);             // -2.333... (f64)
```

这可以防止常见的意外整数截断错误。

### 地板除法 (div / divi)

对于地板除法（类似其他语言中的整数除法），使用 `div()` 和 `divi()` 函数：

```hemlock
// div(a, b) - floor division returning float
print(div(5, 2));          // 2 (f64)
print(div(-7, 3));         // -3 (f64)  -- floors toward -infinity

// divi(a, b) - floor division returning integer
print(divi(5, 2));         // 2 (i64)
print(divi(-7, 3));        // -3 (i64)
print(typeof(divi(5, 2))); // i64
```

**返回整数的数学函数：**
对于其他返回整数的舍入操作：

```hemlock
print(floori(3.7));        // 3 (i64)
print(ceili(3.2));         // 4 (i64)
print(roundi(3.5));        // 4 (i64)
print(trunci(3.9));        // 3 (i64)

// These can be used directly as array indices
let arr = [10, 20, 30, 40];
print(arr[floori(1.9)]);   // 20 (index 1)
```

### 字符串比较

字符串按字典序比较：

```hemlock
print("abc" < "def");      // true
print("apple" > "banana"); // false
print("hello" == "hello"); // true
```

### 空值比较

```hemlock
let x = null;

print(x == null);          // true
print(x != null);          // false
```

### 类型错误

某些操作不允许在不兼容的类型之间进行：

```hemlock
// ERROR: Cannot use bitwise operators on floats
let x = 3.14 & 2.71;

// ERROR: Cannot use bitwise operators on strings
let y = "hello" & "world";

// OK: Type promotion for arithmetic
let a: u8 = 10;
let b: i32 = 20;
let c = a + b;             // i32 (promoted)
```

---

## 另请参阅

- [类型系统](type-system.md) - 类型提升和转换规则
- [内置函数](builtins.md) - 内置操作
- [字符串 API](string-api.md) - 字符串连接和方法
