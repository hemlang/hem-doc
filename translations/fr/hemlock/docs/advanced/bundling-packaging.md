# Empaquetage et distribution

Hemlock fournit des outils integres pour regrouper des projets multi-fichiers en fichiers distribuables uniques et creer des executables autonomes.

## Vue d'ensemble

| Commande | Sortie | Cas d'utilisation |
|----------|--------|-------------------|
| `--bundle` | `.hmlc` ou `.hmlb` | Distribuer du bytecode (necessite Hemlock pour executer) |
| `--package` | Executable | Binaire autonome (sans dependances) |
| `--compile` | `.hmlc` | Compiler un fichier unique (pas de resolution des imports) |

## Regroupement (Bundling)

Le bundler resout toutes les instructions `import` depuis un point d'entree et les aplatit en un seul fichier.

### Utilisation de base

```bash
# Regrouper app.hml et tous ses imports dans app.hmlc
hemlock --bundle app.hml

# Specifier le chemin de sortie
hemlock --bundle app.hml -o dist/app.hmlc

# Creer un bundle compresse (.hmlb) - taille de fichier plus petite
hemlock --bundle app.hml --compress -o app.hmlb

# Sortie verbeuse (montre les modules resolus)
hemlock --bundle app.hml --verbose
```

### Formats de sortie

**`.hmlc` (Non compresse)**
- Format AST serialise
- Rapide a charger et executer
- Format de sortie par defaut

**`.hmlb` (Compresse)**
- `.hmlc` compresse avec zlib
- Taille de fichier plus petite (reduction typique de 50-70%)
- Demarrage legerement plus lent du a la decompression

### Executer des fichiers regroupes

```bash
# Executer un bundle non compresse
hemlock app.hmlc

# Executer un bundle compresse
hemlock app.hmlb

# Passer des arguments
hemlock app.hmlc arg1 arg2
```

### Exemple : Projet multi-modules

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # S'execute avec toutes les dependances incluses
```

### Imports stdlib

Le bundler resout automatiquement les imports `@stdlib/` :

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

Quand ils sont regroupes, les modules stdlib sont inclus dans la sortie.

## Empaquetage (Packaging)

L'empaquetage cree un executable autonome en integrant le bytecode regroupe dans une copie de l'interpreteur Hemlock.

### Utilisation de base

```bash
# Creer un executable depuis app.hml
hemlock --package app.hml

# Specifier le nom de sortie
hemlock --package app.hml -o myapp

# Ignorer la compression (demarrage plus rapide, fichier plus gros)
hemlock --package app.hml --no-compress

# Sortie verbeuse
hemlock --package app.hml --verbose
```

### Executer des executables empaquetes

```bash
# L'executable empaquete s'execute directement
./myapp

# Les arguments sont passes au script
./myapp arg1 arg2
```

### Format de package

Les executables empaquetes utilisent le format HMLP :

```
[binaire hemlock][payload HMLB/HMLC][payload_size:u64][magic HMLP:u32]
```

Quand un executable empaquete s'execute :
1. Il verifie s'il y a un payload integre a la fin du fichier
2. S'il est trouve, il decompresse et execute le payload
3. S'il n'est pas trouve, il se comporte comme un interpreteur Hemlock normal

### Options de compression

| Drapeau | Format | Demarrage | Taille |
|---------|--------|-----------|--------|
| (defaut) | HMLB | Normal | Plus petit |
| `--no-compress` | HMLC | Plus rapide | Plus grand |

Pour les outils CLI ou le temps de demarrage compte, utilisez `--no-compress`.

## Inspecter les bundles

Utilisez `--info` pour inspecter les fichiers regroupes ou compiles :

```bash
hemlock --info app.hmlc
```

Sortie :
```
=== Info fichier : app.hmlc ===
Taille : 12847 octets
Format : HMLC (AST compile)
Version : 1
Drapeaux : 0x0001 [DEBUG]
Chaines : 42
Instructions : 156
```

```bash
hemlock --info app.hmlb
```

Sortie :
```
=== Info fichier : app.hmlb ===
Taille : 5234 octets
Format : HMLB (bundle compresse)
Version : 1
Non compresse : 12847 octets
Compresse : 5224 octets
Ratio : reduction de 59.3%
```

## Compilation native

Pour de vrais executables natifs (pas d'interpreteur), utilisez le compilateur Hemlock :

```bash
# Compiler en executable natif via C
hemlockc app.hml -o app

# Garder le code C genere
hemlockc app.hml -o app --keep-c

# Emettre uniquement le C (ne pas compiler)
hemlockc app.hml -c -o app.c

# Niveau d'optimisation
hemlockc app.hml -o app -O2
```

Le compilateur genere du code C et invoque GCC pour produire un binaire natif. Cela necessite :
- La bibliotheque runtime Hemlock (`libhemlock_runtime`)
- Un compilateur C (GCC par defaut)

### Options du compilateur

| Option | Description |
|--------|-------------|
| `-o <fichier>` | Nom de l'executable de sortie |
| `-c` | Emettre uniquement le code C |
| `--emit-c <fichier>` | Ecrire le C dans le fichier specifie |
| `-k, --keep-c` | Garder le C genere apres compilation |
| `-O<niveau>` | Niveau d'optimisation (0-3) |
| `--cc <chemin>` | Compilateur C a utiliser |
| `--runtime <chemin>` | Chemin vers la bibliotheque runtime |
| `-v, --verbose` | Sortie verbeuse |

## Comparaison

| Approche | Portabilite | Demarrage | Taille | Dependances |
|----------|-------------|-----------|--------|-------------|
| `.hml` | Source uniquement | Temps d'analyse | Plus petit | Hemlock |
| `.hmlc` | Hemlock uniquement | Rapide | Petit | Hemlock |
| `.hmlb` | Hemlock uniquement | Rapide | Plus petit | Hemlock |
| `--package` | Autonome | Rapide | Plus grand | Aucune |
| `hemlockc` | Natif | Plus rapide | Variable | Libs runtime |

## Bonnes pratiques

1. **Developpement** : Executez les fichiers `.hml` directement pour une iteration rapide
2. **Distribution (avec Hemlock)** : Regroupez avec `--compress` pour des fichiers plus petits
3. **Distribution (autonome)** : Empaquetez pour un deploiement sans dependances
4. **Performance critique** : Utilisez `hemlockc` pour la compilation native

## Depannage

### "Cannot find stdlib" (Impossible de trouver la stdlib)

Le bundler cherche la stdlib dans :
1. `./stdlib` (relatif a l'executable)
2. `../stdlib` (relatif a l'executable)
3. `/usr/local/lib/hemlock/stdlib`

Assurez-vous que Hemlock est correctement installe ou executez depuis le repertoire source.

### Dependances circulaires

```
Erreur : Dependance circulaire detectee lors du chargement de 'path/to/module.hml'
```

Refactorisez vos imports pour casser le cycle. Considerez l'utilisation d'un module partage pour les types communs.

### Grande taille de package

- Utilisez la compression par defaut (n'utilisez pas `--no-compress`)
- La taille empaquetee inclut l'interpreteur complet (~500Ko-1Mo de base)
- Pour une taille minimale, utilisez `hemlockc` pour la compilation native
