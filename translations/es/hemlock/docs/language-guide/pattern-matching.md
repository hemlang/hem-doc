# Coincidencia de Patrones

Hemlock proporciona coincidencia de patrones poderosa a través de expresiones `match`, ofreciendo una forma concisa de desestructurar valores, verificar tipos y manejar múltiples casos.

## Sintaxis Básica

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

Las expresiones match evalúan `value` contra cada patrón en orden, retornando el resultado de la expresión del primer brazo que coincida.

## Tipos de Patrones

### Patrones Literales

Coincide contra valores exactos:

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "one",
    42 => "the answer",
    _ => "other"
};
print(msg);  // "the answer"
```

Literales soportados:
- **Enteros**: `0`, `42`, `-5`
- **Flotantes**: `3.14`, `-0.5`
- **Strings**: `"hello"`, `"world"`
- **Booleanos**: `true`, `false`
- **Null**: `null`

### Patrón Comodín (`_`)

Coincide cualquier valor sin vincular:

```hemlock
let x = "anything";
let result = match (x) {
    "specific" => "found it",
    _ => "wildcard matched"
};
```

### Patrones de Vinculación de Variables

Vincula el valor coincidente a una variable:

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "value is " + n  // n se vincula a 100
};
print(result);  // "value is 100"
```

### Patrones OR (`|`)

Coincide múltiples alternativas:

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "small",
    4 | 5 | 6 => "medium",
    _ => "large"
};

// Funciona con strings también
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "exiting",
    "help" | "h" | "?" => "showing help",
    _ => "unknown"
};
```

### Expresiones de Guarda (`if`)

Agregue condiciones a los patrones:

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negative",
    n if n == 0 => "zero",
    n if n < 10 => "small",
    n if n < 100 => "medium",
    n => "large: " + n
};
print(category);  // "medium"

// Guardas complejas
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "even and greater than 10",
    n if n % 2 == 0 => "even",
    n => "odd"
};
```

### Patrones de Tipo

Verifica y vincula basado en tipo:

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "integer: " + num,
    str: string => "string: " + str,
    flag: bool => "boolean: " + flag,
    _ => "other type"
};
print(desc);  // "integer: 42"
```

Tipos soportados: `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Patrones de Desestructuración

### Desestructuración de Objetos

Extraer campos de objetos:

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "point at " + x + "," + y
};
print(result);  // "point at 10,20"

// Con valores literales de campo
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origin",
    { x: 0, y } => "on y-axis at " + y,
    { x, y: 0 } => "on x-axis at " + x,
    { x, y } => "point at " + x + "," + y
};
print(name);  // "origin"
```

### Desestructuración de Arrays

Coincide estructura y elementos de array:

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "empty",
    [x] => "single: " + x,
    [x, y] => "pair: " + x + "," + y,
    [x, y, z] => "triple: " + x + "," + y + "," + z,
    _ => "many elements"
};
print(desc);  // "triple: 1,2,3"

// Con valores literales
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "both zero",
    [1, x] => "starts with 1, second is " + x,
    [x, 1] => "ends with 1",
    _ => "other"
};
print(result);  // "starts with 1, second is 2"
```

### Patrones Rest de Array (`...`)

Capturar elementos restantes:

```hemlock
let nums = [1, 2, 3, 4, 5];

// Cabeza y cola
let result = match (nums) {
    [first, ...rest] => "first: " + first,
    [] => "empty"
};
print(result);  // "first: 1"

// Primeros dos elementos
let result2 = match (nums) {
    [a, b, ...rest] => "first two: " + a + "," + b,
    _ => "too short"
};
print(result2);  // "first two: 1,2"
```

### Desestructuración Anidada

Combine patrones para datos complejos:

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " lives in " + city,
    _ => "unknown"
};
print(result);  // "Alice lives in NYC"

// Objeto conteniendo array
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "first: " + first + ", total: " + count,
    _ => "no items"
};
print(result2);  // "first: 1, total: 3"
```

## Match como Expresión

Match es una expresión que retorna un valor:

```hemlock
// Asignación directa
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// En concatenación de strings
let msg = "Grade: " + match (grade) {
    n if n >= 70 => "passing",
    _ => "failing"
};

// En retorno de función
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positive",
        _ => "negative"
    };
}
```

## Mejores Prácticas de Coincidencia de Patrones

1. **El orden importa**: Los patrones se verifican de arriba hacia abajo; coloque patrones específicos antes de los generales
2. **Use comodines para exhaustividad**: Siempre incluya un `_` de respaldo a menos que esté seguro de que todos los casos están cubiertos
3. **Prefiera guardas sobre condiciones anidadas**: Las guardas hacen la intención más clara
4. **Use desestructuración sobre acceso manual de campos**: Más conciso y seguro

```hemlock
// Bien: Guardas para verificación de rangos
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "below B"
}

// Bien: Desestructurar en lugar de acceder campos
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// Evitar: Patrones anidados excesivamente complejos
// En su lugar, considere dividir en múltiples matches o usar guardas
```

## Comparación con Otros Lenguajes

| Característica | Hemlock | Rust | JavaScript |
|----------------|---------|------|------------|
| Coincidencia básica | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Desestructuración | Sí | Sí | Parcial (switch no desestructura) |
| Guardas | `n if n > 0 =>` | `n if n > 0 =>` | N/A |
| Patrones OR | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Patrones rest | `[a, ...rest]` | `[a, rest @ ..]` | N/A |
| Patrones de tipo | `n: i32` | Tipo vía brazo `match` | N/A |
| Retorna valor | Sí | Sí | No (sentencia) |

## Notas de Implementación

La coincidencia de patrones está implementada tanto en el backend del intérprete como del compilador con paridad completa - ambos producen resultados idénticos para la misma entrada. La característica está disponible en Hemlock v1.8.0+.
