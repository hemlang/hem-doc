# Parcours d'apprentissage

Differents objectifs necessitent differentes connaissances. Choisissez le parcours qui correspond a ce que vous voulez construire.

---

## Parcours 1 : Scripts rapides et automatisation

**Objectif :** Ecrire des scripts pour automatiser des taches, traiter des fichiers et accomplir des choses.

**Temps jusqu'a la productivite :** Rapide - vous pouvez commencer a ecrire des scripts utiles immediatement.

### Ce que vous apprendrez

1. **[Demarrage rapide](quick-start.md)** - Votre premier programme, syntaxe de base
2. **[Chaines](../language-guide/strings.md)** - Traitement de texte, division, recherche
3. **[Tableaux](../language-guide/arrays.md)** - Listes, filtrage, transformation de donnees
4. **[E/S fichier](../advanced/file-io.md)** - Lecture et ecriture de fichiers
5. **[Arguments en ligne de commande](../advanced/command-line-args.md)** - Obtenir des entrees des utilisateurs

### A ignorer pour l'instant

- Gestion de la memoire (automatique pour les scripts)
- Async/concurrence (excessif pour les scripts simples)
- FFI (necessaire uniquement pour l'interoperabilite C)

### Projet d'exemple : Renommeur de fichiers

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// Renommer tous les fichiers .txt en .md
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Renomme : ${file} -> ${new_name}`);
    }
}
```

---

## Parcours 2 : Traitement et analyse de donnees

**Objectif :** Analyser des donnees, les transformer, generer des rapports.

**Temps jusqu'a la productivite :** Rapide - les methodes de chaines et de tableaux de Hemlock rendent cela facile.

### Ce que vous apprendrez

1. **[Demarrage rapide](quick-start.md)** - Bases
2. **[Chaines](../language-guide/strings.md)** - Analyse, division, formatage
3. **[Tableaux](../language-guide/arrays.md)** - map, filter, reduce pour la transformation de donnees
4. **[Objets](../language-guide/objects.md)** - Donnees structurees
5. **Bibliotheque standard :**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - Analyse JSON
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - Fichiers CSV
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - Operations sur fichiers

### Projet d'exemple : Analyseur CSV

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// Calculer le total des ventes
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Total des ventes : ${total} euros`);

// Trouver le meilleur vendeur
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Meilleure vente : ${top.product} - ${top.amount} euros`);
```

---

## Parcours 3 : Programmation web et reseau

**Objectif :** Construire des clients HTTP, travailler avec des API, creer des serveurs.

**Temps jusqu'a la productivite :** Moyen - necessite de comprendre les bases de l'asynchrone.

### Ce que vous apprendrez

1. **[Demarrage rapide](quick-start.md)** - Bases
2. **[Fonctions](../language-guide/functions.md)** - Callbacks et fermetures (closures)
3. **[Gestion des erreurs](../language-guide/error-handling.md)** - try/catch pour les erreurs reseau
4. **[Async et concurrence](../advanced/async-concurrency.md)** - spawn, await, channels
5. **Bibliotheque standard :**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - Requetes HTTP
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON pour les API
   - **[@stdlib/net](../../stdlib/docs/net.md)** - Sockets TCP/UDP
   - **[@stdlib/url](../../stdlib/docs/url.md)** - Analyse d'URL

### Projet d'exemple : Client API

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// Requete GET
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name} : ${user.email}`);
}

// Requete POST
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`Utilisateur cree avec l'ID : ${parse(result.body).id}`);
```

---

## Parcours 4 : Programmation systeme

**Objectif :** Ecrire du code bas niveau, travailler avec la memoire, interfacer avec des bibliotheques C.

**Temps jusqu'a la productivite :** Plus long - necessite de comprendre la gestion de la memoire.

### Ce que vous apprendrez

1. **[Demarrage rapide](quick-start.md)** - Bases
2. **[Types](../language-guide/types.md)** - Comprendre i32, u8, ptr, etc.
3. **[Gestion de la memoire](../language-guide/memory.md)** - alloc, free, buffers
4. **[FFI](../advanced/ffi.md)** - Appeler des fonctions C
5. **[Signaux](../advanced/signals.md)** - Gestion des signaux

### Concepts cles

**Liste de verification de la securite memoire :**
- [ ] Chaque `alloc()` a un `free()` correspondant
- [ ] Utiliser `buffer()` sauf si vous avez besoin d'un `ptr` brut
- [ ] Mettre les pointeurs a `null` apres liberation
- [ ] Utiliser `try/finally` pour garantir le nettoyage

**Correspondance des types pour FFI :**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long` (64 bits) |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### Projet d'exemple : Pool de memoire personnalise

```hemlock
// Allocateur simple par incrementations (bump allocator)
let pool_size = 1024 * 1024;  // 1 Mo
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool epuise";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// Utilisation
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // Reutiliser toute la memoire
pool_destroy();  // Nettoyer
```

---

## Parcours 5 : Programmes paralleles et concurrents

**Objectif :** Executer du code sur plusieurs coeurs CPU, construire des applications reactives.

