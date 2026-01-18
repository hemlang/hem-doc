# Filosofia di Design del Linguaggio Hemlock

> "Un piccolo linguaggio non sicuro per scrivere cose non sicure in modo sicuro."

Questo documento cattura i principi fondamentali di progettazione per gli assistenti AI che lavorano con Hemlock.
Per documentazione dettagliata, consultare `docs/README.md` e la directory `stdlib/docs/`.

---

## Identità Fondamentale

Hemlock è un **linguaggio di scripting di sistema** con gestione manuale della memoria e controllo esplicito:
- La potenza del C con l'ergonomia dei moderni linguaggi di scripting
- Concorrenza asincrona strutturata integrata
- Nessun comportamento nascosto o magia

**Hemlock NON è:** A memoria sicura, un linguaggio con GC, o nasconde complessità.
**Hemlock È:** Esplicito piuttosto che implicito, educativo, un "livello di scripting C" per lavoro di sistema.

---

## Principi di Design

### 1. Esplicito Piuttosto che Implicito
- Punto e virgola obbligatorio (nessun ASI)
- Gestione manuale della memoria (alloc/free)
- Annotazioni di tipo opzionali ma verificate a runtime

### 2. Dinamico di Default, Tipizzato per Scelta
- Ogni valore ha un tag di tipo a runtime
- I letterali inferiscono i tipi: `42` → i32, `5000000000` → i64, `3.14` → f64
- Annotazioni di tipo opzionali impongono controlli a runtime

### 3. Non Sicuro è una Funzionalità
- Aritmetica dei puntatori permessa (responsabilità dell'utente)
- Nessun controllo dei limiti su `ptr` raw (usare `buffer` per sicurezza)
- Double-free può causare crash

### 4. Concorrenza Strutturata di Prima Classe
- `async`/`await` integrato con parallelismo basato su pthread
- Canali per la comunicazione
- `spawn`/`join`/`detach` per la gestione dei task

### 5. Sintassi Simile al C
- Blocchi `{}` sempre richiesti
- Commenti: `// riga` e `/* blocco */`
- Operatori come il C: `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Incremento/decremento: `++x`, `x++`, `--x`, `x--` (prefisso e postfisso)
- Assegnazione composta: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` restituisce sempre float (usare `divi()` per divisione intera)
- Sintassi dei tipi: `let x: type = value;`

---

## Riferimento Rapido

### Tipi
```
Con segno:   i8, i16, i32, i64
Senza segno: u8, u16, u32, u64
Float:       f32, f64
Altri:       bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Alias:       integer (i32), number (f64), byte (u8)
```

**Promozione dei tipi:** i8 → i16 → i32 → i64 → f32 → f64 (i float vincono sempre, ma i64/u64 + f32 → f64 per preservare la precisione)

### Letterali
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> max i32)
let hex = 0xDEADBEEF;    // letterale esadecimale
let bin = 0b1010;        // letterale binario
let oct = 0o777;         // letterale ottale
let sep = 1_000_000;     // separatori numerici permessi
let pi = 3.14;           // f64
let half = .5;           // f64 (senza zero iniziale)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // escape esadecimali e unicode
let ch = 'A';            // rune
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Conversione di Tipo
```hemlock
// Funzioni costruttore di tipo - parsano stringhe in tipi
let n = i32("42");       // Parsa stringa a i32
let f = f64("3.14");     // Parsa stringa a f64
let b = bool("true");    // Parsa stringa a bool ("true" o "false")

// Tutti i tipi numerici supportati
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// Numeri esadecimali e negativi
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// Anche gli alias di tipo funzionano
let x = integer("100");  // Come i32("100")
let y = number("1.5");   // Come f64("1.5")
let z = byte("200");     // Come u8("200")

// Convertire tra tipi numerici
let big = i64(42);       // i32 a i64
let truncated = i32(3.99); // f64 a i32 (tronca a 3)

// Le annotazioni di tipo validano i tipi (ma non parsano stringhe)
let f: f64 = 100;        // i32 a f64 via annotazione (coercizione numerica OK)
// let n: i32 = "42";    // ERRORE - usare i32("42") per parsare stringhe
```

