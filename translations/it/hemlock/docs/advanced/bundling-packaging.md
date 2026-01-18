# Impacchettamento e Distribuzione

Hemlock fornisce strumenti integrati per impacchettare progetti multi-file in singoli file distribuibili e creare eseguibili autonomi.

## Panoramica

| Comando | Output | Caso d'Uso |
|---------|--------|------------|
| `--bundle` | `.hmlc` o `.hmlb` | Distribuire bytecode (richiede Hemlock per l'esecuzione) |
| `--package` | Eseguibile | Binario standalone (nessuna dipendenza) |
| `--compile` | `.hmlc` | Compila singolo file (nessuna risoluzione import) |

## Bundling

Il bundler risolve tutte le istruzioni `import` da un punto di ingresso e le appiattisce in un singolo file.

### Uso Base

```bash
# Impacchetta app.hml e tutti i suoi import in app.hmlc
hemlock --bundle app.hml

# Specifica percorso di output
hemlock --bundle app.hml -o dist/app.hmlc

# Crea bundle compresso (.hmlb) - dimensione file piu piccola
hemlock --bundle app.hml --compress -o app.hmlb

# Output verboso (mostra i moduli risolti)
hemlock --bundle app.hml --verbose
```

### Formati di Output

**`.hmlc` (Non Compresso)**
- Formato AST serializzato
- Veloce da caricare ed eseguire
- Formato di output predefinito

**`.hmlb` (Compresso)**
- `.hmlc` compresso con zlib
- Dimensione file piu piccola (tipicamente riduzione del 50-70%)
- Avvio leggermente piu lento a causa della decompressione

### Esecuzione di File Impacchettati

```bash
# Esegui bundle non compresso
hemlock app.hmlc

# Esegui bundle compresso
hemlock app.hmlb

# Passa argomenti
hemlock app.hmlc arg1 arg2
```

### Esempio: Progetto Multi-Modulo

```
miaapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { somma, moltiplica } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSIONE } from "./config.hml";

log(`App v${VERSIONE}`);
print(somma(2, 3));
```

```bash
hemlock --bundle miaapp/main.hml -o miaapp.hmlc
hemlock miaapp.hmlc  # Esegue con tutte le dipendenze impacchettate
```

### Import della stdlib

Il bundler risolve automaticamente gli import `@stdlib/`:

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

Quando impacchettato, i moduli della stdlib sono inclusi nell'output.

## Packaging

Il packaging crea un eseguibile autonomo incorporando il bytecode impacchettato in una copia dell'interprete Hemlock.

### Uso Base

```bash
# Crea eseguibile da app.hml
hemlock --package app.hml

# Specifica nome output
hemlock --package app.hml -o miaapp

# Salta compressione (avvio piu veloce, file piu grande)
hemlock --package app.hml --no-compress

# Output verboso
hemlock --package app.hml --verbose
```

### Esecuzione di Eseguibili Impacchettati

```bash
# L'eseguibile impacchettato viene eseguito direttamente
./miaapp

# Gli argomenti vengono passati allo script
./miaapp arg1 arg2
```

### Formato del Package

Gli eseguibili impacchettati usano il formato HMLP:

```
[binario hemlock][payload HMLB/HMLC][dimensione_payload:u64][magic HMLP:u32]
```

Quando un eseguibile impacchettato viene eseguito:
1. Controlla la presenza di un payload incorporato alla fine del file
2. Se trovato, decomprime ed esegue il payload
3. Se non trovato, si comporta come un normale interprete Hemlock

### Opzioni di Compressione

| Flag | Formato | Avvio | Dimensione |
|------|---------|-------|------------|
| (predefinito) | HMLB | Normale | Piu piccola |
| `--no-compress` | HMLC | Piu veloce | Piu grande |

Per strumenti CLI dove il tempo di avvio e importante, usare `--no-compress`.

## Ispezione dei Bundle

Usa `--info` per ispezionare file impacchettati o compilati:

```bash
hemlock --info app.hmlc
```

Output:
```
=== Info File: app.hmlc ===
Dimensione: 12847 byte
Formato: HMLC (AST compilato)
Versione: 1
Flag: 0x0001 [DEBUG]
Stringhe: 42
Istruzioni: 156
```

```bash
hemlock --info app.hmlb
```

Output:
```
=== Info File: app.hmlb ===
Dimensione: 5234 byte
Formato: HMLB (bundle compresso)
Versione: 1
Non compresso: 12847 byte
Compresso: 5224 byte
Rapporto: riduzione del 59.3%
```

## Compilazione Nativa

Per veri eseguibili nativi (senza interprete), usare il compilatore Hemlock:

```bash
# Compila in eseguibile nativo tramite C
hemlockc app.hml -o app

# Mantieni codice C generato
hemlockc app.hml -o app --keep-c

# Emetti solo C (non compilare)
hemlockc app.hml -c -o app.c

# Livello di ottimizzazione
hemlockc app.hml -o app -O2
```

Il compilatore genera codice C e invoca GCC per produrre un binario nativo. Questo richiede:
- La libreria runtime di Hemlock (`libhemlock_runtime`)
- Un compilatore C (GCC per impostazione predefinita)

### Opzioni del Compilatore

| Opzione | Descrizione |
|---------|-------------|
| `-o <file>` | Nome eseguibile di output |
| `-c` | Emetti solo codice C |
| `--emit-c <file>` | Scrivi C nel file specificato |
| `-k, --keep-c` | Mantieni C generato dopo la compilazione |
| `-O<livello>` | Livello di ottimizzazione (0-3) |
| `--cc <percorso>` | Compilatore C da usare |
| `--runtime <percorso>` | Percorso alla libreria runtime |
| `-v, --verbose` | Output verboso |

## Confronto

| Approccio | Portabilita | Avvio | Dimensione | Dipendenze |
|-----------|-------------|-------|------------|------------|
| `.hml` | Solo sorgente | Tempo di parsing | Piu piccola | Hemlock |
| `.hmlc` | Solo Hemlock | Veloce | Piccola | Hemlock |
| `.hmlb` | Solo Hemlock | Veloce | Piu piccola | Hemlock |
| `--package` | Standalone | Veloce | Piu grande | Nessuna |
| `hemlockc` | Nativo | Piu veloce | Variabile | Librerie runtime |

## Migliori Pratiche

1. **Sviluppo**: Esegui file `.hml` direttamente per iterazione rapida
2. **Distribuzione (con Hemlock)**: Impacchetta con `--compress` per file piu piccoli
3. **Distribuzione (standalone)**: Usa package per deployment senza dipendenze
4. **Prestazioni critiche**: Usa `hemlockc` per compilazione nativa

## Risoluzione Problemi

### "Impossibile trovare stdlib"

Il bundler cerca la stdlib in:
1. `./stdlib` (relativo all'eseguibile)
2. `../stdlib` (relativo all'eseguibile)
3. `/usr/local/lib/hemlock/stdlib`

Assicurati che Hemlock sia installato correttamente o esegui dalla directory sorgente.

### Dipendenze Circolari

```
Errore: Dipendenza circolare rilevata durante il caricamento di 'percorso/al/modulo.hml'
```

Rifattorizza i tuoi import per rompere il ciclo. Considera l'uso di un modulo condiviso per tipi comuni.

### Dimensione Package Grande

- Usa la compressione predefinita (non usare `--no-compress`)
- La dimensione del package include l'intero interprete (~500KB-1MB base)
- Per dimensione minima, usa `hemlockc` per compilazione nativa
