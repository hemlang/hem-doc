# Strings

Strings em Hemlock são **sequências mutáveis com prioridade UTF-8**, com suporte completo a Unicode e métodos ricos para processamento de texto. Diferente de muitas linguagens, strings em Hemlock são mutáveis e suportam nativamente operações com pontos de código Unicode.

## Visão Geral

```hemlock
let s = "hello";
s[0] = 'H';             // Modifica usando rune (agora é "Hello")
print(s.length);        // 5 (contagem de codepoints)
let c = s[0];           // Retorna rune (ponto de código Unicode)
let msg = s + " world"; // Concatenação
let emoji = "🚀";
print(emoji.length);    // 1 (um codepoint)
print(emoji.byte_length); // 4 (quatro bytes UTF-8)
```

## Propriedades

Strings em Hemlock têm as seguintes características principais:

- **Codificação UTF-8** - Suporte completo a Unicode (U+0000 a U+10FFFF)
- **Mutáveis** - Diferente de Python, JavaScript e Java
- **Indexação baseada em codepoint** - Retorna `rune` (ponto de código Unicode), não bytes
- **Alocação no heap** - Com rastreamento interno de capacidade
- **Duas propriedades de comprimento**:
  - `.length` - Contagem de codepoints (caracteres)
  - `.byte_length` - Contagem de bytes (tamanho da codificação UTF-8)

## Comportamento UTF-8

Todas as operações de string usam **codepoints** (caracteres), não bytes:

```hemlock
let text = "Hello🚀World";
print(text.length);        // 11 (codepoints)
print(text.byte_length);   // 15 (bytes, emoji são 4 bytes)

// Indexação usa codepoints
let h = text[0];           // 'H' (rune)
let rocket = text[5];      // '🚀' (rune)
```

**Caracteres multibyte contam como um:**
```hemlock
"Hello".length;      // 5
"🚀".length;         // 1 (um emoji)
"你好".length;       // 2 (dois caracteres chineses)
"café".length;       // 4 (é é um codepoint)
```

## Literais de String

```hemlock
// Strings básicas
let s1 = "hello";
let s2 = "world";

// Com sequências de escape
let s3 = "Line 1\nLine 2\ttabbed";
let s4 = "Quote: \"Hello\"";
let s5 = "Backslash: \\";

// Caracteres Unicode
let s6 = "🚀 Emoji";
let s7 = "中文字符";
```

## Template Strings (Interpolação de Strings)

Use crases para criar template strings com expressões embutidas:

```hemlock
let name = "Alice";
let age = 30;

// Interpolação básica
let greeting = `Hello, ${name}!`;           // "Hello, Alice!"
let info = `${name} is ${age} years old`;   // "Alice is 30 years old"

// Expressões na interpolação
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;         // "5 + 10 = 15"

// Chamadas de método
let upper = `Name: ${name.to_upper()}`;     // "Name: ALICE"

// Objetos aninhados
let person = { name: "Bob", city: "NYC" };
let desc = `${person.name} lives in ${person.city}`;  // "Bob lives in NYC"

// Múltiplas linhas (preserva quebras)
let multi = `Line 1
Line 2
Line 3`;
```

**Características de template strings:**
- Expressões dentro de `${...}` são avaliadas e convertidas para string
- Pode usar qualquer expressão válida (variáveis, chamadas de função, aritmética)
- Strings com crases suportam as mesmas sequências de escape que strings normais
- Usa-se para construir strings dinâmicas sem concatenação

### Escape em Template Strings

Para incluir `${` literal em uma template string, escape o cifrão:

```hemlock
let price = 100;
let text = `Price: \${price} or ${price}`;
// "Price: ${price} or 100"

// Crase literal
let code = `Use \` for template strings`;
// "Use ` for template strings"
```

### Expressões Complexas

Template strings podem conter qualquer expressão válida:

```hemlock
// Tipo ternário
let age = 25;
let status = `Status: ${age >= 18 ? "adult" : "minor"}`;

// Acesso a array
let items = ["apple", "banana", "cherry"];
let first = `First item: ${items[0]}`;

// Chamada de função com parâmetros
fn format_price(p) { return "$" + p; }
let msg = `Total: ${format_price(99.99)}`;  // "Total: $99.99"

// Métodos encadeados
let name = "alice";
let formatted = `Hello, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Hello, Alice!"
```

### Template Strings vs Concatenação

Template strings geralmente são mais claras que concatenação:

```hemlock
// Concatenação (mais difícil de ler)
let msg1 = "Hello, " + name + "! You have " + count + " messages.";

// Template string (mais fácil de ler)
let msg2 = `Hello, ${name}! You have ${count} messages.`;
```

## Indexação e Modificação

### Lendo Caracteres

Indexação retorna `rune` (ponto de código Unicode):

```hemlock
let s = "Hello";
let first = s[0];      // 'H' (rune)
let last = s[4];       // 'o' (rune)

// Exemplo UTF-8
let emoji = "Hi🚀!";
let rocket = emoji[2];  // '🚀' (rune no índice de codepoint 2)
```

### Escrevendo Caracteres

