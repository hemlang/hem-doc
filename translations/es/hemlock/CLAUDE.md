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
- `/` siempre devuelve flotante (use `divi()` para division entera)
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

**Promocion de tipos:** i8 → i16 → i32 → i64 → f32 → f64 (los flotantes siempre ganan, pero i64/u64 + f32 → f64 para preservar precision)

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
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Conversion de Tipos
```hemlock
// Type constructor functions - parse strings to types
let n = i32("42");       // Parse string to i32
let f = f64("3.14");     // Parse string to f64
let b = bool("true");    // Parse string to bool ("true" or "false")

// All numeric types supported
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// Hex and negative numbers
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// Type aliases work too
let x = integer("100");  // Same as i32("100")
let y = number("1.5");   // Same as f64("1.5")
let z = byte("200");     // Same as u8("200")

// Convert between numeric types
let big = i64(42);       // i32 to i64
let truncated = i32(3.99); // f64 to i32 (truncates to 3)

// Type annotations validate types (but don't parse strings)
let f: f64 = 100;        // i32 to f64 via annotation (numeric coercion OK)
// let n: i32 = "42";    // ERROR - use i32("42") for string parsing
```

### Introspeccion
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5 (string length in bytes)
len([1, 2, 3]);          // 3 (array length)
```

### Memoria
```hemlock
let p = alloc(64);       // raw pointer
let b = buffer(64);      // safe buffer (bounds checked)
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // manual cleanup required
```

### Flujo de Control
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // infinite loop (cleaner than while(true))
switch (x) { case 1: break; default: break; }  // C-style fall-through
defer cleanup();         // runs when function returns

// Loop labels for targeted break/continue in nested loops
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // break outer loop
        if (i == 3) { continue outer; }  // continue outer loop
    }
}
```

### Coincidencia de Patrones
```hemlock
// Match expression - returns value
let result = match (value) {
    0 => "zero",                    // Literal pattern
    1 | 2 | 3 => "small",           // OR pattern
    n if n < 10 => "medium",        // Guard expression
    n => "large: " + n              // Variable binding
};

// Type patterns
match (val) {
    n: i32 => "integer",
    s: string => "string",
    _ => "other"                    // Wildcard
}

// Object destructuring
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// Array destructuring with rest
match (arr) {
    [] => "empty",
    [first, ...rest] => "head: " + first,
    _ => "other"
}

// Nested patterns
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

Consulte `docs/language-guide/pattern-matching.md` para documentacion completa.

### Operadores de Coalescencia Nula
```hemlock
// Null coalescing (??) - returns left if non-null, else right
let name = user.name ?? "Anonymous";
let first = a ?? b ?? c ?? "fallback";

// Null coalescing assignment (??=) - assigns only if null
let config = null;
config ??= { timeout: 30 };    // config is now { timeout: 30 }
config ??= { timeout: 60 };    // config unchanged (not null)

// Works with properties and indices
obj.field ??= "default";
arr[0] ??= "first";

// Safe navigation (?.) - returns null if object is null
let city = user?.address?.city;  // null if any part is null
let upper = name?.to_upper();    // safe method call
let item = arr?.[0];             // safe indexing
```

### Funciones
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // anonymous/closure

// Expression-bodied functions (arrow syntax)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // anonymous expression-bodied

// Parameter modifiers
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // pass-by-reference
fn print_all(const items: array) { for (i in items) { print(i); } }  // immutable
```

### Argumentos con Nombre
```hemlock
// Functions can be called with named arguments
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Positional arguments (traditional)
create_user("Alice", 25, false);

// Named arguments - can be in any order
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Skip optional parameters by naming what you need
create_user("David", active: false);  // Uses default age=18

// Named arguments must come after positional arguments
create_user("Eve", age: 21);          // OK: positional then named
// create_user(name: "Bad", 25);      // ERROR: positional after named
```

**Reglas:**
- Los argumentos con nombre usan sintaxis `name: value`
- Pueden aparecer en cualquier orden despues de los argumentos posicionales
- Los argumentos posicionales no pueden seguir a los argumentos con nombre
- Funciona con parametros por defecto/opcionales
- Los nombres de parametros desconocidos causan errores en tiempo de ejecucion

