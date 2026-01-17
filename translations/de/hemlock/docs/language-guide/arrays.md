# Arrays

Hemlock bietet **dynamische Arrays** mit umfassenden Methoden zur Datenmanipulation und -verarbeitung. Arrays können gemischte Typen enthalten und wachsen bei Bedarf automatisch.

## Übersicht

```hemlock
// Array-Literale
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Gemischte Typen erlaubt
let mixed = [1, "hello", true, null];

// Dynamische Größenanpassung
arr.push(6);           // Wächst automatisch
arr.push(7);
print(arr.length);     // 7
```

## Array-Literale

### Grundlegende Syntax

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### Leere Arrays

```hemlock
let arr = [];  // Leeres Array

// Elemente später hinzufügen
arr.push(1);
arr.push(2);
arr.push(3);
```

### Gemischte Typen

Arrays können verschiedene Typen enthalten:

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3] (verschachteltes Array)
```

### Verschachtelte Arrays

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### Typisierte Arrays

Arrays können Typannotationen haben, um Elementtypen zu erzwingen:

```hemlock
// Typisierte Array-Syntax
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Typüberprüfung zur Laufzeit
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "two", 3]; // Laufzeitfehler: Typkonflikt

// Verschachtelte typisierte Arrays
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Typannotations-Verhalten:**
- Elemente werden beim Hinzufügen zum Array typüberprüft
- Typkonflikte verursachen Laufzeitfehler
- Ohne Typannotation akzeptieren Arrays gemischte Typen

## Indizierung

### Elemente lesen

Nullbasierter Zugriff:

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (erstes Element)
print(arr[4]);  // 50 (letztes Element)

// Zugriff außerhalb der Grenzen gibt null zurück (kein Fehler)
print(arr[10]);  // null
```

### Elemente schreiben

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Bestehendes ändern
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Kann über aktuelle Länge hinaus zuweisen (Array wächst)
arr[5] = 60;    // Erstellt [10, 20, 3, null, null, 60]
```

### Negative Indizes

**Nicht unterstützt** - Verwende nur positive Indizes:

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // FEHLER oder undefiniertes Verhalten

// Verwende length für letztes Element
print(arr[arr.length - 1]);  // 3
```

## Eigenschaften

### `.length`-Eigenschaft

Gibt die Anzahl der Elemente zurück:

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Leeres Array
let empty = [];
print(empty.length);  // 0

// Nach Änderungen
arr.push(6);
print(arr.length);  // 6
```

## Array-Methoden

Hemlock bietet 18 Array-Methoden für umfassende Manipulation.

### Stack-Operationen

