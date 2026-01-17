# Solucion de Problemas

Soluciones a problemas comunes de hpm.

## Problemas de Instalacion

### "hemlock: command not found"

**Causa:** Hemlock no esta instalado o no esta en el PATH.

**Solucion:**

```bash
# Verificar si hemlock existe
which hemlock

# Si no se encuentra, instalar Hemlock primero
# Visita: https://github.com/hemlang/hemlock

# Despues de la instalacion, verificar
hemlock --version
```

### "hpm: command not found"

**Causa:** hpm no esta instalado o no esta en el PATH.

**Solucion:**

```bash
# Verificar donde esta instalado hpm
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Si usas ubicacion personalizada, agregar al PATH
export PATH="$HOME/.local/bin:$PATH"

# Agregar a ~/.bashrc o ~/.zshrc para persistencia
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Reinstalar si es necesario
cd /path/to/hpm
sudo make install
```

### "Permission denied" durante la instalacion

**Causa:** Sin permiso de escritura en el directorio de instalacion.

**Solucion:**

```bash
# Opcion 1: Usar sudo para instalacion en todo el sistema
sudo make install

# Opcion 2: Instalar en directorio de usuario (sin sudo)
make install PREFIX=$HOME/.local
```

## Problemas de Dependencias

### "Package not found" (codigo de salida 2)

**Causa:** El paquete no existe en GitHub.

**Solucion:**

```bash
# Verificar que el paquete existe
# Verifica: https://github.com/owner/repo

# Verificar ortografia
hpm install hemlang/sprout  # Correcto
hpm install hemlan/sprout   # Owner incorrecto
hpm install hemlang/spout   # Repo incorrecto

# Verificar errores tipograficos en package.json
cat package.json | grep -A 5 dependencies
```

### "Version not found" (codigo de salida 3)

**Causa:** Ninguna version coincide con la restriccion de version.

**Solucion:**

```bash
# Listar versiones disponibles (verificar releases/tags en GitHub)
# Las etiquetas deben comenzar con 'v' (ej., v1.0.0)

# Usar una restriccion de version valida
hpm install owner/repo@^1.0.0

# Intentar ultima version
hpm install owner/repo

# Verificar etiquetas disponibles en GitHub
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (codigo de salida 1)

**Causa:** Dos paquetes requieren versiones incompatibles de una dependencia.

**Solucion:**

```bash
# Ver el conflicto
hpm install --verbose

# Verificar que requiere la dependencia
hpm why conflicting/package

# Soluciones:
# 1. Actualizar el paquete en conflicto
hpm update problem/package

# 2. Cambiar restricciones de version en package.json
# Editar para permitir versiones compatibles

# 3. Eliminar uno de los paquetes en conflicto
hpm uninstall one/package
```

### "Circular dependency" (codigo de salida 8)

**Causa:** El paquete A depende de B, que depende de A.

**Solucion:**

```bash
# Identificar el ciclo
hpm install --verbose

# Esto generalmente es un error en los paquetes
# Contactar a los mantenedores del paquete

# Solucion alternativa: evitar uno de los paquetes
```

## Problemas de Red

### "Network error" (codigo de salida 4)

**Causa:** No se puede conectar a la API de GitHub.

**Solucion:**

```bash
# Verificar conexion a internet
ping github.com

# Verificar si la API de GitHub es accesible
curl -I https://api.github.com

# Intentar de nuevo (hpm reintenta automaticamente)
hpm install

# Usar modo sin conexion si los paquetes estan en cache
hpm install --offline

# Verificar configuracion de proxy si estas detras de un firewall
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (codigo de salida 7)

**Causa:** Demasiadas solicitudes a la API sin autenticacion.

**Solucion:**

```bash
# Opcion 1: Autenticar con token de GitHub (recomendado)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Crear token: GitHub → Settings → Developer settings → Personal access tokens

# Opcion 2: Guardar token en archivo de configuracion
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Opcion 3: Esperar a que se reinicie el limite de tasa (se reinicia cada hora)

# Opcion 4: Usar modo sin conexion
hpm install --offline
```

### Timeout de conexion

**Causa:** Red lenta o problemas con la API de GitHub.

**Solucion:**

```bash
# hpm reintenta automaticamente con retroceso exponencial

# Verificar si GitHub tiene problemas
# Visita: https://www.githubstatus.com

# Intentar mas tarde
hpm install

# Usar paquetes en cache
hpm install --offline
```

## Problemas de Package.json

### "Invalid package.json" (codigo de salida 5)

**Causa:** Formato incorrecto o campos requeridos faltantes.

**Solucion:**

```bash
# Validar sintaxis JSON
cat package.json | python -m json.tool

# Verificar campos requeridos
cat package.json

# Campos requeridos:
# - "name": formato "owner/repo"
# - "version": formato "X.Y.Z"

# Regenerar si es necesario
rm package.json
hpm init
```

### Error de formato "name"

**Causa:** Nombre del paquete no esta en formato `owner/repo`.

