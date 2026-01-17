# Référence du système de types

Référence complète pour le système de types de Hemlock, y compris tous les types primitifs et composites.

---

## Aperçu

Hemlock utilise un **système de types dynamique** avec des étiquettes de type à l'exécution et des annotations de type optionnelles. Chaque valeur a un type à l'exécution, et les conversions de type suivent des règles de promotion explicites.

**Caractéristiques principales :**
- Vérification de type à l'exécution (interpréteur)
- Vérification de type à la compilation (hemlockc - activée par défaut)
- Annotations de type optionnelles
- Inférence de type automatique pour les littéraux
- Règles de promotion de type explicites
- Pas de conversions implicites qui perdent de la précision

---

## Vérification de type à la compilation (hemlockc)

Le compilateur Hemlock (`hemlockc`) inclut un vérificateur de types à la compilation qui valide votre code avant de générer les exécutables. Cela attrape les erreurs de type tôt sans avoir besoin d'exécuter le programme.

### Comportement par défaut

La vérification de type est **activée par défaut** dans hemlockc :

```bash
# La vérification de type se fait automatiquement
hemlockc program.hml -o program

# Les erreurs sont signalées avant la compilation
hemlockc bad_types.hml
# Sortie: 1 type error found
```

### Options du compilateur

| Option | Description |
|--------|-------------|
| `--check` | Vérifier les types uniquement, ne pas compiler (quitter après validation) |
| `--no-type-check` | Désactiver la vérification de type (non recommandé) |
| `--strict-types` | Activer des avertissements de type plus stricts |

**Exemples :**

```bash
# Juste valider les types sans compiler
hemlockc --check program.hml
# Sortie: program.hml: no type errors

# Désactiver la vérification de type (utiliser avec précaution)
hemlockc --no-type-check dynamic_code.hml -o program

# Activer les avertissements stricts pour les types any implicites
hemlockc --strict-types program.hml -o program
```

### Ce que le vérificateur de types valide

1. **Annotations de type** - S'assure que les valeurs assignées correspondent aux types déclarés
2. **Appels de fonction** - Valide les types d'arguments contre les types de paramètres
3. **Types de retour** - Vérifie que les instructions return correspondent au type de retour déclaré
4. **Utilisation des opérateurs** - Vérifie que les opérandes sont compatibles
5. **Accès aux propriétés** - Valide les types de champs d'objet pour les objets typés

### Conversions numériques permissives

Le vérificateur de types autorise les conversions de types numériques à la compilation, avec validation de plage à l'exécution :

```hemlock
let x: i8 = 100;      // OK - 100 tient dans i8 (validé à l'exécution)
let y: u8 = 255;      // OK - dans la plage u8
let z: f64 = 42;      // OK - i32 vers f64 est sûr
```

### Support du code dynamique

Le code sans annotations de type est traité comme dynamique (type `any`) et passe toujours le vérificateur de types :

```hemlock
let x = get_value();  // Dynamique - pas d'annotation
process(x);           // OK - les valeurs dynamiques sont acceptées partout
```

---

## Types primitifs

### Types numériques

#### Entiers signés

| Type   | Taille   | Plage                                      | Alias     |
|--------|----------|-------------------------------------------|-----------|
| `i8`   | 1 octet  | -128 à 127                                | -         |
| `i16`  | 2 octets | -32 768 à 32 767                          | -         |
| `i32`  | 4 octets | -2 147 483 648 à 2 147 483 647            | `integer` |
| `i64`  | 8 octets | -9 223 372 036 854 775 808 à 9 223 372 036 854 775 807 | - |

**Exemples :**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Alias de type
let x: integer = 42;  // Identique à i32
```

#### Entiers non signés

| Type   | Taille   | Plage                        | Alias  |
|--------|----------|------------------------------|--------|
| `u8`   | 1 octet  | 0 à 255                      | `byte` |
| `u16`  | 2 octets | 0 à 65 535                   | -      |
| `u32`  | 4 octets | 0 à 4 294 967 295            | -      |
| `u64`  | 8 octets | 0 à 18 446 744 073 709 551 615 | -   |

**Exemples :**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Alias de type
let byte_val: byte = 65;  // Identique à u8
```

