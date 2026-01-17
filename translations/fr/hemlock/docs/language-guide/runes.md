# Runes

Les runes representent des **points de code Unicode** (U+0000 a U+10FFFF) comme un type distinct pour la manipulation de caracteres en Hemlock. Contrairement aux octets (u8), les runes sont des caracteres Unicode complets qui peuvent representer n'importe quel caractere dans n'importe quelle langue ou emoji.

## Apercu

```hemlock
let ch = 'A';           // Litteral de rune
let emoji = 'rocket';   // Caractere multi-octet comme rune unique
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // Concatenation chaine + rune
let r = '>' + " msg";   // Concatenation rune + chaine
```

## Qu'est-ce qu'une rune ?

Une rune est une **valeur de 32 bits** representant un point de code Unicode :

- **Plage :** 0 a 0x10FFFF (1 114 111 points de code valides)
- **Pas un type numerique** - Utilisee pour la representation de caracteres
- **Distincte de u8/char** - Les runes sont du plein Unicode, u8 est juste des octets
- **Retournee par l'indexation de chaine** - `str[0]` retourne une rune, pas un octet

**Pourquoi les runes ?**
- Les chaines Hemlock sont encodees en UTF-8
- Un seul caractere Unicode peut faire de 1 a 4 octets en UTF-8
- Les runes permettent de travailler avec des caracteres complets, pas des octets partiels

## Litteraux de rune

### Syntaxe de base

Les guillemets simples denotent les litteraux de rune :

```hemlock
let a = 'A';            // Caractere ASCII
let b = '0';            // Caractere chiffre
let c = '!';            // Ponctuation
let d = ' ';            // Espace
```

### Caracteres UTF-8 multi-octets

Les runes peuvent representer n'importe quel caractere Unicode :

```hemlock
// Emoji
let rocket = 'rocket';  // Emoji (U+1F680)
let heart = 'coeur';    // Coeur (U+2764)
let smile = 'sourire';  // Visage souriant (U+1F600)

// Caracteres CJK
let chinese = 'zhong';  // Chinois (U+4E2D)
let japanese = 'a';     // Hiragana (U+3042)
let korean = 'han';     // Hangul (U+D55C)

// Symboles
let check = 'coche';    // Coche (U+2713)
let arrow = 'fleche';   // Fleche droite (U+2192)
```

### Sequences d'echappement

Sequences d'echappement communes pour les caracteres speciaux :

```hemlock
let newline = '\n';     // Nouvelle ligne (U+000A)
let tab = '\t';         // Tabulation (U+0009)
let backslash = '\\';   // Antislash (U+005C)
let quote = '\'';       // Guillemet simple (U+0027)
let dquote = '"';       // Guillemet double (U+0022)
let null_char = '\0';   // Caractere nul (U+0000)
let cr = '\r';          // Retour chariot (U+000D)
```

**Sequences d'echappement disponibles :**
- `\n` - Nouvelle ligne (saut de ligne)
- `\t` - Tabulation horizontale
- `\r` - Retour chariot
- `\0` - Caractere nul
- `\\` - Antislash
- `\'` - Guillemet simple
- `\"` - Guillemet double

### Echappements Unicode

