# Async e Concorrenza in Hemlock

Hemlock fornisce **concorrenza strutturata** con sintassi async/await, creazione di task e canali per la comunicazione. L'implementazione utilizza thread POSIX (pthread) per **VERO parallelismo multi-thread**.

## Indice

- [Panoramica](#panoramica)
- [Modello di Threading](#modello-di-threading)
- [Funzioni Async](#funzioni-async)
- [Creazione di Task](#creazione-di-task)
- [Canali](#canali)
- [Propagazione delle Eccezioni](#propagazione-delle-eccezioni)
- [Dettagli di Implementazione](#dettagli-di-implementazione)
- [Migliori Pratiche](#migliori-pratiche)
- [Caratteristiche di Prestazione](#caratteristiche-di-prestazione)
- [Limitazioni Attuali](#limitazioni-attuali)

## Panoramica

**Cosa significa:**
- **Thread del sistema operativo reali** - Ogni task creato viene eseguito su un pthread separato (thread POSIX)
- **Vero parallelismo** - I task vengono eseguiti simultaneamente su piu core della CPU
- **Schedulato dal kernel** - Lo scheduler del sistema operativo distribuisce i task sui core disponibili
- **Canali thread-safe** - Utilizza mutex pthread e variabili di condizione per la sincronizzazione

**Cosa NON e:**
- **NON green thread** - Non e multitasking cooperativo in spazio utente
- **NON coroutine async/await** - Non e un event loop single-thread come JavaScript/Python asyncio
- **NON concorrenza emulata** - Non e parallelismo simulato

Questo e lo **stesso modello di threading di C, C++ e Rust** quando si usano thread del sistema operativo. Si ottiene vera esecuzione parallela su piu core.

## Modello di Threading

### Threading 1:1

Hemlock utilizza un **modello di threading 1:1**, dove:
- Ogni task creato crea un thread dedicato del sistema operativo tramite `pthread_create()`
- Il kernel del sistema operativo schedula i thread sui core CPU disponibili
- Multitasking preemptivo - il sistema operativo puo interrompere e passare tra i thread
- **Nessun GIL** - A differenza di Python, non c'e un Global Interpreter Lock che limita il parallelismo

### Meccanismi di Sincronizzazione

- **Mutex** - I canali usano `pthread_mutex_t` per accesso thread-safe
- **Variabili di condizione** - send/recv bloccanti usano `pthread_cond_t` per attesa efficiente
- **Operazioni lock-free** - Le transizioni di stato dei task sono atomiche

## Funzioni Async

Le funzioni possono essere dichiarate come `async` per indicare che sono progettate per l'esecuzione concorrente:

```hemlock
async fn calcola(n: i32): i32 {
    let somma = 0;
    let i = 0;
    while (i < n) {
        somma = somma + i;
        i = i + 1;
    }
    return somma;
}
```

### Punti Chiave

- `async fn` dichiara una funzione asincrona
- Le funzioni async possono essere create come task concorrenti usando `spawn()`
- Le funzioni async possono anche essere chiamate direttamente (eseguite sincronamente nel thread corrente)
- Quando create con spawn, ogni task viene eseguito sul **proprio thread del sistema operativo** (non una coroutine!)
- La parola chiave `await` e riservata per uso futuro

### Esempio: Chiamata Diretta vs Spawn

```hemlock
async fn fattoriale(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * fattoriale(n - 1);
}

// Chiamata diretta - eseguita sincronamente
let risultato1 = fattoriale(5);  // 120

// Task creato - eseguito su thread separato
let task = spawn(fattoriale, 5);
let risultato2 = join(task);  // 120
```

## Creazione di Task

Usa `spawn()` per eseguire funzioni async **in parallelo su thread separati del sistema operativo**:

```hemlock
async fn fattoriale(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * fattoriale(n - 1);
}

// Crea piu task - questi vengono eseguiti IN PARALLELO su diversi core della CPU!
let t1 = spawn(fattoriale, 5);  // Thread 1
let t2 = spawn(fattoriale, 6);  // Thread 2
let t3 = spawn(fattoriale, 7);  // Thread 3

// Tutti e tre stanno calcolando simultaneamente in questo momento!

// Attendi i risultati
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### Funzioni Built-in

#### spawn(funzione_async, arg1, arg2, ...)

Crea un nuovo task su un nuovo pthread, restituisce un handle del task.

**Parametri:**
- `funzione_async` - La funzione async da eseguire
- `arg1, arg2, ...` - Argomenti da passare alla funzione

**Restituisce:** Handle del task (valore opaco usato con `join()` o `detach()`)

**Esempio:**
```hemlock
async fn elabora(dati: string, conteggio: i32): i32 {
    // ... logica di elaborazione
    return conteggio * 2;
}

let task = spawn(elabora, "test", 42);
```

#### join(task)

Attende il completamento del task (blocca fino al termine del thread), restituisce il risultato.

**Parametri:**
- `task` - Handle del task restituito da `spawn()`

**Restituisce:** Il valore restituito dalla funzione async

**Esempio:**
```hemlock
let task = spawn(calcola, 1000);
let risultato = join(task);  // Blocca fino al completamento di calcola()
print(risultato);
```

**Importante:** Ogni task puo essere joinato solo una volta. Join successivi daranno errore.

#### detach(task)

Esecuzione fire-and-forget (il thread viene eseguito indipendentemente, join non consentito).

**Parametri:**
- `task` - Handle del task restituito da `spawn()`

**Restituisce:** `null`

**Esempio:**
```hemlock
async fn lavoro_in_background() {
    // Task in background a lunga esecuzione
    // ...
}

let task = spawn(lavoro_in_background);
detach(task);  // Il task viene eseguito indipendentemente, non si puo fare join
```

**Importante:** I task detached non possono essere joinati. Sia il pthread che la struttura Task vengono automaticamente puliti quando il task viene completato.

## Canali

I canali forniscono comunicazione thread-safe tra task usando un buffer limitato con semantica bloccante.

### Creazione di Canali

```hemlock
let ch = channel(10);  // Crea canale con dimensione buffer di 10
```

**Parametri:**
- `capacita` (i32) - Numero massimo di valori che il canale puo contenere

**Restituisce:** Oggetto canale

### Metodi del Canale

#### send(valore)

Invia valore al canale (blocca se pieno).

```hemlock
async fn produttore(ch, conteggio: i32) {
    let i = 0;
    while (i < conteggio) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let task = spawn(produttore, ch, 5);
```

**Comportamento:**
- Se il canale ha spazio, il valore viene aggiunto immediatamente
- Se il canale e pieno, il mittente si blocca fino a quando lo spazio diventa disponibile
- Se il canale e chiuso, lancia un'eccezione

#### recv()

Riceve valore dal canale (blocca se vuoto).

```hemlock
async fn consumatore(ch, conteggio: i32): i32 {
    let somma = 0;
    let i = 0;
    while (i < conteggio) {
        let val = ch.recv();
        somma = somma + val;
        i = i + 1;
    }
    return somma;
}

let ch = channel(10);
let task = spawn(consumatore, ch, 5);
```

**Comportamento:**
- Se il canale ha valori, restituisce immediatamente il prossimo valore
- Se il canale e vuoto, il ricevitore si blocca fino a quando un valore e disponibile
- Se il canale e chiuso e vuoto, restituisce `null`

#### close()

Chiude il canale (recv su canale chiuso restituisce null).

```hemlock
ch.close();
```

**Comportamento:**
- Impedisce ulteriori operazioni `send()` (lanceranno eccezione)
- Permette alle operazioni `recv()` in sospeso di completarsi
- Una volta vuoto, `recv()` restituisce `null`

### Multiplexing con select()

La funzione `select()` permette di attendere su piu canali simultaneamente, restituendo quando qualsiasi canale ha dati disponibili.

**Firma:**
```hemlock
select(canali: array, timeout_ms?: i32): object | null
```

**Parametri:**
- `canali` - Array di valori canale
- `timeout_ms` (opzionale) - Timeout in millisecondi (-1 o omettere per attesa infinita)

**Restituisce:**
- `{ channel, value }` - Oggetto con il canale che aveva dati e il valore ricevuto
- `null` - Su timeout (se il timeout e stato specificato)

**Esempio:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Task produttori
spawn(fn() {
    sleep(100);
    ch1.send("dal canale 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("dal canale 2");
});

// Attende il primo risultato (ch2 dovrebbe essere piu veloce)
let risultato = select([ch1, ch2]);
print(risultato.value);  // "dal canale 2"

// Attende il secondo risultato
let risultato2 = select([ch1, ch2]);
print(risultato2.value);  // "dal canale 1"
```

**Con timeout:**
```hemlock
let ch = channel(1);

// Nessun mittente, andra in timeout
let risultato = select([ch], 100);  // timeout 100ms
if (risultato == null) {
    print("Timeout scaduto!");
}
```

**Casi d'uso:**
- Attendere il piu veloce tra piu sorgenti di dati
- Implementare timeout sulle operazioni del canale
- Pattern di event loop con piu sorgenti di eventi
- Fan-in: unire piu canali in uno

**Pattern fan-in:**
```hemlock
fn fan_in(canali: array, output: channel) {
    while (true) {
        let risultato = select(canali);
        if (risultato == null) {
            break;  // Tutti i canali chiusi
        }
        output.send(risultato.value);
    }
    output.close();
}
```

### Esempio Completo Produttore-Consumatore

```hemlock
async fn produttore(ch, conteggio: i32) {
    let i = 0;
    while (i < conteggio) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumatore(ch, conteggio: i32): i32 {
    let somma = 0;
    let i = 0;
    while (i < conteggio) {
        let val = ch.recv();
        somma = somma + val;
        i = i + 1;
    }
    return somma;
}

// Crea canale con dimensione buffer
let ch = channel(10);

// Crea produttore e consumatore
let p = spawn(produttore, ch, 5);
let c = spawn(consumatore, ch, 5);

// Attende il completamento
join(p);
let totale = join(c);  // 100 (0+10+20+30+40)
print(totale);
```

### Multi-Produttore, Multi-Consumatore

I canali possono essere condivisi in sicurezza tra piu produttori e consumatori:

```hemlock
async fn produttore(id: i32, ch, conteggio: i32) {
    let i = 0;
    while (i < conteggio) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumatore(id: i32, ch, conteggio: i32): i32 {
    let somma = 0;
    let i = 0;
    while (i < conteggio) {
        let val = ch.recv();
        somma = somma + val;
        i = i + 1;
    }
    return somma;
}

let ch = channel(20);

// Piu produttori
let p1 = spawn(produttore, 1, ch, 5);
let p2 = spawn(produttore, 2, ch, 5);

// Piu consumatori
let c1 = spawn(consumatore, 1, ch, 5);
let c2 = spawn(consumatore, 2, ch, 5);

// Attende tutti
join(p1);
join(p2);
let somma1 = join(c1);
let somma2 = join(c2);
print(somma1 + somma2);
```

## Propagazione delle Eccezioni

Le eccezioni lanciate nei task creati vengono propagate quando si fa join:

```hemlock
async fn operazione_rischiosa(deve_fallire: i32): i32 {
    if (deve_fallire == 1) {
        throw "Task fallito!";
    }
    return 42;
}

let t = spawn(operazione_rischiosa, 1);
try {
    let risultato = join(t);
} catch (e) {
    print("Catturato: " + e);  // "Catturato: Task fallito!"
}
```

### Pattern di Gestione delle Eccezioni

**Pattern 1: Gestire nel task**
```hemlock
async fn task_sicuro() {
    try {
        // operazione rischiosa
    } catch (e) {
        print("Errore nel task: " + e);
        return null;
    }
}

let task = spawn(task_sicuro);
join(task);  // Nessuna eccezione propagata
```

**Pattern 2: Propagare al chiamante**
```hemlock
async fn task_che_lancia() {
    throw "errore";
}

let task = spawn(task_che_lancia);
try {
    join(task);
} catch (e) {
    print("Catturato dal task: " + e);
}
```

**Pattern 3: Task detached con eccezioni**
```hemlock
async fn task_detached() {
    try {
        // lavoro
    } catch (e) {
        // Deve gestire internamente - non puo propagare
        print("Errore: " + e);
    }
}

let task = spawn(task_detached);
detach(task);  // Non si possono catturare eccezioni da task detached
```

## Dettagli di Implementazione

### Architettura di Threading

- **Threading 1:1** - Ogni task creato crea un thread dedicato del sistema operativo tramite `pthread_create()`
- **Schedulato dal kernel** - Il kernel del sistema operativo schedula i thread sui core CPU disponibili
- **Multitasking preemptivo** - Il sistema operativo puo interrompere e passare tra i thread
- **Nessun GIL** - A differenza di Python, non c'e un Global Interpreter Lock che limita il parallelismo

### Implementazione dei Canali

I canali usano un buffer circolare con sincronizzazione pthread:

```
Struttura Canale:
- buffer[] - Array di dimensione fissa di valori
- capacita - Numero massimo di elementi
- dimensione - Numero attuale di elementi
- testa - Posizione di lettura
- coda - Posizione di scrittura
- mutex - pthread_mutex_t per accesso thread-safe
- non_vuoto - pthread_cond_t per recv bloccante
- non_pieno - pthread_cond_t per send bloccante
- chiuso - Flag booleano
- refcount - Conteggio riferimenti per pulizia
```

**Comportamento bloccante:**
- `send()` su canale pieno: attende sulla variabile di condizione `non_pieno`
- `recv()` su canale vuoto: attende sulla variabile di condizione `non_vuoto`
- Entrambi sono segnalati quando appropriato dall'operazione opposta

### Memoria e Pulizia

- **Task joinati:** Automaticamente puliti dopo che `join()` restituisce
- **Task detached:** Automaticamente puliti quando il task viene completato
- **Canali:** Conteggio riferimenti e liberati quando non piu usati

## Migliori Pratiche

### 1. Chiudere Sempre i Canali

```hemlock
async fn produttore(ch) {
    // ... invia valori
    ch.close();  // Importante: segnala che non ci sono piu valori
}
```

### 2. Usare Concorrenza Strutturata

Creare task e fare join nello stesso scope:

```hemlock
fn elabora_dati(dati) {
    // Crea task
    let t1 = spawn(worker, dati);
    let t2 = spawn(worker, dati);

    // Sempre fare join prima di ritornare
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. Gestire le Eccezioni Appropriatamente

```hemlock
async fn task() {
    try {
        // operazione rischiosa
    } catch (e) {
        // Log errore
        throw e;  // Rilancia se il chiamante deve sapere
    }
}
```

### 4. Usare Capacita del Canale Appropriata

- **Piccola capacita (1-10):** Per coordinazione/segnalazione
- **Media capacita (10-100):** Per produttore-consumatore generale
- **Grande capacita (100+):** Per scenari ad alto throughput

```hemlock
let canale_segnale = channel(1);      // Coordinazione
let canale_lavoro = channel(50);      // Coda di lavoro
let canale_buffer = channel(1000);    // Alto throughput
```

### 5. Detach Solo Quando Necessario

Preferire `join()` rispetto a `detach()` per una migliore gestione delle risorse:

```hemlock
// Buono: Join e ottieni risultato
let task = spawn(lavoro);
let risultato = join(task);

// Usare detach solo per vero fire-and-forget
let task_bg = spawn(logging_in_background);
detach(task_bg);  // Verra eseguito indipendentemente
```

## Caratteristiche di Prestazione

### Vero Parallelismo

- **N task creati possono utilizzare N core CPU simultaneamente**
- Speedup provato - test di stress mostrano 8-9x tempo CPU vs tempo wall (piu core lavorano)
- Scalabilita lineare con il numero di core (fino al conteggio thread)

### Overhead dei Thread

- Ogni task ha ~8KB di stack + overhead pthread
- Costo di creazione thread: ~10-20us
- Costo di context switch: ~1-5us

### Quando Usare Async

**Buoni casi d'uso:**
- Calcoli CPU-intensivi che possono essere parallelizzati
- Operazioni I/O-bound (anche se l'I/O e ancora bloccante)
- Elaborazione concorrente di dati indipendenti
- Architetture pipeline con canali

**Non ideale per:**
- Task molto brevi (l'overhead del thread domina)
- Task con sincronizzazione pesante (overhead di contesa)
- Sistemi single-core (nessun beneficio dal parallelismo)

### I/O Bloccante e Sicuro

Le operazioni bloccanti in un task non bloccano gli altri:

```hemlock
async fn lettore(nomefile: string) {
    let f = open(nomefile, "r");  // Blocca solo questo thread
    let contenuto = f.read();     // Blocca solo questo thread
    f.close();
    return contenuto;
}

// Entrambi leggono concorrentemente (su thread diversi)
let t1 = spawn(lettore, "file1.txt");
let t2 = spawn(lettore, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## Modello di Thread Safety

Hemlock usa un modello di concorrenza **message-passing** dove i task comunicano tramite canali piuttosto che stato mutabile condiviso.

### Isolamento degli Argomenti

Quando crei un task con spawn, **gli argomenti vengono copiati in profondita** per prevenire data race:

```hemlock
async fn modifica_array(arr: array): array {
    arr.push(999);    // Modifica la COPIA, non l'originale
    arr[0] = -1;
    return arr;
}

let originale = [1, 2, 3];
let task = spawn(modifica_array, originale);
let modificato = join(task);

print(originale.length);  // 3 - invariato!
print(modificato.length);  // 4 - ha nuovo elemento
```

**Cosa viene copiato in profondita:**
- Array (e tutti gli elementi ricorsivamente)
- Oggetti (e tutti i campi ricorsivamente)
- Stringhe
- Buffer

**Cosa viene condiviso (riferimento mantenuto):**
- Canali (il meccanismo di comunicazione - intenzionalmente condiviso)
- Handle dei task (per coordinazione)
- Funzioni (il codice e immutabile)
- Handle dei file (il sistema operativo gestisce l'accesso concorrente)
- Handle dei socket (il sistema operativo gestisce l'accesso concorrente)

**Cosa non puo essere passato:**
- Puntatori raw (`ptr`) - usare `buffer` invece

### Perche Message-Passing?

Questo segue la filosofia "esplicito piuttosto che implicito" di Hemlock:

```hemlock
// MALE: Stato mutabile condiviso (causerebbe data race)
let contatore = { valore: 0 };
let t1 = spawn(fn() { contatore.valore = contatore.valore + 1; });  // Race!
let t2 = spawn(fn() { contatore.valore = contatore.valore + 1; });  // Race!

// BENE: Message-passing tramite canali
async fn incrementa(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(incrementa, ch);
join(t1);
let risultato = ch.recv();  // 1 - nessuna race condition
```

### Thread Safety del Conteggio Riferimenti

Tutte le operazioni di conteggio riferimenti usano **operazioni atomiche** per prevenire bug use-after-free:
- `string_retain/release` - atomico
- `array_retain/release` - atomico
- `object_retain/release` - atomico
- `buffer_retain/release` - atomico
- `function_retain/release` - atomico
- `channel_retain/release` - atomico
- `task_retain/release` - atomico

Questo garantisce gestione sicura della memoria anche quando i valori sono condivisi tra thread.

### Accesso all'Ambiente Closure

I task hanno accesso all'ambiente closure per:
- Funzioni built-in (`print`, `len`, ecc.)
- Definizioni di funzioni globali
- Costanti e variabili

L'ambiente closure e protetto da un mutex per-ambiente, rendendo
letture e scritture concorrenti thread-safe:

```hemlock
let x = 10;

async fn leggi_closure(): i32 {
    return x;  // OK: lettura variabile closure (thread-safe)
}

async fn modifica_closure() {
    x = 20;  // OK: scrittura variabile closure (sincronizzata con mutex)
}
```

**Nota:** Mentre l'accesso concorrente e sincronizzato, modificare stato condiviso da
piu task puo ancora portare a race condition logiche (ordinamento non deterministico).
Per comportamento prevedibile, usare canali per comunicazione tra task o
valori di ritorno dai task.

Se hai bisogno di restituire dati da un task, usa il valore di ritorno o i canali.

## Limitazioni Attuali

### 1. Nessuno Scheduler Work-Stealing

Usa 1 thread per task, che puo essere inefficiente per molti task brevi.

**Attuale:** 1000 task = 1000 thread (overhead pesante)

**Pianificato:** Thread pool con work stealing per migliore efficienza

### 3. Nessuna Integrazione I/O Asincrono

Le operazioni su file/rete bloccano ancora il thread:

```hemlock
async fn leggi_file(percorso: string) {
    let f = open(percorso, "r");
    let contenuto = f.read();  // Blocca il thread
    f.close();
    return contenuto;
}
```

**Workaround:** Usare piu thread per operazioni I/O concorrenti

### 4. Capacita del Canale Fissa

La capacita del canale e impostata alla creazione e non puo essere ridimensionata:

```hemlock
let ch = channel(10);
// Non si puo ridimensionare dinamicamente a 20
```

### 5. Dimensione del Canale e Fissa

La dimensione del buffer del canale non puo essere cambiata dopo la creazione.

## Pattern Comuni

### Map Parallelo

```hemlock
async fn map_worker(ch_in, ch_out, fn_trasforma) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let risultato = fn_trasforma(val);
        ch_out.send(risultato);
    }
    ch_out.close();
}

fn parallel_map(dati, fn_trasforma, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // Crea workers
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_trasforma));
        i = i + 1;
    }

    // Invia dati
    let i = 0;
    while (i < dati.length) {
        ch_in.send(dati[i]);
        i = i + 1;
    }
    ch_in.close();

    // Raccogli risultati
    let risultati = [];
    let i = 0;
    while (i < dati.length) {
        risultati.push(ch_out.recv());
        i = i + 1;
    }

    // Attendi i workers
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return risultati;
}
```

### Architettura Pipeline

```hemlock
async fn fase1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn fase2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// Crea pipeline
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(fase1, ch1, ch2);
let s2 = spawn(fase2, ch2, ch3);

// Alimenta input
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// Raccogli output
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### Fan-Out, Fan-In

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // Elabora valore
        let risultato = val * id;
        output_ch.send(risultato);
    }
}

let input = channel(10);
let output = channel(10);

// Fan-out: Piu workers
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// Invia lavoro
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// Fan-in: Raccogli tutti i risultati
let risultati = [];
let i = 0;
while (i < 10) {
    risultati.push(output.recv());
    i = i + 1;
}

// Attendi tutti i workers
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## Riepilogo

Il modello async/concorrenza di Hemlock fornisce:

- Vero parallelismo multi-thread usando thread del sistema operativo
- Primitive di concorrenza semplici e strutturate
- Canali thread-safe per la comunicazione
- Propagazione delle eccezioni tra task
- Prestazioni provate su sistemi multi-core
- **Isolamento degli argomenti** - copia profonda previene data race
- **Conteggio riferimenti atomico** - gestione sicura della memoria tra thread

Questo rende Hemlock adatto per:
- Calcoli paralleli
- Operazioni I/O concorrenti
- Architetture pipeline
- Pattern produttore-consumatore

Evitando la complessita di:
- Gestione manuale dei thread
- Primitive di sincronizzazione di basso livello
- Design basati su lock soggetti a deadlock
- Bug di stato mutabile condiviso
