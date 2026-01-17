# Systeme de types

Hemlock dispose d'un **systeme de types dynamique** avec des annotations de type optionnelles et une verification de type a l'execution.

---

## Guide de selection des types : Quel type dois-je utiliser ?

**Nouveau avec les types ?** Commencez ici. Si vous etes familier avec les systemes de types, passez directement a [Philosophie](#philosophie).

### La reponse courte

**Laissez simplement Hemlock determiner le type :**

```hemlock
let count = 42;        // Hemlock sait que c'est un entier
let price = 19.99;     // Hemlock sait que c'est un decimal
let name = "Alice";    // Hemlock sait que c'est du texte
let active = true;     // Hemlock sait que c'est oui/non
```

Hemlock choisit automatiquement le bon type pour vos valeurs. Vous n'avez pas *besoin* de specifier les types.

### Quand ajouter des annotations de type

Ajoutez des types quand vous voulez :

1. **Etre specifique sur la taille** - `i8` vs `i64` est important pour la memoire ou FFI
2. **Documenter votre code** - Les types montrent ce qu'une fonction attend
3. **Detecter les erreurs tot** - Hemlock verifie les types a l'execution

```hemlock
// Sans types (fonctionne bien) :
fn add(a, b) {
    return a + b;
}

// Avec types (plus explicite) :
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Reference rapide : Choisir les types numeriques

| Ce que vous stockez | Type suggere | Exemple |
|---------------------|--------------|---------|
| Nombres entiers reguliers | `i32` (par defaut) | `let count = 42;` |
| Tres grands nombres | `i64` | `let population = 8000000000;` |
| Comptages jamais negatifs | `u32` | `let items: u32 = 100;` |
| Octets (0-255) | `u8` | `let pixel: u8 = 255;` |
| Decimaux/fractions | `f64` (par defaut) | `let price = 19.99;` |
| Decimaux critiques pour la performance | `f32` | `let x: f32 = 1.5;` |

### Reference rapide : Tous les types

| Categorie | Types | Quand utiliser |
|-----------|-------|----------------|
| **Nombres entiers** | `i8`, `i16`, `i32`, `i64` | Comptage, identifiants, ages, etc. |
| **Nombres positifs uniquement** | `u8`, `u16`, `u32`, `u64` | Octets, tailles, longueurs de tableau |
| **Decimaux** | `f32`, `f64` | Argent, mesures, mathematiques |
| **Oui/Non** | `bool` | Drapeaux, conditions |
| **Texte** | `string` | Noms, messages, tout texte |
| **Caractere unique** | `rune` | Lettres individuelles, emoji |
| **Listes** | `array` | Collections de valeurs |
| **Champs nommes** | `object` | Groupement de donnees liees |
| **Memoire brute** | `ptr`, `buffer` | Programmation bas niveau |
| **Rien** | `null` | Absence de valeur |

### Scenarios courants

**"J'ai juste besoin d'un nombre"**
```hemlock
let x = 42;  // Fait ! Hemlock choisit i32
```

**"J'ai besoin de decimaux"**
```hemlock
let price = 19.99;  // Fait ! Hemlock choisit f64
```

**"Je travaille avec des octets (fichiers, reseau)"**
```hemlock
let byte: u8 = 255;  // Plage 0-255
```

**"J'ai besoin de tres grands nombres"**
```hemlock
let big = 9000000000000;  // Hemlock choisit automatiquement i64 (> i32 max)
// Ou soyez explicite :
let big: i64 = 9000000000000;
```

**"Je stocke de l'argent"**
```hemlock
// Option 1 : Float (simple, mais a des limites de precision)
let price: f64 = 19.99;

// Option 2 : Stocker en centimes (plus precis)
let price_cents: i32 = 1999;  // 19.99 EUR en centimes entiers
```

**"Je passe des donnees au code C (FFI)"**
```hemlock
// Correspondre exactement aux types C
let c_int: i32 = 100;      // C 'int'
let c_long: i64 = 100;     // C 'long' (sur 64-bit)
let c_char: u8 = 65;       // C 'char'
let c_double: f64 = 3.14;  // C 'double'
```

### Que se passe-t-il quand les types se melangent ?

Quand vous combinez differents types, Hemlock promeut vers le type "plus grand" :

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // result est f64 (12.5)
// L'entier est devenu un decimal automatiquement
```

**Regle generale :** Les flottants "gagnent" toujours - melanger un entier avec un flottant donne un flottant.

### Erreurs de type

Si vous essayez d'utiliser le mauvais type, Hemlock vous le dit a l'execution :

```hemlock
let age: i32 = "trente";  // ERREUR : type mismatch - expected i32, got string
```

Pour convertir les types, utilisez les fonctions constructeur de type :

```hemlock
let text = "42";
let number = i32(text);   // Analyser la chaine vers un entier : 42
let back = text + "";     // Deja une chaine
```

---

## Philosophie

- **Dynamique par defaut** - Chaque valeur a une etiquette de type a l'execution
- **Type par choix** - Les annotations de type optionnelles appliquent des verifications a l'execution
- **Conversions explicites** - Les conversions implicites suivent des regles de promotion claires
- **Honnete sur les types** - `typeof()` dit toujours la verite

## Types primitifs

### Types entiers

**Entiers signes :**
```hemlock
let tiny: i8 = 127;              // 8-bit  (-128 a 127)
let small: i16 = 32767;          // 16-bit (-32768 a 32767)
let normal: i32 = 2147483647;    // 32-bit (par defaut)
let large: i64 = 9223372036854775807;  // 64-bit
```

**Entiers non signes :**
```hemlock
let byte: u8 = 255;              // 8-bit  (0 a 255)
let word: u16 = 65535;           // 16-bit (0 a 65535)
let dword: u32 = 4294967295;     // 32-bit (0 a 4294967295)
let qword: u64 = 18446744073709551615;  // 64-bit
```

**Alias de type :**
```hemlock
let i: integer = 42;   // Alias pour i32
let b: byte = 255;     // Alias pour u8
```

### Types a virgule flottante

```hemlock
let f: f32 = 3.14159;        // Flottant 32-bit
let d: f64 = 2.718281828;    // Flottant 64-bit (par defaut)
let n: number = 1.618;       // Alias pour f64
```

### Type booleen

```hemlock
let flag: bool = true;
let active: bool = false;
```

### Type chaine

```hemlock
let text: string = "Bonjour, le monde !";
let empty: string = "";
```

Les chaines sont **mutables**, **encodees en UTF-8**, et **allouees sur le tas**.

Voir [Chaines](strings.md) pour les details complets.

### Type rune

```hemlock
let ch: rune = 'A';
let emoji: rune = 'rocket';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

Les runes representent des **points de code Unicode** (U+0000 a U+10FFFF).

Voir [Runes](runes.md) pour les details complets.

### Type null

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null` est son propre type avec une seule valeur.

## Types composes

### Type tableau

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "deux", true, null];  // Types mixtes autorises
let empty: array = [];
```

Voir [Tableaux](arrays.md) pour les details complets.

### Type objet

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

Voir [Objets](objects.md) pour les details complets.

### Types pointeur

**Pointeur brut :**
```hemlock
let p: ptr = alloc(64);
// Pas de verification des limites, gestion manuelle de la duree de vie
free(p);
```

**Tampon securise :**
```hemlock
let buf: buffer = buffer(64);
// Verification des limites, suit la longueur et la capacite
free(buf);
```

Voir [Gestion de la memoire](memory.md) pour les details complets.

## Types enum

Les enums definissent un ensemble de constantes nommees :

### Enums basiques

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// Comparaison
if (c == Color.RED) {
    print("C'est rouge !");
}

// Switch sur enum
switch (c) {
    case Color.RED:
        print("Stop");
        break;
    case Color.GREEN:
        print("Allez");
        break;
    case Color.BLUE:
        print("Bleu ?");
        break;
}
```

