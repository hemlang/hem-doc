# Operações Atômicas

Hemlock oferece operações atômicas para **programação concorrente lock-free**. Essas operações permitem manipular memória compartilhada com segurança entre múltiplas threads, sem necessidade de locks ou mutexes tradicionais.

## Índice

- [Visão Geral](#visão-geral)
- [Quando Usar Operações Atômicas](#quando-usar-operações-atômicas)
- [Modelo de Memória](#modelo-de-memória)
- [Load e Store Atômicos](#load-e-store-atômicos)
- [Operações Fetch-and-Modify](#operações-fetch-and-modify)
- [Compare-and-Swap (CAS)](#compare-and-swap-cas)
- [Exchange Atômico](#exchange-atômico)
- [Barreiras de Memória](#barreiras-de-memória)
- [Referência de Funções](#referência-de-funções)
- [Padrões Comuns](#padrões-comuns)
- [Melhores Práticas](#melhores-práticas)
- [Limitações](#limitações)

---

## Visão Geral

Operações atômicas são operações **indivisíveis** que completam sem possibilidade de interrupção. Quando uma thread executa uma operação atômica, outras threads não podem observar um estado parcialmente completado da operação.

**Características Principais:**
- Todas as operações usam **consistência sequencial** (`memory_order_seq_cst`)
- Tipos suportados: **i32** e **i64**
- Operações funcionam em ponteiros brutos alocados via `alloc()`
- Garantia de thread-safety sem locks explícitos

**Operações Disponíveis:**
- Load/Store - leitura e escrita atômica de valores
- Add/Sub - operações aritméticas que retornam o valor antigo
- And/Or/Xor - operações bitwise que retornam o valor antigo
- CAS - compare-and-swap para atualizações condicionais
- Exchange - troca atômica de valores
- Fence - barreira de memória completa

---

## Quando Usar Operações Atômicas

**Use operações atômicas para:**
- Contadores compartilhados entre tarefas (ex: contagem de requisições, rastreamento de progresso)
- Flags e indicadores de estado
- Estruturas de dados lock-free
- Primitivas de sincronização simples
- Código concorrente crítico para desempenho

**Use canais em vez disso para:**
- Passar dados complexos entre tarefas
- Implementar padrões produtor-consumidor
- Quando semântica de passagem de mensagens é necessária

**Exemplo de Uso - Contador Compartilhado:**
```hemlock
// Alocar contador compartilhado
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// Criar múltiplos workers
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// Contador será exatamente 3000 (sem corrida de dados)
print(atomic_load_i32(counter));

free(counter);
```

---

## Modelo de Memória

Todas as operações atômicas do Hemlock usam **consistência sequencial** (`memory_order_seq_cst`), fornecendo as garantias mais fortes de ordenação de memória:

1. **Atomicidade**: Cada operação é indivisível
2. **Ordenação Global**: Todas as threads veem a mesma ordem de operações
3. **Sem Reordenação**: Operações não são reordenadas pelo compilador ou CPU

Isso torna o raciocínio sobre código concorrente mais simples, mas pode ter algum custo de desempenho comparado a ordenações de memória mais fracas.

---

## Load e Store Atômicos

### atomic_load_i32 / atomic_load_i64

Lê atomicamente um valor da memória.

**Assinatura:**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**Parâmetros:**
- `ptr` - ponteiro para a localização de memória (deve estar corretamente alinhado)

**Retorna:** O valor na localização de memória

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

Escreve atomicamente um valor na memória.

**Assinatura:**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**Parâmetros:**
- `ptr` - ponteiro para a localização de memória
- `value` - valor a armazenar

**Retorna:** `null`

**Exemplo:**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## Operações Fetch-and-Modify

Essas operações modificam atomicamente um valor e retornam o valor **antigo** (anterior).

### atomic_add_i32 / atomic_add_i64

Adição atômica.

**Assinatura:**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**Retorna:** Valor **antigo** (antes da adição)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100 (valor antigo)
print(atomic_load_i32(p));     // 110 (valor novo)

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

Subtração atômica.

**Assinatura:**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**Retorna:** Valor **antigo** (antes da subtração)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100 (valor antigo)
print(atomic_load_i32(p));     // 75 (valor novo)

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

AND bitwise atômico.

**Assinatura:**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**Retorna:** Valor **antigo** (antes da operação AND)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // Binário 255: 11111111

let old = atomic_and_i32(p, 0x0F);  // AND com 00001111
print(old);                    // 255 (valor antigo)
print(atomic_load_i32(p));     // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

OR bitwise atômico.

**Assinatura:**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**Retorna:** Valor **antigo** (antes da operação OR)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // Binário 15: 00001111

let old = atomic_or_i32(p, 0xF0);  // OR com 11110000
print(old);                    // 15 (valor antigo)
print(atomic_load_i32(p));     // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

XOR bitwise atômico.

**Assinatura:**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**Retorna:** Valor **antigo** (antes da operação XOR)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // Binário 170: 10101010

let old = atomic_xor_i32(p, 0xFF);  // XOR com 11111111
print(old);                    // 170 (valor antigo)
print(atomic_load_i32(p));     // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## Compare-and-Swap (CAS)

A operação atômica mais poderosa. Compara atomicamente o valor atual com um valor esperado e, se coincidirem, substitui pelo novo valor.

### atomic_cas_i32 / atomic_cas_i64

**Assinatura:**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**Parâmetros:**
- `ptr` - ponteiro para a localização de memória
- `expected` - valor que esperamos encontrar
- `desired` - valor a armazenar se expected coincidir

**Retorna:**
- `true` - troca bem-sucedida (valor era `expected`, agora é `desired`)
- `false` - troca falhou (valor não era `expected`, permanece inalterado)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS bem-sucedido: valor é 100, troca para 999
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS falhou: valor é 999, não 100
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999 (inalterado)

free(p);
```

**Casos de Uso:**
- Implementar locks e semáforos
- Estruturas de dados lock-free
- Controle de concorrência otimista
- Atualizações condicionais atômicas

---

## Exchange Atômico

Troca atomicamente valores, retornando o valor antigo.

### atomic_exchange_i32 / atomic_exchange_i64

**Assinatura:**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**Parâmetros:**
- `ptr` - ponteiro para a localização de memória
- `value` - novo valor a armazenar

**Retorna:** Valor **antigo** (antes da troca)

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100 (valor antigo)
print(atomic_load_i32(p));     // 200 (valor novo)

free(p);
```

---

## Barreiras de Memória

Barreira de memória completa, garantindo que todas as operações de memória antes da barreira sejam visíveis para todas as threads antes de qualquer operação após a barreira ser executada.

### atomic_fence

**Assinatura:**
```hemlock
atomic_fence(): null
```

**Retorna:** `null`

**Exemplo:**
```hemlock
// Garantir que todas as escritas anteriores são visíveis para outras threads
atomic_fence();
```

**Nota:** Na maioria dos casos, você não precisa de fences explícitos pois todas as operações atômicas já usam consistência sequencial. Fences são úteis quando você precisa sincronizar operações de memória não-atômicas.

---

## Referência de Funções

### Operações i32

| Função | Assinatura | Retorno | Descrição |
|--------|------------|---------|-----------|
| `atomic_load_i32` | `(ptr)` | `i32` | Carrega valor atomicamente |
| `atomic_store_i32` | `(ptr, value)` | `null` | Armazena valor atomicamente |
| `atomic_add_i32` | `(ptr, value)` | `i32` | Adiciona e retorna valor antigo |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | Subtrai e retorna valor antigo |
| `atomic_and_i32` | `(ptr, value)` | `i32` | AND bitwise e retorna valor antigo |
| `atomic_or_i32` | `(ptr, value)` | `i32` | OR bitwise e retorna valor antigo |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | XOR bitwise e retorna valor antigo |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | Troca e retorna valor antigo |

### Operações i64

| Função | Assinatura | Retorno | Descrição |
|--------|------------|---------|-----------|
| `atomic_load_i64` | `(ptr)` | `i64` | Carrega valor atomicamente |
| `atomic_store_i64` | `(ptr, value)` | `null` | Armazena valor atomicamente |
| `atomic_add_i64` | `(ptr, value)` | `i64` | Adiciona e retorna valor antigo |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | Subtrai e retorna valor antigo |
| `atomic_and_i64` | `(ptr, value)` | `i64` | AND bitwise e retorna valor antigo |
| `atomic_or_i64` | `(ptr, value)` | `i64` | OR bitwise e retorna valor antigo |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | XOR bitwise e retorna valor antigo |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | Compare-and-swap |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | Troca e retorna valor antigo |

### Barreira de Memória

| Função | Assinatura | Retorno | Descrição |
|--------|------------|---------|-----------|
| `atomic_fence` | `()` | `null` | Barreira de memória completa |

---

## Padrões Comuns

### Padrão: Contador Atômico

```hemlock
// Contador thread-safe
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// Uso
increment();  // Retorna 0 (valor antigo)
increment();  // Retorna 1
increment();  // Retorna 2
print(get_count());  // 3

free(counter);
```

### Padrão: Spinlock

```hemlock
// Implementação simples de spinlock
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = desbloqueado, 1 = bloqueado

fn acquire() {
    // Gira até conseguir definir lock de 0 para 1
    while (!atomic_cas_i32(lock, 0, 1)) {
        // Espera ocupada
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// Uso
acquire();
// ... seção crítica ...
release();

free(lock);
```

### Padrão: Inicialização Única

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = não inicializado, 1 = inicializado

fn ensure_initialized() {
    // Tenta ser o inicializador
    if (atomic_cas_i32(initialized, 0, 1)) {
        // Vencemos a corrida, executar inicialização
        do_expensive_init();
    }
    // Caso contrário, já foi inicializado
}
```

### Padrão: Flag Atômica

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // Retorna true se flag já estava definida
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### Padrão: Contador Limitado

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // Máximo atingido
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // Incrementado com sucesso
        }
        // CAS falhou, outra thread modificou o valor - tentar novamente
    }
}
```

---

## Melhores Práticas

### 1. Use Alinhamento Correto

Ponteiros devem estar corretamente alinhados para o tipo de dados:
- i32: alinhamento de 4 bytes
- i64: alinhamento de 8 bytes

Memória de `alloc()` geralmente está corretamente alinhada.

### 2. Prefira Abstrações de Nível Superior

Se possível, use canais para comunicação entre tarefas. Operações atômicas são de nível mais baixo e requerem raciocínio cuidadoso.

```hemlock
// Prefira isto:
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// Em vez de coordenação manual atômica quando apropriado
```

### 3. Cuidado com o Problema ABA

CAS pode sofrer do problema ABA: o valor muda de A para B e depois volta para A. Seu CAS tem sucesso, mas o estado pode ter mudado no meio.

### 4. Inicialize Antes de Compartilhar

Sempre inicialize variáveis atômicas antes de criar tarefas que as acessam:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // Inicializar antes de criar tarefa

let task = spawn(worker, counter);
```

### 5. Libere Após Todas as Tarefas Terminarem

Não libere memória atômica enquanto tarefas ainda podem estar acessando-a:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// Agora seguro para liberar
free(counter);
```

---

## Limitações

### Limitações Atuais

1. **Apenas i32 e i64** - Sem operações atômicas para outros tipos
2. **Sem atômicos de ponteiro** - Não é possível carregar/armazenar ponteiros atomicamente
3. **Apenas consistência sequencial** - Ordenações de memória mais fracas não disponíveis
4. **Sem floats atômicos** - Use representação inteira se necessário

### Notas de Plataforma

- Operações atômicas usam `<stdatomic.h>` do C11 internamente
- Disponível em todas as plataformas que suportam POSIX threads
- Garantidamente lock-free em sistemas modernos de 64 bits

---

## Veja Também

- [Assincronismo/Concorrência](async-concurrency.md) - Criação de tarefas e canais
- [Gerenciamento de Memória](../language-guide/memory.md) - Ponteiros e alocação de buffers
- [API de Memória](../reference/memory-api.md) - Funções de alocação