Utilisez la syntaxe `\u{XXXXXX}` pour les points de code Unicode (jusqu'a 6 chiffres hexadecimaux) :

```hemlock
let rocket = '\u{1F680}';   // Emoji fusee via echappement Unicode
let heart = '\u{2764}';     // Coeur
let ascii = '\u{41}';       // 'A' via echappement
let max = '\u{10FFFF}';     // Point de code Unicode maximum

// Zeros initiaux optionnels
let a = '\u{41}';           // Identique a '\u{0041}'
let b = '\u{0041}';
```

**Regles :**
- Plage : `\u{0}` a `\u{10FFFF}`
- Chiffres hex : 1 a 6 chiffres
- Insensible a la casse : `\u{1F680}` ou `\u{1f680}`
- Les valeurs hors de la plage Unicode valide causent une erreur

## Concatenation chaine + rune

Les runes peuvent etre concatenees avec des chaines :

```hemlock
// Chaine + rune
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Text" + 'coche';   // "Textcoche"

// Rune + chaine
let prefix = '>' + " Message";      // "> Message"
let bullet = 'puce' + " Element";   // "puce Element"

// Concatenations multiples
let msg = "Hi " + 'salut' + " World " + 'terre';  // "Hi salut World terre"

// Le chainage de methodes fonctionne
let result = ('>' + " Important").to_upper();  // "> IMPORTANT"
```

**Fonctionnement :**
- Les runes sont automatiquement encodees en UTF-8
- Converties en chaines pendant la concatenation
- L'operateur de concatenation de chaine gere cela de maniere transparente

## Conversions de type

Les runes peuvent se convertir vers/depuis d'autres types.

### Entier <-> Rune

Convertir entre entiers et runes pour travailler avec les valeurs de point de code :

```hemlock
// Entier vers rune (valeur de point de code)
let code: rune = 65;            // 'A' (ASCII 65)
let emoji_code: rune = 128640;  // U+1F680 (fusee)

// Rune vers entier (obtenir la valeur du point de code)
let r = 'Z';
let value: i32 = r;             // 90 (valeur ASCII)

let rocket = 'fusee';
let code: i32 = rocket;         // 128640 (U+1F680)
```

**Verification de plage :**
- Entier vers rune : Doit etre dans [0, 0x10FFFF]
- Les valeurs hors plage causent une erreur d'execution
- Rune vers entier : Reussit toujours (retourne le point de code)

### Rune -> Chaine

Les runes peuvent etre explicitement converties en chaines :

```hemlock
// Conversion explicite
let ch: string = 'H';           // "H"
let emoji: string = 'fusee';    // "fusee"

// Automatique pendant la concatenation
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8 (octet) -> Rune

Toute valeur u8 (0-255) peut se convertir en rune :

```hemlock
// Plage ASCII (0-127)
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// ASCII etendu / Latin-1 (128-255)
let extended: u8 = 200;
let r: rune = extended;         // U+00C8 (E accent grave)

// Note : Les valeurs 0-127 sont ASCII, 128-255 sont Latin-1
```

### Conversions chainees

Les conversions de type peuvent etre chainees :

```hemlock
// i32 -> rune -> string
let code: i32 = 128512;         // Point de code visage souriant
let r: rune = code;             // sourire
let s: string = r;              // "sourire"

// Tout en une expression
let emoji: string = 128640;     // Implicite i32 -> rune -> string (fusee)
```

## Operations sur les runes

### Affichage

La facon dont les runes sont affichees depend du point de code :

```hemlock
let ascii = 'A';
print(ascii);                   // 'A' (entre guillemets, ASCII imprimable)

let emoji = 'fusee';
print(emoji);                   // U+1F680 (notation Unicode pour non-ASCII)

let tab = '\t';
print(tab);                     // U+0009 (non-imprimable en hex)

let space = ' ';
print(space);                   // ' ' (imprimable)
```

**Format d'affichage :**
- ASCII imprimable (32-126) : Caractere entre guillemets `'A'`
- Non-imprimable ou Unicode : Notation hex `U+XXXX`

### Verification de type

Utilisez `typeof()` pour verifier si une valeur est une rune :

```hemlock
let r = 'fusee';
print(typeof(r));               // "rune"

let s = "text";
let ch = s[0];
print(typeof(ch));              // "rune" (l'indexation retourne des runes)

let num = 65;
print(typeof(num));             // "i32"
```

### Comparaison

Les runes peuvent etre comparees pour l'egalite :

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// Sensible a la casse
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// Les runes peuvent etre comparees avec des entiers (valeurs de point de code)
print(a == 65);                 // true (conversion implicite)
print('fusee' == 128640);       // true
```

**Operateurs de comparaison :**
- `==` - Egal
- `!=` - Different
- `<`, `>`, `<=`, `>=` - Ordre des points de code

```hemlock
print('A' < 'B');               // true (65 < 66)
print('a' > 'Z');               // true (97 > 90)
```

## Travailler avec l'indexation de chaine

L'indexation de chaine retourne des runes, pas des octets :

```hemlock
let s = "Hellofusee";
let h = s[0];                   // 'H' (rune)
let rocket = s[5];              // 'fusee' (rune)

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// Convertir en chaine si necessaire
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "fusee"
```

**Important :** L'indexation de chaine utilise les positions de point de code, pas les decalages d'octets :

```hemlock
let text = "Hifusee!";
// Positions de point de code : 0='H', 1='i', 2='fusee', 3='!'
// Positions d'octet :          0='H', 1='i', 2-5='fusee', 6='!'

let r = text[2];                // 'fusee' (point de code 2)
print(typeof(r));               // "rune"
```

## Exemples

### Exemple : Classification de caracteres

```hemlock
fn is_digit(r: rune): bool {
    return r >= '0' && r <= '9';
}

fn is_upper(r: rune): bool {
    return r >= 'A' && r <= 'Z';
}

fn is_lower(r: rune): bool {
    return r >= 'a' && r <= 'z';
}

print(is_digit('5'));           // true
print(is_upper('A'));           // true
print(is_lower('z'));           // true
```

### Exemple : Conversion de casse

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // Convertir en majuscule (soustraire 32)
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // Convertir en minuscule (ajouter 32)
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### Exemple : Iteration sur les caracteres

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Position " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Hifusee");
// Position 0: 'H'
// Position 1: 'i'
// Position 2: U+1F680
```

### Exemple : Construire des chaines a partir de runes

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let result = "";
    let i = 0;
    while (i < count) {
        result = result + ch;
        i = i + 1;
    }
    return result;
}

let line = repeat_char('=', 40);  // "========================================"
let stars = repeat_char('etoile', 5);  // "etoileetoileetoileetoileetoile"
```

