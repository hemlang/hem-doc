# Дизайн синтаксиса сигнатур

> Расширение системы типов Hemlock типами функций, модификаторами nullable, псевдонимами типов, const-параметрами и сигнатурами методов.

**Статус:** Реализовано (v1.7.0)
**Версия:** 1.0
**Автор:** Claude

---

## Обзор

Этот документ предлагает пять взаимосвязанных расширений системы типов, построенных на существующей инфраструктуре Hemlock:

1. **Аннотации типов функций** — Первоклассные типы функций
2. **Модификаторы nullable типов** — Явная обработка null (расширяет существующий флаг `nullable`)
3. **Псевдонимы типов** — Именованные сокращения типов
4. **Const-параметры** — Контракты неизменяемости
5. **Сигнатуры методов в Define** — Интерфейсоподобное поведение

Эти возможности разделяют философию: **явное важнее неявного, опционально, но применяется при использовании**.

---

## 1. Аннотации типов функций

### Мотивация

В настоящее время нет способа выразить сигнатуру функции как тип:

```hemlock
// Текущее: callback не имеет информации о типе
fn map(arr: array, callback) { ... }

// Предлагаемое: явный тип функции
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Синтаксис

```hemlock
// Базовый тип функции
fn(i32, i32): i32

// С именами параметров (только для документации, не проверяется)
fn(a: i32, b: i32): i32

// Без возвращаемого значения (void)
fn(string): void
fn(string)              // Сокращение: опустить `: void`

// Nullable возврат
fn(i32): string?

// Опциональные параметры
fn(name: string, age?: i32): void

// Rest-параметры
fn(...args: array): i32

// Без параметров
fn(): bool

// Высшего порядка: функция, возвращающая функцию
fn(i32): fn(i32): i32

// Тип асинхронной функции
async fn(i32): i32
```

### Примеры использования

```hemlock
// Переменная с типом функции
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Параметр функции
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Возвращаемый тип — функция
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Массив функций
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// Поле объекта
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### Изменения AST

```c
// В перечислении TypeKind (include/ast.h)
typedef enum {
    // ... существующие типы ...
    TYPE_FUNCTION,      // НОВОЕ: Тип функции
} TypeKind;

// В структуре Type (include/ast.h)
struct Type {
    TypeKind kind;
    // ... существующие поля ...

    // Для TYPE_FUNCTION:
    struct Type **param_types;      // Типы параметров
    char **param_names;             // Опциональные имена параметров (документация)
    int *param_optional;            // Какие параметры опциональны
    int num_params;
    char *rest_param_name;          // Имя rest-параметра или NULL
    struct Type *rest_param_type;   // Тип rest-параметра
    struct Type *return_type;       // Тип возврата (NULL = void)
    int is_async;                   // асинхронный тип fn
};
```

### Парсинг

Типы функций начинаются с `fn` (или `async fn`), за которым следует список параметров:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Разрешение неоднозначности:** При парсинге типа и встрече `fn`:
- Если за ним следует `(`, это тип функции
- Иначе синтаксическая ошибка (голый `fn` не является валидным типом)

### Совместимость типов

```hemlock
// Для типов функций требуется точное совпадение
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Контравариантность параметров (принятие более широких типов OK)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Ковариантность возврата (возврат более узких типов OK)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Арность должна совпадать
let bad: fn(i32): i32 = fn(a, b) { return a; };       // ОШИБКА: несоответствие арности

// Опциональные параметры совместимы с обязательными
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Модификаторы nullable типов

### Мотивация

Суффикс `?` делает явным принятие null в сигнатурах:

```hemlock
// Текущее: неясно, валиден ли null
fn find(arr: array, val: any): i32 { ... }

// Предлагаемое: явный nullable возврат
fn find(arr: array, val: any): i32? { ... }
```

### Синтаксис

```hemlock
// Nullable типы с суффиксом ?
string?           // string или null
i32?              // i32 или null
User?             // User или null
array<i32>?       // array или null
fn(i32): i32?     // функция, возвращающая i32 или null

