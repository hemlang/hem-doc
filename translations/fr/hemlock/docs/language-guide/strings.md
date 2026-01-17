# Chaines

Les chaines Hemlock sont des **sequences mutables UTF-8 de premiere classe** avec un support Unicode complet et un ensemble riche de methodes pour le traitement de texte. Contrairement a de nombreux langages, les chaines Hemlock sont mutables et fonctionnent nativement avec les points de code Unicode.

## Apercu

```hemlock
let s = "hello";
s[0] = 'H';             // muter avec rune (maintenant "Hello")
print(s.length);        // 5 (compte de points de code)
let c = s[0];           // retourne rune (point de code Unicode)
let msg = s + " world"; // concatenation
let emoji = "rocket";
print(emoji.length);    // 1 (un point de code)
print(emoji.byte_length); // 4 (quatre octets UTF-8)
```

## Proprietes

Les chaines Hemlock ont ces caracteristiques cles :

- **Encodage UTF-8** - Support Unicode complet (U+0000 a U+10FFFF)
- **Mutable** - Contrairement aux chaines Python, JavaScript et Java
- **Indexation basee sur les points de code** - Retourne `rune` (point de code Unicode), pas un octet
- **Allouee sur le tas** - Avec suivi de capacite interne
- **Deux proprietes de longueur** :
  - `.length` - Compte de points de code (nombre de caracteres)
  - `.byte_length` - Compte d'octets (taille d'encodage UTF-8)

## Comportement UTF-8

Toutes les operations sur les chaines fonctionnent avec les **points de code** (caracteres), pas les octets :

```hemlock
let text = "Helloworld";
print(text.length);        // 11 (points de code)
print(text.byte_length);   // 15 (octets, emoji fait 4 octets)

// L'indexation utilise les points de code
let h = text[0];           // 'H' (rune)
let rocket = text[5];      // 'rocket' (rune)
```

**Les caracteres multi-octets comptent comme un :**
```hemlock
"Hello".length;      // 5
"rocket".length;     // 1 (un emoji)
"ni hao".length;     // 2 (deux caracteres chinois)
"cafe".length;       // 4 (e est un point de code)
```

## Litteraux de chaine

```hemlock
// Chaines basiques
let s1 = "hello";
let s2 = "world";

// Avec sequences d'echappement
let s3 = "Ligne 1\nLigne 2\ttabulation";
let s4 = "Citation: \"Bonjour\"";
let s5 = "Antislash: \\";

// Caracteres Unicode
let s6 = "rocket Emoji";
let s7 = "zhongwen zifu";
```

## Chaines de modele (interpolation de chaine)

Utilisez les backticks pour les chaines de modele avec des expressions embarquees :

```hemlock
let name = "Alice";
let age = 30;

// Interpolation basique
let greeting = `Bonjour, ${name}!`;           // "Bonjour, Alice!"
let info = `${name} a ${age} ans`;            // "Alice a 30 ans"

// Expressions dans l'interpolation
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;           // "5 + 10 = 15"

// Appels de methode
let upper = `Nom: ${name.to_upper()}`;        // "Nom: ALICE"

// Objets imbriques
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} vit a ${person.city}`;  // "Bob vit a NYC"

