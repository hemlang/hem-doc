# Philosophie de conception du langage Hemlock

> "Un petit langage non securise pour ecrire des choses non securisees en toute securite."

Ce document presente les principes fondamentaux de conception pour les assistants IA travaillant avec Hemlock.
Pour une documentation detaillee, consultez `docs/README.md` et le repertoire `stdlib/docs/`.

---

## Identite fondamentale

Hemlock est un **langage de script systeme** avec gestion manuelle de la memoire et controle explicite :
- La puissance du C avec l'ergonomie des langages de script modernes
- Concurrence asynchrone structuree integree
- Aucun comportement cache ni magie

**Hemlock N'EST PAS :** Un langage securise en memoire, un langage avec ramasse-miettes (GC), ni un langage qui cache la complexite.
**Hemlock EST :** Explicite plutot qu'implicite, educatif, une "couche de script C" pour le travail systeme.

---

## Principes de conception

### 1. Explicite plutot qu'implicite
- Points-virgules obligatoires (pas d'ASI)
- Gestion manuelle de la memoire (alloc/free)
- Annotations de type optionnelles mais verifiees a l'execution

### 2. Dynamique par defaut, type par choix
- Chaque valeur possede une etiquette de type a l'execution
- Les litteraux inferent les types : `42` -> i32, `5000000000` -> i64, `3.14` -> f64
- Les annotations de type optionnelles imposent des verifications a l'execution

### 3. Non securise est une fonctionnalite
- Arithmetique de pointeurs autorisee (responsabilite de l'utilisateur)
- Pas de verification des limites sur les `ptr` bruts (utilisez `buffer` pour la securite)
- Les double-free peuvent provoquer des plantages

### 4. Concurrence structuree de premiere classe
- `async`/`await` integres avec parallelisme base sur pthread
- Canaux (channels) pour la communication
- `spawn`/`join`/`detach` pour la gestion des taches

### 5. Syntaxe proche du C
- Blocs `{}` toujours requis
- Commentaires : `// ligne` et `/* bloc */`
- Operateurs identiques au C : `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Increment/decrement : `++x`, `x++`, `--x`, `x--` (prefixe et postfixe)
- Affectation composee : `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` retourne toujours un flottant (utilisez `divi()` pour la division entiere)
- Syntaxe de type : `let x: type = valeur;`

---

## Reference rapide

### Types
```
Signes:     i8, i16, i32, i64
Non signes: u8, u16, u32, u64
Flottants:  f32, f64
Autres:     bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Alias:      integer (i32), number (f64), byte (u8)
```

**Promotion de type :** i8 -> i16 -> i32 -> i64 -> f32 -> f64 (les flottants gagnent toujours, mais i64/u64 + f32 -> f64 pour preserver la precision)

### Litteraux
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> max i32)
let hex = 0xDEADBEEF;    // litteral hexadecimal
let bin = 0b1010;        // litteral binaire
let oct = 0o777;         // litteral octal
let sep = 1_000_000;     // separateurs numeriques autorises
let pi = 3.14;           // f64
let half = .5;           // f64 (sans zero initial)
let s = "hello";         // string (chaine)
let esc = "\x41\u{1F600}"; // echappements hex et unicode
let ch = 'A';            // rune
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array (tableau)
let obj = { x: 10 };     // object (objet)
```

### Conversion de type
```hemlock
// Fonctions constructeurs de type - analysent les chaines vers les types
let n = i32("42");       // Analyse une chaine vers i32
let f = f64("3.14");     // Analyse une chaine vers f64
let b = bool("true");    // Analyse une chaine vers bool ("true" ou "false")

// Tous les types numeriques sont supportes
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// Nombres hexadecimaux et negatifs
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// Les alias de type fonctionnent aussi
let x = integer("100");  // Equivalent a i32("100")
let y = number("1.5");   // Equivalent a f64("1.5")
let z = byte("200");     // Equivalent a u8("200")

// Convertir entre types numeriques
let big = i64(42);       // i32 vers i64
let truncated = i32(3.99); // f64 vers i32 (tronque a 3)

// Les annotations de type valident les types (mais n'analysent pas les chaines)
let f: f64 = 100;        // i32 vers f64 via annotation (coercition numerique OK)
// let n: i32 = "42";    // ERREUR - utilisez i32("42") pour l'analyse de chaine
```

### Introspection
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5 (longueur de la chaine en octets)
len([1, 2, 3]);          // 3 (longueur du tableau)
```

### Memoire
```hemlock
let p = alloc(64);       // pointeur brut
let b = buffer(64);      // tampon securise (verification des limites)
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // nettoyage manuel requis
```

### Flux de controle
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // boucle infinie (plus propre que while(true))
switch (x) { case 1: break; default: break; }  // style C avec fall-through
defer cleanup();         // s'execute quand la fonction retourne

// Etiquettes de boucle pour break/continue cibles dans les boucles imbriquees
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // sort de la boucle externe
        if (i == 3) { continue outer; }  // continue la boucle externe
    }
}
```

### Pattern matching (Filtrage par motif)
```hemlock
// Expression match - retourne une valeur
let result = match (value) {
    0 => "zero",                    // Motif litteral
    1 | 2 | 3 => "petit",           // Motif OU
    n if n < 10 => "moyen",         // Expression de garde
    n => "grand: " + n              // Liaison de variable
};

// Motifs de type
match (val) {
    n: i32 => "entier",
    s: string => "chaine",
    _ => "autre"                    // Joker (Wildcard)
}

// Destructuration d'objet
match (point) {
    { x: 0, y: 0 } => "origine",
    { x, y } => "a " + x + "," + y
}

// Destructuration de tableau avec reste
match (arr) {
    [] => "vide",
    [first, ...rest] => "tete: " + first,
    _ => "autre"
}

// Motifs imbriques
match (user) {
    { name, address: { city } } => name + " a " + city
}
```

Voir `docs/language-guide/pattern-matching.md` pour la documentation complete.

### Operateurs de coalescence null
```hemlock
// Coalescence null (??) - retourne gauche si non-null, sinon droite
let name = user.name ?? "Anonyme";
let first = a ?? b ?? c ?? "defaut";

// Affectation avec coalescence null (??=) - affecte seulement si null
let config = null;
config ??= { timeout: 30 };    // config est maintenant { timeout: 30 }
config ??= { timeout: 60 };    // config inchange (non null)

// Fonctionne avec les proprietes et indices
obj.field ??= "defaut";
arr[0] ??= "premier";

// Navigation securisee (?.) - retourne null si l'objet est null
let city = user?.address?.city;  // null si une partie est null
let upper = name?.to_upper();    // appel de methode securise
let item = arr?.[0];             // indexation securisee
```

### Fonctions
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Bonjour") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonyme/closure

// Fonctions a corps d'expression (syntaxe fleche)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // anonyme avec corps d'expression

// Modificateurs de parametres
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // passage par reference
fn print_all(const items: array) { for (i in items) { print(i); } }  // immuable
```

### Arguments nommes
```hemlock
// Les fonctions peuvent etre appelees avec des arguments nommes
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " a " + age + " ans");
}

