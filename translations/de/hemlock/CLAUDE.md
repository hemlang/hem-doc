# Hemlock Sprachdesign-Philosophie

> "Eine kleine, unsichere Sprache, um unsichere Dinge sicher zu schreiben."

Dieses Dokument erfasst die grundlegenden Designprinzipien für KI-Assistenten, die mit Hemlock arbeiten.
Für detaillierte Dokumentation siehe `docs/README.md` und das `stdlib/docs/`-Verzeichnis.

---

## Kernidentität

Hemlock ist eine **System-Skriptsprache** mit manueller Speicherverwaltung und expliziter Kontrolle:
- Die Macht von C mit modernen Skripting-Ergonomien
- Strukturierte async Nebenläufigkeit integriert
- Kein verstecktes Verhalten oder Magie

**Hemlock ist NICHT:** Speichersicher, eine GC-Sprache oder versteckt Komplexität.
**Hemlock IST:** Explizit statt implizit, lehrreich, eine "C-Skriptschicht" für Systemarbeit.

---

## Designprinzipien

### 1. Explizit statt Implizit
- Semikolons obligatorisch (kein ASI)
- Manuelle Speicherverwaltung (alloc/free)
- Typannotationen optional, aber zur Laufzeit geprüft

### 2. Dynamisch standardmäßig, typisiert nach Wahl
- Jeder Wert hat ein Laufzeit-Typ-Tag
- Literale inferieren Typen: `42` → i32, `5000000000` → i64, `3.14` → f64
- Optionale Typannotationen erzwingen Laufzeitprüfungen

### 3. Unsicher ist ein Feature
- Zeigerarithmetik erlaubt (Verantwortung des Benutzers)
- Keine Grenzprüfung bei rohem `ptr` (verwende `buffer` für Sicherheit)
- Double-Free-Abstürze erlaubt

### 4. Strukturierte Nebenläufigkeit erstklassig
- `async`/`await` eingebaut mit pthread-basierter Parallelität
- Kanäle für Kommunikation
- `spawn`/`join`/`detach` für Aufgabenverwaltung

### 5. C-ähnliche Syntax
- `{}` Blöcke immer erforderlich
- Kommentare: `// Zeile` und `/* Block */`
- Operatoren entsprechen C: `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Inkrement/Dekrement: `++x`, `x++`, `--x`, `x--` (Präfix und Postfix)
- Zusammengesetzte Zuweisung: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` gibt immer Float zurück (verwende `divi()` aus `@stdlib/math` für Integer-Division)
- Typsyntax: `let x: type = value;`

---

## Kurzreferenz

### Typen
```
Vorzeichenbehaftet: i8, i16, i32, i64
Vorzeichenlos:      u8, u16, u32, u64
Fließkomma:        f32, f64
Andere:             bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Aliase:             integer (i32), number (f64), byte (u8)
```

**Typ-Promotion:** i8 → u8 → i16 → u16 → i32 → u32 → i64 → u64 → f32 → f64 (Fließkomma gewinnt immer, aber i64/u64 + f32 → f64 um Präzision zu erhalten)

### Literale
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> i32 max)
let hex = 0xDEADBEEF;    // Hex-Literal
let bin = 0b1010;        // Binär-Literal
let oct = 0o777;         // Oktal-Literal
let sep = 1_000_000;     // Numerische Trennzeichen erlaubt
let pi = 3.14;           // f64
let half = .5;           // f64 (keine führende Null)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // Hex- und Unicode-Escapes
let ch = 'A';            // rune
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Typkonvertierung
```hemlock
// Typkonstruktorfunktionen - String zu Typ parsen
let n = i32("42");       // String zu i32 parsen
let f = f64("3.14");     // String zu f64 parsen
let b = bool("true");    // String zu bool parsen ("true" oder "false")

// Alle numerischen Typen unterstützt
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// Hex und negative Zahlen
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// Typaliase funktionieren auch
let x = integer("100");  // Gleich wie i32("100")
let y = number("1.5");   // Gleich wie f64("1.5")
let z = byte("200");     // Gleich wie u8("200")

// Zwischen numerischen Typen konvertieren
let big = i64(42);       // i32 zu i64
let truncated = i32(3.99); // f64 zu i32 (schneidet auf 3 ab)

// Typannotationen validieren Typen (aber parsen keine Strings)
let f: f64 = 100;        // i32 zu f64 via Annotation (numerische Umwandlung OK)
// let n: i32 = "42";    // FEHLER - verwende i32("42") für String-Parsing
```

