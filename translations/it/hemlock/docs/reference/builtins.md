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

## Funzioni per i Segnali

### signal

Registra un handler per un segnale.

**Firma:**
```hemlock
signal(sig: i32, handler: function): null
```

**Parametri:**
- `sig` - Numero del segnale
- `handler` - Funzione da chiamare al segnale

**Restituisce:** `null`

**Esempi:**
```hemlock
signal(SIGINT, fn(sig) {
    print("Interrotto!");
    exit(0);
});
```

**Segnali Comuni:**
- `SIGINT` (2) - Interrupt
- `SIGTERM` (15) - Terminazione
- `SIGUSR1` (10) - User-defined 1
- `SIGUSR2` (12) - User-defined 2

---

### raise

Invia un segnale al processo corrente.

**Firma:**
```hemlock
raise(sig: i32): null
```

**Parametri:**
- `sig` - Numero del segnale

**Restituisce:** `null`

**Esempi:**
```hemlock
raise(SIGUSR1);
```

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

## Costanti

### Costanti Booleane

| Costante | Tipo   | Valore |
|----------|--------|--------|
| `true`   | `bool` | Vero   |
| `false`  | `bool` | Falso  |
| `null`   | `null` | Nessun valore |

### Costanti dei Segnali

| Costante   | Valore | Descrizione     |
|------------|--------|-----------------|
| `SIGINT`   | 2      | Interrupt       |
| `SIGTERM`  | 15     | Terminazione    |
| `SIGUSR1`  | 10     | User-defined 1  |
| `SIGUSR2`  | 12     | User-defined 2  |

---

## Riepilogo Completo delle Funzioni

### I/O

| Funzione    | Descrizione                    |
|-------------|--------------------------------|
| `print`     | Stampa su stdout               |
| `eprint`    | Stampa su stderr               |
| `read_line` | Legge riga da stdin            |
| `open`      | Apre file                      |

### Memoria

| Funzione  | Descrizione                    |
|-----------|--------------------------------|
| `alloc`   | Alloca memoria grezza          |
| `buffer`  | Alloca buffer sicuro           |
| `free`    | Libera memoria                 |
| `realloc` | Ridimensiona memoria           |
| `memset`  | Riempie memoria                |
| `memcpy`  | Copia memoria                  |
| `sizeof`  | Dimensione tipo                |
| `talloc`  | Alloca array tipizzato         |

### Tipi

| Funzione | Descrizione                    |
|----------|--------------------------------|
| `typeof` | Ottiene nome tipo              |
| `len`    | Ottiene lunghezza              |

### Asserzione

| Funzione | Descrizione                    |
|----------|--------------------------------|
| `assert` | Verifica condizione            |
| `panic`  | Termina con errore             |

### Concorrenza

| Funzione  | Descrizione                    |
|-----------|--------------------------------|
| `spawn`   | Crea task                      |
| `join`    | Attende task                   |
| `detach`  | Detach task                    |
| `channel` | Crea canale                    |

### Sistema

| Funzione  | Descrizione                    |
|-----------|--------------------------------|
| `exec`    | Esegue comando                 |
| `sleep`   | Pausa esecuzione               |
| `exit`    | Termina programma              |
| `time_ms` | Ottiene tempo                  |

### Segnali

| Funzione | Descrizione                    |
|----------|--------------------------------|
| `signal` | Registra handler               |
| `raise`  | Invia segnale                  |

### FFI

| Funzione  | Descrizione                    |
|-----------|--------------------------------|
| `dlopen`  | Apre libreria                  |
| `dlsym`   | Ottiene simbolo                |
| `dlcall`  | Chiama funzione                |
| `dlclose` | Chiude libreria                |

---

## Vedi Anche

- [API della Memoria](memory-api.md) - Dettagli gestione memoria
- [API dei File](file-api.md) - Dettagli I/O su file
- [API di Concorrenza](concurrency-api.md) - Dettagli threading
- [Sistema di Tipi](type-system.md) - Informazioni sui tipi
