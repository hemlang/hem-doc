# Gestion des erreurs

Hemlock supporte la gestion des erreurs basee sur les exceptions avec `try`, `catch`, `finally`, `throw` et `panic`. Ce guide couvre les erreurs recuperables avec les exceptions et les erreurs irrecuperables avec panic.

## Apercu

```hemlock
// Gestion d'erreur basique
try {
    risky_operation();
} catch (e) {
    print("Erreur: " + e);
}

// Avec nettoyage
try {
    process_file();
} catch (e) {
    print("Echec: " + e);
} finally {
    cleanup();
}

// Lever des erreurs
fn divide(a, b) {
    if (b == 0) {
        throw "division par zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Syntaxe

**Try/catch basique :**
```hemlock
try {
    // code risque
} catch (e) {
    // gerer l'erreur, e contient la valeur levee
}
```

**Try/finally :**
```hemlock
try {
    // code risque
} finally {
    // s'execute toujours, meme si une exception est levee
}
```

**Try/catch/finally :**
```hemlock
try {
    // code risque
} catch (e) {
    // gerer l'erreur
} finally {
    // code de nettoyage
}
```

### Bloc Try

Le bloc try execute les instructions sequentiellement :

```hemlock
try {
    print("Demarrage...");
    risky_operation();
    print("Succes!");  // Seulement si pas d'exception
}
```

**Comportement :**
- Execute les instructions dans l'ordre
- Si une exception est levee : saute au `catch` ou `finally`
- Si pas d'exception : execute `finally` (si present) puis continue

### Bloc Catch

Le bloc catch recoit la valeur levee :

```hemlock
try {
    throw "oups";
} catch (error) {
    print("Attrape: " + error);  // error = "oups"
    // error seulement accessible ici
}
// error non accessible ici
```

**Parametre catch :**
- Recoit la valeur levee (n'importe quel type)
- Portee limitee au bloc catch
- Peut etre nomme n'importe comment (conventionnellement `e`, `err` ou `error`)

**Ce que vous pouvez faire dans catch :**
```hemlock
try {
    risky_operation();
} catch (e) {
    // Logger l'erreur
    print("Erreur: " + e);

    // Relever la meme erreur
    throw e;

    // Lever une erreur differente
    throw "erreur differente";

    // Retourner une valeur par defaut
    return null;

    // Gerer et continuer
    // (pas de throw)
}
```

### Bloc Finally

Le bloc finally **s'execute toujours** :

```hemlock
try {
    print("1: bloc try");
    throw "erreur";
} catch (e) {
    print("2: bloc catch");
} finally {
    print("3: bloc finally");  // S'execute toujours
}
print("4: apres try/catch/finally");

// Sortie : 1: bloc try, 2: bloc catch, 3: bloc finally, 4: apres try/catch/finally
```

**Quand finally s'execute :**
- Apres le bloc try (si pas d'exception)
- Apres le bloc catch (si exception attrapee)
- Meme si try/catch contient `return`, `break` ou `continue`
- Avant que le flux de controle ne quitte le try/catch

**Finally avec return :**
```hemlock
fn example() {
    try {
        return 1;  // Retourne 1 apres que finally s'execute
    } finally {
        print("nettoyage");  // S'execute avant de retourner
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Le return de finally remplace - retourne 2
    }
}
```

**Finally avec flux de controle :**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Break apres que finally s'execute
        }
    } finally {
        print("nettoyage " + typeof(i));
    }
}
```

## Instruction Throw

### Throw basique

Lever n'importe quelle valeur comme exception :

```hemlock
throw "message d'erreur";
throw 404;
throw { code: 500, message: "Erreur interne" };
throw null;
throw ["erreur", "details"];
```

**Execution :**
1. Evalue l'expression
2. Saute immediatement au `catch` englobant le plus proche
3. Si pas de `catch`, propage dans la pile d'appels

### Lever des erreurs

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "L'age ne peut pas etre negatif";
    }
    if (age > 150) {
        throw "L'age est irrealiste";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Erreur de validation: " + e);
}
```

### Lever des objets d'erreur

Creer des informations d'erreur structurees :

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "Le fichier n'existe pas"
        };
    }
    // ... lire le fichier
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("Fichier non trouve: " + e.path);
    }
}
```

### Relever (re-throwing)

Attraper et relever des erreurs :

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Logger erreur: " + e);
        throw e;  // Relever a l'appelant
    }
}

try {
    wrapper();
} catch (e) {
    print("Attrape dans main: " + e);
}
```

## Exceptions non attrapees

Si une exception se propage au sommet de la pile d'appels sans etre attrapee :

```hemlock
fn foo() {
    throw "non attrapee!";
}

