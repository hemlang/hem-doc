# Documentation hpm

Bienvenue dans la documentation de hpm (Hemlock Package Manager). hpm est le gestionnaire de paquets officiel pour le langage de programmation [Hemlock](https://github.com/hemlang/hemlock).

## Vue d'ensemble

hpm utilise GitHub comme registre de paquets, ou les paquets sont identifies par leur chemin de depot GitHub (par exemple, `hemlang/sprout`). Cela signifie :

- **Pas de registre central** - les paquets vivent dans les depots GitHub
- **Tags de version** - les versions sont des tags Git (par exemple, `v1.0.0`)
- **Publier c'est juste git** - poussez un tag pour publier une nouvelle version

## Documentation

### Pour commencer

- [Installation](installation.md) - Comment installer hpm
- [Demarrage rapide](quick-start.md) - Etre operationnel en 5 minutes
- [Configuration de projet](project-setup.md) - Configurer un nouveau projet Hemlock

### Guide utilisateur

- [Reference des commandes](commands.md) - Reference complete pour toutes les commandes hpm
- [Configuration](configuration.md) - Fichiers de configuration et variables d'environnement
- [Depannage](troubleshooting.md) - Problemes courants et solutions

### Developpement de paquets

- [Creer des paquets](creating-packages.md) - Comment creer et publier des paquets
- [Specification de paquet](package-spec.md) - Le format package.json
- [Versionnage](versioning.md) - Versionnage semantique et contraintes de version

### Reference

- [Architecture](architecture.md) - Architecture interne et conception
- [Codes de sortie](exit-codes.md) - Reference des codes de sortie CLI

## Reference rapide

### Commandes de base

```bash
hpm init                              # Creer un nouveau package.json
hpm install                           # Installer toutes les dependances
hpm install owner/repo                # Ajouter et installer un paquet
hpm install owner/repo@^1.0.0        # Installer avec contrainte de version
hpm uninstall owner/repo              # Supprimer un paquet
hpm update                            # Mettre a jour tous les paquets
hpm list                              # Afficher les paquets installes
hpm run <script>                      # Executer un script de paquet
```

### Identification des paquets

Les paquets utilisent le format GitHub `owner/repo` :

```
hemlang/sprout          # Framework web
hemlang/json            # Utilitaires JSON
alice/http-client       # Bibliotheque client HTTP
```

### Contraintes de version

| Syntaxe | Signification |
|---------|---------------|
| `1.0.0` | Version exacte |
| `^1.2.3` | Compatible (>=1.2.3 <2.0.0) |
| `~1.2.3` | Mises a jour de correctif (>=1.2.3 <1.3.0) |
| `>=1.0.0` | Au moins 1.0.0 |
| `*` | N'importe quelle version |

## Obtenir de l'aide

- Utilisez `hpm --help` pour l'aide en ligne de commande
- Utilisez `hpm <commande> --help` pour l'aide specifique a une commande
- Signalez les problemes sur [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## Licence

hpm est distribue sous la licence MIT.
