# Specification des paquets

Reference complete pour le format du fichier `package.json`.

## Apercu

Chaque paquet hpm necessite un fichier `package.json` a la racine du projet. Ce fichier definit les metadonnees du paquet, les dependances et les scripts.

## Exemple minimal

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Exemple complet

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
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

## Reference des champs

### name (obligatoire)

Le nom du paquet au format `owner/repo`.

```json
{
  "name": "hemlang/sprout"
}
```

**Exigences :**
- Doit etre au format `owner/repo`
- `owner` doit etre votre nom d'utilisateur GitHub ou organisation
- `repo` doit etre le nom du depot
- Utilisez des lettres minuscules, des chiffres et des tirets
- Maximum 214 caracteres au total

**Noms valides :**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Noms invalides :**
```
my-package          # Proprietaire manquant
hemlang/My_Package  # Majuscules et underscore
hemlang             # Depot manquant
```

### version (obligatoire)

La version du paquet suivant le [Versionnage semantique](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Format :** `MAJEUR.MINEUR.PATCH[-PRERELEASE][+BUILD]`

**Versions valides :**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Description courte du paquet.

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- Gardez-la sous 200 caracteres
- Decrivez ce que fait le paquet, pas comment

### author

Informations sur l'auteur du paquet.

```json
{
  "author": "Your Name <email@example.com>"
}
```

**Formats acceptes :**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

L'identifiant de licence.

```json
{
  "license": "MIT"
}
```

**Licences courantes :**
- `MIT` - Licence MIT
- `Apache-2.0` - Licence Apache 2.0
- `GPL-3.0` - Licence publique generale GNU v3.0
- `BSD-3-Clause` - Licence BSD 3 clauses
- `ISC` - Licence ISC
- `UNLICENSED` - Proprietaire/prive

Utilisez les [identifiants SPDX](https://spdx.org/licenses/) quand c'est possible.

### repository

Lien vers le depot source.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

URL de la page d'accueil du projet.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

URL du gestionnaire de tickets.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Fichier point d'entree du paquet.

```json
{
  "main": "src/index.hml"
}
```

**Defaut :** `src/index.hml`

Quand les utilisateurs importent votre paquet :
```hemlock
import { x } from "owner/repo";
```

hpm charge le fichier specifie dans `main`.

**Ordre de resolution pour les imports :**
1. Chemin exact : `src/index.hml`
2. Avec extension .hml : `src/index` -> `src/index.hml`
3. Fichier index : `src/index/` -> `src/index/index.hml`

### keywords

Tableau de mots-cles pour la decouverte.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Utilisez des minuscules
- Soyez specifique et pertinent
- Incluez le langage ("hemlock") si approprie

### dependencies

Dependances d'execution requises pour que le paquet fonctionne.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Cle :** Nom du paquet (`owner/repo`)
**Valeur :** Contrainte de version

**Syntaxe des contraintes de version :**

| Contrainte | Signification |
|------------|---------------|
| `1.2.3` | Version exacte |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Au moins 1.0.0 |
| `>=1.0.0 <2.0.0` | Plage |
| `*` | N'importe quelle version |

### devDependencies

Dependances uniquement pour le developpement (tests, compilation, etc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Les dependances de developpement sont :
- Installees pendant le developpement
- Non installees quand le paquet est utilise comme dependance
- Utilisees pour les tests, la compilation, le linting, etc.

### scripts

Commandes nommees qui peuvent etre executees avec `hpm run`.

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

**Executer des scripts :**
```bash
hpm run start
hpm run build
hpm test        # Raccourci pour 'hpm run test'
```

**Passer des arguments :**
```bash
hpm run test -- --verbose --filter=unit
```

**Scripts courants :**

| Script | Objectif |
|--------|----------|
| `start` | Demarrer l'application |
| `dev` | Mode developpement avec rechargement a chaud |
| `test` | Executer les tests |
| `build` | Compiler pour la production |
| `clean` | Supprimer les artefacts de compilation |
| `lint` | Verifier le style du code |
| `format` | Formater le code |

### files

Fichiers et repertoires a inclure quand le paquet est installe.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Comportement par defaut :** Si non specifie, inclut :
- Tous les fichiers du depot
- Exclut `.git/`, `node_modules/`, `hem_modules/`

**Utilisez pour :**
- Reduire la taille du paquet
- Exclure les fichiers de test de la distribution
- Inclure uniquement les fichiers necessaires

### native

Exigences de bibliotheques natives.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Documente les dependances natives qui doivent etre installees sur le systeme.

## Validation

hpm valide package.json lors de diverses operations. Erreurs de validation courantes :

### Champs obligatoires manquants

```
Error: package.json missing required field: name
```

**Correction :** Ajoutez le champ obligatoire.

### Format de nom invalide

```
Error: Invalid package name. Must be in owner/repo format.
```

**Correction :** Utilisez le format `owner/repo`.

### Version invalide

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Correction :** Utilisez le format semver complet (`1.0.0`).

### JSON invalide

```
Error: package.json is not valid JSON
```

**Correction :** Verifiez la syntaxe JSON (virgules, guillemets, crochets).

## Creer package.json

### Interactif

```bash
hpm init
```

Demande chaque champ de maniere interactive.

### Avec les valeurs par defaut

```bash
hpm init --yes
```

Cree avec les valeurs par defaut :
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Manuel

Creez le fichier manuellement :

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Bonnes pratiques

1. **Specifiez toujours main** - Ne vous fiez pas a la valeur par defaut
2. **Utilisez des plages caret** - `^1.0.0` pour la plupart des dependances
3. **Separez les dependances de developpement** - Gardez les deps test/build dans devDependencies
4. **Incluez des mots-cles** - Aidez les utilisateurs a trouver votre paquet
5. **Documentez les scripts** - Nommez les scripts clairement
6. **Specifiez la licence** - Obligatoire pour l'open source
7. **Ajoutez une description** - Aidez les utilisateurs a comprendre l'objectif

## Voir aussi

- [Creer des paquets](creating-packages.md) - Guide de publication
- [Versionnage](versioning.md) - Contraintes de version
- [Configuration du projet](project-setup.md) - Structure du projet
