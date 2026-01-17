# Creer des paquets

Ce guide explique comment creer, structurer et publier des paquets Hemlock.

## Apercu

hpm utilise GitHub comme registre de paquets. Les paquets sont identifies par leur chemin GitHub `owner/repo`, et les versions sont des tags Git. Publier consiste simplement a pousser une release taguee.

## Creer un nouveau paquet

### 1. Initialiser le paquet

Creez un nouveau repertoire et initialisez :

```bash
mkdir my-package
cd my-package
hpm init
```

Repondez aux invites :

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Creer la structure du projet

Structure recommandee pour les paquets :

```
my-package/
├── package.json          # Manifeste du paquet
├── README.md             # Documentation
├── LICENSE               # Fichier de licence
├── src/
│   ├── index.hml         # Point d'entree principal (exporte l'API publique)
│   ├── utils.hml         # Utilitaires internes
│   └── types.hml         # Definitions de types
└── test/
    ├── framework.hml     # Framework de test
    └── test_utils.hml    # Tests
```

### 3. Definir votre API publique

**src/index.hml** - Point d'entree principal :

```hemlock
// Reexporter l'API publique
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Exports directs
export fn create(options: Options): Config {
    // Implementation
}

export fn validate(config: Config): bool {
    // Implementation
}
```

### 4. Ecrire votre package.json

Exemple complet de package.json :

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Nommage des paquets

### Exigences

- Doit etre au format `owner/repo`
- `owner` doit etre votre nom d'utilisateur GitHub ou organisation
- `repo` doit etre le nom du depot
- Utilisez des minuscules avec des tirets pour les noms composes

### Bons noms

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### A eviter

```
my-package          # Proprietaire manquant
alice/MyPackage     # PascalCase
alice/my_package    # Underscores
```

## Bonnes pratiques de structure des paquets

### Point d'entree

Le champ `main` dans package.json specifie le point d'entree :

```json
{
  "main": "src/index.hml"
}
```

Ce fichier doit exporter votre API publique :

```hemlock
// Exporter tout ce dont les utilisateurs ont besoin
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Types
export type { Config, Options } from "./types.hml";
```

### Interne vs public

Gardez les details d'implementation internes prives :

```
src/
├── index.hml          # Public : API exportee
├── parser.hml         # Public : utilise par index.hml
├── formatter.hml      # Public : utilise par index.hml
└── internal/
    ├── helpers.hml    # Prive : usage interne uniquement
    └── constants.hml  # Prive : usage interne uniquement
```

Les utilisateurs importent depuis la racine de votre paquet :

```hemlock
// Bien - importe depuis l'API publique
import { parse, Parser } from "yourusername/my-package";

// Fonctionne aussi - import de sous-chemin
import { validate } from "yourusername/my-package/validator";

// Deconseille - acces aux internes
import { helper } from "yourusername/my-package/internal/helpers";
```

### Exports de sous-chemins

Supportez l'import depuis des sous-chemins :

```
src/
├── index.hml              # Entree principale
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Les utilisateurs peuvent importer :

```hemlock
import { parse } from "yourusername/my-package";           // Principal
import { Parser } from "yourusername/my-package/parser";   // Sous-chemin
import { format } from "yourusername/my-package/formatter";
```

## Dependances

### Ajouter des dependances

```bash
# Dependance d'execution
hpm install hemlang/json

# Dependance de developpement
hpm install hemlang/test-utils --dev
```

### Bonnes pratiques pour les dependances

1. **Utilisez des plages caret** pour la plupart des dependances :
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Epinglez les versions** uniquement si necessaire (instabilite de l'API) :
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Evitez les plages trop restrictives** :
   ```json
   // Mauvais : trop restrictif
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Bon : permet les mises a jour compatibles
   "hemlang/json": "^1.2.3"
   ```

4. **Separez les dependances de developpement** :
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Tester votre paquet

### Ecrire des tests

**test/run.hml :**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Executer les tests

Ajoutez un script de test :

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Executez avec :

```bash
hpm test
```

## Publication

### Prerequis

1. Creez un depot GitHub correspondant au nom de votre paquet
2. Assurez-vous que `package.json` est complet et valide
3. Tous les tests passent

### Processus de publication

Publier consiste simplement a pousser un tag Git :

```bash
# 1. S'assurer que tout est commite
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Creer un tag de version (doit commencer par 'v')
git tag v1.0.0

# 3. Pousser le code et les tags
git push origin main
git push origin v1.0.0
# Ou pousser tous les tags d'un coup
git push origin main --tags
```

### Tags de version

Les tags doivent suivre le format `vX.Y.Z` :

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Patch
git tag v1.1.0      # Mineure
git tag v2.0.0      # Majeure
git tag v1.0.0-beta.1  # Pre-release
```

### Liste de verification avant publication

Avant de publier une nouvelle version :

1. **Mettre a jour la version** dans package.json
2. **Executer les tests** : `hpm test`
3. **Mettre a jour le CHANGELOG** (si vous en avez un)
4. **Mettre a jour le README** si l'API a change
5. **Commiter les modifications**
6. **Creer le tag**
7. **Pousser vers GitHub**

### Exemple automatise

Creez un script de release :

```bash
#!/bin/bash
# release.sh - Publier une nouvelle version

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Executer les tests
hpm test || exit 1

# Mettre a jour la version dans package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Commiter et taguer
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Pousser
git push origin main --tags

echo "Released v$VERSION"
```

## Les utilisateurs installent votre paquet

Apres publication, les utilisateurs peuvent installer :

```bash
# Derniere version
hpm install yourusername/my-package

# Version specifique
hpm install yourusername/my-package@1.0.0

# Contrainte de version
hpm install yourusername/my-package@^1.0.0
```

Et importer :

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Documentation

### README.md

Chaque paquet devrait avoir un README :

```markdown
# my-package

Une breve description de ce que fait ce paquet.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Utilisation

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Analyse la chaine d'entree.

### stringify(obj: any): string

Convertit un objet en chaine.

## Licence

MIT
```

### Documentation de l'API

Documentez tous les exports publics :

```hemlock
/// Analyse la chaine d'entree en un Result structure.
///
/// # Arguments
/// * `input` - La chaine a analyser
///
/// # Retourne
/// Un Result contenant les donnees analysees ou une erreur
///
/// # Exemple
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementation
}
```

## Directives de versionnage

Suivez le [Versionnage semantique](https://semver.org/) :

- **MAJEUR** (1.0.0 -> 2.0.0) : Changements incompatibles
- **MINEUR** (1.0.0 -> 1.1.0) : Nouvelles fonctionnalites, retro-compatibles
- **PATCH** (1.0.0 -> 1.0.1) : Corrections de bugs, retro-compatibles

### Quand incrementer

| Type de changement | Increment de version |
|--------------------|---------------------|
| Changement d'API incompatible | MAJEUR |
| Suppression de fonction/type | MAJEUR |
| Changement de signature de fonction | MAJEUR |
| Ajout d'une nouvelle fonction | MINEUR |
| Ajout d'une nouvelle fonctionnalite | MINEUR |
| Correction de bug | PATCH |
| Mise a jour de documentation | PATCH |
| Refactoring interne | PATCH |

## Voir aussi

- [Specification des paquets](package-spec.md) - Reference complete de package.json
- [Versionnage](versioning.md) - Details du versionnage semantique
- [Configuration](configuration.md) - Authentification GitHub
