# Filosofia de Diseno del Lenguaje Hemlock

> "Un lenguaje pequeno e inseguro para escribir cosas inseguras de manera segura."

Este documento captura los principios de diseno fundamentales para asistentes de IA que trabajan con Hemlock.
Para documentacion detallada, consulte `docs/README.md` y el directorio `stdlib/docs/`.

---

## Identidad Central

Hemlock es un **lenguaje de scripting de sistemas** con gestion manual de memoria y control explicito:
- El poder de C con ergonomia de scripting moderna
- Concurrencia asincrona estructurada incorporada
- Sin comportamiento oculto ni magia

**Hemlock NO ES:** Seguro en memoria, un lenguaje con GC, ni oculta complejidad.
**Hemlock ES:** Explicito sobre implicito, educativo, una "capa de scripting C" para trabajo de sistemas.

---

## Principios de Diseno

### 1. Explicito Sobre Implicito
- Punto y coma obligatorio (sin ASI)
- Gestion manual de memoria (alloc/free)
- Anotaciones de tipo opcionales pero verificadas en tiempo de ejecucion

### 2. Dinamico por Defecto, Tipado por Eleccion
- Cada valor tiene una etiqueta de tipo en tiempo de ejecucion
- Los literales infieren tipos: `42` → i32, `5000000000` → i64, `3.14` → f64
- Las anotaciones de tipo opcionales imponen verificaciones en tiempo de ejecucion

### 3. Inseguro es una Caracteristica
- Aritmetica de punteros permitida (responsabilidad del usuario)
- Sin verificacion de limites en `ptr` crudo (use `buffer` para seguridad)
- Se permiten fallos por doble liberacion

### 4. Concurrencia Estructurada de Primera Clase
- `async`/`await` incorporados con paralelismo basado en pthread
- Canales para comunicacion
- `spawn`/`join`/`detach` para gestion de tareas

### 5. Sintaxis Similar a C
- Bloques `{}` siempre requeridos
- Comentarios: `// linea` y `/* bloque */`
- Operadores coinciden con C: `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Incremento/decremento: `++x`, `x++`, `--x`, `x--` (prefijo y posfijo)
- Asignacion compuesta: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` siempre devuelve flotante (use `divi()` de `@stdlib/math` para division entera)
- Sintaxis de tipo: `let x: type = value;`

---

## Referencia Rapida

### Tipos
```
Signed:   i8, i16, i32, i64
Unsigned: u8, u16, u32, u64
Floats:   f32, f64
Other:    bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Aliases:  integer (i32), number (f64), byte (u8)
```

**Promocion de tipos:** i8 → u8 → i16 → u16 → i32 → u32 → i64 → u64 → f32 → f64 (los flotantes siempre ganan, pero i64/u64 + f32 → f64 para preservar precision)

### Literales
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> i32 max)
let hex = 0xDEADBEEF;    // hex literal
let bin = 0b1010;        // binary literal
let oct = 0o777;         // octal literal
let sep = 1_000_000;     // numeric separators allowed
let pi = 3.14;           // f64
let half = .5;           // f64 (no leading zero)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // hex and unicode escapes
let ch = 'A';            // rune
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Conversion de Tipos
```hemlock
let n = i32("42");       // Parse string to i32
let f = f64("3.14");     // Parse string to f64
let big = i64(42);       // i32 to i64
let truncated = i32(3.99); // f64 to i32 (truncates to 3)
let f: f64 = 100;        // i32 to f64 via annotation (numeric coercion OK)
// let n: i32 = "42";    // ERROR - use i32("42") for string parsing
```

### Introspeccion
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
"hello".length;          // 5 (rune count)
"hello".byte_length;     // 5 (byte count)

// typeid() - deteccion de tipo rapida basada en enteros (sin asignacion de string)
typeid(42);              // 2 (TYPEID_I32)
if (typeid(val) == TYPEID_I32 || typeid(val) == TYPEID_I64) { ... }
```

**Constantes TYPEID:** `TYPEID_I8` (0), `TYPEID_I16` (1), `TYPEID_I32` (2), `TYPEID_I64` (3), `TYPEID_U8` (4), `TYPEID_U16` (5), `TYPEID_U32` (6), `TYPEID_U64` (7), `TYPEID_F32` (8), `TYPEID_F64` (9), `TYPEID_BOOL` (10), `TYPEID_STRING` (11), `TYPEID_RUNE` (12), `TYPEID_PTR` (13), `TYPEID_BUFFER` (14), `TYPEID_ARRAY` (15), `TYPEID_OBJECT` (16), `TYPEID_FILE` (17), `TYPEID_FUNCTION` (18), `TYPEID_TASK` (19), `TYPEID_CHANNEL` (20), `TYPEID_NULL` (21)

### Memoria
```hemlock
let p = alloc(64);       // raw pointer
let b = buffer(64);      // safe buffer (bounds checked)
memset(p, 0, 64); memcpy(dest, src, 64);
free(p);                 // manual cleanup required
let view = b.slice(0, 16);  // zero-copy buffer view
ptr_write_f32(b, 3.14);     // ptr_read/write accept buffers directly
```

### Flujo de Control
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // infinite loop
switch (x) { case 1: break; default: break; }  // C-style fall-through
defer cleanup();         // runs when function returns

// Loop labels for nested break/continue
outer: while (cond) {
    for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }
    }
}
```

