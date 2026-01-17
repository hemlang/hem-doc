# Lernpfade

Verschiedene Ziele erfordern unterschiedliches Wissen. Wählen Sie den Pfad, der zu dem passt, was Sie erstellen möchten.

---

## Pfad 1: Schnelle Skripte & Automatisierung

**Ziel:** Skripte schreiben, um Aufgaben zu automatisieren, Dateien zu verarbeiten und Dinge zu erledigen.

**Zeit bis zur Produktivität:** Schnell - Sie können sofort mit dem Schreiben nützlicher Skripte beginnen.

### Was Sie lernen werden

1. **[Schnellstart](quick-start.md)** - Ihr erstes Programm, grundlegende Syntax
2. **[Zeichenketten](../language-guide/strings.md)** - Textverarbeitung, Aufteilen, Suchen
3. **[Arrays](../language-guide/arrays.md)** - Listen, Filtern, Daten transformieren
4. **[Datei-I/O](../advanced/file-io.md)** - Dateien lesen und schreiben
5. **[Kommandozeilenargumente](../advanced/command-line-args.md)** - Eingaben von Benutzern erhalten

### Vorerst überspringen

- Speicherverwaltung (automatisch für Skripte)
- Async/Nebenläufigkeit (übertrieben für einfache Skripte)
- FFI (nur für C-Interop benötigt)

### Beispielprojekt: Datei-Umbenenner

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// Alle .txt-Dateien in .md umbenennen
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Umbenannt: ${file} -> ${new_name}`);
    }
}
```

---

## Pfad 2: Datenverarbeitung & Analyse

**Ziel:** Daten parsen, transformieren, Berichte generieren.

**Zeit bis zur Produktivität:** Schnell - Hemlocks String- und Array-Methoden machen dies einfach.

### Was Sie lernen werden

1. **[Schnellstart](quick-start.md)** - Grundlagen
2. **[Zeichenketten](../language-guide/strings.md)** - Parsen, Aufteilen, Formatieren
3. **[Arrays](../language-guide/arrays.md)** - map, filter, reduce für Datentransformation
4. **[Objekte](../language-guide/objects.md)** - Strukturierte Daten
5. **Standardbibliothek:**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON-Parsing
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - CSV-Dateien
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - Dateioperationen

### Beispielprojekt: CSV-Analysator

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// Gesamtumsatz berechnen
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Gesamtumsatz: ${total}€`);

// Top-Verkäufer finden
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Top-Verkauf: ${top.product} - ${top.amount}€`);
```

---

## Pfad 3: Web- & Netzwerkprogrammierung

**Ziel:** HTTP-Clients erstellen, mit APIs arbeiten, Server erstellen.

**Zeit bis zur Produktivität:** Mittel - erfordert Verständnis der Async-Grundlagen.

### Was Sie lernen werden

1. **[Schnellstart](quick-start.md)** - Grundlagen
2. **[Funktionen](../language-guide/functions.md)** - Callbacks und Closures
3. **[Fehlerbehandlung](../language-guide/error-handling.md)** - try/catch für Netzwerkfehler
4. **[Async & Nebenläufigkeit](../advanced/async-concurrency.md)** - spawn, await, Channels
5. **Standardbibliothek:**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - HTTP-Anfragen
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON für APIs
   - **[@stdlib/net](../../stdlib/docs/net.md)** - TCP/UDP-Sockets
   - **[@stdlib/url](../../stdlib/docs/url.md)** - URL-Parsing

### Beispielprojekt: API-Client

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// GET-Anfrage
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}: ${user.email}`);
}

// POST-Anfrage
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`Benutzer erstellt mit ID: ${parse(result.body).id}`);
```

---

## Pfad 4: Systemprogrammierung

**Ziel:** Low-Level-Code schreiben, mit Speicher arbeiten, mit C-Bibliotheken interagieren.

**Zeit bis zur Produktivität:** Länger - erfordert Verständnis der Speicherverwaltung.

### Was Sie lernen werden

1. **[Schnellstart](quick-start.md)** - Grundlagen
2. **[Typen](../language-guide/types.md)** - i32, u8, ptr usw. verstehen
3. **[Speicherverwaltung](../language-guide/memory.md)** - alloc, free, Puffer
4. **[FFI](../advanced/ffi.md)** - C-Funktionen aufrufen
5. **[Signale](../advanced/signals.md)** - Signalverarbeitung

### Schlüsselkonzepte

**Speichersicherheits-Checkliste:**
- [ ] Jedes `alloc()` hat ein entsprechendes `free()`
- [ ] `buffer()` verwenden, es sei denn, Sie benötigen rohe `ptr`
- [ ] Zeiger nach dem Freigeben auf `null` setzen
- [ ] `try/finally` verwenden, um Bereinigung zu garantieren

**Typ-Mapping für FFI:**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long` (64-Bit) |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### Beispielprojekt: Benutzerdefinierter Speicherpool

```hemlock
// Einfacher Bump-Allocator
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool erschöpft";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// Verwenden
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // Gesamten Speicher wiederverwenden
pool_destroy();  // Aufräumen
```

---

## Pfad 5: Parallele & Nebenläufige Programme

**Ziel:** Code auf mehreren CPU-Kernen ausführen, reaktionsfähige Anwendungen erstellen.

**Zeit bis zur Produktivität:** Mittel - Async-Syntax ist unkompliziert, aber das Nachdenken über Parallelität erfordert Übung.

