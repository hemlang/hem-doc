# Conception de la syntaxe des signatures

> Extension du système de types de Hemlock avec les types fonction, les modificateurs nullable, les alias de type, les paramètres const et les signatures de méthode.

**Statut :** Implémenté (v1.7.0)
**Version :** 1.0
**Auteur :** Claude

---

## Aperçu

Ce document propose cinq extensions du système de types interconnectées qui s'appuient sur l'infrastructure existante de Hemlock :

1. **Annotations de type fonction** - Types fonction de première classe
2. **Modificateurs de type nullable** - Gestion explicite de null (étend le flag `nullable` existant)
3. **Alias de type** - Abréviations de type nommées
4. **Paramètres const** - Contrats d'immuabilité
5. **Signatures de méthode dans define** - Comportement de type interface

Ces fonctionnalités partagent la philosophie : **explicite plutôt qu'implicite, optionnel mais appliqué quand utilisé**.

---

## 1. Annotations de type fonction

### Motivation

Actuellement, il n'y a pas de moyen d'exprimer la signature d'une fonction comme type :

```hemlock
// Actuel : callback n'a pas d'information de type
fn map(arr: array, callback) { ... }

// Proposé : type fonction explicite
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Syntaxe

```hemlock
// Type fonction basique
fn(i32, i32): i32

// Avec noms de paramètres (documentation seulement, non appliqué)
fn(a: i32, b: i32): i32

// Pas de valeur de retour (void)
fn(string): void
fn(string)              // Raccourci : omettre `: void`

// Retour nullable
fn(i32): string?

// Paramètres optionnels
fn(name: string, age?: i32): void

// Paramètres rest
fn(...args: array): i32

// Pas de paramètres
fn(): bool

// Ordre supérieur : fonction retournant une fonction
fn(i32): fn(i32): i32

// Type fonction asynchrone
async fn(i32): i32
```

### Exemples d'utilisation

```hemlock
// Variable avec type fonction
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Paramètre de fonction
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Le type de retour est une fonction
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tableau de fonctions
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// Champ d'objet
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### Modifications de l'AST

```c
// Dans l'enum TypeKind (include/ast.h)
typedef enum {
    // ... types existants ...
    TYPE_FUNCTION,      // NOUVEAU : Type fonction
} TypeKind;

// Dans la struct Type (include/ast.h)
struct Type {
    TypeKind kind;
    // ... champs existants ...

    // Pour TYPE_FUNCTION :
    struct Type **param_types;      // Types des paramètres
    char **param_names;             // Noms des paramètres optionnels (docs)
    int *param_optional;            // Quels paramètres sont optionnels
    int num_params;
    char *rest_param_name;          // Nom du paramètre rest ou NULL
    struct Type *rest_param_type;   // Type du paramètre rest
    struct Type *return_type;       // Type de retour (NULL = void)
    int is_async;                   // Type fn async
};
```

### Analyse syntaxique

