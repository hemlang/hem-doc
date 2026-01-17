# Funções

Em Hemlock, funções são **cidadãos de primeira classe**, podendo ser atribuídas a variáveis, passadas como argumentos e retornadas de outras funções. Este guia cobre sintaxe de funções, closures, recursão e padrões avançados.

## Visão Geral

```hemlock
// Sintaxe de função nomeada
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Função anônima
let multiply = fn(x, y) {
    return x * y;
};

// Closure
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Declaração de Funções

### Funções Nomeadas

```hemlock
fn greet(name: string): string {
    return "Hello, " + name;
}

let msg = greet("Alice");  // "Hello, Alice"
```

**Componentes:**
- `fn` - palavra-chave de função
- `greet` - nome da função
- `(name: string)` - parâmetros com tipos opcionais
- `: string` - tipo de retorno opcional
- `{ ... }` - corpo da função

### Funções Anônimas

Funções sem nome, atribuídas a variáveis:

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Função nomeada vs anônima:**
```hemlock
// Estas duas formas são equivalentes:
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Nota:** Funções nomeadas são desaçucarizadas para atribuição de variável com função anônima.

## Parâmetros

### Parâmetros Básicos

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Anotações de Tipo

Anotações de tipo opcionais para parâmetros:

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // Verificação de tipo em execução promove para f64
```

**Verificação de tipo:**
- Se anotado, tipos de parâmetros são verificados na chamada
- Conversões implícitas seguem regras de promoção padrão
- Incompatibilidade de tipo causa erro em tempo de execução

### Passagem por Valor

Todos os parâmetros são **copiados** (passagem por valor):

```hemlock
fn modify(x) {
    x = 100;  // Modifica apenas a cópia local
}

let a = 10;
modify(a);
print(a);  // Ainda é 10 (não alterado)
```

**Nota:** Objetos e arrays são passados por referência (a referência é copiada), então seu conteúdo pode ser modificado:

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Modifica o array original
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (modificado)
```

## Valores de Retorno

### Instrução Return

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Anotação de Tipo de Retorno

Anotação de tipo opcional para valor de retorno:

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Verificação de tipo:**
- Se anotado, tipo de retorno é verificado quando a função retorna
- Conversões de tipo seguem regras de promoção padrão

### Retorno Implícito

Funções sem anotação de tipo de retorno implicitamente retornam `null`:

```hemlock
fn print_message(msg) {
    print(msg);
    // Retorna null implicitamente
}

let result = print_message("hello");  // result é null
```

### Retorno Antecipado

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Saída antecipada
        }
    }
    return -1;  // Não encontrado
}
```

### Retorno sem Valor

`return;` sem valor retorna `null`:

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Retorna null
    }
    return value * 2;
}
```

## Funções de Primeira Classe

Funções podem ser atribuídas, passadas e retornadas como qualquer outro valor.

### Funções como Variáveis

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Reatribuir
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Funções como Argumentos

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Funções como Valores de Retorno

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Closures

Funções capturam seu ambiente de definição (escopo léxico).

### Closure Básico

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

**Como funciona:**
- A função interna captura `count` do escopo externo
- `count` persiste entre múltiplas chamadas da função retornada
- Cada chamada a `makeCounter()` cria um novo closure com seu próprio `count`

### Closure com Parâmetros

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Múltiplos Closures

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Escopo Léxico

Funções podem acessar variáveis de escopos externos através de escopo léxico:

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Pode ler global e outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Closures capturam variáveis por referência, permitindo leitura e modificação de variáveis de escopo externo (como mostrado no exemplo `makeCounter` acima).

## Recursão

Funções podem chamar a si mesmas.

### Recursão Básica

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Recursão Mútua

Funções podem chamar umas às outras:

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Processamento de Dados Recursivo

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Nota:** Não há otimização de chamada de cauda ainda - recursão profunda pode causar estouro de pilha.

## Funções de Ordem Superior

Funções que aceitam ou retornam outras funções.

### Padrão Map

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Padrão Filter

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Padrão Reduce

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Composição de Funções

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Padrões Comuns

### Padrão: Função de Fábrica

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### Padrão: Função de Callback

```hemlock
fn process_async(data, callback) {
    // ... processar
    callback(data);
}

process_async("test", fn(result) {
    print("Processing complete: " + result);
});
```