// Arguments positionnels (traditionnel)
create_user("Alice", 25, false);

// Arguments nommes - peuvent etre dans n'importe quel ordre
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Sauter les parametres optionnels en nommant ce dont vous avez besoin
create_user("David", active: false);  // Utilise age=18 par defaut

// Les arguments nommes doivent venir apres les arguments positionnels
create_user("Eve", age: 21);          // OK : positionnel puis nomme
// create_user(name: "Bad", 25);      // ERREUR : positionnel apres nomme
```

**Regles :**
- Les arguments nommes utilisent la syntaxe `nom: valeur`
- Peuvent apparaitre dans n'importe quel ordre apres les arguments positionnels
- Les arguments positionnels ne peuvent pas suivre les arguments nommes
- Fonctionne avec les parametres par defaut/optionnels
- Les noms de parametres inconnus causent des erreurs a l'execution

### Objets et enumerations
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// Syntaxe raccourcie pour les objets (style ES6)
let name = "Alice";
let age = 30;
let person = { name, age };         // equivalent a { name: name, age: age }

// Operateur de propagation d'objet (spread)
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // copie defaults, remplace size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Types composes (Intersection/Duck Types)
```hemlock
// Definir des types structurels
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Type compose : l'objet doit satisfaire TOUS les types
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Parametres de fonction avec types composes
fn greet(p: HasName & HasAge) {
    print(p.name + " a " + p.age + " ans");
}

