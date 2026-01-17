# Architecture

Architecture interne et conception de hpm. Ce document est destine aux contributeurs et a ceux qui souhaitent comprendre comment fonctionne hpm.

## Apercu

hpm est ecrit en Hemlock et se compose de plusieurs modules qui gerent differents aspects de la gestion des paquets :

```
src/
├── main.hml        # Point d'entree CLI et routage des commandes
├── manifest.hml    # Gestion de package.json
├── lockfile.hml    # Gestion de package-lock.json
├── semver.hml      # Versionnage semantique
├── resolver.hml    # Resolution des dependances
├── github.hml      # Client API GitHub
├── installer.hml   # Telechargement et extraction des paquets
└── cache.hml       # Gestion du cache global
```

## Responsabilites des modules

### main.hml

Le point d'entree de l'application CLI.

**Responsabilites :**
- Analyser les arguments de ligne de commande
- Router les commandes vers les gestionnaires appropries
- Afficher l'aide et les informations de version
- Gerer les options globales (--verbose, --dry-run, etc.)
- Sortir avec les codes appropries

**Fonctions principales :**
- `main()` - Point d'entree, analyse les args et dispatche les commandes
- `cmd_init()` - Gerer `hpm init`
- `cmd_install()` - Gerer `hpm install`
- `cmd_uninstall()` - Gerer `hpm uninstall`
- `cmd_update()` - Gerer `hpm update`
- `cmd_list()` - Gerer `hpm list`
- `cmd_outdated()` - Gerer `hpm outdated`
- `cmd_run()` - Gerer `hpm run`
- `cmd_why()` - Gerer `hpm why`
- `cmd_cache()` - Gerer `hpm cache`

**Raccourcis de commandes :**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Gere la lecture et l'ecriture des fichiers `package.json`.

**Responsabilites :**
- Lire/ecrire package.json
- Valider la structure du paquet
- Gerer les dependances
- Analyser les specificateurs de paquets (owner/repo@version)

**Fonctions principales :**
```hemlock
create_default(): Manifest           // Creer un manifeste vide
read_manifest(): Manifest            // Lire depuis le fichier
write_manifest(m: Manifest)          // Ecrire dans le fichier
validate(m: Manifest): bool          // Valider la structure
get_all_dependencies(m): Map         // Obtenir deps + devDeps
add_dependency(m, pkg, ver, dev)     // Ajouter une dependance
remove_dependency(m, pkg)            // Supprimer une dependance
parse_specifier(spec): (name, ver)   // Analyser "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // Analyser "owner/repo"
```

**Structure Manifest :**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Gere le fichier `package-lock.json` pour des installations reproductibles.

**Responsabilites :**
- Creer/lire/ecrire les fichiers de verrouillage
- Suivre les versions exactes resolues
- Stocker les URLs de telechargement et les hashes d'integrite
- Elaguer les dependances orphelines

**Fonctions principales :**
```hemlock
create_empty(): Lockfile              // Creer un lockfile vide
read_lockfile(): Lockfile             // Lire depuis le fichier
write_lockfile(l: Lockfile)           // Ecrire dans le fichier
create_entry(ver, url, hash, deps)    // Creer une entree de verrouillage
get_locked(l, pkg): LockEntry?        // Obtenir la version verrouillee
set_locked(l, pkg, entry)             // Definir la version verrouillee
remove_locked(l, pkg)                 // Supprimer une entree
prune(l, keep: Set)                   // Supprimer les orphelins
needs_update(l, m): bool              // Verifier si desynchronise
```

**Structure Lockfile :**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // URL de telechargement
    integrity: string,    // Hash SHA256
    dependencies: Map<string, string>
};
```

### semver.hml

Implementation complete du Versionnage semantique 2.0.0.

**Responsabilites :**
- Analyser les chaines de version
- Comparer les versions
- Analyser et evaluer les contraintes de version
- Trouver les versions satisfaisant les contraintes

**Fonctions principales :**
```hemlock
// Analyse
parse(s: string): Version             // "1.2.3-beta+build" -> Version
stringify(v: Version): string         // Version -> "1.2.3-beta+build"

