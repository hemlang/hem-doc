# Objets

Hemlock implemente des objets de style JavaScript avec allocation sur le tas, champs dynamiques, methodes et typage canard. Les objets sont des structures de donnees flexibles qui combinent donnees et comportement.

## Apercu

```hemlock
// Objet anonyme
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// Objet avec methodes
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Litteraux d'objet

### Syntaxe basique

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**Syntaxe :**
- Les accolades `{}` enclosent l'objet
- Paires cle-valeur separees par des virgules
- Les cles sont des identifiants (pas de guillemets necessaires)
- Les valeurs peuvent etre de n'importe quel type

### Objets vides

```hemlock
let obj = {};  // Objet vide

// Ajouter des champs plus tard
obj.name = "Alice";
obj.age = 30;
```

### Objets imbriques

```hemlock
let user = {
    info: {
        name: "Bob",
        age: 25
    },
    active: true,
    settings: {
        theme: "dark",
        notifications: true
    }
};

print(user.info.name);           // "Bob"
print(user.settings.theme);      // "dark"
```

### Types de valeur mixtes

```hemlock
let mixed = {
    number: 42,
    text: "hello",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### Syntaxe de propriete abregee

Quand un nom de variable correspond au nom de propriete, utilisez la syntaxe abregee :

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Abrege : { name } est equivalent a { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Melanger abrege avec proprietes regulieres :**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### Operateur spread

L'operateur spread (`...`) copie tous les champs d'un objet dans un autre :

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Remplacer des valeurs avec spread :**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (remplace)
print(custom.size);   // "medium" (depuis defaults)
print(custom.debug);  // false (depuis defaults)
```

**Spreads multiples (les spreads ulterieurs remplacent les precedents) :**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// Le spread ulterieur remplace le precedent
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**Combiner abrege et spread :**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**Modele de remplacement de configuration :**
```hemlock
let defaultConfig = {
    debug: false,
    timeout: 30,
    retries: 3
};

let prodConfig = { ...defaultConfig, timeout: 60 };
let devConfig = { ...defaultConfig, debug: true };

print(prodConfig.timeout);  // 60
print(devConfig.debug);     // true
```

**Note :** Le spread effectue une copie superficielle. Les objets imbriques partagent les references :
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (meme reference que nested.inner)
```

## Acces aux champs

### Notation point

```hemlock
let person = { name: "Alice", age: 30 };

// Lire le champ
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Modifier le champ
person.age = 31;
print(person.age);           // 31
```

### Ajout dynamique de champs

Ajouter de nouveaux champs a l'execution :

```hemlock
let person = { name: "Alice" };

// Ajouter un nouveau champ
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Suppression de champs

**Note :** La suppression de champs n'est pas actuellement supportee. Definissez a `null` a la place :

```hemlock
let obj = { x: 10, y: 20 };

// Impossible de supprimer des champs (non supporte)
// obj.x = undefined;  // Pas de 'undefined' en Hemlock

// Solution : Definir a null
obj.x = null;
```

## Methodes et `self`

### Definir des methodes

Les methodes sont des fonctions stockees dans les champs d'objet :

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
    decrement: fn() {
        self.count = self.count - 1;
    },
    get: fn() {
        return self.count;
    }
};
```

### Le mot-cle `self`

Quand une fonction est appelee comme methode, `self` est automatiquement lie a l'objet :

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self fait reference a counter
    }
};

counter.increment();  // self est lie a counter
print(counter.count);  // 1
```

**Fonctionnement :**
- Les appels de methode sont detectes en verifiant si l'expression de fonction est un acces de propriete
- `self` est automatiquement lie a l'objet au moment de l'appel
- `self` est en lecture seule (impossible de reassigner `self` lui-meme)

### Detection d'appel de methode

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Appele comme methode - self est lie
print(obj.method());  // 10

// Appele comme fonction - self est null (erreur)
let f = obj.method;
print(f());  // ERREUR : self is not defined
```

### Methodes avec parametres

```hemlock
let calculator = {
    result: 0,
    add: fn(x) {
        self.result = self.result + x;
    },
    multiply: fn(x) {
        self.result = self.result * x;
    },
    get: fn() {
        return self.result;
    }
};

calculator.add(5);
calculator.multiply(2);
print(calculator.get());  // 10
```

