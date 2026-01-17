# Referencia de la API de Archivos

Referencia completa para el sistema de E/S de archivos de Hemlock.

---

## Descripcion General

Hemlock proporciona una **API de objetos File** para operaciones de archivos con manejo adecuado de errores y gestion de recursos. Los archivos deben abrirse y cerrarse manualmente.

**Caracteristicas Principales:**
- Objeto File con metodos
- Lectura/escritura de datos de texto y binarios
- Busqueda y posicionamiento
- Mensajes de error apropiados
- Gestion manual de recursos (sin RAII)

---

## Tipo File

**Tipo:** `file`

**Descripcion:** Manejador de archivo para operaciones de E/S

**Propiedades (Solo Lectura):**
- `.path` - Ruta del archivo (string)
- `.mode` - Modo de apertura (string)
- `.closed` - Si el archivo esta cerrado (bool)

---

## Abrir Archivos

### open

Abre un archivo para lectura, escritura, o ambos.

**Firma:**
```hemlock
open(path: string, mode?: string): file
```

**Parametros:**
- `path` - Ruta del archivo (relativa o absoluta)
- `mode` (opcional) - Modo de apertura (predeterminado: `"r"`)

**Retorna:** Objeto File

**Modos:**
- `"r"` - Lectura (predeterminado)
- `"w"` - Escritura (trunca archivo existente)
- `"a"` - Anexar
- `"r+"` - Lectura y escritura
- `"w+"` - Lectura y escritura (trunca)
- `"a+"` - Lectura y anexar

**Ejemplos:**
```hemlock
// Modo lectura (predeterminado)
let f = open("data.txt");
let f_read = open("data.txt", "r");

// Modo escritura (trunca)
let f_write = open("output.txt", "w");

// Modo anexar
let f_append = open("log.txt", "a");

// Modo lectura/escritura
let f_rw = open("data.bin", "r+");

// Lectura/escritura (trunca)
let f_rw_trunc = open("output.bin", "w+");

// Lectura/anexar
let f_ra = open("log.txt", "a+");
```

**Manejo de Errores:**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Error al abrir:", e);
    // Error: Failed to open 'missing.txt': No such file or directory
}
```

**Importante:** Los archivos deben cerrarse manualmente con `f.close()` para evitar fugas de descriptores de archivo.

---

## Metodos de File

### Lectura

#### read

Lee texto desde el archivo.

**Firma:**
```hemlock
file.read(size?: i32): string
```

**Parametros:**
- `size` (opcional) - Numero de bytes a leer (si se omite, lee hasta EOF)

**Retorna:** String con el contenido del archivo

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");

// Leer archivo completo
let all = f.read();
print(all);

// Leer numero especifico de bytes
let chunk = f.read(1024);

f.close();
```

**Comportamiento:**
- Lee desde la posicion actual del archivo
- Retorna string vacio en EOF
- Avanza la posicion del archivo

**Errores:**
- Leer desde archivo cerrado
- Leer desde archivo de solo escritura

---

#### read_bytes

Lee datos binarios desde el archivo.

**Firma:**
```hemlock
file.read_bytes(size: i32): buffer
```

**Parametros:**
- `size` - Numero de bytes a leer

**Retorna:** Buffer con datos binarios

**Ejemplos:**
```hemlock
let f = open("data.bin", "r");

// Leer 256 bytes
let binary = f.read_bytes(256);
print(binary.length);       // 256

// Procesar datos binarios
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**Comportamiento:**
- Lee el numero exacto de bytes
- Retorna buffer (no string)
- Avanza la posicion del archivo

---

### Escritura

#### write

Escribe texto al archivo.

**Firma:**
```hemlock
file.write(data: string): i32
```

**Parametros:**
- `data` - String a escribir

**Retorna:** Numero de bytes escritos (i32)

**Ejemplos:**
```hemlock
let f = open("output.txt", "w");

// Escribir texto
let written = f.write("Hello, World!\n");
print("Escribio", written, "bytes");

// Multiples escrituras
f.write("Linea 1\n");
f.write("Linea 2\n");
f.write("Linea 3\n");

f.close();
```

**Comportamiento:**
- Escribe en la posicion actual del archivo
- Retorna el numero de bytes escritos
- Avanza la posicion del archivo

**Errores:**
- Escribir en archivo cerrado
- Escribir en archivo de solo lectura

---

#### write_bytes

Escribe datos binarios al archivo.

**Firma:**
```hemlock
file.write_bytes(data: buffer): i32
```

**Parametros:**
- `data` - Buffer a escribir

**Retorna:** Numero de bytes escritos (i32)

**Ejemplos:**
```hemlock
let f = open("output.bin", "w");

// Crear buffer
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Escribir buffer
let written = f.write_bytes(buf);
print("Escribio", written, "bytes");

f.close();
```

**Comportamiento:**
- Escribe el contenido del buffer al archivo
- Retorna el numero de bytes escritos
- Avanza la posicion del archivo

---

### Posicionamiento

#### seek

Mueve la posicion del archivo a un desplazamiento especifico de bytes.

**Firma:**
```hemlock
file.seek(position: i32): i32
```

**Parametros:**
- `position` - Desplazamiento en bytes desde el inicio del archivo

**Retorna:** Nueva posicion del archivo (i32)

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");

// Saltar al byte 100
f.seek(100);

// Leer desde esa posicion
let chunk = f.read(50);

// Reiniciar al inicio
f.seek(0);

// Leer desde el inicio
let all = f.read();

f.close();
```

