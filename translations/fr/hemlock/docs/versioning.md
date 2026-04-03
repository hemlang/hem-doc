# Versionnage de Hemlock

Ce document decrit la strategie de versionnage pour Hemlock.

## Format de version

Hemlock utilise le **Versionnage Semantique** (SemVer) :

```
MAJEUR.MINEUR.CORRECTIF
```

| Composant | Quand incrementer |
|-----------|-------------------|
| **MAJEUR** | Changements incompatibles dans la semantique du langage, l'API stdlib ou les formats binaires |
| **MINEUR** | Nouvelles fonctionnalites, ajouts retrocompatibles |
| **CORRECTIF** | Corrections de bugs, ameliorations de performance, documentation |

## Versionnage unifie

Tous les composants de Hemlock partagent un **numero de version unique** :

- **Interpreteur** (`hemlock`)
- **Compilateur** (`hemlockc`)
- **Serveur LSP** (`hemlock --lsp`)
- **Bibliotheque standard** (`@stdlib/*`)

La version est definie dans `include/version.h` :

```c
#define HEMLOCK_VERSION_MAJOR 1
#define HEMLOCK_VERSION_MINOR 8
#define HEMLOCK_VERSION_PATCH 7

#define HEMLOCK_VERSION "1.8.7"
```

### Verification des versions

```bash
# Version de l'interpreteur
hemlock --version

# Version du compilateur
hemlockc --version
```

## Garanties de compatibilite

### Au sein d'une version MAJEURE

- Le code source qui fonctionne en `1.x.0` fonctionnera en `1.x.y` (tout correctif)
- Le code source qui fonctionne en `1.0.x` fonctionnera en `1.y.z` (tout mineur/correctif)
- Les bundles `.hmlb` compiles sont compatibles au sein de la meme version MAJEURE
- Les APIs de la bibliotheque standard sont stables (ajouts uniquement, pas de suppressions)

### Entre versions MAJEURES

- Les changements incompatibles sont documentes dans les notes de version
- Des guides de migration sont fournis pour les changements significatifs
- Les fonctionnalites depreciees sont signalees pendant au moins une version mineure avant leur suppression

## Versionnage des formats binaires

Hemlock utilise des numeros de version separes pour les formats binaires :

| Format | Version | Emplacement |
|--------|---------|-------------|
| `.hmlc` (bundle AST) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (bundle compresse) | Identique a HMLC | Utilise la compression zlib |
| `.hmlp` (executable package) | Magic : `HMLP` | Format autonome |

Les versions des formats binaires s'incrementent independamment quand la serialisation change.

## Versionnage de la bibliotheque standard

La bibliotheque standard (`@stdlib/*`) est versionnee **avec la version principale** :

```hemlock
// Always uses the stdlib bundled with your Hemlock installation
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Compatibilite de la stdlib

- De nouveaux modules peuvent etre ajoutes dans les versions MINEURES
- De nouvelles fonctions peuvent etre ajoutees aux modules existants dans les versions MINEURES
- Les signatures de fonctions sont stables au sein d'une version MAJEURE
- Les fonctions depreciees sont marquees et documentees avant suppression

## Historique des versions

| Version | Date | Points forts |
|---------|------|------------|
| **1.8.7** | 2026 | Correction du print/eprint multi-arguments dans le codegen du compilateur |
| **1.8.6** | 2026 | Correction du segfault dans hml_string_append_inplace pour les chaines SSO |
| **1.8.5** | 2026 | 5 nouvelles methodes de tableau (every, some, indexOf, sort, fill), optimisations de performance majeures, corrections de fuites memoire |
| **1.8.4** | 2026 | Gestion elegante des mots-cles reserves (def, func, var, class), correction des tests CI instables |
| **1.8.3** | 2026 | Polissage du code : consolidation des nombres magiques, standardisation des messages d'erreur |
| **1.8.2** | 2026 | Prevention des fuites memoire : eval securise aux exceptions, nettoyage task/channel, corrections de l'optimiseur |
| **1.8.1** | 2026 | Correction du bug use-after-free dans la gestion des valeurs de retour de fonction |
| **1.8.0** | 2026 | Pattern matching, allocateur arena, corrections de fuites memoire |
| **1.7.5** | 2026 | Correction du bug d'indentation else-if du formateur |
| **1.7.4** | 2026 | Ameliorations du formateur : retour a la ligne des parametres de fonction, expressions binaires, imports et chaines de methodes |
| **1.7.3** | 2026 | Correction de la preservation des commentaires et lignes vides du formateur |
| **1.7.2** | 2026 | Version de maintenance |
| **1.7.1** | 2026 | Instructions if/while/for sur une ligne (syntaxe sans accolades) |
| **1.7.0** | 2026 | Alias de type, types de fonction, parametres const, signatures de methode, etiquettes de boucle, arguments nommes, coalescence null |
| **1.6.7** | 2026 | Litteraux octaux, commentaires bloc, echappements hex/unicode, separateurs numeriques |
| **1.6.6** | 2026 | Litteraux flottants sans zero initial, correction du bug de reduction de force |
| **1.6.5** | 2026 | Correction de la syntaxe de boucle for-in sans mot-cle 'let' |
| **1.6.4** | 2026 | Version de correction urgente |
| **1.6.3** | 2026 | Correction du dispatch de methodes runtime pour les types file, channel, socket |
| **1.6.2** | 2026 | Version de correctif |
| **1.6.1** | 2026 | Version de correctif |
| **1.6.0** | 2025 | Verification de type a la compilation dans hemlockc, integration LSP, operateurs d'affectation composee bit a bit (`&=`, `\|=`, `^=`, `<<=`, `>>=`, `%=`) |
| **1.5.0** | 2024 | Systeme de types complet, async/await, atomics, 39 modules stdlib, support des structures FFI, 99 tests de parite |
| **1.3.0** | 2025 | Portee lexicale par blocs correcte (semantique let/const a la JS), closures par iteration de boucle |
| **1.2.3** | 2025 | Syntaxe import star (`import * from`) |
| **1.2.2** | 2025 | Ajout du support `export extern`, corrections de tests multiplateforme |
| **1.2.1** | 2025 | Correction des echecs de test macOS (generation de cle RSA, liens symboliques de repertoire) |
| **1.2.0** | 2025 | Optimiseur AST, builtin apply(), canaux non bufferises, 7 nouveaux modules stdlib, 97 tests de parite |
| **1.1.3** | 2025 | Mises a jour de documentation, corrections de coherence |
| **1.1.1** | 2025 | Corrections de bugs et ameliorations |
| **1.1.0** | 2024 | Versionnage unifie de tous les composants |
| **1.0.x** | 2024 | Serie de versions initiales |

## Processus de publication

1. Mise a jour de la version dans `include/version.h`
2. Mise a jour du changelog
3. Execution de la suite de tests complete (`make test-all`)
4. Tag de la version dans git
5. Construction des artefacts de publication

## Verification de la compatibilite

Pour verifier que votre code fonctionne avec une version specifique de Hemlock :

```bash
# Executer les tests avec la version installee
make test

# Verifier la parite entre interpreteur et compilateur
make parity
```

## Futur : Manifestes de projet

Une future version pourrait introduire des manifestes de projet optionnels pour les contraintes de version :

```hemlock
// Hypothetical project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

Ceci n'est pas encore implemente mais fait partie de la feuille de route.
