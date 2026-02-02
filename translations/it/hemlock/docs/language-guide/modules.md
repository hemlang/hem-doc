# Sistema di Moduli di Hemlock

Questo documento descrive il sistema di moduli import/export in stile ES6 implementato per Hemlock.

## Panoramica

Hemlock supporta un sistema di moduli basato su file con sintassi import/export in stile ES6. I moduli sono:
- **Singleton**: Ogni modulo viene caricato una volta e memorizzato in cache
- **Basati su file**: I moduli corrispondono a file .hml su disco
- **Importati esplicitamente**: Le dipendenze sono dichiarate con istruzioni import
- **Eseguiti topologicamente**: Le dipendenze vengono eseguite prima dei dipendenti

Per la gestione dei pacchetti e le dipendenze di terze parti, vedi [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Sintassi

### Istruzioni Export

**Export con nome inline:**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**Lista di export:**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Export Extern (Funzioni FFI):**
```hemlock
import "libc.so.6";

// Esporta funzioni FFI per l'uso in altri moduli
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

Vedi [Documentazione FFI](../advanced/ffi.md#exporting-ffi-functions) per maggiori dettagli sull'esportazione di funzioni FFI.

**Export Define (Tipi Struct):**
```hemlock
// Esporta definizioni di tipi struct
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**Importante:** I tipi struct esportati vengono registrati globalmente quando il modulo viene caricato. Diventano disponibili automaticamente quando importi qualcosa dal modulo - NON devi (e non puoi) importarli esplicitamente per nome:

```hemlock
// BENE - i tipi struct sono auto-disponibili dopo qualsiasi import
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Funziona!

// MALE - non puoi importare esplicitamente i tipi struct
import { Vector2 } from "./my_module.hml";  // Errore: Variabile 'Vector2' non definita
```

Vedi [Documentazione FFI](../advanced/ffi.md#exporting-struct-types) per maggiori dettagli sull'esportazione di tipi struct.

**Re-export:**
```hemlock
// Re-esporta da un altro modulo
export { add, subtract } from "./math.hml";
```

### Istruzioni Import

**Import con nome:**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Import namespace:**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**Aliasing:**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## Risoluzione dei Moduli

### Tipi di Percorso

**Percorsi relativi:**
```hemlock
import { foo } from "./module.hml";       // Stessa directory
import { bar } from "../parent.hml";      // Directory padre
import { baz } from "./sub/nested.hml";   // Sottodirectory
```

**Percorsi assoluti:**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Gestione dell'estensione:**
- L'estensione `.hml` puo essere omessa - verra aggiunta automaticamente
- `./math` viene risolto in `./math.hml`

## Funzionalita

### Rilevamento delle Dipendenze Circolari

Il sistema di moduli rileva le dipendenze circolari e riporta un errore:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Cache dei Moduli

I moduli vengono caricati una volta e memorizzati in cache. Import multipli dello stesso modulo restituiscono la stessa istanza:

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // Stessa istanza!
print(count);  // Ancora 1 (stato condiviso)
```

### Immutabilita degli Import

I binding importati non possono essere riassegnati:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // ERRORE: impossibile riassegnare binding importato
```

## Dettagli Implementativi

### Architettura

**File:**
- `include/module.h` - API del sistema di moduli
- `src/module.c` - Caricamento, caching ed esecuzione dei moduli
- Supporto parser in `src/parser.c`
- Supporto runtime in `src/interpreter/runtime.c`

**Componenti chiave:**
1. **ModuleCache**: Mantiene i moduli caricati indicizzati per percorso assoluto
2. **Module**: Rappresenta un modulo caricato con il suo AST e gli export
3. **Risoluzione percorsi**: Risolve percorsi relativi/assoluti in percorsi canonici
4. **Esecuzione topologica**: Esegue i moduli in ordine di dipendenza

### Processo di Caricamento dei Moduli

1. **Fase di parsing**: Tokenizza e analizza il file del modulo
2. **Risoluzione delle dipendenze**: Carica ricorsivamente i moduli importati
3. **Rilevamento cicli**: Controlla se il modulo e gia in fase di caricamento
4. **Caching**: Memorizza il modulo in cache per percorso assoluto
5. **Fase di esecuzione**: Esegue in ordine topologico (dipendenze prima)

### API

```c
// API ad alto livello
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// API a basso livello
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Testing

I moduli di test si trovano in `tests/modules/` e `tests/parity/modules/`:

- `math.hml` - Modulo base con export
- `test_import_named.hml` - Test import con nome
- `test_import_namespace.hml` - Test import namespace
- `test_import_alias.hml` - Test aliasing degli import
- `export_extern.hml` - Test export extern per funzioni FFI (Linux)

## Import di Pacchetti (hpm)

Con [hpm](https://github.com/hemlang/hpm) installato, puoi importare pacchetti di terze parti da GitHub:

```hemlock
// Import dalla root del pacchetto (usa "main" da package.json)
import { app, router } from "hemlang/sprout";

// Import da sottopercorso
import { middleware } from "hemlang/sprout/middleware";

// Libreria standard (integrata in Hemlock)
import { HashMap } from "@stdlib/collections";
```

I pacchetti vengono installati in `hem_modules/` e risolti usando la sintassi GitHub `owner/repo`.

```bash
# Installa un pacchetto
hpm install hemlang/sprout

# Installa con vincolo di versione
hpm install hemlang/sprout@^1.0.0
```

Vedi la [documentazione hpm](https://github.com/hemlang/hpm) per tutti i dettagli.

## Limitazioni Attuali

1. **Nessun import dinamico**: `import()` come funzione runtime non e supportato
2. **Nessun export condizionale**: Gli export devono essere al livello superiore
3. **Percorsi libreria statici**: Gli import di librerie FFI usano percorsi statici (specifici per piattaforma)

## Lavoro Futuro

- Import dinamici con la funzione `import()`
- Export condizionali
- Metadati del modulo (`import.meta`)
- Tree shaking ed eliminazione del codice morto

## Esempi

Vedi `tests/modules/` per esempi funzionanti del sistema di moduli.

Struttura di esempio del modulo:
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (barrel module)
└── utils/
    └── helpers.hml
```

Esempio di utilizzo:
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