// Композиция с типами функций
fn(string?): i32          // Принимает string или null
fn(string): i32?          // Возвращает i32 или null
fn(string?): i32?         // Оба nullable

// В define
define Result {
    value: any?;
    error: string?;
}
```

### Примечания к реализации

**Уже существует:** Флаг `Type.nullable` уже есть в AST. Эта возможность в основном требует:
1. Поддержка парсера для суффикса `?` на любом типе (проверить/расширить)
2. Правильная композиция с типами функций
3. Применение во время выполнения

### Совместимость типов

```hemlock
// Non-nullable присваивается nullable
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullable НЕ присваивается non-nullable
let z: i32 = x;             // ОШИБКА: x может быть null

// Null coalescing для развёртывания
let z: i32 = x ?? 0;        // OK: ?? предоставляет значение по умолчанию

// Optional chaining возвращает nullable
let name: string? = user?.name;
```

---

## 3. Псевдонимы типов

### Мотивация

Сложные типы выигрывают от именованных сокращений:

```hemlock
// Текущее: повторяющиеся составные типы
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// Предлагаемое: именованный псевдоним
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### Синтаксис

```hemlock
// Базовый псевдоним
type Integer = i32;
type Text = string;

// Псевдоним составного типа
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// Псевдоним типа функции
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Nullable псевдоним
type OptionalString = string?;

// Дженерик-псевдоним (если поддерживаем дженерик-псевдонимы типов)
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Псевдоним типа массива
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### Область видимости и видимость

```hemlock
// По умолчанию в области модуля
type Callback = fn(Event): void;

// Экспортируемый
export type Handler = fn(Request): Response;

// В другом файле
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### Изменения AST

```c
// Новый вид оператора
typedef enum {
    // ... существующие операторы ...
    STMT_TYPE_ALIAS,    // НОВОЕ
} StmtKind;

// В объединении Stmt
struct {
    char *name;                 // Имя псевдонима
    char **type_params;         // Дженерик-параметры: <T, U>
    int num_type_params;
    Type *aliased_type;         // Фактический тип
} type_alias;
```

### Парсинг

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Примечание:** `type` — новое ключевое слово. Проверить конфликты с существующими идентификаторами.

### Разрешение

Псевдонимы типов разрешаются на:
- **Этапе парсинга:** Псевдоним записывается в окружение типов
- **Этапе проверки:** Псевдоним разворачивается в базовый тип
- **Во время выполнения:** Псевдоним прозрачен (то же, что базовый тип)

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32" (не "MyInt")
```

---

## 4. Const-параметры

### Мотивация

Сигнализировать намерение неизменяемости в сигнатурах функций:

```hemlock
// Текущее: неясно, будет ли массив изменён
fn print_all(items: array) { ... }

// Предлагаемое: явный контракт неизменяемости
fn print_all(const items: array) { ... }
```

### Синтаксис

```hemlock
// Const-параметр
fn process(const data: buffer) {
    // data[0] = 0;        // ОШИБКА: нельзя изменять const
    let x = data[0];       // OK: чтение разрешено
    return x;
}

// Несколько const-параметров
fn compare(const a: array, const b: array): bool { ... }

// Смешанные const и изменяемые
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK: target изменяемый
    }
}

// Const с выводом типа
fn log(const msg) {
    print(msg);
}

// Const в типах функций
type Reader = fn(const buffer): i32;
```

### Что предотвращает Const

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // ОШИБКА: изменяющий метод
    arr.pop();           // ОШИБКА: изменяющий метод
    arr[0] = 5;          // ОШИБКА: присваивание по индексу
    arr.clear();         // ОШИБКА: изменяющий метод
}

fn ok(const arr: array) {
    let x = arr[0];      // OK: чтение
    let len = len(arr);  // OK: проверка длины
    let copy = arr.slice(0, 10);  // OK: создаёт новый массив
    for (item in arr) {  // OK: итерация
        print(item);
    }
}
```

### Изменяющие vs неизменяющие методы