### Padrão: Aplicação Parcial

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Padrão: Memoização

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Muito mais rápido com cache
```

## Semântica de Funções

### Requisito de Tipo de Retorno

Funções com anotação de tipo de retorno **devem** retornar um valor:

```hemlock
fn get_value(): i32 {
    // Erro: falta instrução return
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Verificação de Tipo

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Promove para f64, retorna f64
add("a", "b");     // Erro em tempo de execução: incompatibilidade de tipo
```

### Regras de Escopo

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Pode acessar: inner_var, outer_var, global
    }

    // Pode acessar: outer_var, global
    // Não pode acessar: inner_var
}

// Pode acessar: global
// Não pode acessar: outer_var, inner_var
```

## Melhores Práticas

1. **Use anotações de tipo** - Ajuda a detectar erros e documentar intenção
2. **Mantenha funções pequenas** - Cada função deve fazer apenas uma coisa
3. **Prefira funções puras** - Evite efeitos colaterais quando possível
4. **Nomeie claramente** - Use nomes de verbos descritivos
5. **Retorno antecipado** - Use cláusulas de guarda para reduzir aninhamento
6. **Documente closures complexos** - Deixe claro quais variáveis são capturadas
7. **Evite recursão profunda** - Sem otimização de chamada de cauda ainda

## Armadilhas Comuns

### Armadilha: Profundidade de Recursão

```hemlock
// Recursão profunda pode causar estouro de pilha
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Pode falhar com estouro de pilha
```

### Armadilha: Modificação de Variáveis Capturadas

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Pode ler e modificar variáveis capturadas
        return count;
    };
}
```

**Nota:** Isso funciona, mas esteja ciente de que todos os closures compartilham o mesmo ambiente capturado.

## Exemplos

### Exemplo: Pipeline de Funções

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Exemplo: Manipulador de Eventos

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clicked: " + data);
});

trigger_event("click", "button1");
```

### Exemplo: Ordenação com Comparador Personalizado

```hemlock
fn sort(arr, compare) {
    // Bubble sort com comparador personalizado
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Parâmetros Opcionais (Parâmetros Padrão)

Funções podem definir parâmetros opcionais com valores padrão usando a sintaxe `?:`:

```hemlock
fn greet(name, greeting?: "Hello") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Hello Alice"
print(greet("Bob", "Hi"));       // "Hi Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Regras:**
- Parâmetros opcionais devem vir após parâmetros obrigatórios
- Valores padrão podem ser qualquer expressão
- Parâmetros omitidos usam valores padrão

## Funções Variádicas (Parâmetros Rest)

Funções podem aceitar número variável de argumentos usando parâmetros rest (`...`):

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Starting", "Running", "Done");
// INFO: Starting
// INFO: Running
// INFO: Done
```

**Regras:**
- Parâmetro rest deve ser o último parâmetro
- Parâmetro rest coleta todos os argumentos restantes em um array
- Pode ser combinado com parâmetros normais e opcionais

## Anotações de Tipo de Função

Tipos de função permitem especificar assinaturas precisas para parâmetros e valores de retorno:

### Tipo de Função Básico

```hemlock
// Sintaxe de tipo de função: fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Tipos de Função de Ordem Superior

```hemlock
// Função que retorna função
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Tipos de Função Assíncrona

```hemlock
// Tipo de função assíncrona
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Running async!");
});
```

### Aliases de Tipo de Função

```hemlock
// Criar tipos de função nomeados para clareza
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Parâmetros Const

O modificador `const` impede modificação de parâmetros dentro da função:

### Parâmetro Const Básico

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // Erro: não pode modificar parâmetro const
    for (item in items) {
        print(item);   // OK: leitura permitida
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Imutabilidade Profunda

Parâmetros const forçam imutabilidade profunda - não pode modificar através de nenhum caminho:

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK: leitura permitida
    // person.name = "Bob";   // Erro: não pode modificar
    // person.address.city = "NYC";  // Erro: const profundo
}
```

### Operações Bloqueadas por Const

| Tipo | Bloqueado por Const | Permitido |
|------|--------------|-------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | atribuição de campo | leitura de campo |
| buffer | atribuição de índice | leitura de índice |
| string | atribuição de índice | todos os métodos (retornam novas strings) |

## Parâmetros Nomeados

Funções podem ser chamadas com parâmetros nomeados para maior clareza e flexibilidade:

### Parâmetros Nomeados Básicos

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Argumentos posicionais (tradicional)
create_user("Alice", 25, false);

// Argumentos nomeados - podem estar em qualquer ordem
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Misturando Argumentos Posicionais e Nomeados

```hemlock
// Pular parâmetros opcionais nomeando
create_user("David", active: false);  // Usa age=18 padrão

// Argumentos nomeados devem vir após posicionais
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // Erro: argumento posicional após nomeado
```

### Regras de Parâmetros Nomeados

- Use sintaxe `name: value` para argumentos nomeados
- Argumentos nomeados podem aparecer em qualquer ordem após argumentos posicionais
- Argumentos posicionais não podem seguir argumentos nomeados
- Funciona com parâmetros padrão/opcionais
- Nomes de parâmetro desconhecidos causam erro em tempo de execução

## Limitações

Limitações atuais a observar:

- **Sem passagem por referência** - Palavra-chave `ref` é analisada mas não implementada
- **Sem sobrecarga de função** - Apenas uma função por nome
- **Sem otimização de chamada de cauda** - Recursão profunda limitada pelo tamanho da pilha

## Tópicos Relacionados

- [Fluxo de Controle](control-flow.md) - Funções trabalham com estruturas de controle
- [Objetos](objects.md) - Métodos são funções armazenadas em objetos
- [Tratamento de Erros](error-handling.md) - Funções e tratamento de exceções
- [Tipos](types.md) - Anotações de tipo e conversões

## Veja Também

- **Closures**: Veja a seção "Functions" em CLAUDE.md para semântica de closures
- **Primeira classe**: Funções são valores como qualquer outro
- **Escopo léxico**: Funções capturam seu ambiente de definição