// Comparaison
compare(a, b: Version): int           // -1, 0, ou 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Contraintes
parse_constraint(s: string): Constraint    // "^1.2.3" -> Constraint
satisfies(v: Version, c: Constraint): bool // Verifier si v correspond a c
max_satisfying(versions, c): Version?      // Trouver la plus haute correspondance
sort(versions): [Version]                  // Trier par ordre croissant

// Utilitaires
constraints_overlap(a, b: Constraint): bool  // Verifier la compatibilite
```

**Structure Version :**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // ex: ["beta", "1"]
    build: string?          // ex: "20230101"
};
```

**Types de contraintes :**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" -> >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" -> >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Plages combinees
    | Any;                     // "*"
```

### resolver.hml

Implemente la resolution de dependances style npm.

**Responsabilites :**
- Resoudre les arbres de dependances
- Detecter les conflits de version
- Detecter les dependances circulaires
- Construire des arbres de visualisation

**Fonctions principales :**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Resolveur principal : retourne une map plate de toutes les dependances avec versions resolues

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Trouver une version satisfaisant toutes les contraintes

detect_cycles(deps: Map): [Cycle]?
    // Trouver les dependances circulaires en utilisant DFS

build_tree(lockfile): Tree
    // Creer une structure d'arbre pour l'affichage

find_why(pkg, lockfile): [Chain]
    // Trouver les chaines de dependances expliquant pourquoi pkg est installe
```

**Algorithme de resolution :**

1. **Collecter les contraintes** : Parcourir le manifeste et les dependances transitives
2. **Resoudre chaque paquet** : Pour chaque paquet :
   - Obtenir toutes les contraintes de version des dependants
   - Recuperer les versions disponibles depuis GitHub
   - Trouver la version la plus haute satisfaisant TOUTES les contraintes
   - Erreur si aucune version ne satisfait toutes (conflit)
3. **Detecter les cycles** : Executer DFS pour trouver les dependances circulaires
4. **Retourner une map plate** : Nom du paquet -> info de version resolue

**Structure ResolveResult :**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

Client API GitHub pour la decouverte et le telechargement de paquets.

**Responsabilites :**
- Recuperer les versions disponibles (tags)
- Telecharger package.json depuis les depots
- Telecharger les tarballs de release
- Gerer l'authentification et les limites de taux

**Fonctions principales :**
```hemlock
get_token(): string?
    // Obtenir le token depuis env ou config

github_request(url, headers?): Response
    // Faire une requete API avec reessais

get_tags(owner, repo): [string]
    // Obtenir les tags de version (v1.0.0, v1.1.0, etc.)

get_package_json(owner, repo, ref): Manifest
    // Recuperer package.json a un tag/commit specifique

download_tarball(owner, repo, tag): bytes
    // Telecharger l'archive de release

repo_exists(owner, repo): bool
    // Verifier si le depot existe

get_repo_info(owner, repo): RepoInfo
    // Obtenir les metadonnees du depot
```

**Logique de reessai :**
- Backoff exponentiel : 1s, 2s, 4s, 8s
- Reessaie sur : 403 (limite de taux), 5xx (erreur serveur), erreurs reseau
- Maximum 4 reessais
- Signale clairement les erreurs de limite de taux

**Points de terminaison API utilises :**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Gere le telechargement et l'extraction des paquets.

**Responsabilites :**
- Telecharger les paquets depuis GitHub
- Extraire les tarballs vers hem_modules
- Verifier/utiliser les paquets en cache
- Installer/desinstaller les paquets

**Fonctions principales :**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Telecharger et installer un seul paquet

install_all(packages: Map, options): InstallResult
    // Installer tous les paquets resolus

uninstall_package(name: string): bool
    // Supprimer un paquet de hem_modules

get_installed(): Map<string, string>
    // Lister les paquets actuellement installes

verify_integrity(pkg): bool
    // Verifier l'integrite du paquet

prefetch_packages(packages: Map): void
    // Telechargement parallele vers le cache (experimental)
```

**Processus d'installation :**

1. Verifier si deja installe a la bonne version
2. Verifier le cache pour le tarball
3. Si pas en cache, telecharger depuis GitHub
4. Stocker dans le cache pour utilisation future
5. Extraire vers `hem_modules/owner/repo/`
6. Verifier l'installation

**Structure de repertoire creee :**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Gere le cache global des paquets.

**Responsabilites :**
- Stocker les tarballs telecharges
- Recuperer les paquets en cache
- Lister les paquets en cache
- Vider le cache
- Gerer la configuration

**Fonctions principales :**
```hemlock
get_cache_dir(): string
    // Obtenir le repertoire de cache (respecte HPM_CACHE_DIR)

