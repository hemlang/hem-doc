# Runes

Los runes representan **puntos de código Unicode** (U+0000 a U+10FFFF) como un tipo distinto para manipulación de caracteres en Hemlock. A diferencia de los bytes (u8), los runes son caracteres Unicode completos que pueden representar cualquier caracter en cualquier idioma o emoji.

## Resumen

```hemlock
let ch = 'A';           // Literal rune
let emoji = '🚀';       // Caracter multi-byte como rune único
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // Concatenación string + rune
let r = '>' + " msg";   // Concatenación rune + string
```

## Qué es un Rune?

Un rune es un **valor de 32 bits** que representa un punto de código Unicode:

- **Rango:** 0 a 0x10FFFF (1,114,111 puntos de código válidos)
- **No es un tipo numérico** - Usado para representación de caracteres
- **Distinto de u8/char** - Los runes son Unicode completo, u8 es solo bytes
- **Retornado por indexación de strings** - `str[0]` retorna un rune, no un byte

**Por qué runes?**
- Los strings de Hemlock están codificados en UTF-8
- Un solo caracter Unicode puede ser 1-4 bytes en UTF-8
- Los runes permiten trabajar con caracteres completos, no bytes parciales

## Literales Rune

### Sintaxis Básica

Las comillas simples denotan literales rune:

```hemlock
let a = 'A';            // Caracter ASCII
let b = '0';            // Caracter dígito
let c = '!';            // Puntuación
let d = ' ';            // Espacio
```

### Caracteres UTF-8 Multi-byte

Los runes pueden representar cualquier caracter Unicode:

```hemlock
// Emoji
let rocket = '🚀';      // Emoji (U+1F680)
let heart = '❤';        // Corazón (U+2764)
let smile = '😀';       // Cara sonriente (U+1F600)

// Caracteres CJK
let chinese = '中';     // Chino (U+4E2D)
let japanese = 'あ';    // Hiragana (U+3042)
let korean = '한';      // Hangul (U+D55C)

// Símbolos
let check = '✓';        // Marca de verificación (U+2713)
let arrow = '→';        // Flecha derecha (U+2192)
```

### Secuencias de Escape

Secuencias de escape comunes para caracteres especiales:

```hemlock
let newline = '\n';     // Nueva línea (U+000A)
let tab = '\t';         // Tabulación (U+0009)
let backslash = '\\';   // Barra invertida (U+005C)
let quote = '\'';       // Comilla simple (U+0027)
let dquote = '"';       // Comilla doble (U+0022)
let null_char = '\0';   // Caracter nulo (U+0000)
let cr = '\r';          // Retorno de carro (U+000D)
```

**Secuencias de escape disponibles:**
- `\n` - Nueva línea (line feed)
- `\t` - Tabulación horizontal
- `\r` - Retorno de carro
- `\0` - Caracter nulo
- `\\` - Barra invertida
- `\'` - Comilla simple
- `\"` - Comilla doble

### Escapes Unicode

Use la sintaxis `\u{XXXXXX}` para puntos de código Unicode (hasta 6 dígitos hexadecimales):

```hemlock
let rocket = '\u{1F680}';   // 🚀 Emoji vía escape Unicode
let heart = '\u{2764}';     // ❤ Corazón
let ascii = '\u{41}';       // 'A' vía escape
let max = '\u{10FFFF}';     // Punto de código Unicode máximo

// Ceros iniciales opcionales
let a = '\u{41}';           // Igual que '\u{0041}'
let b = '\u{0041}';
```

**Reglas:**
- Rango: `\u{0}` a `\u{10FFFF}`
- Dígitos hexadecimales: 1 a 6 dígitos
- Insensible a mayúsculas: `\u{1F680}` o `\u{1f680}`
- Valores fuera del rango Unicode válido causan error

## Concatenación String + Rune

Los runes pueden concatenarse con strings:

```hemlock
// String + rune
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Text" + '✓';       // "Text✓"

// Rune + string
let prefix = '>' + " Message";      // "> Message"
let bullet = '•' + " Item";         // "• Item"

// Múltiples concatenaciones
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"

// El encadenamiento de métodos funciona
let result = ('>' + " Important").to_upper();  // "> IMPORTANT"
```

**Cómo funciona:**
- Los runes se codifican automáticamente a UTF-8
- Se convierten a strings durante la concatenación
- El operador de concatenación de strings maneja esto transparentemente

## Conversiones de Tipo

Los runes pueden convertirse hacia/desde otros tipos.

### Entero ↔ Rune

Convertir entre enteros y runes para trabajar con valores de puntos de código:

```hemlock
// Entero a rune (valor de punto de código)
let code: rune = 65;            // 'A' (ASCII 65)
let emoji_code: rune = 128640;  // U+1F680 (🚀)

// Rune a entero (obtener valor de punto de código)
let r = 'Z';
let value: i32 = r;             // 90 (valor ASCII)

let rocket = '🚀';
let code: i32 = rocket;         // 128640 (U+1F680)
```

**Verificación de rango:**
- Entero a rune: Debe estar en [0, 0x10FFFF]
- Valores fuera de rango causan error en tiempo de ejecución
- Rune a entero: Siempre tiene éxito (retorna punto de código)

### Rune → String

Los runes pueden convertirse explícitamente a strings:

```hemlock
// Conversión explícita
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// Automático durante concatenación
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8 (Byte) → Rune

Cualquier valor u8 (0-255) puede convertirse a rune:

```hemlock
// Rango ASCII (0-127)
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// ASCII extendido / Latin-1 (128-255)
let extended: u8 = 200;
let r: rune = extended;         // U+00C8 (È)

// Nota: Valores 0-127 son ASCII, 128-255 son Latin-1
```

### Conversiones Encadenadas

Las conversiones de tipo pueden encadenarse:

```hemlock
// i32 → rune → string
let code: i32 = 128512;         // Punto de código de cara sonriente
let r: rune = code;             // 😀
let s: string = r;              // "😀"

// Todo en una expresión
let emoji: string = 128640;     // Implícito i32 → rune → string (🚀)
```

## Operaciones con Runes

### Impresión

Cómo se muestran los runes depende del punto de código:

```hemlock
let ascii = 'A';
print(ascii);                   // 'A' (entre comillas, ASCII imprimible)

let emoji = '🚀';
print(emoji);                   // U+1F680 (notación Unicode para no-ASCII)

let tab = '\t';
print(tab);                     // U+0009 (no imprimible como hex)

let space = ' ';
print(space);                   // ' ' (imprimible)
```

**Formato de impresión:**
- ASCII imprimible (32-126): Caracter entre comillas `'A'`
- No imprimible o Unicode: Notación hexadecimal `U+XXXX`

### Verificación de Tipo

Use `typeof()` para verificar si un valor es un rune:

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "text";
let ch = s[0];
print(typeof(ch));              // "rune" (la indexación retorna runes)

let num = 65;
print(typeof(num));             // "i32"
```

### Comparación

Los runes pueden compararse por igualdad:

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// Sensible a mayúsculas
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// Los runes pueden compararse con enteros (valores de punto de código)
print(a == 65);                 // true (conversión implícita)
print('🚀' == 128640);          // true
```

**Operadores de comparación:**
- `==` - Igual
- `!=` - No igual
- `<`, `>`, `<=`, `>=` - Orden de punto de código

```hemlock
print('A' < 'B');               // true (65 < 66)
print('a' > 'Z');               // true (97 > 90)
```

## Trabajando con Indexación de Strings

La indexación de strings retorna runes, no bytes:

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H' (rune)
let rocket = s[5];              // '🚀' (rune)

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// Convertir a string si es necesario
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "🚀"
```

