# Обзор стандартной библиотеки

Hemlock поставляется с 53 модулями стандартной библиотеки, охватывающими системное программирование, ввод/вывод, сети, форматы данных, параллелизм и многое другое. Все модули импортируются с префиксом `@stdlib/`.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Категории модулей

### Базовые утилиты

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Утилиты утверждений для тестирования и валидации |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Инспекция задач и управление стеком |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Форматирование строк в стиле printf |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Утилиты итераторов (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Структурированный логгер с уровнями и выводом в файл |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Генерация случайных чисел и перемешивание |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Расширенные утилиты строк (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | BDD-фреймворк тестирования (describe, test, expect) |

### Математика и наука

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Плотные матричные операции (multiply, transpose, determinant, inverse) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Поиск векторного сходства с USearch ANN |

### Память и низкий уровень

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Аллокатор арены (bump allocation) |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Атомарные операции (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Перестановка байтов, преобразование порядка байтов, буферный ввод/вывод |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | Файловый ввод/вывод с отображением в память |

### Файловая система и ввод/вывод

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Файловые и каталоговые операции (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | Неблокирующий файловый ввод/вывод через пул потоков |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Сопоставление файловых шаблонов |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Манипуляция путями (join, dirname, basename, extname) |

### Параллелизм и асинхронность

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Межпроцессное взаимодействие (каналы, очереди сообщений) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Константы сигналов и обработка (SIGINT, SIGTERM и др.) |

### Сети

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | HTTP-клиент (get, post, request с заголовками) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | TCP/UDP-сокеты (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Unix-сокеты (AF_UNIX потоковые/датаграммные) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | Парсинг и манипуляция URL |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | WebSocket-клиент |

### Форматы данных

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, path access |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | Парсинг и генерация TOML |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | Парсинг и генерация YAML |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | Парсинг и генерация CSV |

### Кодирование и криптография

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, hex, URL-кодирование |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | AES-шифрование, RSA-подпись, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Обработка текста

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Регулярные выражения (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Рендеринг шаблонов, совместимый с Jinja2 |

### Дата, время и версионирование

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | Класс DateTime, форматирование, парсинг |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Метки времени, sleep, измерение часов |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Парсинг и сравнение семантических версий |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | Генерация UUID v4 и v7 |

### Система и окружение

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Парсинг аргументов командной строки |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Переменные окружения, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Определение платформы, CPU count, hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Выполнение shell-команд и экранирование аргументов |

### Терминал и UI

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | ANSI-цвета, стили и управление курсором |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Сырой ввод терминала и определение клавиш |

### База данных

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | База данных SQLite, query, exec, транзакции |

### FFI и интероп

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | Управление FFI-коллбэками и константы типов |

### Утилиты

| Модуль | Импорт | Описание |
|--------|--------|----------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Логика повторных попыток с экспоненциальным откатом |

---

## Быстрые примеры

### Чтение и парсинг конфигурационного файла

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connecting to " + db_host);
```

### HTTP-запрос с JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Параллельная обработка

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Хеширование и кодирование

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Рендеринг шаблонов

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Home", "About", "Contact"] });
```

---

## См. также

- [Справочник по встроенным функциям](./builtins.md) -- функции, доступные без импортов
- [Руководство по миграции (v2.0)](../migration-2.0.md) -- встроенные функции, перемещённые в stdlib в v2.0
- Документация отдельных модулей в [`stdlib/docs/`](../../stdlib/docs/)
