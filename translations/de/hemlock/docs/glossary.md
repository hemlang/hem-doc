# Glossar

Neu in der Programmierung oder bei Systemkonzepten? Dieses Glossar erklärt Begriffe, die in der Hemlock-Dokumentation verwendet werden, in einfacher Sprache.

---

## A

### Allokieren / Allokation
**Was es bedeutet:** Den Computer um einen Speicherblock bitten, den man verwenden kann.

**Analogie:** Wie ein Buch aus einer Bibliothek ausleihen - man leiht sich Platz, den man später zurückgeben muss.

**In Hemlock:**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### Array
**Was es bedeutet:** Eine Liste von Werten, die zusammen gespeichert werden und über die Position (Index) zugänglich sind.

**Analogie:** Wie eine Reihe von Briefkästen, nummeriert 0, 1, 2, 3... Man kann etwas in Briefkasten #2 legen und es später aus Briefkasten #2 holen.

**In Hemlock:**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Asynchron
**Was es bedeutet:** Code, der "im Hintergrund" laufen kann, während anderer Code fortgesetzt wird. In Hemlock läuft asynchroner Code tatsächlich gleichzeitig auf separaten CPU-Kernen.

**Analogie:** Wie mehrere Gerichte gleichzeitig kochen - man setzt den Reis auf, und während er kocht, schneidet man Gemüse. Beides passiert gleichzeitig.

**In Hemlock:**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Boolean / Bool
**Was es bedeutet:** Ein Wert, der entweder `true` oder `false` ist. Nichts anderes.

**Benannt nach:** George Boole, einem Mathematiker, der Wahr/Falsch-Logik untersuchte.

**In Hemlock:**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Grenzenpruefung (Bounds Checking)
**Was es bedeutet:** Automatische Überprüfung, dass man nicht versucht, auf Speicher außerhalb des zugewiesenen Bereichs zuzugreifen. Verhindert Abstürze und Sicherheitslücken.

**Analogie:** Wie ein Bibliothekar, der prüft, ob das angeforderte Buch tatsächlich existiert, bevor er versucht, es zu holen.

**In Hemlock:**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer
**Was es bedeutet:** Ein sicherer Behälter für Rohbytes mit bekannter Größe. Hemlock prüft, dass man nicht über seine Grenzen hinaus liest oder schreibt.

**Analogie:** Wie ein Safe mit einer bestimmten Anzahl von Fächern. Man kann jedes Fach verwenden, aber man kann nicht auf Fach #50 zugreifen, wenn der Safe nur 10 hat.

**In Hemlock:**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Closure
**Was es bedeutet:** Eine Funktion, die sich Variablen von dort "merkt", wo sie erstellt wurde, auch nachdem dieser Code beendet ist.

**Analogie:** Wie eine Notiz, die sagt "addiere 5 zu jeder Zahl, die du mir gibst" - die "5" ist in die Notiz eingebaut.

**In Hemlock:**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Typumwandlung (Type Coercion)
**Was es bedeutet:** Automatische Konvertierung eines Wertes von einem Typ in einen anderen bei Bedarf.

**Beispiel:** Wenn man eine Ganzzahl und eine Dezimalzahl addiert, wird die Ganzzahl zuerst automatisch in eine Dezimalzahl umgewandelt.

**In Hemlock:**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Kompilieren / Compiler
**Was es bedeutet:** Ihren Code in ein Programm übersetzen, das der Computer direkt ausführen kann. Der Compiler (`hemlockc`) liest Ihre `.hml`-Datei und erstellt eine ausführbare Datei.

**Analogie:** Wie ein Buch von Englisch nach Spanisch übersetzen - der Inhalt ist der gleiche, aber jetzt können Spanischsprechende es lesen.

**In Hemlock:**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Nebenläufigkeit (Concurrency)
**Was es bedeutet:** Mehrere Dinge, die sich zeitlich überlappen. In Hemlock bedeutet das tatsächliche parallele Ausführung auf mehreren CPU-Kernen.

**Analogie:** Zwei Köche, die gleichzeitig verschiedene Gerichte in derselben Küche kochen.

---

## D

### Defer
**Was es bedeutet:** Etwas für später einplanen, wenn die aktuelle Funktion beendet wird. Nützlich für Aufräumarbeiten.

**Analogie:** Wie sich selbst sagen "wenn ich gehe, mach das Licht aus" - man setzt die Erinnerung jetzt, sie passiert später.

**In Hemlock:**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck-Typing
**Was es bedeutet:** Wenn es wie eine Ente aussieht und wie eine Ente quakt, behandle es als Ente. Im Code: Wenn ein Objekt die Felder/Methoden hat, die man braucht, verwende es - kümmere dich nicht um seinen offiziellen "Typ".

**Benannt nach:** Dem Ententest - einer Form des logischen Schliessens.

