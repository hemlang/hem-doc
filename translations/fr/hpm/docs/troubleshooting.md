# Depannage

Solutions aux problemes courants de hpm.

## Problemes d'installation

### "hemlock: command not found"

**Cause :** Hemlock n'est pas installe ou n'est pas dans le PATH.

**Solution :**

```bash
# Verifier si hemlock existe
which hemlock

# Si non trouve, installer d'abord Hemlock
# Visitez : https://github.com/hemlang/hemlock

# Apres l'installation, verifier
hemlock --version
```

### "hpm: command not found"

**Cause :** hpm n'est pas installe ou n'est pas dans le PATH.

**Solution :**

```bash
# Verifier ou hpm est installe
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Si utilisation d'un emplacement personnalise, ajouter au PATH
export PATH="$HOME/.local/bin:$PATH"

# Ajouter a ~/.bashrc ou ~/.zshrc pour la persistance
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Reinstaller si necessaire
cd /path/to/hpm
sudo make install
```

### "Permission denied" pendant l'installation

**Cause :** Pas de permission d'ecriture dans le repertoire d'installation.

**Solution :**

```bash
# Option 1 : Utiliser sudo pour une installation systeme
sudo make install

# Option 2 : Installer dans le repertoire utilisateur (sans sudo)
make install PREFIX=$HOME/.local
```

## Problemes de dependances

### "Package not found" (code de sortie 2)

**Cause :** Le paquet n'existe pas sur GitHub.

**Solution :**

```bash
# Verifier que le paquet existe
# Verifiez : https://github.com/owner/repo

# Verifier l'orthographe
hpm install hemlang/sprout  # Correct
hpm install hemlan/sprout   # Mauvais proprietaire
hpm install hemlang/spout   # Mauvais depot

# Verifier les fautes de frappe dans package.json
cat package.json | grep -A 5 dependencies
```

### "Version not found" (code de sortie 3)

**Cause :** Aucune release ne correspond a la contrainte de version.

**Solution :**

```bash
# Lister les versions disponibles (verifier les releases/tags GitHub)
# Les tags doivent commencer par 'v' (ex: v1.0.0)

# Utiliser une contrainte de version valide
hpm install owner/repo@^1.0.0

# Essayer la derniere version
hpm install owner/repo

# Verifier les tags disponibles sur GitHub
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (code de sortie 1)

**Cause :** Deux paquets necessitent des versions incompatibles d'une dependance.

**Solution :**

```bash
# Voir le conflit
hpm install --verbose

# Verifier ce qui necessite la dependance
hpm why conflicting/package

# Solutions :
# 1. Mettre a jour le paquet en conflit
hpm update problem/package

# 2. Modifier les contraintes de version dans package.json
# Editer pour permettre des versions compatibles

# 3. Supprimer un des paquets en conflit
hpm uninstall one/package
```

### "Circular dependency" (code de sortie 8)

**Cause :** Le paquet A depend de B, qui depend de A.

**Solution :**

```bash
# Identifier le cycle
hpm install --verbose

# C'est generalement un bug dans les paquets
# Contacter les mainteneurs des paquets

# Solution de contournement : eviter un des paquets
```

## Problemes reseau

### "Network error" (code de sortie 4)

**Cause :** Impossible de se connecter a l'API GitHub.

**Solution :**

```bash
# Verifier la connexion internet
ping github.com

# Verifier si l'API GitHub est accessible
curl -I https://api.github.com

# Reessayer (hpm reessaie automatiquement)
hpm install

# Utiliser le mode hors ligne si les paquets sont en cache
hpm install --offline

# Verifier les parametres du proxy si derriere un pare-feu
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (code de sortie 7)

**Cause :** Trop de requetes API sans authentification.

**Solution :**

```bash
# Option 1 : S'authentifier avec un token GitHub (recommande)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Creer un token : GitHub > Settings > Developer settings > Personal access tokens

# Option 2 : Enregistrer le token dans le fichier de configuration
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Option 3 : Attendre la reinitialisation de la limite (reinitialisation horaire)

# Option 4 : Utiliser le mode hors ligne
hpm install --offline
```

### Timeout de connexion

**Cause :** Reseau lent ou problemes de l'API GitHub.

**Solution :**

```bash
# hpm reessaie automatiquement avec un backoff exponentiel

# Verifier si GitHub a des problemes
# Visitez : https://www.githubstatus.com

# Reessayer plus tard
hpm install

# Utiliser les paquets en cache
hpm install --offline
```

## Problemes de package.json

### "Invalid package.json" (code de sortie 5)

**Cause :** Malformation ou champs obligatoires manquants.

**Solution :**

```bash
# Valider la syntaxe JSON
cat package.json | python -m json.tool

# Verifier les champs obligatoires
cat package.json

# Champs obligatoires :
# - "name" : format owner/repo
# - "version" : format X.Y.Z

# Regenerer si necessaire
rm package.json
hpm init
```

### Erreur de format "name"

