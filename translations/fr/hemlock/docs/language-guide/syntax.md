# Apercu de la syntaxe

Ce document couvre les regles de syntaxe fondamentales et la structure des programmes Hemlock.

## Regles de syntaxe de base

### Les points-virgules sont obligatoires

Contrairement a JavaScript ou Python, les points-virgules sont **toujours requis** a la fin des instructions :

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**Ceci provoquera une erreur :**
```hemlock
let x = 42  // ERREUR : Point-virgule manquant
let y = 10  // ERREUR : Point-virgule manquant
```

### Les accolades sont toujours requises

Tous les blocs de flux de controle doivent utiliser des accolades, meme pour les instructions simples :

```hemlock
// CORRECT
if (x > 0) {
    print("positif");
}

// ERREUR : Accolades manquantes
if (x > 0)
    print("positif");
```

### Commentaires

```hemlock
// Ceci est un commentaire sur une seule ligne

/*
   Ceci est un
   commentaire multi-lignes
*/

let x = 42;  // Commentaire en ligne
```

## Variables

### Declaration

Les variables sont declarees avec `let` :

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Annotations de type (optionnelles)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "bonjour";
```

### Constantes

Utilisez `const` pour les valeurs immuables :

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Tenter de reassigner une constante entrainera une erreur d'execution : "Cannot assign to const variable".

## Expressions

### Operateurs arithmetiques

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - Addition
print(a - b);   // 7  - Soustraction
print(a * b);   // 30 - Multiplication
print(a / b);   // 3  - Division (entiere)
```

### Operateurs de comparaison

```hemlock
print(a == b);  // false - Egal
print(a != b);  // true  - Different
print(a > b);   // true  - Superieur a
print(a < b);   // false - Inferieur a
print(a >= b);  // true  - Superieur ou egal
print(a <= b);  // false - Inferieur ou egal
```

### Operateurs logiques

```hemlock
let x = true;
let y = false;

print(x && y);  // false - ET
print(x || y);  // true  - OU
print(!x);      // false - NON
```

### Operateurs binaires (bitwise)

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - ET binaire
print(a | b);   // 14 - OU binaire
print(a ^ b);   // 6  - XOR binaire
print(a << 2);  // 48 - Decalage a gauche
print(a >> 1);  // 6  - Decalage a droite
print(~a);      // -13 - NON binaire
```

### Priorite des operateurs

De la plus haute a la plus basse :

1. `()` - Groupement
2. `!`, `~`, `-` (unaire) - Operateurs unaires
3. `*`, `/` - Multiplication, Division
4. `+`, `-` - Addition, Soustraction
5. `<<`, `>>` - Decalages binaires
6. `<`, `<=`, `>`, `>=` - Comparaisons
7. `==`, `!=` - Egalite
8. `&` - ET binaire
9. `^` - XOR binaire
10. `|` - OU binaire
11. `&&` - ET logique
12. `||` - OU logique

**Exemples :**
```hemlock
let x = 2 + 3 * 4;      // 14 (pas 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Flux de controle

### Instructions If

```hemlock
if (condition) {
    // corps
}

if (condition) {
    // branche then
} else {
    // branche else
}

if (condition1) {
    // branche 1
} else if (condition2) {
    // branche 2
} else {
    // branche par defaut
}
```

### Boucles While

```hemlock
while (condition) {
    // corps
}
```

**Exemple :**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Boucles For

**Style C :**
```hemlock
for (initialiseur; condition; increment) {
    // corps
}
```

**Exemple :**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (tableaux) :**
```hemlock
for (let item in array) {
    // corps
}
```

**Exemple :**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Instructions Switch

```hemlock
switch (expression) {
    case valeur1:
        // corps
        break;
    case valeur2:
        // corps
        break;
    default:
        // corps par defaut
        break;
}
```

**Exemple :**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Lundi");
        break;
    case 2:
        print("Mardi");
        break;
    case 3:
        print("Mercredi");
        break;
    default:
        print("Autre");
        break;
}
```

### Break et Continue

```hemlock
// Break : sortir de la boucle
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue : passer a l'iteration suivante
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Fonctions

### Fonctions nommees

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // corps
    return value;
}
```

**Exemple :**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Fonctions anonymes

```hemlock
let func = fn(params) {
    // corps
};
```

**Exemple :**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Annotations de type (optionnelles)

```hemlock
// Sans annotations (types inferes)
fn greet(name) {
    return "Bonjour, " + name;
}

// Avec annotations (verifiees a l'execution)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Objets

### Litteraux d'objet

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Exemple :**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Methodes

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Exemple :**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Definitions de type

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Exemple :**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Tableaux

