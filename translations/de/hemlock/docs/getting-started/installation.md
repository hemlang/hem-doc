# Installation

Diese Anleitung hilft Ihnen bei der Installation von Hemlock auf Ihrem System.

## Schnellinstallation (Empfohlen)

Der einfachste Weg, Hemlock zu installieren, ist das einzeilige Installationsskript:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Dies lädt die neueste vorkompilierte Binärdatei für Ihre Plattform herunter und installiert sie (Linux oder macOS, x86_64 oder arm64).

### Installationsoptionen

```bash
# Installation in ein benutzerdefiniertes Präfix (Standard: ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Installation einer bestimmten Version
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Installation und automatische Aktualisierung des Shell-PATH
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

Nach der Installation überprüfen Sie die Funktionsfähigkeit:

```bash
hemlock --version
```

---

## Aus dem Quellcode kompilieren

Wenn Sie lieber aus dem Quellcode kompilieren möchten oder die vorkompilierten Binärdateien für Ihr System nicht funktionieren, folgen Sie den nachstehenden Anweisungen.

## Voraussetzungen

### Erforderliche Abhängigkeiten

Hemlock benötigt folgende Abhängigkeiten zum Kompilieren:

- **C-Compiler**: GCC oder Clang (C11-Standard)
- **Make**: GNU Make
- **libffi**: Foreign Function Interface-Bibliothek (für FFI-Unterstützung)
- **OpenSSL**: Kryptografie-Bibliothek (für Hash-Funktionen: md5, sha1, sha256)
- **libwebsockets**: WebSocket- und HTTP-Client/Server-Unterstützung
- **zlib**: Kompressionsbibliothek

### Abhängigkeiten installieren

**macOS:**
```bash
# Homebrew installieren, falls noch nicht vorhanden
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Xcode Command Line Tools installieren
xcode-select --install

# Abhängigkeiten über Homebrew installieren
brew install libffi openssl@3 libwebsockets
```

**Hinweis für macOS-Benutzer**: Das Makefile erkennt automatisch Homebrew-Installationen und setzt die korrekten Include-/Bibliothekspfade. Hemlock unterstützt sowohl Intel- (x86_64) als auch Apple-Silicon- (arm64) Architekturen.

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Aus dem Quellcode kompilieren

### 1. Repository klonen

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Hemlock kompilieren

```bash
make
```

Dies kompiliert den Hemlock-Interpreter und platziert die ausführbare Datei im aktuellen Verzeichnis.

### 3. Installation überprüfen

```bash
./hemlock --version
```

Sie sollten die Hemlock-Versionsinformationen sehen.

### 4. Build testen

Führen Sie die Testsuite aus, um sicherzustellen, dass alles korrekt funktioniert:

```bash
make test
```

Alle Tests sollten bestehen. Falls Fehler auftreten, melden Sie diese bitte als Issue.

## Systemweite Installation (Optional)

Um Hemlock systemweit zu installieren (z.B. in `/usr/local/bin`):

```bash
sudo make install
```

Dies ermöglicht es Ihnen, `hemlock` von überall auszuführen, ohne den vollständigen Pfad anzugeben.

## Hemlock ausführen

### Interaktive REPL

Starten Sie die Read-Eval-Print-Schleife:

```bash
./hemlock
```

Sie sehen eine Eingabeaufforderung, in der Sie Hemlock-Code eingeben können:

```
Hemlock REPL
> print("Hallo, Welt!");
Hallo, Welt!
> let x = 42;
> print(x * 2);
84
>
```

Beenden Sie die REPL mit `Ctrl+D` oder `Ctrl+C`.

### Programme ausführen

Führen Sie ein Hemlock-Skript aus:

```bash
./hemlock programm.hml
```

Mit Kommandozeilenargumenten:

```bash
./hemlock programm.hml arg1 arg2 "Argument mit Leerzeichen"
```

## Verzeichnisstruktur

Nach dem Kompilieren sieht Ihr Hemlock-Verzeichnis so aus:

```
hemlock/
├── hemlock           # Kompilierte Interpreter-Ausführungsdatei
├── src/              # Quellcode
├── include/          # Header-Dateien
├── tests/            # Testsuite
├── examples/         # Beispielprogramme
├── docs/             # Dokumentation
├── stdlib/           # Standardbibliothek
├── Makefile          # Build-Konfiguration
└── README.md         # Projekt-README
```

## WebAssembly (WASM) Build

Hemlock kann über [Emscripten](https://emscripten.org/) zu WebAssembly kompiliert werden, sodass der vollständige Interpreter in einem Webbrowser oder Node.js läuft.

### Emscripten installieren

Das Emscripten SDK (`emsdk`) stellt den `emcc`-Compiler bereit, der zum Erstellen des WASM-Interpreters verwendet wird.

**Alle Plattformen (Linux, macOS, Windows WSL):**

```bash
# Clone the emsdk repository
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk

