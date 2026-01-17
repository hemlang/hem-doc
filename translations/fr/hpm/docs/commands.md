# Reference des commandes

Reference complete de toutes les commandes hpm.

## Options globales

Ces options fonctionnent avec toutes les commandes :

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Afficher le message d'aide |
| `--version`, `-v` | Afficher la version de hpm |
| `--verbose` | Afficher une sortie detaillee |

## Commandes

### hpm init

Creer un nouveau fichier `package.json`.

```bash
hpm init        # Mode interactif
hpm init --yes  # Accepter toutes les valeurs par defaut
hpm init -y     # Forme courte
```

**Options :**

| Option | Description |
|--------|-------------|
| `--yes`, `-y` | Accepter les valeurs par defaut pour toutes les invites |

**Invites interactives :**
- Nom du paquet (format owner/repo)
- Version (defaut : 1.0.0)
- Description
- Auteur
- Licence (defaut : MIT)
- Fichier principal (defaut : src/index.hml)

**Exemple :**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Installer des dependances ou ajouter de nouveaux paquets.

```bash
hpm install                           # Installer tout depuis package.json
hpm install owner/repo                # Ajouter et installer un paquet
hpm install owner/repo@^1.0.0        # Avec contrainte de version
hpm install owner/repo --dev         # Comme dependance de developpement
hpm i owner/repo                      # Forme courte
```

**Options :**

| Option | Description |
|--------|-------------|
| `--dev`, `-D` | Ajouter aux devDependencies |
| `--verbose` | Afficher la progression detaillee |
| `--dry-run` | Apercu sans installer |
| `--offline` | Installer depuis le cache uniquement (sans reseau) |
| `--parallel` | Activer les telechargements paralleles (experimental) |

**Syntaxe des contraintes de version :**

| Syntaxe | Exemple | Signification |
|---------|---------|---------------|
| (aucune) | `owner/repo` | Derniere version |
| Exacte | `owner/repo@1.2.3` | Exactement 1.2.3 |
| Caret | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Plage | `owner/repo@>=1.0.0` | Au moins 1.0.0 |

**Exemples :**

```bash
# Installer toutes les dependances
hpm install

# Installer un paquet specifique
hpm install hemlang/json

# Installer avec contrainte de version
hpm install hemlang/sprout@^2.0.0

# Installer comme dependance de developpement
hpm install hemlang/test-utils --dev

# Apercu de ce qui serait installe
hpm install hemlang/sprout --dry-run

# Sortie verbeuse
hpm install --verbose

# Installer depuis le cache uniquement (hors ligne)
hpm install --offline
```

**Sortie :**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Supprimer un paquet.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Forme courte
hpm remove owner/repo      # Alternative
```

**Exemples :**

```bash
hpm uninstall hemlang/sprout
```

**Sortie :**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Mettre a jour les paquets vers les dernieres versions dans les contraintes.

```bash
hpm update              # Mettre a jour tous les paquets
hpm update owner/repo   # Mettre a jour un paquet specifique
hpm up owner/repo       # Forme courte
```

**Options :**

| Option | Description |
|--------|-------------|
| `--verbose` | Afficher la progression detaillee |
| `--dry-run` | Apercu sans mettre a jour |

**Exemples :**

```bash
# Mettre a jour tous les paquets
hpm update

# Mettre a jour un paquet specifique
hpm update hemlang/sprout

# Apercu des mises a jour
hpm update --dry-run
```

**Sortie :**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Afficher les paquets installes.

```bash
hpm list              # Afficher l'arbre complet des dependances
hpm list --depth=0    # Dependances directes uniquement
hpm list --depth=1    # Un niveau de dependances transitives
hpm ls                # Forme courte
```

**Options :**

| Option | Description |
|--------|-------------|
| `--depth=N` | Limiter la profondeur de l'arbre (defaut : tout) |

**Exemples :**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Afficher les paquets avec des versions plus recentes disponibles.

```bash
hpm outdated
```

**Sortie :**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current** : Version installee
- **Wanted** : Version la plus elevee correspondant a la contrainte
- **Latest** : Derniere version disponible

---

### hpm run

Executer un script depuis package.json.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Exemples :**

Avec ce package.json :

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Executer des scripts :

```bash
hpm run start
hpm run test
hpm run build

# Passer des arguments au script
hpm run test -- --verbose
```

---

### hpm test

Raccourci pour `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Equivalent a :

```bash
hpm run test
```

---

### hpm why

Expliquer pourquoi un paquet est installe (afficher la chaine de dependances).

```bash
hpm why owner/repo
```

**Exemple :**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Gerer le cache global des paquets.

```bash
hpm cache list    # Lister les paquets en cache
hpm cache clean   # Vider tous les paquets en cache
```

**Sous-commandes :**

| Sous-commande | Description |
|---------------|-------------|
| `list` | Afficher tous les paquets en cache et leurs tailles |
| `clean` | Supprimer tous les paquets en cache |

**Exemples :**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Raccourcis de commandes

Pour plus de commodite, plusieurs commandes ont des alias courts :

| Commande | Raccourcis |
|----------|------------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Exemples :**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Codes de sortie

hpm utilise des codes de sortie specifiques pour indiquer differentes conditions d'erreur :

| Code | Signification |
|------|---------------|
| 0 | Succes |
| 1 | Conflit de dependances |
| 2 | Paquet non trouve |
| 3 | Version non trouvee |
| 4 | Erreur reseau |
| 5 | package.json invalide |
| 6 | Echec de la verification d'integrite |
| 7 | Limite de taux GitHub depassee |
| 8 | Dependance circulaire |

Utilisez les codes de sortie dans les scripts :

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## Variables d'environnement

hpm respecte ces variables d'environnement :

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | Token API GitHub pour l'authentification |
| `HPM_CACHE_DIR` | Remplacer l'emplacement du repertoire de cache |
| `HOME` | Repertoire personnel de l'utilisateur (pour config/cache) |

**Exemples :**

```bash
# Utiliser un token GitHub pour des limites de taux plus elevees
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Utiliser un repertoire de cache personnalise
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## Voir aussi

- [Configuration](configuration.md) - Fichiers de configuration
- [Specification des paquets](package-spec.md) - Format package.json
- [Depannage](troubleshooting.md) - Problemes courants
