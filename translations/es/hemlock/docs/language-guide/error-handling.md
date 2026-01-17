# Manejo de Errores

Hemlock soporta manejo de errores basado en excepciones con `try`, `catch`, `finally`, `throw` y `panic`. Esta guía cubre errores recuperables con excepciones y errores irrecuperables con panic.

## Resumen

```hemlock
// Manejo básico de errores
try {
    risky_operation();
} catch (e) {
    print("Error: " + e);
}

// Con limpieza
try {
    process_file();
} catch (e) {
    print("Failed: " + e);
} finally {
    cleanup();
}

// Lanzando errores
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Sintaxis

**Try/catch básico:**
```hemlock
try {
    // código riesgoso
} catch (e) {
    // manejar error, e contiene el valor lanzado
}
```

**Try/finally:**
```hemlock
try {
    // código riesgoso
} finally {
    // siempre se ejecuta, incluso si se lanza excepción
}
```

**Try/catch/finally:**
```hemlock
try {
    // código riesgoso
} catch (e) {
    // manejar error
} finally {
    // código de limpieza
}
```

### Bloque Try

El bloque try ejecuta sentencias secuencialmente:

```hemlock
try {
    print("Starting...");
    risky_operation();
    print("Success!");  // Solo si no hay excepción
}
```

**Comportamiento:**
- Ejecuta sentencias en orden
- Si se lanza excepción: salta a `catch` o `finally`
- Si no hay excepción: ejecuta `finally` (si está presente) y luego continúa

### Bloque Catch

El bloque catch recibe el valor lanzado:

```hemlock
try {
    throw "oops";
} catch (error) {
    print("Caught: " + error);  // error = "oops"
    // error solo accesible aquí
}
// error no accesible aquí
```

**Parámetro catch:**
- Recibe el valor lanzado (cualquier tipo)
- Con ámbito del bloque catch
- Puede tener cualquier nombre (convencionalmente `e`, `err` o `error`)

**Qué puede hacer en catch:**
```hemlock
try {
    risky_operation();
} catch (e) {
    // Registrar el error
    print("Error: " + e);

    // Relanzar el mismo error
    throw e;

    // Lanzar error diferente
    throw "different error";

    // Retornar un valor por defecto
    return null;

    // Manejar y continuar
    // (sin relanzar)
}
```

### Bloque Finally

El bloque finally **siempre se ejecuta**:

```hemlock
try {
    print("1: try");
    throw "error";
} catch (e) {
    print("2: catch");
} finally {
    print("3: finally");  // Siempre se ejecuta
}
print("4: after");

// Salida: 1: try, 2: catch, 3: finally, 4: after
```

**Cuándo se ejecuta finally:**
- Después del bloque try (si no hay excepción)
- Después del bloque catch (si se capturó excepción)
- Incluso si try/catch contiene `return`, `break` o `continue`
- Antes de que el flujo de control salga del try/catch

**Finally con return:**
```hemlock
fn example() {
    try {
        return 1;  // Retorna 1 después de que finally se ejecute
    } finally {
        print("cleanup");  // Se ejecuta antes de retornar
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // El return de finally sobrescribe - retorna 2
    }
}
```

**Finally con flujo de control:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Sale después de que finally se ejecute
        }
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

## Sentencia Throw

### Throw Básico

Lanza cualquier valor como excepción:

```hemlock
throw "error message";
throw 404;
throw { code: 500, message: "Internal error" };
throw null;
throw ["error", "details"];
```

**Ejecución:**
1. Evalúa la expresión
2. Inmediatamente salta al `catch` más cercano
3. Si no hay `catch`, propaga hacia arriba en la pila de llamadas

### Lanzando Errores

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "Age cannot be negative";
    }
    if (age > 150) {
        throw "Age is unrealistic";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Validation error: " + e);
}
```

### Lanzando Objetos de Error

Cree información de error estructurada:

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "File does not exist"
        };
    }
    // ... leer archivo
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("File not found: " + e.path);
    }
}
```

### Relanzamiento

Capturar y relanzar errores:

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Logging error: " + e);
        throw e;  // Relanzar al llamador
    }
}

try {
    wrapper();
} catch (e) {
    print("Caught in main: " + e);
}
```

## Excepciones No Capturadas

Si una excepción propaga hasta el tope de la pila de llamadas sin ser capturada:

