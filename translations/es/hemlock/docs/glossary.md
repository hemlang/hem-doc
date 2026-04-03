# Glosario

Nuevo en la programacion o conceptos de sistemas? Este glosario explica los terminos utilizados en la documentacion de Hemlock en lenguaje sencillo.

---

## A

### Asignar / Asignacion
**Que significa:** Pedir al computador un bloque de memoria para usar.

**Analogia:** Como pedir prestado un libro de una biblioteca - estas tomando prestado espacio que necesitas devolver despues.

**En Hemlock:**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### Array
**Que significa:** Una lista de valores almacenados juntos, accedidos por posicion (indice).

**Analogia:** Como una fila de buzones numerados 0, 1, 2, 3... Puedes poner algo en el buzon #2 y luego obtenerlo del buzon #2.

**En Hemlock:**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Asincrono
**Que significa:** Codigo que puede ejecutarse "en segundo plano" mientras otro codigo continua. En Hemlock, el codigo asincrono realmente se ejecuta en nucleos de CPU separados simultaneamente.

**Analogia:** Como cocinar varios platos a la vez - pones el arroz, y mientras se cocina, cortas vegetales. Ambos suceden al mismo tiempo.

**En Hemlock:**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Booleano / Bool
**Que significa:** Un valor que es `true` o `false`. Nada mas.

**Nombrado por:** George Boole, un matematico que estudio la logica verdadero/falso.

**En Hemlock:**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Verificacion de Limites
**Que significa:** Verificar automaticamente que no estes intentando acceder a memoria fuera de lo que fue asignado. Previene fallos y bugs de seguridad.

**Analogia:** Como un bibliotecario que verifica que el libro que solicitas realmente existe antes de intentar buscarlo.

**En Hemlock:**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer
**Que significa:** Un contenedor seguro para bytes crudos con un tamano conocido. Hemlock verifica que no leas ni escribas mas alla de sus limites.

**Analogia:** Como una caja fuerte con un numero especifico de compartimentos. Puedes usar cualquier compartimento, pero no puedes acceder al compartimento #50 si la caja fuerte solo tiene 10.

**En Hemlock:**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Clausura
**Que significa:** Una funcion que "recuerda" variables de donde fue creada, incluso despues de que ese codigo haya terminado.

**Analogia:** Como una nota que dice "suma 5 a cualquier numero que me des" - el "5" esta incorporado en la nota.

**En Hemlock:**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Coercion (Coercion de Tipos)
**Que significa:** Convertir automaticamente un valor de un tipo a otro cuando es necesario.

**Ejemplo:** Cuando sumas un entero y un decimal, el entero se convierte automaticamente a decimal primero.

**En Hemlock:**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Compilar / Compilador
**Que significa:** Traducir tu codigo a un programa que el computador puede ejecutar directamente. El compilador (`hemlockc`) lee tu archivo `.hml` y crea un ejecutable.

**Analogia:** Como traducir un libro de ingles a espanol - el contenido es el mismo, pero ahora los hispanohablantes pueden leerlo.

**En Hemlock:**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Concurrencia
**Que significa:** Multiples cosas sucediendo en tiempos superpuestos. En Hemlock, esto significa ejecucion paralela real en multiples nucleos de CPU.

**Analogia:** Dos chefs cocinando diferentes platos simultaneamente en la misma cocina.

---

## D

### Defer
**Que significa:** Programar algo para que suceda despues, cuando la funcion actual termine. Util para limpieza.

**Analogia:** Como decirte a ti mismo "cuando me vaya, apaga las luces" - estableces el recordatorio ahora, sucede despues.

**En Hemlock:**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck Typing
**Que significa:** Si se ve como un pato y hace cuac como un pato, tratalo como un pato. En codigo: si un objeto tiene los campos/metodos que necesitas, usalo - no te preocupes por su "tipo" oficial.

**Nombrado por:** La prueba del pato - una forma de razonamiento.

**En Hemlock:**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Expresion
**Que significa:** Codigo que produce un valor. Puede usarse en cualquier lugar donde se espere un valor.