# Install and activate the latest SDK
./emsdk install latest
./emsdk activate latest

# Add emcc to your PATH (run this in every new terminal, or add to your shell profile)
source ./emsdk_env.sh
```

Überprüfen Sie die Installation:

```bash
emcc --version
```

Sie sollten eine Ausgabe wie `emcc (Emscripten gcc/clang-like replacement ...) 3.x.x` sehen.

Detaillierte Anweisungen finden Sie im [Emscripten Getting Started Guide](https://emscripten.org/docs/getting_started/downloads.html).

**Optional: Zum Shell-Profil hinzufügen**

Um das Ausführen von `source emsdk_env.sh` jedes Mal zu vermeiden, fügen Sie es zu Ihrem Shell-Profil hinzu:

```bash
# For bash (~/.bashrc or ~/.bash_profile)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.bashrc

# For zsh (~/.zshrc)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.zshrc
```

### WASM-Abhängigkeiten

Der WASM-Build hat weniger Abhängigkeiten als der native Build. Emscripten stellt eigene Versionen der Standard-C-Bibliotheken bereit. Die folgenden nativen Bibliotheken werden **nicht benötigt** (und sind nicht verfügbar) im WASM-Build:

| Bibliothek | Nativ | WASM | Hinweise |
|---------|--------|------|-------|
| libffi | Erforderlich | Stub | FFI ist in WASM nicht verfügbar |
| OpenSSL | Erforderlich | Stub | Krypto-Builtins geben Fehler in WASM zurück |
| libwebsockets | Optional | Stub | WebSocket-Unterstützung nicht verfügbar |
| zlib | Erforderlich | Emscripten stellt bereit | Automatisch verlinkt mit `-sUSE_ZLIB=1` |
| pthreads | Erforderlich | Optional | Verfügbar mit Thread-Build (erfordert SharedArrayBuffer) |

**Kurz gesagt:** Sie benötigen nur das installierte Emscripten SDK. Für den WASM-Build sind keine zusätzlichen Systembibliotheken erforderlich.

### Den WASM-Interpreter erstellen

```bash
# Build the interpreter as WebAssembly
make wasm-interpreter
```

Dies erzeugt zwei Dateien im Verzeichnis `wasm/`:

| Datei | Beschreibung |
|------|-------------|
| `wasm/hemlock.js` | JavaScript-Loader und Emscripten-Glue-Code |
| `wasm/hemlock.wasm` | WebAssembly-Binärmodul |

### Ausführung in Node.js

```bash
node -- wasm/hemlock.js -e 'print("Hello from WASM!");'
node -- wasm/hemlock.js examples/fibonacci.hml
```

### Ausführung im Browser

WASM-Dateien müssen über HTTP mit dem korrekten MIME-Typ (`application/wasm`) bereitgestellt werden. Das direkte Öffnen der HTML-Datei über `file://` funktioniert nicht.

**Mit dem enthaltenen Beispiel:**

```bash
make wasm-browser-example
# Opens http://localhost:8080/examples/wasm-browser/index.html
```

**Oder manuell mit Python:**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/wasm/playground.html
```

**Oder manuell mit Node.js:**

```bash
npx serve .
# Open the URL shown in the terminal
```

Siehe `examples/wasm-browser/` für ein vollständiges Browser-Integrationsbeispiel mit einem interaktiven Code-Editor.

### WASM-Einschränkungen

Einige Funktionen sind in der WASM-Umgebung nicht verfügbar:

- **FFI** - Kein Laden von Shared Libraries (`dlopen`/`dlsym`)
- **Krypto** - Kein OpenSSL (`sha256`, `md5` usw. geben Fehler zurück)
- **Datei-I/O** - Kein nativer Dateisystemzugriff (nur virtuelles Emscripten-FS)
- **Netzwerk** - Keine Raw-Sockets oder HTTP-Client
- **Signale** - Keine POSIX-Signalbehandlung
- **Prozesse** - Kein `fork`, `exec` oder Prozessverwaltung
- **Threading** - `spawn`/`join`/Kanäle erfordern einen Thread-WASM-Build mit `SharedArrayBuffer`

Alle Kern-Sprachfunktionen funktionieren: Variablen, Funktionen, Closures, Objekte, Arrays, Musterabgleich, Typannotationen, try/catch und die vollständige Standardbibliothek der reinen Hemlock-Module.

### Hemlock-Programme zu WASM kompilieren

Zusätzlich zur Ausführung des Interpreters in WASM können Sie einzelne Hemlock-Programme zu eigenständigen WASM-Binaries kompilieren, indem Sie das Compiler-Backend verwenden:

```bash
# Compile a Hemlock program to WASM (requires both hemlockc and Emscripten)
make wasm-compile FILE=program.hml

