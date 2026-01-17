# Arrays

Hemlock proporciona **arrays dinamicos** con metodos completos para manipulacion y procesamiento de datos. Los arrays pueden contener tipos mezclados y crecer automaticamente segun sea necesario.

## Resumen

```hemlock
// Literales de array
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipos mezclados permitidos
let mixed = [1, "hello", true, null];

// Tamano dinamico
arr.push(6);           // Crece automaticamente
arr.push(7);
print(arr.length);     // 7
```

## Literales de Array

### Sintaxis Basica

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### Arrays Vacios

```hemlock
let arr = [];  // Array vacio

// Agregar elementos despues
arr.push(1);
arr.push(2);
arr.push(3);
```

### Tipos Mezclados

Los arrays pueden contener diferentes tipos:

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3] (array anidado)
```

### Arrays Anidados

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### Arrays con Tipo

Los arrays pueden tener anotaciones de tipo para imponer tipos de elementos:

```hemlock
// Sintaxis de array con tipo
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Verificacion de tipos en tiempo de ejecucion
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "two", 3]; // Error de tiempo de ejecucion: incompatibilidad de tipos

// Arrays anidados con tipo
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Comportamiento de anotacion de tipo:**
- Los elementos se verifican por tipo cuando se agregan al array
- Las incompatibilidades de tipo causan errores de tiempo de ejecucion
- Sin anotacion de tipo, los arrays aceptan tipos mezclados

## Indexacion

### Leer Elementos

Acceso indexado desde cero:

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (primer elemento)
print(arr[4]);  // 50 (ultimo elemento)

// Fuera de limites retorna null (sin error)
print(arr[10]);  // null
```

### Escribir Elementos

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Modificar existente
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Puede asignar mas alla de la longitud actual (crece el array)
arr[5] = 60;    // Crea [10, 20, 3, null, null, 60]
```

### Indices Negativos

**No soportado** - Usar solo indices positivos:

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // ERROR o comportamiento indefinido

// Usar length para el ultimo elemento
print(arr[arr.length - 1]);  // 3
```

## Propiedades

### Propiedad `.length`

Retorna el numero de elementos:

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Array vacio
let empty = [];
print(empty.length);  // 0

// Despues de modificaciones
arr.push(6);
print(arr.length);  // 6
```

## Metodos de Array

Hemlock proporciona 18 metodos de array para manipulacion completa.

### Operaciones de Pila

