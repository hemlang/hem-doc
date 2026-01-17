# Paketspezifikation

Vollständige Referenz für das `package.json`-Dateiformat.

## Übersicht

Jedes hpm-Paket erfordert eine `package.json`-Datei im Projektstammverzeichnis. Diese Datei definiert Paketmetadaten, Abhängigkeiten und Skripte.

## Minimales Beispiel

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Vollständiges Beispiel

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "Ein Beispiel-Hemlock-Paket",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
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

## Feldreferenz

### name (erforderlich)

Der Paketname im `owner/repo`-Format.

```json
{
  "name": "hemlang/sprout"
}
```

**Anforderungen:**
- Muss im `owner/repo`-Format sein
- `owner` sollte Ihr GitHub-Benutzername oder Ihre Organisation sein
- `repo` sollte der Repository-Name sein
- Kleinbuchstaben, Zahlen und Bindestriche verwenden
- Maximal 214 Zeichen insgesamt

**Gültige Namen:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Ungültige Namen:**
```
my-package          # Owner fehlt
hemlang/My_Package  # Großbuchstaben und Unterstrich
hemlang             # Repo fehlt
```

### version (erforderlich)

Die Paketversion nach [Semantic Versioning](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Format:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Gültige Versionen:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Kurze Beschreibung des Pakets.

```json
{
  "description": "Ein schneller JSON-Parser für Hemlock"
}
```

- Unter 200 Zeichen halten
- Beschreiben, was das Paket tut, nicht wie

### author

Informationen zum Paketautor.

```json
{
  "author": "Ihr Name <email@beispiel.com>"
}
```

**Akzeptierte Formate:**
```json
"author": "Ihr Name"
"author": "Ihr Name <email@beispiel.com>"
"author": "Ihr Name <email@beispiel.com> (https://website.com)"
```

### license

Der Lizenz-Identifikator.

```json
{
  "license": "MIT"
}
```

**Häufige Lizenzen:**
- `MIT` - MIT-Lizenz
- `Apache-2.0` - Apache-Lizenz 2.0
- `GPL-3.0` - GNU General Public License v3.0
- `BSD-3-Clause` - BSD 3-Clause-Lizenz
- `ISC` - ISC-Lizenz
- `UNLICENSED` - Proprietär/privat

Verwenden Sie wenn möglich [SPDX-Identifikatoren](https://spdx.org/licenses/).

### repository

Link zum Quell-Repository.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

Projekt-Homepage-URL.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

Issue-Tracker-URL.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Einstiegspunktdatei für das Paket.

```json
{
  "main": "src/index.hml"
}
```

**Standard:** `src/index.hml`

Wenn Benutzer Ihr Paket importieren:
```hemlock
import { x } from "owner/repo";
```

hpm lädt die in `main` angegebene Datei.

**Auflösungsreihenfolge für Importe:**
1. Exakter Pfad: `src/index.hml`
2. Mit .hml-Erweiterung: `src/index` → `src/index.hml`
3. Index-Datei: `src/index/` → `src/index/index.hml`

### keywords

Array von Schlüsselwörtern für die Auffindbarkeit.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Kleinbuchstaben verwenden
- Spezifisch und relevant sein
- Sprache ("hemlock") einschließen, falls angemessen

### dependencies

Laufzeitabhängigkeiten, die für das Funktionieren des Pakets erforderlich sind.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Schlüssel:** Paketname (`owner/repo`)
**Wert:** Versionseinschränkung

**Syntax für Versionseinschränkungen:**

| Einschränkung | Bedeutung |
|---------------|-----------|
| `1.2.3` | Exakte Version |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Mindestens 1.0.0 |
| `>=1.0.0 <2.0.0` | Bereich |
| `*` | Beliebige Version |

### devDependencies

Nur für die Entwicklung benötigte Abhängigkeiten (Testen, Bauen, etc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Dev-Abhängigkeiten werden:
- Während der Entwicklung installiert
- Nicht installiert, wenn das Paket als Abhängigkeit verwendet wird
- Für Testen, Bauen, Linting usw. verwendet

### scripts

Benannte Befehle, die mit `hpm run` ausgeführt werden können.

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

**Skripte ausführen:**
```bash
hpm run start
hpm run build
hpm test        # Kurzform für 'hpm run test'
```

**Argumente übergeben:**
```bash
hpm run test -- --verbose --filter=unit
```

**Häufige Skripte:**

| Skript | Zweck |
|--------|-------|
| `start` | Anwendung starten |
| `dev` | Entwicklungsmodus mit Hot Reload |
| `test` | Tests ausführen |
| `build` | Für Produktion bauen |
| `clean` | Build-Artefakte entfernen |
| `lint` | Code-Stil prüfen |
| `format` | Code formatieren |

### files

Dateien und Verzeichnisse, die beim Installieren des Pakets enthalten sein sollen.

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

**Standardverhalten:** Falls nicht angegeben, enthält:
- Alle Dateien im Repository
- Ausgenommen `.git/`, `node_modules/`, `hem_modules/`

**Verwenden um:**
- Paketgröße zu reduzieren
- Testdateien von der Distribution auszuschließen
- Nur notwendige Dateien einzuschließen

### native

Native Bibliotheksanforderungen.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Dokumentiert native Abhängigkeiten, die auf dem System installiert sein müssen.

## Validierung

hpm validiert package.json bei verschiedenen Operationen. Häufige Validierungsfehler:

### Fehlende erforderliche Felder

```
Error: package.json missing required field: name
```

**Lösung:** Das erforderliche Feld hinzufügen.

### Ungültiges Namensformat

```
Error: Invalid package name. Must be in owner/repo format.
```

**Lösung:** `owner/repo`-Format verwenden.

### Ungültige Version

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Lösung:** Vollständiges Semver-Format verwenden (`1.0.0`).

### Ungültiges JSON

```
Error: package.json is not valid JSON
```

**Lösung:** JSON-Syntax prüfen (Kommas, Anführungszeichen, Klammern).

## package.json erstellen

### Interaktiv

```bash
hpm init
```

Fragt interaktiv nach jedem Feld.

### Mit Standardwerten

```bash
hpm init --yes
```

Erstellt mit Standardwerten:
```json
{
  "name": "directory-name/directory-name",
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

### Manuell

Die Datei manuell erstellen:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Ihre Paketbeschreibung",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Best Practices

1. **Immer main angeben** - Nicht auf Standard verlassen
2. **Caret-Bereiche verwenden** - `^1.0.0` für die meisten Abhängigkeiten
3. **Dev-Abhängigkeiten trennen** - Test/Build-Deps in devDependencies
4. **Keywords einschließen** - Helfen Benutzern, Ihr Paket zu finden
5. **Skripte dokumentieren** - Skripte klar benennen
6. **Lizenz angeben** - Erforderlich für Open Source
7. **Beschreibung hinzufügen** - Helfen Benutzern, den Zweck zu verstehen

## Siehe auch

- [Pakete erstellen](creating-packages.md) - Veröffentlichungsanleitung
- [Versionierung](versioning.md) - Versionseinschränkungen
- [Projekteinrichtung](project-setup.md) - Projektstruktur
