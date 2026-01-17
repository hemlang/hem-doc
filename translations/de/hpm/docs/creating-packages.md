# Pakete erstellen

Diese Anleitung behandelt, wie man Hemlock-Pakete erstellt, strukturiert und veröffentlicht.

## Übersicht

hpm verwendet GitHub als Paketregistrierung. Pakete werden durch ihren GitHub-`owner/repo`-Pfad identifiziert, und Versionen sind Git-Tags. Veröffentlichen bedeutet einfach, ein getaggtes Release zu pushen.

## Ein neues Paket erstellen

### 1. Das Paket initialisieren

Ein neues Verzeichnis erstellen und initialisieren:

```bash
mkdir my-package
cd my-package
hpm init
```

Die Eingabeaufforderungen beantworten:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: Ein nützliches Hemlock-Paket
Author: Ihr Name <sie@beispiel.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Die Projektstruktur erstellen

Empfohlene Struktur für Pakete:

```
my-package/
├── package.json          # Paketmanifest
├── README.md             # Dokumentation
├── LICENSE               # Lizenzdatei
├── src/
│   ├── index.hml         # Haupteinstiegspunkt (exportiert öffentliche API)
│   ├── utils.hml         # Interne Hilfsfunktionen
│   └── types.hml         # Typdefinitionen
└── test/
    ├── framework.hml     # Test-Framework
    └── test_utils.hml    # Tests
```

### 3. Ihre öffentliche API definieren

**src/index.hml** - Haupteinstiegspunkt:

```hemlock
// Öffentliche API re-exportieren
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Direkte Exporte
export fn create(options: Options): Config {
    // Implementierung
}

export fn validate(config: Config): bool {
    // Implementierung
}
```

### 4. Ihre package.json schreiben

Vollständiges package.json-Beispiel:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Ein nützliches Hemlock-Paket",
  "author": "Ihr Name <sie@beispiel.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Paketbenennung

### Anforderungen

- Muss im `owner/repo`-Format sein
- `owner` sollte Ihr GitHub-Benutzername oder Ihre Organisation sein
- `repo` sollte der Repository-Name sein
- Kleinbuchstaben mit Bindestrichen für mehrwortige Namen verwenden

### Gute Namen

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### Vermeiden

```
my-package          # Owner fehlt
alice/MyPackage     # PascalCase
alice/my_package    # Unterstriche
```

## Best Practices für Paketstruktur

### Einstiegspunkt

Das `main`-Feld in package.json gibt den Einstiegspunkt an:

```json
{
  "main": "src/index.hml"
}
```

Diese Datei sollte Ihre öffentliche API exportieren:

```hemlock
// Alles exportieren, was Benutzer brauchen
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Typen
export type { Config, Options } from "./types.hml";
```

### Intern vs Öffentlich

Interne Implementierungsdetails privat halten:

```
src/
├── index.hml          # Öffentlich: exportierte API
├── parser.hml         # Öffentlich: von index.hml verwendet
├── formatter.hml      # Öffentlich: von index.hml verwendet
└── internal/
    ├── helpers.hml    # Privat: nur interne Verwendung
    └── constants.hml  # Privat: nur interne Verwendung
```

Benutzer importieren vom Paket-Root:

```hemlock
// Gut - importiert aus öffentlicher API
import { parse, Parser } from "yourusername/my-package";

// Funktioniert auch - Unterpfad-Import
import { validate } from "yourusername/my-package/validator";

// Nicht empfohlen - Zugriff auf Interna
import { helper } from "yourusername/my-package/internal/helpers";
```

### Unterpfad-Exporte

Unterstützung für Importe aus Unterpfaden:

```
src/
├── index.hml              # Haupteinstieg
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Benutzer können importieren:

```hemlock
import { parse } from "yourusername/my-package";           # Haupt
import { Parser } from "yourusername/my-package/parser";   # Unterpfad
import { format } from "yourusername/my-package/formatter";
```

## Abhängigkeiten

### Abhängigkeiten hinzufügen

```bash
# Laufzeitabhängigkeit
hpm install hemlang/json

