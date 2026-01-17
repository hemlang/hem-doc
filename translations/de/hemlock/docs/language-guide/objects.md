# Objekte

Hemlock implementiert JavaScript-ähnliche Objekte mit Heap-Allokation, dynamischen Feldern, Methoden und Duck-Typing. Objekte sind flexible Datenstrukturen, die Daten und Verhalten kombinieren.

## Überblick

```hemlock
// Anonymes Objekt
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// Objekt mit Methoden
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Objektliterale

### Grundlegende Syntax

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**Syntax:**
- Geschweifte Klammern `{}` umschliessen das Objekt
- Schlüssel-Wert-Paare durch Kommas getrennt
- Schlüssel sind Bezeichner (keine Anführungszeichen nötig)
- Werte können jeden Typ haben

### Leere Objekte

```hemlock
let obj = {};  // Leeres Objekt

// Felder später hinzufügen
obj.name = "Alice";
obj.age = 30;
```

### Verschachtelte Objekte

```hemlock
let user = {
    info: {
        name: "Bob",
        age: 25
    },
    active: true,
    settings: {
        theme: "dark",
        notifications: true
    }
};

print(user.info.name);           // "Bob"
print(user.settings.theme);      // "dark"
```

### Gemischte Werttypen

```hemlock
let mixed = {
    number: 42,
    text: "hello",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### Kurzschreibweise für Eigenschaften

Wenn ein Variablenname mit dem Eigenschaftsnamen übereinstimmt, verwenden Sie die Kurzschreibweise:

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Kurzschreibweise: { name } ist äquivalent zu { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Kurzschreibweise mit regulaeren Eigenschaften mischen:**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### Spread-Operator

Der Spread-Operator (`...`) kopiert alle Felder von einem Objekt in ein anderes:

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Werte mit Spread ueberschreiben:**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (überschrieben)
print(custom.size);   // "medium" (von defaults)
print(custom.debug);  // false (von defaults)
```

**Mehrere Spreads (spätere Spreads ueberschreiben fruehere):**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// Spaeterer Spread überschreibt frueheren
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**Kurzschreibweise und Spread kombinieren:**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**Konfigurationsueberschreibungsmuster:**
```hemlock
let defaultConfig = {
    debug: false,
    timeout: 30,
    retries: 3
};

let prodConfig = { ...defaultConfig, timeout: 60 };
let devConfig = { ...defaultConfig, debug: true };

print(prodConfig.timeout);  // 60
print(devConfig.debug);     // true
```

**Hinweis:** Spread führt eine flache Kopie durch. Verschachtelte Objekte teilen Referenzen:
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (gleiche Referenz wie nested.inner)
```

## Feldzugriff

### Punkt-Notation

```hemlock
let person = { name: "Alice", age: 30 };

// Feld lesen
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Feld ändern
person.age = 31;
print(person.age);           // 31
```

### Dynamisches Hinzufügen von Feldern

Neue Felder zur Laufzeit hinzufügen:

```hemlock
let person = { name: "Alice" };

// Neues Feld hinzufügen
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Feldloeschung

**Hinweis:** Feldloeschung wird derzeit nicht unterstützt. Setzen Sie stattdessen auf `null`:

```hemlock
let obj = { x: 10, y: 20 };

// Felder können nicht gelöscht werden (nicht unterstützt)
// obj.x = undefined;  // Kein 'undefined' in Hemlock

// Workaround: Auf null setzen
obj.x = null;
```

## Methoden und `self`

### Methoden definieren

Methoden sind Funktionen, die in Objektfeldern gespeichert sind:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
    decrement: fn() {
        self.count = self.count - 1;
    },
    get: fn() {
        return self.count;
    }
};
```

### Das Schlüsselwort `self`

Wenn eine Funktion als Methode aufgerufen wird, wird `self` automatisch an das Objekt gebunden:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self verweist auf counter
    }
};

counter.increment();  // self ist an counter gebunden
print(counter.count);  // 1
```

**Funktionsweise:**
- Methodenaufrufe werden erkannt, indem geprüft wird, ob der Funktionsausdruck ein Eigenschaftszugriff ist
- `self` wird automatisch zum Aufrufzeitpunkt an das Objekt gebunden
- `self` ist schreibgeschuetzt (man kann `self` selbst nicht neu zuweisen)

### Methodenaufruf-Erkennung

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Als Methode aufgerufen - self ist gebunden
print(obj.method());  // 10

// Als Funktion aufgerufen - self ist null (Fehler)
let f = obj.method;
print(f());  // FEHLER: self ist nicht definiert
```

### Methoden mit Parametern

