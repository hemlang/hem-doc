# String-API-Referenz

Vollständige Referenz für Hemlocks String-Typ und alle 19 String-Methoden.

---

## Übersicht

Strings in Hemlock sind **UTF-8-kodierte, veraenderbare, heap-allokierte** Sequenzen mit vollstaendiger Unicode-Unterstützung. Alle Operationen arbeiten mit **Codepoints** (Zeichen), nicht Bytes.

**Hauptmerkmale:**
- UTF-8-Kodierung (U+0000 bis U+10FFFF)
- Veraenderbar (kann Zeichen direkt ändern)
- Codepoint-basierte Indizierung
- 19 eingebaute Methoden
- Automatische Verkettung mit `+`-Operator

---

## String-Typ

**Typ:** `string`

**Eigenschaften:**
- `.length` - Anzahl der Codepoints (Zeichen)
- `.byte_length` - Anzahl der UTF-8-Bytes

**Literal-Syntax:** Doppelte Anführungszeichen `"text"`

**Beispiele:**
```hemlock
let s = "hello";
print(s.length);        // 5 (Codepoints)
print(s.byte_length);   // 5 (Bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (ein Codepoint)
print(emoji.byte_length);   // 4 (vier UTF-8-Bytes)
```

---

## Indizierung

Strings unterstützen Codepoint-basierte Indizierung mit `[]`:

**Lesezugriff:**
```hemlock
let s = "hello";
let ch = s[0];          // Gibt Rune 'h' zurück
```

**Schreibzugriff:**
```hemlock
let s = "hello";
s[0] = 'H';             // Mit Rune ändern (jetzt "Hello")
```

**UTF-8-Beispiel:**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (ein Codepoint)
print(text[3]);         // '!'
```

---

## Verkettung

Verwenden Sie den `+`-Operator um Strings und Runes zu verketten:

**String + String:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**String + Rune:**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Rune + String:**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**Mehrfache Verkettungen:**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## String-Eigenschaften

### .length

Gibt die Anzahl der Unicode-Codepoints (Zeichen) zurück.

**Typ:** `i32`

**Beispiele:**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (ein Codepoint)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 Emoji)
```

---

### .byte_length

Gibt die Anzahl der UTF-8-Bytes zurück.

**Typ:** `i32`

**Beispiele:**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 Byte pro ASCII-Zeichen)

let emoji = "🚀";
print(emoji.byte_length); // 4 (Emoji ist 4 UTF-8-Bytes)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 für Emoji)
```

---

## String-Methoden

### Teilstring & Slicing

#### substr

Extrahiert Teilstring nach Position und Länge.

**Signatur:**
```hemlock
string.substr(start: i32, length: i32): string
```

**Parameter:**
- `start` - Start-Codepoint-Index (nullbasiert)
- `length` - Anzahl der zu extrahierenden Codepoints

**Rückgabe:** Neuer String

**Beispiele:**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// UTF-8-Beispiel
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

Extrahiert Teilstring nach Bereich (Ende exklusiv).

**Signatur:**
```hemlock
string.slice(start: i32, end: i32): string
```

**Parameter:**
- `start` - Start-Codepoint-Index (nullbasiert)
- `end` - End-Codepoint-Index (exklusiv)

**Rückgabe:** Neuer String

**Beispiele:**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// UTF-8-Beispiel
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### Suchen & Finden

#### find

Findet erstes Vorkommen eines Teilstrings.

**Signatur:**
```hemlock
string.find(needle: string): i32
```

**Parameter:**
- `needle` - Zu suchender Teilstring

**Rückgabe:** Codepoint-Index des ersten Vorkommens, oder `-1` wenn nicht gefunden

**Beispiele:**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (nicht gefunden)
let pos3 = s.find("l");         // 2 (erstes 'l')
```

---

#### contains

Prueft ob String Teilstring enthält.

**Signatur:**
```hemlock
string.contains(needle: string): bool
```

**Parameter:**
- `needle` - Zu suchender Teilstring

**Rückgabe:** `true` wenn gefunden, `false` sonst

**Beispiele:**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### Teilen & Verbinden

#### split

Teilt String in Array nach Trennzeichen.

**Signatur:**
```hemlock
string.split(delimiter: string): array
```

**Parameter:**
- `delimiter` - String zum Teilen

**Rückgabe:** Array von Strings

**Beispiele:**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

Entfernt führende und nachfolgende Leerzeichen.

**Signatur:**
```hemlock
string.trim(): string
```

**Rückgabe:** Neuer String ohne Leerzeichen

**Beispiele:**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

---

### Groß-/Kleinschreibung

#### to_upper

Konvertiert String zu Grossbuchstaben.

**Signatur:**
```hemlock
string.to_upper(): string
```

**Rückgabe:** Neuer String in Grossbuchstaben

**Beispiele:**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

Konvertiert String zu Kleinbuchstaben.

**Signatur:**
```hemlock
string.to_lower(): string
```

**Rückgabe:** Neuer String in Kleinbuchstaben

**Beispiele:**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### Präfix & Suffix

#### starts_with

Prueft ob String mit Präfix beginnt.

**Signatur:**
```hemlock
string.starts_with(prefix: string): bool
```

**Parameter:**
- `prefix` - Zu pruefendes Präfix

**Rückgabe:** `true` wenn String mit Präfix beginnt, `false` sonst

**Beispiele:**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

Prueft ob String mit Suffix endet.

**Signatur:**
```hemlock
string.ends_with(suffix: string): bool
```

**Parameter:**
- `suffix` - Zu pruefendes Suffix

**Rückgabe:** `true` wenn String mit Suffix endet, `false` sonst

**Beispiele:**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### Ersetzen

#### replace

Ersetzt erstes Vorkommen eines Teilstrings.

