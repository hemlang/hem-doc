# Eingebaute Funktionen Referenz

Vollständige Referenz für alle eingebauten Funktionen und Konstanten in Hemlock.

---

## Übersicht

Hemlock bietet eine Reihe von eingebauten Funktionen für I/O, Typ-Introspektion, Speicherverwaltung, Nebenläufigkeit und Systeminteraktion. Alle eingebauten Funktionen sind global verfügbar ohne Imports.

---

## I/O-Funktionen

### print

Gibt Werte auf stdout mit Zeilenumbruch aus.

**Signatur:**
```hemlock
print(...values): null
```

**Parameter:**
- `...values` - Beliebige Anzahl von Werten zum Ausgeben

**Rückgabe:** `null`

**Beispiele:**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// Mehrere Werte
print("x =", 10, "y =", 20);
```

**Verhalten:**
- Konvertiert alle Werte zu Strings
- Trennt mehrere Werte mit Leerzeichen
- Fuegt Zeilenumbruch am Ende hinzu
- Leert stdout

---

### read_line

Liest eine Zeile Text von stdin (Benutzereingabe).

**Signatur:**
```hemlock
read_line(): string | null
```

**Parameter:** Keine

**Rückgabe:**
- `string` - Die von stdin gelesene Zeile (Zeilenumbruch entfernt)
- `null` - Bei EOF (Ende der Datei/Eingabe)

**Beispiele:**
```hemlock
// Einfache Eingabeaufforderung
print("Wie ist dein Name?");
let name = read_line();
print("Hallo, " + name + "!");

// Zahlen lesen (erfordert manuelles Parsen)
print("Gib eine Zahl ein:");
let input = read_line();
let num = parse_int(input);  // Siehe unten für parse_int
print("Das Doppelte:", num * 2);

// EOF behandeln
let line = read_line();
if (line == null) {
    print("Ende der Eingabe");
}

// Mehrere Zeilen lesen
print("Gib Zeilen ein (Strg+D zum Beenden):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("Du sagtest:", line);
}
```

**Verhalten:**
- Blockiert bis Benutzer Enter drueckt
- Entfernt nachfolgenden Zeilenumbruch (`\n`) und Wagenruecklauf (`\r`)
- Gibt `null` bei EOF zurück (Strg+D auf Unix, Strg+Z auf Windows)
- Liest nur von stdin (nicht von Dateien)

**Benutzereingabe parsen:**

Da `read_line()` immer einen String zurückgibt, müssen Sie numerische Eingaben manuell parsen:

```hemlock
// Einfacher Integer-Parser
fn parse_int(s: string): i32 {
    let result: i32 = 0;
    let negative = false;
    let i = 0;

    if (s.length > 0 && s.char_at(0) == '-') {
        negative = true;
        i = 1;
    }

    while (i < s.length) {
        let c = s.char_at(i);
        let code: i32 = c;
        if (code >= 48 && code <= 57) {
            result = result * 10 + (code - 48);
        } else {
            break;
        }
        i = i + 1;
    }

    if (negative) {
        return -result;
    }
    return result;
}

// Verwendung
print("Gib dein Alter ein:");
let age = parse_int(read_line());
print("In 10 Jahren wirst du", age + 10, "sein");
```

**Siehe auch:** [Datei-API](file-api.md) zum Lesen aus Dateien

---

### eprint

Gibt einen Wert auf stderr mit Zeilenumbruch aus.

**Signatur:**
```hemlock
eprint(value: any): null
```

**Parameter:**
- `value` - Einzelner Wert zum Ausgeben auf stderr

**Rückgabe:** `null`

**Beispiele:**
```hemlock
eprint("Fehler: Datei nicht gefunden");
eprint(404);
eprint("Warnung: " + message);

