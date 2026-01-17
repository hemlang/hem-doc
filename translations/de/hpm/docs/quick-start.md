# Schnellstart

Starten Sie mit hpm in 5 Minuten.

## hpm installieren

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Für weitere Installationsoptionen siehe die [Installationsanleitung](installation.md).

## Ein neues Projekt erstellen

Beginnen Sie mit dem Erstellen eines neuen Verzeichnisses und der Initialisierung eines Pakets:

```bash
mkdir my-project
cd my-project
hpm init
```

Sie werden nach Projektdetails gefragt:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: Mein tolles Hemlock-Projekt
Author: Ihr Name <sie@beispiel.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Verwenden Sie `--yes`, um alle Standardwerte zu akzeptieren:

```bash
hpm init --yes
```

## Projektstruktur

Erstellen Sie die grundlegende Projektstruktur:

```
my-project/
├── package.json        # Projektmanifest
├── src/
│   └── index.hml      # Haupteinstiegspunkt
└── test/
    └── test.hml       # Tests
```

Erstellen Sie Ihre Hauptdatei:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Haupteinstiegspunkt
export fn greet(name: string): string {
    return "Hallo, " + name + "!";
}

export fn main() {
    print(greet("Welt"));
}
```

## Abhängigkeiten installieren

Suchen Sie nach Paketen auf GitHub (Pakete verwenden das `owner/repo`-Format):

```bash
# Ein Paket installieren
hpm install hemlang/sprout

# Mit Versionseinschränkung installieren
hpm install hemlang/json@^1.0.0

# Als Entwicklungsabhängigkeit installieren
hpm install hemlang/test-utils --dev
```

Nach der Installation enthält Ihre Projektstruktur `hem_modules/`:

```
my-project/
├── package.json
├── package-lock.json   # Lock-Datei (automatisch generiert)
├── hem_modules/        # Installierte Pakete
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Installierte Pakete verwenden

Importieren Sie Pakete mit ihrem GitHub-Pfad:

```hemlock
// Aus installiertem Paket importieren
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Aus Unterpfad importieren
import { middleware } from "hemlang/sprout/middleware";

// Standardbibliothek (eingebaut)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Skripte hinzufügen

Fügen Sie Skripte zu Ihrer `package.json` hinzu:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Führen Sie Skripte mit `hpm run` aus:

```bash
hpm run start
hpm run build

# Kurzform für test
hpm test
```

## Häufige Arbeitsabläufe

### Alle Abhängigkeiten installieren

Wenn Sie ein Projekt mit einer `package.json` klonen:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Abhängigkeiten aktualisieren

Alle Pakete auf die neuesten Versionen innerhalb der Einschränkungen aktualisieren:

```bash
hpm update
```

Ein bestimmtes Paket aktualisieren:

```bash
hpm update hemlang/sprout
```

### Installierte Pakete anzeigen

Alle installierten Pakete auflisten:

```bash
hpm list
```

Die Ausgabe zeigt den Abhängigkeitsbaum:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Nach Updates suchen

Sehen Sie, welche Pakete neuere Versionen haben:

```bash
hpm outdated
```

### Ein Paket entfernen

```bash
hpm uninstall hemlang/sprout
```

## Beispiel: Webanwendung

Hier ist ein vollständiges Beispiel mit einem Web-Framework:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "Eine Webanwendung",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hallo, Welt!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server läuft auf http://localhost:3000");
}
```

Führen Sie die Anwendung aus:

```bash
hpm install
hpm run start
```

## Nächste Schritte

- [Befehlsreferenz](commands.md) - Lernen Sie alle hpm-Befehle
- [Pakete erstellen](creating-packages.md) - Veröffentlichen Sie Ihre eigenen Pakete
- [Konfiguration](configuration.md) - hpm und GitHub-Tokens konfigurieren
- [Projekteinrichtung](project-setup.md) - Detaillierte Projektkonfiguration
