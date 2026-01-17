# Funktionen

Funktionen in Hemlock sind **erstklassige Werte**, die Variablen zugewiesen, als Argumente uebergeben und von anderen Funktionen zurueckgegeben werden koennen. Diese Anleitung behandelt Funktionssyntax, Closures, Rekursion und fortgeschrittene Muster.

## Uebersicht

```hemlock
// Benannte Funktionssyntax
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Anonyme Funktion
let multiply = fn(x, y) {
    return x * y;
};

// Closures
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Funktionsdeklaration

### Benannte Funktionen

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**Komponenten:**
- `fn` - Funktionsschluesselwort
- `greet` - Funktionsname
- `(name: string)` - Parameter mit optionalen Typen
- `: string` - Optionaler Rueckgabetyp
- `{ ... }` - Funktionskoerper

### Anonyme Funktionen

Funktionen ohne Namen, die Variablen zugewiesen werden:

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Benannt vs. Anonym:**
```hemlock
// Diese sind aequivalent:
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Hinweis:** Benannte Funktionen werden intern zu Variablenzuweisungen mit anonymen Funktionen umgewandelt.

## Parameter

### Grundlegende Parameter

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Typannotationen

Optionale Typannotationen fuer Parameter:

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // Laufzeit-Typueberpruefung konvertiert zu f64
```

**Typueberpruefung:**
- Parametertypen werden beim Aufruf ueberprueft, wenn annotiert
- Implizite Typkonvertierungen folgen Standard-Promotionsregeln
- Typkonflikte verursachen Laufzeitfehler

### Wertuebergabe (Pass-by-Value)

Alle Argumente werden **kopiert** (Wertuebergabe):

```hemlock
fn modify(x) {
    x = 100;  // Aendert nur die lokale Kopie
}

let a = 10;
modify(a);
print(a);  // Immer noch 10 (unveraendert)
```

**Hinweis:** Objekte und Arrays werden per Referenz uebergeben (die Referenz wird kopiert), sodass deren Inhalt geaendert werden kann:

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Aendert das Original-Array
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (geaendert)
```

## Rueckgabewerte

### Return-Anweisung

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Rueckgabetyp-Annotationen

Optionale Typannotation fuer den Rueckgabewert:

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Typueberpruefung:**
- Rueckgabetypen werden beim Zurueckgeben geprueft (wenn annotiert)
- Typkonvertierungen folgen Standard-Promotionsregeln

### Implizite Rueckgabe

Funktionen ohne Rueckgabetyp-Annotation geben implizit `null` zurueck:

```hemlock
fn print_message(msg) {
    print(msg);
    // Gibt implizit null zurueck
}

let result = print_message("hello");  // result ist null
```

### Fruehe Rueckgabe

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Fruehes Beenden
        }
    }
    return -1;  // Nicht gefunden
}
```

### Rueckgabe ohne Wert

`return;` ohne Wert gibt `null` zurueck:

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Gibt null zurueck
    }
    return value * 2;
}
```

## Erstklassige Funktionen

Funktionen koennen wie jeder andere Wert zugewiesen, uebergeben und zurueckgegeben werden.

### Funktionen als Variablen

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Neu zuweisen
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Funktionen als Argumente

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Funktionen als Rueckgabewerte

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Closures

Funktionen erfassen ihre definierende Umgebung (lexikalisches Scoping).

### Grundlegende Closures

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

**Wie es funktioniert:**
- Die innere Funktion erfasst `count` aus dem aeusseren Scope
- `count` bleibt ueber Aufrufe der zurueckgegebenen Funktion erhalten
- Jeder Aufruf von `makeCounter()` erstellt eine neue Closure mit eigenem `count`

### Closure mit Parametern

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Mehrere Closures

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Lexikalisches Scoping

Funktionen koennen durch lexikalisches Scoping auf Variablen des aeusseren Scopes zugreifen:

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Kann global und outer_var lesen
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Closures erfassen Variablen per Referenz, was sowohl Lesen als auch Mutation von Variablen des aeusseren Scopes ermoeglicht (wie im `makeCounter`-Beispiel oben gezeigt).

