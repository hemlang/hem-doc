# Riferimento API della Memoria

Riferimento completo per le funzioni di gestione della memoria e i tipi di puntatore di Hemlock.

---

## Panoramica

Hemlock fornisce **gestione manuale della memoria** con allocazione e deallocazione esplicite. La memoria è gestita attraverso due tipi di puntatore: puntatori grezzi (`ptr`) e buffer sicuri (`buffer`).

**Principi Chiave:**
- Allocazione e deallocazione esplicite
- Nessun garbage collection
- L'utente è responsabile di chiamare `free()`
- Conteggio dei riferimenti interno per sicurezza di scope/riassegnazione (vedi sotto)

### Conteggio dei Riferimenti Interno

Il runtime usa il conteggio dei riferimenti internamente per gestire i tempi di vita degli oggetti attraverso gli scope. Per la maggior parte delle variabili locali, la pulizia è automatica.

**Automatico (nessun `free()` necessario):**
- Le variabili locali di tipi con conteggio riferimenti (buffer, array, oggetto, stringa) vengono liberate all'uscita dallo scope
- I vecchi valori vengono rilasciati quando le variabili vengono riassegnate
- Gli elementi dei contenitori vengono rilasciati quando i contenitori vengono liberati

**`free()` manuale richiesto:**
- Puntatori grezzi da `alloc()` - sempre
- Pulizia anticipata prima dell'uscita dallo scope
- Dati a lunga vita/globali

