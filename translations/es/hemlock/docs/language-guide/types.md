# Sistema de Tipos

Hemlock presenta un **sistema de tipos dinamico** con anotaciones de tipo opcionales y verificacion de tipos en tiempo de ejecucion.

---

## Guia de Seleccion de Tipos: Que Tipo Debo Usar?

**Nuevo en tipos?** Comienza aqui. Si estas familiarizado con sistemas de tipos, salta a [Filosofia](#filosofia).

### La Respuesta Corta

**Simplemente deja que Hemlock lo descubra:**

```hemlock
let count = 42;        // Hemlock sabe que esto es un entero
let price = 19.99;     // Hemlock sabe que esto es un decimal
let name = "Alice";    // Hemlock sabe que esto es texto
let active = true;     // Hemlock sabe que esto es si/no
```

Hemlock automaticamente elige el tipo correcto para tus valores. No *necesitas* especificar tipos.

### Cuando Agregar Anotaciones de Tipo

Agrega tipos cuando quieras:

1. **Ser especifico sobre el tamano** - `i8` vs `i64` importa para memoria o FFI
2. **Documentar tu codigo** - Los tipos muestran lo que espera una funcion
3. **Detectar errores temprano** - Hemlock verifica tipos en tiempo de ejecucion

```hemlock
// Sin tipos (funciona bien):
fn add(a, b) {
    return a + b;
}

// Con tipos (mas explicito):
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Referencia Rapida: Eligiendo Tipos Numericos

| Lo que almacenas | Tipo sugerido | Ejemplo |
|------------------|---------------|---------|
| Numeros enteros regulares | `i32` (por defecto) | `let count = 42;` |
| Numeros muy grandes | `i64` | `let population = 8000000000;` |
| Conteos nunca negativos | `u32` | `let items: u32 = 100;` |
| Bytes (0-255) | `u8` | `let pixel: u8 = 255;` |
| Decimales/fracciones | `f64` (por defecto) | `let price = 19.99;` |
| Decimales criticos para rendimiento | `f32` | `let x: f32 = 1.5;` |

### Referencia Rapida: Todos los Tipos

| Categoria | Tipos | Cuando usar |
|-----------|-------|-------------|
| **Numeros enteros** | `i8`, `i16`, `i32`, `i64` | Conteo, IDs, edades, etc. |
| **Numeros solo positivos** | `u8`, `u16`, `u32`, `u64` | Bytes, tamanos, longitudes de array |
| **Decimales** | `f32`, `f64` | Dinero, medidas, matematicas |
| **Si/No** | `bool` | Banderas, condiciones |
| **Texto** | `string` | Nombres, mensajes, cualquier texto |
| **Caracter individual** | `rune` | Letras individuales, emoji |
| **Listas** | `array` | Colecciones de valores |
| **Campos nombrados** | `object` | Agrupar datos relacionados |
| **Memoria cruda** | `ptr`, `buffer` | Programacion de bajo nivel |
| **Nada** | `null` | Ausencia de un valor |

### Escenarios Comunes

**"Solo necesito un numero"**
```hemlock
let x = 42;  // Listo! Hemlock elige i32
```

**"Necesito decimales"**
```hemlock
let price = 19.99;  // Listo! Hemlock elige f64
```

**"Estoy trabajando con bytes (archivos, red)"**
```hemlock
let byte: u8 = 255;  // rango 0-255
```

**"Necesito numeros realmente grandes"**
```hemlock
let big = 9000000000000;  // Hemlock auto-elige i64 (> max de i32)
// O se explicito:
let big: i64 = 9000000000000;
```

**"Estoy almacenando dinero"**
```hemlock
// Opcion 1: Float (simple, pero tiene limites de precision)
let price: f64 = 19.99;

// Opcion 2: Almacenar como centavos (mas preciso)
let price_cents: i32 = 1999;  // $19.99 como centavos enteros
```

**"Estoy pasando datos a codigo C (FFI)"**
```hemlock
// Coincidir tipos C exactamente
let c_int: i32 = 100;      // C 'int'
let c_long: i64 = 100;     // C 'long' (en 64-bit)
let c_char: u8 = 65;       // C 'char'
let c_double: f64 = 3.14;  // C 'double'
```

### Que Pasa Cuando Se Mezclan Tipos?

Cuando combinas diferentes tipos, Hemlock promueve al tipo "mayor":

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // result es f64 (12.5)
// El entero se convirtio en decimal automaticamente
```

**Regla general:** Los floats siempre "ganan" - mezclar cualquier entero con un float te da un float.

### Errores de Tipo

Si intentas usar el tipo incorrecto, Hemlock te lo dice en tiempo de ejecucion:

```hemlock
let age: i32 = "thirty";  // ERROR: incompatibilidad de tipos - esperaba i32, obtuvo string
```

Para convertir tipos, usa funciones constructoras de tipo:

```hemlock
let text = "42";
let number = i32(text);   // Analizar cadena a entero: 42
let back = text + "";     // Ya es una cadena
```

---

## Filosofia

- **Dinamico por defecto** - Cada valor tiene una etiqueta de tipo en tiempo de ejecucion
- **Tipado por eleccion** - Anotaciones de tipo opcionales imponen verificaciones en tiempo de ejecucion
- **Conversiones explicitas** - Las conversiones implicitas siguen reglas de promocion claras
- **Honesto sobre tipos** - `typeof()` siempre dice la verdad

## Tipos Primitivos

### Tipos Enteros

**Enteros con signo:**
```hemlock
let tiny: i8 = 127;              // 8-bit  (-128 a 127)
let small: i16 = 32767;          // 16-bit (-32768 a 32767)
let normal: i32 = 2147483647;    // 32-bit (por defecto)
let large: i64 = 9223372036854775807;  // 64-bit
```

**Enteros sin signo:**
```hemlock
let byte: u8 = 255;              // 8-bit  (0 a 255)
let word: u16 = 65535;           // 16-bit (0 a 65535)
let dword: u32 = 4294967295;     // 32-bit (0 a 4294967295)
let qword: u64 = 18446744073709551615;  // 64-bit
```

**Alias de tipo:**
```hemlock
let i: integer = 42;   // Alias para i32
let b: byte = 255;     // Alias para u8
```

### Tipos de Punto Flotante

```hemlock
let f: f32 = 3.14159;        // float de 32-bit
let d: f64 = 2.718281828;    // float de 64-bit (por defecto)
let n: number = 1.618;       // Alias para f64
```

### Tipo Booleano

```hemlock
let flag: bool = true;
let active: bool = false;
```

### Tipo String

```hemlock
let text: string = "Hello, World!";
let empty: string = "";
```

Las cadenas son **mutables**, **codificadas en UTF-8** y **asignadas en el heap**.

Ver [Strings](strings.md) para detalles completos.

### Tipo Rune

```hemlock
let ch: rune = 'A';
let emoji: rune = 'rocket';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

Los runes representan **puntos de codigo Unicode** (U+0000 a U+10FFFF).

Ver [Runes](runes.md) para detalles completos.

### Tipo Null

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null` es su propio tipo con un unico valor.

## Tipos Compuestos

### Tipo Array

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];  // Tipos mezclados permitidos
let empty: array = [];
```

Ver [Arrays](arrays.md) para detalles completos.

### Tipo Object

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

Ver [Objects](objects.md) para detalles completos.

### Tipos de Puntero

**Puntero crudo:**
```hemlock
let p: ptr = alloc(64);
// Sin verificacion de limites, gestion manual de tiempo de vida
free(p);
```

**Buffer seguro:**
```hemlock
let buf: buffer = buffer(64);
// Con verificacion de limites, rastrea longitud y capacidad
free(buf);
```

Ver [Gestion de Memoria](memory.md) para detalles completos.

## Tipos Enum

Los enums definen un conjunto de constantes nombradas:

### Enums Basicos

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// Comparacion
if (c == Color.RED) {
    print("It's red!");
}

// Switch sobre enum
switch (c) {
    case Color.RED:
        print("Stop");
        break;
    case Color.GREEN:
        print("Go");
        break;
    case Color.BLUE:
        print("Blue?");
        break;
}
```