// Trois types ou plus
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Champs supplementaires autorises (duck typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Ingenierie"  // OK - champs supplementaires ignores
};
```

Les types composes fournissent un comportement similaire aux interfaces sans mot-cle `interface` separe,
en s'appuyant sur les paradigmes existants de `define` et de duck typing.

### Alias de type
```hemlock
// Alias de type simple
type Integer = i32;
type Text = string;

// Alias de type fonction
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Alias de type compose (excellent pour les interfaces reutilisables)
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Alias de type generique
type Pair<T> = { first: T, second: T };

// Utilisation des alias de type
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

Les alias de type creent des raccourcis nommes pour les types complexes, ameliorant la lisibilite et la maintenabilite.

### Types de fonction
```hemlock
// Annotations de type fonction pour les parametres
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Fonction d'ordre superieur retournant une fonction
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Types de fonction asynchrone
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// Types de fonction avec plusieurs parametres
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Parametres const
```hemlock
// Parametre const - immutabilite profonde
fn print_all(const items: array) {
    // items.push(4);  // ERREUR : impossible de modifier un parametre const
    for (item in items) {
        print(item);
    }
}

// Const avec objets - aucune mutation par aucun chemin
fn describe(const person: object) {
    print(person.name);       // OK : la lecture est autorisee
    // person.name = "Bob";   // ERREUR : impossible de modifier
}

// L'acces imbrique est autorise pour la lecture
fn get_city(const user: object) {
    return user.address.city;  // OK : lecture des proprietes imbriquees
}
```

Le modificateur `const` empeche toute mutation du parametre, y compris les proprietes imbriquees.
Cela fournit une securite a la compilation pour les fonctions qui ne doivent pas modifier leurs entrees.

### Parametres ref (passage par reference)
```hemlock
// Parametre ref - la variable de l'appelant est modifiee directement
fn increment(ref x: i32) {
    x = x + 1;  // Modifie la variable originale
}

let count = 10;
increment(count);
print(count);  // 11 - l'original a ete modifie

// Fonction swap classique
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// Melanger parametres ref et reguliers
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

Le modificateur `ref` passe une reference a la variable de l'appelant, permettant a la fonction de
la modifier directement. Sans `ref`, les primitives sont passees par valeur (copiees). Utilisez `ref` quand
vous devez modifier l'etat de l'appelant sans retourner de valeur.

**Regles :**
- Les parametres `ref` doivent recevoir des variables, pas des litteraux ou expressions
- Fonctionne avec tous les types (primitives, tableaux, objets)
- Combiner avec les annotations de type : `ref x: i32`
- Ne peut pas etre combine avec `const` (ils sont opposes)

### Signatures de methode dans define
```hemlock
// Define avec signatures de methode (patron interface)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Signature de methode requise
}

// Les objets doivent fournir la methode requise
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Methodes optionnelles avec ?
define Serializable {
    fn serialize(): string,        // Requise
    fn pretty?(): string           // Methode optionnelle
}

// Le type Self fait reference au type definissant
define Cloneable {
    fn clone(): Self   // Retourne le meme type que l'objet
}
```

Les signatures de methode dans les blocs `define` utilisent des delimiteurs virgule (comme les interfaces TypeScript),
etablissant des contrats que les objets doivent respecter et permettant des patrons de programmation
de type interface avec le systeme de duck typing de Hemlock.

### Gestion des erreurs
```hemlock
try { throw "erreur"; } catch (e) { print(e); } finally { cleanup(); }
panic("irrecuperable");  // quitte immediatement, non capturable
```

### Async/Concurrence
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // ou join(task)
detach(spawn(background_work));

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**Propriete de la memoire :** Les taches recoivent des copies des valeurs primitives mais partagent les pointeurs. Si vous passez un `ptr` a une tache lancee, vous devez vous assurer que la memoire reste valide jusqu'a ce que la tache se termine. Utilisez `join()` avant `free()`, ou utilisez des canaux pour signaler la completion.

### Entree utilisateur
```hemlock
let name = read_line();          // Lit une ligne depuis stdin (bloquant)
print("Bonjour, " + name);
eprint("Message d'erreur");      // Affiche sur stderr

// read_line() retourne null en fin de fichier (EOF)
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Recu:", line);
}
```

