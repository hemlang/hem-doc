# Contribuer à Hemlock

Merci de votre intérêt pour contribuer à Hemlock ! Ce guide vous aidera à comprendre comment contribuer efficacement tout en maintenant la philosophie de conception et la qualité du code du langage.

---

## Table des matières

- [Avant de commencer](#avant-de-commencer)
- [Processus de contribution](#processus-de-contribution)
- [Directives de style de code](#directives-de-style-de-code)
- [Quoi contribuer](#quoi-contribuer)
- [Quoi NE PAS contribuer](#quoi-ne-pas-contribuer)
- [Modèles courants](#modèles-courants)
- [Ajouter de nouvelles fonctionnalités](#ajouter-de-nouvelles-fonctionnalités)
- [Processus de revue de code](#processus-de-revue-de-code)

---

## Avant de commencer

### Lectures obligatoires

Avant de contribuer, veuillez lire ces documents dans l'ordre :

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Comprendre les principes fondamentaux de Hemlock
2. **`/home/user/hemlock/docs/design/implementation.md`** - Apprendre la structure du code
3. **`/home/user/hemlock/docs/contributing/testing.md`** - Comprendre les exigences de test
4. **Ce document** - Apprendre les directives de contribution

### Prérequis

**Connaissances requises :**
- Programmation C (pointeurs, gestion de la mémoire, structures)
- Bases des compilateurs/interpréteurs (lexing, parsing, AST)
- Workflow Git et GitHub
- Ligne de commande Unix/Linux

**Outils requis :**
- Compilateur GCC ou Clang
- Système de build Make
- Contrôle de version Git
- Valgrind (pour la détection des fuites mémoire)
- Éditeur de texte basique ou IDE

### Canaux de communication

**Où poser des questions :**
- GitHub Issues - Rapports de bugs et demandes de fonctionnalités
- GitHub Discussions - Questions générales et discussions de conception
- Commentaires de Pull Request - Retours spécifiques sur le code

---

## Processus de contribution

### 1. Trouver ou créer une issue

**Avant d'écrire du code :**
- Vérifiez si une issue existe pour votre contribution
- Sinon, créez-en une décrivant ce que vous voulez faire
- Attendez le retour des mainteneurs avant de commencer des changements importants
- Les petites corrections de bugs peuvent sauter cette étape

**Les bonnes descriptions d'issues incluent :**
- Énoncé du problème (ce qui est cassé ou manquant)
- Solution proposée (comment vous prévoyez de le corriger)
- Exemples (extraits de code montrant le problème)
- Justification (pourquoi ce changement s'aligne avec la philosophie de Hemlock)

### 2. Fork et clone

```bash
# Forkez d'abord le dépôt sur GitHub, puis :
git clone https://github.com/VOTRE_NOM_UTILISATEUR/hemlock.git
cd hemlock
git checkout -b feature/nom-de-votre-fonctionnalite
```

### 3. Effectuez vos modifications

Suivez ces directives :
- Écrivez les tests d'abord (approche TDD)
- Implémentez la fonctionnalité
- Assurez-vous que tous les tests passent
- Vérifiez les fuites mémoire
- Mettez à jour la documentation

### 4. Testez vos modifications

```bash
# Exécutez la suite de tests complète
make test

# Exécutez une catégorie de test spécifique
./tests/run_tests.sh tests/category/

# Vérifiez les fuites mémoire
valgrind ./hemlock tests/your_test.hml

# Compilez et testez
make clean && make && make test
```

### 5. Committez vos modifications

**Bons messages de commit :**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**Format du message de commit :**
- Première ligne : Résumé bref (50 caractères max)
- Ligne vide
- Explication détaillée (retour à la ligne à 72 caractères)
- Référencer les numéros d'issue

### 6. Soumettez une Pull Request

**Avant de soumettre :**
- Rebasez sur la dernière branche main
- Assurez-vous que tous les tests passent
- Exécutez valgrind pour vérifier les fuites
- Mettez à jour CLAUDE.md si vous ajoutez des fonctionnalités visibles par l'utilisateur

**La description de la pull request doit inclure :**
- Quel problème cela résout
- Comment cela le résout
- Changements cassants (s'il y en a)
- Exemples de nouvelle syntaxe ou comportement
- Résumé de la couverture des tests

---

## Directives de style de code

### Style de code C

**Formatage :**
```c
// Indentation avec 4 espaces (pas de tabulations)
// Style d'accolade K&R pour les fonctions
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // Accolade sur la même ligne pour les structures de contrôle
        do_something();
    }
}

// Longueur de ligne : 100 caractères max
// Utiliser des espaces autour des opérateurs
int result = (a + b) * c;

// Astérisque de pointeur avec le type
char *string;   // Bon
char* string;   // À éviter
char * string;  // À éviter
```

**Conventions de nommage :**
```c
// Fonctions : minuscules_avec_underscores
void eval_expression(ASTNode *node);

// Types : PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// Constantes : MAJUSCULES_AVEC_UNDERSCORES
#define MAX_BUFFER_SIZE 4096

// Variables : minuscules_avec_underscores
int item_count;
Value *current_value;

// Enums : TYPE_PREFIX_NOM
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**Commentaires :**
```c
// Commentaires sur une ligne pour les explications brèves
// Utiliser des phrases complètes avec majuscule initiale

/*
 * Commentaires multi-lignes pour les explications plus longues
 * Aligner les astérisques pour la lisibilité
 */

/**
 * Commentaire de documentation de fonction
 * @param node - Nœud AST à évaluer
 * @return Valeur évaluée
 */
Value eval_expr(ASTNode *node);
```

**Gestion des erreurs :**
```c
// Vérifier tous les appels malloc
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Erreur : Mémoire insuffisante\n");
    exit(1);
}

// Fournir du contexte dans les messages d'erreur
if (file == NULL) {
    fprintf(stderr, "Erreur : Impossible d'ouvrir '%s' : %s\n",
            filename, strerror(errno));
    exit(1);
}

// Utiliser des messages d'erreur significatifs
// Mauvais : "Erreur : Valeur invalide"
// Bon : "Erreur : Attendu un entier, obtenu une chaîne"
```

**Gestion de la mémoire :**
```c
// Toujours libérer ce que vous allouez
Value *val = value_create_i32(42);
// ... utiliser val
value_free(val);

// Mettre les pointeurs à NULL après libération (évite le double-free)
free(ptr);
ptr = NULL;

// Documenter la propriété dans les commentaires
// Cette fonction prend possession de 'value' et le libérera
void store_value(Value *value);

// Cette fonction NE prend PAS possession (l'appelant doit libérer)
Value *get_value(void);
```

### Organisation du code

**Structure des fichiers :**
```c
// 1. Includes (en-têtes système d'abord, puis locaux)
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. Constantes et macros
#define INITIAL_CAPACITY 16

// 3. Définitions de types
typedef struct Foo Foo;

// 4. Déclarations de fonctions statiques (helpers internes)
static void helper_function(void);

// 5. Implémentations des fonctions publiques
void public_api_function(void)
{
    // Implémentation
}

// 6. Implémentations des fonctions statiques
static void helper_function(void)
{
    // Implémentation
}
```

**Fichiers d'en-tête :**
```c
// Utiliser des gardes d'en-tête
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// Déclarations anticipées
typedef struct Value Value;

// API publique seulement dans les en-têtes
void public_function(Value *val);

// Documenter les paramètres et valeurs de retour
/**
 * Évalue un nœud AST d'expression
 * @param node - Le nœud AST à évaluer
 * @param env - L'environnement courant
 * @return La valeur résultante
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## Quoi contribuer

### Contributions encouragées

**Corrections de bugs :**
- Fuites mémoire
- Erreurs de segmentation
- Comportement incorrect
- Améliorations des messages d'erreur

**Documentation :**
- Commentaires de code
- Documentation d'API
- Guides utilisateur et tutoriels
- Programmes d'exemple
- Documentation des cas de test

**Tests :**
- Cas de test supplémentaires pour les fonctionnalités existantes
- Couverture des cas limites
- Tests de régression pour les bugs corrigés
- Benchmarks de performance

**Petits ajouts de fonctionnalités :**
- Nouvelles fonctions intégrées (si elles correspondent à la philosophie)
- Méthodes de chaîne/tableau
- Fonctions utilitaires
- Améliorations de la gestion des erreurs

**Améliorations de performance :**
- Algorithmes plus rapides (sans changer la sémantique)
- Réduction de l'utilisation mémoire
- Suite de benchmarks
- Outils de profilage

**Outillage :**
- Coloration syntaxique pour les éditeurs
- Language Server Protocol (LSP)
- Intégration du débogueur
- Améliorations du système de build

### Discutez d'abord

**Fonctionnalités majeures :**
- Nouvelles constructions du langage
- Changements du système de types
- Ajouts de syntaxe
- Primitives de concurrence

**Comment discuter :**
1. Ouvrez une issue ou discussion GitHub
2. Décrivez la fonctionnalité et la justification
3. Montrez du code exemple
4. Expliquez comment cela s'inscrit dans la philosophie de Hemlock
5. Attendez le retour des mainteneurs
6. Itérez sur la conception avant d'implémenter

---

## Quoi NE PAS contribuer

### Contributions déconseillées

**N'ajoutez pas de fonctionnalités qui :**
- Cachent la complexité à l'utilisateur
- Rendent le comportement implicite ou magique
- Cassent la sémantique ou la syntaxe existante
- Ajoutent le ramasse-miettes ou la gestion automatique de la mémoire
- Violent le principe "explicite plutôt qu'implicite"

**Exemples de contributions rejetées :**

**1. Insertion automatique de point-virgule**
```hemlock
// MAUVAIS : Cela serait rejeté
let x = 5  // Pas de point-virgule
let y = 10 // Pas de point-virgule
```
Pourquoi : Rend la syntaxe ambiguë, cache les erreurs

**2. RAII/destructeurs**
```hemlock
// MAUVAIS : Cela serait rejeté
let f = open("file.txt");
// Fichier automatiquement fermé à la fin de la portée
```
Pourquoi : Cache quand les ressources sont libérées, pas explicite

**3. Coercition de type implicite qui perd des données**
```hemlock
// MAUVAIS : Cela serait rejeté
let x: i32 = 3.14;  // Tronque silencieusement à 3
```
Pourquoi : La perte de données devrait être explicite, pas silencieuse

**4. Ramasse-miettes (garbage collection)**
```c
// MAUVAIS : Cela serait rejeté
void *gc_malloc(size_t size) {
    // Suivre l'allocation pour un nettoyage automatique
}
```
Pourquoi : Cache la gestion de la mémoire, performances imprévisibles

**5. Système de macros complexe**
```hemlock
// MAUVAIS : Cela serait rejeté
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
Pourquoi : Trop de magie, rend le code difficile à comprendre

### Raisons courantes de rejet

**"C'est trop implicite"**
- Solution : Rendez le comportement explicite et documentez-le

**"Cela cache de la complexité"**
- Solution : Exposez la complexité mais rendez-la ergonomique

**"Cela casse le code existant"**
- Solution : Trouvez une alternative non cassante ou discutez du versioning

**"Cela ne correspond pas à la philosophie de Hemlock"**
- Solution : Relisez philosophy.md et reconsidérez l'approche

---

## Modèles courants

### Modèle de gestion des erreurs

```c
// Utilisez ce modèle pour les erreurs récupérables dans le code Hemlock
Value *divide(Value *a, Value *b)
{
    // Vérifier les préconditions
    if (b->type != TYPE_I32) {
        // Retourner une valeur d'erreur ou lever une exception
        return create_error("Attendu un diviseur entier");
    }

    if (b->i32_value == 0) {
        return create_error("Division par zéro");
    }

    // Effectuer l'opération
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### Modèle de gestion de la mémoire

```c
// Modèle : Allouer, utiliser, libérer
void process_data(void)
{
    // Allouer
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // Utiliser
    if (buf && str) {
        // ... faire le travail
    }

    // Libérer (dans l'ordre inverse de l'allocation)
    free(str);
    free_buffer(buf);
}
```

### Modèle de création de valeur

```c
// Créer des valeurs en utilisant des constructeurs
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Mémoire insuffisante\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### Modèle de vérification de type

```c
// Vérifier les types avant les opérations
Value *add_values(Value *a, Value *b)
{
    // Vérification de type
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Incompatibilité de types");
    }

    // Sûr de procéder
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### Modèle de construction de chaîne

```c
// Construire des chaînes efficacement
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Erreur : %s (ligne %d)", detail, line_number);
}
```

---

## Ajouter de nouvelles fonctionnalités

### Checklist d'ajout de fonctionnalité

Lors de l'ajout d'une nouvelle fonctionnalité, suivez ces étapes :

#### 1. Phase de conception

- [ ] Lire philosophy.md pour assurer l'alignement
- [ ] Créer une issue GitHub décrivant la fonctionnalité
- [ ] Obtenir l'approbation du mainteneur pour la conception
- [ ] Écrire la spécification (syntaxe, sémantique, exemples)
- [ ] Considérer les cas limites et les conditions d'erreur

#### 2. Phase d'implémentation

**Si vous ajoutez une construction du langage :**

- [ ] Ajouter le type de token à `lexer.h` (si nécessaire)
- [ ] Ajouter la règle du lexer dans `lexer.c` (si nécessaire)
- [ ] Ajouter le type de nœud AST dans `ast.h`
- [ ] Ajouter le constructeur AST dans `ast.c`
- [ ] Ajouter la règle du parser dans `parser.c`
- [ ] Ajouter le comportement d'exécution dans `runtime.c` ou le module approprié
- [ ] Gérer le nettoyage dans les fonctions de libération AST

**Si vous ajoutez une fonction intégrée :**

- [ ] Ajouter l'implémentation de la fonction dans `builtins.c`
- [ ] Enregistrer la fonction dans `register_builtins()`
- [ ] Gérer toutes les combinaisons de types de paramètres
- [ ] Retourner les valeurs d'erreur appropriées
- [ ] Documenter les paramètres et le type de retour

**Si vous ajoutez un type de valeur :**

- [ ] Ajouter l'enum de type dans `values.h`
- [ ] Ajouter le champ à l'union Value
- [ ] Ajouter le constructeur dans `values.c`
- [ ] Ajouter à `value_free()` pour le nettoyage
- [ ] Ajouter à `value_copy()` pour la copie
- [ ] Ajouter à `value_to_string()` pour l'affichage
- [ ] Ajouter les règles de promotion de type si numérique

#### 3. Phase de test

- [ ] Écrire les cas de test (voir testing.md)
- [ ] Tester les cas de succès
- [ ] Tester les cas d'erreur
- [ ] Tester les cas limites
- [ ] Exécuter la suite de tests complète (`make test`)
- [ ] Vérifier les fuites mémoire avec valgrind
- [ ] Tester sur plusieurs plateformes (si possible)

#### 4. Phase de documentation

- [ ] Mettre à jour CLAUDE.md avec la documentation destinée à l'utilisateur
- [ ] Ajouter des commentaires de code expliquant l'implémentation
- [ ] Créer des exemples dans `examples/`
- [ ] Mettre à jour les fichiers docs/ pertinents
- [ ] Documenter tout changement cassant

#### 5. Phase de soumission

- [ ] Nettoyer le code de débogage et les commentaires
- [ ] Vérifier la conformité au style de code
- [ ] Rebaser sur la dernière branche main
- [ ] Créer la pull request avec une description détaillée
- [ ] Répondre aux retours de la revue de code

### Exemple : Ajouter un nouvel opérateur

Parcourons l'ajout de l'opérateur modulo `%` comme exemple :

**1. Lexer (lexer.c) :**
```c
// Ajouter à l'instruction switch dans get_next_token()
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. En-tête du lexer (lexer.h) :**
```c
typedef enum {
    // ... tokens existants
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h) :**
```c
typedef enum {
    // ... opérateurs existants
    OP_MOD,
    // ...
} BinaryOp;
```

**4. Parser (parser.c) :**
```c
// Ajouter à parse_multiplicative() ou au niveau de précédence approprié
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. Runtime (runtime.c) :**
```c
// Ajouter à eval_binary_op()
case OP_MOD:
    // Vérification de type
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Erreur : Modulo par zéro\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... gérer les autres combinaisons de types
    break;
```

**6. Tests (tests/operators/modulo.hml) :**
```hemlock
// Modulo basique
print(10 % 3);  // Attendu : 2

// Modulo négatif
print(-10 % 3); // Attendu : -1

// Cas d'erreur (devrait échouer)
// print(10 % 0);  // Division par zéro
```

**7. Documentation (CLAUDE.md) :**
```markdown
### Opérateurs arithmétiques
- `+` - Addition
- `-` - Soustraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo (reste)
```

---

## Processus de revue de code

### Ce que les reviewers recherchent

**1. Correction**
- Le code fait-il ce qu'il prétend ?
- Les cas limites sont-ils gérés ?
- Y a-t-il des fuites mémoire ?
- Les erreurs sont-elles gérées correctement ?

**2. Alignement avec la philosophie**
- Est-ce que cela correspond aux principes de conception de Hemlock ?
- Est-ce explicite ou implicite ?
- Est-ce que cela cache de la complexité ?

**3. Qualité du code**
- Le code est-il lisible et maintenable ?
- Les noms de variables sont-ils descriptifs ?
- Les fonctions ont-elles une taille raisonnable ?
- Y a-t-il une documentation adéquate ?

**4. Tests**
- Y a-t-il suffisamment de cas de test ?
- Les tests couvrent-ils les chemins de succès et d'échec ?
- Les cas limites sont-ils testés ?

**5. Documentation**
- La documentation destinée à l'utilisateur est-elle mise à jour ?
- Les commentaires de code sont-ils clairs ?
- Des exemples sont-ils fournis ?

### Répondre aux retours

**À faire :**
- Remercier les reviewers pour leur temps
- Poser des questions de clarification si vous ne comprenez pas
- Expliquer votre raisonnement si vous n'êtes pas d'accord
- Effectuer les changements demandés rapidement
- Mettre à jour la description de la PR si la portée change

**À ne pas faire :**
- Prendre les critiques personnellement
- Argumenter défensivement
- Ignorer les retours
- Force-push par-dessus les commentaires de revue (sauf si rebase)
- Ajouter des changements non liés à la PR

### Faire merger votre PR

**Conditions pour le merge :**
- [ ] Tous les tests passent
- [ ] Pas de fuites mémoire (valgrind clean)
- [ ] Approbation de la revue de code par un mainteneur
- [ ] Documentation mise à jour
- [ ] Suit les directives de style de code
- [ ] S'aligne avec la philosophie de Hemlock

**Délais :**
- Petites PR (corrections de bugs) : Généralement reviewées en quelques jours
- PR moyennes (nouvelles fonctionnalités) : Peut prendre 1-2 semaines
- Grandes PR (changements majeurs) : Nécessite une discussion approfondie

---

## Ressources supplémentaires

### Ressources d'apprentissage

**Comprendre les interpréteurs :**
- "Crafting Interpreters" par Robert Nystrom
- "Writing An Interpreter In Go" par Thorsten Ball
- "Modern Compiler Implementation in C" par Andrew Appel

**Programmation C :**
- "The C Programming Language" par K&R
- "Expert C Programming" par Peter van der Linden
- "C Interfaces and Implementations" par David Hanson

**Gestion de la mémoire :**
- Documentation Valgrind
- "Understanding and Using C Pointers" par Richard Reese

### Commandes utiles

```bash
# Compiler avec symboles de débogage
make clean && make CFLAGS="-g -O0"

# Exécuter avec valgrind
valgrind --leak-check=full ./hemlock script.hml

# Exécuter une catégorie de test spécifique
./tests/run_tests.sh tests/strings/

# Générer un fichier de tags pour la navigation de code
ctags -R .

# Trouver tous les TODO et FIXME
grep -rn "TODO\|FIXME" src/ include/
```

---

## Questions ?

Si vous avez des questions sur la contribution :

1. Consultez la documentation dans `docs/`
2. Recherchez dans les issues GitHub existantes
3. Demandez dans GitHub Discussions
4. Ouvrez une nouvelle issue avec votre question

**Merci de contribuer à Hemlock !**
