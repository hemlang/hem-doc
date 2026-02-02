# Proprietà della Memoria in Hemlock

> "Ti diamo gli strumenti per essere sicuro, ma non ti obblighiamo a usarli."

Questo documento descrive la semantica della proprietà della memoria in Hemlock, coprendo sia la memoria gestita dal programmatore che i valori gestiti dal runtime.

## Indice

1. [Il Contratto](#il-contratto)
2. [Memoria Gestita dal Programmatore](#memoria-gestita-dal-programmatore)
3. [Valori Gestiti dal Runtime](#valori-gestiti-dal-runtime)
4. [Punti di Trasferimento della Proprietà](#punti-di-trasferimento-della-proprietà)
5. [Async e Concorrenza](#async-e-concorrenza)
6. [Regole di Memoria FFI](#regole-di-memoria-ffi)
7. [Sicurezza delle Eccezioni](#sicurezza-delle-eccezioni)
8. [Best Practice](#best-practice)

---

## Il Contratto

Hemlock ha una chiara divisione delle responsabilità di gestione della memoria:

| Tipo di Memoria | Gestito Da | Metodo di Pulizia |
|-----------------|------------|-------------------|
| Puntatori grezzi (`ptr`) | **Programmatore** | `free(ptr)` |
| Buffer (`buffer`) | **Programmatore** | `free(buf)` |
| String, Array, Oggetti | **Runtime** | Automatico (conteggio riferimenti) |
| Funzioni, Closure | **Runtime** | Automatico (conteggio riferimenti) |
| Task, Channel | **Runtime** | Automatico (conteggio riferimenti) |

**Il principio fondamentale:** Se lo allochi esplicitamente, lo liberi esplicitamente. Tutto il resto viene gestito automaticamente.

---

## Memoria Gestita dal Programmatore

### Puntatori Grezzi

```hemlock
let p = alloc(64);       // Allocare 64 byte
memset(p, 0, 64);        // Inizializzare
// ... usare la memoria ...
free(p);                 // Responsabilità tua!
```

**Regole:**
- `alloc()` restituisce memoria che possiedi tu
- Devi chiamare `free()` quando hai finito
- Il double-free causerà un crash (intenzionalmente)
- L'use-after-free è comportamento indefinito
- L'aritmetica dei puntatori è permessa ma non verificata

### Allocazione Tipizzata

```hemlock
let arr = talloc("i32", 100);  // Allocare 100 i32 (400 byte)
ptr_write_i32(arr, 0, 42);     // Scrivere all'indice 0
let val = ptr_read_i32(arr, 0); // Leggere dall'indice 0
free(arr);                      // Sempre responsabilità tua
```

### Buffer (Alternativa Sicura)

```hemlock
let buf = buffer(64);    // Buffer con controllo dei limiti
buf[0] = 42;             // Indicizzazione sicura
// buf[100] = 1;         // Errore runtime: fuori dai limiti
free(buf);               // Richiede ancora free esplicito
```

**Differenza chiave:** I buffer forniscono controllo dei limiti, i puntatori grezzi no.

---

## Valori Gestiti dal Runtime

### Conteggio dei Riferimenti

I valori allocati sull'heap usano conteggio dei riferimenti atomico:

```hemlock
let s1 = "hello";        // String allocata, refcount = 1
let s2 = s1;             // s2 condivide s1, refcount = 2
// Quando entrambi escono dallo scope, refcount → 0, memoria liberata
```

**Tipi con conteggio dei riferimenti:**
- `string` - Testo UTF-8
- `array` - Array dinamici
- `object` - Oggetti chiave-valore
- `function` - Closure
- `task` - Handle di task async
- `channel` - Canali di comunicazione

### Rilevamento dei Cicli

Il runtime gestisce i cicli nei grafi di oggetti:

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // Ciclo: a → b → a
// Il runtime usa insiemi visitati per rilevare e spezzare i cicli durante la pulizia
```

---

## Punti di Trasferimento della Proprietà

### Binding di Variabili

```hemlock
let x = [1, 2, 3];       // Array creato con refcount 1
                         // x possiede il riferimento
```

### Ritorni di Funzioni

```hemlock
fn make_array() {
    return [1, 2, 3];    // La proprietà dell'array si trasferisce al chiamante
}
let arr = make_array();  // arr ora possiede il riferimento
```

### Assegnazione

```hemlock
let a = "hello";
let b = a;               // Riferimento condiviso (refcount incrementato)
b = "world";             // a ha ancora "hello", b ha "world"
```

### Operazioni sui Channel

```hemlock
let ch = channel(10);
ch.send("message");      // Valore copiato nel buffer del channel
                         // L'originale rimane valido

let msg = ch.recv();     // Riceve la proprietà dal channel
```

### Spawning di Task

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data viene COPIATO IN PROFONDITÀ per isolamento
data.x = 2;                       // Sicuro - il task ha la sua copia
let result = join(task);          // La proprietà del result si trasferisce al chiamante
```

---

## Async e Concorrenza

### Isolamento dei Thread

I task spawnati ricevono **copie profonde** degli argomenti mutabili:

```hemlock
async fn worker(data) {
    data.x = 100;        // Modifica solo la copia del task
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // Sicuro - non influenza il task
let result = join(task);
print(obj.x);            // 2 (invariato dal task)
print(result.x);         // 100 (copia modificata del task)
```

### Oggetti di Coordinazione Condivisi

Alcuni tipi sono condivisi per riferimento (non copiati):
- **Channel** - Per la comunicazione tra task
- **Task** - Per la coordinazione (join/detach)

```hemlock
let ch = channel(1);
spawn(producer, ch);     // Stesso channel, non una copia
spawn(consumer, ch);     // Entrambi i task condividono il channel
```

### Risultati dei Task

```hemlock
let task = spawn(compute);
let result = join(task);  // Il chiamante possiede il risultato
                          // Il riferimento del task viene rilasciato quando il task viene liberato
```

### Task Staccati

```hemlock
detach(spawn(background_work));
// Il task gira indipendentemente
// Il risultato viene rilasciato automaticamente quando il task completa
// Nessun leak anche se nessuno chiama join()
```

---

## Regole di Memoria FFI

### Passaggio a Funzioni C

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock mantiene la proprietà
                         // La string è valida durante la chiamata
                         // La funzione C NON deve liberarla
```

### Ricezione da Funzioni C

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C ha allocato questa memoria
free(copy);                   // Responsabilità tua liberarla
```

### Passaggio di Struct (Solo Compilatore)

```hemlock
// Definire il layout della struct C
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // Restituito per valore, copiato
                                // Nessuna pulizia necessaria per struct sullo stack
```

### Memoria dei Callback

```hemlock
// Quando C richiama Hemlock:
// - Gli argomenti appartengono a C (non liberare)
// - La proprietà del valore di ritorno si trasferisce a C
```

---

## Sicurezza delle Eccezioni

### Garanzie

Il runtime fornisce queste garanzie:

1. **Nessun leak in uscita normale** - Tutti i valori gestiti dal runtime vengono puliti
2. **Nessun leak in eccezione** - I temporanei vengono rilasciati durante lo stack unwinding
3. **Defer esegue in eccezione** - Il codice di pulizia viene eseguito

### Valutazione delle Espressioni

```hemlock
// Se questo lancia durante la creazione dell'array:
let arr = [f(), g(), h()];  // L'array parziale viene rilasciato

// Se questo lancia durante la chiamata di funzione:
foo(a(), b(), c());         // Gli arg precedentemente valutati vengono rilasciati
```

### Defer per la Pulizia

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // Esegue al return O all'eccezione

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close() esegue comunque!
    }
    return data;
}
```

---

## Best Practice

### 1. Preferisci i Tipi Gestiti dal Runtime

```hemlock
// Preferisci questo:
let data = [1, 2, 3, 4, 5];

// A questo (a meno che tu non abbia bisogno di controllo a basso livello):
let data = talloc("i32", 5);
// ... devi ricordarti di liberare ...
```

### 2. Usa Defer per la Memoria Manuale

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // Pulizia garantita

    // ... usare buf ...
    // Non serve liberare ad ogni punto di ritorno
}
```

### 3. Evita i Puntatori Grezzi in Async

```hemlock
// SBAGLIATO - il puntatore potrebbe essere liberato prima che il task completi
let p = alloc(64);
spawn(worker, p);          // Il task ottiene il valore del puntatore
free(p);                   // Ops! Il task lo sta ancora usando

// CORRETTO - usa channel o copia i dati
let ch = channel(1);
let data = buffer(64);
// ... riempire data ...
ch.send(data);             // Copia profonda
spawn(worker, ch);
free(data);                // Sicuro - il task ha la sua copia
```

### 4. Chiudi i Channel Quando Hai Finito

```hemlock
let ch = channel(10);
// ... usare il channel ...
ch.close();                // Svuota e rilascia i valori nel buffer
```

### 5. Join o Detach i Task

```hemlock
let task = spawn(work);

// Opzione 1: Aspettare il risultato
let result = join(task);

// Opzione 2: Fire and forget
// detach(task);

// NON: Lasciare che l'handle del task esca dallo scope senza join o detach
// (Verrà pulito, ma il risultato potrebbe avere leak)
```

---

## Debug dei Problemi di Memoria

### Abilitare ASAN

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### Eseguire i Test di Regressione dei Leak

```bash
make leak-regression       # Suite completa
make leak-regression-quick # Salta il test esaustivo
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## Riepilogo

| Operazione | Comportamento Memoria |
|------------|----------------------|
| `alloc(n)` | Alloca, tu liberi |
| `buffer(n)` | Alloca con controllo limiti, tu liberi |
| `"string"` | Il runtime gestisce |
| `[array]` | Il runtime gestisce |
| `{object}` | Il runtime gestisce |
| `spawn(fn)` | Copia profonda degli arg, il runtime gestisce il task |
| `join(task)` | Il chiamante possiede il risultato |
| `detach(task)` | Il runtime rilascia il risultato quando finito |
| `ch.send(v)` | Copia il valore nel channel |
| `ch.recv()` | Il chiamante possiede il valore ricevuto |
| `ch.close()` | Svuota e rilascia i valori nel buffer |
