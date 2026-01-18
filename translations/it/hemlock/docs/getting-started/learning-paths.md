# Percorsi di Apprendimento

Obiettivi diversi richiedono conoscenze diverse. Scegli il percorso che corrisponde a ciò che vuoi costruire.

---

## Percorso 1: Script Veloci e Automazione

**Obiettivo:** Scrivere script per automatizzare attività, elaborare file e portare a termine il lavoro.

**Tempo per la produttività:** Veloce - puoi iniziare a scrivere script utili immediatamente.

### Cosa Imparerai

1. **[Avvio Rapido](quick-start.md)** - Il tuo primo programma, sintassi base
2. **[Stringhe](../language-guide/strings.md)** - Elaborazione testo, split, ricerca
3. **[Array](../language-guide/arrays.md)** - Liste, filtraggio, trasformazione dati
4. **[I/O File](../advanced/file-io.md)** - Lettura e scrittura file
5. **[Argomenti Riga Comando](../advanced/command-line-args.md)** - Ottenere input dagli utenti

### Salta Per Ora

- Gestione memoria (automatica per gli script)
- Async/concorrenza (eccessivo per script semplici)
- FFI (necessario solo per interop C)

### Progetto Esempio: Rinominatore File

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// Rinomina tutti i file .txt in .md
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Rinominato: ${file} -> ${new_name}`);
    }
}
```

---

## Percorso 2: Elaborazione e Analisi Dati

**Obiettivo:** Parsare dati, trasformarli, generare report.

**Tempo per la produttività:** Veloce - I metodi stringa e array di Hemlock rendono questo facile.

### Cosa Imparerai

1. **[Avvio Rapido](quick-start.md)** - Basi
2. **[Stringhe](../language-guide/strings.md)** - Parsing, split, formattazione
3. **[Array](../language-guide/arrays.md)** - map, filter, reduce per trasformazione dati
4. **[Oggetti](../language-guide/objects.md)** - Dati strutturati
5. **Libreria Standard:**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - Parsing JSON
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - File CSV
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - Operazioni file

### Progetto Esempio: Analizzatore CSV

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("vendite.csv"));

// Calcola vendite totali
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Vendite totali: €${total}`);

// Trova il top venditore
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Vendita top: ${top.product} - €${top.amount}`);
```

---

## Percorso 3: Programmazione Web e Network

**Obiettivo:** Costruire client HTTP, lavorare con API, creare server.

**Tempo per la produttività:** Medio - richiede comprensione delle basi async.

### Cosa Imparerai

1. **[Avvio Rapido](quick-start.md)** - Basi
2. **[Funzioni](../language-guide/functions.md)** - Callback e closure
3. **[Gestione Errori](../language-guide/error-handling.md)** - try/catch per errori di rete
4. **[Async e Concorrenza](../advanced/async-concurrency.md)** - spawn, await, canali
5. **Libreria Standard:**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - Richieste HTTP
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON per API
   - **[@stdlib/net](../../stdlib/docs/net.md)** - Socket TCP/UDP
   - **[@stdlib/url](../../stdlib/docs/url.md)** - Parsing URL

### Progetto Esempio: Client API

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// Richiesta GET
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}: ${user.email}`);
}

// Richiesta POST
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`Creato utente con ID: ${parse(result.body).id}`);
```

---

## Percorso 4: Programmazione di Sistema

**Obiettivo:** Scrivere codice a basso livello, lavorare con la memoria, interfacciarsi con librerie C.

**Tempo per la produttività:** Più lungo - richiede comprensione della gestione memoria.

### Cosa Imparerai

1. **[Avvio Rapido](quick-start.md)** - Basi
2. **[Tipi](../language-guide/types.md)** - Comprendere i32, u8, ptr, ecc.
3. **[Gestione Memoria](../language-guide/memory.md)** - alloc, free, buffer
4. **[FFI](../advanced/ffi.md)** - Chiamare funzioni C
5. **[Segnali](../advanced/signals.md)** - Gestione segnali

### Concetti Chiave

**Checklist Sicurezza Memoria:**
- [ ] Ogni `alloc()` ha un `free()` corrispondente
- [ ] Usa `buffer()` a meno che tu non abbia bisogno di `ptr` raw
- [ ] Imposta i puntatori a `null` dopo aver liberato
- [ ] Usa `try/finally` per garantire la pulizia

**Mappatura Tipi per FFI:**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long` (64-bit) |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### Progetto Esempio: Pool di Memoria Custom

```hemlock
// Semplice allocatore bump
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool esaurito";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// Usalo
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();    // Riusa tutta la memoria
pool_destroy();  // Pulisci
```

---

## Percorso 5: Programmi Paralleli e Concorrenti

**Obiettivo:** Eseguire codice su più core CPU, costruire applicazioni reattive.

**Tempo per la produttività:** Medio - la sintassi async è diretta, ma ragionare sul parallelismo richiede pratica.