**Comportamiento:**
- Establece la posicion del archivo al desplazamiento absoluto
- Retorna la nueva posicion
- Posicionarse mas alla de EOF esta permitido (crea hueco en el archivo al escribir)

---

#### tell

Obtiene la posicion actual del archivo.

**Firma:**
```hemlock
file.tell(): i32
```

**Retorna:** Desplazamiento actual en bytes desde el inicio del archivo (i32)

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0 (al inicio)

f.read(100);
print(f.tell());        // 100 (despues de leer)

f.seek(50);
print(f.tell());        // 50 (despues de posicionarse)

f.close();
```

---

### Cierre

#### close

Cierra el archivo (idempotente).

**Firma:**
```hemlock
file.close(): null
```

**Retorna:** `null`

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// Seguro llamar multiples veces
f.close();  // Sin error
f.close();  // Sin error
```

**Comportamiento:**
- Cierra el manejador del archivo
- Vacia cualquier escritura pendiente
- Idempotente (seguro llamar multiples veces)
- Establece la propiedad `.closed` a `true`

**Importante:** Siempre cierre los archivos cuando termine para evitar fugas de descriptores de archivo.

---

## Propiedades de File

### .path

Obtiene la ruta del archivo.

**Tipo:** `string`

**Acceso:** Solo lectura

**Ejemplos:**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

Obtiene el modo de apertura.

**Tipo:** `string`

**Acceso:** Solo lectura

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Verifica si el archivo esta cerrado.

**Tipo:** `bool`

**Acceso:** Solo lectura

**Ejemplos:**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Manejo de Errores

Todas las operaciones de archivo incluyen mensajes de error apropiados con contexto:

### Archivo No Encontrado
```hemlock
let f = open("missing.txt", "r");
// Error: Failed to open 'missing.txt': No such file or directory
```

### Leer Desde Archivo Cerrado
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Error: Cannot read from closed file 'data.txt'
```

### Escribir en Archivo de Solo Lectura
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Error: Cannot write to file 'readonly.txt' opened in read-only mode
```

### Usando try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("Error de archivo:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Patrones de Gestion de Recursos

### Patron Basico

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Con Manejo de Errores

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Siempre cerrar, incluso en error
}
```

### Patron Seguro

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... procesar contenido ...
} catch (e) {
    print("Error:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Ejemplos de Uso

### Leer Archivo Completo

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### Escribir Archivo de Texto

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### Anexar a Archivo

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Entrada de log 1");
append_file("log.txt", "Entrada de log 2");
```

### Leer Archivo Binario

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Leyo", binary.length, "bytes");
```

### Escribir Archivo Binario

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### Leer Archivo Linea por Linea

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Linea", i, ":", lines[i]);
    i = i + 1;
}
```

### Copiar Archivo

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### Leer Archivo en Fragmentos

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // Leer 1KB a la vez
        if (chunk.length == 0) {
            break;  // EOF
        }

        // Procesar fragmento
        print("Procesando", chunk.length, "bytes");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## Resumen Completo de Metodos

| Metodo        | Firma                    | Retorna   | Descripcion                  |
|---------------|--------------------------|-----------|------------------------------|
| `read`        | `(size?: i32)`           | `string`  | Leer texto                   |
| `read_bytes`  | `(size: i32)`            | `buffer`  | Leer datos binarios          |
| `write`       | `(data: string)`         | `i32`     | Escribir texto               |
| `write_bytes` | `(data: buffer)`         | `i32`     | Escribir datos binarios      |
| `seek`        | `(position: i32)`        | `i32`     | Establecer posicion del archivo |
| `tell`        | `()`                     | `i32`     | Obtener posicion del archivo |
| `close`       | `()`                     | `null`    | Cerrar archivo (idempotente) |

---

## Resumen Completo de Propiedades

| Propiedad | Tipo     | Acceso       | Descripcion              |
|-----------|----------|--------------|--------------------------|
| `.path`   | `string` | Solo lectura | Ruta del archivo         |
| `.mode`   | `string` | Solo lectura | Modo de apertura         |
| `.closed` | `bool`   | Solo lectura | Si el archivo esta cerrado |

---

## Migracion desde la API Antigua

**API Antigua (Eliminada):**
- `read_file(path)` - Use `open(path, "r").read()`
- `write_file(path, data)` - Use `open(path, "w").write(data)`
- `append_file(path, data)` - Use `open(path, "a").write(data)`
- `file_exists(path)` - Sin reemplazo aun

**Ejemplo de Migracion:**
```hemlock
// Antiguo (v0.0)
let content = read_file("data.txt");
write_file("output.txt", content);

// Nuevo (v0.1)
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## Ver Tambien

- [Funciones Integradas](builtins.md) - Funcion `open()`
- [API de Memoria](memory-api.md) - Tipo Buffer
- [API de Strings](string-api.md) - Metodos de string para procesamiento de texto
