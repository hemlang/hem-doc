# Tutorial Hemlock

Una guida completa passo dopo passo per imparare Hemlock.

## Indice

1. [Hello World](#hello-world)
2. [Variabili e Tipi](#variabili-e-tipi)
3. [Aritmetica e Operazioni](#aritmetica-e-operazioni)
4. [Flusso di Controllo](#flusso-di-controllo)
5. [Funzioni](#funzioni)
6. [Stringhe e Rune](#stringhe-e-rune)
7. [Array](#array)
8. [Oggetti](#oggetti)
9. [Gestione della Memoria](#gestione-della-memoria)
10. [Gestione degli Errori](#gestione-degli-errori)
11. [I/O su File](#io-su-file)
12. [Mettere Tutto Insieme](#mettere-tutto-insieme)

## Hello World

Iniziamo con il tradizionale primo programma:

```hemlock
print("Ciao, Mondo!");
```

Salva questo come `hello.hml` ed esegui:

```bash
./hemlock hello.hml
```

**Punti Chiave:**
- `print()` è una funzione integrata che scrive su stdout
- Le stringhe sono racchiuse tra doppi apici
- I punto e virgola sono **obbligatori**

## Variabili e Tipi

### Dichiarare Variabili

```hemlock
// Dichiarazione base di variabile
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### Annotazioni di Tipo

Mentre i tipi sono inferiti di default, puoi essere esplicito:

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### Inferenza di Tipo

Hemlock inferisce i tipi in base ai valori:

```hemlock
let small = 42;              // i32 (entra in 32-bit)
let large = 5000000000;      // i64 (troppo grande per i32)
let decimal = 3.14;          // f64 (default per float)
let text = "ciao";           // string
let flag = true;             // bool
```

### Controllo dei Tipi

```hemlock
// Controlla i tipi con typeof()
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("ciao"));    // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## Aritmetica e Operazioni

### Aritmetica di Base

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3 (divisione intera)
print(a == b);  // false
print(a > b);   // true
```

### Promozione dei Tipi

Quando si mescolano tipi, Hemlock promuove al tipo più grande/preciso:

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result è f64 (10.0 + 3.5 = 13.5)

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### Operazioni Bit a Bit

```hemlock
let a = 12;  // 1100 in binario
let b = 10;  // 1010 in binario

print(a & b);   // 8  (AND)
print(a | b);   // 14 (OR)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24 (shift sinistro)
print(a >> 1);  // 6  (shift destro)
print(~a);      // -13 (NOT)
```

## Flusso di Controllo

### Istruzioni If

```hemlock
let x = 10;

if (x > 0) {
    print("positivo");
} else if (x < 0) {
    print("negativo");
} else {
    print("zero");
}
```

**Nota:** Le parentesi graffe sono **sempre richieste**, anche per singole istruzioni.

### Cicli While

```hemlock
let count = 0;
while (count < 5) {
    print(`Conteggio: ${count}`);
    count = count + 1;
}
```

### Cicli For

```hemlock
// Ciclo for stile C
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// Ciclo for-in (array)
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Elemento: ${item}`);
}
```

### Istruzioni Switch

```hemlock
let day = 3;

switch (day) {
    case 1:
        print("Lunedì");
        break;
    case 2:
        print("Martedì");
        break;
    case 3:
        print("Mercoledì");
        break;
    default:
        print("Altro giorno");
        break;
}
```

### Break e Continue

```hemlock
// Break: esce dal ciclo in anticipo
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Stampa: 0, 1, 2, 3, 4

// Continue: salta alla prossima iterazione
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// Stampa: 0, 1, 3, 4
```

## Funzioni

### Funzioni Nominate

```hemlock
fn greet(name: string): string {
    return "Ciao, " + name + "!";
}

let message = greet("Alice");
print(message);  // "Ciao, Alice!"
```

### Funzioni Anonime

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### Ricorsione

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Closure

Le funzioni catturano il loro ambiente:

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

### Funzioni di Ordine Superiore

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## Stringhe e Rune

### Basi delle Stringhe

Le stringhe sono **mutabili** e **UTF-8**:

```hemlock
let s = "ciao";
print(s.length);      // 4 (conteggio caratteri)
print(s.byte_length); // 4 (conteggio byte)

// Mutazione
s[0] = 'C';
print(s);  // "Ciao"
```

### Metodi Stringa

```hemlock
let text = "  Ciao, Mondo!  ";

// Conversione maiuscole/minuscole
print(text.to_upper());  // "  CIAO, MONDO!  "
print(text.to_lower());  // "  ciao, mondo!  "

// Trim
print(text.trim());      // "Ciao, Mondo!"

// Estrazione sottostringa
let ciao = text.substr(2, 4);  // "Ciao"
let mondo = text.slice(8, 13); // "Mondo"

// Ricerca
let pos = text.find("Mondo");  // 8
let has = text.contains("o");  // true

// Split
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// Sostituzione
let s = "ciao mondo".replace("mondo", "a tutti");
print(s);  // "ciao a tutti"
```

### Rune (Codepoint Unicode)

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Concatenazione Rune + String
let msg = '>' + " Importante";
print(msg);  // "> Importante"

// Conversione tra rune e intero
let code: i32 = ch;     // 65 (codice ASCII)
let r: rune = 128640;   // U+1F680 (🚀)
```

## Array

### Basi degli Array

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Modifica elementi
numbers[2] = 99;
print(numbers[2]);  // 99
```

### Metodi Array

```hemlock
let arr = [10, 20, 30];

// Aggiungi/rimuovi alla fine
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40, arr è ora [10, 20, 30]

// Aggiungi/rimuovi all'inizio
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5, arr è ora [10, 20, 30]

// Inserisci/rimuovi all'indice
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// Ricerca
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// Slice
let slice = arr.slice(0, 2);  // [10, 15]

// Join in stringa
let text = arr.join(", ");    // "10, 15, 30"
```

### Iterazione

```hemlock
let items = ["mela", "banana", "ciliegia"];

// Ciclo for-in
for (let item in items) {
    print(item);
}

// Iterazione manuale
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## Oggetti

### Letterali Oggetto

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// Aggiungi/modifica campi
person.email = "alice@example.com";
person.age = 31;
```

### Metodi e `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### Definizioni di Tipo (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // Opzionale con default
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // Duck typing valida la struttura

print(typeof(typed));   // "Person"
print(typed.active);    // true (default applicato)
```

### Serializzazione JSON

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// Object a JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON a Object
let restored = json.deserialize();
print(restored.name);  // "test"
```

## Gestione della Memoria

### Buffer Sicuri (Raccomandato)

```hemlock
// Alloca buffer
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// Imposta valori (controllo limiti)
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Accedi valori
print(buf[0]);  // 65

// Deve essere liberato quando finito
free(buf);
```

### Puntatori Raw (Avanzato)

```hemlock
// Alloca memoria raw
let ptr = alloc(100);

// Riempi con zeri
memset(ptr, 0, 100);

// Copia dati
let src = alloc(50);
memcpy(ptr, src, 50);

// Libera entrambi
free(src);
free(ptr);
```

### Funzioni di Memoria

```hemlock
// Rialloca
let p = alloc(64);
p = realloc(p, 128);  // Ridimensiona a 128 byte
free(p);

// Allocazione tipizzata (futuro)
// let arr = talloc(i32, 100);  // Array di 100 i32
```

## Gestione degli Errori

### Try/Catch

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "divisione per zero";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Errore: " + e);
}
// Output: Errore: divisione per zero
```

### Blocco Finally

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Errore: " + e);
} finally {
    // Sempre eseguito
    if (file != null) {
        file.close();
    }
}
```

### Lanciare Oggetti

```hemlock
try {
    throw { code: 404, message: "Non trovato" };
} catch (e) {
    print(`Errore ${e.code}: ${e.message}`);
}
// Output: Errore 404: Non trovato
```

### Panic (Errori Irrecuperabili)

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x deve essere non-negativo");
    }
    return x * 2;
}

validate(-5);  // Programma esce con: panic: x deve essere non-negativo
```

## I/O su File

### Lettura File

```hemlock
// Leggi intero file
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// Leggi numero specifico di byte
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // Leggi 100 byte
f2.close();
```

### Scrittura File

```hemlock
// Scrivi testo
let f = open("output.txt", "w");
f.write("Ciao, File!\n");
f.write("Seconda riga\n");
f.close();

// Aggiungi a file
let f2 = open("output.txt", "a");
f2.write("Riga aggiunta\n");
f2.close();
```

### I/O Binario

```hemlock
// Scrivi dati binari
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// Leggi dati binari
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### Proprietà File

```hemlock
let f = open("/path/to/file.txt", "r");

print(f.path);    // "/path/to/file.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## Mettere Tutto Insieme

Costruiamo un semplice programma conta-parole:

```hemlock
// wordcount.hml - Conta le parole in un file

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // Dividi per spazi e conta
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Errore lettura file: " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// Programma principale
if (args.length < 2) {
    print("Uso: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Conteggio parole: ${words}`);
    }
}
```

Esegui con:
```bash
./hemlock wordcount.hml data.txt
```

## Prossimi Passi

Congratulazioni! Hai imparato le basi di Hemlock. Ecco cosa esplorare dopo:

- [Async e Concorrenza](../advanced/async-concurrency.md) - Vero multi-threading
- [FFI](../advanced/ffi.md) - Chiama funzioni C
- [Gestione Segnali](../advanced/signals.md) - Segnali di processo
- [Riferimento API](../reference/builtins.md) - Documentazione API completa
- [Esempi](../../examples/) - Altri programmi reali

## Esercizi Pratici

Prova a costruire questi programmi per esercitarti:

1. **Calcolatrice**: Implementa una semplice calcolatrice con +, -, *, /
2. **Copia File**: Copia un file in un altro
3. **Fibonacci**: Genera numeri di Fibonacci
4. **Parser JSON**: Leggi e parsa file JSON
5. **Processore Testo**: Trova e sostituisci testo nei file

Buona programmazione con Hemlock!
