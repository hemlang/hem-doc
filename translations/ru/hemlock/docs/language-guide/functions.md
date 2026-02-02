# Функции

Функции в Hemlock являются **значениями первого класса**, которые можно присваивать переменным, передавать как аргументы и возвращать из других функций. Это руководство охватывает синтаксис функций, замыкания, рекурсию и продвинутые паттерны.

## Обзор

```hemlock
// Синтаксис именованных функций
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Анонимная функция
let multiply = fn(x, y) {
    return x * y;
};

// Замыкания
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Объявление функций

### Именованные функции

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**Компоненты:**
- `fn` - Ключевое слово функции
- `greet` - Имя функции
- `(name: string)` - Параметры с необязательными типами
- `: string` - Необязательный возвращаемый тип
- `{ ... }` - Тело функции

### Анонимные функции

Функции без имен, присваиваемые переменным:

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Именованные vs. Анонимные:**
```hemlock
// Это эквивалентно:
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Примечание:** Именованные функции преобразуются в присваивания переменных с анонимными функциями.

## Параметры

### Базовые параметры

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Аннотации типов

Необязательные аннотации типов для параметров:

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // Проверка типов во время выполнения продвигает к f64
```

**Проверка типов:**
- Типы параметров проверяются при вызове, если указаны
- Неявные преобразования типов следуют стандартным правилам продвижения
- Несоответствие типов вызывает ошибки времени выполнения

### Передача по значению

Все аргументы **копируются** (передача по значению):

```hemlock
fn modify(x) {
    x = 100;  // Изменяет только локальную копию
}

let a = 10;
modify(a);
print(a);  // Все еще 10 (без изменений)
```

**Примечание:** Объекты и массивы передаются по ссылке (ссылка копируется), поэтому их содержимое можно изменять:

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Изменяет оригинальный массив
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (изменено)
```

## Возвращаемые значения

### Оператор Return

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Аннотации возвращаемого типа

Необязательная аннотация типа для возвращаемого значения:

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Проверка типов:**
- Возвращаемые типы проверяются при возврате из функции (если указаны)
- Преобразования типов следуют стандартным правилам продвижения

### Неявный возврат

Функции без аннотации возвращаемого типа неявно возвращают `null`:

```hemlock
fn print_message(msg) {
    print(msg);
    // Неявно возвращает null
}

let result = print_message("hello");  // result равен null
```

### Ранний возврат

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Ранний выход
        }
    }
    return -1;  // Не найдено
}
```

### Возврат без значения

`return;` без значения возвращает `null`:

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Возвращает null
    }
    return value * 2;
}
```

## Функции первого класса

Функции можно присваивать, передавать и возвращать как любое другое значение.

### Функции как переменные

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Переприсваивание
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Функции как аргументы

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Функции как возвращаемые значения

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Замыкания

Функции захватывают свое окружение определения (лексическая область видимости).

### Базовые замыкания

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

**Как это работает:**
- Внутренняя функция захватывает `count` из внешней области
- `count` сохраняется между вызовами возвращенной функции
- Каждый вызов `makeCounter()` создает новое замыкание со своим `count`

### Замыкание с параметрами

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Множественные замыкания

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Лексическая область видимости

Функции могут обращаться к переменным внешней области через лексическую область видимости:

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Может читать global и outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Замыкания захватывают переменные по ссылке, позволяя как чтение, так и изменение переменных внешней области (как показано в примере `makeCounter` выше).

## Рекурсия

Функции могут вызывать сами себя.

### Базовая рекурсия

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Взаимная рекурсия

Функции могут вызывать друг друга:

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Рекурсивная обработка данных

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Примечание:** Оптимизация хвостовых вызовов пока не реализована - глубокая рекурсия может вызвать переполнение стека.

## Функции высшего порядка

Функции, которые принимают или возвращают другие функции.

### Паттерн Map

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Паттерн Filter

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Паттерн Reduce

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Композиция функций

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Распространенные паттерны

### Паттерн: Фабричные функции

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### Паттерн: Callback-функции

```hemlock
fn process_async(data, callback) {
    // ... выполнение обработки
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### Паттерн: Частичное применение

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Паттерн: Мемоизация

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Намного быстрее с кэшированием
```

## Семантика функций

### Требования к возвращаемому типу

Функции с аннотацией возвращаемого типа **должны** возвращать значение:

```hemlock
fn get_value(): i32 {
    // ОШИБКА: Отсутствует оператор return
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Проверка типов

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Продвигает к f64, возвращает f64
add("a", "b");     // Ошибка времени выполнения: несоответствие типов
```

### Правила области видимости

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Может обращаться к: inner_var, outer_var, global
    }

    // Может обращаться к: outer_var, global
    // Не может обращаться к: inner_var
}