// Typisches Fehlerbehandlungsmuster
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Fehler: Konfigurationsdatei nicht gefunden: " + path);
        return null;
    }
    // ...
}
```

**Verhalten:**
- Gibt auf stderr aus (Standardfehlerausgabe)
- Fuegt Zeilenumbruch am Ende hinzu
- Akzeptiert nur ein Argument (anders als `print`)
- Nützlich für Fehlermeldungen die sich nicht mit normaler Ausgabe vermischen sollen

**Unterschied zu print:**
- `print()` → stdout (normale Ausgabe, kann mit `>` umgeleitet werden)
- `eprint()` → stderr (Fehlerausgabe, kann mit `2>` umgeleitet werden)

```bash
# Shell-Beispiel: stdout und stderr trennen
./hemlock script.hml > output.txt 2> errors.txt
```

---

## Typ-Introspektion

### typeof

Gibt den Typnamen eines Wertes zurück.

**Signatur:**
```hemlock
typeof(value: any): string
```

**Parameter:**
- `value` - Beliebiger Wert

**Rückgabe:** Typname als String

**Beispiele:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// Typisierte Objekte
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// Andere Typen
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**Typnamen:**
- Primitive: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Zusammengesetzt: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Speziell: `"file"`, `"task"`, `"channel"`
- Benutzerdefiniert: Benutzerdefinierte Typnamen aus `define`

**Siehe auch:** [Typsystem](type-system.md)

---

## Befehlsausfuehrung

### exec

Fuehrt Shell-Befehl aus und erfasst Ausgabe.

**Signatur:**
```hemlock
exec(command: string): object
```

**Parameter:**
- `command` - Auszufuehrender Shell-Befehl

**Rückgabe:** Objekt mit Feldern:
- `output` (string) - stdout des Befehls
- `exit_code` (i32) - Exit-Statuscode (0 = Erfolg)

**Beispiele:**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// Exit-Status prüfen
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Gefunden:", r.output);
} else {
    print("Muster nicht gefunden");
}

// Mehrzeilige Ausgabe verarbeiten
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**Verhalten:**
- Fuehrt Befehl über `/bin/sh` aus
- Erfasst nur stdout (stderr geht zum Terminal)
- Blockiert bis Befehl abgeschlossen ist
- Gibt leeren String zurück wenn keine Ausgabe

**Fehlerbehandlung:**
```hemlock
try {
    let r = exec("nonexistent_command");
} catch (e) {
    print("Ausführung fehlgeschlagen:", e);
}
```

**Sicherheitswarnung:** Anfaellig für Shell-Injection. Validieren/bereinigen Sie immer Benutzereingaben.

**Einschränkungen:**
- Keine stderr-Erfassung
- Kein Streaming
- Kein Timeout
- Keine Signalbehandlung

---

### exec_argv

Fuehrt einen Befehl mit explizitem Argument-Array aus (keine Shell-Interpretation).

**Signatur:**
```hemlock
exec_argv(argv: array): object
```

**Parameter:**
- `argv` - Array von Strings: `[befehl, arg1, arg2, ...]`

**Rückgabe:** Objekt mit Feldern:
- `output` (string) - stdout des Befehls
- `exit_code` (i32) - Exit-Statuscode (0 = Erfolg)

**Beispiele:**
```hemlock
// Einfacher Befehl
let result = exec_argv(["ls", "-la"]);
print(result.output);

// Befehl mit Argumenten die Leerzeichen enthalten (sicher!)
let r = exec_argv(["grep", "hello world", "file.txt"]);

// Skript mit Argumenten ausführen
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**Unterschied zu exec:**
```hemlock
// exec() verwendet Shell - UNSICHER mit Benutzereingaben
exec("ls " + user_input);  // Shell-Injection-Risiko!

// exec_argv() umgeht Shell - SICHER
exec_argv(["ls", user_input]);  // Keine Injection möglich
```

**Wann verwenden:**
- Wenn Argumente Leerzeichen, Anführungszeichen oder Sonderzeichen enthalten
- Bei Verarbeitung von Benutzereingaben (Sicherheit)
- Wenn vorhersagbares Argument-Parsing benötigt wird

**Siehe auch:** `exec()` für einfache Shell-Befehle

---

## Fehlerbehandlung

### throw

Wirft eine Ausnahme.

**Signatur:**
```hemlock
throw expression
```

**Parameter:**
- `expression` - Zu werfender Wert (beliebiger Typ)

