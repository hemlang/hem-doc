# Sistema dei tipi

Hemlock presenta un **sistema di tipi dinamico** con annotazioni di tipo opzionali e verifica dei tipi a runtime.

---

## Guida alla selezione dei tipi: Quale tipo devo usare?

**Nuovo ai tipi?** Inizia qui. Se hai familiarita con i sistemi di tipi, vai a [Filosofia](#filosofia).

### La risposta breve

**Lascia che Hemlock lo capisca da solo:**

```hemlock
let count = 42;        // Hemlock sa che questo e un intero
let price = 19.99;     // Hemlock sa che questo e un decimale
let name = "Alice";    // Hemlock sa che questo e testo
let active = true;     // Hemlock sa che questo e si/no
```

Hemlock sceglie automaticamente il tipo giusto per i tuoi valori. Non *devi* specificare i tipi.

### Quando aggiungere annotazioni di tipo

Aggiungi i tipi quando vuoi:

1. **Essere specifico sulla dimensione** - `i8` vs `i64` conta per la memoria o FFI
2. **Documentare il codice** - I tipi mostrano cosa si aspetta una funzione
3. **Catturare errori presto** - Hemlock verifica i tipi a runtime

```hemlock
// Senza tipi (funziona bene):
fn add(a, b) {
    return a + b;
}

// Con tipi (piu esplicito):
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Riferimento rapido: Scelta dei tipi numerici

| Cosa stai memorizzando | Tipo suggerito | Esempio |
|------------------------|----------------|---------|
| Numeri interi normali | `i32` (predefinito) | `let count = 42;` |
| Numeri molto grandi | `i64` | `let population = 8000000000;` |
| Conteggi mai negativi | `u32` | `let items: u32 = 100;` |
| Byte (0-255) | `u8` | `let pixel: u8 = 255;` |
| Decimali/frazioni | `f64` (predefinito) | `let price = 19.99;` |
| Decimali critici per le prestazioni | `f32` | `let x: f32 = 1.5;` |

### Riferimento rapido: Tutti i tipi

| Categoria | Tipi | Quando usare |
|-----------|------|--------------|
| **Numeri interi** | `i8`, `i16`, `i32`, `i64` | Conteggi, ID, eta, ecc. |
| **Numeri solo positivi** | `u8`, `u16`, `u32`, `u64` | Byte, dimensioni, lunghezze di array |
| **Decimali** | `f32`, `f64` | Denaro, misurazioni, matematica |
| **Si/No** | `bool` | Flag, condizioni |
| **Testo** | `string` | Nomi, messaggi, qualsiasi testo |
| **Singolo carattere** | `rune` | Singole lettere, emoji |
| **Liste** | `array` | Collezioni di valori |
| **Campi con nome** | `object` | Raggruppamento di dati correlati |
| **Memoria raw** | `ptr`, `buffer` | Programmazione a basso livello |
| **Nulla** | `null` | Assenza di un valore |

### Scenari comuni

**"Ho solo bisogno di un numero"**
```hemlock
let x = 42;  // Fatto! Hemlock sceglie i32
```

**"Ho bisogno di decimali"**
```hemlock
let price = 19.99;  // Fatto! Hemlock sceglie f64
```

**"Sto lavorando con byte (file, rete)"**
```hemlock
let byte: u8 = 255;  // Intervallo 0-255
```

**"Ho bisogno di numeri veramente grandi"**
```hemlock
let big = 9000000000000;  // Hemlock sceglie automaticamente i64 (> max i32)
// Oppure sii esplicito:
let big: i64 = 9000000000000;
```

**"Sto memorizzando denaro"**
```hemlock
// Opzione 1: Float (semplice, ma ha limiti di precisione)
let price: f64 = 19.99;

// Opzione 2: Memorizza come centesimi (piu preciso)
let price_cents: i32 = 1999;  // 19.99 euro come centesimi interi
```

**"Sto passando dati al codice C (FFI)"**
```hemlock
// Fai corrispondere esattamente i tipi C
let c_int: i32 = 100;      // C 'int'
let c_long: i64 = 100;     // C 'long' (su 64-bit)
let c_char: u8 = 65;       // C 'char'
let c_double: f64 = 3.14;  // C 'double'
```

### Cosa succede quando i tipi si mescolano?

Quando combini tipi diversi, Hemlock promuove al tipo "piu grande":

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // result e f64 (12.5)
// L'intero e diventato automaticamente un decimale
```

**Regola generale:** I float "vincono" sempre - mescolare qualsiasi intero con un float ti da un float.

### Errori di tipo

Se provi a usare il tipo sbagliato, Hemlock te lo dice a runtime:

```hemlock
let age: i32 = "trenta";  // ERRORE: tipo non corrispondente - atteso i32, ottenuto string
```

Per convertire i tipi, usa le funzioni costruttore di tipo:

```hemlock
let text = "42";
let number = i32(text);   // Analizza stringa in intero: 42
let back = text + "";     // Gia una stringa
```

---

## Filosofia

- **Dinamico per impostazione predefinita** - Ogni valore ha un tag di tipo a runtime
- **Tipizzato per scelta** - Le annotazioni di tipo opzionali impongono controlli a runtime
- **Conversioni esplicite** - Le conversioni implicite seguono regole di promozione chiare
- **Onesto sui tipi** - `typeof()` dice sempre la verita

## Tipi primitivi

### Tipi interi

**Interi con segno:**
```hemlock
let tiny: i8 = 127;              // 8-bit  (-128 a 127)
let small: i16 = 32767;          // 16-bit (-32768 a 32767)
let normal: i32 = 2147483647;    // 32-bit (predefinito)
let large: i64 = 9223372036854775807;  // 64-bit
```

**Interi senza segno:**
```hemlock
let byte: u8 = 255;              // 8-bit  (0 a 255)
let word: u16 = 65535;           // 16-bit (0 a 65535)
let dword: u32 = 4294967295;     // 32-bit (0 a 4294967295)
let qword: u64 = 18446744073709551615;  // 64-bit
```

**Alias di tipo:**
```hemlock
let i: integer = 42;   // Alias per i32
let b: byte = 255;     // Alias per u8
```

### Tipi in virgola mobile

```hemlock
let f: f32 = 3.14159;        // float 32-bit
let d: f64 = 2.718281828;    // float 64-bit (predefinito)
let n: number = 1.618;       // Alias per f64
```

### Tipo booleano

```hemlock
let flag: bool = true;
let active: bool = false;
```

### Tipo stringa

```hemlock
let text: string = "Ciao, Mondo!";
let empty: string = "";
```

Le stringhe sono **mutabili**, **codificate UTF-8** e **allocate nell'heap**.

Vedi [Stringhe](strings.md) per i dettagli completi.

### Tipo rune

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

Le rune rappresentano **codepoint Unicode** (da U+0000 a U+10FFFF).

Vedi [Rune](runes.md) per i dettagli completi.

### Tipo null

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null` e un tipo proprio con un singolo valore.

## Tipi composti

### Tipo array

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "due", true, null];  // Tipi misti consentiti
let empty: array = [];
```

Vedi [Array](arrays.md) per i dettagli completi.

### Tipo oggetto

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

Vedi [Oggetti](objects.md) per i dettagli completi.

### Tipi puntatore

**Puntatore raw:**
```hemlock
let p: ptr = alloc(64);
// Nessun controllo dei limiti, gestione manuale del ciclo di vita
free(p);
```

**Buffer sicuro:**
```hemlock
let buf: buffer = buffer(64);
// Controllo dei limiti, tiene traccia di lunghezza e capacita
free(buf);
```

Vedi [Gestione della memoria](memory.md) per i dettagli completi.

## Tipi enum

Gli enum definiscono un insieme di costanti con nome:

### Enum di base

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// Confronto
if (c == Color.RED) {
    print("E rosso!");
}

// Switch su enum
switch (c) {
    case Color.RED:
        print("Stop");
        break;
    case Color.GREEN:
        print("Vai");
        break;
    case Color.BLUE:
        print("Blu?");
        break;
}
```

### Enum con valori

Gli enum possono avere valori interi espliciti:

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### Valori auto-incrementanti

Senza valori espliciti, gli enum auto-incrementano da 0:

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// Puoi mescolare valori espliciti e automatici
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### Pattern di utilizzo degli enum

```hemlock
// Come parametri di funzione
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Urgente!");
    }
}

