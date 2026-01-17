# Installation

Diese Anleitung beschreibt, wie Sie hpm auf Ihrem System installieren.

## Schnellinstallation (Empfohlen)

Installieren Sie die neueste Version mit einem einzigen Befehl:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Dies geschieht automatisch:
- Erkennung Ihres Betriebssystems (Linux, macOS)
- Erkennung Ihrer Architektur (x86_64, arm64)
- Herunterladen der passenden vorkompilierten Binärdatei
- Installation nach `/usr/local/bin` (oder mit sudo falls erforderlich)

### Installationsoptionen

```bash
# An einem benutzerdefinierten Ort installieren (kein sudo erforderlich)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Eine bestimmte Version installieren
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Optionen kombinieren
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Unterstützte Plattformen

| Plattform | Architektur | Status |
|-----------|-------------|--------|
| Linux     | x86_64      | ✓ Unterstützt |
| macOS     | x86_64      | ✓ Unterstützt |
| macOS     | arm64 (M1/M2/M3) | ✓ Unterstützt |
| Linux     | arm64       | Aus Quellcode bauen |

## Aus Quellcode bauen

Wenn Sie lieber aus dem Quellcode bauen möchten oder eine Plattform benötigen, die nicht durch vorkompilierte Binärdateien abgedeckt ist, folgen Sie diesen Anweisungen.

### Voraussetzungen

hpm erfordert, dass [Hemlock](https://github.com/hemlang/hemlock) zuerst installiert wird. Folgen Sie den Hemlock-Installationsanweisungen, bevor Sie fortfahren.

Überprüfen Sie, ob Hemlock installiert ist:

```bash
hemlock --version
```

## Installationsmethoden

### Methode 1: Make Install

Aus dem Quellcode bauen und installieren.

```bash
# Repository klonen
git clone https://github.com/hemlang/hpm.git
cd hpm

# Nach /usr/local/bin installieren (erfordert sudo)
sudo make install
```

Nach der Installation überprüfen Sie, ob es funktioniert:

```bash
hpm --version
```

### Methode 2: Benutzerdefinierter Speicherort

An einem benutzerdefinierten Verzeichnis installieren (kein sudo erforderlich):

```bash
# Repository klonen
git clone https://github.com/hemlang/hpm.git
cd hpm

# Nach ~/.local/bin installieren
make install PREFIX=$HOME/.local

# Oder an einem beliebigen benutzerdefinierten Ort
make install PREFIX=/opt/hemlock
```

Stellen Sie sicher, dass Ihr benutzerdefiniertes bin-Verzeichnis in Ihrem PATH ist:

```bash
# Zu ~/.bashrc oder ~/.zshrc hinzufügen
export PATH="$HOME/.local/bin:$PATH"
```

### Methode 3: Ohne Installation ausführen

Sie können hpm direkt ohne Installation ausführen:

```bash
# Repository klonen
git clone https://github.com/hemlang/hpm.git
cd hpm

# Lokales Wrapper-Skript erstellen
make

# Aus dem hpm-Verzeichnis ausführen
./hpm --help

# Oder direkt über hemlock ausführen
hemlock src/main.hml --help
```

### Methode 4: Manuelle Installation

Erstellen Sie Ihr eigenes Wrapper-Skript:

```bash
# An einen permanenten Ort klonen
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Wrapper-Skript erstellen
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Installationsvariablen

Das Makefile unterstützt diese Variablen:

| Variable | Standard | Beschreibung |
|----------|----------|--------------|
| `PREFIX` | `/usr/local` | Installationspräfix |
| `BINDIR` | `$(PREFIX)/bin` | Binärverzeichnis |
| `HEMLOCK` | `hemlock` | Pfad zum Hemlock-Interpreter |

Beispiel mit benutzerdefinierten Variablen:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Funktionsweise

Der Installer erstellt ein Shell-Wrapper-Skript, das den Hemlock-Interpreter mit dem hpm-Quellcode aufruft:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

Dieser Ansatz:
- Erfordert keine Kompilierung
- Führt immer den neuesten Quellcode aus
- Funktioniert zuverlässig auf allen Plattformen

## hpm aktualisieren

Um hpm auf die neueste Version zu aktualisieren:

```bash
cd /path/to/hpm
git pull origin main

# Bei Pfadänderung neu installieren
sudo make install
```

## Deinstallation

hpm von Ihrem System entfernen:

```bash
cd /path/to/hpm
sudo make uninstall
```

Oder manuell entfernen:

```bash
sudo rm /usr/local/bin/hpm
```

## Installation überprüfen

Nach der Installation überprüfen Sie, ob alles funktioniert:

```bash
# Version prüfen
hpm --version

# Hilfe anzeigen
hpm --help

# Initialisierung testen (in einem leeren Verzeichnis)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Fehlerbehebung

### "hemlock: command not found"

Hemlock ist nicht installiert oder nicht in Ihrem PATH. Installieren Sie zuerst Hemlock:

```bash
# Prüfen, ob hemlock existiert
which hemlock

# Falls nicht gefunden, Hemlock von https://github.com/hemlang/hemlock installieren
```

### "Permission denied"

Verwenden Sie sudo für die systemweite Installation oder installieren Sie in einem Benutzerverzeichnis:

```bash
# Option 1: sudo verwenden
sudo make install

# Option 2: In Benutzerverzeichnis installieren
make install PREFIX=$HOME/.local
```

### "hpm: command not found" nach der Installation

Ihr PATH enthält möglicherweise nicht das Installationsverzeichnis:

```bash
# Prüfen, wo hpm installiert wurde
ls -la /usr/local/bin/hpm

# Zum PATH hinzufügen, wenn benutzerdefinierter Speicherort verwendet wird
export PATH="$HOME/.local/bin:$PATH"
```

## Plattformspezifische Hinweise

### Linux

Die Standardinstallation funktioniert auf allen Linux-Distributionen. Einige Distributionen erfordern möglicherweise:

```bash
# Debian/Ubuntu: Build-Essentials sicherstellen
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

Die Standardinstallation funktioniert. Bei Verwendung von Homebrew:

```bash
# Xcode-Kommandozeilentools sicherstellen
xcode-select --install
```

### Windows (WSL)

hpm funktioniert im Windows Subsystem for Linux:

```bash
# Im WSL-Terminal
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Nächste Schritte

Nach der Installation:

1. [Schnellstart](quick-start.md) - Erstellen Sie Ihr erstes Projekt
2. [Befehlsreferenz](commands.md) - Lernen Sie alle Befehle
3. [Konfiguration](configuration.md) - hpm konfigurieren
