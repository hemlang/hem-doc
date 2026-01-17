# Fehlerbehebung

Lösungen für häufige hpm-Probleme.

## Installationsprobleme

### "hemlock: command not found"

**Ursache:** Hemlock ist nicht installiert oder nicht im PATH.

**Lösung:**

```bash
# Prüfen, ob hemlock existiert
which hemlock

# Falls nicht gefunden, zuerst Hemlock installieren
# Besuchen Sie: https://github.com/hemlang/hemlock

# Nach der Installation überprüfen
hemlock --version
```

### "hpm: command not found"

**Ursache:** hpm ist nicht installiert oder nicht im PATH.

**Lösung:**

```bash
# Prüfen, wo hpm installiert ist
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Bei benutzerdefiniertem Speicherort zum PATH hinzufügen
export PATH="$HOME/.local/bin:$PATH"

# Für Persistenz zu ~/.bashrc oder ~/.zshrc hinzufügen
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Bei Bedarf neu installieren
cd /path/to/hpm
sudo make install
```

### "Permission denied" bei Installation

**Ursache:** Keine Schreibberechtigung für das Installationsverzeichnis.

**Lösung:**

```bash
# Option 1: sudo für systemweite Installation verwenden
sudo make install

# Option 2: In Benutzerverzeichnis installieren (kein sudo)
make install PREFIX=$HOME/.local
```

## Abhängigkeitsprobleme

### "Package not found" (Exit-Code 2)

**Ursache:** Das Paket existiert nicht auf GitHub.

**Lösung:**

```bash
# Prüfen, ob das Paket existiert
# Besuchen Sie: https://github.com/owner/repo

# Rechtschreibung überprüfen
hpm install hemlang/sprout  # Richtig
hpm install hemlan/sprout   # Falscher Owner
hpm install hemlang/spout   # Falscher Repo

# Auf Tippfehler in package.json prüfen
cat package.json | grep -A 5 dependencies
```

### "Version not found" (Exit-Code 3)

**Ursache:** Kein Release entspricht der Versionseinschränkung.

**Lösung:**

```bash
# Verfügbare Versionen auflisten (GitHub-Releases/Tags prüfen)
# Tags müssen mit 'v' beginnen (z.B. v1.0.0)

# Eine gültige Versionseinschränkung verwenden
hpm install owner/repo@^1.0.0

# Neueste Version versuchen
hpm install owner/repo

# Verfügbare Tags auf GitHub prüfen
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (Exit-Code 1)

**Ursache:** Zwei Pakete benötigen inkompatible Versionen einer Abhängigkeit.

**Lösung:**

```bash
# Konflikt anzeigen
hpm install --verbose

# Prüfen, was die Abhängigkeit benötigt
hpm why conflicting/package

# Lösungen:
# 1. Das konfliktverursachende Paket aktualisieren
hpm update problem/package

# 2. Versionseinschränkungen in package.json ändern
# Bearbeiten, um kompatible Versionen zu erlauben

# 3. Eines der konfliktverursachenden Pakete entfernen
hpm uninstall one/package
```

### "Circular dependency" (Exit-Code 8)

**Ursache:** Paket A hängt von B ab, das wiederum von A abhängt.

**Lösung:**

```bash
# Den Zyklus identifizieren
hpm install --verbose

# Dies ist normalerweise ein Bug in den Paketen
# Paket-Maintainer kontaktieren

# Workaround: eines der Pakete vermeiden
```

## Netzwerkprobleme

### "Network error" (Exit-Code 4)

**Ursache:** Keine Verbindung zur GitHub-API möglich.

**Lösung:**

```bash
# Internetverbindung prüfen
ping github.com

# Prüfen, ob GitHub-API erreichbar ist
curl -I https://api.github.com

# Erneut versuchen (hpm wiederholt automatisch)
hpm install

# Offline-Modus verwenden, wenn Pakete gecacht sind
hpm install --offline

# Proxy-Einstellungen prüfen, falls hinter Firewall
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (Exit-Code 7)

**Ursache:** Zu viele API-Anfragen ohne Authentifizierung.

**Lösung:**

```bash
# Option 1: Mit GitHub-Token authentifizieren (empfohlen)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Token erstellen: GitHub → Einstellungen → Entwicklereinstellungen → Personal access tokens

# Option 2: Token in Konfigurationsdatei speichern
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Option 3: Auf Rate-Limit-Reset warten (wird stündlich zurückgesetzt)

# Option 4: Offline-Modus verwenden
hpm install --offline
```

### Verbindungs-Timeout

**Ursache:** Langsames Netzwerk oder GitHub-API-Probleme.

**Lösung:**

```bash
# hpm wiederholt automatisch mit exponentiellem Backoff

# Prüfen, ob GitHub Probleme hat
# Besuchen Sie: https://www.githubstatus.com

# Später erneut versuchen
hpm install

# Gecachte Pakete verwenden
hpm install --offline
```

## Package.json-Probleme

### "Invalid package.json" (Exit-Code 5)

**Ursache:** Fehlerhafte oder fehlende erforderliche Felder.

**Lösung:**

```bash
# JSON-Syntax validieren
cat package.json | python -m json.tool

# Erforderliche Felder prüfen
cat package.json

# Erforderliche Felder:
# - "name": "owner/repo"-Format
# - "version": "X.Y.Z"-Format

# Bei Bedarf neu generieren
rm package.json
hpm init
```

