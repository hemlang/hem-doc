# Operaciones Atomicas

Hemlock proporciona operaciones atomicas para **programacion concurrente sin bloqueos**. Estas operaciones permiten la manipulacion segura de memoria compartida a traves de multiples hilos sin bloqueos o mutexes tradicionales.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Cuando Usar Atomicos](#cuando-usar-atomicos)
- [Modelo de Memoria](#modelo-de-memoria)
- [Carga y Almacenamiento Atomico](#carga-y-almacenamiento-atomico)
- [Operaciones Fetch-and-Modify](#operaciones-fetch-and-modify)
- [Compare-and-Swap (CAS)](#compare-and-swap-cas)
- [Intercambio Atomico](#intercambio-atomico)
- [Barrera de Memoria](#barrera-de-memoria)
- [Referencia de Funciones](#referencia-de-funciones)
- [Patrones Comunes](#patrones-comunes)
- [Mejores Practicas](#mejores-practicas)
- [Limitaciones](#limitaciones)

---

## Vision General

Las operaciones atomicas son operaciones **indivisibles** que se completan sin posibilidad de interrupcion. Cuando un hilo realiza una operacion atomica, ningun otro hilo puede observar la operacion en un estado parcialmente completado.

**Caracteristicas clave:**
- Todas las operaciones usan **consistencia secuencial** (`memory_order_seq_cst`)
- Tipos soportados: **i32** e **i64**
- Las operaciones trabajan con punteros crudos asignados con `alloc()`
- Seguro para hilos sin bloqueos explicitos

**Operaciones disponibles:**
- Load/Store - Leer y escribir valores atomicamente
- Add/Sub - Operaciones aritmeticas que retornan el valor anterior
- And/Or/Xor - Operaciones de bits que retornan el valor anterior
- CAS - Compare-and-swap para actualizaciones condicionales
- Exchange - Intercambiar valores atomicamente
- Fence - Barrera de memoria completa

---

## Cuando Usar Atomicos

**Usar atomicos para:**
- Contadores compartidos entre tareas (ej. conteos de solicitudes, seguimiento de progreso)
- Flags e indicadores de estado
- Estructuras de datos sin bloqueos
- Primitivas de sincronizacion simples
- Codigo concurrente critico en rendimiento

**Usar canales en su lugar cuando:**
- Pasar datos complejos entre tareas
- Implementar patrones productor-consumidor
- Necesitas semantica de paso de mensajes

**Caso de uso de ejemplo - Contador compartido:**
```hemlock
// Asignar contador compartido
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// Crear multiples workers
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// El contador sera exactamente 3000 (sin carreras de datos)
print(atomic_load_i32(counter));

free(counter);
```

---

## Modelo de Memoria

Todas las operaciones atomicas de Hemlock usan **consistencia secuencial** (`memory_order_seq_cst`), que proporciona las garantias de ordenamiento de memoria mas fuertes:

1. **Atomicidad**: Cada operacion es indivisible
2. **Ordenamiento total**: Todos los hilos ven el mismo orden de operaciones
3. **Sin reordenamiento**: Las operaciones no son reordenadas por el compilador o la CPU

Esto hace que razonar sobre codigo concurrente sea mas simple, a costa de algo de rendimiento potencial comparado con ordenamientos de memoria mas debiles.

---

## Carga y Almacenamiento Atomico

### atomic_load_i32 / atomic_load_i64

Leer atomicamente un valor de memoria.

**Firma:**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**Parametros:**
- `ptr` - Puntero a la ubicacion de memoria (debe estar correctamente alineado)

**Retorna:** El valor en la ubicacion de memoria

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

Escribir atomicamente un valor a memoria.

**Firma:**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**Parametros:**
- `ptr` - Puntero a la ubicacion de memoria
- `value` - Valor a almacenar

**Retorna:** `null`

**Ejemplo:**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## Operaciones Fetch-and-Modify

Estas operaciones modifican atomicamente un valor y retornan el valor **anterior** (previo).

### atomic_add_i32 / atomic_add_i64

Sumar atomicamente a un valor.

**Firma:**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**Retorna:** El valor **anterior** (antes de la suma)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100 (valor anterior)
print(atomic_load_i32(p));     // 110 (valor nuevo)

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

Restar atomicamente de un valor.

**Firma:**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**Retorna:** El valor **anterior** (antes de la resta)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100 (valor anterior)
print(atomic_load_i32(p));     // 75 (valor nuevo)

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

Realizar atomicamente AND de bits.

**Firma:**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**Retorna:** El valor **anterior** (antes del AND)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 255 en binario: 11111111

let old = atomic_and_i32(p, 0x0F);  // AND con 00001111
print(old);                    // 255 (valor anterior)
print(atomic_load_i32(p));     // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

Realizar atomicamente OR de bits.

**Firma:**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**Retorna:** El valor **anterior** (antes del OR)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 15 en binario: 00001111

let old = atomic_or_i32(p, 0xF0);  // OR con 11110000
print(old);                    // 15 (valor anterior)
print(atomic_load_i32(p));     // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

Realizar atomicamente XOR de bits.

**Firma:**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**Retorna:** El valor **anterior** (antes del XOR)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 170 en binario: 10101010

let old = atomic_xor_i32(p, 0xFF);  // XOR con 11111111
print(old);                    // 170 (valor anterior)
print(atomic_load_i32(p));     // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## Compare-and-Swap (CAS)

La operacion atomica mas poderosa. Compara atomicamente el valor actual con un valor esperado y, si coinciden, lo reemplaza con un nuevo valor.

### atomic_cas_i32 / atomic_cas_i64

**Firma:**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**Parametros:**
- `ptr` - Puntero a la ubicacion de memoria
- `expected` - Valor que esperamos encontrar
- `desired` - Valor a almacenar si la expectativa coincide

**Retorna:**
- `true` - El intercambio tuvo exito (el valor era `expected`, ahora es `desired`)
- `false` - El intercambio fallo (el valor no era `expected`, sin cambios)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS exitoso: el valor es 100, intercambiar a 999
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS fallido: el valor es 999, no 100
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999 (sin cambios)

free(p);
```

**Casos de uso:**
- Implementar bloqueos y semaforos
- Estructuras de datos sin bloqueos
- Control de concurrencia optimista
- Actualizaciones condicionales atomicas

---

## Intercambio Atomico

Intercambiar atomicamente un valor, retornando el valor anterior.

### atomic_exchange_i32 / atomic_exchange_i64

**Firma:**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**Parametros:**
- `ptr` - Puntero a la ubicacion de memoria
- `value` - Nuevo valor a almacenar

**Retorna:** El valor **anterior** (antes del intercambio)

**Ejemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100 (valor anterior)
print(atomic_load_i32(p));     // 200 (valor nuevo)

free(p);
```

---

## Barrera de Memoria

Una barrera de memoria completa que asegura que todas las operaciones de memoria antes de la barrera sean visibles para todos los hilos antes de cualquier operacion despues de la barrera.

### atomic_fence

**Firma:**
```hemlock
atomic_fence(): null
```

**Retorna:** `null`

**Ejemplo:**
```hemlock
// Asegurar que todas las escrituras anteriores sean visibles
atomic_fence();
```

**Nota:** En la mayoria de los casos, no necesitas barreras explicitas porque todas las operaciones atomicas ya usan consistencia secuencial. Las barreras son utiles cuando necesitas sincronizar operaciones de memoria no atomicas.

---

## Referencia de Funciones

### Operaciones i32

| Funcion | Firma | Retorna | Descripcion |
|---------|-------|---------|-------------|
| `atomic_load_i32` | `(ptr)` | `i32` | Cargar valor atomicamente |
| `atomic_store_i32` | `(ptr, value)` | `null` | Almacenar valor atomicamente |
| `atomic_add_i32` | `(ptr, value)` | `i32` | Sumar y retornar valor anterior |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | Restar y retornar valor anterior |
| `atomic_and_i32` | `(ptr, value)` | `i32` | AND de bits y retornar valor anterior |
| `atomic_or_i32` | `(ptr, value)` | `i32` | OR de bits y retornar valor anterior |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | XOR de bits y retornar valor anterior |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | Intercambiar y retornar valor anterior |

### Operaciones i64

| Funcion | Firma | Retorna | Descripcion |
|---------|-------|---------|-------------|
| `atomic_load_i64` | `(ptr)` | `i64` | Cargar valor atomicamente |
| `atomic_store_i64` | `(ptr, value)` | `null` | Almacenar valor atomicamente |
| `atomic_add_i64` | `(ptr, value)` | `i64` | Sumar y retornar valor anterior |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | Restar y retornar valor anterior |
| `atomic_and_i64` | `(ptr, value)` | `i64` | AND de bits y retornar valor anterior |
| `atomic_or_i64` | `(ptr, value)` | `i64` | OR de bits y retornar valor anterior |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | XOR de bits y retornar valor anterior |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | Intercambiar y retornar valor anterior |

### Barrera de Memoria

| Funcion | Firma | Retorna | Descripcion |
|---------|-------|---------|-------------|
| `atomic_fence` | `()` | `null` | Barrera de memoria completa |

---

## Patrones Comunes

### Patron: Contador Atomico

```hemlock
// Contador seguro para hilos
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// Uso
increment();  // Retorna 0 (valor anterior)
increment();  // Retorna 1
increment();  // Retorna 2
print(get_count());  // 3

free(counter);
```

### Patron: Spinlock

```hemlock
// Implementacion simple de spinlock
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = desbloqueado, 1 = bloqueado

fn acquire() {
    // Girar hasta que establezcamos exitosamente el bloqueo de 0 a 1
    while (!atomic_cas_i32(lock, 0, 1)) {
        // Espera activa
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// Uso
acquire();
// ... seccion critica ...
release();

free(lock);
```

### Patron: Inicializacion Unica

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = no inicializado, 1 = inicializado

fn ensure_initialized() {
    // Intentar ser el que inicializa
    if (atomic_cas_i32(initialized, 0, 1)) {
        // Ganamos la carrera, hacer inicializacion
        do_expensive_init();
    }
    // De lo contrario, ya inicializado
}
```

### Patron: Flag Atomico

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // Retorna true si el flag ya estaba establecido
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### Patron: Contador Acotado

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // En el maximo
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // Incrementado exitosamente
        }
        // CAS fallo, otro hilo modifico - reintentar
    }
}
```

---

## Mejores Practicas

### 1. Usar Alineacion Apropiada

Los punteros deben estar correctamente alineados para el tipo de datos:
- i32: alineacion de 4 bytes
- i64: alineacion de 8 bytes

La memoria de `alloc()` tipicamente esta correctamente alineada.

### 2. Preferir Abstracciones de Nivel Superior

Cuando sea posible, usa canales para comunicacion entre tareas. Los atomicos son de nivel mas bajo y requieren razonamiento cuidadoso.

```hemlock
// Preferir esto:
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// Sobre coordinacion atomica manual cuando sea apropiado
```

### 3. Estar Consciente del Problema ABA

CAS puede sufrir del problema ABA: un valor cambia de A a B y vuelve a A. Tu CAS tiene exito, pero el estado puede haber cambiado entre medio.

### 4. Inicializar Antes de Compartir

Siempre inicializa las variables atomicas antes de crear tareas que las accedan:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // Inicializar ANTES de crear tareas

let task = spawn(worker, counter);
```

### 5. Liberar Despues de que Todas las Tareas Completen

No liberes memoria atomica mientras las tareas todavia podrian accederla:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// Ahora es seguro liberar
free(counter);
```

---

## Limitaciones

### Limitaciones Actuales

1. **Solo i32 e i64 soportados** - Sin operaciones atomicas para otros tipos
2. **Sin atomicos de puntero** - No se pueden cargar/almacenar punteros atomicamente
3. **Solo consistencia secuencial** - Sin ordenamientos de memoria mas debiles disponibles
4. **Sin punto flotante atomico** - Usar representacion entera si es necesario

### Notas de Plataforma

- Las operaciones atomicas usan `<stdatomic.h>` de C11 internamente
- Disponible en todas las plataformas que soportan hilos POSIX
- Garantizado estar libre de bloqueos en sistemas modernos de 64 bits

---

## Ver Tambien

- [Async/Concurrencia](async-concurrency.md) - Creacion de tareas y canales
- [Gestion de Memoria](../language-guide/memory.md) - Asignacion de punteros y buffers
- [API de Memoria](../reference/memory-api.md) - Funciones de asignacion
