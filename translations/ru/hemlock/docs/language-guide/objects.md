# Объекты

Hemlock реализует объекты в стиле JavaScript с размещением в куче, динамическими полями, методами и утиной типизацией. Объекты - это гибкие структуры данных, которые объединяют данные и поведение.

## Обзор

```hemlock
// Анонимный объект
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// Объект с методами
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Литералы объектов

### Базовый синтаксис

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**Синтаксис:**
- Фигурные скобки `{}` окружают объект
- Пары ключ-значение разделены запятыми
- Ключи - это идентификаторы (кавычки не нужны)
- Значения могут быть любого типа

### Пустые объекты

```hemlock
let obj = {};  // Пустой объект

// Добавление полей позже
obj.name = "Alice";
obj.age = 30;
```

### Вложенные объекты

```hemlock
let user = {
    info: {
        name: "Bob",
        age: 25
    },
    active: true,
    settings: {
        theme: "dark",
        notifications: true
    }
};

print(user.info.name);           // "Bob"
print(user.settings.theme);      // "dark"
```

### Смешанные типы значений

```hemlock
let mixed = {
    number: 42,
    text: "hello",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### Сокращенный синтаксис свойств

Когда имя переменной совпадает с именем свойства, используйте сокращенный синтаксис:

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Сокращение: { name } эквивалентно { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Смешивание сокращений с обычными свойствами:**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### Оператор распространения (spread)

Оператор spread (`...`) копирует все поля из одного объекта в другой:

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Переопределение значений со spread:**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (переопределено)
print(custom.size);   // "medium" (из defaults)
print(custom.debug);  // false (из defaults)
```

**Множественные spread (более поздние переопределяют ранние):**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// Более поздний spread переопределяет ранний
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**Комбинирование сокращений и spread:**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**Паттерн переопределения конфигурации:**
```hemlock
let defaultConfig = {
    debug: false,
    timeout: 30,
    retries: 3
};

let prodConfig = { ...defaultConfig, timeout: 60 };
let devConfig = { ...defaultConfig, debug: true };

print(prodConfig.timeout);  // 60
print(devConfig.debug);     // true
```

**Примечание:** Spread выполняет поверхностное копирование. Вложенные объекты разделяют ссылки:
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (та же ссылка что и nested.inner)
```

## Доступ к полям

### Точечная нотация

```hemlock
let person = { name: "Alice", age: 30 };

// Чтение поля
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Изменение поля
person.age = 31;
print(person.age);           // 31
```

### Динамическое добавление полей

Добавление новых полей во время выполнения:

```hemlock
let person = { name: "Alice" };

// Добавление нового поля
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Удаление полей

**Примечание:** Удаление полей в настоящее время не поддерживается. Вместо этого установите значение в `null`:

```hemlock
let obj = { x: 10, y: 20 };

// Нельзя удалить поля (не поддерживается)
// obj.x = undefined;  // Нет 'undefined' в Hemlock

// Обходной путь: Установить в null
obj.x = null;
```

## Методы и `self`

### Определение методов

Методы - это функции, хранящиеся в полях объекта:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
    decrement: fn() {
        self.count = self.count - 1;
    },
    get: fn() {
        return self.count;
    }
};
```

### Ключевое слово `self`

Когда функция вызывается как метод, `self` автоматически привязывается к объекту:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self ссылается на counter
    }
};

counter.increment();  // self привязан к counter
print(counter.count);  // 1
```

**Как это работает:**
- Вызовы методов определяются проверкой, является ли выражение функции доступом к свойству
- `self` автоматически привязывается к объекту во время вызова
- `self` только для чтения (нельзя переназначить сам `self`)

### Обнаружение вызова метода

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Вызов как метод - self привязан
print(obj.method());  // 10

// Вызов как функция - self равен null (ошибка)
let f = obj.method;
print(f());  // ОШИБКА: self не определен
```

### Методы с параметрами

```hemlock
let calculator = {
    result: 0,
    add: fn(x) {
        self.result = self.result + x;
    },
    multiply: fn(x) {
        self.result = self.result * x;
    },
    get: fn() {
        return self.result;
    }
};

calculator.add(5);
calculator.multiply(2);
print(calculator.get());  // 10
```

