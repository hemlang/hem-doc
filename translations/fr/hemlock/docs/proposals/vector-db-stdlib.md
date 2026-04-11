# Proposition : `@stdlib/vector` -- Module de recherche de similarite vectorielle

**Statut :** Exploration / RFC
**Date :** 2026-02-07

---

## Resume

Ajouter un module `@stdlib/vector` fournissant une recherche de similarite vectorielle en processus (recherche du plus proche voisin). Cela permet la recherche basee sur les embeddings, les systemes de recommandation et les workflows IA/ML directement depuis Hemlock sans necessiter de serveur externe.

---

## Options evaluees

Dix options de base de donnees vectorielles / bibliotheques ont ete evaluees selon ces criteres :

| Critere | Poids | Justification |
|---------|-------|---------------|
| Qualite de l'API C | Critique | Le FFI de Hemlock necessite une liaison C (`extern fn`) vers des bibliotheques `.so` |
| Embarquable (en processus) | Critique | Les modules stdlib de Hemlock sont des bibliotheques, pas des protocoles client-serveur |
| Poids des dependances | Eleve | Dependances minimales preferees (comme sqlite -- juste un `.so`) |
| Simplicite de l'API | Eleve | Hemlock valorise les APIs explicites et petites |
| Performance | Moyen | Suffisant pour 1M+ vecteurs ; pas besoin d'echelle milliard |
| Persistance | Moyen | Sauvegarder/charger les index sur disque |
| Licence | Moyen | Doit etre permissive (Apache-2.0, MIT, BSD) |

### Resultats

| Option | API C | Embarquable | Deps | Performance | Verdict |
|--------|-------|-------------|------|-------------|---------|
| **USearch** | C99 premiere classe | Oui | Zero | HNSW + SIMD | **PRINCIPAL** |
| **sqlite-vec** | Via SQL | Oui | Zero (C pur) | Force brute | **SECONDAIRE** |
| hnswlib | C++ uniquement | Oui | Zero | HNSW | Pas d'API C -- passe |
| FAISS | API C (faiss_c) | Oui | BLAS requis | Etat de l'art | Trop lourd |
| pgvector | N/A | Non (necessite PG) | PostgreSQL | Bon | Serveur requis -- passe |
| Qdrant | Aucune | Non (serveur) | Lourd | Excellent | Serveur requis -- passe |
| Milvus | SDK C++ | Non (distribue) | Tres lourd | Excellent | Systeme distribue -- passe |
| Annoy | C++ uniquement | Oui | Zero | Modere | Obsolete, pas d'API C |
| LanceDB | C communautaire seul | Oui | Modere (Rust) | Bon | Pas d'API C officielle |
| ChromaDB | Aucune | Limite | Lourd | Modere | Pas d'API C |

---

## Recommandation : USearch (principal) + sqlite-vec (alternative legere)

### Pourquoi PAS pgvector

pgvector necessite un serveur PostgreSQL en cours d'execution. Les modules stdlib de Hemlock sont des bibliotheques embarquables chargees via FFI (`import "libfoo.so"`), pas des protocoles client-serveur. Exiger des utilisateurs d'installer, configurer et executer PostgreSQL pour la recherche vectorielle est fondamentalement incompatible avec le patron stdlib. Le module sqlite fonctionne precisement parce que SQLite est une bibliotheque en processus sans exigence de serveur.

### Principal : USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) est une bibliotheque de recherche de similarite vectorielle open-source (Apache-2.0) avec une API C99 de premiere classe. Elle utilise l'algorithme HNSW (Hierarchical Navigable Small World) avec optimisation SIMD.

**Pourquoi USearch convient a Hemlock :**

