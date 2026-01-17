# Détails d'implémentation de Hemlock

Ce document décrit l'implémentation technique du langage Hemlock, incluant la structure du projet, le pipeline de compilation, l'architecture d'exécution et les décisions de conception.

---

## Table des matières

- [Structure du projet](#structure-du-projet)
- [Pipeline de compilation](#pipeline-de-compilation)
- [Conception modulaire de l'interpréteur](#conception-modulaire-de-linterpréteur)
- [Architecture d'exécution](#architecture-dexécution)
- [Représentation des valeurs](#représentation-des-valeurs)
- [Implémentation du système de types](#implémentation-du-système-de-types)
- [Gestion de la mémoire](#gestion-de-la-mémoire)
- [Modèle de concurrence](#modèle-de-concurrence)
- [Plans futurs](#plans-futurs)

---

## Structure du projet

```
hemlock/
├── src/
│   ├── frontend/              # Partagé : lexer, parser, AST
│   │   ├── lexer.c            # Tokenisation
│   │   ├── parser/            # Parser à descente récursive
│   │   ├── ast.c              # Gestion des nœuds AST
│   │   └── module.c           # Résolution des modules
│   ├── backends/
│   │   ├── interpreter/       # hemlock : interpréteur par parcours d'arbre
│   │   │   ├── main.c         # Point d'entrée CLI
│   │   │   ├── runtime.c      # Évaluation des expressions/instructions
│   │   │   ├── builtins.c     # Fonctions intégrées
│   │   │   └── ...
│   │   └── compiler/          # hemlockc : générateur de code C
│   │       ├── main.c         # CLI, orchestration
│   │       ├── type_check.c   # Vérification de types à la compilation
│   │       ├── codegen.c      # Contexte de génération de code
│   │       ├── codegen_expr.c # Génération de code pour les expressions
│   │       ├── codegen_stmt.c # Génération de code pour les instructions
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # Language Server Protocol
│   │   └── bundler/           # Outils de bundle/package
├── runtime/                   # libhemlock_runtime.a (pour les programmes compilés)
├── stdlib/                    # Bibliothèque standard (39 modules)
│   └── docs/                  # Documentation des modules
├── tests/
│   ├── parity/                # Tests devant passer sur les deux backends
│   ├── interpreter/           # Tests spécifiques à l'interpréteur
│   └── compiler/              # Tests spécifiques au compilateur
├── examples/                  # Programmes exemples
└── docs/                      # Documentation
```

### Organisation des répertoires

**`include/`** - En-têtes d'API publique qui définissent l'interface entre les composants :
- Séparation nette entre lexer, parser, AST et interpréteur
- Déclarations anticipées pour minimiser les dépendances
- API publique pour intégrer Hemlock dans d'autres programmes

**`src/`** - Fichiers d'implémentation :
- Les fichiers de niveau supérieur gèrent le lexing, le parsing, la gestion de l'AST
- `main.c` fournit la CLI et le REPL
- L'interpréteur est modularisé en sous-systèmes séparés

**`src/interpreter/`** - Implémentation modulaire de l'interpréteur :
- Chaque module a une seule responsabilité claire
- API interne définie dans `internal.h` pour la communication inter-modules
- Les modules peuvent être compilés indépendamment pour des builds plus rapides

**`tests/`** - Suite de tests complète :
- Organisée par domaine fonctionnel
- Chaque répertoire contient des cas de test ciblés
- `run_tests.sh` orchestre l'exécution des tests

---

## Pipeline de compilation

Hemlock utilise un pipeline de compilation traditionnel avec des phases distinctes :

### Phase 1 : Analyse lexicale (Lexer)

**Entrée :** Texte du code source
**Sortie :** Flux de tokens
**Implémentation :** `src/lexer.c`

```
Source : "let x = 42;"
   ↓
Tokens : [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**Caractéristiques clés :**
- Reconnaît les mots-clés, identifiants, littéraux, opérateurs, ponctuation
- Gère les littéraux de chaîne UTF-8 et les littéraux de rune
- Rapporte les numéros de ligne pour les messages d'erreur
- Passe unique, pas de retour arrière

### Phase 2 : Analyse syntaxique (Parser)

**Entrée :** Flux de tokens
**Sortie :** Arbre de syntaxe abstraite (AST)
**Implémentation :** `src/parser.c`

```
Tokens : [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST : LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**Caractéristiques clés :**
- Parser à descente récursive
- Construit une représentation arborescente de la structure du programme
- Gère la précédence des opérateurs
- Valide la syntaxe (accolades, points-virgules, etc.)
- Pas d'analyse sémantique encore (faite à l'exécution)

**Précédence des opérateurs (du plus bas au plus haut) :**
1. Affectation : `=`
2. OU logique : `||`
3. ET logique : `&&`
4. OU bit à bit : `|`
5. XOR bit à bit : `^`
6. ET bit à bit : `&`
7. Égalité : `==`, `!=`
8. Comparaison : `<`, `>`, `<=`, `>=`
9. Décalages bit à bit : `<<`, `>>`
10. Addition/Soustraction : `+`, `-`
11. Multiplication/Division/Modulo : `*`, `/`, `%`
12. Unaire : `!`, `-`, `~`
13. Appel/Index/Membre : `()`, `[]`, `.`

### Phase 3a : Interprétation (parcours d'arbre)

**Entrée :** AST
**Sortie :** Exécution du programme
**Implémentation :** `src/backends/interpreter/runtime.c`

```
AST : LetStmt { ... }
   ↓
Exécution : Évalue les nœuds AST récursivement
   ↓
Résultat : Variable x créée avec la valeur 42
```

**Caractéristiques clés :**
- Parcours direct de l'AST (interpréteur par parcours d'arbre)
- Vérification de type dynamique à l'exécution
- Stockage des variables basé sur l'environnement

### Phase 3b : Compilation (hemlockc)

**Entrée :** AST
**Sortie :** Exécutable natif via génération de code C
**Implémentation :** `src/backends/compiler/`

```
AST : LetStmt { ... }
   ↓
Vérification de types : Valide les types à la compilation
   ↓
Génération C : Génère le code C équivalent
   ↓
GCC : Compile le C en binaire natif
   ↓
Résultat : Exécutable autonome
```

**Caractéristiques clés :**
- Vérification de types à la compilation (activée par défaut)
- Génération de code C pour la portabilité
- Liaison avec `libhemlock_runtime.a`
- Exécution significativement plus rapide que l'interpréteur

---

## Backend compilateur (hemlockc)

Le compilateur Hemlock génère du code C à partir de l'AST, qui est ensuite compilé en exécutable natif avec GCC.

### Architecture du compilateur

```
src/backends/compiler/
├── main.c              # CLI, analyse des arguments, orchestration
├── codegen.c           # Contexte de génération de code principal
├── codegen_expr.c      # Génération de code pour les expressions
├── codegen_stmt.c      # Génération de code pour les instructions
├── codegen_call.c      # Génération des appels de fonction
├── codegen_closure.c   # Implémentation des closures
├── codegen_program.c   # Génération du programme de niveau supérieur
├── codegen_module.c    # Gestion des modules/imports
├── type_check.c        # Vérification de types à la compilation
└── type_check.h        # API du vérificateur de types
```

### Vérification de types

Le compilateur inclut un système de vérification de types unifié qui :

1. **Valide les types à la compilation** - Détecte les erreurs de type avant l'exécution
2. **Supporte le code dynamique** - Le code non typé est traité comme `any` (toujours valide)
3. **Fournit des indices d'optimisation** - Identifie les variables qui peuvent être déballées

**Options de vérification de types :**

| Option | Description |
|--------|-------------|
| (défaut) | Vérification de types activée |
| `--check` | Vérifier les types uniquement, ne pas compiler |
| `--no-type-check` | Désactiver la vérification de types |
| `--strict-types` | Avertir sur les types `any` implicites |

**Implémentation du vérificateur de types :**

```c
// type_check.h - Structures clés
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // Indices d'optimisation
    // ... environnement de types, définitions, etc.
} TypeCheckContext;

// Point d'entrée principal
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### Génération de code

La phase de génération de code traduit les nœuds AST en code C :

**Correspondance des expressions :**
```
Hemlock                 →  C généré
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  Closure avec capture d'environnement
```

**Intégration du runtime :**

Le code C généré est lié avec `libhemlock_runtime.a` qui fournit :
- Type union étiqueté `HmlValue`
- Gestion de la mémoire (comptage de références)
- Fonctions intégrées (print, typeof, etc.)
- Primitives de concurrence (tâches, canaux)
- Support FFI

### Optimisation du déballage (unboxing)

Le vérificateur de types identifie les variables qui peuvent utiliser des types C natifs au lieu de `HmlValue` emballés :

**Motifs déballables :**
- Compteurs de boucle avec type entier connu
- Variables d'accumulateur dans les boucles
- Variables avec annotations de type explicites (i32, i64, f64, bool)

```hemlock
// Le compteur de boucle 'i' peut être déballé en int32_t natif
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    sum = sum + i;
}
```

---

## Conception modulaire de l'interpréteur

L'interpréteur est divisé en modules ciblés pour la maintenabilité et l'extensibilité.

### Responsabilités des modules

#### 1. Environnement (`environment.c`) - 121 lignes

**Objectif :** Portée des variables et résolution des noms

**Fonctions clés :**
- `env_create()` - Créer un nouvel environnement avec parent optionnel
- `env_define()` - Définir une nouvelle variable dans la portée courante
- `env_get()` - Rechercher une variable dans la portée courante ou parente
- `env_set()` - Mettre à jour la valeur d'une variable existante
- `env_free()` - Libérer l'environnement et toutes les variables

**Conception :**
- Portées liées (chaque environnement a un pointeur vers le parent)
- HashMap pour une recherche rapide des variables
- Supporte la portée lexicale pour les closures

#### 2. Valeurs (`values.c`) - 394 lignes

**Objectif :** Constructeurs de valeurs et gestion des structures de données

**Fonctions clés :**
- `value_create_*()` - Constructeurs pour chaque type de valeur
- `value_copy()` - Logique de copie profonde/superficielle
- `value_free()` - Nettoyage et désallocation mémoire
- `value_to_string()` - Représentation en chaîne pour l'affichage

**Structures de données :**
- Objets (tableaux de champs dynamiques)
- Tableaux (redimensionnement dynamique)
- Buffers (ptr + longueur + capacité)
- Closures (fonction + environnement capturé)
- Tâches et canaux (primitives de concurrence)

#### 3. Types (`types.c`) - 440 lignes

**Objectif :** Système de types, conversions et duck typing

**Fonctions clés :**
- `type_check()` - Validation de type à l'exécution
- `type_convert()` - Conversions/promotions de type implicites
- `duck_type_check()` - Vérification de type structurel pour les objets
- `type_name()` - Obtenir le nom de type affichable

**Fonctionnalités :**
- Hiérarchie de promotion de type (i8 → i16 → i32 → i64 → f32 → f64, avec i64/u64 + f32 → f64)
- Vérification de plage pour les types numériques
- Duck typing pour les définitions de type objet
- Valeurs par défaut des champs optionnels

#### 4. Fonctions intégrées (`builtins.c`) - 955 lignes

**Objectif :** Fonctions intégrées et enregistrement global

**Fonctions clés :**
- `register_builtins()` - Enregistrer toutes les fonctions et constantes intégrées
- Implémentations des fonctions intégrées (print, typeof, alloc, free, etc.)
- Fonctions de gestion des signaux
- Exécution de commandes (exec)

**Catégories de fonctions intégrées :**
- E/S : print, open, read_file, write_file
- Mémoire : alloc, free, memset, memcpy, realloc
- Types : typeof, assert
- Concurrence : spawn, join, detach, channel
- Système : exec, signal, raise, panic
- FFI : dlopen, dlsym, dlcall, dlclose

#### 5. E/S (`io.c`) - 449 lignes

**Objectif :** E/S de fichiers et sérialisation JSON

**Fonctions clés :**
- Méthodes d'objet fichier (read, write, seek, tell, close)
- Sérialisation/désérialisation JSON
- Détection des références circulaires

**Fonctionnalités :**
- Objet fichier avec propriétés (path, mode, closed)
- E/S texte compatible UTF-8
- Support E/S binaire
- Aller-retour JSON pour objets et tableaux

#### 6. FFI (`ffi.c`) - Interface de fonction étrangère

**Objectif :** Appeler des fonctions C depuis des bibliothèques partagées

**Fonctions clés :**
- `dlopen()` - Charger une bibliothèque partagée
- `dlsym()` - Obtenir un pointeur de fonction par nom
- `dlcall()` - Appeler une fonction C avec conversion de type
- `dlclose()` - Décharger la bibliothèque

**Fonctionnalités :**
- Intégration avec libffi pour les appels de fonction dynamiques
- Conversion de type automatique (Hemlock ↔ types C)
- Support pour tous les types primitifs
- Support des pointeurs et buffers

#### 7. Runtime (`runtime.c`) - 865 lignes

**Objectif :** Évaluation des expressions et exécution des instructions

**Fonctions clés :**
- `eval_expr()` - Évaluer les expressions (récursif)
- `eval_stmt()` - Exécuter les instructions
- Gestion du flux de contrôle (if, while, for, switch, etc.)
- Gestion des exceptions (try/catch/finally/throw)

**Fonctionnalités :**
- Évaluation récursive des expressions
- Évaluation booléenne en court-circuit
- Détection d'appel de méthode et liaison de `self`
- Propagation des exceptions
- Gestion de break/continue/return

### Avantages de la conception modulaire

**1. Séparation des préoccupations**
- Chaque module a une seule responsabilité claire
- Facile de trouver où les fonctionnalités sont implémentées
- Réduit la charge cognitive lors des modifications

**2. Builds incrémentaux plus rapides**
- Seuls les modules modifiés nécessitent une recompilation
- Compilation parallèle possible
- Temps d'itération plus courts pendant le développement

**3. Tests et débogage plus faciles**
- Les modules peuvent être testés isolément
- Les bugs sont localisés dans des sous-systèmes spécifiques
- Implémentations mock possibles pour les tests

**4. Extensibilité**
- Les nouvelles fonctionnalités peuvent être ajoutées aux modules appropriés
- Les modules peuvent être refactorisés indépendamment
- La taille du code par fichier reste gérable

**5. Organisation du code**
- Regroupement logique des fonctionnalités connexes
- Graphe de dépendances clair
- Intégration plus facile des nouveaux contributeurs

---

## Architecture d'exécution

### Représentation des valeurs

Toutes les valeurs dans Hemlock sont représentées par la structure `Value` utilisant une union étiquetée :

```c
typedef struct Value {
    ValueType type;  // Étiquette de type à l'exécution
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**Décisions de conception :**
- **Union étiquetée** pour la sécurité de type tout en maintenant la flexibilité
- **Étiquettes de type à l'exécution** permettent le typage dynamique avec vérification de type
- **Stockage direct des valeurs** pour les primitives (pas de boxing)
- **Stockage de pointeur** pour les types alloués sur le tas (chaînes, objets, tableaux)

### Exemples de disposition mémoire

**Entier (i32) :**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- Taille totale : ~16 octets (étiquette de 8 octets + union de 8 octets)
- Alloué sur la pile
- Pas d'allocation sur le tas nécessaire

**Chaîne :**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // Pointeur vers le tas
}

Tas : "hello\0" (6 octets, UTF-8 terminé par null)
```
- La valeur fait 16 octets sur la pile
- Les données de chaîne sont allouées sur le tas
- Doit être libérée manuellement

**Objet :**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // Pointeur vers le tas
}

Tas : Object {
    type_name: "Person",
    fields: [
        { name: "name", value: Value{TYPE_STRING, "Alice"} },
        { name: "age", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- Structure d'objet sur le tas
- Champs stockés dans un tableau dynamique
- Les valeurs des champs sont des structures Value intégrées

### Implémentation de l'environnement

Les variables sont stockées dans des chaînes d'environnement :

```c
typedef struct Environment {
    HashMap *bindings;           // nom → Value
    struct Environment *parent;  // Portée parente lexicale
} Environment;
```

**Exemple de chaîne de portée :**
```
Portée globale : { print: <builtin>, args: <array> }
    ↑
Portée fonction : { x: 10, y: 20 }
    ↑
Portée bloc : { i: 0 }
```

**Algorithme de recherche :**
1. Vérifier le hashmap de l'environnement courant
2. Si non trouvé, vérifier l'environnement parent
3. Répéter jusqu'à trouver ou atteindre la portée globale
4. Erreur si non trouvé dans aucune portée

---

## Implémentation du système de types

### Stratégie de vérification de types

Hemlock utilise la **vérification de type à l'exécution** avec des **annotations de type optionnelles** :

```hemlock
let x = 42;           // Pas de vérification de type, infère i32
let y: u8 = 255;      // Vérification à l'exécution : la valeur doit tenir dans u8
let z: i32 = x + y;   // Vérification à l'exécution + promotion de type
```

**Flux d'implémentation :**
1. **Inférence de littéral** - Le lexer/parser détermine le type initial du littéral
2. **Vérification d'annotation de type** - Si annotation présente, valider à l'affectation
3. **Promotion** - Les opérations binaires promeuvent vers un type commun
4. **Conversion** - Les conversions explicites se font à la demande

### Implémentation de la promotion de type

La promotion de type suit une hiérarchie fixe avec préservation de la précision :

```c
// Logique de promotion simplifiée
ValueType promote_types(ValueType a, ValueType b) {
    // f64 gagne toujours
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 avec i64/u64 promeut vers f64 (préservation de la précision)
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // Les types entiers plus grands gagnent
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**Rangs de types :**
- i8 : 0
- u8 : 1
- i16 : 2
- u16 : 3
- i32 : 4
- u32 : 5
- i64 : 6
- u64 : 7
- f32 : 8
- f64 : 9

### Implémentation du duck typing

La vérification de type d'objet utilise la comparaison structurelle :

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // Vérifier tous les champs requis
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // Champ manquant
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // Mauvais type
        }
    }

    return true;  // Tous les champs requis présents et de type correct
}
```

**Le duck typing permet :**
- Champs supplémentaires dans les objets (ignorés)
- Typage substructurel (l'objet peut avoir plus que requis)
- Affectation du nom de type après validation

---

## Gestion de la mémoire

### Stratégie d'allocation

Hemlock utilise la **gestion manuelle de la mémoire** avec deux primitives d'allocation :

**1. Pointeurs bruts (`ptr`) :**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Mémoire insuffisante\n");
        exit(1);
    }
    return ptr;
}
```
- malloc/free direct
- Pas de suivi
- Responsabilité de l'utilisateur de libérer

**2. Buffers (`buffer`) :**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- Suit la taille et la capacité
- Vérification des limites à l'accès
- Nécessite toujours une libération manuelle

### Types alloués sur le tas

**Chaînes :**
- Tableau d'octets UTF-8 sur le tas
- Terminé par null pour l'interopérabilité C
- Mutable (peut modifier sur place)
- Comptage de références (auto-libéré quand la portée se termine)

**Objets :**
- Tableau de champs dynamique
- Noms et valeurs des champs sur le tas
- Comptage de références (auto-libéré quand la portée se termine)
- Références circulaires possibles (géré avec suivi d'ensemble visité)

**Tableaux :**
- Croissance par doublement de capacité dynamique
- Les éléments sont des structures Value intégrées
- Réallocation automatique lors de la croissance
- Comptage de références (auto-libéré quand la portée se termine)

**Closures :**
- Capture l'environnement par référence
- L'environnement est alloué sur le tas
- Les environnements de closure sont correctement libérés quand ils ne sont plus référencés

---

## Modèle de concurrence

### Architecture de threading

Hemlock utilise le **threading 1:1** avec les threads POSIX (pthreads) :

```
Tâche utilisateur       Thread OS          Cœur CPU
----------------        ---------          --------
spawn(f1) ------>  pthread_create --> Cœur 0
spawn(f2) ------>  pthread_create --> Cœur 1
spawn(f3) ------>  pthread_create --> Cœur 2
```

**Caractéristiques clés :**
- Chaque `spawn()` crée un nouveau pthread
- Le noyau planifie les threads sur les cœurs
- Vraie exécution parallèle (pas de GIL)
- Multitâche préemptif

### Implémentation des tâches

```c
typedef struct Task {
    pthread_t thread;        // Handle de thread OS
    Value result;            // Valeur de retour
    char *error;             // Message d'exception (si levée)
    pthread_mutex_t lock;    // Protège l'état
    TaskState state;         // RUNNING, FINISHED, ERROR
} Task;
```

**Cycle de vie d'une tâche :**
1. `spawn(func, args)` → Créer Task, démarrer pthread
2. Le thread exécute la fonction avec les arguments
3. Au retour : Stocker le résultat, définir l'état à FINISHED
4. Sur exception : Stocker le message d'erreur, définir l'état à ERROR
5. `join(task)` → Attendre le thread, retourner le résultat ou lever l'exception

### Implémentation des canaux

```c
typedef struct Channel {
    void **buffer;           // Buffer circulaire de Value*
    size_t capacity;         // Maximum d'éléments en buffer
    size_t count;            // Éléments actuels dans le buffer
    size_t read_index;       // Prochaine position de lecture
    size_t write_index;      // Prochaine position d'écriture
    bool closed;             // Indicateur de canal fermé
    pthread_mutex_t lock;    // Protège le buffer
    pthread_cond_t not_full; // Signal quand de l'espace est disponible
    pthread_cond_t not_empty;// Signal quand des données sont disponibles
} Channel;
```

**Opération d'envoi :**
1. Verrouiller le mutex
2. Attendre si le buffer est plein (cond_wait sur not_full)
3. Écrire la valeur dans buffer[write_index]
4. Incrémenter write_index (circulaire)
5. Signaler not_empty
6. Déverrouiller le mutex

**Opération de réception :**
1. Verrouiller le mutex
2. Attendre si le buffer est vide (cond_wait sur not_empty)
3. Lire la valeur depuis buffer[read_index]
4. Incrémenter read_index (circulaire)
5. Signaler not_full
6. Déverrouiller le mutex

**Garanties de synchronisation :**
- Envoi/réception thread-safe (protégé par mutex)
- Sémantique bloquante (le producteur attend si plein, le consommateur attend si vide)
- Livraison ordonnée (FIFO dans un canal)

---

## Plans futurs

### Terminé : Backend compilateur

Le backend compilateur (`hemlockc`) a été implémenté avec :
- Génération de code C depuis l'AST
- Vérification de types à la compilation (activée par défaut)
- Bibliothèque runtime (`libhemlock_runtime.a`)
- Parité complète avec l'interpréteur (98% de taux de réussite des tests)
- Framework d'optimisation par déballage

### Focus actuel : Améliorations du système de types

**Améliorations récentes :**
- Systèmes de vérification et d'inférence de types unifiés
- Vérification de types à la compilation activée par défaut
- Option `--check` pour la validation de types uniquement
- Contexte de type passé au codegen pour les indices d'optimisation

### Améliorations futures

**Ajouts potentiels :**
- Génériques/templates
- Pattern matching
- Intégration LSP pour le support IDE avec conscience des types
- Optimisations de déballage plus agressives
- Analyse d'échappement pour l'allocation sur la pile

### Optimisations à long terme

**Améliorations possibles :**
- Cache en ligne pour les appels de méthode
- Compilation JIT pour les chemins de code chauds
- Planificateur avec vol de travail pour une meilleure concurrence
- Optimisation guidée par le profilage

---

## Directives d'implémentation

### Ajouter de nouvelles fonctionnalités

Lors de l'implémentation de nouvelles fonctionnalités, suivez ces directives :

**1. Choisir le bon module :**
- Nouveaux types de valeur → `values.c`
- Conversions de type → `types.c`
- Fonctions intégrées → `builtins.c`
- Opérations E/S → `io.c`
- Flux de contrôle → `runtime.c`

**2. Mettre à jour toutes les couches :**
- Ajouter les types de nœud AST si nécessaire (`ast.h`, `ast.c`)
- Ajouter les tokens du lexer si nécessaire (`lexer.c`)
- Ajouter les règles du parser (`parser.c`)
- Implémenter le comportement d'exécution (`runtime.c` ou module approprié)
- Ajouter les tests (`tests/`)

**3. Maintenir la cohérence :**
- Suivre le style de code existant
- Utiliser des conventions de nommage cohérentes
- Documenter l'API publique dans les en-têtes
- Garder les messages d'erreur clairs et cohérents

**4. Tester minutieusement :**
- Ajouter les cas de test avant d'implémenter
- Tester les chemins de succès et d'erreur
- Tester les cas limites
- Vérifier l'absence de fuites mémoire (valgrind)

### Considérations de performance

**Goulots d'étranglement actuels :**
- Recherches HashMap pour l'accès aux variables
- Appels de fonction récursifs (pas d'optimisation des appels terminaux)
- Concaténation de chaînes (alloue une nouvelle chaîne à chaque fois)
- Surcharge de vérification de type à chaque opération

**Opportunités d'optimisation :**
- Mettre en cache les emplacements de variables (cache en ligne)
- Optimisation des appels terminaux
- StringBuilder pour la concaténation
- Inférence de type pour éviter les vérifications à l'exécution

### Conseils de débogage

**Outils utiles :**
- `valgrind` - Détection des fuites mémoire
- `gdb` - Débogage des crashs
- Option `-g` - Symboles de débogage
- Débogage avec `printf` - Simple mais efficace

**Problèmes courants :**
- Segfault → Déréférencement de pointeur null (vérifier les valeurs de retour)
- Fuite mémoire → Appel free() manquant (vérifier les chemins de value_free)
- Erreur de type → Vérifier la logique de type_convert() et type_check()
- Crash dans les threads → Condition de course (vérifier l'utilisation des mutex)

---

## Conclusion

L'implémentation de Hemlock priorise :
- **Modularité** - Séparation nette des préoccupations
- **Simplicité** - Implémentation directe
- **Explicitation** - Pas de magie cachée
- **Maintenabilité** - Facile à comprendre et modifier

L'interpréteur actuel par parcours d'arbre est intentionnellement simple pour faciliter le développement rapide de fonctionnalités et l'expérimentation. Le futur backend compilateur améliorera les performances tout en maintenant la même sémantique.
