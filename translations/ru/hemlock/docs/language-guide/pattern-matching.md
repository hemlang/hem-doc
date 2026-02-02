# Сопоставление с образцом

Hemlock предоставляет мощное сопоставление с образцом через выражения `match`, предлагая лаконичный способ деструктурировать значения, проверять типы и обрабатывать множественные случаи.

## Базовый синтаксис

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

Выражения match вычисляют `value` относительно каждого паттерна по порядку, возвращая результат выражения первой совпавшей ветки.

## Типы паттернов

### Литеральные паттерны

Сопоставление с точными значениями:

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "one",
    42 => "the answer",
    _ => "other"
};
print(msg);  // "the answer"
```

Поддерживаемые литералы:
- **Целые числа**: `0`, `42`, `-5`
- **Числа с плавающей точкой**: `3.14`, `-0.5`
- **Строки**: `"hello"`, `"world"`
- **Булевы**: `true`, `false`
- **Null**: `null`

### Паттерн-заполнитель (`_`)

Совпадает с любым значением без связывания:

```hemlock
let x = "anything";
let result = match (x) {
    "specific" => "found it",
    _ => "wildcard matched"
};
```

### Паттерны связывания переменных

Связывание совпавшего значения с переменной:

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "value is " + n  // n связывается со 100
};
print(result);  // "value is 100"
```

### Паттерны ИЛИ (`|`)

Сопоставление с несколькими альтернативами:

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "small",
    4 | 5 | 6 => "medium",
    _ => "large"
};

// Работает и со строками
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "exiting",
    "help" | "h" | "?" => "showing help",
    _ => "unknown"
};
```

### Guard-выражения (`if`)

Добавление условий к паттернам:

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negative",
    n if n == 0 => "zero",
    n if n < 10 => "small",
    n if n < 100 => "medium",
    n => "large: " + n
};
print(category);  // "medium"

// Сложные guards
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "even and greater than 10",
    n if n % 2 == 0 => "even",
    n => "odd"
};
```

### Типовые паттерны

Проверка и связывание на основе типа:

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "integer: " + num,
    str: string => "string: " + str,
    flag: bool => "boolean: " + flag,
    _ => "other type"
};
print(desc);  // "integer: 42"
```

Поддерживаемые типы: `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Деструктурирующие паттерны

### Деструктуризация объектов

Извлечение полей из объектов:

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "point at " + x + "," + y
};
print(result);  // "point at 10,20"

// С литеральными значениями полей
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origin",
    { x: 0, y } => "on y-axis at " + y,
    { x, y: 0 } => "on x-axis at " + x,
    { x, y } => "point at " + x + "," + y
};
print(name);  // "origin"
```

### Деструктуризация массивов

Сопоставление структуры и элементов массива:

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "empty",
    [x] => "single: " + x,
    [x, y] => "pair: " + x + "," + y,
    [x, y, z] => "triple: " + x + "," + y + "," + z,
    _ => "many elements"
};
print(desc);  // "triple: 1,2,3"

// С литеральными значениями
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "both zero",
    [1, x] => "starts with 1, second is " + x,
    [x, 1] => "ends with 1",
    _ => "other"
};
print(result);  // "starts with 1, second is 2"
```

### Rest-паттерны для массивов (`...`)

Захват оставшихся элементов:

```hemlock
let nums = [1, 2, 3, 4, 5];

// Голова и хвост
let result = match (nums) {
    [first, ...rest] => "first: " + first,
    [] => "empty"
};
print(result);  // "first: 1"

// Первые два элемента
let result2 = match (nums) {
    [a, b, ...rest] => "first two: " + a + "," + b,
    _ => "too short"
};
print(result2);  // "first two: 1,2"
```

### Вложенная деструктуризация

Комбинирование паттернов для сложных данных:

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " lives in " + city,
    _ => "unknown"
};
print(result);  // "Alice lives in NYC"

// Объект содержащий массив
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "first: " + first + ", total: " + count,
    _ => "no items"
};
print(result2);  // "first: 1, total: 3"
```

## Match как выражение

Match это выражение, которое возвращает значение:

```hemlock
// Прямое присваивание
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// В конкатенации строк
let msg = "Grade: " + match (grade) {
    n if n >= 70 => "passing",
    _ => "failing"
};

// В возврате функции
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positive",
        _ => "negative"
    };
}
```

## Лучшие практики сопоставления с образцом

1. **Порядок важен**: Паттерны проверяются сверху вниз; помещайте специфичные паттерны перед общими
2. **Используйте заполнители для полноты**: Всегда включайте запасной `_` если не уверены что все случаи покрыты
3. **Предпочитайте guards вложенным условиям**: Guards делают намерение яснее
4. **Используйте деструктуризацию вместо ручного доступа к полям**: Более лаконично и безопасно

```hemlock
// Хорошо: Guards для проверки диапазона
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "below B"
}

// Хорошо: Деструктуризация вместо доступа к полям
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// Избегайте: Слишком сложные вложенные паттерны
// Вместо этого рассмотрите разбиение на несколько match или использование guards
```

## Сравнение с другими языками

| Возможность | Hemlock | Rust | JavaScript |
|-------------|---------|------|------------|
| Базовое сопоставление | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Деструктуризация | Да | Да | Частично (switch не деструктурирует) |
| Guards | `n if n > 0 =>` | `n if n > 0 =>` | Н/Д |
| ИЛИ паттерны | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Rest паттерны | `[a, ...rest]` | `[a, rest @ ..]` | Н/Д |
| Типовые паттерны | `n: i32` | Тип через `match` ветку | Н/Д |
| Возвращает значение | Да | Да | Нет (оператор) |

## Примечания по реализации

Сопоставление с образцом реализовано в обоих бэкендах - интерпретаторе и компиляторе - с полным паритетом: оба производят идентичные результаты для одного и того же входа. Функция доступна в Hemlock v1.8.0+.
