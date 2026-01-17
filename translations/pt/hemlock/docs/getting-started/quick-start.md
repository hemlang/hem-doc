# Inicio Rapido

Comece a usar o Hemlock em poucos minutos!

## Seu Primeiro Programa

Crie um arquivo chamado `hello.hml`:

```hemlock
print("Hello, Hemlock!");
```

Execute com o interpretador:

```bash
./hemlock hello.hml
```

Ou compile para um executavel nativo:

```bash
./hemlockc hello.hml -o hello
./hello
```

Saida:
```
Hello, Hemlock!
```

### Interpretador vs Compilador

O Hemlock oferece duas maneiras de executar programas:

| Ferramenta | Caso de Uso | Verificacao de Tipos |
|------------|-------------|----------------------|
| `hemlock` | Scripts rapidos, REPL, desenvolvimento | Apenas em tempo de execucao |
| `hemlockc` | Binarios de producao, melhor desempenho | Em tempo de compilacao (padrao) |

O compilador (`hemlockc`) verifica os tipos do seu codigo antes de gerar o executavel, capturando erros antecipadamente.

## Sintaxe Basica

### Variaveis

```hemlock
// Use 'let' para declarar variaveis
let x = 42;
let name = "Alice";
let pi = 3.14159;

// Anotacoes de tipo sao opcionais
let count: i32 = 100;
let ratio: f64 = 0.618;
```

**Importante**: Ponto e virgula e **obrigatorio** no Hemlock!

### Tipos

O Hemlock possui um sistema de tipos rico:

```hemlock
// Inteiros
let small: i8 = 127;          // 8 bits com sinal
let byte: u8 = 255;           // 8 bits sem sinal
let num: i32 = 2147483647;    // 32 bits com sinal (padrao)
let big: i64 = 9223372036854775807;  // 64 bits com sinal

// Ponto flutuante
let f: f32 = 3.14;            // 32 bits ponto flutuante
let d: f64 = 2.71828;         // 64 bits ponto flutuante (padrao)

// Strings e caracteres
let text: string = "Hello";   // String UTF-8
let emoji: rune = '🚀';       // Ponto de codigo Unicode

// Booleano e nulo
let flag: bool = true;
let empty = null;
```

### Fluxo de Controle

```hemlock
// Instrucao if
if (x > 0) {
    print("Positivo");
} else if (x < 0) {
    print("Negativo");
} else {
    print("Zero");
}

// Laco while
let i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// Laco for
for (let j = 0; j < 10; j = j + 1) {
    print(j);
}
```

### Funcoes

```hemlock
// Funcao nomeada
fn add(a: i32, b: i32): i32 {
    return a + b;
}

let result = add(5, 3);  // 8

// Funcao anonima
let multiply = fn(x, y) {
    return x * y;
};

print(multiply(4, 7));  // 28
```

## Operacoes com Strings

Strings no Hemlock sao **mutaveis** e codificadas em **UTF-8**:

```hemlock
let s = "hello";
s[0] = 'H';              // Agora e "Hello"
print(s);

// Metodos de string
let upper = s.to_upper();     // "HELLO"
let words = "a,b,c".split(","); // ["a", "b", "c"]
let sub = s.substr(1, 3);     // "ell"

// Concatenacao
let greeting = "Hello" + ", " + "World!";
print(greeting);  // "Hello, World!"
```

## Arrays

Arrays dinamicos com suporte a tipos mistos:

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Metodos de array
numbers.push(6);        // [1, 2, 3, 4, 5, 6]
let last = numbers.pop();  // 6
let slice = numbers.slice(1, 4);  // [2, 3, 4]

// Tipos mistos permitidos
let mixed = [1, "two", true, null];
```

## Objetos

Objetos no estilo JavaScript:

```hemlock
// Literal de objeto
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
person.age = 31;     // Modificar campo

// Metodos com 'self'
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Gerenciamento de Memoria

O Hemlock usa **gerenciamento de memoria manual**:

```hemlock
// Buffer seguro (recomendado)
let buf = buffer(64);   // Alocar 64 bytes
buf[0] = 65;            // Definir primeiro byte como 'A'
print(buf[0]);          // 65
free(buf);              // Liberar memoria

// Ponteiros brutos (avancado)
let ptr = alloc(100);
memset(ptr, 0, 100);    // Preencher com zeros
free(ptr);
```

**Importante**: Voce deve usar `free()` na memoria que voce alocou com `alloc()`!

## Tratamento de Erros

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "Erro de divisao por zero";
    }
    return a / b;
}

try {
    let result = divide(10, 0);
    print(result);
} catch (e) {
    print("Erro: " + e);
} finally {
    print("Concluido");
}
```

## Argumentos de Linha de Comando

Acesse os argumentos do programa atraves do array `args`:

```hemlock
// script.hml
print("Script:", args[0]);
print(`Numero de argumentos: ${args.length - 1}`);

let i = 1;
while (i < args.length) {
    print(`  Argumento ${i}: ${args[i]}`);
    i = i + 1;
}
```

Executar:
```bash
./hemlock script.hml hello world
```

Saida:
```
Script: script.hml
Numero de argumentos: 2
  Argumento 1: hello
  Argumento 2: world
```

## E/S de Arquivos

```hemlock
// Escrever em arquivo
let f = open("data.txt", "w");
f.write("Hello, File!");
f.close();

// Ler arquivo
let f2 = open("data.txt", "r");
let content = f2.read();
print(content);  // "Hello, File!"
f2.close();
```

## O Que Aprender a Seguir?

Agora que voce conhece o basico, pode explorar mais:

- [Tutorial](tutorial.md) - Guia completo passo a passo
- [Guia da Linguagem](../language-guide/syntax.md) - Aprofunde-se em todos os recursos
- [Exemplos](../../examples/) - Programas de exemplo do mundo real
- [Referencia da API](../reference/builtins.md) - Documentacao completa da API

## Armadilhas Comuns

### Esquecer o Ponto e Virgula

```hemlock
// ❌ Errado: falta ponto e virgula
let x = 42
let y = 10

// ✅ Correto
let x = 42;
let y = 10;
```

### Esquecer de Liberar Memoria

```hemlock
// ❌ Vazamento de memoria
let buf = buffer(100);
// ... usar buf ...
// Esqueceu de chamar free(buf)!

// ✅ Correto
let buf = buffer(100);
// ... usar buf ...
free(buf);
```

### Chaves Sao Obrigatorias

```hemlock
// ❌ Errado: faltam chaves
if (x > 0)
    print("Positivo");

// ✅ Correto
if (x > 0) {
    print("Positivo");
}
```

## Obtendo Ajuda

- Leia a [documentacao completa](../README.md)
- Confira o [diretorio de exemplos](../../examples/)
- Veja os [arquivos de teste](../../tests/) para padroes de uso
- Reporte problemas no GitHub
