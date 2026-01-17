# Referencia do Sistema de Tipos

Referencia completa do sistema de tipos do Hemlock, incluindo todos os tipos primitivos e compostos.

---

## Visao Geral

Hemlock usa um **sistema de tipos dinamico** com tags de tipo em tempo de execucao e anotacoes de tipo opcionais. Todo valor tem um tipo em tempo de execucao, e conversoes de tipo seguem regras de promocao claras.

**Caracteristicas Principais:**
- Verificacao de tipo em tempo de execucao (interpretador)
- Verificacao de tipo em tempo de compilacao (hemlockc - habilitada por padrao)
- Anotacoes de tipo opcionais
- Inferencia de tipo automatica para literais
- Regras de promocao de tipo claras
- Sem conversoes implicitas que percam precisao

---

## Verificacao de Tipo em Tempo de Compilacao (hemlockc)

O compilador Hemlock (`hemlockc`) inclui um verificador de tipo em tempo de compilacao que valida seu codigo antes de gerar o executavel. Isso detecta erros de tipo cedo sem executar o programa.

### Comportamento Padrao

Verificacao de tipo e **habilitada por padrao** no hemlockc:

```bash
# Verificacao de tipo acontece automaticamente
hemlockc program.hml -o program

# Erros sao reportados antes da compilacao
hemlockc bad_types.hml
# Saida: 1 type error found
```

### Flags do Compilador

| Flag | Descricao |
|------|-----------|
| `--check` | Apenas verifica tipos, nao compila (termina apos validacao) |
| `--no-type-check` | Desabilita verificacao de tipo (nao recomendado) |
| `--strict-types` | Habilita avisos mais rigorosos de tipo |

**Exemplo:**

```bash
# Apenas valida tipos sem compilar
hemlockc --check program.hml
# Saida: program.hml: no type errors

# Desabilita verificacao de tipo (use com cautela)
hemlockc --no-type-check dynamic_code.hml -o program

# Habilita avisos rigorosos para tipos 'any' implicitos
hemlockc --strict-types program.hml -o program
```

### O Que o Verificador de Tipo Valida

1. **Anotacoes de Tipo** - Garante que valores atribuidos correspondam aos tipos declarados
2. **Chamadas de Funcao** - Verifica que tipos de argumentos correspondam aos tipos de parametros
3. **Tipos de Retorno** - Verifica que instrucoes return correspondam ao tipo de retorno declarado
4. **Uso de Operadores** - Valida que operandos sao compativeis
5. **Acesso a Propriedades** - Verifica tipos de campo de objeto para objetos tipados

### Coercao Numerica Relaxada

O verificador de tipo permite coercoes de tipo numerico em tempo de compilacao, com validacao de faixa em tempo de execucao:

```hemlock
let x: i8 = 100;      // OK - 100 cabe em i8 (validado em tempo de execucao)
let y: u8 = 255;      // OK - dentro da faixa de u8
let z: f64 = 42;      // OK - i32 para f64 e seguro
```

### Suporte a Codigo Dinamico

Codigo sem anotacoes de tipo e tratado como dinamico (tipo `any`), e sempre passa no verificador de tipo:

```hemlock
let x = get_value();  // Dinamico - sem anotacao
process(x);           // OK - valores dinamicos aceitos em qualquer lugar
```

---

## Tipos Primitivos

### Tipos Numericos

#### Inteiros com Sinal

| Tipo   | Tamanho | Faixa                                      | Alias     |
|--------|---------|-------------------------------------------|-----------|
| `i8`   | 1 byte  | -128 a 127                                | -         |
| `i16`  | 2 bytes | -32.768 a 32.767                          | -         |
| `i32`  | 4 bytes | -2.147.483.648 a 2.147.483.647            | `integer` |
| `i64`  | 8 bytes | -9.223.372.036.854.775.808 a 9.223.372.036.854.775.807 | - |

**Exemplo:**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Alias de tipo
let x: integer = 42;  // Mesmo que i32
```

#### Inteiros sem Sinal

| Tipo   | Tamanho | Faixa                         | Alias  |
|--------|---------|-------------------------------|--------|
| `u8`   | 1 byte  | 0 a 255                       | `byte` |
| `u16`  | 2 bytes | 0 a 65.535                    | -      |
| `u32`  | 4 bytes | 0 a 4.294.967.295             | -      |
| `u64`  | 8 bytes | 0 a 18.446.744.073.709.551.615| -      |

**Exemplo:**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Alias de tipo
let byte_val: byte = 65;  // Mesmo que u8
```

#### Ponto Flutuante

