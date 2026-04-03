# Riferimento delle Funzioni Integrate

Riferimento completo per le funzioni e costanti integrate di Hemlock.

---

## Panoramica

Hemlock fornisce un insieme di funzioni integrate sempre disponibili nel scope globale. Queste funzioni coprono I/O, gestione della memoria, introspezione dei tipi, concorrenza e utilità di sistema.

---

## Funzioni di I/O

### print

Stampa valori sullo standard output.

**Firma:**
```hemlock
print(...valori: any): null
```

**Parametri:**
- `valori` - Uno o più valori da stampare

**Restituisce:** `null`

**Esempi:**
```hemlock
print("Ciao, Mondo!");
print(42);
print("x =", 10, "y =", 20);
print([1, 2, 3]);
print({ nome: "Alice" });
```

**Comportamento:**
- Converte tutti i valori in stringhe
- Separa più valori con spazi
- Aggiunge newline alla fine

---

### write

Stampa un valore sullo standard output senza newline finale.

**Firma:**
```hemlock
write(value: any): null
```

**Parametri:**
- `value` - Un valore da stampare

**Restituisce:** `null`

**Esempi:**
```hemlock
// Costruire l'output su una singola riga
write("hello");
write(" ");
write("world");
print("");  // solo il newline

// Stampare una lista collegata in linea
let parts = [1, 2, 3];
for (let i = 0; i < parts.length; i++) {
    if (i > 0) { write(" -> "); }
    write(parts[i]);
}
print("");  // Output: 1 -> 2 -> 3
```

**Comportamento:**
- Converte il valore in stringa e lo stampa su stdout
- NON aggiunge un newline finale
- Svuota stdout immediatamente
- Usa `print("")` dopo una serie di chiamate `write()` per aggiungere un newline

---

### eprint

Stampa valori sullo standard error.

**Firma:**
```hemlock
eprint(...valori: any): null
```

**Parametri:**
- `valori` - Uno o più valori da stampare

**Restituisce:** `null`

**Esempi:**
```hemlock
eprint("Errore: qualcosa non va");
eprint("Attenzione:", errore_msg);
```

**Comportamento:**
- Identico a `print()` ma scrive su stderr
- Utile per messaggi di errore e diagnostica

---

### read_line

Legge una riga dallo standard input.

**Firma:**
```hemlock
read_line(): string?
```

**Restituisce:** Stringa con la riga di input, o `null` a EOF

**Esempi:**
```hemlock
print("Inserisci il tuo nome:");
let nome = read_line();
print("Ciao,", nome);

// Gestisci EOF
while (true) {
    let riga = read_line();
    if (riga == null) { break; }
    print("Ricevuto:", riga);
}
```

**Comportamento:**
- Si blocca finché non è disponibile input
- Rimuove il newline finale
- Restituisce `null` a fine file

---

### open

Apre un file per lettura/scrittura.

**Firma:**
```hemlock
open(percorso: string, modalita?: string): file
```

**Parametri:**
- `percorso` - Percorso del file
- `modalita` (opzionale) - Modalità di apertura (predefinito: `"r"`)

**Modalità:**
- `"r"` - Lettura
- `"w"` - Scrittura (tronca)
- `"a"` - Append
- `"r+"` - Lettura e scrittura
- `"w+"` - Lettura e scrittura (tronca)
- `"a+"` - Lettura e append

**Restituisce:** Oggetto file

**Esempi:**
```hemlock
let f = open("dati.txt", "r");
let contenuto = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write("Ciao!");
f2.close();
```

**Vedi Anche:** [API dei File](file-api.md)

---

## Funzioni di Memoria

### alloc

Alloca memoria grezza.

**Firma:**
```hemlock
alloc(dimensione: i32): ptr
```

**Parametri:**
- `dimensione` - Numero di byte da allocare

**Restituisce:** Puntatore alla memoria allocata

**Esempi:**
```hemlock
let p = alloc(1024);
memset(p, 0, 1024);
free(p);
```