**Ejemplos:** `42`, `x + y`, `get_name()`, `true && false`

### Enum / Enumeracion
**Que significa:** Un tipo con un conjunto fijo de valores posibles, cada uno con un nombre.

**Analogia:** Como un menu desplegable - solo puedes elegir de las opciones listadas.

**En Hemlock:**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Punto Flotante
**Que significa:** Un numero con punto decimal. Se llama "flotante" porque el punto decimal puede estar en diferentes posiciones.

**En Hemlock:**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free (Liberar)
**Que significa:** Devolver memoria que ya no usas al sistema para que pueda ser reutilizada.

**Analogia:** Devolver un libro de biblioteca para que otros puedan tomarlo prestado.

**En Hemlock:**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Funcion
**Que significa:** Un bloque reutilizable de codigo que toma entradas (parametros) y puede producir una salida (valor de retorno).

**Analogia:** Como una receta - dale ingredientes (entradas), sigue los pasos, obtiene un plato (salida).

**En Hemlock:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Recoleccion de Basura (GC)
**Que significa:** Limpieza automatica de memoria. El runtime periodicamente encuentra memoria no utilizada y la libera por ti.

**Por que Hemlock no lo tiene:** El GC puede causar pausas impredecibles. Hemlock prefiere control explicito - tu decides cuando liberar memoria.

**Nota:** La mayoria de los tipos de Hemlock (strings, arrays, objetos) SI se limpian automaticamente cuando salen de alcance. Solo el `ptr` crudo de `alloc()` necesita `free()` manual.

---

## H

### Heap
**Que significa:** Una region de memoria para datos que necesitan sobrevivir a la funcion actual. Asignas y liberas memoria del heap explicitamente.

**Contraste con:** Stack (almacenamiento automatico y temporal para variables locales)

**En Hemlock:**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Indice
**Que significa:** La posicion de un elemento en un array o string. Comienza en 0 en Hemlock.

**En Hemlock:**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Entero
**Que significa:** Un numero entero sin punto decimal. Puede ser positivo, negativo o cero.

**En Hemlock:**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interprete
**Que significa:** Un programa que lee tu codigo y lo ejecuta directamente, linea por linea.

**Contraste con:** Compilador (traduce el codigo primero, luego ejecuta la traduccion)

**En Hemlock:**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Literal
**Que significa:** Un valor escrito directamente en tu codigo, no calculado.

**Ejemplos:**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Fuga de Memoria
**Que significa:** Olvidar liberar memoria asignada. La memoria permanece reservada pero sin usar, desperdiciando recursos.

**Analogia:** Pedir prestados libros de la biblioteca y nunca devolverlos. Eventualmente, la biblioteca se queda sin libros.

**En Hemlock:**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Metodo
**Que significa:** Una funcion adjunta a un objeto o tipo.

**En Hemlock:**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex
**Que significa:** Un bloqueo que asegura que solo un hilo acceda a algo a la vez. Previene corrupcion de datos cuando multiples hilos tocan datos compartidos.

**Analogia:** Como el seguro de un bano - solo una persona puede usarlo a la vez.

---

## N

### Null
**Que significa:** Un valor especial que significa "nada" o "sin valor."

**En Hemlock:**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Objeto
**Que significa:** Una coleccion de valores con nombre (campos/propiedades) agrupados juntos.

**En Hemlock:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parametro
**Que significa:** Una variable que una funcion espera recibir cuando se llama.

**Tambien llamado:** Argumento (tecnicamente, parametro es en la definicion, argumento es en la llamada)

**En Hemlock:**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Puntero
**Que significa:** Un valor que contiene una direccion de memoria - "apunta a" donde se almacenan los datos.

**Analogia:** Como una direccion de calle. La direccion no es la casa - te dice donde encontrar la casa.

**En Hemlock:**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitivo
**Que significa:** Un tipo basico incorporado que no esta hecho de otros tipos.

