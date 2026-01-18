# Riferimento Comandi

Riferimento completo per tutti i comandi hpm.

## Opzioni Globali

Queste opzioni funzionano con qualsiasi comando:

| Opzione | Descrizione |
|---------|-------------|
| `--help`, `-h` | Mostra messaggio di aiuto |
| `--version`, `-v` | Mostra versione di hpm |
| `--verbose` | Mostra output dettagliato |

## Comandi

### hpm init

Crea un nuovo file `package.json`.

```bash
hpm init        # Modalita interattiva
hpm init --yes  # Accetta tutti i valori predefiniti
hpm init -y     # Forma breve
```

**Opzioni:**

| Opzione | Descrizione |
|---------|-------------|
| `--yes`, `-y` | Accetta valori predefiniti per tutti i prompt |

**Prompt interattivi:**
- Nome pacchetto (formato proprietario/repo)
- Versione (default: 1.0.0)
- Descrizione
- Autore
- Licenza (default: MIT)
- File principale (default: src/index.hml)

**Esempio:**

```bash
$ hpm init
Nome pacchetto (proprietario/repo): alice/mia-lib
Versione (1.0.0):
Descrizione: Una libreria di utilita
Autore: Alice <alice@esempio.com>
Licenza (MIT):
File principale (src/index.hml):

Creato package.json
```

---

### hpm install

Installa dipendenze o aggiungi nuovi pacchetti.

```bash
hpm install                           # Installa tutto da package.json
hpm install proprietario/repo         # Aggiungi e installa pacchetto
hpm install proprietario/repo@^1.0.0  # Con vincolo di versione
hpm install proprietario/repo --dev   # Come dipendenza di sviluppo
hpm i proprietario/repo               # Forma breve
```

**Opzioni:**

| Opzione | Descrizione |
|---------|-------------|
| `--dev`, `-D` | Aggiungi a devDependencies |
| `--verbose` | Mostra progresso dettagliato |
| `--dry-run` | Anteprima senza installare |
| `--offline` | Installa solo dalla cache (nessuna rete) |
| `--parallel` | Abilita download paralleli (sperimentale) |

**Sintassi vincoli di versione:**

| Sintassi | Esempio | Significato |
|----------|---------|-------------|
| (nessuno) | `proprietario/repo` | Ultima versione |
| Esatta | `proprietario/repo@1.2.3` | Esattamente 1.2.3 |
| Caret | `proprietario/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `proprietario/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Range | `proprietario/repo@>=1.0.0` | Almeno 1.0.0 |

**Esempi:**

```bash
# Installa tutte le dipendenze
hpm install

# Installa pacchetto specifico
hpm install hemlang/json

# Installa con vincolo di versione
hpm install hemlang/sprout@^2.0.0

# Installa come dipendenza di sviluppo
hpm install hemlang/test-utils --dev

# Anteprima di cio che verrebbe installato
hpm install hemlang/sprout --dry-run

# Output verboso
hpm install --verbose

# Installa solo dalla cache (offline)
hpm install --offline
```

**Output:**

```
Installazione dipendenze...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dipendenza di hemlang/sprout)

Installati 2 pacchetti in 1.2s
```

---

### hpm uninstall

Rimuovi un pacchetto.

```bash
hpm uninstall proprietario/repo
hpm rm proprietario/repo          # Forma breve
hpm remove proprietario/repo      # Alternativa
```

**Esempi:**

```bash
hpm uninstall hemlang/sprout
```

**Output:**

```
Rimosso hemlang/sprout@2.1.0
Aggiornato package.json
Aggiornato package-lock.json
```

---

### hpm update

Aggiorna i pacchetti alle ultime versioni entro i vincoli.

```bash
hpm update              # Aggiorna tutti i pacchetti
hpm update proprietario/repo   # Aggiorna pacchetto specifico
hpm up proprietario/repo       # Forma breve
```

**Opzioni:**

| Opzione | Descrizione |
|---------|-------------|
| `--verbose` | Mostra progresso dettagliato |
| `--dry-run` | Anteprima senza aggiornare |

