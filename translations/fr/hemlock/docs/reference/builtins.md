# Référence des fonctions intégrées

Référence complète pour toutes les fonctions et constantes intégrées dans Hemlock.

---

## Aperçu

Hemlock fournit un ensemble de fonctions intégrées pour les E/S, l'introspection de types, la gestion de la mémoire, la concurrence et l'interaction système. Toutes les fonctions intégrées sont disponibles globalement sans imports.

---

## Fonctions d'E/S

### print

Affiche des valeurs sur stdout avec un saut de ligne.

**Signature :**
```hemlock
print(...values): null
```

**Paramètres :**
- `...values` - N'importe quel nombre de valeurs à afficher

**Retourne :** `null`

**Exemples :**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// Plusieurs valeurs
print("x =", 10, "y =", 20);
```

**Comportement :**
- Convertit toutes les valeurs en chaînes
- Sépare les valeurs multiples par des espaces
- Ajoute un saut de ligne à la fin
- Vide stdout

---

### read_line

Lit une ligne de texte depuis stdin (entrée utilisateur).

**Signature :**
```hemlock
read_line(): string | null
```

**Paramètres :** Aucun

**Retourne :**
- `string` - La ligne lue depuis stdin (saut de ligne supprimé)
- `null` - En fin de fichier/entrée (EOF)

**Exemples :**
```hemlock
// Invite simple
print("Quel est votre nom ?");
let name = read_line();
print("Bonjour, " + name + "!");

// Lecture de nombres (nécessite un parsing manuel)
print("Entrez un nombre:");
let input = read_line();
let num = parse_int(input);  // Voir ci-dessous pour parse_int
print("Double:", num * 2);

// Gérer EOF
let line = read_line();
if (line == null) {
    print("Fin de l'entrée");
}

// Lire plusieurs lignes
print("Entrez des lignes (Ctrl+D pour arrêter):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("Vous avez dit:", line);
}
```

**Comportement :**
- Bloque jusqu'à ce que l'utilisateur appuie sur Entrée
- Supprime le saut de ligne final (`\n`) et le retour chariot (`\r`)
- Retourne `null` en EOF (Ctrl+D sur Unix, Ctrl+Z sur Windows)
- Lit depuis stdin uniquement (pas depuis les fichiers)

**Parsing de l'entrée utilisateur :**

Comme `read_line()` retourne toujours une chaîne, vous devez parser l'entrée numérique manuellement :

```hemlock
// Parseur d'entiers simple
fn parse_int(s: string): i32 {
    let result: i32 = 0;
    let negative = false;
    let i = 0;

    if (s.length > 0 && s.char_at(0) == '-') {
        negative = true;
        i = 1;
    }

    while (i < s.length) {
        let c = s.char_at(i);
        let code: i32 = c;
        if (code >= 48 && code <= 57) {
            result = result * 10 + (code - 48);
        } else {
            break;
        }
        i = i + 1;
    }

    if (negative) {
        return -result;
    }
    return result;
}

// Utilisation
print("Entrez votre âge:");
let age = parse_int(read_line());
print("Dans 10 ans vous aurez", age + 10);
```

**Voir aussi :** [API File](file-api.md) pour la lecture depuis les fichiers

---

### eprint

Affiche une valeur sur stderr avec un saut de ligne.

**Signature :**
```hemlock
eprint(value: any): null
```

**Paramètres :**
- `value` - Une seule valeur à afficher sur stderr

**Retourne :** `null`

**Exemples :**
```hemlock
eprint("Erreur: fichier non trouvé");
eprint(404);
eprint("Avertissement: " + message);

