# Référence de l'API Memory

Référence complète pour les fonctions de gestion de la mémoire et les types de pointeurs de Hemlock.

---

## Aperçu

Hemlock fournit une **gestion manuelle de la mémoire** avec allocation et désallocation explicites. La mémoire est gérée à travers deux types de pointeurs : les pointeurs bruts (`ptr`) et les buffers sécurisés (`buffer`).

**Principes clés :**
- Allocation et désallocation explicites
- Pas de ramasse-miettes (garbage collection)
- L'utilisateur est responsable d'appeler `free()`
- Comptage de références interne pour la sécurité des portées/réaffectations (voir ci-dessous)

### Comptage de références interne

Le runtime utilise le comptage de références en interne pour gérer la durée de vie des objets à travers les portées. Pour la plupart des variables locales, le nettoyage est automatique.

**Automatique (pas de `free()` nécessaire) :**
- Les variables locales de types à comptage de références (buffer, array, object, string) sont libérées à la sortie de la portée
- Les anciennes valeurs sont libérées lors de la réaffectation des variables
- Les éléments des conteneurs sont libérés quand les conteneurs sont libérés

**`free()` manuel requis :**
- Pointeurs bruts de `alloc()` - toujours
- Nettoyage anticipé avant la fin de la portée
- Données à longue durée de vie/globales

