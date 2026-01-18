# Panoramica della sintassi

Questo documento illustra le regole fondamentali della sintassi e la struttura dei programmi Hemlock.

## Regole di sintassi di base

### I punti e virgola sono obbligatori

A differenza di JavaScript o Python, i punti e virgola sono **sempre richiesti** alla fine delle istruzioni:

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**Questo causera un errore:**
```hemlock
let x = 42  // ERRORE: Punto e virgola mancante
let y = 10  // ERRORE: Punto e virgola mancante
```

### Le parentesi graffe sono sempre richieste

Tutti i blocchi di flusso di controllo devono utilizzare le parentesi graffe, anche per le istruzioni singole:

```hemlock
// CORRETTO
if (x > 0) {
    print("positivo");
}

// ERRORE: Parentesi graffe mancanti
if (x > 0)
    print("positivo");
```

### Commenti

```hemlock
// Questo e un commento su una singola riga

/*
   Questo e un
   commento multi-riga
*/

let x = 42;  // Commento in linea
```

## Variabili

### Dichiarazione

Le variabili vengono dichiarate con `let`:

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Annotazioni di tipo (opzionali)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "ciao";
```

### Costanti

Usare `const` per i valori immutabili:

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Tentare di riassegnare una costante causera un errore di esecuzione: "Cannot assign to const variable".

## Espressioni

### Operatori aritmetici

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - Addizione
print(a - b);   // 7  - Sottrazione
print(a * b);   // 30 - Moltiplicazione
print(a / b);   // 3  - Divisione (intera)
```

### Operatori di confronto

```hemlock
print(a == b);  // false - Uguale
print(a != b);  // true  - Diverso
print(a > b);   // true  - Maggiore di
print(a < b);   // false - Minore di
print(a >= b);  // true  - Maggiore o uguale
print(a <= b);  // false - Minore o uguale
```

### Operatori logici

```hemlock
let x = true;
let y = false;

print(x && y);  // false - AND
print(x || y);  // true  - OR
print(!x);      // false - NOT
```

### Operatori bitwise

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - AND bit a bit
print(a | b);   // 14 - OR bit a bit
print(a ^ b);   // 6  - XOR bit a bit
print(a << 2);  // 48 - Shift a sinistra
print(a >> 1);  // 6  - Shift a destra
print(~a);      // -13 - NOT bit a bit
```

### Precedenza degli operatori

Dalla piu alta alla piu bassa:

1. `()` - Raggruppamento
2. `!`, `~`, `-` (unario) - Operatori unari
3. `*`, `/` - Moltiplicazione, Divisione
4. `+`, `-` - Addizione, Sottrazione
5. `<<`, `>>` - Shift bit a bit
6. `<`, `<=`, `>`, `>=` - Confronti
7. `==`, `!=` - Uguaglianza
8. `&` - AND bit a bit
9. `^` - XOR bit a bit
10. `|` - OR bit a bit
11. `&&` - AND logico
12. `||` - OR logico

**Esempi:**
```hemlock
let x = 2 + 3 * 4;      // 14 (non 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Flusso di controllo

### Istruzioni If

```hemlock
if (condizione) {
    // corpo
}

if (condizione) {
    // ramo then
} else {
    // ramo else
}

if (condizione1) {
    // ramo 1
} else if (condizione2) {
    // ramo 2
} else {
    // ramo predefinito
}
```

### Cicli While

```hemlock
while (condizione) {
    // corpo
}
```

**Esempio:**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Cicli For

**Stile C:**
```hemlock
for (inizializzatore; condizione; incremento) {
    // corpo
}
```

**Esempio:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (array):**
```hemlock
for (let item in array) {
    // corpo
}
```

**Esempio:**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Istruzioni Switch

```hemlock
switch (espressione) {
    case valore1:
        // corpo
        break;
    case valore2:
        // corpo
        break;
    default:
        // corpo predefinito
        break;
}
```

**Esempio:**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Lunedi");
        break;
    case 2:
        print("Martedi");
        break;
    case 3:
        print("Mercoledi");
        break;
    default:
        print("Altro");
        break;
}
```

### Break e Continue

```hemlock
// Break: uscire dal ciclo
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue: passare all'iterazione successiva
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Funzioni

### Funzioni con nome

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // corpo
    return value;
}
```

**Esempio:**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Funzioni anonime

```hemlock
let func = fn(params) {
    // corpo
};
```

**Esempio:**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Annotazioni di tipo (opzionali)

```hemlock
// Senza annotazioni (tipi inferiti)
fn greet(name) {
    return "Ciao, " + name;
}

// Con annotazioni (verificate a runtime)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Oggetti