### Enums avec valeurs

Les enums peuvent avoir des valeurs entieres explicites :

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### Valeurs auto-incrementees

Sans valeurs explicites, les enums s'auto-incrementent a partir de 0 :

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// Peut melanger valeurs explicites et auto
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### Modeles d'utilisation des enums

```hemlock
// Comme parametres de fonction
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Urgent !");
    }
}

set_priority(Priority.HIGH);

// Dans les objets
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Corriger le bug",
    priority: Priority.HIGH
};
```

## Types speciaux

### Type fichier

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

Represente un descripteur de fichier ouvert.

### Type tache

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

Represente un descripteur de tache asynchrone.

### Type canal

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

Represente un canal de communication entre taches.

### Type void

```hemlock
extern fn exit(code: i32): void;
```

Utilise pour les fonctions qui ne retournent pas de valeur (FFI seulement).

## Inference de type

### Inference de litteraux entiers

Hemlock infere les types entiers en fonction de la plage de valeurs :

```hemlock
let a = 42;              // i32 (tient dans 32-bit)
let b = 5000000000;      // i64 (> i32 max)
let c = 128;             // i32
let d: u8 = 128;         // u8 (annotation explicite)
```

**Regles :**
- Valeurs dans la plage i32 (-2147483648 a 2147483647) : infere comme `i32`
- Valeurs hors plage i32 mais dans i64 : infere comme `i64`
- Utilisez des annotations explicites pour les autres types (i8, i16, u8, u16, u32, u64)