// Modèle typique de gestion d'erreur
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Erreur: fichier de configuration non trouvé: " + path);
        return null;
    }
    // ...
}
```

**Comportement :**
- Affiche sur stderr (flux d'erreur standard)
- Ajoute un saut de ligne à la fin
- N'accepte qu'un seul argument (contrairement à `print`)
- Utile pour les messages d'erreur qui ne doivent pas se mélanger avec la sortie normale

**Différence avec print :**
- `print()` → stdout (sortie normale, peut être redirigée avec `>`)
- `eprint()` → stderr (sortie d'erreur, peut être redirigée avec `2>`)

```bash
# Exemple shell: séparer stdout et stderr
./hemlock script.hml > output.txt 2> errors.txt
```

---

## Introspection de types

### typeof

Obtient le nom du type d'une valeur.

**Signature :**
```hemlock
typeof(value: any): string
```

**Paramètres :**
- `value` - N'importe quelle valeur

**Retourne :** Nom du type sous forme de chaîne

**Exemples :**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// Objets typés
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// Autres types
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**Noms de types :**
- Primitifs : `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Composites : `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Spéciaux : `"file"`, `"task"`, `"channel"`
- Personnalisés : Noms de types définis par l'utilisateur avec `define`

**Voir aussi :** [Système de types](type-system.md)

---

## Exécution de commandes

### exec

Exécute une commande shell et capture la sortie.

**Signature :**
```hemlock
exec(command: string): object
```

**Paramètres :**
- `command` - Commande shell à exécuter

**Retourne :** Objet avec les champs :
- `output` (string) - stdout de la commande
- `exit_code` (i32) - Code de statut de sortie (0 = succès)

**Exemples :**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// Vérifier le statut de sortie
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Trouvé:", r.output);
} else {
    print("Motif non trouvé");
}

// Traiter une sortie multi-lignes
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**Comportement :**
- Exécute la commande via `/bin/sh`
- Capture stdout uniquement (stderr va au terminal)
- Bloque jusqu'à ce que la commande se termine
- Retourne une chaîne vide s'il n'y a pas de sortie

**Gestion des erreurs :**
```hemlock
try {
    let r = exec("nonexistent_command");
} catch (e) {
    print("Échec d'exécution:", e);
}
```

**Avertissement de sécurité :** ⚠️ Vulnérable à l'injection shell. Toujours valider/assainir l'entrée utilisateur.

**Limitations :**
- Pas de capture de stderr
- Pas de streaming
- Pas de timeout
- Pas de gestion des signaux

---

### exec_argv

Exécute une commande avec un tableau d'arguments explicite (pas d'interprétation shell).

**Signature :**
```hemlock
exec_argv(argv: array): object
```

**Paramètres :**
- `argv` - Tableau de chaînes : `[commande, arg1, arg2, ...]`

**Retourne :** Objet avec les champs :
- `output` (string) - stdout de la commande
- `exit_code` (i32) - Code de statut de sortie (0 = succès)

**Exemples :**
```hemlock
// Commande simple
let result = exec_argv(["ls", "-la"]);
print(result.output);

// Commande avec arguments contenant des espaces (sûr !)
let r = exec_argv(["grep", "hello world", "file.txt"]);

// Exécuter un script avec arguments
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**Différence avec exec :**
```hemlock
// exec() utilise le shell - NON SÛR avec l'entrée utilisateur
exec("ls " + user_input);  // Risque d'injection shell !

// exec_argv() contourne le shell - SÛR
exec_argv(["ls", user_input]);  // Pas d'injection possible
```

**Quand utiliser :**
- Quand les arguments contiennent des espaces, guillemets ou caractères spéciaux
- Lors du traitement de l'entrée utilisateur (sécurité)
- Quand vous avez besoin d'un parsing d'arguments prévisible

**Voir aussi :** `exec()` pour les commandes shell simples

---

## Gestion des erreurs

### throw

Lève une exception.

**Signature :**
```hemlock
throw expression
```

