# Arguments en ligne de commande dans Hemlock

Les programmes Hemlock peuvent acceder aux arguments en ligne de commande via un **tableau `args` integre** qui est automatiquement rempli au demarrage du programme.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Le tableau args](#le-tableau-args)
- [Proprietes](#proprietes)
- [Patterns d'iteration](#patterns-diteration)
- [Cas d'utilisation courants](#cas-dutilisation-courants)
- [Patterns d'analyse d'arguments](#patterns-danalyse-darguments)
- [Bonnes pratiques](#bonnes-pratiques)
- [Exemples complets](#exemples-complets)

## Vue d'ensemble

Le tableau `args` fournit un acces aux arguments en ligne de commande passes a votre programme Hemlock :

- **Toujours disponible** - Variable globale integree dans tous les programmes Hemlock
- **Nom du script inclus** - `args[0]` contient toujours le chemin/nom du script
- **Tableau de chaines** - Tous les arguments sont des chaines
- **Indexe a zero** - Indexation standard de tableau (0, 1, 2, ...)

## Le tableau args

### Structure de base

```hemlock
// args[0] est toujours le nom du fichier script
// args[1] a args[n-1] sont les arguments reels
print(args[0]);        // "script.hml"
print(args.length);    // Nombre total d'arguments (incluant le nom du script)
```

### Exemple d'utilisation

**Commande :**
```bash
./hemlock script.hml hello world "test 123"
```

**Dans script.hml :**
```hemlock
print("Nom du script : " + args[0]);     // "script.hml"
print("Total args : " + typeof(args.length));  // "4"
print("Premier arg : " + args[1]);       // "hello"
print("Deuxieme arg : " + args[2]);      // "world"
print("Troisieme arg : " + args[3]);     // "test 123"
```

### Reference des index

| Index | Contient | Valeur d'exemple |
|-------|----------|------------------|
| `args[0]` | Chemin/nom du script | `"script.hml"` ou `"./script.hml"` |
| `args[1]` | Premier argument | `"hello"` |
| `args[2]` | Deuxieme argument | `"world"` |
| `args[3]` | Troisieme argument | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Dernier argument | (variable) |

## Proprietes

### Toujours present

`args` est un tableau global disponible dans **tous** les programmes Hemlock :

```hemlock
// Pas besoin de declarer ou d'importer
print(args.length);  // Fonctionne immediatement
```

### Nom du script inclus

`args[0]` contient toujours le chemin/nom du script :

```hemlock
print("Execution de : " + args[0]);
```

**Valeurs possibles pour args[0] :**
- `"script.hml"` - Juste le nom de fichier
- `"./script.hml"` - Chemin relatif
- `"/home/user/script.hml"` - Chemin absolu
- Depend de la facon dont le script a ete invoque

### Type : Tableau de chaines

Tous les arguments sont stockes comme chaines :

```hemlock
// Arguments : ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (chaine, pas nombre)
print(args[2]);  // "3.14" (chaine, pas nombre)
print(args[3]);  // "true" (chaine, pas booleen)

// Convertir si necessaire :
let num = 42;  // Parser manuellement si necessaire
```

### Longueur minimale

Toujours au moins 1 (le nom du script) :

```hemlock
print(args.length);  // Minimum : 1
```

**Meme sans arguments :**
```bash
./hemlock script.hml
```

```hemlock
// Dans script.hml :
print(args.length);  // 1 (juste le nom du script)
```

### Comportement du REPL

Dans le REPL, `args.length` est 0 (tableau vide) :

```hemlock
# Session REPL
> print(args.length);
0
```

## Patterns d'iteration

### Iteration de base

Ignorer `args[0]` (nom du script) et traiter les arguments reels :

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + " : " + args[i]);
    i = i + 1;
}
```

**Sortie pour : `./hemlock script.hml foo bar baz`**
```
Argument 1 : foo
Argument 2 : bar
Argument 3 : baz
```

### Iteration for-in (incluant le nom du script)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Sortie :**
```
script.hml
foo
bar
baz
```

### Verification du nombre d'arguments

```hemlock
if (args.length < 2) {
    print("Usage : " + args[0] + " <argument>");
    // exit ou return
} else {
    let arg = args[1];
    // traiter arg
}
```

### Traitement de tous les arguments sauf le nom du script

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Traitement : " + arg);
}
```

## Cas d'utilisation courants

### 1. Traitement d'argument simple

Verifier un argument requis :

```hemlock
if (args.length < 2) {
    print("Usage : " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Traitement du fichier : " + filename);
    // ... traiter le fichier
}
```

**Utilisation :**
```bash
./hemlock script.hml data.txt
# Sortie : Traitement du fichier : data.txt
```

### 2. Arguments multiples

```hemlock
if (args.length < 3) {
    print("Usage : " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Entree : " + input_file);
    print("Sortie : " + output_file);

    // Traiter les fichiers...
}
```

**Utilisation :**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. Nombre variable d'arguments

Traiter tous les arguments fournis :

```hemlock
if (args.length < 2) {
    print("Usage : " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Traitement de " + typeof(args.length - 1) + " fichiers :");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**Utilisation :**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Message d'aide

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Usage : " + args[0] + " [OPTIONS] <file>");
    print("Options :");
    print("  -h, --help     Afficher ce message d'aide");
    print("  -v, --verbose  Activer la sortie verbeuse");
} else {
    // Traitement normal
}
```

### 5. Validation d'arguments

```hemlock
fn validate_file(filename: string): bool {
    // Verifier si le fichier existe (exemple)
    return filename != "";
}

if (args.length < 2) {
    print("Erreur : Pas de nom de fichier fourni");
} else if (!validate_file(args[1])) {
    print("Erreur : Fichier invalide : " + args[1]);
} else {
    print("Traitement : " + args[1]);
}
```

## Patterns d'analyse d'arguments

### Arguments nommes (drapeaux)

Pattern simple pour les arguments nommes :

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Mode verbeux active");
}
print("Entree : " + input_file);
print("Sortie : " + output_file);
```

**Utilisation :**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Drapeaux booleens

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### Arguments avec valeurs

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // Necessiterait de parser la chaine en int
        }
    }
    i = i + 1;
}
```

### Arguments positionnels et nommes melanges

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // Traiter comme argument positionnel
        positional.push(args[i]);
    }
    i = i + 1;
}

// Assigner les arguments positionnels
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### Fonction d'aide a l'analyse d'arguments

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // Argument positionnel
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose : " + typeof(opts.verbose));
print("Output : " + opts.output);
print("Fichiers : " + typeof(opts.files.length));
```

## Bonnes pratiques

### 1. Toujours verifier le nombre d'arguments

```hemlock
// Bien
if (args.length < 2) {
    print("Usage : " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// Mauvais - peut planter si pas d'arguments
process_file(args[1]);  // Erreur si args.length == 1
```

### 2. Fournir des informations d'utilisation

```hemlock
fn show_usage() {
    print("Usage : " + args[0] + " [OPTIONS] <file>");
    print("Options :");
    print("  -h, --help     Afficher l'aide");
    print("  -v, --verbose  Sortie verbeuse");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. Valider les arguments

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Erreur : Argument requis manquant");
        return false;
    }

    if (args[1] == "") {
        print("Erreur : Argument vide");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // exit ou afficher l'utilisation
}
```

### 4. Utiliser des noms de variables descriptifs

```hemlock
// Bien
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// Mauvais
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Gerer les arguments avec espaces entre guillemets

Le shell gere cela automatiquement :

```bash
./hemlock script.hml "fichier avec espaces.txt"
```

```hemlock
print(args[1]);  // "fichier avec espaces.txt"
```

### 6. Creer des objets d'arguments

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Entree : " + arguments.input);
```

## Exemples complets

### Exemple 1 : Processeur de fichiers

```hemlock
// Usage : ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Usage : " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Traitement de " + input + " -> " + output);

    // Traiter les fichiers
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // Exemple de traitement
        f_out.write(processed);

        print("Termine !");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Exemple 2 : Processeur de fichiers par lots

```hemlock
// Usage : ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Usage : " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Traitement de " + typeof(args.length - 1) + " fichiers :");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Traitement : " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // Traiter le contenu...
            print("    " + typeof(content.length) + " octets");
        } catch (e) {
            print("    Erreur : " + e);
        }

        i = i + 1;
    }

    print("Termine !");
}
```

### Exemple 3 : Analyseur d'arguments avance

```hemlock
// Usage : ./hemlock app.hml [OPTIONS] <files...>
// Options :
//   --verbose, -v     Activer la sortie verbeuse
//   --output, -o FILE Definir le fichier de sortie
//   --help, -h        Afficher l'aide

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Erreur : --output necessite une valeur");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Erreur : Option inconnue : " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Usage : " + args[0] + " [OPTIONS] <files...>");
    print("Options :");
    print("  --verbose, -v     Activer la sortie verbeuse");
    print("  --output, -o FILE Definir le fichier de sortie");
    print("  --help, -h        Afficher cette aide");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Erreur : Aucun fichier d'entree specifie");
    show_help();
} else {
    if (config.verbose) {
        print("Mode verbeux active");
        print("Fichier de sortie : " + config.output);
        print("Fichiers d'entree : " + typeof(config.files.length));
    }

    // Traiter les fichiers
    for (let file in config.files) {
        if (config.verbose) {
            print("Traitement : " + file);
        }
        // ... traiter le fichier
    }
}
```

### Exemple 4 : Outil de configuration

```hemlock
// Usage : ./hemlock config.hml <action> [arguments]
// Actions :
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Usage : " + args[0] + " <action> [arguments]");
    print("Actions :");
    print("  get <key>         Obtenir une valeur de configuration");
    print("  set <key> <value> Definir une valeur de configuration");
    print("  list              Lister toute la configuration");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Erreur : 'get' necessite une cle");
        } else {
            let key = args[2];
            print("Obtention de : " + key);
            // ... obtenir depuis la config
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Erreur : 'set' necessite cle et valeur");
        } else {
            let key = args[2];
            let value = args[3];
            print("Definition de " + key + " = " + value);
            // ... definir dans la config
        }
    } else if (action == "list") {
        print("Liste de toute la configuration :");
        // ... lister la config
    } else {
        print("Erreur : Action inconnue : " + action);
        show_usage();
    }
}
```

## Resume

Le support des arguments en ligne de commande de Hemlock fournit :

- ✅ Tableau `args` integre disponible globalement
- ✅ Acces simple base sur tableau aux arguments
- ✅ Nom du script dans `args[0]`
- ✅ Tous les arguments en tant que chaines
- ✅ Methodes de tableau disponibles (.length, .slice, etc.)

Rappelez-vous :
- Toujours verifier `args.length` avant d'acceder aux elements
- `args[0]` est le nom du script
- Les arguments reels commencent a `args[1]`
- Tous les arguments sont des chaines - convertir si necessaire
- Fournir des informations d'utilisation pour des outils conviviaux
- Valider les arguments avant le traitement

Patterns courants :
- Arguments positionnels simples
- Arguments nommes/drapeaux (--flag)
- Arguments avec valeurs (--option value)
- Messages d'aide (--help)
- Validation d'arguments
