# Cadenas

Las cadenas de Hemlock son **secuencias mutables de primera clase codificadas en UTF-8** con soporte completo de Unicode y un amplio conjunto de metodos para procesamiento de texto. A diferencia de muchos lenguajes, las cadenas de Hemlock son mutables y trabajan nativamente con puntos de codigo Unicode.

## Resumen

```hemlock
let s = "hello";
s[0] = 'H';             // mutar con rune (ahora "Hello")
print(s.length);        // 5 (conteo de puntos de codigo)
let c = s[0];           // retorna rune (punto de codigo Unicode)
let msg = s + " world"; // concatenacion
let emoji = "rocket";
print(emoji.length);    // 1 (un punto de codigo)
print(emoji.byte_length); // 4 (cuatro bytes UTF-8)
```

## Propiedades

Las cadenas de Hemlock tienen estas caracteristicas clave:

- **Codificadas en UTF-8** - Soporte completo de Unicode (U+0000 a U+10FFFF)
- **Mutables** - A diferencia de cadenas en Python, JavaScript y Java
- **Indexacion basada en puntos de codigo** - Retorna `rune` (punto de codigo Unicode), no byte
- **Asignadas en heap** - Con seguimiento de capacidad interna
- **Dos propiedades de longitud**:
  - `.length` - Conteo de puntos de codigo (numero de caracteres)
  - `.byte_length` - Conteo de bytes (tamano de codificacion UTF-8)

## Comportamiento UTF-8

Todas las operaciones de cadena trabajan con **puntos de codigo** (caracteres), no bytes:

```hemlock
let text = "Helloroute";
print(text.length);        // 11 (puntos de codigo)
print(text.byte_length);   // 15 (bytes, el emoji son 4 bytes)

// La indexacion usa puntos de codigo
let h = text[0];           // 'H' (rune)
let rocket = text[5];      // 'rocket' (rune)
```

**Los caracteres multi-byte cuentan como uno:**
```hemlock
"Hello".length;      // 5
"rocket".length;     // 1 (un emoji)
"nihao".length;      // 2 (dos caracteres chinos)
"cafe".length;       // 4 (e con acento es un punto de codigo)
```

## Literales de Cadena

```hemlock
// Cadenas basicas
let s1 = "hello";
let s2 = "world";

// Con secuencias de escape
let s3 = "Line 1\nLine 2\ttabbed";
let s4 = "Quote: \"Hello\"";
let s5 = "Backslash: \\";

// Caracteres Unicode
let s6 = "rocket Emoji";
let s7 = "zhongwenzifu";
```

## Cadenas de Plantilla (Interpolacion de Cadenas)

Usa comillas invertidas para cadenas de plantilla con expresiones embebidas:

```hemlock
let name = "Alice";
let age = 30;

// Interpolacion basica
let greeting = `Hello, ${name}!`;           // "Hello, Alice!"
let info = `${name} is ${age} years old`;   // "Alice is 30 years old"

// Expresiones en interpolacion
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// Llamadas a metodos
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// Objetos anidados
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lives in ${person.city}`;  // "Bob lives in NYC"