### Introspezione
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5 (lunghezza stringa in byte)
len([1, 2, 3]);          // 3 (lunghezza array)
```

### Memoria
```hemlock
let p = alloc(64);       // puntatore raw
let b = buffer(64);      // buffer sicuro (controllo limiti)
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // pulizia manuale richiesta
```

### Flusso di Controllo
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // ciclo infinito (più pulito di while(true))
switch (x) { case 1: break; default: break; }  // fall-through stile C
defer cleanup();         // eseguito quando la funzione ritorna

// Etichette di ciclo per break/continue mirati in cicli annidati
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // esce dal ciclo esterno
        if (i == 3) { continue outer; }  // continua il ciclo esterno
    }
}
```

### Pattern Matching
```hemlock
// Espressione match - restituisce un valore
let result = match (value) {
    0 => "zero",                    // Pattern letterale
    1 | 2 | 3 => "piccolo",         // Pattern OR
    n if n < 10 => "medio",         // Espressione guard
    n => "grande: " + n             // Binding di variabile
};

// Pattern di tipo
match (val) {
    n: i32 => "intero",
    s: string => "stringa",
    _ => "altro"                    // Wildcard
}

// Destrutturazione di oggetti
match (point) {
    { x: 0, y: 0 } => "origine",
    { x, y } => "a " + x + "," + y
}

// Destrutturazione di array con rest
match (arr) {
    [] => "vuoto",
    [first, ...rest] => "testa: " + first,
    _ => "altro"
}

// Pattern annidati
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

Vedere `docs/language-guide/pattern-matching.md` per la documentazione completa.

### Operatori di Null Coalescing
```hemlock
// Null coalescing (??) - restituisce sinistra se non-null, altrimenti destra
let name = user.name ?? "Anonimo";
let first = a ?? b ?? c ?? "fallback";

// Assegnazione null coalescing (??=) - assegna solo se null
let config = null;
config ??= { timeout: 30 };    // config è ora { timeout: 30 }
config ??= { timeout: 60 };    // config invariato (non null)

// Funziona con proprietà e indici
obj.field ??= "default";
arr[0] ??= "primo";

// Navigazione sicura (?.) - restituisce null se l'oggetto è null
let city = user?.address?.city;  // null se qualsiasi parte è null
let upper = name?.to_upper();    // chiamata metodo sicura
let item = arr?.[0];             // indicizzazione sicura
```

### Funzioni
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Ciao") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonima/closure

// Funzioni con corpo espressione (sintassi freccia)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // anonima con corpo espressione

// Modificatori di parametro
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // passaggio per riferimento
fn print_all(const items: array) { for (i in items) { print(i); } }  // immutabile
```

### Argomenti Nominati
```hemlock
// Le funzioni possono essere chiamate con argomenti nominati
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " ha " + age + " anni");
}

// Argomenti posizionali (tradizionali)
create_user("Alice", 25, false);

// Argomenti nominati - possono essere in qualsiasi ordine
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Salta parametri opzionali nominando ciò che ti serve
create_user("David", active: false);  // Usa default age=18

// Gli argomenti nominati devono venire dopo quelli posizionali
create_user("Eve", age: 21);          // OK: posizionale poi nominato
// create_user(name: "Bad", 25);      // ERRORE: posizionale dopo nominato
```

**Regole:**
- Gli argomenti nominati usano la sintassi `nome: valore`
- Possono apparire in qualsiasi ordine dopo gli argomenti posizionali
- Gli argomenti posizionali non possono seguire quelli nominati
- Funziona con parametri default/opzionali
- Nomi di parametri sconosciuti causano errori runtime

### Oggetti e Enum
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// Sintassi shorthand per oggetti (stile ES6)
let name = "Alice";
let age = 30;
let person = { name, age };         // equivalente a { name: name, age: age }

// Operatore spread per oggetti
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // copia defaults, sovrascrive size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Tipi Composti (Intersezione/Duck Types)
```hemlock
// Definisci tipi strutturali
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Tipo composto: l'oggetto deve soddisfare TUTTI i tipi
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Parametri di funzione con tipi composti
fn greet(p: HasName & HasAge) {
    print(p.name + " ha " + p.age);
}

// Tre o più tipi
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Campi extra permessi (duck typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - campi extra ignorati
};
```

