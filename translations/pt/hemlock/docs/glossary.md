# Glossario

Novo em programacao ou conceitos de sistemas? Este glossario explica termos usados ao longo da documentacao do Hemlock em linguagem simples.

---

## A

### Alocar / Alocacao
**O que significa:** Solicitar ao computador um bloco de memoria para usar.

**Analogia:** Como pegar um livro emprestado em uma biblioteca - voce esta emprestando espaco que precisa devolver depois.

**Em Hemlock:**
```hemlock
let space = alloc(100);  // "I need 100 bytes of memory, please"
// ... use it ...
free(space);             // "I'm done, you can have it back"
```

### Array
**O que significa:** Uma lista de valores armazenados juntos, acessados por posicao (indice).

**Analogia:** Como uma fileira de caixas de correio numeradas 0, 1, 2, 3... Voce pode colocar algo na caixa #2 e depois pegar da caixa #2.

**Em Hemlock:**
```hemlock
let colors = ["red", "green", "blue"];
print(colors[0]);  // "red" - first item is at position 0
print(colors[2]);  // "blue" - third item is at position 2
```

### Async / Assincrono
**O que significa:** Codigo que pode executar "em segundo plano" enquanto outro codigo continua. Em Hemlock, codigo async realmente executa em nucleos de CPU separados simultaneamente.

**Analogia:** Como cozinhar varios pratos ao mesmo tempo - voce coloca o arroz no fogo, e enquanto cozinha, corta os vegetais. Ambos acontecem ao mesmo tempo.

**Em Hemlock:**
```hemlock
async fn slow_task(): i32 {
    // This can run on another CPU core
    return 42;
}

let task = spawn(slow_task);  // Start it running
// ... do other stuff while it runs ...
let result = join(task);      // Wait for it to finish, get result
```

---

## B

### Booleano / Bool
**O que significa:** Um valor que e `true` ou `false`. Nada mais.

**Nomeado apos:** George Boole, um matematico que estudou logica verdadeiro/falso.

**Em Hemlock:**
```hemlock
let is_raining = true;
let has_umbrella = false;

if (is_raining && !has_umbrella) {
    print("You'll get wet!");
}
```

### Verificacao de Limites
**O que significa:** Verificar automaticamente que voce nao esta tentando acessar memoria fora do que foi alocado. Previne crashes e bugs de seguranca.

**Analogia:** Como um bibliotecario que verifica se o livro que voce esta solicitando realmente existe antes de tentar busca-lo.

**Em Hemlock:**
```hemlock
let buf = buffer(10);  // 10 slots, numbered 0-9
buf[5] = 42;           // OK - slot 5 exists
buf[100] = 42;         // ERROR! Hemlock stops you - slot 100 doesn't exist
```

### Buffer
**O que significa:** Um container seguro para bytes brutos com tamanho conhecido. Hemlock verifica que voce nao le ou escreve alem de seus limites.

**Analogia:** Como um cofre com um numero especifico de compartimentos. Voce pode usar qualquer compartimento, mas nao pode acessar o compartimento #50 se o cofre so tem 10.

**Em Hemlock:**
```hemlock
let data = buffer(64);   // 64 bytes of safe storage
data[0] = 65;            // Put 65 in the first byte
print(data.length);      // 64 - you can check its size
free(data);              // Clean up when done
```

---

## C

### Closure
**O que significa:** Uma funcao que "lembra" variaveis de onde foi criada, mesmo apos aquele codigo ter terminado.

**Analogia:** Como uma nota que diz "adicione 5 a qualquer numero que voce me der" - o "5" esta embutido na nota.

**Em Hemlock:**
```hemlock
fn make_adder(amount) {
    return fn(x) {
        return x + amount;  // 'amount' is remembered!
    };
}

let add_five = make_adder(5);
print(add_five(10));  // 15 - it remembered that amount=5
```

### Coercao (Coercao de Tipo)
**O que significa:** Converter automaticamente um valor de um tipo para outro quando necessario.

**Exemplo:** Quando voce soma um inteiro e um decimal, o inteiro e automaticamente convertido para decimal primeiro.

**Em Hemlock:**
```hemlock
let whole: i32 = 5;
let decimal: f64 = 2.5;
let result = whole + decimal;  // 'whole' becomes 5.0, then adds to 2.5
print(result);  // 7.5
```

### Compilar / Compilador
**O que significa:** Traduzir seu codigo para um programa que o computador pode executar diretamente. O compilador (`hemlockc`) le seu arquivo `.hml` e cria um executavel.