foo();  // Plante avec : Runtime error: non attrapee!
```

**Comportement :**
- Le programme plante
- Affiche le message d'erreur sur stderr
- Quitte avec un code de statut non nul
- Trace de pile a ajouter dans les versions futures

## Panic - Erreurs irrecuperables

### Qu'est-ce que Panic ?

`panic()` est pour les **erreurs irrecuperables** qui devraient immediatement terminer le programme :

```hemlock
panic();                    // Message par defaut : "panic!"
panic("message personnalise");    // Message personnalise
panic(42);                  // Les valeurs non-chaine sont affichees
```

**Semantique :**
- **Quitte immediatement** le programme avec code de sortie 1
- Affiche le message d'erreur sur stderr : `panic: <message>`
- **NON attrapable** avec try/catch
- Utiliser pour les bugs et erreurs irrecuperables

### Panic vs Throw

```hemlock
// throw - Erreur recuperable (peut etre attrapee)
try {
    throw "erreur recuperable";
} catch (e) {
    print("Attrape: " + e);  // Attrape avec succes
}

// panic - Erreur irrecuperable (ne peut pas etre attrapee)
try {
    panic("erreur irrecuperable");  // Le programme quitte immediatement
} catch (e) {
    print("Ceci ne s'execute jamais");       // Ne s'execute jamais
}
```

### Quand utiliser Panic

**Utilisez panic pour :**
- **Bugs** : Du code inatteignable a ete atteint
- **Etat invalide** : Corruption de structure de donnees detectee
- **Erreurs irrecuperables** : Ressource critique indisponible
- **Echecs d'assertion** : Quand `assert()` n'est pas suffisant

**Exemples :**
```hemlock
// Code inatteignable
fn process_state(state: i32) {
    if (state == 1) {
        return "pret";
    } else if (state == 2) {
        return "en cours";
    } else if (state == 3) {
        return "arrete";
    } else {
        panic("etat invalide: " + typeof(state));  // Ne devrait jamais arriver
    }
}

// Verification de ressource critique
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json non trouve - impossible de demarrer");
    }
    // ...
}

// Invariant de structure de donnees
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() appele sur pile vide");
    }
    return stack.pop();
}
```

### Quand NE PAS utiliser Panic

**Utilisez throw a la place pour :**
- Validation d'entree utilisateur
- Fichier non trouve
- Erreurs reseau
- Conditions d'erreur attendues

```hemlock
// MAUVAIS : Panic pour erreurs attendues
fn divide(a, b) {
    if (b == 0) {
        panic("division par zero");  // Trop severe
    }
    return a / b;
}

// BON : Throw pour erreurs attendues
fn divide(a, b) {
    if (b == 0) {
        throw "division par zero";  // Recuperable
    }
    return a / b;
}
```

## Interactions avec le flux de controle

### Return dans Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Retourne 1 apres que finally s'execute
    } finally {
        print("nettoyage");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Le return de finally remplace celui de try - retourne 2
    }
}
```

**Regle :** Les valeurs de retour du bloc finally remplacent les valeurs de retour try/catch.

### Break/Continue dans Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Break apres que finally s'execute
    } finally {
        print("nettoyage " + typeof(i));
    }
}
```

**Regle :** Break/continue s'executent apres le bloc finally.

### Try/Catch imbrique

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Attrape: " + e);  // Affiche : Attrape: inner
        throw "outer";  // Releve une erreur differente
    }
} catch (e) {
    print("Attrape: " + e);  // Affiche : Attrape: outer
}
```

**Regle :** Les blocs try/catch imbriques fonctionnent comme attendu, les catches internes arrivent en premier.

## Modeles courants

### Modele : Nettoyage de ressource

Utilisez toujours `finally` pour le nettoyage :

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Erreur lors du traitement du fichier: " + e);
    } finally {
        if (file != null) {
            file.close();  // Ferme toujours, meme en cas d'erreur
        }
    }
}
```

### Modele : Enveloppe d'erreur

Envelopper les erreurs de bas niveau avec du contexte :

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Echec du chargement de config depuis " + path + ": " + e;
    }
}
```

### Modele : Recuperation d'erreur

Fournir une valeur de repli en cas d'erreur :

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "division par zero";
        }
        return a / b;
    } catch (e) {
        print("Erreur: " + e);
        return null;  // Valeur de repli
    }
}
```

### Modele : Validation

Utiliser les exceptions pour la validation :

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Le nom est requis";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Age invalide";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Email invalide";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "invalide" });
} catch (e) {
    print("Validation echouee: " + e);
}
```

### Modele : Types d'erreur multiples

