# E/S de fichiers dans Hemlock

Hemlock fournit une **API objet File** pour les operations sur fichiers avec une gestion des erreurs et des ressources appropriee.

## Table des matieres

- [Vue d'ensemble](#vue-densemble)
- [Ouverture de fichiers](#ouverture-de-fichiers)
- [Methodes de fichier](#methodes-de-fichier)
- [Proprietes de fichier](#proprietes-de-fichier)
- [Gestion des erreurs](#gestion-des-erreurs)
- [Gestion des ressources](#gestion-des-ressources)
- [Reference API complete](#reference-api-complete)
- [Patterns courants](#patterns-courants)
- [Bonnes pratiques](#bonnes-pratiques)

## Vue d'ensemble

L'API objet File fournit :

- **Gestion explicite des ressources** - Les fichiers doivent etre fermes manuellement
- **Plusieurs modes d'ouverture** - Lecture, ecriture, ajout, lecture/ecriture
- **Operations texte et binaires** - Lecture/ecriture de texte et de donnees binaires
- **Support du positionnement** - Acces aleatoire au sein des fichiers
- **Messages d'erreur complets** - Rapport d'erreurs contextuel

**Important :** Les fichiers ne sont pas fermes automatiquement. Vous devez appeler `f.close()` pour eviter les fuites de descripteurs de fichiers.

## Ouverture de fichiers

Utilisez `open(path, mode?)` pour ouvrir un fichier :

```hemlock
let f = open("data.txt", "r");     // Mode lecture (par defaut)
let f2 = open("output.txt", "w");  // Mode ecriture (tronque)
let f3 = open("log.txt", "a");     // Mode ajout
let f4 = open("data.bin", "r+");   // Mode lecture/ecriture
```

### Modes d'ouverture

| Mode | Description | Le fichier doit exister | Tronque | Position |
|------|-------------|-------------------------|---------|----------|
| `"r"` | Lecture (par defaut) | Oui | Non | Debut |
| `"w"` | Ecriture | Non (cree) | Oui | Debut |
| `"a"` | Ajout | Non (cree) | Non | Fin |
| `"r+"` | Lecture et ecriture | Oui | Non | Debut |
| `"w+"` | Lecture et ecriture | Non (cree) | Oui | Debut |
| `"a+"` | Lecture et ajout | Non (cree) | Non | Fin |

### Exemples

**Lecture d'un fichier existant :**
```hemlock
let f = open("config.json", "r");
// ou simplement :
let f = open("config.json");  // "r" est le defaut
```

**Creation d'un nouveau fichier pour ecriture :**
```hemlock
let f = open("output.txt", "w");  // Cree ou tronque
```

**Ajout a un fichier :**
```hemlock
let f = open("log.txt", "a");  // Cree s'il n'existe pas
```

**Mode lecture et ecriture :**
```hemlock
let f = open("data.bin", "r+");  // Fichier existant, peut lire/ecrire
```

## Methodes de fichier

### Lecture

#### read(size?: i32): string

Lire du texte depuis le fichier (parametre size optionnel).

**Sans size (lire tout) :**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // Lire depuis la position actuelle jusqu'a EOF
f.close();
```

**Avec size (lire des octets specifiques) :**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // Lire jusqu'a 1024 octets
let next = f.read(1024);   // Lire les 1024 octets suivants
f.close();
```

**Retourne :** Chaine contenant les donnees lues, ou chaine vide si a EOF

**Exemple - Lecture du fichier entier :**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**Exemple - Lecture par morceaux :**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // Morceaux de 4Ko
    if (chunk == "") { break; }  // EOF atteint
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

Lire des donnees binaires (retourne un buffer).

**Parametres :**
- `size` (i32) - Nombre d'octets a lire

**Retourne :** Buffer contenant les octets lus

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // Lire 256 octets
print(binary.length);  // 256 (ou moins si EOF)

// Acceder aux octets individuels
let first_byte = binary[0];
print(first_byte);

f.close();
```

**Exemple - Lecture du fichier binaire entier :**
```hemlock
let f = open("data.bin", "r");
let size = 10240;  // Taille attendue
let data = f.read_bytes(size);
f.close();

// Traiter les donnees binaires
let i = 0;
while (i < data.length) {
    let byte = data[i];
    // ... traiter l'octet
    i = i + 1;
}
```

### Ecriture

#### write(data: string): i32

Ecrire du texte dans le fichier (retourne les octets ecrits).

**Parametres :**
- `data` (string) - Texte a ecrire

**Retourne :** Nombre d'octets ecrits (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Ecrit " + typeof(written) + " octets");  // "Ecrit 14 octets"
f.close();
```

**Exemple - Ecriture de plusieurs lignes :**
```hemlock
let f = open("output.txt", "w");
f.write("Ligne 1\n");
f.write("Ligne 2\n");
f.write("Ligne 3\n");
f.close();
```

**Exemple - Ajout au fichier de log :**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Application demarree\n");
f.write("[INFO] Utilisateur connecte\n");
f.close();
```

#### write_bytes(data: buffer): i32

Ecrire des donnees binaires (retourne les octets ecrits).

**Parametres :**
- `data` (buffer) - Donnees binaires a ecrire

**Retourne :** Nombre d'octets ecrits (i32)

```hemlock
let f = open("output.bin", "w");

// Creer des donnees binaires
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Ecrit " + typeof(bytes) + " octets");

f.close();
```

**Exemple - Copie de fichier binaire :**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let data = src.read_bytes(1024);
while (data.length > 0) {
    dst.write_bytes(data);
    data = src.read_bytes(1024);
}

src.close();
dst.close();
```

### Positionnement

#### seek(position: i32): i32

Se deplacer a une position specifique (retourne la nouvelle position).

**Parametres :**
- `position` (i32) - Offset en octets depuis le debut du fichier

**Retourne :** Nouvelle position (i32)

```hemlock
let f = open("data.txt", "r");

// Aller a l'octet 100
f.seek(100);

// Lire depuis la position 100
let data = f.read(50);

// Revenir au debut
f.seek(0);

f.close();
```

**Exemple - Acces aleatoire :**
```hemlock
let f = open("records.dat", "r");

// Lire l'enregistrement a l'offset 1000
f.seek(1000);
let record1 = f.read_bytes(100);

// Lire l'enregistrement a l'offset 2000
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Obtenir la position actuelle dans le fichier.

**Retourne :** Offset en octets actuel (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0 (au debut)

f.read(100);
let pos2 = f.tell();  // 100 (apres lecture de 100 octets)

f.seek(500);
let pos3 = f.tell();  // 500 (apres positionnement)

f.close();
```

**Exemple - Mesurer la quantite lue :**
```hemlock
let f = open("data.txt", "r");

let start = f.tell();
let content = f.read();
let end = f.tell();

let bytes_read = end - start;
print("Lu " + typeof(bytes_read) + " octets");

f.close();
```

### Fermeture

#### close()

Fermer le fichier (idempotent, peut etre appele plusieurs fois).

```hemlock
let f = open("data.txt", "r");
// ... utiliser le fichier
f.close();
f.close();  // Sur - pas d'erreur au deuxieme appel
```

**Notes importantes :**
- Toujours fermer les fichiers quand termine pour eviter les fuites de descripteurs
- La fermeture est idempotente - peut etre appelee plusieurs fois en securite
- Apres fermeture, toutes les autres operations provoqueront une erreur
- Utilisez des blocs `finally` pour assurer que les fichiers sont fermes meme en cas d'erreurs

## Proprietes de fichier

Les objets File ont trois proprietes en lecture seule :

### path: string

Le chemin de fichier utilise pour ouvrir le fichier.

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

Le mode avec lequel le fichier a ete ouvert.

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Si le fichier est ferme.

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Exemple - Verification si le fichier est ouvert :**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... traiter le contenu
}

f.close();

if (f.closed) {
    print("Le fichier est maintenant ferme");
}
```

## Gestion des erreurs

Toutes les operations sur fichiers incluent des messages d'erreur avec contexte.

### Erreurs courantes

**Fichier non trouve :**
```hemlock
let f = open("missing.txt", "r");
// Erreur : Echec de l'ouverture de 'missing.txt' : Fichier ou repertoire inexistant
```

**Lecture depuis un fichier ferme :**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Erreur : Impossible de lire depuis le fichier ferme 'data.txt'
```

**Ecriture dans un fichier en lecture seule :**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Erreur : Impossible d'ecrire dans le fichier 'readonly.txt' ouvert en mode lecture seule
```

**Lecture depuis un fichier en ecriture seule :**
```hemlock
let f = open("output.txt", "w");
f.read();
// Erreur : Impossible de lire depuis le fichier 'output.txt' ouvert en mode ecriture seule
```

### Utilisation de try/catch

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Erreur de lecture du fichier : " + e);
}
```

## Gestion des ressources

### Pattern de base

Toujours fermer les fichiers explicitement :

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Avec gestion des erreurs (recommande)

Utilisez `finally` pour assurer que les fichiers sont fermes meme en cas d'erreurs :

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Toujours fermer, meme en cas d'erreur
}
```

### Fichiers multiples

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Pattern de fonction d'aide

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Utilisation :
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## Reference API complete

### Fonctions

| Fonction | Parametres | Retourne | Description |
|----------|-----------|----------|-------------|
| `open(path, mode?)` | path: string, mode?: string | File | Ouvrir un fichier (mode par defaut "r") |

### Methodes

| Methode | Parametres | Retourne | Description |
|---------|-----------|----------|-------------|
| `read(size?)` | size?: i32 | string | Lire du texte (tout ou octets specifiques) |
| `read_bytes(size)` | size: i32 | buffer | Lire des donnees binaires |
| `write(data)` | data: string | i32 | Ecrire du texte, retourne les octets ecrits |
| `write_bytes(data)` | data: buffer | i32 | Ecrire des donnees binaires, retourne les octets ecrits |
| `seek(position)` | position: i32 | i32 | Aller a la position, retourne la nouvelle position |
| `tell()` | - | i32 | Obtenir la position actuelle |
| `close()` | - | null | Fermer le fichier (idempotent) |

### Proprietes (lecture seule)

| Propriete | Type | Description |
|-----------|------|-------------|
| `path` | string | Chemin du fichier |
| `mode` | string | Mode d'ouverture |
| `closed` | bool | Si le fichier est ferme |

## Patterns courants

### Lecture du fichier entier

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### Ecriture du fichier entier

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### Ajout au fichier

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Evenement survenu\n");
```

### Lecture de lignes

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Ligne " + typeof(i) + " : " + lines[i]);
    i = i + 1;
}
```

### Traitement de gros fichiers par morceaux

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // Morceaux de 4Ko
            if (chunk == "") { break; }

            // Traiter le morceau
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Copie de fichier binaire

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### Troncature de fichier

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // Le mode "w" tronque
    f.close();
}

truncate_file("empty_me.txt");
```

### Lecture a un offset specifique

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

### Taille de fichier

```hemlock
fn file_size(path: string): i32 {
    let f = open(path, "r");
    try {
        // Aller a la fin
        let end = f.seek(999999999);  // Grand nombre
        f.seek(0);  // Reinitialiser
        return end;
    } finally {
        f.close();
    }
}

let size = file_size("data.txt");
print("Taille du fichier : " + typeof(size) + " octets");
```

### Lecture/ecriture conditionnelle

```hemlock
fn update_file(path: string, condition, new_content: string) {
    let f = open(path, "r+");
    try {
        let content = f.read();

        if (condition(content)) {
            f.seek(0);  // Revenir au debut
            f.write(new_content);
        }
    } finally {
        f.close();
    }
}
```

## Bonnes pratiques

### 1. Toujours utiliser try/finally

```hemlock
// Bien
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// Mauvais - le fichier pourrait ne pas se fermer en cas d'erreur
let f = open("data.txt", "r");
let content = f.read();
process(content);  // Si cela lance, le fichier fuit
f.close();
```

### 2. Verifier l'etat du fichier avant les operations

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... utiliser le contenu
}

f.close();
```

### 3. Utiliser les modes appropries

```hemlock
// Lecture seulement ? Utiliser "r"
let f = open("config.json", "r");

// Remplacement complet ? Utiliser "w"
let f = open("output.txt", "w");

// Ajout a la fin ? Utiliser "a"
let f = open("log.txt", "a");
```

### 4. Gerer les erreurs gracieusement

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Attention : Impossible de lire " + path + " : " + e);
        return "";
    }
}
```

### 5. Fermer les fichiers dans l'ordre inverse de l'ouverture

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... utiliser les fichiers
} finally {
    // Fermer dans l'ordre inverse
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Eviter de lire entierement les gros fichiers

```hemlock
// Mauvais pour les gros fichiers
let f = open("huge.log", "r");
let content = f.read();  // Charge le fichier entier en memoire
f.close();

// Bien - traiter par morceaux
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Resume

L'API E/S de fichiers de Hemlock fournit :

- ✅ Operations sur fichiers simples et explicites
- ✅ Support texte et binaire
- ✅ Acces aleatoire avec seek/tell
- ✅ Messages d'erreur clairs avec contexte
- ✅ Operation de fermeture idempotente

Rappelez-vous :
- Toujours fermer les fichiers manuellement
- Utiliser try/finally pour la securite des ressources
- Choisir les modes d'ouverture appropries
- Gerer les erreurs gracieusement
- Traiter les gros fichiers par morceaux
