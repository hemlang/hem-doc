# Referencia de Funciones Integradas

Referencia completa para todas las funciones integradas y constantes en Hemlock v2.0.0.

> **Cambio Importante v2.0.0:** 63 builtins fueron movidos del espacio de nombres global a
> modulos `@stdlib`. Funciones como `sin()`, `open()`, `exec()`, `signal()`, y
> constantes como `SIGINT`, `AF_INET` ahora requieren importaciones. Vea [Movidos a Modulos Stdlib](#movidos-a-modulos-stdlib)
> para la lista completa.

---

## Builtins Globales (Sin Importacion Requerida)

Estos estan disponibles en todas partes sin ninguna sentencia `import`.

### E/S

| Funcion | Descripcion |
|---------|-------------|
| `print(value, ...)` | Imprimir valores a stdout con nueva linea |
| `write(value)` | Imprimir valor a stdout sin nueva linea (vacia inmediatamente) |
| `eprint(value, ...)` | Imprimir valores a stderr con nueva linea |
| `read_line()` | Leer una linea de stdin; retorna `string` o `null` en EOF |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline (no \n)
eprint("error!");           // -> stderr
let name = read_line();     // blocks until input
```

### Gestion de Memoria

| Funcion | Descripcion |
|---------|-------------|
| `alloc(size)` | Asignar `size` bytes de memoria cruda, retorna `ptr` |
| `talloc(type, count)` | Asignacion con tipo: `talloc(i32, 10)` asigna 10 i32s |
| `realloc(ptr, new_size)` | Redimensionar memoria previamente asignada |
| `free(ptr)` | Liberar memoria asignada |
| `memset(ptr, value, size)` | Establecer `size` bytes al `value` |
| `memcpy(dest, src, size)` | Copiar `size` bytes de `src` a `dest` |
| `buffer(size)` | Crear un buffer con verificacion de limites de `size` bytes |

```hemlock
let p = alloc(64);       // raw pointer, no bounds checking
let b = buffer(64);      // safe buffer, bounds checked
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // manual cleanup
```

### Sistema de Tipos

| Funcion | Descripcion |
|---------|-------------|
| `typeof(value)` | Retorna nombre del tipo como string (`"i32"`, `"string"`, etc.) |
| `typeid(value)` | Retorna tipo como constante entera (mas rapido que `typeof()` para comparaciones) |
| `sizeof(type)` | Retorna tamano en bytes de un tipo (`sizeof(i32)` → 4) |

**Constructores de tipo** (usados para conversion y asignacion tipada):

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Alias de tipo:** `integer` (i32), `number` (f64), `byte` (u8)

**Constantes TYPEID** (para uso con `typeid()`):

| Constante | Valor | Constante | Valor |
|-----------|-------|-----------|-------|
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
let n = i32("42");  // parse string to i32

// typeid() retorna un entero - mas rapido que comparaciones de strings con typeof()
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("integer type");
}
```

### Flujo de Control

| Funcion | Descripcion |
|---------|-------------|
| `assert(condition, message?)` | Panico si la condicion es falsa |
| `panic(message)` | Salida inmediata irrecuperable (no capturable por try/catch) |

```hemlock
assert(x > 0, "x must be positive");
panic("unrecoverable error");
```

### Concurrencia

| Funcion | Descripcion |
|---------|-------------|
| `spawn(fn, args...)` | Generar tarea async, retorna manejador de tarea |
| `spawn_with(options, fn, args...)` | Generar con config por hilo (`stack_size` en bytes, `name` string max 16 chars) |
| `join(task)` | Esperar finalizacion de tarea, retorna resultado |
| `detach(task)` | Dejar tarea ejecutandose independientemente (disparar y olvidar) |
| `channel(capacity?)` | Crear canal de comunicacion (0 = sin buffer) |
| `select(channels)` | Esperar en multiples canales |
| `apply(fn, args_array)` | Llamar funcion con array de argumentos |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### Auxiliares de Puntero / FFI

Estos son globales porque son primitivas de bajo nivel usadas con `alloc`/`free`.

| Funcion | Descripcion |
|---------|-------------|
| `ptr_offset(ptr, bytes)` | Desplazar un puntero por bytes |
| `ptr_null()` | Obtener un puntero nulo |
| `ptr_to_buffer(ptr, size)` | Envolver un puntero en un buffer con verificacion de limites |
| `buffer_ptr(buffer)` | Obtener el puntero crudo de un buffer |

**Lectura/escritura/deref de puntero** para todos los tipos numericos y `ptr`:

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

Todas las funciones `ptr_read_*`, `ptr_write_*` y `ptr_deref_*` aceptan tanto tipos `ptr` como `buffer` directamente:

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Tambien funciona directamente con buffers (sin necesidad de buffer_ptr())
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Movidos a Modulos Stdlib

Estos builtins fueron movidos en v2.0.0 y ahora requieren importaciones.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Funciones:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Constantes:** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Funciones:** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Funciones:** `signal`, `raise`

**Constantes:** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Funciones:** `socket_create`, `dns_resolve`, `poll`

**Constantes:** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Funciones:** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Funciones:** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Funciones:** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Funciones (i32):** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Funciones (i64):** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Funciones:** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Funciones:** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Funciones:** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Funciones:** `string_concat_many`

---

## Guia de Migracion (v1.x → v2.0.0)

### Antes (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### Despues (v2.0.0)
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

Las llamadas a funciones en si son identicas -- solo cambian las importaciones.
