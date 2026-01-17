# Référence de l'API Concurrency

Référence complète pour le système async/concurrence de Hemlock.

---

## Aperçu

Hemlock fournit une **concurrence structurée** avec un véritable parallélisme multi-threadé utilisant les threads POSIX (pthreads). Chaque tâche lancée s'exécute sur un thread OS séparé, permettant une exécution véritablement parallèle sur plusieurs cœurs CPU.

**Caractéristiques principales :**
- Véritable parallélisme multi-threadé (pas de green threads)
- Syntaxe de fonction async
- Lancement et jointure de tâches
- Canaux thread-safe
- Propagation des exceptions

**Modèle de threading :**
- ✅ Vrais threads OS (POSIX pthreads)
- ✅ Véritable parallélisme (plusieurs cœurs CPU)
- ✅ Ordonnancé par le noyau (multitâche préemptif)
- ✅ Synchronisation thread-safe (mutex, variables de condition)

---

## Fonctions async

### Déclaration de fonction async

Les fonctions peuvent être déclarées comme `async` pour indiquer qu'elles sont conçues pour l'exécution concurrente.

**Syntaxe :**
```hemlock
async fn nom_fonction(params): type_retour {
    // corps de la fonction
}
```

**Exemples :**
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

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Traitement:", data);
    return null;
}
```

**Comportement :**
- `async fn` déclare une fonction asynchrone
- Peut être appelée de manière synchrone (s'exécute dans le thread courant)
- Peut être lancée comme tâche concurrente (s'exécute sur un nouveau thread)
- Quand lancée, s'exécute sur son propre thread OS

**Note :** Le mot-clé `await` est réservé pour une utilisation future mais n'est pas actuellement implémenté.

---

## Gestion des tâches

### spawn

Crée et démarre une nouvelle tâche concurrente.

**Signature :**
```hemlock
spawn(async_fn: function, ...args): task
```

**Paramètres :**
- `async_fn` - Fonction async à exécuter
- `...args` - Arguments à passer à la fonction

**Retourne :** Handle de tâche

**Exemples :**
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

// Lancer une seule tâche
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// Lancer plusieurs tâches (s'exécutent en parallèle !)
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// Les trois s'exécutent simultanément
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**Comportement :**
- Crée un nouveau thread OS via `pthread_create()`
- Commence l'exécution de la fonction immédiatement
- Retourne un handle de tâche pour une jointure ultérieure
- Les tâches s'exécutent en parallèle sur des cœurs CPU séparés

---

### join

Attend la fin de la tâche et récupère le résultat.

**Signature :**
```hemlock
join(task: task): any
```

**Paramètres :**
- `task` - Handle de tâche de `spawn()`

**Retourne :** Valeur de retour de la tâche

**Exemples :**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // Bloque jusqu'à ce que la tâche se termine
print(result);         // 3628800
```

**Comportement :**
- Bloque le thread courant jusqu'à ce que la tâche se termine
- Retourne la valeur de retour de la tâche
- Propage les exceptions levées par la tâche
- Nettoie les ressources de la tâche après le retour

**Gestion des erreurs :**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "La tâche a échoué !";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Intercepté:", e);  // "Intercepté: La tâche a échoué !"
}
```

---

### detach

Détache la tâche (exécution fire-and-forget).

**Signature :**
```hemlock
detach(task: task): null
```

**Paramètres :**
- `task` - Handle de tâche de `spawn()`

**Retourne :** `null`

**Exemples :**
```hemlock
async fn background_work() {
    print("Travail en arrière-plan...");
    return null;
}

let t = spawn(background_work);
detach(t);  // La tâche continue de s'exécuter indépendamment

