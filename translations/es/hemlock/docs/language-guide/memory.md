# Gestión de Memoria

Hemlock adopta la **gestión manual de memoria** con control explícito sobre la asignación y liberación. Esta guía cubre el modelo de memoria de Hemlock, los dos tipos de punteros y la API completa de memoria.

---

## Memoria 101: Lo Básico

**Nuevo en programación?** Comience aquí. Si ya entiende la gestión de memoria, salte a [Filosofía](#filosofía).

### Qué es la Gestión de Memoria?

Cuando su programa necesita almacenar datos (texto, números, listas), necesita espacio para colocarlos. Ese espacio viene de la memoria de su computadora (RAM). La gestión de memoria trata sobre:

1. **Obtener espacio** - solicitar memoria cuando la necesita
2. **Usar espacio** - leer y escribir sus datos
3. **Devolverla** - retornar la memoria cuando haya terminado

### Por Qué Importa?

Imagine una biblioteca con libros limitados:
- Si sigue sacando libros y nunca los devuelve, eventualmente no quedan
- Si intenta leer un libro que ya devolvió, se confundirá o causará problemas

La memoria funciona de la misma manera. Si olvida devolver la memoria, su programa lentamente usa más y más (una "fuga de memoria"). Si intenta usar memoria después de devolverla, suceden cosas malas.

### Las Buenas Noticias

**La mayor parte del tiempo, no necesita pensar en esto!**

Hemlock limpia automáticamente la mayoría de los tipos comunes:

```hemlock
fn example() {
    let name = "Alice";       // Hemlock maneja esto
    let numbers = [1, 2, 3];  // Y esto
    let person = { age: 30 }; // Y esto también

    // Cuando la función termina, todo esto se limpia automáticamente!
}
```

### Cuándo SÍ Necesita Pensar en Ello

Solo necesita gestión manual de memoria cuando usa:

1. **`alloc()`** - asignación de memoria cruda (retorna `ptr`)
2. **`buffer()`** - cuando quiere liberar temprano (opcional - se auto-libera al final del ámbito)

```hemlock
// Esto necesita limpieza manual:
let raw = alloc(100);   // Memoria cruda - USTED debe liberarla
// ... usar raw ...
free(raw);              // Requerido! O tiene una fuga de memoria

// Esto se limpia automáticamente (pero PUEDE liberar temprano):
let buf = buffer(100);  // Buffer seguro
// ... usar buf ...
// free(buf);           // Opcional - se auto-liberará cuando el ámbito termine
```

### La Regla Simple

> **Si llama a `alloc()`, debe llamar a `free()`.**
>
> Todo lo demás se maneja por usted.

### Cuál Debería Usar?

| Situación | Use Esto | Por Qué |
|-----------|----------|---------|
| **Recién comenzando** | `buffer()` | Seguro, con verificación de límites, auto-limpieza |
| **Necesita almacenamiento de bytes** | `buffer()` | Seguro y fácil |
| **Trabajando con bibliotecas C (FFI)** | `alloc()` / `ptr` | Requerido para interoperabilidad con C |
| **Máximo rendimiento** | `alloc()` / `ptr` | Sin overhead de verificación de límites |
| **No está seguro** | `buffer()` | Siempre la opción más segura |

### Ejemplo Rápido: Seguro vs Crudo

```hemlock
// RECOMENDADO: Buffer seguro
fn safe_example() {
    let data = buffer(10);
    data[0] = 65;           // OK
    data[5] = 66;           // OK
    // data[100] = 67;      // ERROR - Hemlock lo detiene (verificación de límites)
    free(data);             // Limpiar
}

// AVANZADO: Puntero crudo (solo cuando lo necesita)
fn raw_example() {
    let data = alloc(10);
    *data = 65;             // OK
    *(data + 5) = 66;       // OK
    *(data + 100) = 67;     // PELIGRO - Sin verificación de límites, corrompe memoria!
    free(data);             // Limpiar
}
```

**Comience con `buffer()`. Solo use `alloc()` cuando específicamente necesite punteros crudos.**

---

## Filosofía

Hemlock sigue el principio de gestión explícita de memoria con valores por defecto sensatos:
- Sin recolección de basura (sin pausas impredecibles)
- Conteo de referencias interno para tipos comunes (string, array, object, buffer)
- Los punteros crudos (`ptr`) requieren `free()` manual

Este enfoque híbrido le da control completo cuando lo necesita (punteros crudos) mientras previene errores comunes para casos de uso típicos (tipos con conteo de referencias auto-liberados al salir del ámbito).

## Conteo de Referencias Interno

El runtime usa **conteo de referencias interno** para gestionar tiempos de vida de objetos. Para la mayoría de las variables locales de tipos con conteo de referencias, la limpieza es automática y determinista.

### Qué Maneja el Conteo de Referencias

El runtime automáticamente gestiona conteos de referencias cuando:

1. **Las variables se reasignan** - el valor antiguo se libera:
   ```hemlock
   let x = "first";   // ref_count = 1
   x = "second";      // "first" liberado internamente, "second" ref_count = 1
   ```

2. **Los ámbitos terminan** - las variables locales se liberan:
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // arr liberado cuando la función retorna
   ```

3. **Los contenedores se liberan** - los elementos se liberan:
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // obj1 y obj2 obtienen sus ref_counts decrementados
   ```

### Cuándo Necesita `free()` vs Cuándo Es Automático

**Automático (no necesita `free()`):** Las variables locales de tipos con conteo de referencias se liberan cuando el ámbito termina:

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... usarlos ...
}  // Todos liberados automáticamente cuando la función retorna - no necesita free()
```

**Se requiere `free()` manual:**

1. **Punteros crudos** - `alloc()` no tiene conteo de referencias:
   ```hemlock
   let p = alloc(64);
   // ... usar p ...
   free(p);  // Siempre requerido - fugará de otro modo
   ```

2. **Limpieza temprana** - liberar antes de que el ámbito termine para liberar memoria más pronto:
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10MB
       // ... terminado con big ...
       free(big);  // Liberar ahora, no esperar a que la función retorne
       // ... más trabajo que no necesita big ...
   }
   ```