**Rückgabe:** Gibt nie zurück (überträgt Kontrolle)

**Beispiele:**
```hemlock
throw "Fehlermeldung";
throw 404;
throw { code: 500, message: "Interner Fehler" };
throw null;
```

**Siehe auch:** try/catch/finally-Anweisungen

---

### panic

Beendet Programm sofort mit Fehlermeldung (nicht wiederherstellbar).

**Signatur:**
```hemlock
panic(message?: any): never
```

**Parameter:**
- `message` (optional) - Auszugebende Fehlermeldung

**Rückgabe:** Gibt nie zurück (Programm beendet sich)

**Beispiele:**
```hemlock
panic();                          // Standard: "panic!"
panic("Unerreichbarer Code erreicht");
panic(42);

// Haeufiger Anwendungsfall
fn process_state(state: i32): string {
    if (state == 1) { return "bereit"; }
    if (state == 2) { return "läuft"; }
    panic("Ungueltiger Status: " + typeof(state));
}
```

**Verhalten:**
- Gibt Fehler auf stderr aus: `panic: <message>`
- Beendet mit Code 1
- **NICHT abfangbar** mit try/catch
- Verwenden für Bugs und nicht wiederherstellbare Fehler

**Panic vs Throw:**
- `panic()` - Nicht wiederherstellbarer Fehler, beendet sofort
- `throw` - Wiederherstellbarer Fehler, kann abgefangen werden

---

### assert

Stellt sicher dass eine Bedingung wahr ist, oder beendet mit Fehlermeldung.

**Signatur:**
```hemlock
assert(condition: any, message?: string): null
```

**Parameter:**
- `condition` - Auf Wahrheit zu pruefender Wert
- `message` (optional) - Benutzerdefinierte Fehlermeldung bei fehlgeschlagener Prüfung

**Rückgabe:** `null` (wenn Prüfung erfolgreich)

**Beispiele:**
```hemlock
// Grundlegende Prüfungen
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "Array darf nicht leer sein");

// Mit benutzerdefinierten Meldungen
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Division durch Null");
    return a / b;
}

// Funktionsargumente validieren
fn process_data(data: array) {
    assert(data != null, "data darf nicht null sein");
    assert(data.length > 0, "data darf nicht leer sein");
    // ...
}
```

**Verhalten:**
- Wenn Bedingung wahr: gibt `null` zurück, Ausführung fortgesetzt
- Wenn Bedingung falsch: gibt Fehler aus und beendet mit Code 1
- Falsche Werte: `false`, `0`, `0.0`, `null`, `""` (leerer String)
- Wahre Werte: alles andere

**Ausgabe bei Fehlschlag:**
```
Assertion failed: Array darf nicht leer sein
```

**Wann verwenden:**
- Validierung von Funktionsvorbedingungen
- Prüfen von Invarianten während der Entwicklung
- Fruehzeitiges Erkennen von Programmierfehlern

**assert vs panic:**
- `assert(cond, msg)` - Prueft eine Bedingung, schlaegt fehl wenn falsch
- `panic(msg)` - Schlaegt immer bedingungslos fehl

---

## Signalbehandlung

### signal

Registriert oder setzt Signal-Handler zurück.

**Signatur:**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**Parameter:**
- `signum` - Signalnummer (verwenden Sie Konstanten wie `SIGINT`)
- `handler` - Funktion die bei Signalempfang aufgerufen wird, oder `null` zum Zurücksetzen auf Standard

**Rückgabe:** Vorherige Handler-Funktion, oder `null`

**Beispiele:**
```hemlock
fn handle_interrupt(sig) {
    print("SIGINT abgefangen!");
}

signal(SIGINT, handle_interrupt);

// Auf Standard zurücksetzen
signal(SIGINT, null);
```

**Handler-Signatur:**
```hemlock
fn handler(signum: i32) {
    // signum enthält die Signalnummer
}
```

