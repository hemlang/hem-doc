# Riferimento API dei File

Riferimento completo per il sistema di I/O su file di Hemlock.

---

## Panoramica

Hemlock fornisce un'**API a oggetti File** per le operazioni sui file con gestione appropriata degli errori e gestione delle risorse. I file devono essere aperti e chiusi manualmente.

**Caratteristiche Principali:**
- Oggetto file con metodi
- Lettura/scrittura di dati testuali e binari
- Ricerca e posizionamento
- Messaggi di errore appropriati
- Gestione manuale delle risorse (no RAII)

---

## Tipo File

**Tipo:** `file`

**Descrizione:** Handle di file per operazioni di I/O

**Proprietà (Sola Lettura):**
- `.path` - Percorso del file (string)
- `.mode` - Modalità di apertura (string)
- `.closed` - Se il file è chiuso (bool)

---

## Apertura dei File

### open

Apre un file per lettura, scrittura o entrambe.

**Firma:**
```hemlock
open(percorso: string, modalita?: string): file
```

**Parametri:**
- `percorso` - Percorso del file (relativo o assoluto)
- `modalita` (opzionale) - Modalità di apertura (predefinito: `"r"`)

**Restituisce:** Oggetto file

**Modalità:**
- `"r"` - Lettura (predefinita)
- `"w"` - Scrittura (tronca file esistente)
- `"a"` - Append
- `"r+"` - Lettura e scrittura
- `"w+"` - Lettura e scrittura (tronca)
- `"a+"` - Lettura e append

**Esempi:**
```hemlock
// Modalità lettura (predefinita)
let f = open("dati.txt");
let f_lettura = open("dati.txt", "r");

// Modalità scrittura (tronca)
let f_scrittura = open("output.txt", "w");

// Modalità append
let f_append = open("log.txt", "a");

// Modalità lettura/scrittura
let f_rw = open("dati.bin", "r+");

// Lettura/scrittura (tronca)
let f_rw_trunc = open("output.bin", "w+");

// Lettura/append
let f_ra = open("log.txt", "a+");
```

**Gestione degli Errori:**
```hemlock
try {
    let f = open("mancante.txt", "r");
} catch (e) {
    print("Apertura fallita:", e);
    // Errore: Impossibile aprire 'mancante.txt': File o directory inesistente
}
```

**Importante:** I file devono essere chiusi manualmente con `f.close()` per evitare perdite di descrittori di file.

---

## Metodi dei File

### Lettura

#### read

Legge testo dal file.

**Firma:**
```hemlock
file.read(dimensione?: i32): string
```

**Parametri:**
- `dimensione` (opzionale) - Numero di byte da leggere (se omesso, legge fino a EOF)

**Restituisce:** Stringa con il contenuto del file

**Esempi:**
```hemlock
let f = open("dati.txt", "r");

// Leggi intero file
let tutto = f.read();
print(tutto);

// Leggi numero specifico di byte
let blocco = f.read(1024);

f.close();
```

**Comportamento:**
- Legge dalla posizione corrente del file
- Restituisce stringa vuota a EOF
- Avanza la posizione del file

**Errori:**
- Lettura da file chiuso
- Lettura da file di sola scrittura

---

#### read_bytes

Legge dati binari dal file.

**Firma:**
```hemlock
file.read_bytes(dimensione: i32): buffer
```

**Parametri:**
- `dimensione` - Numero di byte da leggere

**Restituisce:** Buffer con dati binari

**Esempi:**
```hemlock
let f = open("dati.bin", "r");

// Leggi 256 byte
let binario = f.read_bytes(256);
print(binario.length);       // 256

// Elabora dati binari
let i = 0;
while (i < binario.length) {
    print(binario[i]);
    i = i + 1;
}

f.close();
```

**Comportamento:**
- Legge numero esatto di byte
- Restituisce buffer (non stringa)
- Avanza la posizione del file

---

### Scrittura

#### write

Scrive testo nel file.

**Firma:**
```hemlock
file.write(dati: string): i32
```

**Parametri:**
- `dati` - Stringa da scrivere

**Restituisce:** Numero di byte scritti (i32)

**Esempi:**
```hemlock
let f = open("output.txt", "w");

// Scrivi testo
let scritti = f.write("Ciao, Mondo!\n");
print("Scritti", scritti, "byte");

// Scritture multiple
f.write("Riga 1\n");
f.write("Riga 2\n");
f.write("Riga 3\n");

f.close();
```

**Comportamento:**
- Scrive alla posizione corrente del file
- Restituisce numero di byte scritti
- Avanza la posizione del file

**Errori:**
- Scrittura su file chiuso
- Scrittura su file di sola lettura

---

