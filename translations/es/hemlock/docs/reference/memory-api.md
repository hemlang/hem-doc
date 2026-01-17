# Referencia de la API de Memoria

Referencia completa para las funciones de gestion de memoria y tipos de puntero de Hemlock.

---

## Descripcion General

Hemlock proporciona **gestion manual de memoria** con asignacion y liberacion explicitas. La memoria se gestiona a traves de dos tipos de puntero: punteros crudos (`ptr`) y buffers seguros (`buffer`).

**Principios Clave:**
- Asignacion y liberacion explicitas
- Sin recoleccion de basura
- El usuario es responsable de llamar a `free()`
- Conteo de referencias interno para seguridad de alcance/reasignacion (ver abajo)

### Conteo de Referencias Interno

El runtime usa conteo de referencias internamente para gestionar los tiempos de vida de objetos a traves de alcances. Para la mayoria de variables locales, la limpieza es automatica.

**Automatico (sin necesidad de `free()`):**
- Variables locales de tipos con conteo de referencias (buffer, array, object, string) se liberan cuando el alcance termina
- Los valores antiguos se liberan cuando las variables se reasignan
- Los elementos de contenedores se liberan cuando los contenedores se liberan

**Se requiere `free()` manual:**
- Punteros crudos de `alloc()` - siempre
- Limpieza temprana antes de que termine el alcance
- Datos de larga duracion/globales

