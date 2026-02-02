# Справочник по API файлов

Полный справочник по системе ввода-вывода файлов Hemlock.

---

## Обзор

Hemlock предоставляет **API файловых объектов** для файловых операций с надлежащей обработкой ошибок и управлением ресурсами. Файлы должны открываться и закрываться вручную.

**Ключевые особенности:**
- Файловый объект с методами
- Чтение/запись текстовых и бинарных данных
- Позиционирование и перемещение
- Корректные сообщения об ошибках
- Ручное управление ресурсами (без RAII)

---

## Тип файла

**Тип:** `file`

**Описание:** Дескриптор файла для операций ввода-вывода

**Свойства (только для чтения):**
- `.path` - Путь к файлу (string)
- `.mode` - Режим открытия (string)
- `.closed` - Закрыт ли файл (bool)

---

## Открытие файлов

### open

Открыть файл для чтения, записи или обоих действий.

**Сигнатура:**
```hemlock
open(path: string, mode?: string): file
```

**Параметры:**
- `path` - Путь к файлу (относительный или абсолютный)
- `mode` (необязательно) - Режим открытия (по умолчанию: `"r"`)

**Возвращает:** Файловый объект

**Режимы:**
- `"r"` - Чтение (по умолчанию)
- `"w"` - Запись (очистка существующего файла)
- `"a"` - Добавление
- `"r+"` - Чтение и запись
- `"w+"` - Чтение и запись (очистка)
- `"a+"` - Чтение и добавление

**Примеры:**
```hemlock
// Режим чтения (по умолчанию)
let f = open("data.txt");
let f_read = open("data.txt", "r");

// Режим записи (очистка)
let f_write = open("output.txt", "w");

// Режим добавления
let f_append = open("log.txt", "a");

// Режим чтения/записи
let f_rw = open("data.bin", "r+");

// Чтение/запись (очистка)
let f_rw_trunc = open("output.bin", "w+");

// Чтение/добавление
let f_ra = open("log.txt", "a+");
```

**Обработка ошибок:**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Не удалось открыть:", e);
    // Ошибка: Не удалось открыть 'missing.txt': Нет такого файла или каталога
}
```

**Важно:** Файлы должны закрываться вручную с помощью `f.close()` во избежание утечки файловых дескрипторов.

---

## Методы файла

### Чтение

#### read

Прочитать текст из файла.

**Сигнатура:**
```hemlock
file.read(size?: i32): string
```

**Параметры:**
- `size` (необязательно) - Количество байтов для чтения (если пропущено, читает до конца файла)

**Возвращает:** Строку с содержимым файла

**Примеры:**
```hemlock
let f = open("data.txt", "r");

// Прочитать весь файл
let all = f.read();
print(all);

// Прочитать указанное количество байтов
let chunk = f.read(1024);

f.close();
```

**Поведение:**
- Читает с текущей позиции в файле
- Возвращает пустую строку в конце файла
- Перемещает позицию в файле

**Ошибки:**
- Чтение из закрытого файла
- Чтение из файла, открытого только для записи

---

#### read_bytes

Прочитать бинарные данные из файла.

**Сигнатура:**
```hemlock
file.read_bytes(size: i32): buffer
```

**Параметры:**
- `size` - Количество байтов для чтения

**Возвращает:** Буфер с бинарными данными

**Примеры:**
```hemlock
let f = open("data.bin", "r");

// Прочитать 256 байтов
let binary = f.read_bytes(256);
print(binary.length);       // 256

// Обработка бинарных данных
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**Поведение:**
- Читает точное количество байтов
- Возвращает буфер (не строку)
- Перемещает позицию в файле

---

### Запись

#### write

Записать текст в файл.

**Сигнатура:**
```hemlock
file.write(data: string): i32
```

**Параметры:**
- `data` - Строка для записи

**Возвращает:** Количество записанных байтов (i32)

**Примеры:**
```hemlock
let f = open("output.txt", "w");

// Записать текст
let written = f.write("Hello, World!\n");
print("Записано", written, "байтов");

// Множественные записи
f.write("Строка 1\n");
f.write("Строка 2\n");
f.write("Строка 3\n");

f.close();
```

**Поведение:**
- Записывает с текущей позиции в файле
- Возвращает количество записанных байтов
- Перемещает позицию в файле

**Ошибки:**
- Запись в закрытый файл
- Запись в файл, открытый только для чтения

---

#### write_bytes

Записать бинарные данные в файл.

**Сигнатура:**
```hemlock
file.write_bytes(data: buffer): i32
```

**Параметры:**
- `data` - Буфер для записи

**Возвращает:** Количество записанных байтов (i32)

**Примеры:**
```hemlock
let f = open("output.bin", "w");

// Создать буфер
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Записать буфер
let written = f.write_bytes(buf);
print("Записано", written, "байтов");

f.close();
```

**Поведение:**
- Записывает содержимое буфера в файл
- Возвращает количество записанных байтов
- Перемещает позицию в файле

---

### Позиционирование

#### seek

Переместить позицию в файле на указанное смещение в байтах.

**Сигнатура:**
```hemlock
file.seek(position: i32): i32
```

