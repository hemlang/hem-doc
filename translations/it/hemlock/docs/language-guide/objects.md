# Oggetti

Hemlock implementa oggetti in stile JavaScript con allocazione nell'heap, campi dinamici, metodi e duck typing. Gli oggetti sono strutture dati flessibili che combinano dati e comportamento.

## Panoramica

```hemlock
// Oggetto anonimo
let person = { name: "Alice", age: 30, city: "Roma" };
print(person.name);  // "Alice"

// Oggetto con metodi
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Letterali oggetto

### Sintassi di base

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "Roma"
};
```

**Sintassi:**
- Le parentesi graffe `{}` racchiudono l'oggetto
- Coppie chiave-valore separate da virgole
- Le chiavi sono identificatori (non servono virgolette)
- I valori possono essere di qualsiasi tipo

### Oggetti vuoti

```hemlock
let obj = {};  // Oggetto vuoto

// Aggiungi campi dopo
obj.name = "Alice";
obj.age = 30;
```

### Oggetti annidati

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

### Tipi di valore misti

```hemlock
let mixed = {
    number: 42,
    text: "ciao",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### Sintassi abbreviata delle proprieta

Quando il nome di una variabile corrisponde al nome della proprieta, usa la sintassi abbreviata:

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Abbreviazione: { name } e equivalente a { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Mescola abbreviazione con proprieta normali:**
```hemlock
let city = "Roma";
let obj = { name, age, city, role: "admin" };
```

### Operatore spread

L'operatore spread (`...`) copia tutti i campi da un oggetto in un altro:

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Sovrascrivere valori con spread:**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (sovrascritto)
print(custom.size);   // "medium" (dai defaults)
print(custom.debug);  // false (dai defaults)
```

**Spread multipli (gli spread successivi sovrascrivono i precedenti):**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// Lo spread successivo sovrascrive il precedente
let first = { val: "primo" };
let second = { val: "secondo" };
let combined = { ...first, ...second };
print(combined.val);  // "secondo"
```

**Combina abbreviazione e spread:**
```hemlock
let status = "active";
let data = { id: 1, name: "Elemento" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Elemento"
print(full.status);  // "active"
```

**Pattern di override della configurazione:**
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

**Nota:** Lo spread esegue una copia superficiale. Gli oggetti annidati condividono i riferimenti:
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (stesso riferimento di nested.inner)
```

## Accesso ai campi

### Notazione punto

```hemlock
let person = { name: "Alice", age: 30 };

// Leggi campo
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Modifica campo
person.age = 31;
print(person.age);           // 31
```

### Aggiunta dinamica di campi

Aggiungi nuovi campi a runtime:

```hemlock
let person = { name: "Alice" };

// Aggiungi nuovo campo
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Eliminazione dei campi

**Nota:** L'eliminazione dei campi non e attualmente supportata. Imposta a `null` invece:

```hemlock
let obj = { x: 10, y: 20 };

// Non puoi eliminare campi (non supportato)
// obj.x = undefined;  // Nessun 'undefined' in Hemlock

// Workaround: Imposta a null
obj.x = null;
```

## Metodi e `self`

### Definire metodi

I metodi sono funzioni memorizzate nei campi dell'oggetto:

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

### La parola chiave `self`

Quando una funzione viene chiamata come metodo, `self` viene automaticamente associato all'oggetto:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self si riferisce a counter
    }
};

counter.increment();  // self e associato a counter
print(counter.count);  // 1
```

**Come funziona:**
- Le chiamate di metodo vengono rilevate verificando se l'espressione funzione e un accesso a proprieta
- `self` viene automaticamente associato all'oggetto al momento della chiamata
- `self` e di sola lettura (non puoi riassegnare `self` stesso)

### Rilevamento della chiamata di metodo

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Chiamato come metodo - self e associato
print(obj.method());  // 10

// Chiamato come funzione - self e null (errore)
let f = obj.method;
print(f());  // ERRORE: self non e definito
```

### Metodi con parametri

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

## Definizioni di tipo con `define`

### Definizione di tipo di base

Definisci le forme degli oggetti con `define`:

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Crea oggetto e assegna a variabile tipizzata
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Il duck typing valida la struttura

print(typeof(typed_p));  // "Person"
```

**Cosa fa `define`:**
- Dichiara un tipo con campi richiesti
- Abilita la validazione duck typing
- Imposta il nome del tipo dell'oggetto per `typeof()`

### Duck Typing

Gli oggetti vengono validati contro `define` usando la **compatibilita strutturale**:

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Ha tutti i campi richiesti
let p1: Person = { name: "Alice", age: 30 };

// OK: Campi extra consentiti
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "Roma",
    active: true
};

