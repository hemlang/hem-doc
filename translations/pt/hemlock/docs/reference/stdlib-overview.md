# Visao Geral da Biblioteca Padrao

Hemlock inclui 53 modulos de biblioteca padrao cobrindo programacao de sistemas, I/O, rede, formatos de dados, concorrencia e mais. Todos os modulos sao importados com o prefixo `@stdlib/`.

```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { parse, stringify } from "@stdlib/json";
import { ThreadPool } from "@stdlib/async";
```

---

## Categorias de Modulos

### Utilitarios Core

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`assert`](../../stdlib/docs/assert.md) | `@stdlib/assert` | Utilitarios de assercao para teste e validacao |
| [`collections`](../../stdlib/docs/collections.md) | `@stdlib/collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| [`debug`](../../stdlib/docs/debug.md) | `@stdlib/debug` | Inspecao de tarefas e gerenciamento de pilha |
| [`fmt`](../../stdlib/docs/fmt.md) | `@stdlib/fmt` | Formatacao de string estilo printf |
| [`iter`](../../stdlib/docs/iter.md) | `@stdlib/iter` | Utilitarios de iterador (range, enumerate, zip, chain) |
| [`logging`](../../stdlib/docs/logging.md) | `@stdlib/logging` | Logger estruturado com niveis e saida para arquivo |
| [`random`](../../stdlib/docs/random.md) | `@stdlib/random` | Geracao de numeros aleatorios e embaralhamento |
| [`strings`](../../stdlib/docs/strings.md) | `@stdlib/strings` | Utilitarios de string estendidos (pad, reverse, lines) |
| [`testing`](../../stdlib/docs/testing.md) | `@stdlib/testing` | Framework de testes estilo BDD (describe, test, expect) |

### Matematica e Ciencia

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`math`](../../stdlib/docs/math.md) | `@stdlib/math` | sin, cos, sqrt, pow, rand, PI, E, divi |
| [`decimal`](../../stdlib/docs/decimal.md) | `@stdlib/decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| [`matrix`](../../stdlib/docs/matrix.md) | `@stdlib/matrix` | Operacoes de matriz densa (multiplicar, transpor, determinante, inversa) |
| [`vector`](../../stdlib/docs/vector.md) | `@stdlib/vector` | Busca de similaridade vetorial usando USearch ANN |

### Memoria e Baixo Nivel

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`arena`](../../stdlib/docs/arena.md) | `@stdlib/arena` | Alocador de memoria arena (bump allocation) |
| [`atomic`](../../stdlib/docs/atomic.md) | `@stdlib/atomic` | Operacoes atomicas (load, store, add, CAS, fence) |
| [`bytes`](../../stdlib/docs/bytes.md) | `@stdlib/bytes` | Troca de bytes, conversao de endianness, I/O de buffer |
| [`mmap`](../../stdlib/docs/mmap.md) | `@stdlib/mmap` | I/O de arquivo com mapeamento de memoria |

### Sistema de Arquivos e I/O

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`fs`](../../stdlib/docs/fs.md) | `@stdlib/fs` | Operacoes de arquivo e diretorio (open, read_file, write_file, list_dir) |
| [`async_fs`](../../stdlib/docs/async_fs.md) | `@stdlib/async_fs` | I/O de arquivo nao-bloqueante via pool de threads |
| [`glob`](../../stdlib/docs/glob.md) | `@stdlib/glob` | Matching de padroes de arquivo |
| [`path`](../../stdlib/docs/path.md) | `@stdlib/path` | Manipulacao de caminhos (join, dirname, basename, extname) |

### Concorrencia e Async

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`async`](../../stdlib/docs/async.md) | `@stdlib/async` | ThreadPool, parallel_map |
| [`ipc`](../../stdlib/docs/ipc.md) | `@stdlib/ipc` | Comunicacao entre processos (pipes, filas de mensagens) |
| [`signal`](../../stdlib/docs/signal.md) | `@stdlib/signal` | Constantes e tratamento de sinais (SIGINT, SIGTERM, etc.) |

### Rede

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`http`](../../stdlib/docs/http.md) | `@stdlib/http` | Cliente HTTP (get, post, request com headers) |
| [`net`](../../stdlib/docs/net.md) | `@stdlib/net` | Sockets TCP/UDP (TcpListener, TcpStream, UdpSocket) |
| [`unix_socket`](../../stdlib/docs/unix_socket.md) | `@stdlib/unix_socket` | Sockets de dominio Unix (AF_UNIX stream/datagram) |
| [`url`](../../stdlib/docs/url.md) | `@stdlib/url` | Parsing e manipulacao de URL |
| [`websocket`](../../stdlib/docs/websocket.md) | `@stdlib/websocket` | Cliente WebSocket |