| Tipo   | Tamanho | Precisao              | Alias    |
|--------|---------|----------------------|----------|
| `f32`  | 4 bytes | ~7 digitos           | -        |
| `f64`  | 8 bytes | ~15 digitos          | `number` |

**Exemplo:**
```hemlock
let pi: f32 = 3.14159;
let precise: f64 = 3.14159265359;

// Alias de tipo
let x: number = 2.718;  // Mesmo que f64
```

---

### Inferencia de Literais Inteiros

Literais inteiros determinam seu tipo automaticamente baseado no valor:

**Regras:**
- Valores na faixa de i32 (-2.147.483.648 a 2.147.483.647): inferidos como `i32`
- Valores fora da faixa de i32 mas na faixa de i64: inferidos como `i64`
- Outros tipos (i8, i16, u8, u16, u32, u64) usam anotacoes de tipo explicitas

**Exemplo:**
```hemlock
let small = 42;                    // i32 (cabe em i32)
let large = 5000000000;            // i64 (> i32 max)
let max_i64 = 9223372036854775807; // i64 (INT64_MAX)
let explicit: u32 = 100;           // u32 (anotacao de tipo sobrescreve)
```

---

### Tipo Booleano

**Tipo:** `bool`

**Valores:** `true`, `false`

**Tamanho:** 1 byte (internamente)

**Exemplo:**
```hemlock
let is_active: bool = true;
let done = false;

if (is_active && !done) {
    print("trabalhando");
}
```

---

### Tipos de Caractere

#### Rune

**Tipo:** `rune`

**Descricao:** Ponto de codigo Unicode (U+0000 a U+10FFFF)

**Tamanho:** 4 bytes (valor de 32 bits)

**Faixa:** 0 a 0x10FFFF (1.114.111)

**Sintaxe Literal:** Aspas simples `'x'`

**Exemplo:**
```hemlock
// ASCII
let a = 'A';
let digit = '0';

// UTF-8 multi-byte
let rocket = '🚀';      // U+1F680
let heart = '❤';        // U+2764
let chinese = '中';     // U+4E2D

// Sequencias de escape
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let quote = '\'';
let null = '\0';

// Escapes Unicode
let emoji = '\u{1F680}';   // Ate 6 digitos hex
let max = '\u{10FFFF}';    // Ponto de codigo maximo
```

**Conversoes de Tipo:**
```hemlock
// Inteiro para rune
let code: rune = 65;        // 'A'
let r: rune = 128640;       // 🚀

// Rune para inteiro
let value: i32 = 'Z';       // 90

// Rune para string
let s: string = 'H';        // "H"

// u8 para rune
let byte: u8 = 65;
let rune_val: rune = byte;  // 'A'
```

**Veja Tambem:** [API de Strings](string-api.md) para concatenacao string + rune

---

### Tipo String

**Tipo:** `string`

**Descricao:** Texto codificado em UTF-8, mutavel, alocado no heap

**Codificacao:** UTF-8 (U+0000 a U+10FFFF)

**Mutabilidade:** Mutavel (diferente da maioria das linguagens)

**Propriedades:**
- `.length` - Contagem de pontos de codigo (caracteres)
- `.byte_length` - Contagem de bytes (tamanho de codificacao UTF-8)

**Sintaxe Literal:** Aspas duplas `"texto"`

**Exemplo:**
```hemlock
let s = "hello";
s[0] = 'H';             // Muta (agora "Hello")
print(s.length);        // 5 (contagem de pontos de codigo)
print(s.byte_length);   // 5 (bytes UTF-8)

let emoji = "🚀";
print(emoji.length);        // 1 (um ponto de codigo)
print(emoji.byte_length);   // 4 (quatro bytes UTF-8)
```

**Indexacao:**
```hemlock
let s = "hello";
let ch = s[0];          // Retorna rune 'h'
s[0] = 'H';             // Define com rune
```

**Veja Tambem:** [API de Strings](string-api.md) para referencia completa de metodos

---

### Tipo Null

**Tipo:** `null`

**Descricao:** Valor nulo (representa ausencia de valor)

**Tamanho:** 8 bytes (internamente)

**Valor:** `null`

**Exemplo:**
```hemlock
let x = null;
let y: i32 = null;  // ERRO: tipo incompativel

if (x == null) {
    print("x e nulo");
}
```

---

## Tipos Compostos

### Tipo Array

**Tipo:** `array`

**Descricao:** Array dinamico, alocado no heap, de tipo misto

**Propriedades:**
- `.length` - Numero de elementos

**Baseado em Zero:** Sim

