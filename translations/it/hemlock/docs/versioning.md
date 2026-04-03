# Versionamento di Hemlock

Questo documento descrive la strategia di versionamento di Hemlock.

## Formato della versione

Hemlock utilizza il **Versionamento Semantico** (SemVer):

```
MAJOR.MINOR.PATCH
```

| Componente | Quando incrementare |
|------------|---------------------|
| **MAJOR** | Modifiche incompatibili alla semantica del linguaggio, API della stdlib o formati binari |
| **MINOR** | Nuove funzionalita, aggiunte retrocompatibili |
| **PATCH** | Correzioni di bug, miglioramenti delle prestazioni, documentazione |

## Versionamento unificato

Tutti i componenti di Hemlock condividono un **unico numero di versione**:

- **Interprete** (`hemlock`)
- **Compilatore** (`hemlockc`)
- **Server LSP** (`hemlock --lsp`)
- **Libreria standard** (`@stdlib/*`)

La versione e definita in `include/version.h`:

```c
#define HEMLOCK_VERSION_MAJOR 1
#define HEMLOCK_VERSION_MINOR 8
#define HEMLOCK_VERSION_PATCH 7

#define HEMLOCK_VERSION "1.8.7"
```

### Controllare le versioni

```bash
# Versione dell'interprete
hemlock --version

# Versione del compilatore
hemlockc --version
```

## Garanzie di compatibilita

### All'interno di una versione MAJOR

- Il codice sorgente che funziona in `1.x.0` funzionera in `1.x.y` (qualsiasi patch)
- Il codice sorgente che funziona in `1.0.x` funzionera in `1.y.z` (qualsiasi minor/patch)
- I bundle `.hmlb` compilati sono compatibili all'interno della stessa versione MAJOR
- Le API della libreria standard sono stabili (solo aggiunte, nessuna rimozione)

### Tra versioni MAJOR

- Le modifiche incompatibili sono documentate nelle note di rilascio
- Vengono fornite guide alla migrazione per le modifiche significative
- Le funzionalita deprecate vengono segnalate per almeno una versione minore prima della rimozione

## Versionamento dei formati binari

Hemlock utilizza numeri di versione separati per i formati binari:

| Formato | Versione | Posizione |
|---------|----------|-----------|
| `.hmlc` (bundle AST) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (bundle compresso) | Uguale a HMLC | Utilizza la compressione zlib |
| `.hmlp` (eseguibile pacchettizzato) | Magic: `HMLP` | Formato autonomo |

Le versioni dei formati binari vengono incrementate indipendentemente quando cambia la serializzazione.

## Versionamento della libreria standard

La libreria standard (`@stdlib/*`) e versionata **con il rilascio principale**:

```hemlock
// Utilizza sempre la stdlib inclusa con la tua installazione di Hemlock
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Compatibilita della stdlib

- Nuovi moduli possono essere aggiunti nelle versioni MINOR
- Nuove funzioni possono essere aggiunte ai moduli esistenti nelle versioni MINOR
- Le firme delle funzioni sono stabili all'interno di una versione MAJOR
- Le funzioni deprecate vengono contrassegnate e documentate prima della rimozione

## Cronologia delle versioni

| Versione | Data | Punti salienti |
|----------|------|----------------|
| **1.8.7** | 2026 | Fix multi-argument print/eprint in compiler codegen |
| **1.8.6** | 2026 | Fix segfault in hml_string_append_inplace for SSO strings |
| **1.8.5** | 2026 | 5 new array methods (every, some, indexOf, sort, fill), major performance optimizations, memory leak fixes |
| **1.8.4** | 2026 | Graceful handling for reserved keywords (def, func, var, class), fix flaky CI tests |
| **1.8.3** | 2026 | Code polish: consolidate magic numbers, standardize error messages |
| **1.8.2** | 2026 | Memory leak prevention: exception-safe eval, task/channel cleanup, optimizer fixes |
| **1.8.1** | 2026 | Fix use-after-free bug in function return value handling |
| **1.8.0** | 2026 | Pattern matching, arena allocator, memory leak fixes |
| **1.7.5** | 2026 | Fix formatter else-if indentation bug |
| **1.7.4** | 2026 | Formatter improvements: function parameter, binary expr, import, and method chain line breaking |
| **1.7.3** | 2026 | Fix formatter comment and blank line preservation |
| **1.7.2** | 2026 | Maintenance release |
| **1.7.1** | 2026 | Single-line if/while/for statements (braceless syntax) |
| **1.7.0** | 2026 | Type aliases, function types, const params, method signatures, loop labels, named args, null coalescing |
| **1.6.7** | 2026 | Octal literals, block comments, hex/unicode escapes, numeric separators |
| **1.6.6** | 2026 | Float literals without leading zero, fix strength reduction bug |
| **1.6.5** | 2026 | Fix for-in loop syntax without 'let' keyword |
| **1.6.4** | 2026 | Hotfix release |
| **1.6.3** | 2026 | Fix runtime method dispatch for file, channel, socket types |
| **1.6.2** | 2026 | Patch release |
| **1.6.1** | 2026 | Patch release |
| **1.6.0** | 2025 | Compile-time type checking in hemlockc, LSP integration, compound bitwise operators (`&=`, `\|=`, `^=`, `<<=`, `>>=`, `%=`) |
| **1.5.0** | 2024 | Full type system, async/await, atomics, 39 stdlib modules, FFI struct support, 99 parity tests |
| **1.3.0** | 2025 | Proper lexical block scoping (JS-like let/const semantics), per-iteration loop closures |
| **1.2.3** | 2025 | Import star syntax (`import * from`) |
| **1.2.2** | 2025 | Add `export extern` support, cross-platform test fixes |
| **1.2.1** | 2025 | Fix macOS test failures (RSA key generation, directory symlinks) |
| **1.2.0** | 2025 | AST optimizer, apply() builtin, unbuffered channels, 7 new stdlib modules, 97 parity tests |
| **1.1.3** | 2025 | Documentation updates, consistency fixes |
| **1.1.1** | 2025 | Bug fixes and improvements |
| **1.1.0** | 2024 | Unified versioning across all components |
| **1.0.x** | 2024 | Initial release series |

## Processo di rilascio

1. Aggiornamento della versione in `include/version.h`
2. Aggiornare il registro delle modifiche
3. Eseguire la suite di test completa (`make test-all`)
4. Taggare il rilascio in git
5. Compilare gli artefatti di rilascio

## Verifica della compatibilita

Per verificare che il tuo codice funzioni con una versione specifica di Hemlock:

```bash
# Eseguire i test con la versione installata
make test

# Verificare la parita tra interprete e compilatore
make parity
```

## Futuro: Manifesti di progetto

Una versione futura potrebbe introdurre manifesti di progetto opzionali per i vincoli di versione:

```hemlock
// Ipotetico project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

Questo non e ancora implementato ma fa parte della roadmap.
