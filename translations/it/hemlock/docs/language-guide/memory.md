# Gestione della Memoria

Hemlock abbraccia la **gestione manuale della memoria** con controllo esplicito sull'allocazione e deallocazione. Questa guida copre il modello di memoria di Hemlock, i due tipi di puntatore e l'API completa per la memoria.

---

## Memoria 101: Le Basi

**Nuovo alla programmazione?** Inizia da qui. Se conosci gia la gestione della memoria, vai a [Filosofia](#filosofia).

### Cos'e la Gestione della Memoria?

Quando il tuo programma deve memorizzare dati (testo, numeri, liste), ha bisogno di spazio dove metterli. Quello spazio viene dalla memoria del tuo computer (RAM). La gestione della memoria riguarda:

1. **Ottenere spazio** - chiedere memoria quando ne hai bisogno
2. **Usare lo spazio** - leggere e scrivere i tuoi dati
3. **Restituirlo** - restituire la memoria quando hai finito

### Perche e Importante?

Immagina una biblioteca con libri limitati:
- Se continui a prendere in prestito libri e non li restituisci mai, alla fine non ce ne sono piu
- Se provi a leggere un libro che hai gia restituito, ti confondi o causi problemi

La memoria funziona allo stesso modo. Se dimentichi di restituire la memoria, il tuo programma usa lentamente sempre di piu (un "memory leak"). Se provi a usare la memoria dopo averla restituita, succedono cose brutte.

### La Buona Notizia

**La maggior parte delle volte, non devi pensarci!**

Hemlock pulisce automaticamente i tipi piu comuni:

```hemlock
fn example() {
    let name = "Alice";       // Hemlock gestisce questo
    let numbers = [1, 2, 3];  // E questo
    let person = { age: 30 }; // E anche questo

    // Quando la funzione termina, tutto questo viene pulito automaticamente!
}
```

### Quando DEVI Pensarci

Hai bisogno della gestione manuale della memoria solo quando usi:

1. **`alloc()`** - allocazione di memoria grezza (restituisce `ptr`)
2. **`buffer()`** - quando vuoi liberare in anticipo (opzionale - si libera automaticamente alla fine dello scope)

```hemlock
// Questo richiede pulizia manuale:
let raw = alloc(100);   // Memoria grezza - TU devi liberarla
// ... usa raw ...
free(raw);              // Obbligatorio! Altrimenti hai un memory leak

// Questo si pulisce automaticamente (ma PUOI liberare in anticipo):
let buf = buffer(100);  // Buffer sicuro
// ... usa buf ...
// free(buf);           // Opzionale - si libera automaticamente quando lo scope termina
```

### La Regola Semplice

> **Se chiami `alloc()`, devi chiamare `free()`.**
>
> Tutto il resto e gestito per te.

### Quale Dovresti Usare?

| Situazione | Usa Questo | Perche |
|-----------|----------|-----|
| **Appena iniziato** | `buffer()` | Sicuro, con controllo dei limiti, pulizia automatica |
| **Serve memorizzazione di byte** | `buffer()` | Sicuro e facile |
| **Lavori con librerie C (FFI)** | `alloc()` / `ptr` | Richiesto per l'interoperabilita C |
| **Massime prestazioni** | `alloc()` / `ptr` | Nessun overhead per il controllo dei limiti |
| **Non sei sicuro** | `buffer()` | Sempre la scelta piu sicura |

### Esempio Rapido: Sicuro vs Grezzo

```hemlock
// CONSIGLIATO: Buffer sicuro
fn safe_example() {
    let data = buffer(10);
    data[0] = 65;           // OK
    data[5] = 66;           // OK
    // data[100] = 67;      // ERRORE - Hemlock ti ferma (controllo limiti)
    free(data);             // Pulizia
}

// AVANZATO: Puntatore grezzo (solo quando serve)
fn raw_example() {
    let data = alloc(10);
    *data = 65;             // OK
    *(data + 5) = 66;       // OK
    *(data + 100) = 67;     // PERICOLO - Nessun controllo limiti, corrompe la memoria!
    free(data);             // Pulizia
}
```

**Inizia con `buffer()`. Usa `alloc()` solo quando hai specificamente bisogno di puntatori grezzi.**

---

## Filosofia

Hemlock segue il principio della gestione esplicita della memoria con default sensati:
- Nessun garbage collection (nessuna pausa imprevedibile)
- Reference counting interno per i tipi comuni (string, array, object, buffer)
- I puntatori grezzi (`ptr`) richiedono `free()` manuale

Questo approccio ibrido ti da il controllo completo quando necessario (puntatori grezzi) mentre previene bug comuni per i casi d'uso tipici (tipi con reference count liberati automaticamente all'uscita dallo scope).

