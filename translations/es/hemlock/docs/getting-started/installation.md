# Instalacion

Esta guia le ayudara a compilar e instalar Hemlock en su sistema.

## Instalacion Rapida (Recomendada)

La forma mas sencilla de instalar Hemlock es usando el script de instalacion de una linea:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Esto descarga e instala el binario precompilado mas reciente para su plataforma (Linux o macOS, x86_64 o arm64).

### Opciones de Instalacion

```bash
# Instalar en un prefijo personalizado (por defecto: ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Instalar una version especifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Instalar y actualizar automaticamente el PATH del shell
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

Despues de la instalacion, verifique que funciona:

```bash
hemlock --version
```

---

## Compilacion desde el Codigo Fuente

Si prefiere compilar desde el codigo fuente o los binarios precompilados no funcionan en su sistema, siga las instrucciones a continuacion.

## Requisitos Previos

### Dependencias Requeridas

Hemlock requiere las siguientes dependencias para compilar:

- **Compilador C**: GCC o Clang (estandar C11)
- **Make**: GNU Make
- **libffi**: Biblioteca de Interfaz de Funciones Foraneas (para soporte FFI)
- **OpenSSL**: Biblioteca criptografica (para funciones hash: md5, sha1, sha256)
- **libwebsockets**: Soporte para cliente/servidor WebSocket y HTTP
- **zlib**: Biblioteca de compresion

### Dependencias Opcionales

#### USearch (busqueda de similitud vectorial)

Requerida solo si desea usar [`@stdlib/vector`](../../stdlib/docs/vector.md). Sin ella, el modulo de vectores no esta disponible y esas pruebas se omiten -- todo lo demas funciona correctamente.

> **Nota:** `cmake --install` **no** instala la biblioteca compartida para usearch v2.x. Debe copiar los archivos manualmente (vea a continuacion).

**Linux:**
```bash
sudo apt-get install -y cmake  # dependencia de compilacion

git clone --depth 1 --branch v2.24.0 --recurse-submodules \
  https://github.com/unum-cloud/usearch.git /tmp/usearch
cmake -B /tmp/usearch/build -S /tmp/usearch -DUSEARCH_BUILD_LIB_C=ON
cmake --build /tmp/usearch/build

sudo cp $(find /tmp/usearch/build -name 'libusearch_c.so' | head -1) /usr/local/lib/
sudo cp /tmp/usearch/c/usearch.h /usr/local/include/
sudo ldconfig
```

**macOS:**
```bash
brew install cmake  # dependencia de compilacion

git clone --depth 1 --branch v2.24.0 --recurse-submodules \
  https://github.com/unum-cloud/usearch.git /tmp/usearch
cmake -B /tmp/usearch/build -S /tmp/usearch -DUSEARCH_BUILD_LIB_C=ON
cmake --build /tmp/usearch/build

sudo mkdir -p /usr/local/lib /usr/local/include
sudo cp $(find /tmp/usearch/build -name 'libusearch_c.dylib' | head -1) /usr/local/lib/
sudo cp /tmp/usearch/c/usearch.h /usr/local/include/
```

#### libwebsockets (cliente/servidor HTTP y WebSocket)

Requerida solo para `@stdlib/http` y `@stdlib/websocket`. Sin ella esos modulos no estan disponibles y sus pruebas se omiten.

---

### Instalacion de Dependencias

**macOS:**
```bash
# Instalar Homebrew si aun no esta instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Xcode Command Line Tools
xcode-select --install