#### Virgule flottante

| Type   | Taille   | Précision      | Alias    |
|--------|----------|----------------|----------|
| `f32`  | 4 octets | ~7 chiffres    | -        |
| `f64`  | 8 octets | ~15 chiffres   | `number` |

**Exemples :**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// Alias de type
let x: number = 2.718;  // Identique à f64
```

---

### Inférence de type pour les littéraux entiers

Les littéraux entiers sont automatiquement typés en fonction de leur valeur :

**Règles :**
- Valeurs dans la plage i32 (-2 147 483 648 à 2 147 483 647) : inférer comme `i32`
- Valeurs hors de la plage i32 mais dans la plage i64 : inférer comme `i64`
- Utiliser des annotations de type explicites pour les autres types (i8, i16, u8, u16, u32, u64)

**Exemples :**
```hemlock
let small = 42;                    // i32 (tient dans i32)
let large = 5000000000;            // i64 (> max i32)
let max_i64 = 9223372036854775807; // i64 (INT64_MAX)
let explicit: u32 = 100;           // u32 (l'annotation de type prévaut)
```

---

### Type booléen

**Type :** `bool`

**Valeurs :** `true`, `false`

**Taille :** 1 octet (en interne)

**Exemples :**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("en cours");
}
```

---

### Types de caractères

#### Rune

**Type :** `rune`

**Description :** Point de code Unicode (U+0000 à U+10FFFF)

**Taille :** 4 octets (valeur 32 bits)

**Plage :** 0 à 0x10FFFF (1 114 111)

**Syntaxe littérale :** Guillemets simples `'x'`

**Exemples :**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// UTF-8 multi-octets
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// Séquences d'échappement
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Échappements Unicode
let emoji = '\u{1F680}';   // Jusqu'à 6 chiffres hexadécimaux
let max = '\u{10FFFF}';    // Point de code maximum
```

**Conversions de type :**
```hemlock
// Entier vers rune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// Rune vers entier
let value: i32 = 'Z';       // 90

// Rune vers chaîne
let s: string = 'H';        // "H"

// u8 vers rune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**Voir aussi :** [API String](string-api.md) pour la concaténation string + rune

---

### Type chaîne

**Type :** `string`

**Description :** Texte encodé en UTF-8, mutable, alloué sur le tas

**Encodage :** UTF-8 (U+0000 à U+10FFFF)

**Mutabilité :** Mutable (contrairement à la plupart des langages)

**Propriétés :**
- `.length` - Nombre de points de code (nombre de caractères)
- `.byte_length` - Nombre d'octets (taille de l'encodage UTF-8)

**Syntaxe littérale :** Guillemets doubles `"texte"`

**Exemples :**
```hemlock
let s = "hello";
s[0] = 'H';             // Modifier (maintenant "Hello")
print(s.length);        // 5 (nombre de points de code)
print(s.byte_length);   // 5 (octets UTF-8)

let emoji = "🚀";
print(emoji.length);        // 1 (un point de code)
print(emoji.byte_length);   // 4 (quatre octets UTF-8)
```

**Indexation :**
```hemlock
let s = "hello";
let ch = s[0];          // Retourne le rune 'h'
s[0] = 'H';             // Définir avec un rune
```

**Voir aussi :** [API String](string-api.md) pour la référence complète des méthodes

---

### Type null

**Type :** `null`

**Description :** La valeur null (absence de valeur)

**Taille :** 8 octets (en interne)

**Valeur :** `null`

**Exemples :**
```hemlock
let x = null;
let y: i32 = null;  // ERREUR: incompatibilité de type

if (x == null) {
    print("x est null");
}
```

---

## Types composites

### Type tableau

**Type :** `array`

**Description :** Tableau dynamique, alloué sur le tas, de types mixtes

**Propriétés :**
- `.length` - Nombre d'éléments

**Indexation base zéro :** Oui

