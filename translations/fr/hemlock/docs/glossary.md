# Glossaire

Nouveau en programmation ou en concepts systeme ? Ce glossaire explique les termes utilises dans la documentation de Hemlock en langage clair.

---

## A

### Allouer / Allocation
**Ce que cela signifie :** Demander a l'ordinateur un bloc de memoire a utiliser.

**Analogie :** Comme emprunter un livre a une bibliotheque - vous empruntez de l'espace que vous devrez rendre plus tard.

**Dans Hemlock :**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### Array (Tableau)
**Ce que cela signifie :** Une liste de valeurs stockees ensemble, accessibles par position (index).

**Analogie :** Comme une rangee de boites aux lettres numerotees 0, 1, 2, 3... Vous pouvez mettre quelque chose dans la boite #2 et le recuperer plus tard depuis la boite #2.

**Dans Hemlock :**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Asynchrone
**Ce que cela signifie :** Du code qui peut s'executer "en arriere-plan" pendant que d'autre code continue. Dans Hemlock, le code asynchrone s'execute reellement en parallele sur des coeurs CPU distincts.

**Analogie :** Comme cuisiner plusieurs plats en meme temps - vous mettez le riz a cuire, puis pendant qu'il cuit, vous coupez les legumes. Les deux se passent en meme temps.

**Dans Hemlock :**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Boolean / Bool (Booleen)
**Ce que cela signifie :** Une valeur qui est soit `true` soit `false`. Rien d'autre.

**Nomme d'apres :** George Boole, un mathematicien qui a etudie la logique vrai/faux.

**Dans Hemlock :**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Verification des limites (Bounds Checking)
**Ce que cela signifie :** Verifier automatiquement que vous n'essayez pas d'acceder a de la memoire en dehors de ce qui a ete alloue. Empeche les plantages et les failles de securite.

**Analogie :** Comme un bibliothecaire qui verifie que le livre que vous demandez existe reellement avant d'essayer de le chercher.

**Dans Hemlock :**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer (Tampon)
**Ce que cela signifie :** Un conteneur securise pour des octets bruts avec une taille connue. Hemlock verifie que vous ne lisez ni n'ecrivez au-dela de ses limites.

**Analogie :** Comme un coffre-fort avec un nombre specifique de compartiments. Vous pouvez utiliser n'importe quel compartiment, mais vous ne pouvez pas acceder au compartiment #50 si le coffre n'en a que 10.

**Dans Hemlock :**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Closure (Fermeture)
**Ce que cela signifie :** Une fonction qui "se souvient" des variables de l'endroit ou elle a ete creee, meme apres que ce code a fini de s'executer.

**Analogie :** Comme une note qui dit "ajoute 5 a n'importe quel nombre que tu me donnes" - le "5" est integre dans la note.

**Dans Hemlock :**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Coercition de type (Type Coercion)
**Ce que cela signifie :** Convertir automatiquement une valeur d'un type vers un autre quand c'est necessaire.

**Exemple :** Quand vous additionnez un entier et un nombre decimal, l'entier est automatiquement converti en decimal d'abord.

**Dans Hemlock :**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Compiler / Compilateur
**Ce que cela signifie :** Traduire votre code en un programme que l'ordinateur peut executer directement. Le compilateur (`hemlockc`) lit votre fichier `.hml` et cree un executable.

**Analogie :** Comme traduire un livre de l'anglais vers l'espagnol - le contenu est le meme, mais maintenant les hispanophones peuvent le lire.

**Dans Hemlock :**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Concurrence
**Ce que cela signifie :** Plusieurs choses se produisant a des moments qui se chevauchent. Dans Hemlock, cela signifie une execution parallele reelle sur plusieurs coeurs CPU.

**Analogie :** Deux chefs cuisinant differents plats simultanement dans la meme cuisine.

---

## D

### Defer (Differer)
**Ce que cela signifie :** Planifier quelque chose pour plus tard, quand la fonction en cours se termine. Utile pour le nettoyage.

**Analogie :** Comme se dire "quand je partirai, eteins les lumieres" - vous posez le rappel maintenant, il se produit plus tard.

**Dans Hemlock :**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck Typing (Typage canard)
**Ce que cela signifie :** Si ca ressemble a un canard et ca fait coin-coin comme un canard, traitez-le comme un canard. En code : si un objet a les champs/methodes dont vous avez besoin, utilisez-le - ne vous souciez pas de son "type" officiel.

**Nomme d'apres :** Le test du canard - une forme de raisonnement.

