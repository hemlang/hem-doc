# Propriété de la Mémoire dans Hemlock

> "Nous vous donnons les outils pour être en sécurité, mais nous ne vous obligeons pas à les utiliser."

Ce document décrit la sémantique de propriété de la mémoire dans Hemlock, couvrant à la fois la mémoire gérée par le programmeur et les valeurs gérées par le runtime.

## Table des Matières

1. [Le Contrat](#le-contrat)
2. [Mémoire Gérée par le Programmeur](#mémoire-gérée-par-le-programmeur)
3. [Valeurs Gérées par le Runtime](#valeurs-gérées-par-le-runtime)
4. [Points de Transfert de Propriété](#points-de-transfert-de-propriété)
5. [Async et Concurrence](#async-et-concurrence)
6. [Règles de Mémoire FFI](#règles-de-mémoire-ffi)
7. [Sécurité des Exceptions](#sécurité-des-exceptions)
8. [Meilleures Pratiques](#meilleures-pratiques)

---

## Le Contrat

Hemlock a une division claire de la responsabilité de gestion de la mémoire :

| Type de Mémoire | Géré Par | Méthode de Nettoyage |
|-----------------|----------|----------------------|
| Pointeurs bruts (`ptr`) | **Programmeur** | `free(ptr)` |
| Buffers (`buffer`) | **Programmeur** | `free(buf)` |
| Strings, Arrays, Objets | **Runtime** | Automatique (comptage de références) |
| Fonctions, Closures | **Runtime** | Automatique (comptage de références) |
| Tasks, Channels | **Runtime** | Automatique (comptage de références) |

**Le principe fondamental :** Si vous l'allouez explicitement, vous le libérez explicitement. Tout le reste est géré automatiquement.

---

## Mémoire Gérée par le Programmeur

### Pointeurs Bruts

```hemlock
let p = alloc(64);       // Allouer 64 octets
memset(p, 0, 64);        // Initialiser
// ... utiliser la mémoire ...
free(p);                 // Votre responsabilité !
```

**Règles :**
- `alloc()` retourne de la mémoire que vous possédez
- Vous devez appeler `free()` quand vous avez terminé
- Le double-free plantera (intentionnellement)
- L'use-after-free est un comportement indéfini
- L'arithmétique des pointeurs est permise mais non vérifiée

### Allocation Typée

```hemlock
let arr = talloc("i32", 100);  // Allouer 100 i32s (400 octets)
ptr_write_i32(arr, 0, 42);     // Écrire à l'index 0
let val = ptr_read_i32(arr, 0); // Lire depuis l'index 0
free(arr);                      // Toujours votre responsabilité
```

### Buffers (Alternative Sûre)

```hemlock
let buf = buffer(64);    // Buffer avec vérification des limites
buf[0] = 42;             // Indexation sûre
// buf[100] = 1;         // Erreur d'exécution : hors limites
free(buf);               // Nécessite toujours un free explicite
```

**Différence clé :** Les buffers fournissent une vérification des limites, pas les pointeurs bruts.

---

## Valeurs Gérées par le Runtime

### Comptage de Références

Les valeurs allouées sur le tas utilisent un comptage de références atomique :

```hemlock
let s1 = "hello";        // String alloué, refcount = 1
let s2 = s1;             // s2 partage s1, refcount = 2
// Quand les deux sortent du scope, refcount → 0, mémoire libérée
```

**Types avec comptage de références :**
- `string` - Texte UTF-8
- `array` - Arrays dynamiques
- `object` - Objets clé-valeur
- `function` - Closures
- `task` - Handles de tâches async
- `channel` - Canaux de communication

### Détection de Cycles

Le runtime gère les cycles dans les graphes d'objets :

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // Cycle : a → b → a
// Le runtime utilise des ensembles visités pour détecter et briser les cycles pendant le nettoyage
```

---

## Points de Transfert de Propriété

### Liaison de Variables

```hemlock
let x = [1, 2, 3];       // Array créé avec refcount 1
                         // x possède la référence
```

### Retours de Fonctions

```hemlock
fn make_array() {
    return [1, 2, 3];    // La propriété de l'array est transférée à l'appelant
}
let arr = make_array();  // arr possède maintenant la référence
```

### Assignation

```hemlock
let a = "hello";
let b = a;               // Référence partagée (refcount incrémenté)
b = "world";             // a a toujours "hello", b a "world"
```

### Opérations de Channel

```hemlock
let ch = channel(10);
ch.send("message");      // Valeur copiée dans le buffer du channel
                         // L'original reste valide

let msg = ch.recv();     // Reçoit la propriété du channel
```

### Spawning de Tasks

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data est COPIÉ EN PROFONDEUR pour l'isolation
data.x = 2;                       // Sûr - le task a sa propre copie
let result = join(task);          // La propriété du result est transférée à l'appelant
```

---

## Async et Concurrence

### Isolation des Threads

Les tasks spawnés reçoivent des **copies profondes** des arguments mutables :

```hemlock
async fn worker(data) {
    data.x = 100;        // Modifie seulement la copie du task
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // Sûr - n'affecte pas le task
let result = join(task);
print(obj.x);            // 2 (inchangé par le task)
print(result.x);         // 100 (copie modifiée du task)
```

### Objets de Coordination Partagés

Certains types sont partagés par référence (non copiés) :
- **Channels** - Pour la communication inter-tasks
- **Tasks** - Pour la coordination (join/detach)

```hemlock
let ch = channel(1);
spawn(producer, ch);     // Même channel, pas une copie
spawn(consumer, ch);     // Les deux tasks partagent le channel
```

### Résultats des Tasks

```hemlock
let task = spawn(compute);
let result = join(task);  // L'appelant possède le résultat
                          // La référence du task est libérée quand le task est libéré
```

### Tasks Détachés

```hemlock
detach(spawn(background_work));
// Le task s'exécute indépendamment
// Le résultat est automatiquement libéré quand le task se termine
// Pas de fuite même si personne n'appelle join()
```

---

## Règles de Mémoire FFI

### Passer aux Fonctions C

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock conserve la propriété
                         // Le string est valide pendant l'appel
                         // La fonction C ne doit PAS le libérer
```

### Recevoir des Fonctions C

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C a alloué cette mémoire
free(copy);                   // Votre responsabilité de libérer
```

### Passage de Structs (Compilateur Seulement)

```hemlock
// Définir le layout de struct C
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // Retourné par valeur, copié
                                // Pas de nettoyage nécessaire pour les structs sur la pile
```

### Mémoire des Callbacks

```hemlock
// Quand C rappelle Hemlock :
// - Les arguments appartiennent à C (ne pas libérer)
// - La propriété de la valeur de retour est transférée à C
```

---

## Sécurité des Exceptions

### Garanties

Le runtime fournit ces garanties :

1. **Pas de fuite en sortie normale** - Toutes les valeurs gérées par le runtime sont nettoyées
2. **Pas de fuite en exception** - Les temporaires sont libérés pendant le déroulement de la pile
3. **Defer s'exécute en exception** - Le code de nettoyage s'exécute

### Évaluation d'Expressions

```hemlock
// Si cela lance pendant la création de l'array :
let arr = [f(), g(), h()];  // L'array partiel est libéré

// Si cela lance pendant l'appel de fonction :
foo(a(), b(), c());         // Les args précédemment évalués sont libérés
```

### Defer pour le Nettoyage

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // S'exécute au return OU à l'exception

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close() s'exécute quand même !
    }
    return data;
}
```

---

## Meilleures Pratiques

### 1. Préférez les Types Gérés par le Runtime

```hemlock
// Préférez ceci :
let data = [1, 2, 3, 4, 5];

// À ceci (sauf si vous avez besoin de contrôle bas niveau) :
let data = talloc("i32", 5);
// ... doit se souvenir de libérer ...
```

### 2. Utilisez Defer pour la Mémoire Manuelle

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // Nettoyage garanti

    // ... utiliser buf ...
    // Pas besoin de libérer à chaque point de retour
}
```

### 3. Évitez les Pointeurs Bruts en Async

```hemlock
// FAUX - le pointeur peut être libéré avant que le task se termine
let p = alloc(64);
spawn(worker, p);          // Le task obtient la valeur du pointeur
free(p);                   // Oups ! Le task l'utilise encore

// CORRECT - utilisez des channels ou copiez les données
let ch = channel(1);
let data = buffer(64);
// ... remplir data ...
ch.send(data);             // Copie profonde
spawn(worker, ch);
free(data);                // Sûr - le task a sa propre copie
```

### 4. Fermez les Channels Quand Vous Avez Terminé

```hemlock
let ch = channel(10);
// ... utiliser le channel ...
ch.close();                // Vide et libère les valeurs en buffer
```

### 5. Join ou Detach les Tasks

```hemlock
let task = spawn(work);

// Option 1 : Attendre le résultat
let result = join(task);

// Option 2 : Fire and forget
// detach(task);

// NE PAS : Laisser le handle du task sortir du scope sans join ou detach
// (Il sera nettoyé, mais le résultat peut fuir)
```

---

## Déboguer les Problèmes de Mémoire

### Activer ASAN

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### Exécuter les Tests de Régression de Fuites

```bash
make leak-regression       # Suite complète
make leak-regression-quick # Sauter le test exhaustif
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## Résumé

| Opération | Comportement Mémoire |
|-----------|---------------------|
| `alloc(n)` | Alloue, vous libérez |
| `buffer(n)` | Alloue avec vérification des limites, vous libérez |
| `"string"` | Le runtime gère |
| `[array]` | Le runtime gère |
| `{object}` | Le runtime gère |
| `spawn(fn)` | Copie profonde des args, le runtime gère le task |
| `join(task)` | L'appelant possède le résultat |
| `detach(task)` | Le runtime libère le résultat quand terminé |
| `ch.send(v)` | Copie la valeur dans le channel |
| `ch.recv()` | L'appelant possède la valeur reçue |
| `ch.close()` | Vide et libère les valeurs en buffer |
