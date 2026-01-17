# Référence de l'API File

Référence complète pour le système d'entrée/sortie de fichiers de Hemlock.

---

## Aperçu

Hemlock fournit une **API objet File** pour les opérations sur les fichiers avec une gestion appropriée des erreurs et des ressources. Les fichiers doivent être ouverts et fermés manuellement.

**Caractéristiques principales :**
- Objet file avec méthodes
- Lecture/écriture de texte et données binaires
- Positionnement et recherche
- Messages d'erreur appropriés
- Gestion manuelle des ressources (pas de RAII)

---

## Type File

**Type :** `file`

**Description :** Handle de fichier pour les opérations d'E/S

**Propriétés (lecture seule) :**
- `.path` - Chemin du fichier (string)
- `.mode` - Mode d'ouverture (string)
- `.closed` - Si le fichier est fermé (bool)

---

## Ouverture des fichiers

### open

Ouvre un fichier pour lecture, écriture, ou les deux.

**Signature :**
```hemlock
open(path: string, mode?: string): file
```

**Paramètres :**
- `path` - Chemin du fichier (relatif ou absolu)
- `mode` (optionnel) - Mode d'ouverture (par défaut : `"r"`)

**Retourne :** Objet file

**Modes :**
- `"r"` - Lecture (par défaut)
- `"w"` - Écriture (tronque le fichier existant)
- `"a"` - Ajout
- `"r+"` - Lecture et écriture
- `"w+"` - Lecture et écriture (tronque)
- `"a+"` - Lecture et ajout

**Exemples :**
```hemlock
// Mode lecture (par défaut)
let f = open("data.txt");
let f_read = open("data.txt", "r");

// Mode écriture (tronque)
let f_write = open("output.txt", "w");

// Mode ajout
let f_append = open("log.txt", "a");

// Mode lecture/écriture
let f_rw = open("data.bin", "r+");

// Lecture/écriture (tronque)
let f_rw_trunc = open("output.bin", "w+");

// Lecture/ajout
let f_ra = open("log.txt", "a+");
```

**Gestion des erreurs :**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Échec d'ouverture:", e);
    // Erreur: Échec d'ouverture de 'missing.txt': Fichier ou répertoire inexistant
}
```

**Important :** Les fichiers doivent être fermés manuellement avec `f.close()` pour éviter les fuites de descripteurs de fichiers.

---

## Méthodes File

### Lecture

#### read

Lit du texte depuis le fichier.

**Signature :**
```hemlock
file.read(size?: i32): string
```

**Paramètres :**
- `size` (optionnel) - Nombre d'octets à lire (si omis, lit jusqu'à la fin du fichier)

**Retourne :** Chaîne avec le contenu du fichier

**Exemples :**
```hemlock
let f = open("data.txt", "r");

// Lire le fichier entier
let all = f.read();
print(all);

// Lire un nombre spécifique d'octets
let chunk = f.read(1024);

f.close();
```

**Comportement :**
- Lit depuis la position actuelle du fichier
- Retourne une chaîne vide à la fin du fichier
- Avance la position du fichier

**Erreurs :**
- Lecture depuis un fichier fermé
- Lecture depuis un fichier en écriture seule

---

#### read_bytes

Lit des données binaires depuis le fichier.

**Signature :**
```hemlock
file.read_bytes(size: i32): buffer
```

**Paramètres :**
- `size` - Nombre d'octets à lire

**Retourne :** Buffer avec les données binaires

**Exemples :**
```hemlock
let f = open("data.bin", "r");

// Lire 256 octets
let binary = f.read_bytes(256);
print(binary.length);       // 256

// Traiter les données binaires
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**Comportement :**
- Lit le nombre exact d'octets
- Retourne un buffer (pas une chaîne)
- Avance la position du fichier

---

### Écriture

#### write

Écrit du texte dans le fichier.

**Signature :**
```hemlock
file.write(data: string): i32
```

**Paramètres :**
- `data` - Chaîne à écrire

**Retourne :** Nombre d'octets écrits (i32)

**Exemples :**
```hemlock
let f = open("output.txt", "w");

// Écrire du texte
let written = f.write("Hello, World!\n");
print("Écrit", written, "octets");

// Écritures multiples
f.write("Ligne 1\n");
f.write("Ligne 2\n");
f.write("Ligne 3\n");

f.close();
```

**Comportement :**
- Écrit à la position actuelle du fichier
- Retourne le nombre d'octets écrits
- Avance la position du fichier

**Erreurs :**
- Écriture dans un fichier fermé
- Écriture dans un fichier en lecture seule

---

#### write_bytes

Écrit des données binaires dans le fichier.

**Signature :**
```hemlock
file.write_bytes(data: buffer): i32
```

**Paramètres :**
- `data` - Buffer à écrire

**Retourne :** Nombre d'octets écrits (i32)

**Exemples :**
```hemlock
let f = open("output.bin", "w");

// Créer un buffer
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Écrire le buffer
let written = f.write_bytes(buf);
print("Écrit", written, "octets");

f.close();
```

**Comportement :**
- Écrit le contenu du buffer dans le fichier
- Retourne le nombre d'octets écrits
- Avance la position du fichier

---

### Positionnement

#### seek

Déplace la position du fichier à un décalage d'octets spécifique.

**Signature :**
```hemlock
file.seek(position: i32): i32
```

**Paramètres :**
- `position` - Décalage en octets depuis le début du fichier

