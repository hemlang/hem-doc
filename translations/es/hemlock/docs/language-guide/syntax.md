# Resumen de Sintaxis

Este documento cubre las reglas fundamentales de sintaxis y la estructura de los programas Hemlock.

## Reglas Fundamentales de Sintaxis

### Los Punto y Coma Son Obligatorios

A diferencia de JavaScript o Python, los punto y coma son **siempre requeridos** al final de las sentencias:

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**Esto causara un error:**
```hemlock
let x = 42  // ERROR: Falta punto y coma
let y = 10  // ERROR: Falta punto y coma
```

### Las Llaves Son Siempre Requeridas

Todos los bloques de flujo de control deben usar llaves, incluso para sentencias individuales:

```hemlock
// CORRECTO
if (x > 0) {
    print("positivo");
}

// ERROR: Faltan llaves
if (x > 0)
    print("positivo");
```

### Comentarios

```hemlock
// Este es un comentario de una linea

/*
   Este es un
   comentario de multiples lineas
*/

let x = 42;  // Comentario en linea
```

## Variables

### Declaracion

Las variables se declaran con `let`:

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Anotaciones de Tipo (Opcionales)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hello";
```

### Constantes

Usa `const` para valores inmutables:

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Intentar reasignar una constante resultara en un error de tiempo de ejecucion: "Cannot assign to const variable".

## Expresiones

### Operadores Aritmeticos

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - Suma
print(a - b);   // 7  - Resta
print(a * b);   // 30 - Multiplicacion
print(a / b);   // 3  - Division (entera)
```

### Operadores de Comparacion

```hemlock
print(a == b);  // false - Igual
print(a != b);  // true  - No igual
print(a > b);   // true  - Mayor que
print(a < b);   // false - Menor que
print(a >= b);  // true  - Mayor o igual
print(a <= b);  // false - Menor o igual
```

### Operadores Logicos

```hemlock
let x = true;
let y = false;

print(x && y);  // false - AND
print(x || y);  // true  - OR
print(!x);      // false - NOT
```

### Operadores de Bits

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - AND de bits
print(a | b);   // 14 - OR de bits
print(a ^ b);   // 6  - XOR de bits
print(a << 2);  // 48 - Desplazamiento a la izquierda
print(a >> 1);  // 6  - Desplazamiento a la derecha
print(~a);      // -13 - NOT de bits
```

### Precedencia de Operadores

De mayor a menor:

1. `()` - Agrupacion
2. `!`, `~`, `-` (unario) - Operadores unarios
3. `*`, `/` - Multiplicacion, Division
4. `+`, `-` - Suma, Resta
5. `<<`, `>>` - Desplazamientos de bits
6. `<`, `<=`, `>`, `>=` - Comparaciones
7. `==`, `!=` - Igualdad
8. `&` - AND de bits
9. `^` - XOR de bits
10. `|` - OR de bits
11. `&&` - AND logico
12. `||` - OR logico

**Ejemplos:**
```hemlock
let x = 2 + 3 * 4;      // 14 (no 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Flujo de Control

### Sentencias If

```hemlock
if (condition) {
    // cuerpo
}

if (condition) {
    // rama then
} else {
    // rama else
}

if (condition1) {
    // rama 1
} else if (condition2) {
    // rama 2
} else {
    // rama por defecto
}
```

### Bucles While

```hemlock
while (condition) {
    // cuerpo
}
```

**Ejemplo:**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Bucles For

**For estilo C:**
```hemlock
for (initializer; condition; increment) {
    // cuerpo
}
```

**Ejemplo:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (arrays):**
```hemlock
for (let item in array) {
    // cuerpo
}
```

**Ejemplo:**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Sentencias Switch

```hemlock
switch (expression) {
    case value1:
        // cuerpo
        break;
    case value2:
        // cuerpo
        break;
    default:
        // cuerpo por defecto
        break;
}
```

**Ejemplo:**
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
        print("Other");
        break;
}
```

### Break y Continue

```hemlock
// Break: salir del bucle
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue: saltar a la siguiente iteracion
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Funciones

### Funciones con Nombre

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // cuerpo
    return value;
}
```

**Ejemplo:**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Funciones Anonimas

```hemlock
let func = fn(params) {
    // cuerpo
};
```

**Ejemplo:**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Anotaciones de Tipo (Opcionales)

```hemlock
// Sin anotaciones (tipos inferidos)
fn greet(name) {
    return "Hello, " + name;
}

// Con anotaciones (verificados en tiempo de ejecucion)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Objetos

