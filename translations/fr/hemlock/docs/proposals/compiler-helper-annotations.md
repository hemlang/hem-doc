# Annotations d'aide au compilateur : Analyse et proposition

**Auteur :** Claude
**Date :** 2026-01-08
**Statut :** Partiellement implemente (Phases 1-2 terminees dans v1.9.0 ; Phases 3-5 restent des propositions)
**Associe :** Issue #TBD

## Table des matieres

1. [Resume executif](#resume-executif)
2. [Analyse de l'etat actuel](#analyse-de-letat-actuel)
3. [Annotations proposees](#annotations-proposees)
4. [Plan d'implementation](#plan-dimplementation)
5. [Exemples](#exemples)
6. [Strategie de test](#strategie-de-test)
7. [Considerations futures](#considerations-futures)

---

## Resume executif

Le systeme d'annotations de Hemlock fournit une base robuste pour ajouter des indications et directives au compilateur. Cette proposition etend l'infrastructure d'annotations actuelle avec **15 nouvelles annotations d'aide au compilateur** organisees en cinq categories :

- **Indications d'optimisation** (7 annotations)
- **Gestion de la memoire** (3 annotations)
- **Controle de la generation de code** (2 annotations)
- **Verification d'erreurs** (2 annotations)
- **FFI/Interop** (1 annotation)

Ces annotations permettront aux developpeurs de fournir des directives explicites au compilateur (`hemlockc`) tout en maintenant la retrocompatibilite avec l'interpreteur.

---

## Analyse de l'etat actuel

### 1. Infrastructure d'annotations

Le systeme d'annotations est entierement implemente avec trois composants principaux :

**Parseur** (`src/frontend/parser/statements.c`) :
- Parse la syntaxe `@name` et `@name(args...)`
- Supporte les arguments positionnels et nommes
- Attache les annotations aux declarations (let, const, define, enum)

**Validateur** (`src/frontend/annotations.c`) :
- Valide les cibles d'annotation (fonction, type, variable, etc.)
- Verifie les comptes et types d'arguments
- Avertit sur les annotations inconnues ou dupliquees

**Resolveur** (`src/frontend/resolver.c`) :
- Stocke les annotations aux cotes des definitions de variables
- Permet la recherche d'annotations pendant l'analyse semantique
- Alimente les avertissements `@deprecated` a l'utilisation des variables

### 2. Annotations actuellement implementees

```c
// Annotations de securite (pour le verificateur memoire Tricycle)
@safe       // La fonction est securisee en memoire
@unsafe     // La fonction contient des operations non securisees
@trusted    // La fonction est de confiance malgre les operations non securisees

// Indications d'optimisation du compilateur (IMPLEMENTEES dans v1.9.0)
@inline     // Suggerer l'inlining de cette fonction
@noinline   // Empecher l'inlining de cette fonction
@cold       // La fonction est rarement executee
@hot        // La fonction est frequemment executee
@pure       // La fonction n'a pas d'effets de bord

// Autres annotations
@deprecated      // Marquer comme obsolete avec message optionnel
@test, @skip     // Annotations du framework de test
@author, @since  // Annotations de documentation
```

### 3. Limitations actuelles

**Mise a jour (v1.9.0) :** Les annotations de base au niveau fonction (`@inline`, `@noinline`, `@hot`, `@cold`, `@pure`, `@const`, `@flatten`, `@optimize`, `@warn_unused`, `@section`) sont maintenant entierement implementees dans le backend du compilateur. Les propositions restantes (annotations de boucle, annotations memoire) dans les Phases 3-5 ci-dessous sont toujours non implementees.

---

## Annotations proposees

### Categorie 1 : Indications d'optimisation

#### `@unroll(count?: number)`
**Cible :** Boucles (for, while)
**Arguments :** Facteur de deroulement optionnel (defaut : le compilateur decide)

Suggere le deroulement de boucle pour les boucles critiques en performance.

```hemlock
@unroll(4)
for (let i = 0; i < 1024; i++) {
    buffer[i] = buffer[i] * 2;
}
```

**Codegen compilateur :**
```c
// Genere : #pragma GCC unroll 4
// Ou : #pragma clang loop unroll_count(4)
```

---

#### `@simd` / `@nosimd`
**Cible :** Fonctions, boucles
**Arguments :** Aucun

Active ou desactive la vectorisation SIMD.

```hemlock
@simd
fn vector_add(a: buffer, b: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        ptr_write_f64(a, i, ptr_read_f64(a, i) + ptr_read_f64(b, i));
    }
}
```

**Codegen compilateur :**
```c
// Niveau fonction : __attribute__((target("avx2")))
// Niveau boucle : #pragma omp simd
```

---

#### `@likely` / `@unlikely`
**Cible :** Instructions if, conditionnels
**Arguments :** Aucun

Indications de prediction de branche pour les chemins critiques.

```hemlock
@likely
if (cache.has(key)) {
    return cache.get(key);
}

@unlikely
if (error) {
    handle_error(error);
}
```

**Codegen compilateur :**
```c
if (__builtin_expect(!!(condition), 1))  // @likely
if (__builtin_expect(!!(condition), 0))  // @unlikely
```

---

#### `@const`
**Cible :** Fonctions
**Arguments :** Aucun

La fonction retourne toujours le meme resultat pour les memes entrees (plus fort que `@pure`).

```hemlock
@const
fn square(x: i32): i32 => x * x;

@const
fn add(a: i32, b: i32): i32 => a + b;
```

**Codegen compilateur :**
```c
__attribute__((const))
```

**Difference avec `@pure` :**
- `@pure` : Peut lire la memoire globale, mais ne la modifie pas
- `@const` : Ne peut meme pas lire la memoire globale, utilise uniquement les parametres

---

#### `@tail_call`
**Cible :** Appels de fonction
**Arguments :** Aucun

Demande l'optimisation des appels terminaux (TCO).

```hemlock
fn factorial_helper(n: i32, acc: i32): i32 {
    if (n <= 1) { return acc; }
    @tail_call
    return factorial_helper(n - 1, n * acc);
}
```

**Codegen compilateur :**
```c
// Generer une boucle tail-recursive au lieu d'un appel recursif
// Ou utiliser : __attribute__((musttail)) sur Clang
```

---

#### `@flatten`
**Cible :** Fonctions
**Arguments :** Aucun

Integrer tous les appels dans cette fonction.

```hemlock
@flatten
fn compute_hash(data: buffer, len: i32): u64 {
    let hash = init_hash();
    hash = process_block(hash, data, len);
    return finalize_hash(hash);
}
```

**Codegen compilateur :**
```c
__attribute__((flatten))
```

---

#### `@optimize(level: string)`
**Cible :** Fonctions
**Arguments :** Niveau d'optimisation ("0", "1", "2", "3", "s", "fast")

Remplacer le niveau d'optimisation global pour une fonction specifique.

```hemlock
@optimize("3")
fn matrix_multiply(a: buffer, b: buffer, n: i32) {
    // Boucle interne critique en performance
}

@optimize("s")
fn rarely_called_error_handler() {
    // Optimiser pour la taille, pas la vitesse
}
```

**Codegen compilateur :**
```c
__attribute__((optimize("O3")))
__attribute__((optimize("Os")))
```

---

### Categorie 2 : Gestion de la memoire

#### `@stack`
**Cible :** Variables (tableaux, buffers)
**Arguments :** Aucun

Allouer sur la pile au lieu du tas (quand possible).

```hemlock
@stack
let temp_buffer = buffer(1024);  // Allocation sur la pile

fn process_small_data() {
    @stack
    let workspace: array<i32> = [0, 0, 0, 0];  // Tableau sur la pile
}
```

---

#### `@noalias`
**Cible :** Parametres de fonction (pointeurs/buffers)
**Arguments :** Aucun

Promettre que le pointeur n'a pas d'alias avec d'autres pointeurs.

```hemlock
fn memcpy_fast(@noalias dest: ptr, @noalias src: ptr, n: i32) {
    // Le compilateur sait que dest et src ne se chevauchent pas
    memcpy(dest, src, n);
}
```

---

#### `@aligned(bytes: number)`
**Cible :** Variables (pointeurs, buffers), retours de fonctions
**Arguments :** Alignement en octets (doit etre une puissance de 2)

Specifier les exigences d'alignement memoire.

```hemlock
@aligned(64)  // Aligne sur la ligne de cache
let cache_line_buffer = buffer(64);
```

---

### Categorie 3 : Controle de la generation de code

#### `@extern(name?: string, abi?: string)`
**Cible :** Fonctions
**Arguments :**
- `name` : Nom du symbole externe (defaut : nom de la fonction)
- `abi` : Convention d'appel ("C", "stdcall", "fastcall")

Marquer la fonction pour la liaison externe ou l'export FFI.

```hemlock
@extern
fn hemlock_init() {
    print("Library initialized");
}

@extern("_ZN3foo3barEv")
fn mangled_cpp_function() { }
```

---

#### `@section(name: string)`
**Cible :** Fonctions, variables globales
**Arguments :** Nom de section

Placer le symbole dans une section ELF/Mach-O specifique.

```hemlock
@section(".text.hot")
@hot
fn critical_path() { }
```

---

### Categorie 4 : Verification d'erreurs

#### `@bounds_check` / `@no_bounds_check`
**Cible :** Operations tableau/buffer, boucles
**Arguments :** Aucun

Remplacer la politique globale de verification des limites.

```hemlock
@bounds_check
fn safe_array_access(arr: array, idx: i32) {
    return arr[idx];
}

@no_bounds_check
fn trusted_hot_loop(data: buffer, n: i32) {
    for (let i = 0; i < n; i++) {
        data[i] = 0;
    }
}
```

---

#### `@warn_unused`
**Cible :** Valeurs de retour de fonction
**Arguments :** Aucun

Avertir si l'appelant ignore la valeur de retour.

```hemlock
@warn_unused
fn allocate_memory(size: i32): ptr {
    return alloc(size);
}

let p = allocate_memory(1024);  // OK
allocate_memory(1024);          // Avertissement : valeur de retour inutilisee
```

---

### Categorie 5 : FFI/Interop

#### `@packed`
**Cible :** Definitions de type (define)
**Arguments :** Aucun

Creer une structure compacte sans remplissage (pour l'interoperabilite C).

```hemlock
@packed
define NetworkHeader {
    magic: u32,
    version: u8,
    flags: u8,
    length: u16
}  // Total : 8 octets, pas de remplissage
```

---

## Plan d'implementation

### Phase 1 : Infrastructure de base (Semaine 1)

**Objectif :** Permettre au compilateur d'interroger et utiliser les annotations

### Phase 2 : Annotations de fonction (Semaine 2)

**Objectif :** Implementer les indications d'optimisation au niveau fonction

### Phase 3 : Annotations de boucle (Semaine 3)

**Objectif :** Supporter les indications au niveau boucle (@unroll, @simd, @likely/@unlikely)

### Phase 4 : Annotations memoire (Semaine 4)

**Objectif :** Implementer @stack, @noalias, @aligned

### Phase 5 : Tests et documentation (Semaine 5)

**Objectif :** Couverture de test complete et documentation

---

## Exemples

### Exemple 1 : Mathematiques vectorielles haute performance

```hemlock
@simd
@flatten
fn vector_add(a: buffer, b: buffer, result: buffer, n: i32) {
    @unroll(8)
    for (let i = 0; i < n; i++) {
        let av = ptr_read_f64(a, i * 8);
        let bv = ptr_read_f64(b, i * 8);
        ptr_write_f64(result, i * 8, av + bv);
    }
}
```

### Exemple 2 : Structure de donnees optimisee pour le cache

```hemlock
@packed
define CacheLineNode {
    next: ptr,
    data: i64,
    timestamp: u64,
    flags: u32,
    padding: u32
}

@hot
@inline
fn cache_lookup(@aligned(64) cache: ptr, key: u64): ptr {
    @likely
    if (cache == null) {
        return null;
    }

    let node = ptr_read_ptr(cache);
    @unroll(4)
    while (node != null) {
        let node_key = ptr_read_u64(node, 8);
        if (node_key == key) {
            return node;
        }
        node = ptr_read_ptr(node);
    }

    return null;
}
```

### Exemple 3 : Optimisation des appels terminaux recursifs

```hemlock
@tail_call
fn sum_range(start: i32, end: i32, acc: i32): i32 {
    if (start > end) {
        return acc;
    }
    @tail_call
    return sum_range(start + 1, end, acc + start);
}
```

---

## Strategie de test

### 1. Tests de validation (`tests/annotations/validation_*.hml`)

Tester que les nouvelles annotations sont validees correctement.

### 2. Tests de parite (`tests/parity/annotations/`)

S'assurer que les annotations ne changent pas le comportement du programme.

### 3. Tests specifiques au compilateur (`tests/compiler/annotations/`)

Verifier que le code C genere contient les attributs/pragmas corrects.

### 4. Benchmarks de performance (`benchmarks/annotations/`)

Mesurer les ameliorations de performance reelles.

---

## Considerations futures

### 1. Heritage des annotations

Les annotations sur les types doivent-elles s'appliquer a toutes les instances ?

**Recommandation :** Oui pour @aligned, @packed. Non pour @deprecated, @inline.

### 2. Composition d'annotations

Permettre de creer des annotations personnalisees a partir d'autres ?

**Recommandation :** Reporter. Garder la version actuelle concentree sur les annotations de base.

### 3. Integration des flags du compilateur

Les annotations doivent-elles remplacer les flags du compilateur ?

**Recommandation :** Les annotations gagnent. L'intention explicite du developpeur doit etre respectee.

---

## Conclusion

Cette proposition ajoute **15 nouvelles annotations d'aide au compilateur** a Hemlock, permettant aux developpeurs de fournir des indications d'optimisation explicites tout en maintenant la philosophie "explicite plutot qu'implicite" du langage.

**Avantages cles :**

1. **Performance :** Accelerations de 2 a 10x pour les chemins critiques avec SIMD, deroulement, inlining
2. **Controle :** Les developpeurs peuvent remplacer les heuristiques par defaut du compilateur
3. **Interoperabilite :** Meilleur support FFI avec @extern, @packed, @aligned
4. **Securite :** Les @bounds_check/@no_bounds_check explicites rendent les compromis de securite visibles
5. **Explicite :** S'inscrit dans la philosophie de Hemlock -- pas de magie, juste des directives claires

**Effort d'implementation :**

- Phase 1-2 : ~2 semaines (infrastructure de base + annotations de fonction)
- Phase 3 : ~1 semaine (annotations de boucle)
- Phase 4 : ~1 semaine (annotations memoire)
- Phase 5 : ~1 semaine (tests et documentation)

**Total : ~5 semaines pour l'implementation complete**

---

## Annexe : Tableau de reference complet des annotations

| Annotation | Cible | Args | Description | Attribut C |
|------------|-------|------|-------------|------------|
| `@inline` | fn | 0 | Forcer l'inlining | `always_inline` |
| `@noinline` | fn | 0 | Empecher l'inlining | `noinline` |
| `@cold` | fn | 0 | Rarement execute | `cold` |
| `@hot` | fn | 0 | Frequemment execute | `hot` |
| `@pure` | fn | 0 | Pas d'effets de bord, peut lire les globaux | `pure` |
| `@const` | fn | 0 | Pas d'effets de bord, pas de lecture de globaux | `const` |
| `@flatten` | fn | 0 | Integrer tous les appels dans la fonction | `flatten` |
| `@tail_call` | fn | 0 | Demander l'optimisation des appels terminaux | Personnalise |
| `@optimize(level)` | fn | 1 | Remplacer le niveau d'optimisation | `optimize("OX")` |
| `@unroll(factor?)` | boucle | 0-1 | Indication de deroulement de boucle | `#pragma unroll` |
| `@simd` | fn, boucle | 0 | Activer la vectorisation SIMD | `#pragma omp simd` |
| `@nosimd` | fn, boucle | 0 | Desactiver SIMD | Personnalise |
| `@likely` | if | 0 | Branche probablement prise | `__builtin_expect` |
| `@unlikely` | if | 0 | Branche probablement non prise | `__builtin_expect` |
| `@stack` | let | 0 | Allocation sur la pile | Personnalise |
| `@noalias` | param | 0 | Pas d'aliasing de pointeur | `noalias` |
| `@aligned(N)` | let, fn | 1 | Alignement memoire | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | Liaison externe | `extern "C"` |
| `@section(name)` | fn, let | 1 | Placer dans une section specifique | `section("X")` |
| `@bounds_check` | fn | 0 | Forcer la verification des limites | Personnalise |
| `@no_bounds_check` | fn | 0 | Desactiver la verification des limites | Personnalise |
| `@warn_unused` | fn | 0 | Avertir sur retour inutilise | `warn_unused_result` |
| `@packed` | define | 0 | Pas de remplissage de structure | `packed` |

**Annotations existantes (non couvertes dans cette proposition) :**
- `@safe`, `@unsafe`, `@trusted` (pour Tricycle)
- `@deprecated` (deja implemente)
- `@test`, `@skip`, `@timeout` (framework de test)
- `@author`, `@since`, `@see` (documentation)
