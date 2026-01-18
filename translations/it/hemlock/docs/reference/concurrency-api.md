# Riferimento API di Concorrenza

Riferimento completo per le funzionalità di concorrenza e parallelismo di Hemlock.

---

## Panoramica

Hemlock fornisce **concorrenza strutturata** basata su POSIX threads (pthreads) con task, canali e funzioni asincrone. Ogni task esegue su un thread del sistema operativo per un vero parallelismo su più core CPU.

**Caratteristiche Principali:**
- Vero parallelismo multi-thread (non event loop o green threads)
- Scheduling preemptive da parte del kernel
- Canali per comunicazione sicura tra thread
- async/await per funzioni asincrone
- Propagazione delle eccezioni dai task

---

## Modello di Threading

### Architettura

Hemlock usa threading **1:1** (un task = un pthread):

```
Task Utente          Thread OS          Core CPU
---------            ---------          --------
spawn(f1) ------->   pthread_create --> Core 0
spawn(f2) ------->   pthread_create --> Core 1
spawn(f3) ------->   pthread_create --> Core 2
```

**Caratteristiche:**
- Ogni `spawn()` crea un nuovo pthread
- Il kernel pianifica i thread sui core
- Vera esecuzione parallela (nessun GIL)
- Multitasking preemptive

---

## Tipo Task

**Tipo:** `task`

**Descrizione:** Handle per un task concorrente in esecuzione

**Proprietà:**
- Handle opaco al thread sottostante
- Contiene il risultato quando completato
- Memorizza l'eccezione se lanciata

---

## Tipo Channel

**Tipo:** `channel`

**Descrizione:** Canale di comunicazione thread-safe con buffer

**Proprietà:**
- `.length` - Numero di elementi attualmente nel buffer (i32)
- `.capacity` - Dimensione massima del buffer (i32)
- `.closed` - Se il canale è chiuso (bool)

---

## Funzioni di Gestione dei Task

### spawn

Crea un nuovo task per eseguire una funzione.

**Firma:**
```hemlock
spawn(func: function, ...args): task
```

**Parametri:**
- `func` - Funzione da eseguire
- `args` - Argomenti da passare alla funzione

**Restituisce:** Handle del task

**Esempi:**
```hemlock
// Funzione semplice
fn calcola(n: i32): i32 {
    return n * n;
}

let t = spawn(calcola, 42);
let risultato = join(t);       // 1764

// Funzione con più argomenti
fn somma(a: i32, b: i32): i32 {
    return a + b;
}

let t2 = spawn(somma, 10, 20);
let risultato2 = join(t2);     // 30

// Spawn multipli per parallelismo
let t1 = spawn(calcola, 10);
let t2 = spawn(calcola, 20);
let t3 = spawn(calcola, 30);

let r1 = join(t1);  // 100
let r2 = join(t2);  // 400
let r3 = join(t3);  // 900
```

**Comportamento:**
- Crea nuovo pthread
- Inizia l'esecuzione immediatamente
- Il task esegue concorrentemente con il chiamante
- Gestisci il task con `join()` o `detach()`

**Importante:** I task devono essere joinati o detachati per evitare leak di risorse.

---

### join

Attende il completamento del task e ottiene il risultato.

**Firma:**
```hemlock
join(t: task): any
```

**Parametri:**
- `t` - Handle del task da attendere

**Restituisce:** Valore di ritorno della funzione del task

**Esempi:**
```hemlock
fn lavoro(): i32 {
    // Calcolo lungo...
    return 42;
}

let t = spawn(lavoro);
// ... fai altro lavoro ...
let risultato = join(t);       // Attende, restituisce 42
```

**Comportamento:**
- Si blocca finché il task non completa
- Restituisce il valore di ritorno della funzione del task
- Se il task ha lanciato un'eccezione, la rilancia nel chiamante
- Può essere chiamato una sola volta per task

**Gestione Eccezioni:**
```hemlock
fn rischioso(): i32 {
    throw "fallimento";
}

let t = spawn(rischioso);
try {
    let risultato = join(t);
} catch (e) {
    print("Task fallito:", e);  // "Task fallito: fallimento"
}
```

---

### detach

Detach un task per permettergli di eseguire indipendentemente.

