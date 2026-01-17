# Referencia da API de Strings

Referencia completa do tipo string do Hemlock e todos os seus 19 metodos de string.

---

## Visao Geral

Strings em Hemlock sao sequencias **codificadas em UTF-8, mutaveis e alocadas no heap** com suporte completo a Unicode. Todas as operacoes sao baseadas em **pontos de codigo** (caracteres), nao em bytes.

**Caracteristicas Principais:**
- Codificacao UTF-8 (U+0000 a U+10FFFF)
- Mutavel (pode modificar caracteres no local)
- Indexacao baseada em pontos de codigo
- 19 metodos integrados
- Concatenacao automatica com operador `+`

---

## Tipo String

**Tipo:** `string`

**Propriedades:**
- `.length` - Numero de pontos de codigo (caracteres)
- `.byte_length` - Numero de bytes UTF-8

**Sintaxe Literal:** Aspas duplas `"texto"`

**Exemplo:**
```hemlock
let s = "hello";
print(s.length);        // 5 (pontos de codigo)
print(s.byte_length);   // 5 (bytes)

let emoji = "🚀";
print(emoji.length);        // 1 (um ponto de codigo)
print(emoji.byte_length);   // 4 (quatro bytes UTF-8)
```

---

## Indexacao

Strings suportam indexacao baseada em pontos de codigo usando `[]`:

**Acesso de Leitura:**
```hemlock
let s = "hello";
let ch = s[0];          // Retorna rune 'h'
```

**Acesso de Escrita:**
```hemlock
let s = "hello";
s[0] = 'H';             // Muta com rune (agora "Hello")
```

**Exemplo UTF-8:**
```hemlock
let text = "Hi🚀!";
print(text[0]);         // 'H'
print(text[1]);         // 'i'
print(text[2]);         // '🚀' (um ponto de codigo)
print(text[3]);         // '!'
```

---

## Concatenacao

Use o operador `+` para concatenar strings e runes:

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

**Concatenacao Multipla:**
```hemlock
let msg = "Hi " + '👋' + " World " + '🌍';  // "Hi 👋 World 🌍"
```

---

## Propriedades de String

### .length

Obtem o numero de pontos de codigo Unicode (caracteres).

**Tipo:** `i32`

**Exemplo:**
```hemlock
let s = "hello";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (um ponto de codigo)

let text = "Hello 🌍!";
print(text.length);     // 8 (7 ASCII + 1 emoji)
```

---

### .byte_length

Obtem o numero de bytes UTF-8.

**Tipo:** `i32`

**Exemplo:**
```hemlock
let s = "hello";
print(s.byte_length);   // 5 (1 byte por caractere ASCII)

let emoji = "🚀";
print(emoji.byte_length); // 4 (emoji sao 4 bytes UTF-8)

let text = "Hello 🌍!";
print(text.byte_length);  // 11 (7 ASCII + 4 para emoji)
```

---

## Metodos de String

### Substrings e Fatiamento

#### substr

Extrai substring por posicao e comprimento.

**Assinatura:**
```hemlock
string.substr(start: i32, length: i32): string
```

**Parametros:**
- `start` - Indice do ponto de codigo inicial (baseado em 0)
- `length` - Numero de pontos de codigo a extrair

**Retorna:** Nova string

**Exemplo:**
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world"
let first = s.substr(0, 5);     // "hello"

// Exemplo UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀"
```

---

#### slice

Extrai substring por intervalo (final exclusivo).

**Assinatura:**
```hemlock
string.slice(start: i32, end: i32): string
```

**Parametros:**
- `start` - Indice do ponto de codigo inicial (baseado em 0)
- `end` - Indice do ponto de codigo final (exclusivo)

**Retorna:** Nova string

**Exemplo:**
```hemlock
let s = "hello world";
let sub = s.slice(0, 5);        // "hello"
let world = s.slice(6, 11);     // "world"

// Exemplo UTF-8
let text = "Hi🚀!";
let first_three = text.slice(0, 3);  // "Hi🚀"
```

---

### Busca e Localizacao

#### find

Encontra a primeira ocorrencia de uma substring.

**Assinatura:**
```hemlock
string.find(needle: string): i32
```

**Parametros:**
- `needle` - A substring a ser buscada

**Retorna:** Indice do ponto de codigo da primeira ocorrencia, ou `-1` se nao encontrada

**Exemplo:**
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6
let pos2 = s.find("foo");       // -1 (nao encontrado)
let pos3 = s.find("l");         // 2 (primeiro 'l')
```

