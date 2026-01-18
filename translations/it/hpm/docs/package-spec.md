# Specifiche dei Pacchetti

Riferimento completo per il formato del file `package.json`.

## Panoramica

Ogni pacchetto hpm richiede un file `package.json` nella root del progetto. Questo file definisce i metadati del pacchetto, le dipendenze e gli script.

## Esempio Minimo

```json
{
  "name": "proprietario/repo",
  "version": "1.0.0"
}
```

## Esempio Completo

```json
{
  "name": "hemlang/pacchetto-esempio",
  "version": "1.2.3",
  "description": "Un pacchetto Hemlock di esempio",
  "author": "Team Hemlock <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/pacchetto-esempio",
  "homepage": "https://hemlang.github.io/pacchetto-esempio",
  "bugs": "https://github.com/hemlang/pacchetto-esempio/issues",
  "main": "src/index.hml",
  "keywords": ["esempio", "utilita", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
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

## Riferimento Campi

### name (obbligatorio)

Il nome del pacchetto nel formato `proprietario/repo`.

```json
{
  "name": "hemlang/sprout"
}
```

**Requisiti:**
- Deve essere nel formato `proprietario/repo`
- `proprietario` dovrebbe essere il tuo username o organizzazione GitHub
- `repo` dovrebbe essere il nome del repository
- Usa lettere minuscole, numeri e trattini
- Massimo 214 caratteri totali

**Nomi validi:**
```
hemlang/sprout
alice/http-client
miaorg/json-utils
bob123/mia-lib
```

**Nomi non validi:**
```
mio-pacchetto          # Manca il proprietario
hemlang/Mio_Pacchetto  # Maiuscole e underscore
hemlang                # Manca il repo
```

### version (obbligatorio)

La versione del pacchetto seguendo il [Versionamento Semantico](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Formato:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Versioni valide:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Breve descrizione del pacchetto.

```json
{
  "description": "Un parser JSON veloce per Hemlock"
}
```

- Mantienila sotto i 200 caratteri
- Descrivi cosa fa il pacchetto, non come

### author

Informazioni sull'autore del pacchetto.

```json
{
  "author": "Il Tuo Nome <email@esempio.com>"
}
```

**Formati accettati:**
```json
"author": "Il Tuo Nome"
"author": "Il Tuo Nome <email@esempio.com>"
"author": "Il Tuo Nome <email@esempio.com> (https://sitoweb.com)"
```

### license

L'identificatore della licenza.

```json
{
  "license": "MIT"
}
```

**Licenze comuni:**
- `MIT` - Licenza MIT
- `Apache-2.0` - Licenza Apache 2.0
- `GPL-3.0` - GNU General Public License v3.0
- `BSD-3-Clause` - Licenza BSD 3-Clause
- `ISC` - Licenza ISC
- `UNLICENSED` - Proprietario/privato

Usa gli [identificatori SPDX](https://spdx.org/licenses/) quando possibile.

### repository

Link al repository sorgente.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

URL della homepage del progetto.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

URL del tracker dei problemi.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

File punto di ingresso per il pacchetto.

```json
{
  "main": "src/index.hml"
}
```

**Predefinito:** `src/index.hml`

Quando gli utenti importano il tuo pacchetto:
```hemlock
import { x } from "proprietario/repo";
```

hpm carica il file specificato in `main`.

**Ordine di risoluzione per le import:**
1. Percorso esatto: `src/index.hml`
2. Con estensione .hml: `src/index` -> `src/index.hml`
3. File index: `src/index/` -> `src/index/index.hml`

### keywords

Array di parole chiave per la scoperta.

```json
{
  "keywords": ["json", "parser", "utilita", "hemlock"]
}
```

- Usa minuscole
- Sii specifico e rilevante
- Includi il linguaggio ("hemlock") se appropriato

### dependencies

Dipendenze runtime richieste per il funzionamento del pacchetto.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Chiave:** Nome del pacchetto (`proprietario/repo`)
**Valore:** Vincolo di versione

**Sintassi vincoli di versione:**

| Vincolo | Significato |
|---------|-------------|
| `1.2.3` | Versione esatta |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Almeno 1.0.0 |
| `>=1.0.0 <2.0.0` | Range |
| `*` | Qualsiasi versione |

### devDependencies

Dipendenze solo per lo sviluppo (test, build, ecc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Le dipendenze di sviluppo sono:
- Installate durante lo sviluppo
- Non installate quando il pacchetto e usato come dipendenza
- Usate per test, build, linting, ecc.

### scripts

Comandi denominati che possono essere eseguiti con `hpm run`.

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

**Esecuzione degli script:**
```bash
hpm run start
hpm run build
hpm test        # Abbreviazione per 'hpm run test'
```

**Passare argomenti:**
```bash
hpm run test -- --verbose --filter=unit
```

**Script comuni:**

| Script | Scopo |
|--------|-------|
| `start` | Avvia l'applicazione |
| `dev` | Modalita sviluppo con hot reload |
| `test` | Esegui i test |
| `build` | Build per produzione |
| `clean` | Rimuovi artefatti di build |
| `lint` | Controlla stile codice |
| `format` | Formatta il codice |

### files

File e directory da includere quando il pacchetto viene installato.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Comportamento predefinito:** Se non specificato, include:
- Tutti i file nel repository
- Esclude `.git/`, `node_modules/`, `hem_modules/`

**Usa per:**
- Ridurre la dimensione del pacchetto
- Escludere file di test dalla distribuzione
- Includere solo i file necessari

### native

Requisiti di librerie native.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Documenta le dipendenze native che devono essere installate sul sistema.

## Validazione

hpm valida package.json in varie operazioni. Errori di validazione comuni:

### Campi obbligatori mancanti

```
Errore: package.json manca del campo obbligatorio: name
```

**Soluzione:** Aggiungi il campo obbligatorio.

### Formato nome non valido

```
Errore: Nome pacchetto non valido. Deve essere nel formato proprietario/repo.
```

**Soluzione:** Usa il formato `proprietario/repo`.

### Versione non valida

```
Errore: Versione non valida "1.0". Deve essere in formato semver (X.Y.Z).
```

**Soluzione:** Usa il formato semver completo (`1.0.0`).

### JSON non valido

```
Errore: package.json non e un JSON valido
```

**Soluzione:** Controlla la sintassi JSON (virgole, virgolette, parentesi).

## Creazione di package.json

### Interattivo

```bash
hpm init
```

Richiede ogni campo interattivamente.

### Con Valori Predefiniti

```bash
hpm init --yes
```

Crea con valori predefiniti:
```json
{
  "name": "nome-directory/nome-directory",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Manuale

Crea il file manualmente:

```bash
cat > package.json << 'EOF'
{
  "name": "tuonome/tuo-pacchetto",
  "version": "1.0.0",
  "description": "Descrizione del tuo pacchetto",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Best Practice

1. **Specifica sempre main** - Non affidarti al default
2. **Usa range caret** - `^1.0.0` per la maggior parte delle dipendenze
3. **Separa le dipendenze di sviluppo** - Mantieni le dipendenze test/build in devDependencies
4. **Includi keywords** - Aiuta gli utenti a trovare il tuo pacchetto
5. **Documenta gli script** - Dai nomi chiari agli script
6. **Specifica la licenza** - Obbligatorio per open source
7. **Aggiungi descrizione** - Aiuta gli utenti a capire lo scopo

## Vedi Anche

- [Creazione di Pacchetti](creating-packages.md) - Guida alla pubblicazione
- [Versionamento](versioning.md) - Vincoli di versione
- [Configurazione del Progetto](project-setup.md) - Struttura del progetto
