# Demarrage rapide

Soyez operationnel avec hpm en 5 minutes.

## Installer hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Pour plus d'options d'installation, consultez le [Guide d'installation](installation.md).

## Creer un nouveau projet

Commencez par creer un nouveau repertoire et initialiser un paquet :

```bash
mkdir my-project
cd my-project
hpm init
```

Vous serez invite a saisir les details du projet :

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Utilisez `--yes` pour accepter toutes les valeurs par defaut :

```bash
hpm init --yes
```

## Structure du projet

Creez la structure de base du projet :

```
my-project/
├── package.json        # Manifeste du projet
├── src/
│   └── index.hml      # Point d'entree principal
└── test/
    └── test.hml       # Tests
```

Creez votre fichier principal :

```bash
mkdir -p src test
```

**src/index.hml :**
```hemlock
// Point d'entree principal
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## Installer des dependances

Recherchez des paquets sur GitHub (les paquets utilisent le format `owner/repo`) :

```bash
# Installer un paquet
hpm install hemlang/sprout

# Installer avec une contrainte de version
hpm install hemlang/json@^1.0.0

# Installer comme dependance de developpement
hpm install hemlang/test-utils --dev
```

Apres l'installation, la structure de votre projet inclut `hem_modules/` :

```
my-project/
├── package.json
├── package-lock.json   # Fichier de verrouillage (genere automatiquement)
├── hem_modules/        # Paquets installes
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Utiliser les paquets installes

Importez les paquets en utilisant leur chemin GitHub :

```hemlock
// Importer depuis un paquet installe
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Importer depuis un sous-chemin
import { middleware } from "hemlang/sprout/middleware";

// Bibliotheque standard (integree)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Ajouter des scripts

Ajoutez des scripts a votre `package.json` :

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Executez les scripts avec `hpm run` :

```bash
hpm run start
hpm run build

# Raccourci pour test
hpm test
```

## Flux de travail courants

### Installer toutes les dependances

Lorsque vous clonez un projet avec un `package.json` :

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Mettre a jour les dependances

Mettre a jour tous les paquets vers les dernieres versions dans les contraintes :

```bash
hpm update
```

Mettre a jour un paquet specifique :

```bash
hpm update hemlang/sprout
```

### Afficher les paquets installes

Lister tous les paquets installes :

```bash
hpm list
```

La sortie affiche l'arbre des dependances :

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Verifier les mises a jour disponibles

Voir quels paquets ont des versions plus recentes :

```bash
hpm outdated
```

### Supprimer un paquet

```bash
hpm uninstall hemlang/sprout
```

## Exemple : Application web

Voici un exemple complet utilisant un framework web :

**package.json :**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml :**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

Executez l'application :

```bash
hpm install
hpm run start
```

## Prochaines etapes

- [Reference des commandes](commands.md) - Apprenez toutes les commandes hpm
- [Creer des paquets](creating-packages.md) - Publiez vos propres paquets
- [Configuration](configuration.md) - Configurez hpm et les tokens GitHub
- [Configuration du projet](project-setup.md) - Configuration detaillee du projet