### Was Sie lernen werden

1. **[Schnellstart](quick-start.md)** - Grundlagen
2. **[Funktionen](../language-guide/functions.md)** - Closures (wichtig für Async)
3. **[Async & Nebenläufigkeit](../advanced/async-concurrency.md)** - Vollständiger Tiefgang
4. **[Atomics](../advanced/atomics.md)** - Lock-freie Programmierung

### Schlüsselkonzepte

**Hemlocks Async-Modell:**
- `async fn` - Definiert eine Funktion, die auf einem anderen Thread laufen kann
- `spawn(fn, args...)` - Startet die Ausführung, gibt ein Task-Handle zurück
- `join(task)` oder `await task` - Warten auf Fertigstellung, Ergebnis abrufen
- `channel(size)` - Warteschlange zum Senden von Daten zwischen Tasks erstellen

**Wichtig:** Tasks erhalten *Kopien* von Werten. Wenn Sie einen Zeiger übergeben, sind Sie dafür verantwortlich, sicherzustellen, dass der Speicher gültig bleibt, bis der Task abgeschlossen ist.

### Beispielprojekt: Paralleler Dateiprozessor

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// Alle Dateien parallel verarbeiten
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// Ergebnisse sammeln
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}: ${count} Zeilen`);
    total_lines = total_lines + count;
}

print(`Gesamt: ${total_lines} Zeilen`);
```

---

## Was zuerst lernen (Jeder Pfad)

Egal welches Ziel, beginnen Sie mit diesen Grundlagen:

### Woche 1: Kerngrundlagen
1. **[Schnellstart](quick-start.md)** - Schreiben und führen Sie Ihr erstes Programm aus
2. **[Syntax](../language-guide/syntax.md)** - Variablen, Operatoren, Kontrollfluss
3. **[Funktionen](../language-guide/functions.md)** - Funktionen definieren und aufrufen

### Woche 2: Datenverarbeitung
4. **[Zeichenketten](../language-guide/strings.md)** - Textmanipulation
5. **[Arrays](../language-guide/arrays.md)** - Sammlungen und Iteration
6. **[Objekte](../language-guide/objects.md)** - Strukturierte Daten

### Woche 3: Robustheit
7. **[Fehlerbehandlung](../language-guide/error-handling.md)** - try/catch/throw
8. **[Module](../language-guide/modules.md)** - Import/Export, Stdlib verwenden

### Dann: Wählen Sie Ihren Pfad oben

---

## Spickzettel: Kommend von anderen Sprachen

### Von Python

| Python | Hemlock | Hinweise |
|--------|---------|----------|
| `x = 42` | `let x = 42;` | Semikolons erforderlich |
| `def fn():` | `fn name() { }` | Geschweifte Klammern erforderlich |
| `if x:` | `if (x) { }` | Klammern und geschweifte Klammern erforderlich |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | C-ähnliche For-Schleifen |
| `for item in list:` | `for (item in array) { }` | For-in funktioniert gleich |
| `list.append(x)` | `array.push(x);` | Anderer Methodenname |
| `len(s)` | `s.length` oder `len(s)` | Beides funktioniert |
| Automatischer Speicher | Manuell für `ptr` | Die meisten Typen räumen automatisch auf |

### Von JavaScript

| JavaScript | Hemlock | Hinweise |
|------------|---------|----------|
| `let x = 42` | `let x = 42;` | Gleich (Semikolons erforderlich) |
| `const x = 42` | `let x = 42;` | Kein const-Schlüsselwort |
| `function fn()` | `fn name() { }` | Anderes Schlüsselwort |
| `() => x` | `fn() { return x; }` | Keine Pfeilfunktionen |
| `async/await` | `async/await` | Gleiche Syntax |
| `Promise` | `spawn/join` | Anderes Modell |
| Automatische GC | Manuell für `ptr` | Die meisten Typen räumen automatisch auf |

### Von C/C++

| C | Hemlock | Hinweise |
|---|---------|----------|
| `int x = 42;` | `let x: i32 = 42;` | Typ nach Doppelpunkt |
| `malloc(n)` | `alloc(n)` | Gleiches Konzept |
| `free(p)` | `free(p)` | Gleich |
| `char* s = "hi"` | `let s = "hi";` | Strings werden verwaltet |
| `#include` | `import { } from` | Modul-Imports |
| Manuell für alles | Auto für die meisten Typen | Nur `ptr` braucht manuell |

---

## Hilfe erhalten

- **[Glossar](../glossary.md)** - Definitionen von Programmierbegriffen
- **[Beispiele](../../examples/)** - Vollständige funktionierende Programme
- **[Tests](../../tests/)** - Sehen Sie, wie Funktionen verwendet werden
- **GitHub Issues** - Fragen stellen, Fehler melden

---

## Schwierigkeitsstufen

In der gesamten Dokumentation sehen Sie diese Markierungen:

| Markierung | Bedeutung |
|------------|-----------|
| **Anfänger** | Keine vorherige Programmiererfahrung erforderlich |
| **Fortgeschritten** | Setzt grundlegende Programmierkenntnisse voraus |
| **Experte** | Erfordert Verständnis von Systemkonzepten |

Wenn Sie etwas, das als "Anfänger" markiert ist, verwirrt, schauen Sie im [Glossar](../glossary.md) nach Begriffsdefinitionen.