```hemlock
let calculator = {
    result: 0,
    add: fn(x) {
        self.result = self.result + x;
    },
    multiply: fn(x) {
        self.result = self.result * x;
    },
    get: fn() {
        return self.result;
    }
};

calculator.add(5);
calculator.multiply(2);
print(calculator.get());  // 10
```

## Typdefinitionen mit `define`

### Grundlegende Typdefinition

Objektstrukturen mit `define` definieren:

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Objekt erstellen und typisierter Variable zuweisen
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Duck-Typing validiert Struktur

print(typeof(typed_p));  // "Person"
```

**Was `define` macht:**
- Deklariert einen Typ mit erforderlichen Feldern
- Ermöglicht Duck-Typing-Validierung
- Setzt den Typnamen des Objekts für `typeof()`

### Duck-Typing

Objekte werden gegen `define` mittels **struktureller Kompatibilitaet** validiert:

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Hat alle erforderlichen Felder
let p1: Person = { name: "Alice", age: 30 };

// OK: Zusätzliche Felder sind erlaubt
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// FEHLER: Fehlendes erforderliches Feld 'age'
let p3: Person = { name: "Carol" };

// FEHLER: Falscher Typ für 'age'
let p4: Person = { name: "Dave", age: "dreissig" };
```

**Duck-Typing-Regeln:**
- Alle erforderlichen Felder müssen vorhanden sein
- Feldtypen müssen übereinstimmen
- Zusätzliche Felder sind erlaubt und werden beibehalten
- Validierung erfolgt zum Zuweisungszeitpunkt

### Optionale Felder

Felder können mit Standardwerten optional sein:

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Optional mit Standardwert
    nickname?: string,   // Optional, Standard ist null
}

// Objekt mit nur erforderlichen Feldern
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (Standard angewendet)
print(typed_p.nickname);  // null (kein Standard)

// Optionale Felder können überschrieben werden
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (überschrieben)
```

**Syntax für optionale Felder:**
- `field?: default_value` - Optional mit Standard
- `field?: type` - Optional mit Typannotation, Standard ist null
- Optionale Felder werden beim Duck-Typing hinzugefügt, falls fehlend

### Typprüfung

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // Typprüfung erfolgt hier

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (Original ist immer noch anonym)
```

**Wann Typprüfung erfolgt:**
- Zum Zuweisungszeitpunkt an typisierte Variable
- Validiert, dass alle erforderlichen Felder vorhanden sind
- Validiert, dass Feldtypen übereinstimmen (mit impliziten Konvertierungen)
- Setzt den Typnamen des Objekts

## Methodensignaturen in Define

Define-Blöcke können Methodensignaturen spezifizieren und erstellen Interface-ähnliche Verträge:

### Erforderliche Methoden

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Erforderliche Methodensignatur
}

// Objekte müssen die erforderliche Methode bereitstellen
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Optionale Methoden

```hemlock
define Serializable {
    fn serialize(): string;       // Erforderlich
    fn pretty?(): string;         // Optionale Methode (kann fehlen)
}
```

### Der `Self`-Typ

`Self` verweist auf den zu definierenden Typ und ermöglicht rekursive Typdefinitionen:

```hemlock
define Cloneable {
    fn clone(): Self;  // Gibt denselben Typ wie das Objekt zurück
}

define Comparable {
    fn compare(other: Self): i32;  // Nimmt denselben Typ als Parameter
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Gemischte Felder und Methoden

```hemlock
define Entity {
    id: i32,
    name: string,
    fn validate(): bool;
    fn serialize(): string;
}

let user: Entity = {
    id: 1,
    name: "Alice",
    validate: fn() { return self.id > 0 && self.name != ""; },
    serialize: fn() { return '{"id":' + self.id + ',"name":"' + self.name + '"}'; }
};
```

## Zusammengesetzte Typen (Schnittmengentypen)

Zusammengesetzte Typen verwenden `&`, um zu verlangen, dass ein Objekt mehrere Typdefinitionen erfüllt:

### Grundlegende zusammengesetzte Typen

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Zusammengesetzter Typ: Objekt muss ALLE Typen erfüllen
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Funktionsparameter mit zusammengesetzten Typen

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " ist " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // Zusätzliche Felder OK
```

### Drei oder mehr Typen

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Typaliasse für zusammengesetzte Typen

```hemlock
// Benannten Alias für zusammengesetzten Typ erstellen
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Duck-Typing mit zusammengesetzten Typen:** Zusätzliche Felder sind immer erlaubt - das Objekt muss nur mindestens die von allen Komponententypen geforderten Felder haben.

## JSON-Serialisierung

### Zu JSON serialisieren

Objekte in JSON-Strings konvertieren:

```hemlock
// obj.serialize() - Objekt in JSON-String konvertieren
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Verschachtelte Objekte
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Von JSON deserialisieren