**Importante:** La indexación de strings usa posiciones de punto de código, no offsets de bytes:

```hemlock
let text = "Hi🚀!";
// Posiciones de punto de código: 0='H', 1='i', 2='🚀', 3='!'
// Posiciones de byte:            0='H', 1='i', 2-5='🚀', 6='!'

let r = text[2];                // '🚀' (punto de código 2)
print(typeof(r));               // "rune"
```

## Ejemplos

### Ejemplo: Clasificación de Caracteres

```hemlock
fn is_digit(r: rune): bool {
    return r >= '0' && r <= '9';
}

fn is_upper(r: rune): bool {
    return r >= 'A' && r <= 'Z';
}

fn is_lower(r: rune): bool {
    return r >= 'a' && r <= 'z';
}

print(is_digit('5'));           // true
print(is_upper('A'));           // true
print(is_lower('z'));           // true
```

### Ejemplo: Conversión de Mayúsculas/Minúsculas

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // Convertir a mayúscula (restar 32)
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // Convertir a minúscula (sumar 32)
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### Ejemplo: Iteración de Caracteres

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Position " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Hi🚀");
// Position 0: 'H'
// Position 1: 'i'
// Position 2: U+1F680
```

### Ejemplo: Construyendo Strings desde Runes

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let result = "";
    let i = 0;
    while (i < count) {
        result = result + ch;
        i = i + 1;
    }
    return result;
}

let line = repeat_char('=', 40);  // "========================================"
let stars = repeat_char('⭐', 5);  // "⭐⭐⭐⭐⭐"
```

## Patrones Comunes

### Patrón: Filtro de Caracteres

```hemlock
fn filter_digits(s: string): string {
    let result = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            result = result + ch;
        }
        i = i + 1;
    }
    return result;
}

let text = "abc123def456";
let digits = filter_digits(text);  // "123456"
```

### Patrón: Conteo de Caracteres

```hemlock
fn count_char(s: string, target: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == target) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let text = "hello world";
let l_count = count_char(text, 'l');  // 3
let o_count = count_char(text, 'o');  // 2
```

## Mejores Prácticas

1. **Use runes para operaciones de caracteres** - No intente trabajar con bytes para texto
2. **La indexación de strings retorna runes** - Recuerde que `str[i]` le da un rune
3. **Comparaciones conscientes de Unicode** - Los runes manejan cualquier caracter Unicode
4. **Convierta cuando sea necesario** - Los runes se convierten fácilmente a strings y enteros
5. **Pruebe con emoji** - Siempre pruebe operaciones de caracteres con caracteres multi-byte

## Errores Comunes

### Error: Confusión entre Rune y Byte

```hemlock
// NO: Tratar runes como bytes
let r: rune = '🚀';
let b: u8 = r;              // ERROR: El punto de código 128640 no cabe en u8

// SÍ: Usar conversiones apropiadas
let r: rune = '🚀';
let code: i32 = r;          // OK: 128640
```

### Error: Indexación de Bytes de String

```hemlock
// NO: Asumir indexación de bytes
let s = "🚀";
let byte = s.byte_at(0);    // 240 (primer byte UTF-8, no caracter completo)

// SÍ: Usar indexación de punto de código
let s = "🚀";
let rune = s[0];            // '🚀' (caracter completo)
let rune2 = s.char_at(0);   // '🚀' (método explícito)
```

## Temas Relacionados

- [Strings](strings.md) - Operaciones de strings y manejo UTF-8
- [Tipos](types.md) - Sistema de tipos y conversiones
- [Flujo de Control](control-flow.md) - Usando runes en comparaciones

## Ver También

- **Estándar Unicode**: Los puntos de código Unicode son definidos por el Consorcio Unicode
- **Codificación UTF-8**: Consulte [Strings](strings.md) para detalles de UTF-8
- **Conversiones de Tipo**: Consulte [Tipos](types.md) para reglas de conversión
