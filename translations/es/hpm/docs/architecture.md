# Arquitectura

Arquitectura interna y diseno de hpm. Este documento es para contribuidores y aquellos interesados en entender como funciona hpm.

## Descripcion General

hpm esta escrito en Hemlock y consiste en varios modulos que manejan diferentes aspectos de la gestion de paquetes:

```
src/
├── main.hml        # Punto de entrada CLI y enrutamiento de comandos
├── manifest.hml    # Manejo de package.json
├── lockfile.hml    # Manejo de package-lock.json
├── semver.hml      # Versionado semantico
├── resolver.hml    # Resolucion de dependencias
├── github.hml      # Cliente de API de GitHub
├── installer.hml   # Descarga y extraccion de paquetes
└── cache.hml       # Gestion de cache global
```

## Responsabilidades de los Modulos

### main.hml

El punto de entrada para la aplicacion CLI.

**Responsabilidades:**
- Parsear argumentos de linea de comandos
- Enrutar comandos a los manejadores apropiados
- Mostrar informacion de ayuda y version
- Manejar flags globales (--verbose, --dry-run, etc.)
- Salir con codigos apropiados

**Funciones principales:**
- `main()` - Punto de entrada, parsea args y despacha comandos
- `cmd_init()` - Manejar `hpm init`
- `cmd_install()` - Manejar `hpm install`
- `cmd_uninstall()` - Manejar `hpm uninstall`
- `cmd_update()` - Manejar `hpm update`
- `cmd_list()` - Manejar `hpm list`
- `cmd_outdated()` - Manejar `hpm outdated`
- `cmd_run()` - Manejar `hpm run`
- `cmd_why()` - Manejar `hpm why`
- `cmd_cache()` - Manejar `hpm cache`

**Atajos de comandos:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Maneja lectura y escritura de archivos `package.json`.

**Responsabilidades:**
- Leer/escribir package.json
- Validar estructura del paquete
- Gestionar dependencias
- Parsear especificadores de paquetes (owner/repo@version)

**Funciones principales:**
```hemlock
create_default(): Manifest           // Crear manifiesto vacio
read_manifest(): Manifest            // Leer desde archivo
write_manifest(m: Manifest)          // Escribir a archivo
validate(m: Manifest): bool          // Validar estructura
get_all_dependencies(m): Map         // Obtener deps + devDeps
add_dependency(m, pkg, ver, dev)     // Agregar dependencia
remove_dependency(m, pkg)            // Eliminar dependencia
parse_specifier(spec): (name, ver)   // Parsear "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // Parsear "owner/repo"
```

**Estructura de Manifest:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Gestiona el archivo `package-lock.json` para instalaciones reproducibles.

**Responsabilidades:**
- Crear/leer/escribir archivos de bloqueo
- Rastrear versiones exactas resueltas
- Almacenar URLs de descarga y hashes de integridad
- Podar dependencias huerfanas

**Funciones principales:**
```hemlock
create_empty(): Lockfile              // Crear lockfile vacio
read_lockfile(): Lockfile             // Leer desde archivo
write_lockfile(l: Lockfile)           // Escribir a archivo
create_entry(ver, url, hash, deps)    // Crear entrada de bloqueo
get_locked(l, pkg): LockEntry?        // Obtener version bloqueada
set_locked(l, pkg, entry)             // Establecer version bloqueada
remove_locked(l, pkg)                 // Eliminar entrada
prune(l, keep: Set)                   // Eliminar huerfanos
needs_update(l, m): bool              // Verificar si esta desincronizado
```

**Estructura de Lockfile:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // URL de descarga
    integrity: string,    // Hash SHA256
    dependencies: Map<string, string>
};
```

### semver.hml

Implementacion completa de Versionado Semantico 2.0.0.

**Responsabilidades:**
- Parsear cadenas de version
- Comparar versiones
- Parsear y evaluar restricciones de version
- Encontrar versiones que satisfacen restricciones

**Funciones principales:**
```hemlock
// Parseo
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// Comparacion
compare(a, b: Version): int           // -1, 0, o 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Restricciones
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // Verificar si v coincide con c
max_satisfying(versions, c): Version?      // Encontrar coincidencia mas alta
sort(versions): [Version]                  // Ordenar ascendente

