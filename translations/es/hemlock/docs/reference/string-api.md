# Referencia de la API de Strings

Referencia completa para el tipo string de Hemlock y sus 19 metodos.

---

## Descripcion General

Los strings en Hemlock son secuencias **codificadas en UTF-8, mutables, asignadas en el heap** con soporte completo de Unicode. Todas las operaciones trabajan con **puntos de codigo** (caracteres), no bytes.

**Caracteristicas Principales:**
- Codificacion UTF-8 (U+0000 a U+10FFFF)
- Mutable (puede modificar caracteres en su lugar)
- Indexacion basada en puntos de codigo
- 19 metodos integrados
- Concatenacion automatica con el operador `+`

---

## Tipo String

**Tipo:** `string`

**Propiedades:**
- `.length` - Numero de puntos de codigo (caracteres)
- `.byte_length` - Numero de bytes UTF-8

**Sintaxis Literal:** Comillas dobles `"texto"`

**Ejemplos:**
```hemlock
let s = "hello";
print(s.length);        // 5 (puntos de codigo)
print(s.byte_length);   // 5 (bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (un punto de codigo)
print(emoji.byte_length);   // 4 (cuatro bytes UTF-8)
```

---

## Indexacion

Los strings soportan indexacion basada en puntos de codigo usando `[]`:

**Acceso de Lectura:**
```hemlock
let s = "hello";
let ch = s[0];          // Retorna rune 'h'
```

**Acceso de Escritura:**
```hemlock
let s = "hello";
s[0] = 'H';             // Mutar con rune (ahora "Hello")
```

**Ejemplo UTF-8:**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (un punto de codigo)
print(text[3]);         // '!'
```

---

## Concatenacion

Use el operador `+` para concatenar strings y runes:

**String + String:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Count: " + typeof(42); // "Count: 42"
```

**String + Rune:**
```hemlock
let greeting = "Hello" + '!';      // "Hello!"
let decorated = "Text" + '✓';      // "Text✓"
```

**Rune + String:**
```hemlock
let prefix = '>' + " Message";     // "> Message"
let bullet = '•' + " Item";        // "• Item"
```

**Concatenaciones Multiples:**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## Propiedades de String

### .length

Obtiene el numero de puntos de codigo Unicode (caracteres).

**Tipo:** `i32`

**Ejemplos:**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (un punto de codigo)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 emoji)
```

---

### .byte_length

Obtiene el numero de bytes UTF-8.

**Tipo:** `i32`

**Ejemplos:**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 byte por caracter ASCII)

let emoji = "🚀";
print(emoji.byte_length); // 4 (emoji es 4 bytes UTF-8)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 para emoji)
```

---

## Metodos de String

### Subcadenas y Segmentacion

#### substr

Extrae subcadena por posicion y longitud.

**Firma:**
```hemlock
string.substr(start: i32, length: i32): string
```

**Parametros:**
- `start` - Indice inicial del punto de codigo (basado en 0)
- `length` - Numero de puntos de codigo a extraer

**Retorna:** Nuevo string

**Ejemplos:**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// Ejemplo UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

Extrae subcadena por rango (fin exclusivo).

**Firma:**
```hemlock
string.slice(start: i32, end: i32): string
```

**Parametros:**
- `start` - Indice inicial del punto de codigo (basado en 0)
- `end` - Indice final del punto de codigo (exclusivo)

**Retorna:** Nuevo string

**Ejemplos:**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// Ejemplo UTF-8
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### Busqueda y Encontrar

#### find

Encuentra la primera ocurrencia de una subcadena.

**Firma:**
```hemlock
string.find(needle: string): i32
```

**Parametros:**
- `needle` - Subcadena a buscar

**Retorna:** Indice del punto de codigo de la primera ocurrencia, o `-1` si no se encuentra