### Literales de Objeto

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Ejemplo:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Metodos

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Ejemplo:**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Definiciones de Tipo

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Ejemplo:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Arrays

### Literales de Array

```hemlock
let arr = [element1, element2, element3];
```

**Ejemplo:**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];
let empty = [];
```

### Indexacion de Arrays

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // Modificar elemento
```

## Manejo de Errores

### Try/Catch

```hemlock
try {
    // codigo riesgoso
} catch (e) {
    // manejar error
}
```

### Try/Finally

```hemlock
try {
    // codigo riesgoso
} finally {
    // siempre se ejecuta
}
```

### Try/Catch/Finally

```hemlock
try {
    // codigo riesgoso
} catch (e) {
    // manejar error
} finally {
    // limpieza
}
```

### Throw

```hemlock
throw expression;
```

**Ejemplo:**
```hemlock
if (x < 0) {
    throw "x must be positive";
}
```

### Panic

```hemlock
panic(message);
```

**Ejemplo:**
```hemlock
panic("unrecoverable error");
```

## Modulos (Experimental)

### Sentencias Export

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Sentencias Import

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Async (Experimental)

### Funciones Async

```hemlock
async fn function_name(params): return_type {
    // cuerpo
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Canales

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (Interfaz de Funcion Foranea)

### Importar Biblioteca Compartida

```hemlock
import "library_name.so";
```

### Declarar Funcion Externa

```hemlock
extern fn function_name(param: type): return_type;
```

**Ejemplo:**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Literales

### Literales Enteros

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // Auto i64

// Hexadecimal (prefijo 0x)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Binario (prefijo 0b)
let bin = 0b1010;
let bin2 = 0b11110000;

// Octal (prefijo 0o)
let oct = 0o777;
let oct2 = 0O123;

// Separadores numericos para legibilidad
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Literales de Punto Flotante

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // Notacion cientifica
let sci2 = 2.5E+3;       // E mayuscula tambien funciona
let no_lead = .5;        // Sin cero inicial (0.5)
let sep = 3.14_159_265;  // Separadores numericos
```

### Literales de Cadena

```hemlock
let s = "hello";
let escaped = "line1\nline2\ttabbed";
let quote = "She said \"hello\"";

// Secuencias de escape hexadecimales
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Secuencias de escape Unicode
let emoji = "\u{1F600}";               // grinning face
let heart = "\u{2764}";                // heart
let mixed = "Hello \u{1F30D}!";        // Hello earth!
```

**Secuencias de escape:**
- `\n` - nueva linea
- `\t` - tabulador
- `\r` - retorno de carro
- `\\` - barra invertida
- `\"` - comilla doble
- `\'` - comilla simple
- `\0` - caracter nulo
- `\xNN` - escape hexadecimal (2 digitos)
- `\u{XXXX}` - escape unicode (1-6 digitos)

### Literales Rune

```hemlock
let ch = 'A';
let emoji = 'rocket';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Literales Booleanos

```hemlock
let t = true;
let f = false;
```

### Literal Null

```hemlock
let nothing = null;
```

## Reglas de Alcance

### Alcance de Bloque

Las variables tienen alcance en el bloque mas cercano:

```hemlock
let x = 1;  // Alcance externo

if (true) {
    let x = 2;  // Alcance interno (oculta el externo)
    print(x);   // 2
}

print(x);  // 1
```

### Alcance de Funcion

Las funciones crean su propio alcance:

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // Puede leer alcance externo
}

foo();
// print(local);  // ERROR: 'local' no definido aqui
```

### Alcance de Clausura

Las clausuras capturan variables del alcance que las contiene:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Captura 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Espacios en Blanco y Formato

### Indentacion

Hemlock no impone una indentacion especifica, pero se recomiendan 4 espacios:

```hemlock
fn example() {
    if (true) {
        print("indented");
    }
}
```

### Saltos de Linea

Las sentencias pueden abarcar multiples lineas:

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Sentencia Loop

La palabra clave `loop` proporciona una sintaxis mas limpia para bucles infinitos:

```hemlock
loop {
    // ... hacer trabajo
    if (done) {
        break;
    }
}
```

Esto es equivalente a `while (true)` pero hace la intencion mas clara.

## Palabras Clave Reservadas

Las siguientes palabras clave estan reservadas en Hemlock:

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Siguientes Pasos

- [Sistema de Tipos](types.md) - Aprende sobre el sistema de tipos de Hemlock
- [Flujo de Control](control-flow.md) - Profundiza en las estructuras de control
- [Funciones](functions.md) - Domina funciones y clausuras
- [Gestion de Memoria](memory.md) - Entiende punteros y buffers
