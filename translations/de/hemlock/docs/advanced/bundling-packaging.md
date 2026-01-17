# Bundling & Paketierung

Hemlock bietet eingebaute Werkzeuge, um Multi-Datei-Projekte in einzelne verteilbare Dateien zu bündeln und eigenständige ausführbare Dateien zu erstellen.

## Überblick

| Befehl | Ausgabe | Anwendungsfall |
|--------|---------|----------------|
| `--bundle` | `.hmlc` oder `.hmlb` | Bytecode verteilen (erfordert Hemlock zur Ausführung) |
| `--package` | Ausführbare Datei | Eigenständige Binärdatei (keine Abhängigkeiten) |
| `--compile` | `.hmlc` | Einzelne Datei kompilieren (keine Import-Auflösung) |

## Bundling

Der Bundler löst alle `import`-Anweisungen von einem Einstiegspunkt auf und flacht sie in eine einzelne Datei ab.

### Grundlegende Verwendung

```bash
# app.hml und alle Imports in app.hmlc bündeln
hemlock --bundle app.hml

# Ausgabepfad angeben
hemlock --bundle app.hml -o dist/app.hmlc

# Komprimiertes Bundle erstellen (.hmlb) - kleinere Dateigröße
hemlock --bundle app.hml --compress -o app.hmlb

# Ausführliche Ausgabe (zeigt aufgelöste Module)
hemlock --bundle app.hml --verbose
```

### Ausgabeformate

**`.hmlc` (Unkomprimiert)**
- Serialisiertes AST-Format
- Schnell zu laden und auszuführen
- Standard-Ausgabeformat

**`.hmlb` (Komprimiert)**
- zlib-komprimiertes `.hmlc`
- Kleinere Dateigröße (typischerweise 50-70% Reduktion)
- Etwas langsamerer Start durch Dekomprimierung

### Gebündelte Dateien ausführen

```bash
# Unkomprimiertes Bundle ausführen
hemlock app.hmlc

# Komprimiertes Bundle ausführen
hemlock app.hmlb

# Argumente übergeben
hemlock app.hmlc arg1 arg2
```

### Beispiel: Multi-Modul-Projekt

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # Läuft mit allen gebündelten Abhängigkeiten
```

### stdlib-Imports

Der Bundler löst automatisch `@stdlib/`-Imports auf:

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

Beim Bündeln werden stdlib-Module in die Ausgabe einbezogen.

## Paketierung

Paketierung erstellt eine eigenständige ausführbare Datei, indem der gebündelte Bytecode in eine Kopie des Hemlock-Interpreters eingebettet wird.

### Grundlegende Verwendung

```bash
# Ausführbare Datei aus app.hml erstellen
hemlock --package app.hml

# Ausgabenamen angeben
hemlock --package app.hml -o myapp

# Komprimierung überspringen (schnellerer Start, größere Datei)
hemlock --package app.hml --no-compress

# Ausführliche Ausgabe
hemlock --package app.hml --verbose
```

### Paketierte ausführbare Dateien ausführen

```bash
# Die paketierte ausführbare Datei läuft direkt
./myapp

# Argumente werden an das Skript übergeben
./myapp arg1 arg2
```

### Paketformat

Paketierte ausführbare Dateien verwenden das HMLP-Format:

```
[hemlock binary][HMLB/HMLC payload][payload_size:u64][HMLP magic:u32]
```

Wenn eine paketierte ausführbare Datei läuft:
1. Sie prüft auf ein eingebettetes Payload am Ende der Datei
2. Falls gefunden, dekomprimiert und führt sie das Payload aus
3. Falls nicht gefunden, verhält sie sich wie ein normaler Hemlock-Interpreter

### Komprimierungsoptionen

| Flag | Format | Start | Größe |
|------|--------|-------|-------|
| (Standard) | HMLB | Normal | Kleiner |
| `--no-compress` | HMLC | Schneller | Größer |

Für CLI-Tools, bei denen Startzeit wichtig ist, verwenden Sie `--no-compress`.

## Bundles inspizieren

Verwenden Sie `--info`, um gebündelte oder kompilierte Dateien zu inspizieren:

```bash
hemlock --info app.hmlc
```

Ausgabe:
```
=== Datei-Info: app.hmlc ===
Größe: 12847 Bytes
Format: HMLC (kompilierter AST)
Version: 1
Flags: 0x0001 [DEBUG]
Strings: 42
Anweisungen: 156
```

```bash
hemlock --info app.hmlb
```

Ausgabe:
```
=== Datei-Info: app.hmlb ===
Größe: 5234 Bytes
Format: HMLB (komprimiertes Bundle)
Version: 1
Unkomprimiert: 12847 Bytes
Komprimiert: 5224 Bytes
Verhältnis: 59,3% Reduktion
```

## Native Kompilierung

Für echte native ausführbare Dateien (kein Interpreter) verwenden Sie den Hemlock-Compiler:

```bash
# Zu nativer ausführbarer Datei über C kompilieren
hemlockc app.hml -o app