### Objetos y Enums
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// Object shorthand syntax (ES6-style)
let name = "Alice";
let age = 30;
let person = { name, age };         // equivalent to { name: name, age: age }

// Object spread operator
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // copies defaults, overrides size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Tipos Compuestos (Interseccion/Tipos Duck)
```hemlock
// Define structural types
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Compound type: object must satisfy ALL types
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Function parameters with compound types
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

// Three or more types
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Extra fields allowed (duck typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - extra fields ignored
};
```

Los tipos compuestos proporcionan comportamiento similar a interfaces sin una palabra clave `interface` separada,
construyendo sobre los paradigmas existentes de `define` y duck typing.

### Alias de Tipos
```hemlock
// Simple type alias
type Integer = i32;
type Text = string;

// Function type alias
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Compound type alias (great for reusable interfaces)
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Generic type alias
type Pair<T> = { first: T, second: T };

// Using type aliases
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

Los alias de tipos crean atajos con nombre para tipos complejos, mejorando la legibilidad y mantenibilidad.

### Tipos de Funcion
```hemlock
// Function type annotations for parameters
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Higher-order function returning a function
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Async function types
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// Function types with multiple parameters
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Parametros Const
```hemlock
// Const parameter - deep immutability
fn print_all(const items: array) {
    // items.push(4);  // ERROR: cannot mutate const parameter
    for (item in items) {
        print(item);
    }
}

// Const with objects - no mutation through any path
fn describe(const person: object) {
    print(person.name);       // OK: reading is allowed
    // person.name = "Bob";   // ERROR: cannot mutate
}

// Nested access is allowed for reading
fn get_city(const user: object) {
    return user.address.city;  // OK: reading nested properties
}
```

El modificador `const` previene cualquier mutacion del parametro, incluyendo propiedades anidadas.
Esto proporciona seguridad en tiempo de compilacion para funciones que no deben modificar sus entradas.

### Parametros Ref (Paso por Referencia)
```hemlock
// Ref parameter - caller's variable is modified directly
fn increment(ref x: i32) {
    x = x + 1;  // Modifies the original variable
}

let count = 10;
increment(count);
print(count);  // 11 - original was modified

// Classic swap function
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// Mix ref and regular parameters
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

El modificador `ref` pasa una referencia a la variable del llamador, permitiendo que la funcion
la modifique directamente. Sin `ref`, los primitivos se pasan por valor (copiados). Use `ref` cuando
necesite mutar el estado del llamador sin devolver un valor.

**Reglas:**
- Los parametros `ref` deben recibir variables, no literales o expresiones
- Funciona con todos los tipos (primitivos, arrays, objetos)
- Combine con anotaciones de tipo: `ref x: i32`
- No se puede combinar con `const` (son opuestos)

### Firmas de Metodos en Define
```hemlock
// Define with method signatures (interface pattern)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Required method signature
}

// Objects must provide the required method
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Optional methods with ?
define Serializable {
    fn serialize(): string,        // Required
    fn pretty?(): string           // Optional method
}

// Self type refers to the defining type
define Cloneable {
    fn clone(): Self   // Returns same type as the object
}
```

Las firmas de metodos en bloques `define` usan delimitadores de coma (como interfaces de TypeScript),
estableciendo contratos que los objetos deben cumplir y habilitando patrones de programacion
similares a interfaces con el sistema de duck typing de Hemlock.

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

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**Propiedad de memoria:** Las tareas reciben copias de valores primitivos pero comparten punteros. Si pasa un `ptr` a una tarea generada, debe asegurarse de que la memoria permanezca valida hasta que la tarea complete. Use `join()` antes de `free()`, o use canales para senalar finalizacion.

### Entrada de Usuario
```hemlock
let name = read_line();          // Read line from stdin (blocks)
print("Hello, " + name);
eprint("Error message");         // Print to stderr

