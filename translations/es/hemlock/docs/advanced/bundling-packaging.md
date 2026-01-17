# Empaquetado y Distribucion

Hemlock proporciona herramientas integradas para empaquetar proyectos de multiples archivos en archivos distribuibles unicos y crear ejecutables autocontenidos.

## Vision General

| Comando | Salida | Caso de Uso |
|---------|--------|-------------|
| `--bundle` | `.hmlc` o `.hmlb` | Distribuir bytecode (requiere Hemlock para ejecutar) |
| `--package` | Ejecutable | Binario independiente (sin dependencias) |
| `--compile` | `.hmlc` | Compilar archivo unico (sin resolucion de imports) |

## Empaquetado (Bundling)

El empaquetador resuelve todas las sentencias `import` desde un punto de entrada y las aplana en un solo archivo.

### Uso Basico

```bash
# Empaquetar app.hml y todos sus imports en app.hmlc
hemlock --bundle app.hml

# Especificar ruta de salida
hemlock --bundle app.hml -o dist/app.hmlc

# Crear paquete comprimido (.hmlb) - tamano de archivo mas pequeno
hemlock --bundle app.hml --compress -o app.hmlb

# Salida detallada (muestra modulos resueltos)
hemlock --bundle app.hml --verbose
```

### Formatos de Salida

**`.hmlc` (Sin comprimir)**
- Formato AST serializado
- Rapido de cargar y ejecutar
- Formato de salida por defecto

**`.hmlb` (Comprimido)**
- `.hmlc` comprimido con zlib
- Tamano de archivo mas pequeno (tipicamente 50-70% de reduccion)
- Inicio ligeramente mas lento debido a la descompresion

### Ejecutando Archivos Empaquetados

```bash
# Ejecutar paquete sin comprimir
hemlock app.hmlc

# Ejecutar paquete comprimido
hemlock app.hmlb

# Pasar argumentos
hemlock app.hmlc arg1 arg2
```

### Ejemplo: Proyecto Multi-Modulo

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # Se ejecuta con todas las dependencias empaquetadas
```

### Imports de stdlib

El empaquetador resuelve automaticamente imports de `@stdlib/`:

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

Cuando se empaqueta, los modulos de stdlib se incluyen en la salida.

## Empaquetado como Ejecutable

El empaquetado crea un ejecutable autocontenido incrustando el bytecode empaquetado en una copia del interprete de Hemlock.

### Uso Basico

```bash
# Crear ejecutable desde app.hml
hemlock --package app.hml

# Especificar nombre de salida
hemlock --package app.hml -o myapp

# Saltar compresion (inicio mas rapido, archivo mas grande)
hemlock --package app.hml --no-compress

# Salida detallada
hemlock --package app.hml --verbose
```

### Ejecutando Ejecutables Empaquetados

```bash
# El ejecutable empaquetado se ejecuta directamente
./myapp

# Los argumentos se pasan al script
./myapp arg1 arg2
```

### Formato de Paquete

Los ejecutables empaquetados usan el formato HMLP:

```
[binario hemlock][carga HMLB/HMLC][tamano_carga:u64][magic HMLP:u32]
```

Cuando un ejecutable empaquetado se ejecuta:
1. Verifica si hay una carga incrustada al final del archivo
2. Si la encuentra, descomprime y ejecuta la carga
3. Si no la encuentra, se comporta como un interprete normal de Hemlock

### Opciones de Compresion

| Flag | Formato | Inicio | Tamano |
|------|---------|--------|--------|
| (por defecto) | HMLB | Normal | Mas pequeno |
| `--no-compress` | HMLC | Mas rapido | Mas grande |

Para herramientas CLI donde el tiempo de inicio importa, usa `--no-compress`.

## Inspeccionando Paquetes

Usa `--info` para inspeccionar archivos empaquetados o compilados:

```bash
hemlock --info app.hmlc
```

Salida:
```
=== File Info: app.hmlc ===
Size: 12847 bytes
Format: HMLC (compiled AST)
Version: 1
Flags: 0x0001 [DEBUG]
Strings: 42
Statements: 156
```

```bash
hemlock --info app.hmlb
```

Salida:
```
=== File Info: app.hmlb ===
Size: 5234 bytes
Format: HMLB (compressed bundle)
Version: 1
Uncompressed: 12847 bytes
Compressed: 5224 bytes
Ratio: 59.3% reduction
```

## Compilacion Nativa

Para ejecutables verdaderamente nativos (sin interprete), usa el compilador de Hemlock:

```bash
# Compilar a ejecutable nativo via C
hemlockc app.hml -o app

# Mantener codigo C generado
hemlockc app.hml -o app --keep-c

# Emitir solo C (no compilar)
hemlockc app.hml -c -o app.c

# Nivel de optimizacion
hemlockc app.hml -o app -O2
```

El compilador genera codigo C e invoca GCC para producir un binario nativo. Esto requiere:
- La biblioteca de runtime de Hemlock (`libhemlock_runtime`)
- Un compilador de C (GCC por defecto)

### Opciones del Compilador

| Opcion | Descripcion |
|--------|-------------|
| `-o <file>` | Nombre del ejecutable de salida |
| `-c` | Emitir solo codigo C |
| `--emit-c <file>` | Escribir C al archivo especificado |
| `-k, --keep-c` | Mantener C generado despues de compilacion |
| `-O<level>` | Nivel de optimizacion (0-3) |
| `--cc <path>` | Compilador de C a usar |
| `--runtime <path>` | Ruta a la biblioteca de runtime |
| `-v, --verbose` | Salida detallada |

## Comparacion

| Enfoque | Portabilidad | Inicio | Tamano | Dependencias |
|---------|--------------|--------|--------|--------------|
| `.hml` | Solo fuente | Tiempo de parseo | Mas pequeno | Hemlock |
| `.hmlc` | Solo Hemlock | Rapido | Pequeno | Hemlock |
| `.hmlb` | Solo Hemlock | Rapido | Mas pequeno | Hemlock |
| `--package` | Independiente | Rapido | Mas grande | Ninguna |
| `hemlockc` | Nativo | Mas rapido | Variable | Libs de runtime |

## Mejores Practicas

1. **Desarrollo**: Ejecutar archivos `.hml` directamente para iteracion rapida
2. **Distribucion (con Hemlock)**: Empaquetar con `--compress` para archivos mas pequenos
3. **Distribucion (independiente)**: Empaquetar como ejecutable para despliegue sin dependencias
4. **Critico en rendimiento**: Usar `hemlockc` para compilacion nativa

## Solucion de Problemas

### "Cannot find stdlib"

El empaquetador busca stdlib en:
1. `./stdlib` (relativo al ejecutable)
2. `../stdlib` (relativo al ejecutable)
3. `/usr/local/lib/hemlock/stdlib`

Asegurate de que Hemlock este correctamente instalado o ejecuta desde el directorio fuente.

### Dependencias Circulares

```
Error: Circular dependency detected when loading 'path/to/module.hml'
```

Refactoriza tus imports para romper el ciclo. Considera usar un modulo compartido para tipos comunes.

### Tamano Grande de Paquete

- Usa compresion por defecto (no uses `--no-compress`)
- El tamano empaquetado incluye el interprete completo (~500KB-1MB base)
- Para tamano minimo, usa `hemlockc` para compilacion nativa
