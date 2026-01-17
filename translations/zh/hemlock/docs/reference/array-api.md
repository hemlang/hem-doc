# 数组 API 参考

Hemlock 数组类型及其全部 18 个数组方法的完整参考文档。

---

## 概述

Hemlock 中的数组是**动态的、堆分配的**序列，可以存储混合类型。它们提供了全面的数据操作和处理方法。

**主要特性：**
- 动态大小（自动增长）
- 从零开始索引
- 允许混合类型
- 18 个内置方法
- 堆分配并跟踪容量

---

## 数组类型

**类型：** `array`

**属性：**
- `.length` - 元素数量 (i32)

**字面量语法：** 方括号 `[elem1, elem2, ...]`

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// 混合类型
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// 空数组
let empty = [];
print(empty.length);   // 0
```

---

## 索引

数组支持使用 `[]` 进行从零开始的索引：

**读取访问：**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**写入访问：**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**注意：** 直接索引不进行边界检查。请使用方法以确保安全。

---

## 数组属性

### .length

获取数组中的元素数量。

**类型：** `i32`

**示例：**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// 长度动态变化
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## 数组方法

### 栈操作

#### push

将元素添加到数组末尾。

**签名：**
```hemlock
array.push(value: any): null
```

**参数：**
- `value` - 要添加的元素

**返回值：** `null`

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

移除并返回最后一个元素。

**签名：**
```hemlock
array.pop(): any
```

**返回值：** 最后一个元素（从数组中移除）

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**错误：** 如果数组为空则抛出运行时错误。

---

### 队列操作

#### shift

移除并返回第一个元素。

**签名：**
```hemlock
array.shift(): any
```

**返回值：** 第一个元素（从数组中移除）

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**错误：** 如果数组为空则抛出运行时错误。

---

#### unshift

将元素添加到数组开头。

**签名：**
```hemlock
array.unshift(value: any): null
```

**参数：**
- `value` - 要添加的元素

**返回值：** `null`

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### 插入与删除

#### insert

在指定索引位置插入元素。

**签名：**
```hemlock
array.insert(index: i32, value: any): null
```

**参数：**
- `index` - 插入位置（从 0 开始）
- `value` - 要插入的元素

**返回值：** `null`

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// 在末尾插入
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**行为：** 将索引位置及其后的元素向右移动。

---

#### remove

移除并返回指定索引位置的元素。

**签名：**
```hemlock
array.remove(index: i32): any
```

**参数：**
- `index` - 要移除的位置（从 0 开始）

**返回值：** 被移除的元素

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**行为：** 将索引位置后的元素向左移动。

**错误：** 如果索引超出边界则抛出运行时错误。

---

### 搜索与查找

#### find

查找值的第一次出现位置。

**签名：**
```hemlock
array.find(value: any): i32
```

**参数：**
- `value` - 要搜索的值

**返回值：** 第一次出现的索引，如果未找到则返回 `-1`

**示例：**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1（未找到）

// 查找第一个重复项
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1（第一次出现）
```

**比较方式：** 对基本类型和字符串使用值相等比较。

---

#### contains

检查数组是否包含某个值。

**签名：**
```hemlock
array.contains(value: any): bool
```

**参数：**
- `value` - 要搜索的值

**返回值：** 如果找到返回 `true`，否则返回 `false`

**示例：**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// 对字符串也适用
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### 切片与提取

#### slice

按范围提取子数组（结束位置不包含）。

**签名：**
```hemlock
array.slice(start: i32, end: i32): array
```

**参数：**
- `start` - 起始索引（从 0 开始，包含）
- `end` - 结束索引（不包含）

**返回值：** 包含 [start, end) 范围内元素的新数组

**是否修改原数组：** 否（返回新数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// 空切片
let empty = arr.slice(2, 2); // []
```

---

#### first

获取第一个元素但不移除。

**签名：**
```hemlock
array.first(): any
```

**返回值：** 第一个元素

**是否修改原数组：** 否

**示例：**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3]（未改变）
```

**错误：** 如果数组为空则抛出运行时错误。

---

#### last

获取最后一个元素但不移除。

**签名：**
```hemlock
array.last(): any
```

**返回值：** 最后一个元素

**是否修改原数组：** 否