**Syntaxe littérale :** `[elem1, elem2, ...]`

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Types mixtes
let mixed = [1, "hello", true, null];
```

**Voir aussi :** [API Array](array-api.md) pour la référence complète des méthodes

---

### Type objet

**Type :** `object`

**Description :** Objet de style JavaScript avec champs dynamiques

**Syntaxe littérale :** `{ field: value, ... }`

**Exemples :**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// Ajouter un champ dynamiquement
person.email = "alice@example.com";
```

**Définitions de type :**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // Champ optionnel
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### Types de pointeur

#### Pointeur brut (ptr)

**Type :** `ptr`

**Description :** Adresse mémoire brute (non sûr)

**Taille :** 8 octets

**Vérification des limites :** Aucune

**Exemples :**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### Buffer (buffer)

**Type :** `buffer`

**Description :** Enveloppe de pointeur sécurisée avec vérification des limites

**Structure :** Pointeur + longueur + capacité

**Propriétés :**
- `.length` - Taille du buffer
- `.capacity` - Capacité allouée

**Exemples :**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Vérifié aux limites
print(b.length);        // 64
free(b);
```

**Voir aussi :** [API Memory](memory-api.md) pour les fonctions d'allocation

---

## Types spéciaux

### Type file

**Type :** `file`

**Description :** Handle de fichier pour les opérations d'E/S

**Propriétés :**
- `.path` - Chemin du fichier (string)
- `.mode` - Mode d'ouverture (string)
- `.closed` - Si le fichier est fermé (bool)

**Voir aussi :** [API File](file-api.md)

---

### Type task

**Type :** `task`

**Description :** Handle pour une tâche concurrente

**Voir aussi :** [API Concurrency](concurrency-api.md)

---

### Type channel

**Type :** `channel`

**Description :** Canal de communication thread-safe

**Voir aussi :** [API Concurrency](concurrency-api.md)

---

### Type function

**Type :** `function`

**Description :** Valeur de fonction de première classe

**Exemples :**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Type void

**Type :** `void`

**Description :** Absence de valeur de retour (usage interne)

---

## Règles de promotion de type

Lors du mélange de types dans les opérations, Hemlock promeut vers le type "supérieur" :

**Hiérarchie de promotion :**
```
f64 (plus haute précision)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (plus basse)
```

**Règles :**
1. Le flottant gagne toujours sur l'entier
2. La plus grande taille gagne dans la même catégorie (int/uint/float)
3. Les deux opérandes sont promus vers le type résultat
4. **Préservation de la précision :** i64/u64 + f32 promeut vers f64 (pas f32)

**Exemples :**
```hemlock
// Promotion de taille
u8 + i32    → i32    // La plus grande taille gagne
i32 + i64   → i64    // La plus grande taille gagne
u32 + u64   → u64    // La plus grande taille gagne

// Promotion flottante
i32 + f32   → f32    // Le flottant gagne, f32 suffit pour i32
i64 + f32   → f64    // Promeut vers f64 pour préserver la précision i64
i64 + f64   → f64    // Le flottant gagne toujours
i8 + f64    → f64    // Flottant + plus grand gagne
```

**Pourquoi i64 + f32 → f64 ?**

f32 n'a qu'une mantisse de 24 bits, qui ne peut pas représenter précisément les entiers plus grands que 2^24 (16 777 216). Puisque i64 peut contenir des valeurs jusqu'à 2^63, mélanger i64 avec f32 causerait une perte de précision sévère. Hemlock promeut vers f64 (mantisse de 53 bits) à la place.

---

## Vérification de plage

Les annotations de type appliquent des vérifications de plage à l'affectation :

**Affectations valides :**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**Affectations invalides (erreur d'exécution) :**
```hemlock
let x: u8 = 256;             // ERREUR: hors plage
let y: i8 = 128;             // ERREUR: max est 127
let z: u64 = -1;             // ERREUR: u64 ne peut pas être négatif
```

---

## Introspection de type

### typeof(value)

Retourne le nom du type sous forme de chaîne.

**Signature :**
```hemlock
typeof(value: any): string
```

**Retourne :**
- Types primitifs : `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Types composites : `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Types spéciaux : `"file"`, `"task"`, `"channel"`
- Objets typés : Nom de type personnalisé (ex., `"Person"`)

**Exemples :**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**Voir aussi :** [Fonctions intégrées](builtins.md#typeof)

---

## Conversions de type

### Conversions implicites

Hemlock effectue des conversions de type implicites dans les opérations arithmétiques suivant les règles de promotion de type.

**Exemples :**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // result est i32 (promu)
```