#### write_bytes

Scrive dati binari nel file.

**Firma:**
```hemlock
file.write_bytes(dati: buffer): i32
```

**Parametri:**
- `dati` - Buffer da scrivere

**Restituisce:** Numero di byte scritti (i32)

**Esempi:**
```hemlock
let f = open("output.bin", "w");

// Crea buffer
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Scrivi buffer
let scritti = f.write_bytes(buf);
print("Scritti", scritti, "byte");

f.close();
```

**Comportamento:**
- Scrive il contenuto del buffer nel file
- Restituisce numero di byte scritti
- Avanza la posizione del file

---

### Posizionamento

#### seek

Sposta la posizione del file a un offset di byte specifico.

**Firma:**
```hemlock
file.seek(posizione: i32): i32
```

**Parametri:**
- `posizione` - Offset in byte dall'inizio del file

**Restituisce:** Nuova posizione nel file (i32)

**Esempi:**
```hemlock
let f = open("dati.txt", "r");

// Salta al byte 100
f.seek(100);

// Leggi da quella posizione
let blocco = f.read(50);

// Torna all'inizio
f.seek(0);

// Leggi dall'inizio
let tutto = f.read();

f.close();
```

**Comportamento:**
- Imposta la posizione del file all'offset assoluto
- Restituisce la nuova posizione
- Posizionarsi oltre EOF è permesso (crea buco nel file durante la scrittura)

---

#### tell

Ottiene la posizione corrente nel file.

**Firma:**
```hemlock
file.tell(): i32
```

**Restituisce:** Offset corrente in byte dall'inizio del file (i32)

**Esempi:**
```hemlock
let f = open("dati.txt", "r");

print(f.tell());        // 0 (all'inizio)

f.read(100);
print(f.tell());        // 100 (dopo la lettura)

f.seek(50);
print(f.tell());        // 50 (dopo il seek)

f.close();
```

---

### Chiusura

#### close

Chiude il file (idempotente).

**Firma:**
```hemlock
file.close(): null
```

**Restituisce:** `null`

**Esempi:**
```hemlock
let f = open("dati.txt", "r");
let contenuto = f.read();
f.close();

// Sicuro chiamarlo più volte
f.close();  // Nessun errore
f.close();  // Nessun errore
```

**Comportamento:**
- Chiude l'handle del file
- Svuota qualsiasi scrittura in sospeso
- Idempotente (sicuro chiamarlo più volte)
- Imposta la proprietà `.closed` a `true`

**Importante:** Chiudi sempre i file quando hai finito per evitare perdite di descrittori.

---

## Proprietà dei File

### .path

Ottiene il percorso del file.

**Tipo:** `string`

**Accesso:** Sola lettura

**Esempi:**
```hemlock
let f = open("/percorso/al/file.txt", "r");
print(f.path);          // "/percorso/al/file.txt"
f.close();
```

---

### .mode

Ottiene la modalità di apertura.

**Tipo:** `string`

**Accesso:** Sola lettura