Strings são mutáveis - pode modificar caracteres individuais:

```hemlock
let s = "hello";
s[0] = 'H';            // Agora é "Hello"
s[4] = '!';            // Agora é "Hell!"

// Exemplo Unicode
let msg = "Go!";
msg[0] = '🚀';         // Agora é "🚀o!"
```

## Concatenação

Use `+` para concatenar strings:

```hemlock
let greeting = "Hello" + " " + "World";  // "Hello World"

// Com variáveis
let name = "Alice";
let msg = "Hi, " + name + "!";  // "Hi, Alice!"

// Com rune (veja documentação de Runas)
let s = "Hello" + '!';          // "Hello!"
```

## Métodos de String

Hemlock fornece 19 métodos de string para manipulação abrangente de texto.

### Substrings e Fatiamento

**`substr(start, length)`** - Extrai substring por posição e comprimento:
```hemlock
let s = "hello world";
let sub = s.substr(6, 5);       // "world" (de 6, comprimento 5)
let first = s.substr(0, 5);     // "hello"

// Exemplo UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀" (posição 2, comprimento 1)
```

**`slice(start, end)`** - Extrai substring por intervalo (end não incluído):
```hemlock
let s = "hello world";
let slice = s.slice(0, 5);      // "hello" (índice 0 a 4)
let slice2 = s.slice(6, 11);    // "world"
```

**Diferença:**
- `substr(start, length)` - Usa parâmetro de comprimento
- `slice(start, end)` - Usa índice final (não incluído)

### Busca e Localização

**`find(needle)`** - Encontra primeira ocorrência:
```hemlock
let s = "hello world";
let pos = s.find("world");      // 6 (índice da primeira ocorrência)
let pos2 = s.find("foo");       // -1 (não encontrado)
let pos3 = s.find("l");         // 2 (primeiro 'l')
```

**`contains(needle)`** - Verifica se string contém substring:
```hemlock
let s = "hello world";
let has = s.contains("world");  // true
let has2 = s.contains("foo");   // false
```

### Divisão e Aparagem

**`split(delimiter)`** - Divide em array de strings:
```hemlock
let csv = "apple,banana,cherry";
let parts = csv.split(",");     // ["apple", "banana", "cherry"]

let words = "one two three".split(" ");  // ["one", "two", "three"]

// Delimitador vazio divide por caractere
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Remove espaços em branco do início e fim:
```hemlock
let s = "  hello  ";
let clean = s.trim();           // "hello"

let s2 = "\t\ntext\n\t";
let clean2 = s2.trim();         // "text"
```

### Conversão de Caso

**`to_upper()`** - Converte para maiúsculas:
```hemlock
let s = "hello world";
let upper = s.to_upper();       // "HELLO WORLD"

// Preserva caracteres não-ASCII
let s2 = "café";
let upper2 = s2.to_upper();     // "CAFÉ"
```

**`to_lower()`** - Converte para minúsculas:
```hemlock
let s = "HELLO WORLD";
let lower = s.to_lower();       // "hello world"
```

### Verificação de Prefixo/Sufixo

**`starts_with(prefix)`** - Verifica se começa com prefixo:
```hemlock
let s = "hello world";
let starts = s.starts_with("hello");  // true
let starts2 = s.starts_with("world"); // false
```

**`ends_with(suffix)`** - Verifica se termina com sufixo:
```hemlock
let s = "hello world";
let ends = s.ends_with("world");      // true
let ends2 = s.ends_with("hello");     // false
```

### Substituição

**`replace(old, new)`** - Substitui primeira ocorrência:
```hemlock
let s = "hello world";
let s2 = s.replace("world", "there");      // "hello there"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (apenas primeiro)
```

**`replace_all(old, new)`** - Substitui todas as ocorrências:
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "hello world, world!";
let s4 = s3.replace_all("world", "hemlock"); // "hello hemlock, hemlock!"
```

### Repetição

**`repeat(count)`** - Repete string n vezes:
```hemlock
let s = "ha";
let laugh = s.repeat(3);        // "hahaha"

let line = "=".repeat(40);      // "========================================"
```

### Acesso a Caracteres e Bytes

**`char_at(index)`** - Obtém ponto de código Unicode no índice (retorna rune):
```hemlock
let s = "hello";
let char = s.char_at(0);        // 'h' (rune)

// Exemplo UTF-8
let emoji = "🚀";
let rocket = emoji.char_at(0);  // Retorna rune U+1F680
```

**`chars()`** - Converte para array de runes (codepoints):
```hemlock
let s = "hello";
let chars = s.chars();          // ['h', 'e', 'l', 'l', 'o'] (array de runes)

// Exemplo UTF-8
let text = "Hi🚀";
let chars2 = text.chars();      // ['H', 'i', '🚀']
```

**`byte_at(index)`** - Obtém valor de byte no índice (retorna u8):
```hemlock
let s = "hello";
let byte = s.byte_at(0);        // 104 (valor ASCII de 'h')

// Exemplo UTF-8
let emoji = "🚀";
let first_byte = emoji.byte_at(0);  // 240 (primeiro byte UTF-8)
```

