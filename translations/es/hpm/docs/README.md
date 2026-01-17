# Documentacion de hpm

Bienvenido a la documentacion de hpm (Hemlock Package Manager). hpm es el gestor de paquetes oficial para el lenguaje de programacion [Hemlock](https://github.com/hemlang/hemlock).

## Descripcion General

hpm utiliza GitHub como su registro de paquetes, donde los paquetes se identifican por su ruta de repositorio de GitHub (por ejemplo, `hemlang/sprout`). Esto significa:

- **Sin registro central** - los paquetes residen en repositorios de GitHub
- **Etiquetas de version** - las versiones son etiquetas de Git (por ejemplo, `v1.0.0`)
- **Publicar es solo git** - enviar una etiqueta para publicar una nueva version

## Documentacion

### Primeros Pasos

- [Instalacion](installation.md) - Como instalar hpm
- [Inicio Rapido](quick-start.md) - Comienza a trabajar en 5 minutos
- [Configuracion del Proyecto](project-setup.md) - Configurar un nuevo proyecto Hemlock

### Guia del Usuario

- [Referencia de Comandos](commands.md) - Referencia completa de todos los comandos de hpm
- [Configuracion](configuration.md) - Archivos de configuracion y variables de entorno
- [Solucion de Problemas](troubleshooting.md) - Problemas comunes y soluciones

### Desarrollo de Paquetes

- [Creacion de Paquetes](creating-packages.md) - Como crear y publicar paquetes
- [Especificacion de Paquetes](package-spec.md) - El formato de package.json
- [Versionado](versioning.md) - Versionado semantico y restricciones de version

### Referencia

- [Arquitectura](architecture.md) - Arquitectura interna y diseno
- [Codigos de Salida](exit-codes.md) - Referencia de codigos de salida de CLI

## Referencia Rapida

### Comandos Basicos

```bash
hpm init                              # Crear un nuevo package.json
hpm install                           # Instalar todas las dependencias
hpm install owner/repo                # Agregar e instalar un paquete
hpm install owner/repo@^1.0.0        # Instalar con restriccion de version
hpm uninstall owner/repo              # Eliminar un paquete
hpm update                            # Actualizar todos los paquetes
hpm list                              # Mostrar paquetes instalados
hpm run <script>                      # Ejecutar un script del paquete
```

### Identificacion de Paquetes

Los paquetes usan el formato `owner/repo` de GitHub:

```
hemlang/sprout          # Framework web
hemlang/json            # Utilidades JSON
alice/http-client       # Biblioteca cliente HTTP
```

### Restricciones de Version

| Sintaxis | Significado |
|----------|-------------|
| `1.0.0` | Version exacta |
| `^1.2.3` | Compatible (>=1.2.3 <2.0.0) |
| `~1.2.3` | Actualizaciones de parche (>=1.2.3 <1.3.0) |
| `>=1.0.0` | Al menos 1.0.0 |
| `*` | Cualquier version |

## Obtener Ayuda

- Usa `hpm --help` para ayuda en linea de comandos
- Usa `hpm <comando> --help` para ayuda especifica del comando
- Reporta problemas en [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## Licencia

hpm se distribuye bajo la Licencia MIT.
