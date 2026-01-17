# Test-Leitfaden für Hemlock

Dieser Leitfaden erklärt Hemlocks Test-Philosophie, wie man Tests schreibt und wie man die Test-Suite ausführt.

---

## Inhaltsverzeichnis

- [Test-Philosophie](#test-philosophie)
- [Test-Suite-Struktur](#test-suite-struktur)
- [Tests ausführen](#tests-ausführen)
- [Tests schreiben](#tests-schreiben)
- [Testkategorien](#testkategorien)
- [Speicherleck-Tests](#speicherleck-tests)
- [Continuous Integration](#continuous-integration)
- [Best Practices](#best-practices)

---

## Test-Philosophie

### Kernprinzipien

**1. Testgetriebene Entwicklung (TDD)**

Schreiben Sie Tests **bevor** Sie Features implementieren:

```
1. Schreiben Sie einen fehlschlagenden Test
2. Implementieren Sie das Feature
3. Führen Sie den Test aus (sollte bestehen)
4. Refaktorieren Sie bei Bedarf
5. Wiederholen
```

**Vorteile:**
- Stellt sicher, dass Features tatsächlich funktionieren
- Verhindert Regressionen
- Dokumentiert erwartetes Verhalten
- Macht Refactoring sicherer

**2. Umfassende Abdeckung**

Testen Sie sowohl Erfolgs- als auch Fehlerfälle:

```hemlock
// Erfolgsfall
let x: u8 = 255;  // Sollte funktionieren

// Fehlerfall
let y: u8 = 256;  // Sollte einen Fehler werfen
```

**3. Früh und oft testen**

Führen Sie Tests aus:
- Vor dem Committen von Code
- Nach dem Vornehmen von Änderungen
- Vor dem Einreichen von Pull Requests
- Während des Code-Reviews

**Regel:** Alle Tests müssen vor dem Mergen bestehen.

### Was zu testen ist

**Immer testen:**
- Grundfunktionalität (Happy Path)
- Fehlerbedingungen (Sad Path)
- Randfälle (Grenzwertbedingungen)
- Typprüfung und -konvertierungen
- Speicherverwaltung (keine Lecks)
- Nebenläufigkeit und Race Conditions

**Beispiel für Testabdeckung:**
```hemlock
// Feature: String.substr(start, length)

// Happy Path
print("hello".substr(0, 5));  // "hello"

// Randfälle
print("hello".substr(0, 0));  // "" (leer)
print("hello".substr(5, 0));  // "" (am Ende)
print("hello".substr(2, 100)); // "llo" (über Ende hinaus)

// Fehlerfälle
// "hello".substr(-1, 5);  // Fehler: negativer Index
// "hello".substr(0, -1);  // Fehler: negative Länge
```

---

## Test-Suite-Struktur

### Verzeichnisorganisation

```
tests/
├── run_tests.sh          # Haupt-Testrunner-Skript
├── primitives/           # Typsystem-Tests
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # Typkonvertierungs-Tests
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # Zeiger-/Buffer-Tests
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # String-Operationstests
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # Kontrollfluss-Tests
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # Funktions- und Closure-Tests
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # Objekt-Tests
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # Array-Operationstests
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # Schleifen-Tests
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # Fehlerbehandlungs-Tests
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # Datei-I/O-Tests
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # Nebenläufigkeits-Tests
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # FFI-Tests
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # Signal-Behandlungs-Tests
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # Kommandozeilen-Argument-Tests
    └── basic.hml
```

### Testdatei-Benennung

**Konventionen:**
- Verwenden Sie beschreibende Namen: `method_chaining.hml` nicht `test1.hml`
- Gruppieren Sie verwandte Tests: `string_substr.hml`, `string_slice.hml`
- Ein Feature-Bereich pro Datei
- Halten Sie Dateien fokussiert und klein

---

## Tests ausführen

### Alle Tests ausführen

```bash
# Vom Hemlock-Stammverzeichnis
make test

# Oder direkt
./tests/run_tests.sh
```

**Ausgabe:**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### Bestimmte Kategorie ausführen

```bash
# Nur String-Tests ausführen
./tests/run_tests.sh tests/strings/

# Nur eine Testdatei ausführen
./tests/run_tests.sh tests/strings/concat.hml

# Mehrere Kategorien ausführen
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Mit Valgrind ausführen (Speicherleck-Prüfung)

```bash
# Einzelnen Test auf Lecks prüfen
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# Alle Tests prüfen (langsam!)
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### Fehlgeschlagene Tests debuggen

```bash
# Mit ausführlicher Ausgabe ausführen
./hemlock tests/failing_test.hml

# Mit gdb ausführen
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # bei Absturz
```

---

## Tests schreiben

### Testdatei-Format

Testdateien sind einfach Hemlock-Programme mit erwarteter Ausgabe:

**Beispiel: tests/primitives/integers.hml**
```hemlock
// Grundlegende Integer-Literale testen
let x = 42;
print(x);  // Erwartet: 42

let y: i32 = 100;
print(y);  // Erwartet: 100

// Arithmetik testen
let sum = x + y;
print(sum);  // Erwartet: 142

// Typinferenz testen
let small = 10;
print(typeof(small));  // Erwartet: i32

let large = 5000000000;
print(typeof(large));  // Erwartet: i64
```

**Wie Tests funktionieren:**
1. Der Testrunner führt die .hml-Datei aus
2. Erfasst die stdout-Ausgabe
3. Vergleicht mit erwarteter Ausgabe (aus Kommentaren oder separater .out-Datei)
4. Meldet Bestanden/Fehlgeschlagen

### Methoden für erwartete Ausgabe

**Methode 1: Inline-Kommentare (empfohlen für einfache Tests)**

```hemlock
print("hello");  // Erwartet: hello
print(42);       // Erwartet: 42
```

Der Testrunner parst `// Erwartet: ...`-Kommentare.

**Methode 2: Separate .out-Datei**

Erstellen Sie `test_name.hml.out` mit erwarteter Ausgabe:

**test_name.hml:**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**test_name.hml.out:**
```
line 1
line 2
line 3
```

### Fehlerfälle testen

Fehler-Tests sollten das Programm mit einem Nicht-Null-Status beenden:

**Beispiel: tests/primitives/range_error.hml**
```hemlock
// Dies sollte mit einem Typfehler fehlschlagen
let x: u8 = 256;  // Außerhalb des Bereichs für u8
```

**Erwartetes Verhalten:**
- Programm beendet sich mit Nicht-Null-Status
- Gibt Fehlermeldung auf stderr aus

**Testrunner-Behandlung:**
- Tests, die Fehler erwarten, sollten in separaten Dateien sein
- Verwenden Sie die Namenskonvention: `*_error.hml` oder `*_fail.hml`
- Dokumentieren Sie den erwarteten Fehler in Kommentaren

### Erfolgsfälle testen

**Beispiel: tests/strings/methods.hml**
```hemlock
// substr testen
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Erwartet: world

// find testen
let pos = s.find("world");
print(pos);  // Erwartet: 6

// contains testen
let has = s.contains("lo");
print(has);  // Erwartet: true

// trim testen
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Erwartet: hello
```

### Randfälle testen

**Beispiel: tests/arrays/edge_cases.hml**
```hemlock
// Leeres Array
let empty = [];
print(empty.length);  // Erwartet: 0

// Einzelnes Element
let single = [42];
print(single[0]);  // Erwartet: 42

// Negativer Index (sollte in separater Testdatei fehlschlagen)
// print(single[-1]);  // Fehler

// Index über Ende hinaus (sollte fehlschlagen)
// print(single[100]);  // Fehler

// Grenzwertbedingungen
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Erwartet: [] (leer)
print(arr.slice(3, 3));  // Erwartet: [] (leer)
print(arr.slice(1, 2));  // Erwartet: [2]
```

### Typsystem testen

**Beispiel: tests/conversions/promotion.hml**
```hemlock
// Typ-Promotion bei binären Operationen testen

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Erwartet: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Erwartet: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Erwartet: i32
```

### Nebenläufigkeit testen

**Beispiel: tests/async/basic.hml**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Tasks spawnen
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// Joinen und Ergebnisse ausgeben
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Erwartet: 45
print(r2);  // Erwartet: 190
```

### Exceptions testen

**Beispiel: tests/exceptions/try_catch.hml**
```hemlock
// Grundlegendes try/catch testen
try {
    throw "error message";
} catch (e) {
    print("Gefangen: " + e);  // Erwartet: Gefangen: error message
}

// finally testen
let executed = false;
try {
    print("try");  // Erwartet: try
} finally {
    executed = true;
    print("finally");  // Erwartet: finally
}

// Exception-Propagierung testen
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // Erwartet: failure
}
```

---

## Testkategorien

### Primitiven-Tests

**Was zu testen ist:**
- Integer-Typen (i8, i16, i32, i64, u8, u16, u32, u64)
- Float-Typen (f32, f64)
- Boolean-Typ
- String-Typ
- Rune-Typ
- Null-Typ

**Beispielbereiche:**
- Literal-Syntax
- Typinferenz
- Bereichsprüfung
- Überlaufverhalten
- Typannotationen

### Konvertierungstests

**Was zu testen ist:**
- Implizite Typ-Promotion
- Explizite Typkonvertierung
- Verlustbehaftete Konvertierungen (sollten fehlschlagen)
- Typ-Promotion bei Operationen
- Typ-übergreifende Vergleiche

### Speichertests

**Was zu testen ist:**
- alloc/free-Korrektheit
- Buffer-Erstellung und -Zugriff
- Grenzprüfung bei Buffern
- memset, memcpy, realloc
- Speicherleck-Erkennung (Valgrind)

### String-Tests

**Was zu testen ist:**
- Konkatenation
- Alle 18 String-Methoden
- UTF-8-Behandlung
- Rune-Indizierung
- String + Rune-Konkatenation
- Randfälle (leere Strings, einzelnes Zeichen, etc.)

### Kontrollfluss-Tests

**Was zu testen ist:**
- if/else/else if
- while-Schleifen
- for-Schleifen
- switch-Anweisungen
- break/continue
- return-Anweisungen

### Funktions-Tests

**Was zu testen ist:**
- Funktionsdefinition und -aufruf
- Parameterübergabe
- Rückgabewerte
- Rekursion
- Closures und Capture
- First-Class-Funktionen
- Anonyme Funktionen

### Objekt-Tests

**Was zu testen ist:**
- Objekt-Literale
- Feldzugriff und -zuweisung
- Methoden und self-Bindung
- Duck Typing
- Optionale Felder
- JSON-Serialisierung/Deserialisierung
- Erkennung zirkulärer Referenzen

### Array-Tests

**Was zu testen ist:**
- Array-Erstellung
- Indizierung und Zuweisung
- Alle 15 Array-Methoden
- Gemischte Typen
- Dynamische Größenanpassung
- Randfälle (leer, einzelnes Element)

### Exception-Tests

**Was zu testen ist:**
- try/catch/finally
- throw-Anweisung
- Exception-Propagierung
- Verschachtelte try/catch
- Return in try/catch/finally
- Nicht gefangene Exceptions

### I/O-Tests

**Was zu testen ist:**
- Datei-Öffnungsmodi
- Lese-/Schreiboperationen
- Seek/Tell
- Dateieigenschaften
- Fehlerbehandlung (fehlende Dateien, etc.)
- Ressourcen-Aufräumen

### Async-Tests

**Was zu testen ist:**
- spawn/join/detach
- Channel send/recv
- Exception-Propagierung in Tasks
- Mehrere gleichzeitige Tasks
- Channel-Blockierungsverhalten

### FFI-Tests

**Was zu testen ist:**
- dlopen/dlclose
- dlsym
- dlcall mit verschiedenen Typen
- Typkonvertierung
- Fehlerbehandlung

---

## Speicherleck-Tests

### Valgrind verwenden

**Grundlegende Verwendung:**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**Beispielausgabe (keine Lecks):**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**Beispielausgabe (mit Leck):**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### Häufige Leck-Quellen

**1. Fehlende free()-Aufrufe:**
```c
// SCHLECHT
char *str = malloc(100);
// ... str verwenden
// Vergessen freizugeben!

// GUT
char *str = malloc(100);
// ... str verwenden
free(str);
```

**2. Verlorene Zeiger:**
```c
// SCHLECHT
char *ptr = malloc(100);
ptr = malloc(200);  // Referenz zur ersten Allokation verloren!

// GUT
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. Exception-Pfade:**
```c
// SCHLECHT
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // Leck!
    }
    free(data);
}

// GUT
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### Bekannte akzeptable Lecks

Einige kleine "Lecks" sind beabsichtigte Start-Allokationen:

**Globale Built-ins:**
```hemlock
// Eingebaute Funktionen, FFI-Typen und Konstanten werden beim Start allokiert
// und beim Beenden nicht freigegeben (typischerweise ~200 Bytes)
```

Dies sind keine echten Lecks - es sind einmalige Allokationen, die für die Programmlebensdauer bestehen bleiben und beim Beenden vom Betriebssystem bereinigt werden.

---

## Continuous Integration

### GitHub Actions (Zukunft)

Sobald CI eingerichtet ist, werden alle Tests automatisch ausgeführt bei:
- Push zum Main-Branch
- Pull-Request-Erstellung/-Aktualisierung
- Geplante tägliche Läufe

**CI-Workflow:**
1. Hemlock bauen
2. Test-Suite ausführen
3. Auf Speicherlecks prüfen (Valgrind)
4. Ergebnisse im PR melden

### Pre-Commit-Prüfungen

Vor dem Committen ausführen:

```bash
# Frisch bauen
make clean && make

# Alle Tests ausführen
make test

# Einige Tests auf Lecks prüfen
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## Best Practices

### Dos

**Tests zuerst schreiben (TDD)**
```bash
1. tests/feature/new_feature.hml erstellen
2. Feature in src/ implementieren
3. Tests ausführen, bis sie bestehen
```

**Sowohl Erfolg als auch Fehler testen**
```hemlock
// Erfolg: tests/feature/success.hml
let result = do_thing();
print(result);  // Erwartet: erwarteter Wert

// Fehler: tests/feature/failure.hml
do_invalid_thing();  // Sollte fehlschlagen
```

**Beschreibende Testnamen verwenden**
```
Gut: tests/strings/substr_utf8_boundary.hml
Schlecht:  tests/test1.hml
```

**Tests fokussiert halten**
- Ein Feature-Bereich pro Datei
- Klares Setup und Assertions
- Minimaler Code

**Kommentare hinzufügen, die knifflige Tests erklären**
```hemlock
// Testen, dass Closure äußere Variable per Referenz erfasst
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // Nach Closure-Erstellung modifizieren
    return f();  // Sollte 20 zurückgeben, nicht 10
}
```

**Randfälle testen**
- Leere Eingaben
- Null-Werte
- Grenzwerte (min/max)
- Große Eingaben
- Negative Werte

### Don'ts

**Tests nicht überspringen**
- Alle Tests müssen vor dem Mergen bestehen
- Kommentieren Sie fehlschlagende Tests nicht aus
- Beheben Sie den Fehler oder entfernen Sie das Feature

**Keine Tests schreiben, die voneinander abhängen**
```hemlock
// SCHLECHT: test2.hml hängt von test1.hml-Ausgabe ab
// Tests sollten unabhängig sein
```

**Keine Zufallswerte in Tests verwenden**
```hemlock
// SCHLECHT: Nicht-deterministisch
let x = random();
print(x);  // Ausgabe nicht vorhersagbar

// GUT: Deterministisch
let x = 42;
print(x);  // Erwartet: 42
```

**Keine Implementierungsdetails testen**
```hemlock
// SCHLECHT: Interne Struktur testen
let obj = { x: 10 };
// Nicht interne Feldreihenfolge, Kapazität etc. prüfen

// GUT: Verhalten testen
print(obj.x);  // Erwartet: 10
```

**Speicherlecks nicht ignorieren**
- Alle Tests sollten Valgrind-sauber sein
- Bekannte/akzeptable Lecks dokumentieren
- Lecks vor dem Mergen beheben

### Test-Wartung

**Wann Tests aktualisieren:**
- Feature-Verhalten ändert sich
- Fehlerbehebungen erfordern neue Testfälle
- Randfälle entdeckt
- Performance-Verbesserungen

**Wann Tests entfernen:**
- Feature aus der Sprache entfernt
- Test dupliziert bestehende Abdeckung
- Test war falsch

**Tests refaktorieren:**
- Verwandte Tests zusammen gruppieren
- Gemeinsamen Setup-Code extrahieren
- Einheitliche Benennung verwenden
- Tests einfach und lesbar halten

---

## Beispiel-Testsitzung

Hier ist ein vollständiges Beispiel für das Hinzufügen eines Features mit Tests:

### Feature: `array.first()`-Methode hinzufügen

**1. Zuerst den Test schreiben:**

```bash
# Testdatei erstellen
cat > tests/arrays/first_method.hml << 'EOF'
// array.first()-Methode testen

// Grundfall
let arr = [1, 2, 3];
print(arr.first());  // Erwartet: 1

// Einzelnes Element
let single = [42];
print(single.first());  // Erwartet: 42

// Leeres Array (sollte fehlschlagen - separate Testdatei)
// let empty = [];
// print(empty.first());  // Fehler
EOF
```

**2. Den Test ausführen (sollte fehlschlagen):**

```bash
./hemlock tests/arrays/first_method.hml
# Fehler: Methode 'first' nicht auf Array gefunden
```

**3. Das Feature implementieren:**

`src/interpreter/builtins.c` bearbeiten:

```c
// array_first-Methode hinzufügen
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Fehler: Kann erstes Element eines leeren Arrays nicht holen\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// In Array-Methoden-Tabelle registrieren
// ... zur Array-Methodenregistrierung hinzufügen
```

**4. Den Test ausführen (sollte bestehen):**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# Erfolg!
```

**5. Auf Speicherlecks prüfen:**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. Vollständige Test-Suite ausführen:**

```bash
make test
# Total: 252 tests (251 + neuer)
# Passed: 252
# Failed: 0
```

**7. Committen:**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## Zusammenfassung

**Denken Sie daran:**
- Tests zuerst schreiben (TDD)
- Erfolgs- und Fehlerfälle testen
- Alle Tests vor dem Committen ausführen
- Auf Speicherlecks prüfen
- Bekannte Probleme dokumentieren
- Tests einfach und fokussiert halten

**Testqualität ist genauso wichtig wie Code-Qualität!**
