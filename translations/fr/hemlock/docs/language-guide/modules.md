# Systeme de modules Hemlock

Ce document decrit le systeme de modules import/export de style ES6 implemente pour Hemlock.

## Apercu

Hemlock supporte un systeme de modules base sur les fichiers avec une syntaxe import/export de style ES6. Les modules sont :
- **Singletons** : Chaque module est charge une fois et mis en cache
- **Bases sur les fichiers** : Les modules correspondent a des fichiers .hml sur disque
- **Explicitement importes** : Les dependances sont declarees avec des instructions import
- **Executes topologiquement** : Les dependances sont executees avant les dependants

Pour la gestion des paquets et les dependances tierces, voir [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Syntaxe

### Instructions d'export

**Exports nommes en ligne :**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**Liste d'export :**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Export Extern (fonctions FFI) :**
```hemlock
import "libc.so.6";

// Exporter des fonctions FFI pour utilisation dans d'autres modules
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

Voir [Documentation FFI](../advanced/ffi.md#exporting-ffi-functions) pour plus de details sur l'export des fonctions FFI.

**Export Define (types struct) :**
```hemlock
// Exporter des definitions de type struct
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**Important :** Les types struct exportes sont enregistres globalement quand le module est charge. Ils deviennent disponibles automatiquement quand vous importez quoi que ce soit du module - vous n'avez PAS besoin de (et ne pouvez pas) les importer explicitement par nom :

```hemlock
// BON - les types struct sont auto-disponibles apres tout import
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Fonctionne !

// MAUVAIS - impossible d'importer explicitement les types struct
import { Vector2 } from "./my_module.hml";  // Erreur : Undefined variable 'Vector2'
```

Voir [Documentation FFI](../advanced/ffi.md#exporting-struct-types) pour plus de details sur l'export des types struct.

**Re-exports :**
```hemlock
// Re-exporter depuis un autre module
export { add, subtract } from "./math.hml";
```

### Instructions d'import

**Imports nommes :**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Import d'espace de noms :**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**Alias :**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## Resolution de module

### Types de chemin

**Chemins relatifs :**
```hemlock
import { foo } from "./module.hml";       // Meme repertoire
import { bar } from "../parent.hml";      // Repertoire parent
import { baz } from "./sub/nested.hml";   // Sous-repertoire
```

**Chemins absolus :**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Gestion des extensions :**
- L'extension `.hml` peut etre omise - elle sera ajoutee automatiquement
- `./math` se resout en `./math.hml`

## Fonctionnalites

### Detection de dependance circulaire

Le systeme de modules detecte les dependances circulaires et signale une erreur :

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Mise en cache des modules

Les modules sont charges une fois et mis en cache. Plusieurs imports du meme module retournent la meme instance :

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // Meme instance !
print(count);  // Toujours 1 (etat partage)
```

### Immutabilite des imports

Les liaisons importees ne peuvent pas etre reassignees :

```hemlock
import { add } from "./math.hml";
add = fn() { };  // ERREUR : cannot reassign imported binding
```

## Details d'implementation

### Architecture

**Fichiers :**
- `include/module.h` - API du systeme de modules
- `src/module.c` - Chargement, mise en cache et execution des modules
- Support parser dans `src/parser.c`
- Support runtime dans `src/interpreter/runtime.c`

**Composants cles :**
1. **ModuleCache** : Maintient les modules charges indexes par chemin absolu
2. **Module** : Represente un module charge avec son AST et exports
3. **Resolution de chemin** : Resout les chemins relatifs/absolus en chemins canoniques
4. **Execution topologique** : Execute les modules dans l'ordre des dependances

### Processus de chargement des modules

1. **Phase d'analyse** : Tokeniser et analyser le fichier module
2. **Resolution des dependances** : Charger recursivement les modules importes
3. **Detection de cycle** : Verifier si le module est deja en cours de chargement
4. **Mise en cache** : Stocker le module dans le cache par chemin absolu
5. **Phase d'execution** : Executer dans l'ordre topologique (dependances d'abord)

### API

```c
// API haut niveau
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// API bas niveau
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Tests

Les modules de test sont situes dans `tests/modules/` et `tests/parity/modules/` :

- `math.hml` - Module basique avec exports
- `test_import_named.hml` - Test d'import nomme
- `test_import_namespace.hml` - Test d'import d'espace de noms
- `test_import_alias.hml` - Test d'alias d'import
- `export_extern.hml` - Test d'export extern de fonction FFI (Linux)

## Imports de paquets (hpm)

Avec [hpm](https://github.com/hemlang/hpm) installe, vous pouvez importer des paquets tiers depuis GitHub :

```hemlock
// Importer depuis la racine du paquet (utilise "main" de package.json)
import { app, router } from "hemlang/sprout";

// Importer depuis un sous-chemin
import { middleware } from "hemlang/sprout/middleware";

// Bibliotheque standard (integree a Hemlock)
import { HashMap } from "@stdlib/collections";
```

Les paquets sont installes dans `hem_modules/` et resolus en utilisant la syntaxe GitHub `owner/repo`.

```bash
# Installer un paquet
hpm install hemlang/sprout

# Installer avec contrainte de version
hpm install hemlang/sprout@^1.0.0
```

Voir la [documentation hpm](https://github.com/hemlang/hpm) pour tous les details.

## Limitations actuelles

1. **Pas d'imports dynamiques** : `import()` comme fonction runtime n'est pas supporte
2. **Pas d'exports conditionnels** : Les exports doivent etre au niveau superieur
3. **Chemins de bibliotheque statiques** : Les imports de bibliotheque FFI utilisent des chemins statiques (specifiques a la plateforme)

## Travaux futurs

- Imports dynamiques avec fonction `import()`
- Exports conditionnels
- Metadonnees de module (`import.meta`)
- Tree shaking et elimination de code mort

## Exemples

Voir `tests/modules/` pour des exemples fonctionnels du systeme de modules.

Exemple de structure de module :
```
project/
|-- main.hml
|-- lib/
|   |-- math.hml
|   |-- string.hml
|   |-- index.hml (module barrel)
|-- utils/
    |-- helpers.hml
```

Exemple d'utilisation :
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
