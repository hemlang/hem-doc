# Referencia de Funciones Integradas

Referencia completa para todas las funciones integradas y constantes en Hemlock.

---

## Descripcion General

Hemlock proporciona un conjunto de funciones integradas para E/S, introspeccion de tipos, gestion de memoria, concurrencia e interaccion con el sistema. Todas las funciones integradas estan disponibles globalmente sin importaciones.

---

## Funciones de E/S

### print

Imprime valores a stdout con nueva linea.

**Firma:**
```hemlock
print(...values): null
```

**Parametros:**
- `...values` - Cualquier numero de valores a imprimir

**Retorna:** `null`

**Ejemplos:**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// Multiples valores
print("x =", 10, "y =", 20);
```

**Comportamiento:**
- Convierte todos los valores a strings
- Separa multiples valores con espacios
- Agrega nueva linea al final
- Vacia stdout

---

### read_line

Lee una linea de texto desde stdin (entrada del usuario).

**Firma:**
```hemlock
read_line(): string | null
```

**Parametros:** Ninguno

**Retorna:**
- `string` - La linea leida desde stdin (nueva linea eliminada)
- `null` - En EOF (fin de archivo/entrada)

**Ejemplos:**
```hemlock
// Prompt simple
print("Cual es tu nombre?");
let name = read_line();
print("Hola, " + name + "!");

// Leer numeros (requiere analisis manual)
print("Ingresa un numero:");
let input = read_line();
let num = parse_int(input);  // Ver abajo para parse_int
print("Doble:", num * 2);

// Manejar EOF
let line = read_line();
if (line == null) {
    print("Fin de entrada");
}

// Leer multiples lineas
print("Ingresa lineas (Ctrl+D para parar):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("Dijiste:", line);
}
```

**Comportamiento:**
- Bloquea hasta que el usuario presiona Enter
- Elimina nueva linea (`\n`) y retorno de carro (`\r`) finales
- Retorna `null` en EOF (Ctrl+D en Unix, Ctrl+Z en Windows)
- Lee solo desde stdin (no desde archivos)

**Analizando Entrada del Usuario:**

Como `read_line()` siempre retorna un string, necesita analizar entrada numerica manualmente:

```hemlock
// Analizador simple de enteros
fn parse_int(s: string): i32 {
    let result: i32 = 0;
    let negative = false;
    let i = 0;

    if (s.length > 0 && s.char_at(0) == '-') {
        negative = true;
        i = 1;
    }

    while (i < s.length) {
        let c = s.char_at(i);
        let code: i32 = c;
        if (code >= 48 && code <= 57) {
            result = result * 10 + (code - 48);
        } else {
            break;
        }
        i = i + 1;
    }

    if (negative) {
        return -result;
    }
    return result;
}

// Uso
print("Ingresa tu edad:");
let age = parse_int(read_line());
print("En 10 anos tendras", age + 10);
```

**Ver Tambien:** [API de Archivos](file-api.md) para leer desde archivos

---

### eprint

Imprime un valor a stderr con nueva linea.

**Firma:**
```hemlock
eprint(value: any): null
```

**Parametros:**
- `value` - Valor unico a imprimir a stderr

**Retorna:** `null`

**Ejemplos:**
```hemlock
eprint("Error: archivo no encontrado");
eprint(404);
eprint("Advertencia: " + message);