**Analogia:** Como traduzir um livro do ingles para o espanhol - o conteudo e o mesmo, mas agora falantes de espanhol podem le-lo.

**Em Hemlock:**
```bash
hemlockc myprogram.hml -o myprogram   # Translate to executable
./myprogram                            # Run the executable
```

### Concorrencia
**O que significa:** Varias coisas acontecendo em momentos sobrepostos. Em Hemlock, isso significa execucao paralela real em multiplos nucleos de CPU.

**Analogia:** Dois chefs cozinhando pratos diferentes simultaneamente na mesma cozinha.

---

## D

### Defer
**O que significa:** Agendar algo para acontecer depois, quando a funcao atual terminar. Util para limpeza.

**Analogia:** Como dizer para si mesmo "quando eu sair, apague as luzes" - voce define o lembrete agora, ele acontece depois.

**Em Hemlock:**
```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();  // "Close this file when I'm done here"

    // ... lots of code ...
    // Even if there's an error, f.close() will run
}
```

### Duck Typing
**O que significa:** Se parece com um pato e faz quack como um pato, trate como um pato. Em codigo: se um objeto tem os campos/metodos que voce precisa, use-o - nao se preocupe com seu "tipo" oficial.

**Nomeado apos:** O teste do pato - uma forma de raciocinio.

**Em Hemlock:**
```hemlock
define Printable {
    name: string
}

fn greet(thing: Printable) {
    print("Hello, " + thing.name);
}

// Any object with a 'name' field works!
greet({ name: "Alice" });
greet({ name: "Bob", age: 30 });  // Extra fields are OK
```

---

## E

### Expressao
**O que significa:** Codigo que produz um valor. Pode ser usado em qualquer lugar onde um valor e esperado.

**Exemplos:** `42`, `x + y`, `get_name()`, `true && false`

### Enum / Enumeracao
**O que significa:** Um tipo com um conjunto fixo de valores possiveis, cada um com um nome.

**Analogia:** Como um menu dropdown - voce so pode escolher entre as opcoes listadas.

**Em Hemlock:**
```hemlock
enum Status {
    PENDING,
    APPROVED,
    REJECTED
}

let my_status = Status.APPROVED;

if (my_status == Status.REJECTED) {
    print("Sorry!");
}
```

---

## F

### Float / Ponto Flutuante
**O que significa:** Um numero com ponto decimal. Chamado "flutuante" porque o ponto decimal pode estar em posicoes diferentes.

**Em Hemlock:**
```hemlock
let pi = 3.14159;      // f64 - 64-bit float (default)
let half: f32 = 0.5;   // f32 - 32-bit float (smaller, less precise)
```

### Free
**O que significa:** Devolver memoria que voce terminou de usar ao sistema para que possa ser reutilizada.

**Analogia:** Devolver um livro da biblioteca para que outros possam pega-lo emprestado.

**Em Hemlock:**
```hemlock
let data = alloc(100);  // Borrow 100 bytes
// ... use data ...
free(data);             // Return it - REQUIRED!
```

### Funcao
**O que significa:** Um bloco reutilizavel de codigo que recebe entradas (parametros) e pode produzir uma saida (valor de retorno).

**Analogia:** Como uma receita - de os ingredientes (entradas), siga os passos, obtenha um prato (saida).

**Em Hemlock:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(3, 4);  // result is 7
```

---

## G

### Coleta de Lixo (GC)
**O que significa:** Limpeza automatica de memoria. O runtime periodicamente encontra memoria nao utilizada e a libera para voce.

**Por que Hemlock nao tem:** GC pode causar pausas imprevisiveis. Hemlock prefere controle explicito - voce decide quando liberar memoria.

**Nota:** A maioria dos tipos Hemlock (strings, arrays, objetos) SAO automaticamente limpos quando saem de escopo. Apenas `ptr` bruto de `alloc()` precisa de `free()` manual.

---

## H

### Heap
**O que significa:** Uma regiao de memoria para dados que precisam sobreviver a funcao atual. Voce aloca e libera memoria heap explicitamente.

**Contraste com:** Stack (armazenamento automatico e temporario para variaveis locais)

**Em Hemlock:**
```hemlock
let ptr = alloc(100);  // This goes on the heap
// ... use it ...
free(ptr);             // You clean up the heap yourself
```

---

## I

### Indice
**O que significa:** A posicao de um item em um array ou string. Comeca em 0 em Hemlock.

**Em Hemlock:**
```hemlock
let letters = ["a", "b", "c"];
//             [0]  [1]  [2]   <- indices

