# Обработка ошибок

Hemlock поддерживает обработку ошибок на основе исключений с `try`, `catch`, `finally`, `throw` и `panic`. Это руководство охватывает восстанавливаемые ошибки с исключениями и невосстанавливаемые ошибки с panic.

## Обзор

```hemlock
// Базовая обработка ошибок
try {
    risky_operation();
} catch (e) {
    print("Error: " + e);
}

// С очисткой
try {
    process_file();
} catch (e) {
    print("Failed: " + e);
} finally {
    cleanup();
}

// Выброс ошибок
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Синтаксис

**Базовый try/catch:**
```hemlock
try {
    // рискованный код
} catch (e) {
    // обработка ошибки, e содержит выброшенное значение
}
```

**Try/finally:**
```hemlock
try {
    // рискованный код
} finally {
    // выполняется всегда, даже если брошено исключение
}
```

**Try/catch/finally:**
```hemlock
try {
    // рискованный код
} catch (e) {
    // обработка ошибки
} finally {
    // код очистки
}
```

### Блок Try

Блок try выполняет операторы последовательно:

```hemlock
try {
    print("Starting...");
    risky_operation();
    print("Success!");  // Только если нет исключения
}
```

**Поведение:**
- Выполняет операторы по порядку
- Если брошено исключение: переходит к `catch` или `finally`
- Если нет исключения: выполняет `finally` (если есть) и продолжает

### Блок Catch

Блок catch получает выброшенное значение:

```hemlock
try {
    throw "oops";
} catch (error) {
    print("Caught: " + error);  // error = "oops"
    // error доступна только здесь
}
// error здесь недоступна
```

**Параметр catch:**
- Получает выброшенное значение (любого типа)
- Область видимости ограничена блоком catch
- Может называться как угодно (по соглашению `e`, `err` или `error`)

**Что можно делать в catch:**
```hemlock
try {
    risky_operation();
} catch (e) {
    // Логировать ошибку
    print("Error: " + e);

    // Повторно выбросить ту же ошибку
    throw e;

    // Выбросить другую ошибку
    throw "different error";

    // Вернуть значение по умолчанию
    return null;

    // Обработать и продолжить
    // (без повторного выброса)
}
```

### Блок Finally

Блок finally **всегда выполняется**:

```hemlock
try {
    print("1: try");
    throw "error";
} catch (e) {
    print("2: catch");
} finally {
    print("3: finally");  // Выполняется всегда
}
print("4: after");

// Вывод: 1: try, 2: catch, 3: finally, 4: after
```

**Когда выполняется finally:**
- После блока try (если нет исключения)
- После блока catch (если исключение поймано)
- Даже если try/catch содержит `return`, `break` или `continue`
- До выхода потока управления из try/catch

**Finally с return:**
```hemlock
fn example() {
    try {
        return 1;  // Возвращает 1 после выполнения finally
    } finally {
        print("cleanup");  // Выполняется перед возвратом
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Return в finally переопределяет - возвращает 2
    }
}
```

**Finally с управлением потоком:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Break после выполнения finally
        }
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

## Оператор Throw

### Базовый Throw

Выбросить любое значение как исключение:

```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
throw ["error", "details"];
```

**Выполнение:**
1. Вычисляет выражение
2. Немедленно переходит к ближайшему охватывающему `catch`
3. Если нет `catch`, распространяется вверх по стеку вызовов

### Выброс ошибок

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "Age cannot be negative";
    }
    if (age > 150) {
        throw "Age is unrealistic";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Validation error: " + e);
}
```

### Выброс объектов ошибок

Создание структурированной информации об ошибке:

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "File does not exist"
        };
    }
    // ... чтение файла
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("File not found: " + e.path);
    }
}
```

### Повторный выброс

Поймать и повторно выбросить ошибки:

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Logging error: " + e);
        throw e;  // Повторный выброс вызывающему
    }
}

try {
    wrapper();
} catch (e) {
    print("Caught in main: " + e);
}
```

## Непойманные исключения

Если исключение распространяется до вершины стека вызовов без перехвата:

```hemlock
fn foo() {
    throw "uncaught!";
}

foo();  // Падает с: Runtime error: uncaught!
```

**Поведение:**
- Программа падает
- Печатает сообщение об ошибке в stderr
- Завершается с ненулевым кодом выхода
- Трассировка стека будет добавлена в будущих версиях

