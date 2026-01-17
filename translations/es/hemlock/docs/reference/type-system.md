# Referencia del Sistema de Tipos

Referencia completa para el sistema de tipos de Hemlock, incluyendo todos los tipos primitivos y compuestos.

---

## Descripcion General

Hemlock usa un **sistema de tipos dinamico** con etiquetas de tipo en tiempo de ejecucion y anotaciones de tipo opcionales. Cada valor tiene un tipo en tiempo de ejecucion, y las conversiones de tipo siguen reglas de promocion explicitas.

**Caracteristicas Principales:**
- Verificacion de tipos en tiempo de ejecucion (interprete)
- Verificacion de tipos en tiempo de compilacion (hemlockc - habilitado por defecto)
- Anotaciones de tipo opcionales
- Inferencia de tipos automatica para literales
- Reglas de promocion de tipos explicitas
- Sin conversiones implicitas que pierdan precision

---

## Verificacion de Tipos en Tiempo de Compilacion (hemlockc)

El compilador de Hemlock (`hemlockc`) incluye un verificador de tipos en tiempo de compilacion que valida su codigo antes de generar ejecutables. Esto captura errores de tipo tempranamente sin necesidad de ejecutar el programa.

### Comportamiento por Defecto

La verificacion de tipos esta **habilitada por defecto** en hemlockc:

```bash
# La verificacion de tipos ocurre automaticamente
hemlockc program.hml -o program

# Los errores se reportan antes de la compilacion
hemlockc bad_types.hml
# Salida: 1 type error found
```

### Banderas del Compilador

| Bandera | Descripcion |
|---------|-------------|
| `--check` | Solo verificar tipos, no compilar (salir despues de validacion) |
| `--no-type-check` | Deshabilitar verificacion de tipos (no recomendado) |
| `--strict-types` | Habilitar advertencias de tipos mas estrictas |

**Ejemplos:**

```bash
# Solo validar tipos sin compilar
hemlockc --check program.hml
# Salida: program.hml: no type errors

# Deshabilitar verificacion de tipos (usar con precaucion)
hemlockc --no-type-check dynamic_code.hml -o program

# Habilitar advertencias estrictas para tipos any implicitos
hemlockc --strict-types program.hml -o program
```

### Que Valida el Verificador de Tipos

1. **Anotaciones de tipo** - Asegura que los valores asignados coincidan con los tipos declarados
2. **Llamadas a funciones** - Valida tipos de argumentos contra tipos de parametros
3. **Tipos de retorno** - Verifica que las sentencias return coincidan con el tipo de retorno declarado
4. **Uso de operadores** - Verifica que los operandos sean compatibles
5. **Acceso a propiedades** - Valida tipos de campos de objetos para objetos tipados

### Conversiones Numericas Permisivas

El verificador de tipos permite conversiones de tipos numericos en tiempo de compilacion, con validacion de rango ocurriendo en tiempo de ejecucion:

```hemlock
let x: i8 = 100;      // OK - 100 cabe en i8 (validado en tiempo de ejecucion)
let y: u8 = 255;      // OK - dentro del rango de u8
let z: f64 = 42;      // OK - i32 a f64 es seguro
```

### Soporte de Codigo Dinamico

El codigo sin anotaciones de tipo se trata como dinamico (tipo `any`) y siempre pasa el verificador de tipos:

```hemlock
let x = get_value();  // Dinamico - sin anotacion
process(x);           // OK - valores dinamicos aceptados en cualquier lugar
```

---

## Tipos Primitivos

### Tipos Numericos

#### Enteros con Signo

| Tipo   | Tamano    | Rango                                      | Alias     |
|--------|-----------|-------------------------------------------|-----------|
| `i8`   | 1 byte    | -128 a 127                                | -         |
| `i16`  | 2 bytes   | -32,768 a 32,767                          | -         |
| `i32`  | 4 bytes   | -2,147,483,648 a 2,147,483,647            | `integer` |
| `i64`  | 8 bytes   | -9,223,372,036,854,775,808 a 9,223,372,036,854,775,807 | - |

