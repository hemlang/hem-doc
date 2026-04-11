# Руководство по миграции: v1.x на v2.0.0

## Критическое изменение: встроенные функции перемещены в stdlib

Hemlock 2.0.0 переместил 63 глобальные встроенные функции в модули `@stdlib` для уменьшения загрязнения пространства имён. Код, использующий эти функции без импортов, будет получать ошибки "undefined variable".

## Быстрое исправление

Добавьте соответствующий оператор `import` для каждой функции. Таблица ниже показывает, куда каждая встроенная функция была перемещена.

### Математические функции

```hemlock
// До (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// После (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Перемещённые функции:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Обработка сигналов

```hemlock
// До
signal(SIGINT, handler);

// После
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### Файловая система

```hemlock
// До
let f = open("file.txt", "r");

// После
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Процессы / Окружение

```hemlock
// До
let home = getenv("HOME");
exec("ls");

// После
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Сети

```hemlock
// До
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// После
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Атомарные операции

```hemlock
// До
atomic_store(ptr, 42);

// После
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### FFI-коллбэки

```hemlock
// До
let cb = callback(my_func);

// После
import { callback, callback_free } from "@stdlib/ffi";
```

### Отладка / Стек

```hemlock
// До
let info = task_debug_info(task);

// После
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Полная таблица соответствия модулей

| Функции | Новый модуль |
|---------|-------------|
| Математические функции (sin, cos, sqrt и др.) | `@stdlib/math` |
| `signal`, `raise`, константы SIG* | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| Константы AF_*, SOCK_*, POLL*, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| Операции `atomic_*` | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Других критических изменений нет

Все остальные возможности языка, синтаксис и API остаются обратно совместимыми. Существующий код требует только добавления импортов.
