# Annotazioni Helper del Compilatore: Analisi e Proposta

**Autore:** Claude
**Data:** 2026-01-08
**Stato:** Parzialmente Implementato (Fase 1-2 completate nella v1.9.0; Fase 3-5 rimangono proposte)
**Correlato:** Issue #TBD

## Indice

1. [Sommario Esecutivo](#sommario-esecutivo)
2. [Analisi dello Stato Attuale](#analisi-dello-stato-attuale)
3. [Annotazioni Proposte](#annotazioni-proposte)
4. [Piano di Implementazione](#piano-di-implementazione)
5. [Esempi](#esempi)
6. [Strategia di Testing](#strategia-di-testing)
7. [Considerazioni Future](#considerazioni-future)

---

## Sommario Esecutivo

Il sistema di annotazioni di Hemlock fornisce una base robusta per aggiungere hint e direttive del compilatore. Questa proposta estende l'infrastruttura di annotazioni attuale con **15 nuove annotazioni helper del compilatore** organizzate in cinque categorie:

- **Hint di Ottimizzazione** (7 annotazioni)
- **Gestione della Memoria** (3 annotazioni)
- **Controllo della Generazione del Codice** (2 annotazioni)
- **Controllo degli Errori** (2 annotazioni)
- **FFI/Interop** (1 annotazione)

Queste annotazioni consentiranno agli sviluppatori di fornire guida esplicita al compilatore (`hemlockc`) mantenendo la retrocompatibilità con l'interprete.

---

## Analisi dello Stato Attuale

### 1. Infrastruttura delle Annotazioni

Il sistema di annotazioni è completamente implementato con tre componenti principali:

**Parser** (`src/frontend/parser/statements.c`):
- Analizza la sintassi `@name` e `@name(args...)`
- Supporta argomenti posizionali e nominati
- Associa le annotazioni alle dichiarazioni (let, const, define, enum)

**Validatore** (`src/frontend/annotations.c`):
- Valida i target delle annotazioni (funzione, tipo, variabile, ecc.)
- Verifica conteggi e tipi degli argomenti
- Avvisa su annotazioni sconosciute o duplicate

**Risolutore** (`src/frontend/resolver.c`):
- Memorizza le annotazioni insieme alle definizioni delle variabili
- Abilita il lookup delle annotazioni durante l'analisi semantica
- Alimenta gli avvisi `@deprecated` sull'uso delle variabili

### 2. Annotazioni Attualmente Implementate

```c
// Annotazioni di sicurezza (per il memory checker Tricycle)
@safe       // La funzione è memory-safe
@unsafe     // La funzione contiene operazioni non sicure
@trusted    // La funzione è fidata nonostante operazioni non sicure

// Hint di ottimizzazione del compilatore (IMPLEMENTATI nella v1.9.0)
@inline     // Suggerisci l'inlining di questa funzione
@noinline   // Impedisci l'inlining di questa funzione
@cold       // La funzione è eseguita raramente
@hot        // La funzione è eseguita frequentemente
@pure       // La funzione non ha effetti collaterali

// Altre annotazioni
@deprecated      // Segna come deprecata con messaggio opzionale
@test, @skip     // Annotazioni del framework di testing
@author, @since  // Annotazioni di documentazione
```

### 3. Limitazioni Attuali

**Aggiornamento (v1.9.0):** Le annotazioni core a livello di funzione (`@inline`, `@noinline`, `@hot`, `@cold`, `@pure`, `@const`, `@flatten`, `@optimize`, `@warn_unused`, `@section`) sono ora completamente implementate nel backend del compilatore. Le proposte rimanenti (annotazioni ciclo, annotazioni memoria) nelle Fasi 3-5 seguenti sono ancora non implementate.

---

## Annotazioni Proposte

### Categoria 1: Hint di Ottimizzazione

#### `@unroll(count?: number)`
**Target:** Cicli (for, while)
**Argomenti:** Fattore di srotolamento opzionale (default: decide il compilatore)

Suggerisce lo srotolamento del ciclo per cicli stretti critici per le prestazioni.

```hemlock
@unroll(4)
for (let i = 0; i < 1024; i++) {
    buffer[i] = buffer[i] * 2;
}
```

#### `@simd` / `@nosimd`
**Target:** Funzioni, cicli

Abilita o disabilita la vettorizzazione SIMD.

```hemlock
@simd
fn vector_add(a: buffer, b: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        ptr_write_f64(a, i, ptr_read_f64(a, i) + ptr_read_f64(b, i));
    }
}
```

#### `@likely` / `@unlikely`
**Target:** Istruzioni if, condizionali

Hint per la predizione dei branch nei percorsi critici.

```hemlock
@likely
if (cache.has(key)) {
    return cache.get(key);
}

@unlikely
if (error) {
    handle_error(error);
}
```

#### `@const`
**Target:** Funzioni

La funzione restituisce sempre lo stesso risultato per gli stessi input (più forte di `@pure`).

```hemlock
@const
fn square(x: i32): i32 => x * x;
```

**Differenza da `@pure`:**
- `@pure`: Può leggere la memoria globale, ma non la modifica
- `@const`: Non può nemmeno leggere la memoria globale, usa solo i parametri

#### `@tail_call`
**Target:** Chiamate di funzione

Richiede l'ottimizzazione della chiamata in coda (TCO).

```hemlock
fn factorial_helper(n: i32, acc: i32): i32 {
    if (n <= 1) { return acc; }
    @tail_call
    return factorial_helper(n - 1, n * acc);
}
```

#### `@flatten`
**Target:** Funzioni

Esegue l'inlining di tutte le chiamate all'interno di questa funzione.

```hemlock
@flatten
fn compute_hash(data: buffer, len: i32): u64 {
    let hash = init_hash();
    hash = process_block(hash, data, len);
    return finalize_hash(hash);
}
```

#### `@optimize(level: string)`
**Target:** Funzioni
**Argomenti:** Livello di ottimizzazione ("0", "1", "2", "3", "s", "fast")

Sovrascrive il livello di ottimizzazione globale per una funzione specifica.

```hemlock
@optimize("3")
fn matrix_multiply(a: buffer, b: buffer, n: i32) {
    // Ciclo interno critico per le prestazioni
}

@optimize("s")
fn rarely_called_error_handler() {
    // Ottimizza per dimensione, non velocità
}
```

### Categoria 2: Gestione della Memoria

#### `@stack`
**Target:** Variabili (array, buffer)

Alloca sullo stack invece che nell'heap (dove possibile).

```hemlock
@stack
let temp_buffer = buffer(1024);  // Allocazione sullo stack
```

#### `@noalias`
**Target:** Parametri di funzione (puntatori/buffer)

Promette che il puntatore non è alias con altri puntatori.

```hemlock
fn memcpy_fast(@noalias dest: ptr, @noalias src: ptr, n: i32) {
    memcpy(dest, src, n);
}
```

#### `@aligned(bytes: number)`
**Target:** Variabili (puntatori, buffer), ritorni di funzione
**Argomenti:** Allineamento in byte (deve essere potenza di 2)

Specifica requisiti di allineamento della memoria.

```hemlock
@aligned(64)  // Allineato alla linea di cache
let cache_line_buffer = buffer(64);
```

### Categoria 3: Controllo della Generazione del Codice

#### `@extern(name?: string, abi?: string)`
**Target:** Funzioni

Segna la funzione per linkage esterno o export FFI.

```hemlock
@extern
fn hemlock_init() {
    print("Libreria inizializzata");
}
```

#### `@section(name: string)`
**Target:** Funzioni, variabili globali

Posiziona il simbolo in una sezione ELF/Mach-O specifica.

```hemlock
@section(".text.hot")
@hot
fn critical_path() { }
```

### Categoria 4: Controllo degli Errori

#### `@bounds_check` / `@no_bounds_check`
**Target:** Operazioni array/buffer, cicli

Sovrascrive la policy globale di controllo dei limiti.

```hemlock
@bounds_check
fn safe_array_access(arr: array, idx: i32) {
    return arr[idx];
}

@no_bounds_check
fn trusted_hot_loop(data: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        data[i] = 0;
    }
}
```

#### `@warn_unused`
**Target:** Valori di ritorno delle funzioni

Avvisa se il chiamante ignora il valore di ritorno.

```hemlock
@warn_unused
fn allocate_memory(size: i32): ptr {
    return alloc(size);
}

let p = allocate_memory(1024);  // OK
allocate_memory(1024);          // Avviso: valore di ritorno non utilizzato
```

### Categoria 5: FFI/Interop

#### `@packed`
**Target:** Definizioni di tipo (define)

Crea struct packed senza padding (per interop C).

```hemlock
@packed
define NetworkHeader {
    magic: u32,
    version: u8,
    flags: u8,
    length: u16
}  // Totale: 8 byte, nessun padding
```

---

## Piano di Implementazione

### Fase 1: Infrastruttura Core (Settimana 1)
**Obiettivo:** Abilitare il compilatore a interrogare e usare le annotazioni

### Fase 2: Annotazioni Funzione (Settimana 2)
**Obiettivo:** Implementare hint di ottimizzazione a livello di funzione

### Fase 3: Annotazioni Ciclo (Settimana 3)
**Obiettivo:** Supportare hint a livello di ciclo (@unroll, @simd, @likely/@unlikely)

### Fase 4: Annotazioni Memoria (Settimana 4)
**Obiettivo:** Implementare @stack, @noalias, @aligned

### Fase 5: Testing e Documentazione (Settimana 5)
**Obiettivo:** Copertura test completa e documentazione

---

## Esempi

### Esempio 1: Matematica Vettoriale ad Alte Prestazioni

```hemlock
@simd
@flatten
fn vector_add(a: buffer, b: buffer, result: buffer, n: i32) {
    @unroll(8)
    for (let i = 0; i < n; i++) {
        let av = ptr_read_f64(a, i * 8);
        let bv = ptr_read_f64(b, i * 8);
        ptr_write_f64(result, i * 8, av + bv);
    }
}
```

### Esempio 2: Struttura Dati Ottimizzata per la Cache

```hemlock
@packed
define CacheLineNode {
    next: ptr,
    data: i64,
    timestamp: u64,
    flags: u32,
    padding: u32
}

@hot
@inline
fn cache_lookup(@aligned(64) cache: ptr, key: u64): ptr {
    @likely
    if (cache == null) {
        return null;
    }
    let node = ptr_read_ptr(cache);
    @unroll(4)
    while (node != null) {
        let node_key = ptr_read_u64(node, 8);
        if (node_key == key) {
            return node;
        }
        node = ptr_read_ptr(node);
    }
    return null;
}
```

### Esempio 3: Ottimizzazione Ricorsione in Coda

```hemlock
@tail_call
fn sum_range(start: i32, end: i32, acc: i32): i32 {
    if (start > end) {
        return acc;
    }
    @tail_call
    return sum_range(start + 1, end, acc + start);
}
```

---

## Strategia di Testing

### 1. Test di Validazione
Test che le nuove annotazioni siano validate correttamente.

### 2. Test di Parità
Assicurarsi che le annotazioni non cambino il comportamento del programma.

### 3. Test Specifici del Compilatore
Verificare che il codice C generato contenga gli attributi/pragma corretti.

### 4. Benchmark di Prestazioni
Misurare i miglioramenti di prestazioni effettivi.

---

## Considerazioni Future

1. **Ereditarietà delle annotazioni** - Le annotazioni sui tipi dovrebbero applicarsi a tutte le istanze?
2. **Composizione delle annotazioni** - Permettere di creare annotazioni personalizzate da altre?
3. **Integrazione con i flag del compilatore** - Le annotazioni dovrebbero sovrascrivere i flag del compilatore?
4. **Integrazione con analisi statica** - Le annotazioni potrebbero alimentare strumenti di analisi statica.
5. **Accesso alle annotazioni a runtime** - Le annotazioni dovrebbero essere interrogabili a runtime?

---

## Tabella di Riferimento Completa delle Annotazioni

| Annotazione | Target | Argomenti | Descrizione | Attributo C |
|-------------|--------|-----------|-------------|-------------|
| `@inline` | fn | 0 | Forza inlining | `always_inline` |
| `@noinline` | fn | 0 | Impedisci inlining | `noinline` |
| `@cold` | fn | 0 | Eseguita raramente | `cold` |
| `@hot` | fn | 0 | Eseguita frequentemente | `hot` |
| `@pure` | fn | 0 | Nessun effetto collaterale, può leggere globali | `pure` |
| `@const` | fn | 0 | Nessun effetto collaterale, nessuna lettura globale | `const` |
| `@flatten` | fn | 0 | Inline tutte le chiamate nella funzione | `flatten` |
| `@tail_call` | fn | 0 | Richiedi ottimizzazione chiamata in coda | Personalizzato |
| `@optimize(level)` | fn | 1 | Sovrascrivere livello ottimizzazione | `optimize("OX")` |
| `@unroll(factor?)` | ciclo | 0-1 | Hint srotolamento ciclo | `#pragma unroll` |
| `@simd` | fn, ciclo | 0 | Abilita vettorizzazione SIMD | `#pragma omp simd` |
| `@nosimd` | fn, ciclo | 0 | Disabilita SIMD | Personalizzato |
| `@likely` | if | 0 | Branch probabilmente preso | `__builtin_expect` |
| `@unlikely` | if | 0 | Branch probabilmente non preso | `__builtin_expect` |
| `@stack` | let | 0 | Allocazione sullo stack | Personalizzato |
| `@noalias` | param | 0 | Nessun aliasing puntatore | `noalias` |
| `@aligned(N)` | let, fn | 1 | Allineamento memoria | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | Linkage esterno | `extern "C"` |
| `@section(name)` | fn, let | 1 | Posiziona in sezione specifica | `section("X")` |
| `@bounds_check` | fn | 0 | Forza controllo limiti | Personalizzato |
| `@no_bounds_check` | fn | 0 | Disabilita controllo limiti | Personalizzato |
| `@warn_unused` | fn | 0 | Avvisa su ritorno non usato | `warn_unused_result` |
| `@packed` | define | 0 | Nessun padding struct | `packed` |
