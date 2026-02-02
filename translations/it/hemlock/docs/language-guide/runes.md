# Rune

Le rune rappresentano **codepoint Unicode** (da U+0000 a U+10FFFF) come tipo distinto per la manipolazione dei caratteri in Hemlock. A differenza dei byte (u8), le rune sono caratteri Unicode completi che possono rappresentare qualsiasi carattere in qualsiasi lingua o emoji.

## Panoramica

```hemlock
let ch = 'A';           // Letterale rune
let emoji = '🚀';       // Carattere multi-byte come singola rune
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // Concatenazione stringa + rune
let r = '>' + " msg";   // Concatenazione rune + stringa
```

## Cos'e una Rune?

Una rune e un **valore a 32 bit** che rappresenta un codepoint Unicode:

- **Range:** da 0 a 0x10FFFF (1.114.111 codepoint validi)
- **Non e un tipo numerico** - Usata per la rappresentazione dei caratteri
- **Distinta da u8/char** - Le rune sono Unicode completo, u8 sono solo byte
- **Restituita dall'indicizzazione delle stringhe** - `str[0]` restituisce una rune, non un byte

**Perche le rune?**
- Le stringhe di Hemlock sono codificate in UTF-8
- Un singolo carattere Unicode puo essere da 1 a 4 byte in UTF-8
- Le rune permettono di lavorare con caratteri completi, non byte parziali

## Letterali Rune

### Sintassi Base

Gli apici singoli denotano letterali rune:

```hemlock
let a = 'A';            // Carattere ASCII
let b = '0';            // Carattere cifra
let c = '!';            // Punteggiatura
let d = ' ';            // Spazio
```

### Caratteri UTF-8 Multi-byte

Le rune possono rappresentare qualsiasi carattere Unicode:

```hemlock
// Emoji
let rocket = '🚀';      // Emoji (U+1F680)
let heart = '❤';        // Cuore (U+2764)
let smile = '😀';       // Faccina sorridente (U+1F600)

// Caratteri CJK
let chinese = '中';     // Cinese (U+4E2D)
let japanese = 'あ';    // Hiragana (U+3042)
let korean = '한';      // Hangul (U+D55C)

// Simboli
let check = '✓';        // Segno di spunta (U+2713)
let arrow = '→';        // Freccia destra (U+2192)
```

### Sequenze di Escape

Sequenze di escape comuni per caratteri speciali:

```hemlock
let newline = '\n';     // Newline (U+000A)
let tab = '\t';         // Tab (U+0009)
let backslash = '\\';   // Backslash (U+005C)
let quote = '\'';       // Apice singolo (U+0027)
let dquote = '"';       // Doppio apice (U+0022)
let null_char = '\0';   // Carattere null (U+0000)
let cr = '\r';          // Ritorno a capo (U+000D)
```

**Sequenze di escape disponibili:**
- `\n` - Newline (line feed)
- `\t` - Tab orizzontale
- `\r` - Ritorno a capo
- `\0` - Carattere null
- `\\` - Backslash
- `\'` - Apice singolo
- `\"` - Doppio apice

### Escape Unicode

Usa la sintassi `\u{XXXXXX}` per i codepoint Unicode (fino a 6 cifre esadecimali):

```hemlock
let rocket = '\u{1F680}';   // 🚀 Emoji tramite escape Unicode
let heart = '\u{2764}';     // ❤ Cuore
let ascii = '\u{41}';       // 'A' tramite escape
let max = '\u{10FFFF}';     // Codepoint Unicode massimo

// Zeri iniziali opzionali
let a = '\u{41}';           // Uguale a '\u{0041}'
let b = '\u{0041}';
```

**Regole:**
- Range: da `\u{0}` a `\u{10FFFF}`
- Cifre esadecimali: da 1 a 6 cifre
- Case insensitive: `\u{1F680}` o `\u{1f680}`
- Valori fuori dal range Unicode valido causano errore

## Concatenazione Stringa + Rune