// Utilidades
constraints_overlap(a, b: Constraint): bool  // Verificar compatibilidad
```

**Estructura de Version:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // ej., ["beta", "1"]
    build: string?          // ej., "20230101"
};
```

**Tipos de Restriccion:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Rangos combinados
    | Any;                     // "*"
```

### resolver.hml

Implementa resolucion de dependencias estilo npm.

**Responsabilidades:**
- Resolver arboles de dependencias
- Detectar conflictos de versiones
- Detectar dependencias circulares
- Construir arboles de visualizacion

**Funciones principales:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Resolutor principal: retorna mapa plano de todas las dependencias con versiones resueltas

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Encontrar version que satisface todas las restricciones

detect_cycles(deps: Map): [Cycle]?
    // Encontrar dependencias circulares usando DFS

build_tree(lockfile): Tree
    // Crear estructura de arbol para mostrar

find_why(pkg, lockfile): [Chain]
    // Encontrar cadenas de dependencia explicando por que pkg esta instalado
```

**Algoritmo de resolucion:**

1. **Recopilar restricciones**: Recorrer manifiesto y dependencias transitivas
2. **Resolver cada paquete**: Para cada paquete:
   - Obtener todas las restricciones de version de los dependientes
   - Obtener versiones disponibles de GitHub
   - Encontrar version maxima que satisface TODAS las restricciones
   - Error si ninguna version satisface todas (conflicto)
3. **Detectar ciclos**: Ejecutar DFS para encontrar dependencias circulares
4. **Retornar mapa plano**: Nombre del paquete → informacion de version resuelta

**Estructura de ResolveResult:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

Cliente de API de GitHub para descubrimiento y descarga de paquetes.

**Responsabilidades:**
- Obtener versiones disponibles (etiquetas)
- Descargar package.json de repositorios
- Descargar tarballs de lanzamientos
- Manejar autenticacion y limites de tasa

**Funciones principales:**
```hemlock
get_token(): string?
    // Obtener token de env o config

github_request(url, headers?): Response
    // Hacer solicitud a API con reintentos

get_tags(owner, repo): [string]
    // Obtener etiquetas de version (v1.0.0, v1.1.0, etc.)

get_package_json(owner, repo, ref): Manifest
    // Obtener package.json en etiqueta/commit especifico

download_tarball(owner, repo, tag): bytes
    // Descargar archivo de lanzamiento

repo_exists(owner, repo): bool
    // Verificar si el repositorio existe

get_repo_info(owner, repo): RepoInfo
    // Obtener metadatos del repositorio
```

**Logica de reintento:**
- Retroceso exponencial: 1s, 2s, 4s, 8s
- Reintenta en: 403 (limite de tasa), 5xx (error de servidor), errores de red
- Maximo 4 reintentos
- Reporta errores de limite de tasa claramente

**Endpoints de API usados:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Maneja descarga y extraccion de paquetes.

**Responsabilidades:**
- Descargar paquetes de GitHub
- Extraer tarballs a hem_modules
- Verificar/usar paquetes en cache
- Instalar/desinstalar paquetes

**Funciones principales:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Descargar e instalar un solo paquete

install_all(packages: Map, options): InstallResult
    // Instalar todos los paquetes resueltos

uninstall_package(name: string): bool
    // Eliminar paquete de hem_modules

get_installed(): Map<string, string>
    // Listar paquetes actualmente instalados

verify_integrity(pkg): bool
    // Verificar integridad del paquete

prefetch_packages(packages: Map): void
    // Descarga paralela a cache (experimental)
```

**Proceso de instalacion:**

1. Verificar si ya esta instalado en la version correcta
2. Verificar cache por tarball
3. Si no esta en cache, descargar de GitHub
4. Almacenar en cache para uso futuro
5. Extraer a `hem_modules/owner/repo/`
6. Verificar instalacion

**Estructura de directorio creada:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Gestiona la cache global de paquetes.

**Responsabilidades:**
- Almacenar tarballs descargados
- Recuperar paquetes en cache
- Listar paquetes en cache
- Limpiar cache
- Gestionar configuracion

**Funciones principales:**
```hemlock
get_cache_dir(): string
    // Obtener directorio de cache (respeta HPM_CACHE_DIR)

