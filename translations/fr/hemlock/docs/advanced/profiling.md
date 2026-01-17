# Profilage

Hemlock inclut un profiler integre pour l'**analyse du temps CPU**, le **suivi memoire** et la **detection de fuites**. Le profiler aide a identifier les goulots d'etranglement de performance et les problemes memoire dans vos programmes.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Demarrage rapide](#demarrage-rapide)
- [Modes de profilage](#modes-de-profilage)
- [Formats de sortie](#formats-de-sortie)
- [Detection de fuites](#detection-de-fuites)
- [Comprendre les rapports](#comprendre-les-rapports)
- [Generation de flamegraph](#generation-de-flamegraph)
- [Bonnes pratiques](#bonnes-pratiques)

---

## Vue d'ensemble

Le profiler est accessible via la sous-commande `profile` :

```bash
hemlock profile [OPTIONS] <FILE>
```

**Fonctionnalites cles :**
- **Profilage CPU** - Mesurer le temps passe dans chaque fonction (temps propre et temps total)
- **Profilage memoire** - Suivre toutes les allocations avec les emplacements source
- **Detection de fuites** - Identifier la memoire qui n'a jamais ete liberee
- **Formats de sortie multiples** - Texte, JSON et sortie compatible flamegraph
- **Statistiques memoire par fonction** - Voir quelles fonctions allouent le plus de memoire

---

## Demarrage rapide

### Profiler le temps CPU (par defaut)

```bash
hemlock profile script.hml
```

### Profiler les allocations memoire

```bash
hemlock profile --memory script.hml
```

### Detecter les fuites memoire

```bash
hemlock profile --leaks script.hml
```

### Generer des donnees flamegraph

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## Modes de profilage

### Profilage CPU (par defaut)

Mesure le temps passe dans chaque fonction, distinguant entre :
- **Temps propre (Self)** - Temps passe a executer le propre code de la fonction
- **Temps total (Total)** - Temps propre plus temps passe dans les fonctions appelees

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # Explicite
```

**Exemple de sortie :**
```
=== Rapport du profiler Hemlock ===

Temps total : 1.234ms
Fonctions appelees : 5 uniques

--- Top 5 par temps propre ---

Fonction                        Self      Total   Appels
--------                        ----      -----   ------
expensive_calc              0.892ms    0.892ms     100  (72.3%)
process_data                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### Profilage memoire

Suit toutes les allocations memoire (`alloc`, `buffer`, `talloc`, `realloc`) avec les emplacements source.

```bash
hemlock profile --memory script.hml
```

**Exemple de sortie :**
```
=== Rapport du profiler Hemlock ===

Temps total : 0.543ms
Fonctions appelees : 3 uniques
Allocations totales : 15 (4.2Ko)

--- Top 3 par temps propre ---

Fonction                        Self      Total   Appels      Alloc      Nombre
--------                        ----      -----   ------      -----      ------
allocator                   0.312ms    0.312ms      10      3.2Ko         10  (57.5%)
buffer_ops                  0.156ms    0.156ms       5       1Ko          5  (28.7%)
main                        0.075ms    0.543ms       1        0o          0  (13.8%)

--- Top 10 sites d'allocation ---

Emplacement                                   Total    Nombre
-----------                                   -----    ------
src/data.hml:42                               1.5Ko        5
src/data.hml:67                               1.0Ko       10
src/main.hml:15                               512o         1
```

---

### Mode comptage d'appels

Mode a surcharge minimale qui compte uniquement les appels de fonction (pas de chronometrage).

```bash
hemlock profile --calls script.hml
```

---

## Formats de sortie

### Texte (par defaut)

Resume lisible par l'humain avec des tableaux.

```bash
hemlock profile script.hml
```

---

### JSON

Format lisible par machine pour l'integration avec d'autres outils.

```bash
hemlock profile --json script.hml
```

**Exemple de sortie :**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "expensive_calc",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### Flamegraph

Genere un format de pile reduit compatible avec [flamegraph.pl](https://github.com/brendangregg/FlameGraph).

```bash
hemlock profile --flamegraph script.hml > profile.folded

# Generer le SVG avec flamegraph.pl
flamegraph.pl profile.folded > profile.svg
```

**Exemple de sortie reduite :**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## Detection de fuites

Le drapeau `--leaks` montre uniquement les allocations qui n'ont jamais ete liberees, facilitant l'identification des fuites memoire.

```bash
hemlock profile --leaks script.hml
```

**Exemple de programme avec fuites :**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // Fuite - jamais libere
    let p2 = alloc(200);    // OK - libere ci-dessous
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // Correctement libere
}

leaky();
clean();
```

**Sortie avec --leaks :**
```
=== Rapport du profiler Hemlock ===

Temps total : 0.034ms
Fonctions appelees : 2 uniques
Allocations totales : 3 (388o)

--- Top 2 par temps propre ---

Fonction                        Self      Total   Appels      Alloc      Nombre
--------                        ----      -----   ------      -----      ------
leaky                       0.021ms    0.021ms       1       300o          2  (61.8%)
clean                       0.013ms    0.013ms       1        88o          1  (38.2%)

--- Fuites memoire (1 site) ---

Emplacement                                  Fuite      Total    Nombre
-----------                                  -----      -----    ------
script.hml:2                                  100o       100o        1
```

Le rapport de fuites montre :
- **Fuite (Leaked)** - Octets actuellement non liberes a la fin du programme
- **Total** - Octets totaux jamais alloues a ce site
- **Nombre (Count)** - Nombre d'allocations a ce site

---

## Comprendre les rapports

### Statistiques de fonction

| Colonne | Description |
|---------|-------------|
| Fonction | Nom de la fonction |
| Self | Temps dans la fonction excluant les appeles |
| Total | Temps incluant toutes les fonctions appelees |
| Appels (Calls) | Nombre de fois que la fonction a ete appelee |
| Alloc | Octets totaux alloues par cette fonction |
| Nombre (Count) | Nombre d'allocations par cette fonction |
| (%) | Pourcentage du temps total du programme |

### Sites d'allocation

| Colonne | Description |
|---------|-------------|
| Emplacement (Location) | Fichier source et numero de ligne |
| Total | Octets totaux alloues a cet emplacement |
| Nombre (Count) | Nombre d'allocations |
| Fuite (Leaked) | Octets encore alloues a la fin du programme (--leaks uniquement) |

### Unites de temps

Le profiler selectionne automatiquement les unites appropriees :
- `ns` - Nanosecondes (< 1us)
- `us` - Microsecondes (< 1ms)
- `ms` - Millisecondes (< 1s)
- `s` - Secondes

---

## Reference des commandes

```
hemlock profile [OPTIONS] <FILE>

OPTIONS :
    --cpu           Profilage CPU/temps (par defaut)
    --memory        Profilage des allocations memoire
    --calls         Comptage d'appels uniquement (surcharge minimale)
    --leaks         Montrer uniquement les allocations non liberees (implique --memory)
    --json          Sortie en format JSON
    --flamegraph    Sortie en format compatible flamegraph
    --top N         Montrer les top N entrees (defaut : 20)
```

---

## Generation de flamegraph

Les flamegraphs visualisent ou votre programme passe du temps, avec des barres plus larges indiquant plus de temps passe.

### Generer un flamegraph

1. Installer flamegraph.pl :
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. Profiler votre programme :
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. Generer le SVG :
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. Ouvrir `profile.svg` dans un navigateur pour une visualisation interactive.

### Lire les flamegraphs

- **Axe X** : Pourcentage du temps total (largeur = proportion du temps)
- **Axe Y** : Profondeur de la pile d'appels (bas = point d'entree, haut = fonctions feuilles)
- **Couleur** : Aleatoire, pour distinction visuelle uniquement
- **Clic** : Zoomer sur une fonction pour voir ses appeles

---

## Bonnes pratiques

### 1. Profiler des charges de travail representatives

Profilez avec des donnees et des patterns d'utilisation realistes. Les petits cas de test peuvent ne pas reveler les vrais goulots d'etranglement.

```bash
# Bien : Profiler avec des donnees type production
hemlock profile --memory process_large_file.hml large_input.txt

# Moins utile : Petit cas de test
hemlock profile quick_test.hml
```

### 2. Utiliser --leaks pendant le developpement

Executez la detection de fuites regulierement pour attraper les fuites memoire tot :

```bash
hemlock profile --leaks my_program.hml
```

### 3. Comparer avant et apres

Profilez avant et apres les optimisations pour mesurer l'impact :

```bash
# Avant optimisation
hemlock profile --json script.hml > before.json

# Apres optimisation
hemlock profile --json script.hml > after.json

# Comparer les resultats
```

### 4. Utiliser --top pour les gros programmes

Limitez la sortie pour vous concentrer sur les fonctions les plus significatives :

```bash
hemlock profile --top 10 large_program.hml
```

### 5. Combiner avec les flamegraphs

Pour des patterns d'appels complexes, les flamegraphs fournissent une meilleure visualisation que la sortie texte :

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## Surcharge du profiler

Le profiler ajoute une certaine surcharge a l'execution du programme :

| Mode | Surcharge | Cas d'utilisation |
|------|-----------|-------------------|
| `--calls` | Minimale | Juste compter les appels de fonction |
| `--cpu` | Faible | Profilage de performance general |
| `--memory` | Moderee | Analyse memoire et detection de fuites |

Pour les resultats les plus precis, profilez plusieurs fois et cherchez des patterns coherents.

---

## Voir aussi

- [Gestion memoire](../language-guide/memory.md) - Pointeurs et tampons
- [API memoire](../reference/memory-api.md) - Fonctions alloc, free, buffer
- [Async/Concurrence](async-concurrency.md) - Profilage du code async