## Panic - невосстанавливаемые ошибки

### Что такое Panic?

`panic()` предназначен для **невосстанавливаемых ошибок**, которые должны немедленно завершить программу:

```hemlock
panic();                    // Сообщение по умолчанию: "panic!"
panic("custom message");    // Пользовательское сообщение
panic(42);                  // Нестроковые значения выводятся
```

**Семантика:**
- **Немедленно завершает** программу с кодом выхода 1
- Печатает сообщение об ошибке в stderr: `panic: <message>`
- **НЕ перехватывается** с помощью try/catch
- Используйте для багов и невосстанавливаемых ошибок

### Panic vs Throw

```hemlock
// throw - Восстанавливаемая ошибка (можно поймать)
try {
    throw "recoverable error";
} catch (e) {
    print("Caught: " + e);  // Успешно поймано
}

// panic - Невосстанавливаемая ошибка (нельзя поймать)
try {
    panic("unrecoverable error");  // Программа немедленно завершается
} catch (e) {
    print("This never runs");       // Никогда не выполняется
}
```

### Когда использовать Panic

**Используйте panic для:**
- **Багов**: Достигнут недостижимый код
- **Недопустимое состояние**: Обнаружено повреждение структуры данных
- **Невосстанавливаемые ошибки**: Критический ресурс недоступен
- **Сбои утверждений**: Когда `assert()` недостаточно

**Примеры:**
```hemlock
// Недостижимый код
fn process_state(state: i32) {
    if (state == 1) {
        return "ready";
    } else if (state == 2) {
        return "running";
    } else if (state == 3) {
        return "stopped";
    } else {
        panic("invalid state: " + typeof(state));  // Не должно произойти
    }
}

// Проверка критического ресурса
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json not found - cannot start");
    }
    // ...
}

// Инвариант структуры данных
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() called on empty stack");
    }
    return stack.pop();
}
```

### Когда НЕ использовать Panic

**Используйте throw вместо для:**
- Валидации пользовательского ввода
- Файл не найден
- Сетевых ошибок
- Ожидаемых условий ошибок

```hemlock
// ПЛОХО: Panic для ожидаемых ошибок
fn divide(a, b) {
    if (b == 0) {
        panic("division by zero");  // Слишком жестко
    }
    return a / b;
}

// ХОРОШО: Throw для ожидаемых ошибок
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";  // Восстанавливаемо
    }
    return a / b;
}
```

## Взаимодействие с управлением потоком

### Return внутри Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Возвращает 1 после выполнения finally
    } finally {
        print("cleanup");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Return в finally переопределяет try return - возвращает 2
    }
}
```

**Правило:** Возвращаемые значения блока finally переопределяют возвращаемые значения try/catch.

### Break/Continue внутри Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Break после выполнения finally
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

**Правило:** Break/continue выполняются после блока finally.

### Вложенные Try/Catch

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Caught: " + e);  // Выводит: Caught: inner
        throw "outer";  // Повторный выброс другой ошибки
    }
} catch (e) {
    print("Caught: " + e);  // Выводит: Caught: outer
}
```

**Правило:** Вложенные блоки try/catch работают как ожидается, внутренние перехваты происходят первыми.

## Распространенные паттерны

### Паттерн: Очистка ресурсов

Всегда используйте `finally` для очистки:

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Error processing file: " + e);
    } finally {
        if (file != null) {
            file.close();  // Всегда закрывает, даже при ошибке
        }
    }
}
```

### Паттерн: Обертывание ошибок

Оборачивание низкоуровневых ошибок контекстом:

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Failed to load config from " + path + ": " + e;
    }
}
```

### Паттерн: Восстановление после ошибки

Предоставление запасного варианта при ошибке:

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "division by zero";
        }
        return a / b;
    } catch (e) {
        print("Error: " + e);
        return null;  // Запасное значение
    }
}
```

### Паттерн: Валидация

Использование исключений для валидации:

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Name is required";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Invalid age";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Invalid email";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "invalid" });
} catch (e) {
    print("Validation failed: " + e);
}
```

### Паттерн: Множество типов ошибок

