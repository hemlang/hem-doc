# Flux de controle

Hemlock fournit un flux de controle familier de style C avec des accolades obligatoires et une syntaxe explicite. Ce guide couvre les conditionnelles, les boucles, les instructions switch et les operateurs.

## Apercu

Fonctionnalites de flux de controle disponibles :

- `if`/`else`/`else if` - Branches conditionnelles
- Boucles `while` - Iteration basee sur condition
- Boucles `for` - Style C et iteration for-in
- `loop` - Boucles infinies (plus propre que `while (true)`)
- Instructions `switch` - Branchement multi-voies
- `break`/`continue` - Controle de boucle
- Labels de boucle - break/continue cible pour les boucles imbriquees
- `defer` - Execution differee (nettoyage)
- Operateurs booleens : `&&`, `||`, `!`
- Operateurs de comparaison : `==`, `!=`, `<`, `>`, `<=`, `>=`
- Operateurs binaires : `&`, `|`, `^`, `<<`, `>>`, `~`

## Instructions If

### If/Else basique

```hemlock
if (x > 10) {
    print("grand");
} else {
    print("petit");
}
```

**Regles :**
- Les accolades sont **toujours requises** pour toutes les branches
- Les conditions doivent etre entre parentheses
- Pas d'accolades optionnelles (contrairement au C)

### If sans Else

```hemlock
if (x > 0) {
    print("positif");
}
// Pas de branche else necessaire
```

### Chaines Else-If

```hemlock
if (x > 100) {
    print("tres grand");
} else if (x > 50) {
    print("grand");
} else if (x > 10) {
    print("moyen");
} else {
    print("petit");
}
```

**Note :** `else if` est du sucre syntaxique pour des instructions if imbriquees. Ces deux sont equivalents :

```hemlock
// else if (sucre syntaxique)
if (a) {
    foo();
} else if (b) {
    bar();
}

// If imbrique equivalent
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### Instructions If imbriquees

```hemlock
if (x > 0) {
    if (x < 10) {
        print("chiffre positif");
    } else {
        print("positif multi-chiffres");
    }
} else {
    print("non-positif");
}
```

## Boucles While

Iteration basee sur condition :

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**Boucles infinies (ancien style) :**
```hemlock
while (true) {
    // ... faire le travail
    if (should_exit) {
        break;
    }
}
```

**Note :** Pour les boucles infinies, preferez le mot-cle `loop` (voir ci-dessous).

## Loop (boucle infinie)

Le mot-cle `loop` fournit une syntaxe plus propre pour les boucles infinies :

```hemlock
loop {
    // ... faire le travail
    if (should_exit) {
        break;
    }
}
```

**Equivalent a `while (true)` mais plus explicite sur l'intention.**

### Loop basique avec Break

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Affiche : 0, 1, 2, 3, 4
```

### Loop avec Continue

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // Sauter l'affichage de 3
    }
    print(i);
}
// Affiche : 1, 2, 4, 5
```

### Boucles imbriquees

```hemlock
let x = 0;
loop {
    if (x >= 2) { break; }
    let y = 0;
    loop {
        if (y >= 3) { break; }
        print(x * 10 + y);
        y = y + 1;
    }
    x = x + 1;
}
// Affiche : 0, 1, 2, 10, 11, 12
```

### Quand utiliser Loop

- **Utilisez `loop`** pour les boucles intentionnellement infinies qui sortent via `break`
- **Utilisez `while`** quand il y a une condition de terminaison naturelle
- **Utilisez `for`** pour iterer un nombre connu de fois ou sur une collection

## Boucles For

### For style C

Boucle for classique en trois parties :

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Composants :**
- **Initialiseur** : `let i = 0` - S'execute une fois avant la boucle
- **Condition** : `i < 10` - Verifiee avant chaque iteration
- **Mise a jour** : `i = i + 1` - S'execute apres chaque iteration

**Portee :**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i non accessible ici (portee de boucle)
```

### Boucles For-In

Iterer sur les elements d'un tableau :

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // Affiche chaque element
}
```

**Avec index et valeur :**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Index: ${i}, Valeur: ${arr[i]}`);
}
```

## Instructions Switch

Branchement multi-voies base sur une valeur :

### Switch basique

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("un");
        break;
    case 2:
        print("deux");
        break;
    case 3:
        print("trois");
        break;
}
```

