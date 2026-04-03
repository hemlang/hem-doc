# hpm Dokumentation

Willkommen bei der Dokumentation von hpm (Hemlock Package Manager). hpm ist der offizielle Paketmanager für die Programmiersprache [Hemlock](https://github.com/hemlang/hemlock).

## Überblick

hpm verwendet GitHub als Paketregister, wobei Pakete über ihren GitHub-Repository-Pfad identifiziert werden (z. B. `hemlang/sprout`). Das bedeutet:

- **Kein zentrales Register** - Pakete befinden sich in GitHub-Repositories
- **Versions-Tags** - Releases sind Git-Tags (z. B. `v1.0.0`)
- **Veröffentlichen ist einfach Git** - einen Tag pushen, um eine neue Version zu veröffentlichen

## Dokumentation

### Erste Schritte

- [Installation](installation.md) - So installieren Sie hpm
- [Schnellstart](quick-start.md) - In 5 Minuten startklar
- [Projekteinrichtung](project-setup.md) - Ein neues Hemlock-Projekt einrichten

### Benutzerhandbuch

- [Befehlsreferenz](commands.md) - Vollständige Referenz aller hpm-Befehle
- [Konfiguration](configuration.md) - Konfigurationsdateien und Umgebungsvariablen
- [Fehlerbehebung](troubleshooting.md) - Häufige Probleme und Lösungen

### Paketentwicklung

- [Pakete erstellen](creating-packages.md) - So erstellen und veröffentlichen Sie Pakete
- [Paketspezifikation](package-spec.md) - Das package.json-Format
- [Versionierung](versioning.md) - Semantische Versionierung und Versionseinschränkungen

### Referenz

- [Architektur](architecture.md) - Interne Architektur und Design
- [Exit-Codes](exit-codes.md) - Referenz der CLI-Exit-Codes

## Kurzreferenz

### Grundlegende Befehle

```bash
hpm init                              # Neue package.json erstellen
hpm install                           # Alle Abhängigkeiten installieren
hpm install owner/repo                # Ein Paket hinzufügen und installieren
hpm install owner/repo@^1.0.0        # Mit Versionseinschränkung installieren
hpm uninstall owner/repo              # Ein Paket entfernen
hpm update                            # Alle Pakete aktualisieren
hpm list                              # Installierte Pakete anzeigen
hpm run <script>                      # Ein Paketskript ausführen
```

### Paketidentifikation

Pakete verwenden das GitHub-Format `owner/repo`:

```
hemlang/sprout          # Web-Framework
hemlang/json            # JSON-Hilfsprogramme
alice/http-client       # HTTP-Client-Bibliothek
```

### Versionseinschränkungen

| Syntax | Bedeutung |
|--------|-----------|
| `1.0.0` | Exakte Version |
| `^1.2.3` | Kompatibel (>=1.2.3 <2.0.0) |
| `~1.2.3` | Patch-Updates (>=1.2.3 <1.3.0) |
| `>=1.0.0` | Mindestens 1.0.0 |
| `*` | Beliebige Version |

## Hilfe erhalten

- Verwenden Sie `hpm --help` für die Befehlszeilenhilfe
- Verwenden Sie `hpm <command> --help` für befehlsspezifische Hilfe
- Melden Sie Probleme unter [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## Lizenz

hpm wird unter der MIT-Lizenz veröffentlicht.
