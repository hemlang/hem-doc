# Обзор синтаксиса

Этот документ описывает основные правила синтаксиса и структуру программ на Hemlock.

## Основные правила синтаксиса

### Точки с запятой обязательны

В отличие от JavaScript или Python, точки с запятой **всегда обязательны** в конце операторов:

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**Это вызовет ошибку:**
```hemlock
let x = 42  // ОШИБКА: Отсутствует точка с запятой
let y = 10  // ОШИБКА: Отсутствует точка с запятой
```

### Фигурные скобки всегда обязательны

Все блоки управления потоком должны использовать фигурные скобки, даже для одиночных операторов:

```hemlock
// ПРАВИЛЬНО
if (x > 0) {
    print("positive");
}

// ОШИБКА: Отсутствуют фигурные скобки
if (x > 0)
    print("positive");
```

### Комментарии

```hemlock
// Это однострочный комментарий

/*
   Это
   многострочный комментарий
*/

let x = 42;  // Встроенный комментарий
```

## Переменные

### Объявление

Переменные объявляются с помощью `let`:

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Аннотации типов (необязательно)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hello";
```

### Константы

Используйте `const` для неизменяемых значений:

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Попытка переназначить константу приведет к ошибке времени выполнения: "Cannot assign to const variable".

## Выражения

### Арифметические операторы

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - Сложение
print(a - b);   // 7  - Вычитание
print(a * b);   // 30 - Умножение
print(a / b);   // 3  - Деление (целочисленное)
```

### Операторы сравнения

```hemlock
print(a == b);  // false - Равно
print(a != b);  // true  - Не равно
print(a > b);   // true  - Больше
print(a < b);   // false - Меньше
print(a >= b);  // true  - Больше или равно
print(a <= b);  // false - Меньше или равно
```

### Логические операторы

```hemlock
let x = true;
let y = false;

print(x && y);  // false - И
print(x || y);  // true  - ИЛИ
print(!x);      // false - НЕ
```

### Побитовые операторы

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - Побитовое И
print(a | b);   // 14 - Побитовое ИЛИ
print(a ^ b);   // 6  - Побитовое исключающее ИЛИ
print(a << 2);  // 48 - Сдвиг влево
print(a >> 1);  // 6  - Сдвиг вправо
print(~a);      // -13 - Побитовое НЕ
```

### Приоритет операторов

От высшего к низшему:

1. `()` - Группировка
2. `!`, `~`, `-` (унарный) - Унарные операторы
3. `*`, `/` - Умножение, Деление
4. `+`, `-` - Сложение, Вычитание
5. `<<`, `>>` - Побитовые сдвиги
6. `<`, `<=`, `>`, `>=` - Сравнения
7. `==`, `!=` - Равенство
8. `&` - Побитовое И
9. `^` - Побитовое исключающее ИЛИ
10. `|` - Побитовое ИЛИ
11. `&&` - Логическое И
12. `||` - Логическое ИЛИ

**Примеры:**
```hemlock
let x = 2 + 3 * 4;      // 14 (не 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Управление потоком

### Условные операторы If

```hemlock
if (condition) {
    // тело
}

if (condition) {
    // ветка then
} else {
    // ветка else
}

if (condition1) {
    // ветка 1
} else if (condition2) {
    // ветка 2
} else {
    // ветка по умолчанию
}
```

### Циклы While

```hemlock
while (condition) {
    // тело
}
```

**Пример:**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Циклы For

**Цикл for в стиле C:**
```hemlock
for (initializer; condition; increment) {
    // тело
}
```

**Пример:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (массивы):**
```hemlock
for (let item in array) {
    // тело
}
```

**Пример:**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Операторы Switch

```hemlock
switch (expression) {
    case value1:
        // тело
        break;
    case value2:
        // тело
        break;
    default:
        // тело по умолчанию
        break;
}
```

**Пример:**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Monday");
        break;
    case 2:
        print("Tuesday");
        break;
    case 3:
        print("Wednesday");
        break;
    default:
        print("Other");
        break;
}
```

### Break и Continue

```hemlock
// Break: выход из цикла
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue: переход к следующей итерации
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Функции

### Именованные функции

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // тело
    return value;
}
```

**Пример:**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Анонимные функции

```hemlock
let func = fn(params) {
    // тело
};
```

**Пример:**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Аннотации типов (необязательно)

```hemlock
// Без аннотаций (типы выводятся)
fn greet(name) {
    return "Hello, " + name;
}

// С аннотациями (проверяются во время выполнения)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Объекты

