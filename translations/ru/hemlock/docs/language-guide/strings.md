# Строки

Строки Hemlock - это **изменяемые последовательности UTF-8 первого класса** с полной поддержкой Unicode и богатым набором методов для обработки текста. В отличие от многих языков, строки Hemlock изменяемы и нативно работают с кодовыми точками Unicode.

## Обзор

```hemlock
let s = "hello";
s[0] = 'H';             // изменение с помощью rune (теперь "Hello")
print(s.length);        // 5 (количество кодовых точек)
let c = s[0];           // возвращает rune (кодовую точку Unicode)
let msg = s + " world"; // конкатенация
let emoji = "(ракета)";
print(emoji.length);    // 1 (одна кодовая точка)
print(emoji.byte_length); // 4 (четыре байта UTF-8)
```

## Свойства

Строки Hemlock имеют следующие ключевые характеристики:

- **Кодировка UTF-8** - Полная поддержка Unicode (U+0000 до U+10FFFF)
- **Изменяемые** - В отличие от строк Python, JavaScript и Java
- **Индексация по кодовым точкам** - Возвращает `rune` (кодовую точку Unicode), не байт
- **Размещение в куче** - С внутренним отслеживанием емкости
- **Два свойства длины**:
  - `.length` - Количество кодовых точек (число символов)
  - `.byte_length` - Количество байт (размер кодировки UTF-8)

## Поведение UTF-8

Все строковые операции работают с **кодовыми точками** (символами), не с байтами:

```hemlock
let text = "Hello(ракета)World";
print(text.length);        // 11 (кодовых точек)
print(text.byte_length);   // 15 (байт, эмодзи занимает 4 байта)

// Индексация использует кодовые точки
let h = text[0];           // 'H' (rune)
let rocket = text[5];      // '(ракета)' (rune)
```

**Многобайтовые символы считаются как один:**
```hemlock
"Hello".length;      // 5
"(ракета)".length;   // 1 (один эмодзи)
"(привет)".length;   // 2 (два китайских символа)
"cafe".length;       // 4 (e с ударением - одна кодовая точка)
```

## Строковые литералы

```hemlock
// Базовые строки
let s1 = "hello";
let s2 = "world";

// С escape-последовательностями
let s3 = "Line 1\nLine 2\ttabbed";
let s4 = "Quote: \"Hello\"";
let s5 = "Backslash: \\";

// Unicode символы
let s6 = "(ракета) Emoji";
let s7 = "(китайские символы)";
```

## Шаблонные строки (интерполяция строк)

Используйте обратные кавычки для шаблонных строк со встроенными выражениями:

```hemlock
let name = "Alice";
let age = 30;

// Базовая интерполяция
let greeting = `Hello, ${name}!`;           // "Hello, Alice!"
let info = `${name} is ${age} years old`;   // "Alice is 30 years old"

// Выражения в интерполяции
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// Вызовы методов
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// Вложенные объекты
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lives in ${person.city}`;  // "Bob lives in NYC"