// Patron tipico de manejo de errores
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Error: archivo de configuracion no encontrado: " + path);
        return null;
    }
    // ...
}
```

**Comportamiento:**
- Imprime a stderr (flujo de error estandar)
- Agrega nueva linea al final
- Solo acepta un argumento (a diferencia de `print`)
- Util para mensajes de error que no deben mezclarse con salida normal

**Diferencia con print:**
- `print()` -> stdout (salida normal, puede redirigirse con `>`)
- `eprint()` -> stderr (salida de error, puede redirigirse con `2>`)

```bash
# Ejemplo de shell: separar stdout y stderr
./hemlock script.hml > output.txt 2> errors.txt
```

---

## Introspeccion de Tipos

### typeof

Obtiene el nombre del tipo de un valor.

**Firma:**
```hemlock
typeof(value: any): string
```

**Parametros:**
- `value` - Cualquier valor

**Retorna:** Nombre del tipo como string

**Ejemplos:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// Objetos tipados
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// Otros tipos
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**Nombres de Tipos:**
- Primitivos: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Compuestos: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Especiales: `"file"`, `"task"`, `"channel"`
- Personalizados: Nombres de tipos definidos por el usuario desde `define`

**Ver Tambien:** [Sistema de Tipos](type-system.md)

---

## Ejecucion de Comandos

### exec

Ejecuta comando de shell y captura salida.

**Firma:**
```hemlock
exec(command: string): object
```

**Parametros:**
- `command` - Comando de shell a ejecutar

**Retorna:** Objeto con campos:
- `output` (string) - stdout del comando
- `exit_code` (i32) - Codigo de estado de salida (0 = exito)

**Ejemplos:**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// Verificar estado de salida
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Encontrado:", r.output);
} else {
    print("Patron no encontrado");
}

// Procesar salida multi-linea
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**Comportamiento:**
- Ejecuta comando via `/bin/sh`
- Captura solo stdout (stderr va a terminal)
- Bloquea hasta que el comando complete
- Retorna string vacio si no hay salida

**Manejo de Errores:**
```hemlock
try {
    let r = exec("nonexistent_command");
} catch (e) {
    print("Fallo al ejecutar:", e);
}
```

**Advertencia de Seguridad:** Vulnerable a inyeccion de shell. Siempre valide/sanee entrada del usuario.

**Limitaciones:**
- Sin captura de stderr
- Sin streaming
- Sin timeout
- Sin manejo de senales

---

### exec_argv

Ejecuta un comando con array de argumentos explicito (sin interpretacion de shell).

**Firma:**
```hemlock
exec_argv(argv: array): object
```

**Parametros:**
- `argv` - Array de strings: `[comando, arg1, arg2, ...]`

**Retorna:** Objeto con campos:
- `output` (string) - stdout del comando
- `exit_code` (i32) - Codigo de estado de salida (0 = exito)

**Ejemplos:**
```hemlock
// Comando simple
let result = exec_argv(["ls", "-la"]);
print(result.output);

// Comando con argumentos que contienen espacios (seguro!)
let r = exec_argv(["grep", "hello world", "file.txt"]);

// Ejecutar script con argumentos
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**Diferencia con exec:**
```hemlock
// exec() usa shell - INSEGURO con entrada de usuario
exec("ls " + user_input);  // Riesgo de inyeccion de shell!

// exec_argv() evita shell - SEGURO
exec_argv(["ls", user_input]);  // Sin inyeccion posible
```

**Cuando usar:**
- Cuando los argumentos contienen espacios, comillas o caracteres especiales
- Al procesar entrada de usuario (seguridad)
- Cuando necesita analisis predecible de argumentos

**Ver Tambien:** `exec()` para comandos de shell simples

---

## Manejo de Errores

### throw

Lanza una excepcion.

**Firma:**
```hemlock
throw expression
```

**Parametros:**
- `expression` - Valor a lanzar (cualquier tipo)

**Retorna:** Nunca retorna (transfiere control)

**Ejemplos:**
```hemlock
throw "mensaje de error";
throw 404;
throw { code: 500, message: "Error interno" };
throw null;
```

**Ver Tambien:** Sentencias try/catch/finally

---

### panic

Termina inmediatamente el programa con mensaje de error (irrecuperable).

**Firma:**
```hemlock
panic(message?: any): never
```

**Parametros:**
- `message` (opcional) - Mensaje de error a imprimir

**Retorna:** Nunca retorna (el programa sale)

**Ejemplos:**
```hemlock
panic();                          // Por defecto: "panic!"
panic("codigo inalcanzable alcanzado");
panic(42);

// Caso de uso comun
fn process_state(state: i32): string {
    if (state == 1) { return "listo"; }
    if (state == 2) { return "ejecutando"; }
    panic("estado invalido: " + typeof(state));
}
```

**Comportamiento:**
- Imprime error a stderr: `panic: <mensaje>`
- Sale con codigo 1
- **NO se puede capturar** con try/catch
- Use para bugs y errores irrecuperables

