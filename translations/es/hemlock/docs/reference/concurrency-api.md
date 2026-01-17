# Referencia de la API de Concurrencia

Referencia completa para el sistema async/concurrencia de Hemlock.

---

## Descripcion General

Hemlock proporciona **concurrencia estructurada** con verdadero paralelismo multi-hilo usando hilos POSIX (pthreads). Cada tarea generada se ejecuta en un hilo separado del sistema operativo, permitiendo ejecucion paralela real a traves de multiples nucleos de CPU.

**Caracteristicas Principales:**
- Verdadero paralelismo multi-hilo (no hilos verdes)
- Sintaxis de funciones async
- Generacion y union de tareas
- Canales seguros para hilos
- Propagacion de excepciones

**Modelo de Hilos:**
- Hilos reales del SO (POSIX pthreads)
- Verdadero paralelismo (multiples nucleos de CPU)
- Planificacion del kernel (multitarea preemptiva)
- Sincronizacion segura para hilos (mutexes, variables de condicion)

---

## Funciones Async

### Declaracion de Funcion Async

Las funciones pueden declararse como `async` para indicar que estan disenadas para ejecucion concurrente.

**Sintaxis:**
```hemlock
async fn nombre_funcion(params): tipo_retorno {
    // cuerpo de funcion
}
```

**Ejemplos:**
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

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Procesando:", data);
    return null;
}
```

**Comportamiento:**
- `async fn` declara una funcion asincrona
- Puede llamarse sincronicamente (se ejecuta en el hilo actual)
- Puede generarse como tarea concurrente (se ejecuta en nuevo hilo)
- Cuando se genera, se ejecuta en su propio hilo del SO

**Nota:** La palabra clave `await` esta reservada para uso futuro pero no esta implementada actualmente.

---

## Gestion de Tareas

### spawn

Crea e inicia una nueva tarea concurrente.

**Firma:**
```hemlock
spawn(async_fn: function, ...args): task
```

**Parametros:**
- `async_fn` - Funcion async a ejecutar
- `...args` - Argumentos a pasar a la funcion

**Retorna:** Manejador de tarea

**Ejemplos:**
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

// Generar una sola tarea
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// Generar multiples tareas (se ejecutan en paralelo!)
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// Las tres se estan ejecutando simultaneamente
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**Comportamiento:**
- Crea nuevo hilo del SO via `pthread_create()`
- Comienza a ejecutar la funcion inmediatamente
- Retorna manejador de tarea para union posterior
- Las tareas se ejecutan en paralelo en nucleos de CPU separados

---

### join

Espera la finalizacion de la tarea y recupera el resultado.

**Firma:**
```hemlock
join(task: task): any
```

**Parametros:**
- `task` - Manejador de tarea de `spawn()`

**Retorna:** Valor de retorno de la tarea

**Ejemplos:**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // Bloquea hasta que la tarea complete
print(result);         // 3628800
```

**Comportamiento:**
- Bloquea el hilo actual hasta que la tarea complete
- Retorna el valor de retorno de la tarea
- Propaga excepciones lanzadas por la tarea
- Limpia recursos de la tarea despues de retornar

**Manejo de Errores:**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarea fallo!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Capturado:", e);  // "Capturado: Tarea fallo!"
}
```

---

### detach

Desvincula la tarea (ejecucion de disparar y olvidar).

**Firma:**
```hemlock
detach(task: task): null
```

**Parametros:**
- `task` - Manejador de tarea de `spawn()`

**Retorna:** `null`

**Ejemplos:**
```hemlock
async fn background_work() {
    print("Trabajando en segundo plano...");
    return null;
}

let t = spawn(background_work);
detach(t);  // La tarea continua ejecutandose independientemente