### Introspektion
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
"hello".length;          // 5 (Rune-Anzahl)
"hello".byte_length;     // 5 (Byte-Anzahl)

// typeid() - schnelle ganzzahlige Typerkennung (keine String-Allokation)
typeid(42);              // 2 (TYPEID_I32)
if (typeid(val) == TYPEID_I32 || typeid(val) == TYPEID_I64) { ... }
```

**TYPEID-Konstanten:** `TYPEID_I8` (0), `TYPEID_I16` (1), `TYPEID_I32` (2), `TYPEID_I64` (3), `TYPEID_U8` (4), `TYPEID_U16` (5), `TYPEID_U32` (6), `TYPEID_U64` (7), `TYPEID_F32` (8), `TYPEID_F64` (9), `TYPEID_BOOL` (10), `TYPEID_STRING` (11), `TYPEID_RUNE` (12), `TYPEID_PTR` (13), `TYPEID_BUFFER` (14), `TYPEID_ARRAY` (15), `TYPEID_OBJECT` (16), `TYPEID_FILE` (17), `TYPEID_FUNCTION` (18), `TYPEID_TASK` (19), `TYPEID_CHANNEL` (20), `TYPEID_NULL` (21)

### Speicher
```hemlock
let p = alloc(64);       // roher Zeiger
let b = buffer(64);      // sicherer Buffer (grenzgeprüft)
memset(p, 0, 64); memcpy(dest, src, 64);
free(p);                 // manuelle Bereinigung erforderlich
let view = b.slice(0, 16);  // Zero-Copy Buffer-View
ptr_write_f32(b, 3.14);     // ptr_read/write akzeptieren Buffer direkt
```

### Kontrollfluss
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // Endlosschleife (sauberer als while(true))
switch (x) { case 1: break; default: break; }  // C-artiges Fall-Through
defer cleanup();         // läuft wenn Funktion zurückkehrt

// Schleifenlabels für gezieltes break/continue in verschachtelten Schleifen
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // äußere Schleife beenden
        if (i == 3) { continue outer; }  // äußere Schleife fortsetzen
    }
}
```

### Musterabgleich
```hemlock
// Match-Ausdruck - gibt Wert zurück
let result = match (value) {
    0 => "null",                        // Literal-Muster
    1 | 2 | 3 => "klein",               // ODER-Muster
    n if n < 10 => "mittel",            // Guard-Ausdruck
    n => "groß: " + n                  // Variablenbindung
};

// Typmuster
match (val) {
    n: i32 => "ganzzahl",
    s: string => "zeichenkette",
    _ => "anderes"                      // Platzhalter
}

// Objekt-Destrukturierung
match (point) {
    { x: 0, y: 0 } => "ursprung",
    { x, y } => "bei " + x + "," + y
}

// Array-Destrukturierung mit Rest
match (arr) {
    [] => "leer",
    [first, ...rest] => "kopf: " + first,
    _ => "anderes"
}

// Verschachtelte Muster
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

Siehe `docs/language-guide/pattern-matching.md` für vollständige Dokumentation.

### Null-Koaleszenz-Operatoren
```hemlock
// Null-Koaleszenz (??) - gibt links zurück wenn nicht-null, sonst rechts
let name = user.name ?? "Anonym";
let first = a ?? b ?? c ?? "fallback";

// Null-Koaleszenz-Zuweisung (??=) - weist nur zu wenn null
let config = null;
config ??= { timeout: 30 };    // config ist jetzt { timeout: 30 }
config ??= { timeout: 60 };    // config unverändert (nicht null)

