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
