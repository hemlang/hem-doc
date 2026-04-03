# Hemlock Dokumentation

Willkommen zur Dokumentation der Programmiersprache Hemlock!

> Eine kleine, unsichere Sprache, um unsichere Dinge sicher zu schreiben.

## Inhaltsverzeichnis

### Erste Schritte
- [Installation](getting-started/installation.md) - Hemlock kompilieren und installieren
- [Schnellstart](getting-started/quick-start.md) - Ihr erstes Hemlock-Programm
- [Tutorial](getting-started/tutorial.md) - Schritt-für-Schritt-Anleitung zu den Grundlagen von Hemlock
- [Lernpfade](getting-started/learning-paths.md) - Wählen Sie Ihren Lernweg basierend auf Ihren Zielen

### Neu in der Programmierung?
- [Glossar](glossary.md) - Verständliche Definitionen von Programmierbegriffen

### Sprachhandbuch
- [Syntax-Übersicht](language-guide/syntax.md) - Grundlegende Syntax und Struktur
- [Typsystem](language-guide/types.md) - Primitive Typen, Typinferenz und Konvertierungen
- [Speicherverwaltung](language-guide/memory.md) - Zeiger, Buffer und manueller Speicher
- [Strings](language-guide/strings.md) - UTF-8-Strings und Operationen
- [Runes](language-guide/runes.md) - Unicode-Codepunkte und Zeichenbehandlung
- [Kontrollfluss](language-guide/control-flow.md) - if/else, Schleifen, switch und Operatoren
- [Funktionen](language-guide/functions.md) - Funktionen, Closures und Rekursion
- [Objekte](language-guide/objects.md) - Objektliterale, Methoden und Duck-Typing
- [Arrays](language-guide/arrays.md) - Dynamische Arrays und Operationen
- [Fehlerbehandlung](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [Module](language-guide/modules.md) - Import/Export-System und Paketimporte

### Fortgeschrittene Themen
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Hemlock im Browser via Emscripten ausführen
- [Async & Nebenläufigkeit](advanced/async-concurrency.md) - Echtes Multi-Threading mit async/await
- [Bündelung & Paketierung](advanced/bundling-packaging.md) - Bundles und eigenständige Executables erstellen
- [Foreign Function Interface](advanced/ffi.md) - C-Funktionen aus Shared Libraries aufrufen
- [Datei-I/O](advanced/file-io.md) - Dateioperationen und Ressourcenverwaltung
- [Signalbehandlung](advanced/signals.md) - POSIX-Signalbehandlung
- [Kommandozeilenargumente](advanced/command-line-args.md) - Auf Programmargumente zugreifen
- [Befehlsausführung](advanced/command-execution.md) - Shell-Befehle ausführen
- [Profiling](advanced/profiling.md) - CPU-Zeit, Speicherverfolgung und Leck-Erkennung

### API-Referenz
- [Typsystem-Referenz](reference/type-system.md) - Vollständige Typreferenz
- [Operatoren-Referenz](reference/operators.md) - Alle Operatoren und Prioritäten
- [Eingebaute Funktionen](reference/builtins.md) - Globale Funktionen und Konstanten
- [String-API](reference/string-api.md) - String-Methoden und -Eigenschaften
- [Array-API](reference/array-api.md) - Array-Methoden und -Eigenschaften
- [Speicher-API](reference/memory-api.md) - Speicherallokation und -manipulation
- [Datei-API](reference/file-api.md) - Datei-I/O-Methoden
- [Nebenläufigkeits-API](reference/concurrency-api.md) - Tasks und Kanäle

### Design & Philosophie
- [Designphilosophie](design/philosophy.md) - Kernprinzipien und Ziele
- [Implementierungsdetails](design/implementation.md) - Wie Hemlock intern funktioniert

### Mitwirken
- [Richtlinien für Beiträge](contributing/guidelines.md) - Wie Sie beitragen können
- [Testanleitung](contributing/testing.md) - Tests schreiben und ausführen

## Kurzreferenz

### Hallo Welt
```hemlock
print("Hello, World!");
```

### Grundlegende Typen
```hemlock
let x: i32 = 42;           // 32-Bit vorzeichenbehaftete Ganzzahl
let y: u8 = 255;           // 8-Bit vorzeichenlose Ganzzahl
let pi: f64 = 3.14159;     // 64-Bit Fließkommazahl
let name: string = "Alice"; // UTF-8 String
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode-Codepunkt
```

### Speicherverwaltung
```hemlock
// Sicherer Buffer (empfohlen)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Roher Zeiger (für Experten)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### Async/Nebenläufigkeit
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## Philosophie

Hemlock ist **explizit statt implizit**, immer:
- Semikolons sind obligatorisch
- Manuelle Speicherverwaltung (kein GC)
- Optionale Typannotationen mit Laufzeitprüfungen
- Unsichere Operationen sind erlaubt (Ihre Verantwortung)

Wir geben Ihnen die Werkzeuge, um sicher zu sein (`buffer`, Typannotationen, Grenzprüfung), aber wir zwingen Sie nicht, sie zu verwenden (`ptr`, manueller Speicher, unsichere Operationen).

## Hilfe erhalten

- **Quellcode**: [GitHub-Repository](https://github.com/hemlang/hemlock)
- **Paketmanager**: [hpm](https://github.com/hemlang/hpm) - Hemlock-Paketmanager
- **Issues**: Fehler melden und Features anfragen
- **Beispiele**: Siehe das `examples/`-Verzeichnis
- **Tests**: Siehe das `tests/`-Verzeichnis für Verwendungsbeispiele

## Lizenz

Hemlock wird unter der MIT-Lizenz veröffentlicht.
