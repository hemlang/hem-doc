# Operatoren-Referenz

Vollständige Referenz für alle Operatoren in Hemlock, einschließlich Präzedenz, Assoziativitaet und Verhalten.

---

## Übersicht

Hemlock bietet C-ähnliche Operatoren mit expliziten Praezedenzregeln. Alle Operatoren folgen strikten Typisierungsregeln mit automatischer Typpromovierung wo anwendbar.

---

## Arithmetische Operatoren

### Binäre Arithmetik

| Operator | Name            | Beispiel   | Beschreibung               |
|----------|-----------------|------------|----------------------------|
| `+`      | Addition        | `a + b`    | Zwei Werte addieren        |
| `-`      | Subtraktion     | `a - b`    | b von a subtrahieren       |
| `*`      | Multiplikation  | `a * b`    | Zwei Werte multiplizieren  |
| `/`      | Division        | `a / b`    | a durch b dividieren       |

**Typpromovierung:**
Ergebnisse folgen Typpromovierungsregeln (siehe [Typsystem](type-system.md#type-promotion-rules)).

**Beispiele:**
```hemlock
let a = 10 + 5;        // 15 (i32)
let b = 10 - 3;        // 7 (i32)
let c = 4 * 5;         // 20 (i32)
let d = 20 / 4;        // 5 (i32)

// Gleitkomma-Division
let e = 10.0 / 3.0;    // 3.333... (f64)

// Gemischte Typen
let f: u8 = 10;
let g: i32 = 20;
let h = f + g;         // 30 (i32, promoviert)
```

**Division durch Null:**
- Ganzzahl-Division durch Null: Laufzeitfehler
- Gleitkomma-Division durch Null: Gibt `inf` oder `-inf` zurück

---

### Unaere Arithmetik

| Operator | Name     | Beispiel | Beschreibung          |
|----------|----------|----------|-----------------------|
| `-`      | Negation | `-a`     | Wert negieren         |
| `+`      | Plus     | `+a`     | Identität (keine Änderung) |

**Beispiele:**
```hemlock
let a = 5;
let b = -a;            // -5
let c = +a;            // 5 (keine Änderung)

let x = -3.14;         // -3.14
```

---

## Vergleichsoperatoren

| Operator | Name                    | Beispiel   | Rückgabe |
|----------|-------------------------|------------|-----------|
| `==`     | Gleich                  | `a == b`   | `bool`    |
| `!=`     | Ungleich                | `a != b`   | `bool`    |
| `<`      | Kleiner als             | `a < b`    | `bool`    |
| `>`      | Größer als            | `a > b`    | `bool`    |
| `<=`     | Kleiner oder gleich     | `a <= b`   | `bool`    |
| `>=`     | Größer oder gleich    | `a >= b`   | `bool`    |

**Typpromovierung:**
Operanden werden vor Vergleich promoviert.

**Beispiele:**
```hemlock
print(5 == 5);         // true
print(10 != 5);        // true
print(3 < 7);          // true
print(10 > 5);         // true
print(5 <= 5);         // true
print(10 >= 5);        // true

// String-Vergleich
print("hello" == "hello");  // true
print("abc" < "def");       // true (lexikografisch)

// Gemischte Typen
let a: u8 = 10;
let b: i32 = 10;
print(a == b);         // true (auf i32 promoviert)
```

---

## Logische Operatoren

| Operator | Name         | Beispiel     | Beschreibung              |
|----------|--------------|--------------|---------------------------|
| `&&`     | Logisches UND| `a && b`     | Wahr wenn beide wahr      |
| `||`     | Logisches ODER| `a || b`    | Wahr wenn einer wahr      |
| `!`      | Logisches NICHT| `!a`       | Boolean negieren          |

**Kurzschluss-Auswertung:**
- `&&` - Stoppt beim ersten falschen Wert
- `||` - Stoppt beim ersten wahren Wert

**Beispiele:**
```hemlock
let a = true;
let b = false;

print(a && b);         // false
print(a || b);         // true
print(!a);             // false
print(!b);             // true

// Kurzschluss
if (x != 0 && (10 / x) > 2) {
    print("sicher");
}

if (x == 0 || (10 / x) > 2) {
    print("sicher");
}
```

---

## Bitweise Operatoren

**Einschränkung:** Nur Ganzzahltypen (i8-i64, u8-u64)

### Binäre Bitweise

| Operator | Name           | Beispiel   | Beschreibung              |
|----------|----------------|------------|---------------------------|
| `&`      | Bitweises UND  | `a & b`    | UND jedes Bit             |
| `|`      | Bitweises ODER | `a | b`    | ODER jedes Bit            |
| `^`      | Bitweises XOR  | `a ^ b`    | XOR jedes Bit             |
| `<<`     | Linksverschiebung | `a << b` | Um b Bits nach links verschieben |
| `>>`     | Rechtsverschiebung| `a >> b` | Um b Bits nach rechts verschieben |

**Typerhaltung:**
Ergebnistyp entspricht Operandentypen (mit Typpromovierung).

**Beispiele:**
```hemlock
let a = 12;  // 1100 in Binär
let b = 10;  // 1010 in Binär

print(a & b);          // 8  (1000)
print(a | b);          // 14 (1110)
print(a ^ b);          // 6  (0110)
print(a << 2);         // 48 (110000)
print(a >> 1);         // 6  (110)
```

**Beispiel mit Unsigned:**
```hemlock
let c: u8 = 15;        // 00001111
let d: u8 = 7;         // 00000111

print(c & d);          // 7  (00000111)
print(c | d);          // 15 (00001111)
print(c ^ d);          // 8  (00001000)
```

**Rechtsverschiebungs-Verhalten:**
- Vorzeichenbehaftete Typen: Arithmetische Verschiebung (Vorzeichenerweiterung)
- Vorzeichenlose Typen: Logische Verschiebung (Null-Fuellung)

---

### Unaere Bitweise

| Operator | Name          | Beispiel | Beschreibung              |
|----------|---------------|----------|---------------------------|
| `~`      | Bitweises NICHT| `~a`    | Alle Bits umkehren        |

**Beispiele:**
```hemlock
let a = 12;            // 00001100 (i32)
print(~a);             // -13 (Zweierkomplement)

let b: u8 = 15;        // 00001111
print(~b);             // 240 (11110000)
```

---

## String-Operatoren

### Verkettung

| Operator | Name        | Beispiel   | Beschreibung        |
|----------|-------------|------------|---------------------|
| `+`      | Verkettung  | `a + b`    | Strings verbinden   |

**Beispiele:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"

// String + Rune
let greeting = "Hello" + '!';      // "Hello!"

// Rune + String
let prefix = '>' + " Message";     // "> Message"
```

---

## Zuweisungsoperatoren

### Einfache Zuweisung

| Operator | Name       | Beispiel   | Beschreibung                  |
|----------|------------|------------|-------------------------------|
| `=`      | Zuweisung  | `a = b`    | Wert an Variable zuweisen     |

**Beispiele:**
```hemlock
let x = 10;
x = 20;

let arr = [1, 2, 3];
arr[0] = 99;

let obj = { x: 10 };
obj.x = 20;
```

### Zusammengesetzte Zuweisung

#### Arithmetische zusammengesetzte Zuweisung

| Operator | Name               | Beispiel   | Äquivalent        |
|----------|--------------------|------------|--------------------|
| `+=`     | Addieren und zuweisen | `a += b` | `a = a + b`        |
| `-=`     | Subtrahieren und zuweisen | `a -= b` | `a = a - b`    |
| `*=`     | Multiplizieren und zuweisen | `a *= b` | `a = a * b`  |
| `/=`     | Dividieren und zuweisen | `a /= b` | `a = a / b`      |
| `%=`     | Modulo und zuweisen | `a %= b`   | `a = a % b`        |

**Beispiele:**
```hemlock
let x = 10;
x += 5;      // x ist jetzt 15
x -= 3;      // x ist jetzt 12
x *= 2;      // x ist jetzt 24
x /= 4;      // x ist jetzt 6

let count = 0;
count += 1;  // Um 1 erhöhen
```

#### Bitweise zusammengesetzte Zuweisung

| Operator | Name                      | Beispiel    | Äquivalent         |
|----------|---------------------------|-------------|---------------------|
| `&=`     | Bitweises UND und zuweisen | `a &= b`   | `a = a & b`         |
| `\|=`    | Bitweises ODER und zuweisen| `a \|= b`  | `a = a \| b`        |
| `^=`     | Bitweises XOR und zuweisen | `a ^= b`   | `a = a ^ b`         |
| `<<=`    | Linksverschiebung und zuweisen | `a <<= b` | `a = a << b`     |
| `>>=`    | Rechtsverschiebung und zuweisen | `a >>= b` | `a = a >> b`   |

**Beispiele:**
```hemlock
let flags = 0b1111;
flags &= 0b0011;   // flags ist jetzt 0b0011 (obere Bits maskieren)
flags |= 0b1000;   // flags ist jetzt 0b1011 (Bit setzen)
flags ^= 0b0001;   // flags ist jetzt 0b1010 (Bit umschalten)

let x = 1;
x <<= 4;           // x ist jetzt 16 (um 4 nach links verschieben)
x >>= 2;           // x ist jetzt 4 (um 2 nach rechts verschieben)
```

### Inkrement/Dekrement

| Operator | Name       | Beispiel | Beschreibung                  |
|----------|------------|----------|-------------------------------|
| `++`     | Inkrement  | `a++`    | Um 1 erhöhen (Postfix)       |
| `--`     | Dekrement  | `a--`    | Um 1 verringern (Postfix)     |

**Beispiele:**
```hemlock
let i = 0;
i++;         // i ist jetzt 1
i++;         // i ist jetzt 2
i--;         // i ist jetzt 1

// Häufig in Schleifen
for (let j = 0; j < 10; j++) {
    print(j);
}
```

**Hinweis:** Sowohl `++` als auch `--` sind Postfix-Operatoren (Wert wird vor Inkrement/Dekrement zurückgegeben)

---

## Null-Sicherheitsoperatoren

### Null-Koaleszenz (`??`)

Gibt den linken Operanden zurück wenn er nicht null ist, sonst den rechten Operanden.

| Operator | Name             | Beispiel     | Beschreibung                    |
|----------|------------------|--------------|--------------------------------|
| `??`     | Null-Koaleszenz  | `a ?? b`     | a zurückgeben wenn nicht null, sonst b |

**Beispiele:**
```hemlock
let name = null;
let display = name ?? "Anonym";  // "Anonym"

let value = 42;
let result = value ?? 0;            // 42

// Verkettung
let a = null;
let b = null;
let c = "gefunden";
let result2 = a ?? b ?? c;          // "gefunden"

// Mit Funktionsaufrufen
fn get_config() { return null; }
let config = get_config() ?? { default: true };
```

---

### Optionale Verkettung (`?.`)

Sicherer Zugriff auf Eigenschaften oder Aufruf von Methoden auf potenziell null-Werten.

| Operator | Name                 | Beispiel       | Beschreibung                      |
|----------|----------------------|----------------|-----------------------------------|
| `?.`     | Optionale Verkettung | `a?.b`         | a.b zurückgeben wenn a nicht null, sonst null |
| `?.[`    | Optionaler Index     | `a?.[0]`       | a[0] zurückgeben wenn a nicht null, sonst null |
| `?.(`    | Optionaler Aufruf    | `a?.()`        | a() aufrufen wenn a nicht null, sonst null |

**Beispiele:**
```hemlock
let user = null;
let name = user?.name;              // null (kein Fehler)

let person = { name: "Alice", address: null };
let city = person?.address?.city;   // null (sichere Navigation)

// Mit Arrays
let arr = null;
let first = arr?.[0];               // null

let items = [1, 2, 3];
let second = items?.[1];            // 2

// Mit Methodenaufrufen
let obj = { greet: fn() { return "Hallo"; } };
let greeting = obj?.greet?.();      // "Hallo"

let empty = null;
let result = empty?.method?.();     // null
```

**Verhalten:**
- Wenn linker Operand null, wird gesamter Ausdruck auf null kurzgeschlossen
- Wenn linker Operand nicht null, wird Zugriff normal durchgeführt
- Kann für tiefen Eigenschaftszugriff verkettet werden

---

## Elementzugriffsoperatoren

### Punkt-Operator

| Operator | Name               | Beispiel     | Beschreibung           |
|----------|--------------------|--------------|-----------------------|
| `.`      | Elementzugriff     | `obj.field`  | Objektfeld zugreifen   |
| `.`      | Eigenschaftszugriff| `arr.length` | Eigenschaft zugreifen  |

**Beispiele:**
```hemlock
// Objektfeld-Zugriff
let person = { name: "Alice", age: 30 };
print(person.name);        // "Alice"

// Array-Eigenschaft
let arr = [1, 2, 3];
print(arr.length);         // 3

// String-Eigenschaft
let s = "hello";
print(s.length);           // 5

// Methodenaufruf
let result = s.to_upper(); // "HELLO"
```

---

### Index-Operator

| Operator | Name    | Beispiel  | Beschreibung          |
|----------|---------|-----------|----------------------|
| `[]`     | Index   | `arr[i]`  | Element zugreifen     |

**Beispiele:**
```hemlock
// Array-Indizierung
let arr = [10, 20, 30];
print(arr[0]);             // 10
arr[1] = 99;

// String-Indizierung (gibt Rune zurück)
let s = "hello";
print(s[0]);               // 'h'
s[0] = 'H';                // "Hello"

// Buffer-Indizierung
let buf = buffer(10);
buf[0] = 65;
print(buf[0]);             // 65
```

---

## Funktionsaufruf-Operator

| Operator | Name           | Beispiel     | Beschreibung        |
|----------|----------------|--------------|---------------------|
| `()`     | Funktionsaufruf| `f(a, b)`    | Funktion aufrufen   |

**Beispiele:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(5, 3);    // 8

// Methodenaufruf
let s = "hello";
let upper = s.to_upper();  // "HELLO"

// Eingebauter Aufruf
print("message");
```

---

## Operatorpraezedenz

Operatoren von hoechster zu niedrigster Präzedenz:

| Präzedenz | Operatoren                 | Beschreibung                    | Assoziativitaet |
|------------|----------------------------|--------------------------------|----------------|
| 1          | `()` `[]` `.` `?.`         | Aufruf, Index, Elementzugriff, optionale Verkettung | Links-nach-rechts |
| 2          | `++` `--`                  | Postfix-Inkrement/Dekrement    | Links-nach-rechts |
| 3          | `!` `~` `-` (unaer) `+` (unaer) | Logisches NICHT, bitweises NICHT, Negation | Rechts-nach-links |
| 4          | `*` `/` `%`                | Multiplikation, Division, Modulo | Links-nach-rechts |
| 5          | `+` `-`                    | Addition, Subtraktion          | Links-nach-rechts |
| 6          | `<<` `>>`                  | Bitverschiebungen              | Links-nach-rechts |
| 7          | `<` `<=` `>` `>=`          | Relational                     | Links-nach-rechts |
| 8          | `==` `!=`                  | Gleichheit                     | Links-nach-rechts |
| 9          | `&`                        | Bitweises UND                  | Links-nach-rechts |
| 10         | `^`                        | Bitweises XOR                  | Links-nach-rechts |
| 11         | `|`                        | Bitweises ODER                 | Links-nach-rechts |
| 12         | `&&`                       | Logisches UND                  | Links-nach-rechts |
| 13         | `||`                       | Logisches ODER                 | Links-nach-rechts |
| 14         | `??`                       | Null-Koaleszenz                | Links-nach-rechts |
| 15         | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | Zuweisung | Rechts-nach-links |

---

## Präzedenz-Beispiele

### Beispiel 1: Arithmetik und Vergleich
```hemlock
let result = 5 + 3 * 2;
// Ausgewertet als: 5 + (3 * 2) = 11
// Multiplikation hat höhere Präzedenz als Addition

let cmp = 10 > 5 + 3;
// Ausgewertet als: 10 > (5 + 3) = true
// Addition hat höhere Präzedenz als Vergleich
```

### Beispiel 2: Bitweise Operatoren
```hemlock
let result1 = 12 | 10 & 8;
// Ausgewertet als: 12 | (10 & 8) = 12 | 8 = 12
// & hat höhere Präzedenz als |

let result2 = 8 | 1 << 2;
// Ausgewertet als: 8 | (1 << 2) = 8 | 4 = 12
// Verschiebung hat höhere Präzedenz als bitweises ODER

// Klammern für Klarheit verwenden
let result3 = (5 & 3) | (2 << 1);
// Ausgewertet als: 1 | 4 = 5
```

### Beispiel 3: Logische Operatoren
```hemlock
let result = true || false && false;
// Ausgewertet als: true || (false && false) = true
// && hat höhere Präzedenz als ||

let cmp = 5 < 10 && 10 < 20;
// Ausgewertet als: (5 < 10) && (10 < 20) = true
// Vergleich hat höhere Präzedenz als &&
```

### Beispiel 4: Klammern verwenden
```hemlock
// Ohne Klammern
let a = 2 + 3 * 4;        // 14

// Mit Klammern
let b = (2 + 3) * 4;      // 20

// Komplexer Ausdruck
let c = (a + b) * (a - b);
```

---

## Typspezifisches Operatorverhalten

### Division (immer Gleitkomma)

Der `/`-Operator **gibt immer eine Gleitkommazahl zurück** (f64), unabhängig von Operandentypen:

```hemlock
print(10 / 3);             // 3.333... (f64)
print(5 / 2);              // 2.5 (f64)
print(10.0 / 4.0);         // 2.5 (f64)
print(-7 / 3);             // -2.333... (f64)
```

Dies verhindert den haeufigen Bug unerwarteter Ganzzahl-Trunkierung.

### Ganzzahl-Division (div / divi)

Für Ganzzahl-Division (wie Integer-Division in anderen Sprachen) verwenden Sie die `div()` und `divi()` Funktionen:

```hemlock
// div(a, b) - Ganzzahl-Division gibt Gleitkomma zurück
print(div(5, 2));          // 2 (f64)
print(div(-7, 3));         // -3 (f64)  -- rundet Richtung -unendlich

// divi(a, b) - Ganzzahl-Division gibt Ganzzahl zurück
print(divi(5, 2));         // 2 (i64)
print(divi(-7, 3));        // -3 (i64)
print(typeof(divi(5, 2))); // i64
```

**Ganzzahl-zurueckgebende Mathematikfunktionen:**
Für andere Rundungsoperationen die Ganzzahlen zurückgeben:

```hemlock
print(floori(3.7));        // 3 (i64)
print(ceili(3.2));         // 4 (i64)
print(roundi(3.5));        // 4 (i64)
print(trunci(3.9));        // 3 (i64)

// Diese können direkt als Array-Indizes verwendet werden
let arr = [10, 20, 30, 40];
print(arr[floori(1.9)]);   // 20 (Index 1)
```

### String-Vergleich

Strings werden lexikografisch verglichen:

```hemlock
print("abc" < "def");      // true
print("apple" > "banana"); // false
print("hello" == "hello"); // true
```

### Null-Vergleich

```hemlock
let x = null;

print(x == null);          // true
print(x != null);          // false
```

### Typfehler

Manche Operationen sind zwischen inkompatiblen Typen nicht erlaubt:

```hemlock
// FEHLER: Kann bitweise Operatoren nicht auf Gleitkomma anwenden
let x = 3.14 & 2.71;

// FEHLER: Kann bitweise Operatoren nicht auf Strings anwenden
let y = "hello" & "world";

// OK: Typpromovierung für Arithmetik
let a: u8 = 10;
let b: i32 = 20;
let c = a + b;             // i32 (promoviert)
```

---

## Siehe auch

- [Typsystem](type-system.md) - Typpromovierungs- und Konvertierungsregeln
- [Eingebaute Funktionen](builtins.md) - Eingebaute Operationen
- [String-API](string-api.md) - String-Verkettung und -Methoden