## Modeles courants

### Modele : Filtre de caracteres

```hemlock
fn filter_digits(s: string): string {
    let result = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}

let text = "abc123def456";
let digits = filter_digits(text);  // "123456"
```

### Modele : Comptage de caracteres

```hemlock
fn count_char(s: string, target: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == target) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let text = "hello world";
let l_count = count_char(text, 'l');  // 3
let o_count = count_char(text, 'o');  // 2
```

## Bonnes pratiques

1. **Utilisez les runes pour les operations sur les caracteres** - N'essayez pas de travailler avec des octets pour le texte
2. **L'indexation de chaine retourne des runes** - Rappelez-vous que `str[i]` vous donne une rune
3. **Comparaisons compatibles Unicode** - Les runes gerent n'importe quel caractere Unicode
4. **Convertissez quand necessaire** - Les runes se convertissent facilement en chaines et entiers
5. **Testez avec des emoji** - Testez toujours les operations sur les caracteres avec des caracteres multi-octets

## Pieges courants

### Piege : Confusion rune vs. octet

```hemlock
// NE PAS : Traiter les runes comme des octets
let r: rune = 'fusee';
let b: u8 = r;              // ERREUR : Le point de code 128640 ne tient pas dans u8

// FAIRE : Utiliser les conversions appropriees
let r: rune = 'fusee';
let code: i32 = r;          // OK : 128640
```

### Piege : Indexation d'octet de chaine

```hemlock
// NE PAS : Supposer l'indexation par octet
let s = "fusee";
let byte = s.byte_at(0);    // 240 (premier octet UTF-8, pas le caractere complet)

// FAIRE : Utiliser l'indexation par point de code
let s = "fusee";
let rune = s[0];            // 'fusee' (caractere complet)
let rune2 = s.char_at(0);   // 'fusee' (methode explicite)
```

## Sujets connexes

- [Chaines](strings.md) - Operations sur les chaines et gestion UTF-8
- [Types](types.md) - Systeme de types et conversions
- [Flux de controle](control-flow.md) - Utiliser les runes dans les comparaisons

## Voir aussi

- **Standard Unicode** : Les points de code Unicode sont definis par le Consortium Unicode
- **Encodage UTF-8** : Voir [Chaines](strings.md) pour les details UTF-8
- **Conversions de type** : Voir [Types](types.md) pour les regles de conversion
