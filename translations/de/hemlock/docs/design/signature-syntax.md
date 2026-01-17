# Design der Signatur-Syntax

> Erweiterung des Typsystems von Hemlock um Funktionstypen, Nullable-Modifikatoren, Typaliase, Const-Parameter und Methodensignaturen.

**Status:** Implementiert (v1.7.0)
**Version:** 1.0
**Autor:** Claude

---

## Überblick

Dieses Dokument schlägt fünf zusammenhängende Typsystem-Erweiterungen vor, die auf der bestehenden Infrastruktur von Hemlock aufbauen:

1. **Funktionstyp-Annotationen** - Erstklassige Funktionstypen
2. **Nullable-Typ-Modifikatoren** - Explizite Null-Behandlung (erweitert bestehendes `nullable`-Flag)
3. **Typaliase** - Benannte Typabkürzungen
4. **Const-Parameter** - Unveränderlichkeitsverträge
5. **Methodensignaturen in Define** - Interface-ähnliches Verhalten

Diese Features teilen die Philosophie: **explizit statt implizit, optional aber durchgesetzt wenn verwendet**.

---

## 1. Funktionstyp-Annotationen

### Motivation

Derzeit gibt es keine Möglichkeit, die Signatur einer Funktion als Typ auszudrücken:

```hemlock
// Aktuell: callback hat keine Typinformation
fn map(arr: array, callback) { ... }

// Vorgeschlagen: expliziter Funktionstyp
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Syntax

```hemlock
// Einfacher Funktionstyp
fn(i32, i32): i32

// Mit Parameternamen (nur Dokumentation, nicht durchgesetzt)
fn(a: i32, b: i32): i32

// Kein Rückgabewert (void)
fn(string): void
fn(string)              // Kurzform: `: void` weglassen

// Nullbarer Rückgabewert
fn(i32): string?

// Optionale Parameter
fn(name: string, age?: i32): void

// Rest-Parameter
fn(...args: array): i32

// Keine Parameter
fn(): bool

// Höherer Ordnung: Funktion, die Funktion zurückgibt
fn(i32): fn(i32): i32

// Async-Funktionstyp
async fn(i32): i32
```

### Verwendungsbeispiele

```hemlock
// Variable mit Funktionstyp
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Funktionsparameter
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Rückgabetyp ist Funktion
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Array von Funktionen
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// Objektfeld
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### AST-Änderungen

```c
// In TypeKind-Enum (include/ast.h)
typedef enum {
    // ... bestehende Typen ...
    TYPE_FUNCTION,      // NEU: Funktionstyp
} TypeKind;

// In Type-Struct (include/ast.h)
struct Type {
    TypeKind kind;
    // ... bestehende Felder ...

    // Für TYPE_FUNCTION:
    struct Type **param_types;      // Parametertypen
    char **param_names;             // Optionale Parameternamen (Doku)
    int *param_optional;            // Welche Parameter optional sind
    int num_params;
    char *rest_param_name;          // Rest-Parametername oder NULL
    struct Type *rest_param_type;   // Rest-Parametertyp
    struct Type *return_type;       // Rückgabetyp (NULL = void)
    int is_async;                   // async fn-Typ
};
```

### Parsing

Funktionstypen beginnen mit `fn` (oder `async fn`) gefolgt von Parameterliste:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Disambiguierung:** Beim Parsen eines Typs und `fn` wird angetroffen:
- Falls gefolgt von `(`, ist es ein Funktionstyp
- Sonst Syntaxfehler (bloßes `fn` ist kein gültiger Typ)

### Typkompatibilität

```hemlock
// Exakte Übereinstimmung für Funktionstypen erforderlich
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Parameter-Kontravarianz (breitere Typen akzeptieren ist OK)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Rückgabe-Kovarianz (engere Typen zurückgeben ist OK)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Arität muss übereinstimmen
let bad: fn(i32): i32 = fn(a, b) { return a; };       // FEHLER: Arität stimmt nicht überein

// Optionale Parameter kompatibel mit erforderlichen
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Nullable-Typ-Modifikatoren

### Motivation

Das `?`-Suffix macht Null-Akzeptanz in Signaturen explizit:

```hemlock
// Aktuell: unklar ob null gültig ist
fn find(arr: array, val: any): i32 { ... }

// Vorgeschlagen: explizit nullbarer Rückgabewert
fn find(arr: array, val: any): i32? { ... }
```

### Syntax

```hemlock
// Nullbare Typen mit ?-Suffix
string?           // String oder null
i32?              // i32 oder null
User?             // User oder null
array<i32>?       // Array oder null
fn(i32): i32?     // Funktion, die i32 oder null zurückgibt

