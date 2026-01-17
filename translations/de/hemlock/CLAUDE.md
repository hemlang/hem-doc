# Hemlock Sprachdesign-Philosophie

> "Eine kleine, unsichere Sprache, um unsichere Dinge sicher zu schreiben."

Dieses Dokument erfasst die grundlegenden Designprinzipien fuer KI-Assistenten, die mit Hemlock arbeiten.
Fuer detaillierte Dokumentation siehe `docs/README.md` und das `stdlib/docs/`-Verzeichnis.

---

## Kernidentitaet

Hemlock ist eine **System-Skriptsprache** mit manueller Speicherverwaltung und expliziter Kontrolle:
- Die Macht von C mit modernen Skripting-Ergonomien
- Strukturierte async Nebenlaeufigkeit integriert
- Kein verstecktes Verhalten oder Magie

**Hemlock ist NICHT:** Speichersicher, eine GC-Sprache oder versteckt Komplexitaet.
**Hemlock IST:** Explizit statt implizit, lehrreich, eine "C-Skriptschicht" fuer Systemarbeit.

---

## Designprinzipien

### 1. Explizit statt Implizit
- Semikolons obligatorisch (kein ASI)
- Manuelle Speicherverwaltung (alloc/free)
- Typannotationen optional, aber zur Laufzeit geprueft

### 2. Dynamisch standardmaessig, typisiert nach Wahl
- Jeder Wert hat ein Laufzeit-Typ-Tag
- Literale inferieren Typen: `42` → i32, `5000000000` → i64, `3.14` → f64
- Optionale Typannotationen erzwingen Laufzeitpruefungen

### 3. Unsicher ist ein Feature
- Zeigerarithmetik erlaubt (Verantwortung des Benutzers)
- Keine Grenzpruefung bei rohem `ptr` (verwende `buffer` fuer Sicherheit)
- Double-Free-Abstuerze erlaubt

### 4. Strukturierte Nebenlaeufigkeit erstklassig
- `async`/`await` eingebaut mit pthread-basierter Parallelitaet
- Kanaele fuer Kommunikation
- `spawn`/`join`/`detach` fuer Aufgabenverwaltung

### 5. C-aehnliche Syntax
- `{}` Bloecke immer erforderlich
- Kommentare: `// Zeile` und `/* Block */`
- Operatoren entsprechen C: `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Inkrement/Dekrement: `++x`, `x++`, `--x`, `x--` (Praefix und Postfix)
- Zusammengesetzte Zuweisung: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` gibt immer Float zurueck (verwende `divi()` fuer Integer-Division)
- Typsyntax: `let x: type = value;`

---

## Kurzreferenz

### Typen
```
Vorzeichenbehaftet: i8, i16, i32, i64
Vorzeichenlos:      u8, u16, u32, u64
Fliesskomma:        f32, f64
Andere:             bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Aliase:             integer (i32), number (f64), byte (u8)
```

**Typ-Promotion:** i8 → i16 → i32 → i64 → f32 → f64 (Fliesskomma gewinnt immer, aber i64/u64 + f32 → f64 um Praezision zu erhalten)

### Literale
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> i32 max)
let hex = 0xDEADBEEF;    // Hex-Literal
let bin = 0b1010;        // Binaer-Literal
let oct = 0o777;         // Oktal-Literal
let sep = 1_000_000;     // Numerische Trennzeichen erlaubt
let pi = 3.14;           // f64
let half = .5;           // f64 (keine fuehrende Null)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // Hex- und Unicode-Escapes
let ch = 'A';            // rune
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Typkonvertierung
```hemlock
// Typkonstruktorfunktionen - String zu Typ parsen
let n = i32("42");       // String zu i32 parsen
let f = f64("3.14");     // String zu f64 parsen
let b = bool("true");    // String zu bool parsen ("true" oder "false")

// Alle numerischen Typen unterstuetzt
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
// let n: i32 = "42";    // FEHLER - verwende i32("42") fuer String-Parsing
```