// ERRORE: Campo richiesto 'age' mancante
let p3: Person = { name: "Carol" };

// ERRORE: Tipo sbagliato per 'age'
let p4: Person = { name: "Dave", age: "trenta" };
```

**Regole del duck typing:**
- Tutti i campi richiesti devono essere presenti
- I tipi dei campi devono corrispondere
- I campi extra sono consentiti e preservati
- La validazione avviene al momento dell'assegnazione

### Campi opzionali

I campi possono essere opzionali con valori predefiniti:

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Opzionale con valore predefinito
    nickname?: string,   // Opzionale, predefinito a null
}

// Oggetto con solo campi richiesti
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (predefinito applicato)
print(typed_p.nickname);  // null (nessun predefinito)

// Puo sovrascrivere i campi opzionali
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (sovrascritto)
```

**Sintassi dei campi opzionali:**
- `campo?: valore_predefinito` - Opzionale con predefinito
- `campo?: tipo` - Opzionale con annotazione di tipo, predefinito a null
- I campi opzionali vengono aggiunti durante il duck typing se mancanti

### Verifica del tipo

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // La verifica del tipo avviene qui

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (l'originale e ancora anonimo)
```

**Quando avviene la verifica del tipo:**
- Al momento dell'assegnazione alla variabile tipizzata
- Valida che tutti i campi richiesti siano presenti
- Valida che i tipi dei campi corrispondano (con conversioni implicite)
- Imposta il nome del tipo dell'oggetto

## Firme di metodo in Define

I blocchi define possono specificare firme di metodo, creando contratti simili alle interfacce:

### Metodi richiesti

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Firma di metodo richiesta
}

// Gli oggetti devono fornire il metodo richiesto
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Metodi opzionali

```hemlock
define Serializable {
    fn serialize(): string;       // Richiesto
    fn pretty?(): string;         // Metodo opzionale (puo essere assente)
}
```

### Il tipo `Self`

`Self` si riferisce al tipo che viene definito, consentendo definizioni di tipo ricorsive:

```hemlock
define Cloneable {
    fn clone(): Self;  // Restituisce lo stesso tipo dell'oggetto
}

define Comparable {
    fn compare(other: Self): i32;  // Prende lo stesso tipo come parametro
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Campi e metodi misti

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

## Tipi composti (Tipi intersezione)

I tipi composti usano `&` per richiedere che un oggetto soddisfi piu definizioni di tipo:

### Tipi composti di base

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Tipo composto: l'oggetto deve soddisfare TUTTI i tipi
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Parametri di funzione con tipi composti

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " ha " + p.age + " anni");
}

greet({ name: "Bob", age: 25, city: "Roma" });  // Campi extra OK
```

### Tre o piu tipi

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Alias di tipo per tipi composti

```hemlock
// Crea un alias con nome per un tipo composto
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Duck typing con composti:** I campi extra sono sempre consentiti - l'oggetto deve solo avere almeno i campi richiesti da tutti i tipi componenti.

## Serializzazione JSON

### Serializzare in JSON

Converti oggetti in stringhe JSON:

```hemlock
// obj.serialize() - Converti oggetto in stringa JSON
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Oggetti annidati
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Deserializzare da JSON

Analizza stringhe JSON in oggetti:

```hemlock
// json.deserialize() - Analizza stringa JSON in oggetto
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Rilevamento dei cicli

I riferimenti circolari vengono rilevati e causano errori:

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Crea riferimento circolare

obj.serialize();  // ERRORE: serialize() ha rilevato riferimento circolare
```

### Tipi supportati

La serializzazione JSON supporta:

- **Numeri**: i8-i32, u8-u32, f32, f64
- **Booleani**: true, false
- **Stringhe**: Con sequenze di escape
- **Null**: valore null
- **Oggetti**: Oggetti annidati
- **Array**: Array annidati

**Non supportati:**
- Funzioni (omesse silenziosamente)
- Puntatori (errore)
- Buffer (errore)

### Gestione degli errori

La serializzazione e deserializzazione possono generare errori:

```hemlock
// JSON non valido genera un errore
try {
    let bad = "json non valido".deserialize();
} catch (e) {
    print("Errore di parsing:", e);
}

