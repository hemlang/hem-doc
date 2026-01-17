# Architektur

Interne Architektur und Design von hpm. Dieses Dokument richtet sich an Mitwirkende und diejenigen, die verstehen möchten, wie hpm funktioniert.

## Übersicht

hpm ist in Hemlock geschrieben und besteht aus mehreren Modulen, die verschiedene Aspekte der Paketverwaltung behandeln:

```
src/
├── main.hml        # CLI-Einstiegspunkt und Befehlsrouting
├── manifest.hml    # package.json-Verarbeitung
├── lockfile.hml    # package-lock.json-Verarbeitung
├── semver.hml      # Semantische Versionierung
├── resolver.hml    # Abhängigkeitsauflösung
├── github.hml      # GitHub-API-Client
├── installer.hml   # Paket-Download und -Extraktion
└── cache.hml       # Globale Cache-Verwaltung
```

## Modulverantwortlichkeiten

### main.hml

Der Einstiegspunkt für die CLI-Anwendung.

**Verantwortlichkeiten:**
- Kommandozeilenargumente parsen
- Befehle an entsprechende Handler weiterleiten
- Hilfe- und Versionsinformationen anzeigen
- Globale Flags behandeln (--verbose, --dry-run, etc.)
- Mit entsprechenden Codes beenden

**Hauptfunktionen:**
- `main()` - Einstiegspunkt, parst Args und verteilt Befehle
- `cmd_init()` - `hpm init` behandeln
- `cmd_install()` - `hpm install` behandeln
- `cmd_uninstall()` - `hpm uninstall` behandeln
- `cmd_update()` - `hpm update` behandeln
- `cmd_list()` - `hpm list` behandeln
- `cmd_outdated()` - `hpm outdated` behandeln
- `cmd_run()` - `hpm run` behandeln
- `cmd_why()` - `hpm why` behandeln
- `cmd_cache()` - `hpm cache` behandeln

**Befehlskürzel:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Behandelt das Lesen und Schreiben von `package.json`-Dateien.

**Verantwortlichkeiten:**
- package.json lesen/schreiben
- Paketstruktur validieren
- Abhängigkeiten verwalten
- Paketspezifizierer parsen (owner/repo@version)

**Hauptfunktionen:**
```hemlock
create_default(): Manifest           // Leeres Manifest erstellen
read_manifest(): Manifest            // Aus Datei lesen
write_manifest(m: Manifest)          // In Datei schreiben
validate(m: Manifest): bool          // Struktur validieren
get_all_dependencies(m): Map         // deps + devDeps holen
add_dependency(m, pkg, ver, dev)     // Abhängigkeit hinzufügen
remove_dependency(m, pkg)            // Abhängigkeit entfernen
parse_specifier(spec): (name, ver)   // "owner/repo@^1.0.0" parsen
split_name(name): (owner, repo)      // "owner/repo" parsen
```

**Manifest-Struktur:**
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

Verwaltet die `package-lock.json`-Datei für reproduzierbare Installationen.

**Verantwortlichkeiten:**
- Lock-Dateien erstellen/lesen/schreiben
- Exakt aufgelöste Versionen verfolgen
- Download-URLs und Integritäts-Hashes speichern
- Verwaiste Abhängigkeiten bereinigen

**Hauptfunktionen:**
```hemlock
create_empty(): Lockfile              // Leere Lockfile erstellen
read_lockfile(): Lockfile             // Aus Datei lesen
write_lockfile(l: Lockfile)           // In Datei schreiben
create_entry(ver, url, hash, deps)    // Lock-Eintrag erstellen
get_locked(l, pkg): LockEntry?        // Gesperrte Version holen
set_locked(l, pkg, entry)             // Gesperrte Version setzen
remove_locked(l, pkg)                 // Eintrag entfernen
prune(l, keep: Set)                   // Verwaiste entfernen
needs_update(l, m): bool              // Prüfen, ob nicht synchron
```

**Lockfile-Struktur:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // Download-URL
    integrity: string,    // SHA256-Hash
    dependencies: Map<string, string>
};
```

### semver.hml

Vollständige Implementierung von Semantic Versioning 2.0.0.

**Verantwortlichkeiten:**
- Versionszeichenketten parsen
- Versionen vergleichen
- Versionseinschränkungen parsen und auswerten
- Versionen finden, die Einschränkungen erfüllen

**Hauptfunktionen:**
```hemlock
// Parsen
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// Vergleich
compare(a, b: Version): int           // -1, 0 oder 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Einschränkungen
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // Prüfen, ob v c entspricht
max_satisfying(versions, c): Version?      // Höchste Übereinstimmung finden
sort(versions): [Version]                  // Aufsteigend sortieren