## Rekursion

Funktionen koennen sich selbst aufrufen.

### Grundlegende Rekursion

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Wechselseitige Rekursion

Funktionen koennen sich gegenseitig aufrufen:

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Rekursive Datenverarbeitung

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Hinweis:** Noch keine Tail-Call-Optimierung - tiefe Rekursion kann zu Stack-Ueberlauf fuehren.

## Hoehere Ordnung Funktionen

Funktionen, die andere Funktionen entgegennehmen oder zurueckgeben.

### Map-Muster

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Filter-Muster

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Reduce-Muster

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Funktionskomposition

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Haeufige Muster

### Muster: Factory-Funktionen

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### Muster: Callback-Funktionen

```hemlock
fn process_async(data, callback) {
    // ... Verarbeitung durchfuehren
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### Muster: Partielle Anwendung

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Muster: Memoisierung

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Viel schneller mit Caching
```

## Funktionssemantik

### Rueckgabetyp-Anforderungen

Funktionen mit Rueckgabetyp-Annotation **muessen** einen Wert zurueckgeben:

```hemlock
fn get_value(): i32 {
    // FEHLER: Fehlende Return-Anweisung
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Typueberpruefung

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Konvertiert zu f64, gibt f64 zurueck
add("a", "b");     // Laufzeitfehler: Typkonflikt
```

### Scope-Regeln

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Kann zugreifen auf: inner_var, outer_var, global
    }

    // Kann zugreifen auf: outer_var, global
    // Kann nicht zugreifen auf: inner_var
}

// Kann zugreifen auf: global
// Kann nicht zugreifen auf: outer_var, inner_var
```

## Best Practices

1. **Verwende Typannotationen** - Hilft Fehler zu finden und dokumentiert die Absicht
2. **Halte Funktionen klein** - Jede Funktion sollte eine Sache tun
3. **Bevorzuge reine Funktionen** - Vermeide Seiteneffekte wenn moeglich
4. **Benenne Funktionen klar** - Verwende beschreibende Verb-Namen
5. **Fruehe Rueckgabe** - Verwende Guard-Klauseln um Verschachtelung zu reduzieren
6. **Dokumentiere komplexe Closures** - Mache erfasste Variablen explizit
7. **Vermeide tiefe Rekursion** - Noch keine Tail-Call-Optimierung

## Haeufige Fallstricke

### Fallstrick: Rekursionstiefe

```hemlock
// Tiefe Rekursion kann Stack-Ueberlauf verursachen
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Kann mit Stack-Ueberlauf abstuerzen
```

### Fallstrick: Aendern erfasster Variablen

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Kann erfasste Variablen lesen und aendern
        return count;
    };
}
```

**Hinweis:** Das funktioniert, aber sei dir bewusst, dass alle Closures dieselbe erfasste Umgebung teilen.

## Beispiele

### Beispiel: Funktions-Pipeline

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Beispiel: Event-Handler

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clicked: " + data);
});