### Coincidencia de Patrones
```hemlock
let result = match (value) {
    0 => "zero",
    1 | 2 | 3 => "small",           // OR pattern
    n if n < 10 => "medium",        // Guard
    n => "large: " + n              // Variable binding
};

// Also supports: type patterns (n: i32), object/array destructuring,
// nested patterns, wildcard (_). See docs/language-guide/pattern-matching.md
```

### Coalescencia Null
```hemlock
let name = user.name ?? "Anonymous";     // null coalescing
config ??= { timeout: 30 };             // null coalescing assignment
let city = user?.address?.city;          // safe navigation
```

### Funciones
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonymous/closure
fn double(x: i32): i32 => x * 2;  // expression-bodied

// Parameter modifiers
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // pass-by-reference
fn print_all(const items: array) { for (i in items) { print(i); } }  // immutable

// Named arguments
create_user(name: "Bob", age: 30);
create_user("David", active: false);  // positional then named
```

### Objetos, Enums y Tipos
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let person = { name, age };             // shorthand syntax
let config = { ...defaults, size: "large" }; // spread operator

// Bracket notation with key coercion (non-string keys auto-coerce to string)
let map = {};
map[42] = "value";              // integer key → "42"
map[true] = "yes";              // bool key → "true"
map['A'] = "alpha";             // rune key → "A"
print(map[42]);                 // "value"
print(map.has(42));             // true
map.delete(42);                 // removes field "42"
let keys = map.keys();          // returns array of string keys

enum Color { RED, GREEN, BLUE }

// Compound types (intersection/duck typing)
let p: HasName & HasAge = { name: "Alice", age: 30 };

// Type aliases
type Callback = fn(i32): void;
type Person = HasName & HasAge;

// Method signatures in define
define Comparable { value: i32, fn compare(other: Self): i32 }
```

### Manejo de Errores
```hemlock
try { throw "error"; } catch (e) { print(e); } finally { cleanup(); }
panic("unrecoverable");  // exits immediately, not catchable
```

### Async/Concurrencia
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // or join(task)
detach(spawn(background_work));
let t = spawn_with({ stack_size: 4194304, name: "worker" }, compute, 42);

let ch = channel(10);
ch.send(value); let val = ch.recv(); ch.close();
```

**Propiedad de memoria:** Las tareas comparten punteros pero copian primitivos. Use `join()` antes de `free()` cuando comparta `ptr`.

### E/S
```hemlock
let name = read_line();          // stdin (returns null on EOF)
print("hello"); write("no newline"); eprint("stderr");
let f = open("file.txt", "r");  // modes: r, w, a, r+, w+, a+
f.read(); f.write("data"); f.close();
```

---

## Metodos de String (22)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `trim_start`, `trim_end`,
`to_upper`, `to_lower`, `starts_with`, `ends_with`, `replace`, `replace_all`,
`repeat`, `char_at`, `byte_at`, `chars`, `bytes`, `to_bytes`, `byte_ptr`, `deserialize`

Strings de plantilla: `` `Hello ${name}!` ``

**Mutabilidad de strings:** Los strings son mutables via asignacion por indice (`s[0] = 'H'`), pero todos los metodos de string devuelven nuevos strings.

## Metodos de Array (28)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `findIndex`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`,
`every`, `some`, `indexOf`, `lastIndexOf`, `sort`, `fill`, `reserve`, `flat`, `serialize`

Arrays tipados: `let nums: array<i32> = [1, 2, 3];`

---

## Biblioteca Estandar (53 modulos)

Importe con prefijo `@stdlib/`: `import { sin, cos, PI } from "@stdlib/math";`

