# Visão Geral da Sintaxe

Este documento apresenta as regras básicas de sintaxe e estrutura dos programas Hemlock.

## Regras Básicas de Sintaxe

### Ponto e Vírgula é Obrigatório

Diferente do JavaScript ou Python, o ponto e vírgula **deve** ser usado no final das instruções:

```hemlock
let x = 42;
let y = 10;
print(x + y);
```

**O código a seguir causará erro:**
```hemlock
let x = 42  // Erro: falta ponto e vírgula
let y = 10  // Erro: falta ponto e vírgula
```

### Chaves são Obrigatórias

Todos os blocos de fluxo de controle devem usar chaves, mesmo para instruções únicas:

```hemlock
// Correto
if (x > 0) {
    print("positive");
}

// Erro: faltam chaves
if (x > 0)
    print("positive");
```

### Comentários

```hemlock
// Este é um comentário de linha única

/*
   Este é um
   comentário de múltiplas linhas
*/

let x = 42;  // Comentário inline
```

## Variáveis

### Declaração

Use `let` para declarar variáveis:

```hemlock
let count = 0;
let name = "Alice";
let pi = 3.14159;
```

### Anotações de Tipo (Opcionais)

```hemlock
let age: i32 = 30;
let ratio: f64 = 1.618;
let flag: bool = true;
let text: string = "hello";
```

### Constantes

Use `const` para declarar valores imutáveis:

```hemlock
const MAX_SIZE: i32 = 1000;
const PI: f64 = 3.14159;
```

Tentar reatribuir uma constante causará um erro em tempo de execução: "Cannot assign to const variable".

## Expressões

### Operadores Aritméticos

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13 - adição
print(a - b);   // 7  - subtração
print(a * b);   // 30 - multiplicação
print(a / b);   // 3  - divisão (inteira)
```

### Operadores de Comparação

```hemlock
print(a == b);  // false - igual
print(a != b);  // true  - diferente
print(a > b);   // true  - maior que
print(a < b);   // false - menor que
print(a >= b);  // true  - maior ou igual
print(a <= b);  // false - menor ou igual
```

### Operadores Lógicos

```hemlock
let x = true;
let y = false;

print(x && y);  // false - e
print(x || y);  // true  - ou
print(!x);      // false - não
```

### Operadores Bit a Bit

```hemlock
let a = 12;  // 1100
let b = 10;  // 1010

print(a & b);   // 8  - e bit a bit
print(a | b);   // 14 - ou bit a bit
print(a ^ b);   // 6  - ou exclusivo bit a bit
print(a << 2);  // 48 - deslocamento à esquerda
print(a >> 1);  // 6  - deslocamento à direita
print(~a);      // -13 - inversão bit a bit
```

### Precedência de Operadores

Da maior para a menor:

1. `()` - agrupamento
2. `!`, `~`, `-` (unário) - operadores unários
3. `*`, `/` - multiplicação, divisão
4. `+`, `-` - adição, subtração
5. `<<`, `>>` - deslocamento de bits
6. `<`, `<=`, `>`, `>=` - comparação
7. `==`, `!=` - igualdade
8. `&` - e bit a bit
9. `^` - ou exclusivo bit a bit
10. `|` - ou bit a bit
11. `&&` - e lógico
12. `||` - ou lógico

**Exemplo:**
```hemlock
let x = 2 + 3 * 4;      // 14 (não 20)
let y = (2 + 3) * 4;    // 20
let z = 5 << 2 + 1;     // 40 (5 << 3)
```

## Fluxo de Controle

### Instrução If

```hemlock
if (condition) {
    // corpo
}

if (condition) {
    // bloco then
} else {
    // bloco else
}

if (condition1) {
    // bloco 1
} else if (condition2) {
    // bloco 2
} else {
    // bloco padrão
}
```

### Laço While

```hemlock
while (condition) {
    // corpo
}
```

**Exemplo:**
```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Laço For

**For estilo C:**
```hemlock
for (initializer; condition; increment) {
    // corpo
}
```

**Exemplo:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**For-in (arrays):**
```hemlock
for (let item in array) {
    // corpo
}
```

