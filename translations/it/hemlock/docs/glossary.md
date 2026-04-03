# Glossario

Nuovo alla programmazione o ai concetti di sistema? Questo glossario spiega i termini usati nella documentazione di Hemlock in linguaggio semplice.

---

## A

### Allocare / Allocazione
**Cosa significa:** Chiedere al computer un blocco di memoria da usare.

**Analogia:** Come prendere in prestito un libro da una biblioteca - stai prendendo spazio che dovrai restituire dopo.

**In Hemlock:**
```hemlock
let space = alloc(100);  // "Mi servono 100 byte di memoria, per favore"
// ... usalo ...
free(space);             // "Ho finito, puoi riprendertelo"
```

### Array
**Cosa significa:** Una lista di valori memorizzati insieme, accessibili per posizione (indice).

**Analogia:** Come una fila di cassette postali numerate 0, 1, 2, 3... Puoi mettere qualcosa nella cassetta #2 e poi recuperarlo dalla cassetta #2.

**In Hemlock:**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Asincrono
**Cosa significa:** Codice che puo eseguire "in background" mentre altro codice continua. In Hemlock, il codice async esegue effettivamente su core CPU separati simultaneamente.

**Analogia:** Come cucinare piu piatti contemporaneamente - metti il riso sul fuoco, poi mentre cuoce, tagli le verdure. Entrambe le cose accadono allo stesso tempo.

**In Hemlock:**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Booleano / Bool
**Cosa significa:** Un valore che e `true` o `false`. Nient'altro.

**Prende il nome da:** George Boole, un matematico che studio la logica vero/falso.

**In Hemlock:**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Controllo dei Limiti (Bounds Checking)
**Cosa significa:** Verificare automaticamente che non stai cercando di accedere alla memoria al di fuori di cio che e stato allocato. Previene crash e bug di sicurezza.

**Analogia:** Come un bibliotecario che controlla che il libro che stai richiedendo esista effettivamente prima di cercare di prenderlo.

**In Hemlock:**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer
**Cosa significa:** Un contenitore sicuro per byte grezzi con una dimensione nota. Hemlock controlla che tu non legga o scriva oltre i suoi limiti.

**Analogia:** Come una cassaforte con un numero specifico di scomparti. Puoi usare qualsiasi scomparto, ma non puoi accedere allo scomparto #50 se la cassaforte ne ha solo 10.

**In Hemlock:**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Closure
**Cosa significa:** Una funzione che "ricorda" le variabili da dove e stata creata, anche dopo che quel codice e terminato.

**Analogia:** Come un appunto che dice "aggiungi 5 a qualsiasi numero mi dai" - il "5" e incorporato nell'appunto.

**In Hemlock:**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Coercizione (Coercizione di Tipo)
**Cosa significa:** Convertire automaticamente un valore da un tipo a un altro quando necessario.

**Esempio:** Quando sommi un intero e un decimale, l'intero viene automaticamente convertito prima in decimale.

**In Hemlock:**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Compilare / Compilatore
**Cosa significa:** Tradurre il tuo codice in un programma che il computer puo eseguire direttamente. Il compilatore (`hemlockc`) legge il tuo file `.hml` e crea un eseguibile.

**Analogia:** Come tradurre un libro dall'inglese allo spagnolo - il contenuto e lo stesso, ma ora i lettori spagnoli possono leggerlo.

**In Hemlock:**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Concorrenza
**Cosa significa:** Piu cose che accadono in tempi sovrapposti. In Hemlock, questo significa effettiva esecuzione parallela su piu core CPU.

**Analogia:** Due chef che cucinano piatti diversi contemporaneamente nella stessa cucina.

---

## D

### Defer
**Cosa significa:** Pianificare qualcosa che accada dopo, quando la funzione corrente termina. Utile per la pulizia.

**Analogia:** Come dirsi "quando esco, spegni le luci" - imposti il promemoria ora, accade dopo.

**In Hemlock:**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck Typing
**Cosa significa:** Se sembra un'anatra e fa il verso dell'anatra, trattalo come un'anatra. Nel codice: se un oggetto ha i campi/metodi di cui hai bisogno, usalo - non preoccuparti del suo "tipo" ufficiale.

**Prende il nome da:** Il test dell'anatra - una forma di ragionamento.