### Литералы объектов

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Пример:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Методы

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Пример:**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Определения типов

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Пример:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Массивы

### Литералы массивов

```hemlock
let arr = [element1, element2, element3];
```

**Пример:**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];
let empty = [];
```

### Индексация массивов

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // Изменение элемента
```

## Обработка ошибок

### Try/Catch

```hemlock
try {
    // рискованный код
} catch (e) {
    // обработка ошибки
}
```

### Try/Finally

```hemlock
try {
    // рискованный код
} finally {
    // выполняется всегда
}
```

### Try/Catch/Finally

```hemlock
try {
    // рискованный код
} catch (e) {
    // обработка ошибки
} finally {
    // очистка
}
```

### Throw

```hemlock
throw expression;
```

**Пример:**
```hemlock
if (x < 0) {
    throw "x must be positive";
}
```

### Panic

```hemlock
panic(message);
```

**Пример:**
```hemlock
panic("unrecoverable error");
```

## Модули (экспериментально)

### Операторы экспорта

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Операторы импорта

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Async (экспериментально)

### Асинхронные функции

```hemlock
async fn function_name(params): return_type {
    // тело
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Каналы

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (интерфейс внешних функций)

### Импорт разделяемой библиотеки

```hemlock
import "library_name.so";
```

### Объявление внешней функции

```hemlock
extern fn function_name(param: type): return_type;
```

**Пример:**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Литералы

### Целочисленные литералы

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // Автоматически i64

// Шестнадцатеричные (префикс 0x)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Двоичные (префикс 0b)
let bin = 0b1010;
let bin2 = 0b11110000;

// Восьмеричные (префикс 0o)
let oct = 0o777;
let oct2 = 0O123;

// Числовые разделители для читаемости
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Литералы с плавающей точкой

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // Научная нотация
let sci2 = 2.5E+3;       // Заглавная E тоже работает
let no_lead = .5;        // Без ведущего нуля (0.5)
let sep = 3.14_159_265;  // Числовые разделители
```

### Строковые литералы

```hemlock
let s = "hello";
let escaped = "line1\nline2\ttabbed";
let quote = "She said \"hello\"";

// Шестнадцатеричные escape-последовательности
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Unicode escape-последовательности
let emoji = "\u{1F600}";               // (смайлик)
let heart = "\u{2764}";                // (сердце)
let mixed = "Hello \u{1F30D}!";        // Hello (земля)!
```

**Escape-последовательности:**
- `\n` - новая строка
- `\t` - табуляция
- `\r` - возврат каретки
- `\\` - обратный слеш
- `\"` - двойная кавычка
- `\'` - одинарная кавычка
- `\0` - нулевой символ
- `\xNN` - шестнадцатеричный escape (2 цифры)
- `\u{XXXX}` - unicode escape (1-6 цифр)

### Литералы рун

```hemlock
let ch = 'A';
let emoji = '(ракета)';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Булевы литералы

```hemlock
let t = true;
let f = false;
```

### Литерал Null

```hemlock
let nothing = null;
```

## Правила области видимости

### Блочная область видимости

Переменные ограничены ближайшим охватывающим блоком:

```hemlock
let x = 1;  // Внешняя область

if (true) {
    let x = 2;  // Внутренняя область (затеняет внешнюю)
    print(x);   // 2
}

print(x);  // 1
```

### Область видимости функций

Функции создают собственную область видимости:

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // Может читать внешнюю область
}

foo();
// print(local);  // ОШИБКА: 'local' не определена здесь
```

### Область видимости замыканий

Замыкания захватывают переменные из охватывающей области:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Захватывает 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Пробелы и форматирование

### Отступы

Hemlock не требует определенного отступа, но рекомендуется 4 пробела:

```hemlock
fn example() {
    if (true) {
        print("indented");
    }
}
```

### Разрывы строк

Операторы могут занимать несколько строк:

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Оператор Loop

Ключевое слово `loop` предоставляет более чистый синтаксис для бесконечных циклов:

```hemlock
loop {
    // ... выполнение работы
    if (done) {
        break;
    }
}
```

Это эквивалентно `while (true)`, но делает намерение более ясным.

## Зарезервированные ключевые слова

Следующие ключевые слова зарезервированы в Hemlock:

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Следующие шаги

- [Система типов](types.md) - Узнайте о системе типов Hemlock
- [Управление потоком](control-flow.md) - Углубленное изучение управляющих структур
- [Функции](functions.md) - Освойте функции и замыкания
- [Управление памятью](memory.md) - Понимание указателей и буферов