**In Hemlock:**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Ausdruck (Expression)
**Was es bedeutet:** Code, der einen Wert erzeugt. Kann überall verwendet werden, wo ein Wert erwartet wird.

**Beispiele:** `42`, `x + y`, `get_name()`, `true && false`

### Enum / Aufzählung
**Was es bedeutet:** Ein Typ mit einer festen Menge möglicher Werte, jeder mit einem Namen.

**Analogie:** Wie ein Dropdown-Menü - man kann nur aus den aufgelisteten Optionen wählen.

**In Hemlock:**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Fliesskommazahl
**Was es bedeutet:** Eine Zahl mit Dezimalpunkt. "Fliesskomma" genannt, weil der Dezimalpunkt an verschiedenen Positionen sein kann.

**In Hemlock:**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free (Freigeben)
**Was es bedeutet:** Speicher, den man nicht mehr benötigt, an das System zurückgeben, damit er wiederverwendet werden kann.

**Analogie:** Ein Bibliotheksbuch zurückgeben, damit andere es ausleihen können.

**In Hemlock:**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Funktion
**Was es bedeutet:** Ein wiederverwendbarer Codeblock, der Eingaben (Parameter) entgegennimmt und möglicherweise eine Ausgabe (Rückgabewert) produziert.

**Analogie:** Wie ein Rezept - gib ihm Zutaten (Eingaben), folge den Schritten, erhalte ein Gericht (Ausgabe).

**In Hemlock:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Garbage Collection (GC)
**Was es bedeutet:** Automatische Speicherbereinigung. Die Laufzeitumgebung findet periodisch ungenutzten Speicher und gibt ihn für Sie frei.

**Warum Hemlock es nicht hat:** GC kann unvorhersehbare Pausen verursachen. Hemlock bevorzugt explizite Kontrolle - Sie entscheiden, wann Speicher freigegeben wird.

**Hinweis:** Die meisten Hemlock-Typen (Strings, Arrays, Objekte) werden automatisch bereinigt, wenn sie den Gültigkeitsbereich verlassen. Nur rohe `ptr` von `alloc()` benötigen manuelles `free()`.

---

## H

### Heap
**Was es bedeutet:** Ein Speicherbereich für Daten, die länger als die aktuelle Funktion bestehen müssen. Man allokiert und gibt Heap-Speicher explizit frei.

**Im Gegensatz zu:** Stack (automatischer, temporärer Speicher für lokale Variablen)

**In Hemlock:**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Index
**Was es bedeutet:** Die Position eines Elements in einem Array oder String. Beginnt bei 0 in Hemlock.

**In Hemlock:**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Ganzzahl (Integer)
**Was es bedeutet:** Eine ganze Zahl ohne Dezimalpunkt. Kann positiv, negativ oder Null sein.

**In Hemlock:**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interpreter
**Was es bedeutet:** Ein Programm, das Ihren Code liest und ihn direkt, Zeile für Zeile, ausführt.

**Im Gegensatz zu:** Compiler (übersetzt Code zuerst, führt dann die Übersetzung aus)

**In Hemlock:**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Literal
**Was es bedeutet:** Ein Wert, der direkt in Ihrem Code geschrieben wird, nicht berechnet.

**Beispiele:**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Speicherleck (Memory Leak)
**Was es bedeutet:** Vergessen, allokierten Speicher freizugeben. Der Speicher bleibt reserviert, aber ungenutzt und verschwendet Ressourcen.

**Analogie:** Bibliotheksbuecher ausleihen und nie zurückgeben. Irgendwann hat die Bibliothek keine Bücher mehr.

**In Hemlock:**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Methode
**Was es bedeutet:** Eine Funktion, die an ein Objekt oder einen Typ angehängt ist.

**In Hemlock:**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex
**Was es bedeutet:** Eine Sperre, die sicherstellt, dass nur ein Thread gleichzeitig auf etwas zugreift. Verhindert Datenbeschädigung, wenn mehrere Threads gemeinsame Daten berühren.

**Analogie:** Wie ein Badezimmerschloss - nur eine Person kann es gleichzeitig benutzen.

---

## N

### Null
**Was es bedeutet:** Ein spezieller Wert, der "nichts" oder "kein Wert" bedeutet.

**In Hemlock:**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Objekt
**Was es bedeutet:** Eine Sammlung von benannten Werten (Feldern/Eigenschaften), die zusammen gruppiert sind.

**In Hemlock:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parameter
**Was es bedeutet:** Eine Variable, die eine Funktion beim Aufruf erwartet.

**Auch genannt:** Argument (technisch gesehen ist Parameter in der Definition, Argument im Aufruf)

**In Hemlock:**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Zeiger (Pointer)
**Was es bedeutet:** Ein Wert, der eine Speicheradresse enthält - er "zeigt" auf den Ort, an dem Daten gespeichert sind.

**Analogie:** Wie eine Strassenadresse. Die Adresse ist nicht das Haus - sie sagt Ihnen, wo Sie das Haus finden.