// No se puede unir tarea desvinculada
// join(t);  // ERROR
```

**Comportamiento:**
- La tarea continua ejecutandose independientemente
- No se puede hacer `join()` a tarea desvinculada
- La tarea y el hilo se limpian automaticamente cuando la tarea completa

**Casos de Uso:**
- Tareas de segundo plano de disparar y olvidar
- Tareas de logging/monitoreo
- Tareas que no necesitan retornar valores

---

## Canales

Los canales proporcionan comunicacion segura entre hilos para tareas.

### channel

Crea un canal con buffer.

**Firma:**
```hemlock
channel(capacity: i32): channel
```

**Parametros:**
- `capacity` - Tamano del buffer (numero de valores)

**Retorna:** Objeto Canal

**Ejemplos:**
```hemlock
let ch = channel(10);  // Canal con buffer de capacidad 10
let ch2 = channel(1);  // Buffer minimo (sincrono)
let ch3 = channel(100); // Buffer grande
```

**Comportamiento:**
- Crea canal seguro para hilos
- Usa mutexes pthread para sincronizacion
- La capacidad es fija al momento de creacion

---

### Metodos de Canal

#### send

Envia valor al canal (bloquea si esta lleno).

**Firma:**
```hemlock
channel.send(value: any): null
```

**Parametros:**
- `value` - Valor a enviar (cualquier tipo)

**Retorna:** `null`

**Ejemplos:**
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
let t = spawn(producer, ch, 5);
```

**Comportamiento:**
- Envia valor al canal
- Bloquea si el canal esta lleno
- Seguro para hilos (usa mutex)
- Retorna despues de que el valor se envia

---

#### recv

Recibe valor del canal (bloquea si esta vacio).

**Firma:**
```hemlock
channel.recv(): any
```

**Retorna:** Valor del canal, o `null` si el canal esta cerrado y vacio

**Ejemplos:**
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
let t = spawn(consumer, ch, 5);
```

**Comportamiento:**
- Recibe valor del canal
- Bloquea si el canal esta vacio
- Retorna `null` si el canal esta cerrado y vacio
- Seguro para hilos (usa mutex)

---

#### close

Cierra el canal (no se permiten mas envios).

**Firma:**
```hemlock
channel.close(): null
```

**Retorna:** `null`

**Ejemplos:**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // Senalar que no hay mas valores
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // Canal cerrado
        }
        print(val);
    }
    return null;
}
```

**Comportamiento:**
- Cierra el canal
- No se permiten mas envios
- `recv()` retorna `null` cuando el canal esta vacio
- Seguro para hilos

---

## Ejemplo Completo de Concurrencia

### Patron Productor-Consumidor

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Produciendo:", i);
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
        print("Consumiendo:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Crear canal
let ch = channel(10);

// Generar productor y consumidor
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Esperar finalizacion
join(p);
let total = join(c);
print("Total:", total);  // 0+10+20+30+40 = 100
```

---

## Computacion Paralela

### Ejemplo de Multiples Tareas

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Generar multiples tareas (se ejecutan en paralelo!)
let t1 = spawn(factorial, 5);   // Hilo 1
let t2 = spawn(factorial, 6);   // Hilo 2
let t3 = spawn(factorial, 7);   // Hilo 3
let t4 = spawn(factorial, 8);   // Hilo 4

// Las cuatro estan computando simultaneamente!

// Esperar resultados
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## Ciclo de Vida de Tareas

### Transiciones de Estado

1. **Creada** - Tarea generada pero aun no ejecutando
2. **Ejecutando** - Tarea ejecutandose en hilo del SO
3. **Completada** - Tarea terminada (resultado disponible)
4. **Unida** - Resultado recuperado, recursos limpiados
5. **Desvinculada** - Tarea continua independientemente

### Ejemplo de Ciclo de Vida

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. Crear tarea
let t = spawn(work, 21);  // Estado: Ejecutando

// La tarea se ejecuta en hilo separado...

// 2. Unir tarea
let result = join(t);     // Estado: Completada -> Unida
print(result);            // 42

// Recursos de tarea limpiados despues de union
```

### Ciclo de Vida Desvinculado

```hemlock
async fn background() {
    print("Tarea de segundo plano ejecutandose");
    return null;
}

// 1. Crear tarea
let t = spawn(background);  // Estado: Ejecutando

// 2. Desvincular tarea
detach(t);                  // Estado: Desvinculada

// La tarea continua ejecutandose independientemente
// Recursos limpiados por el SO cuando termina
```

---

## Manejo de Errores

### Propagacion de Excepciones

Las excepciones lanzadas en tareas se propagan cuando se unen:

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarea fallo!";
    }
    return 42;
}

