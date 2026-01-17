# Syntax-Uebersicht

Dieses Dokument behandelt die grundlegenden Syntaxregeln und die Struktur von Hemlock-Programmen.

## Grundlegende Syntaxregeln

### Semikolons sind erforderlich

Im Gegensatz zu JavaScript oder Python sind Semikolons **immer erforderlich** am Ende von Anweisungen:

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**Dies verursacht einen Fehler:**
```hemlock
let x = 42  // FEHLER: Fehlendes Semikolon
let y = 10  // FEHLER: Fehlendes Semikolon
```

### Geschweifte Klammern sind immer erforderlich

Alle Kontrollfluss-Bloecke muessen geschweifte Klammern verwenden, auch bei einzelnen Anweisungen:

```hemlock
// RICHTIG
if (x > 0) {
    print("positiv");
}

// FEHLER: Fehlende Klammern
if (x > 0)
    print("positiv");
```

### Kommentare

```hemlock
// Dies ist ein einzeiliger Kommentar

/*
   Dies ist ein
   mehrzeiliger Kommentar
*/

let x = 42;  // Inline-Kommentar
```

## Variablen

### Deklaration

Variablen werden mit `let` deklariert:

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Typannotationen (Optional)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hallo";
```

### Konstanten

Verwenden Sie `const` fuer unveraenderliche Werte:

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Der Versuch, eine Konstante neu zuzuweisen, fuehrt zu einem Laufzeitfehler: "Cannot assign to const variable".

## Ausdruecke

### Arithmetische Operatoren

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - Addition
print(a - b);   // 7  - Subtraktion
print(a * b);   // 30 - Multiplikation
print(a / b);   // 3  - Division (ganzzahlig)
```

### Vergleichsoperatoren

```hemlock
print(a == b);  // false - Gleich
print(a != b);  // true  - Ungleich
print(a > b);   // true  - Groesser als
print(a < b);   // false - Kleiner als
print(a >= b);  // true  - Groesser oder gleich
print(a <= b);  // false - Kleiner oder gleich
```

### Logische Operatoren

```hemlock
let x = true;
let y = false;

print(x && y);  // false - UND
print(x || y);  // true  - ODER
print(!x);      // false - NICHT
```

### Bitweise Operatoren

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - Bitweises UND
print(a | b);   // 14 - Bitweises ODER
print(a ^ b);   // 6  - Bitweises XOR
print(a << 2);  // 48 - Linksverschiebung
print(a >> 1);  // 6  - Rechtsverschiebung
print(~a);      // -13 - Bitweises NICHT
```

### Operatorrangfolge

Von hoechster zu niedrigster Prioritaet:

1. `()` - Gruppierung
2. `!`, `~`, `-` (unaer) - Unaere Operatoren
3. `*`, `/` - Multiplikation, Division
4. `+`, `-` - Addition, Subtraktion
5. `<<`, `>>` - Bitverschiebungen
6. `<`, `<=`, `>`, `>=` - Vergleiche
7. `==`, `!=` - Gleichheit
8. `&` - Bitweises UND
9. `^` - Bitweises XOR
10. `|` - Bitweises ODER
11. `&&` - Logisches UND
12. `||` - Logisches ODER

**Beispiele:**
```hemlock
let x = 2 + 3 * 4;      // 14 (nicht 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Kontrollfluss

### If-Anweisungen

```hemlock
if (condition) {
    // Koerper
}

if (condition) {
    // Then-Zweig
} else {
    // Else-Zweig
}

if (condition1) {
    // Zweig 1
} else if (condition2) {
    // Zweig 2
} else {
    // Standard-Zweig
}
```

### While-Schleifen

```hemlock
while (condition) {
    // Koerper
}
```

**Beispiel:**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### For-Schleifen

**C-artige for-Schleife:**
```hemlock
for (initializer; condition; increment) {
    // Koerper
}
```

**Beispiel:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (Arrays):**
```hemlock
for (let item in array) {
    // Koerper
}
```

**Beispiel:**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Switch-Anweisungen

```hemlock
switch (expression) {
    case value1:
        // Koerper
        break;
    case value2:
        // Koerper
        break;
    default:
        // Standard-Koerper
        break;
}
```

**Beispiel:**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Montag");
        break;
    case 2:
        print("Dienstag");
        break;
    case 3:
        print("Mittwoch");
        break;
    default:
        print("Anderer Tag");
        break;
}
```

### Break und Continue

```hemlock
// Break: Schleife verlassen
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue: Zur naechsten Iteration springen
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Funktionen

### Benannte Funktionen

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // Koerper
    return value;
}
```

**Beispiel:**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Anonyme Funktionen

```hemlock
let func = fn(params) {
    // Koerper
};
```

**Beispiel:**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Typannotationen (Optional)

```hemlock
// Ohne Annotationen (Typen werden abgeleitet)
fn greet(name) {
    return "Hallo, " + name;
}

// Mit Annotationen (zur Laufzeit geprueft)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Objekte

### Objektliterale

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Beispiel:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Methoden

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Beispiel:**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Typdefinitionen

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Beispiel:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Arrays

### Array-Literale

```hemlock
let arr = [element1, element2, element3];
```