1. **L'API C99 correspond directement au FFI de Hemlock.** Le patron est identique a `@stdlib/sqlite`.
2. **Zero dependance obligatoire.** Se compile en un seul `.so` sans BLAS, LAPACK, ni autre exigence externe.
3. **En processus et persistant.** Support des fichiers mappes en memoire -- les index sont sauvegardes sur disque, charges sans tout lire en RAM.
4. **API petite et explicite.** ~20 fonctions C couvrant : init, add, search, remove, save, load, free. S'inscrit dans la philosophie "explicite plutot qu'implicite" de Hemlock.
5. **Prouve en production.** Utilise par ScyllaDB et YugabyteDB pour l'indexation vectorielle.
6. **Performance.** Algorithme HNSW avec SIMD (AVX-512, NEON). Supporte f32, f64, f16, et quantification int8. Gere des millions de vecteurs en processus.

### Secondaire : sqlite-vec (extension de `@stdlib/sqlite`)

[sqlite-vec](https://github.com/asg017/sqlite-vec) est une extension SQLite fournissant la recherche vectorielle via SQL. Elle pourrait etre chargee via `sqlite3_load_extension()` depuis le module `@stdlib/sqlite` existant sans nouveau binding FFI necessaire.

---

## Conception d'API proposee (`@stdlib/vector`)

Suivant les patrons etablis par `@stdlib/sqlite` (wrapper FFI avec API idiomatique Hemlock) :

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Creer un index
let idx = create_index(dimensions: 384, metric: "cosine");

// Ajouter des vecteurs (cle + tableau de flottants)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// Rechercher les k plus proches voisins
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// retourne : [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Persistance
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Recherche filtree (avec predicat)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;  // ne correspond qu'aux cles > 100
});

// Informations
print(idx.size());       // nombre de vecteurs
print(idx.dimensions()); // dimensionnalite
print(idx.contains(42)); // verification d'appartenance

// Nettoyage
idx.remove(2);
idx.free();
```

### Exports du module

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // mappe en memoire, lecture seule

VectorIndex.add(key, vector)
VectorIndex.search(query, k?)
VectorIndex.search_filtered(query, k?, filter)
VectorIndex.remove(key)
VectorIndex.contains(key)
VectorIndex.count()
VectorIndex.size()
VectorIndex.dimensions()
VectorIndex.save(path)
VectorIndex.free()

distance(a, b, metric?)  // calcul de distance autonome

// Metriques de distance
METRIC_COSINE
METRIC_L2SQ       // Euclidien (L2 au carre)
METRIC_IP          // Produit interieur (produit scalaire)
METRIC_HAMMING
METRIC_JACCARD

// Types scalaires
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

### Exigences systeme

```
# Debian/Ubuntu
sudo apt install libusearch-dev

# Depuis les sources
git clone https://github.com/unum-cloud/usearch
cd usearch && cmake -B build && cmake --build build
sudo cmake --install build
```

---

## Plan d'implementation

1. **Ecrire les bindings FFI** -- declarations `extern fn` pour l'API C USearch (~20 fonctions)
2. **Implementer le wrapper Hemlock** -- `create_index()`, define `VectorIndex` avec methodes
3. **Gerer la memoire** -- `alloc`/`free` corrects pour le marshalling de donnees vectorielles, nettoyage de chaines d'erreur
4. **Ajouter la documentation** -- `stdlib/docs/vector.md` suivant le patron de sqlite.md
5. **Ajouter des tests** -- `tests/stdlib_vector/` avec CRUD basique, persistance, precision de recherche
6. **Ajouter des tests de parite** -- Si le support compilateur est necessaire pour les patrons FFI utilises

Portee estimee : ~400-600 lignes de Hemlock (comparable a `sqlite.hml` avec 968 lignes, mais surface d'API plus simple).

---

## Questions ouvertes

1. **Nom du module :** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity` ?
2. **Integration sqlite-vec :** Livrer comme partie de `@stdlib/sqlite` (chargement d'extension) ou module separe ?
3. **API de quantification :** Exposer la quantification int8/f16 de USearch, ou utiliser f32 par defaut et rester simple ?
4. **Operations par lot :** Ajouter `add_batch()` / `search_batch()` pour les operations en masse, ou garder l'API element par element ?
5. **Configuration d'index :** Quelle part du reglage HNSW de USearch (connectivite, facteurs d'expansion) exposer ?
