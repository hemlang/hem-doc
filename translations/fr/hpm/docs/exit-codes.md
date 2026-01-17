# Codes de sortie

Reference des codes de sortie de hpm et leur signification.

## Tableau des codes de sortie

| Code | Nom | Description |
|------|-----|-------------|
| 0 | SUCCESS | Commande executee avec succes |
| 1 | CONFLICT | Conflit de version de dependance |
| 2 | NOT_FOUND | Paquet non trouve |
| 3 | VERSION_NOT_FOUND | Version demandee non trouvee |
| 4 | NETWORK | Erreur reseau |
| 5 | INVALID_MANIFEST | package.json invalide |
| 6 | INTEGRITY | Echec de la verification d'integrite |
| 7 | RATE_LIMIT | Limite de taux de l'API GitHub depassee |
| 8 | CIRCULAR | Dependance circulaire detectee |

## Descriptions detaillees

### Code de sortie 0 : SUCCESS

La commande s'est executee avec succes.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Code de sortie 1 : CONFLICT

Deux paquets ou plus necessitent des versions incompatibles d'une dependance.

**Exemple :**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Solutions :**
1. Verifiez quels paquets ont le conflit :
   ```bash
   hpm why hemlang/json
   ```
2. Mettez a jour le paquet en conflit :
   ```bash
   hpm update package-a
   ```
3. Assouplissez les contraintes de version dans package.json
4. Supprimez un des paquets en conflit

### Code de sortie 2 : NOT_FOUND

Le paquet specifie n'existe pas sur GitHub.

**Exemple :**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Solutions :**
1. Verifiez l'orthographe du nom du paquet
2. Verifiez si le depot existe : `https://github.com/owner/repo`
3. Verifiez que vous avez acces (pour les depots prives, definissez GITHUB_TOKEN)

### Code de sortie 3 : VERSION_NOT_FOUND

Aucune version ne correspond a la contrainte specifiee.

**Exemple :**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Solutions :**
1. Verifiez les versions disponibles sur les releases/tags GitHub
2. Utilisez une contrainte de version valide
3. Les tags de version doivent commencer par 'v' (ex: `v1.0.0`)

### Code de sortie 4 : NETWORK

Une erreur liee au reseau s'est produite.

**Exemple :**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Solutions :**
1. Verifiez votre connexion internet
2. Verifiez si GitHub est accessible
3. Verifiez les parametres du proxy si vous etes derriere un pare-feu
4. Utilisez `--offline` si les paquets sont en cache :
   ```bash
   hpm install --offline
   ```
5. Attendez et reessayez (hpm reessaie automatiquement)

### Code de sortie 5 : INVALID_MANIFEST

Le fichier package.json est invalide ou malformation.

**Exemple :**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Solutions :**
1. Verifiez la syntaxe JSON (utilisez un validateur JSON)
2. Assurez-vous que les champs obligatoires existent (`name`, `version`)
3. Verifiez les formats des champs :
   - name : format `owner/repo`
   - version : format semver `X.Y.Z`
4. Regenerez :
   ```bash
   rm package.json
   hpm init
   ```

### Code de sortie 6 : INTEGRITY

La verification d'integrite du paquet a echoue.

**Exemple :**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Solutions :**
1. Videz le cache et reinstallez :
   ```bash
   hpm cache clean
   hpm install
   ```
2. Verifiez les problemes reseau (telechargements partiels)
3. Verifiez que le paquet n'a pas ete altere

### Code de sortie 7 : RATE_LIMIT

La limite de taux de l'API GitHub a ete depassee.

**Exemple :**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Solutions :**
1. **S'authentifier avec GitHub** (recommande) :
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Attendre la reinitialisation de la limite de taux (reinitialisation horaire)
3. Utiliser le mode hors ligne si les paquets sont en cache :
   ```bash
   hpm install --offline
   ```

### Code de sortie 8 : CIRCULAR

Dependance circulaire detectee dans le graphe de dependances.

**Exemple :**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**Solutions :**
1. C'est generalement un bug dans les paquets eux-memes
2. Contactez les mainteneurs des paquets
3. Evitez d'utiliser un des paquets circulaires

## Utiliser les codes de sortie dans les scripts

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation reussie"
    ;;
  1)
    echo "Conflit de dependances - verifiez les contraintes de version"
    exit 1
    ;;
  2)
    echo "Paquet non trouve - verifiez le nom du paquet"
    exit 1
    ;;
  4)
    echo "Erreur reseau - verifiez la connexion"
    exit 1
    ;;
  7)
    echo "Limite de taux atteinte - definissez GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Erreur inconnue : $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## Depannage par code de sortie

### Reference rapide

| Code | Premiere chose a verifier |
|------|---------------------------|
| 1 | Executez `hpm why <package>` pour voir le conflit |
| 2 | Verifiez le nom du paquet sur GitHub |
| 3 | Verifiez les versions disponibles sur les tags GitHub |
| 4 | Verifiez la connexion internet |
| 5 | Validez la syntaxe de package.json |
| 6 | Executez `hpm cache clean && hpm install` |
| 7 | Definissez la variable d'environnement `GITHUB_TOKEN` |
| 8 | Contactez les mainteneurs des paquets |

## Voir aussi

- [Depannage](troubleshooting.md) - Solutions detaillees
- [Commandes](commands.md) - Reference des commandes
- [Configuration](configuration.md) - Configuration du token GitHub