---

#### contains

Verifica se a string contem uma substring.

**Assinatura:**
```hemlock
string.contains(needle: string): bool
```

**Parametros:**
- `needle` - A substring a ser buscada

**Retorna:** `true` se encontrada, caso contrario `false`

**Exemplo:**
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

---

### Divisao e Uniao

#### split

Divide a string em um array por delimitador.

**Assinatura:**
```hemlock
string.split(delimiter: string): array
```

**Parametros:**
- `delimiter` - A string pela qual dividir

**Retorna:** Array de strings

**Exemplo:**
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

Remove espacos em branco do inicio e fim.

**Assinatura:**
```hemlock
string.trim(): string
```

**Retorna:** Nova string com espacos removidos

**Exemplo:**
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let text = "\n\t  world  \n";
let clean2 = text.trim();       // "world"
```

---

### Conversao de Maiusculas/Minusculas

#### to_upper

Converte a string para maiusculas.

**Assinatura:**
```hemlock
string.to_upper(): string
```

**Retorna:** Nova string em maiusculas

**Exemplo:**
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

let mixed = "HeLLo";
let upper2 = mixed.to_upper();  // "HELLO"
```

---

#### to_lower

Converte a string para minusculas.

**Assinatura:**
```hemlock
string.to_lower(): string
```

**Retorna:** Nova string em minusculas

**Exemplo:**
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"

let mixed = "HeLLo";
let lower2 = mixed.to_lower();  // "hello"
```

---

### Prefixo e Sufixo

#### starts_with

Verifica se a string comeca com o prefixo especificado.

**Assinatura:**
```hemlock
string.starts_with(prefix: string): bool
```

**Parametros:**
- `prefix` - O prefixo a verificar

**Retorna:** `true` se a string comecar com o prefixo, caso contrario `false`

**Exemplo:**
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

---

#### ends_with

Verifica se a string termina com o sufixo especificado.

**Assinatura:**
```hemlock
string.ends_with(suffix: string): bool
```

**Parametros:**
- `suffix` - O sufixo a verificar

**Retorna:** `true` se a string terminar com o sufixo, caso contrario `false`

**Exemplo:**
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

---

### Substituicao

#### replace

Substitui a primeira ocorrencia de uma substring.

**Assinatura:**
```hemlock
string.replace(old: string, new: string): string
```

**Parametros:**
- `old` - A substring a ser substituida
- `new` - A string de substituicao

**Retorna:** Nova string com a primeira ocorrencia substituida

**Exemplo:**
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");  // "hello there"

let text = "foo foo foo";
let text2 = text.replace("foo", "bar"); // "bar foo foo" (apenas a primeira)
```

---

#### replace_all

Substitui todas as ocorrencias de uma substring.

**Assinatura:**
```hemlock
string.replace_all(old: string, new: string): string
```

**Parametros:**
- `old` - A substring a ser substituida
- `new` - A string de substituicao

**Retorna:** Nova string com todas as ocorrencias substituidas

**Exemplo:**
```hemlock
let text = "foo foo foo";
let text2 = text.replace_all("foo", "bar"); // "bar bar bar"

let s = "hello world hello";
let s2 = s.replace_all("hello", "hi");      // "hi world hi"
```

---

### Repeticao

#### repeat

Repete a string n vezes.

**Assinatura:**
```hemlock
string.repeat(count: i32): string
```

**Parametros:**
- `count` - Numero de repeticoes

**Retorna:** Nova string repetida count vezes

**Exemplo:**
```hemlock
let s = "ha";
let repeated = s.repeat(3);     // "hahaha"

let line = "-";
let separator = line.repeat(40); // "----------------------------------------"
```

---

### Acesso a Caracteres

#### char_at

Obtem o ponto de codigo Unicode em um indice especificado.

**Assinatura:**
```hemlock
string.char_at(index: i32): rune
```

**Parametros:**
- `index` - Indice do ponto de codigo (baseado em 0)

**Retorna:** Rune (ponto de codigo Unicode)

**Exemplo:**
```hemlock
let s = "hello";
let ch = s.char_at(0);          // 'h'
let ch2 = s.char_at(1);         // 'e'

// Exemplo UTF-8
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (foguete)
```

---

#### chars

Converte a string em um array de runes.

**Assinatura:**
```hemlock
string.chars(): array
```