**Firma:**
```hemlock
detach(t: task): null
```

**Parametri:**
- `t` - Handle del task da detachare

**Restituisce:** `null`

**Esempi:**
```hemlock
fn lavoro_sfondo() {
    // Lavoro di lunga durata...
    print("Sfondo completato");
}

let t = spawn(lavoro_sfondo);
detach(t);  // Esegue indipendentemente

// Il chiamante continua senza attendere
print("Continua...");
```

**Comportamento:**
- Il task esegue indipendentemente
- Le risorse vengono pulite automaticamente quando completa
- Non può joinare dopo il detach
- Il task potrebbe ancora essere in esecuzione quando il programma esce

**Casi d'Uso:**
- Operazioni fire-and-forget
- Lavoro in background
- Servizi di lunga durata

---

## Operazioni sui Canali

### channel

Crea un nuovo canale con buffer.

**Firma:**
```hemlock
channel(capacita?: i32): channel
```

**Parametri:**
- `capacita` (opzionale) - Dimensione del buffer (predefinito: 0 per canale non bufferizzato)

**Restituisce:** Nuovo canale

**Esempi:**
```hemlock
// Canale non bufferizzato (capacità 0)
let ch_sync = channel();
let ch_sync2 = channel(0);

// Canale bufferizzato
let ch_buf = channel(10);      // Può contenere 10 elementi

print(ch_buf.capacity);        // 10
print(ch_buf.length);          // 0 (vuoto)
```

**Comportamento:**
- Buffer circolare per elementi
- Thread-safe (protetto da mutex)
- Supporta più mittenti e ricevitori

---

### send

Invia un valore su un canale.

**Firma:**
```hemlock
channel.send(valore: any): null
```

**Parametri:**
- `valore` - Valore da inviare

**Restituisce:** `null`

**Esempi:**
```hemlock
let ch = channel(10);

// Invia valori
ch.send(42);
ch.send("ciao");
ch.send([1, 2, 3]);

print(ch.length);              // 3
```

**Comportamento:**
- Aggiunge il valore al buffer del canale
- Si blocca se il buffer è pieno (attende spazio)
- Thread-safe

**Pattern Produttore:**
```hemlock
fn produttore(ch: channel) {
    let i = 0;
    while (i < 10) {
        ch.send(i);
        i = i + 1;
    }
    ch.close();
}

let ch = channel(5);
let t = spawn(produttore, ch);

// Consuma...
```

---

### recv

Riceve un valore da un canale.

**Firma:**
```hemlock
channel.recv(): any
```

**Restituisce:** Valore ricevuto dal canale

**Esempi:**
```hemlock
let ch = channel(10);

ch.send(42);
ch.send("ciao");

let val1 = ch.recv();          // 42
let val2 = ch.recv();          // "ciao"
```

**Comportamento:**
- Rimuove e restituisce il valore più vecchio dal buffer
- Si blocca se il buffer è vuoto (attende dati)
- Thread-safe
- Restituisce `null` se il canale è chiuso e vuoto

**Pattern Consumatore:**
```hemlock
fn consumatore(ch: channel) {
    while (true) {
        let val = ch.recv();
        if (val == null && ch.closed) {
            break;
        }
        print("Ricevuto:", val);
    }
}
```

---

### close

Chiude un canale.

**Firma:**
```hemlock
channel.close(): null
```

**Restituisce:** `null`

**Esempi:**
```hemlock
let ch = channel(10);
ch.send(1);
ch.send(2);
ch.close();

print(ch.closed);              // true

// Può ancora ricevere valori esistenti
let val = ch.recv();           // 1
let val2 = ch.recv();          // 2
let val3 = ch.recv();          // null (canale chiuso e vuoto)

// L'invio al canale chiuso genera errore
// ch.send(3);                 // ERRORE
```

**Comportamento:**
- Segna il canale come chiuso
- Gli invii al canale chiuso generano errore
- Le ricezioni possono ancora ottenere i valori esistenti
- Le ricezioni restituiscono `null` quando chiuso e vuoto

---

## Proprietà dei Canali

### .length

Numero di elementi attualmente nel buffer.

**Tipo:** `i32`