### Switch avec Default

```hemlock
let color = "blue";

switch (color) {
    case "red":
        print("stop");
        break;
    case "yellow":
        print("ralentir");
        break;
    case "green":
        print("passer");
        break;
    default:
        print("couleur inconnue");
        break;
}
```

**Regles :**
- `default` correspond quand aucun autre case ne correspond
- `default` peut apparaitre n'importe ou dans le corps du switch
- Un seul case default autorise

### Comportement de fall-through

Les cases sans `break` passent au case suivant (comportement style C). C'est **intentionnel** et peut etre utilise pour grouper les cases :

```hemlock
let grade = 85;

switch (grade) {
    case 100:
    case 95:
    case 90:
        print("A");
        break;
    case 85:
    case 80:
        print("B");
        break;
    default:
        print("C ou moins");
        break;
}
```

**Exemple de fallthrough explicite :**
```hemlock
let day = 3;

switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Jour de semaine");
        break;
    case 6:
    case 7:
        print("Week-end");
        break;
}
```

**Important :** Contrairement a certains langages modernes, Hemlock ne necessite PAS de mot-cle `fallthrough` explicite. Les cases passent automatiquement au suivant sauf s'ils sont termines par `break`, `return` ou `throw`. Utilisez toujours `break` pour eviter le fallthrough involontaire.

### Switch avec Return

Dans les fonctions, `return` quitte immediatement le switch :

```hemlock
fn get_day_name(day: i32): string {
    switch (day) {
        case 1:
            return "Lundi";
        case 2:
            return "Mardi";
        case 3:
            return "Mercredi";
        default:
            return "Inconnu";
    }
}
```

### Types de valeur Switch

Switch fonctionne avec n'importe quel type de valeur :

```hemlock
// Entiers
switch (count) {
    case 0: print("zero"); break;
    case 1: print("un"); break;
}

// Chaines
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// Booleens
switch (flag) {
    case true: print("actif"); break;
    case false: print("inactif"); break;
}
```

**Note :** Les cases sont compares par egalite de valeur.

## Break et Continue

### Break

Quitter la boucle ou le switch le plus interne :

```hemlock
// Dans les boucles
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // Quitter la boucle
    }
    print(i);
    i = i + 1;
}

// Dans switch
switch (x) {
    case 1:
        print("un");
        break;  // Quitter le switch
    case 2:
        print("deux");
        break;
}
```

### Continue

Passer a l'iteration suivante de la boucle :

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // Sauter l'iteration quand i est 5
    }
    print(i);  // Affiche 0,1,2,3,4,6,7,8,9
}
```

**Difference :**
- `break` - Quitte entierement la boucle
- `continue` - Passe a l'iteration suivante

## Labels de boucle

Les labels de boucle permettent a `break` et `continue` de cibler des boucles externes specifiques au lieu de la boucle la plus interne. C'est utile pour les boucles imbriquees ou vous devez controler une boucle externe depuis une boucle interne.

### Break labele

Quitter une boucle externe depuis une boucle interne :

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // Quitter la boucle while externe
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// Affiche : 0, 1, 2, 10 (s'arrete a i=1, j=1)
```

### Continue labele

Passer a l'iteration suivante d'une boucle externe :

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // Sauter le reste de la boucle interne, continuer externe
        }
        print(i * 10 + j);
    }
}
// Quand i=2, j=1 : saute a l'iteration externe suivante
```

### Labels avec boucles For

Les labels fonctionnent avec tous les types de boucle :

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 3; y = y + 1) {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
    }
}
```

### Labels avec boucles For-In

```hemlock
let arr1 = [1, 2, 3];
let arr2 = [10, 20, 30];

outer: for (let a in arr1) {
    for (let b in arr2) {
        if (a == 2 && b == 20) {
            break outer;
        }
        print(a * 100 + b);
    }
}
```

### Labels avec mot-cle Loop

```hemlock
let x = 0;
outer: loop {
    let y = 0;
    loop {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
        y = y + 1;
        if (y >= 3) { break; }
    }
    x = x + 1;
    if (x >= 3) { break; }
}
```

### Labels multiples

