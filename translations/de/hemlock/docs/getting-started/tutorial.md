# Hemlock Tutorial

Eine umfassende Schritt-für-Schritt-Anleitung zum Erlernen von Hemlock.

## Inhaltsverzeichnis

1. [Hallo Welt](#hallo-welt)
2. [Variablen und Typen](#variablen-und-typen)
3. [Arithmetik und Operationen](#arithmetik-und-operationen)
4. [Kontrollfluss](#kontrollfluss)
5. [Funktionen](#funktionen)
6. [Zeichenketten und Runen](#zeichenketten-und-runen)
7. [Arrays](#arrays)
8. [Objekte](#objekte)
9. [Speicherverwaltung](#speicherverwaltung)
10. [Fehlerbehandlung](#fehlerbehandlung)
11. [Datei-I/O](#datei-io)
12. [Alles zusammenfügen](#alles-zusammenfügen)

## Hallo Welt

Beginnen wir mit dem traditionellen ersten Programm:

```hemlock
print("Hallo, Welt!");
```

Speichern Sie dies als `hello.hml` und führen Sie es aus:

```bash
./hemlock hello.hml
```

**Wichtige Punkte:**
- `print()` ist eine eingebaute Funktion, die auf stdout ausgibt
- Zeichenketten werden in doppelte Anführungszeichen eingeschlossen
- Semikolons sind **obligatorisch**

## Variablen und Typen

### Variablen deklarieren

```hemlock
// Einfache Variablendeklaration
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### Typannotationen

Während Typen standardmäßig abgeleitet werden, können Sie explizit sein:

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### Typinferenz

Hemlock leitet Typen basierend auf Werten ab:

```hemlock
let small = 42;              // i32 (passt in 32-Bit)
let large = 5000000000;      // i64 (zu groß für i32)
let decimal = 3.14;          // f64 (Standard für Gleitkomma)
let text = "hallo";          // string
let flag = true;             // bool
```

### Typprüfung

```hemlock
// Typen mit typeof() prüfen
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hallo"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## Arithmetik und Operationen

### Grundlegende Arithmetik

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3 (Ganzzahldivision)
print(a == b);  // false
print(a > b);   // true
```

### Typpromotion

Beim Mischen von Typen fördert Hemlock zum größeren/genaueren Typ:

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result ist f64 (10.0 + 3.5 = 13.5)

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### Bitweise Operationen

```hemlock
let a = 12;  // 1100 in Binär
let b = 10;  // 1010 in Binär

print(a & b);   // 8  (UND)
print(a | b);   // 14 (ODER)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24 (Linksverschiebung)
print(a >> 1);  // 6  (Rechtsverschiebung)
print(~a);      // -13 (NICHT)
```

## Kontrollfluss

### If-Anweisungen

```hemlock
let x = 10;

if (x > 0) {
    print("positiv");
} else if (x < 0) {
    print("negativ");
} else {
    print("null");
}
```

**Hinweis:** Geschweifte Klammern sind **immer erforderlich**, auch für einzelne Anweisungen.

### While-Schleifen

```hemlock
let count = 0;
while (count < 5) {
    print(`Zähler: ${count}`);
    count = count + 1;
}
```

### For-Schleifen

```hemlock
// C-ähnliche For-Schleife
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// For-in-Schleife (Arrays)
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Element: ${item}`);
}
```

### Switch-Anweisungen

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
// Break: Schleife vorzeitig verlassen
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Gibt aus: 0, 1, 2, 3, 4

// Continue: zur nächsten Iteration springen
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// Gibt aus: 0, 1, 3, 4
```

## Funktionen

### Benannte Funktionen

```hemlock
fn greet(name: string): string {
    return "Hallo, " + name + "!";
}

let message = greet("Alice");
print(message);  // "Hallo, Alice!"
```

### Anonyme Funktionen

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### Rekursion

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Closures

Funktionen erfassen ihre Umgebung:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

### Funktionen höherer Ordnung

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## Zeichenketten und Runen

### Grundlagen von Zeichenketten

Zeichenketten sind **veränderbar** und **UTF-8**:

```hemlock
let s = "hallo";
print(s.length);      // 5 (Zeichenanzahl)
print(s.byte_length); // 5 (Byteanzahl)

// Veränderung
s[0] = 'H';
print(s);  // "Hallo"
```

### Zeichenketten-Methoden

```hemlock
let text = "  Hallo, Welt!  ";

// Groß-/Kleinschreibung
print(text.to_upper());  // "  HALLO, WELT!  "
print(text.to_lower());  // "  hallo, welt!  "

// Trimmen
print(text.trim());      // "Hallo, Welt!"

// Teilstring-Extraktion
let hello = text.substr(2, 5);  // "Hallo"
let world = text.slice(9, 13);  // "Welt"

// Suchen
let pos = text.find("Welt");    // 9
let has = text.contains("o");   // true

// Aufteilen
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// Ersetzen
let s = "hallo welt".replace("welt", "dort");
print(s);  // "hallo dort"
```

### Runen (Unicode-Codepunkte)

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Rune + String-Verkettung
let msg = '>' + " Wichtig";
print(msg);  // "> Wichtig"

// Zwischen Rune und Integer konvertieren
let code: i32 = ch;     // 65 (ASCII-Code)
let r: rune = 128640;   // U+1F680 (🚀)
```

## Arrays

### Array-Grundlagen

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Elemente ändern
numbers[2] = 99;
print(numbers[2]);  // 99
```

### Array-Methoden

```hemlock
let arr = [10, 20, 30];

// Am Ende hinzufügen/entfernen
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40, arr ist jetzt [10, 20, 30]

// Am Anfang hinzufügen/entfernen
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5, arr ist jetzt [10, 20, 30]

// An Index einfügen/entfernen
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// Suchen
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// Slice
let slice = arr.slice(0, 2);  // [10, 15]

// Zu String verbinden
let text = arr.join(", ");    // "10, 15, 30"
```

### Iteration

```hemlock
let items = ["apfel", "banane", "kirsche"];

// For-in-Schleife
for (let item in items) {
    print(item);
}

// Manuelle Iteration
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## Objekte

### Objekt-Literale

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// Felder hinzufügen/ändern
person.email = "alice@example.com";
person.age = 31;
```

### Methoden und `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### Typdefinitionen (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // Optional mit Standard
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // Duck Typing validiert Struktur

print(typeof(typed));   // "Person"
print(typed.active);    // true (Standard angewendet)
```

### JSON-Serialisierung

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// Objekt zu JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON zu Objekt
let restored = json.deserialize();
print(restored.name);  // "test"
```

## Speicherverwaltung

### Sichere Puffer (Empfohlen)

```hemlock
// Puffer allokieren
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// Werte setzen (mit Grenzprüfung)
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Werte zugreifen
print(buf[0]);  // 65

// Muss freigegeben werden, wenn fertig
free(buf);
```

### Rohe Zeiger (Fortgeschritten)

```hemlock
// Rohen Speicher allokieren
let ptr = alloc(100);

// Mit Nullen füllen
memset(ptr, 0, 100);

// Daten kopieren
let src = alloc(50);
memcpy(ptr, src, 50);

// Beide freigeben
free(src);
free(ptr);
```

### Speicherfunktionen

```hemlock
// Neu allokieren
let p = alloc(64);
p = realloc(p, 128);  // Auf 128 Bytes vergrößern
free(p);

// Typisierte Allokation (zukünftig)
// let arr = talloc(i32, 100);  // Array von 100 i32s
```

## Fehlerbehandlung

### Try/Catch

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "Division durch Null";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Fehler: " + e);
}
// Ausgabe: Fehler: Division durch Null
```

### Finally-Block

```hemlock
let file = null;

try {
    file = open("daten.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Fehler: " + e);
} finally {
    // Wird immer ausgeführt
    if (file != null) {
        file.close();
    }
}
```

### Objekte werfen

```hemlock
try {
    throw { code: 404, message: "Nicht gefunden" };
} catch (e) {
    print(`Fehler ${e.code}: ${e.message}`);
}
// Ausgabe: Fehler 404: Nicht gefunden
```

### Panic (Nicht behebbare Fehler)

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x muss nicht-negativ sein");
    }
    return x * 2;
}

validate(-5);  // Programm beendet mit: panic: x muss nicht-negativ sein
```

## Datei-I/O

### Dateien lesen

```hemlock
// Ganze Datei lesen
let f = open("daten.txt", "r");
let content = f.read();
print(content);
f.close();

// Bestimmte Anzahl Bytes lesen
let f2 = open("daten.txt", "r");
let chunk = f2.read(100);  // 100 Bytes lesen
f2.close();
```

### Dateien schreiben

```hemlock
// Text schreiben
let f = open("ausgabe.txt", "w");
f.write("Hallo, Datei!\n");
f.write("Zweite Zeile\n");
f.close();

// An Datei anhängen
let f2 = open("ausgabe.txt", "a");
f2.write("Angehängte Zeile\n");
f2.close();
```

### Binär-I/O

```hemlock
// Binärdaten schreiben
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("daten.bin", "w");
f.write_bytes(buf);
f.close();

// Binärdaten lesen
let f2 = open("daten.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### Dateieigenschaften

```hemlock
let f = open("/pfad/zur/datei.txt", "r");

print(f.path);    // "/pfad/zur/datei.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## Alles zusammenfügen

Lassen Sie uns ein einfaches Wortzähler-Programm erstellen:

```hemlock
// wordcount.hml - Wörter in einer Datei zählen

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // Nach Leerzeichen aufteilen und zählen
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Fehler beim Lesen der Datei: " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// Hauptprogramm
if (args.length < 2) {
    print("Verwendung: " + args[0] + " <dateiname>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Wortanzahl: ${words}`);
    }
}
```

Ausführen mit:
```bash
./hemlock wordcount.hml daten.txt
```

## Nächste Schritte

Herzlichen Glückwunsch! Sie haben die Grundlagen von Hemlock gelernt. Hier ist, was Sie als Nächstes erkunden können:

- [Async & Nebenläufigkeit](../advanced/async-concurrency.md) - Echtes Multi-Threading
- [FFI](../advanced/ffi.md) - C-Funktionen aufrufen
- [Signalverarbeitung](../advanced/signals.md) - Prozesssignale
- [API-Referenz](../reference/builtins.md) - Vollständige API-Dokumentation
- [Beispiele](../../examples/) - Weitere praxisnahe Programme

## Übungsaufgaben

Versuchen Sie, diese Programme zu erstellen, um zu üben:

1. **Taschenrechner**: Implementieren Sie einen einfachen Rechner mit +, -, *, /
2. **Dateikopierer**: Kopieren Sie eine Datei in eine andere
3. **Fibonacci**: Generieren Sie Fibonacci-Zahlen
4. **JSON-Parser**: Lesen und parsen Sie JSON-Dateien
5. **Textprozessor**: Suchen und ersetzen Sie Text in Dateien

Viel Spaß beim Programmieren mit Hemlock! 🚀