**Siehe auch:**
- [Signalkonstanten](#signalkonstanten)
- `raise()`

---

### raise

Sendet Signal an aktuellen Prozess.

**Signatur:**
```hemlock
raise(signum: i32): null
```

**Parameter:**
- `signum` - Zu sendende Signalnummer

**Rückgabe:** `null`

**Beispiele:**
```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

raise(SIGUSR1);
raise(SIGUSR1);
print(count);  // 2
```

---

## Globale Variablen

### args

Kommandozeilenargumente-Array.

**Typ:** `array` von Strings

**Struktur:**
- `args[0]` - Skriptdateiname
- `args[1..n]` - Kommandozeilenargumente

**Beispiele:**
```bash
# Befehl: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// Argumente durchlaufen
let i = 1;
while (i < args.length) {
    print("Argument", i, ":", args[i]);
    i = i + 1;
}
```

**REPL-Verhalten:** Im REPL ist `args.length` 0 (leeres Array)

---

## Signalkonstanten

Standard-POSIX-Signalkonstanten (i32-Werte):

### Unterbrechung & Beendigung

| Konstante  | Wert  | Beschreibung                                |
|------------|-------|---------------------------------------------|
| `SIGINT`   | 2     | Unterbrechung von Tastatur (Strg+C)         |
| `SIGTERM`  | 15    | Beendigungsanforderung                      |
| `SIGQUIT`  | 3     | Beenden von Tastatur (Strg+\)               |
| `SIGHUP`   | 1     | Aufhaengen am steuernden Terminal erkannt   |
| `SIGABRT`  | 6     | Abbruchsignal                               |

### Benutzerdefiniert

| Konstante  | Wert  | Beschreibung               |
|------------|-------|----------------------------|
| `SIGUSR1`  | 10    | Benutzerdefiniertes Signal 1 |
| `SIGUSR2`  | 12    | Benutzerdefiniertes Signal 2 |

### Prozesssteuerung

| Konstante  | Wert  | Beschreibung                      |
|------------|-------|-----------------------------------|
| `SIGALRM`  | 14    | Wecker-Timer                      |
| `SIGCHLD`  | 17    | Kindprozess-Statusaenderung       |
| `SIGCONT`  | 18    | Fortsetzen wenn gestoppt          |
| `SIGSTOP`  | 19    | Prozess stoppen (nicht abfangbar) |
| `SIGTSTP`  | 20    | Terminal-Stopp (Strg+Z)           |

### I/O

| Konstante  | Wert  | Beschreibung                           |
|------------|-------|----------------------------------------|
| `SIGPIPE`  | 13    | Unterbrochene Pipe                     |
| `SIGTTIN`  | 21    | Hintergrund-Lesen vom Terminal         |
| `SIGTTOU`  | 22    | Hintergrund-Schreiben zum Terminal     |

**Beispiele:**
```hemlock
fn handle_signal(sig) {
    if (sig == SIGINT) {
        print("Unterbrechung erkannt");
    }
    if (sig == SIGTERM) {
        print("Beendigung angefordert");
    }
}

signal(SIGINT, handle_signal);
signal(SIGTERM, handle_signal);
```

**Hinweis:** `SIGKILL` (9) und `SIGSTOP` (19) können nicht abgefangen oder ignoriert werden.

---

## Mathematik/Arithmetik-Funktionen

### div

Ganzzahldivision die eine Gleitkommazahl zurückgibt.

**Signatur:**
```hemlock
div(a: number, b: number): f64
```

**Parameter:**
- `a` - Dividend
- `b` - Divisor

**Rückgabe:** Abrundung von `a / b` als Gleitkommazahl (f64)

**Beispiele:**
```hemlock
let result = div(7, 2);    // 3.0 (nicht 3.5)
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0 (Abrundung richtet sich nach negativer Unendlichkeit)
```

**Hinweis:** In Hemlock gibt der `/`-Operator immer eine Gleitkommazahl zurück. Verwenden Sie `div()` für Ganzzahldivision wenn Sie den ganzzahligen Teil als Gleitkommazahl benötigen, oder `divi()` wenn Sie ein ganzzahliges Ergebnis benötigen.

---

### divi

Ganzzahldivision die eine Ganzzahl zurückgibt.

**Signatur:**
```hemlock
divi(a: number, b: number): i64
```

**Parameter:**
- `a` - Dividend
- `b` - Divisor

**Rückgabe:** Abrundung von `a / b` als Ganzzahl (i64)

**Beispiele:**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4 (Abrundung richtet sich nach negativer Unendlichkeit)
```

**Vergleich:**
```hemlock
print(7 / 2);      // 3.5 (normale Division, immer Gleitkomma)
print(div(7, 2));  // 3.0 (Ganzzahldivision, Gleitkommaergebnis)
print(divi(7, 2)); // 3   (Ganzzahldivision, Ganzzahlergebnis)
```

---

## Speicherverwaltungsfunktionen

Siehe [Speicher-API](memory-api.md) für vollständige Referenz:
- `alloc(size)` - Rohen Speicher allokieren
- `free(ptr)` - Speicher freigeben
- `buffer(size)` - Sicheren Buffer allokieren
- `memset(ptr, byte, size)` - Speicher fuellen
- `memcpy(dest, src, size)` - Speicher kopieren
- `realloc(ptr, new_size)` - Allokation vergroessern/verkleinern

### sizeof

Gibt die Größe eines Typs in Bytes zurück.

**Signatur:**
```hemlock
sizeof(type): i32
```

**Parameter:**
- `type` - Eine Typkonstante (`i32`, `f64`, `ptr`, etc.) oder Typname-String

**Rückgabe:** Größe in Bytes als `i32`

**Beispiele:**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// Mit Typ-Aliasen
print(sizeof(byte));     // 1 (gleich wie u8)
print(sizeof(integer));  // 4 (gleich wie i32)
print(sizeof(number));   // 8 (gleich wie f64)

// String-Form funktioniert auch
print(sizeof("i32"));    // 4
```

**Unterstuetzte Typen:**
| Typ | Größe | Aliase |
|-----|---------|--------|
| `i8` | 1 | - |
| `i16` | 2 | - |
| `i32` | 4 | `integer` |
| `i64` | 8 | - |
| `u8` | 1 | `byte` |
| `u16` | 2 | - |
| `u32` | 4 | - |
| `u64` | 8 | - |
| `f32` | 4 | - |
| `f64` | 8 | `number` |
| `ptr` | 8 | - |
| `rune` | 4 | - |
| `bool` | 1 | - |

**Siehe auch:** `talloc()` für typisierte Allokation

---

### talloc

Allokiert Speicher für ein typisiertes Array (typbewusste Allokation).

**Signatur:**
```hemlock
talloc(type, count: i32): ptr
```

**Parameter:**
- `type` - Eine Typkonstante (`i32`, `f64`, `ptr`, etc.)
- `count` - Anzahl der zu allokierenden Elemente

**Rückgabe:** `ptr` zum allokierten Speicher, oder `null` bei Fehlschlag

**Beispiele:**
```hemlock
// Array von 10 i32s allokieren (40 Bytes)
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// Array von 5 f64s allokieren (40 Bytes)
let float_arr = talloc(f64, 5);

// Array von 100 Bytes allokieren
let byte_arr = talloc(u8, 100);

// Nicht vergessen freizugeben!
free(int_arr);
free(float_arr);
free(byte_arr);
```

**Vergleich mit alloc:**
```hemlock
// Diese sind äquivalent:
let p1 = talloc(i32, 10);      // Typbewusst: 10 i32s
let p2 = alloc(sizeof(i32) * 10);  // Manuelle Berechnung

// talloc ist klarer und weniger fehleranfaellig
```

**Fehlerbehandlung:**
- Gibt `null` zurück wenn Allokation fehlschlaegt
- Beendet mit Fehler wenn count nicht positiv ist
- Prueft auf Groessenueberlauf (count * element_size)

**Siehe auch:** `alloc()`, `sizeof()`, `free()`

---

## FFI-Pointer-Hilfsfunktionen

Diese Funktionen helfen beim Lesen und Schreiben von typisierten Werten im Rohspeicher, nützlich für FFI und Low-Level-Speichermanipulation.

### ptr_null

Erstellt einen Null-Pointer.

**Signatur:**
```hemlock
ptr_null(): ptr
```

**Rückgabe:** Ein Null-Pointer

**Beispiel:**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Pointer ist null");
}
```

---

### ptr_offset

Berechnet Pointer-Offset (Pointer-Arithmetik).

**Signatur:**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**Parameter:**
- `ptr` - Basis-Pointer
- `index` - Element-Index
- `element_size` - Größe jedes Elements in Bytes

**Rückgabe:** Pointer zum Element am gegebenen Index

**Beispiel:**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### Pointer-Lesefunktionen

Liest typisierte Werte aus dem Speicher.

| Funktion | Signatur | Rückgabe | Beschreibung |
|----------|----------|-----------|--------------|
| `ptr_read_i8` | `(ptr)` | `i8` | Liest vorzeichenbehaftete 8-Bit-Ganzzahl |
| `ptr_read_i16` | `(ptr)` | `i16` | Liest vorzeichenbehaftete 16-Bit-Ganzzahl |
| `ptr_read_i32` | `(ptr)` | `i32` | Liest vorzeichenbehaftete 32-Bit-Ganzzahl |
| `ptr_read_i64` | `(ptr)` | `i64` | Liest vorzeichenbehaftete 64-Bit-Ganzzahl |
| `ptr_read_u8` | `(ptr)` | `u8` | Liest vorzeichenlose 8-Bit-Ganzzahl |
| `ptr_read_u16` | `(ptr)` | `u16` | Liest vorzeichenlose 16-Bit-Ganzzahl |
| `ptr_read_u32` | `(ptr)` | `u32` | Liest vorzeichenlose 32-Bit-Ganzzahl |
| `ptr_read_u64` | `(ptr)` | `u64` | Liest vorzeichenlose 64-Bit-Ganzzahl |
| `ptr_read_f32` | `(ptr)` | `f32` | Liest 32-Bit-Gleitkommazahl |
| `ptr_read_f64` | `(ptr)` | `f64` | Liest 64-Bit-Gleitkommazahl |
| `ptr_read_ptr` | `(ptr)` | `ptr` | Liest Pointer-Wert |

**Beispiel:**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### Pointer-Schreibfunktionen

Schreibt typisierte Werte in den Speicher.

| Funktion | Signatur | Rückgabe | Beschreibung |
|----------|----------|-----------|--------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | Schreibt vorzeichenbehaftete 8-Bit-Ganzzahl |
| `ptr_write_i16` | `(ptr, value)` | `null` | Schreibt vorzeichenbehaftete 16-Bit-Ganzzahl |
| `ptr_write_i32` | `(ptr, value)` | `null` | Schreibt vorzeichenbehaftete 32-Bit-Ganzzahl |
| `ptr_write_i64` | `(ptr, value)` | `null` | Schreibt vorzeichenbehaftete 64-Bit-Ganzzahl |
| `ptr_write_u8` | `(ptr, value)` | `null` | Schreibt vorzeichenlose 8-Bit-Ganzzahl |
| `ptr_write_u16` | `(ptr, value)` | `null` | Schreibt vorzeichenlose 16-Bit-Ganzzahl |
| `ptr_write_u32` | `(ptr, value)` | `null` | Schreibt vorzeichenlose 32-Bit-Ganzzahl |
| `ptr_write_u64` | `(ptr, value)` | `null` | Schreibt vorzeichenlose 64-Bit-Ganzzahl |
| `ptr_write_f32` | `(ptr, value)` | `null` | Schreibt 32-Bit-Gleitkommazahl |
| `ptr_write_f64` | `(ptr, value)` | `null` | Schreibt 64-Bit-Gleitkommazahl |
| `ptr_write_ptr` | `(ptr, value)` | `null` | Schreibt Pointer-Wert |

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### Buffer/Pointer-Konvertierung

#### buffer_ptr

Holt rohen Pointer aus einem Buffer.

**Signatur:**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**Beispiel:**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// Jetzt zeigt p auf denselben Speicher wie buf
```