### Enums con Valores

Los enums pueden tener valores enteros explicitos:

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### Valores Auto-incrementales

Sin valores explicitos, los enums auto-incrementan desde 0:

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// Puede mezclar valores explicitos y auto
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### Patrones de Uso de Enum

```hemlock
// Como parametros de funcion
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Urgent!");
    }
}

set_priority(Priority.HIGH);

// En objetos
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Fix bug",
    priority: Priority.HIGH
};
```

## Tipos Especiales

### Tipo File

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

Representa un manejador de archivo abierto.

### Tipo Task

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

Representa un manejador de tarea asincrona.

### Tipo Channel

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

Representa un canal de comunicacion entre tareas.

### Tipo Void

```hemlock
extern fn exit(code: i32): void;
```

Usado para funciones que no retornan un valor (solo FFI).

## Inferencia de Tipos

### Inferencia de Literales Enteros

Hemlock infiere tipos enteros basado en el rango de valores:

```hemlock
let a = 42;              // i32 (cabe en 32-bit)
let b = 5000000000;      // i64 (> max de i32)
let c = 128;             // i32
let d: u8 = 128;         // u8 (anotacion explicita)
```

**Reglas:**
- Valores en rango i32 (-2147483648 a 2147483647): inferir como `i32`
- Valores fuera del rango i32 pero dentro de i64: inferir como `i64`
- Usar anotaciones explicitas para otros tipos (i8, i16, u8, u16, u32, u64)