// read_line() returns null on EOF
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Got:", line);
}
```

### E/S de Archivos
```hemlock
let f = open("file.txt", "r");  // modes: r, w, a, r+, w+, a+
let content = f.read();
f.write("data");
f.seek(0);
f.close();
```

### Senales
```hemlock
signal(SIGINT, fn(sig) { print("Interrupted"); });
raise(SIGUSR1);
```

---

## Metodos de String (19)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `to_upper`, `to_lower`,
`starts_with`, `ends_with`, `replace`, `replace_all`, `repeat`, `char_at`,
`byte_at`, `chars`, `bytes`, `to_bytes`, `deserialize`

Strings de plantilla: `` `Hello ${name}!` ``

**Mutabilidad de strings:** Los strings son mutables via asignacion por indice (`s[0] = 'H'`), pero todos los metodos de string devuelven nuevos strings sin modificar el original. Esto permite mutacion in situ cuando se necesita mientras mantiene el encadenamiento de metodos funcional.

**Propiedades de longitud de string:**
```hemlock
let s = "hello 🚀";
print(s.length);       // 7 (character/rune count)
print(s.byte_length);  // 10 (byte count - emoji is 4 bytes UTF-8)
```

## Metodos de Array (18)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`

Arrays tipados: `let nums: array<i32> = [1, 2, 3];`

---

## Biblioteca Estandar (40 modulos)

Importe con prefijo `@stdlib/`:
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| Modulo | Descripcion |
|--------|-------------|
| `arena` | Asignador de memoria arena (asignacion bump) |
| `args` | Analisis de argumentos de linea de comandos |
| `assert` | Utilidades de asercion |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Operaciones de E/S de archivos asincronas |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | Analisis y generacion de CSV |
| `datetime` | Clase DateTime, formateo, analisis |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `fmt` | Utilidades de formateo de strings |
| `fs` | read_file, write_file, list_dir, exists |
| `glob` | Coincidencia de patrones de archivos |
| `hash` | sha256, sha512, md5, djb2 |
| `http` | http_get, http_post, http_request |
| `ipc` | Comunicacion entre procesos |
| `iter` | Utilidades de iterador |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger con niveles |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Manipulacion de rutas de archivos |
| `process` | fork, exec, wait, kill |
| `random` | Generacion de numeros aleatorios |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Logica de reintento con backoff |
| `semver` | Versionado semantico |
| `shell` | Utilidades de comandos shell |
| `sqlite` | Base de datos SQLite, query, exec, transacciones |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | Colores y estilos ANSI |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | Analisis y generacion de TOML |
| `url` | Analisis y manipulacion de URL |
| `uuid` | Generacion de UUID |
| `websocket` | Cliente WebSocket |

Consulte `stdlib/docs/` para documentacion detallada de modulos.

---

## FFI (Interfaz de Funcion Foranea)

Declare y llame funciones C desde bibliotecas compartidas:
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hello!");  // 6
let pid = getpid();
```

Exporte funciones FFI desde modulos:
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

FFI dinamico (enlace en tiempo de ejecucion):
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

Tipos: `FFI_INT`, `FFI_DOUBLE`, `FFI_POINTER`, `FFI_STRING`, `FFI_VOID`, etc.

---

## Operaciones Atomicas

Programacion concurrente sin bloqueos con operaciones atomicas:

```hemlock
// Allocate memory for atomic i32
let p = alloc(4);
ptr_write_i32(p, 0);

// Atomic load/store
let val = atomic_load_i32(p);        // Read atomically
atomic_store_i32(p, 42);             // Write atomically

// Fetch-and-modify operations (return OLD value)
let old = atomic_add_i32(p, 10);     // Add, return old
old = atomic_sub_i32(p, 5);          // Subtract, return old
old = atomic_and_i32(p, 0xFF);       // Bitwise AND
old = atomic_or_i32(p, 0x10);        // Bitwise OR
old = atomic_xor_i32(p, 0x0F);       // Bitwise XOR

// Compare-and-swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // If *p == 42, set to 100
// Returns true if swap succeeded, false otherwise

// Atomic exchange
old = atomic_exchange_i32(p, 999);   // Swap, return old

free(p);

// i64 variants available (atomic_load_i64, atomic_add_i64, etc.)