**Ejemplos:**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Alias de tipo
let x: integer = 42;  // Igual que i32
```

#### Enteros sin Signo

| Tipo   | Tamano    | Rango                     | Alias  |
|--------|-----------|---------------------------|--------|
| `u8`   | 1 byte    | 0 a 255                   | `byte` |
| `u16`  | 2 bytes   | 0 a 65,535                | -      |
| `u32`  | 4 bytes   | 0 a 4,294,967,295         | -      |
| `u64`  | 8 bytes   | 0 a 18,446,744,073,709,551,615 | - |

**Ejemplos:**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Alias de tipo
let byte_val: byte = 65;  // Igual que u8
```

#### Punto Flotante

| Tipo   | Tamano    | Precision      | Alias    |
|--------|-----------|----------------|----------|
| `f32`  | 4 bytes   | ~7 digitos     | -        |
| `f64`  | 8 bytes   | ~15 digitos    | `number` |

**Ejemplos:**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// Alias de tipo
let x: number = 2.718;  // Igual que f64
```

---

### Inferencia de Literales Enteros

Los literales enteros se tipan automaticamente basandose en su valor:

**Reglas:**
- Valores en rango i32 (-2,147,483,648 a 2,147,483,647): inferir como `i32`
- Valores fuera del rango i32 pero dentro del rango i64: inferir como `i64`
- Use anotaciones de tipo explicitas para otros tipos (i8, i16, u8, u16, u32, u64)

**Ejemplos:**
```hemlock
let small = 42;                    // i32 (cabe en i32)
let large = 5000000000;            // i64 (> maximo i32)
let max_i64 = 9223372036854775807; // i64 (INT64_MAX)
let explicit: u32 = 100;           // u32 (anotacion de tipo anula)
```

---

### Tipo Booleano

**Tipo:** `bool`

**Valores:** `true`, `false`

**Tamano:** 1 byte (internamente)

**Ejemplos:**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("trabajando");
}
```

---

### Tipos de Caracter

#### Rune

**Tipo:** `rune`

**Descripcion:** Punto de codigo Unicode (U+0000 a U+10FFFF)

**Tamano:** 4 bytes (valor de 32 bits)

**Rango:** 0 a 0x10FFFF (1,114,111)

**Sintaxis Literal:** Comillas simples `'x'`

**Ejemplos:**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// UTF-8 multi-byte
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// Secuencias de escape
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Escapes Unicode
let emoji = '\u{1F680}';   // Hasta 6 digitos hex
let max = '\u{10FFFF}';    // Punto de codigo maximo
```

**Conversiones de Tipo:**
```hemlock
// Entero a rune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// Rune a entero
let value: i32 = 'Z';       // 90

// Rune a string
let s: string = 'H';        // "H"

// u8 a rune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**Ver Tambien:** [API de Strings](string-api.md) para concatenacion de string + rune

---

### Tipo String

**Tipo:** `string`

**Descripcion:** Texto codificado en UTF-8, mutable, asignado en heap

**Codificacion:** UTF-8 (U+0000 a U+10FFFF)

**Mutabilidad:** Mutable (a diferencia de la mayoria de lenguajes)

**Propiedades:**
- `.length` - Conteo de puntos de codigo (numero de caracteres)
- `.byte_length` - Conteo de bytes (tamano de codificacion UTF-8)

**Sintaxis Literal:** Comillas dobles `"texto"`

**Ejemplos:**
```hemlock
let s = "hello";
s[0] = 'H';             // Mutar (ahora "Hello")
print(s.length);        // 5 (conteo de puntos de codigo)
print(s.byte_length);   // 5 (bytes UTF-8)

let emoji = "🚀";
print(emoji.length);        // 1 (un punto de codigo)
print(emoji.byte_length);   // 4 (cuatro bytes UTF-8)
```

**Indexacion:**
```hemlock
let s = "hello";
let ch = s[0];          // Retorna rune 'h'
s[0] = 'H';             // Establecer con rune
```

**Ver Tambien:** [API de Strings](string-api.md) para referencia completa de metodos

---

### Tipo Null

**Tipo:** `null`

**Descripcion:** El valor null (ausencia de valor)

**Tamano:** 8 bytes (internamente)

**Valor:** `null`

**Ejemplos:**
```hemlock
let x = null;
let y: i32 = null;  // ERROR: discrepancia de tipo

if (x == null) {
    print("x es null");
}
```

---

## Tipos Compuestos

### Tipo Array

**Tipo:** `array`

**Descripcion:** Array dinamico, asignado en heap, de tipos mixtos

**Propiedades:**
- `.length` - Numero de elementos

