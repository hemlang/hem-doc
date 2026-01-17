# Referencia da API de Concorrencia

Documentacao completa do sistema assincrono/concorrente do Hemlock.

---

## Visao Geral

Hemlock fornece **concorrencia estruturada** e verdadeiro paralelismo multithreaded usando threads POSIX (pthreads). Cada tarefa criada executa em uma thread de sistema operacional separada, permitindo execucao paralela real atraves de multiplos nucleos de CPU.

**Caracteristicas Principais:**
- Verdadeiro paralelismo multithreaded (nao green threads)
- Sintaxe de funcoes assincronas
- Criacao e uniao de tarefas
- Canais thread-safe
- Propagacao de excecoes

**Modelo de Threading:**
- Threads de SO reais (POSIX pthreads)
- Verdadeiro paralelismo (multiplos nucleos de CPU)
- Escalonamento do kernel (multitarefa preemptiva)
- Sincronizacao thread-safe (mutexes, variaveis de condicao)

---

## Funcoes Assincronas

### Declaracao de Funcao Assincrona

Funcoes podem ser declaradas como `async` para indicar que sao projetadas para execucao concorrente.

**Sintaxe:**
```hemlock
async fn nome_funcao(params): tipo_retorno {
    // corpo da funcao
}
```

**Exemplo:**
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

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Processando:", data);
    return null;
}
```

**Comportamento:**
- `async fn` declara uma funcao assincrona
- Pode ser chamada sincronamente (executa na thread atual)
- Pode ser criada como tarefa concorrente (executa em nova thread)
- Quando criada, executa em sua propria thread de SO

**Nota:** A palavra-chave `await` esta reservada para uso futuro, mas nao esta implementada atualmente.

---

## Gerenciamento de Tarefas

### spawn

Cria e inicia uma nova tarefa concorrente.

**Assinatura:**
```hemlock
spawn(async_fn: function, ...args): task
```

**Parametros:**
- `async_fn` - A funcao assincrona a executar
- `...args` - Argumentos a passar para a funcao

**Retorna:** Handle de tarefa

**Exemplo:**
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

// Cria uma unica tarefa
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// Cria multiplas tarefas (executam em paralelo!)
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// Tres tarefas executando simultaneamente!

// Aguarda resultados
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**Comportamento:**
- Cria nova thread de SO via `pthread_create()`
- Comeca a executar a funcao imediatamente
- Retorna handle de tarefa para uniao posterior
- Tarefas executam em paralelo em nucleos de CPU separados

---

### join

Aguarda a conclusao de uma tarefa e obtem seu resultado.

**Assinatura:**
```hemlock
join(task: task): any
```

**Parametros:**
- `task` - Handle de tarefa de `spawn()`

**Retorna:** O valor de retorno da tarefa

**Exemplo:**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // Bloqueia ate a tarefa completar
print(result);         // 3628800
```

**Comportamento:**
- Bloqueia a thread atual ate a tarefa completar
- Retorna o valor de retorno da tarefa
- Propaga excecoes lancadas na tarefa
- Limpa recursos da tarefa apos retornar

**Tratamento de Erros:**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarefa falhou!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Capturado:", e);  // "Capturado: Tarefa falhou!"
}
```

---

### detach

Desanexa uma tarefa (execucao fire-and-forget).

**Assinatura:**
```hemlock
detach(task: task): null
```

**Parametros:**
- `task` - Handle de tarefa de `spawn()`

**Retorna:** `null`

**Exemplo:**
```hemlock
async fn background_work() {
    print("Trabalhando em segundo plano...");
    return null;
}

let t = spawn(background_work);
detach(t);  // Tarefa continua executando independentemente