### Inferencia de Literales Float

```hemlock
let x = 3.14;        // f64 (por defecto)
let y: f32 = 3.14;   // f32 (explicito)
```

### Notacion Cientifica

Hemlock soporta notacion cientifica para literales numericos:

```hemlock
let a = 1e10;        // 10000000000.0 (f64)
let b = 1e-12;       // 0.000000000001 (f64)
let c = 3.14e2;      // 314.0 (f64)
let d = 2.5e-3;      // 0.0025 (f64)
let e = 1E10;        // Insensible a mayusculas
let f = 1e+5;        // Exponente positivo explicito
```

**Nota:** Cualquier literal usando notacion cientifica siempre se infiere como `f64`.

### Otra Inferencia de Tipos

```hemlock
let s = "hello";     // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## Anotaciones de Tipo

### Anotaciones de Variable

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### Anotaciones de Parametros de Funcion

```hemlock
fn greet(name: string, age: i32) {
    print("Hello, " + name + "!");
}
```

### Anotaciones de Tipo de Retorno de Funcion

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Anotaciones de Tipo de Objeto (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## Verificacion de Tipos

### Verificacion de Tipos en Tiempo de Ejecucion

Las anotaciones de tipo se verifican en **tiempo de ejecucion**, no en tiempo de compilacion:

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // Error de tiempo de ejecucion: incompatibilidad de tipos

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "hello");     // Error de tiempo de ejecucion: incompatibilidad de tipos
```

### Consultas de Tipo

Usa `typeof()` para verificar tipos de valores:

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("hello"));    // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## Conversiones de Tipo

### Promocion Implicita de Tipo

Cuando se mezclan tipos en operaciones, Hemlock promueve al tipo "superior":

**Jerarquia de Promocion (menor a mayor):**
```
i8 -> i16 -> i32 -> u32 -> i64 -> u64 -> f32 -> f64
      ^      ^      ^
     u8    u16
```

**Float siempre gana:**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result es f64 (13.5)
```

**El tamano mayor gana:**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sum es i64 (300)
```

**Preservacion de precision:** Cuando se mezclan enteros de 64-bit con f32, Hemlock promueve
a f64 para evitar perdida de precision (f32 tiene solo mantisa de 24-bit, insuficiente para i64/u64):
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // result es f64, no f32!
```

**Ejemplos:**
```hemlock
u8 + i32  -> i32
i32 + i64 -> i64
u32 + u64 -> u64
i32 + f32 -> f32    // f32 suficiente para i32
i64 + f32 -> f64    // f64 necesario para preservar precision de i64
i64 + f64 -> f64
i8 + f64  -> f64
```

### Conversion Explicita de Tipo

**Entero <-> Float:**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 -> f64 (42.0)

let x: f64 = 3.14;
let n: i32 = x;      // f64 -> i32 (3, truncado)
```

**Entero <-> Rune:**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 -> rune ('A')

let r: rune = 'Z';
let value: i32 = r;   // rune -> i32 (90)
```

**Rune -> String:**
```hemlock
let ch: rune = 'rocket';
let s: string = ch;   // rune -> string ("rocket")
```

**u8 -> Rune:**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 -> rune ('A')
```

### Funciones Constructoras de Tipo

Los nombres de tipo pueden usarse como funciones para convertir o analizar valores:

**Analizar cadenas a numeros:**
```hemlock
let n = i32("42");       // Analizar cadena a i32: 42
let f = f64("3.14159");  // Analizar cadena a f64: 3.14159
let b = bool("true");    // Analizar cadena a bool: true

// Todos los tipos numericos soportados
let a = i8("-128");      // Analizar a i8
let c = u8("255");       // Analizar a u8
let d = i16("1000");     // Analizar a i16
let e = u16("50000");    // Analizar a u16
let g = i64("9000000000000"); // Analizar a i64
let h = u64("18000000000000"); // Analizar a u64
let j = f32("1.5");      // Analizar a f32
```

**Hex y numeros negativos:**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10 (binario)
```

**Alias de tipo tambien funcionan:**
```hemlock
let x = integer("100");  // Igual que i32("100")
let y = number("1.5");   // Igual que f64("1.5")
let z = byte("200");     // Igual que u8("200")
```

**Convertir entre tipos numericos:**
```hemlock
let big = i64(42);           // i32 a i64
let truncated = i32(3.99);   // f64 a i32 (trunca a 3)
let promoted = f64(100);     // i32 a f64 (100.0)
let narrowed = i8(127);      // i32 a i8
```

**Las anotaciones de tipo realizan coercion numerica (pero NO analisis de cadenas):**
```hemlock
let f: f64 = 100;        // i32 a f64 via anotacion (OK)
let s: string = 'A';     // Rune a string via anotacion (OK)
let code: i32 = 'A';     // Rune a i32 via anotacion (obtiene codepoint, OK)