**Retorna:** Array de runes (pontos de codigo)

**Exemplo:**
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o']

// Exemplo UTF-8
let text = "Hi🚀!";
let chars2 = text.chars();      // ['H', 'i', '🚀', '!']
```

---

### Acesso a Bytes

#### byte_at

Obtem o valor do byte em um indice especificado.

**Assinatura:**
```hemlock
string.byte_at(index: i32): u8
```

**Parametros:**
- `index` - Indice do byte (baseado em 0, nao indice de ponto de codigo)

**Retorna:** Valor do byte (u8)

**Exemplo:**
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (ASCII 'h')
let byte2 = s.byte_at(1);       // 101 (ASCII 'e')

// Exemplo UTF-8
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (primeiro byte UTF-8)
```

---

#### bytes

Converte a string em um array de bytes.

**Assinatura:**
```hemlock
string.bytes(): array
```

**Retorna:** Array de bytes u8

**Exemplo:**
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111]

// Exemplo UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 bytes UTF-8)
```

---

#### to_bytes

Converte a string em um buffer.

**Assinatura:**
```hemlock
string.to_bytes(): buffer
```

**Retorna:** Buffer contendo bytes UTF-8

**Exemplo:**
```hemlock
let s = "hello";
let buf = s.to_bytes();
print(buf.length);              // 5

// Exemplo UTF-8
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Nota:** Este e um metodo legado. Prefira `.bytes()` na maioria dos casos.

---

### Desserializacao JSON

#### deserialize

Analisa uma string JSON em um valor.

**Assinatura:**
```hemlock
string.deserialize(): any
```

**Retorna:** Valor analisado (objeto, array, numero, string, booleano ou null)

**Exemplo:**
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

**Tipos Suportados:**
- Objetos: `{"key": value}`
- Arrays: `[1, 2, 3]`
- Numeros: `42`, `3.14`
- Strings: `"texto"`
- Booleanos: `true`, `false`
- Nulo: `null`

**Veja Tambem:** Metodo `.serialize()` de objetos

---

## Encadeamento de Metodos

Metodos de string podem ser encadeados para operacoes concisas:

**Exemplo:**
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

## Resumo Completo dos Metodos

| Metodo         | Assinatura                                       | Retorna   | Descricao                         |
|----------------|--------------------------------------------------|-----------|-----------------------------------|
| `substr`       | `(start: i32, length: i32)`                      | `string`  | Extrai substring por posicao/comprimento |
| `slice`        | `(start: i32, end: i32)`                         | `string`  | Extrai substring por intervalo    |
| `find`         | `(needle: string)`                               | `i32`     | Encontra primeira ocorrencia (-1 se nao encontrada) |
| `contains`     | `(needle: string)`                               | `bool`    | Verifica se contem substring      |
| `split`        | `(delimiter: string)`                            | `array`   | Divide em array                   |
| `trim`         | `()`                                             | `string`  | Remove espacos em branco          |
| `to_upper`     | `()`                                             | `string`  | Converte para maiusculas          |
| `to_lower`     | `()`                                             | `string`  | Converte para minusculas          |
| `starts_with`  | `(prefix: string)`                               | `bool`    | Verifica se comeca com prefixo    |
| `ends_with`    | `(suffix: string)`                               | `bool`    | Verifica se termina com sufixo    |
| `replace`      | `(old: string, new: string)`                     | `string`  | Substitui primeira ocorrencia     |
| `replace_all`  | `(old: string, new: string)`                     | `string`  | Substitui todas as ocorrencias    |
| `repeat`       | `(count: i32)`                                   | `string`  | Repete a string n vezes           |
| `char_at`      | `(index: i32)`                                   | `rune`    | Obtem ponto de codigo no indice   |
| `byte_at`      | `(index: i32)`                                   | `u8`      | Obtem byte no indice              |
| `chars`        | `()`                                             | `array`   | Converte para array de runes      |
| `bytes`        | `()`                                             | `array`   | Converte para array de bytes      |
| `to_bytes`     | `()`                                             | `buffer`  | Converte para buffer (legado)     |
| `deserialize`  | `()`                                             | `any`     | Analisa string JSON               |

---

## Veja Tambem

- [Sistema de Tipos](type-system.md) - Detalhes do tipo string
- [API de Arrays](array-api.md) - Metodos de array para resultados de split()
- [Operadores](operators.md) - Operador de concatenacao de strings
