# Runes

Runes repraesentieren **Unicode-Codepoints** (U+0000 bis U+10FFFF) als eigenstaendigen Typ fuer Zeichenmanipulation in Hemlock. Im Gegensatz zu Bytes (u8) sind Runes vollstaendige Unicode-Zeichen, die jedes Zeichen in jeder Sprache oder Emoji darstellen koennen.

## Ueberblick

```hemlock
let ch = 'A';           // Rune-Literal
let emoji = '🚀';       // Multi-Byte-Zeichen als einzelne Rune
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // String + Rune Verkettung
let r = '>' + " msg";   // Rune + String Verkettung
```

## Was ist eine Rune?

Eine Rune ist ein **32-Bit-Wert**, der einen Unicode-Codepoint repraesentiert:

- **Bereich:** 0 bis 0x10FFFF (1.114.111 gueltige Codepoints)
- **Kein numerischer Typ** - Wird fuer Zeichendarstellung verwendet
- **Unterschiedlich von u8/char** - Runes sind volles Unicode, u8 sind nur Bytes
- **Von String-Indexierung zurueckgegeben** - `str[0]` gibt eine Rune zurueck, kein Byte

**Warum Runes?**
- Hemlock-Strings sind UTF-8-kodiert
- Ein einzelnes Unicode-Zeichen kann 1-4 Bytes in UTF-8 sein
- Runes ermoeglichen die Arbeit mit vollstaendigen Zeichen, nicht mit Teilbytes

## Rune-Literale

### Grundlegende Syntax

Einfache Anfuehrungszeichen kennzeichnen Rune-Literale:

```hemlock
let a = 'A';            // ASCII-Zeichen
let b = '0';            // Ziffernzeichen
let c = '!';            // Satzzeichen
let d = ' ';            // Leerzeichen
```

### Multi-Byte UTF-8 Zeichen

Runes koennen jedes Unicode-Zeichen darstellen:

```hemlock
// Emoji
let rocket = '🚀';      // Emoji (U+1F680)
let heart = '❤';        // Herz (U+2764)
let smile = '😀';       // Grinsendes Gesicht (U+1F600)

// CJK-Zeichen
let chinese = '中';     // Chinesisch (U+4E2D)
let japanese = 'あ';    // Hiragana (U+3042)
let korean = '한';      // Hangul (U+D55C)

// Symbole
let check = '✓';        // Haekchen (U+2713)
let arrow = '→';        // Pfeil nach rechts (U+2192)
```

### Escape-Sequenzen

Gaengige Escape-Sequenzen fuer Sonderzeichen:

```hemlock
let newline = '\n';     // Zeilenumbruch (U+000A)
let tab = '\t';         // Tabulator (U+0009)
let backslash = '\\';   // Backslash (U+005C)
let quote = '\'';       // Einfaches Anfuehrungszeichen (U+0027)
let dquote = '"';       // Doppeltes Anfuehrungszeichen (U+0022)
let null_char = '\0';   // Null-Zeichen (U+0000)
let cr = '\r';          // Wagenruecklauf (U+000D)
```

**Verfuegbare Escape-Sequenzen:**
- `\n` - Zeilenumbruch (Line Feed)
- `\t` - Horizontaler Tabulator
- `\r` - Wagenruecklauf
- `\0` - Null-Zeichen
- `\\` - Backslash
- `\'` - Einfaches Anfuehrungszeichen
- `\"` - Doppeltes Anfuehrungszeichen

### Unicode-Escapes

Verwenden Sie `\u{XXXXXX}`-Syntax fuer Unicode-Codepoints (bis zu 6 Hex-Ziffern):

```hemlock
let rocket = '\u{1F680}';   // 🚀 Emoji via Unicode-Escape
let heart = '\u{2764}';     // ❤ Herz
let ascii = '\u{41}';       // 'A' via Escape
let max = '\u{10FFFF}';     // Maximaler Unicode-Codepoint

// Fuehrende Nullen optional
let a = '\u{41}';           // Gleich wie '\u{0041}'
let b = '\u{0041}';
```

**Regeln:**
- Bereich: `\u{0}` bis `\u{10FFFF}`
- Hex-Ziffern: 1 bis 6 Ziffern
- Gross-/Kleinschreibung egal: `\u{1F680}` oder `\u{1f680}`
- Werte ausserhalb des gueltigen Unicode-Bereichs verursachen Fehler

