# Funciones

Las funciones en Hemlock son **valores de primera clase** que pueden asignarse a variables, pasarse como argumentos y retornarse desde otras funciones. Esta guia cubre la sintaxis de funciones, clausuras, recursion y patrones avanzados.

## Resumen

```hemlock
// Sintaxis de funcion con nombre
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Funcion anonima
let multiply = fn(x, y) {
    return x * y;
};

// Clausuras
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Declaracion de Funciones

### Funciones con Nombre

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**Componentes:**
- `fn` - Palabra clave de funcion
- `greet` - Nombre de la funcion
- `(name: string)` - Parametros con tipos opcionales
- `: string` - Tipo de retorno opcional
- `{ ... }` - Cuerpo de la funcion

### Funciones Anonimas

Funciones sin nombre, asignadas a variables:

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Con nombre vs. Anonima:**
```hemlock
// Estas son equivalentes:
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Nota:** Las funciones con nombre se descomponen en asignaciones de variables con funciones anonimas.

## Parametros

### Parametros Basicos

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Anotaciones de Tipo

Anotaciones de tipo opcionales en parametros:

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // La verificacion de tipo en tiempo de ejecucion promueve a f64
```

**Verificacion de tipos:**
- Los tipos de parametros se verifican en el momento de la llamada si estan anotados
- Las conversiones implicitas de tipo siguen reglas estandar de promocion
- Las incompatibilidades de tipo causan errores de tiempo de ejecucion

### Paso por Valor

Todos los argumentos se **copian** (paso por valor):

```hemlock
fn modify(x) {
    x = 100;  // Solo modifica la copia local
}

let a = 10;
modify(a);
print(a);  // Sigue siendo 10 (sin cambios)
```

**Nota:** Los objetos y arrays se pasan por referencia (la referencia se copia), por lo que su contenido puede modificarse:

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Modifica el array original
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (modificado)
```

## Valores de Retorno

### Sentencia Return

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Anotaciones de Tipo de Retorno

Anotacion de tipo opcional para el valor de retorno:

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Verificacion de tipos:**
- Los tipos de retorno se verifican cuando la funcion retorna (si estan anotados)
- Las conversiones de tipo siguen reglas estandar de promocion

### Retorno Implicito

Las funciones sin anotacion de tipo de retorno retornan implicitamente `null`:

```hemlock
fn print_message(msg) {
    print(msg);
    // Retorna implicitamente null
}

let result = print_message("hello");  // result es null
```

### Retorno Temprano

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Salida temprana
        }
    }
    return -1;  // No encontrado
}
```

### Retorno Sin Valor

`return;` sin valor retorna `null`:

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Retorna null
    }
    return value * 2;
}
```

## Funciones de Primera Clase

Las funciones pueden asignarse, pasarse y retornarse como cualquier otro valor.

### Funciones como Variables

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Reasignar
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Funciones como Argumentos

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Funciones como Valores de Retorno

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Clausuras

Las funciones capturan su entorno de definicion (alcance lexico).

### Clausuras Basicas

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

**Como funciona:**
- La funcion interna captura `count` del alcance externo
- `count` persiste entre llamadas a la funcion retornada
- Cada llamada a `makeCounter()` crea una nueva clausura con su propio `count`

### Clausura con Parametros

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Clausuras Multiples

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Alcance Lexico

Las funciones pueden acceder a variables del alcance externo a traves del alcance lexico:

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Puede leer global y outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Las clausuras capturan variables por referencia, permitiendo tanto lectura como mutacion de variables del alcance externo (como se muestra en el ejemplo `makeCounter` anterior).

## Recursion

Las funciones pueden llamarse a si mismas.

### Recursion Basica

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Recursion Mutua

Las funciones pueden llamarse entre si:

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Procesamiento Recursivo de Datos

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Nota:** Aun no hay optimizacion de llamada de cola - la recursion profunda puede causar desbordamiento de pila.

## Funciones de Orden Superior

Funciones que toman o retornan otras funciones.

### Patron Map

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Patron Filter

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Patron Reduce

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Composicion de Funciones

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Patrones Comunes

### Patron: Funciones Fabrica

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### Patron: Funciones Callback

```hemlock
fn process_async(data, callback) {
    // ... hacer procesamiento
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### Patron: Aplicacion Parcial

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Patron: Memorizacion

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Mucho mas rapido con cache
```

## Semantica de Funciones

### Requisitos de Tipo de Retorno

Las funciones con anotacion de tipo de retorno **deben** retornar un valor:

```hemlock
fn get_value(): i32 {
    // ERROR: Falta sentencia return
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Verificacion de Tipos

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Promueve a f64, retorna f64
add("a", "b");     // Error de tiempo de ejecucion: incompatibilidad de tipos
```

### Reglas de Alcance

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Puede acceder: inner_var, outer_var, global
    }

    // Puede acceder: outer_var, global
    // No puede acceder: inner_var
}