**Параметры:**
- `position` - Смещение в байтах от начала файла

**Возвращает:** Новую позицию в файле (i32)

**Примеры:**
```hemlock
let f = open("data.txt", "r");

// Перейти к байту 100
f.seek(100);

// Прочитать с этой позиции
let chunk = f.read(50);

// Вернуться в начало
f.seek(0);

// Прочитать сначала
let all = f.read();

f.close();
```

**Поведение:**
- Устанавливает позицию файла на абсолютное смещение
- Возвращает новую позицию
- Перемещение за конец файла допускается (создаёт дыру в файле при записи)

---

#### tell

Получить текущую позицию в файле.

**Сигнатура:**
```hemlock
file.tell(): i32
```

**Возвращает:** Текущее смещение в байтах от начала файла (i32)

**Примеры:**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0 (в начале)

f.read(100);
print(f.tell());        // 100 (после чтения)

f.seek(50);
print(f.tell());        // 50 (после перемещения)

f.close();
```

---

### Закрытие

#### close

Закрыть файл (идемпотентно).

**Сигнатура:**
```hemlock
file.close(): null
```

**Возвращает:** `null`

**Примеры:**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// Безопасно вызывать несколько раз
f.close();  // Без ошибки
f.close();  // Без ошибки
```

**Поведение:**
- Закрывает дескриптор файла
- Записывает все ожидающие записи
- Идемпотентно (безопасно вызывать несколько раз)
- Устанавливает свойство `.closed` в `true`

**Важно:** Всегда закрывайте файлы после использования во избежание утечки файловых дескрипторов.

---

## Свойства файла

### .path

Получить путь к файлу.

**Тип:** `string`

**Доступ:** Только для чтения

**Примеры:**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

Получить режим открытия.

**Тип:** `string`

**Доступ:** Только для чтения

**Примеры:**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Проверить, закрыт ли файл.

**Тип:** `bool`

**Доступ:** Только для чтения

**Примеры:**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Обработка ошибок

Все файловые операции включают корректные сообщения об ошибках с контекстом:

### Файл не найден
```hemlock
let f = open("missing.txt", "r");
// Ошибка: Не удалось открыть 'missing.txt': Нет такого файла или каталога
```

### Чтение из закрытого файла
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Ошибка: Невозможно прочитать из закрытого файла 'data.txt'
```

### Запись в файл только для чтения
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Ошибка: Невозможно записать в файл 'readonly.txt', открытый в режиме только для чтения
```

### Использование try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("Ошибка файла:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Паттерны управления ресурсами

### Базовый паттерн

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### С обработкой ошибок

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Всегда закрывать, даже при ошибке
}
```

### Безопасный паттерн

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... обработка содержимого ...
} catch (e) {
    print("Ошибка:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Примеры использования

### Прочитать весь файл

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### Записать текстовый файл

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### Добавить в файл

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Запись в журнал 1");
append_file("log.txt", "Запись в журнал 2");
```

### Прочитать бинарный файл

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Прочитано", binary.length, "байтов");
```

### Записать бинарный файл

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### Прочитать файл построчно

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Строка", i, ":", lines[i]);
    i = i + 1;
}
```

### Копировать файл

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### Прочитать файл порциями

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // Читать по 1КБ за раз
        if (chunk.length == 0) {
            break;  // Конец файла
        }

        // Обработать порцию
        print("Обработка", chunk.length, "байтов");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## Полная сводка методов

| Метод         | Сигнатура                | Возвращает | Описание                     |
|---------------|--------------------------|------------|------------------------------|
| `read`        | `(size?: i32)`           | `string`   | Прочитать текст              |
| `read_bytes`  | `(size: i32)`            | `buffer`   | Прочитать бинарные данные    |
| `write`       | `(data: string)`         | `i32`      | Записать текст               |
| `write_bytes` | `(data: buffer)`         | `i32`      | Записать бинарные данные     |
| `seek`        | `(position: i32)`        | `i32`      | Установить позицию           |
| `tell`        | `()`                     | `i32`      | Получить позицию             |
| `close`       | `()`                     | `null`     | Закрыть файл (идемпотентно)  |

---

## Полная сводка свойств

| Свойство  | Тип      | Доступ          | Описание               |
|-----------|----------|-----------------|------------------------|
| `.path`   | `string` | Только чтение   | Путь к файлу           |
| `.mode`   | `string` | Только чтение   | Режим открытия         |
| `.closed` | `bool`   | Только чтение   | Закрыт ли файл         |

---

## Миграция со старого API

**Старый API (удалён):**
- `read_file(path)` - Используйте `open(path, "r").read()`
- `write_file(path, data)` - Используйте `open(path, "w").write(data)`
- `append_file(path, data)` - Используйте `open(path, "a").write(data)`
- `file_exists(path)` - Пока нет замены

**Пример миграции:**
```hemlock
// Старый (v0.0)
let content = read_file("data.txt");
write_file("output.txt", content);

// Новый (v0.1)
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## См. также

- [Встроенные функции](builtins.md) - Функция `open()`
- [API памяти](memory-api.md) - Тип буфера
- [API строк](string-api.md) - Методы строк для обработки текста