**Esempi:**
```hemlock
let f = open("dati.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Verifica se il file è chiuso.

**Tipo:** `bool`

**Accesso:** Sola lettura

**Esempi:**
```hemlock
let f = open("dati.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Gestione degli Errori

Tutte le operazioni sui file includono messaggi di errore appropriati con contesto:

### File Non Trovato
```hemlock
let f = open("mancante.txt", "r");
// Errore: Impossibile aprire 'mancante.txt': File o directory inesistente
```

### Lettura da File Chiuso
```hemlock
let f = open("dati.txt", "r");
f.close();
f.read();
// Errore: Impossibile leggere da file chiuso 'dati.txt'
```

### Scrittura su File di Sola Lettura
```hemlock
let f = open("sola_lettura.txt", "r");
f.write("dati");
// Errore: Impossibile scrivere su file 'sola_lettura.txt' aperto in modalità sola lettura
```

### Uso di try/catch
```hemlock
let f = null;
try {
    f = open("dati.txt", "r");
    let contenuto = f.read();
    print(contenuto);
} catch (e) {
    print("Errore file:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Pattern di Gestione delle Risorse

### Pattern Base

```hemlock
let f = open("dati.txt", "r");
let contenuto = f.read();
f.close();
```

### Con Gestione degli Errori

```hemlock
let f = open("dati.txt", "r");
try {
    let contenuto = f.read();
    elabora(contenuto);
} finally {
    f.close();  // Chiudi sempre, anche in caso di errore
}
```

### Pattern Sicuro

```hemlock
let f = null;
try {
    f = open("dati.txt", "r");
    let contenuto = f.read();
    // ... elabora contenuto ...
} catch (e) {
    print("Errore:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Esempi di Utilizzo

### Leggi Intero File

```hemlock
fn leggi_file(nome_file: string): string {
    let f = open(nome_file, "r");
    let contenuto = f.read();
    f.close();
    return contenuto;
}

let testo = leggi_file("dati.txt");
print(testo);
```

### Scrivi File di Testo

```hemlock
fn scrivi_file(nome_file: string, contenuto: string) {
    let f = open(nome_file, "w");
    f.write(contenuto);
    f.close();
}

scrivi_file("output.txt", "Ciao, Mondo!\n");
```

### Append a File

```hemlock
fn aggiungi_a_file(nome_file: string, riga: string) {
    let f = open(nome_file, "a");
    f.write(riga + "\n");
    f.close();
}

aggiungi_a_file("log.txt", "Voce log 1");
aggiungi_a_file("log.txt", "Voce log 2");
```

### Leggi File Binario

```hemlock
fn leggi_binario(nome_file: string, dimensione: i32): buffer {
    let f = open(nome_file, "r");
    let dati = f.read_bytes(dimensione);
    f.close();
    return dati;
}

let binario = leggi_binario("dati.bin", 256);
print("Letti", binario.length, "byte");
```

### Scrivi File Binario

```hemlock
fn scrivi_binario(nome_file: string, dati: buffer) {
    let f = open(nome_file, "w");
    f.write_bytes(dati);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
scrivi_binario("output.bin", buf);
```

### Leggi File Riga per Riga

```hemlock
fn leggi_righe(nome_file: string): array {
    let f = open(nome_file, "r");
    let contenuto = f.read();
    f.close();
    return contenuto.split("\n");
}

let righe = leggi_righe("dati.txt");
let i = 0;
while (i < righe.length) {
    print("Riga", i, ":", righe[i]);
    i = i + 1;
}
```

### Copia File

```hemlock
fn copia_file(sorgente: string, dest: string) {
    let f_in = open(sorgente, "r");
    let f_out = open(dest, "w");

    let contenuto = f_in.read();
    f_out.write(contenuto);

    f_in.close();
    f_out.close();
}

copia_file("input.txt", "output.txt");
```

### Leggi File a Blocchi

```hemlock
fn elabora_blocchi(nome_file: string) {
    let f = open(nome_file, "r");

    while (true) {
        let blocco = f.read(1024);  // Leggi 1KB alla volta
        if (blocco.length == 0) {
            break;  // EOF
        }

        // Elabora blocco
        print("Elaborando", blocco.length, "byte");
    }

    f.close();
}

elabora_blocchi("file_grande.txt");
```

---

## Riepilogo Completo dei Metodi

| Metodo        | Firma                  | Restituisce | Descrizione                  |
|---------------|------------------------|-------------|------------------------------|
| `read`        | `(dimensione?: i32)`   | `string`    | Legge testo                  |
| `read_bytes`  | `(dimensione: i32)`    | `buffer`    | Legge dati binari            |
| `write`       | `(dati: string)`       | `i32`       | Scrive testo                 |
| `write_bytes` | `(dati: buffer)`       | `i32`       | Scrive dati binari           |
| `seek`        | `(posizione: i32)`     | `i32`       | Imposta posizione file       |
| `tell`        | `()`                   | `i32`       | Ottiene posizione file       |
| `close`       | `()`                   | `null`      | Chiude file (idempotente)    |

---

## Riepilogo Completo delle Proprietà

| Proprietà | Tipo     | Accesso     | Descrizione              |
|-----------|----------|-------------|--------------------------|
| `.path`   | `string` | Sola lettura| Percorso del file        |
| `.mode`   | `string` | Sola lettura| Modalità di apertura     |
| `.closed` | `bool`   | Sola lettura| Se il file è chiuso      |

---

## Migrazione dalla Vecchia API

**Vecchia API (Rimossa):**
- `read_file(percorso)` - Usa `open(percorso, "r").read()`
- `write_file(percorso, dati)` - Usa `open(percorso, "w").write(dati)`
- `append_file(percorso, dati)` - Usa `open(percorso, "a").write(dati)`
- `file_exists(percorso)` - Nessuna sostituzione ancora

**Esempio di Migrazione:**
```hemlock
// Vecchio (v0.0)
let contenuto = read_file("dati.txt");
write_file("output.txt", contenuto);

// Nuovo (v0.1)
let f = open("dati.txt", "r");
let contenuto = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(contenuto);
f2.close();
```

---

## Vedi Anche

- [Funzioni Integrate](builtins.md) - Funzione `open()`
- [API della Memoria](memory-api.md) - Tipo buffer
- [API delle Stringhe](string-api.md) - Metodi delle stringhe per elaborazione del testo
