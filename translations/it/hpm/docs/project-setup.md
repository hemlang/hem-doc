# Configurazione del Progetto

Guida completa per configurare progetti Hemlock con hpm.

## Iniziare un Nuovo Progetto

### Configurazione di Base

Crea un nuovo progetto da zero:

```bash
# Crea la directory del progetto
mkdir mio-progetto
cd mio-progetto

# Inizializza package.json
hpm init

# Crea la struttura delle directory
mkdir -p src test
```

### Modelli di Progetto

Ecco strutture di progetto comuni per diversi casi d'uso:

#### Pacchetto Libreria

Per librerie riutilizzabili:

```
mia-libreria/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Ingresso principale, esporta API pubblica
│   ├── core.hml           # Funzionalita core
│   ├── utils.hml          # Funzioni di utilita
│   └── types.hml          # Definizioni dei tipi
└── test/
    ├── framework.hml      # Framework di test
    ├── run.hml            # Esecutore dei test
    └── test_core.hml      # Test
```

**package.json:**

```json
{
  "name": "tuonome/mia-libreria",
  "version": "1.0.0",
  "description": "Una libreria Hemlock riutilizzabile",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Applicazione

Per applicazioni standalone:

```
mia-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Punto di ingresso dell'applicazione
│   ├── config.hml         # Configurazione
│   ├── commands/          # Comandi CLI
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Librerie interne
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # File di dati
```

**package.json:**

```json
{
  "name": "tuonome/mia-app",
  "version": "1.0.0",
  "description": "Un'applicazione Hemlock",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Applicazione Web

Per server web:

```
mia-app-web/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Punto di ingresso del server
│   ├── routes/            # Gestori delle route
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Modelli dati
│   │   └── user.hml
│   └── services/          # Logica di business
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # File statici
│   ├── css/
│   └── js/
└── views/                 # Template
    └── index.hml
```

**package.json:**

```json
{
  "name": "tuonome/mia-app-web",
  "version": "1.0.0",
  "description": "Un'applicazione web Hemlock",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## Il File package.json

### Campi Obbligatori

```json
{
  "name": "proprietario/repo",
  "version": "1.0.0"
}
```

### Tutti i Campi

```json
{
  "name": "tuonome/mio-pacchetto",
  "version": "1.0.0",
  "description": "Descrizione del pacchetto",
  "author": "Il Tuo Nome <tu@esempio.com>",
  "license": "MIT",
  "repository": "https://github.com/tuonome/mio-pacchetto",
  "homepage": "https://tuonome.github.io/mio-pacchetto",
  "bugs": "https://github.com/tuonome/mio-pacchetto/issues",
  "main": "src/index.hml",
  "keywords": ["utilita", "parser"],
  "dependencies": {
    "proprietario/pacchetto": "^1.0.0"
  },
  "devDependencies": {
    "proprietario/lib-test": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

### Riferimento Campi

| Campo | Tipo | Descrizione |
|-------|------|-------------|
| `name` | stringa | Nome del pacchetto in formato proprietario/repo (obbligatorio) |
| `version` | stringa | Versione semantica (obbligatorio) |
| `description` | stringa | Breve descrizione |
| `author` | stringa | Nome e email dell'autore |
| `license` | stringa | Identificatore della licenza (MIT, Apache-2.0, ecc.) |
| `repository` | stringa | URL del repository |
| `homepage` | stringa | Homepage del progetto |
| `bugs` | stringa | URL del tracker dei problemi |
| `main` | stringa | File punto di ingresso (default: src/index.hml) |
| `keywords` | array | Parole chiave per la ricerca |
| `dependencies` | oggetto | Dipendenze runtime |
| `devDependencies` | oggetto | Dipendenze di sviluppo |
| `scripts` | oggetto | Script denominati |
| `files` | array | File da includere nella pubblicazione |
| `native` | oggetto | Requisiti librerie native |

## Il File package-lock.json

Il file di lock viene generato automaticamente e dovrebbe essere committato nel controllo versione. Garantisce installazioni riproducibili.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Best Practice per il File di Lock

- **Committa** package-lock.json nel controllo versione
- **Non modificare** manualmente - viene generato automaticamente
- **Esegui `hpm install`** dopo aver scaricato le modifiche
- **Elimina e rigenera** se corrotto:
  ```bash
  rm package-lock.json
  hpm install
  ```

## La Directory hem_modules

I pacchetti installati sono memorizzati in `hem_modules/`:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### Best Practice per hem_modules

- **Aggiungi a .gitignore** - non committare le dipendenze
- **Non modificare** - le modifiche verranno sovrascritte
- **Elimina per reinstallare da zero**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

File .gitignore consigliato per progetti Hemlock:

```gitignore
# Dipendenze
hem_modules/

# Output di build
dist/
*.hmlc

# File IDE
.idea/
.vscode/
*.swp
*.swo

# File del sistema operativo
.DS_Store
Thumbs.db

# Log
*.log
logs/

# Ambiente
.env
.env.local

# Copertura dei test
coverage/
```

## Lavorare con le Dipendenze

### Aggiungere Dipendenze

```bash
# Aggiungi dipendenza runtime
hpm install hemlang/json

# Aggiungi con vincolo di versione
hpm install hemlang/sprout@^2.0.0

# Aggiungi dipendenza di sviluppo
hpm install hemlang/test-utils --dev
```

### Importare Dipendenze

```hemlock
// Importa dal pacchetto (usa la voce "main")
import { parse, stringify } from "hemlang/json";

// Importa da sottopercorso
import { Router } from "hemlang/sprout/router";

// Importa libreria standard
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Risoluzione delle Import

hpm risolve le import in questo ordine:

1. **Libreria standard**: import `@stdlib/*` per moduli integrati
2. **Root del pacchetto**: `proprietario/repo` usa il campo `main`
3. **Sottopercorso**: `proprietario/repo/percorso` controlla:
   - `hem_modules/proprietario/repo/percorso.hml`
   - `hem_modules/proprietario/repo/percorso/index.hml`
   - `hem_modules/proprietario/repo/src/percorso.hml`
   - `hem_modules/proprietario/repo/src/percorso/index.hml`

## Script

### Definire Script

Aggiungi script a package.json:

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

### Eseguire Script

```bash
hpm run start
hpm run dev
hpm run build

# Abbreviazione per test
hpm test

# Passare argomenti
hpm run test -- --verbose --filter=unit
```

### Convenzioni di Denominazione degli Script

| Script | Scopo |
|--------|-------|
| `start` | Esegui l'applicazione |
| `dev` | Esegui in modalita sviluppo |
| `test` | Esegui tutti i test |
| `build` | Compila per la produzione |
| `clean` | Rimuovi i file generati |
| `lint` | Controlla lo stile del codice |
| `format` | Formatta il codice |

## Flusso di Lavoro di Sviluppo

### Configurazione Iniziale

```bash
# Clona il progetto
git clone https://github.com/tuonome/mio-progetto.git
cd mio-progetto

# Installa le dipendenze
hpm install

# Esegui i test
hpm test

# Inizia lo sviluppo
hpm run dev
```

### Flusso di Lavoro Giornaliero

```bash
# Scarica le ultime modifiche
git pull

# Installa eventuali nuove dipendenze
hpm install

# Apporta modifiche...

# Esegui i test
hpm test

# Committa
git add .
git commit -m "Aggiungi funzionalita"
git push
```

### Aggiungere una Nuova Funzionalita

```bash
# Crea branch per la funzionalita
git checkout -b feature/nuova-funzionalita

# Aggiungi nuova dipendenza se necessario
hpm install hemlang/nuova-lib

# Implementa la funzionalita...

# Testa
hpm test

# Committa e pusha
git add .
git commit -m "Aggiungi nuova funzionalita"
git push -u origin feature/nuova-funzionalita
```

## Configurazione Specifica per Ambiente

### Usare Variabili d'Ambiente

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Attenzione: API_KEY non impostata");
}
```

### File di Configurazione

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "miaapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## Vedi Anche

- [Avvio Rapido](quick-start.md) - Inizia velocemente
- [Comandi](commands.md) - Riferimento comandi
- [Creazione di Pacchetti](creating-packages.md) - Pubblicare pacchetti
- [Configurazione](configuration.md) - Configurazione di hpm
