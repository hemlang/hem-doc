# Tableaux

Hemlock fournit des **tableaux dynamiques** avec des methodes completes pour la manipulation et le traitement des donnees. Les tableaux peuvent contenir des types mixtes et s'agrandissent automatiquement selon les besoins.

## Apercu

```hemlock
// Litteraux de tableau
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Types mixtes autorises
let mixed = [1, "bonjour", true, null];

// Dimensionnement dynamique
arr.push(6);           // S'agrandit automatiquement
arr.push(7);
print(arr.length);     // 7
```

## Litteraux de tableau

### Syntaxe basique

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["pomme", "banane", "cerise"];
let booleans = [true, false, true];
```

### Tableaux vides

```hemlock
let arr = [];  // Tableau vide

// Ajouter des elements plus tard
arr.push(1);
arr.push(2);
arr.push(3);
```

### Types mixtes

Les tableaux peuvent contenir differents types :

```hemlock
let mixed = [
    42,
    "bonjour",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "bonjour"
print(mixed[4]);  // [1, 2, 3] (tableau imbrique)
```

### Tableaux imbriques

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### Tableaux types

Les tableaux peuvent avoir des annotations de type pour appliquer les types d'elements :

```hemlock
// Syntaxe de tableau type
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Verification de type a l'execution
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "deux", 3]; // Erreur d'execution : type mismatch

// Tableaux types imbriques
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Comportement des annotations de type :**
- Les elements sont verifies quand ils sont ajoutes au tableau
- Les incompatibilites de type causent des erreurs a l'execution
- Sans annotation de type, les tableaux acceptent des types mixtes

## Indexation

### Lecture d'elements

Acces indexe a partir de zero :

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (premier element)
print(arr[4]);  // 50 (dernier element)

// Hors limites retourne null (pas d'erreur)
print(arr[10]);  // null
```

### Ecriture d'elements

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Modifier existant
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Peut assigner au-dela de la longueur actuelle (agrandit le tableau)
arr[5] = 60;    // Cree [10, 20, 3, null, null, 60]
```

### Indices negatifs

**Non supportes** - Utilisez uniquement des indices positifs :

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // ERREUR ou comportement indefini

// Utilisez length pour le dernier element
print(arr[arr.length - 1]);  // 3
```

## Proprietes

### Propriete `.length`

Retourne le nombre d'elements :

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Tableau vide
let empty = [];
print(empty.length);  // 0

// Apres modifications
arr.push(6);
print(arr.length);  // 6
```

## Methodes de tableau

Hemlock fournit 18 methodes de tableau pour une manipulation complete.

### Operations de pile