### Introspektion
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5 (Stringlaenge in Bytes)
len([1, 2, 3]);          // 3 (Arraylaenge)
```

### Speicher
```hemlock
let p = alloc(64);       // roher Zeiger
let b = buffer(64);      // sicherer Buffer (grenzgeprueft)
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // manuelle Bereinigung erforderlich
```

### Kontrollfluss
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // Endlosschleife (sauberer als while(true))
switch (x) { case 1: break; default: break; }  // C-artiges Fall-Through
defer cleanup();         // laeuft wenn Funktion zurueckkehrt

// Schleifenlabels fuer gezieltes break/continue in verschachtelten Schleifen
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // aeussere Schleife beenden
        if (i == 3) { continue outer; }  // aeussere Schleife fortsetzen
    }
}
```

### Musterabgleich
```hemlock
// Match-Ausdruck - gibt Wert zurueck
let result = match (value) {
    0 => "null",                        // Literal-Muster
    1 | 2 | 3 => "klein",               // ODER-Muster
    n if n < 10 => "mittel",            // Guard-Ausdruck
    n => "gross: " + n                  // Variablenbindung
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

Siehe `docs/language-guide/pattern-matching.md` fuer vollstaendige Dokumentation.

### Null-Koaleszenz-Operatoren
```hemlock
// Null-Koaleszenz (??) - gibt links zurueck wenn nicht-null, sonst rechts
let name = user.name ?? "Anonym";
let first = a ?? b ?? c ?? "fallback";

// Null-Koaleszenz-Zuweisung (??=) - weist nur zu wenn null
let config = null;
config ??= { timeout: 30 };    // config ist jetzt { timeout: 30 }
config ??= { timeout: 60 };    // config unveraendert (nicht null)

// Funktioniert mit Eigenschaften und Indizes
obj.field ??= "standard";
arr[0] ??= "erstes";

// Sichere Navigation (?.) - gibt null zurueck wenn Objekt null ist
let city = user?.address?.city;  // null wenn irgendein Teil null ist
let upper = name?.to_upper();    // sicherer Methodenaufruf
let item = arr?.[0];             // sichere Indizierung
```

### Funktionen
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hallo") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonym/Closure

// Ausdruckskoerper-Funktionen (Pfeilsyntax)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // anonyme Ausdruckskoerper

// Parametermodifikatoren
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // Uebergabe per Referenz
fn print_all(const items: array) { for (i in items) { print(i); } }  // unveraenderlich
```

### Benannte Argumente
```hemlock
// Funktionen koennen mit benannten Argumenten aufgerufen werden
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " ist " + age + " Jahre alt");
}

// Positionelle Argumente (traditionell)
create_user("Alice", 25, false);

// Benannte Argumente - koennen in beliebiger Reihenfolge sein
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Optionale Parameter durch Benennung ueberspringen
create_user("David", active: false);  // Verwendet Standard age=18

// Benannte Argumente muessen nach positionellen kommen
create_user("Eve", age: 21);          // OK: positionell dann benannt
// create_user(name: "Bad", 25);      // FEHLER: positionell nach benannt
```

**Regeln:**
- Benannte Argumente verwenden `name: value` Syntax
- Koennen in beliebiger Reihenfolge nach positionellen Argumenten erscheinen
- Positionelle Argumente koennen nicht nach benannten Argumenten folgen
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
let person = { name, age };         // aequivalent zu { name: name, age: age }

// Objekt-Spread-Operator
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // kopiert defaults, ueberschreibt size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Zusammengesetzte Typen (Schnittmengen-/Duck-Typen)
```hemlock
// Strukturelle Typen definieren
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Zusammengesetzter Typ: Objekt muss ALLE Typen erfuellen
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Funktionsparameter mit zusammengesetzten Typen
fn greet(p: HasName & HasAge) {
    print(p.name + " ist " + p.age);
}

// Drei oder mehr Typen
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Zusaetzliche Felder erlaubt (Duck-Typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - zusaetzliche Felder ignoriert
};
```

Zusammengesetzte Typen bieten Interface-aehnliches Verhalten ohne separates `interface`-Schluesselwort,
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

// Zusammengesetzter Typalias (grossartig fuer wiederverwendbare Interfaces)
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