## Определения типов с `define`

### Базовое определение типа

Определение форм объектов с помощью `define`:

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Создание объекта и присваивание типизированной переменной
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Утиная типизация проверяет структуру

print(typeof(typed_p));  // "Person"
```

**Что делает `define`:**
- Объявляет тип с обязательными полями
- Включает валидацию утиной типизации
- Устанавливает имя типа объекта для `typeof()`

### Утиная типизация

Объекты валидируются относительно `define` используя **структурную совместимость**:

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Имеет все обязательные поля
let p1: Person = { name: "Alice", age: 30 };

// OK: Дополнительные поля разрешены
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// ОШИБКА: Отсутствует обязательное поле 'age'
let p3: Person = { name: "Carol" };

// ОШИБКА: Неправильный тип для 'age'
let p4: Person = { name: "Dave", age: "thirty" };
```

**Правила утиной типизации:**
- Все обязательные поля должны присутствовать
- Типы полей должны совпадать
- Дополнительные поля разрешены и сохраняются
- Валидация происходит во время присваивания

### Необязательные поля

Поля могут быть необязательными со значениями по умолчанию:

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Необязательное со значением по умолчанию
    nickname?: string,   // Необязательное, по умолчанию null
}

// Объект только с обязательными полями
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (применено значение по умолчанию)
print(typed_p.nickname);  // null (нет значения по умолчанию)

// Можно переопределить необязательные поля
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (переопределено)
```

**Синтаксис необязательных полей:**
- `field?: default_value` - Необязательное со значением по умолчанию
- `field?: type` - Необязательное с аннотацией типа, по умолчанию null
- Необязательные поля добавляются при утиной типизации если отсутствуют

### Проверка типов

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // Проверка типов происходит здесь

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (оригинал все еще анонимный)
```

**Когда происходит проверка типов:**
- Во время присваивания типизированной переменной
- Проверяет наличие всех обязательных полей
- Проверяет соответствие типов полей (с неявными преобразованиями)
- Устанавливает имя типа объекта

## Сигнатуры методов в Define

Блоки define могут указывать сигнатуры методов, создавая контракты подобные интерфейсам:

### Обязательные методы

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Сигнатура обязательного метода
}

// Объекты должны предоставлять обязательный метод
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Необязательные методы

```hemlock
define Serializable {
    fn serialize(): string;       // Обязательный
    fn pretty?(): string;         // Необязательный метод (может отсутствовать)
}
```

### Тип `Self`

`Self` ссылается на определяемый тип, позволяя рекурсивные определения типов:

```hemlock
define Cloneable {
    fn clone(): Self;  // Возвращает тот же тип что и объект
}

define Comparable {
    fn compare(other: Self): i32;  // Принимает тот же тип как параметр
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Смешанные поля и методы

```hemlock
define Entity {
    id: i32,
    name: string,
    fn validate(): bool;
    fn serialize(): string;
}

let user: Entity = {
    id: 1,
    name: "Alice",
    validate: fn() { return self.id > 0 && self.name != ""; },
    serialize: fn() { return '{"id":' + self.id + ',"name":"' + self.name + '"}'; }
};
```

## Составные типы (типы пересечения)

Составные типы используют `&` для требования, чтобы объект удовлетворял нескольким определениям типов:

### Базовые составные типы

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Составной тип: объект должен удовлетворять ВСЕМ типам
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Параметры функций с составными типами

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // Дополнительные поля OK
```

### Три и более типов

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Псевдонимы типов для составных типов

```hemlock
// Создание именованного псевдонима для составного типа
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Утиная типизация с составными:** Дополнительные поля всегда разрешены - объект просто должен иметь как минимум поля, требуемые всеми компонентами типа.

## Сериализация JSON

### Сериализация в JSON

Преобразование объектов в строки JSON:

```hemlock
// obj.serialize() - Преобразовать объект в строку JSON
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Вложенные объекты
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Десериализация из JSON

