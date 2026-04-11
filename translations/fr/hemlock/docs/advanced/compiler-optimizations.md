# Optimisations du compilateur

Le compilateur Hemlock (`hemlockc`) applique plusieurs passes d'optimisation lors de la generation de code C. Ces optimisations sont automatiques et ne necessitent aucune intervention de l'utilisateur, mais les comprendre aide a expliquer les caracteristiques de performance.

---

## Vue d'ensemble

```
Source (.hml)
    ↓
  Parse → AST
    ↓
  Verification de type (optionnelle)
    ↓
  Passe d'optimisation AST
    ↓
  Generation de code C (avec inlining + unboxing)
    ↓
  Compilation GCC/Clang
```

---

## Unboxing au niveau des expressions

Le runtime de Hemlock represente toutes les valeurs sous forme de structures `HmlValue` etiquetees. Dans l'interpreteur, chaque operation arithmetique encapsule et desencapsule les valeurs via un dispatch a l'execution. Le compilateur elimine cette surcharge pour les expressions dont les types primitifs sont connus.

**Avant (codegen naif) :**
```c
// x + 1 ou x est i32
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 appels d'encapsulation + dispatch a l'execution
```

**Apres (avec unboxing d'expression) :**
```c
// x + 1 ou x est i32
hml_val_i32((x + 1))  // Arithmetique C pure, encapsulation unique a la fin
```

### Ce qui est desencapsule

- Arithmetique binaire : `+`, `-`, `*`, `%`
- Operations bit a bit : `&`, `|`, `^`, `<<`, `>>`
- Comparaisons : `<`, `>`, `<=`, `>=`, `==`, `!=`
- Operations unaires : `-`, `~`, `!`
- Variables annotees par type et compteurs de boucle

### Ce qui retombe sur HmlValue

- Appels de fonction (le type de retour peut etre dynamique)
- Acces tableau/objet (type d'element inconnu a la compilation)
- Variables sans annotations de type et sans type infere

### Conseil

Ajouter des annotations de type aux variables du chemin critique aide le compilateur a appliquer l'unboxing :

```hemlock
// Le compilateur peut desencapsuler toute cette expression
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## Inlining de fonctions multi-niveaux

Le compilateur integre les petites fonctions aux sites d'appel, remplacant la surcharge d'appel de fonction par du code direct. Hemlock supporte l'inlining multi-niveaux jusqu'a une profondeur de 3, ce qui signifie que les appels de fonctions utilitaires imbriquees sont egalement integres.

### Fonctionnement

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // ep0 ET rotr sont integres ici
    // ...
}
```

A la profondeur 1, `ep0()` est integree dans `sha256_round()`. A la profondeur 2, les appels `rotr()` a l'interieur de `ep0()` sont egalement integres. Le resultat est un bloc unique d'arithmetique native sans surcharge d'appel de fonction.

### Criteres d'inlining

Les fonctions sont integrees quand :
- Le corps de la fonction est petit (expression unique ou quelques instructions)
- La fonction n'est pas recursive
- La profondeur d'inlining actuelle est inferieure a 3

### Controler l'inlining avec des annotations

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // Fonction complexe qui ne doit pas etre dupliquee
    return x;
}
```

---

## Unboxing des accumulateurs de boucle while

Pour les boucles while de niveau superieur, le compilateur detecte les variables compteur et accumulateur et les remplace par des variables locales C natives, eliminant la surcharge d'encapsulation/desencapsulation a chaque iteration.

### Ce qui est optimise

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

Le compilateur detecte que `sum` et `i` sont des accumulateurs entiers utilises uniquement dans la boucle, et genere des variables locales `int32_t` natives au lieu d'operations `HmlValue`. Cela elimine la surcharge de retain/release et le dispatch de type a chaque iteration.

### Impact sur les performances

Ameliorations de benchmark grace a ces optimisations (mesurees sur des charges de travail typiques) :

| Benchmark | Avant | Apres | Amelioration |
|-----------|-------|-------|--------------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## Annotations d'aide

Le compilateur supporte 10 annotations d'optimisation qui correspondent a des attributs GCC/Clang :

| Annotation | Effet |
|------------|-------|
| `@inline` | Encourager l'inlining de fonction |
| `@noinline` | Empecher l'inlining de fonction |
| `@hot` | Marquer comme frequemment execute (prediction de branche) |
| `@cold` | Marquer comme rarement execute |
| `@pure` | La fonction n'a pas d'effets de bord (lit l'etat externe) |
| `@const` | La fonction ne depend que de ses arguments (pas d'etat externe) |
| `@flatten` | Integrer tous les appels dans la fonction |
| `@optimize(level)` | Niveau d'optimisation par fonction ("0"-"3", "s", "fast") |
| `@warn_unused` | Avertir si la valeur de retour est ignoree |
| `@section(name)` | Placer la fonction dans une section ELF personnalisee |

### Exemple

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // Fonction de hachage du chemin critique
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## Pools d'allocation

Le runtime utilise des pools d'objets pre-alloues pour eviter la surcharge `malloc`/`free` pour les objets a courte duree de vie frequemment crees :

| Pool | Emplacements | Description |
|------|-------------|-------------|
| Pool d'environnements | 1024 | Environnements de portee closure/fonction (jusqu'a 16 variables chacun) |
| Pool d'objets | 512 | Objets anonymes avec jusqu'a 8 champs |
| Pool de fonctions | 512 | Structures de closure pour les fonctions capturees |

Les pools utilisent des piles de listes libres pour une allocation et desallocation O(1). Quand un pool est epuise, le runtime retombe sur `malloc`. Les objets qui depassent leur emplacement de pool (par ex., un objet gagnant un 9e champ) sont migres de maniere transparente vers le stockage sur le tas.

### Parametres empruntes a l'AST

Les closures empruntent les metadonnees de parametres directement a l'AST au lieu de les copier en profondeur, eliminant environ 6 appels `malloc` + N appels `strdup` par creation de closure. Les hachages des noms de parametres sont calcules paresseusement et mis en cache sur le noeud AST.

---

## Verification de type

Le compilateur inclut la verification de type a la compilation (activee par defaut) :

```bash
hemlockc program.hml -o program       # Verification de type + compilation
hemlockc --check program.hml          # Verification de type uniquement
hemlockc --no-type-check program.hml  # Ignorer la verification de type
hemlockc --strict-types program.hml   # Avertir sur les types 'any' implicites
```

Le code non type est traite comme dynamique (type `any`) et passe toujours la verification de type. Les annotations de type fournissent des indications d'optimisation qui permettent l'unboxing.

---

## Voir aussi

- [Proposition d'annotations d'aide](../proposals/compiler-helper-annotations.md) - Reference detaillee des annotations
- [API Memory](../reference/memory-api.md) - Operations sur les buffers et pointeurs
- [Fonctions](../language-guide/functions.md) - Annotations de type et fonctions a corps d'expression