JSON-Strings zurück in Objekte parsen:

```hemlock
// json.deserialize() - JSON-String in Objekt parsen
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Zyklenerkennung

Zirkulaere Referenzen werden erkannt und verursachen Fehler:

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Zirkulaere Referenz erstellen

obj.serialize();  // FEHLER: serialize() hat zirkulaere Referenz erkannt
```

### Unterstuetzte Typen

JSON-Serialisierung unterstützt:

- **Zahlen**: i8-i32, u8-u32, f32, f64
- **Booleans**: true, false
- **Strings**: Mit Escape-Sequenzen
- **Null**: null-Wert
- **Objekte**: Verschachtelte Objekte
- **Arrays**: Verschachtelte Arrays

**Nicht unterstützt:**
- Funktionen (werden still ausgelassen)
- Pointer (Fehler)
- Buffer (Fehler)

### Fehlerbehandlung

Serialisierung und Deserialisierung können Fehler werfen:

```hemlock
// Ungueltiges JSON wirft einen Fehler
try {
    let bad = "kein gueltiges json".deserialize();
} catch (e) {
    print("Parse-Fehler:", e);
}

// Pointer können nicht serialisiert werden
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialisierungsfehler:", e);
}
```

### Round-Trip-Beispiel

Vollstaendiges Beispiel für Serialisierung und Deserialisierung:

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Erstellen und serialisieren
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Zurück deserialisieren
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Eingebaute Funktionen

### `typeof(value)`

Gibt den Typnamen als String zurück:

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Rueckgabewerte:**
- Anonyme Objekte: `"object"`
- Typisierte Objekte: Benutzerdefinierter Typname (z.B. `"Person"`)

## Implementierungsdetails

### Speichermodell

- **Heap-allokiert** - Alle Objekte werden auf dem Heap allokiert
- **Flache Kopie** - Zuweisung kopiert die Referenz, nicht das Objekt
- **Dynamische Felder** - Gespeichert als dynamische Arrays von Name/Wert-Paaren
- **Referenzgezählt** - Objekte werden automatisch freigegeben, wenn der Gültigkeitsbereich endet

### Referenzsemantik

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Flache Kopie (gleiche Referenz)

obj2.x = 20;
print(obj1.x);  // 20 (beide verweisen auf dasselbe Objekt)
```

### Methodenspeicherung

Methoden sind einfach Funktionen, die in Feldern gespeichert sind:

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method ist eine Funktion, die in obj.method gespeichert ist
print(typeof(obj.method));  // "function"
```

## Gängige Muster

### Muster: Konstruktorfunktion

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hallo, ich bin " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hallo, ich bin Alice"
```

### Muster: Objekt-Builder

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Verkettung ermöglichen
        },

        setAge: fn(a) {
            self.age = a;
            return self;
        },

        build: fn() {
            return { name: self.name, age: self.age };
        }
    };
}

let person = PersonBuilder()
    .setName("Alice")
    .setAge(30)
    .build();
```

### Muster: Zustandsobjekt

```hemlock
let state = {
    status: "idle",
    data: null,
    error: null,

    setState: fn(new_status) {
        self.status = new_status;
    },

    setData: fn(new_data) {
        self.data = new_data;
        self.status = "success";
    },

    setError: fn(err) {
        self.error = err;
        self.status = "error";
    }
};
```

### Muster: Konfigurationsobjekt

```hemlock
let config = {
    defaults: {
        timeout: 30,
        retries: 3,
        debug: false
    },

    get: fn(key) {
        if (self.defaults[key] != null) {
            return self.defaults[key];
        }
        return null;
    },

    set: fn(key, value) {
        self.defaults[key] = value;
    }
};
```

## Best Practices

1. **`define` für Struktur verwenden** - Erwartete Objektstrukturen dokumentieren
2. **Factory-Funktionen bevorzugen** - Objekte mit Konstruktoren erstellen
3. **Objekte einfach halten** - Nicht zu tief verschachteln
4. **`self`-Verwendung dokumentieren** - Methodenverhalten klar machen
5. **Bei Zuweisung validieren** - Duck-Typing verwenden, um Fehler frueh zu erkennen
6. **Zirkulaere Referenzen vermeiden** - Verursachen Serialisierungsfehler
7. **Optionale Felder verwenden** - Sinnvolle Standardwerte bereitstellen

## Häufige Fallstricke

### Fallstrick: Referenz vs. Wert

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Flache Kopie