## Definitions de type avec `define`

### Definition de type basique

Definir les formes d'objet avec `define` :

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Creer un objet et assigner a une variable typee
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Le typage canard valide la structure

print(typeof(typed_p));  // "Person"
```

**Ce que fait `define` :**
- Declare un type avec des champs requis
- Active la validation par typage canard
- Definit le nom de type de l'objet pour `typeof()`

### Typage canard

Les objets sont valides contre `define` en utilisant la **compatibilite structurelle** :

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK : A tous les champs requis
let p1: Person = { name: "Alice", age: 30 };

// OK : Les champs supplementaires sont autorises
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// ERREUR : Champ requis 'age' manquant
let p3: Person = { name: "Carol" };

// ERREUR : Mauvais type pour 'age'
let p4: Person = { name: "Dave", age: "trente" };
```

**Regles du typage canard :**
- Tous les champs requis doivent etre presents
- Les types de champs doivent correspondre
- Les champs supplementaires sont autorises et preserves
- La validation a lieu au moment de l'assignation

### Champs optionnels

Les champs peuvent etre optionnels avec des valeurs par defaut :

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Optionnel avec valeur par defaut
    nickname?: string,   // Optionnel, par defaut null
}

// Objet avec seulement les champs requis
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (defaut applique)
print(typed_p.nickname);  // null (pas de defaut)

// Peut remplacer les champs optionnels
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (remplace)
```

**Syntaxe des champs optionnels :**
- `field?: default_value` - Optionnel avec defaut
- `field?: type` - Optionnel avec annotation de type, par defaut null
- Les champs optionnels sont ajoutes lors du typage canard si absents

### Verification de type

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // La verification de type a lieu ici

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (l'original est toujours anonyme)
```

**Quand la verification de type a lieu :**
- Au moment de l'assignation a une variable typee
- Valide que tous les champs requis sont presents
- Valide que les types de champs correspondent (avec conversions implicites)
- Definit le nom de type de l'objet

## Signatures de methode dans Define

Les blocs define peuvent specifier des signatures de methode, creant des contrats de type interface :

### Methodes requises

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Signature de methode requise
}

// Les objets doivent fournir la methode requise
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Methodes optionnelles

```hemlock
define Serializable {
    fn serialize(): string;       // Requise
    fn pretty?(): string;         // Methode optionnelle (peut etre absente)
}
```

### Le type `Self`

`Self` fait reference au type en cours de definition, permettant les definitions de type recursives :

```hemlock
define Cloneable {
    fn clone(): Self;  // Retourne le meme type que l'objet
}

define Comparable {
    fn compare(other: Self): i32;  // Prend le meme type en parametre
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Melange de champs et methodes

```hemlock
define Entity {
    id: i32,
    name: string,
    fn validate(): bool;
    fn serialize(): string;
}

let user: Entity = {
    id: 1,
    name: "Alice",
    validate: fn() { return self.id > 0 && self.name != ""; },
    serialize: fn() { return '{"id":' + self.id + ',"name":"' + self.name + '"}'; }
};
```

## Types composes (types d'intersection)

Les types composes utilisent `&` pour exiger qu'un objet satisfasse plusieurs definitions de type :

### Types composes basiques

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Type compose : l'objet doit satisfaire TOUS les types
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Parametres de fonction avec types composes

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " a " + p.age + " ans");
}

greet({ name: "Bob", age: 25, city: "NYC" });  // Champs supplementaires OK
```

### Trois types ou plus

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Alias de type pour types composes

```hemlock
// Creer un alias nomme pour un type compose
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Typage canard avec composes :** Les champs supplementaires sont toujours autorises - l'objet doit juste avoir au moins les champs requis par tous les types composants.

## Serialisation JSON

### Serialiser en JSON

Convertir des objets en chaines JSON :

```hemlock
// obj.serialize() - Convertir l'objet en chaine JSON
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Objets imbriques
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Deserialiser depuis JSON

Analyser des chaines JSON vers des objets :

