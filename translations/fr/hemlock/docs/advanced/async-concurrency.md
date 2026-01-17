# Async/Concurrence dans Hemlock

Hemlock fournit une **concurrence structuree** avec une syntaxe async/await, le lancement de taches et des canaux pour la communication. L'implementation utilise les threads POSIX (pthreads) pour un **VERITABLE parallelisme multi-thread**.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Modele de threading](#modele-de-threading)
- [Fonctions asynchrones](#fonctions-asynchrones)
- [Lancement de taches](#lancement-de-taches)
- [Canaux](#canaux)
- [Propagation des exceptions](#propagation-des-exceptions)
- [Details d'implementation](#details-dimplementation)
- [Bonnes pratiques](#bonnes-pratiques)
- [Caracteristiques de performance](#caracteristiques-de-performance)
- [Limitations actuelles](#limitations-actuelles)

## Vue d'ensemble

**Ce que cela signifie :**
- ✅ **Vrais threads OS** - Chaque tache lancee s'execute sur un pthread separe (thread POSIX)
- ✅ **Vrai parallelisme** - Les taches s'executent simultanement sur plusieurs coeurs CPU
- ✅ **Ordonnance par le noyau** - L'ordonnanceur du systeme d'exploitation distribue les taches sur les coeurs disponibles
- ✅ **Canaux thread-safe** - Utilise des mutex pthread et des variables de condition pour la synchronisation

**Ce que ce n'est PAS :**
- ❌ **PAS des green threads** - Pas de multitache cooperatif en espace utilisateur
- ❌ **PAS des coroutines async/await** - Pas de boucle d'evenements mono-thread comme JavaScript/Python asyncio
- ❌ **PAS une concurrence emulee** - Pas de parallelisme simule

C'est le **meme modele de threading que C, C++ et Rust** lors de l'utilisation des threads OS. Vous obtenez une execution parallele reelle sur plusieurs coeurs.

## Modele de threading

### Threading 1:1

Hemlock utilise un **modele de threading 1:1**, ou :
- Chaque tache lancee cree un thread OS dedie via `pthread_create()`
- Le noyau du systeme d'exploitation ordonnance les threads sur les coeurs CPU disponibles
- Multitache preemptif - le systeme peut interrompre et basculer entre les threads
- **Pas de GIL** - Contrairement a Python, il n'y a pas de Global Interpreter Lock limitant le parallelisme

### Mecanismes de synchronisation

- **Mutex** - Les canaux utilisent `pthread_mutex_t` pour un acces thread-safe
- **Variables de condition** - Les send/recv bloquants utilisent `pthread_cond_t` pour une attente efficace
- **Operations sans verrou** - Les transitions d'etat des taches sont atomiques

## Fonctions asynchrones

Les fonctions peuvent etre declarees comme `async` pour indiquer qu'elles sont concues pour une execution concurrente :

```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
```

### Points cles

- `async fn` declare une fonction asynchrone
- Les fonctions async peuvent etre lancees comme taches concurrentes en utilisant `spawn()`
- Les fonctions async peuvent aussi etre appelees directement (s'execute de maniere synchrone dans le thread courant)
- Une fois lancee, chaque tache s'execute sur **son propre thread OS** (pas une coroutine !)
- Le mot-cle `await` est reserve pour une utilisation future

### Exemple : Appel direct vs Spawn

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Appel direct - s'execute de maniere synchrone
let result1 = factorial(5);  // 120

// Tache lancee - s'execute sur un thread separe
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## Lancement de taches

Utilisez `spawn()` pour executer des fonctions async **en parallele sur des threads OS separes** :

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Lancer plusieurs taches - elles s'executent en PARALLELE sur differents coeurs CPU !
let t1 = spawn(factorial, 5);  // Thread 1
let t2 = spawn(factorial, 6);  // Thread 2
let t3 = spawn(factorial, 7);  // Thread 3

// Toutes les trois calculent simultanement en ce moment !

// Attendre les resultats
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### Fonctions integrees

#### spawn(async_fn, arg1, arg2, ...)

Cree une nouvelle tache sur un nouveau pthread, retourne un handle de tache.

**Parametres :**
- `async_fn` - La fonction async a executer
- `arg1, arg2, ...` - Arguments a passer a la fonction

**Retourne :** Handle de tache (valeur opaque utilisee avec `join()` ou `detach()`)

**Exemple :**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... logique de traitement
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

Attend la completion de la tache (bloque jusqu'a ce que le thread se termine), retourne le resultat.

**Parametres :**
- `task` - Handle de tache retourne par `spawn()`

**Retourne :** La valeur retournee par la fonction async

**Exemple :**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // Bloque jusqu'a ce que compute() se termine
print(result);
```

**Important :** Chaque tache ne peut etre jointe qu'une seule fois. Les joins subsequents provoqueront une erreur.

#### detach(task)

Execution fire-and-forget (le thread s'execute independamment, join non autorise).

**Parametres :**
- `task` - Handle de tache retourne par `spawn()`

**Retourne :** `null`

**Exemple :**
```hemlock
async fn background_work() {
    // Tache de fond de longue duree
    // ...
}

let task = spawn(background_work);
detach(task);  // La tache s'execute independamment, impossible de joindre
```

**Important :** Les taches detachees ne peuvent pas etre jointes. Le pthread et la structure Task sont automatiquement nettoyes quand la tache se termine.

## Canaux

Les canaux fournissent une communication thread-safe entre les taches en utilisant un tampon borne avec une semantique bloquante.

### Creation de canaux

```hemlock
let ch = channel(10);  // Creer un canal avec une taille de tampon de 10
```

**Parametres :**
- `capacity` (i32) - Nombre maximum de valeurs que le canal peut contenir

**Retourne :** Objet canal

### Methodes de canal

#### send(value)

Envoyer une valeur au canal (bloque si plein).

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let task = spawn(producer, ch, 5);
```

**Comportement :**
- Si le canal a de l'espace, la valeur est ajoutee immediatement
- Si le canal est plein, l'expediteur bloque jusqu'a ce que de l'espace devienne disponible
- Si le canal est ferme, lance une exception

#### recv()

Recevoir une valeur du canal (bloque si vide).

```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let task = spawn(consumer, ch, 5);
```

**Comportement :**
- Si le canal a des valeurs, retourne la prochaine valeur immediatement
- Si le canal est vide, le recepteur bloque jusqu'a ce qu'une valeur soit disponible
- Si le canal est ferme et vide, retourne `null`

#### close()

Fermer le canal (recv sur un canal ferme retourne null).

```hemlock
ch.close();
```

**Comportement :**
- Empeche les operations `send()` ulterieures (lancera une exception)
- Permet aux operations `recv()` en attente de se terminer
- Une fois vide, `recv()` retourne `null`

### Multiplexage avec select()

La fonction `select()` permet d'attendre sur plusieurs canaux simultanement, retournant quand n'importe quel canal a des donnees disponibles.

**Signature :**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parametres :**
- `channels` - Tableau de valeurs de canaux
- `timeout_ms` (optionnel) - Delai d'attente en millisecondes (-1 ou omettre pour attente infinie)

**Retourne :**
- `{ channel, value }` - Objet avec le canal qui avait des donnees et la valeur recue
- `null` - En cas de timeout (si un timeout etait specifie)

**Exemple :**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Taches productrices
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// Attendre le premier resultat (ch2 devrait etre plus rapide)
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"

// Attendre le deuxieme resultat
let result2 = select([ch1, ch2]);
print(result2.value);  // "from channel 1"
```

**Avec timeout :**
```hemlock
let ch = channel(1);

// Pas d'expediteur, va expirer
let result = select([ch], 100);  // timeout de 100ms
if (result == null) {
    print("Delai depasse !");
}
```

**Cas d'utilisation :**
- Attendre le plus rapide parmi plusieurs sources de donnees
- Implementer des timeouts sur les operations de canal
- Patterns de boucle d'evenements avec plusieurs sources d'evenements
- Fan-in : fusionner plusieurs canaux en un seul

**Pattern fan-in :**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // Tous les canaux fermes
        }
        output.send(result.value);
    }
    output.close();
}
```

### Exemple complet producteur-consommateur

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Creer un canal avec une taille de tampon
let ch = channel(10);

// Lancer le producteur et le consommateur
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Attendre la completion
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### Multi-producteur, multi-consommateur

Les canaux peuvent etre partages en toute securite entre plusieurs producteurs et consommateurs :

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// Plusieurs producteurs
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// Plusieurs consommateurs
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// Attendre tous
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## Propagation des exceptions

Les exceptions lancees dans les taches spawn sont propagees lors du join :

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "La tache a echoue !";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Intercepte : " + e);  // "Intercepte : La tache a echoue !"
}
```

### Patterns de gestion des exceptions

**Pattern 1 : Gerer dans la tache**
```hemlock
async fn safe_task() {
    try {
        // operation risquee
    } catch (e) {
        print("Erreur dans la tache : " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // Pas d'exception propagee
```

**Pattern 2 : Propager a l'appelant**
```hemlock
async fn task_that_throws() {
    throw "erreur";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("Intercepte depuis la tache : " + e);
}
```

**Pattern 3 : Taches detachees avec exceptions**
```hemlock
async fn detached_task() {
    try {
        // travail
    } catch (e) {
        // Doit gerer en interne - ne peut pas propager
        print("Erreur : " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // Impossible d'intercepter les exceptions des taches detachees
```

## Details d'implementation

### Architecture de threading

- **Threading 1:1** - Chaque tache lancee cree un thread OS dedie via `pthread_create()`
- **Ordonnance par le noyau** - Le noyau du systeme ordonnance les threads sur les coeurs CPU disponibles
- **Multitache preemptif** - Le systeme peut interrompre et basculer entre les threads
- **Pas de GIL** - Contrairement a Python, il n'y a pas de Global Interpreter Lock limitant le parallelisme

### Implementation des canaux

Les canaux utilisent un tampon circulaire avec synchronisation pthread :

```
Structure du canal :
- buffer[] - Tableau de taille fixe de Values
- capacity - Nombre maximum d'elements
- size - Nombre actuel d'elements
- head - Position de lecture
- tail - Position d'ecriture
- mutex - pthread_mutex_t pour un acces thread-safe
- not_empty - pthread_cond_t pour recv bloquant
- not_full - pthread_cond_t pour send bloquant
- closed - Drapeau booleen
- refcount - Compteur de references pour le nettoyage
```

**Comportement bloquant :**
- `send()` sur canal plein : attend sur la variable de condition `not_full`
- `recv()` sur canal vide : attend sur la variable de condition `not_empty`
- Les deux sont signales de maniere appropriee par l'operation opposee

### Memoire et nettoyage

- **Taches jointes :** Automatiquement nettoyees apres que `join()` retourne
- **Taches detachees :** Automatiquement nettoyees quand la tache se termine
- **Canaux :** Comptes par reference et liberes quand plus utilises

## Bonnes pratiques

### 1. Toujours fermer les canaux

```hemlock
async fn producer(ch) {
    // ... envoyer des valeurs
    ch.close();  // Important : signaler qu'il n'y a plus de valeurs
}
```

### 2. Utiliser la concurrence structuree

Lancer des taches et les joindre dans la meme portee :

```hemlock
fn process_data(data) {
    // Lancer des taches
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // Toujours joindre avant de retourner
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. Gerer les exceptions de maniere appropriee

```hemlock
async fn task() {
    try {
        // operation risquee
    } catch (e) {
        // Logger l'erreur
        throw e;  // Relancer si l'appelant doit savoir
    }
}
```

### 4. Utiliser une capacite de canal appropriee

- **Petite capacite (1-10) :** Pour la coordination/signalisation
- **Capacite moyenne (10-100) :** Pour le producteur-consommateur general
- **Grande capacite (100+) :** Pour les scenarios a haut debit

```hemlock
let signal_ch = channel(1);      // Coordination
let work_ch = channel(50);       // File de travail
let buffer_ch = channel(1000);   // Haut debit
```

### 5. Detacher uniquement si necessaire

Preferez `join()` a `detach()` pour une meilleure gestion des ressources :

```hemlock
// Bien : Joindre et obtenir le resultat
let task = spawn(work);
let result = join(task);

// Utiliser detach uniquement pour le vrai fire-and-forget
let bg_task = spawn(background_logging);
detach(bg_task);  // S'executera independamment
```

## Caracteristiques de performance

### Vrai parallelisme

- **N taches lancees peuvent utiliser N coeurs CPU simultanement**
- Acceleration prouvee - les tests de stress montrent 8-9x le temps CPU vs le temps reel (plusieurs coeurs travaillant)
- Mise a l'echelle lineaire avec le nombre de coeurs (jusqu'au nombre de threads)

### Surcharge des threads

- Chaque tache a ~8Ko de pile + surcharge pthread
- Cout de creation de thread : ~10-20us
- Cout de changement de contexte : ~1-5us

### Quand utiliser Async

**Bons cas d'utilisation :**
- Calculs intensifs en CPU qui peuvent etre parallelises
- Operations liees aux E/S (bien que les E/S soient toujours bloquantes)
- Traitement concurrent de donnees independantes
- Architectures en pipeline avec canaux

**Pas ideal pour :**
- Taches tres courtes (la surcharge des threads domine)
- Taches avec beaucoup de synchronisation (surcharge de contention)
- Systemes mono-coeur (pas de benefice de parallelisme)

### E/S bloquantes securisees

Les operations bloquantes dans une tache ne bloquent pas les autres :

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // Bloque ce thread uniquement
    let content = f.read();       // Bloque ce thread uniquement
    f.close();
    return content;
}

// Les deux lisent de maniere concurrente (sur differents threads)
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## Modele de securite des threads

Hemlock utilise un modele de concurrence par **passage de messages** ou les taches communiquent via des canaux plutot que par un etat mutable partage.

### Isolation des arguments

Quand vous lancez une tache, **les arguments sont copies en profondeur** pour prevenir les courses de donnees :

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // Modifie la COPIE, pas l'original
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - inchange !
print(modified.length);  // 4 - a le nouvel element
```

**Ce qui est copie en profondeur :**
- Tableaux (et tous les elements recursivement)
- Objets (et tous les champs recursivement)
- Chaines de caracteres
- Tampons (buffers)

**Ce qui est partage (reference retenue) :**
- Canaux (le mecanisme de communication - intentionnellement partage)
- Handles de taches (pour la coordination)
- Fonctions (le code est immuable)
- Handles de fichiers (le systeme gere l'acces concurrent)
- Handles de sockets (le systeme gere l'acces concurrent)

**Ce qui ne peut pas etre passe :**
- Pointeurs bruts (`ptr`) - utilisez `buffer` a la place

### Pourquoi le passage de messages ?

Cela suit la philosophie "explicite plutot qu'implicite" de Hemlock :

```hemlock
// MAUVAIS : Etat mutable partage (causerait des courses de donnees)
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // Course !
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // Course !

// BON : Passage de messages via canaux
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - pas de condition de course
```

### Securite du comptage de references

Toutes les operations de comptage de references utilisent des **operations atomiques** pour prevenir les bugs use-after-free :
- `string_retain/release` - atomique
- `array_retain/release` - atomique
- `object_retain/release` - atomique
- `buffer_retain/release` - atomique
- `function_retain/release` - atomique
- `channel_retain/release` - atomique
- `task_retain/release` - atomique

Cela assure une gestion memoire securisee meme quand les valeurs sont partagees entre threads.

### Acces a l'environnement de closure

Les taches ont acces a l'environnement de closure pour :
- Les fonctions integrees (`print`, `len`, etc.)
- Les definitions de fonctions globales
- Les constantes et variables

L'environnement de closure est protege par un mutex par environnement, rendant
les lectures et ecritures concurrentes thread-safe :

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK : lecture de variable de closure (thread-safe)
}

async fn modify_closure() {
    x = 20;  // OK : ecriture de variable de closure (synchronise avec mutex)
}
```

**Note :** Bien que l'acces concurrent soit synchronise, modifier un etat partage depuis
plusieurs taches peut toujours mener a des conditions de course logiques (ordonnancement
non deterministe). Pour un comportement previsible, utilisez des canaux pour la communication
entre taches ou des valeurs de retour des taches.

Si vous devez retourner des donnees d'une tache, utilisez la valeur de retour ou les canaux.

## Limitations actuelles

### 1. Pas d'ordonnanceur avec vol de travail

Utilise 1 thread par tache, ce qui peut etre inefficace pour beaucoup de taches courtes.

**Actuel :** 1000 taches = 1000 threads (surcharge importante)

**Prevu :** Pool de threads avec vol de travail pour une meilleure efficacite

### 3. Pas d'integration d'E/S asynchrones

Les operations fichier/reseau bloquent toujours le thread :

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // Bloque le thread
    f.close();
    return content;
}
```

**Solution de contournement :** Utilisez plusieurs threads pour les operations d'E/S concurrentes

### 4. Capacite de canal fixe

La capacite du canal est definie a la creation et ne peut pas etre redimensionnee :

```hemlock
let ch = channel(10);
// Impossible de redimensionner dynamiquement a 20
```

### 5. La taille du canal est fixe

La taille du tampon du canal ne peut pas etre changee apres creation.

## Patterns courants

### Map parallele

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // Lancer les workers
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // Envoyer les donnees
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // Collecter les resultats
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // Attendre les workers
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### Architecture en pipeline

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// Creer le pipeline
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// Alimenter l'entree
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// Collecter la sortie
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### Fan-Out, Fan-In

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // Traiter la valeur
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// Fan-out : Plusieurs workers
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// Envoyer le travail
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// Fan-in : Collecter tous les resultats
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// Attendre tous les workers
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## Resume

Le modele async/concurrence de Hemlock fournit :

- ✅ Vrai parallelisme multi-thread utilisant les threads OS
- ✅ Primitives de concurrence structuree simples
- ✅ Canaux thread-safe pour la communication
- ✅ Propagation des exceptions entre taches
- ✅ Performance prouvee sur les systemes multi-coeur
- ✅ **Isolation des arguments** - la copie profonde previent les courses de donnees
- ✅ **Comptage de references atomique** - gestion memoire securisee entre threads

Cela rend Hemlock adapte pour :
- Les calculs paralleles
- Les operations d'E/S concurrentes
- Les architectures en pipeline
- Les patterns producteur-consommateur

Tout en evitant la complexite de :
- La gestion manuelle des threads
- Les primitives de synchronisation bas niveau
- Les conceptions basees sur les verrous sujettes aux deadlocks
- Les bugs d'etat mutable partage