**Solucion:**

```json
// Incorrecto
{
  "name": "my-package"
}

// Correcto
{
  "name": "yourusername/my-package"
}
```

### Error de formato "version"

**Causa:** Version no esta en formato semver.

**Solucion:**

```json
// Incorrecto
{
  "version": "1.0"
}

// Correcto
{
  "version": "1.0.0"
}
```

## Problemas del Archivo de Bloqueo

### Archivo de bloqueo desincronizado

**Causa:** package.json modificado sin ejecutar install.

**Solucion:**

```bash
# Regenerar archivo de bloqueo
rm package-lock.json
hpm install
```

### Archivo de bloqueo corrupto

**Causa:** JSON invalido o ediciones manuales.

**Solucion:**

```bash
# Verificar validez del JSON
cat package-lock.json | python -m json.tool

# Regenerar
rm package-lock.json
hpm install
```

## Problemas de hem_modules

### Los paquetes no se instalan

**Causa:** Varios problemas posibles.

**Solucion:**

```bash
# Limpiar y reinstalar
rm -rf hem_modules
hpm install

# Verificar salida detallada
hpm install --verbose
```

### La importacion no funciona

**Causa:** Paquete no instalado correctamente o ruta de importacion incorrecta.

**Solucion:**

```bash
# Verificar que el paquete este instalado
ls hem_modules/owner/repo/

# Verificar campo main de package.json
cat hem_modules/owner/repo/package.json

# Formato correcto de importacion
import { x } from "owner/repo";          # Usa entrada main
import { y } from "owner/repo/subpath";  # Importacion de subruta
```

### Error "Module not found"

**Causa:** La ruta de importacion no resuelve a un archivo.

**Solucion:**

```bash
# Verificar ruta de importacion
ls hem_modules/owner/repo/src/

# Verificar existencia de index.hml
ls hem_modules/owner/repo/src/index.hml

# Verificar campo main en package.json
cat hem_modules/owner/repo/package.json | grep main
```

## Problemas de Cache

### La cache ocupa demasiado espacio

**Solucion:**

```bash
# Ver tamano de cache
hpm cache list

# Limpiar cache
hpm cache clean
```

### Permisos de cache

**Solucion:**

```bash
# Arreglar permisos
chmod -R u+rw ~/.hpm/cache

# O eliminar y reinstalar
rm -rf ~/.hpm/cache
hpm install
```

### Usando cache incorrecta

**Solucion:**

```bash
# Verificar ubicacion de cache
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Limpiar variable de entorno si es incorrecta
unset HPM_CACHE_DIR
```

## Problemas de Scripts

### "Script not found"

**Causa:** El nombre del script no existe en package.json.

**Solucion:**

```bash
# Listar scripts disponibles
cat package.json | grep -A 20 scripts

# Verificar ortografia
hpm run test    # Correcto
hpm run tests   # Incorrecto si el script se llama "test"
```

### El script falla

**Causa:** Error en el comando del script.

**Solucion:**

```bash
# Ejecutar comando directamente para ver el error
hemlock test/run.hml

# Verificar definicion del script
cat package.json | grep test
```

## Depuracion

### Habilitar salida detallada

```bash
hpm install --verbose
```

### Verificar version de hpm

```bash
hpm --version
```

### Verificar version de hemlock

```bash
hemlock --version
```

### Ejecucion en seco

Vista previa sin hacer cambios:

```bash
hpm install --dry-run
```

### Empezar de cero

Comenzar desde cero:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Obtener Ayuda

### Ayuda de comandos

```bash
hpm --help
hpm install --help
```

### Reportar problemas

Si encuentras un error:

1. Verifica problemas existentes: https://github.com/hemlang/hpm/issues
2. Crea un nuevo problema con:
   - Version de hpm (`hpm --version`)
   - Version de Hemlock (`hemlock --version`)
   - Sistema operativo
   - Pasos para reproducir
   - Mensaje de error (usa `--verbose`)

## Referencia de Codigos de Salida

| Codigo | Significado | Solucion Comun |
|--------|-------------|----------------|
| 0 | Exito | - |
| 1 | Conflicto de dependencias | Actualizar o cambiar restricciones |
| 2 | Paquete no encontrado | Verificar ortografia, verificar que el repo existe |
| 3 | Version no encontrada | Verificar versiones disponibles en GitHub |
| 4 | Error de red | Verificar conexion, reintentar |
| 5 | package.json invalido | Arreglar sintaxis JSON y campos requeridos |
| 6 | Verificacion de integridad fallida | Limpiar cache, reinstalar |
| 7 | Limite de tasa de GitHub | Agregar GITHUB_TOKEN |
| 8 | Dependencia circular | Contactar mantenedores del paquete |

## Ver Tambien

- [Instalacion](installation.md) - Guia de instalacion
- [Configuracion](configuration.md) - Opciones de configuracion
- [Comandos](commands.md) - Referencia de comandos