// Kombination mit Funktionstypen
fn(string?): i32          // Akzeptiert String oder null
fn(string): i32?          // Gibt i32 oder null zurück
fn(string?): i32?         // Beide nullbar

// In Define
define Result {
    value: any?;
    error: string?;
}
```

### Implementierungshinweise

**Existiert bereits:** Das `Type.nullable`-Flag ist bereits im AST. Dieses Feature benötigt hauptsächlich:
1. Parser-Unterstützung für `?`-Suffix bei jedem Typ (verifizieren/erweitern)
2. Ordnungsgemäße Komposition mit Funktionstypen
3. Laufzeit-Durchsetzung

### Typkompatibilität

```hemlock
// Nicht-nullbar kann nullbar zugewiesen werden
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullbar kann NICHT nicht-nullbar zugewiesen werden
let z: i32 = x;             // FEHLER: x könnte null sein

// Null-Koaleszenz zum Auspacken
let z: i32 = x ?? 0;        // OK: ?? liefert Standardwert

// Optionale Verkettung gibt nullbar zurück
let name: string? = user?.name;
```

---

## 3. Typaliase

### Motivation

Komplexe Typen profitieren von benannten Abkürzungen:

```hemlock
// Aktuell: repetitive zusammengesetzte Typen
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// Vorgeschlagen: benannter Alias
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### Syntax

```hemlock
// Einfacher Alias
type Integer = i32;
type Text = string;

// Zusammengesetzter Typ-Alias
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// Funktionstyp-Alias
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Nullbarer Alias
type OptionalString = string?;

// Generischer Alias (falls generische Typaliase unterstützt werden)
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Array-Typ-Alias
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### Scope und Sichtbarkeit

```hemlock
// Standardmäßig modul-begrenzt
type Callback = fn(Event): void;

// Exportierbar
export type Handler = fn(Request): Response;

// In einer anderen Datei
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### AST-Änderungen

```c
// Neuer Statement-Typ
typedef enum {
    // ... bestehende Statements ...
    STMT_TYPE_ALIAS,    // NEU
} StmtKind;

// In Stmt-Union
struct {
    char *name;                 // Aliasname
    char **type_params;         // Generische Parameter: <T, U>
    int num_type_params;
    Type *aliased_type;         // Der eigentliche Typ
} type_alias;
```

### Parsing

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Hinweis:** `type` ist ein neues Schlüsselwort. Auf Konflikte mit bestehenden Bezeichnern prüfen.

### Auflösung

Typaliase werden aufgelöst bei:
- **Parse-Zeit:** Alias wird in Typumgebung aufgezeichnet
- **Prüf-Zeit:** Alias wird zum zugrunde liegenden Typ erweitert
- **Laufzeit:** Alias ist transparent (gleich wie zugrunde liegender Typ)

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32" (nicht "MyInt")
```

---

## 4. Const-Parameter

### Motivation

Unveränderlichkeitsabsicht in Funktionssignaturen signalisieren:

```hemlock
// Aktuell: unklar ob Array modifiziert wird
fn print_all(items: array) { ... }

// Vorgeschlagen: expliziter Unveränderlichkeitsvertrag
fn print_all(const items: array) { ... }
```

### Syntax

```hemlock
// Const-Parameter
fn process(const data: buffer) {
    // data[0] = 0;        // FEHLER: kann const nicht mutieren
    let x = data[0];       // OK: Lesen erlaubt
    return x;
}

// Mehrere Const-Parameter
fn compare(const a: array, const b: array): bool { ... }

// Gemischte const und veränderliche
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK: target ist veränderlich
    }
}

// Const mit Typinferenz
fn log(const msg) {
    print(msg);
}

// Const in Funktionstypen
type Reader = fn(const buffer): i32;
```

### Was Const verhindert

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // FEHLER: mutierende Methode
    arr.pop();           // FEHLER: mutierende Methode
    arr[0] = 5;          // FEHLER: Index-Zuweisung
    arr.clear();         // FEHLER: mutierende Methode
}

fn ok(const arr: array) {
    let x = arr[0];      // OK: Lesen
    let len = len(arr);  // OK: Längenprüfung
    let copy = arr.slice(0, 10);  // OK: erstellt neues Array
    for (item in arr) {  // OK: Iteration
        print(item);
    }
}
```

### Mutierende vs. nicht-mutierende Methoden

