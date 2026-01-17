# Flujo de Control

Hemlock proporciona flujo de control estilo C familiar con llaves obligatorias y sintaxis explícita. Esta guía cubre condicionales, bucles, sentencias switch y operadores.

## Resumen

Características de flujo de control disponibles:

- `if`/`else`/`else if` - Ramas condicionales
- Bucles `while` - Iteración basada en condiciones
- Bucles `for` - Iteración estilo C y for-in
- `loop` - Bucles infinitos (más limpio que `while (true)`)
- Sentencias `switch` - Ramificación múltiple
- `break`/`continue` - Control de bucles
- Etiquetas de bucle - break/continue dirigido para bucles anidados
- `defer` - Ejecución diferida (limpieza)
- Operadores booleanos: `&&`, `||`, `!`
- Operadores de comparación: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Operadores bit a bit: `&`, `|`, `^`, `<<`, `>>`, `~`

## Sentencias If

### If/Else Básico

```hemlock
if (x > 10) {
    print("large");
} else {
    print("small");
}
```

**Reglas:**
- Las llaves son **siempre requeridas** para todas las ramas
- Las condiciones deben estar encerradas en paréntesis
- Sin llaves opcionales (a diferencia de C)

### If Sin Else

```hemlock
if (x > 0) {
    print("positive");
}
// No se necesita rama else
```

### Cadenas Else-If

```hemlock
if (x > 100) {
    print("very large");
} else if (x > 50) {
    print("large");
} else if (x > 10) {
    print("medium");
} else {
    print("small");
}
```

**Nota:** `else if` es azúcar sintáctico para sentencias if anidadas. Estos son equivalentes:

```hemlock
// else if (azúcar sintáctico)
if (a) {
    foo();
} else if (b) {
    bar();
}

// If anidado equivalente
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### Sentencias If Anidadas

```hemlock
if (x > 0) {
    if (x < 10) {
        print("single digit positive");
    } else {
        print("multi-digit positive");
    }
} else {
    print("non-positive");
}
```

## Bucles While

Iteración basada en condiciones:

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**Bucles infinitos (estilo antiguo):**
```hemlock
while (true) {
    // ... hacer trabajo
    if (should_exit) {
        break;
    }
}
```

**Nota:** Para bucles infinitos, prefiera la palabra clave `loop` (ver abajo).

## Loop (Bucle Infinito)

La palabra clave `loop` proporciona una sintaxis más limpia para bucles infinitos:

```hemlock
loop {
    // ... hacer trabajo
    if (should_exit) {
        break;
    }
}
```

**Equivalente a `while (true)` pero más explícito sobre la intención.**

### Bucle Básico con Break

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Imprime: 0, 1, 2, 3, 4
```

### Bucle con Continue

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // Omite imprimir 3
    }
    print(i);
}
// Imprime: 1, 2, 4, 5
```

### Bucles Anidados

```hemlock
let x = 0;
loop {
    if (x >= 2) { break; }
    let y = 0;
    loop {
        if (y >= 3) { break; }
        print(x * 10 + y);
        y = y + 1;
    }
    x = x + 1;
}
// Imprime: 0, 1, 2, 10, 11, 12
```

### Cuándo Usar Loop

- **Use `loop`** para bucles intencionalmente infinitos que salen vía `break`
- **Use `while`** cuando hay una condición de terminación natural
- **Use `for`** cuando itera un número conocido de veces o sobre una colección

## Bucles For

### For Estilo C

Bucle for clásico de tres partes:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Componentes:**
- **Inicializador**: `let i = 0` - Se ejecuta una vez antes del bucle
- **Condición**: `i < 10` - Se verifica antes de cada iteración
- **Actualización**: `i = i + 1` - Se ejecuta después de cada iteración

**Ámbito:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i no es accesible aquí (ámbito del bucle)
```

### Bucles For-In

Iterar sobre elementos de array:

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // Imprime cada elemento
}
```

**Con índice y valor:**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Index: ${i}, Value: ${arr[i]}`);
}
```

## Sentencias Switch

Ramificación múltiple basada en valor:

### Switch Básico

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("one");
        break;
    case 2:
        print("two");
        break;
    case 3:
        print("three");
        break;
}
```

### Switch con Default

