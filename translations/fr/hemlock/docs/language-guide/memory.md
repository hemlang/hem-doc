# Gestion de la memoire

Hemlock adopte la **gestion manuelle de la memoire** avec un controle explicite sur l'allocation et la desallocation. Ce guide couvre le modele memoire de Hemlock, les deux types de pointeur et l'API memoire complete.

---

## Memoire 101 : Les bases

**Nouveau en programmation ?** Commencez ici. Si vous comprenez deja la gestion de la memoire, passez a [Philosophie](#philosophie).

### Qu'est-ce que la gestion de la memoire ?

Quand votre programme a besoin de stocker des donnees (texte, nombres, listes), il a besoin d'espace pour les placer. Cet espace vient de la memoire de votre ordinateur (RAM). La gestion de la memoire concerne :

1. **Obtenir de l'espace** - demander de la memoire quand vous en avez besoin
2. **Utiliser l'espace** - lire et ecrire vos donnees
3. **Le rendre** - retourner la memoire quand vous avez fini

### Pourquoi est-ce important ?

Imaginez une bibliotheque avec des livres limites :
- Si vous continuez a emprunter des livres et ne les rendez jamais, il n'y en a plus
- Si vous essayez de lire un livre que vous avez deja rendu, vous serez confus ou causerez des problemes

La memoire fonctionne de la meme facon. Si vous oubliez de retourner la memoire, votre programme utilise de plus en plus (une "fuite memoire"). Si vous essayez d'utiliser la memoire apres l'avoir rendue, de mauvaises choses arrivent.

### La bonne nouvelle

**La plupart du temps, vous n'avez pas besoin d'y penser !**

Hemlock nettoie automatiquement la plupart des types courants :

```hemlock
fn example() {
    let name = "Alice";       // Hemlock gere ceci
    let numbers = [1, 2, 3];  // Et ceci
    let person = { age: 30 }; // Et cela aussi

    // Quand la fonction se termine, tout ceci est nettoye automatiquement !
}
```

### Quand vous DEVEZ y penser

Vous avez besoin de gestion manuelle de la memoire uniquement quand vous utilisez :

1. **`alloc()`** - allocation de memoire brute (retourne `ptr`)
2. **`buffer()`** - quand vous voulez liberer tot (optionnel - il s'auto-libere a la fin de portee)

```hemlock
// Ceci necessite un nettoyage manuel :
let raw = alloc(100);   // Memoire brute - VOUS devez la liberer
// ... utiliser raw ...
free(raw);              // Requis ! Sinon vous avez une fuite memoire

// Ceci se nettoie automatiquement (mais vous POUVEZ liberer tot) :
let buf = buffer(100);  // Buffer securise
// ... utiliser buf ...
// free(buf);           // Optionnel - s'auto-libere quand la portee se termine
```

### La regle simple

> **Si vous appelez `alloc()`, vous devez appeler `free()`.**
>
> Tout le reste est gere pour vous.

### Lequel utiliser ?

| Situation | Utilisez | Pourquoi |
|-----------|----------|----------|
| **Debutant** | `buffer()` | Securise, verifie les limites, auto-nettoyage |
| **Besoin de stockage d'octets** | `buffer()` | Securise et facile |
| **Travailler avec des bibliotheques C (FFI)** | `alloc()` / `ptr` | Requis pour l'interop C |
| **Performance maximale** | `alloc()` / `ptr` | Pas de surcharge de verification des limites |
| **Pas sur** | `buffer()` | Toujours le choix plus sur |

### Exemple rapide : Securise vs Brut

```hemlock
// RECOMMANDE : Buffer securise
fn safe_example() {
    let data = buffer(10);
    data[0] = 65;           // OK
    data[5] = 66;           // OK
    // data[100] = 67;      // ERREUR - Hemlock vous arrete (verification des limites)
    free(data);             // Nettoyage
}

// AVANCE : Pointeur brut (seulement quand necessaire)
fn raw_example() {
    let data = alloc(10);
    *data = 65;             // OK
    *(data + 5) = 66;       // OK
    *(data + 100) = 67;     // DANGER - Pas de verification des limites, corrompt la memoire !
    free(data);             // Nettoyage
}
```

**Commencez avec `buffer()`. Utilisez `alloc()` seulement quand vous avez specifiquement besoin de pointeurs bruts.**

---

## Philosophie

Hemlock suit le principe de gestion explicite de la memoire avec des valeurs par defaut sensees :
- Pas de garbage collection (pas de pauses imprevisibles)
- Comptage de reference interne pour les types courants (string, array, object, buffer)
- Les pointeurs bruts (`ptr`) necessitent un `free()` manuel

Cette approche hybride vous donne un controle complet quand necessaire (pointeurs bruts) tout en evitant les bugs courants pour les cas d'utilisation typiques (types comptes par reference auto-liberes a la sortie de portee).

## Comptage de reference interne

Le runtime utilise le **comptage de reference interne** pour gerer les durees de vie des objets. Pour la plupart des variables locales de types comptes par reference, le nettoyage est automatique et deterministe.

### Ce que gere le comptage de reference

Le runtime gere automatiquement les comptes de reference quand :

1. **Les variables sont reassignees** - l'ancienne valeur est liberee :
   ```hemlock
   let x = "first";   // ref_count = 1
   x = "second";      // "first" libere en interne, "second" ref_count = 1
   ```

2. **Les portees se terminent** - les variables locales sont liberees :
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // arr libere quand la fonction retourne
   ```

3. **Les conteneurs sont liberes** - les elements sont liberes :
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // obj1 et obj2 voient leur ref_count decremente
   ```

### Quand vous avez besoin de `free()` vs quand c'est automatique

**Automatique (pas de `free()` necessaire) :** Les variables locales de types comptes par reference sont liberees quand la portee se termine :

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... les utiliser ...
}  // Tout automatiquement libere quand la fonction retourne - pas de free() necessaire
```

**`free()` manuel requis :**

1. **Pointeurs bruts** - `alloc()` n'a pas de comptage de reference :
   ```hemlock
   let p = alloc(64);
   // ... utiliser p ...
   free(p);  // Toujours requis - fuira sinon
   ```

2. **Nettoyage anticipe** - liberer avant la fin de portee pour liberer la memoire plus tot :
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10Mo
       // ... termine avec big ...
       free(big);  // Liberer maintenant, ne pas attendre que la fonction retourne
       // ... plus de travail qui n'a pas besoin de big ...
   }
   ```

3. **Donnees longue duree** - globales ou donnees stockees dans des structures persistantes :
   ```hemlock
   let cache = {};  // Niveau module, vit jusqu'a la fin du programme sauf si libere

   fn cleanup() {
       free(cache);  // Nettoyage manuel pour donnees longue duree
   }
   ```

### Comptage de reference vs Garbage Collection

| Aspect | Comptage ref Hemlock | Garbage Collection |
|--------|---------------------|-------------------|
| Moment du nettoyage | Deterministe (immediat quand ref atteint 0) | Non-deterministe (GC decide quand) |
| Responsabilite utilisateur | Doit appeler `free()` | Entierement automatique |
| Pauses runtime | Aucune | Pauses "stop the world" |
| Visibilite | Detail d'implementation cache | Generalement invisible |
| Cycles | Geres avec suivi de visited-set | Geres par tracage |

### Quels types ont le comptage de reference

| Type | Compte par ref | Notes |
|------|------------|-------|
| `ptr` | Non | Necessite toujours `free()` manuel |
| `buffer` | Oui | Auto-libere a la sortie de portee ; `free()` manuel pour nettoyage anticipe |
| `array` | Oui | Auto-libere a la sortie de portee ; `free()` manuel pour nettoyage anticipe |
| `object` | Oui | Auto-libere a la sortie de portee ; `free()` manuel pour nettoyage anticipe |
| `string` | Oui | Entierement automatique, pas de `free()` necessaire |
| `function` | Oui | Entierement automatique (environnements de fermeture) |
| `task` | Oui | Comptage de reference atomique thread-safe |
| `channel` | Oui | Comptage de reference atomique thread-safe |
| Primitives | Non | Allouees sur la pile, pas d'allocation tas |

### Pourquoi cette conception ?

Cette approche hybride vous donne :
- **Controle explicite** - Vous decidez quand desallouer
- **Securite des bugs de portee** - La reassignation ne fuit pas
- **Performance previsible** - Pas de pauses GC
- **Support des fermetures** - Les fonctions peuvent capturer les variables en securite

La philosophie reste : vous etes en controle, mais le runtime aide a prevenir les bugs courants comme les fuites a la reassignation ou les double-free dans les conteneurs.

## Les deux types de pointeur

Hemlock fournit deux types de pointeur distincts, chacun avec des caracteristiques de securite differentes :

### `ptr` - Pointeur brut (dangereux)

Les pointeurs bruts sont **juste des adresses** avec des garanties de securite minimales :

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Vous devez vous souvenir de liberer
```

**Caracteristiques :**
- Juste une adresse de 8 octets
- Pas de verification des limites
- Pas de suivi de longueur
- L'utilisateur gere entierement la duree de vie
- Pour experts et FFI

**Cas d'utilisation :**
- Programmation systeme bas niveau
- Interface de fonction etrangere (FFI)
- Code critique en performance
- Quand vous avez besoin d'un controle complet

**Dangers :**
```hemlock
let p = alloc(10);
let q = p + 100;  // Bien au-dela de l'allocation - autorise mais dangereux
free(p);
let x = *p;       // Pointeur pendant - comportement indefini
free(p);          // Double-free - va planter
```

### `buffer` - Enveloppe securisee (recommande)

Les buffers fournissent un **acces verifie en limites** tout en necessitant une desallocation manuelle :

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // verifie en limites
print(b.length);        // 64
free(b);                // toujours manuel
```

**Caracteristiques :**
- Pointeur + longueur + capacite
- Verification des limites a l'acces
- Necessite toujours `free()` manuel
- Meilleur defaut pour la plupart du code

**Proprietes :**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100 (taille actuelle)
print(buf.capacity);    // 100 (capacite allouee)
```

**Verification des limites :**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // OK
buf[100] = 42;    // ERREUR : Index out of bounds
```

## API memoire

### Allocation de base

**`alloc(bytes)` - Allouer de la memoire brute**
```hemlock
let p = alloc(1024);  // Allouer 1Ko, retourne ptr
// ... utiliser la memoire
free(p);
```

**`buffer(size)` - Allouer un buffer securise**
```hemlock
let buf = buffer(256);  // Allouer un buffer de 256 octets
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - Liberer la memoire**
```hemlock
let p = alloc(100);
free(p);  // Doit liberer pour eviter la fuite memoire

let buf = buffer(100);
free(buf);  // Fonctionne sur ptr et buffer
```

**Important :** `free()` fonctionne sur les types `ptr` et `buffer`.

### Operations memoire

**`memset(ptr, byte, size)` - Remplir la memoire**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // Mettre a zero 100 octets
memset(p, 65, 10);     // Remplir les 10 premiers octets avec 'A'
free(p);
```

**`memcpy(dest, src, size)` - Copier la memoire**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // Copier 50 octets de src vers dst
free(src);
free(dst);
```

**`realloc(ptr, size)` - Redimensionner l'allocation**
```hemlock
let p = alloc(100);
// ... utiliser 100 octets
p = realloc(p, 200);   // Redimensionner a 200 octets
// ... utiliser 200 octets
free(p);
```

**Note :** Apres `realloc()`, l'ancien pointeur peut etre invalide. Utilisez toujours le pointeur retourne.

### Allocation typee

Hemlock fournit des aides d'allocation typee pour la commodite :

```hemlock
let arr = talloc(i32, 100);  // Allouer 100 valeurs i32 (400 octets)
let size = sizeof(i32);      // Retourne 4 (octets)
```

**`sizeof(type)`** retourne la taille en octets d'un type :
- `sizeof(i8)` / `sizeof(u8)` -> 1
- `sizeof(i16)` / `sizeof(u16)` -> 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` -> 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` -> 8
- `sizeof(ptr)` -> 8 (sur systemes 64-bit)

**`talloc(type, count)`** alloue `count` elements de `type` :

```hemlock
let ints = talloc(i32, 10);   // 40 octets pour 10 valeurs i32
let floats = talloc(f64, 5);  // 40 octets pour 5 valeurs f64
free(ints);
free(floats);
```

## Modeles courants

### Modele : Allouer, utiliser, liberer

Le modele basique pour la gestion memoire :

```hemlock
// 1. Allouer
let data = alloc(1024);

// 2. Utiliser
memset(data, 0, 1024);
// ... faire le travail

// 3. Liberer
free(data);
```

### Modele : Utilisation de buffer securise

Preferez les buffers pour l'acces verifie en limites :

```hemlock
let buf = buffer(256);

// Iteration securisee
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### Modele : Gestion de ressource avec try/finally

Assurer le nettoyage meme en cas d'erreur :

```hemlock
let data = alloc(1024);
try {
    // ... operations risquees
    process(data);
} finally {
    free(data);  // Toujours libere, meme en cas d'erreur
}
```

## Considerations de securite memoire

### Double-Free

**Autorise mais va planter :**
```hemlock
let p = alloc(100);
free(p);
free(p);  // CRASH : Double-free detected
```

**Prevention :**
```hemlock
let p = alloc(100);
free(p);
p = null;  // Mettre a null apres liberation

if (p != null) {
    free(p);  // Ne s'executera pas
}
```

### Pointeurs pendants

**Autorise mais comportement indefini :**
```hemlock
let p = alloc(100);
*p = 42;      // OK
free(p);
let x = *p;   // INDEFINI : Lecture de memoire liberee
```

**Prevention :** N'accedez pas a la memoire apres l'avoir liberee.

### Fuites memoire

**Facile a creer, difficile a debugger :**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // Oublie de liberer !
    return;  // Memoire fuite
}
```

**Prevention :** Toujours associer `alloc()` avec `free()` :
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... utiliser p
    } finally {
        free(p);  // Toujours libere
    }
}
```

