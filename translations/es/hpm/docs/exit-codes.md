# Codigos de Salida

Referencia de codigos de salida de hpm y sus significados.

## Tabla de Codigos de Salida

| Codigo | Nombre | Descripcion |
|--------|--------|-------------|
| 0 | SUCCESS | Comando completado exitosamente |
| 1 | CONFLICT | Conflicto de version de dependencia |
| 2 | NOT_FOUND | Paquete no encontrado |
| 3 | VERSION_NOT_FOUND | Version solicitada no encontrada |
| 4 | NETWORK | Error de red |
| 5 | INVALID_MANIFEST | package.json invalido |
| 6 | INTEGRITY | Verificacion de integridad fallida |
| 7 | RATE_LIMIT | Limite de tasa de API de GitHub excedido |
| 8 | CIRCULAR | Dependencia circular detectada |

## Descripciones Detalladas

### Codigo de Salida 0: SUCCESS

El comando se completo exitosamente.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Codigo de Salida 1: CONFLICT

Dos o mas paquetes requieren versiones incompatibles de una dependencia.

**Ejemplo:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Soluciones:**
1. Verificar que paquetes tienen el conflicto:
   ```bash
   hpm why hemlang/json
   ```
2. Actualizar el paquete en conflicto:
   ```bash
   hpm update package-a
   ```
3. Relajar restricciones de version en package.json
4. Eliminar uno de los paquetes en conflicto

### Codigo de Salida 2: NOT_FOUND

El paquete especificado no existe en GitHub.

**Ejemplo:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Soluciones:**
1. Verificar la ortografia del nombre del paquete
2. Verificar si el repositorio existe: `https://github.com/owner/repo`
3. Verificar que tienes acceso (para repos privados, establecer GITHUB_TOKEN)

### Codigo de Salida 3: VERSION_NOT_FOUND

Ninguna version coincide con la restriccion especificada.

**Ejemplo:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Soluciones:**
1. Verificar versiones disponibles en releases/tags de GitHub
2. Usar una restriccion de version valida
3. Las etiquetas de version deben comenzar con 'v' (ej., `v1.0.0`)

### Codigo de Salida 4: NETWORK

Ocurrio un error relacionado con la red.

**Ejemplo:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Soluciones:**
1. Verificar conexion a internet
2. Verificar si GitHub es accesible
3. Verificar configuracion de proxy si estas detras de un firewall
4. Usar `--offline` si los paquetes estan en cache:
   ```bash
   hpm install --offline
   ```
5. Esperar y reintentar (hpm reintenta automaticamente)

### Codigo de Salida 5: INVALID_MANIFEST

El archivo package.json es invalido o tiene formato incorrecto.

**Ejemplo:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Soluciones:**
1. Verificar sintaxis JSON (usar un validador de JSON)
2. Asegurar que los campos requeridos existan (`name`, `version`)
3. Verificar formatos de campos:
   - name: formato `owner/repo`
   - version: formato semver `X.Y.Z`
4. Regenerar:
   ```bash
   rm package.json
   hpm init
   ```

### Codigo de Salida 6: INTEGRITY

La verificacion de integridad del paquete fallo.

**Ejemplo:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Soluciones:**
1. Limpiar cache y reinstalar:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Verificar problemas de red (descargas parciales)
3. Verificar que el paquete no fue manipulado

### Codigo de Salida 7: RATE_LIMIT

Se ha excedido el limite de tasa de la API de GitHub.

**Ejemplo:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Soluciones:**
1. **Autenticar con GitHub** (recomendado):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Esperar a que se reinicie el limite de tasa (se reinicia cada hora)
3. Usar modo sin conexion si los paquetes estan en cache:
   ```bash
   hpm install --offline
   ```

### Codigo de Salida 8: CIRCULAR

Dependencia circular detectada en el grafo de dependencias.

**Ejemplo:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**Soluciones:**
1. Esto generalmente es un error en los paquetes mismos
2. Contactar a los mantenedores del paquete
3. Evitar usar uno de los paquetes circulares

## Usar Codigos de Salida en Scripts

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## Solucion de Problemas por Codigo de Salida

### Referencia Rapida

| Codigo | Primer Paso a Verificar |
|--------|------------------------|
| 1 | Ejecutar `hpm why <paquete>` para ver conflicto |
| 2 | Verificar nombre del paquete en GitHub |
| 3 | Verificar versiones disponibles en etiquetas de GitHub |
| 4 | Verificar conexion a internet |
| 5 | Validar sintaxis de package.json |
| 6 | Ejecutar `hpm cache clean && hpm install` |
| 7 | Establecer variable de entorno `GITHUB_TOKEN` |
| 8 | Contactar mantenedores del paquete |

## Ver Tambien

- [Solucion de Problemas](troubleshooting.md) - Soluciones detalladas
- [Comandos](commands.md) - Referencia de comandos
- [Configuracion](configuration.md) - Configurar token de GitHub
