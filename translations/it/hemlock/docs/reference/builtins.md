# Riferimento delle Funzioni Integrate

Riferimento completo per tutte le funzioni e costanti integrate di Hemlock v2.0.0.

> **Modifica non retrocompatibile v2.0.0:** 63 builtin sono stati spostati dal namespace globale
> ai moduli `@stdlib`. Funzioni come `sin()`, `open()`, `exec()`, `signal()`, e
> costanti come `SIGINT`, `AF_INET` ora richiedono import. Vedi [Spostati nei Moduli Stdlib](#spostati-nei-moduli-stdlib)
> per la lista completa.

---

## Builtin Globali (Nessun Import Richiesto)

Questi sono disponibili ovunque senza alcuna istruzione `import`.

### I/O

| Funzione | Descrizione |
|----------|-------------|
| `print(valore, ...)` | Stampa valori su stdout con nuova riga |
| `write(valore)` | Stampa valore su stdout senza nuova riga (flush immediato) |
| `eprint(valore, ...)` | Stampa valori su stderr con nuova riga |
| `read_line()` | Legge una riga da stdin; restituisce `string` o `null` su EOF |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline (nessun \n)
eprint("error!");           // -> stderr
let name = read_line();     // blocca fino all'input
```

### Gestione della Memoria

| Funzione | Descrizione |
|----------|-------------|
| `alloc(size)` | Alloca `size` byte di memoria grezza, restituisce `ptr` |
| `talloc(type, count)` | Allocazione tipizzata: `talloc(i32, 10)` alloca 10 i32 |
| `realloc(ptr, new_size)` | Ridimensiona memoria precedentemente allocata |
| `free(ptr)` | Libera memoria allocata |
| `memset(ptr, value, size)` | Imposta `size` byte al `value` |
| `memcpy(dest, src, size)` | Copia `size` byte da `src` a `dest` |
| `buffer(size)` | Crea un buffer con controllo dei limiti di `size` byte |

```hemlock
let p = alloc(64);       // puntatore grezzo, nessun controllo limiti
let b = buffer(64);      // buffer sicuro, controllo limiti
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // pulizia manuale
```

### Sistema di Tipi

| Funzione | Descrizione |
|----------|-------------|
| `typeof(valore)` | Restituisce il nome del tipo come stringa (`"i32"`, `"string"`, ecc.) |
| `typeid(valore)` | Restituisce il tipo come costante intera (più veloce di `typeof()` per confronti) |
| `sizeof(tipo)` | Restituisce la dimensione in byte di un tipo (`sizeof(i32)` → 4) |

**Costruttori di tipo** (usati per conversione e allocazione tipizzata):

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Alias di tipo:** `integer` (i32), `number` (f64), `byte` (u8)

**Costanti TYPEID** (per uso con `typeid()`):

| Costante | Valore | Costante | Valore |
|----------|--------|----------|--------|
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
let n = i32("42");  // parsa stringa a i32

// typeid() restituisce un intero - più veloce dei confronti stringa di typeof()
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("tipo intero");
}
```

### Flusso di Controllo

| Funzione | Descrizione |
|----------|-------------|
| `assert(condizione, messaggio?)` | Panic se la condizione è false |
| `panic(messaggio)` | Uscita immediata irrecuperabile (non catturabile da try/catch) |

```hemlock
assert(x > 0, "x deve essere positivo");
panic("errore irrecuperabile");
```

### Concorrenza

| Funzione | Descrizione |
|----------|-------------|
| `spawn(fn, args...)` | Spawna un task asincrono, restituisce handle del task |
| `spawn_with(opzioni, fn, args...)` | Spawn con config per-thread (`stack_size` in byte, `name` stringa max 16 caratteri) |
| `join(task)` | Attende il completamento del task, restituisce il risultato |
| `detach(task)` | Lascia il task eseguire indipendentemente (fire and forget) |
| `channel(capacita?)` | Crea un canale di comunicazione (0 = non bufferizzato) |
| `select(canali)` | Attende su canali multipli |
| `apply(fn, args_array)` | Chiama funzione con array di argomenti |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### Helper Puntatore / FFI

Questi sono globali perché sono primitive di basso livello usate con `alloc`/`free`.

| Funzione | Descrizione |
|----------|-------------|
| `ptr_offset(ptr, bytes)` | Sposta un puntatore di byte |
| `ptr_null()` | Ottiene un puntatore null |
| `ptr_to_buffer(ptr, size)` | Avvolge un puntatore in un buffer con controllo dei limiti |
| `buffer_ptr(buffer)` | Ottiene il puntatore grezzo da un buffer |

**Lettura/scrittura/deref puntatore** per tutti i tipi numerici e `ptr`:

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

Tutte le funzioni `ptr_read_*`, `ptr_write_*` e `ptr_deref_*` accettano sia tipi `ptr` che `buffer` direttamente:

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Funziona anche direttamente con i buffer (nessun buffer_ptr() necessario)
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Spostati nei Moduli Stdlib

Questi builtin sono stati spostati nella v2.0.0 e ora richiedono import.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Funzioni:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Costanti:** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Funzioni:** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Funzioni:** `signal`, `raise`

**Costanti:** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Funzioni:** `socket_create`, `dns_resolve`, `poll`

**Costanti:** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Funzioni:** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Funzioni:** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Funzioni:** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Funzioni (i32):** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Funzioni (i64):** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Funzioni:** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Funzioni:** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Funzioni:** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Funzioni:** `string_concat_many`

---

## Guida alla Migrazione (v1.x → v2.0.0)

### Prima (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### Dopo (v2.0.0)
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

Le chiamate di funzione sono identiche — cambiano solo gli import.
