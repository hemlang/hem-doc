# Especificacion de Paquetes

Referencia completa para el formato del archivo `package.json`.

## Descripcion General

Cada paquete de hpm requiere un archivo `package.json` en la raiz del proyecto. Este archivo define los metadatos del paquete, dependencias y scripts.

## Ejemplo Minimo

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Ejemplo Completo

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

## Referencia de Campos

### name (requerido)

El nombre del paquete en formato `owner/repo`.

```json
{
  "name": "hemlang/sprout"
}
```

**Requisitos:**
- Debe estar en formato `owner/repo`
- `owner` debe ser tu nombre de usuario u organizacion de GitHub
- `repo` debe ser el nombre del repositorio
- Usa letras minusculas, numeros y guiones
- Maximo 214 caracteres en total

**Nombres validos:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Nombres invalidos:**
```
my-package          # Falta owner
hemlang/My_Package  # Mayusculas y guion bajo
hemlang             # Falta repo
```

### version (requerido)

La version del paquete siguiendo [Versionado Semantico](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Formato:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Versiones validas:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Descripcion corta del paquete.

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- Mantenla bajo 200 caracteres
- Describe lo que hace el paquete, no como

### author

Informacion del autor del paquete.

```json
{
  "author": "Your Name <email@example.com>"
}
```

**Formatos aceptados:**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

El identificador de licencia.

```json
{
  "license": "MIT"
}
```

**Licencias comunes:**
- `MIT` - Licencia MIT
- `Apache-2.0` - Licencia Apache 2.0
- `GPL-3.0` - Licencia Publica General GNU v3.0
- `BSD-3-Clause` - Licencia BSD de 3 clausulas
- `ISC` - Licencia ISC
- `UNLICENSED` - Propietario/privado

Usa [identificadores SPDX](https://spdx.org/licenses/) cuando sea posible.

### repository

Enlace al repositorio de codigo fuente.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

URL de la pagina principal del proyecto.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

URL del rastreador de problemas.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Archivo de punto de entrada para el paquete.

```json
{
  "main": "src/index.hml"
}
```

**Por defecto:** `src/index.hml`

Cuando los usuarios importan tu paquete:
```hemlock
import { x } from "owner/repo";
```

hpm carga el archivo especificado en `main`.

**Orden de resolucion para importaciones:**
1. Ruta exacta: `src/index.hml`
2. Con extension .hml: `src/index` → `src/index.hml`
3. Archivo index: `src/index/` → `src/index/index.hml`

### keywords

Array de palabras clave para descubrimiento.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Usa minusculas
- Se especifico y relevante
- Incluye el lenguaje ("hemlock") si es apropiado

### dependencies

Dependencias de tiempo de ejecucion requeridas para que el paquete funcione.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Clave:** Nombre del paquete (`owner/repo`)
**Valor:** Restriccion de version

**Sintaxis de restriccion de version:**

| Restriccion | Significado |
|-------------|-------------|
| `1.2.3` | Version exacta |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Al menos 1.0.0 |
| `>=1.0.0 <2.0.0` | Rango |
| `*` | Cualquier version |

### devDependencies

Dependencias solo de desarrollo (pruebas, compilacion, etc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Las dependencias de desarrollo son:
- Instaladas durante el desarrollo
- No instaladas cuando el paquete se usa como dependencia
- Usadas para pruebas, compilacion, linting, etc.

### scripts

Comandos con nombre que se pueden ejecutar con `hpm run`.

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

**Ejecutar scripts:**
```bash
hpm run start
hpm run build
hpm test        # Atajo para 'hpm run test'
```

**Pasar argumentos:**
```bash
hpm run test -- --verbose --filter=unit
```

**Scripts comunes:**

| Script | Proposito |
|--------|-----------|
| `start` | Iniciar la aplicacion |
| `dev` | Modo desarrollo con recarga en caliente |
| `test` | Ejecutar pruebas |
| `build` | Compilar para produccion |
| `clean` | Eliminar artefactos de compilacion |
| `lint` | Verificar estilo de codigo |
| `format` | Formatear codigo |

### files

Archivos y directorios a incluir cuando el paquete se instala.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Comportamiento por defecto:** Si no se especifica, incluye:
- Todos los archivos en el repositorio
- Excluye `.git/`, `node_modules/`, `hem_modules/`

**Usar para:**
- Reducir el tamano del paquete
- Excluir archivos de prueba de la distribucion
- Incluir solo archivos necesarios

### native

Requisitos de bibliotecas nativas.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Documenta dependencias nativas que deben estar instaladas en el sistema.

## Validacion

hpm valida package.json en varias operaciones. Errores de validacion comunes:

### Campos requeridos faltantes

```
Error: package.json missing required field: name
```

**Solucion:** Agregar el campo requerido.

### Formato de nombre invalido

```
Error: Invalid package name. Must be in owner/repo format.
```

**Solucion:** Usar formato `owner/repo`.

### Version invalida

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Solucion:** Usar formato semver completo (`1.0.0`).

### JSON invalido

```
Error: package.json is not valid JSON
```

**Solucion:** Verificar sintaxis JSON (comas, comillas, corchetes).

## Crear package.json

### Interactivo

```bash
hpm init
```

Solicita cada campo de forma interactiva.

### Con Valores por Defecto

```bash
hpm init --yes
```

Crea con valores por defecto:
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Manual

Crea el archivo manualmente:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Mejores Practicas

1. **Siempre especifica main** - No dependas del valor por defecto
2. **Usa rangos caret** - `^1.0.0` para la mayoria de dependencias
3. **Separa dependencias de desarrollo** - Mantener dependencias de prueba/compilacion en devDependencies
4. **Incluye palabras clave** - Ayuda a los usuarios a encontrar tu paquete
5. **Documenta scripts** - Nombra los scripts claramente
6. **Especifica licencia** - Requerido para codigo abierto
7. **Agrega descripcion** - Ayuda a los usuarios a entender el proposito

## Ver Tambien

- [Creacion de Paquetes](creating-packages.md) - Guia de publicacion
- [Versionado](versioning.md) - Restricciones de version
- [Configuracion del Proyecto](project-setup.md) - Estructura del proyecto
