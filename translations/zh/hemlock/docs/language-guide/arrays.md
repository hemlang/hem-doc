# 数组

Hemlock 提供**动态数组**，具有全面的数据操作和处理方法。数组可以存储混合类型，并根据需要自动增长。

## 概述

```hemlock
// 数组字面量
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// 允许混合类型
let mixed = [1, "hello", true, null];

// 动态大小调整
arr.push(6);           // 自动增长
arr.push(7);
print(arr.length);     // 7
```

## 数组字面量

### 基本语法

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### 空数组

```hemlock
let arr = [];  // 空数组

// 稍后添加元素
arr.push(1);
arr.push(2);
arr.push(3);
```

### 混合类型

数组可以包含不同类型：

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3]（嵌套数组）
```

### 嵌套数组

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### 类型化数组

数组可以使用类型注解来强制元素类型：

```hemlock
// 类型化数组语法
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// 运行时类型检查
let valid: array<i32> = [1, 2, 3];       // 正确
let invalid: array<i32> = [1, "two", 3]; // 运行时错误：类型不匹配

// 嵌套类型化数组
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**类型注解行为：**
- 元素在添加到数组时进行类型检查
- 类型不匹配会导致运行时错误
- 没有类型注解时，数组接受混合类型

## 索引

### 读取元素

从零开始的索引访问：

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10（第一个元素）
print(arr[4]);  // 50（最后一个元素）

// 越界访问返回 null（不报错）
print(arr[10]);  // null
```

### 写入元素

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // 修改现有元素
arr[1] = 20;
print(arr);     // [10, 20, 3]

// 可以在超出当前长度的位置赋值（数组会增长）
arr[5] = 60;    // 创建 [10, 20, 3, null, null, 60]
```

### 负数索引

**不支持** - 只能使用正数索引：

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // 错误或未定义行为

// 使用 length 获取最后一个元素
print(arr[arr.length - 1]);  // 3
```

## 属性

### `.length` 属性

返回元素数量：

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// 空数组
let empty = [];
print(empty.length);  // 0

// 修改后
arr.push(6);
print(arr.length);  // 6
```

## 数组方法

Hemlock 提供 18 个数组方法用于全面的操作。

### 栈操作

**`push(value)`** - 在末尾添加元素：
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - 移除并返回最后一个元素：
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // 返回 5，arr 现在是 [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### 队列操作

**`shift()`** - 移除并返回第一个元素：
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // 返回 1，arr 现在是 [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - 在开头添加元素：
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### 插入和删除

**`insert(index, value)`** - 在指定索引处插入元素：
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // 在索引 2 处插入 3：[1, 2, 3, 4, 5]

arr.insert(0, 0);      // 在开头插入：[0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - 移除并返回指定索引处的元素：
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // 返回 3，arr 现在是 [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### 搜索操作

**`find(value)`** - 查找首次出现的位置：
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2（首次出现的索引）
let idx2 = arr.find(99);     // -1（未找到）

// 适用于任何类型
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - 检查数组是否包含某值：
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### 提取操作

**`slice(start, end)`** - 提取子数组（end 不包含在内）：
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]（索引 1, 2, 3）
let first = arr.slice(0, 2); // [1, 2]

// 原数组不变
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - 获取第一个元素（不移除）：
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1（不移除）
print(arr);                  // [1, 2, 3]（不变）
```

**`last()`** - 获取最后一个元素（不移除）：
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3（不移除）
print(arr);                  // [1, 2, 3]（不变）
```

### 转换操作

**`reverse()`** - 原地反转数组：
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1]（已修改）
```

**`join(delimiter)`** - 将元素连接成字符串：
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// 适用于混合类型
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - 与另一个数组连接：
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]（新数组）

// 原数组不变
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### 实用操作

**`clear()`** - 移除所有元素：
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## 方法链式调用

返回数组或值的方法可以进行链式调用：

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## 完整方法参考

| 方法 | 参数 | 返回值 | 是否修改原数组 | 描述 |
|--------|-----------|---------|---------|-------------|
| `push(value)` | any | void | 是 | 在末尾添加元素 |
| `pop()` | - | any | 是 | 移除并返回最后一个元素 |
| `shift()` | - | any | 是 | 移除并返回第一个元素 |
| `unshift(value)` | any | void | 是 | 在开头添加元素 |
| `insert(index, value)` | i32, any | void | 是 | 在指定索引处插入 |
| `remove(index)` | i32 | any | 是 | 移除并返回指定索引处的元素 |
| `find(value)` | any | i32 | 否 | 查找首次出现的位置（未找到返回 -1） |
| `contains(value)` | any | bool | 否 | 检查是否包含某值 |
| `slice(start, end)` | i32, i32 | array | 否 | 提取子数组（新数组） |
| `join(delimiter)` | string | string | 否 | 连接成字符串 |
| `concat(other)` | array | array | 否 | 连接数组（新数组） |
| `reverse()` | - | void | 是 | 原地反转 |
| `first()` | - | any | 否 | 获取第一个元素 |
| `last()` | - | any | 否 | 获取最后一个元素 |
| `clear()` | - | void | 是 | 移除所有元素 |
| `map(callback)` | fn | array | 否 | 转换每个元素 |
| `filter(predicate)` | fn | array | 否 | 选择匹配的元素 |
| `reduce(callback, initial)` | fn, any | any | 否 | 归约为单个值 |

## 实现细节

### 内存模型

- **堆分配** - 动态容量
- **自动增长** - 超出容量时翻倍
- **不自动收缩** - 容量不会减少
- **索引无边界检查** - 使用方法以确保安全

### 容量管理

```hemlock
let arr = [];  // 初始容量：0