Использование объектов ошибок для различения типов ошибок:

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Data is null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Expected array" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Array is empty" };
    }

    // ... обработка
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("No data provided");
    } else if (e.type == "TypeError") {
        print("Wrong data type: " + e.message);
    } else {
        print("Error: " + e.message);
    }
}
```

## Лучшие практики

1. **Используйте исключения для исключительных случаев** - Не для обычного управления потоком
2. **Выбрасывайте осмысленные ошибки** - Используйте строки или объекты с контекстом
3. **Всегда используйте finally для очистки** - Гарантирует освобождение ресурсов
4. **Не ловите и не игнорируйте** - Хотя бы логируйте ошибку
5. **Повторно выбрасывайте когда уместно** - Позвольте вызывающему обработать если вы не можете
6. **Panic для багов** - Используйте panic для невосстанавливаемых ошибок
7. **Документируйте исключения** - Ясно показывайте, что могут бросить функции

## Распространенные ловушки

### Ловушка: Проглатывание ошибок

```hemlock
// ПЛОХО: Молчаливый сбой
try {
    risky_operation();
} catch (e) {
    // Ошибка проигнорирована - молчаливый сбой
}

// ХОРОШО: Логирование или обработка
try {
    risky_operation();
} catch (e) {
    print("Operation failed: " + e);
    // Обработать соответственно
}
```

### Ловушка: Переопределение в Finally

```hemlock
// ПЛОХО: Finally переопределяет return
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Возвращает 0, не 42!
    }
}

// ХОРОШО: Не возвращать в finally
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Только очистка, без return
    }
}
```

### Ловушка: Забытая очистка

```hemlock
// ПЛОХО: Файл может быть не закрыт при ошибке
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Может бросить
    file.close();  // Никогда не достигнуто при ошибке
}

// ХОРОШО: Используйте finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Ловушка: Использование Panic для ожидаемых ошибок

```hemlock
// ПЛОХО: Panic для ожидаемой ошибки
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Config file not found");  // Слишком жестко
    }
    return read_file(path);
}

// ХОРОШО: Throw для ожидаемой ошибки
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Config file not found: " + path;  // Восстанавливаемо
    }
    return read_file(path);
}
```

## Примеры

### Пример: Базовая обработка ошибок

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Error: " + e);  // Выводит: Error: division by zero
}
```

### Пример: Управление ресурсами

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("File copied successfully");
    } catch (e) {
        print("Failed to copy file: " + e);
        throw e;  // Повторный выброс
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Пример: Вложенная обработка ошибок

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Failed to process user: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Processed: " + typeof(success_count) + " success, " + typeof(error_count) + " errors");
}
```

### Пример: Пользовательские типы ошибок

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a must be a number", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b must be a number", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Cannot divide by zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Пример: Логика повторных попыток

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // Успех!
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation failed after " + typeof(max_attempts) + " attempts: " + e;
            }
            print("Attempt " + typeof(attempt) + " failed, retrying...");
        }
    }
}

fn unreliable_operation() {
    // Имитация ненадежной операции
    if (random() < 0.7) {
        throw "Operation failed";
    }
    return "Success";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("All retries failed: " + e);
}
```

## Порядок выполнения

Понимание порядка выполнения:

```hemlock
try {
    print("1: try block start");
    throw "error";
    print("2: never reached");
} catch (e) {
    print("3: catch block");
} finally {
    print("4: finally block");
}
print("5: after try/catch/finally");

// Вывод:
// 1: try block start
// 3: catch block
// 4: finally block
// 5: after try/catch/finally
```

## Текущие ограничения

- **Нет трассировки стека** - Непойманные исключения не показывают трассировку стека (планируется)
- **Некоторые встроенные функции завершаются** - Некоторые встроенные функции все еще делают `exit()` вместо throw (будет пересмотрено)
- **Нет пользовательских типов исключений** - Любое значение может быть выброшено, но нет формальной иерархии исключений

## Связанные темы

- [Функции](functions.md) - Исключения и возвраты функций
- [Управление потоком](control-flow.md) - Как исключения влияют на управление потоком
- [Память](memory.md) - Использование finally для очистки памяти

## См. также

- **Семантика исключений**: См. раздел "Обработка ошибок" в CLAUDE.md
- **Panic vs Throw**: Разные случаи использования для разных типов ошибок
- **Гарантия Finally**: Всегда выполняется, даже с return/break/continue
