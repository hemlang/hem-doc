# Contribuir a Hemlock

Gracias por tu interés en contribuir a Hemlock. Esta guía te ayudará a entender cómo contribuir de manera efectiva mientras mantienes la filosofía de diseño del lenguaje y la calidad del código.

---

## Tabla de Contenidos

- [Antes de Comenzar](#antes-de-comenzar)
- [Flujo de Trabajo de Contribución](#flujo-de-trabajo-de-contribución)
- [Guía de Estilo de Código](#guía-de-estilo-de-código)
- [Qué Contribuir](#qué-contribuir)
- [Qué NO Contribuir](#qué-no-contribuir)
- [Patrones Comunes](#patrones-comunes)
- [Agregar Nuevas Funcionalidades](#agregar-nuevas-funcionalidades)
- [Proceso de Revisión de Código](#proceso-de-revisión-de-código)

---

## Antes de Comenzar

### Lectura Requerida

Antes de contribuir, por favor lee estos documentos en orden:

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Comprende los principios fundamentales de Hemlock
2. **`/home/user/hemlock/docs/design/implementation.md`** - Aprende la estructura del código base
3. **`/home/user/hemlock/docs/contributing/testing.md`** - Comprende los requisitos de pruebas
4. **Este documento** - Aprende las guías de contribución

### Prerrequisitos

**Conocimiento requerido:**
- Programación en C (punteros, gestión de memoria, estructuras)
- Fundamentos de compiladores/intérpretes (análisis léxico, sintáctico, AST)
- Flujo de trabajo con Git y GitHub
- Línea de comandos Unix/Linux

**Herramientas requeridas:**
- Compilador GCC o Clang
- Sistema de compilación Make
- Control de versiones Git
- Valgrind (para detección de fugas de memoria)
- Editor de texto básico o IDE

### Canales de Comunicación

**Dónde hacer preguntas:**
- GitHub Issues - Reportes de errores y solicitudes de funcionalidades
- GitHub Discussions - Preguntas generales y discusiones de diseño
- Comentarios en Pull Request - Retroalimentación específica de código

---

## Flujo de Trabajo de Contribución

### 1. Encontrar o Crear un Issue

**Antes de escribir código:**
- Verifica si existe un issue para tu contribución
- Si no existe, crea uno describiendo lo que quieres hacer
- Espera retroalimentación de los mantenedores antes de comenzar cambios grandes
- Las correcciones pequeñas de errores pueden omitir este paso

**Las buenas descripciones de issues incluyen:**
- Declaración del problema (qué está roto o falta)
- Solución propuesta (cómo planeas solucionarlo)
- Ejemplos (fragmentos de código mostrando el problema)
- Justificación (por qué este cambio se alinea con la filosofía de Hemlock)

### 2. Fork y Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/hemlock.git
cd hemlock
git checkout -b feature/your-feature-name
```

### 3. Hacer tus Cambios

Sigue estas directrices:
- Escribe las pruebas primero (enfoque TDD)
- Implementa la funcionalidad
- Asegúrate de que todas las pruebas pasen
- Verifica fugas de memoria
- Actualiza la documentación

### 4. Probar tus Cambios

```bash
# Run the full test suite
make test

# Run specific test category
./tests/run_tests.sh tests/category/

# Check for memory leaks
valgrind ./hemlock tests/your_test.hml

# Build and test
make clean && make && make test
```

### 5. Hacer Commit de tus Cambios

**Buenos mensajes de commit:**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**Formato del mensaje de commit:**
- Primera línea: Resumen breve (máximo 50 caracteres)
- Línea en blanco
- Explicación detallada (ajustar a 72 caracteres)
- Referenciar números de issue

### 6. Enviar un Pull Request

**Antes de enviar:**
- Haz rebase sobre la última rama main
- Asegúrate de que todas las pruebas pasen
- Ejecuta valgrind para verificar fugas
- Actualiza CLAUDE.md si agregas funcionalidades visibles al usuario

**La descripción del pull request debe incluir:**
- Qué problema resuelve
- Cómo lo resuelve
- Cambios incompatibles (si los hay)
- Ejemplos de nueva sintaxis o comportamiento
- Resumen de cobertura de pruebas

---

## Guía de Estilo de Código

### Estilo de Código C

**Formato:**
```c
// Indent with 4 spaces (no tabs)
// K&R brace style for functions
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // Brace on same line for control structures
        do_something();
    }
}

// Line length: 100 characters max
// Use spaces around operators
int result = (a + b) * c;

// Pointer asterisk with type
char *string;   // Good
char* string;   // Avoid
char * string;  // Avoid
```

**Convenciones de nombres:**
```c
// Functions: lowercase_with_underscores
void eval_expression(ASTNode *node);

// Types: PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// Constants: UPPERCASE_WITH_UNDERSCORES
#define MAX_BUFFER_SIZE 4096

// Variables: lowercase_with_underscores
int item_count;
Value *current_value;

// Enums: TYPE_PREFIX_NAME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**Comentarios:**
```c
// Single-line comments for brief explanations
// Use complete sentences with proper capitalization

/*
 * Multi-line comments for longer explanations
 * Align asterisks for readability
 */

/**
 * Function documentation comment
 * @param node - AST node to evaluate
 * @return Evaluated value
 */
Value eval_expr(ASTNode *node);
```

**Manejo de errores:**
```c
// Check all malloc calls
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Error: Out of memory\n");
    exit(1);
}

// Provide context in error messages
if (file == NULL) {
    fprintf(stderr, "Error: Failed to open '%s': %s\n",
            filename, strerror(errno));
    exit(1);
}

// Use meaningful error messages
// Bad: "Error: Invalid value"
// Good: "Error: Expected integer, got string"
```

**Gestión de memoria:**
```c
// Always free what you allocate
Value *val = value_create_i32(42);
// ... use val
value_free(val);

// Set pointers to NULL after freeing (prevents double-free)
free(ptr);
ptr = NULL;

// Document ownership in comments
// This function takes ownership of 'value' and will free it
void store_value(Value *value);

// This function does NOT take ownership (caller must free)
Value *get_value(void);
```

### Organización del Código

**Estructura de archivos:**
```c
// 1. Includes (system headers first, then local)
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. Constants and macros
#define INITIAL_CAPACITY 16

// 3. Type definitions
typedef struct Foo Foo;

// 4. Static function declarations (internal helpers)
static void helper_function(void);

// 5. Public function implementations
void public_api_function(void)
{
    // Implementation
}

// 6. Static function implementations
static void helper_function(void)
{
    // Implementation
}
```

**Archivos de cabecera:**
```c
// Use header guards
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// Forward declarations
typedef struct Value Value;

// Public API only in headers
void public_function(Value *val);

// Document parameters and return values
/**
 * Evaluates an expression AST node
 * @param node - The AST node to evaluate
 * @param env - The current environment
 * @return The result value
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## Qué Contribuir

### Contribuciones Recomendadas

**Correcciones de errores:**
- Fugas de memoria
- Fallos de segmentación
- Comportamiento incorrecto
- Mejoras en mensajes de error

**Documentación:**
- Comentarios de código
- Documentación de API
- Guías de usuario y tutoriales
- Programas de ejemplo
- Documentación de casos de prueba

**Pruebas:**
- Casos de prueba adicionales para funcionalidades existentes
- Cobertura de casos límite
- Pruebas de regresión para errores corregidos
- Benchmarks de rendimiento

**Adiciones de funcionalidades pequeñas:**
- Nuevas funciones incorporadas (si encajan con la filosofía)
- Métodos de string/array
- Funciones utilitarias
- Mejoras en manejo de errores

**Mejoras de rendimiento:**
- Algoritmos más rápidos (sin cambiar la semántica)
- Reducción del uso de memoria
- Suite de benchmarks
- Herramientas de profiling

**Herramientas:**
- Resaltado de sintaxis para editores
- Protocolo de servidor de lenguaje (LSP)
- Integración con depurador
- Mejoras del sistema de compilación

### Discutir Primero

**Funcionalidades mayores:**
- Nuevas construcciones del lenguaje
- Cambios en el sistema de tipos
- Adiciones de sintaxis
- Primitivas de concurrencia

**Cómo discutir:**
1. Abre un issue o discusión en GitHub
2. Describe la funcionalidad y justificación
3. Muestra código de ejemplo
4. Explica cómo encaja con la filosofía de Hemlock
5. Espera retroalimentación de los mantenedores
6. Itera en el diseño antes de implementar

---

## Qué NO Contribuir

### Contribuciones Desaconsejadas

**No agregues funcionalidades que:**
- Ocultan complejidad al usuario
- Hacen el comportamiento implícito o mágico
- Rompen la semántica o sintaxis existente
- Agregan recolección de basura o gestión automática de memoria
- Violan el principio de "explícito sobre implícito"

**Ejemplos de contribuciones rechazadas:**

**1. Inserción automática de punto y coma**
```hemlock
// BAD: This would be rejected
let x = 5  // No semicolon
let y = 10 // No semicolon
```
Por qué: Hace la sintaxis ambigua, oculta errores

**2. RAII/destructores**
```hemlock
// BAD: This would be rejected
let f = open("file.txt");
// File automatically closed at end of scope
```
Por qué: Oculta cuándo se liberan los recursos, no es explícito

**3. Coerción implícita de tipos que pierde datos**
```hemlock
// BAD: This would be rejected
let x: i32 = 3.14;  // Silently truncates to 3
```
Por qué: La pérdida de datos debe ser explícita, no silenciosa

**4. Recolección de basura**
```c
// BAD: This would be rejected
void *gc_malloc(size_t size) {
    // Track allocation for automatic cleanup
}
```
Por qué: Oculta la gestión de memoria, rendimiento impredecible

**5. Sistema de macros complejo**
```hemlock
// BAD: This would be rejected
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
Por qué: Demasiada magia, hace el código difícil de razonar

### Razones Comunes de Rechazo

**"Esto es demasiado implícito"**
- Solución: Haz el comportamiento explícito y documéntalo

**"Esto oculta complejidad"**
- Solución: Expone la complejidad pero hazla ergonómica

**"Esto rompe código existente"**
- Solución: Encuentra una alternativa no disruptiva o discute versionado

**"Esto no encaja con la filosofía de Hemlock"**
- Solución: Relee philosophy.md y reconsidera el enfoque

---

## Patrones Comunes

### Patrón de Manejo de Errores

```c
// Use this pattern for recoverable errors in Hemlock code
Value *divide(Value *a, Value *b)
{
    // Check preconditions
    if (b->type != TYPE_I32) {
        // Return error value or throw exception
        return create_error("Expected integer divisor");
    }

    if (b->i32_value == 0) {
        return create_error("Division by zero");
    }

    // Perform operation
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### Patrón de Gestión de Memoria

```c
// Pattern: Allocate, use, free
void process_data(void)
{
    // Allocate
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // Use
    if (buf && str) {
        // ... do work
    }

    // Free (in reverse order of allocation)
    free(str);
    free_buffer(buf);
}
```

### Patrón de Creación de Valores

```c
// Create values using constructors
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### Patrón de Verificación de Tipos

```c
// Check types before operations
Value *add_values(Value *a, Value *b)
{
    // Type checking
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Type mismatch");
    }

    // Safe to proceed
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### Patrón de Construcción de Strings

```c
// Build strings efficiently
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Error: %s (line %d)", detail, line_number);
}
```

---

## Agregar Nuevas Funcionalidades

### Lista de Verificación para Adición de Funcionalidades

Cuando agregues una nueva funcionalidad, sigue estos pasos:

#### 1. Fase de Diseño

- [ ] Lee philosophy.md para asegurar alineación
- [ ] Crea un issue en GitHub describiendo la funcionalidad
- [ ] Obtén aprobación de los mantenedores para el diseño
- [ ] Escribe especificación (sintaxis, semántica, ejemplos)
- [ ] Considera casos límite y condiciones de error

#### 2. Fase de Implementación

**Si agregas una construcción del lenguaje:**

- [ ] Agrega tipo de token a `lexer.h` (si es necesario)
- [ ] Agrega regla del lexer en `lexer.c` (si es necesario)
- [ ] Agrega tipo de nodo AST en `ast.h`
- [ ] Agrega constructor AST en `ast.c`
- [ ] Agrega regla del parser en `parser.c`
- [ ] Agrega comportamiento en tiempo de ejecución en `runtime.c` o módulo apropiado
- [ ] Maneja limpieza en funciones free del AST

**Si agregas una función incorporada:**

- [ ] Agrega implementación de la función en `builtins.c`
- [ ] Registra la función en `register_builtins()`
- [ ] Maneja todas las combinaciones de tipos de parámetros
- [ ] Retorna valores de error apropiados
- [ ] Documenta parámetros y tipo de retorno

**Si agregas un tipo de valor:**

- [ ] Agrega enum de tipo en `values.h`
- [ ] Agrega campo a la unión Value
- [ ] Agrega constructor en `values.c`
- [ ] Agrega a `value_free()` para limpieza
- [ ] Agrega a `value_copy()` para copiar
- [ ] Agrega a `value_to_string()` para imprimir
- [ ] Agrega reglas de promoción de tipos si es numérico

#### 3. Fase de Pruebas

- [ ] Escribe casos de prueba (ver testing.md)
- [ ] Prueba casos exitosos
- [ ] Prueba casos de error
- [ ] Prueba casos límite
- [ ] Ejecuta suite completa de pruebas (`make test`)
- [ ] Verifica fugas de memoria con valgrind
- [ ] Prueba en múltiples plataformas (si es posible)

#### 4. Fase de Documentación

- [ ] Actualiza CLAUDE.md con documentación visible al usuario
- [ ] Agrega comentarios de código explicando la implementación
- [ ] Crea ejemplos en `examples/`
- [ ] Actualiza archivos relevantes en docs/
- [ ] Documenta cualquier cambio incompatible

#### 5. Fase de Envío

- [ ] Limpia código de depuración y comentarios
- [ ] Verifica cumplimiento del estilo de código
- [ ] Haz rebase sobre la última main
- [ ] Crea pull request con descripción detallada
- [ ] Responde a la retroalimentación de revisión de código

### Ejemplo: Agregar un Nuevo Operador

Recorramos el proceso de agregar el operador módulo `%` como ejemplo:

**1. Lexer (lexer.c):**
```c
// Add to switch statement in get_next_token()
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. Cabecera del Lexer (lexer.h):**
```c
typedef enum {
    // ... existing tokens
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h):**
```c
typedef enum {
    // ... existing operators
    OP_MOD,
    // ...
} BinaryOp;
```

**4. Parser (parser.c):**
```c
// Add to parse_multiplicative() or appropriate precedence level
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. Runtime (runtime.c):**
```c
// Add to eval_binary_op()
case OP_MOD:
    // Type checking
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Error: Modulo by zero\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... handle other type combinations
    break;
```

**6. Pruebas (tests/operators/modulo.hml):**
```hemlock
// Basic modulo
print(10 % 3);  // Expect: 2

// Negative modulo
print(-10 % 3); // Expect: -1

// Error case (should fail)
// print(10 % 0);  // Division by zero
```

**7. Documentación (CLAUDE.md):**
```markdown
### Arithmetic Operators
- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo (remainder)
```

---

## Proceso de Revisión de Código

### Qué Buscan los Revisores

**1. Corrección**
- ¿El código hace lo que dice que hace?
- ¿Se manejan los casos límite?
- ¿Hay fugas de memoria?
- ¿Se manejan los errores correctamente?

**2. Alineación con la Filosofía**
- ¿Encaja esto con los principios de diseño de Hemlock?
- ¿Es explícito o implícito?
- ¿Oculta complejidad?

**3. Calidad de Código**
- ¿Es el código legible y mantenible?
- ¿Son descriptivos los nombres de variables?
- ¿Tienen las funciones un tamaño razonable?
- ¿Hay documentación adecuada?

**4. Pruebas**
- ¿Hay suficientes casos de prueba?
- ¿Las pruebas cubren caminos de éxito y fallo?
- ¿Se prueban los casos límite?

**5. Documentación**
- ¿Se actualizó la documentación visible al usuario?
- ¿Son claros los comentarios de código?
- ¿Se proporcionan ejemplos?

### Responder a la Retroalimentación

**Sí:**
- Agradece a los revisores por su tiempo
- Haz preguntas aclaratorias si no entiendes
- Explica tu razonamiento si no estás de acuerdo
- Haz los cambios solicitados prontamente
- Actualiza la descripción del PR si el alcance cambia

**No:**
- Tomes las críticas personalmente
- Discutas defensivamente
- Ignores la retroalimentación
- Hagas force-push sobre comentarios de revisión (a menos que hagas rebase)
- Agregues cambios no relacionados al PR

### Lograr que tu PR sea Fusionado

**Requisitos para fusión:**
- [ ] Todas las pruebas pasan
- [ ] Sin fugas de memoria (valgrind limpio)
- [ ] Aprobación de revisión de código del mantenedor
- [ ] Documentación actualizada
- [ ] Sigue las guías de estilo de código
- [ ] Se alinea con la filosofía de Hemlock

**Cronograma:**
- PRs pequeños (correcciones de errores): Usualmente revisados en unos días
- PRs medianos (nuevas funcionalidades): Puede tomar 1-2 semanas
- PRs grandes (cambios mayores): Requiere discusión extensa

---

## Recursos Adicionales

### Recursos de Aprendizaje

**Entender intérpretes:**
- "Crafting Interpreters" por Robert Nystrom
- "Writing An Interpreter In Go" por Thorsten Ball
- "Modern Compiler Implementation in C" por Andrew Appel

**Programación en C:**
- "The C Programming Language" por K&R
- "Expert C Programming" por Peter van der Linden
- "C Interfaces and Implementations" por David Hanson

**Gestión de memoria:**
- Documentación de Valgrind
- "Understanding and Using C Pointers" por Richard Reese

### Comandos Útiles

```bash
# Build with debug symbols
make clean && make CFLAGS="-g -O0"

# Run with valgrind
valgrind --leak-check=full ./hemlock script.hml

# Run specific test category
./tests/run_tests.sh tests/strings/

# Generate tags file for code navigation
ctags -R .

# Find all TODOs and FIXMEs
grep -rn "TODO\|FIXME" src/ include/
```

---

## ¿Preguntas?

Si tienes preguntas sobre contribuir:

1. Revisa la documentación en `docs/`
2. Busca en issues existentes de GitHub
3. Pregunta en GitHub Discussions
4. Abre un nuevo issue con tu pregunta

**¡Gracias por contribuir a Hemlock!**