Typaliase erstellen benannte Abkuerzungen fuer komplexe Typen und verbessern Lesbarkeit und Wartbarkeit.

### Funktionstypen
```hemlock
// Funktionstyp-Annotationen fuer Parameter
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Hoehere Funktion die eine Funktion zurueckgibt
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
// Const-Parameter - tiefe Unveraenderlichkeit
fn print_all(const items: array) {
    // items.push(4);  // FEHLER: kann const-Parameter nicht mutieren
    for (item in items) {
        print(item);
    }
}

// Const mit Objekten - keine Mutation ueber irgendeinen Pfad
fn describe(const person: object) {
    print(person.name);       // OK: Lesen ist erlaubt
    // person.name = "Bob";   // FEHLER: kann nicht mutieren
}

// Verschachtelter Zugriff ist zum Lesen erlaubt
fn get_city(const user: object) {
    return user.address.city;  // OK: verschachtelte Eigenschaften lesen
}
```

Der `const`-Modifikator verhindert jede Mutation des Parameters, einschliesslich verschachtelter Eigenschaften.
Dies bietet Kompilierzeit-Sicherheit fuer Funktionen, die ihre Eingaben nicht modifizieren sollten.

### Ref-Parameter (Uebergabe per Referenz)
```hemlock
// Ref-Parameter - Variable des Aufrufers wird direkt modifiziert
fn increment(ref x: i32) {
    x = x + 1;  // Modifiziert die urspruengliche Variable
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

// Ref und regulaere Parameter mischen
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

Der `ref`-Modifikator uebergibt eine Referenz zur Variable des Aufrufers, sodass die Funktion
sie direkt modifizieren kann. Ohne `ref` werden Primitives per Wert uebergeben (kopiert). Verwende `ref` wenn
du den Zustand des Aufrufers mutieren musst, ohne einen Wert zurueckzugeben.

**Regeln:**
- `ref`-Parameter muessen Variablen uebergeben werden, keine Literale oder Ausdruecke
- Funktioniert mit allen Typen (Primitives, Arrays, Objekte)
- Kombiniere mit Typannotationen: `ref x: i32`
- Kann nicht mit `const` kombiniert werden (sie sind Gegensaetze)

### Methodensignaturen in Define
```hemlock
// Define mit Methodensignaturen (Interface-Muster)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Erforderliche Methodensignatur
}

// Objekte muessen die erforderliche Methode bereitstellen
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
    fn clone(): Self   // Gibt gleichen Typ wie das Objekt zurueck
}
```

Methodensignaturen in `define`-Bloecken verwenden Komma-Trennzeichen (wie TypeScript-Interfaces),
etablieren Vertraege, die Objekte erfuellen muessen, und ermoeglichen Interface-artige Programmier-
muster mit Hemlocks Duck-Typing-System.

### Fehlerbehandlung
```hemlock
try { throw "fehler"; } catch (e) { print(e); } finally { cleanup(); }
panic("nicht behebbar");  // beendet sofort, nicht abfangbar
```

### Async/Nebenlaeufigkeit
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // oder join(task)
detach(spawn(background_work));

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**Speicherbesitz:** Tasks erhalten Kopien von Primitivwerten, teilen aber Zeiger. Wenn du einen `ptr` an einen gespawnten Task uebergibst, musst du sicherstellen, dass der Speicher gueltig bleibt, bis der Task abgeschlossen ist. Verwende `join()` vor `free()`, oder verwende Kanaele, um Abschluss zu signalisieren.

### Benutzereingabe
```hemlock
let name = read_line();          // Zeile von stdin lesen (blockiert)
print("Hallo, " + name);
eprint("Fehlermeldung");         // Auf stderr ausgeben

// read_line() gibt null bei EOF zurueck
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

## String-Methoden (19)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `to_upper`, `to_lower`,
`starts_with`, `ends_with`, `replace`, `replace_all`, `repeat`, `char_at`,
`byte_at`, `chars`, `bytes`, `to_bytes`, `deserialize`

Template-Strings: `` `Hallo ${name}!` ``