**Indexacion desde cero:** Si

**Sintaxis Literal:** `[elem1, elem2, ...]`

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipos mixtos
let mixed = [1, "hello", true, null];
```

**Ver Tambien:** [API de Arrays](array-api.md) para referencia completa de metodos

---

### Tipo Objeto

**Tipo:** `object`

**Descripcion:** Objeto estilo JavaScript con campos dinamicos

**Sintaxis Literal:** `{ campo: valor, ... }`

**Ejemplos:**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// Agregar campo dinamicamente
person.email = "alice@example.com";
```

**Definiciones de Tipo:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // Campo opcional
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### Tipos de Puntero

#### Puntero Crudo (ptr)

**Tipo:** `ptr`

**Descripcion:** Direccion de memoria cruda (inseguro)

**Tamano:** 8 bytes

**Verificacion de Limites:** Ninguna

**Ejemplos:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### Buffer (buffer)

**Tipo:** `buffer`

**Descripcion:** Envoltorio de puntero seguro con verificacion de limites

**Estructura:** Puntero + longitud + capacidad

**Propiedades:**
- `.length` - Tamano del buffer
- `.capacity` - Capacidad asignada

**Ejemplos:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificacion de limites
print(b.length);        // 64
free(b);
```

**Ver Tambien:** [API de Memoria](memory-api.md) para funciones de asignacion

---

## Tipos Especiales

### Tipo File

**Tipo:** `file`

**Descripcion:** Manejador de archivo para operaciones de E/S

**Propiedades:**
- `.path` - Ruta del archivo (string)
- `.mode` - Modo de apertura (string)
- `.closed` - Si el archivo esta cerrado (bool)

**Ver Tambien:** [API de Archivos](file-api.md)

---

### Tipo Task

**Tipo:** `task`

**Descripcion:** Manejador para tarea concurrente

**Ver Tambien:** [API de Concurrencia](concurrency-api.md)

---

### Tipo Channel

**Tipo:** `channel`

**Descripcion:** Canal de comunicacion seguro para hilos

**Ver Tambien:** [API de Concurrencia](concurrency-api.md)

---

### Tipo Function

**Tipo:** `function`

**Descripcion:** Valor de funcion de primera clase

**Ejemplos:**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Tipo Void

**Tipo:** `void`

**Descripcion:** Ausencia de valor de retorno (uso interno)

---

## Reglas de Promocion de Tipos

Cuando se mezclan tipos en operaciones, Hemlock promociona al tipo "superior":

**Jerarquia de Promocion:**
```
f64 (mayor precision)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (menor)
```

**Reglas:**
1. Flotante siempre gana sobre entero
2. Tamano mayor gana dentro de la misma categoria (int/uint/float)
3. Ambos operandos se promocionan al tipo del resultado
4. **Preservacion de precision:** i64/u64 + f32 promociona a f64 (no f32)

**Ejemplos:**
```hemlock
// Promocion por tamano
u8 + i32    → i32    // Tamano mayor gana
i32 + i64   → i64    // Tamano mayor gana
u32 + u64   → u64    // Tamano mayor gana

// Promocion a flotante
i32 + f32   → f32    // Flotante gana, f32 suficiente para i32
i64 + f32   → f64    // Promociona a f64 para preservar precision de i64
i64 + f64   → f64    // Flotante siempre gana
i8 + f64    → f64    // Flotante + mayor gana
```

**Por que i64 + f32 -> f64?**

f32 tiene solo una mantisa de 24 bits, que no puede representar precisamente enteros mayores que 2^24 (16,777,216). Como i64 puede contener valores hasta 2^63, mezclar i64 con f32 causaria perdida severa de precision. Hemlock promociona a f64 (mantisa de 53 bits) en su lugar.

---

## Verificacion de Rango

Las anotaciones de tipo imponen verificaciones de rango en asignacion:

**Asignaciones Validas:**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**Asignaciones Invalidas (Error en Tiempo de Ejecucion):**
```hemlock
let x: u8 = 256;             // ERROR: fuera de rango
let y: i8 = 128;             // ERROR: maximo es 127
let z: u64 = -1;             // ERROR: u64 no puede ser negativo
```

---

## Introspeccion de Tipos

### typeof(value)

Retorna el nombre del tipo como string.

**Firma:**
```hemlock
typeof(value: any): string
```

**Retorna:**
- Tipos primitivos: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Tipos compuestos: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Tipos especiales: `"file"`, `"task"`, `"channel"`
- Objetos tipados: Nombre de tipo personalizado (ej., `"Person"`)

**Ejemplos:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**Ver Tambien:** [Funciones Integradas](builtins.md#typeof)

---

## Conversiones de Tipo

### Conversiones Implicitas

Hemlock realiza conversiones de tipo implicitas en operaciones aritmeticas siguiendo las reglas de promocion de tipos.

**Ejemplos:**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // result es i32 (promocionado)
```