**Vedi Anche:** [API della Memoria](memory-api.md)

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
buf[0] = 65;
print(buf.length);
free(buf);
```

**Vedi Anche:** [API della Memoria](memory-api.md)

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

**Vedi Anche:** [API della Memoria](memory-api.md)

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

**Restituisce:** Puntatore alla memoria ridimensionata

**Vedi Anche:** [API della Memoria](memory-api.md)

---

### memset

Riempie la memoria con un valore byte.

**Firma:**
```hemlock
memset(ptr: ptr, byte: i32, dimensione: i32): null
```

**Parametri:**
- `ptr` - Puntatore alla memoria
- `byte` - Valore byte (0-255)
- `dimensione` - Numero di byte

**Vedi Anche:** [API della Memoria](memory-api.md)

---

### memcpy

Copia memoria.

**Firma:**
```hemlock
memcpy(dest: ptr, src: ptr, dimensione: i32): null
```

**Parametri:**
- `dest` - Puntatore destinazione
- `src` - Puntatore sorgente
- `dimensione` - Numero di byte da copiare

**Vedi Anche:** [API della Memoria](memory-api.md)

---

### sizeof

Ottiene la dimensione di un tipo in byte.

**Firma:**
```hemlock
sizeof(tipo): i32
```

**Parametri:**
- `tipo` - Identificatore di tipo

**Restituisce:** Dimensione in byte

**Esempi:**
```hemlock
print(sizeof(i32));         // 4
print(sizeof(f64));         // 8
print(sizeof(ptr));         // 8
```

**Vedi Anche:** [API della Memoria](memory-api.md)

---

### talloc

Alloca array tipizzato.

**Firma:**
```hemlock
talloc(tipo, conteggio: i32): ptr
```

**Parametri:**
- `tipo` - Tipo di elemento
- `conteggio` - Numero di elementi

**Restituisce:** Puntatore all'array allocato

**Esempi:**
```hemlock
let arr = talloc(i32, 100);    // 400 byte
free(arr);
```

**Vedi Anche:** [API della Memoria](memory-api.md)

---

## Funzioni di Introspezione dei Tipi

### typeof

Ottiene il nome del tipo come stringa.

**Firma:**
```hemlock
typeof(valore: any): string
```

**Parametri:**
- `valore` - Qualsiasi valore

**Restituisce:** Stringa del nome del tipo

**Esempi:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("ciao"));          // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"
print(typeof(null));            // "null"

define Persona { nome: string }
let p: Persona = { nome: "Alice" };
print(typeof(p));               // "Persona"
```

**Valori Restituiti:**
- Tipi primitivi: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Tipi composti: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Tipi speciali: `"file"`, `"task"`, `"channel"`
- Oggetti tipizzati: Nome del tipo personalizzato

---

### len

Ottiene la lunghezza di una stringa o array.

**Firma:**
```hemlock
len(valore: string | array): i32
```

**Parametri:**
- `valore` - Stringa o array

**Restituisce:** Numero di elementi/caratteri

**Esempi:**
```hemlock
print(len("ciao"));             // 5
print(len([1, 2, 3]));          // 3
print(len([]));                 // 0
```

---

## Funzioni di Asserzione

### assert

Asserisce che una condizione è vera.

**Firma:**
```hemlock
assert(condizione: bool, messaggio?: string): null
```

**Parametri:**
- `condizione` - Condizione da verificare
- `messaggio` (opzionale) - Messaggio di errore se fallisce

**Restituisce:** `null`

**Esempi:**
```hemlock
assert(x > 0);
assert(x > 0, "x deve essere positivo");
assert(utente != null, "utente non trovato");
```

**Comportamento:**
- Non fa nulla se la condizione è vera
- Esce con errore se la condizione è falsa

---

### panic

Termina il programma con messaggio di errore.

**Firma:**
```hemlock
panic(messaggio: string): never
```

**Parametri:**
- `messaggio` - Messaggio di errore

**Restituisce:** Non ritorna mai (termina il programma)

**Esempi:**
```hemlock
if (ptr == null) {
    panic("allocazione fallita");
}

panic("errore irrecuperabile");
```

**Comportamento:**
- Stampa messaggio su stderr
- Esce con codice di stato non-zero
- Non può essere catturato da try/catch

---

## Funzioni di Concorrenza

### spawn

Crea un nuovo task concorrente.

**Firma:**
```hemlock
spawn(func: function, ...args): task
```

**Parametri:**
- `func` - Funzione da eseguire
- `args` - Argomenti per la funzione

**Restituisce:** Handle del task

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