**Ejemplos:**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (no encontrado)
let pos3 = s.find("l");         // 2 (primera 'l')
```

---

#### contains

Verifica si el string contiene una subcadena.

**Firma:**
```hemlock
string.contains(needle: string): bool
```

**Parametros:**
- `needle` - Subcadena a buscar

**Retorna:** `true` si se encuentra, `false` en caso contrario

**Ejemplos:**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### Dividir y Unir

#### split

Divide el string en un array por delimitador.

**Firma:**
```hemlock
string.split(delimiter: string): array
```

**Parametros:**
- `delimiter` - String por el cual dividir

**Retorna:** Array de strings

**Ejemplos:**
```hemlock
let csv = "a,b,c";
let parts = csv.split(",");     // ["a", "b", "c"]

let path = "/usr/local/bin";
let dirs = path.split("/");     // ["", "usr", "local", "bin"]

let text = "hello world foo";
let words = text.split(" ");    // ["hello", "world", "foo"]
```

---

#### trim

Elimina espacios en blanco al inicio y al final.

**Firma:**
```hemlock
string.trim(): string
```

**Retorna:** Nuevo string con espacios en blanco eliminados

**Ejemplos:**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

---

### Conversion de Mayusculas/Minusculas

#### to_upper

Convierte el string a mayusculas.

**Firma:**
```hemlock
string.to_upper(): string
```

**Retorna:** Nuevo string en mayusculas

**Ejemplos:**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

Convierte el string a minusculas.

**Firma:**
```hemlock
string.to_lower(): string
```

**Retorna:** Nuevo string en minusculas

**Ejemplos:**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### Prefijo y Sufijo

#### starts_with

Verifica si el string comienza con un prefijo.

**Firma:**
```hemlock
string.starts_with(prefix: string): bool
```

**Parametros:**
- `prefix` - Prefijo a verificar

**Retorna:** `true` si el string comienza con el prefijo, `false` en caso contrario

**Ejemplos:**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

Verifica si el string termina con un sufijo.

**Firma:**
```hemlock
string.ends_with(suffix: string): bool
```

**Parametros:**
- `suffix` - Sufijo a verificar

**Retorna:** `true` si el string termina con el sufijo, `false` en caso contrario

**Ejemplos:**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### Reemplazo

#### replace

Reemplaza la primera ocurrencia de una subcadena.

**Firma:**
```hemlock
string.replace(old: string, new: string): string
```

**Parametros:**
- `old` - Subcadena a reemplazar
- `new` - String de reemplazo

**Retorna:** Nuevo string con la primera ocurrencia reemplazada

**Ejemplos:**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (solo la primera)
```

---

#### replace_all

Reemplaza todas las ocurrencias de una subcadena.

**Firma:**
```hemlock
string.replace_all(old: string, new: string): string
```

**Parametros:**
- `old` - Subcadena a reemplazar
- `new` - String de reemplazo

**Retorna:** Nuevo string con todas las ocurrencias reemplazadas

**Ejemplos:**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### Repeticion

#### repeat

Repite el string n veces.

**Firma:**
```hemlock
string.repeat(count: i32): string
```

**Parametros:**
- `count` - Numero de repeticiones

**Retorna:** Nuevo string repetido count veces

**Ejemplos:**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### Acceso a Caracteres

#### char_at

Obtiene el punto de codigo Unicode en el indice.

**Firma:**
```hemlock
string.char_at(index: i32): rune
```

**Parametros:**
- `index` - Indice del punto de codigo (basado en 0)

**Retorna:** Rune (punto de codigo Unicode)

**Ejemplos:**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// Ejemplo UTF-8
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (cohete)
```

---

#### chars

Convierte el string a un array de runes.

**Firma:**
```hemlock
string.chars(): array
```

**Retorna:** Array de runes (puntos de codigo)

**Ejemplos:**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// Ejemplo UTF-8
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### Acceso a Bytes

#### byte_at

Obtiene el valor del byte en el indice.

**Firma:**
```hemlock
string.byte_at(index: i32): u8
```

**Parametros:**
- `index` - Indice del byte (basado en 0, NO indice de punto de codigo)

**Retorna:** Valor del byte (u8)

**Ejemplos:**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// Ejemplo UTF-8
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (primer byte UTF-8)
```

