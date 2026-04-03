# Documentacion de Hemlock

Bienvenido a la documentacion del lenguaje de programacion Hemlock!

> Un lenguaje pequeno e inseguro para escribir cosas inseguras de manera segura.

## Tabla de Contenidos

### Primeros Pasos
- [Instalacion](getting-started/installation.md) - Compilar e instalar Hemlock
- [Inicio Rapido](getting-started/quick-start.md) - Tu primer programa en Hemlock
- [Tutorial](getting-started/tutorial.md) - Guia paso a paso de los conceptos basicos de Hemlock
- [Caminos de Aprendizaje](getting-started/learning-paths.md) - Elige tu ruta de aprendizaje segun tus objetivos

### Nuevo en la Programacion?
- [Glosario](glossary.md) - Definiciones en lenguaje sencillo de terminos de programacion

### Guia del Lenguaje
- [Descripcion General de la Sintaxis](language-guide/syntax.md) - Sintaxis y estructura basica
- [Sistema de Tipos](language-guide/types.md) - Tipos primitivos, inferencia de tipos y conversiones
- [Gestion de Memoria](language-guide/memory.md) - Punteros, buffers y memoria manual
- [Strings](language-guide/strings.md) - Strings UTF-8 y operaciones
- [Runes](language-guide/runes.md) - Codepoints Unicode y manejo de caracteres
- [Flujo de Control](language-guide/control-flow.md) - if/else, bucles, switch y operadores
- [Funciones](language-guide/functions.md) - Funciones, clausuras y recursion
- [Objetos](language-guide/objects.md) - Literales de objeto, metodos y duck typing
- [Arrays](language-guide/arrays.md) - Arrays dinamicos y operaciones
- [Manejo de Errores](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [Modulos](language-guide/modules.md) - Sistema de import/export e importaciones de paquetes

### Temas Avanzados
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Ejecutar Hemlock en el navegador via Emscripten
- [Async y Concurrencia](advanced/async-concurrency.md) - Multi-threading real con async/await
- [Empaquetado y Distribucion](advanced/bundling-packaging.md) - Crear bundles y ejecutables independientes
- [Interfaz de Funciones Foraneas](advanced/ffi.md) - Llamar funciones C desde bibliotecas compartidas
- [E/S de Archivos](advanced/file-io.md) - Operaciones de archivos y gestion de recursos
- [Manejo de Senales](advanced/signals.md) - Manejo de senales POSIX
- [Argumentos de Linea de Comandos](advanced/command-line-args.md) - Acceder a argumentos del programa
- [Ejecucion de Comandos](advanced/command-execution.md) - Ejecutar comandos de shell
- [Perfilado](advanced/profiling.md) - Tiempo de CPU, seguimiento de memoria y deteccion de fugas

### Referencia de API
- [Referencia del Sistema de Tipos](reference/type-system.md) - Referencia completa de tipos
- [Referencia de Operadores](reference/operators.md) - Todos los operadores y precedencia
- [Funciones Integradas](reference/builtins.md) - Funciones y constantes globales
- [API de Strings](reference/string-api.md) - Metodos y propiedades de string
- [API de Arrays](reference/array-api.md) - Metodos y propiedades de array
- [API de Memoria](reference/memory-api.md) - Asignacion y manipulacion de memoria
- [API de Archivos](reference/file-api.md) - Metodos de E/S de archivos
- [API de Concurrencia](reference/concurrency-api.md) - Tareas y canales

### Diseno y Filosofia
- [Filosofia de Diseno](design/philosophy.md) - Principios y objetivos fundamentales
- [Detalles de Implementacion](design/implementation.md) - Como funciona Hemlock internamente

### Contribuir
- [Guias de Contribucion](contributing/guidelines.md) - Como contribuir
- [Guia de Pruebas](contributing/testing.md) - Escribir y ejecutar pruebas

## Referencia Rapida

### Hola Mundo
```hemlock
print("Hello, World!");
```

### Tipos Basicos
```hemlock
let x: i32 = 42;           // 32-bit signed integer
let y: u8 = 255;           // 8-bit unsigned integer
let pi: f64 = 3.14159;     // 64-bit float
let name: string = "Alice"; // UTF-8 string
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode codepoint
```

### Gestion de Memoria
```hemlock
// Safe buffer (recommended)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Raw pointer (for experts)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### Async/Concurrencia
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## Filosofia

Hemlock es **explicito sobre implicito**, siempre:
- Los puntos y coma son obligatorios
- Gestion manual de memoria (sin GC)
- Anotaciones de tipo opcionales con verificaciones en tiempo de ejecucion
- Las operaciones inseguras estan permitidas (tu responsabilidad)

Le damos las herramientas para estar seguro (`buffer`, anotaciones de tipo, verificacion de limites) pero no le obligamos a usarlas (`ptr`, memoria manual, operaciones inseguras).

## Obtener Ayuda

- **Codigo Fuente**: [Repositorio en GitHub](https://github.com/hemlang/hemlock)
- **Gestor de Paquetes**: [hpm](https://github.com/hemlang/hpm) - Gestor de Paquetes de Hemlock
- **Issues**: Reportar bugs y solicitar funcionalidades
- **Ejemplos**: Ver el directorio `examples/`
- **Pruebas**: Ver el directorio `tests/` para ejemplos de uso

## Licencia

Hemlock se distribuye bajo la Licencia MIT.