Le rune possono essere concatenate con le stringhe:

```hemlock
// Stringa + rune
let greeting = "Hello" + '!';       // "Hello!"
let decorated = "Testo" + '✓';      // "Testo✓"

// Rune + stringa
let prefix = '>' + " Messaggio";    // "> Messaggio"
let bullet = '•' + " Elemento";     // "• Elemento"

// Concatenazioni multiple
let msg = "Ciao " + '👋' + " Mondo " + '🌍';  // "Ciao 👋 Mondo 🌍"

// Il method chaining funziona
let result = ('>' + " Importante").to_upper();  // "> IMPORTANTE"
```

**Come funziona:**
- Le rune vengono automaticamente codificate in UTF-8
- Convertite in stringhe durante la concatenazione
- L'operatore di concatenazione delle stringhe gestisce questo in modo trasparente

## Conversioni di Tipo

Le rune possono essere convertite da/verso altri tipi.

### Intero <-> Rune

Converti tra interi e rune per lavorare con i valori dei codepoint:

```hemlock
// Intero a rune (valore del codepoint)
let code: rune = 65;            // 'A' (ASCII 65)
let emoji_code: rune = 128640;  // U+1F680 (🚀)

// Rune a intero (ottieni il valore del codepoint)
let r = 'Z';
let value: i32 = r;             // 90 (valore ASCII)

let rocket = '🚀';
let code: i32 = rocket;         // 128640 (U+1F680)
```

**Controllo del range:**
- Intero a rune: Deve essere in [0, 0x10FFFF]
- Valori fuori range causano errore a runtime
- Rune a intero: Sempre successo (restituisce il codepoint)

### Rune -> Stringa

Le rune possono essere convertite esplicitamente in stringhe:

```hemlock
// Conversione esplicita
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// Automatica durante la concatenazione
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8 (Byte) -> Rune

Qualsiasi valore u8 (0-255) puo essere convertito in rune:

```hemlock
// Range ASCII (0-127)
let byte: u8 = 65;
let rune_val: rune = byte;      // 'A'

// ASCII esteso / Latin-1 (128-255)
let extended: u8 = 200;
let r: rune = extended;         // U+00C8 (È)

// Nota: I valori 0-127 sono ASCII, 128-255 sono Latin-1
```

### Conversioni Concatenate

Le conversioni di tipo possono essere concatenate:

```hemlock
// i32 -> rune -> stringa
let code: i32 = 128512;         // Codepoint faccina sorridente
let r: rune = code;             // 😀
let s: string = r;              // "😀"

// Tutto in un'unica espressione
let emoji: string = 128640;     // i32 -> rune -> stringa implicito (🚀)
```

## Operazioni sulle Rune

### Stampa

Come vengono visualizzate le rune dipende dal codepoint:

```hemlock
let ascii = 'A';
print(ascii);                   // 'A' (quotato, ASCII stampabile)

let emoji = '🚀';
print(emoji);                   // U+1F680 (notazione Unicode per non-ASCII)

let tab = '\t';
print(tab);                     // U+0009 (non stampabile come hex)

let space = ' ';
print(space);                   // ' ' (stampabile)
```

**Formato di stampa:**
- ASCII stampabile (32-126): Carattere quotato `'A'`
- Non stampabile o Unicode: Notazione hex `U+XXXX`

### Controllo del Tipo

Usa `typeof()` per controllare se un valore e una rune:

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "testo";
let ch = s[0];
print(typeof(ch));              // "rune" (l'indicizzazione restituisce rune)

let num = 65;
print(typeof(num));             // "i32"
```

### Confronto

Le rune possono essere confrontate per uguaglianza:

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// Case sensitive
let upper = 'A';
let lower = 'a';
print(upper == lower);          // false

