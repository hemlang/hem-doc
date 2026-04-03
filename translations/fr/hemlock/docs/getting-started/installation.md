# Installation

Ce guide vous aidera a compiler et installer Hemlock sur votre systeme.

## Installation rapide (Recommandee)

La maniere la plus simple d'installer Hemlock est d'utiliser le script d'installation en une ligne :

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Cela telecharge et installe le dernier binaire pre-compile pour votre plateforme (Linux ou macOS, x86_64 ou arm64).

### Options d'installation

```bash
# Installer vers un prefixe personnalise (par defaut : ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Installer une version specifique
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Installer et mettre a jour automatiquement le PATH du shell
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

Apres l'installation, verifiez qu'elle fonctionne :

```bash
hemlock --version
```

---

## Compilation depuis les sources

Si vous preferez compiler depuis les sources ou si les binaires pre-compiles ne fonctionnent pas pour votre systeme, suivez les instructions ci-dessous.

## Prerequis

### Dependances requises

Hemlock necessite les dependances suivantes pour la compilation :

- **Compilateur C** : GCC ou Clang (standard C11)
- **Make** : GNU Make
- **libffi** : Bibliotheque d'interface de fonction etrangere (FFI - Foreign Function Interface) (pour le support FFI)
- **OpenSSL** : Bibliotheque cryptographique (pour les fonctions de hachage : md5, sha1, sha256)
- **libwebsockets** : Support client/serveur WebSocket et HTTP
- **zlib** : Bibliotheque de compression

### Installation des dependances

**macOS :**
```bash
# Installer Homebrew s'il n'est pas deja installe
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer les outils en ligne de commande Xcode
xcode-select --install

# Installer les dependances via Homebrew
brew install libffi openssl@3 libwebsockets
```

**Remarque pour les utilisateurs macOS** : Le Makefile detecte automatiquement les installations Homebrew et configure les chemins d'inclusion/bibliotheque corrects. Hemlock prend en charge les architectures Intel (x86_64) et Apple Silicon (arm64).

**Ubuntu/Debian :**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL :**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux :**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Compilation depuis les sources

### 1. Cloner le depot

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Compiler Hemlock

```bash
make
```

Cela compilera l'interpreteur Hemlock et placera l'executable dans le repertoire courant.

### 3. Verifier l'installation

```bash
./hemlock --version
```

Vous devriez voir les informations de version de Hemlock.

### 4. Tester la compilation

Executez la suite de tests pour vous assurer que tout fonctionne correctement :

```bash
make test
```

Tous les tests devraient reussir. Si vous constatez des echecs, veuillez les signaler en creant une issue.

## Installation systeme (Optionnel)

Pour installer Hemlock a l'echelle du systeme (par exemple, dans `/usr/local/bin`) :

```bash
sudo make install
```

Cela vous permet d'executer `hemlock` de n'importe ou sans specifier le chemin complet.

## Executer Hemlock

### REPL interactif

Demarrez la boucle lecture-evaluation-affichage (REPL - Read-Eval-Print Loop) :

```bash
./hemlock
```

Vous verrez une invite ou vous pouvez taper du code Hemlock :

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

Quittez le REPL avec `Ctrl+D` ou `Ctrl+C`.

### Executer des programmes

Executez un script Hemlock :

```bash
./hemlock program.hml
```

Avec des arguments en ligne de commande :

```bash
./hemlock program.hml arg1 arg2 "argument avec des espaces"
```

## Structure des repertoires

Apres la compilation, votre repertoire Hemlock ressemblera a ceci :

```
hemlock/
├── hemlock           # Executable de l'interpreteur compile
├── src/              # Code source
├── include/          # Fichiers d'en-tete
├── tests/            # Suite de tests
├── examples/         # Programmes d'exemple
├── docs/             # Documentation
├── stdlib/           # Bibliotheque standard
├── Makefile          # Configuration de compilation
└── README.md         # README du projet
```

## Compilation WebAssembly (WASM)

Hemlock peut etre compile en WebAssembly via [Emscripten](https://emscripten.org/), permettant a l'interpreteur complet de fonctionner dans un navigateur web ou Node.js.

### Installation d'Emscripten

Le SDK Emscripten (`emsdk`) fournit le compilateur `emcc` utilise pour compiler l'interpreteur WASM.

**Toutes les plateformes (Linux, macOS, Windows WSL) :**

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

Verifiez l'installation :

```bash
emcc --version
```

Vous devriez voir une sortie comme `emcc (Emscripten gcc/clang-like replacement ...) 3.x.x`.

Pour des instructions detaillees, consultez le [guide de demarrage d'Emscripten](https://emscripten.org/docs/getting_started/downloads.html).

**Optionnel : Ajouter au profil du shell**

Pour eviter d'executer `source emsdk_env.sh` a chaque fois, ajoutez-le a votre profil de shell :

```bash
# For bash (~/.bashrc or ~/.bash_profile)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.bashrc