**Sintaxe Literal:** `[elem1, elem2, ...]`

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipos mistos
let mixed = [1, "hello", true, null];
```

**Veja Tambem:** [API de Arrays](array-api.md) para referencia completa de metodos

---

### Tipo Objeto

**Tipo:** `object`

**Descricao:** Objeto de campos dinamicos estilo JavaScript

**Sintaxe Literal:** `{ campo: valor, ... }`

**Exemplo:**
```hemlock
let person = { name: "Alice", age: 30 };
print(person.name);  // "Alice"

// Adiciona campo dinamicamente
person.email = "alice@example.com";
```

**Definicoes de Tipo:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: bool,  // Campo opcional
}

let p: Person = { name: "Bob", age: 25 };
print(typeof(p));  // "Person"
```

---

### Tipos de Ponteiro

#### Ponteiro Bruto (ptr)

**Tipo:** `ptr`

**Descricao:** Endereco de memoria bruto (inseguro)

**Tamanho:** 8 bytes

**Verificacao de Limites:** Nenhuma

**Exemplo:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### Buffer

**Tipo:** `buffer`

**Descricao:** Wrapper de ponteiro seguro com verificacao de limites

**Estrutura:** Ponteiro + comprimento + capacidade

**Propriedades:**
- `.length` - Tamanho do buffer
- `.capacity` - Capacidade alocada

**Exemplo:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificacao de limites
print(b.length);        // 64
free(b);
```

**Veja Tambem:** [API de Memoria](memory-api.md) para funcoes de alocacao

---

## Tipos Especiais

### Tipo File

**Tipo:** `file`

**Descricao:** Handle de arquivo para operacoes de I/O

**Propriedades:**
- `.path` - Caminho do arquivo (string)
- `.mode` - Modo de abertura (string)
- `.closed` - Se o arquivo esta fechado (bool)

**Veja Tambem:** [API de Arquivos](file-api.md)

---

### Tipo Task

**Tipo:** `task`

**Descricao:** Handle para uma tarefa concorrente

**Veja Tambem:** [API de Concorrencia](concurrency-api.md)

---

### Tipo Channel

**Tipo:** `channel`

**Descricao:** Canal de comunicacao thread-safe

**Veja Tambem:** [API de Concorrencia](concurrency-api.md)

---

### Tipo Function

**Tipo:** `function`

**Descricao:** Valor de funcao de primeira classe

**Exemplo:**
```hemlock
fn add(a, b) {
    return a + b;
}

let multiply = fn(x, y) {
    return x * y;
};

print(typeof(add));      // "function"
print(typeof(multiply)); // "function"
```

---

### Tipo Void

**Tipo:** `void`

**Descricao:** Representa nenhum valor de retorno (uso interno)

---

## Regras de Promocao de Tipo

Quando tipos sao misturados em operacoes, Hemlock promove para o tipo "maior":

**Hierarquia de Promocao:**
```
f64 (maior precisao)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (menor)
```

**Regras:**
1. Floats sempre tem precedencia sobre inteiros
2. Dentro da mesma categoria (int/uint/float) tamanho maior tem precedencia
3. Ambos operandos sao promovidos para o tipo resultado
4. **Preservacao de Precisao:** i64/u64 + f32 promove para f64 (nao f32)

**Exemplo:**
```hemlock
// Promocao de tamanho
u8 + i32    → i32    // Tamanho maior vence
i32 + i64   → i64    // Tamanho maior vence
u32 + u64   → u64    // Tamanho maior vence

// Promocao de float
i32 + f32   → f32    // Float vence, f32 suficiente para i32
i64 + f32   → f64    // Promove para f64 para preservar precisao de i64
i64 + f64   → f64    // Float sempre vence
i8 + f64    → f64    // Float + maior vence
```

**Por que i64 + f32 → f64?**

f32 tem apenas 24 bits de mantissa, nao pode representar precisamente inteiros maiores que 2^24 (16.777.216). Como i64 pode armazenar valores ate 2^63, misturar i64 com f32 causaria perda severa de precisao. Hemlock promove para f64 (53 bits de mantissa) em vez disso.

---

## Verificacao de Faixa

Anotacoes de tipo aplicam verificacao de faixa na atribuicao:

**Atribuicoes Validas:**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**Atribuicoes Invalidas (erro de runtime):**
```hemlock
let x: u8 = 256;             // ERRO: fora da faixa
let y: i8 = 128;             // ERRO: max e 127
let z: u64 = -1;             // ERRO: u64 nao pode ser negativo
```

---

## Introspeccao de Tipo

### typeof(value)

Retorna o nome do tipo como string.

**Assinatura:**
```hemlock
typeof(value: any): string
```

**Retorna:**
- Tipos primitivos: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Tipos compostos: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Tipos especiais: `"file"`, `"task"`, `"channel"`
- Objetos tipados: Nome de tipo personalizado (ex: `"Person"`)

**Exemplo:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"
```