# Entwicklungsabhängigkeit
hpm install hemlang/test-utils --dev
```

### Best Practices für Abhängigkeiten

1. **Caret-Bereiche verwenden** für die meisten Abhängigkeiten:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Versionen nur bei Bedarf pinnen** (API-Instabilität):
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Zu restriktive Bereiche vermeiden**:
   ```json
   // Schlecht: zu restriktiv
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Gut: erlaubt kompatible Updates
   "hemlang/json": "^1.2.3"
   ```

4. **Dev-Abhängigkeiten getrennt halten**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Ihr Paket testen

### Tests schreiben

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parst gültige Eingabe", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("behandelt leere Eingabe", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifiziert Objekt", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Tests ausführen

Test-Skript hinzufügen:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Ausführen mit:

```bash
hpm test
```

## Veröffentlichen

### Voraussetzungen

1. GitHub-Repository erstellen, das Ihrem Paketnamen entspricht
2. Sicherstellen, dass `package.json` vollständig und gültig ist
3. Alle Tests bestehen

### Veröffentlichungsprozess

Veröffentlichen bedeutet einfach, einen Git-Tag zu pushen:

```bash
# 1. Sicherstellen, dass alles committet ist
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Versions-Tag erstellen (muss mit 'v' beginnen)
git tag v1.0.0

# 3. Code und Tags pushen
git push origin main
git push origin v1.0.0
# Oder alle Tags auf einmal pushen
git push origin main --tags
```

### Versions-Tags

Tags müssen dem Format `vX.Y.Z` folgen:

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Patch
git tag v1.1.0      # Minor
git tag v2.0.0      # Major
git tag v1.0.0-beta.1  # Pre-Release
```

### Release-Checkliste

Vor dem Veröffentlichen einer neuen Version:

1. **Version aktualisieren** in package.json
2. **Tests ausführen**: `hpm test`
3. **CHANGELOG aktualisieren** (falls vorhanden)
4. **README aktualisieren**, falls API geändert
5. **Änderungen committen**
6. **Tag erstellen**
7. **Zu GitHub pushen**

### Automatisiertes Beispiel

Release-Skript erstellen:

```bash
#!/bin/bash
# release.sh - Neue Version veröffentlichen

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Verwendung: ./release.sh 1.0.0"
    exit 1
fi

# Tests ausführen
hpm test || exit 1

# Version in package.json aktualisieren
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Committen und taggen
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Pushen
git push origin main --tags

echo "v$VERSION veröffentlicht"
```

## Benutzer installieren Ihr Paket

Nach der Veröffentlichung können Benutzer installieren:

```bash
# Neueste Version
hpm install yourusername/my-package

# Bestimmte Version
hpm install yourusername/my-package@1.0.0

# Versionseinschränkung
hpm install yourusername/my-package@^1.0.0
```

Und importieren:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Dokumentation

### README.md

Jedes Paket sollte eine README haben:

```markdown
# my-package

Eine kurze Beschreibung, was dieses Paket tut.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Verwendung

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Parst die Eingabezeichenkette.

### stringify(obj: any): string

Konvertiert Objekt in Zeichenkette.

## Lizenz

MIT
```

### API-Dokumentation

Alle öffentlichen Exporte dokumentieren:

```hemlock
/// Parst die Eingabezeichenkette in ein strukturiertes Result.
///
/// # Argumente
/// * `input` - Die zu parsende Zeichenkette
///
/// # Rückgabe
/// Ein Result mit den geparsten Daten oder einem Fehler
///
/// # Beispiel
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementierung
}
```

## Versionierungsrichtlinien

Folgen Sie [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking Changes
- **MINOR** (1.0.0 → 1.1.0): Neue Features, abwärtskompatibel
- **PATCH** (1.0.0 → 1.0.1): Bugfixes, abwärtskompatibel

### Wann erhöhen

| Änderungstyp | Versionsbump |
|--------------|--------------|
| Breaking API-Änderung | MAJOR |
| Funktion/Typ entfernen | MAJOR |
| Funktionssignatur ändern | MAJOR |
| Neue Funktion hinzufügen | MINOR |
| Neues Feature hinzufügen | MINOR |
| Bugfix | PATCH |
| Dokumentations-Update | PATCH |
| Internes Refactoring | PATCH |

## Siehe auch

- [Paketspezifikation](package-spec.md) - Vollständige package.json-Referenz
- [Versionierung](versioning.md) - Details zur semantischen Versionierung
- [Konfiguration](configuration.md) - GitHub-Authentifizierung