### join

Attende il completamento del task.

**Firma:**
```hemlock
join(t: task): any
```

**Parametri:**
- `t` - Handle del task

**Restituisce:** Risultato del task

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

### detach

Esegue il task in modo indipendente.

**Firma:**
```hemlock
detach(t: task): null
```

**Parametri:**
- `t` - Handle del task

**Restituisce:** `null`

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

### channel

Crea un canale di comunicazione.

**Firma:**
```hemlock
channel(capacita?: i32): channel
```

**Parametri:**
- `capacita` (opzionale) - Dimensione del buffer (predefinito: 0)

**Restituisce:** Nuovo canale

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

## Funzioni di Sistema

### exec

Esegue un comando shell.

**Firma:**
```hemlock
exec(comando: string): { stdout: string, stderr: string, code: i32 }
```

**Parametri:**
- `comando` - Comando da eseguire

**Restituisce:** Oggetto con stdout, stderr e codice di uscita

**Esempi:**
```hemlock
let risultato = exec("ls -la");
print(risultato.stdout);
print(risultato.code);           // 0 se successo

let risultato2 = exec("comando_inesistente");
print(risultato2.stderr);
print(risultato2.code);          // Non-zero se fallimento
```

**Comportamento:**
- Esegue il comando tramite `/bin/sh`
- Cattura solo stdout (stderr va al terminale)
- Si blocca fino al completamento del comando
- Restituisce stringa vuota se nessun output

**Gestione Errori:**
```hemlock
try {
    let r = exec("comando_inesistente");
} catch (e) {
    print("Esecuzione fallita:", e);
}
```

**Avviso di Sicurezza:** Vulnerabile a shell injection. Validare/sanificare sempre l'input utente.

---

### exec_argv

Esegue un comando con array esplicito di argomenti (senza interpretazione shell).

**Firma:**
```hemlock
exec_argv(argv: array): object
```

**Parametri:**
- `argv` - Array di stringhe: `[comando, arg1, arg2, ...]`

**Restituisce:** Oggetto con campi:
- `output` (string) - Stdout del comando
- `exit_code` (i32) - Codice di stato di uscita (0 = successo)

**Esempi:**
```hemlock
// Comando semplice
let result = exec_argv(["ls", "-la"]);
print(result.output);

// Comando con argomenti contenenti spazi (sicuro!)
let r = exec_argv(["grep", "hello world", "file.txt"]);

// Eseguire script con argomenti
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**Differenza da exec:**
```hemlock
// exec() usa la shell - NON SICURO con input utente
exec("ls " + input_utente);  // Rischio shell injection!

// exec_argv() bypassa la shell - SICURO
exec_argv(["ls", input_utente]);  // Nessuna injection possibile
```

**Quando usare:**
- Quando gli argomenti contengono spazi, virgolette o caratteri speciali
- Quando si elabora input utente (sicurezza)
- Quando serve un parsing degli argomenti prevedibile

---

### sleep

Mette in pausa l'esecuzione.

**Firma:**
```hemlock
sleep(ms: i32): null
```

**Parametri:**
- `ms` - Millisecondi di pausa

**Restituisce:** `null`

**Esempi:**
```hemlock
print("Aspetta...");
sleep(1000);                     // 1 secondo
print("Fatto!");
```

---

### exit

Termina il programma con codice di stato.

**Firma:**
```hemlock
exit(codice?: i32): never
```

**Parametri:**
- `codice` (opzionale) - Codice di uscita (predefinito: 0)

**Restituisce:** Non ritorna mai

**Esempi:**
```hemlock
if (errore) {
    exit(1);
}
exit(0);  // Successo
```

---

### time_ms

Ottiene il tempo corrente in millisecondi.

**Firma:**
```hemlock
time_ms(): i64
```

**Restituisce:** Timestamp Unix in millisecondi

**Esempi:**
```hemlock
let inizio = time_ms();
// ... fai lavoro ...
let fine = time_ms();
print("Tempo impiegato:", fine - inizio, "ms");
```

---

## Gestione dei Segnali

### signal

Registra o resetta un handler di segnale.

**Firma:**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**Parametri:**
- `signum` - Numero del segnale (usa costanti come `SIGINT`)
- `handler` - Funzione da chiamare quando il segnale viene ricevuto, o `null` per resettare al default

**Restituisce:** Funzione handler precedente, o `null`

**Esempi:**
```hemlock
fn gestisci_interrupt(sig) {
    print("Catturato SIGINT!");
}