// Может обращаться к: global
// Не может обращаться к: outer_var, inner_var
```

## Лучшие практики

1. **Используйте аннотации типов** - Помогает ловить ошибки и документирует намерения
2. **Делайте функции маленькими** - Каждая функция должна делать одно дело
3. **Предпочитайте чистые функции** - Избегайте побочных эффектов когда возможно
4. **Называйте функции ясно** - Используйте описательные имена с глаголами
5. **Возвращайте рано** - Используйте guard clauses для уменьшения вложенности
6. **Документируйте сложные замыкания** - Делайте захваченные переменные явными
7. **Избегайте глубокой рекурсии** - Оптимизация хвостовых вызовов пока не реализована

## Распространенные ловушки

### Ловушка: Глубина рекурсии

```hemlock
// Глубокая рекурсия может вызвать переполнение стека
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Может упасть с переполнением стека
```

### Ловушка: Изменение захваченных переменных

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Может читать и изменять захваченные переменные
        return count;
    };
}
```

**Примечание:** Это работает, но учитывайте, что все замыкания разделяют одно и то же захваченное окружение.

## Примеры

### Пример: Конвейер функций

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Пример: Обработчик событий

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clicked: " + data);
});

trigger_event("click", "button1");
```

### Пример: Сортировка с пользовательским компаратором

```hemlock
fn sort(arr, compare) {
    // Пузырьковая сортировка с пользовательским компаратором
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Необязательные параметры (аргументы по умолчанию)

Функции могут иметь необязательные параметры со значениями по умолчанию с использованием синтаксиса `?:`:

```hemlock
fn greet(name, greeting?: "Hello") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Hello Alice"
print(greet("Bob", "Hi"));       // "Hi Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Правила:**
- Необязательные параметры должны идти после обязательных
- Значения по умолчанию могут быть любыми выражениями
- Пропущенные аргументы используют значение по умолчанию

## Вариативные функции (rest-параметры)

Функции могут принимать переменное количество аргументов используя rest-параметры (`...`):

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Starting", "Running", "Done");
// INFO: Starting
// INFO: Running
// INFO: Done
```

**Правила:**
- Rest-параметр должен быть последним параметром
- Rest-параметр собирает все оставшиеся аргументы в массив
- Можно комбинировать с обычными и необязательными параметрами

## Аннотации функциональных типов

Функциональные типы позволяют указать точную сигнатуру, ожидаемую для параметров и возвращаемых значений функций:

### Базовые функциональные типы

```hemlock
// Синтаксис функционального типа: fn(типы_параметров): возвращаемый_тип
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Функциональные типы высшего порядка

```hemlock
// Функция, возвращающая функцию
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Асинхронные функциональные типы

```hemlock
// Асинхронный функциональный тип
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### Псевдонимы функциональных типов

```hemlock
// Создание именованных функциональных типов для ясности
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Const-параметры

Модификатор `const` предотвращает изменение параметра внутри функции:

### Базовые const-параметры

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // ОШИБКА: нельзя изменять const параметр
    for (item in items) {
        print(item);   // OK: чтение разрешено
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Глубокая неизменяемость

Const-параметры обеспечивают глубокую неизменяемость - изменение невозможно ни по какому пути:

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK: чтение разрешено
    // person.name = "Bob";   // ОШИБКА: нельзя изменять
    // person.address.city = "NYC";  // ОШИБКА: глубокий const
}
```

### Что предотвращает Const

| Тип | Блокируется Const | Разрешено |
|-----|-------------------|-----------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | присваивание полей | чтение полей |
| buffer | присваивание по индексу | чтение по индексу |
| string | присваивание по индексу | все методы (возвращают новые строки) |

## Именованные аргументы

Функции можно вызывать с именованными аргументами для ясности и гибкости:

### Базовые именованные аргументы

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Позиционные аргументы (традиционные)
create_user("Alice", 25, false);

// Именованные аргументы - могут быть в любом порядке
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Смешивание позиционных и именованных

```hemlock
// Пропуск необязательных параметров через именование нужных
create_user("David", active: false);  // Использует default age=18

// Именованные аргументы должны идти после позиционных
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // ОШИБКА: позиционный после именованного
```

### Правила для именованных аргументов

- Используйте синтаксис `name: value` для именованных аргументов
- Именованные аргументы могут появляться в любом порядке после позиционных
- Позиционные аргументы не могут следовать за именованными
- Работает с default/необязательными параметрами
- Неизвестные имена параметров вызывают ошибки времени выполнения

## Ограничения

Текущие ограничения:

- **Нет передачи по ссылке** - Ключевое слово `ref` разбирается, но не реализовано
- **Нет перегрузки функций** - Одна функция на имя
- **Нет оптимизации хвостовых вызовов** - Глубокая рекурсия ограничена размером стека

## Связанные темы

- [Управление потоком](control-flow.md) - Использование функций с управляющими структурами
- [Объекты](objects.md) - Методы это функции, хранящиеся в объектах
- [Обработка ошибок](error-handling.md) - Функции и обработка исключений
- [Типы](types.md) - Аннотации типов и преобразования

## См. также

- **Замыкания**: См. раздел "Функции" в CLAUDE.md для семантики замыканий
- **Значения первого класса**: Функции - это значения как любые другие
- **Лексическая область видимости**: Функции захватывают свое окружение определения
