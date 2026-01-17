# Async/Concurrencia en Hemlock

Hemlock proporciona **concurrencia estructurada** con sintaxis async/await, creacion de tareas y canales para comunicacion. La implementacion utiliza hilos POSIX (pthreads) para **VERDADERO paralelismo multihilo**.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Modelo de Hilos](#modelo-de-hilos)
- [Funciones Async](#funciones-async)
- [Creacion de Tareas](#creacion-de-tareas)
- [Canales](#canales)
- [Propagacion de Excepciones](#propagacion-de-excepciones)
- [Detalles de Implementacion](#detalles-de-implementacion)
- [Mejores Practicas](#mejores-practicas)
- [Caracteristicas de Rendimiento](#caracteristicas-de-rendimiento)
- [Limitaciones Actuales](#limitaciones-actuales)

## Vision General

**Lo que esto significa:**
- ✅ **Hilos reales del SO** - Cada tarea creada se ejecuta en un pthread separado (hilo POSIX)
- ✅ **Verdadero paralelismo** - Las tareas se ejecutan simultaneamente en multiples nucleos de CPU
- ✅ **Planificado por el kernel** - El planificador del SO distribuye las tareas entre los nucleos disponibles
- ✅ **Canales seguros para hilos** - Utiliza mutexes y variables de condicion de pthread para sincronizacion

**Lo que esto NO es:**
- ❌ **NO son hilos verdes** - No es multitarea cooperativa en espacio de usuario
- ❌ **NO son corrutinas async/await** - No es un bucle de eventos de un solo hilo como JavaScript/Python asyncio
- ❌ **NO es concurrencia emulada** - No es paralelismo simulado

Este es el **mismo modelo de hilos que C, C++ y Rust** cuando se usan hilos del SO. Obtienes ejecucion paralela real a traves de multiples nucleos.

## Modelo de Hilos

### Hilos 1:1

Hemlock utiliza un **modelo de hilos 1:1**, donde:
- Cada tarea creada crea un hilo dedicado del SO via `pthread_create()`
- El kernel del SO planifica los hilos a traves de los nucleos de CPU disponibles
- Multitarea preventiva - el SO puede interrumpir y cambiar entre hilos
- **Sin GIL** - A diferencia de Python, no hay un Bloqueo Global del Interprete limitando el paralelismo

### Mecanismos de Sincronizacion

- **Mutexes** - Los canales usan `pthread_mutex_t` para acceso seguro entre hilos
- **Variables de condicion** - send/recv bloqueantes usan `pthread_cond_t` para espera eficiente
- **Operaciones sin bloqueo** - Las transiciones de estado de tareas son atomicas

## Funciones Async

Las funciones pueden declararse como `async` para indicar que estan disenadas para ejecucion concurrente:

```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
```

### Puntos Clave

- `async fn` declara una funcion asincrona
- Las funciones async pueden crearse como tareas concurrentes usando `spawn()`
- Las funciones async tambien pueden llamarse directamente (se ejecuta sincronicamente en el hilo actual)
- Cuando se crean, cada tarea se ejecuta en su **propio hilo del SO** (no es una corrutina!)
- La palabra clave `await` esta reservada para uso futuro

### Ejemplo: Llamada Directa vs Spawn

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Llamada directa - se ejecuta sincronicamente
let result1 = factorial(5);  // 120

// Tarea creada - se ejecuta en hilo separado
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## Creacion de Tareas

Usa `spawn()` para ejecutar funciones async **en paralelo en hilos separados del SO**:

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Crear multiples tareas - estas se ejecutan en PARALELO en diferentes nucleos de CPU!
let t1 = spawn(factorial, 5);  // Hilo 1
let t2 = spawn(factorial, 6);  // Hilo 2
let t3 = spawn(factorial, 7);  // Hilo 3

// Las tres estan computando simultaneamente ahora mismo!

// Esperar resultados
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### Funciones Integradas

#### spawn(async_fn, arg1, arg2, ...)

Crea una nueva tarea en un nuevo pthread, retorna el manejador de tarea.

**Parametros:**
- `async_fn` - La funcion async a ejecutar
- `arg1, arg2, ...` - Argumentos a pasar a la funcion

**Retorna:** Manejador de tarea (valor opaco usado con `join()` o `detach()`)

**Ejemplo:**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... logica de procesamiento
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

Espera a que la tarea complete (bloquea hasta que el hilo termine), retorna el resultado.

**Parametros:**
- `task` - Manejador de tarea retornado por `spawn()`

**Retorna:** El valor retornado por la funcion async

**Ejemplo:**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // Bloquea hasta que compute() termine
print(result);
```

**Importante:** Cada tarea solo puede unirse una vez. Uniones posteriores daran error.

#### detach(task)

Ejecucion de disparar y olvidar (el hilo se ejecuta independientemente, no se permite union).

**Parametros:**
- `task` - Manejador de tarea retornado por `spawn()`

**Retorna:** `null`

**Ejemplo:**
```hemlock
async fn background_work() {
    // Tarea de fondo de larga duracion
    // ...
}

let task = spawn(background_work);
detach(task);  // La tarea se ejecuta independientemente, no se puede unir
```

**Importante:** Las tareas desacopladas no pueden unirse. Tanto el pthread como la estructura Task se limpian automaticamente cuando la tarea completa.

## Canales

Los canales proporcionan comunicacion segura entre hilos usando un buffer limitado con semantica de bloqueo.

### Creando Canales

```hemlock
let ch = channel(10);  // Crear canal con tamano de buffer de 10
```

**Parametros:**
- `capacity` (i32) - Numero maximo de valores que el canal puede contener

**Retorna:** Objeto Canal

### Metodos de Canal

#### send(value)

Enviar valor al canal (bloquea si esta lleno).

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let task = spawn(producer, ch, 5);
```

**Comportamiento:**
- Si el canal tiene espacio, el valor se agrega inmediatamente
- Si el canal esta lleno, el emisor bloquea hasta que haya espacio disponible
- Si el canal esta cerrado, lanza una excepcion

#### recv()

Recibir valor del canal (bloquea si esta vacio).

```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let task = spawn(consumer, ch, 5);
```

**Comportamiento:**
- Si el canal tiene valores, retorna el siguiente valor inmediatamente
- Si el canal esta vacio, el receptor bloquea hasta que haya un valor disponible
- Si el canal esta cerrado y vacio, retorna `null`

#### close()

Cerrar canal (recv en canal cerrado retorna null).

```hemlock
ch.close();
```

**Comportamiento:**
- Previene futuras operaciones `send()` (lanzara excepcion)
- Permite que las operaciones `recv()` pendientes completen
- Una vez vacio, `recv()` retorna `null`

### Multiplexacion con select()

La funcion `select()` permite esperar en multiples canales simultaneamente, retornando cuando cualquier canal tiene datos disponibles.

**Firma:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parametros:**
- `channels` - Array de valores de canal
- `timeout_ms` (opcional) - Tiempo de espera en milisegundos (-1 u omitir para espera infinita)

**Retorna:**
- `{ channel, value }` - Objeto con el canal que tenia datos y el valor recibido
- `null` - En tiempo de espera agotado (si se especifico timeout)

**Ejemplo:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Tareas productoras
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// Esperar primer resultado (ch2 deberia ser mas rapido)
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"

// Esperar segundo resultado
let result2 = select([ch1, ch2]);
print(result2.value);  // "from channel 1"
```

**Con tiempo de espera:**
```hemlock
let ch = channel(1);

// Sin emisor, se agotara el tiempo
let result = select([ch], 100);  // 100ms de timeout
if (result == null) {
    print("Timed out!");
}
```

**Casos de uso:**
- Esperar el mas rapido de multiples fuentes de datos
- Implementar tiempos de espera en operaciones de canal
- Patrones de bucle de eventos con multiples fuentes de eventos
- Fan-in: fusionar multiples canales en uno

**Patron fan-in:**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // Todos los canales cerrados
        }
        output.send(result.value);
    }
    output.close();
}
```

### Ejemplo Completo de Productor-Consumidor

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Crear canal con tamano de buffer
let ch = channel(10);

// Crear productor y consumidor
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Esperar finalizacion
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### Multi-Productor, Multi-Consumidor

Los canales pueden compartirse de forma segura entre multiples productores y consumidores:

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// Multiples productores
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// Multiples consumidores
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// Esperar a todos
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## Propagacion de Excepciones

Las excepciones lanzadas en tareas creadas se propagan cuando se unen:

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Caught: " + e);  // "Caught: Task failed!"
}
```

### Patrones de Manejo de Excepciones

**Patron 1: Manejar en la tarea**
```hemlock
async fn safe_task() {
    try {
        // operacion riesgosa
    } catch (e) {
        print("Error in task: " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // Sin excepcion propagada
```

**Patron 2: Propagar al llamador**
```hemlock
async fn task_that_throws() {
    throw "error";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("Caught from task: " + e);
}
```

**Patron 3: Tareas desacopladas con excepciones**
```hemlock
async fn detached_task() {
    try {
        // trabajo
    } catch (e) {
        // Debe manejarse internamente - no puede propagarse
        print("Error: " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // No se pueden capturar excepciones de tareas desacopladas
```

## Detalles de Implementacion

### Arquitectura de Hilos

- **Hilos 1:1** - Cada tarea creada crea un hilo dedicado del SO via `pthread_create()`
- **Planificado por el kernel** - El kernel del SO planifica los hilos a traves de los nucleos de CPU disponibles
- **Multitarea preventiva** - El SO puede interrumpir y cambiar entre hilos
- **Sin GIL** - A diferencia de Python, no hay un Bloqueo Global del Interprete limitando el paralelismo

### Implementacion de Canales

Los canales usan un buffer circular con sincronizacion de pthread:

```
Estructura de Canal:
- buffer[] - Array de tamano fijo de Values
- capacity - Numero maximo de elementos
- size - Numero actual de elementos
- head - Posicion de lectura
- tail - Posicion de escritura
- mutex - pthread_mutex_t para acceso seguro entre hilos
- not_empty - pthread_cond_t para recv bloqueante
- not_full - pthread_cond_t para send bloqueante
- closed - Flag booleano
- refcount - Contador de referencias para limpieza
```

**Comportamiento de bloqueo:**
- `send()` en canal lleno: espera en la variable de condicion `not_full`
- `recv()` en canal vacio: espera en la variable de condicion `not_empty`
- Ambas son senalizadas cuando corresponde por la operacion opuesta

### Memoria y Limpieza

- **Tareas unidas:** Limpiadas automaticamente despues de que `join()` retorna
- **Tareas desacopladas:** Limpiadas automaticamente cuando la tarea completa
- **Canales:** Contados por referencia y liberados cuando ya no se usan

## Mejores Practicas

### 1. Siempre Cerrar Canales

```hemlock
async fn producer(ch) {
    // ... enviar valores
    ch.close();  // Importante: senalar que no hay mas valores
}
```

### 2. Usar Concurrencia Estructurada

Crear tareas y unirlas en el mismo ambito:

```hemlock
fn process_data(data) {
    // Crear tareas
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // Siempre unir antes de retornar
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. Manejar Excepciones Apropiadamente

```hemlock
async fn task() {
    try {
        // operacion riesgosa
    } catch (e) {
        // Registrar error
        throw e;  // Re-lanzar si el llamador debe saberlo
    }
}
```

### 4. Usar Capacidad de Canal Apropiada

- **Capacidad pequena (1-10):** Para coordinacion/senalizacion
- **Capacidad media (10-100):** Para productor-consumidor general
- **Capacidad grande (100+):** Para escenarios de alto rendimiento

```hemlock
let signal_ch = channel(1);      // Coordinacion
let work_ch = channel(50);       // Cola de trabajo
let buffer_ch = channel(1000);   // Alto rendimiento
```

### 5. Desacoplar Solo Cuando Sea Necesario

Preferir `join()` sobre `detach()` para mejor gestion de recursos:

```hemlock
// Bueno: Unir y obtener resultado
let task = spawn(work);
let result = join(task);

// Usar detach solo para verdadero disparar y olvidar
let bg_task = spawn(background_logging);
detach(bg_task);  // Se ejecutara independientemente
```

## Caracteristicas de Rendimiento

### Verdadero Paralelismo

- **N tareas creadas pueden utilizar N nucleos de CPU simultaneamente**
- Aceleracion probada - pruebas de estres muestran 8-9x tiempo de CPU vs tiempo real (multiples nucleos trabajando)
- Escalado lineal con numero de nucleos (hasta el conteo de hilos)

### Sobrecarga de Hilos

- Cada tarea tiene ~8KB de pila + sobrecarga de pthread
- Costo de creacion de hilo: ~10-20us
- Costo de cambio de contexto: ~1-5us

### Cuando Usar Async

**Buenos casos de uso:**
- Computaciones intensivas de CPU que pueden paralelizarse
- Operaciones limitadas por I/O (aunque I/O sigue siendo bloqueante)
- Procesamiento concurrente de datos independientes
- Arquitecturas de pipeline con canales

**No ideal para:**
- Tareas muy cortas (la sobrecarga de hilos domina)
- Tareas con sincronizacion pesada (sobrecarga de contencion)
- Sistemas de un solo nucleo (sin beneficio de paralelismo)

### I/O Bloqueante Seguro

Las operaciones bloqueantes en una tarea no bloquean otras:

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // Bloquea solo este hilo
    let content = f.read();       // Bloquea solo este hilo
    f.close();
    return content;
}

// Ambos leen concurrentemente (en diferentes hilos)
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## Modelo de Seguridad de Hilos

Hemlock usa un modelo de concurrencia de **paso de mensajes** donde las tareas se comunican via canales en lugar de estado mutable compartido.

### Aislamiento de Argumentos

Cuando creas una tarea, **los argumentos se copian profundamente** para prevenir carreras de datos:

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // Modifica la COPIA, no el original
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - sin cambios!
print(modified.length);  // 4 - tiene nuevo elemento
```

**Lo que se copia profundamente:**
- Arrays (y todos los elementos recursivamente)
- Objetos (y todos los campos recursivamente)
- Strings
- Buffers

**Lo que se comparte (referencia retenida):**
- Canales (el mecanismo de comunicacion - compartido intencionalmente)
- Manejadores de tarea (para coordinacion)
- Funciones (el codigo es inmutable)
- Manejadores de archivo (el SO gestiona acceso concurrente)
- Manejadores de socket (el SO gestiona acceso concurrente)

**Lo que no puede pasarse:**
- Punteros crudos (`ptr`) - usar `buffer` en su lugar

### Por Que Paso de Mensajes?

Esto sigue la filosofia de Hemlock de "explicito sobre implicito":

```hemlock
// MAL: Estado mutable compartido (causaria carreras de datos)
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // Carrera!
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // Carrera!

// BIEN: Paso de mensajes via canales
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - sin condicion de carrera
```

### Seguridad de Hilos en Conteo de Referencias

Todas las operaciones de conteo de referencias usan **operaciones atomicas** para prevenir errores de uso despues de liberar:
- `string_retain/release` - atomico
- `array_retain/release` - atomico
- `object_retain/release` - atomico
- `buffer_retain/release` - atomico
- `function_retain/release` - atomico
- `channel_retain/release` - atomico
- `task_retain/release` - atomico

Esto asegura gestion de memoria segura incluso cuando los valores se comparten entre hilos.

### Acceso al Entorno de Clausura

Las tareas tienen acceso al entorno de clausura para:
- Funciones integradas (`print`, `len`, etc.)
- Definiciones de funciones globales
- Constantes y variables

El entorno de clausura esta protegido por un mutex por entorno, haciendo
las lecturas y escrituras concurrentes seguras para hilos:

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK: leyendo variable de clausura (seguro para hilos)
}

async fn modify_closure() {
    x = 20;  // OK: escribiendo variable de clausura (sincronizado con mutex)
}
```

**Nota:** Aunque el acceso concurrente esta sincronizado, modificar estado compartido desde
multiples tareas todavia puede llevar a condiciones de carrera logicas (ordenamiento
no determinista). Para comportamiento predecible, usa canales para comunicacion de tareas o
valores de retorno de tareas.

Si necesitas retornar datos de una tarea, usa el valor de retorno o canales.

## Limitaciones Actuales

### 1. Sin Planificador con Robo de Trabajo

Usa 1 hilo por tarea, lo cual puede ser ineficiente para muchas tareas cortas.

**Actual:** 1000 tareas = 1000 hilos (sobrecarga pesada)

**Planeado:** Pool de hilos con robo de trabajo para mejor eficiencia

### 3. Sin Integracion de I/O Async

Las operaciones de archivo/red todavia bloquean el hilo:

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // Bloquea el hilo
    f.close();
    return content;
}
```

**Solucion temporal:** Usar multiples hilos para operaciones de I/O concurrentes

### 4. Capacidad de Canal Fija

La capacidad del canal se establece en la creacion y no puede redimensionarse:

```hemlock
let ch = channel(10);
// No puede redimensionarse dinamicamente a 20
```

### 5. El Tamano del Canal es Fijo

El tamano del buffer del canal no puede cambiarse despues de la creacion.

## Patrones Comunes

### Map Paralelo

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // Crear workers
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // Enviar datos
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // Recolectar resultados
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // Esperar a los workers
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### Arquitectura de Pipeline

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// Crear pipeline
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// Alimentar entrada
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// Recolectar salida
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### Fan-Out, Fan-In

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // Procesar valor
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// Fan-out: Multiples workers
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// Enviar trabajo
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// Fan-in: Recolectar todos los resultados
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// Esperar a todos los workers
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## Resumen

El modelo de async/concurrencia de Hemlock proporciona:

- ✅ Verdadero paralelismo multihilo usando hilos del SO
- ✅ Primitivas de concurrencia estructurada simples
- ✅ Canales seguros para hilos para comunicacion
- ✅ Propagacion de excepciones a traves de tareas
- ✅ Rendimiento probado en sistemas multinucleo
- ✅ **Aislamiento de argumentos** - copia profunda previene carreras de datos
- ✅ **Conteo de referencias atomico** - gestion de memoria segura a traves de hilos

Esto hace que Hemlock sea adecuado para:
- Computaciones paralelas
- Operaciones de I/O concurrentes
- Arquitecturas de pipeline
- Patrones productor-consumidor

Mientras evita la complejidad de:
- Gestion manual de hilos
- Primitivas de sincronizacion de bajo nivel
- Disenos basados en bloqueos propensos a deadlocks
- Errores de estado mutable compartido