// Le rune possono essere confrontate con interi (valori dei codepoint)
print(a == 65);                 // true (conversione implicita)
print('🚀' == 128640);          // true
```

**Operatori di confronto:**
- `==` - Uguale
- `!=` - Diverso
- `<`, `>`, `<=`, `>=` - Ordine dei codepoint

```hemlock
print('A' < 'B');               // true (65 < 66)
print('a' > 'Z');               // true (97 > 90)
```

## Lavorare con l'Indicizzazione delle Stringhe

L'indicizzazione delle stringhe restituisce rune, non byte:

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H' (rune)
let rocket = s[5];              // '🚀' (rune)

print(typeof(h));               // "rune"
print(typeof(rocket));          // "rune"

// Converti in stringa se necessario
let h_str: string = h;          // "H"
let rocket_str: string = rocket; // "🚀"
```

**Importante:** L'indicizzazione delle stringhe usa posizioni dei codepoint, non offset dei byte:

```hemlock
let text = "Ciao🚀!";
// Posizioni codepoint: 0='C', 1='i', 2='a', 3='o', 4='🚀', 5='!'
// Posizioni byte:      0='C', 1='i', 2='a', 3='o', 4-7='🚀', 8='!'

let r = text[4];                // '🚀' (codepoint 4)
print(typeof(r));               // "rune"
```

## Esempi

### Esempio: Classificazione dei Caratteri

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

### Esempio: Conversione di Caso

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // Converti in maiuscolo (sottrai 32)
        let code: i32 = r;
        code = code - 32;
        return code;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // Converti in minuscolo (aggiungi 32)
        let code: i32 = r;
        code = code + 32;
        return code;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### Esempio: Iterazione sui Caratteri

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Posizione " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Ciao🚀");
// Posizione 0: 'C'
// Posizione 1: 'i'
// Posizione 2: 'a'
// Posizione 3: 'o'
// Posizione 4: U+1F680
```

### Esempio: Costruire Stringhe dalle Rune

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
let stars = repeat_char('⭐', 5); // "⭐⭐⭐⭐⭐"
```

## Pattern Comuni

### Pattern: Filtro di Caratteri

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

### Pattern: Conteggio Caratteri

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

## Best Practice

1. **Usa le rune per le operazioni sui caratteri** - Non provare a lavorare con i byte per il testo
2. **L'indicizzazione delle stringhe restituisce rune** - Ricorda che `str[i]` ti da una rune
3. **Confronti consapevoli di Unicode** - Le rune gestiscono qualsiasi carattere Unicode
4. **Converti quando necessario** - Le rune si convertono facilmente in stringhe e interi
5. **Testa con emoji** - Testa sempre le operazioni sui caratteri con caratteri multi-byte

## Insidie Comuni

### Insidia: Confusione Rune vs. Byte

```hemlock
// NON FARE: Trattare le rune come byte
let r: rune = '🚀';
let b: u8 = r;              // ERRORE: Il codepoint rune 128640 non entra in u8

// FARE: Usa conversioni appropriate
let r: rune = '🚀';
let code: i32 = r;          // OK: 128640
```

### Insidia: Indicizzazione per Byte delle Stringhe

```hemlock
// NON FARE: Assumere l'indicizzazione per byte
let s = "🚀";
let byte = s.byte_at(0);    // 240 (primo byte UTF-8, non il carattere completo)

// FARE: Usa l'indicizzazione per codepoint
let s = "🚀";
let rune = s[0];            // '🚀' (carattere completo)
let rune2 = s.char_at(0);   // '🚀' (metodo esplicito)
```

## Argomenti Correlati

- [Stringhe](strings.md) - Operazioni sulle stringhe e gestione UTF-8
- [Tipi](types.md) - Sistema di tipi e conversioni
- [Flusso di Controllo](control-flow.md) - Usare le rune nei confronti

## Vedi Anche

- **Standard Unicode**: I codepoint Unicode sono definiti dall'Unicode Consortium
- **Codifica UTF-8**: Vedi [Stringhe](strings.md) per i dettagli su UTF-8
- **Conversioni di Tipo**: Vedi [Tipi](types.md) per le regole di conversione