**Temps jusqu'a la productivite :** Moyen - la syntaxe async est simple, mais raisonner sur le parallelisme demande de la pratique.

### Ce que vous apprendrez

1. **[Demarrage rapide](quick-start.md)** - Bases
2. **[Fonctions](../language-guide/functions.md)** - Fermetures (closures) (important pour l'async)
3. **[Async et concurrence](../advanced/async-concurrency.md)** - Plongee complete
4. **[Atomiques](../advanced/atomics.md)** - Programmation sans verrous (lock-free)

### Concepts cles

**Modele async de Hemlock :**
- `async fn` - Definir une fonction qui peut s'executer sur un autre thread
- `spawn(fn, args...)` - Commencer l'execution, retourne un handle de tache
- `join(task)` ou `await task` - Attendre la fin, obtenir le resultat
- `channel(size)` - Creer une file pour envoyer des donnees entre les taches

**Important :** Les taches recoivent des *copies* des valeurs. Si vous passez un pointeur, vous etes responsable de vous assurer que la memoire reste valide jusqu'a ce que la tache se termine.

### Projet d'exemple : Processeur de fichiers parallele

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// Traiter tous les fichiers en parallele
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// Collecter les resultats
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name} : ${count} lignes`);
    total_lines = total_lines + count;
}

print(`Total : ${total_lines} lignes`);
```

---

## Ce qu'il faut apprendre en premier (Tous les parcours)

Quel que soit votre objectif, commencez par ces fondamentaux :

### Semaine 1 : Bases essentielles
1. **[Demarrage rapide](quick-start.md)** - Ecrire et executer votre premier programme
2. **[Syntaxe](../language-guide/syntax.md)** - Variables, operateurs, flux de controle
3. **[Fonctions](../language-guide/functions.md)** - Definir et appeler des fonctions

### Semaine 2 : Manipulation des donnees
4. **[Chaines](../language-guide/strings.md)** - Manipulation de texte
5. **[Tableaux](../language-guide/arrays.md)** - Collections et iteration
6. **[Objets](../language-guide/objects.md)** - Donnees structurees

### Semaine 3 : Robustesse
7. **[Gestion des erreurs](../language-guide/error-handling.md)** - try/catch/throw
8. **[Modules](../language-guide/modules.md)** - Import/export, utilisation de la stdlib

### Ensuite : Choisissez votre parcours ci-dessus

---

## Aide-memoire : Venant d'autres langages

### Depuis Python

| Python | Hemlock | Notes |
|--------|---------|-------|
| `x = 42` | `let x = 42;` | Points-virgules obligatoires |
| `def fn():` | `fn name() { }` | Accolades obligatoires |
| `if x:` | `if (x) { }` | Parentheses et accolades obligatoires |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | Boucles for de style C |
| `for item in list:` | `for (item in array) { }` | For-in fonctionne pareil |
| `list.append(x)` | `array.push(x);` | Nom de methode different |
| `len(s)` | `s.length` ou `len(s)` | Les deux fonctionnent |
| Memoire automatique | Manuelle pour `ptr` | La plupart des types se nettoient automatiquement |

### Depuis JavaScript

| JavaScript | Hemlock | Notes |
|------------|---------|-------|
| `let x = 42` | `let x = 42;` | Pareil (points-virgules obligatoires) |
| `const x = 42` | `let x = 42;` | Pas de mot-cle const |
| `function fn()` | `fn name() { }` | Mot-cle different |
| `() => x` | `fn() { return x; }` | Pas de fonctions flechees |
| `async/await` | `async/await` | Meme syntaxe |
| `Promise` | `spawn/join` | Modele different |
| GC automatique | Manuel pour `ptr` | La plupart des types se nettoient automatiquement |

### Depuis C/C++

| C | Hemlock | Notes |
|---|---------|-------|
| `int x = 42;` | `let x: i32 = 42;` | Type apres les deux-points |
| `malloc(n)` | `alloc(n)` | Meme concept |
| `free(p)` | `free(p)` | Pareil |
| `char* s = "hi"` | `let s = "hi";` | Les chaines sont gerees |
| `#include` | `import { } from` | Imports de modules |
| Tout manuel | Auto pour la plupart des types | Seul `ptr` necessite une gestion manuelle |

---

## Obtenir de l'aide

- **[Glossaire](../glossary.md)** - Definitions des termes de programmation
- **[Exemples](../../examples/)** - Programmes complets fonctionnels
- **[Tests](../../tests/)** - Voir comment les fonctionnalites sont utilisees
- **GitHub Issues** - Poser des questions, signaler des bugs

---

## Niveaux de difficulte

Dans toute la documentation, vous verrez ces marqueurs :

| Marqueur | Signification |
|----------|---------------|
| **Debutant** | Aucune experience de programmation prealable necessaire |
| **Intermediaire** | Suppose des connaissances de base en programmation |
| **Avance** | Necessite une comprehension des concepts systeme |

Si quelque chose marque "Debutant" vous deroute, consultez le [Glossaire](../glossary.md) pour les definitions des termes.
