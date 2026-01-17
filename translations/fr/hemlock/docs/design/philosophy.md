# Philosophie de conception du langage Hemlock

> "Un petit langage non sécurisé pour écrire des choses non sécurisées en toute sécurité."

Ce document présente les principes et la philosophie de conception fondamentaux de Hemlock. Lisez-le avant d'apporter des modifications ou des ajouts au langage.

---

## Table des matières

- [Identité fondamentale](#identité-fondamentale)
- [Principes de conception](#principes-de-conception)
- [Philosophie sur la sécurité](#philosophie-sur-la-sécurité)
- [Ce qu'il ne faut PAS ajouter](#ce-quil-ne-faut-pas-ajouter)
- [Considérations futures](#considérations-futures)
- [Réflexions finales](#réflexions-finales)

---

## Identité fondamentale

Hemlock est un **langage de script système** qui adopte la gestion manuelle de la mémoire et le contrôle explicite. Il est conçu pour les programmeurs qui veulent :

- La puissance du C
- L'ergonomie des langages de script modernes
- La concurrence asynchrone structurée intégrée
- Aucun comportement caché ni magie

### Ce que Hemlock N'EST PAS

- **Sécurisé en mémoire** (les pointeurs invalides sont de votre responsabilité)
- **Un remplacement pour Rust, Go ou Lua**
- **Un langage qui vous cache la complexité**

### Ce que Hemlock EST

- **Explicite plutôt qu'implicite, toujours**
- **Éducatif et expérimental**
- **Une "couche de script C" pour le travail système**
- **Honnête sur les compromis**

---

## Principes de conception

### 1. Explicite plutôt qu'implicite

Hemlock favorise l'explicitation dans toutes les constructions du langage. Il ne devrait y avoir aucune surprise, aucune magie et aucun comportement caché.

**Mauvais (implicite) :**
```hemlock
let x = 5  // Point-virgule manquant - devrait générer une erreur
```

**Bon (explicite) :**
```hemlock
let x = 5;
free(ptr);  // Vous l'avez alloué, vous le libérez
```

**Aspects clés :**
- Les points-virgules sont obligatoires (pas d'insertion automatique)
- Pas de ramasse-miettes (garbage collection)
- Gestion manuelle de la mémoire (alloc/free)
- Les annotations de type sont optionnelles mais vérifiées à l'exécution
- Pas de nettoyage automatique des ressources (pas de RAII), mais `defer` fournit un nettoyage explicite

### 2. Dynamique par défaut, typé par choix

Chaque valeur possède une étiquette de type à l'exécution, mais le système est conçu pour être flexible tout en détectant les erreurs.

**Inférence de type :**
- Petits entiers (tient dans i32) : `42` → `i32`
- Grands entiers (> plage i32) : `9223372036854775807` → `i64`
- Flottants : `3.14` → `f64`

**Typage explicite si nécessaire :**
```hemlock
let x = 42;              // i32 inféré (petite valeur)
let y: u8 = 255;         // u8 explicite
let z = x + y;           // promu en i32
let big = 5000000000;    // i64 inféré (> max i32)
```

**Les règles de promotion de type** suivent une hiérarchie claire du plus petit au plus grand, les flottants l'emportant toujours sur les entiers.

### 3. L'insécurité est une fonctionnalité, pas un bug

Hemlock n'essaie pas de prévenir toutes les erreurs. Au lieu de cela, il vous donne les outils pour être en sécurité tout en vous permettant d'opter pour un comportement non sécurisé si nécessaire.

**Exemples d'insécurité intentionnelle :**
- L'arithmétique des pointeurs peut déborder (responsabilité de l'utilisateur)
- Pas de vérification des limites sur `ptr` brut (utilisez `buffer` si vous voulez la sécurité)
- Les crashs de double libération sont autorisés (gestion manuelle de la mémoire)
- Le système de types prévient les accidents mais permet les pièges si nécessaire

```hemlock
let p = alloc(10);
let q = p + 100;  // Bien au-delà de l'allocation - autorisé mais dangereux
```

**La philosophie :** Le système de types devrait prévenir les *accidents* mais autoriser les opérations non sécurisées *intentionnelles*.

### 4. Concurrence structurée de première classe

La concurrence n'est pas une réflexion après coup dans Hemlock. Elle est intégrée au langage dès le départ.

**Fonctionnalités clés :**
- `async`/`await` intégrés au langage
- Canaux pour la communication
- `spawn`/`join`/`detach` pour la gestion des tâches
- Pas de threads bruts, pas de verrous - structuré uniquement
- Vrai parallélisme multi-thread utilisant les threads POSIX

**Ce n'est pas une boucle d'événements ni des green threads** - Hemlock utilise de vrais threads du système d'exploitation pour un vrai parallélisme sur plusieurs cœurs CPU.

### 5. Syntaxe proche du C, peu de cérémonie

Hemlock devrait sembler familier aux programmeurs système tout en réduisant le code répétitif.

**Choix de conception :**
- Blocs `{}` toujours, pas d'accolades optionnelles
- Les opérateurs correspondent au C : `+`, `-`, `*`, `/`, `&&`, `||`, `!`
- La syntaxe de type correspond à Rust/TypeScript : `let x: type = value;`
- Les fonctions sont des valeurs de première classe
- Minimum de mots-clés et de formes spéciales

---

## Philosophie sur la sécurité

**La position de Hemlock sur la sécurité :**

> "Nous vous donnons les outils pour être en sécurité (`buffer`, annotations de type, vérification des limites) mais nous ne vous forçons pas à les utiliser (`ptr`, mémoire manuelle, opérations non sécurisées).
>
> Le comportement par défaut devrait guider vers la sécurité, mais la porte de sortie devrait toujours être disponible."

### Outils de sécurité fournis

**1. Type buffer sécurisé :**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // vérifié aux limites
print(b.length);        // 64
free(b);                // toujours manuel
```

**2. Pointeurs bruts non sécurisés :**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Vous devez penser à libérer
```

**3. Annotations de type :**
```hemlock
let x: u8 = 255;   // OK
let y: u8 = 256;   // ERREUR : hors plage
```

**4. Vérification de type à l'exécution :**
```hemlock
let val = some_function();
if (typeof(val) == "i32") {
    // Sûr de l'utiliser comme entier
}
```

### Principes directeurs

1. **Par défaut, utiliser des modèles sûrs dans la documentation** - Montrer `buffer` avant `ptr`, encourager les annotations de type
2. **Rendre les opérations non sécurisées évidentes** - L'arithmétique des pointeurs bruts devrait sembler intentionnelle
3. **Fournir des portes de sortie** - Ne pas empêcher les utilisateurs expérimentés de faire du travail bas niveau
4. **Être honnête sur les compromis** - Documenter ce qui peut mal tourner

### Exemples de sécurité vs insécurité

| Modèle sûr | Modèle non sûr | Quand utiliser le non sûr |
|------------|----------------|---------------------------|
| Type `buffer` | Type `ptr` | FFI, code critique en performance |
| Annotations de type | Pas d'annotations | Interfaces externes, validation |
| Accès vérifié aux limites | Arithmétique de pointeurs | Opérations mémoire bas niveau |
| Gestion des exceptions | Retour de null/codes d'erreur | Quand les exceptions sont trop lourdes |

---

## Ce qu'il ne faut PAS ajouter

Comprendre ce qu'il **ne faut pas** ajouter est aussi important que savoir quoi ajouter.

### Ne pas ajouter de comportement implicite

**Mauvais exemples :**

```hemlock
// MAUVAIS : Insertion automatique de point-virgule
let x = 5
let y = 10

// MAUVAIS : Conversions de type implicites qui perdent en précision
let x: i32 = 3.14  // Devrait tronquer ou générer une erreur ?
```

**Pourquoi :** Le comportement implicite crée des surprises et rend le code plus difficile à comprendre.

### Ne pas cacher la complexité

**Mauvais exemples :**

```hemlock
// MAUVAIS : Optimisation magique en coulisses
let arr = [1, 2, 3]  // Est-ce sur la pile ou le tas ? L'utilisateur devrait savoir ! (Tas, comptage de références)

// MAUVAIS : Pointeur brut auto-libéré
let p = alloc(100)  // Est-ce auto-libéré ? NON ! Les ptr bruts nécessitent toujours free()
```

**Note sur le comptage de références :** Hemlock utilise le comptage de références interne pour les chaînes, tableaux, objets et buffers - ceux-ci SONT auto-libérés quand la portée se termine. C'est explicite et prévisible (nettoyage déterministe quand la référence atteint 0, pas de pauses GC). Les pointeurs bruts (`ptr` de `alloc()`) ne sont PAS comptés par référence et nécessitent toujours `free()` manuel.

**Pourquoi :** La complexité cachée rend impossible de prédire les performances et de déboguer les problèmes.

### Ne pas casser les sémantiques existantes

**Ne jamais changer ces décisions fondamentales :**
- Les points-virgules sont obligatoires - ne pas les rendre optionnels
- Gestion manuelle de la mémoire - ne pas ajouter de GC
- Chaînes mutables - ne pas les rendre immuables
- Vérification de type à l'exécution - ne pas la supprimer

**Pourquoi :** La cohérence et la stabilité sont plus importantes que les fonctionnalités à la mode.

### Ne pas ajouter de fonctionnalités "pratiques" qui réduisent l'explicitation

**Exemples de fonctionnalités à éviter :**
- Surcharge d'opérateurs (peut-être pour les types utilisateur, mais avec prudence)
- Coercition de type implicite qui perd de l'information
- Nettoyage automatique des ressources (RAII)
- Chaînage de méthodes qui cache la complexité
- DSL et syntaxe magique

**Exception :** Les fonctionnalités de commodité sont OK si elles sont du **sucre syntaxique explicite** sur des opérations simples :
- `else if` est bien (ce sont juste des instructions if imbriquées)
- L'interpolation de chaînes pourrait être OK si c'est clairement du sucre syntaxique
- La syntaxe de méthode pour les objets est bien (c'est explicite ce que ça fait)

---

## Considérations futures

### Peut-être ajouter (en discussion)

Ces fonctionnalités s'alignent avec la philosophie de Hemlock mais nécessitent une conception soignée :

**1. Pattern matching (correspondance de motifs)**
```hemlock
match (value) {
    case i32: print("entier");
    case string: print("texte");
    case _: print("autre");
}
```
- Vérification de type explicite
- Pas de coûts cachés
- Vérification d'exhaustivité à la compilation possible

**2. Types d'erreur (`Result<T, E>`)**
```hemlock
fn divide(a: i32, b: i32): Result<i32, string> {
    if (b == 0) {
        return Err("division par zéro");
    }
    return Ok(a / b);
}
```
- Gestion d'erreur explicite
- Force les utilisateurs à penser aux erreurs
- Alternative aux exceptions

**3. Types tableau/slice**
- Nous avons déjà des tableaux dynamiques
- Pourrait ajouter des tableaux de taille fixe pour l'allocation sur la pile
- Devrait être explicite sur pile vs tas

**4. Outils de sécurité mémoire améliorés**
- Option de vérification des limites
- Détection des fuites mémoire en mode debug
- Intégration des sanitizers

### Probablement jamais ajouter

Ces fonctionnalités violent les principes fondamentaux :

**1. Ramasse-miettes (garbage collection)**
- Cache la complexité de la gestion mémoire
- Performances imprévisibles
- Contre le principe de contrôle explicite

**2. Gestion automatique de la mémoire**
- Mêmes raisons que le GC
- Le comptage de références pourrait être OK s'il est explicite

**3. Conversions de type implicites qui perdent des données**
- Va contre "explicite plutôt qu'implicite"
- Source de bugs subtils

**4. Macros (complexes)**
- Trop de puissance, trop de complexité
- Un système de macros simple pourrait être OK
- Préférer la génération de code ou les fonctions

**5. POO basée sur les classes avec héritage**
- Trop de comportement implicite
- Le duck typing et les objets sont suffisants
- Composition plutôt qu'héritage

**6. Système de modules avec résolution complexe**
- Garder les imports simples et explicites
- Pas de chemins de recherche magiques
- Pas de résolution de version (utiliser le gestionnaire de paquets de l'OS)

---

## Réflexions finales

### Confiance et responsabilité

Hemlock est une question de **confiance et responsabilité**. Nous faisons confiance au programmeur pour :

- Gérer la mémoire correctement
- Utiliser les types de manière appropriée
- Gérer les erreurs correctement
- Comprendre les compromis

En retour, Hemlock fournit :

- Pas de coûts cachés
- Pas de comportement surprise
- Contrôle total quand nécessaire
- Outils de sécurité quand souhaité

### La question directrice

**Quand vous considérez une nouvelle fonctionnalité, demandez-vous :**

> "Est-ce que cela donne au programmeur plus de contrôle explicite, ou est-ce que cela cache quelque chose ?"

- Si cela **ajoute du contrôle explicite** → convient probablement à Hemlock
- Si cela **cache de la complexité** → n'appartient probablement pas
- Si c'est du **sucre optionnel** clairement documenté → pourrait être OK

### Exemples de bons ajouts

Les **instructions switch** - Flux de contrôle explicite, pas de magie, sémantique claire

L'**async/await avec pthreads** - Concurrence explicite, vrai parallélisme, l'utilisateur contrôle le lancement

Le **type Buffer à côté de ptr** - Donne le choix entre sûr et non sûr

Les **annotations de type optionnelles** - Aide à détecter les bugs sans forcer la rigueur

**Try/catch/finally** - Gestion d'erreur explicite avec flux de contrôle clair

### Exemples de mauvais ajouts

L'**insertion automatique de point-virgule** - Cache les erreurs de syntaxe, rend le code ambigu

Le **RAII/destructeurs** - Le nettoyage automatique cache quand les ressources sont libérées

La **coalescence null implicite** - Cache les vérifications de null, rend le code plus difficile à comprendre

Les **chaînes à croissance automatique** - Cache l'allocation mémoire, performances imprévisibles

---

## Conclusion

Hemlock n'essaie pas d'être le langage le plus sûr, le plus rapide ou le plus riche en fonctionnalités.

**Hemlock essaie d'être le langage le plus *honnête*.**

Il vous dit exactement ce qu'il fait, vous donne le contrôle quand vous en avez besoin, et ne cache pas les bords tranchants. C'est un langage pour les personnes qui veulent comprendre leur code à bas niveau tout en profitant d'une ergonomie moderne.

Si vous n'êtes pas sûr qu'une fonctionnalité appartient à Hemlock, souvenez-vous :

> **Explicite plutôt qu'implicite, toujours.**
> **L'insécurité est une fonctionnalité, pas un bug.**
> **L'utilisateur est responsable, et c'est OK.**
