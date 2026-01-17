# Creacion de Paquetes

Esta guia cubre como crear, estructurar y publicar paquetes Hemlock.

## Descripcion General

hpm usa GitHub como su registro de paquetes. Los paquetes se identifican por su ruta `owner/repo` de GitHub, y las versiones son etiquetas de Git. Publicar es simplemente enviar una version etiquetada.

## Crear un Nuevo Paquete

### 1. Inicializar el Paquete

Crea un nuevo directorio e inicializa:

```bash
mkdir my-package
cd my-package
hpm init
```

Responde las preguntas:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Crear la Estructura del Proyecto

Estructura recomendada para paquetes:

```
my-package/
├── package.json          # Manifiesto del paquete
├── README.md             # Documentacion
├── LICENSE               # Archivo de licencia
├── src/
│   ├── index.hml         # Punto de entrada principal (exporta API publica)
│   ├── utils.hml         # Utilidades internas
│   └── types.hml         # Definiciones de tipos
└── test/
    ├── framework.hml     # Framework de pruebas
    └── test_utils.hml    # Pruebas
```

### 3. Definir Tu API Publica

**src/index.hml** - Punto de entrada principal:

```hemlock
// Re-export public API
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Direct exports
export fn create(options: Options): Config {
    // Implementation
}

export fn validate(config: Config): bool {
    // Implementation
}
```

### 4. Escribir Tu package.json

Ejemplo completo de package.json:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Nomenclatura de Paquetes

### Requisitos

- Debe estar en formato `owner/repo`
- `owner` debe ser tu nombre de usuario u organizacion de GitHub
- `repo` debe ser el nombre del repositorio
- Usa minusculas con guiones para nombres de varias palabras

### Buenos Nombres

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### Evitar

```
my-package          # Falta owner
alice/MyPackage     # PascalCase
alice/my_package    # Guiones bajos
```

## Mejores Practicas de Estructura de Paquetes

### Punto de Entrada

El campo `main` en package.json especifica el punto de entrada:

```json
{
  "main": "src/index.hml"
}
```

Este archivo debe exportar tu API publica:

```hemlock
// Export everything users need
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Types
export type { Config, Options } from "./types.hml";
```

### Interno vs Publico

Mantener los detalles de implementacion interna privados:

```
src/
├── index.hml          # Publico: API exportada
├── parser.hml         # Publico: usado por index.hml
├── formatter.hml      # Publico: usado por index.hml
└── internal/
    ├── helpers.hml    # Privado: solo uso interno
    └── constants.hml  # Privado: solo uso interno
```

Los usuarios importan desde la raiz de tu paquete:

```hemlock
// Bien - importa desde API publica
import { parse, Parser } from "yourusername/my-package";

// Tambien funciona - importacion de subruta
import { validate } from "yourusername/my-package/validator";

// Desaconsejado - acceder a internos
import { helper } from "yourusername/my-package/internal/helpers";
```

### Exportaciones de Subrutas

Soportar importacion desde subrutas:

```
src/
├── index.hml              # Entrada principal
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Los usuarios pueden importar:

```hemlock
import { parse } from "yourusername/my-package";           # Principal
import { Parser } from "yourusername/my-package/parser";   # Subruta
import { format } from "yourusername/my-package/formatter";
```

## Dependencias

### Agregar Dependencias

```bash
# Dependencia de tiempo de ejecucion
hpm install hemlang/json

# Dependencia de desarrollo
hpm install hemlang/test-utils --dev
```

### Mejores Practicas de Dependencias

1. **Usar rangos caret** para la mayoria de dependencias:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Fijar versiones** solo cuando sea necesario (inestabilidad de API):
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Evitar rangos demasiado restrictivos**:
   ```json
   // Malo: demasiado restrictivo
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Bueno: permite actualizaciones compatibles
   "hemlang/json": "^1.2.3"
   ```

4. **Separar dependencias de desarrollo**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Probar Tu Paquete

### Escribir Pruebas

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Ejecutar Pruebas

Agrega un script de pruebas:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Ejecuta con:

```bash
hpm test
```

## Publicacion

### Prerrequisitos

1. Crear un repositorio en GitHub que coincida con el nombre de tu paquete
2. Asegurar que `package.json` este completo y sea valido
3. Todas las pruebas pasan

### Proceso de Publicacion

Publicar es simplemente enviar una etiqueta de Git:

```bash
# 1. Asegurar que todo este confirmado
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Crear una etiqueta de version (debe comenzar con 'v')
git tag v1.0.0

# 3. Enviar codigo y etiquetas
git push origin main
git push origin v1.0.0
# O enviar todas las etiquetas a la vez
git push origin main --tags
```

### Etiquetas de Version

Las etiquetas deben seguir el formato `vX.Y.Z`:

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Parche
git tag v1.1.0      # Menor
git tag v2.0.0      # Mayor
git tag v1.0.0-beta.1  # Pre-release
```

### Lista de Verificacion de Lanzamiento

Antes de publicar una nueva version:

1. **Actualizar version** en package.json
2. **Ejecutar pruebas**: `hpm test`
3. **Actualizar CHANGELOG** (si tienes uno)
4. **Actualizar README** si la API cambio
5. **Confirmar cambios**
6. **Crear etiqueta**
7. **Enviar a GitHub**

### Ejemplo Automatizado

Crea un script de lanzamiento:

```bash
#!/bin/bash
# release.sh - Release a new version

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Run tests
hpm test || exit 1

# Update version in package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Commit and tag
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Push
git push origin main --tags

echo "Released v$VERSION"
```

## Usuarios Instalando Tu Paquete

Despues de publicar, los usuarios pueden instalar:

```bash
# Ultima version
hpm install yourusername/my-package

# Version especifica
hpm install yourusername/my-package@1.0.0

# Restriccion de version
hpm install yourusername/my-package@^1.0.0
```

E importar:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Documentacion

### README.md

Cada paquete debe tener un README:

```markdown
# my-package

A brief description of what this package does.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Usage

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Parses the input string.

### stringify(obj: any): string

Converts object to string.

## License

MIT
```

### Documentacion de API

Documenta todas las exportaciones publicas:

```hemlock
/// Parses the input string into a structured Result.
///
/// # Arguments
/// * `input` - The string to parse
///
/// # Returns
/// A Result containing the parsed data or an error
///
/// # Example
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementation
}
```

## Directrices de Versionado

Sigue [Versionado Semantico](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Cambios incompatibles
- **MINOR** (1.0.0 → 1.1.0): Nuevas caracteristicas, compatibles hacia atras
- **PATCH** (1.0.0 → 1.0.1): Correcciones de errores, compatibles hacia atras

### Cuando Incrementar

| Tipo de Cambio | Incremento de Version |
|----------------|----------------------|
| Cambio de API incompatible | MAJOR |
| Eliminar funcion/tipo | MAJOR |
| Cambiar firma de funcion | MAJOR |
| Agregar nueva funcion | MINOR |
| Agregar nueva caracteristica | MINOR |
| Correccion de error | PATCH |
| Actualizacion de documentacion | PATCH |
| Refactorizacion interna | PATCH |

## Ver Tambien

- [Especificacion de Paquetes](package-spec.md) - Referencia completa de package.json
- [Versionado](versioning.md) - Detalles de versionado semantico
- [Configuracion](configuration.md) - Autenticacion de GitHub
