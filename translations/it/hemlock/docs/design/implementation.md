# Dettagli di Implementazione di Hemlock

Questo documento descrive l'implementazione tecnica del linguaggio Hemlock, inclusa la struttura del progetto, la pipeline di compilazione, l'architettura del runtime e le decisioni di progettazione.

---

## Sommario

- [Struttura del Progetto](#struttura-del-progetto)
- [Pipeline di Compilazione](#pipeline-di-compilazione)
- [Design Modulare dell'Interprete](#design-modulare-dellinterprete)
- [Architettura del Runtime](#architettura-del-runtime)
- [Rappresentazione dei Valori](#rappresentazione-dei-valori)
- [Implementazione del Sistema di Tipi](#implementazione-del-sistema-di-tipi)
- [Gestione della Memoria](#gestione-della-memoria)
- [Modello di Concorrenza](#modello-di-concorrenza)
- [Piani Futuri](#piani-futuri)

---

## Struttura del Progetto

```
hemlock/
├── src/
│   ├── frontend/              # Condiviso: lexer, parser, AST
│   │   ├── lexer.c            # Tokenizzazione
│   │   ├── parser/            # Parser a discesa ricorsiva
│   │   ├── ast.c              # Gestione nodi AST
│   │   └── module.c           # Risoluzione moduli
│   ├── backends/
│   │   ├── interpreter/       # hemlock: interprete tree-walking
│   │   │   ├── main.c         # Entry point CLI
│   │   │   ├── runtime.c      # Valutazione espressioni/istruzioni
│   │   │   ├── builtins.c     # Funzioni integrate
│   │   │   └── ...
│   │   └── compiler/          # hemlockc: generatore codice C
│   │       ├── main.c         # CLI, orchestrazione
│   │       ├── type_check.c   # Controllo tipi compile-time
│   │       ├── codegen.c      # Contesto generazione codice
│   │       ├── codegen_expr.c # Generazione espressioni
│   │       ├── codegen_stmt.c # Generazione istruzioni
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # Language Server Protocol
│   │   └── bundler/           # Strumenti bundle/package
├── runtime/                   # libhemlock_runtime.a (per programmi compilati)
├── stdlib/                    # Libreria standard (39 moduli)
│   └── docs/                  # Documentazione moduli
├── tests/
│   ├── parity/                # Test che devono passare entrambi i backend
│   ├── interpreter/           # Test specifici interprete
│   └── compiler/              # Test specifici compilatore
├── examples/                  # Programmi di esempio
└── docs/                      # Documentazione
```

### Organizzazione delle Directory

**`include/`** - Header API pubblici che definiscono l'interfaccia tra i componenti:
- Separazione pulita tra lexer, parser, AST e interprete
- Dichiarazioni forward per minimizzare le dipendenze
- API pubblica per incorporare Hemlock in altri programmi

**`src/`** - File di implementazione:
- I file di livello superiore gestiscono lexing, parsing, gestione AST
- `main.c` fornisce CLI e REPL
- L'interprete è modularizzato in sottosistemi separati

**`src/interpreter/`** - Implementazione modulare dell'interprete:
- Ogni modulo ha una singola, chiara responsabilità
- API interna definita in `internal.h` per comunicazione inter-modulo
- I moduli possono essere compilati indipendentemente per build più veloci

**`tests/`** - Suite di test completa:
- Organizzata per area funzionale
- Ogni directory contiene casi di test focalizzati
- `run_tests.sh` orchestra l'esecuzione dei test

---

## Pipeline di Compilazione

Hemlock usa una pipeline di compilazione tradizionale con fasi distinte:

### Fase 1: Analisi Lessicale (Lexer)

**Input:** Testo del codice sorgente
**Output:** Stream di token
**Implementazione:** `src/lexer.c`

```
Sorgente: "let x = 42;"
   ↓
Token: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**Caratteristiche principali:**
- Riconosce parole chiave, identificatori, letterali, operatori, punteggiatura
- Gestisce letterali stringa UTF-8 e letterali rune
- Riporta numeri di riga per messaggi di errore
- Passata singola, nessun backtracking

### Fase 2: Analisi Sintattica (Parser)

**Input:** Stream di token
**Output:** Abstract Syntax Tree (AST)
**Implementazione:** `src/parser.c`

```
Token: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST: LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**Caratteristiche principali:**
- Parser a discesa ricorsiva
- Costruisce rappresentazione ad albero della struttura del programma
- Gestisce la precedenza degli operatori
- Valida la sintassi (parentesi, punti e virgola, ecc.)
- Nessuna analisi semantica ancora (fatta a runtime)

**Precedenza Operatori (dalla più bassa alla più alta):**
1. Assegnazione: `=`
2. OR logico: `||`
3. AND logico: `&&`
4. OR bit a bit: `|`
5. XOR bit a bit: `^`
6. AND bit a bit: `&`
7. Uguaglianza: `==`, `!=`
8. Confronto: `<`, `>`, `<=`, `>=`
9. Shift bit a bit: `<<`, `>>`
10. Addizione/Sottrazione: `+`, `-`
11. Moltiplicazione/Divisione/Modulo: `*`, `/`, `%`
12. Unario: `!`, `-`, `~`
13. Chiamata/Indice/Membro: `()`, `[]`, `.`

### Fase 3a: Interpretazione (Tree-Walking)

**Input:** AST
**Output:** Esecuzione del programma
**Implementazione:** `src/backends/interpreter/runtime.c`

```
AST: LetStmt { ... }
   ↓
Esecuzione: Valuta nodi AST ricorsivamente
   ↓
Risultato: Variabile x creata con valore 42
```

**Caratteristiche principali:**
- Attraversamento diretto dell'AST (interprete tree-walking)
- Controllo dinamico dei tipi a runtime
- Storage delle variabili basato su environment

### Fase 3b: Compilazione (hemlockc)

**Input:** AST
**Output:** Eseguibile nativo via generazione codice C
**Implementazione:** `src/backends/compiler/`

```
AST: LetStmt { ... }
   ↓
Controllo Tipi: Valida tipi a compile-time
   ↓
Codegen C: Genera codice C equivalente
   ↓
GCC: Compila C in binario nativo
   ↓
Risultato: Eseguibile standalone
```

**Caratteristiche principali:**
- Controllo tipi a compile-time (abilitato di default)
- Generazione codice C per portabilità
- Linka contro `libhemlock_runtime.a`
- Esecuzione significativamente più veloce dell'interprete

---

## Backend Compilatore (hemlockc)

Il compilatore Hemlock genera codice C dall'AST, che viene poi compilato in un eseguibile nativo usando GCC.

### Architettura del Compilatore

```
src/backends/compiler/
├── main.c              # CLI, parsing argomenti, orchestrazione
├── codegen.c           # Contesto core generazione codice
├── codegen_expr.c      # Generazione codice espressioni
├── codegen_stmt.c      # Generazione codice istruzioni
├── codegen_call.c      # Generazione chiamate funzione
├── codegen_closure.c   # Implementazione closure
├── codegen_program.c   # Generazione programma top-level
├── codegen_module.c    # Gestione moduli/import
├── type_check.c        # Controllo tipi compile-time
└── type_check.h        # API controllo tipi
```

### Controllo dei Tipi

Il compilatore include un sistema unificato di controllo dei tipi che:

1. **Valida i tipi a compile-time** - Cattura errori di tipo prima dell'esecuzione
2. **Supporta codice dinamico** - Codice non tipizzato trattato come `any` (sempre valido)
3. **Fornisce hint di ottimizzazione** - Identifica variabili che possono essere unboxed

**Flag Controllo Tipi:**

| Flag | Descrizione |
|------|-------------|
| (default) | Controllo tipi abilitato |
| `--check` | Solo controllo tipi, non compila |
| `--no-type-check` | Disabilita controllo tipi |
| `--strict-types` | Avvisa su tipi `any` impliciti |

**Implementazione Controllo Tipi:**

```c
// type_check.h - Strutture chiave
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // Hint ottimizzazione
    // ... type environment, definizioni, ecc.
} TypeCheckContext;

// Entry point principale
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### Generazione del Codice

La fase di codegen traduce i nodi AST in codice C:

**Mapping Espressioni:**
```
Hemlock                 →  C Generato
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  Closure con cattura environment
```

**Integrazione Runtime:**

Il codice C generato linka contro `libhemlock_runtime.a` che fornisce:
- Tipo union taggata `HmlValue`
- Gestione memoria (reference counting)
- Funzioni integrate (print, typeof, ecc.)
- Primitive di concorrenza (task, canali)
- Supporto FFI

### Ottimizzazione Unboxing

Il controllo tipi identifica variabili che possono usare tipi C nativi invece di `HmlValue` boxed:

**Pattern Unboxable:**
- Contatori di loop con tipo intero noto
- Variabili accumulatore nei loop
- Variabili con annotazioni di tipo esplicite (i32, i64, f64, bool)

```hemlock
// Il contatore loop 'i' può essere unboxed a int32_t nativo
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    somma = somma + i;
}
```

---

## Design Modulare dell'Interprete

L'interprete è diviso in moduli focalizzati per manutenibilità e scalabilità.

### Responsabilità dei Moduli

#### 1. Environment (`environment.c`) - 121 righe

**Scopo:** Scoping delle variabili e risoluzione dei nomi

**Funzioni chiave:**
- `env_create()` - Crea nuovo environment con parent opzionale
- `env_define()` - Definisce nuova variabile nello scope corrente
- `env_get()` - Cerca variabile nello scope corrente o parent
- `env_set()` - Aggiorna valore variabile esistente
- `env_free()` - Libera environment e tutte le variabili

**Design:**
- Scope collegati (ogni environment ha puntatore al parent)
- HashMap per lookup veloce delle variabili
- Supporta scoping lessicale per le closure

#### 2. Values (`values.c`) - 394 righe

**Scopo:** Costruttori di valori e gestione strutture dati

**Funzioni chiave:**
- `value_create_*()` - Costruttori per ogni tipo di valore
- `value_copy()` - Logica di copia deep/shallow
- `value_free()` - Pulizia e deallocazione memoria
- `value_to_string()` - Rappresentazione stringa per stampa

**Strutture dati:**
- Oggetti (array campi dinamici)
- Array (ridimensionamento dinamico)
- Buffer (ptr + length + capacity)
- Closure (funzione + environment catturato)
- Task e Channel (primitive di concorrenza)

#### 3. Types (`types.c`) - 440 righe

**Scopo:** Sistema tipi, conversioni e duck typing

**Funzioni chiave:**
- `type_check()` - Validazione tipi runtime
- `type_convert()` - Conversioni/promozioni implicite
- `duck_type_check()` - Controllo tipi strutturale per oggetti
- `type_name()` - Ottiene nome tipo stampabile

**Caratteristiche:**
- Gerarchia promozione tipi (i8 → i16 → i32 → i64 → f32 → f64, con i64/u64 + f32 → f64)
- Controllo intervallo per tipi numerici
- Duck typing per definizioni tipo oggetto
- Default campi opzionali

#### 4. Builtins (`builtins.c`) - 955 righe

**Scopo:** Funzioni integrate e registrazione globale

**Funzioni chiave:**
- `register_builtins()` - Registra tutte le funzioni e costanti integrate
- Implementazioni funzioni integrate (print, typeof, alloc, free, ecc.)
- Funzioni gestione segnali
- Esecuzione comandi (exec)

**Categorie di builtin:**
- I/O: print, open, read_file, write_file
- Memoria: alloc, free, memset, memcpy, realloc
- Tipi: typeof, assert
- Concorrenza: spawn, join, detach, channel
- Sistema: exec, signal, raise, panic
- FFI: dlopen, dlsym, dlcall, dlclose

#### 5. I/O (`io.c`) - 449 righe

**Scopo:** I/O su file e serializzazione JSON

**Funzioni chiave:**
- Metodi oggetto file (read, write, seek, tell, close)
- Serializzazione/deserializzazione JSON
- Rilevamento riferimenti circolari

**Caratteristiche:**
- Oggetto file con proprietà (path, mode, closed)
- I/O testo consapevole UTF-8
- Supporto I/O binario
- Round-tripping JSON per oggetti e array

#### 6. FFI (`ffi.c`) - Foreign Function Interface

**Scopo:** Chiamare funzioni C da librerie condivise

**Funzioni chiave:**
- `dlopen()` - Carica libreria condivisa
- `dlsym()` - Ottiene puntatore funzione per nome
- `dlcall()` - Chiama funzione C con conversione tipi
- `dlclose()` - Scarica libreria

**Caratteristiche:**
- Integrazione con libffi per chiamate funzione dinamiche
- Conversione tipi automatica (Hemlock ↔ tipi C)
- Supporto per tutti i tipi primitivi
- Supporto puntatori e buffer

#### 7. Runtime (`runtime.c`) - 865 righe

**Scopo:** Valutazione espressioni ed esecuzione istruzioni

**Funzioni chiave:**
- `eval_expr()` - Valuta espressioni (ricorsivo)
- `eval_stmt()` - Esegue istruzioni
- Gestione flusso di controllo (if, while, for, switch, ecc.)
- Gestione eccezioni (try/catch/finally/throw)

**Caratteristiche:**
- Valutazione espressioni ricorsiva
- Valutazione booleana cortocircuito
- Rilevamento chiamate metodo e binding `self`
- Propagazione eccezioni
- Gestione break/continue/return

### Benefici del Design Modulare

**1. Separazione delle Responsabilità**
- Ogni modulo ha una chiara responsabilità
- Facile trovare dove sono implementate le funzionalità
- Riduce il carico cognitivo quando si fanno modifiche

**2. Build Incrementali Più Veloci**
- Solo i moduli modificati necessitano ricompilazione
- Compilazione parallela possibile
- Tempi di iterazione più brevi durante lo sviluppo

**3. Testing e Debug Più Facili**
- I moduli possono essere testati in isolamento
- I bug sono localizzati in sottosistemi specifici
- Implementazioni mock possibili per testing

**4. Scalabilità**
- Nuove funzionalità possono essere aggiunte ai moduli appropriati
- I moduli possono essere refactorizzati indipendentemente
- La dimensione del codice per file rimane gestibile

**5. Organizzazione del Codice**
- Raggruppamento logico di funzionalità correlate
- Grafo delle dipendenze chiaro
- Onboarding più facile per nuovi contributori

---

## Architettura del Runtime

### Rappresentazione dei Valori

Tutti i valori in Hemlock sono rappresentati dalla struct `Value` usando una union taggata:

```c
typedef struct Value {
    ValueType type;  // Tag tipo runtime
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**Decisioni di design:**
- **Union taggata** per type safety mantenendo flessibilità
- **Tag tipo runtime** abilitano tipizzazione dinamica con controllo tipi
- **Storage valore diretto** per primitivi (no boxing)
- **Storage puntatore** per tipi allocati nell'heap (stringhe, oggetti, array)

### Esempi Layout Memoria

**Intero (i32):**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- Dimensione totale: ~16 byte (8-byte tag + 8-byte union)
- Allocato sullo stack
- Nessuna allocazione heap necessaria

**Stringa:**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // Puntatore a heap
}

Heap: "ciao\0" (6 byte, null-terminated UTF-8)
```
- Value è 16 byte sullo stack
- Dati stringa allocati nell'heap
- Deve essere liberata manualmente

**Oggetto:**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // Puntatore a heap
}

Heap: Object {
    type_name: "Persona",
    fields: [
        { name: "nome", value: Value{TYPE_STRING, "Alice"} },
        { name: "eta", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- Struttura oggetto nell'heap
- Campi memorizzati in array dinamico
- Valori campi sono struct Value embedded

### Implementazione Environment

Le variabili sono memorizzate in catene di environment:

```c
typedef struct Environment {
    HashMap *bindings;           // nome → Value
    struct Environment *parent;  // Scope parent lessicale
} Environment;
```

**Esempio catena scope:**
```
Scope Globale: { print: <builtin>, args: <array> }
    ↑
Scope Funzione: { x: 10, y: 20 }
    ↑
Scope Blocco: { i: 0 }
```

**Algoritmo di lookup:**
1. Controlla hashmap dell'environment corrente
2. Se non trovato, controlla environment parent
3. Ripeti finché trovato o raggiunto scope globale
4. Errore se non trovato in nessuno scope

---

## Implementazione del Sistema di Tipi

### Strategia Controllo Tipi

Hemlock usa **controllo tipi runtime** con **annotazioni tipo opzionali**:

```hemlock
let x = 42;           // Nessun controllo tipo, inferisce i32
let y: u8 = 255;      // Controllo runtime: valore deve stare in u8
let z: i32 = x + y;   // Controllo runtime + promozione tipo
```

**Flusso implementazione:**
1. **Inferenza letterali** - Lexer/parser determinano tipo iniziale dal letterale
2. **Controllo annotazione tipo** - Se annotazione presente, valida all'assegnazione
3. **Promozione** - Operazioni binarie promuovono a tipo comune
4. **Conversione** - Conversioni esplicite avvengono su richiesta

### Implementazione Promozione Tipi

La promozione tipi segue una gerarchia fissa con preservazione precisione:

```c
// Logica promozione semplificata
ValueType promote_types(ValueType a, ValueType b) {
    // f64 vince sempre
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 con i64/u64 promuove a f64 (preservazione precisione)
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // Tipi interi più grandi vincono
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**Rank dei tipi:**
- i8: 0
- u8: 1
- i16: 2
- u16: 3
- i32: 4
- u32: 5
- i64: 6
- u64: 7
- f32: 8
- f64: 9

### Implementazione Duck Typing

Il controllo tipo degli oggetti usa confronto strutturale:

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // Controlla tutti i campi richiesti
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // Campo mancante
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // Tipo sbagliato
        }
    }

    return true;  // Tutti i campi richiesti presenti e tipo corretto
}
```

**Il duck typing permette:**
- Campi extra negli oggetti (ignorati)
- Tipizzazione sub-strutturale (oggetto può avere più del richiesto)
- Assegnazione nome tipo dopo validazione

---

## Gestione della Memoria

### Strategia di Allocazione

Hemlock usa **gestione manuale della memoria** con due primitive di allocazione:

**1. Puntatori grezzi (`ptr`):**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Memoria esaurita\n");
        exit(1);
    }
    return ptr;
}
```
- malloc/free diretti
- Nessun tracking
- Responsabilità utente liberare

**2. Buffer (`buffer`):**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- Traccia dimensione e capacità
- Controllo limiti sull'accesso
- Richiede comunque free manuale

### Tipi Allocati nell'Heap

**Stringhe:**
- Array byte UTF-8 nell'heap
- Null-terminated per interop C
- Mutabili (possono modificare in loco)
- Refcounted (auto-liberate quando scope esce)

**Oggetti:**
- Array campi dinamico
- Nomi e valori campi nell'heap
- Refcounted (auto-liberati quando scope esce)
- Riferimenti circolari possibili (gestiti con tracking visited-set)

**Array:**
- Crescita capacità dinamica (raddoppio)
- Elementi sono struct Value embedded
- Riallocazione automatica alla crescita
- Refcounted (auto-liberati quando scope esce)

**Closure:**
- Cattura environment per riferimento
- Environment allocato nell'heap
- Environment closure liberati propriamente quando non più referenziati

---

## Modello di Concorrenza

### Architettura Threading

Hemlock usa **threading 1:1** con POSIX threads (pthreads):

```
Task Utente          Thread OS          Core CPU
---------            ---------          --------
spawn(f1) ------->   pthread_create --> Core 0
spawn(f2) ------->   pthread_create --> Core 1
spawn(f3) ------->   pthread_create --> Core 2
```

**Caratteristiche chiave:**
- Ogni `spawn()` crea un nuovo pthread
- Kernel schedula thread sui core
- Vera esecuzione parallela (nessun GIL)
- Multitasking preemptive

### Implementazione Task

```c
typedef struct Task {
    pthread_t thread;        // Handle thread OS
    Value result;            // Valore ritorno
    char *error;             // Messaggio eccezione (se lanciata)
    pthread_mutex_t lock;    // Protegge lo stato
    TaskState state;         // RUNNING, FINISHED, ERROR
} Task;
```

**Ciclo vita task:**
1. `spawn(func, args)` → Crea Task, avvia pthread
2. Thread esegue funzione con argomenti
3. Al ritorno: Memorizza risultato, imposta stato a FINISHED
4. All'eccezione: Memorizza messaggio errore, imposta stato a ERROR
5. `join(task)` → Attende thread, restituisce risultato o lancia eccezione

### Implementazione Channel

```c
typedef struct Channel {
    void **buffer;           // Buffer circolare di Value*
    size_t capacity;         // Elementi massimi bufferizzati
    size_t count;            // Elementi correnti nel buffer
    size_t read_index;       // Prossima posizione lettura
    size_t write_index;      // Prossima posizione scrittura
    bool closed;             // Flag canale chiuso
    pthread_mutex_t lock;    // Protegge buffer
    pthread_cond_t not_full; // Segnala quando spazio disponibile
    pthread_cond_t not_empty;// Segnala quando dati disponibili
} Channel;
```

**Operazione send:**
1. Lock mutex
2. Attendi se buffer pieno (cond_wait su not_full)
3. Scrivi valore a buffer[write_index]
4. Incrementa write_index (circolare)
5. Segnala not_empty
6. Unlock mutex

**Operazione receive:**
1. Lock mutex
2. Attendi se buffer vuoto (cond_wait su not_empty)
3. Leggi valore da buffer[read_index]
4. Incrementa read_index (circolare)
5. Segnala not_full
6. Unlock mutex

**Garanzie di sincronizzazione:**
- send/recv thread-safe (protetti da mutex)
- Semantica bloccante (produttore attende se pieno, consumatore attende se vuoto)
- Consegna ordinata (FIFO all'interno di un canale)

---

## Piani Futuri

### Completato: Backend Compilatore

Il backend compilatore (`hemlockc`) è stato implementato con:
- Generazione codice C da AST
- Controllo tipi compile-time (abilitato di default)
- Libreria runtime (`libhemlock_runtime.a`)
- Parità completa con interprete (98% test pass rate)
- Framework ottimizzazione unboxing

### Focus Corrente: Miglioramenti Sistema Tipi

**Miglioramenti recenti:**
- Sistemi unificati controllo tipi e inferenza tipi
- Controllo tipi compile-time abilitato di default
- Flag `--check` per validazione solo tipi
- Contesto tipi passato a codegen per hint ottimizzazione

### Miglioramenti Futuri

**Potenziali aggiunte:**
- Generics/template
- Pattern matching
- Integrazione LSP per supporto IDE type-aware
- Ottimizzazioni unboxing più aggressive
- Escape analysis per allocazione stack

### Ottimizzazioni a Lungo Termine

**Possibili miglioramenti:**
- Inline caching per chiamate metodo
- Compilazione JIT per hot path
- Scheduler work-stealing per migliore concorrenza
- Ottimizzazione profile-guided

---

## Linee Guida Implementazione

### Aggiungere Nuove Funzionalità

Quando si implementano nuove funzionalità, seguire queste linee guida:

**1. Scegliere il modulo giusto:**
- Nuovi tipi valore → `values.c`
- Conversioni tipo → `types.c`
- Funzioni integrate → `builtins.c`
- Operazioni I/O → `io.c`
- Flusso controllo → `runtime.c`

**2. Aggiornare tutti i layer:**
- Aggiungere tipi nodo AST se necessario (`ast.h`, `ast.c`)
- Aggiungere token lexer se necessario (`lexer.c`)
- Aggiungere regole parser (`parser.c`)
- Implementare comportamento runtime (`runtime.c` o modulo appropriato)
- Aggiungere test (`tests/`)

**3. Mantenere consistenza:**
- Seguire stile codice esistente
- Usare convenzioni naming consistenti
- Documentare API pubblica negli header
- Mantenere messaggi errore chiari e consistenti

**4. Testare approfonditamente:**
- Aggiungere casi test prima di implementare
- Testare percorsi successo ed errore
- Testare casi limite
- Verificare nessun memory leak (valgrind)

### Considerazioni Prestazioni

**Colli di bottiglia attuali:**
- Lookup HashMap per accesso variabili
- Chiamate funzione ricorsive (no TCO)
- Concatenazione stringhe (alloca nuova stringa ogni volta)
- Overhead controllo tipi su ogni operazione

**Opportunità ottimizzazione:**
- Cache posizioni variabili (inline caching)
- Ottimizzazione tail call
- String builder per concatenazione
- Inferenza tipi per saltare controlli runtime

### Suggerimenti Debug

**Strumenti utili:**
- `valgrind` - Rilevamento memory leak
- `gdb` - Debug crash
- Flag `-g` - Simboli debug
- Debug con `printf` - Semplice ma efficace

**Problemi comuni:**
- Segfault → Dereferenziazione puntatore null (controlla valori ritorno)
- Memory leak → Chiamata free() mancante (controlla percorsi value_free)
- Errore tipo → Controlla logica type_convert() e type_check()
- Crash nei thread → Race condition (controlla uso mutex)

---

## Conclusione

L'implementazione di Hemlock priorizza:
- **Modularità** - Chiara separazione responsabilità
- **Semplicità** - Implementazione diretta
- **Esplicitezza** - Nessuna magia nascosta
- **Manutenibilità** - Facile da capire e modificare

L'attuale interprete tree-walking è intenzionalmente semplice per facilitare lo sviluppo rapido di funzionalità e la sperimentazione. Il futuro backend compilatore migliorerà le prestazioni mantenendo la stessa semantica.
