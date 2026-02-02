# Speicherverwaltung in Hemlock

> "Wir geben dir die Werkzeuge, um sicher zu sein, aber wir zwingen dich nicht, sie zu benutzen."

Dieses Dokument beschreibt die Speicherverwaltungssemantik in Hemlock und behandelt sowohl programmierverwalteten Speicher als auch laufzeitverwaltete Werte.

## Inhaltsverzeichnis

1. [Der Vertrag](#der-vertrag)
2. [Programmierverwalteter Speicher](#programmierverwalteter-speicher)
3. [Laufzeitverwaltete Werte](#laufzeitverwaltete-werte)
4. [Eigentumsübergabepunkte](#eigentumsübergabepunkte)
5. [Async und Nebenläufigkeit](#async-und-nebenläufigkeit)
6. [FFI-Speicherregeln](#ffi-speicherregeln)
7. [Ausnahmesicherheit](#ausnahmesicherheit)
8. [Best Practices](#best-practices)

---

## Der Vertrag

Hemlock hat eine klare Aufteilung der Speicherverwaltungsverantwortung:

| Speichertyp | Verwaltet von | Bereinigungsmethode |
|-------------|---------------|---------------------|
| Rohe Zeiger (`ptr`) | **Programmierer** | `free(ptr)` |
| Buffer (`buffer`) | **Programmierer** | `free(buf)` |
| Strings, Arrays, Objekte | **Laufzeit** | Automatisch (Referenzzählung) |
| Funktionen, Closures | **Laufzeit** | Automatisch (Referenzzählung) |
| Tasks, Channels | **Laufzeit** | Automatisch (Referenzzählung) |

**Das Kernprinzip:** Wenn du es explizit allokierst, gibst du es explizit frei. Alles andere wird automatisch behandelt.

---

## Programmierverwalteter Speicher

### Rohe Zeiger

```hemlock
let p = alloc(64);       // 64 Bytes allokieren
memset(p, 0, 64);        // Initialisieren
// ... Speicher verwenden ...
free(p);                 // Deine Verantwortung!
```

**Regeln:**
- `alloc()` gibt Speicher zurück, den du besitzt
- Du musst `free()` aufrufen, wenn du fertig bist
- Double-free wird abstürzen (absichtlich)
- Use-after-free ist undefiniertes Verhalten
- Zeigerarithmetik ist erlaubt, aber ungeprüft

### Typisierte Allokation

```hemlock
let arr = talloc("i32", 100);  // 100 i32s allokieren (400 Bytes)
ptr_write_i32(arr, 0, 42);     // In Index 0 schreiben
let val = ptr_read_i32(arr, 0); // Von Index 0 lesen
free(arr);                      // Immer noch deine Verantwortung
```

### Buffer (Sichere Alternative)

```hemlock
let buf = buffer(64);    // Grenzengeprüfter Buffer
buf[0] = 42;             // Sicherer Zugriff
// buf[100] = 1;         // Laufzeitfehler: außerhalb der Grenzen
free(buf);               // Braucht immer noch explizites free
```

**Hauptunterschied:** Buffer bieten Grenzenprüfung, rohe Zeiger nicht.

---

## Laufzeitverwaltete Werte

### Referenzzählung

Heap-allokierte Werte verwenden atomare Referenzzählung:

```hemlock
let s1 = "hello";        // String allokiert, refcount = 1
let s2 = s1;             // s2 teilt s1, refcount = 2
// Wenn beide aus dem Scope gehen, refcount → 0, Speicher freigegeben
```

**Referenzgezählte Typen:**
- `string` - UTF-8 Text
- `array` - Dynamische Arrays
- `object` - Schlüssel-Wert Objekte
- `function` - Closures
- `task` - Async Task Handles
- `channel` - Kommunikationskanäle

### Zyklenerkennung

Die Laufzeit behandelt Zyklen in Objektgraphen:

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // Zyklus: a → b → a
// Laufzeit verwendet visited sets um Zyklen während der Bereinigung zu erkennen und zu brechen
```

---

## Eigentumsübergabepunkte

### Variablenbindung

```hemlock
let x = [1, 2, 3];       // Array erstellt mit refcount 1
                         // x besitzt die Referenz
```

### Funktionsrückgaben

```hemlock
fn make_array() {
    return [1, 2, 3];    // Array-Eigentum wird an Aufrufer übertragen
}
let arr = make_array();  // arr besitzt jetzt die Referenz
```

### Zuweisung

```hemlock
let a = "hello";
let b = a;               // Geteilte Referenz (refcount erhöht)
b = "world";             // a hat immer noch "hello", b hat "world"
```

### Channel-Operationen

```hemlock
let ch = channel(10);
ch.send("message");      // Wert wird in Channel-Buffer kopiert
                         // Original bleibt gültig

let msg = ch.recv();     // Erhält Eigentum vom Channel
```

### Task-Spawning

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data wird TIEF KOPIERT für Isolation
data.x = 2;                       // Sicher - Task hat eigene Kopie
let result = join(task);          // result Eigentum wird an Aufrufer übertragen
```

---

## Async und Nebenläufigkeit

### Thread-Isolation

Gespawnte Tasks erhalten **tiefe Kopien** von veränderlichen Argumenten:

```hemlock
async fn worker(data) {
    data.x = 100;        // Modifiziert nur die Kopie des Tasks
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // Sicher - beeinflusst Task nicht
let result = join(task);
print(obj.x);            // 2 (unverändert durch Task)
print(result.x);         // 100 (modifizierte Kopie des Tasks)
```

### Geteilte Koordinationsobjekte

Einige Typen werden per Referenz geteilt (nicht kopiert):
- **Channels** - Für Inter-Task Kommunikation
- **Tasks** - Für Koordination (join/detach)

```hemlock
let ch = channel(1);
spawn(producer, ch);     // Gleicher Channel, keine Kopie
spawn(consumer, ch);     // Beide Tasks teilen den Channel
```

### Task-Ergebnisse

```hemlock
let task = spawn(compute);
let result = join(task);  // Aufrufer besitzt das Ergebnis
                          // Task-Referenz wird freigegeben wenn Task beendet
```

### Losgelöste Tasks

```hemlock
detach(spawn(background_work));
// Task läuft unabhängig
// Ergebnis wird automatisch freigegeben wenn Task abgeschlossen
// Kein Leak obwohl niemand join() aufruft
```

---

## FFI-Speicherregeln

### An C-Funktionen übergeben

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock behält Eigentum
                         // String ist während des Aufrufs gültig
                         // C-Funktion sollte ihn NICHT freigeben
```

### Von C-Funktionen empfangen

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C hat diesen Speicher allokiert
free(copy);                   // Deine Verantwortung freizugeben
```

### Struct-Übergabe (Nur Compiler)

```hemlock
// C struct Layout definieren
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // Per Wert zurückgegeben, kopiert
                                // Keine Bereinigung für Stack-Structs nötig
```

### Callback-Speicher

```hemlock
// Wenn C zurück nach Hemlock ruft:
// - Argumente gehören C (nicht freigeben)
// - Rückgabewert-Eigentum wird an C übertragen
```

---

## Ausnahmesicherheit

### Garantien

Die Laufzeit bietet diese Garantien:

1. **Kein Leak bei normalem Exit** - Alle laufzeitverwalteten Werte werden bereinigt
2. **Kein Leak bei Ausnahme** - Temporäre werden während Stack-Unwinding freigegeben
3. **Defer läuft bei Ausnahme** - Bereinigungscode wird ausgeführt

### Ausdrucksauswertung

```hemlock
// Wenn dies während Array-Erstellung wirft:
let arr = [f(), g(), h()];  // Teilweises Array wird freigegeben

// Wenn dies während Funktionsaufruf wirft:
foo(a(), b(), c());         // Zuvor ausgewertete Args werden freigegeben
```

### Defer für Bereinigung

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // Läuft bei return ODER Ausnahme

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close() läuft trotzdem!
    }
    return data;
}
```

---

## Best Practices

### 1. Bevorzuge Laufzeitverwaltete Typen

```hemlock
// Bevorzuge dies:
let data = [1, 2, 3, 4, 5];

// Statt dies (außer du brauchst Low-Level Kontrolle):
let data = talloc("i32", 5);
// ... muss daran denken freizugeben ...
```

### 2. Verwende Defer für Manuellen Speicher

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // Garantierte Bereinigung

    // ... buf verwenden ...
    // Kein free an jedem Return-Punkt nötig
}
```

### 3. Vermeide Rohe Zeiger in Async

```hemlock
// FALSCH - Zeiger könnte freigegeben werden bevor Task abgeschlossen
let p = alloc(64);
spawn(worker, p);          // Task bekommt den Zeigerwert
free(p);                   // Hoppla! Task verwendet ihn noch

// RICHTIG - verwende Channels oder kopiere Daten
let ch = channel(1);
let data = buffer(64);
// ... data füllen ...
ch.send(data);             // Tief kopiert
spawn(worker, ch);
free(data);                // Sicher - Task hat eigene Kopie
```

### 4. Schließe Channels wenn Fertig

```hemlock
let ch = channel(10);
// ... channel verwenden ...
ch.close();                // Leert und gibt gepufferte Werte frei
```

### 5. Join oder Detach Tasks

```hemlock
let task = spawn(work);

// Option 1: Auf Ergebnis warten
let result = join(task);

// Option 2: Fire and forget
// detach(task);

// NICHT: Task-Handle aus Scope gehen lassen ohne join oder detach
// (Es wird bereinigt, aber Ergebnis könnte leaken)
```

---

## Speicherprobleme Debuggen

### ASAN Aktivieren

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### Leak-Regressionstests Ausführen

```bash
make leak-regression       # Vollständige Suite
make leak-regression-quick # Umfassenden Test überspringen
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## Zusammenfassung

| Operation | Speicherverhalten |
|-----------|-------------------|
| `alloc(n)` | Allokiert, du gibst frei |
| `buffer(n)` | Allokiert mit Grenzenprüfung, du gibst frei |
| `"string"` | Laufzeit verwaltet |
| `[array]` | Laufzeit verwaltet |
| `{object}` | Laufzeit verwaltet |
| `spawn(fn)` | Kopiert Args tief, Laufzeit verwaltet Task |
| `join(task)` | Aufrufer besitzt Ergebnis |
| `detach(task)` | Laufzeit gibt Ergebnis frei wenn fertig |
| `ch.send(v)` | Kopiert Wert in Channel |
| `ch.recv()` | Aufrufer besitzt empfangenen Wert |
| `ch.close()` | Leert und gibt gepufferte Werte frei |
