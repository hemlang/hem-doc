# Аргументы командной строки в Hemlock

Программы Hemlock могут получать доступ к аргументам командной строки через встроенный **массив `args`**, который автоматически заполняется при запуске программы.

## Содержание

- [Обзор](#обзор)
- [Массив args](#массив-args)
- [Свойства](#свойства)
- [Паттерны итерации](#паттерны-итерации)
- [Распространённые случаи использования](#распространённые-случаи-использования)
- [Паттерны парсинга аргументов](#паттерны-парсинга-аргументов)
- [Лучшие практики](#лучшие-практики)
- [Полные примеры](#полные-примеры)

## Обзор

Массив `args` предоставляет доступ к аргументам командной строки, переданным вашей программе Hemlock:

- **Всегда доступен** - Встроенная глобальная переменная во всех программах Hemlock
- **Имя скрипта включено** - `args[0]` всегда содержит путь/имя скрипта
- **Массив строк** - Все аргументы являются строками
- **Индексация с нуля** - Стандартная индексация массива (0, 1, 2, ...)

## Массив args

### Базовая структура

```hemlock
// args[0] - это всегда имя файла скрипта
// args[1] до args[n-1] - это фактические аргументы
print(args[0]);        // "script.hml"
print(args.length);    // Общее количество аргументов (включая имя скрипта)
```

### Пример использования

**Команда:**
```bash
./hemlock script.hml hello world "test 123"
```

**В script.hml:**
```hemlock
print("Имя скрипта: " + args[0]);     // "script.hml"
print("Всего аргументов: " + typeof(args.length));  // "4"
print("Первый аргумент: " + args[1]);       // "hello"
print("Второй аргумент: " + args[2]);      // "world"
print("Третий аргумент: " + args[3]);       // "test 123"
```

### Справочник по индексам

| Индекс | Содержит | Пример значения |
|--------|----------|-----------------|
| `args[0]` | Путь/имя скрипта | `"script.hml"` или `"./script.hml"` |
| `args[1]` | Первый аргумент | `"hello"` |
| `args[2]` | Второй аргумент | `"world"` |
| `args[3]` | Третий аргумент | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Последний аргумент | (варьируется) |

## Свойства

### Всегда присутствует

`args` - это глобальный массив, доступный во **всех** программах Hemlock:

```hemlock
// Не нужно объявлять или импортировать
print(args.length);  // Работает сразу
```

### Имя скрипта включено

`args[0]` всегда содержит путь/имя скрипта:

```hemlock
print("Запущено: " + args[0]);
```

**Возможные значения args[0]:**
- `"script.hml"` - Просто имя файла
- `"./script.hml"` - Относительный путь
- `"/home/user/script.hml"` - Абсолютный путь
- Зависит от того, как был вызван скрипт

### Тип: Массив строк

Все аргументы хранятся как строки:

```hemlock
// Аргументы: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (строка, не число)
print(args[2]);  // "3.14" (строка, не число)
print(args[3]);  // "true" (строка, не булево значение)

// Конвертируйте при необходимости:
let num = 42;  // Парсите вручную при необходимости
```

### Минимальная длина

Всегда минимум 1 (имя скрипта):

```hemlock
print(args.length);  // Минимум: 1
```

**Даже без аргументов:**
```bash
./hemlock script.hml
```

```hemlock
// В script.hml:
print(args.length);  // 1 (только имя скрипта)
```

### Поведение в REPL

В REPL `args.length` равно 0 (пустой массив):

```hemlock
# Сессия REPL
> print(args.length);
0
```

## Паттерны итерации

### Базовая итерация

Пропустите `args[0]` (имя скрипта) и обрабатывайте фактические аргументы:

```hemlock
let i = 1;
while (i < args.length) {
    print("Аргумент " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**Вывод для: `./hemlock script.hml foo bar baz`**
```
Аргумент 1: foo
Аргумент 2: bar
Аргумент 3: baz
```

### Итерация for-in (включая имя скрипта)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Вывод:**
```
script.hml
foo
bar
baz
```

### Проверка количества аргументов

```hemlock
if (args.length < 2) {
    print("Использование: " + args[0] + " <аргумент>");
    // exit или return
} else {
    let arg = args[1];
    // обработка arg
}
```

### Обработка всех аргументов кроме имени скрипта

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Обработка: " + arg);
}
```

## Распространённые случаи использования

### 1. Простая обработка аргументов

Проверка обязательного аргумента:

```hemlock
if (args.length < 2) {
    print("Использование: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Обработка файла: " + filename);
    // ... обработка файла
}
```

**Использование:**
```bash
./hemlock script.hml data.txt
# Вывод: Обработка файла: data.txt
```

### 2. Несколько аргументов

```hemlock
if (args.length < 3) {
    print("Использование: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Вход: " + input_file);
    print("Выход: " + output_file);

    // Обработка файлов...
}
```

**Использование:**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. Переменное количество аргументов

Обработка всех предоставленных аргументов:

```hemlock
if (args.length < 2) {
    print("Использование: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Обработка " + typeof(args.length - 1) + " файлов:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**Использование:**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Справочное сообщение

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Использование: " + args[0] + " [ОПЦИИ] <file>");
    print("Опции:");
    print("  -h, --help     Показать это справочное сообщение");
    print("  -v, --verbose  Включить подробный вывод");
} else {
    // Обычная обработка
}
```

### 5. Валидация аргументов

```hemlock
fn validate_file(filename: string): bool {
    // Проверка существования файла (пример)
    return filename != "";
}

if (args.length < 2) {
    print("Ошибка: Имя файла не указано");
} else if (!validate_file(args[1])) {
    print("Ошибка: Недопустимый файл: " + args[1]);
} else {
    print("Обработка: " + args[1]);
}
```

## Паттерны парсинга аргументов

### Именованные аргументы (флаги)

Простой паттерн для именованных аргументов:

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Подробный режим включён");
}
print("Вход: " + input_file);
print("Выход: " + output_file);
```

**Использование:**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Булевы флаги

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### Аргументы со значениями

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // Нужно парсить строку в int
        }
    }
    i = i + 1;
}
```

### Смешанные позиционные и именованные аргументы

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // Трактовать как позиционный аргумент
        positional.push(args[i]);
    }
    i = i + 1;
}

// Присвоение позиционных аргументов
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### Вспомогательная функция парсера аргументов

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // Позиционный аргумент
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Подробный: " + typeof(opts.verbose));
print("Выход: " + opts.output);
print("Файлов: " + typeof(opts.files.length));
```

## Лучшие практики

### 1. Всегда проверяйте количество аргументов

```hemlock
// Хорошо
if (args.length < 2) {
    print("Использование: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// Плохо - может упасть если нет аргументов
process_file(args[1]);  // Ошибка если args.length == 1
```

### 2. Предоставляйте информацию об использовании

```hemlock
fn show_usage() {
    print("Использование: " + args[0] + " [ОПЦИИ] <file>");
    print("Опции:");
    print("  -h, --help     Показать справку");
    print("  -v, --verbose  Подробный вывод");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. Валидируйте аргументы

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Ошибка: Отсутствует обязательный аргумент");
        return false;
    }

    if (args[1] == "") {
        print("Ошибка: Пустой аргумент");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // exit или показать использование
}
```

### 4. Используйте описательные имена переменных

```hemlock
// Хорошо
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// Плохо
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Обрабатывайте аргументы с пробелами в кавычках

Оболочка автоматически обрабатывает это:

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. Создавайте объекты аргументов

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Вход: " + arguments.input);
```

## Полные примеры

### Пример 1: Обработчик файлов

```hemlock
// Использование: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Использование: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Обработка " + input + " -> " + output);

    // Обработка файлов
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // Пример обработки
        f_out.write(processed);

        print("Готово!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Пример 2: Пакетный обработчик файлов

```hemlock
// Использование: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Использование: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Обработка " + typeof(args.length - 1) + " файлов:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Обработка: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // Обработка содержимого...
            print("    " + typeof(content.length) + " байт");
        } catch (e) {
            print("    Ошибка: " + e);
        }

        i = i + 1;
    }

    print("Готово!");
}
```

### Пример 3: Продвинутый парсер аргументов

```hemlock
// Использование: ./hemlock app.hml [ОПЦИИ] <files...>
// Опции:
//   --verbose, -v     Включить подробный вывод
//   --output, -o FILE Установить выходной файл
//   --help, -h        Показать справку

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Ошибка: --output требует значение");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Ошибка: Неизвестная опция: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Использование: " + args[0] + " [ОПЦИИ] <files...>");
    print("Опции:");
    print("  --verbose, -v     Включить подробный вывод");
    print("  --output, -o FILE Установить выходной файл");
    print("  --help, -h        Показать эту справку");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Ошибка: Не указаны входные файлы");
    show_help();
} else {
    if (config.verbose) {
        print("Подробный режим включён");
        print("Выходной файл: " + config.output);
        print("Входных файлов: " + typeof(config.files.length));
    }

    // Обработка файлов
    for (let file in config.files) {
        if (config.verbose) {
            print("Обработка: " + file);
        }
        // ... обработка файла
    }
}
```

### Пример 4: Инструмент конфигурации

```hemlock
// Использование: ./hemlock config.hml <action> [arguments]
// Действия:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Использование: " + args[0] + " <action> [arguments]");
    print("Действия:");
    print("  get <key>         Получить значение конфигурации");
    print("  set <key> <value> Установить значение конфигурации");
    print("  list              Показать всю конфигурацию");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Ошибка: 'get' требует ключ");
        } else {
            let key = args[2];
            print("Получение: " + key);
            // ... получить из конфига
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Ошибка: 'set' требует ключ и значение");
        } else {
            let key = args[2];
            let value = args[3];
            print("Установка " + key + " = " + value);
            // ... установить в конфиге
        }
    } else if (action == "list") {
        print("Вывод всей конфигурации:");
        // ... вывести конфиг
    } else {
        print("Ошибка: Неизвестное действие: " + action);
        show_usage();
    }
}
```

## Итог

Поддержка аргументов командной строки в Hemlock предоставляет:

- Встроенный массив `args`, доступный глобально
- Простой доступ к аргументам на основе массива
- Имя скрипта в `args[0]`
- Все аргументы как строки
- Доступные методы массива (.length, .slice, и т.д.)

Помните:
- Всегда проверяйте `args.length` перед доступом к элементам
- `args[0]` - это имя скрипта
- Фактические аргументы начинаются с `args[1]`
- Все аргументы - строки, конвертируйте при необходимости
- Предоставляйте информацию об использовании для удобных инструментов
- Валидируйте аргументы перед обработкой

Распространённые паттерны:
- Простые позиционные аргументы
- Именованные аргументы/флаги (--flag)
- Аргументы со значениями (--option value)
- Справочные сообщения (--help)
- Валидация аргументов