**`push(value)`** - Ajouter un element a la fin :
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Supprimer et retourner le dernier element :
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Retourne 5, arr est maintenant [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Operations de file

**`shift()`** - Supprimer et retourner le premier element :
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Retourne 1, arr est maintenant [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Ajouter un element au debut :
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Insertion et suppression

**`insert(index, value)`** - Inserer un element a l'index :
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // Inserer 3 a l'index 2 : [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Inserer au debut : [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Supprimer et retourner l'element a l'index :
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Retourne 3, arr est maintenant [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Operations de recherche

**`find(value)`** - Trouver la premiere occurrence :
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (index de la premiere occurrence)
let idx2 = arr.find(99);     // -1 (non trouve)

// Fonctionne avec n'importe quel type
let words = ["pomme", "banane", "cerise"];
let idx3 = words.find("banane");  // 1
```

**`contains(value)`** - Verifier si le tableau contient une valeur :
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Operations d'extraction

**`slice(start, end)`** - Extraire un sous-tableau (fin exclusive) :
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (indices 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Original inchange
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Obtenir le premier element (sans le supprimer) :
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (sans le supprimer)
print(arr);                  // [1, 2, 3] (inchange)
```

**`last()`** - Obtenir le dernier element (sans le supprimer) :
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (sans le supprimer)
print(arr);                  // [1, 2, 3] (inchange)
```

### Operations de transformation

**`reverse()`** - Inverser le tableau sur place :
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (modifie)
```

**`join(delimiter)`** - Joindre les elements en chaine :
```hemlock
let words = ["bonjour", "monde", "foo"];
let joined = words.join(" ");  // "bonjour monde foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Fonctionne avec les types mixtes
let mixed = [1, "bonjour", true, null];
print(mixed.join(" | "));  // "1 | bonjour | true | null"
```

**`concat(other)`** - Concatener avec un autre tableau :
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (nouveau tableau)

// Originaux inchanges
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Operations utilitaires

**`clear()`** - Supprimer tous les elements :
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Chainage de methodes

Les methodes qui retournent des tableaux ou des valeurs permettent le chainage :

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["pomme", "banane", "cerise"]
    .slice(0, 2)
    .join(" et ");  // "pomme et banane"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Reference complete des methodes

| Methode | Parametres | Retourne | Modifie | Description |
|---------|------------|----------|---------|-------------|
| `push(value)` | any | void | Oui | Ajouter un element a la fin |
| `pop()` | - | any | Oui | Supprimer et retourner le dernier |
| `shift()` | - | any | Oui | Supprimer et retourner le premier |
| `unshift(value)` | any | void | Oui | Ajouter un element au debut |
| `insert(index, value)` | i32, any | void | Oui | Inserer a l'index |
| `remove(index)` | i32 | any | Oui | Supprimer et retourner a l'index |
| `find(value)` | any | i32 | Non | Trouver la premiere occurrence (-1 si non trouve) |
| `contains(value)` | any | bool | Non | Verifier si contient la valeur |
| `slice(start, end)` | i32, i32 | array | Non | Extraire un sous-tableau (nouveau tableau) |
| `join(delimiter)` | string | string | Non | Joindre en chaine |
| `concat(other)` | array | array | Non | Concatener (nouveau tableau) |
| `reverse()` | - | void | Oui | Inverser sur place |
| `first()` | - | any | Non | Obtenir le premier element |
| `last()` | - | any | Non | Obtenir le dernier element |
| `clear()` | - | void | Oui | Supprimer tous les elements |
| `map(callback)` | fn | array | Non | Transformer chaque element |
| `filter(predicate)` | fn | array | Non | Selectionner les elements correspondants |
| `reduce(callback, initial)` | fn, any | any | Non | Reduire a une seule valeur |

## Details d'implementation

### Modele memoire

- **Alloue sur le tas** - Capacite dynamique
- **Croissance automatique** - Double la capacite quand depassee
- **Pas de reduction automatique** - La capacite ne diminue pas
- **Pas de verification des limites sur l'indexation** - Utilisez les methodes pour la securite

### Gestion de la capacite

```hemlock
let arr = [];  // Capacite initiale : 0

arr.push(1);   // Croit vers capacite 1
arr.push(2);   // Croit vers capacite 2
arr.push(3);   // Croit vers capacite 4 (double)
arr.push(4);   // Toujours capacite 4
arr.push(5);   // Croit vers capacite 8 (double)
```

### Comparaison de valeurs

`find()` et `contains()` utilisent l'egalite de valeur :

```hemlock
// Primitives : comparaison par valeur
let arr = [1, 2, 3];
arr.contains(2);  // true

// Chaines : comparaison par valeur
let words = ["bonjour", "monde"];
words.contains("bonjour");  // true

// Objets : comparaison par reference
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (meme reference)
arr2.contains(obj2);  // false (reference differente)
```

## Modeles courants

### Operations fonctionnelles (map/filter/reduce)

Les tableaux ont des methodes integrees `map`, `filter` et `reduce` :

```hemlock
// map - transformer chaque element
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - selectionner les elements correspondants
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - accumuler vers une seule valeur
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Chainage des operations fonctionnelles
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Modele : Tableau comme pile

```hemlock
let stack = [];

// Empiler sur la pile
stack.push(1);
stack.push(2);
stack.push(3);

// Depiler de la pile
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Modele : Tableau comme file

```hemlock
let queue = [];

// Enfiler (ajouter a la fin)
queue.push(1);
queue.push(2);
queue.push(3);

// Defiler (supprimer du debut)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Bonnes pratiques

1. **Utilisez les methodes plutot que l'indexation directe** - Verification des limites et clarte
2. **Verifiez les limites** - L'indexation directe ne verifie pas les limites
3. **Preferez les operations immuables** - Utilisez `slice()` et `concat()` plutot que la mutation
4. **Initialisez avec la capacite** - Si vous connaissez la taille (pas actuellement supporte)
5. **Utilisez `contains()` pour l'appartenance** - Plus clair que les boucles manuelles
6. **Chainez les methodes** - Plus lisible que les appels imbriques

## Pieges courants

### Piege : Index direct hors limites

```hemlock
let arr = [1, 2, 3];

// Pas de verification des limites !
arr[10] = 99;  // Cree un tableau sparse avec des nulls
print(arr.length);  // 11 (pas 3 !)

// Mieux : Utilisez push() ou verifiez la longueur
if (arr.length <= 10) {
    arr.push(99);
}
```

### Piege : Mutation vs. nouveau tableau

```hemlock
let arr = [1, 2, 3];

// Modifie l'original
arr.reverse();
print(arr);  // [3, 2, 1]

// Retourne un nouveau tableau
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (inchange)
print(sub);  // [3, 2]
```

### Piege : Egalite de reference

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Meme reference : true
arr.contains(obj);  // true

// Reference differente : false
arr.contains({ x: 10 });  // false (objet different)
```

### Piege : Tableaux longue duree

```hemlock
// Les tableaux en portee locale sont auto-liberes, mais les tableaux globaux/longue duree necessitent attention
let global_cache = [];  // Niveau module, persiste jusqu'a la fin du programme

fn add_to_cache(item) {
    global_cache.push(item);  // Croit indefiniment
}

// Pour les donnees longue duree, considerez :
// - Vider le tableau periodiquement : global_cache.clear();
// - Liberer tot quand termine : free(global_cache);
```

## Exemples

### Exemple : Statistiques de tableau

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### Exemple : Deduplication de tableau

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### Exemple : Decoupage de tableau

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### Exemple : Aplatissement de tableau

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Tableau imbrique - l'aplatir
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### Exemple : Tri (tri a bulles)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Echanger
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // Modifie sur place
print(numbers);  // [1, 2, 5, 8, 9]
```

## Limitations

Limitations actuelles :

- **Pas de verification des limites sur l'indexation** - L'acces direct n'est pas verifie
- **Egalite de reference pour les objets** - `find()` et `contains()` utilisent la comparaison de reference
- **Pas de destructuration de tableau** - Pas de syntaxe `let [a, b] = arr`
- **Pas d'operateur spread** - Pas de syntaxe `[...arr1, ...arr2]`

**Note :** Les tableaux sont comptes par reference et automatiquement liberes quand la portee se termine. Voir [Gestion de la memoire](memory.md#internal-reference-counting) pour les details.

## Sujets connexes

- [Chaines](strings.md) - Methodes de chaine similaires aux methodes de tableau
- [Objets](objects.md) - Les tableaux sont aussi similaires a des objets
- [Fonctions](functions.md) - Fonctions d'ordre superieur avec les tableaux
- [Flux de controle](control-flow.md) - Iterer sur les tableaux

## Voir aussi

- **Dimensionnement dynamique** : Les tableaux croissent automatiquement avec doublement de la capacite
- **Methodes** : 18 methodes completes pour la manipulation incluant map/filter/reduce
- **Memoire** : Voir [Memoire](memory.md) pour les details d'allocation de tableau
