# Operations atomiques

Hemlock fournit des operations atomiques pour la **programmation concurrente sans verrou**. Ces operations permettent une manipulation securisee de la memoire partagee entre plusieurs threads sans verrous ou mutex traditionnels.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Quand utiliser les atomiques](#quand-utiliser-les-atomiques)
- [Modele memoire](#modele-memoire)
- [Chargement et stockage atomiques](#chargement-et-stockage-atomiques)
- [Operations fetch-and-modify](#operations-fetch-and-modify)
- [Compare-and-Swap (CAS)](#compare-and-swap-cas)
- [Echange atomique](#echange-atomique)
- [Barriere memoire](#barriere-memoire)
- [Reference des fonctions](#reference-des-fonctions)
- [Patterns courants](#patterns-courants)
- [Bonnes pratiques](#bonnes-pratiques)
- [Limitations](#limitations)

---

## Vue d'ensemble

Les operations atomiques sont des operations **indivisibles** qui se terminent sans possibilite d'interruption. Quand un thread effectue une operation atomique, aucun autre thread ne peut observer l'operation dans un etat partiellement termine.

**Caracteristiques cles :**
- Toutes les operations utilisent la **coherence sequentielle** (`memory_order_seq_cst`)
- Types supportes : **i32** et **i64**
- Les operations fonctionnent sur des pointeurs bruts alloues avec `alloc()`
- Thread-safe sans verrous explicites

**Operations disponibles :**
- Load/Store - Lire et ecrire des valeurs de maniere atomique
- Add/Sub - Operations arithmetiques retournant l'ancienne valeur
- And/Or/Xor - Operations bit a bit retournant l'ancienne valeur
- CAS - Compare-and-swap pour les mises a jour conditionnelles
- Exchange - Echanger des valeurs de maniere atomique
- Fence - Barriere memoire complete

---

## Quand utiliser les atomiques

**Utilisez les atomiques pour :**
- Compteurs partages entre taches (ex. comptage de requetes, suivi de progression)
- Drapeaux et indicateurs d'etat
- Structures de donnees sans verrou
- Primitives de synchronisation simples
- Code concurrent critique en performance

**Utilisez les canaux a la place quand :**
- Vous passez des donnees complexes entre taches
- Vous implementez des patterns producteur-consommateur
- Vous avez besoin d'une semantique de passage de messages

**Exemple de cas d'utilisation - Compteur partage :**
```hemlock
// Allouer un compteur partage
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// Lancer plusieurs workers
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// Le compteur sera exactement 3000 (pas de courses de donnees)
print(atomic_load_i32(counter));

free(counter);
```

---

## Modele memoire

Toutes les operations atomiques Hemlock utilisent la **coherence sequentielle** (`memory_order_seq_cst`), qui fournit les garanties d'ordonnancement memoire les plus fortes :

1. **Atomicite** : Chaque operation est indivisible
2. **Ordonnancement total** : Tous les threads voient le meme ordre d'operations
3. **Pas de reordonnancement** : Les operations ne sont pas reordonnees par le compilateur ou le CPU

Cela rend le raisonnement sur le code concurrent plus simple, au prix d'une certaine perte de performance par rapport aux ordonnancements memoire plus faibles.

---

## Chargement et stockage atomiques

### atomic_load_i32 / atomic_load_i64

Lire atomiquement une valeur depuis la memoire.

**Signature :**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**Parametres :**
- `ptr` - Pointeur vers l'emplacement memoire (doit etre correctement aligne)

**Retourne :** La valeur a l'emplacement memoire

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

Ecrire atomiquement une valeur en memoire.

**Signature :**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**Parametres :**
- `ptr` - Pointeur vers l'emplacement memoire
- `value` - Valeur a stocker

**Retourne :** `null`

**Exemple :**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## Operations fetch-and-modify

Ces operations modifient atomiquement une valeur et retournent l'**ancienne** valeur (precedente).

### atomic_add_i32 / atomic_add_i64

Ajouter atomiquement a une valeur.

**Signature :**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**Retourne :** L'**ancienne** valeur (avant addition)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100 (ancienne valeur)
print(atomic_load_i32(p));     // 110 (nouvelle valeur)

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

Soustraire atomiquement d'une valeur.

**Signature :**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**Retourne :** L'**ancienne** valeur (avant soustraction)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100 (ancienne valeur)
print(atomic_load_i32(p));     // 75 (nouvelle valeur)

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

Effectuer atomiquement un ET bit a bit.

**Signature :**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**Retourne :** L'**ancienne** valeur (avant ET)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 255 en binaire : 11111111

let old = atomic_and_i32(p, 0x0F);  // ET avec 00001111
print(old);                    // 255 (ancienne valeur)
print(atomic_load_i32(p));     // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

Effectuer atomiquement un OU bit a bit.

**Signature :**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**Retourne :** L'**ancienne** valeur (avant OU)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 15 en binaire : 00001111

let old = atomic_or_i32(p, 0xF0);  // OU avec 11110000
print(old);                    // 15 (ancienne valeur)
print(atomic_load_i32(p));     // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

Effectuer atomiquement un XOR bit a bit.

**Signature :**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**Retourne :** L'**ancienne** valeur (avant XOR)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 170 en binaire : 10101010

let old = atomic_xor_i32(p, 0xFF);  // XOR avec 11111111
print(old);                    // 170 (ancienne valeur)
print(atomic_load_i32(p));     // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## Compare-and-Swap (CAS)

L'operation atomique la plus puissante. Compare atomiquement la valeur actuelle avec une valeur attendue et, si elles correspondent, la remplace par une nouvelle valeur.

### atomic_cas_i32 / atomic_cas_i64

**Signature :**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**Parametres :**
- `ptr` - Pointeur vers l'emplacement memoire
- `expected` - Valeur qu'on s'attend a trouver
- `desired` - Valeur a stocker si l'attente correspond

**Retourne :**
- `true` - L'echange a reussi (la valeur etait `expected`, maintenant c'est `desired`)
- `false` - L'echange a echoue (la valeur n'etait pas `expected`, inchangee)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS reussit : la valeur est 100, echange vers 999
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS echoue : la valeur est 999, pas 100
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999 (inchange)

free(p);
```

**Cas d'utilisation :**
- Implementation de verrous et semaphores
- Structures de donnees sans verrou
- Controle de concurrence optimiste
- Mises a jour conditionnelles atomiques

---

## Echange atomique

Echanger atomiquement une valeur, retournant l'ancienne valeur.

### atomic_exchange_i32 / atomic_exchange_i64

**Signature :**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**Parametres :**
- `ptr` - Pointeur vers l'emplacement memoire
- `value` - Nouvelle valeur a stocker

**Retourne :** L'**ancienne** valeur (avant echange)

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100 (ancienne valeur)
print(atomic_load_i32(p));     // 200 (nouvelle valeur)

free(p);
```

---

## Barriere memoire

Une barriere memoire complete qui assure que toutes les operations memoire avant la barriere sont visibles par tous les threads avant toute operation apres la barriere.

### atomic_fence

**Signature :**
```hemlock
atomic_fence(): null
```

**Retourne :** `null`

**Exemple :**
```hemlock
// S'assurer que toutes les ecritures precedentes sont visibles
atomic_fence();
```

**Note :** Dans la plupart des cas, vous n'avez pas besoin de barrieres explicites car toutes les operations atomiques utilisent deja la coherence sequentielle. Les barrieres sont utiles quand vous devez synchroniser des operations memoire non atomiques.

---

## Reference des fonctions

### Operations i32

| Fonction | Signature | Retourne | Description |
|----------|-----------|----------|-------------|
| `atomic_load_i32` | `(ptr)` | `i32` | Charger une valeur atomiquement |
| `atomic_store_i32` | `(ptr, value)` | `null` | Stocker une valeur atomiquement |
| `atomic_add_i32` | `(ptr, value)` | `i32` | Ajouter et retourner l'ancienne valeur |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | Soustraire et retourner l'ancienne valeur |
| `atomic_and_i32` | `(ptr, value)` | `i32` | ET bit a bit et retourner l'ancienne valeur |
| `atomic_or_i32` | `(ptr, value)` | `i32` | OU bit a bit et retourner l'ancienne valeur |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | XOR bit a bit et retourner l'ancienne valeur |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | Echanger et retourner l'ancienne valeur |

### Operations i64

| Fonction | Signature | Retourne | Description |
|----------|-----------|----------|-------------|
| `atomic_load_i64` | `(ptr)` | `i64` | Charger une valeur atomiquement |
| `atomic_store_i64` | `(ptr, value)` | `null` | Stocker une valeur atomiquement |
| `atomic_add_i64` | `(ptr, value)` | `i64` | Ajouter et retourner l'ancienne valeur |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | Soustraire et retourner l'ancienne valeur |
| `atomic_and_i64` | `(ptr, value)` | `i64` | ET bit a bit et retourner l'ancienne valeur |
| `atomic_or_i64` | `(ptr, value)` | `i64` | OU bit a bit et retourner l'ancienne valeur |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | XOR bit a bit et retourner l'ancienne valeur |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | Echanger et retourner l'ancienne valeur |

### Barriere memoire

| Fonction | Signature | Retourne | Description |
|----------|-----------|----------|-------------|
| `atomic_fence` | `()` | `null` | Barriere memoire complete |

---

## Patterns courants

### Pattern : Compteur atomique

```hemlock
// Compteur thread-safe
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// Utilisation
increment();  // Retourne 0 (ancienne valeur)
increment();  // Retourne 1
increment();  // Retourne 2
print(get_count());  // 3

free(counter);
```

### Pattern : Spinlock

```hemlock
// Implementation simple de spinlock
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = deverrouille, 1 = verrouille

fn acquire() {
    // Tourner jusqu'a ce qu'on reussisse a mettre le verrou de 0 a 1
    while (!atomic_cas_i32(lock, 0, 1)) {
        // Attente active
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// Utilisation
acquire();
// ... section critique ...
release();

free(lock);
```

### Pattern : Initialisation unique

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = non initialise, 1 = initialise

fn ensure_initialized() {
    // Essayer d'etre celui qui initialise
    if (atomic_cas_i32(initialized, 0, 1)) {
        // On a gagne la course, faire l'initialisation
        do_expensive_init();
    }
    // Sinon, deja initialise
}
```

### Pattern : Drapeau atomique

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // Retourne true si le drapeau etait deja mis
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### Pattern : Compteur borne

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // Au maximum
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // Incremente avec succes
        }
        // CAS echoue, un autre thread a modifie - reessayer
    }
}
```

---

## Bonnes pratiques

### 1. Utiliser un alignement correct

Les pointeurs doivent etre correctement alignes pour le type de donnees :
- i32 : alignement sur 4 octets
- i64 : alignement sur 8 octets

La memoire de `alloc()` est typiquement correctement alignee.

### 2. Preferer les abstractions de plus haut niveau

Quand c'est possible, utilisez les canaux pour la communication inter-taches. Les atomiques sont de plus bas niveau et necessitent un raisonnement attentif.

```hemlock
// Preferez ceci :
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// Plutot que la coordination atomique manuelle quand c'est approprie
```

### 3. Etre conscient du probleme ABA

Le CAS peut souffrir du probleme ABA : une valeur change de A vers B puis revient a A. Votre CAS reussit, mais l'etat peut avoir change entre temps.

### 4. Initialiser avant de partager

Toujours initialiser les variables atomiques avant de lancer des taches qui y accedent :

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // Initialiser AVANT de lancer

let task = spawn(worker, counter);
```

### 5. Liberer apres que toutes les taches sont terminees

Ne liberez pas la memoire atomique tant que des taches peuvent encore y acceder :

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// Maintenant c'est sur de liberer
free(counter);
```

---

## Limitations

### Limitations actuelles

1. **Seuls i32 et i64 supportes** - Pas d'operations atomiques pour d'autres types
2. **Pas d'atomiques de pointeurs** - Impossible de charger/stocker des pointeurs atomiquement
3. **Coherence sequentielle uniquement** - Pas d'ordonnancements memoire plus faibles disponibles
4. **Pas de virgule flottante atomique** - Utilisez une representation entiere si necessaire

### Notes de plateforme

- Les operations atomiques utilisent `<stdatomic.h>` du C11 en interne
- Disponible sur toutes les plateformes qui supportent les threads POSIX
- Garanti sans verrou sur les systemes 64 bits modernes

---

## Voir aussi

- [Async/Concurrence](async-concurrency.md) - Lancement de taches et canaux
- [Gestion memoire](../language-guide/memory.md) - Allocation de pointeurs et tampons
- [API memoire](../reference/memory-api.md) - Fonctions d'allocation
