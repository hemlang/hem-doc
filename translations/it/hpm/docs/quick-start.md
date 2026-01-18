# Avvio Rapido

Inizia a usare hpm in 5 minuti.

## Installa hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Per ulteriori opzioni di installazione, consulta la [Guida all'Installazione](installation.md).

## Crea un Nuovo Progetto

Inizia creando una nuova directory e inizializzando un pacchetto:

```bash
mkdir mio-progetto
cd mio-progetto
hpm init
```

Ti verranno richiesti i dettagli del progetto:

```
Nome pacchetto (proprietario/repo): mionome/mio-progetto
Versione (1.0.0):
Descrizione: Il mio fantastico progetto Hemlock
Autore: Il Tuo Nome <tu@esempio.com>
Licenza (MIT):
File principale (src/index.hml):

Creato package.json
```

Usa `--yes` per accettare tutti i valori predefiniti:

```bash
hpm init --yes
```

## Struttura del Progetto

Crea la struttura di base del progetto:

```
mio-progetto/
├── package.json        # Manifesto del progetto
├── src/
│   └── index.hml      # Punto di ingresso principale
└── test/
    └── test.hml       # Test
```

Crea il tuo file principale:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Punto di ingresso principale
export fn saluta(nome: string): string {
    return "Ciao, " + nome + "!";
}

export fn main() {
    print(saluta("Mondo"));
}
```

## Installa le Dipendenze

Cerca pacchetti su GitHub (i pacchetti usano il formato `proprietario/repo`):

```bash
# Installa un pacchetto
hpm install hemlang/sprout

# Installa con vincolo di versione
hpm install hemlang/json@^1.0.0

# Installa come dipendenza di sviluppo
hpm install hemlang/test-utils --dev
```

Dopo l'installazione, la struttura del tuo progetto include `hem_modules/`:

```
mio-progetto/
├── package.json
├── package-lock.json   # File di lock (generato automaticamente)
├── hem_modules/        # Pacchetti installati
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Usa i Pacchetti Installati

Importa i pacchetti usando il loro percorso GitHub:

```hemlock
// Importa dal pacchetto installato
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Importa da un sottopercorso
import { middleware } from "hemlang/sprout/middleware";

// Libreria standard (integrata)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Aggiungi Script

Aggiungi script al tuo `package.json`:

```json
{
  "name": "mionome/mio-progetto",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Esegui gli script con `hpm run`:

```bash
hpm run start
hpm run build

# Abbreviazione per test
hpm test
```

## Flussi di Lavoro Comuni

### Installazione di Tutte le Dipendenze

Quando cloni un progetto con un `package.json`:

```bash
git clone https://github.com/qualcuno/progetto.git
cd progetto
hpm install
```

### Aggiornamento delle Dipendenze

Aggiorna tutti i pacchetti alle ultime versioni entro i vincoli:

```bash
hpm update
```

Aggiorna un pacchetto specifico:

```bash
hpm update hemlang/sprout
```

### Visualizzazione dei Pacchetti Installati

Elenca tutti i pacchetti installati:

```bash
hpm list
```

L'output mostra l'albero delle dipendenze:

```
mio-progetto@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Verifica degli Aggiornamenti

Vedi quali pacchetti hanno versioni piu recenti:

```bash
hpm outdated
```

### Rimozione di un Pacchetto

```bash
hpm uninstall hemlang/sprout
```

## Esempio: Applicazione Web

Ecco un esempio completo usando un framework web:

**package.json:**
```json
{
  "name": "mionome/mia-app-web",
  "version": "1.0.0",
  "description": "Un'applicazione web",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Ciao, Mondo!");
    });

    router.get("/api/stato", fn(req, res) {
        res.json({ stato: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server in esecuzione su http://localhost:3000");
}
```

Esegui l'applicazione:

```bash
hpm install
hpm run start
```

## Prossimi Passi

- [Riferimento Comandi](commands.md) - Impara tutti i comandi hpm
- [Creazione di Pacchetti](creating-packages.md) - Pubblica i tuoi pacchetti
- [Configurazione](configuration.md) - Configura hpm e i token GitHub
- [Configurazione del Progetto](project-setup.md) - Configurazione dettagliata del progetto