// Multi-linea (preserva saltos de linea)
let multi = `Line 1
Line 2
Line 3`;
```

**Caracteristicas de cadenas de plantilla:**
- Las expresiones dentro de `${...}` se evaluan y convierten a cadenas
- Se puede usar cualquier expresion valida (variables, llamadas a funciones, aritmetica)
- Las cadenas con comillas invertidas soportan las mismas secuencias de escape que las cadenas regulares
- Util para construir cadenas dinamicas sin concatenacion

### Escape en Cadenas de Plantilla

Para incluir un `${` literal en una cadena de plantilla, escapa el signo de dolar:

```hemlock
let price = 100;
let text = `Price: \${price} or ${price}`;
// "Price: ${price} or 100"

// Comilla invertida literal
let code = `Use \` for template strings`;
// "Use ` for template strings"
```

### Expresiones Complejas

Las cadenas de plantilla pueden contener cualquier expresion valida:

```hemlock
// Expresiones tipo ternario
let age = 25;
let status = `Status: ${age >= 18 ? "adult" : "minor"}`;

// Acceso a array
let items = ["apple", "banana", "cherry"];
let first = `First item: ${items[0]}`;

// Llamadas a funciones con argumentos
fn format_price(p) { return "$" + p; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: $99.99"

// Llamadas a metodos encadenados
let name = "alice";
let formatted = `Hello, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hello, Alice!"
```

### Cadenas de Plantilla vs Concatenacion

Las cadenas de plantilla son frecuentemente mas limpias que la concatenacion:

```hemlock
// Concatenacion (mas dificil de leer)
let msg1 = "Hello, " + name + "! You have " + count + " messages.";

// Cadena de plantilla (mas facil de leer)
let msg2 = `Hello, ${name}! You have ${count} messages.`;
```

## Indexacion y Mutacion

### Lectura de Caracteres

La indexacion retorna un `rune` (punto de codigo Unicode):

```hemlock
let s = "Hello";
let first = s[0];      // 'H' (rune)
let last = s[4];       // 'o' (rune)

// Ejemplo UTF-8
let emoji = "Hirocket!";
let rocket = emoji[2];  // 'rocket' (rune en indice de punto de codigo 2)
```

### Escritura de Caracteres

Las cadenas son mutables - puedes modificar caracteres individuales:

```hemlock
let s = "hello";
s[0] = 'H';            // Ahora "Hello"
s[4] = '!';            // Ahora "Hell!"

// Con Unicode
let msg = "Go!";
msg[0] = 'rocket';     // Ahora "rocketo!"
```

## Concatenacion

Usa `+` para concatenar cadenas:

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// Con variables
let name = "Alice";
let msg = "Hi, " + name + "!";  // "Hi, Alice!"

// Con runes (ver documentacion de Runes)
let s = "Hello" + '!';          // "Hello!"
```

## Metodos de Cadena

Hemlock proporciona 19 metodos de cadena para manipulacion completa de texto.

### Subcadena y Extraccion

**`substr(start, length)`** - Extraer subcadena por posicion y longitud:
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world" (inicia en 6, longitud 5)
let first = s.substr(0, 5);     // "hello"

// Ejemplo UTF-8
let text = "Hirocket!";
let emoji = text.substr(2, 1);  // "rocket" (posicion 2, longitud 1)
```

**`slice(start, end)`** - Extraer subcadena por rango (end exclusivo):
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello" (indice 0 a 4)
let slice2 = s.slice(6, 11);    // "world"
```

**Diferencia:**
- `substr(start, length)` - Usa parametro de longitud
- `slice(start, end)` - Usa indice final (exclusivo)

### Busqueda y Encontrar

**`find(needle)`** - Encontrar primera ocurrencia:
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6 (indice de primera ocurrencia)
let pos2 = s.find("foo");       // -1 (no encontrado)
let pos3 = s.find("l");         // 2 (primera 'l')
```

**`contains(needle)`** - Verificar si la cadena contiene subcadena:
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### Division y Recorte

**`split(delimiter)`** - Dividir en array de cadenas:
```hemlock
let csv = "apple,banana,cherry";
let parts = csv.split(",");     // ["apple", "banana", "cherry"]

let words = "one two three".split(" ");  // ["one", "two", "three"]

// Delimitador vacio divide por caracter
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Remover espacios al inicio/final:
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### Conversion de Mayusculas/Minusculas

**`to_upper()`** - Convertir a mayusculas:
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// Preserva no-ASCII
let s2 = "cafe";
let upper2 = s2.to_upper();     // "CAFE"
```

**`to_lower()`** - Convertir a minusculas:
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### Verificacion de Prefijo/Sufijo

**`starts_with(prefix)`** - Verificar si inicia con prefijo:
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - Verificar si termina con sufijo:
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### Reemplazo

**`replace(old, new)`** - Reemplazar primera ocurrencia:
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (solo primera)
```

**`replace_all(old, new)`** - Reemplazar todas las ocurrencias:
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### Repeticion

**`repeat(count)`** - Repetir cadena n veces:
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### Acceso a Caracteres y Bytes

**`char_at(index)`** - Obtener punto de codigo Unicode en indice (retorna rune):
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h' (rune)

// Ejemplo UTF-8
let emoji = "rocket";
let rocket = emoji.char_at(0);  // Retorna rune U+1F680
```

**`chars()`** - Convertir a array de runes (puntos de codigo):
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o'] (array de runes)

// Ejemplo UTF-8
let text = "Hirocket";
let chars2 = text.chars();      // ['H', 'i', 'rocket']
```

**`byte_at(index)`** - Obtener valor de byte en indice (retorna u8):
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (valor ASCII de 'h')

// Ejemplo UTF-8
let emoji = "rocket";
let first_byte = emoji.byte_at(0);  // 240 (primer byte UTF-8)
```

**`bytes()`** - Convertir a array de bytes (valores u8):
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111] (array de u8)

// Ejemplo UTF-8
let emoji = "rocket";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 bytes UTF-8)
```

**`to_bytes()`** - Convertir a buffer para acceso de bajo nivel:
```hemlock
let s = "hello";
let buf = s.to_bytes();         // Retorna buffer con bytes UTF-8
print(buf.length);              // 5
free(buf);                      // Recuerda liberar
```

## Encadenamiento de Metodos

Todos los metodos de cadena retornan nuevas cadenas, permitiendo encadenamiento:

```hemlock
let result = "  Hello World  "
    .trim()
    .to_lower()
    .replace("world", "hemlock");  // "hello hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## Referencia Completa de Metodos

