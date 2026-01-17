# Typsystem-Referenz

Vollstaendige Referenz fuer Hemlocks Typsystem, einschliesslich aller primitiven und zusammengesetzten Typen.

---

## Uebersicht

Hemlock verwendet ein **dynamisches Typsystem** mit Laufzeit-Typ-Tags und optionalen Typannotationen. Jeder Wert hat einen Laufzeittyp, und Typkonvertierungen folgen expliziten Promovierungsregeln.

**Hauptmerkmale:**
- Laufzeit-Typprüfung (Interpreter)
- Kompilierzeit-Typprüfung (hemlockc - standardmaessig aktiviert)
- Optionale Typannotationen
- Automatische Typinferenz fuer Literale
- Explizite Typpromovierungsregeln
- Keine impliziten Konvertierungen die Praezision verlieren

---

## Kompilierzeit-Typprüfung (hemlockc)

Der Hemlock-Compiler (`hemlockc`) enthaelt einen Kompilierzeit-Typchecker der Ihren Code vor der Generierung von ausfuehrbaren Dateien validiert. Dies erkennt Typfehler frueh ohne das Programm ausfuehren zu muessen.

### Standardverhalten

Typprüfung ist in hemlockc **standardmaessig aktiviert**:

```bash
# Typprüfung erfolgt automatisch
hemlockc program.hml -o program

# Fehler werden vor Kompilierung gemeldet
hemlockc bad_types.hml
# Ausgabe: 1 Typfehler gefunden
```

### Compiler-Flags

| Flag | Beschreibung |
|------|--------------|
| `--check` | Nur Typen pruefen, nicht kompilieren (nach Validierung beenden) |
| `--no-type-check` | Typprüfung deaktivieren (nicht empfohlen) |
| `--strict-types` | Strengere Typwarnungen aktivieren |

**Beispiele:**

```bash
# Nur Typen validieren ohne zu kompilieren
hemlockc --check program.hml
# Ausgabe: program.hml: keine Typfehler

# Typprüfung deaktivieren (mit Vorsicht verwenden)
hemlockc --no-type-check dynamic_code.hml -o program

# Strenge Warnungen fuer implizite any-Typen aktivieren
hemlockc --strict-types program.hml -o program
```

### Was der Typchecker validiert

1. **Typannotationen** - Stellt sicher dass zugewiesene Werte deklarierten Typen entsprechen
2. **Funktionsaufrufe** - Validiert Argumenttypen gegen Parametertypen
3. **Rueckgabetypen** - Prueft ob return-Anweisungen deklariertem Rueckgabetyp entsprechen
4. **Operatorverwendung** - Verifiziert dass Operanden kompatibel sind
5. **Eigenschaftszugriff** - Validiert Objektfeldtypen fuer typisierte Objekte

### Tolerante numerische Konvertierungen

Der Typchecker erlaubt numerische Typkonvertierungen zur Kompilierzeit, mit Bereichsvalidierung zur Laufzeit:

```hemlock
let x: i8 = 100;      // OK - 100 passt in i8 (zur Laufzeit validiert)
let y: u8 = 255;      // OK - innerhalb u8-Bereich
let z: f64 = 42;      // OK - i32 zu f64 ist sicher
```

### Dynamischer Code-Support

Code ohne Typannotationen wird als dynamisch (`any`-Typ) behandelt und besteht immer den Typchecker:

```hemlock
let x = get_value();  // Dynamisch - keine Annotation
process(x);           // OK - dynamische Werte ueberall akzeptiert
```

---

## Primitive Typen

### Numerische Typen

#### Vorzeichenbehaftete Ganzzahlen

| Typ    | Groesse  | Bereich                                     | Alias     |
|--------|----------|---------------------------------------------|-----------|
| `i8`   | 1 Byte   | -128 bis 127                                | -         |
| `i16`  | 2 Bytes  | -32.768 bis 32.767                          | -         |
| `i32`  | 4 Bytes  | -2.147.483.648 bis 2.147.483.647            | `integer` |
| `i64`  | 8 Bytes  | -9.223.372.036.854.775.808 bis 9.223.372.036.854.775.807 | - |

**Beispiele:**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Typ-Alias
let x: integer = 42;  // Gleich wie i32
```

#### Vorzeichenlose Ganzzahlen

| Typ    | Groesse  | Bereich                          | Alias  |
|--------|----------|----------------------------------|--------|
| `u8`   | 1 Byte   | 0 bis 255                        | `byte` |
| `u16`  | 2 Bytes  | 0 bis 65.535                     | -      |
| `u32`  | 4 Bytes  | 0 bis 4.294.967.295              | -      |
| `u64`  | 8 Bytes  | 0 bis 18.446.744.073.709.551.615 | -      |

**Beispiele:**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Typ-Alias
let byte_val: byte = 65;  // Gleich wie u8
```