# With threading support
make wasm-compile-threaded FILE=program.hml
```

Dies verwendet `hemlockc` zur Erzeugung von C-Code, dann Emscripten zur Kompilierung zu WASM.

## Build-Optionen

### Debug-Build

Mit Debug-Symbolen und ohne Optimierung kompilieren:

```bash
make debug
```

### Bereinigter Build

Alle kompilierten Dateien entfernen:

```bash
make clean
```

Von Grund auf neu kompilieren:

```bash
make clean && make
```

## Fehlerbehebung

### macOS: Bibliothek nicht gefunden

Wenn Sie Fehler über fehlende Bibliotheken erhalten (`-lcrypto`, `-lffi`, usw.):

1. Stellen Sie sicher, dass die Homebrew-Abhängigkeiten installiert sind:
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Überprüfen Sie die Homebrew-Pfade:
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Das Makefile sollte diese Pfade automatisch erkennen. Falls nicht, überprüfen Sie, ob `brew` in Ihrem PATH ist:
   ```bash
   which brew
   ```

### macOS: BSD-Typfehler (`u_int`, `u_char` nicht gefunden)

Wenn Sie Fehler über unbekannte Typnamen wie `u_int` oder `u_char` sehen:

1. Dies wurde in v1.0.0+ durch Verwendung von `_DARWIN_C_SOURCE` anstelle von `_POSIX_C_SOURCE` behoben
2. Stellen Sie sicher, dass Sie die neueste Version des Codes haben
3. Bereinigen und neu kompilieren:
   ```bash
   make clean && make
   ```

### Linux: libffi nicht gefunden

Wenn Sie Fehler über fehlende `ffi.h` oder `-lffi` erhalten:

1. Stellen Sie sicher, dass `libffi-dev` installiert ist (siehe Abhängigkeiten oben)
2. Prüfen Sie, ob `pkg-config` es finden kann:
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. Falls nicht gefunden, müssen Sie möglicherweise `PKG_CONFIG_PATH` setzen:
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Kompilierungsfehler

Wenn Kompilierungsfehler auftreten:

1. Stellen Sie sicher, dass Sie einen C11-kompatiblen Compiler haben
2. Unter macOS versuchen Sie Clang (Standard):
   ```bash
   make CC=clang
   ```
3. Unter Linux versuchen Sie GCC:
   ```bash
   make CC=gcc
   ```
4. Überprüfen Sie, ob alle Abhängigkeiten installiert sind
5. Versuchen Sie, von Grund auf neu zu kompilieren:
   ```bash
   make clean && make
   ```

### Testfehler

Wenn Tests fehlschlagen:

1. Stellen Sie sicher, dass Sie die neueste Version des Codes haben
2. Versuchen Sie, von Grund auf neu zu kompilieren:
   ```bash
   make clean && make test
   ```
3. Unter macOS stellen Sie sicher, dass Sie die neuesten Xcode Command Line Tools haben:
   ```bash
   xcode-select --install
   ```
4. Melden Sie das Problem auf GitHub mit:
   - Ihrer Plattform (macOS-Version / Linux-Distribution)
   - Architektur (x86_64 / arm64)
   - Testausgabe
   - Ausgabe von `make -v` und `gcc --version` (oder `clang --version`)

## Nächste Schritte

- [Schnellstart-Anleitung](quick-start.md) - Schreiben Sie Ihr erstes Hemlock-Programm
- [Tutorial](tutorial.md) - Lernen Sie Hemlock Schritt für Schritt
- [Sprachhandbuch](../language-guide/syntax.md) - Entdecken Sie Hemlock-Funktionen