### "name"-Formatfehler

**Ursache:** Paketname nicht im `owner/repo`-Format.

**Lösung:**

```json
// Falsch
{
  "name": "my-package"
}

// Richtig
{
  "name": "yourusername/my-package"
}
```

### "version"-Formatfehler

**Ursache:** Version nicht im Semver-Format.

**Lösung:**

```json
// Falsch
{
  "version": "1.0"
}

// Richtig
{
  "version": "1.0.0"
}
```

## Lock-Datei-Probleme

### Lock-Datei nicht synchron

**Ursache:** package.json geändert ohne install auszuführen.

**Lösung:**

```bash
# Lock-Datei neu generieren
rm package-lock.json
hpm install
```

### Beschädigte Lock-Datei

**Ursache:** Ungültiges JSON oder manuelle Bearbeitungen.

**Lösung:**

```bash
# JSON-Gültigkeit prüfen
cat package-lock.json | python -m json.tool

# Neu generieren
rm package-lock.json
hpm install
```

## hem_modules-Probleme

### Pakete werden nicht installiert

**Ursache:** Verschiedene mögliche Probleme.

**Lösung:**

```bash
# Bereinigen und neu installieren
rm -rf hem_modules
hpm install

# Ausführliche Ausgabe prüfen
hpm install --verbose
```

### Import funktioniert nicht

**Ursache:** Paket nicht korrekt installiert oder falscher Importpfad.

**Lösung:**

```bash
# Überprüfen, ob Paket installiert ist
ls hem_modules/owner/repo/

# main-Feld in package.json prüfen
cat hem_modules/owner/repo/package.json

# Korrektes Import-Format
import { x } from "owner/repo";          # Verwendet main-Eintrag
import { y } from "owner/repo/subpath";  # Unterpfad-Import
```

### "Module not found"-Fehler

**Ursache:** Importpfad löst nicht zu einer Datei auf.

**Lösung:**

```bash
# Importpfad prüfen
ls hem_modules/owner/repo/src/

# Auf index.hml prüfen
ls hem_modules/owner/repo/src/index.hml

# main-Feld in package.json überprüfen
cat hem_modules/owner/repo/package.json | grep main
```

## Cache-Probleme

### Cache belegt zu viel Speicherplatz

**Lösung:**

```bash
# Cache-Größe anzeigen
hpm cache list

# Cache leeren
hpm cache clean
```

### Cache-Berechtigungen

**Lösung:**

```bash
# Berechtigungen reparieren
chmod -R u+rw ~/.hpm/cache

# Oder entfernen und neu installieren
rm -rf ~/.hpm/cache
hpm install
```

### Falschen Cache verwenden

**Lösung:**

```bash
# Cache-Speicherort prüfen
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Umgebungsvariable löschen, falls falsch
unset HPM_CACHE_DIR
```

## Skript-Probleme

### "Script not found"

**Ursache:** Skriptname existiert nicht in package.json.

**Lösung:**

```bash
# Verfügbare Skripte auflisten
cat package.json | grep -A 20 scripts

# Rechtschreibung prüfen
hpm run test    # Richtig
hpm run tests   # Falsch, wenn Skript "test" heißt
```

### Skript schlägt fehl

**Ursache:** Fehler im Skriptbefehl.

**Lösung:**

```bash
# Befehl direkt ausführen, um Fehler zu sehen
hemlock test/run.hml

# Skriptdefinition prüfen
cat package.json | grep test
```

## Debugging

### Ausführliche Ausgabe aktivieren

```bash
hpm install --verbose
```

### hpm-Version prüfen

```bash
hpm --version
```

### Hemlock-Version prüfen

```bash
hemlock --version
```

### Trockenlauf

Vorschau ohne Änderungen:

```bash
hpm install --dry-run
```

### Neuanfang

Frisch starten:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Hilfe erhalten

### Befehlshilfe

```bash
hpm --help
hpm install --help
```

### Probleme melden

Wenn Sie einen Bug finden:

1. Bestehende Issues prüfen: https://github.com/hemlang/hpm/issues
2. Neues Issue erstellen mit:
   - hpm-Version (`hpm --version`)
   - Hemlock-Version (`hemlock --version`)
   - Betriebssystem
   - Schritte zum Reproduzieren
   - Fehlermeldung (mit `--verbose`)

## Exit-Code-Referenz

| Code | Bedeutung | Häufige Lösung |
|------|-----------|----------------|
| 0 | Erfolg | - |
| 1 | Abhängigkeitskonflikt | Aktualisieren oder Einschränkungen ändern |
| 2 | Paket nicht gefunden | Rechtschreibung prüfen, Repo-Existenz verifizieren |
| 3 | Version nicht gefunden | Verfügbare Versionen auf GitHub prüfen |
| 4 | Netzwerkfehler | Verbindung prüfen, erneut versuchen |
| 5 | Ungültige package.json | JSON-Syntax und erforderliche Felder reparieren |
| 6 | Integritätsprüfung fehlgeschlagen | Cache leeren, neu installieren |
| 7 | GitHub-Rate-Limit | GITHUB_TOKEN hinzufügen |
| 8 | Zirkuläre Abhängigkeit | Paket-Maintainer kontaktieren |

## Siehe auch

- [Installation](installation.md) - Installationsanleitung
- [Konfiguration](configuration.md) - Konfigurationsoptionen
- [Befehle](commands.md) - Befehlsreferenz