#### ptr_to_buffer

Erstellt einen Buffer-Wrapper um einen rohen Pointer.

**Signatur:**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**Beispiel:**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // Hat jetzt Grenzenprüfung
// Hinweis: Freigeben von buf gibt den zugrundeliegenden Speicher frei
```

---

## Datei-I/O-Funktionen

Siehe [Datei-API](file-api.md) für vollständige Referenz:
- `open(path, mode?)` - Datei öffnen

---

## Nebenlaeufigkeitsfunktionen

Siehe [Nebenlaeufigkeits-API](concurrency-api.md) für vollständige Referenz:
- `spawn(fn, args...)` - Task starten
- `join(task)` - Auf Task warten
- `detach(task)` - Task ablösen
- `channel(capacity)` - Kanal erstellen

### apply

Ruft eine Funktion dynamisch mit einem Array von Argumenten auf.

**Signatur:**
```hemlock
apply(fn: function, args: array): any
```

**Parameter:**
- `fn` - Die aufzurufende Funktion
- `args` - Array von Argumenten die an die Funktion übergeben werden

**Rückgabe:** Der Rückgabewert der aufgerufenen Funktion

**Beispiele:**
```hemlock
fn add(a, b) {
    return a + b;
}

// Mit Array von Argumenten aufrufen
let result = apply(add, [2, 3]);
print(result);  // 5