```hemlock
// json.deserialize() - Analyser chaine JSON vers objet
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Detection de cycle

Les references circulaires sont detectees et causent des erreurs :

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Creer une reference circulaire

obj.serialize();  // ERREUR : serialize() detected circular reference
```

### Types supportes

La serialisation JSON supporte :

- **Nombres** : i8-i32, u8-u32, f32, f64
- **Booleens** : true, false
- **Chaines** : Avec sequences d'echappement
- **Null** : valeur null
- **Objets** : Objets imbriques
- **Tableaux** : Tableaux imbriques

**Non supporte :**
- Fonctions (omises silencieusement)
- Pointeurs (erreur)
- Buffers (erreur)

### Gestion des erreurs

La serialisation et deserialisation peuvent lever des erreurs :

```hemlock
// JSON invalide leve une erreur
try {
    let bad = "pas du json valide".deserialize();
} catch (e) {
    print("Erreur d'analyse :", e);
}

// Les pointeurs ne peuvent pas etre serialises
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Erreur de serialisation :", e);
}
```

### Exemple aller-retour

Exemple complet de serialisation et deserialisation :

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Creer et serialiser
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Deserialiser
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Fonctions integrees

### `typeof(value)`

Retourne le nom du type sous forme de chaine :

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Valeurs de retour :**
- Objets anonymes : `"object"`
- Objets types : Nom de type personnalise (ex. `"Person"`)

## Details d'implementation

### Modele memoire

- **Alloue sur le tas** - Tous les objets sont alloues sur le tas
- **Copie superficielle** - L'assignation copie la reference, pas l'objet
- **Champs dynamiques** - Stockes comme tableaux dynamiques de paires nom/valeur
- **Compte par reference** - Les objets sont automatiquement liberes quand la portee se termine

### Semantique de reference

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copie superficielle (meme reference)

obj2.x = 20;
print(obj1.x);  // 20 (les deux font reference au meme objet)
```

### Stockage des methodes

Les methodes sont simplement des fonctions stockees dans des champs :

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method est une fonction stockee dans obj.method
print(typeof(obj.method));  // "function"
```

## Modeles courants

### Modele : Fonction constructeur

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Salut, je suis " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Salut, je suis Alice"
```

### Modele : Constructeur d'objet (Builder)

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Permettre le chainage
        },

        setAge: fn(a) {
            self.age = a;
            return self;
        },

        build: fn() {
            return { name: self.name, age: self.age };
        }
    };
}

let person = PersonBuilder()
    .setName("Alice")
    .setAge(30)
    .build();
```

### Modele : Objet d'etat

```hemlock
let state = {
    status: "idle",
    data: null,
    error: null,

    setState: fn(new_status) {
        self.status = new_status;
    },

    setData: fn(new_data) {
        self.data = new_data;
        self.status = "success";
    },

    setError: fn(err) {
        self.error = err;
        self.status = "error";
    }
};
```

### Modele : Objet de configuration

```hemlock
let config = {
    defaults: {
        timeout: 30,
        retries: 3,
        debug: false
    },

    get: fn(key) {
        if (self.defaults[key] != null) {
            return self.defaults[key];
        }
        return null;
    },

    set: fn(key, value) {
        self.defaults[key] = value;
    }
};
```

## Bonnes pratiques

1. **Utilisez `define` pour la structure** - Documentez les formes d'objet attendues
2. **Preferez les fonctions usine** - Creez des objets avec des constructeurs
3. **Gardez les objets simples** - N'imbriquez pas trop profondement
4. **Documentez l'utilisation de `self`** - Rendez le comportement des methodes clair
5. **Validez a l'assignation** - Utilisez le typage canard pour detecter les erreurs tot
6. **Evitez les references circulaires** - Causera des erreurs de serialisation
7. **Utilisez les champs optionnels** - Fournissez des defauts raisonnables

## Pieges courants

### Piege : Reference vs. valeur

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copie superficielle

obj2.x = 20;
print(obj1.x);  // 20 (surprise ! les deux ont change)