// Multi-lignes (preserve les sauts de ligne)
let multi = `Ligne 1
Ligne 2
Ligne 3`;
```

**Fonctionnalites des chaines de modele :**
- Les expressions dans `${...}` sont evaluees et converties en chaines
- Toute expression valide peut etre utilisee (variables, appels de fonction, arithmetique)
- Les chaines backtick supportent les memes sequences d'echappement que les chaines regulieres
- Utile pour construire des chaines dynamiques sans concatenation

### Echappement dans les chaines de modele

Pour inclure un litteral `${` dans une chaine de modele, echappez le signe dollar :

```hemlock
let price = 100;
let text = `Prix: \${price} ou ${price}`;
// "Prix: ${price} ou 100"

// Backtick litteral
let code = `Utilisez \` pour les chaines de modele`;
// "Utilisez ` pour les chaines de modele"
```

### Expressions complexes

Les chaines de modele peuvent contenir n'importe quelle expression valide :

```hemlock
// Expressions ternaires
let age = 25;
let status = `Statut: ${age >= 18 ? "adulte" : "mineur"}`;

// Acces tableau
let items = ["pomme", "banane", "cerise"];
let first = `Premier element: ${items[0]}`;

// Appels de fonction avec arguments
fn format_price(p) { return p + " EUR"; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: 99.99 EUR"

// Appels de methode chaines
let name = "alice";
let formatted = `Bonjour, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Bonjour, Alice!"
```

### Chaines de modele vs concatenation

Les chaines de modele sont souvent plus claires que la concatenation :

```hemlock
// Concatenation (plus difficile a lire)
let msg1 = "Bonjour, " + name + "! Vous avez " + count + " messages.";

// Chaine de modele (plus facile a lire)
let msg2 = `Bonjour, ${name}! Vous avez ${count} messages.`;
```

## Indexation et mutation

### Lecture de caracteres

L'indexation retourne une `rune` (point de code Unicode) :

```hemlock
let s = "Hello";
let first = s[0];      // 'H' (rune)
let last = s[4];       // 'o' (rune)

// Exemple UTF-8
let emoji = "Hi!";
let rocket = emoji[2];  // 'rocket' (rune a l'index de point de code 2)
```

### Ecriture de caracteres

Les chaines sont mutables - vous pouvez modifier des caracteres individuels :

```hemlock
let s = "hello";
s[0] = 'H';            // Maintenant "Hello"
s[4] = '!';            // Maintenant "Hell!"

// Avec Unicode
let msg = "Go!";
msg[0] = 'rocket';     // Maintenant "rocketo!"
```

## Concatenation

Utilisez `+` pour concatener les chaines :

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// Avec variables
let name = "Alice";
let msg = "Salut, " + name + "!";  // "Salut, Alice!"

// Avec runes (voir documentation Runes)
let s = "Hello" + '!';          // "Hello!"
```

## Methodes de chaine

Hemlock fournit 19 methodes de chaine pour une manipulation de texte complete.

### Sous-chaine et decoupage

**`substr(start, length)`** - Extraire une sous-chaine par position et longueur :
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world" (commence a 6, longueur 5)
let first = s.substr(0, 5);     // "hello"

// Exemple UTF-8
let text = "Hirocket!";
let emoji = text.substr(2, 1);  // "rocket" (position 2, longueur 1)
```

**`slice(start, end)`** - Extraire une sous-chaine par plage (fin exclusive) :
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello" (index 0 a 4)
let slice2 = s.slice(6, 11);    // "world"
```

**Difference :**
- `substr(start, length)` - Utilise le parametre longueur
- `slice(start, end)` - Utilise l'index de fin (exclusive)

### Recherche

**`find(needle)`** - Trouver la premiere occurrence :
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6 (index de premiere occurrence)
let pos2 = s.find("foo");       // -1 (non trouve)
let pos3 = s.find("l");         // 2 (premier 'l')
```

**`contains(needle)`** - Verifier si la chaine contient une sous-chaine :
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### Decoupage et nettoyage

**`split(delimiter)`** - Decouper en tableau de chaines :
```hemlock
let csv = "pomme,banane,cerise";
let parts = csv.split(",");     // ["pomme", "banane", "cerise"]

let words = "un deux trois".split(" ");  // ["un", "deux", "trois"]

// Delimiteur vide decoupe par caractere
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Supprimer les espaces de debut et fin :
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntexte\n\t";
let clean2 = s2.trim();         // "texte"
```

### Conversion de casse

**`to_upper()`** - Convertir en majuscules :
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// Preserve les non-ASCII
let s2 = "cafe";
let upper2 = s2.to_upper();     // "CAFE"
```

**`to_lower()`** - Convertir en minuscules :
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### Verification de prefixe/suffixe

**`starts_with(prefix)`** - Verifier si commence par le prefixe :
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - Verifier si finit par le suffixe :
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### Remplacement

**`replace(old, new)`** - Remplacer la premiere occurrence :
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (premier seulement)
```

**`replace_all(old, new)`** - Remplacer toutes les occurrences :
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### Repetition

**`repeat(count)`** - Repeter la chaine n fois :
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### Acces caractere et octet

**`char_at(index)`** - Obtenir le point de code Unicode a l'index (retourne rune) :
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h' (rune)

// Exemple UTF-8
let emoji = "rocket";
let rocket = emoji.char_at(0);  // Retourne rune U+1F680
```

**`chars()`** - Convertir en tableau de runes (points de code) :
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o'] (tableau de runes)

// Exemple UTF-8
let text = "Hirocket";
let chars2 = text.chars();      // ['H', 'i', 'rocket']
```

**`byte_at(index)`** - Obtenir la valeur d'octet a l'index (retourne u8) :
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (valeur ASCII de 'h')

// Exemple UTF-8
let emoji = "rocket";
let first_byte = emoji.byte_at(0);  // 240 (premier octet UTF-8)
```

**`bytes()`** - Convertir en tableau d'octets (valeurs u8) :
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111] (tableau de u8)

// Exemple UTF-8
let emoji = "rocket";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 octets UTF-8)
```

**`to_bytes()`** - Convertir en buffer pour acces bas niveau :
```hemlock
let s = "hello";
let buf = s.to_bytes();         // Retourne buffer avec octets UTF-8
print(buf.length);              // 5
free(buf);                      // N'oubliez pas de liberer
```

## Chainage de methodes

Toutes les methodes de chaine retournent de nouvelles chaines, permettant le chainage :

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## Reference complete des methodes

| Methode | Parametres | Retourne | Description |
|---------|------------|----------|-------------|
| `substr(start, length)` | i32, i32 | string | Extraire sous-chaine par position et longueur |
| `slice(start, end)` | i32, i32 | string | Extraire sous-chaine par plage (fin exclusive) |
| `find(needle)` | string | i32 | Trouver premiere occurrence (-1 si non trouve) |
| `contains(needle)` | string | bool | Verifier si contient sous-chaine |
| `split(delimiter)` | string | array | Decouper en tableau de chaines |
| `trim()` | - | string | Supprimer espaces debut/fin |
| `to_upper()` | - | string | Convertir en majuscules |
| `to_lower()` | - | string | Convertir en minuscules |
| `starts_with(prefix)` | string | bool | Verifier si commence par prefixe |
| `ends_with(suffix)` | string | bool | Verifier si finit par suffixe |
| `replace(old, new)` | string, string | string | Remplacer premiere occurrence |
| `replace_all(old, new)` | string, string | string | Remplacer toutes occurrences |
| `repeat(count)` | i32 | string | Repeter chaine n fois |
| `char_at(index)` | i32 | rune | Obtenir point de code a l'index |
| `byte_at(index)` | i32 | u8 | Obtenir valeur d'octet a l'index |
| `chars()` | - | array | Convertir en tableau de runes |
| `bytes()` | - | array | Convertir en tableau d'octets u8 |
| `to_bytes()` | - | buffer | Convertir en buffer (doit liberer) |

## Exemples

### Exemple : Traitement de texte

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Normaliser les espaces
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### Exemple : Analyseur CSV

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "pomme, banane , cerise";
let fields = parse_csv_line(csv);  // ["pomme", "banane", "cerise"]
```

### Exemple : Compteur de mots

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "Le rapide renard brun";
let count = count_words(sentence);  // 4
```

### Exemple : Validation de chaine

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## Gestion de la memoire

Les chaines sont allouees sur le tas avec comptage de reference interne :

- **Creation** : Allouee sur le tas avec suivi de capacite
- **Concatenation** : Cree une nouvelle chaine (anciennes chaines inchangees)
- **Methodes** : La plupart des methodes retournent de nouvelles chaines
- **Duree de vie** : Les chaines sont comptees par reference et automatiquement liberees quand la portee se termine

**Nettoyage automatique :**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // Nouvelle allocation
}  // s et s2 sont automatiquement liberes quand la fonction retourne
```

**Note :** Les variables de chaine locales sont automatiquement nettoyees quand elles sortent de la portee. Utilisez `free()` uniquement pour le nettoyage anticipe avant la fin de portee ou pour les donnees globales/longue duree. Voir [Gestion de la memoire](memory.md#internal-reference-counting) pour les details.

## Bonnes pratiques

1. **Utilisez l'indexation par point de code** - Les chaines utilisent les positions de point de code, pas les decalages d'octets
2. **Testez avec Unicode** - Testez toujours les operations sur chaines avec des caracteres multi-octets
3. **Preferez les operations immuables** - Utilisez les methodes qui retournent de nouvelles chaines plutot que la mutation
4. **Verifiez les limites** - L'indexation de chaine ne verifie pas les limites (retourne null/erreur si invalide)
5. **Normalisez l'entree** - Utilisez `trim()` et `to_lower()` pour l'entree utilisateur

## Pieges courants

### Piege : Confusion octet vs. point de code

```hemlock
let emoji = "rocket";
print(emoji.length);        // 1 (point de code)
print(emoji.byte_length);   // 4 (octets)

// Ne melangez pas les operations octet et point de code
let byte = emoji.byte_at(0);  // 240 (premier octet)
let char = emoji.char_at(0);  // 'rocket' (point de code complet)
```

### Piege : Surprises de mutation

```hemlock
let s1 = "hello";
let s2 = s1;       // Copie superficielle
s1[0] = 'H';       // Mute s1
print(s2);         // Toujours "hello" (les chaines sont des types valeur)
```

## Sujets connexes

- [Runes](runes.md) - Type point de code Unicode utilise dans l'indexation de chaine
- [Tableaux](arrays.md) - Les methodes de chaine retournent ou travaillent souvent avec des tableaux
- [Types](types.md) - Details du type chaine et conversions

## Voir aussi

- **Encodage UTF-8** : Voir section "Strings" de CLAUDE.md
- **Conversions de type** : Voir [Types](types.md) pour les conversions de chaine
- **Memoire** : Voir [Memoire](memory.md) pour les details d'allocation de chaine