Vea la [Guia de Gestion de Memoria](../language-guide/memory.md#internal-reference-counting) para detalles.

---

## Tipos de Puntero

### ptr (Puntero Crudo)

**Tipo:** `ptr`

**Descripcion:** Direccion de memoria cruda sin verificacion de limites ni seguimiento.

**Tamano:** 8 bytes

**Casos de Uso:**
- Operaciones de memoria de bajo nivel
- FFI (Interfaz de Funciones Foraneas)
- Maximo rendimiento (sin sobrecarga)

**Seguridad:** Inseguro - sin verificacion de limites, el usuario debe rastrear el tiempo de vida

**Ejemplos:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer (Buffer Seguro)

**Tipo:** `buffer`

**Descripcion:** Envoltorio de puntero seguro con verificacion de limites.

**Estructura:** Puntero + longitud + capacidad + ref_count

**Propiedades:**
- `.length` - Tamano del buffer (i32)
- `.capacity` - Capacidad asignada (i32)

**Casos de Uso:**
- La mayoria de las asignaciones de memoria
- Cuando la seguridad es importante
- Arrays dinamicos

**Seguridad:** Verificacion de limites en acceso por indice

**Conteo de Referencias:** Los buffers tienen conteo de referencias interno. Se liberan automaticamente cuando el alcance termina o la variable se reasigna. Use `free()` para limpieza temprana o datos de larga duracion.

**Ejemplos:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificacion de limites
print(b.length);        // 64
free(b);
```

---

## Funciones de Asignacion de Memoria

### alloc

Asigna memoria cruda.

**Firma:**
```hemlock
alloc(size: i32): ptr
```

**Parametros:**
- `size` - Numero de bytes a asignar

**Retorna:** Puntero a la memoria asignada (`ptr`)

**Ejemplos:**
```hemlock
let p = alloc(1024);        // Asignar 1KB
memset(p, 0, 1024);         // Inicializar a cero
free(p);                    // Liberar cuando termine

// Asignar para estructura
let struct_size = 16;
let p2 = alloc(struct_size);
```

**Comportamiento:**
- Retorna memoria sin inicializar
- La memoria debe liberarse manualmente
- Retorna `null` en fallo de asignacion (el llamador debe verificar)

**Ver Tambien:** `buffer()` para alternativa mas segura

---

### buffer

Asigna buffer seguro con verificacion de limites.

**Firma:**
```hemlock
buffer(size: i32): buffer
```

**Parametros:**
- `size` - Tamano del buffer en bytes

**Retorna:** Objeto Buffer

**Ejemplos:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// Acceso con verificacion de limites
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // ERROR: fuera de limites

free(buf);
```

**Propiedades:**
- `.length` - Tamano actual (i32)
- `.capacity` - Capacidad asignada (i32)

**Comportamiento:**
- Inicializa la memoria a cero
- Proporciona verificacion de limites en acceso por indice
- Retorna `null` en fallo de asignacion (el llamador debe verificar)
- Debe liberarse manualmente

---

### free

Libera memoria asignada.

**Firma:**
```hemlock
free(ptr: ptr | buffer): null
```

**Parametros:**
- `ptr` - Puntero o buffer a liberar

**Retorna:** `null`

**Ejemplos:**
```hemlock
// Liberar puntero crudo
let p = alloc(1024);
free(p);

// Liberar buffer
let buf = buffer(256);
free(buf);
```

**Comportamiento:**
- Libera memoria asignada por `alloc()` o `buffer()`
- Doble liberacion causa crash (responsabilidad del usuario evitarlo)
- Liberar punteros invalidos causa comportamiento indefinido

**Importante:** Tu asignas, tu liberas. Sin limpieza automatica.

---

### realloc

Redimensiona memoria asignada.

**Firma:**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**Parametros:**
- `ptr` - Puntero a redimensionar
- `new_size` - Nuevo tamano en bytes

**Retorna:** Puntero a la memoria redimensionada (puede ser direccion diferente)

**Ejemplos:**
```hemlock
let p = alloc(100);
// ... usar memoria ...

// Necesita mas espacio
p = realloc(p, 200);        // Ahora 200 bytes
// ... usar memoria expandida ...

free(p);
```

**Comportamiento:**
- Puede mover la memoria a nueva ubicacion
- Preserva datos existentes (hasta el minimo del tamano antiguo/nuevo)
- El puntero antiguo es invalido despues de realloc exitoso (use el puntero retornado)
- Si new_size es menor, los datos se truncan
- Retorna `null` en fallo de asignacion (el puntero original permanece valido)

**Importante:** Siempre verifique si es `null` y actualice su variable de puntero con el resultado.

---

## Operaciones de Memoria

### memset

Llena memoria con valor de byte.

**Firma:**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**Parametros:**
- `ptr` - Puntero a memoria
- `byte` - Valor de byte a llenar (0-255)
- `size` - Numero de bytes a llenar

**Retorna:** `null`

**Ejemplos:**
```hemlock
let p = alloc(100);

// Poner memoria a cero
memset(p, 0, 100);

// Llenar con valor especifico
memset(p, 0xFF, 100);

// Inicializar buffer
let buf = alloc(256);
memset(buf, 65, 256);       // Llenar con 'A'

free(p);
free(buf);
```

**Comportamiento:**
- Escribe el valor de byte a cada byte en el rango
- El valor de byte se trunca a 8 bits (0-255)
- Sin verificacion de limites (inseguro)

---

### memcpy

Copia memoria desde origen a destino.

**Firma:**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**Parametros:**
- `dest` - Puntero destino
- `src` - Puntero origen
- `size` - Numero de bytes a copiar

**Retorna:** `null`

**Ejemplos:**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// Inicializar origen
memset(src, 65, 100);

// Copiar a destino
memcpy(dest, src, 100);

// dest ahora contiene los mismos datos que src

free(src);
free(dest);
```

**Comportamiento:**
- Copia byte por byte desde src a dest
- Sin verificacion de limites (inseguro)
- Regiones superpuestas tienen comportamiento indefinido (use con cuidado)

---

## Operaciones de Memoria Tipadas

### sizeof

Obtiene el tamano de un tipo en bytes.

**Firma:**
```hemlock
sizeof(type): i32
```

**Parametros:**
- `type` - Identificador de tipo (ej., `i32`, `f64`, `ptr`)

**Retorna:** Tamano en bytes (i32)

**Tamanos de Tipos:**

| Tipo | Tamano (bytes) |
|------|----------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**Ejemplos:**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// Calcular tamano de asignacion de array
let count = 100;
let total = sizeof(i32) * count; // 400 bytes
```

**Comportamiento:**
- Retorna 0 para tipos desconocidos
- Acepta tanto identificadores de tipo como strings de tipo

---

### talloc

Asigna array de valores tipados.

**Firma:**
```hemlock
talloc(type, count: i32): ptr
```

**Parametros:**
- `type` - Tipo a asignar (ej., `i32`, `f64`, `ptr`)
- `count` - Numero de elementos (debe ser positivo)

**Retorna:** Puntero al array asignado, o `null` en fallo de asignacion

**Ejemplos:**
```hemlock
let arr = talloc(i32, 100);      // Array de 100 i32s (400 bytes)
let floats = talloc(f64, 50);    // Array de 50 f64s (400 bytes)
let bytes = talloc(u8, 1024);    // Array de 1024 bytes

// Siempre verificar fallo de asignacion
if (arr == null) {
    panic("fallo de asignacion");
}

// Usar la memoria asignada
// ...

free(arr);
free(floats);
free(bytes);
```

**Comportamiento:**
- Asigna `sizeof(type) * count` bytes
- Retorna memoria sin inicializar
- La memoria debe liberarse manualmente con `free()`
- Retorna `null` en fallo de asignacion (el llamador debe verificar)
- Entra en panico si count no es positivo

---

## Propiedades de Buffer

### .length

Obtiene el tamano del buffer.

**Tipo:** `i32`

**Acceso:** Solo lectura

**Ejemplos:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

Obtiene la capacidad del buffer.

**Tipo:** `i32`

**Acceso:** Solo lectura

**Ejemplos:**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**Nota:** Actualmente, `.length` y `.capacity` son iguales para buffers creados con `buffer()`.

---

## Patrones de Uso

### Patron de Asignacion Basico

```hemlock
// Asignar
let p = alloc(1024);
if (p == null) {
    panic("fallo de asignacion");
}

// Usar
memset(p, 0, 1024);

// Liberar
free(p);
```

### Patron de Buffer Seguro

```hemlock
// Asignar buffer
let buf = buffer(256);
if (buf == null) {
    panic("fallo de asignacion de buffer");
}

// Usar con verificacion de limites
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// Liberar
free(buf);
```

### Patron de Crecimiento Dinamico

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("fallo de asignacion");
}