// Hilfsfunktionen
constraints_overlap(a, b: Constraint): bool  // Kompatibilität prüfen
```

**Version-Struktur:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // z.B. ["beta", "1"]
    build: string?          // z.B. "20230101"
};
```

**Constraint-Typen:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Kombinierte Bereiche
    | Any;                     // "*"
```

### resolver.hml

Implementiert npm-artige Abhängigkeitsauflösung.

**Verantwortlichkeiten:**
- Abhängigkeitsbäume auflösen
- Versionskonflikte erkennen
- Zirkuläre Abhängigkeiten erkennen
- Visualisierungsbäume erstellen

**Hauptfunktionen:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Haupt-Resolver: gibt flache Map aller Abhängigkeiten mit aufgelösten Versionen zurück

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Version finden, die alle Einschränkungen erfüllt

detect_cycles(deps: Map): [Cycle]?
    // Zirkuläre Abhängigkeiten mit DFS finden

build_tree(lockfile): Tree
    // Baumstruktur für Anzeige erstellen

find_why(pkg, lockfile): [Chain]
    // Abhängigkeitsketten finden, die erklären warum pkg installiert ist
```

**Auflösungsalgorithmus:**

1. **Einschränkungen sammeln**: Manifest und transitive Abhängigkeiten durchgehen
2. **Jedes Paket auflösen**: Für jedes Paket:
   - Alle Versionseinschränkungen von Abhängigen holen
   - Verfügbare Versionen von GitHub abrufen (gecacht)
   - Höchste Version finden, die ALLE Einschränkungen erfüllt
   - Fehler, wenn keine Version alle erfüllt (Konflikt)
3. **Zyklen erkennen**: DFS ausführen, um zirkuläre Abhängigkeiten zu finden
4. **Flache Map zurückgeben**: Paketname → aufgelöste Versionsinformation

**ResolveResult-Struktur:**
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

GitHub-API-Client für Paketentdeckung und Downloads.

**Verantwortlichkeiten:**
- Verfügbare Versionen (Tags) abrufen
- package.json aus Repositories herunterladen
- Release-Tarballs herunterladen
- Authentifizierung und Rate-Limits behandeln

**Hauptfunktionen:**
```hemlock
get_token(): string?
    // Token aus Umgebung oder Konfiguration holen

github_request(url, headers?): Response
    // API-Anfrage mit Wiederholungen machen

get_tags(owner, repo): [string]
    // Versions-Tags holen (v1.0.0, v1.1.0, etc.)

get_package_json(owner, repo, ref): Manifest
    // package.json bei bestimmtem Tag/Commit abrufen

download_tarball(owner, repo, tag): bytes
    // Release-Archiv herunterladen

repo_exists(owner, repo): bool
    // Prüfen, ob Repository existiert

get_repo_info(owner, repo): RepoInfo
    // Repository-Metadaten holen
```

**Wiederholungslogik:**
- Exponentieller Backoff: 1s, 2s, 4s, 8s
- Wiederholungen bei: 403 (Rate-Limit), 5xx (Serverfehler), Netzwerkfehler
- Maximal 4 Wiederholungen
- Rate-Limit-Fehler klar melden

**Verwendete API-Endpunkte:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Behandelt das Herunterladen und Extrahieren von Paketen.

**Verantwortlichkeiten:**
- Pakete von GitHub herunterladen
- Tarballs nach hem_modules extrahieren
- Gecachte Pakete prüfen/verwenden
- Pakete installieren/deinstallieren

**Hauptfunktionen:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Einzelnes Paket herunterladen und installieren

install_all(packages: Map, options): InstallResult
    // Alle aufgelösten Pakete installieren

uninstall_package(name: string): bool
    // Paket aus hem_modules entfernen

get_installed(): Map<string, string>
    // Aktuell installierte Pakete auflisten

verify_integrity(pkg): bool
    // Paketintegrität überprüfen

prefetch_packages(packages: Map): void
    // Paralleler Download in Cache (experimentell)
```

**Installationsprozess:**

1. Prüfen, ob bereits in korrekter Version installiert
2. Cache auf Tarball prüfen
3. Wenn nicht gecacht, von GitHub herunterladen
4. Im Cache für zukünftige Verwendung speichern
5. Nach `hem_modules/owner/repo/` extrahieren
6. Installation verifizieren

**Erstellte Verzeichnisstruktur:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Verwaltet den globalen Paket-Cache.

**Verantwortlichkeiten:**
- Heruntergeladene Tarballs speichern
- Gecachte Pakete abrufen
- Gecachte Pakete auflisten
- Cache leeren
- Konfiguration verwalten

**Hauptfunktionen:**
```hemlock
get_cache_dir(): string
    // Cache-Verzeichnis holen (berücksichtigt HPM_CACHE_DIR)

