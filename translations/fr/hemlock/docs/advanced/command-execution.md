# Execution de commandes dans Hemlock

Hemlock fournit la **fonction integree `exec()`** pour executer des commandes shell et capturer leur sortie.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [La fonction exec()](#la-fonction-exec)
- [Objet resultat](#objet-resultat)
- [Utilisation de base](#utilisation-de-base)
- [Exemples avances](#exemples-avances)
- [Gestion des erreurs](#gestion-des-erreurs)
- [Details d'implementation](#details-dimplementation)
- [Considerations de securite](#considerations-de-securite)
- [Limitations](#limitations)
- [Cas d'utilisation](#cas-dutilisation)
- [Bonnes pratiques](#bonnes-pratiques)
- [Exemples complets](#exemples-complets)

## Vue d'ensemble

La fonction `exec()` permet aux programmes Hemlock de :
- Executer des commandes shell
- Capturer la sortie standard (stdout)
- Verifier les codes de sortie
- Utiliser les fonctionnalites du shell (pipes, redirections, etc.)
- S'integrer avec les utilitaires systeme

**Important :** Les commandes sont executees via `/bin/sh`, donnant un acces complet aux fonctionnalites du shell mais introduisant aussi des considerations de securite.

## La fonction exec()

### Signature

```hemlock
exec(command: string): object
```

**Parametres :**
- `command` (string) - Commande shell a executer

**Retourne :** Un objet avec deux champs :
- `output` (string) - La sortie stdout de la commande
- `exit_code` (i32) - Le code de sortie de la commande

### Exemple de base

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## Objet resultat

L'objet retourne par `exec()` a la structure suivante :

```hemlock
{
    output: string,      // Stdout de la commande (sortie capturee)
    exit_code: i32       // Statut de sortie du processus (0 = succes)
}
```

### Champ output

Contient tout le texte ecrit sur stdout par la commande.

**Proprietes :**
- Chaine vide si la commande ne produit pas de sortie
- Inclut les retours a la ligne et espaces tels quels
- La sortie multi-lignes est preservee
- Pas de limite de taille (allouee dynamiquement)

**Exemples :**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Listing du repertoire avec retours a la ligne

let r3 = exec("true");
print(r3.output);  // "" (chaine vide)
```

### Champ exit_code

Le code de sortie de la commande.

**Valeurs :**
- `0` indique typiquement le succes
- `1-255` indiquent des erreurs (la convention varie selon la commande)
- `-1` si la commande n'a pas pu etre executee ou s'est terminee anormalement

**Exemples :**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (succes)

let r2 = exec("false");
print(r2.exit_code);  // 1 (echec)

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2 (fichier non trouve, varie selon la commande)
```

## Utilisation de base

### Commande simple

```hemlock
let r = exec("ls -la");
print(r.output);
print("Code de sortie : " + typeof(r.exit_code));
```

### Verification du statut de sortie

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Trouve : " + r.output);
} else {
    print("Pattern non trouve");
}
```

### Commandes avec pipes

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Commandes multiples

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Substitution de commandes

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Date actuelle
```

## Exemples avances

### Gestion des echecs

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Commande echouee avec le code : " + typeof(r.exit_code));
    print("Sortie d'erreur : " + r.output);  // Note : stderr non capture
}
```

### Traitement de sortie multi-lignes

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Ligne " + typeof(i) + " : " + lines[i]);
    i = i + 1;
}
```

### Chainage de commandes

**Avec && (ET) :**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Configuration terminee");
}
```

**Avec || (OU) :**
```hemlock
let r = exec("command1 || command2");
// Execute command2 seulement si command1 echoue
```

**Avec ; (sequence) :**
```hemlock
let r = exec("command1; command2");
// Execute les deux peu importe le succes/echec
```

### Utilisation des pipes

```hemlock
let r = exec("echo 'data' | base64");
print("Base64 : " + r.output);
```

**Pipelines complexes :**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Patterns de codes de sortie

Differents codes de sortie indiquent differentes conditions :

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Le fichier existe");
} else if (r.exit_code == 1) {
    print("Le fichier n'existe pas");
} else {
    print("Commande test echouee : " + typeof(r.exit_code));
}
```

### Redirections de sortie

```hemlock
// Rediriger stdout vers un fichier (dans le shell)
let r1 = exec("echo 'test' > /tmp/output.txt");

// Rediriger stderr vers stdout (Note : stderr toujours non capture par Hemlock)
let r2 = exec("command 2>&1");
```

### Variables d'environnement

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### Changements de repertoire de travail

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Gestion des erreurs

### Quand exec() lance des exceptions

La fonction `exec()` lance une exception si la commande ne peut pas etre executee :

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Echec d'execution : " + e);
}
```

**Les exceptions sont lancees quand :**
- `popen()` echoue (ex. impossible de creer un pipe)
- Limites de ressources systeme depassees
- Echecs d'allocation memoire

### Quand exec() NE lance PAS d'exception

```hemlock
// La commande s'execute mais retourne un code de sortie non nul
let r1 = exec("false");
print(r1.exit_code);  // 1 (pas une exception)

// La commande ne produit pas de sortie
let r2 = exec("true");
print(r2.output);  // "" (pas une exception)

// Commande non trouvee par le shell
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127 (pas une exception)
```

### Pattern d'execution securisee

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Attention : Commande echouee avec le code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Erreur lors de l'execution de la commande : " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## Details d'implementation

### Comment ca fonctionne

**En interne :**
- Utilise `popen()` pour executer les commandes via `/bin/sh`
- Capture uniquement stdout (stderr n'est pas capture)
- Sortie mise en tampon dynamiquement (commence a 4Ko, augmente si necessaire)
- Statut de sortie extrait avec les macros `WIFEXITED()` et `WEXITSTATUS()`
- La chaine de sortie est correctement terminee par null

**Flux du processus :**
1. `popen(command, "r")` cree un pipe et fork le processus
2. Le processus enfant execute `/bin/sh -c "command"`
3. Le parent lit stdout via le pipe dans un tampon croissant
4. `pclose()` attend l'enfant et retourne le statut de sortie
5. Le statut de sortie est extrait et stocke dans l'objet resultat

### Considerations de performance

**Couts :**
- Cree un nouveau processus shell pour chaque appel (~1-5ms de surcharge)
- Sortie stockee entierement en memoire (pas de streaming)
- Pas de support du streaming (attend la completion de la commande)
- Adapte pour les commandes avec des tailles de sortie raisonnables

**Optimisations :**
- Le tampon commence a 4Ko et double quand il est plein (utilisation memoire efficace)
- Boucle de lecture unique minimise les appels systeme
- Pas de copie de chaine supplementaire

**Quand utiliser :**
- Commandes courtes (< 1 seconde)
- Taille de sortie moderee (< 10Mo)
- Operations batch avec des intervalles raisonnables

**Quand NE PAS utiliser :**
- Daemons ou services de longue duree
- Commandes produisant des gigaoctets de sortie
- Traitement de donnees en streaming temps reel
- Execution haute frequence (> 100 appels/seconde)

## Considerations de securite

### Risque d'injection shell

⚠️ **CRITIQUE :** Les commandes sont executees par le shell (`/bin/sh`), ce qui signifie que **l'injection shell est possible**.

**Code vulnerable :**
```hemlock
// DANGEREUX - NE FAITES PAS CELA
let filename = args[1];  // Entree utilisateur
let r = exec("cat " + filename);  // Injection shell !
```

**Attaque :**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Execute : cat ; rm -rf /; echo pwned
```

### Pratiques securisees

**1. Ne jamais utiliser d'entree utilisateur non assainie :**
```hemlock
// Mauvais
let user_input = args[1];
let r = exec("process " + user_input);  // DANGEREUX

// Bon - valider d'abord
fn is_safe_filename(name: string): bool {
    // Autoriser uniquement alphanumerique, tiret, underscore, point
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Nom de fichier invalide");
}
```

**2. Utiliser des listes blanches, pas des listes noires :**
```hemlock
// Bon - liste blanche stricte
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Commande invalide");
}
```

**3. Echapper les caracteres speciaux :**
```hemlock
fn shell_escape(s: string): string {
    // Echappement simple - entourer de guillemets simples et echapper les guillemets simples
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. Eviter exec() pour les operations sur fichiers :**
```hemlock
// Mauvais - utiliser exec pour les operations sur fichiers
let r = exec("cat file.txt");

// Bon - utiliser l'API de fichiers Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### Considerations de permissions

Les commandes s'executent avec les memes permissions que le processus Hemlock :

```hemlock
// Si Hemlock s'execute en root, les commandes exec() s'executent aussi en root !
let r = exec("rm -rf /important");  // DANGEREUX si execution en root
```

**Bonne pratique :** Executez Hemlock avec le minimum de privileges necessaires.

## Limitations

### 1. Pas de capture de stderr

Seul stdout est capture, stderr va au terminal :

```hemlock
let r = exec("ls /nonexistent");
// r.output est vide
// Le message d'erreur apparait sur le terminal, non capture
```

**Solution de contournement - rediriger stderr vers stdout :**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// Maintenant les messages d'erreur sont dans r.output
```

### 2. Pas de streaming

Doit attendre la completion de la commande :

```hemlock
let r = exec("long_running_command");
// Bloque jusqu'a ce que la commande finisse
// Impossible de traiter la sortie incrementalement
```

### 3. Pas de timeout

Les commandes peuvent s'executer indefiniment :

```hemlock
let r = exec("sleep 1000");
// Bloque pendant 1000 secondes
// Pas de moyen de timeout ou annuler
```

**Solution de contournement - utiliser la commande timeout :**
```hemlock
let r = exec("timeout 5 long_command");
// Expirera apres 5 secondes
```

### 4. Pas de gestion des signaux

Impossible d'envoyer des signaux aux commandes en cours d'execution :

```hemlock
let r = exec("long_command");
// Impossible d'envoyer SIGINT, SIGTERM, etc. a la commande
```

### 5. Pas de controle de processus

Impossible d'interagir avec la commande apres le demarrage :

```hemlock
let r = exec("interactive_program");
// Impossible d'envoyer de l'entree au programme
// Impossible de controler l'execution
```

## Cas d'utilisation

### Bons cas d'utilisation

**1. Execution d'utilitaires systeme :**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Traitement rapide de donnees avec les outils Unix :**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Lignes uniques : " + r.output);
```

**3. Verification de l'etat systeme :**
```hemlock
let r = exec("df -h");
print("Utilisation disque :\n" + r.output);
```

**4. Verification d'existence de fichier :**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Le fichier existe");
}
```

**5. Generation de rapports :**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Instances en cours : " + count);
```

**6. Scripts d'automatisation :**
```hemlock
exec("git add .");
exec("git commit -m 'Commit automatique'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push echoue");
}
```

### Non recommande pour

**1. Services de longue duree :**
```hemlock
// Mauvais
let r = exec("nginx");  // Bloque indefiniment
```

**2. Commandes interactives :**
```hemlock
// Mauvais - impossible de fournir de l'entree
let r = exec("ssh user@host");
```

**3. Commandes produisant d'enormes sorties :**
```hemlock
// Mauvais - charge toute la sortie en memoire
let r = exec("cat 10GB_file.log");
```

**4. Streaming temps reel :**
```hemlock
// Mauvais - impossible de traiter la sortie incrementalement
let r = exec("tail -f /var/log/app.log");
```

**5. Gestion d'erreurs critique :**
```hemlock
// Mauvais - stderr non capture
let r = exec("critical_operation");
// Impossible de voir les messages d'erreur detailles
```

## Bonnes pratiques

### 1. Toujours verifier les codes de sortie

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Commande echouee !");
    // Gerer l'erreur
}
```

### 2. Nettoyer la sortie si necessaire

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // Supprimer le retour a la ligne final
print(clean);  // "test" (sans retour a la ligne)
```

### 3. Valider avant d'executer

```hemlock
fn is_valid_command(cmd: string): bool {
    // Valider que la commande est sure
    return true;  // Votre logique de validation
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. Utiliser try/catch pour les operations critiques

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Commande echouee";
    }
} catch (e) {
    print("Erreur : " + e);
    // Nettoyage ou recuperation
}
```

### 5. Preferer les APIs Hemlock a exec()

```hemlock
// Mauvais - utiliser exec pour les operations sur fichiers
let r = exec("cat file.txt");

// Bon - utiliser l'API File de Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. Capturer stderr si necessaire

```hemlock
// Rediriger stderr vers stdout
let r = exec("command 2>&1");
// Maintenant r.output contient stdout et stderr
```

### 7. Utiliser les fonctionnalites du shell judicieusement

```hemlock
// Utiliser les pipes pour l'efficacite
let r = exec("cat large.txt | grep pattern | head -n 10");

// Utiliser la substitution de commandes
let r = exec("echo Utilisateur actuel : $(whoami)");

// Utiliser l'execution conditionnelle
let r = exec("test -f file.txt && cat file.txt");
```

## Exemples complets

### Exemple 1 : Collecteur d'informations systeme

```hemlock
fn get_system_info() {
    print("=== Informations systeme ===");

    // Nom d'hote
    let r1 = exec("hostname");
    print("Nom d'hote : " + r1.output.trim());

    // Uptime
    let r2 = exec("uptime");
    print("Uptime : " + r2.output.trim());

    // Utilisation disque
    let r3 = exec("df -h /");
    print("\nUtilisation disque :");
    print(r3.output);

    // Utilisation memoire
    let r4 = exec("free -h");
    print("Utilisation memoire :");
    print(r4.output);
}

get_system_info();
```

### Exemple 2 : Analyseur de logs

```hemlock
fn analyze_log(logfile: string) {
    print("Analyse du log : " + logfile);

    // Compter le nombre total de lignes
    let r1 = exec("wc -l " + logfile);
    print("Lignes totales : " + r1.output.trim());

    // Compter les erreurs
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Erreurs : " + errors);
    } else {
        print("Erreurs : 0");
    }

    // Compter les avertissements
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Avertissements : " + warnings);
    } else {
        print("Avertissements : 0");
    }

    // Erreurs recentes
    print("\nErreurs recentes :");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Usage : " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### Exemple 3 : Assistant Git

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Erreur : Pas un depot git");
        return;
    }

    if (r.output == "") {
        print("Repertoire de travail propre");
    } else {
        print("Modifications :");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Ajout de toutes les modifications...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Erreur lors de l'ajout des fichiers");
        return;
    }

    print("Commit en cours...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Erreur lors du commit");
        return;
    }

    print("Commit reussi");
    print(r2.output);
}

// Utilisation
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### Exemple 4 : Script de sauvegarde

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Sauvegarde de " + source + " vers " + dest);

    // Creer le repertoire de sauvegarde
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Erreur lors de la creation du repertoire de sauvegarde");
        return false;
    }

    // Creer une archive avec horodatage
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Creation de l'archive : " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Erreur lors de la creation de la sauvegarde :");
        print(r3.output);
        return false;
    }

    print("Sauvegarde terminee avec succes");

    // Afficher la taille de la sauvegarde
    let r4 = exec("du -h " + backup_file);
    print("Taille de la sauvegarde : " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Usage : " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Resume

La fonction `exec()` de Hemlock fournit :

- ✅ Execution simple de commandes shell
- ✅ Capture de sortie (stdout)
- ✅ Verification du code de sortie
- ✅ Acces complet aux fonctionnalites du shell (pipes, redirections, etc.)
- ✅ Integration avec les utilitaires systeme

Rappelez-vous :
- Toujours verifier les codes de sortie
- Etre conscient des implications de securite (injection shell)
- Valider les entrees utilisateur avant de les utiliser dans les commandes
- Preferer les APIs Hemlock a exec() quand c'est possible
- stderr n'est pas capture (utilisez `2>&1` pour rediriger)
- Les commandes bloquent jusqu'a completion
- Utilisez pour les utilitaires courts, pas les services de longue duree

**Liste de verification de securite :**
- ❌ Ne jamais utiliser d'entree utilisateur non assainie
- ✅ Valider toutes les entrees
- ✅ Utiliser des listes blanches pour les commandes
- ✅ Echapper les caracteres speciaux si necessaire
- ✅ Executer avec le minimum de privileges
- ✅ Preferer les APIs Hemlock aux commandes shell