Разбор строк JSON обратно в объекты:

```hemlock
// json.deserialize() - Разобрать строку JSON в объект
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Обнаружение циклов

Циклические ссылки обнаруживаются и вызывают ошибки:

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Создание циклической ссылки

obj.serialize();  // ОШИБКА: serialize() обнаружил циклическую ссылку
```

### Поддерживаемые типы

Сериализация JSON поддерживает:

- **Числа**: i8-i32, u8-u32, f32, f64
- **Булевы**: true, false
- **Строки**: С escape-последовательностями
- **Null**: значение null
- **Объекты**: Вложенные объекты
- **Массивы**: Вложенные массивы

**Не поддерживаются:**
- Функции (молча пропускаются)
- Указатели (ошибка)
- Буферы (ошибка)

### Обработка ошибок

Сериализация и десериализация могут вызывать ошибки:

```hemlock
// Недопустимый JSON вызывает ошибку
try {
    let bad = "not valid json".deserialize();
} catch (e) {
    print("Parse error:", e);
}

// Указатели нельзя сериализовать
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialize error:", e);
}
```

### Пример полного цикла

Полный пример сериализации и десериализации:

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Создание и сериализация
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Десериализация обратно
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Встроенные функции

### `typeof(value)`

Возвращает имя типа как строку:

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Возвращаемые значения:**
- Анонимные объекты: `"object"`
- Типизированные объекты: Имя пользовательского типа (например, `"Person"`)

## Детали реализации

### Модель памяти

- **Размещение в куче** - Все объекты размещаются в куче
- **Поверхностное копирование** - Присваивание копирует ссылку, не объект
- **Динамические поля** - Хранятся как динамические массивы пар имя/значение
- **Подсчет ссылок** - Объекты автоматически освобождаются при выходе из области видимости

### Семантика ссылок

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Поверхностное копирование (та же ссылка)

obj2.x = 20;
print(obj1.x);  // 20 (оба ссылаются на один объект)
```

### Хранение методов

Методы - это просто функции, хранящиеся в полях:

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method это функция, хранящаяся в obj.method
print(typeof(obj.method));  // "function"
```

## Распространенные паттерны

### Паттерн: Функция-конструктор

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

### Паттерн: Строитель объектов

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Включает цепочку
        },

        setAge: fn(a) {
            self.age = a;
            return self;
        },

        build: fn() {
            return { name: self.name, age: self.age };
        }
    };
}

let person = PersonBuilder()
    .setName("Alice")
    .setAge(30)
    .build();
```

### Паттерн: Объект состояния

```hemlock
let state = {
    status: "idle",
    data: null,
    error: null,

    setState: fn(new_status) {
        self.status = new_status;
    },

    setData: fn(new_data) {
        self.data = new_data;
        self.status = "success";
    },

    setError: fn(err) {
        self.error = err;
        self.status = "error";
    }
};
```

### Паттерн: Объект конфигурации

```hemlock
let config = {
    defaults: {
        timeout: 30,
        retries: 3,
        debug: false
    },

    get: fn(key) {
        if (self.defaults[key] != null) {
            return self.defaults[key];
        }
        return null;
    },

    set: fn(key, value) {
        self.defaults[key] = value;
    }
};
```

## Лучшие практики

1. **Используйте `define` для структуры** - Документируйте ожидаемые формы объектов
2. **Предпочитайте фабричные функции** - Создавайте объекты с конструкторами
3. **Держите объекты простыми** - Не вкладывайте слишком глубоко
4. **Документируйте использование `self`** - Делайте поведение методов ясным
5. **Валидируйте при присваивании** - Используйте утиную типизацию для раннего обнаружения ошибок
6. **Избегайте циклических ссылок** - Вызовут ошибки сериализации
7. **Используйте необязательные поля** - Предоставляйте разумные значения по умолчанию

## Распространенные ловушки

### Ловушка: Ссылка vs значение

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Поверхностное копирование

obj2.x = 20;
print(obj1.x);  // 20 (сюрприз! оба изменились)

// Чтобы избежать: Создайте новый объект
let obj3 = { x: obj1.x };  // Глубокое копирование (вручную)
```