// Memory fence (full barrier)
atomic_fence();
```

Todas las operaciones usan consistencia secuencial (`memory_order_seq_cst`).

---

## Estructura del Proyecto

```
hemlock/
├── src/
│   ├── frontend/         # Shared: lexer, parser, AST, modules
│   ├── backends/
│   │   ├── interpreter/  # hemlock: tree-walking interpreter
│   │   └── compiler/     # hemlockc: C code generator
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # Bundle/package tools
├── runtime/              # Compiled program runtime (libhemlock_runtime.a)
├── stdlib/               # Standard library (40 modules)
│   └── docs/             # Module documentation
├── docs/                 # Full documentation
│   ├── language-guide/   # Types, strings, arrays, etc.
│   ├── reference/        # API references
│   └── advanced/         # Async, FFI, signals, etc.
├── tests/                # 625+ tests
└── examples/             # Example programs
```

---

## Guias de Estilo de Codigo

### Constantes y Numeros Magicos

Al agregar constantes numericas al codigo base en C, siga estas guias:

1. **Defina constantes en `include/hemlock_limits.h`** - Este archivo es la ubicacion central para todos los limites de tiempo de compilacion y ejecucion, capacidades y constantes con nombre.

2. **Use nombres descriptivos con prefijo `HML_`** - Todas las constantes deben tener prefijo `HML_` para claridad de espacio de nombres.

3. **Evite numeros magicos** - Reemplace valores numericos codificados con constantes con nombre. Ejemplos:
   - Limites de rango de tipos: `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Capacidades de buffer: `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Conversiones de tiempo: `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Semillas de hash: `HML_DJB2_HASH_SEED`
   - Valores ASCII: `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Incluya `hemlock_limits.h`** - Los archivos fuente deben incluir este encabezado (frecuentemente via `internal.h`) para acceder a las constantes.

5. **Documente el proposito** - Agregue un comentario explicando lo que cada constante representa.

---

## Que NO Hacer

- No agregar comportamiento implicito (ASI, GC, limpieza automatica)
- No ocultar complejidad (optimizaciones magicas, conteos de referencias ocultos)
- No romper semantica existente (punto y coma, memoria manual, strings mutables)
- No perder precision en conversiones implicitas
- No usar numeros magicos - defina constantes con nombre en `hemlock_limits.h` en su lugar

---

## Pruebas

```bash
make test              # Run interpreter tests
make test-compiler     # Run compiler tests
make parity            # Run parity tests (both must match)
make test-all          # Run all test suites
```

**Importante:** Las pruebas pueden colgarse debido a problemas de async/concurrencia. Siempre use un timeout al ejecutar pruebas:
```bash
timeout 60 make test   # 60 second timeout
timeout 120 make parity
```

Categorias de pruebas: primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Arquitectura del Compilador/Interprete

Hemlock tiene dos backends de ejecucion que comparten un frontend comun:

```
Source (.hml)
    ↓
┌─────────────────────────────┐
│  SHARED FRONTEND            │
│  - Lexer (src/frontend/)    │
│  - Parser (src/frontend/)   │
│  - AST (src/frontend/)      │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ INTERPRETER│    │  COMPILER  │
│ (hemlock)  │    │ (hemlockc) │
│            │    │            │
│ Tree-walk  │    │ Type check │
│ evaluation │    │ AST → C    │
│            │    │ gcc link   │
└────────────┘    └────────────┘
```

### Verificacion de Tipos del Compilador

El compilador (`hemlockc`) incluye verificacion de tipos en tiempo de compilacion, **habilitada por defecto**:

```bash
hemlockc program.hml -o program    # Type checks, then compiles
hemlockc --check program.hml       # Type check only, don't compile
hemlockc --no-type-check prog.hml  # Disable type checking
hemlockc --strict-types prog.hml   # Warn on implicit 'any' types
```

El verificador de tipos:
- Valida anotaciones de tipo en tiempo de compilacion
- Trata codigo sin tipo como dinamico (tipo `any`) - siempre valido
- Proporciona sugerencias de optimizacion para unboxing
- Usa conversiones numericas permisivas (rango validado en tiempo de ejecucion)

### Estructura de Directorios

```
hemlock/
├── src/
│   ├── frontend/           # Shared: lexer, parser, AST, modules
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock: tree-walking interpreter
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc: C code generator
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # Language server
│   │   └── bundler/        # Bundle/package tools
├── runtime/                # libhemlock_runtime.a for compiled programs
├── stdlib/                 # Shared standard library
└── tests/
    ├── parity/             # Tests that MUST pass both backends
    ├── interpreter/        # Interpreter-specific tests
    └── compiler/           # Compiler-specific tests