**`push(value)`** - Agregar elemento al final:
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Remover y retornar ultimo elemento:
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Retorna 5, arr es ahora [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Operaciones de Cola

**`shift()`** - Remover y retornar primer elemento:
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Retorna 1, arr es ahora [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Agregar elemento al principio:
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Insercion y Remocion

**`insert(index, value)`** - Insertar elemento en indice:
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // Insertar 3 en indice 2: [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Insertar al principio: [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Remover y retornar elemento en indice:
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Retorna 3, arr es ahora [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Operaciones de Busqueda

**`find(value)`** - Encontrar primera ocurrencia:
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (indice de primera ocurrencia)
let idx2 = arr.find(99);     // -1 (no encontrado)

// Funciona con cualquier tipo
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - Verificar si array contiene valor:
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Operaciones de Extraccion

**`slice(start, end)`** - Extraer subarray (end exclusivo):
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (indices 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Original sin cambios
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Obtener primer elemento (sin remover):
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (sin remover)
print(arr);                  // [1, 2, 3] (sin cambios)
```

**`last()`** - Obtener ultimo elemento (sin remover):
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (sin remover)
print(arr);                  // [1, 2, 3] (sin cambios)
```

### Operaciones de Transformacion

**`reverse()`** - Invertir array en su lugar:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (modificado)
```

**`join(delimiter)`** - Unir elementos en cadena:
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funciona con tipos mezclados
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - Concatenar con otro array:
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (nuevo array)

// Originales sin cambios
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Operaciones de Utilidad

**`clear()`** - Remover todos los elementos:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Encadenamiento de Metodos

Los metodos que retornan arrays o valores permiten encadenamiento:

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Referencia Completa de Metodos

| Metodo | Parametros | Retorna | Muta | Descripcion |
|--------|------------|---------|------|-------------|
| `push(value)` | any | void | Si | Agregar elemento al final |
| `pop()` | - | any | Si | Remover y retornar ultimo |
| `shift()` | - | any | Si | Remover y retornar primero |
| `unshift(value)` | any | void | Si | Agregar elemento al principio |
| `insert(index, value)` | i32, any | void | Si | Insertar en indice |
| `remove(index)` | i32 | any | Si | Remover y retornar en indice |
| `find(value)` | any | i32 | No | Encontrar primera ocurrencia (-1 si no encontrado) |
| `contains(value)` | any | bool | No | Verificar si contiene valor |
| `slice(start, end)` | i32, i32 | array | No | Extraer subarray (nuevo array) |
| `join(delimiter)` | string | string | No | Unir en cadena |
| `concat(other)` | array | array | No | Concatenar (nuevo array) |
| `reverse()` | - | void | Si | Invertir en su lugar |
| `first()` | - | any | No | Obtener primer elemento |
| `last()` | - | any | No | Obtener ultimo elemento |
| `clear()` | - | void | Si | Remover todos los elementos |
| `map(callback)` | fn | array | No | Transformar cada elemento |
| `filter(predicate)` | fn | array | No | Seleccionar elementos coincidentes |
| `reduce(callback, initial)` | fn, any | any | No | Reducir a valor unico |

## Detalles de Implementacion

### Modelo de Memoria

- **Asignado en heap** - Capacidad dinamica
- **Crecimiento automatico** - Duplica capacidad cuando se excede
- **Sin reduccion automatica** - La capacidad no disminuye
- **Sin verificacion de limites en indexacion** - Usar metodos para seguridad

### Gestion de Capacidad

```hemlock
let arr = [];  // Capacidad inicial: 0

arr.push(1);   // Crece a capacidad 1
arr.push(2);   // Crece a capacidad 2
arr.push(3);   // Crece a capacidad 4 (duplica)
arr.push(4);   // Aun capacidad 4
arr.push(5);   // Crece a capacidad 8 (duplica)
```

### Comparacion de Valores

`find()` y `contains()` usan igualdad de valores:

```hemlock
// Primitivos: comparar por valor
let arr = [1, 2, 3];
arr.contains(2);  // true

// Cadenas: comparar por valor
let words = ["hello", "world"];
words.contains("hello");  // true

// Objetos: comparar por referencia
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (misma referencia)
arr2.contains(obj2);  // false (diferente referencia)
```

## Patrones Comunes

### Operaciones Funcionales (map/filter/reduce)

Los arrays tienen metodos integrados `map`, `filter` y `reduce`:

```hemlock
// map - transformar cada elemento
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - seleccionar elementos coincidentes
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - acumular a valor unico
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Encadenamiento de operaciones funcionales
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Patron: Array como Pila

```hemlock
let stack = [];

// Push a la pila
stack.push(1);
stack.push(2);
stack.push(3);

// Pop de la pila
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Patron: Array como Cola

```hemlock
let queue = [];

// Encolar (agregar al final)
queue.push(1);
queue.push(2);
queue.push(3);

// Desencolar (remover del frente)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Mejores Practicas

1. **Usar metodos sobre indexacion directa** - Verificacion de limites y claridad
2. **Verificar limites** - La indexacion directa no verifica limites
3. **Preferir operaciones inmutables** - Usar `slice()` y `concat()` sobre mutacion
4. **Inicializar con capacidad** - Si conoces el tamano (actualmente no soportado)
5. **Usar `contains()` para membresia** - Mas claro que bucles manuales
6. **Encadenar metodos** - Mas legible que llamadas anidadas

## Errores Comunes

### Error: Indice Directo Fuera de Limites

```hemlock
let arr = [1, 2, 3];

// Sin verificacion de limites!
arr[10] = 99;  // Crea array disperso con nulls
print(arr.length);  // 11 (no 3!)

// Mejor: Usar push() o verificar length
if (arr.length <= 10) {
    arr.push(99);
}
```

### Error: Mutacion vs. Nuevo Array

```hemlock
let arr = [1, 2, 3];

// Muta original
arr.reverse();
print(arr);  // [3, 2, 1]

// Retorna nuevo array
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (sin cambios)
print(sub);  // [3, 2]
```

### Error: Igualdad de Referencia

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Misma referencia: true
arr.contains(obj);  // true

// Diferente referencia: false
arr.contains({ x: 10 });  // false (diferente objeto)
```

### Error: Arrays de Larga Vida

```hemlock
// Los arrays en alcance local se liberan automaticamente, pero los arrays globales/de larga vida necesitan atencion
let global_cache = [];  // Nivel de modulo, persiste hasta fin del programa

fn add_to_cache(item) {
    global_cache.push(item);  // Crece indefinidamente
}

// Para datos de larga vida, considera:
// - Limpiar el array periodicamente: global_cache.clear();
// - Liberar temprano cuando termines: free(global_cache);
```

## Ejemplos

### Ejemplo: Estadisticas de Array

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### Ejemplo: Deduplicacion de Array

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### Ejemplo: Fragmentacion de Array

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### Ejemplo: Aplanamiento de Array

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Array anidado - aplanarlo
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### Ejemplo: Ordenamiento (Burbuja)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Intercambiar
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // Modifica en su lugar
print(numbers);  // [1, 2, 5, 8, 9]
```

## Limitaciones

Limitaciones actuales:

- **Sin verificacion de limites en indexacion** - El acceso directo no se verifica
- **Igualdad de referencia para objetos** - `find()` y `contains()` usan comparacion de referencia
- **Sin desestructuracion de arrays** - Sin sintaxis `let [a, b] = arr`
- **Sin operador spread** - Sin sintaxis `[...arr1, ...arr2]`

**Nota:** Los arrays tienen conteo de referencias y se liberan automaticamente cuando el alcance termina. Ver [Gestion de Memoria](memory.md#conteo-de-referencias-interno) para detalles.

## Temas Relacionados

- [Strings](strings.md) - Metodos de cadena similares a metodos de array
- [Objects](objects.md) - Los arrays tambien son similares a objetos
- [Functions](functions.md) - Funciones de orden superior con arrays
- [Control Flow](control-flow.md) - Iterando sobre arrays

## Ver Tambien

- **Tamano Dinamico**: Los arrays crecen automaticamente con duplicacion de capacidad
- **Metodos**: 18 metodos completos para manipulacion incluyendo map/filter/reduce
- **Memoria**: Ver [Memory](memory.md) para detalles de asignacion de arrays