get_config_dir(): string
    // Konfigurationsverzeichnis holen (~/.hpm)

is_cached(owner, repo, version): bool
    // Prüfen, ob Tarball gecacht ist

get_cached_path(owner, repo, version): string
    // Pfad zu gecachtem Tarball holen

store_tarball_file(owner, repo, version, data): void
    // Tarball im Cache speichern

list_cached(): [CachedPackage]
    // Alle gecachten Pakete auflisten

clear_cache(): int
    // Alle gecachten Pakete entfernen, freigegebene Bytes zurückgeben

get_cache_size(): int
    // Gesamte Cache-Größe berechnen

read_config(): Config
    // ~/.hpm/config.json lesen

write_config(c: Config): void
    // Konfigurationsdatei schreiben
```

**Cache-Struktur:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Datenfluss

### Install-Befehl-Ablauf

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Args parsen, cmd_install aufrufen
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ package.json lesen, Abhängigkeit hinzufügen
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Alle Abhängigkeiten auflösen
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Versionen holen, passende finden
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Pakete herunterladen und extrahieren
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Herunterladen oder Cache verwenden
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ package-lock.json aktualisieren
    └──────────┘
```

### Auflösungsalgorithmus-Detail

```
Eingabe: manifest.dependencies, manifest.devDependencies, bestehende Lockfile

1. Initialisieren:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [direkte Abhängigkeiten]

2. Solange Queue nicht leer:
   a. pkg = queue.pop()
   b. Wenn pkg bereits aufgelöst, überspringen
   c. Alle Einschränkungen für pkg von Abhängigen holen
   d. Verfügbare Versionen von GitHub abrufen (gecacht)
   e. Max Version finden, die alle Einschränkungen erfüllt
   f. Wenn keine gefunden: KONFLIKT
   g. resolved[pkg] = {version, url, deps}
   h. pkg's Abhängigkeiten zur Queue hinzufügen

3. Zyklen im aufgelösten Graphen erkennen
   - Wenn Zyklus gefunden: FEHLER

4. Aufgelöste Map zurückgeben
```

## Fehlerbehandlung

### Exit-Codes

Definiert in main.hml:

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

### Fehler-Propagierung

Fehler steigen durch Rückgabewerte auf:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propagiert
    // ...
}
```

## Testen

### Test-Framework

Eigenes Test-Framework in `test/framework.hml`:

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
        throw "Erwartet " + expected + ", bekam " + actual;
    }
}
```

### Testdateien

- `test/test_semver.hml` - Versionsparsen, Vergleich, Einschränkungen
- `test/test_manifest.hml` - Manifest-Lesen/Schreiben, Validierung
- `test/test_lockfile.hml` - Lockfile-Operationen
- `test/test_cache.hml` - Cache-Verwaltung

### Tests ausführen

```bash
# Alle Tests
make test

# Spezifische Tests
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Zukünftige Verbesserungen

### Geplante Features

1. **Integritätsverifikation** - Vollständige SHA256-Hash-Prüfung
2. **Workspaces** - Monorepo-Unterstützung
3. **Plugin-System** - Erweiterbare Befehle
4. **Audit** - Sicherheitslücken-Prüfung
5. **Private Registry** - Selbst-gehostetes Paket-Hosting

### Bekannte Einschränkungen

1. **Bundler-Bug** - Kann keine eigenständige Executable erstellen
2. **Parallele Downloads** - Experimentell, kann Race Conditions haben
3. **Integrität** - SHA256 nicht vollständig implementiert

## Mitwirken

### Code-Stil

- 4 Leerzeichen Einrückung verwenden
- Funktionen sollten eine Sache tun
- Komplexe Logik kommentieren
- Tests für neue Features schreiben

### Befehl hinzufügen

1. Handler in `main.hml` hinzufügen:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementierung
   }
   ```

2. Zur Befehlsverteilung hinzufügen:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Hilfetext aktualisieren

### Modul hinzufügen

1. `src/newmodule.hml` erstellen
2. Öffentliche Schnittstelle exportieren
3. In Modulen importieren, die es benötigen
4. Tests in `test/test_newmodule.hml` hinzufügen

## Siehe auch

- [Befehle](commands.md) - CLI-Referenz
- [Pakete erstellen](creating-packages.md) - Paketentwicklung
- [Versionierung](versioning.md) - Semantische Versionierung
