# Migrationsleitfaden: v1.x zu v2.0.0

## Breaking Change: Builtins in die Stdlib verschoben

Hemlock 2.0.0 hat 63 globale Builtins in `@stdlib`-Module verschoben, um Namespace-Verschmutzung zu reduzieren. Code, der diese Funktionen ohne Imports verwendet, erhält "undefined variable"-Fehler.

## Schnelle Lösung

Fügen Sie die entsprechende `import`-Anweisung für jede Funktion hinzu. Die folgende Tabelle zeigt, wohin jedes Builtin verschoben wurde.

### Mathematische Funktionen

```hemlock
// Vorher (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// Nachher (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Verschobene Funktionen:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Signalbehandlung

```hemlock
// Vorher
signal(SIGINT, handler);

// Nachher
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### Dateisystem

```hemlock
// Vorher
let f = open("file.txt", "r");

// Nachher
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Prozess / Umgebung

```hemlock
// Vorher
let home = getenv("HOME");
exec("ls");

// Nachher
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Netzwerk

```hemlock
// Vorher
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// Nachher
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Atomare Operationen

```hemlock
// Vorher
atomic_store(ptr, 42);

// Nachher
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### FFI-Callbacks

```hemlock
// Vorher
let cb = callback(my_func);

// Nachher
import { callback, callback_free } from "@stdlib/ffi";
```

### Debug / Stack

```hemlock
// Vorher
let info = task_debug_info(task);

// Nachher
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Vollständige Modul-Zuordnung

| Funktion(en) | Neues Modul |
|--------------|-------------|
| Mathematische Funktionen (sin, cos, sqrt, etc.) | `@stdlib/math` |
| `signal`, `raise`, SIG*-Konstanten | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| AF_*, SOCK_*, POLL*-Konstanten, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| `atomic_*`-Operationen | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Keine weiteren Breaking Changes

Alle anderen Sprachfeatures, Syntax und APIs bleiben abwärtskompatibel. Bestehender Code benötigt nur Import-Ergänzungen.