// ... usar memoria ...

// Necesita mas espacio - verificar fallo
let new_p = realloc(p, 200);
if (new_p == null) {
    // El puntero original sigue valido, limpiar
    free(p);
    panic("fallo de realloc");
}
p = new_p;
size = 200;

// ... usar memoria expandida ...

free(p);
```

### Patron de Copia de Memoria

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// Crear copia
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## Consideraciones de Seguridad

**La gestion de memoria de Hemlock es INSEGURA por diseno:**

### Errores Comunes

**1. Fugas de Memoria**
```hemlock
// MAL: Fuga de memoria
fn create_buffer() {
    let p = alloc(1024);
    return null;  // Memoria perdida!
}

// BIEN: Limpieza apropiada
fn create_buffer() {
    let p = alloc(1024);
    // ... usar memoria ...
    free(p);
    return null;
}
```

**2. Uso Despues de Liberar**
```hemlock
// MAL: Uso despues de liberar
let p = alloc(100);
free(p);
memset(p, 0, 100);  // CRASH: usando memoria liberada

// BIEN: No usar despues de liberar
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// No tocar p2 despues de esto
```

**3. Doble Liberacion**
```hemlock
// MAL: Doble liberacion
let p = alloc(100);
free(p);
free(p);  // CRASH: doble liberacion

// BIEN: Liberar una vez
let p2 = alloc(100);
free(p2);
```

**4. Desbordamiento de Buffer (ptr)**
```hemlock
// MAL: Desbordamiento de buffer con ptr
let p = alloc(10);
memset(p, 65, 100);  // CRASH: escribiendo mas alla de la asignacion

// BIEN: Usar buffer para verificacion de limites
let buf = buffer(10);
// buf[100] = 65;  // ERROR: verificacion de limites falla
```

**5. Punteros Colgantes**
```hemlock
// MAL: Puntero colgante
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // CRASH: p2 esta colgando

// BIEN: Rastrear propiedad cuidadosamente
let p = alloc(100);
// ... usar p ...
free(p);
// No mantener otras referencias a p
```

**6. Fallo de Asignacion sin Verificar**
```hemlock
// MAL: No verificar null
let p = alloc(1000000000);  // Puede fallar con poca memoria
memset(p, 0, 1000000000);   // CRASH: p es null

// BIEN: Siempre verificar resultado de asignacion
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("sin memoria");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## Cuando Usar Que

### Use `buffer()` cuando:
- Necesite verificacion de limites
- Trabaje con datos dinamicos
- La seguridad sea importante
- Este aprendiendo Hemlock

### Use `alloc()` cuando:
- Necesite maximo rendimiento
- Interfaz FFI/con C
- Conozca el layout exacto de memoria
- Sea un experto

### Use `realloc()` cuando:
- Crezca/reduzca asignaciones
- Arrays dinamicos
- Necesite preservar datos

---

## Resumen Completo de Funciones

| Funcion   | Firma                              | Retorna  | Descripcion                |
|-----------|----------------------------------------|----------|----------------------------|
| `alloc`   | `(size: i32)`                          | `ptr`    | Asignar memoria cruda      |
| `buffer`  | `(size: i32)`                          | `buffer` | Asignar buffer seguro      |
| `free`    | `(ptr: ptr \| buffer)`                 | `null`   | Liberar memoria            |
| `realloc` | `(ptr: ptr, new_size: i32)`            | `ptr`    | Redimensionar asignacion   |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`     | `null`   | Llenar memoria             |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`     | `null`   | Copiar memoria             |
| `sizeof`  | `(type)`                               | `i32`    | Obtener tamano de tipo en bytes |
| `talloc`  | `(type, count: i32)`                   | `ptr`    | Asignar array tipado       |

---

## Ver Tambien

- [Sistema de Tipos](type-system.md) - Tipos de puntero y buffer
- [Funciones Integradas](builtins.md) - Todas las funciones integradas
- [API de Strings](string-api.md) - Metodo `.to_bytes()` de string
