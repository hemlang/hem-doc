# Demarrage rapide

Soyez operationnel avec Hemlock en quelques minutes !

## Votre premier programme

Creez un fichier appele `hello.hml` :

```hemlock
print("Hello, Hemlock!");
```

Executez-le avec l'interpreteur :

```bash
./hemlock hello.hml
```

Ou compilez-le en executable natif :

```bash
./hemlockc hello.hml -o hello
./hello
```

Sortie :
```
Hello, Hemlock!
```

### Interpreteur vs Compilateur

Hemlock offre deux manieres d'executer des programmes :

| Outil | Cas d'utilisation | Verification des types |
|-------|-------------------|------------------------|
| `hemlock` | Scripts rapides, REPL, developpement | A l'execution uniquement |
| `hemlockc` | Binaires de production, meilleures performances | A la compilation (par defaut) |

Le compilateur (`hemlockc`) verifie les types de votre code avant de generer un executable, detectant les erreurs plus tot.

## Syntaxe de base

### Variables

```hemlock
// Les variables sont declarees avec 'let'
let x = 42;
let name = "Alice";
let pi = 3.14159;

// Les annotations de type sont optionnelles
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**Important** : Les points-virgules sont **obligatoires** en Hemlock !

### Types

Hemlock possede un systeme de types riche :

```hemlock
// Entiers
let small: i8 = 127;          // 8 bits signe
let byte: u8 = 255;           // 8 bits non signe
let num: i32 = 2147483647;    // 32 bits signe (par defaut)
let big: i64 = 9223372036854775807;  // 64 bits signe

// Flottants
let f: f32 = 3.14;            // flottant 32 bits
let d: f64 = 2.71828;         // flottant 64 bits (par defaut)

// Chaines et caracteres
let text: string = "Hello";   // chaine UTF-8
let emoji: rune = '🚀';       // point de code Unicode

// Booleen et null
let flag: bool = true;
let empty = null;
```

### Flux de controle

```hemlock
// Instructions if
if (x > 0) {
    print("positif");
} else if (x < 0) {
    print("negatif");
} else {
    print("zero");
}

// Boucles while
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// Boucles for
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### Fonctions

```hemlock
// Fonction nommee
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// Fonction anonyme
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## Travailler avec les chaines

Les chaines en Hemlock sont **mutables** et **UTF-8** :

```hemlock
let s = "hello";
s[0] = 'H';              // Maintenant "Hello"
print(s);

// Methodes de chaines
let upper = s.to_upper();     // "HELLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "ell"

// Concatenation
let greeting = "Hello" + ", " + "World!";
print(greeting);  // "Hello, World!"
```

## Tableaux

Tableaux dynamiques avec types mixtes :

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Methodes de tableaux
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// Types mixtes autorises
let mixed = [1, "two", true, null];
```

## Objets

Objets de style JavaScript :

```hemlock
// Litteral d'objet
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // Modifier un champ

// Methodes avec 'self'
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Gestion de la memoire

Hemlock utilise la **gestion manuelle de la memoire** :

```hemlock
// Buffer securise (recommande)
let buf = buffer(64);   // Allouer 64 octets
buf[0] = 65;            // Definir le premier octet a 'A'
print(buf[0]);          // 65
free(buf);              // Liberer la memoire

// Pointeur brut (avance)
let ptr = alloc(100);
memset(ptr, 0, 100);    // Remplir avec des zeros
free(ptr);
```

**Important** : Vous devez appeler `free()` pour ce que vous avez alloue avec `alloc()` !

## Gestion des erreurs

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division par zero";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Erreur : " + e);
} finally {
    print("Termine");
}
```

## Arguments en ligne de commande

Accedez aux arguments du programme via le tableau `args` :

```hemlock
// script.hml
print("Script:", args[0]);
print(`Arguments : ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  arg ${i}: ${args[i]}`);
    i = i + 1;
}
```

Executez avec :
```bash
./hemlock script.hml hello world
```

Sortie :
```
Script: script.hml
Arguments : 2
  arg 1: hello
  arg 2: world
```

## Entrees/Sorties fichier

```hemlock
// Ecrire dans un fichier
let f = open("data.txt", "w");
f.write("Hello, File!");
f.close();

// Lire depuis un fichier
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Hello, File!"
f2.close();
```

## Et ensuite ?

Maintenant que vous avez vu les bases, explorez davantage :

- [Tutoriel](tutorial.md) - Guide complet etape par etape
- [Guide du langage](../language-guide/syntax.md) - Plongee approfondie dans toutes les fonctionnalites
- [Exemples](../../examples/) - Programmes d'exemple concrets
- [Reference API](../reference/builtins.md) - Documentation complete de l'API

## Pieges courants

### Oublier les points-virgules

```hemlock
// ERREUR : Point-virgule manquant
let x = 42
let y = 10

// CORRECT
let x = 42;
let y = 10;
```

### Oublier de liberer la memoire

```hemlock
// FUITE DE MEMOIRE
let buf = buffer(100);
// ... utiliser buf ...
// Oublie d'appeler free(buf) !

// CORRECT
let buf = buffer(100);
// ... utiliser buf ...
free(buf);
```

### Les accolades sont obligatoires

```hemlock
// ERREUR : Accolades manquantes
if (x > 0)
    print("positif");

// CORRECT
if (x > 0) {
    print("positif");
}
```

## Obtenir de l'aide

- Lisez la [documentation complete](../README.md)
- Consultez le [repertoire d'exemples](../../examples/)
- Regardez les [fichiers de test](../../tests/) pour des exemples d'utilisation
- Signalez les problemes sur GitHub
