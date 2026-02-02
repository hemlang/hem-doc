# Файловый ввод-вывод в Hemlock

Hemlock предоставляет **API объекта File** для файловых операций с правильной обработкой ошибок и управлением ресурсами.

## Содержание

- [Обзор](#обзор)
- [Открытие файлов](#открытие-файлов)
- [Методы файлов](#методы-файлов)
- [Свойства файлов](#свойства-файлов)
- [Обработка ошибок](#обработка-ошибок)
- [Управление ресурсами](#управление-ресурсами)
- [Полный справочник API](#полный-справочник-api)
- [Распространённые паттерны](#распространённые-паттерны)
- [Лучшие практики](#лучшие-практики)

## Обзор

API объекта File предоставляет:

- **Явное управление ресурсами** - Файлы должны закрываться вручную
- **Несколько режимов открытия** - Чтение, запись, добавление, чтение/запись
- **Текстовые и бинарные операции** - Чтение/запись как текстовых, так и бинарных данных
- **Поддержка позиционирования** - Произвольный доступ внутри файлов
- **Подробные сообщения об ошибках** - Контекстно-зависимое сообщение об ошибках

**Важно:** Файлы не закрываются автоматически. Вы должны вызывать `f.close()`, чтобы избежать утечки файловых дескрипторов.

## Открытие файлов

Используйте `open(path, mode?)` для открытия файла:

```hemlock
let f = open("data.txt", "r");     // Режим чтения (по умолчанию)
let f2 = open("output.txt", "w");  // Режим записи (усечение)
let f3 = open("log.txt", "a");     // Режим добавления
let f4 = open("data.bin", "r+");   // Режим чтения/записи
```

### Режимы открытия

| Режим | Описание | Файл должен существовать | Усекает | Позиция |
|-------|----------|--------------------------|---------|---------|
| `"r"` | Чтение (по умолчанию) | Да | Нет | Начало |
| `"w"` | Запись | Нет (создаёт) | Да | Начало |
| `"a"` | Добавление | Нет (создаёт) | Нет | Конец |
| `"r+"` | Чтение и запись | Да | Нет | Начало |
| `"w+"` | Чтение и запись | Нет (создаёт) | Да | Начало |
| `"a+"` | Чтение и добавление | Нет (создаёт) | Нет | Конец |

### Примеры

**Чтение существующего файла:**
```hemlock
let f = open("config.json", "r");
// или просто:
let f = open("config.json");  // "r" по умолчанию
```

**Создание нового файла для записи:**
```hemlock
let f = open("output.txt", "w");  // Создаёт или усекает
```

**Добавление в файл:**
```hemlock
let f = open("log.txt", "a");  // Создаёт, если не существует
```

**Режим чтения и записи:**
```hemlock
let f = open("data.bin", "r+");  // Существующий файл, можно читать/писать
```

## Методы файлов

### Чтение

#### read(size?: i32): string

Чтение текста из файла (опциональный параметр размера).

**Без размера (чтение всего):**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // Чтение от текущей позиции до EOF
f.close();
```

**С размером (чтение определённого количества байт):**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // Чтение до 1024 байт
let next = f.read(1024);   // Чтение следующих 1024 байт
f.close();
```

**Возвращает:** Строку, содержащую прочитанные данные, или пустую строку при EOF

**Пример - Чтение всего файла:**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**Пример - Чтение частями:**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // Части по 4KB
    if (chunk == "") { break; }  // Достигнут EOF
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

Чтение бинарных данных (возвращает буфер).

**Параметры:**
- `size` (i32) - Количество байт для чтения

**Возвращает:** Буфер, содержащий прочитанные байты

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // Чтение 256 байт
print(binary.length);  // 256 (или меньше при EOF)

// Доступ к отдельным байтам
let first_byte = binary[0];
print(first_byte);

f.close();
```

**Пример - Чтение всего бинарного файла:**
```hemlock
let f = open("data.bin", "r");
let size = 10240;  // Ожидаемый размер
let data = f.read_bytes(size);
f.close();

// Обработка бинарных данных
let i = 0;
while (i < data.length) {
    let byte = data[i];
    // ... обработка байта
    i = i + 1;
}
```

### Запись

#### write(data: string): i32

Запись текста в файл (возвращает количество записанных байт).

**Параметры:**
- `data` (string) - Текст для записи

**Возвращает:** Количество записанных байт (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Записано " + typeof(written) + " байт");  // "Записано 14 байт"
f.close();
```

**Пример - Запись нескольких строк:**
```hemlock
let f = open("output.txt", "w");
f.write("Строка 1\n");
f.write("Строка 2\n");
f.write("Строка 3\n");
f.close();
```

**Пример - Добавление в лог-файл:**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Приложение запущено\n");
f.write("[INFO] Пользователь вошёл в систему\n");
f.close();
```

#### write_bytes(data: buffer): i32

Запись бинарных данных (возвращает количество записанных байт).

**Параметры:**
- `data` (buffer) - Бинарные данные для записи

**Возвращает:** Количество записанных байт (i32)

```hemlock
let f = open("output.bin", "w");

// Создание бинарных данных
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Записано " + typeof(bytes) + " байт");

f.close();
```

**Пример - Копирование бинарного файла:**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let data = src.read_bytes(1024);
while (data.length > 0) {
    dst.write_bytes(data);
    data = src.read_bytes(1024);
}

src.close();
dst.close();
```

### Позиционирование

#### seek(position: i32): i32

Переход к определённой позиции (возвращает новую позицию).

**Параметры:**
- `position` (i32) - Смещение в байтах от начала файла

**Возвращает:** Новую позицию (i32)

```hemlock
let f = open("data.txt", "r");

// Переход к байту 100
f.seek(100);

// Чтение с позиции 100
let data = f.read(50);

// Сброс к началу
f.seek(0);

f.close();
```

**Пример - Произвольный доступ:**
```hemlock
let f = open("records.dat", "r");

// Чтение записи со смещением 1000
f.seek(1000);
let record1 = f.read_bytes(100);

// Чтение записи со смещением 2000
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Получение текущей позиции в файле.

**Возвращает:** Текущее смещение в байтах (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0 (в начале)

f.read(100);
let pos2 = f.tell();  // 100 (после чтения 100 байт)

f.seek(500);
let pos3 = f.tell();  // 500 (после позиционирования)

f.close();
```

**Пример - Измерение количества прочитанного:**
```hemlock
let f = open("data.txt", "r");

let start = f.tell();
let content = f.read();
let end = f.tell();

let bytes_read = end - start;
print("Прочитано " + typeof(bytes_read) + " байт");

f.close();
```

### Закрытие

#### close()

Закрытие файла (идемпотентно, можно вызывать несколько раз).

```hemlock
let f = open("data.txt", "r");
// ... использование файла
f.close();
f.close();  // Безопасно - нет ошибки при повторном закрытии
```

**Важные примечания:**
- Всегда закрывайте файлы по завершении, чтобы избежать утечки файловых дескрипторов
- Закрытие идемпотентно - можно безопасно вызывать несколько раз
- После закрытия все другие операции вызовут ошибку
- Используйте блоки `finally` для гарантии закрытия файлов даже при ошибках

## Свойства файлов

Объекты файлов имеют три свойства только для чтения:

### path: string

Путь файла, использованный для открытия.

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

Режим, в котором файл был открыт.

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Закрыт ли файл.

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Пример - Проверка, открыт ли файл:**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... обработка содержимого
}

f.close();

if (f.closed) {
    print("Файл теперь закрыт");
}
```

## Обработка ошибок

Все файловые операции включают правильные сообщения об ошибках с контекстом.

### Распространённые ошибки

**Файл не найден:**
```hemlock
let f = open("missing.txt", "r");
// Error: Failed to open 'missing.txt': No such file or directory
```

**Чтение из закрытого файла:**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Error: Cannot read from closed file 'data.txt'
```

**Запись в файл только для чтения:**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Error: Cannot write to file 'readonly.txt' opened in read-only mode
```

**Чтение из файла только для записи:**
```hemlock
let f = open("output.txt", "w");
f.read();
// Error: Cannot read from file 'output.txt' opened in write-only mode
```

### Использование try/catch

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Ошибка чтения файла: " + e);
}
```

## Управление ресурсами

### Базовый паттерн

Всегда закрывайте файлы явно:

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### С обработкой ошибок (рекомендуется)

Используйте `finally` для гарантии закрытия файлов даже при ошибках:

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Всегда закрывать, даже при ошибке
}
```

### Несколько файлов

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Паттерн вспомогательной функции

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Использование:
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## Полный справочник API

### Функции

| Функция | Параметры | Возвращает | Описание |
|---------|-----------|------------|----------|
| `open(path, mode?)` | path: string, mode?: string | File | Открытие файла (режим по умолчанию "r") |

### Методы

| Метод | Параметры | Возвращает | Описание |
|-------|-----------|------------|----------|
| `read(size?)` | size?: i32 | string | Чтение текста (всего или определённое количество байт) |
| `read_bytes(size)` | size: i32 | buffer | Чтение бинарных данных |
| `write(data)` | data: string | i32 | Запись текста, возвращает количество записанных байт |
| `write_bytes(data)` | data: buffer | i32 | Запись бинарных данных, возвращает количество записанных байт |
| `seek(position)` | position: i32 | i32 | Переход к позиции, возвращает новую позицию |
| `tell()` | - | i32 | Получение текущей позиции |
| `close()` | - | null | Закрытие файла (идемпотентно) |

### Свойства (только для чтения)

| Свойство | Тип | Описание |
|----------|-----|----------|
| `path` | string | Путь файла |
| `mode` | string | Режим открытия |
| `closed` | bool | Закрыт ли файл |

## Распространённые паттерны

### Чтение всего файла

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### Запись всего файла

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### Добавление в файл

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Событие произошло\n");
```

### Чтение строк

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Строка " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Обработка больших файлов частями

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // Части по 4KB
            if (chunk == "") { break; }

            // Обработка части
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Копирование бинарного файла

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### Усечение файла

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // Режим "w" усекает
    f.close();
}

truncate_file("empty_me.txt");
```

### Чтение с произвольным доступом

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

### Размер файла

```hemlock
fn file_size(path: string): i32 {
    let f = open(path, "r");
    try {
        // Переход к концу
        let end = f.seek(999999999);  // Большое число
        f.seek(0);  // Сброс
        return end;
    } finally {
        f.close();
    }
}

let size = file_size("data.txt");
print("Размер файла: " + typeof(size) + " байт");
```

### Условное чтение/запись

```hemlock
fn update_file(path: string, condition, new_content: string) {
    let f = open(path, "r+");
    try {
        let content = f.read();

        if (condition(content)) {
            f.seek(0);  // Сброс к началу
            f.write(new_content);
        }
    } finally {
        f.close();
    }
}
```

## Лучшие практики

### 1. Всегда используйте try/finally

```hemlock
// Хорошо
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// Плохо - файл может не закрыться при ошибке
let f = open("data.txt", "r");
let content = f.read();
process(content);  // Если здесь исключение, файл утекает
f.close();
```

### 2. Проверяйте состояние файла перед операциями

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... использование content
}

f.close();
```

### 3. Используйте подходящие режимы

```hemlock
// Только чтение? Используйте "r"
let f = open("config.json", "r");

// Полная замена? Используйте "w"
let f = open("output.txt", "w");

// Добавление в конец? Используйте "a"
let f = open("log.txt", "a");
```

### 4. Обрабатывайте ошибки gracefully

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Предупреждение: Не удалось прочитать " + path + ": " + e);
        return "";
    }
}
```

### 5. Закрывайте файлы в обратном порядке открытия

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... использование файлов
} finally {
    // Закрытие в обратном порядке
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Избегайте чтения больших файлов целиком

```hemlock
// Плохо для больших файлов
let f = open("huge.log", "r");
let content = f.read();  // Загружает весь файл в память
f.close();

// Хорошо - обрабатывать частями
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Итог

API файлового ввода-вывода Hemlock предоставляет:

- Простые, явные файловые операции
- Поддержка текста и бинарных данных
- Произвольный доступ с seek/tell
- Понятные сообщения об ошибках с контекстом
- Идемпотентная операция закрытия

Помните:
- Всегда закрывайте файлы вручную
- Используйте try/finally для безопасности ресурсов
- Выбирайте подходящие режимы открытия
- Обрабатывайте ошибки gracefully
- Обрабатывайте большие файлы частями
