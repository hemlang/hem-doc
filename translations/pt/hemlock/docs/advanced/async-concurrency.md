# Hemlock Assincronismo e Concorrência

Hemlock oferece **concorrência estruturada**, com suporte a sintaxe async/await, criação de tarefas e comunicação por canais. A implementação é baseada em threads POSIX (pthreads), proporcionando **verdadeiro paralelismo multi-thread**.

## Índice

- [Visão Geral](#visão-geral)
- [Modelo de Threads](#modelo-de-threads)
- [Funções Assíncronas](#funções-assíncronas)
- [Criação de Tarefas](#criação-de-tarefas)
- [Canais](#canais)
- [Propagação de Exceções](#propagação-de-exceções)
- [Detalhes de Implementação](#detalhes-de-implementação)
- [Melhores Práticas](#melhores-práticas)
- [Características de Desempenho](#características-de-desempenho)
- [Limitações Atuais](#limitações-atuais)

## Visão Geral

**Isso significa:**
- Threads reais do sistema operacional - cada tarefa criada executa em seu próprio pthread (thread POSIX)
- Paralelismo real - tarefas executam simultaneamente em múltiplos núcleos de CPU
- Escalonamento do kernel - o escalonador do SO distribui tarefas entre os núcleos disponíveis
- Canais thread-safe - sincronização usando mutexes e variáveis de condição pthread

**Isso não é:**
- Não são green threads - não é multitarefa cooperativa em espaço de usuário
- Não são coroutines async/await - não é um event loop single-thread como JavaScript/Python asyncio
- Não é concorrência simulada - não é paralelismo simulado

Isso é o **mesmo modelo de threads** que **C, C++ e Rust** usam com threads do SO. Você obtém execução paralela real em múltiplos núcleos.

## Modelo de Threads

### Modelo de Threads 1:1

Hemlock usa um **modelo de threads 1:1**, onde:
- Cada tarefa criada gera uma thread dedicada do SO via `pthread_create()`
- O kernel do SO escalona threads entre os núcleos de CPU disponíveis
- Multitarefa preemptiva - o SO pode interromper e alternar entre threads
- **Sem GIL** - diferente de Python, não há Global Interpreter Lock limitando o paralelismo

### Mecanismos de Sincronização

- **Mutexes** - canais usam `pthread_mutex_t` para acesso thread-safe
- **Variáveis de Condição** - send/recv bloqueantes usam `pthread_cond_t` para espera eficiente
- **Operações Lock-free** - transições de estado de tarefas são atômicas

## Funções Assíncronas

Funções podem ser declaradas como `async`, indicando que foram projetadas para execução concorrente:

```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
```

### Pontos Importantes

- `async fn` declara uma função assíncrona
- Funções assíncronas podem ser criadas como tarefas concorrentes usando `spawn()`
- Funções assíncronas também podem ser chamadas diretamente (executando sincronamente na thread atual)
- Quando criadas, cada tarefa executa em **sua própria thread do SO** (não são coroutines!)
- A palavra-chave `await` está reservada para uso futuro

### Exemplo: Chamada Direta vs Criação de Tarefa

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Chamada direta - executa sincronamente
let result1 = factorial(5);  // 120

// Criar tarefa - executa em thread separada
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## Criação de Tarefas

Use `spawn()` para executar funções assíncronas **em paralelo em threads separadas do SO**:

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Criar múltiplas tarefas - estas executam em paralelo em diferentes núcleos de CPU!
let t1 = spawn(factorial, 5);  // Thread 1
let t2 = spawn(factorial, 6);  // Thread 2
let t3 = spawn(factorial, 7);  // Thread 3

// As três tarefas estão computando simultaneamente agora!

// Aguardar resultados
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### Funções Integradas

#### spawn(async_fn, arg1, arg2, ...)

Cria uma nova tarefa em um novo pthread, retorna um handle de tarefa.

**Parâmetros:**
- `async_fn` - a função assíncrona a executar
- `arg1, arg2, ...` - argumentos a passar para a função

**Retorna:** Handle de tarefa (valor opaco para uso com `join()` ou `detach()`)

**Exemplo:**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... lógica de processamento
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

Aguarda a tarefa completar (bloqueia até a thread terminar), retorna o resultado.

**Parâmetros:**
- `task` - handle de tarefa retornado por `spawn()`

**Retorna:** O valor retornado pela função assíncrona

**Exemplo:**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // Bloqueia até compute() terminar
print(result);
```

**Importante:** Cada tarefa só pode ser joined uma vez. Joins subsequentes resultarão em erro.

#### detach(task)

Execução fire-and-forget (a thread executa independentemente, join não é permitido).

**Parâmetros:**
- `task` - handle de tarefa retornado por `spawn()`

**Retorna:** `null`

**Exemplo:**
```hemlock
async fn background_work() {
    // Tarefa de longa duração em background
    // ...
}

let task = spawn(background_work);
detach(task);  // Tarefa executa independentemente, não pode ser joined
```

**Importante:** Tarefas detached não podem ser joined. Quando a tarefa completa, tanto o pthread quanto a estrutura Task são automaticamente limpos.

## Canais

Canais fornecem comunicação thread-safe entre tarefas usando buffers limitados e semântica bloqueante.

### Criando Canais

```hemlock
let ch = channel(10);  // Cria canal com buffer de tamanho 10
```

**Parâmetros:**
- `capacity` (i32) - número máximo de valores que o canal pode armazenar

**Retorna:** Objeto canal

### Métodos de Canal

#### send(value)

Envia valor para o canal (bloqueia se estiver cheio).

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let task = spawn(producer, ch, 5);
```

**Comportamento:**
- Se o canal tem espaço, o valor é adicionado imediatamente
- Se o canal está cheio, o emissor bloqueia até haver espaço disponível
- Se o canal está fechado, lança uma exceção

#### recv()

Recebe valor do canal (bloqueia se estiver vazio).

```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let task = spawn(consumer, ch, 5);
```

**Comportamento:**
- Se o canal tem valores, retorna o próximo valor imediatamente
- Se o canal está vazio, o receptor bloqueia até um valor estar disponível
- Se o canal está fechado e vazio, retorna `null`

#### close()

Fecha o canal (recv em canal fechado retorna null).

```hemlock
ch.close();
```

**Comportamento:**
- Impede operações `send()` futuras (lançará exceção)
- Permite operações `recv()` pendentes completarem
- Uma vez vazio, `recv()` retorna `null`

### Multiplexação com select()

A função `select()` permite esperar em múltiplos canais simultaneamente, retornando quando qualquer canal tiver dados disponíveis.

**Assinatura:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parâmetros:**
- `channels` - array de valores de canal
- `timeout_ms` (opcional) - timeout em milissegundos (-1 ou omitido para espera infinita)

**Retorna:**
- `{ channel, value }` - objeto contendo o canal que tinha dados e o valor recebido
- `null` - em timeout (se timeout foi especificado)

**Exemplo:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Tarefas produtoras
spawn(fn() {
    sleep(100);
    ch1.send("from channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("from channel 2");
});

// Espera pelo primeiro resultado (ch2 deve ser mais rápido)
let result = select([ch1, ch2]);
print(result.value);  // "from channel 2"

// Espera pelo segundo resultado
let result2 = select([ch1, ch2]);
print(result2.value);  // "from channel 1"
```

**Com Timeout:**
```hemlock
let ch = channel(1);

// Sem emissor, vai ter timeout
let result = select([ch], 100);  // timeout de 100ms
if (result == null) {
    print("Timed out!");
}
```

**Casos de Uso:**
- Esperar pelo mais rápido entre múltiplas fontes de dados
- Implementar timeouts em operações de canal
- Padrões de event loop com múltiplas fontes de eventos
- Fan-in: combinar múltiplos canais em um

**Padrão Fan-in:**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // Todos os canais fechados
        }
        output.send(result.value);
    }
    output.close();
}
```

### Exemplo Completo Produtor-Consumidor

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Criar canal com tamanho de buffer
let ch = channel(10);

// Criar produtor e consumidor
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Esperar completar
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### Múltiplos Produtores, Múltiplos Consumidores

Canais podem ser compartilhados com segurança entre múltiplos produtores e consumidores:

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// Múltiplos produtores
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// Múltiplos consumidores
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// Esperar todos
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## Propagação de Exceções

Exceções lançadas em tarefas criadas são propagadas no join:

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task failed!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Caught: " + e);  // "Caught: Task failed!"
}
```

### Padrões de Tratamento de Exceções

**Padrão 1: Tratar na Tarefa**
```hemlock
async fn safe_task() {
    try {
        // Operação arriscada
    } catch (e) {
        print("Error in task: " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // Sem propagação de exceção
```

**Padrão 2: Propagar ao Chamador**
```hemlock
async fn task_that_throws() {
    throw "error";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("Caught from task: " + e);
}
```

**Padrão 3: Tarefas Detached com Exceções**
```hemlock
async fn detached_task() {
    try {
        // Trabalho
    } catch (e) {
        // Deve tratar internamente - não pode propagar
        print("Error: " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // Não é possível capturar exceções de tarefas detached
```

## Detalhes de Implementação

### Arquitetura de Threads

- **Threads 1:1** - cada tarefa criada gera uma thread dedicada do SO via `pthread_create()`
- **Escalonamento do Kernel** - o kernel do SO escalona threads entre os núcleos de CPU disponíveis
- **Multitarefa Preemptiva** - o SO pode interromper e alternar entre threads
- **Sem GIL** - diferente de Python, não há Global Interpreter Lock limitando o paralelismo

### Implementação de Canais

Canais usam um buffer circular com sincronização pthread:

```
Estrutura do Canal:
- buffer[] - array de Values de tamanho fixo
- capacity - número máximo de elementos
- size - número atual de elementos
- head - posição de leitura
- tail - posição de escrita
- mutex - pthread_mutex_t para acesso thread-safe
- not_empty - pthread_cond_t para recv bloqueante
- not_full - pthread_cond_t para send bloqueante
- closed - flag booleana
- refcount - contagem de referências para limpeza
```

**Comportamento Bloqueante:**
- `send()` em canal cheio: espera na variável de condição `not_full`
- `recv()` em canal vazio: espera na variável de condição `not_empty`
- Ambas são sinalizadas pela operação oposta quando apropriado

### Memória e Limpeza

- **Tarefas Joined:** Limpas automaticamente após `join()` retornar
- **Tarefas Detached:** Limpas automaticamente quando a tarefa completa
- **Canais:** Contagem de referências, liberados quando não mais em uso

## Melhores Práticas

### 1. Sempre Feche Canais

```hemlock
async fn producer(ch) {
    // ... enviar valores
    ch.close();  // Importante: sinaliza que não há mais valores
}
```

### 2. Use Concorrência Estruturada

Crie tarefas e as faça join no mesmo escopo:

```hemlock
fn process_data(data) {
    // Criar tarefas
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // Sempre join antes de retornar
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. Trate Exceções Apropriadamente

```hemlock
async fn task() {
    try {
        // Operação arriscada
    } catch (e) {
        // Registrar erro
        throw e;  // Re-lançar se o chamador precisa saber
    }
}
```

### 4. Use Capacidade de Canal Apropriada

- **Capacidade pequena (1-10):** Para coordenação/sinalização
- **Capacidade média (10-100):** Para produtor-consumidor geral
- **Capacidade grande (100+):** Para cenários de alto throughput

```hemlock
let signal_ch = channel(1);      // Coordenação
let work_ch = channel(50);       // Fila de trabalho
let buffer_ch = channel(1000);   // Alto throughput
```

### 5. Detach Apenas Quando Necessário

Prefira `join()` sobre `detach()` para melhor gerenciamento de recursos:

```hemlock
// Bom: Join e obter resultado
let task = spawn(work);
let result = join(task);

// Use detach apenas para fire-and-forget real
let bg_task = spawn(background_logging);
detach(bg_task);  // Executará independentemente
```

## Características de Desempenho

### Paralelismo Real

- **N tarefas criadas podem utilizar N núcleos de CPU simultaneamente**
- Speedup comprovado - testes de stress mostram tempo de CPU vs tempo de relógio de 8-9x (trabalho multi-core)
- Escala linearmente com número de núcleos (até o número de threads)

### Overhead de Threads

- Cada tarefa tem ~8KB de stack + overhead de pthread
- Custo de criação de thread: ~10-20 microssegundos
- Custo de troca de contexto: ~1-5 microssegundos

### Quando Usar Async

**Bons casos de uso:**
- Computações CPU-intensivas paralelizáveis
- Operações I/O-bound (embora I/O ainda seja bloqueante)
- Processamento concorrente de dados independentes
- Arquitetura de pipeline usando canais

**Não ideal para:**
- Tarefas muito curtas (overhead de thread domina)
- Tarefas com muita sincronização (overhead de contenção)
- Sistemas single-core (sem ganho de paralelismo)

### I/O Bloqueante Seguro

Operações bloqueantes em uma tarefa não bloqueiam outras tarefas:

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // Bloqueia apenas esta thread
    let content = f.read();       // Bloqueia apenas esta thread
    f.close();
    return content;
}

// Ambas leem concorrentemente (em threads diferentes)
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## Modelo de Segurança de Threads

Hemlock usa um modelo de concorrência **passagem de mensagens**, onde tarefas se comunicam através de canais ao invés de estado mutável compartilhado.

### Isolamento de Argumentos

Quando você cria uma tarefa, **argumentos são copiados profundamente** para prevenir condições de corrida:

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // Modifica a cópia, não o original
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - não modificado!
print(modified.length);  // 4 - tem novo elemento
```

**O que é copiado profundamente:**
- Arrays (e todos os elementos recursivamente)
- Objetos (e todos os campos recursivamente)
- Strings
- Buffers

**O que é compartilhado (mantém referência):**
- Canais (mecanismo de comunicação - compartilhado intencionalmente)
- Handles de tarefa (para coordenação)
- Funções (código é imutável)
- Handles de arquivo (SO gerencia acesso concorrente)
- Handles de socket (SO gerencia acesso concorrente)

**O que não pode ser passado:**
- Ponteiros brutos (`ptr`) - use `buffer` em vez disso

### Por Que Passagem de Mensagens?

Isso segue a filosofia do Hemlock de "explícito é melhor que implícito":

```hemlock
// Ruim: Estado mutável compartilhado (causaria corrida de dados)
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // Corrida!
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // Corrida!

// Bom: Passagem de mensagens através de canais
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - sem condição de corrida
```

### Segurança de Thread na Contagem de Referências

Todas as operações de contagem de referências usam **operações atômicas** para prevenir erros use-after-free:
- `string_retain/release` - atômico
- `array_retain/release` - atômico
- `object_retain/release` - atômico
- `buffer_retain/release` - atômico
- `function_retain/release` - atômico
- `channel_retain/release` - atômico
- `task_retain/release` - atômico

Isso garante gerenciamento de memória seguro mesmo quando valores são compartilhados entre threads.

### Acesso ao Ambiente de Closure

Tarefas podem acessar o ambiente de closure:
- Funções integradas (`print`, `len`, etc.)
- Definições de funções globais
- Constantes e variáveis

O ambiente de closure é protegido por um mutex por ambiente, tornando leituras e escritas concorrentes thread-safe:

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK: lendo variável de closure (thread-safe)
}

async fn modify_closure() {
    x = 20;  // OK: escrevendo variável de closure (sincronizado com mutex)
}
```

**Nota:** Embora o acesso concorrente seja sincronizado, modificar estado compartilhado de múltiplas tarefas ainda pode levar a condições de corrida lógicas (ordem não-determinística). Para comportamento previsível, use canais para comunicação entre tarefas ou use valores de retorno de tarefas.

Se você precisa retornar dados de tarefas, use valores de retorno ou canais.

## Limitações Atuais

### 1. Sem Escalonador Work-Stealing

Cada tarefa usa 1 thread, o que pode ser ineficiente para muitas tarefas curtas.

**Atual:** 1000 tarefas = 1000 threads (muito overhead)

**Planejado:** Pool de threads com work-stealing para eficiência

### 3. Sem Integração de I/O Assíncrono

Operações de arquivo/rede ainda bloqueiam a thread:

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // Bloqueia a thread
    f.close();
    return content;
}
```

**Workaround:** Use múltiplas threads para operações I/O concorrentes

### 4. Capacidade de Canal Fixa

A capacidade do canal é definida na criação e não pode ser redimensionada:

```hemlock
let ch = channel(10);
// Não é possível redimensionar dinamicamente para 20
```

### 5. Tamanho de Canal Fixo

O tamanho do buffer do canal não pode ser alterado após a criação.

## Padrões Comuns

### Map Paralelo

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // Criar workers
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // Enviar dados
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // Coletar resultados
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // Esperar workers
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### Arquitetura de Pipeline

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// Criar pipeline
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// Entrada de dados
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// Coletar saída
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### Fan-out, Fan-in

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // Processar valor
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// Fan-out: múltiplos workers
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// Enviar trabalho
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// Fan-in: coletar todos os resultados
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// Esperar todos os workers
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## Resumo

O modelo de assincronismo/concorrência do Hemlock oferece:

- Paralelismo multi-thread real usando threads do SO
- Primitivas simples de concorrência estruturada
- Comunicação thread-safe via canais
- Propagação de exceções entre tarefas
- Desempenho comprovado em sistemas multi-core
- **Isolamento de argumentos** - cópia profunda previne corridas de dados
- **Contagem de referências atômica** - gerenciamento de memória seguro entre threads

Isso torna Hemlock adequado para:
- Computação paralela
- Operações I/O concorrentes
- Arquiteturas de pipeline
- Padrões produtor-consumidor

Enquanto evita as complexidades de:
- Gerenciamento manual de threads
- Primitivas de sincronização de baixo nível
- Designs baseados em locks propensos a deadlock
- Erros de estado mutável compartilhado