// Pour eviter : Creer un nouvel objet
let obj3 = { x: obj1.x };  // Copie profonde (manuelle)
```

### Piege : `self` dans les appels non-methode

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Fonctionne : Appele comme methode
print(obj.method());  // 10

// ERREUR : Appele comme fonction
let f = obj.method;
print(f());  // ERREUR : self is not defined
```

### Piege : Pointeurs bruts dans les objets

```hemlock
// Les objets sont auto-liberes, mais les pointeurs bruts a l'interieur NE le sont PAS
fn create_objects() {
    let obj = { data: alloc(1000) };  // ptr brut necessite free manuel
    // obj est auto-libere quand la portee se termine, mais obj.data fuit !
}

// Solution : Liberer les pointeurs bruts avant la sortie de portee
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... utiliser obj.data ...
    free(obj.data);  // Liberer le pointeur brut explicitement
}  // obj lui-meme est auto-libere
```

### Piege : Confusion de type

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// ERREUR : Champ requis 'y' manquant
let p: Point = obj;
```

## Exemples

### Exemple : Mathematiques vectorielles

```hemlock
fn createVector(x, y) {
    return {
        x: x,
        y: y,

        add: fn(other) {
            return createVector(
                self.x + other.x,
                self.y + other.y
            );
        },

        length: fn() {
            return sqrt(self.x * self.x + self.y * self.y);
        },

        toString: fn() {
            return "(" + typeof(self.x) + ", " + typeof(self.y) + ")";
        }
    };
}

let v1 = createVector(3, 4);
let v2 = createVector(1, 2);
let v3 = v1.add(v2);

print(v3.toString());  // "(4, 6)"
```

### Exemple : Base de donnees simple

```hemlock
fn createDatabase() {
    let records = [];
    let next_id = 1;

    return {
        insert: fn(data) {
            let record = { id: next_id, data: data };
            records.push(record);
            next_id = next_id + 1;
            return record.id;
        },

        find: fn(id) {
            let i = 0;
            while (i < records.length) {
                if (records[i].id == id) {
                    return records[i];
                }
                i = i + 1;
            }
            return null;
        },

        count: fn() {
            return records.length;
        }
    };
}

let db = createDatabase();
let id = db.insert({ name: "Alice", age: 30 });
let record = db.find(id);
print(record.data.name);  // "Alice"
```

### Exemple : Emetteur d'evenements

```hemlock
fn createEventEmitter() {
    let listeners = {};

    return {
        on: fn(event, handler) {
            if (listeners[event] == null) {
                listeners[event] = [];
            }
            listeners[event].push(handler);
        },

        emit: fn(event, data) {
            if (listeners[event] != null) {
                let i = 0;
                while (i < listeners[event].length) {
                    listeners[event][i](data);
                    i = i + 1;
                }
            }
        }
    };
}

let emitter = createEventEmitter();

emitter.on("message", fn(data) {
    print("Recu : " + data);
});

emitter.emit("message", "Bonjour !");
```

## Limitations

Limitations actuelles :

- **Pas de copie profonde** - Doit copier manuellement les objets imbriques (spread est superficiel)
- **Pas de passage par valeur** - Les objets sont toujours passes par reference
- **Pas de proprietes calculees** - Pas de syntaxe `{[key]: value}`
- **`self` est en lecture seule** - Impossible de reassigner `self` dans les methodes
- **Pas de suppression de propriete** - Impossible de supprimer des champs une fois ajoutes

**Note :** Les objets sont comptes par reference et automatiquement liberes quand la portee se termine. Voir [Gestion de la memoire](memory.md#internal-reference-counting) pour les details.

## Sujets connexes

- [Fonctions](functions.md) - Les methodes sont des fonctions stockees dans les objets
- [Tableaux](arrays.md) - Les tableaux sont aussi similaires a des objets
- [Types](types.md) - Typage canard et definitions de type
- [Gestion des erreurs](error-handling.md) - Lever des objets d'erreur

## Voir aussi

- **Typage canard** : Voir section "Objects" de CLAUDE.md pour les details du typage canard
- **JSON** : Voir CLAUDE.md pour les details de serialisation JSON
- **Memoire** : Voir [Memoire](memory.md) pour l'allocation d'objet