#### Gleitkomma

| Typ    | Groesse  | Praezision     | Alias    |
|--------|----------|----------------|----------|
| `f32`  | 4 Bytes  | ~7 Stellen     | -        |
| `f64`  | 8 Bytes  | ~15 Stellen    | `number` |

**Beispiele:**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// Typ-Alias
let x: number = 2.718;  // Gleich wie f64
```

---

### Ganzzahl-Literal-Inferenz

Ganzzahl-Literale werden automatisch basierend auf ihrem Wert typisiert:

**Regeln:**
- Werte im i32-Bereich (-2.147.483.648 bis 2.147.483.647): als `i32` inferiert
- Werte ausserhalb i32-Bereich aber innerhalb i64-Bereich: als `i64` inferiert
- Verwenden Sie explizite Typannotationen fuer andere Typen (i8, i16, u8, u16, u32, u64)

**Beispiele:**
```hemlock
let small = 42;                    // i32 (passt in i32)
let large = 5000000000;            // i64 (> i32 max)
let max_i64 = 9223372036854775807; // i64 (INT64_MAX)
let explicit: u32 = 100;           // u32 (Typannotation ueberschreibt)
```

---

### Boolean-Typ

**Typ:** `bool`

**Werte:** `true`, `false`

**Groesse:** 1 Byte (intern)

**Beispiele:**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("arbeite");
}
```

---

### Zeichen-Typen

#### Rune

**Typ:** `rune`

**Beschreibung:** Unicode-Codepoint (U+0000 bis U+10FFFF)

**Groesse:** 4 Bytes (32-Bit-Wert)

**Bereich:** 0 bis 0x10FFFF (1.114.111)

**Literal-Syntax:** Einfache Anfuehrungszeichen `'x'`

**Beispiele:**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// Mehrbyte-UTF-8
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// Escape-Sequenzen
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Unicode-Escapes
let emoji = '\u{1F680}';   // Bis zu 6 Hex-Ziffern
let max = '\u{10FFFF}';    // Maximaler Codepoint
```

**Typkonvertierungen:**
```hemlock
// Ganzzahl zu Rune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// Rune zu Ganzzahl
let value: i32 = 'Z';       // 90

// Rune zu String
let s: string = 'H';        // "H"

// u8 zu Rune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**Siehe auch:** [String-API](string-api.md) fuer String + Rune Verkettung

---

### String-Typ

**Typ:** `string`

**Beschreibung:** UTF-8-kodierter, veraenderbarer, heap-allokierter Text

**Kodierung:** UTF-8 (U+0000 bis U+10FFFF)

**Veraenderbarkeit:** Veraenderbar (anders als in den meisten Sprachen)

**Eigenschaften:**
- `.length` - Codepoint-Anzahl (Anzahl der Zeichen)
- `.byte_length` - Byte-Anzahl (UTF-8-Kodierungsgroesse)

**Literal-Syntax:** Doppelte Anfuehrungszeichen `"text"`

**Beispiele:**
```hemlock
let s = "hello";
s[0] = 'H';             // Aendern (jetzt "Hello")
print(s.length);        // 5 (Codepoint-Anzahl)
print(s.byte_length);   // 5 (UTF-8-Bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (ein Codepoint)
print(emoji.byte_length);   // 4 (vier UTF-8-Bytes)
```

**Indizierung:**
```hemlock
let s = "hello";
let ch = s[0];          // Gibt Rune 'h' zurueck
s[0] = 'H';             // Mit Rune setzen
```

**Siehe auch:** [String-API](string-api.md) fuer vollstaendige Methodenreferenz

---

### Null-Typ

**Typ:** `null`

**Beschreibung:** Der Null-Wert (Abwesenheit eines Wertes)

**Groesse:** 8 Bytes (intern)

**Wert:** `null`

**Beispiele:**
```hemlock
let x = null;
let y: i32 = null;  // FEHLER: Typfehlanpassung

if (x == null) {
    print("x ist null");
}
```

---

## Zusammengesetzte Typen

### Array-Typ

**Typ:** `array`

**Beschreibung:** Dynamisches, heap-allokiertes Array mit gemischten Typen

**Eigenschaften:**
- `.length` - Anzahl der Elemente

**Nullbasiert:** Ja

**Literal-Syntax:** `[elem1, elem2, ...]`

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Gemischte Typen
let mixed = [1, "hello", true, null];
```

**Siehe auch:** [Array-API](array-api.md) fuer vollstaendige Methodenreferenz

---

### Objekt-Typ

**Typ:** `object`

**Beschreibung:** JavaScript-aehnliches Objekt mit dynamischen Feldern

**Literal-Syntax:** `{ field: value, ... }`

**Beispiele:**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// Feld dynamisch hinzufuegen
person.email = "alice@example.com";
```

