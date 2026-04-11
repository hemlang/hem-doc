# Guide de migration : v1.x vers v2.0.0

## Changement cassant : Builtins deplaces vers la stdlib

Hemlock 2.0.0 a deplace 63 builtins globaux dans des modules `@stdlib` pour reduire la pollution de l'espace de noms. Le code qui utilise ces fonctions sans imports obtiendra des erreurs "undefined variable".

## Correction rapide

Ajoutez l'instruction `import` appropriee pour chaque fonction. Le tableau ci-dessous montre ou chaque builtin a ete deplace.

### Fonctions mathematiques

```hemlock
// Avant (v1.x)
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);

// Apres (v2.0.0)
import { sin, floor, divi } from "@stdlib/math";
let x = sin(3.14);
let y = floor(2.7);
let z = divi(10, 3);
```

**Fonctions deplacees :** `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `cbrt`, `exp`, `log`, `log2`, `log10`, `floor`, `ceil`, `round`, `trunc`, `abs`, `pow`, `fmod`, `min`, `max`, `rand`, `div`, `divi`, `floori`, `ceili`, `roundi`, `trunci`

### Gestion des signaux

```hemlock
// Avant
signal(SIGINT, handler);

// Apres
import { signal, raise, SIGINT, SIGTERM, SIGUSR1 } from "@stdlib/signal";
signal(SIGINT, handler);
```

### Systeme de fichiers

```hemlock
// Avant
let f = open("file.txt", "r");

// Apres
import { open } from "@stdlib/fs";
let f = open("file.txt", "r");
```

### Processus / Environnement

```hemlock
// Avant
let home = getenv("HOME");
exec("ls");

// Apres
import { getenv, setenv } from "@stdlib/env";
import { exec } from "@stdlib/process";
```

### Reseau

```hemlock
// Avant
let sock = socket_create(AF_INET, SOCK_STREAM, 0);

// Apres
import { socket_create, AF_INET, SOCK_STREAM } from "@stdlib/net";
```

### Operations atomiques

```hemlock
// Avant
atomic_store(ptr, 42);

// Apres
import { atomic_store, atomic_load, atomic_add } from "@stdlib/atomic";
```

### Callbacks FFI

```hemlock
// Avant
let cb = callback(my_func);

// Apres
import { callback, callback_free } from "@stdlib/ffi";
```

### Debug / Pile

```hemlock
// Avant
let info = task_debug_info(task);

// Apres
import { task_debug_info, set_stack_limit } from "@stdlib/debug";
```

## Correspondance complete des modules

| Fonction(s) | Nouveau module |
|-------------|---------------|
| Fonctions math (sin, cos, sqrt, etc.) | `@stdlib/math` |
| `signal`, `raise`, constantes SIG* | `@stdlib/signal` |
| `open` | `@stdlib/fs` |
| `exec`, `exec_argv` | `@stdlib/process` |
| `getenv`, `setenv` | `@stdlib/env` |
| Constantes AF_*, SOCK_*, POLL*, `socket_create`, `dns_resolve`, `poll` | `@stdlib/net` |
| Operations `atomic_*` | `@stdlib/atomic` |
| `callback`, `callback_free`, `ffi_sizeof` | `@stdlib/ffi` |
| `task_debug_info`, `set_stack_limit`, `get_stack_limit` | `@stdlib/debug` |
| `string_concat_many` | `@stdlib/strings` |
| `get_default_stack_size`, `set_default_stack_size` | `@stdlib/async` |

## Aucun autre changement cassant

Toutes les autres fonctionnalites du langage, syntaxe et APIs restent retrocompatibles. Le code existant n'a besoin que d'ajouts d'imports.
