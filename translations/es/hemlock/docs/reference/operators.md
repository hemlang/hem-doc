# Referencia de Operadores

Referencia completa para todos los operadores en Hemlock, incluyendo precedencia, asociatividad y comportamiento.

---

## Descripcion General

Hemlock proporciona operadores estilo C con reglas de precedencia explicitas. Todos los operadores siguen reglas de tipado estrictas con promocion automatica de tipos donde sea aplicable.

---

## Operadores Aritmeticos

### Aritmeticos Binarios

| Operador | Nombre         | Ejemplo    | Descripcion                  |
|----------|----------------|------------|------------------------------|
| `+`      | Suma           | `a + b`    | Sumar dos valores            |
| `-`      | Resta          | `a - b`    | Restar b de a                |
| `*`      | Multiplicacion | `a * b`    | Multiplicar dos valores      |
| `/`      | Division       | `a / b`    | Dividir a entre b            |

**Promocion de Tipos:**
Los resultados siguen reglas de promocion de tipos (vea [Sistema de Tipos](type-system.md#reglas-de-promocion-de-tipos)).

**Ejemplos:**
```hemlock
let a = 10 + 5;        // 15 (i32)
let b = 10 - 3;        // 7 (i32)
let c = 4 * 5;         // 20 (i32)
let d = 20 / 4;        // 5 (i32)

// Division flotante
let e = 10.0 / 3.0;    // 3.333... (f64)

// Tipos mixtos
let f: u8 = 10;
let g: i32 = 20;
let h = f + g;         // 30 (i32, promocionado)
```

**Division por Cero:**
- Division entera por cero: Error en tiempo de ejecucion
- Division flotante por cero: Retorna `inf` o `-inf`

---

### Aritmeticos Unarios

| Operador | Nombre   | Ejemplo | Descripcion          |
|----------|----------|---------|----------------------|
| `-`      | Negacion | `-a`    | Negar valor          |
| `+`      | Mas      | `+a`    | Identidad (sin efecto) |

**Ejemplos:**
```hemlock
let a = 5;
let b = -a;            // -5
let c = +a;            // 5 (sin cambio)

let x = -3.14;         // -3.14
```

---

## Operadores de Comparacion

| Operador | Nombre                | Ejemplo    | Retorna |
|----------|-----------------------|------------|---------|
| `==`     | Igual                 | `a == b`   | `bool`  |
| `!=`     | No igual              | `a != b`   | `bool`  |
| `<`      | Menor que             | `a < b`    | `bool`  |
| `>`      | Mayor que             | `a > b`    | `bool`  |
| `<=`     | Menor o igual que     | `a <= b`   | `bool`  |
| `>=`     | Mayor o igual que     | `a >= b`   | `bool`  |

**Promocion de Tipos:**
Los operandos se promocionan antes de la comparacion.

**Ejemplos:**
```hemlock
print(5 == 5);         // true
print(10 != 5);        // true
print(3 < 7);          // true
print(10 > 5);         // true
print(5 <= 5);         // true
print(10 >= 5);        // true

// Comparacion de strings
print("hello" == "hello");  // true
print("abc" < "def");       // true (lexicografico)

// Tipos mixtos
let a: u8 = 10;
let b: i32 = 10;
print(a == b);         // true (promocionado a i32)
```

---

## Operadores Logicos

| Operador | Nombre      | Ejemplo      | Descripcion              |
|----------|-------------|--------------|--------------------------|
| `&&`     | AND Logico  | `a && b`     | Verdadero si ambos son verdaderos |
| `||`     | OR Logico   | `a || b`     | Verdadero si alguno es verdadero |
| `!`      | NOT Logico  | `!a`         | Negar booleano           |

**Evaluacion de Cortocircuito:**
- `&&` - Se detiene en el primer valor falso
- `||` - Se detiene en el primer valor verdadero

**Ejemplos:**
```hemlock
let a = true;
let b = false;

print(a && b);         // false
print(a || b);         // true
print(!a);             // false
print(!b);             // true

// Cortocircuito
if (x != 0 && (10 / x) > 2) {
    print("seguro");
}

if (x == 0 || (10 / x) > 2) {
    print("seguro");
}
```

---

## Operadores de Bits

**Restriccion:** Solo tipos enteros (i8-i64, u8-u64)

### Binarios de Bits

| Operador | Nombre           | Ejemplo    | Descripcion              |
|----------|------------------|------------|--------------------------|
| `&`      | AND de Bits      | `a & b`    | AND cada bit             |
| `|`      | OR de Bits       | `a | b`    | OR cada bit              |
| `^`      | XOR de Bits      | `a ^ b`    | XOR cada bit             |
| `<<`     | Desplazamiento izq | `a << b` | Desplazar izquierda b bits |
| `>>`     | Desplazamiento der | `a >> b` | Desplazar derecha b bits |

**Preservacion de Tipo:**
El tipo del resultado coincide con los tipos de operandos (con promocion de tipos).

**Ejemplos:**
```hemlock
let a = 12;  // 1100 en binario
let b = 10;  // 1010 en binario

print(a & b);          // 8  (1000)
print(a | b);          // 14 (1110)
print(a ^ b);          // 6  (0110)
print(a << 2);         // 48 (110000)
print(a >> 1);         // 6  (110)
```

**Ejemplo Sin Signo:**
```hemlock
let c: u8 = 15;        // 00001111
let d: u8 = 7;         // 00000111

print(c & d);          // 7  (00000111)
print(c | d);          // 15 (00001111)
print(c ^ d);          // 8  (00001000)
```

**Comportamiento de Desplazamiento Derecho:**
- Tipos con signo: Desplazamiento aritmetico (extiende signo)
- Tipos sin signo: Desplazamiento logico (llena con ceros)

---

### Unarios de Bits

| Operador | Nombre        | Ejemplo | Descripcion              |
|----------|---------------|---------|--------------------------|
| `~`      | NOT de Bits   | `~a`    | Invertir todos los bits  |

**Ejemplos:**
```hemlock
let a = 12;            // 00001100 (i32)
print(~a);             // -13 (complemento a dos)

let b: u8 = 15;        // 00001111
print(~b);             // 240 (11110000)
```

---

## Operadores de String

### Concatenacion

| Operador | Nombre         | Ejemplo    | Descripcion        |
|----------|----------------|------------|--------------------|
| `+`      | Concatenacion  | `a + b`    | Unir strings       |

**Ejemplos:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"

// String + rune
let greeting = "Hello" + '!';      // "Hello!"

// Rune + string
let prefix = '>' + " Message";     // "> Message"
```

---

## Operadores de Asignacion

### Asignacion Basica

| Operador | Nombre     | Ejemplo    | Descripcion              |
|----------|------------|------------|--------------------------|
| `=`      | Asignacion | `a = b`    | Asignar valor a variable |

**Ejemplos:**
```hemlock
let x = 10;
x = 20;

let arr = [1, 2, 3];
arr[0] = 99;

let obj = { x: 10 };
obj.x = 20;
```

### Asignacion Compuesta

#### Asignacion Compuesta Aritmetica

| Operador | Nombre            | Ejemplo    | Equivalente         |
|----------|-------------------|------------|---------------------|
| `+=`     | Asignar suma      | `a += b`   | `a = a + b`        |
| `-=`     | Asignar resta     | `a -= b`   | `a = a - b`        |
| `*=`     | Asignar mult      | `a *= b`   | `a = a * b`        |
| `/=`     | Asignar div       | `a /= b`   | `a = a / b`        |
| `%=`     | Asignar modulo    | `a %= b`   | `a = a % b`        |

**Ejemplos:**
```hemlock
let x = 10;
x += 5;      // x ahora es 15
x -= 3;      // x ahora es 12
x *= 2;      // x ahora es 24
x /= 4;      // x ahora es 6

let count = 0;
count += 1;  // Incrementar por 1
```

#### Asignacion Compuesta de Bits

| Operador | Nombre                 | Ejemplo     | Equivalente          |
|----------|------------------------|-------------|----------------------|
| `&=`     | Asignar AND de bits    | `a &= b`    | `a = a & b`         |
| `\|=`   | Asignar OR de bits     | `a \|= b`   | `a = a \| b`        |
| `^=`     | Asignar XOR de bits    | `a ^= b`    | `a = a ^ b`         |
| `<<=`    | Asignar desp izq       | `a <<= b`   | `a = a << b`        |
| `>>=`    | Asignar desp der       | `a >>= b`   | `a = a >> b`        |

**Ejemplos:**
```hemlock
let flags = 0b1111;
flags &= 0b0011;   // flags ahora es 0b0011 (enmascarar bits superiores)
flags |= 0b1000;   // flags ahora es 0b1011 (establecer un bit)
flags ^= 0b0001;   // flags ahora es 0b1010 (alternar un bit)

let x = 1;
x <<= 4;           // x ahora es 16 (desplazar izquierda por 4)
x >>= 2;           // x ahora es 4 (desplazar derecha por 2)
```

### Incremento/Decremento

| Operador | Nombre     | Ejemplo | Descripcion              |
|----------|------------|---------|--------------------------|
| `++`     | Incremento | `a++`   | Incrementar por 1 (postfijo) |
| `--`     | Decremento | `a--`   | Decrementar por 1 (postfijo) |

**Ejemplos:**
```hemlock
let i = 0;
i++;         // i ahora es 1
i++;         // i ahora es 2
i--;         // i ahora es 1

// Comun en bucles
for (let j = 0; j < 10; j++) {
    print(j);
}
```

**Nota:** Tanto `++` como `--` son operadores postfijos (el valor se retorna antes del incremento/decremento)

---

## Operadores de Seguridad Null

### Coalescencia Null (`??`)

Retorna el operando izquierdo si no es null, de lo contrario retorna el operando derecho.

| Operador | Nombre            | Ejemplo      | Descripcion                    |
|----------|-------------------|--------------|--------------------------------|
| `??`     | Coalescencia null | `a ?? b`     | Retornar a si no es null, sino b |

**Ejemplos:**
```hemlock
let name = null;
let display = name ?? "Anonimo";  // "Anonimo"

let value = 42;
let result = value ?? 0;            // 42

// Encadenamiento
let a = null;
let b = null;
let c = "encontrado";
let result2 = a ?? b ?? c;          // "encontrado"

// Con llamadas a funcion
fn get_config() { return null; }
let config = get_config() ?? { default: true };
```

---

### Encadenamiento Opcional (`?.`)

Accede a propiedades o llama metodos de forma segura en valores potencialmente null.

| Operador | Nombre               | Ejemplo        | Descripcion                      |
|----------|----------------------|----------------|----------------------------------|
| `?.`     | Encadenamiento opcional | `a?.b`      | Retornar a.b si a no es null, sino null |
| `?.[`    | Indice opcional      | `a?.[0]`       | Retornar a[0] si a no es null, sino null |
| `?.(`    | Llamada opcional     | `a?.()`        | Llamar a() si a no es null, sino null |

**Ejemplos:**
```hemlock
let user = null;
let name = user?.name;              // null (sin error)

let person = { name: "Alice", address: null };
let city = person?.address?.city;   // null (navegacion segura)

// Con arrays
let arr = null;
let first = arr?.[0];               // null

let items = [1, 2, 3];
let second = items?.[1];            // 2

// Con llamadas a metodos
let obj = { greet: fn() { return "Hola"; } };
let greeting = obj?.greet?.();      // "Hola"

let empty = null;
let result = empty?.method?.();     // null
```

**Comportamiento:**
- Si el operando izquierdo es null, toda la expresion cortocircuita a null
- Si el operando izquierdo no es null, el acceso procede normalmente
- Puede encadenarse para acceso profundo a propiedades

---

## Operadores de Acceso a Miembros

### Operador Punto

| Operador | Nombre              | Ejemplo      | Descripcion           |
|----------|---------------------|--------------|-----------------------|
| `.`      | Acceso a miembro    | `obj.field`  | Acceder campo de objeto |
| `.`      | Acceso a propiedad  | `arr.length` | Acceder propiedad     |

**Ejemplos:**
```hemlock
// Acceso a campo de objeto
let person = { name: "Alice", age: 30 };
print(person.name);        // "Alice"

// Propiedad de array
let arr = [1, 2, 3];
print(arr.length);         // 3

// Propiedad de string
let s = "hello";
print(s.length);           // 5

// Llamada a metodo
let result = s.to_upper(); // "HELLO"
```

---

### Operador de Indice

| Operador | Nombre  | Ejemplo   | Descripcion          |
|----------|---------|-----------|----------------------|
| `[]`     | Indice  | `arr[i]`  | Acceder elemento     |

**Ejemplos:**
```hemlock
// Indexacion de array
let arr = [10, 20, 30];
print(arr[0]);             // 10
arr[1] = 99;

// Indexacion de string (retorna rune)
let s = "hello";
print(s[0]);               // 'h'
s[0] = 'H';                // "Hello"

// Indexacion de buffer
let buf = buffer(10);
buf[0] = 65;
print(buf[0]);             // 65
```

---

## Operador de Llamada a Funcion

| Operador | Nombre           | Ejemplo      | Descripcion        |
|----------|------------------|--------------|--------------------|
| `()`     | Llamada a funcion | `f(a, b)`   | Llamar funcion     |

**Ejemplos:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(5, 3);    // 8

// Llamada a metodo
let s = "hello";
let upper = s.to_upper();  // "HELLO"

// Llamada integrada
print("mensaje");
```

---

## Precedencia de Operadores

Los operadores se listan de mayor a menor precedencia:

| Precedencia | Operadores                  | Descripcion                    | Asociatividad |
|-------------|----------------------------|--------------------------------|---------------|
| 1          | `()` `[]` `.` `?.`         | Llamada, indice, acceso miembro, encadenamiento opcional | Izq-a-der |
| 2          | `++` `--`                  | Incremento/decremento postfijo | Izq-a-der |
| 3          | `!` `~` `-` (unario) `+` (unario) | NOT logico, NOT de bits, negacion | Der-a-izq |
| 4          | `*` `/` `%`                | Multiplicacion, division, modulo | Izq-a-der |
| 5          | `+` `-`                    | Suma, resta          | Izq-a-der |
| 6          | `<<` `>>`                  | Desplazamientos de bits        | Izq-a-der |
| 7          | `<` `<=` `>` `>=`          | Relacionales                   | Izq-a-der |
| 8          | `==` `!=`                  | Igualdad                       | Izq-a-der |
| 9          | `&`                        | AND de bits                    | Izq-a-der |
| 10         | `^`                        | XOR de bits                    | Izq-a-der |
| 11         | `|`                        | OR de bits                     | Izq-a-der |
| 12         | `&&`                       | AND logico                     | Izq-a-der |
| 13         | `||`                       | OR logico                      | Izq-a-der |
| 14         | `??`                       | Coalescencia null              | Izq-a-der |
| 15         | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | Asignacion | Der-a-izq |

---

## Ejemplos de Precedencia

### Ejemplo 1: Aritmetica y Comparacion
```hemlock
let result = 5 + 3 * 2;
// Evaluado como: 5 + (3 * 2) = 11
// Multiplicacion tiene mayor precedencia que suma

let cmp = 10 > 5 + 3;
// Evaluado como: 10 > (5 + 3) = true
// Suma tiene mayor precedencia que comparacion
```

### Ejemplo 2: Operadores de Bits
```hemlock
let result1 = 12 | 10 & 8;
// Evaluado como: 12 | (10 & 8) = 12 | 8 = 12
// & tiene mayor precedencia que |

let result2 = 8 | 1 << 2;
// Evaluado como: 8 | (1 << 2) = 8 | 4 = 12
// Desplazamiento tiene mayor precedencia que OR de bits

// Use parentesis para claridad
let result3 = (5 & 3) | (2 << 1);
// Evaluado como: 1 | 4 = 5
```

### Ejemplo 3: Operadores Logicos
```hemlock
let result = true || false && false;
// Evaluado como: true || (false && false) = true
// && tiene mayor precedencia que ||

let cmp = 5 < 10 && 10 < 20;
// Evaluado como: (5 < 10) && (10 < 20) = true
// Comparacion tiene mayor precedencia que &&
```

### Ejemplo 4: Usando Parentesis
```hemlock
// Sin parentesis
let a = 2 + 3 * 4;        // 14

// Con parentesis
let b = (2 + 3) * 4;      // 20

// Expresion compleja
let c = (a + b) * (a - b);
```

---

## Comportamiento de Operadores Especifico por Tipo

### Division (Siempre Flotante)

El operador `/` **siempre retorna un flotante** (f64), independientemente de los tipos de operandos:

```hemlock
print(10 / 3);             // 3.333... (f64)
print(5 / 2);              // 2.5 (f64)
print(10.0 / 4.0);         // 2.5 (f64)
print(-7 / 3);             // -2.333... (f64)
```

Esto previene el bug comun de truncamiento entero inesperado.

### Division Entera (div / divi)

Para division entera (como division de enteros en otros lenguajes), use las funciones `div()` y `divi()`:

```hemlock
// div(a, b) - division entera retornando flotante
print(div(5, 2));          // 2 (f64)
print(div(-7, 3));         // -3 (f64)  -- piso hacia -infinito

// divi(a, b) - division entera retornando entero
print(divi(5, 2));         // 2 (i64)
print(divi(-7, 3));        // -3 (i64)
print(typeof(divi(5, 2))); // i64
```

**Funciones matematicas que retornan enteros:**
Para otras operaciones de redondeo que retornan enteros:

```hemlock
print(floori(3.7));        // 3 (i64)
print(ceili(3.2));         // 4 (i64)
print(roundi(3.5));        // 4 (i64)
print(trunci(3.9));        // 3 (i64)

// Estos pueden usarse directamente como indices de array
let arr = [10, 20, 30, 40];
print(arr[floori(1.9)]);   // 20 (indice 1)
```

### Comparacion de Strings

Los strings se comparan lexicograficamente:

```hemlock
print("abc" < "def");      // true
print("apple" > "banana"); // false
print("hello" == "hello"); // true
```

### Comparacion con Null

```hemlock
let x = null;

print(x == null);          // true
print(x != null);          // false
```

### Errores de Tipo

Algunas operaciones no estan permitidas entre tipos incompatibles:

```hemlock
// ERROR: No se pueden usar operadores de bits en flotantes
let x = 3.14 & 2.71;

// ERROR: No se pueden usar operadores de bits en strings
let y = "hello" & "world";

// OK: Promocion de tipo para aritmetica
let a: u8 = 10;
let b: i32 = 20;
let c = a + b;             // i32 (promocionado)
```

---

## Ver Tambien

- [Sistema de Tipos](type-system.md) - Reglas de promocion y conversion de tipos
- [Funciones Integradas](builtins.md) - Operaciones integradas
- [API de Strings](string-api.md) - Concatenacion y metodos de strings
