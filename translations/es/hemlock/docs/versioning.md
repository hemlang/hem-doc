# Versionado de Hemlock

Este documento describe la estrategia de versionado para Hemlock.

## Formato de Version

Hemlock usa **Versionado Semantico** (SemVer):

```
MAJOR.MINOR.PATCH
```

| Componente | Cuando Incrementar |
|-----------|-------------------|
| **MAJOR** | Cambios incompatibles en la semantica del lenguaje, API de stdlib o formatos binarios |
| **MINOR** | Nuevas funcionalidades, adiciones compatibles hacia atras |
| **PATCH** | Correcciones de errores, mejoras de rendimiento, documentacion |

## Versionado Unificado

Todos los componentes de Hemlock comparten un **unico numero de version**:

- **Interprete** (`hemlock`)
- **Compilador** (`hemlockc`)
- **Servidor LSP** (`hemlock --lsp`)
- **Biblioteca Estandar** (`@stdlib/*`)

La version se define en `include/version.h`:

```c
#define HEMLOCK_VERSION_MAJOR 1
#define HEMLOCK_VERSION_MINOR 8
#define HEMLOCK_VERSION_PATCH 7

#define HEMLOCK_VERSION "1.8.7"
```

### Verificar Versiones

```bash
# Version del interprete
hemlock --version

# Version del compilador
hemlockc --version
```

## Garantias de Compatibilidad

### Dentro de una Version MAJOR

- El codigo fuente que funciona en `1.x.0` funcionara en `1.x.y` (cualquier patch)
- El codigo fuente que funciona en `1.0.x` funcionara en `1.y.z` (cualquier minor/patch)
- Los bundles compilados `.hmlb` son compatibles dentro de la misma version MAJOR
- Las APIs de la biblioteca estandar son estables (solo adiciones, sin eliminaciones)

### Entre Versiones MAJOR

- Los cambios incompatibles se documentan en las notas de lanzamiento
- Se proporcionan guias de migracion para cambios significativos
- Las funcionalidades obsoletas se advierten durante al menos una version minor antes de su eliminacion

## Versionado de Formato Binario

Hemlock usa numeros de version separados para los formatos binarios:

| Formato | Version | Ubicacion |
|--------|---------|----------|
| `.hmlc` (bundle AST) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (bundle comprimido) | Igual que HMLC | Usa compresion zlib |
| `.hmlp` (ejecutable empaquetado) | Magic: `HMLP` | Formato auto-contenido |

Las versiones de formato binario se incrementan independientemente cuando cambia la serializacion.

## Versionado de la Biblioteca Estandar

La biblioteca estandar (`@stdlib/*`) se versiona **con el lanzamiento principal**:

```hemlock
// Always uses the stdlib bundled with your Hemlock installation
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Compatibilidad de Stdlib

- Se pueden agregar nuevos modulos en versiones MINOR
- Se pueden agregar nuevas funciones a modulos existentes en versiones MINOR
- Las firmas de funciones son estables dentro de una version MAJOR
- Las funciones obsoletas se marcan y documentan antes de su eliminacion

## Historial de Versiones

| Version | Fecha | Destacados |
|---------|------|------------|
| **1.8.7** | 2026 | Correccion de print/eprint multi-argumento en codegen del compilador |
| **1.8.6** | 2026 | Correccion de segfault en hml_string_append_inplace para strings SSO |
| **1.8.5** | 2026 | 5 nuevos metodos de array (every, some, indexOf, sort, fill), optimizaciones de rendimiento importantes, correcciones de fugas de memoria |
| **1.8.4** | 2026 | Manejo elegante de palabras clave reservadas (def, func, var, class), correccion de pruebas CI intermitentes |
| **1.8.3** | 2026 | Pulido de codigo: consolidar numeros magicos, estandarizar mensajes de error |
| **1.8.2** | 2026 | Prevencion de fugas de memoria: eval seguro ante excepciones, limpieza de task/channel, correcciones del optimizador |
| **1.8.1** | 2026 | Correccion de bug use-after-free en manejo de valores de retorno de funciones |
| **1.8.0** | 2026 | Coincidencia de patrones, asignador arena, correcciones de fugas de memoria |
| **1.7.5** | 2026 | Correccion de bug de indentacion else-if en el formateador |
| **1.7.4** | 2026 | Mejoras del formateador: salto de linea en parametros de funcion, expr binaria, import y cadena de metodos |
| **1.7.3** | 2026 | Correccion de preservacion de comentarios y lineas en blanco en el formateador |
| **1.7.2** | 2026 | Version de mantenimiento |
| **1.7.1** | 2026 | Sentencias if/while/for de una sola linea (sintaxis sin llaves) |
| **1.7.0** | 2026 | Alias de tipos, tipos de funcion, parametros const, firmas de metodos, etiquetas de bucle, argumentos con nombre, coalescencia nula |
| **1.6.7** | 2026 | Literales octales, comentarios de bloque, escapes hex/unicode, separadores numericos |
| **1.6.6** | 2026 | Literales flotantes sin cero inicial, correccion de bug de reduccion de fuerza |
| **1.6.5** | 2026 | Correccion de sintaxis de bucle for-in sin palabra clave 'let' |
| **1.6.4** | 2026 | Version de correccion urgente |
| **1.6.3** | 2026 | Correccion de despacho de metodos en tiempo de ejecucion para tipos file, channel, socket |
| **1.6.2** | 2026 | Version de parche |
| **1.6.1** | 2026 | Version de parche |
| **1.6.0** | 2025 | Verificacion de tipos en tiempo de compilacion en hemlockc, integracion LSP, operadores bitwise compuestos (`&=`, `\|=`, `^=`, `<<=`, `>>=`, `%=`) |
| **1.5.0** | 2024 | Sistema de tipos completo, async/await, atomicos, 39 modulos stdlib, soporte de struct FFI, 99 pruebas de paridad |
| **1.3.0** | 2025 | Ambito de bloque lexico apropiado (semantica let/const tipo JS), clausuras por iteracion de bucle |
| **1.2.3** | 2025 | Sintaxis import star (`import * from`) |
| **1.2.2** | 2025 | Agregar soporte `export extern`, correcciones de pruebas multiplataforma |
| **1.2.1** | 2025 | Correccion de fallos en pruebas de macOS (generacion de clave RSA, enlaces simbolicos de directorio) |
| **1.2.0** | 2025 | Optimizador AST, builtin apply(), canales sin buffer, 7 nuevos modulos stdlib, 97 pruebas de paridad |
| **1.1.3** | 2025 | Actualizaciones de documentacion, correcciones de consistencia |
| **1.1.1** | 2025 | Correcciones de bugs y mejoras |
| **1.1.0** | 2024 | Versionado unificado en todos los componentes |
| **1.0.x** | 2024 | Serie de lanzamiento inicial |

## Proceso de Lanzamiento

1. Cambio de version en `include/version.h`
2. Actualizar changelog
3. Ejecutar suite de pruebas completa (`make test-all`)
4. Etiquetar lanzamiento en git
5. Compilar artefactos de lanzamiento

## Verificar Compatibilidad

Para verificar que tu codigo funciona con una version especifica de Hemlock:

```bash
# Ejecutar pruebas contra version instalada
make test

# Verificar paridad entre interprete y compilador
make parity
```

## Futuro: Manifiestos de Proyecto

Un lanzamiento futuro puede introducir manifiestos de proyecto opcionales para restricciones de version:

```hemlock
// Hypothetical project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

Esto aun no esta implementado pero es parte de la hoja de ruta.
