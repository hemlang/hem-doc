# E/S de Archivos en Hemlock

Hemlock proporciona una **API de objeto File** para operaciones de archivo con manejo de errores apropiado y gestion de recursos.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Abriendo Archivos](#abriendo-archivos)
- [Metodos de File](#metodos-de-file)
- [Propiedades de File](#propiedades-de-file)
- [Manejo de Errores](#manejo-de-errores)
- [Gestion de Recursos](#gestion-de-recursos)
- [Referencia Completa de API](#referencia-completa-de-api)
- [Patrones Comunes](#patrones-comunes)
- [Mejores Practicas](#mejores-practicas)

## Vision General

La API de objeto File proporciona:

- **Gestion explicita de recursos** - Los archivos deben cerrarse manualmente
- **Multiples modos de apertura** - Lectura, escritura, anexar, lectura/escritura
- **Operaciones de texto y binario** - Leer/escribir tanto texto como datos binarios
- **Soporte de busqueda** - Acceso aleatorio dentro de archivos
- **Mensajes de error completos** - Reporte de errores consciente del contexto

**Importante:** Los archivos no se cierran automaticamente. Debes llamar `f.close()` para evitar fugas de descriptores de archivo.

## Abriendo Archivos

Usa `open(path, mode?)` para abrir un archivo:

```hemlock
let f = open("data.txt", "r");     // Modo lectura (por defecto)
let f2 = open("output.txt", "w");  // Modo escritura (trunca)
let f3 = open("log.txt", "a");     // Modo anexar
let f4 = open("data.bin", "r+");   // Modo lectura/escritura
```

### Modos de Apertura

| Modo | Descripcion | Archivo Debe Existir | Trunca | Posicion |
|------|-------------|---------------------|--------|----------|
| `"r"` | Lectura (por defecto) | Si | No | Inicio |
| `"w"` | Escritura | No (crea) | Si | Inicio |
| `"a"` | Anexar | No (crea) | No | Final |
| `"r+"` | Leer y escribir | Si | No | Inicio |
| `"w+"` | Leer y escribir | No (crea) | Si | Inicio |
| `"a+"` | Leer y anexar | No (crea) | No | Final |

### Ejemplos

**Leyendo un archivo existente:**
```hemlock
let f = open("config.json", "r");
// o simplemente:
let f = open("config.json");  // "r" es por defecto
```

**Creando un nuevo archivo para escritura:**
```hemlock
let f = open("output.txt", "w");  // Crea o trunca
```

**Anexando a un archivo:**
```hemlock
let f = open("log.txt", "a");  // Crea si no existe
```

**Modo lectura y escritura:**
```hemlock
let f = open("data.bin", "r+");  // Archivo existente, puede leer/escribir
```

## Metodos de File

### Lectura

#### read(size?: i32): string

Leer texto del archivo (parametro size opcional).

**Sin size (leer todo):**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // Leer desde posicion actual hasta EOF
f.close();
```

**Con size (leer bytes especificos):**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // Leer hasta 1024 bytes
let next = f.read(1024);   // Leer siguientes 1024 bytes
f.close();
```

**Retorna:** String conteniendo los datos leidos, o string vacio si esta en EOF

**Ejemplo - Leyendo archivo completo:**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**Ejemplo - Leyendo en chunks:**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // Chunks de 4KB
    if (chunk == "") { break; }  // EOF alcanzado
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

Leer datos binarios (retorna buffer).

**Parametros:**
- `size` (i32) - Numero de bytes a leer

**Retorna:** Buffer conteniendo los bytes leidos

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // Leer 256 bytes
print(binary.length);  // 256 (o menos si EOF)

// Acceder a bytes individuales
let first_byte = binary[0];
print(first_byte);

f.close();
```

**Ejemplo - Leyendo archivo binario completo:**
```hemlock
let f = open("data.bin", "r");
let size = 10240;  // Tamano esperado
let data = f.read_bytes(size);
f.close();

// Procesar datos binarios
let i = 0;
while (i < data.length) {
    let byte = data[i];
    // ... procesar byte
    i = i + 1;
}
```

### Escritura

#### write(data: string): i32

Escribir texto al archivo (retorna bytes escritos).

**Parametros:**
- `data` (string) - Texto a escribir

**Retorna:** Numero de bytes escritos (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Wrote " + typeof(written) + " bytes");  // "Wrote 14 bytes"
f.close();
```

**Ejemplo - Escribiendo multiples lineas:**
```hemlock
let f = open("output.txt", "w");
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");
f.close();
```

**Ejemplo - Anexando a archivo de log:**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Application started\n");
f.write("[INFO] User logged in\n");
f.close();
```

#### write_bytes(data: buffer): i32

Escribir datos binarios (retorna bytes escritos).

**Parametros:**
- `data` (buffer) - Datos binarios a escribir

**Retorna:** Numero de bytes escritos (i32)

```hemlock
let f = open("output.bin", "w");

// Crear datos binarios
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Wrote " + typeof(bytes) + " bytes");

f.close();
```

**Ejemplo - Copiando archivo binario:**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let data = src.read_bytes(1024);
while (data.length > 0) {
    dst.write_bytes(data);
    data = src.read_bytes(1024);
}

src.close();
dst.close();
```

### Busqueda

#### seek(position: i32): i32

Moverse a posicion especifica (retorna nueva posicion).

**Parametros:**
- `position` (i32) - Desplazamiento en bytes desde el inicio del archivo

**Retorna:** Nueva posicion (i32)

```hemlock
let f = open("data.txt", "r");

// Moverse al byte 100
f.seek(100);

// Leer desde posicion 100
let data = f.read(50);

// Restablecer al inicio
f.seek(0);

f.close();
```

**Ejemplo - Acceso aleatorio:**
```hemlock
let f = open("records.dat", "r");

// Leer registro en offset 1000
f.seek(1000);
let record1 = f.read_bytes(100);

// Leer registro en offset 2000
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Obtener posicion actual en el archivo.

**Retorna:** Desplazamiento actual en bytes (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0 (al inicio)

f.read(100);
let pos2 = f.tell();  // 100 (despues de leer 100 bytes)

f.seek(500);
let pos3 = f.tell();  // 500 (despues de busqueda)

f.close();
```

**Ejemplo - Midiendo cantidad leida:**
```hemlock
let f = open("data.txt", "r");

let start = f.tell();
let content = f.read();
let end = f.tell();

let bytes_read = end - start;
print("Read " + typeof(bytes_read) + " bytes");

f.close();
```

### Cierre

#### close()

Cerrar archivo (idempotente, puede llamarse multiples veces).

```hemlock
let f = open("data.txt", "r");
// ... usar archivo
f.close();
f.close();  // Seguro - sin error en segundo cierre
```

**Notas importantes:**
- Siempre cerrar archivos cuando termines para evitar fugas de descriptores de archivo
- El cierre es idempotente - puede llamarse multiples veces de forma segura
- Despues de cerrar, todas las otras operaciones daran error
- Usar bloques `finally` para asegurar que los archivos se cierren incluso en errores

## Propiedades de File

Los objetos File tienen tres propiedades de solo lectura:

### path: string

La ruta del archivo usada para abrirlo.

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

El modo con el que se abrio el archivo.

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Si el archivo esta cerrado.

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Ejemplo - Verificando si el archivo esta abierto:**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... procesar contenido
}

f.close();

if (f.closed) {
    print("File is now closed");
}
```

## Manejo de Errores

Todas las operaciones de archivo incluyen mensajes de error apropiados con contexto.

### Errores Comunes

**Archivo no encontrado:**
```hemlock
let f = open("missing.txt", "r");
// Error: Failed to open 'missing.txt': No such file or directory
```

**Leyendo de archivo cerrado:**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Error: Cannot read from closed file 'data.txt'
```

**Escribiendo a archivo de solo lectura:**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Error: Cannot write to file 'readonly.txt' opened in read-only mode
```

**Leyendo de archivo de solo escritura:**
```hemlock
let f = open("output.txt", "w");
f.read();
// Error: Cannot read from file 'output.txt' opened in write-only mode
```

### Usando try/catch

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Error reading file: " + e);
}
```

## Gestion de Recursos

### Patron Basico

Siempre cerrar archivos explicitamente:

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Con Manejo de Errores (Recomendado)

Usar `finally` para asegurar que los archivos se cierren incluso en errores:

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Siempre cerrar, incluso en error
}
```

### Multiples Archivos

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Patron de Funcion Auxiliar

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Uso:
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## Referencia Completa de API

### Funciones

| Funcion | Parametros | Retorna | Descripcion |
|---------|-----------|---------|-------------|
| `open(path, mode?)` | path: string, mode?: string | File | Abrir archivo (modo por defecto es "r") |

### Metodos

| Metodo | Parametros | Retorna | Descripcion |
|--------|-----------|---------|-------------|
| `read(size?)` | size?: i32 | string | Leer texto (todo o bytes especificos) |
| `read_bytes(size)` | size: i32 | buffer | Leer datos binarios |
| `write(data)` | data: string | i32 | Escribir texto, retorna bytes escritos |
| `write_bytes(data)` | data: buffer | i32 | Escribir datos binarios, retorna bytes escritos |
| `seek(position)` | position: i32 | i32 | Buscar posicion, retorna nueva posicion |
| `tell()` | - | i32 | Obtener posicion actual |
| `close()` | - | null | Cerrar archivo (idempotente) |

### Propiedades (solo lectura)

| Propiedad | Tipo | Descripcion |
|-----------|------|-------------|
| `path` | string | Ruta del archivo |
| `mode` | string | Modo de apertura |
| `closed` | bool | Si el archivo esta cerrado |

## Patrones Comunes

### Leyendo Archivo Completo

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### Escribiendo Archivo Completo

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### Anexando a Archivo

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Event occurred\n");
```

### Leyendo Lineas

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Procesando Archivos Grandes en Chunks

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // Chunks de 4KB
            if (chunk == "") { break; }

            // Procesar chunk
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Copia de Archivo Binario

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### Truncar Archivo

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // Modo "w" trunca
    f.close();
}

truncate_file("empty_me.txt");
```

### Lectura de Acceso Aleatorio

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

### Tamano de Archivo

```hemlock
fn file_size(path: string): i32 {
    let f = open(path, "r");
    try {
        // Buscar al final
        let end = f.seek(999999999);  // Numero grande
        f.seek(0);  // Restablecer
        return end;
    } finally {
        f.close();
    }
}

let size = file_size("data.txt");
print("File size: " + typeof(size) + " bytes");
```

### Lectura/Escritura Condicional

```hemlock
fn update_file(path: string, condition, new_content: string) {
    let f = open(path, "r+");
    try {
        let content = f.read();

        if (condition(content)) {
            f.seek(0);  // Restablecer al inicio
            f.write(new_content);
        }
    } finally {
        f.close();
    }
}
```

## Mejores Practicas

### 1. Siempre Usar try/finally

```hemlock
// Bueno
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// Malo - el archivo podria no cerrarse en error
let f = open("data.txt", "r");
let content = f.read();
process(content);  // Si esto lanza, el archivo tiene fuga
f.close();
```

### 2. Verificar Estado del Archivo Antes de Operaciones

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... usar contenido
}

f.close();
```

### 3. Usar Modos Apropiados

```hemlock
// Solo lectura? Usar "r"
let f = open("config.json", "r");

// Reemplazando completamente? Usar "w"
let f = open("output.txt", "w");

// Agregando al final? Usar "a"
let f = open("log.txt", "a");
```

### 4. Manejar Errores Graciosamente

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Warning: Could not read " + path + ": " + e);
        return "";
    }
}
```

### 5. Cerrar Archivos en Orden Inverso de Apertura

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... usar archivos
} finally {
    // Cerrar en orden inverso
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Evitar Leer Archivos Grandes Completamente

```hemlock
// Malo para archivos grandes
let f = open("huge.log", "r");
let content = f.read();  // Carga archivo completo en memoria
f.close();

// Bueno - procesar en chunks
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Resumen

La API de E/S de Archivos de Hemlock proporciona:

- ✅ Operaciones de archivo simples y explicitas
- ✅ Soporte de texto y binario
- ✅ Acceso aleatorio con seek/tell
- ✅ Mensajes de error claros con contexto
- ✅ Operacion de cierre idempotente

Recuerda:
- Siempre cerrar archivos manualmente
- Usar try/finally para seguridad de recursos
- Elegir modos de apertura apropiados
- Manejar errores graciosamente
- Procesar archivos grandes en chunks
