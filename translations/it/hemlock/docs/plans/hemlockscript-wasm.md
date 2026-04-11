# HemlockScript: Hemlock → WASM via Emscripten

> Programmi Hemlock portatili che girano nel browser.

## Obiettivo

Aggiungere un target di compilazione WASM a `hemlockc` in modo che i programmi Hemlock possano girare nei browser e in altri runtime WASM (Node/Deno/Cloudflare Workers). L'approccio: compilare Hemlock → C (pipeline esistente) → WASM (via Emscripten), con uno shim runtime compatibile con il browser che sostituisce i builtin solo-POSIX.

**Non-obiettivo:** Riscrivere il compilatore o il runtime da zero. Sfruttiamo il codegen C esistente di `hemlockc` e `libhemlock_runtime` il più possibile.

---

## Architettura

```
Sorgente Hemlock (.hml)
        ↓
   hemlockc (frontend + codegen esistenti)
        ↓
   Codice C generato (esistente)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (runtime adattato WASM)
        ↓
   program.wasm + program.js (loader/glue)
        ↓
   Browser / Node / Deno / Runtime WASM
```

L'intuizione chiave: `hemlockc` emette già C portatile. Non serve un nuovo backend — serve una libreria runtime compatibile con WASM e una pipeline di build Emscripten.

---

## Fase 1: Build WASM Minimale (Solo Linguaggio Core)

**Risultato:** `make wasm` produce un bundle `.wasm` + `.js` che può eseguire programmi Hemlock puramente computazionali nel browser.

### 1.1 Creare il layer shim runtime WASM

Creare `runtime/src/wasm_shim.c` con implementazioni stub/sostitutive per le funzioni dipendenti da POSIX. Questo file viene compilato *al posto delle* implementazioni POSIX quando si compila per WASM.

**Funzioni da stub (errore alla chiamata):**
- `fork()`, `execve()`, `waitpid()`, `kill()` — gestione processi
- `signal()`, `raise()` — gestione segnali
- `dlopen()`, `dlsym()`, `dlclose()` — caricamento librerie dinamiche (FFI)