**Exemplo:**
```hemlock
let items = [10, 20, 30];
for (let x in items) {
    print(x);
}
```

### Instrução Switch

```hemlock
switch (expression) {
    case value1:
        // corpo
        break;
    case value2:
        // corpo
        break;
    default:
        // corpo padrão
        break;
}
```

**Exemplo:**
```hemlock
let day = 3;
switch (day) {
    case 1:
        print("Monday");
        break;
    case 2:
        print("Tuesday");
        break;
    case 3:
        print("Wednesday");
        break;
    default:
        print("Other");
        break;
}
```

### Break e Continue

```hemlock
// Break: sai do laço
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        break;
    }
    print(i);
}

// Continue: pula para a próxima iteração
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;
    }
    print(i);
}
```

## Funções

### Funções Nomeadas

```hemlock
fn function_name(param1: type1, param2: type2): return_type {
    // corpo
    return value;
}
```

**Exemplo:**
```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}
```

### Funções Anônimas

```hemlock
let func = fn(params) {
    // corpo
};
```

**Exemplo:**
```hemlock
let multiply = fn(x, y) {
    return x * y;
};
```

### Anotações de Tipo (Opcionais)

```hemlock
// Sem anotações (inferência de tipo)
fn greet(name) {
    return "Hello, " + name;
}

// Com anotações (verificação em tempo de execução)
fn divide(a: i32, b: i32): f64 {
    return a / b;
}
```

## Objetos

### Literais de Objeto

```hemlock
let obj = {
    field1: value1,
    field2: value2,
};
```

**Exemplo:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    active: true,
};
```

### Métodos

```hemlock
let obj = {
    method: fn() {
        self.field = value;
    },
};
```

**Exemplo:**
```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
};
```

### Definições de Tipo

```hemlock
define TypeName {
    field1: type1,
    field2: type2,
    optional_field?: default_value,
}
```

**Exemplo:**
```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,
}
```

## Arrays

### Literais de Array

```hemlock
let arr = [element1, element2, element3];
```

**Exemplo:**
```hemlock
let numbers = [1, 2, 3, 4, 5];
let mixed = [1, "two", true, null];
let empty = [];
```

### Indexação de Array

```hemlock
let arr = [10, 20, 30];
print(arr[0]);   // 10
arr[1] = 99;     // modificar elemento
```

## Tratamento de Erros

### Try/Catch

```hemlock
try {
    // código que pode falhar
} catch (e) {
    // tratar erro
}
```

### Try/Finally

```hemlock
try {
    // código que pode falhar
} finally {
    // sempre executa
}
```

### Try/Catch/Finally

```hemlock
try {
    // código que pode falhar
} catch (e) {
    // tratar erro
} finally {
    // limpeza
}
```

### Throw

```hemlock
throw expression;
```

**Exemplo:**
```hemlock
if (x < 0) {
    throw "x must be positive";
}
```

### Panic

```hemlock
panic(message);
```

**Exemplo:**
```hemlock
panic("unrecoverable error");
```

## Módulos (Experimental)

### Instruções de Exportação

```hemlock
export fn function_name() { }
export const CONSTANT = value;
export let variable = value;
export { name1, name2 };
```

### Instruções de Importação

```hemlock
import { name1, name2 } from "./module.hml";
import * as namespace from "./module.hml";
import { name as alias } from "./module.hml";
```

## Assíncrono (Experimental)

### Funções Assíncronas

```hemlock
async fn function_name(params): return_type {
    // corpo
}
```

### Spawn/Join

```hemlock
let task = spawn(async_function, arg1, arg2);
let result = join(task);
```

### Canais

```hemlock
let ch = channel(capacity);
ch.send(value);
let value = ch.recv();
ch.close();
```

## FFI (Interface de Função Estrangeira)

### Importar Bibliotecas Compartilhadas

```hemlock
import "library_name.so";
```

### Declarar Funções Externas

```hemlock
extern fn function_name(param: type): return_type;
```

**Exemplo:**
```hemlock
import "libc.so.6";
extern fn strlen(s: string): i32;
```

## Literais

### Literais Inteiros

```hemlock
let decimal = 42;
let negative = -100;
let large = 5000000000;  // i64 automático