// Nao pode unir tarefa desanexada
// join(t);  // Erro
```

**Comportamento:**
- Tarefa continua executando independentemente
- Nao pode fazer `join()` em tarefa desanexada
- Tarefa e thread sao limpos automaticamente quando completa

**Casos de Uso:**
- Tarefas de segundo plano fire-and-forget
- Tarefas de log/monitoramento
- Tarefas onde o valor de retorno nao e necessario

---

## Canais

Canais fornecem comunicacao thread-safe entre tarefas.

### channel

Cria um canal com buffer.

**Assinatura:**
```hemlock
channel(capacity: i32): channel
```

**Parametros:**
- `capacity` - Tamanho do buffer (numero de valores)

**Retorna:** Objeto de canal

**Exemplo:**
```hemlock
let ch = channel(10);  // Canal com buffer de capacidade 10
let ch2 = channel(1);  // Buffer minimo (sincrono)
let ch3 = channel(100); // Buffer grande
```

**Comportamento:**
- Cria canal thread-safe
- Usa pthread mutex para sincronizacao
- Capacidade e fixa na criacao

---

### Metodos de Canal

#### send

Envia um valor para o canal (bloqueia se cheio).

**Assinatura:**
```hemlock
channel.send(value: any): null
```

**Parametros:**
- `value` - Valor a enviar (qualquer tipo)

**Retorna:** `null`

**Exemplo:**
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
let t = spawn(producer, ch, 5);
```

**Comportamento:**
- Envia valor para o canal
- Bloqueia se o canal estiver cheio
- Thread-safe (usa mutex)
- Retorna apos o valor ser enviado

---

#### recv

Recebe um valor do canal (bloqueia se vazio).

**Assinatura:**
```hemlock
channel.recv(): any
```

**Retorna:** Valor do canal, ou `null` se o canal estiver fechado e vazio

**Exemplo:**
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
let t = spawn(consumer, ch, 5);
```

**Comportamento:**
- Recebe valor do canal
- Bloqueia se o canal estiver vazio
- Retorna `null` se o canal estiver fechado e vazio
- Thread-safe (usa mutex)

---

#### close

Fecha o canal (nao permite mais envios).

**Assinatura:**
```hemlock
channel.close(): null
```

**Retorna:** `null`

**Exemplo:**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // Sinaliza que nao ha mais valores
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // Canal fechado
        }
        print(val);
    }
    return null;
}
```

**Comportamento:**
- Fecha o canal
- Nao permite mais envios
- `recv()` retorna `null` quando o canal estiver vazio
- Thread-safe

---

## Exemplo Completo de Concorrencia

### Padrao Produtor-Consumidor

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Produzindo:", i);
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
        print("Consumindo:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Cria canal
let ch = channel(10);

// Cria produtor e consumidor
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Aguarda conclusao
join(p);
let total = join(c);
print("Total:", total);  // 0+10+20+30+40 = 100
```

---

## Computacao Paralela

### Exemplo Multi-Tarefa

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Cria multiplas tarefas (executam em paralelo!)
let t1 = spawn(factorial, 5);   // Thread 1
let t2 = spawn(factorial, 6);   // Thread 2
let t3 = spawn(factorial, 7);   // Thread 3
let t4 = spawn(factorial, 8);   // Thread 4

// Quatro tarefas computando simultaneamente!

// Aguarda resultados
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## Ciclo de Vida de Tarefas

### Transicoes de Estado

1. **Criada** - Tarefa foi criada mas ainda nao esta executando
2. **Executando** - Tarefa esta executando em thread de SO
3. **Completada** - Tarefa terminou (resultado disponivel)
4. **Unida** - Resultado foi obtido, recursos limpos
5. **Desanexada** - Tarefa continua executando independentemente

### Exemplo de Ciclo de Vida

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. Cria tarefa
let t = spawn(work, 21);  // Estado: Executando

// Tarefa executa em thread separada...

// 2. Une tarefa
let result = join(t);     // Estado: Completada -> Unida
print(result);            // 42

// Recursos da tarefa sao limpos apos uniao
```

### Ciclo de Vida Desanexado

```hemlock
async fn background() {
    print("Tarefa de segundo plano executando");
    return null;
}

// 1. Cria tarefa
let t = spawn(background);  // Estado: Executando

// 2. Desanexa tarefa
detach(t);                  // Estado: Desanexada

// Tarefa continua executando independentemente
// Recursos limpos pelo SO quando completa
```

---

## Tratamento de Erros

### Propagacao de Excecoes

Excecoes lancadas em tarefas sao propagadas ao unir:

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarefa falhou!";
    }
    return 42;
}

