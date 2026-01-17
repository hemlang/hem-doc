# Referencia de Comandos

Referencia completa de todos los comandos de hpm.

## Opciones Globales

Estas opciones funcionan con cualquier comando:

| Opcion | Descripcion |
|--------|-------------|
| `--help`, `-h` | Mostrar mensaje de ayuda |
| `--version`, `-v` | Mostrar version de hpm |
| `--verbose` | Mostrar salida detallada |

## Comandos

### hpm init

Crea un nuevo archivo `package.json`.

```bash
hpm init        # Modo interactivo
hpm init --yes  # Aceptar todos los valores por defecto
hpm init -y     # Forma corta
```

**Opciones:**

| Opcion | Descripcion |
|--------|-------------|
| `--yes`, `-y` | Aceptar valores por defecto para todas las preguntas |

**Preguntas interactivas:**
- Nombre del paquete (formato owner/repo)
- Version (por defecto: 1.0.0)
- Descripcion
- Autor
- Licencia (por defecto: MIT)
- Archivo principal (por defecto: src/index.hml)

**Ejemplo:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Instala dependencias o agrega nuevos paquetes.

```bash
hpm install                           # Instalar todo desde package.json
hpm install owner/repo                # Agregar e instalar paquete
hpm install owner/repo@^1.0.0        # Con restriccion de version
hpm install owner/repo --dev         # Como dependencia de desarrollo
hpm i owner/repo                      # Forma corta
```

**Opciones:**

| Opcion | Descripcion |
|--------|-------------|
| `--dev`, `-D` | Agregar a devDependencies |
| `--verbose` | Mostrar progreso detallado |
| `--dry-run` | Vista previa sin instalar |
| `--offline` | Instalar solo desde cache (sin red) |
| `--parallel` | Habilitar descargas paralelas (experimental) |

**Sintaxis de restriccion de version:**

| Sintaxis | Ejemplo | Significado |
|----------|---------|-------------|
| (ninguna) | `owner/repo` | Ultima version |
| Exacta | `owner/repo@1.2.3` | Exactamente 1.2.3 |
| Caret | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Rango | `owner/repo@>=1.0.0` | Al menos 1.0.0 |

**Ejemplos:**

```bash
# Instalar todas las dependencias
hpm install

# Instalar paquete especifico
hpm install hemlang/json

# Instalar con restriccion de version
hpm install hemlang/sprout@^2.0.0

# Instalar como dependencia de desarrollo
hpm install hemlang/test-utils --dev

# Vista previa de lo que se instalaria
hpm install hemlang/sprout --dry-run

# Salida detallada
hpm install --verbose

# Instalar solo desde cache (sin conexion)
hpm install --offline
```

**Salida:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Elimina un paquete.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Forma corta
hpm remove owner/repo      # Alternativa
```

**Ejemplos:**

```bash
hpm uninstall hemlang/sprout
```

**Salida:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Actualiza paquetes a las ultimas versiones dentro de las restricciones.

```bash
hpm update              # Actualizar todos los paquetes
hpm update owner/repo   # Actualizar paquete especifico
hpm up owner/repo       # Forma corta
```

**Opciones:**

| Opcion | Descripcion |
|--------|-------------|
| `--verbose` | Mostrar progreso detallado |
| `--dry-run` | Vista previa sin actualizar |

**Ejemplos:**

```bash
# Actualizar todos los paquetes
hpm update

# Actualizar paquete especifico
hpm update hemlang/sprout

# Vista previa de actualizaciones
hpm update --dry-run
```

**Salida:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Muestra los paquetes instalados.

```bash
hpm list              # Mostrar arbol completo de dependencias
hpm list --depth=0    # Solo dependencias directas
hpm list --depth=1    # Un nivel de dependencias transitivas
hpm ls                # Forma corta
```

**Opciones:**

| Opcion | Descripcion |
|--------|-------------|
| `--depth=N` | Limitar profundidad del arbol (por defecto: todo) |

**Ejemplos:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Muestra los paquetes con versiones mas nuevas disponibles.

```bash
hpm outdated
```

**Salida:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: Version instalada
- **Wanted**: Version mas alta que coincide con la restriccion
- **Latest**: Ultima version disponible

---

### hpm run

Ejecuta un script desde package.json.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Ejemplos:**

Dado este package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Ejecutar scripts:

```bash
hpm run start
hpm run test
hpm run build

# Pasar argumentos al script
hpm run test -- --verbose
```

---

### hpm test

Atajo para `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Equivalente a:

```bash
hpm run test
```

---

### hpm why

Explica por que un paquete esta instalado (muestra la cadena de dependencias).

```bash
hpm why owner/repo
```

**Ejemplo:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Administra la cache global de paquetes.

```bash
hpm cache list    # Listar paquetes en cache
hpm cache clean   # Limpiar todos los paquetes en cache
```

**Subcomandos:**

| Subcomando | Descripcion |
|------------|-------------|
| `list` | Mostrar todos los paquetes en cache y sus tamanos |
| `clean` | Eliminar todos los paquetes en cache |

**Ejemplos:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Atajos de Comandos

Por conveniencia, varios comandos tienen alias cortos:

| Comando | Atajos |
|---------|--------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Ejemplos:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Codigos de Salida

hpm usa codigos de salida especificos para indicar diferentes condiciones de error:

| Codigo | Significado |
|--------|-------------|
| 0 | Exito |
| 1 | Conflicto de dependencias |
| 2 | Paquete no encontrado |
| 3 | Version no encontrada |
| 4 | Error de red |
| 5 | package.json invalido |
| 6 | Verificacion de integridad fallida |
| 7 | Limite de tasa de GitHub excedido |
| 8 | Dependencia circular |

Usa codigos de salida en scripts:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## Variables de Entorno

hpm respeta estas variables de entorno:

| Variable | Descripcion |
|----------|-------------|
| `GITHUB_TOKEN` | Token de API de GitHub para autenticacion |
| `HPM_CACHE_DIR` | Sobrescribir ubicacion del directorio de cache |
| `HOME` | Directorio home del usuario (para config/cache) |

**Ejemplos:**

```bash
# Usar token de GitHub para mayores limites de tasa
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Usar directorio de cache personalizado
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## Ver Tambien

- [Configuracion](configuration.md) - Archivos de configuracion
- [Especificacion de Paquetes](package-spec.md) - formato de package.json
- [Solucion de Problemas](troubleshooting.md) - Problemas comunes