3. **Datos de larga vida** - globales o datos almacenados en estructuras persistentes:
   ```hemlock
   let cache = {};  // Nivel de módulo, vive hasta que el programa termine a menos que se libere

   fn cleanup() {
       free(cache);  // Limpieza manual para datos de larga vida
   }
   ```

### Conteo de Referencias vs Recolección de Basura

| Aspecto | Conteo de Referencias Hemlock | Recolección de Basura |
|---------|------------------------------|----------------------|
| Momento de limpieza | Determinista (inmediato cuando ref llega a 0) | No determinista (GC decide cuándo) |
| Responsabilidad del usuario | Debe llamar `free()` | Completamente automático |
| Pausas del runtime | Ninguna | Pausas "detener el mundo" |
| Visibilidad | Detalle de implementación oculto | Usualmente invisible |
| Ciclos | Manejados con seguimiento de conjunto visitado | Manejados por rastreo |

### Qué Tipos Tienen Conteo de Referencias

| Tipo | Con Conteo | Notas |
|------|------------|-------|
| `ptr` | No | Siempre requiere `free()` manual |
| `buffer` | Sí | Auto-liberado al salir del ámbito; `free()` manual para limpieza temprana |
| `array` | Sí | Auto-liberado al salir del ámbito; `free()` manual para limpieza temprana |
| `object` | Sí | Auto-liberado al salir del ámbito; `free()` manual para limpieza temprana |
| `string` | Sí | Completamente automático, no necesita `free()` |
| `function` | Sí | Completamente automático (entornos de closure) |
| `task` | Sí | Conteo de referencias atómico thread-safe |
| `channel` | Sí | Conteo de referencias atómico thread-safe |
| Primitivos | No | Asignados en stack, sin asignación de heap |

### Por Qué Este Diseño?

Este enfoque híbrido le da:
- **Control explícito** - Usted decide cuándo liberar
- **Seguridad contra bugs de ámbito** - La reasignación no fuga
- **Rendimiento predecible** - Sin pausas de GC
- **Soporte de closures** - Las funciones pueden capturar variables de forma segura

