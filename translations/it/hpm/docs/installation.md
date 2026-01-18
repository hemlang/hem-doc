# Installazione

Questa guida spiega come installare hpm sul tuo sistema.

## Installazione Rapida (Consigliata)

Installa l'ultima versione con un singolo comando:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Questo esegue automaticamente:
- Rileva il tuo sistema operativo (Linux, macOS)
- Rileva la tua architettura (x86_64, arm64)
- Scarica il binario precompilato appropriato
- Installa in `/usr/local/bin` (o usa sudo se necessario)

### Opzioni di Installazione

```bash
# Installa in una posizione personalizzata (sudo non richiesto)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Installa una versione specifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Combina le opzioni
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Piattaforme Supportate

| Piattaforma | Architettura | Stato |
|-------------|--------------|-------|
| Linux    | x86_64       | Supportato |
| macOS    | x86_64       | Supportato |
| macOS    | arm64 (M1/M2/M3) | Supportato |
| Linux    | arm64        | Compilare dal sorgente |

## Compilazione dal Sorgente

Se preferisci compilare dal sorgente o hai bisogno di una piattaforma non coperta dai binari precompilati, segui queste istruzioni.

### Prerequisiti

hpm richiede che [Hemlock](https://github.com/hemlang/hemlock) sia installato prima. Segui le istruzioni di installazione di Hemlock prima di procedere.

Verifica che Hemlock sia installato:

```bash
hemlock --version
```

## Metodi di Installazione

### Metodo 1: Make Install

Compila dal sorgente e installa.

```bash
# Clona il repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Installa in /usr/local/bin (richiede sudo)
sudo make install
```

Dopo l'installazione, verifica che funzioni:

```bash
hpm --version
```

### Metodo 2: Posizione Personalizzata

Installa in una directory personalizzata (sudo non richiesto):

```bash
# Clona il repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Installa in ~/.local/bin
make install PREFIX=$HOME/.local

# Oppure qualsiasi posizione personalizzata
make install PREFIX=/opt/hemlock
```

Assicurati che la tua directory bin personalizzata sia nel tuo PATH:

```bash
# Aggiungi a ~/.bashrc o ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Metodo 3: Esegui Senza Installare

Puoi eseguire hpm direttamente senza installare:

```bash
# Clona il repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Crea lo script wrapper locale
make

# Esegui dalla directory hpm
./hpm --help

# Oppure esegui tramite hemlock direttamente
hemlock src/main.hml --help
```

### Metodo 4: Installazione Manuale

Crea il tuo script wrapper:

```bash
# Clona in una posizione permanente
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Crea lo script wrapper
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Variabili di Installazione

Il Makefile supporta queste variabili:

| Variabile | Predefinito | Descrizione |
|-----------|-------------|-------------|
| `PREFIX` | `/usr/local` | Prefisso di installazione |
| `BINDIR` | `$(PREFIX)/bin` | Directory dei binari |
| `HEMLOCK` | `hemlock` | Percorso dell'interprete hemlock |

Esempio con variabili personalizzate:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Come Funziona

L'installer crea uno script shell wrapper che invoca l'interprete Hemlock con il codice sorgente di hpm:

```bash
#!/bin/sh
exec hemlock "/percorso/a/hpm/src/main.hml" "$@"
```

Questo approccio:
- Non richiede compilazione
- Esegue sempre il codice sorgente piu recente
- Funziona in modo affidabile su tutte le piattaforme

## Aggiornamento di hpm

Per aggiornare hpm all'ultima versione:

```bash
cd /percorso/a/hpm
git pull origin main

# Reinstalla se il percorso e cambiato
sudo make install
```

## Disinstallazione

Rimuovi hpm dal tuo sistema:

```bash
cd /percorso/a/hpm
sudo make uninstall
```

Oppure rimuovi manualmente:

```bash
sudo rm /usr/local/bin/hpm
```

## Verifica dell'Installazione

Dopo l'installazione, verifica che tutto funzioni:

```bash
# Controlla la versione
hpm --version

# Visualizza l'aiuto
hpm --help

# Testa l'inizializzazione (in una directory vuota)
mkdir progetto-test && cd progetto-test
hpm init --yes
cat package.json
```

## Risoluzione dei Problemi

### "hemlock: comando non trovato"

Hemlock non e installato o non e nel tuo PATH. Installa prima Hemlock:

```bash
# Controlla se hemlock esiste
which hemlock

# Se non trovato, installa Hemlock da https://github.com/hemlang/hemlock
```

### "Permesso negato"

Usa sudo per l'installazione a livello di sistema, oppure installa in una directory utente:

```bash
# Opzione 1: Usa sudo
sudo make install

# Opzione 2: Installa nella directory utente
make install PREFIX=$HOME/.local
```

### "hpm: comando non trovato" dopo l'installazione

Il tuo PATH potrebbe non includere la directory di installazione:

```bash
# Controlla dove e stato installato hpm
ls -la /usr/local/bin/hpm

# Aggiungi al PATH se usi una posizione personalizzata
export PATH="$HOME/.local/bin:$PATH"
```

## Note Specifiche per Piattaforma

### Linux

L'installazione standard funziona su tutte le distribuzioni Linux. Alcune distribuzioni potrebbero richiedere:

```bash
# Debian/Ubuntu: Assicurati di avere gli strumenti di compilazione
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

L'installazione standard funziona. Se usi Homebrew:

```bash
# Assicurati di avere gli strumenti da riga di comando Xcode
xcode-select --install
```

### Windows (WSL)

hpm funziona nel Windows Subsystem for Linux:

```bash
# Nel terminale WSL
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Prossimi Passi

Dopo l'installazione:

1. [Avvio Rapido](quick-start.md) - Crea il tuo primo progetto
2. [Riferimento Comandi](commands.md) - Impara tutti i comandi
3. [Configurazione](configuration.md) - Configura hpm