## Reference Counting Interno

Il runtime usa il **reference counting interno** per gestire la durata degli oggetti. Per la maggior parte delle variabili locali di tipi con reference count, la pulizia e automatica e deterministica.

### Cosa Gestisce il Reference Counting

Il runtime gestisce automaticamente i conteggi dei riferimenti quando:

1. **Le variabili vengono riassegnate** - il vecchio valore viene rilasciato:
   ```hemlock
   let x = "primo";   // ref_count = 1
   x = "secondo";     // "primo" rilasciato internamente, "secondo" ref_count = 1
   ```

2. **Gli scope terminano** - le variabili locali vengono rilasciate:
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // arr rilasciato quando la funzione ritorna
   ```

3. **I container vengono liberati** - gli elementi vengono rilasciati:
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // obj1 e obj2 ottengono i loro ref_count decrementati
   ```

### Quando Serve `free()` vs Quando e Automatico

**Automatico (nessun `free()` necessario):** Le variabili locali di tipi con reference count vengono liberate quando lo scope termina:

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... usali ...
}  // Tutto liberato automaticamente quando la funzione ritorna - nessun free() necessario
```

**`free()` manuale richiesto:**

1. **Puntatori grezzi** - `alloc()` non ha reference counting:
   ```hemlock
   let p = alloc(64);
   // ... usa p ...
   free(p);  // Sempre richiesto - altrimenti leak
   ```

2. **Pulizia anticipata** - libera prima della fine dello scope per rilasciare memoria prima:
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10MB
       // ... finito con big ...
       free(big);  // Libera ora, non aspettare che la funzione ritorni
       // ... altro lavoro che non ha bisogno di big ...
   }
   ```

3. **Dati a lunga vita** - globali o dati memorizzati in strutture persistenti:
   ```hemlock
   let cache = {};  // A livello di modulo, vive fino all'uscita del programma a meno che non venga liberato

   fn cleanup() {
       free(cache);  // Pulizia manuale per dati a lunga vita
   }
   ```

### Reference Counting vs Garbage Collection

| Aspetto | Reference Counting di Hemlock | Garbage Collection |
|--------|---------------------|-------------------|
| Tempistica pulizia | Deterministica (immediata quando ref arriva a 0) | Non deterministica (il GC decide quando) |
| Responsabilita utente | Deve chiamare `free()` | Completamente automatico |
| Pause del runtime | Nessuna | Pause "stop the world" |
| Visibilita | Dettaglio implementativo nascosto | Di solito invisibile |
| Cicli | Gestiti con tracciamento visited-set | Gestiti dal tracing |

### Quali Tipi Hanno il Reference Counting

| Tipo | Reference Counted | Note |
|------|------------|-------|
| `ptr` | No | Richiede sempre `free()` manuale |
| `buffer` | Si | Liberato automaticamente all'uscita dallo scope; `free()` manuale per pulizia anticipata |
| `array` | Si | Liberato automaticamente all'uscita dallo scope; `free()` manuale per pulizia anticipata |
| `object` | Si | Liberato automaticamente all'uscita dallo scope; `free()` manuale per pulizia anticipata |
| `string` | Si | Completamente automatico, nessun `free()` necessario |
| `function` | Si | Completamente automatico (ambienti delle closure) |
| `task` | Si | Reference counting atomico thread-safe |
| `channel` | Si | Reference counting atomico thread-safe |
| Primitivi | No | Allocati sullo stack, nessuna allocazione heap |

### Perche Questo Design?

Questo approccio ibrido ti da:
- **Controllo esplicito** - Tu decidi quando deallocare
- **Sicurezza dai bug di scope** - La riassegnazione non causa leak
- **Prestazioni prevedibili** - Nessuna pausa GC
- **Supporto closure** - Le funzioni possono catturare variabili in sicurezza

