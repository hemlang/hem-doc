# Guía de Pruebas para Hemlock

Esta guía explica la filosofía de pruebas de Hemlock, cómo escribir pruebas y cómo ejecutar la suite de pruebas.

---

## Tabla de Contenidos

- [Filosofía de Pruebas](#filosofía-de-pruebas)
- [Estructura de la Suite de Pruebas](#estructura-de-la-suite-de-pruebas)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Escribir Pruebas](#escribir-pruebas)
- [Categorías de Pruebas](#categorías-de-pruebas)
- [Pruebas de Fugas de Memoria](#pruebas-de-fugas-de-memoria)
- [Integración Continua](#integración-continua)
- [Mejores Prácticas](#mejores-prácticas)

---

## Filosofía de Pruebas

### Principios Fundamentales

**1. Desarrollo Guiado por Pruebas (TDD)**

Escribe pruebas **antes** de implementar funcionalidades:

```
1. Write a failing test
2. Implement the feature
3. Run the test (should pass)
4. Refactor if needed
5. Repeat
```

**Beneficios:**
- Asegura que las funcionalidades realmente funcionan
- Previene regresiones
- Documenta el comportamiento esperado
- Hace la refactorización más segura

**2. Cobertura Integral**

Prueba tanto los casos de éxito como los de fallo:

```hemlock
// Success case
let x: u8 = 255;  // Should work

// Failure case
let y: u8 = 256;  // Should error
```

**3. Probar Temprano y Frecuentemente**

Ejecuta las pruebas:
- Antes de hacer commit del código
- Después de hacer cambios
- Antes de enviar pull requests
- Durante la revisión de código

**Regla:** Todas las pruebas deben pasar antes de fusionar.

### Qué Probar

**Siempre prueba:**
- Funcionalidad básica (camino feliz)
- Condiciones de error (camino triste)
- Casos límite (condiciones de frontera)
- Verificación de tipos y conversiones
- Gestión de memoria (sin fugas)
- Concurrencia y condiciones de carrera

**Ejemplo de cobertura de pruebas:**
```hemlock
// Feature: String.substr(start, length)

// Happy path
print("hello".substr(0, 5));  // "hello"

// Edge cases
print("hello".substr(0, 0));  // "" (empty)
print("hello".substr(5, 0));  // "" (at end)
print("hello".substr(2, 100)); // "llo" (past end)

// Error cases
// "hello".substr(-1, 5);  // Error: negative index
// "hello".substr(0, -1);  // Error: negative length
```

---

## Estructura de la Suite de Pruebas

### Organización de Directorios

```
tests/
├── run_tests.sh          # Main test runner script
├── primitives/           # Type system tests
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # Type conversion tests
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # Pointer/buffer tests
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # String operation tests
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # Control flow tests
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # Function and closure tests
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # Object tests
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # Array operation tests
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # Loop tests
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # Error handling tests
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # File I/O tests
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # Concurrency tests
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # FFI tests
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # Signal handling tests
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # Command-line args tests
    └── basic.hml
```

### Nomenclatura de Archivos de Prueba

**Convenciones:**
- Usa nombres descriptivos: `method_chaining.hml` no `test1.hml`
- Agrupa pruebas relacionadas: `string_substr.hml`, `string_slice.hml`
- Un área de funcionalidad por archivo
- Mantén los archivos enfocados y pequeños

---

## Ejecutar Pruebas

### Ejecutar Todas las Pruebas

```bash
# From hemlock root directory
make test

# Or directly
./tests/run_tests.sh
```

**Salida:**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### Ejecutar Categoría Específica

```bash
# Run only string tests
./tests/run_tests.sh tests/strings/

# Run only one test file
./tests/run_tests.sh tests/strings/concat.hml

# Run multiple categories
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Ejecutar con Valgrind (Verificación de Fugas de Memoria)

```bash
# Check single test for leaks
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# Check all tests (slow!)
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### Depurar Pruebas Fallidas

```bash
# Run with verbose output
./hemlock tests/failing_test.hml

# Run with gdb
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # if it crashes
```

---

## Escribir Pruebas

### Formato de Archivos de Prueba

Los archivos de prueba son simplemente programas Hemlock con salida esperada:

**Ejemplo: tests/primitives/integers.hml**
```hemlock
// Test basic integer literals
let x = 42;
print(x);  // Expect: 42

let y: i32 = 100;
print(y);  // Expect: 100

// Test arithmetic
let sum = x + y;
print(sum);  // Expect: 142

// Test type inference
let small = 10;
print(typeof(small));  // Expect: i32

let large = 5000000000;
print(typeof(large));  // Expect: i64
```

**Cómo funcionan las pruebas:**
1. El ejecutor de pruebas ejecuta el archivo .hml
2. Captura la salida stdout
3. Compara con la salida esperada (de comentarios o archivo .out separado)
4. Reporta éxito/fallo

### Métodos de Salida Esperada

**Método 1: Comentarios en línea (recomendado para pruebas simples)**

```hemlock
print("hello");  // Expect: hello
print(42);       // Expect: 42
```

El ejecutor de pruebas analiza los comentarios `// Expect: ...`.

**Método 2: Archivo .out separado**

Crea `test_name.hml.out` con la salida esperada:

**test_name.hml:**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**test_name.hml.out:**
```
line 1
line 2
line 3
```

### Probar Casos de Error

Las pruebas de error deben hacer que el programa termine con estado distinto de cero:

**Ejemplo: tests/primitives/range_error.hml**
```hemlock
// This should fail with a type error
let x: u8 = 256;  // Out of range for u8
```

**Comportamiento esperado:**
- El programa termina con estado distinto de cero
- Imprime mensaje de error a stderr

**Manejo del ejecutor de pruebas:**
- Las pruebas que esperan errores deben estar en archivos separados
- Usa convención de nombres: `*_error.hml` o `*_fail.hml`
- Documenta el error esperado en comentarios

### Probar Casos de Éxito

**Ejemplo: tests/strings/methods.hml**
```hemlock
// Test substr
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Expect: world

// Test find
let pos = s.find("world");
print(pos);  // Expect: 6

// Test contains
let has = s.contains("lo");
print(has);  // Expect: true

// Test trim
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Expect: hello
```

### Probar Casos Límite

**Ejemplo: tests/arrays/edge_cases.hml**
```hemlock
// Empty array
let empty = [];
print(empty.length);  // Expect: 0

// Single element
let single = [42];
print(single[0]);  // Expect: 42

// Negative index (should error in separate test file)
// print(single[-1]);  // Error

// Past-end index (should error)
// print(single[100]);  // Error

// Boundary conditions
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Expect: [] (empty)
print(arr.slice(3, 3));  // Expect: [] (empty)
print(arr.slice(1, 2));  // Expect: [2]
```

### Probar Sistema de Tipos

**Ejemplo: tests/conversions/promotion.hml**
```hemlock
// Test type promotion in binary operations

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Expect: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Expect: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Expect: i32
```

### Probar Concurrencia

**Ejemplo: tests/async/basic.hml**
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

// Spawn tasks
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// Join and print results
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Expect: 45
print(r2);  // Expect: 190
```

### Probar Excepciones

**Ejemplo: tests/exceptions/try_catch.hml**
```hemlock
// Test basic try/catch
try {
    throw "error message";
} catch (e) {
    print("Caught: " + e);  // Expect: Caught: error message
}

// Test finally
let executed = false;
try {
    print("try");  // Expect: try
} finally {
    executed = true;
    print("finally");  // Expect: finally
}

// Test exception propagation
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // Expect: failure
}
```

---

## Categorías de Pruebas

### Pruebas de Primitivos

**Qué probar:**
- Tipos enteros (i8, i16, i32, i64, u8, u16, u32, u64)
- Tipos de punto flotante (f32, f64)
- Tipo booleano
- Tipo string
- Tipo rune
- Tipo null

**Áreas de ejemplo:**
- Sintaxis de literales
- Inferencia de tipos
- Verificación de rangos
- Comportamiento de desbordamiento
- Anotaciones de tipo

### Pruebas de Conversión

**Qué probar:**
- Promoción implícita de tipos
- Conversión explícita de tipos
- Conversiones con pérdida (deben dar error)
- Promoción de tipos en operaciones
- Comparaciones entre tipos

### Pruebas de Memoria

**Qué probar:**
- Corrección de alloc/free
- Creación y acceso a Buffer
- Verificación de límites en buffers
- memset, memcpy, realloc
- Detección de fugas de memoria (valgrind)

### Pruebas de Strings

**Qué probar:**
- Concatenación
- Los 18 métodos de string
- Manejo de UTF-8
- Indexación de runes
- Concatenación de string + rune
- Casos límite (strings vacíos, un solo carácter, etc.)

### Pruebas de Flujo de Control

**Qué probar:**
- if/else/else if
- Bucles while
- Bucles for
- Sentencias switch
- break/continue
- Sentencias return

### Pruebas de Funciones

**Qué probar:**
- Definición y llamada de funciones
- Paso de parámetros
- Valores de retorno
- Recursión
- Closures y captura
- Funciones de primera clase
- Funciones anónimas

### Pruebas de Objetos

**Qué probar:**
- Literales de objeto
- Acceso y asignación de campos
- Métodos y binding de self
- Duck typing
- Campos opcionales
- Serialización/deserialización JSON
- Detección de referencias circulares

### Pruebas de Arrays

**Qué probar:**
- Creación de arrays
- Indexación y asignación
- Los 15 métodos de array
- Tipos mezclados
- Redimensionamiento dinámico
- Casos límite (vacío, un solo elemento)

### Pruebas de Excepciones

**Qué probar:**
- try/catch/finally
- Sentencia throw
- Propagación de excepciones
- try/catch anidados
- Return en try/catch/finally
- Excepciones no capturadas

### Pruebas de E/S

**Qué probar:**
- Modos de apertura de archivos
- Operaciones de lectura/escritura
- Seek/tell
- Propiedades de archivos
- Manejo de errores (archivos faltantes, etc.)
- Limpieza de recursos

### Pruebas Asíncronas

**Qué probar:**
- spawn/join/detach
- send/recv de Channel
- Propagación de excepciones en tareas
- Múltiples tareas concurrentes
- Comportamiento de bloqueo de canales

### Pruebas de FFI

**Qué probar:**
- dlopen/dlclose
- dlsym
- dlcall con varios tipos
- Conversión de tipos
- Manejo de errores

---

## Pruebas de Fugas de Memoria

### Usar Valgrind

**Uso básico:**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**Ejemplo de salida (sin fugas):**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**Ejemplo de salida (con fuga):**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### Fuentes Comunes de Fugas

**1. Llamadas free() faltantes:**
```c
// BAD
char *str = malloc(100);
// ... use str
// Forgot to free!

// GOOD
char *str = malloc(100);
// ... use str
free(str);
```

**2. Punteros perdidos:**
```c
// BAD
char *ptr = malloc(100);
ptr = malloc(200);  // Lost reference to first allocation!

// GOOD
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. Caminos de excepción:**
```c
// BAD
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // Leak!
    }
    free(data);
}

// GOOD
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### Fugas Aceptables Conocidas

Algunas pequeñas "fugas" son asignaciones intencionales de inicio:

**Funciones incorporadas globales:**
```hemlock
// Built-in functions, FFI types, and constants are allocated at startup
// and not freed at exit (typically ~200 bytes)
```

Estas no son fugas verdaderas - son asignaciones únicas que persisten durante la vida del programa y son limpiadas por el SO al salir.

---

## Integración Continua

### GitHub Actions (Futuro)

Una vez que el CI esté configurado, todas las pruebas se ejecutarán automáticamente en:
- Push a la rama main
- Creación/actualización de pull request
- Ejecuciones programadas diarias

**Flujo de trabajo de CI:**
1. Compilar Hemlock
2. Ejecutar suite de pruebas
3. Verificar fugas de memoria (valgrind)
4. Reportar resultados en el PR

### Verificaciones Pre-Commit

Antes de hacer commit, ejecuta:

```bash
# Build fresh
make clean && make

# Run all tests
make test

# Check a few tests for leaks
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## Mejores Prácticas

### Hacer

**Escribe pruebas primero (TDD)**
```bash
1. Create tests/feature/new_feature.hml
2. Implement feature in src/
3. Run tests until they pass
```

**Prueba tanto éxito como fallo**
```hemlock
// Success: tests/feature/success.hml
let result = do_thing();
print(result);  // Expect: expected value

// Failure: tests/feature/failure.hml
do_invalid_thing();  // Should error
```

**Usa nombres de prueba descriptivos**
```
Good: tests/strings/substr_utf8_boundary.hml
Bad:  tests/test1.hml
```

**Mantén las pruebas enfocadas**
- Un área de funcionalidad por archivo
- Configuración y aserciones claras
- Código mínimo

**Agrega comentarios explicando pruebas complicadas**
```hemlock
// Test that closure captures outer variable by reference
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // Modify after closure creation
    return f();  // Should return 20, not 10
}
```

**Prueba casos límite**
- Entradas vacías
- Valores null
- Valores de frontera (min/max)
- Entradas grandes
- Valores negativos

### No Hacer

**No omitas pruebas**
- Todas las pruebas deben pasar antes de fusionar
- No comentes pruebas que fallan
- Arregla el error o elimina la funcionalidad

**No escribas pruebas que dependan unas de otras**
```hemlock
// BAD: test2.hml depends on test1.hml output
// Tests should be independent
```

**No uses valores aleatorios en pruebas**
```hemlock
// BAD: Non-deterministic
let x = random();
print(x);  // Can't predict output

// GOOD: Deterministic
let x = 42;
print(x);  // Expect: 42
```

**No pruebes detalles de implementación**
```hemlock
// BAD: Testing internal structure
let obj = { x: 10 };
// Don't check internal field order, capacity, etc.

// GOOD: Testing behavior
print(obj.x);  // Expect: 10
```

**No ignores fugas de memoria**
- Todas las pruebas deben pasar valgrind sin errores
- Documenta fugas conocidas/aceptables
- Arregla las fugas antes de fusionar

### Mantenimiento de Pruebas

**Cuándo actualizar pruebas:**
- El comportamiento de la funcionalidad cambia
- Las correcciones de errores requieren nuevos casos de prueba
- Se descubren casos límite
- Mejoras de rendimiento

**Cuándo eliminar pruebas:**
- La funcionalidad se elimina del lenguaje
- La prueba duplica cobertura existente
- La prueba era incorrecta

**Refactorizar pruebas:**
- Agrupa pruebas relacionadas
- Extrae código de configuración común
- Usa nombres consistentes
- Mantén las pruebas simples y legibles

---

## Sesión de Prueba de Ejemplo

Aquí hay un ejemplo completo de agregar una funcionalidad con pruebas:

### Funcionalidad: Agregar método `array.first()`

**1. Escribe la prueba primero:**

```bash
# Create test file
cat > tests/arrays/first_method.hml << 'EOF'
// Test array.first() method

// Basic case
let arr = [1, 2, 3];
print(arr.first());  // Expect: 1

// Single element
let single = [42];
print(single.first());  // Expect: 42

// Empty array (should error - separate test file)
// let empty = [];
// print(empty.first());  // Error
EOF
```

**2. Ejecuta la prueba (debe fallar):**

```bash
./hemlock tests/arrays/first_method.hml
# Error: Method 'first' not found on array
```

**3. Implementa la funcionalidad:**

Edita `src/interpreter/builtins.c`:

```c
// Add array_first method
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Error: Cannot get first element of empty array\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// Register in array method table
// ... add to array method registration
```

**4. Ejecuta la prueba (debe pasar):**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# Success!
```

**5. Verifica fugas de memoria:**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. Ejecuta la suite completa de pruebas:**

```bash
make test
# Total: 252 tests (251 + new one)
# Passed: 252
# Failed: 0
```

**7. Commit:**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## Resumen

**Recuerda:**
- Escribe pruebas primero (TDD)
- Prueba casos de éxito y fallo
- Ejecuta todas las pruebas antes de hacer commit
- Verifica fugas de memoria
- Documenta problemas conocidos
- Mantén las pruebas simples y enfocadas

**¡La calidad de las pruebas es tan importante como la calidad del código!**
