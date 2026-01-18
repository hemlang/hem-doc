# Creazione di Pacchetti

Questa guida spiega come creare, strutturare e pubblicare pacchetti Hemlock.

## Panoramica

hpm usa GitHub come suo registro di pacchetti. I pacchetti sono identificati dal loro percorso GitHub `proprietario/repo`, e le versioni sono tag Git. Pubblicare significa semplicemente pushare una release taggata.

## Creazione di un Nuovo Pacchetto

### 1. Inizializza il Pacchetto

Crea una nuova directory e inizializza:

```bash
mkdir mio-pacchetto
cd mio-pacchetto
hpm init
```

Rispondi ai prompt:

```
Nome pacchetto (proprietario/repo): tuonome/mio-pacchetto
Versione (1.0.0):
Descrizione: Un utile pacchetto Hemlock
Autore: Il Tuo Nome <tu@esempio.com>
Licenza (MIT):
File principale (src/index.hml):

Creato package.json
```

### 2. Crea la Struttura del Progetto

Struttura consigliata per i pacchetti:

```
mio-pacchetto/
├── package.json          # Manifesto del pacchetto
├── README.md             # Documentazione
├── LICENSE               # File di licenza
├── src/
│   ├── index.hml         # Punto di ingresso principale (esporta API pubblica)
│   ├── utils.hml         # Utilita interne
│   └── types.hml         # Definizioni dei tipi
└── test/
    ├── framework.hml     # Framework di test
    └── test_utils.hml    # Test
```

### 3. Definisci la Tua API Pubblica

**src/index.hml** - Punto di ingresso principale:

```hemlock
// Riesporta API pubblica
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Export diretti
export fn create(options: Options): Config {
    // Implementazione
}

export fn validate(config: Config): bool {
    // Implementazione
}
```

### 4. Scrivi il Tuo package.json

Esempio completo di package.json:

```json
{
  "name": "tuonome/mio-pacchetto",
  "version": "1.0.0",
  "description": "Un utile pacchetto Hemlock",
  "author": "Il Tuo Nome <tu@esempio.com>",
  "license": "MIT",
  "repository": "https://github.com/tuonome/mio-pacchetto",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utilita", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Denominazione dei Pacchetti

### Requisiti

- Deve essere nel formato `proprietario/repo`
- `proprietario` dovrebbe essere il tuo username o organizzazione GitHub
- `repo` dovrebbe essere il nome del repository
- Usa minuscole con trattini per nomi composti

### Nomi Validi

```
hemlang/sprout
alice/http-client
miaorg/json-utils
bob/date-formatter
```

### Da Evitare

```
mio-pacchetto          # Manca il proprietario
alice/MioPacchetto     # PascalCase
alice/mio_pacchetto    # Underscore
```

## Best Practice per la Struttura del Pacchetto

### Punto di Ingresso

Il campo `main` in package.json specifica il punto di ingresso:

```json
{
  "main": "src/index.hml"
}
```

Questo file dovrebbe esportare la tua API pubblica:

```hemlock
// Esporta tutto cio di cui gli utenti hanno bisogno
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Tipi
export type { Config, Options } from "./types.hml";
```

### Interno vs Pubblico

Mantieni i dettagli di implementazione interni privati:

```
src/
├── index.hml          # Pubblico: API esportata
├── parser.hml         # Pubblico: usato da index.hml
├── formatter.hml      # Pubblico: usato da index.hml
└── internal/
    ├── helpers.hml    # Privato: solo uso interno
    └── constants.hml  # Privato: solo uso interno
```

Gli utenti importano dalla root del tuo pacchetto:

```hemlock
// Buono - importa dall'API pubblica
import { parse, Parser } from "tuonome/mio-pacchetto";

// Funziona anche - import da sottopercorso
import { validate } from "tuonome/mio-pacchetto/validator";

// Sconsigliato - accesso agli interni
import { helper } from "tuonome/mio-pacchetto/internal/helpers";
```

### Export da Sottopercorso

Supporta l'import da sottopercorsi:

```
src/
├── index.hml              # Ingresso principale
├── parser/
│   └── index.hml          # tuonome/pkg/parser
├── formatter/
│   └── index.hml          # tuonome/pkg/formatter
└── utils/
    └── index.hml          # tuonome/pkg/utils
```

Gli utenti possono importare:

```hemlock
import { parse } from "tuonome/mio-pacchetto";           # Principale
import { Parser } from "tuonome/mio-pacchetto/parser";   # Sottopercorso
import { format } from "tuonome/mio-pacchetto/formatter";
```

## Dipendenze

### Aggiungere Dipendenze

```bash
# Dipendenza runtime
hpm install hemlang/json