```hemlock
fn foo() {
    throw "uncaught!";
}

foo();  // Falla con: Runtime error: uncaught!
```

**Comportamiento:**
- El programa falla
- Imprime mensaje de error a stderr
- Sale con código de estado distinto de cero
- Traza de pila a ser agregada en versiones futuras

## Panic - Errores Irrecuperables

### Qué es Panic?

`panic()` es para **errores irrecuperables** que deben terminar el programa inmediatamente:

```hemlock
panic();                    // Mensaje por defecto: "panic!"
panic("custom message");    // Mensaje personalizado
panic(42);                  // Valores no string se imprimen
```

**Semántica:**
- **Sale inmediatamente** del programa con código de salida 1
- Imprime mensaje de error a stderr: `panic: <mensaje>`
- **NO es capturable** con try/catch
- Usar para bugs y errores irrecuperables

### Panic vs Throw

```hemlock
// throw - Error recuperable (puede ser capturado)
try {
    throw "recoverable error";
} catch (e) {
    print("Caught: " + e);  // Capturado exitosamente
}

// panic - Error irrecuperable (no puede ser capturado)
try {
    panic("unrecoverable error");  // El programa sale inmediatamente
} catch (e) {
    print("This never runs");       // Nunca se ejecuta
}
```

### Cuándo Usar Panic

**Use panic para:**
- **Bugs**: Se alcanzó código inalcanzable
- **Estado inválido**: Se detectó corrupción de estructura de datos
- **Errores irrecuperables**: Recurso crítico no disponible
- **Fallos de aserción**: Cuando `assert()` no es suficiente

**Ejemplos:**
```hemlock
// Código inalcanzable
fn process_state(state: i32) {
    if (state == 1) {
        return "ready";
    } else if (state == 2) {
        return "running";
    } else if (state == 3) {
        return "stopped";
    } else {
        panic("invalid state: " + typeof(state));  // Nunca debería pasar
    }
}

// Verificación de recurso crítico
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json not found - cannot start");
    }
    // ...
}

// Invariante de estructura de datos
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() called on empty stack");
    }
    return stack.pop();
}
```

### Cuándo NO Usar Panic

**Use throw en su lugar para:**
- Validación de entrada de usuario
- Archivo no encontrado
- Errores de red
- Condiciones de error esperadas

```hemlock
// MAL: Panic para errores esperados
fn divide(a, b) {
    if (b == 0) {
        panic("division by zero");  // Demasiado severo
    }
    return a / b;
}

// BIEN: Throw para errores esperados
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";  // Recuperable
    }
    return a / b;
}
```

## Interacciones de Flujo de Control

### Return Dentro de Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Retorna 1 después de que finally se ejecute
    } finally {
        print("cleanup");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // El return de finally sobrescribe el return de try - retorna 2
    }
}
```

**Regla:** Los valores de retorno del bloque finally sobrescriben los valores de retorno de try/catch.

### Break/Continue Dentro de Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Sale después de que finally se ejecute
    } finally {
        print("cleanup " + typeof(i));
    }
}
```

**Regla:** Break/continue se ejecutan después del bloque finally.

### Try/Catch Anidados

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Caught: " + e);  // Imprime: Caught: inner
        throw "outer";  // Relanza error diferente
    }
} catch (e) {
    print("Caught: " + e);  // Imprime: Caught: outer
}
```

**Regla:** Los bloques try/catch anidados funcionan como se espera, las capturas internas suceden primero.

## Patrones Comunes

### Patrón: Limpieza de Recursos

Siempre use `finally` para limpieza:

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Error processing file: " + e);
    } finally {
        if (file != null) {
            file.close();  // Siempre cierra, incluso en error
        }
    }
}
```

### Patrón: Envolvimiento de Errores

Envuelva errores de nivel inferior con contexto:

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Failed to load config from " + path + ": " + e;
    }
}
```

### Patrón: Recuperación de Errores

Proporcione alternativa en caso de error:

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "division by zero";
        }
        return a / b;
    } catch (e) {
        print("Error: " + e);
        return null;  // Valor alternativo
    }
}
```

### Patrón: Validación

