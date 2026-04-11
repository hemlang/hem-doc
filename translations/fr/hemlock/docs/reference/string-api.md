# Référence de l'API String

Reference complete pour le type string de Hemlock et ses 22 methodes.

---

## Aperçu

Les chaînes de caractères (strings) dans Hemlock sont des séquences **encodées en UTF-8, mutables, allouées sur le tas** avec support complet d'Unicode. Toutes les opérations fonctionnent avec des **points de code** (caractères), pas des octets.

**Caractéristiques principales :**
- Encodage UTF-8 (U+0000 à U+10FFFF)
- Mutables (peuvent modifier les caractères sur place)
- Indexation basée sur les points de code
- 22 methodes integrees
- Concaténation automatique avec l'opérateur `+`

---

## Type String

**Type :** `string`

**Propriétés :**
- `.length` - Nombre de points de code (caractères)
- `.byte_length` - Nombre d'octets UTF-8

**Syntaxe littérale :** Guillemets doubles `"texte"`

**Exemples :**
```hemlock
let s = "hello";
print(s.length);        // 5 (points de code)
print(s.byte_length);   // 5 (octets)

let emoji = "🚀";
print(emoji.length);        // 1 (un point de code)
print(emoji.byte_length);   // 4 (quatre octets UTF-8)
```

---

## Indexation

Les chaînes supportent l'indexation basée sur les points de code en utilisant `[]` :

**Accès en lecture :**
```hemlock
let s = "hello";
let ch = s[0];          // Retourne le rune 'h'
```

**Accès en écriture :**
```hemlock
let s = "hello";
s[0] = 'H';             // Modifie avec un rune (maintenant "Hello")
```

**Exemple UTF-8 :**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (un point de code)
print(text[3]);         // '!'
```

---

## Concaténation

Utilisez l'opérateur `+` pour concaténer des chaînes et des runes :

**String + String :**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**String + Rune :**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Rune + String :**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**Concaténations multiples :**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## Propriétés des chaînes

### .length

Obtient le nombre de points de code Unicode (caractères).

**Type :** `i32`

**Exemples :**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (un point de code)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 emoji)
```

---

### .byte_length

Obtient le nombre d'octets UTF-8.

**Type :** `i32`

**Exemples :**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 octet par caractère ASCII)

let emoji = "🚀";
print(emoji.byte_length); // 4 (l'emoji fait 4 octets UTF-8)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 pour l'emoji)
```

---

## Méthodes des chaînes

### Sous-chaîne et découpage

#### substr

Extrait une sous-chaîne par position et longueur.

**Signature :**
```hemlock
string.substr(start: i32, length: i32): string
```

**Paramètres :**
- `start` - Index du point de code de départ (base 0)
- `length` - Nombre de points de code à extraire

**Retourne :** Nouvelle chaîne

**Exemples :**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// Exemple UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

Extrait une sous-chaîne par plage (fin exclusive).

**Signature :**
```hemlock
string.slice(start: i32, end: i32): string
```

**Paramètres :**
- `start` - Index du point de code de départ (base 0)
- `end` - Index du point de code de fin (exclusif)

**Retourne :** Nouvelle chaîne

**Exemples :**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// Exemple UTF-8
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### Recherche

#### find

Trouve la première occurrence d'une sous-chaîne.

**Signature :**
```hemlock
string.find(needle: string): i32
```

**Paramètres :**
- `needle` - Sous-chaîne à rechercher

**Retourne :** Index du point de code de la première occurrence, ou `-1` si non trouvée

**Exemples :**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (non trouvée)
let pos3 = s.find("l");         // 2 (premier 'l')
```

---

#### contains

Vérifie si la chaîne contient une sous-chaîne.

**Signature :**
```hemlock
string.contains(needle: string): bool
```

**Paramètres :**
- `needle` - Sous-chaîne à rechercher

**Retourne :** `true` si trouvée, `false` sinon

**Exemples :**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### Séparation et jonction

#### split

Sépare la chaîne en un tableau par délimiteur.

**Signature :**
```hemlock
string.split(delimiter: string): array
```

**Paramètres :**
- `delimiter` - Chaîne sur laquelle séparer

**Retourne :** Tableau de chaînes

**Exemples :**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

Supprime les espaces blancs au début et à la fin.

**Signature :**
```hemlock
string.trim(): string
```

**Retourne :** Nouvelle chaîne sans espaces blancs

**Exemples :**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

#### trim_start

Supprime les espaces blancs au debut uniquement.

**Signature :**
```hemlock
string.trim_start(): string
```

**Retourne :** Nouvelle chaine sans espaces blancs au debut