| Metodo | Parametros | Retorna | Descripcion |
|--------|-----------|---------|-------------|
| `substr(start, length)` | i32, i32 | string | Extraer subcadena por posicion y longitud |
| `slice(start, end)` | i32, i32 | string | Extraer subcadena por rango (end exclusivo) |
| `find(needle)` | string | i32 | Encontrar primera ocurrencia (-1 si no encontrado) |
| `contains(needle)` | string | bool | Verificar si contiene subcadena |
| `split(delimiter)` | string | array | Dividir en array de cadenas |
| `trim()` | - | string | Remover espacios al inicio/final |
| `to_upper()` | - | string | Convertir a mayusculas |
| `to_lower()` | - | string | Convertir a minusculas |
| `starts_with(prefix)` | string | bool | Verificar si inicia con prefijo |
| `ends_with(suffix)` | string | bool | Verificar si termina con sufijo |
| `replace(old, new)` | string, string | string | Reemplazar primera ocurrencia |
| `replace_all(old, new)` | string, string | string | Reemplazar todas las ocurrencias |
| `repeat(count)` | i32 | string | Repetir cadena n veces |
| `char_at(index)` | i32 | rune | Obtener punto de codigo en indice |
| `byte_at(index)` | i32 | u8 | Obtener valor de byte en indice |
| `chars()` | - | array | Convertir a array de runes |
| `bytes()` | - | array | Convertir a array de bytes u8 |
| `to_bytes()` | - | buffer | Convertir a buffer (debe liberarse) |

## Ejemplos

### Ejemplo: Procesamiento de Texto

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Normalizar espacios
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### Ejemplo: Analizador CSV

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "apple, banana , cherry";
let fields = parse_csv_line(csv);  // ["apple", "banana", "cherry"]
```

### Ejemplo: Contador de Palabras

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "The quick brown fox";
let count = count_words(sentence);  // 4
```

### Ejemplo: Validacion de Cadenas

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## Gestion de Memoria

Las cadenas se asignan en heap con conteo de referencias interno:

- **Creacion**: Asignadas en heap con seguimiento de capacidad
- **Concatenacion**: Crea nueva cadena (cadenas originales sin cambios)
- **Metodos**: La mayoria de metodos retornan nuevas cadenas
- **Tiempo de vida**: Las cadenas tienen conteo de referencias y se liberan automaticamente cuando el alcance termina

**Limpieza automatica:**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // Nueva asignacion
}  // Tanto s como s2 se liberan automaticamente cuando la funcion retorna
```

**Nota:** Las variables de cadena locales se limpian automaticamente cuando salen del alcance. Usa `free()` solo para limpieza anticipada antes de que termine el alcance o para datos de larga vida/globales. Ver [Gestion de Memoria](memory.md#conteo-de-referencias-interno) para detalles.

## Mejores Practicas

1. **Usar indexacion de puntos de codigo** - Las cadenas usan posiciones de puntos de codigo, no desplazamientos de bytes
2. **Probar con Unicode** - Siempre probar operaciones de cadena con caracteres multi-byte
3. **Preferir operaciones inmutables** - Usar metodos que retornan nuevas cadenas en vez de mutacion
4. **Verificar limites** - La indexacion de cadenas no verifica limites (retorna null/error en invalido)
5. **Normalizar entrada** - Usar `trim()` y `to_lower()` para entrada de usuario

## Errores Comunes

### Error: Confusion Byte vs. Punto de Codigo

```hemlock
let emoji = "rocket";
print(emoji.length);        // 1 (punto de codigo)
print(emoji.byte_length);   // 4 (bytes)

// No mezclar operaciones de byte y punto de codigo
let byte = emoji.byte_at(0);  // 240 (primer byte, no caracter completo)
let char = emoji.char_at(0);  // 'rocket' (punto de codigo completo)
```

### Error: Sorpresas de Mutacion

```hemlock
let s1 = "hello";
let s2 = s1;       // Copia superficial
s1[0] = 'H';       // Muta s1
print(s2);         // Sigue siendo "hello" (las cadenas son tipos de valor)
```

## Temas Relacionados

- [Runes](runes.md) - Tipo de punto de codigo Unicode usado en indexacion de cadenas
- [Arrays](arrays.md) - Los metodos de cadena frecuentemente retornan o trabajan con arrays
- [Types](types.md) - Detalles del tipo string y conversiones

## Ver Tambien

- **Codificacion UTF-8**: Ver seccion "Strings" en CLAUDE.md
- **Conversiones de Tipo**: Ver [Types](types.md) para conversiones de cadenas
- **Memoria**: Ver [Memory](memory.md) para detalles de asignacion de cadenas