**`push(value)`** - Element am Ende hinzufügen:
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Letztes Element entfernen und zurückgeben:
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Gibt 5 zurück, arr ist jetzt [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Queue-Operationen

**`shift()`** - Erstes Element entfernen und zurückgeben:
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Gibt 1 zurück, arr ist jetzt [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Element am Anfang hinzufügen:
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Einfüge- und Entfernungsoperationen

**`insert(index, value)`** - Element an Index einfügen:
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // 3 an Index 2 einfügen: [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Am Anfang einfügen: [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Element an Index entfernen und zurückgeben:
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Gibt 3 zurück, arr ist jetzt [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Suchoperationen

**`find(value)`** - Erstes Vorkommen finden:
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (Index des ersten Vorkommens)
let idx2 = arr.find(99);     // -1 (nicht gefunden)

// Funktioniert mit jedem Typ
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - Prüfen ob Array Wert enthält:
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Extraktionsoperationen

**`slice(start, end)`** - Teilarray extrahieren (Ende exklusiv):
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (Indizes 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Original unverändert
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Erstes Element holen (ohne Entfernen):
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (ohne Entfernen)
print(arr);                  // [1, 2, 3] (unverändert)
```

**`last()`** - Letztes Element holen (ohne Entfernen):
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (ohne Entfernen)
print(arr);                  // [1, 2, 3] (unverändert)
```

### Transformationsoperationen

**`reverse()`** - Array an Ort und Stelle umkehren:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (geändert)
```

**`join(delimiter)`** - Elemente zu String verbinden:
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funktioniert mit gemischten Typen
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - Mit anderem Array verketten:
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (neues Array)

// Originale unverändert
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Hilfsoperationen

**`clear()`** - Alle Elemente entfernen:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Methodenverkettung

Methoden, die Arrays oder Werte zurückgeben, ermöglichen Verkettung:

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Vollständige Methodenreferenz

| Methode | Parameter | Rückgabe | Mutiert | Beschreibung |
|--------|-----------|---------|---------|-------------|
| `push(value)` | any | void | Ja | Element am Ende hinzufügen |
| `pop()` | - | any | Ja | Letztes entfernen und zurückgeben |
| `shift()` | - | any | Ja | Erstes entfernen und zurückgeben |
| `unshift(value)` | any | void | Ja | Element am Anfang hinzufügen |
| `insert(index, value)` | i32, any | void | Ja | An Index einfügen |
| `remove(index)` | i32 | any | Ja | An Index entfernen und zurückgeben |
| `find(value)` | any | i32 | Nein | Erstes Vorkommen finden (-1 wenn nicht gefunden) |
| `contains(value)` | any | bool | Nein | Prüfen ob Wert enthalten |
| `slice(start, end)` | i32, i32 | array | Nein | Teilarray extrahieren (neues Array) |
| `join(delimiter)` | string | string | Nein | Zu String verbinden |
| `concat(other)` | array | array | Nein | Verketten (neues Array) |
| `reverse()` | - | void | Ja | An Ort und Stelle umkehren |
| `first()` | - | any | Nein | Erstes Element holen |
| `last()` | - | any | Nein | Letztes Element holen |
| `clear()` | - | void | Ja | Alle Elemente entfernen |
| `map(callback)` | fn | array | Nein | Jedes Element transformieren |
| `filter(predicate)` | fn | array | Nein | Passende Elemente auswählen |
| `reduce(callback, initial)` | fn, any | any | Nein | Auf einzelnen Wert reduzieren |

## Implementierungsdetails

### Speichermodell

- **Heap-allokiert** - Dynamische Kapazität
- **Automatisches Wachstum** - Verdoppelt Kapazität bei Überschreitung
- **Kein automatisches Schrumpfen** - Kapazität nimmt nicht ab
- **Keine Grenzprüfung bei Indizierung** - Verwende Methoden für Sicherheit

### Kapazitätsverwaltung

```hemlock
let arr = [];  // Anfangskapazität: 0

arr.push(1);   // Wächst auf Kapazität 1
arr.push(2);   // Wächst auf Kapazität 2
arr.push(3);   // Wächst auf Kapazität 4 (verdoppelt)
arr.push(4);   // Immer noch Kapazität 4
arr.push(5);   // Wächst auf Kapazität 8 (verdoppelt)
```

### Wertvergleich

`find()` und `contains()` verwenden Wertgleichheit:

```hemlock
// Primitive: Vergleich nach Wert
let arr = [1, 2, 3];
arr.contains(2);  // true

// Strings: Vergleich nach Wert
let words = ["hello", "world"];
words.contains("hello");  // true

// Objekte: Vergleich nach Referenz
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (gleiche Referenz)
arr2.contains(obj2);  // false (verschiedene Referenz)
```

## Häufige Muster

### Funktionale Operationen (map/filter/reduce)

Arrays haben eingebaute `map`, `filter` und `reduce` Methoden:

```hemlock
// map - jedes Element transformieren
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - passende Elemente auswählen
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - auf einzelnen Wert akkumulieren
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Funktionale Operationen verketten
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Muster: Array als Stack

```hemlock
let stack = [];

// Auf Stack legen
stack.push(1);
stack.push(2);
stack.push(3);

// Vom Stack nehmen
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Muster: Array als Queue

```hemlock
let queue = [];

// Einreihen (am Ende hinzufügen)
queue.push(1);
queue.push(2);
queue.push(3);

// Ausreihen (vom Anfang entfernen)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Best Practices

1. **Verwende Methoden statt direkter Indizierung** - Grenzprüfung und Klarheit
2. **Pruefe Grenzen** - Direkte Indizierung prüft keine Grenzen
3. **Bevorzuge unveränderliche Operationen** - Verwende `slice()` und `concat()` statt Mutation
4. **Initialisiere mit Kapazität** - Wenn du die Größe kennst (derzeit nicht unterstützt)
5. **Verwende `contains()` für Zugehörigkeit** - Klarer als manuelle Schleifen
6. **Verkette Methoden** - Lesbarer als verschachtelte Aufrufe

## Häufige Fallstricke

### Fallstrick: Direkter Index außerhalb der Grenzen

```hemlock
let arr = [1, 2, 3];

// Keine Grenzprüfung!
arr[10] = 99;  // Erstellt duenn besetztes Array mit nulls
print(arr.length);  // 11 (nicht 3!)

// Besser: Verwende push() oder pruefe Länge
if (arr.length <= 10) {
    arr.push(99);
}
```

### Fallstrick: Mutation vs. Neues Array

```hemlock
let arr = [1, 2, 3];

// Mutiert Original
arr.reverse();
print(arr);  // [3, 2, 1]

// Gibt neues Array zurück
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (unverändert)
print(sub);  // [3, 2]
```

### Fallstrick: Referenzgleichheit

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Gleiche Referenz: true
arr.contains(obj);  // true

// Verschiedene Referenz: false
arr.contains({ x: 10 });  // false (verschiedenes Objekt)
```

### Fallstrick: Langlebige Arrays

```hemlock
// Arrays im lokalen Scope werden automatisch freigegeben, aber globale/langlebige Arrays brauchen Aufmerksamkeit
let global_cache = [];  // Modulebene, existiert bis Programmende

fn add_to_cache(item) {
    global_cache.push(item);  // Wächst unbegrenzt
}

// Für langlebige Daten, erwaege:
// - Array periodisch leeren: global_cache.clear();
// - Frueh freigeben wenn fertig: free(global_cache);
```

## Beispiele

### Beispiel: Array-Statistiken

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### Beispiel: Array-Deduplizierung

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### Beispiel: Array-Chunking

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### Beispiel: Array-Flachung

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Verschachteltes Array - flach machen
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### Beispiel: Sortierung (Bubble Sort)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Tauschen
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // Aendert an Ort und Stelle
print(numbers);  // [1, 2, 5, 8, 9]
```

## Einschränkungen

Aktuelle Einschränkungen:

- **Keine Grenzprüfung bei Indizierung** - Direkter Zugriff ist ungeprüft
- **Referenzgleichheit für Objekte** - `find()` und `contains()` verwenden Referenzvergleich
- **Keine Array-Destrukturierung** - Keine `let [a, b] = arr` Syntax
- **Kein Spread-Operator** - Keine `[...arr1, ...arr2]` Syntax

**Hinweis:** Arrays sind referenzgezählt und werden automatisch freigegeben, wenn der Scope endet. Siehe [Speicherverwaltung](memory.md#internal-reference-counting) für Details.

## Verwandte Themen

- [Strings](strings.md) - String-Methoden ähnlich wie Array-Methoden
- [Objekte](objects.md) - Arrays sind auch objektaehnlich
- [Funktionen](functions.md) - Höhere Ordnung Funktionen mit Arrays
- [Kontrollfluss](control-flow.md) - Über Arrays iterieren

## Siehe auch

- **Dynamische Größenanpassung**: Arrays wachsen automatisch mit Kapazitätsverdopplung
- **Methoden**: 18 umfassende Methoden zur Manipulation inklusive map/filter/reduce
- **Speicher**: Siehe [Speicher](memory.md) für Array-Allokationsdetails