# For zsh (~/.zshrc)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.zshrc
```

### Dependances WASM

La compilation WASM a moins de dependances que la compilation native. Emscripten fournit ses propres versions des bibliotheques C standard. Les bibliotheques natives suivantes ne sont **pas necessaires** (et ne sont pas disponibles) dans la compilation WASM :

| Bibliotheque | Native | WASM | Notes |
|---------|--------|------|-------|
| libffi | Requise | Stub | FFI n'est pas disponible en WASM |
| OpenSSL | Requise | Stub | Les builtins de cryptographie retournent des erreurs en WASM |
| libwebsockets | Optionnelle | Stub | Support WebSocket non disponible |
| zlib | Requise | Emscripten la fournit | Liee automatiquement avec `-sUSE_ZLIB=1` |
| pthreads | Requise | Optionnelle | Disponible avec une compilation threadee (necessite SharedArrayBuffer) |

**En resume :** Vous avez seulement besoin du SDK Emscripten installe. Aucune bibliotheque systeme supplementaire n'est requise pour la compilation WASM.

### Compilation de l'interpreteur WASM

```bash
# Build the interpreter as WebAssembly
make wasm-interpreter
```

Cela produit deux fichiers dans le repertoire `wasm/` :

| Fichier | Description |
|------|-------------|
| `wasm/hemlock.js` | Chargeur JavaScript et code de liaison Emscripten |
| `wasm/hemlock.wasm` | Module binaire WebAssembly |

### Execution dans Node.js

```bash
node -- wasm/hemlock.js -e 'print("Hello from WASM!");'
node -- wasm/hemlock.js examples/fibonacci.hml
```

### Execution dans un navigateur

Les fichiers WASM doivent etre servis via HTTP avec le type MIME correct (`application/wasm`). L'ouverture directe du fichier HTML via `file://` ne fonctionnera pas.

**En utilisant l'exemple inclus :**

```bash
make wasm-browser-example
# Opens http://localhost:8080/examples/wasm-browser/index.html
```

**Ou manuellement avec Python :**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/wasm/playground.html
```

**Ou manuellement avec Node.js :**

```bash
npx serve .
# Open the URL shown in the terminal
```

Voir `examples/wasm-browser/` pour un exemple complet d'integration navigateur avec un editeur de code interactif.

### Limitations WASM

Certaines fonctionnalites ne sont pas disponibles dans l'environnement WASM :

- **FFI** - Pas de chargement de bibliotheques partagees (`dlopen`/`dlsym`)
- **Cryptographie** - Pas d'OpenSSL (`sha256`, `md5`, etc. retournent des erreurs)
- **E/S fichier** - Pas d'acces au systeme de fichiers natif (uniquement le FS virtuel d'Emscripten)
- **Reseau** - Pas de sockets bruts ni de client HTTP
- **Signaux** - Pas de gestion des signaux POSIX
- **Processus** - Pas de `fork`, `exec` ni de gestion de processus
- **Threading** - `spawn`/`join`/canaux necessitent une compilation WASM threadee avec `SharedArrayBuffer`

Toutes les fonctionnalites principales du langage fonctionnent : variables, fonctions, closures, objets, tableaux, pattern matching, annotations de type, try/catch et la bibliotheque standard complete des modules Hemlock purs.

### Compilation de programmes Hemlock en WASM

En plus d'executer l'interpreteur en WASM, vous pouvez compiler des programmes Hemlock individuels en binaires WASM autonomes en utilisant le backend du compilateur :

```bash
# Compile a Hemlock program to WASM (requires both hemlockc and Emscripten)
make wasm-compile FILE=program.hml

