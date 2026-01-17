# Configuration du projet

Guide complet pour configurer des projets Hemlock avec hpm.

## Demarrer un nouveau projet

### Configuration de base

Creer un nouveau projet a partir de zero :

```bash
# Creer le repertoire du projet
mkdir my-project
cd my-project

# Initialiser package.json
hpm init

# Creer la structure des repertoires
mkdir -p src test
```

### Modeles de projets

Voici des structures de projets courantes pour differents cas d'utilisation :

#### Paquet bibliotheque

Pour les bibliotheques reutilisables :

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Entree principale, exporte l'API publique
│   ├── core.hml           # Fonctionnalites principales
│   ├── utils.hml          # Fonctions utilitaires
│   └── types.hml          # Definitions de types
└── test/
    ├── framework.hml      # Framework de test
    ├── run.hml            # Lanceur de tests
    └── test_core.hml      # Tests
```

**package.json :**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Application

Pour les applications autonomes :

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Point d'entree de l'application
│   ├── config.hml         # Configuration
│   ├── commands/          # Commandes CLI
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Bibliotheques internes
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Fichiers de donnees
```

**package.json :**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Application web

Pour les serveurs web :

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Point d'entree du serveur
│   ├── routes/            # Gestionnaires de routes
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Modeles de donnees
│   │   └── user.hml
│   └── services/          # Logique metier
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Fichiers statiques
│   ├── css/
│   └── js/
└── views/                 # Templates
    └── index.hml
```

**package.json :**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## Le fichier package.json

### Champs obligatoires

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### Tous les champs

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

### Reference des champs

| Champ | Type | Description |
|-------|------|-------------|
| `name` | string | Nom du paquet au format owner/repo (obligatoire) |
| `version` | string | Version semantique (obligatoire) |
| `description` | string | Description courte |
| `author` | string | Nom et email de l'auteur |
| `license` | string | Identifiant de licence (MIT, Apache-2.0, etc.) |
| `repository` | string | URL du depot |
| `homepage` | string | Page d'accueil du projet |
| `bugs` | string | URL du gestionnaire de tickets |
| `main` | string | Fichier point d'entree (defaut : src/index.hml) |
| `keywords` | array | Mots-cles de recherche |
| `dependencies` | object | Dependances d'execution |
| `devDependencies` | object | Dependances de developpement |
| `scripts` | object | Scripts nommes |
| `files` | array | Fichiers a inclure lors de la publication |
| `native` | object | Exigences de bibliotheques natives |

## Le fichier package-lock.json

Le fichier de verrouillage est genere automatiquement et doit etre commite dans le controle de version. Il garantit des installations reproductibles.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Bonnes pratiques pour le fichier de verrouillage

- **Commitez** package-lock.json dans le controle de version
- **Ne modifiez pas** manuellement - il est genere automatiquement
- **Executez `hpm install`** apres avoir tire des modifications
- **Supprimez et regenerez** si corrompu :
  ```bash
  rm package-lock.json
  hpm install
  ```

## Le repertoire hem_modules

Les paquets installes sont stockes dans `hem_modules/` :

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### Bonnes pratiques pour hem_modules

- **Ajoutez a .gitignore** - ne commitez pas les dependances
- **Ne modifiez pas** - les modifications seront ecrasees
- **Supprimez pour reinstaller proprement** :
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Fichier .gitignore recommande pour les projets Hemlock :

```gitignore
# Dependances
hem_modules/

# Sortie de compilation
dist/
*.hmlc

# Fichiers IDE
.idea/
.vscode/
*.swp
*.swo

# Fichiers OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environnement
.env
.env.local

# Couverture de tests
coverage/
```

## Travailler avec les dependances

### Ajouter des dependances

```bash
# Ajouter une dependance d'execution
hpm install hemlang/json

# Ajouter avec une contrainte de version
hpm install hemlang/sprout@^2.0.0

# Ajouter une dependance de developpement
hpm install hemlang/test-utils --dev
```

### Importer des dependances

```hemlock
// Importer depuis un paquet (utilise l'entree "main")
import { parse, stringify } from "hemlang/json";

// Importer depuis un sous-chemin
import { Router } from "hemlang/sprout/router";

// Importer la bibliotheque standard
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Resolution des imports

hpm resout les imports dans cet ordre :

1. **Bibliotheque standard** : les imports `@stdlib/*` chargent les modules integres
2. **Racine du paquet** : `owner/repo` utilise le champ `main`
3. **Sous-chemin** : `owner/repo/path` verifie :
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Scripts

### Definir des scripts

Ajoutez des scripts a package.json :

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

### Executer des scripts

```bash
hpm run start
hpm run dev
hpm run build

# Raccourci pour test
hpm test

# Passer des arguments
hpm run test -- --verbose --filter=unit
```

### Conventions de nommage des scripts

| Script | Objectif |
|--------|----------|
| `start` | Executer l'application |
| `dev` | Executer en mode developpement |
| `test` | Executer tous les tests |
| `build` | Compiler pour la production |
| `clean` | Supprimer les fichiers generes |
| `lint` | Verifier le style du code |
| `format` | Formater le code |

## Flux de travail de developpement

### Configuration initiale

```bash
# Cloner le projet
git clone https://github.com/yourusername/my-project.git
cd my-project

# Installer les dependances
hpm install

# Executer les tests
hpm test

# Demarrer le developpement
hpm run dev
```

### Flux de travail quotidien

```bash
# Tirer les dernieres modifications
git pull

# Installer les nouvelles dependances
hpm install

# Faire des modifications...

# Executer les tests
hpm test

# Commiter
git add .
git commit -m "Add feature"
git push
```

### Ajouter une nouvelle fonctionnalite

```bash
# Creer une branche de fonctionnalite
git checkout -b feature/new-feature

# Ajouter une nouvelle dependance si necessaire
hpm install hemlang/new-lib

# Implementer la fonctionnalite...

# Tester
hpm test

# Commiter et pousser
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## Configuration specifique a l'environnement

### Utiliser les variables d'environnement

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### Fichier de configuration

**config.hml :**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## Voir aussi

- [Demarrage rapide](quick-start.md) - Commencez rapidement
- [Commandes](commands.md) - Reference des commandes
- [Creer des paquets](creating-packages.md) - Publication de paquets
- [Configuration](configuration.md) - Configuration de hpm
