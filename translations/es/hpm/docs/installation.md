# Instalacion

Esta guia cubre como instalar hpm en tu sistema.

## Instalacion Rapida (Recomendada)

Instala la ultima version con un solo comando:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Esto automaticamente:
- Detecta tu sistema operativo (Linux, macOS)
- Detecta tu arquitectura (x86_64, arm64)
- Descarga el binario precompilado apropiado
- Instala en `/usr/local/bin` (o usa sudo si es necesario)

### Opciones de Instalacion

```bash
# Instalar en una ubicacion personalizada (no requiere sudo)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Instalar una version especifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Combinar opciones
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Plataformas Soportadas

| Plataforma | Arquitectura | Estado |
|------------|--------------|--------|
| Linux    | x86_64       | ✓ Soportado |
| macOS    | x86_64       | ✓ Soportado |
| macOS    | arm64 (M1/M2/M3) | ✓ Soportado |
| Linux    | arm64        | Compilar desde fuente |

## Compilar desde Fuente

Si prefieres compilar desde fuente o necesitas una plataforma no cubierta por los binarios precompilados, sigue estas instrucciones.

### Prerrequisitos

hpm requiere que [Hemlock](https://github.com/hemlang/hemlock) este instalado primero. Sigue las instrucciones de instalacion de Hemlock antes de continuar.

Verifica que Hemlock este instalado:

```bash
hemlock --version
```

## Metodos de Instalacion

### Metodo 1: Make Install

Compila desde fuente e instala.

```bash
# Clonar el repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Instalar en /usr/local/bin (requiere sudo)
sudo make install
```

Despues de la instalacion, verifica que funcione:

```bash
hpm --version
```

### Metodo 2: Ubicacion Personalizada

Instala en un directorio personalizado (no requiere sudo):

```bash
# Clonar el repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Instalar en ~/.local/bin
make install PREFIX=$HOME/.local

# O cualquier ubicacion personalizada
make install PREFIX=/opt/hemlock
```

Asegurate de que tu directorio bin personalizado este en tu PATH:

```bash
# Agregar a ~/.bashrc o ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Metodo 3: Ejecutar Sin Instalar

Puedes ejecutar hpm directamente sin instalar:

```bash
# Clonar el repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Crear script wrapper local
make

# Ejecutar desde el directorio hpm
./hpm --help

# O ejecutar via hemlock directamente
hemlock src/main.hml --help
```

### Metodo 4: Instalacion Manual

Crea tu propio script wrapper:

```bash
# Clonar en una ubicacion permanente
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Crear script wrapper
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Variables de Instalacion

El Makefile soporta estas variables:

| Variable | Por Defecto | Descripcion |
|----------|-------------|-------------|
| `PREFIX` | `/usr/local` | Prefijo de instalacion |
| `BINDIR` | `$(PREFIX)/bin` | Directorio de binarios |
| `HEMLOCK` | `hemlock` | Ruta al interprete hemlock |

Ejemplo con variables personalizadas:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Como Funciona

El instalador crea un script shell wrapper que invoca el interprete Hemlock con el codigo fuente de hpm:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

Este enfoque:
- No requiere compilacion
- Siempre ejecuta el ultimo codigo fuente
- Funciona de manera confiable en todas las plataformas

## Actualizar hpm

Para actualizar hpm a la ultima version:

```bash
cd /path/to/hpm
git pull origin main

# Re-instalar si la ruta cambio
sudo make install
```

## Desinstalar

Eliminar hpm de tu sistema:

```bash
cd /path/to/hpm
sudo make uninstall
```

O eliminar manualmente:

```bash
sudo rm /usr/local/bin/hpm
```

## Verificar la Instalacion

Despues de la instalacion, verifica que todo funcione:

```bash
# Verificar version
hpm --version

# Ver ayuda
hpm --help

# Probar inicializacion (en un directorio vacio)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Solucion de Problemas

### "hemlock: command not found"

Hemlock no esta instalado o no esta en tu PATH. Instala Hemlock primero:

```bash
# Verificar si hemlock existe
which hemlock

# Si no se encuentra, instalar Hemlock desde https://github.com/hemlang/hemlock
```

### "Permission denied"

Usa sudo para instalacion en todo el sistema, o instala en un directorio de usuario:

```bash
# Opcion 1: Usar sudo
sudo make install

# Opcion 2: Instalar en directorio de usuario
make install PREFIX=$HOME/.local
```

### "hpm: command not found" despues de la instalacion

Tu PATH puede no incluir el directorio de instalacion:

```bash
# Verificar donde se instalo hpm
ls -la /usr/local/bin/hpm

# Agregar al PATH si usas ubicacion personalizada
export PATH="$HOME/.local/bin:$PATH"
```

## Notas Especificas por Plataforma

### Linux

La instalacion estandar funciona en todas las distribuciones de Linux. Algunas distribuciones pueden requerir:

```bash
# Debian/Ubuntu: Asegurar herramientas de compilacion
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

La instalacion estandar funciona. Si usas Homebrew:

```bash
# Asegurar herramientas de linea de comandos de Xcode
xcode-select --install
```

### Windows (WSL)

hpm funciona en Windows Subsystem for Linux:

```bash
# En terminal WSL
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Proximos Pasos

Despues de la instalacion:

1. [Inicio Rapido](quick-start.md) - Crea tu primer proyecto
2. [Referencia de Comandos](commands.md) - Aprende todos los comandos
3. [Configuracion](configuration.md) - Configura hpm
