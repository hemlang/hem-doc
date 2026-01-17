# Detalles de Implementacion de Hemlock

Este documento describe la implementacion tecnica del lenguaje Hemlock, incluyendo la estructura del proyecto, el pipeline de compilacion, la arquitectura del runtime y las decisiones de diseno.

---

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Pipeline de Compilacion](#pipeline-de-compilacion)
- [Diseno Modular del Interprete](#diseno-modular-del-interprete)
- [Arquitectura del Runtime](#arquitectura-del-runtime)
- [Representacion de Valores](#representacion-de-valores)
- [Implementacion del Sistema de Tipos](#implementacion-del-sistema-de-tipos)
- [Gestion de Memoria](#gestion-de-memoria)
- [Modelo de Concurrencia](#modelo-de-concurrencia)
- [Planes Futuros](#planes-futuros)

---

## Estructura del Proyecto

```
hemlock/
├── src/
│   ├── frontend/              # Compartido: lexer, parser, AST
│   │   ├── lexer.c            # Tokenizacion
│   │   ├── parser/            # Parser de descenso recursivo
│   │   ├── ast.c              # Gestion de nodos AST
│   │   └── module.c           # Resolucion de modulos
│   ├── backends/
│   │   ├── interpreter/       # hemlock: interprete de recorrido de arbol
│   │   │   ├── main.c         # Punto de entrada CLI
│   │   │   ├── runtime.c      # Evaluacion de expresiones/sentencias
│   │   │   ├── builtins.c     # Funciones integradas
│   │   │   └── ...
│   │   └── compiler/          # hemlockc: generador de codigo C
│   │       ├── main.c         # CLI, orquestacion
│   │       ├── type_check.c   # Verificacion de tipos en compilacion
│   │       ├── codegen.c      # Contexto de generacion de codigo
│   │       ├── codegen_expr.c # Codegen de expresiones
│   │       ├── codegen_stmt.c # Codegen de sentencias
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # Protocolo de Servidor de Lenguaje
│   │   └── bundler/           # Herramientas de empaquetado
├── runtime/                   # libhemlock_runtime.a (para programas compilados)
├── stdlib/                    # Biblioteca estandar (39 modulos)
│   └── docs/                  # Documentacion de modulos
├── tests/
│   ├── parity/                # Pruebas que deben pasar ambos backends
│   ├── interpreter/           # Pruebas especificas del interprete
│   └── compiler/              # Pruebas especificas del compilador
├── examples/                  # Programas de ejemplo
└── docs/                      # Documentacion
```

### Organizacion de Directorios

**`include/`** - Headers de API publica que definen la interfaz entre componentes:
- Separacion limpia entre lexer, parser, AST e interprete
- Declaraciones adelantadas para minimizar dependencias
- API publica para incrustar Hemlock en otros programas

**`src/`** - Archivos de implementacion:
- Los archivos de nivel superior manejan lexing, parsing, gestion de AST
- `main.c` proporciona CLI y REPL
- El interprete esta modularizado en subsistemas separados

**`src/interpreter/`** - Implementacion modular del interprete:
- Cada modulo tiene una responsabilidad unica y clara
- API interna definida en `internal.h` para comunicacion entre modulos
- Los modulos pueden compilarse independientemente para compilaciones mas rapidas

**`tests/`** - Suite de pruebas completa:
- Organizada por area de caracteristica
- Cada directorio contiene casos de prueba enfocados
- `run_tests.sh` orquesta la ejecucion de pruebas

---

## Pipeline de Compilacion

Hemlock usa un pipeline de compilacion tradicional con fases distintas:

### Fase 1: Analisis Lexico (Lexer)

**Entrada:** Texto de codigo fuente
**Salida:** Flujo de tokens
**Implementacion:** `src/lexer.c`

```
Fuente: "let x = 42;"
   ↓
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**Caracteristicas clave:**
- Reconoce palabras clave, identificadores, literales, operadores, puntuacion
- Maneja literales de string UTF-8 y literales de runa
- Reporta numeros de linea para mensajes de error
- Pasada unica, sin retroceso

### Fase 2: Analisis Sintactico (Parser)

**Entrada:** Flujo de tokens
**Salida:** Arbol de Sintaxis Abstracta (AST)
**Implementacion:** `src/parser.c`

```
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST: LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**Caracteristicas clave:**
- Parser de descenso recursivo
- Construye representacion en arbol de la estructura del programa
- Maneja precedencia de operadores
- Valida sintaxis (llaves, puntos y coma, etc.)
- Sin analisis semantico aun (se hace en tiempo de ejecucion)

**Precedencia de Operadores (menor a mayor):**
1. Asignacion: `=`
2. OR logico: `||`
3. AND logico: `&&`
4. OR a nivel de bits: `|`
5. XOR a nivel de bits: `^`
6. AND a nivel de bits: `&`
7. Igualdad: `==`, `!=`
8. Comparacion: `<`, `>`, `<=`, `>=`
9. Desplazamientos de bits: `<<`, `>>`
10. Suma/Resta: `+`, `-`
11. Multiplicacion/Division/Modulo: `*`, `/`, `%`
12. Unarios: `!`, `-`, `~`
13. Llamada/Indice/Miembro: `()`, `[]`, `.`

### Fase 3a: Interpretacion (Recorrido de Arbol)

**Entrada:** AST
**Salida:** Ejecucion del programa
**Implementacion:** `src/backends/interpreter/runtime.c`

```
AST: LetStmt { ... }
   ↓
Ejecucion: Evalua nodos AST recursivamente
   ↓
Resultado: Variable x creada con valor 42
```

**Caracteristicas clave:**
- Recorrido directo del AST (interprete de recorrido de arbol)
- Verificacion dinamica de tipos en tiempo de ejecucion
- Almacenamiento de variables basado en entorno

### Fase 3b: Compilacion (hemlockc)

**Entrada:** AST
**Salida:** Ejecutable nativo via generacion de codigo C
**Implementacion:** `src/backends/compiler/`

```
AST: LetStmt { ... }
   ↓
Verificacion de Tipos: Validar tipos en tiempo de compilacion
   ↓
Codegen C: Generar codigo C equivalente
   ↓
GCC: Compilar C a binario nativo
   ↓
Resultado: Ejecutable independiente
```

**Caracteristicas clave:**
- Verificacion de tipos en tiempo de compilacion (habilitada por defecto)
- Generacion de codigo C para portabilidad
- Enlaza contra `libhemlock_runtime.a`
- Ejecucion significativamente mas rapida que el interprete

---

## Backend del Compilador (hemlockc)

El compilador de Hemlock genera codigo C desde el AST, que luego se compila a un ejecutable nativo usando GCC.

### Arquitectura del Compilador

```
src/backends/compiler/
├── main.c              # CLI, parseo de argumentos, orquestacion
├── codegen.c           # Contexto central de generacion de codigo
├── codegen_expr.c      # Generacion de codigo de expresiones
├── codegen_stmt.c      # Generacion de codigo de sentencias
├── codegen_call.c      # Generacion de llamadas a funciones
├── codegen_closure.c   # Implementacion de closures
├── codegen_program.c   # Generacion de programa de nivel superior
├── codegen_module.c    # Manejo de modulos/importaciones
├── type_check.c        # Verificacion de tipos en compilacion
└── type_check.h        # API del verificador de tipos
```

### Verificacion de Tipos

El compilador incluye un sistema unificado de verificacion de tipos que:

1. **Valida tipos en tiempo de compilacion** - Detecta errores de tipo antes de la ejecucion
2. **Soporta codigo dinamico** - Codigo sin tipos tratado como `any` (siempre valido)
3. **Proporciona pistas de optimizacion** - Identifica variables que pueden desempaquetarse

**Banderas de Verificacion de Tipos:**

| Bandera | Descripcion |
|---------|-------------|
| (defecto) | Verificacion de tipos habilitada |
| `--check` | Solo verificar tipos, no compilar |
| `--no-type-check` | Deshabilitar verificacion de tipos |
| `--strict-types` | Advertir sobre tipos `any` implicitos |

**Implementacion del Verificador de Tipos:**

```c
// type_check.h - Estructuras clave
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // Pistas de optimizacion
    // ... entorno de tipos, definiciones, etc.
} TypeCheckContext;

// Punto de entrada principal
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### Generacion de Codigo

La fase de codegen traduce nodos AST a codigo C:

**Mapeo de Expresiones:**
```
Hemlock                 →  C Generado
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  Closure con captura de entorno
```

**Integracion con Runtime:**

El codigo C generado enlaza contra `libhemlock_runtime.a` que proporciona:
- Tipo union etiquetada `HmlValue`
- Gestion de memoria (conteo de referencias)
- Funciones integradas (print, typeof, etc.)
- Primitivas de concurrencia (tareas, canales)
- Soporte FFI

### Optimizacion de Desempaquetado

El verificador de tipos identifica variables que pueden usar tipos C nativos en lugar de `HmlValue` empaquetados:

**Patrones Desempaquetables:**
- Contadores de bucle con tipo entero conocido
- Variables acumuladoras en bucles
- Variables con anotaciones de tipo explicitas (i32, i64, f64, bool)

```hemlock
// El contador de bucle 'i' puede desempaquetarse a int32_t nativo
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    sum = sum + i;
}
```

---

## Diseno Modular del Interprete

El interprete esta dividido en modulos enfocados para mantenibilidad y escalabilidad.

### Responsabilidades de los Modulos

#### 1. Entorno (`environment.c`) - 121 lineas

**Proposito:** Alcance de variables y resolucion de nombres

**Funciones clave:**
- `env_create()` - Crear nuevo entorno con padre opcional
- `env_define()` - Definir nueva variable en alcance actual
- `env_get()` - Buscar variable en alcances actual o padres
- `env_set()` - Actualizar valor de variable existente
- `env_free()` - Liberar entorno y todas las variables

**Diseno:**
- Alcances enlazados (cada entorno tiene puntero al padre)
- HashMap para busqueda rapida de variables
- Soporta alcance lexico para closures

#### 2. Valores (`values.c`) - 394 lineas

**Proposito:** Constructores de valores y gestion de estructuras de datos

**Funciones clave:**
- `value_create_*()` - Constructores para cada tipo de valor
- `value_copy()` - Logica de copia profunda/superficial
- `value_free()` - Limpieza y desasignacion de memoria
- `value_to_string()` - Representacion en string para impresion

**Estructuras de datos:**
- Objetos (arrays de campos dinamicos)
- Arrays (redimensionamiento dinamico)
- Buffers (ptr + longitud + capacidad)
- Closures (funcion + entorno capturado)
- Tareas y Canales (primitivas de concurrencia)

#### 3. Tipos (`types.c`) - 440 lineas

**Proposito:** Sistema de tipos, conversiones y duck typing

**Funciones clave:**
- `type_check()` - Validacion de tipos en tiempo de ejecucion
- `type_convert()` - Conversiones/promociones de tipo implicitas
- `duck_type_check()` - Verificacion de tipos estructural para objetos
- `type_name()` - Obtener nombre de tipo imprimible

**Caracteristicas:**
- Jerarquia de promocion de tipos (i8 → i16 → i32 → i64 → f32 → f64, con i64/u64 + f32 → f64)
- Verificacion de rango para tipos numericos
- Duck typing para definiciones de tipos de objetos
- Valores por defecto de campos opcionales

#### 4. Funciones Integradas (`builtins.c`) - 955 lineas

**Proposito:** Funciones integradas y registro global

**Funciones clave:**
- `register_builtins()` - Registrar todas las funciones y constantes integradas
- Implementaciones de funciones integradas (print, typeof, alloc, free, etc.)
- Funciones de manejo de senales
- Ejecucion de comandos (exec)

**Categorias de funciones integradas:**
- E/S: print, open, read_file, write_file
- Memoria: alloc, free, memset, memcpy, realloc
- Tipos: typeof, assert
- Concurrencia: spawn, join, detach, channel
- Sistema: exec, signal, raise, panic
- FFI: dlopen, dlsym, dlcall, dlclose

#### 5. E/S (`io.c`) - 449 lineas

**Proposito:** E/S de archivos y serializacion JSON

**Funciones clave:**
- Metodos de objeto archivo (read, write, seek, tell, close)
- Serializacion/deserializacion JSON
- Deteccion de referencias circulares

**Caracteristicas:**
- Objeto archivo con propiedades (path, mode, closed)
- E/S de texto consciente de UTF-8
- Soporte de E/S binaria
- Ida y vuelta JSON para objetos y arrays

#### 6. FFI (`ffi.c`) - Interfaz de Funciones Foraneas

**Proposito:** Llamar funciones C desde bibliotecas compartidas

**Funciones clave:**
- `dlopen()` - Cargar biblioteca compartida
- `dlsym()` - Obtener puntero de funcion por nombre
- `dlcall()` - Llamar funcion C con conversion de tipos
- `dlclose()` - Descargar biblioteca

**Caracteristicas:**
- Integracion con libffi para llamadas dinamicas a funciones
- Conversion automatica de tipos (Hemlock ↔ tipos C)
- Soporte para todos los tipos primitivos
- Soporte de punteros y buffers

#### 7. Runtime (`runtime.c`) - 865 lineas

**Proposito:** Evaluacion de expresiones y ejecucion de sentencias

**Funciones clave:**
- `eval_expr()` - Evaluar expresiones (recursivo)
- `eval_stmt()` - Ejecutar sentencias
- Manejo de flujo de control (if, while, for, switch, etc.)
- Manejo de excepciones (try/catch/finally/throw)

**Caracteristicas:**
- Evaluacion recursiva de expresiones
- Evaluacion booleana de cortocircuito
- Deteccion de llamadas a metodos y vinculacion de `self`
- Propagacion de excepciones
- Manejo de break/continue/return

### Beneficios del Diseno Modular

**1. Separacion de Responsabilidades**
- Cada modulo tiene una responsabilidad clara
- Facil encontrar donde se implementan las caracteristicas
- Reduce la carga cognitiva al hacer cambios

**2. Compilaciones Incrementales mas Rapidas**
- Solo los modulos modificados necesitan recompilacion
- Compilacion paralela posible
- Tiempos de iteracion mas cortos durante el desarrollo

**3. Pruebas y Depuracion mas Faciles**
- Los modulos pueden probarse en aislamiento
- Los errores se localizan en subsistemas especificos
- Implementaciones mock posibles para pruebas

**4. Escalabilidad**
- Nuevas caracteristicas pueden agregarse a modulos apropiados
- Los modulos pueden refactorizarse independientemente
- El tamano del codigo por archivo se mantiene manejable

**5. Organizacion del Codigo**
- Agrupacion logica de funcionalidad relacionada
- Grafo de dependencias claro
- Incorporacion mas facil para nuevos contribuidores

---

## Arquitectura del Runtime

### Representacion de Valores

Todos los valores en Hemlock se representan por la estructura `Value` usando una union etiquetada:

```c
typedef struct Value {
    ValueType type;  // Etiqueta de tipo en tiempo de ejecucion
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**Decisiones de diseno:**
- **Union etiquetada** para seguridad de tipos manteniendo flexibilidad
- **Etiquetas de tipo en tiempo de ejecucion** habilitan tipado dinamico con verificacion de tipos
- **Almacenamiento directo de valores** para primitivos (sin empaquetado)
- **Almacenamiento de punteros** para tipos asignados en heap (strings, objetos, arrays)

### Ejemplos de Disposicion en Memoria

**Entero (i32):**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- Tamano total: ~16 bytes (etiqueta de 8 bytes + union de 8 bytes)
- Asignado en pila
- No necesita asignacion en heap

**String:**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // Puntero al heap
}

Heap: "hello\0" (6 bytes, terminado en null UTF-8)
```
- El valor es 16 bytes en la pila
- Los datos del string estan asignados en heap
- Debe liberarse manualmente

**Objeto:**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // Puntero al heap
}

Heap: Object {
    type_name: "Person",
    fields: [
        { name: "name", value: Value{TYPE_STRING, "Alice"} },
        { name: "age", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- Estructura del objeto en heap
- Campos almacenados en array dinamico
- Valores de campos son estructuras Value incrustadas

### Implementacion de Entorno

Las variables se almacenan en cadenas de entorno:

```c
typedef struct Environment {
    HashMap *bindings;           // nombre → Value
    struct Environment *parent;  // Alcance padre lexico
} Environment;
```

**Ejemplo de cadena de alcances:**
```
Alcance Global: { print: <builtin>, args: <array> }
    ↑
Alcance de Funcion: { x: 10, y: 20 }
    ↑
Alcance de Bloque: { i: 0 }
```

**Algoritmo de busqueda:**
1. Verificar el hashmap del entorno actual
2. Si no se encuentra, verificar el entorno padre
3. Repetir hasta encontrar o alcanzar el alcance global
4. Error si no se encuentra en ningun alcance

---

## Implementacion del Sistema de Tipos

### Estrategia de Verificacion de Tipos

Hemlock usa **verificacion de tipos en tiempo de ejecucion** con **anotaciones de tipo opcionales**:

```hemlock
let x = 42;           // Sin verificacion de tipo, infiere i32
let y: u8 = 255;      // Verificacion en tiempo de ejecucion: valor debe caber en u8
let z: i32 = x + y;   // Verificacion en tiempo de ejecucion + promocion de tipos
```

**Flujo de implementacion:**
1. **Inferencia de literales** - Lexer/parser determinan tipo inicial del literal
2. **Verificacion de anotacion de tipo** - Si hay anotacion presente, validar en asignacion
3. **Promocion** - Operaciones binarias promueven a tipo comun
4. **Conversion** - Conversiones explicitas ocurren bajo demanda

### Implementacion de Promocion de Tipos

La promocion de tipos sigue una jerarquia fija con preservacion de precision:

```c
// Logica de promocion simplificada
ValueType promote_types(ValueType a, ValueType b) {
    // f64 siempre gana
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 con i64/u64 promueve a f64 (preservacion de precision)
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // Tipos enteros mas grandes ganan
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**Rangos de tipos:**
- i8: 0
- u8: 1
- i16: 2
- u16: 3
- i32: 4
- u32: 5
- i64: 6
- u64: 7
- f32: 8
- f64: 9

### Implementacion de Duck Typing

La verificacion de tipos de objetos usa comparacion estructural:

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // Verificar todos los campos requeridos
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // Campo faltante
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // Tipo incorrecto
        }
    }

    return true;  // Todos los campos requeridos presentes y tipo correcto
}
```

**El duck typing permite:**
- Campos extra en objetos (ignorados)
- Tipado subestructural (objeto puede tener mas de lo requerido)
- Asignacion de nombre de tipo despues de validacion

---

## Gestion de Memoria

### Estrategia de Asignacion

Hemlock usa **gestion manual de memoria** con dos primitivas de asignacion:

**1. Punteros crudos (`ptr`):**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Sin memoria\n");
        exit(1);
    }
    return ptr;
}
```
- malloc/free directo
- Sin seguimiento
- Responsabilidad del usuario liberar

**2. Buffers (`buffer`):**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- Rastrea tamano y capacidad
- Verificacion de limites en acceso
- Aun requiere free manual

### Tipos Asignados en Heap

**Strings:**
- Array de bytes UTF-8 en heap
- Terminado en null para interoperabilidad con C
- Mutable (puede modificar en lugar)
- Con conteo de referencias (auto-liberado cuando el alcance termina)

**Objetos:**
- Array de campos dinamico
- Nombres y valores de campos en heap
- Con conteo de referencias (auto-liberado cuando el alcance termina)
- Referencias circulares posibles (manejadas con seguimiento de conjunto visitado)

**Arrays:**
- Crecimiento dinamico con duplicacion de capacidad
- Elementos son estructuras Value incrustadas
- Reasignacion automatica al crecer
- Con conteo de referencias (auto-liberado cuando el alcance termina)

**Closures:**
- Captura entorno por referencia
- Entorno asignado en heap
- Entornos de closure se liberan apropiadamente cuando ya no se referencian

---

## Modelo de Concurrencia

### Arquitectura de Hilos

Hemlock usa **hilos 1:1** con hilos POSIX (pthreads):

```
Tarea de Usuario       Hilo del SO         Nucleo de CPU
----------------       -----------         -------------
spawn(f1) ------>  pthread_create --> Nucleo 0
spawn(f2) ------>  pthread_create --> Nucleo 1
spawn(f3) ------>  pthread_create --> Nucleo 2
```

**Caracteristicas clave:**
- Cada `spawn()` crea un nuevo pthread
- El kernel programa hilos a traves de nucleos
- Ejecucion paralela verdadera (sin GIL)
- Multitarea preventiva

### Implementacion de Tareas

```c
typedef struct Task {
    pthread_t thread;        // Handle de hilo del SO
    Value result;            // Valor de retorno
    char *error;             // Mensaje de excepcion (si se lanzo)
    pthread_mutex_t lock;    // Protege el estado
    TaskState state;         // RUNNING, FINISHED, ERROR
} Task;
```

**Ciclo de vida de tareas:**
1. `spawn(func, args)` → Crear Task, iniciar pthread
2. El hilo ejecuta la funcion con argumentos
3. Al retornar: Almacenar resultado, establecer estado a FINISHED
4. En excepcion: Almacenar mensaje de error, establecer estado a ERROR
5. `join(task)` → Esperar al hilo, retornar resultado o lanzar excepcion

### Implementacion de Canales

```c
typedef struct Channel {
    void **buffer;           // Buffer circular de Value*
    size_t capacity;         // Maximo de elementos en buffer
    size_t count;            // Elementos actuales en buffer
    size_t read_index;       // Siguiente posicion de lectura
    size_t write_index;      // Siguiente posicion de escritura
    bool closed;             // Bandera de canal cerrado
    pthread_mutex_t lock;    // Protege el buffer
    pthread_cond_t not_full; // Senal cuando hay espacio disponible
    pthread_cond_t not_empty;// Senal cuando hay datos disponibles
} Channel;
```

**Operacion de envio:**
1. Bloquear mutex
2. Esperar si buffer lleno (cond_wait en not_full)
3. Escribir valor en buffer[write_index]
4. Incrementar write_index (circular)
5. Senalar not_empty
6. Desbloquear mutex

**Operacion de recepcion:**
1. Bloquear mutex
2. Esperar si buffer vacio (cond_wait en not_empty)
3. Leer valor de buffer[read_index]
4. Incrementar read_index (circular)
5. Senalar not_full
6. Desbloquear mutex

**Garantias de sincronizacion:**
- Envio/recepcion seguro entre hilos (protegido por mutex)
- Semantica bloqueante (productor espera si esta lleno, consumidor espera si esta vacio)
- Entrega ordenada (FIFO dentro de un canal)

---

## Planes Futuros

### Completado: Backend del Compilador

El backend del compilador (`hemlockc`) ha sido implementado con:
- Generacion de codigo C desde AST
- Verificacion de tipos en tiempo de compilacion (habilitada por defecto)
- Biblioteca de runtime (`libhemlock_runtime.a`)
- Paridad completa con el interprete (98% de tasa de aprobacion de pruebas)
- Marco de optimizacion de desempaquetado

### Enfoque Actual: Mejoras del Sistema de Tipos

**Mejoras recientes:**
- Sistemas unificados de verificacion de tipos e inferencia de tipos
- Verificacion de tipos en tiempo de compilacion habilitada por defecto
- Bandera `--check` para validacion solo de tipos
- Contexto de tipos pasado a codegen para pistas de optimizacion

### Mejoras Futuras

**Adiciones potenciales:**
- Genericos/plantillas
- Coincidencia de patrones
- Integracion LSP para soporte de IDE consciente de tipos
- Optimizaciones de desempaquetado mas agresivas
- Analisis de escape para asignacion en pila

### Optimizaciones a Largo Plazo

**Mejoras posibles:**
- Cache en linea para llamadas a metodos
- Compilacion JIT para caminos de codigo calientes
- Programador de robo de trabajo para mejor concurrencia
- Optimizacion guiada por perfil

---

## Directrices de Implementacion

### Agregar Nuevas Caracteristicas

Al implementar nuevas caracteristicas, siga estas directrices:

**1. Elegir el modulo correcto:**
- Nuevos tipos de valor → `values.c`
- Conversiones de tipo → `types.c`
- Funciones integradas → `builtins.c`
- Operaciones de E/S → `io.c`
- Flujo de control → `runtime.c`

**2. Actualizar todas las capas:**
- Agregar tipos de nodo AST si es necesario (`ast.h`, `ast.c`)
- Agregar tokens de lexer si es necesario (`lexer.c`)
- Agregar reglas de parser (`parser.c`)
- Implementar comportamiento en runtime (`runtime.c` o modulo apropiado)
- Agregar pruebas (`tests/`)

**3. Mantener consistencia:**
- Seguir el estilo de codigo existente
- Usar convenciones de nomenclatura consistentes
- Documentar API publica en headers
- Mantener mensajes de error claros y consistentes

**4. Probar exhaustivamente:**
- Agregar casos de prueba antes de implementar
- Probar caminos de exito y error
- Probar casos limite
- Verificar que no haya fugas de memoria (valgrind)

### Consideraciones de Rendimiento

**Cuellos de botella actuales:**
- Busquedas en HashMap para acceso a variables
- Llamadas a funciones recursivas (sin TCO)
- Concatenacion de strings (asigna nuevo string cada vez)
- Sobrecarga de verificacion de tipos en cada operacion

**Oportunidades de optimizacion:**
- Cachear ubicaciones de variables (cache en linea)
- Optimizacion de llamada de cola
- Constructor de strings para concatenacion
- Inferencia de tipos para omitir verificaciones en tiempo de ejecucion

### Consejos de Depuracion

**Herramientas utiles:**
- `valgrind` - Deteccion de fugas de memoria
- `gdb` - Depurar crashes
- Bandera `-g` - Simbolos de depuracion
- Depuracion con `printf` - Simple pero efectivo

**Problemas comunes:**
- Segfault → Desreferencia de puntero nulo (verificar valores de retorno)
- Fuga de memoria → Llamada a free() faltante (verificar caminos de value_free)
- Error de tipo → Verificar logica de type_convert() y type_check()
- Crash en hilos → Condicion de carrera (verificar uso de mutex)

---

## Conclusion

La implementacion de Hemlock prioriza:
- **Modularidad** - Separacion limpia de responsabilidades
- **Simplicidad** - Implementacion directa
- **Explicitud** - Sin magia oculta
- **Mantenibilidad** - Facil de entender y modificar

El actual interprete de recorrido de arbol es intencionalmente simple para facilitar el desarrollo rapido de caracteristicas y la experimentacion. El futuro backend del compilador mejorara el rendimiento manteniendo la misma semantica.
