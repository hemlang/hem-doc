# Fonctions

Les fonctions en Hemlock sont des **valeurs de premiere classe** qui peuvent etre assignees a des variables, passees en arguments et retournees par d'autres fonctions. Ce guide couvre la syntaxe des fonctions, les fermetures, la recursivite et les modeles avances.

## Apercu

```hemlock
// Syntaxe de fonction nommee
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Fonction anonyme
let multiply = fn(x, y) {
    return x * y;
};

// Fermetures
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Declaration de fonction

### Fonctions nommees

```hemlock
fn greet(name: string): string {
    return "Bonjour, " + name;
}

let msg = greet("Alice");  // "Bonjour, Alice"
```

**Composants :**
- `fn` - Mot-cle fonction
- `greet` - Nom de la fonction
- `(name: string)` - Parametres avec types optionnels
- `: string` - Type de retour optionnel
- `{ ... }` - Corps de la fonction

### Fonctions anonymes

Fonctions sans nom, assignees a des variables :

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Nommee vs. Anonyme :**
```hemlock
// Ces deux sont equivalentes :
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Note :** Les fonctions nommees se transforment en assignations de variables avec des fonctions anonymes.

## Parametres

### Parametres basiques

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Annotations de type

Annotations de type optionnelles sur les parametres :

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // La verification de type a l'execution promeut vers f64
```

**Verification de type :**
- Les types de parametre sont verifies a l'appel si annotes
- Les conversions de type implicites suivent les regles de promotion standard
- Les incompatibilites de type causent des erreurs a l'execution

### Passage par valeur

Tous les arguments sont **copies** (passage par valeur) :

```hemlock
fn modify(x) {
    x = 100;  // Modifie uniquement la copie locale
}

let a = 10;
modify(a);
print(a);  // Toujours 10 (inchange)
```

**Note :** Les objets et tableaux sont passes par reference (la reference est copiee), donc leur contenu peut etre modifie :

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Modifie le tableau original
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (modifie)
```

## Valeurs de retour

### Instruction return

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Annotations de type de retour

Annotation de type optionnelle pour la valeur de retour :

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Verification de type :**
- Les types de retour sont verifies quand la fonction retourne (si annotes)
- Les conversions de type suivent les regles de promotion standard

### Retour implicite

Les fonctions sans annotation de type de retour retournent implicitement `null` :

```hemlock
fn print_message(msg) {
    print(msg);
    // Retourne implicitement null
}

let result = print_message("bonjour");  // result est null
```

### Retour anticipe

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Sortie anticipee
        }
    }
    return -1;  // Non trouve
}
```

### Retour sans valeur

`return;` sans valeur retourne `null` :

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Retourne null
    }
    return value * 2;
}
```

## Fonctions de premiere classe

Les fonctions peuvent etre assignees, passees et retournees comme n'importe quelle autre valeur.

### Fonctions comme variables

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Reassigner
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Fonctions comme arguments

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Fonctions comme valeurs de retour

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Fermetures (Closures)

Les fonctions capturent leur environnement de definition (portee lexicale).

### Fermetures basiques

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

**Comment ca marche :**
- La fonction interne capture `count` de la portee externe
- `count` persiste a travers les appels a la fonction retournee
- Chaque appel a `makeCounter()` cree une nouvelle fermeture avec son propre `count`

### Fermeture avec parametres

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Fermetures multiples

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Portee lexicale

Les fonctions peuvent acceder aux variables de la portee externe via la portee lexicale :

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Peut lire global et outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Les fermetures capturent les variables par reference, permettant la lecture et la modification des variables de la portee externe (comme montre dans l'exemple `makeCounter` ci-dessus).

## Recursivite

Les fonctions peuvent s'appeler elles-memes.

### Recursivite basique

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Recursivite mutuelle

Les fonctions peuvent s'appeler mutuellement :

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Traitement de donnees recursif

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Note :** Pas encore d'optimisation de la recursivite terminale - une recursivite profonde peut causer un debordement de pile.

## Fonctions d'ordre superieur

Fonctions qui prennent ou retournent d'autres fonctions.

### Modele Map

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Modele Filter

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Modele Reduce

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Composition de fonctions

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Modeles courants

### Modele : Fonctions usine (Factory)

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Salut, je suis " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Salut, je suis Alice"
```

### Modele : Fonctions de rappel (Callback)

```hemlock
fn process_async(data, callback) {
    // ... faire le traitement
    callback(data);
}

process_async("test", fn(result) {
    print("Traitement termine : " + result);
});
```

### Modele : Application partielle

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Modele : Memoisation

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Beaucoup plus rapide avec le cache
```

## Semantique des fonctions

### Exigences de type de retour

Les fonctions avec annotation de type de retour **doivent** retourner une valeur :

```hemlock
fn get_value(): i32 {
    // ERREUR : Instruction return manquante
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Verification de type

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Promeut vers f64, retourne f64
add("a", "b");     // Erreur d'execution : type mismatch
```

### Regles de portee

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Peut acceder : inner_var, outer_var, global
    }

    // Peut acceder : outer_var, global
    // Ne peut pas acceder : inner_var
}