**Beispiel:**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "zwei", true, null];
let empty = [];
```

### Array-Indizierung

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // Element aendern
```

## Fehlerbehandlung

### Try/Catch

```hemlock
try {
    // Riskanter Code
} catch (e) {
    // Fehler behandeln
}
```

### Try/Finally

```hemlock
try {
    // Riskanter Code
} finally {
    // Wird immer ausgefuehrt
}
```

### Try/Catch/Finally

```hemlock
try {
    // Riskanter Code
} catch (e) {
    // Fehler behandeln
} finally {
    // Aufraeumen
}
```

### Throw

```hemlock
throw expression;
```

**Beispiel:**
```hemlock
if (x < 0) {
    throw "x muss positiv sein";
}
```

### Panic

```hemlock
panic(message);
```

**Beispiel:**
```hemlock
panic("nicht behebbarer Fehler");
```

## Module (Experimentell)

### Export-Anweisungen

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Import-Anweisungen

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Async (Experimentell)

### Async-Funktionen

```hemlock
async fn function_name(params): return_type {
    // Koerper
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Channels

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (Foreign Function Interface)

### Shared Library importieren

```hemlock
import "library_name.so";
```

### Externe Funktion deklarieren

```hemlock
extern fn function_name(param: type): return_type;
```

**Beispiel:**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Literale

### Ganzzahl-Literale

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // Automatisch i64

// Hexadezimal (0x-Praefix)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Binaer (0b-Praefix)
let bin = 0b1010;
let bin2 = 0b11110000;

// Oktal (0o-Praefix)
let oct = 0o777;
let oct2 = 0O123;

// Numerische Trennzeichen fuer Lesbarkeit
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Gleitkomma-Literale

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // Wissenschaftliche Notation
let sci2 = 2.5E+3;       // Grosses E funktioniert auch
let no_lead = .5;        // Ohne fuehrende Null (0.5)
let sep = 3.14_159_265;  // Numerische Trennzeichen
```

### String-Literale

```hemlock
let s = "hallo";
let escaped = "zeile1\nzeile2\ttabuliert";
let quote = "Sie sagte \"hallo\"";

// Hex-Escape-Sequenzen
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Unicode-Escape-Sequenzen
let emoji = "\u{1F600}";               // (Smiley)
let heart = "\u{2764}";                // (Herz)
let mixed = "Hallo \u{1F30D}!";        // Hallo (Erde)!
```

**Escape-Sequenzen:**
- `\n` - Zeilenumbruch
- `\t` - Tabulator
- `\r` - Wagenruecklauf
- `\\` - Backslash
- `\"` - Anfuehrungszeichen
- `\'` - Apostroph
- `\0` - Null-Zeichen
- `\xNN` - Hex-Escape (2 Ziffern)
- `\u{XXXX}` - Unicode-Escape (1-6 Ziffern)

### Rune-Literale

```hemlock
let ch = 'A';
let emoji = '(Rakete)';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Boolesche Literale

```hemlock
let t = true;
let f = false;
```

### Null-Literal

```hemlock
let nothing = null;
```

## Gueltigkeitsbereichsregeln

### Block-Gueltigkeitsbereich

Variablen sind auf den naechsten umschliessenden Block beschraenkt:

```hemlock
let x = 1;  // Aeusserer Gueltigkeitsbereich

if (true) {
    let x = 2;  // Innerer Gueltigkeitsbereich (ueberdeckt aeusseren)
    print(x);   // 2
}

print(x);  // 1
```

### Funktions-Gueltigkeitsbereich

Funktionen erstellen ihren eigenen Gueltigkeitsbereich:

```hemlock
let global = "global";

fn foo() {
    let local = "lokal";
    print(global);  // Kann aeusseren Gueltigkeitsbereich lesen
}

foo();
// print(local);  // FEHLER: 'local' ist hier nicht definiert
```

### Closure-Gueltigkeitsbereich

Closures erfassen Variablen aus dem umschliessenden Gueltigkeitsbereich:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Erfasst 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Whitespace und Formatierung

### Einrueckung

Hemlock erzwingt keine bestimmte Einrueckung, aber 4 Leerzeichen werden empfohlen:

```hemlock
fn example() {
    if (true) {
        print("eingerueckt");
    }
}
```

### Zeilenumbrueche

Anweisungen koennen mehrere Zeilen umfassen:

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Loop-Anweisung

Das `loop`-Schluesselwort bietet eine sauberere Syntax fuer Endlosschleifen:

```hemlock
loop {
    // ... Arbeit ausfuehren
    if (done) {
        break;
    }
}
```

Dies entspricht `while (true)`, macht aber die Absicht deutlicher.

## Reservierte Schluesselwoerter

Die folgenden Schluesselwoerter sind in Hemlock reserviert:

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Naechste Schritte

- [Typsystem](types.md) - Erfahren Sie mehr ueber das Hemlock-Typsystem
- [Kontrollfluss](control-flow.md) - Vertiefte Betrachtung der Kontrollstrukturen
- [Funktionen](functions.md) - Beherrschen Sie Funktionen und Closures
- [Speicherverwaltung](memory.md) - Verstehen Sie Pointer und Buffer