**String-Mutabilitaet:** Strings sind per Indexzuweisung mutierbar (`s[0] = 'H'`), aber alle String-Methoden geben neue Strings zurueck, ohne das Original zu modifizieren. Dies erlaubt In-Place-Mutation wenn noetig, waehrend Methodenverkettung funktional bleibt.

**String-Laengeneigenschaften:**
```hemlock
let s = "hallo 🚀";
print(s.length);       // 7 (Zeichen-/Rune-Anzahl)
print(s.byte_length);  // 10 (Byte-Anzahl - Emoji ist 4 Bytes UTF-8)
```

## Array-Methoden (18)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`

Typisierte Arrays: `let nums: array<i32> = [1, 2, 3];`

---

## Standardbibliothek (40 Module)

Importieren mit `@stdlib/`-Praefix:
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
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | CSV-Parsing und -Generierung |
| `datetime` | DateTime-Klasse, Formatierung, Parsing |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `fmt` | String-Formatierungs-Utilities |
| `fs` | read_file, write_file, list_dir, exists |
| `glob` | Datei-Musterabgleich |
| `hash` | sha256, sha512, md5, djb2 |
| `http` | http_get, http_post, http_request |
| `ipc` | Inter-Prozess-Kommunikation |
| `iter` | Iterator-Utilities |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger mit Stufen |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Dateipfad-Manipulation |
| `process` | fork, exec, wait, kill |
| `random` | Zufallszahlengenerierung |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Wiederholungslogik mit Backoff |
| `semver` | Semantische Versionierung |
| `shell` | Shell-Befehls-Utilities |
| `sqlite` | SQLite-Datenbank, query, exec, Transaktionen |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | ANSI-Farben und -Stile |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | TOML-Parsing und -Generierung |
| `url` | URL-Parsing und -Manipulation |
| `uuid` | UUID-Generierung |
| `websocket` | WebSocket-Client |

Siehe `stdlib/docs/` fuer detaillierte Moduldokumentation.

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

Lock-freie nebenlaeufige Programmierung mit atomaren Operationen:

```hemlock
// Speicher fuer atomares i32 allokieren
let p = alloc(4);
ptr_write_i32(p, 0);

// Atomares Laden/Speichern
let val = atomic_load_i32(p);        // Atomar lesen
atomic_store_i32(p, 42);             // Atomar schreiben

// Fetch-and-Modify-Operationen (geben ALTEN Wert zurueck)
let old = atomic_add_i32(p, 10);     // Addieren, alten zurueckgeben
old = atomic_sub_i32(p, 5);          // Subtrahieren, alten zurueckgeben
old = atomic_and_i32(p, 0xFF);       // Bitweises UND
old = atomic_or_i32(p, 0x10);        // Bitweises ODER
old = atomic_xor_i32(p, 0x0F);       // Bitweises XOR

// Compare-and-Swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // Wenn *p == 42, auf 100 setzen
// Gibt true zurueck wenn Swap erfolgreich, sonst false

// Atomarer Austausch
old = atomic_exchange_i32(p, 999);   // Tauschen, alten zurueckgeben

free(p);

// i64-Varianten verfuegbar (atomic_load_i64, atomic_add_i64, etc.)

// Speicherbarriere (vollstaendige Barriere)
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
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # Bundle-/Paket-Tools
├── runtime/              # Kompilierte Programm-Laufzeit (libhemlock_runtime.a)
├── stdlib/               # Standardbibliothek (40 Module)
│   └── docs/             # Moduldokumentation
├── docs/                 # Vollstaendige Dokumentation
│   ├── language-guide/   # Typen, Strings, Arrays, etc.
│   ├── reference/        # API-Referenzen
│   └── advanced/         # Async, FFI, Signale, etc.
├── tests/                # 625+ Tests
└── examples/             # Beispielprogramme
```

---

## Code-Stil-Richtlinien

### Konstanten und magische Zahlen

Beim Hinzufuegen von numerischen Konstanten zur C-Codebasis folge diesen Richtlinien:

1. **Definiere Konstanten in `include/hemlock_limits.h`** - Diese Datei ist der zentrale Ort fuer alle Kompilierzeit- und Laufzeitlimits, Kapazitaeten und benannte Konstanten.

