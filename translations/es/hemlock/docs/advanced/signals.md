# Manejo de Senales en Hemlock

Hemlock proporciona **manejo de senales POSIX** para gestionar senales del sistema como SIGINT (Ctrl+C), SIGTERM y senales personalizadas. Esto habilita control de procesos de bajo nivel y comunicacion entre procesos.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [API de Senales](#api-de-senales)
- [Constantes de Senal](#constantes-de-senal)
- [Manejo Basico de Senales](#manejo-basico-de-senales)
- [Patrones Avanzados](#patrones-avanzados)
- [Comportamiento del Manejador de Senales](#comportamiento-del-manejador-de-senales)
- [Consideraciones de Seguridad](#consideraciones-de-seguridad)
- [Casos de Uso Comunes](#casos-de-uso-comunes)
- [Ejemplos Completos](#ejemplos-completos)

## Vision General

El manejo de senales permite a los programas:
- Responder a interrupciones de usuario (Ctrl+C, Ctrl+Z)
- Implementar apagado gracioso
- Manejar solicitudes de terminacion
- Usar senales personalizadas para comunicacion entre procesos
- Crear mecanismos de alarma/temporizador

**Importante:** El manejo de senales es **inherentemente inseguro** en la filosofia de Hemlock. Los manejadores pueden llamarse en cualquier momento, interrumpiendo la ejecucion normal. El usuario es responsable de la sincronizacion apropiada.

## API de Senales

### signal(signum, handler_fn)

Registrar una funcion manejadora de senal.

**Parametros:**
- `signum` (i32) - Numero de senal (constante como SIGINT, SIGTERM)
- `handler_fn` (funcion o null) - Funcion a llamar cuando se recibe la senal, o `null` para restablecer al comportamiento por defecto

**Retorna:** La funcion manejadora anterior (o `null` si no habia ninguna)

**Ejemplo:**
```hemlock
fn my_handler(sig) {
    print("Caught signal: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**Restableciendo al comportamiento por defecto:**
```hemlock
signal(SIGINT, null);  // Restablecer SIGINT al comportamiento por defecto
```

### raise(signum)

Enviar una senal al proceso actual.

**Parametros:**
- `signum` (i32) - Numero de senal a enviar

**Retorna:** `null`

**Ejemplo:**
```hemlock
raise(SIGUSR1);  // Disparar manejador de SIGUSR1
```

## Constantes de Senal

Hemlock proporciona constantes de senal POSIX estandar como valores i32.

### Interrupcion y Terminacion

| Constante | Valor | Descripcion | Disparador Comun |
|-----------|-------|-------------|------------------|
| `SIGINT` | 2 | Interrupcion desde teclado | Ctrl+C |
| `SIGTERM` | 15 | Solicitud de terminacion | Comando `kill` |
| `SIGQUIT` | 3 | Salir desde teclado | Ctrl+\ |
| `SIGHUP` | 1 | Hangup detectado | Terminal cerrada |
| `SIGABRT` | 6 | Senal de aborto | Funcion `abort()` |

**Ejemplos:**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // Comando kill
signal(SIGHUP, handle_hangup);      // Terminal se cierra
```

### Senales Definidas por Usuario

| Constante | Valor | Descripcion | Caso de Uso |
|-----------|-------|-------------|-------------|
| `SIGUSR1` | 10 | Senal definida por usuario 1 | IPC personalizado |
| `SIGUSR2` | 12 | Senal definida por usuario 2 | IPC personalizado |

**Ejemplos:**
```hemlock
// Usar para comunicacion personalizada
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### Control de Proceso

| Constante | Valor | Descripcion | Notas |
|-----------|-------|-------------|-------|
| `SIGALRM` | 14 | Temporizador de alarma | Despues de `alarm()` |
| `SIGCHLD` | 17 | Cambio de estado de proceso hijo | Gestion de procesos |
| `SIGCONT` | 18 | Continuar si esta detenido | Reanudar despues de SIGSTOP |
| `SIGSTOP` | 19 | Detener proceso | **No puede capturarse** |
| `SIGTSTP` | 20 | Detener desde terminal | Ctrl+Z |

**Ejemplos:**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### Senales de E/S

| Constante | Valor | Descripcion | Cuando se Envia |
|-----------|-------|-------------|-----------------|
| `SIGPIPE` | 13 | Pipe roto | Escribir a pipe cerrado |
| `SIGTTIN` | 21 | Lectura en segundo plano desde terminal | Proceso BG lee TTY |
| `SIGTTOU` | 22 | Escritura en segundo plano a terminal | Proceso BG escribe TTY |

**Ejemplos:**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## Manejo Basico de Senales

### Capturando Ctrl+C

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("Caught SIGINT!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// El programa continua ejecutandose...
// El usuario presiona Ctrl+C -> handle_interrupt() es llamada

while (!interrupted) {
    // Hacer trabajo...
}

print("Exiting due to interrupt");
```

### Firma de Funcion Manejadora

Los manejadores de senal reciben un argumento: el numero de senal (i32)

```hemlock
fn my_handler(signum) {
    print("Received signal: " + typeof(signum));
    // signum contiene el numero de senal (ej. 2 para SIGINT)

    if (signum == SIGINT) {
        print("This is SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // Mismo manejador para multiples senales
```

### Multiples Manejadores de Senal

Diferentes manejadores para diferentes senales:

```hemlock
fn handle_int(sig) {
    print("SIGINT received");
}

fn handle_term(sig) {
    print("SIGTERM received");
}

fn handle_usr1(sig) {
    print("SIGUSR1 received");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### Restableciendo al Comportamiento por Defecto

Pasar `null` como manejador para restablecer al comportamiento por defecto:

```hemlock
// Registrar manejador personalizado
signal(SIGINT, my_handler);

// Despues, restablecer al comportamiento por defecto (terminar en SIGINT)
signal(SIGINT, null);
```

### Enviando Senales Manualmente

Enviar senales a tu propio proceso:

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// Disparar manejador manualmente
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## Patrones Avanzados

### Patron de Apagado Gracioso

Patron comun para limpieza en terminacion:

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Shutting down gracefully...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// Bucle principal
while (!should_exit) {
    // Hacer trabajo...
    // Verificar flag should_exit periodicamente
}

print("Cleanup complete");
```

### Contador de Senales

Rastrear numero de senales recibidas:

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Received " + typeof(signal_count) + " signals");
}

signal(SIGUSR1, count_signals);

// Despues...
print("Total signals: " + typeof(signal_count));
```

### Recarga de Configuracion en Senal

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Reloading configuration...");
    config = load_config();
    print("Configuration reloaded");
}

signal(SIGHUP, reload_config);  // Recargar en SIGHUP

// Enviar SIGHUP al proceso para recargar config
// Desde shell: kill -HUP <pid>
```

### Timeout Usando SIGALRM

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// Establecer alarma (aun no implementado en Hemlock, solo ejemplo)
// alarm(5);  // timeout de 5 segundos

while (!timed_out) {
    // Hacer trabajo con timeout
}
```

### Maquina de Estados Basada en Senales

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("State: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("State: " + typeof(state));
}

signal(SIGUSR1, next_state);  // Avanzar estado
signal(SIGUSR2, prev_state);  // Retroceder

// Controlar maquina de estados:
// kill -USR1 <pid>  # Siguiente estado
// kill -USR2 <pid>  # Estado anterior
```

## Comportamiento del Manejador de Senales

### Notas Importantes

**Ejecucion del Manejador:**
- Los manejadores se llaman **sincronicamente** cuando se recibe la senal
- Los manejadores se ejecutan en el contexto del proceso actual
- Los manejadores de senal comparten el entorno de clausura de la funcion donde fueron definidos
- Los manejadores pueden acceder y modificar variables del ambito exterior (como globales o variables capturadas)

**Mejores Practicas:**
- Mantener los manejadores simples y rapidos - evitar operaciones de larga duracion
- Establecer flags en lugar de realizar logica compleja
- Evitar llamar funciones que puedan tomar bloqueos
- Estar consciente de que los manejadores pueden interrumpir cualquier operacion

### Que Senales Pueden Capturarse

**Pueden capturarse y manejarse:**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (pero el programa abortara despues de que el manejador retorne)

**No pueden capturarse:**
- `SIGKILL` (9) - Siempre termina el proceso
- `SIGSTOP` (19) - Siempre detiene el proceso

**Dependiente del sistema:**
- Algunas senales tienen comportamientos por defecto que pueden diferir por sistema
- Verificar la documentacion de senales de tu plataforma para detalles

### Limitaciones del Manejador

```hemlock
fn complex_handler(sig) {
    // Evitar esto en manejadores de senal:

    // ❌ Operaciones de larga duracion
    // process_large_file();

    // ❌ E/S bloqueante
    // let f = open("log.txt", "a");
    // f.write("Signal received\n");

    // ❌ Cambios de estado complejos
    // rebuild_entire_data_structure();

    // ✅ Establecer flag simple es seguro
    let should_stop = true;

    // ✅ Actualizaciones simples de contador usualmente son seguras
    let signal_count = signal_count + 1;
}
```

## Consideraciones de Seguridad

El manejo de senales es **inherentemente inseguro** en la filosofia de Hemlock.

### Condiciones de Carrera

Los manejadores pueden llamarse en cualquier momento, interrumpiendo la ejecucion normal:

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // Condicion de carrera si se llama durante actualizacion de counter
}

signal(SIGUSR1, increment);

// El codigo principal tambien modifica counter
counter = counter + 1;  // Podria ser interrumpido por manejador de senal
```

**Problema:** Si la senal llega mientras el codigo principal esta actualizando `counter`, el resultado es impredecible.

### Seguridad Async-Signal

Hemlock **no** garantiza seguridad async-signal:
- Los manejadores pueden llamar cualquier codigo de Hemlock (a diferencia de las funciones async-signal-safe restringidas de C)
- Esto proporciona flexibilidad pero requiere precaucion del usuario
- Las condiciones de carrera son posibles si el manejador modifica estado compartido

### Mejores Practicas para Manejo Seguro de Senales

**1. Usar Flags Atomicos**

Asignaciones booleanas simples son generalmente seguras:

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // Asignacion simple es segura
}

signal(SIGINT, handler);

while (!should_exit) {
    // trabajo...
}
```

**2. Minimizar Estado Compartido**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // Solo modificar esta variable
    interrupt_count = interrupt_count + 1;
}
```

**3. Diferir Operaciones Complejas**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // Solo establecer flag
}

signal(SIGHUP, signal_reload);

// En bucle principal:
while (true) {
    if (pending_reload) {
        reload_config();  // Hacer trabajo complejo aqui
        pending_reload = false;
    }

    // Trabajo normal...
}
```

**4. Evitar Problemas de Reentrada**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // No modificar data mientras el codigo principal lo esta usando
        return;
    }
    // Seguro proceder
}
```

## Casos de Uso Comunes

### 1. Apagado Gracioso de Servidor

```hemlock
let running = true;

fn shutdown(sig) {
    print("Shutdown signal received");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Bucle principal del servidor
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Server stopped");
```

### 2. Recarga de Configuracion (Sin Reinicio)

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Reloading configuration...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // Usar config...
}
```

### 3. Rotacion de Logs

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // Renombrar log viejo, abrir nuevo
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // Logging normal...
    log_file.write("Log entry\n");
}
```

### 4. Reporte de Estado

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Status: " + typeof(requests_handled) + " requests handled");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// Desde shell: kill -USR1 <pid>
```

### 5. Alternar Modo Debug

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Debug mode: ON");
    } else {
        print("Debug mode: OFF");
    }
}

signal(SIGUSR2, toggle_debug);

// Desde shell: kill -USR2 <pid> para alternar
```

## Ejemplos Completos

### Ejemplo 1: Manejador de Interrupcion con Limpieza

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Interrupt detected (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("User signal 1 received");
    }
}

// Registrar manejadores
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// Simular algo de trabajo
let i = 0;
while (running && i < 100) {
    print("Working... " + typeof(i));

    // Disparar SIGUSR1 cada 10 iteraciones
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Total signals received: " + typeof(signal_count));
```

### Ejemplo 2: Maquina de Estados Multi-Senal

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("State: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("State: " + state);
}

fn report_stats(sig) {
    print("State: " + state);
    print("Requests: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // Hacer trabajo
        request_count = request_count + 1;
    }

    // Verificar cada iteracion...
}
```

### Ejemplo 3: Controlador de Pool de Workers

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Workers: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Workers: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Shutting down...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// El bucle principal ajusta pool de workers basado en worker_count
while (!should_exit) {
    // Gestionar workers basado en worker_count
    // ...
}
```

### Ejemplo 4: Patron de Timeout

```hemlock
let operation_complete = false;
let timed_out = false;

fn timeout_handler(sig) {
    timed_out = true;
}

signal(SIGALRM, timeout_handler);

// Iniciar operacion larga
async fn long_operation() {
    // ... trabajo
    operation_complete = true;
}

let task = spawn(long_operation);

// Esperar con timeout (verificacion manual)
let elapsed = 0;
while (!operation_complete && elapsed < 1000) {
    // Dormir o verificar
    elapsed = elapsed + 1;
}

if (!operation_complete) {
    print("Operation timed out");
    detach(task);  // Abandonar espera
} else {
    join(task);
    print("Operation completed");
}
```

## Depurando Manejadores de Senal

### Agregar Prints de Diagnostico

```hemlock
fn debug_handler(sig) {
    print("Handler called for signal: " + typeof(sig));
    print("Stack: (not yet available)");

    // Tu logica de manejador...
}

signal(SIGINT, debug_handler);
```

### Contar Llamadas de Senal

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Handler call #" + typeof(handler_calls));

    // Tu logica de manejador...
}
```

### Probar con raise()

```hemlock
fn test_handler(sig) {
    print("Test signal received: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// Probar enviando manualmente
raise(SIGUSR1);
print("Handler should have been called");
```

## Resumen

El manejo de senales de Hemlock proporciona:

- ✅ Manejo de senales POSIX para control de procesos de bajo nivel
- ✅ 15 constantes de senal estandar
- ✅ API simple de signal() y raise()
- ✅ Funciones manejadoras flexibles con soporte de clausura
- ✅ Multiples senales pueden compartir manejadores

Recuerda:
- El manejo de senales es inherentemente inseguro - usar con precaucion
- Mantener los manejadores simples y rapidos
- Usar flags para cambios de estado, no operaciones complejas
- Los manejadores pueden interrumpir la ejecucion en cualquier momento
- No se pueden capturar SIGKILL o SIGSTOP
- Probar manejadores exhaustivamente con raise()

Patrones comunes:
- Apagado gracioso (SIGINT, SIGTERM)
- Recarga de configuracion (SIGHUP)
- Rotacion de logs (SIGUSR1)
- Reporte de estado (SIGUSR1/SIGUSR2)
- Alternar modo debug (SIGUSR2)