### E/S fichier
```hemlock
let f = open("fichier.txt", "r");  // modes: r, w, a, r+, w+, a+
let content = f.read();
f.write("donnees");
f.seek(0);
f.close();
```

### Signaux
```hemlock
signal(SIGINT, fn(sig) { print("Interrompu"); });
raise(SIGUSR1);
```

---

## Methodes de chaine (19)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `to_upper`, `to_lower`,
`starts_with`, `ends_with`, `replace`, `replace_all`, `repeat`, `char_at`,
`byte_at`, `chars`, `bytes`, `to_bytes`, `deserialize`

Chaines de modele : `` `Bonjour ${name}!` ``

**Mutabilite des chaines :** Les chaines sont mutables via l'affectation par index (`s[0] = 'H'`), mais toutes les methodes de chaine retournent de nouvelles chaines sans modifier l'originale. Cela permet la mutation sur place quand necessaire tout en gardant le chainage de methodes fonctionnel.

**Proprietes de longueur de chaine :**
```hemlock
let s = "hello 🚀";
print(s.length);       // 7 (nombre de caracteres/runes)
print(s.byte_length);  // 10 (nombre d'octets - l'emoji fait 4 octets UTF-8)
```

## Methodes de tableau (18)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`

Tableaux types : `let nums: array<i32> = [1, 2, 3];`

---

## Bibliotheque standard (40 modules)

Importer avec le prefixe `@stdlib/` :
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| Module | Description |
|--------|-------------|
| `arena` | Allocateur memoire arena (allocation par bump) |
| `args` | Analyse des arguments de ligne de commande |
| `assert` | Utilitaires d'assertion |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Operations d'E/S fichier asynchrones |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | Analyse et generation CSV |
| `datetime` | Classe DateTime, formatage, analyse |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `fmt` | Utilitaires de formatage de chaine |
| `fs` | read_file, write_file, list_dir, exists |
| `glob` | Correspondance de motifs de fichier |
| `hash` | sha256, sha512, md5, djb2 |
| `http` | http_get, http_post, http_request |
| `ipc` | Communication inter-processus |
| `iter` | Utilitaires d'iterateur |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger avec niveaux |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Manipulation de chemins de fichier |
| `process` | fork, exec, wait, kill |
| `random` | Generation de nombres aleatoires |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Logique de reessai avec backoff |
| `semver` | Versionnage semantique |
| `shell` | Utilitaires de commandes shell |
| `sqlite` | Base de donnees SQLite, query, exec, transactions |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | Couleurs et styles ANSI |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | Analyse et generation TOML |
| `url` | Analyse et manipulation d'URL |
| `uuid` | Generation d'UUID |
| `websocket` | Client WebSocket |

Voir `stdlib/docs/` pour la documentation detaillee des modules.

---

## FFI (Interface de fonction etrangere)

Declarer et appeler des fonctions C depuis des bibliotheques partagees :
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hello!");  // 6
let pid = getpid();
```

Exporter des fonctions FFI depuis des modules :
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

FFI dynamique (liaison a l'execution) :
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

Types : `FFI_INT`, `FFI_DOUBLE`, `FFI_POINTER`, `FFI_STRING`, `FFI_VOID`, etc.

---

## Operations atomiques

Programmation concurrente sans verrou avec des operations atomiques :

```hemlock
// Allouer de la memoire pour un i32 atomique
let p = alloc(4);
ptr_write_i32(p, 0);

// Chargement/stockage atomique
let val = atomic_load_i32(p);        // Lecture atomique
atomic_store_i32(p, 42);             // Ecriture atomique

// Operations fetch-and-modify (retournent l'ANCIENNE valeur)
let old = atomic_add_i32(p, 10);     // Ajoute, retourne l'ancienne valeur
old = atomic_sub_i32(p, 5);          // Soustrait, retourne l'ancienne valeur
old = atomic_and_i32(p, 0xFF);       // ET bit a bit
old = atomic_or_i32(p, 0x10);        // OU bit a bit
old = atomic_xor_i32(p, 0x0F);       // XOR bit a bit

// Compare-and-swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // Si *p == 42, mettre a 100
// Retourne true si l'echange a reussi, false sinon

// Echange atomique
old = atomic_exchange_i32(p, 999);   // Echange, retourne l'ancienne valeur

free(p);

// Variantes i64 disponibles (atomic_load_i64, atomic_add_i64, etc.)