```

---

## Desarrollo con Paridad Primero

**Tanto el interprete como el compilador deben producir salida identica para la misma entrada.**

### Politica de Desarrollo

Al agregar o modificar caracteristicas del lenguaje:

1. **Disenar** - Definir el cambio AST/semantico en el frontend compartido
2. **Implementar interprete** - Agregar evaluacion tree-walking
3. **Implementar compilador** - Agregar generacion de codigo C
4. **Agregar prueba de paridad** - Escribir prueba en `tests/parity/` con archivo `.expected`
5. **Verificar** - Ejecutar `make parity` antes de fusionar

### Estructura de Pruebas de Paridad

```
tests/parity/
├── language/       # Core language features (control flow, closures, etc.)
├── builtins/       # Built-in functions (print, typeof, memory, etc.)
├── methods/        # String and array methods
└── modules/        # Import/export, stdlib imports
```

Cada prueba tiene dos archivos:
- `feature.hml` - El programa de prueba
- `feature.expected` - Salida esperada (debe coincidir para ambos backends)

### Resultados de Pruebas de Paridad

| Estado | Significado |
|--------|-------------|
| `✓ PASSED` | Tanto interprete como compilador coinciden con salida esperada |
| `◐ INTERP_ONLY` | Interprete funciona, compilador falla (necesita correccion del compilador) |
| `◑ COMPILER_ONLY` | Compilador funciona, interprete falla (raro) |
| `✗ FAILED` | Ambos fallan (error de prueba o implementacion) |

### Que Requiere Paridad

- Todas las construcciones del lenguaje (if, while, for, switch, defer, try/catch)
- Todos los operadores (aritmeticos, bitwise, logicos, comparacion)
- Todas las funciones incorporadas (print, typeof, alloc, etc.)
- Todos los metodos de string y array
- Reglas de coercion y promocion de tipos
- Mensajes de error para errores en tiempo de ejecucion

### Que Puede Diferir

- Caracteristicas de rendimiento
- Detalles de disposicion de memoria
- Formato de debug/stack trace
- Errores de compilacion (el compilador puede detectar mas en tiempo de compilacion)

### Agregar una Prueba de Paridad

```bash
# 1. Create test file
cat > tests/parity/language/my_feature.hml << 'EOF'
// Test description
let x = some_feature();
print(x);
EOF

