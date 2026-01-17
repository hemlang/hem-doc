# Ejecucion de Comandos en Hemlock

Hemlock proporciona la **funcion integrada `exec()`** para ejecutar comandos de shell y capturar su salida.

## Tabla de Contenidos

- [Vision General](#vision-general)
- [La Funcion exec()](#la-funcion-exec)
- [Objeto de Resultado](#objeto-de-resultado)
- [Uso Basico](#uso-basico)
- [Ejemplos Avanzados](#ejemplos-avanzados)
- [Manejo de Errores](#manejo-de-errores)
- [Detalles de Implementacion](#detalles-de-implementacion)
- [Consideraciones de Seguridad](#consideraciones-de-seguridad)
- [Limitaciones](#limitaciones)
- [Casos de Uso](#casos-de-uso)
- [Mejores Practicas](#mejores-practicas)
- [Ejemplos Completos](#ejemplos-completos)

## Vision General

La funcion `exec()` permite a los programas de Hemlock:
- Ejecutar comandos de shell
- Capturar salida estandar (stdout)
- Verificar codigos de estado de salida
- Usar caracteristicas del shell (pipes, redirecciones, etc.)
- Integrarse con utilidades del sistema

**Importante:** Los comandos se ejecutan via `/bin/sh`, dando capacidades completas del shell pero tambien introduciendo consideraciones de seguridad.

## La Funcion exec()

### Firma

```hemlock
exec(command: string): object
```

**Parametros:**
- `command` (string) - Comando de shell a ejecutar

**Retorna:** Un objeto con dos campos:
- `output` (string) - La salida stdout del comando
- `exit_code` (i32) - El codigo de estado de salida del comando

### Ejemplo Basico

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## Objeto de Resultado

El objeto retornado por `exec()` tiene la siguiente estructura:

```hemlock
{
    output: string,      // stdout del comando (salida capturada)
    exit_code: i32       // Estado de salida del proceso (0 = exito)
}
```

### Campo output

Contiene todo el texto escrito a stdout por el comando.

**Propiedades:**
- Cadena vacia si el comando no produce salida
- Incluye saltos de linea y espacios en blanco tal cual
- Salida multi-linea preservada
- Sin limite de tamano (asignado dinamicamente)

**Ejemplos:**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Listado de directorio con saltos de linea

let r3 = exec("true");
print(r3.output);  // "" (cadena vacia)
```

### Campo exit_code

El codigo de estado de salida del comando.

**Valores:**
- `0` tipicamente indica exito
- `1-255` indican errores (la convencion varia por comando)
- `-1` si el comando no pudo ejecutarse o termino anormalmente

**Ejemplos:**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (exito)

let r2 = exec("false");
print(r2.exit_code);  // 1 (fallo)

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2 (archivo no encontrado, varia por comando)
```

## Uso Basico

### Comando Simple

```hemlock
let r = exec("ls -la");
print(r.output);
print("Exit code: " + typeof(r.exit_code));
```

### Verificando Estado de Salida

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found: " + r.output);
} else {
    print("Pattern not found");
}
```

### Comandos con Pipes

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Multiples Comandos

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Sustitucion de Comandos

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Fecha actual
```

## Ejemplos Avanzados

### Manejando Fallos

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Command failed with code: " + typeof(r.exit_code));
    print("Error output: " + r.output);  // Nota: stderr no se captura
}
```

### Procesando Salida Multi-Linea

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Encadenamiento de Comandos

**Con && (AND):**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup complete");
}
```

**Con || (OR):**
```hemlock
let r = exec("command1 || command2");
// Ejecuta command2 solo si command1 falla
```

**Con ; (secuencia):**
```hemlock
let r = exec("command1; command2");
// Ejecuta ambos independientemente del exito/fallo
```

### Usando Pipes

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**Pipelines complejos:**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Patrones de Codigo de Salida

Diferentes codigos de salida indican diferentes condiciones:

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
} else if (r.exit_code == 1) {
    print("File does not exist");
} else {
    print("Test command failed: " + typeof(r.exit_code));
}
```

### Redirecciones de Salida

```hemlock
// Redirigir stdout a archivo (dentro del shell)
let r1 = exec("echo 'test' > /tmp/output.txt");

// Redirigir stderr a stdout (Nota: stderr todavia no se captura por Hemlock)
let r2 = exec("command 2>&1");
```

### Variables de Entorno

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### Cambios de Directorio de Trabajo

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Manejo de Errores

### Cuando exec() Lanza Excepciones

La funcion `exec()` lanza una excepcion si el comando no puede ejecutarse:

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Failed to execute: " + e);
}
```

**Se lanzan excepciones cuando:**
- `popen()` falla (ej. no puede crear pipe)
- Se exceden los limites de recursos del sistema
- Fallos de asignacion de memoria

### Cuando exec() NO Lanza

```hemlock
// El comando se ejecuta pero retorna codigo de salida no cero
let r1 = exec("false");
print(r1.exit_code);  // 1 (no es una excepcion)

// El comando no produce salida
let r2 = exec("true");
print(r2.output);  // "" (no es una excepcion)

// Comando no encontrado por el shell
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127 (no es una excepcion)
```

### Patron de Ejecucion Segura

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Warning: Command failed with code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Error executing command: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## Detalles de Implementacion

### Como Funciona

**Bajo el capo:**
- Usa `popen()` para ejecutar comandos via `/bin/sh`
- Captura solo stdout (stderr no se captura)
- Salida almacenada dinamicamente (comienza en 4KB, crece segun necesidad)
- Estado de salida extraido usando macros `WIFEXITED()` y `WEXITSTATUS()`
- Cadena de salida correctamente terminada en null

**Flujo del proceso:**
1. `popen(command, "r")` crea pipe y bifurca el proceso
2. El proceso hijo ejecuta `/bin/sh -c "command"`
3. El padre lee stdout via pipe a buffer creciente
4. `pclose()` espera al hijo y retorna estado de salida
5. Estado de salida se extrae y almacena en objeto de resultado

### Consideraciones de Rendimiento

**Costos:**
- Crea un nuevo proceso de shell para cada llamada (~1-5ms de sobrecarga)
- Salida almacenada completamente en memoria (no transmitida)
- Sin soporte de streaming (espera a que el comando complete)
- Adecuado para comandos con tamanos de salida razonables

**Optimizaciones:**
- Buffer comienza en 4KB y se duplica cuando esta lleno (uso eficiente de memoria)
- Bucle de lectura unico minimiza llamadas al sistema
- Sin copia adicional de strings

**Cuando usar:**
- Comandos de corta duracion (< 1 segundo)
- Tamano de salida moderado (< 10MB)
- Operaciones por lotes con intervalos razonables

**Cuando NO usar:**
- Daemons o servicios de larga duracion
- Comandos que producen gigabytes de salida
- Procesamiento de datos de streaming en tiempo real
- Ejecucion de alta frecuencia (> 100 llamadas/segundo)

## Consideraciones de Seguridad

### Riesgo de Inyeccion de Shell

⚠️ **CRITICO:** Los comandos son ejecutados por el shell (`/bin/sh`), lo que significa que **la inyeccion de shell es posible**.

**Codigo vulnerable:**
```hemlock
// PELIGROSO - NO HACER ESTO
let filename = args[1];  // Entrada de usuario
let r = exec("cat " + filename);  // Inyeccion de shell!
```

**Ataque:**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Ejecuta: cat ; rm -rf /; echo pwned
```

### Practicas Seguras

**1. Nunca usar entrada de usuario sin sanitizar:**
```hemlock
// Malo
let user_input = args[1];
let r = exec("process " + user_input);  // PELIGROSO

// Bueno - validar primero
fn is_safe_filename(name: string): bool {
    // Solo permitir alfanumericos, guion, guion bajo, punto
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Invalid filename");
}
```

**2. Usar listas permitidas, no listas denegadas:**
```hemlock
// Bueno - lista estricta de permitidos
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Invalid command");
}
```

**3. Escapar caracteres especiales:**
```hemlock
fn shell_escape(s: string): string {
    // Escape simple - envolver en comillas simples y escapar comillas simples
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. Evitar exec() para operaciones de archivo:**
```hemlock
// Malo - usar exec para operaciones de archivo
let r = exec("cat file.txt");

// Bueno - usar API de archivos de Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### Consideraciones de Permisos

Los comandos se ejecutan con los mismos permisos que el proceso de Hemlock:

```hemlock
// Si Hemlock se ejecuta como root, los comandos exec() tambien se ejecutan como root!
let r = exec("rm -rf /important");  // PELIGROSO si se ejecuta como root
```

**Mejor practica:** Ejecutar Hemlock con los privilegios minimos necesarios.

## Limitaciones

### 1. Sin Captura de stderr

Solo stdout se captura, stderr va a la terminal:

```hemlock
let r = exec("ls /nonexistent");
// r.output esta vacio
// El mensaje de error aparece en la terminal, no se captura
```

**Solucion - redirigir stderr a stdout:**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// Ahora los mensajes de error estan en r.output
```

### 2. Sin Streaming

Debe esperar a que el comando complete:

```hemlock
let r = exec("long_running_command");
// Bloquea hasta que el comando termine
// No puede procesar salida incrementalmente
```

### 3. Sin Timeout

Los comandos pueden ejecutarse indefinidamente:

```hemlock
let r = exec("sleep 1000");
// Bloquea por 1000 segundos
// No hay forma de hacer timeout o cancelar
```

**Solucion - usar comando timeout:**
```hemlock
let r = exec("timeout 5 long_command");
// Hara timeout despues de 5 segundos
```

### 4. Sin Manejo de Senales

No se pueden enviar senales a comandos en ejecucion:

```hemlock
let r = exec("long_command");
// No se puede enviar SIGINT, SIGTERM, etc. al comando
```

### 5. Sin Control de Proceso

No se puede interactuar con el comando despues de iniciarlo:

```hemlock
let r = exec("interactive_program");
// No se puede enviar entrada al programa
// No se puede controlar la ejecucion
```

## Casos de Uso

### Buenos Casos de Uso

**1. Ejecutar utilidades del sistema:**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Procesamiento rapido de datos con herramientas Unix:**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Unique lines: " + r.output);
```

**3. Verificar estado del sistema:**
```hemlock
let r = exec("df -h");
print("Disk usage:\n" + r.output);
```

**4. Verificaciones de existencia de archivos:**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
}
```

**5. Generar reportes:**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Running instances: " + count);
```

**6. Scripts de automatizacion:**
```hemlock
exec("git add .");
exec("git commit -m 'Auto commit'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push failed");
}
```

### No Recomendado Para

**1. Servicios de larga duracion:**
```hemlock
// Malo
let r = exec("nginx");  // Bloquea para siempre
```

**2. Comandos interactivos:**
```hemlock
// Malo - no puede proporcionar entrada
let r = exec("ssh user@host");
```

**3. Comandos que producen salida enorme:**
```hemlock
// Malo - carga toda la salida en memoria
let r = exec("cat 10GB_file.log");
```

**4. Streaming en tiempo real:**
```hemlock
// Malo - no puede procesar salida incrementalmente
let r = exec("tail -f /var/log/app.log");
```

**5. Manejo de errores criticos para la mision:**
```hemlock
// Malo - stderr no se captura
let r = exec("critical_operation");
// No puede ver mensajes de error detallados
```

## Mejores Practicas

### 1. Siempre Verificar Codigos de Salida

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Command failed!");
    // Manejar error
}
```

### 2. Recortar Salida Cuando Sea Necesario

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // Remover salto de linea final
print(clean);  // "test" (sin salto de linea)
```

### 3. Validar Antes de Ejecutar

```hemlock
fn is_valid_command(cmd: string): bool {
    // Validar que el comando es seguro
    return true;  // Tu logica de validacion
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. Usar try/catch para Operaciones Criticas

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Command failed";
    }
} catch (e) {
    print("Error: " + e);
    // Limpieza o recuperacion
}
```

### 5. Preferir APIs de Hemlock Sobre exec()

```hemlock
// Malo - usar exec para operaciones de archivo
let r = exec("cat file.txt");

// Bueno - usar API de archivos de Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. Capturar stderr Cuando Sea Necesario

```hemlock
// Redirigir stderr a stdout
let r = exec("command 2>&1");
// Ahora r.output contiene tanto stdout como stderr
```

### 7. Usar Caracteristicas del Shell Sabiamente

```hemlock
// Usar pipes para eficiencia
let r = exec("cat large.txt | grep pattern | head -n 10");

// Usar sustitucion de comandos
let r = exec("echo Current user: $(whoami)");

// Usar ejecucion condicional
let r = exec("test -f file.txt && cat file.txt");
```

## Ejemplos Completos

### Ejemplo 1: Recopilador de Informacion del Sistema

```hemlock
fn get_system_info() {
    print("=== System Information ===");

    // Nombre de host
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // Uptime
    let r2 = exec("uptime");
    print("Uptime: " + r2.output.trim());

    // Uso de disco
    let r3 = exec("df -h /");
    print("\nDisk Usage:");
    print(r3.output);

    // Uso de memoria
    let r4 = exec("free -h");
    print("Memory Usage:");
    print(r4.output);
}

get_system_info();
```

### Ejemplo 2: Analizador de Logs

```hemlock
fn analyze_log(logfile: string) {
    print("Analyzing log: " + logfile);

    // Contar lineas totales
    let r1 = exec("wc -l " + logfile);
    print("Total lines: " + r1.output.trim());

    // Contar errores
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Errors: " + errors);
    } else {
        print("Errors: 0");
    }

    // Contar advertencias
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Warnings: " + warnings);
    } else {
        print("Warnings: 0");
    }

    // Errores recientes
    print("\nRecent errors:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Usage: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### Ejemplo 3: Ayudante de Git

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Error: Not a git repository");
        return;
    }

    if (r.output == "") {
        print("Working directory clean");
    } else {
        print("Changes:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Adding all changes...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Error adding files");
        return;
    }

    print("Committing...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Error committing");
        return;
    }

    print("Committed successfully");
    print(r2.output);
}

// Uso
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### Ejemplo 4: Script de Respaldo

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Backing up " + source + " to " + dest);

    // Crear directorio de respaldo
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Error creating backup directory");
        return false;
    }

    // Crear tarball con marca de tiempo
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Creating archive: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Error creating backup:");
        print(r3.output);
        return false;
    }

    print("Backup completed successfully");

    // Mostrar tamano del respaldo
    let r4 = exec("du -h " + backup_file);
    print("Backup size: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Usage: " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Resumen

La funcion `exec()` de Hemlock proporciona:

- ✅ Ejecucion simple de comandos de shell
- ✅ Captura de salida (stdout)
- ✅ Verificacion de codigo de salida
- ✅ Acceso completo a caracteristicas del shell (pipes, redirecciones, etc.)
- ✅ Integracion con utilidades del sistema

Recuerda:
- Siempre verificar codigos de salida
- Estar consciente de las implicaciones de seguridad (inyeccion de shell)
- Validar entrada de usuario antes de usar en comandos
- Preferir APIs de Hemlock sobre exec() cuando esten disponibles
- stderr no se captura (usar `2>&1` para redirigir)
- Los comandos bloquean hasta completar
- Usar para utilidades de corta duracion, no servicios de larga duracion

**Lista de verificacion de seguridad:**
- ❌ Nunca usar entrada de usuario sin sanitizar
- ✅ Validar toda entrada
- ✅ Usar listas de permitidos para comandos
- ✅ Escapar caracteres especiales cuando sea necesario
- ✅ Ejecutar con privilegios minimos
- ✅ Preferir APIs de Hemlock sobre comandos de shell
