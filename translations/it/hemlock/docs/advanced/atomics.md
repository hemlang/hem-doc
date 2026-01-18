# Operazioni Atomiche

Hemlock fornisce operazioni atomiche per la **programmazione concorrente lock-free**. Queste operazioni consentono la manipolazione sicura della memoria condivisa tra piu thread senza l'uso di lock o mutex tradizionali.

## Indice

- [Panoramica](#panoramica)
- [Quando Usare le Atomiche](#quando-usare-le-atomiche)
- [Modello di Memoria](#modello-di-memoria)
- [Load e Store Atomici](#load-e-store-atomici)
- [Operazioni Fetch-and-Modify](#operazioni-fetch-and-modify)
- [Compare-and-Swap (CAS)](#compare-and-swap-cas)
- [Exchange Atomico](#exchange-atomico)
- [Memory Fence](#memory-fence)
- [Riferimento Funzioni](#riferimento-funzioni)
- [Pattern Comuni](#pattern-comuni)
- [Migliori Pratiche](#migliori-pratiche)
- [Limitazioni](#limitazioni)

---

## Panoramica

Le operazioni atomiche sono operazioni **indivisibili** che si completano senza la possibilita di interruzione. Quando un thread esegue un'operazione atomica, nessun altro thread puo osservare l'operazione in uno stato parzialmente completato.

**Caratteristiche principali:**
- Tutte le operazioni usano **consistenza sequenziale** (`memory_order_seq_cst`)
- Tipi supportati: **i32** e **i64**
- Le operazioni lavorano su puntatori raw allocati con `alloc()`
- Thread-safe senza lock espliciti

**Operazioni disponibili:**
- Load/Store - Leggere e scrivere valori atomicamente
- Add/Sub - Operazioni aritmetiche che restituiscono il vecchio valore
- And/Or/Xor - Operazioni bitwise che restituiscono il vecchio valore
- CAS - Compare-and-swap per aggiornamenti condizionali
- Exchange - Scambiare valori atomicamente
- Fence - Barriera di memoria completa

---

## Quando Usare le Atomiche

**Usare le atomiche per:**
- Contatori condivisi tra task (es. conteggio richieste, tracciamento progresso)
- Flag e indicatori di stato
- Strutture dati lock-free
- Primitive di sincronizzazione semplici
- Codice concorrente critico per le prestazioni

**Usare i canali invece quando:**
- Si passano dati complessi tra task
- Si implementano pattern produttore-consumatore
- Si ha bisogno di semantica message-passing

**Esempio di caso d'uso - Contatore condiviso:**
```hemlock
// Alloca contatore condiviso
let contatore = alloc(4);
ptr_write_i32(contatore, 0);

async fn worker(contatore: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(contatore, 1);
        i = i + 1;
    }
}

// Crea piu workers
let t1 = spawn(worker, contatore, 1);
let t2 = spawn(worker, contatore, 2);
let t3 = spawn(worker, contatore, 3);

join(t1);
join(t2);
join(t3);

// Il contatore sara esattamente 3000 (nessuna data race)
print(atomic_load_i32(contatore));

free(contatore);
```

---

## Modello di Memoria

Tutte le operazioni atomiche di Hemlock usano **consistenza sequenziale** (`memory_order_seq_cst`), che fornisce le garanzie di ordinamento di memoria piu forti:

1. **Atomicita**: Ogni operazione e indivisibile
2. **Ordinamento totale**: Tutti i thread vedono lo stesso ordine delle operazioni
3. **Nessun riordinamento**: Le operazioni non vengono riordinate dal compilatore o dalla CPU

Questo rende piu semplice il ragionamento sul codice concorrente, a costo di alcune potenziali prestazioni rispetto a ordinamenti di memoria piu deboli.

---

## Load e Store Atomici

### atomic_load_i32 / atomic_load_i64

Legge atomicamente un valore dalla memoria.

**Firma:**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**Parametri:**
- `ptr` - Puntatore alla locazione di memoria (deve essere allineato correttamente)

**Restituisce:** Il valore nella locazione di memoria

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let valore = atomic_load_i32(p);
print(valore);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

Scrive atomicamente un valore in memoria.

**Firma:**
```hemlock
atomic_store_i32(ptr: ptr, valore: i32): null
atomic_store_i64(ptr: ptr, valore: i64): null
```

**Parametri:**
- `ptr` - Puntatore alla locazione di memoria
- `valore` - Valore da memorizzare

**Restituisce:** `null`

**Esempio:**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## Operazioni Fetch-and-Modify

Queste operazioni modificano atomicamente un valore e restituiscono il valore **precedente** (vecchio).

### atomic_add_i32 / atomic_add_i64

Aggiunge atomicamente a un valore.

**Firma:**
```hemlock
atomic_add_i32(ptr: ptr, valore: i32): i32
atomic_add_i64(ptr: ptr, valore: i64): i64
```

**Restituisce:** Il valore **precedente** (prima dell'addizione)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let vecchio = atomic_add_i32(p, 10);
print(vecchio);                    // 100 (valore precedente)
print(atomic_load_i32(p));         // 110 (nuovo valore)

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

Sottrae atomicamente da un valore.

**Firma:**
```hemlock
atomic_sub_i32(ptr: ptr, valore: i32): i32
atomic_sub_i64(ptr: ptr, valore: i64): i64
```

**Restituisce:** Il valore **precedente** (prima della sottrazione)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let vecchio = atomic_sub_i32(p, 25);
print(vecchio);                    // 100 (valore precedente)
print(atomic_load_i32(p));         // 75 (nuovo valore)

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

Esegue atomicamente AND bitwise.

**Firma:**
```hemlock
atomic_and_i32(ptr: ptr, valore: i32): i32
atomic_and_i64(ptr: ptr, valore: i64): i64
```

**Restituisce:** Il valore **precedente** (prima dell'AND)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 255 in binario: 11111111

let vecchio = atomic_and_i32(p, 0x0F);  // AND con 00001111
print(vecchio);                    // 255 (valore precedente)
print(atomic_load_i32(p));         // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

Esegue atomicamente OR bitwise.

**Firma:**
```hemlock
atomic_or_i32(ptr: ptr, valore: i32): i32
atomic_or_i64(ptr: ptr, valore: i64): i64
```

**Restituisce:** Il valore **precedente** (prima dell'OR)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 15 in binario: 00001111

let vecchio = atomic_or_i32(p, 0xF0);  // OR con 11110000
print(vecchio);                    // 15 (valore precedente)
print(atomic_load_i32(p));         // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

Esegue atomicamente XOR bitwise.

**Firma:**
```hemlock
atomic_xor_i32(ptr: ptr, valore: i32): i32
atomic_xor_i64(ptr: ptr, valore: i64): i64
```

**Restituisce:** Il valore **precedente** (prima dello XOR)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 170 in binario: 10101010

let vecchio = atomic_xor_i32(p, 0xFF);  // XOR con 11111111
print(vecchio);                    // 170 (valore precedente)
print(atomic_load_i32(p));         // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## Compare-and-Swap (CAS)

L'operazione atomica piu potente. Confronta atomicamente il valore attuale con un valore atteso e, se corrispondono, lo sostituisce con un nuovo valore.

### atomic_cas_i32 / atomic_cas_i64

**Firma:**
```hemlock
atomic_cas_i32(ptr: ptr, atteso: i32, desiderato: i32): bool
atomic_cas_i64(ptr: ptr, atteso: i64, desiderato: i64): bool
```

**Parametri:**
- `ptr` - Puntatore alla locazione di memoria
- `atteso` - Valore che ci aspettiamo di trovare
- `desiderato` - Valore da memorizzare se l'aspettativa corrisponde

**Restituisce:**
- `true` - Scambio riuscito (il valore era `atteso`, ora e `desiderato`)
- `false` - Scambio fallito (il valore non era `atteso`, invariato)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS riuscito: il valore e 100, scambia a 999
let successo1 = atomic_cas_i32(p, 100, 999);
print(successo1);                  // true
print(atomic_load_i32(p));         // 999

// CAS fallito: il valore e 999, non 100
let successo2 = atomic_cas_i32(p, 100, 888);
print(successo2);                  // false
print(atomic_load_i32(p));         // 999 (invariato)

free(p);
```

**Casi d'uso:**
- Implementazione di lock e semafori
- Strutture dati lock-free
- Controllo di concorrenza ottimistico
- Aggiornamenti condizionali atomici

---

## Exchange Atomico

Scambia atomicamente un valore, restituendo il vecchio valore.

### atomic_exchange_i32 / atomic_exchange_i64

**Firma:**
```hemlock
atomic_exchange_i32(ptr: ptr, valore: i32): i32
atomic_exchange_i64(ptr: ptr, valore: i64): i64
```

**Parametri:**
- `ptr` - Puntatore alla locazione di memoria
- `valore` - Nuovo valore da memorizzare

**Restituisce:** Il valore **precedente** (prima dello scambio)

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let vecchio = atomic_exchange_i32(p, 200);
print(vecchio);                    // 100 (valore precedente)
print(atomic_load_i32(p));         // 200 (nuovo valore)

free(p);
```

---

## Memory Fence

Una barriera di memoria completa che assicura che tutte le operazioni di memoria prima della fence siano visibili a tutti i thread prima di qualsiasi operazione dopo la fence.

### atomic_fence

**Firma:**
```hemlock
atomic_fence(): null
```

**Restituisce:** `null`

**Esempio:**
```hemlock
// Assicura che tutte le scritture precedenti siano visibili
atomic_fence();
```

**Nota:** Nella maggior parte dei casi, non hai bisogno di fence esplicite perche tutte le operazioni atomiche gia usano consistenza sequenziale. Le fence sono utili quando hai bisogno di sincronizzare operazioni di memoria non atomiche.

---

## Riferimento Funzioni

### Operazioni i32

| Funzione | Firma | Restituisce | Descrizione |
|----------|-------|-------------|-------------|
| `atomic_load_i32` | `(ptr)` | `i32` | Carica valore atomicamente |
| `atomic_store_i32` | `(ptr, valore)` | `null` | Memorizza valore atomicamente |
| `atomic_add_i32` | `(ptr, valore)` | `i32` | Aggiunge e restituisce vecchio valore |
| `atomic_sub_i32` | `(ptr, valore)` | `i32` | Sottrae e restituisce vecchio valore |
| `atomic_and_i32` | `(ptr, valore)` | `i32` | AND bitwise e restituisce vecchio valore |
| `atomic_or_i32` | `(ptr, valore)` | `i32` | OR bitwise e restituisce vecchio valore |
| `atomic_xor_i32` | `(ptr, valore)` | `i32` | XOR bitwise e restituisce vecchio valore |
| `atomic_cas_i32` | `(ptr, atteso, desiderato)` | `bool` | Compare-and-swap |
| `atomic_exchange_i32` | `(ptr, valore)` | `i32` | Scambia e restituisce vecchio valore |

### Operazioni i64

| Funzione | Firma | Restituisce | Descrizione |
|----------|-------|-------------|-------------|
| `atomic_load_i64` | `(ptr)` | `i64` | Carica valore atomicamente |
| `atomic_store_i64` | `(ptr, valore)` | `null` | Memorizza valore atomicamente |
| `atomic_add_i64` | `(ptr, valore)` | `i64` | Aggiunge e restituisce vecchio valore |
| `atomic_sub_i64` | `(ptr, valore)` | `i64` | Sottrae e restituisce vecchio valore |
| `atomic_and_i64` | `(ptr, valore)` | `i64` | AND bitwise e restituisce vecchio valore |
| `atomic_or_i64` | `(ptr, valore)` | `i64` | OR bitwise e restituisce vecchio valore |
| `atomic_xor_i64` | `(ptr, valore)` | `i64` | XOR bitwise e restituisce vecchio valore |
| `atomic_cas_i64` | `(ptr, atteso, desiderato)` | `bool` | Compare-and-swap |
| `atomic_exchange_i64` | `(ptr, valore)` | `i64` | Scambia e restituisce vecchio valore |

### Barriera di Memoria

| Funzione | Firma | Restituisce | Descrizione |
|----------|-------|-------------|-------------|
| `atomic_fence` | `()` | `null` | Barriera di memoria completa |

---

## Pattern Comuni

### Pattern: Contatore Atomico

```hemlock
// Contatore thread-safe
let contatore = alloc(4);
ptr_write_i32(contatore, 0);

fn incrementa(): i32 {
    return atomic_add_i32(contatore, 1);
}

fn decrementa(): i32 {
    return atomic_sub_i32(contatore, 1);
}

fn ottieni_conteggio(): i32 {
    return atomic_load_i32(contatore);
}

// Utilizzo
incrementa();  // Restituisce 0 (vecchio valore)
incrementa();  // Restituisce 1
incrementa();  // Restituisce 2
print(ottieni_conteggio());  // 3

free(contatore);
```

### Pattern: Spinlock

```hemlock
// Implementazione semplice di spinlock
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = sbloccato, 1 = bloccato

fn acquisisci() {
    // Gira finche non riesce a impostare il lock da 0 a 1
    while (!atomic_cas_i32(lock, 0, 1)) {
        // Attesa attiva
    }
}

fn rilascia() {
    atomic_store_i32(lock, 0);
}

// Utilizzo
acquisisci();
// ... sezione critica ...
rilascia();

free(lock);
```

### Pattern: Inizializzazione Una Tantum

```hemlock
let inizializzato = alloc(4);
ptr_write_i32(inizializzato, 0);  // 0 = non inizializzato, 1 = inizializzato

fn assicura_inizializzato() {
    // Prova a essere quello che inizializza
    if (atomic_cas_i32(inizializzato, 0, 1)) {
        // Abbiamo vinto la gara, esegui l'inizializzazione
        esegui_inizializzazione_costosa();
    }
    // Altrimenti, gia inizializzato
}
```

### Pattern: Flag Atomico

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn imposta_flag() {
    atomic_store_i32(flag, 1);
}

fn resetta_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // Restituisce true se il flag era gia impostato
    return atomic_exchange_i32(flag, 1) == 1;
}

fn controlla_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### Pattern: Contatore Limitato

```hemlock
let contatore = alloc(4);
ptr_write_i32(contatore, 0);
let valore_massimo = 100;

fn prova_incrementa(): bool {
    while (true) {
        let corrente = atomic_load_i32(contatore);
        if (corrente >= valore_massimo) {
            return false;  // Al massimo
        }
        if (atomic_cas_i32(contatore, corrente, corrente + 1)) {
            return true;  // Incrementato con successo
        }
        // CAS fallito, un altro thread ha modificato - riprova
    }
}
```

---

## Migliori Pratiche

### 1. Usare Allineamento Corretto

I puntatori devono essere allineati correttamente per il tipo di dato:
- i32: allineamento 4 byte
- i64: allineamento 8 byte

La memoria da `alloc()` e tipicamente allineata correttamente.

### 2. Preferire Astrazioni di Alto Livello

Quando possibile, usare i canali per la comunicazione inter-task. Le atomiche sono di livello piu basso e richiedono ragionamento attento.

```hemlock
// Preferire questo:
let ch = channel(10);
spawn(fn() { ch.send(risultato); });
let valore = ch.recv();

// Invece di coordinazione atomica manuale quando appropriato
```

### 3. Essere Consapevoli del Problema ABA

CAS puo soffrire del problema ABA: un valore cambia da A a B e torna ad A. Il tuo CAS ha successo, ma lo stato potrebbe essere cambiato nel frattempo.

### 4. Inizializzare Prima di Condividere

Inizializzare sempre le variabili atomiche prima di creare task che le accedono:

```hemlock
let contatore = alloc(4);
ptr_write_i32(contatore, 0);  // Inizializza PRIMA di fare spawn

let task = spawn(worker, contatore);
```

### 5. Liberare Dopo il Completamento di Tutti i Task

Non liberare memoria atomica mentre i task potrebbero ancora accedervi:

```hemlock
let contatore = alloc(4);
ptr_write_i32(contatore, 0);

let t1 = spawn(worker, contatore);
let t2 = spawn(worker, contatore);

join(t1);
join(t2);

// Ora e sicuro liberare
free(contatore);
```

---

## Limitazioni

### Limitazioni Attuali

1. **Solo i32 e i64 supportati** - Nessuna operazione atomica per altri tipi
2. **Nessuna atomica per puntatori** - Non si possono caricare/memorizzare puntatori atomicamente
3. **Solo consistenza sequenziale** - Nessun ordinamento di memoria piu debole disponibile
4. **Nessuna atomica in virgola mobile** - Usare rappresentazione intera se necessario

### Note sulla Piattaforma

- Le operazioni atomiche usano C11 `<stdatomic.h>` internamente
- Disponibile su tutte le piattaforme che supportano thread POSIX
- Garantito essere lock-free su moderni sistemi a 64 bit

---

## Vedi Anche

- [Async/Concorrenza](async-concurrency.md) - Creazione di task e canali
- [Gestione della Memoria](../language-guide/memory.md) - Allocazione di puntatori e buffer
- [API Memoria](../reference/memory-api.md) - Funzioni di allocazione