**Dans Hemlock :**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Expression
**Ce que cela signifie :** Du code qui produit une valeur. Peut etre utilise partout ou une valeur est attendue.

**Exemples :** `42`, `x + y`, `get_name()`, `true && false`

### Enum / Enumeration
**Ce que cela signifie :** Un type avec un ensemble fixe de valeurs possibles, chacune avec un nom.

**Analogie :** Comme un menu deroulant - vous ne pouvez choisir que parmi les options listees.

**Dans Hemlock :**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Virgule flottante
**Ce que cela signifie :** Un nombre avec une virgule decimale. Appele "flottant" parce que la virgule peut etre a differentes positions.

**Dans Hemlock :**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free (Liberer)
**Ce que cela signifie :** Rendre la memoire dont vous n'avez plus besoin au systeme pour qu'elle puisse etre reutilisee.

**Analogie :** Rendre un livre emprunte a la bibliotheque pour que d'autres puissent l'emprunter.

**Dans Hemlock :**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Fonction
**Ce que cela signifie :** Un bloc de code reutilisable qui prend des entrees (parametres) et peut produire une sortie (valeur de retour).

**Analogie :** Comme une recette - donnez-lui des ingredients (entrees), suivez les etapes, obtenez un plat (sortie).

**Dans Hemlock :**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Ramasse-miettes (Garbage Collection / GC)
**Ce que cela signifie :** Nettoyage automatique de la memoire. Le runtime trouve periodiquement la memoire inutilisee et la libere pour vous.

**Pourquoi Hemlock ne l'a pas :** Le GC peut causer des pauses imprevisibles. Hemlock prefere le controle explicite - c'est vous qui decidez quand liberer la memoire.

**Remarque :** La plupart des types Hemlock (strings, arrays, objets) SONT automatiquement nettoyes quand ils sortent de la portee. Seuls les `ptr` bruts de `alloc()` necessitent un `free()` manuel.

---

## H

### Heap (Tas)
**Ce que cela signifie :** Une region de memoire pour les donnees qui doivent survivre a la fonction en cours. Vous allouez et liberez la memoire du tas explicitement.

**En contraste avec :** La pile (stack) - stockage automatique et temporaire pour les variables locales.

**Dans Hemlock :**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Index
**Ce que cela signifie :** La position d'un element dans un tableau ou une chaine. Commence a 0 dans Hemlock.

**Dans Hemlock :**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Entier (Integer)
**Ce que cela signifie :** Un nombre entier sans virgule decimale. Peut etre positif, negatif ou zero.

**Dans Hemlock :**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interpreteur
**Ce que cela signifie :** Un programme qui lit votre code et l'execute directement, ligne par ligne.

