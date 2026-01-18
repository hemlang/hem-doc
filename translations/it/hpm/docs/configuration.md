# Configurazione

Questa guida copre tutte le opzioni di configurazione per hpm.

## Panoramica

hpm puo essere configurato attraverso:

1. **Variabili d'ambiente** - Per impostazioni runtime
2. **File di configurazione globale** - `~/.hpm/config.json`
3. **File di progetto** - `package.json` e `package-lock.json`

## Variabili d'Ambiente

### GITHUB_TOKEN

Token API GitHub per l'autenticazione.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Vantaggi dell'autenticazione:**
- Limiti di frequenza API piu alti (5000 vs 60 richieste/ora)
- Accesso a repository privati
- Risoluzione delle dipendenze piu veloce

**Creazione di un token:**

1. Vai su GitHub -> Impostazioni -> Impostazioni sviluppatore -> Token di accesso personali
2. Clicca "Genera nuovo token (classico)"
3. Seleziona gli ambiti:
   - `repo` - Per accesso a repository privati
   - `read:packages` - Per GitHub Packages (se usato)
4. Genera e copia il token

### HPM_CACHE_DIR

Sovrascrive la directory cache predefinita.

```bash
export HPM_CACHE_DIR=/percorso/cache/personalizzato
```

Predefinito: `~/.hpm/cache`

**Casi d'uso:**
- Sistemi CI/CD con posizioni cache personalizzate
- Cache condivisa tra progetti
- Cache temporanea per build isolate

### HOME

Directory home dell'utente. Usata per localizzare:
- Directory config: `$HOME/.hpm/`
- Directory cache: `$HOME/.hpm/cache/`

Solitamente impostata dal sistema; sovrascrivere solo se necessario.

### Esempio .bashrc / .zshrc

```bash
# Autenticazione GitHub (consigliata)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Posizione cache personalizzata (opzionale)
# export HPM_CACHE_DIR=/percorso/a/cache

# Aggiungi hpm al PATH (se usi posizione di installazione personalizzata)
export PATH="$HOME/.local/bin:$PATH"
```

## File di Configurazione Globale

### Posizione

`~/.hpm/config.json`

### Formato

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Creazione del File di Configurazione

```bash
# Crea directory di configurazione
mkdir -p ~/.hpm

# Crea file di configurazione
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_il_tuo_token_qui"
}
EOF

# Proteggi il file (consigliato)
chmod 600 ~/.hpm/config.json
```

### Priorita del Token

Se entrambi sono impostati, la variabile d'ambiente ha la precedenza:

1. Variabile d'ambiente `GITHUB_TOKEN` (piu alta)
2. Campo `github_token` in `~/.hpm/config.json`
3. Nessuna autenticazione (default)

## Struttura delle Directory

### Directory Globali

```
~/.hpm/
├── config.json          # Configurazione globale
└── cache/               # Cache dei pacchetti
    └── proprietario/
        └── repo/
            └── 1.0.0.tar.gz
```

### Directory di Progetto

```
mio-progetto/
├── package.json         # Manifesto del progetto
├── package-lock.json    # File di lock delle dipendenze
├── hem_modules/         # Pacchetti installati
│   └── proprietario/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Codice sorgente
└── test/                # Test
```

## Cache dei Pacchetti

### Posizione

Predefinita: `~/.hpm/cache/`

Sovrascrivere con: variabile d'ambiente `HPM_CACHE_DIR`

### Struttura

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Gestione della Cache

```bash
# Visualizza pacchetti in cache
hpm cache list

# Pulisci l'intera cache
hpm cache clean
```

### Comportamento della Cache

- I pacchetti vengono messi in cache dopo il primo download
- Le installazioni successive usano le versioni in cache
- Usa `--offline` per installare solo dalla cache
- La cache e condivisa tra tutti i progetti

## Limiti di Frequenza API GitHub

### Senza Autenticazione

- **60 richieste per ora** per indirizzo IP
- Condiviso tra tutti gli utenti non autenticati sullo stesso IP
- Esaurito rapidamente in CI/CD o con molte dipendenze

### Con Autenticazione

- **5000 richieste per ora** per utente autenticato
- Limite di frequenza personale, non condiviso

### Gestione dei Limiti di Frequenza

hpm automaticamente:
- Riprova con backoff esponenziale (1s, 2s, 4s, 8s)
- Riporta errori di limite di frequenza con codice di uscita 7
- Suggerisce l'autenticazione se viene raggiunto il limite

**Soluzioni quando si raggiunge il limite:**

```bash
# Opzione 1: Autenticarsi con token GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Opzione 2: Aspettare il reset del limite di frequenza
# (I limiti si resettano ogni ora)

# Opzione 3: Usare la modalita offline (se i pacchetti sono in cache)
hpm install --offline
```

## Modalita Offline

Installa pacchetti senza accesso alla rete:

```bash
hpm install --offline
```

**Requisiti:**
- Tutti i pacchetti devono essere in cache
- Il file di lock deve esistere con versioni esatte

**Casi d'uso:**
- Ambienti air-gapped
- Build CI/CD piu veloci (con cache calda)
- Evitare limiti di frequenza

## Configurazione CI/CD

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Configura Hemlock
      run: |
        # Installa Hemlock (adatta in base alla tua configurazione)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache pacchetti hpm
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Installa dipendenze
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Esegui test
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copia prima i file del pacchetto (per il caching dei layer)
COPY package.json package-lock.json ./

# Installa le dipendenze
RUN hpm install

# Copia il codice sorgente
COPY . .

# Esegui l'applicazione
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Configurazione Proxy

Per ambienti dietro un proxy, configura a livello di sistema:

```bash
export HTTP_PROXY=http://proxy.esempio.com:8080
export HTTPS_PROXY=http://proxy.esempio.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Best Practice di Sicurezza

### Sicurezza del Token

1. **Non committare mai token** nel controllo versione
2. **Usa variabili d'ambiente** in CI/CD
3. **Limita gli ambiti del token** al minimo necessario
4. **Ruota i token** regolarmente
5. **Proteggi il file di configurazione**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Repository Privati

Per accedere a pacchetti privati:

1. Crea token con ambito `repo`
2. Configura l'autenticazione (variabile d'ambiente o file di configurazione)
3. Assicurati che il token abbia accesso al repository

```bash
# Testa l'accesso
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install tuaorg/pacchetto-privato
```

## Risoluzione Problemi di Configurazione

### Verifica Configurazione

```bash
# Controlla se il token e impostato
echo $GITHUB_TOKEN | head -c 10

# Controlla il file di configurazione
cat ~/.hpm/config.json

# Controlla la directory cache
ls -la ~/.hpm/cache/

# Testa con output verboso
hpm install --verbose
```

### Problemi Comuni

**"Limite di frequenza GitHub superato"**
- Configura l'autenticazione con `GITHUB_TOKEN`
- Aspetta il reset del limite di frequenza
- Usa `--offline` se i pacchetti sono in cache

**"Permesso negato" sulla cache**
```bash
# Correggi i permessi della cache
chmod -R u+rw ~/.hpm/cache
```

**"File di configurazione non trovato"**
```bash
# Crea la directory di configurazione
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## Vedi Anche

- [Installazione](installation.md) - Installare hpm
- [Risoluzione dei Problemi](troubleshooting.md) - Problemi comuni
- [Comandi](commands.md) - Riferimento comandi
