# HemlockScript : Hemlock → WASM via Emscripten

> Des programmes Hemlock portables qui s'executent dans le navigateur.

## Objectif

Ajouter une cible de compilation WASM a `hemlockc` afin que les programmes Hemlock puissent s'executer dans les navigateurs et autres runtimes WASM (Node/Deno/Cloudflare Workers). L'approche : compiler Hemlock → C (pipeline existant) → WASM (via Emscripten), avec un shim de runtime compatible navigateur remplacant les builtins POSIX uniquement.

**Non-objectif :** Reecrire le compilateur ou le runtime de zero. Nous exploitons le codegen C existant de `hemlockc` et `libhemlock_runtime` autant que possible.

---

## Architecture

```
Source Hemlock (.hml)
        ↓
   hemlockc (frontend + codegen existants)
        ↓
   Code C genere (existant)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (runtime adapte WASM)
        ↓
   program.wasm + program.js (chargeur/glue)
        ↓
   Navigateur / Node / Deno / Runtime WASM
```

L'idee cle : `hemlockc` emet deja du C portable. Nous n'avons pas besoin d'un nouveau backend -- nous avons besoin d'une bibliotheque runtime compatible WASM et d'un pipeline de build Emscripten.

---

## Phase 1 : Build WASM minimal (langage de base uniquement)

**Resultat :** `make wasm` produit un bundle `.wasm` + `.js` qui peut executer des programmes Hemlock purement computationnels dans le navigateur.

### 1.1 Creer la couche shim runtime WASM

Creer `runtime/src/wasm_shim.c` avec des implementations stub/remplacement pour les fonctions dependantes de POSIX. Ce fichier est compile *a la place* des implementations POSIX lors du ciblage WASM.

