# Array-API-Referenz

Vollstaendige Referenz fuer Hemlocks Array-Typ und alle 18 Array-Methoden.

---

## Uebersicht

Arrays in Hemlock sind **dynamische, heap-allokierte** Sequenzen, die gemischte Typen enthalten koennen. Sie bieten umfassende Methoden zur Datenmanipulation und -verarbeitung.

**Hauptmerkmale:**
- Dynamische Groessenanpassung (automatisches Wachstum)
- Nullbasierte Indizierung
- Gemischte Typen erlaubt
- 18 eingebaute Methoden
- Heap-allokiert mit Kapazitaetsverfolgung

---

## Array-Typ

**Typ:** `array`

**Eigenschaften:**
- `.length` - Anzahl der Elemente (i32)

**Literal-Syntax:** Eckige Klammern `[elem1, elem2, ...]`

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// Gemischte Typen
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// Leeres Array
let empty = [];
print(empty.length);   // 0
```

---

## Indizierung

Arrays unterstuetzen nullbasierte Indizierung mit `[]`:

**Lesezugriff:**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**Schreibzugriff:**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**Hinweis:** Direkter Indexzugriff hat keine Grenzenprüfung. Verwenden Sie Methoden fuer Sicherheit.

---

## Array-Eigenschaften

### .length

Gibt die Anzahl der Elemente im Array zurueck.

**Typ:** `i32`

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// Laenge aendert sich dynamisch
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## Array-Methoden

### Stack-Operationen

#### push

Fuegt ein Element am Ende des Arrays hinzu.

**Signatur:**
```hemlock
array.push(value: any): null
```

**Parameter:**
- `value` - Element zum Hinzufuegen

**Rueckgabe:** `null`

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

Entfernt und gibt das letzte Element zurueck.

**Signatur:**
```hemlock
array.pop(): any
```

**Rueckgabe:** Letztes Element (aus Array entfernt)

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**Fehler:** Laufzeitfehler wenn Array leer ist.

---

### Warteschlangen-Operationen

#### shift

Entfernt und gibt das erste Element zurueck.

**Signatur:**
```hemlock
array.shift(): any
```

**Rueckgabe:** Erstes Element (aus Array entfernt)

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**Fehler:** Laufzeitfehler wenn Array leer ist.

---

#### unshift

Fuegt ein Element am Anfang des Arrays hinzu.

**Signatur:**
```hemlock
array.unshift(value: any): null
```

**Parameter:**
- `value` - Element zum Hinzufuegen

**Rueckgabe:** `null`

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### Einfuegen & Entfernen

#### insert

Fuegt ein Element an einem bestimmten Index ein.

**Signatur:**
```hemlock
array.insert(index: i32, value: any): null
```

**Parameter:**
- `index` - Position zum Einfuegen (nullbasiert)
- `value` - Element zum Einfuegen

**Rueckgabe:** `null`

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// Am Ende einfuegen
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**Verhalten:** Verschiebt Elemente ab dem Index nach rechts.

---

#### remove

Entfernt und gibt das Element am Index zurueck.

**Signatur:**
```hemlock
array.remove(index: i32): any
```

**Parameter:**
- `index` - Position zum Entfernen (nullbasiert)

**Rueckgabe:** Entferntes Element

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**Verhalten:** Verschiebt Elemente nach dem Index nach links.

**Fehler:** Laufzeitfehler wenn Index ausserhalb der Grenzen.

---

### Suchen & Finden

#### find

Findet das erste Vorkommen eines Wertes.

**Signatur:**
```hemlock
array.find(value: any): i32
```

**Parameter:**
- `value` - Zu suchender Wert

**Rueckgabe:** Index des ersten Vorkommens, oder `-1` wenn nicht gefunden

**Beispiele:**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1 (nicht gefunden)

// Erstes Duplikat finden
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1 (erstes Vorkommen)
```

**Vergleich:** Verwendet Wertgleichheit fuer Primitive und Strings.

