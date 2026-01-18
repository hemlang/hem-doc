# Architettura

Architettura interna e design di hpm. Questo documento e per i contributori e per chi e interessato a capire come funziona hpm.

## Panoramica

hpm e scritto in Hemlock e consiste di diversi moduli che gestiscono diversi aspetti della gestione dei pacchetti:

```
src/
├── main.hml        # Punto di ingresso CLI e routing dei comandi
├── manifest.hml    # Gestione package.json
├── lockfile.hml    # Gestione package-lock.json
├── semver.hml      # Versionamento semantico
├── resolver.hml    # Risoluzione delle dipendenze
├── github.hml      # Client API GitHub
├── installer.hml   # Download ed estrazione dei pacchetti
└── cache.hml       # Gestione cache globale
```

## Responsabilita dei Moduli

### main.hml

Il punto di ingresso per l'applicazione CLI.

**Responsabilita:**
- Analizzare gli argomenti da riga di comando
- Instradare i comandi ai gestori appropriati
- Visualizzare aiuto e informazioni sulla versione
- Gestire flag globali (--verbose, --dry-run, ecc.)
- Uscire con codici appropriati

**Funzioni principali:**
- `main()` - Punto di ingresso, analizza args e smista comandi
- `cmd_init()` - Gestisce `hpm init`
- `cmd_install()` - Gestisce `hpm install`
- `cmd_uninstall()` - Gestisce `hpm uninstall`
- `cmd_update()` - Gestisce `hpm update`
- `cmd_list()` - Gestisce `hpm list`
- `cmd_outdated()` - Gestisce `hpm outdated`
- `cmd_run()` - Gestisce `hpm run`
- `cmd_why()` - Gestisce `hpm why`
- `cmd_cache()` - Gestisce `hpm cache`

**Scorciatoie dei comandi:**
```hemlock
let scorciatoie = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Gestisce la lettura e scrittura dei file `package.json`.

**Responsabilita:**
- Leggere/scrivere package.json
- Validare la struttura del pacchetto
- Gestire le dipendenze
- Analizzare gli specificatori dei pacchetti (proprietario/repo@versione)

**Funzioni principali:**
```hemlock
create_default(): Manifest           // Crea manifesto vuoto
read_manifest(): Manifest            // Leggi da file
write_manifest(m: Manifest)          // Scrivi su file
validate(m: Manifest): bool          // Valida struttura
get_all_dependencies(m): Map         // Ottieni deps + devDeps
add_dependency(m, pkg, ver, dev)     // Aggiungi dipendenza
remove_dependency(m, pkg)            // Rimuovi dipendenza
parse_specifier(spec): (name, ver)   // Analizza "proprietario/repo@^1.0.0"
split_name(name): (owner, repo)      // Analizza "proprietario/repo"
```

**Struttura Manifest:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Gestisce il file `package-lock.json` per installazioni riproducibili.

**Responsabilita:**
- Creare/leggere/scrivere file di lock
- Tracciare le versioni esatte risolte
- Memorizzare URL di download e hash di integrita
- Eliminare dipendenze orfane

**Funzioni principali:**
```hemlock
create_empty(): Lockfile              // Crea lockfile vuoto
read_lockfile(): Lockfile             // Leggi da file
write_lockfile(l: Lockfile)           // Scrivi su file
create_entry(ver, url, hash, deps)    // Crea voce lock
get_locked(l, pkg): LockEntry?        // Ottieni versione bloccata
set_locked(l, pkg, entry)             // Imposta versione bloccata
remove_locked(l, pkg)                 // Rimuovi voce
prune(l, keep: Set)                   // Rimuovi orfani
needs_update(l, m): bool              // Controlla se non sincronizzato
```

**Struttura Lockfile:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // URL di download
    integrity: string,    // Hash SHA256
    dependencies: Map<string, string>
};
```

### semver.hml

Implementazione completa del Versionamento Semantico 2.0.0.

**Responsabilita:**
- Analizzare stringhe di versione
- Confrontare versioni
- Analizzare e valutare vincoli di versione
- Trovare versioni che soddisfano i vincoli

**Funzioni principali:**
```hemlock
// Analisi
parse(s: string): Version             // "1.2.3-beta+build" -> Version
stringify(v: Version): string         // Version -> "1.2.3-beta+build"

// Confronto
compare(a, b: Version): int           // -1, 0, o 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Vincoli
parse_constraint(s: string): Constraint    // "^1.2.3" -> Constraint
satisfies(v: Version, c: Constraint): bool // Controlla se v corrisponde a c
max_satisfying(versions, c): Version?      // Trova la corrispondenza piu alta
sort(versions): [Version]                  // Ordina ascendente

// Utilita
constraints_overlap(a, b: Constraint): bool  // Controlla compatibilita
```

