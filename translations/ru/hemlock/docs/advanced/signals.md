# Обработка сигналов в Hemlock

Hemlock предоставляет **обработку POSIX-сигналов** для управления системными сигналами, такими как SIGINT (Ctrl+C), SIGTERM и пользовательскими сигналами. Это позволяет осуществлять низкоуровневое управление процессами и межпроцессное взаимодействие.

## Содержание

- [Обзор](#обзор)
- [API сигналов](#api-сигналов)
- [Константы сигналов](#константы-сигналов)
- [Базовая обработка сигналов](#базовая-обработка-сигналов)
- [Продвинутые паттерны](#продвинутые-паттерны)
- [Поведение обработчиков сигналов](#поведение-обработчиков-сигналов)
- [Вопросы безопасности](#вопросы-безопасности)
- [Распространённые случаи использования](#распространённые-случаи-использования)
- [Полные примеры](#полные-примеры)

## Обзор

Обработка сигналов позволяет программам:
- Реагировать на прерывания пользователя (Ctrl+C, Ctrl+Z)
- Реализовывать корректное завершение
- Обрабатывать запросы на завершение
- Использовать пользовательские сигналы для межпроцессного взаимодействия
- Создавать механизмы будильников/таймеров

**Важно:** Обработка сигналов **по своей природе небезопасна** в философии Hemlock. Обработчики могут быть вызваны в любой момент, прерывая нормальное выполнение. Пользователь отвечает за правильную синхронизацию.

## API сигналов

### signal(signum, handler_fn)

Регистрация функции-обработчика сигнала.

**Параметры:**
- `signum` (i32) - Номер сигнала (константа типа SIGINT, SIGTERM)
- `handler_fn` (функция или null) - Функция для вызова при получении сигнала, или `null` для сброса к поведению по умолчанию

**Возвращает:** Предыдущую функцию-обработчик (или `null`, если её не было)

**Пример:**
```hemlock
fn my_handler(sig) {
    print("Перехвачен сигнал: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**Сброс к поведению по умолчанию:**
```hemlock
signal(SIGINT, null);  // Сброс SIGINT к поведению по умолчанию
```

### raise(signum)

Отправка сигнала текущему процессу.

**Параметры:**
- `signum` (i32) - Номер сигнала для отправки

**Возвращает:** `null`

**Пример:**
```hemlock
raise(SIGUSR1);  // Вызов обработчика SIGUSR1
```

## Константы сигналов

Hemlock предоставляет стандартные константы POSIX-сигналов как значения i32.

### Прерывание и завершение

| Константа | Значение | Описание | Распространённый триггер |
|-----------|----------|----------|--------------------------|
| `SIGINT` | 2 | Прерывание с клавиатуры | Ctrl+C |
| `SIGTERM` | 15 | Запрос на завершение | Команда `kill` |
| `SIGQUIT` | 3 | Выход с клавиатуры | Ctrl+\ |
| `SIGHUP` | 1 | Обнаружен обрыв связи | Терминал закрыт |
| `SIGABRT` | 6 | Сигнал прерывания | Функция `abort()` |

**Примеры:**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // Команда kill
signal(SIGHUP, handle_hangup);      // Закрытие терминала
```

### Пользовательские сигналы

| Константа | Значение | Описание | Случай использования |
|-----------|----------|----------|----------------------|
| `SIGUSR1` | 10 | Пользовательский сигнал 1 | Пользовательское IPC |
| `SIGUSR2` | 12 | Пользовательский сигнал 2 | Пользовательское IPC |

**Примеры:**
```hemlock
// Использование для пользовательского взаимодействия
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### Управление процессами

| Константа | Значение | Описание | Примечания |
|-----------|----------|----------|------------|
| `SIGALRM` | 14 | Таймер будильника | После `alarm()` |
| `SIGCHLD` | 17 | Изменение статуса дочернего процесса | Управление процессами |
| `SIGCONT` | 18 | Продолжить, если остановлен | Возобновление после SIGSTOP |
| `SIGSTOP` | 19 | Остановить процесс | **Нельзя перехватить** |
| `SIGTSTP` | 20 | Остановка терминала | Ctrl+Z |

**Примеры:**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### Сигналы ввода-вывода

| Константа | Значение | Описание | Когда отправляется |
|-----------|----------|----------|-------------------|
| `SIGPIPE` | 13 | Разорванный канал | Запись в закрытый канал |
| `SIGTTIN` | 21 | Фоновое чтение с терминала | Фоновый процесс читает TTY |
| `SIGTTOU` | 22 | Фоновая запись в терминал | Фоновый процесс пишет в TTY |

**Примеры:**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## Базовая обработка сигналов

### Перехват Ctrl+C

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("Перехвачен SIGINT!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// Программа продолжает работать...
// Пользователь нажимает Ctrl+C -> вызывается handle_interrupt()

while (!interrupted) {
    // Выполнение работы...
}

print("Выход из-за прерывания");
```

### Сигнатура функции-обработчика

Обработчики сигналов получают один аргумент: номер сигнала (i32)

```hemlock
fn my_handler(signum) {
    print("Получен сигнал: " + typeof(signum));
    // signum содержит номер сигнала (например, 2 для SIGINT)

    if (signum == SIGINT) {
        print("Это SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // Один обработчик для нескольких сигналов
```

### Несколько обработчиков сигналов

Разные обработчики для разных сигналов:

```hemlock
fn handle_int(sig) {
    print("Получен SIGINT");
}

fn handle_term(sig) {
    print("Получен SIGTERM");
}

fn handle_usr1(sig) {
    print("Получен SIGUSR1");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### Сброс к поведению по умолчанию

Передайте `null` в качестве обработчика для сброса к поведению по умолчанию:

```hemlock
// Регистрация пользовательского обработчика
signal(SIGINT, my_handler);

// Позже сброс к поведению по умолчанию (завершение при SIGINT)
signal(SIGINT, null);
```

### Ручная отправка сигналов

Отправка сигналов своему собственному процессу:

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// Ручной вызов обработчика
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## Продвинутые паттерны

### Паттерн корректного завершения

Распространённый паттерн для очистки при завершении:

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Корректное завершение...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// Основной цикл
while (!should_exit) {
    // Выполнение работы...
    // Периодическая проверка флага should_exit
}

print("Очистка завершена");
```

### Счётчик сигналов

Отслеживание количества полученных сигналов:

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Получено " + typeof(signal_count) + " сигналов");
}

signal(SIGUSR1, count_signals);

// Позже...
print("Всего сигналов: " + typeof(signal_count));
```

### Перезагрузка конфигурации по сигналу

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Перезагрузка конфигурации...");
    config = load_config();
    print("Конфигурация перезагружена");
}

signal(SIGHUP, reload_config);  // Перезагрузка по SIGHUP

// Отправка SIGHUP процессу для перезагрузки конфига
// Из оболочки: kill -HUP <pid>
```

### Таймаут с использованием SIGALRM

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Таймаут!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// Установка будильника (ещё не реализовано в Hemlock, только пример)
// alarm(5);  // 5 секунд таймаут

while (!timed_out) {
    // Работа с таймаутом
}
```

### Машина состояний на сигналах

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("Состояние: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("Состояние: " + typeof(state));
}

signal(SIGUSR1, next_state);  // Следующее состояние
signal(SIGUSR2, prev_state);  // Предыдущее состояние

// Управление машиной состояний:
// kill -USR1 <pid>  # Следующее состояние
// kill -USR2 <pid>  # Предыдущее состояние
```

## Поведение обработчиков сигналов

### Важные примечания

**Выполнение обработчиков:**
- Обработчики вызываются **синхронно** при получении сигнала
- Обработчики выполняются в контексте текущего процесса
- Обработчики сигналов разделяют окружение замыкания функции, в которой они определены
- Обработчики могут обращаться и изменять переменные внешней области видимости (как глобальные или захваченные переменные)

**Лучшие практики:**
- Держите обработчики простыми и быстрыми - избегайте долгих операций
- Устанавливайте флаги вместо выполнения сложной логики
- Избегайте вызова функций, которые могут захватывать блокировки
- Помните, что обработчики могут прервать любую операцию

### Какие сигналы можно перехватить

**Можно перехватить и обработать:**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (но программа завершится после возврата обработчика)

**Нельзя перехватить:**
- `SIGKILL` (9) - Всегда завершает процесс
- `SIGSTOP` (19) - Всегда останавливает процесс

**Зависит от системы:**
- Некоторые сигналы имеют поведение по умолчанию, которое может различаться по системам
- Проверьте документацию сигналов вашей платформы для подробностей

### Ограничения обработчиков

```hemlock
fn complex_handler(sig) {
    // Избегайте этого в обработчиках сигналов:

    // Долгие операции
    // process_large_file();

    // Блокирующий I/O
    // let f = open("log.txt", "a");
    // f.write("Сигнал получен\n");

    // Сложные изменения состояния
    // rebuild_entire_data_structure();

    // Простая установка флага безопасна
    let should_stop = true;

    // Простое обновление счётчиков обычно безопасно
    let signal_count = signal_count + 1;
}
```

## Вопросы безопасности

Обработка сигналов **по своей природе небезопасна** в философии Hemlock.

### Состояния гонки

Обработчики могут быть вызваны в любой момент, прерывая нормальное выполнение:

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // Состояние гонки если вызван во время обновления counter
}

signal(SIGUSR1, increment);

// Основной код тоже изменяет counter
counter = counter + 1;  // Может быть прервано обработчиком сигнала
```

**Проблема:** Если сигнал приходит пока основной код обновляет `counter`, результат непредсказуем.

### Безопасность относительно асинхронных сигналов

Hemlock **не** гарантирует безопасность относительно асинхронных сигналов:
- Обработчики могут вызывать любой код Hemlock (в отличие от ограниченных функций C, безопасных для асинхронных сигналов)
- Это обеспечивает гибкость, но требует осторожности пользователя
- Возможны состояния гонки, если обработчик изменяет общее состояние

### Лучшие практики для безопасной обработки сигналов

**1. Используйте атомарные флаги**

Простые присваивания булевых значений обычно безопасны:

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // Простое присваивание безопасно
}

signal(SIGINT, handler);

while (!should_exit) {
    // работа...
}
```

**2. Минимизируйте общее состояние**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // Изменяем только эту одну переменную
    interrupt_count = interrupt_count + 1;
}
```

**3. Откладывайте сложные операции**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // Только устанавливаем флаг
}

signal(SIGHUP, signal_reload);

// В основном цикле:
while (true) {
    if (pending_reload) {
        reload_config();  // Выполняем сложную работу здесь
        pending_reload = false;
    }

    // Обычная работа...
}
```

**4. Избегайте проблем повторного входа**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // Не изменяем данные пока основной код их использует
        return;
    }
    // Безопасно продолжать
}
```

## Распространённые случаи использования

### 1. Корректное завершение сервера

```hemlock
let running = true;

fn shutdown(sig) {
    print("Получен сигнал завершения");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Основной цикл сервера
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Сервер остановлен");
```

### 2. Перезагрузка конфигурации (без перезапуска)

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Перезагрузка конфигурации...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // Использование config...
}
```

### 3. Ротация логов

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // Переименование старого лога, открытие нового
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // Обычное логирование...
    log_file.write("Запись в лог\n");
}
```

### 4. Отчёт о статусе

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Статус: " + typeof(requests_handled) + " запросов обработано");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// Из оболочки: kill -USR1 <pid>
```

### 5. Переключение режима отладки

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Режим отладки: ВКЛ");
    } else {
        print("Режим отладки: ВЫКЛ");
    }
}

signal(SIGUSR2, toggle_debug);

// Из оболочки: kill -USR2 <pid> для переключения
```

## Полные примеры

### Пример 1: Обработчик прерываний с очисткой

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Обнаружено прерывание (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("Получен пользовательский сигнал 1");
    }
}

// Регистрация обработчиков
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// Симуляция работы
let i = 0;
while (running && i < 100) {
    print("Работа... " + typeof(i));

    // Вызов SIGUSR1 каждые 10 итераций
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Всего получено сигналов: " + typeof(signal_count));
```

### Пример 2: Машина состояний на нескольких сигналах

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("Состояние: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("Состояние: " + state);
}

fn report_stats(sig) {
    print("Состояние: " + state);
    print("Запросов: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // Выполнение работы
        request_count = request_count + 1;
    }

    // Проверка каждую итерацию...
}
```

### Пример 3: Контроллер пула воркеров

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Воркеров: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Воркеров: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Завершение...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Основной цикл регулирует пул воркеров на основе worker_count
while (!should_exit) {
    // Управление воркерами на основе worker_count
    // ...
}
```

### Пример 4: Паттерн таймаута

```hemlock
let operation_complete = false;
let timed_out = false;

fn timeout_handler(sig) {
    timed_out = true;
}

signal(SIGALRM, timeout_handler);

// Запуск долгой операции
async fn long_operation() {
    // ... работа
    operation_complete = true;
}

let task = spawn(long_operation);

// Ожидание с таймаутом (ручная проверка)
let elapsed = 0;
while (!operation_complete && elapsed < 1000) {
    // Сон или проверка
    elapsed = elapsed + 1;
}

if (!operation_complete) {
    print("Операция прервана по таймауту");
    detach(task);  // Прекращаем ожидание
} else {
    join(task);
    print("Операция завершена");
}
```

## Отладка обработчиков сигналов

### Добавление диагностических выводов

```hemlock
fn debug_handler(sig) {
    print("Обработчик вызван для сигнала: " + typeof(sig));
    print("Стек: (пока недоступно)");

    // Ваша логика обработчика...
}

signal(SIGINT, debug_handler);
```

### Подсчёт вызовов обработчика

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Вызов обработчика #" + typeof(handler_calls));

    // Ваша логика обработчика...
}
```

### Тестирование с raise()

```hemlock
fn test_handler(sig) {
    print("Тестовый сигнал получен: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// Тестирование ручной отправкой
raise(SIGUSR1);
print("Обработчик должен был быть вызван");
```

## Итог

Обработка сигналов в Hemlock предоставляет:

- Обработка POSIX-сигналов для низкоуровневого управления процессами
- 15 стандартных констант сигналов
- Простой API signal() и raise()
- Гибкие функции-обработчики с поддержкой замыканий
- Несколько сигналов могут использовать общие обработчики

Помните:
- Обработка сигналов по своей природе небезопасна - используйте с осторожностью
- Держите обработчики простыми и быстрыми
- Используйте флаги для изменений состояния, не сложные операции
- Обработчики могут прервать выполнение в любой момент
- Невозможно перехватить SIGKILL или SIGSTOP
- Тщательно тестируйте обработчики с raise()

Распространённые паттерны:
- Корректное завершение (SIGINT, SIGTERM)
- Перезагрузка конфигурации (SIGHUP)
- Ротация логов (SIGUSR1)
- Отчёт о статусе (SIGUSR1/SIGUSR2)
- Переключение режима отладки (SIGUSR2)
