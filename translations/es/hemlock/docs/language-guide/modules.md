# Sistema de Módulos de Hemlock

Este documento describe el sistema de módulos de importación/exportación estilo ES6 implementado para Hemlock.

## Resumen

Hemlock soporta un sistema de módulos basado en archivos con sintaxis de importación/exportación estilo ES6. Los módulos son:
- **Singletons**: Cada módulo se carga una vez y se almacena en caché
- **Basados en archivos**: Los módulos corresponden a archivos .hml en disco
- **Importados explícitamente**: Las dependencias se declaran con sentencias import
- **Ejecutados topológicamente**: Las dependencias se ejecutan antes que los dependientes

Para gestión de paquetes y dependencias de terceros, consulte [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Sintaxis

### Sentencias Export

**Exportaciones con nombre en línea:**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**Lista de exportación:**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Export Extern (Funciones FFI):**
```hemlock
import "libc.so.6";

// Exportar funciones FFI para uso en otros módulos
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

Consulte la [Documentación FFI](../advanced/ffi.md#exporting-ffi-functions) para más detalles sobre la exportación de funciones FFI.

**Export Define (Tipos Struct):**
```hemlock
// Exportar definiciones de tipos struct
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**Importante:** Los tipos struct exportados se registran globalmente cuando el módulo se carga. Se vuelven disponibles automáticamente cuando importa cualquier cosa del módulo - NO necesita (y no puede) importarlos explícitamente por nombre:

```hemlock
// BIEN - los tipos struct están auto-disponibles después de cualquier importación
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Funciona!

// MAL - no puede importar explícitamente tipos struct
import { Vector2 } from "./my_module.hml";  // Error: Undefined variable 'Vector2'
```

Consulte la [Documentación FFI](../advanced/ffi.md#exporting-struct-types) para más detalles sobre la exportación de tipos struct.

**Re-exportaciones:**
```hemlock
// Re-exportar desde otro módulo
export { add, subtract } from "./math.hml";
```

### Sentencias Import

**Importaciones con nombre:**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Importación de espacio de nombres:**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**Alias:**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## Resolución de Módulos

### Tipos de Ruta

**Rutas relativas:**
```hemlock
import { foo } from "./module.hml";       // Mismo directorio
import { bar } from "../parent.hml";      // Directorio padre
import { baz } from "./sub/nested.hml";   // Subdirectorio
```

**Rutas absolutas:**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Manejo de extensiones:**
- La extensión `.hml` puede omitirse - se agregará automáticamente
- `./math` se resuelve a `./math.hml`

## Características

### Detección de Dependencias Circulares

El sistema de módulos detecta dependencias circulares y reporta un error:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Caché de Módulos

Los módulos se cargan una vez y se almacenan en caché. Múltiples importaciones del mismo módulo retornan la misma instancia:

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // Misma instancia!
print(count);  // Todavía 1 (estado compartido)
```

### Inmutabilidad de Importaciones

Los bindings importados no pueden ser reasignados:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // ERROR: cannot reassign imported binding
```

## Detalles de Implementación

### Arquitectura

**Archivos:**
- `include/module.h` - API del sistema de módulos
- `src/module.c` - Carga, caché y ejecución de módulos
- Soporte del parser en `src/parser.c`
- Soporte del runtime en `src/interpreter/runtime.c`

**Componentes clave:**
1. **ModuleCache**: Mantiene módulos cargados indexados por ruta absoluta
2. **Module**: Representa un módulo cargado con su AST y exportaciones
3. **Resolución de Rutas**: Resuelve rutas relativas/absolutas a rutas canónicas
4. **Ejecución Topológica**: Ejecuta módulos en orden de dependencias

### Proceso de Carga de Módulos

1. **Fase de Análisis**: Tokenizar y parsear el archivo del módulo
2. **Resolución de Dependencias**: Cargar recursivamente módulos importados
3. **Detección de Ciclos**: Verificar si el módulo ya está siendo cargado
4. **Caché**: Almacenar módulo en caché por ruta absoluta
5. **Fase de Ejecución**: Ejecutar en orden topológico (dependencias primero)

### API

```c
// API de alto nivel
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// API de bajo nivel
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Pruebas

Los módulos de prueba están ubicados en `tests/modules/` y `tests/parity/modules/`:

- `math.hml` - Módulo básico con exportaciones
- `test_import_named.hml` - Prueba de importación con nombre
- `test_import_namespace.hml` - Prueba de importación de espacio de nombres
- `test_import_alias.hml` - Prueba de alias de importación
- `export_extern.hml` - Prueba de exportación de función FFI extern (Linux)

## Importaciones de Paquetes (hpm)

Con [hpm](https://github.com/hemlang/hpm) instalado, puede importar paquetes de terceros desde GitHub:

```hemlock
// Importar desde la raíz del paquete (usa "main" de package.json)
import { app, router } from "hemlang/sprout";

// Importar desde subruta
import { middleware } from "hemlang/sprout/middleware";

// Biblioteca estándar (incorporada en Hemlock)
import { HashMap } from "@stdlib/collections";
```

Los paquetes se instalan en `hem_modules/` y se resuelven usando la sintaxis `owner/repo` de GitHub.

```bash
# Instalar un paquete
hpm install hemlang/sprout

# Instalar con restricción de versión
hpm install hemlang/sprout@^1.0.0
```

Consulte la [documentación de hpm](https://github.com/hemlang/hpm) para detalles completos.

## Limitaciones Actuales

1. **Sin Importaciones Dinámicas**: `import()` como función en tiempo de ejecución no está soportado
2. **Sin Exportaciones Condicionales**: Las exportaciones deben estar en el nivel superior
3. **Rutas de Biblioteca Estáticas**: Las importaciones de bibliotecas FFI usan rutas estáticas (específicas de plataforma)

## Trabajo Futuro

- Importaciones dinámicas con función `import()`
- Exportaciones condicionales
- Metadatos de módulo (`import.meta`)
- Tree shaking y eliminación de código muerto

## Ejemplos

Consulte `tests/modules/` para ejemplos funcionales del sistema de módulos.

Estructura de módulos de ejemplo:
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (módulo barrel)
└── utils/
    └── helpers.hml
```

Uso de ejemplo:
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