La filosofia rimane: sei tu al controllo, ma il runtime aiuta a prevenire bug comuni come leak alla riassegnazione o double-free nei container.

## I Due Tipi di Puntatore

Hemlock fornisce due tipi di puntatore distinti, ognuno con diverse caratteristiche di sicurezza:

### `ptr` - Puntatore Grezzo (Pericoloso)

I puntatori grezzi sono **solo indirizzi** con garanzie di sicurezza minime:

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Devi ricordarti di liberare
```

**Caratteristiche:**
- Solo un indirizzo di 8 byte
- Nessun controllo dei limiti
- Nessun tracciamento della lunghezza
- L'utente gestisce interamente la durata
- Per esperti e FFI

**Casi d'uso:**
- Programmazione di sistema a basso livello
- Foreign Function Interface (FFI)
- Codice critico per le prestazioni
- Quando hai bisogno di controllo completo

**Pericoli:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Molto oltre il limite dell'allocazione - permesso ma pericoloso
free(p);
let x = *p;       // Puntatore dangling - comportamento indefinito
free(p);          // Double-free - crashera
```

### `buffer` - Wrapper Sicuro (Consigliato)

I buffer forniscono **accesso con controllo dei limiti** richiedendo comunque deallocazione manuale:

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // controllo limiti
print(b.length);        // 64
free(b);                // sempre manuale
```

**Caratteristiche:**
- Puntatore + lunghezza + capacita
- Controllo dei limiti all'accesso
- Richiede comunque `free()` manuale
- Default migliore per la maggior parte del codice

**Proprieta:**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100 (dimensione attuale)
print(buf.capacity);    // 100 (capacita allocata)
```

**Controllo dei limiti:**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // OK
buf[100] = 42;    // ERRORE: Indice fuori dai limiti
```

## API della Memoria

### Allocazione Base

**`alloc(bytes)` - Alloca memoria grezza**
```hemlock
let p = alloc(1024);  // Alloca 1KB, restituisce ptr
// ... usa la memoria
free(p);
```

**`buffer(size)` - Alloca buffer sicuro**
```hemlock
let buf = buffer(256);  // Alloca buffer di 256 byte
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - Libera memoria**
```hemlock
let p = alloc(100);
free(p);  // Devi liberare per evitare memory leak

let buf = buffer(100);
free(buf);  // Funziona sia con ptr che con buffer
```

**Importante:** `free()` funziona sia con tipi `ptr` che `buffer`.

### Operazioni sulla Memoria

**`memset(ptr, byte, size)` - Riempi memoria**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // Azzera 100 byte
memset(p, 65, 10);     // Riempi i primi 10 byte con 'A'
free(p);
```

**`memcpy(dest, src, size)` - Copia memoria**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // Copia 50 byte da src a dst
free(src);
free(dst);
```

**`realloc(ptr, size)` - Ridimensiona allocazione**
```hemlock
let p = alloc(100);
// ... usa 100 byte
p = realloc(p, 200);   // Ridimensiona a 200 byte
// ... usa 200 byte
free(p);
```

**Nota:** Dopo `realloc()`, il vecchio puntatore potrebbe essere invalido. Usa sempre il puntatore restituito.

### Allocazione Tipizzata

Hemlock fornisce helper di allocazione tipizzata per comodita:

```hemlock
let arr = talloc(i32, 100);  // Alloca 100 valori i32 (400 byte)
let size = sizeof(i32);      // Restituisce 4 (byte)
```

**`sizeof(type)`** restituisce la dimensione in byte di un tipo:
- `sizeof(i8)` / `sizeof(u8)` -> 1
- `sizeof(i16)` / `sizeof(u16)` -> 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` -> 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` -> 8
- `sizeof(ptr)` -> 8 (su sistemi a 64 bit)

**`talloc(type, count)`** alloca `count` elementi di `type`:

```hemlock
let ints = talloc(i32, 10);   // 40 byte per 10 valori i32
let floats = talloc(f64, 5);  // 40 byte per 5 valori f64
free(ints);
free(floats);
```

## Pattern Comuni

### Pattern: Alloca, Usa, Libera

Il pattern base per la gestione della memoria:

```hemlock
// 1. Alloca
let data = alloc(1024);

// 2. Usa
memset(data, 0, 1024);
// ... fai il lavoro

// 3. Libera
free(data);
```

### Pattern: Uso Sicuro del Buffer

Preferisci i buffer per accesso con controllo dei limiti:

```hemlock
let buf = buffer(256);

// Iterazione sicura
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### Pattern: Gestione Risorse con try/finally

Assicura la pulizia anche in caso di errori:

```hemlock
let data = alloc(1024);
try {
    // ... operazioni rischiose
    process(data);
} finally {
    free(data);  // Sempre liberato, anche in caso di errore
}
```

## Considerazioni sulla Sicurezza della Memoria

### Double-Free

**Permesso ma crashera:**
```hemlock
let p = alloc(100);
free(p);
free(p);  // CRASH: Double-free rilevato
```

**Prevenzione:**
```hemlock
let p = alloc(100);
free(p);
p = null;  // Imposta a null dopo aver liberato

if (p != null) {
    free(p);  // Non verra eseguito
}
```

### Puntatori Dangling

**Permesso ma comportamento indefinito:**
```hemlock
let p = alloc(100);
*p = 42;      // OK
free(p);
let x = *p;   // INDEFINITO: Lettura di memoria liberata
```

**Prevenzione:** Non accedere alla memoria dopo averla liberata.

### Memory Leak

**Facili da creare, difficili da debuggare:**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // Dimenticato di liberare!
    return;  // Memoria persa
}
```

**Prevenzione:** Abbina sempre `alloc()` con `free()`:
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... usa p
    } finally {
        free(p);  // Sempre liberato
    }
}
```

### Aritmetica dei Puntatori

**Permessa ma pericolosa:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Molto oltre il limite dell'allocazione
*q = 42;          // INDEFINITO: Scrittura fuori dai limiti
free(p);
```

**Usa i buffer per il controllo dei limiti:**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // ERRORE: Il controllo dei limiti previene l'overflow
```

## Best Practice

1. **Default a `buffer`** - Usa `buffer` a meno che tu non abbia specificamente bisogno di `ptr` grezzo
2. **Abbina alloc/free** - Ogni `alloc()` dovrebbe avere esattamente un `free()`
3. **Usa try/finally** - Assicura la pulizia con la gestione delle eccezioni
4. **Null dopo free** - Imposta i puntatori a `null` dopo averli liberati per catturare use-after-free
5. **Controllo dei limiti** - Usa l'indicizzazione dei buffer per il controllo automatico dei limiti
6. **Documenta la proprieta** - Rendi chiaro quale codice possiede e libera ogni allocazione

## Esempi

### Esempio: Costruttore di Stringhe Dinamico

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // Il chiamante deve liberare
}

let msg = build_message(5);
// ... usa msg
free(msg);
```

### Esempio: Operazioni Sicure su Array

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // Riempi l'array
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // Elabora
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // Pulizia sempre
    }
}
```

### Esempio: Pattern Memory Pool

```hemlock
// Memory pool semplice (semplificato)
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool esaurito";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// Usa il pool
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// Libera l'intero pool in una volta
free(pool);
```

## Limitazioni

Limitazioni attuali di cui essere consapevoli:

- **I puntatori grezzi richiedono free manuale** - `alloc()` restituisce `ptr` senza reference counting
- **Nessun allocatore personalizzato** - Solo malloc/free di sistema

**Nota:** I tipi con reference count (string, array, object, buffer) SONO liberati automaticamente quando lo scope termina. Solo i `ptr` grezzi da `alloc()` richiedono `free()` esplicito.

## Argomenti Correlati

- [Stringhe](strings.md) - Gestione della memoria delle stringhe e codifica UTF-8
- [Array](arrays.md) - Array dinamici e loro caratteristiche di memoria
- [Oggetti](objects.md) - Allocazione e durata degli oggetti
- [Gestione degli Errori](error-handling.md) - Usare try/finally per la pulizia

## Vedi Anche

- **Filosofia di Design**: Vedi la sezione "Memory Management" in CLAUDE.md
- **Sistema di Tipi**: Vedi [Tipi](types.md) per i dettagli sui tipi `ptr` e `buffer`
- **FFI**: I puntatori grezzi sono essenziali per la Foreign Function Interface