Vous pouvez avoir des labels a differents niveaux d'imbrication :

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // Passer a l'iteration suivante de la boucle du milieu
            }
            if (a == 1 && b == 1) {
                break outer;      // Quitter la boucle la plus externe
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### Break/Continue non labeles avec boucles labelees

Les `break` et `continue` non labeles fonctionnent toujours normalement (affectant la boucle la plus interne), meme quand les boucles externes ont des labels :

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // Ne sort que de la boucle interne
        }
        print(x * 10 + y);
    }
}
// Affiche : 0, 1, 10, 11, 20, 21
```

### Syntaxe des labels

- Les labels sont des identifiants suivis de deux-points
- Les labels doivent immediatement preceder une instruction de boucle (`while`, `for`, `loop`)
- Les noms de label suivent les regles d'identifiant (lettres, chiffres, underscores)
- Conventions courantes : `outer`, `inner`, `row`, `col`, noms descriptifs

## Instruction Defer

L'instruction `defer` planifie du code pour s'executer quand la fonction courante retourne. C'est utile pour les operations de nettoyage comme fermer des fichiers, liberer des ressources ou relacher des verrous.

### Defer basique

```hemlock
fn example() {
    print("debut");
    defer print("nettoyage");  // S'execute quand la fonction retourne
    print("fin");
}

example();
// Sortie :
// debut
// fin
// nettoyage
```

**Comportement cle :**
- Les instructions differees s'executent **apres** que le corps de la fonction soit termine
- Les instructions differees s'executent **avant** que la fonction ne retourne a son appelant
- Les instructions differees s'executent toujours, meme si la fonction leve une exception

### Defers multiples (ordre LIFO)

Quand plusieurs instructions `defer` sont utilisees, elles s'executent dans l'**ordre inverse** (Dernier-Entre-Premier-Sorti) :

```hemlock
fn example() {
    defer print("premier");   // S'execute en dernier
    defer print("second");    // S'execute en second
    defer print("troisieme"); // S'execute en premier
    print("corps");
}

example();
// Sortie :
// corps
// troisieme
// second
// premier
```

Cet ordre LIFO est intentionnel - il correspond a l'ordre naturel pour le nettoyage de ressources imbriquees (fermer les ressources internes avant les externes).

### Defer avec Return

Les instructions differees s'executent avant que `return` ne transfere le controle :

```hemlock
fn get_value(): i32 {
    defer print("nettoyage");
    print("avant return");
    return 42;
}

let result = get_value();
print("resultat:", result);
// Sortie :
// avant return
// nettoyage
// resultat: 42
```

### Defer avec exceptions

Les instructions differees s'executent meme quand une exception est levee :

```hemlock
fn risky() {
    defer print("nettoyage 1");
    defer print("nettoyage 2");
    print("avant throw");
    throw "erreur!";
    print("apres throw");  // Jamais atteint
}

try {
    risky();
} catch (e) {
    print("Attrape:", e);
}
// Sortie :
// avant throw
// nettoyage 2
// nettoyage 1
// Attrape: erreur!
```

### Modele de nettoyage de ressource

Le cas d'utilisation principal de `defer` est d'assurer que les ressources sont nettoyees :

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // Ferme toujours, meme en cas d'erreur

    let content = file.read();
    // ... traiter le contenu ...

    // Fichier automatiquement ferme quand la fonction retourne
}
```

**Sans defer (propice aux erreurs) :**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // Si cela leve une exception, file.close() n'est jamais appele !
    process(content);
    file.close();
}
```

### Defer avec fermetures

Defer peut utiliser des fermetures pour capturer l'etat :

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Liberation de la ressource");
        release(resource);
    }();  // Note : expression de fonction immediatement invoquee

    use_resource(resource);
}
```

### Quand utiliser Defer

**Utilisez defer pour :**
- Fermer des fichiers et connexions reseau
- Liberer la memoire allouee
- Relacher des verrous et mutex
- Nettoyage dans toute fonction qui acquiert des ressources

**Defer vs Finally :**
- `defer` est plus simple pour le nettoyage de ressource unique
- `try/finally` est mieux pour la gestion d'erreur complexe avec recuperation

### Bonnes pratiques

1. **Placez defer immediatement apres l'acquisition d'une ressource :**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... utiliser file ...
   ```

2. **Utilisez plusieurs defers pour plusieurs ressources :**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // Les deux fichiers seront fermes dans l'ordre inverse
   ```

