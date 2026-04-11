# Справочник по встроенным функциям

Полный справочник по всем встроенным функциям и константам Hemlock v2.0.0.

> **Критическое изменение v2.0.0:** 63 встроенные функции были перемещены из глобального пространства
> имён в модули `@stdlib`. Функции вроде `sin()`, `open()`, `exec()`, `signal()` и
> константы вроде `SIGINT`, `AF_INET` теперь требуют импортов. См. [Перемещено в stdlib](#перемещено-в-модули-stdlib)
> для полного списка.

---

## Глобальные встроенные (без импорта)

Доступны везде без оператора `import`.

### Ввод/Вывод

| Функция | Описание |
|---------|----------|
| `print(value, ...)` | Вывести значения в stdout с переводом строки |
| `write(value)` | Вывести значение в stdout без перевода строки (немедленный сброс) |
| `eprint(value, ...)` | Вывести значения в stderr с переводом строки |
| `read_line()` | Прочитать строку из stdin; возвращает `string` или `null` при EOF |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline (без \n)
eprint("error!");           // -> stderr
let name = read_line();     // блокирует до ввода
```

### Управление памятью

| Функция | Описание |
|---------|----------|
| `alloc(size)` | Выделить `size` байтов сырой памяти, возвращает `ptr` |
| `talloc(type, count)` | Типизированное выделение: `talloc(i32, 10)` выделяет 10 i32 |
| `realloc(ptr, new_size)` | Изменить размер ранее выделенной памяти |
| `free(ptr)` | Освободить выделенную память |
| `memset(ptr, value, size)` | Заполнить `size` байтов значением `value` |
| `memcpy(dest, src, size)` | Копировать `size` байтов из `src` в `dest` |
| `buffer(size)` | Создать буфер с проверкой границ размером `size` байтов |

```hemlock
let p = alloc(64);       // сырой указатель, без проверки границ
let b = buffer(64);      // безопасный буфер, с проверкой границ
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // ручная очистка
```

### Система типов

| Функция | Описание |
|---------|----------|
| `typeof(value)` | Возвращает имя типа как строку (`"i32"`, `"string"` и др.) |
| `typeid(value)` | Возвращает тип как целочисленную константу (быстрее `typeof()` для сравнений) |
| `sizeof(type)` | Возвращает размер типа в байтах (`sizeof(i32)` → 4) |

**Конструкторы типов** (для преобразования и типизированного выделения):

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Псевдонимы типов:** `integer` (i32), `number` (f64), `byte` (u8)

**Константы TYPEID** (для использования с `typeid()`):

| Константа | Значение | Константа | Значение |
|-----------|----------|-----------|----------|
| `TYPEID_I8` | 0 | `TYPEID_STRING` | 11 |
| `TYPEID_I16` | 1 | `TYPEID_RUNE` | 12 |
| `TYPEID_I32` | 2 | `TYPEID_PTR` | 13 |
| `TYPEID_I64` | 3 | `TYPEID_BUFFER` | 14 |
| `TYPEID_U8` | 4 | `TYPEID_ARRAY` | 15 |
| `TYPEID_U16` | 5 | `TYPEID_OBJECT` | 16 |
| `TYPEID_U32` | 6 | `TYPEID_FILE` | 17 |
| `TYPEID_U64` | 7 | `TYPEID_FUNCTION` | 18 |
| `TYPEID_F32` | 8 | `TYPEID_TASK` | 19 |
| `TYPEID_F64` | 9 | `TYPEID_CHANNEL` | 20 |
| `TYPEID_BOOL` | 10 | `TYPEID_NULL` | 21 |

```hemlock
typeof(42);         // "i32"
typeof("hello");    // "string"
sizeof(i64);        // 8
let n = i32("42");  // парсинг строки в i32

// typeid() возвращает целое число - быстрее сравнения строк typeof()
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("целочисленный тип");
}
```

### Управление потоком

| Функция | Описание |
|---------|----------|
| `assert(condition, message?)` | Паника, если условие ложно |
| `panic(message)` | Немедленный невосстановимый выход (не перехватывается try/catch) |

```hemlock
assert(x > 0, "x must be positive");
panic("unrecoverable error");
```

### Параллелизм

| Функция | Описание |
|---------|----------|
| `spawn(fn, args...)` | Запустить асинхронную задачу, возвращает дескриптор задачи |
| `spawn_with(options, fn, args...)` | Запуск с настройками потока (`stack_size` в байтах, `name` строка макс. 16 символов) |
| `join(task)` | Дождаться завершения задачи, получить результат |
| `detach(task)` | Позволить задаче работать независимо (запустил и забыл) |
| `channel(capacity?)` | Создать канал коммуникации (0 = небуферизованный) |
| `select(channels)` | Ожидание на нескольких каналах |
| `apply(fn, args_array)` | Вызвать функцию с массивом аргументов |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### Вспомогательные функции указателей / FFI

Глобальные, так как являются низкоуровневыми примитивами для `alloc`/`free`.

| Функция | Описание |
|---------|----------|
| `ptr_offset(ptr, bytes)` | Сместить указатель на bytes байтов |
| `ptr_null()` | Получить нулевой указатель |
| `ptr_to_buffer(ptr, size)` | Обернуть указатель в буфер с проверкой границ |
| `buffer_ptr(buffer)` | Получить сырой указатель из буфера |

**Чтение/запись/разыменование указателей** для всех числовых типов и `ptr`:

```
ptr_read_i8, ptr_read_i16, ptr_read_i32, ptr_read_i64
ptr_read_u8, ptr_read_u16, ptr_read_u32, ptr_read_u64
ptr_read_f32, ptr_read_f64, ptr_read_ptr

ptr_write_i8, ptr_write_i16, ptr_write_i32, ptr_write_i64
ptr_write_u8, ptr_write_u16, ptr_write_u32, ptr_write_u64
ptr_write_f32, ptr_write_f64, ptr_write_ptr

ptr_deref_i8, ptr_deref_i16, ptr_deref_i32, ptr_deref_i64
ptr_deref_u8, ptr_deref_u16, ptr_deref_u32, ptr_deref_u64
ptr_deref_f32, ptr_deref_f64, ptr_deref_ptr
```

Все функции `ptr_read_*`, `ptr_write_*` и `ptr_deref_*` принимают как `ptr`, так и `buffer` напрямую:

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Также работает напрямую с буферами (без buffer_ptr())
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Перемещено в модули stdlib

Эти встроенные были перемещены в v2.0.0 и теперь требуют импортов.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Функции:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Константы:** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Функции:** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Функции:** `signal`, `raise`

**Константы:** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Функции:** `socket_create`, `dns_resolve`, `poll`

**Константы:** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Функции:** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Функции:** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Функции:** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Функции (i32):** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Функции (i64):** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Функции:** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Функции:** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Функции:** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Функции:** `string_concat_many`

---

## Руководство по миграции (v1.x → v2.0.0)

### До (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### После (v2.0.0)
```hemlock
import { sin, PI } from "@stdlib/math";
import { get_pid } from "@stdlib/env";
import { signal, SIGUSR1 } from "@stdlib/signal";
import { open } from "@stdlib/fs";
import { exec } from "@stdlib/process";

let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

Сами вызовы функций идентичны -- меняются только импорты.
