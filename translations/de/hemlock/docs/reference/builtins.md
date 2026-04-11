# Eingebaute Funktionen Referenz

Vollständige Referenz für alle eingebauten Funktionen und Konstanten in Hemlock v2.0.0.

> **v2.0.0 Breaking Change:** 63 Builtins wurden aus dem globalen Namensraum in
> `@stdlib`-Module verschoben. Funktionen wie `sin()`, `open()`, `exec()`, `signal()` und
> Konstanten wie `SIGINT`, `AF_INET` erfordern jetzt Imports. Siehe [In Stdlib verschoben](#in-stdlib-module-verschoben)
> für die vollständige Liste.

---

## Globale Builtins (kein Import erforderlich)

Diese sind überall ohne `import`-Anweisung verfügbar.

### I/O

| Funktion | Beschreibung |
|----------|-------------|
| `print(value, ...)` | Werte auf stdout mit Zeilenumbruch ausgeben |
| `write(value)` | Wert auf stdout ohne Zeilenumbruch ausgeben (sofortiges Flushing) |
| `eprint(value, ...)` | Werte auf stderr mit Zeilenumbruch ausgeben |
| `read_line()` | Zeile von stdin lesen; gibt `string` oder `null` bei EOF zurück |

```hemlock
print("Hello", "world");    // Hello world\n
write("kein Zeilenumbruch"); // kein Zeilenumbruch (kein \n)
eprint("Fehler!");           // -> stderr
let name = read_line();      // blockiert bis Eingabe
```

### Speicherverwaltung

| Funktion | Beschreibung |
|----------|-------------|
| `alloc(size)` | `size` Bytes Roh-Speicher allokieren, gibt `ptr` zurück |
| `talloc(type, count)` | Typisierte Allokation: `talloc(i32, 10)` allokiert 10 i32s |
| `realloc(ptr, new_size)` | Zuvor allokierten Speicher vergrößern/verkleinern |
| `free(ptr)` | Allokierten Speicher freigeben |
| `memset(ptr, value, size)` | `size` Bytes auf `value` setzen |
| `memcpy(dest, src, size)` | `size` Bytes von `src` nach `dest` kopieren |
| `buffer(size)` | Grenzengeprüften Buffer mit `size` Bytes erstellen |

```hemlock
let p = alloc(64);       // roher Zeiger, keine Grenzenprüfung
let b = buffer(64);      // sicherer Buffer, grenzengeprüft
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // manuelle Bereinigung
```

### Typsystem

| Funktion | Beschreibung |
|----------|-------------|
| `typeof(value)` | Gibt Typnamen als String zurück (`"i32"`, `"string"`, etc.) |
| `typeid(value)` | Gibt Typ als Ganzzahlkonstante zurück (schneller als `typeof()` für Vergleiche) |
| `sizeof(type)` | Gibt Bytegröße eines Typs zurück (`sizeof(i32)` -> 4) |

**Typkonstruktoren** (für Konvertierung und typisierte Allokation):

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Typaliase:** `integer` (i32), `number` (f64), `byte` (u8)

**TYPEID-Konstanten** (für Verwendung mit `typeid()`):

| Konstante | Wert | Konstante | Wert |
|-----------|------|-----------|------|
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
let n = i32("42");  // String zu i32 parsen

// typeid() gibt eine Ganzzahl zurück - schneller als typeof()-String-Vergleiche
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("Ganzzahl-Typ");
}
```

### Kontrollfluss

| Funktion | Beschreibung |
|----------|-------------|
| `assert(condition, message?)` | Panic wenn Bedingung falsch |
| `panic(message)` | Sofortiger nicht behebbarer Abbruch (nicht durch try/catch abfangbar) |

```hemlock
assert(x > 0, "x muss positiv sein");
panic("nicht behebbarer Fehler");
```

### Nebenläufigkeit

| Funktion | Beschreibung |
|----------|-------------|
| `spawn(fn, args...)` | Async-Task starten, gibt Task-Handle zurück |
| `spawn_with(options, fn, args...)` | Starten mit Thread-Konfiguration (`stack_size` in Bytes, `name` String max 16 Zeichen) |
| `join(task)` | Auf Task-Abschluss warten, gibt Ergebnis zurück |
| `detach(task)` | Task unabhängig laufen lassen (Fire-and-Forget) |
| `channel(capacity?)` | Kommunikationskanal erstellen (0 = ungepuffert) |
| `select(channels)` | Auf mehrere Kanäle warten |
| `apply(fn, args_array)` | Funktion mit Array von Argumenten aufrufen |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hallo");
let msg = ch.recv();
```

### Pointer/FFI-Helfer

Diese sind global, weil sie Low-Level-Primitive sind, die mit `alloc`/`free` verwendet werden.

| Funktion | Beschreibung |
|----------|-------------|
| `ptr_offset(ptr, bytes)` | Pointer um Bytes verschieben |
| `ptr_null()` | Null-Pointer erhalten |
| `ptr_to_buffer(ptr, size)` | Pointer in grenzengeprüften Buffer einwickeln |
| `buffer_ptr(buffer)` | Rohen Pointer aus Buffer holen |

**Pointer-Lesen/Schreiben/Deref** für alle numerischen Typen und `ptr`:

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

Alle `ptr_read_*`, `ptr_write_*` und `ptr_deref_*` Funktionen akzeptieren sowohl `ptr`- als auch `buffer`-Typen direkt:

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Funktioniert auch direkt mit Buffern (kein buffer_ptr() nötig)
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## In Stdlib-Module verschoben

Diese Builtins wurden in v2.0.0 verschoben und erfordern jetzt Imports.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Funktionen:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Konstanten:** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Funktionen:** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Funktionen:** `signal`, `raise`

**Konstanten:** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Funktionen:** `socket_create`, `dns_resolve`, `poll`

**Konstanten:** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Funktionen:** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Funktionen:** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Funktionen:** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Funktionen (i32):** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Funktionen (i64):** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Funktionen:** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Funktionen:** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Funktionen:** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Funktionen:** `string_concat_many`

---

## Migrationsleitfaden (v1.x -> v2.0.0)

### Vorher (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### Nachher (v2.0.0)
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

Die Funktionsaufrufe selbst sind identisch -- nur die Imports ändern sich.
