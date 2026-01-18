# Installazione

Questa guida ti aiuterà a compilare e installare Hemlock sul tuo sistema.

## Installazione Rapida (Raccomandata)

Il modo più semplice per installare Hemlock è usare lo script di installazione one-line:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Questo scarica e installa l'ultimo binario pre-compilato per la tua piattaforma (Linux o macOS, x86_64 o arm64).

### Opzioni di Installazione

```bash
# Installa in un prefisso personalizzato (default: ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Installa una versione specifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Installa e aggiorna automaticamente il PATH della shell
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

Dopo l'installazione, verifica che funzioni:

```bash
hemlock --version
```

---

## Compilazione da Sorgente

Se preferisci compilare da sorgente o i binari pre-compilati non funzionano per il tuo sistema, segui le istruzioni qui sotto.

## Prerequisiti

### Dipendenze Richieste

Hemlock richiede le seguenti dipendenze per la compilazione:

- **Compilatore C**: GCC o Clang (standard C11)
- **Make**: GNU Make
- **libffi**: Libreria Foreign Function Interface (per supporto FFI)
- **OpenSSL**: Libreria crittografica (per funzioni hash: md5, sha1, sha256)
- **libwebsockets**: Supporto client/server WebSocket e HTTP
- **zlib**: Libreria di compressione

### Installazione Dipendenze

**macOS:**
```bash
# Installa Homebrew se non già installato
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installa Xcode Command Line Tools
xcode-select --install

# Installa dipendenze via Homebrew
brew install libffi openssl@3 libwebsockets
```

**Nota per utenti macOS**: Il Makefile rileva automaticamente le installazioni Homebrew e imposta i path corretti di include/librerie. Hemlock supporta sia architetture Intel (x86_64) che Apple Silicon (arm64).

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Compilazione da Sorgente

### 1. Clona il Repository

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Compila Hemlock

```bash
make
```

Questo compilerà l'interprete Hemlock e posizionerà l'eseguibile nella directory corrente.

### 3. Verifica l'Installazione

```bash
./hemlock --version
```

Dovresti vedere le informazioni sulla versione di Hemlock.

### 4. Testa la Compilazione

Esegui la suite di test per assicurarti che tutto funzioni correttamente:

```bash
make test
```

Tutti i test dovrebbero passare. Se vedi fallimenti, segnalali come issue.

## Installazione System-Wide (Opzionale)

Per installare Hemlock system-wide (es. in `/usr/local/bin`):

```bash
sudo make install
```

Questo ti permette di eseguire `hemlock` da qualsiasi posizione senza specificare il path completo.

## Esecuzione di Hemlock

### REPL Interattivo

Avvia il Read-Eval-Print Loop:

```bash
./hemlock
```

Vedrai un prompt dove puoi digitare codice Hemlock:

```
Hemlock REPL
> print("Ciao, Mondo!");
Ciao, Mondo!
> let x = 42;
> print(x * 2);
84
>
```

Esci dal REPL con `Ctrl+D` o `Ctrl+C`.

### Esecuzione di Programmi

Esegui uno script Hemlock:

```bash
./hemlock programma.hml
```

Con argomenti da riga di comando:

```bash
./hemlock programma.hml arg1 arg2 "argomento con spazi"
```

## Struttura delle Directory

Dopo la compilazione, la tua directory Hemlock apparirà così:

```
hemlock/
├── hemlock           # Eseguibile interprete compilato
├── src/              # Codice sorgente
├── include/          # File header
├── tests/            # Suite di test
├── examples/         # Programmi esempio
├── docs/             # Documentazione
├── stdlib/           # Libreria standard
├── Makefile          # Configurazione build
└── README.md         # README del progetto
```

## Opzioni di Build

### Build di Debug

Compila con simboli di debug e senza ottimizzazione:

```bash
make debug
```

### Build Pulita

Rimuovi tutti i file compilati:

```bash
make clean
```

Ricompila da zero:

```bash
make clean && make
```

## Risoluzione Problemi

### macOS: Errori Libreria Non Trovata

Se ottieni errori su librerie mancanti (`-lcrypto`, `-lffi`, ecc.):

1. Assicurati che le dipendenze Homebrew siano installate:
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Verifica i path Homebrew:
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Il Makefile dovrebbe auto-rilevare questi path. Se non lo fa, verifica che `brew` sia nel tuo PATH:
   ```bash
   which brew
   ```

### macOS: Errori di Tipo BSD (`u_int`, `u_char` non trovati)

Se vedi errori su nomi di tipo sconosciuti come `u_int` o `u_char`:

1. Questo è risolto in v1.0.0+ usando `_DARWIN_C_SOURCE` invece di `_POSIX_C_SOURCE`
2. Assicurati di avere l'ultima versione del codice
3. Pulisci e ricompila:
   ```bash
   make clean && make
   ```

### Linux: libffi Non Trovata

Se ottieni errori su `ffi.h` mancante o `-lffi`:

1. Assicurati che `libffi-dev` sia installato (vedi dipendenze sopra)
2. Verifica se `pkg-config` può trovarla:
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. Se non trovata, potresti dover impostare `PKG_CONFIG_PATH`:
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Errori di Compilazione

Se incontri errori di compilazione:

1. Assicurati di avere un compilatore compatibile con C11
2. Su macOS, prova a usare Clang (default):
   ```bash
   make CC=clang
   ```
3. Su Linux, prova a usare GCC:
   ```bash
   make CC=gcc
   ```
4. Verifica che tutte le dipendenze siano installate
5. Prova a ricompilare da zero:
   ```bash
   make clean && make
   ```

### Fallimenti nei Test

Se i test falliscono:

1. Verifica di avere l'ultima versione del codice
2. Prova a ricompilare da zero:
   ```bash
   make clean && make test
   ```
3. Su macOS, assicurati di avere gli ultimi Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
4. Segnala il problema su GitHub con:
   - La tua piattaforma (versione macOS / distro Linux)
   - Architettura (x86_64 / arm64)
   - Output dei test
   - Output di `make -v` e `gcc --version` (o `clang --version`)

## Prossimi Passi

- [Guida all'Avvio Rapido](quick-start.md) - Scrivi il tuo primo programma Hemlock
- [Tutorial](tutorial.md) - Impara Hemlock passo dopo passo
- [Guida al Linguaggio](../language-guide/syntax.md) - Esplora le funzionalità di Hemlock
