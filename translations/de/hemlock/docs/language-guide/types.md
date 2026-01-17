# Typsystem

Hemlock verfuegt ueber ein **dynamisches Typsystem** mit optionalen Typannotationen und Laufzeit-Typueberpruefung.

---

## Typauswahl-Leitfaden: Welchen Typ sollte ich verwenden?

**Neu bei Typen?** Beginnen Sie hier. Wenn Sie mit Typsystemen vertraut sind, springen Sie zu [Philosophie](#philosophie).

### Die kurze Antwort

**Lassen Sie Hemlock es einfach herausfinden:**

```hemlock
let count = 42;        // Hemlock weiss, dass dies eine Ganzzahl ist
let price = 19.99;     // Hemlock weiss, dass dies eine Dezimalzahl ist
let name = "Alice";    // Hemlock weiss, dass dies Text ist
let active = true;     // Hemlock weiss, dass dies ja/nein ist
```

Hemlock waehlt automatisch den richtigen Typ fuer Ihre Werte. Sie *muessen* keine Typen angeben.

### Wann Typannotationen hinzufuegen

Fuegen Sie Typen hinzu, wenn Sie:

1. **Genau ueber die Groesse sein wollen** - `i8` vs `i64` ist wichtig fuer Speicher oder FFI
2. **Ihren Code dokumentieren** - Typen zeigen, was eine Funktion erwartet
3. **Fehler frueh erkennen wollen** - Hemlock prueft Typen zur Laufzeit

```hemlock
// Ohne Typen (funktioniert gut):
fn add(a, b) {
    return a + b;
}

// Mit Typen (expliziter):
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Schnellreferenz: Zahlentypen waehlen

| Was Sie speichern | Empfohlener Typ | Beispiel |
|-------------------|-----------------|----------|
| Normale Ganzzahlen | `i32` (Standard) | `let count = 42;` |
| Sehr grosse Zahlen | `i64` | `let population = 8000000000;` |
| Nie-negative Zaehler | `u32` | `let items: u32 = 100;` |
| Bytes (0-255) | `u8` | `let pixel: u8 = 255;` |
| Dezimalzahlen/Brueche | `f64` (Standard) | `let price = 19.99;` |
| Leistungskritische Dezimalzahlen | `f32` | `let x: f32 = 1.5;` |

### Schnellreferenz: Alle Typen

| Kategorie | Typen | Wann verwenden |
|-----------|-------|----------------|
| **Ganzzahlen** | `i8`, `i16`, `i32`, `i64` | Zaehlen, IDs, Alter, usw. |
| **Nur-positive Zahlen** | `u8`, `u16`, `u32`, `u64` | Bytes, Groessen, Array-Laengen |
| **Dezimalzahlen** | `f32`, `f64` | Geld, Messungen, Mathematik |
| **Ja/Nein** | `bool` | Flags, Bedingungen |
| **Text** | `string` | Namen, Nachrichten, jeder Text |
| **Einzelnes Zeichen** | `rune` | Einzelne Buchstaben, Emoji |
| **Listen** | `array` | Sammlungen von Werten |
| **Benannte Felder** | `object` | Gruppierung verwandter Daten |
| **Roher Speicher** | `ptr`, `buffer` | Low-Level-Programmierung |
| **Nichts** | `null` | Abwesenheit eines Wertes |

### Haeufige Szenarien

**"Ich brauche nur eine Zahl"**
```hemlock
let x = 42;  // Fertig! Hemlock waehlt i32
```

**"Ich brauche Dezimalzahlen"**
```hemlock
let price = 19.99;  // Fertig! Hemlock waehlt f64
```

**"Ich arbeite mit Bytes (Dateien, Netzwerk)"**
```hemlock
let byte: u8 = 255;  // 0-255 Bereich
```

**"Ich brauche wirklich grosse Zahlen"**
```hemlock
let big = 9000000000000;  // Hemlock waehlt automatisch i64 (> i32 max)
// Oder explizit:
let big: i64 = 9000000000000;
```

**"Ich speichere Geld"**
```hemlock
// Option 1: Float (einfach, aber hat Praezisionsgrenzen)
let price: f64 = 19.99;

// Option 2: Als Cent speichern (praeziser)
let price_cents: i32 = 1999;  // 19.99 EUR als Ganzzahl-Cent
```

**"Ich uebergebe Daten an C-Code (FFI)"**
```hemlock
// C-Typen genau entsprechen
let c_int: i32 = 100;      // C 'int'
let c_long: i64 = 100;     // C 'long' (auf 64-bit)
let c_char: u8 = 65;       // C 'char'
let c_double: f64 = 3.14;  // C 'double'
```

### Was passiert, wenn Typen gemischt werden?

Wenn Sie verschiedene Typen kombinieren, befördert Hemlock zum "groesseren" Typ:

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // result ist f64 (12.5)
// Die Ganzzahl wurde automatisch zur Dezimalzahl
```

**Faustregel:** Floats "gewinnen" immer - das Mischen einer Ganzzahl mit einem Float ergibt einen Float.

### Typfehler

Wenn Sie versuchen, den falschen Typ zu verwenden, sagt Ihnen Hemlock dies zur Laufzeit:

```hemlock
let age: i32 = "dreissig";  // FEHLER: Typenkonflikt - erwartet i32, erhalten string
```

Um Typen zu konvertieren, verwenden Sie Typ-Konstruktorfunktionen:

```hemlock
let text = "42";
let number = i32(text);   // String zu Ganzzahl parsen: 42
let back = text + "";     // Bereits ein String
```

---

## Philosophie

- **Standardmaessig dynamisch** - Jeder Wert hat ein Laufzeit-Typ-Tag
- **Typisiert nach Wahl** - Optionale Typannotationen erzwingen Laufzeitpruefungen
- **Explizite Konvertierungen** - Implizite Konvertierungen folgen klaren Befoerderungsregeln
- **Ehrlich ueber Typen** - `typeof()` sagt immer die Wahrheit

## Primitive Typen

### Ganzzahltypen

**Vorzeichenbehaftete Ganzzahlen:**
```hemlock
let tiny: i8 = 127;              // 8-Bit  (-128 bis 127)
let small: i16 = 32767;          // 16-Bit (-32768 bis 32767)
let normal: i32 = 2147483647;    // 32-Bit (Standard)
let large: i64 = 9223372036854775807;  // 64-Bit
```

**Vorzeichenlose Ganzzahlen:**
```hemlock
let byte: u8 = 255;              // 8-Bit  (0 bis 255)
let word: u16 = 65535;           // 16-Bit (0 bis 65535)
let dword: u32 = 4294967295;     // 32-Bit (0 bis 4294967295)
let qword: u64 = 18446744073709551615;  // 64-Bit
```

**Typ-Aliase:**
```hemlock
let i: integer = 42;   // Alias fuer i32
let b: byte = 255;     // Alias fuer u8
```

### Gleitkommatypen

```hemlock
let f: f32 = 3.14159;        // 32-Bit Float
let d: f64 = 2.718281828;    // 64-Bit Float (Standard)
let n: number = 1.618;       // Alias fuer f64
```

### Boolescher Typ

```hemlock
let flag: bool = true;
let active: bool = false;
```

### String-Typ

```hemlock
let text: string = "Hallo, Welt!";
let empty: string = "";
```

Strings sind **veraenderlich**, **UTF-8-kodiert** und **heap-allokiert**.

Siehe [Strings](strings.md) fuer vollstaendige Details.

### Rune-Typ

```hemlock
let ch: rune = 'A';
let emoji: rune = '(Rakete)';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

Runes repraesentieren **Unicode-Codepoints** (U+0000 bis U+10FFFF).

Siehe [Runes](runes.md) fuer vollstaendige Details.

### Null-Typ

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null` ist sein eigener Typ mit einem einzelnen Wert.

## Zusammengesetzte Typen

### Array-Typ

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "zwei", true, null];  // Gemischte Typen erlaubt
let empty: array = [];
```

Siehe [Arrays](arrays.md) fuer vollstaendige Details.

### Object-Typ

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

Siehe [Objects](objects.md) fuer vollstaendige Details.

### Pointer-Typen

**Roher Pointer:**
```hemlock
let p: ptr = alloc(64);
// Keine Grenzpruefung, manuelle Lebenszeitverwaltung
free(p);
```

**Sicherer Buffer:**
```hemlock
let buf: buffer = buffer(64);
// Grenzgeprueft, verfolgt Laenge und Kapazitaet
free(buf);
```

Siehe [Speicherverwaltung](memory.md) fuer vollstaendige Details.

## Enum-Typen

Enums definieren eine Menge benannter Konstanten:

### Einfache Enums

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// Vergleich
if (c == Color.RED) {
    print("Es ist rot!");
}

// Switch auf Enum
switch (c) {
    case Color.RED:
        print("Stopp");
        break;
    case Color.GREEN:
        print("Los");
        break;
    case Color.BLUE:
        print("Blau?");
        break;
}
```