trigger_event("click", "button1");
```

### Beispiel: Sortierung mit benutzerdefiniertem Vergleicher

```hemlock
fn sort(arr, compare) {
    // Bubble-Sort mit benutzerdefiniertem Vergleicher
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Optionale Parameter (Standardargumente)

Funktionen koennen optionale Parameter mit Standardwerten haben, unter Verwendung der `?:`-Syntax:

```hemlock
fn greet(name, greeting?: "Hello") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Hello Alice"
print(greet("Bob", "Hi"));       // "Hi Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Regeln:**
- Optionale Parameter muessen nach erforderlichen Parametern kommen
- Standardwerte koennen beliebige Ausdruecke sein
- Ausgelassene Argumente verwenden den Standardwert

## Variadische Funktionen (Rest-Parameter)

Funktionen koennen eine variable Anzahl von Argumenten akzeptieren, unter Verwendung von Rest-Parametern (`...`):

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Starting", "Running", "Done");
// INFO: Starting
// INFO: Running
// INFO: Done
```

**Regeln:**
- Der Rest-Parameter muss der letzte Parameter sein
- Der Rest-Parameter sammelt alle verbleibenden Argumente in einem Array
- Kann mit regulaeren und optionalen Parametern kombiniert werden

## Funktionstyp-Annotationen

Funktionstypen ermoeglichen es, die genaue Signatur fuer Funktionsparameter und Rueckgabewerte zu spezifizieren:

### Grundlegende Funktionstypen

```hemlock
// Funktionstyp-Syntax: fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Hoehere Ordnung Funktionstypen

```hemlock
// Funktion die eine Funktion zurueckgibt
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Async-Funktionstypen

```hemlock
// Async-Funktionstyp
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### Funktionstyp-Aliase

```hemlock
// Benannte Funktionstypen fuer Klarheit erstellen
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Const-Parameter

Der `const`-Modifikator verhindert, dass ein Parameter innerhalb der Funktion veraendert wird:

### Grundlegende Const-Parameter

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // FEHLER: kann const-Parameter nicht veraendern
    for (item in items) {
        print(item);   // OK: Lesen ist erlaubt
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Tiefe Unveraenderlichkeit

Const-Parameter erzwingen tiefe Unveraenderlichkeit - keine Mutation ueber irgendeinen Pfad:

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK: Lesen ist erlaubt
    // person.name = "Bob";   // FEHLER: kann nicht veraendern
    // person.address.city = "NYC";  // FEHLER: tiefes const
}
```

### Was Const verhindert

| Typ | Durch Const blockiert | Erlaubt |
|------|-----------------|---------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | Feldzuweisung | Feldlesen |
| buffer | Indexzuweisung | Indexlesen |
| string | Indexzuweisung | alle Methoden (geben neue Strings zurueck) |

## Benannte Argumente

Funktionen koennen mit benannten Argumenten aufgerufen werden fuer Klarheit und Flexibilitaet:

### Grundlegende benannte Argumente

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Positionsargumente (traditionell)
create_user("Alice", 25, false);

// Benannte Argumente - koennen in beliebiger Reihenfolge sein
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Mischen von Positions- und benannten Argumenten

```hemlock
// Optionale Parameter ueberspringen durch Benennen des Benotigten
create_user("David", active: false);  // Verwendet Standard-age=18

// Benannte Argumente muessen nach Positionsargumenten kommen
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // FEHLER: Positionsargument nach benanntem
```

### Regeln fuer benannte Argumente

- Verwende `name: wert`-Syntax fuer benannte Argumente
- Benannte Argumente koennen in beliebiger Reihenfolge nach Positionsargumenten erscheinen
- Positionsargumente koennen nicht auf benannte Argumente folgen
- Funktioniert mit Standard/optionalen Parametern
- Unbekannte Parameternamen verursachen Laufzeitfehler

## Einschraenkungen

Aktuelle Einschraenkungen, die zu beachten sind:

- **Keine Referenzuebergabe** - `ref`-Schluesselwort wird geparst aber nicht implementiert
- **Kein Funktionsueberladen** - Eine Funktion pro Name
- **Keine Tail-Call-Optimierung** - Tiefe Rekursion durch Stack-Groesse begrenzt

## Verwandte Themen

- [Kontrollfluss](control-flow.md) - Funktionen mit Kontrollstrukturen verwenden
- [Objekte](objects.md) - Methoden sind Funktionen in Objekten gespeichert
- [Fehlerbehandlung](error-handling.md) - Funktionen und Ausnahmebehandlung
- [Typen](types.md) - Typannotationen und Konvertierungen

## Siehe auch

- **Closures**: Siehe CLAUDE.md Abschnitt "Functions" fuer Closure-Semantik
- **Erstklassige Werte**: Funktionen sind Werte wie alle anderen
- **Lexikalisches Scoping**: Funktionen erfassen ihre definierende Umgebung