**Typdefinitionen:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // Optionales Feld
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### Pointer-Typen

#### Roh-Pointer (ptr)

**Typ:** `ptr`

**Beschreibung:** Rohe Speicheradresse (unsicher)

**Groesse:** 8 Bytes

**Grenzenprüfung:** Keine

**Beispiele:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### Buffer (buffer)

**Typ:** `buffer`

**Beschreibung:** Sicherer Pointer-Wrapper mit Grenzenprüfung

**Struktur:** Pointer + Laenge + Kapazitaet

**Eigenschaften:**
- `.length` - Buffergroesse
- `.capacity` - Allokierte Kapazitaet

**Beispiele:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Grenzenprüfung
print(b.length);        // 64
free(b);
```

**Siehe auch:** [Speicher-API](memory-api.md) fuer Allokationsfunktionen

---

## Spezielle Typen

### Datei-Typ

**Typ:** `file`

**Beschreibung:** Dateihandle fuer I/O-Operationen

**Eigenschaften:**
- `.path` - Dateipfad (string)
- `.mode` - Oeffnungsmodus (string)
- `.closed` - Ob Datei geschlossen (bool)

**Siehe auch:** [Datei-API](file-api.md)

---

### Task-Typ

**Typ:** `task`

**Beschreibung:** Handle fuer nebenlaeufigen Task

**Siehe auch:** [Nebenlaeufigkeits-API](concurrency-api.md)

---

### Kanal-Typ

**Typ:** `channel`

**Beschreibung:** Thread-sicherer Kommunikationskanal

**Siehe auch:** [Nebenlaeufigkeits-API](concurrency-api.md)

---

### Funktions-Typ

**Typ:** `function`

**Beschreibung:** First-Class-Funktionswert

**Beispiele:**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Void-Typ

**Typ:** `void`

**Beschreibung:** Abwesenheit eines Rueckgabewertes (interne Verwendung)

---

## Typpromovierungsregeln

Beim Mischen von Typen in Operationen promoviert Hemlock zum "hoeheren" Typ:

**Promovierungshierarchie:**
```
f64 (hoechste Praezision)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (niedrigste)
```

**Regeln:**
1. Float gewinnt immer ueber Ganzzahl
2. Groessere Groesse gewinnt innerhalb gleicher Kategorie (int/uint/float)
3. Beide Operanden werden zum Ergebnistyp promoviert
4. **Praezisionserhaltung:** i64/u64 + f32 promoviert zu f64 (nicht f32)

**Beispiele:**
```hemlock
// Groessenpromovierung
u8 + i32    → i32    // Groessere Groesse gewinnt
i32 + i64   → i64    // Groessere Groesse gewinnt
u32 + u64   → u64    // Groessere Groesse gewinnt

// Float-Promovierung
i32 + f32   → f32    // Float gewinnt, f32 ausreichend fuer i32
i64 + f32   → f64    // Promoviert zu f64 um i64-Praezision zu erhalten
i64 + f64   → f64    // Float gewinnt immer
i8 + f64    → f64    // Float + groesster gewinnt
```

**Warum i64 + f32 → f64?**

f32 hat nur eine 24-Bit-Mantisse, die Ganzzahlen groesser als 2^24 (16.777.216) nicht praezise darstellen kann. Da i64 Werte bis 2^63 halten kann, wuerde das Mischen von i64 mit f32 schweren Praezisionsverlust verursachen. Hemlock promoviert stattdessen zu f64 (53-Bit-Mantisse).

---

## Bereichsprüfung

Typannotationen erzwingen Bereichsprüfungen bei Zuweisung:

**Gueltige Zuweisungen:**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**Ungueltige Zuweisungen (Laufzeitfehler):**
```hemlock
let x: u8 = 256;             // FEHLER: ausserhalb des Bereichs
let y: i8 = 128;             // FEHLER: max ist 127
let z: u64 = -1;             // FEHLER: u64 kann nicht negativ sein
```

---

## Typ-Introspektion

### typeof(value)

Gibt den Typnamen als String zurueck.

**Signatur:**
```hemlock
typeof(value: any): string
```

**Rueckgabe:**
- Primitive Typen: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Zusammengesetzte Typen: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Spezielle Typen: `"file"`, `"task"`, `"channel"`
- Typisierte Objekte: Benutzerdefinierter Typname (z.B. `"Person"`)

**Beispiele:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**Siehe auch:** [Eingebaute Funktionen](builtins.md#typeof)

---

## Typkonvertierungen

### Implizite Konvertierungen

Hemlock fuehrt implizite Typkonvertierungen in arithmetischen Operationen nach den Typpromovierungsregeln durch.

**Beispiele:**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // result ist i32 (promoviert)
```