### Enums mit Werten

Enums koennen explizite Ganzzahlwerte haben:

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### Auto-inkrementierende Werte

Ohne explizite Werte inkrementieren Enums automatisch von 0:

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// Kann explizite und Auto-Werte mischen
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### Enum-Verwendungsmuster

```hemlock
// Als Funktionsparameter
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Dringend!");
    }
}

set_priority(Priority.HIGH);

// In Objekten
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Fehler beheben",
    priority: Priority.HIGH
};
```

## Spezielle Typen

### File-Typ

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

Repraesentiert ein offenes Datei-Handle.

### Task-Typ

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

Repraesentiert ein Async-Task-Handle.

### Channel-Typ

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

Repraesentiert einen Kommunikationskanal zwischen Tasks.

### Void-Typ

```hemlock
extern fn exit(code: i32): void;
```

Wird fuer Funktionen verwendet, die keinen Wert zurueckgeben (nur FFI).

## Typinferenz

### Ganzzahl-Literal-Inferenz

Hemlock leitet Ganzzahltypen basierend auf dem Wertebereich ab:

```hemlock
let a = 42;              // i32 (passt in 32-Bit)
let b = 5000000000;      // i64 (> i32 max)
let c = 128;             // i32
let d: u8 = 128;         // u8 (explizite Annotation)
```