**Veja Tambem:** [Funcoes Integradas](builtins.md#typeof)

---

## Conversao de Tipo

### Conversao Implicita

Hemlock realiza conversao implicita de tipo em operacoes aritmeticas seguindo regras de promocao de tipo.

**Exemplo:**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let result = a + b;     // result e i32 (promovido)
```

### Conversao Explicita

Use anotacoes de tipo para conversao explicita:

**Exemplo:**
```hemlock
// Inteiro para float
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Float para inteiro (trunca)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Inteiro para rune
let code: rune = 65;    // 'A'

// Rune para inteiro
let value: i32 = 'Z';   // 90

// Rune para string
let s: string = 'H';    // "H"
```

---

## Alias de Tipo

### Alias Integrados

Hemlock fornece alias de tipo integrados para tipos comuns:

| Alias     | Tipo Real | Uso           |
|-----------|----------|---------------|
| `integer` | `i32`    | Inteiro geral |
| `number`  | `f64`    | Float geral   |
| `byte`    | `u8`     | Valores de byte |

**Exemplo:**
```hemlock
let count: integer = 100;       // Mesmo que i32
let price: number = 19.99;      // Mesmo que f64
let b: byte = 255;              // Mesmo que u8
```

### Alias de Tipo Personalizados

Use a palavra-chave `type` para definir alias de tipo personalizados:

```hemlock
// Alias simples
type Integer = i32;
type Text = string;

// Alias de tipo de funcao
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

// Alias de tipo composto
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Alias de tipo generico
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
```

**Usando alias personalizados:**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Nota:** Alias de tipo sao transparentes - `typeof()` retorna o nome do tipo subjacente.

---

## Tipos de Funcao

Tipos de funcao especificam a assinatura de valores de funcao:

### Sintaxe

```hemlock
fn(tipos_parametros): tipo_retorno
```

### Exemplos

```hemlock
// Tipo de funcao basico
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parametro de funcao
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Funcao de ordem superior retornando funcao
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tipo de funcao assincrona
fn run_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## Tipos Compostos (Tipos de Intersecao)

Tipos compostos usam `&` para requerer multiplas restricoes de tipo:

```hemlock
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Objeto deve satisfazer todos os tipos
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Tres ou mais tipos
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

---

## Tabela de Resumo

| Tipo       | Tamanho  | Mutavel | Heap | Descricao                |
|------------|----------|---------|------|--------------------------|
| `i8`-`i64` | 1-8 bytes | Nao    | Nao  | Inteiros com sinal       |
| `u8`-`u64` | 1-8 bytes | Nao    | Nao  | Inteiros sem sinal       |
| `f32`      | 4 bytes  | Nao    | Nao  | Float precisao simples   |
| `f64`      | 8 bytes  | Nao    | Nao  | Float precisao dupla     |
| `bool`     | 1 byte   | Nao    | Nao  | Booleano                 |
| `rune`     | 4 bytes  | Nao    | Nao  | Ponto de codigo Unicode  |
| `string`   | Variavel | Sim    | Sim  | Texto UTF-8              |
| `array`    | Variavel | Sim    | Sim  | Array dinamico           |
| `object`   | Variavel | Sim    | Sim  | Objeto dinamico          |
| `ptr`      | 8 bytes  | Nao    | Nao  | Ponteiro bruto           |
| `buffer`   | Variavel | Sim    | Sim  | Wrapper de ponteiro seguro |
| `file`     | Opaco    | Sim    | Sim  | Handle de arquivo        |
| `task`     | Opaco    | Nao    | Sim  | Handle de tarefa concorrente |
| `channel`  | Opaco    | Sim    | Sim  | Canal thread-safe        |
| `function` | Opaco    | Nao    | Sim  | Valor de funcao          |
| `null`     | 8 bytes  | Nao    | Nao  | Valor nulo               |

---

## Veja Tambem

- [Referencia de Operadores](operators.md) - Comportamento de tipo em operacoes
- [Funcoes Integradas](builtins.md) - Introspeccao e conversao de tipo
- [API de Strings](string-api.md) - Metodos do tipo string
- [API de Arrays](array-api.md) - Metodos do tipo array
- [API de Memoria](memory-api.md) - Operacoes com ponteiro e buffer
