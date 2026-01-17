# Schnellstart

Starten Sie mit Hemlock in wenigen Minuten!

## Ihr erstes Programm

Erstellen Sie eine Datei namens `hello.hml`:

```hemlock
print("Hallo, Hemlock!");
```

Führen Sie es mit dem Interpreter aus:

```bash
./hemlock hello.hml
```

Oder kompilieren Sie es zu einer nativen ausführbaren Datei:

```bash
./hemlockc hello.hml -o hello
./hello
```

Ausgabe:
```
Hallo, Hemlock!
```

### Interpreter vs. Compiler

Hemlock bietet zwei Möglichkeiten, Programme auszuführen:

| Werkzeug | Anwendungsfall | Typprüfung |
|----------|----------------|------------|
| `hemlock` | Schnelle Skripte, REPL, Entwicklung | Nur zur Laufzeit |
| `hemlockc` | Produktionsbinärdateien, bessere Leistung | Zur Kompilierzeit (Standard) |

Der Compiler (`hemlockc`) prüft Ihren Code auf Typfehler, bevor er eine ausführbare Datei generiert, und erkennt Fehler frühzeitig.

## Grundlegende Syntax

### Variablen

```hemlock
// Variablen werden mit 'let' deklariert
let x = 42;
let name = "Alice";
let pi = 3.14159;

// Typannotationen sind optional
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**Wichtig**: Semikolons sind in Hemlock **obligatorisch**!

### Typen

Hemlock hat ein reichhaltiges Typsystem:

```hemlock
// Ganzzahlen
let small: i8 = 127;          // 8-Bit mit Vorzeichen
let byte: u8 = 255;           // 8-Bit ohne Vorzeichen
let num: i32 = 2147483647;    // 32-Bit mit Vorzeichen (Standard)
let big: i64 = 9223372036854775807;  // 64-Bit mit Vorzeichen

// Gleitkommazahlen
let f: f32 = 3.14;            // 32-Bit Gleitkomma
let d: f64 = 2.71828;         // 64-Bit Gleitkomma (Standard)

// Zeichenketten und Zeichen
let text: string = "Hallo";   // UTF-8-Zeichenkette
let emoji: rune = '🚀';       // Unicode-Codepunkt

// Boolean und null
let flag: bool = true;
let empty = null;
```

### Kontrollfluss

```hemlock
// If-Anweisungen
if (x > 0) {
    print("positiv");
} else if (x < 0) {
    print("negativ");
} else {
    print("null");
}

// While-Schleifen
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// For-Schleifen
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### Funktionen

```hemlock
// Benannte Funktion
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// Anonyme Funktion
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## Mit Zeichenketten arbeiten

Zeichenketten in Hemlock sind **veränderbar** und **UTF-8**:

```hemlock
let s = "hallo";
s[0] = 'H';              // Jetzt "Hallo"
print(s);

// Zeichenketten-Methoden
let upper = s.to_upper();     // "HALLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "all"

// Verkettung
let greeting = "Hallo" + ", " + "Welt!";
print(greeting);  // "Hallo, Welt!"
```

## Arrays

Dynamische Arrays mit gemischten Typen:

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Array-Methoden
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// Gemischte Typen erlaubt
let mixed = [1, "zwei", true, null];
```

## Objekte

JavaScript-ähnliche Objekte:

```hemlock
// Objekt-Literal
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // Feld ändern

// Methoden mit 'self'
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Speicherverwaltung

Hemlock verwendet **manuelle Speicherverwaltung**:

```hemlock
// Sicherer Puffer (empfohlen)
let buf = buffer(64);   // 64 Bytes allokieren
buf[0] = 65;            // Erstes Byte auf 'A' setzen
print(buf[0]);          // 65
free(buf);              // Speicher freigeben

// Roher Zeiger (fortgeschritten)
let ptr = alloc(100);
memset(ptr, 0, 100);    // Mit Nullen füllen
free(ptr);
```

**Wichtig**: Sie müssen `free()` aufrufen, was Sie `alloc()`iert haben!

## Fehlerbehandlung

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
} finally {
    print("Fertig");
}
```

## Kommandozeilenargumente

Zugriff auf Programmargumente über das `args`-Array:

```hemlock
// script.hml
print("Skript:", args[0]);
print(`Argumente: ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  arg ${i}: ${args[i]}`);
    i = i + 1;
}
```

Ausführen mit:
```bash
./hemlock script.hml hallo welt
```

Ausgabe:
```
Skript: script.hml
Argumente: 2
  arg 1: hallo
  arg 2: welt
```

## Datei-I/O

```hemlock
// In Datei schreiben
let f = open("daten.txt", "w");
f.write("Hallo, Datei!");
f.close();

// Aus Datei lesen
let f2 = open("daten.txt", "r");
let content = f2.read();
print(content);  // "Hallo, Datei!"
f2.close();
```

## Was kommt als Nächstes?

Nachdem Sie nun die Grundlagen gesehen haben, erkunden Sie mehr:

- [Tutorial](tutorial.md) - Umfassende Schritt-für-Schritt-Anleitung
- [Sprachhandbuch](../language-guide/syntax.md) - Tiefer Einblick in alle Funktionen
- [Beispiele](../../examples/) - Praxisnahe Beispielprogramme
- [API-Referenz](../reference/builtins.md) - Vollständige API-Dokumentation

## Häufige Fallstricke

### Semikolons vergessen

```hemlock
// ❌ FEHLER: Semikolon fehlt
let x = 42
let y = 10

// ✅ KORREKT
let x = 42;
let y = 10;
```

### Speicherfreigabe vergessen

```hemlock
// ❌ SPEICHERLECK
let buf = buffer(100);
// ... buf verwenden ...
// Vergessen, free(buf) aufzurufen!

// ✅ KORREKT
let buf = buffer(100);
// ... buf verwenden ...
free(buf);
```

### Geschweifte Klammern sind erforderlich

```hemlock
// ❌ FEHLER: Geschweifte Klammern fehlen
if (x > 0)
    print("positiv");

// ✅ KORREKT
if (x > 0) {
    print("positiv");
}
```

## Hilfe erhalten

- Lesen Sie die [vollständige Dokumentation](../README.md)
- Schauen Sie sich das [Beispielverzeichnis](../../examples/) an
- Betrachten Sie [Testdateien](../../tests/) für Verwendungsmuster
- Melden Sie Probleme auf GitHub