```hemlock
let color = "blue";

switch (color) {
    case "red":
        print("stop");
        break;
    case "yellow":
        print("slow");
        break;
    case "green":
        print("go");
        break;
    default:
        print("unknown color");
        break;
}
```

**Reglas:**
- `default` coincide cuando ningún otro caso coincide
- `default` puede aparecer en cualquier lugar del cuerpo del switch
- Solo se permite un caso default

### Comportamiento de Fall-Through

Los casos sin `break` caen al siguiente caso (comportamiento estilo C). Esto es **intencional** y puede usarse para agrupar casos:

```hemlock
let grade = 85;

switch (grade) {
    case 100:
    case 95:
    case 90:
        print("A");
        break;
    case 85:
    case 80:
        print("B");
        break;
    default:
        print("C or below");
        break;
}
```

**Ejemplo de fallthrough explícito:**
```hemlock
let day = 3;

switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Weekday");
        break;
    case 6:
    case 7:
        print("Weekend");
        break;
}
```

**Importante:** A diferencia de algunos lenguajes modernos, Hemlock NO requiere una palabra clave `fallthrough` explícita. Los casos automáticamente caen al siguiente a menos que terminen con `break`, `return` o `throw`. Siempre use `break` para prevenir fallthrough no intencionado.

### Switch con Return

En funciones, `return` sale del switch inmediatamente:

```hemlock
fn get_day_name(day: i32): string {
    switch (day) {
        case 1:
            return "Monday";
        case 2:
            return "Tuesday";
        case 3:
            return "Wednesday";
        default:
            return "Unknown";
    }
}
```

### Tipos de Valor en Switch

Switch funciona con cualquier tipo de valor:

```hemlock
// Enteros
switch (count) {
    case 0: print("zero"); break;
    case 1: print("one"); break;
}

// Strings
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// Booleanos
switch (flag) {
    case true: print("on"); break;
    case false: print("off"); break;
}
```

**Nota:** Los casos se comparan usando igualdad de valores.

## Break y Continue

### Break

Sale del bucle o switch más interno:

```hemlock
// En bucles
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // Sale del bucle
    }
    print(i);
    i = i + 1;
}

// En switch
switch (x) {
    case 1:
        print("one");
        break;  // Sale del switch
    case 2:
        print("two");
        break;
}
```

### Continue

Salta a la siguiente iteración del bucle:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // Omite la iteración cuando i es 5
    }
    print(i);  // Imprime 0,1,2,3,4,6,7,8,9
}
```

**Diferencia:**
- `break` - Sale del bucle completamente
- `continue` - Salta a la siguiente iteración

## Etiquetas de Bucle

Las etiquetas de bucle permiten que `break` y `continue` apunten a bucles externos específicos en lugar de solo al bucle más interno. Esto es útil para bucles anidados donde necesita controlar un bucle externo desde uno interno.

### Break con Etiqueta

Salir de un bucle externo desde un bucle interno:

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // Sale del bucle while externo
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// Imprime: 0, 1, 2, 10 (se detiene en i=1, j=1)
```

### Continue con Etiqueta

Saltar a la siguiente iteración de un bucle externo:

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // Omite el resto del bucle interno, continúa el externo
        }
        print(i * 10 + j);
    }
}
// Cuando i=2, j=1: salta a la siguiente iteración externa
```

### Etiquetas con Bucles For

Las etiquetas funcionan con todos los tipos de bucle:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 3; y = y + 1) {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
    }
}
```

### Etiquetas con Bucles For-In

```hemlock
let arr1 = [1, 2, 3];
let arr2 = [10, 20, 30];

outer: for (let a in arr1) {
    for (let b in arr2) {
        if (a == 2 && b == 20) {
            break outer;
        }
        print(a * 100 + b);
    }
}
```

### Etiquetas con Palabra Clave Loop

```hemlock
let x = 0;
outer: loop {
    let y = 0;
    loop {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
        y = y + 1;
        if (y >= 3) { break; }
    }
    x = x + 1;
    if (x >= 3) { break; }
}
```

### Múltiples Etiquetas