### Litteraux de tableau

```hemlock
let arr = [element1, element2, element3];
```

**Exemple :**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "deux", true, null];
let empty = [];
```

### Indexation de tableau

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // Modifier un element
```

## Gestion des erreurs

### Try/Catch

```hemlock
try {
    // code risque
} catch (e) {
    // gerer l'erreur
}
```

### Try/Finally

```hemlock
try {
    // code risque
} finally {
    // s'execute toujours
}
```

### Try/Catch/Finally

```hemlock
try {
    // code risque
} catch (e) {
    // gerer l'erreur
} finally {
    // nettoyage
}
```

### Throw

```hemlock
throw expression;
```

**Exemple :**
```hemlock
if (x < 0) {
    throw "x doit etre positif";
}
```

### Panic

```hemlock
panic(message);
```

**Exemple :**
```hemlock
panic("erreur irrecuperable");
```

## Modules (experimental)

### Instructions d'export

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Instructions d'import

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Async (experimental)

### Fonctions asynchrones

```hemlock
async fn function_name(params): return_type {
    // corps
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Canaux (Channels)

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (Interface de fonction etrangere)

### Importer une bibliotheque partagee

```hemlock
import "library_name.so";
```

### Declarer une fonction externe

```hemlock
extern fn function_name(param: type): return_type;
```

**Exemple :**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Litteraux

### Litteraux entiers

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // Auto i64

// Hexadecimal (prefixe 0x)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Binaire (prefixe 0b)
let bin = 0b1010;
let bin2 = 0b11110000;

// Octal (prefixe 0o)
let oct = 0o777;
let oct2 = 0O123;

// Separateurs numeriques pour la lisibilite
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Litteraux flottants

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // Notation scientifique
let sci2 = 2.5E+3;       // E majuscule fonctionne aussi
let no_lead = .5;        // Sans zero initial (0.5)
let sep = 3.14_159_265;  // Separateurs numeriques
```

### Litteraux de chaine

```hemlock
let s = "bonjour";
let escaped = "ligne1\nligne2\ttabulation";
let quote = "Elle a dit \"bonjour\"";

// Sequences d'echappement hexadecimales
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Sequences d'echappement Unicode
let emoji = "\u{1F600}";               // grinning face
let heart = "\u{2764}";                // coeur
let mixed = "Bonjour \u{1F30D}!";      // Bonjour globe!
```

**Sequences d'echappement :**
- `\n` - nouvelle ligne
- `\t` - tabulation
- `\r` - retour chariot
- `\\` - barre oblique inverse
- `\"` - guillemet double
- `\'` - guillemet simple
- `\0` - caractere nul
- `\xNN` - echappement hexadecimal (2 chiffres)
- `\u{XXXX}` - echappement unicode (1-6 chiffres)

### Litteraux de rune

```hemlock
let ch = 'A';
let emoji = 'rocket';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Litteraux booleens

```hemlock
let t = true;
let f = false;
```

### Litteral null

```hemlock
let nothing = null;
```

## Regles de portee

### Portee de bloc

Les variables sont limitees au bloc englobant le plus proche :

```hemlock
let x = 1;  // Portee externe

if (true) {
    let x = 2;  // Portee interne (masque l'externe)
    print(x);   // 2
}

print(x);  // 1
```

### Portee de fonction

Les fonctions creent leur propre portee :

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // Peut lire la portee externe
}

foo();
// print(local);  // ERREUR : 'local' non defini ici
```

### Portee de fermeture (Closure)

Les fermetures capturent les variables de la portee englobante :

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Capture 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Espaces et formatage

### Indentation

Hemlock n'impose pas d'indentation specifique, mais 4 espaces sont recommandes :

```hemlock
fn example() {
    if (true) {
        print("indente");
    }
}
```

### Sauts de ligne

Les instructions peuvent s'etendre sur plusieurs lignes :

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Instruction Loop

Le mot-cle `loop` fournit une syntaxe plus claire pour les boucles infinies :

```hemlock
loop {
    // ... faire le travail
    if (done) {
        break;
    }
}
```

Ceci est equivalent a `while (true)` mais rend l'intention plus claire.

## Mots-cles reserves

Les mots-cles suivants sont reserves dans Hemlock :

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Prochaines etapes

- [Systeme de types](types.md) - Decouvrez le systeme de types de Hemlock
- [Flux de controle](control-flow.md) - Approfondissez les structures de controle
- [Fonctions](functions.md) - Maitrisez les fonctions et les fermetures
- [Gestion de la memoire](memory.md) - Comprenez les pointeurs et les tampons
