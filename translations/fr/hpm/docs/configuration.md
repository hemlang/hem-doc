# Configuration

Ce guide couvre toutes les options de configuration de hpm.

## Apercu

hpm peut etre configure via :

1. **Variables d'environnement** - Pour les parametres d'execution
2. **Fichier de configuration global** - `~/.hpm/config.json`
3. **Fichiers de projet** - `package.json` et `package-lock.json`

## Variables d'environnement

### GITHUB_TOKEN

Token API GitHub pour l'authentification.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Avantages de l'authentification :**
- Limites de taux API plus elevees (5000 contre 60 requetes/heure)
- Acces aux depots prives
- Resolution des dependances plus rapide

**Creer un token :**

1. Allez dans GitHub > Settings > Developer settings > Personal access tokens
2. Cliquez sur "Generate new token (classic)"
3. Selectionnez les portees :
   - `repo` - Pour l'acces aux depots prives
   - `read:packages` - Pour GitHub Packages (si utilise)
4. Generez et copiez le token

### HPM_CACHE_DIR

Remplacer le repertoire de cache par defaut.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

Defaut : `~/.hpm/cache`

**Cas d'utilisation :**
- Systemes CI/CD avec des emplacements de cache personnalises
- Cache partage entre plusieurs projets
- Cache temporaire pour des builds isoles

### HOME

Repertoire personnel de l'utilisateur. Utilise pour localiser :
- Repertoire de configuration : `$HOME/.hpm/`
- Repertoire de cache : `$HOME/.hpm/cache/`

Generalement defini par le systeme ; remplacez uniquement si necessaire.

### Exemple .bashrc / .zshrc

```bash
# Authentification GitHub (recommande)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Emplacement de cache personnalise (optionnel)
# export HPM_CACHE_DIR=/path/to/cache

# Ajouter hpm au PATH (si utilisation d'un emplacement d'installation personnalise)
export PATH="$HOME/.local/bin:$PATH"
```

## Fichier de configuration global

### Emplacement

`~/.hpm/config.json`

### Format

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Creer le fichier de configuration

```bash
# Creer le repertoire de configuration
mkdir -p ~/.hpm

# Creer le fichier de configuration
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Securiser le fichier (recommande)
chmod 600 ~/.hpm/config.json
```

### Priorite des tokens

Si les deux sont definis, la variable d'environnement a la priorite :

1. Variable d'environnement `GITHUB_TOKEN` (la plus haute)
2. Champ `github_token` de `~/.hpm/config.json`
3. Pas d'authentification (par defaut)

## Structure des repertoires

### Repertoires globaux

```
~/.hpm/
├── config.json          # Configuration globale
└── cache/               # Cache des paquets
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Repertoires de projet

```
my-project/
├── package.json         # Manifeste du projet
├── package-lock.json    # Fichier de verrouillage des dependances
├── hem_modules/         # Paquets installes
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Code source
└── test/                # Tests
```

## Cache des paquets

### Emplacement

Defaut : `~/.hpm/cache/`

Remplacer avec : variable d'environnement `HPM_CACHE_DIR`

### Structure

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Gestion du cache

```bash
# Voir les paquets en cache
hpm cache list

# Vider tout le cache
hpm cache clean
```

### Comportement du cache

- Les paquets sont mis en cache apres le premier telechargement
- Les installations suivantes utilisent les versions en cache
- Utilisez `--offline` pour installer uniquement depuis le cache
- Le cache est partage entre tous les projets

## Limites de taux de l'API GitHub

### Sans authentification

- **60 requetes par heure** par adresse IP
- Partage entre tous les utilisateurs non authentifies sur la meme IP
- Rapidement epuise en CI/CD ou avec beaucoup de dependances

### Avec authentification

- **5000 requetes par heure** par utilisateur authentifie
- Limite de taux personnelle, non partagee

### Gestion des limites de taux

hpm automatiquement :
- Reessaie avec un backoff exponentiel (1s, 2s, 4s, 8s)
- Signale les erreurs de limite de taux avec le code de sortie 7
- Suggere l'authentification en cas de limitation

**Solutions en cas de limitation :**

```bash
# Option 1 : S'authentifier avec un token GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Option 2 : Attendre la reinitialisation de la limite de taux
# (Les limites se reinitialisent toutes les heures)

# Option 3 : Utiliser le mode hors ligne (si les paquets sont en cache)
hpm install --offline
```

## Mode hors ligne

Installer des paquets sans acces reseau :

```bash
hpm install --offline
```

**Exigences :**
- Tous les paquets doivent etre dans le cache
- Le fichier de verrouillage doit exister avec les versions exactes

**Cas d'utilisation :**
- Environnements air-gap
- Builds CI/CD plus rapides (avec cache prechauff)
- Eviter les limites de taux

## Configuration CI/CD

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Installer Hemlock (ajuster selon votre configuration)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile :**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copier d'abord les fichiers de paquet (pour le cache des couches)
COPY package.json package-lock.json ./

# Installer les dependances
RUN hpm install

# Copier le code source
COPY . .

# Executer l'application
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml :**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Configuration du proxy

Pour les environnements derriere un proxy, configurez au niveau du systeme :

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Bonnes pratiques de securite

### Securite des tokens

1. **Ne commitez jamais les tokens** dans le controle de version
2. **Utilisez des variables d'environnement** en CI/CD
3. **Limitez les portees des tokens** au minimum requis
4. **Faites tourner les tokens** regulierement
5. **Securisez le fichier de configuration** :
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Depots prives

Pour acceder aux paquets prives :

1. Creez un token avec la portee `repo`
2. Configurez l'authentification (variable d'environnement ou fichier de configuration)
3. Assurez-vous que le token a acces au depot

```bash
# Tester l'acces
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Depannage de la configuration

### Verifier la configuration

```bash
# Verifier si le token est defini
echo $GITHUB_TOKEN | head -c 10

# Verifier le fichier de configuration
cat ~/.hpm/config.json

# Verifier le repertoire de cache
ls -la ~/.hpm/cache/

# Tester avec une sortie verbeuse
hpm install --verbose
```

### Problemes courants

**"GitHub rate limit exceeded"**
- Configurez l'authentification avec `GITHUB_TOKEN`
- Attendez la reinitialisation de la limite de taux
- Utilisez `--offline` si les paquets sont en cache

**"Permission denied" sur le cache**
```bash
# Corriger les permissions du cache
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Creer le repertoire de configuration
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## Voir aussi

- [Installation](installation.md) - Installer hpm
- [Depannage](troubleshooting.md) - Problemes courants
- [Commandes](commands.md) - Reference des commandes
