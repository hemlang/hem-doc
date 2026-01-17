# Inicio Rapido

Ponga Hemlock en funcionamiento en minutos.

## Su Primer Programa

Cree un archivo llamado `hello.hml`:

```hemlock
print("Hello, Hemlock!");
```

Ejecute con el interprete:

```bash
./hemlock hello.hml
```

O compile a un ejecutable nativo:

```bash
./hemlockc hello.hml -o hello
./hello
```

Salida:
```
Hello, Hemlock!
```

### Interprete vs Compilador

Hemlock proporciona dos formas de ejecutar programas:

| Herramienta | Caso de Uso | Verificacion de Tipos |
|-------------|-------------|----------------------|
| `hemlock` | Scripts rapidos, REPL, desarrollo | Solo en tiempo de ejecucion |
| `hemlockc` | Binarios de produccion, mejor rendimiento | Tiempo de compilacion (por defecto) |

El compilador (`hemlockc`) verifica los tipos de su codigo antes de generar un ejecutable, detectando errores tempranamente.

## Sintaxis Basica

### Variables

```hemlock
// Las variables se declaran con 'let'
let x = 42;
let name = "Alice";
let pi = 3.14159;

// Las anotaciones de tipo son opcionales
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**Importante**: Los puntos y coma son **obligatorios** en Hemlock.

### Tipos

Hemlock tiene un sistema de tipos rico:

```hemlock
// Enteros
let small: i8 = 127;          // 8 bits con signo
let byte: u8 = 255;           // 8 bits sin signo
let num: i32 = 2147483647;    // 32 bits con signo (por defecto)
let big: i64 = 9223372036854775807;  // 64 bits con signo

// Flotantes
let f: f32 = 3.14;            // flotante de 32 bits
let d: f64 = 2.71828;         // flotante de 64 bits (por defecto)

// Cadenas y caracteres
let text: string = "Hello";   // cadena UTF-8
let emoji: rune = '🚀';       // punto de codigo Unicode

// Booleano y nulo
let flag: bool = true;
let empty = null;
```

### Flujo de Control

```hemlock
// Sentencias if
if (x > 0) {
    print("positive");
} else if (x < 0) {
    print("negative");
} else {
    print("zero");
}

// Bucles while
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// Bucles for
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### Funciones

```hemlock
// Funcion con nombre
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// Funcion anonima
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## Trabajando con Cadenas

Las cadenas en Hemlock son **mutables** y **UTF-8**:

```hemlock
let s = "hello";
s[0] = 'H';              // Ahora "Hello"
print(s);

// Metodos de cadena
let upper = s.to_upper();     // "HELLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "ell"

// Concatenacion
let greeting = "Hello" + ", " + "World!";
print(greeting);  // "Hello, World!"
```

## Arreglos

Arreglos dinamicos con tipos mixtos:

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Metodos de arreglo
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// Tipos mixtos permitidos
let mixed = [1, "two", true, null];
```

## Objetos

Objetos al estilo JavaScript:

```hemlock
// Literal de objeto
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // Modificar campo

// Metodos con 'self'
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Gestion de Memoria

Hemlock usa **gestion de memoria manual**:

```hemlock
// Buffer seguro (recomendado)
let buf = buffer(64);   // Asignar 64 bytes
buf[0] = 65;            // Establecer primer byte a 'A'
print(buf[0]);          // 65
free(buf);              // Liberar memoria

// Puntero crudo (avanzado)
let ptr = alloc(100);
memset(ptr, 0, 100);    // Llenar con ceros
free(ptr);
```

**Importante**: Debe liberar con `free()` lo que asigna con `alloc()`.

## Manejo de Errores

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
} finally {
    print("Done");
}
```

## Argumentos de Linea de Comandos

Acceda a los argumentos del programa a traves del arreglo `args`:

```hemlock
// script.hml
print("Script:", args[0]);
print(`Arguments: ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  arg ${i}: ${args[i]}`);
    i = i + 1;
}
```

Ejecute con:
```bash
./hemlock script.hml hello world
```

Salida:
```
Script: script.hml
Arguments: 2
  arg 1: hello
  arg 2: world
```

## E/S de Archivos

```hemlock
// Escribir en archivo
let f = open("data.txt", "w");
f.write("Hello, File!");
f.close();

// Leer de archivo
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Hello, File!"
f2.close();
```

## Que Sigue

Ahora que ha visto lo basico, explore mas:

- [Tutorial](tutorial.md) - Guia completa paso a paso
- [Guia del Lenguaje](../language-guide/syntax.md) - Profundice en todas las caracteristicas
- [Ejemplos](../../examples/) - Programas de ejemplo del mundo real
- [Referencia de API](../reference/builtins.md) - Documentacion completa de la API

## Errores Comunes

### Olvidar los Puntos y Coma

```hemlock
// ❌ ERROR: Falta punto y coma
let x = 42
let y = 10

// ✅ CORRECTO
let x = 42;
let y = 10;
```

### Olvidar Liberar Memoria

```hemlock
// ❌ FUGA DE MEMORIA
let buf = buffer(100);
// ... usar buf ...
// Olvido llamar a free(buf)!

// ✅ CORRECTO
let buf = buffer(100);
// ... usar buf ...
free(buf);
```

### Las Llaves Son Obligatorias

```hemlock
// ❌ ERROR: Faltan llaves
if (x > 0)
    print("positive");

// ✅ CORRECTO
if (x > 0) {
    print("positive");
}
```

## Obteniendo Ayuda

- Lea la [documentacion completa](../README.md)
- Revise el [directorio de ejemplos](../../examples/)
- Vea los [archivos de prueba](../../tests/) para patrones de uso
- Reporte problemas en GitHub
