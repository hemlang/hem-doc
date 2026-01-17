# Tutoriel Hemlock

Un guide complet etape par etape pour apprendre Hemlock.

## Table des matieres

1. [Hello World](#hello-world)
2. [Variables et types](#variables-et-types)
3. [Arithmetique et operations](#arithmetique-et-operations)
4. [Flux de controle](#flux-de-controle)
5. [Fonctions](#fonctions)
6. [Chaines et runes](#chaines-et-runes)
7. [Tableaux](#tableaux)
8. [Objets](#objets)
9. [Gestion de la memoire](#gestion-de-la-memoire)
10. [Gestion des erreurs](#gestion-des-erreurs)
11. [Entrees/Sorties fichier](#entreessorties-fichier)
12. [Mettre tout ensemble](#mettre-tout-ensemble)

## Hello World

Commencons par le traditionnel premier programme :

```hemlock
print("Hello, World!");
```

Enregistrez ceci sous `hello.hml` et executez :

```bash
./hemlock hello.hml
```

**Points cles :**
- `print()` est une fonction integree qui affiche sur stdout
- Les chaines sont entourees de guillemets doubles
- Les points-virgules sont **obligatoires**

## Variables et types

### Declaration de variables

```hemlock
// Declaration de variable simple
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### Annotations de type

Bien que les types soient inferes par defaut, vous pouvez etre explicite :

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### Inference de type

Hemlock infere les types en fonction des valeurs :

```hemlock
let small = 42;              // i32 (tient dans 32 bits)
let large = 5000000000;      // i64 (trop grand pour i32)
let decimal = 3.14;          // f64 (par defaut pour les flottants)
let text = "hello";          // string
let flag = true;             // bool
```

### Verification de type

```hemlock
// Verifier les types avec typeof()
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hello"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## Arithmetique et operations

### Arithmetique de base

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3 (division entiere)
print(a == b);  // false
print(a > b);   // true
```

### Promotion de type

Lors du melange de types, Hemlock promeut vers le type plus grand/plus precis :

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result est f64 (10.0 + 3.5 = 13.5)

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### Operations bit a bit

```hemlock
let a = 12;  // 1100 en binaire
let b = 10;  // 1010 en binaire

print(a & b);   // 8  (ET)
print(a | b);   // 14 (OU)
print(a ^ b);   // 6  (OU exclusif)
print(a << 1);  // 24 (decalage a gauche)
print(a >> 1);  // 6  (decalage a droite)
print(~a);      // -13 (NON)
```

## Flux de controle

### Instructions if

```hemlock
let x = 10;

if (x > 0) {
    print("positif");
} else if (x < 0) {
    print("negatif");
} else {
    print("zero");
}
```

**Remarque :** Les accolades sont **toujours obligatoires**, meme pour les instructions simples.

### Boucles while

```hemlock
let count = 0;
while (count < 5) {
    print(`Compteur : ${count}`);
    count = count + 1;
}
```

### Boucles for

```hemlock
// Boucle for de style C
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// Boucle for-in (tableaux)
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Element : ${item}`);
}
```

### Instructions switch

```hemlock
let day = 3;

switch (day) {
    case 1:
        print("Lundi");
        break;
    case 2:
        print("Mardi");
        break;
    case 3:
        print("Mercredi");
        break;
    default:
        print("Autre jour");
        break;
}
```

### Break et continue

```hemlock
// Break : sortir de la boucle prematurement
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Affiche : 0, 1, 2, 3, 4

// Continue : passer a l'iteration suivante
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// Affiche : 0, 1, 3, 4
```

## Fonctions

### Fonctions nommees

```hemlock
fn greet(name: string): string {
    return "Bonjour, " + name + " !";
}

let message = greet("Alice");
print(message);  // "Bonjour, Alice !"
```

### Fonctions anonymes

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### Recursivite

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Fermetures (Closures)

Les fonctions capturent leur environnement :

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

### Fonctions d'ordre superieur

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## Chaines et runes

### Bases des chaines

Les chaines sont **mutables** et **UTF-8** :

```hemlock
let s = "hello";
print(s.length);      // 5 (nombre de caracteres)
print(s.byte_length); // 5 (nombre d'octets)

// Mutation
s[0] = 'H';
print(s);  // "Hello"
```

### Methodes de chaines

```hemlock
let text = "  Hello, World!  ";

// Conversion de casse
print(text.to_upper());  // "  HELLO, WORLD!  "
print(text.to_lower());  // "  hello, world!  "

// Suppression des espaces
print(text.trim());      // "Hello, World!"

// Extraction de sous-chaines
let hello = text.substr(2, 5);  // "Hello"
let world = text.slice(9, 14);  // "World"

// Recherche
let pos = text.find("World");   // 9
let has = text.contains("o");   // true

// Division
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// Remplacement
let s = "hello world".replace("world", "there");
print(s);  // "hello there"
```

### Runes (points de code Unicode)

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Concatenation rune + chaine
let msg = '>' + " Important";
print(msg);  // "> Important"

// Convertir entre rune et entier
let code: i32 = ch;     // 65 (code ASCII)
let r: rune = 128640;   // U+1F680 (🚀)
```

## Tableaux

### Bases des tableaux

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Modifier les elements
numbers[2] = 99;
print(numbers[2]);  // 99
```

### Methodes de tableaux

```hemlock
let arr = [10, 20, 30];

// Ajouter/supprimer a la fin
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40, arr est maintenant [10, 20, 30]

// Ajouter/supprimer au debut
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5, arr est maintenant [10, 20, 30]

// Inserer/supprimer a un index
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// Recherche
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// Tranche
let slice = arr.slice(0, 2);  // [10, 15]

// Joindre en chaine
let text = arr.join(", ");    // "10, 15, 30"
```

### Iteration

```hemlock
let items = ["pomme", "banane", "cerise"];

// Boucle for-in
for (let item in items) {
    print(item);
}

// Iteration manuelle
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## Objets

### Litteraux d'objets

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// Ajouter/modifier des champs
person.email = "alice@example.com";
person.age = 31;
```

### Methodes et `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### Definitions de types (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // Optionnel avec valeur par defaut
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // Le duck typing valide la structure

print(typeof(typed));   // "Person"
print(typed.active);    // true (valeur par defaut appliquee)
```

### Serialisation JSON

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// Objet vers JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON vers objet
let restored = json.deserialize();
print(restored.name);  // "test"
```

## Gestion de la memoire

### Buffers securises (Recommande)

```hemlock
// Allouer un buffer
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// Definir des valeurs (verification des limites)
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Acceder aux valeurs
print(buf[0]);  // 65

// Doit etre libere a la fin
free(buf);
```

### Pointeurs bruts (Avance)

```hemlock
// Allouer de la memoire brute
let ptr = alloc(100);

// Remplir avec des zeros
memset(ptr, 0, 100);

// Copier des donnees
let src = alloc(50);
memcpy(ptr, src, 50);

// Liberer les deux
free(src);
free(ptr);
```

### Fonctions de memoire

```hemlock
// Reallouer
let p = alloc(64);
p = realloc(p, 128);  // Redimensionner a 128 octets
free(p);

// Allocation typee (futur)
// let arr = talloc(i32, 100);  // Tableau de 100 i32
```

## Gestion des erreurs

### Try/Catch

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
}
// Sortie : Erreur : division par zero
```

### Bloc finally

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Erreur : " + e);
} finally {
    // S'execute toujours
    if (file != null) {
        file.close();
    }
}
```

### Lancer des objets

```hemlock
try {
    throw { code: 404, message: "Non trouve" };
} catch (e) {
    print(`Erreur ${e.code} : ${e.message}`);
}
// Sortie : Erreur 404 : Non trouve
```

### Panic (Erreurs irrecuperables)

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x doit etre non negatif");
    }
    return x * 2;
}

validate(-5);  // Le programme se termine avec : panic: x doit etre non negatif
```

## Entrees/Sorties fichier

### Lecture de fichiers

```hemlock
// Lire le fichier entier
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// Lire un nombre specifique d'octets
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // Lire 100 octets
f2.close();
```

### Ecriture de fichiers

```hemlock
// Ecrire du texte
let f = open("output.txt", "w");
f.write("Bonjour, Fichier !\n");
f.write("Deuxieme ligne\n");
f.close();

// Ajouter au fichier
let f2 = open("output.txt", "a");
f2.write("Ligne ajoutee\n");
f2.close();
```

### E/S binaires

```hemlock
// Ecrire des donnees binaires
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// Lire des donnees binaires
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### Proprietes de fichier

```hemlock
let f = open("/chemin/vers/fichier.txt", "r");

print(f.path);    // "/chemin/vers/fichier.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## Mettre tout ensemble

Construisons un simple programme de comptage de mots :

```hemlock
// wordcount.hml - Compter les mots dans un fichier

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // Diviser par les espaces et compter
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Erreur de lecture du fichier : " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// Programme principal
if (args.length < 2) {
    print("Usage : " + args[0] + " <nom_fichier>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Nombre de mots : ${words}`);
    }
}
```

Executez avec :
```bash
./hemlock wordcount.hml data.txt
```

## Prochaines etapes

Felicitations ! Vous avez appris les bases de Hemlock. Voici ce que vous pouvez explorer ensuite :

- [Async et concurrence](../advanced/async-concurrency.md) - Veritable multithreading
- [FFI](../advanced/ffi.md) - Appeler des fonctions C
- [Gestion des signaux](../advanced/signals.md) - Signaux de processus
- [Reference API](../reference/builtins.md) - Documentation complete de l'API
- [Exemples](../../examples/) - Plus de programmes concrets

## Exercices pratiques

Essayez de construire ces programmes pour vous entrainer :

1. **Calculatrice** : Implementez une calculatrice simple avec +, -, *, /
2. **Copie de fichier** : Copiez un fichier vers un autre
3. **Fibonacci** : Generez les nombres de Fibonacci
4. **Analyseur JSON** : Lisez et analysez des fichiers JSON
5. **Processeur de texte** : Trouvez et remplacez du texte dans des fichiers

Bon codage avec Hemlock !
