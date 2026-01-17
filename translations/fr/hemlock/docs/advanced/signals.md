# Gestion des signaux dans Hemlock

Hemlock fournit une **gestion des signaux POSIX** pour gerer les signaux systeme comme SIGINT (Ctrl+C), SIGTERM et les signaux personnalises. Cela permet le controle de processus bas niveau et la communication inter-processus.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [API des signaux](#api-des-signaux)
- [Constantes de signaux](#constantes-de-signaux)
- [Gestion basique des signaux](#gestion-basique-des-signaux)
- [Patterns avances](#patterns-avances)
- [Comportement des gestionnaires de signaux](#comportement-des-gestionnaires-de-signaux)
- [Considerations de securite](#considerations-de-securite)
- [Cas d'utilisation courants](#cas-dutilisation-courants)
- [Exemples complets](#exemples-complets)

## Vue d'ensemble

La gestion des signaux permet aux programmes de :
- Repondre aux interruptions utilisateur (Ctrl+C, Ctrl+Z)
- Implementer un arret gracieux
- Gerer les demandes de terminaison
- Utiliser des signaux personnalises pour la communication inter-processus
- Creer des mecanismes d'alarme/minuterie

**Important :** La gestion des signaux est **inheremment non securisee** dans la philosophie de Hemlock. Les gestionnaires peuvent etre appeles a tout moment, interrompant l'execution normale. L'utilisateur est responsable de la synchronisation appropriee.

## API des signaux

### signal(signum, handler_fn)

Enregistrer une fonction de gestion de signal.

**Parametres :**
- `signum` (i32) - Numero de signal (constante comme SIGINT, SIGTERM)
- `handler_fn` (fonction ou null) - Fonction a appeler quand le signal est recu, ou `null` pour reinitialiser au comportement par defaut

**Retourne :** La fonction de gestion precedente (ou `null` si aucune)

**Exemple :**
```hemlock
fn my_handler(sig) {
    print("Signal intercepte : " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**Reinitialisation au defaut :**
```hemlock
signal(SIGINT, null);  // Reinitialiser SIGINT au comportement par defaut
```

### raise(signum)

Envoyer un signal au processus courant.

**Parametres :**
- `signum` (i32) - Numero de signal a envoyer

**Retourne :** `null`

**Exemple :**
```hemlock
raise(SIGUSR1);  // Declencher le gestionnaire SIGUSR1
```

## Constantes de signaux

Hemlock fournit les constantes de signaux POSIX standard sous forme de valeurs i32.

### Interruption et terminaison

| Constante | Valeur | Description | Declencheur courant |
|-----------|--------|-------------|---------------------|
| `SIGINT` | 2 | Interruption depuis le clavier | Ctrl+C |
| `SIGTERM` | 15 | Demande de terminaison | Commande `kill` |
| `SIGQUIT` | 3 | Quitter depuis le clavier | Ctrl+\ |
| `SIGHUP` | 1 | Deconnexion detectee | Terminal ferme |
| `SIGABRT` | 6 | Signal d'abandon | Fonction `abort()` |

**Exemples :**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // Commande kill
signal(SIGHUP, handle_hangup);      // Terminal ferme
```

### Signaux definis par l'utilisateur

| Constante | Valeur | Description | Cas d'utilisation |
|-----------|--------|-------------|-------------------|
| `SIGUSR1` | 10 | Signal utilisateur 1 | IPC personnalise |
| `SIGUSR2` | 12 | Signal utilisateur 2 | IPC personnalise |

**Exemples :**
```hemlock
// Utiliser pour communication personnalisee
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### Controle de processus

| Constante | Valeur | Description | Notes |
|-----------|--------|-------------|-------|
| `SIGALRM` | 14 | Minuterie d'alarme | Apres `alarm()` |
| `SIGCHLD` | 17 | Changement d'etat du processus enfant | Gestion de processus |
| `SIGCONT` | 18 | Continuer si arrete | Reprendre apres SIGSTOP |
| `SIGSTOP` | 19 | Arreter le processus | **Ne peut pas etre intercepte** |
| `SIGTSTP` | 20 | Arret terminal | Ctrl+Z |

**Exemples :**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### Signaux E/S

| Constante | Valeur | Description | Quand envoye |
|-----------|--------|-------------|--------------|
| `SIGPIPE` | 13 | Pipe casse | Ecriture vers pipe ferme |
| `SIGTTIN` | 21 | Lecture en arriere-plan depuis terminal | Processus BG lit TTY |
| `SIGTTOU` | 22 | Ecriture en arriere-plan vers terminal | Processus BG ecrit TTY |

**Exemples :**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## Gestion basique des signaux

### Intercepter Ctrl+C

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("SIGINT intercepte !");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// Le programme continue de s'executer...
// L'utilisateur appuie sur Ctrl+C -> handle_interrupt() est appele

while (!interrupted) {
    // Faire le travail...
}

print("Sortie due a l'interruption");
```

### Signature de fonction de gestionnaire

Les gestionnaires de signaux recoivent un argument : le numero de signal (i32)

```hemlock
fn my_handler(signum) {
    print("Signal recu : " + typeof(signum));
    // signum contient le numero de signal (ex. 2 pour SIGINT)

    if (signum == SIGINT) {
        print("C'est SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // Meme gestionnaire pour plusieurs signaux
```

### Gestionnaires de signaux multiples

Differents gestionnaires pour differents signaux :

```hemlock
fn handle_int(sig) {
    print("SIGINT recu");
}

fn handle_term(sig) {
    print("SIGTERM recu");
}

fn handle_usr1(sig) {
    print("SIGUSR1 recu");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### Reinitialisation au comportement par defaut

Passez `null` comme gestionnaire pour reinitialiser au comportement par defaut :

```hemlock
// Enregistrer un gestionnaire personnalise
signal(SIGINT, my_handler);

// Plus tard, reinitialiser au defaut (terminer sur SIGINT)
signal(SIGINT, null);
```

### Lever des signaux manuellement

Envoyer des signaux a votre propre processus :

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// Declencher le gestionnaire manuellement
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## Patterns avances

### Pattern d'arret gracieux

Pattern courant pour le nettoyage a la terminaison :

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Arret gracieux en cours...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// Boucle principale
while (!should_exit) {
    // Faire le travail...
    // Verifier le drapeau should_exit periodiquement
}

print("Nettoyage termine");
```

### Compteur de signaux

Suivre le nombre de signaux recus :

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Recu " + typeof(signal_count) + " signaux");
}

signal(SIGUSR1, count_signals);

// Plus tard...
print("Signaux totaux : " + typeof(signal_count));
```

### Rechargement de configuration sur signal

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Rechargement de la configuration...");
    config = load_config();
    print("Configuration rechargee");
}

signal(SIGHUP, reload_config);  // Recharger sur SIGHUP

// Envoyer SIGHUP au processus pour recharger la config
// Depuis le shell : kill -HUP <pid>
```

### Timeout utilisant SIGALRM

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout !");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// Definir l'alarme (pas encore implemente dans Hemlock, exemple seulement)
// alarm(5);  // timeout de 5 secondes

while (!timed_out) {
    // Faire le travail avec timeout
}
```

### Machine a etats basee sur signaux

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("Etat : " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("Etat : " + typeof(state));
}

signal(SIGUSR1, next_state);  // Avancer l'etat
signal(SIGUSR2, prev_state);  // Reculer

// Controler la machine a etats :
// kill -USR1 <pid>  # Etat suivant
// kill -USR2 <pid>  # Etat precedent
```

## Comportement des gestionnaires de signaux

### Notes importantes

**Execution des gestionnaires :**
- Les gestionnaires sont appeles **de maniere synchrone** quand le signal est recu
- Les gestionnaires s'executent dans le contexte du processus courant
- Les gestionnaires de signaux partagent l'environnement de closure de la fonction ou ils sont definis
- Les gestionnaires peuvent acceder et modifier les variables de portee externe (comme les globales ou les variables capturees)

**Bonnes pratiques :**
- Garder les gestionnaires simples et rapides - eviter les operations de longue duree
- Definir des drapeaux plutot que d'effectuer une logique complexe
- Eviter d'appeler des fonctions qui pourraient prendre des verrous
- Etre conscient que les gestionnaires peuvent interrompre n'importe quelle operation

### Quels signaux peuvent etre interceptes

**Peuvent etre interceptes et geres :**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (mais le programme s'arretera apres le retour du gestionnaire)

**Ne peuvent pas etre interceptes :**
- `SIGKILL` (9) - Termine toujours le processus
- `SIGSTOP` (19) - Arrete toujours le processus

**Dependant du systeme :**
- Certains signaux ont des comportements par defaut qui peuvent differer selon le systeme
- Consultez la documentation des signaux de votre plateforme pour les specificites

### Limitations des gestionnaires

```hemlock
fn complex_handler(sig) {
    // Eviter ceci dans les gestionnaires de signaux :

    // ❌ Operations de longue duree
    // process_large_file();

    // ❌ E/S bloquantes
    // let f = open("log.txt", "a");
    // f.write("Signal recu\n");

    // ❌ Changements d'etat complexes
    // rebuild_entire_data_structure();

    // ✅ La definition simple de drapeaux est sure
    let should_stop = true;

    // ✅ Les mises a jour simples de compteurs sont generalement sures
    let signal_count = signal_count + 1;
}
```

## Considerations de securite

La gestion des signaux est **inheremment non securisee** dans la philosophie de Hemlock.

### Conditions de course

Les gestionnaires peuvent etre appeles a tout moment, interrompant l'execution normale :

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // Condition de course si appele pendant la mise a jour du compteur
}

signal(SIGUSR1, increment);

// Le code principal modifie aussi le compteur
counter = counter + 1;  // Pourrait etre interrompu par le gestionnaire de signal
```

**Probleme :** Si le signal arrive pendant que le code principal met a jour `counter`, le resultat est imprevisible.

### Securite async-signal

Hemlock ne **garantit PAS** la securite async-signal :
- Les gestionnaires peuvent appeler n'importe quel code Hemlock (contrairement aux fonctions async-signal-safe restreintes du C)
- Cela fournit de la flexibilite mais necessite de la prudence de l'utilisateur
- Les conditions de course sont possibles si le gestionnaire modifie un etat partage

### Bonnes pratiques pour une gestion de signaux sure

**1. Utiliser des drapeaux atomiques**

Les assignations booleennes simples sont generalement sures :

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // L'assignation simple est sure
}

signal(SIGINT, handler);

while (!should_exit) {
    // travail...
}
```

**2. Minimiser l'etat partage**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // Modifier uniquement cette variable
    interrupt_count = interrupt_count + 1;
}
```

**3. Differer les operations complexes**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // Juste definir le drapeau
}

signal(SIGHUP, signal_reload);

// Dans la boucle principale :
while (true) {
    if (pending_reload) {
        reload_config();  // Faire le travail complexe ici
        pending_reload = false;
    }

    // Travail normal...
}
```

**4. Eviter les problemes de reentrance**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // Ne pas modifier les donnees pendant que le code principal les utilise
        return;
    }
    // Sur de proceder
}
```

## Cas d'utilisation courants

### 1. Arret gracieux de serveur

```hemlock
let running = true;

fn shutdown(sig) {
    print("Signal d'arret recu");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Boucle principale du serveur
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Serveur arrete");
```

### 2. Rechargement de configuration (sans redemarrage)

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Rechargement de la configuration...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // Utiliser la config...
}
```

### 3. Rotation des logs

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // Renommer l'ancien log, ouvrir le nouveau
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // Journalisation normale...
    log_file.write("Entree de log\n");
}
```

### 4. Rapport d'etat

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Etat : " + typeof(requests_handled) + " requetes traitees");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// Depuis le shell : kill -USR1 <pid>
```

### 5. Basculement du mode debug

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Mode debug : ACTIVE");
    } else {
        print("Mode debug : DESACTIVE");
    }
}

signal(SIGUSR2, toggle_debug);

// Depuis le shell : kill -USR2 <pid> pour basculer
```

## Exemples complets

### Exemple 1 : Gestionnaire d'interruption avec nettoyage

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Interruption detectee (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("Signal utilisateur 1 recu");
    }
}

// Enregistrer les gestionnaires
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// Simuler du travail
let i = 0;
while (running && i < 100) {
    print("Travail en cours... " + typeof(i));

    // Declencher SIGUSR1 toutes les 10 iterations
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Signaux totaux recus : " + typeof(signal_count));
```

### Exemple 2 : Machine a etats multi-signaux

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("Etat : " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("Etat : " + state);
}

fn report_stats(sig) {
    print("Etat : " + state);
    print("Requetes : " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // Faire le travail
        request_count = request_count + 1;
    }

    // Verifier a chaque iteration...
}
```

### Exemple 3 : Controleur de pool de workers

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Workers : " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Workers : " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Arret en cours...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// La boucle principale ajuste le pool de workers selon worker_count
while (!should_exit) {
    // Gerer les workers selon worker_count
    // ...
}
```

### Exemple 4 : Pattern de timeout

```hemlock
let operation_complete = false;
let timed_out = false;

fn timeout_handler(sig) {
    timed_out = true;
}

signal(SIGALRM, timeout_handler);

// Demarrer une operation longue
async fn long_operation() {
    // ... travail
    operation_complete = true;
}

let task = spawn(long_operation);

// Attendre avec timeout (verification manuelle)
let elapsed = 0;
while (!operation_complete && elapsed < 1000) {
    // Sleep ou verifier
    elapsed = elapsed + 1;
}

if (!operation_complete) {
    print("Operation expir");
    detach(task);  // Abandonner l'attente
} else {
    join(task);
    print("Operation terminee");
}
```

## Debogage des gestionnaires de signaux

### Ajouter des prints de diagnostic

```hemlock
fn debug_handler(sig) {
    print("Gestionnaire appele pour le signal : " + typeof(sig));
    print("Pile : (pas encore disponible)");

    // Votre logique de gestionnaire...
}

signal(SIGINT, debug_handler);
```

### Compter les appels de gestionnaire

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Appel de gestionnaire #" + typeof(handler_calls));

    // Votre logique de gestionnaire...
}
```

### Tester avec raise()

```hemlock
fn test_handler(sig) {
    print("Signal de test recu : " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// Tester en levant manuellement
raise(SIGUSR1);
print("Le gestionnaire devrait avoir ete appele");
```

## Resume

La gestion des signaux de Hemlock fournit :

- ✅ Gestion des signaux POSIX pour le controle de processus bas niveau
- ✅ 15 constantes de signaux standard
- ✅ API simple signal() et raise()
- ✅ Fonctions de gestionnaire flexibles avec support des closures
- ✅ Plusieurs signaux peuvent partager des gestionnaires

Rappelez-vous :
- La gestion des signaux est inheremment non securisee - utilisez avec prudence
- Garder les gestionnaires simples et rapides
- Utiliser des drapeaux pour les changements d'etat, pas des operations complexes
- Les gestionnaires peuvent interrompre l'execution a tout moment
- Impossible d'intercepter SIGKILL ou SIGSTOP
- Tester les gestionnaires minutieusement avec raise()

Patterns courants :
- Arret gracieux (SIGINT, SIGTERM)
- Rechargement de configuration (SIGHUP)
- Rotation des logs (SIGUSR1)
- Rapport d'etat (SIGUSR1/SIGUSR2)
- Basculement du mode debug (SIGUSR2)