set_priority(Priority.HIGH);

// Negli oggetti
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Correggere bug",
    priority: Priority.HIGH
};
```

## Tipi speciali

### Tipo file

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

Rappresenta un handle di file aperto.

### Tipo task

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

Rappresenta un handle di task asincrono.

### Tipo channel

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

Rappresenta un canale di comunicazione tra task.

### Tipo void

```hemlock
extern fn exit(code: i32): void;
```

Usato per funzioni che non restituiscono un valore (solo FFI).

## Inferenza di tipo

### Inferenza dei letterali interi

Hemlock inferisce i tipi interi in base all'intervallo di valori:

```hemlock
let a = 42;              // i32 (entra in 32-bit)
let b = 5000000000;      // i64 (> max i32)
let c = 128;             // i32
let d: u8 = 128;         // u8 (annotazione esplicita)
```

**Regole:**
- Valori nell'intervallo i32 (da -2147483648 a 2147483647): inferiti come `i32`
- Valori fuori dall'intervallo i32 ma dentro i64: inferiti come `i64`
- Usa annotazioni esplicite per altri tipi (i8, i16, u8, u16, u32, u64)

### Inferenza dei letterali float

```hemlock
let x = 3.14;        // f64 (predefinito)
let y: f32 = 3.14;   // f32 (esplicito)
```

### Notazione scientifica

Hemlock supporta la notazione scientifica per i letterali numerici:

```hemlock
let a = 1e10;        // 10000000000.0 (f64)
let b = 1e-12;       // 0.000000000001 (f64)
let c = 3.14e2;      // 314.0 (f64)
let d = 2.5e-3;      // 0.0025 (f64)
let e = 1E10;        // Maiuscolo/minuscolo irrilevante
let f = 1e+5;        // Esponente positivo esplicito
```

**Nota:** Qualsiasi letterale che usa la notazione scientifica e sempre inferito come `f64`.

### Altra inferenza di tipo

```hemlock
let s = "ciao";      // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## Annotazioni di tipo

