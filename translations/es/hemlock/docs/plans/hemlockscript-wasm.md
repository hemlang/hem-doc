# HemlockScript: Hemlock → WASM via Emscripten

> Programas Hemlock portables que se ejecutan en el navegador.

## Objetivo

Agregar un objetivo de compilacion WASM a `hemlockc` para que los programas Hemlock puedan ejecutarse en navegadores y otros runtimes WASM (Node/Deno/Cloudflare Workers). El enfoque: compilar Hemlock → C (pipeline existente) → WASM (via Emscripten), con un shim de runtime compatible con navegadores que reemplaza los builtins solo de POSIX.

**No es objetivo:** Reescribir el compilador o runtime desde cero. Aprovechamos el codegen C existente de `hemlockc` y `libhemlock_runtime` tanto como sea posible.

---

## Arquitectura

```
Fuente Hemlock (.hml)
        ↓
   hemlockc (frontend existente + codegen)
        ↓
   Codigo C generado (existente)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (runtime adaptado para WASM)
        ↓
   program.wasm + program.js (cargador/enlace)
        ↓
   Navegador / Node / Deno / Runtime WASM
```

La idea clave: `hemlockc` ya emite C portable. No necesitamos un nuevo backend -- necesitamos una biblioteca de runtime compatible con WASM y un pipeline de compilacion con Emscripten.

---

## Fase 1: Compilacion WASM Minima (Solo Lenguaje Base)

**Resultado:** `make wasm` produce un bundle `.wasm` + `.js` que puede ejecutar programas Hemlock computacionales puros en el navegador.

### 1.1 Crear capa shim de runtime WASM

Crear `runtime/src/wasm_shim.c` con implementaciones stub/reemplazo para funciones dependientes de POSIX.

### 1.2 Agregar guardas `#ifdef __EMSCRIPTEN__` al runtime

Envolver codigo solo de POSIX en los archivos fuente existentes del runtime con guardas de preprocesador.

### 1.3 Crear objetivo de Makefile especifico para WASM

### 1.4 Modificar `hemlockc` para soportar objetivo WASM

Agregar una bandera `--target wasm` a `hemlockc`.

### 1.5 Crear harness de prueba HTML

### Entregables de la Fase 1
- `make wasm-compile FILE=hello.hml` produce salida ejecutable en navegador
- Todas las caracteristicas de computacion pura de Hemlock funcionan
- `print()` produce salida a la consola del navegador / elemento HTML
- Caracteristicas no soportadas (FFI, sockets, procesos, senales) entran en panico con mensaje claro

---

## Fase 2: E/S del Navegador y Stdlib

**Resultado:** Los programas Hemlock pueden hacer trabajo util en el navegador -- acceso a archivos (FS virtual), operaciones de tiempo, y los modulos portables de stdlib funcionan.

### 2.1 Sistema de archivos virtual de Emscripten

### 2.2 Portar los 22 modulos de stdlib ya portables

Estos modulos son Hemlock puro y no necesitan cambios:

`arena`, `assert`, `collections`, `csv`, `datetime`, `encoding`, `fmt`, `iter`, `json`, `logging`, `math`, `path`, `random`, `regex`, `retry`, `semver`, `strings`, `testing`, `terminal`, `toml`, `url`, `uuid`

### 2.3 Adaptar modulo de tiempo

### 2.4 Adaptar modulos env/os/args

---

## Fase 3: Puente de Interoperabilidad con JavaScript

**Resultado:** Los programas Hemlock WASM pueden llamar APIs del navegador y funciones JavaScript, y JavaScript puede llamar funciones de Hemlock.

### 3.1 Puente JavaScript (`hemlock_js_bridge`)

```hemlock
import { fetch } from "@wasm/browser";
let response = await fetch("https://api.example.com/data");
print(response);
```

### 3.2 Funciones exportadas (Hemlock → JS)

```hemlock
export fn fibonacci(n: i32): i32 {
    if (n <= 1) { return n; }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

### 3.3 Adaptar modulos de red para navegador

### 3.4 Adaptar modulo de criptografia

---

## Fase 4: Async e Hilos (Extension)

**Resultado:** El `spawn`/`await` de Hemlock funciona en el navegador usando Web Workers.

### 4.1 Generacion de tareas basada en Web Workers

### 4.2 Asyncify para operaciones bloqueantes

---

## Lo que Funciona Inmediatamente (Sin Cambios Necesarios)

Estas caracteristicas de Hemlock compilan a C estandar que Emscripten maneja nativamente:

- Todos los operadores aritmeticos, de bits, logicos
- Variables, alcance, clausuras
- Funciones, recursion, funciones con cuerpo de expresion
- if/else, while, for, loop, switch, coincidencia de patrones
- Objetos, arrays, strings (todos los 19+23 metodos)
- Anotaciones de tipo y verificacion de tipos en runtime
- Try/catch/finally/throw
- Defer
- Strings de plantilla
- Coalescencia null (`??`, `?.`, `??=`)
- Argumentos con nombre
- Tipos compuestos, alias de tipo
- `print()`, `eprint()` (via mapeo de consola de Emscripten)
- `alloc()`/`free()`/`buffer()` (memoria lineal)
- `typeof()`, `len()`, `sizeof()`
- Builtins matematicos (sin, cos, sqrt, etc.)
- Todo el conteo de referencias / gestion de memoria

---

## Alcance Estimado por Fase

| Fase | Alcance | Dependencias |
|------|---------|-------------|
| **Fase 1** | ~800 lineas nuevo C, ~200 lineas guardas #ifdef, cambios en Makefile | SDK de Emscripten |
| **Fase 2** | ~200 lineas C, pruebas de stdlib, Makefile | Fase 1 |
| **Fase 3** | ~600 lineas C (puente), ~200 lineas Hemlock (stdlib) | Fase 1 |
| **Fase 4** | ~1000 lineas C (hilos Worker), complejo | Fase 1+3 |

Orden recomendado: Fase 1 → Fase 2 → Fase 3 → Fase 4

La Fase 1 sola le da un "Hemlock en el navegador" util para cargas de trabajo computacionales. Las Fases 2-4 agregan incrementalmente E/S e interoperabilidad.