# Instalar dependencias via Homebrew
brew install libffi openssl@3 libwebsockets
```

**Nota para usuarios de macOS**: El Makefile detecta automaticamente las instalaciones de Homebrew y configura las rutas correctas de include/library. Hemlock soporta arquitecturas Intel (x86_64) y Apple Silicon (arm64).

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Compilacion desde el Codigo Fuente

### 1. Clonar el Repositorio

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Compilar Hemlock

```bash
make
```

Esto compilara el interprete de Hemlock y colocara el ejecutable en el directorio actual.

### 3. Verificar la Instalacion

```bash
./hemlock --version
```

Deberia ver la informacion de version de Hemlock.

### 4. Compilar los Modulos C de la Biblioteca Estandar (Opcional)

Algunos modulos de stdlib (`@stdlib/http`, `@stdlib/websocket`, `@stdlib/vector`) requieren bibliotecas compartidas nativas. Compile sus wrappers con:

```bash
make stdlib
```

Esto compila `lws_wrapper.so` (HTTP/WebSocket) si libwebsockets esta instalada. USearch (`libusearch_c.so`) debe instalarse por separado -- vea [Dependencias Opcionales](#dependencias-opcionales) arriba.

### 5. Probar la Compilacion

Ejecute el conjunto de pruebas para asegurarse de que todo funciona correctamente:

```bash
make test
```

Todas las pruebas deberian pasar. Si ve algun fallo, por favor reportelo como un issue.

## Instalacion a Nivel del Sistema (Opcional)

Para instalar Hemlock a nivel del sistema (por ejemplo, en `/usr/local/bin`):

```bash
sudo make install
```

Esto le permite ejecutar `hemlock` desde cualquier lugar sin especificar la ruta completa.

## Ejecutando Hemlock

### REPL Interactivo

Inicie el bucle Leer-Evaluar-Imprimir (REPL):

```bash
./hemlock
```

Vera un prompt donde puede escribir codigo Hemlock:

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

Salga del REPL con `Ctrl+D` o `Ctrl+C`.

### Ejecutando Programas

Ejecute un script de Hemlock:

```bash
./hemlock program.hml
```

Con argumentos de linea de comandos:

```bash
./hemlock program.hml arg1 arg2 "argumento con espacios"
```

## Estructura de Directorios

Despues de compilar, su directorio de Hemlock se vera asi:

```
hemlock/
├── hemlock           # Ejecutable del interprete compilado
├── src/              # Codigo fuente
├── include/          # Archivos de cabecera
├── tests/            # Conjunto de pruebas
├── examples/         # Programas de ejemplo
├── docs/             # Documentacion
├── stdlib/           # Biblioteca estandar
├── Makefile          # Configuracion de compilacion
└── README.md         # README del proyecto
```

## Compilacion WebAssembly (WASM)

Hemlock puede compilarse a WebAssembly mediante [Emscripten](https://emscripten.org/), permitiendo que el interprete completo se ejecute en un navegador web o Node.js.

### Instalacion de Emscripten

El SDK de Emscripten (`emsdk`) proporciona el compilador `emcc` utilizado para compilar el interprete WASM.

**Todas las plataformas (Linux, macOS, Windows WSL):**

```bash
# Clone the emsdk repository
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk

# Install and activate the latest SDK
./emsdk install latest
./emsdk activate latest

# Add emcc to your PATH (run this in every new terminal, or add to your shell profile)
source ./emsdk_env.sh
```

Verifique la instalacion:

```bash
emcc --version
```

Deberia ver una salida como `emcc (Emscripten gcc/clang-like replacement ...) 3.x.x`.

Para instrucciones detalladas, consulte la [guia de inicio de Emscripten](https://emscripten.org/docs/getting_started/downloads.html).

**Opcional: Agregar al perfil del shell**

Para evitar ejecutar `source emsdk_env.sh` cada vez, agreguelo a su perfil del shell:

```bash
# For bash (~/.bashrc or ~/.bash_profile)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.bashrc

# For zsh (~/.zshrc)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.zshrc
```

### Dependencias WASM

La compilacion WASM tiene menos dependencias que la compilacion nativa. Emscripten proporciona sus propias versiones de las bibliotecas C estandar. Las siguientes bibliotecas nativas **no son necesarias** (y no estan disponibles) en la compilacion WASM:

| Biblioteca | Nativa | WASM | Notas |
|---------|--------|------|-------|
| libffi | Requerida | Stub | FFI no esta disponible en WASM |
| OpenSSL | Requerida | Stub | Los builtins de criptografia devuelven errores en WASM |
| libwebsockets | Opcional | Stub | Soporte WebSocket no disponible |
| zlib | Requerida | Emscripten la proporciona | Vinculada automaticamente con `-sUSE_ZLIB=1` |
| pthreads | Requerida | Opcional | Disponible con compilacion con hilos (requiere SharedArrayBuffer) |

**En resumen:** Solo necesita el SDK de Emscripten instalado. No se requieren bibliotecas adicionales del sistema para la compilacion WASM.

### Compilar el Interprete WASM

```bash
# Build the interpreter as WebAssembly
make wasm-interpreter
```

Esto produce dos archivos en el directorio `wasm/`:

| Archivo | Descripcion |
|------|-------------|
| `wasm/hemlock.js` | Cargador JavaScript y codigo de enlace de Emscripten |
| `wasm/hemlock.wasm` | Modulo binario WebAssembly |

### Ejecucion en Node.js

```bash
node -- wasm/hemlock.js -e 'print("Hello from WASM!");'
node -- wasm/hemlock.js examples/fibonacci.hml
```

### Ejecucion en un Navegador

Los archivos WASM deben servirse a traves de HTTP con el tipo MIME correcto (`application/wasm`). Abrir el archivo HTML directamente via `file://` no funcionara.

**Usando el ejemplo incluido:**

