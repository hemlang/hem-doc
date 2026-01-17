# Hemlock Implementierungsdetails

Dieses Dokument beschreibt die technische Implementierung der Hemlock-Sprache, einschließlich Projektstruktur, Kompilierungspipeline, Laufzeitarchitektur und Designentscheidungen.

---

## Inhaltsverzeichnis

- [Projektstruktur](#projektstruktur)
- [Kompilierungspipeline](#kompilierungspipeline)
- [Modulares Interpreter-Design](#modulares-interpreter-design)
- [Laufzeitarchitektur](#laufzeitarchitektur)
- [Wertdarstellung](#wertdarstellung)
- [Typsystem-Implementierung](#typsystem-implementierung)
- [Speicherverwaltung](#speicherverwaltung)
- [Nebenläufigkeitsmodell](#nebenläufigkeitsmodell)
- [Zukunftspläne](#zukunftspläne)

---

## Projektstruktur

```
hemlock/
├── src/
│   ├── frontend/              # Gemeinsam: Lexer, Parser, AST
│   │   ├── lexer.c            # Tokenisierung
│   │   ├── parser/            # Rekursiver Abstiegsparser
│   │   ├── ast.c              # AST-Knotenverwaltung
│   │   └── module.c           # Modulauflösung
│   ├── backends/
│   │   ├── interpreter/       # hemlock: Tree-Walking-Interpreter
│   │   │   ├── main.c         # CLI-Einstiegspunkt
│   │   │   ├── runtime.c      # Ausdrucks-/Anweisungsauswertung
│   │   │   ├── builtins.c     # Eingebaute Funktionen
│   │   │   └── ...
│   │   └── compiler/          # hemlockc: C-Code-Generator
│   │       ├── main.c         # CLI, Orchestrierung
│   │       ├── type_check.c   # Kompilierzeit-Typprüfung
│   │       ├── codegen.c      # Code-Generierungskontext
│   │       ├── codegen_expr.c # Ausdrucks-Codegen
│   │       ├── codegen_stmt.c # Anweisungs-Codegen
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # Language Server Protocol
│   │   └── bundler/           # Bundle-/Paket-Werkzeuge
├── runtime/                   # libhemlock_runtime.a (für kompilierte Programme)
├── stdlib/                    # Standardbibliothek (39 Module)
│   └── docs/                  # Moduldokumentation
├── tests/
│   ├── parity/                # Tests, die beide Backends bestehen müssen
│   ├── interpreter/           # Interpreter-spezifische Tests
│   └── compiler/              # Compiler-spezifische Tests
├── examples/                  # Beispielprogramme
└── docs/                      # Dokumentation
```

### Verzeichnisorganisation

**`include/`** - Öffentliche API-Header, die die Schnittstelle zwischen Komponenten definieren:
- Saubere Trennung zwischen Lexer, Parser, AST und Interpreter
- Vorwärtsdeklarationen zur Minimierung von Abhängigkeiten
- Öffentliche API zum Einbetten von Hemlock in andere Programme

**`src/`** - Implementierungsdateien:
- Dateien auf oberster Ebene behandeln Lexing, Parsing, AST-Verwaltung
- `main.c` bietet CLI und REPL
- Der Interpreter ist in separate Subsysteme modularisiert

**`src/interpreter/`** - Modulare Interpreter-Implementierung:
- Jedes Modul hat eine einzelne, klare Verantwortung
- Interne API in `internal.h` für Inter-Modul-Kommunikation definiert
- Module können unabhängig kompiliert werden für schnellere Builds

**`tests/`** - Umfassende Testsuite:
- Nach Funktionsbereich organisiert
- Jedes Verzeichnis enthält fokussierte Testfälle
- `run_tests.sh` orchestriert die Testausführung

---

## Kompilierungspipeline

Hemlock verwendet eine traditionelle Kompilierungspipeline mit verschiedenen Phasen:

### Phase 1: Lexikalische Analyse (Lexer)

**Eingabe:** Quellcode-Text
**Ausgabe:** Token-Strom
**Implementierung:** `src/lexer.c`

```
Quelle: "let x = 42;"
   ↓
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**Schlüsselfunktionen:**
- Erkennt Schlüsselwörter, Bezeichner, Literale, Operatoren, Interpunktion
- Behandelt UTF-8-Stringliterale und Rune-Literale
- Meldet Zeilennummern für Fehlermeldungen
- Einziger Durchlauf, kein Backtracking

### Phase 2: Syntaxanalyse (Parser)

**Eingabe:** Token-Strom
**Ausgabe:** Abstrakter Syntaxbaum (AST)
**Implementierung:** `src/parser.c`

```
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST: LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**Schlüsselfunktionen:**
- Rekursiver Abstiegsparser
- Baut Baumdarstellung der Programmstruktur auf
- Behandelt Operatorpriorität
- Validiert Syntax (Klammern, Semikolons usw.)
- Noch keine semantische Analyse (erfolgt zur Laufzeit)

**Operatorpriorität (niedrigste bis höchste):**
1. Zuweisung: `=`
2. Logisches ODER: `||`
3. Logisches UND: `&&`
4. Bitweises ODER: `|`
5. Bitweises XOR: `^`
6. Bitweises UND: `&`
7. Gleichheit: `==`, `!=`
8. Vergleich: `<`, `>`, `<=`, `>=`
9. Bitweise Verschiebungen: `<<`, `>>`
10. Addition/Subtraktion: `+`, `-`
11. Multiplikation/Division/Modulo: `*`, `/`, `%`
12. Unär: `!`, `-`, `~`
13. Aufruf/Index/Element: `()`, `[]`, `.`

### Phase 3a: Interpretation (Tree-Walking)

**Eingabe:** AST
**Ausgabe:** Programmausführung
**Implementierung:** `src/backends/interpreter/runtime.c`

```
AST: LetStmt { ... }
   ↓
Ausführung: Wertet AST-Knoten rekursiv aus
   ↓
Ergebnis: Variable x mit Wert 42 erstellt
```

**Schlüsselfunktionen:**
- Direkte AST-Traversierung (Tree-Walking-Interpreter)
- Dynamische Typprüfung zur Laufzeit
- Umgebungsbasierte Variablenspeicherung

### Phase 3b: Kompilierung (hemlockc)

**Eingabe:** AST
**Ausgabe:** Native ausführbare Datei über C-Codegenerierung
**Implementierung:** `src/backends/compiler/`

```
AST: LetStmt { ... }
   ↓
Typprüfung: Typen zur Kompilierzeit validieren
   ↓
C-Codegen: Äquivalenten C-Code generieren
   ↓
GCC: C zu nativer Binärdatei kompilieren
   ↓
Ergebnis: Eigenständige ausführbare Datei
```

**Schlüsselfunktionen:**
- Kompilierzeit-Typprüfung (standardmäßig aktiviert)
- C-Codegenerierung für Portabilität
- Linkt gegen `libhemlock_runtime.a`
- Deutlich schnellere Ausführung als Interpreter

---

## Compiler-Backend (hemlockc)

Der Hemlock-Compiler generiert C-Code aus dem AST, der dann mit GCC zu einer nativen ausführbaren Datei kompiliert wird.

### Compiler-Architektur

```
src/backends/compiler/
├── main.c              # CLI, Argumentparsing, Orchestrierung
├── codegen.c           # Kern-Codegenerierungskontext
├── codegen_expr.c      # Ausdrucks-Codegenerierung
├── codegen_stmt.c      # Anweisungs-Codegenerierung
├── codegen_call.c      # Funktionsaufruf-Generierung
├── codegen_closure.c   # Closure-Implementierung
├── codegen_program.c   # Programm-Generierung auf oberster Ebene
├── codegen_module.c    # Modul-/Import-Behandlung
├── type_check.c        # Kompilierzeit-Typprüfung
└── type_check.h        # Typprüfer-API
```

### Typprüfung

Der Compiler enthält ein vereinheitlichtes Typprüfungssystem, das:

1. **Typen zur Kompilierzeit validiert** - Erkennt Typfehler vor der Ausführung
2. **Dynamischen Code unterstützt** - Untypisierter Code wird als `any` behandelt (immer gültig)
3. **Optimierungshinweise liefert** - Identifiziert Variablen, die unboxed werden können

**Typprüfungs-Flags:**

| Flag | Beschreibung |
|------|--------------|
| (Standard) | Typprüfung aktiviert |
| `--check` | Nur Typprüfung, nicht kompilieren |
| `--no-type-check` | Typprüfung deaktivieren |
| `--strict-types` | Warnung bei impliziten `any`-Typen |

**Typprüfer-Implementierung:**

```c
// type_check.h - Schlüsselstrukturen
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // Optimierungshinweise
    // ... Typumgebung, Definitionen usw.
} TypeCheckContext;

// Haupteinstiegspunkt
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### Codegenerierung

Die Codegen-Phase übersetzt AST-Knoten in C-Code:

**Ausdruckszuordnung:**
```
Hemlock                 →  Generiertes C
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  Closure mit Umgebungserfassung
```

**Laufzeit-Integration:**

Generierter C-Code linkt gegen `libhemlock_runtime.a`, die bereitstellt:
- `HmlValue` tagged union-Typ
- Speicherverwaltung (Reference Counting)
- Eingebaute Funktionen (print, typeof usw.)
- Nebenläufigkeitsprimitiven (Tasks, Kanäle)
- FFI-Unterstützung

### Unboxing-Optimierung

Der Typprüfer identifiziert Variablen, die native C-Typen anstelle von geboxten `HmlValue` verwenden können:

**Unboxbare Muster:**
- Schleifenzähler mit bekanntem Integer-Typ
- Akkumulatorvariablen in Schleifen
- Variablen mit expliziten Typannotationen (i32, i64, f64, bool)

```hemlock
// Schleifenzähler 'i' kann zu nativem int32_t unboxed werden
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    sum = sum + i;
}
```

---

## Modulares Interpreter-Design

Der Interpreter ist für Wartbarkeit und Skalierbarkeit in fokussierte Module aufgeteilt.

### Modulverantwortlichkeiten

#### 1. Umgebung (`environment.c`) - 121 Zeilen

**Zweck:** Variablen-Scoping und Namensauflösung

**Schlüsselfunktionen:**
- `env_create()` - Neue Umgebung mit optionalem Elternteil erstellen
- `env_define()` - Neue Variable im aktuellen Scope definieren
- `env_get()` - Variable im aktuellen oder Eltern-Scope nachschlagen
- `env_set()` - Bestehenden Variablenwert aktualisieren
- `env_free()` - Umgebung und alle Variablen freigeben

**Design:**
- Verknüpfte Scopes (jede Umgebung hat Zeiger auf Elternteil)
- HashMap für schnelle Variablensuche
- Unterstützt lexikalisches Scoping für Closures

#### 2. Werte (`values.c`) - 394 Zeilen

**Zweck:** Wertkonstruktoren und Datenstrukturverwaltung

**Schlüsselfunktionen:**
- `value_create_*()` - Konstruktoren für jeden Werttyp
- `value_copy()` - Tiefe/flache Kopierlogik
- `value_free()` - Bereinigung und Speicherfreigabe
- `value_to_string()` - Stringdarstellung für Ausgabe

**Datenstrukturen:**
- Objekte (dynamische Feldarrays)
- Arrays (dynamische Größenänderung)
- Buffer (ptr + Länge + Kapazität)
- Closures (Funktion + erfasste Umgebung)
- Tasks und Kanäle (Nebenläufigkeitsprimitiven)

#### 3. Typen (`types.c`) - 440 Zeilen

**Zweck:** Typsystem, Konvertierungen und Duck-Typing

**Schlüsselfunktionen:**
- `type_check()` - Laufzeit-Typvalidierung
- `type_convert()` - Implizite Typkonvertierungen/-promotionen
- `duck_type_check()` - Strukturelle Typprüfung für Objekte
- `type_name()` - Druckbaren Typnamen abrufen

**Funktionen:**
- Typpromotionshierarchie (i8 → i16 → i32 → i64 → f32 → f64, wobei i64/u64 + f32 → f64)
- Bereichsprüfung für numerische Typen
- Duck-Typing für Objekttypdefinitionen
- Optionale Feldstandards

#### 4. Builtins (`builtins.c`) - 955 Zeilen

**Zweck:** Eingebaute Funktionen und globale Registrierung

**Schlüsselfunktionen:**
- `register_builtins()` - Alle eingebauten Funktionen und Konstanten registrieren
- Implementierungen eingebauter Funktionen (print, typeof, alloc, free usw.)
- Signalbehandlungsfunktionen
- Befehlsausführung (exec)

**Kategorien von Builtins:**
- I/O: print, open, read_file, write_file
- Speicher: alloc, free, memset, memcpy, realloc
- Typen: typeof, assert
- Nebenläufigkeit: spawn, join, detach, channel
- System: exec, signal, raise, panic
- FFI: dlopen, dlsym, dlcall, dlclose

#### 5. I/O (`io.c`) - 449 Zeilen

**Zweck:** Datei-I/O und JSON-Serialisierung

**Schlüsselfunktionen:**
- Dateiobjektmethoden (read, write, seek, tell, close)
- JSON-Serialisierung/Deserialisierung
- Erkennung zirkulärer Referenzen

**Funktionen:**
- Dateiobjekt mit Eigenschaften (Pfad, Modus, geschlossen)
- UTF-8-bewusste Text-I/O
- Binäre I/O-Unterstützung
- JSON-Roundtripping für Objekte und Arrays

#### 6. FFI (`ffi.c`) - Foreign Function Interface

**Zweck:** Aufrufen von C-Funktionen aus gemeinsam genutzten Bibliotheken

**Schlüsselfunktionen:**
- `dlopen()` - Gemeinsam genutzte Bibliothek laden
- `dlsym()` - Funktionszeiger nach Namen abrufen
- `dlcall()` - C-Funktion mit Typkonvertierung aufrufen
- `dlclose()` - Bibliothek entladen

**Funktionen:**
- Integration mit libffi für dynamische Funktionsaufrufe
- Automatische Typkonvertierung (Hemlock ↔ C-Typen)
- Unterstützung für alle primitiven Typen
- Zeiger- und Buffer-Unterstützung

#### 7. Laufzeit (`runtime.c`) - 865 Zeilen

**Zweck:** Ausdrucksauswertung und Anweisungsausführung

**Schlüsselfunktionen:**
- `eval_expr()` - Ausdrücke auswerten (rekursiv)
- `eval_stmt()` - Anweisungen ausführen
- Kontrollflussbehandlung (if, while, for, switch usw.)
- Ausnahmebehandlung (try/catch/finally/throw)

**Funktionen:**
- Rekursive Ausdrucksauswertung
- Kurzschluss-Auswertung für boolesche Ausdrücke
- Methodenaufruferkennung und `self`-Bindung
- Ausnahmepropagierung
- Break/continue/return-Behandlung

### Vorteile des modularen Designs

**1. Trennung der Zuständigkeiten**
- Jedes Modul hat eine klare Verantwortung
- Leicht zu finden, wo Funktionen implementiert sind
- Reduziert kognitive Belastung bei Änderungen

**2. Schnellere inkrementelle Builds**
- Nur modifizierte Module müssen neu kompiliert werden
- Parallele Kompilierung möglich
- Kürzere Iterationszeiten während der Entwicklung

**3. Einfacheres Testen und Debuggen**
- Module können isoliert getestet werden
- Bugs sind auf spezifische Subsysteme lokalisiert
- Mock-Implementierungen für Tests möglich

**4. Skalierbarkeit**
- Neue Funktionen können zu geeigneten Modulen hinzugefügt werden
- Module können unabhängig refaktoriert werden
- Codegröße pro Datei bleibt handhabbar

**5. Code-Organisation**
- Logische Gruppierung verwandter Funktionalität
- Klarer Abhängigkeitsgraph
- Einfacheres Onboarding für neue Mitwirkende

---

## Laufzeitarchitektur

### Wertdarstellung

Alle Werte in Hemlock werden durch die `Value`-Struktur unter Verwendung einer tagged union dargestellt:

```c
typedef struct Value {
    ValueType type;  // Laufzeit-Typ-Tag
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**Designentscheidungen:**
- **Tagged Union** für Typsicherheit bei gleichzeitiger Flexibilität
- **Laufzeit-Typ-Tags** ermöglichen dynamische Typisierung mit Typprüfung
- **Direkte Wertspeicherung** für Primitiven (kein Boxing)
- **Zeigerspeicherung** für heap-allokierte Typen (Strings, Objekte, Arrays)

### Beispiele für Speicherlayout

**Ganzzahl (i32):**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- Gesamtgröße: ~16 Bytes (8-Byte-Tag + 8-Byte-Union)
- Stack-allokiert
- Keine Heap-Allokation erforderlich

**String:**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // Zeiger auf Heap
}

Heap: "hello\0" (6 Bytes, nullterminiertes UTF-8)
```
- Wert ist 16 Bytes auf dem Stack
- Stringdaten sind heap-allokiert
- Muss manuell freigegeben werden

**Objekt:**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // Zeiger auf Heap
}

Heap: Object {
    type_name: "Person",
    fields: [
        { name: "name", value: Value{TYPE_STRING, "Alice"} },
        { name: "age", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- Objektstruktur auf dem Heap
- Felder in dynamischem Array gespeichert
- Feldwerte sind eingebettete Value-Structs

### Umgebungsimplementierung

Variablen werden in Umgebungsketten gespeichert:

```c
typedef struct Environment {
    HashMap *bindings;           // Name → Value
    struct Environment *parent;  // Lexikalischer Eltern-Scope
} Environment;
```

**Scope-Ketten-Beispiel:**
```
Globaler Scope: { print: <builtin>, args: <array> }
    ↑
Funktions-Scope: { x: 10, y: 20 }
    ↑
Block-Scope: { i: 0 }
```

**Suchalgorithmus:**
1. Hashmap der aktuellen Umgebung prüfen
2. Falls nicht gefunden, Elternumgebung prüfen
3. Wiederholen bis gefunden oder globaler Scope erreicht
4. Fehler wenn in keinem Scope gefunden

---

## Typsystem-Implementierung

### Typprüfungsstrategie

Hemlock verwendet **Laufzeit-Typprüfung** mit **optionalen Typannotationen**:

```hemlock
let x = 42;           // Keine Typprüfung, inferiert i32
let y: u8 = 255;      // Laufzeitprüfung: Wert muss in u8 passen
let z: i32 = x + y;   // Laufzeitprüfung + Typpromotion
```

**Implementierungsfluss:**
1. **Literalinferenz** - Lexer/Parser bestimmen initialen Typ aus Literal
2. **Typannotationsprüfung** - Falls Annotation vorhanden, bei Zuweisung validieren
3. **Promotion** - Binäre Operationen werden zu gemeinsamem Typ hochgestuft
4. **Konvertierung** - Explizite Konvertierungen erfolgen bei Bedarf

### Typpromotionsimplementierung

Typpromotion folgt einer festen Hierarchie mit Präzisionserhaltung:

```c
// Vereinfachte Promotionslogik
ValueType promote_types(ValueType a, ValueType b) {
    // f64 gewinnt immer
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 mit i64/u64 wird zu f64 hochgestuft (Präzisionserhaltung)
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // Größere Integer-Typen gewinnen
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**Typränge:**
- i8: 0
- u8: 1
- i16: 2
- u16: 3
- i32: 4
- u32: 5
- i64: 6
- u64: 7
- f32: 8
- f64: 9

### Duck-Typing-Implementierung

Objekttypprüfung verwendet strukturellen Vergleich:

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // Alle erforderlichen Felder prüfen
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // Fehlendes Feld
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // Falscher Typ
        }
    }

    return true;  // Alle erforderlichen Felder vorhanden und korrekter Typ
}
```

**Duck-Typing erlaubt:**
- Zusätzliche Felder in Objekten (ignoriert)
- Substrukturelle Typisierung (Objekt kann mehr als erforderlich haben)
- Typnamenzuweisung nach Validierung

---

## Speicherverwaltung

### Allokationsstrategie

Hemlock verwendet **manuelle Speicherverwaltung** mit zwei Allokationsprimitiven:

**1. Rohe Zeiger (`ptr`):**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Kein Speicher mehr\n");
        exit(1);
    }
    return ptr;
}
```
- Direktes malloc/free
- Kein Tracking
- Benutzerverantwortung zur Freigabe

**2. Buffer (`buffer`):**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- Verfolgt Größe und Kapazität
- Bereichsprüfung beim Zugriff
- Erfordert immer noch manuelles free

### Heap-allokierte Typen

**Strings:**
- UTF-8-Byte-Array auf dem Heap
- Nullterminiert für C-Interoperabilität
- Veränderbar (kann an Ort und Stelle modifiziert werden)
- Refgezählt (automatisch freigegeben, wenn Scope verlassen wird)

**Objekte:**
- Dynamisches Feldarray
- Feldnamen und Werte auf dem Heap
- Refgezählt (automatisch freigegeben, wenn Scope verlassen wird)
- Zirkuläre Referenzen möglich (behandelt mit Visited-Set-Tracking)

**Arrays:**
- Dynamisches Kapazitätsverdopplungswachstum
- Elemente sind eingebettete Value-Structs
- Automatische Neuzuweisung bei Wachstum
- Refgezählt (automatisch freigegeben, wenn Scope verlassen wird)

**Closures:**
- Erfassen Umgebung per Referenz
- Umgebung ist heap-allokiert
- Closure-Umgebungen werden ordnungsgemäß freigegeben, wenn nicht mehr referenziert

---

## Nebenläufigkeitsmodell

### Threading-Architektur

Hemlock verwendet **1:1-Threading** mit POSIX-Threads (pthreads):

```
Benutzer-Task          OS-Thread          CPU-Kern
------------          ---------          --------
spawn(f1) ------>  pthread_create --> Kern 0
spawn(f2) ------>  pthread_create --> Kern 1
spawn(f3) ------>  pthread_create --> Kern 2
```

**Schlüsseleigenschaften:**
- Jedes `spawn()` erstellt einen neuen pthread
- Kernel plant Threads über Kerne
- Echte parallele Ausführung (kein GIL)
- Präemptives Multitasking

### Task-Implementierung

```c
typedef struct Task {
    pthread_t thread;        // OS-Thread-Handle
    Value result;            // Rückgabewert
    char *error;             // Ausnahmemeldung (falls geworfen)
    pthread_mutex_t lock;    // Schützt Zustand
    TaskState state;         // RUNNING, FINISHED, ERROR
} Task;
```

**Task-Lebenszyklus:**
1. `spawn(func, args)` → Task erstellen, pthread starten
2. Thread führt Funktion mit Argumenten aus
3. Bei Rückgabe: Ergebnis speichern, Zustand auf FINISHED setzen
4. Bei Ausnahme: Fehlermeldung speichern, Zustand auf ERROR setzen
5. `join(task)` → Auf Thread warten, Ergebnis zurückgeben oder Ausnahme werfen

### Kanal-Implementierung

```c
typedef struct Channel {
    void **buffer;           // Zirkulärer Puffer von Value*
    size_t capacity;         // Maximale gepufferte Elemente
    size_t count;            // Aktuelle Elemente im Puffer
    size_t read_index;       // Nächste Leseposition
    size_t write_index;      // Nächste Schreibposition
    bool closed;             // Kanal-geschlossen-Flag
    pthread_mutex_t lock;    // Schützt Puffer
    pthread_cond_t not_full; // Signal wenn Platz verfügbar
    pthread_cond_t not_empty;// Signal wenn Daten verfügbar
} Channel;
```

**Sende-Operation:**
1. Mutex sperren
2. Warten wenn Puffer voll (cond_wait auf not_full)
3. Wert in buffer[write_index] schreiben
4. write_index inkrementieren (zirkulär)
5. not_empty signalisieren
6. Mutex entsperren

**Empfangs-Operation:**
1. Mutex sperren
2. Warten wenn Puffer leer (cond_wait auf not_empty)
3. Wert aus buffer[read_index] lesen
4. read_index inkrementieren (zirkulär)
5. not_full signalisieren
6. Mutex entsperren

**Synchronisationsgarantien:**
- Thread-sicheres Senden/Empfangen (durch Mutex geschützt)
- Blockierende Semantik (Produzent wartet wenn voll, Konsument wartet wenn leer)
- Geordnete Zustellung (FIFO innerhalb eines Kanals)

---

## Zukunftspläne

### Abgeschlossen: Compiler-Backend ✓

Das Compiler-Backend (`hemlockc`) wurde implementiert mit:
- C-Codegenerierung aus AST
- Kompilierzeit-Typprüfung (standardmäßig aktiviert)
- Laufzeitbibliothek (`libhemlock_runtime.a`)
- Volle Parität mit Interpreter (98% Testbestehensrate)
- Unboxing-Optimierungsframework

### Aktueller Fokus: Typsystem-Erweiterungen

**Aktuelle Verbesserungen:**
- Vereinheitlichte Typprüfungs- und Typinferenzsysteme
- Kompilierzeit-Typprüfung standardmäßig aktiviert
- `--check`-Flag für Nur-Typ-Validierung
- Typkontext wird an Codegen für Optimierungshinweise übergeben

### Zukünftige Erweiterungen

**Potenzielle Ergänzungen:**
- Generics/Templates
- Pattern Matching
- LSP-Integration für typbewusste IDE-Unterstützung
- Aggressivere Unboxing-Optimierungen
- Escape-Analyse für Stack-Allokation

### Langfristige Optimierungen

**Mögliche Verbesserungen:**
- Inline-Caching für Methodenaufrufe
- JIT-Kompilierung für heiße Codepfade
- Work-Stealing-Scheduler für bessere Nebenläufigkeit
- Profilgeführte Optimierung

---

## Implementierungsrichtlinien

### Hinzufügen neuer Features

Beim Implementieren neuer Features befolgen Sie diese Richtlinien:

**1. Das richtige Modul wählen:**
- Neue Werttypen → `values.c`
- Typkonvertierungen → `types.c`
- Eingebaute Funktionen → `builtins.c`
- I/O-Operationen → `io.c`
- Kontrollfluss → `runtime.c`

**2. Alle Schichten aktualisieren:**
- AST-Knotentypen hinzufügen falls nötig (`ast.h`, `ast.c`)
- Lexer-Token hinzufügen falls nötig (`lexer.c`)
- Parser-Regeln hinzufügen (`parser.c`)
- Laufzeitverhalten implementieren (`runtime.c` oder geeignetes Modul)
- Tests hinzufügen (`tests/`)

**3. Konsistenz beibehalten:**
- Bestehendem Codestil folgen
- Konsistente Namenskonventionen verwenden
- Öffentliche API in Headern dokumentieren
- Fehlermeldungen klar und konsistent halten

**4. Gründlich testen:**
- Testfälle vor der Implementierung hinzufügen
- Erfolgs- und Fehlerpfade testen
- Randfälle testen
- Keine Speicherlecks verifizieren (valgrind)

### Leistungsüberlegungen

**Aktuelle Engpässe:**
- HashMap-Suchen für Variablenzugriff
- Rekursive Funktionsaufrufe (keine TCO)
- String-Verkettung (allokiert jedes Mal neuen String)
- Typprüfungs-Overhead bei jeder Operation

**Optimierungsmöglichkeiten:**
- Variablenpositionen cachen (Inline-Caching)
- Endrekursionsoptimierung
- String-Builder für Verkettung
- Typinferenz um Laufzeitprüfungen zu überspringen

### Debugging-Tipps

**Nützliche Werkzeuge:**
- `valgrind` - Speicherleckerkennung
- `gdb` - Abstürze debuggen
- `-g`-Flag - Debug-Symbole
- `printf`-Debugging - Einfach aber effektiv

**Häufige Probleme:**
- Segfault → Nullzeiger-Dereferenzierung (Rückgabewerte prüfen)
- Speicherleck → Fehlender free()-Aufruf (value_free-Pfade prüfen)
- Typfehler → type_convert()- und type_check()-Logik prüfen
- Absturz in Threads → Race Condition (Mutex-Verwendung prüfen)

---

## Fazit

Hemlocks Implementierung priorisiert:
- **Modularität** - Saubere Trennung der Zuständigkeiten
- **Einfachheit** - Geradlinige Implementierung
- **Explizitheit** - Keine versteckte Magie
- **Wartbarkeit** - Leicht zu verstehen und zu modifizieren

Der aktuelle Tree-Walking-Interpreter ist absichtlich einfach, um schnelle Feature-Entwicklung und Experimente zu ermöglichen. Das zukünftige Compiler-Backend wird die Leistung verbessern und dabei die gleiche Semantik beibehalten.
