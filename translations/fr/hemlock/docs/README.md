# Documentation Hemlock

Bienvenue dans la documentation du langage de programmation Hemlock !

> Un petit langage non securise pour ecrire des choses non securisees en toute securite.

## Table des matieres

### Pour commencer
- [Installation](getting-started/installation.md) - Compiler et installer Hemlock
- [Demarrage rapide](getting-started/quick-start.md) - Votre premier programme Hemlock
- [Tutoriel](getting-started/tutorial.md) - Guide etape par etape des bases de Hemlock
- [Parcours d'apprentissage](getting-started/learning-paths.md) - Choisissez votre parcours d'apprentissage selon vos objectifs

### Nouveau en programmation ?
- [Glossaire](glossary.md) - Definitions en langage clair des termes de programmation

### Guide du langage
- [Apercu de la syntaxe](language-guide/syntax.md) - Syntaxe et structure de base
- [Systeme de types](language-guide/types.md) - Types primitifs, inference de type et conversions
- [Gestion de la memoire](language-guide/memory.md) - Pointeurs, buffers et memoire manuelle
- [Chaines](language-guide/strings.md) - Chaines UTF-8 et operations
- [Runes](language-guide/runes.md) - Points de code Unicode et gestion des caracteres
- [Flux de controle](language-guide/control-flow.md) - if/else, boucles, switch et operateurs
- [Fonctions](language-guide/functions.md) - Fonctions, closures et recursion
- [Objets](language-guide/objects.md) - Litteraux d'objet, methodes et duck typing
- [Tableaux](language-guide/arrays.md) - Tableaux dynamiques et operations
- [Gestion des erreurs](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [Modules](language-guide/modules.md) - Systeme d'import/export et imports de paquets

### Sujets avances
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Executer Hemlock dans le navigateur via Emscripten
- [Async et concurrence](advanced/async-concurrency.md) - Veritable multi-threading avec async/await
- [Empaquetage et packaging](advanced/bundling-packaging.md) - Creer des bundles et des executables autonomes
- [Interface de fonction etrangere](advanced/ffi.md) - Appeler des fonctions C depuis des bibliotheques partagees
- [E/S fichier](advanced/file-io.md) - Operations sur les fichiers et gestion des ressources
- [Gestion des signaux](advanced/signals.md) - Gestion des signaux POSIX
- [Arguments de ligne de commande](advanced/command-line-args.md) - Acceder aux arguments du programme
- [Execution de commandes](advanced/command-execution.md) - Executer des commandes shell
- [Profilage](advanced/profiling.md) - Temps CPU, suivi de la memoire et detection de fuites

### Reference API
- [Reference du systeme de types](reference/type-system.md) - Reference complete des types
- [Reference des operateurs](reference/operators.md) - Tous les operateurs et leur precedence
- [Fonctions integrees](reference/builtins.md) - Fonctions et constantes globales
- [API String](reference/string-api.md) - Methodes et proprietes des chaines
- [API Array](reference/array-api.md) - Methodes et proprietes des tableaux
- [API Memory](reference/memory-api.md) - Allocation et manipulation de la memoire
- [API File](reference/file-api.md) - Methodes d'E/S fichier
- [API Concurrency](reference/concurrency-api.md) - Taches et canaux

### Conception et philosophie
- [Philosophie de conception](design/philosophy.md) - Principes et objectifs fondamentaux
- [Details d'implementation](design/implementation.md) - Comment Hemlock fonctionne en interne

### Contribuer
- [Guide de contribution](contributing/guidelines.md) - Comment contribuer
- [Guide de test](contributing/testing.md) - Ecrire et executer des tests

## Reference rapide

### Hello World
```hemlock
print("Hello, World!");
```

### Types de base
```hemlock
let x: i32 = 42;           // 32-bit signed integer
let y: u8 = 255;           // 8-bit unsigned integer
let pi: f64 = 3.14159;     // 64-bit float
let name: string = "Alice"; // UTF-8 string
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode codepoint
```

### Gestion de la memoire
```hemlock
// Safe buffer (recommended)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Raw pointer (for experts)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### Async/Concurrence
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## Philosophie

Hemlock est **explicite plutot qu'implicite**, toujours :
- Les points-virgules sont obligatoires
- Gestion manuelle de la memoire (pas de GC)
- Annotations de type optionnelles avec verifications a l'execution
- Les operations non securisees sont autorisees (c'est votre responsabilite)

Nous vous donnons les outils pour etre en securite (`buffer`, annotations de type, verification des limites) mais nous ne vous forcons pas a les utiliser (`ptr`, memoire manuelle, operations non securisees).

## Obtenir de l'aide

- **Code source** : [Depot GitHub](https://github.com/hemlang/hemlock)
- **Gestionnaire de paquets** : [hpm](https://github.com/hemlang/hpm) - Hemlock Package Manager
- **Issues** : Signaler des bugs et demander des fonctionnalites
- **Exemples** : Voir le repertoire `examples/`
- **Tests** : Voir le repertoire `tests/` pour des exemples d'utilisation

## Licence

Hemlock est distribue sous la licence MIT.