obj2.x = 20;
print(obj1.x);  // 20 (Ueberraschung! Beide haben sich geändert)

// Um das zu vermeiden: Neues Objekt erstellen
let obj3 = { x: obj1.x };  // Tiefe Kopie (manuell)
```

### Fallstrick: `self` bei Nicht-Methodenaufrufen

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Funktioniert: Als Methode aufgerufen
print(obj.method());  // 10

// FEHLER: Als Funktion aufgerufen
let f = obj.method;
print(f());  // FEHLER: self ist nicht definiert
```

### Fallstrick: Rohe Pointer in Objekten

```hemlock
// Objekte werden automatisch freigegeben, aber rohe Pointer darin NICHT
fn create_objects() {
    let obj = { data: alloc(1000) };  // roher ptr braucht manuelles free
    // obj wird automatisch freigegeben, wenn Bereich endet, aber obj.data leckt!
}

// Lösung: Rohe Pointer vor Bereichsende freigeben
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... obj.data verwenden ...
    free(obj.data);  // Rohen Pointer explizit freigeben
}  // obj selbst wird automatisch freigegeben
```

### Fallstrick: Typverwirrung

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// FEHLER: Fehlendes erforderliches Feld 'y'
let p: Point = obj;
```

## Beispiele

### Beispiel: Vektormathematik

```hemlock
fn createVector(x, y) {
    return {
        x: x,
        y: y,

        add: fn(other) {
            return createVector(
                self.x + other.x,
                self.y + other.y
            );
        },

        length: fn() {
            return sqrt(self.x * self.x + self.y * self.y);
        },

        toString: fn() {
            return "(" + typeof(self.x) + ", " + typeof(self.y) + ")";
        }
    };
}

let v1 = createVector(3, 4);
let v2 = createVector(1, 2);
let v3 = v1.add(v2);

print(v3.toString());  // "(4, 6)"
```

### Beispiel: Einfache Datenbank

```hemlock
fn createDatabase() {
    let records = [];
    let next_id = 1;

    return {
        insert: fn(data) {
            let record = { id: next_id, data: data };
            records.push(record);
            next_id = next_id + 1;
            return record.id;
        },

        find: fn(id) {
            let i = 0;
            while (i < records.length) {
                if (records[i].id == id) {
                    return records[i];
                }
                i = i + 1;
            }
            return null;
        },

        count: fn() {
            return records.length;
        }
    };
}

let db = createDatabase();
let id = db.insert({ name: "Alice", age: 30 });
let record = db.find(id);
print(record.data.name);  // "Alice"
```

### Beispiel: Event-Emitter

```hemlock
fn createEventEmitter() {
    let listeners = {};

    return {
        on: fn(event, handler) {
            if (listeners[event] == null) {
                listeners[event] = [];
            }
            listeners[event].push(handler);
        },

        emit: fn(event, data) {
            if (listeners[event] != null) {
                let i = 0;
                while (i < listeners[event].length) {
                    listeners[event][i](data);
                    i = i + 1;
                }
            }
        }
    };
}

let emitter = createEventEmitter();

emitter.on("message", fn(data) {
    print("Empfangen: " + data);
});

emitter.emit("message", "Hallo!");
```

## Einschränkungen

Aktuelle Einschränkungen:

- **Keine tiefe Kopie** - Verschachtelte Objekte müssen manuell kopiert werden (Spread ist flach)
- **Keine Wertuebergabe** - Objekte werden immer als Referenz übergeben
- **Keine berechneten Eigenschaften** - Keine `{[key]: value}`-Syntax
- **`self` ist schreibgeschuetzt** - Kann `self` in Methoden nicht neu zuweisen
- **Keine Eigenschaftsloeschung** - Felder können nicht entfernt werden, sobald sie hinzugefügt sind

**Hinweis:** Objekte sind referenzgezählt und werden automatisch freigegeben, wenn der Gültigkeitsbereich endet. Siehe [Speicherverwaltung](memory.md#internal-reference-counting) für Details.

## Verwandte Themen

- [Functions](functions.md) - Methoden sind Funktionen, die in Objekten gespeichert sind
- [Arrays](arrays.md) - Arrays sind ebenfalls objektaehnlich
- [Types](types.md) - Duck-Typing und Typdefinitionen
- [Error Handling](error-handling.md) - Fehlerobjekte werfen

## Siehe auch

- **Duck-Typing**: Siehe CLAUDE.md Abschnitt "Objects" für Duck-Typing-Details
- **JSON**: Siehe CLAUDE.md für JSON-Serialisierungsdetails
- **Speicher**: Siehe [Memory](memory.md) für Objekt-Allokation