// Impossible de joindre une tâche détachée
// join(t);  // ERREUR
```

**Comportement :**
- La tâche continue de s'exécuter indépendamment
- Impossible de faire `join()` sur une tâche détachée
- La tâche et le thread sont automatiquement nettoyés quand la tâche se termine

**Cas d'utilisation :**
- Tâches en arrière-plan fire-and-forget
- Tâches de journalisation/surveillance
- Tâches qui n'ont pas besoin de retourner de valeurs

---

## Canaux

Les canaux fournissent une communication thread-safe entre les tâches.

### channel

Crée un canal avec buffer.

**Signature :**
```hemlock
channel(capacity: i32): channel
```

**Paramètres :**
- `capacity` - Taille du buffer (nombre de valeurs)

**Retourne :** Objet channel

**Exemples :**
```hemlock
let ch = channel(10);  // Canal avec buffer de capacité 10
let ch2 = channel(1);  // Buffer minimal (synchrone)
let ch3 = channel(100); // Grand buffer
```

**Comportement :**
- Crée un canal thread-safe
- Utilise des mutex pthread pour la synchronisation
- La capacité est fixée à la création

---

### Méthodes des canaux

#### send

Envoie une valeur au canal (bloque si plein).

**Signature :**
```hemlock
channel.send(value: any): null
```

**Paramètres :**
- `value` - Valeur à envoyer (n'importe quel type)

**Retourne :** `null`

**Exemples :**
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
let t = spawn(producer, ch, 5);
```

**Comportement :**
- Envoie la valeur au canal
- Bloque si le canal est plein
- Thread-safe (utilise un mutex)
- Retourne après que la valeur est envoyée

---

#### recv

Reçoit une valeur du canal (bloque si vide).

**Signature :**
```hemlock
channel.recv(): any
```

**Retourne :** Valeur du canal, ou `null` si le canal est fermé et vide

**Exemples :**
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
let t = spawn(consumer, ch, 5);
```

**Comportement :**
- Reçoit une valeur du canal
- Bloque si le canal est vide
- Retourne `null` si le canal est fermé et vide
- Thread-safe (utilise un mutex)

---

#### close

Ferme le canal (plus d'envois autorisés).

**Signature :**
```hemlock
channel.close(): null
```

**Retourne :** `null`

**Exemples :**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // Signale qu'il n'y a plus de valeurs
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // Canal fermé
        }
        print(val);
    }
    return null;
}
```

**Comportement :**
- Ferme le canal
- Plus d'envois autorisés
- `recv()` retourne `null` quand le canal est vide
- Thread-safe

---

## Exemple complet de concurrence

### Modèle producteur-consommateur

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Production:", i);
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
        print("Consommation:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Créer le canal
let ch = channel(10);

// Lancer producteur et consommateur
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Attendre la fin
join(p);
let total = join(c);
print("Total:", total);  // 0+10+20+30+40 = 100
```

---

## Calcul parallèle

### Exemple de tâches multiples

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Lancer plusieurs tâches (s'exécutent en parallèle !)
let t1 = spawn(factorial, 5);   // Thread 1
let t2 = spawn(factorial, 6);   // Thread 2
let t3 = spawn(factorial, 7);   // Thread 3
let t4 = spawn(factorial, 8);   // Thread 4

// Les quatre calculent simultanément !

// Attendre les résultats
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## Cycle de vie des tâches

### Transitions d'état

1. **Créée** - Tâche lancée mais pas encore en exécution
2. **En cours** - Tâche en exécution sur un thread OS
3. **Terminée** - Tâche terminée (résultat disponible)
4. **Jointe** - Résultat récupéré, ressources nettoyées
5. **Détachée** - Tâche continue indépendamment

### Exemple de cycle de vie

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. Créer la tâche
let t = spawn(work, 21);  // État: En cours

// La tâche s'exécute sur un thread séparé...

// 2. Joindre la tâche
let result = join(t);     // État: Terminée → Jointe
print(result);            // 42

// Ressources de la tâche nettoyées après join
```

### Cycle de vie détaché

```hemlock
async fn background() {
    print("Tâche en arrière-plan en cours");
    return null;
}

// 1. Créer la tâche
let t = spawn(background);  // État: En cours

// 2. Détacher la tâche
detach(t);                  // État: Détachée

// La tâche continue de s'exécuter indépendamment
// Ressources nettoyées par l'OS quand terminée
```

---

## Gestion des erreurs

### Propagation des exceptions

Les exceptions levées dans les tâches sont propagées lors de la jointure :

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "La tâche a échoué !";
    }
    return 42;
}

