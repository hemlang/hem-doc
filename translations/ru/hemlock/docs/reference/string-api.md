# Справочник по API строк

Полный справочник по типу строк Hemlock и всем 22 методам строк.

---

## Обзор

Строки в Hemlock — это **последовательности в кодировке UTF-8, изменяемые, размещаемые в куче**, с полной поддержкой Unicode. Все операции работают с **кодовыми точками** (символами), а не байтами.

**Ключевые особенности:**
- Кодировка UTF-8 (U+0000 до U+10FFFF)
- Изменяемые (можно модифицировать символы на месте)
- Индексация на основе кодовых точек
- 22 встроенных метода
- Автоматическая конкатенация оператором `+`

---

## Тип строки

**Тип:** `string`

**Свойства:**
- `.length` - Количество кодовых точек (символов)
- `.byte_length` - Количество байтов UTF-8

**Синтаксис литерала:** Двойные кавычки `"текст"`

**Примеры:**
```hemlock
let s = "hello";
print(s.length);        // 5 (кодовых точек)
print(s.byte_length);   // 5 (байтов)

let emoji = "🚀";
print(emoji.length);        // 1 (одна кодовая точка)
print(emoji.byte_length);   // 4 (четыре байта UTF-8)
```

---

## Индексация

Строки поддерживают индексацию на основе кодовых точек с использованием `[]`:

**Чтение:**
```hemlock
let s = "hello";
let ch = s[0];          // Возвращает руну 'h'
```

**Запись:**
```hemlock
let s = "hello";
s[0] = 'H';             // Изменение руной (теперь "Hello")
```

**Пример UTF-8:**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (одна кодовая точка)
print(text[3]);         // '!'
```

---

## Конкатенация

Используйте оператор `+` для объединения строк и рун:

**Строка + Строка:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**Строка + Руна:**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Руна + Строка:**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**Множественная конкатенация:**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## Свойства строки

### .length

Получить количество кодовых точек Unicode (символов).

**Тип:** `i32`

**Примеры:**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (одна кодовая точка)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 эмодзи)
```

---

### .byte_length

Получить количество байтов UTF-8.

**Тип:** `i32`

**Примеры:**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 байт на символ ASCII)

let emoji = "🚀";
print(emoji.byte_length); // 4 (эмодзи занимает 4 байта UTF-8)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 для эмодзи)
```

---

## Методы строк

### Подстрока и срезы

#### substr

Извлечь подстроку по позиции и длине.

**Сигнатура:**
```hemlock
string.substr(start: i32, length: i32): string
```

**Параметры:**
- `start` - Начальный индекс кодовой точки (с 0)
- `length` - Количество кодовых точек для извлечения

**Возвращает:** Новую строку

**Примеры:**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// Пример UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

Извлечь подстроку по диапазону (конец не включается).

**Сигнатура:**
```hemlock
string.slice(start: i32, end: i32): string
```

**Параметры:**
- `start` - Начальный индекс кодовой точки (с 0)
- `end` - Конечный индекс кодовой точки (не включается)

**Возвращает:** Новую строку

**Примеры:**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// Пример UTF-8
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### Поиск

#### find

Найти первое вхождение подстроки.

**Сигнатура:**
```hemlock
string.find(needle: string): i32
```

**Параметры:**
- `needle` - Искомая подстрока

**Возвращает:** Индекс кодовой точки первого вхождения или `-1`, если не найдено

**Примеры:**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (не найдено)
let pos3 = s.find("l");         // 2 (первая 'l')
```

---

#### contains

Проверить, содержит ли строка подстроку.

**Сигнатура:**
```hemlock
string.contains(needle: string): bool
```

**Параметры:**
- `needle` - Искомая подстрока

**Возвращает:** `true`, если найдено, `false` в противном случае

**Примеры:**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### Разделение и объединение

#### split

Разделить строку в массив по разделителю.

**Сигнатура:**
```hemlock
string.split(delimiter: string): array
```

**Параметры:**
- `delimiter` - Строка-разделитель

**Возвращает:** Массив строк

**Примеры:**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

Удалить начальные и конечные пробельные символы.

**Сигнатура:**
```hemlock
string.trim(): string
```

**Возвращает:** Новую строку с удалёнными пробелами

**Примеры:**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

#### trim_start

Удалить только начальные пробельные символы.

**Сигнатура:**
```hemlock
string.trim_start(): string
```

**Возвращает:** Новую строку с удалёнными начальными пробелами