**Exemples :**
```hemlock
let s = "  hello  ";
let clean = s.trim_start();     // "hello  "

let text = "\n\t  world  \n";
let clean2 = text.trim_start(); // "world  \n"
```

#### trim_end

Supprime les espaces blancs a la fin uniquement.

**Signature :**
```hemlock
string.trim_end(): string
```

**Retourne :** Nouvelle chaine sans espaces blancs a la fin

**Exemples :**
```hemlock
let s = "  hello  ";
let clean = s.trim_end();       // "  hello"

let text = "\n\t  world  \n";
let clean2 = text.trim_end();   // "\n\t  world"
```

---

### Conversion de casse

#### to_upper

Convertit la chaîne en majuscules.

**Signature :**
```hemlock
string.to_upper(): string
```

**Retourne :** Nouvelle chaîne en majuscules

**Exemples :**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

Convertit la chaîne en minuscules.

**Signature :**
```hemlock
string.to_lower(): string
```

**Retourne :** Nouvelle chaîne en minuscules

**Exemples :**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### Préfixe et suffixe

#### starts_with

Vérifie si la chaîne commence par un préfixe.

**Signature :**
```hemlock
string.starts_with(prefix: string): bool
```

**Paramètres :**
- `prefix` - Préfixe à vérifier

**Retourne :** `true` si la chaîne commence par le préfixe, `false` sinon

**Exemples :**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

Vérifie si la chaîne se termine par un suffixe.

**Signature :**
```hemlock
string.ends_with(suffix: string): bool
```

**Paramètres :**
- `suffix` - Suffixe à vérifier

**Retourne :** `true` si la chaîne se termine par le suffixe, `false` sinon

**Exemples :**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### Remplacement

#### replace

Remplace la première occurrence d'une sous-chaîne.

**Signature :**
```hemlock
string.replace(old: string, new: string): string
```

**Paramètres :**
- `old` - Sous-chaîne à remplacer
- `new` - Chaîne de remplacement

**Retourne :** Nouvelle chaîne avec la première occurrence remplacée

**Exemples :**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (seulement la première)
```

---

#### replace_all

Remplace toutes les occurrences d'une sous-chaîne.

**Signature :**
```hemlock
string.replace_all(old: string, new: string): string
```

**Paramètres :**
- `old` - Sous-chaîne à remplacer
- `new` - Chaîne de remplacement

**Retourne :** Nouvelle chaîne avec toutes les occurrences remplacées

**Exemples :**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### Répétition

#### repeat

Répète la chaîne n fois.

**Signature :**
```hemlock
string.repeat(count: i32): string
```

**Paramètres :**
- `count` - Nombre de répétitions

**Retourne :** Nouvelle chaîne répétée count fois

**Exemples :**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### Accès aux caractères

#### char_at

Obtient le point de code Unicode à l'index.

**Signature :**
```hemlock
string.char_at(index: i32): rune
```

**Paramètres :**
- `index` - Index du point de code (base 0)

**Retourne :** Rune (point de code Unicode)

**Exemples :**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// Exemple UTF-8
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (fusée)
```

---

#### chars

Convertit la chaîne en tableau de runes.

**Signature :**
```hemlock
string.chars(): array
```

**Retourne :** Tableau de runes (points de code)

**Exemples :**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// Exemple UTF-8
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### Accès aux octets

#### byte_at

Obtient la valeur de l'octet à l'index.

**Signature :**
```hemlock
string.byte_at(index: i32): u8
```

**Paramètres :**
- `index` - Index de l'octet (base 0, PAS l'index du point de code)

**Retourne :** Valeur de l'octet (u8)

**Exemples :**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// Exemple UTF-8
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (premier octet UTF-8)
```

---

#### bytes

Convertit la chaîne en tableau d'octets.

**Signature :**
```hemlock
string.bytes(): array
```

**Retourne :** Tableau d'octets u8

**Exemples :**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// Exemple UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 octets UTF-8)
```

---

#### to_bytes

Convertit la chaîne en buffer.

**Signature :**
```hemlock
string.to_bytes(): buffer
```

**Retourne :** Buffer contenant les octets UTF-8

**Exemples :**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// Exemple UTF-8
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Note :** Ceci est une methode heritee. Preferez `.bytes()` pour la plupart des cas d'utilisation.

---

### Acces au pointeur brut

#### byte_ptr

Obtient un pointeur brut vers le buffer interne d'octets UTF-8 de la chaine. C'est une operation sans allocation -- aucune copie n'est faite.

**Signature :**
```hemlock
string.byte_ptr(): ptr
```

**Retourne :** Pointeur brut (`ptr`) vers les octets UTF-8 internes de la chaine