| Тип | Изменяющие (блокируются const) | Неизменяющие (разрешены) |
|-----|-------------------------------|-------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (на месте) | slice, concat, map, filter, find, contains, first, last, join |
| string | присваивание по индексу (`s[0] = 'x'`) | все методы (возвращают новые строки) |
| buffer | присваивание по индексу, memset, memcpy (в) | чтение по индексу, slice |
| object | присваивание поля | чтение поля |

### Изменения AST

```c
// В выражении функции (include/ast.h)
struct {
    // ... существующие поля ...
    int *param_is_const;    // НОВОЕ: 1 если const, 0 иначе
} function;

// В структуре Type для типов функций
struct Type {
    // ... существующие поля ...
    int *param_is_const;    // Для TYPE_FUNCTION
};
```

### Применение

**Интерпретатор:**
- Отслеживать const-ность в привязках переменных
- Проверять перед операциями изменения
- Ошибка времени выполнения при нарушении const

**Компилятор:**
- Генерировать const-квалифицированные переменные C где полезно
- Статический анализ нарушений const
- Предупреждение/ошибка на этапе компиляции

---

## 5. Сигнатуры методов в Define

### Мотивация

Позволить блокам `define` указывать ожидаемые методы, а не только поля данных:

```hemlock
// Текущее: только поля данных
define User {
    name: string;
    age: i32;
}

// Предлагаемое: сигнатуры методов
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // Статический метод
}
```

### Синтаксис

```hemlock
// Сигнатура метода (без тела)
define Hashable {
    fn hash(): i32;
}

// Несколько методов
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// Смешанные поля и методы
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Использование типа Self
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// Опциональные методы
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // Опциональный метод (может отсутствовать)
}

// Методы с реализациями по умолчанию
define Ordered {
    fn compare(other: Self): i32;  // Обязательный

    // Реализации по умолчанию (наследуются, если не переопределены)
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### Тип `Self`

`Self` ссылается на конкретный тип, реализующий интерфейс:

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// При использовании:
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### Структурная типизация (утиная типизация)

Сигнатуры методов используют ту же утиную типизацию, что и поля:

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// Любой объект с методом to_string() удовлетворяет Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// Составные типы с методами
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### Изменения AST

```c
// Расширить define_object в объединении Stmt
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Поля (существующие)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Методы (НОВОЕ)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Опциональные методы (fn name?(): type)
    Expr **method_defaults;     // Реализации по умолчанию (NULL если только сигнатура)
    int num_methods;
} define_object;
```

### Проверка типов

При проверке `value: InterfaceType`:
1. Проверить, что все обязательные поля существуют с совместимыми типами
2. Проверить, что все обязательные методы существуют с совместимыми сигнатурами
3. Опциональные поля/методы могут отсутствовать

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// Валидно: есть метод compare
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Невалидно: отсутствует compare
let invalid: Sortable = { value: 10 };  // ОШИБКА: отсутствует метод 'compare'

// Невалидно: неправильная сигнатура
let wrong: Sortable = {
    compare: fn() { return 0; }  // ОШИБКА: ожидается (Self): i32
};
```

---

## Примеры взаимодействия

### Объединение всех возможностей

```hemlock
// Псевдоним типа для сложного типа функции
type EventCallback = fn(event: Event, context: Context?): bool;

// Псевдоним типа для составного интерфейса
type Entity = HasId & HasName & Serializable;

// Define с сигнатурами методов
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// Использование всего вместе
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### Колбэки с явными типами

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Nullable типы функций

```hemlock
// Опциональный колбэк
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// Nullable возврат из типа функции
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## План реализации

### Фаза 1: Основная инфраструктура
1. Добавить `TYPE_FUNCTION` в перечисление TypeKind
2. Расширить структуру Type полями типа функции
3. Добавить `CHECKED_FUNCTION` в проверку типов компилятора
4. Добавить поддержку типа `Self` (TYPE_SELF)

### Фаза 2: Парсинг
1. Реализовать `parse_function_type()` в парсере
2. Обработать `fn(...)` в позиции типа
3. Добавить ключевое слово `type` и парсинг `STMT_TYPE_ALIAS`
4. Добавить парсинг модификатора `const` для параметров
5. Расширить парсинг define для сигнатур методов