| Modulo | Descripcion |
|--------|-------------|
| `arena` | Asignador de memoria arena (asignacion bump) |
| `args` | Analisis de argumentos de linea de comandos |
| `assert` | Utilidades de asercion |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Operaciones de E/S de archivos asincronas |
| `atomic` | Operaciones atomicas (load, store, add, CAS, fence) |
| `bytes` | Utilidades de orden de bytes (bswap, hton/ntoh, E/S endian) |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | Analisis y generacion de CSV |
| `debug` | Inspeccion de tareas y gestion de pila |
| `datetime` | Clase DateTime, formateo, analisis |
| `decimal` | to_fixed, to_hex, parse_int, parse_float, StringBuilder |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `ffi` | Gestion de callbacks FFI |
| `fmt` | Utilidades de formateo de strings |
| `fs` | open, read_file, write_file, list_dir, exists |
| `glob` | Coincidencia de patrones de archivos |
| `hash` | sha1, sha256, sha512, md5, djb2, crc32, adler32 |
| `http` | http_get, http_post, http_request |
| `ipc` | Comunicacion entre procesos |
| `iter` | Utilidades de iterador |
| `jinja` | Renderizado de plantillas compatible con Jinja2 |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger con niveles |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `matrix` | Operaciones de matrices densas (add, multiply, transpose, determinant, inverse) |
| `mmap` | E/S de archivos mapeados en memoria (mmap, munmap, msync) |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Manipulacion de rutas de archivos |
| `process` | fork, exec, wait, kill |
| `random` | Generacion de numeros aleatorios |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Logica de reintento con backoff |
| `semver` | Versionado semantico |
| `shell` | Utilidades de comandos shell |
| `signal` | Constantes de senales (SIGINT, SIGTERM, etc.) |
| `sqlite` | Base de datos SQLite, query, exec, transacciones |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | Colores y estilos ANSI |
| `termios` | Entrada de terminal cruda, deteccion de teclas |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | Analisis y generacion de TOML |
| `url` | Analisis y manipulacion de URL |
| `unix_socket` | Sockets de dominio Unix (stream/datagram AF_UNIX) |
| `uuid` | Generacion de UUID |
| `vector` | Busqueda de similitud de vectores (USearch ANN) |
| `websocket` | Cliente WebSocket |
| `yaml` | Analisis y generacion de YAML |

Consulte `stdlib/docs/` para documentacion detallada de modulos.

---

## FFI (Interfaz de Funcion Foranea)

```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
let len = strlen("Hello!");  // 6

// Dynamic FFI
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

Consulte `docs/advanced/ffi.md` para documentacion completa.

---

## Estructura del Proyecto

```
hemlock/
├── src/
│   ├── frontend/         # Compartido: lexer, parser, AST, modulos
│   ├── backends/
│   │   ├── interpreter/  # hemlock: interprete tree-walking
│   │   └── compiler/     # hemlockc: generador de codigo C
│   ├── modules/          # Implementaciones de modulos nativos
│   ├── runtime/          # Codigo C relacionado con el runtime
│   ├── shared/           # Utilidades compartidas (promocion de tipos, etc.)
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   ├── bundler/      # Herramientas de bundle/paquetes
│   │   └── formatter/    # Formateador de codigo
├── runtime/              # Runtime de programas compilados (libhemlock_runtime.a)
├── stdlib/               # Biblioteca estandar
│   └── docs/             # Documentacion de modulos
├── include/              # Archivos de cabecera C (hemlock_limits.h, etc.)
├── docs/                 # Documentacion completa
├── tests/                # 978+ pruebas
├── examples/             # Programas de ejemplo
├── benchmark/            # Benchmarks
├── editors/              # Integraciones de editores
└── wasm/                 # Soporte WebAssembly
```

### Arquitectura del Compilador/Interprete

Ambos backends comparten un frontend comun (lexer, parser, AST). El interprete realiza evaluacion tree-walk; el compilador genera codigo C y enlaza con GCC. Consulte `docs/` para detalles.

---

## Guias de Estilo de Codigo

1. **Defina constantes en `include/hemlock_limits.h`** con prefijo `HML_`
2. **Evite numeros magicos** - use constantes con nombre
3. **Incluya `hemlock_limits.h`** via `internal.h` para acceder a constantes

---

## Que NO Hacer

- Agregar comportamiento implicito (ASI, GC, limpieza automatica)
- Ocultar complejidad (optimizaciones magicas, conteos de referencias ocultos)
- Romper semantica existente (punto y coma, memoria manual, strings mutables)
- Perder precision en conversiones implicitas
- Usar numeros magicos - defina constantes con nombre en `hemlock_limits.h` en su lugar

---

## Pruebas

```bash
make test              # Run interpreter tests
make test-compiler     # Run compiler tests
make parity            # Run parity tests (both must match)
make test-all          # Run all test suites
```

**Importante:** Siempre use un timeout al ejecutar pruebas (las pruebas async pueden colgarse):
```bash
timeout 60 make test
timeout 120 make parity
```

---

## Desarrollo con Paridad Primero

**Tanto el interprete como el compilador deben producir salida identica para la misma entrada.**

Al agregar/modificar caracteristicas del lenguaje:
1. Disenar el cambio AST/semantico en el frontend compartido
2. Implementar en el interprete (evaluacion tree-walking)
3. Implementar en el compilador (generacion de codigo C)
4. Agregar prueba de paridad en `tests/parity/` con archivo `.expected`
5. Ejecutar `make parity` antes de fusionar

Cada prueba tiene `feature.hml` + `feature.expected`. Ambos backends deben coincidir con la salida esperada.

---

## Filosofia

> Te damos las herramientas para ser seguro (`buffer`, anotaciones de tipo, verificacion de limites) pero no te obligamos a usarlas (`ptr`, memoria manual, operaciones inseguras).

**Si no esta seguro de si una caracteristica encaja en Hemlock, pregunte: "Esto le da al programador mas control explicito, o esconde algo?"**

Si lo esconde, probablemente no pertenece a Hemlock.