Puede tener etiquetas en diferentes niveles de anidamiento:

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // Salta a la siguiente iteración del bucle medio
            }
            if (a == 1 && b == 1) {
                break outer;      // Sale del bucle más externo
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### Break/Continue Sin Etiqueta con Bucles Etiquetados

`break` y `continue` sin etiqueta siguen funcionando normalmente (afectando al bucle más interno), incluso cuando los bucles externos tienen etiquetas:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // Solo sale del bucle interno
        }
        print(x * 10 + y);
    }
}
// Imprime: 0, 1, 10, 11, 20, 21
```

### Sintaxis de Etiquetas

- Las etiquetas son identificadores seguidos de dos puntos
- Las etiquetas deben preceder inmediatamente a una sentencia de bucle (`while`, `for`, `loop`)
- Los nombres de etiquetas siguen las reglas de identificadores (letras, dígitos, guiones bajos)
- Convenciones comunes: `outer`, `inner`, `row`, `col`, nombres descriptivos

## Sentencia Defer

La sentencia `defer` programa código para ejecutarse cuando la función actual retorna. Esto es útil para operaciones de limpieza como cerrar archivos, liberar recursos o liberar bloqueos.

### Defer Básico

```hemlock
fn example() {
    print("start");
    defer print("cleanup");  // Se ejecuta cuando la función retorna
    print("end");
}

example();
// Salida:
// start
// end
// cleanup
```

**Comportamiento clave:**
- Las sentencias diferidas se ejecutan **después** de que el cuerpo de la función se complete
- Las sentencias diferidas se ejecutan **antes** de que la función retorne a su llamador
- Las sentencias diferidas siempre se ejecutan, incluso si la función lanza una excepción

### Múltiples Defers (Orden LIFO)

Cuando se usan múltiples sentencias `defer`, se ejecutan en **orden inverso** (Último en Entrar, Primero en Salir):

```hemlock
fn example() {
    defer print("first");   // Se ejecuta último
    defer print("second");  // Se ejecuta segundo
    defer print("third");   // Se ejecuta primero
    print("body");
}

example();
// Salida:
// body
// third
// second
// first
```

Este orden LIFO es intencional - coincide con el orden natural para la limpieza de recursos anidados (cerrar recursos internos antes que los externos).

### Defer con Return

Las sentencias diferidas se ejecutan antes de que `return` transfiera el control:

```hemlock
fn get_value(): i32 {
    defer print("cleanup");
    print("before return");
    return 42;
}

let result = get_value();
print("result:", result);
// Salida:
// before return
// cleanup
// result: 42
```

### Defer con Excepciones

Las sentencias diferidas se ejecutan incluso cuando se lanza una excepción:

```hemlock
fn risky() {
    defer print("cleanup 1");
    defer print("cleanup 2");
    print("before throw");
    throw "error!";
    print("after throw");  // Nunca se alcanza
}

try {
    risky();
} catch (e) {
    print("Caught:", e);
}
// Salida:
// before throw
// cleanup 2
// cleanup 1
// Caught: error!
```

### Patrón de Limpieza de Recursos

El caso de uso principal para `defer` es asegurar que los recursos se limpien:

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // Siempre cierra, incluso en error

    let content = file.read();
    // ... procesar contenido ...

    // El archivo se cierra automáticamente cuando la función retorna
}
```

**Sin defer (propenso a errores):**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // Si esto lanza, file.close() nunca se llama!
    process(content);
    file.close();
}
```

### Defer con Closures

Defer puede usar closures para capturar estado:

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Releasing resource");
        release(resource);
    }();  // Nota: expresión de función invocada inmediatamente

    use_resource(resource);
}
```

### Cuándo Usar Defer

**Use defer para:**
- Cerrar archivos y conexiones de red
- Liberar memoria asignada
- Liberar bloqueos y mutexes
- Limpieza en cualquier función que adquiera recursos

**Defer vs Finally:**
- `defer` es más simple para limpieza de un solo recurso
- `try/finally` es mejor para manejo de errores complejo con recuperación

### Mejores Prácticas

1. **Coloque defer inmediatamente después de adquirir un recurso:**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... usar archivo ...
   ```

2. **Use múltiples defers para múltiples recursos:**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // Ambos archivos se cerrarán en orden inverso
   ```

