# Referencia de la API de Arrays

Referencia completa para el tipo array de Hemlock y sus 18 metodos.

---

## Descripcion General

Los arrays en Hemlock son secuencias **dinamicas, asignadas en el heap** que pueden contener tipos mixtos. Proporcionan metodos completos para la manipulacion y procesamiento de datos.

**Caracteristicas Principales:**
- Tamano dinamico (crecimiento automatico)
- Indexacion desde cero
- Tipos mixtos permitidos
- 18 metodos integrados
- Asignados en el heap con seguimiento de capacidad

---

## Tipo Array

**Tipo:** `array`

**Propiedades:**
- `.length` - Numero de elementos (i32)

**Sintaxis Literal:** Corchetes `[elem1, elem2, ...]`

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// Tipos mixtos
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// Array vacio
let empty = [];
print(empty.length);   // 0
```

---

## Indexacion

Los arrays soportan indexacion basada en cero usando `[]`:

**Acceso de Lectura:**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**Acceso de Escritura:**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**Nota:** La indexacion directa no tiene verificacion de limites. Use metodos para mayor seguridad.

---

## Propiedades de Array

### .length

Obtiene el numero de elementos en el array.

**Tipo:** `i32`

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// La longitud cambia dinamicamente
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## Metodos de Array

### Operaciones de Pila

#### push

Agrega un elemento al final del array.

**Firma:**
```hemlock
array.push(value: any): null
```

**Parametros:**
- `value` - Elemento a agregar

**Retorna:** `null`

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

Elimina y retorna el ultimo elemento.

**Firma:**
```hemlock
array.pop(): any
```

**Retorna:** Ultimo elemento (eliminado del array)

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**Error:** Error en tiempo de ejecucion si el array esta vacio.

---

### Operaciones de Cola

#### shift

Elimina y retorna el primer elemento.

**Firma:**
```hemlock
array.shift(): any
```

**Retorna:** Primer elemento (eliminado del array)

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**Error:** Error en tiempo de ejecucion si el array esta vacio.

---

#### unshift

Agrega un elemento al inicio del array.

**Firma:**
```hemlock
array.unshift(value: any): null
```

**Parametros:**
- `value` - Elemento a agregar

**Retorna:** `null`

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### Insercion y Eliminacion

#### insert

Inserta un elemento en un indice especifico.

**Firma:**
```hemlock
array.insert(index: i32, value: any): null
```

**Parametros:**
- `index` - Posicion donde insertar (basada en 0)
- `value` - Elemento a insertar

**Retorna:** `null`

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// Insertar al final
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**Comportamiento:** Desplaza los elementos en y despues del indice hacia la derecha.

---

#### remove

Elimina y retorna el elemento en el indice.

**Firma:**
```hemlock
array.remove(index: i32): any
```

**Parametros:**
- `index` - Posicion de donde eliminar (basada en 0)

**Retorna:** Elemento eliminado

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**Comportamiento:** Desplaza los elementos despues del indice hacia la izquierda.

**Error:** Error en tiempo de ejecucion si el indice esta fuera de limites.

---

### Busqueda y Encontrar

#### find

Encuentra la primera ocurrencia de un valor.

**Firma:**
```hemlock
array.find(value: any): i32
```

**Parametros:**
- `value` - Valor a buscar

**Retorna:** Indice de la primera ocurrencia, o `-1` si no se encuentra

**Ejemplos:**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1 (no encontrado)

// Encontrar el primer duplicado
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1 (primera ocurrencia)
```

**Comparacion:** Usa igualdad de valor para primitivos y strings.

---

#### contains

Verifica si el array contiene un valor.

**Firma:**
```hemlock
array.contains(value: any): bool
```

**Parametros:**
- `value` - Valor a buscar

**Retorna:** `true` si se encuentra, `false` en caso contrario

**Ejemplos:**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// Funciona con strings
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### Segmentacion y Extraccion

#### slice

Extrae un subarray por rango (fin exclusivo).

**Firma:**
```hemlock
array.slice(start: i32, end: i32): array
```

**Parametros:**
- `start` - Indice inicial (basado en 0, inclusivo)
- `end` - Indice final (exclusivo)

**Retorna:** Nuevo array con elementos desde [start, end)

**Muta:** No (retorna nuevo array)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// Segmento vacio
let empty = arr.slice(2, 2); // []
```

---

#### first

Obtiene el primer elemento sin eliminarlo.

**Firma:**
```hemlock
array.first(): any
```

**Retorna:** Primer elemento

**Muta:** No

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3] (sin cambios)
```

**Error:** Error en tiempo de ejecucion si el array esta vacio.

---

#### last

Obtiene el ultimo elemento sin eliminarlo.

**Firma:**
```hemlock
array.last(): any
```

**Retorna:** Ultimo elemento

**Muta:** No

