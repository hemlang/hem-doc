# Strings

Hemlock-Strings sind **UTF-8 erstklassige veraenderbare Sequenzen** mit voller Unicode-Unterstützung und einem umfangreichen Satz von Methoden zur Textverarbeitung. Anders als in vielen Sprachen sind Hemlock-Strings veraenderbar und arbeiten nativ mit Unicode-Codepoints.

## Überblick

```hemlock
let s = "hello";
s[0] = 'H';             // veraendern mit Rune (jetzt "Hello")
print(s.length);        // 5 (Codepoint-Anzahl)
let c = s[0];           // gibt Rune zurück (Unicode-Codepoint)
let msg = s + " world"; // Verkettung
let emoji = "🚀";
print(emoji.length);    // 1 (ein Codepoint)
print(emoji.byte_length); // 4 (vier UTF-8-Bytes)
```

## Eigenschaften

Hemlock-Strings haben diese Hauptmerkmale:

- **UTF-8-kodiert** - Volle Unicode-Unterstützung (U+0000 bis U+10FFFF)
- **Veraenderbar** - Anders als Python-, JavaScript- und Java-Strings
- **Codepoint-basierte Indizierung** - Gibt `rune` (Unicode-Codepoint) zurück, nicht Byte
- **Heap-allokiert** - Mit interner Kapazitaetsverfolgung
- **Zwei Längeneigenschaften**:
  - `.length` - Codepoint-Anzahl (Anzahl der Zeichen)
  - `.byte_length` - Byte-Anzahl (UTF-8-Kodierungsgroesse)

## UTF-8-Verhalten

Alle String-Operationen arbeiten mit **Codepoints** (Zeichen), nicht mit Bytes:

```hemlock
let text = "Hello🚀World";
print(text.length);        // 11 (Codepoints)
print(text.byte_length);   // 15 (Bytes, Emoji ist 4 Bytes)

// Indizierung verwendet Codepoints
let h = text[0];           // 'H' (Rune)
let rocket = text[5];      // '🚀' (Rune)
```

**Mehrbyte-Zeichen zaehlen als eins:**
```hemlock
"Hello".length;      // 5
"🚀".length;         // 1 (ein Emoji)
"你好".length;       // 2 (zwei chinesische Zeichen)
"café".length;       // 4 (é ist ein Codepoint)
```

## String-Literale

```hemlock
// Einfache Strings
let s1 = "hello";
let s2 = "world";

// Mit Escape-Sequenzen
let s3 = "Zeile 1\nZeile 2\teingerueckt";
let s4 = "Zitat: \"Hallo\"";
let s5 = "Backslash: \\";

// Unicode-Zeichen
let s6 = "🚀 Emoji";
let s7 = "中文字符";
```

## Template-Strings (String-Interpolation)

Verwenden Sie Backticks für Template-Strings mit eingebetteten Ausdrücken:

```hemlock
let name = "Alice";
let age = 30;

// Einfache Interpolation
let greeting = `Hallo, ${name}!`;           // "Hallo, Alice!"
let info = `${name} ist ${age} Jahre alt`;  // "Alice ist 30 Jahre alt"

// Ausdrücke in der Interpolation
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// Methodenaufrufe
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// Verschachtelte Objekte
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lebt in ${person.city}`;  // "Bob lebt in NYC"