I tipi composti forniscono comportamento simile alle interfacce senza una parola chiave `interface` separata,
costruendo sui paradigmi `define` e duck typing esistenti.

### Alias di Tipo
```hemlock
// Alias di tipo semplice
type Integer = i32;
type Text = string;

// Alias di tipo funzione
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Alias di tipo composto (ottimo per interfacce riutilizzabili)
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Alias di tipo generico
type Pair<T> = { first: T, second: T };

// Usare alias di tipo
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

Gli alias di tipo creano scorciatoie nominate per tipi complessi, migliorando leggibilità e manutenibilità.

### Tipi di Funzione
```hemlock
// Annotazioni di tipo funzione per parametri
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Funzione di ordine superiore che restituisce una funzione
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tipi di funzione async
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// Tipi di funzione con più parametri
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Parametri Const
```hemlock
// Parametro const - immutabilità profonda
fn print_all(const items: array) {
    // items.push(4);  // ERRORE: non può mutare parametro const
    for (item in items) {
        print(item);
    }
}

// Const con oggetti - nessuna mutazione attraverso alcun percorso
fn describe(const person: object) {
    print(person.name);       // OK: lettura permessa
    // person.name = "Bob";   // ERRORE: non può mutare
}

// Accesso annidato permesso per lettura
fn get_city(const user: object) {
    return user.address.city;  // OK: lettura proprietà annidate
}
```

Il modificatore `const` previene qualsiasi mutazione del parametro, incluse proprietà annidate.
Questo fornisce sicurezza a compile-time per funzioni che non dovrebbero modificare i loro input.

### Parametri Ref (Passaggio per Riferimento)
```hemlock
// Parametro ref - la variabile del chiamante viene modificata direttamente
fn increment(ref x: i32) {
    x = x + 1;  // Modifica la variabile originale
}

let count = 10;
increment(count);
print(count);  // 11 - l'originale è stato modificato

// Classica funzione swap
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// Mescola parametri ref e regolari
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

Il modificatore `ref` passa un riferimento alla variabile del chiamante, permettendo alla funzione di
modificarla direttamente. Senza `ref`, i primitivi sono passati per valore (copiati). Usa `ref` quando
devi mutare lo stato del chiamante senza restituire un valore.

**Regole:**
- I parametri `ref` devono ricevere variabili, non letterali o espressioni
- Funziona con tutti i tipi (primitivi, array, oggetti)
- Combina con annotazioni di tipo: `ref x: i32`
- Non può combinarsi con `const` (sono opposti)

### Firme di Metodo in Define
```hemlock
// Define con firme di metodo (pattern interfaccia)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Firma di metodo richiesta
}

// Gli oggetti devono fornire il metodo richiesto
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Metodi opzionali con ?
define Serializable {
    fn serialize(): string,        // Richiesto
    fn pretty?(): string           // Metodo opzionale
}

// Il tipo Self si riferisce al tipo che definisce
define Cloneable {
    fn clone(): Self   // Restituisce lo stesso tipo dell'oggetto
}
```

Le firme di metodo nei blocchi `define` usano delimitatori virgola (come interfacce TypeScript),
stabilendo contratti che gli oggetti devono soddisfare e abilitando pattern di programmazione
simili alle interfacce con il sistema duck typing di Hemlock.

### Gestione degli Errori
```hemlock
try { throw "errore"; } catch (e) { print(e); } finally { cleanup(); }
panic("irrecuperabile");  // esce immediatamente, non catturabile
```

### Async/Concorrenza
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // oppure join(task)
detach(spawn(background_work));

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**Ownership della memoria:** I task ricevono copie dei valori primitivi ma condividono i puntatori. Se passi un `ptr` a un task spawned, devi assicurarti che la memoria rimanga valida fino al completamento del task. Usa `join()` prima di `free()`, o usa i canali per segnalare il completamento.

### Input Utente
```hemlock
let name = read_line();          // Legge riga da stdin (blocca)
print("Ciao, " + name);
eprint("Messaggio di errore");   // Stampa su stderr