// Tarea que tiene exito
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// Tarea que falla
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Capturado:", e);  // "Capturado: Tarea fallo!"
}
```

### Manejando Multiples Tareas

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarea " + typeof(id) + " fallo";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // Fallara
let t3 = spawn(work, 3, 0);

// Unir con manejo de errores
try {
    let r1 = join(t1);  // OK
    print("Tarea 1:", r1);

    let r2 = join(t2);  // Lanza
    print("Tarea 2:", r2);  // Nunca se alcanza
} catch (e) {
    print("Error:", e);  // "Error: Tarea 2 fallo"
}

// Aun se puede unir la tarea restante
let r3 = join(t3);
print("Tarea 3:", r3);
```

---

## Caracteristicas de Rendimiento

### Verdadero Paralelismo

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Ejecucion secuencial
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// Ejecucion paralela
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// parallel_time deberia ser ~50% de sequential_time en sistemas multi-nucleo
```

**Caracteristicas Comprobadas:**
- N tareas pueden utilizar N nucleos de CPU simultaneamente
- Pruebas de estres muestran 8-9x tiempo de CPU vs tiempo real (prueba de paralelismo)
- Sobrecarga de hilo: ~8KB de pila + sobrecarga de pthread por tarea
- Operaciones bloqueantes en una tarea no bloquean otras

---

## Detalles de Implementacion

### Modelo de Hilos

- **Hilos 1:1** - Cada tarea = 1 hilo del SO (`pthread`)
- **Planificacion del kernel** - El kernel del SO distribuye hilos entre nucleos
- **Multitarea preemptiva** - El SO puede interrumpir y cambiar hilos
- **Sin GIL** - Sin Bloqueo Global del Interprete (a diferencia de Python)

### Sincronizacion

- **Mutexes** - Los canales usan `pthread_mutex_t`
- **Variables de condicion** - send/recv bloqueantes usan `pthread_cond_t`
- **Operaciones sin bloqueo** - Las transiciones de estado de tarea son atomicas

### Memoria y Limpieza

- **Tareas unidas** - Limpiadas automaticamente despues de `join()`
- **Tareas desvinculadas** - Limpiadas automaticamente cuando la tarea completa
- **Canales** - Con conteo de referencias, liberados cuando ya no se usan

---

## Limitaciones

- Sin `select()` para multiplexar multiples canales
- Sin planificador de robo de trabajo (1 hilo por tarea)
- Sin integracion de E/S async (operaciones de archivo/red bloquean)
- Capacidad del canal fija al momento de creacion

---

## Resumen Completo de la API

### Funciones

| Funcion   | Firma                             | Retorna   | Descripcion                    |
|-----------|-----------------------------------|-----------|--------------------------------|
| `spawn`   | `(async_fn: function, ...args)`   | `task`    | Crear e iniciar tarea concurrente |
| `join`    | `(task: task)`                    | `any`     | Esperar tarea, obtener resultado |
| `detach`  | `(task: task)`                    | `null`    | Desvincular tarea (disparar y olvidar) |
| `channel` | `(capacity: i32)`                 | `channel` | Crear canal seguro para hilos  |

### Metodos de Canal

| Metodo  | Firma           | Retorna | Descripcion                      |
|---------|-----------------|---------|----------------------------------|
| `send`  | `(value: any)`  | `null`  | Enviar valor (bloquea si lleno)  |
| `recv`  | `()`            | `any`   | Recibir valor (bloquea si vacio) |
| `close` | `()`            | `null`  | Cerrar canal                     |

### Tipos

| Tipo      | Descripcion                          |
|-----------|--------------------------------------|
| `task`    | Manejador para tarea concurrente     |
| `channel` | Canal de comunicacion seguro para hilos |

---

## Mejores Practicas

### Hacer

- Use canales para comunicacion entre tareas
- Maneje excepciones de tareas unidas
- Cierre canales cuando termine de enviar
- Use `join()` para obtener resultados y limpiar
- Genere solo funciones async

### No Hacer

- No comparta estado mutable sin sincronizacion
- No una la misma tarea dos veces
- No envie en canales cerrados
- No genere funciones no-async
- No olvide unir tareas (a menos que esten desvinculadas)

---

## Ver Tambien

- [Funciones Integradas](builtins.md) - `spawn()`, `join()`, `detach()`, `channel()`
- [Sistema de Tipos](type-system.md) - Tipos de tarea y canal
