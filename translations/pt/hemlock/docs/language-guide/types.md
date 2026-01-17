# Sistema de Tipos

Hemlock possui um **sistema de tipos dinâmico** com anotações de tipo opcionais e verificação de tipo em tempo de execução.

---

## Guia de Escolha de Tipos: Qual tipo devo usar?

**Novo em tipos?** Comece aqui. Se você está familiarizado com sistemas de tipos, pule para [Filosofia de Design](#filosofia-de-design).

### Resposta Curta

**Deixe o Hemlock decidir automaticamente:**

```hemlock
let count = 42;        // Hemlock sabe que é um inteiro
let price = 19.99;     // Hemlock sabe que é um decimal
let name = "Alice";    // Hemlock sabe que é texto
let active = true;     // Hemlock sabe que é booleano
```

Hemlock escolherá automaticamente o tipo correto para seus valores. Você *não precisa* especificar tipos.

### Quando Adicionar Anotações de Tipo

Adicione tipos quando:

1. **Precisa especificar tamanho** - `i8` vs `i64` é importante para memória ou FFI
2. **Documentar código** - Tipos mostram o que a função espera
3. **Detectar erros cedo** - Hemlock verifica tipos em tempo de execução

```hemlock
// Sem tipos (funciona normalmente):
fn add(a, b) {
    return a + b;
}

// Com tipos (mais explícito):
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Referência Rápida: Escolhendo Tipos Numéricos

| O que armazenar | Tipo recomendado | Exemplo |
|---------|---------|------|
| Inteiros comuns | `i32` (padrão) | `let count = 42;` |
| Números muito grandes | `i64` | `let population = 8000000000;` |
| Contagens nunca negativas | `u32` | `let items: u32 = 100;` |
| Bytes (0-255) | `u8` | `let pixel: u8 = 255;` |
| Decimais/frações | `f64` (padrão) | `let price = 19.99;` |
| Decimais críticos para performance | `f32` | `let x: f32 = 1.5;` |

### Referência Rápida: Todos os Tipos

| Categoria | Tipo | Quando usar |
|-----|------|---------|
| **Inteiros** | `i8`, `i16`, `i32`, `i64` | Contagens, IDs, idades etc. |
| **Apenas positivos** | `u8`, `u16`, `u32`, `u64` | Bytes, tamanhos, comprimentos de array |
| **Decimais** | `f32`, `f64` | Valores monetários, medidas, cálculos matemáticos |
| **Sim/Não** | `bool` | Flags, condições |
| **Texto** | `string` | Nomes, mensagens, qualquer texto |
| **Caractere único** | `rune` | Letras individuais, emojis |
| **Listas** | `array` | Coleções de valores |
| **Campos nomeados** | `object` | Agrupar dados relacionados |
| **Memória bruta** | `ptr`, `buffer` | Programação de baixo nível |
| **Valor vazio** | `null` | Representar ausência de valor |

### Cenários Comuns

**"Só preciso de um número"**
```hemlock
let x = 42;  // Pronto! Hemlock escolhe i32
```

**"Preciso de decimais"**
```hemlock
let price = 19.99;  // Pronto! Hemlock escolhe f64
```

**"Estou trabalhando com bytes (arquivos, rede)"**
```hemlock
let byte: u8 = 255;  // Faixa 0-255
```

**"Preciso de números muito grandes"**
```hemlock
let big = 9000000000000;  // Hemlock escolhe i64 automaticamente (> máx i32)
// Ou explicitamente:
let big: i64 = 9000000000000;
```

**"Estou armazenando valores monetários"**
```hemlock
// Opção 1: Ponto flutuante (simples, mas com limitações de precisão)
let price: f64 = 19.99;

// Opção 2: Armazenar em centavos (mais preciso)
let price_cents: i32 = 1999;  // R$19,99 como centavos inteiros
```

**"Estou passando dados para código C (FFI)"**
```hemlock
// Corresponder tipos C exatamente
let c_int: i32 = 100;      // C 'int'
let c_long: i64 = 100;     // C 'long' (sistemas 64-bit)
let c_char: u8 = 65;       // C 'char'
let c_double: f64 = 3.14;  // C 'double'
```

### O que Acontece Quando Tipos se Misturam?

Quando você combina tipos diferentes, Hemlock promove para o tipo "maior":

```hemlock
let a: i32 = 10;
let b: f64 = 2.5;
let result = a + b;  // result é f64 (12.5)
// O inteiro se tornou decimal automaticamente
```

**Regra geral:** Ponto flutuante sempre "vence" - qualquer inteiro misturado com ponto flutuante resulta em ponto flutuante.

### Erros de Tipo

Se você tentar usar o tipo errado, Hemlock informará em tempo de execução:

```hemlock
let age: i32 = "thirty";  // Erro: incompatibilidade de tipo - esperava i32, recebeu string
```

Para converter tipos, use construtores de tipo:

```hemlock
let text = "42";
let number = i32(text);   // Analisa string para inteiro: 42
let back = text + "";     // Já é string
```

---

## Filosofia de Design

- **Dinâmico por padrão** - Todo valor tem uma tag de tipo em tempo de execução
- **Tipos opcionais** - Anotações de tipo opcionais forçam verificações em tempo de execução
- **Conversão explícita** - Conversões implícitas seguem regras de promoção claras
- **Honestidade de tipo** - `typeof()` sempre diz a verdade

## Tipos Primitivos

### Tipos Inteiros

**Inteiros com sinal:**
```hemlock
let tiny: i8 = 127;              // 8 bits (-128 a 127)
let small: i16 = 32767;          // 16 bits (-32768 a 32767)
let normal: i32 = 2147483647;    // 32 bits (padrão)
let large: i64 = 9223372036854775807;  // 64 bits
```

**Inteiros sem sinal:**
```hemlock
let byte: u8 = 255;              // 8 bits (0 a 255)
let word: u16 = 65535;           // 16 bits (0 a 65535)
let dword: u32 = 4294967295;     // 32 bits (0 a 4294967295)
let qword: u64 = 18446744073709551615;  // 64 bits
```

**Aliases de tipo:**
```hemlock
let i: integer = 42;   // Alias para i32
let b: byte = 255;     // Alias para u8
```

### Tipos de Ponto Flutuante

```hemlock
let f: f32 = 3.14159;        // Ponto flutuante 32 bits
let d: f64 = 2.718281828;    // Ponto flutuante 64 bits (padrão)
let n: number = 1.618;       // Alias para f64
```

### Tipo Booleano

```hemlock
let flag: bool = true;
let active: bool = false;
```

### Tipo String

```hemlock
let text: string = "Hello, World!";
let empty: string = "";
```

Strings são **mutáveis**, **codificadas em UTF-8** e **alocadas no heap**.

Veja [Strings](strings.md) para detalhes.

### Tipo Rune

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';
let newline: rune = '\n';
let unicode: rune = '\u{1F680}';
```

Runes representam **pontos de código Unicode** (U+0000 a U+10FFFF).

Veja [Runas](runes.md) para detalhes.

### Tipo Null

```hemlock
let nothing = null;
let uninitialized: string = null;
```

`null` é um tipo distinto com um único valor.

## Tipos Compostos

### Tipo Array

```hemlock
let numbers: array = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];  // Tipos mistos permitidos
let empty: array = [];
```

Veja [Arrays](arrays.md) para detalhes.

### Tipo Object

```hemlock
let obj: object = { x: 10, y: 20 };
let person = { name: "Alice", age: 30 };
```

Veja [Objetos](objects.md) para detalhes.

### Tipos de Ponteiro

**Ponteiros brutos:**
```hemlock
let p: ptr = alloc(64);
// Sem verificação de limites, gerenciamento de ciclo de vida manual
free(p);
```

**Buffers seguros:**
```hemlock
let buf: buffer = buffer(64);
// Com verificação de limites, rastreia comprimento e capacidade
free(buf);
```

Veja [Gerenciamento de Memória](memory.md) para detalhes.

## Tipos Enum

Enums definem um conjunto de constantes nomeadas:

### Enum Básico

```hemlock
enum Color {
    RED,
    GREEN,
    BLUE
}

let c = Color.RED;
print(c);              // 0
print(typeof(c));      // "Color"

// Comparação
if (c == Color.RED) {
    print("It's red!");
}

// Usando switch com enum
switch (c) {
    case Color.RED:
        print("Stop");
        break;
    case Color.GREEN:
        print("Go");
        break;
    case Color.BLUE:
        print("Blue?");
        break;
}
```

### Enum com Valores

Enums podem ter valores inteiros explícitos:

```hemlock
enum Status {
    OK = 0,
    ERROR = 1,
    PENDING = 2
}

print(Status.OK);      // 0
print(Status.ERROR);   // 1

enum HttpCode {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
}

let code = HttpCode.NOT_FOUND;
print(code);           // 404
```

### Valores Auto-incrementados

Sem valores explícitos, enums auto-incrementam a partir de 0:

```hemlock
enum Priority {
    LOW,       // 0
    MEDIUM,    // 1
    HIGH,      // 2
    CRITICAL   // 3
}

// Pode misturar valores explícitos e automáticos
enum Level {
    DEBUG = 10,
    INFO,      // 11
    WARN,      // 12
    ERROR = 50,
    FATAL      // 51
}
```

### Padrões de Uso de Enum

```hemlock
// Como parâmetro de função
fn set_priority(p: Priority) {
    if (p == Priority.CRITICAL) {
        print("Urgent!");
    }
}

set_priority(Priority.HIGH);

// Em objetos
define Task {
    name: string,
    priority: Priority
}

let task: Task = {
    name: "Fix bug",
    priority: Priority.HIGH
};
```

## Tipos Especiais

### Tipo File

```hemlock
let f: file = open("data.txt", "r");
f.close();
```

Representa um handle de arquivo aberto.

### Tipo Task

```hemlock
async fn compute(): i32 { return 42; }
let task = spawn(compute);
let result: i32 = join(task);
```

Representa um handle de tarefa assíncrona.

### Tipo Channel

```hemlock
let ch: channel = channel(10);
ch.send(42);
let value = ch.recv();
```

Representa um canal de comunicação entre tarefas.

### Tipo Void

```hemlock
extern fn exit(code: i32): void;
```

Usado para funções que não retornam valores (apenas FFI).

## Inferência de Tipos

### Inferência de Literais Inteiros

Hemlock infere o tipo inteiro baseado na faixa de valores:

```hemlock
let a = 42;              // i32 (cabe em 32 bits)
let b = 5000000000;      // i64 (> máx i32)
let c = 128;             // i32
let d: u8 = 128;         // u8 (anotação explícita)
```

**Regras:**
- Valores na faixa i32 (-2147483648 a 2147483647): inferido como `i32`
- Valores fora da faixa i32 mas dentro da faixa i64: inferido como `i64`
- Outros tipos (i8, i16, u8, u16, u32, u64) usam anotação explícita

### Inferência de Literais de Ponto Flutuante

```hemlock
let x = 3.14;        // f64 (padrão)
let y: f32 = 3.14;   // f32 (explícito)
```

### Notação Científica

Hemlock suporta notação científica para literais numéricos:

```hemlock
let a = 1e10;        // 10000000000.0 (f64)
let b = 1e-12;       // 0.000000000001 (f64)
let c = 3.14e2;      // 314.0 (f64)
let d = 2.5e-3;      // 0.0025 (f64)
let e = 1E10;        // Não diferencia maiúsculas/minúsculas
let f = 1e+5;        // Expoente positivo explícito
```

**Nota:** Qualquer literal usando notação científica é sempre inferido como `f64`.

### Outras Inferências de Tipo

```hemlock
let s = "hello";     // string
let ch = 'A';        // rune
let flag = true;     // bool
let arr = [1, 2, 3]; // array
let obj = { x: 10 }; // object
let nothing = null;  // null
```

## Anotações de Tipo

### Anotações de Variável

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let name: string = "Alice";
```

### Anotações de Parâmetros de Função

```hemlock
fn greet(name: string, age: i32) {
    print("Hello, " + name + "!");
}
```

### Anotações de Tipo de Retorno de Função

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Anotações de Tipo de Objeto (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
}

let p: Person = { name: "Bob", age: 25 };
```

## Verificação de Tipos

### Verificação de Tipo em Tempo de Execução

Anotações de tipo são verificadas em **tempo de execução**, não em tempo de compilação:

```hemlock
let x: i32 = 42;     // OK
let y: i32 = 3.14;   // Erro em tempo de execução: incompatibilidade de tipo

fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 3);           // OK
add(5, "hello");     // Erro em tempo de execução: incompatibilidade de tipo
```

### Consulta de Tipo

Use `typeof()` para verificar o tipo de um valor:

```hemlock
print(typeof(42));         // "i32"
print(typeof(3.14));       // "f64"
print(typeof("hello"));    // "string"
print(typeof(true));       // "bool"
print(typeof(null));       // "null"
print(typeof([1, 2, 3]));  // "array"
print(typeof({ x: 10 }));  // "object"
```

## Conversão de Tipos

### Promoção Implícita de Tipos

Quando tipos são misturados em operações, Hemlock promove para o tipo "maior":

**Hierarquia de promoção (do menor para o maior):**
```
i8 → i16 → i32 → u32 → i64 → u64 → f32 → f64
      ↑     ↑     ↑
     u8    u16
```

**Ponto flutuante sempre vence:**
```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result é f64 (13.5)
```

**Tamanho maior vence:**
```hemlock
let a: i32 = 100;
let b: i64 = 200;
let sum = a + b;     // sum é i64 (300)
```

**Preservação de precisão:** Quando inteiros de 64 bits são misturados com f32, Hemlock promove para f64 para evitar perda de precisão (f32 tem apenas 24 bits de mantissa, insuficiente para representar i64/u64):
```hemlock
let big: i64 = 9007199254740993;
let small: f32 = 1.0;
let result = big + small;  // result é f64, não f32!
```

**Exemplos:**
```hemlock
u8 + i32  → i32
i32 + i64 → i64
u32 + u64 → u64
i32 + f32 → f32    // f32 é suficiente para representar i32
i64 + f32 → f64    // Precisa de f64 para manter precisão de i64
i64 + f64 → f64
i8 + f64  → f64
```

### Conversão Explícita de Tipos

**Conversão inteiro/ponto flutuante:**
```hemlock
let i: i32 = 42;
let f: f64 = i;      // i32 → f64 (42.0)

let x: f64 = 3.14;
let n: i32 = x;      // f64 → i32 (3, truncado)
```

**Conversão inteiro/rune:**
```hemlock
let code: i32 = 65;
let ch: rune = code;  // i32 → rune ('A')

let r: rune = 'Z';
let value: i32 = r;   // rune → i32 (90)
```

**Rune para string:**
```hemlock
let ch: rune = '🚀';
let s: string = ch;   // rune → string ("🚀")
```

**u8 para rune:**
```hemlock
let b: u8 = 65;
let r: rune = b;      // u8 → rune ('A')
```

### Construtores de Tipo

Nomes de tipo podem ser usados como funções para converter ou analisar valores:

**Analisar strings para números:**
```hemlock
let n = i32("42");       // Analisa string para i32: 42
let f = f64("3.14159");  // Analisa string para f64: 3.14159
let b = bool("true");    // Analisa string para bool: true

// Suporta todos os tipos numéricos
let a = i8("-128");      // Analisa para i8
let c = u8("255");       // Analisa para u8
let d = i16("1000");     // Analisa para i16
let e = u16("50000");    // Analisa para u16
let g = i64("9000000000000"); // Analisa para i64
let h = u64("18000000000000"); // Analisa para u64
let j = f32("1.5");      // Analisa para f32
```

**Hexadecimal e negativos:**
```hemlock
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42
let bin = i32("0b1010"); // 10 (binário)
```

**Aliases de tipo também funcionam:**
```hemlock
let x = integer("100");  // Equivalente a i32("100")
let y = number("1.5");   // Equivalente a f64("1.5")
let z = byte("200");     // Equivalente a u8("200")
```

**Conversão entre tipos numéricos:**
```hemlock
let big = i64(42);           // i32 para i64
let truncated = i32(3.99);   // f64 para i32 (trunca para 3)
let promoted = f64(100);     // i32 para f64 (100.0)
let narrowed = i8(127);      // i32 para i8
```

**Anotações de tipo executam coerção numérica (mas não analisam strings):**
```hemlock
let f: f64 = 100;        // i32 para f64 via anotação (OK)
let s: string = 'A';     // Rune para string via anotação (OK)
let code: i32 = 'A';     // Rune para i32 via anotação (obtém codepoint, OK)

// Análise de string requer construtor de tipo explícito:
let n = i32("42");       // Use construtor de tipo para analisar string
// let x: i32 = "42";    // Erro - anotação de tipo não analisa strings
```

**Tratamento de erros:**
```hemlock
// Ao usar construtores de tipo, strings inválidas lançam erro
let bad = i32("hello");  // Erro em tempo de execução: não é possível analisar "hello" como i32
let overflow = u8("256"); // Erro em tempo de execução: 256 está fora da faixa de u8
```

**Análise de booleano:**
```hemlock
let t = bool("true");    // true
let f = bool("false");   // false
let bad = bool("yes");   // Erro em tempo de execução: deve ser "true" ou "false"
```

## Verificação de Faixa

Anotações de tipo forçam verificação de faixa na atribuição:

```hemlock
let x: u8 = 255;    // OK
let y: u8 = 256;    // Erro: fora da faixa de u8

let a: i8 = 127;    // OK
let b: i8 = 128;    // Erro: fora da faixa de i8

let c: i64 = 2147483647;   // OK
let d: u64 = 4294967295;   // OK
let e: u64 = -1;           // Erro: u64 não pode ser negativo
```

## Exemplos de Promoção de Tipos

### Misturando Tipos Inteiros

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let sum = a + b;     // i32 (30)

let c: u8 = 100;
let d: u32 = 200;
let total = c + d;   // u32 (300)
```

### Inteiro + Ponto Flutuante

```hemlock
let i: i32 = 5;
let f: f32 = 2.5;
let result = i * f;  // f32 (12.5)
```

### Expressões Complexas

```hemlock
let a: i8 = 10;
let b: i32 = 20;
let c: f64 = 3.0;

let result = a + b * c;  // f64 (70.0)
// Cálculo: b * c → f64(60.0)
//          a + f64(60.0) → f64(70.0)
```

## Duck Typing (Objetos)

Objetos usam **tipagem estrutural** (duck typing):

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: tem todos os campos obrigatórios
let p1: Person = { name: "Alice", age: 30 };

// OK: campos extras permitidos
let p2: Person = { name: "Bob", age: 25, city: "NYC" };

// Erro: falta campo 'age'
let p3: Person = { name: "Carol" };

// Erro: tipo errado para 'age'
let p4: Person = { name: "Dave", age: "thirty" };
```

**Verificação de tipo ocorre na atribuição:**
- Verifica se todos os campos obrigatórios existem
- Verifica se tipos dos campos correspondem
- Permite e preserva campos extras
- Define o nome do tipo do objeto para `typeof()`

## Campos Opcionais

```hemlock
define Config {
    host: string,
    port: i32,
    debug?: false,     // Campo opcional com valor padrão
    timeout?: i32,     // Opcional, padrão null
}

let cfg1: Config = { host: "localhost", port: 8080 };
print(cfg1.debug);    // false (padrão)
print(cfg1.timeout);  // null

let cfg2: Config = { host: "0.0.0.0", port: 80, debug: true };
print(cfg2.debug);    // true (sobrescrito)
```

## Aliases de Tipo

Hemlock suporta aliases de tipo personalizados usando a palavra-chave `type`:

### Aliases de Tipo Básicos

```hemlock
// Aliases de tipo simples
type Integer = i32;
type Text = string;

// Usando aliases
let x: Integer = 42;
let msg: Text = "hello";
```

### Aliases de Tipo de Função

```hemlock
// Aliases de tipo de função
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Usando aliases de tipo de função
let cb: Callback = fn(n) { print(n); };
let isEven: Predicate = fn(n) { return n % 2 == 0; };
```

### Aliases de Tipo Composto

```hemlock
// Combinar múltiplos defines em um tipo
define HasName { name: string }
define HasAge { age: i32 }

type Person = HasName & HasAge;

let p: Person = { name: "Alice", age: 30 };
```

### Aliases de Tipo Genérico

```hemlock
// Aliases de tipo genérico
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Usando aliases genéricos
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
```

**Nota:** Aliases de tipo são transparentes - `typeof()` retorna o nome do tipo subjacente, não o alias.

## Limitações do Sistema de Tipos

Limitações atuais:

- **Sem genéricos para funções** - Parâmetros de tipo de função ainda não suportados
- **Sem tipos união** - Não é possível expressar "A ou B"
- **Sem tipos anuláveis** - Todos os tipos podem ser null (use sufixo `?` para nullable explícito)

**Nota:** O compilador (`hemlockc`) fornece verificação de tipos em tempo de compilação. O interpretador apenas realiza verificação de tipos em tempo de execução. Veja a [documentação do compilador](../design/implementation.md) para detalhes.

## Melhores Práticas

### Quando Usar Anotações de Tipo

**Deve usar anotações quando:**
- O tipo preciso importa (ex: `u8` para valores de byte)
- Documentar interfaces de função
- Forçar restrições (ex: verificação de faixa)

```hemlock
fn hash(data: buffer, length: u32): u64 {
    // implementação
}
```

**Não precisa usar anotações quando:**
- O tipo é óbvio pelo literal
- Detalhes de implementação interna
- Formalidade desnecessária

```hemlock
// Desnecessário
let x: i32 = 42;

// Melhor
let x = 42;
```

### Padrões de Segurança de Tipos

**Verificar antes de usar:**
```hemlock
if (typeof(value) == "i32") {
    // Pode usar com segurança como i32
}
```

**Validar argumentos de função:**
```hemlock
fn divide(a, b) {
    if (typeof(a) != "i32" || typeof(b) != "i32") {
        throw "arguments must be integers";
    }
    if (b == 0) {
        throw "division by zero";
    }
    return a / b;
}
```

**Usar duck typing para flexibilidade:**
```hemlock
define Printable {
    toString: fn,
}

fn print_item(item: Printable) {
    print(item.toString());
}
```

## Próximos Passos

- [Strings](strings.md) - Tipo string UTF-8 e operações
- [Runas](runes.md) - Tipo de ponto de código Unicode
- [Arrays](arrays.md) - Tipo de array dinâmico
- [Objetos](objects.md) - Literais de objeto e duck typing
- [Memória](memory.md) - Tipos ponteiro e buffer