# With threading support
make wasm-compile-threaded FILE=program.hml
```

Cela utilise `hemlockc` pour generer du code C, puis Emscripten pour le compiler en WASM.

## Options de compilation

### Compilation de debogage

Compiler avec les symboles de debogage et sans optimisation :

```bash
make debug
```

### Nettoyage de la compilation

Supprimer tous les fichiers compiles :

```bash
make clean
```

Recompiler depuis zero :

```bash
make clean && make
```

## Depannage

### macOS : Erreurs de bibliotheque introuvable

Si vous obtenez des erreurs concernant des bibliotheques manquantes (`-lcrypto`, `-lffi`, etc.) :

1. Assurez-vous que les dependances Homebrew sont installees :
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Verifiez les chemins Homebrew :
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Le Makefile devrait detecter automatiquement ces chemins. Si ce n'est pas le cas, verifiez que `brew` est dans votre PATH :
   ```bash
   which brew
   ```

### macOS : Erreurs de types BSD (`u_int`, `u_char` non trouves)

Si vous voyez des erreurs concernant des noms de types inconnus comme `u_int` ou `u_char` :

1. Cela a ete corrige dans v1.0.0+ en utilisant `_DARWIN_C_SOURCE` au lieu de `_POSIX_C_SOURCE`
2. Assurez-vous d'avoir la derniere version du code
3. Nettoyez et recompilez :
   ```bash
   make clean && make
   ```

### Linux : libffi non trouve

Si vous obtenez des erreurs concernant `ffi.h` manquant ou `-lffi` :

1. Assurez-vous que `libffi-dev` est installe (voir les dependances ci-dessus)
2. Verifiez si `pkg-config` peut le trouver :
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. S'il n'est pas trouve, vous devrez peut-etre definir `PKG_CONFIG_PATH` :
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Erreurs de compilation

Si vous rencontrez des erreurs de compilation :

1. Assurez-vous d'avoir un compilateur compatible C11
2. Sur macOS, essayez d'utiliser Clang (par defaut) :
   ```bash
   make CC=clang
   ```
3. Sur Linux, essayez d'utiliser GCC :
   ```bash
   make CC=gcc
   ```
4. Verifiez que toutes les dependances sont installees
5. Essayez de recompiler depuis zero :
   ```bash
   make clean && make
   ```

### Echecs de tests

Si les tests echouent :

1. Verifiez que vous avez la derniere version du code
2. Essayez de recompiler depuis zero :
   ```bash
   make clean && make test
   ```
3. Sur macOS, assurez-vous d'avoir les derniers outils en ligne de commande Xcode :
   ```bash
   xcode-select --install
   ```
4. Signalez le probleme sur GitHub avec :
   - Votre plateforme (version macOS / distribution Linux)
   - Architecture (x86_64 / arm64)
   - Sortie des tests
   - Sortie de `make -v` et `gcc --version` (ou `clang --version`)

## Prochaines etapes

- [Guide de demarrage rapide](quick-start.md) - Ecrivez votre premier programme Hemlock
- [Tutoriel](tutorial.md) - Apprenez Hemlock etape par etape
- [Guide du langage](../language-guide/syntax.md) - Explorez les fonctionnalites de Hemlock
