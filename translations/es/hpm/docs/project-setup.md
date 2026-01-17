# Configuracion del Proyecto

Guia completa para configurar proyectos Hemlock con hpm.

## Iniciar un Nuevo Proyecto

### Configuracion Basica

Crea un nuevo proyecto desde cero:

```bash
# Crear directorio del proyecto
mkdir my-project
cd my-project

# Inicializar package.json
hpm init

# Crear estructura de directorios
mkdir -p src test
```

### Plantillas de Proyecto

Aqui hay estructuras de proyecto comunes para diferentes casos de uso:

#### Paquete de Biblioteca

Para bibliotecas reutilizables:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Entrada principal, exporta API publica
│   ├── core.hml           # Funcionalidad principal
│   ├── utils.hml          # Funciones utilitarias
│   └── types.hml          # Definiciones de tipos
└── test/
    ├── framework.hml      # Framework de pruebas
    ├── run.hml            # Ejecutor de pruebas
    └── test_core.hml      # Pruebas
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Aplicacion

Para aplicaciones independientes:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Punto de entrada de la aplicacion
│   ├── config.hml         # Configuracion
│   ├── commands/          # Comandos CLI
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Bibliotecas internas
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Archivos de datos
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Aplicacion Web

Para servidores web:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Punto de entrada del servidor
│   ├── routes/            # Manejadores de rutas
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Modelos de datos
│   │   └── user.hml
│   └── services/          # Logica de negocio
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Archivos estaticos
│   ├── css/
│   └── js/
└── views/                 # Plantillas
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## El Archivo package.json

### Campos Requeridos

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### Todos los Campos

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
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

### Referencia de Campos

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `name` | string | Nombre del paquete en formato owner/repo (requerido) |
| `version` | string | Version semantica (requerido) |
| `description` | string | Descripcion corta |
| `author` | string | Nombre y email del autor |
| `license` | string | Identificador de licencia (MIT, Apache-2.0, etc.) |
| `repository` | string | URL del repositorio |
| `homepage` | string | Pagina principal del proyecto |
| `bugs` | string | URL del rastreador de problemas |
| `main` | string | Archivo de punto de entrada (por defecto: src/index.hml) |
| `keywords` | array | Palabras clave de busqueda |
| `dependencies` | object | Dependencias de tiempo de ejecucion |
| `devDependencies` | object | Dependencias de desarrollo |
| `scripts` | object | Scripts con nombre |
| `files` | array | Archivos a incluir al publicar |
| `native` | object | Requisitos de bibliotecas nativas |

## El Archivo package-lock.json

El archivo de bloqueo se genera automaticamente y debe incluirse en el control de versiones. Asegura instalaciones reproducibles.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Mejores Practicas del Archivo de Bloqueo

- **Incluye** package-lock.json en el control de versiones
- **No edites** manualmente - se genera automaticamente
- **Ejecuta `hpm install`** despues de hacer pull de cambios
- **Elimina y regenera** si esta corrupto:
  ```bash
  rm package-lock.json
  hpm install
  ```

## El Directorio hem_modules

Los paquetes instalados se almacenan en `hem_modules/`:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### Mejores Practicas de hem_modules

- **Agregar a .gitignore** - no incluir dependencias en commits
- **No modificar** - los cambios se sobrescribiran
- **Eliminar para reinstalar desde cero**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

.gitignore recomendado para proyectos Hemlock:

```gitignore
# Dependencies
hem_modules/

# Build output
dist/
*.hmlc

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local

# Test coverage
coverage/
```

## Trabajar con Dependencias

### Agregar Dependencias

```bash
# Agregar dependencia de tiempo de ejecucion
hpm install hemlang/json

# Agregar con restriccion de version
hpm install hemlang/sprout@^2.0.0

# Agregar dependencia de desarrollo
hpm install hemlang/test-utils --dev
```

### Importar Dependencias

```hemlock
// Import from package (uses "main" entry)
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { Router } from "hemlang/sprout/router";

// Import standard library
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Resolucion de Importaciones

hpm resuelve importaciones en este orden:

1. **Biblioteca estandar**: importaciones `@stdlib/*` cargan modulos integrados
2. **Raiz del paquete**: `owner/repo` usa el campo `main`
3. **Subruta**: `owner/repo/path` verifica:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Scripts

### Definir Scripts

Agrega scripts a package.json:

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

### Ejecutar Scripts

```bash
hpm run start
hpm run dev
hpm run build

# Atajo para test
hpm test

# Pasar argumentos
hpm run test -- --verbose --filter=unit
```

### Convenciones de Nombres de Scripts

| Script | Proposito |
|--------|-----------|
| `start` | Ejecutar la aplicacion |
| `dev` | Ejecutar en modo desarrollo |
| `test` | Ejecutar todas las pruebas |
| `build` | Compilar para produccion |
| `clean` | Eliminar archivos generados |
| `lint` | Verificar estilo de codigo |
| `format` | Formatear codigo |

## Flujo de Trabajo de Desarrollo

### Configuracion Inicial

```bash
# Clonar proyecto
git clone https://github.com/yourusername/my-project.git
cd my-project

# Instalar dependencias
hpm install

# Ejecutar pruebas
hpm test

# Iniciar desarrollo
hpm run dev
```

### Flujo de Trabajo Diario

```bash
# Obtener ultimos cambios
git pull

# Instalar cualquier nueva dependencia
hpm install

# Hacer cambios...

# Ejecutar pruebas
hpm test

# Commit
git add .
git commit -m "Add feature"
git push
```

### Agregar una Nueva Caracteristica

```bash
# Crear rama de caracteristica
git checkout -b feature/new-feature

# Agregar nueva dependencia si es necesario
hpm install hemlang/new-lib

# Implementar caracteristica...

# Probar
hpm test

# Commit y push
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## Configuracion Especifica del Entorno

### Usar Variables de Entorno

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### Archivo de Configuracion

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## Ver Tambien

- [Inicio Rapido](quick-start.md) - Comenzar rapidamente
- [Comandos](commands.md) - Referencia de comandos
- [Creacion de Paquetes](creating-packages.md) - Publicar paquetes
- [Configuracion](configuration.md) - Configuracion de hpm