// Многострочные (сохраняют переносы строк)
let multi = `Line 1
Line 2
Line 3`;
```

**Возможности шаблонных строк:**
- Выражения внутри `${...}` вычисляются и преобразуются в строки
- Можно использовать любое допустимое выражение (переменные, вызовы функций, арифметику)
- Строки с обратными кавычками поддерживают те же escape-последовательности что и обычные строки
- Полезно для построения динамических строк без конкатенации

### Экранирование в шаблонных строках

Чтобы включить буквальный `${` в шаблонную строку, экранируйте знак доллара:

```hemlock
let price = 100;
let text = `Price: \${price} or ${price}`;
// "Price: ${price} or 100"

// Буквальная обратная кавычка
let code = `Use \` for template strings`;
// "Use ` for template strings"
```

### Сложные выражения

Шаблонные строки могут содержать любое допустимое выражение:

```hemlock
// Тернарные выражения
let age = 25;
let status = `Status: ${age >= 18 ? "adult" : "minor"}`;

// Доступ к массиву
let items = ["apple", "banana", "cherry"];
let first = `First item: ${items[0]}`;

// Вызовы функций с аргументами
fn format_price(p) { return "$" + p; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: $99.99"

// Цепочки вызовов методов
let name = "alice";
let formatted = `Hello, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hello, Alice!"
```

### Шаблонные строки vs Конкатенация

Шаблонные строки часто чище чем конкатенация:

```hemlock
// Конкатенация (сложнее читать)
let msg1 = "Hello, " + name + "! You have " + count + " messages.";

// Шаблонная строка (легче читать)
let msg2 = `Hello, ${name}! You have ${count} messages.`;
```

## Индексация и изменение

### Чтение символов

Индексация возвращает `rune` (кодовую точку Unicode):

```hemlock
let s = "Hello";
let first = s[0];      // 'H' (rune)
let last = s[4];       // 'o' (rune)

// Пример UTF-8
let emoji = "Hi(ракета)!";
let rocket = emoji[2];  // '(ракета)' (rune по индексу кодовой точки 2)
```

### Запись символов

Строки изменяемы - вы можете модифицировать отдельные символы:

```hemlock
let s = "hello";
s[0] = 'H';            // Теперь "Hello"
s[4] = '!';            // Теперь "Hell!"

// С Unicode
let msg = "Go!";
msg[0] = '(ракета)';   // Теперь "(ракета)o!"
```

## Конкатенация

Используйте `+` для объединения строк:

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// С переменными
let name = "Alice";
let msg = "Hi, " + name + "!";  // "Hi, Alice!"

// С rune (см. документацию Runes)
let s = "Hello" + '!';          // "Hello!"
```

## Методы строк

Hemlock предоставляет 19 методов строк для комплексной работы с текстом.

### Подстрока и срезы

**`substr(start, length)`** - Извлечь подстроку по позиции и длине:
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world" (начало с 6, длина 5)
let first = s.substr(0, 5);     // "hello"

// Пример UTF-8
let text = "Hi(ракета)!";
let emoji = text.substr(2, 1);  // "(ракета)" (позиция 2, длина 1)
```

**`slice(start, end)`** - Извлечь подстроку по диапазону (end не включается):
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello" (индекс с 0 до 4)
let slice2 = s.slice(6, 11);    // "world"
```

**Разница:**
- `substr(start, length)` - Использует параметр длины
- `slice(start, end)` - Использует конечный индекс (не включая)

### Поиск

**`find(needle)`** - Найти первое вхождение:
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6 (индекс первого вхождения)
let pos2 = s.find("foo");       // -1 (не найдено)
let pos3 = s.find("l");         // 2 (первая 'l')
```

**`contains(needle)`** - Проверить, содержит ли строка подстроку:
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### Разделение и обрезка

**`split(delimiter)`** - Разделить на массив строк:
```hemlock
let csv = "apple,banana,cherry";
let parts = csv.split(",");     // ["apple", "banana", "cherry"]

let words = "one two three".split(" ");  // ["one", "two", "three"]

// Пустой разделитель разделяет по символам
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Удалить начальные/конечные пробелы:
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### Преобразование регистра

**`to_upper()`** - Преобразовать в верхний регистр:
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// Сохраняет не-ASCII
let s2 = "cafe";
let upper2 = s2.to_upper();     // "CAFE"
```

**`to_lower()`** - Преобразовать в нижний регистр:
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### Проверка префикса/суффикса

**`starts_with(prefix)`** - Проверить, начинается ли с префикса:
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - Проверить, заканчивается ли суффиксом:
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### Замена

**`replace(old, new)`** - Заменить первое вхождение:
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (только первое)
```

**`replace_all(old, new)`** - Заменить все вхождения:
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### Повторение

**`repeat(count)`** - Повторить строку n раз:
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### Доступ к символам и байтам

**`char_at(index)`** - Получить кодовую точку Unicode по индексу (возвращает rune):
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h' (rune)

// Пример UTF-8
let emoji = "(ракета)";
let rocket = emoji.char_at(0);  // Возвращает rune U+1F680
```

**`chars()`** - Преобразовать в массив rune (кодовых точек):
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o'] (массив rune)

// Пример UTF-8
let text = "Hi(ракета)";
let chars2 = text.chars();      // ['H', 'i', '(ракета)']
```

**`byte_at(index)`** - Получить значение байта по индексу (возвращает u8):
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII значение 'h')

// Пример UTF-8
let emoji = "(ракета)";
let first_byte = emoji.byte_at(0);  // 240 (первый байт UTF-8)
```

**`bytes()`** - Преобразовать в массив байт (значений u8):
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111] (массив u8)

// Пример UTF-8
let emoji = "(ракета)";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 байта UTF-8)
```

**`to_bytes()`** - Преобразовать в буфер для низкоуровневого доступа:
```hemlock
let s = "hello";
let buf = s.to_bytes();         // Возвращает буфер с байтами UTF-8
print(buf.length);              // 5
free(buf);                      // Не забудьте освободить
```

## Цепочка методов

Все методы строк возвращают новые строки, позволяя создавать цепочки:

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## Полная справка по методам

| Метод | Параметры | Возвращает | Описание |
|-------|-----------|------------|----------|
| `substr(start, length)` | i32, i32 | string | Извлечь подстроку по позиции и длине |
| `slice(start, end)` | i32, i32 | string | Извлечь подстроку по диапазону (end не включается) |
| `find(needle)` | string | i32 | Найти первое вхождение (-1 если не найдено) |
| `contains(needle)` | string | bool | Проверить наличие подстроки |
| `split(delimiter)` | string | array | Разделить на массив строк |
| `trim()` | - | string | Удалить начальные/конечные пробелы |
| `to_upper()` | - | string | Преобразовать в верхний регистр |
| `to_lower()` | - | string | Преобразовать в нижний регистр |
| `starts_with(prefix)` | string | bool | Проверить начало на префикс |
| `ends_with(suffix)` | string | bool | Проверить конец на суффикс |
| `replace(old, new)` | string, string | string | Заменить первое вхождение |
| `replace_all(old, new)` | string, string | string | Заменить все вхождения |
| `repeat(count)` | i32 | string | Повторить строку n раз |
| `char_at(index)` | i32 | rune | Получить кодовую точку по индексу |
| `byte_at(index)` | i32 | u8 | Получить значение байта по индексу |
| `chars()` | - | array | Преобразовать в массив rune |
| `bytes()` | - | array | Преобразовать в массив байт u8 |
| `to_bytes()` | - | buffer | Преобразовать в буфер (нужно освободить) |

## Примеры

### Пример: Обработка текста

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Нормализация пробелов
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### Пример: Парсер CSV

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "apple, banana , cherry";
let fields = parse_csv_line(csv);  // ["apple", "banana", "cherry"]
```

