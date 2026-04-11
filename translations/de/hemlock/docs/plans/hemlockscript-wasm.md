# HemlockScript: Hemlock → WASM via Emscripten

> Portable Hemlock-Programme, die im Browser laufen.

## Ziel

Ein WASM-Kompilierungsziel zu `hemlockc` hinzufügen, damit Hemlock-Programme in Browsern und anderen WASM-Laufzeiten (Node/Deno/Cloudflare Workers) laufen können. Der Ansatz: Hemlock → C (bestehende Pipeline) → WASM (via Emscripten) kompilieren, mit einem browserkompatiblen Laufzeit-Shim, der POSIX-only-Builtins ersetzt.

**Nicht-Ziel:** Compiler oder Laufzeit von Grund auf neu schreiben. Wir nutzen den bestehenden `hemlockc` C-Codegen und `libhemlock_runtime` so weit wie möglich.

---

## Architektur

```
Hemlock-Quelle (.hml)
        ↓
   hemlockc (bestehendes Frontend + Codegen)
        ↓
   Generierter C-Code (bestehend)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (WASM-angepasste Laufzeit)
        ↓
   program.wasm + program.js (Loader/Glue)
        ↓
   Browser / Node / Deno / WASM-Laufzeit
```

Die Schlüsselerkenntnis: `hemlockc` gibt bereits portablen C-Code aus. Wir brauchen kein neues Backend -- wir brauchen eine WASM-kompatible Laufzeitbibliothek und eine Emscripten-Build-Pipeline.

---

## Phase 1: Minimaler WASM-Build (nur Kernsprache)

**Ergebnis:** `make wasm` erzeugt ein `.wasm` + `.js`-Bundle, das rein berechnungsorientierte Hemlock-Programme im Browser ausführen kann.

### 1.1 WASM-Laufzeit-Shim-Schicht erstellen

`runtime/src/wasm_shim.c` mit Stub-/Ersatzimplementierungen für POSIX-abhängige Funktionen erstellen. Diese Datei wird *anstelle der* POSIX-Implementierungen kompiliert, wenn WASM als Ziel gewählt wird.

**Zu stubbende Funktionen (Fehler bei Aufruf):**
- `fork()`, `execve()`, `waitpid()`, `kill()` -- Prozessverwaltung
- `signal()`, `raise()` -- Signalbehandlung
- `dlopen()`, `dlsym()`, `dlclose()` -- dynamisches Bibliotheksladen (FFI)

**Anzupassende Funktionen:**
- `print()` / `eprint()` → Emscriptens `printf`/`fprintf(stderr)` (funktioniert direkt, da Emscripten diese auf `console.log`/`console.error` abbildet)
- `sleep()` → `emscripten_sleep()` (erfordert `-sASYNCIFY`)
- `time_ms()` / `now()` → `emscripten_get_now()` oder `gettimeofday()` (Emscripten stellt diese bereit)

**Zu deaktivierende Funktionen (mit `#ifdef __EMSCRIPTEN__` auskompilieren):**
- Gesamte `builtins_socket.c` (TCP/UDP-Sockets)
- Gesamte `builtins_http.c` (libwebsockets-basiertes HTTP)
- Gesamte `builtins_process.c` (fork/exec/Signale)
- Gesamte `builtins_ffi.c` (dlopen-basiertes FFI)
- Thread-Erstellung in `builtins_async.c` (pthread_create)

### 1.2 `#ifdef __EMSCRIPTEN__`-Guards zur Laufzeit hinzufügen

POSIX-only-Code in den bestehenden Laufzeit-Quelldateien mit Präprozessor-Guards umschließen.

### 1.3 WASM-spezifisches Makefile-Target erstellen

### 1.4 `hemlockc` für WASM-Ziel modifizieren

Ein `--target wasm`-Flag zu `hemlockc` hinzufügen.

### 1.5 HTML-Test-Harness erstellen

### Phase 1-Lieferungen
- `make wasm-compile FILE=hello.hml` erzeugt funktionsfähige Browser-Ausgabe
- Alle rein berechnungsorientierten Hemlock-Features funktionieren: Variablen, Funktionen, Closures, Kontrollfluss, Pattern Matching, Objekte, Arrays, Strings, Mathematik, Typsystem
- `print()` gibt in Browser-Konsole / HTML-Element aus
- Nicht unterstützte Features (FFI, Sockets, Prozess, Signale) lösen Panic mit klarer Meldung aus

---