get_config_dir(): string
    // Obtener directorio de configuracion (~/.hpm)

is_cached(owner, repo, version): bool
    // Verificar si tarball esta en cache

get_cached_path(owner, repo, version): string
    // Obtener ruta a tarball en cache

store_tarball_file(owner, repo, version, data): void
    // Guardar tarball en cache

list_cached(): [CachedPackage]
    // Listar todos los paquetes en cache

clear_cache(): int
    // Eliminar todos los paquetes en cache, retorna bytes liberados

get_cache_size(): int
    // Calcular tamano total de cache

read_config(): Config
    // Leer ~/.hpm/config.json

write_config(c: Config): void
    // Escribir archivo de configuracion
```

**Estructura de cache:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Flujo de Datos

### Flujo del Comando Install

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Parsear args, llamar cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Leer package.json, agregar dependencia
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Resolver todas las dependencias
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Obtener versiones, encontrar satisfactoria
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Descargar y extraer paquetes
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Descargar o usar cache
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Actualizar package-lock.json
    └──────────┘
```

### Detalle del Algoritmo de Resolucion

```
Entrada: manifest.dependencies, manifest.devDependencies, lockfile existente

1. Inicializar:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [dependencias directas]

2. Mientras queue no este vacia:
   a. pkg = queue.pop()
   b. Si pkg ya esta resuelto, saltar
   c. Obtener todas las restricciones para pkg de dependientes
   d. Obtener versiones disponibles de GitHub (cacheado)
   e. Encontrar version maxima que satisface TODAS las restricciones
   f. Si ninguna encontrada: CONFLICTO
   g. resolved[pkg] = {version, url, deps}
   h. Agregar dependencias de pkg a queue

3. Detectar ciclos en grafo resuelto
   - Si se encuentra ciclo: ERROR

4. Retornar mapa resuelto
```

## Manejo de Errores

### Codigos de Salida

Definidos en main.hml:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Propagacion de Errores

Los errores se propagan a traves de valores de retorno:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propaga
    // ...
}
```

## Pruebas

### Framework de Pruebas

Framework de pruebas personalizado en `test/framework.hml`:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### Archivos de Prueba

- `test/test_semver.hml` - Parseo de versiones, comparacion, restricciones
- `test/test_manifest.hml` - Lectura/escritura de manifiesto, validacion
- `test/test_lockfile.hml` - Operaciones de lockfile
- `test/test_cache.hml` - Gestion de cache

### Ejecutar Pruebas

```bash
# Todas las pruebas
make test

# Pruebas especificas
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Mejoras Futuras

### Caracteristicas Planeadas

1. **Verificacion de integridad** - Verificacion completa de hash SHA256
2. **Espacios de trabajo** - Soporte de monorepo
3. **Sistema de plugins** - Comandos extensibles
4. **Auditoria** - Verificacion de vulnerabilidades de seguridad
5. **Registro privado** - Alojamiento de paquetes auto-hospedado

### Limitaciones Conocidas

1. **Error del bundler** - No puede crear ejecutable independiente
2. **Descargas paralelas** - Experimental, puede tener condiciones de carrera
3. **Integridad** - SHA256 no completamente implementado

## Contribuir

### Estilo de Codigo

- Usar indentacion de 4 espacios
- Las funciones deben hacer una cosa
- Comentar logica compleja
- Escribir pruebas para nuevas caracteristicas

### Agregar un Comando

1. Agregar manejador en `main.hml`:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementation
   }
   ```

2. Agregar al despacho de comandos:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Actualizar texto de ayuda

### Agregar un Modulo

1. Crear `src/newmodule.hml`
2. Exportar interfaz publica
3. Importar en modulos que lo necesiten
4. Agregar pruebas en `test/test_newmodule.hml`

## Ver Tambien

- [Comandos](commands.md) - Referencia de CLI
- [Creacion de Paquetes](creating-packages.md) - Desarrollo de paquetes
- [Versionado](versioning.md) - Versionado semantico