**In Hemlock:**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Espressione
**Cosa significa:** Codice che produce un valore. Puo essere usato ovunque ci si aspetti un valore.

**Esempi:** `42`, `x + y`, `get_name()`, `true && false`

### Enum / Enumerazione
**Cosa significa:** Un tipo con un insieme fisso di valori possibili, ciascuno con un nome.

**Analogia:** Come un menu a tendina - puoi scegliere solo tra le opzioni elencate.

**In Hemlock:**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Virgola Mobile
**Cosa significa:** Un numero con il punto decimale. Chiamato "mobile" perche il punto decimale puo essere in posizioni diverse.

**In Hemlock:**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free (Liberare)
**Cosa significa:** Restituire la memoria che hai finito di usare al sistema cosi che possa essere riutilizzata.

**Analogia:** Restituire un libro alla biblioteca cosi che altri possano prenderlo in prestito.

**In Hemlock:**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Funzione
**Cosa significa:** Un blocco di codice riutilizzabile che prende input (parametri) e puo produrre un output (valore di ritorno).

**Analogia:** Come una ricetta - dagli gli ingredienti (input), segui i passaggi, ottieni un piatto (output).

**In Hemlock:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Garbage Collection (GC)
**Cosa significa:** Pulizia automatica della memoria. Il runtime trova periodicamente la memoria inutilizzata e la libera per te.

**Perche Hemlock non ce l'ha:** Il GC puo causare pause imprevedibili. Hemlock preferisce il controllo esplicito - sei tu a decidere quando liberare la memoria.

**Nota:** La maggior parte dei tipi Hemlock (stringhe, array, oggetti) VENGONO puliti automaticamente quando escono dallo scope. Solo i `ptr` grezzi da `alloc()` necessitano di `free()` manuale.

---

## H

### Heap
**Cosa significa:** Una regione di memoria per dati che devono sopravvivere alla funzione corrente. Allochi e liberi esplicitamente la memoria heap.

**In contrasto con:** Stack (archiviazione automatica e temporanea per variabili locali)

**In Hemlock:**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Indice
**Cosa significa:** La posizione di un elemento in un array o stringa. Inizia da 0 in Hemlock.

**In Hemlock:**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Intero
**Cosa significa:** Un numero intero senza punto decimale. Puo essere positivo, negativo o zero.

**In Hemlock:**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interprete
**Cosa significa:** Un programma che legge il tuo codice e lo esegue direttamente, riga per riga.

**In contrasto con:** Compilatore (traduce prima il codice, poi esegue la traduzione)

**In Hemlock:**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Letterale
**Cosa significa:** Un valore scritto direttamente nel tuo codice, non calcolato.

**Esempi:**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Memory Leak (Perdita di Memoria)
**Cosa significa:** Dimenticare di liberare memoria allocata. La memoria rimane riservata ma inutilizzata, sprecando risorse.

**Analogia:** Prendere in prestito libri dalla biblioteca e non restituirli mai. Alla fine, la biblioteca esaurisce i libri.

**In Hemlock:**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Metodo
**Cosa significa:** Una funzione collegata a un oggetto o tipo.

**In Hemlock:**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex
**Cosa significa:** Un blocco che garantisce che solo un thread acceda a qualcosa alla volta. Previene la corruzione dei dati quando piu thread toccano dati condivisi.

**Analogia:** Come la serratura di un bagno - solo una persona puo usarlo alla volta.

---

## N

### Null
**Cosa significa:** Un valore speciale che significa "niente" o "nessun valore."

**In Hemlock:**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Oggetto
**Cosa significa:** Una collezione di valori nominati (campi/proprieta) raggruppati insieme.

**In Hemlock:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parametro
**Cosa significa:** Una variabile che una funzione si aspetta di ricevere quando viene chiamata.