---

#### contains

Prueft ob das Array einen Wert enthaelt.

**Signatur:**
```hemlock
array.contains(value: any): bool
```

**Parameter:**
- `value` - Zu suchender Wert

**Rueckgabe:** `true` wenn gefunden, `false` sonst

**Beispiele:**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// Funktioniert mit Strings
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### Slicing & Extraktion

#### slice

Extrahiert ein Teilarray nach Bereich (Ende exklusiv).

**Signatur:**
```hemlock
array.slice(start: i32, end: i32): array
```

**Parameter:**
- `start` - Startindex (nullbasiert, inklusiv)
- `end` - Endindex (exklusiv)

**Rueckgabe:** Neues Array mit Elementen von [start, end)

**Mutiert:** Nein (gibt neues Array zurueck)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// Leerer Slice
let empty = arr.slice(2, 2); // []
```

---

#### first

Gibt das erste Element zurueck ohne es zu entfernen.

**Signatur:**
```hemlock
array.first(): any
```

**Rueckgabe:** Erstes Element

**Mutiert:** Nein

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3] (unveraendert)
```

**Fehler:** Laufzeitfehler wenn Array leer ist.

---

#### last

Gibt das letzte Element zurueck ohne es zu entfernen.

**Signatur:**
```hemlock
array.last(): any
```

**Rueckgabe:** Letztes Element

**Mutiert:** Nein

**Beispiele:**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3] (unveraendert)
```

**Fehler:** Laufzeitfehler wenn Array leer ist.

---

### Array-Manipulation

#### reverse

Kehrt das Array an Ort und Stelle um.

**Signatur:**
```hemlock
array.reverse(): null
```

**Rueckgabe:** `null`

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

Entfernt alle Elemente aus dem Array.

**Signatur:**
```hemlock
array.clear(): null
```

**Rueckgabe:** `null`

**Mutiert:** Ja (modifiziert Array direkt)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### Array-Kombination

#### concat

Verkettet mit einem anderen Array.

**Signatur:**
```hemlock
array.concat(other: array): array
```

**Parameter:**
- `other` - Array zum Verketten

**Rueckgabe:** Neues Array mit Elementen aus beiden Arrays

**Mutiert:** Nein (gibt neues Array zurueck)

**Beispiele:**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3] (unveraendert)
print(b);                    // [4, 5, 6] (unveraendert)

// Verkettungen verketten
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### Funktionale Operationen

#### map

Transformiert jedes Element mit einer Callback-Funktion.

**Signatur:**
```hemlock
array.map(callback: fn): array
```

**Parameter:**
- `callback` - Funktion die ein Element nimmt und transformierten Wert zurueckgibt

**Rueckgabe:** Neues Array mit transformierten Elementen

**Mutiert:** Nein (gibt neues Array zurueck)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

Waehlt Elemente aus die einem Praedikat entsprechen.

**Signatur:**
```hemlock
array.filter(predicate: fn): array
```

**Parameter:**
- `predicate` - Funktion die ein Element nimmt und bool zurueckgibt

**Rueckgabe:** Neues Array mit Elementen wo Praedikat true zurueckgab

**Mutiert:** Nein (gibt neues Array zurueck)

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

Reduziert Array auf einen einzelnen Wert mit Akkumulator.

**Signatur:**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**Parameter:**
- `callback` - Funktion die (Akkumulator, Element) nimmt und neuen Akkumulator zurueckgibt
- `initial` - Startwert fuer den Akkumulator

**Rueckgabe:** Endgueltiger akkumulierter Wert

**Mutiert:** Nein

**Beispiele:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// Maximalwert finden
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### String-Konvertierung

#### join

Verbindet Elemente zu einem String mit Trennzeichen.

**Signatur:**
```hemlock
array.join(delimiter: string): string
```

**Parameter:**
- `delimiter` - String der zwischen Elementen platziert wird

**Rueckgabe:** String mit allen verbundenen Elementen

**Beispiele:**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funktioniert mit gemischten Typen
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// Leeres Trennzeichen
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**Verhalten:** Konvertiert automatisch alle Elemente zu Strings.

---

## Methoden-Verkettung

Array-Methoden koennen fuer praegnante Operationen verkettet werden:

**Beispiele:**
```hemlock
// slice und join verketten
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// concat und slice verketten
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// Komplexe Verkettung
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## Vollstaendige Methodenuebersicht