Les types fonction commencent par `fn` (ou `async fn`) suivi de la liste des paramètres :

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Désambiguïsation :** Lors de l'analyse d'un type et que `fn` est rencontré :
- Si suivi de `(`, c'est un type fonction
- Sinon, erreur de syntaxe (`fn` seul n'est pas un type valide)

### Compatibilité de types

```hemlock
// Correspondance exacte requise pour les types fonction
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Contravariance des paramètres (accepter des types plus larges est OK)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK : i32 <: any

// Covariance du retour (retourner des types plus étroits est OK)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK : i32 <: any

// L'arité doit correspondre
let bad: fn(i32): i32 = fn(a, b) { return a; };       // ERREUR : arité différente

// Paramètres optionnels compatibles avec les requis
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Modificateurs de type nullable

### Motivation

Le suffixe `?` rend l'acceptation de null explicite dans les signatures :

```hemlock
// Actuel : pas clair si null est valide
fn find(arr: array, val: any): i32 { ... }

// Proposé : retour nullable explicite
fn find(arr: array, val: any): i32? { ... }
```

### Syntaxe

```hemlock
// Types nullable avec suffixe ?
string?           // string ou null
i32?              // i32 ou null
User?             // User ou null
array<i32>?       // array ou null
fn(i32): i32?     // fonction retournant i32 ou null

// Composition avec les types fonction
fn(string?): i32          // Accepte string ou null
fn(string): i32?          // Retourne i32 ou null
fn(string?): i32?         // Les deux nullable

// Dans define
define Result {
    value: any?;
    error: string?;
}
```

### Notes d'implémentation

**Existe déjà :** Le flag `Type.nullable` est déjà dans l'AST. Cette fonctionnalité nécessite principalement :
1. Support du parser pour le suffixe `?` sur tout type (vérifier/étendre)
2. Composition correcte avec les types fonction
3. Application à l'exécution

### Compatibilité de types

```hemlock
// Non-nullable assignable à nullable
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullable NON assignable à non-nullable
let z: i32 = x;             // ERREUR : x pourrait être null

// Coalescence null pour déballer
let z: i32 = x ?? 0;        // OK : ?? fournit une valeur par défaut

// Le chaînage optionnel retourne nullable
let name: string? = user?.name;
```

---

## 3. Alias de type

### Motivation

Les types complexes bénéficient d'abréviations nommées :

```hemlock
// Actuel : types composés répétitifs
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// Proposé : alias nommé
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### Syntaxe

```hemlock
// Alias basique
type Integer = i32;
type Text = string;

// Alias de type composé
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// Alias de type fonction
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Alias nullable
type OptionalString = string?;

// Alias générique (si nous supportons les alias de type génériques)
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Alias de type tableau
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### Portée et visibilité

```hemlock
// Portée module par défaut
type Callback = fn(Event): void;

// Exportable
export type Handler = fn(Request): Response;

// Dans un autre fichier
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### Modifications de l'AST

```c
// Nouveau type d'instruction
typedef enum {
    // ... instructions existantes ...
    STMT_TYPE_ALIAS,    // NOUVEAU
} StmtKind;

// Dans l'union Stmt
struct {
    char *name;                 // Nom de l'alias
    char **type_params;         // Paramètres génériques : <T, U>
    int num_type_params;
    Type *aliased_type;         // Le type réel
} type_alias;
```

### Analyse syntaxique

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Note :** `type` est un nouveau mot-clé. Vérifier les conflits avec les identifiants existants.

### Résolution

Les alias de type sont résolus à :
- **Temps d'analyse :** L'alias est enregistré dans l'environnement de types
- **Temps de vérification :** L'alias est développé vers le type sous-jacent
- **Exécution :** L'alias est transparent (même que le type sous-jacent)

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32" (pas "MyInt")
```

---

## 4. Paramètres const

### Motivation

Signaler l'intention d'immuabilité dans les signatures de fonction :

```hemlock
// Actuel : pas clair si array sera modifié
fn print_all(items: array) { ... }

// Proposé : contrat d'immuabilité explicite
fn print_all(const items: array) { ... }
```

### Syntaxe

```hemlock
// Paramètre const
fn process(const data: buffer) {
    // data[0] = 0;        // ERREUR : impossible de muter const
    let x = data[0];       // OK : lecture autorisée
    return x;
}

// Plusieurs paramètres const
fn compare(const a: array, const b: array): bool { ... }

// Mélange const et mutable
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK : target est mutable
    }
}

// Const avec inférence de type
fn log(const msg) {
    print(msg);
}

// Const dans les types fonction
type Reader = fn(const buffer): i32;
```

### Ce que const empêche

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // ERREUR : méthode de mutation
    arr.pop();           // ERREUR : méthode de mutation
    arr[0] = 5;          // ERREUR : affectation par index
    arr.clear();         // ERREUR : méthode de mutation
}

fn ok(const arr: array) {
    let x = arr[0];      // OK : lecture
    let len = len(arr);  // OK : vérification de longueur
    let copy = arr.slice(0, 10);  // OK : crée un nouveau tableau
    for (item in arr) {  // OK : itération
        print(item);
    }
}
```

### Méthodes mutantes vs non-mutantes