## String + Rune Verkettung

Runes koennen mit Strings verkettet werden:

```hemlock
// String + Rune
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Text" + '✓';       // "Text✓"

// Rune + String
let prefix = '>' + " Nachricht";    // "> Nachricht"
let bullet = '•' + " Element";      // "• Element"

// Mehrfache Verkettungen
let msg = "Hi " + '👋' + " Welt " + '🌍';  // "Hi 👋 Welt 🌍"

// Method-Chaining funktioniert
let result = ('>' + " Wichtig").to_upper();  // "> WICHTIG"
```

**Wie es funktioniert:**
- Runes werden automatisch in UTF-8 kodiert
- Waehrend der Verkettung in Strings konvertiert
- Der String-Verkettungsoperator behandelt dies transparent

## Typkonvertierungen

Runes koennen in/von anderen Typen konvertiert werden.

### Integer <-> Rune

Konvertieren zwischen Integers und Runes um mit Codepoint-Werten zu arbeiten:

```hemlock
// Integer zu Rune (Codepoint-Wert)
let code: rune = 65;            // 'A' (ASCII 65)
let emoji_code: rune = 128640;  // U+1F680 (🚀)

// Rune zu Integer (Codepoint-Wert erhalten)
let r = 'Z';
let value: i32 = r;             // 90 (ASCII-Wert)

let rocket = '🚀';
let code: i32 = rocket;         // 128640 (U+1F680)
```

**Bereichspruefung:**
- Integer zu Rune: Muss in [0, 0x10FFFF] sein
- Werte ausserhalb des Bereichs verursachen Laufzeitfehler
- Rune zu Integer: Funktioniert immer (gibt Codepoint zurueck)

### Rune -> String

Runes koennen explizit in Strings konvertiert werden:

```hemlock
// Explizite Konvertierung
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// Automatisch waehrend Verkettung
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8 (Byte) -> Rune

Jeder u8-Wert (0-255) kann in Rune konvertiert werden:

```hemlock
// ASCII-Bereich (0-127)
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// Erweitertes ASCII / Latin-1 (128-255)
let extended: u8 = 200;
let r: rune = extended;         // U+00C8 (E)

// Hinweis: Werte 0-127 sind ASCII, 128-255 sind Latin-1
```

### Verkettete Konvertierungen

Typkonvertierungen koennen verkettet werden:

```hemlock
// i32 -> Rune -> String
let code: i32 = 128512;         // Grinsendes Gesicht Codepoint
let r: rune = code;             // 😀
let s: string = r;              // "😀"

// Alles in einem Ausdruck
let emoji: string = 128640;     // Implizit i32 -> Rune -> String (🚀)
```

## Rune-Operationen

### Ausgabe

Wie Runes angezeigt werden haengt vom Codepoint ab:

```hemlock
let ascii = 'A';
print(ascii);                   // 'A' (in Anfuehrungszeichen, druckbares ASCII)

let emoji = '🚀';
print(emoji);                   // U+1F680 (Unicode-Notation fuer Nicht-ASCII)

let tab = '\t';
print(tab);                     // U+0009 (nicht-druckbar als Hex)

let space = ' ';
print(space);                   // ' ' (druckbar)
```

**Ausgabeformat:**
- Druckbares ASCII (32-126): Zeichen in Anfuehrungszeichen `'A'`
- Nicht-druckbar oder Unicode: Hex-Notation `U+XXXX`

### Typpruefung

Verwenden Sie `typeof()` um zu pruefen ob ein Wert eine Rune ist:

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "text";
let ch = s[0];
print(typeof(ch));              // "rune" (Indexierung gibt Runes zurueck)

let num = 65;
print(typeof(num));             // "i32"
```

### Vergleich

Runes koennen auf Gleichheit verglichen werden:

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// Gross-/Kleinschreibung sensitiv
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// Runes koennen mit Integers verglichen werden (Codepoint-Werte)
print(a == 65);                 // true (implizite Konvertierung)
print('🚀' == 128640);          // true
```

**Vergleichsoperatoren:**
- `==` - Gleich
- `!=` - Ungleich
- `<`, `>`, `<=`, `>=` - Codepoint-Reihenfolge

```hemlock
print('A' < 'B');               // true (65 < 66)
print('a' > 'Z');               // true (97 > 90)
```

## Arbeiten mit String-Indexierung

String-Indexierung gibt Runes zurueck, keine Bytes:

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H' (Rune)
let rocket = s[5];              // '🚀' (Rune)

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// Bei Bedarf in String konvertieren
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "🚀"
```