// Funktioniert mit Eigenschaften und Indizes
obj.field ??= "standard";
arr[0] ??= "erstes";

// Sichere Navigation (?.) - gibt null zurück wenn Objekt null ist
let city = user?.address?.city;  // null wenn irgendein Teil null ist
let upper = name?.to_upper();    // sicherer Methodenaufruf
let item = arr?.[0];             // sichere Indizierung
```

### Funktionen
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hallo") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonym/Closure

// Ausdruckskörper-Funktionen (Pfeilsyntax)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // anonyme Ausdruckskörper

// Parametermodifikatoren
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // Übergabe per Referenz
fn print_all(const items: array) { for (i in items) { print(i); } }  // unveränderlich
```

### Benannte Argumente
```hemlock
// Funktionen können mit benannten Argumenten aufgerufen werden
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " ist " + age + " Jahre alt");
}

// Positionelle Argumente (traditionell)
create_user("Alice", 25, false);

// Benannte Argumente - können in beliebiger Reihenfolge sein
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Optionale Parameter durch Benennung überspringen
create_user("David", active: false);  // Verwendet Standard age=18

// Benannte Argumente müssen nach positionellen kommen
create_user("Eve", age: 21);          // OK: positionell dann benannt
// create_user(name: "Bad", 25);      // FEHLER: positionell nach benannt
```

**Regeln:**
- Benannte Argumente verwenden `name: value` Syntax
- Können in beliebiger Reihenfolge nach positionellen Argumenten erscheinen
- Positionelle Argumente können nicht nach benannten Argumenten folgen
- Funktioniert mit Standard-/optionalen Parametern
- Unbekannte Parameternamen verursachen Laufzeitfehler

### Objekte & Enums
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// Objekt-Kurzschreibweise (ES6-Stil)
let name = "Alice";
let age = 30;
let person = { name, age };         // äquivalent zu { name: name, age: age }

// Objekt-Spread-Operator
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // kopiert defaults, überschreibt size

// Klammernotation mit Schlüssel-Koersion (Nicht-String-Schlüssel werden automatisch zu String)
let map = {};
map[42] = "wert";              // Integer-Schlüssel -> "42"
map[true] = "ja";              // Bool-Schlüssel -> "true"
map['A'] = "alpha";            // Rune-Schlüssel -> "A"
print(map[42]);                // "wert"
print(map.has(42));            // true
map.delete(42);                // entfernt Feld "42"
let keys = map.keys();         // gibt Array von String-Schlüsseln zurück

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Zusammengesetzte Typen (Schnittmengen-/Duck-Typen)
```hemlock
// Strukturelle Typen definieren
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Zusammengesetzter Typ: Objekt muss ALLE Typen erfüllen
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Funktionsparameter mit zusammengesetzten Typen
fn greet(p: HasName & HasAge) {
    print(p.name + " ist " + p.age);
}

// Drei oder mehr Typen
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Zusätzliche Felder erlaubt (Duck-Typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - zusätzliche Felder ignoriert
};
```

Zusammengesetzte Typen bieten Interface-ähnliches Verhalten ohne separates `interface`-Schlüsselwort,
aufbauend auf den bestehenden `define`- und Duck-Typing-Paradigmen.

### Typaliase
```hemlock
// Einfacher Typalias
type Integer = i32;
type Text = string;

// Funktionstyp-Alias
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Zusammengesetzter Typalias (grossartig für wiederverwendbare Interfaces)
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Generischer Typalias
type Pair<T> = { first: T, second: T };

// Typaliase verwenden
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

Typaliase erstellen benannte Abkürzungen für komplexe Typen und verbessern Lesbarkeit und Wartbarkeit.

### Funktionstypen
```hemlock
// Funktionstyp-Annotationen für Parameter
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Höhere Funktion die eine Funktion zurückgibt
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Async-Funktionstypen
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// Funktionstypen mit mehreren Parametern
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Const-Parameter
```hemlock
// Const-Parameter - tiefe Unveränderlichkeit
fn print_all(const items: array) {
    // items.push(4);  // FEHLER: kann const-Parameter nicht mutieren
    for (item in items) {
        print(item);
    }
}

// Const mit Objekten - keine Mutation über irgendeinen Pfad
fn describe(const person: object) {
    print(person.name);       // OK: Lesen ist erlaubt
    // person.name = "Bob";   // FEHLER: kann nicht mutieren
}

// Verschachtelter Zugriff ist zum Lesen erlaubt
fn get_city(const user: object) {
    return user.address.city;  // OK: verschachtelte Eigenschaften lesen
}
```

