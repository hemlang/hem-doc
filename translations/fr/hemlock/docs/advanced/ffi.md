# Interface de fonctions etrangeres (FFI) dans Hemlock

Hemlock fournit une **FFI (Foreign Function Interface)** pour appeler des fonctions C depuis des bibliotheques partagees en utilisant libffi, permettant l'integration avec des bibliotheques C existantes et des APIs systeme.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Etat actuel](#etat-actuel)
- [Types supportes](#types-supportes)
- [Concepts de base](#concepts-de-base)
- [Exportation de fonctions FFI](#exportation-de-fonctions-ffi)
- [Cas d'utilisation](#cas-dutilisation)
- [Developpement futur](#developpement-futur)
- [Callbacks FFI](#callbacks-ffi)
- [Structures FFI](#structures-ffi)
- [Exportation de types struct](#exportation-de-types-struct)
- [Limitations actuelles](#limitations-actuelles)
- [Bonnes pratiques](#bonnes-pratiques)

## Vue d'ensemble

L'interface de fonctions etrangeres (FFI) permet aux programmes Hemlock de :
- Appeler des fonctions C depuis des bibliotheques partagees (.so, .dylib, .dll)
- Utiliser des bibliotheques C existantes sans ecrire de code wrapper
- Acceder directement aux APIs systeme
- S'integrer avec des bibliotheques natives tierces
- Faire le pont entre Hemlock et les fonctionnalites systeme bas niveau

**Capacites cles :**
- Chargement dynamique de bibliotheques
- Liaison de fonctions C
- Conversion automatique de types entre Hemlock et les types C
- Support de tous les types primitifs
- Implementation basee sur libffi pour la portabilite

## Etat actuel

Le support FFI est disponible dans Hemlock avec les fonctionnalites suivantes :

**Implemente :**
- ✅ Appeler des fonctions C depuis des bibliotheques partagees
- ✅ Support de tous les types primitifs (entiers, flottants, pointeurs)
- ✅ Conversion automatique de types
- ✅ Implementation basee sur libffi
- ✅ Chargement dynamique de bibliotheques
- ✅ **Callbacks avec pointeurs de fonction** - Passer des fonctions Hemlock au C
- ✅ **Exporter des fonctions extern** - Partager des liaisons FFI entre modules
- ✅ **Passage et retour de structures** - Passer des structures compatibles C par valeur
- ✅ **Assistants pointeur complets** - Lecture/ecriture de tous les types (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Conversion buffer/pointeur** - `buffer_ptr()`, `ptr_to_buffer()`
- ✅ **Tailles de types FFI** - `ffi_sizeof()` pour les tailles de types sensibles a la plateforme
- ✅ **Types de plateforme** - Support de `size_t`, `usize`, `isize`, `intptr_t`

**En developpement :**
- 🔄 Assistants de marshaling de chaines
- 🔄 Ameliorations de la gestion des erreurs

**Couverture de tests :**
- Tests FFI passants incluant les tests de callbacks
- Appels de fonctions basiques verifies
- Conversion de types testee
- Integration callback qsort testee

## Types supportes

### Types primitifs

Les types Hemlock suivants peuvent etre passes depuis/vers les fonctions C :

| Type Hemlock | Type C | Taille | Notes |
|--------------|--------|--------|-------|
| `i8` | `int8_t` | 1 octet | Entier signe 8 bits |
| `i16` | `int16_t` | 2 octets | Entier signe 16 bits |
| `i32` | `int32_t` | 4 octets | Entier signe 32 bits |
| `i64` | `int64_t` | 8 octets | Entier signe 64 bits |
| `u8` | `uint8_t` | 1 octet | Entier non signe 8 bits |
| `u16` | `uint16_t` | 2 octets | Entier non signe 16 bits |
| `u32` | `uint32_t` | 4 octets | Entier non signe 32 bits |
| `u64` | `uint64_t` | 8 octets | Entier non signe 64 bits |
| `f32` | `float` | 4 octets | Virgule flottante 32 bits |
| `f64` | `double` | 8 octets | Virgule flottante 64 bits |
| `ptr` | `void*` | 8 octets | Pointeur brut |

### Conversion de types

**Conversions automatiques :**
- Entiers Hemlock → Entiers C (avec verification de plage)
- Flottants Hemlock → Flottants C
- Pointeurs Hemlock → Pointeurs C
- Valeurs de retour C → Valeurs Hemlock

**Exemples de correspondances de types :**
```hemlock
// Hemlock → C
let i: i32 = 42;         // → int32_t (4 octets)
let f: f64 = 3.14;       // → double (8 octets)
let p: ptr = alloc(64);  // → void* (8 octets)

// C → Hemlock (valeurs de retour)
// int32_t foo() → i32
// double bar() → f64
// void* baz() → ptr
```

## Concepts de base

### Bibliotheques partagees

FFI fonctionne avec des bibliotheques partagees compilees :

**Linux :** Fichiers `.so`
```
libexample.so
/usr/lib/libm.so
```

**macOS :** Fichiers `.dylib`
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows :** Fichiers `.dll`
```
example.dll
kernel32.dll
```

### Signatures de fonctions

Les fonctions C doivent avoir des signatures connues pour que FFI fonctionne correctement :

```c
// Exemples de signatures de fonctions C
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

Celles-ci peuvent etre appelees depuis Hemlock une fois que la bibliotheque est chargee et que les fonctions sont liees.

### Compatibilite des plateformes

FFI utilise **libffi** pour la portabilite :
- Fonctionne sur x86, x86-64, ARM, ARM64
- Gere automatiquement les conventions d'appel
- Abstrait les details ABI specifiques a la plateforme
- Supporte Linux, macOS, Windows (avec libffi approprie)

## Exportation de fonctions FFI

Les fonctions FFI declarees avec `extern fn` peuvent etre exportees depuis les modules, vous permettant de creer des wrappers de bibliotheques reutilisables qui peuvent etre partages entre plusieurs fichiers.

### Syntaxe d'exportation de base

```hemlock
// string_utils.hml - Un module de bibliotheque wrappant les fonctions chaine C
import "libc.so.6";

// Exporter la fonction extern directement
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// Vous pouvez aussi exporter des fonctions wrapper a cote des fonctions extern
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### Importation de fonctions FFI exportees

```hemlock
// main.hml - Utilisation des fonctions FFI exportees
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hello, World!";
print(strlen(msg));           // 13 - appel extern direct
print(string_length(msg));    // 13 - fonction wrapper

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### Cas d'utilisation pour export extern

**1. Abstraction de plateforme**
```hemlock
// platform.hml - Abstraire les differences de plateforme
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. Wrappers de bibliotheques**
```hemlock
// crypto_lib.hml - Wrapper de fonctions de bibliotheque crypto
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Ajouter des wrappers conviviaux pour Hemlock
export fn sha256_string(s: string): string {
    // Implementation utilisant la fonction extern
}
```

**3. Declarations FFI centralisees**
```hemlock
// libc.hml - Module central pour les liaisons libc
import "libc.so.6";

// Fonctions chaine
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// Fonctions memoire
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// Fonctions processus
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

Puis utiliser dans tout votre projet :
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

### Combinaison avec les exports reguliers

Vous pouvez melanger les fonctions extern exportees avec les exports de fonctions regulieres :

```hemlock
// math_extended.hml
import "libm.so.6";

// Exporter les fonctions C brutes
export extern fn sin(x: f64): f64;
export extern fn cos(x: f64): f64;
export extern fn tan(x: f64): f64;

// Exporter des fonctions Hemlock qui les utilisent
export fn deg_to_rad(degrees: f64): f64 {
    return degrees * 3.14159265359 / 180.0;
}

export fn sin_degrees(degrees: f64): f64 {
    return sin(deg_to_rad(degrees));
}
```

### Bibliotheques specifiques a la plateforme

Lors de l'exportation de fonctions extern, rappelez-vous que les noms de bibliotheques different selon la plateforme :

```hemlock
// Pour Linux
import "libc.so.6";

// Pour macOS (approche differente necessaire)
import "libSystem.B.dylib";
```

Actuellement, la syntaxe `import "library"` de Hemlock utilise des chemins de bibliotheques statiques, donc des modules specifiques a la plateforme peuvent etre necessaires pour le code FFI multiplateforme.

## Cas d'utilisation

### 1. Bibliotheques systeme

Acces aux fonctions de la bibliotheque C standard :

**Fonctions mathematiques :**
```hemlock
// Appeler sqrt depuis libm
let result = sqrt(16.0);  // 4.0
```

**Allocation memoire :**
```hemlock
// Appeler malloc/free depuis libc
let ptr = malloc(1024);
free(ptr);
```

### 2. Bibliotheques tierces

Utiliser des bibliotheques C existantes :

**Exemple : Traitement d'images**
```hemlock
// Charger libpng ou libjpeg
// Traiter des images en utilisant les fonctions de la bibliotheque C
```

**Exemple : Cryptographie**
```hemlock
// Utiliser OpenSSL ou libsodium
// Chiffrement/dechiffrement via FFI
```

### 3. APIs systeme

Appels systeme directs :

**Exemple : APIs POSIX**
```hemlock
// Appeler getpid, getuid, etc.
// Acces aux fonctionnalites systeme bas niveau
```

### 4. Code critique en performance

Appeler des implementations C optimisees :

```hemlock
// Utiliser des bibliotheques C hautement optimisees
// Operations SIMD, code vectorise
// Fonctions accelerees par le materiel
```

### 5. Acces au materiel

Interface avec les bibliotheques materielles :

```hemlock
// Controle GPIO sur systemes embarques
// Communication avec peripheriques USB
// Acces au port serie
```

### 6. Integration de code legacy

Reutiliser des bases de code C existantes :

```hemlock
// Appeler des fonctions depuis des applications C legacy
// Migrer progressivement vers Hemlock
// Preserver le code C fonctionnel
```

## Developpement futur

### Fonctionnalites prevues

**1. Support des structures**
```hemlock
// Futur : Passer/retourner des structures C
define Point {
    x: f64,
    y: f64,
}

let p = Point { x: 1.0, y: 2.0 };
c_function_with_struct(p);
```

**2. Gestion des tableaux/tampons**
```hemlock
// Futur : Meilleur passage de tableaux
let arr = [1, 2, 3, 4, 5];
process_array(arr);  // Passer a une fonction C
```

**3. Callbacks avec pointeurs de fonction** ✅ (Implemente !)
```hemlock
// Passer des fonctions Hemlock au C comme callbacks
fn my_compare(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    return va - vb;
}

// Creer un pointeur de fonction appelable depuis C
let cmp = callback(my_compare, ["ptr", "ptr"], "i32");

// Utiliser avec qsort ou toute fonction C attendant un callback
qsort(arr, count, elem_size, cmp);

// Nettoyer quand termine
callback_free(cmp);
```

**4. Marshaling de chaines**
```hemlock
// Futur : Conversion automatique de chaines
let s = "hello";
c_string_function(s);  // Auto-conversion en chaine C
```

**5. Gestion des erreurs**
```hemlock
// Futur : Meilleur rapport d'erreurs
try {
    let result = risky_c_function();
} catch (e) {
    print("Erreur FFI : " + e);
}
```

**6. Securite des types**
```hemlock
// Futur : Annotations de types pour FFI
@ffi("libm.so")
fn sqrt(x: f64): f64;

let result = sqrt(16.0);  // Verifie au niveau des types
```

### Fonctionnalites

**v1.0 :**
- ✅ FFI basique avec types primitifs
- ✅ Chargement dynamique de bibliotheques
- ✅ Appels de fonctions
- ✅ Support des callbacks via closures libffi

**Futur :**
- Support des structures
- Ameliorations de la gestion des tableaux
- Generation automatique de liaisons

## Callbacks FFI

Hemlock supporte le passage de fonctions au code C comme callbacks en utilisant les closures libffi. Cela permet l'integration avec les APIs C qui attendent des pointeurs de fonction, comme `qsort`, les boucles d'evenements et les bibliotheques basees sur callbacks.

### Creation de callbacks

Utilisez `callback()` pour creer un pointeur de fonction appelable depuis C a partir d'une fonction Hemlock :

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**Parametres :**
- `function` : Une fonction Hemlock a wrapper
- `param_types` : Tableau de chaines de noms de types (ex. `["ptr", "i32"]`)
- `return_type` : Chaine de type de retour (ex. `"i32"`, `"void"`)

**Types de callback supportes :**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Entiers signes
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Entiers non signes
- `"f32"`, `"f64"` - Virgule flottante
- `"ptr"` - Pointeur
- `"void"` - Pas de valeur de retour
- `"bool"` - Booleen

### Exemple : qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// Fonction de comparaison pour entiers (ordre croissant)
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// Allouer un tableau de 5 entiers
let arr = alloc(20);  // 5 * 4 octets
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// Creer le callback et trier
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// Le tableau est maintenant trie : [1, 2, 5, 8, 9]

// Nettoyer
callback_free(cmp);
free(arr);
```

### Fonctions d'assistance pour pointeurs

Hemlock fournit des fonctions d'assistance completes pour travailler avec les pointeurs bruts. Celles-ci sont essentielles pour les callbacks FFI et la manipulation directe de memoire.

#### Assistants pour types entiers

| Fonction | Description |
|----------|-------------|
| `ptr_deref_i8(ptr)` | Dereferencer pointeur, lire i8 |
| `ptr_deref_i16(ptr)` | Dereferencer pointeur, lire i16 |
| `ptr_deref_i32(ptr)` | Dereferencer pointeur, lire i32 |
| `ptr_deref_i64(ptr)` | Dereferencer pointeur, lire i64 |
| `ptr_deref_u8(ptr)` | Dereferencer pointeur, lire u8 |
| `ptr_deref_u16(ptr)` | Dereferencer pointeur, lire u16 |
| `ptr_deref_u32(ptr)` | Dereferencer pointeur, lire u32 |
| `ptr_deref_u64(ptr)` | Dereferencer pointeur, lire u64 |
| `ptr_write_i8(ptr, value)` | Ecrire i8 a l'emplacement pointeur |
| `ptr_write_i16(ptr, value)` | Ecrire i16 a l'emplacement pointeur |
| `ptr_write_i32(ptr, value)` | Ecrire i32 a l'emplacement pointeur |
| `ptr_write_i64(ptr, value)` | Ecrire i64 a l'emplacement pointeur |
| `ptr_write_u8(ptr, value)` | Ecrire u8 a l'emplacement pointeur |
| `ptr_write_u16(ptr, value)` | Ecrire u16 a l'emplacement pointeur |
| `ptr_write_u32(ptr, value)` | Ecrire u32 a l'emplacement pointeur |
| `ptr_write_u64(ptr, value)` | Ecrire u64 a l'emplacement pointeur |

#### Assistants pour types flottants

| Fonction | Description |
|----------|-------------|
| `ptr_deref_f32(ptr)` | Dereferencer pointeur, lire f32 (float) |
| `ptr_deref_f64(ptr)` | Dereferencer pointeur, lire f64 (double) |
| `ptr_write_f32(ptr, value)` | Ecrire f32 a l'emplacement pointeur |
| `ptr_write_f64(ptr, value)` | Ecrire f64 a l'emplacement pointeur |

#### Assistants pour types pointeur

| Fonction | Description |
|----------|-------------|
| `ptr_deref_ptr(ptr)` | Dereferencer pointeur-vers-pointeur |
| `ptr_write_ptr(ptr, value)` | Ecrire pointeur a l'emplacement pointeur |
| `ptr_offset(ptr, index, size)` | Calculer offset : `ptr + index * size` |
| `ptr_read_i32(ptr)` | Lire i32 a travers pointeur-vers-pointeur (pour callbacks qsort) |
| `ptr_null()` | Obtenir une constante pointeur null |

#### Assistants de conversion de buffer

| Fonction | Description |
|----------|-------------|
| `buffer_ptr(buffer)` | Obtenir le pointeur brut depuis un buffer |
| `ptr_to_buffer(ptr, size)` | Copier les donnees depuis un pointeur dans un nouveau buffer |

#### Fonctions utilitaires FFI

| Fonction | Description |
|----------|-------------|
| `ffi_sizeof(type_name)` | Obtenir la taille en octets d'un type FFI |

**Noms de types supportes pour `ffi_sizeof` :**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Entiers signes (1, 2, 4, 8 octets)
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Entiers non signes (1, 2, 4, 8 octets)
- `"f32"`, `"f64"` - Flottants (4, 8 octets)
- `"ptr"` - Pointeur (8 octets sur 64 bits)
- `"size_t"`, `"usize"` - Type de taille dependant de la plateforme
- `"intptr_t"`, `"isize"` - Type de pointeur signe dependant de la plateforme

#### Exemple : Travailler avec differents types

```hemlock
let p = alloc(64);

// Ecrire et lire des entiers
ptr_write_i8(p, 42);
print(ptr_deref_i8(p));  // 42

ptr_write_i64(ptr_offset(p, 1, 8), 9000000000);
print(ptr_deref_i64(ptr_offset(p, 1, 8)));  // 9000000000

// Ecrire et lire des flottants
ptr_write_f64(p, 3.14159);
print(ptr_deref_f64(p));  // 3.14159

// Pointeur-vers-pointeur
let inner = alloc(4);
ptr_write_i32(inner, 999);
ptr_write_ptr(p, inner);
let retrieved = ptr_deref_ptr(p);
print(ptr_deref_i32(retrieved));  // 999

// Obtenir les tailles de types
print(ffi_sizeof("i64"));  // 8
print(ffi_sizeof("ptr"));  // 8 (sur 64 bits)

// Conversion de buffer
let buf = buffer(64);
ptr_write_i32(buffer_ptr(buf), 12345);
print(ptr_deref_i32(buffer_ptr(buf)));  // 12345

free(inner);
free(p);
```

### Liberation des callbacks

**Important :** Toujours liberer les callbacks quand ils ne sont plus necessaires pour eviter les fuites memoire :

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ... utiliser le callback ...
callback_free(cb);  // Liberer quand termine
```

Les callbacks sont aussi automatiquement liberes quand le programme se termine.

### Closures dans les callbacks

Les callbacks capturent leur environnement de closure, donc ils peuvent acceder aux variables de la portee externe :

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // Peut acceder a 'multiplier' depuis la portee externe
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### Securite des threads

Les invocations de callbacks sont serialisees avec un mutex pour assurer la securite des threads, car l'interpreteur Hemlock n'est pas entierement thread-safe. Cela signifie :
- Un seul callback peut s'executer a la fois
- Sur pour utiliser avec les bibliotheques C multi-threadees
- Peut impacter les performances si les callbacks sont appeles tres frequemment depuis plusieurs threads

### Gestion des erreurs dans les callbacks

Les exceptions lancees dans les callbacks ne peuvent pas se propager au code C. A la place :
- Un avertissement est affiche sur stderr
- Le callback retourne une valeur par defaut (0 ou NULL)
- L'exception est enregistree mais pas propagee

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Quelque chose s'est mal passe";  // Avertissement affiche, retourne 0
}
```

Pour une gestion des erreurs robuste, validez les entrees et evitez de lancer dans les callbacks.

## Structures FFI

Hemlock supporte le passage de structures par valeur aux fonctions C. Les types struct sont automatiquement enregistres pour FFI quand vous les definissez avec des annotations de types.

### Definition de structures compatibles FFI

Une structure est compatible FFI quand tous les champs ont des annotations de types explicites utilisant des types compatibles FFI :

```hemlock
// Structure compatible FFI
define Point {
    x: f64,
    y: f64,
}

// Structure compatible FFI avec plusieurs types de champs
define Rectangle {
    top_left: Point,      // Structure imbriquee
    width: f64,
    height: f64,
}

// NON compatible FFI (champ sans annotation de type)
define DynamicObject {
    name,                 // Pas de type - non utilisable en FFI
    value,
}
```

### Utilisation des structures en FFI

Declarez des fonctions extern qui utilisent des types struct :

```hemlock
// Definir le type struct
define Vector2D {
    x: f64,
    y: f64,
}

// Importer la bibliotheque C
import "libmath.so";

// Declarer une fonction extern qui prend/retourne des structures
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// Utiliser naturellement
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### Types de champs supportes

Les champs de structure doivent utiliser ces types compatibles FFI :

| Type Hemlock | Type C | Taille |
|--------------|--------|--------|
| `i8` | `int8_t` | 1 octet |
| `i16` | `int16_t` | 2 octets |
| `i32` | `int32_t` | 4 octets |
| `i64` | `int64_t` | 8 octets |
| `u8` | `uint8_t` | 1 octet |
| `u16` | `uint16_t` | 2 octets |
| `u32` | `uint32_t` | 4 octets |
| `u64` | `uint64_t` | 8 octets |
| `f32` | `float` | 4 octets |
| `f64` | `double` | 8 octets |
| `ptr` | `void*` | 8 octets |
| `string` | `char*` | 8 octets |
| `bool` | `int` | variable |
| Struct imbriquee | struct | variable |

### Disposition des structures

Hemlock utilise les regles de disposition native de la plateforme (correspondant a l'ABI C) :
- Les champs sont alignes selon leur type
- Du padding est insere si necessaire
- La taille totale est paddee pour aligner le plus grand membre

```hemlock
// Exemple : disposition compatible C
define Mixed {
    a: i8,    // offset 0, taille 1
              // 3 octets de padding
    b: i32,   // offset 4, taille 4
}
// Taille totale : 8 octets (avec padding)

define Point3D {
    x: f64,   // offset 0, taille 8
    y: f64,   // offset 8, taille 8
    z: f64,   // offset 16, taille 8
}
// Taille totale : 24 octets (pas de padding necessaire)
```

### Structures imbriquees

Les structures peuvent contenir d'autres structures :

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### Valeurs de retour struct

Les fonctions C peuvent retourner des structures :

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### Limitations

- **Les champs de structure doivent avoir des annotations de types** - les champs sans types ne sont pas compatibles FFI
- **Pas de tableaux dans les structures** - utilisez des pointeurs a la place
- **Pas d'unions** - seuls les types struct sont supportes
- **Les callbacks ne peuvent pas retourner de structures** - utilisez des pointeurs pour les valeurs de retour des callbacks

### Exportation de types struct

Vous pouvez exporter des definitions de types struct depuis un module en utilisant `export define` :

```hemlock
// geometry.hml
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}

export fn create_rect(x: f32, y: f32, w: f32, h: f32): Rectangle {
    return { x: x, y: y, width: w, height: h };
}
```

**Important :** Les types struct exportes sont enregistres **globalement** quand le module est charge. Ils deviennent automatiquement disponibles quand vous importez quoi que ce soit du module. Vous n'avez PAS besoin de (et ne pouvez pas) les importer explicitement par nom :

```hemlock
// main.hml

// BON - les types struct sont auto-disponibles apres tout import du module
import { create_rect } from "./geometry.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };      // Fonctionne - Vector2 est globalement disponible
let r: Rectangle = create_rect(0.0, 0.0, 100.0, 50.0);  // Fonctionne

// MAUVAIS - impossible d'importer explicitement les types struct par nom
import { Vector2 } from "./geometry.hml";  // Erreur : Variable non definie 'Vector2'
```

Ce comportement existe parce que les types struct sont enregistres dans le registre de types global quand le module charge, plutot que d'etre stockes comme valeurs dans l'environnement d'export du module. Le type devient disponible pour tout le code qui importe depuis le module.

## Limitations actuelles

FFI a les limitations suivantes :

**1. Conversion de types manuelle**
- Doit gerer manuellement les conversions de chaines
- Pas de conversion automatique Hemlock string ↔ C string

**2. Gestion des erreurs limitee**
- Rapport d'erreurs basique
- Les exceptions dans les callbacks ne peuvent pas se propager au C

**3. Chargement manuel de bibliotheques**
- Doit charger manuellement les bibliotheques
- Pas de generation automatique de liaisons

**4. Code specifique a la plateforme**
- Les chemins de bibliotheques different selon la plateforme
- Doit gerer .so vs .dylib vs .dll

## Bonnes pratiques

Bien que la documentation FFI complete soit encore en cours de developpement, voici les bonnes pratiques generales :

### 1. Securite des types

```hemlock
// Etre explicite sur les types
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. Gestion memoire

```hemlock
// Rappelez-vous de liberer la memoire allouee
let ptr = c_malloc(1024);
// ... utiliser ptr
c_free(ptr);
```

### 3. Verification des erreurs

```hemlock
// Verifier les valeurs de retour
let result = c_function();
if (result == null) {
    print("La fonction C a echoue");
}
```

### 4. Compatibilite des plateformes

```hemlock
// Gerer les differences de plateforme
// Utiliser les extensions de bibliotheque appropriees (.so, .dylib, .dll)
```

## Exemples

Pour des exemples fonctionnels, referez-vous a :
- Tests de callbacks : `/tests/ffi_callbacks/` - exemples de callbacks qsort
- Utilisation FFI de la stdlib : `/stdlib/hash.hml`, `/stdlib/regex.hml`, `/stdlib/crypto.hml`
- Programmes d'exemple : `/examples/` (si disponible)

## Obtenir de l'aide

FFI est une fonctionnalite plus recente dans Hemlock. Pour les questions ou problemes :

1. Consultez la suite de tests pour des exemples fonctionnels
2. Referez-vous a la documentation libffi pour les details bas niveau
3. Signalez les bugs ou demandez des fonctionnalites via les issues du projet

## Resume

La FFI de Hemlock fournit :

- ✅ Appels de fonctions C depuis des bibliotheques partagees
- ✅ Support des types primitifs (i8-i64, u8-u64, f32, f64, ptr)
- ✅ Conversion automatique de types
- ✅ Portabilite basee sur libffi
- ✅ Base pour l'integration de bibliotheques natives
- ✅ **Callbacks avec pointeurs de fonction** - passer des fonctions Hemlock au C
- ✅ **Export de fonctions extern** - partager des liaisons FFI entre modules
- ✅ **Passage et retour de structures** - passer des structures compatibles C par valeur
- ✅ **Export define** - partager des definitions de types struct entre modules (auto-importe globalement)
- ✅ **Assistants pointeur complets** - lecture/ecriture de tous les types (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Conversion buffer/pointeur** - `buffer_ptr()`, `ptr_to_buffer()` pour le marshaling de donnees
- ✅ **Tailles de types FFI** - `ffi_sizeof()` pour les tailles de types sensibles a la plateforme
- ✅ **Types de plateforme** - support de `size_t`, `usize`, `isize`, `intptr_t`, `uintptr_t`

**Etat actuel :** FFI completement fonctionnel avec types primitifs, structures, callbacks, exports de modules et fonctions d'assistance pointeur completes

**Futur :** Assistants de marshaling de chaines

**Cas d'utilisation :** Bibliotheques systeme, bibliotheques tierces, qsort, boucles d'evenements, APIs basees sur callbacks, wrappers de bibliotheques reutilisables

## Contribuer

La documentation FFI est en cours d'expansion. Si vous travaillez avec FFI :
- Documentez vos cas d'utilisation
- Partagez du code d'exemple
- Signalez les problemes ou limitations
- Suggerez des ameliorations

Le systeme FFI est concu pour etre pratique et sur tout en fournissant un acces bas niveau quand necessaire, suivant la philosophie de Hemlock "explicite plutot qu'implicite" et "unsafe est une fonctionnalite, pas un bug."