| Typ | Mutierend (blockiert durch const) | Nicht-mutierend (erlaubt) |
|-----|-----------------------------------|---------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (in-place) | slice, concat, map, filter, find, contains, first, last, join |
| string | Index-Zuweisung (`s[0] = 'x'`) | alle Methoden (geben neue Strings zurück) |
| buffer | Index-Zuweisung, memset, memcpy (an) | Index-Lesen, slice |
| object | Feld-Zuweisung | Feld-Lesen |

### AST-Änderungen

```c
// In Funktionsausdruck (include/ast.h)
struct {
    // ... bestehende Felder ...
    int *param_is_const;    // NEU: 1 wenn const, 0 sonst
} function;

// In Type-Struct für Funktionstypen
struct Type {
    // ... bestehende Felder ...
    int *param_is_const;    // Für TYPE_FUNCTION
};
```

### Durchsetzung

**Interpreter:**
- Const-heit in Variablenbindungen verfolgen
- Vor Mutationsoperationen prüfen
- Laufzeitfehler bei Const-Verletzung

**Compiler:**
- Const-qualifizierte C-Variablen emittieren wo vorteilhaft
- Statische Analyse für Const-Verletzungen
- Warnung/Fehler zur Kompilierzeit

---

## 5. Methodensignaturen in Define

### Motivation

`define`-Blöcken erlauben, erwartete Methoden zu spezifizieren, nicht nur Datenfelder:

```hemlock
// Aktuell: nur Datenfelder
define User {
    name: string;
    age: i32;
}

// Vorgeschlagen: Methodensignaturen
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // Statische Methode
}
```

### Syntax

```hemlock
// Methodensignatur (kein Body)
define Hashable {
    fn hash(): i32;
}

// Mehrere Methoden
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// Gemischte Felder und Methoden
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Self-Typ verwenden
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// Optionale Methoden
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // Optionale Methode (kann fehlen)
}

// Methoden mit Standard-Implementierungen
define Ordered {
    fn compare(other: Self): i32;  // Erforderlich

    // Standard-Implementierungen (geerbt wenn nicht überschrieben)
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### Der `Self`-Typ

`Self` bezieht sich auf den konkreten Typ, der das Interface implementiert:

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// Bei Verwendung:
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### Strukturelle Typisierung (Duck-Typing)

Methodensignaturen verwenden das gleiche Duck-Typing wie Felder:

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// Jedes Objekt mit to_string()-Methode erfüllt Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// Zusammengesetzte Typen mit Methoden
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### AST-Änderungen

```c
// define_object in Stmt-Union erweitern
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Felder (bestehend)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Methoden (NEU)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Optionale Methoden (fn name?(): type)
    Expr **method_defaults;     // Standard-Implementierungen (NULL wenn nur Signatur)
    int num_methods;
} define_object;
```

### Typprüfung

Beim Prüfen von `value: InterfaceType`:
1. Prüfen dass alle erforderlichen Felder mit kompatiblen Typen existieren
2. Prüfen dass alle erforderlichen Methoden mit kompatiblen Signaturen existieren
3. Optionale Felder/Methoden dürfen fehlen

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// Gültig: hat compare-Methode
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Ungültig: fehlendes compare
let invalid: Sortable = { value: 10 };  // FEHLER: fehlende Methode 'compare'

// Ungültig: falsche Signatur
let wrong: Sortable = {
    compare: fn() { return 0; }  // FEHLER: erwartet (Self): i32
};
```

---

## Interaktionsbeispiele

### Alle Features kombinieren

```hemlock
// Typalias für komplexen Funktionstyp
type EventCallback = fn(event: Event, context: Context?): bool;

// Typalias für zusammengesetztes Interface
type Entity = HasId & HasName & Serializable;

// Define mit Methodensignaturen
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// Alles zusammen verwenden
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### Callbacks mit expliziten Typen

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Nullbare Funktionstypen

```hemlock
// Optionaler Callback
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// Nullbarer Rückgabewert vom Funktionstyp
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## Implementierungs-Roadmap

### Phase 1: Kern-Infrastruktur
1. `TYPE_FUNCTION` zum TypeKind-Enum hinzufügen
2. Type-Struct mit Funktionstyp-Feldern erweitern
3. `CHECKED_FUNCTION` zum Compiler-Typprüfer hinzufügen
4. `Self`-Typ-Unterstützung hinzufügen (TYPE_SELF)