// Mehrzeilig (behält Zeilenumbrueche bei)
let multi = `Zeile 1
Zeile 2
Zeile 3`;
```

**Template-String-Funktionen:**
- Ausdrücke innerhalb von `${...}` werden ausgewertet und in Strings konvertiert
- Jeder gueltige Ausdruck kann verwendet werden (Variablen, Funktionsaufrufe, Arithmetik)
- Backtick-Strings unterstützen dieselben Escape-Sequenzen wie reguläre Strings
- Nützlich zum Erstellen dynamischer Strings ohne Verkettung

### Escaping in Template-Strings

Um ein literales `${` in einem Template-String einzufuegen, escapen Sie das Dollarzeichen:

```hemlock
let price = 100;
let text = `Preis: \${price} oder ${price}`;
// "Preis: ${price} oder 100"

// Literaler Backtick
let code = `Verwende \` für Template-Strings`;
// "Verwende ` für Template-Strings"
```

### Komplexe Ausdrücke

Template-Strings können jeden gueltigen Ausdruck enthalten:

```hemlock
// Ternaer-ähnliche Ausdrücke
let age = 25;
let status = `Status: ${age >= 18 ? "erwachsen" : "minderjaehrig"}`;

// Array-Zugriff
let items = ["Apfel", "Banane", "Kirsche"];
let first = `Erstes Element: ${items[0]}`;

// Funktionsaufrufe mit Argumenten
fn format_price(p) { return p + " EUR"; }
let msg = `Gesamt: ${format_price(99.99)}`;  // "Gesamt: 99.99 EUR"

// Verkettete Methodenaufrufe
let name = "alice";
let formatted = `Hallo, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hallo, Alice!"
```

### Template-Strings vs. Verkettung

Template-Strings sind oft sauberer als Verkettung:

```hemlock
// Verkettung (schwerer zu lesen)
let msg1 = "Hallo, " + name + "! Du hast " + count + " Nachrichten.";

// Template-String (leichter zu lesen)
let msg2 = `Hallo, ${name}! Du hast ${count} Nachrichten.`;
```

## Indizierung und Veraenderung

### Zeichen lesen

Indizierung gibt eine `rune` (Unicode-Codepoint) zurück:

```hemlock
let s = "Hello";
let first = s[0];      // 'H' (Rune)
let last = s[4];       // 'o' (Rune)

// UTF-8-Beispiel
let emoji = "Hi🚀!";
let rocket = emoji[2];  // '🚀' (Rune an Codepoint-Index 2)
```

### Zeichen schreiben

Strings sind veraenderbar - Sie können einzelne Zeichen modifizieren:

```hemlock
let s = "hello";
s[0] = 'H';            // Jetzt "Hello"
s[4] = '!';            // Jetzt "Hell!"

// Mit Unicode
let msg = "Go!";
msg[0] = '🚀';         // Jetzt "🚀o!"
```

## Verkettung

Verwenden Sie `+` um Strings zu verketten:

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// Mit Variablen
let name = "Alice";
let msg = "Hallo, " + name + "!";  // "Hallo, Alice!"

// Mit Runen (siehe Runes-Dokumentation)
let s = "Hello" + '!';          // "Hello!"
```

## String-Methoden

Hemlock bietet 19 String-Methoden für umfassende Textmanipulation.

### Teilstring & Slicing

**`substr(start, length)`** - Teilstring nach Position und Länge extrahieren:
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world" (Start bei 6, Länge 5)
let first = s.substr(0, 5);     // "hello"

// UTF-8-Beispiel
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀" (Position 2, Länge 1)
```

**`slice(start, end)`** - Teilstring nach Bereich extrahieren (Ende exklusiv):
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello" (Index 0 bis 4)
let slice2 = s.slice(6, 11);    // "world"
```

**Unterschied:**
- `substr(start, length)` - Verwendet Laengenparameter
- `slice(start, end)` - Verwendet Endindex (exklusiv)

### Suchen & Finden

**`find(needle)`** - Erstes Vorkommen finden:
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6 (Index des ersten Vorkommens)
let pos2 = s.find("foo");       // -1 (nicht gefunden)
let pos3 = s.find("l");         // 2 (erstes 'l')
```

**`contains(needle)`** - Prüfen, ob String Teilstring enthält:
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### Aufteilen & Trimmen

**`split(delimiter)`** - In Array von Strings aufteilen:
```hemlock
let csv = "Apfel,Banane,Kirsche";
let parts = csv.split(",");     // ["Apfel", "Banane", "Kirsche"]

let words = "eins zwei drei".split(" ");  // ["eins", "zwei", "drei"]

// Leerer Delimiter teilt nach Zeichen
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Führende/nachfolgende Leerzeichen entfernen:
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### Groß-/Kleinschreibung

**`to_upper()`** - In Grossbuchstaben umwandeln:
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// Behaelt Nicht-ASCII bei
let s2 = "café";
let upper2 = s2.to_upper();     // "CAFÉ"
```

**`to_lower()`** - In Kleinbuchstaben umwandeln:
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### Präfix-/Suffix-Prüfung

**`starts_with(prefix)`** - Prüfen, ob mit Präfix beginnt:
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - Prüfen, ob mit Suffix endet:
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### Ersetzen

**`replace(old, new)`** - Erstes Vorkommen ersetzen:
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (nur erstes)
```

**`replace_all(old, new)`** - Alle Vorkommen ersetzen:
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### Wiederholung

**`repeat(count)`** - String n-mal wiederholen:
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### Zeichen- & Byte-Zugriff

**`char_at(index)`** - Unicode-Codepoint an Index abrufen (gibt Rune zurück):
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h' (Rune)

// UTF-8-Beispiel
let emoji = "🚀";
let rocket = emoji.char_at(0);  // Gibt Rune U+1F680 zurück
```

**`chars()`** - In Array von Runen (Codepoints) umwandeln:
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o'] (Array von Runen)

// UTF-8-Beispiel
let text = "Hi🚀";
let chars2 = text.chars();      // ['H', 'i', '🚀']
```

**`byte_at(index)`** - Byte-Wert an Index abrufen (gibt u8 zurück):
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII-Wert von 'h')

// UTF-8-Beispiel
let emoji = "🚀";
let first_byte = emoji.byte_at(0);  // 240 (erstes UTF-8-Byte)
```

**`bytes()`** - In Array von Bytes (u8-Werte) umwandeln:
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111] (Array von u8)