// read_line() restituisce null su EOF
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Ricevuto:", line);
}
```

### I/O su File
```hemlock
let f = open("file.txt", "r");  // modi: r, w, a, r+, w+, a+
let content = f.read();
f.write("data");
f.seek(0);
f.close();
```

### Segnali
```hemlock
signal(SIGINT, fn(sig) { print("Interrotto"); });
raise(SIGUSR1);
```

---

## Metodi Stringa (19)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `to_upper`, `to_lower`,
`starts_with`, `ends_with`, `replace`, `replace_all`, `repeat`, `char_at`,
`byte_at`, `chars`, `bytes`, `to_bytes`, `deserialize`

Template string: `` `Ciao ${name}!` ``

**Mutabilità delle stringhe:** Le stringhe sono mutabili via assegnazione indice (`s[0] = 'H'`), ma tutti i metodi stringa restituiscono nuove stringhe senza modificare l'originale. Questo permette mutazione in-place quando necessario mantenendo il method chaining funzionale.

**Proprietà lunghezza stringa:**
```hemlock
let s = "ciao 🚀";
print(s.length);       // 6 (conteggio caratteri/rune)
print(s.byte_length);  // 9 (conteggio byte - emoji è 4 byte UTF-8)
```

## Metodi Array (18)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`

Array tipizzati: `let nums: array<i32> = [1, 2, 3];`

---

## Libreria Standard (40 moduli)

Importa con prefisso `@stdlib/`:
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| Modulo | Descrizione |
|--------|-------------|
| `arena` | Allocatore di memoria arena (bump allocation) |
| `args` | Parsing argomenti da riga di comando |
| `assert` | Utilità di asserzione |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Operazioni I/O file async |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | Parsing e generazione CSV |
| `datetime` | Classe DateTime, formattazione, parsing |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `fmt` | Utilità di formattazione stringhe |
| `fs` | read_file, write_file, list_dir, exists |
| `glob` | Pattern matching file |
| `hash` | sha256, sha512, md5, djb2 |
| `http` | http_get, http_post, http_request |
| `ipc` | Comunicazione inter-processo |
| `iter` | Utilità iteratore |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger con livelli |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Manipolazione path file |
| `process` | fork, exec, wait, kill |
| `random` | Generazione numeri casuali |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Logica retry con backoff |
| `semver` | Semantic versioning |
| `shell` | Utilità comandi shell |
| `sqlite` | Database SQLite, query, exec, transazioni |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | Colori e stili ANSI |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | Parsing e generazione TOML |
| `url` | Parsing e manipolazione URL |
| `uuid` | Generazione UUID |
| `websocket` | Client WebSocket |

Vedere `stdlib/docs/` per documentazione dettagliata dei moduli.

---

## FFI (Foreign Function Interface)

Dichiara e chiama funzioni C da librerie condivise:
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Ciao!");  // 5
let pid = getpid();
```

Esporta funzioni FFI dai moduli:
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

FFI dinamico (binding runtime):
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Ciao dal C!");
ffi_close(lib);
```

Tipi: `FFI_INT`, `FFI_DOUBLE`, `FFI_POINTER`, `FFI_STRING`, `FFI_VOID`, ecc.

---

## Operazioni Atomiche

Programmazione concorrente lock-free con operazioni atomiche:

```hemlock
// Alloca memoria per i32 atomico
let p = alloc(4);
ptr_write_i32(p, 0);

// Load/store atomici
let val = atomic_load_i32(p);        // Legge atomicamente
atomic_store_i32(p, 42);             // Scrive atomicamente

// Operazioni fetch-and-modify (restituiscono il valore VECCHIO)
let old = atomic_add_i32(p, 10);     // Aggiunge, restituisce vecchio
old = atomic_sub_i32(p, 5);          // Sottrae, restituisce vecchio
old = atomic_and_i32(p, 0xFF);       // AND bit a bit
old = atomic_or_i32(p, 0x10);        // OR bit a bit
old = atomic_xor_i32(p, 0x0F);       // XOR bit a bit

// Compare-and-swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // Se *p == 42, imposta a 100
// Restituisce true se lo swap ha successo, false altrimenti

// Atomic exchange
old = atomic_exchange_i32(p, 999);   // Scambia, restituisce vecchio

free(p);

// Varianti i64 disponibili (atomic_load_i64, atomic_add_i64, ecc.)

// Memory fence (barriera completa)
atomic_fence();
```