### Explizite Konvertierungen

Verwenden Sie Typannotationen fuer explizite Konvertierungen:

**Beispiele:**
```hemlock
// Ganzzahl zu Float
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Float zu Ganzzahl (trunciert)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Ganzzahl zu Rune
let code: rune = 65;    // 'A'

// Rune zu Ganzzahl
let value: i32 = 'Z';   // 90

// Rune zu String
let s: string = 'H';    // "H"
```

---

## Typ-Aliase

### Eingebaute Aliase

Hemlock bietet eingebaute Typ-Aliase fuer haeufige Typen:

| Alias     | Tatsaechlicher Typ | Verwendung                 |
|-----------|-------------------|----------------------------|
| `integer` | `i32`             | Allzweck-Ganzzahlen        |
| `number`  | `f64`             | Allzweck-Gleitkomma        |
| `byte`    | `u8`              | Byte-Werte                 |

**Beispiele:**
```hemlock
let count: integer = 100;       // Gleich wie i32
let price: number = 19.99;      // Gleich wie f64
let b: byte = 255;              // Gleich wie u8
```

### Benutzerdefinierte Typ-Aliase

Definieren Sie benutzerdefinierte Typ-Aliase mit dem `type`-Schluesselwort:

```hemlock
// Einfache Aliase
type Integer = i32;
type Text = string;

// Funktionstyp-Aliase
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// Zusammengesetzte Typ-Aliase
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Generische Typ-Aliase
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**Benutzerdefinierte Aliase verwenden:**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Hinweis:** Typ-Aliase sind transparent - `typeof()` gibt den zugrundeliegenden Typnamen zurueck.

---

## Funktionstypen

Funktionstypen spezifizieren die Signatur von Funktionswerten:

### Syntax

```hemlock
fn(param_types): return_type
```

### Beispiele

```hemlock
// Grundlegender Funktionstyp
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Funktionsparameter
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Higher-Order-Funktion die Funktion zurueckgibt
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Async-Funktionstyp
fn run_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## Zusammengesetzte Typen (Schnittmenge)

Zusammengesetzte Typen verwenden `&` um mehrere Typanforderungen zu verlangen:

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Objekt muss alle Typen erfuellen
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Drei oder mehr Typen
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## Zusammenfassungstabelle

| Typ        | Groesse   | Veraenderbar | Heap-allokiert | Beschreibung                   |
|------------|-----------|--------------|----------------|--------------------------------|
| `i8`-`i64` | 1-8 Bytes | Nein         | Nein           | Vorzeichenbehaftete Ganzzahlen |
| `u8`-`u64` | 1-8 Bytes | Nein         | Nein           | Vorzeichenlose Ganzzahlen      |
| `f32`      | 4 Bytes   | Nein         | Nein           | Einfach-Praezisions-Float      |
| `f64`      | 8 Bytes   | Nein         | Nein           | Doppel-Praezisions-Float       |
| `bool`     | 1 Byte    | Nein         | Nein           | Boolean                        |
| `rune`     | 4 Bytes   | Nein         | Nein           | Unicode-Codepoint              |
| `string`   | Variabel  | Ja           | Ja             | UTF-8-Text                     |
| `array`    | Variabel  | Ja           | Ja             | Dynamisches Array              |
| `object`   | Variabel  | Ja           | Ja             | Dynamisches Objekt             |
| `ptr`      | 8 Bytes   | Nein         | Nein           | Roh-Pointer                    |
| `buffer`   | Variabel  | Ja           | Ja             | Sicherer Pointer-Wrapper       |
| `file`     | Opak      | Ja           | Ja             | Dateihandle                    |
| `task`     | Opak      | Nein         | Ja             | Nebenlaeufiger Task-Handle     |
| `channel`  | Opak      | Ja           | Ja             | Thread-sicherer Kanal          |
| `function` | Opak      | Nein         | Ja             | Funktionswert                  |
| `null`     | 8 Bytes   | Nein         | Nein           | Null-Wert                      |

---

## Siehe auch

- [Operatoren-Referenz](operators.md) - Typverhalten in Operationen
- [Eingebaute Funktionen](builtins.md) - Typ-Introspektion und Konvertierung
- [String-API](string-api.md) - String-Typ-Methoden
- [Array-API](array-api.md) - Array-Typ-Methoden
- [Speicher-API](memory-api.md) - Pointer- und Buffer-Operationen
