# Avvio Rapido

Inizia a usare Hemlock in pochi minuti!

## Il Tuo Primo Programma

Crea un file chiamato `hello.hml`:

```hemlock
print("Ciao, Hemlock!");
```

Esegui con l'interprete:

```bash
./hemlock hello.hml
```

Oppure compila in un eseguibile nativo:

```bash
./hemlockc hello.hml -o hello
./hello
```

Output:
```
Ciao, Hemlock!
```

### Interprete vs Compilatore

Hemlock fornisce due modi per eseguire i programmi:

| Strumento | Caso d'Uso | Type Checking |
|-----------|------------|---------------|
| `hemlock` | Script veloci, REPL, sviluppo | Solo runtime |
| `hemlockc` | Binari di produzione, prestazioni migliori | Compile-time (default) |

Il compilatore (`hemlockc`) verifica i tipi del tuo codice prima di generare un eseguibile, catturando gli errori in anticipo.

## Sintassi di Base

### Variabili

```hemlock
// Le variabili sono dichiarate con 'let'
let x = 42;
let name = "Alice";
let pi = 3.14159;

// Le annotazioni di tipo sono opzionali
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**Importante**: I punto e virgola sono **obbligatori** in Hemlock!

### Tipi

Hemlock ha un sistema di tipi ricco:

```hemlock
// Interi
let small: i8 = 127;          // 8-bit con segno
let byte: u8 = 255;           // 8-bit senza segno
let num: i32 = 2147483647;    // 32-bit con segno (default)
let big: i64 = 9223372036854775807;  // 64-bit con segno

// Float
let f: f32 = 3.14;            // float 32-bit
let d: f64 = 2.71828;         // float 64-bit (default)

// Stringhe e caratteri
let text: string = "Ciao";    // stringa UTF-8
let emoji: rune = '🚀';       // codepoint Unicode

// Booleano e null
let flag: bool = true;
let empty = null;
```

### Flusso di Controllo

```hemlock
// Istruzioni if
if (x > 0) {
    print("positivo");
} else if (x < 0) {
    print("negativo");
} else {
    print("zero");
}

// Cicli while
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// Cicli for
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### Funzioni

```hemlock
// Funzione nominata
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// Funzione anonima
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## Lavorare con le Stringhe

Le stringhe in Hemlock sono **mutabili** e **UTF-8**:

```hemlock
let s = "ciao";
s[0] = 'C';              // Ora "Ciao"
print(s);

// Metodi stringa
let upper = s.to_upper();     // "CIAO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "iao"

// Concatenazione
let greeting = "Ciao" + ", " + "Mondo!";
print(greeting);  // "Ciao, Mondo!"
```

## Array

Array dinamici con tipi misti:

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Metodi array
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// Tipi misti permessi
let mixed = [1, "due", true, null];
```

## Oggetti

Oggetti in stile JavaScript:

```hemlock
// Letterale oggetto
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // Modifica campo

// Metodi con 'self'
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Gestione della Memoria

Hemlock usa **gestione manuale della memoria**:

```hemlock
// Buffer sicuro (raccomandato)
let buf = buffer(64);   // Alloca 64 byte
buf[0] = 65;            // Imposta primo byte a 'A'
print(buf[0]);          // 65
free(buf);              // Libera memoria

// Puntatore raw (avanzato)
let ptr = alloc(100);
memset(ptr, 0, 100);    // Riempi con zeri
free(ptr);
```

**Importante**: Devi fare `free()` di ciò che `alloc()`!

## Gestione degli Errori

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
} finally {
    print("Fatto");
}
```

## Argomenti da Riga di Comando

Accedi agli argomenti del programma tramite l'array `args`:

```hemlock
// script.hml
print("Script:", args[0]);
print(`Argomenti: ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  arg ${i}: ${args[i]}`);
    i = i + 1;
}
```

Esegui con:
```bash
./hemlock script.hml ciao mondo
```

Output:
```
Script: script.hml
Argomenti: 2
  arg 1: ciao
  arg 2: mondo
```

## I/O su File

```hemlock
// Scrivi su file
let f = open("data.txt", "w");
f.write("Ciao, File!");
f.close();

// Leggi da file
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Ciao, File!"
f2.close();
```

## Cosa c'è Dopo?

Ora che hai visto le basi, esplora di più:

- [Tutorial](tutorial.md) - Guida completa passo dopo passo
- [Guida al Linguaggio](../language-guide/syntax.md) - Approfondimento su tutte le funzionalità
- [Esempi](../../examples/) - Programmi esempio reali
- [Riferimento API](../reference/builtins.md) - Documentazione API completa

## Errori Comuni

### Dimenticare i Punto e Virgola

```hemlock
// ❌ ERRORE: Punto e virgola mancante
let x = 42
let y = 10

// ✅ CORRETTO
let x = 42;
let y = 10;
```

### Dimenticare di Liberare la Memoria

```hemlock
// ❌ MEMORY LEAK
let buf = buffer(100);
// ... usa buf ...
// Dimenticato di chiamare free(buf)!

// ✅ CORRETTO
let buf = buffer(100);
// ... usa buf ...
free(buf);
```

### Le Parentesi Graffe Sono Richieste

```hemlock
// ❌ ERRORE: Parentesi graffe mancanti
if (x > 0)
    print("positivo");

// ✅ CORRETTO
if (x > 0) {
    print("positivo");
}
```

## Ottenere Aiuto

- Leggi la [documentazione completa](../README.md)
- Controlla la [directory degli esempi](../../examples/)
- Guarda i [file di test](../../tests/) per pattern d'uso
- Segnala problemi su GitHub