| Type | Mutantes (bloquées par const) | Non-mutantes (autorisées) |
|------|-------------------------------|---------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (sur place) | slice, concat, map, filter, find, contains, first, last, join |
| string | affectation par index (`s[0] = 'x'`) | toutes les méthodes (retournent de nouvelles chaînes) |
| buffer | affectation par index, memset, memcpy (vers) | lecture par index, slice |
| object | affectation de champ | lecture de champ |

### Modifications de l'AST

```c
// Dans l'expression fonction (include/ast.h)
struct {
    // ... champs existants ...
    int *param_is_const;    // NOUVEAU : 1 si const, 0 sinon
} function;

// Dans la struct Type pour les types fonction
struct Type {
    // ... champs existants ...
    int *param_is_const;    // Pour TYPE_FUNCTION
};
```

### Application

**Interpréteur :**
- Suivre la propriété const dans les liaisons de variables
- Vérifier avant les opérations de mutation
- Erreur à l'exécution en cas de violation const

**Compilateur :**
- Émettre des variables C qualifiées const si bénéfique
- Analyse statique des violations const
- Avertissement/erreur à la compilation

---

## 5. Signatures de méthode dans define

### Motivation

Permettre aux blocs `define` de spécifier les méthodes attendues, pas seulement les champs de données :

```hemlock
// Actuel : seulement les champs de données
define User {
    name: string;
    age: i32;
}

// Proposé : signatures de méthode
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // Méthode statique
}
```

### Syntaxe

```hemlock
// Signature de méthode (pas de corps)
define Hashable {
    fn hash(): i32;
}

// Plusieurs méthodes
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// Mélange de champs et méthodes
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Utilisation du type Self
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// Méthodes optionnelles
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // Méthode optionnelle (peut être absente)
}

// Méthodes avec implémentations par défaut
define Ordered {
    fn compare(other: Self): i32;  // Requis

    // Implémentations par défaut (héritées si non surchargées)
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### Le type `Self`

`Self` fait référence au type concret implémentant l'interface :

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// Quand utilisé :
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### Typage structurel (duck typing)

Les signatures de méthode utilisent le même duck typing que les champs :

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// Tout objet avec une méthode to_string() satisfait Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// Types composés avec méthodes
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Nom : " + self.name; }
};
```

### Modifications de l'AST

```c
// Étendre define_object dans l'union Stmt
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Champs (existants)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Méthodes (NOUVEAU)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Méthodes optionnelles (fn name?(): type)
    Expr **method_defaults;     // Implémentations par défaut (NULL si signature seulement)
    int num_methods;
} define_object;
```

### Vérification de types

Lors de la vérification de `value: InterfaceType` :
1. Vérifier que tous les champs requis existent avec des types compatibles
2. Vérifier que toutes les méthodes requises existent avec des signatures compatibles
3. Les champs/méthodes optionnels peuvent être absents

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// Valide : a la méthode compare
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Invalide : compare manquant
let invalid: Sortable = { value: 10 };  // ERREUR : méthode 'compare' manquante

// Invalide : mauvaise signature
let wrong: Sortable = {
    compare: fn() { return 0; }  // ERREUR : attendu (Self): i32
};
```

---

## Exemples d'interaction

### Combinaison de toutes les fonctionnalités

```hemlock
// Alias de type pour type fonction complexe
type EventCallback = fn(event: Event, context: Context?): bool;

// Alias de type pour interface composée
type Entity = HasId & HasName & Serializable;

// Define avec signatures de méthode
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// Utilisation de tout ensemble
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### Callbacks avec types explicites

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Types fonction nullable

