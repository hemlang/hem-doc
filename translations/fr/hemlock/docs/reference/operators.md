# Référence des opérateurs

Référence complète pour tous les opérateurs dans Hemlock, y compris la priorité, l'associativité et le comportement.

---

## Aperçu

Hemlock fournit des opérateurs de style C avec des règles de priorité explicites. Tous les opérateurs suivent des règles de typage strictes avec promotion de type automatique lorsque applicable.

---

## Opérateurs arithmétiques

### Arithmétique binaire

| Opérateur | Nom            | Exemple    | Description                    |
|-----------|----------------|------------|--------------------------------|
| `+`       | Addition       | `a + b`    | Additionner deux valeurs       |
| `-`       | Soustraction   | `a - b`    | Soustraire b de a              |
| `*`       | Multiplication | `a * b`    | Multiplier deux valeurs        |
| `/`       | Division       | `a / b`    | Diviser a par b                |

**Promotion de type :**
Les résultats suivent les règles de promotion de type (voir [Système de types](type-system.md#règles-de-promotion-de-type)).

**Exemples :**
```hemlock
let a = 10 + 5;        // 15 (i32)
let b = 10 - 3;        // 7 (i32)
let c = 4 * 5;         // 20 (i32)
let d = 20 / 4;        // 5 (i32)

// Division flottante
let e = 10.0 / 3.0;    // 3.333... (f64)

// Types mixtes
let f: u8 = 10;
let g: i32 = 20;
let h = f + g;         // 30 (i32, promu)
```

**Division par zéro :**
- Division entière par zéro : Erreur d'exécution
- Division flottante par zéro : Retourne `inf` ou `-inf`

---

### Arithmétique unaire

| Opérateur | Nom      | Exemple | Description          |
|-----------|----------|---------|----------------------|
| `-`       | Négation | `-a`    | Négation de la valeur|
| `+`       | Plus     | `+a`    | Identité (pas d'effet)|

**Exemples :**
```hemlock
let a = 5;
let b = -a;            // -5
let c = +a;            // 5 (pas de changement)

let x = -3.14;         // -3.14
```

---

## Opérateurs de comparaison

| Opérateur | Nom                       | Exemple    | Retourne |
|-----------|---------------------------|------------|----------|
| `==`      | Égal                      | `a == b`   | `bool`   |
| `!=`      | Différent                 | `a != b`   | `bool`   |
| `<`       | Inférieur à               | `a < b`    | `bool`   |
| `>`       | Supérieur à               | `a > b`    | `bool`   |
| `<=`      | Inférieur ou égal à       | `a <= b`   | `bool`   |
| `>=`      | Supérieur ou égal à       | `a >= b`   | `bool`   |

**Promotion de type :**
Les opérandes sont promus avant la comparaison.

**Exemples :**
```hemlock
print(5 == 5);         // true
print(10 != 5);        // true
print(3 < 7);          // true
print(10 > 5);         // true
print(5 <= 5);         // true
print(10 >= 5);        // true

// Comparaison de chaînes
print("hello" == "hello");  // true
print("abc" < "def");       // true (lexicographique)

// Types mixtes
let a: u8 = 10;
let b: i32 = 10;
print(a == b);         // true (promu en i32)
```

---

## Opérateurs logiques

| Opérateur | Nom         | Exemple      | Description                    |
|-----------|-------------|--------------|--------------------------------|
| `&&`      | ET logique  | `a && b`     | Vrai si les deux sont vrais    |
| `||`      | OU logique  | `a || b`     | Vrai si l'un est vrai          |
| `!`       | NON logique | `!a`         | Négation booléenne             |

**Évaluation en court-circuit :**
- `&&` - S'arrête à la première valeur fausse
- `||` - S'arrête à la première valeur vraie

**Exemples :**
```hemlock
let a = true;
let b = false;

print(a && b);         // false
print(a || b);         // true
print(!a);             // false
print(!b);             // true

// Court-circuit
if (x != 0 && (10 / x) > 2) {
    print("sûr");
}

if (x == 0 || (10 / x) > 2) {
    print("sûr");
}
```

---

## Opérateurs bit à bit

**Restriction :** Types entiers uniquement (i8-i64, u8-u64)

### Bit à bit binaire

| Opérateur | Nom              | Exemple    | Description               |
|-----------|------------------|------------|---------------------------|
| `&`       | ET bit à bit     | `a & b`    | ET sur chaque bit         |
| `|`       | OU bit à bit     | `a | b`    | OU sur chaque bit         |
| `^`       | XOR bit à bit    | `a ^ b`    | XOR sur chaque bit        |
| `<<`      | Décalage gauche  | `a << b`   | Décaler à gauche de b bits|
| `>>`      | Décalage droite  | `a >> b`   | Décaler à droite de b bits|

**Préservation du type :**
Le type du résultat correspond aux types des opérandes (avec promotion de type).

**Exemples :**
```hemlock
let a = 12;  // 1100 en binaire
let b = 10;  // 1010 en binaire

print(a & b);          // 8  (1000)
print(a | b);          // 14 (1110)
print(a ^ b);          // 6  (0110)
print(a << 2);         // 48 (110000)
print(a >> 1);         // 6  (110)
```

**Exemple non signé :**
```hemlock
let c: u8 = 15;        // 00001111
let d: u8 = 7;         // 00000111

print(c & d);          // 7  (00000111)
print(c | d);          // 15 (00001111)
print(c ^ d);          // 8  (00001000)
```

**Comportement du décalage droit :**
- Types signés : Décalage arithmétique (étend le signe)
- Types non signés : Décalage logique (remplit avec des zéros)

---

### Bit à bit unaire

| Opérateur | Nom            | Exemple | Description               |
|-----------|----------------|---------|---------------------------|
| `~`       | NON bit à bit  | `~a`    | Inverse tous les bits     |

**Exemples :**
```hemlock
let a = 12;            // 00001100 (i32)
print(~a);             // -13 (complément à deux)

let b: u8 = 15;        // 00001111
print(~b);             // 240 (11110000)
```

---

## Opérateurs de chaîne

### Concaténation

| Opérateur | Nom            | Exemple    | Description        |
|-----------|----------------|------------|--------------------|
| `+`       | Concaténation  | `a + b`    | Joindre des chaînes|

**Exemples :**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"

// String + rune
let greeting = "Hello" + '!';      // "Hello!"

// Rune + string
let prefix = '>' + " Message";     // "> Message"
```

---

## Opérateurs d'affectation

### Affectation basique

| Opérateur | Nom         | Exemple    | Description                   |
|-----------|-------------|------------|-------------------------------|
| `=`       | Affectation | `a = b`    | Affecter une valeur à une variable |

**Exemples :**
```hemlock
let x = 10;
x = 20;

let arr = [1, 2, 3];
arr[0] = 99;

let obj = { x: 10 };
obj.x = 20;
```

### Affectation composée

#### Affectation composée arithmétique

| Opérateur | Nom                   | Exemple    | Équivalent         |
|-----------|-----------------------|------------|--------------------|
| `+=`      | Ajouter et affecter   | `a += b`   | `a = a + b`        |
| `-=`      | Soustraire et affecter| `a -= b`   | `a = a - b`        |
| `*=`      | Multiplier et affecter| `a *= b`   | `a = a * b`        |
| `/=`      | Diviser et affecter   | `a /= b`   | `a = a / b`        |
| `%=`      | Modulo et affecter    | `a %= b`   | `a = a % b`        |

**Exemples :**
```hemlock
let x = 10;
x += 5;      // x vaut maintenant 15
x -= 3;      // x vaut maintenant 12
x *= 2;      // x vaut maintenant 24
x /= 4;      // x vaut maintenant 6

let count = 0;
count += 1;  // Incrémenter de 1
```

#### Affectation composée bit à bit

| Opérateur | Nom                        | Exemple     | Équivalent          |
|-----------|----------------------------|-------------|---------------------|
| `&=`      | ET bit à bit et affecter   | `a &= b`    | `a = a & b`         |
| `\|=`     | OU bit à bit et affecter   | `a \|= b`   | `a = a \| b`        |
| `^=`      | XOR bit à bit et affecter  | `a ^= b`    | `a = a ^ b`         |
| `<<=`     | Décaler gauche et affecter | `a <<= b`   | `a = a << b`        |
| `>>=`     | Décaler droite et affecter | `a >>= b`   | `a = a >> b`        |

**Exemples :**
```hemlock
let flags = 0b1111;
flags &= 0b0011;   // flags vaut maintenant 0b0011 (masquer les bits supérieurs)
flags |= 0b1000;   // flags vaut maintenant 0b1011 (activer un bit)
flags ^= 0b0001;   // flags vaut maintenant 0b1010 (basculer un bit)

let x = 1;
x <<= 4;           // x vaut maintenant 16 (décaler à gauche de 4)
x >>= 2;           // x vaut maintenant 4 (décaler à droite de 2)
```

### Incrémentation/Décrémentation

| Opérateur | Nom           | Exemple | Description                    |
|-----------|---------------|---------|--------------------------------|
| `++`      | Incrémentation| `a++`   | Incrémenter de 1 (postfixe)    |
| `--`      | Décrémentation| `a--`   | Décrémenter de 1 (postfixe)    |

**Exemples :**
```hemlock
let i = 0;
i++;         // i vaut maintenant 1
i++;         // i vaut maintenant 2
i--;         // i vaut maintenant 1

// Courant dans les boucles
for (let j = 0; j < 10; j++) {
    print(j);
}
```

**Note :** `++` et `--` sont des opérateurs postfixes (la valeur est retournée avant l'incrémentation/décrémentation)

---

## Opérateurs de sécurité null

### Coalescence null (`??`)

Retourne l'opérande gauche s'il n'est pas null, sinon retourne l'opérande droit.

| Opérateur | Nom              | Exemple      | Description                      |
|-----------|------------------|--------------|----------------------------------|
| `??`      | Coalescence null | `a ?? b`     | Retourner a si non null, sinon b |

**Exemples :**
```hemlock
let name = null;
let display = name ?? "Anonyme";  // "Anonyme"

let value = 42;
let result = value ?? 0;            // 42

// Chaînage
let a = null;
let b = null;
let c = "trouvé";
let result2 = a ?? b ?? c;          // "trouvé"

// Avec des appels de fonction
fn get_config() { return null; }
let config = get_config() ?? { default: true };
```

---

### Chaînage optionnel (`?.`)

Accède en toute sécurité aux propriétés ou appelle des méthodes sur des valeurs potentiellement null.

| Opérateur | Nom                 | Exemple        | Description                           |
|-----------|---------------------|----------------|---------------------------------------|
| `?.`      | Chaînage optionnel  | `a?.b`         | Retourner a.b si a non null, sinon null |
| `?.[`     | Index optionnel     | `a?.[0]`       | Retourner a[0] si a non null, sinon null |
| `?.(`     | Appel optionnel     | `a?.()`        | Appeler a() si a non null, sinon null |

**Exemples :**
```hemlock
let user = null;
let name = user?.name;              // null (pas d'erreur)

let person = { name: "Alice", address: null };
let city = person?.address?.city;   // null (navigation sûre)

// Avec des tableaux
let arr = null;
let first = arr?.[0];               // null

let items = [1, 2, 3];
let second = items?.[1];            // 2

// Avec des appels de méthode
let obj = { greet: fn() { return "Hello"; } };
let greeting = obj?.greet?.();      // "Hello"

let empty = null;
let result = empty?.method?.();     // null
```

**Comportement :**
- Si l'opérande gauche est null, toute l'expression court-circuite vers null
- Si l'opérande gauche n'est pas null, l'accès se poursuit normalement
- Peut être chaîné pour un accès profond aux propriétés

---

## Opérateurs d'accès aux membres

### Opérateur point

| Opérateur | Nom                | Exemple      | Description              |
|-----------|--------------------|--------------|--------------------------|
| `.`       | Accès membre       | `obj.field`  | Accéder au champ objet   |
| `.`       | Accès propriété    | `arr.length` | Accéder à la propriété   |

**Exemples :**
```hemlock
// Accès au champ objet
let person = { name: "Alice", age: 30 };
print(person.name);        // "Alice"

// Propriété de tableau
let arr = [1, 2, 3];
print(arr.length);         // 3

// Propriété de chaîne
let s = "hello";
print(s.length);           // 5

// Appel de méthode
let result = s.to_upper(); // "HELLO"
```

---

### Opérateur d'index

| Opérateur | Nom    | Exemple   | Description           |
|-----------|--------|-----------|----------------------|
| `[]`      | Index  | `arr[i]`  | Accéder à l'élément  |

**Exemples :**
```hemlock
// Indexation de tableau
let arr = [10, 20, 30];
print(arr[0]);             // 10
arr[1] = 99;

// Indexation de chaîne (retourne un rune)
let s = "hello";
print(s[0]);               // 'h'
s[0] = 'H';                // "Hello"

// Indexation de buffer
let buf = buffer(10);
buf[0] = 65;
print(buf[0]);             // 65
```

---

## Opérateur d'appel de fonction

| Opérateur | Nom              | Exemple      | Description         |
|-----------|------------------|--------------|---------------------|
| `()`      | Appel de fonction| `f(a, b)`    | Appeler la fonction |

**Exemples :**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(5, 3);    // 8

// Appel de méthode
let s = "hello";
let upper = s.to_upper();  // "HELLO"

// Appel de fonction intégrée
print("message");
```

---

## Priorité des opérateurs

Les opérateurs sont listés de la plus haute à la plus basse priorité :

| Priorité | Opérateurs                   | Description                         | Associativité   |
|----------|------------------------------|-------------------------------------|-----------------|
| 1        | `()` `[]` `.` `?.`           | Appel, index, accès membre, chaînage optionnel | Gauche à droite |
| 2        | `++` `--`                    | Incrémentation/décrémentation postfixe | Gauche à droite |
| 3        | `!` `~` `-` (unaire) `+` (unaire) | NON logique, NON bit à bit, négation | Droite à gauche |
| 4        | `*` `/` `%`                  | Multiplication, division, modulo    | Gauche à droite |
| 5        | `+` `-`                      | Addition, soustraction              | Gauche à droite |
| 6        | `<<` `>>`                    | Décalages de bits                   | Gauche à droite |
| 7        | `<` `<=` `>` `>=`            | Relationnel                         | Gauche à droite |
| 8        | `==` `!=`                    | Égalité                             | Gauche à droite |
| 9        | `&`                          | ET bit à bit                        | Gauche à droite |
| 10       | `^`                          | XOR bit à bit                       | Gauche à droite |
| 11       | `|`                          | OU bit à bit                        | Gauche à droite |
| 12       | `&&`                         | ET logique                          | Gauche à droite |
| 13       | `||`                         | OU logique                          | Gauche à droite |
| 14       | `??`                         | Coalescence null                    | Gauche à droite |
| 15       | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | Affectation | Droite à gauche |

---

## Exemples de priorité

### Exemple 1 : Arithmétique et comparaison
```hemlock
let result = 5 + 3 * 2;
// Évalué comme : 5 + (3 * 2) = 11
// La multiplication a une priorité plus élevée que l'addition

let cmp = 10 > 5 + 3;
// Évalué comme : 10 > (5 + 3) = true
// L'addition a une priorité plus élevée que la comparaison
```

### Exemple 2 : Opérateurs bit à bit
```hemlock
let result1 = 12 | 10 & 8;
// Évalué comme : 12 | (10 & 8) = 12 | 8 = 12
// & a une priorité plus élevée que |

let result2 = 8 | 1 << 2;
// Évalué comme : 8 | (1 << 2) = 8 | 4 = 12
// Le décalage a une priorité plus élevée que le OU bit à bit

// Utiliser des parenthèses pour la clarté
let result3 = (5 & 3) | (2 << 1);
// Évalué comme : 1 | 4 = 5
```

### Exemple 3 : Opérateurs logiques
```hemlock
let result = true || false && false;
// Évalué comme : true || (false && false) = true
// && a une priorité plus élevée que ||

let cmp = 5 < 10 && 10 < 20;
// Évalué comme : (5 < 10) && (10 < 20) = true
// La comparaison a une priorité plus élevée que &&
```

### Exemple 4 : Utilisation de parenthèses
```hemlock
// Sans parenthèses
let a = 2 + 3 * 4;        // 14

// Avec parenthèses
let b = (2 + 3) * 4;      // 20

// Expression complexe
let c = (a + b) * (a - b);
```

---

## Comportement des opérateurs spécifiques aux types

### Division (toujours flottante)

L'opérateur `/` **retourne toujours un flottant** (f64), quel que soit le type des opérandes :

```hemlock
print(10 / 3);             // 3.333... (f64)
print(5 / 2);              // 2.5 (f64)
print(10.0 / 4.0);         // 2.5 (f64)
print(-7 / 3);             // -2.333... (f64)
```

Cela évite le bug courant de troncature entière inattendue.

### Division entière (div / divi)

Pour la division entière (comme la division entière dans d'autres langages), utilisez les fonctions `div()` et `divi()` :

```hemlock
// div(a, b) - division entière retournant un flottant
print(div(5, 2));          // 2 (f64)
print(div(-7, 3));         // -3 (f64)  -- arrondit vers -infini

// divi(a, b) - division entière retournant un entier
print(divi(5, 2));         // 2 (i64)
print(divi(-7, 3));        // -3 (i64)
print(typeof(divi(5, 2))); // i64
```

**Fonctions mathématiques retournant des entiers :**
Pour d'autres opérations d'arrondi qui retournent des entiers :

```hemlock
print(floori(3.7));        // 3 (i64)
print(ceili(3.2));         // 4 (i64)
print(roundi(3.5));        // 4 (i64)
print(trunci(3.9));        // 3 (i64)

// Ceux-ci peuvent être utilisés directement comme indices de tableau
let arr = [10, 20, 30, 40];
print(arr[floori(1.9)]);   // 20 (index 1)
```

### Comparaison de chaînes

Les chaînes sont comparées lexicographiquement :

```hemlock
print("abc" < "def");      // true
print("apple" > "banana"); // false
print("hello" == "hello"); // true
```

### Comparaison null

```hemlock
let x = null;

print(x == null);          // true
print(x != null);          // false
```

### Erreurs de type

Certaines opérations ne sont pas autorisées entre types incompatibles :

```hemlock
// ERREUR : Impossible d'utiliser les opérateurs bit à bit sur les flottants
let x = 3.14 & 2.71;

// ERREUR : Impossible d'utiliser les opérateurs bit à bit sur les chaînes
let y = "hello" & "world";

// OK : Promotion de type pour l'arithmétique
let a: u8 = 10;
let b: i32 = 20;
let c = a + b;             // i32 (promu)
```

---

## Voir aussi

- [Système de types](type-system.md) - Règles de promotion et conversion de types
- [Fonctions intégrées](builtins.md) - Opérations intégrées
- [API String](string-api.md) - Concaténation et méthodes de chaînes