# 2. Generate expected output from interpreter
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Verify parity
make parity
```

---

## Version

**v1.8.0** - Version actual con:
- **Coincidencia de patrones** (expresiones `match`) - Desestructuracion y flujo de control poderosos:
  - Patrones literales, comodin y enlace de variables
  - Patrones OR (`1 | 2 | 3`)
  - Expresiones guard (`n if n > 0`)
  - Desestructuracion de objetos (`{ x, y }`)
  - Desestructuracion de arrays con rest (`[first, ...rest]`)
  - Patrones de tipo (`n: i32`)
  - Paridad completa entre interprete y compilador
- **Anotaciones auxiliares del compilador** - 11 anotaciones de optimizacion para control de GCC/Clang:
  - `@inline`, `@noinline` - control de inlining de funciones
  - `@hot`, `@cold` - sugerencias de prediccion de rama
  - `@pure`, `@const` - anotaciones de efectos secundarios
  - `@flatten` - hacer inline a todas las llamadas dentro de la funcion
  - `@optimize(level)` - nivel de optimizacion por funcion ("0", "1", "2", "3", "s", "fast")
  - `@warn_unused` - advertir sobre valores de retorno ignorados
  - `@section(name)` - colocacion de seccion ELF personalizada (ej., `@section(".text.hot")`)
- **Funciones con cuerpo de expresion** (`fn double(x): i32 => x * 2;`) - sintaxis concisa de funcion de una sola expresion
- **Sentencias de una linea** - sintaxis sin llaves para `if`, `while`, `for` (ej., `if (x > 0) print(x);`)
- **Alias de tipos** (`type Name = Type;`) - atajos con nombre para tipos complejos
- **Anotaciones de tipo de funcion** (`fn(i32): i32`) - tipos de funcion de primera clase
- **Parametros const** (`fn(const x: array)`) - inmutabilidad profunda para parametros
- **Parametros ref** (`fn(ref x: i32)`) - paso por referencia para mutacion directa del llamador
- **Firmas de metodos en define** (`fn method(): Type`) - contratos tipo interfaz (delimitados por coma)
- **Tipo Self** en firmas de metodos - se refiere al tipo que define
- **Palabra clave loop** (`loop { }`) - bucles infinitos mas limpios, reemplaza `while (true)`
- **Etiquetas de bucle** (`outer: while`) - break/continue dirigido para bucles anidados
- **Shorthand de objetos** (`{ name }`) - sintaxis de propiedad abreviada estilo ES6
- **Spread de objetos** (`{ ...obj }`) - copiar y fusionar campos de objetos
- **Tipos duck compuestos** (`A & B & C`) - tipos de interseccion para tipado estructural
- **Argumentos con nombre** para llamadas de funcion (`foo(name: "value", age: 30)`)
- **Operadores de coalescencia nula** (`??`, `??=`, `?.`) para manejo seguro de null
- **Literales octales** (`0o777`, `0O123`)
- **Separadores numericos** (`1_000_000`, `0xFF_FF`, `0b1111_0000`)
- **Comentarios de bloque** (`/* ... */`)
- **Secuencias de escape hexadecimales** en strings/runes (`\x41` = 'A')
- **Secuencias de escape Unicode** en strings (`\u{1F600}` = 😀)
- **Literales flotantes sin cero inicial** (`.5`, `.123`, `.5e2`)
- **Verificacion de tipos en tiempo de compilacion** en hemlockc (habilitada por defecto)
- **Integracion LSP** con verificacion de tipos para diagnosticos en tiempo real
- **Operadores de asignacion compuesta** (`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`)
- **Operadores de incremento/decremento** (`++x`, `x++`, `--x`, `x--`)
- **Correccion de precision de tipos**: i64/u64 + f32 → f64 para preservar precision
- Sistema de tipos unificado con sugerencias de optimizacion de unboxing
- Sistema de tipos completo (i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object, enum, file, task, channel)
- Strings UTF-8 con 19 metodos
- Arrays con 18 metodos incluyendo map/filter/reduce
- Gestion manual de memoria con `talloc()` y `sizeof()`
- Async/await con verdadero paralelismo pthread
- Operaciones atomicas para programacion concurrente sin bloqueos
- 40 modulos stdlib (+ arena, assert, semver, toml, retry, iter, random, shell)
- FFI para interoperabilidad con C con `export extern fn` para wrappers de biblioteca reutilizables
- Soporte de struct FFI en compilador (pasar structs C por valor)
- Helpers de puntero FFI (`ptr_null`, `ptr_read_*`, `ptr_write_*`)
- defer, try/catch/finally/throw, panic
- E/S de archivos, manejo de senales, ejecucion de comandos
- Gestor de paquetes [hpm](https://github.com/hemlang/hpm) con registro basado en GitHub
- Backend de compilador (generacion de codigo C) con 100% de paridad con interprete
- Servidor LSP con ir-a-definicion y encontrar-referencias
- Paso de optimizacion AST y resolucion de variables para busqueda O(1)
- Builtin apply() para llamadas de funcion dinamicas
- Canales sin buffer y soporte de muchos parametros
- 159 pruebas de paridad (100% tasa de aprobacion)

---

## Filosofia

> Le damos las herramientas para estar seguro (`buffer`, anotaciones de tipo, verificacion de limites) pero no le obligamos a usarlas (`ptr`, memoria manual, operaciones inseguras).

**Si no esta seguro de si una caracteristica encaja en Hemlock, pregunte: "Esto le da al programador mas control explicito, o esconde algo?"**

Si esconde, probablemente no pertenece a Hemlock.