signal(SIGINT, gestisci_interrupt);

// Resetta al default
signal(SIGINT, null);
```

**Firma dell'Handler:**
```hemlock
fn handler(signum: i32) {
    // signum contiene il numero del segnale
}
```

**Vedi Anche:**
- [Costanti dei segnali](#costanti-dei-segnali)
- `raise()`

---

### raise

Invia un segnale al processo corrente.

**Firma:**
```hemlock
raise(signum: i32): null
```

**Parametri:**
- `signum` - Numero del segnale da inviare

**Restituisce:** `null`

**Esempi:**
```hemlock
let contatore = 0;

fn incrementa(sig) {
    contatore = contatore + 1;
}

signal(SIGUSR1, incrementa);

raise(SIGUSR1);
raise(SIGUSR1);
print(contatore);  // 2
```

---

## Variabili Globali

### args

Array degli argomenti della riga di comando.

**Tipo:** `array` di stringhe

**Struttura:**
- `args[0]` - Nome file dello script
- `args[1..n]` - Argomenti della riga di comando

**Esempi:**
```bash
# Comando: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// Itera sugli argomenti
let i = 1;
while (i < args.length) {
    print("Argomento", i, ":", args[i]);
    i = i + 1;
}
```

**Comportamento nel REPL:** Nel REPL, `args.length` è 0 (array vuoto)

---

## Costanti dei Segnali

Costanti POSIX standard dei segnali (valori i32):

### Interrupt e Terminazione

| Costante   | Valore | Descrizione                              |
|------------|--------|------------------------------------------|
| `SIGINT`   | 2      | Interrupt dalla tastiera (Ctrl+C)        |
| `SIGTERM`  | 15     | Richiesta di terminazione                |
| `SIGQUIT`  | 3      | Quit dalla tastiera (Ctrl+\)            |
| `SIGHUP`   | 1      | Hangup rilevato sul terminale            |
| `SIGABRT`  | 6      | Segnale di abort                         |

### Definiti dall'Utente

| Costante   | Valore | Descrizione              |
|------------|--------|--------------------------|
| `SIGUSR1`  | 10     | Segnale definito dall'utente 1 |
| `SIGUSR2`  | 12     | Segnale definito dall'utente 2 |

### Controllo dei Processi

| Costante   | Valore | Descrizione                          |
|------------|--------|--------------------------------------|
| `SIGALRM`  | 14     | Timer dell'allarme                   |
| `SIGCHLD`  | 17     | Cambio di stato processo figlio      |
| `SIGCONT`  | 18     | Continua se fermato                  |
| `SIGSTOP`  | 19     | Ferma processo (non catturabile)     |
| `SIGTSTP`  | 20     | Stop del terminale (Ctrl+Z)          |

### I/O

| Costante   | Valore | Descrizione                            |
|------------|--------|----------------------------------------|
| `SIGPIPE`  | 13     | Pipe interrotto                        |
| `SIGTTIN`  | 21     | Lettura in background dal terminale    |
| `SIGTTOU`  | 22     | Scrittura in background sul terminale  |

**Nota:** `SIGKILL` (9) e `SIGSTOP` (19) non possono essere catturati o ignorati.

---

## Funzioni Matematiche/Aritmetiche

### div

Divisione intera che restituisce un float.

**Firma:**
```hemlock
div(a: number, b: number): f64
```

**Parametri:**
- `a` - Dividendo
- `b` - Divisore

**Restituisce:** Floor di `a / b` come float (f64)

**Esempi:**
```hemlock
let result = div(7, 2);    // 3.0 (non 3.5)
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0 (floor arrotonda verso infinito negativo)
```

**Nota:** In Hemlock, l'operatore `/` restituisce sempre un float. Usa `div()` per la divisione intera quando serve il risultato come float, o `divi()` quando serve un risultato intero.

---

### divi

Divisione intera che restituisce un intero.

**Firma:**
```hemlock
divi(a: number, b: number): i64
```

**Parametri:**
- `a` - Dividendo
- `b` - Divisore

**Restituisce:** Floor di `a / b` come intero (i64)

**Esempi:**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4 (floor arrotonda verso infinito negativo)
```

