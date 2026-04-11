# Guida alla Migrazione: v1.x a v2.0.0

## Modifica Non Retrocompatibile: Builtin Spostati nella Stdlib

Hemlock 2.0.0 ha spostato 63 builtin globali nei moduli `@stdlib` per ridurre l'inquinamento del namespace. Il codice che usa queste funzioni senza import riceverà errori "undefined variable".

## Soluzione Rapida

Aggiungi l'istruzione `import` appropriata per ogni funzione. La tabella seguente mostra dove è stato spostato ogni builtin.

### Funzioni Matematiche

```hemlock
// Prima (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// Dopo (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Funzioni spostate:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Gestione dei Segnali

```hemlock
// Prima
signal(SIGINT, handler);

// Dopo
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### File System

```hemlock
// Prima
let f = open("file.txt", "r");

// Dopo
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Processo / Ambiente

```hemlock
// Prima
let home = getenv("HOME");
exec("ls");

// Dopo
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Rete

```hemlock
// Prima
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// Dopo
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Operazioni Atomiche

```hemlock
// Prima
atomic_store(ptr, 42);

// Dopo
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### Callback FFI

```hemlock
// Prima
let cb = callback(my_func);

// Dopo
import { callback, callback_free } from "@stdlib/ffi";
```

### Debug / Stack

```hemlock
// Prima
let info = task_debug_info(task);

// Dopo
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Mappatura Completa dei Moduli

| Funzione/i | Nuovo Modulo |
|------------|-------------|
| Funzioni matematiche (sin, cos, sqrt, ecc.) | `@stdlib/math` |
| `signal`, `raise`, costanti SIG* | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| Costanti AF_*, SOCK_*, POLL*, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| Operazioni `atomic_*` | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Nessuna Altra Modifica Non Retrocompatibile

Tutte le altre funzionalità del linguaggio, la sintassi e le API rimangono retrocompatibili. Il codice esistente necessita solo dell'aggiunta degli import.
