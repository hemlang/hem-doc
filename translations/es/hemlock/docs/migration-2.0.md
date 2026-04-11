# Guia de Migracion: v1.x a v2.0.0

## Cambio Importante: Builtins Movidos a Stdlib

Hemlock 2.0.0 movio 63 builtins globales a modulos `@stdlib` para reducir la contaminacion del espacio de nombres. El codigo que usa estas funciones sin importaciones obtendra errores de "variable indefinida".

## Solucion Rapida

Agregue la sentencia `import` apropiada para cada funcion. La tabla a continuacion muestra donde se movio cada builtin.

### Funciones Matematicas

```hemlock
// Antes (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// Despues (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Funciones movidas:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Manejo de Senales

```hemlock
// Antes
signal(SIGINT, handler);

// Despues
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### Sistema de Archivos

```hemlock
// Antes
let f = open("file.txt", "r");

// Despues
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Proceso / Entorno

```hemlock
// Antes
let home = getenv("HOME");
exec("ls");

// Despues
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Redes

```hemlock
// Antes
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// Despues
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Operaciones Atomicas

```hemlock
// Antes
atomic_store(ptr, 42);

// Despues
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### Callbacks FFI

```hemlock
// Antes
let cb = callback(my_func);

// Despues
import { callback, callback_free } from "@stdlib/ffi";
```

### Debug / Pila

```hemlock
// Antes
let info = task_debug_info(task);

// Despues
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Mapeo Completo de Modulos

| Funcion(es) | Nuevo Modulo |
|-------------|-------------|
| Funciones matematicas (sin, cos, sqrt, etc.) | `@stdlib/math` |
| `signal`, `raise`, constantes SIG* | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| Constantes AF_*, SOCK_*, POLL*, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| Operaciones `atomic_*` | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Sin Otros Cambios Importantes

Todas las demas caracteristicas del lenguaje, sintaxis y APIs permanecen retrocompatibles. El codigo existente solo necesita agregar importaciones.