Utiliser des objets d'erreur pour distinguer les types d'erreur :

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Les donnees sont null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Tableau attendu" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Le tableau est vide" };
    }

    // ... traitement
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("Pas de donnees fournies");
    } else if (e.type == "TypeError") {
        print("Mauvais type de donnees: " + e.message);
    } else {
        print("Erreur: " + e.message);
    }
}
```

## Bonnes pratiques

1. **Utilisez les exceptions pour les cas exceptionnels** - Pas pour le flux de controle normal
2. **Levez des erreurs significatives** - Utilisez des chaines ou objets avec contexte
3. **Utilisez toujours finally pour le nettoyage** - Assure que les ressources sont liberees
4. **N'attrapez pas pour ignorer** - Au minimum loggez l'erreur
5. **Relevez quand approprie** - Laissez l'appelant gerer si vous ne pouvez pas
6. **Panic pour les bugs** - Utilisez panic pour les erreurs irrecuperables
7. **Documentez les exceptions** - Rendez clair quelles fonctions peuvent lever

## Pieges courants

### Piege : Avaler les erreurs

```hemlock
// MAUVAIS : Echec silencieux
try {
    risky_operation();
} catch (e) {
    // Erreur ignoree - echec silencieux
}

// BON : Logger ou gerer
try {
    risky_operation();
} catch (e) {
    print("Operation echouee: " + e);
    // Gerer de maniere appropriee
}
```

### Piege : Remplacement par Finally

```hemlock
// MAUVAIS : Finally remplace le return
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Retourne 0, pas 42 !
    }
}

// BON : Ne pas retourner dans finally
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Juste nettoyage, pas de return
    }
}
```

### Piege : Oublier le nettoyage

```hemlock
// MAUVAIS : Le fichier peut ne pas etre ferme en cas d'erreur
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Peut lever
    file.close();  // Jamais atteint si erreur
}

// BON : Utiliser finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Piege : Utiliser Panic pour erreurs attendues

```hemlock
// MAUVAIS : Panic pour erreur attendue
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Fichier de config non trouve");  // Trop severe
    }
    return read_file(path);
}

// BON : Throw pour erreur attendue
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Fichier de config non trouve: " + path;  // Recuperable
    }
    return read_file(path);
}
```

## Exemples

### Exemple : Gestion d'erreur basique

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division par zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Erreur: " + e);  // Affiche : Erreur: division par zero
}
```

### Exemple : Gestion de ressource

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("Fichier copie avec succes");
    } catch (e) {
        print("Echec de la copie du fichier: " + e);
        throw e;  // Relever
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Exemple : Gestion d'erreur imbriquee

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Echec du traitement de l'utilisateur: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Traites: " + typeof(success_count) + " succes, " + typeof(error_count) + " erreurs");
}
```

### Exemple : Types d'erreur personnalises

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a doit etre un nombre", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b doit etre un nombre", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Impossible de diviser par zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Exemple : Logique de reessai

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // Succes !
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation echouee apres " + typeof(max_attempts) + " tentatives: " + e;
            }
            print("Tentative " + typeof(attempt) + " echouee, nouvel essai...");
        }
    }
}

fn unreliable_operation() {
    // Operation peu fiable simulee
    if (random() < 0.7) {
        throw "Operation echouee";
    }
    return "Succes";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("Tous les reessais ont echoue: " + e);
}
```

## Ordre d'execution

Comprendre l'ordre d'execution :

```hemlock
try {
    print("1: debut bloc try");
    throw "erreur";
    print("2: jamais atteint");
} catch (e) {
    print("3: bloc catch");
} finally {
    print("4: bloc finally");
}
print("5: apres try/catch/finally");

// Sortie :
// 1: debut bloc try
// 3: bloc catch
// 4: bloc finally
// 5: apres try/catch/finally
```

## Limitations actuelles

- **Pas de trace de pile** - Les exceptions non attrapees n'affichent pas la trace de pile (prevu)
- **Certaines fonctions integrees quittent** - Certaines fonctions integrees font `exit()` au lieu de lever (a revoir)
- **Pas de types d'exception personnalises** - N'importe quelle valeur peut etre levee, mais pas de hierarchie d'exception formelle

## Sujets connexes

- [Fonctions](functions.md) - Exceptions et retours de fonction
- [Flux de controle](control-flow.md) - Comment les exceptions affectent le flux de controle
- [Memoire](memory.md) - Utiliser finally pour le nettoyage memoire

## Voir aussi

- **Semantique des exceptions** : Voir section "Error Handling" de CLAUDE.md
- **Panic vs Throw** : Cas d'utilisation differents pour types d'erreur differents
- **Garantie Finally** : S'execute toujours, meme avec return/break/continue