**Fonctions a stubber (erreur a l'appel) :**
- `fork()`, `execve()`, `waitpid()`, `kill()` -- gestion de processus
- `signal()`, `raise()` -- gestion des signaux
- `dlopen()`, `dlsym()`, `dlclose()` -- chargement dynamique de bibliotheques (FFI)

**Fonctions a adapter :**
- `print()` / `eprint()` → `printf`/`fprintf(stderr)` d'Emscripten (fonctionne tel quel puisque Emscripten les mappe vers `console.log`/`console.error`)
- `sleep()` → `emscripten_sleep()` (necessite `-sASYNCIFY`)
- `time_ms()` / `now()` → `emscripten_get_now()` ou `gettimeofday()` (Emscripten les fournit)

**Fonctions a desactiver (compiler avec `#ifdef __EMSCRIPTEN__`) :**
- Tout `builtins_socket.c` (sockets TCP/UDP)
- Tout `builtins_http.c` (HTTP base sur libwebsockets)
- Tout `builtins_process.c` (fork/exec/signaux)
- Tout `builtins_ffi.c` (FFI base sur dlopen)
- Creation de threads dans `builtins_async.c` (pthread_create)

### 1.2 Ajouter des gardes `#ifdef __EMSCRIPTEN__` au runtime

Envelopper le code POSIX uniquement dans les fichiers source du runtime existant avec des gardes preprocesseur. Ceci est prefere au maintien d'un fork separe du runtime.

Fichiers necessitant des gardes :

| Fichier | Quoi garder | Remplacement |
|---------|-------------|-------------|
| `builtins_process.c` | Fichier entier | Stubs qui `panic("not available in WASM")` |
| `builtins_socket.c` | Fichier entier | Stubs |
| `builtins_http.c` | Fichier entier | Stubs |
| `builtins_ffi.c` | `dlopen`/`dlsym`/`ffi_call` | Stubs |
| `builtins_async.c` | `pthread_create`, canaux | Stubs mono-thread (Phase 1) |
| `builtins_io.c` | `open()`, `read()`, `write()` | Emscripten MEMFS (fonctionne tel quel pour l'E/S basique) |
| `builtins_time.c` | `clock_gettime`, `nanosleep` | Equivalents Emscripten |
| `builtins_crypto.c` | Appels OpenSSL | Stubs (Phase 1), API Web Crypto (Phase 3) |
| `atomics.c` | Operations atomiques | Emscripten fournit `<stdatomic.h>`, devrait fonctionner |

### 1.3 Creer une cible Makefile specifique WASM

Ajouter a `runtime/Makefile` :

```makefile
# Build WASM via Emscripten
wasm: $(BUILD_DIR)/libhemlock_runtime_wasm.a

$(BUILD_DIR)/libhemlock_runtime_wasm.a: $(WASM_OBJS)
	emar rcs $@ $^

$(BUILD_DIR)/wasm_%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	emcc $(WASM_CFLAGS) -c $< -o $@
```

Ajouter au `Makefile` de niveau superieur :

```makefile
# Construire un programme Hemlock pour WASM
wasm: compiler runtime-wasm
	@echo "Usage: make wasm-compile FILE=program.hml"

wasm-compile: compiler runtime-wasm
	./hemlockc -c $(FILE) -o /tmp/hemlock_wasm.c
	emcc -O2 -s WASM=1 -s EXPORTED_FUNCTIONS='["_main"]' \
	     -I runtime/include \
	     /tmp/hemlock_wasm.c \
	     runtime/build/libhemlock_runtime_wasm.a \
	     -o $(basename $(FILE)).js
	@echo "Built: $(basename $(FILE)).js + $(basename $(FILE)).wasm"

runtime-wasm:
	$(MAKE) -C $(RUNTIME_DIR) wasm
```

### 1.4 Modifier `hemlockc` pour supporter la cible WASM

Ajouter un flag `--target wasm` a `hemlockc` qui :
1. Definit `__HEMLOCK_WASM__` dans le code C genere (`#define __HEMLOCK_WASM__ 1`)
2. Emet `#include <emscripten.h>` lors du ciblage WASM
3. Saute le codegen pour les fonctionnalites non supportees (declarations FFI extern, signaux)
4. Utilise `emscripten_sleep()` au lieu du `sleep()` de la plateforme

Modifications dans `src/backends/compiler/main.c` :
- Ajouter l'option CLI `--target wasm`
- Passer les infos de cible au `CodegenContext`

Modifications dans `src/backends/compiler/codegen_program.c` :
- Emettre un preambule `#ifdef __EMSCRIPTEN__` lors du ciblage WASM
- Sauter les declarations `extern fn` (emettre un avertissement)

### 1.5 Creer un harnais de test HTML

Creer `wasm/index.html` -- une page de test minimale :

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

### Livrables Phase 1
- `make wasm-compile FILE=hello.hml` produit une sortie executable dans le navigateur
- Toutes les fonctionnalites Hemlock de calcul pur fonctionnent : variables, fonctions, closures, flux de controle, pattern matching, objets, tableaux, chaines, math, systeme de types
- `print()` sort vers la console du navigateur / element HTML
- Les fonctionnalites non supportees (FFI, sockets, processus, signaux) paniquent avec un message clair

### Tests Phase 1
- Ajouter un repertoire `tests/wasm/` avec des tests basiques
- Script qui compile chaque test avec emcc, execute avec Node.js, compare la sortie
- Reutiliser l'infrastructure de test de parite : memes fichiers `.expected`, executeur different

---

## Phase 2 : E/S navigateur et Stdlib

**Resultat :** Les programmes Hemlock peuvent faire du travail utile dans le navigateur -- acces fichier (FS virtuel), operations temporelles, et les modules stdlib portables fonctionnent.

### 2.1 Systeme de fichiers virtuel Emscripten

Emscripten fournit MEMFS (systeme de fichiers en memoire) par defaut. Les appels `open()`/`read()`/`write()` de Hemlock passent deja par libc, donc ils fonctionnent sur MEMFS sans modifications pour la Phase 1.

Pour le stockage persistant, ajouter le support optionnel IDBFS (base sur IndexedDB) :

```c
#ifdef __EMSCRIPTEN__
#include <emscripten.h>
// Monter le systeme de fichiers persistant
EM_ASM(
    FS.mkdir('/persistent');
    FS.mount(IDBFS, {}, '/persistent');
    FS.syncfs(true, function(err) { /* charge */ });
);
#endif
```

Ajouter a la variante WASM de `@stdlib/fs` :
- `read_file()` / `write_file()` → fonctionnent sur MEMFS/IDBFS
- `list_dir()` → fonctionne sur le FS virtuel
- `exists()` → fonctionne sur le FS virtuel

### 2.2 Porter les 22 modules stdlib deja portables

Ces modules sont du Hemlock pur et ne necessitent aucune modification :

`arena`, `assert`, `collections`, `csv`, `datetime`, `encoding`, `fmt`, `iter`, `json`, `logging`, `math`, `path`, `random`, `regex`, `retry`, `semver`, `strings`, `testing`, `terminal`, `toml`, `url`, `uuid`

**Travail necessaire :** S'assurer que le chargeur de modules stdlib fonctionne dans le contexte WASM. Le mecanisme existant `import { x } from "@stdlib/module"` compile le code du module en ligne -- verifier que cela fonctionne avec emcc.

### 2.3 Adapter le module de temps

- `now()` → `emscripten_get_now()` (haute resolution, deja disponible)
- `time_ms()` → `gettimeofday()` (Emscripten le fournit)
- `sleep(ms)` → `emscripten_sleep(ms)` (necessite le flag `-sASYNCIFY`)
- `clock()` → Emscripten fournit `clock()` de libc

### 2.4 Adapter les modules env/os/args

- `getenv()`/`setenv()` → Emscripten les fournit (env en memoire)
- `platform()` → retourne `"wasm"`
- `arch()` → retourne `"wasm32"`
- `args` → Peut etre defini via `Module.arguments` en JS

### Livrables Phase 2
- 22 modules stdlib fonctionnant en WASM
- Systeme de fichiers virtuel pour l'E/S fichier
- Fonctions temporelles fonctionnelles
- `make wasm-test` execute les tests stdlib dans le runtime WASM Node.js

---

## Phase 3 : Pont d'interoperabilite JavaScript

**Resultat :** Les programmes Hemlock WASM peuvent appeler les APIs navigateur et les fonctions JavaScript, et JavaScript peut appeler les fonctions Hemlock.

### 3.1 Pont JavaScript (`hemlock_js_bridge`)

Creer une couche d'interoperabilite JS-vers-WASM qui remplace FFI pour le navigateur :

```hemlock
// Au lieu de : import "libcrypto.so.6"; extern fn ...
// Utiliser :    import { fetch, setTimeout } from "@wasm/browser";

import { fetch } from "@wasm/browser";
let response = await fetch("https://api.example.com/data");
print(response);
```

Implementation : macros `EM_JS` / `EM_ASM` d'Emscripten pour appeler JS depuis C :

```c
// runtime/src/wasm_bridge.c
#ifdef __EMSCRIPTEN__
#include <emscripten.h>

EM_JS(char*, hml_js_fetch_sync, (const char* url), {
    // Fetch synchrone via Asyncify
    var xhr = new XMLHttpRequest();
    xhr.open('GET', UTF8ToString(url), false);
    xhr.send();
    return allocateUTF8(xhr.responseText);
});
#endif
```

### 3.2 Fonctions exportees (Hemlock → JS)

Permettre aux fonctions Hemlock d'etre appelees depuis JavaScript :

```hemlock
// math_utils.hml
export fn fibonacci(n: i32): i32 {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

Compile en :
```c
EMSCRIPTEN_KEEPALIVE
HmlValue hml_fn_fibonacci(HmlClosureEnv* env, HmlValue n) { ... }
```

Cote JS :
```javascript
const fib = Module.cwrap('hml_fn_fibonacci', 'number', ['number', 'number']);
console.log(fib(0, 10)); // 55
```

### 3.3 Adapter les modules reseau pour le navigateur

Remplacer le reseau base sur les sockets par les APIs navigateur :

| API Hemlock | Remplacement navigateur |
|-------------|----------------------|
| `http_get(url)` | `fetch()` via Asyncify |
| `http_post(url, body)` | `fetch()` avec POST |
| `WebSocket(url)` | API `WebSocket` du navigateur |

Ceux-ci vont dans un nouveau `@wasm/http` ou adaptent `@stdlib/http` avec `#ifdef` dans les builtins runtime sous-jacents.

### 3.4 Adapter le module crypto

Remplacer OpenSSL par l'API Web Crypto :

```c
#ifdef __EMSCRIPTEN__
EM_JS(void, hml_sha256_wasm, (const char* input, int len, char* output), {
    // Utiliser SubtleCrypto
    var data = HEAPU8.slice(input, input + len);
    crypto.subtle.digest('SHA-256', data).then(function(hash) {
        var arr = new Uint8Array(hash);
        for (var i = 0; i < 32; i++) HEAPU8[output + i] = arr[i];
    });
});
#endif
```

### Livrables Phase 3
- Appels de fonctions bidirectionnels JS ↔ Hemlock
- Module `@wasm/browser` pour les APIs navigateur
- HTTP via fetch, WebSocket via WebSocket du navigateur
- Crypto via API Web Crypto
- Fonctions Hemlock exportees appelables depuis JS

---

## Phase 4 : Async et threading (Extension)

**Resultat :** Le `spawn`/`await` de Hemlock fonctionne dans le navigateur en utilisant les Web Workers.

### 4.1 Lancement de taches base sur les Web Workers

Mapper le `spawn()` de Hemlock vers les Web Workers :

```
Hemlock spawn(fn, args)  →  new Worker() avec SharedArrayBuffer
Hemlock join(task)       →  Atomics.wait() / passage de messages
Hemlock channel          →  MessagePort ou buffer circulaire SharedArrayBuffer
```

C'est la phase la plus difficile car :
- Chaque Worker a besoin de sa propre instance WASM
- SharedArrayBuffer necessite les en-tetes COOP/COEP
- Les donnees doivent etre serialisees a travers les frontieres Worker

### 4.2 Asyncify pour les operations bloquantes

Utiliser Asyncify d'Emscripten pour gerer les appels bloquants :
- `sleep()` → `emscripten_sleep()`
- `channel.recv()` → attente async
- `read_line()` → lecture stdin async

Asyncify ajoute environ 10% de surcharge en taille de code mais permet du code d'apparence synchrone.

### Livrables Phase 4
- `spawn()` cree des Web Workers
- Les canaux fonctionnent entre workers via SharedArrayBuffer
- `sleep()` et l'E/S bloquante ne bloquent pas le thread principal

---

## Resume des modifications de fichiers

### Nouveaux fichiers
```
runtime/src/wasm_shim.c          — Stubs WASM pour les fonctions POSIX
runtime/src/wasm_bridge.c        — Pont d'interoperabilite JS (Phase 3)
wasm/                            — Repertoire de sortie WASM
wasm/index.html                  — Page HTML de harnais de test
wasm/hemlock.js                  — API wrapper/chargeur JS optionnel
tests/wasm/                      — Tests specifiques WASM
tests/wasm/run_wasm_tests.sh     — Executeur de tests (utilise Node.js)
```

### Fichiers modifies
```
Makefile                         — Ajouter les cibles wasm, wasm-compile, wasm-test
runtime/Makefile                 — Ajouter la cible de build wasm utilisant emcc/emar
src/backends/compiler/main.c     — Ajouter le flag --target wasm
src/backends/compiler/codegen_program.c — Generation du preambule WASM
runtime/src/builtins_process.c   — Gardes #ifdef __EMSCRIPTEN__
runtime/src/builtins_socket.c    — Gardes #ifdef __EMSCRIPTEN__
runtime/src/builtins_http.c      — Gardes #ifdef __EMSCRIPTEN__
runtime/src/builtins_ffi.c       — Gardes #ifdef __EMSCRIPTEN__
runtime/src/builtins_async.c     — Gardes #ifdef __EMSCRIPTEN__
runtime/src/builtins_io.c        — #ifdef __EMSCRIPTEN__ pour MEMFS/IDBFS
runtime/src/builtins_time.c      — #ifdef pour emscripten_sleep
runtime/src/builtins_crypto.c    — #ifdef pour stubs Web Crypto
runtime/include/hemlock_runtime.h — Macros de detection de fonctionnalites WASM
```

### Ajouts stdlib (Phase 3)
```
stdlib/wasm_browser.hml          — Module @wasm/browser (fetch, DOM, etc.)
```

---

## Exigences de build

- **SDK Emscripten** (emcc, emar, emconfigure)
- **Node.js** (pour executer les tests WASM hors navigateur)
- Toutes les exigences de build existantes (pour le compilateur hemlockc lui-meme)

Le compilateur (`hemlockc`) se construit toujours nativement -- seule la *sortie* cible WASM.

---

## Ce qui fonctionne immediatement (aucune modification necessaire)

Ces fonctionnalites Hemlock se compilent en C standard que Emscripten gere nativement :

- Tous les operateurs arithmetiques, bit a bit, logiques
- Variables, portee, closures
- Fonctions, recursivite, fonctions a corps d'expression
- if/else, while, for, loop, switch, pattern matching
- Objets, tableaux, chaines (toutes les 19+23 methodes)
- Annotations de type et verification de type a l'execution
- Try/catch/finally/throw
- Defer
- Chaines de modele
- Coalescence null (`??`, `?.`, `??=`)
- Arguments nommes
- Types composes, alias de type
- `print()`, `eprint()` (via le mapping console d'Emscripten)
- `alloc()`/`free()`/`buffer()` (memoire lineaire)
- `typeof()`, `len()`, `sizeof()`
- Builtins math (sin, cos, sqrt, etc.)
- Tout le comptage de references / gestion memoire

---

## Estimation de la portee par phase

| Phase | Portee | Dependances |
|-------|--------|-------------|
| **Phase 1** | ~800 lignes de nouveau C, ~200 lignes de gardes #ifdef, modifications Makefile | SDK Emscripten |
| **Phase 2** | ~200 lignes C, tests stdlib, Makefile | Phase 1 |
| **Phase 3** | ~600 lignes C (pont), ~200 lignes Hemlock (stdlib) | Phase 1 |
| **Phase 4** | ~1000 lignes C (threading Worker), complexe | Phase 1+3 |

Ordre recommande : Phase 1 → Phase 2 → Phase 3 → Phase 4

La Phase 1 seule vous donne un "Hemlock dans le navigateur" utile pour les charges de travail computationnelles. Les Phases 2-4 ajoutent progressivement l'E/S et l'interoperabilite.