**Confronto:**
```hemlock
print(7 / 2);      // 3.5 (divisione regolare, sempre float)
print(div(7, 2));  // 3.0 (divisione intera, risultato float)
print(divi(7, 2)); // 3   (divisione intera, risultato intero)
```

---

## Helper per Puntatori FFI

Queste funzioni aiutano a leggere e scrivere valori tipizzati nella memoria grezza, utili per FFI e manipolazione di memoria a basso livello.

### ptr_null

Crea un puntatore nullo.

**Firma:**
```hemlock
ptr_null(): ptr
```

**Restituisce:** Un puntatore nullo

**Esempio:**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Il puntatore è nullo");
}
```

---

### ptr_offset

Calcola l'offset del puntatore (aritmetica dei puntatori).

**Firma:**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**Parametri:**
- `ptr` - Puntatore base
- `index` - Indice dell'elemento
- `element_size` - Dimensione di ogni elemento in byte

**Restituisce:** Puntatore all'elemento all'indice dato

**Esempio:**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### Funzioni di Scrittura Puntatore

Scrivi valori tipizzati nella memoria.

| Funzione | Firma | Restituisce | Descrizione |
|----------|-------|-------------|-------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | Scrive intero con segno a 8 bit |
| `ptr_write_i16` | `(ptr, value)` | `null` | Scrive intero con segno a 16 bit |
| `ptr_write_i32` | `(ptr, value)` | `null` | Scrive intero con segno a 32 bit |
| `ptr_write_i64` | `(ptr, value)` | `null` | Scrive intero con segno a 64 bit |
| `ptr_write_u8` | `(ptr, value)` | `null` | Scrive intero senza segno a 8 bit |
| `ptr_write_u16` | `(ptr, value)` | `null` | Scrive intero senza segno a 16 bit |
| `ptr_write_u32` | `(ptr, value)` | `null` | Scrive intero senza segno a 32 bit |
| `ptr_write_u64` | `(ptr, value)` | `null` | Scrive intero senza segno a 64 bit |
| `ptr_write_f32` | `(ptr, value)` | `null` | Scrive float a 32 bit |
| `ptr_write_f64` | `(ptr, value)` | `null` | Scrive float a 64 bit |
| `ptr_write_ptr` | `(ptr, value)` | `null` | Scrive valore puntatore |

**Esempio:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### Funzioni di Lettura Puntatore

Leggi valori tipizzati dalla memoria.

| Funzione | Firma | Restituisce | Descrizione |
|----------|-------|-------------|-------------|
| `ptr_read_i8` | `(ptr)` | `i8` | Legge intero con segno a 8 bit |
| `ptr_read_i16` | `(ptr)` | `i16` | Legge intero con segno a 16 bit |
| `ptr_read_i32` | `(ptr)` | `i32` | Legge intero con segno a 32 bit |
| `ptr_read_i64` | `(ptr)` | `i64` | Legge intero con segno a 64 bit |
| `ptr_read_u8` | `(ptr)` | `u8` | Legge intero senza segno a 8 bit |
| `ptr_read_u16` | `(ptr)` | `u16` | Legge intero senza segno a 16 bit |
| `ptr_read_u32` | `(ptr)` | `u32` | Legge intero senza segno a 32 bit |
| `ptr_read_u64` | `(ptr)` | `u64` | Legge intero senza segno a 64 bit |
| `ptr_read_f32` | `(ptr)` | `f32` | Legge float a 32 bit |
| `ptr_read_f64` | `(ptr)` | `f64` | Legge float a 64 bit |
| `ptr_read_ptr` | `(ptr)` | `ptr` | Legge valore puntatore |

**Esempio:**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### Conversione Buffer/Puntatore

#### buffer_ptr

Ottiene il puntatore grezzo da un buffer.

**Firma:**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**Esempio:**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// Ora p punta alla stessa memoria di buf
```

#### ptr_to_buffer

Crea un wrapper buffer attorno a un puntatore grezzo.