### Conversions explicites

Utilisez les annotations de type pour les conversions explicites :

**Exemples :**
```hemlock
// Entier vers flottant
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Flottant vers entier (tronque)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Entier vers rune
let code: rune = 65;    // 'A'

// Rune vers entier
let value: i32 = 'Z';   // 90

// Rune vers chaîne
let s: string = 'H';    // "H"
```

---

## Alias de type

### Alias intégrés

Hemlock fournit des alias de type intégrés pour les types courants :

| Alias     | Type réel | Usage                        |
|-----------|-----------|------------------------------|
| `integer` | `i32`     | Entiers à usage général      |
| `number`  | `f64`     | Flottants à usage général    |
| `byte`    | `u8`      | Valeurs d'octets             |

**Exemples :**
```hemlock
let count: integer = 100;       // Identique à i32
let price: number = 19.99;      // Identique à f64
let b: byte = 255;              // Identique à u8
```

### Alias de type personnalisés

Définissez des alias de type personnalisés avec le mot-clé `type` :

```hemlock
// Alias simples
type Integer = i32;
type Text = string;

// Alias de type fonction
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// Alias de type composé
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Alias de type générique
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**Utilisation des alias personnalisés :**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Note :** Les alias de type sont transparents - `typeof()` retourne le nom du type sous-jacent.

---

## Types de fonction

Les types de fonction spécifient la signature des valeurs de fonction :

### Syntaxe

```hemlock
fn(types_paramètres): type_retour
```

### Exemples

```hemlock
// Type de fonction basique
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Paramètre de fonction
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Fonction d'ordre supérieur retournant une fonction
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Type de fonction async
fn run_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## Types composés (intersection)

Les types composés utilisent `&` pour exiger plusieurs contraintes de type :

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// L'objet doit satisfaire tous les types
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Trois types ou plus
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## Tableau récapitulatif

| Type       | Taille    | Mutable | Alloué sur le tas | Description                    |
|------------|-----------|---------|-------------------|--------------------------------|
| `i8`-`i64` | 1-8 octets| Non     | Non               | Entiers signés                 |
| `u8`-`u64` | 1-8 octets| Non     | Non               | Entiers non signés             |
| `f32`      | 4 octets  | Non     | Non               | Flottant simple précision      |
| `f64`      | 8 octets  | Non     | Non               | Flottant double précision      |
| `bool`     | 1 octet   | Non     | Non               | Booléen                        |
| `rune`     | 4 octets  | Non     | Non               | Point de code Unicode          |
| `string`   | Variable  | Oui     | Oui               | Texte UTF-8                    |
| `array`    | Variable  | Oui     | Oui               | Tableau dynamique              |
| `object`   | Variable  | Oui     | Oui               | Objet dynamique                |
| `ptr`      | 8 octets  | Non     | Non               | Pointeur brut                  |
| `buffer`   | Variable  | Oui     | Oui               | Enveloppe de pointeur sécurisée|
| `file`     | Opaque    | Oui     | Oui               | Handle de fichier              |
| `task`     | Opaque    | Non     | Oui               | Handle de tâche concurrente    |
| `channel`  | Opaque    | Oui     | Oui               | Canal thread-safe              |
| `function` | Opaque    | Non     | Oui               | Valeur de fonction             |
| `null`     | 8 octets  | Non     | Non               | Valeur null                    |

---

## Voir aussi

- [Référence des opérateurs](operators.md) - Comportement des types dans les opérations
- [Fonctions intégrées](builtins.md) - Introspection et conversion de types
- [API String](string-api.md) - Méthodes du type string
- [API Array](array-api.md) - Méthodes du type array
- [API Memory](memory-api.md) - Opérations sur les pointeurs et buffers