arr.push(1);   // 增长到容量 1
arr.push(2);   // 增长到容量 2
arr.push(3);   // 增长到容量 4（翻倍）
arr.push(4);   // 仍然是容量 4
arr.push(5);   // 增长到容量 8（翻倍）
```

### 值比较

`find()` 和 `contains()` 使用值相等比较：

```hemlock
// 基本类型：按值比较
let arr = [1, 2, 3];
arr.contains(2);  // true

// 字符串：按值比较
let words = ["hello", "world"];
words.contains("hello");  // true

// 对象：按引用比较
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true（相同引用）
arr2.contains(obj2);  // false（不同引用）
```

## 常见模式

### 函数式操作（map/filter/reduce）

数组内置 `map`、`filter` 和 `reduce` 方法：

```hemlock
// map - 转换每个元素
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - 选择匹配的元素
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - 归约为单个值
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// 链式调用函数式操作
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### 模式：数组作为栈

```hemlock
let stack = [];

// 压入栈
stack.push(1);
stack.push(2);
stack.push(3);

// 弹出栈
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### 模式：数组作为队列

```hemlock
let queue = [];

// 入队（添加到末尾）
queue.push(1);
queue.push(2);
queue.push(3);

// 出队（从前面移除）
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## 最佳实践

1. **使用方法而非直接索引** - 边界检查和代码清晰度
2. **检查边界** - 直接索引不进行边界检查
3. **优先使用不可变操作** - 使用 `slice()` 和 `concat()` 而非修改原数组
4. **预先初始化容量** - 如果知道大小（目前不支持）
5. **使用 `contains()` 检查成员** - 比手动循环更清晰
6. **链式调用方法** - 比嵌套调用更易读

## 常见陷阱

### 陷阱：直接索引越界

```hemlock
let arr = [1, 2, 3];

// 无边界检查！
arr[10] = 99;  // 创建带有 null 的稀疏数组
print(arr.length);  // 11（不是 3！）

// 更好的做法：使用 push() 或检查长度
if (arr.length <= 10) {
    arr.push(99);
}
```

### 陷阱：修改与新建数组

```hemlock
let arr = [1, 2, 3];

// 修改原数组
arr.reverse();
print(arr);  // [3, 2, 1]

// 返回新数组
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1]（不变）
print(sub);  // [3, 2]
```

### 陷阱：引用相等

```hemlock
let obj = { x: 10 };
let arr = [obj];

// 相同引用：true
arr.contains(obj);  // true

// 不同引用：false
arr.contains({ x: 10 });  // false（不同对象）
```

### 陷阱：长期存活的数组

```hemlock
// 局部作用域中的数组会自动释放，但全局/长期存活的数组需要注意
let global_cache = [];  // 模块级别，持续到程序退出

fn add_to_cache(item) {
    global_cache.push(item);  // 无限增长
}

// 对于长期存活的数据，考虑：
// - 定期清空数组：global_cache.clear();
// - 提前释放：free(global_cache);
```

## 示例

### 示例：数组统计

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### 示例：数组去重

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### 示例：数组分块

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### 示例：数组扁平化

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // 嵌套数组 - 扁平化它
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### 示例：排序（冒泡排序）

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // 交换
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // 原地修改
print(numbers);  // [1, 2, 5, 8, 9]
```

## 限制

当前限制：

- **索引无边界检查** - 直接访问不检查边界
- **对象使用引用相等** - `find()` 和 `contains()` 使用引用比较
- **无数组解构** - 不支持 `let [a, b] = arr` 语法
- **无展开运算符** - 不支持 `[...arr1, ...arr2]` 语法

**注意：** 数组使用引用计数，作用域退出时自动释放。详见 [内存管理](memory.md#internal-reference-counting)。

## 相关主题

- [字符串](strings.md) - 字符串方法与数组方法类似
- [对象](objects.md) - 数组也是类对象的
- [函数](functions.md) - 数组与高阶函数
- [控制流](control-flow.md) - 遍历数组

## 另请参阅

- **动态大小**：数组通过容量翻倍自动增长
- **方法**：18 个全面的操作方法，包括 map/filter/reduce
- **内存**：详见 [内存](memory.md) 了解数组分配细节
