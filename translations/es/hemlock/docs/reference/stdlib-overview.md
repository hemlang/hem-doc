# Descripcion General de la Biblioteca Estandar

Hemlock incluye 53 modulos de biblioteca estandar que cubren programacion de sistemas, E/S, redes, formatos de datos, concurrencia y mas. Todos los modulos se importan con el prefijo `@stdlib/`.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Categorias de Modulos

### Utilidades Principales

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Utilidades de asercion para pruebas y validacion |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Inspeccion de tareas y gestion de pila |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Formateo de cadenas estilo printf |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Utilidades de iterador (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Logger estructurado con niveles y salida a archivo |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Generacion de numeros aleatorios y mezcla |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Utilidades extendidas de string (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | Framework de pruebas estilo BDD (describe, test, expect) |

### Matematicas y Ciencia

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Operaciones de matrices densas (multiply, transpose, determinant, inverse) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Busqueda de similitud vectorial usando USearch ANN |

### Memoria y Bajo Nivel

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Asignador de memoria arena (asignacion bump) |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Operaciones atomicas (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Intercambio de bytes, conversion endian, E/S de buffer |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | E/S de archivos mapeados en memoria |

### Sistema de Archivos y E/S

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Operaciones de archivos y directorios (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | E/S de archivos no bloqueante via pool de hilos |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Coincidencia de patrones de archivos |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Manipulacion de rutas (join, dirname, basename, extname) |

### Concurrencia y Async

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Comunicacion entre procesos (pipes, colas de mensajes) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Constantes de senales y manejo (SIGINT, SIGTERM, etc.) |

### Redes

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | Cliente HTTP (get, post, request con headers) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | Sockets TCP/UDP (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Sockets de dominio Unix (stream/datagram AF_UNIX) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | Analisis y manipulacion de URL |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | Cliente WebSocket |

### Formatos de Datos

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, acceso por ruta |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | Analisis y generacion de TOML |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | Analisis y generacion de YAML |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | Analisis y generacion de CSV |

### Codificacion y Criptografia

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, hex, codificacion URL |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | Cifrado AES, firma RSA, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Procesamiento de Texto

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Expresiones regulares (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Renderizado de plantillas compatible con Jinja2 |

### Fecha, Hora y Versionado

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | Clase DateTime, formateo, analisis |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Marcas de tiempo, sleep, medicion de reloj |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Analisis y comparacion de versiones semanticas |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | Generacion de UUID v4 y v7 |

### Sistema y Entorno

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Analisis de argumentos de linea de comandos |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Variables de entorno, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Deteccion de plataforma, conteo de CPU, hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Ejecucion de comandos shell y escape de argumentos |

### Terminal e Interfaz

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | Colores, estilos y control de cursor ANSI |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Entrada de terminal cruda y deteccion de teclas |

### Base de Datos

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | Base de datos SQLite, query, exec, transacciones |

### FFI e Interoperabilidad

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | Gestion de callbacks FFI y constantes de tipo |

### Utilidad

| Modulo | Import | Descripcion |
|--------|--------|-------------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Logica de reintento con backoff exponencial |

---

## Ejemplos Rapidos

### Leer y analizar un archivo de configuracion

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connecting to " + db_host);
```

### Solicitud HTTP con JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Procesamiento concurrente

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Hash y codificacion

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Renderizado de plantillas

```hemlock
import { render } from "@stdlib/jinja";

let html = render(`
<h1>{{ title }}</h1>
<ul>
{% for item in items %}<li>{{ item }}</li>
{% endfor %}</ul>
`, { title: "Menu", items: ["Home", "About", "Contact"] });
```

---

## Ver Tambien

- [Referencia de Funciones Integradas](./builtins.md) -- funciones disponibles sin importaciones
- [Guia de Migracion (v2.0)](../migration-2.0.md) -- builtins movidos a stdlib en v2.0
- Documentacion individual de modulos en [`stdlib/docs/`](../../stdlib/docs/)