### Letterali oggetto

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Esempio:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Metodi

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Esempio:**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Definizioni di tipo

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Esempio:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Array

### Letterali array

```hemlock
let arr = [elemento1, elemento2, elemento3];
```

**Esempio:**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "due", true, null];
let empty = [];
```

### Indicizzazione array

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // Modificare un elemento
```

## Gestione degli errori

### Try/Catch

```hemlock
try {
    // codice rischioso
} catch (e) {
    // gestire l'errore
}
```

### Try/Finally

```hemlock
try {
    // codice rischioso
} finally {
    // viene sempre eseguito
}
```

### Try/Catch/Finally

```hemlock
try {
    // codice rischioso
} catch (e) {
    // gestire l'errore
} finally {
    // pulizia
}
```

### Throw

```hemlock
throw espressione;
```

**Esempio:**
```hemlock
if (x < 0) {
    throw "x deve essere positivo";
}
```

### Panic

```hemlock
panic(messaggio);
```

**Esempio:**
```hemlock
panic("errore irreversibile");
```

## Moduli (sperimentale)

### Istruzioni di export

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Istruzioni di import

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Async (sperimentale)

### Funzioni asincrone

```hemlock
async fn function_name(params): return_type {
    // corpo
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Canali (Channels)

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (Interfaccia di funzione esterna)

### Importare una libreria condivisa

```hemlock
import "library_name.so";
```

### Dichiarare una funzione esterna

```hemlock
extern fn function_name(param: type): return_type;
```

**Esempio:**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Letterali

### Letterali interi

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // Automaticamente i64

// Esadecimale (prefisso 0x)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Binario (prefisso 0b)
let bin = 0b1010;
let bin2 = 0b11110000;

// Ottale (prefisso 0o)
let oct = 0o777;
let oct2 = 0O123;

// Separatori numerici per la leggibilita
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Letterali in virgola mobile

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // Notazione scientifica
let sci2 = 2.5E+3;       // La E maiuscola funziona
let no_lead = .5;        // Senza zero iniziale (0.5)
let sep = 3.14_159_265;  // Separatori numerici
```

### Letterali stringa

```hemlock
let s = "ciao";
let escaped = "riga1\nriga2\ttabulazione";
let quote = "Ha detto \"ciao\"";

// Sequenze di escape esadecimali
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Sequenze di escape Unicode
let emoji = "\u{1F600}";               // faccina sorridente
let heart = "\u{2764}";                // cuore
let mixed = "Ciao \u{1F30D}!";         // Ciao mondo!
```

**Sequenze di escape:**
- `\n` - nuova riga
- `\t` - tabulazione
- `\r` - ritorno a capo
- `\\` - barra rovesciata
- `\"` - virgolette doppie
- `\'` - virgolette singole
- `\0` - carattere nullo
- `\xNN` - escape esadecimale (2 cifre)
- `\u{XXXX}` - escape unicode (1-6 cifre)

### Letterali rune

```hemlock
let ch = 'A';
let emoji = 'rocket';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Letterali booleani

```hemlock
let t = true;
let f = false;
```

### Letterale null

```hemlock
let nothing = null;
```

## Regole di scope

### Scope di blocco

Le variabili sono limitate al blocco contenitore piu vicino:

```hemlock
let x = 1;  // Scope esterno

if (true) {
    let x = 2;  // Scope interno (nasconde quello esterno)
    print(x);   // 2
}

print(x);  // 1
```

### Scope di funzione

Le funzioni creano il proprio scope:

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // Puo leggere lo scope esterno
}

foo();
// print(local);  // ERRORE: 'local' non definito qui
```

### Scope delle closure

Le closure catturano le variabili dallo scope contenitore:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Cattura 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Spazi bianchi e formattazione

### Indentazione

Hemlock non impone un'indentazione specifica, ma sono raccomandati 4 spazi:

```hemlock
fn example() {
    if (true) {
        print("indentato");
    }
}
```

### Interruzioni di riga

Le istruzioni possono estendersi su piu righe:

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Istruzione Loop

La parola chiave `loop` fornisce una sintassi piu chiara per i cicli infiniti:

```hemlock
loop {
    // ... eseguire il lavoro
    if (done) {
        break;
    }
}
```

Questo e equivalente a `while (true)` ma rende l'intenzione piu chiara.

## Parole chiave riservate

Le seguenti parole chiave sono riservate in Hemlock:

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Prossimi passi

- [Sistema dei tipi](types.md) - Scopri il sistema dei tipi di Hemlock
- [Flusso di controllo](control-flow.md) - Approfondisci le strutture di controllo
- [Funzioni](functions.md) - Padroneggia le funzioni e le closure
- [Gestione della memoria](memory.md) - Comprendi i puntatori e i buffer