// Barriere memoire (barriere complete)
atomic_fence();
```

Toutes les operations utilisent la coherence sequentielle (`memory_order_seq_cst`).

---

## Structure du projet

```
hemlock/
├── src/
│   ├── frontend/         # Partage : lexer, parser, AST, modules
│   ├── backends/
│   │   ├── interpreter/  # hemlock : interpreteur par parcours d'arbre
│   │   └── compiler/     # hemlockc : generateur de code C
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # Outils de bundle/package
├── runtime/              # Runtime du programme compile (libhemlock_runtime.a)
├── stdlib/               # Bibliotheque standard (40 modules)
│   └── docs/             # Documentation des modules
├── docs/                 # Documentation complete
│   ├── language-guide/   # Types, chaines, tableaux, etc.
│   ├── reference/        # References API
│   └── advanced/         # Async, FFI, signaux, etc.
├── tests/                # 625+ tests
└── examples/             # Programmes d'exemple
```

---

## Directives de style de code

### Constantes et nombres magiques

Lors de l'ajout de constantes numeriques a la base de code C, suivez ces directives :

1. **Definir les constantes dans `include/hemlock_limits.h`** - Ce fichier est l'emplacement central pour toutes les limites de compilation et d'execution, capacites et constantes nommees.

2. **Utiliser des noms descriptifs avec le prefixe `HML_`** - Toutes les constantes doivent etre prefixees avec `HML_` pour la clarte de l'espace de noms.

3. **Eviter les nombres magiques** - Remplacer les valeurs numeriques codees en dur par des constantes nommees. Exemples :
   - Limites de plage de type : `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Capacites de tampon : `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Conversions de temps : `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Graines de hachage : `HML_DJB2_HASH_SEED`
   - Valeurs ASCII : `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Inclure `hemlock_limits.h`** - Les fichiers sources doivent inclure cet en-tete (souvent via `internal.h`) pour acceder aux constantes.

5. **Documenter l'objectif** - Ajouter un commentaire expliquant ce que chaque constante represente.

---

## Ce qu'il ne faut PAS faire

- Ne pas ajouter de comportement implicite (ASI, GC, nettoyage automatique)
- Ne pas cacher la complexite (optimisations magiques, compteurs de references caches)
- Ne pas casser la semantique existante (points-virgules, memoire manuelle, chaines mutables)
- Ne pas perdre de precision dans les conversions implicites
- Ne pas utiliser de nombres magiques - definir des constantes nommees dans `hemlock_limits.h` a la place

---

## Tests

```bash
make test              # Executer les tests de l'interpreteur
make test-compiler     # Executer les tests du compilateur
make parity            # Executer les tests de parite (les deux doivent correspondre)
make test-all          # Executer toutes les suites de tests
```

**Important :** Les tests peuvent se bloquer a cause de problemes async/concurrence. Toujours utiliser un timeout lors de l'execution des tests :
```bash
timeout 60 make test   # timeout de 60 secondes
timeout 120 make parity
```

Categories de tests : primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Architecture compilateur/interpreteur

Hemlock a deux backends d'execution qui partagent un frontend commun :

```
Source (.hml)
    ↓
┌─────────────────────────────┐
│  FRONTEND PARTAGE           │
│  - Lexer (src/frontend/)    │
│  - Parser (src/frontend/)   │
│  - AST (src/frontend/)      │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ INTERPRETEUR│   │ COMPILATEUR│
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ Evaluation │    │ Verif type │
│ par arbre  │    │ AST → C    │
│            │    │ liaison gcc│
└────────────┘    └────────────┘
```

### Verification de type du compilateur

Le compilateur (`hemlockc`) inclut une verification de type a la compilation, **activee par defaut** :

```bash
hemlockc program.hml -o program    # Verifie les types, puis compile
hemlockc --check program.hml       # Verification de type seulement, pas de compilation
hemlockc --no-type-check prog.hml  # Desactiver la verification de type
hemlockc --strict-types prog.hml   # Avertir sur les types 'any' implicites
```

Le verificateur de type :
- Valide les annotations de type a la compilation
- Traite le code non type comme dynamique (type `any`) - toujours valide
- Fournit des indications d'optimisation pour le deballage (unboxing)
- Utilise des conversions numeriques permissives (plage validee a l'execution)

### Structure des repertoires

```
hemlock/
├── src/
│   ├── frontend/           # Partage : lexer, parser, AST, modules
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock : interpreteur par parcours d'arbre
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc : generateur de code C
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # Serveur de langage
│   │   └── bundler/        # Outils de bundle/package
├── runtime/                # libhemlock_runtime.a pour les programmes compiles
├── stdlib/                 # Bibliotheque standard partagee
└── tests/
    ├── parity/             # Tests qui DOIVENT passer les deux backends
    ├── interpreter/        # Tests specifiques a l'interpreteur
    └── compiler/           # Tests specifiques au compilateur