```bash
make wasm-browser-example
# Opens http://localhost:8080/examples/wasm-browser/index.html
```

**O manualmente con Python:**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/wasm/playground.html
```

**O manualmente con Node.js:**

```bash
npx serve .
# Open the URL shown in the terminal
```

Consulte `examples/wasm-browser/` para un ejemplo completo de integracion en navegador con un editor de codigo interactivo.

### Limitaciones de WASM

Algunas funcionalidades no estan disponibles en el entorno WASM:

- **FFI** - No se pueden cargar bibliotecas compartidas (`dlopen`/`dlsym`)
- **Criptografia** - Sin OpenSSL (`sha256`, `md5`, etc. devuelven errores)
- **E/S de Archivos** - Sin acceso al sistema de archivos nativo (solo FS virtual de Emscripten)
- **Red** - Sin sockets crudos ni cliente HTTP
- **Senales** - Sin manejo de senales POSIX
- **Procesos** - Sin `fork`, `exec` ni gestion de procesos
- **Hilos** - `spawn`/`join`/canales requieren una compilacion WASM con hilos y `SharedArrayBuffer`

Todas las funcionalidades principales del lenguaje funcionan: variables, funciones, closures, objetos, arrays, coincidencia de patrones, anotaciones de tipo, try/catch y la biblioteca estandar completa de modulos Hemlock puros.

### Compilar Programas Hemlock a WASM

Ademas de ejecutar el interprete en WASM, puede compilar programas Hemlock individuales a binarios WASM independientes usando el backend del compilador:

```bash
# Compile a Hemlock program to WASM (requires both hemlockc and Emscripten)
make wasm-compile FILE=program.hml

# With threading support
make wasm-compile-threaded FILE=program.hml
```

Esto usa `hemlockc` para generar codigo C, luego Emscripten para compilarlo a WASM.

## Opciones de Compilacion

### Compilacion de Depuracion

Compilar con simbolos de depuracion y sin optimizacion:

```bash
make debug
```

### Compilacion Limpia

Eliminar todos los archivos compilados:

```bash
make clean
```

Recompilar desde cero:

```bash
make clean && make
```

## Solucion de Problemas

### macOS: Errores de Biblioteca No Encontrada

Si obtiene errores sobre bibliotecas faltantes (`-lcrypto`, `-lffi`, etc.):

1. Asegurese de que las dependencias de Homebrew estan instaladas:
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Verifique las rutas de Homebrew:
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. El Makefile deberia auto-detectar estas rutas. Si no lo hace, verifique que `brew` esta en su PATH:
   ```bash
   which brew
   ```

### macOS: Errores de Tipo BSD (`u_int`, `u_char` no encontrado)

Si ve errores sobre nombres de tipo desconocidos como `u_int` o `u_char`:

1. Esto se corrigio en v1.0.0+ usando `_DARWIN_C_SOURCE` en lugar de `_POSIX_C_SOURCE`
2. Asegurese de tener la version mas reciente del codigo
3. Limpie y recompile:
   ```bash
   make clean && make
   ```

### Linux: libffi No Encontrada

Si obtiene errores sobre `ffi.h` o `-lffi` faltantes:

1. Asegurese de que `libffi-dev` esta instalada (vea las dependencias arriba)
2. Verifique si `pkg-config` puede encontrarla:
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. Si no se encuentra, puede necesitar configurar `PKG_CONFIG_PATH`:
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Errores de Compilacion

Si encuentra errores de compilacion:

1. Asegurese de tener un compilador compatible con C11
2. En macOS, intente usar Clang (por defecto):
   ```bash
   make CC=clang
   ```
3. En Linux, intente usar GCC:
   ```bash
   make CC=gcc
   ```
4. Verifique que todas las dependencias estan instaladas
5. Intente recompilar desde cero:
   ```bash
   make clean && make
   ```

### Fallos en las Pruebas

Si las pruebas fallan:

1. Verifique que tiene la version mas reciente del codigo
2. Intente recompilar desde cero:
   ```bash
   make clean && make test
   ```
3. En macOS, asegurese de tener las Xcode Command Line Tools mas recientes:
   ```bash
   xcode-select --install
   ```
4. Reporte el problema en GitHub con:
   - Su plataforma (version de macOS / distribucion de Linux)
   - Arquitectura (x86_64 / arm64)
   - Salida de las pruebas
   - Salida de `make -v` y `gcc --version` (o `clang --version`)

## Proximos Pasos

- [Guia de Inicio Rapido](quick-start.md) - Escriba su primer programa en Hemlock
- [Tutorial](tutorial.md) - Aprenda Hemlock paso a paso
- [Guia del Lenguaje](../language-guide/syntax.md) - Explore las caracteristicas de Hemlock
