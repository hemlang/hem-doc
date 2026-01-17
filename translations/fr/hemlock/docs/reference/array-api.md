# Référence de l'API Array

Référence complète pour le type array de Hemlock et ses 18 méthodes.

---

## Aperçu

Les tableaux (arrays) dans Hemlock sont des séquences **dynamiques, allouées sur le tas** qui peuvent contenir des types mixtes. Ils fournissent des méthodes complètes pour la manipulation et le traitement des données.

**Caractéristiques principales :**
- Dimensionnement dynamique (croissance automatique)
- Indexation à partir de zéro
- Types mixtes autorisés
- 18 méthodes intégrées
- Alloués sur le tas avec suivi de la capacité

---

## Type Array

**Type :** `array`

**Propriétés :**
- `.length` - Nombre d'éléments (i32)

**Syntaxe littérale :** Crochets `[elem1, elem2, ...]`

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// Types mixtes
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// Tableau vide
let empty = [];
print(empty.length);   // 0
```

---

## Indexation

Les tableaux supportent l'indexation à base zéro en utilisant `[]` :

**Accès en lecture :**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**Accès en écriture :**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**Note :** L'indexation directe ne vérifie pas les limites. Utilisez les méthodes pour plus de sécurité.

---

## Propriétés des tableaux

### .length

Obtient le nombre d'éléments dans le tableau.

**Type :** `i32`

**Exemples :**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// La longueur change dynamiquement
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## Méthodes des tableaux

### Opérations de pile (Stack)

#### push

Ajoute un élément à la fin du tableau.

**Signature :**
```hemlock
array.push(value: any): null
```

**Paramètres :**
- `value` - Élément à ajouter

**Retourne :** `null`

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

Retire et retourne le dernier élément.

**Signature :**
```hemlock
array.pop(): any
```

**Retourne :** Dernier élément (retiré du tableau)

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**Erreur :** Erreur d'exécution si le tableau est vide.

---

### Opérations de file (Queue)

#### shift

Retire et retourne le premier élément.

**Signature :**
```hemlock
array.shift(): any
```

**Retourne :** Premier élément (retiré du tableau)

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**Erreur :** Erreur d'exécution si le tableau est vide.

---

#### unshift

Ajoute un élément au début du tableau.

**Signature :**
```hemlock
array.unshift(value: any): null
```

**Paramètres :**
- `value` - Élément à ajouter

**Retourne :** `null`

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### Insertion et suppression

#### insert

Insère un élément à un index spécifique.

**Signature :**
```hemlock
array.insert(index: i32, value: any): null
```

**Paramètres :**
- `index` - Position d'insertion (base 0)
- `value` - Élément à insérer

**Retourne :** `null`

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// Insertion à la fin
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**Comportement :** Décale les éléments à partir de l'index vers la droite.

---

#### remove

Retire et retourne l'élément à l'index spécifié.

**Signature :**
```hemlock
array.remove(index: i32): any
```

**Paramètres :**
- `index` - Position de suppression (base 0)

**Retourne :** Élément supprimé

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**Comportement :** Décale les éléments après l'index vers la gauche.

**Erreur :** Erreur d'exécution si l'index est hors limites.

---

### Recherche

#### find

Trouve la première occurrence d'une valeur.

**Signature :**
```hemlock
array.find(value: any): i32
```

**Paramètres :**
- `value` - Valeur à rechercher

**Retourne :** Index de la première occurrence, ou `-1` si non trouvée

**Exemples :**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1 (non trouvée)

// Trouver le premier doublon
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1 (première occurrence)
```

**Comparaison :** Utilise l'égalité de valeur pour les primitives et les chaînes.

---

#### contains

Vérifie si le tableau contient une valeur.

**Signature :**
```hemlock
array.contains(value: any): bool
```

**Paramètres :**
- `value` - Valeur à rechercher

**Retourne :** `true` si trouvée, `false` sinon

**Exemples :**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// Fonctionne avec les chaînes
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### Découpage et extraction

#### slice

Extrait un sous-tableau par plage (fin exclusive).

**Signature :**
```hemlock
array.slice(start: i32, end: i32): array
```

**Paramètres :**
- `start` - Index de départ (base 0, inclusif)
- `end` - Index de fin (exclusif)

**Retourne :** Nouveau tableau avec les éléments de [start, end)

**Modifie :** Non (retourne un nouveau tableau)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// Tranche vide
let empty = arr.slice(2, 2); // []
```

---

#### first

Obtient le premier élément sans le retirer.

**Signature :**
```hemlock
array.first(): any
```

**Retourne :** Premier élément

**Modifie :** Non

**Exemples :**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3] (inchangé)
```

**Erreur :** Erreur d'exécution si le tableau est vide.

---

#### last

Obtient le dernier élément sans le retirer.

**Signature :**
```hemlock
array.last(): any
```

**Retourne :** Dernier élément

**Modifie :** Non

