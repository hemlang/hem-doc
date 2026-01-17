# Hemlock Modulsystem

Dieses Dokument beschreibt das ES6-artige Import/Export-Modulsystem von Hemlock.

## Uebersicht

Hemlock unterstuetzt ein dateibasiertes Modulsystem mit ES6-artiger Import/Export-Syntax. Module sind:
- **Singletons**: Jedes Modul wird einmal geladen und gecacht
- **Dateibasiert**: Module entsprechen .hml-Dateien auf der Festplatte
- **Explizit importiert**: Abhaengigkeiten werden mit Import-Anweisungen deklariert
- **Topologisch ausgefuehrt**: Abhaengigkeiten werden vor abhaengigen Modulen ausgefuehrt

Fuer Paketverwaltung und Drittanbieter-Abhaengigkeiten siehe [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Syntax

### Export-Anweisungen

**Inline benannte Exports:**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**Export-Liste:**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Export Extern (FFI-Funktionen):**
```hemlock
import "libc.so.6";

// FFI-Funktionen zur Verwendung in anderen Modulen exportieren
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

Siehe [FFI-Dokumentation](../advanced/ffi.md#exporting-ffi-functions) fuer weitere Details zum Exportieren von FFI-Funktionen.

**Export Define (Struct-Typen):**
```hemlock
// Struct-Typdefinitionen exportieren
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

**Wichtig:** Exportierte Struct-Typen werden global registriert, wenn das Modul geladen wird. Sie werden automatisch verfuegbar, wenn Sie etwas aus dem Modul importieren - Sie muessen (und koennen) sie NICHT explizit nach Namen importieren:

```hemlock
// GUT - Struct-Typen sind nach jedem Import automatisch verfuegbar
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Funktioniert!

// SCHLECHT - Struct-Typen koennen nicht explizit importiert werden
import { Vector2 } from "./my_module.hml";  // Fehler: Undefinierte Variable 'Vector2'
```

Siehe [FFI-Dokumentation](../advanced/ffi.md#exporting-struct-types) fuer weitere Details zum Exportieren von Struct-Typen.

**Re-Exports:**
```hemlock
// Aus einem anderen Modul re-exportieren
export { add, subtract } from "./math.hml";
```

### Import-Anweisungen

**Benannte Imports:**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Namespace-Import:**
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

## Modulaufloesung

### Pfadtypen

**Relative Pfade:**
```hemlock
import { foo } from "./module.hml";       // Gleiches Verzeichnis
import { bar } from "../parent.hml";      // Uebergeordnetes Verzeichnis
import { baz } from "./sub/nested.hml";   // Unterverzeichnis
```

**Absolute Pfade:**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Erweiterungsbehandlung:**
- Die `.hml`-Erweiterung kann weggelassen werden - sie wird automatisch hinzugefuegt
- `./math` wird zu `./math.hml` aufgeloest

## Funktionen

### Erkennung zirkulaerer Abhaengigkeiten

Das Modulsystem erkennt zirkulaere Abhaengigkeiten und meldet einen Fehler:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Modul-Caching

Module werden einmal geladen und gecacht. Mehrere Imports desselben Moduls geben dieselbe Instanz zurueck:

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
import { count } from "./counter.hml";  // Dieselbe Instanz!
print(count);  // Immer noch 1 (geteilter Zustand)
```

### Import-Unveraenderlichkeit

Importierte Bindungen koennen nicht neu zugewiesen werden:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // FEHLER: kann importierte Bindung nicht neu zuweisen
```

## Implementierungsdetails

### Architektur

**Dateien:**
- `include/module.h` - Modulsystem-API
- `src/module.c` - Modulladen, Caching und Ausfuehrung
- Parser-Unterstuetzung in `src/parser.c`
- Laufzeit-Unterstuetzung in `src/interpreter/runtime.c`

**Schluesselkomponenten:**
1. **ModuleCache**: Verwaltet geladene Module, indiziert nach absolutem Pfad
2. **Module**: Repraesentiert ein geladenes Modul mit seinem AST und Exports
3. **Pfadaufloesung**: Loest relative/absolute Pfade zu kanonischen Pfaden auf
4. **Topologische Ausfuehrung**: Fuehrt Module in Abhaengigkeitsreihenfolge aus

### Modulladeprozess

1. **Parse-Phase**: Tokenisieren und Parsen der Moduldatei
2. **Abhaengigkeitsaufloesung**: Rekursives Laden importierter Module
3. **Zykluserkennung**: Pruefen, ob das Modul bereits geladen wird
4. **Caching**: Modul im Cache nach absolutem Pfad speichern
5. **Ausfuehrungsphase**: Ausfuehrung in topologischer Reihenfolge (Abhaengigkeiten zuerst)

### API

```c
// High-Level-API
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// Low-Level-API
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Testen

Testmodule befinden sich in `tests/modules/` und `tests/parity/modules/`:

- `math.hml` - Basismodul mit Exports
- `test_import_named.hml` - Test fuer benannte Imports
- `test_import_namespace.hml` - Test fuer Namespace-Imports
- `test_import_alias.hml` - Test fuer Import-Aliasing
- `export_extern.hml` - Test fuer Export extern FFI-Funktion (Linux)

## Paket-Imports (hpm)

Mit installiertem [hpm](https://github.com/hemlang/hpm) koennen Sie Drittanbieter-Pakete von GitHub importieren:

```hemlock
// Import aus Paket-Root (verwendet "main" aus package.json)
import { app, router } from "hemlang/sprout";

// Import aus Unterpfad
import { middleware } from "hemlang/sprout/middleware";

// Standardbibliothek (in Hemlock eingebaut)
import { HashMap } from "@stdlib/collections";
```

Pakete werden in `hem_modules/` installiert und mit GitHub `owner/repo`-Syntax aufgeloest.

```bash
# Ein Paket installieren
hpm install hemlang/sprout

# Mit Versionsbeschraenkung installieren
hpm install hemlang/sprout@^1.0.0
```

Siehe die [hpm-Dokumentation](https://github.com/hemlang/hpm) fuer vollstaendige Details.

## Aktuelle Einschraenkungen

1. **Keine dynamischen Imports**: `import()` als Laufzeitfunktion wird nicht unterstuetzt
2. **Keine bedingten Exports**: Exports muessen auf oberster Ebene sein
3. **Statische Bibliothekspfade**: FFI-Bibliotheksimports verwenden statische Pfade (plattformspezifisch)

## Zukuenftige Arbeit

- Dynamische Imports mit `import()`-Funktion
- Bedingte Exports
- Modul-Metadaten (`import.meta`)
- Tree Shaking und Eliminierung von totem Code

## Beispiele

Siehe `tests/modules/` fuer funktionierende Beispiele des Modulsystems.

Beispiel-Modulstruktur:
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (Barrel-Modul)
└── utils/
    └── helpers.hml
```

Beispielverwendung:
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (Barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
