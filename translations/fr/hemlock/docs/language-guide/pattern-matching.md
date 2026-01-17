# Filtrage par motif (Pattern Matching)

Hemlock fournit un filtrage par motif puissant grace aux expressions `match`, offrant un moyen concis de destructurer les valeurs, verifier les types et gerer plusieurs cas.

## Syntaxe de base

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => expression_par_defaut
};
```

Les expressions match evaluent `value` contre chaque motif dans l'ordre, retournant le resultat de l'expression de la premiere branche correspondante.

## Types de motifs

### Motifs litteraux

Correspondre a des valeurs exactes :

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "un",
    42 => "la reponse",
    _ => "autre"
};
print(msg);  // "la reponse"
```

Litteraux supportes :
- **Entiers** : `0`, `42`, `-5`
- **Flottants** : `3.14`, `-0.5`
- **Chaines** : `"hello"`, `"world"`
- **Booleens** : `true`, `false`
- **Null** : `null`

### Motif joker (`_`)

Correspond a n'importe quelle valeur sans liaison :

```hemlock
let x = "n'importe quoi";
let result = match (x) {
    "specifique" => "trouve",
    _ => "joker correspond"
};
```

### Motifs de liaison de variable

Lier la valeur correspondante a une variable :

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "la valeur est " + n  // n lie a 100
};
print(result);  // "la valeur est 100"
```

### Motifs OU (`|`)

Correspondre a plusieurs alternatives :

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "petit",
    4 | 5 | 6 => "moyen",
    _ => "grand"
};

// Fonctionne avec les chaines aussi
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "sortie",
    "help" | "h" | "?" => "afficher aide",
    _ => "inconnu"
};
```

### Expressions de garde (`if`)

Ajouter des conditions aux motifs :

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negatif",
    n if n == 0 => "zero",
    n if n < 10 => "petit",
    n if n < 100 => "moyen",
    n => "grand: " + n
};
print(category);  // "moyen"

// Gardes complexes
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "pair et superieur a 10",
    n if n % 2 == 0 => "pair",
    n => "impair"
};
```

### Motifs de type

Verifier et lier en fonction du type :

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "entier: " + num,
    str: string => "chaine: " + str,
    flag: bool => "booleen: " + flag,
    _ => "autre type"
};
print(desc);  // "entier: 42"
```

Types supportes : `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Motifs de destructuration

### Destructuration d'objet

Extraire des champs des objets :

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "point a " + x + "," + y
};
print(result);  // "point a 10,20"

// Avec valeurs de champ litterales
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origine",
    { x: 0, y } => "sur axe y a " + y,
    { x, y: 0 } => "sur axe x a " + x,
    { x, y } => "point a " + x + "," + y
};
print(name);  // "origine"
```

### Destructuration de tableau

Correspondre a la structure et aux elements du tableau :

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "vide",
    [x] => "unique: " + x,
    [x, y] => "paire: " + x + "," + y,
    [x, y, z] => "triple: " + x + "," + y + "," + z,
    _ => "beaucoup d'elements"
};
print(desc);  // "triple: 1,2,3"

// Avec valeurs litterales
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "les deux zero",
    [1, x] => "commence par 1, second est " + x,
    [x, 1] => "finit par 1",
    _ => "autre"
};
print(result);  // "commence par 1, second est 2"
```

### Motifs rest de tableau (`...`)

Capturer les elements restants :

```hemlock
let nums = [1, 2, 3, 4, 5];

// Tete et queue
let result = match (nums) {
    [first, ...rest] => "premier: " + first,
    [] => "vide"
};
print(result);  // "premier: 1"

// Deux premiers elements
let result2 = match (nums) {
    [a, b, ...rest] => "deux premiers: " + a + "," + b,
    _ => "trop court"
};
print(result2);  // "deux premiers: 1,2"
```

### Destructuration imbriquee

Combiner les motifs pour des donnees complexes :

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " vit a " + city,
    _ => "inconnu"
};
print(result);  // "Alice vit a NYC"

// Objet contenant un tableau
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "premier: " + first + ", total: " + count,
    _ => "pas d'elements"
};
print(result2);  // "premier: 1, total: 3"
```

## Match comme expression

Match est une expression qui retourne une valeur :

```hemlock
// Assignation directe
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// Dans une concatenation de chaines
let msg = "Note: " + match (grade) {
    n if n >= 70 => "reussite",
    _ => "echec"
};

// Dans un retour de fonction
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positif",
        _ => "negatif"
    };
}
```

## Bonnes pratiques du filtrage par motif

1. **L'ordre compte** : Les motifs sont verifies de haut en bas ; mettez les motifs specifiques avant les generaux
2. **Utilisez les jokers pour l'exhaustivite** : Incluez toujours un repli `_` sauf si vous etes certain que tous les cas sont couverts
3. **Preferez les gardes aux conditions imbriquees** : Les gardes rendent l'intention plus claire
4. **Utilisez la destructuration plutot que l'acces manuel aux champs** : Plus concis et plus sur

```hemlock
// Bon : Gardes pour verification de plage
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "en dessous de B"
}

// Bon : Destructurer au lieu d'acceder aux champs
match (point) {
    { x: 0, y: 0 } => "origine",
    { x, y } => "a " + x + "," + y
}

// Eviter : Motifs imbriques trop complexes
// A la place, considerez diviser en plusieurs match ou utiliser des gardes
```

## Comparaison avec d'autres langages

| Fonctionnalite | Hemlock | Rust | JavaScript |
|----------------|---------|------|------------|
| Match basique | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Destructuration | Oui | Oui | Partiel (switch ne destructure pas) |
| Gardes | `n if n > 0 =>` | `n if n > 0 =>` | N/A |
| Motifs OU | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Motifs rest | `[a, ...rest]` | `[a, rest @ ..]` | N/A |
| Motifs de type | `n: i32` | Type via branche `match` | N/A |
| Retourne valeur | Oui | Oui | Non (instruction) |

## Notes d'implementation

Le filtrage par motif est implemente dans les backends interpreteur et compilateur avec parite complete - les deux produisent des resultats identiques pour la meme entree. Cette fonctionnalite est disponible dans Hemlock v1.8.0+.