**Wichtig:** String-Indexierung verwendet Codepoint-Positionen, keine Byte-Offsets:

```hemlock
let text = "Hi🚀!";
// Codepoint-Positionen: 0='H', 1='i', 2='🚀', 3='!'
// Byte-Positionen:      0='H', 1='i', 2-5='🚀', 6='!'

let r = text[2];                // '🚀' (Codepoint 2)
print(typeof(r));               // "rune"
```

## Beispiele

### Beispiel: Zeichenklassifikation

```hemlock
fn is_digit(r: rune): bool {
    return r >= '0' && r <= '9';
}

fn is_upper(r: rune): bool {
    return r >= 'A' && r <= 'Z';
}

fn is_lower(r: rune): bool {
    return r >= 'a' && r <= 'z';
}

print(is_digit('5'));           // true
print(is_upper('A'));           // true
print(is_lower('z'));           // true
```

### Beispiel: Gross-/Kleinschreibung Konvertierung

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // In Grossbuchstaben konvertieren (32 subtrahieren)
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // In Kleinbuchstaben konvertieren (32 addieren)
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### Beispiel: Zeichen-Iteration

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Position " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Hi🚀");
// Position 0: 'H'
// Position 1: 'i'
// Position 2: U+1F680
```

### Beispiel: Strings aus Runes bauen

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let result = "";
    let i = 0;
    while (i < count) {
        result = result + ch;
        i = i + 1;
    }
    return result;
}

let line = repeat_char('=', 40);  // "========================================"
let stars = repeat_char('⭐', 5);  // "⭐⭐⭐⭐⭐"
```

## Gaengige Muster

### Muster: Zeichenfilter

```hemlock
fn filter_digits(s: string): string {
    let result = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}

let text = "abc123def456";
let digits = filter_digits(text);  // "123456"
```

### Muster: Zeichen zaehlen

```hemlock
fn count_char(s: string, target: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == target) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let text = "hello world";
let l_count = count_char(text, 'l');  // 3
let o_count = count_char(text, 'o');  // 2
```

## Best Practices

1. **Runes fuer Zeichenoperationen verwenden** - Versuchen Sie nicht mit Bytes fuer Text zu arbeiten
2. **String-Indexierung gibt Runes zurueck** - Denken Sie daran dass `str[i]` Ihnen eine Rune gibt
3. **Unicode-bewusste Vergleiche** - Runes behandeln jedes Unicode-Zeichen
4. **Bei Bedarf konvertieren** - Runes konvertieren einfach in Strings und Integers
5. **Mit Emoji testen** - Testen Sie Zeichenoperationen immer mit Multi-Byte-Zeichen

## Haeufige Fallstricke

### Fallstrick: Rune vs. Byte Verwechslung

```hemlock
// NICHT: Runes als Bytes behandeln
let r: rune = '🚀';
let b: u8 = r;              // FEHLER: Rune-Codepoint 128640 passt nicht in u8

// RICHTIG: Passende Konvertierungen verwenden
let r: rune = '🚀';
let code: i32 = r;          // OK: 128640
```

### Fallstrick: String Byte-Indexierung

```hemlock
// NICHT: Byte-Indexierung annehmen
let s = "🚀";
let byte = s.byte_at(0);    // 240 (erstes UTF-8 Byte, nicht vollstaendiges Zeichen)

// RICHTIG: Codepoint-Indexierung verwenden
let s = "🚀";
let rune = s[0];            // '🚀' (vollstaendiges Zeichen)
let rune2 = s.char_at(0);   // '🚀' (explizite Methode)
```

## Verwandte Themen

- [Strings](strings.md) - String-Operationen und UTF-8-Behandlung
- [Types](types.md) - Typsystem und Konvertierungen
- [Control Flow](control-flow.md) - Verwendung von Runes in Vergleichen

## Siehe auch

- **Unicode-Standard**: Unicode-Codepoints werden vom Unicode Consortium definiert
- **UTF-8-Kodierung**: Siehe [Strings](strings.md) fuer UTF-8-Details
- **Typkonvertierungen**: Siehe [Types](types.md) fuer Konvertierungsregeln