get_config_dir(): string
    // Obtenir le repertoire de config (~/.hpm)

is_cached(owner, repo, version): bool
    // Verifier si le tarball est en cache

get_cached_path(owner, repo, version): string
    // Obtenir le chemin vers le tarball en cache

store_tarball_file(owner, repo, version, data): void
    // Sauvegarder le tarball dans le cache

list_cached(): [CachedPackage]
    // Lister tous les paquets en cache

clear_cache(): int
    // Supprimer tous les paquets en cache, retourner les octets liberes

get_cache_size(): int
    // Calculer la taille totale du cache

read_config(): Config
    // Lire ~/.hpm/config.json

write_config(c: Config): void
    // Ecrire le fichier de config
```

**Structure du cache :**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Flux de donnees

### Flux de la commande Install

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Analyser les args, appeler cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Lire package.json, ajouter la dependance
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Resoudre toutes les dependances
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Obtenir versions, trouver satisfaisante
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Telecharger et extraire les paquets
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Telecharger ou utiliser le cache
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Mettre a jour package-lock.json
    └──────────┘
```

### Detail de l'algorithme de resolution

```
Entree: manifest.dependencies, manifest.devDependencies, lockfile existant

1. Initialiser:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [dependances directes]

2. Tant que queue non vide:
   a. pkg = queue.pop()
   b. Si pkg deja resolu, passer
   c. Obtenir toutes les contraintes pour pkg depuis les dependants
   d. Recuperer les versions disponibles depuis GitHub (en cache)
   e. Trouver la version max satisfaisant toutes les contraintes
   f. Si aucune trouvee: CONFLIT
   g. resolved[pkg] = {version, url, deps}
   h. Ajouter les dependances de pkg a la queue

3. Detecter les cycles dans le graphe resolu
   - Si cycle trouve: ERREUR

4. Retourner la map resolue
```

## Gestion des erreurs

### Codes de sortie

Definis dans main.hml :

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Propagation des erreurs

Les erreurs remontent via les valeurs de retour :

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propage
    // ...
}
```

## Tests

### Framework de test

Framework de test personnalise dans `test/framework.hml` :

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### Fichiers de test

- `test/test_semver.hml` - Analyse de version, comparaison, contraintes
- `test/test_manifest.hml` - Lecture/ecriture de manifeste, validation
- `test/test_lockfile.hml` - Operations sur le lockfile
- `test/test_cache.hml` - Gestion du cache

### Executer les tests

```bash
# Tous les tests
make test

# Tests specifiques
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Ameliorations futures

### Fonctionnalites prevues

1. **Verification d'integrite** - Verification complete du hash SHA256
2. **Workspaces** - Support des monorepos
3. **Systeme de plugins** - Commandes extensibles
4. **Audit** - Verification des vulnerabilites de securite
5. **Registre prive** - Hebergement de paquets auto-heberge

### Limitations connues

1. **Bug du bundler** - Ne peut pas creer d'executable autonome
2. **Telechargements paralleles** - Experimental, peut avoir des conditions de course
3. **Integrite** - SHA256 pas completement implemente

## Contribuer

### Style de code

- Utilisez une indentation de 4 espaces
- Les fonctions doivent faire une seule chose
- Commentez la logique complexe
- Ecrivez des tests pour les nouvelles fonctionnalites

### Ajouter une commande

1. Ajoutez un gestionnaire dans `main.hml` :
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementation
   }
   ```

2. Ajoutez au dispatch de commande :
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Mettez a jour le texte d'aide

### Ajouter un module

1. Creez `src/newmodule.hml`
2. Exportez l'interface publique
3. Importez dans les modules qui en ont besoin
4. Ajoutez des tests dans `test/test_newmodule.hml`

## Voir aussi

- [Commandes](commands.md) - Reference CLI
- [Creer des paquets](creating-packages.md) - Developpement de paquets
- [Versionnage](versioning.md) - Versionnage semantique