**Ejemplos:**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3] (sin cambios)
```

**Error:** Error en tiempo de ejecucion si el array esta vacio.

---

### Manipulacion de Arrays

#### reverse

Invierte el array en su lugar.

**Firma:**
```hemlock
array.reverse(): null
```

**Retorna:** `null`

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

Elimina todos los elementos del array.

**Firma:**
```hemlock
array.clear(): null
```

**Retorna:** `null`

**Muta:** Si (modifica el array en su lugar)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### Combinacion de Arrays

#### concat

Concatena con otro array.

**Firma:**
```hemlock
array.concat(other: array): array
```

**Parametros:**
- `other` - Array a concatenar

**Retorna:** Nuevo array con elementos de ambos arrays

**Muta:** No (retorna nuevo array)

**Ejemplos:**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3] (sin cambios)
print(b);                    // [4, 5, 6] (sin cambios)

// Encadenar concatenaciones
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### Operaciones Funcionales

#### map

Transforma cada elemento usando una funcion de callback.

**Firma:**
```hemlock
array.map(callback: fn): array
```

**Parametros:**
- `callback` - Funcion que toma un elemento y retorna el valor transformado

**Retorna:** Nuevo array con elementos transformados

**Muta:** No (retorna nuevo array)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

Selecciona elementos que coinciden con un predicado.

**Firma:**
```hemlock
array.filter(predicate: fn): array
```

**Parametros:**
- `predicate` - Funcion que toma un elemento y retorna bool

**Retorna:** Nuevo array con elementos donde el predicado retorno true

**Muta:** No (retorna nuevo array)

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

Reduce el array a un solo valor usando un acumulador.

**Firma:**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**Parametros:**
- `callback` - Funcion que toma (acumulador, elemento) y retorna nuevo acumulador
- `initial` - Valor inicial para el acumulador

**Retorna:** Valor acumulado final

**Muta:** No

**Ejemplos:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// Encontrar el valor maximo
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### Conversion a String

#### join

Une elementos en un string con un delimitador.

**Firma:**
```hemlock
array.join(delimiter: string): string
```

**Parametros:**
- `delimiter` - String a colocar entre elementos

**Retorna:** String con todos los elementos unidos

**Ejemplos:**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funciona con tipos mixtos
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// Delimitador vacio
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**Comportamiento:** Convierte automaticamente todos los elementos a strings.

---

## Encadenamiento de Metodos

Los metodos de array pueden encadenarse para operaciones concisas:

**Ejemplos:**
```hemlock
// Encadenar slice y join
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// Encadenar concat y slice
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// Encadenamiento complejo
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## Resumen Completo de Metodos

### Metodos que Mutan

Metodos que modifican el array en su lugar:

| Metodo     | Firma                      | Retorna   | Descripcion                    |
|------------|----------------------------|-----------|--------------------------------|
| `push`     | `(value: any)`             | `null`    | Agregar al final               |
| `pop`      | `()`                       | `any`     | Eliminar del final             |
| `shift`    | `()`                       | `any`     | Eliminar del inicio            |
| `unshift`  | `(value: any)`             | `null`    | Agregar al inicio              |
| `insert`   | `(index: i32, value: any)` | `null`    | Insertar en indice             |
| `remove`   | `(index: i32)`             | `any`     | Eliminar en indice             |
| `reverse`  | `()`                       | `null`    | Invertir en su lugar           |
| `clear`    | `()`                       | `null`    | Eliminar todos los elementos   |

### Metodos que No Mutan

Metodos que retornan nuevos valores sin modificar el original:

| Metodo     | Firma                      | Retorna   | Descripcion                    |
|------------|----------------------------|-----------|--------------------------------|
| `find`     | `(value: any)`             | `i32`     | Encontrar primera ocurrencia   |
| `contains` | `(value: any)`             | `bool`    | Verificar si contiene valor    |
| `slice`    | `(start: i32, end: i32)`   | `array`   | Extraer subarray               |
| `first`    | `()`                       | `any`     | Obtener primer elemento        |
| `last`     | `()`                       | `any`     | Obtener ultimo elemento        |
| `concat`   | `(other: array)`           | `array`   | Concatenar arrays              |
| `join`     | `(delimiter: string)`      | `string`  | Unir elementos en string       |
| `map`      | `(callback: fn)`           | `array`   | Transformar cada elemento      |
| `filter`   | `(predicate: fn)`          | `array`   | Seleccionar elementos que coincidan |
| `reduce`   | `(callback: fn, initial: any)` | `any` | Reducir a un solo valor        |

---

## Patrones de Uso

### Uso como Pila

```hemlock
let stack = [];

// Push de elementos
stack.push(1);
stack.push(2);
stack.push(3);

// Pop de elementos
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### Uso como Cola

```hemlock
let queue = [];

// Encolar
queue.push(1);
queue.push(2);
queue.push(3);

// Desencolar
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### Transformacion de Arrays

```hemlock
// Filtrar (manual)
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// Mapear (manual)
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### Construir Arrays

```hemlock
let arr = [];

// Construir array con bucle
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## Detalles de Implementacion

**Gestion de Capacidad:**
- Los arrays crecen automaticamente cuando es necesario
- La capacidad se duplica cuando se excede
- Sin control manual de capacidad

**Comparacion de Valores:**
- `find()` y `contains()` usan igualdad de valor
- Funciona correctamente para primitivos y strings
- Objetos/arrays se comparan por referencia

**Memoria:**
- Asignados en el heap
- Sin liberacion automatica (gestion manual de memoria)
- Sin verificacion de limites en acceso directo por indice

---

## Ver Tambien

- [Sistema de Tipos](type-system.md) - Detalles del tipo array
- [API de Strings](string-api.md) - Resultados de join() en strings
- [Operadores](operators.md) - Operador de indexacion de arrays