# Dipendenza di sviluppo
hpm install hemlang/test-utils --dev
```

### Best Practice per le Dipendenze

1. **Usa range caret** per la maggior parte delle dipendenze:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Fissa le versioni** solo quando necessario (instabilita API):
   ```json
   {
     "dependencies": {
       "instabile/lib": "1.2.3"
     }
   }
   ```

3. **Evita range troppo restrittivi**:
   ```json
   // Male: troppo restrittivo
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Bene: permette aggiornamenti compatibili
   "hemlang/json": "^1.2.3"
   ```

4. **Separa le dipendenze di sviluppo**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Test del Pacchetto

### Scrivi i Test

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn esegui_test() {
    suite("Parser", fn() {
        test("analizza input valido", fn() {
            let risultato = parse("ciao");
            assert_eq(risultato.value, "ciao");
        });

        test("gestisce input vuoto", fn() {
            let risultato = parse("");
            assert_eq(risultato.value, "");
        });
    });

    suite("Stringify", fn() {
        test("converte oggetto in stringa", fn() {
            let obj = { nome: "test" };
            let risultato = stringify(obj);
            assert_eq(risultato, '{"nome":"test"}');
        });
    });
}

esegui_test();
```

### Esegui i Test

Aggiungi uno script di test:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Esegui con:

```bash
hpm test
```

## Pubblicazione

### Prerequisiti

1. Crea un repository GitHub corrispondente al nome del tuo pacchetto
2. Assicurati che `package.json` sia completo e valido
3. Tutti i test passano

### Processo di Pubblicazione

Pubblicare significa semplicemente pushare un tag Git:

```bash
# 1. Assicurati che tutto sia committato
git add .
git commit -m "Prepara release v1.0.0"

# 2. Crea un tag versione (deve iniziare con 'v')
git tag v1.0.0

# 3. Pusha codice e tag
git push origin main
git push origin v1.0.0
# Oppure pusha tutti i tag insieme
git push origin main --tags
```

### Tag di Versione

I tag devono seguire il formato `vX.Y.Z`:

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Patch
git tag v1.1.0      # Minor
git tag v2.0.0      # Major
git tag v1.0.0-beta.1  # Pre-release
```

### Checklist per la Release

Prima di pubblicare una nuova versione:

1. **Aggiorna la versione** in package.json
2. **Esegui i test**: `hpm test`
3. **Aggiorna il CHANGELOG** (se ne hai uno)
4. **Aggiorna il README** se l'API e cambiata
5. **Committa le modifiche**
6. **Crea il tag**
7. **Pusha su GitHub**

### Esempio Automatizzato

Crea uno script di release:

```bash
#!/bin/bash
# release.sh - Rilascia una nuova versione

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Uso: ./release.sh 1.0.0"
    exit 1
fi

# Esegui i test
hpm test || exit 1

# Aggiorna la versione in package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Committa e tagga
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Pusha
git push origin main --tags

echo "Rilasciata v$VERSION"
```

## Utenti che Installano il Tuo Pacchetto

Dopo la pubblicazione, gli utenti possono installare:

```bash
# Ultima versione
hpm install tuonome/mio-pacchetto

# Versione specifica
hpm install tuonome/mio-pacchetto@1.0.0

# Vincolo di versione
hpm install tuonome/mio-pacchetto@^1.0.0
```

E importare:

```hemlock
import { parse, stringify } from "tuonome/mio-pacchetto";
```

## Documentazione

### README.md

Ogni pacchetto dovrebbe avere un README:

```markdown
# mio-pacchetto

Una breve descrizione di cosa fa questo pacchetto.

## Installazione

\`\`\`bash
hpm install tuonome/mio-pacchetto
\`\`\`

## Utilizzo

\`\`\`hemlock
import { parse } from "tuonome/mio-pacchetto";

let risultato = parse("input");
\`\`\`

## API

### parse(input: string): Result

Analizza la stringa di input.

### stringify(obj: any): string

Converte l'oggetto in stringa.

## Licenza

MIT
```

### Documentazione API

Documenta tutti gli export pubblici:

```hemlock
/// Analizza la stringa di input in un Result strutturato.
///
/// # Argomenti
/// * `input` - La stringa da analizzare
///
/// # Ritorna
/// Un Result contenente i dati analizzati o un errore
///
/// # Esempio
/// ```
/// let risultato = parse("ciao mondo");
/// print(risultato.value);
/// ```
export fn parse(input: string): Result {
    // Implementazione
}
```

## Linee Guida per il Versionamento

Segui il [Versionamento Semantico](https://semver.org/):

- **MAJOR** (1.0.0 -> 2.0.0): Modifiche incompatibili
- **MINOR** (1.0.0 -> 1.1.0): Nuove funzionalita, retrocompatibili
- **PATCH** (1.0.0 -> 1.0.1): Correzioni bug, retrocompatibili

### Quando Incrementare

| Tipo di Modifica | Incremento Versione |
|------------------|---------------------|
| Modifica API incompatibile | MAJOR |
| Rimozione funzione/tipo | MAJOR |
| Cambio firma funzione | MAJOR |
| Aggiunta nuova funzione | MINOR |
| Aggiunta nuova funzionalita | MINOR |
| Correzione bug | PATCH |
| Aggiornamento documentazione | PATCH |
| Refactoring interno | PATCH |

## Vedi Anche

- [Specifiche dei Pacchetti](package-spec.md) - Riferimento completo package.json
- [Versionamento](versioning.md) - Dettagli versionamento semantico
- [Configurazione](configuration.md) - Autenticazione GitHub