Voir le [Guide de gestion de la mémoire](../language-guide/memory.md#internal-reference-counting) pour les détails.

---

## Types de pointeurs

### ptr (Pointeur brut)

**Type :** `ptr`

**Description :** Adresse mémoire brute sans vérification des limites ni suivi.

**Taille :** 8 octets

**Cas d'utilisation :**
- Opérations mémoire de bas niveau
- FFI (Interface de fonction étrangère)
- Performance maximale (pas de surcharge)

**Sécurité :** Non sûr - pas de vérification des limites, l'utilisateur doit suivre la durée de vie

**Exemples :**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer (Buffer sécurisé)

**Type :** `buffer`

**Description :** Enveloppe de pointeur sécurisée avec vérification des limites.

**Structure :** Pointeur + longueur + capacité + ref_count

**Propriétés :**
- `.length` - Taille du buffer (i32)
- `.capacity` - Capacité allouée (i32)

**Cas d'utilisation :**
- La plupart des allocations mémoire
- Quand la sécurité est importante
- Tableaux dynamiques

**Sécurité :** Vérification des limites sur l'accès par index

**Comptage de références :** Les buffers sont comptés par références en interne. Libérés automatiquement à la sortie de la portée ou lors de la réaffectation de la variable. Utilisez `free()` pour un nettoyage anticipé ou les données à longue durée de vie.

**Exemples :**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Vérifié aux limites
print(b.length);        // 64
free(b);
```

---

## Fonctions d'allocation mémoire

### alloc

Alloue de la mémoire brute.

**Signature :**
```hemlock
alloc(size: i32): ptr
```

**Paramètres :**
- `size` - Nombre d'octets à allouer

**Retourne :** Pointeur vers la mémoire allouée (`ptr`)

**Exemples :**
```hemlock
let p = alloc(1024);        // Allouer 1 Ko
memset(p, 0, 1024);         // Initialiser à zéro
free(p);                    // Libérer une fois terminé

// Allouer pour une structure
let struct_size = 16;
let p2 = alloc(struct_size);
```

**Comportement :**
- Retourne de la mémoire non initialisée
- La mémoire doit être libérée manuellement
- Retourne `null` en cas d'échec d'allocation (l'appelant doit vérifier)

**Voir aussi :** `buffer()` pour une alternative plus sûre

---

### buffer

Alloue un buffer sécurisé avec vérification des limites.

**Signature :**
```hemlock
buffer(size: i32): buffer
```

**Paramètres :**
- `size` - Taille du buffer en octets

**Retourne :** Objet buffer

**Exemples :**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// Accès avec vérification des limites
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // ERREUR: hors limites

free(buf);
```

**Propriétés :**
- `.length` - Taille actuelle (i32)
- `.capacity` - Capacité allouée (i32)

**Comportement :**
- Initialise la mémoire à zéro
- Fournit une vérification des limites sur l'accès par index
- Retourne `null` en cas d'échec d'allocation (l'appelant doit vérifier)
- Doit être libéré manuellement

---

### free

Libère la mémoire allouée.

**Signature :**
```hemlock
free(ptr: ptr | buffer): null
```

**Paramètres :**
- `ptr` - Pointeur ou buffer à libérer

**Retourne :** `null`

**Exemples :**
```hemlock
// Libérer un pointeur brut
let p = alloc(1024);
free(p);

// Libérer un buffer
let buf = buffer(256);
free(buf);
```

**Comportement :**
- Libère la mémoire allouée par `alloc()` ou `buffer()`
- Double-free provoque un crash (responsabilité de l'utilisateur de l'éviter)
- Libérer des pointeurs invalides provoque un comportement indéfini

**Important :** Vous allouez, vous libérez. Pas de nettoyage automatique.

---

### realloc

Redimensionne la mémoire allouée.

**Signature :**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**Paramètres :**
- `ptr` - Pointeur à redimensionner
- `new_size` - Nouvelle taille en octets

**Retourne :** Pointeur vers la mémoire redimensionnée (peut être une adresse différente)

**Exemples :**
```hemlock
let p = alloc(100);
// ... utiliser la mémoire ...

// Besoin de plus d'espace
p = realloc(p, 200);        // Maintenant 200 octets
// ... utiliser la mémoire étendue ...

free(p);
```

**Comportement :**
- Peut déplacer la mémoire vers un nouvel emplacement
- Préserve les données existantes (jusqu'au minimum de l'ancienne/nouvelle taille)
- L'ancien pointeur est invalide après un realloc réussi (utiliser le pointeur retourné)
- Si new_size est plus petit, les données sont tronquées
- Retourne `null` en cas d'échec d'allocation (le pointeur original reste valide)

**Important :** Vérifiez toujours `null` et mettez à jour votre variable pointeur avec le résultat.

---

## Opérations mémoire

### memset

Remplit la mémoire avec une valeur d'octet.

**Signature :**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**Paramètres :**
- `ptr` - Pointeur vers la mémoire
- `byte` - Valeur d'octet à remplir (0-255)
- `size` - Nombre d'octets à remplir

**Retourne :** `null`

**Exemples :**
```hemlock
let p = alloc(100);

// Mettre la mémoire à zéro
memset(p, 0, 100);

// Remplir avec une valeur spécifique
memset(p, 0xFF, 100);

// Initialiser un buffer
let buf = alloc(256);
memset(buf, 65, 256);       // Remplir avec 'A'

free(p);
free(buf);
```

**Comportement :**
- Écrit la valeur d'octet dans chaque octet de la plage
- La valeur d'octet est tronquée à 8 bits (0-255)
- Pas de vérification des limites (non sûr)

---

### memcpy

Copie la mémoire de la source vers la destination.

**Signature :**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**Paramètres :**
- `dest` - Pointeur de destination
- `src` - Pointeur source
- `size` - Nombre d'octets à copier

**Retourne :** `null`

**Exemples :**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// Initialiser la source
memset(src, 65, 100);

// Copier vers la destination
memcpy(dest, src, 100);

// dest contient maintenant les mêmes données que src

free(src);
free(dest);
```

**Comportement :**
- Copie octet par octet de src vers dest
- Pas de vérification des limites (non sûr)
- Les régions qui se chevauchent ont un comportement indéfini (utiliser avec précaution)

---

## Opérations mémoire typées

### sizeof

Obtient la taille d'un type en octets.

**Signature :**
```hemlock
sizeof(type): i32
```

**Paramètres :**
- `type` - Identifiant de type (par ex., `i32`, `f64`, `ptr`)

**Retourne :** Taille en octets (i32)

**Tailles des types :**

| Type | Taille (octets) |
|------|-----------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**Exemples :**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// Calculer la taille d'allocation d'un tableau
let count = 100;
let total = sizeof(i32) * count; // 400 octets
```

**Comportement :**
- Retourne 0 pour les types inconnus
- Accepte à la fois les identifiants de type et les chaînes de type

---

### talloc

Alloue un tableau de valeurs typées.

**Signature :**
```hemlock
talloc(type, count: i32): ptr
```

**Paramètres :**
- `type` - Type à allouer (par ex., `i32`, `f64`, `ptr`)
- `count` - Nombre d'éléments (doit être positif)

**Retourne :** Pointeur vers le tableau alloué, ou `null` en cas d'échec d'allocation

**Exemples :**
```hemlock
let arr = talloc(i32, 100);      // Tableau de 100 i32 (400 octets)
let floats = talloc(f64, 50);    // Tableau de 50 f64 (400 octets)
let bytes = talloc(u8, 1024);    // Tableau de 1024 octets

// Toujours vérifier l'échec d'allocation
if (arr == null) {
    panic("échec d'allocation");
}

// Utiliser la mémoire allouée
// ...

free(arr);
free(floats);
free(bytes);
```

**Comportement :**
- Alloue `sizeof(type) * count` octets
- Retourne de la mémoire non initialisée
- La mémoire doit être libérée manuellement avec `free()`
- Retourne `null` en cas d'échec d'allocation (l'appelant doit vérifier)
- Panique si count n'est pas positif

---

## Propriétés des buffers

### .length

Obtient la taille du buffer.

**Type :** `i32`

**Accès :** Lecture seule

**Exemples :**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

Obtient la capacité du buffer.

**Type :** `i32`

**Accès :** Lecture seule

**Exemples :**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**Note :** Actuellement, `.length` et `.capacity` sont identiques pour les buffers crees avec `buffer()`.

---

## Interoperabilite Pointeur/Buffer

Tous les builtins `ptr_read_*`, `ptr_write_*` et `ptr_deref_*` acceptent directement les types `ptr` et `buffer`. Quand un buffer est passe, l'operation utilise le pointeur de donnees sous-jacent du buffer.

```hemlock
let buf = buffer(16);

// Ecrire directement dans un buffer (pas besoin d'extraire le ptr d'abord)
ptr_write_i32(buf, 42);
ptr_write_f64(ptr_offset(buffer_ptr(buf), 4), 3.14);

// Lire directement depuis un buffer
let val = ptr_read_i32(buf);      // 42
let fval = ptr_deref_i32(buf);    // 42

// Fonctionne aussi avec les pointeurs bruts comme avant
let p = alloc(8);
ptr_write_i32(p, 99);
let pval = ptr_read_i32(p);      // 99
free(p);
```

Cela elimine le besoin d'appeler `buffer_ptr()` avant chaque operation de lecture/ecriture typee, rendant le code base sur les buffers plus concis.

---

## Methodes de buffer

### .slice

Cree une vue zero-copie dans la memoire du buffer. La vue retournee partage la meme memoire sous-jacente que le buffer parent -- les modifications de l'original sont visibles a travers la vue et vice versa.

**Signature :**
```hemlock
buffer.slice(start: i32, end?: i32): buffer
```

**Parametres :**
- `start` - Offset d'octet de depart (base 0, inclusif). Les valeurs negatives sont bornees a 0.
- `end` - Offset d'octet de fin (exclusif). Par defaut `buffer.length` si omis. Les valeurs au-dela de la longueur du buffer sont bornees.

**Retourne :** Vue de buffer (zero-copie)

**Exemples :**
```hemlock
let buf = buffer(10);
for (let i = 0; i < 10; i++) {
    buf[i] = i + 65;  // A=65, B=66, ...
}

// Slice basique
let view = buf.slice(2, 5);
print(view.length);    // 3
print(view[0]);        // 67 (C)
print(view[1]);        // 68 (D)
print(view[2]);        // 69 (E)

// Preuve zero-copie : modifier l'original est visible a travers la vue
buf[3] = 90;           // Changer D(68) en Z(90)
print(view[1]);        // 90 (reflete le changement du parent)

// Slice a un argument (debut jusqu'a la fin)
let tail = buf.slice(7);
print(tail.length);    // 3

// Slices chainees (slice d'un slice)
let inner = view.slice(1, 3);
print(inner.length);   // 2
print(inner[0]);       // 90 (Z)

// Slice vide
let empty = buf.slice(5, 5);
print(empty.length);   // 0
```

**Comportement :**
- Retourne une vue zero-copie -- aucune memoire n'est allouee pour les donnees
- Les vues conservent une reference au buffer racine (empeche l'utilisation apres liberation)
- Les slices chainces (slice d'un slice) suivent le proprietaire racine, pas la vue intermediaire
- La verification des limites est effectuee relativement a la plage de la vue
- Les valeurs `start`/`end` hors plage sont bornees aux limites valides
- Vous **ne pouvez pas** `free()` un buffer vue -- seul le buffer racine doit etre libere
- Mettez les vues a `null` avant de liberer le buffer parent pour relacher les references

---

## Methodes de lecture/ecriture typees de buffer

Les buffers fournissent des methodes de lecture et ecriture typees sensibles a l'endianness pour construire et parser des structures de donnees binaires comme les paquets reseau, les formats de fichier et les protocoles filaires. Ces methodes sont verifiees aux limites et levent des erreurs d'execution en cas d'acces hors limites.

### Methodes d'ecriture

Ecrit une valeur typee a un offset d'octets. Les suffixes `_le` et `_be` specifient l'ordre d'octets little-endian et big-endian respectivement.

```hemlock
let pkt = buffer(64);
let offset = 0;

// Construire un en-tete de paquet
pkt.write_u16_be(offset, 0x0800);    // EtherType: IPv4
offset += 2;
pkt.write_u8(offset, 0x45);          // Version + IHL
offset += 1;
pkt.write_u8(offset, 0x00);          // DSCP/ECN
offset += 1;
pkt.write_u16_be(offset, 40);        // Longueur totale
offset += 2;
pkt.write_u32_be(offset, 0xC0A80001); // IP source : 192.168.0.1
offset += 4;

// Valeurs flottantes
pkt.write_f32_le(offset, 3.14);
offset += 4;
pkt.write_f64_be(offset, 2.71828);
offset += 8;
```

**Les ecritures mono-octet** (`write_u8`, `write_i8`) n'ont pas de suffixe d'endianness car l'ordre des octets n'est pas pertinent pour un seul octet.

### Methodes de lecture

Lit une valeur typee depuis un offset d'octets. Les suffixes d'endianness correspondent aux methodes d'ecriture.

```hemlock
let pkt = buffer(64);
// ... remplir le buffer avec des donnees ...

// Parser un en-tete de paquet
let ether_type = pkt.read_u16_be(0);    // 0x0800
let version = pkt.read_u8(2);            // 0x45
let total_len = pkt.read_u16_be(4);      // 40
let src_ip = pkt.read_u32_be(6);         // 0xC0A80001

// Lire des valeurs flottantes
let pi = pkt.read_f32_le(10);
let e = pkt.read_f64_be(14);
```

### Operations en masse

```hemlock
let src = buffer(8);
for (let i = 0; i < 8; i++) { src[i] = i + 1; }

let dest = buffer(32);
dest.write_bytes(4, src);          // Copier src dans dest a l'offset 4

let chunk = dest.read_bytes(4, 8); // Lire 8 octets a partir de l'offset 4
print(chunk[0]);                   // 1
```

### Verification des limites

Toutes les methodes de lecture/ecriture typees valident que la valeur entiere tient dans le buffer. Par exemple, `write_u32_be(offset, val)` verifie que `offset + 4 <= buffer.length`.

```hemlock
let buf = buffer(4);
buf.write_u32_be(0, 42);    // OK : 4 octets tiennent
// buf.write_u32_be(2, 42); // ERREUR : ecrirait au-dela de la fin (offset 2 + 4 > 4)
```

### Cas d'utilisation

- **Protocoles reseau :** Construire/parser des paquets TCP, UDP, DNS et personnalises
- **Formats de fichier binaires :** Lire/ecrire des en-tetes d'image, formats d'archive, etc.
- **Protocoles filaires :** Serialiser/deserialiser des messages binaires structures
- **Echange de donnees FFI :** Preparer des buffers pour les appels de bibliotheques C

---

## Modeles d'utilisation

### Modèle d'allocation basique

```hemlock
// Allouer
let p = alloc(1024);
if (p == null) {
    panic("échec d'allocation");
}

// Utiliser
memset(p, 0, 1024);

// Libérer
free(p);
```

### Modèle de buffer sécurisé

```hemlock
// Allouer le buffer
let buf = buffer(256);
if (buf == null) {
    panic("échec d'allocation du buffer");
}

// Utiliser avec vérification des limites
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// Libérer
free(buf);
```

### Modèle de croissance dynamique

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("échec d'allocation");
}

// ... utiliser la mémoire ...

// Besoin de plus d'espace - vérifier l'échec
let new_p = realloc(p, 200);
if (new_p == null) {
    // Le pointeur original est toujours valide, nettoyer
    free(p);
    panic("échec de realloc");
}
p = new_p;
size = 200;

// ... utiliser la mémoire étendue ...

free(p);
```

### Modèle de copie mémoire

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// Créer une copie
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## Considérations de sécurité

**La gestion de la mémoire de Hemlock est NON SÛRE par conception :**

### Pièges courants

**1. Fuites de mémoire**
```hemlock
// MAUVAIS: Fuite de mémoire
fn create_buffer() {
    let p = alloc(1024);
    return null;  // Mémoire fuitée !
}

// BON: Nettoyage approprié
fn create_buffer() {
    let p = alloc(1024);
    // ... utiliser la mémoire ...
    free(p);
    return null;
}
```

**2. Utilisation après libération**
```hemlock
// MAUVAIS: Utilisation après libération
let p = alloc(100);
free(p);
memset(p, 0, 100);  // CRASH: utilisation de mémoire libérée

// BON: Ne pas utiliser après libération
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// Ne pas toucher p2 après cela
```

**3. Double libération**
```hemlock
// MAUVAIS: Double libération
let p = alloc(100);
free(p);
free(p);  // CRASH: double libération

// BON: Libérer une fois
let p2 = alloc(100);
free(p2);
```

**4. Dépassement de buffer (ptr)**
```hemlock
// MAUVAIS: Dépassement de buffer avec ptr
let p = alloc(10);
memset(p, 65, 100);  // CRASH: écriture au-delà de l'allocation

// BON: Utiliser buffer pour la vérification des limites
let buf = buffer(10);
// buf[100] = 65;  // ERREUR: la vérification des limites échoue
```

**5. Pointeurs pendants**
```hemlock
// MAUVAIS: Pointeur pendant
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // CRASH: p2 est pendant

// BON: Suivre la propriété avec soin
let p = alloc(100);
// ... utiliser p ...
free(p);
// Ne pas garder d'autres références à p
```

**6. Échec d'allocation non vérifié**
```hemlock
// MAUVAIS: Ne pas vérifier null
let p = alloc(1000000000);  // Peut échouer avec peu de mémoire
memset(p, 0, 1000000000);   // CRASH: p est null

// BON: Toujours vérifier le résultat de l'allocation
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("plus de mémoire");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## Quand utiliser quoi

### Utilisez `buffer()` quand :
- Vous avez besoin de vérification des limites
- Vous travaillez avec des données dynamiques
- La sécurité est importante
- Vous apprenez Hemlock

### Utilisez `alloc()` quand :
- Performance maximale nécessaire
- FFI/interface avec C
- Vous connaissez l'agencement mémoire exact
- Vous êtes un expert

### Utilisez `realloc()` quand :
- Croissance/réduction des allocations
- Tableaux dynamiques
- Vous devez préserver les données

---

## Résumé complet des fonctions

| Fonction  | Signature                              | Retourne | Description                    |
|-----------|----------------------------------------|----------|--------------------------------|
| `alloc`   | `(size: i32)`                          | `ptr`    | Allouer de la mémoire brute    |
| `buffer`  | `(size: i32)`                          | `buffer` | Allouer un buffer sécurisé     |
| `free`    | `(ptr: ptr \| buffer)`                 | `null`   | Libérer la mémoire             |
| `realloc` | `(ptr: ptr, new_size: i32)`            | `ptr`    | Redimensionner l'allocation    |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`     | `null`   | Remplir la mémoire             |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`     | `null`   | Copier la mémoire              |
| `sizeof`  | `(type)`                               | `i32`    | Obtenir la taille du type en octets |
| `talloc`  | `(type, count: i32)`                   | `ptr`    | Allouer un tableau typé        |

---

## Voir aussi

- [Système de types](type-system.md) - Types pointeur et buffer
- [Fonctions intégrées](builtins.md) - Toutes les fonctions intégrées
- [API String](string-api.md) - Méthode `.to_bytes()` des chaînes