Der `const`-Modifikator verhindert jede Mutation des Parameters, einschließlich verschachtelter Eigenschaften.
Dies bietet Kompilierzeit-Sicherheit für Funktionen, die ihre Eingaben nicht modifizieren sollten.

### Ref-Parameter (Übergabe per Referenz)
```hemlock
// Ref-Parameter - Variable des Aufrufers wird direkt modifiziert
fn increment(ref x: i32) {
    x = x + 1;  // Modifiziert die ursprüngliche Variable
}

let count = 10;
increment(count);
print(count);  // 11 - Original wurde modifiziert

// Klassische Swap-Funktion
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// Ref und reguläre Parameter mischen
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

Der `ref`-Modifikator übergibt eine Referenz zur Variable des Aufrufers, sodass die Funktion
sie direkt modifizieren kann. Ohne `ref` werden Primitives per Wert übergeben (kopiert). Verwende `ref` wenn
du den Zustand des Aufrufers mutieren musst, ohne einen Wert zurückzugeben.

**Regeln:**
- `ref`-Parameter müssen Variablen übergeben werden, keine Literale oder Ausdrücke
- Funktioniert mit allen Typen (Primitives, Arrays, Objekte)
- Kombiniere mit Typannotationen: `ref x: i32`
- Kann nicht mit `const` kombiniert werden (sie sind Gegensätze)

### Methodensignaturen in Define
```hemlock
// Define mit Methodensignaturen (Interface-Muster)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Erforderliche Methodensignatur
}

// Objekte müssen die erforderliche Methode bereitstellen
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Optionale Methoden mit ?
define Serializable {
    fn serialize(): string,        // Erforderlich
    fn pretty?(): string           // Optionale Methode
}

// Self-Typ bezieht sich auf den definierenden Typ
define Cloneable {
    fn clone(): Self   // Gibt gleichen Typ wie das Objekt zurück
}
```

Methodensignaturen in `define`-Blöcken verwenden Komma-Trennzeichen (wie TypeScript-Interfaces),
etablieren Verträge, die Objekte erfüllen müssen, und ermöglichen Interface-artige Programmier-
muster mit Hemlocks Duck-Typing-System.

### Fehlerbehandlung
```hemlock
try { throw "fehler"; } catch (e) { print(e); } finally { cleanup(); }
panic("nicht behebbar");  // beendet sofort, nicht abfangbar
```

### Async/Nebenläufigkeit
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // oder join(task)
detach(spawn(background_work));
let t = spawn_with({ stack_size: 4194304, name: "worker" }, compute, 42);

let ch = channel(10);
ch.send(value); let val = ch.recv(); ch.close();
```

**Speicherbesitz:** Tasks erhalten Kopien von Primitivwerten, teilen aber Zeiger. Wenn du einen `ptr` an einen gespawnten Task übergibst, musst du sicherstellen, dass der Speicher gültig bleibt, bis der Task abgeschlossen ist. Verwende `join()` vor `free()`, oder verwende Kanäle, um Abschluss zu signalisieren.

### Benutzereingabe
```hemlock
let name = read_line();          // Zeile von stdin lesen (blockiert)
print("Hallo, " + name);
write("kein Zeilenumbruch");     // Ohne abschließenden Zeilenumbruch ausgeben
eprint("Fehlermeldung");         // Auf stderr ausgeben

// read_line() gibt null bei EOF zurück
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Erhalten:", line);
}
```