// I puntatori non possono essere serializzati
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Errore di serializzazione:", e);
}
```

### Esempio round-trip

Esempio completo di serializzazione e deserializzazione:

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Crea e serializza
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Deserializza
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Funzioni integrate

### `typeof(value)`

Restituisce il nome del tipo come stringa:

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Valori restituiti:**
- Oggetti anonimi: `"object"`
- Oggetti tipizzati: Nome del tipo personalizzato (es. `"Person"`)

## Dettagli di implementazione

### Modello di memoria

- **Allocato nell'heap** - Tutti gli oggetti sono allocati nell'heap
- **Copia superficiale** - L'assegnazione copia il riferimento, non l'oggetto
- **Campi dinamici** - Memorizzati come array dinamici di coppie nome/valore
- **Conteggiati per riferimento** - Gli oggetti vengono liberati automaticamente quando lo scope termina

### Semantica dei riferimenti

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copia superficiale (stesso riferimento)

obj2.x = 20;
print(obj1.x);  // 20 (entrambi si riferiscono allo stesso oggetto)
```

### Memorizzazione dei metodi

I metodi sono semplicemente funzioni memorizzate nei campi:

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method e una funzione memorizzata in obj.method
print(typeof(obj.method));  // "function"
```

## Pattern comuni

### Pattern: Funzione costruttore

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Ciao, sono " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Ciao, sono Alice"
```

### Pattern: Object builder

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Abilita il concatenamento
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

### Pattern: Oggetto stato

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

### Pattern: Oggetto configurazione

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

## Buone pratiche

1. **Usa `define` per la struttura** - Documenta le forme degli oggetti attese
2. **Preferisci le funzioni factory** - Crea oggetti con costruttori
3. **Mantieni gli oggetti semplici** - Non annidare troppo profondamente
4. **Documenta l'uso di `self`** - Rendi chiaro il comportamento dei metodi
5. **Valida all'assegnazione** - Usa il duck typing per catturare gli errori presto
6. **Evita i riferimenti circolari** - Causeranno errori di serializzazione
7. **Usa i campi opzionali** - Fornisci valori predefiniti sensati

## Trabocchetti comuni

### Trabocchetto: Riferimento vs. Valore

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copia superficiale

obj2.x = 20;
print(obj1.x);  // 20 (sorpresa! entrambi sono cambiati)

// Per evitare: Crea nuovo oggetto
let obj3 = { x: obj1.x };  // Copia profonda (manuale)
```

### Trabocchetto: `self` in chiamate non-metodo

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Funziona: Chiamato come metodo
print(obj.method());  // 10

// ERRORE: Chiamato come funzione
let f = obj.method;
print(f());  // ERRORE: self non e definito
```

### Trabocchetto: Puntatori raw negli oggetti

```hemlock
// Gli oggetti vengono liberati automaticamente, ma i puntatori raw dentro NON lo sono
fn create_objects() {
    let obj = { data: alloc(1000) };  // ptr raw richiede free manuale
    // obj viene liberato automaticamente quando lo scope termina, ma obj.data perde memoria!
}

// Soluzione: Libera i puntatori raw prima che lo scope termini
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... usa obj.data ...
    free(obj.data);  // Libera esplicitamente il puntatore raw
}  // obj stesso viene liberato automaticamente
```

### Trabocchetto: Confusione di tipo

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// ERRORE: Campo richiesto 'y' mancante
let p: Point = obj;
```

## Esempi

### Esempio: Matematica vettoriale

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

### Esempio: Database semplice

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

### Esempio: Emettitore di eventi

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
    print("Ricevuto: " + data);
});

emitter.emit("message", "Ciao!");
```

## Limitazioni

Limitazioni attuali:

- **Nessuna copia profonda** - Devi copiare manualmente gli oggetti annidati (spread e superficiale)
- **Nessun passaggio per valore** - Gli oggetti vengono sempre passati per riferimento
- **Nessuna proprieta calcolata** - Nessuna sintassi `{[key]: value}`
- **`self` e di sola lettura** - Non puoi riassegnare `self` nei metodi
- **Nessuna eliminazione di proprieta** - Non puoi rimuovere i campi una volta aggiunti

**Nota:** Gli oggetti sono conteggiati per riferimento e liberati automaticamente quando lo scope termina. Vedi [Gestione della memoria](memory.md#conteggio-interno-dei-riferimenti) per i dettagli.

## Argomenti correlati

- [Funzioni](functions.md) - I metodi sono funzioni memorizzate negli oggetti
- [Array](arrays.md) - Gli array sono anche simili agli oggetti
- [Tipi](types.md) - Duck typing e definizioni di tipo
- [Gestione degli errori](error-handling.md) - Lanciare oggetti errore

## Vedi anche

- **Duck Typing**: Vedi sezione "Objects" di CLAUDE.md per i dettagli sul duck typing
- **JSON**: Vedi CLAUDE.md per i dettagli sulla serializzazione JSON
- **Memoria**: Vedi [Memoria](memory.md) per l'allocazione degli oggetti