### Phase 2: Parsing
1. `parse_function_type()` im Parser implementieren
2. `fn(...)` in Typposition behandeln
3. `type`-Schlüsselwort und `STMT_TYPE_ALIAS`-Parsing hinzufügen
4. `const`-Parameter-Modifikator-Parsing hinzufügen
5. Define-Parsing für Methodensignaturen erweitern

### Phase 3: Typprüfung
1. Funktionstyp-Kompatibilitätsregeln
2. Typalias-Auflösung und -Erweiterung
3. Const-Parameter-Mutationsprüfung
4. Methodensignatur-Validierung in Define-Typen
5. Self-Typ-Auflösung

### Phase 4: Laufzeit
1. Funktionstyp-Validierung an Aufrufstellen
2. Const-Verletzungserkennung
3. Typalias-Transparenz

### Phase 5: Paritätstests
1. Funktionstyp-Annotationstests
2. Nullable-Kompositionstests
3. Typalias-Tests
4. Const-Parameter-Tests
5. Methodensignatur-Tests

---

## Designentscheidungen

### 1. Generische Typaliase: **JA**

Typaliase unterstützen generische Parameter:

```hemlock
// Generische Typaliase
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Verwendung
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Const-Propagierung: **TIEF**

Const-Parameter sind vollständig unveränderlich - keine Mutation über irgendeinen Pfad:

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // FEHLER: kann const-Array nicht mutieren
    arr[0] = {};         // FEHLER: kann const-Array nicht mutieren
    arr[0].x = 5;        // FEHLER: kann nicht durch const mutieren (TIEF)

    let x = arr[0].x;    // OK: Lesen ist in Ordnung
    let copy = arr[0];   // OK: erstellt eine Kopie
    copy.x = 5;          // OK: Kopie ist nicht const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // FEHLER: tiefes const verhindert verschachtelte Mutation
    obj.items[0] = 1;    // FEHLER: tiefes const verhindert verschachtelte Mutation
}
```

**Begründung:** Tiefes const bietet stärkere Garantien und ist nützlicher, um
Datenintegrität zu gewährleisten. Wenn Sie verschachtelte Daten mutieren müssen, erstellen Sie zuerst eine Kopie.

### 3. Self in eigenständigen Typaliasen: **NEIN**

`Self` ist nur innerhalb von `define`-Blöcken gültig, wo es eine klare Bedeutung hat:

```hemlock
// Gültig: Self bezieht sich auf den definierten Typ
define Comparable {
    fn compare(other: Self): i32;
}

// Ungültig: Self hat hier keine Bedeutung
type Cloner = fn(Self): Self;  // FEHLER: Self außerhalb des Define-Kontexts

// Stattdessen Generics verwenden:
type Cloner<T> = fn(T): T;
```

### 4. Methoden-Standard-Implementierungen: **JA (nur einfache)**

Erlauben Sie Standard-Implementierungen für einfache/Hilfsmethoden:

```hemlock
define Comparable {
    // Erforderlich: muss implementiert werden
    fn compare(other: Self): i32;

    // Standard-Implementierungen (einfache Hilfsmethoden)
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // Standard: delegiert an erforderliche Methode
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// Objekt muss nur erforderliche Methoden implementieren
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_than werden von Standards geerbt
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**Richtlinien für Standards:**
- Halten Sie sie einfach (1-3 Zeilen)
- Sollten an erforderliche Methoden delegieren
- Keine komplexe Logik oder Nebeneffekte
- Nur Primitiven und einfache Kompositionen

### 5. Varianz: **INFERIERT (keine expliziten Annotationen)**

Varianz wird aus der Verwendung von Typparametern inferiert:

```hemlock
// Varianz ist automatisch basierend auf Position
type Producer<T> = fn(): T;           // T in Rückgabe = kovariant
type Consumer<T> = fn(T): void;       // T in Parameter = kontravariant
type Transformer<T> = fn(T): T;       // T in beiden = invariant

// Beispiel: Dog <: Animal (Dog ist Subtyp von Animal)
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK: kovariant

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK: kontravariant
```

**Warum inferieren?**
- Weniger Boilerplate (`<out T>` / `<in T>` fügt Rauschen hinzu)
- Folgt "explizit statt implizit" - die Position IST explizit
- Entspricht der Behandlung von Funktionstyp-Varianz in den meisten Sprachen
- Fehler sind klar, wenn Varianzregeln verletzt werden

---

## Anhang: Grammatik-Änderungen

```ebnf
(* Typen *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* Statements *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" markiert optionale Methode, block liefert Standard-Implementierung *)

(* Parameter *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