3. **Rappelez-vous l'ordre LIFO pour les ressources dependantes :**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner libere avant outer (ordre de dependance correct)
   ```

## Operateurs booleens

### ET logique (`&&`)

Les deux conditions doivent etre vraies :

```hemlock
if (x > 0 && x < 10) {
    print("chiffre positif");
}
```

**Evaluation court-circuit :**
```hemlock
if (false && expensive_check()) {
    // expensive_check() jamais appelee
}
```

### OU logique (`||`)

Au moins une condition doit etre vraie :

```hemlock
if (x < 0 || x > 100) {
    print("hors plage");
}
```

**Evaluation court-circuit :**
```hemlock
if (true || expensive_check()) {
    // expensive_check() jamais appelee
}
```

### NON logique (`!`)

Inverse la valeur booleenne :

```hemlock
if (!is_valid) {
    print("invalide");
}

if (!(x > 10)) {
    // Equivalent a : if (x <= 10)
}
```

## Operateurs de comparaison

### Egalite

```hemlock
if (x == 10) { }    // Egal
if (x != 10) { }    // Different
```

Fonctionne avec tous les types :
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### Relationnel

```hemlock
if (x < 10) { }     // Inferieur a
if (x > 10) { }     // Superieur a
if (x <= 10) { }    // Inferieur ou egal
if (x >= 10) { }    // Superieur ou egal
```

**La promotion de type s'applique :**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true (i32 promu vers i64)
```

## Operateurs binaires (bitwise)

Hemlock fournit des operateurs binaires pour la manipulation d'entiers. Ceux-ci fonctionnent **uniquement avec les types entiers** (i8-i64, u8-u64).

### Operateurs binaires binaires

**ET binaire (`&`)**
```hemlock
let a = 12;  // 1100 en binaire
let b = 10;  // 1010 en binaire
print(a & b);   // 8 (1000)
```