**Firma:**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**Esempio:**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // Ora ha controllo dei limiti
// Nota: liberare buf libererà la memoria sottostante
```

---

## Funzioni di Concorrenza

Vedi [API di Concorrenza](concurrency-api.md) per il riferimento completo:
- `spawn(fn, args...)` - Crea task
- `join(task)` - Attende task
- `detach(task)` - Detach task
- `channel(capacity)` - Crea canale

### apply

Chiama una funzione dinamicamente con un array di argomenti.

**Firma:**
```hemlock
apply(fn: function, args: array): any
```

**Parametri:**
- `fn` - La funzione da chiamare
- `args` - Array di argomenti da passare alla funzione

**Restituisce:** Il valore di ritorno della funzione chiamata

**Esempi:**
```hemlock
fn add(a, b) {
    return a + b;
}

// Chiama con array di argomenti
let result = apply(add, [2, 3]);
print(result);  // 5

// Dispatch dinamico
let operazioni = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calcola(op: string, args: array) {
    return apply(operazioni[op], args);
}

print(calcola("add", [10, 5]));  // 15
print(calcola("mul", [10, 5]));  // 50
print(calcola("sub", [10, 5]));  // 5
```

**Casi d'Uso:**
- Dispatch dinamico delle funzioni basato su valori runtime
- Chiamata di funzioni con liste di argomenti variabili
- Implementazione di utilità di ordine superiore (map, filter, ecc.)
- Sistemi di plugin/estensione

---

### select

Attende dati da più canali, restituendo quando uno ha dati.

**Firma:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parametri:**
- `channels` - Array di valori canale
- `timeout_ms` (opzionale) - Timeout in millisecondi (-1 o omettere per infinito)

**Restituisce:**
- `{ channel, value }` - Oggetto con il canale che aveva dati e il valore ricevuto
- `null` - Al timeout

**Esempi:**
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

// Attendi il primo messaggio
let result = select([ch1, ch2]);
print(result.value);  // "dal canale 2" (arrivato per primo)

// Con timeout
let result2 = select([ch1, ch2], 1000);  // Attendi fino a 1 secondo
if (result2 == null) {
    print("Timeout - nessun dato ricevuto");
} else {
    print("Ricevuto:", result2.value);
}
```

**Comportamento:**
- Si blocca finché un canale non ha dati o scade il timeout
- Restituisce immediatamente se un canale ha già dati
- Se il canale è chiuso e vuoto, restituisce `{ channel, value: null }`
- Interroga i canali in ordine (il primo pronto vince)

---

## Funzioni FFI

### dlopen

Apre una libreria condivisa.

**Firma:**
```hemlock
dlopen(percorso: string): ptr
```

**Parametri:**
- `percorso` - Percorso alla libreria condivisa

**Restituisce:** Handle alla libreria

---

### dlsym

Ottiene un simbolo da una libreria.

**Firma:**
```hemlock
dlsym(lib: ptr, nome: string): ptr
```

**Parametri:**
- `lib` - Handle alla libreria
- `nome` - Nome del simbolo

**Restituisce:** Puntatore al simbolo

---

### dlcall

Chiama una funzione esterna.

**Firma:**
```hemlock
dlcall(func: ptr, ...args): any
```

**Parametri:**
- `func` - Puntatore alla funzione
- `args` - Argomenti per la funzione

**Restituisce:** Valore di ritorno della funzione

---

### dlclose

Chiude una libreria condivisa.

**Firma:**
```hemlock
dlclose(lib: ptr): null
```

**Parametri:**
- `lib` - Handle alla libreria

**Restituisce:** `null`

---

## Funzioni di Conversione dei Tipi

### i32, i64, f64, bool, ecc.

Converte valori o analizza stringhe.

**Firma:**
```hemlock
i32(valore: any): i32
i64(valore: any): i64
f64(valore: any): f64
bool(valore: any): bool
// ... altri tipi
```

**Parametri:**
- `valore` - Valore da convertire o stringa da analizzare

**Restituisce:** Valore convertito

**Esempi:**
```hemlock
let n = i32("42");              // 42
let f = f64("3.14");            // 3.14
let b = bool("true");           // true

let hex = i32("0xFF");          // 255
let neg = i32("-42");           // -42

// Conversioni tra tipi
let grande = i64(42);           // i32 a i64
let troncato = i32(3.99);       // f64 a i32 (tronca a 3)
```

---

## Tabella Riassuntiva