### Datei-I/O
```hemlock
let f = open("datei.txt", "r");  // Modi: r, w, a, r+, w+, a+
let content = f.read();
f.write("daten");
f.seek(0);
f.close();
```

### Signale
```hemlock
signal(SIGINT, fn(sig) { print("Unterbrochen"); });
raise(SIGUSR1);
```

---

## String-Methoden (22)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `trim_start`, `trim_end`,
`to_upper`, `to_lower`, `starts_with`, `ends_with`, `replace`, `replace_all`,
`repeat`, `char_at`, `byte_at`, `chars`, `bytes`, `to_bytes`, `byte_ptr`, `deserialize`

Template-Strings: `` `Hallo ${name}!` ``

**String-Mutabilität:** Strings sind per Indexzuweisung mutierbar (`s[0] = 'H'`), aber alle String-Methoden geben neue Strings zurück, ohne das Original zu modifizieren. Dies erlaubt In-Place-Mutation wenn nötig, während Methodenverkettung funktional bleibt.

**String-Längeneigenschaften:**
```hemlock
let s = "hallo 🚀";
print(s.length);       // 7 (Zeichen-/Rune-Anzahl)
print(s.byte_length);  // 10 (Byte-Anzahl - Emoji ist 4 Bytes UTF-8)
```

## Array-Methoden (28)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `findIndex`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`,
`every`, `some`, `indexOf`, `lastIndexOf`, `sort`, `fill`, `reserve`, `flat`, `serialize`

```hemlock
// every(predicate) - true wenn alle Elemente das Prädikat erfüllen
let allPositive = [1, 2, 3].every(fn(x) { return x > 0; });  // true

// some(predicate) - true wenn ein Element das Prädikat erfüllt
let hasEven = [1, 2, 3].some(fn(x) { return x % 2 == 0; });  // true

// indexOf(value) - findet ersten Index des Werts, oder -1
let idx = ["a", "b", "c"].indexOf("b");  // 1

// sort(comparator?) - sortiert in-place, optionaler Comparator
let nums = [3, 1, 4, 1, 5];
nums.sort();                              // [1, 1, 3, 4, 5]
nums.sort(fn(a, b) { return b - a; });    // absteigend

// fill(value, start?, end?) - füllt mit Wert
let arr = [1, 2, 3, 4, 5];
arr.fill(0);        // [0, 0, 0, 0, 0]
arr.fill(9, 2);     // [0, 0, 9, 9, 9]
arr.fill(7, 1, 4);  // [0, 7, 7, 7, 9]
```

Typisierte Arrays: `let nums: array<i32> = [1, 2, 3];`

---

## Standardbibliothek (53 Module)

