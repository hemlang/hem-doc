# Referencia de Funcoes Integradas

Referencia completa de todas as funcoes e constantes integradas do Hemlock v2.0.0.

> **Mudanca Incompativel v2.0.0:** 63 builtins foram movidos do namespace global para
> modulos `@stdlib`. Funcoes como `sin()`, `open()`, `exec()`, `signal()` e
> constantes como `SIGINT`, `AF_INET` agora requerem imports. Veja [Movidos para Stdlib](#movidos-para-modulos-stdlib)
> para a lista completa.

---

## Builtins Globais (Sem Import Necessario)

Estes estao disponiveis em todos os lugares sem nenhuma instrucao `import`.

### I/O

| Funcao | Descricao |
|--------|-----------|
| `print(value, ...)` | Imprime valores em stdout com quebra de linha |
| `write(value)` | Imprime valor em stdout sem quebra de linha (flush imediato) |
| `eprint(value, ...)` | Imprime valores em stderr com quebra de linha |
| `read_line()` | Le uma linha de stdin; retorna `string` ou `null` em EOF |

```hemlock
print("Hello", "world");    // Hello world\n
write("sem quebra de linha"); // sem quebra de linha (sem \n)
eprint("error!");           // -> stderr
let name = read_line();     // bloqueia ate entrada
```

### Gerenciamento de Memoria

| Funcao | Descricao |
|--------|-----------|
| `alloc(size)` | Aloca `size` bytes de memoria bruta, retorna `ptr` |
| `talloc(type, count)` | Alocacao com tipo: `talloc(i32, 10)` aloca 10 i32s |
| `realloc(ptr, new_size)` | Redimensiona memoria alocada anteriormente |
| `free(ptr)` | Libera memoria alocada |
| `memset(ptr, value, size)` | Define `size` bytes com `value` |
| `memcpy(dest, src, size)` | Copia `size` bytes de `src` para `dest` |
| `buffer(size)` | Cria buffer com verificacao de limites de `size` bytes |

```hemlock
let p = alloc(64);       // ponteiro bruto, sem verificacao de limites
let b = buffer(64);      // buffer seguro, verificacao de limites
memset(p, 0, 64);
memcpy(b, p, 64);
free(p);                 // limpeza manual
```

### Sistema de Tipos

| Funcao | Descricao |
|--------|-----------|
| `typeof(value)` | Retorna nome do tipo como string (`"i32"`, `"string"`, etc.) |
| `typeid(value)` | Retorna tipo como constante inteira (mais rapido que `typeof()` para comparacoes) |
| `sizeof(type)` | Retorna tamanho em bytes de um tipo (`sizeof(i32)` → 4) |

**Construtores de tipo** (usados para conversao e alocacao tipada):

`i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `ptr`

**Aliases de tipo:** `integer` (i32), `number` (f64), `byte` (u8)

**Constantes TYPEID** (para uso com `typeid()`):

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
let n = i32("42");  // parseia string para i32

// typeid() retorna inteiro - mais rapido que comparacoes de string com typeof()
typeid(42);                          // 2 (TYPEID_I32)
typeid(42) == TYPEID_I32;            // true
let tid = typeid(val);
if (tid == TYPEID_I32 || tid == TYPEID_I64) {
    print("tipo inteiro");
}
```

### Fluxo de Controle

| Funcao | Descricao |
|--------|-----------|
| `assert(condition, message?)` | Panic se condicao for falsa |
| `panic(message)` | Saida imediata irrecuperavel (nao capturavel por try/catch) |

```hemlock
assert(x > 0, "x deve ser positivo");
panic("erro irrecuperavel");
```

### Concorrencia

| Funcao | Descricao |
|--------|-----------|
| `spawn(fn, args...)` | Cria uma tarefa assincrona, retorna handle de tarefa |
| `spawn_with(options, fn, args...)` | Cria tarefa com configuracao por thread (`stack_size` em bytes, `name` string max 16 chars) |
| `join(task)` | Aguarda conclusao da tarefa, retorna resultado |
| `detach(task)` | Permite tarefa executar independentemente (fire and forget) |
| `channel(capacity?)` | Cria canal de comunicacao (0 = sem buffer) |
| `select(channels)` | Aguarda em multiplos canais |
| `apply(fn, args_array)` | Chama funcao com array de argumentos |

```hemlock
let task = spawn(fn(n) { return n * n; }, 42);
let result = join(task);  // 1764

let ch = channel(10);
ch.send("hello");
let msg = ch.recv();
```

### Helpers de Ponteiro / FFI

Estes sao globais porque sao primitivos de baixo nivel usados com `alloc`/`free`.

| Funcao | Descricao |
|--------|-----------|
| `ptr_offset(ptr, bytes)` | Desloca ponteiro por bytes |
| `ptr_null()` | Obtem ponteiro nulo |
| `ptr_to_buffer(ptr, size)` | Encapsula ponteiro em buffer com verificacao de limites |
| `buffer_ptr(buffer)` | Obtem ponteiro bruto de um buffer |

**Leitura/escrita/deref de ponteiro** para todos os tipos numericos e `ptr`:

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

Todas as funcoes `ptr_read_*`, `ptr_write_*` e `ptr_deref_*` aceitam ambos os tipos `ptr` e `buffer` diretamente:

```hemlock
let p = alloc(8);
ptr_write_i32(p, 42);
let val = ptr_read_i32(p);  // 42
let p2 = ptr_offset(p, 4);
ptr_write_i32(p2, 99);
free(p);

// Tambem funciona diretamente com buffers (sem buffer_ptr() necessario)
let buf = buffer(8);
ptr_write_i32(buf, 42);
let bval = ptr_read_i32(buf);  // 42
```

---

## Movidos para Modulos Stdlib

Estes builtins foram movidos na v2.0.0 e agora requerem imports.

### `@stdlib/math`

```hemlock
import { sin, cos, sqrt, floor, PI } from "@stdlib/math";
```

**Funcoes:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sqrt`, `pow`, `exp`, `log`, `log10`, `log2`, `floor`, `ceil`, `round`, `trunc`, `floori`, `ceili`, `roundi`, `trunci`, `div`, `divi`, `abs`, `min`, `max`, `clamp`, `rand`, `rand_range`, `seed`

**Constantes:** `PI`, `E`, `TAU`, `INF`, `NAN`

### `@stdlib/env`

```hemlock
import { getenv, setenv } from "@stdlib/env";
```

**Funcoes:** `getenv`, `setenv`, `unsetenv`, `get_pid`, `exit`

### `@stdlib/signal`

```hemlock
import { signal, raise, SIGUSR1 } from "@stdlib/signal";
```

**Funcoes:** `signal`, `raise`

**Constantes:** `SIGINT`, `SIGTERM`, `SIGHUP`, `SIGQUIT`, `SIGABRT`, `SIGUSR1`, `SIGUSR2`, `SIGALRM`, `SIGCHLD`, `SIGPIPE`, `SIGCONT`, `SIGSTOP`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`

### `@stdlib/net`

```hemlock
import { AF_INET, SOCK_STREAM, socket_create } from "@stdlib/net";
```

**Funcoes:** `socket_create`, `dns_resolve`, `poll`

**Constantes:** `AF_INET`, `AF_INET6`, `SOCK_STREAM`, `SOCK_DGRAM`, `IPPROTO_TCP`, `IPPROTO_UDP`, `SOL_SOCKET`, `SO_REUSEADDR`, `SO_KEEPALIVE`, `SO_RCVTIMEO`, `SO_SNDTIMEO`, `POLLIN`, `POLLOUT`, `POLLERR`, `POLLHUP`, `POLLNVAL`, `POLLPRI`

### `@stdlib/process`

```hemlock
import { exec, fork, kill } from "@stdlib/process";
```

**Funcoes:** `exec`, `exec_argv`, `fork`, `wait`, `waitpid`, `kill`, `abort`, `exit`, `get_pid`, `getppid`, `getuid`, `geteuid`, `getgid`, `getegid`

### `@stdlib/fs`

```hemlock
import { open, read_file } from "@stdlib/fs";
```

**Funcoes:** `open`, `read_file`, `write_file`, `append_file`, `remove_file`, `rename`, `copy_file`, `is_file`, `is_dir`, `file_stat`, `make_dir`, `remove_dir`, `list_dir`, `cwd`, `chdir`, `absolute_path`, `exists`

### `@stdlib/time`

```hemlock
import { now, sleep } from "@stdlib/time";
```

**Funcoes:** `now`, `time_ms`, `sleep`, `clock`

### `@stdlib/atomic`

```hemlock
import { atomic_load_i32, atomic_cas_i32, atomic_fence } from "@stdlib/atomic";
```

**Funcoes (i32):** `atomic_load_i32`, `atomic_store_i32`, `atomic_add_i32`, `atomic_sub_i32`, `atomic_and_i32`, `atomic_or_i32`, `atomic_xor_i32`, `atomic_cas_i32`, `atomic_exchange_i32`

**Funcoes (i64):** `atomic_load_i64`, `atomic_store_i64`, `atomic_add_i64`, `atomic_sub_i64`, `atomic_and_i64`, `atomic_or_i64`, `atomic_xor_i64`, `atomic_cas_i64`, `atomic_exchange_i64`

**Funcoes:** `atomic_fence`

### `@stdlib/debug`

```hemlock
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

**Funcoes:** `task_debug_info`, `set_stack_limit`, `get_stack_limit`

### `@stdlib/ffi`

```hemlock
import { callback, callback_free } from "@stdlib/ffi";
```

**Funcoes:** `callback`, `callback_free`

### `@stdlib/strings`

```hemlock
import { string_concat_many } from "@stdlib/strings";
```

**Funcoes:** `string_concat_many`

---

## Guia de Migracao (v1.x → v2.0.0)

### Antes (v1.x)
```hemlock
let x = sin(PI / 2);
let pid = get_pid();
signal(SIGUSR1, handler);
let f = open("file.txt", "r");
let r = exec("echo hello");
```

### Depois (v2.0.0)
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

As chamadas de funcao em si sao identicas -- apenas os imports mudam.
