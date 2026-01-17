# Pattern Matching

Hemlock bietet leistungsfaehiges Pattern Matching durch `match`-Ausdruecke, die eine praegnante Moeglichkeit bieten, Werte zu destrukturieren, Typen zu pruefen und mehrere Faelle zu behandeln.

## Grundlegende Syntax

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

Match-Ausdruecke werten `value` gegen jedes Pattern der Reihe nach aus und geben das Ergebnis des Ausdrucks des ersten passenden Arms zurueck.

## Pattern-Typen

### Literal-Patterns

Exakte Werte abgleichen:

```hemlock
let x = 42;
let msg = match (x) {
    0 => "null",
    1 => "eins",
    42 => "die Antwort",
    _ => "andere"
};
print(msg);  // "die Antwort"
```

Unterstuetzte Literale:
- **Ganzzahlen**: `0`, `42`, `-5`
- **Fliesskommazahlen**: `3.14`, `-0.5`
- **Strings**: `"hello"`, `"world"`
- **Booleans**: `true`, `false`
- **Null**: `null`

### Wildcard-Pattern (`_`)

Passt auf jeden Wert ohne Bindung:

```hemlock
let x = "anything";
let result = match (x) {
    "specific" => "gefunden",
    _ => "wildcard matched"
};
```

### Variablenbindungs-Patterns

Den gematchten Wert an eine Variable binden:

```hemlock
let x = 100;
let result = match (x) {
    0 => "null",
    n => "Wert ist " + n  // n wird an 100 gebunden
};
print(result);  // "Wert ist 100"
```

### ODER-Patterns (`|`)

Mehrere Alternativen abgleichen:

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "klein",
    4 | 5 | 6 => "mittel",
    _ => "gross"
};

// Funktioniert auch mit Strings
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "beende",
    "help" | "h" | "?" => "zeige Hilfe",
    _ => "unbekannt"
};
```

### Guard-Ausdruecke (`if`)

Bedingungen zu Patterns hinzufuegen:

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negativ",
    n if n == 0 => "null",
    n if n < 10 => "klein",
    n if n < 100 => "mittel",
    n => "gross: " + n
};
print(category);  // "mittel"

// Komplexe Guards
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "gerade und groesser als 10",
    n if n % 2 == 0 => "gerade",
    n => "ungerade"
};
```

### Typ-Patterns

Basierend auf Typ pruefen und binden:

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "Ganzzahl: " + num,
    str: string => "String: " + str,
    flag: bool => "Boolean: " + flag,
    _ => "anderer Typ"
};
print(desc);  // "Ganzzahl: 42"
```

Unterstuetzte Typen: `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Destrukturierungs-Patterns

### Objekt-Destrukturierung

Felder aus Objekten extrahieren:

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "Punkt bei " + x + "," + y
};
print(result);  // "Punkt bei 10,20"

// Mit literalen Feldwerten
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "Ursprung",
    { x: 0, y } => "auf y-Achse bei " + y,
    { x, y: 0 } => "auf x-Achse bei " + x,
    { x, y } => "Punkt bei " + x + "," + y
};
print(name);  // "Ursprung"
```

### Array-Destrukturierung

Array-Struktur und Elemente abgleichen:

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "leer",
    [x] => "einzeln: " + x,
    [x, y] => "Paar: " + x + "," + y,
    [x, y, z] => "Tripel: " + x + "," + y + "," + z,
    _ => "viele Elemente"
};
print(desc);  // "Tripel: 1,2,3"

// Mit literalen Werten
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "beide null",
    [1, x] => "beginnt mit 1, zweites ist " + x,
    [x, 1] => "endet mit 1",
    _ => "andere"
};
print(result);  // "beginnt mit 1, zweites ist 2"
```

### Array-Rest-Patterns (`...`)

Verbleibende Elemente erfassen:

```hemlock
let nums = [1, 2, 3, 4, 5];

// Kopf und Rest
let result = match (nums) {
    [first, ...rest] => "erstes: " + first,
    [] => "leer"
};
print(result);  // "erstes: 1"

// Erste zwei Elemente
let result2 = match (nums) {
    [a, b, ...rest] => "erste zwei: " + a + "," + b,
    _ => "zu kurz"
};
print(result2);  // "erste zwei: 1,2"
```

### Verschachtelte Destrukturierung

Patterns fuer komplexe Daten kombinieren:

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " lebt in " + city,
    _ => "unbekannt"
};
print(result);  // "Alice lebt in NYC"

// Objekt mit Array
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "erstes: " + first + ", gesamt: " + count,
    _ => "keine Elemente"
};
print(result2);  // "erstes: 1, gesamt: 3"
```

## Match als Ausdruck

Match ist ein Ausdruck, der einen Wert zurueckgibt:

```hemlock
// Direkte Zuweisung
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// In String-Verkettung
let msg = "Note: " + match (grade) {
    n if n >= 70 => "bestanden",
    _ => "durchgefallen"
};

// In Funktionsrueckgabe
fn classify(n: i32): string {
    return match (n) {
        0 => "null",
        n if n > 0 => "positiv",
        _ => "negativ"
    };
}
```

## Best Practices fuer Pattern Matching

1. **Reihenfolge ist wichtig**: Patterns werden von oben nach unten geprueft; setzen Sie spezifische Patterns vor allgemeine
2. **Wildcards fuer Vollstaendigkeit**: Fuegen Sie immer einen `_`-Fallback ein, ausser Sie sind sicher, dass alle Faelle abgedeckt sind
3. **Guards statt verschachtelter Bedingungen bevorzugen**: Guards machen die Absicht klarer
4. **Destrukturierung statt manuellem Feldzugriff bevorzugen**: Praegnanter und sicherer

```hemlock
// Gut: Guards fuer Bereichspruefung
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "unter B"
}

// Gut: Destrukturieren statt Feldzugriff
match (point) {
    { x: 0, y: 0 } => "Ursprung",
    { x, y } => "bei " + x + "," + y
}

// Vermeiden: Ueberkomplexe verschachtelte Patterns
// Stattdessen in mehrere Matches aufteilen oder Guards verwenden
```

## Vergleich mit anderen Sprachen

| Feature | Hemlock | Rust | JavaScript |
|---------|---------|------|------------|
| Basis-Matching | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Destrukturierung | Ja | Ja | Teilweise (switch destrukturiert nicht) |
| Guards | `n if n > 0 =>` | `n if n > 0 =>` | N/A |
| ODER-Patterns | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Rest-Patterns | `[a, ...rest]` | `[a, rest @ ..]` | N/A |
| Typ-Patterns | `n: i32` | Typ via `match`-Arm | N/A |
| Gibt Wert zurueck | Ja | Ja | Nein (Statement) |

## Implementierungshinweise

Pattern Matching ist sowohl im Interpreter- als auch im Compiler-Backend mit voller Paritaet implementiert - beide erzeugen identische Ergebnisse fuer dieselbe Eingabe. Das Feature ist ab Hemlock v1.8.0 verfuegbar.