# Generierten C-Code behalten
hemlockc app.hml -o app --keep-c

# Nur C ausgeben (nicht kompilieren)
hemlockc app.hml -c -o app.c

# Optimierungsstufe
hemlockc app.hml -o app -O2
```

Der Compiler generiert C-Code und ruft GCC auf, um eine native Binärdatei zu erzeugen. Dies erfordert:
- Die Hemlock-Laufzeitbibliothek (`libhemlock_runtime`)
- Einen C-Compiler (standardmäßig GCC)

### Compiler-Optionen

| Option | Beschreibung |
|--------|--------------|
| `-o <file>` | Name der ausführbaren Ausgabedatei |
| `-c` | Nur C-Code ausgeben |
| `--emit-c <file>` | C in angegebene Datei schreiben |
| `-k, --keep-c` | Generierten C-Code nach Kompilierung behalten |
| `-O<level>` | Optimierungsstufe (0-3) |
| `--cc <path>` | Zu verwendender C-Compiler |
| `--runtime <path>` | Pfad zur Laufzeitbibliothek |
| `-v, --verbose` | Ausführliche Ausgabe |

## Vergleich

| Ansatz | Portabilität | Start | Größe | Abhängigkeiten |
|--------|--------------|-------|-------|----------------|
| `.hml` | Nur Quellcode | Parse-Zeit | Kleinste | Hemlock |
| `.hmlc` | Nur Hemlock | Schnell | Klein | Hemlock |
| `.hmlb` | Nur Hemlock | Schnell | Kleiner | Hemlock |
| `--package` | Eigenständig | Schnell | Größer | Keine |
| `hemlockc` | Nativ | Schnellste | Variiert | Laufzeit-Libs |

## Best Practices

1. **Entwicklung**: `.hml`-Dateien direkt ausführen für schnelle Iteration
2. **Verteilung (mit Hemlock)**: Mit `--compress` für kleinere Dateien bündeln
3. **Verteilung (eigenständig)**: Paketieren für Deployment ohne Abhängigkeiten
4. **Leistungskritisch**: `hemlockc` für native Kompilierung verwenden

## Fehlerbehebung

### "Cannot find stdlib"

Der Bundler sucht nach stdlib in:
1. `./stdlib` (relativ zur ausführbaren Datei)
2. `../stdlib` (relativ zur ausführbaren Datei)
3. `/usr/local/lib/hemlock/stdlib`

Stellen Sie sicher, dass Hemlock ordnungsgemäß installiert ist oder führen Sie es aus dem Quellverzeichnis aus.

### Zirkuläre Abhängigkeiten

```
Fehler: Zirkuläre Abhängigkeit beim Laden von 'path/to/module.hml' erkannt
```

Refaktorieren Sie Ihre Imports, um den Zyklus zu durchbrechen. Erwägen Sie die Verwendung eines gemeinsamen Moduls für gemeinsame Typen.

### Große Paketgröße

- Verwenden Sie die Standardkomprimierung (verwenden Sie nicht `--no-compress`)
- Die paketierte Größe beinhaltet den vollständigen Interpreter (~500KB-1MB Basis)
- Für minimale Größe verwenden Sie `hemlockc` für native Kompilierung