### Пример: Счетчик слов

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "The quick brown fox";
let count = count_words(sentence);  // 4
```

### Пример: Валидация строк

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## Управление памятью

Строки размещаются в куче с внутренним подсчетом ссылок:

- **Создание**: Размещаются в куче с отслеживанием емкости
- **Конкатенация**: Создает новую строку (старые строки не изменяются)
- **Методы**: Большинство методов возвращают новые строки
- **Время жизни**: Строки используют подсчет ссылок и автоматически освобождаются при выходе из области видимости

**Автоматическая очистка:**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // Новое выделение
}  // Обе s и s2 автоматически освобождаются при возврате функции
```

**Примечание:** Локальные строковые переменные автоматически очищаются при выходе из области видимости. Используйте `free()` только для ранней очистки до конца области или для долгоживущих/глобальных данных. См. [Управление памятью](memory.md#internal-reference-counting) для деталей.

## Лучшие практики

1. **Используйте индексацию по кодовым точкам** - Строки используют позиции кодовых точек, не байтовые смещения
2. **Тестируйте с Unicode** - Всегда тестируйте строковые операции с многобайтовыми символами
3. **Предпочитайте неизменяющие операции** - Используйте методы, возвращающие новые строки, а не мутацию
4. **Проверяйте границы** - Индексация строк не проверяет границы (возвращает null/ошибку при недопустимом)
5. **Нормализуйте ввод** - Используйте `trim()` и `to_lower()` для пользовательского ввода

## Распространенные ловушки

### Ловушка: Путаница байт vs кодовая точка

```hemlock
let emoji = "(ракета)";
print(emoji.length);        // 1 (кодовая точка)
print(emoji.byte_length);   // 4 (байты)

// Не смешивайте байтовые и кодовые операции
let byte = emoji.byte_at(0);  // 240 (первый байт)
let char = emoji.char_at(0);  // '(ракета)' (полная кодовая точка)
```

### Ловушка: Неожиданности мутации

```hemlock
let s1 = "hello";
let s2 = s1;       // Поверхностная копия
s1[0] = 'H';       // Изменяет s1
print(s2);         // Все еще "hello" (строки - типы значений)
```

## Связанные темы

- [Руны](runes.md) - Тип кодовых точек Unicode, используемый в индексации строк
- [Массивы](arrays.md) - Методы строк часто возвращают или работают с массивами
- [Типы](types.md) - Детали типа string и преобразования

## См. также

- **Кодировка UTF-8**: См. раздел "Строки" в CLAUDE.md
- **Преобразования типов**: См. [Типы](types.md) для преобразований строк
- **Память**: См. [Память](memory.md) для деталей размещения строк
