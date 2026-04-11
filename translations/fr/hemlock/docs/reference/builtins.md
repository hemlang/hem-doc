# Reference des fonctions integrees

Reference complete pour toutes les fonctions et constantes integrees dans Hemlock v2.0.0.

> **Changement cassant v2.0.0 :** 63 builtins ont ete deplaces de l'espace de noms global vers des
> modules `@stdlib`. Les fonctions comme `sin()`, `open()`, `exec()`, `signal()`, et
> les constantes comme `SIGINT`, `AF_INET` necessitent maintenant des imports. Voir [Deplaces vers la Stdlib](#deplaces-vers-les-modules-stdlib)
> pour la liste complete.

---

## Builtins globaux (aucun import requis)

Ces fonctions sont disponibles partout sans aucune instruction `import`.

### E/S

| Fonction | Description |
|----------|-------------|
| `print(value, ...)` | Affiche les valeurs sur stdout avec saut de ligne |
| `write(value)` | Affiche la valeur sur stdout sans saut de ligne (flush immediat) |
| `eprint(value, ...)` | Affiche les valeurs sur stderr avec saut de ligne |
| `read_line()` | Lit une ligne depuis stdin ; retourne `string` ou `null` en fin de fichier |

```hemlock
print("Hello", "world");    // Hello world\n
write("no newline");        // no newline (pas de \n)
eprint("error!");           // -> stderr
let name = read_line();     // bloque jusqu'a l'entree
```

### Gestion de la memoire

| Fonction | Description |
|----------|-------------|
| `alloc(size)` | Alloue `size` octets de memoire brute, retourne `ptr` |
| `talloc(type, count)` | Allocation typee : `talloc(i32, 10)` alloue 10 i32 |
| `realloc(ptr, new_size)` | Redimensionne la memoire precedemment allouee |
| `free(ptr)` | Libere la memoire allouee |
| `memset(ptr, value, size)` | Remplit `size` octets avec `value` |
| `memcpy(dest, src, size)` | Copie `size` octets de `src` vers `dest` |
| `buffer(size)` | Cree un buffer avec verification des limites de `size` octets |

```hemlock
let p = alloc(64);       // pointeur brut, pas de verification des limites
let b = buffer(64);      // buffer securise, verification des limites
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // nettoyage manuel
```

### Systeme de types

| Fonction | Description |
|----------|-------------|
| `typeof(value)` | Retourne le nom du type comme chaine (`"i32"`, `"string"`, etc.) |
| `typeid(value)` | Retourne le type comme constante entiere (plus rapide que `typeof()` pour les comparaisons) |
| `sizeof(type)` | Retourne la taille en octets d'un type (`sizeof(i32)` → 4) |

**Constructeurs de type** (utilises pour la conversion et l'allocation typee) :

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Alias de type :** `integer` (i32), `number` (f64), `byte` (u8)

**Constantes TYPEID** (pour utilisation avec `typeid()`) :

| Constante | Valeur | Constante | Valeur |
|-----------|--------|-----------|--------|
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
let n = i32("42");  // parse une chaine vers i32

// typeid() retourne un entier - plus rapide que les comparaisons de chaines typeof()
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("type entier");
}
```

### Flux de controle

| Fonction | Description |
|----------|-------------|
| `assert(condition, message?)` | Panique si la condition est fausse |
| `panic(message)` | Sortie immediate irrecuperable (non capturable par try/catch) |

```hemlock
assert(x > 0, "x doit etre positif");
panic("erreur irrecuperable");
```

### Concurrence

| Fonction | Description |
|----------|-------------|
| `spawn(fn, args...)` | Lance une tache async, retourne un handle de tache |
| `spawn_with(options, fn, args...)` | Lance avec une config par thread (`stack_size` en octets, `name` chaine max 16 car) |
| `join(task)` | Attend la completion de la tache, retourne le resultat |
| `detach(task)` | Laisse la tache s'executer independamment (fire and forget) |
| `channel(capacity?)` | Cree un canal de communication (0 = non bufferise) |
| `select(channels)` | Attend sur plusieurs canaux |
| `apply(fn, args_array)` | Appelle une fonction avec un tableau d'arguments |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### Helpers Pointeur / FFI

Ces fonctions sont globales car ce sont des primitives de bas niveau utilisees avec `alloc`/`free`.

| Fonction | Description |
|----------|-------------|
| `ptr_offset(ptr, bytes)` | Decale un pointeur de bytes octets |
| `ptr_null()` | Obtient un pointeur null |
| `ptr_to_buffer(ptr, size)` | Enveloppe un pointeur dans un buffer avec verification des limites |
| `buffer_ptr(buffer)` | Obtient le pointeur brut d'un buffer |

**Lecture/ecriture/deref de pointeur** pour tous les types numeriques et `ptr` :

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

Toutes les fonctions `ptr_read_*`, `ptr_write_*` et `ptr_deref_*` acceptent directement les types `ptr` et `buffer` :

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Fonctionne aussi directement avec les buffers (pas besoin de buffer_ptr())
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Deplaces vers les modules Stdlib

Ces builtins ont ete deplaces dans v2.0.0 et necessitent maintenant des imports.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Fonctions :** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Constantes :** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Fonctions :** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Fonctions :** `signal`, `raise`

**Constantes :** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Fonctions :** `socket_create`, `dns_resolve`, `poll`

**Constantes :** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Fonctions :** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Fonctions :** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Fonctions :** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Fonctions (i32) :** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Fonctions (i64) :** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Fonctions :** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Fonctions :** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Fonctions :** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Fonctions :** `string_concat_many`

---

## Guide de migration (v1.x → v2.0.0)

### Avant (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### Apres (v2.0.0)
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

Les appels de fonctions eux-memes sont identiques -- seuls les imports changent.
