# Hemlock-Versionierung

Dieses Dokument beschreibt die Versionierungsstrategie von Hemlock.

## Versionsformat

Hemlock verwendet **Semantische Versionierung** (SemVer):

```
MAJOR.MINOR.PATCH
```

| Komponente | Wann zu erhöhen |
|------------|------------------|
| **MAJOR** | Inkompatible Änderungen an Sprachsemantik, Stdlib-API oder Binärformaten |
| **MINOR** | Neue Funktionen, abwärtskompatible Erweiterungen |
| **PATCH** | Fehlerbehebungen, Leistungsverbesserungen, Dokumentation |

## Einheitliche Versionierung

Alle Hemlock-Komponenten teilen sich eine **einzige Versionsnummer**:

- **Interpreter** (`hemlock`)
- **Compiler** (`hemlockc`)
- **LSP-Server** (`hemlock --lsp`)
- **Standardbibliothek** (`@stdlib/*`)

Die Version wird in `include/version.h` definiert:

```c
#define HEMLOCK_VERSION_MAJOR 2
#define HEMLOCK_VERSION_MINOR 0
#define HEMLOCK_VERSION_PATCH 0

#define HEMLOCK_VERSION "2.0.0"
```

### Versionen prüfen

```bash
# Interpreter-Version
hemlock --version

# Compiler-Version
hemlockc --version
```

## Kompatibilitätsgarantien

### Innerhalb einer MAJOR-Version

- Quellcode, der in `1.x.0` funktioniert, wird in `1.x.y` funktionieren (beliebiger Patch)
- Quellcode, der in `1.0.x` funktioniert, wird in `1.y.z` funktionieren (beliebige Minor-/Patch-Version)
- Kompilierte `.hmlb`-Bundles sind innerhalb derselben MAJOR-Version kompatibel
- Standardbibliotheks-APIs sind stabil (nur Erweiterungen, keine Entfernungen)

### Über MAJOR-Versionen hinweg

- Inkompatible Änderungen werden in den Release-Notes dokumentiert
- Migrationsanleitungen werden für wesentliche Änderungen bereitgestellt
- Veraltete Funktionen werden mindestens ein Minor-Release vor der Entfernung gewarnt

## Binärformat-Versionierung

Hemlock verwendet separate Versionsnummern für Binärformate:

| Format | Version | Speicherort |
|--------|---------|-------------|
| `.hmlc` (AST-Bundle) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (komprimiertes Bundle) | Wie HMLC | Verwendet zlib-Komprimierung |
| `.hmlp` (gepackte ausführbare Datei) | Magic: `HMLP` | Eigenständiges Format |

Binärformat-Versionen werden unabhängig erhöht, wenn sich die Serialisierung ändert.

## Standardbibliothek-Versionierung

Die Standardbibliothek (`@stdlib/*`) wird **mit dem Hauptrelease** versioniert:

```hemlock
// Verwendet immer die mit Ihrer Hemlock-Installation gebündelte Stdlib
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Stdlib-Kompatibilität

- Neue Module können in MINOR-Releases hinzugefügt werden
- Neue Funktionen können in MINOR-Releases zu bestehenden Modulen hinzugefügt werden
- Funktionssignaturen sind innerhalb einer MAJOR-Version stabil
- Veraltete Funktionen werden vor der Entfernung markiert und dokumentiert

## Versionsgeschichte

| Version | Datum | Highlights |
|---------|-------|------------|
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

## Release-Prozess

1. Versionserhöhung in `include/version.h`
2. Änderungsprotokoll aktualisieren
3. Vollständige Testsuite ausführen (`make test-all`)
4. Release in Git taggen
5. Release-Artefakte erstellen

## Kompatibilität prüfen

Um zu überprüfen, ob Ihr Code mit einer bestimmten Hemlock-Version funktioniert:

```bash
# Tests gegen die installierte Version ausführen
make test

# Parität zwischen Interpreter und Compiler prüfen
make parity
```

## Zukunft: Projektmanifeste

Ein zukünftiges Release könnte optionale Projektmanifeste für Versionseinschränkungen einführen:

```hemlock
// Hypothetisches project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

Dies ist noch nicht implementiert, aber Teil der Roadmap.