// Hexadecimal (prefixo 0x)
let hex = 0xDEADBEEF;
let hex2 = 0xFF;

// Binário (prefixo 0b)
let bin = 0b1010;
let bin2 = 0b11110000;

// Octal (prefixo 0o)
let oct = 0o777;
let oct2 = 0O123;

// Separadores numéricos para legibilidade
let million = 1_000_000;
let hex_sep = 0xFF_FF_FF;
let bin_sep = 0b1111_0000_1010_0101;
let oct_sep = 0o77_77;
```

### Literais de Ponto Flutuante

```hemlock
let f = 3.14;
let e = 2.71828;
let sci = 1.5e-10;       // notação científica
let sci2 = 2.5E+3;       // E maiúsculo também funciona
let no_lead = .5;        // sem zero inicial (0.5)
let sep = 3.14_159_265;  // separadores numéricos
```

### Literais de String

```hemlock
let s = "hello";
let escaped = "line1\nline2\ttabbed";
let quote = "She said \"hello\"";

// Sequências de escape hexadecimal
let hex_esc = "\x48\x65\x6c\x6c\x6f";  // "Hello"

// Sequências de escape Unicode
let emoji = "\u{1F600}";               // 😀
let heart = "\u{2764}";                // ❤
let mixed = "Hello \u{1F30D}!";        // Hello 🌍!
```

**Sequências de Escape:**
- `\n` - nova linha
- `\t` - tabulação
- `\r` - retorno de carro
- `\\` - barra invertida
- `\"` - aspas duplas
- `\'` - aspas simples
- `\0` - caractere nulo
- `\xNN` - escape hexadecimal (2 dígitos)
- `\u{XXXX}` - escape Unicode (1-6 dígitos)

### Literais Rune

```hemlock
let ch = 'A';
let emoji = '🚀';
let escaped = '\n';
let unicode = '\u{1F680}';
let hex_rune = '\x41';      // 'A'
```

### Literais Booleanos

```hemlock
let t = true;
let f = false;
```

### Literal Null

```hemlock
let nothing = null;
```

## Regras de Escopo

### Escopo de Bloco

O escopo de uma variável é o bloco mais próximo que a contém:

```hemlock
let x = 1;  // escopo externo

if (true) {
    let x = 2;  // escopo interno (oculta o externo)
    print(x);   // 2
}

print(x);  // 1
```

### Escopo de Função

Funções criam seu próprio escopo:

```hemlock
let global = "global";

fn foo() {
    let local = "local";
    print(global);  // pode ler escopo externo
}

foo();
// print(local);  // Erro: 'local' não está definido aqui
```

### Escopo de Closure

Closures capturam variáveis do escopo envolvente:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;  // captura 'count'
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
```

## Espaços em Branco e Formatação

### Indentação

Hemlock não impõe indentação específica, mas 4 espaços são recomendados:

```hemlock
fn example() {
    if (true) {
        print("indented");
    }
}
```

### Quebras de Linha

Instruções podem abranger múltiplas linhas:

```hemlock
let result =
    very_long_function_name(
        arg1,
        arg2,
        arg3
    );
```

## Instrução Loop

A palavra-chave `loop` fornece sintaxe mais clara para laços infinitos:

```hemlock
loop {
    // ... executar trabalho
    if (done) {
        break;
    }
}
```

Isso é equivalente a `while (true)`, mas a intenção é mais clara.

## Palavras-chave Reservadas

As seguintes palavras-chave são reservadas em Hemlock:

```
let, const, fn, if, else, while, for, in, loop, break, continue,
return, true, false, null, typeof, import, export, from,
try, catch, finally, throw, panic, async, await, spawn, join,
detach, channel, define, switch, case, default, extern, self,
type, defer, enum, ref, buffer, Self
```

## Próximos Passos

- [Sistema de Tipos](types.md) - Aprenda sobre o sistema de tipos do Hemlock
- [Fluxo de Controle](control-flow.md) - Aprofunde-se nas estruturas de controle
- [Funções](functions.md) - Domine funções e closures
- [Gerenciamento de Memória](memory.md) - Entenda ponteiros e buffers