### Annotazioni di variabile

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### Annotazioni dei parametri di funzione

```hemlock
fn greet(name: string, age: i32) {
    print("Ciao, " + name + "!");
}
```

### Annotazioni del tipo di ritorno delle funzioni

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Annotazioni di tipo oggetto (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## Verifica dei tipi

### Verifica dei tipi a runtime

Le annotazioni di tipo vengono verificate a **runtime**, non a tempo di compilazione:

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // Errore runtime: tipo non corrispondente

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "ciao");      // Errore runtime: tipo non corrispondente
```

### Query di tipo

Usa `typeof()` per verificare i tipi dei valori:

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("ciao"));     // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## Conversioni di tipo

### Promozione di tipo implicita

Quando si mescolano tipi nelle operazioni, Hemlock promuove al tipo "superiore":

**Gerarchia di promozione (dal piu basso al piu alto):**
```
i8 → i16 → i32 → u32 → i64 → u64 → f32 → f64
      ↑     ↑     ↑
     u8    u16
```

**Il float vince sempre:**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result e f64 (13.5)
```

**La dimensione maggiore vince:**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sum e i64 (300)
```

**Preservazione della precisione:** Quando si mescolano interi a 64-bit con f32, Hemlock promuove
a f64 per evitare perdita di precisione (f32 ha solo mantissa a 24-bit, insufficiente per i64/u64):
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // result e f64, non f32!
```

**Esempi:**
```hemlock
u8 + i32  → i32
i32 + i64 → i64
u32 + u64 → u64
i32 + f32 → f32    // f32 sufficiente per i32
i64 + f32 → f64    // f64 necessario per preservare precisione i64
i64 + f64 → f64
i8 + f64  → f64
```

### Conversione di tipo esplicita

**Intero ↔ Float:**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 → f64 (42.0)

let x: f64 = 3.14;
let n: i32 = x;      // f64 → i32 (3, troncato)
```

**Intero ↔ Rune:**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 → rune ('A')

let r: rune = 'Z';
let value: i32 = r;   // rune → i32 (90)
```

**Rune → Stringa:**
```hemlock
let ch: rune = '🚀';
let s: string = ch;   // rune → string ("🚀")
```

**u8 → Rune:**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 → rune ('A')
```

### Funzioni costruttore di tipo

I nomi dei tipi possono essere usati come funzioni per convertire o analizzare valori:

**Analisi di stringhe in numeri:**
```hemlock
let n = i32("42");       // Analizza stringa in i32: 42
let f = f64("3.14159");  // Analizza stringa in f64: 3.14159
let b = bool("true");    // Analizza stringa in bool: true

// Tutti i tipi numerici supportati
let a = i8("-128");      // Analizza in i8
let c = u8("255");       // Analizza in u8
let d = i16("1000");     // Analizza in i16
let e = u16("50000");    // Analizza in u16
let g = i64("9000000000000"); // Analizza in i64
let h = u64("18000000000000"); // Analizza in u64
let j = f32("1.5");      // Analizza in f32
```

**Numeri esadecimali e negativi:**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10 (binario)
```

**Funzionano anche gli alias di tipo:**
```hemlock
let x = integer("100");  // Uguale a i32("100")
let y = number("1.5");   // Uguale a f64("1.5")
let z = byte("200");     // Uguale a u8("200")
```

**Conversione tra tipi numerici:**
```hemlock
let big = i64(42);           // i32 a i64
let truncated = i32(3.99);   // f64 a i32 (tronca a 3)
let promoted = f64(100);     // i32 a f64 (100.0)
let narrowed = i8(127);      // i32 a i8
```

**Le annotazioni di tipo eseguono coercizione numerica (ma NON analisi di stringhe):**
```hemlock
let f: f64 = 100;        // i32 a f64 via annotazione (OK)
let s: string = 'A';     // Rune a string via annotazione (OK)
let code: i32 = 'A';     // Rune a i32 via annotazione (ottiene codepoint, OK)

// L'analisi di stringhe richiede costruttori di tipo espliciti:
let n = i32("42");       // Usa costruttore di tipo per analisi stringa
// let x: i32 = "42";    // ERRORE - le annotazioni di tipo non analizzano stringhe
```