### Inference de litteraux flottants

```hemlock
let x = 3.14;        // f64 (par defaut)
let y: f32 = 3.14;   // f32 (explicite)
```

### Notation scientifique

Hemlock supporte la notation scientifique pour les litteraux numeriques :

```hemlock
let a = 1e10;        // 10000000000.0 (f64)
let b = 1e-12;       // 0.000000000001 (f64)
let c = 3.14e2;      // 314.0 (f64)
let d = 2.5e-3;      // 0.0025 (f64)
let e = 1E10;        // Insensible a la casse
let f = 1e+5;        // Exposant positif explicite
```

**Note :** Tout litteral utilisant la notation scientifique est toujours infere comme `f64`.

### Autre inference de type

```hemlock
let s = "bonjour";   // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## Annotations de type

### Annotations de variable

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### Annotations de parametre de fonction

```hemlock
fn greet(name: string, age: i32) {
    print("Bonjour, " + name + " !");
}
```

### Annotations de type de retour de fonction

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Annotations de type objet (typage canard)

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## Verification de type

### Verification de type a l'execution

Les annotations de type sont verifiees a **l'execution**, pas a la compilation :

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // Erreur d'execution : type mismatch

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "bonjour");   // Erreur d'execution : type mismatch
```

### Requetes de type

Utilisez `typeof()` pour verifier les types de valeur :

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("bonjour"));  // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## Conversions de type

### Promotion de type implicite

Lors du melange de types dans les operations, Hemlock promeut vers le type "superieur" :

**Hierarchie de promotion (du plus bas au plus haut) :**
```
i8 -> i16 -> i32 -> u32 -> i64 -> u64 -> f32 -> f64
      ^      ^      ^
     u8     u16
```

**Le flottant gagne toujours :**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result est f64 (13.5)
```

**La plus grande taille gagne :**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sum est i64 (300)
```

