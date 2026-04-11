# Standardbibliothek-Überblick

Hemlock wird mit 53 Standardbibliotheks-Modulen ausgeliefert, die Systemprogrammierung, I/O, Netzwerk, Datenformate, Nebenläufigkeit und mehr abdecken. Alle Module werden mit dem `@stdlib/`-Präfix importiert.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Modulkategorien

### Kern-Utilities

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Assertions-Utilities für Testen und Validierung |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Task-Inspektion und Stack-Verwaltung |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Printf-artige String-Formatierung |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Iterator-Utilities (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Strukturierter Logger mit Stufen und Dateiausgabe |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Zufallszahlengenerierung und Mischen |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Erweiterte String-Utilities (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | BDD-artiges Test-Framework (describe, test, expect) |

### Mathematik & Wissenschaft

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Dichte Matrixoperationen (multiply, transpose, determinant, inverse) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Vektor-Ähnlichkeitssuche mit USearch ANN |

### Speicher & Low-Level

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Arena (Bump)-Speicherallokator |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Atomare Operationen (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Byte-Swapping, Endian-Konvertierung, Buffer-I/O |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | Memory-mapped Datei-I/O |

### Dateisystem & I/O

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Datei- und Verzeichnisoperationen (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | Nicht-blockierende Datei-I/O via Thread-Pool |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Datei-Musterabgleich |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Pfad-Manipulation (join, dirname, basename, extname) |

### Nebenläufigkeit & Async

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Inter-Prozess-Kommunikation (Pipes, Nachrichtenwarteschlangen) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Signalkonstanten und -behandlung (SIGINT, SIGTERM, etc.) |

### Netzwerk

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | HTTP-Client (get, post, request mit Headers) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | TCP/UDP-Sockets (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Unix-Domain-Sockets (AF_UNIX Stream/Datagramm) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | URL-Parsing und -Manipulation |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | WebSocket-Client |

### Datenformate

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, Pfadzugriff |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | TOML-Parsing und -Generierung |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | YAML-Parsing und -Generierung |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | CSV-Parsing und -Generierung |

### Kodierung & Kryptografie

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, Hex, URL-Kodierung |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | AES-Verschlüsselung, RSA-Signierung, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Textverarbeitung

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Reguläre Ausdrücke (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Jinja2-kompatibles Template-Rendering |

### Datum, Zeit & Versionierung

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | DateTime-Klasse, Formatierung, Parsing |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Zeitstempel, sleep, Zeitmessung |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Semantische Versions-Parsing und -Vergleich |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | UUID v4 und v7 Generierung |

### System & Umgebung

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Kommandozeilenargument-Parsing |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Umgebungsvariablen, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Plattformerkennung, CPU-Anzahl, Hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Shell-Befehlsausführung und Argument-Escaping |

### Terminal & UI

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | ANSI-Farben, -Stile und Cursor-Steuerung |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Rohe Terminal-Eingabe und Tastenerkennung |

### Datenbank

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | SQLite-Datenbank, query, exec, Transaktionen |

### FFI & Interop

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | FFI-Callback-Verwaltung und Typkonstanten |

### Utility

| Modul | Import | Beschreibung |
|-------|--------|--------------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Wiederholungslogik mit exponentiellem Backoff |

---

## Schnellbeispiele

### Konfigurationsdatei lesen und parsen

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Verbinde mit " + db_host);
```

### HTTP-Anfrage mit JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Nebenläufige Verarbeitung

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Hashen und kodieren

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Template-Rendering

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menü", items: ["Start", "Über", "Kontakt"] });
```

---

## Siehe auch

- [Eingebaute Funktionen-Referenz](./builtins.md) -- Funktionen ohne Imports verfügbar
- [Migrationsleitfaden (v2.0)](../migration-2.0.md) -- Builtins in v2.0 in die Stdlib verschoben
- Individuelle Modul-Dokumentation in [`stdlib/docs/`](../../stdlib/docs/)
