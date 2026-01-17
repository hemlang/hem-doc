# Interfaz de Funciones Foraneas (FFI) en Hemlock

Hemlock proporciona **FFI (Interfaz de Funciones Foraneas)** para llamar funciones de C desde bibliotecas compartidas usando libffi, habilitando la integracion con bibliotecas C existentes y APIs del sistema.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Estado Actual](#estado-actual)
- [Tipos Soportados](#tipos-soportados)
- [Conceptos Basicos](#conceptos-basicos)
- [Exportando Funciones FFI](#exportando-funciones-ffi)
- [Casos de Uso](#casos-de-uso)
- [Desarrollo Futuro](#desarrollo-futuro)
- [Callbacks FFI](#callbacks-ffi)
- [Structs FFI](#structs-ffi)
- [Exportando Tipos de Struct](#exportando-tipos-de-struct)
- [Limitaciones Actuales](#limitaciones-actuales)
- [Mejores Practicas](#mejores-practicas)

## Vision General

La Interfaz de Funciones Foraneas (FFI) permite a los programas de Hemlock:
- Llamar funciones de C desde bibliotecas compartidas (.so, .dylib, .dll)
- Usar bibliotecas C existentes sin escribir codigo envolvente
- Acceder a APIs del sistema directamente
- Integrarse con bibliotecas nativas de terceros
- Conectar Hemlock con funcionalidad de bajo nivel del sistema

**Capacidades clave:**
- Carga dinamica de bibliotecas
- Vinculacion de funciones C
- Conversion automatica de tipos entre Hemlock y tipos C
- Soporte para todos los tipos primitivos
- Implementacion basada en libffi para portabilidad

## Estado Actual

El soporte FFI esta disponible en Hemlock con las siguientes caracteristicas:

**Implementado:**
- ✅ Llamar funciones C desde bibliotecas compartidas
- ✅ Soporte para todos los tipos primitivos (enteros, flotantes, punteros)
- ✅ Conversion automatica de tipos
- ✅ Implementacion basada en libffi
- ✅ Carga dinamica de bibliotecas
- ✅ **Callbacks de punteros a funcion** - Pasar funciones de Hemlock a C
- ✅ **Exportar funciones extern** - Compartir bindings FFI entre modulos
- ✅ **Paso de structs y valores de retorno** - Pasar structs compatibles con C por valor
- ✅ **Ayudantes de puntero completos** - Leer/escribir todos los tipos (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Conversion buffer/puntero** - `buffer_ptr()`, `ptr_to_buffer()`
- ✅ **Tamanos de tipos FFI** - `ffi_sizeof()` para tamanos de tipo conscientes de la plataforma
- ✅ **Tipos de plataforma** - Soporte para `size_t`, `usize`, `isize`, `intptr_t`

**En Desarrollo:**
- 🔄 Ayudantes de marshaling de strings
- 🔄 Mejoras en manejo de errores

**Cobertura de Pruebas:**
- Pruebas FFI pasando incluyendo pruebas de callback
- Llamada basica de funciones verificada
- Conversion de tipos probada
- Integracion de callback qsort probada

## Tipos Soportados

### Tipos Primitivos

Los siguientes tipos de Hemlock pueden pasarse a/desde funciones C:

| Tipo Hemlock | Tipo C | Tamano | Notas |
|--------------|--------|--------|-------|
| `i8` | `int8_t` | 1 byte | Entero con signo de 8 bits |
| `i16` | `int16_t` | 2 bytes | Entero con signo de 16 bits |
| `i32` | `int32_t` | 4 bytes | Entero con signo de 32 bits |
| `i64` | `int64_t` | 8 bytes | Entero con signo de 64 bits |
| `u8` | `uint8_t` | 1 byte | Entero sin signo de 8 bits |
| `u16` | `uint16_t` | 2 bytes | Entero sin signo de 16 bits |
| `u32` | `uint32_t` | 4 bytes | Entero sin signo de 32 bits |
| `u64` | `uint64_t` | 8 bytes | Entero sin signo de 64 bits |
| `f32` | `float` | 4 bytes | Punto flotante de 32 bits |
| `f64` | `double` | 8 bytes | Punto flotante de 64 bits |
| `ptr` | `void*` | 8 bytes | Puntero crudo |

### Conversion de Tipos

**Conversiones automaticas:**
- Enteros de Hemlock → Enteros de C (con verificacion de rango)
- Flotantes de Hemlock → Flotantes de C
- Punteros de Hemlock → Punteros de C
- Valores de retorno de C → Valores de Hemlock

**Mapeos de tipo de ejemplo:**
```hemlock
// Hemlock → C
let i: i32 = 42;         // → int32_t (4 bytes)
let f: f64 = 3.14;       // → double (8 bytes)
let p: ptr = alloc(64);  // → void* (8 bytes)

// C → Hemlock (valores de retorno)
// int32_t foo() → i32
// double bar() → f64
// void* baz() → ptr
```

## Conceptos Basicos

### Bibliotecas Compartidas

FFI funciona con bibliotecas compartidas compiladas:

**Linux:** archivos `.so`
```
libexample.so
/usr/lib/libm.so
```

**macOS:** archivos `.dylib`
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** archivos `.dll`
```
example.dll
kernel32.dll
```

### Firmas de Funcion

Las funciones C deben tener firmas conocidas para que FFI funcione correctamente:

```c
// Firmas de funcion C de ejemplo
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

Estas pueden llamarse desde Hemlock una vez que la biblioteca este cargada y las funciones vinculadas.

### Compatibilidad de Plataforma

FFI usa **libffi** para portabilidad:
- Funciona en x86, x86-64, ARM, ARM64
- Maneja convenciones de llamada automaticamente
- Abstrae detalles ABI especificos de la plataforma
- Soporta Linux, macOS, Windows (con libffi apropiado)

## Exportando Funciones FFI

Las funciones FFI declaradas con `extern fn` pueden exportarse desde modulos, permitiendote crear envoltorios de biblioteca reutilizables que pueden compartirse entre multiples archivos.

### Sintaxis Basica de Exportacion

```hemlock
// string_utils.hml - Un modulo de biblioteca envolviendo funciones de strings de C
import "libc.so.6";

// Exportar la funcion extern directamente
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// Tambien puedes exportar funciones envolventes junto con funciones extern
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### Importando Funciones FFI Exportadas

```hemlock
// main.hml - Usando las funciones FFI exportadas
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hello, World!";
print(strlen(msg));           // 13 - llamada extern directa
print(string_length(msg));    // 13 - funcion envolvente

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### Casos de Uso para Export Extern

**1. Abstraccion de Plataforma**
```hemlock
// platform.hml - Abstraer diferencias de plataforma
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. Envoltorios de Biblioteca**
```hemlock
// crypto_lib.hml - Envolver funciones de biblioteca crypto
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Agregar envoltorios amigables para Hemlock
export fn sha256_string(s: string): string {
    // Implementacion usando la funcion extern
}
```

**3. Declaraciones FFI Centralizadas**
```hemlock
// libc.hml - Modulo central para bindings de libc
import "libc.so.6";

// Funciones de string
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// Funciones de memoria
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// Funciones de proceso
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

Luego usar en todo tu proyecto:
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

### Combinando con Exportaciones Regulares

Puedes mezclar funciones extern exportadas con exportaciones de funciones regulares:

```hemlock
// math_extended.hml
import "libm.so.6";

// Exportar funciones C crudas
export extern fn sin(x: f64): f64;
export extern fn cos(x: f64): f64;
export extern fn tan(x: f64): f64;

// Exportar funciones de Hemlock que las usan
export fn deg_to_rad(degrees: f64): f64 {
    return degrees * 3.14159265359 / 180.0;
}

export fn sin_degrees(degrees: f64): f64 {
    return sin(deg_to_rad(degrees));
}
```

### Bibliotecas Especificas de Plataforma

Al exportar funciones extern, recuerda que los nombres de biblioteca difieren por plataforma:

```hemlock
// Para Linux
import "libc.so.6";

// Para macOS (enfoque diferente necesario)
import "libSystem.B.dylib";
```

Actualmente, la sintaxis `import "library"` de Hemlock usa rutas de biblioteca estaticas, por lo que pueden necesitarse modulos especificos de plataforma para codigo FFI multiplataforma.

## Casos de Uso

### 1. Bibliotecas del Sistema

Acceder a funciones de la biblioteca estandar de C:

**Funciones matematicas:**
```hemlock
// Llamar sqrt desde libm
let result = sqrt(16.0);  // 4.0
```

**Asignacion de memoria:**
```hemlock
// Llamar malloc/free desde libc
let ptr = malloc(1024);
free(ptr);
```

### 2. Bibliotecas de Terceros

Usar bibliotecas C existentes:

**Ejemplo: Procesamiento de imagenes**
```hemlock
// Cargar libpng o libjpeg
// Procesar imagenes usando funciones de biblioteca C
```

**Ejemplo: Criptografia**
```hemlock
// Usar OpenSSL o libsodium
// Encriptacion/desencriptacion via FFI
```

### 3. APIs del Sistema

Llamadas al sistema directas:

**Ejemplo: APIs POSIX**
```hemlock
// Llamar getpid, getuid, etc.
// Acceder a funcionalidad de bajo nivel del sistema
```

### 4. Codigo Critico en Rendimiento

Llamar implementaciones C optimizadas:

```hemlock
// Usar bibliotecas C altamente optimizadas
// Operaciones SIMD, codigo vectorizado
// Funciones aceleradas por hardware
```

### 5. Acceso a Hardware

Interfaz con bibliotecas de hardware:

```hemlock
// Control GPIO en sistemas embebidos
// Comunicacion con dispositivos USB
// Acceso a puerto serial
```

### 6. Integracion de Codigo Legado

Reutilizar bases de codigo C existentes:

```hemlock
// Llamar funciones de aplicaciones C legadas
// Migrar gradualmente a Hemlock
// Preservar codigo C funcionando
```

## Desarrollo Futuro

### Caracteristicas Planeadas

**1. Soporte de Structs**
```hemlock
// Futuro: Pasar/retornar structs de C
define Point {
    x: f64,
    y: f64,
}

let p = Point { x: 1.0, y: 2.0 };
c_function_with_struct(p);
```

**2. Manejo de Arrays/Buffers**
```hemlock
// Futuro: Mejor paso de arrays
let arr = [1, 2, 3, 4, 5];
process_array(arr);  // Pasar a funcion C
```

**3. Callbacks de Punteros a Funcion** ✅ (Implementado!)
```hemlock
// Pasar funciones de Hemlock a C como callbacks
fn my_compare(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    return va - vb;
}

// Crear un puntero a funcion llamable desde C
let cmp = callback(my_compare, ["ptr", "ptr"], "i32");

// Usar con qsort o cualquier funcion C que espera un callback
qsort(arr, count, elem_size, cmp);

// Limpiar cuando termines
callback_free(cmp);
```

**4. Marshaling de Strings**
```hemlock
// Futuro: Conversion automatica de strings
let s = "hello";
c_string_function(s);  // Auto-convertir a string C
```

**5. Manejo de Errores**
```hemlock
// Futuro: Mejor reporte de errores
try {
    let result = risky_c_function();
} catch (e) {
    print("FFI error: " + e);
}
```

**6. Seguridad de Tipos**
```hemlock
// Futuro: Anotaciones de tipo para FFI
@ffi("libm.so")
fn sqrt(x: f64): f64;

let result = sqrt(16.0);  // Verificado por tipos
```

### Caracteristicas

**v1.0:**
- ✅ FFI basico con tipos primitivos
- ✅ Carga dinamica de bibliotecas
- ✅ Llamada de funciones
- ✅ Soporte de callbacks via clausuras libffi

**Futuro:**
- Soporte de structs
- Mejoras en manejo de arrays
- Generacion automatica de bindings

## Callbacks FFI

Hemlock soporta pasar funciones a codigo C como callbacks usando clausuras libffi. Esto habilita la integracion con APIs de C que esperan punteros a funcion, como `qsort`, bucles de eventos y bibliotecas basadas en callbacks.

### Creando Callbacks

Usa `callback()` para crear un puntero a funcion llamable desde C a partir de una funcion de Hemlock:

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**Parametros:**
- `function`: Una funcion de Hemlock para envolver
- `param_types`: Array de strings de nombres de tipo (ej. `["ptr", "i32"]`)
- `return_type`: String de tipo de retorno (ej. `"i32"`, `"void"`)

**Tipos de callback soportados:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Enteros con signo
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Enteros sin signo
- `"f32"`, `"f64"` - Punto flotante
- `"ptr"` - Puntero
- `"void"` - Sin valor de retorno
- `"bool"` - Booleano

### Ejemplo: qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// Funcion de comparacion para enteros (orden ascendente)
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// Asignar array de 5 enteros
let arr = alloc(20);  // 5 * 4 bytes
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// Crear callback y ordenar
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// El array ahora esta ordenado: [1, 2, 5, 8, 9]

// Limpiar
callback_free(cmp);
free(arr);
```

### Funciones Auxiliares de Puntero

Hemlock proporciona funciones auxiliares completas para trabajar con punteros crudos. Estas son esenciales para callbacks FFI y manipulacion directa de memoria.

#### Auxiliares de Tipos Enteros

| Funcion | Descripcion |
|---------|-------------|
| `ptr_deref_i8(ptr)` | Dereferenciar puntero, leer i8 |
| `ptr_deref_i16(ptr)` | Dereferenciar puntero, leer i16 |
| `ptr_deref_i32(ptr)` | Dereferenciar puntero, leer i32 |
| `ptr_deref_i64(ptr)` | Dereferenciar puntero, leer i64 |
| `ptr_deref_u8(ptr)` | Dereferenciar puntero, leer u8 |
| `ptr_deref_u16(ptr)` | Dereferenciar puntero, leer u16 |
| `ptr_deref_u32(ptr)` | Dereferenciar puntero, leer u32 |
| `ptr_deref_u64(ptr)` | Dereferenciar puntero, leer u64 |
| `ptr_write_i8(ptr, value)` | Escribir i8 en ubicacion del puntero |
| `ptr_write_i16(ptr, value)` | Escribir i16 en ubicacion del puntero |
| `ptr_write_i32(ptr, value)` | Escribir i32 en ubicacion del puntero |
| `ptr_write_i64(ptr, value)` | Escribir i64 en ubicacion del puntero |
| `ptr_write_u8(ptr, value)` | Escribir u8 en ubicacion del puntero |
| `ptr_write_u16(ptr, value)` | Escribir u16 en ubicacion del puntero |
| `ptr_write_u32(ptr, value)` | Escribir u32 en ubicacion del puntero |
| `ptr_write_u64(ptr, value)` | Escribir u64 en ubicacion del puntero |

#### Auxiliares de Tipos Flotantes

| Funcion | Descripcion |
|---------|-------------|
| `ptr_deref_f32(ptr)` | Dereferenciar puntero, leer f32 (float) |
| `ptr_deref_f64(ptr)` | Dereferenciar puntero, leer f64 (double) |
| `ptr_write_f32(ptr, value)` | Escribir f32 en ubicacion del puntero |
| `ptr_write_f64(ptr, value)` | Escribir f64 en ubicacion del puntero |

#### Auxiliares de Tipos Puntero

| Funcion | Descripcion |
|---------|-------------|
| `ptr_deref_ptr(ptr)` | Dereferenciar puntero a puntero |
| `ptr_write_ptr(ptr, value)` | Escribir puntero en ubicacion del puntero |
| `ptr_offset(ptr, index, size)` | Calcular desplazamiento: `ptr + index * size` |
| `ptr_read_i32(ptr)` | Leer i32 a traves de puntero a puntero (para callbacks qsort) |
| `ptr_null()` | Obtener una constante de puntero nulo |

#### Auxiliares de Conversion de Buffer

| Funcion | Descripcion |
|---------|-------------|
| `buffer_ptr(buffer)` | Obtener puntero crudo de un buffer |
| `ptr_to_buffer(ptr, size)` | Copiar datos de puntero a un nuevo buffer |

#### Funciones de Utilidad FFI

| Funcion | Descripcion |
|---------|-------------|
| `ffi_sizeof(type_name)` | Obtener tamano en bytes de un tipo FFI |

**Nombres de tipo soportados para `ffi_sizeof`:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Enteros con signo (1, 2, 4, 8 bytes)
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Enteros sin signo (1, 2, 4, 8 bytes)
- `"f32"`, `"f64"` - Flotantes (4, 8 bytes)
- `"ptr"` - Puntero (8 bytes en 64-bit)
- `"size_t"`, `"usize"` - Tipo de tamano dependiente de plataforma
- `"intptr_t"`, `"isize"` - Tipo de puntero con signo dependiente de plataforma

#### Ejemplo: Trabajando con Diferentes Tipos

```hemlock
let p = alloc(64);

// Escribir y leer enteros
ptr_write_i8(p, 42);
print(ptr_deref_i8(p));  // 42

ptr_write_i64(ptr_offset(p, 1, 8), 9000000000);
print(ptr_deref_i64(ptr_offset(p, 1, 8)));  // 9000000000

// Escribir y leer flotantes
ptr_write_f64(p, 3.14159);
print(ptr_deref_f64(p));  // 3.14159

// Puntero a puntero
let inner = alloc(4);
ptr_write_i32(inner, 999);
ptr_write_ptr(p, inner);
let retrieved = ptr_deref_ptr(p);
print(ptr_deref_i32(retrieved));  // 999

// Obtener tamanos de tipo
print(ffi_sizeof("i64"));  // 8
print(ffi_sizeof("ptr"));  // 8 (en 64-bit)

// Conversion de buffer
let buf = buffer(64);
ptr_write_i32(buffer_ptr(buf), 12345);
print(ptr_deref_i32(buffer_ptr(buf)));  // 12345

free(inner);
free(p);
```

### Liberando Callbacks

**Importante:** Siempre liberar callbacks cuando termines para prevenir fugas de memoria:

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ... usar callback ...
callback_free(cb);  // Liberar cuando termines
```

Los callbacks tambien se liberan automaticamente cuando el programa termina.

### Clausuras en Callbacks

Los callbacks capturan su entorno de clausura, por lo que pueden acceder a variables del ambito exterior:

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // Puede acceder a 'multiplier' del ambito exterior
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### Seguridad de Hilos

Las invocaciones de callback se serializan con un mutex para asegurar seguridad de hilos, ya que el interprete de Hemlock no es completamente seguro para hilos. Esto significa:
- Solo un callback puede ejecutarse a la vez
- Seguro de usar con bibliotecas C multihilo
- Puede impactar rendimiento si los callbacks se llaman muy frecuentemente desde multiples hilos

### Manejo de Errores en Callbacks

Las excepciones lanzadas en callbacks no pueden propagarse a codigo C. En su lugar:
- Se imprime una advertencia a stderr
- El callback retorna un valor por defecto (0 o NULL)
- La excepcion se registra pero no se propaga

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Something went wrong";  // Advertencia impresa, retorna 0
}
```

Para manejo de errores robusto, valida las entradas y evita lanzar en callbacks.

## Structs FFI

Hemlock soporta pasar structs por valor a funciones C. Los tipos de struct se registran automaticamente para FFI cuando los defines con anotaciones de tipo.

### Definiendo Structs Compatibles con FFI

Un struct es compatible con FFI cuando todos los campos tienen anotaciones de tipo explicitas usando tipos compatibles con FFI:

```hemlock
// Struct compatible con FFI
define Point {
    x: f64,
    y: f64,
}

// Struct compatible con FFI con multiples tipos de campo
define Rectangle {
    top_left: Point,      // Struct anidado
    width: f64,
    height: f64,
}

// NO compatible con FFI (campo sin anotacion de tipo)
define DynamicObject {
    name,                 // Sin tipo - no usable en FFI
    value,
}
```

### Usando Structs en FFI

Declarar funciones extern que usan tipos de struct:

```hemlock
// Definir el tipo de struct
define Vector2D {
    x: f64,
    y: f64,
}

// Importar la biblioteca C
import "libmath.so";

// Declarar funcion extern que toma/retorna structs
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// Usarlo naturalmente
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### Tipos de Campo Soportados

Los campos de struct deben usar estos tipos compatibles con FFI:

| Tipo Hemlock | Tipo C | Tamano |
|--------------|--------|--------|
| `i8` | `int8_t` | 1 byte |
| `i16` | `int16_t` | 2 bytes |
| `i32` | `int32_t` | 4 bytes |
| `i64` | `int64_t` | 8 bytes |
| `u8` | `uint8_t` | 1 byte |
| `u16` | `uint16_t` | 2 bytes |
| `u32` | `uint32_t` | 4 bytes |
| `u64` | `uint64_t` | 8 bytes |
| `f32` | `float` | 4 bytes |
| `f64` | `double` | 8 bytes |
| `ptr` | `void*` | 8 bytes |
| `string` | `char*` | 8 bytes |
| `bool` | `int` | varia |
| Struct anidado | struct | varia |

### Layout de Struct

Hemlock usa las reglas de layout de struct nativas de la plataforma (coincidiendo con la ABI de C):
- Los campos se alinean segun su tipo
- Se inserta padding segun necesidad
- El tamano total se rellena para alinear al miembro mas grande

```hemlock
// Ejemplo: layout compatible con C
define Mixed {
    a: i8,    // offset 0, tamano 1
              // 3 bytes padding
    b: i32,   // offset 4, tamano 4
}
// Tamano total: 8 bytes (con padding)

define Point3D {
    x: f64,   // offset 0, tamano 8
    y: f64,   // offset 8, tamano 8
    z: f64,   // offset 16, tamano 8
}
// Tamano total: 24 bytes (sin padding necesario)
```

### Structs Anidados

Los structs pueden contener otros structs:

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### Valores de Retorno de Struct

Las funciones C pueden retornar structs:

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### Limitaciones

- **Los campos de struct deben tener anotaciones de tipo** - campos sin tipos no son compatibles con FFI
- **Sin arrays en structs** - usar punteros en su lugar
- **Sin unions** - solo tipos struct son soportados
- **Los callbacks no pueden retornar structs** - usar punteros para valores de retorno de callback

### Exportando Tipos de Struct

Puedes exportar definiciones de tipo de struct desde un modulo usando `export define`:

```hemlock
// geometry.hml
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}

export fn create_rect(x: f32, y: f32, w: f32, h: f32): Rectangle {
    return { x: x, y: y, width: w, height: h };
}
```

**Importante:** Los tipos de struct exportados se registran **globalmente** cuando el modulo se carga. Se vuelven disponibles automaticamente cuando importas cualquier cosa del modulo. NO necesitas (y no puedes) importarlos explicitamente por nombre:

```hemlock
// main.hml

// BUENO - los tipos de struct estan auto-disponibles despues de cualquier import del modulo
import { create_rect } from "./geometry.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };      // Funciona - Vector2 esta globalmente disponible
let r: Rectangle = create_rect(0.0, 0.0, 100.0, 50.0);  // Funciona

// MALO - no se pueden importar tipos de struct explicitamente por nombre
import { Vector2 } from "./geometry.hml";  // Error: Undefined variable 'Vector2'
```

Este comportamiento existe porque los tipos de struct se registran en el registro global de tipos cuando el modulo carga, en lugar de almacenarse como valores en el entorno de exportacion del modulo. El tipo se vuelve disponible para todo el codigo que importa del modulo.

## Limitaciones Actuales

FFI tiene las siguientes limitaciones:

**1. Conversion Manual de Tipos**
- Debe gestionar manualmente conversiones de strings
- Sin conversion automatica de string Hemlock ↔ string C

**2. Manejo de Errores Limitado**
- Reporte basico de errores
- Las excepciones en callbacks no pueden propagarse a C

**3. Carga Manual de Bibliotecas**
- Debe cargar manualmente las bibliotecas
- Sin generacion automatica de bindings

**4. Codigo Especifico de Plataforma**
- Las rutas de biblioteca difieren por plataforma
- Debe manejar .so vs .dylib vs .dll

## Mejores Practicas

Mientras la documentacion completa de FFI todavia esta siendo desarrollada, aqui hay mejores practicas generales:

### 1. Seguridad de Tipos

```hemlock
// Ser explicito sobre tipos
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. Gestion de Memoria

```hemlock
// Recordar liberar memoria asignada
let ptr = c_malloc(1024);
// ... usar ptr
c_free(ptr);
```

### 3. Verificacion de Errores

```hemlock
// Verificar valores de retorno
let result = c_function();
if (result == null) {
    print("C function failed");
}
```

### 4. Compatibilidad de Plataforma

```hemlock
// Manejar diferencias de plataforma
// Usar extensiones de biblioteca apropiadas (.so, .dylib, .dll)
```

## Ejemplos

Para ejemplos funcionales, referirse a:
- Pruebas de callback: `/tests/ffi_callbacks/` - ejemplos de callback qsort
- Uso de FFI en stdlib: `/stdlib/hash.hml`, `/stdlib/regex.hml`, `/stdlib/crypto.hml`
- Programas de ejemplo: `/examples/` (si estan disponibles)

## Obteniendo Ayuda

FFI es una caracteristica mas nueva en Hemlock. Para preguntas o problemas:

1. Verificar la suite de pruebas para ejemplos funcionales
2. Referirse a documentacion de libffi para detalles de bajo nivel
3. Reportar bugs o solicitar caracteristicas via issues del proyecto

## Resumen

El FFI de Hemlock proporciona:

- ✅ Llamada de funciones C desde bibliotecas compartidas
- ✅ Soporte de tipos primitivos (i8-i64, u8-u64, f32, f64, ptr)
- ✅ Conversion automatica de tipos
- ✅ Portabilidad basada en libffi
- ✅ Base para integracion de bibliotecas nativas
- ✅ **Callbacks de punteros a funcion** - pasar funciones de Hemlock a C
- ✅ **Exportar funciones extern** - compartir bindings FFI entre modulos
- ✅ **Paso y retorno de structs** - pasar structs compatibles con C por valor
- ✅ **Export define** - compartir definiciones de tipo de struct entre modulos (auto-importados globalmente)
- ✅ **Auxiliares de puntero completos** - leer/escribir todos los tipos (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Conversion buffer/puntero** - `buffer_ptr()`, `ptr_to_buffer()` para marshaling de datos
- ✅ **Tamanos de tipos FFI** - `ffi_sizeof()` para tamanos de tipo conscientes de plataforma
- ✅ **Tipos de plataforma** - soporte para `size_t`, `usize`, `isize`, `intptr_t`, `uintptr_t`

**Estado actual:** FFI completamente caracterizado con tipos primitivos, structs, callbacks, exportaciones de modulo y funciones auxiliares de puntero completas

**Futuro:** Ayudantes de marshaling de strings

**Casos de uso:** Bibliotecas del sistema, bibliotecas de terceros, qsort, bucles de eventos, APIs basadas en callbacks, envoltorios de biblioteca reutilizables

## Contribuyendo

La documentacion de FFI esta siendo expandida. Si trabajas con FFI:
- Documenta tus casos de uso
- Comparte codigo de ejemplo
- Reporta problemas o limitaciones
- Sugiere mejoras

El sistema FFI esta disenado para ser practico y seguro mientras proporciona acceso de bajo nivel cuando se necesita, siguiendo la filosofia de Hemlock de "explicito sobre implicito" y "unsafe es una caracteristica, no un bug."
