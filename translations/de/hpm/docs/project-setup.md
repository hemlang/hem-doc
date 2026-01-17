# Projekteinrichtung

Vollständige Anleitung zur Einrichtung von Hemlock-Projekten mit hpm.

## Ein neues Projekt starten

### Grundlegende Einrichtung

Ein neues Projekt von Grund auf erstellen:

```bash
# Projektverzeichnis erstellen
mkdir my-project
cd my-project

# package.json initialisieren
hpm init

# Verzeichnisstruktur erstellen
mkdir -p src test
```

### Projektvorlagen

Hier sind gängige Projektstrukturen für verschiedene Anwendungsfälle:

#### Bibliothekspaket

Für wiederverwendbare Bibliotheken:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Haupteinstiegspunkt, exportiert öffentliche API
│   ├── core.hml           # Kernfunktionalität
│   ├── utils.hml          # Hilfsfunktionen
│   └── types.hml          # Typdefinitionen
└── test/
    ├── framework.hml      # Test-Framework
    ├── run.hml            # Test-Runner
    └── test_core.hml      # Tests
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "Eine wiederverwendbare Hemlock-Bibliothek",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Anwendung

Für eigenständige Anwendungen:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Anwendungseinstiegspunkt
│   ├── config.hml         # Konfiguration
│   ├── commands/          # CLI-Befehle
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Interne Bibliotheken
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Datendateien
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "Eine Hemlock-Anwendung",
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

#### Webanwendung

Für Webserver:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Server-Einstiegspunkt
│   ├── routes/            # Route-Handler
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Datenmodelle
│   │   └── user.hml
│   └── services/          # Geschäftslogik
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Statische Dateien
│   ├── css/
│   └── js/
└── views/                 # Templates
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "Eine Hemlock-Webanwendung",
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

## Die package.json-Datei

### Erforderliche Felder

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### Alle Felder

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Paketbeschreibung",
  "author": "Ihr Name <sie@beispiel.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
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

### Feldreferenz

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `name` | string | Paketname im owner/repo-Format (erforderlich) |
| `version` | string | Semantische Version (erforderlich) |
| `description` | string | Kurze Beschreibung |
| `author` | string | Autorname und E-Mail |
| `license` | string | Lizenz-Identifikator (MIT, Apache-2.0, etc.) |
| `repository` | string | Repository-URL |
| `homepage` | string | Projekt-Homepage |
| `bugs` | string | Issue-Tracker-URL |
| `main` | string | Einstiegspunktdatei (Standard: src/index.hml) |
| `keywords` | array | Such-Schlüsselwörter |
| `dependencies` | object | Laufzeitabhängigkeiten |
| `devDependencies` | object | Entwicklungsabhängigkeiten |
| `scripts` | object | Benannte Skripte |
| `files` | array | Dateien, die beim Veröffentlichen enthalten sein sollen |
| `native` | object | Native Bibliotheksanforderungen |

## Die package-lock.json-Datei

Die Lock-Datei wird automatisch generiert und sollte zur Versionskontrolle committet werden. Sie gewährleistet reproduzierbare Installationen.

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

### Best Practices für Lock-Dateien

- **Committen** Sie package-lock.json zur Versionskontrolle
- **Nicht manuell bearbeiten** - sie wird automatisch generiert
- **`hpm install` ausführen** nach dem Pullen von Änderungen
- **Löschen und neu generieren** falls beschädigt:
  ```bash
  rm package-lock.json
  hpm install
  ```

## Das hem_modules-Verzeichnis

Installierte Pakete werden in `hem_modules/` gespeichert:

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

### Best Practices für hem_modules

- **Zu .gitignore hinzufügen** - Abhängigkeiten nicht committen
- **Nicht modifizieren** - Änderungen werden überschrieben
- **Löschen zum Neu-Installieren**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Empfohlene .gitignore für Hemlock-Projekte:

```gitignore
# Abhängigkeiten
hem_modules/

# Build-Ausgabe
dist/
*.hmlc

# IDE-Dateien
.idea/
.vscode/
*.swp
*.swo

# OS-Dateien
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Umgebung
.env
.env.local

# Testabdeckung
coverage/
```

## Mit Abhängigkeiten arbeiten

### Abhängigkeiten hinzufügen

```bash
# Laufzeitabhängigkeit hinzufügen
hpm install hemlang/json

# Mit Versionseinschränkung hinzufügen
hpm install hemlang/sprout@^2.0.0

# Entwicklungsabhängigkeit hinzufügen
hpm install hemlang/test-utils --dev
```

### Abhängigkeiten importieren

```hemlock
// Aus Paket importieren (verwendet "main"-Eintrag)
import { parse, stringify } from "hemlang/json";

// Aus Unterpfad importieren
import { Router } from "hemlang/sprout/router";

// Standardbibliothek importieren
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Import-Auflösung

hpm löst Importe in dieser Reihenfolge auf:

1. **Standardbibliothek**: `@stdlib/*` importiert eingebaute Module
2. **Paket-Root**: `owner/repo` verwendet das `main`-Feld
3. **Unterpfad**: `owner/repo/path` prüft:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Skripte

### Skripte definieren

Skripte zur package.json hinzufügen:

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

### Skripte ausführen

```bash
hpm run start
hpm run dev
hpm run build

# Kurzform für test
hpm test

# Argumente übergeben
hpm run test -- --verbose --filter=unit
```

### Skript-Namenskonventionen

| Skript | Zweck |
|--------|-------|
| `start` | Anwendung ausführen |
| `dev` | Im Entwicklungsmodus ausführen |
| `test` | Alle Tests ausführen |
| `build` | Für Produktion bauen |
| `clean` | Generierte Dateien entfernen |
| `lint` | Code-Stil prüfen |
| `format` | Code formatieren |

## Entwicklungsworkflow

### Ersteinrichtung

```bash
# Projekt klonen
git clone https://github.com/yourusername/my-project.git
cd my-project

# Abhängigkeiten installieren
hpm install

# Tests ausführen
hpm test

# Entwicklung starten
hpm run dev
```

### Täglicher Workflow

```bash
# Neueste Änderungen pullen
git pull

# Neue Abhängigkeiten installieren
hpm install

# Änderungen vornehmen...

# Tests ausführen
hpm test

# Committen
git add .
git commit -m "Feature hinzugefügt"
git push
```

### Neues Feature hinzufügen

```bash
# Feature-Branch erstellen
git checkout -b feature/new-feature

# Bei Bedarf neue Abhängigkeit hinzufügen
hpm install hemlang/new-lib

# Feature implementieren...

# Testen
hpm test

# Committen und pushen
git add .
git commit -m "Neues Feature hinzugefügt"
git push -u origin feature/new-feature
```

## Umgebungsspezifische Konfiguration

### Umgebungsvariablen verwenden

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warnung: API_KEY nicht gesetzt");
}
```

### Konfigurationsdatei

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
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

## Siehe auch

- [Schnellstart](quick-start.md) - Schnell loslegen
- [Befehle](commands.md) - Befehlsreferenz
- [Pakete erstellen](creating-packages.md) - Pakete veröffentlichen
- [Konfiguration](configuration.md) - hpm-Konfiguration
