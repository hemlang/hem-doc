# Argumentos de Linea de Comandos en Hemlock

Los programas de Hemlock pueden acceder a los argumentos de linea de comandos a traves de un **array `args` integrado** que se llena automaticamente al iniciar el programa.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [El Array args](#el-array-args)
- [Propiedades](#propiedades)
- [Patrones de Iteracion](#patrones-de-iteracion)
- [Casos de Uso Comunes](#casos-de-uso-comunes)
- [Patrones de Analisis de Argumentos](#patrones-de-analisis-de-argumentos)
- [Mejores Practicas](#mejores-practicas)
- [Ejemplos Completos](#ejemplos-completos)

## Vision General

El array `args` proporciona acceso a los argumentos de linea de comandos pasados a tu programa de Hemlock:

- **Siempre disponible** - Variable global integrada en todos los programas de Hemlock
- **Nombre del script incluido** - `args[0]` siempre contiene la ruta/nombre del script
- **Array de strings** - Todos los argumentos son strings
- **Indexado desde cero** - Indexacion estandar de array (0, 1, 2, ...)

## El Array args

### Estructura Basica

```hemlock
// args[0] es siempre el nombre del archivo de script
// args[1] a args[n-1] son los argumentos reales
print(args[0]);        // "script.hml"
print(args.length);    // Numero total de argumentos (incluyendo nombre del script)
```

### Ejemplo de Uso

**Comando:**
```bash
./hemlock script.hml hello world "test 123"
```

**En script.hml:**
```hemlock
print("Script name: " + args[0]);     // "script.hml"
print("Total args: " + typeof(args.length));  // "4"
print("First arg: " + args[1]);       // "hello"
print("Second arg: " + args[2]);      // "world"
print("Third arg: " + args[3]);       // "test 123"
```

### Referencia de Indices

| Indice | Contiene | Valor de Ejemplo |
|--------|----------|------------------|
| `args[0]` | Ruta/nombre del script | `"script.hml"` o `"./script.hml"` |
| `args[1]` | Primer argumento | `"hello"` |
| `args[2]` | Segundo argumento | `"world"` |
| `args[3]` | Tercer argumento | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Ultimo argumento | (varia) |

## Propiedades

### Siempre Presente

`args` es un array global disponible en **todos** los programas de Hemlock:

```hemlock
// No necesita declararse o importarse
print(args.length);  // Funciona inmediatamente
```

### Nombre del Script Incluido

`args[0]` siempre contiene la ruta/nombre del script:

```hemlock
print("Running: " + args[0]);
```

**Valores posibles para args[0]:**
- `"script.hml"` - Solo el nombre del archivo
- `"./script.hml"` - Ruta relativa
- `"/home/user/script.hml"` - Ruta absoluta
- Depende de como se invoco el script

### Tipo: Array de Strings

Todos los argumentos se almacenan como strings:

```hemlock
// Argumentos: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (string, no numero)
print(args[2]);  // "3.14" (string, no numero)
print(args[3]);  // "true" (string, no booleano)

// Convertir segun necesidad:
let num = 42;  // Parsear manualmente si es necesario
```

### Longitud Minima

Siempre al menos 1 (el nombre del script):

```hemlock
print(args.length);  // Minimo: 1
```

**Incluso sin argumentos:**
```bash
./hemlock script.hml
```

```hemlock
// En script.hml:
print(args.length);  // 1 (solo nombre del script)
```

### Comportamiento en REPL

En el REPL, `args.length` es 0 (array vacio):

```hemlock
# Sesion REPL
> print(args.length);
0
```

## Patrones de Iteracion

### Iteracion Basica

Saltar `args[0]` (nombre del script) y procesar argumentos reales:

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**Salida para: `./hemlock script.hml foo bar baz`**
```
Argument 1: foo
Argument 2: bar
Argument 3: baz
```

### Iteracion For-In (Incluyendo Nombre del Script)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Salida:**
```
script.hml
foo
bar
baz
```

### Verificando Cantidad de Argumentos

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <argument>");
    // salir o retornar
} else {
    let arg = args[1];
    // procesar arg
}
```

### Procesando Todos los Argumentos Excepto el Nombre del Script

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Processing: " + arg);
}
```

## Casos de Uso Comunes

### 1. Procesamiento Simple de Argumentos

Verificar argumento requerido:

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Processing file: " + filename);
    // ... procesar archivo
}
```

**Uso:**
```bash
./hemlock script.hml data.txt
# Salida: Processing file: data.txt
```

### 2. Multiples Argumentos

```hemlock
if (args.length < 3) {
    print("Usage: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Input: " + input_file);
    print("Output: " + output_file);

    // Procesar archivos...
}
```

**Uso:**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. Numero Variable de Argumentos

Procesar todos los argumentos proporcionados:

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**Uso:**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Mensaje de Ayuda

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show this help message");
    print("  -v, --verbose  Enable verbose output");
} else {
    // Procesar normalmente
}
```

### 5. Validacion de Argumentos

```hemlock
fn validate_file(filename: string): bool {
    // Verificar si el archivo existe (ejemplo)
    return filename != "";
}

if (args.length < 2) {
    print("Error: No filename provided");
} else if (!validate_file(args[1])) {
    print("Error: Invalid file: " + args[1]);
} else {
    print("Processing: " + args[1]);
}
```

## Patrones de Analisis de Argumentos

### Argumentos con Nombre (Flags)

Patron simple para argumentos con nombre:

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Verbose mode enabled");
}
print("Input: " + input_file);
print("Output: " + output_file);
```

**Uso:**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Flags Booleanos

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### Argumentos con Valor

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // Necesitaria parsear string a int
        }
    }
    i = i + 1;
}
```

### Argumentos Posicionales y con Nombre Mezclados

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // Tratar como argumento posicional
        positional.push(args[i]);
    }
    i = i + 1;
}

// Asignar argumentos posicionales
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### Funcion Auxiliar de Analizador de Argumentos

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // Argumento posicional
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose: " + typeof(opts.verbose));
print("Output: " + opts.output);
print("Files: " + typeof(opts.files.length));
```

## Mejores Practicas

### 1. Siempre Verificar Cantidad de Argumentos

```hemlock
// Bueno
if (args.length < 2) {
    print("Usage: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// Malo - puede fallar si no hay argumentos
process_file(args[1]);  // Error si args.length == 1
```

### 2. Proporcionar Informacion de Uso

```hemlock
fn show_usage() {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show help");
    print("  -v, --verbose  Verbose output");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. Validar Argumentos

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Error: Missing required argument");
        return false;
    }

    if (args[1] == "") {
        print("Error: Empty argument");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // salir o mostrar uso
}
```

### 4. Usar Nombres de Variables Descriptivos

```hemlock
// Bueno
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// Malo
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Manejar Argumentos con Comillas y Espacios

El shell maneja esto automaticamente:

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. Crear Objetos de Argumentos

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Input: " + arguments.input);
```

## Ejemplos Completos

### Ejemplo 1: Procesador de Archivos

```hemlock
// Uso: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Usage: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Processing " + input + " -> " + output);

    // Procesar archivos
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // Procesamiento de ejemplo
        f_out.write(processed);

        print("Done!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Ejemplo 2: Procesador de Archivos por Lotes

```hemlock
// Uso: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Processing: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // Procesar contenido...
            print("    " + typeof(content.length) + " bytes");
        } catch (e) {
            print("    Error: " + e);
        }

        i = i + 1;
    }

    print("Done!");
}
```

### Ejemplo 3: Analizador de Argumentos Avanzado

```hemlock
// Uso: ./hemlock app.hml [OPTIONS] <files...>
// Opciones:
//   --verbose, -v     Habilitar salida detallada
//   --output, -o FILE Establecer archivo de salida
//   --help, -h        Mostrar ayuda

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Error: --output requires a value");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Error: Unknown option: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Usage: " + args[0] + " [OPTIONS] <files...>");
    print("Options:");
    print("  --verbose, -v     Enable verbose output");
    print("  --output, -o FILE Set output file");
    print("  --help, -h        Show this help");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Error: No input files specified");
    show_help();
} else {
    if (config.verbose) {
        print("Verbose mode enabled");
        print("Output file: " + config.output);
        print("Input files: " + typeof(config.files.length));
    }

    // Procesar archivos
    for (let file in config.files) {
        if (config.verbose) {
            print("Processing: " + file);
        }
        // ... procesar archivo
    }
}
```

### Ejemplo 4: Herramienta de Configuracion

```hemlock
// Uso: ./hemlock config.hml <action> [arguments]
// Acciones:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Usage: " + args[0] + " <action> [arguments]");
    print("Actions:");
    print("  get <key>         Get configuration value");
    print("  set <key> <value> Set configuration value");
    print("  list              List all configuration");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Error: 'get' requires a key");
        } else {
            let key = args[2];
            print("Getting: " + key);
            // ... obtener de configuracion
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Error: 'set' requires key and value");
        } else {
            let key = args[2];
            let value = args[3];
            print("Setting " + key + " = " + value);
            // ... establecer en configuracion
        }
    } else if (action == "list") {
        print("Listing all configuration:");
        // ... listar configuracion
    } else {
        print("Error: Unknown action: " + action);
        show_usage();
    }
}
```

## Resumen

El soporte de argumentos de linea de comandos de Hemlock proporciona:

- ✅ Array `args` integrado disponible globalmente
- ✅ Acceso simple basado en array a los argumentos
- ✅ Nombre del script en `args[0]`
- ✅ Todos los argumentos como strings
- ✅ Metodos de array disponibles (.length, .slice, etc.)

Recuerda:
- Siempre verificar `args.length` antes de acceder a elementos
- `args[0]` es el nombre del script
- Los argumentos reales comienzan en `args[1]`
- Todos los argumentos son strings - convertir segun necesidad
- Proporcionar informacion de uso para herramientas amigables
- Validar argumentos antes de procesar

Patrones comunes:
- Argumentos posicionales simples
- Argumentos con nombre/flags (--flag)
- Argumentos con valor (--option value)
- Mensajes de ayuda (--help)
- Validacion de argumentos
