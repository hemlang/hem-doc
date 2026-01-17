# Installation

Ce guide explique comment installer hpm sur votre systeme.

## Installation rapide (recommandee)

Installez la derniere version avec une seule commande :

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Cela effectue automatiquement :
- La detection de votre systeme d'exploitation (Linux, macOS)
- La detection de votre architecture (x86_64, arm64)
- Le telechargement du binaire precompile approprie
- L'installation dans `/usr/local/bin` (ou utilise sudo si necessaire)

### Options d'installation

```bash
# Installer dans un emplacement personnalise (sans sudo)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Installer une version specifique
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Combiner les options
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Plateformes supportees

| Plateforme | Architecture | Statut |
|------------|--------------|--------|
| Linux    | x86_64       | Supportee |
| macOS    | x86_64       | Supportee |
| macOS    | arm64 (M1/M2/M3) | Supportee |
| Linux    | arm64        | Compiler depuis les sources |

## Compilation depuis les sources

Si vous preferez compiler depuis les sources ou si vous avez besoin d'une plateforme non couverte par les binaires precompiles, suivez ces instructions.

### Prerequis

hpm necessite que [Hemlock](https://github.com/hemlang/hemlock) soit installe au prealable. Suivez les instructions d'installation de Hemlock avant de continuer.

Verifiez que Hemlock est installe :

```bash
hemlock --version
```

## Methodes d'installation

### Methode 1 : Make Install

Compiler depuis les sources et installer.

```bash
# Cloner le depot
git clone https://github.com/hemlang/hpm.git
cd hpm

# Installer dans /usr/local/bin (necessite sudo)
sudo make install
```

Apres l'installation, verifiez que cela fonctionne :

```bash
hpm --version
```

### Methode 2 : Emplacement personnalise

Installer dans un repertoire personnalise (sans sudo) :

```bash
# Cloner le depot
git clone https://github.com/hemlang/hpm.git
cd hpm

# Installer dans ~/.local/bin
make install PREFIX=$HOME/.local

# Ou tout autre emplacement personnalise
make install PREFIX=/opt/hemlock
```

Assurez-vous que votre repertoire bin personnalise est dans votre PATH :

```bash
# Ajouter a ~/.bashrc ou ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Methode 3 : Executer sans installer

Vous pouvez executer hpm directement sans l'installer :

```bash
# Cloner le depot
git clone https://github.com/hemlang/hpm.git
cd hpm

# Creer le script wrapper local
make

# Executer depuis le repertoire hpm
./hpm --help

# Ou executer via hemlock directement
hemlock src/main.hml --help
```

### Methode 4 : Installation manuelle

Creez votre propre script wrapper :

```bash
# Cloner dans un emplacement permanent
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Creer le script wrapper
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Variables d'installation

Le Makefile supporte ces variables :

| Variable | Valeur par defaut | Description |
|----------|-------------------|-------------|
| `PREFIX` | `/usr/local` | Prefixe d'installation |
| `BINDIR` | `$(PREFIX)/bin` | Repertoire des binaires |
| `HEMLOCK` | `hemlock` | Chemin vers l'interpreteur hemlock |

Exemple avec des variables personnalisees :

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Fonctionnement

L'installateur cree un script shell wrapper qui invoque l'interpreteur Hemlock avec le code source de hpm :

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

Cette approche :
- Ne necessite aucune compilation
- Execute toujours le dernier code source
- Fonctionne de maniere fiable sur toutes les plateformes

## Mise a jour de hpm

Pour mettre a jour hpm vers la derniere version :

```bash
cd /path/to/hpm
git pull origin main

# Reinstaller si le chemin a change
sudo make install
```

## Desinstallation

Supprimer hpm de votre systeme :

```bash
cd /path/to/hpm
sudo make uninstall
```

Ou supprimer manuellement :

```bash
sudo rm /usr/local/bin/hpm
```

## Verification de l'installation

Apres l'installation, verifiez que tout fonctionne :

```bash
# Verifier la version
hpm --version

# Afficher l'aide
hpm --help

# Tester l'initialisation (dans un repertoire vide)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Depannage

### "hemlock: command not found"

Hemlock n'est pas installe ou n'est pas dans votre PATH. Installez d'abord Hemlock :

```bash
# Verifier si hemlock existe
which hemlock

# Si non trouve, installer Hemlock depuis https://github.com/hemlang/hemlock
```

### "Permission denied"

Utilisez sudo pour une installation systeme, ou installez dans un repertoire utilisateur :

```bash
# Option 1 : Utiliser sudo
sudo make install

# Option 2 : Installer dans le repertoire utilisateur
make install PREFIX=$HOME/.local
```

### "hpm: command not found" apres l'installation

Votre PATH peut ne pas inclure le repertoire d'installation :

```bash
# Verifier ou hpm a ete installe
ls -la /usr/local/bin/hpm

# Ajouter au PATH si utilisation d'un emplacement personnalise
export PATH="$HOME/.local/bin:$PATH"
```

## Notes specifiques aux plateformes

### Linux

L'installation standard fonctionne sur toutes les distributions Linux. Certaines distributions peuvent necessiter :

```bash
# Debian/Ubuntu : S'assurer que les outils de compilation sont installes
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

L'installation standard fonctionne. Si vous utilisez Homebrew :

```bash
# S'assurer que les outils en ligne de commande Xcode sont installes
xcode-select --install
```

### Windows (WSL)

hpm fonctionne dans le Sous-systeme Windows pour Linux :

```bash
# Dans le terminal WSL
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Prochaines etapes

Apres l'installation :

1. [Demarrage rapide](quick-start.md) - Creez votre premier projet
2. [Reference des commandes](commands.md) - Apprenez toutes les commandes
3. [Configuration](configuration.md) - Configurez hpm