**Preservation de la precision :** Lors du melange d'entiers 64-bit avec f32, Hemlock promeut
vers f64 pour eviter la perte de precision (f32 n'a que 24-bit de mantisse, insuffisant pour i64/u64) :
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // result est f64, pas f32 !
```

**Exemples :**
```hemlock
u8 + i32  -> i32
i32 + i64 -> i64
u32 + u64 -> u64
i32 + f32 -> f32    // f32 suffisant pour i32
i64 + f32 -> f64    // f64 necessaire pour preserver la precision i64
i64 + f64 -> f64
i8 + f64  -> f64
```

### Conversion de type explicite

**Entier <-> Flottant :**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 -> f64 (42.0)

let x: f64 = 3.14;
let n: i32 = x;      // f64 -> i32 (3, tronque)
```

**Entier <-> Rune :**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 -> rune ('A')

let r: rune = 'Z';
let value: i32 = r;   // rune -> i32 (90)
```

**Rune -> Chaine :**
```hemlock
let ch: rune = 'rocket';
let s: string = ch;   // rune -> string ("rocket")
```

**u8 -> Rune :**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 -> rune ('A')
```

### Fonctions constructeur de type

Les noms de type peuvent etre utilises comme fonctions pour convertir ou analyser des valeurs :

**Analyser des chaines vers des nombres :**
```hemlock
let n = i32("42");       // Analyser chaine vers i32 : 42
let f = f64("3.14159");  // Analyser chaine vers f64 : 3.14159
let b = bool("true");    // Analyser chaine vers bool : true

// Tous les types numeriques supportes
let a = i8("-128");      // Analyser vers i8
let c = u8("255");       // Analyser vers u8
let d = i16("1000");     // Analyser vers i16
let e = u16("50000");    // Analyser vers u16
let g = i64("9000000000000"); // Analyser vers i64
let h = u64("18000000000000"); // Analyser vers u64
let j = f32("1.5");      // Analyser vers f32
```

**Nombres hexadecimaux et negatifs :**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10 (binaire)
```

**Les alias de type fonctionnent aussi :**
```hemlock
let x = integer("100");  // Identique a i32("100")
let y = number("1.5");   // Identique a f64("1.5")
let z = byte("200");     // Identique a u8("200")
```

**Convertir entre types numeriques :**
```hemlock
let big = i64(42);           // i32 vers i64
let truncated = i32(3.99);   // f64 vers i32 (tronque a 3)
let promoted = f64(100);     // i32 vers f64 (100.0)
let narrowed = i8(127);      // i32 vers i8
```

**Les annotations de type effectuent la coercition numerique (mais PAS l'analyse de chaine) :**
```hemlock
let f: f64 = 100;        // i32 vers f64 via annotation (OK)
let s: string = 'A';     // Rune vers string via annotation (OK)
let code: i32 = 'A';     // Rune vers i32 via annotation (obtient le point de code, OK)

// L'analyse de chaine necessite des constructeurs de type explicites :
let n = i32("42");       // Utiliser le constructeur de type pour l'analyse de chaine
// let x: i32 = "42";    // ERREUR - les annotations de type n'analysent pas les chaines
```

**Gestion des erreurs :**
```hemlock
// Les chaines invalides levent des erreurs lors de l'utilisation de constructeurs de type
let bad = i32("bonjour");  // Erreur d'execution : cannot parse "bonjour" as i32
let overflow = u8("256");  // Erreur d'execution : 256 out of range for u8
```

**Analyse de booleen :**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("oui");   // Erreur d'execution : must be "true" or "false"
```

## Verification de plage

Les annotations de type appliquent des verifications de plage a l'assignation :

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // ERREUR : out of range for u8

let a: i8 = 127;    // OK
let b: i8 = 128;    // ERREUR : out of range for i8

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // ERREUR : u64 cannot be negative
```

## Exemples de promotion de type

### Types entiers mixtes

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32 (30)

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32 (300)
```

### Entier + Flottant

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32 (12.5)
```

### Expressions complexes

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64 (70.0)
// Evaluation : b * c -> f64(60.0)
//              a + f64(60.0) -> f64(70.0)
```

## Typage canard (Objets)

Les objets utilisent le **typage structurel** (typage canard) :

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK : A tous les champs requis
let p1: Person = { name: "Alice", age: 30 };

// OK : Champs supplementaires autorises
let p2: Person = { name: "Bob", age: 25, city: "NYC" };

// ERREUR : Champ 'age' manquant
let p3: Person = { name: "Carol" };

// ERREUR : Mauvais type pour 'age'
let p4: Person = { name: "Dave", age: "trente" };
```

**La verification de type se fait a l'assignation :**
- Valide que tous les champs requis sont presents
- Valide que les types de champ correspondent
- Les champs supplementaires sont autorises et preserves
- Definit le nom de type de l'objet pour `typeof()`

## Champs optionnels

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // Optionnel avec valeur par defaut
    timeout?: i32,     // Optionnel, par defaut null
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false (par defaut)
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true (remplace)
```

## Alias de type

Hemlock supporte les alias de type personnalises avec le mot-cle `type` :

### Alias de type basiques

```hemlock
// Alias de type simple
type Integer = i32;
type Text = string;

// Utiliser l'alias
let x: Integer = 42;
let msg: Text = "bonjour";
```

### Alias de type fonction

```hemlock
// Alias de type fonction
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Utiliser les alias de type fonction
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### Alias de type compose

```hemlock
// Combiner plusieurs defines en un seul type
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### Alias de type generique

```hemlock
// Alias de type generique
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Utiliser les alias generiques
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Note :** Les alias de type sont transparents - `typeof()` retourne le nom du type sous-jacent, pas l'alias.

## Limitations du systeme de types

Limitations actuelles :

- **Pas de generiques sur les fonctions** - Les parametres de type de fonction pas encore supportes
- **Pas de types union** - Impossible d'exprimer "A ou B"
- **Pas de types nullables** - Tous les types peuvent etre null (utilisez le suffixe `?` pour la nullabilite explicite)

**Note :** Le compilateur (`hemlockc`) fournit une verification de type a la compilation. L'interpreteur effectue uniquement une verification de type a l'execution. Voir la [documentation du compilateur](../design/implementation.md) pour plus de details.

## Bonnes pratiques

### Quand utiliser les annotations de type

**UTILISEZ des annotations quand :**
- Le type precis compte (ex. `u8` pour les valeurs d'octet)
- Documenter les interfaces de fonction
- Appliquer des contraintes (ex. verifications de plage)

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // Implementation
}
```

**N'UTILISEZ PAS d'annotations quand :**
- Le type est evident d'apres le litteral
- Details d'implementation internes
- Ceremonie inutile

```hemlock
// Inutile
let x: i32 = 42;

// Mieux
let x = 42;
```

### Modeles de securite de type

**Verifier avant utilisation :**
```hemlock
if (typeof(value) == "i32") {
    // Securise a utiliser comme i32
}
```

**Valider les arguments de fonction :**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "les arguments doivent etre des entiers";
    }
    if (b == 0) {
        throw "division par zero";
    }
    return a / b;
}
```

**Utiliser le typage canard pour la flexibilite :**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## Prochaines etapes

- [Chaines](strings.md) - Type chaine UTF-8 et operations
- [Runes](runes.md) - Type point de code Unicode
- [Tableaux](arrays.md) - Type tableau dynamique
- [Objets](objects.md) - Litteraux d'objet et typage canard
- [Memoire](memory.md) - Types pointeur et buffer