**Panic vs Throw:**
- `panic()` - Error irrecuperable, sale inmediatamente
- `throw` - Error recuperable, puede capturarse

---

### assert

Afirma que una condicion es verdadera, o termina con un mensaje de error.

**Firma:**
```hemlock
assert(condition: any, message?: string): null
```

**Parametros:**
- `condition` - Valor a verificar por veracidad
- `message` (opcional) - Mensaje de error personalizado si la afirmacion falla

**Retorna:** `null` (si la afirmacion pasa)

**Ejemplos:**
```hemlock
// Afirmaciones basicas
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "El array no debe estar vacio");

// Con mensajes personalizados
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Division por cero");
    return a / b;
}

// Validar argumentos de funcion
fn process_data(data: array) {
    assert(data != null, "data no puede ser null");
    assert(data.length > 0, "data no puede estar vacio");
    // ...
}
```

**Comportamiento:**
- Si la condicion es verdadera: retorna `null`, la ejecucion continua
- Si la condicion es falsa: imprime error y sale con codigo 1
- Valores falsos: `false`, `0`, `0.0`, `null`, `""` (string vacio)
- Valores verdaderos: todo lo demas

**Salida en fallo:**
```
Assertion failed: El array no debe estar vacio
```

**Cuando usar:**
- Validar precondiciones de funciones
- Verificar invariantes durante desarrollo
- Capturar errores del programador temprano

**assert vs panic:**
- `assert(cond, msg)` - Verifica una condicion, falla si es falsa
- `panic(msg)` - Siempre falla incondicionalmente

---

## Manejo de Senales

### signal

Registra o reinicia manejador de senal.

**Firma:**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**Parametros:**
- `signum` - Numero de senal (use constantes como `SIGINT`)
- `handler` - Funcion a llamar cuando se recibe senal, o `null` para reiniciar a predeterminado

**Retorna:** Funcion manejadora anterior, o `null`

**Ejemplos:**
```hemlock
fn handle_interrupt(sig) {
    print("SIGINT capturado!");
}

signal(SIGINT, handle_interrupt);

// Reiniciar a predeterminado
signal(SIGINT, null);
```

**Firma del Manejador:**
```hemlock
fn handler(signum: i32) {
    // signum contiene el numero de senal
}
```

