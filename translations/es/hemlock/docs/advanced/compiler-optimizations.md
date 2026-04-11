# Optimizaciones del Compilador

El compilador de Hemlock (`hemlockc`) aplica varios pases de optimizacion al generar codigo C. Estas optimizaciones son automaticas y no requieren intervencion del usuario, pero entenderlas ayuda a explicar las caracteristicas de rendimiento.

---

## Descripcion General

```
Fuente (.hml)
    ↓
  Parsear → AST
    ↓
  Verificacion de Tipos (opcional)
    ↓
  Pase de Optimizacion del AST
    ↓
  Generacion de Codigo C (con inlining + unboxing)
    ↓
  Compilacion GCC/Clang
```

---

## Unboxing de Expresiones

El runtime de Hemlock representa todos los valores como structs `HmlValue` etiquetados. En el interprete, cada operacion aritmetica encapsula y desencapsula valores a traves de despacho en tiempo de ejecucion. El compilador elimina esta sobrecarga para expresiones con tipos primitivos conocidos.

**Antes (codegen ingenuo):**
```c
// x + 1 donde x es i32
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 llamadas de boxing + despacho en runtime
```

**Despues (con unboxing de expresiones):**
```c
// x + 1 donde x es i32
hml_val_i32((x + 1))  // Aritmetica C pura, un solo box al final
```

### Que se Desencapsula

- Aritmetica binaria: `+`, `-`, `*`, `%`
- Operaciones de bits: `&`, `|`, `^`, `<<`, `>>`
- Comparaciones: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Operaciones unarias: `-`, `~`, `!`
- Variables con anotacion de tipo y contadores de bucle

### Que Recurre a HmlValue

- Llamadas a funciones (el tipo de retorno puede ser dinamico)
- Acceso a arrays/objetos (tipo de elemento desconocido en tiempo de compilacion)
- Variables sin anotaciones de tipo y sin tipo inferido

### Consejo

Agregar anotaciones de tipo a las variables en rutas criticas ayuda al compilador a aplicar unboxing:

```hemlock
// El compilador puede desencapsular toda esta expresion
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## Inlining de Funciones Multinivel

El compilador incorpora funciones pequenas en los sitios de llamada, reemplazando la sobrecarga de llamada de funcion con codigo directo. Hemlock soporta inlining multinivel hasta profundidad 3, lo que significa que las llamadas a funciones auxiliares anidadas tambien se incorporan.

### Como Funciona

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // Tanto ep0 COMO rotr se incorporan aqui
    // ...
}
```

A profundidad 1, `ep0()` se incorpora en `sha256_round()`. A profundidad 2, las llamadas a `rotr()` dentro de `ep0()` tambien se incorporan. El resultado es un solo bloque de aritmetica nativa sin sobrecarga de llamada de funcion.

### Criterios de Inlining

Las funciones se incorporan cuando:
- El cuerpo de la funcion es pequeno (expresion unica o pocas sentencias)
- La funcion no es recursiva
- La profundidad actual de inlining es menor que 3

### Controlando el Inlining con Anotaciones

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // Funcion compleja que no debe duplicarse
    return x;
}
```

---

## Unboxing de Acumuladores en Bucles While

Para bucles while de nivel superior, el compilador detecta variables contador y acumulador y las sombrea con variables locales C nativas, eliminando la sobrecarga de boxing/unboxing en cada iteracion.

### Que se Optimiza

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

El compilador detecta que `sum` e `i` son acumuladores enteros usados solo dentro del bucle, y genera variables locales `int32_t` nativas en lugar de operaciones `HmlValue`. Esto elimina la sobrecarga de retain/release y despacho de tipos en cada iteracion.

### Impacto en el Rendimiento

Mejoras de benchmarks de estas optimizaciones (medidas en cargas de trabajo tipicas):

| Benchmark | Antes | Despues | Mejora |
|-----------|-------|---------|--------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## Anotaciones Auxiliares

El compilador soporta 10 anotaciones de optimizacion que mapean a atributos de GCC/Clang:

| Anotacion | Efecto |
|-----------|--------|
| `@inline` | Fomentar el inlining de la funcion |
| `@noinline` | Prevenir el inlining de la funcion |
| `@hot` | Marcar como ejecutada frecuentemente (prediccion de ramas) |
| `@cold` | Marcar como ejecutada raramente |
| `@pure` | La funcion no tiene efectos secundarios (lee estado externo) |
| `@const` | La funcion depende solo de los argumentos (sin estado externo) |
| `@flatten` | Incorporar todas las llamadas dentro de la funcion |
| `@optimize(level)` | Nivel de optimizacion por funcion ("0"-"3", "s", "fast") |
| `@warn_unused` | Advertir si el valor de retorno se ignora |
| `@section(name)` | Colocar la funcion en seccion ELF personalizada |

### Ejemplo

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // Funcion de hash en ruta critica
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## Pools de Asignacion

El runtime usa pools de objetos preasignados para evitar la sobrecarga de `malloc`/`free` para objetos de corta duracion creados frecuentemente:

| Pool | Slots | Descripcion |
|------|-------|-------------|
| Pool de entornos | 1024 | Entornos de alcance de clausuras/funciones (hasta 16 variables cada uno) |
| Pool de objetos | 512 | Objetos anonimos con hasta 8 campos |
| Pool de funciones | 512 | Structs de clausura para funciones capturadas |

Los pools usan pilas de listas libres para asignacion y liberacion O(1). Cuando un pool se agota, el runtime recurre a `malloc`. Los objetos que superan su slot de pool (ej., un objeto que gana un 9no campo) se migran transparentemente al almacenamiento heap.

### Parametros Prestados del AST

Las clausuras toman prestada la metadata de parametros directamente del AST en lugar de hacer copia profunda, eliminando aproximadamente 6 llamadas `malloc` + N llamadas `strdup` por creacion de clausura. Los hashes de nombres de parametros se calculan perezosamente y se cachean en el nodo del AST.

---

## Verificacion de Tipos

El compilador incluye verificacion de tipos en tiempo de compilacion (habilitada por defecto):

```bash
hemlockc program.hml -o program       # Verificar tipos + compilar
hemlockc --check program.hml          # Solo verificar tipos
hemlockc --no-type-check program.hml  # Omitir verificacion de tipos
hemlockc --strict-types program.hml   # Advertir sobre tipos 'any' implicitos
```

El codigo sin tipos se trata como dinamico (tipo `any`) y siempre pasa la verificacion de tipos. Las anotaciones de tipo proporcionan pistas de optimizacion que habilitan el unboxing.

---

## Ver Tambien

- [Propuesta de Anotaciones Auxiliares](../proposals/compiler-helper-annotations.md) - Referencia detallada de anotaciones
- [API de Memoria](../reference/memory-api.md) - Operaciones de buffer y puntero
- [Funciones](../language-guide/functions.md) - Anotaciones de tipo y funciones con cuerpo de expresion