Use excepciones para validación:

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Name is required";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Invalid age";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Invalid email";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "invalid" });
} catch (e) {
    print("Validation failed: " + e);
}
```

### Patrón: Múltiples Tipos de Error

Use objetos de error para distinguir tipos de error:

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Data is null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Expected array" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Array is empty" };
    }

    // ... procesar
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("No data provided");
    } else if (e.type == "TypeError") {
        print("Wrong data type: " + e.message);
    } else {
        print("Error: " + e.message);
    }
}
```

## Mejores Prácticas

1. **Use excepciones para casos excepcionales** - No para flujo de control normal
2. **Lance errores significativos** - Use strings u objetos con contexto
3. **Siempre use finally para limpieza** - Asegura que los recursos se liberen
4. **No capture e ignore** - Al menos registre el error
5. **Relance cuando sea apropiado** - Deje que el llamador maneje si usted no puede
6. **Panic para bugs** - Use panic para errores irrecuperables
7. **Documente las excepciones** - Deje claro qué funciones pueden lanzar

## Errores Comunes

### Error: Tragarse Errores

```hemlock
// MAL: Fallo silencioso
try {
    risky_operation();
} catch (e) {
    // Error ignorado - fallo silencioso
}

// BIEN: Registrar o manejar
try {
    risky_operation();
} catch (e) {
    print("Operation failed: " + e);
    // Manejar apropiadamente
}
```

### Error: Sobrescritura de Finally

```hemlock
// MAL: Finally sobrescribe return
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Retorna 0, no 42!
    }
}

// BIEN: No retornar en finally
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Solo limpieza, sin return
    }
}
```

### Error: Olvidar Limpieza

```hemlock
// MAL: El archivo puede no cerrarse en error
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Puede lanzar
    file.close();  // Nunca se alcanza si hay error
}

// BIEN: Usar finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Error: Usar Panic para Errores Esperados

```hemlock
// MAL: Panic para error esperado
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Config file not found");  // Demasiado severo
    }
    return read_file(path);
}

// BIEN: Throw para error esperado
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Config file not found: " + path;  // Recuperable
    }
    return read_file(path);
}
```

## Ejemplos

### Ejemplo: Manejo Básico de Errores

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Error: " + e);  // Imprime: Error: division by zero
}
```

### Ejemplo: Gestión de Recursos

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("File copied successfully");
    } catch (e) {
        print("Failed to copy file: " + e);
        throw e;  // Relanzar
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Ejemplo: Manejo de Errores Anidado

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Failed to process user: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Processed: " + typeof(success_count) + " success, " + typeof(error_count) + " errors");
}
```

### Ejemplo: Tipos de Error Personalizados

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a must be a number", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b must be a number", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Cannot divide by zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Ejemplo: Lógica de Reintento

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // Éxito!
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation failed after " + typeof(max_attempts) + " attempts: " + e;
            }
            print("Attempt " + typeof(attempt) + " failed, retrying...");
        }
    }
}

fn unreliable_operation() {
    // Operación no confiable simulada
    if (random() < 0.7) {
        throw "Operation failed";
    }
    return "Success";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("All retries failed: " + e);
}
```

## Orden de Ejecución

Entendiendo el orden de ejecución:

```hemlock
try {
    print("1: try block start");
    throw "error";
    print("2: never reached");
} catch (e) {
    print("3: catch block");
} finally {
    print("4: finally block");
}
print("5: after try/catch/finally");

// Salida:
// 1: try block start
// 3: catch block
// 4: finally block
// 5: after try/catch/finally
```

## Limitaciones Actuales

- **Sin traza de pila** - Las excepciones no capturadas no muestran traza de pila (planificado)
- **Algunos builtins salen** - Algunas funciones integradas todavía usan `exit()` en lugar de lanzar (a revisar)
- **Sin tipos de excepción personalizados** - Cualquier valor puede ser lanzado, pero no hay jerarquía formal de excepciones

## Temas Relacionados

- [Funciones](functions.md) - Excepciones y retornos de funciones
- [Flujo de Control](control-flow.md) - Cómo las excepciones afectan el flujo de control
- [Memoria](memory.md) - Usando finally para limpieza de memoria

## Ver También

- **Semántica de Excepciones**: Consulte la sección "Error Handling" de CLAUDE.md
- **Panic vs Throw**: Diferentes casos de uso para diferentes tipos de error
- **Garantía de Finally**: Siempre se ejecuta, incluso con return/break/continue
