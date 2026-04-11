# Panoramica della Libreria Standard

Hemlock include 53 moduli di libreria standard che coprono programmazione di sistema, I/O, rete, formati dati, concorrenza e altro. Tutti i moduli vengono importati con il prefisso `@stdlib/`.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Categorie dei Moduli

### Utilità Core

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Utilità di asserzione per testing e validazione |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Ispezione task e gestione stack |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Formattazione stringhe stile printf |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Utilità iteratore (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Logger strutturato con livelli e output su file |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Generazione numeri casuali e shuffling |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Utilità stringa estese (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | Framework test stile BDD (describe, test, expect) |

### Matematica e Scienza

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Operazioni matrici dense (multiply, transpose, determinant, inverse) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Ricerca similarità vettoriale usando USearch ANN |

### Memoria e Basso Livello

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Allocatore di memoria arena (bump allocation) |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Operazioni atomiche (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Byte swapping, conversione endian, I/O buffer |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | I/O file memory-mapped |

### File System e I/O

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Operazioni su file e directory (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | I/O file non bloccante via thread pool |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Pattern matching di file |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Manipolazione path (join, dirname, basename, extname) |

### Concorrenza e Async

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Comunicazione inter-processo (pipe, code di messaggi) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Costanti e gestione segnali (SIGINT, SIGTERM, ecc.) |

### Rete

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | Client HTTP (get, post, request con header) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | Socket TCP/UDP (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Socket di dominio Unix (AF_UNIX stream/datagram) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | Parsing e manipolazione URL |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | Client WebSocket |

### Formati Dati

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, accesso via path |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | Parsing e generazione TOML |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | Parsing e generazione YAML |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | Parsing e generazione CSV |

### Codifica e Crittografia

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, hex, codifica URL |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | Crittografia AES, firma RSA, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Elaborazione Testo

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Espressioni regolari (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Rendering template compatibile Jinja2 |

### Data, Ora e Versioning

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | Classe DateTime, formattazione, parsing |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Timestamp, sleep, misurazione clock |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Parsing e confronto versioni semantiche |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | Generazione UUID v4 e v7 |

### Sistema e Ambiente

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Parsing argomenti da riga di comando |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Variabili d'ambiente, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Rilevamento piattaforma, conteggio CPU, hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Esecuzione comandi shell e escaping argomenti |

### Terminale e UI

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | Colori ANSI, stili e controllo cursore |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Input terminale raw e rilevamento tasti |

### Database

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | Database SQLite, query, exec, transazioni |

### FFI e Interop

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | Gestione callback FFI e costanti di tipo |

### Utilità

| Modulo | Import | Descrizione |
|--------|--------|-------------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Logica retry con backoff esponenziale |

---

## Esempi Rapidi

### Leggere e analizzare un file di configurazione

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connessione a " + db_host);
```

### Richiesta HTTP con JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Elaborazione concorrente

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Hash e codifica

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Rendering template

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Home", "Chi Siamo", "Contatti"] });
```

---

## Vedi Anche

- [Riferimento Funzioni Integrate](./builtins.md) - funzioni disponibili senza import
- [Guida alla Migrazione (v2.0)](../migration-2.0.md) - builtin spostati nella stdlib nella v2.0
- Documentazione individuale dei moduli in [`stdlib/docs/`](../../stdlib/docs/)
