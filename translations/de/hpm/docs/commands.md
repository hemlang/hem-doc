# Befehlsreferenz

Vollständige Referenz für alle hpm-Befehle.

## Globale Optionen

Diese Optionen funktionieren mit jedem Befehl:

| Option | Beschreibung |
|--------|--------------|
| `--help`, `-h` | Hilfemeldung anzeigen |
| `--version`, `-v` | hpm-Version anzeigen |
| `--verbose` | Detaillierte Ausgabe anzeigen |

## Befehle

### hpm init

Erstellt eine neue `package.json`-Datei.

```bash
hpm init        # Interaktiver Modus
hpm init --yes  # Alle Standardwerte akzeptieren
hpm init -y     # Kurzform
```

**Optionen:**

| Option | Beschreibung |
|--------|--------------|
| `--yes`, `-y` | Standardwerte für alle Eingabeaufforderungen akzeptieren |

**Interaktive Eingabeaufforderungen:**
- Paketname (owner/repo-Format)
- Version (Standard: 1.0.0)
- Beschreibung
- Autor
- Lizenz (Standard: MIT)
- Hauptdatei (Standard: src/index.hml)

**Beispiel:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: Eine Hilfsbibliothek
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Abhängigkeiten installieren oder neue Pakete hinzufügen.

```bash
hpm install                           # Alle aus package.json installieren
hpm install owner/repo                # Paket hinzufügen und installieren
hpm install owner/repo@^1.0.0        # Mit Versionseinschränkung
hpm install owner/repo --dev         # Als Entwicklungsabhängigkeit
hpm i owner/repo                      # Kurzform
```

**Optionen:**

| Option | Beschreibung |
|--------|--------------|
| `--dev`, `-D` | Zu devDependencies hinzufügen |
| `--verbose` | Detaillierten Fortschritt anzeigen |
| `--dry-run` | Vorschau ohne Installation |
| `--offline` | Nur aus dem Cache installieren (kein Netzwerk) |
| `--parallel` | Parallele Downloads aktivieren (experimentell) |

**Syntax für Versionseinschränkungen:**

| Syntax | Beispiel | Bedeutung |
|--------|----------|-----------|
| (keine) | `owner/repo` | Neueste Version |
| Exakt | `owner/repo@1.2.3` | Genau 1.2.3 |
| Caret | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Bereich | `owner/repo@>=1.0.0` | Mindestens 1.0.0 |

**Beispiele:**

```bash
# Alle Abhängigkeiten installieren
hpm install

# Bestimmtes Paket installieren
hpm install hemlang/json

# Mit Versionseinschränkung installieren
hpm install hemlang/sprout@^2.0.0

# Als Entwicklungsabhängigkeit installieren
hpm install hemlang/test-utils --dev

# Vorschau, was installiert werden würde
hpm install hemlang/sprout --dry-run

# Ausführliche Ausgabe
hpm install --verbose

# Nur aus dem Cache installieren (offline)
hpm install --offline
```

**Ausgabe:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (Abhängigkeit von hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Ein Paket entfernen.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Kurzform
hpm remove owner/repo      # Alternative
```

**Beispiele:**

```bash
hpm uninstall hemlang/sprout
```

**Ausgabe:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Pakete auf die neuesten Versionen innerhalb der Einschränkungen aktualisieren.

```bash
hpm update              # Alle Pakete aktualisieren
hpm update owner/repo   # Bestimmtes Paket aktualisieren
hpm up owner/repo       # Kurzform
```

**Optionen:**

| Option | Beschreibung |
|--------|--------------|
| `--verbose` | Detaillierten Fortschritt anzeigen |
| `--dry-run` | Vorschau ohne Aktualisierung |

**Beispiele:**

```bash
# Alle Pakete aktualisieren
hpm update

# Bestimmtes Paket aktualisieren
hpm update hemlang/sprout

# Aktualisierungen vorab anzeigen
hpm update --dry-run
```

**Ausgabe:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Installierte Pakete anzeigen.

```bash
hpm list              # Vollständigen Abhängigkeitsbaum anzeigen
hpm list --depth=0    # Nur direkte Abhängigkeiten
hpm list --depth=1    # Eine Ebene transitiver Abhängigkeiten
hpm ls                # Kurzform
```

**Optionen:**

| Option | Beschreibung |
|--------|--------------|
| `--depth=N` | Baumtiefe begrenzen (Standard: alle) |

**Beispiele:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Pakete mit neueren verfügbaren Versionen anzeigen.

```bash
hpm outdated
```

**Ausgabe:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: Installierte Version
- **Wanted**: Höchste Version, die der Einschränkung entspricht
- **Latest**: Neueste verfügbare Version

---

### hpm run

Ein Skript aus package.json ausführen.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Beispiele:**

Bei dieser package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Skripte ausführen:

```bash
hpm run start
hpm run test
hpm run build

# Argumente an das Skript übergeben
hpm run test -- --verbose
```

---

### hpm test

Kurzform für `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Entspricht:

```bash
hpm run test
```

---

### hpm why

Erklären, warum ein Paket installiert ist (Abhängigkeitskette anzeigen).

```bash
hpm why owner/repo
```

**Beispiel:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 ist installiert, weil:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Den globalen Paket-Cache verwalten.

```bash
hpm cache list    # Gecachte Pakete auflisten
hpm cache clean   # Alle gecachten Pakete löschen
```

**Unterbefehle:**

| Unterbefehl | Beschreibung |
|-------------|--------------|
| `list` | Alle gecachten Pakete und Größen anzeigen |
| `clean` | Alle gecachten Pakete entfernen |

**Beispiele:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Befehlskürzel

Der Einfachheit halber haben mehrere Befehle kurze Aliase:

| Befehl | Kürzel |
|--------|--------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Beispiele:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Exit-Codes

hpm verwendet spezifische Exit-Codes, um verschiedene Fehlerbedingungen anzuzeigen:

| Code | Bedeutung |
|------|-----------|
| 0 | Erfolg |
| 1 | Abhängigkeitskonflikt |
| 2 | Paket nicht gefunden |
| 3 | Version nicht gefunden |
| 4 | Netzwerkfehler |
| 5 | Ungültige package.json |
| 6 | Integritätsprüfung fehlgeschlagen |
| 7 | GitHub-Rate-Limit überschritten |
| 8 | Zirkuläre Abhängigkeit |

Exit-Codes in Skripten verwenden:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation fehlgeschlagen"
    exit 1
fi
```

---

## Umgebungsvariablen

hpm berücksichtigt diese Umgebungsvariablen:

| Variable | Beschreibung |
|----------|--------------|
| `GITHUB_TOKEN` | GitHub-API-Token für Authentifizierung |
| `HPM_CACHE_DIR` | Cache-Verzeichnis überschreiben |
| `HOME` | Benutzer-Home-Verzeichnis (für Konfiguration/Cache) |

**Beispiele:**

```bash
# GitHub-Token für höhere Rate-Limits verwenden
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Benutzerdefiniertes Cache-Verzeichnis verwenden
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## Siehe auch

- [Konfiguration](configuration.md) - Konfigurationsdateien
- [Paketspezifikation](package-spec.md) - package.json-Format
- [Fehlerbehebung](troubleshooting.md) - Häufige Probleme