**Regeln:**
- Werte im i32-Bereich (-2147483648 bis 2147483647): als `i32` abgeleitet
- Werte ausserhalb des i32-Bereichs aber innerhalb von i64: als `i64` abgeleitet
- Verwenden Sie explizite Annotationen fuer andere Typen (i8, i16, u8, u16, u32, u64)

### Float-Literal-Inferenz

```hemlock
let x = 3.14;        // f64 (Standard)
let y: f32 = 3.14;   // f32 (explizit)
```

### Wissenschaftliche Notation

Hemlock unterstuetzt wissenschaftliche Notation fuer numerische Literale:

```hemlock
let a = 1e10;        // 10000000000.0 (f64)
let b = 1e-12;       // 0.000000000001 (f64)
let c = 3.14e2;      // 314.0 (f64)
let d = 2.5e-3;      // 0.0025 (f64)
let e = 1E10;        // Gross-/Kleinschreibung egal
let f = 1e+5;        // Explizit positiver Exponent
```

**Hinweis:** Jedes Literal mit wissenschaftlicher Notation wird immer als `f64` abgeleitet.

### Andere Typinferenz

```hemlock
let s = "hallo";     // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## Typannotationen

### Variablenannotationen

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### Funktionsparameter-Annotationen

```hemlock
fn greet(name: string, age: i32) {
    print("Hallo, " + name + "!");
}
```

### Funktions-Rueckgabetyp-Annotationen

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Object-Typannotationen (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## Typueberpruefung

### Laufzeit-Typueberpruefung

Typannotationen werden zur **Laufzeit** geprueft, nicht zur Kompilierzeit:

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // Laufzeitfehler: Typenkonflikt

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "hallo");     // Laufzeitfehler: Typenkonflikt
```

### Typabfragen

Verwenden Sie `typeof()` um Werttypen zu pruefen:

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("hallo"));    // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## Typkonvertierungen

### Implizite Typbefoerderung

Beim Mischen von Typen in Operationen befördert Hemlock zum "hoeheren" Typ:

**Befoerderungshierarchie (niedrigste zu hoechste):**
```
i8 -> i16 -> i32 -> u32 -> i64 -> u64 -> f32 -> f64
      ^      ^      ^
     u8     u16
```

**Float gewinnt immer:**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result ist f64 (13.5)
```

**Groessere Groesse gewinnt:**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sum ist i64 (300)
```