// Peut acceder : global
// Ne peut pas acceder : outer_var, inner_var
```

## Bonnes pratiques

1. **Utilisez des annotations de type** - Aide a detecter les erreurs et documente l'intention
2. **Gardez les fonctions petites** - Chaque fonction devrait faire une seule chose
3. **Preferez les fonctions pures** - Evitez les effets de bord quand possible
4. **Nommez les fonctions clairement** - Utilisez des noms de verbes descriptifs
5. **Retournez tot** - Utilisez des clauses de garde pour reduire l'imbrication
6. **Documentez les fermetures complexes** - Rendez les variables capturees explicites
7. **Evitez la recursivite profonde** - Pas encore d'optimisation de la recursivite terminale

## Pieges courants

### Piege : Profondeur de recursivite

```hemlock
// La recursivite profonde peut causer un debordement de pile
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Peut planter avec un debordement de pile
```

### Piege : Modification des variables capturees

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Peut lire et modifier les variables capturees
        return count;
    };
}
```

**Note :** Cela fonctionne, mais soyez conscient que toutes les fermetures partagent le meme environnement capture.

## Exemples

### Exemple : Pipeline de fonctions

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Exemple : Gestionnaire d'evenements

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clique : " + data);
});

trigger_event("click", "button1");
```

### Exemple : Tri avec comparateur personnalise

```hemlock
fn sort(arr, compare) {
    // Tri a bulles avec comparateur personnalise
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Parametres optionnels (arguments par defaut)

Les fonctions peuvent avoir des parametres optionnels avec des valeurs par defaut en utilisant la syntaxe `?:` :

```hemlock
fn greet(name, greeting?: "Bonjour") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Bonjour Alice"
print(greet("Bob", "Salut"));    // "Salut Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Regles :**
- Les parametres optionnels doivent venir apres les parametres requis
- Les valeurs par defaut peuvent etre n'importe quelle expression
- Les arguments omis utilisent la valeur par defaut

## Fonctions variadiques (parametres rest)

Les fonctions peuvent accepter un nombre variable d'arguments en utilisant les parametres rest (`...`) :

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Demarrage", "Execution", "Termine");
// INFO: Demarrage
// INFO: Execution
// INFO: Termine
```

**Regles :**
- Le parametre rest doit etre le dernier parametre
- Le parametre rest collecte tous les arguments restants dans un tableau
- Peut etre combine avec des parametres reguliers et optionnels

## Annotations de type de fonction

Les types de fonction permettent de specifier la signature exacte attendue pour les parametres de fonction et les valeurs de retour :

### Types de fonction basiques

```hemlock
// Syntaxe de type de fonction : fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Types de fonction d'ordre superieur

```hemlock
// Fonction retournant une fonction
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Types de fonction asynchrone

```hemlock
// Type de fonction asynchrone
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Execution asynchrone !");
});
```

### Alias de type de fonction

```hemlock
// Creer des types de fonction nommes pour la clarte
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Parametres const

Le modificateur `const` empeche un parametre d'etre modifie dans la fonction :

### Parametres const basiques

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // ERREUR : cannot mutate const parameter
    for (item in items) {
        print(item);   // OK : la lecture est autorisee
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Immutabilite profonde

Les parametres const appliquent une immutabilite profonde - pas de modification via aucun chemin :

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK : la lecture est autorisee
    // person.name = "Bob";   // ERREUR : cannot mutate
    // person.address.city = "NYC";  // ERREUR : const profond
}
```

### Ce que const empeche

| Type | Bloque par const | Autorise |
|------|------------------|----------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | assignation de champ | lecture de champ |
| buffer | assignation d'index | lecture d'index |
| string | assignation d'index | toutes les methodes (retournent de nouvelles chaines) |

## Arguments nommes

Les fonctions peuvent etre appelees avec des arguments nommes pour plus de clarte et de flexibilite :

### Arguments nommes basiques

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " a " + age + " ans");
}

// Arguments positionnels (traditionnel)
create_user("Alice", 25, false);

// Arguments nommes - peuvent etre dans n'importe quel ordre
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Melanger positionnel et nomme

```hemlock
// Sauter les parametres optionnels en nommant ce dont vous avez besoin
create_user("David", active: false);  // Utilise l'age par defaut=18

// Les arguments nommes doivent venir apres les positionnels
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // ERREUR : positionnel apres nomme
```

### Regles pour les arguments nommes

- Utilisez la syntaxe `name: value` pour les arguments nommes
- Les arguments nommes peuvent apparaitre dans n'importe quel ordre apres les arguments positionnels
- Les arguments positionnels ne peuvent pas suivre les arguments nommes
- Fonctionne avec les parametres par defaut/optionnels
- Les noms de parametre inconnus causent des erreurs a l'execution

## Limitations

Limitations actuelles a connaitre :

- **Pas de passage par reference** - Mot-cle `ref` parse mais pas implemente
- **Pas de surcharge de fonction** - Une fonction par nom
- **Pas d'optimisation de la recursivite terminale** - Recursivite profonde limitee par la taille de la pile

## Sujets connexes

- [Flux de controle](control-flow.md) - Utilisation des fonctions avec les structures de controle
- [Objets](objects.md) - Les methodes sont des fonctions stockees dans les objets
- [Gestion des erreurs](error-handling.md) - Fonctions et gestion des exceptions
- [Types](types.md) - Annotations de type et conversions

## Voir aussi

- **Fermetures** : Voir la section "Functions" de CLAUDE.md pour la semantique des fermetures
- **Valeurs de premiere classe** : Les fonctions sont des valeurs comme n'importe quelle autre
- **Portee lexicale** : Les fonctions capturent leur environnement de definition