**Esempi:**
```hemlock
let ch = channel(10);
print(ch.length);              // 0

ch.send(1);
ch.send(2);
print(ch.length);              // 2

ch.recv();
print(ch.length);              // 1
```

---

### .capacity

Dimensione massima del buffer.

**Tipo:** `i32`

**Esempi:**
```hemlock
let ch = channel(10);
print(ch.capacity);            // 10

let ch2 = channel();
print(ch2.capacity);           // 0
```

---

### .closed

Se il canale è chiuso.

**Tipo:** `bool`

**Esempi:**
```hemlock
let ch = channel(10);
print(ch.closed);              // false

ch.close();
print(ch.closed);              // true
```

---

## Funzioni Async

### async fn

Dichiara una funzione asincrona.

**Sintassi:**
```hemlock
async fn nome(params): tipo_ritorno {
    // corpo
}
```

**Esempi:**
```hemlock
async fn carica_dati(url: string): string {
    // Operazione I/O simulata
    let dati = http_get(url);
    return dati;
}

async fn calcola(n: i32): i32 {
    // Calcolo CPU-bound
    let risultato = 0;
    let i = 0;
    while (i < n) {
        risultato = risultato + i;
        i = i + 1;
    }
    return risultato;
}
```

**Comportamento:**
- Le funzioni async possono essere spawned come task
- Restituiscono i loro valori normalmente
- Le eccezioni si propagano al joiner

---

### await

Attende il risultato di un task.

**Firma:**
```hemlock
await task: any
```

**Esempi:**
```hemlock
async fn calcola(n: i32): i32 {
    return n * n;
}

let t = spawn(calcola, 42);
let risultato = await t;       // 1764

// Equivalente a join()
let t2 = spawn(calcola, 10);
let risultato2 = join(t2);     // 100
```

**Comportamento:**
- Identico a `join()`
- Attende il completamento del task
- Restituisce il risultato
- Propaga le eccezioni

---

## Pattern di Utilizzo

### Parallelismo Semplice

```hemlock
fn elabora(dati: array): array {
    // Elaborazione pesante
    return dati.map(fn(x) { return x * 2; });
}

// Elabora dataset in parallelo
let t1 = spawn(elabora, dati1);
let t2 = spawn(elabora, dati2);
let t3 = spawn(elabora, dati3);

let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

### Pattern Produttore-Consumatore

```hemlock
fn produttore(ch: channel, conteggio: i32) {
    let i = 0;
    while (i < conteggio) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
}

fn consumatore(ch: channel) {
    while (true) {
        let val = ch.recv();
        if (val == null && ch.closed) {
            break;
        }
        print("Elaborato:", val);
    }
}

let ch = channel(5);
let prod = spawn(produttore, ch, 10);
let cons = spawn(consumatore, ch);

join(prod);
join(cons);
```

### Pattern Worker Pool

```hemlock
fn worker(id: i32, lavori: channel, risultati: channel) {
    while (true) {
        let lavoro = lavori.recv();
        if (lavoro == null && lavori.closed) {
            break;
        }

        // Elabora lavoro
        let risultato = lavoro * lavoro;
        risultati.send({ worker_id: id, risultato: risultato });
    }
}

// Crea canali
let lavori = channel(100);
let risultati = channel(100);

// Crea worker
let worker1 = spawn(worker, 1, lavori, risultati);
let worker2 = spawn(worker, 2, lavori, risultati);
let worker3 = spawn(worker, 3, lavori, risultati);

// Invia lavori
let i = 0;
while (i < 10) {
    lavori.send(i);
    i = i + 1;
}
lavori.close();

// Raccogli risultati
let conteggio = 0;
while (conteggio < 10) {
    let r = risultati.recv();
    print("Worker", r.worker_id, ":", r.risultato);
    conteggio = conteggio + 1;
}

// Pulisci
join(worker1);
join(worker2);
join(worker3);
```

### Pattern Fan-Out/Fan-In

```hemlock
fn worker(lavoro: i32): i32 {
    return lavoro * lavoro;
}

// Fan-out: spawna più task
let task = [];
let i = 0;
while (i < 10) {
    task.push(spawn(worker, i));
    i = i + 1;
}