3. **Recuerde el orden LIFO para recursos dependientes:**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner se libera antes que outer (orden de dependencia correcto)
   ```

## Operadores Booleanos

### AND Lógico (`&&`)

Ambas condiciones deben ser verdaderas:

```hemlock
if (x > 0 && x < 10) {
    print("single digit positive");
}
```

**Evaluación de cortocircuito:**
```hemlock
if (false && expensive_check()) {
    // expensive_check() nunca se llama
}
```

### OR Lógico (`||`)

Al menos una condición debe ser verdadera:

```hemlock
if (x < 0 || x > 100) {
    print("out of range");
}
```

**Evaluación de cortocircuito:**
```hemlock
if (true || expensive_check()) {
    // expensive_check() nunca se llama
}
```

### NOT Lógico (`!`)

Niega el valor booleano:

```hemlock
if (!is_valid) {
    print("invalid");
}

if (!(x > 10)) {
    // Igual que: if (x <= 10)
}
```

## Operadores de Comparación

### Igualdad

```hemlock
if (x == 10) { }    // Igual
if (x != 10) { }    // No igual
```

Funciona con todos los tipos:
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### Relacionales

```hemlock
if (x < 10) { }     // Menor que
if (x > 10) { }     // Mayor que
if (x <= 10) { }    // Menor o igual
if (x >= 10) { }    // Mayor o igual
```

**Se aplica promoción de tipos:**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true (i32 promovido a i64)
```

## Operadores Bit a Bit

Hemlock proporciona operadores bit a bit para manipulación de enteros. Estos funcionan **solo con tipos enteros** (i8-i64, u8-u64).

### Operadores Bit a Bit Binarios

**AND Bit a Bit (`&`)**
```hemlock
let a = 12;  // 1100 en binario
let b = 10;  // 1010 en binario
print(a & b);   // 8 (1000)
```

**OR Bit a Bit (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**XOR Bit a Bit (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**Desplazamiento a la Izquierda (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - desplaza a la izquierda 2
```

**Desplazamiento a la Derecha (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - desplaza a la derecha 1
```

### Operador Bit a Bit Unario

**NOT Bit a Bit (`~`)**
```hemlock
let a = 12;
print(~a);      // -13 (complemento a dos)

let c: u8 = 15;   // 00001111 en binario
print(~c);        // 240 (11110000) en u8
```

### Ejemplos Bit a Bit

**Con tipos sin signo:**
```hemlock
let c: u8 = 15;   // 00001111 en binario
let d: u8 = 7;    // 00000111 en binario

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - en u8
```

**Preservación de tipos:**
```hemlock
// Las operaciones bit a bit preservan el tipo de los operandos
let x: u8 = 255;
let result = ~x;  // result es u8 con valor 0

let y: i32 = 100;
let result2 = y << 2;  // result2 es i32 con valor 400
```

**Patrones comunes:**
```hemlock
// Verificar si un bit está establecido
if (flags & 0x04) {
    print("bit 2 is set");
}

// Establecer un bit
flags = flags | 0x08;

// Limpiar un bit
flags = flags & ~0x02;

// Alternar un bit
flags = flags ^ 0x01;
```

### Precedencia de Operadores

Los operadores bit a bit siguen la precedencia estilo C:

1. `~` (NOT unario) - más alta, mismo nivel que `!` y `-`
2. `<<`, `>>` (desplazamientos) - mayor que comparaciones, menor que `+`/`-`
3. `&` (AND bit a bit) - mayor que `^` y `|`
4. `^` (XOR bit a bit) - entre `&` y `|`
5. `|` (OR bit a bit) - menor que `&` y `^`, mayor que `&&`
6. `&&`, `||` (lógicos) - precedencia más baja

**Ejemplos:**
```hemlock
// & tiene mayor precedencia que |
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// Desplazamiento tiene mayor precedencia que operadores bit a bit
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// Use paréntesis para claridad
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**Notas importantes:**
- Los operadores bit a bit solo funcionan con tipos enteros (no flotantes, strings, etc.)
- La promoción de tipos sigue las reglas estándar (tipos más pequeños se promueven a más grandes)
- El desplazamiento a la derecha (`>>`) es aritmético para tipos con signo, lógico para sin signo
- Las cantidades de desplazamiento no se verifican por rango (el comportamiento depende de la plataforma para desplazamientos grandes)

## Precedencia de Operadores (Completa)

De mayor a menor precedencia:

1. **Unarios**: `!`, `-`, `~`
2. **Multiplicativos**: `*`, `/`, `%`
3. **Aditivos**: `+`, `-`
4. **Desplazamiento**: `<<`, `>>`
5. **Relacionales**: `<`, `>`, `<=`, `>=`
6. **Igualdad**: `==`, `!=`
7. **AND Bit a Bit**: `&`
8. **XOR Bit a Bit**: `^`
9. **OR Bit a Bit**: `|`
10. **AND Lógico**: `&&`
11. **OR Lógico**: `||`

**Use paréntesis para claridad:**
```hemlock
// Poco claro
if (a || b && c) { }

// Claro
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## Patrones Comunes

### Patrón: Validación de Entrada

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### Patrón: Verificación de Rango

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("valid score");
}
```

### Patrón: Máquina de Estados

```hemlock
let state = "start";

while (true) {
    switch (state) {
        case "start":
            print("Starting...");
            state = "running";
            break;

        case "running":
            if (should_pause) {
                state = "paused";
            } else if (should_stop) {
                state = "stopped";
            }
            break;

        case "paused":
            if (should_resume) {
                state = "running";
            }
            break;

        case "stopped":
            print("Stopped");
            break;
    }

    if (state == "stopped") {
        break;
    }
}
```

### Patrón: Iteración con Filtrado

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Imprimir solo números pares
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // Omitir números impares
    }
    print(arr[i]);
}
```

### Patrón: Salida Temprana

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Salida temprana
        }
    }
    return -1;  // No encontrado
}
```

## Mejores Prácticas

1. **Siempre use llaves** - Incluso para bloques de una sola sentencia (requerido por sintaxis)
2. **Condiciones explícitas** - Use `x == 0` en lugar de `!x` para claridad
3. **Evite anidamiento profundo** - Extraiga condiciones anidadas a funciones
4. **Use retornos tempranos** - Reduzca el anidamiento con cláusulas de guarda
5. **Divida condiciones complejas** - Sepárelas en variables booleanas nombradas
6. **Default en switch** - Siempre incluya un caso default
7. **Comente fall-through** - Haga explícito el fall-through intencional

## Errores Comunes

### Error: Asignación en Condición

```hemlock
// Esto NO está permitido (sin asignación en condiciones)
if (x = 10) { }  // ERROR: Error de sintaxis