// Tarefa bem-sucedida
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// Tarefa que falha
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Capturado:", e);  // "Capturado: Tarefa falhou!"
}
```

### Tratando Multiplas Tarefas

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Tarefa " + typeof(id) + " falhou";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // Vai falhar
let t3 = spawn(work, 3, 0);

// Une com tratamento de erros
try {
    let r1 = join(t1);  // OK
    print("Tarefa 1:", r1);

    let r2 = join(t2);  // Lanca excecao
    print("Tarefa 2:", r2);  // Nunca alcancado
} catch (e) {
    print("Erro:", e);  // "Erro: Tarefa 2 falhou"
}

// Ainda pode unir tarefas restantes
let r3 = join(t3);
print("Tarefa 3:", r3);
```

---

## Caracteristicas de Performance

### Verdadeiro Paralelismo

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Execucao sequencial
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// Execucao paralela
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// parallel_time deve ser ~50% de sequential_time em sistema multi-core
```

**Caracteristicas Comprovadas:**
- N tarefas podem utilizar N nucleos de CPU simultaneamente
- Testes de estresse mostram razao de tempo CPU/wall de 8-9x (prova de paralelismo)
- Overhead de thread: ~8KB de pilha + overhead de pthread por tarefa
- Operacao bloqueante em uma tarefa nao bloqueia outras tarefas

---

## Detalhes de Implementacao

### Modelo de Threading

- **Threading 1:1** - Cada tarefa = 1 thread de SO (`pthread`)
- **Escalonamento do Kernel** - Kernel do SO distribui threads entre nucleos
- **Multitarefa Preemptiva** - SO pode interromper e alternar threads
- **Sem GIL** - Sem lock de interpretador global (diferente de Python)

### Sincronizacao

- **Mutexes** - Canais usam `pthread_mutex_t`
- **Variaveis de Condicao** - send/recv bloqueantes usam `pthread_cond_t`
- **Operacoes Lock-Free** - Transicoes de estado de tarefa sao atomicas

### Memoria e Limpeza

- **Tarefas Unidas** - Limpas automaticamente apos `join()`
- **Tarefas Desanexadas** - Limpas automaticamente quando tarefa completa
- **Canais** - Contados por referencia, liberados quando nao mais em uso

---

## Limitacoes

- Sem `select()` para multiplexar multiplos canais
- Sem escalonador work-stealing (1 thread por tarefa)
- Sem integracao de I/O assincrono (operacoes de arquivo/rede bloqueiam)
- Capacidade de canal e fixa na criacao

---

## Resumo Completo da API

### Funcoes

| Funcao    | Assinatura                            | Retorna   | Descricao                           |
|-----------|---------------------------------------|-----------|-------------------------------------|
| `spawn`   | `(async_fn: function, ...args)`       | `task`    | Cria e inicia tarefa concorrente    |
| `join`    | `(task: task)`                        | `any`     | Aguarda tarefa, obtem resultado     |
| `detach`  | `(task: task)`                        | `null`    | Desanexa tarefa (fire-and-forget)   |
| `channel` | `(capacity: i32)`                     | `channel` | Cria canal thread-safe              |

### Metodos de Canal

| Metodo  | Assinatura        | Retorna | Descricao                           |
|---------|-------------------|---------|-------------------------------------|
| `send`  | `(value: any)`    | `null`  | Envia valor (bloqueia se cheio)     |
| `recv`  | `()`              | `any`   | Recebe valor (bloqueia se vazio)    |
| `close` | `()`              | `null`  | Fecha canal                         |

### Tipos

| Tipo      | Descricao                              |
|-----------|----------------------------------------|
| `task`    | Handle para uma tarefa concorrente     |
| `channel` | Canal de comunicacao thread-safe       |

---

## Melhores Praticas

### O Que Fazer

- Use canais para comunicacao entre tarefas
- Trate excecoes de tarefas unidas
- Feche canais apos enviar
- Use `join()` para obter resultados e limpar
- Apenas crie funcoes async

### O Que Nao Fazer

- Nao compartilhe estado mutavel sem sincronizacao
- Nao una a mesma tarefa duas vezes
- Nao envie para canal fechado
- Nao crie funcoes nao-async
- Nao esqueca de unir tarefas (a menos que desanexadas)

---

## Veja Tambem

- [Funcoes Integradas](builtins.md) - `spawn()`, `join()`, `detach()`, `channel()`
- [Sistema de Tipos](type-system.md) - Tipos task e channel