// Tâche qui réussit
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// Tâche qui échoue
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Intercepté:", e);  // "Intercepté: La tâche a échoué !"
}
```

### Gestion de plusieurs tâches

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tâche " + typeof(id) + " a échoué";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // Va échouer
let t3 = spawn(work, 3, 0);

// Joindre avec gestion des erreurs
try {
    let r1 = join(t1);  // OK
    print("Tâche 1:", r1);

    let r2 = join(t2);  // Lève une exception
    print("Tâche 2:", r2);  // Jamais atteint
} catch (e) {
    print("Erreur:", e);  // "Erreur: Tâche 2 a échoué"
}

// Peut toujours joindre la tâche restante
let r3 = join(t3);
print("Tâche 3:", r3);
```

---

## Caractéristiques de performance

### Véritable parallélisme

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Exécution séquentielle
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// Exécution parallèle
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// parallel_time devrait être ~50% de sequential_time sur les systèmes multi-cœurs
```

**Caractéristiques prouvées :**
- N tâches peuvent utiliser N cœurs CPU simultanément
- Les tests de stress montrent 8-9x le temps CPU vs temps réel (preuve de parallélisme)
- Surcharge de thread : ~8 Ko de pile + surcharge pthread par tâche
- Les opérations bloquantes dans une tâche ne bloquent pas les autres

---

## Détails d'implémentation

### Modèle de threading

- **Threading 1:1** - Chaque tâche = 1 thread OS (`pthread`)
- **Ordonnancé par le noyau** - Le noyau OS distribue les threads sur les cœurs
- **Multitâche préemptif** - L'OS peut interrompre et changer de thread
- **Pas de GIL** - Pas de Global Interpreter Lock (contrairement à Python)

### Synchronisation

- **Mutex** - Les canaux utilisent `pthread_mutex_t`
- **Variables de condition** - send/recv bloquants utilisent `pthread_cond_t`
- **Opérations lock-free** - Les transitions d'état des tâches sont atomiques

### Mémoire et nettoyage

- **Tâches jointes** - Automatiquement nettoyées après `join()`
- **Tâches détachées** - Automatiquement nettoyées quand la tâche se termine
- **Canaux** - Comptés par références, libérés quand plus utilisés

---

## Limitations

- Pas de `select()` pour le multiplexage de plusieurs canaux
- Pas d'ordonnanceur work-stealing (1 thread par tâche)
- Pas d'intégration d'E/S async (les opérations fichier/réseau bloquent)
- Capacité du canal fixée à la création

---

## Résumé complet de l'API

### Fonctions

| Fonction  | Signature                         | Retourne  | Description                          |
|-----------|-----------------------------------|-----------|--------------------------------------|
| `spawn`   | `(async_fn: function, ...args)`   | `task`    | Créer et démarrer une tâche concurrente |
| `join`    | `(task: task)`                    | `any`     | Attendre la tâche, obtenir le résultat |
| `detach`  | `(task: task)`                    | `null`    | Détacher la tâche (fire-and-forget)  |
| `channel` | `(capacity: i32)`                 | `channel` | Créer un canal thread-safe           |

### Méthodes des canaux

| Méthode | Signature       | Retourne | Description                           |
|---------|-----------------|----------|---------------------------------------|
| `send`  | `(value: any)`  | `null`   | Envoyer valeur (bloque si plein)      |
| `recv`  | `()`            | `any`    | Recevoir valeur (bloque si vide)      |
| `close` | `()`            | `null`   | Fermer le canal                       |

### Types

| Type      | Description                          |
|-----------|--------------------------------------|
| `task`    | Handle pour tâche concurrente        |
| `channel` | Canal de communication thread-safe   |

---

## Bonnes pratiques

### À faire

✅ Utiliser les canaux pour la communication entre tâches
✅ Gérer les exceptions des tâches jointes
✅ Fermer les canaux quand l'envoi est terminé
✅ Utiliser `join()` pour obtenir les résultats et nettoyer
✅ Ne lancer que des fonctions async

### À éviter

❌ Ne pas partager d'état mutable sans synchronisation
❌ Ne pas joindre la même tâche deux fois
❌ Ne pas envoyer sur des canaux fermés
❌ Ne pas lancer de fonctions non-async
❌ Ne pas oublier de joindre les tâches (sauf si détachées)

---

## Voir aussi

- [Fonctions intégrées](builtins.md) - `spawn()`, `join()`, `detach()`, `channel()`
- [Système de types](type-system.md) - Types task et channel