Importieren mit `@stdlib/`-Präfix:
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| Modul | Beschreibung |
|-------|--------------|
| `arena` | Arena-Speicherallokator (Bump-Allocation) |
| `args` | Kommandozeilenargument-Parsing |
| `assert` | Assertions-Utilities |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Asynchrone Datei-I/O-Operationen |
| `atomic` | Atomare Operationen (load, store, add, CAS, fence) |
| `bytes` | Byte-Ordnungs-Utilities (bswap, hton/ntoh, Endian-aware I/O) |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | CSV-Parsing und -Generierung |
| `debug` | Task-Inspektion und Stack-Verwaltung |
| `datetime` | DateTime-Klasse, Formatierung, Parsing |
| `decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `ffi` | FFI-Callback-Verwaltung |
| `fmt` | String-Formatierungs-Utilities |
| `fs` | open, read_file, write_file, list_dir, exists |
| `glob` | Datei-Musterabgleich |
| `hash` | sha1, sha256, sha512, md5, djb2, crc32, adler32 |
| `http` | http_get, http_post, http_request |
| `ipc` | Inter-Prozess-Kommunikation |
| `iter` | Iterator-Utilities |
| `jinja` | Jinja2-kompatibles Template-Rendering |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger mit Stufen |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `matrix` | Dichte Matrixoperationen (add, multiply, transpose, determinant, inverse) |
| `mmap` | Memory-mapped Datei-I/O (mmap, munmap, msync) |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Dateipfad-Manipulation |
| `process` | fork, exec, wait, kill |
| `random` | Zufallszahlengenerierung |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Wiederholungslogik mit Backoff |
| `semver` | Semantische Versionierung |
| `shell` | Shell-Befehls-Utilities |
| `signal` | Signalkonstanten (SIGINT, SIGTERM, etc.) |
| `sqlite` | SQLite-Datenbank, query, exec, Transaktionen |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | ANSI-Farben und -Stile |
| `termios` | Rohe Terminal-Eingabe, Tastenerkennung |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | TOML-Parsing und -Generierung |
| `url` | URL-Parsing und -Manipulation |
| `unix_socket` | Unix-Domain-Sockets (AF_UNIX Stream/Datagramm) |
| `uuid` | UUID-Generierung |
| `vector` | Vektor-Ähnlichkeitssuche (USearch ANN) |
| `websocket` | WebSocket-Client |
| `yaml` | YAML-Parsing und -Generierung |

Siehe `stdlib/docs/` für detaillierte Moduldokumentation.

---

## FFI (Foreign Function Interface)

C-Funktionen aus Shared Libraries deklarieren und aufrufen:
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hallo!");  // 6
let pid = getpid();
```

FFI-Funktionen aus Modulen exportieren:
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

Dynamisches FFI (Laufzeit-Binding):
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hallo von C!");
ffi_close(lib);
```

Typen: `FFI_INT`, `FFI_DOUBLE`, `FFI_POINTER`, `FFI_STRING`, `FFI_VOID`, etc.

---

## Atomare Operationen

Lock-freie nebenläufige Programmierung mit atomaren Operationen:

```hemlock
// Speicher für atomares i32 allokieren
let p = alloc(4);
ptr_write_i32(p, 0);

// Atomares Laden/Speichern
let val = atomic_load_i32(p);        // Atomar lesen
atomic_store_i32(p, 42);             // Atomar schreiben

// Fetch-and-Modify-Operationen (geben ALTEN Wert zurück)
let old = atomic_add_i32(p, 10);     // Addieren, alten zurückgeben
old = atomic_sub_i32(p, 5);          // Subtrahieren, alten zurückgeben
old = atomic_and_i32(p, 0xFF);       // Bitweises UND
old = atomic_or_i32(p, 0x10);        // Bitweises ODER
old = atomic_xor_i32(p, 0x0F);       // Bitweises XOR

// Compare-and-Swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // Wenn *p == 42, auf 100 setzen
// Gibt true zurück wenn Swap erfolgreich, sonst false

// Atomarer Austausch
old = atomic_exchange_i32(p, 999);   // Tauschen, alten zurückgeben

free(p);

// i64-Varianten verfügbar (atomic_load_i64, atomic_add_i64, etc.)