### Cosa Imparerai

1. **[Avvio Rapido](quick-start.md)** - Basi
2. **[Funzioni](../language-guide/functions.md)** - Closure (importanti per async)
3. **[Async e Concorrenza](../advanced/async-concurrency.md)** - Approfondimento completo
4. **[Atomiche](../advanced/atomics.md)** - Programmazione lock-free

### Concetti Chiave

**Modello async di Hemlock:**
- `async fn` - Definisce una funzione che può girare su un altro thread
- `spawn(fn, args...)` - Inizia l'esecuzione, restituisce un handle task
- `join(task)` o `await task` - Aspetta che finisca, ottieni il risultato
- `channel(size)` - Crea una coda per inviare dati tra task

**Importante:** I task ricevono *copie* dei valori. Se passi un puntatore, sei responsabile di assicurarti che la memoria rimanga valida fino al completamento del task.

### Progetto Esempio: Processore File Parallelo

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// Processa tutti i file in parallelo
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// Raccogli risultati
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}: ${count} righe`);
    total_lines = total_lines + count;
}

print(`Totale: ${total_lines} righe`);
```

---

## Cosa Imparare Prima (Qualsiasi Percorso)

Indipendentemente dal tuo obiettivo, inizia con questi fondamentali:

### Settimana 1: Basi Fondamentali
1. **[Avvio Rapido](quick-start.md)** - Scrivi ed esegui il tuo primo programma
2. **[Sintassi](../language-guide/syntax.md)** - Variabili, operatori, flusso di controllo
3. **[Funzioni](../language-guide/functions.md)** - Definisci e chiama funzioni

### Settimana 2: Gestione Dati
4. **[Stringhe](../language-guide/strings.md)** - Manipolazione testo
5. **[Array](../language-guide/arrays.md)** - Collezioni e iterazione
6. **[Oggetti](../language-guide/objects.md)** - Dati strutturati

### Settimana 3: Robustezza
7. **[Gestione Errori](../language-guide/error-handling.md)** - try/catch/throw
8. **[Moduli](../language-guide/modules.md)** - Import/export, uso stdlib

### Poi: Scegli il Tuo Percorso Sopra

---

## Cheat Sheet: Provenienza da Altri Linguaggi

### Da Python

| Python | Hemlock | Note |
|--------|---------|------|
| `x = 42` | `let x = 42;` | Punto e virgola richiesto |
| `def fn():` | `fn name() { }` | Parentesi graffe richieste |
| `if x:` | `if (x) { }` | Parentesi e graffe richieste |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | Cicli for stile C |
| `for item in list:` | `for (item in array) { }` | For-in funziona uguale |
| `list.append(x)` | `array.push(x);` | Nome metodo diverso |
| `len(s)` | `s.length` o `len(s)` | Entrambi funzionano |
| Memoria automatica | Manuale per `ptr` | La maggior parte dei tipi auto-pulizia |

### Da JavaScript

| JavaScript | Hemlock | Note |
|------------|---------|------|
| `let x = 42` | `let x = 42;` | Uguale (punto e virgola richiesto) |
| `const x = 42` | `let x = 42;` | Nessuna keyword const |
| `function fn()` | `fn name() { }` | Keyword diversa |
| `() => x` | `fn() { return x; }` | Nessuna arrow function |
| `async/await` | `async/await` | Stessa sintassi |
| `Promise` | `spawn/join` | Modello diverso |
| GC automatico | Manuale per `ptr` | La maggior parte dei tipi auto-pulizia |

### Da C/C++

| C | Hemlock | Note |
|---|---------|------|
| `int x = 42;` | `let x: i32 = 42;` | Tipo dopo due punti |
| `malloc(n)` | `alloc(n)` | Stesso concetto |
| `free(p)` | `free(p)` | Uguale |
| `char* s = "hi"` | `let s = "hi";` | Le stringhe sono gestite |
| `#include` | `import { } from` | Import moduli |
| Tutto manuale | Auto per la maggior parte dei tipi | Solo `ptr` richiede manuale |

---

## Ottenere Aiuto

- **[Glossario](../glossary.md)** - Definizioni dei termini di programmazione
- **[Esempi](../../examples/)** - Programmi funzionanti completi
- **[Test](../../tests/)** - Vedi come vengono usate le funzionalità
- **GitHub Issues** - Fai domande, segnala bug

---

## Livelli di Difficoltà

In tutta la documentazione, vedrai questi marcatori:

| Marcatore | Significato |
|-----------|-------------|
| **Principiante** | Nessuna esperienza di programmazione precedente necessaria |
| **Intermedio** | Assume conoscenza base di programmazione |
| **Avanzato** | Richiede comprensione di concetti di sistema |

Se qualcosa marcato "Principiante" ti confonde, controlla il [Glossario](../glossary.md) per le definizioni dei termini.