// Dynamischer Dispatch
let operations = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calculate(op: string, args: array) {
    return apply(operations[op], args);
}

print(calculate("add", [10, 5]));  // 15
print(calculate("mul", [10, 5]));  // 50
print(calculate("sub", [10, 5]));  // 5

// Variable Argumente
fn sum(...nums) {
    let total = 0;
    for (n in nums) {
        total = total + n;
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5];
print(apply(sum, numbers));  // 15
```

**Anwendungsfaelle:**
- Dynamischer Funktionsdispatch basierend auf Laufzeitwerten
- Aufrufen von Funktionen mit variablen Argumentlisten
- Implementierung von Higher-Order-Utilities (map, filter, etc.)
- Plugin/Erweiterungssysteme

---

### select

Wartet auf Daten von mehreren Kanaelen, gibt zurück wenn einer Daten hat.

**Signatur:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parameter:**
- `channels` - Array von Kanalwerten
- `timeout_ms` (optional) - Timeout in Millisekunden (-1 oder weglassen für unendlich)

**Rückgabe:**
- `{ channel, value }` - Objekt mit dem Kanal der Daten hatte und dem empfangenen Wert
- `null` - Bei Timeout

**Beispiele:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Produzenten-Tasks
spawn(fn() {
    sleep(100);
    ch1.send("von Kanal 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("von Kanal 2");
});

// Auf erste Nachricht warten
let result = select([ch1, ch2]);
print(result.value);  // "von Kanal 2" (kam zuerst an)

// Mit Timeout
let result2 = select([ch1, ch2], 1000);  // Warte bis zu 1 Sekunde
if (result2 == null) {
    print("Timeout - keine Daten empfangen");
} else {
    print("Empfangen:", result2.value);
}

// Kontinuierliche Select-Schleife
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("Keine Aktivitaet für 5 Sekunden");
        break;
    }
    print("Nachricht erhalten:", msg.value);
}
```

**Verhalten:**
- Blockiert bis ein Kanal Daten hat oder Timeout abläuft
- Gibt sofort zurück wenn ein Kanal bereits Daten hat
- Wenn Kanal geschlossen und leer ist, gibt `{ channel, value: null }` zurück
- Prueft Kanäle der Reihe nach (erster bereiter Kanal gewinnt)

**Anwendungsfaelle:**
- Multiplexen mehrerer Produzenten
- Implementierung von Timeouts bei Kanaloperationen
- Aufbau von Event-Loops mit mehreren Quellen

---

## Zusammenfassungstabelle

### Funktionen

| Funktion   | Kategorie       | Rückgabe    | Beschreibung                     |
|------------|-----------------|--------------|----------------------------------|
| `print`    | I/O             | `null`       | Auf stdout ausgeben              |
| `read_line`| I/O             | `string?`    | Zeile von stdin lesen            |
| `eprint`   | I/O             | `null`       | Auf stderr ausgeben              |
| `typeof`   | Typ             | `string`     | Typname holen                    |
| `exec`     | Befehl          | `object`     | Shell-Befehl ausführen          |
| `exec_argv`| Befehl          | `object`     | Mit Argument-Array ausführen    |
| `assert`   | Fehler          | `null`       | Bedingung prüfen oder beenden   |
| `panic`    | Fehler          | `never`      | Nicht wiederherstellbarer Fehler (beendet) |
| `signal`   | Signal          | `function?`  | Signal-Handler registrieren      |
| `raise`    | Signal          | `null`       | Signal an Prozess senden         |
| `alloc`    | Speicher        | `ptr`        | Rohen Speicher allokieren        |
| `talloc`   | Speicher        | `ptr`        | Typisierte Allokation            |
| `sizeof`   | Speicher        | `i32`        | Typgroesse in Bytes holen        |
| `free`     | Speicher        | `null`       | Speicher freigeben               |
| `buffer`   | Speicher        | `buffer`     | Sicheren Buffer allokieren       |
| `memset`   | Speicher        | `null`       | Speicher fuellen                 |
| `memcpy`   | Speicher        | `null`       | Speicher kopieren                |
| `realloc`  | Speicher        | `ptr`        | Allokation vergroessern          |
| `open`     | Datei-I/O       | `file`       | Datei öffnen                    |
| `spawn`    | Nebenläufigkeit| `task`       | Nebenlaeufigen Task starten      |
| `join`     | Nebenläufigkeit| `any`        | Auf Task-Ergebnis warten         |
| `detach`   | Nebenläufigkeit| `null`       | Task abloesen                    |
| `channel`  | Nebenläufigkeit| `channel`    | Kommunikationskanal erstellen    |
| `select`   | Nebenläufigkeit| `object?`    | Auf mehrere Kanäle warten       |
| `apply`    | Funktionen      | `any`        | Funktion mit Args-Array aufrufen |

### Globale Variablen

| Variable   | Typ      | Beschreibung                      |
|------------|----------|-----------------------------------|
| `args`     | `array`  | Kommandozeilenargumente           |

### Konstanten

| Konstante  | Typ   | Kategorie | Wert  | Beschreibung              |
|------------|-------|-----------|-------|---------------------------|
| `SIGINT`   | `i32` | Signal    | 2     | Tastatur-Unterbrechung    |
| `SIGTERM`  | `i32` | Signal    | 15    | Beendigungsanforderung    |
| `SIGQUIT`  | `i32` | Signal    | 3     | Tastatur-Beenden          |
| `SIGHUP`   | `i32` | Signal    | 1     | Aufhaengen                |
| `SIGABRT`  | `i32` | Signal    | 6     | Abbruch                   |
| `SIGUSR1`  | `i32` | Signal    | 10    | Benutzerdefiniert 1       |
| `SIGUSR2`  | `i32` | Signal    | 12    | Benutzerdefiniert 2       |
| `SIGALRM`  | `i32` | Signal    | 14    | Wecker-Timer              |
| `SIGCHLD`  | `i32` | Signal    | 17    | Kind-Statusaenderung      |
| `SIGCONT`  | `i32` | Signal    | 18    | Fortsetzen                |
| `SIGSTOP`  | `i32` | Signal    | 19    | Stopp (nicht abfangbar)   |
| `SIGTSTP`  | `i32` | Signal    | 20    | Terminal-Stopp            |
| `SIGPIPE`  | `i32` | Signal    | 13    | Unterbrochene Pipe        |
| `SIGTTIN`  | `i32` | Signal    | 21    | Hintergrund-Terminal-Lesen |
| `SIGTTOU`  | `i32` | Signal    | 22    | Hintergrund-Terminal-Schreiben |

---

## Siehe auch

- [Typsystem](type-system.md) - Typen und Konvertierungen
- [Speicher-API](memory-api.md) - Speicherallokationsfunktionen
- [Datei-API](file-api.md) - Datei-I/O-Funktionen
- [Nebenlaeufigkeits-API](concurrency-api.md) - Async/Nebenlaeufigkeitsfunktionen
- [String-API](string-api.md) - String-Methoden
- [Array-API](array-api.md) - Array-Methoden