### Фаза 3: Проверка типов
1. Правила совместимости типов функций
2. Разрешение и развёртывание псевдонимов типов
3. Проверка изменений const-параметров
4. Валидация сигнатур методов в define-типах
5. Разрешение типа Self

### Фаза 4: Среда выполнения
1. Валидация типов функций в местах вызова
2. Обнаружение нарушений const
3. Прозрачность псевдонимов типов

### Фаза 5: Паритетные тесты
1. Тесты аннотаций типов функций
2. Тесты композиции nullable
3. Тесты псевдонимов типов
4. Тесты const-параметров
5. Тесты сигнатур методов

---

## Проектные решения

### 1. Дженерик-псевдонимы типов: **ДА**

Псевдонимы типов поддерживают дженерик-параметры:

```hemlock
// Дженерик-псевдонимы типов
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Использование
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Распространение Const: **ГЛУБОКОЕ**

Const-параметры полностью неизменяемы — никакого изменения через любой путь:

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // ОШИБКА: нельзя изменять const массив
    arr[0] = {};         // ОШИБКА: нельзя изменять const массив
    arr[0].x = 5;        // ОШИБКА: нельзя изменять через const (ГЛУБОКОЕ)

    let x = arr[0].x;    // OK: чтение допустимо
    let copy = arr[0];   // OK: создаёт копию
    copy.x = 5;          // OK: копия не const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // ОШИБКА: глубокий const предотвращает вложенное изменение
    obj.items[0] = 1;    // ОШИБКА: глубокий const предотвращает вложенное изменение
}
```

**Обоснование:** Глубокий const предоставляет более сильные гарантии и более полезен для
обеспечения целостности данных. Если нужно изменить вложенные данные, сначала сделайте копию.

### 3. Self в автономных псевдонимах типов: **НЕТ**

`Self` валиден только внутри блоков `define`, где имеет ясный смысл:

```hemlock
// Валидно: Self ссылается на определяемый тип
define Comparable {
    fn compare(other: Self): i32;
}

// Невалидно: Self не имеет смысла здесь
type Cloner = fn(Self): Self;  // ОШИБКА: Self вне контекста define

// Вместо этого используйте дженерики:
type Cloner<T> = fn(T): T;
```

### 4. Реализации методов по умолчанию: **ДА (только простые)**

Разрешить реализации по умолчанию для простых/вспомогательных методов:

```hemlock
define Comparable {
    // Обязательный: должен быть реализован
    fn compare(other: Self): i32;

    // Реализации по умолчанию (простые вспомогательные методы)
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // По умолчанию: делегирует обязательному методу
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// Объекту нужно реализовать только обязательные методы
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_than наследуются из значений по умолчанию
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**Руководства для методов по умолчанию:**
- Держите их простыми (1-3 строки)
- Должны делегировать обязательным методам
- Никакой сложной логики или побочных эффектов
- Только примитивы и простые композиции

### 5. Вариантность: **ВЫВОДИТСЯ (без явных аннотаций)**

Вариантность выводится из того, как используются параметры типа:

```hemlock
// Вариантность автоматическая на основе позиции
type Producer<T> = fn(): T;           // T в возврате = ковариантный
type Consumer<T> = fn(T): void;       // T в параметре = контравариантный
type Transformer<T> = fn(T): T;       // T в обоих = инвариантный

// Пример: Dog <: Animal (Dog — подтип Animal)
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK: ковариантный

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK: контравариантный
```

**Почему вывод?**
- Меньше шаблонного кода (`<out T>` / `<in T>` добавляют шум)
- Следует принципу "явное важнее неявного" — позиция И ЕСТЬ явная
- Соответствует тому, как большинство языков обрабатывают вариантность типов функций
- Ошибки ясны при нарушении правил вариантности

---

## Приложение: Изменения грамматики

```ebnf
(* Типы *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* Операторы *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" отмечает опциональный метод, block предоставляет реализацию по умолчанию *)

(* Параметры *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