### Arithmetique de pointeur

**Autorise mais dangereux :**
```hemlock
let p = alloc(10);
let q = p + 100;  // Bien au-dela de la limite d'allocation
*q = 42;          // INDEFINI : Ecriture hors limites
free(p);
```

**Utilisez les buffers pour la verification des limites :**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // ERREUR : La verification des limites empeche le debordement
```

## Bonnes pratiques

1. **Defaut sur `buffer`** - Utilisez `buffer` sauf si vous avez specifiquement besoin de `ptr` brut
2. **Associer alloc/free** - Chaque `alloc()` devrait avoir exactement un `free()`
3. **Utiliser try/finally** - Assurer le nettoyage avec la gestion des exceptions
4. **Null apres free** - Mettre les pointeurs a `null` apres liberation pour attraper l'utilisation apres liberation
5. **Verifier les limites** - Utiliser l'indexation de buffer pour la verification automatique des limites
6. **Documenter la propriete** - Rendre clair quel code possede et libere chaque allocation

## Exemples

### Exemple : Constructeur de chaine dynamique

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // L'appelant doit liberer
}

let msg = build_message(5);
// ... utiliser msg
free(msg);
```

### Exemple : Operations de tableau securisees

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // Remplir le tableau
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // Traiter
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // Toujours nettoyer
    }
}
```

### Exemple : Modele de pool memoire

```hemlock
// Pool memoire simple (simplifie)
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool epuise";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// Utiliser le pool
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// Liberer tout le pool d'un coup
free(pool);
```

## Limitations

Limitations actuelles a connaitre :

- **Les pointeurs bruts necessitent un free manuel** - `alloc()` retourne `ptr` sans comptage de reference
- **Pas d'allocateurs personnalises** - Seulement malloc/free systeme

**Note :** Les types comptes par reference (string, array, object, buffer) SONT automatiquement liberes quand la portee se termine. Seul le `ptr` brut de `alloc()` necessite un `free()` explicite.

## Sujets connexes

- [Chaines](strings.md) - Gestion memoire des chaines et encodage UTF-8
- [Tableaux](arrays.md) - Tableaux dynamiques et leurs caracteristiques memoire
- [Objets](objects.md) - Allocation et duree de vie des objets
- [Gestion des erreurs](error-handling.md) - Utiliser try/finally pour le nettoyage

## Voir aussi

- **Philosophie de conception** : Voir section "Memory Management" de CLAUDE.md
- **Systeme de types** : Voir [Types](types.md) pour les details des types `ptr` et `buffer`
- **FFI** : Les pointeurs bruts sont essentiels pour l'Interface de Fonction Etrangere
