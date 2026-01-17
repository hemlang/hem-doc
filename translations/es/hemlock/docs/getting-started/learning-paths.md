# Rutas de Aprendizaje

Diferentes objetivos requieren diferentes conocimientos. Elija la ruta que coincida con lo que desea construir.

---

## Ruta 1: Scripts Rapidos y Automatizacion

**Objetivo:** Escribir scripts para automatizar tareas, procesar archivos y realizar trabajos.

**Tiempo para ser productivo:** Rapido - puede comenzar a escribir scripts utiles inmediatamente.

### Lo Que Aprendera

1. **[Inicio Rapido](quick-start.md)** - Su primer programa, sintaxis basica
2. **[Cadenas](../language-guide/strings.md)** - Procesamiento de texto, division, busqueda
3. **[Arreglos](../language-guide/arrays.md)** - Listas, filtrado, transformacion de datos
4. **[E/S de Archivos](../advanced/file-io.md)** - Lectura y escritura de archivos
5. **[Argumentos de Linea de Comandos](../advanced/command-line-args.md)** - Obtener entrada de usuarios

### Omitir Por Ahora

- Gestion de memoria (automatica para scripts)
- Async/concurrencia (excesivo para scripts simples)
- FFI (solo necesario para interoperabilidad con C)

### Proyecto de Ejemplo: Renombrador de Archivos

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// Renombrar todos los archivos .txt a .md
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Renamed: ${file} -> ${new_name}`);
    }
}
```

---

## Ruta 2: Procesamiento y Analisis de Datos

**Objetivo:** Analizar datos, transformarlos, generar informes.

**Tiempo para ser productivo:** Rapido - los metodos de cadenas y arreglos de Hemlock lo hacen facil.

### Lo Que Aprendera

1. **[Inicio Rapido](quick-start.md)** - Conceptos basicos
2. **[Cadenas](../language-guide/strings.md)** - Analisis, division, formato
3. **[Arreglos](../language-guide/arrays.md)** - map, filter, reduce para transformacion de datos
4. **[Objetos](../language-guide/objects.md)** - Datos estructurados
5. **Biblioteca Estandar:**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - Analisis de JSON
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - Archivos CSV
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - Operaciones de archivo

### Proyecto de Ejemplo: Analizador CSV

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// Calcular ventas totales
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Total sales: $${total}`);

// Encontrar el mejor vendedor
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Top sale: ${top.product} - $${top.amount}`);
```

---

## Ruta 3: Programacion Web y de Redes

**Objetivo:** Construir clientes HTTP, trabajar con APIs, crear servidores.

**Tiempo para ser productivo:** Medio - requiere entender los conceptos basicos de async.

### Lo Que Aprendera

1. **[Inicio Rapido](quick-start.md)** - Conceptos basicos
2. **[Funciones](../language-guide/functions.md)** - Callbacks y clausuras
3. **[Manejo de Errores](../language-guide/error-handling.md)** - try/catch para errores de red
4. **[Async y Concurrencia](../advanced/async-concurrency.md)** - spawn, await, canales
5. **Biblioteca Estandar:**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - Solicitudes HTTP
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON para APIs
   - **[@stdlib/net](../../stdlib/docs/net.md)** - Sockets TCP/UDP
   - **[@stdlib/url](../../stdlib/docs/url.md)** - Analisis de URL

### Proyecto de Ejemplo: Cliente de API

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// Solicitud GET
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}: ${user.email}`);
}

// Solicitud POST
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`Created user with ID: ${parse(result.body).id}`);
```

---

## Ruta 4: Programacion de Sistemas

**Objetivo:** Escribir codigo de bajo nivel, trabajar con memoria, interfaces con bibliotecas C.

**Tiempo para ser productivo:** Mas largo - requiere entender la gestion de memoria.

### Lo Que Aprendera

1. **[Inicio Rapido](quick-start.md)** - Conceptos basicos
2. **[Tipos](../language-guide/types.md)** - Entender i32, u8, ptr, etc.
3. **[Gestion de Memoria](../language-guide/memory.md)** - alloc, free, buffers
4. **[FFI](../advanced/ffi.md)** - Llamar funciones C
5. **[Senales](../advanced/signals.md)** - Manejo de senales

### Conceptos Clave

**Lista de Verificacion de Seguridad de Memoria:**
- [ ] Cada `alloc()` tiene un `free()` correspondiente
- [ ] Usar `buffer()` a menos que necesite `ptr` crudo
- [ ] Establecer punteros a `null` despues de liberar
- [ ] Usar `try/finally` para garantizar limpieza

**Mapeo de Tipos para FFI:**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long` (64-bit) |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### Proyecto de Ejemplo: Pool de Memoria Personalizado

```hemlock
// Asignador bump simple
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool exhausted";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// Usarlo
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // Reutilizar toda la memoria
pool_destroy();  // Limpiar
```

---

## Ruta 5: Programas Paralelos y Concurrentes

**Objetivo:** Ejecutar codigo en multiples nucleos de CPU, construir aplicaciones responsivas.