2. **Verwende beschreibende Namen mit `HML_`-Praefix** - Alle Konstanten sollten mit `HML_` praefixiert werden fuer Namensraum-Klarheit.

3. **Vermeide magische Zahlen** - Ersetze hart-codierte numerische Werte durch benannte Konstanten. Beispiele:
   - Typbereichslimits: `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Pufferkapazitaeten: `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Zeitumrechnungen: `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Hash-Seeds: `HML_DJB2_HASH_SEED`
   - ASCII-Werte: `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Inkludiere `hemlock_limits.h`** - Quelldateien sollten diesen Header einbinden (oft via `internal.h`) um auf Konstanten zuzugreifen.

5. **Dokumentiere den Zweck** - Fuege einen Kommentar hinzu, der erklaert, was jede Konstante repraesentiert.

---

## Was man NICHT tun sollte

- Implizites Verhalten hinzufuegen (ASI, GC, Auto-Cleanup)
- Komplexitaet verstecken (magische Optimierungen, versteckte Refcounts)
- Bestehende Semantik brechen (Semikolons, manueller Speicher, mutable Strings)
- Praezision bei impliziten Konvertierungen verlieren
- Magische Zahlen verwenden - definiere stattdessen benannte Konstanten in `hemlock_limits.h`

---

## Testen

```bash
make test              # Interpreter-Tests ausfuehren
make test-compiler     # Compiler-Tests ausfuehren
make parity            # Paritaetstests ausfuehren (beide muessen uebereinstimmen)
make test-all          # Alle Testsuiten ausfuehren
```

**Wichtig:** Tests koennen aufgrund von async/Nebenlaeufigkeitsproblemen haengen bleiben. Verwende immer einen Timeout beim Ausfuehren von Tests:
```bash
timeout 60 make test   # 60 Sekunden Timeout
timeout 120 make parity
```

Testkategorien: primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Compiler/Interpreter-Architektur

Hemlock hat zwei Ausfuehrungsbackends, die ein gemeinsames Frontend teilen:

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

### Compiler-Typpruefung

Der Compiler (`hemlockc`) beinhaltet Kompilierzeit-Typpruefung, **standardmaessig aktiviert**:

```bash
hemlockc program.hml -o program    # Typprueft, dann kompiliert
hemlockc --check program.hml       # Nur Typpruefung, nicht kompilieren
hemlockc --no-type-check prog.hml  # Typpruefung deaktivieren
hemlockc --strict-types prog.hml   # Warnung bei impliziten 'any'-Typen
```

Der Typchecker:
- Validiert Typannotationen zur Kompilierzeit
- Behandelt untypisierten Code als dynamisch (`any`-Typ) - immer gueltig
- Bietet Optimierungshinweise fuer Unboxing
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
├── runtime/                # libhemlock_runtime.a fuer kompilierte Programme
├── stdlib/                 # Gemeinsame Standardbibliothek
└── tests/
    ├── parity/             # Tests die BEIDE Backends bestehen MUESSEN
    ├── interpreter/        # Interpreter-spezifische Tests
    └── compiler/           # Compiler-spezifische Tests