Vedi [Guida alla Gestione della Memoria](../language-guide/memory.md#internal-reference-counting) per dettagli.

---

## Tipi di Puntatore

### ptr (Puntatore Grezzo)

**Tipo:** `ptr`

**Descrizione:** Indirizzo di memoria grezzo senza controllo dei limiti o tracciamento.

**Dimensione:** 8 byte

**Casi d'Uso:**
- Operazioni di memoria a basso livello
- FFI (Foreign Function Interface)
- Massime prestazioni (nessun overhead)

**Sicurezza:** Non sicuro - nessun controllo dei limiti, l'utente deve tracciare il tempo di vita

**Esempi:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer (Buffer Sicuro)

**Tipo:** `buffer`

**Descrizione:** Wrapper sicuro del puntatore con controllo dei limiti.

**Struttura:** Puntatore + lunghezza + capacità + ref_count

**Proprietà:**
- `.length` - Dimensione del buffer (i32)
- `.capacity` - Capacità allocata (i32)

**Casi d'Uso:**
- La maggior parte delle allocazioni di memoria
- Quando la sicurezza è importante
- Array dinamici

**Sicurezza:** Controllo dei limiti nell'accesso all'indice

**Conteggio Riferimenti:** I buffer hanno conteggio riferimenti interno. Automaticamente liberati all'uscita dallo scope o quando la variabile viene riassegnata. Usa `free()` per pulizia anticipata o dati a lunga vita.

**Esempi:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Controllo limiti
print(b.length);        // 64
free(b);
```

---

## Funzioni di Allocazione della Memoria

### alloc

Alloca memoria grezza.

**Firma:**
```hemlock
alloc(dimensione: i32): ptr
```

**Parametri:**
- `dimensione` - Numero di byte da allocare

**Restituisce:** Puntatore alla memoria allocata (`ptr`)

**Esempi:**
```hemlock
let p = alloc(1024);        // Alloca 1KB
memset(p, 0, 1024);         // Inizializza a zero
free(p);                    // Libera quando finito

// Alloca per struttura
let dim_struct = 16;
let p2 = alloc(dim_struct);
```

**Comportamento:**
- Restituisce memoria non inizializzata
- La memoria deve essere liberata manualmente
- Restituisce `null` in caso di fallimento dell'allocazione (il chiamante deve verificare)

**Vedi Anche:** `buffer()` per alternativa più sicura

---

### buffer

Alloca buffer sicuro con controllo dei limiti.

**Firma:**
```hemlock
buffer(dimensione: i32): buffer
```

**Parametri:**
- `dimensione` - Dimensione del buffer in byte

**Restituisce:** Oggetto buffer

**Esempi:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// Accesso con controllo limiti
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // ERRORE: fuori limiti

free(buf);
```

**Proprietà:**
- `.length` - Dimensione corrente (i32)
- `.capacity` - Capacità allocata (i32)

**Comportamento:**
- Inizializza la memoria a zero
- Fornisce controllo limiti nell'accesso all'indice
- Restituisce `null` in caso di fallimento dell'allocazione (il chiamante deve verificare)
- Deve essere liberato manualmente

---

### free

Libera memoria allocata.

**Firma:**
```hemlock
free(ptr: ptr | buffer): null
```

**Parametri:**
- `ptr` - Puntatore o buffer da liberare

**Restituisce:** `null`

**Esempi:**
```hemlock
// Libera puntatore grezzo
let p = alloc(1024);
free(p);

// Libera buffer
let buf = buffer(256);
free(buf);
```

**Comportamento:**
- Libera memoria allocata da `alloc()` o `buffer()`
- Double-free causa crash (responsabilità dell'utente evitarlo)
- Liberare puntatori non validi causa comportamento indefinito

**Importante:** Tu allochi, tu liberi. Nessuna pulizia automatica.

---

### realloc

Ridimensiona memoria allocata.

**Firma:**
```hemlock
realloc(ptr: ptr, nuova_dimensione: i32): ptr
```

**Parametri:**
- `ptr` - Puntatore da ridimensionare
- `nuova_dimensione` - Nuova dimensione in byte

**Restituisce:** Puntatore alla memoria ridimensionata (potrebbe essere indirizzo diverso)

**Esempi:**
```hemlock
let p = alloc(100);
// ... usa memoria ...

// Serve più spazio
p = realloc(p, 200);        // Ora 200 byte
// ... usa memoria espansa ...

free(p);
```

**Comportamento:**
- Potrebbe spostare la memoria in nuova posizione
- Preserva dati esistenti (fino al minimo tra vecchia/nuova dimensione)
- Il vecchio puntatore non è valido dopo realloc riuscito (usa il puntatore restituito)
- Se nuova_dimensione è più piccola, i dati vengono troncati
- Restituisce `null` in caso di fallimento (il puntatore originale rimane valido)

**Importante:** Verifica sempre `null` e aggiorna la tua variabile puntatore con il risultato.

---

## Operazioni sulla Memoria

### memset

Riempie la memoria con un valore byte.

**Firma:**
```hemlock
memset(ptr: ptr, byte: i32, dimensione: i32): null
```

**Parametri:**
- `ptr` - Puntatore alla memoria
- `byte` - Valore byte da riempire (0-255)
- `dimensione` - Numero di byte da riempire

**Restituisce:** `null`

**Esempi:**
```hemlock
let p = alloc(100);

// Azzera la memoria
memset(p, 0, 100);

// Riempi con valore specifico
memset(p, 0xFF, 100);

// Inizializza buffer
let buf = alloc(256);
memset(buf, 65, 256);       // Riempi con 'A'

free(p);
free(buf);
```

**Comportamento:**
- Scrive il valore byte su ogni byte nell'intervallo
- Il valore byte è troncato a 8 bit (0-255)
- Nessun controllo limiti (non sicuro)

---

### memcpy

Copia memoria da sorgente a destinazione.

**Firma:**
```hemlock
memcpy(dest: ptr, src: ptr, dimensione: i32): null
```

**Parametri:**
- `dest` - Puntatore destinazione
- `src` - Puntatore sorgente
- `dimensione` - Numero di byte da copiare

**Restituisce:** `null`

**Esempi:**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// Inizializza sorgente
memset(src, 65, 100);

// Copia a destinazione
memcpy(dest, src, 100);

// dest ora contiene gli stessi dati di src

free(src);
free(dest);
```

**Comportamento:**
- Copia byte per byte da src a dest
- Nessun controllo limiti (non sicuro)
- Regioni sovrapposte hanno comportamento indefinito (usa con cautela)

---

## Operazioni sulla Memoria Tipizzate

### sizeof

Ottiene la dimensione di un tipo in byte.

**Firma:**
```hemlock
sizeof(tipo): i32
```

**Parametri:**
- `tipo` - Identificatore di tipo (es. `i32`, `f64`, `ptr`)

**Restituisce:** Dimensione in byte (i32)

**Dimensioni dei Tipi:**

| Tipo | Dimensione (byte) |
|------|-------------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**Esempi:**
```hemlock
let dim_int = sizeof(i32);      // 4
let dim_ptr = sizeof(ptr);      // 8
let dim_float = sizeof(f64);    // 8
let dim_byte = sizeof(u8);      // 1
let dim_rune = sizeof(rune);    // 4

// Calcola dimensione allocazione array
let conteggio = 100;
let totale = sizeof(i32) * conteggio; // 400 byte
```

**Comportamento:**
- Restituisce 0 per tipi sconosciuti
- Accetta sia identificatori di tipo che stringhe di tipo

---

### talloc

Alloca array di valori tipizzati.

**Firma:**
```hemlock
talloc(tipo, conteggio: i32): ptr
```

**Parametri:**
- `tipo` - Tipo da allocare (es. `i32`, `f64`, `ptr`)
- `conteggio` - Numero di elementi (deve essere positivo)

**Restituisce:** Puntatore all'array allocato, o `null` in caso di fallimento

**Esempi:**
```hemlock
let arr = talloc(i32, 100);      // Array di 100 i32 (400 byte)
let floats = talloc(f64, 50);    // Array di 50 f64 (400 byte)
let bytes = talloc(u8, 1024);    // Array di 1024 byte

// Verifica sempre il fallimento dell'allocazione
if (arr == null) {
    panic("allocazione fallita");
}

// Usa la memoria allocata
// ...

free(arr);
free(floats);
free(bytes);
```

**Comportamento:**
- Alloca `sizeof(tipo) * conteggio` byte
- Restituisce memoria non inizializzata
- La memoria deve essere liberata manualmente con `free()`
- Restituisce `null` in caso di fallimento dell'allocazione (il chiamante deve verificare)
- Va in panic se il conteggio non è positivo

---

## Interoperabilità Puntatore/Buffer

Tutte le funzioni builtin `ptr_read_*`, `ptr_write_*` e `ptr_deref_*` accettano sia tipi `ptr` che `buffer` direttamente. Quando viene passato un buffer, l'operazione usa il puntatore dati sottostante del buffer.

```hemlock
let buf = buffer(16);

// Scrivi direttamente su un buffer (non serve estrarre il ptr prima)
ptr_write_i32(buf, 42);
ptr_write_f64(ptr_offset(buffer_ptr(buf), 4), 3.14);

// Leggi direttamente da un buffer
let val = ptr_read_i32(buf);      // 42
let fval = ptr_deref_i32(buf);    // 42

// Funziona anche con puntatori grezzi come prima
let p = alloc(8);
ptr_write_i32(p, 99);
let pval = ptr_read_i32(p);      // 99
free(p);
```

Questo elimina la necessità di chiamare `buffer_ptr()` prima di ogni operazione di lettura/scrittura tipizzata, rendendo il codice basato su buffer più conciso.

---

## Proprietà del Buffer

### .length

Ottiene la dimensione del buffer.

**Tipo:** `i32`

**Accesso:** Sola lettura

**Esempi:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

Ottiene la capacità del buffer.

**Tipo:** `i32`

**Accesso:** Sola lettura

**Esempi:**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**Nota:** Attualmente, `.length` e `.capacity` sono uguali per i buffer creati con `buffer()`.

---

## Metodi del Buffer

### .slice

Crea una vista a zero-copy nella memoria del buffer. La vista restituita condivide la stessa memoria sottostante del buffer padre -- le modifiche all'originale sono visibili attraverso la vista e viceversa.

**Firma:**
```hemlock
buffer.slice(inizio: i32, fine?: i32): buffer
```

**Parametri:**
- `inizio` - Offset byte iniziale (base 0, inclusivo). I valori negativi vengono limitati a 0.
- `fine` - Offset byte finale (esclusivo). Default a `buffer.length` se omesso. I valori oltre la lunghezza del buffer vengono limitati.

**Restituisce:** Vista del buffer (zero-copy)

**Esempi:**
```hemlock
let buf = buffer(10);
for (let i = 0; i < 10; i++) {
    buf[i] = i + 65;  // A=65, B=66, ...
}

// Slice base
let vista = buf.slice(2, 5);
print(vista.length);    // 3
print(vista[0]);        // 67 (C)

// Prova zero-copy: modificare l'originale è visibile attraverso la vista
buf[3] = 90;           // Cambia D(68) a Z(90)
print(vista[1]);       // 90 (riflette la modifica del padre)

// Slice a singolo argomento (dall'indice alla fine)
let coda = buf.slice(7);
print(coda.length);    // 3
```

**Comportamento:**
- Restituisce una vista a zero-copy -- nessuna memoria viene allocata per i dati
- Le viste mantengono un riferimento al buffer radice (previene use-after-free)
- Il controllo dei limiti viene eseguito relativo all'intervallo della vista
- **Non puoi** fare `free()` su un buffer vista -- solo il buffer radice dovrebbe essere liberato

---

## Metodi di Lettura/Scrittura Tipizzati del Buffer

I buffer forniscono metodi di lettura e scrittura tipizzati con consapevolezza dell'endianness per costruire e analizzare strutture dati binarie come pacchetti di rete, formati di file e protocolli wire. Questi metodi hanno controllo dei limiti e sollevano errori a runtime in caso di accesso fuori dai limiti.

### Metodi di Scrittura

Scrivono un valore tipizzato a un offset in byte. I suffissi `_le` e `_be` specificano rispettivamente l'ordine dei byte little-endian e big-endian.

```hemlock
let pkt = buffer(64);
let offset = 0;

// Costruisci un header di pacchetto
pkt.write_u16_be(offset, 0x0800);    // EtherType: IPv4
offset += 2;
pkt.write_u8(offset, 0x45);          // Version + IHL
offset += 1;
pkt.write_u32_be(offset, 0xC0A80001); // IP Sorgente: 192.168.0.1
offset += 4;

// Valori float
pkt.write_f32_le(offset, 3.14);
offset += 4;
pkt.write_f64_be(offset, 2.71828);
offset += 8;
```

**Le scritture a singolo byte** (`write_u8`, `write_i8`) non hanno suffisso di endianness poiché l'ordine dei byte è irrilevante per singoli byte.

### Metodi di Lettura

Leggono un valore tipizzato da un offset in byte. I suffissi di endianness corrispondono ai metodi di scrittura.

```hemlock
let pkt = buffer(64);
// ... riempi il buffer con dati ...

// Analizza un header di pacchetto
let ether_type = pkt.read_u16_be(0);    // 0x0800
let version = pkt.read_u8(2);            // 0x45
let src_ip = pkt.read_u32_be(6);         // 0xC0A80001
```

### Operazioni in Blocco

```hemlock
let src = buffer(8);
for (let i = 0; i < 8; i++) { src[i] = i + 1; }

let dest = buffer(32);
dest.write_bytes(4, src);          // Copia src in dest all'offset 4

let chunk = dest.read_bytes(4, 8); // Leggi 8 byte a partire dall'offset 4
print(chunk[0]);                   // 1
```

### Controllo dei Limiti

Tutti i metodi di lettura/scrittura tipizzati validano che l'intero valore rientri nel buffer. Per esempio, `write_u32_be(offset, val)` verifica che `offset + 4 <= buffer.length`.

```hemlock
let buf = buffer(4);
buf.write_u32_be(0, 42);    // OK: 4 byte ci stanno
// buf.write_u32_be(2, 42); // ERRORE: scriverebbe oltre la fine (offset 2 + 4 > 4)
```

### Casi d'Uso

- **Protocolli di rete:** Costruire/analizzare pacchetti TCP, UDP, DNS e personalizzati
- **Formati file binari:** Leggere/scrivere header di immagini, formati di archivio, ecc.
- **Protocolli wire:** Serializzare/deserializzare messaggi binari strutturati
- **Scambio dati FFI:** Preparare buffer per chiamate a librerie C

---

## Pattern di Utilizzo

### Pattern di Allocazione Base

```hemlock
// Alloca
let p = alloc(1024);
if (p == null) {
    panic("allocazione fallita");
}

// Usa
memset(p, 0, 1024);

// Libera
free(p);
```

### Pattern Buffer Sicuro

```hemlock
// Alloca buffer
let buf = buffer(256);
if (buf == null) {
    panic("allocazione buffer fallita");
}

// Usa con controllo limiti
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// Libera
free(buf);
```

### Pattern di Crescita Dinamica

```hemlock
let dimensione = 100;
let p = alloc(dimensione);
if (p == null) {
    panic("allocazione fallita");
}

// ... usa memoria ...

// Serve più spazio - verifica fallimento
let nuovo_p = realloc(p, 200);
if (nuovo_p == null) {
    // Il puntatore originale è ancora valido, pulisci
    free(p);
    panic("realloc fallito");
}
p = nuovo_p;
dimensione = 200;

// ... usa memoria espansa ...

free(p);
```

### Pattern di Copia Memoria

```hemlock
let originale = alloc(100);
memset(originale, 65, 100);

// Crea copia
let copia = alloc(100);
memcpy(copia, originale, 100);

free(originale);
free(copia);
```

---

## Considerazioni sulla Sicurezza

**La gestione della memoria di Hemlock è NON SICURA per design:**

### Trappole Comuni

**1. Memory Leak**
```hemlock
// MALE: Memory leak
fn crea_buffer() {
    let p = alloc(1024);
    return null;  // Memoria persa!
}

// BENE: Pulizia appropriata
fn crea_buffer() {
    let p = alloc(1024);
    // ... usa memoria ...
    free(p);
    return null;
}
```

**2. Use After Free**
```hemlock
// MALE: Use after free
let p = alloc(100);
free(p);
memset(p, 0, 100);  // CRASH: uso di memoria liberata

// BENE: Non usare dopo free
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// Non toccare p2 dopo questo
```

**3. Double Free**
```hemlock
// MALE: Double free
let p = alloc(100);
free(p);
free(p);  // CRASH: double free

// BENE: Libera una volta sola
let p2 = alloc(100);
free(p2);
```

**4. Buffer Overflow (ptr)**
```hemlock
// MALE: Buffer overflow con ptr
let p = alloc(10);
memset(p, 65, 100);  // CRASH: scrittura oltre allocazione

// BENE: Usa buffer per controllo limiti
let buf = buffer(10);
// buf[100] = 65;  // ERRORE: controllo limiti fallisce
```

**5. Dangling Pointers**
```hemlock
// MALE: Dangling pointer
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // CRASH: p2 è dangling

// BENE: Traccia ownership attentamente
let p = alloc(100);
// ... usa p ...
free(p);
// Non mantenere altri riferimenti a p
```

**6. Fallimento Allocazione Non Verificato**
```hemlock
// MALE: Non verificare null
let p = alloc(1000000000);  // Potrebbe fallire con poca memoria
memset(p, 0, 1000000000);   // CRASH: p è null

// BENE: Verifica sempre il risultato dell'allocazione
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("memoria esaurita");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## Quando Usare Cosa

### Usa `buffer()` quando:
- Hai bisogno di controllo limiti
- Lavori con dati dinamici
- La sicurezza è importante
- Stai imparando Hemlock

### Usa `alloc()` quando:
- Servono prestazioni massime
- FFI/interfacciamento con C
- Conosci esattamente il layout della memoria
- Sei un esperto

### Usa `realloc()` quando:
- Devi crescere/ridurre allocazioni
- Array dinamici
- Devi preservare i dati

---

## Riepilogo Completo delle Funzioni

| Funzione  | Firma                              | Restituisce | Descrizione                |
|-----------|------------------------------------|-------------|----------------------------|
| `alloc`   | `(dimensione: i32)`                | `ptr`       | Alloca memoria grezza      |
| `buffer`  | `(dimensione: i32)`                | `buffer`    | Alloca buffer sicuro       |
| `free`    | `(ptr: ptr \| buffer)`             | `null`      | Libera memoria             |
| `realloc` | `(ptr: ptr, nuova_dim: i32)`       | `ptr`       | Ridimensiona allocazione   |
| `memset`  | `(ptr: ptr, byte: i32, dim: i32)`  | `null`      | Riempie memoria            |
| `memcpy`  | `(dest: ptr, src: ptr, dim: i32)`  | `null`      | Copia memoria              |
| `sizeof`  | `(tipo)`                           | `i32`       | Ottiene dimensione tipo in byte |
| `talloc`  | `(tipo, conteggio: i32)`           | `ptr`       | Alloca array tipizzato     |

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Tipi puntatore e buffer
- [Funzioni Integrate](builtins.md) - Tutte le funzioni integrate
- [API delle Stringhe](string-api.md) - Metodo `.to_bytes()` delle stringhe