### Formatos de Dados

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`json`](../../stdlib/docs/json.md) | `@stdlib/json` | JSON parse, stringify, pretty, acesso por caminho |
| [`toml`](../../stdlib/docs/toml.md) | `@stdlib/toml` | Parsing e geracao de TOML |
| [`yaml`](../../stdlib/docs/yaml.md) | `@stdlib/yaml` | Parsing e geracao de YAML |
| [`csv`](../../stdlib/docs/csv.md) | `@stdlib/csv` | Parsing e geracao de CSV |

### Codificacao e Criptografia

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`encoding`](../../stdlib/docs/encoding.md) | `@stdlib/encoding` | Base64, Base32, hex, codificacao de URL |
| [`hash`](../../stdlib/docs/hash.md) | `@stdlib/hash` | SHA-1, SHA-256, SHA-512, MD5, CRC32, DJB2 |
| [`crypto`](../../stdlib/docs/crypto.md) | `@stdlib/crypto` | Criptografia AES, assinatura RSA, random_bytes |
| [`compression`](../../stdlib/docs/compression.md) | `@stdlib/compression` | gzip, gunzip, deflate |

### Processamento de Texto

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`regex`](../../stdlib/docs/regex.md) | `@stdlib/regex` | Expressoes regulares (POSIX ERE) |
| [`jinja`](../../stdlib/docs/jinja.md) | `@stdlib/jinja` | Renderizacao de templates compativel com Jinja2 |

### Data, Hora e Versionamento

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`datetime`](../../stdlib/docs/datetime.md) | `@stdlib/datetime` | Classe DateTime, formatacao, parsing |
| [`time`](../../stdlib/docs/time.md) | `@stdlib/time` | Timestamps, sleep, medicao de clock |
| [`semver`](../../stdlib/docs/semver.md) | `@stdlib/semver` | Parsing e comparacao de versao semantica |
| [`uuid`](../../stdlib/docs/uuid.md) | `@stdlib/uuid` | Geracao de UUID v4 e v7 |

### Sistema e Ambiente

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`args`](../../stdlib/docs/args.md) | `@stdlib/args` | Parsing de argumentos de linha de comando |
| [`env`](../../stdlib/docs/env.md) | `@stdlib/env` | Variaveis de ambiente, exit, get_pid |
| [`os`](../../stdlib/docs/os.md) | `@stdlib/os` | Deteccao de plataforma, contagem de CPUs, hostname |
| [`process`](../../stdlib/docs/process.md) | `@stdlib/process` | fork, exec, wait, kill |
| [`shell`](../../stdlib/docs/shell.md) | `@stdlib/shell` | Execucao de comandos shell e escape de argumentos |

### Terminal e UI

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`terminal`](../../stdlib/docs/terminal.md) | `@stdlib/terminal` | Cores ANSI, estilos e controle de cursor |
| [`termios`](../../stdlib/docs/termios.md) | `@stdlib/termios` | Entrada de terminal bruta e deteccao de teclas |

### Banco de Dados

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`sqlite`](../../stdlib/docs/sqlite.md) | `@stdlib/sqlite` | SQLite database, query, exec, transacoes |

### FFI e Interop

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`ffi`](../../stdlib/docs/ffi.md) | `@stdlib/ffi` | Gerenciamento de callbacks FFI e constantes de tipo |

### Utilitarios

| Modulo | Import | Descricao |
|--------|--------|-----------|
| [`retry`](../../stdlib/docs/retry.md) | `@stdlib/retry` | Logica de retry com backoff exponencial |

---

## Exemplos Rapidos

### Ler e parsear um arquivo de configuracao

```hemlock
import { parse_file } from "@stdlib/yaml";
import { get } from "@stdlib/yaml";

let config = parse_file("config.yaml");
let db_host = get(config, "database.host");
print("Connecting to " + db_host);
```

### Requisicao HTTP com JSON

```hemlock
import { http_get } from "@stdlib/http";
import { parse } from "@stdlib/json";

let resp = http_get("https://api.example.com/data");
let data = parse(resp.body);
print(data["name"]);
```

### Processamento concorrente

```hemlock
import { ThreadPool, parallel_map } from "@stdlib/async";

let pool = ThreadPool(4);
let results = parallel_map(pool, fn(x) { return x * x; }, [1, 2, 3, 4, 5]);
pool.shutdown();
```

### Hash e codificacao

```hemlock
import { sha256 } from "@stdlib/hash";
import { base64_encode } from "@stdlib/encoding";

let digest = sha256("hello world");
let encoded = base64_encode(digest);
print(encoded);
```

### Renderizacao de template

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

## Veja Tambem

- [Referencia de Funcoes Integradas](./builtins.md) -- funcoes disponiveis sem imports
- [Guia de Migracao (v2.0)](../migration-2.0.md) -- builtins movidos para stdlib na v2.0
- Documentacao individual dos modulos em [`stdlib/docs/`](../../stdlib/docs/)