// Analisis de cadenas requiere constructores de tipo explicitos:
let n = i32("42");       // Usar constructor de tipo para analisis de cadenas
// let x: i32 = "42";    // ERROR - las anotaciones de tipo no analizan cadenas
```

**Manejo de errores:**
```hemlock
// Cadenas invalidas lanzan errores cuando usan constructores de tipo
let bad = i32("hello");  // Error de tiempo de ejecucion: no se puede analizar "hello" como i32
let overflow = u8("256"); // Error de tiempo de ejecucion: 256 fuera de rango para u8
```

**Analisis de booleanos:**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("yes");   // Error de tiempo de ejecucion: debe ser "true" o "false"
```

## Verificacion de Rango

Las anotaciones de tipo imponen verificaciones de rango en la asignacion:

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // ERROR: fuera de rango para u8

let a: i8 = 127;    // OK
let b: i8 = 128;    // ERROR: fuera de rango para i8

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // ERROR: u64 no puede ser negativo
```

## Ejemplos de Promocion de Tipo

### Tipos Enteros Mezclados

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32 (30)

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32 (300)
```

### Entero + Float

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32 (12.5)
```

### Expresiones Complejas

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64 (70.0)
// Evaluacion: b * c -> f64(60.0)
//             a + f64(60.0) -> f64(70.0)
```

## Duck Typing (Objetos)

Los objetos usan **tipado estructural** (duck typing):

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Tiene todos los campos requeridos
let p1: Person = { name: "Alice", age: 30 };

// OK: Campos extra permitidos
let p2: Person = { name: "Bob", age: 25, city: "NYC" };

// ERROR: Falta campo 'age'
let p3: Person = { name: "Carol" };

// ERROR: Tipo incorrecto para 'age'
let p4: Person = { name: "Dave", age: "thirty" };
```

**La verificacion de tipo ocurre en la asignacion:**
- Valida que todos los campos requeridos esten presentes
- Valida que los tipos de campo coincidan
- Los campos extra estan permitidos y preservados
- Establece el nombre de tipo del objeto para `typeof()`

## Campos Opcionales

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // Opcional con valor por defecto
    timeout?: i32,     // Opcional, por defecto null
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false (por defecto)
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true (sobrescrito)
```

## Alias de Tipo

Hemlock soporta alias de tipo personalizados usando la palabra clave `type`:

### Alias de Tipo Basicos

```hemlock
// Alias de tipo simple
type Integer = i32;
type Text = string;

// Usando el alias
let x: Integer = 42;
let msg: Text = "hello";
```

### Alias de Tipo de Funcion

```hemlock
// Alias de tipo de funcion
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Usando alias de tipo de funcion
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### Alias de Tipo Compuesto

```hemlock
// Combinar multiples defines en un tipo
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### Alias de Tipo Generico

```hemlock
// Alias de tipo generico
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Usando alias genericos
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Nota:** Los alias de tipo son transparentes - `typeof()` retorna el nombre del tipo subyacente, no el alias.

## Limitaciones del Sistema de Tipos

Limitaciones actuales:

- **Sin genericos en funciones** - Parametros de tipo en funciones aun no soportados
- **Sin tipos union** - No se puede expresar "A o B"
- **Sin tipos nullable** - Todos los tipos pueden ser null (usar sufijo `?` para nulabilidad explicita)

**Nota:** El compilador (`hemlockc`) proporciona verificacion de tipos en tiempo de compilacion. El interprete realiza verificacion de tipos solo en tiempo de ejecucion. Ver la [documentacion del compilador](../design/implementation.md) para detalles.

## Mejores Practicas

### Cuando Usar Anotaciones de Tipo

**USA anotaciones cuando:**
- El tipo preciso importa (ej., `u8` para valores de byte)
- Documentar interfaces de funciones
- Imponer restricciones (ej., verificaciones de rango)

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // Implementacion
}
```

**NO uses anotaciones cuando:**
- El tipo es obvio del literal
- Detalles de implementacion interna
- Ceremonia innecesaria

```hemlock
// Innecesario
let x: i32 = 42;

// Mejor
let x = 42;
```

### Patrones de Seguridad de Tipo

**Verificar antes de usar:**
```hemlock
if (typeof(value) == "i32") {
    // Seguro usar como i32
}
```

**Validar argumentos de funcion:**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "arguments must be integers";
    }
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

**Usar duck typing para flexibilidad:**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## Siguientes Pasos

- [Strings](strings.md) - Tipo string UTF-8 y operaciones
- [Runes](runes.md) - Tipo de punto de codigo Unicode
- [Arrays](arrays.md) - Tipo de array dinamico
- [Objects](objects.md) - Literales de objeto y duck typing
- [Memory](memory.md) - Tipos de puntero y buffer