```hemlock
// Callback optionnel
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// Retour nullable depuis un type fonction
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## Feuille de route d'implémentation

### Phase 1 : Infrastructure de base
1. Ajouter `TYPE_FUNCTION` à l'enum TypeKind
2. Étendre la struct Type avec les champs de type fonction
3. Ajouter `CHECKED_FUNCTION` au vérificateur de types du compilateur
4. Ajouter le support du type `Self` (TYPE_SELF)

### Phase 2 : Analyse syntaxique
1. Implémenter `parse_function_type()` dans le parser
2. Gérer `fn(...)` en position de type
3. Ajouter le mot-clé `type` et l'analyse de `STMT_TYPE_ALIAS`
4. Ajouter l'analyse du modificateur de paramètre `const`
5. Étendre l'analyse de define pour les signatures de méthode

### Phase 3 : Vérification de types
1. Règles de compatibilité des types fonction
2. Résolution et expansion des alias de type
3. Vérification de mutation des paramètres const
4. Validation des signatures de méthode dans les types define
5. Résolution du type Self

### Phase 4 : Exécution
1. Validation du type fonction aux sites d'appel
2. Détection des violations const
3. Transparence des alias de type

### Phase 5 : Tests de parité
1. Tests d'annotation de type fonction
2. Tests de composition nullable
3. Tests d'alias de type
4. Tests de paramètres const
5. Tests de signatures de méthode

---

## Décisions de conception

### 1. Alias de type génériques : **OUI**

Les alias de type supportent les paramètres génériques :

```hemlock
// Alias de type génériques
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Utilisation
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Propagation const : **PROFONDE**

Les paramètres const sont totalement immuables - pas de mutation par aucun chemin :

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // ERREUR : impossible de muter un tableau const
    arr[0] = {};         // ERREUR : impossible de muter un tableau const
    arr[0].x = 5;        // ERREUR : impossible de muter à travers const (PROFOND)

    let x = arr[0].x;    // OK : la lecture est autorisée
    let copy = arr[0];   // OK : crée une copie
    copy.x = 5;          // OK : la copie n'est pas const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // ERREUR : const profond empêche la mutation imbriquée
    obj.items[0] = 1;    // ERREUR : const profond empêche la mutation imbriquée
}
```

**Justification :** Le const profond fournit des garanties plus fortes et est plus utile pour
assurer l'intégrité des données. Si vous devez muter des données imbriquées, faites d'abord une copie.

### 3. Self dans les alias de type autonomes : **NON**

`Self` n'est valide qu'à l'intérieur des blocs `define` où il a un sens clair :

```hemlock
// Valide : Self fait référence au type défini
define Comparable {
    fn compare(other: Self): i32;
}

// Invalide : Self n'a pas de sens ici
type Cloner = fn(Self): Self;  // ERREUR : Self en dehors du contexte define

// À la place, utilisez les génériques :
type Cloner<T> = fn(T): T;
```

### 4. Implémentations de méthode par défaut : **OUI (simples seulement)**

Autoriser les implémentations par défaut pour les méthodes simples/utilitaires :

```hemlock
define Comparable {
    // Requis : doit être implémenté
    fn compare(other: Self): i32;

    // Implémentations par défaut (méthodes de commodité simples)
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // Défaut : délègue à la méthode requise
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// L'objet doit seulement implémenter les méthodes requises
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_than sont héritées des valeurs par défaut
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**Directives pour les valeurs par défaut :**
- Les garder simples (1-3 lignes)
- Devraient déléguer aux méthodes requises
- Pas de logique complexe ni d'effets de bord
- Primitives et compositions simples uniquement

### 5. Variance : **INFÉRÉE (pas d'annotations explicites)**

La variance est inférée de la façon dont les paramètres de type sont utilisés :

```hemlock
// La variance est automatique basée sur la position
type Producer<T> = fn(): T;           // T en retour = covariant
type Consumer<T> = fn(T): void;       // T en paramètre = contravariant
type Transformer<T> = fn(T): T;       // T dans les deux = invariant

// Exemple : Dog <: Animal (Dog est un sous-type de Animal)
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK : covariant

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK : contravariant
```

**Pourquoi inférer ?**
- Moins de code répétitif (`<out T>` / `<in T>` ajoute du bruit)
- Suit "explicite plutôt qu'implicite" - la position EST explicite
- Correspond à la façon dont la plupart des langages gèrent la variance des types fonction
- Les erreurs sont claires quand les règles de variance sont violées

---

## Annexe : Modifications de la grammaire

```ebnf
(* Types *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* Instructions *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" marque une méthode optionnelle, block fournit l'implémentation par défaut *)

(* Paramètres *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