```

---

## Paritaets-zuerst-Entwicklung

**Sowohl der Interpreter als auch der Compiler muessen identische Ausgabe fuer die gleiche Eingabe produzieren.**

### Entwicklungsrichtlinie

Beim Hinzufuegen oder Modifizieren von Sprachfeatures:

1. **Design** - Definiere die AST-/semantische Aenderung im gemeinsamen Frontend
2. **Interpreter implementieren** - Tree-Walking-Auswertung hinzufuegen
3. **Compiler implementieren** - C-Code-Generierung hinzufuegen
4. **Paritaetstest hinzufuegen** - Test in `tests/parity/` mit `.expected`-Datei schreiben
5. **Verifizieren** - Fuehre `make parity` vor dem Mergen aus

### Paritaetsteststruktur

```
tests/parity/
├── language/       # Kern-Sprachfeatures (Kontrollfluss, Closures, etc.)
├── builtins/       # Eingebaute Funktionen (print, typeof, memory, etc.)
├── methods/        # String- und Array-Methoden
└── modules/        # Import/Export, Stdlib-Imports
```

Jeder Test hat zwei Dateien:
- `feature.hml` - Das Testprogramm
- `feature.expected` - Erwartete Ausgabe (muss fuer beide Backends uebereinstimmen)

### Paritaetstestergebnisse

| Status | Bedeutung |
|--------|-----------|
| `✓ PASSED` | Sowohl Interpreter als auch Compiler stimmen mit erwarteter Ausgabe ueberein |
| `◐ INTERP_ONLY` | Interpreter funktioniert, Compiler scheitert (braucht Compiler-Fix) |
| `◑ COMPILER_ONLY` | Compiler funktioniert, Interpreter scheitert (selten) |
| `✗ FAILED` | Beide scheitern (Test- oder Implementierungsfehler) |

### Was Paritaet erfordert

- Alle Sprachkonstrukte (if, while, for, switch, defer, try/catch)
- Alle Operatoren (arithmetisch, bitweise, logisch, Vergleich)
- Alle eingebauten Funktionen (print, typeof, alloc, etc.)
- Alle String- und Array-Methoden
- Typzwangs- und Promotionsregeln
- Fehlermeldungen fuer Laufzeitfehler

### Was sich unterscheiden darf

- Leistungscharakteristiken
- Speicherlayout-Details
- Debug-/Stacktrace-Format
- Kompilierungsfehler (Compiler kann mehr zur Kompilierzeit erkennen)

### Einen Paritaetstest hinzufuegen

```bash
# 1. Testdatei erstellen
cat > tests/parity/language/my_feature.hml << 'EOF'
// Testbeschreibung
let x = some_feature();
print(x);
EOF

