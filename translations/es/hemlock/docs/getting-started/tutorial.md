# Tutorial de Hemlock

Una guia completa paso a paso para aprender Hemlock.

## Tabla de Contenidos

1. [Hola Mundo](#hola-mundo)
2. [Variables y Tipos](#variables-y-tipos)
3. [Aritmetica y Operaciones](#aritmetica-y-operaciones)
4. [Flujo de Control](#flujo-de-control)
5. [Funciones](#funciones)
6. [Cadenas y Runes](#cadenas-y-runes)
7. [Arreglos](#arreglos)
8. [Objetos](#objetos)
9. [Gestion de Memoria](#gestion-de-memoria)
10. [Manejo de Errores](#manejo-de-errores)
11. [E/S de Archivos](#es-de-archivos)
12. [Poniendolo Todo Junto](#poniendolo-todo-junto)

## Hola Mundo

Comencemos con el tradicional primer programa:

```hemlock
print("Hello, World!");
```

Guardelo como `hello.hml` y ejecute:

```bash
./hemlock hello.hml
```

**Puntos Clave:**
- `print()` es una funcion incorporada que escribe a stdout
- Las cadenas se encierran entre comillas dobles
- Los puntos y coma son **obligatorios**

## Variables y Tipos

### Declarando Variables

```hemlock
// Declaracion basica de variable
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### Anotaciones de Tipo

Aunque los tipos se infieren por defecto, puede ser explicito:

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### Inferencia de Tipos

Hemlock infiere tipos basandose en los valores:

```hemlock
let small = 42;              // i32 (cabe en 32 bits)
let large = 5000000000;      // i64 (muy grande para i32)
let decimal = 3.14;          // f64 (por defecto para flotantes)
let text = "hello";          // string
let flag = true;             // bool
```

### Verificacion de Tipos

```hemlock
// Verificar tipos con typeof()
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hello"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## Aritmetica y Operaciones

### Aritmetica Basica

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3 (division entera)
print(a == b);  // false
print(a > b);   // true
```

### Promocion de Tipos

Al mezclar tipos, Hemlock promueve al tipo mas grande/preciso:

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result es f64 (10.0 + 3.5 = 13.5)

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### Operaciones de Bits

```hemlock
let a = 12;  // 1100 en binario
let b = 10;  // 1010 en binario

print(a & b);   // 8  (AND)
print(a | b);   // 14 (OR)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24 (desplazamiento izquierda)
print(a >> 1);  // 6  (desplazamiento derecha)
print(~a);      // -13 (NOT)
```

## Flujo de Control

### Sentencias If

```hemlock
let x = 10;

if (x > 0) {
    print("positive");
} else if (x < 0) {
    print("negative");
} else {
    print("zero");
}
```

**Nota:** Las llaves son **siempre requeridas**, incluso para sentencias individuales.

### Bucles While

```hemlock
let count = 0;
while (count < 5) {
    print(`Count: ${count}`);
    count = count + 1;
}
```

### Bucles For

```hemlock
// Bucle for estilo C
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// Bucle for-in (arreglos)
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Item: ${item}`);
}
```

### Sentencias Switch

```hemlock
let day = 3;

switch (day) {
    case 1:
        print("Monday");
        break;
    case 2:
        print("Tuesday");
        break;
    case 3:
        print("Wednesday");
        break;
    default:
        print("Other day");
        break;
}
```

### Break y Continue

```hemlock
// Break: salir del bucle anticipadamente
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Imprime: 0, 1, 2, 3, 4

// Continue: saltar a la siguiente iteracion
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// Imprime: 0, 1, 3, 4
```

## Funciones

### Funciones con Nombre

```hemlock
fn greet(name: string): string {
    return "Hello, " + name + "!";
}

let message = greet("Alice");
print(message);  // "Hello, Alice!"
```

### Funciones Anonimas

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### Recursion

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Clausuras

Las funciones capturan su entorno:

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

### Funciones de Orden Superior

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## Cadenas y Runes

### Conceptos Basicos de Cadenas

Las cadenas son **mutables** y **UTF-8**:

```hemlock
let s = "hello";
print(s.length);      // 5 (conteo de caracteres)
print(s.byte_length); // 5 (conteo de bytes)

// Mutacion
s[0] = 'H';
print(s);  // "Hello"
```

### Metodos de Cadena

```hemlock
let text = "  Hello, World!  ";

// Conversion de mayusculas/minusculas
print(text.to_upper());  // "  HELLO, WORLD!  "
print(text.to_lower());  // "  hello, world!  "

// Recorte
print(text.trim());      // "Hello, World!"

// Extraccion de subcadena
let hello = text.substr(2, 5);  // "Hello"
let world = text.slice(9, 14);  // "World"

// Busqueda
let pos = text.find("World");   // 9
let has = text.contains("o");   // true

// Division
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// Reemplazo
let s = "hello world".replace("world", "there");
print(s);  // "hello there"
```

### Runes (Puntos de Codigo Unicode)

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Concatenacion Rune + String
let msg = '>' + " Important";
print(msg);  // "> Important"

// Convertir entre rune y entero
let code: i32 = ch;     // 65 (codigo ASCII)
let r: rune = 128640;   // U+1F680 (🚀)
```

## Arreglos

### Conceptos Basicos de Arreglos

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Modificar elementos
numbers[2] = 99;
print(numbers[2]);  // 99
```

### Metodos de Arreglo

```hemlock
let arr = [10, 20, 30];

// Agregar/eliminar al final
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40, arr ahora es [10, 20, 30]

// Agregar/eliminar al principio
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5, arr ahora es [10, 20, 30]

// Insertar/eliminar en indice
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// Busqueda
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// Porcion
let slice = arr.slice(0, 2);  // [10, 15]

// Unir a cadena
let text = arr.join(", ");    // "10, 15, 30"
```

### Iteracion

```hemlock
let items = ["apple", "banana", "cherry"];

// Bucle for-in
for (let item in items) {
    print(item);
}

// Iteracion manual
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## Objetos

### Literales de Objeto

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// Agregar/modificar campos
person.email = "alice@example.com";
person.age = 31;
```

### Metodos y `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### Definiciones de Tipo (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // Opcional con valor por defecto
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // Duck typing valida la estructura

print(typeof(typed));   // "Person"
print(typed.active);    // true (por defecto aplicado)
```

### Serializacion JSON

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// Objeto a JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON a Objeto
let restored = json.deserialize();
print(restored.name);  // "test"
```

## Gestion de Memoria

### Buffers Seguros (Recomendado)

```hemlock
// Asignar buffer
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// Establecer valores (con verificacion de limites)
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Acceder a valores
print(buf[0]);  // 65

// Debe liberar cuando termine
free(buf);
```

### Punteros Crudos (Avanzado)

```hemlock
// Asignar memoria cruda
let ptr = alloc(100);

// Llenar con ceros
memset(ptr, 0, 100);

// Copiar datos
let src = alloc(50);
memcpy(ptr, src, 50);

// Liberar ambos
free(src);
free(ptr);
```

### Funciones de Memoria

```hemlock
// Reasignar
let p = alloc(64);
p = realloc(p, 128);  // Redimensionar a 128 bytes
free(p);

// Asignacion tipada (futuro)
// let arr = talloc(i32, 100);  // Arreglo de 100 i32s
```

## Manejo de Errores

### Try/Catch

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Error: " + e);
}
// Salida: Error: division by zero
```

### Bloque Finally

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Error: " + e);
} finally {
    // Siempre se ejecuta
    if (file != null) {
        file.close();
    }
}
```

### Lanzando Objetos

```hemlock
try {
    throw { code: 404, message: "Not found" };
} catch (e) {
    print(`Error ${e.code}: ${e.message}`);
}
// Salida: Error 404: Not found
```

### Panic (Errores Irrecuperables)

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x must be non-negative");
    }
    return x * 2;
}

validate(-5);  // El programa termina con: panic: x must be non-negative
```

## E/S de Archivos

### Leyendo Archivos

```hemlock
// Leer archivo completo
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// Leer numero especifico de bytes
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // Leer 100 bytes
f2.close();
```

### Escribiendo Archivos

```hemlock
// Escribir texto
let f = open("output.txt", "w");
f.write("Hello, File!\n");
f.write("Second line\n");
f.close();

// Agregar al archivo
let f2 = open("output.txt", "a");
f2.write("Appended line\n");
f2.close();
```

### E/S Binaria

```hemlock
// Escribir datos binarios
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// Leer datos binarios
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### Propiedades de Archivo

```hemlock
let f = open("/path/to/file.txt", "r");

print(f.path);    // "/path/to/file.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## Poniendolo Todo Junto

Construyamos un programa simple de contador de palabras:

```hemlock
// wordcount.hml - Contar palabras en un archivo

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // Dividir por espacios en blanco y contar
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Error reading file: " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// Programa principal
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Word count: ${words}`);
    }
}
```

Ejecute con:
```bash
./hemlock wordcount.hml data.txt
```

## Proximos Pasos

Felicitaciones! Ha aprendido lo basico de Hemlock. Esto es lo que puede explorar a continuacion:

- [Async y Concurrencia](../advanced/async-concurrency.md) - Multi-hilos verdaderos
- [FFI](../advanced/ffi.md) - Llamar funciones C
- [Manejo de Senales](../advanced/signals.md) - Senales de proceso
- [Referencia de API](../reference/builtins.md) - Documentacion completa de la API
- [Ejemplos](../../examples/) - Mas programas del mundo real

## Ejercicios de Practica

Intente construir estos programas para practicar:

1. **Calculadora**: Implemente una calculadora simple con +, -, *, /
2. **Copia de Archivo**: Copie un archivo a otro
3. **Fibonacci**: Genere numeros de Fibonacci
4. **Parser JSON**: Lea y analice archivos JSON
5. **Procesador de Texto**: Encuentre y reemplace texto en archivos

Feliz programacion con Hemlock!
