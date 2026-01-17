# Hemlock Modulsystem

Dieses Dokument beschreibt das ES6-artige Import/Export-Modulsystem von Hemlock.

## Übersicht

Hemlock unterstützt ein dateibasiertes Modulsystem mit ES6-artiger Import/Export-Syntax. Module sind:
- **Singletons**: Jedes Modul wird einmal geladen und gecacht
- **Dateibasiert**: Module entsprechen .hml-Dateien auf der Festplatte
- **Explizit importiert**: Abhängigkeiten werden mit Import-Anweisungen deklariert
- **Topologisch ausgeführt**: Abhängigkeiten werden vor abhängigen Modulen ausgeführt

Für Paketverwaltung und Drittanbieter-Abhängigkeiten siehe [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

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

Siehe [FFI-Dokumentation](../advanced/ffi.md#exporting-ffi-functions) für weitere Details zum Exportieren von FFI-Funktionen.

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

**Wichtig:** Exportierte Struct-Typen werden global registriert, wenn das Modul geladen wird. Sie werden automatisch verfügbar, wenn Sie etwas aus dem Modul importieren - Sie müssen (und können) sie NICHT explizit nach Namen importieren:

```hemlock
// GUT - Struct-Typen sind nach jedem Import automatisch verfügbar
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Funktioniert!

// SCHLECHT - Struct-Typen können nicht explizit importiert werden
import { Vector2 } from "./my_module.hml";  // Fehler: Undefinierte Variable 'Vector2'
```

Siehe [FFI-Dokumentation](../advanced/ffi.md#exporting-struct-types) für weitere Details zum Exportieren von Struct-Typen.

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
- Die `.hml`-Erweiterung kann weggelassen werden - sie wird automatisch hinzugefügt
- `./math` wird zu `./math.hml` aufgelöst

## Funktionen

### Erkennung zirkulaerer Abhängigkeiten

Das Modulsystem erkennt zirkulaere Abhängigkeiten und meldet einen Fehler:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Modul-Caching

Module werden einmal geladen und gecacht. Mehrere Imports desselben Moduls geben dieselbe Instanz zurück:

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

### Import-Unveränderlichkeit

Importierte Bindungen können nicht neu zugewiesen werden:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // FEHLER: kann importierte Bindung nicht neu zuweisen
```

## Implementierungsdetails

### Architektur

**Dateien:**
- `include/module.h` - Modulsystem-API
- `src/module.c` - Modulladen, Caching und Ausführung
- Parser-Unterstützung in `src/parser.c`
- Laufzeit-Unterstützung in `src/interpreter/runtime.c`

**Schluesselkomponenten:**
1. **ModuleCache**: Verwaltet geladene Module, indiziert nach absolutem Pfad
2. **Module**: Repraesentiert ein geladenes Modul mit seinem AST und Exports
3. **Pfadaufloesung**: Loest relative/absolute Pfade zu kanonischen Pfaden auf
4. **Topologische Ausführung**: Fuehrt Module in Abhaengigkeitsreihenfolge aus

### Modulladeprozess

1. **Parse-Phase**: Tokenisieren und Parsen der Moduldatei
2. **Abhaengigkeitsaufloesung**: Rekursives Laden importierter Module
3. **Zykluserkennung**: Prüfen, ob das Modul bereits geladen wird
4. **Caching**: Modul im Cache nach absolutem Pfad speichern
5. **Ausfuehrungsphase**: Ausführung in topologischer Reihenfolge (Abhängigkeiten zuerst)

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
- `test_import_named.hml` - Test für benannte Imports
- `test_import_namespace.hml` - Test für Namespace-Imports
- `test_import_alias.hml` - Test für Import-Aliasing
- `export_extern.hml` - Test für Export extern FFI-Funktion (Linux)

## Paket-Imports (hpm)

Mit installiertem [hpm](https://github.com/hemlang/hpm) können Sie Drittanbieter-Pakete von GitHub importieren:

```hemlock
// Import aus Paket-Root (verwendet "main" aus package.json)
import { app, router } from "hemlang/sprout";

// Import aus Unterpfad
import { middleware } from "hemlang/sprout/middleware";

// Standardbibliothek (in Hemlock eingebaut)
import { HashMap } from "@stdlib/collections";
```

Pakete werden in `hem_modules/` installiert und mit GitHub `owner/repo`-Syntax aufgelöst.

```bash
# Ein Paket installieren
hpm install hemlang/sprout

# Mit Versionsbeschraenkung installieren
hpm install hemlang/sprout@^1.0.0
```

Siehe die [hpm-Dokumentation](https://github.com/hemlang/hpm) für vollständige Details.

## Aktuelle Einschränkungen

1. **Keine dynamischen Imports**: `import()` als Laufzeitfunktion wird nicht unterstützt
2. **Keine bedingten Exports**: Exports müssen auf oberster Ebene sein
3. **Statische Bibliothekspfade**: FFI-Bibliotheksimports verwenden statische Pfade (plattformspezifisch)

## Zukuenftige Arbeit

- Dynamische Imports mit `import()`-Funktion
- Bedingte Exports
- Modul-Metadaten (`import.meta`)
- Tree Shaking und Eliminierung von totem Code

## Beispiele

Siehe `tests/modules/` für funktionierende Beispiele des Modulsystems.

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