**Tiempo para ser productivo:** Medio - la sintaxis async es directa, pero razonar sobre paralelismo requiere practica.

### Lo Que Aprendera

1. **[Inicio Rapido](quick-start.md)** - Conceptos basicos
2. **[Funciones](../language-guide/functions.md)** - Clausuras (importantes para async)
3. **[Async y Concurrencia](../advanced/async-concurrency.md)** - Profundizacion completa
4. **[Atomicos](../advanced/atomics.md)** - Programacion sin bloqueos

### Conceptos Clave

**Modelo async de Hemlock:**
- `async fn` - Definir una funcion que puede ejecutarse en otro hilo
- `spawn(fn, args...)` - Comenzar a ejecutarla, devuelve un manejador de tarea
- `join(task)` o `await task` - Esperar a que termine, obtener resultado
- `channel(size)` - Crear una cola para enviar datos entre tareas

**Importante:** Las tareas reciben *copias* de valores. Si pasa un puntero, usted es responsable de asegurar que la memoria permanezca valida hasta que la tarea complete.

### Proyecto de Ejemplo: Procesador de Archivos Paralelo

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// Procesar todos los archivos en paralelo
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// Recolectar resultados
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}: ${count} lines`);
    total_lines = total_lines + count;
}

print(`Total: ${total_lines} lines`);
```

---

## Que Aprender Primero (Cualquier Ruta)

Sin importar su objetivo, comience con estos fundamentos:

### Semana 1: Conceptos Basicos Principales
1. **[Inicio Rapido](quick-start.md)** - Escriba y ejecute su primer programa
2. **[Sintaxis](../language-guide/syntax.md)** - Variables, operadores, flujo de control
3. **[Funciones](../language-guide/functions.md)** - Definir y llamar funciones

### Semana 2: Manejo de Datos
4. **[Cadenas](../language-guide/strings.md)** - Manipulacion de texto
5. **[Arreglos](../language-guide/arrays.md)** - Colecciones e iteracion
6. **[Objetos](../language-guide/objects.md)** - Datos estructurados

### Semana 3: Robustez
7. **[Manejo de Errores](../language-guide/error-handling.md)** - try/catch/throw
8. **[Modulos](../language-guide/modules.md)** - Import/export, usando stdlib

### Luego: Elija Su Ruta Arriba

---

## Hoja de Referencia: Viniendo de Otros Lenguajes

### Desde Python

| Python | Hemlock | Notas |
|--------|---------|-------|
| `x = 42` | `let x = 42;` | Punto y coma requerido |
| `def fn():` | `fn name() { }` | Llaves requeridas |
| `if x:` | `if (x) { }` | Parentesis y llaves requeridos |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | Bucles for estilo C |
| `for item in list:` | `for (item in array) { }` | For-in funciona igual |
| `list.append(x)` | `array.push(x);` | Nombre de metodo diferente |
| `len(s)` | `s.length` o `len(s)` | Ambos funcionan |
| Memoria automatica | Manual para `ptr` | La mayoria de tipos auto-limpian |

### Desde JavaScript

| JavaScript | Hemlock | Notas |
|------------|---------|-------|
| `let x = 42` | `let x = 42;` | Igual (punto y coma requerido) |
| `const x = 42` | `let x = 42;` | Sin palabra clave const |
| `function fn()` | `fn name() { }` | Palabra clave diferente |
| `() => x` | `fn() { return x; }` | Sin funciones flecha |
| `async/await` | `async/await` | Misma sintaxis |
| `Promise` | `spawn/join` | Modelo diferente |
| GC automatico | Manual para `ptr` | La mayoria de tipos auto-limpian |

### Desde C/C++

| C | Hemlock | Notas |
|---|---------|-------|
| `int x = 42;` | `let x: i32 = 42;` | Tipo despues de dos puntos |
| `malloc(n)` | `alloc(n)` | Mismo concepto |
| `free(p)` | `free(p)` | Igual |
| `char* s = "hi"` | `let s = "hi";` | Las cadenas son gestionadas |
| `#include` | `import { } from` | Importaciones de modulos |
| Manual todo | Auto para la mayoria de tipos | Solo `ptr` necesita manual |

---

## Obteniendo Ayuda

- **[Glosario](../glossary.md)** - Definiciones de terminos de programacion
- **[Ejemplos](../../examples/)** - Programas completos funcionando
- **[Pruebas](../../tests/)** - Ver como se usan las caracteristicas
- **GitHub Issues** - Hacer preguntas, reportar errores

---

## Niveles de Dificultad

A lo largo de la documentacion, vera estos marcadores:

| Marcador | Significado |
|----------|-------------|
| **Principiante** | No se necesita experiencia previa en programacion |
| **Intermedio** | Asume conocimientos basicos de programacion |
| **Avanzado** | Requiere comprension de conceptos de sistemas |

Si algo marcado como "Principiante" le confunde, consulte el [Glosario](../glossary.md) para definiciones de terminos.