**Struttura Version:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // es. ["beta", "1"]
    build: string?          // es. "20230101"
};
```

**Tipi di Vincolo:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" -> >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" -> >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Range combinati
    | Any;                     // "*"
```

### resolver.hml

Implementa la risoluzione delle dipendenze in stile npm.

**Responsabilita:**
- Risolvere alberi di dipendenze
- Rilevare conflitti di versione
- Rilevare dipendenze circolari
- Costruire alberi di visualizzazione

**Funzioni principali:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Risolutore principale: ritorna mappa piatta di tutte le dipendenze con versioni risolte

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Trova versione che soddisfa tutti i vincoli

detect_cycles(deps: Map): [Cycle]?
    // Trova dipendenze circolari usando DFS

build_tree(lockfile): Tree
    // Crea struttura ad albero per la visualizzazione

find_why(pkg, lockfile): [Chain]
    // Trova catene di dipendenze che spiegano perche pkg e installato
```

**Algoritmo di risoluzione:**

1. **Raccogli vincoli**: Percorri manifesto e dipendenze transitive
2. **Risolvi ogni pacchetto**: Per ogni pacchetto:
   - Ottieni tutti i vincoli di versione dai dipendenti
   - Recupera versioni disponibili da GitHub
   - Trova la versione piu alta che soddisfa TUTTI i vincoli
   - Errore se nessuna versione soddisfa tutti (conflitto)
3. **Rileva cicli**: Esegui DFS per trovare dipendenze circolari
4. **Ritorna mappa piatta**: Nome pacchetto -> info versione risolta

**Struttura ResolveResult:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

Client API GitHub per la scoperta e il download dei pacchetti.

**Responsabilita:**
- Recuperare versioni disponibili (tag)
- Scaricare package.json dai repository
- Scaricare tarball delle release
- Gestire autenticazione e limiti di frequenza

**Funzioni principali:**
```hemlock
get_token(): string?
    // Ottieni token da env o config

github_request(url, headers?): Response
    // Effettua richiesta API con retry

get_tags(owner, repo): [string]
    // Ottieni tag di versione (v1.0.0, v1.1.0, ecc.)

get_package_json(owner, repo, ref): Manifest
    // Recupera package.json a un tag/commit specifico

download_tarball(owner, repo, tag): bytes
    // Scarica archivio release

repo_exists(owner, repo): bool
    // Controlla se il repository esiste

get_repo_info(owner, repo): RepoInfo
    // Ottieni metadati del repository
```

**Logica di retry:**
- Backoff esponenziale: 1s, 2s, 4s, 8s
- Retry su: 403 (limite frequenza), 5xx (errore server), errori di rete
- Massimo 4 retry
- Riporta errori di limite di frequenza chiaramente

**Endpoint API usati:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Gestisce il download e l'estrazione dei pacchetti.

**Responsabilita:**
- Scaricare pacchetti da GitHub
- Estrarre tarball in hem_modules
- Controllare/usare pacchetti in cache
- Installare/disinstallare pacchetti

**Funzioni principali:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Scarica e installa singolo pacchetto

install_all(packages: Map, options): InstallResult
    // Installa tutti i pacchetti risolti

uninstall_package(name: string): bool
    // Rimuovi pacchetto da hem_modules

get_installed(): Map<string, string>
    // Elenca pacchetti attualmente installati

verify_integrity(pkg): bool
    // Verifica integrita del pacchetto

prefetch_packages(packages: Map): void
    // Download parallelo in cache (sperimentale)
```

**Processo di installazione:**

1. Controlla se gia installato alla versione corretta
2. Controlla cache per tarball
3. Se non in cache, scarica da GitHub
4. Memorizza in cache per uso futuro
5. Estrai in `hem_modules/proprietario/repo/`
6. Verifica installazione

**Struttura directory creata:**
```
hem_modules/
└── proprietario/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Gestisce la cache globale dei pacchetti.

**Responsabilita:**
- Memorizzare tarball scaricati
- Recuperare pacchetti in cache
- Elencare pacchetti in cache
- Pulire cache
- Gestire configurazione

**Funzioni principali:**
```hemlock
get_cache_dir(): string
    // Ottieni directory cache (rispetta HPM_CACHE_DIR)