**In Hemlock:**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitiv
**Was es bedeutet:** Ein grundlegender, eingebauter Typ, der nicht aus anderen Typen besteht.

**In Hemlock:** `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `null`

---

## R

### Referenzzählung (Reference Counting)
**Was es bedeutet:** Verfolgen, wie viele Dinge ein Datenstück verwenden. Wenn nichts es mehr verwendet, wird es automatisch bereinigt.

**In Hemlock:** Strings, Arrays, Objekte und Buffer verwenden intern Referenzzählung. Man sieht es nicht, aber es verhindert Speicherlecks für die meisten gängigen Typen.

### Rückgabewert
**Was es bedeutet:** Der Wert, den eine Funktion zurücksendet, wenn sie fertig ist.

**In Hemlock:**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**Was es bedeutet:** Ein einzelnes Unicode-Zeichen (Codepunkt). Kann jedes Zeichen einschliesslich Emoji darstellen.

**Warum "Rune"?** Der Begriff kommt von Go. Er betont, dass es sich um ein vollständiges Zeichen handelt, nicht nur um ein Byte.

**In Hemlock:**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Laufzeit (Runtime)
**Was es bedeutet:** Die Zeit, in der Ihr Programm tatsächlich läuft (im Gegensatz zur "Kompilierzeit", wenn es übersetzt wird).

**Auch:** Der unterstützende Code, der neben Ihrem Programm läuft (z.B. der Speicherallokator).

---

## S

### Gültigkeitsbereich (Scope)
**Was es bedeutet:** Der Bereich des Codes, in dem eine Variable existiert und verwendet werden kann.

**In Hemlock:**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Stack
**Was es bedeutet:** Speicher für temporäre, kurzlebige Daten. Automatisch verwaltet - wenn eine Funktion zurückkehrt, wird ihr Stack-Speicher zurückgewonnen.

**Im Gegensatz zu:** Heap (langlebiger, manuell verwaltet)

### Anweisung (Statement)
**Was es bedeutet:** Eine einzelne Instruktion oder ein Befehl. Anweisungen TUN Dinge; Ausdrücke ERZEUGEN Werte.

**Beispiele:** `let x = 5;`, `print("hi");`, `if (x > 0) { ... }`

### String
**Was es bedeutet:** Eine Zeichenfolge (Text).

**In Hemlock:**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Strukturelle Typisierung
**Was es bedeutet:** Typkompatibilität basierend auf der Struktur (welche Felder/Methoden existieren), nicht auf dem Namen. Dasselbe wie "Duck-Typing".

---

## T

### Thread
**Was es bedeutet:** Ein separater Ausführungspfad. Mehrere Threads können gleichzeitig auf verschiedenen CPU-Kernen laufen.

**In Hemlock:** `spawn()` erstellt einen neuen Thread.

### Typ
**Was es bedeutet:** Die Art von Daten, die ein Wert repräsentiert. Bestimmt, welche Operationen gültig sind.

**In Hemlock:**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Typannotation
**Was es bedeutet:** Explizites Deklarieren, welchen Typ eine Variable haben soll.

**In Hemlock:**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**Was es bedeutet:** Eine Methode zur Textkodierung, die alle Weltsprachen und Emoji unterstützt. Jedes Zeichen kann 1-4 Bytes lang sein.

**In Hemlock:** Alle Strings sind UTF-8.

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variable
**Was es bedeutet:** Ein benannter Speicherort, der einen Wert enthält.

**In Hemlock:**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## Kurzreferenz: Welchen Typ sollte ich verwenden?

| Situation | Verwende dies | Warum |
|-----------|---------------|-------|
| Brauche einfach eine Zahl | `let x = 42;` | Hemlock wählt den richtigen Typ |
| Dinge zählen | `i32` | Gross genug für die meisten Zählungen |
| Riesige Zahlen | `i64` | Wenn i32 nicht reicht |
| Bytes (0-255) | `u8` | Dateien, Netzwerkdaten |
| Dezimalzahlen | `f64` | Präzise Dezimalmathematik |
| Ja/Nein-Werte | `bool` | Nur `true` oder `false` |
| Text | `string` | Beliebiger Textinhalt |
| Einzelnes Zeichen | `rune` | Ein Buchstabe/Emoji |
| Liste von Dingen | `array` | Geordnete Sammlung |
| Benannte Felder | `object` | Zusammengehörige Daten gruppieren |
| Rohspeicher | `buffer` | Sichere Byte-Speicherung |
| FFI/Systemarbeit | `ptr` | Fortgeschritten, manueller Speicher |

---

## Siehe auch

- [Schnellstart](getting-started/quick-start.md) - Ihr erstes Hemlock-Programm
- [Typsystem](language-guide/types.md) - Vollständige Typdokumentation
- [Speicherverwaltung](language-guide/memory.md) - Speicher verstehen
