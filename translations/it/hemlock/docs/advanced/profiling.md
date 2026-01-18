# Profilazione

Hemlock include un profiler integrato per **analisi del tempo CPU**, **tracciamento della memoria** e **rilevamento leak**. Il profiler aiuta a identificare colli di bottiglia delle prestazioni e problemi di memoria nei tuoi programmi.

## Indice

- [Panoramica](#panoramica)
- [Avvio Rapido](#avvio-rapido)
- [Modalita di Profilazione](#modalita-di-profilazione)
- [Formati di Output](#formati-di-output)
- [Rilevamento Leak](#rilevamento-leak)
- [Comprensione dei Report](#comprensione-dei-report)
- [Generazione Flamegraph](#generazione-flamegraph)
- [Migliori Pratiche](#migliori-pratiche)

---

## Panoramica

Il profiler e accessibile tramite il sottocomando `profile`:

```bash
hemlock profile [OPZIONI] <FILE>
```

**Funzionalita principali:**
- **Profilazione CPU** - Misura il tempo speso in ogni funzione (self-time e total-time)
- **Profilazione memoria** - Traccia tutte le allocazioni con locazioni sorgente
- **Rilevamento leak** - Identifica memoria mai liberata
- **Formati output multipli** - Testo, JSON e output compatibile flamegraph
- **Statistiche memoria per-funzione** - Vedi quali funzioni allocano piu memoria

---

## Avvio Rapido

### Profila tempo CPU (predefinito)

```bash
hemlock profile script.hml
```

### Profila allocazioni memoria

```bash
hemlock profile --memory script.hml
```

### Rileva memory leak

```bash
hemlock profile --leaks script.hml
```

### Genera dati flamegraph

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## Modalita di Profilazione

### Profilazione CPU (predefinita)

Misura il tempo speso in ogni funzione, distinguendo tra:
- **Self time** - Tempo speso nell'esecuzione del codice proprio della funzione
- **Total time** - Self time piu tempo speso nelle funzioni chiamate

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # Esplicito
```

**Esempio output:**
```
=== Report Profiler Hemlock ===

Tempo totale: 1.234ms
Funzioni chiamate: 5 uniche

--- Top 5 per Self Time ---

Funzione                        Self      Total   Chiamate
--------                        ----      -----   --------
calcolo_costoso             0.892ms    0.892ms     100  (72.3%)
elabora_dati                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### Profilazione Memoria

Traccia tutte le allocazioni di memoria (`alloc`, `buffer`, `talloc`, `realloc`) con locazioni sorgente.

```bash
hemlock profile --memory script.hml
```

**Esempio output:**
```
=== Report Profiler Hemlock ===

Tempo totale: 0.543ms
Funzioni chiamate: 3 uniche
Allocazioni totali: 15 (4.2KB)

--- Top 3 per Self Time ---

Funzione                        Self      Total   Chiamate      Alloc      Conteggio
--------                        ----      -----   --------      -----      ---------
allocatore                  0.312ms    0.312ms      10      3.2KB         10  (57.5%)
operazioni_buffer           0.156ms    0.156ms       5       1KB          5  (28.7%)
main                        0.075ms    0.543ms       1        0B          0  (13.8%)

--- Top 10 Siti di Allocazione ---

Locazione                                     Totale    Conteggio
---------                                     ------    ---------
src/data.hml:42                               1.5KB        5
src/data.hml:67                               1.0KB       10
src/main.hml:15                               512B         1
```

---

### Modalita Conteggio Chiamate

Modalita a overhead minimo che conta solo le chiamate a funzione (nessun timing).

```bash
hemlock profile --calls script.hml
```

---

## Formati di Output

### Testo (predefinito)

Riepilogo leggibile con tabelle.

```bash
hemlock profile script.hml
```

---

### JSON

Formato leggibile dalla macchina per integrazione con altri strumenti.

```bash
hemlock profile --json script.hml
```

**Esempio output:**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "calcolo_costoso",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### Flamegraph

Genera formato stack collapsed compatibile con [flamegraph.pl](https://github.com/brendangregg/FlameGraph).

```bash
hemlock profile --flamegraph script.hml > profile.folded

# Genera SVG con flamegraph.pl
flamegraph.pl profile.folded > profile.svg
```

**Esempio output folded:**
```
main;elabora_dati;calcolo_costoso 892
main;elabora_dati;helper 67
main;elabora_dati 234
main 41
```

---

## Rilevamento Leak

Il flag `--leaks` mostra solo allocazioni mai liberate, rendendo facile identificare memory leak.

```bash
hemlock profile --leaks script.hml
```

**Esempio programma con leak:**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // Leak - mai liberato
    let p2 = alloc(200);    // OK - liberato sotto
    free(p2);
}

fn pulito() {
    let b = buffer(64);
    free(b);                // Liberato correttamente
}

leaky();
pulito();
```

**Output con --leaks:**
```
=== Report Profiler Hemlock ===

Tempo totale: 0.034ms
Funzioni chiamate: 2 uniche
Allocazioni totali: 3 (388B)

--- Top 2 per Self Time ---

Funzione                        Self      Total   Chiamate      Alloc      Conteggio
--------                        ----      -----   --------      -----      ---------
leaky                       0.021ms    0.021ms       1       300B          2  (61.8%)
pulito                      0.013ms    0.013ms       1        88B          1  (38.2%)

--- Memory Leak (1 sito) ---

Locazione                                    Leaked      Totale    Conteggio
---------                                    ------      ------    ---------
script.hml:2                                   100B       100B        1
```

Il report leak mostra:
- **Leaked** - Byte attualmente non liberati all'uscita del programma
- **Totale** - Byte totali mai allocati in questo sito
- **Conteggio** - Numero di allocazioni in questo sito

---

## Comprensione dei Report

### Statistiche Funzioni

| Colonna | Descrizione |
|---------|-------------|
| Funzione | Nome funzione |
| Self | Tempo nella funzione escludendo funzioni chiamate |
| Total | Tempo includendo tutte le funzioni chiamate |
| Chiamate | Numero di volte che la funzione e stata chiamata |
| Alloc | Byte totali allocati da questa funzione |
| Conteggio | Numero di allocazioni da questa funzione |
| (%) | Percentuale del tempo totale del programma |

### Siti di Allocazione

| Colonna | Descrizione |
|---------|-------------|
| Locazione | File sorgente e numero riga |
| Totale | Byte totali allocati in questa locazione |
| Conteggio | Numero di allocazioni |
| Leaked | Byte ancora allocati all'uscita del programma (solo --leaks) |

### Unita di Tempo

Il profiler seleziona automaticamente le unita appropriate:
- `ns` - Nanosecondi (< 1us)
- `us` - Microsecondi (< 1ms)
- `ms` - Millisecondi (< 1s)
- `s` - Secondi

---

## Riferimento Comandi

```
hemlock profile [OPZIONI] <FILE>

OPZIONI:
    --cpu           Profilazione CPU/tempo (predefinito)
    --memory        Profilazione allocazione memoria
    --calls         Solo conteggio chiamate (overhead minimo)
    --leaks         Mostra solo allocazioni non liberate (implica --memory)
    --json          Output in formato JSON
    --flamegraph    Output in formato compatibile flamegraph
    --top N         Mostra top N voci (predefinito: 20)
```

---

## Generazione Flamegraph

I flamegraph visualizzano dove il tuo programma spende tempo, con barre piu larghe che indicano piu tempo speso.

### Genera un Flamegraph

1. Installa flamegraph.pl:
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. Profila il tuo programma:
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. Genera SVG:
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. Apri `profile.svg` in un browser per una visualizzazione interattiva.

### Lettura dei Flamegraph

- **Asse X**: Percentuale del tempo totale (larghezza = proporzione tempo)
- **Asse Y**: Profondita stack chiamate (basso = punto di ingresso, alto = funzioni foglia)
- **Colore**: Casuale, solo per distinzione visiva
- **Click**: Zoom in una funzione per vedere le sue funzioni chiamate

---

## Migliori Pratiche

### 1. Profilare Carichi di Lavoro Rappresentativi

Profila con dati e pattern di utilizzo realistici. Casi di test piccoli potrebbero non rivelare veri colli di bottiglia.

```bash
# Bene: Profila con dati simili alla produzione
hemlock profile --memory elabora_file_grande.hml grande_input.txt

# Meno utile: Caso di test piccolo
hemlock profile test_veloce.hml
```

### 2. Usare --leaks Durante lo Sviluppo

Esegui rilevamento leak regolarmente per catturare memory leak presto:

```bash
hemlock profile --leaks mio_programma.hml
```

### 3. Confrontare Prima e Dopo

Profila prima e dopo le ottimizzazioni per misurare l'impatto:

```bash
# Prima dell'ottimizzazione
hemlock profile --json script.hml > prima.json

# Dopo l'ottimizzazione
hemlock profile --json script.hml > dopo.json

# Confronta risultati
```

### 4. Usare --top per Programmi Grandi

Limita l'output per concentrarti sulle funzioni piu significative:

```bash
hemlock profile --top 10 programma_grande.hml
```

### 5. Combinare con Flamegraph

Per pattern di chiamata complessi, i flamegraph forniscono migliore visualizzazione rispetto all'output testuale:

```bash
hemlock profile --flamegraph app_complessa.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## Overhead del Profiler

Il profiler aggiunge un po' di overhead all'esecuzione del programma:

| Modalita | Overhead | Caso d'Uso |
|----------|----------|------------|
| `--calls` | Minimo | Solo conteggio chiamate funzione |
| `--cpu` | Basso | Profilazione prestazioni generale |
| `--memory` | Moderato | Analisi memoria e rilevamento leak |

Per risultati piu accurati, profila piu volte e cerca pattern consistenti.

---

## Vedi Anche

- [Gestione Memoria](../language-guide/memory.md) - Puntatori e buffer
- [API Memoria](../reference/memory-api.md) - Funzioni alloc, free, buffer
- [Async/Concorrenza](async-concurrency.md) - Profilazione codice async
