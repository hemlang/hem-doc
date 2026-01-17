# Perfilado

Hemlock incluye un perfilador integrado para **analisis de tiempo de CPU**, **seguimiento de memoria** y **deteccion de fugas**. El perfilador ayuda a identificar cuellos de botella de rendimiento y problemas de memoria en tus programas.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [Inicio Rapido](#inicio-rapido)
- [Modos de Perfilado](#modos-de-perfilado)
- [Formatos de Salida](#formatos-de-salida)
- [Deteccion de Fugas](#deteccion-de-fugas)
- [Entendiendo los Reportes](#entendiendo-los-reportes)
- [Generacion de Flamegraph](#generacion-de-flamegraph)
- [Mejores Practicas](#mejores-practicas)

---

## Vision General

El perfilador se accede via el subcomando `profile`:

```bash
hemlock profile [OPTIONS] <FILE>
```

**Caracteristicas clave:**
- **Perfilado de CPU** - Medir tiempo gastado en cada funcion (tiempo propio y tiempo total)
- **Perfilado de memoria** - Rastrear todas las asignaciones con ubicaciones de codigo fuente
- **Deteccion de fugas** - Identificar memoria que nunca fue liberada
- **Multiples formatos de salida** - Texto, JSON y salida compatible con flamegraph
- **Estadisticas de memoria por funcion** - Ver que funciones asignan mas memoria

---

## Inicio Rapido

### Perfilar tiempo de CPU (por defecto)

```bash
hemlock profile script.hml
```

### Perfilar asignaciones de memoria

```bash
hemlock profile --memory script.hml
```

### Detectar fugas de memoria

```bash
hemlock profile --leaks script.hml
```

### Generar datos de flamegraph

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## Modos de Perfilado

### Perfilado de CPU (por defecto)

Mide el tiempo gastado en cada funcion, distinguiendo entre:
- **Tiempo propio** - Tiempo gastado ejecutando el codigo propio de la funcion
- **Tiempo total** - Tiempo propio mas tiempo gastado en funciones llamadas

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # Explicito
```

**Ejemplo de salida:**
```
=== Hemlock Profiler Report ===

Total time: 1.234ms
Functions called: 5 unique

--- Top 5 by Self Time ---

Function                        Self      Total   Calls
--------                        ----      -----   -----
expensive_calc              0.892ms    0.892ms     100  (72.3%)
process_data                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### Perfilado de Memoria

Rastrea todas las asignaciones de memoria (`alloc`, `buffer`, `talloc`, `realloc`) con ubicaciones de codigo fuente.

```bash
hemlock profile --memory script.hml
```

**Ejemplo de salida:**
```
=== Hemlock Profiler Report ===

Total time: 0.543ms
Functions called: 3 unique
Total allocations: 15 (4.2KB)

--- Top 3 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
allocator                   0.312ms    0.312ms      10      3.2KB         10  (57.5%)
buffer_ops                  0.156ms    0.156ms       5       1KB          5  (28.7%)
main                        0.075ms    0.543ms       1        0B          0  (13.8%)

--- Top 10 Allocation Sites ---

Location                                      Total    Count
--------                                      -----    -----
src/data.hml:42                               1.5KB        5
src/data.hml:67                               1.0KB       10
src/main.hml:15                               512B         1
```

---

### Modo de Conteo de Llamadas

Modo de sobrecarga minima que solo cuenta llamadas a funciones (sin tiempos).

```bash
hemlock profile --calls script.hml
```

---

## Formatos de Salida

### Texto (por defecto)

Resumen legible por humanos con tablas.

```bash
hemlock profile script.hml
```

---

### JSON

Formato legible por maquina para integracion con otras herramientas.

```bash
hemlock profile --json script.hml
```

**Ejemplo de salida:**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "expensive_calc",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### Flamegraph

Genera formato de pila colapsada compatible con [flamegraph.pl](https://github.com/brendangregg/FlameGraph).

```bash
hemlock profile --flamegraph script.hml > profile.folded

# Generar SVG con flamegraph.pl
flamegraph.pl profile.folded > profile.svg
```

**Ejemplo de salida colapsada:**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## Deteccion de Fugas

El flag `--leaks` muestra solo asignaciones que nunca fueron liberadas, haciendo facil identificar fugas de memoria.

```bash
hemlock profile --leaks script.hml
```

**Programa de ejemplo con fugas:**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // Fuga - nunca liberado
    let p2 = alloc(200);    // OK - liberado abajo
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // Correctamente liberado
}

leaky();
clean();
```

**Salida con --leaks:**
```
=== Hemlock Profiler Report ===

Total time: 0.034ms
Functions called: 2 unique
Total allocations: 3 (388B)

--- Top 2 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
leaky                       0.021ms    0.021ms       1       300B          2  (61.8%)
clean                       0.013ms    0.013ms       1        88B          1  (38.2%)

--- Memory Leaks (1 site) ---

Location                                     Leaked      Total    Count
--------                                     ------      -----    -----
script.hml:2                                   100B       100B        1
```

El reporte de fugas muestra:
- **Leaked** - Bytes actualmente sin liberar al terminar el programa
- **Total** - Total de bytes alguna vez asignados en este sitio
- **Count** - Numero de asignaciones en este sitio

---

## Entendiendo los Reportes

### Estadisticas de Funcion

| Columna | Descripcion |
|---------|-------------|
| Function | Nombre de funcion |
| Self | Tiempo en funcion excluyendo funciones llamadas |
| Total | Tiempo incluyendo todas las funciones llamadas |
| Calls | Numero de veces que la funcion fue llamada |
| Alloc | Total de bytes asignados por esta funcion |
| Count | Numero de asignaciones por esta funcion |
| (%) | Porcentaje del tiempo total del programa |

### Sitios de Asignacion

| Columna | Descripcion |
|---------|-------------|
| Location | Archivo fuente y numero de linea |
| Total | Total de bytes asignados en esta ubicacion |
| Count | Numero de asignaciones |
| Leaked | Bytes todavia asignados al terminar el programa (solo --leaks) |

### Unidades de Tiempo

El perfilador selecciona automaticamente unidades apropiadas:
- `ns` - Nanosegundos (< 1us)
- `us` - Microsegundos (< 1ms)
- `ms` - Milisegundos (< 1s)
- `s` - Segundos

---

## Referencia de Comandos

```
hemlock profile [OPTIONS] <FILE>

OPTIONS:
    --cpu           Perfilado de CPU/tiempo (por defecto)
    --memory        Perfilado de asignacion de memoria
    --calls         Solo conteo de llamadas (sobrecarga minima)
    --leaks         Mostrar solo asignaciones sin liberar (implica --memory)
    --json          Salida en formato JSON
    --flamegraph    Salida en formato compatible con flamegraph
    --top N         Mostrar top N entradas (por defecto: 20)
```

---

## Generacion de Flamegraph

Los flamegraphs visualizan donde tu programa pasa tiempo, con barras mas anchas indicando mas tiempo gastado.

### Generar un Flamegraph

1. Instalar flamegraph.pl:
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. Perfilar tu programa:
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. Generar SVG:
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. Abrir `profile.svg` en un navegador para una visualizacion interactiva.

### Leyendo Flamegraphs

- **Eje X**: Porcentaje de tiempo total (ancho = proporcion de tiempo)
- **Eje Y**: Profundidad de pila de llamadas (abajo = punto de entrada, arriba = funciones hoja)
- **Color**: Aleatorio, solo para distincion visual
- **Click**: Hacer zoom en una funcion para ver sus funciones llamadas

---

## Mejores Practicas

### 1. Perfilar Cargas de Trabajo Representativas

Perfilar con datos y patrones de uso realistas. Casos de prueba pequenos pueden no revelar cuellos de botella reales.

```bash
# Bueno: Perfilar con datos similares a produccion
hemlock profile --memory process_large_file.hml large_input.txt

# Menos util: Caso de prueba pequeno
hemlock profile quick_test.hml
```

### 2. Usar --leaks Durante Desarrollo

Ejecutar deteccion de fugas regularmente para detectar fugas de memoria temprano:

```bash
hemlock profile --leaks my_program.hml
```

### 3. Comparar Antes y Despues

Perfilar antes y despues de optimizaciones para medir impacto:

```bash
# Antes de optimizacion
hemlock profile --json script.hml > before.json

# Despues de optimizacion
hemlock profile --json script.hml > after.json

# Comparar resultados
```

### 4. Usar --top para Programas Grandes

Limitar salida para enfocarse en las funciones mas significativas:

```bash
hemlock profile --top 10 large_program.hml
```

### 5. Combinar con Flamegraphs

Para patrones de llamada complejos, los flamegraphs proporcionan mejor visualizacion que salida de texto:

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## Sobrecarga del Perfilador

El perfilador agrega algo de sobrecarga a la ejecucion del programa:

| Modo | Sobrecarga | Caso de Uso |
|------|------------|-------------|
| `--calls` | Minima | Solo contar llamadas a funciones |
| `--cpu` | Baja | Perfilado de rendimiento general |
| `--memory` | Moderada | Analisis de memoria y deteccion de fugas |

Para resultados mas precisos, perfilar multiples veces y buscar patrones consistentes.

---

## Ver Tambien

- [Gestion de Memoria](../language-guide/memory.md) - Punteros y buffers
- [API de Memoria](../reference/memory-api.md) - Funciones alloc, free, buffer
- [Async/Concurrencia](async-concurrency.md) - Perfilando codigo async