print(letters[0]);  // "a" - first item
print(letters[2]);  // "c" - third item
```

### Inteiro
**O que significa:** Um numero inteiro sem ponto decimal. Pode ser positivo, negativo ou zero.

**Em Hemlock:**
```hemlock
let small = 42;       // i32 - fits in 32 bits
let big = 5000000000; // i64 - needs 64 bits (auto-detected)
let tiny: i8 = 100;   // i8 - explicitly 8 bits
```

### Interpretador
**O que significa:** Um programa que le seu codigo e o executa diretamente, linha por linha.

**Contraste com:** Compilador (traduz o codigo primeiro, depois executa a traducao)

**Em Hemlock:**
```bash
./hemlock script.hml   # Interpreter runs your code directly
```

---

## L

### Literal
**O que significa:** Um valor escrito diretamente no seu codigo, nao calculado.

**Exemplos:**
```hemlock
42              // integer literal
3.14            // float literal
"hello"         // string literal
true            // boolean literal
[1, 2, 3]       // array literal
{ x: 10 }       // object literal
```

---

## M

### Vazamento de Memoria
**O que significa:** Esquecer de liberar memoria alocada. A memoria permanece reservada mas nao utilizada, desperdicando recursos.

**Analogia:** Pegar livros emprestados da biblioteca e nunca devolve-los. Eventualmente, a biblioteca fica sem livros.

**Em Hemlock:**
```hemlock
fn leaky() {
    let ptr = alloc(1000);
    // Oops! Forgot to free(ptr)
    // Those 1000 bytes are lost until program exits
}
```

### Metodo
**O que significa:** Uma funcao associada a um objeto ou tipo.

**Em Hemlock:**
```hemlock
let text = "hello";
let upper = text.to_upper();  // to_upper() is a method on strings
print(upper);  // "HELLO"
```

### Mutex
**O que significa:** Um lock que garante que apenas uma thread acessa algo por vez. Previne corrupcao de dados quando multiplas threads tocam dados compartilhados.

**Analogia:** Como uma tranca de banheiro - apenas uma pessoa pode usa-lo por vez.

---

## N

### Null
**O que significa:** Um valor especial significando "nada" ou "sem valor."

**Em Hemlock:**
```hemlock
let maybe_name = null;

if (maybe_name == null) {
    print("No name provided");
}
```

---

## O

### Objeto
**O que significa:** Uma colecao de valores nomeados (campos/propriedades) agrupados.

**Em Hemlock:**
```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};

print(person.name);  // "Alice"
print(person.age);   // 30
```

---

## P

### Parametro
**O que significa:** Uma variavel que uma funcao espera receber quando chamada.

**Tambem chamado:** Argumento (tecnicamente, parametro esta na definicao, argumento esta na chamada)

**Em Hemlock:**
```hemlock
fn greet(name, times) {   // 'name' and 'times' are parameters
    // ...
}

greet("Alice", 3);        // "Alice" and 3 are arguments
```

### Ponteiro
**O que significa:** Um valor que armazena um endereco de memoria - ele "aponta" para onde os dados estao armazenados.

**Analogia:** Como um endereco de rua. O endereco nao e a casa - ele te diz onde encontrar a casa.

**Em Hemlock:**
```hemlock
let ptr = alloc(100);  // ptr holds the address of 100 bytes
// ptr doesn't contain the data - it points to where the data lives
free(ptr);
```

### Primitivo
**O que significa:** Um tipo basico e integrado que nao e feito de outros tipos.

**Em Hemlock:** `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `rune`, `null`

---

## R

### Contagem de Referencia (Refcounting)
**O que significa:** Rastrear quantas coisas estao usando um dado. Quando nada mais o usa, limpar automaticamente.

**Em Hemlock:** Strings, arrays, objetos e buffers usam refcounting internamente. Voce nao ve, mas previne vazamentos de memoria para os tipos mais comuns.

### Valor de Retorno
**O que significa:** O valor que uma funcao envia de volta quando termina.

**Em Hemlock:**
```hemlock
fn double(x) {
    return x * 2;  // This is the return value
}

let result = double(5);  // result gets the return value: 10
```

### Rune
**O que significa:** Um unico caractere Unicode (codepoint). Pode representar qualquer caractere incluindo emoji.

**Por que "rune"?** O termo vem de Go. Ele enfatiza que este e um caractere completo, nao apenas um byte.

**Em Hemlock:**
```hemlock
let letter = 'A';
let emoji = '🚀';
let code: i32 = letter;  // 65 - the Unicode codepoint
```