**Praezisionserhaltung:** Beim Mischen von 64-Bit-Ganzzahlen mit f32 befördert Hemlock
zu f64, um Praezisionsverlust zu vermeiden (f32 hat nur 24-Bit-Mantisse, unzureichend fuer i64/u64):
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // result ist f64, nicht f32!
```

**Beispiele:**
```hemlock
u8 + i32  -> i32
i32 + i64 -> i64
u32 + u64 -> u64
i32 + f32 -> f32    // f32 ausreichend fuer i32
i64 + f32 -> f64    // f64 noetig um i64-Praezision zu erhalten
i64 + f64 -> f64
i8 + f64  -> f64
```

### Explizite Typkonvertierung

**Ganzzahl <-> Float:**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 -> f64 (42.0)

let x: f64 = 3.14;
let n: i32 = x;      // f64 -> i32 (3, abgeschnitten)
```

**Ganzzahl <-> Rune:**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 -> rune ('A')

let r: rune = 'Z';
let value: i32 = r;   // rune -> i32 (90)
```

**Rune -> String:**
```hemlock
let ch: rune = '(Rakete)';
let s: string = ch;   // rune -> string ("(Rakete)")
```

**u8 -> Rune:**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 -> rune ('A')
```

### Typ-Konstruktorfunktionen

Typnamen koennen als Funktionen verwendet werden, um Werte zu konvertieren oder zu parsen:

**Strings zu Zahlen parsen:**
```hemlock
let n = i32("42");       // String zu i32 parsen: 42
let f = f64("3.14159");  // String zu f64 parsen: 3.14159
let b = bool("true");    // String zu bool parsen: true

// Alle numerischen Typen unterstuetzt
let a = i8("-128");      // Zu i8 parsen
let c = u8("255");       // Zu u8 parsen
let d = i16("1000");     // Zu i16 parsen
let e = u16("50000");    // Zu u16 parsen
let g = i64("9000000000000"); // Zu i64 parsen
let h = u64("18000000000000"); // Zu u64 parsen
let j = f32("1.5");      // Zu f32 parsen
```

**Hex und negative Zahlen:**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10 (binaer)
```

**Typ-Aliase funktionieren auch:**
```hemlock
let x = integer("100");  // Gleich wie i32("100")
let y = number("1.5");   // Gleich wie f64("1.5")
let z = byte("200");     // Gleich wie u8("200")
```

**Zwischen numerischen Typen konvertieren:**
```hemlock
let big = i64(42);           // i32 zu i64
let truncated = i32(3.99);   // f64 zu i32 (schneidet auf 3 ab)
let promoted = f64(100);     // i32 zu f64 (100.0)
let narrowed = i8(127);      // i32 zu i8
```

**Typannotationen fuehren numerische Koersion durch (aber KEIN String-Parsen):**
```hemlock
let f: f64 = 100;        // i32 zu f64 via Annotation (OK)
let s: string = 'A';     // Rune zu String via Annotation (OK)
let code: i32 = 'A';     // Rune zu i32 via Annotation (erhaelt Codepoint, OK)

// String-Parsen erfordert explizite Typ-Konstruktoren:
let n = i32("42");       // Typ-Konstruktor fuer String-Parsen verwenden
// let x: i32 = "42";    // FEHLER - Typannotationen parsen keine Strings
```

**Fehlerbehandlung:**
```hemlock
// Ungueltige Strings werfen Fehler bei Verwendung von Typ-Konstruktoren
let bad = i32("hallo");  // Laufzeitfehler: kann "hallo" nicht als i32 parsen
let overflow = u8("256"); // Laufzeitfehler: 256 ausserhalb des Bereichs fuer u8
```

**Boolean-Parsen:**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("ja");    // Laufzeitfehler: muss "true" oder "false" sein
```

## Bereichspruefung

Typannotationen erzwingen Bereichspruefungen bei Zuweisung:

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // FEHLER: ausserhalb des Bereichs fuer u8

let a: i8 = 127;    // OK
let b: i8 = 128;    // FEHLER: ausserhalb des Bereichs fuer i8

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // FEHLER: u64 kann nicht negativ sein
```

## Typbefoerderungs-Beispiele

### Gemischte Ganzzahltypen

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32 (30)

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32 (300)
```

