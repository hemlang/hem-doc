# Inicio Rapido

Comienza a trabajar con hpm en 5 minutos.

## Instalar hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Para mas opciones de instalacion, consulta la [Guia de Instalacion](installation.md).

## Crear un Nuevo Proyecto

Comienza creando un nuevo directorio e inicializando un paquete:

```bash
mkdir my-project
cd my-project
hpm init
```

Se te solicitaran los detalles del proyecto:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Usa `--yes` para aceptar todos los valores por defecto:

```bash
hpm init --yes
```

## Estructura del Proyecto

Crea la estructura basica del proyecto:

```
my-project/
├── package.json        # Manifiesto del proyecto
├── src/
│   └── index.hml      # Punto de entrada principal
└── test/
    └── test.hml       # Pruebas
```

Crea tu archivo principal:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Main entry point
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## Instalar Dependencias

Busca paquetes en GitHub (los paquetes usan el formato `owner/repo`):

```bash
# Instalar un paquete
hpm install hemlang/sprout

# Instalar con restriccion de version
hpm install hemlang/json@^1.0.0

# Instalar como dependencia de desarrollo
hpm install hemlang/test-utils --dev
```

Despues de la instalacion, la estructura de tu proyecto incluye `hem_modules/`:

```
my-project/
├── package.json
├── package-lock.json   # Archivo de bloqueo (auto-generado)
├── hem_modules/        # Paquetes instalados
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Usar Paquetes Instalados

Importa paquetes usando su ruta de GitHub:

```hemlock
// Import from installed package
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { middleware } from "hemlang/sprout/middleware";

// Standard library (built-in)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Agregar Scripts

Agrega scripts a tu `package.json`:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Ejecuta scripts con `hpm run`:

```bash
hpm run start
hpm run build

# Atajo para test
hpm test
```

## Flujos de Trabajo Comunes

### Instalar Todas las Dependencias

Cuando clonas un proyecto con un `package.json`:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Actualizar Dependencias

Actualiza todos los paquetes a las ultimas versiones dentro de las restricciones:

```bash
hpm update
```

Actualiza un paquete especifico:

```bash
hpm update hemlang/sprout
```

### Ver Paquetes Instalados

Lista todos los paquetes instalados:

```bash
hpm list
```

La salida muestra el arbol de dependencias:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Verificar Actualizaciones

Ve que paquetes tienen versiones mas nuevas:

```bash
hpm outdated
```

### Eliminar un Paquete

```bash
hpm uninstall hemlang/sprout
```

## Ejemplo: Aplicacion Web

Aqui hay un ejemplo completo usando un framework web:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

Ejecuta la aplicacion:

```bash
hpm install
hpm run start
```

## Proximos Pasos

- [Referencia de Comandos](commands.md) - Aprende todos los comandos de hpm
- [Creacion de Paquetes](creating-packages.md) - Publica tus propios paquetes
- [Configuracion](configuration.md) - Configura hpm y tokens de GitHub
- [Configuracion del Proyecto](project-setup.md) - Configuracion detallada del proyecto