### Runtime
**O que significa:** O momento em que seu programa esta realmente executando (em oposicao a "tempo de compilacao" quando esta sendo traduzido).

**Tambem:** O codigo de suporte que executa junto com seu programa (ex: o alocador de memoria).

---

## S

### Escopo
**O que significa:** A regiao de codigo onde uma variavel existe e pode ser usada.

**Em Hemlock:**
```hemlock
let outer = 1;              // Lives in outer scope

if (true) {
    let inner = 2;          // Lives only inside this block
    print(outer);           // OK - can see outer scope
    print(inner);           // OK - we're inside its scope
}

print(outer);               // OK
// print(inner);            // ERROR - inner doesn't exist here
```

### Stack
**O que significa:** Memoria para dados temporarios e de curta duracao. Gerenciada automaticamente - quando uma funcao retorna, seu espaco na stack e recuperado.

**Contraste com:** Heap (vida mais longa, gerenciada manualmente)

### Statement
**O que significa:** Uma unica instrucao ou comando. Statements FAZEM coisas; expressoes PRODUZEM valores.

**Exemplos:** `let x = 5;`, `print("hi");`, `if (x > 0) { ... }`

### String
**O que significa:** Uma sequencia de caracteres de texto.

**Em Hemlock:**
```hemlock
let greeting = "Hello, World!";
print(greeting.length);    // 13 characters
print(greeting[0]);        // "H" - first character
```

### Tipagem Estrutural
**O que significa:** Compatibilidade de tipo baseada em estrutura (quais campos/metodos existem), nao em nome. O mesmo que "duck typing."

---

## T

### Thread
**O que significa:** Um caminho separado de execucao. Multiplas threads podem executar simultaneamente em diferentes nucleos de CPU.

**Em Hemlock:** `spawn()` cria uma nova thread.

### Tipo
**O que significa:** O tipo de dado que um valor representa. Determina quais operacoes sao validas.

**Em Hemlock:**
```hemlock
let x = 42;              // type: i32
let name = "Alice";      // type: string
let nums = [1, 2, 3];    // type: array

print(typeof(x));        // "i32"
print(typeof(name));     // "string"
```

### Anotacao de Tipo
**O que significa:** Declarar explicitamente qual tipo uma variavel deve ter.

**Em Hemlock:**
```hemlock
let x: i32 = 42;         // x must be an i32
let name: string = "hi"; // name must be a string

fn add(a: i32, b: i32): i32 {  // parameters and return type annotated
    return a + b;
}
```

---

## U

### UTF-8
**O que significa:** Uma forma de codificar texto que suporta todos os idiomas do mundo e emoji. Cada caractere pode ter de 1 a 4 bytes.

**Em Hemlock:** Todas as strings sao UTF-8.

```hemlock
let text = "Hello, 世界! 🌍";  // Mix of ASCII, Chinese, emoji - all work
```

---

## V

### Variavel
**O que significa:** Um local de armazenamento nomeado que guarda um valor.

**Em Hemlock:**
```hemlock
let count = 0;    // Create variable 'count', store 0
count = count + 1; // Update it to 1
print(count);     // Read its value: 1
```

---

## Referencia Rapida: Qual Tipo Devo Usar?

| Situacao | Use Isto | Por que |
|----------|----------|---------|
| Preciso apenas de um numero | `let x = 42;` | Hemlock escolhe o tipo certo |
| Contando coisas | `i32` | Grande o suficiente para a maioria das contagens |
| Numeros enormes | `i64` | Quando i32 nao e suficiente |
| Bytes (0-255) | `u8` | Arquivos, dados de rede |
| Decimais | `f64` | Matematica decimal precisa |
| Valores Sim/Nao | `bool` | Apenas `true` ou `false` |
| Texto | `string` | Qualquer conteudo de texto |
| Caractere unico | `rune` | Uma letra/emoji |
| Lista de coisas | `array` | Colecao ordenada |
| Campos nomeados | `object` | Agrupar dados relacionados |
| Memoria bruta | `buffer` | Armazenamento seguro de bytes |
| Trabalho FFI/sistemas | `ptr` | Avancado, memoria manual |

---

## Veja Tambem

- [Inicio Rapido](getting-started/quick-start.md) - Seu primeiro programa Hemlock
- [Sistema de Tipos](language-guide/types.md) - Documentacao completa de tipos
- [Gerenciamento de Memoria](language-guide/memory.md) - Entendendo memoria