**Retourne :** Nouvelle position du fichier (i32)

**Exemples :**
```hemlock
let f = open("data.txt", "r");

// Aller à l'octet 100
f.seek(100);

// Lire depuis cette position
let chunk = f.read(50);

// Revenir au début
f.seek(0);

// Lire depuis le début
let all = f.read();

f.close();
```

**Comportement :**
- Définit la position du fichier au décalage absolu
- Retourne la nouvelle position
- Se positionner au-delà de la fin du fichier est autorisé (crée un trou dans le fichier lors de l'écriture)

---

#### tell

Obtient la position actuelle du fichier.

**Signature :**
```hemlock
file.tell(): i32
```

**Retourne :** Décalage actuel en octets depuis le début du fichier (i32)

**Exemples :**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0 (au début)

f.read(100);
print(f.tell());        // 100 (après lecture)

f.seek(50);
print(f.tell());        // 50 (après positionnement)

f.close();
```

---

### Fermeture

#### close

Ferme le fichier (idempotent).

**Signature :**
```hemlock
file.close(): null
```

**Retourne :** `null`

**Exemples :**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// Sûr d'appeler plusieurs fois
f.close();  // Pas d'erreur
f.close();  // Pas d'erreur
```

**Comportement :**
- Ferme le handle du fichier
- Vide les écritures en attente
- Idempotent (sûr d'appeler plusieurs fois)
- Met la propriété `.closed` à `true`

**Important :** Fermez toujours les fichiers une fois terminé pour éviter les fuites de descripteurs de fichiers.

---

## Propriétés File

### .path

Obtient le chemin du fichier.

**Type :** `string`

**Accès :** Lecture seule

**Exemples :**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

Obtient le mode d'ouverture.

**Type :** `string`

**Accès :** Lecture seule

**Exemples :**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Vérifie si le fichier est fermé.

**Type :** `bool`

**Accès :** Lecture seule

**Exemples :**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Gestion des erreurs

Toutes les opérations sur les fichiers incluent des messages d'erreur appropriés avec contexte :

### Fichier non trouvé
```hemlock
let f = open("missing.txt", "r");
// Erreur: Échec d'ouverture de 'missing.txt': Fichier ou répertoire inexistant
```

### Lecture depuis un fichier fermé
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Erreur: Impossible de lire depuis le fichier fermé 'data.txt'
```

### Écriture dans un fichier en lecture seule
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Erreur: Impossible d'écrire dans le fichier 'readonly.txt' ouvert en mode lecture seule
```

### Utilisation de try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("Erreur fichier:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Modèles de gestion des ressources

### Modèle basique

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Avec gestion des erreurs

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Toujours fermer, même en cas d'erreur
}
```

### Modèle sûr

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... traiter le contenu ...
} catch (e) {
    print("Erreur:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Exemples d'utilisation

### Lire un fichier entier

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### Écrire un fichier texte

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### Ajouter à un fichier

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Entrée de log 1");
append_file("log.txt", "Entrée de log 2");
```

### Lire un fichier binaire

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Lu", binary.length, "octets");
```

### Écrire un fichier binaire

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### Lire un fichier ligne par ligne

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Ligne", i, ":", lines[i]);
    i = i + 1;
}
```

### Copier un fichier

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### Lire un fichier par morceaux

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // Lire 1 Ko à la fois
        if (chunk.length == 0) {
            break;  // Fin du fichier
        }

        // Traiter le morceau
        print("Traitement de", chunk.length, "octets");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## Résumé complet des méthodes

| Méthode       | Signature                | Retourne  | Description                    |
|---------------|--------------------------|-----------|--------------------------------|
| `read`        | `(size?: i32)`           | `string`  | Lire du texte                  |
| `read_bytes`  | `(size: i32)`            | `buffer`  | Lire des données binaires      |
| `write`       | `(data: string)`         | `i32`     | Écrire du texte                |
| `write_bytes` | `(data: buffer)`         | `i32`     | Écrire des données binaires    |
| `seek`        | `(position: i32)`        | `i32`     | Définir la position du fichier |
| `tell`        | `()`                     | `i32`     | Obtenir la position du fichier |
| `close`       | `()`                     | `null`    | Fermer le fichier (idempotent) |

---

## Résumé complet des propriétés

| Propriété | Type     | Accès          | Description                    |
|-----------|----------|----------------|--------------------------------|
| `.path`   | `string` | Lecture seule  | Chemin du fichier              |
| `.mode`   | `string` | Lecture seule  | Mode d'ouverture               |
| `.closed` | `bool`   | Lecture seule  | Si le fichier est fermé        |

---

## Migration depuis l'ancienne API

**Ancienne API (supprimée) :**
- `read_file(path)` - Utilisez `open(path, "r").read()`
- `write_file(path, data)` - Utilisez `open(path, "w").write(data)`
- `append_file(path, data)` - Utilisez `open(path, "a").write(data)`
- `file_exists(path)` - Pas encore de remplacement

**Exemple de migration :**
```hemlock
// Ancien (v0.0)
let content = read_file("data.txt");
write_file("output.txt", content);

// Nouveau (v0.1)
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## Voir aussi

- [Fonctions intégrées](builtins.md) - Fonction `open()`
- [API Memory](memory-api.md) - Type buffer
- [API String](string-api.md) - Méthodes de chaîne pour le traitement de texte