**示例：**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3]（未改变）
```

**错误：** 如果数组为空则抛出运行时错误。

---

### 数组操作

#### reverse

原地反转数组。

**签名：**
```hemlock
array.reverse(): null
```

**返回值：** `null`

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

移除数组中的所有元素。

**签名：**
```hemlock
array.clear(): null
```

**返回值：** `null`

**是否修改原数组：** 是（原地修改数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### 数组合并

#### concat

与另一个数组连接。

**签名：**
```hemlock
array.concat(other: array): array
```

**参数：**
- `other` - 要连接的数组

**返回值：** 包含两个数组元素的新数组

**是否修改原数组：** 否（返回新数组）

**示例：**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3]（未改变）
print(b);                    // [4, 5, 6]（未改变）

// 链式连接
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### 函数式操作

#### map

使用回调函数转换每个元素。

**签名：**
```hemlock
array.map(callback: fn): array
```

**参数：**
- `callback` - 接收一个元素并返回转换后值的函数

**返回值：** 包含转换后元素的新数组

**是否修改原数组：** 否（返回新数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

选择匹配谓词的元素。

**签名：**
```hemlock
array.filter(predicate: fn): array
```

**参数：**
- `predicate` - 接收一个元素并返回 bool 的函数

**返回值：** 包含谓词返回 true 的元素的新数组

**是否修改原数组：** 否（返回新数组）

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

使用累加器将数组归约为单个值。

**签名：**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**参数：**
- `callback` - 接收 (累加器, 元素) 并返回新累加器的函数
- `initial` - 累加器的初始值

**返回值：** 最终累加值

**是否修改原数组：** 否

**示例：**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// 查找最大值
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### 字符串转换

#### join

使用分隔符将元素连接成字符串。

**签名：**
```hemlock
array.join(delimiter: string): string
```

**参数：**
- `delimiter` - 放置在元素之间的字符串

**返回值：** 连接所有元素的字符串

**示例：**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// 对混合类型也适用
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// 空分隔符
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**行为：** 自动将所有元素转换为字符串。

---

## 方法链式调用

数组方法可以链式调用以实现简洁的操作：

**示例：**
```hemlock
// 链式调用 slice 和 join
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// 链式调用 concat 和 slice
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// 复杂链式调用
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## 完整方法总结

### 修改原数组的方法

原地修改数组的方法：

| 方法       | 签名                       | 返回值    | 描述                           |
|------------|----------------------------|-----------|--------------------------------|
| `push`     | `(value: any)`             | `null`    | 添加到末尾                     |
| `pop`      | `()`                       | `any`     | 从末尾移除                     |
| `shift`    | `()`                       | `any`     | 从开头移除                     |
| `unshift`  | `(value: any)`             | `null`    | 添加到开头                     |
| `insert`   | `(index: i32, value: any)` | `null`    | 在索引位置插入                 |
| `remove`   | `(index: i32)`             | `any`     | 在索引位置移除                 |
| `reverse`  | `()`                       | `null`    | 原地反转                       |
| `clear`    | `()`                       | `null`    | 移除所有元素                   |

### 不修改原数组的方法

返回新值而不修改原数组的方法：

| 方法       | 签名                       | 返回值    | 描述                           |
|------------|----------------------------|-----------|--------------------------------|
| `find`     | `(value: any)`             | `i32`     | 查找第一次出现位置             |
| `contains` | `(value: any)`             | `bool`    | 检查是否包含值                 |
| `slice`    | `(start: i32, end: i32)`   | `array`   | 提取子数组                     |
| `first`    | `()`                       | `any`     | 获取第一个元素                 |
| `last`     | `()`                       | `any`     | 获取最后一个元素               |
| `concat`   | `(other: array)`           | `array`   | 连接数组                       |
| `join`     | `(delimiter: string)`      | `string`  | 将元素连接成字符串             |
| `map`      | `(callback: fn)`           | `array`   | 转换每个元素                   |
| `filter`   | `(predicate: fn)`          | `array`   | 选择匹配的元素                 |
| `reduce`   | `(callback: fn, initial: any)` | `any` | 归约为单个值                   |

---

## 使用模式

### 栈用法

```hemlock
let stack = [];

// 压栈
stack.push(1);
stack.push(2);
stack.push(3);

// 弹栈
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### 队列用法

```hemlock
let queue = [];

// 入队
queue.push(1);
queue.push(2);
queue.push(3);

// 出队
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### 数组转换

```hemlock
// 过滤（手动方式）
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// 映射（手动方式）
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### 构建数组

```hemlock
let arr = [];

// 使用循环构建数组
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## 实现细节

**容量管理：**
- 数组在需要时自动增长
- 超出容量时容量翻倍
- 无手动容量控制

**值比较：**
- `find()` 和 `contains()` 使用值相等比较
- 对基本类型和字符串正确工作
- 对象/数组按引用比较

**内存：**
- 堆分配
- 无自动释放（手动内存管理）
- 直接索引访问无边界检查

---

## 另请参阅

- [类型系统](type-system.md) - 数组类型详情
- [字符串 API](string-api.md) - 字符串 join() 结果
- [运算符](operators.md) - 数组索引运算符
