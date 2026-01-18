# I/O su File in Hemlock

Hemlock fornisce un'**API oggetto File** per operazioni sui file con gestione appropriata degli errori e gestione delle risorse.

## Indice

- [Panoramica](#panoramica)
- [Apertura di File](#apertura-di-file)
- [Metodi File](#metodi-file)
- [Proprieta File](#proprieta-file)
- [Gestione degli Errori](#gestione-degli-errori)
- [Gestione delle Risorse](#gestione-delle-risorse)
- [Riferimento API Completo](#riferimento-api-completo)
- [Pattern Comuni](#pattern-comuni)
- [Migliori Pratiche](#migliori-pratiche)

## Panoramica

L'API oggetto File fornisce:

- **Gestione esplicita delle risorse** - I file devono essere chiusi manualmente
- **Modalita di apertura multiple** - Lettura, scrittura, append, lettura/scrittura
- **Operazioni testo e binarie** - Lettura/scrittura sia di dati testo che binari
- **Supporto seeking** - Accesso casuale all'interno dei file
- **Messaggi di errore completi** - Reporting errori consapevole del contesto

**Importante:** I file non vengono chiusi automaticamente. Devi chiamare `f.close()` per evitare leak di file descriptor.

## Apertura di File

Usa `open(percorso, modalita?)` per aprire un file:

```hemlock
let f = open("dati.txt", "r");     // Modalita lettura (predefinita)
let f2 = open("output.txt", "w");  // Modalita scrittura (tronca)
let f3 = open("log.txt", "a");     // Modalita append
let f4 = open("dati.bin", "r+");   // Modalita lettura/scrittura
```

### Modalita di Apertura

| Modalita | Descrizione | File Deve Esistere | Tronca | Posizione |
|----------|-------------|-------------------|--------|-----------|
| `"r"` | Lettura (predefinita) | Si | No | Inizio |
| `"w"` | Scrittura | No (crea) | Si | Inizio |
| `"a"` | Append | No (crea) | No | Fine |
| `"r+"` | Lettura e scrittura | Si | No | Inizio |
| `"w+"` | Lettura e scrittura | No (crea) | Si | Inizio |
| `"a+"` | Lettura e append | No (crea) | No | Fine |

### Esempi

**Lettura di un file esistente:**
```hemlock
let f = open("config.json", "r");
// o semplicemente:
let f = open("config.json");  // "r" e predefinito
```

**Creazione di un nuovo file per scrittura:**
```hemlock
let f = open("output.txt", "w");  // Crea o tronca
```

**Append a un file:**
```hemlock
let f = open("log.txt", "a");  // Crea se non esiste
```

**Modalita lettura e scrittura:**
```hemlock
let f = open("dati.bin", "r+");  // File esistente, puo leggere/scrivere
```

## Metodi File

### Lettura

#### read(dimensione?: i32): string

Legge testo dal file (parametro dimensione opzionale).

**Senza dimensione (leggi tutto):**
```hemlock
let f = open("dati.txt", "r");
let tutto = f.read();  // Legge dalla posizione corrente a EOF
f.close();
```

**Con dimensione (leggi byte specifici):**
```hemlock
let f = open("dati.txt", "r");
let chunk = f.read(1024);  // Legge fino a 1024 byte
let successivo = f.read(1024);   // Legge i successivi 1024 byte
f.close();
```

**Restituisce:** Stringa contenente i dati letti, o stringa vuota se a EOF

**Esempio - Lettura file intero:**
```hemlock
let f = open("poesia.txt", "r");
let contenuto = f.read();
print(contenuto);
f.close();
```

**Esempio - Lettura a chunk:**
```hemlock
let f = open("grande.txt", "r");
while (true) {
    let chunk = f.read(4096);  // Chunk da 4KB
    if (chunk == "") { break; }  // EOF raggiunto
    elabora(chunk);
}
f.close();
```

#### read_bytes(dimensione: i32): buffer

Legge dati binari (restituisce buffer).

**Parametri:**
- `dimensione` (i32) - Numero di byte da leggere

**Restituisce:** Buffer contenente i byte letti

```hemlock
let f = open("immagine.png", "r");
let binario = f.read_bytes(256);  // Legge 256 byte
print(binario.length);  // 256 (o meno se EOF)

// Accedi a byte individuali
let primo_byte = binario[0];
print(primo_byte);

f.close();
```

**Esempio - Lettura file binario intero:**
```hemlock
let f = open("dati.bin", "r");
let dimensione = 10240;  // Dimensione attesa
let dati = f.read_bytes(dimensione);
f.close();

// Elabora dati binari
let i = 0;
while (i < dati.length) {
    let byte = dati[i];
    // ... elabora byte
    i = i + 1;
}
```

### Scrittura

#### write(dati: string): i32

Scrive testo nel file (restituisce byte scritti).

**Parametri:**
- `dati` (string) - Testo da scrivere

**Restituisce:** Numero di byte scritti (i32)

```hemlock
let f = open("output.txt", "w");
let scritti = f.write("Ciao, Mondo!\n");
print("Scritti " + typeof(scritti) + " byte");  // "Scritti 14 byte"
f.close();
```

**Esempio - Scrittura righe multiple:**
```hemlock
let f = open("output.txt", "w");
f.write("Riga 1\n");
f.write("Riga 2\n");
f.write("Riga 3\n");
f.close();
```

**Esempio - Append a file di log:**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Applicazione avviata\n");
f.write("[INFO] Utente connesso\n");
f.close();
```

#### write_bytes(dati: buffer): i32

Scrive dati binari (restituisce byte scritti).

**Parametri:**
- `dati` (buffer) - Dati binari da scrivere

**Restituisce:** Numero di byte scritti (i32)

```hemlock
let f = open("output.bin", "w");

// Crea dati binari
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let byte = f.write_bytes(buf);
print("Scritti " + typeof(byte) + " byte");

f.close();
```

**Esempio - Copia file binario:**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let dati = src.read_bytes(1024);
while (dati.length > 0) {
    dst.write_bytes(dati);
    dati = src.read_bytes(1024);
}

src.close();
dst.close();
```

### Seeking

#### seek(posizione: i32): i32

Sposta a posizione specifica (restituisce nuova posizione).

**Parametri:**
- `posizione` (i32) - Offset in byte dall'inizio del file

**Restituisce:** Nuova posizione (i32)

```hemlock
let f = open("dati.txt", "r");

// Sposta al byte 100
f.seek(100);

// Leggi dalla posizione 100
let dati = f.read(50);

// Resetta all'inizio
f.seek(0);

f.close();
```

**Esempio - Accesso casuale:**
```hemlock
let f = open("records.dat", "r");

// Leggi record all'offset 1000
f.seek(1000);
let record1 = f.read_bytes(100);

// Leggi record all'offset 2000
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Ottiene posizione corrente nel file.

**Restituisce:** Offset byte corrente (i32)

```hemlock
let f = open("dati.txt", "r");

let pos1 = f.tell();  // 0 (all'inizio)

f.read(100);
let pos2 = f.tell();  // 100 (dopo aver letto 100 byte)

f.seek(500);
let pos3 = f.tell();  // 500 (dopo seeking)

f.close();
```

**Esempio - Misurazione quantita letta:**
```hemlock
let f = open("dati.txt", "r");

let inizio = f.tell();
let contenuto = f.read();
let fine = f.tell();

let byte_letti = fine - inizio;
print("Letti " + typeof(byte_letti) + " byte");

f.close();
```

### Chiusura

#### close()

Chiude file (idempotente, puo essere chiamato piu volte).

```hemlock
let f = open("dati.txt", "r");
// ... usa file
f.close();
f.close();  // Sicuro - nessun errore alla seconda chiusura
```

**Note importanti:**
- Chiudere sempre i file quando finito per evitare leak di file descriptor
- La chiusura e idempotente - puo essere chiamata piu volte in sicurezza
- Dopo la chiusura, tutte le altre operazioni daranno errore
- Usare blocchi `finally` per assicurarsi che i file siano chiusi anche in caso di errori

## Proprieta File

Gli oggetti file hanno tre proprieta di sola lettura:

### path: string

Il percorso del file usato per aprirlo.

```hemlock
let f = open("/percorso/al/file.txt", "r");
print(f.path);  // "/percorso/al/file.txt"
f.close();
```

### mode: string

La modalita con cui il file e stato aperto.

```hemlock
let f = open("dati.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Se il file e chiuso.

```hemlock
let f = open("dati.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Esempio - Controllo se file e aperto:**
```hemlock
let f = open("dati.txt", "r");

if (!f.closed) {
    let contenuto = f.read();
    // ... elabora contenuto
}

f.close();

if (f.closed) {
    print("Il file e ora chiuso");
}
```

## Gestione degli Errori

Tutte le operazioni sui file includono messaggi di errore appropriati con contesto.

### Errori Comuni

**File non trovato:**
```hemlock
let f = open("mancante.txt", "r");
// Errore: Impossibile aprire 'mancante.txt': File o directory non esistente
```

**Lettura da file chiuso:**
```hemlock
let f = open("dati.txt", "r");
f.close();
f.read();
// Errore: Impossibile leggere da file chiuso 'dati.txt'
```

**Scrittura su file di sola lettura:**
```hemlock
let f = open("sololettura.txt", "r");
f.write("dati");
// Errore: Impossibile scrivere su file 'sololettura.txt' aperto in modalita sola lettura
```

**Lettura da file di sola scrittura:**
```hemlock
let f = open("output.txt", "w");
f.read();
// Errore: Impossibile leggere da file 'output.txt' aperto in modalita sola scrittura
```

### Uso di try/catch

```hemlock
try {
    let f = open("dati.txt", "r");
    let contenuto = f.read();
    f.close();
    elabora(contenuto);
} catch (e) {
    print("Errore lettura file: " + e);
}
```

## Gestione delle Risorse

### Pattern Base

Chiudere sempre i file esplicitamente:

```hemlock
let f = open("dati.txt", "r");
let contenuto = f.read();
f.close();
```

### Con Gestione Errori (Raccomandato)

Usare `finally` per assicurarsi che i file siano chiusi anche in caso di errori:

```hemlock
let f = open("dati.txt", "r");
try {
    let contenuto = f.read();
    elabora(contenuto);
} finally {
    f.close();  // Chiude sempre, anche in caso di errore
}
```

### File Multipli

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let contenuto = src.read();
    dst.write(contenuto);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Pattern Funzione Helper

```hemlock
fn con_file(percorso: string, modalita: string, callback) {
    let f = open(percorso, modalita);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Utilizzo:
con_file("dati.txt", "r", fn(f) {
    return f.read();
});
```

## Riferimento API Completo

### Funzioni

| Funzione | Parametri | Restituisce | Descrizione |
|----------|-----------|-------------|-------------|
| `open(percorso, modalita?)` | percorso: string, modalita?: string | File | Apre file (modalita predefinita "r") |

### Metodi

| Metodo | Parametri | Restituisce | Descrizione |
|--------|-----------|-------------|-------------|
| `read(dimensione?)` | dimensione?: i32 | string | Legge testo (tutto o byte specifici) |
| `read_bytes(dimensione)` | dimensione: i32 | buffer | Legge dati binari |
| `write(dati)` | dati: string | i32 | Scrive testo, restituisce byte scritti |
| `write_bytes(dati)` | dati: buffer | i32 | Scrive dati binari, restituisce byte scritti |
| `seek(posizione)` | posizione: i32 | i32 | Vai a posizione, restituisce nuova posizione |
| `tell()` | - | i32 | Ottieni posizione corrente |
| `close()` | - | null | Chiudi file (idempotente) |

### Proprieta (sola lettura)

| Proprieta | Tipo | Descrizione |
|-----------|------|-------------|
| `path` | string | Percorso file |
| `mode` | string | Modalita apertura |
| `closed` | bool | Se il file e chiuso |

## Pattern Comuni

### Lettura File Intero

```hemlock
fn leggi_file(percorso: string): string {
    let f = open(percorso, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let contenuto = leggi_file("config.json");
```

### Scrittura File Intero

```hemlock
fn scrivi_file(percorso: string, contenuto: string) {
    let f = open(percorso, "w");
    try {
        f.write(contenuto);
    } finally {
        f.close();
    }
}

scrivi_file("output.txt", "Ciao, Mondo!");
```

### Append a File

```hemlock
fn appendi_file(percorso: string, contenuto: string) {
    let f = open(percorso, "a");
    try {
        f.write(contenuto);
    } finally {
        f.close();
    }
}

appendi_file("log.txt", "[INFO] Evento verificato\n");
```

### Lettura Righe

```hemlock
fn leggi_righe(percorso: string) {
    let f = open(percorso, "r");
    try {
        let contenuto = f.read();
        return contenuto.split("\n");
    } finally {
        f.close();
    }
}

let righe = leggi_righe("dati.txt");
let i = 0;
while (i < righe.length) {
    print("Riga " + typeof(i) + ": " + righe[i]);
    i = i + 1;
}
```

### Elaborazione File Grandi a Chunk

```hemlock
fn elabora_file_grande(percorso: string) {
    let f = open(percorso, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // Chunk da 4KB
            if (chunk == "") { break; }

            // Elabora chunk
            elabora_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Copia File Binario

```hemlock
fn copia_file(percorso_src: string, percorso_dst: string) {
    let src = null;
    let dst = null;

    try {
        src = open(percorso_src, "r");
        dst = open(percorso_dst, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copia_file("input.dat", "output.dat");
```

### Troncamento File

```hemlock
fn tronca_file(percorso: string) {
    let f = open(percorso, "w");  // modalita "w" tronca
    f.close();
}

tronca_file("svuotami.txt");
```

### Lettura ad Accesso Casuale

```hemlock
fn leggi_a_offset(percorso: string, offset: i32, dimensione: i32): string {
    let f = open(percorso, "r");
    try {
        f.seek(offset);
        return f.read(dimensione);
    } finally {
        f.close();
    }
}

let dati = leggi_a_offset("records.dat", 1000, 100);
```

### Dimensione File

```hemlock
fn dimensione_file(percorso: string): i32 {
    let f = open(percorso, "r");
    try {
        // Vai alla fine
        let fine = f.seek(999999999);  // Numero grande
        f.seek(0);  // Resetta
        return fine;
    } finally {
        f.close();
    }
}

let dimensione = dimensione_file("dati.txt");
print("Dimensione file: " + typeof(dimensione) + " byte");
```

### Lettura/Scrittura Condizionale

```hemlock
fn aggiorna_file(percorso: string, condizione, nuovo_contenuto: string) {
    let f = open(percorso, "r+");
    try {
        let contenuto = f.read();

        if (condizione(contenuto)) {
            f.seek(0);  // Resetta all'inizio
            f.write(nuovo_contenuto);
        }
    } finally {
        f.close();
    }
}
```

## Migliori Pratiche

### 1. Usare Sempre try/finally

```hemlock
// Bene
let f = open("dati.txt", "r");
try {
    let contenuto = f.read();
    elabora(contenuto);
} finally {
    f.close();
}

// Male - il file potrebbe non chiudersi in caso di errore
let f = open("dati.txt", "r");
let contenuto = f.read();
elabora(contenuto);  // Se questo lancia, il file ha leak
f.close();
```

### 2. Controllare Stato del File Prima delle Operazioni

```hemlock
let f = open("dati.txt", "r");

if (!f.closed) {
    let contenuto = f.read();
    // ... usa contenuto
}

f.close();
```

### 3. Usare Modalita Appropriate

```hemlock
// Solo lettura? Usa "r"
let f = open("config.json", "r");

// Sostituzione completa? Usa "w"
let f = open("output.txt", "w");

// Aggiunta alla fine? Usa "a"
let f = open("log.txt", "a");
```

### 4. Gestire gli Errori con Grazia

```hemlock
fn leggi_file_sicuro(percorso: string): string {
    try {
        let f = open(percorso, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Attenzione: Impossibile leggere " + percorso + ": " + e);
        return "";
    }
}
```

### 5. Chiudere File in Ordine Inverso di Apertura

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... usa file
} finally {
    // Chiudi in ordine inverso
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Evitare di Leggere File Grandi Interamente

```hemlock
// Male per file grandi
let f = open("enorme.log", "r");
let contenuto = f.read();  // Carica intero file in memoria
f.close();

// Bene - elabora a chunk
let f = open("enorme.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        elabora_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Riepilogo

L'API I/O su File di Hemlock fornisce:

- Operazioni sui file semplici ed esplicite
- Supporto testo e binario
- Accesso casuale con seek/tell
- Messaggi di errore chiari con contesto
- Operazione close idempotente

Ricorda:
- Chiudere sempre i file manualmente
- Usare try/finally per sicurezza delle risorse
- Scegliere modalita di apertura appropriate
- Gestire gli errori con grazia
- Elaborare file grandi a chunk
