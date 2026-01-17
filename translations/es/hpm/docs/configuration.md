# Configuracion

Esta guia cubre todas las opciones de configuracion para hpm.

## Descripcion General

hpm puede configurarse a traves de:

1. **Variables de entorno** - Para configuraciones en tiempo de ejecucion
2. **Archivo de configuracion global** - `~/.hpm/config.json`
3. **Archivos del proyecto** - `package.json` y `package-lock.json`

## Variables de Entorno

### GITHUB_TOKEN

Token de API de GitHub para autenticacion.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Beneficios de la autenticacion:**
- Mayores limites de tasa de API (5000 vs 60 solicitudes/hora)
- Acceso a repositorios privados
- Resolucion de dependencias mas rapida

**Crear un token:**

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Haz clic en "Generate new token (classic)"
3. Selecciona los alcances:
   - `repo` - Para acceso a repositorios privados
   - `read:packages` - Para GitHub Packages (si se usa)
4. Genera y copia el token

### HPM_CACHE_DIR

Sobrescribe el directorio de cache por defecto.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

Por defecto: `~/.hpm/cache`

**Casos de uso:**
- Sistemas CI/CD con ubicaciones de cache personalizadas
- Cache compartida entre proyectos
- Cache temporal para compilaciones aisladas

### HOME

Directorio home del usuario. Se usa para ubicar:
- Directorio de configuracion: `$HOME/.hpm/`
- Directorio de cache: `$HOME/.hpm/cache/`

Normalmente establecido por el sistema; sobrescribe solo si es necesario.

### Ejemplo .bashrc / .zshrc

```bash
# GitHub authentication (recommended)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Custom cache location (optional)
# export HPM_CACHE_DIR=/path/to/cache

# Add hpm to PATH (if using custom install location)
export PATH="$HOME/.local/bin:$PATH"
```

## Archivo de Configuracion Global

### Ubicacion

`~/.hpm/config.json`

### Formato

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Crear el Archivo de Configuracion

```bash
# Crear directorio de configuracion
mkdir -p ~/.hpm

# Crear archivo de configuracion
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Asegurar el archivo (recomendado)
chmod 600 ~/.hpm/config.json
```

### Prioridad del Token

Si ambos estan establecidos, la variable de entorno tiene precedencia:

1. Variable de entorno `GITHUB_TOKEN` (mayor)
2. Campo `github_token` de `~/.hpm/config.json`
3. Sin autenticacion (por defecto)

## Estructura de Directorios

### Directorios Globales

```
~/.hpm/
├── config.json          # Configuracion global
└── cache/               # Cache de paquetes
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Directorios del Proyecto

```
my-project/
├── package.json         # Manifiesto del proyecto
├── package-lock.json    # Archivo de bloqueo de dependencias
├── hem_modules/         # Paquetes instalados
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Codigo fuente
└── test/                # Pruebas
```

## Cache de Paquetes

### Ubicacion

Por defecto: `~/.hpm/cache/`

Sobrescribir con: variable de entorno `HPM_CACHE_DIR`

### Estructura

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Administrar la Cache

```bash
# Ver paquetes en cache
hpm cache list

# Limpiar toda la cache
hpm cache clean
```

### Comportamiento de la Cache

- Los paquetes se almacenan en cache despues de la primera descarga
- Las instalaciones posteriores usan versiones en cache
- Usa `--offline` para instalar solo desde cache
- La cache se comparte entre todos los proyectos

## Limites de Tasa de API de GitHub

### Sin Autenticacion

- **60 solicitudes por hora** por direccion IP
- Compartido entre todos los usuarios no autenticados en la misma IP
- Se agota rapidamente en CI/CD o con muchas dependencias

### Con Autenticacion

- **5000 solicitudes por hora** por usuario autenticado
- Limite de tasa personal, no compartido

### Manejo de Limites de Tasa

hpm automaticamente:
- Reintenta con retroceso exponencial (1s, 2s, 4s, 8s)
- Reporta errores de limite de tasa con codigo de salida 7
- Sugiere autenticacion si se alcanza el limite

**Soluciones cuando se alcanza el limite:**

```bash
# Opcion 1: Autenticar con token de GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Opcion 2: Esperar a que se reinicie el limite de tasa
# (Los limites se reinician cada hora)

# Opcion 3: Usar modo sin conexion (si los paquetes estan en cache)
hpm install --offline
```

## Modo Sin Conexion

Instalar paquetes sin acceso a red:

```bash
hpm install --offline
```

**Requisitos:**
- Todos los paquetes deben estar en cache
- El archivo de bloqueo debe existir con versiones exactas

**Casos de uso:**
- Entornos aislados
- Compilaciones de CI/CD mas rapidas (con cache caliente)
- Evitar limites de tasa

## Configuracion de CI/CD

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Install Hemlock (adjust based on your setup)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copy package files first (for layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN hpm install

# Copy source code
COPY . .

# Run application
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Configuracion de Proxy

Para entornos detras de un proxy, configura a nivel de sistema:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Mejores Practicas de Seguridad

### Seguridad de Tokens

1. **Nunca envies tokens** al control de versiones
2. **Usa variables de entorno** en CI/CD
3. **Restringe los alcances de tokens** al minimo requerido
4. **Rota tokens** regularmente
5. **Asegura el archivo de configuracion**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Repositorios Privados

Para acceder a paquetes privados:

1. Crea un token con alcance `repo`
2. Configura la autenticacion (variable de entorno o archivo de configuracion)
3. Asegurate de que el token tenga acceso al repositorio

```bash
# Probar acceso
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Solucion de Problemas de Configuracion

### Verificar Configuracion

```bash
# Verificar si el token esta establecido
echo $GITHUB_TOKEN | head -c 10

# Verificar archivo de configuracion
cat ~/.hpm/config.json

# Verificar directorio de cache
ls -la ~/.hpm/cache/

# Probar con salida detallada
hpm install --verbose
```

### Problemas Comunes

**"GitHub rate limit exceeded"**
- Configura autenticacion con `GITHUB_TOKEN`
- Espera a que se reinicie el limite de tasa
- Usa `--offline` si los paquetes estan en cache

**"Permission denied" en cache**
```bash
# Arreglar permisos de cache
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Crear directorio de configuracion
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## Ver Tambien

- [Instalacion](installation.md) - Instalar hpm
- [Solucion de Problemas](troubleshooting.md) - Problemas comunes
- [Comandos](commands.md) - Referencia de comandos