```

---

## Developpement parite-en-premier

**L'interpreteur et le compilateur doivent produire une sortie identique pour la meme entree.**

### Politique de developpement

Lors de l'ajout ou de la modification de fonctionnalites du langage :

1. **Concevoir** - Definir le changement AST/semantique dans le frontend partage
2. **Implementer l'interpreteur** - Ajouter l'evaluation par parcours d'arbre
3. **Implementer le compilateur** - Ajouter la generation de code C
4. **Ajouter un test de parite** - Ecrire le test dans `tests/parity/` avec un fichier `.expected`
5. **Verifier** - Executer `make parity` avant de fusionner

### Structure des tests de parite

```
tests/parity/
├── language/       # Fonctionnalites du langage de base (flux de controle, closures, etc.)
├── builtins/       # Fonctions integrees (print, typeof, memory, etc.)
├── methods/        # Methodes de chaine et de tableau
└── modules/        # Import/export, imports stdlib
```

Chaque test a deux fichiers :
- `feature.hml` - Le programme de test
- `feature.expected` - Sortie attendue (doit correspondre pour les deux backends)

### Resultats des tests de parite

| Statut | Signification |
|--------|---------------|
| `✓ PASSED` | L'interpreteur et le compilateur correspondent a la sortie attendue |
| `◐ INTERP_ONLY` | L'interpreteur fonctionne, le compilateur echoue (correction du compilateur necessaire) |
| `◑ COMPILER_ONLY` | Le compilateur fonctionne, l'interpreteur echoue (rare) |
| `✗ FAILED` | Les deux echouent (bug de test ou d'implementation) |

### Ce qui requiert la parite

- Toutes les constructions du langage (if, while, for, switch, defer, try/catch)
- Tous les operateurs (arithmetiques, bit a bit, logiques, comparaison)
- Toutes les fonctions integrees (print, typeof, alloc, etc.)
- Toutes les methodes de chaine et de tableau
- Regles de coercition et promotion de type
- Messages d'erreur pour les erreurs d'execution

### Ce qui peut differer

- Caracteristiques de performance
- Details de disposition memoire
- Format de debogage/trace de pile
- Erreurs de compilation (le compilateur peut en detecter plus a la compilation)

### Ajouter un test de parite

```bash
# 1. Creer le fichier de test
cat > tests/parity/language/my_feature.hml << 'EOF'
// Description du test
let x = some_feature();
print(x);
EOF

