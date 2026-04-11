# Anotaciones Auxiliares del Compilador: Analisis y Propuesta

**Autor:** Claude
**Fecha:** 2026-01-08
**Estado:** Parcialmente Implementado (Fase 1-2 completadas en v1.9.0; Fases 3-5 siguen siendo propuestas)
**Relacionado:** Issue #TBD

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Analisis del Estado Actual](#analisis-del-estado-actual)
3. [Anotaciones Propuestas](#anotaciones-propuestas)
4. [Plan de Implementacion](#plan-de-implementacion)
5. [Ejemplos](#ejemplos)
6. [Estrategia de Pruebas](#estrategia-de-pruebas)
7. [Consideraciones Futuras](#consideraciones-futuras)

---

## Resumen Ejecutivo

El sistema de anotaciones de Hemlock proporciona una base robusta para agregar pistas y directivas del compilador. Esta propuesta extiende la infraestructura de anotaciones actual con **15 nuevas anotaciones auxiliares del compilador** organizadas en cinco categorias:

- **Pistas de Optimizacion** (7 anotaciones)
- **Gestion de Memoria** (3 anotaciones)
- **Control de Generacion de Codigo** (2 anotaciones)
- **Verificacion de Errores** (2 anotaciones)
- **FFI/Interoperabilidad** (1 anotacion)

Estas anotaciones permitiran a los desarrolladores proporcionar guia explicita al compilador (`hemlockc`) manteniendo compatibilidad retroactiva con el interprete.

---

## Analisis del Estado Actual

### 1. Infraestructura de Anotaciones

El sistema de anotaciones esta completamente implementado con tres componentes principales:

**Parser** (`src/frontend/parser/statements.c`):
- Parsea sintaxis `@name` y `@name(args...)`
- Soporta argumentos posicionales y con nombre
- Adjunta anotaciones a declaraciones (let, const, define, enum)

**Validador** (`src/frontend/annotations.c`):
- Valida objetivos de anotaciones (funcion, tipo, variable, etc.)
- Verifica conteos y tipos de argumentos
- Advierte sobre anotaciones desconocidas o duplicadas

**Resolvedor** (`src/frontend/resolver.c`):
- Almacena anotaciones junto a definiciones de variables
- Habilita busqueda de anotaciones durante analisis semantico
- Impulsa advertencias `@deprecated` en uso de variables

### 2. Anotaciones Actualmente Implementadas

```c
// Anotaciones de seguridad (para verificador de memoria Tricycle)
@safe       // La funcion es segura en memoria
@unsafe     // La funcion contiene operaciones inseguras
@trusted    // La funcion es confiable a pesar de operaciones inseguras

// Pistas de optimizacion del compilador (IMPLEMENTADAS en v1.9.0)
@inline     // Sugerir inlining de esta funcion
@noinline   // Prevenir inlining de esta funcion
@cold       // La funcion se ejecuta raramente
@hot        // La funcion se ejecuta frecuentemente
@pure       // La funcion no tiene efectos secundarios

// Otras anotaciones
@deprecated      // Marcar como obsoleta con mensaje opcional
@test, @skip     // Anotaciones del framework de pruebas
@author, @since  // Anotaciones de documentacion
```

### 3. Limitaciones Actuales

**Actualizacion (v1.9.0):** Las anotaciones centrales a nivel de funcion (`@inline`, `@noinline`, `@hot`, `@cold`, `@pure`, `@const`, `@flatten`, `@optimize`, `@warn_unused`, `@section`) estan ahora completamente implementadas en el backend del compilador. Las propuestas restantes (anotaciones de bucle, anotaciones de memoria) en las Fases 3-5 a continuacion siguen sin implementar.

---

## Anotaciones Propuestas

### Categoria 1: Pistas de Optimizacion

#### `@unroll(count?: number)`
**Objetivo:** Bucles (for, while)
Sugiere desenrollado de bucle para bucles criticos de rendimiento.

#### `@simd` / `@nosimd`
**Objetivo:** Funciones, bucles
Habilita o deshabilita vectorizacion SIMD.

#### `@likely` / `@unlikely`
**Objetivo:** Sentencias if, condicionales
Pistas de prediccion de ramas para rutas criticas.

#### `@const`
**Objetivo:** Funciones
La funcion siempre retorna el mismo resultado para las mismas entradas (mas fuerte que `@pure`).

#### `@tail_call`
**Objetivo:** Llamadas a funciones
Solicita optimizacion de llamada de cola (TCO).

#### `@flatten`
**Objetivo:** Funciones
Incorporar todas las llamadas dentro de esta funcion.

#### `@optimize(level: string)`
**Objetivo:** Funciones
Sobrescribir el nivel de optimizacion global para una funcion especifica.

### Categoria 2: Gestion de Memoria

#### `@stack`
**Objetivo:** Variables (arrays, buffers)
Asignar en la pila en lugar del heap (donde sea posible).

#### `@noalias`
**Objetivo:** Parametros de funcion (punteros/buffers)
Prometer que el puntero no tiene alias con otros punteros.

#### `@aligned(bytes: number)`
**Objetivo:** Variables (punteros, buffers), retornos de funcion
Especificar requisitos de alineacion de memoria.

### Categoria 3: Control de Generacion de Codigo

#### `@extern(name?: string, abi?: string)`
**Objetivo:** Funciones
Marcar funcion para enlace externo o exportacion FFI.

#### `@section(name: string)`
**Objetivo:** Funciones, variables globales
Colocar simbolo en seccion ELF/Mach-O especifica.

### Categoria 4: Verificacion de Errores

#### `@bounds_check` / `@no_bounds_check`
**Objetivo:** Operaciones de array/buffer, bucles
Sobrescribir politica global de verificacion de limites.

#### `@warn_unused`
**Objetivo:** Valores de retorno de funciones
Advertir si el llamador ignora el valor de retorno.

### Categoria 5: FFI/Interoperabilidad

#### `@packed`
**Objetivo:** Definiciones de tipo (define)
Crear struct empaquetado sin relleno (para interoperabilidad con C).

---

## Ejemplos

### Ejemplo 1: Matematica Vectorial de Alto Rendimiento

```hemlock
@simd
@flatten
fn vector_add(a: buffer, b: buffer, result: buffer, n: i32) {
    @unroll(8)
    for (let i = 0; i < n; i++) {
        let av = ptr_read_f64(a, i * 8);
        let bv = ptr_read_f64(b, i * 8);
        ptr_write_f64(result, i * 8, av + bv);
    }
}
```

### Ejemplo 2: Optimizacion de Cache

```hemlock
@packed
define CacheLineNode {
    next: ptr,
    data: i64,
    timestamp: u64,
    flags: u32,
    padding: u32
}

@hot
@inline
fn cache_lookup(@aligned(64) cache: ptr, key: u64): ptr {
    @likely
    if (cache == null) {
        return null;
    }
    // ...
}
```

### Ejemplo 3: Optimizacion de Llamada de Cola Recursiva

```hemlock
@tail_call
fn sum_range(start: i32, end: i32, acc: i32): i32 {
    if (start > end) {
        return acc;
    }
    @tail_call
    return sum_range(start + 1, end, acc + start);
}
```

---

## Estrategia de Pruebas

### 1. Pruebas de Validacion
Probar que las nuevas anotaciones se validan correctamente.

### 2. Pruebas de Paridad
Asegurar que las anotaciones no cambian el comportamiento del programa.

### 3. Pruebas Especificas del Compilador
Verificar que el codigo C generado contiene los atributos/pragmas correctos.

### 4. Benchmarks de Rendimiento
Medir mejoras reales de rendimiento.

---

## Consideraciones Futuras

### 1. Herencia de Anotaciones
Las anotaciones en tipos deberian aplicarse a todas las instancias?

### 2. Composicion de Anotaciones
Permitir crear anotaciones personalizadas a partir de otras.

### 3. Integracion de Banderas del Compilador
Las anotaciones deberian sobrescribir banderas del compilador.

### 4. Integracion de Analisis Estatico
Las anotaciones podrian impulsar herramientas de analisis estatico.

### 5. Acceso a Anotaciones en Runtime
Las anotaciones deberian ser consultables en runtime?

---

## Conclusion

Esta propuesta agrega **15 nuevas anotaciones auxiliares del compilador** a Hemlock, permitiendo a los desarrolladores proporcionar pistas de optimizacion explicitas manteniendo la filosofia de "explicito sobre implicito" del lenguaje.

**Beneficios Clave:**

1. **Rendimiento:** Aceleraciones de 2-10x para rutas criticas con SIMD, desenrollado, inlining
2. **Control:** Los desarrolladores pueden sobrescribir heuristicas predeterminadas del compilador
3. **Interoperabilidad:** Mejor soporte FFI con @extern, @packed, @aligned
4. **Seguridad:** @bounds_check/@no_bounds_check explicitos hacen visibles los compromisos de seguridad
5. **Explicito:** Se ajusta a la filosofia de Hemlock -- sin magia, solo directivas claras

---

## Apendice: Tabla de Referencia Completa de Anotaciones

| Anotacion | Objetivo | Args | Descripcion | Atributo C |
|-----------|----------|------|-------------|------------|
| `@inline` | fn | 0 | Forzar inlining | `always_inline` |
| `@noinline` | fn | 0 | Prevenir inlining | `noinline` |
| `@cold` | fn | 0 | Ejecutada raramente | `cold` |
| `@hot` | fn | 0 | Ejecutada frecuentemente | `hot` |
| `@pure` | fn | 0 | Sin efectos secundarios, puede leer globales | `pure` |
| `@const` | fn | 0 | Sin efectos secundarios, sin lectura de globales | `const` |
| `@flatten` | fn | 0 | Incorporar todas las llamadas dentro de la funcion | `flatten` |
| `@tail_call` | fn | 0 | Solicitar optimizacion de llamada de cola | Personalizado |
| `@optimize(level)` | fn | 1 | Sobrescribir nivel de optimizacion | `optimize("OX")` |
| `@unroll(factor?)` | loop | 0-1 | Pista de desenrollado de bucle | `#pragma unroll` |
| `@simd` | fn, loop | 0 | Habilitar vectorizacion SIMD | `#pragma omp simd` |
| `@nosimd` | fn, loop | 0 | Deshabilitar SIMD | Personalizado |
| `@likely` | if | 0 | Rama probablemente tomada | `__builtin_expect` |
| `@unlikely` | if | 0 | Rama probablemente no tomada | `__builtin_expect` |
| `@stack` | let | 0 | Asignacion en pila | Personalizado |
| `@noalias` | param | 0 | Sin alias de puntero | `noalias` |
| `@aligned(N)` | let, fn | 1 | Alineacion de memoria | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | Enlace externo | `extern "C"` |
| `@section(name)` | fn, let | 1 | Colocar en seccion especifica | `section("X")` |
| `@bounds_check` | fn | 0 | Forzar verificacion de limites | Personalizado |
| `@no_bounds_check` | fn | 0 | Deshabilitar verificacion de limites | Personalizado |
| `@warn_unused` | fn | 0 | Advertir si retorno no usado | `warn_unused_result` |
| `@packed` | define | 0 | Sin relleno en struct | `packed` |