**Signatur:**
```hemlock
string.replace(old: string, new: string): string
```

**Parameter:**
- `old` - Zu ersetzender Teilstring
- `new` - Ersetzungsstring

**Rückgabe:** Neuer String mit erstem Vorkommen ersetzt

**Beispiele:**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (nur erstes)
```

---

#### replace_all

Ersetzt alle Vorkommen eines Teilstrings.

**Signatur:**
```hemlock
string.replace_all(old: string, new: string): string
```

**Parameter:**
- `old` - Zu ersetzender Teilstring
- `new` - Ersetzungsstring

**Rückgabe:** Neuer String mit allen Vorkommen ersetzt

**Beispiele:**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### Wiederholung

#### repeat

Wiederholt String n-mal.

**Signatur:**
```hemlock
string.repeat(count: i32): string
```

**Parameter:**
- `count` - Anzahl der Wiederholungen

**Rückgabe:** Neuer String count-mal wiederholt

**Beispiele:**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### Zeichenzugriff

#### char_at

Gibt Unicode-Codepoint am Index zurück.

**Signatur:**
```hemlock
string.char_at(index: i32): rune
```

**Parameter:**
- `index` - Codepoint-Index (nullbasiert)

**Rückgabe:** Rune (Unicode-Codepoint)

**Beispiele:**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// UTF-8-Beispiel
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (Rakete)
```

---

#### chars

Konvertiert String zu Array von Runes.

**Signatur:**
```hemlock
string.chars(): array
```

**Rückgabe:** Array von Runes (Codepoints)

**Beispiele:**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// UTF-8-Beispiel
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### Byte-Zugriff

#### byte_at

Gibt Byte-Wert am Index zurück.

**Signatur:**
```hemlock
string.byte_at(index: i32): u8
```

**Parameter:**
- `index` - Byte-Index (nullbasiert, NICHT Codepoint-Index)

**Rückgabe:** Byte-Wert (u8)

**Beispiele:**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// UTF-8-Beispiel
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (erstes UTF-8-Byte)
```

---

#### bytes

Konvertiert String zu Array von Bytes.

**Signatur:**
```hemlock
string.bytes(): array
```

**Rückgabe:** Array von u8-Bytes

**Beispiele:**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// UTF-8-Beispiel
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 UTF-8-Bytes)
```

---

#### to_bytes

Konvertiert String zu Buffer.

**Signatur:**
```hemlock
string.to_bytes(): buffer
```

**Rückgabe:** Buffer mit UTF-8-Bytes

**Beispiele:**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// UTF-8-Beispiel
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Hinweis:** Dies ist eine Legacy-Methode. Bevorzugen Sie `.bytes()` für die meisten Anwendungsfaelle.

---

### JSON-Deserialisierung

#### deserialize

Parst JSON-String zu Wert.

**Signatur:**
```hemlock
string.deserialize(): any
```

**Rückgabe:** Geparster Wert (Objekt, Array, Zahl, String, Bool oder null)

**Beispiele:**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**Unterstuetzte Typen:**
- Objekte: `{"key": value}`
- Arrays: `[1, 2, 3]`
- Zahlen: `42`, `3.14`
- Strings: `"text"`
- Booleans: `true`, `false`
- Null: `null`

**Siehe auch:** Objekt `.serialize()`-Methode

---

## Methoden-Verkettung

String-Methoden können für praegnante Operationen verkettet werden:

**Beispiele:**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## Vollständige Methodenuebersicht

| Methode        | Signatur                                     | Rückgabe | Beschreibung                          |
|----------------|----------------------------------------------|-----------|---------------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`  | Teilstring nach Position/Länge extrahieren |
| `slice`        | `(start: i32, end: i32)`                     | `string`  | Teilstring nach Bereich extrahieren   |
| `find`         | `(needle: string)`                           | `i32`     | Erstes Vorkommen finden (-1 wenn nicht gefunden) |
| `contains`     | `(needle: string)`                           | `bool`    | Prüfen ob Teilstring enthalten       |
| `split`        | `(delimiter: string)`                        | `array`   | In Array teilen                       |
| `trim`         | `()`                                         | `string`  | Leerzeichen entfernen                 |
| `to_upper`     | `()`                                         | `string`  | Zu Grossbuchstaben konvertieren       |
| `to_lower`     | `()`                                         | `string`  | Zu Kleinbuchstaben konvertieren       |
| `starts_with`  | `(prefix: string)`                           | `bool`    | Prüfen ob mit Präfix beginnt        |
| `ends_with`    | `(suffix: string)`                           | `bool`    | Prüfen ob mit Suffix endet           |
| `replace`      | `(old: string, new: string)`                 | `string`  | Erstes Vorkommen ersetzen             |
| `replace_all`  | `(old: string, new: string)`                 | `string`  | Alle Vorkommen ersetzen               |
| `repeat`       | `(count: i32)`                               | `string`  | String n-mal wiederholen              |
| `char_at`      | `(index: i32)`                               | `rune`    | Codepoint am Index holen              |
| `byte_at`      | `(index: i32)`                               | `u8`      | Byte am Index holen                   |
| `chars`        | `()`                                         | `array`   | Zu Array von Runes konvertieren       |
| `bytes`        | `()`                                         | `array`   | Zu Array von Bytes konvertieren       |
| `to_bytes`     | `()`                                         | `buffer`  | Zu Buffer konvertieren (Legacy)       |
| `deserialize`  | `()`                                         | `any`     | JSON-String parsen                    |

---

## Siehe auch

- [Typsystem](type-system.md) - String-Typ-Details
- [Array-API](array-api.md) - Array-Methoden für split()-Ergebnisse
- [Operatoren](operators.md) - String-Verkettungsoperator