**Paramètres :**
- `expression` - Valeur à lever (n'importe quel type)

**Retourne :** Ne retourne jamais (transfère le contrôle)

**Exemples :**
```hemlock
throw "message d'erreur";
throw 404;
throw { code: 500, message: "Erreur interne" };
throw null;
```

**Voir aussi :** instructions try/catch/finally

---

### panic

Termine immédiatement le programme avec un message d'erreur (irrécupérable).

**Signature :**
```hemlock
panic(message?: any): never
```

**Paramètres :**
- `message` (optionnel) - Message d'erreur à afficher

**Retourne :** Ne retourne jamais (le programme se termine)

**Exemples :**
```hemlock
panic();                          // Par défaut: "panic!"
panic("code inaccessible atteint");
panic(42);

// Cas d'utilisation courant
fn process_state(state: i32): string {
    if (state == 1) { return "prêt"; }
    if (state == 2) { return "en cours"; }
    panic("état invalide: " + typeof(state));
}
```

**Comportement :**
- Affiche l'erreur sur stderr : `panic: <message>`
- Quitte avec le code 1
- **NON rattrapable** avec try/catch
- Utiliser pour les bugs et erreurs irrécupérables

**Panic vs Throw :**
- `panic()` - Erreur irrécupérable, quitte immédiatement
- `throw` - Erreur récupérable, peut être rattrapée

---

### assert

Affirme qu'une condition est vraie, ou termine avec un message d'erreur.

**Signature :**
```hemlock
assert(condition: any, message?: string): null
```

**Paramètres :**
- `condition` - Valeur à vérifier pour la véracité
- `message` (optionnel) - Message d'erreur personnalisé si l'assertion échoue

**Retourne :** `null` (si l'assertion réussit)

**Exemples :**
```hemlock
// Assertions basiques
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "Le tableau ne doit pas être vide");

// Avec messages personnalisés
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Division par zéro");
    return a / b;
}

// Valider les arguments de fonction
fn process_data(data: array) {
    assert(data != null, "data ne peut pas être null");
    assert(data.length > 0, "data ne peut pas être vide");
    // ...
}
```

**Comportement :**
- Si la condition est vraie : retourne `null`, l'exécution continue
- Si la condition est fausse : affiche l'erreur et quitte avec le code 1
- Valeurs fausses : `false`, `0`, `0.0`, `null`, `""` (chaîne vide)
- Valeurs vraies : tout le reste

**Sortie en cas d'échec :**
```
Assertion failed: Le tableau ne doit pas être vide
```

**Quand utiliser :**
- Validation des préconditions de fonction
- Vérification des invariants pendant le développement
- Attraper les erreurs de programmation tôt

**assert vs panic :**
- `assert(cond, msg)` - Vérifie une condition, échoue si fausse
- `panic(msg)` - Échoue toujours inconditionnellement

---

## Gestion des signaux

### signal

Enregistre ou réinitialise un gestionnaire de signal.

**Signature :**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**Paramètres :**
- `signum` - Numéro de signal (utiliser des constantes comme `SIGINT`)
- `handler` - Fonction à appeler quand le signal est reçu, ou `null` pour réinitialiser par défaut

**Retourne :** Fonction gestionnaire précédente, ou `null`

**Exemples :**
```hemlock
fn handle_interrupt(sig) {
    print("SIGINT intercepté !");
}

signal(SIGINT, handle_interrupt);

// Réinitialiser par défaut
signal(SIGINT, null);
```

**Signature du gestionnaire :**
```hemlock
fn handler(signum: i32) {
    // signum contient le numéro du signal
}
```

**Voir aussi :**
- [Constantes de signal](#constantes-de-signal)
- `raise()`

---

### raise

Envoie un signal au processus courant.

**Signature :**
```hemlock
raise(signum: i32): null
```

**Paramètres :**
- `signum` - Numéro de signal à lever

**Retourne :** `null`

**Exemples :**
```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

raise(SIGUSR1);
raise(SIGUSR1);
print(count);  // 2
```

---

## Variables globales

### args

Tableau des arguments de ligne de commande.

**Type :** `array` de chaînes

**Structure :**
- `args[0]` - Nom du fichier script
- `args[1..n]` - Arguments de ligne de commande

**Exemples :**
```bash
# Commande: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// Itérer sur les arguments
let i = 1;
while (i < args.length) {
    print("Argument", i, ":", args[i]);
    i = i + 1;
}
```

**Comportement REPL :** Dans le REPL, `args.length` est 0 (tableau vide)

---

## Constantes de signal

Constantes de signal POSIX standard (valeurs i32) :

### Interruption et terminaison

| Constante  | Valeur | Description                            |
|------------|--------|----------------------------------------|
| `SIGINT`   | 2      | Interruption depuis le clavier (Ctrl+C)|
| `SIGTERM`  | 15     | Demande de terminaison                 |
| `SIGQUIT`  | 3      | Quitter depuis le clavier (Ctrl+\)     |
| `SIGHUP`   | 1      | Déconnexion détectée sur le terminal   |
| `SIGABRT`  | 6      | Signal d'abandon                       |

### Définis par l'utilisateur

| Constante  | Valeur | Description                |
|------------|--------|----------------------------|
| `SIGUSR1`  | 10     | Signal défini par l'utilisateur 1 |
| `SIGUSR2`  | 12     | Signal défini par l'utilisateur 2 |

### Contrôle de processus

| Constante  | Valeur | Description                     |
|------------|--------|---------------------------------|
| `SIGALRM`  | 14     | Minuterie d'alarme              |
| `SIGCHLD`  | 17     | Changement de statut du processus enfant |
| `SIGCONT`  | 18     | Continuer si arrêté             |
| `SIGSTOP`  | 19     | Arrêter le processus (ne peut pas être intercepté) |
| `SIGTSTP`  | 20     | Arrêt terminal (Ctrl+Z)         |

### E/S

| Constante  | Valeur | Description                        |
|------------|--------|------------------------------------|
| `SIGPIPE`  | 13     | Pipe cassé                         |
| `SIGTTIN`  | 21     | Lecture en arrière-plan depuis le terminal |
| `SIGTTOU`  | 22     | Écriture en arrière-plan vers le terminal |

**Exemples :**
```hemlock
fn handle_signal(sig) {
    if (sig == SIGINT) {
        print("Interruption détectée");
    }
    if (sig == SIGTERM) {
        print("Terminaison demandée");
    }
}

signal(SIGINT, handle_signal);
signal(SIGTERM, handle_signal);
```

**Note :** `SIGKILL` (9) et `SIGSTOP` (19) ne peuvent pas être interceptés ou ignorés.

---

## Fonctions mathématiques/arithmétiques

### div

Division entière (floor) retournant un flottant.

**Signature :**
```hemlock
div(a: number, b: number): f64
```

**Paramètres :**
- `a` - Dividende
- `b` - Diviseur

**Retourne :** Partie entière de `a / b` sous forme de flottant (f64)

**Exemples :**
```hemlock
let result = div(7, 2);    // 3.0 (pas 3.5)
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0 (floor arrondit vers l'infini négatif)
```

**Note :** Dans Hemlock, l'opérateur `/` retourne toujours un flottant. Utilisez `div()` pour la division entière quand vous avez besoin de la partie entière sous forme de flottant, ou `divi()` quand vous avez besoin d'un résultat entier.

---

### divi

Division entière (floor) retournant un entier.

**Signature :**
```hemlock
divi(a: number, b: number): i64
```

**Paramètres :**
- `a` - Dividende
- `b` - Diviseur

**Retourne :** Partie entière de `a / b` sous forme d'entier (i64)

**Exemples :**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4 (floor arrondit vers l'infini négatif)
```

**Comparaison :**
```hemlock
print(7 / 2);      // 3.5 (division régulière, toujours flottant)
print(div(7, 2));  // 3.0 (division entière, résultat flottant)
print(divi(7, 2)); // 3   (division entière, résultat entier)
```

---

## Fonctions de gestion de la mémoire

Voir [API Memory](memory-api.md) pour la référence complète :
- `alloc(size)` - Allouer de la mémoire brute
- `free(ptr)` - Libérer la mémoire
- `buffer(size)` - Allouer un buffer sécurisé
- `memset(ptr, byte, size)` - Remplir la mémoire
- `memcpy(dest, src, size)` - Copier la mémoire
- `realloc(ptr, new_size)` - Redimensionner l'allocation

### sizeof

Obtient la taille d'un type en octets.

**Signature :**
```hemlock
sizeof(type): i32
```

**Paramètres :**
- `type` - Une constante de type (`i32`, `f64`, `ptr`, etc.) ou une chaîne de nom de type

**Retourne :** Taille en octets sous forme de `i32`

**Exemples :**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// Utilisation des alias de type
print(sizeof(byte));     // 1 (identique à u8)
print(sizeof(integer));  // 4 (identique à i32)
print(sizeof(number));   // 8 (identique à f64)

// La forme chaîne fonctionne aussi
print(sizeof("i32"));    // 4
```

**Types supportés :**
| Type | Taille | Alias |
|------|--------|-------|
| `i8` | 1 | - |
| `i16` | 2 | - |
| `i32` | 4 | `integer` |
| `i64` | 8 | - |
| `u8` | 1 | `byte` |
| `u16` | 2 | - |
| `u32` | 4 | - |
| `u64` | 8 | - |
| `f32` | 4 | - |
| `f64` | 8 | `number` |
| `ptr` | 8 | - |
| `rune` | 4 | - |
| `bool` | 1 | - |

**Voir aussi :** `talloc()` pour l'allocation typée

---

### talloc

Alloue de la mémoire pour un tableau typé (allocation sensible au type).

**Signature :**
```hemlock
talloc(type, count: i32): ptr
```

**Paramètres :**
- `type` - Une constante de type (`i32`, `f64`, `ptr`, etc.)
- `count` - Nombre d'éléments à allouer

**Retourne :** `ptr` vers la mémoire allouée, ou `null` en cas d'échec

**Exemples :**
```hemlock
// Allouer tableau de 10 i32 (40 octets)
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// Allouer tableau de 5 f64 (40 octets)
let float_arr = talloc(f64, 5);

// Allouer tableau de 100 octets
let byte_arr = talloc(u8, 100);

// N'oubliez pas de libérer !
free(int_arr);
free(float_arr);
free(byte_arr);
```

**Comparaison avec alloc :**
```hemlock
// Ces deux sont équivalents:
let p1 = talloc(i32, 10);      // Sensible au type: 10 i32
let p2 = alloc(sizeof(i32) * 10);  // Calcul manuel

// talloc est plus clair et moins sujet aux erreurs
```

**Gestion des erreurs :**
- Retourne `null` si l'allocation échoue
- Quitte avec erreur si count n'est pas positif
- Vérifie le dépassement de taille (count * element_size)

**Voir aussi :** `alloc()`, `sizeof()`, `free()`

---

## Helpers de pointeurs FFI

Ces fonctions aident à lire et écrire des valeurs typées dans la mémoire brute, utiles pour FFI et la manipulation de mémoire de bas niveau.

### ptr_null

Crée un pointeur null.

**Signature :**
```hemlock
ptr_null(): ptr
```

**Retourne :** Un pointeur null

**Exemple :**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Le pointeur est null");
}
```

---

### ptr_offset

Calcule le décalage de pointeur (arithmétique de pointeur).

**Signature :**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**Paramètres :**
- `ptr` - Pointeur de base
- `index` - Index de l'élément
- `element_size` - Taille de chaque élément en octets

**Retourne :** Pointeur vers l'élément à l'index donné

**Exemple :**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### Fonctions de lecture de pointeur

Lisent des valeurs typées depuis la mémoire.

| Fonction | Signature | Retourne | Description |
|----------|-----------|----------|-------------|
| `ptr_read_i8` | `(ptr)` | `i8` | Lire entier signé 8 bits |
| `ptr_read_i16` | `(ptr)` | `i16` | Lire entier signé 16 bits |
| `ptr_read_i32` | `(ptr)` | `i32` | Lire entier signé 32 bits |
| `ptr_read_i64` | `(ptr)` | `i64` | Lire entier signé 64 bits |
| `ptr_read_u8` | `(ptr)` | `u8` | Lire entier non signé 8 bits |
| `ptr_read_u16` | `(ptr)` | `u16` | Lire entier non signé 16 bits |
| `ptr_read_u32` | `(ptr)` | `u32` | Lire entier non signé 32 bits |
| `ptr_read_u64` | `(ptr)` | `u64` | Lire entier non signé 64 bits |
| `ptr_read_f32` | `(ptr)` | `f32` | Lire flottant 32 bits |
| `ptr_read_f64` | `(ptr)` | `f64` | Lire flottant 64 bits |
| `ptr_read_ptr` | `(ptr)` | `ptr` | Lire valeur de pointeur |

**Exemple :**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### Fonctions d'écriture de pointeur

Écrivent des valeurs typées dans la mémoire.

| Fonction | Signature | Retourne | Description |
|----------|-----------|----------|-------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | Écrire entier signé 8 bits |
| `ptr_write_i16` | `(ptr, value)` | `null` | Écrire entier signé 16 bits |
| `ptr_write_i32` | `(ptr, value)` | `null` | Écrire entier signé 32 bits |
| `ptr_write_i64` | `(ptr, value)` | `null` | Écrire entier signé 64 bits |
| `ptr_write_u8` | `(ptr, value)` | `null` | Écrire entier non signé 8 bits |
| `ptr_write_u16` | `(ptr, value)` | `null` | Écrire entier non signé 16 bits |
| `ptr_write_u32` | `(ptr, value)` | `null` | Écrire entier non signé 32 bits |
| `ptr_write_u64` | `(ptr, value)` | `null` | Écrire entier non signé 64 bits |
| `ptr_write_f32` | `(ptr, value)` | `null` | Écrire flottant 32 bits |
| `ptr_write_f64` | `(ptr, value)` | `null` | Écrire flottant 64 bits |
| `ptr_write_ptr` | `(ptr, value)` | `null` | Écrire valeur de pointeur |

**Exemple :**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### Conversion buffer/pointeur

#### buffer_ptr

Obtient le pointeur brut depuis un buffer.

**Signature :**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**Exemple :**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// Maintenant p pointe vers la même mémoire que buf
```

#### ptr_to_buffer

Crée un wrapper buffer autour d'un pointeur brut.

**Signature :**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**Exemple :**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // Maintenant a une vérification des limites
// Note: libérer buf libérera la mémoire sous-jacente
```

---

## Fonctions d'E/S fichier

Voir [API File](file-api.md) pour la référence complète :
- `open(path, mode?)` - Ouvrir un fichier

---

## Fonctions de concurrence

Voir [API Concurrency](concurrency-api.md) pour la référence complète :
- `spawn(fn, args...)` - Lancer une tâche
- `join(task)` - Attendre une tâche
- `detach(task)` - Détacher une tâche
- `channel(capacity)` - Créer un canal

### apply

Appelle une fonction dynamiquement avec un tableau d'arguments.

**Signature :**
```hemlock
apply(fn: function, args: array): any
```

**Paramètres :**
- `fn` - La fonction à appeler
- `args` - Tableau d'arguments à passer à la fonction

**Retourne :** La valeur de retour de la fonction appelée

**Exemples :**
```hemlock
fn add(a, b) {
    return a + b;
}

// Appeler avec un tableau d'arguments
let result = apply(add, [2, 3]);
print(result);  // 5

// Dispatch dynamique
let operations = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calculate(op: string, args: array) {
    return apply(operations[op], args);
}

print(calculate("add", [10, 5]));  // 15
print(calculate("mul", [10, 5]));  // 50
print(calculate("sub", [10, 5]));  // 5

// Arguments variables
fn sum(...nums) {
    let total = 0;
    for (n in nums) {
        total = total + n;
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5];
print(apply(sum, numbers));  // 15
```

**Cas d'utilisation :**
- Dispatch dynamique de fonction basé sur des valeurs à l'exécution
- Appel de fonctions avec des listes d'arguments variables
- Implémentation d'utilitaires d'ordre supérieur (map, filter, etc.)
- Systèmes de plugins/extensions

---

### select

Attend des données de plusieurs canaux, retourne quand l'un a des données.

**Signature :**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Paramètres :**
- `channels` - Tableau de valeurs de canal
- `timeout_ms` (optionnel) - Timeout en millisecondes (-1 ou omettre pour infini)

**Retourne :**
- `{ channel, value }` - Objet avec le canal qui avait des données et la valeur reçue
- `null` - En cas de timeout

**Exemples :**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Tâches productrices
spawn(fn() {
    sleep(100);
    ch1.send("du canal 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("du canal 2");
});

// Attendre le premier message
let result = select([ch1, ch2]);
print(result.value);  // "du canal 2" (arrivé en premier)

// Avec timeout
let result2 = select([ch1, ch2], 1000);  // Attendre jusqu'à 1 seconde
if (result2 == null) {
    print("Timeout - pas de données reçues");
} else {
    print("Reçu:", result2.value);
}

// Boucle de select continue
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("Pas d'activité depuis 5 secondes");
        break;
    }
    print("Message reçu:", msg.value);
}
```

**Comportement :**
- Bloque jusqu'à ce qu'un canal ait des données ou que le timeout expire
- Retourne immédiatement si un canal a déjà des données
- Si le canal est fermé et vide, retourne `{ channel, value: null }`
- Interroge les canaux dans l'ordre (le premier canal prêt gagne)

**Cas d'utilisation :**
- Multiplexage de plusieurs producteurs
- Implémentation de timeouts sur les opérations de canal
- Construction de boucles d'événements avec plusieurs sources

---

## Tableau récapitulatif

### Fonctions

| Fonction   | Catégorie        | Retourne     | Description                          |
|------------|------------------|--------------|--------------------------------------|
| `print`    | E/S              | `null`       | Afficher sur stdout                  |
| `read_line`| E/S              | `string?`    | Lire une ligne depuis stdin          |
| `eprint`   | E/S              | `null`       | Afficher sur stderr                  |
| `typeof`   | Type             | `string`     | Obtenir le nom du type               |
| `exec`     | Commande         | `object`     | Exécuter une commande shell          |
| `exec_argv`| Commande         | `object`     | Exécuter avec tableau d'arguments    |
| `assert`   | Erreur           | `null`       | Affirmer une condition ou quitter    |
| `panic`    | Erreur           | `never`      | Erreur irrécupérable (quitte)        |
| `signal`   | Signal           | `function?`  | Enregistrer un gestionnaire de signal|
| `raise`    | Signal           | `null`       | Envoyer un signal au processus       |
| `alloc`    | Mémoire          | `ptr`        | Allouer de la mémoire brute          |
| `talloc`   | Mémoire          | `ptr`        | Allocation typée                     |
| `sizeof`   | Mémoire          | `i32`        | Obtenir la taille du type en octets  |
| `free`     | Mémoire          | `null`       | Libérer la mémoire                   |
| `buffer`   | Mémoire          | `buffer`     | Allouer un buffer sécurisé           |
| `memset`   | Mémoire          | `null`       | Remplir la mémoire                   |
| `memcpy`   | Mémoire          | `null`       | Copier la mémoire                    |
| `realloc`  | Mémoire          | `ptr`        | Redimensionner l'allocation          |
| `open`     | E/S fichier      | `file`       | Ouvrir un fichier                    |
| `spawn`    | Concurrence      | `task`       | Lancer une tâche concurrente         |
| `join`     | Concurrence      | `any`        | Attendre le résultat de la tâche     |
| `detach`   | Concurrence      | `null`       | Détacher la tâche                    |
| `channel`  | Concurrence      | `channel`    | Créer un canal de communication      |
| `select`   | Concurrence      | `object?`    | Attendre sur plusieurs canaux        |
| `apply`    | Fonctions        | `any`        | Appeler fonction avec tableau d'args |

### Variables globales

| Variable   | Type     | Description                       |
|------------|----------|-----------------------------------|
| `args`     | `array`  | Arguments de ligne de commande    |

### Constantes

| Constante  | Type  | Catégorie | Valeur | Description               |
|------------|-------|-----------|--------|---------------------------|
| `SIGINT`   | `i32` | Signal    | 2      | Interruption clavier      |
| `SIGTERM`  | `i32` | Signal    | 15     | Demande de terminaison    |
| `SIGQUIT`  | `i32` | Signal    | 3      | Quitter clavier           |
| `SIGHUP`   | `i32` | Signal    | 1      | Déconnexion               |
| `SIGABRT`  | `i32` | Signal    | 6      | Abandon                   |
| `SIGUSR1`  | `i32` | Signal    | 10     | Défini par l'utilisateur 1|
| `SIGUSR2`  | `i32` | Signal    | 12     | Défini par l'utilisateur 2|
| `SIGALRM`  | `i32` | Signal    | 14     | Minuterie d'alarme        |
| `SIGCHLD`  | `i32` | Signal    | 17     | Changement statut enfant  |
| `SIGCONT`  | `i32` | Signal    | 18     | Continuer                 |
| `SIGSTOP`  | `i32` | Signal    | 19     | Arrêt (non interceptable) |
| `SIGTSTP`  | `i32` | Signal    | 20     | Arrêt terminal            |
| `SIGPIPE`  | `i32` | Signal    | 13     | Pipe cassé                |
| `SIGTTIN`  | `i32` | Signal    | 21     | Lecture terminal en arrière-plan |
| `SIGTTOU`  | `i32` | Signal    | 22     | Écriture terminal en arrière-plan |

---

## Voir aussi

- [Système de types](type-system.md) - Types et conversions
- [API Memory](memory-api.md) - Fonctions d'allocation mémoire
- [API File](file-api.md) - Fonctions d'E/S fichier
- [API Concurrency](concurrency-api.md) - Fonctions async/concurrence
- [API String](string-api.md) - Méthodes des chaînes
- [API Array](array-api.md) - Méthodes des tableaux