// Fan-in: raccogli risultati
let risultati = [];
i = 0;
while (i < task.length) {
    risultati.push(join(task[i]));
    i = i + 1;
}

print(risultati);  // [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### Gestione delle Eccezioni nei Task

```hemlock
fn lavoro_rischioso(): i32 {
    if (random() < 0.5) {
        throw "operazione fallita";
    }
    return 42;
}

let t = spawn(lavoro_rischioso);

try {
    let risultato = join(t);
    print("Successo:", risultato);
} catch (e) {
    print("Task fallito:", e);
}
```

### Modello di Timeout

```hemlock
// Nota: Questo è un pattern concettuale
// L'implementazione effettiva può variare

fn lavoro_lungo(): i32 {
    sleep(5000);  // 5 secondi
    return 42;
}

fn timeout_wrapper(func: function, timeout_ms: i32): any {
    let ch = channel(1);

    let worker = spawn(fn() {
        let risultato = func();
        ch.send(risultato);
    });

    // Attendi con timeout (concettuale)
    sleep(timeout_ms);
    if (ch.length == 0) {
        throw "operazione in timeout";
    }

    return ch.recv();
}
```

---

## Considerazioni sulla Sicurezza dei Thread

### Condivisione Dati

**Primitivi:** Passati per valore (sicuro)
```hemlock
let x = 42;
let t = spawn(fn() {
    print(x);  // Copia di x
});
```

**Oggetti/Array:** Passati per riferimento (usare cautela)
```hemlock
let arr = [1, 2, 3];
let t = spawn(fn() {
    // Condivide lo stesso array!
    arr.push(4);  // Potenziale race condition
});
```

**Canali:** Comunicazione thread-safe
```hemlock
// Passa dati tramite canali invece della memoria condivisa
let ch = channel(10);

let t = spawn(fn() {
    while (true) {
        let dati = ch.recv();
        if (dati == null) { break; }
        elabora(dati);
    }
});

ch.send({ x: 10, y: 20 });
```

### Best Practice

**1. Preferisci i Canali**
```hemlock
// BENE: Comunica tramite canali
let ch = channel(10);
let t = spawn(worker, ch);
ch.send(dati);
```

**2. Evita la Memoria Condivisa**
```hemlock
// MALE: Accesso condiviso all'array
let risultati = [];
let t1 = spawn(fn() { risultati.push(1); });
let t2 = spawn(fn() { risultati.push(2); });

// BENE: Ogni task ha il proprio spazio, merge dopo
let t1 = spawn(fn() { return [1]; });
let t2 = spawn(fn() { return [2]; });
let risultati = join(t1).concat(join(t2));
```

**3. Joina Sempre i Task**
```hemlock
// BENE: Pulizia appropriata
let t = spawn(lavoro);
let risultato = join(t);

// O detach se è fire-and-forget
let t2 = spawn(sfondo);
detach(t2);
```

---

## Riepilogo Completo delle Funzioni

### Funzioni

| Funzione  | Firma                          | Restituisce | Descrizione              |
|-----------|--------------------------------|-------------|--------------------------|
| `spawn`   | `(func, ...args)`              | `task`      | Crea nuovo task          |
| `join`    | `(t: task)`                    | `any`       | Attende risultato task   |
| `detach`  | `(t: task)`                    | `null`      | Detach task              |
| `channel` | `(capacita?: i32)`             | `channel`   | Crea canale              |

### Metodi dei Canali

| Metodo    | Firma                | Restituisce | Descrizione              |
|-----------|----------------------|-------------|--------------------------|
| `send`    | `(valore: any)`      | `null`      | Invia valore             |
| `recv`    | `()`                 | `any`       | Riceve valore            |
| `close`   | `()`                 | `null`      | Chiude canale            |

### Proprietà dei Canali

| Proprietà   | Tipo   | Descrizione                |
|-------------|--------|----------------------------|
| `.length`   | `i32`  | Elementi nel buffer        |
| `.capacity` | `i32`  | Dimensione massima buffer  |
| `.closed`   | `bool` | Se chiuso                  |

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Tipi task e channel
- [Funzioni Integrate](builtins.md) - Funzioni spawn, join, detach
- [Gestione delle Eccezioni](../language-guide/exceptions.md) - Propagazione eccezioni