### Conversiones Explicitas

Use anotaciones de tipo para conversiones explicitas:

**Ejemplos:**
```hemlock
// Entero a flotante
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Flotante a entero (trunca)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Entero a rune
let code: rune = 65;    // 'A'

// Rune a entero
let value: i32 = 'Z';   // 90

// Rune a string
let s: string = 'H';    // "H"
```

---

## Alias de Tipo

### Alias Integrados

Hemlock proporciona alias de tipo integrados para tipos comunes:

| Alias     | Tipo Real | Uso                      |
|-----------|-----------|--------------------------|
| `integer` | `i32`     | Enteros de proposito general |
| `number`  | `f64`     | Flotantes de proposito general |
| `byte`    | `u8`      | Valores de byte          |

**Ejemplos:**
```hemlock
let count: integer = 100;       // Igual que i32
let price: number = 19.99;      // Igual que f64
let b: byte = 255;              // Igual que u8
```

### Alias de Tipo Personalizados

Defina alias de tipo personalizados usando la palabra clave `type`:

```hemlock
// Alias simples
type Integer = i32;
type Text = string;

// Alias de tipo funcion
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// Alias de tipo compuesto
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Alias de tipo generico
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**Usando alias personalizados:**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Nota:** Los alias de tipo son transparentes - `typeof()` retorna el nombre del tipo subyacente.

---

## Tipos de Funcion

Los tipos de funcion especifican la firma de valores de funcion:

### Sintaxis

```hemlock
fn(tipos_parametros): tipo_retorno
```

### Ejemplos

```hemlock
// Tipo de funcion basico
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parametro de funcion
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Funcion de orden superior retornando funcion
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tipo de funcion async
fn run_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## Tipos Compuestos (Interseccion)

Los tipos compuestos usan `&` para requerir multiples restricciones de tipo:

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// El objeto debe satisfacer todos los tipos
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Tres o mas tipos
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## Tabla Resumen

| Tipo       | Tamano   | Mutable | Asignado en Heap | Descripcion                    |
|------------|----------|---------|------------------|--------------------------------|
| `i8`-`i64` | 1-8 bytes| No      | No               | Enteros con signo              |
| `u8`-`u64` | 1-8 bytes| No      | No               | Enteros sin signo              |
| `f32`      | 4 bytes  | No      | No               | Flotante precision simple      |
| `f64`      | 8 bytes  | No      | No               | Flotante precision doble       |
| `bool`     | 1 byte   | No      | No               | Booleano                       |
| `rune`     | 4 bytes  | No      | No               | Punto de codigo Unicode        |
| `string`   | Variable | Si      | Si               | Texto UTF-8                    |
| `array`    | Variable | Si      | Si               | Array dinamico                 |
| `object`   | Variable | Si      | Si               | Objeto dinamico                |
| `ptr`      | 8 bytes  | No      | No               | Puntero crudo                  |
| `buffer`   | Variable | Si      | Si               | Envoltorio de puntero seguro   |
| `file`     | Opaco    | Si      | Si               | Manejador de archivo           |
| `task`     | Opaco    | No      | Si               | Manejador de tarea concurrente |
| `channel`  | Opaco    | Si      | Si               | Canal seguro para hilos        |
| `function` | Opaco    | No      | Si               | Valor de funcion               |
| `null`     | 8 bytes  | No      | No               | Valor null                     |

---

## Ver Tambien

- [Referencia de Operadores](operators.md) - Comportamiento de tipos en operaciones
- [Funciones Integradas](builtins.md) - Introspeccion y conversion de tipos
- [API de Strings](string-api.md) - Metodos de tipo string
- [API de Arrays](array-api.md) - Metodos de tipo array
- [API de Memoria](memory-api.md) - Operaciones de puntero y buffer
