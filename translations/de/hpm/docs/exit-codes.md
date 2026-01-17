# Exit-Codes

Referenz für hpm-Exit-Codes und ihre Bedeutungen.

## Exit-Code-Tabelle

| Code | Name | Beschreibung |
|------|------|--------------|
| 0 | SUCCESS | Befehl erfolgreich abgeschlossen |
| 1 | CONFLICT | Abhängigkeits-Versionskonflikt |
| 2 | NOT_FOUND | Paket nicht gefunden |
| 3 | VERSION_NOT_FOUND | Angeforderte Version nicht gefunden |
| 4 | NETWORK | Netzwerkfehler |
| 5 | INVALID_MANIFEST | Ungültige package.json |
| 6 | INTEGRITY | Integritätsprüfung fehlgeschlagen |
| 7 | RATE_LIMIT | GitHub-API-Rate-Limit überschritten |
| 8 | CIRCULAR | Zirkuläre Abhängigkeit erkannt |

## Detaillierte Beschreibungen

### Exit-Code 0: SUCCESS

Der Befehl wurde erfolgreich abgeschlossen.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Exit-Code 1: CONFLICT

Zwei oder mehr Pakete erfordern inkompatible Versionen einer Abhängigkeit.

**Beispiel:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Lösungen:**
1. Prüfen, welche Pakete den Konflikt haben:
   ```bash
   hpm why hemlang/json
   ```
2. Das konfliktverursachende Paket aktualisieren:
   ```bash
   hpm update package-a
   ```
3. Versionseinschränkungen in package.json lockern
4. Eines der konfliktverursachenden Pakete entfernen

### Exit-Code 2: NOT_FOUND

Das angegebene Paket existiert nicht auf GitHub.

**Beispiel:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Lösungen:**
1. Paketnamen-Schreibweise überprüfen
2. Prüfen, ob Repository existiert: `https://github.com/owner/repo`
3. Überprüfen, ob Sie Zugriff haben (für private Repos, GITHUB_TOKEN setzen)

### Exit-Code 3: VERSION_NOT_FOUND

Keine Version entspricht der angegebenen Einschränkung.

**Beispiel:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Lösungen:**
1. Verfügbare Versionen auf GitHub-Releases/Tags prüfen
2. Eine gültige Versionseinschränkung verwenden
3. Versions-Tags müssen mit 'v' beginnen (z.B. `v1.0.0`)

### Exit-Code 4: NETWORK

Ein netzwerkbezogener Fehler ist aufgetreten.

**Beispiel:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Lösungen:**
1. Internetverbindung prüfen
2. Prüfen, ob GitHub erreichbar ist
3. Proxy-Einstellungen überprüfen, falls hinter Firewall
4. `--offline` verwenden, wenn Pakete gecacht sind:
   ```bash
   hpm install --offline
   ```
5. Warten und erneut versuchen (hpm wiederholt automatisch)

### Exit-Code 5: INVALID_MANIFEST

Die package.json-Datei ist ungültig oder fehlerhaft.

**Beispiel:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Lösungen:**
1. JSON-Syntax prüfen (JSON-Validator verwenden)
2. Sicherstellen, dass erforderliche Felder existieren (`name`, `version`)
3. Feldformate überprüfen:
   - name: `owner/repo`-Format
   - version: `X.Y.Z` Semver-Format
4. Neu generieren:
   ```bash
   rm package.json
   hpm init
   ```

### Exit-Code 6: INTEGRITY

Paket-Integritätsverifikation fehlgeschlagen.

**Beispiel:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Lösungen:**
1. Cache leeren und neu installieren:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Auf Netzwerkprobleme prüfen (unvollständige Downloads)
3. Überprüfen, ob das Paket manipuliert wurde

### Exit-Code 7: RATE_LIMIT

GitHub-API-Rate-Limit wurde überschritten.

**Beispiel:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Lösungen:**
1. **Mit GitHub authentifizieren** (empfohlen):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Auf Rate-Limit-Reset warten (wird stündlich zurückgesetzt)
3. Offline-Modus verwenden, wenn Pakete gecacht sind:
   ```bash
   hpm install --offline
   ```

### Exit-Code 8: CIRCULAR

Zirkuläre Abhängigkeit im Abhängigkeitsgraphen erkannt.

**Beispiel:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (zirkulär!)

Cannot resolve dependency tree.
```

**Lösungen:**
1. Dies ist normalerweise ein Bug in den Paketen selbst
2. Paket-Maintainer kontaktieren
3. Eines der zirkulären Pakete nicht verwenden

## Exit-Codes in Skripten verwenden

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation erfolgreich"
    ;;
  1)
    echo "Abhängigkeitskonflikt - Versionseinschränkungen prüfen"
    exit 1
    ;;
  2)
    echo "Paket nicht gefunden - Paketnamen prüfen"
    exit 1
    ;;
  4)
    echo "Netzwerkfehler - Verbindung prüfen"
    exit 1
    ;;
  7)
    echo "Rate-limitiert - GITHUB_TOKEN setzen"
    exit 1
    ;;
  *)
    echo "Unbekannter Fehler: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Abhängigkeiten installieren
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub-Rate-Limit überschritten. GITHUB_TOKEN hinzufügen."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation fehlgeschlagen mit Code $$?"; exit 1)

test: install
	@hpm test
```

## Fehlerbehebung nach Exit-Code

### Kurzreferenz

| Code | Zuerst prüfen |
|------|---------------|
| 1 | `hpm why <package>` ausführen, um Konflikt zu sehen |
| 2 | Paketnamen auf GitHub überprüfen |
| 3 | Verfügbare Versionen auf GitHub-Tags prüfen |
| 4 | Internetverbindung prüfen |
| 5 | package.json-Syntax validieren |
| 6 | `hpm cache clean && hpm install` ausführen |
| 7 | `GITHUB_TOKEN`-Umgebungsvariable setzen |
| 8 | Paket-Maintainer kontaktieren |

## Siehe auch

- [Fehlerbehebung](troubleshooting.md) - Detaillierte Lösungen
- [Befehle](commands.md) - Befehlsreferenz
- [Konfiguration](configuration.md) - GitHub-Token einrichten