**Chiamato anche:** Argomento (tecnicamente, il parametro e nella definizione, l'argomento e nella chiamata)

**In Hemlock:**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Puntatore
**Cosa significa:** Un valore che contiene un indirizzo di memoria - "punta a" dove sono memorizzati i dati.

**Analogia:** Come un indirizzo stradale. L'indirizzo non e la casa - ti dice dove trovare la casa.

**In Hemlock:**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitivo
**Cosa significa:** Un tipo di base, integrato, che non e composto da altri tipi.

**In Hemlock:** `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `null`

---

## R

### Reference Counting (Conteggio dei Riferimenti)
**Cosa significa:** Tenere traccia di quante cose stanno usando un pezzo di dati. Quando nessuno lo usa piu, pulirlo automaticamente.

**In Hemlock:** Stringhe, array, oggetti e buffer usano internamente il conteggio dei riferimenti. Non lo vedi, ma previene le perdite di memoria per i tipi piu comuni.

### Valore di Ritorno
**Cosa significa:** Il valore che una funzione rimanda quando termina.

**In Hemlock:**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**Cosa significa:** Un singolo carattere Unicode (codepoint). Puo rappresentare qualsiasi carattere inclusi gli emoji.

**Perche "rune"?** Il termine viene da Go. Enfatizza che questo e un carattere completo, non solo un byte.

**In Hemlock:**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Runtime
**Cosa significa:** Il momento in cui il tuo programma sta effettivamente eseguendo (al contrario del "compile time" quando viene tradotto).

**Anche:** Il codice di supporto che esegue insieme al tuo programma (es. l'allocatore di memoria).

---

## S

### Scope
**Cosa significa:** La regione di codice dove una variabile esiste e puo essere usata.

**In Hemlock:**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Stack
**Cosa significa:** Memoria per dati temporanei a breve durata. Gestito automaticamente - quando una funzione ritorna, il suo spazio nello stack viene recuperato.

**In contrasto con:** Heap (piu longevo, gestito manualmente)

### Istruzione (Statement)
**Cosa significa:** Una singola istruzione o comando. Le istruzioni FANNO cose; le espressioni PRODUCONO valori.

**Esempi:** `let x = 5;`, `print("hi");`, `if (x > 0) { ... }`

### Stringa
**Cosa significa:** Una sequenza di caratteri di testo.

**In Hemlock:**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Tipizzazione Strutturale
**Cosa significa:** Compatibilita dei tipi basata sulla struttura (quali campi/metodi esistono), non sul nome. Uguale al "duck typing."

---

## T

### Thread
**Cosa significa:** Un percorso di esecuzione separato. Piu thread possono eseguire simultaneamente su diversi core CPU.

**In Hemlock:** `spawn()` crea un nuovo thread.

### Tipo
**Cosa significa:** Il genere di dati che un valore rappresenta. Determina quali operazioni sono valide.

**In Hemlock:**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Annotazione di Tipo
**Cosa significa:** Dichiarare esplicitamente quale tipo dovrebbe avere una variabile.

**In Hemlock:**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**Cosa significa:** Un modo per codificare il testo che supporta tutte le lingue del mondo e gli emoji. Ogni carattere puo occupare da 1 a 4 byte.

**In Hemlock:** Tutte le stringhe sono UTF-8.

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variabile
**Cosa significa:** Una posizione di memorizzazione nominata che contiene un valore.

**In Hemlock:**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## Riferimento Rapido: Quale Tipo Dovrei Usare?

| Situazione | Usa Questo | Perche |
|------------|-----------|-------|
| Ti serve solo un numero | `let x = 42;` | Hemlock sceglie il tipo giusto |
| Contare cose | `i32` | Abbastanza grande per la maggior parte dei conteggi |
| Numeri enormi | `i64` | Quando i32 non basta |
| Byte (0-255) | `u8` | File, dati di rete |
| Decimali | `f64` | Matematica decimale precisa |
| Valori Si/No | `bool` | Solo `true` o `false` |
| Testo | `string` | Qualsiasi contenuto testuale |
| Singolo carattere | `rune` | Una lettera/emoji |
| Lista di cose | `array` | Collezione ordinata |
| Campi nominati | `object` | Raggruppare dati correlati |
| Memoria grezza | `buffer` | Archiviazione byte sicura |
| Lavoro FFI/sistemi | `ptr` | Avanzato, memoria manuale |

---

## Vedi Anche

- [Avvio Rapido](getting-started/quick-start.md) - Il tuo primo programma Hemlock
- [Sistema di Tipi](language-guide/types.md) - Documentazione completa dei tipi
- [Gestione della Memoria](language-guide/memory.md) - Comprendere la memoria
