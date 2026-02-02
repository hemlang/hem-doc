# Propriedade de Memória no Hemlock

> "Nós te damos as ferramentas para ser seguro, mas não te forçamos a usá-las."

Este documento descreve a semântica de propriedade de memória no Hemlock, cobrindo tanto a memória gerenciada pelo programador quanto os valores gerenciados pelo runtime.

## Índice

1. [O Contrato](#o-contrato)
2. [Memória Gerenciada pelo Programador](#memória-gerenciada-pelo-programador)
3. [Valores Gerenciados pelo Runtime](#valores-gerenciados-pelo-runtime)
4. [Pontos de Transferência de Propriedade](#pontos-de-transferência-de-propriedade)
5. [Async e Concorrência](#async-e-concorrência)
6. [Regras de Memória FFI](#regras-de-memória-ffi)
7. [Segurança de Exceções](#segurança-de-exceções)
8. [Melhores Práticas](#melhores-práticas)

---

## O Contrato

Hemlock tem uma divisão clara de responsabilidade no gerenciamento de memória:

| Tipo de Memória | Gerenciado Por | Método de Limpeza |
|-----------------|----------------|-------------------|
| Ponteiros brutos (`ptr`) | **Programador** | `free(ptr)` |
| Buffers (`buffer`) | **Programador** | `free(buf)` |
| Strings, Arrays, Objetos | **Runtime** | Automático (contagem de referências) |
| Funções, Closures | **Runtime** | Automático (contagem de referências) |
| Tasks, Channels | **Runtime** | Automático (contagem de referências) |

**O princípio central:** Se você aloca explicitamente, você libera explicitamente. Todo o resto é tratado automaticamente.

---

## Memória Gerenciada pelo Programador

### Ponteiros Brutos

```hemlock
let p = alloc(64);       // Alocar 64 bytes
memset(p, 0, 64);        // Inicializar
// ... usar a memória ...
free(p);                 // Sua responsabilidade!
```

**Regras:**
- `alloc()` retorna memória que você possui
- Você deve chamar `free()` quando terminar
- Double-free causará crash (por design)
- Use-after-free é comportamento indefinido
- Aritmética de ponteiros é permitida mas não verificada

### Alocação Tipada

```hemlock
let arr = talloc("i32", 100);  // Alocar 100 i32s (400 bytes)
ptr_write_i32(arr, 0, 42);     // Escrever no índice 0
let val = ptr_read_i32(arr, 0); // Ler do índice 0
free(arr);                      // Ainda é sua responsabilidade
```

### Buffers (Alternativa Segura)

```hemlock
let buf = buffer(64);    // Buffer com verificação de limites
buf[0] = 42;             // Indexação segura
// buf[100] = 1;         // Erro em tempo de execução: fora dos limites
free(buf);               // Ainda precisa de free explícito
```

**Diferença chave:** Buffers fornecem verificação de limites, ponteiros brutos não.

---

## Valores Gerenciados pelo Runtime

### Contagem de Referências

Valores alocados no heap usam contagem de referências atômica:

```hemlock
let s1 = "hello";        // String alocada, refcount = 1
let s2 = s1;             // s2 compartilha s1, refcount = 2
// Quando ambos saem do escopo, refcount → 0, memória liberada
```

**Tipos com contagem de referências:**
- `string` - Texto UTF-8
- `array` - Arrays dinâmicos
- `object` - Objetos chave-valor
- `function` - Closures
- `task` - Handles de tasks async
- `channel` - Canais de comunicação

### Detecção de Ciclos

O runtime trata ciclos em grafos de objetos:

```hemlock
let a = { ref: null };
let b = { ref: a };
a.ref = b;               // Ciclo: a → b → a
// O runtime usa conjuntos visitados para detectar e quebrar ciclos durante a limpeza
```

---

## Pontos de Transferência de Propriedade

### Binding de Variáveis

```hemlock
let x = [1, 2, 3];       // Array criado com refcount 1
                         // x possui a referência
```

### Retornos de Funções

```hemlock
fn make_array() {
    return [1, 2, 3];    // Propriedade do array transferida para o chamador
}
let arr = make_array();  // arr agora possui a referência
```

### Atribuição

```hemlock
let a = "hello";
let b = a;               // Referência compartilhada (refcount incrementado)
b = "world";             // a ainda tem "hello", b tem "world"
```

### Operações de Channel

```hemlock
let ch = channel(10);
ch.send("message");      // Valor copiado para o buffer do channel
                         // Original ainda válido

let msg = ch.recv();     // Recebe propriedade do channel
```

### Spawning de Tasks

```hemlock
let data = { x: 1 };
let task = spawn(worker, data);  // data é COPIADO PROFUNDAMENTE para isolamento
data.x = 2;                       // Seguro - task tem sua própria cópia
let result = join(task);          // Propriedade do result transferida para o chamador
```

---

## Async e Concorrência

### Isolamento de Threads

Tasks spawnadas recebem **cópias profundas** de argumentos mutáveis:

```hemlock
async fn worker(data) {
    data.x = 100;        // Modifica apenas a cópia do task
    return data;
}

let obj = { x: 1 };
let task = spawn(worker, obj);
obj.x = 2;               // Seguro - não afeta o task
let result = join(task);
print(obj.x);            // 2 (não alterado pelo task)
print(result.x);         // 100 (cópia modificada do task)
```

### Objetos de Coordenação Compartilhados

Alguns tipos são compartilhados por referência (não copiados):
- **Channels** - Para comunicação entre tasks
- **Tasks** - Para coordenação (join/detach)

```hemlock
let ch = channel(1);
spawn(producer, ch);     // Mesmo channel, não uma cópia
spawn(consumer, ch);     // Ambos os tasks compartilham o channel
```

### Resultados de Tasks

```hemlock
let task = spawn(compute);
let result = join(task);  // Chamador possui o resultado
                          // Referência do task é liberada quando o task é liberado
```

### Tasks Desacopladas

```hemlock
detach(spawn(background_work));
// Task roda independentemente
// Resultado é liberado automaticamente quando o task completa
// Sem leak mesmo que ninguém chame join()
```

---

## Regras de Memória FFI

### Passando para Funções C

```hemlock
extern fn strlen(s: string): i32;

let s = "hello";
let len = strlen(s);     // Hemlock retém a propriedade
                         // String é válida durante a chamada
                         // Função C NÃO deve liberá-la
```

### Recebendo de Funções C

```hemlock
extern fn strdup(s: string): ptr;

let copy = strdup("hello");  // C alocou esta memória
free(copy);                   // Sua responsabilidade liberar
```

### Passagem de Structs (Apenas Compilador)

```hemlock
// Definir layout de struct C
ffi_struct Point { x: f64, y: f64 }

extern fn make_point(x: f64, y: f64): Point;

let p = make_point(1.0, 2.0);  // Retornado por valor, copiado
                                // Não precisa de limpeza para structs na stack
```

### Memória de Callbacks

```hemlock
// Quando C chama de volta para Hemlock:
// - Argumentos pertencem a C (não liberar)
// - Propriedade do valor de retorno transferida para C
```

---

## Segurança de Exceções

### Garantias

O runtime fornece estas garantias:

1. **Sem leak em saída normal** - Todos os valores gerenciados pelo runtime são limpos
2. **Sem leak em exceção** - Temporários são liberados durante o stack unwinding
3. **Defer executa em exceção** - Código de limpeza é executado

### Avaliação de Expressões

```hemlock
// Se isso lançar durante a criação do array:
let arr = [f(), g(), h()];  // Array parcial é liberado

// Se isso lançar durante a chamada de função:
foo(a(), b(), c());         // Args previamente avaliados são liberados
```

### Defer para Limpeza

```hemlock
fn process_file() {
    let f = open("data.txt", "r");
    defer f.close();         // Executa no return OU exceção

    let data = f.read();
    if (data == "") {
        throw "Empty file";  // f.close() ainda executa!
    }
    return data;
}
```

---

## Melhores Práticas

### 1. Prefira Tipos Gerenciados pelo Runtime

```hemlock
// Prefira isto:
let data = [1, 2, 3, 4, 5];

// A isto (a menos que precise de controle de baixo nível):
let data = talloc("i32", 5);
// ... deve lembrar de liberar ...
```

### 2. Use Defer para Memória Manual

```hemlock
fn process() {
    let buf = alloc(1024);
    defer free(buf);        // Limpeza garantida

    // ... usar buf ...
    // Não precisa liberar em cada ponto de retorno
}
```

### 3. Evite Ponteiros Brutos em Async

```hemlock
// ERRADO - ponteiro pode ser liberado antes do task completar
let p = alloc(64);
spawn(worker, p);          // Task obtém o valor do ponteiro
free(p);                   // Ops! Task ainda está usando

// CERTO - use channels ou copie os dados
let ch = channel(1);
let data = buffer(64);
// ... preencher data ...
ch.send(data);             // Cópia profunda
spawn(worker, ch);
free(data);                // Seguro - task tem sua própria cópia
```

### 4. Feche Channels Quando Terminar

```hemlock
let ch = channel(10);
// ... usar channel ...
ch.close();                // Drena e libera valores no buffer
```

### 5. Join ou Detach Tasks

```hemlock
let task = spawn(work);

// Opção 1: Esperar o resultado
let result = join(task);

// Opção 2: Fire and forget
// detach(task);

// NÃO: Deixar o handle do task sair do escopo sem join ou detach
// (Será limpo, mas o resultado pode ter leak)
```

---

## Depuração de Problemas de Memória

### Habilitar ASAN

```bash
make asan
ASAN_OPTIONS=detect_leaks=1 ./hemlock script.hml
```

### Executar Testes de Regressão de Leaks

```bash
make leak-regression       # Suite completa
make leak-regression-quick # Pular teste exaustivo
```

### Valgrind

```bash
make valgrind-check FILE=script.hml
```

---

## Resumo

| Operação | Comportamento de Memória |
|----------|-------------------------|
| `alloc(n)` | Aloca, você libera |
| `buffer(n)` | Aloca com verificação de limites, você libera |
| `"string"` | Runtime gerencia |
| `[array]` | Runtime gerencia |
| `{object}` | Runtime gerencia |
| `spawn(fn)` | Copia profundamente args, runtime gerencia task |
| `join(task)` | Chamador possui resultado |
| `detach(task)` | Runtime libera resultado quando terminado |
| `ch.send(v)` | Copia valor para o channel |
| `ch.recv()` | Chamador possui valor recebido |
| `ch.close()` | Drena e libera valores no buffer |
