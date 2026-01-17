# Guide de test pour Hemlock

Ce guide explique la philosophie de test de Hemlock, comment écrire des tests et comment exécuter la suite de tests.

---

## Table des matières

- [Philosophie de test](#philosophie-de-test)
- [Structure de la suite de tests](#structure-de-la-suite-de-tests)
- [Exécuter les tests](#exécuter-les-tests)
- [Écrire des tests](#écrire-des-tests)
- [Catégories de tests](#catégories-de-tests)
- [Tests de fuites mémoire](#tests-de-fuites-mémoire)
- [Intégration continue](#intégration-continue)
- [Bonnes pratiques](#bonnes-pratiques)

---

## Philosophie de test

### Principes fondamentaux

**1. Développement piloté par les tests (TDD)**

Écrivez les tests **avant** d'implémenter les fonctionnalités :

```
1. Écrire un test qui échoue
2. Implémenter la fonctionnalité
3. Exécuter le test (devrait passer)
4. Refactoriser si nécessaire
5. Répéter
```

**Avantages :**
- Assure que les fonctionnalités fonctionnent réellement
- Prévient les régressions
- Documente le comportement attendu
- Rend le refactoring plus sûr

**2. Couverture complète**

Testez les cas de succès et d'échec :

```hemlock
// Cas de succès
let x: u8 = 255;  // Devrait fonctionner

// Cas d'échec
let y: u8 = 256;  // Devrait générer une erreur
```

**3. Testez tôt et souvent**

Exécutez les tests :
- Avant de committer du code
- Après avoir fait des modifications
- Avant de soumettre des pull requests
- Pendant la revue de code

**Règle :** Tous les tests doivent passer avant le merge.

### Quoi tester

**Toujours tester :**
- La fonctionnalité de base (chemin heureux)
- Les conditions d'erreur (chemin malheureux)
- Les cas limites (conditions aux frontières)
- La vérification et les conversions de types
- La gestion de la mémoire (pas de fuites)
- La concurrence et les conditions de course

**Exemple de couverture de test :**
```hemlock
// Fonctionnalité : String.substr(start, length)

// Chemin heureux
print("hello".substr(0, 5));  // "hello"

// Cas limites
print("hello".substr(0, 0));  // "" (vide)
print("hello".substr(5, 0));  // "" (à la fin)
print("hello".substr(2, 100)); // "llo" (au-delà de la fin)

// Cas d'erreur
// "hello".substr(-1, 5);  // Erreur : index négatif
// "hello".substr(0, -1);  // Erreur : longueur négative
```

---

## Structure de la suite de tests

### Organisation des répertoires

```
tests/
├── run_tests.sh          # Script principal d'exécution des tests
├── primitives/           # Tests du système de types
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # Tests de conversion de types
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # Tests de pointeur/buffer
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # Tests d'opérations sur les chaînes
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # Tests de flux de contrôle
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # Tests de fonctions et closures
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # Tests d'objets
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # Tests d'opérations sur les tableaux
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # Tests de boucles
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # Tests de gestion des erreurs
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # Tests d'E/S de fichiers
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # Tests de concurrence
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # Tests FFI
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # Tests de gestion des signaux
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # Tests d'arguments en ligne de commande
    └── basic.hml
```

### Nommage des fichiers de test

**Conventions :**
- Utiliser des noms descriptifs : `method_chaining.hml` pas `test1.hml`
- Grouper les tests liés : `string_substr.hml`, `string_slice.hml`
- Un domaine fonctionnel par fichier
- Garder les fichiers ciblés et petits

---

## Exécuter les tests

### Exécuter tous les tests

```bash
# Depuis le répertoire racine de hemlock
make test

# Ou directement
./tests/run_tests.sh
```

**Sortie :**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### Exécuter une catégorie spécifique

```bash
# Exécuter seulement les tests de chaînes
./tests/run_tests.sh tests/strings/

# Exécuter un seul fichier de test
./tests/run_tests.sh tests/strings/concat.hml

# Exécuter plusieurs catégories
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Exécuter avec Valgrind (vérification des fuites mémoire)

```bash
# Vérifier un seul test pour les fuites
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# Vérifier tous les tests (lent !)
for test in tests/**/*.hml; do
    echo "Test de $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### Déboguer les tests échoués

```bash
# Exécuter avec sortie détaillée
./hemlock tests/failing_test.hml

# Exécuter avec gdb
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # si ça plante
```

---

## Écrire des tests

### Format des fichiers de test

Les fichiers de test sont simplement des programmes Hemlock avec une sortie attendue :

**Exemple : tests/primitives/integers.hml**
```hemlock
// Test des littéraux entiers basiques
let x = 42;
print(x);  // Attendu : 42

let y: i32 = 100;
print(y);  // Attendu : 100

// Test de l'arithmétique
let sum = x + y;
print(sum);  // Attendu : 142

// Test de l'inférence de type
let small = 10;
print(typeof(small));  // Attendu : i32

let large = 5000000000;
print(typeof(large));  // Attendu : i64
```

**Comment fonctionnent les tests :**
1. Le lanceur de tests exécute le fichier .hml
2. Capture la sortie stdout
3. Compare avec la sortie attendue (depuis les commentaires ou un fichier .out séparé)
4. Rapporte succès/échec

### Méthodes pour la sortie attendue

**Méthode 1 : Commentaires en ligne (recommandée pour les tests simples)**

```hemlock
print("hello");  // Attendu : hello
print(42);       // Attendu : 42
```

Le lanceur de tests analyse les commentaires `// Attendu : ...`.

**Méthode 2 : Fichier .out séparé**

Créez `nom_test.hml.out` avec la sortie attendue :

**nom_test.hml :**
```hemlock
print("ligne 1");
print("ligne 2");
print("ligne 3");
```

**nom_test.hml.out :**
```
ligne 1
ligne 2
ligne 3
```

### Tester les cas d'erreur

Les tests d'erreur devraient faire sortir le programme avec un statut non-zéro :

**Exemple : tests/primitives/range_error.hml**
```hemlock
// Cela devrait échouer avec une erreur de type
let x: u8 = 256;  // Hors plage pour u8
```

**Comportement attendu :**
- Le programme sort avec un statut non-zéro
- Affiche un message d'erreur sur stderr

**Gestion par le lanceur de tests :**
- Les tests attendant des erreurs devraient être dans des fichiers séparés
- Utiliser la convention de nommage : `*_error.hml` ou `*_fail.hml`
- Documenter l'erreur attendue dans les commentaires

### Tester les cas de succès

**Exemple : tests/strings/methods.hml**
```hemlock
// Test de substr
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Attendu : world

// Test de find
let pos = s.find("world");
print(pos);  // Attendu : 6

// Test de contains
let has = s.contains("lo");
print(has);  // Attendu : true

// Test de trim
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Attendu : hello
```

### Tester les cas limites

**Exemple : tests/arrays/edge_cases.hml**
```hemlock
// Tableau vide
let empty = [];
print(empty.length);  // Attendu : 0

// Élément unique
let single = [42];
print(single[0]);  // Attendu : 42

// Index négatif (devrait générer une erreur dans un fichier de test séparé)
// print(single[-1]);  // Erreur

// Index au-delà de la fin (devrait générer une erreur)
// print(single[100]);  // Erreur

// Conditions aux frontières
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Attendu : [] (vide)
print(arr.slice(3, 3));  // Attendu : [] (vide)
print(arr.slice(1, 2));  // Attendu : [2]
```

### Tester le système de types

**Exemple : tests/conversions/promotion.hml**
```hemlock
// Test de la promotion de type dans les opérations binaires

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Attendu : i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Attendu : f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Attendu : i32
```

### Tester la concurrence

**Exemple : tests/async/basic.hml**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Lancer des tâches
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// Joindre et afficher les résultats
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Attendu : 45
print(r2);  // Attendu : 190
```

### Tester les exceptions

**Exemple : tests/exceptions/try_catch.hml**
```hemlock
// Test du try/catch basique
try {
    throw "message d'erreur";
} catch (e) {
    print("Capturé : " + e);  // Attendu : Capturé : message d'erreur
}

// Test de finally
let executed = false;
try {
    print("try");  // Attendu : try
} finally {
    executed = true;
    print("finally");  // Attendu : finally
}

// Test de la propagation des exceptions
fn risky(): i32 {
    throw "échec";
}

try {
    risky();
} catch (e) {
    print(e);  // Attendu : échec
}
```

---

## Catégories de tests

### Tests des primitives

**Quoi tester :**
- Types entiers (i8, i16, i32, i64, u8, u16, u32, u64)
- Types flottants (f32, f64)
- Type booléen
- Type chaîne
- Type rune
- Type null

**Exemples de domaines :**
- Syntaxe des littéraux
- Inférence de type
- Vérification de plage
- Comportement de débordement
- Annotations de type

### Tests de conversion

**Quoi tester :**
- Promotion de type implicite
- Conversion de type explicite
- Conversions avec perte (devraient générer une erreur)
- Promotion de type dans les opérations
- Comparaisons inter-types

### Tests mémoire

**Quoi tester :**
- Exactitude de alloc/free
- Création et accès aux buffers
- Vérification des limites sur les buffers
- memset, memcpy, realloc
- Détection des fuites mémoire (valgrind)

### Tests de chaînes

**Quoi tester :**
- Concaténation
- Les 18 méthodes de chaîne
- Gestion UTF-8
- Indexation par rune
- Concaténation chaîne + rune
- Cas limites (chaînes vides, caractère unique, etc.)

### Tests de flux de contrôle

**Quoi tester :**
- if/else/else if
- Boucles while
- Boucles for
- Instructions switch
- break/continue
- Instructions return

### Tests de fonctions

**Quoi tester :**
- Définition et appel de fonctions
- Passage de paramètres
- Valeurs de retour
- Récursion
- Closures et capture
- Fonctions de première classe
- Fonctions anonymes

### Tests d'objets

**Quoi tester :**
- Littéraux d'objets
- Accès et affectation de champs
- Méthodes et liaison de self
- Duck typing
- Champs optionnels
- Sérialisation/désérialisation JSON
- Détection des références circulaires

### Tests de tableaux

**Quoi tester :**
- Création de tableaux
- Indexation et affectation
- Les 15 méthodes de tableau
- Types mixtes
- Redimensionnement dynamique
- Cas limites (vide, élément unique)

### Tests d'exceptions

**Quoi tester :**
- try/catch/finally
- Instruction throw
- Propagation des exceptions
- try/catch imbriqués
- Return dans try/catch/finally
- Exceptions non capturées

### Tests d'E/S

**Quoi tester :**
- Modes d'ouverture de fichiers
- Opérations de lecture/écriture
- Seek/tell
- Propriétés de fichier
- Gestion des erreurs (fichiers manquants, etc.)
- Nettoyage des ressources

### Tests async

**Quoi tester :**
- spawn/join/detach
- Envoi/réception sur canal
- Propagation des exceptions dans les tâches
- Tâches concurrentes multiples
- Comportement de blocage des canaux

### Tests FFI

**Quoi tester :**
- dlopen/dlclose
- dlsym
- dlcall avec différents types
- Conversion de types
- Gestion des erreurs

---

## Tests de fuites mémoire

### Utilisation de Valgrind

**Utilisation basique :**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**Exemple de sortie (pas de fuites) :**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**Exemple de sortie (avec fuite) :**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### Sources courantes de fuites

**1. Appels free() manquants :**
```c
// MAUVAIS
char *str = malloc(100);
// ... utiliser str
// Oublié de libérer !

// BON
char *str = malloc(100);
// ... utiliser str
free(str);
```

**2. Pointeurs perdus :**
```c
// MAUVAIS
char *ptr = malloc(100);
ptr = malloc(200);  // Référence à la première allocation perdue !

// BON
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. Chemins d'exception :**
```c
// MAUVAIS
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // Fuite !
    }
    free(data);
}

// BON
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### Fuites acceptables connues

Quelques petites "fuites" sont des allocations de démarrage intentionnelles :

**Fonctions intégrées globales :**
```hemlock
// Les fonctions intégrées, types FFI et constantes sont alloués au démarrage
// et non libérés à la sortie (typiquement ~200 octets)
```

Ce ne sont pas de vraies fuites - ce sont des allocations uniques qui persistent pendant la durée de vie du programme et sont nettoyées par l'OS à la sortie.

---

## Intégration continue

### GitHub Actions (futur)

Une fois la CI configurée, tous les tests s'exécuteront automatiquement sur :
- Push sur la branche main
- Création/mise à jour de pull request
- Exécutions planifiées quotidiennes

**Workflow CI :**
1. Compiler Hemlock
2. Exécuter la suite de tests
3. Vérifier les fuites mémoire (valgrind)
4. Rapporter les résultats sur la PR

### Vérifications pré-commit

Avant de committer, exécutez :

```bash
# Compiler à neuf
make clean && make

# Exécuter tous les tests
make test

# Vérifier quelques tests pour les fuites
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## Bonnes pratiques

### À faire

**Écrivez les tests d'abord (TDD)**
```bash
1. Créer tests/feature/new_feature.hml
2. Implémenter la fonctionnalité dans src/
3. Exécuter les tests jusqu'à ce qu'ils passent
```

**Testez les succès et les échecs**
```hemlock
// Succès : tests/feature/success.hml
let result = do_thing();
print(result);  // Attendu : valeur attendue

// Échec : tests/feature/failure.hml
do_invalid_thing();  // Devrait générer une erreur
```

**Utilisez des noms de tests descriptifs**
```
Bon : tests/strings/substr_utf8_boundary.hml
Mauvais : tests/test1.hml
```

**Gardez les tests ciblés**
- Un domaine fonctionnel par fichier
- Configuration et assertions claires
- Code minimal

**Ajoutez des commentaires expliquant les tests complexes**
```hemlock
// Test que la closure capture la variable externe par référence
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // Modifier après la création de la closure
    return f();  // Devrait retourner 20, pas 10
}
```

**Testez les cas limites**
- Entrées vides
- Valeurs null
- Valeurs aux frontières (min/max)
- Grandes entrées
- Valeurs négatives

### À ne pas faire

**Ne sautez pas les tests**
- Tous les tests doivent passer avant le merge
- Ne commentez pas les tests qui échouent
- Corrigez le bug ou supprimez la fonctionnalité

**N'écrivez pas de tests qui dépendent les uns des autres**
```hemlock
// MAUVAIS : test2.hml dépend de la sortie de test1.hml
// Les tests devraient être indépendants
```

**N'utilisez pas de valeurs aléatoires dans les tests**
```hemlock
// MAUVAIS : Non-déterministe
let x = random();
print(x);  // Impossible de prédire la sortie

// BON : Déterministe
let x = 42;
print(x);  // Attendu : 42
```

**Ne testez pas les détails d'implémentation**
```hemlock
// MAUVAIS : Tester la structure interne
let obj = { x: 10 };
// Ne pas vérifier l'ordre interne des champs, la capacité, etc.

// BON : Tester le comportement
print(obj.x);  // Attendu : 10
```

**N'ignorez pas les fuites mémoire**
- Tous les tests devraient être propres selon valgrind
- Documentez les fuites connues/acceptables
- Corrigez les fuites avant le merge

### Maintenance des tests

**Quand mettre à jour les tests :**
- Le comportement de la fonctionnalité change
- Les corrections de bugs nécessitent de nouveaux cas de test
- Des cas limites sont découverts
- Améliorations de performance

**Quand supprimer des tests :**
- Fonctionnalité supprimée du langage
- Le test duplique une couverture existante
- Le test était incorrect

**Refactorisation des tests :**
- Grouper les tests liés ensemble
- Extraire le code de configuration commun
- Utiliser un nommage cohérent
- Garder les tests simples et lisibles

---

## Exemple de session de test

Voici un exemple complet d'ajout d'une fonctionnalité avec des tests :

### Fonctionnalité : Ajouter la méthode `array.first()`

**1. Écrire le test d'abord :**

```bash
# Créer le fichier de test
cat > tests/arrays/first_method.hml << 'EOF'
// Test de la méthode array.first()

// Cas basique
let arr = [1, 2, 3];
print(arr.first());  // Attendu : 1

// Élément unique
let single = [42];
print(single.first());  // Attendu : 42

// Tableau vide (devrait générer une erreur - fichier de test séparé)
// let empty = [];
// print(empty.first());  // Erreur
EOF
```

**2. Exécuter le test (devrait échouer) :**

```bash
./hemlock tests/arrays/first_method.hml
# Erreur : Méthode 'first' non trouvée sur array
```

**3. Implémenter la fonctionnalité :**

Modifier `src/interpreter/builtins.c` :

```c
// Ajouter la méthode array_first
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Erreur : Impossible d'obtenir le premier élément d'un tableau vide\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// Enregistrer dans la table des méthodes de tableau
// ... ajouter à l'enregistrement des méthodes de tableau
```

**4. Exécuter le test (devrait passer) :**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# Succès !
```

**5. Vérifier les fuites mémoire :**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. Exécuter la suite de tests complète :**

```bash
make test
# Total : 252 tests (251 + nouveau)
# Passés : 252
# Échoués : 0
```

**7. Committer :**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## Résumé

**Rappelez-vous :**
- Écrivez les tests d'abord (TDD)
- Testez les cas de succès et d'échec
- Exécutez tous les tests avant de committer
- Vérifiez les fuites mémoire
- Documentez les problèmes connus
- Gardez les tests simples et ciblés

**La qualité des tests est aussi importante que la qualité du code !**