**Exemples :**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3] (inchangé)
```

**Erreur :** Erreur d'exécution si le tableau est vide.

---

### Manipulation de tableaux

#### reverse

Inverse le tableau sur place.

**Signature :**
```hemlock
array.reverse(): null
```

**Retourne :** `null`

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

Supprime tous les éléments du tableau.

**Signature :**
```hemlock
array.clear(): null
```

**Retourne :** `null`

**Modifie :** Oui (modifie le tableau sur place)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### Combinaison de tableaux

#### concat

Concatène avec un autre tableau.

**Signature :**
```hemlock
array.concat(other: array): array
```

**Paramètres :**
- `other` - Tableau à concaténer

**Retourne :** Nouveau tableau avec les éléments des deux tableaux

**Modifie :** Non (retourne un nouveau tableau)

**Exemples :**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3] (inchangé)
print(b);                    // [4, 5, 6] (inchangé)

// Enchaîner les concaténations
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### Opérations fonctionnelles

#### map

Transforme chaque élément en utilisant une fonction de rappel (callback).

**Signature :**
```hemlock
array.map(callback: fn): array
```

**Paramètres :**
- `callback` - Fonction qui prend un élément et retourne une valeur transformée

**Retourne :** Nouveau tableau avec les éléments transformés

**Modifie :** Non (retourne un nouveau tableau)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

Sélectionne les éléments qui correspondent à un prédicat.

**Signature :**
```hemlock
array.filter(predicate: fn): array
```

**Paramètres :**
- `predicate` - Fonction qui prend un élément et retourne bool

**Retourne :** Nouveau tableau avec les éléments où le prédicat a retourné true

**Modifie :** Non (retourne un nouveau tableau)

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

Réduit le tableau à une seule valeur en utilisant un accumulateur.

**Signature :**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**Paramètres :**
- `callback` - Fonction qui prend (accumulateur, élément) et retourne le nouvel accumulateur
- `initial` - Valeur de départ pour l'accumulateur

**Retourne :** Valeur finale accumulée

**Modifie :** Non

**Exemples :**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// Trouver la valeur maximale
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### Conversion en chaîne

#### join

Joint les éléments en une chaîne avec un délimiteur.

**Signature :**
```hemlock
array.join(delimiter: string): string
```

**Paramètres :**
- `delimiter` - Chaîne à placer entre les éléments

**Retourne :** Chaîne avec tous les éléments joints

**Exemples :**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Fonctionne avec les types mixtes
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// Délimiteur vide
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**Comportement :** Convertit automatiquement tous les éléments en chaînes.

---

## Chaînage de méthodes

Les méthodes de tableaux peuvent être chaînées pour des opérations concises :

**Exemples :**
```hemlock
// Chaîner slice et join
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// Chaîner concat et slice
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// Chaînage complexe
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## Résumé complet des méthodes

### Méthodes modifiantes

Méthodes qui modifient le tableau sur place :

| Méthode    | Signature                    | Retourne  | Description                         |
|------------|------------------------------|-----------|-------------------------------------|
| `push`     | `(value: any)`               | `null`    | Ajouter à la fin                    |
| `pop`      | `()`                         | `any`     | Retirer de la fin                   |
| `shift`    | `()`                         | `any`     | Retirer du début                    |
| `unshift`  | `(value: any)`               | `null`    | Ajouter au début                    |
| `insert`   | `(index: i32, value: any)`   | `null`    | Insérer à l'index                   |
| `remove`   | `(index: i32)`               | `any`     | Retirer à l'index                   |
| `reverse`  | `()`                         | `null`    | Inverser sur place                  |
| `clear`    | `()`                         | `null`    | Supprimer tous les éléments         |

### Méthodes non modifiantes

Méthodes qui retournent de nouvelles valeurs sans modifier l'original :

| Méthode    | Signature                        | Retourne  | Description                         |
|------------|----------------------------------|-----------|-------------------------------------|
| `find`     | `(value: any)`                   | `i32`     | Trouver la première occurrence      |
| `contains` | `(value: any)`                   | `bool`    | Vérifier si contient la valeur      |
| `slice`    | `(start: i32, end: i32)`         | `array`   | Extraire un sous-tableau            |
| `first`    | `()`                             | `any`     | Obtenir le premier élément          |
| `last`     | `()`                             | `any`     | Obtenir le dernier élément          |
| `concat`   | `(other: array)`                 | `array`   | Concaténer les tableaux             |
| `join`     | `(delimiter: string)`            | `string`  | Joindre les éléments en chaîne      |
| `map`      | `(callback: fn)`                 | `array`   | Transformer chaque élément          |
| `filter`   | `(predicate: fn)`                | `array`   | Sélectionner les éléments correspondants |
| `reduce`   | `(callback: fn, initial: any)`   | `any`     | Réduire à une seule valeur          |

---

## Modèles d'utilisation

### Utilisation comme pile (Stack)

```hemlock
let stack = [];

// Empiler des éléments
stack.push(1);
stack.push(2);
stack.push(3);

// Dépiler des éléments
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### Utilisation comme file (Queue)

```hemlock
let queue = [];

// Enfiler
queue.push(1);
queue.push(2);
queue.push(3);

// Défiler
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### Transformation de tableau

```hemlock
// Filtrage (manuel)
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// Mapping (manuel)
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### Construction de tableaux

```hemlock
let arr = [];

// Construire un tableau avec une boucle
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## Détails d'implémentation

**Gestion de la capacité :**
- Les tableaux grandissent automatiquement selon les besoins
- La capacité double lorsqu'elle est dépassée
- Pas de contrôle manuel de la capacité

**Comparaison de valeurs :**
- `find()` et `contains()` utilisent l'égalité de valeur
- Fonctionne correctement pour les primitives et les chaînes
- Les objets/tableaux sont comparés par référence

**Mémoire :**
- Alloués sur le tas
- Pas de libération automatique (gestion manuelle de la mémoire)
- Pas de vérification des limites sur l'accès direct par index

---

## Voir aussi

- [Système de types](type-system.md) - Détails sur le type array
- [API String](string-api.md) - Résultats de join() sur les chaînes
- [Opérateurs](operators.md) - Opérateur d'indexation des tableaux
