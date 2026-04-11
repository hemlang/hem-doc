# Vue d'ensemble de la bibliotheque standard

Hemlock est livre avec 53 modules de bibliotheque standard couvrant la programmation systeme, les E/S, le reseau, les formats de donnees, la concurrence et plus encore. Tous les modules sont importes avec le prefixe `@stdlib/`.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Categories de modules

### Utilitaires de base

| Module | Import | Description |
|--------|--------|-------------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Utilitaires d'assertion pour les tests et la validation |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Inspection de taches et gestion de pile |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Formatage de chaines style printf |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Utilitaires d'iterateur (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Logger structure avec niveaux et sortie fichier |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Generation de nombres aleatoires et melange |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Utilitaires de chaines etendus (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | Framework de test style BDD (describe, test, expect) |

### Mathematiques et sciences

| Module | Import | Description |
|--------|--------|-------------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Operations sur matrices denses (multiplier, transposer, determinant, inverse) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Recherche de similarite vectorielle avec USearch ANN |

### Memoire et bas niveau

| Module | Import | Description |
|--------|--------|-------------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Allocateur memoire arena (allocation par bump) |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Operations atomiques (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Echange d'octets, conversion d'endianness, E/S buffer |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | E/S fichier mappee en memoire |

### Systeme de fichiers et E/S

| Module | Import | Description |
|--------|--------|-------------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Operations sur fichiers et repertoires (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | E/S fichier non bloquante via pool de threads |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Correspondance de motifs de fichiers |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Manipulation de chemins (join, dirname, basename, extname) |

### Concurrence et async

| Module | Import | Description |
|--------|--------|-------------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Communication inter-processus (pipes, files de messages) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Constantes et gestion de signaux (SIGINT, SIGTERM, etc.) |

### Reseau

| Module | Import | Description |
|--------|--------|-------------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | Client HTTP (get, post, request avec en-tetes) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | Sockets TCP/UDP (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Sockets de domaine Unix (AF_UNIX stream/datagram) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | Analyse et manipulation d'URL |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | Client WebSocket |

### Formats de donnees

| Module | Import | Description |
|--------|--------|-------------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, acces par chemin |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | Analyse et generation TOML |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | Analyse et generation YAML |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | Analyse et generation CSV |

### Encodage et cryptographie

| Module | Import | Description |
|--------|--------|-------------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, hex, encodage URL |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | Chiffrement AES, signature RSA, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Traitement de texte

| Module | Import | Description |
|--------|--------|-------------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Expressions regulieres (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Rendu de modeles compatible Jinja2 |

### Date, heure et versionnage

| Module | Import | Description |
|--------|--------|-------------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | Classe DateTime, formatage, analyse |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Horodatages, sleep, mesure d'horloge |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Analyse et comparaison de versions semantiques |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | Generation d'UUID v4 et v7 |

### Systeme et environnement

| Module | Import | Description |
|--------|--------|-------------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Analyse des arguments de ligne de commande |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Variables d'environnement, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Detection de plateforme, nombre de CPU, hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Execution de commandes shell et echappement d'arguments |

### Terminal et interface

| Module | Import | Description |
|--------|--------|-------------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | Couleurs, styles ANSI et controle du curseur |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Entree terminal brute et detection de touches |

### Base de donnees

| Module | Import | Description |
|--------|--------|-------------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | Base de donnees SQLite, query, exec, transactions |

### FFI et interoperabilite

| Module | Import | Description |
|--------|--------|-------------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | Gestion des callbacks FFI et constantes de type |

### Utilitaire

| Module | Import | Description |
|--------|--------|-------------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Logique de reessai avec backoff exponentiel |

---

## Exemples rapides

### Lire et parser un fichier de configuration

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connexion a " + db_host);
```

### Requete HTTP avec JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Traitement concurrent

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Hachage et encodage

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Rendu de modele

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Accueil", "A propos", "Contact"] });
```

---

## Voir aussi

- [Reference des fonctions integrees](./builtins.md) -- fonctions disponibles sans imports
- [Guide de migration (v2.0)](../migration-2.0.md) -- builtins deplaces vers la stdlib dans v2.0
- Documentation individuelle des modules dans [`stdlib/docs/`](../../stdlib/docs/)