Tutte le operazioni usano sequential consistency (`memory_order_seq_cst`).

---

## Struttura del Progetto

```
hemlock/
├── src/
│   ├── frontend/         # Condiviso: lexer, parser, AST, moduli
│   ├── backends/
│   │   ├── interpreter/  # hemlock: interprete tree-walking
│   │   └── compiler/     # hemlockc: generatore codice C
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # Strumenti bundle/package
├── runtime/              # Runtime programmi compilati (libhemlock_runtime.a)
├── stdlib/               # Libreria standard (40 moduli)
│   └── docs/             # Documentazione moduli
├── docs/                 # Documentazione completa
│   ├── language-guide/   # Tipi, stringhe, array, ecc.
│   ├── reference/        # Riferimenti API
│   └── advanced/         # Async, FFI, segnali, ecc.
├── tests/                # 625+ test
└── examples/             # Programmi esempio
```

---

## Linee Guida per lo Stile del Codice

### Costanti e Numeri Magici

Quando aggiungi costanti numeriche al codebase C, segui queste linee guida:

1. **Definisci le costanti in `include/hemlock_limits.h`** - Questo file è la posizione centrale per tutti i limiti compile-time e runtime, capacità e costanti nominate.

2. **Usa nomi descrittivi con prefisso `HML_`** - Tutte le costanti dovrebbero avere prefisso `HML_` per chiarezza del namespace.

3. **Evita numeri magici** - Sostituisci valori numerici hard-coded con costanti nominate. Esempi:
   - Limiti range tipo: `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Capacità buffer: `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Conversioni tempo: `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Seed hash: `HML_DJB2_HASH_SEED`
   - Valori ASCII: `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Includi `hemlock_limits.h`** - I file sorgente dovrebbero includere questo header (spesso via `internal.h`) per accedere alle costanti.

5. **Documenta lo scopo** - Aggiungi un commento che spiega cosa rappresenta ogni costante.

---

## Cosa NON Fare

❌ Aggiungere comportamento implicito (ASI, GC, auto-cleanup)
❌ Nascondere complessità (ottimizzazioni magiche, refcount nascosti)
❌ Rompere semantica esistente (punto e virgola, memoria manuale, stringhe mutabili)
❌ Perdere precisione in conversioni implicite
❌ Usare numeri magici - definisci costanti nominate in `hemlock_limits.h` invece

---

## Testing

```bash
make test              # Esegui test interprete
make test-compiler     # Esegui test compilatore
make parity            # Esegui test parità (entrambi devono corrispondere)
make test-all          # Esegui tutte le suite di test
```

**Importante:** I test potrebbero bloccarsi per problemi async/concorrenza. Usa sempre un timeout quando esegui i test:
```bash
timeout 60 make test   # 60 secondi timeout
timeout 120 make parity
```

Categorie test: primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Architettura Compilatore/Interprete

Hemlock ha due backend di esecuzione che condividono un frontend comune:

```
Sorgente (.hml)
    ↓
┌─────────────────────────────┐
│  FRONTEND CONDIVISO         │
│  - Lexer (src/frontend/)    │
│  - Parser (src/frontend/)   │
│  - AST (src/frontend/)      │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ INTERPRETE │    │ COMPILATORE│
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ Tree-walk  │    │ Type check │
│ evaluation │    │ AST → C    │
│            │    │ gcc link   │
└────────────┘    └────────────┘
```

### Type Checking del Compilatore

Il compilatore (`hemlockc`) include type checking compile-time, **abilitato di default**:

```bash
hemlockc program.hml -o program    # Type check, poi compila
hemlockc --check program.hml       # Solo type check, non compila
hemlockc --no-type-check prog.hml  # Disabilita type checking
hemlockc --strict-types prog.hml   # Avvisa su tipi 'any' impliciti
```

Il type checker:
- Valida le annotazioni di tipo a compile time
- Tratta il codice non tipizzato come dinamico (tipo `any`) - sempre valido
- Fornisce hint di ottimizzazione per unboxing
- Usa conversioni numeriche permissive (range validato a runtime)