**Funzioni da adattare:**
- `print()` / `eprint()` → `printf`/`fprintf(stderr)` di Emscripten (funziona così com'è dato che Emscripten mappa queste a `console.log`/`console.error`)
- `sleep()` → `emscripten_sleep()` (richiede `-sASYNCIFY`)
- `time_ms()` / `now()` → `emscripten_get_now()` o `gettimeofday()` (Emscripten fornisce queste)

**Funzioni da disabilitare (escluse dalla compilazione con `#ifdef __EMSCRIPTEN__`):**
- Tutto `builtins_socket.c` (socket TCP/UDP)
- Tutto `builtins_http.c` (HTTP basato su libwebsockets)
- Tutto `builtins_process.c` (fork/exec/segnali)
- Tutto `builtins_ffi.c` (FFI basato su dlopen)
- Creazione thread in `builtins_async.c` (pthread_create)

### 1.2 Aggiungere guard `#ifdef __EMSCRIPTEN__` al runtime

Racchiudere il codice solo-POSIX nei file sorgente del runtime esistente con guard del preprocessore. Questo è preferito rispetto al mantenimento di un fork separato del runtime.

File che richiedono guard:

| File | Cosa proteggere | Sostituzione |
|------|-----------------|-------------|
| `builtins_process.c` | File intero | Stub che fanno `panic("non disponibile in WASM")` |
| `builtins_socket.c` | File intero | Stub |
| `builtins_http.c` | File intero | Stub |
| `builtins_ffi.c` | `dlopen`/`dlsym`/`ffi_call` | Stub |
| `builtins_async.c` | `pthread_create`, canali | Stub single-threaded (Fase 1) |
| `builtins_io.c` | `open()`, `read()`, `write()` | MEMFS di Emscripten (funziona così com'è per I/O base) |
| `builtins_time.c` | `clock_gettime`, `nanosleep` | Equivalenti Emscripten |
| `builtins_crypto.c` | Chiamate OpenSSL | Stub (Fase 1), Web Crypto API (Fase 3) |
| `atomics.c` | Operazioni atomiche | Emscripten fornisce `<stdatomic.h>`, dovrebbe funzionare |

### 1.3 Creare target Makefile specifico per WASM

Aggiungere a `runtime/Makefile`:

```makefile
# Build WASM via Emscripten
wasm: $(BUILD_DIR)/libhemlock_runtime_wasm.a

$(BUILD_DIR)/libhemlock_runtime_wasm.a: $(WASM_OBJS)
	emar rcs $@ $^

$(BUILD_DIR)/wasm_%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	emcc $(WASM_CFLAGS) -c $< -o $@
```

Aggiungere al `Makefile` di livello superiore:

```makefile
# Compila programma Hemlock per WASM
wasm: compiler runtime-wasm
	@echo "Utilizzo: make wasm-compile FILE=program.hml"

wasm-compile: compiler runtime-wasm
	./hemlockc -c $(FILE) -o /tmp/hemlock_wasm.c
	emcc -O2 -s WASM=1 -s EXPORTED_FUNCTIONS='["_main"]' \
	     -I runtime/include \
	     /tmp/hemlock_wasm.c \
	     runtime/build/libhemlock_runtime_wasm.a \
	     -o $(basename $(FILE)).js
	@echo "Compilato: $(basename $(FILE)).js + $(basename $(FILE)).wasm"

runtime-wasm:
	$(MAKE) -C $(RUNTIME_DIR) wasm
```

### 1.4 Modificare `hemlockc` per supportare target WASM

Aggiungere un flag `--target wasm` a `hemlockc` che:
1. Definisce `__HEMLOCK_WASM__` nel codice C generato (`#define __HEMLOCK_WASM__ 1`)
2. Emette `#include <emscripten.h>` quando compila per WASM
3. Salta il codegen per funzionalità non supportate (dichiarazioni extern FFI, segnali)
4. Usa `emscripten_sleep()` invece di `sleep()` della piattaforma

Modifiche in `src/backends/compiler/main.c`:
- Aggiungere opzione CLI `--target wasm`
- Passare info target al `CodegenContext`

Modifiche in `src/backends/compiler/codegen_program.c`:
- Emettere preambolo `#ifdef __EMSCRIPTEN__` quando compila per WASM
- Saltare dichiarazioni `extern fn` (emettere warning)

### 1.5 Creare harness di test HTML

Creare `wasm/index.html` — una pagina di test minimale:

```html
<!DOCTYPE html>
<html>
<head><title>HemlockScript</title></head>
<body>
  <pre id="output"></pre>
  <script>
    var Module = {
      print: function(text) {
        document.getElementById('output').textContent += text + '\n';
      },
      printErr: function(text) {
        console.error(text);
      }
    };
  </script>
  <script src="program.js"></script>
</body>
</html>
```

### Deliverable Fase 1
- `make wasm-compile FILE=hello.hml` produce output eseguibile nel browser
- Tutte le funzionalità Hemlock di pura computazione funzionano: variabili, funzioni, closure, flusso di controllo, pattern matching, oggetti, array, stringhe, matematica, sistema di tipi
- `print()` produce output nella console del browser / elemento HTML
- Le funzionalità non supportate (FFI, socket, processi, segnali) fanno panic con messaggio chiaro

### Testing Fase 1
- Aggiungere directory `tests/wasm/` con test di base
- Script che compila ogni test con emcc, esegue con Node.js, confronta output
- Riuso dell'infrastruttura di test di parità: stessi file `.expected`, runner diverso

---

## Fase 2: I/O Browser e Stdlib

**Risultato:** I programmi Hemlock possono fare lavoro utile nel browser — accesso ai file (FS virtuale), operazioni temporali, e i moduli stdlib portatili funzionano.

### 2.1 Filesystem virtuale Emscripten

Emscripten fornisce MEMFS (filesystem in-memory) di default. Le chiamate `open()`/`read()`/`write()` di Hemlock passano già attraverso libc, quindi funzionano su MEMFS senza modifiche per la Fase 1.

Per storage persistente, aggiungere IDBFS opzionale (basato su IndexedDB):

```c
#ifdef __EMSCRIPTEN__
#include <emscripten.h>
// Monta filesystem persistente
EM_ASM(
    FS.mkdir('/persistent');
    FS.mount(IDBFS, {}, '/persistent');
    FS.syncfs(true, function(err) { /* caricato */ });
);
#endif
```

### 2.2 Portare i 22 moduli stdlib già portatili

Questi moduli sono Hemlock puro e non necessitano di modifiche:

`arena`, `assert`, `collections`, `csv`, `datetime`, `encoding`, `fmt`, `iter`, `json`, `logging`, `math`, `path`, `random`, `regex`, `retry`, `semver`, `strings`, `testing`, `terminal`, `toml`, `url`, `uuid`

**Lavoro necessario:** Assicurarsi che il caricatore di moduli stdlib funzioni nel contesto WASM.

### 2.3 Adattare modulo time

- `now()` → `emscripten_get_now()` (alta risoluzione, già disponibile)
- `time_ms()` → `gettimeofday()` (Emscripten fornisce questa)
- `sleep(ms)` → `emscripten_sleep(ms)` (richiede flag `-sASYNCIFY`)
- `clock()` → Emscripten fornisce `clock()` da libc

### 2.4 Adattare moduli env/os/args

- `getenv()`/`setenv()` → Emscripten fornisce questi (env in-memory)
- `platform()` → restituisce `"wasm"`
- `arch()` → restituisce `"wasm32"`
- `args` → Può essere impostato via `Module.arguments` in JS

### Deliverable Fase 2
- 22 moduli stdlib funzionanti in WASM
- Filesystem virtuale per I/O file
- Funzioni temporali funzionanti
- `make wasm-test` esegue test stdlib nel runtime WASM di Node.js

---

## Fase 3: Bridge di Interop JavaScript

**Risultato:** I programmi WASM Hemlock possono chiamare API del browser e funzioni JavaScript, e JavaScript può chiamare funzioni Hemlock.

### 3.1 Bridge JavaScript (`hemlock_js_bridge`)

Creare un layer di interop JS-to-WASM che sostituisce FFI per il browser:

```hemlock
// Invece di: import "libcrypto.so.6"; extern fn ...
// Usare:     import { fetch, setTimeout } from "@wasm/browser";

import { fetch } from "@wasm/browser";
let response = await fetch("https://api.example.com/data");
print(response);
```

### 3.2 Funzioni esportate (Hemlock → JS)

Permettere che le funzioni Hemlock siano chiamabili da JavaScript:

```hemlock
// math_utils.hml
export fn fibonacci(n: i32): i32 {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

Lato JS:
```javascript
const fib = Module.cwrap('hml_fn_fibonacci', 'number', ['number', 'number']);
console.log(fib(0, 10)); // 55
```

### 3.3 Adattare moduli di rete per il browser

| API Hemlock | Sostituzione browser |
|-------------|---------------------|
| `http_get(url)` | `fetch()` via Asyncify |
| `http_post(url, body)` | `fetch()` con POST |
| `WebSocket(url)` | API `WebSocket` del browser |

### 3.4 Adattare modulo crypto

Sostituire OpenSSL con Web Crypto API.

### Deliverable Fase 3
- Chiamate di funzione bidirezionali JS ↔ Hemlock
- Modulo `@wasm/browser` per API del browser
- HTTP via fetch, WebSocket via WebSocket del browser
- Crypto via Web Crypto API
- Funzioni Hemlock esportate chiamabili da JS

---

## Fase 4: Async e Threading (Stretch)

**Risultato:** `spawn`/`await` di Hemlock funziona nel browser usando Web Workers.

### 4.1 Spawning di task basato su Web Worker

Mappare `spawn()` di Hemlock a Web Workers:

```
Hemlock spawn(fn, args)  →  new Worker() con SharedArrayBuffer
Hemlock join(task)       →  Atomics.wait() / message passing
Hemlock channel          →  MessagePort o ring buffer SharedArrayBuffer
```

Questa è la fase più difficile perché:
- Ogni Worker necessita della propria istanza WASM
- SharedArrayBuffer richiede header COOP/COEP
- I dati devono essere serializzati attraverso i confini dei Worker

### 4.2 Asyncify per operazioni bloccanti

Usare Asyncify di Emscripten per gestire le chiamate bloccanti:
- `sleep()` → `emscripten_sleep()`
- `channel.recv()` → attesa asincrona
- `read_line()` → lettura stdin asincrona

Asyncify aggiunge ~10% di overhead sulla dimensione del codice ma abilita codice dall'aspetto sincrono.

### Deliverable Fase 4
- `spawn()` crea Web Workers
- I canali funzionano attraverso i worker via SharedArrayBuffer
- `sleep()` e I/O bloccante non bloccano il thread principale

---

## Riepilogo Modifiche ai File

### Nuovi file
```
runtime/src/wasm_shim.c          — Stub WASM per funzioni POSIX
runtime/src/wasm_bridge.c        — Bridge interop JS (Fase 3)
wasm/                            — Directory output WASM
wasm/index.html                  — Pagina HTML harness di test
wasm/hemlock.js                  — API wrapper/loader JS opzionale
tests/wasm/                      — Test specifici WASM
tests/wasm/run_wasm_tests.sh     — Test runner (usa Node.js)
```

### File modificati
```
Makefile                         — Aggiungere target wasm, wasm-compile, wasm-test
runtime/Makefile                 — Aggiungere target build wasm usando emcc/emar
src/backends/compiler/main.c     — Aggiungere flag --target wasm
src/backends/compiler/codegen_program.c — Generazione preambolo WASM
runtime/src/builtins_process.c   — Guard #ifdef __EMSCRIPTEN__
runtime/src/builtins_socket.c    — Guard #ifdef __EMSCRIPTEN__
runtime/src/builtins_http.c      — Guard #ifdef __EMSCRIPTEN__
runtime/src/builtins_ffi.c       — Guard #ifdef __EMSCRIPTEN__
runtime/src/builtins_async.c     — Guard #ifdef __EMSCRIPTEN__
runtime/src/builtins_io.c        — #ifdef __EMSCRIPTEN__ per MEMFS/IDBFS
runtime/src/builtins_time.c      — #ifdef per emscripten_sleep
runtime/src/builtins_crypto.c    — #ifdef per stub Web Crypto
runtime/include/hemlock_runtime.h — Macro di rilevamento funzionalità WASM
```

---

## Requisiti di Build

- **Emscripten SDK** (emcc, emar, emconfigure)
- **Node.js** (per eseguire test WASM fuori dal browser)
- Tutti i requisiti di build esistenti (per il compilatore hemlockc stesso)

Il compilatore (`hemlockc`) viene comunque compilato nativamente — solo l'*output* compila per WASM.

---

## Cosa Funziona Immediatamente (Nessuna Modifica Necessaria)

Queste funzionalità Hemlock compilano in C standard che Emscripten gestisce nativamente:

- Tutti gli operatori aritmetici, bit a bit, logici
- Variabili, scope, closure
- Funzioni, ricorsione, funzioni con corpo espressione
- if/else, while, for, loop, switch, pattern matching
- Oggetti, array, stringhe (tutti i 19+23 metodi)
- Annotazioni di tipo e type checking a runtime
- Try/catch/finally/throw
- Defer
- Template string
- Null coalescing (`??`, `?.`, `??=`)
- Argomenti nominati
- Tipi composti, alias di tipo
- `print()`, `eprint()` (tramite mappatura console di Emscripten)
- `alloc()`/`free()`/`buffer()` (memoria lineare)
- `typeof()`, `len()`, `sizeof()`
- Builtin matematici (sin, cos, sqrt, ecc.)
- Tutto il conteggio riferimenti / gestione memoria

---

## Stima dello Scope per Fase

| Fase | Scope | Dipendenze |
|------|-------|------------|
| **Fase 1** | ~800 righe C nuove, ~200 righe guard #ifdef, modifiche Makefile | SDK Emscripten |
| **Fase 2** | ~200 righe C, testing stdlib, Makefile | Fase 1 |
| **Fase 3** | ~600 righe C (bridge), ~200 righe Hemlock (stdlib) | Fase 1 |
| **Fase 4** | ~1000 righe C (threading Worker), complesso | Fase 1+3 |

Ordine raccomandato: Fase 1 → Fase 2 → Fase 3 → Fase 4

La Fase 1 da sola fornisce un utile "Hemlock nel browser" per carichi di lavoro computazionali. Le Fasi 2-4 aggiungono incrementalmente I/O e interop.
