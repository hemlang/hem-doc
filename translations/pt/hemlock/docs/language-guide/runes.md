# Caracteres Rune

Rune representa **pontos de codigo Unicode** (U+0000 a U+10FFFF), como um tipo distinto para operacoes de caracteres em Hemlock. Diferente de bytes (u8), runes sao caracteres Unicode completos que podem representar caracteres de qualquer idioma ou emojis.

## Visao Geral

```hemlock
let ch = 'A';           // Literal rune
let emoji = '🚀';       // Caractere multi-byte como um unico rune
print(ch);              // 'A'
print(emoji);           // U+1F680

let s = "Hello " + '!'; // Concatenacao string + rune
let r = '>' + " msg";   // Concatenacao rune + string
```

## O que e um Rune?

Rune e um **valor de 32 bits** que representa um ponto de codigo Unicode:

- **Intervalo:** 0 a 0x10FFFF (1.114.111 pontos de codigo validos)
- **Nao e um tipo numerico** - Usado para representacao de caracteres
- **Diferente de u8/char** - Rune e Unicode completo, u8 e apenas um byte
- **Indexacao de string retorna** - `str[0]` retorna rune, nao byte

**Por que usar rune?**
- Strings Hemlock sao codificadas em UTF-8
- Um unico caractere Unicode pode ter 1-4 bytes em UTF-8
- Rune permite trabalhar com caracteres completos, nao bytes parciais

## Literais Rune

### Sintaxe Basica

Aspas simples denotam literais rune:

```hemlock
let a = 'A';            // Caractere ASCII
let b = '0';            // Caractere digito
let c = '!';            // Pontuacao
let d = ' ';            // Espaco
```

### Caracteres UTF-8 Multi-byte

Rune pode representar qualquer caractere Unicode:

```hemlock
// Emojis
let foguete = '🚀';     // Emoji (U+1F680)
let coracao = '❤';      // Coracao (U+2764)
let sorriso = '😀';     // Rosto sorridente (U+1F600)

// Caracteres CJK
let chines = '中';      // Chines (U+4E2D)
let japones = 'あ';     // Hiragana (U+3042)
let coreano = '한';     // Hangul (U+D55C)

// Simbolos
let check = '✓';        // Marca de verificacao (U+2713)
let seta = '→';         // Seta direita (U+2192)
```

### Sequencias de Escape

Sequencias de escape comuns para caracteres especiais:

```hemlock
let newline = '\n';     // Quebra de linha (U+000A)
let tab = '\t';         // Tabulacao (U+0009)
let backslash = '\\';   // Barra invertida (U+005C)
let quote = '\'';       // Aspas simples (U+0027)
let dquote = '"';       // Aspas duplas (U+0022)
let null_char = '\0';   // Caractere nulo (U+0000)
let cr = '\r';          // Retorno de carro (U+000D)
```

**Sequencias de escape disponiveis:**
- `\n` - Quebra de linha
- `\t` - Tabulacao horizontal
- `\r` - Retorno de carro
- `\0` - Caractere nulo
- `\\` - Barra invertida
- `\'` - Aspas simples
- `\"` - Aspas duplas

### Escapes Unicode

Use sintaxe `\u{XXXXXX}` para pontos de codigo Unicode (ate 6 digitos hexadecimais):

```hemlock
let foguete = '\u{1F680}';   // 🚀 emoji via escape Unicode
let coracao = '\u{2764}';    // ❤ coracao
let ascii = '\u{41}';        // 'A' via escape
let max = '\u{10FFFF}';      // Ponto de codigo Unicode maximo

// Zeros a esquerda sao opcionais
let a = '\u{41}';            // Mesmo que '\u{0041}'
let b = '\u{0041}';
```

**Regras:**
- Intervalo: `\u{0}` a `\u{10FFFF}`
- Digitos hexadecimais: 1 a 6 digitos
- Case-insensitive: `\u{1F680}` ou `\u{1f680}`
- Valores fora do intervalo Unicode valido causam erro

## Concatenacao String + Rune

Runes podem ser concatenados com strings:

```hemlock
// String + rune
let saudacao = "Ola" + '!';         // "Ola!"
let decorado = "Texto" + '✓';       // "Texto✓"

// Rune + string
let prefixo = '>' + " Mensagem";    // "> Mensagem"
let marcador = '•' + " Item";       // "• Item"

// Concatenacao multipla
let msg = "Oi " + '👋' + " Mundo " + '🌍';  // "Oi 👋 Mundo 🌍"

// Encadeamento de metodos funciona
let resultado = ('>' + " Importante").to_upper();  // "> IMPORTANTE"
```