### Struttura Directory

```
hemlock/
├── src/
│   ├── frontend/           # Condiviso: lexer, parser, AST, moduli
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock: interprete tree-walking
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc: generatore codice C
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # Language server
│   │   └── bundler/        # Strumenti bundle/package
├── runtime/                # libhemlock_runtime.a per programmi compilati
├── stdlib/                 # Libreria standard condivisa
└── tests/
    ├── parity/             # Test che DEVONO passare entrambi i backend
    ├── interpreter/        # Test specifici interprete
    └── compiler/           # Test specifici compilatore
```

---

## Sviluppo Parity-First

**Sia l'interprete che il compilatore devono produrre output identico per lo stesso input.**

### Policy di Sviluppo

Quando aggiungi o modifichi funzionalità del linguaggio:

1. **Design** - Definisci il cambiamento AST/semantico nel frontend condiviso
2. **Implementa interprete** - Aggiungi valutazione tree-walking
3. **Implementa compilatore** - Aggiungi generazione codice C
4. **Aggiungi test parità** - Scrivi test in `tests/parity/` con file `.expected`
5. **Verifica** - Esegui `make parity` prima di merge

### Struttura Test Parità

```
tests/parity/
├── language/       # Funzionalità core linguaggio (control flow, closure, ecc.)
├── builtins/       # Funzioni integrate (print, typeof, memory, ecc.)
├── methods/        # Metodi stringa e array
└── modules/        # Import/export, import stdlib
```

Ogni test ha due file:
- `feature.hml` - Il programma di test
- `feature.expected` - Output atteso (deve corrispondere per entrambi i backend)

### Risultati Test Parità

| Stato | Significato |
|-------|-------------|
| `✓ PASSED` | Sia interprete che compilatore corrispondono all'output atteso |
| `◐ INTERP_ONLY` | Interprete funziona, compilatore fallisce (necessita fix compilatore) |
| `◑ COMPILER_ONLY` | Compilatore funziona, interprete fallisce (raro) |
| `✗ FAILED` | Entrambi falliscono (bug test o implementazione) |

### Cosa Richiede Parità

- Tutti i costrutti del linguaggio (if, while, for, switch, defer, try/catch)
- Tutti gli operatori (aritmetici, bit a bit, logici, confronto)
- Tutte le funzioni integrate (print, typeof, alloc, ecc.)
- Tutti i metodi stringa e array
- Regole di coercizione e promozione tipo
- Messaggi di errore per errori runtime

### Cosa Può Differire

- Caratteristiche di performance
- Dettagli layout memoria
- Formato debug/stack trace
- Errori di compilazione (il compilatore può catturare di più a compile time)

### Aggiungere un Test Parità

```bash
# 1. Crea file test
cat > tests/parity/language/my_feature.hml << 'EOF'
// Descrizione test
let x = some_feature();
print(x);
EOF

# 2. Genera output atteso dall'interprete
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Verifica parità
make parity
```

---

## Versione

**v1.8.1** - Release corrente con:
- **Pattern matching** (espressioni `match`) - Potente destrutturazione e flusso di controllo:
  - Pattern letterali, wildcard e binding variabile
  - Pattern OR (`1 | 2 | 3`)
  - Espressioni guard (`n if n > 0`)
  - Destrutturazione oggetti (`{ x, y }`)
  - Destrutturazione array con rest (`[first, ...rest]`)
  - Pattern tipo (`n: i32`)
  - Parità completa tra interprete e compilatore
- **Annotazioni helper compilatore** - 11 annotazioni di ottimizzazione per controllo GCC/Clang:
  - `@inline`, `@noinline` - controllo inlining funzione
  - `@hot`, `@cold` - hint predizione branch
  - `@pure`, `@const` - annotazioni effetti collaterali
  - `@flatten` - inline tutte le chiamate nella funzione
  - `@optimize(level)` - livello ottimizzazione per funzione ("0", "1", "2", "3", "s", "fast")
  - `@warn_unused` - avvisa su valori ritorno ignorati
  - `@section(name)` - posizionamento sezione ELF custom (es. `@section(".text.hot")`)
