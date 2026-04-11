# Guia de Migracao: v1.x para v2.0.0

## Mudanca Incompativel: Builtins Movidos para Stdlib

Hemlock 2.0.0 moveu 63 builtins globais para modulos `@stdlib` para reduzir poluicao de namespace. Codigo que usa essas funcoes sem imports tera erros de "variavel indefinida".

## Correcao Rapida

Adicione a instrucao `import` apropriada para cada funcao. A tabela abaixo mostra para onde cada builtin foi movido.

### Funcoes Matematicas

```hemlock
// Antes (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// Depois (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Funcoes movidas:** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Tratamento de Sinais

```hemlock
// Antes
signal(SIGINT, handler);

// Depois
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### Sistema de Arquivos

```hemlock
// Antes
let f = open("file.txt", "r");

// Depois
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Processo / Ambiente

```hemlock
// Antes
let home = getenv("HOME");
exec("ls");

// Depois
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Rede

```hemlock
// Antes
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// Depois
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Operacoes Atomicas

```hemlock
// Antes
atomic_store(ptr, 42);

// Depois
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### Callbacks FFI

```hemlock
// Antes
let cb = callback(my_func);

// Depois
import { callback, callback_free } from "@stdlib/ffi";
```

### Debug / Pilha

```hemlock
// Antes
let info = task_debug_info(task);

// Depois
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Mapeamento Completo de Modulos

| Funcao(oes) | Novo Modulo |
|-------------|-------------|
| Funcoes matematicas (sin, cos, sqrt, etc.) | `@stdlib/math` |
| `signal`, `raise`, constantes SIG* | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| Constantes AF_*, SOCK_*, POLL*, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| Operacoes `atomic_*` | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Nenhuma Outra Mudanca Incompativel

Todos os outros recursos da linguagem, sintaxe e APIs permanecem retrocompativeis. O codigo existente precisa apenas de adicoes de import.