**Gestione degli errori:**
```hemlock
// Stringhe non valide generano errori quando si usano costruttori di tipo
let bad = i32("ciao");   // Errore runtime: impossibile analizzare "ciao" come i32
let overflow = u8("256"); // Errore runtime: 256 fuori intervallo per u8
```

**Analisi booleana:**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("si");    // Errore runtime: deve essere "true" o "false"
```

## Verifica degli intervalli

Le annotazioni di tipo impongono controlli di intervallo all'assegnazione:

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // ERRORE: fuori intervallo per u8

let a: i8 = 127;    // OK
let b: i8 = 128;    // ERRORE: fuori intervallo per i8

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // ERRORE: u64 non puo essere negativo
```

## Esempi di promozione di tipo

### Tipi interi misti

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32 (30)

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32 (300)
```

### Intero + Float

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32 (12.5)
```

### Espressioni complesse

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64 (70.0)
// Valutazione: b * c → f64(60.0)
//              a + f64(60.0) → f64(70.0)
```

## Duck Typing (Oggetti)

Gli oggetti usano il **typing strutturale** (duck typing):

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Ha tutti i campi richiesti
let p1: Person = { name: "Alice", age: 30 };

// OK: Campi extra consentiti
let p2: Person = { name: "Bob", age: 25, city: "Milano" };

// ERRORE: Campo 'age' mancante
let p3: Person = { name: "Carol" };

// ERRORE: Tipo sbagliato per 'age'
let p4: Person = { name: "Dave", age: "trenta" };
```

**La verifica del tipo avviene all'assegnazione:**
- Verifica che tutti i campi richiesti siano presenti
- Verifica che i tipi dei campi corrispondano
- I campi extra sono consentiti e preservati
- Imposta il nome del tipo dell'oggetto per `typeof()`

## Campi opzionali

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // Opzionale con default
    timeout?: i32,     // Opzionale, predefinito a null
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false (predefinito)
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true (sovrascritto)
```

## Alias di tipo

Hemlock supporta alias di tipo personalizzati usando la parola chiave `type`:

### Alias di tipo di base

```hemlock
// Alias di tipo semplice
type Integer = i32;
type Text = string;

// Uso dell'alias
let x: Integer = 42;
let msg: Text = "ciao";
```

### Alias di tipo funzione

```hemlock
// Alias di tipo funzione
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Uso degli alias di tipo funzione
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### Alias di tipo composto

```hemlock
// Combina piu define in un tipo
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### Alias di tipo generico

```hemlock
// Alias di tipo generico
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Uso degli alias generici
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Nota:** Gli alias di tipo sono trasparenti - `typeof()` restituisce il nome del tipo sottostante, non l'alias.

## Limitazioni del sistema dei tipi

Limitazioni attuali:

- **Nessun generico sulle funzioni** - Parametri di tipo delle funzioni non ancora supportati
- **Nessun tipo union** - Impossibile esprimere "A o B"
- **Nessun tipo nullable** - Tutti i tipi possono essere null (usa suffisso `?` per nullabilita esplicita)

**Nota:** Il compilatore (`hemlockc`) fornisce verifica dei tipi a tempo di compilazione. L'interprete esegue solo verifica dei tipi a runtime. Vedi la [documentazione del compilatore](../design/implementation.md) per i dettagli.

## Buone pratiche

### Quando usare le annotazioni di tipo

**USA le annotazioni quando:**
- Il tipo preciso conta (es. `u8` per valori byte)
- Documenti interfacce di funzione
- Imponi vincoli (es. controlli di intervallo)

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // Implementazione
}
```

**NON usare le annotazioni quando:**
- Il tipo e ovvio dal letterale
- Dettagli di implementazione interni
- Cerimonia non necessaria

```hemlock
// Non necessario
let x: i32 = 42;

// Meglio
let x = 42;
```

### Pattern di sicurezza dei tipi

**Verifica prima dell'uso:**
```hemlock
if (typeof(value) == "i32") {
    // Sicuro usare come i32
}
```

**Valida gli argomenti delle funzioni:**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "gli argomenti devono essere interi";
    }
    if (b == 0) {
        throw "divisione per zero";
    }
    return a / b;
}
```

**Usa il duck typing per flessibilita:**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## Prossimi passi

- [Stringhe](strings.md) - Tipo stringa UTF-8 e operazioni
- [Rune](runes.md) - Tipo codepoint Unicode
- [Array](arrays.md) - Tipo array dinamico
- [Oggetti](objects.md) - Letterali oggetto e duck typing
- [Memoria](memory.md) - Tipi puntatore e buffer
