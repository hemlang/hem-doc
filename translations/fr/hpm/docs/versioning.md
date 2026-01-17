# Versionnage

Guide complet du versionnage semantique dans hpm.

## Versionnage semantique

hpm utilise le [Versionnage semantique 2.0.0](https://semver.org/) (semver) pour les versions des paquets.

### Format de version

```
MAJEUR.MINEUR.PATCH[-PRERELEASE][+BUILD]
```

**Exemples :**
```
1.0.0           # Version de release
2.1.3           # Version de release
1.0.0-alpha     # Pre-release
1.0.0-beta.1    # Pre-release avec numero
1.0.0-rc.1      # Release candidate
1.0.0+20231201  # Avec metadonnees de build
1.0.0-beta+exp  # Pre-release avec metadonnees de build
```

### Composants de version

| Composant | Description | Exemple |
|-----------|-------------|---------|
| MAJEUR | Changements incompatibles | `1.0.0` -> `2.0.0` |
| MINEUR | Nouvelles fonctionnalites (retro-compatible) | `1.0.0` -> `1.1.0` |
| PATCH | Corrections de bugs (retro-compatible) | `1.0.0` -> `1.0.1` |
| PRERELEASE | Identifiant de pre-release | `1.0.0-alpha` |
| BUILD | Metadonnees de build (ignorees dans la comparaison) | `1.0.0+build123` |

### Quand incrementer

| Type de changement | Increment | Exemple |
|--------------------|-----------|---------|
| Changement d'API incompatible | MAJEUR | Suppression d'une fonction |
| Renommer une fonction publique | MAJEUR | `parse()` -> `decode()` |
| Changer la signature d'une fonction | MAJEUR | Ajouter un parametre obligatoire |
| Ajouter une nouvelle fonction | MINEUR | Ajouter `validate()` |
| Ajouter un parametre optionnel | MINEUR | Nouveau arg `options` optionnel |
| Correction de bug | PATCH | Corriger un pointeur null |
| Amelioration de performance | PATCH | Algorithme plus rapide |
| Refactoring interne | PATCH | Pas de changement d'API |

## Contraintes de version

### Syntaxe des contraintes

| Syntaxe | Signification | Resout vers |
|---------|---------------|-------------|
| `1.2.3` | Version exacte | 1.2.3 uniquement |
| `^1.2.3` | Caret (compatible) | >=1.2.3 et <2.0.0 |
| `~1.2.3` | Tilde (mises a jour patch) | >=1.2.3 et <1.3.0 |
| `>=1.0.0` | Au moins | 1.0.0 ou superieur |
| `>1.0.0` | Superieur a | Superieur a 1.0.0 |
| `<2.0.0` | Inferieur a | Inferieur a 2.0.0 |
| `<=2.0.0` | Au plus | 2.0.0 ou inferieur |
| `>=1.0.0 <2.0.0` | Plage | Entre 1.0.0 et 2.0.0 |
| `*` | N'importe quelle | N'importe quelle version |

### Plages Caret (^)

Le caret (`^`) permet les changements qui ne modifient pas le chiffre non-nul le plus a gauche :

```
^1.2.3  ->  >=1.2.3 <2.0.0   # Permet 1.x.x
^0.2.3  ->  >=0.2.3 <0.3.0   # Permet 0.2.x
^0.0.3  ->  >=0.0.3 <0.0.4   # Permet 0.0.3 uniquement
```

**Utilisez quand :** Vous voulez des mises a jour compatibles dans une version majeure.

**Contrainte la plus courante** - recommandee pour la plupart des dependances.

### Plages Tilde (~)

Le tilde (`~`) permet uniquement les changements de niveau patch :

```
~1.2.3  ->  >=1.2.3 <1.3.0   # Permet 1.2.x
~1.2    ->  >=1.2.0 <1.3.0   # Permet 1.2.x
~1      ->  >=1.0.0 <2.0.0   # Permet 1.x.x
```

**Utilisez quand :** Vous voulez uniquement les corrections de bugs, pas de nouvelles fonctionnalites.

### Plages de comparaison

Combinez les operateurs de comparaison pour un controle precis :

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### N'importe quelle version (*)

Correspond a n'importe quelle version :

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**Attention :** Non recommande pour la production. Obtiendra toujours la derniere version.

## Versions pre-release

### Identifiants de pre-release

Les pre-releases ont une precedence inferieure aux releases :

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Tags de pre-release courants

| Tag | Signification | Etape |
|-----|---------------|-------|
| `alpha` | Developpement initial | Tres instable |
| `beta` | Fonctionnalites completes | Tests |
| `rc` | Release candidate | Tests finaux |
| `dev` | Snapshot de developpement | Instable |

### Pre-release dans les contraintes

Les contraintes ne correspondent pas aux pre-releases par defaut :

```
^1.0.0    # Ne correspond PAS a 1.1.0-beta
>=1.0.0   # Ne correspond PAS a 2.0.0-alpha
```

Pour inclure les pre-releases, referencez-les explicitement :

```
>=1.0.0-alpha <2.0.0   # Inclut toutes les pre-releases 1.x
```

## Comparaison de versions

### Regles de comparaison

1. Comparez MAJEUR, MINEUR, PATCH numeriquement
2. Release > pre-release avec la meme version
3. Pre-releases comparees alphanumeriquement
4. Les metadonnees de build sont ignorees

### Exemples

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Metadonnees de build ignorees
```

### Tri

Les versions sont triees par ordre croissant :

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Resolution de version

### Algorithme de resolution

Quand plusieurs paquets necessitent la meme dependance :

1. Collecter toutes les contraintes
2. Trouver l'intersection de toutes les plages
3. Selectionner la version la plus elevee dans l'intersection
4. Erreur si aucune version ne satisfait toutes les contraintes

### Exemple de resolution

```
package-a necessite hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b necessite hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Intersection: >=1.2.0 <1.3.0
Disponibles: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Resolue: 1.2.5 (la plus elevee dans l'intersection)
```

### Detection de conflits

Un conflit survient quand aucune version ne satisfait toutes les contraintes :

```
package-a necessite hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b necessite hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Intersection: (vide)
Resultat: CONFLIT - aucune version ne satisfait les deux
```

## Bonnes pratiques

### Pour les consommateurs de paquets

1. **Utilisez des plages caret** pour la plupart des dependances :
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Utilisez des plages tilde** pour les dependances critiques :
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **Epinglez les versions** uniquement si necessaire :
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **Commitez votre fichier de verrouillage** pour des builds reproductibles

5. **Mettez a jour regulierement** pour obtenir les correctifs de securite :
   ```bash
   hpm update
   hpm outdated
   ```

### Pour les auteurs de paquets

1. **Commencez a 0.1.0** pour le developpement initial :
   - L'API peut changer frequemment
   - Les utilisateurs s'attendent a de l'instabilite

2. **Passez a 1.0.0** quand l'API est stable :
   - Engagement public envers la stabilite
   - Les changements incompatibles necessitent un increment majeur

3. **Suivez strictement semver** :
   - Changement incompatible = MAJEUR
   - Nouvelle fonctionnalite = MINEUR
   - Correction de bug = PATCH

4. **Utilisez les pre-releases** pour les tests :
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Documentez les changements incompatibles** dans le CHANGELOG

## Publication de versions

### Creer des releases

```bash
# Mettre a jour la version dans package.json
# Editez package.json : "version": "1.1.0"

# Commiter le changement de version
git add package.json
git commit -m "Bump version to 1.1.0"

# Creer et pousser le tag
git tag v1.1.0
git push origin main --tags
```

### Format des tags

Les tags **doivent** commencer par `v` :

```
v1.0.0      Correct
v1.0.0-beta Correct
1.0.0       Ne sera pas reconnu
```

### Flux de travail de release

```bash
# 1. S'assurer que les tests passent
hpm test

# 2. Mettre a jour la version dans package.json
# 3. Mettre a jour CHANGELOG.md
# 4. Commiter les changements
git add -A
git commit -m "Release v1.2.0"

# 5. Creer le tag
git tag v1.2.0

# 6. Tout pousser
git push origin main --tags
```

## Verifier les versions

### Lister les versions installees

```bash
hpm list
```

### Verifier les mises a jour disponibles

```bash
hpm outdated
```

Sortie :
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current** : Version installee
- **Wanted** : Plus haute correspondant a la contrainte
- **Latest** : Derniere disponible

### Mettre a jour les paquets

```bash
# Mettre a jour tout
hpm update

# Mettre a jour un paquet specifique
hpm update hemlang/json
```

## Voir aussi

- [Creer des paquets](creating-packages.md) - Guide de publication
- [Specification des paquets](package-spec.md) - Format package.json
- [Commandes](commands.md) - Reference CLI
