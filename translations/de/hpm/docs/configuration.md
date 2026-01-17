# Konfiguration

Diese Anleitung behandelt alle Konfigurationsoptionen für hpm.

## Übersicht

hpm kann konfiguriert werden durch:

1. **Umgebungsvariablen** - Für Laufzeiteinstellungen
2. **Globale Konfigurationsdatei** - `~/.hpm/config.json`
3. **Projektdateien** - `package.json` und `package-lock.json`

## Umgebungsvariablen

### GITHUB_TOKEN

GitHub-API-Token für Authentifizierung.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Vorteile der Authentifizierung:**
- Höhere API-Rate-Limits (5000 statt 60 Anfragen/Stunde)
- Zugriff auf private Repositories
- Schnellere Abhängigkeitsauflösung

**Token erstellen:**

1. Gehen Sie zu GitHub → Einstellungen → Entwicklereinstellungen → Personal access tokens
2. Klicken Sie auf "Generate new token (classic)"
3. Wählen Sie Berechtigungen:
   - `repo` - Für Zugriff auf private Repositories
   - `read:packages` - Für GitHub Packages (falls verwendet)
4. Generieren und Token kopieren

### HPM_CACHE_DIR

Das Standard-Cache-Verzeichnis überschreiben.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

Standard: `~/.hpm/cache`

**Anwendungsfälle:**
- CI/CD-Systeme mit benutzerdefinierten Cache-Speicherorten
- Gemeinsamer Cache über Projekte hinweg
- Temporärer Cache für isolierte Builds

### HOME

Benutzer-Home-Verzeichnis. Wird verwendet, um zu finden:
- Konfigurationsverzeichnis: `$HOME/.hpm/`
- Cache-Verzeichnis: `$HOME/.hpm/cache/`

Normalerweise vom System gesetzt; nur bei Bedarf überschreiben.

### Beispiel .bashrc / .zshrc

```bash
# GitHub-Authentifizierung (empfohlen)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Benutzerdefinierter Cache-Speicherort (optional)
# export HPM_CACHE_DIR=/path/to/cache

# hpm zum PATH hinzufügen (bei benutzerdefiniertem Installationsort)
export PATH="$HOME/.local/bin:$PATH"
```

## Globale Konfigurationsdatei

### Speicherort

`~/.hpm/config.json`

### Format

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Konfigurationsdatei erstellen

```bash
# Konfigurationsverzeichnis erstellen
mkdir -p ~/.hpm

# Konfigurationsdatei erstellen
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Datei sichern (empfohlen)
chmod 600 ~/.hpm/config.json
```

### Token-Priorität

Wenn beide gesetzt sind, hat die Umgebungsvariable Vorrang:

1. `GITHUB_TOKEN` Umgebungsvariable (höchste)
2. `~/.hpm/config.json` `github_token`-Feld
3. Keine Authentifizierung (Standard)

## Verzeichnisstruktur

### Globale Verzeichnisse

```
~/.hpm/
├── config.json          # Globale Konfiguration
└── cache/               # Paket-Cache
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Projektverzeichnisse

```
my-project/
├── package.json         # Projektmanifest
├── package-lock.json    # Abhängigkeits-Lock-Datei
├── hem_modules/         # Installierte Pakete
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Quellcode
└── test/                # Tests
```

## Paket-Cache

### Speicherort

Standard: `~/.hpm/cache/`

Überschreiben mit: `HPM_CACHE_DIR` Umgebungsvariable

### Struktur

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

### Cache verwalten

```bash
# Gecachte Pakete anzeigen
hpm cache list

# Gesamten Cache leeren
hpm cache clean
```

### Cache-Verhalten

- Pakete werden nach dem ersten Download gecacht
- Nachfolgende Installationen verwenden gecachte Versionen
- Verwenden Sie `--offline`, um nur aus dem Cache zu installieren
- Der Cache wird über alle Projekte geteilt

## GitHub-API-Rate-Limits

### Ohne Authentifizierung

- **60 Anfragen pro Stunde** pro IP-Adresse
- Geteilt unter allen nicht authentifizierten Benutzern derselben IP
- Schnell erschöpft bei CI/CD oder vielen Abhängigkeiten

### Mit Authentifizierung

- **5000 Anfragen pro Stunde** pro authentifiziertem Benutzer
- Persönliches Rate-Limit, nicht geteilt

### Rate-Limits behandeln

hpm macht automatisch:
- Wiederholungen mit exponentiellem Backoff (1s, 2s, 4s, 8s)
- Meldet Rate-Limit-Fehler mit Exit-Code 7
- Schlägt Authentifizierung vor, wenn Rate-Limit erreicht

**Lösungen bei Rate-Limit:**

```bash
# Option 1: Mit GitHub-Token authentifizieren
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Option 2: Auf Rate-Limit-Reset warten
# (Limits werden stündlich zurückgesetzt)

# Option 3: Offline-Modus verwenden (wenn Pakete gecacht sind)
hpm install --offline
```

## Offline-Modus

Pakete ohne Netzwerkzugriff installieren:

```bash
hpm install --offline
```

**Voraussetzungen:**
- Alle Pakete müssen im Cache sein
- Lock-Datei muss mit exakten Versionen existieren

**Anwendungsfälle:**
- Air-Gapped-Umgebungen
- Schnellere CI/CD-Builds (mit warmem Cache)
- Rate-Limits vermeiden

## CI/CD-Konfiguration

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Hemlock einrichten
      run: |
        # Hemlock installieren (anpassen basierend auf Ihrem Setup)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: hpm-Pakete cachen
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Abhängigkeiten installieren
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Tests ausführen
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

# Paketdateien zuerst kopieren (für Layer-Caching)
COPY package.json package-lock.json ./

# Abhängigkeiten installieren
RUN hpm install

# Quellcode kopieren
COPY . .

# Anwendung ausführen
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

## Proxy-Konfiguration

Für Umgebungen hinter einem Proxy auf Systemebene konfigurieren:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Sicherheits-Best-Practices

### Token-Sicherheit

1. **Tokens niemals committen** zur Versionskontrolle
2. **Umgebungsvariablen verwenden** in CI/CD
3. **Token-Berechtigungen einschränken** auf das erforderliche Minimum
4. **Tokens regelmäßig rotieren**
5. **Konfigurationsdatei sichern**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Private Repositories

Um auf private Pakete zuzugreifen:

1. Token mit `repo`-Berechtigung erstellen
2. Authentifizierung konfigurieren (Umgebungsvariable oder Konfigurationsdatei)
3. Sicherstellen, dass das Token Zugriff auf das Repository hat

```bash
# Zugriff testen
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Konfiguration-Fehlerbehebung

### Konfiguration überprüfen

```bash
# Prüfen, ob Token gesetzt ist
echo $GITHUB_TOKEN | head -c 10

# Konfigurationsdatei prüfen
cat ~/.hpm/config.json

# Cache-Verzeichnis prüfen
ls -la ~/.hpm/cache/

# Mit ausführlicher Ausgabe testen
hpm install --verbose
```

### Häufige Probleme

**"GitHub rate limit exceeded"**
- Authentifizierung mit `GITHUB_TOKEN` einrichten
- Auf Rate-Limit-Reset warten
- `--offline` verwenden, wenn Pakete gecacht sind

**"Permission denied" beim Cache**
```bash
# Cache-Berechtigungen reparieren
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Konfigurationsverzeichnis erstellen
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## Siehe auch

- [Installation](installation.md) - hpm installieren
- [Fehlerbehebung](troubleshooting.md) - Häufige Probleme
- [Befehle](commands.md) - Befehlsreferenz