**Cause :** Le nom du paquet n'est pas au format `owner/repo`.

**Solution :**

```json
// Incorrect
{
  "name": "my-package"
}

// Correct
{
  "name": "yourusername/my-package"
}
```

### Erreur de format "version"

**Cause :** La version n'est pas au format semver.

**Solution :**

```json
// Incorrect
{
  "version": "1.0"
}

// Correct
{
  "version": "1.0.0"
}
```

## Problemes de fichier de verrouillage

### Fichier de verrouillage desynchronise

**Cause :** package.json modifie sans executer install.

**Solution :**

```bash
# Regenerer le fichier de verrouillage
rm package-lock.json
hpm install
```

### Fichier de verrouillage corrompu

**Cause :** JSON invalide ou modifications manuelles.

**Solution :**

```bash
# Verifier la validite JSON
cat package-lock.json | python -m json.tool

# Regenerer
rm package-lock.json
hpm install
```

## Problemes de hem_modules

### Les paquets ne s'installent pas

**Cause :** Divers problemes possibles.

**Solution :**

```bash
# Nettoyer et reinstaller
rm -rf hem_modules
hpm install

# Verifier la sortie verbeuse
hpm install --verbose
```

### L'import ne fonctionne pas

**Cause :** Paquet pas correctement installe ou mauvais chemin d'import.

**Solution :**

```bash
# Verifier que le paquet est installe
ls hem_modules/owner/repo/

# Verifier le champ main de package.json
cat hem_modules/owner/repo/package.json

# Format d'import correct
import { x } from "owner/repo";          # Utilise l'entree main
import { y } from "owner/repo/subpath";  # Import de sous-chemin
```

### Erreur "Module not found"

**Cause :** Le chemin d'import ne correspond pas a un fichier.

**Solution :**

```bash
# Verifier le chemin d'import
ls hem_modules/owner/repo/src/

# Verifier index.hml
ls hem_modules/owner/repo/src/index.hml

# Verifier le champ main dans package.json
cat hem_modules/owner/repo/package.json | grep main
```

## Problemes de cache

### Le cache prend trop d'espace

**Solution :**

```bash
# Voir la taille du cache
hpm cache list

# Vider le cache
hpm cache clean
```

### Permissions du cache

**Solution :**

```bash
# Corriger les permissions
chmod -R u+rw ~/.hpm/cache

# Ou supprimer et reinstaller
rm -rf ~/.hpm/cache
hpm install
```

### Utilisation du mauvais cache

**Solution :**

```bash
# Verifier l'emplacement du cache
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Effacer la variable d'environnement si incorrecte
unset HPM_CACHE_DIR
```

## Problemes de scripts

### "Script not found"

**Cause :** Le nom du script n'existe pas dans package.json.

**Solution :**

```bash
# Lister les scripts disponibles
cat package.json | grep -A 20 scripts

# Verifier l'orthographe
hpm run test    # Correct
hpm run tests   # Incorrect si le script s'appelle "test"
```

### Le script echoue

**Cause :** Erreur dans la commande du script.

**Solution :**

```bash
# Executer la commande directement pour voir l'erreur
hemlock test/run.hml

# Verifier la definition du script
cat package.json | grep test
```

## Debogage

### Activer la sortie verbeuse

```bash
hpm install --verbose
```

### Verifier la version de hpm

```bash
hpm --version
```

### Verifier la version de hemlock

```bash
hemlock --version
```

### Simulation (dry run)

Apercu sans effectuer de modifications :

```bash
hpm install --dry-run
```

### Repartir de zero

Commencer proprement :

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Obtenir de l'aide

### Aide des commandes

```bash
hpm --help
hpm install --help
```

### Signaler des problemes

Si vous rencontrez un bug :

1. Verifiez les issues existantes : https://github.com/hemlang/hpm/issues
2. Creez une nouvelle issue avec :
   - Version de hpm (`hpm --version`)
   - Version de Hemlock (`hemlock --version`)
   - Systeme d'exploitation
   - Etapes pour reproduire
   - Message d'erreur (utilisez `--verbose`)

## Reference des codes de sortie

| Code | Signification | Solution courante |
|------|---------------|-------------------|
| 0 | Succes | - |
| 1 | Conflit de dependances | Mettre a jour ou changer les contraintes |
| 2 | Paquet non trouve | Verifier l'orthographe, verifier que le depot existe |
| 3 | Version non trouvee | Verifier les versions disponibles sur GitHub |
| 4 | Erreur reseau | Verifier la connexion, reessayer |
| 5 | package.json invalide | Corriger la syntaxe JSON et les champs obligatoires |
| 6 | Echec de verification d'integrite | Vider le cache, reinstaller |
| 7 | Limite de taux GitHub | Ajouter GITHUB_TOKEN |
| 8 | Dependance circulaire | Contacter les mainteneurs des paquets |

## Voir aussi

- [Installation](installation.md) - Guide d'installation
- [Configuration](configuration.md) - Options de configuration
- [Commandes](commands.md) - Reference des commandes