// Speicherbarriere (vollständige Barriere)
atomic_fence();
```

Alle Operationen verwenden sequenzielle Konsistenz (`memory_order_seq_cst`).

---

## Projektstruktur

```
hemlock/
├── src/
│   ├── frontend/         # Gemeinsam: Lexer, Parser, AST, Module
│   ├── backends/
│   │   ├── interpreter/  # hemlock: Tree-Walking-Interpreter
│   │   └── compiler/     # hemlockc: C-Code-Generator
│   ├── modules/          # Native Modulimplementierungen
│   ├── runtime/          # Laufzeit-bezogener C-Code
│   ├── shared/           # Gemeinsame Utilities (Typ-Promotion, etc.)
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   ├── bundler/      # Bundle-/Paket-Tools
│   │   └── formatter/    # Code-Formatierer
├── runtime/              # Kompilierte Programm-Laufzeit (libhemlock_runtime.a)
├── stdlib/               # Standardbibliothek
│   └── docs/             # Moduldokumentation
├── include/              # C-Headerdateien (hemlock_limits.h, etc.)
├── docs/                 # Vollständige Dokumentation
├── tests/                # 978+ Tests
├── examples/             # Beispielprogramme
├── benchmark/            # Benchmarks
├── editors/              # Editor-Integrationen
└── wasm/                 # WebAssembly-Unterstützung
```

---

## Code-Stil-Richtlinien

### Konstanten und magische Zahlen

Beim Hinzufügen von numerischen Konstanten zur C-Codebasis folge diesen Richtlinien:

1. **Definiere Konstanten in `include/hemlock_limits.h`** - Diese Datei ist der zentrale Ort für alle Kompilierzeit- und Laufzeitlimits, Kapazitäten und benannte Konstanten.

2. **Verwende beschreibende Namen mit `HML_`-Präfix** - Alle Konstanten sollten mit `HML_` präfixiert werden für Namensraum-Klarheit.

3. **Vermeide magische Zahlen** - Ersetze hart-codierte numerische Werte durch benannte Konstanten. Beispiele:
   - Typbereichslimits: `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Pufferkapazitäten: `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Zeitumrechnungen: `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Hash-Seeds: `HML_DJB2_HASH_SEED`
   - ASCII-Werte: `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Inkludiere `hemlock_limits.h`** - Quelldateien sollten diesen Header einbinden (oft via `internal.h`) um auf Konstanten zuzugreifen.

5. **Dokumentiere den Zweck** - Füge einen Kommentar hinzu, der erklärt, was jede Konstante repräsentiert.

---

## Was man NICHT tun sollte

- Implizites Verhalten hinzufügen (ASI, GC, Auto-Cleanup)
- Komplexität verstecken (magische Optimierungen, versteckte Refcounts)
- Bestehende Semantik brechen (Semikolons, manueller Speicher, mutable Strings)
- Präzision bei impliziten Konvertierungen verlieren
- Magische Zahlen verwenden - definiere stattdessen benannte Konstanten in `hemlock_limits.h`

---

## Testen

```bash
make test              # Interpreter-Tests ausführen
make test-compiler     # Compiler-Tests ausführen
make parity            # Paritätstests ausführen (beide müssen übereinstimmen)
make test-all          # Alle Testsuiten ausführen
```

**Wichtig:** Tests können aufgrund von async/Nebenläufigkeitsproblemen hängen bleiben. Verwende immer einen Timeout beim Ausführen von Tests:
```bash
timeout 60 make test   # 60 Sekunden Timeout
timeout 120 make parity
```

Testkategorien: primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Compiler/Interpreter-Architektur

Hemlock hat zwei Ausführungsbackends, die ein gemeinsames Frontend teilen:

```
Quellcode (.hml)
    ↓
┌─────────────────────────────┐
│  GEMEINSAMES FRONTEND       │
│  - Lexer (src/frontend/)    │
│  - Parser (src/frontend/)   │
│  - AST (src/frontend/)      │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ INTERPRETER│    │  COMPILER  │
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ Tree-Walk  │    │ Typcheck   │
│ Auswertung │    │ AST → C    │
│            │    │ gcc Link   │
└────────────┘    └────────────┘
```

### Compiler-Typprüfung

Der Compiler (`hemlockc`) beinhaltet Kompilierzeit-Typprüfung, **standardmäßig aktiviert**:

```bash
hemlockc program.hml -o program    # Typprüft, dann kompiliert
hemlockc --check program.hml       # Nur Typprüfung, nicht kompilieren
hemlockc --no-type-check prog.hml  # Typprüfung deaktivieren
hemlockc --strict-types prog.hml   # Warnung bei impliziten 'any'-Typen
```

Der Typchecker:
- Validiert Typannotationen zur Kompilierzeit
- Behandelt untypisierten Code als dynamisch (`any`-Typ) - immer gültig
- Bietet Optimierungshinweise für Unboxing
- Verwendet permissive numerische Konvertierungen (Bereich zur Laufzeit validiert)

### Verzeichnisstruktur

```
hemlock/
├── src/
│   ├── frontend/           # Gemeinsam: Lexer, Parser, AST, Module
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock: Tree-Walking-Interpreter
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc: C-Code-Generator
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # Language Server
│   │   └── bundler/        # Bundle-/Paket-Tools
├── runtime/                # libhemlock_runtime.a für kompilierte Programme
├── stdlib/                 # Gemeinsame Standardbibliothek
└── tests/
    ├── parity/             # Tests die BEIDE Backends bestehen MÜSSEN
    ├── interpreter/        # Interpreter-spezifische Tests
    └── compiler/           # Compiler-spezifische Tests