**Esempi:**

```bash
# Aggiorna tutti i pacchetti
hpm update

# Aggiorna pacchetto specifico
hpm update hemlang/sprout

# Anteprima aggiornamenti
hpm update --dry-run
```

**Output:**

```
Aggiornamento dipendenze...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Aggiornati 2 pacchetti
```

---

### hpm list

Mostra i pacchetti installati.

```bash
hpm list              # Mostra albero completo delle dipendenze
hpm list --depth=0    # Solo dipendenze dirette
hpm list --depth=1    # Un livello di dipendenze transitive
hpm ls                # Forma breve
```

**Opzioni:**

| Opzione | Descrizione |
|---------|-------------|
| `--depth=N` | Limita profondita albero (default: tutto) |

**Esempi:**

```bash
$ hpm list
mio-progetto@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
mio-progetto@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Mostra i pacchetti con versioni piu recenti disponibili.

```bash
hpm outdated
```

**Output:**

```
Pacchetto          Corrente Desiderata Ultima
hemlang/sprout     2.0.0    2.0.5      2.1.0
hemlang/router     1.4.0    1.4.2      1.5.0
```

- **Corrente**: Versione installata
- **Desiderata**: Versione piu alta che soddisfa il vincolo
- **Ultima**: Ultima versione disponibile

---

### hpm run

Esegui uno script da package.json.

```bash
hpm run <script>
hpm run <script> -- <argomenti>
```

**Esempi:**

Dato questo package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Esegui gli script:

```bash
hpm run start
hpm run test
hpm run build

# Passa argomenti allo script
hpm run test -- --verbose
```

---

### hpm test

Abbreviazione per `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Equivalente a:

```bash
hpm run test
```

---

### hpm why

Spiega perche un pacchetto e installato (mostra la catena delle dipendenze).

```bash
hpm why proprietario/repo
```

**Esempio:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 e installato perche:

mio-progetto@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Gestisci la cache globale dei pacchetti.

```bash
hpm cache list    # Elenca pacchetti in cache
hpm cache clean   # Pulisci tutti i pacchetti in cache
```

**Sottocomandi:**

| Sottocomando | Descrizione |
|--------------|-------------|
| `list` | Mostra tutti i pacchetti in cache e le dimensioni |
| `clean` | Rimuovi tutti i pacchetti in cache |

**Esempi:**

```bash
$ hpm cache list
Pacchetti in cache in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Totale: 2.95 MB

$ hpm cache clean
Cache pulita (2.95 MB liberati)
```

---

## Scorciatoie dei Comandi

Per comodita, diversi comandi hanno alias brevi:

| Comando | Scorciatoie |
|---------|-------------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Esempi:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Codici di Uscita

hpm usa codici di uscita specifici per indicare diverse condizioni di errore:

| Codice | Significato |
|--------|-------------|
| 0 | Successo |
| 1 | Conflitto di dipendenze |
| 2 | Pacchetto non trovato |
| 3 | Versione non trovata |
| 4 | Errore di rete |
| 5 | package.json non valido |
| 6 | Verifica integrita fallita |
| 7 | Limite di frequenza GitHub superato |
| 8 | Dipendenza circolare |

Usa i codici di uscita negli script:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installazione fallita"
    exit 1
fi
```

---

## Variabili d'Ambiente

hpm rispetta queste variabili d'ambiente:

| Variabile | Descrizione |
|-----------|-------------|
| `GITHUB_TOKEN` | Token API GitHub per autenticazione |
| `HPM_CACHE_DIR` | Sovrascrive la posizione della directory cache |
| `HOME` | Directory home utente (per config/cache) |

**Esempi:**

```bash
# Usa token GitHub per limiti di frequenza piu alti
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Usa directory cache personalizzata
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## Vedi Anche

- [Configurazione](configuration.md) - File di configurazione
- [Specifiche dei Pacchetti](package-spec.md) - Formato package.json
- [Risoluzione dei Problemi](troubleshooting.md) - Problemi comuni