get_config_dir(): string
    // Ottieni directory config (~/.hpm)

is_cached(owner, repo, version): bool
    // Controlla se tarball e in cache

get_cached_path(owner, repo, version): string
    // Ottieni percorso a tarball in cache

store_tarball_file(owner, repo, version, data): void
    // Salva tarball in cache

list_cached(): [CachedPackage]
    // Elenca tutti i pacchetti in cache

clear_cache(): int
    // Rimuovi tutti i pacchetti in cache, ritorna byte liberati

get_cache_size(): int
    // Calcola dimensione totale cache

read_config(): Config
    // Leggi ~/.hpm/config.json

write_config(c: Config): void
    // Scrivi file config
```

**Struttura cache:**
```
~/.hpm/
├── config.json
└── cache/
    └── proprietario/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Flusso dei Dati

### Flusso del Comando Install

```
hpm install proprietario/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Analizza args, chiama cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Leggi package.json, aggiungi dipendenza
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Risolvi tutte le dipendenze
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Ottieni versioni, trova soddisfacente
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Scarica ed estrai pacchetti
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Scarica o usa cache
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Aggiorna package-lock.json
    └──────────┘
```

### Dettaglio Algoritmo di Risoluzione

```
Input: manifest.dependencies, manifest.devDependencies, lockfile esistente

1. Inizializza:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [dipendenze dirette]

2. Mentre queue non e vuota:
   a. pkg = queue.pop()
   b. Se pkg gia risolto, salta
   c. Ottieni tutti i vincoli per pkg dai dipendenti
   d. Recupera versioni disponibili da GitHub (in cache)
   e. Trova versione max che soddisfa tutti i vincoli
   f. Se nessuna trovata: CONFLITTO
   g. resolved[pkg] = {version, url, deps}
   h. Aggiungi dipendenze di pkg alla queue

3. Rileva cicli nel grafo risolto
   - Se ciclo trovato: ERRORE

4. Ritorna mappa risolta
```

## Gestione degli Errori

### Codici di Uscita

Definiti in main.hml:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Propagazione degli Errori

Gli errori risalgono attraverso i valori di ritorno:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propaga
    // ...
}
```

## Test

### Framework di Test

Framework di test personalizzato in `test/framework.hml`:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Atteso " + expected + ", ottenuto " + actual;
    }
}
```

### File di Test

- `test/test_semver.hml` - Parsing versioni, confronto, vincoli
- `test/test_manifest.hml` - Lettura/scrittura manifesto, validazione
- `test/test_lockfile.hml` - Operazioni lockfile
- `test/test_cache.hml` - Gestione cache

### Esecuzione dei Test

```bash
# Tutti i test
make test

# Test specifici
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Miglioramenti Futuri

### Funzionalita Pianificate

1. **Verifica integrita** - Controllo hash SHA256 completo
2. **Workspace** - Supporto monorepo
3. **Sistema plugin** - Comandi estensibili
4. **Audit** - Controllo vulnerabilita di sicurezza
5. **Registro privato** - Hosting pacchetti self-hosted

### Limitazioni Note

1. **Bug bundler** - Non puo creare eseguibile standalone
2. **Download paralleli** - Sperimentale, potrebbe avere race condition
3. **Integrita** - SHA256 non completamente implementato

## Contribuire

### Stile del Codice

- Usa indentazione di 4 spazi
- Le funzioni dovrebbero fare una cosa sola
- Commenta la logica complessa
- Scrivi test per le nuove funzionalita

### Aggiungere un Comando

1. Aggiungi handler in `main.hml`:
   ```hemlock
   fn cmd_nuovocmd(args: [string]) {
       // Implementazione
   }
   ```

2. Aggiungi al dispatch dei comandi:
   ```hemlock
   match command {
       "nuovocmd" => cmd_nuovocmd(args),
       // ...
   }
   ```

3. Aggiorna il testo di aiuto

### Aggiungere un Modulo

1. Crea `src/nuovomodulo.hml`
2. Esporta l'interfaccia pubblica
3. Importa nei moduli che ne hanno bisogno
4. Aggiungi test in `test/test_nuovomodulo.hml`

## Vedi Anche

- [Comandi](commands.md) - Riferimento CLI
- [Creazione di Pacchetti](creating-packages.md) - Sviluppo pacchetti
- [Versionamento](versioning.md) - Versionamento semantico