# 2. Generer la sortie attendue depuis l'interpreteur
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Verifier la parite
make parity
```

---

## Version

**v1.8.1** - Version actuelle avec :
- **Pattern matching** (expressions `match`) - Destructuration et flux de controle puissants :
  - Motifs litteral, joker et liaison de variable
  - Motifs OU (`1 | 2 | 3`)
  - Expressions de garde (`n if n > 0`)
  - Destructuration d'objet (`{ x, y }`)
  - Destructuration de tableau avec reste (`[first, ...rest]`)
  - Motifs de type (`n: i32`)
  - Parite complete entre interpreteur et compilateur
- **Annotations d'aide au compilateur** - 11 annotations d'optimisation pour le controle GCC/Clang :
  - `@inline`, `@noinline` - controle de l'inlining de fonction
  - `@hot`, `@cold` - indications de prediction de branche
  - `@pure`, `@const` - annotations d'effets de bord
  - `@flatten` - inliner tous les appels dans la fonction
  - `@optimize(level)` - niveau d'optimisation par fonction ("0", "1", "2", "3", "s", "fast")
  - `@warn_unused` - avertir sur les valeurs de retour ignorees
  - `@section(name)` - placement de section ELF personnalise (ex: `@section(".text.hot")`)
- **Fonctions a corps d'expression** (`fn double(x): i32 => x * 2;`) - syntaxe concise pour les fonctions a expression unique
- **Instructions sur une ligne** - syntaxe sans accolades pour `if`, `while`, `for` (ex: `if (x > 0) print(x);`)
- **Alias de type** (`type Name = Type;`) - raccourcis nommes pour les types complexes
- **Annotations de type fonction** (`fn(i32): i32`) - types de fonction de premiere classe
- **Parametres const** (`fn(const x: array)`) - immutabilite profonde pour les parametres
- **Parametres ref** (`fn(ref x: i32)`) - passage par reference pour la mutation directe de l'appelant
- **Signatures de methode dans define** (`fn method(): Type`) - contrats de type interface (delimites par virgule)
- **Type Self** dans les signatures de methode - fait reference au type definissant
- **Mot-cle loop** (`loop { }`) - boucles infinies plus propres, remplace `while (true)`
- **Etiquettes de boucle** (`outer: while`) - break/continue cibles pour les boucles imbriquees
- **Raccourci objet** (`{ name }`) - syntaxe de propriete raccourcie style ES6
- **Propagation d'objet** (`{ ...obj }`) - copier et fusionner les champs d'objet
- **Types duck composes** (`A & B & C`) - types d'intersection pour le typage structurel
- **Arguments nommes** pour les appels de fonction (`foo(name: "value", age: 30)`)
- **Operateurs de coalescence null** (`??`, `??=`, `?.`) pour la gestion securisee des null
- **Litteraux octaux** (`0o777`, `0O123`)
- **Separateurs numeriques** (`1_000_000`, `0xFF_FF`, `0b1111_0000`)
- **Commentaires bloc** (`/* ... */`)
- **Sequences d'echappement hexadecimales** dans les chaines/runes (`\x41` = 'A')
- **Sequences d'echappement Unicode** dans les chaines (`\u{1F600}` = 😀)
- **Litteraux flottants sans zero initial** (`.5`, `.123`, `.5e2`)
- **Verification de type a la compilation** dans hemlockc (activee par defaut)
- **Integration LSP** avec verification de type pour les diagnostics en temps reel
- **Operateurs d'affectation composee** (`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`)
- **Operateurs d'increment/decrement** (`++x`, `x++`, `--x`, `x--`)
- **Correction de precision de type** : i64/u64 + f32 -> f64 pour preserver la precision
- Systeme de type unifie avec indications d'optimisation de deballage
- Systeme de type complet (i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object, enum, file, task, channel)
- Chaines UTF-8 avec 19 methodes
- Tableaux avec 18 methodes incluant map/filter/reduce
- Gestion manuelle de la memoire avec `talloc()` et `sizeof()`
- Async/await avec vrai parallelisme pthread
- Operations atomiques pour la programmation concurrente sans verrou
- 40 modules stdlib (+ arena, assert, semver, toml, retry, iter, random, shell)
- FFI pour l'interoperabilite C avec `export extern fn` pour les wrappers de bibliotheque reutilisables
- Support des structures FFI dans le compilateur (passer des structures C par valeur)
- Helpers de pointeur FFI (`ptr_null`, `ptr_read_*`, `ptr_write_*`)
- defer, try/catch/finally/throw, panic
- E/S fichier, gestion des signaux, execution de commandes
- Gestionnaire de paquets [hpm](https://github.com/hemlang/hpm) avec registre base sur GitHub
- Backend compilateur (generation de code C) avec 100% de parite interpreteur
- Serveur LSP avec go-to-definition et find-references
- Passe d'optimisation AST et resolution de variable pour recherche O(1)
- Fonction integree apply() pour les appels de fonction dynamiques
- Canaux non bufferises et support de nombreux parametres
- 159 tests de parite (100% de taux de reussite)

---

## Philosophie

> Nous vous donnons les outils pour etre en securite (`buffer`, annotations de type, verification des limites) mais nous ne vous forcons pas a les utiliser (`ptr`, memoire manuelle, operations non securisees).

**Si vous n'etes pas sur qu'une fonctionnalite convient a Hemlock, demandez-vous : "Est-ce que cela donne au programmeur plus de controle explicite, ou est-ce que cela cache quelque chose ?"**

Si cela cache, cela n'a probablement pas sa place dans Hemlock.