**OU binaire (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**XOR binaire (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**Decalage a gauche (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - decaler a gauche de 2
```

**Decalage a droite (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - decaler a droite de 1
```

### Operateur binaire unaire

**NON binaire (`~`)**
```hemlock
let a = 12;
print(~a);      // -13 (complement a deux)

let c: u8 = 15;   // 00001111 en binaire
print(~c);        // 240 (11110000) en u8
```

### Exemples binaires

**Avec types non signes :**
```hemlock
let c: u8 = 15;   // 00001111 en binaire
let d: u8 = 7;    // 00000111 en binaire

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - en u8
```

**Preservation du type :**
```hemlock
// Les operations binaires preservent le type des operandes
let x: u8 = 255;
let result = ~x;  // result est u8 avec valeur 0

let y: i32 = 100;
let result2 = y << 2;  // result2 est i32 avec valeur 400
```

**Modeles courants :**
```hemlock
// Verifier si un bit est defini
if (flags & 0x04) {
    print("bit 2 est defini");
}

// Definir un bit
flags = flags | 0x08;

// Effacer un bit
flags = flags & ~0x02;

// Inverser un bit
flags = flags ^ 0x01;
```

### Priorite des operateurs

Les operateurs binaires suivent la priorite style C :

1. `~` (NON unaire) - plus haute, meme niveau que `!` et `-`
2. `<<`, `>>` (decalages) - plus haute que comparaisons, plus basse que `+`/`-`
3. `&` (ET binaire) - plus haute que `^` et `|`
4. `^` (XOR binaire) - entre `&` et `|`
5. `|` (OU binaire) - plus basse que `&` et `^`, plus haute que `&&`
6. `&&`, `||` (logiques) - priorite la plus basse

**Exemples :**
```hemlock
// & a une priorite plus haute que |
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// Decalage a une priorite plus haute que les operateurs binaires
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// Utilisez des parentheses pour la clarte
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**Notes importantes :**
- Les operateurs binaires fonctionnent uniquement avec les types entiers (pas les flottants, chaines, etc.)
- La promotion de type suit les regles standard (les types plus petits sont promus vers les plus grands)
- Le decalage a droite (`>>`) est arithmetique pour les types signes, logique pour les non signes
- Les quantites de decalage ne sont pas verifiees (comportement dependant de la plateforme pour les grands decalages)

## Priorite des operateurs (complete)

De la priorite la plus haute a la plus basse :

1. **Unaire** : `!`, `-`, `~`
2. **Multiplicatif** : `*`, `/`, `%`
3. **Additif** : `+`, `-`
4. **Decalage** : `<<`, `>>`
5. **Relationnel** : `<`, `>`, `<=`, `>=`
6. **Egalite** : `==`, `!=`
7. **ET binaire** : `&`
8. **XOR binaire** : `^`
9. **OU binaire** : `|`
10. **ET logique** : `&&`
11. **OU logique** : `||`

**Utilisez des parentheses pour la clarte :**
```hemlock
// Pas clair
if (a || b && c) { }

// Clair
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## Modeles courants

### Modele : Validation d'entree

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### Modele : Verification de plage

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("score valide");
}
```

### Modele : Machine a etats

```hemlock
let state = "start";

while (true) {
    switch (state) {
        case "start":
            print("Demarrage...");
            state = "running";
            break;

        case "running":
            if (should_pause) {
                state = "paused";
            } else if (should_stop) {
                state = "stopped";
            }
            break;

        case "paused":
            if (should_resume) {
                state = "running";
            }
            break;

        case "stopped":
            print("Arrete");
            break;
    }

    if (state == "stopped") {
        break;
    }
}
```

### Modele : Iteration avec filtrage

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Afficher uniquement les nombres pairs
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // Sauter les nombres impairs
    }
    print(arr[i]);
}
```

### Modele : Sortie anticipee

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Sortie anticipee
        }
    }
    return -1;  // Non trouve
}
```

## Bonnes pratiques

1. **Utilisez toujours des accolades** - Meme pour les blocs a instruction unique (impose par la syntaxe)
2. **Conditions explicites** - Utilisez `x == 0` au lieu de `!x` pour la clarte
3. **Evitez l'imbrication profonde** - Extrayez les conditions imbriquees en fonctions
4. **Utilisez les retours anticipes** - Reduisez l'imbrication avec des clauses de garde
5. **Divisez les conditions complexes** - Divisez en variables booleennes nommees
6. **Default dans switch** - Incluez toujours un case default
7. **Commentez le fall-through** - Rendez le fall-through intentionnel explicite

## Pieges courants

### Piege : Assignation dans la condition

```hemlock
// Ceci n'est PAS autorise (pas d'assignation dans les conditions)
if (x = 10) { }  // ERREUR : Erreur de syntaxe

// Utilisez la comparaison a la place
if (x == 10) { }  // OK
```

### Piege : Break manquant dans Switch

```hemlock
// Fall-through involontaire
switch (x) {
    case 1:
        print("un");
        // Break manquant - fall-through !
    case 2:
        print("deux");  // S'execute pour 1 et 2
        break;
}

// Correction : Ajouter break
switch (x) {
    case 1:
        print("un");
        break;  // Maintenant correct
    case 2:
        print("deux");
        break;
}
```

### Piege : Portee de variable de boucle

```hemlock
// i a une portee limitee a la boucle
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // ERREUR : i non defini ici
```

## Exemples

### Exemple : FizzBuzz

```hemlock
for (let i = 1; i <= 100; i = i + 1) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else if (i % 3 == 0) {
        print("Fizz");
    } else if (i % 5 == 0) {
        print("Buzz");
    } else {
        print(i);
    }
}
```

### Exemple : Verificateur de nombre premier

```hemlock
fn is_prime(n: i32): bool {
    if (n < 2) {
        return false;
    }

    let i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
```

### Exemple : Systeme de menu

```hemlock
fn menu() {
    while (true) {
        print("1. Demarrer");
        print("2. Parametres");
        print("3. Quitter");

        let choice = get_input();

        switch (choice) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Au revoir !");
                return;
            default:
                print("Choix invalide");
                break;
        }
    }
}
```

## Sujets connexes

- [Fonctions](functions.md) - Flux de controle avec appels de fonction et retours
- [Gestion des erreurs](error-handling.md) - Flux de controle avec exceptions
- [Types](types.md) - Conversions de type dans les conditions

## Voir aussi

- **Syntaxe** : Voir [Syntaxe](syntax.md) pour les details de syntaxe des instructions
- **Operateurs** : Voir [Types](types.md) pour la promotion de type dans les operations