## Phase 2: Browser-I/O & Stdlib

**Ergebnis:** Hemlock-Programme können nützliche Arbeit im Browser leisten -- Dateizugriff (virtuelles FS), Zeitoperationen und die portablen Stdlib-Module funktionieren.

### 2.1 Emscripten virtuelles Dateisystem

Emscripten stellt MEMFS (In-Memory-Dateisystem) standardmäßig bereit. Hemlocks `open()`/`read()`/`write()`-Aufrufe gehen bereits durch libc, sie funktionieren also auf MEMFS ohne Änderungen.

### 2.2 Die 22 bereits portablen Stdlib-Module portieren

Diese Module sind reines Hemlock und benötigen keine Änderungen:

`arena`, `assert`, `collections`, `csv`, `datetime`, `encoding`, `fmt`, `iter`, `json`, `logging`, `math`, `path`, `random`, `regex`, `retry`, `semver`, `strings`, `testing`, `terminal`, `toml`, `url`, `uuid`

---

## Phase 3: JavaScript-Interop-Brücke

**Ergebnis:** Hemlock-WASM-Programme können Browser-APIs und JavaScript-Funktionen aufrufen, und JavaScript kann Hemlock-Funktionen aufrufen.

### 3.1 JavaScript-Brücke (`hemlock_js_bridge`)

JS-zu-WASM-Interop-Schicht erstellen, die FFI für den Browser ersetzt:

```hemlock
// Statt: import "libcrypto.so.6"; extern fn ...
// Verwende: import { fetch, setTimeout } from "@wasm/browser";

import { fetch } from "@wasm/browser";
let response = await fetch("https://api.example.com/data");
print(response);
```

### 3.2 Exportierte Funktionen (Hemlock → JS)

Hemlock-Funktionen von JavaScript aus aufrufbar machen:

```hemlock
// math_utils.hml
export fn fibonacci(n: i32): i32 {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

---

## Phase 4: Async & Threading (Erweiterung)

**Ergebnis:** Hemlocks `spawn`/`await` funktioniert im Browser unter Verwendung von Web Workers.

### 4.1 Web-Worker-basiertes Task-Spawning

Hemlocks `spawn()` auf Web Workers abbilden:

```
Hemlock spawn(fn, args)  →  new Worker() mit SharedArrayBuffer
Hemlock join(task)       →  Atomics.wait() / Message Passing
Hemlock channel          →  MessagePort oder SharedArrayBuffer Ring Buffer
```

---

## Was sofort funktioniert (keine Änderungen nötig)

Diese Hemlock-Features kompilieren zu Standard-C, das Emscripten nativ verarbeitet:

- Alle arithmetischen, bitweisen, logischen Operatoren
- Variablen, Scoping, Closures
- Funktionen, Rekursion, Ausdruckskörper-Funktionen
- if/else, while, for, loop, switch, Pattern Matching
- Objekte, Arrays, Strings (alle 19+23 Methoden)
- Typannotationen und Laufzeit-Typprüfung
- Try/catch/finally/throw
- Defer
- Template-Strings
- Null-Koaleszenz (`??`, `?.`, `??=`)
- Benannte Argumente
- Zusammengesetzte Typen, Typaliase
- `print()`, `eprint()` (via Emscriptens Konsolen-Mapping)
- `alloc()`/`free()`/`buffer()` (linearer Speicher)
- `typeof()`, `len()`, `sizeof()`
- Mathe-Builtins (sin, cos, sqrt, etc.)
- Alle Referenzzählung / Speicherverwaltung

---

## Geschätzter Umfang pro Phase

| Phase | Umfang | Abhängigkeiten |
|-------|--------|----------------|
| **Phase 1** | ~800 Zeilen neues C, ~200 Zeilen #ifdef Guards, Makefile-Änderungen | Emscripten SDK |
| **Phase 2** | ~200 Zeilen C, Stdlib-Tests, Makefile | Phase 1 |
| **Phase 3** | ~600 Zeilen C (Brücke), ~200 Zeilen Hemlock (Stdlib) | Phase 1 |
| **Phase 4** | ~1000 Zeilen C (Worker-Threading), komplex | Phase 1+3 |

Empfohlene Reihenfolge: Phase 1 → Phase 2 → Phase 3 → Phase 4

Phase 1 allein gibt Ihnen ein nützliches "Hemlock im Browser" für Berechnungsworkloads. Phasen 2-4 fügen inkrementell I/O und Interop hinzu.