**Примеры:**
```hemlock
let s = "  hello  ";
let clean = s.trim_start();     // "hello  "

let text = "\n\t  world  \n";
let clean2 = text.trim_start(); // "world  \n"
```

#### trim_end

Удалить только конечные пробельные символы.

**Сигнатура:**
```hemlock
string.trim_end(): string
```

**Возвращает:** Новую строку с удалёнными конечными пробелами

**Примеры:**
```hemlock
let s = "  hello  ";
let clean = s.trim_end();       // "  hello"

let text = "\n\t  world  \n";
let clean2 = text.trim_end();   // "\n\t  world"
```

---

### Преобразование регистра

#### to_upper

Преобразовать строку в верхний регистр.

**Сигнатура:**
```hemlock
string.to_upper(): string
```

**Возвращает:** Новую строку в верхнем регистре

**Примеры:**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

Преобразовать строку в нижний регистр.

**Сигнатура:**
```hemlock
string.to_lower(): string
```

**Возвращает:** Новую строку в нижнем регистре

**Примеры:**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### Префикс и суффикс

#### starts_with

Проверить, начинается ли строка с префикса.

**Сигнатура:**
```hemlock
string.starts_with(prefix: string): bool
```

**Параметры:**
- `prefix` - Проверяемый префикс

**Возвращает:** `true`, если строка начинается с префикса, `false` в противном случае

**Примеры:**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

Проверить, заканчивается ли строка суффиксом.

**Сигнатура:**
```hemlock
string.ends_with(suffix: string): bool
```

**Параметры:**
- `suffix` - Проверяемый суффикс

**Возвращает:** `true`, если строка заканчивается суффиксом, `false` в противном случае

**Примеры:**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### Замена

#### replace

Заменить первое вхождение подстроки.

**Сигнатура:**
```hemlock
string.replace(old: string, new: string): string
```

**Параметры:**
- `old` - Заменяемая подстрока
- `new` - Строка для замены

**Возвращает:** Новую строку с заменённым первым вхождением

**Примеры:**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (только первое)
```

---

#### replace_all

Заменить все вхождения подстроки.

**Сигнатура:**
```hemlock
string.replace_all(old: string, new: string): string
```

**Параметры:**
- `old` - Заменяемая подстрока
- `new` - Строка для замены

**Возвращает:** Новую строку со всеми заменёнными вхождениями

**Примеры:**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### Повторение

#### repeat

Повторить строку n раз.

**Сигнатура:**
```hemlock
string.repeat(count: i32): string
```

**Параметры:**
- `count` - Количество повторений

**Возвращает:** Новую строку, повторённую count раз

**Примеры:**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### Доступ к символам

#### char_at

Получить кодовую точку Unicode по индексу.

**Сигнатура:**
```hemlock
string.char_at(index: i32): rune
```

**Параметры:**
- `index` - Индекс кодовой точки (с 0)

**Возвращает:** Руну (кодовую точку Unicode)

**Примеры:**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// Пример UTF-8
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (ракета)
```

---

#### chars

Преобразовать строку в массив рун.

**Сигнатура:**
```hemlock
string.chars(): array
```

**Возвращает:** Массив рун (кодовых точек)

**Примеры:**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// Пример UTF-8
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### Доступ к байтам

#### byte_at

Получить значение байта по индексу.

**Сигнатура:**
```hemlock
string.byte_at(index: i32): u8
```

**Параметры:**
- `index` - Индекс байта (с 0, НЕ индекс кодовой точки)

**Возвращает:** Значение байта (u8)

**Примеры:**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// Пример UTF-8
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (первый байт UTF-8)
```

---

#### bytes

Преобразовать строку в массив байтов.

**Сигнатура:**
```hemlock
string.bytes(): array
```

**Возвращает:** Массив байтов u8

**Примеры:**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// Пример UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 байта UTF-8)
```

---

#### to_bytes

Преобразовать строку в буфер.

**Сигнатура:**
```hemlock
string.to_bytes(): buffer
```

**Возвращает:** Буфер, содержащий байты UTF-8

**Примеры:**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// Пример UTF-8
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Примечание:** Это устаревший метод. Предпочтительно использовать `.bytes()` в большинстве случаев.

---

### Доступ к сырому указателю

#### byte_ptr

Получить сырой указатель на внутренний буфер байтов UTF-8 строки. Это операция без выделения памяти — копия не создаётся.

**Сигнатура:**
```hemlock
string.byte_ptr(): ptr
```