### Funzioni

| Funzione    | Categoria       | Restituisce  | Descrizione                           |
|-------------|-----------------|--------------|---------------------------------------|
| `print`     | I/O             | `null`       | Stampa su stdout                      |
| `read_line` | I/O             | `string?`    | Legge riga da stdin                   |
| `eprint`    | I/O             | `null`       | Stampa su stderr                      |
| `typeof`    | Tipo            | `string`     | Ottiene nome del tipo                 |
| `exec`      | Comando         | `object`     | Esegue comando shell                  |
| `exec_argv` | Comando         | `object`     | Esegue con array di argomenti         |
| `assert`    | Errore          | `null`       | Verifica condizione o termina         |
| `panic`     | Errore          | `never`      | Errore irrecuperabile (termina)       |
| `signal`    | Segnale         | `function?`  | Registra handler di segnale           |
| `raise`     | Segnale         | `null`       | Invia segnale al processo             |
| `alloc`     | Memoria         | `ptr`        | Alloca memoria grezza                 |
| `talloc`    | Memoria         | `ptr`        | Allocazione tipizzata                 |
| `sizeof`    | Memoria         | `i32`        | Dimensione tipo in byte               |
| `free`      | Memoria         | `null`       | Libera memoria                        |
| `buffer`    | Memoria         | `buffer`     | Alloca buffer sicuro                  |
| `memset`    | Memoria         | `null`       | Riempie memoria                       |
| `memcpy`    | Memoria         | `null`       | Copia memoria                         |
| `realloc`   | Memoria         | `ptr`        | Ridimensiona allocazione              |
| `open`      | I/O File        | `file`       | Apre file                             |
| `spawn`     | Concorrenza     | `task`       | Crea task concorrente                 |
| `join`      | Concorrenza     | `any`        | Attende risultato task                |
| `detach`    | Concorrenza     | `null`       | Detach task                           |
| `channel`   | Concorrenza     | `channel`    | Crea canale di comunicazione          |
| `select`    | Concorrenza     | `object?`    | Attende su più canali                 |
| `apply`     | Funzioni        | `any`        | Chiama funzione con array di argomenti|

### Variabili Globali

| Variabile  | Tipo     | Descrizione                         |
|------------|----------|-------------------------------------|
| `args`     | `array`  | Argomenti della riga di comando     |

### Costanti

| Costante   | Tipo  | Categoria | Valore | Descrizione                     |
|------------|-------|-----------|--------|---------------------------------|
| `SIGINT`   | `i32` | Segnale   | 2      | Interrupt da tastiera           |
| `SIGTERM`  | `i32` | Segnale   | 15     | Richiesta di terminazione       |
| `SIGQUIT`  | `i32` | Segnale   | 3      | Quit da tastiera                |
| `SIGHUP`   | `i32` | Segnale   | 1      | Hangup                          |
| `SIGABRT`  | `i32` | Segnale   | 6      | Abort                           |
| `SIGUSR1`  | `i32` | Segnale   | 10     | Definito dall'utente 1          |
| `SIGUSR2`  | `i32` | Segnale   | 12     | Definito dall'utente 2          |
| `SIGALRM`  | `i32` | Segnale   | 14     | Timer dell'allarme              |
| `SIGCHLD`  | `i32` | Segnale   | 17     | Cambio stato figlio             |
| `SIGCONT`  | `i32` | Segnale   | 18     | Continua                        |
| `SIGSTOP`  | `i32` | Segnale   | 19     | Stop (non catturabile)          |
| `SIGTSTP`  | `i32` | Segnale   | 20     | Stop del terminale              |
| `SIGPIPE`  | `i32` | Segnale   | 13     | Pipe interrotto                 |
| `SIGTTIN`  | `i32` | Segnale   | 21     | Lettura terminale in background |
| `SIGTTOU`  | `i32` | Segnale   | 22     | Scrittura terminale in background|

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Tipi e conversioni
- [API della Memoria](memory-api.md) - Funzioni di allocazione memoria
- [API dei File](file-api.md) - Funzioni I/O su file
- [API di Concorrenza](concurrency-api.md) - Funzioni async/concorrenza
- [API delle Stringhe](string-api.md) - Metodi stringa
- [API degli Array](array-api.md) - Metodi array