### Ловушка: `self` при не-методных вызовах

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Работает: Вызван как метод
print(obj.method());  // 10

// ОШИБКА: Вызван как функция
let f = obj.method;
print(f());  // ОШИБКА: self не определен
```

### Ловушка: Сырые указатели в объектах

```hemlock
// Объекты авто-освобождаются, но сырые указатели внутри НЕТ
fn create_objects() {
    let obj = { data: alloc(1000) };  // сырой ptr нужно освободить вручную
    // obj авто-освобождается при выходе из области, но obj.data утекает!
}

// Решение: Освобождайте сырые указатели до выхода из области
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... используем obj.data ...
    free(obj.data);  // Освобождаем сырой указатель явно
}  // сам obj авто-освобождается
```

### Ловушка: Путаница с типами

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// ОШИБКА: Отсутствует обязательное поле 'y'
let p: Point = obj;
```

## Примеры

### Пример: Векторная математика

```hemlock
fn createVector(x, y) {
    return {
        x: x,
        y: y,

        add: fn(other) {
            return createVector(
                self.x + other.x,
                self.y + other.y
            );
        },

        length: fn() {
            return sqrt(self.x * self.x + self.y * self.y);
        },

        toString: fn() {
            return "(" + typeof(self.x) + ", " + typeof(self.y) + ")";
        }
    };
}

let v1 = createVector(3, 4);
let v2 = createVector(1, 2);
let v3 = v1.add(v2);

print(v3.toString());  // "(4, 6)"
```

### Пример: Простая база данных

```hemlock
fn createDatabase() {
    let records = [];
    let next_id = 1;

    return {
        insert: fn(data) {
            let record = { id: next_id, data: data };
            records.push(record);
            next_id = next_id + 1;
            return record.id;
        },

        find: fn(id) {
            let i = 0;
            while (i < records.length) {
                if (records[i].id == id) {
                    return records[i];
                }
                i = i + 1;
            }
            return null;
        },

        count: fn() {
            return records.length;
        }
    };
}

let db = createDatabase();
let id = db.insert({ name: "Alice", age: 30 });
let record = db.find(id);
print(record.data.name);  // "Alice"
```

### Пример: Эмиттер событий

```hemlock
fn createEventEmitter() {
    let listeners = {};

    return {
        on: fn(event, handler) {
            if (listeners[event] == null) {
                listeners[event] = [];
            }
            listeners[event].push(handler);
        },

        emit: fn(event, data) {
            if (listeners[event] != null) {
                let i = 0;
                while (i < listeners[event].length) {
                    listeners[event][i](data);
                    i = i + 1;
                }
            }
        }
    };
}

let emitter = createEventEmitter();

emitter.on("message", fn(data) {
    print("Received: " + data);
});

emitter.emit("message", "Hello!");
```

## Ограничения

Текущие ограничения:

- **Нет глубокого копирования** - Нужно вручную копировать вложенные объекты (spread поверхностный)
- **Нет передачи по значению** - Объекты всегда передаются по ссылке
- **Нет вычисляемых свойств** - Нет синтаксиса `{[key]: value}`
- **`self` только для чтения** - Нельзя переназначить `self` в методах
- **Нет удаления свойств** - Нельзя удалить поля после добавления

**Примечание:** Объекты используют подсчет ссылок и автоматически освобождаются при выходе из области видимости. См. [Управление памятью](memory.md#internal-reference-counting) для деталей.

## Связанные темы

- [Функции](functions.md) - Методы это функции, хранящиеся в объектах
- [Массивы](arrays.md) - Массивы также являются объектоподобными
- [Типы](types.md) - Утиная типизация и определения типов
- [Обработка ошибок](error-handling.md) - Выброс объектов ошибок

## См. также

- **Утиная типизация**: См. раздел "Объекты" в CLAUDE.md для деталей утиной типизации
- **JSON**: См. CLAUDE.md для деталей сериализации JSON
- **Память**: См. [Память](memory.md) для размещения объектов