**`bytes()`** - Converte para array de bytes (valores u8):
```hemlock
let s = "hello";
let bytes = s.bytes();          // [104, 101, 108, 108, 111] (array u8)

// Exemplo UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 bytes UTF-8)
```

**`to_bytes()`** - Converte para buffer para acesso de baixo nível:
```hemlock
let s = "hello";
let buf = s.to_bytes();         // Retorna buffer contendo bytes UTF-8
print(buf.length);              // 5
free(buf);                      // Lembre-se de liberar
```

## Encadeamento de Métodos

Todos os métodos de string retornam novas strings, suportando encadeamento:

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

## Referência Completa de Métodos

| Método | Parâmetros | Retorno | Descrição |
|--------|-----------|---------|-------------|
| `substr(start, length)` | i32, i32 | string | Extrai substring por posição e comprimento |
| `slice(start, end)` | i32, i32 | string | Extrai substring por intervalo (end não incluído) |
| `find(needle)` | string | i32 | Encontra primeira ocorrência (retorna -1 se não encontrado) |
| `contains(needle)` | string | bool | Verifica se contém substring |
| `split(delimiter)` | string | array | Divide em array de strings |
| `trim()` | - | string | Remove espaços em branco do início e fim |
| `to_upper()` | - | string | Converte para maiúsculas |
| `to_lower()` | - | string | Converte para minúsculas |
| `starts_with(prefix)` | string | bool | Verifica se começa com prefixo |
| `ends_with(suffix)` | string | bool | Verifica se termina com sufixo |
| `replace(old, new)` | string, string | string | Substitui primeira ocorrência |
| `replace_all(old, new)` | string, string | string | Substitui todas as ocorrências |
| `repeat(count)` | i32 | string | Repete string n vezes |
| `char_at(index)` | i32 | rune | Obtém codepoint no índice |
| `byte_at(index)` | i32 | u8 | Obtém valor de byte no índice |
| `chars()` | - | array | Converte para array de runes |
| `bytes()` | - | array | Converte para array de bytes u8 |
| `to_bytes()` | - | buffer | Converte para buffer (precisa liberar) |

## Exemplos

### Exemplo: Processamento de Texto

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Normaliza espaços em branco
}

let input = "  HELLO   WORLD  ";
let clean = process_input(input);  // "hello world"
```

### Exemplo: Parser CSV

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

### Exemplo: Contador de Palavras

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "The quick brown fox";
let count = count_words(sentence);  // 4
```

### Exemplo: Validação de String

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

## Gerenciamento de Memória

Strings são alocadas no heap com contagem de referência interna:

- **Criação**: Aloca no heap com rastreamento de capacidade
- **Concatenação**: Cria nova string (strings antigas inalteradas)
- **Métodos**: A maioria dos métodos retorna novas strings
- **Ciclo de vida**: Strings usam contagem de referência, liberadas automaticamente ao sair do escopo

**Limpeza automática:**
```hemlock
fn create_strings() {
    let s = "hello";
    let s2 = s + " world";  // Nova alocação
}  // s e s2 liberadas automaticamente quando função retorna
```

**Nota:** Variáveis de string locais são limpas automaticamente ao sair do escopo. Use `free()` apenas quando precisar de limpeza antecipada (antes do fim do escopo) ou ao lidar com dados de longa duração/globais. Veja [Gerenciamento de Memória](memory.md#internal-reference-counting) para detalhes.

## Melhores Práticas

1. **Use indexação por codepoint** - Strings usam posições de codepoint, não offsets de byte
2. **Teste com Unicode** - Sempre teste operações de string com caracteres multibyte
3. **Prefira operações imutáveis** - Use métodos que retornam novas strings em vez de modificar diretamente
4. **Verifique limites** - Indexação de string não verifica limites (retorna null/erro se inválido)
5. **Normalize entrada** - Use `trim()` e `to_lower()` para entrada de usuário

## Armadilhas Comuns

### Armadilha: Confusão entre Bytes e Codepoints

```hemlock
let emoji = "🚀";
print(emoji.length);        // 1 (codepoints)
print(emoji.byte_length);   // 4 (bytes)

// Não misture operações de byte e codepoint
let byte = emoji.byte_at(0);  // 240 (primeiro byte)
let char = emoji.char_at(0);  // '🚀' (codepoint completo)
```

### Armadilha: Surpresas de Modificação

```hemlock
let s1 = "hello";
let s2 = s1;       // Cópia rasa
s1[0] = 'H';       // Modifica s1
print(s2);         // Ainda é "hello" (strings são tipo valor)
```

## Tópicos Relacionados

- [Runas](runes.md) - Tipo de ponto de código Unicode usado em indexação de string
- [Arrays](arrays.md) - Métodos de string frequentemente retornam ou usam arrays
- [Tipos](types.md) - Detalhes e conversões do tipo string

## Veja Também

- **Codificação UTF-8**: Veja seção "Strings" em CLAUDE.md
- **Conversão de tipos**: Veja [Tipos](types.md) para conversão de strings
- **Memória**: Veja [Memória](memory.md) para detalhes de alocação de strings