// Use comparación en su lugar
if (x == 10) { }  // OK
```

### Error: Break Faltante en Switch

```hemlock
// Fall-through no intencional
switch (x) {
    case 1:
        print("one");
        // Falta break - cae al siguiente!
    case 2:
        print("two");  // Se ejecuta tanto para 1 como para 2
        break;
}

// Corrección: Agregar break
switch (x) {
    case 1:
        print("one");
        break;  // Ahora correcto
    case 2:
        print("two");
        break;
}
```

### Error: Ámbito de Variable de Bucle

```hemlock
// i tiene ámbito del bucle
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // ERROR: i no está definida aquí
```

## Ejemplos

### Ejemplo: FizzBuzz

```hemlock
for (let i = 1; i <= 100; i = i + 1) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else if (i % 3 == 0) {
        print("Fizz");
    } else if (i % 5 == 0) {
        print("Buzz");
    } else {
        print(i);
    }
}
```

### Ejemplo: Verificador de Primos

```hemlock
fn is_prime(n: i32): bool {
    if (n < 2) {
        return false;
    }

    let i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
```

### Ejemplo: Sistema de Menú

```hemlock
fn menu() {
    while (true) {
        print("1. Start");
        print("2. Settings");
        print("3. Exit");

        let choice = get_input();

        switch (choice) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Goodbye!");
                return;
            default:
                print("Invalid choice");
                break;
        }
    }
}
```

## Temas Relacionados

- [Funciones](functions.md) - Flujo de control con llamadas a funciones y retornos
- [Manejo de Errores](error-handling.md) - Flujo de control con excepciones
- [Tipos](types.md) - Conversiones de tipos en condiciones

## Ver También

- **Sintaxis**: Consulte [Sintaxis](syntax.md) para detalles de sintaxis de sentencias
- **Operadores**: Consulte [Tipos](types.md) para promoción de tipos en operaciones
