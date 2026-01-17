# Bienvenue dans Hemlock

> "Un petit langage non sécurisé pour écrire des choses non sécurisées en toute sécurité."

**Hemlock** est un langage de script système qui combine la puissance du C avec l'ergonomie des langages de script modernes. Il propose une gestion manuelle de la mémoire, un contrôle explicite et une concurrence asynchrone structurée intégrée.

## Qu'est-ce que Hemlock ?

Hemlock est conçu pour les programmeurs qui veulent :

- **Un contrôle explicite** sur la mémoire et l'exécution
- **Une syntaxe similaire au C** avec des commodités modernes
- **Aucun comportement caché** ni magie
- **Une vraie concurrence asynchrone parallèle** avec une concurrence basée sur pthread

Hemlock N'EST PAS un langage à mémoire sécurisée avec ramasse-miettes. Au lieu de cela, il vous donne les outils pour être en sécurité (`buffer`, annotations de type, vérification des limites) sans vous forcer à les utiliser (`ptr`, mémoire manuelle, opérations non sécurisées).

## Exemple Rapide

```hemlock
// Bonjour, Hemlock !
fn greet(name: string): string {
    return `Bonjour, ${name} !`;
}

let message = greet("Monde");
print(message);

// Gestion manuelle de la mémoire
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Fonctionnalités en un Coup d'Œil

| Fonctionnalité | Description |
|----------------|-------------|
| **Système de Types** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Mémoire** | Gestion manuelle avec `alloc()`, `buffer()`, `free()` |
| **Async** | `async`/`await` intégré avec vrai parallélisme pthread |
| **FFI** | Appeler des fonctions C directement depuis des bibliothèques partagées |
| **Bibliothèque Standard** | 40 modules incluant crypto, http, sqlite, json, et plus |

## Prise en Main

Prêt à vous lancer ? Voici comment commencer :

1. **[Installation](#getting-started-installation)** - Télécharger et configurer Hemlock
2. **[Démarrage Rapide](#getting-started-quick-start)** - Écrire votre premier programme en quelques minutes
3. **[Tutoriel](#getting-started-tutorial)** - Apprendre Hemlock étape par étape

## Sections de la Documentation

- **Prise en Main** - Installation, guide de démarrage rapide et tutoriels
- **Guide du Langage** - Plongée approfondie dans la syntaxe, les types, les fonctions, et plus
- **Sujets Avancés** - Programmation asynchrone, FFI, signaux et atomiques
- **Référence API** - Référence complète pour les fonctions intégrées et la bibliothèque standard
- **Conception et Philosophie** - Comprendre pourquoi Hemlock est ce qu'il est

## Gestionnaire de Paquets

Hemlock est livré avec **hpm**, un gestionnaire de paquets pour gérer les dépendances :

```bash
hpm init mon-projet
hpm add un-paquet
hpm run
```

Consultez les sections de documentation hpm pour plus de détails.

---

Utilisez la navigation à gauche pour explorer la documentation, ou utilisez la barre de recherche pour trouver des sujets spécifiques.