**Ver Tambien:**
- [Constantes de senal](#constantes-de-senal)
- `raise()`

---

### raise

Envia senal al proceso actual.

**Firma:**
```hemlock
raise(signum: i32): null
```

**Parametros:**
- `signum` - Numero de senal a lanzar

**Retorna:** `null`

**Ejemplos:**
```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

raise(SIGUSR1);
raise(SIGUSR1);
print(count);  // 2
```

---

## Variables Globales

### args

Array de argumentos de linea de comandos.

**Tipo:** `array` de strings

**Estructura:**
- `args[0]` - Nombre del archivo de script
- `args[1..n]` - Argumentos de linea de comandos

**Ejemplos:**
```bash
# Comando: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// Iterar argumentos
let i = 1;
while (i < args.length) {
    print("Argumento", i, ":", args[i]);
    i = i + 1;
}
```

**Comportamiento en REPL:** En el REPL, `args.length` es 0 (array vacio)

---

## Constantes de Senal

Constantes de senal POSIX estandar (valores i32):

### Interrupcion y Terminacion

| Constante  | Valor | Descripcion                            |
|------------|-------|----------------------------------------|
| `SIGINT`   | 2     | Interrupcion desde teclado (Ctrl+C)    |
| `SIGTERM`  | 15    | Solicitud de terminacion               |
| `SIGQUIT`  | 3     | Salir desde teclado (Ctrl+\)           |
| `SIGHUP`   | 1     | Colgado detectado en terminal controladora |
| `SIGABRT`  | 6     | Senal de abortar                       |

### Definidas por Usuario

| Constante  | Valor | Descripcion                |
|------------|-------|----------------------------|
| `SIGUSR1`  | 10    | Senal definida por usuario 1 |
| `SIGUSR2`  | 12    | Senal definida por usuario 2 |

### Control de Proceso

| Constante  | Valor | Descripcion                     |
|------------|-------|---------------------------------|
| `SIGALRM`  | 14    | Temporizador de alarma          |
| `SIGCHLD`  | 17    | Cambio de estado de proceso hijo |
| `SIGCONT`  | 18    | Continuar si esta detenido      |
| `SIGSTOP`  | 19    | Detener proceso (no se puede capturar) |
| `SIGTSTP`  | 20    | Parada de terminal (Ctrl+Z)     |

### E/S

| Constante  | Valor | Descripcion                        |
|------------|-------|------------------------------------|
| `SIGPIPE`  | 13    | Tuberia rota                       |
| `SIGTTIN`  | 21    | Lectura de terminal en segundo plano |
| `SIGTTOU`  | 22    | Escritura de terminal en segundo plano |

**Ejemplos:**
```hemlock
fn handle_signal(sig) {
    if (sig == SIGINT) {
        print("Interrupcion detectada");
    }
    if (sig == SIGTERM) {
        print("Terminacion solicitada");
    }
}

signal(SIGINT, handle_signal);
signal(SIGTERM, handle_signal);
```

**Nota:** `SIGKILL` (9) y `SIGSTOP` (19) no pueden capturarse ni ignorarse.

---

## Funciones Matematicas/Aritmeticas

### div

Division entera que retorna un flotante.

**Firma:**
```hemlock
div(a: number, b: number): f64
```

**Parametros:**
- `a` - Dividendo
- `b` - Divisor

**Retorna:** Piso de `a / b` como flotante (f64)

**Ejemplos:**
```hemlock
let result = div(7, 2);    // 3.0 (no 3.5)
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0 (piso redondea hacia infinito negativo)
```

**Nota:** En Hemlock, el operador `/` siempre retorna un flotante. Use `div()` para division entera cuando necesite la parte entera como flotante, o `divi()` cuando necesite un resultado entero.

---

### divi

Division entera que retorna un entero.

**Firma:**
```hemlock
divi(a: number, b: number): i64
```

**Parametros:**
- `a` - Dividendo
- `b` - Divisor

**Retorna:** Piso de `a / b` como entero (i64)

**Ejemplos:**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4 (piso redondea hacia infinito negativo)
```

**Comparacion:**
```hemlock
print(7 / 2);      // 3.5 (division regular, siempre flotante)
print(div(7, 2));  // 3.0 (division entera, resultado flotante)
print(divi(7, 2)); // 3   (division entera, resultado entero)
```

---

## Funciones de Gestion de Memoria

Vea la [API de Memoria](memory-api.md) para referencia completa:
- `alloc(size)` - Asignar memoria cruda
- `free(ptr)` - Liberar memoria
- `buffer(size)` - Asignar buffer seguro
- `memset(ptr, byte, size)` - Llenar memoria
- `memcpy(dest, src, size)` - Copiar memoria
- `realloc(ptr, new_size)` - Redimensionar asignacion

### sizeof

Obtiene el tamano de un tipo en bytes.

**Firma:**
```hemlock
sizeof(type): i32
```

**Parametros:**
- `type` - Una constante de tipo (`i32`, `f64`, `ptr`, etc.) o string de nombre de tipo

**Retorna:** Tamano en bytes como `i32`

**Ejemplos:**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// Usando alias de tipo
print(sizeof(byte));     // 1 (igual que u8)
print(sizeof(integer));  // 4 (igual que i32)
print(sizeof(number));   // 8 (igual que f64)

// Forma string tambien funciona
print(sizeof("i32"));    // 4
```

**Tipos Soportados:**
| Tipo | Tamano | Alias |
|------|--------|-------|
| `i8` | 1 | - |
| `i16` | 2 | - |
| `i32` | 4 | `integer` |
| `i64` | 8 | - |
| `u8` | 1 | `byte` |
| `u16` | 2 | - |
| `u32` | 4 | - |
| `u64` | 8 | - |
| `f32` | 4 | - |
| `f64` | 8 | `number` |
| `ptr` | 8 | - |
| `rune` | 4 | - |
| `bool` | 1 | - |

**Ver Tambien:** `talloc()` para asignacion tipada

---

### talloc

Asigna memoria para un array tipado (asignacion consciente del tipo).

**Firma:**
```hemlock
talloc(type, count: i32): ptr
```

**Parametros:**
- `type` - Una constante de tipo (`i32`, `f64`, `ptr`, etc.)
- `count` - Numero de elementos a asignar

**Retorna:** `ptr` a memoria asignada, o `null` en fallo

**Ejemplos:**
```hemlock
// Asignar array de 10 i32s (40 bytes)
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// Asignar array de 5 f64s (40 bytes)
let float_arr = talloc(f64, 5);

// Asignar array de 100 bytes
let byte_arr = talloc(u8, 100);

// No olvide liberar!
free(int_arr);
free(float_arr);
free(byte_arr);
```

**Comparacion con alloc:**
```hemlock
// Estos son equivalentes:
let p1 = talloc(i32, 10);      // Consciente del tipo: 10 i32s
let p2 = alloc(sizeof(i32) * 10);  // Calculo manual

// talloc es mas claro y menos propenso a errores
```

**Manejo de Errores:**
- Retorna `null` si la asignacion falla
- Sale con error si count no es positivo
- Verifica desbordamiento de tamano (count * tamano_elemento)

**Ver Tambien:** `alloc()`, `sizeof()`, `free()`

---

## Ayudantes de Puntero FFI

Estas funciones ayudan a leer y escribir valores tipados en memoria cruda, utiles para FFI y manipulacion de memoria de bajo nivel.

### ptr_null

Crea un puntero nulo.

**Firma:**
```hemlock
ptr_null(): ptr
```

**Retorna:** Un puntero nulo

**Ejemplo:**
```hemlock
let p = ptr_null();
if (p == null) {
    print("El puntero es nulo");
}
```

---

### ptr_offset

Calcula desplazamiento de puntero (aritmetica de punteros).

**Firma:**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**Parametros:**
- `ptr` - Puntero base
- `index` - Indice del elemento
- `element_size` - Tamano de cada elemento en bytes

**Retorna:** Puntero al elemento en el indice dado

**Ejemplo:**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### Funciones de Lectura de Puntero

Lee valores tipados desde memoria.

| Funcion | Firma | Retorna | Descripcion |
|---------|-------|---------|-------------|
| `ptr_read_i8` | `(ptr)` | `i8` | Lee entero con signo de 8 bits |
| `ptr_read_i16` | `(ptr)` | `i16` | Lee entero con signo de 16 bits |
| `ptr_read_i32` | `(ptr)` | `i32` | Lee entero con signo de 32 bits |
| `ptr_read_i64` | `(ptr)` | `i64` | Lee entero con signo de 64 bits |
| `ptr_read_u8` | `(ptr)` | `u8` | Lee entero sin signo de 8 bits |
| `ptr_read_u16` | `(ptr)` | `u16` | Lee entero sin signo de 16 bits |
| `ptr_read_u32` | `(ptr)` | `u32` | Lee entero sin signo de 32 bits |
| `ptr_read_u64` | `(ptr)` | `u64` | Lee entero sin signo de 64 bits |
| `ptr_read_f32` | `(ptr)` | `f32` | Lee flotante de 32 bits |
| `ptr_read_f64` | `(ptr)` | `f64` | Lee flotante de 64 bits |
| `ptr_read_ptr` | `(ptr)` | `ptr` | Lee valor de puntero |

**Ejemplo:**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### Funciones de Escritura de Puntero

Escribe valores tipados a memoria.

| Funcion | Firma | Retorna | Descripcion |
|---------|-------|---------|-------------|
| `ptr_write_i8` | `(ptr, value)` | `null` | Escribe entero con signo de 8 bits |
| `ptr_write_i16` | `(ptr, value)` | `null` | Escribe entero con signo de 16 bits |
| `ptr_write_i32` | `(ptr, value)` | `null` | Escribe entero con signo de 32 bits |
| `ptr_write_i64` | `(ptr, value)` | `null` | Escribe entero con signo de 64 bits |
| `ptr_write_u8` | `(ptr, value)` | `null` | Escribe entero sin signo de 8 bits |
| `ptr_write_u16` | `(ptr, value)` | `null` | Escribe entero sin signo de 16 bits |
| `ptr_write_u32` | `(ptr, value)` | `null` | Escribe entero sin signo de 32 bits |
| `ptr_write_u64` | `(ptr, value)` | `null` | Escribe entero sin signo de 64 bits |
| `ptr_write_f32` | `(ptr, value)` | `null` | Escribe flotante de 32 bits |
| `ptr_write_f64` | `(ptr, value)` | `null` | Escribe flotante de 64 bits |
| `ptr_write_ptr` | `(ptr, value)` | `null` | Escribe valor de puntero |

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### Conversion Buffer/Puntero

#### buffer_ptr

Obtiene puntero crudo desde un buffer.

**Firma:**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**Ejemplo:**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// Ahora p apunta a la misma memoria que buf
```

#### ptr_to_buffer

Crea un envoltorio de buffer alrededor de un puntero crudo.

**Firma:**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**Ejemplo:**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // Ahora tiene verificacion de limites
// Nota: liberar buf liberara la memoria subyacente
```

---

## Funciones de E/S de Archivos

Vea la [API de Archivos](file-api.md) para referencia completa:
- `open(path, mode?)` - Abrir archivo

---

## Funciones de Concurrencia

Vea la [API de Concurrencia](concurrency-api.md) para referencia completa:
- `spawn(fn, args...)` - Generar tarea
- `join(task)` - Esperar tarea
- `detach(task)` - Desvincular tarea
- `channel(capacity)` - Crear canal

### apply

Llama una funcion dinamicamente con un array de argumentos.

**Firma:**
```hemlock
apply(fn: function, args: array): any
```

**Parametros:**
- `fn` - La funcion a llamar
- `args` - Array de argumentos a pasar a la funcion

**Retorna:** El valor de retorno de la funcion llamada

**Ejemplos:**
```hemlock
fn add(a, b) {
    return a + b;
}

// Llamar con array de argumentos
let result = apply(add, [2, 3]);
print(result);  // 5

// Despacho dinamico
let operations = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calculate(op: string, args: array) {
    return apply(operations[op], args);
}

print(calculate("add", [10, 5]));  // 15
print(calculate("mul", [10, 5]));  // 50
print(calculate("sub", [10, 5]));  // 5

// Argumentos variables
fn sum(...nums) {
    let total = 0;
    for (n in nums) {
        total = total + n;
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5];
print(apply(sum, numbers));  // 15
```

**Casos de Uso:**
- Despacho dinamico de funciones basado en valores en tiempo de ejecucion
- Llamar funciones con listas de argumentos variables
- Implementar utilidades de orden superior (map, filter, etc.)
- Sistemas de plugins/extensiones

---

### select

Espera datos de multiples canales, retornando cuando alguno tenga datos.

**Firma:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parametros:**
- `channels` - Array de valores de canal
- `timeout_ms` (opcional) - Timeout en milisegundos (-1 u omitir para infinito)

**Retorna:**
- `{ channel, value }` - Objeto con el canal que tenia datos y el valor recibido
- `null` - En timeout

**Ejemplos:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Tareas productoras
spawn(fn() {
    sleep(100);
    ch1.send("desde canal 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("desde canal 2");
});

// Esperar primer mensaje
let result = select([ch1, ch2]);
print(result.value);  // "desde canal 2" (llego primero)

// Con timeout
let result2 = select([ch1, ch2], 1000);  // Esperar hasta 1 segundo
if (result2 == null) {
    print("Timeout - no se recibieron datos");
} else {
    print("Recibido:", result2.value);
}

// Bucle select continuo
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("Sin actividad por 5 segundos");
        break;
    }
    print("Mensaje recibido:", msg.value);
}
```

**Comportamiento:**
- Bloquea hasta que un canal tenga datos o expire el timeout
- Retorna inmediatamente si un canal ya tiene datos
- Si el canal esta cerrado y vacio, retorna `{ channel, value: null }`
- Sondea canales en orden (el primer canal listo gana)

**Casos de Uso:**
- Multiplexar multiples productores
- Implementar timeouts en operaciones de canal
- Construir bucles de eventos con multiples fuentes

---

## Tabla Resumen

### Funciones

| Funcion    | Categoria       | Retorna      | Descripcion                     |
|------------|-----------------|--------------|----------------------------------|
| `print`    | E/S             | `null`       | Imprimir a stdout               |
| `read_line`| E/S             | `string?`    | Leer linea desde stdin          |
| `eprint`   | E/S             | `null`       | Imprimir a stderr               |
| `typeof`   | Tipo            | `string`     | Obtener nombre de tipo          |
| `exec`     | Comando         | `object`     | Ejecutar comando de shell       |
| `exec_argv`| Comando         | `object`     | Ejecutar con array de argumentos |
| `assert`   | Error           | `null`       | Afirmar condicion o salir       |
| `panic`    | Error           | `never`      | Error irrecuperable (sale)      |
| `signal`   | Senal           | `function?`  | Registrar manejador de senal    |
| `raise`    | Senal           | `null`       | Enviar senal al proceso         |
| `alloc`    | Memoria         | `ptr`        | Asignar memoria cruda           |
| `talloc`   | Memoria         | `ptr`        | Asignacion tipada               |
| `sizeof`   | Memoria         | `i32`        | Obtener tamano de tipo en bytes |
| `free`     | Memoria         | `null`       | Liberar memoria                 |
| `buffer`   | Memoria         | `buffer`     | Asignar buffer seguro           |
| `memset`   | Memoria         | `null`       | Llenar memoria                  |
| `memcpy`   | Memoria         | `null`       | Copiar memoria                  |
| `realloc`  | Memoria         | `ptr`        | Redimensionar asignacion        |
| `open`     | E/S Archivo     | `file`       | Abrir archivo                   |
| `spawn`    | Concurrencia    | `task`       | Generar tarea concurrente       |
| `join`     | Concurrencia    | `any`        | Esperar resultado de tarea      |
| `detach`   | Concurrencia    | `null`       | Desvincular tarea               |
| `channel`  | Concurrencia    | `channel`    | Crear canal de comunicacion     |
| `select`   | Concurrencia    | `object?`    | Esperar en multiples canales    |
| `apply`    | Funciones       | `any`        | Llamar funcion con array de args |

### Variables Globales

| Variable   | Tipo     | Descripcion                       |
|------------|----------|-----------------------------------|
| `args`     | `array`  | Argumentos de linea de comandos   |

### Constantes

| Constante  | Tipo  | Categoria | Valor | Descripcion               |
|------------|-------|----------|-------|---------------------------|
| `SIGINT`   | `i32` | Senal    | 2     | Interrupcion de teclado   |
| `SIGTERM`  | `i32` | Senal    | 15    | Solicitud de terminacion  |
| `SIGQUIT`  | `i32` | Senal    | 3     | Salir de teclado          |
| `SIGHUP`   | `i32` | Senal    | 1     | Colgado                   |
| `SIGABRT`  | `i32` | Senal    | 6     | Abortar                   |
| `SIGUSR1`  | `i32` | Senal    | 10    | Definida por usuario 1    |
| `SIGUSR2`  | `i32` | Senal    | 12    | Definida por usuario 2    |
| `SIGALRM`  | `i32` | Senal    | 14    | Temporizador de alarma    |
| `SIGCHLD`  | `i32` | Senal    | 17    | Cambio de estado de hijo  |
| `SIGCONT`  | `i32` | Senal    | 18    | Continuar                 |
| `SIGSTOP`  | `i32` | Senal    | 19    | Parar (no capturable)     |
| `SIGTSTP`  | `i32` | Senal    | 20    | Parada de terminal        |
| `SIGPIPE`  | `i32` | Senal    | 13    | Tuberia rota              |
| `SIGTTIN`  | `i32` | Senal    | 21    | Lectura terminal segundo plano |
| `SIGTTOU`  | `i32` | Senal    | 22    | Escritura terminal segundo plano |

---

## Ver Tambien

- [Sistema de Tipos](type-system.md) - Tipos y conversiones
- [API de Memoria](memory-api.md) - Funciones de asignacion de memoria
- [API de Archivos](file-api.md) - Funciones de E/S de archivos
- [API de Concurrencia](concurrency-api.md) - Funciones async/concurrencia
- [API de Strings](string-api.md) - Metodos de string
- [API de Arrays](array-api.md) - Metodos de array