```

---

## Paritäts-zuerst-Entwicklung

**Sowohl der Interpreter als auch der Compiler müssen identische Ausgabe für die gleiche Eingabe produzieren.**

### Entwicklungsrichtlinie

Beim Hinzufügen oder Modifizieren von Sprachfeatures:

1. **Design** - Definiere die AST-/semantische Änderung im gemeinsamen Frontend
2. **Interpreter implementieren** - Tree-Walking-Auswertung hinzufügen
3. **Compiler implementieren** - C-Code-Generierung hinzufügen
4. **Paritätstest hinzufügen** - Test in `tests/parity/` mit `.expected`-Datei schreiben
5. **Verifizieren** - Führe `make parity` vor dem Mergen aus

### Paritätsteststruktur

```
tests/parity/
├── language/       # Kern-Sprachfeatures (Kontrollfluss, Closures, etc.)
├── builtins/       # Eingebaute Funktionen (print, typeof, memory, etc.)
├── methods/        # String- und Array-Methoden
└── modules/        # Import/Export, Stdlib-Imports
```

Jeder Test hat zwei Dateien:
- `feature.hml` - Das Testprogramm
- `feature.expected` - Erwartete Ausgabe (muss für beide Backends übereinstimmen)

### Paritätstestergebnisse

| Status | Bedeutung |
|--------|-----------|
| `✓ PASSED` | Sowohl Interpreter als auch Compiler stimmen mit erwarteter Ausgabe überein |
| `◐ INTERP_ONLY` | Interpreter funktioniert, Compiler scheitert (braucht Compiler-Fix) |
| `◑ COMPILER_ONLY` | Compiler funktioniert, Interpreter scheitert (selten) |
| `✗ FAILED` | Beide scheitern (Test- oder Implementierungsfehler) |

### Was Parität erfordert

- Alle Sprachkonstrukte (if, while, for, switch, defer, try/catch)
- Alle Operatoren (arithmetisch, bitweise, logisch, Vergleich)
- Alle eingebauten Funktionen (print, typeof, alloc, etc.)
- Alle String- und Array-Methoden
- Typzwangs- und Promotionsregeln
- Fehlermeldungen für Laufzeitfehler

### Was sich unterscheiden darf

- Leistungscharakteristiken
- Speicherlayout-Details
- Debug-/Stacktrace-Format
- Kompilierungsfehler (Compiler kann mehr zur Kompilierzeit erkennen)

### Einen Paritätstest hinzufügen

```bash
# 1. Testdatei erstellen
cat > tests/parity/language/my_feature.hml << 'EOF'
// Testbeschreibung
let x = some_feature();
print(x);
EOF

# 2. Erwartete Ausgabe vom Interpreter generieren
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Parität verifizieren
make parity
```

---

## Philosophie

> Wir geben dir die Werkzeuge, um sicher zu sein (`buffer`, Typannotationen, Grenzprüfung), aber wir zwingen dich nicht, sie zu verwenden (`ptr`, manueller Speicher, unsichere Operationen).

**Wenn du unsicher bist, ob ein Feature zu Hemlock passt, frage: "Gibt dies dem Programmierer mehr explizite Kontrolle, oder versteckt es etwas?"**

Wenn es versteckt, gehört es wahrscheinlich nicht in Hemlock.