// Puede acceder: global
// No puede acceder: outer_var, inner_var
```

## Mejores Practicas

1. **Usar anotaciones de tipo** - Ayuda a detectar errores y documenta la intencion
2. **Mantener funciones pequenas** - Cada funcion debe hacer una cosa
3. **Preferir funciones puras** - Evitar efectos secundarios cuando sea posible
4. **Nombrar funciones claramente** - Usar nombres verbales descriptivos
5. **Retornar temprano** - Usar clausulas de guarda para reducir anidamiento
6. **Documentar clausuras complejas** - Hacer explicitas las variables capturadas
7. **Evitar recursion profunda** - Aun no hay optimizacion de llamada de cola

## Errores Comunes

### Error: Profundidad de Recursion

```hemlock
// La recursion profunda puede causar desbordamiento de pila
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Puede fallar con desbordamiento de pila
```

### Error: Modificar Variables Capturadas

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Puede leer y modificar variables capturadas
        return count;
    };
}
```

**Nota:** Esto funciona, pero ten en cuenta que todas las clausuras comparten el mismo entorno capturado.

## Ejemplos

### Ejemplo: Pipeline de Funciones

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Ejemplo: Manejador de Eventos

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clicked: " + data);
});

trigger_event("click", "button1");
```

### Ejemplo: Ordenamiento con Comparador Personalizado

```hemlock
fn sort(arr, compare) {
    // Ordenamiento burbuja con comparador personalizado
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Parametros Opcionales (Argumentos por Defecto)

Las funciones pueden tener parametros opcionales con valores por defecto usando la sintaxis `?:`:

```hemlock
fn greet(name, greeting?: "Hello") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Hello Alice"
print(greet("Bob", "Hi"));       // "Hi Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Reglas:**
- Los parametros opcionales deben venir despues de los parametros requeridos
- Los valores por defecto pueden ser cualquier expresion
- Los argumentos omitidos usan el valor por defecto

## Funciones Variadicas (Parametros Rest)

Las funciones pueden aceptar un numero variable de argumentos usando parametros rest (`...`):

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Starting", "Running", "Done");
// INFO: Starting
// INFO: Running
// INFO: Done
```

**Reglas:**
- El parametro rest debe ser el ultimo parametro
- El parametro rest recolecta todos los argumentos restantes en un array
- Puede combinarse con parametros regulares y opcionales

## Anotaciones de Tipo de Funcion

Los tipos de funcion te permiten especificar la firma exacta esperada para parametros de funcion y valores de retorno:

### Tipos de Funcion Basicos

```hemlock
// Sintaxis de tipo de funcion: fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Tipos de Funciones de Orden Superior

```hemlock
// Funcion que retorna una funcion
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Tipos de Funcion Async

```hemlock
// Tipo de funcion async
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### Alias de Tipo de Funcion

```hemlock
// Crear tipos de funcion nombrados para claridad
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Parametros Const

El modificador `const` previene que un parametro sea mutado dentro de la funcion:

### Parametros Const Basicos

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // ERROR: no se puede mutar parametro const
    for (item in items) {
        print(item);   // OK: leer esta permitido
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Inmutabilidad Profunda

Los parametros const imponen inmutabilidad profunda - ninguna mutacion a traves de ninguna ruta:

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK: leer esta permitido
    // person.name = "Bob";   // ERROR: no se puede mutar
    // person.address.city = "NYC";  // ERROR: const profundo
}
```

### Lo Que Const Previene

| Tipo | Bloqueado por Const | Permitido |
|------|---------------------|-----------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | asignacion de campo | lectura de campo |
| buffer | asignacion de indice | lectura de indice |
| string | asignacion de indice | todos los metodos (retornan nuevas cadenas) |

## Argumentos con Nombre

Las funciones pueden llamarse con argumentos con nombre para claridad y flexibilidad:

### Argumentos con Nombre Basicos

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Argumentos posicionales (tradicional)
create_user("Alice", 25, false);

// Argumentos con nombre - pueden estar en cualquier orden
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Mezclar Posicionales y con Nombre

```hemlock
// Saltar parametros opcionales nombrando lo que necesitas
create_user("David", active: false);  // Usa age=18 por defecto

// Los argumentos con nombre deben venir despues de los posicionales
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // ERROR: posicional despues de nombrado
```

### Reglas para Argumentos con Nombre

- Usar sintaxis `name: value` para argumentos con nombre
- Los argumentos con nombre pueden aparecer en cualquier orden despues de los argumentos posicionales
- Los argumentos posicionales no pueden seguir a los argumentos con nombre
- Funciona con parametros por defecto/opcionales
- Nombres de parametros desconocidos causan errores de tiempo de ejecucion

## Limitaciones

Limitaciones actuales a tener en cuenta:

- **Sin paso por referencia** - La palabra clave `ref` se analiza pero no esta implementada
- **Sin sobrecarga de funciones** - Una funcion por nombre
- **Sin optimizacion de llamada de cola** - La recursion profunda limitada por tamano de pila

## Temas Relacionados

- [Flujo de Control](control-flow.md) - Usando funciones con estructuras de control
- [Objetos](objects.md) - Los metodos son funciones almacenadas en objetos
- [Manejo de Errores](error-handling.md) - Funciones y manejo de excepciones
- [Tipos](types.md) - Anotaciones de tipo y conversiones

## Ver Tambien

- **Clausuras**: Ver la seccion "Funciones" en CLAUDE.md para semantica de clausuras
- **Valores de Primera Clase**: Las funciones son valores como cualquier otro
- **Alcance Lexico**: Las funciones capturan su entorno de definicion