**Exemples :**
```hemlock
let s = "Hello";
let p = s.byte_ptr();
print(typeof(p));              // "ptr"

// Lire les octets via le pointeur
print(ptr_deref_u8(p));                    // 72 ('H')
print(ptr_deref_u8(ptr_offset(p, 1, 1))); // 101 ('e')
print(ptr_deref_u8(ptr_offset(p, 4, 1))); // 111 ('o')

// Utiliser avec memcpy pour copier les octets de la chaine
let buf = alloc(5);
memcpy(buf, s.byte_ptr(), 5);
print(ptr_deref_u8(buf));  // 72
free(buf);

// Associer avec .byte_length pour un suivi de taille securise
let emoji = "Hello 🚀";
let ep = emoji.byte_ptr();
print(emoji.byte_length);  // 10 (utiliser byte_length, pas length, pour les operations en octets)
```

**Comportement :**
- Retourne un pointeur directement dans la memoire interne de la chaine (zero-copie)
- Le pointeur est valide tant que la chaine est vivante et non modifiee
- Utilisez `.byte_length` (pas `.length`) pour determiner le nombre d'octets accessibles via le pointeur
- Contrairement a `.to_bytes()`, ceci n'alloue pas un nouveau buffer

**Cas d'utilisation :**
- Appels FFI necessitant un pointeur vers les donnees de la chaine
- Interoperabilite zero-copie avec les fonctions C
- Code critique en performance qui evite les allocations

**Avertissement :** Modifier la chaine (par ex., affectation par index) apres avoir appele `byte_ptr()` peut invalider le pointeur si le buffer interne de la chaine est realloue.

---

### Deserialisation JSON

#### deserialize

Parse une chaîne JSON en valeur.

**Signature :**
```hemlock
string.deserialize(): any
```

**Retourne :** Valeur parsée (objet, tableau, nombre, chaîne, bool ou null)

**Exemples :**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**Types supportés :**
- Objets : `{"key": value}`
- Tableaux : `[1, 2, 3]`
- Nombres : `42`, `3.14`
- Chaînes : `"text"`
- Booléens : `true`, `false`
- Null : `null`

**Voir aussi :** Méthode `.serialize()` des objets

---

## Chaînage de méthodes

Les méthodes de chaînes peuvent être chaînées pour des opérations concises :

**Exemples :**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## Résumé complet des méthodes

| Méthode        | Signature                                    | Retourne  | Description                                |
|----------------|----------------------------------------------|-----------|-------------------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`  | Extraire sous-chaîne par position/longueur |
| `slice`        | `(start: i32, end: i32)`                     | `string`  | Extraire sous-chaîne par plage             |
| `find`         | `(needle: string)`                           | `i32`     | Trouver première occurrence (-1 si non trouvée) |
| `contains`     | `(needle: string)`                           | `bool`    | Vérifier si contient sous-chaîne           |
| `split`        | `(delimiter: string)`                        | `array`   | Séparer en tableau                         |
| `trim`         | `()`                                         | `string`  | Supprimer espaces blancs                   |
| `trim_start`   | `()`                                         | `string`  | Supprimer espaces blancs au debut          |
| `trim_end`     | `()`                                         | `string`  | Supprimer espaces blancs a la fin          |
| `to_upper`     | `()`                                         | `string`  | Convertir en majuscules                    |
| `to_lower`     | `()`                                         | `string`  | Convertir en minuscules                    |
| `starts_with`  | `(prefix: string)`                           | `bool`    | Vérifier si commence par préfixe           |
| `ends_with`    | `(suffix: string)`                           | `bool`    | Vérifier si termine par suffixe            |
| `replace`      | `(old: string, new: string)`                 | `string`  | Remplacer première occurrence              |
| `replace_all`  | `(old: string, new: string)`                 | `string`  | Remplacer toutes les occurrences           |
| `repeat`       | `(count: i32)`                               | `string`  | Répéter chaîne n fois                      |
| `char_at`      | `(index: i32)`                               | `rune`    | Obtenir point de code à l'index            |
| `byte_at`      | `(index: i32)`                               | `u8`      | Obtenir octet à l'index                    |
| `chars`        | `()`                                         | `array`   | Convertir en tableau de runes              |
| `bytes`        | `()`                                         | `array`   | Convertir en tableau d'octets              |
| `to_bytes`     | `()`                                         | `buffer`  | Convertir en buffer (herite)               |
| `byte_ptr`     | `()`                                         | `ptr`     | Pointeur brut vers les octets UTF-8 internes |
| `deserialize`  | `()`                                         | `any`     | Parser chaine JSON                         |

---

## Voir aussi

- [Système de types](type-system.md) - Détails sur le type string
- [API Array](array-api.md) - Méthodes de tableau pour les résultats de split()
- [Opérateurs](operators.md) - Opérateur de concaténation de chaînes
