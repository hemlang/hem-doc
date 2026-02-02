# Propiedad de Memoria en Hemlock

> "Te damos las herramientas para ser seguro, pero no te obligamos a usarlas."

Este documento describe la semántica de propiedad de memoria en Hemlock, cubriendo tanto la memoria gestionada por el programador como los valores gestionados por el runtime.

## Tabla de Contenidos

1. [El Contrato](#el-contrato)
2. [Memoria Gestionada por el Programador](#memoria-gestionada-por-el-programador)
3. [Valores Gestionados por el Runtime](#valores-gestionados-por-el-runtime)
4. [Puntos de Transferencia de Propiedad](#puntos-de-transferencia-de-propiedad)
5. [Async y Concurrencia](#async-y-concurrencia)
6. [Reglas de Memoria FFI](#reglas-de-memoria-ffi)
7. [Seguridad ante Excepciones](#seguridad-ante-excepciones)
8. [Mejores Prácticas](#mejores-prácticas)

---

## El Contrato

Hemlock tiene una división clara de responsabilidad en la gestión de memoria:

| Tipo de Memoria | Gestionado Por | Método de Limpieza |
|-----------------|----------------|-------------------|
| Punteros crudos (`ptr`) | **Programador** | `free(ptr)` |
| Buffers (`buffer`) | **Programador** | `free(buf)` |
| Strings, Arrays, Objetos | **Runtime** | Automático (conteo de referencias) |
| Funciones, Closures | **Runtime** | Automático (conteo de referencias) |
| Tasks, Channels | **Runtime** | Automático (conteo de referencias) |

**El principio central:** Si lo asignas explícitamente, lo liberas explícitamente. Todo lo demás se maneja automáticamente.

---

## Memoria Gestionada por el Programador

### Punteros Crudos

```hemlock
let p = alloc(64);       // Asignar 64 bytes
memset(p, 0, 64);        // Inicializar
// ... usar la memoria ...
free(p);                 // ¡Tu responsabilidad!
```

**Reglas:**
- `alloc()` devuelve memoria que tú posees
- Debes llamar a `free()` cuando termines
- Double-free causará un crash (por diseño)
- Use-after-free es comportamiento indefinido
- La aritmética de punteros está permitida pero no verificada

### Asignación Tipada

```hemlock
let arr = talloc("i32", 100);  // Asignar 100 i32s (400 bytes)
ptr_write_i32(arr, 0, 42);     // Escribir en índice 0
let val = ptr_read_i32(arr, 0); // Leer del índice 0
free(arr);                      // Sigue siendo tu responsabilidad
```

### Buffers (Alternativa Segura)

```hemlock
let buf = buffer(64);    // Buffer con verificación de límites
buf[0] = 42;             // Indexación segura
// buf[100] = 1;         // Error en tiempo de ejecución: fuera de límites
free(buf);               // Aún necesita free explícito
```

**Diferencia clave:** Los buffers proporcionan verificación de límites, los punteros crudos no.

---

## Valores Gestionados por el Runtime

### Conteo de Referencias

Los valores asignados en el heap usan conteo de referencias atómico:

```hemlock
let s1 = "hello";        // String asignado, refcount = 1
let s2 = s1;             // s2 comparte s1, refcount = 2
// Cuando ambos salen del scope, refcount → 0, memoria liberada
```

**Tipos con conteo de referencias:**
- `string` - Texto UTF-8
- `array` - Arrays dinámicos
- `object` - Objetos clave-valor
- `function` - Closures
- `task` - Handles de tareas async
- `channel` - Canales de comunicación

### Detección de Ciclos

El runtime maneja ciclos en grafos de objetos:

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // Ciclo: a → b → a
// El runtime usa conjuntos visitados para detectar y romper ciclos durante la limpieza
```

---

## Puntos de Transferencia de Propiedad

### Enlace de Variables

```hemlock
let x = [1, 2, 3];       // Array creado con refcount 1
                         // x posee la referencia
```

### Retornos de Funciones

```hemlock
fn make_array() {
    return [1, 2, 3];    // La propiedad del array se transfiere al llamador
}
let arr = make_array();  // arr ahora posee la referencia
```

### Asignación

```hemlock
let a = "hello";
let b = a;               // Referencia compartida (refcount incrementado)
b = "world";             // a todavía tiene "hello", b tiene "world"
```

### Operaciones de Channel

```hemlock
let ch = channel(10);
ch.send("message");      // Valor copiado al buffer del channel
                         // El original sigue siendo válido

let msg = ch.recv();     // Recibe propiedad del channel
```

### Spawning de Tasks

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data se COPIA PROFUNDAMENTE para aislamiento
data.x = 2;                       // Seguro - el task tiene su propia copia
let result = join(task);          // La propiedad del result se transfiere al llamador
```

---

## Async y Concurrencia

### Aislamiento de Threads

Los tasks spawneados reciben **copias profundas** de argumentos mutables:

```hemlock
async fn worker(data) {
    data.x = 100;        // Modifica solo la copia del task
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // Seguro - no afecta al task
let result = join(task);
print(obj.x);            // 2 (sin cambios por el task)
print(result.x);         // 100 (copia modificada del task)
```

### Objetos de Coordinación Compartidos

Algunos tipos se comparten por referencia (no se copian):
- **Channels** - Para comunicación entre tasks
- **Tasks** - Para coordinación (join/detach)

```hemlock
let ch = channel(1);
spawn(producer, ch);     // Mismo channel, no una copia
spawn(consumer, ch);     // Ambos tasks comparten el channel
```

### Resultados de Tasks

```hemlock
let task = spawn(compute);
let result = join(task);  // El llamador posee el resultado
                          // La referencia del task se libera cuando el task es liberado
```

### Tasks Desacoplados

```hemlock
detach(spawn(background_work));
// El task corre independientemente
// El resultado se libera automáticamente cuando el task completa
// Sin leak aunque nadie llame a join()
```

---

## Reglas de Memoria FFI

### Pasando a Funciones C

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock retiene la propiedad
                         // El string es válido durante la llamada
                         // La función C NO debe liberarlo
```

### Recibiendo de Funciones C

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C asignó esta memoria
free(copy);                   // Tu responsabilidad liberarla
```

### Pasaje de Structs (Solo Compiler)

```hemlock
// Definir layout de struct C
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // Retornado por valor, copiado
                                // No se necesita limpieza para structs en stack
```

### Memoria de Callbacks

```hemlock
// Cuando C llama de vuelta a Hemlock:
// - Los argumentos son propiedad de C (no liberar)
// - La propiedad del valor de retorno se transfiere a C
```

---

## Seguridad ante Excepciones

### Garantías

El runtime proporciona estas garantías:

1. **Sin leak en salida normal** - Todos los valores gestionados por runtime se limpian
2. **Sin leak en excepción** - Los temporales se liberan durante el stack unwinding
3. **Defer se ejecuta en excepción** - El código de limpieza se ejecuta

### Evaluación de Expresiones

```hemlock
// Si esto lanza durante la creación del array:
let arr = [f(), g(), h()];  // El array parcial se libera

// Si esto lanza durante la llamada a función:
foo(a(), b(), c());         // Los args evaluados previamente se liberan
```

### Defer para Limpieza

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // Se ejecuta al return O excepción

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // ¡f.close() aún se ejecuta!
    }
    return data;
}
```

---

## Mejores Prácticas

### 1. Prefiere Tipos Gestionados por Runtime

```hemlock
// Prefiere esto:
let data = [1, 2, 3, 4, 5];

// Sobre esto (a menos que necesites control de bajo nivel):
let data = talloc("i32", 5);
// ... debes recordar liberar ...
```

### 2. Usa Defer para Memoria Manual

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // Limpieza garantizada

    // ... usar buf ...
    // No necesitas liberar en cada punto de retorno
}
```

### 3. Evita Punteros Crudos en Async

```hemlock
// MAL - el puntero puede liberarse antes de que el task complete
let p = alloc(64);
spawn(worker, p);          // El task obtiene el valor del puntero
free(p);                   // ¡Ups! El task aún lo está usando

// BIEN - usa channels o copia los datos
let ch = channel(1);
let data = buffer(64);
// ... llenar data ...
ch.send(data);             // Copia profunda
spawn(worker, ch);
free(data);                // Seguro - el task tiene su propia copia
```

### 4. Cierra Channels Cuando Termines

```hemlock
let ch = channel(10);
// ... usar channel ...
ch.close();                // Drena y libera valores en buffer
```

### 5. Join o Detach Tasks

```hemlock
let task = spawn(work);

// Opción 1: Esperar el resultado
let result = join(task);

// Opción 2: Fire and forget
// detach(task);

// NO: Dejar que el handle del task salga del scope sin join o detach
// (Se limpiará, pero el resultado puede tener leak)
```

---

## Depuración de Problemas de Memoria

### Habilitar ASAN

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### Ejecutar Tests de Regresión de Leaks

```bash
make leak-regression       # Suite completa
make leak-regression-quick # Omitir test exhaustivo
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## Resumen

| Operación | Comportamiento de Memoria |
|-----------|---------------------------|
| `alloc(n)` | Asigna, tú liberas |
| `buffer(n)` | Asigna con verificación de límites, tú liberas |
| `"string"` | Runtime gestiona |
| `[array]` | Runtime gestiona |
| `{object}` | Runtime gestiona |
| `spawn(fn)` | Copia profunda de args, runtime gestiona task |
| `join(task)` | Llamador posee resultado |
| `detach(task)` | Runtime libera resultado cuando termina |
| `ch.send(v)` | Copia valor al channel |
| `ch.recv()` | Llamador posee valor recibido |
| `ch.close()` | Drena y libera valores en buffer |