### Mutierende Methoden

Methoden die das Array direkt modifizieren:

| Methode    | Signatur                   | Rueckgabe | Beschreibung                   |
|------------|----------------------------|-----------|--------------------------------|
| `push`     | `(value: any)`             | `null`    | Am Ende hinzufuegen            |
| `pop`      | `()`                       | `any`     | Vom Ende entfernen             |
| `shift`    | `()`                       | `any`     | Vom Anfang entfernen           |
| `unshift`  | `(value: any)`             | `null`    | Am Anfang hinzufuegen          |
| `insert`   | `(index: i32, value: any)` | `null`    | An Index einfuegen             |
| `remove`   | `(index: i32)`             | `any`     | An Index entfernen             |
| `reverse`  | `()`                       | `null`    | An Ort und Stelle umkehren     |
| `clear`    | `()`                       | `null`    | Alle Elemente entfernen        |

### Nicht-mutierende Methoden

Methoden die neue Werte zurueckgeben ohne das Original zu modifizieren:

| Methode    | Signatur                   | Rueckgabe | Beschreibung                   |
|------------|----------------------------|-----------|--------------------------------|
| `find`     | `(value: any)`             | `i32`     | Erstes Vorkommen finden        |
| `contains` | `(value: any)`             | `bool`    | Pruefen ob Wert enthalten      |
| `slice`    | `(start: i32, end: i32)`   | `array`   | Teilarray extrahieren          |
| `first`    | `()`                       | `any`     | Erstes Element holen           |
| `last`     | `()`                       | `any`     | Letztes Element holen          |
| `concat`   | `(other: array)`           | `array`   | Arrays verketten               |
| `join`     | `(delimiter: string)`      | `string`  | Elemente zu String verbinden   |
| `map`      | `(callback: fn)`           | `array`   | Jedes Element transformieren   |
| `filter`   | `(predicate: fn)`          | `array`   | Passende Elemente auswaehlen   |
| `reduce`   | `(callback: fn, initial: any)` | `any` | Auf einzelnen Wert reduzieren  |

---

## Verwendungsmuster

### Stack-Verwendung

```hemlock
let stack = [];

// Elemente pushen
stack.push(1);
stack.push(2);
stack.push(3);

// Elemente poppen
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### Warteschlangen-Verwendung

```hemlock
let queue = [];

// Einreihen
queue.push(1);
queue.push(2);
queue.push(3);

// Ausreihen
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### Array-Transformation

```hemlock
// Filtern (manuell)
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// Abbilden (manuell)
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### Arrays aufbauen

```hemlock
let arr = [];

// Array mit Schleife aufbauen
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## Implementierungsdetails

**Kapazitaetsverwaltung:**
- Arrays wachsen automatisch bei Bedarf
- Kapazitaet verdoppelt sich bei Ueberschreitung
- Keine manuelle Kapazitaetssteuerung

**Wertvergleich:**
- `find()` und `contains()` verwenden Wertgleichheit
- Funktioniert korrekt fuer Primitive und Strings
- Objekte/Arrays werden per Referenz verglichen

**Speicher:**
- Heap-allokiert
- Keine automatische Freigabe (manuelle Speicherverwaltung)
- Keine Grenzenprüfung bei direktem Indexzugriff

---

## Siehe auch

- [Typsystem](type-system.md) - Array-Typ-Details
- [String-API](string-api.md) - String join()-Ergebnisse
- [Operatoren](operators.md) - Array-Indizierungsoperator