---

#### bytes

Convierte el string a un array de bytes.

**Firma:**
```hemlock
string.bytes(): array
```

**Retorna:** Array de bytes u8

**Ejemplos:**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// Ejemplo UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 bytes UTF-8)
```

---

#### to_bytes

Convierte el string a buffer.

**Firma:**
```hemlock
string.to_bytes(): buffer
```

**Retorna:** Buffer conteniendo bytes UTF-8

**Ejemplos:**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// Ejemplo UTF-8
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Nota:** Este es un metodo heredado. Prefiera `.bytes()` para la mayoria de los casos de uso.

---

### Deserializacion JSON

#### deserialize

Analiza un string JSON a un valor.

**Firma:**
```hemlock
string.deserialize(): any
```

**Retorna:** Valor analizado (objeto, array, numero, string, bool, o null)

**Ejemplos:**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**Tipos Soportados:**
- Objetos: `{"key": value}`
- Arrays: `[1, 2, 3]`
- Numeros: `42`, `3.14`
- Strings: `"text"`
- Booleanos: `true`, `false`
- Null: `null`

**Ver Tambien:** Metodo `.serialize()` de objetos

---

## Encadenamiento de Metodos

Los metodos de string pueden encadenarse para operaciones concisas:

**Ejemplos:**
```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let cleaned = "  HELLO  "
    .trim()
    .to_lower();                   // "hello"
```

---

## Resumen Completo de Metodos

| Metodo         | Firma                                        | Retorna   | Descripcion                           |
|----------------|----------------------------------------------|-----------|---------------------------------------|
| `substr`       | `(start: i32, length: i32)`                  | `string`  | Extraer subcadena por posicion/longitud |
| `slice`        | `(start: i32, end: i32)`                     | `string`  | Extraer subcadena por rango           |
| `find`         | `(needle: string)`                           | `i32`     | Encontrar primera ocurrencia (-1 si no se encuentra) |
| `contains`     | `(needle: string)`                           | `bool`    | Verificar si contiene subcadena       |
| `split`        | `(delimiter: string)`                        | `array`   | Dividir en array                      |
| `trim`         | `()`                                         | `string`  | Eliminar espacios en blanco           |
| `to_upper`     | `()`                                         | `string`  | Convertir a mayusculas                |
| `to_lower`     | `()`                                         | `string`  | Convertir a minusculas                |
| `starts_with`  | `(prefix: string)`                           | `bool`    | Verificar si comienza con prefijo     |
| `ends_with`    | `(suffix: string)`                           | `bool`    | Verificar si termina con sufijo       |
| `replace`      | `(old: string, new: string)`                 | `string`  | Reemplazar primera ocurrencia         |
| `replace_all`  | `(old: string, new: string)`                 | `string`  | Reemplazar todas las ocurrencias      |
| `repeat`       | `(count: i32)`                               | `string`  | Repetir string n veces                |
| `char_at`      | `(index: i32)`                               | `rune`    | Obtener punto de codigo en indice     |
| `byte_at`      | `(index: i32)`                               | `u8`      | Obtener byte en indice                |
| `chars`        | `()`                                         | `array`   | Convertir a array de runes            |
| `bytes`        | `()`                                         | `array`   | Convertir a array de bytes            |
| `to_bytes`     | `()`                                         | `buffer`  | Convertir a buffer (heredado)         |
| `deserialize`  | `()`                                         | `any`     | Analizar string JSON                  |

---

## Ver Tambien

- [Sistema de Tipos](type-system.md) - Detalles del tipo string
- [API de Arrays](array-api.md) - Metodos de array para resultados de split()
- [Operadores](operators.md) - Operador de concatenacion de strings