# 2. Erwartete Ausgabe vom Interpreter generieren
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Paritaet verifizieren
make parity
```

---

## Version

**v1.8.0** - Aktuelles Release mit:
- **Musterabgleich** (`match`-Ausdruecke) - Maechtige Destrukturierung und Kontrollfluss:
  - Literal-, Platzhalter- und Variablenbindungsmuster
  - ODER-Muster (`1 | 2 | 3`)
  - Guard-Ausdruecke (`n if n > 0`)
  - Objekt-Destrukturierung (`{ x, y }`)
  - Array-Destrukturierung mit Rest (`[first, ...rest]`)
  - Typmuster (`n: i32`)
  - Volle Paritaet zwischen Interpreter und Compiler
- **Compiler-Hilfsannotationen** - 11 Optimierungsannotationen fuer GCC/Clang-Kontrolle:
  - `@inline`, `@noinline` - Funktions-Inlining-Kontrolle
  - `@hot`, `@cold` - Branch-Prediction-Hinweise
  - `@pure`, `@const` - Seiteneffekt-Annotationen
  - `@flatten` - alle Aufrufe innerhalb der Funktion inlinen
  - `@optimize(level)` - Pro-Funktion-Optimierungsstufe ("0", "1", "2", "3", "s", "fast")
  - `@warn_unused` - Warnung bei ignorierten Rueckgabewerten
  - `@section(name)` - Benutzerdefinierte ELF-Sektionsplatzierung (z.B. `@section(".text.hot")`)
- **Ausdruckskoerper-Funktionen** (`fn double(x): i32 => x * 2;`) - praegnante Einzelausdruck-Funktionssyntax
- **Einzeilige Anweisungen** - klammerlose `if`, `while`, `for`-Syntax (z.B. `if (x > 0) print(x);`)
- **Typaliase** (`type Name = Type;`) - benannte Abkuerzungen fuer komplexe Typen
- **Funktionstyp-Annotationen** (`fn(i32): i32`) - erstklassige Funktionstypen
- **Const-Parameter** (`fn(const x: array)`) - tiefe Unveraenderlichkeit fuer Parameter
- **Ref-Parameter** (`fn(ref x: i32)`) - Uebergabe per Referenz fuer direkte Aufrufer-Mutation
- **Methodensignaturen in define** (`fn method(): Type`) - Interface-artige Vertraege (komma-getrennt)
- **Self-Typ** in Methodensignaturen - bezieht sich auf den definierenden Typ
- **Loop-Schluesselwort** (`loop { }`) - sauberere Endlosschleifen, ersetzt `while (true)`
- **Schleifenlabels** (`outer: while`) - gezieltes break/continue fuer verschachtelte Schleifen
- **Objekt-Kurzschreibweise** (`{ name }`) - ES6-Stil-Kurzeigenschaften-Syntax
- **Objekt-Spread** (`{ ...obj }`) - Objektfelder kopieren und zusammenfuehren
- **Zusammengesetzte Duck-Typen** (`A & B & C`) - Schnittmengentypen fuer strukturelle Typisierung
- **Benannte Argumente** fuer Funktionsaufrufe (`foo(name: "value", age: 30)`)
- **Null-Koaleszenz-Operatoren** (`??`, `??=`, `?.`) fuer sichere Null-Behandlung
- **Oktal-Literale** (`0o777`, `0O123`)
- **Numerische Trennzeichen** (`1_000_000`, `0xFF_FF`, `0b1111_0000`)
- **Blockkommentare** (`/* ... */`)
- **Hex-Escape-Sequenzen** in Strings/Runes (`\x41` = 'A')
- **Unicode-Escape-Sequenzen** in Strings (`\u{1F600}` = 😀)
- **Float-Literale ohne fuehrende Null** (`.5`, `.123`, `.5e2`)
- **Kompilierzeit-Typpruefung** in hemlockc (standardmaessig aktiviert)
- **LSP-Integration** mit Typpruefung fuer Echtzeit-Diagnosen
- **Zusammengesetzte Zuweisungsoperatoren** (`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`)
- **Inkrement/Dekrement-Operatoren** (`++x`, `x++`, `--x`, `x--`)
- **Typ-Praezisions-Fix**: i64/u64 + f32 → f64 um Praezision zu erhalten
- Vereinheitlichtes Typsystem mit Unboxing-Optimierungshinweisen
- Volles Typsystem (i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object, enum, file, task, channel)
- UTF-8-Strings mit 19 Methoden
- Arrays mit 18 Methoden einschliesslich map/filter/reduce
- Manuelle Speicherverwaltung mit `talloc()` und `sizeof()`
- Async/await mit echter pthread-Parallelitaet
- Atomare Operationen fuer lock-freie nebenlaeufige Programmierung
- 40 Stdlib-Module (+ arena, assert, semver, toml, retry, iter, random, shell)
- FFI fuer C-Interop mit `export extern fn` fuer wiederverwendbare Bibliotheks-Wrapper
- FFI-Struct-Unterstuetzung im Compiler (C-Structs per Wert uebergeben)
- FFI-Zeiger-Helfer (`ptr_null`, `ptr_read_*`, `ptr_write_*`)
- defer, try/catch/finally/throw, panic
- Datei-I/O, Signalbehandlung, Befehlsausfuehrung
- [hpm](https://github.com/hemlang/hpm) Paketmanager mit GitHub-basierter Registry
- Compiler-Backend (C-Code-Generierung) mit 100% Interpreter-Paritaet
- LSP-Server mit Go-to-Definition und Find-References
- AST-Optimierungspass und Variablenaufloesung fuer O(1)-Lookup
- apply()-Builtin fuer dynamische Funktionsaufrufe
- Ungepufferte Kanaele und Many-Params-Unterstuetzung
- 159 Paritaetstests (100% Erfolgsrate)

---

## Philosophie

> Wir geben dir die Werkzeuge, um sicher zu sein (`buffer`, Typannotationen, Grenzpruefung), aber wir zwingen dich nicht, sie zu verwenden (`ptr`, manueller Speicher, unsichere Operationen).

**Wenn du unsicher bist, ob ein Feature zu Hemlock passt, frage: "Gibt dies dem Programmierer mehr explizite Kontrolle, oder versteckt es etwas?"**

Wenn es versteckt, gehoert es wahrscheinlich nicht in Hemlock.