**Возвращает:** Сырой указатель (`ptr`) на внутренние байты UTF-8 строки

**Примеры:**
```hemlock
let s = "Hello";
let p = s.byte_ptr();
print(typeof(p));              // "ptr"

// Чтение байтов через указатель
print(ptr_deref_u8(p));                    // 72 ('H')
print(ptr_deref_u8(ptr_offset(p, 1, 1))); // 101 ('e')
print(ptr_deref_u8(ptr_offset(p, 4, 1))); // 111 ('o')

// Использование с memcpy для копирования байтов строки
let buf = alloc(5);
memcpy(buf, s.byte_ptr(), 5);
print(ptr_deref_u8(buf));  // 72
free(buf);

// Совмещение с .byte_length для безопасного отслеживания размера
let emoji = "Hello 🚀";
let ep = emoji.byte_ptr();
print(emoji.byte_length);  // 10 (используйте byte_length, не length, для байтовых операций)
```

**Поведение:**
- Возвращает указатель непосредственно во внутреннюю память строки (без копирования)
- Указатель действителен, пока строка не модифицирована

**Случаи использования:**
- FFI-вызовы, которым нужен указатель на данные строки
- Интероп без копирования с C-функциями
- Критичный к производительности код, избегающий выделений

**Предупреждение:** Модификация строки (например, присваивание по индексу) после вызова `byte_ptr()` может инвалидировать указатель, если внутренний буфер строки перераспределён.

---

### Десериализация JSON

#### deserialize

Разобрать JSON-строку в значение.

**Сигнатура:**
```hemlock
string.deserialize(): any
```

**Возвращает:** Разобранное значение (объект, массив, число, строка, bool или null)

**Примеры:**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**Поддерживаемые типы:**
- Объекты: `{"key": value}`
- Массивы: `[1, 2, 3]`
- Числа: `42`, `3.14`
- Строки: `"text"`
- Булевы: `true`, `false`
- Null: `null`

**См. также:** Метод `.serialize()` для объектов

---

## Цепочки методов

Методы строк можно объединять в цепочки для краткости:

**Примеры:**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## Полная сводка методов

| Метод          | Сигнатура                                    | Возвращает | Описание                              |
|----------------|----------------------------------------------|------------|---------------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`   | Извлечь подстроку по позиции/длине    |
| `slice`        | `(start: i32, end: i32)`                     | `string`   | Извлечь подстроку по диапазону        |
| `find`         | `(needle: string)`                           | `i32`      | Найти первое вхождение (-1 если нет)  |
| `contains`     | `(needle: string)`                           | `bool`     | Проверить наличие подстроки           |
| `split`        | `(delimiter: string)`                        | `array`    | Разделить в массив                    |
| `trim`         | `()`                                         | `string`   | Удалить пробелы                       |
| `trim_start`   | `()`                                         | `string`   | Удалить начальные пробелы             |
| `trim_end`     | `()`                                         | `string`   | Удалить конечные пробелы              |
| `to_upper`     | `()`                                         | `string`   | Преобразовать в верхний регистр       |
| `to_lower`     | `()`                                         | `string`   | Преобразовать в нижний регистр        |
| `starts_with`  | `(prefix: string)`                           | `bool`     | Проверить начало с префикса           |
| `ends_with`    | `(suffix: string)`                           | `bool`     | Проверить окончание суффиксом         |
| `replace`      | `(old: string, new: string)`                 | `string`   | Заменить первое вхождение             |
| `replace_all`  | `(old: string, new: string)`                 | `string`   | Заменить все вхождения                |
| `repeat`       | `(count: i32)`                               | `string`   | Повторить строку n раз                |
| `char_at`      | `(index: i32)`                               | `rune`     | Получить кодовую точку по индексу     |
| `byte_at`      | `(index: i32)`                               | `u8`       | Получить байт по индексу              |
| `chars`        | `()`                                         | `array`    | Преобразовать в массив рун            |
| `bytes`        | `()`                                         | `array`    | Преобразовать в массив байтов         |
| `to_bytes`     | `()`                                         | `buffer`   | Преобразовать в буфер (устаревший)    |
| `byte_ptr`     | `()`                                         | `ptr`      | Сырой указатель на внутренние байты UTF-8 |
| `deserialize`  | `()`                                         | `any`      | Разобрать JSON-строку                 |

---

## См. также

- [Система типов](type-system.md) - Детали типа строки
- [API массивов](array-api.md) - Методы массивов для результатов split()
- [Операторы](operators.md) - Оператор конкатенации строк