### Ganzzahl + Float

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32 (12.5)
```

### Komplexe Ausdruecke

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64 (70.0)
// Auswertung: b * c -> f64(60.0)
//             a + f64(60.0) -> f64(70.0)
```

## Duck Typing (Objects)

Objects verwenden **strukturelle Typisierung** (Duck Typing):

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Hat alle erforderlichen Felder
let p1: Person = { name: "Alice", age: 30 };

// OK: Zusaetzliche Felder erlaubt
let p2: Person = { name: "Bob", age: 25, city: "NYC" };

// FEHLER: Fehlendes 'age'-Feld
let p3: Person = { name: "Carol" };

// FEHLER: Falscher Typ fuer 'age'
let p4: Person = { name: "Dave", age: "dreissig" };
```

**Typueberpruefung erfolgt bei Zuweisung:**
- Validiert, dass alle erforderlichen Felder vorhanden sind
- Validiert, dass Feldtypen uebereinstimmen
- Zusaetzliche Felder sind erlaubt und werden beibehalten
- Setzt den Typnamen des Objects fuer `typeof()`

## Optionale Felder

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // Optional mit Standard
    timeout?: i32,     // Optional, Standard ist null
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false (Standard)
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true (ueberschrieben)
```

## Typ-Aliase

Hemlock unterstuetzt benutzerdefinierte Typ-Aliase mit dem `type`-Schluesselwort:

### Einfache Typ-Aliase

```hemlock
// Einfacher Typ-Alias
type Integer = i32;
type Text = string;

// Alias verwenden
let x: Integer = 42;
let msg: Text = "hallo";
```

### Funktionstyp-Aliase

```hemlock
// Funktionstyp-Alias
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Funktionstyp-Aliase verwenden
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### Zusammengesetzte Typ-Aliase

```hemlock
// Mehrere defines zu einem Typ kombinieren
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### Generische Typ-Aliase

```hemlock
// Generischer Typ-Alias
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Generische Aliase verwenden
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Hinweis:** Typ-Aliase sind transparent - `typeof()` gibt den zugrunde liegenden Typnamen zurueck, nicht den Alias.

## Typsystem-Einschraenkungen

Aktuelle Einschraenkungen:

- **Keine Generics bei Funktionen** - Funktions-Typparameter noch nicht unterstuetzt
- **Keine Union-Typen** - Kann "A oder B" nicht ausdruecken
- **Keine Nullable-Typen** - Alle Typen koennen null sein (verwenden Sie `?`-Suffix fuer explizite Nullability)

**Hinweis:** Der Compiler (`hemlockc`) bietet Kompilierzeit-Typueberpruefung. Der Interpreter fuehrt nur Laufzeit-Typueberpruefung durch. Siehe die [Compiler-Dokumentation](../design/implementation.md) fuer Details.

## Best Practices

### Wann Typannotationen verwenden

**Verwenden Sie Annotationen, wenn:**
- Praeziser Typ wichtig ist (z.B. `u8` fuer Byte-Werte)
- Funktionsschnittstellen dokumentieren
- Einschraenkungen erzwingen (z.B. Bereichspruefungen)

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // Implementierung
}
```

**Verwenden Sie keine Annotationen, wenn:**
- Der Typ aus dem Literal offensichtlich ist
- Interne Implementierungsdetails
- Unnoetige Zeremonie

```hemlock
// Unnoetig
let x: i32 = 42;

// Besser
let x = 42;
```

### Typsicherheits-Muster

**Vor Verwendung pruefen:**
```hemlock
if (typeof(value) == "i32") {
    // Sicher als i32 zu verwenden
}
```

**Funktionsargumente validieren:**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "Argumente muessen Ganzzahlen sein";
    }
    if (b == 0) {
        throw "Division durch Null";
    }
    return a / b;
}
```

**Duck Typing fuer Flexibilitaet verwenden:**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## Naechste Schritte

- [Strings](strings.md) - UTF-8-String-Typ und Operationen
- [Runes](runes.md) - Unicode-Codepoint-Typ
- [Arrays](arrays.md) - Dynamischer Array-Typ
- [Objects](objects.md) - Object-Literale und Duck Typing
- [Memory](memory.md) - Pointer- und Buffer-Typen
