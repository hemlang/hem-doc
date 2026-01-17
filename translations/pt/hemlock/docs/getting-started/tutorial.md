# Tutorial do Hemlock

Um guia completo passo a passo para aprender Hemlock.

## Sumario

1. [Hello World](#hello-world)
2. [Variaveis e Tipos](#variaveis-e-tipos)
3. [Aritmetica e Operacoes](#aritmetica-e-operacoes)
4. [Fluxo de Controle](#fluxo-de-controle)
5. [Funcoes](#funcoes)
6. [Strings e Caracteres](#strings-e-caracteres)
7. [Arrays](#arrays)
8. [Objetos](#objetos)
9. [Gerenciamento de Memoria](#gerenciamento-de-memoria)
10. [Tratamento de Erros](#tratamento-de-erros)
11. [E/S de Arquivos](#es-de-arquivos)
12. [Exemplo Completo](#exemplo-completo)

## Hello World

Vamos comecar com o tradicional primeiro programa:

```hemlock
print("Hello, World!");
```

Salve como `hello.hml` e execute:

```bash
./hemlock hello.hml
```

**Pontos-chave:**
- `print()` e uma funcao embutida que imprime na saida padrao
- Strings sao delimitadas por aspas duplas
- Ponto e virgula e **obrigatorio**

## Variaveis e Tipos

### Declarando Variaveis

```hemlock
// Declaracao basica de variaveis
let x = 42;
let name = "Alice";
let pi = 3.14159;

print(x);      // 42
print(name);   // Alice
print(pi);     // 3.14159
```

### Anotacoes de Tipo

Embora os tipos sejam inferidos por padrao, voce pode especifica-los explicitamente:

```hemlock
let age: i32 = 30;
let height: f64 = 5.9;
let initial: rune = 'A';
let active: bool = true;
```

### Inferencia de Tipos

O Hemlock infere os tipos com base nos valores:

```hemlock
let small = 42;              // i32 (cabe em 32 bits)
let large = 5000000000;      // i64 (muito grande para i32)
let decimal = 3.14;          // f64 (padrao para ponto flutuante)
let text = "hello";          // string
let flag = true;             // bool
```

### Verificacao de Tipos

```hemlock
// Use typeof() para verificar tipos
print(typeof(42));        // "i32"
print(typeof(3.14));      // "f64"
print(typeof("hello"));   // "string"
print(typeof(true));      // "bool"
print(typeof(null));      // "null"
```

## Aritmetica e Operacoes

### Aritmetica Basica

```hemlock
let a = 10;
let b = 3;

print(a + b);   // 13
print(a - b);   // 7
print(a * b);   // 30
print(a / b);   // 3 (divisao inteira)
print(a == b);  // false
print(a > b);   // true
```

### Promocao de Tipos

Ao misturar tipos, o Hemlock promove para o tipo maior/mais preciso:

```hemlock
let x: i32 = 10;
let y: f64 = 3.5;
let result = x + y;  // result e f64 (10.0 + 3.5 = 13.5)

print(result);       // 13.5
print(typeof(result)); // "f64"
```

### Operacoes Bit a Bit

```hemlock
let a = 12;  // Binario 1100
let b = 10;  // Binario 1010

print(a & b);   // 8  (AND)
print(a | b);   // 14 (OR)
print(a ^ b);   // 6  (XOR)
print(a << 1);  // 24 (deslocamento a esquerda)
print(a >> 1);  // 6  (deslocamento a direita)
print(~a);      // -13 (NOT)
```

## Fluxo de Controle

### Instrucao If

```hemlock
let x = 10;

if (x > 0) {
    print("Positivo");
} else if (x < 0) {
    print("Negativo");
} else {
    print("Zero");
}
```

**Nota:** Chaves sao **sempre obrigatorias**, mesmo para instrucoes unicas.

### Laco While

```hemlock
let count = 0;
while (count < 5) {
    print(`Contagem: ${count}`);
    count = count + 1;
}
```

### Laco For

```hemlock
// Laco for estilo C
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// Laco for-in (arrays)
let items = [10, 20, 30, 40];
for (let item in items) {
    print(`Item: ${item}`);
}
```

### Instrucao Switch

```hemlock
let day = 3;

switch (day) {
    case 1:
        print("Segunda-feira");
        break;
    case 2:
        print("Terca-feira");
        break;
    case 3:
        print("Quarta-feira");
        break;
    default:
        print("Outro dia");
        break;
}
```

### Break e Continue

```hemlock
// Break: sai do laco antecipadamente
let i = 0;
while (i < 10) {
    if (i == 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Saida: 0, 1, 2, 3, 4

// Continue: pula para a proxima iteracao
for (let j = 0; j < 5; j = j + 1) {
    if (j == 2) {
        continue;
    }
    print(j);
}
// Saida: 0, 1, 3, 4
```

## Funcoes

### Funcoes Nomeadas

```hemlock
fn greet(name: string): string {
    return "Ola, " + name + "!";
}

let message = greet("Alice");
print(message);  // "Ola, Alice!"
```

### Funcoes Anonimas

```hemlock
let add = fn(a, b) {
    return a + b;
};

print(add(5, 3));  // 8
```

### Recursao

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Closures

Funcoes capturam seu ambiente:

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

### Funcoes de Ordem Superior

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 21);
print(result);  // 42
```

## Strings e Caracteres

### Basico de Strings

Strings sao **mutaveis** e codificadas em **UTF-8**:

```hemlock
let s = "hello";
print(s.length);      // 5 (contagem de caracteres)
print(s.byte_length); // 5 (contagem de bytes)

// Modificacao
s[0] = 'H';
print(s);  // "Hello"
```

### Metodos de String

```hemlock
let text = "  Hello, World!  ";

// Conversao de maiusculas/minusculas
print(text.to_upper());  // "  HELLO, WORLD!  "
print(text.to_lower());  // "  hello, world!  "

// Remover espacos em branco
print(text.trim());      // "Hello, World!"

// Extracao de substring
let hello = text.substr(2, 5);  // "Hello"
let world = text.slice(9, 14);  // "World"

// Busca
let pos = text.find("World");   // 9
let has = text.contains("o");   // true

// Divisao
let parts = "a,b,c".split(","); // ["a", "b", "c"]

// Substituicao
let s = "hello world".replace("world", "there");
print(s);  // "hello there"
```

### Caracteres (Pontos de Codigo Unicode)

```hemlock
let ch: rune = 'A';
let emoji: rune = '🚀';

print(ch);      // 'A'
print(emoji);   // U+1F680

// Concatenacao de caractere + string
let msg = '>' + " Importante";
print(msg);  // "> Importante"

// Conversao entre caracteres e inteiros
let code: i32 = ch;     // 65 (codigo ASCII)
let r: rune = 128640;   // U+1F680 (🚀)
```

## Arrays

### Basico de Arrays

```hemlock
let numbers = [1, 2, 3, 4, 5];
print(numbers[0]);      // 1
print(numbers.length);  // 5

// Modificar elementos
numbers[2] = 99;
print(numbers[2]);  // 99
```

### Metodos de Array

```hemlock
let arr = [10, 20, 30];

// Adicionar/remover no final
arr.push(40);           // [10, 20, 30, 40]
let last = arr.pop();   // 40, arr agora e [10, 20, 30]

// Adicionar/remover no inicio
arr.unshift(5);         // [5, 10, 20, 30]
let first = arr.shift(); // 5, arr agora e [10, 20, 30]

// Inserir/remover em indice
arr.insert(1, 15);      // [10, 15, 20, 30]
let removed = arr.remove(2);  // 20

// Busca
let index = arr.find(15);     // 1
let has = arr.contains(10);   // true

// Fatiamento
let slice = arr.slice(0, 2);  // [10, 15]

// Juntar em string
let text = arr.join(", ");    // "10, 15, 30"
```

### Iteracao

```hemlock
let items = ["maca", "banana", "cereja"];

// Laco for-in
for (let item in items) {
    print(item);
}

// Iteracao manual
let i = 0;
while (i < items.length) {
    print(items[i]);
    i = i + 1;
}
```

## Objetos

### Literais de Objeto

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30

// Adicionar/modificar campos
person.email = "alice@example.com";
person.age = 31;
```

### Metodos e `self`

```hemlock
let calculator = {
    value: 0,
    add: fn(x) {
        self.value = self.value + x;
    },
    get: fn() {
        return self.value;
    }
};

calculator.add(10);
calculator.add(5);
print(calculator.get());  // 15
```

### Definicoes de Tipo (Duck Typing)

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,  // Campo opcional com valor padrao
}

let p = { name: "Bob", age: 25 };
let typed: Person = p;  // Duck typing valida a estrutura

print(typeof(typed));   // "Person"
print(typed.active);    // true (valor padrao aplicado)
```

### Serializacao JSON

```hemlock
let obj = { x: 10, y: 20, name: "test" };

// Objeto para JSON
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// JSON para objeto
let restored = json.deserialize();
print(restored.name);  // "test"
```

## Gerenciamento de Memoria

### Buffers Seguros (Recomendado)

```hemlock
// Alocar buffer
let buf = buffer(10);
print(buf.length);    // 10
print(buf.capacity);  // 10

// Definir valores (com verificacao de limites)
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Acessar valores
print(buf[0]);  // 65

// Deve liberar quando terminar
free(buf);
```

### Ponteiros Brutos (Avancado)

```hemlock
// Alocar memoria bruta
let ptr = alloc(100);

// Preencher com zeros
memset(ptr, 0, 100);

// Copiar dados
let src = alloc(50);
memcpy(ptr, src, 50);

// Liberar ambos
free(src);
free(ptr);
```

### Funcoes de Memoria

```hemlock
// Realocar
let p = alloc(64);
p = realloc(p, 128);  // Redimensionar para 128 bytes
free(p);

// Alocacao tipada (recurso futuro)
// let arr = talloc(i32, 100);  // Array de 100 i32s
```

## Tratamento de Erros

### Try/Catch

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
}
// Saida: Erro: Erro de divisao por zero
```

### Bloco Finally

```hemlock
let file = null;

try {
    file = open("data.txt", "r");
    let content = file.read();
    print(content);
} catch (e) {
    print("Erro: " + e);
} finally {
    // Sempre executa
    if (file != null) {
        file.close();
    }
}
```

### Lancando Objetos

```hemlock
try {
    throw { code: 404, message: "Nao encontrado" };
} catch (e) {
    print(`Erro ${e.code}: ${e.message}`);
}
// Saida: Erro 404: Nao encontrado
```

### Panic (Erro Irrecuperavel)

```hemlock
fn validate(x) {
    if (x < 0) {
        panic("x deve ser nao negativo");
    }
    return x * 2;
}

validate(-5);  // Programa sai com: panic: x deve ser nao negativo
```

## E/S de Arquivos

### Lendo Arquivos

```hemlock
// Ler arquivo inteiro
let f = open("data.txt", "r");
let content = f.read();
print(content);
f.close();

// Ler numero especifico de bytes
let f2 = open("data.txt", "r");
let chunk = f2.read(100);  // Ler 100 bytes
f2.close();
```

### Escrevendo Arquivos

```hemlock
// Escrever texto
let f = open("output.txt", "w");
f.write("Hello, File!\n");
f.write("Segunda linha\n");
f.close();

// Anexar ao arquivo
let f2 = open("output.txt", "a");
f2.write("Linha anexada\n");
f2.close();
```

### E/S Binaria

```hemlock
// Escrever dados binarios
let buf = buffer(256);
buf[0] = 255;
buf[1] = 128;

let f = open("data.bin", "w");
f.write_bytes(buf);
f.close();

// Ler dados binarios
let f2 = open("data.bin", "r");
let data = f2.read_bytes(256);
print(data[0]);  // 255
f2.close();

free(buf);
free(data);
```

### Propriedades de Arquivo

```hemlock
let f = open("/path/to/file.txt", "r");

print(f.path);    // "/path/to/file.txt"
print(f.mode);    // "r"
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

## Exemplo Completo

Vamos construir um programa simples de contagem de palavras:

```hemlock
// wordcount.hml - Conta palavras em um arquivo

fn count_words(filename: string): i32 {
    let file = null;
    let count = 0;

    try {
        file = open(filename, "r");
        let content = file.read();

        // Dividir por espacos e contar
        let words = content.split(" ");
        count = words.length;

    } catch (e) {
        print("Erro ao ler arquivo: " + e);
        return -1;
    } finally {
        if (file != null) {
            file.close();
        }
    }

    return count;
}

// Programa principal
if (args.length < 2) {
    print("Uso: " + args[0] + " <nome_do_arquivo>");
} else {
    let filename = args[1];
    let words = count_words(filename);

    if (words >= 0) {
        print(`Contagem de palavras: ${words}`);
    }
}
```

Executar:
```bash
./hemlock wordcount.hml data.txt
```

## Proximos Passos

Parabens! Voce aprendeu o basico do Hemlock. A seguir, voce pode explorar:

- [Async e Concorrencia](../advanced/async-concurrency.md) - Multithreading real
- [FFI](../advanced/ffi.md) - Chamar funcoes C
- [Tratamento de Sinais](../advanced/signals.md) - Sinais de processo
- [Referencia da API](../reference/builtins.md) - Documentacao completa da API
- [Exemplos](../../examples/) - Mais programas do mundo real

## Exercicios

Tente construir estes programas para praticar:

1. **Calculadora**: Implemente uma calculadora simples que suporte +, -, *, /
2. **Copiador de Arquivos**: Copie um arquivo para outro
3. **Fibonacci**: Gere a sequencia de Fibonacci
4. **Analisador JSON**: Leia e analise um arquivo JSON
5. **Processador de Texto**: Encontre e substitua texto em um arquivo

Divirta-se programando com Hemlock!