**En Hemlock:** `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `null`

---

## R

### Conteo de Referencias (Refcounting)
**Que significa:** Rastrear cuantas cosas estan usando un dato. Cuando nada lo usa mas, limpiarlo automaticamente.

**En Hemlock:** Los strings, arrays, objetos y buffers usan conteo de referencias internamente. No lo ves, pero previene fugas de memoria para los tipos comunes mas usados.

### Valor de Retorno
**Que significa:** El valor que una funcion envia de vuelta cuando termina.

**En Hemlock:**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**Que significa:** Un unico caracter Unicode (codepoint). Puede representar cualquier caracter incluyendo emoji.

**Por que "rune"?** El termino viene de Go. Enfatiza que es un caracter completo, no solo un byte.

**En Hemlock:**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Runtime (Tiempo de Ejecucion)
**Que significa:** El momento en que tu programa esta realmente ejecutandose (en contraposicion al "tiempo de compilacion" cuando se esta traduciendo).

**Tambien:** El codigo de soporte que se ejecuta junto a tu programa (ej., el asignador de memoria).

---

## S

### Alcance (Scope)
**Que significa:** La region de codigo donde una variable existe y puede usarse.

**En Hemlock:**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Stack (Pila)
**Que significa:** Memoria para datos temporales y de corta vida. Se gestiona automaticamente - cuando una funcion retorna, su espacio de stack se reclama.

**Contraste con:** Heap (mas longevos, gestionados manualmente)

### Sentencia
**Que significa:** Una unica instruccion o comando. Las sentencias HACEN cosas; las expresiones PRODUCEN valores.

**Ejemplos:** `let x = 5;`, `print("hi");`, `if (x > 0) { ... }`

### String (Cadena)
**Que significa:** Una secuencia de caracteres de texto.

**En Hemlock:**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Tipado Estructural
**Que significa:** Compatibilidad de tipos basada en estructura (que campos/metodos existen), no en el nombre. Igual que "duck typing."

---

## T

### Hilo (Thread)
**Que significa:** Un camino separado de ejecucion. Multiples hilos pueden ejecutarse simultaneamente en diferentes nucleos de CPU.

**En Hemlock:** `spawn()` crea un nuevo hilo.

### Tipo
**Que significa:** La clase de dato que un valor representa. Determina que operaciones son validas.

**En Hemlock:**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Anotacion de Tipo
**Que significa:** Declarar explicitamente que tipo deberia tener una variable.

**En Hemlock:**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**Que significa:** Una forma de codificar texto que soporta todos los idiomas del mundo y emoji. Cada caracter puede ser de 1 a 4 bytes.

**En Hemlock:** Todos los strings son UTF-8.

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variable
**Que significa:** Un lugar de almacenamiento con nombre que contiene un valor.

**En Hemlock:**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## Referencia Rapida: Que Tipo Deberia Usar?

| Situacion | Usar Esto | Por Que |
|-----------|----------|---------|
| Solo necesito un numero | `let x = 42;` | Hemlock elige el tipo correcto |
| Contar cosas | `i32` | Suficientemente grande para la mayoria de conteos |
| Numeros enormes | `i64` | Cuando i32 no es suficiente |
| Bytes (0-255) | `u8` | Archivos, datos de red |
| Decimales | `f64` | Matematica decimal precisa |
| Valores Si/No | `bool` | Solo `true` o `false` |
| Texto | `string` | Cualquier contenido de texto |
| Un solo caracter | `rune` | Una letra/emoji |
| Lista de cosas | `array` | Coleccion ordenada |
| Campos con nombre | `object` | Agrupar datos relacionados |
| Memoria cruda | `buffer` | Almacenamiento de bytes seguro |
| Trabajo FFI/sistemas | `ptr` | Avanzado, memoria manual |

---

## Ver Tambien

- [Inicio Rapido](getting-started/quick-start.md) - Tu primer programa en Hemlock
- [Sistema de Tipos](language-guide/types.md) - Documentacion completa de tipos
- [Gestion de Memoria](language-guide/memory.md) - Entender la memoria
