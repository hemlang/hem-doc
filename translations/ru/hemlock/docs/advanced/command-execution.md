# Выполнение команд в Hemlock

Hemlock предоставляет **встроенную функцию `exec()`** для выполнения команд оболочки и захвата их вывода.

## Содержание

- [Обзор](#обзор)
- [Функция exec()](#функция-exec)
- [Объект результата](#объект-результата)
- [Базовое использование](#базовое-использование)
- [Продвинутые примеры](#продвинутые-примеры)
- [Обработка ошибок](#обработка-ошибок)
- [Детали реализации](#детали-реализации)
- [Вопросы безопасности](#вопросы-безопасности)
- [Ограничения](#ограничения)
- [Случаи использования](#случаи-использования)
- [Лучшие практики](#лучшие-практики)
- [Полные примеры](#полные-примеры)

## Обзор

Функция `exec()` позволяет программам Hemlock:
- Выполнять команды оболочки
- Захватывать стандартный вывод (stdout)
- Проверять коды завершения
- Использовать возможности оболочки (каналы, перенаправления и т.д.)
- Интегрироваться с системными утилитами

**Важно:** Команды выполняются через `/bin/sh`, что даёт полные возможности оболочки, но также вносит вопросы безопасности.

## Функция exec()

### Сигнатура

```hemlock
exec(command: string): object
```

**Параметры:**
- `command` (string) - Команда оболочки для выполнения

**Возвращает:** Объект с двумя полями:
- `output` (string) - Вывод stdout команды
- `exit_code` (i32) - Код статуса завершения команды

### Базовый пример

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## Объект результата

Объект, возвращаемый `exec()`, имеет следующую структуру:

```hemlock
{
    output: string,      // stdout команды (захваченный вывод)
    exit_code: i32       // Статус завершения процесса (0 = успех)
}
```

### Поле output

Содержит весь текст, записанный в stdout командой.

**Свойства:**
- Пустая строка, если команда не производит вывода
- Включает переносы строк и пробелы как есть
- Многострочный вывод сохраняется
- Не ограничен по размеру (динамически выделяется)

**Примеры:**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Листинг директории с переносами строк

let r3 = exec("true");
print(r3.output);  // "" (пустая строка)
```

### Поле exit_code

Код статуса завершения команды.

**Значения:**
- `0` обычно означает успех
- `1-255` означают ошибки (соглашение варьируется по командам)
- `-1` если команда не смогла быть выполнена или завершилась аномально

**Примеры:**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (успех)

let r2 = exec("false");
print(r2.exit_code);  // 1 (неудача)

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2 (файл не найден, варьируется по командам)
```

## Базовое использование

### Простая команда

```hemlock
let r = exec("ls -la");
print(r.output);
print("Код завершения: " + typeof(r.exit_code));
```

### Проверка статуса завершения

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Найдено: " + r.output);
} else {
    print("Паттерн не найден");
}
```

### Команды с каналами

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Несколько команд

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Подстановка команд

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Текущая дата
```

## Продвинутые примеры

### Обработка ошибок

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Команда завершилась с ошибкой, код: " + typeof(r.exit_code));
    print("Вывод ошибки: " + r.output);  // Примечание: stderr не захватывается
}
```

### Обработка многострочного вывода

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Строка " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Цепочки команд

**С && (И):**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Настройка завершена");
}
```

**С || (ИЛИ):**
```hemlock
let r = exec("command1 || command2");
// Запускает command2 только если command1 завершилась с ошибкой
```

**С ; (последовательность):**
```hemlock
let r = exec("command1; command2");
// Запускает обе независимо от успеха/неудачи
```

### Использование каналов

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**Сложные конвейеры:**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Паттерны кодов завершения

Разные коды завершения означают разные условия:

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Файл существует");
} else if (r.exit_code == 1) {
    print("Файл не существует");
} else {
    print("Команда test завершилась с ошибкой: " + typeof(r.exit_code));
}
```

### Перенаправления вывода

```hemlock
// Перенаправление stdout в файл (внутри оболочки)
let r1 = exec("echo 'test' > /tmp/output.txt");

// Перенаправление stderr в stdout (Примечание: stderr всё ещё не захватывается Hemlock)
let r2 = exec("command 2>&1");
```

### Переменные окружения

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### Изменения рабочей директории

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Обработка ошибок

### Когда exec() выбрасывает исключения

Функция `exec()` выбрасывает исключение, если команда не может быть выполнена:

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Не удалось выполнить: " + e);
}
```

**Исключения выбрасываются когда:**
- `popen()` завершается с ошибкой (например, не удаётся создать канал)
- Превышены лимиты системных ресурсов
- Ошибки выделения памяти

### Когда exec() НЕ выбрасывает

```hemlock
// Команда выполняется, но возвращает ненулевой код завершения
let r1 = exec("false");
print(r1.exit_code);  // 1 (не исключение)

// Команда не производит вывода
let r2 = exec("true");
print(r2.output);  // "" (не исключение)

// Команда не найдена оболочкой
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127 (не исключение)
```

### Паттерн безопасного выполнения

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Предупреждение: Команда завершилась с кодом " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Ошибка выполнения команды: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## Детали реализации

### Как это работает

**Под капотом:**
- Использует `popen()` для выполнения команд через `/bin/sh`
- Захватывает только stdout (stderr не захватывается)
- Вывод буферизуется динамически (начиная с 4KB, растёт по необходимости)
- Статус завершения извлекается с помощью макросов `WIFEXITED()` и `WEXITSTATUS()`
- Строка вывода правильно завершается нулём

**Поток процесса:**
1. `popen(command, "r")` создаёт канал и форкает процесс
2. Дочерний процесс выполняет `/bin/sh -c "command"`
3. Родитель читает stdout через канал в растущий буфер
4. `pclose()` ожидает дочерний процесс и возвращает статус завершения
5. Статус завершения извлекается и сохраняется в объекте результата

### Соображения производительности

**Затраты:**
- Создаёт новый процесс оболочки для каждого вызова (~1-5мс накладных расходов)
- Вывод сохраняется полностью в памяти (не потоковый)
- Нет поддержки потоковой передачи (ожидает завершения команды)
- Подходит для команд с разумным размером вывода

**Оптимизации:**
- Буфер начинается с 4KB и удваивается при заполнении (эффективное использование памяти)
- Единственный цикл чтения минимизирует системные вызовы
- Нет дополнительного копирования строк

**Когда использовать:**
- Краткосрочные команды (< 1 секунды)
- Умеренный размер вывода (< 10MB)
- Пакетные операции с разумными интервалами

**Когда НЕ использовать:**
- Долгоработающие демоны или сервисы
- Команды, производящие гигабайты вывода
- Обработка данных в реальном времени с потоковой передачей
- Высокочастотное выполнение (> 100 вызовов/секунду)

## Вопросы безопасности

### Риск инъекции оболочки

**КРИТИЧНО:** Команды выполняются оболочкой (`/bin/sh`), что означает **возможность инъекции оболочки**.

**Уязвимый код:**
```hemlock
// ОПАСНО - НЕ ДЕЛАЙТЕ ТАК
let filename = args[1];  // Пользовательский ввод
let r = exec("cat " + filename);  // Инъекция оболочки!
```

**Атака:**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Выполняет: cat ; rm -rf /; echo pwned
```

### Безопасные практики

**1. Никогда не используйте несанитизированный пользовательский ввод:**
```hemlock
// Плохо
let user_input = args[1];
let r = exec("process " + user_input);  // ОПАСНО

// Хорошо - сначала валидируйте
fn is_safe_filename(name: string): bool {
    // Разрешаем только буквенно-цифровые символы, дефис, подчёркивание, точку
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Недопустимое имя файла");
}
```

**2. Используйте белые списки, не чёрные:**
```hemlock
// Хорошо - строгий белый список
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Недопустимая команда");
}
```

**3. Экранируйте специальные символы:**
```hemlock
fn shell_escape(s: string): string {
    // Простое экранирование - обёртываем в одинарные кавычки и экранируем одинарные кавычки
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. Избегайте exec() для файловых операций:**
```hemlock
// Плохо - использовать exec для файловых операций
let r = exec("cat file.txt");

// Хорошо - использовать API файлов Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### Соображения о правах

Команды выполняются с теми же правами, что и процесс Hemlock:

```hemlock
// Если Hemlock запущен от root, команды exec() тоже выполняются от root!
let r = exec("rm -rf /important");  // ОПАСНО если запущено от root
```

**Лучшая практика:** Запускайте Hemlock с минимально необходимыми привилегиями.

## Ограничения

### 1. Нет захвата stderr

Захватывается только stdout, stderr выводится в терминал:

```hemlock
let r = exec("ls /nonexistent");
// r.output пуст
// Сообщение об ошибке появляется в терминале, не захватывается
```

**Обходной путь - перенаправить stderr в stdout:**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// Теперь сообщения об ошибках в r.output
```

### 2. Нет потоковой передачи

Необходимо ждать завершения команды:

```hemlock
let r = exec("long_running_command");
// Блокируется до завершения команды
// Невозможно обрабатывать вывод инкрементально
```

### 3. Нет таймаута

Команды могут выполняться бесконечно:

```hemlock
let r = exec("sleep 1000");
// Блокируется на 1000 секунд
// Нет способа установить таймаут или отменить
```

**Обходной путь - использовать команду timeout:**
```hemlock
let r = exec("timeout 5 long_command");
// Таймаут через 5 секунд
```

### 4. Нет обработки сигналов

Невозможно отправлять сигналы выполняющимся командам:

```hemlock
let r = exec("long_command");
// Невозможно отправить SIGINT, SIGTERM и т.д. команде
```

### 5. Нет контроля процесса

Невозможно взаимодействовать с командой после запуска:

```hemlock
let r = exec("interactive_program");
// Невозможно отправить ввод программе
// Невозможно контролировать выполнение
```

## Случаи использования

### Хорошие случаи использования

**1. Запуск системных утилит:**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Быстрая обработка данных с Unix-инструментами:**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Уникальных строк: " + r.output);
```

**3. Проверка состояния системы:**
```hemlock
let r = exec("df -h");
print("Использование диска:\n" + r.output);
```

**4. Проверки существования файлов:**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Файл существует");
}
```

**5. Генерация отчётов:**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Запущенных экземпляров: " + count);
```

**6. Скрипты автоматизации:**
```hemlock
exec("git add .");
exec("git commit -m 'Авто-коммит'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push не удался");
}
```

### Не рекомендуется для

**1. Долгоработающих сервисов:**
```hemlock
// Плохо
let r = exec("nginx");  // Блокируется навсегда
```

**2. Интерактивных команд:**
```hemlock
// Плохо - невозможно предоставить ввод
let r = exec("ssh user@host");
```

**3. Команд, производящих огромный вывод:**
```hemlock
// Плохо - загружает весь вывод в память
let r = exec("cat 10GB_file.log");
```

**4. Потоковой передачи в реальном времени:**
```hemlock
// Плохо - невозможно обрабатывать вывод инкрементально
let r = exec("tail -f /var/log/app.log");
```

**5. Критичной обработки ошибок:**
```hemlock
// Плохо - stderr не захватывается
let r = exec("critical_operation");
// Невозможно увидеть подробные сообщения об ошибках
```

## Лучшие практики

### 1. Всегда проверяйте коды завершения

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Команда завершилась с ошибкой!");
    // Обработка ошибки
}
```

### 2. Обрезайте вывод при необходимости

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // Удаление завершающего переноса строки
print(clean);  // "test" (без переноса строки)
```

### 3. Валидируйте перед выполнением

```hemlock
fn is_valid_command(cmd: string): bool {
    // Валидация безопасности команды
    return true;  // Ваша логика валидации
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. Используйте try/catch для критических операций

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Команда завершилась с ошибкой";
    }
} catch (e) {
    print("Ошибка: " + e);
    // Очистка или восстановление
}
```

### 5. Предпочитайте API Hemlock вместо exec()

```hemlock
// Плохо - использовать exec для файловых операций
let r = exec("cat file.txt");

// Хорошо - использовать File API Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. Захватывайте stderr при необходимости

```hemlock
// Перенаправление stderr в stdout
let r = exec("command 2>&1");
// Теперь r.output содержит и stdout, и stderr
```

### 7. Используйте возможности оболочки разумно

```hemlock
// Используйте каналы для эффективности
let r = exec("cat large.txt | grep pattern | head -n 10");

// Используйте подстановку команд
let r = exec("echo Текущий пользователь: $(whoami)");

// Используйте условное выполнение
let r = exec("test -f file.txt && cat file.txt");
```

## Полные примеры

### Пример 1: Сборщик системной информации

```hemlock
fn get_system_info() {
    print("=== Системная информация ===");

    // Имя хоста
    let r1 = exec("hostname");
    print("Имя хоста: " + r1.output.trim());

    // Время работы
    let r2 = exec("uptime");
    print("Время работы: " + r2.output.trim());

    // Использование диска
    let r3 = exec("df -h /");
    print("\nИспользование диска:");
    print(r3.output);

    // Использование памяти
    let r4 = exec("free -h");
    print("Использование памяти:");
    print(r4.output);
}

get_system_info();
```

### Пример 2: Анализатор логов

```hemlock
fn analyze_log(logfile: string) {
    print("Анализ лога: " + logfile);

    // Подсчёт общего количества строк
    let r1 = exec("wc -l " + logfile);
    print("Всего строк: " + r1.output.trim());

    // Подсчёт ошибок
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Ошибок: " + errors);
    } else {
        print("Ошибок: 0");
    }

    // Подсчёт предупреждений
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Предупреждений: " + warnings);
    } else {
        print("Предупреждений: 0");
    }

    // Последние ошибки
    print("\nПоследние ошибки:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Использование: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### Пример 3: Git-помощник

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Ошибка: Не git-репозиторий");
        return;
    }

    if (r.output == "") {
        print("Рабочая директория чистая");
    } else {
        print("Изменения:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Добавление всех изменений...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Ошибка добавления файлов");
        return;
    }

    print("Коммит...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Ошибка коммита");
        return;
    }

    print("Коммит успешен");
    print(r2.output);
}

// Использование
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### Пример 4: Скрипт резервного копирования

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Резервное копирование " + source + " в " + dest);

    // Создание директории для бэкапа
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Ошибка создания директории для бэкапа");
        return false;
    }

    // Создание архива с меткой времени
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Создание архива: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Ошибка создания бэкапа:");
        print(r3.output);
        return false;
    }

    print("Резервное копирование успешно завершено");

    // Показать размер бэкапа
    let r4 = exec("du -h " + backup_file);
    print("Размер бэкапа: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Использование: " + args[0] + " <источник> <назначение>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Итог

Функция `exec()` в Hemlock предоставляет:

- Простое выполнение команд оболочки
- Захват вывода (stdout)
- Проверку кодов завершения
- Полный доступ к возможностям оболочки (каналы, перенаправления и т.д.)
- Интеграцию с системными утилитами

Помните:
- Всегда проверяйте коды завершения
- Учитывайте последствия для безопасности (инъекция оболочки)
- Валидируйте пользовательский ввод перед использованием в командах
- Предпочитайте API Hemlock вместо exec() когда доступны
- stderr не захватывается (используйте `2>&1` для перенаправления)
- Команды блокируются до завершения
- Используйте для краткосрочных утилит, не для долгоработающих сервисов

**Чеклист безопасности:**
- Никогда не используйте несанитизированный пользовательский ввод
- Валидируйте весь ввод
- Используйте белые списки для команд
- Экранируйте специальные символы при необходимости
- Запускайте с минимальными привилегиями
- Предпочитайте API Hemlock вместо команд оболочки