La filosofía permanece: usted tiene el control, pero el runtime ayuda a prevenir errores comunes como fugas en reasignación o double-free en contenedores.

## Los Dos Tipos de Punteros

Hemlock proporciona dos tipos de punteros distintos, cada uno con diferentes características de seguridad:

### `ptr` - Puntero Crudo (Peligroso)

Los punteros crudos son **solo direcciones** con garantías de seguridad mínimas:

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Debe recordar liberar
```

**Características:**
- Solo una dirección de 8 bytes
- Sin verificación de límites
- Sin seguimiento de longitud
- El usuario gestiona el tiempo de vida completamente
- Para expertos y FFI

**Casos de uso:**
- Programación de sistemas de bajo nivel
- Interfaz de Funciones Foráneas (FFI)
- Código crítico para rendimiento
- Cuando necesita control completo

**Peligros:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Muy pasado el límite de asignación - permitido pero peligroso
free(p);
let x = *p;       // Puntero colgante - comportamiento indefinido
free(p);          // Double-free - fallará
```

### `buffer` - Envoltorio Seguro (Recomendado)

Los buffers proporcionan **acceso con verificación de límites** mientras aún requieren liberación manual:

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // verificado por límites
print(b.length);        // 64
free(b);                // aún manual
```

**Características:**
- Puntero + longitud + capacidad
- Verificación de límites en acceso
- Aún requiere `free()` manual
- Mejor opción por defecto para la mayoría del código

**Propiedades:**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100 (tamaño actual)
print(buf.capacity);    // 100 (capacidad asignada)
```

**Verificación de límites:**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // OK
buf[100] = 42;    // ERROR: Index out of bounds
```

## API de Memoria

### Asignación Básica

**`alloc(bytes)` - Asignar memoria cruda**
```hemlock
let p = alloc(1024);  // Asignar 1KB, retorna ptr
// ... usar memoria
free(p);
```

**`buffer(size)` - Asignar buffer seguro**
```hemlock
let buf = buffer(256);  // Asignar buffer de 256 bytes
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - Liberar memoria**
```hemlock
let p = alloc(100);
free(p);  // Debe liberar para evitar fuga de memoria

let buf = buffer(100);
free(buf);  // Funciona tanto en ptr como en buffer
```

**Importante:** `free()` funciona tanto en tipos `ptr` como `buffer`.

### Operaciones de Memoria

**`memset(ptr, byte, size)` - Llenar memoria**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // Poner a cero 100 bytes
memset(p, 65, 10);     // Llenar los primeros 10 bytes con 'A'
free(p);
```

**`memcpy(dest, src, size)` - Copiar memoria**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // Copiar 50 bytes de src a dst
free(src);
free(dst);
```

**`realloc(ptr, size)` - Redimensionar asignación**
```hemlock
let p = alloc(100);
// ... usar 100 bytes
p = realloc(p, 200);   // Redimensionar a 200 bytes
// ... usar 200 bytes
free(p);
```

**Nota:** Después de `realloc()`, el puntero antiguo puede ser inválido. Siempre use el puntero retornado.

### Asignación Tipada

Hemlock proporciona ayudantes de asignación tipada por conveniencia:

```hemlock
let arr = talloc(i32, 100);  // Asignar 100 valores i32 (400 bytes)
let size = sizeof(i32);      // Retorna 4 (bytes)
```

**`sizeof(type)`** retorna el tamaño en bytes de un tipo:
- `sizeof(i8)` / `sizeof(u8)` → 1
- `sizeof(i16)` / `sizeof(u16)` → 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` → 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` → 8
- `sizeof(ptr)` → 8 (en sistemas de 64 bits)

**`talloc(type, count)`** asigna `count` elementos de `type`:

```hemlock
let ints = talloc(i32, 10);   // 40 bytes para 10 valores i32
let floats = talloc(f64, 5);  // 40 bytes para 5 valores f64
free(ints);
free(floats);
```

## Patrones Comunes

### Patrón: Asignar, Usar, Liberar

El patrón básico para gestión de memoria:

```hemlock
// 1. Asignar
let data = alloc(1024);

// 2. Usar
memset(data, 0, 1024);
// ... hacer trabajo

// 3. Liberar
free(data);
```

### Patrón: Uso de Buffer Seguro

Prefiera buffers para acceso con verificación de límites:

```hemlock
let buf = buffer(256);

// Iteración segura
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### Patrón: Gestión de Recursos con try/finally

Asegure la limpieza incluso en errores:

```hemlock
let data = alloc(1024);
try {
    // ... operaciones riesgosas
    process(data);
} finally {
    free(data);  // Siempre liberado, incluso en error
}
```

## Consideraciones de Seguridad de Memoria

### Double-Free

**Permitido pero fallará:**
```hemlock
let p = alloc(100);
free(p);
free(p);  // FALLA: Double-free detectado
```

**Prevención:**
```hemlock
let p = alloc(100);
free(p);
p = null;  // Establecer a null después de liberar

if (p != null) {
    free(p);  // No se ejecutará
}
```

### Punteros Colgantes

**Permitido pero comportamiento indefinido:**
```hemlock
let p = alloc(100);
*p = 42;      // OK
free(p);
let x = *p;   // INDEFINIDO: Leyendo memoria liberada
```

**Prevención:** No acceda a memoria después de liberar.

### Fugas de Memoria

**Fáciles de crear, difíciles de depurar:**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // Olvidó liberar!
    return;  // Memoria fugada
}
```

**Prevención:** Siempre empareje `alloc()` con `free()`:
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... usar p
    } finally {
        free(p);  // Siempre liberado
    }
}
```

### Aritmética de Punteros

**Permitida pero peligrosa:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Muy pasado el límite de asignación
*q = 42;          // INDEFINIDO: Escritura fuera de límites
free(p);
```

**Use buffers para verificación de límites:**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // ERROR: La verificación de límites previene el desbordamiento
```

## Mejores Prácticas

1. **Por defecto use `buffer`** - Use `buffer` a menos que específicamente necesite `ptr` crudo
2. **Empareje alloc/free** - Cada `alloc()` debe tener exactamente un `free()`
3. **Use try/finally** - Asegure limpieza con manejo de excepciones
4. **Null después de free** - Establezca punteros a `null` después de liberar para detectar uso después de liberación
5. **Verificación de límites** - Use indexación de buffer para verificación automática de límites
6. **Documente propiedad** - Deje claro qué código posee y libera cada asignación

## Ejemplos

### Ejemplo: Constructor de Strings Dinámico

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // El llamador debe liberar
}

let msg = build_message(5);
// ... usar msg
free(msg);
```

### Ejemplo: Operaciones de Array Seguras

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // Llenar array
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // Procesar
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // Siempre limpiar
    }
}
```

### Ejemplo: Patrón de Pool de Memoria

```hemlock
// Pool de memoria simple (simplificado)
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool exhausted";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// Usar pool
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// Liberar todo el pool de una vez
free(pool);
```

## Limitaciones

Limitaciones actuales a tener en cuenta:

- **Los punteros crudos requieren free manual** - `alloc()` retorna `ptr` sin conteo de referencias
- **Sin asignadores personalizados** - Solo malloc/free del sistema

**Nota:** Los tipos con conteo de referencias (string, array, object, buffer) SÍ se liberan automáticamente cuando el ámbito termina. Solo `ptr` crudo de `alloc()` requiere `free()` explícito.

## Temas Relacionados

- [Strings](strings.md) - Gestión de memoria de strings y codificación UTF-8
- [Arrays](arrays.md) - Arrays dinámicos y sus características de memoria
- [Objetos](objects.md) - Asignación y tiempo de vida de objetos
- [Manejo de Errores](error-handling.md) - Usando try/finally para limpieza

## Ver También

- **Filosofía de Diseño**: Consulte la sección "Memory Management" de CLAUDE.md
- **Sistema de Tipos**: Consulte [Tipos](types.md) para detalles de tipos `ptr` y `buffer`
- **FFI**: Los punteros crudos son esenciales para la Interfaz de Funciones Foráneas