// UTF-8-Beispiel
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 UTF-8-Bytes)
```

**`to_bytes()`** - In Buffer für Low-Level-Zugriff umwandeln:
```hemlock
let s = "hello";
let buf = s.to_bytes();         // Gibt Buffer mit UTF-8-Bytes zurück
print(buf.length);              // 5
free(buf);                      // Nicht vergessen freizugeben
```

## Methodenverkettung

Alle String-Methoden geben neue Strings zurück, was Verkettung ermöglicht:

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## Vollständige Methodenreferenz

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|-----------|--------------|
| `substr(start, length)` | i32, i32 | string | Teilstring nach Position und Länge extrahieren |
| `slice(start, end)` | i32, i32 | string | Teilstring nach Bereich extrahieren (Ende exklusiv) |
| `find(needle)` | string | i32 | Erstes Vorkommen finden (-1 wenn nicht gefunden) |
| `contains(needle)` | string | bool | Prüfen, ob Teilstring enthalten ist |
| `split(delimiter)` | string | array | In Array von Strings aufteilen |
| `trim()` | - | string | Führende/nachfolgende Leerzeichen entfernen |
| `to_upper()` | - | string | In Grossbuchstaben umwandeln |
| `to_lower()` | - | string | In Kleinbuchstaben umwandeln |
| `starts_with(prefix)` | string | bool | Prüfen, ob mit Präfix beginnt |
| `ends_with(suffix)` | string | bool | Prüfen, ob mit Suffix endet |
| `replace(old, new)` | string, string | string | Erstes Vorkommen ersetzen |
| `replace_all(old, new)` | string, string | string | Alle Vorkommen ersetzen |
| `repeat(count)` | i32 | string | String n-mal wiederholen |
| `char_at(index)` | i32 | rune | Codepoint an Index abrufen |
| `byte_at(index)` | i32 | u8 | Byte-Wert an Index abrufen |
| `chars()` | - | array | In Array von Runen umwandeln |
| `bytes()` | - | array | In Array von u8-Bytes umwandeln |
| `to_bytes()` | - | buffer | In Buffer umwandeln (muss freigegeben werden) |

## Beispiele

### Beispiel: Textverarbeitung

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Leerzeichen normalisieren
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### Beispiel: CSV-Parser

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "Apfel, Banane , Kirsche";
let fields = parse_csv_line(csv);  // ["Apfel", "Banane", "Kirsche"]
```

### Beispiel: Wörter zaehlen

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "Der schnelle braune Fuchs";
let count = count_words(sentence);  // 4
```

### Beispiel: String-Validierung

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("ungültig"));         // false
```

## Speicherverwaltung

Strings sind heap-allokiert mit interner Referenzzaehlung:

- **Erstellung**: Auf dem Heap allokiert mit Kapazitaetsverfolgung
- **Verkettung**: Erzeugt neuen String (alte Strings unverändert)
- **Methoden**: Die meisten Methoden geben neue Strings zurück
- **Lebensdauer**: Strings sind referenzgezählt und werden automatisch freigegeben, wenn der Gültigkeitsbereich endet

**Automatische Bereinigung:**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // Neue Allokation
}  // Sowohl s als auch s2 werden automatisch freigegeben, wenn die Funktion zurückkehrt
```

**Hinweis:** Lokale String-Variablen werden automatisch bereinigt, wenn sie den Gültigkeitsbereich verlassen. Verwenden Sie `free()` nur für fruehe Bereinigung vor Bereichsende oder für langlebige/globale Daten. Siehe [Speicherverwaltung](memory.md#internal-reference-counting) für Details.

## Best Practices

1. **Codepoint-Indizierung verwenden** - Strings verwenden Codepoint-Positionen, nicht Byte-Offsets
2. **Mit Unicode testen** - String-Operationen immer mit Mehrbyte-Zeichen testen
3. **Unveränderliche Operationen bevorzugen** - Methoden verwenden, die neue Strings zurückgeben, statt Mutation
4. **Grenzen prüfen** - String-Indizierung führt keine Grenzprüfung durch (gibt null/Fehler bei ungültig zurück)
5. **Eingabe normalisieren** - `trim()` und `to_lower()` für Benutzereingaben verwenden

## Häufige Fallstricke

### Fallstrick: Byte vs. Codepoint-Verwirrung

```hemlock
let emoji = "🚀";
print(emoji.length);        // 1 (Codepoint)
print(emoji.byte_length);   // 4 (Bytes)

// Byte- und Codepoint-Operationen nicht mischen
let byte = emoji.byte_at(0);  // 240 (erstes Byte)
let char = emoji.char_at(0);  // '🚀' (vollstaendiger Codepoint)
```

### Fallstrick: Mutations-Ueberraschungen

```hemlock
let s1 = "hello";
let s2 = s1;       // Flache Kopie
s1[0] = 'H';       // Veraendert s1
print(s2);         // Immer noch "hello" (Strings sind Werttypen)
```

## Verwandte Themen

- [Runes](runes.md) - Unicode-Codepoint-Typ, der bei String-Indizierung verwendet wird
- [Arrays](arrays.md) - String-Methoden geben oft Arrays zurück oder arbeiten mit ihnen
- [Types](types.md) - String-Typ-Details und Konvertierungen

## Siehe auch

- **UTF-8-Kodierung**: Siehe CLAUDE.md Abschnitt "Strings"
- **Typkonvertierungen**: Siehe [Types](types.md) für String-Konvertierungen
- **Speicher**: Siehe [Memory](memory.md) für String-Allokationsdetails