**Como funciona:**
- Rune e automaticamente codificado em UTF-8
- Convertido para string durante concatenacao
- Operador de concatenacao de string trata isso transparentemente

## Conversao de Tipos

Runes podem ser convertidos de/para outros tipos.

### Inteiro <-> Rune

Converte entre inteiros e runes para trabalhar com valores de pontos de codigo:

```hemlock
// Inteiro para rune (valor do ponto de codigo)
let codigo: rune = 65;            // 'A' (ASCII 65)
let emoji_code: rune = 128640;    // U+1F680 (🚀)

// Rune para inteiro (obter valor do ponto de codigo)
let r = 'Z';
let valor: i32 = r;               // 90 (valor ASCII)

let foguete = '🚀';
let codigo: i32 = foguete;        // 128640 (U+1F680)
```

**Verificacao de intervalo:**
- Inteiro para rune: deve estar no intervalo [0, 0x10FFFF]
- Valores fora do intervalo causam erro de runtime
- Rune para inteiro: sempre sucede (retorna ponto de codigo)

### Rune -> String

Runes podem ser explicitamente convertidos para strings:

```hemlock
// Conversao explicita
let ch: string = 'H';           // "H"
let emoji: string = '🚀';       // "🚀"

// Conversao automatica em concatenacao
let s = "" + 'A';               // "A"
let s2 = "x" + 'y' + "z";       // "xyz"
```

### u8 (Byte) -> Rune

Qualquer valor u8 (0-255) pode ser convertido para rune:

```hemlock
// Intervalo ASCII (0-127)
let byte: u8 = 65;
let valor_rune: rune = byte;    // 'A'

// ASCII estendido / Latin-1 (128-255)
let estendido: u8 = 200;
let r: rune = estendido;        // U+00C8 (E)

// Nota: 0-127 e ASCII, 128-255 e Latin-1
```

### Conversoes Encadeadas

Conversoes de tipo podem ser encadeadas:

```hemlock
// i32 -> rune -> string
let codigo: i32 = 128512;       // Ponto de codigo sorriso
let r: rune = codigo;           // 😀
let s: string = r;              // "😀"

// Em uma expressao
let emoji: string = 128640;     // Implicito i32 -> rune -> string (🚀)
```

## Operacoes com Runes

### Impressao

Runes sao exibidos de forma diferente dependendo do ponto de codigo:

```hemlock
let ascii = 'A';
print(ascii);                   // 'A' (com aspas, ASCII imprimivel)

let emoji = '🚀';
print(emoji);                   // U+1F680 (notacao Unicode para nao-ASCII)

let tab = '\t';
print(tab);                     // U+0009 (hex para nao-imprimiveis)

let espaco = ' ';
print(espaco);                  // ' ' (imprimivel)
```

**Formato de impressao:**
- ASCII imprimivel (32-126): Caractere com aspas `'A'`
- Nao-imprimivel ou Unicode: Notacao hexadecimal `U+XXXX`

### Verificacao de Tipo

Use `typeof()` para verificar se um valor e rune:

```hemlock
let r = '🚀';
print(typeof(r));               // "rune"

let s = "texto";
let ch = s[0];
print(typeof(ch));              // "rune" (indexacao retorna rune)

let num = 65;
print(typeof(num));             // "i32"
```

### Comparacao

Runes podem ser comparados por igualdade:

```hemlock
let a = 'A';
let b = 'B';
print(a == a);                  // true
print(a == b);                  // false

// Case-sensitive
let maiuscula = 'A';
let minuscula = 'a';
print(maiuscula == minuscula);  // false

// Runes podem ser comparados com inteiros (valor do ponto de codigo)
print(a == 65);                 // true (conversao implicita)
print('🚀' == 128640);          // true
```

**Operadores de comparacao:**
- `==` - Igual a
- `!=` - Diferente de
- `<`, `>`, `<=`, `>=` - Ordem de ponto de codigo

```hemlock
print('A' < 'B');               // true (65 < 66)
print('a' > 'Z');               // true (97 > 90)
```

## Trabalhando com Indexacao de Strings

Indexacao de strings retorna runes, nao bytes:

```hemlock
let s = "Hello🚀";
let h = s[0];                   // 'H' (rune)
let foguete = s[5];             // '🚀' (rune)

print(typeof(h));               // "rune"
print(typeof(foguete));         // "rune"

// Pode converter para string se necessario
let h_str: string = h;          // "H"
let foguete_str: string = foguete; // "🚀"
```

**Importante:** Indexacao de strings usa posicao de ponto de codigo, nao offset de byte:

```hemlock
let texto = "Oi🚀!";
// Posicoes de ponto de codigo: 0='O', 1='i', 2='🚀', 3='!'
// Posicoes de byte: 0='O', 1='i', 2-5='🚀', 6='!'

let r = texto[2];               // '🚀' (ponto de codigo 2)
print(typeof(r));               // "rune"
```

## Exemplos

### Exemplo: Classificacao de Caracteres

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

### Exemplo: Conversao de Caso

```hemlock
fn to_upper_rune(r: rune): rune {
    if (r >= 'a' && r <= 'z') {
        // Converte para maiuscula (subtrai 32)
        let codigo: i32 = r;
        codigo = codigo - 32;
        return codigo;
    }
    return r;
}

fn to_lower_rune(r: rune): rune {
    if (r >= 'A' && r <= 'Z') {
        // Converte para minuscula (adiciona 32)
        let codigo: i32 = r;
        codigo = codigo + 32;
        return codigo;
    }
    return r;
}

print(to_upper_rune('a'));      // 'A'
print(to_lower_rune('Z'));      // 'z'
```

### Exemplo: Iteracao de Caracteres

```hemlock
fn print_chars(s: string) {
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        print("Posicao " + typeof(i) + ": " + typeof(ch));
        i = i + 1;
    }
}

print_chars("Oi🚀");
// Posicao 0: 'O'
// Posicao 1: 'i'
// Posicao 2: U+1F680
```

### Exemplo: Construindo Strings a partir de Runes

```hemlock
fn repeat_char(ch: rune, count: i32): string {
    let resultado = "";
    let i = 0;
    while (i < count) {
        resultado = resultado + ch;
        i = i + 1;
    }
    return resultado;
}

let linha = repeat_char('=', 40);   // "========================================"
let estrelas = repeat_char('⭐', 5); // "⭐⭐⭐⭐⭐"
```

## Padroes Comuns

### Padrao: Filtragem de Caracteres

```hemlock
fn filter_digits(s: string): string {
    let resultado = "";
    let i = 0;
    while (i < s.length) {
        let ch = s[i];
        if (ch >= '0' && ch <= '9') {
            resultado = resultado + ch;
        }
        i = i + 1;
    }
    return resultado;
}

let texto = "abc123def456";
let digitos = filter_digits(texto);  // "123456"
```

### Padrao: Contagem de Caracteres

```hemlock
fn count_char(s: string, alvo: rune): i32 {
    let count = 0;
    let i = 0;
    while (i < s.length) {
        if (s[i] == alvo) {
            count = count + 1;
        }
        i = i + 1;
    }
    return count;
}

let texto = "hello world";
let count_l = count_char(texto, 'l');  // 3
let count_o = count_char(texto, 'o');  // 2
```

## Melhores Praticas

1. **Use rune para operacoes de caracteres** - Nao tente processar texto com bytes
2. **Indexacao de string retorna rune** - Lembre que `str[i]` retorna um rune
3. **Comparacoes conscientes de Unicode** - Runes tratam qualquer caractere Unicode
4. **Converta quando necessario** - Runes podem ser facilmente convertidos para strings e inteiros
5. **Teste com emojis** - Sempre teste operacoes de caracteres com caracteres multi-byte

## Armadilhas Comuns

### Armadilha: Confundir Rune com Byte

```hemlock
// Nao faca: tratar rune como byte
let r: rune = '🚀';
let b: u8 = r;              // Erro: ponto de codigo rune 128640 nao cabe em u8

// Faca: use conversao apropriada
let r: rune = '🚀';
let codigo: i32 = r;        // OK: 128640
```

### Armadilha: Indexacao de Bytes em String

```hemlock
// Nao faca: assumir indexacao por byte
let s = "🚀";
let byte = s.byte_at(0);    // 240 (primeiro byte UTF-8, nao caractere completo)

// Faca: use indexacao por ponto de codigo
let s = "🚀";
let rune = s[0];            // '🚀' (caractere completo)
let rune2 = s.char_at(0);   // '🚀' (metodo explicito)
```

## Topicos Relacionados

- [Strings](strings.md) - Operacoes de string e tratamento UTF-8
- [Tipos](types.md) - Sistema de tipos e conversoes
- [Fluxo de Controle](control-flow.md) - Usando runes em comparacoes

## Veja Tambem

- **Padrao Unicode**: Pontos de codigo Unicode sao definidos pelo Consorcio Unicode
- **Codificacao UTF-8**: Veja [Strings](strings.md) para detalhes de UTF-8
- **Conversao de Tipos**: Veja [Tipos](types.md) para regras de conversao