- **Funzioni con corpo espressione** (`fn double(x): i32 => x * 2;`) - sintassi concisa per funzioni a singola espressione
- **Istruzioni singola riga** - sintassi `if`, `while`, `for` senza parentesi (es. `if (x > 0) print(x);`)
- **Alias di tipo** (`type Name = Type;`) - scorciatoie nominate per tipi complessi
- **Annotazioni tipo funzione** (`fn(i32): i32`) - tipi funzione di prima classe
- **Parametri const** (`fn(const x: array)`) - immutabilità profonda per parametri
- **Parametri ref** (`fn(ref x: i32)`) - passaggio per riferimento per mutazione diretta chiamante
- **Firme metodo in define** (`fn method(): Type`) - contratti simili a interfacce (delimitati da virgola)
- **Tipo Self** nelle firme metodo - si riferisce al tipo che definisce
- **Keyword loop** (`loop { }`) - cicli infiniti più puliti, sostituisce `while (true)`
- **Etichette ciclo** (`outer: while`) - break/continue mirati per cicli annidati
- **Shorthand oggetti** (`{ name }`) - sintassi proprietà shorthand stile ES6
- **Spread oggetti** (`{ ...obj }`) - copia e unisce campi oggetto
- **Tipi duck composti** (`A & B & C`) - tipi intersezione per typing strutturale
- **Argomenti nominati** per chiamate funzione (`foo(name: "value", age: 30)`)
- **Operatori null coalescing** (`??`, `??=`, `?.`) per gestione null sicura
- **Letterali ottali** (`0o777`, `0O123`)
- **Separatori numerici** (`1_000_000`, `0xFF_FF`, `0b1111_0000`)
- **Commenti blocco** (`/* ... */`)
- **Sequenze escape esadecimali** in stringhe/rune (`\x41` = 'A')
- **Sequenze escape unicode** in stringhe (`\u{1F600}` = 😀)
- **Letterali float senza zero iniziale** (`.5`, `.123`, `.5e2`)
- **Type checking compile-time** in hemlockc (abilitato di default)
- **Integrazione LSP** con type checking per diagnostica real-time
- **Operatori assegnazione composta** (`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`)
- **Operatori incremento/decremento** (`++x`, `x++`, `--x`, `x--`)
- **Fix precisione tipo**: i64/u64 + f32 → f64 per preservare precisione
- Sistema tipi unificato con hint ottimizzazione unboxing
- Sistema tipi completo (i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object, enum, file, task, channel)
- Stringhe UTF-8 con 19 metodi
- Array con 18 metodi inclusi map/filter/reduce
- Gestione memoria manuale con `talloc()` e `sizeof()`
- Async/await con vero parallelismo pthread
- Operazioni atomiche per programmazione concorrente lock-free
- 40 moduli stdlib (+ arena, assert, semver, toml, retry, iter, random, shell)
- FFI per interop C con `export extern fn` per wrapper libreria riutilizzabili
- Supporto struct FFI nel compilatore (passa struct C per valore)
- Helper puntatori FFI (`ptr_null`, `ptr_read_*`, `ptr_write_*`)
- defer, try/catch/finally/throw, panic
- I/O File, gestione segnali, esecuzione comandi
- Gestore pacchetti [hpm](https://github.com/hemlang/hpm) con registry basato su GitHub
- Backend compilatore (generazione codice C) con 100% parità interprete
- Server LSP con go-to-definition e find-references
- Pass ottimizzazione AST e risoluzione variabili per lookup O(1)
- Builtin apply() per chiamate funzione dinamiche
- Canali unbuffered e supporto many-params
- 159 test parità (100% pass rate)

---

## Filosofia

> Ti diamo gli strumenti per essere sicuro (`buffer`, annotazioni tipo, controllo limiti) ma non ti obblighiamo a usarli (`ptr`, memoria manuale, operazioni non sicure).

**Se non sei sicuro se una funzionalità si adatta a Hemlock, chiediti: "Questo dà al programmatore più controllo esplicito, o nasconde qualcosa?"**

Se nasconde, probabilmente non appartiene a Hemlock.