**En contraste avec :** Le compilateur (traduit le code d'abord, puis execute la traduction).

**Dans Hemlock :**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Litteral
**Ce que cela signifie :** Une valeur ecrite directement dans votre code, non calculee.

**Exemples :**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Fuite memoire (Memory Leak)
**Ce que cela signifie :** Oublier de liberer la memoire allouee. La memoire reste reservee mais inutilisee, gaspillant des ressources.

**Analogie :** Emprunter des livres a la bibliotheque et ne jamais les rendre. A terme, la bibliotheque n'a plus de livres.

**Dans Hemlock :**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Methode
**Ce que cela signifie :** Une fonction attachee a un objet ou un type.

**Dans Hemlock :**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex
**Ce que cela signifie :** Un verrou qui garantit qu'un seul thread accede a quelque chose a la fois. Empeche la corruption des donnees quand plusieurs threads touchent des donnees partagees.

**Analogie :** Comme un verrou de salle de bain - une seule personne peut l'utiliser a la fois.

---

## N

### Null
**Ce que cela signifie :** Une valeur speciale signifiant "rien" ou "pas de valeur".

**Dans Hemlock :**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Objet
**Ce que cela signifie :** Une collection de valeurs nommees (champs/proprietes) regroupees ensemble.

**Dans Hemlock :**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parametre
**Ce que cela signifie :** Une variable qu'une fonction s'attend a recevoir lors de l'appel.

**Aussi appele :** Argument (techniquement, le parametre est dans la definition, l'argument est dans l'appel).

**Dans Hemlock :**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Pointeur (Pointer)
**Ce que cela signifie :** Une valeur qui contient une adresse memoire - elle "pointe vers" l'endroit ou les donnees sont stockees.

**Analogie :** Comme une adresse postale. L'adresse n'est pas la maison - elle vous dit ou trouver la maison.

**Dans Hemlock :**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitif
**Ce que cela signifie :** Un type de base, integre, qui n'est pas compose d'autres types.

**Dans Hemlock :** `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `null`

---

## R

### Comptage de references (Reference Counting)
**Ce que cela signifie :** Suivre combien de choses utilisent une donnee. Quand plus rien ne l'utilise, la nettoyer automatiquement.

**Dans Hemlock :** Les strings, tableaux, objets et buffers utilisent le comptage de references en interne. Vous ne le voyez pas, mais cela empeche les fuites memoire pour la plupart des types courants.

### Valeur de retour
**Ce que cela signifie :** La valeur qu'une fonction renvoie quand elle se termine.

**Dans Hemlock :**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**Ce que cela signifie :** Un seul caractere Unicode (point de code). Peut representer n'importe quel caractere, y compris les emoji.

**Pourquoi "rune" ?** Le terme vient de Go. Il souligne qu'il s'agit d'un caractere complet, pas juste d'un octet.

**Dans Hemlock :**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Runtime (Execution)
**Ce que cela signifie :** Le moment ou votre programme s'execute reellement (par opposition au "temps de compilation" quand il est traduit).

**Aussi :** Le code de support qui s'execute aux cotes de votre programme (par ex. l'allocateur memoire).

---

## S

### Portee (Scope)
**Ce que cela signifie :** La region du code ou une variable existe et peut etre utilisee.

**Dans Hemlock :**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Pile (Stack)
**Ce que cela signifie :** De la memoire pour des donnees temporaires et de courte duree. Geree automatiquement - quand une fonction retourne, son espace de pile est recupere.

**En contraste avec :** Le tas (heap) - plus durable, gere manuellement.

### Instruction (Statement)
**Ce que cela signifie :** Une seule instruction ou commande. Les instructions FONT des choses ; les expressions PRODUISENT des valeurs.

**Exemples :** `let x = 5;`, `print("hi");`, `if (x > 0) { ... }`

### String (Chaine de caracteres)
**Ce que cela signifie :** Une sequence de caracteres textuels.

**Dans Hemlock :**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Typage structurel (Structural Typing)
**Ce que cela signifie :** Compatibilite de type basee sur la structure (quels champs/methodes existent), pas sur le nom. Identique au "duck typing".

---

## T

### Thread (Fil d'execution)
**Ce que cela signifie :** Un chemin d'execution separe. Plusieurs threads peuvent s'executer simultanement sur differents coeurs CPU.

**Dans Hemlock :** `spawn()` cree un nouveau thread.

### Type
**Ce que cela signifie :** Le genre de donnees qu'une valeur represente. Determine quelles operations sont valides.

**Dans Hemlock :**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Annotation de type
**Ce que cela signifie :** Declarer explicitement quel type une variable doit avoir.

**Dans Hemlock :**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**Ce que cela signifie :** Une methode d'encodage de texte qui supporte toutes les langues du monde et les emoji. Chaque caractere peut occuper de 1 a 4 octets.

**Dans Hemlock :** Toutes les chaines sont en UTF-8.

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variable
**Ce que cela signifie :** Un emplacement de stockage nomme qui contient une valeur.

**Dans Hemlock :**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## Reference rapide : Quel type utiliser ?

| Situation | Utilisez ceci | Pourquoi |
|-----------|---------------|----------|
| Besoin d'un simple nombre | `let x = 42;` | Hemlock choisit le bon type |
| Compter des choses | `i32` | Assez grand pour la plupart des comptages |
| Tres grands nombres | `i64` | Quand i32 ne suffit pas |
| Octets (0-255) | `u8` | Fichiers, donnees reseau |
| Nombres decimaux | `f64` | Calcul decimal precis |
| Valeurs oui/non | `bool` | Seulement `true` ou `false` |
| Texte | `string` | Tout contenu textuel |
| Un seul caractere | `rune` | Une lettre/un emoji |
| Liste de choses | `array` | Collection ordonnee |
| Champs nommes | `object` | Regrouper des donnees liees |
| Memoire brute | `buffer` | Stockage d'octets securise |
| FFI/travail systeme | `ptr` | Avance, memoire manuelle |

---

## Voir aussi

- [Demarrage rapide](getting-started/quick-start.md) - Votre premier programme Hemlock
- [Systeme de types](language-guide/types.md) - Documentation complete des types
- [Gestion de la memoire](language-guide/memory.md) - Comprendre la memoire
