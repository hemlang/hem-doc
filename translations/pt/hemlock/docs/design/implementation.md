# Detalhes de Implementação do Hemlock

Este documento descreve a implementação técnica da linguagem Hemlock, incluindo estrutura do projeto, pipeline de compilação, arquitetura de runtime e decisões de design.

---

## Sumário

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pipeline de Compilação](#pipeline-de-compilação)
- [Design Modular do Interpretador](#design-modular-do-interpretador)
- [Arquitetura de Runtime](#arquitetura-de-runtime)
- [Representação de Valores](#representação-de-valores)
- [Implementação do Sistema de Tipos](#implementação-do-sistema-de-tipos)
- [Gerenciamento de Memória](#gerenciamento-de-memória)
- [Modelo de Concorrência](#modelo-de-concorrência)
- [Planos Futuros](#planos-futuros)

---

## Estrutura do Projeto

```
hemlock/
├── src/
│   ├── frontend/              # Compartilhado: lexer, parser, AST
│   │   ├── lexer.c            # Análise léxica
│   │   ├── parser/            # Parser descendente recursivo
│   │   ├── ast.c              # Gerenciamento de nós AST
│   │   └── module.c           # Resolução de módulos
│   ├── backends/
│   │   ├── interpreter/       # hemlock: interpretador tree-walking
│   │   │   ├── main.c         # Ponto de entrada CLI
│   │   │   ├── runtime.c      # Avaliação de expressões/statements
│   │   │   ├── builtins.c     # Funções builtin
│   │   │   └── ...
│   │   └── compiler/          # hemlockc: gerador de código C
│   │       ├── main.c         # CLI, orquestração
│   │       ├── type_check.c   # Verificação de tipos em compile-time
│   │       ├── codegen.c      # Contexto de geração de código
│   │       ├── codegen_expr.c # Geração de código para expressões
│   │       ├── codegen_stmt.c # Geração de código para statements
│   │       └── ...
│   ├── tools/
│   │   ├── lsp/               # Protocolo Language Server
│   │   └── bundler/           # Ferramenta de bundling/pacotes
├── runtime/                   # libhemlock_runtime.a (para programas compilados)
├── stdlib/                    # Biblioteca padrão (39 módulos)
│   └── docs/                  # Documentação dos módulos
├── tests/
│   ├── parity/                # Testes que devem passar em ambos backends
│   ├── interpreter/           # Testes específicos do interpretador
│   └── compiler/              # Testes específicos do compilador
├── examples/                  # Programas de exemplo
└── docs/                      # Documentação
```

### Organização de Diretórios

**`include/`** - Headers de API pública que definem interfaces entre componentes:
- Separação clara entre lexer, parser, AST e interpretador
- Declarações forward para minimizar dependências
- API pública para incorporar Hemlock em outros programas

**`src/`** - Arquivos de implementação:
- Arquivos de nível superior tratam lexing, parsing, gerenciamento de AST
- `main.c` fornece CLI e REPL
- Interpretador modularizado em subsistemas independentes

**`src/interpreter/`** - Implementação modular do interpretador:
- Cada módulo tem uma única responsabilidade clara
- APIs internas definidas em `internal.h` para comunicação entre módulos
- Módulos podem ser compilados independentemente para builds mais rápidos

**`tests/`** - Suíte de testes abrangente:
- Organizada por área funcional
- Cada diretório contém casos de teste focados
- `run_tests.sh` orquestra execução de testes

---

## Pipeline de Compilação

Hemlock usa um pipeline de compilação tradicional com fases distintas:

### Fase 1: Análise Léxica (Lexer)

**Entrada:** Texto do código fonte
**Saída:** Stream de tokens
**Implementação:** `src/lexer.c`

```
Fonte: "let x = 42;"
   ↓
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
```

**Recursos principais:**
- Reconhece palavras-chave, identificadores, literais, operadores, pontuação
- Trata literais de string UTF-8 e literais de rune
- Reporta números de linha para mensagens de erro
- Passagem única, sem backtracking

### Fase 2: Análise Sintática (Parser)

**Entrada:** Stream de tokens
**Saída:** Árvore Sintática Abstrata (AST)
**Implementação:** `src/parser.c`

```
Tokens: [LET, IDENTIFIER("x"), EQUALS, INTEGER(42), SEMICOLON]
   ↓
AST: LetStmt {
    name: "x",
    type: null,
    value: IntLiteral(42)
}
```

**Recursos principais:**
- Parser descendente recursivo
- Constrói representação em árvore da estrutura do programa
- Trata precedência de operadores
- Valida sintaxe (chaves, ponto e vírgula, etc.)
- Sem análise semântica ainda (feita em tempo de execução)

**Precedência de Operadores (da mais baixa para a mais alta):**
1. Atribuição: `=`
2. Ou lógico: `||`
3. E lógico: `&&`
4. Ou bit a bit: `|`
5. Xor bit a bit: `^`
6. E bit a bit: `&`
7. Igualdade: `==`, `!=`
8. Comparação: `<`, `>`, `<=`, `>=`
9. Shift: `<<`, `>>`
10. Adição/Subtração: `+`, `-`
11. Multiplicação/Divisão/Módulo: `*`, `/`, `%`
12. Unário: `!`, `-`, `~`
13. Chamada/Índice/Membro: `()`, `[]`, `.`

### Fase 3a: Execução Interpretada (Tree-Walking)

**Entrada:** AST
**Saída:** Execução do programa
**Implementação:** `src/backends/interpreter/runtime.c`

```
AST: LetStmt { ... }
   ↓
Execução: Avaliar nós AST recursivamente
   ↓
Resultado: Criar variável x com valor 42
```

**Recursos principais:**
- Travessia direta de AST (interpretador tree-walking)
- Verificação de tipos dinâmica em tempo de execução
- Armazenamento de variáveis baseado em ambiente

### Fase 3b: Compilação (hemlockc)

**Entrada:** AST
**Saída:** Executável nativo via geração de código C
**Implementação:** `src/backends/compiler/`

```
AST: LetStmt { ... }
   ↓
Verificação de Tipos: Validar tipos em compile-time
   ↓
Geração de Código C: Gerar código C equivalente
   ↓
GCC: Compilar C para binário nativo
   ↓
Resultado: Executável standalone
```

**Recursos principais:**
- Verificação de tipos em compile-time (habilitada por padrão)
- Geração de código C para portabilidade
- Linka com `libhemlock_runtime.a`
- Execução significativamente mais rápida que interpretador

---

## Backend do Compilador (hemlockc)

O compilador Hemlock gera código C a partir do AST, que é então compilado para executável nativo usando GCC.

### Arquitetura do Compilador

```
src/backends/compiler/
├── main.c              # CLI, parsing de argumentos, orquestração
├── codegen.c           # Contexto core de geração de código
├── codegen_expr.c      # Geração de código para expressões
├── codegen_stmt.c      # Geração de código para statements
├── codegen_call.c      # Geração de chamadas de função
├── codegen_closure.c   # Implementação de closures
├── codegen_program.c   # Geração de programa de nível superior
├── codegen_module.c    # Tratamento de módulos/imports
├── type_check.c        # Verificação de tipos em compile-time
└── type_check.h        # API do type checker
```

### Verificação de Tipos

O compilador inclui um sistema unificado de verificação de tipos que pode:

1. **Validar tipos em compile-time** - Capturar erros de tipo antes da execução
2. **Suportar código dinâmico** - Código sem tipos é tratado como `any` (sempre válido)
3. **Fornecer dicas de otimização** - Identificar variáveis que podem ser unboxed

**Flags de verificação de tipos:**

| Flag | Descrição |
|------|-----------|
| (padrão) | Verificação de tipos habilitada |
| `--check` | Apenas verificar tipos, não compilar |
| `--no-type-check` | Desabilitar verificação de tipos |
| `--strict-types` | Avisar sobre tipos `any` implícitos |

**Implementação do Type Checker:**

```c
// type_check.h - Estruturas principais
typedef struct TypeCheckContext {
    const char *filename;
    int error_count;
    int warning_count;
    UnboxableVar *unboxable_vars;  // Dicas de otimização
    // ... ambiente de tipos, definições, etc
} TypeCheckContext;

// Ponto de entrada principal
int type_check_program(TypeCheckContext *ctx, Stmt **stmts, int count);
```

### Geração de Código

A fase de geração de código transforma nós AST em código C:

**Mapeamento de Expressões:**
```
Hemlock                 →  C Gerado
----------------------------------------
let x = 42;            →  HmlValue x = hml_val_i32(42);
x + y                  →  hml_add(x, y)
arr[i]                 →  hml_array_get(arr, i)
obj.field              →  hml_object_get_field(obj, "field")
fn(a, b) { ... }       →  closure com captura de ambiente
```

**Integração com Runtime:**

O código C gerado linka com `libhemlock_runtime.a`, que fornece:
- Tipo `HmlValue` tagged union
- Gerenciamento de memória (contagem de referência)
- Funções builtin (print, typeof, etc.)
- Primitivas de concorrência (tasks, channels)
- Suporte FFI

### Otimização de Unboxing

O type checker identifica variáveis que podem usar tipos C nativos ao invés de `HmlValue` boxed:

**Padrões unboxáveis:**
- Contadores de loop com tipo inteiro conhecido
- Variáveis acumuladoras em loops
- Variáveis com anotações de tipo explícitas (i32, i64, f64, bool)

```hemlock
// Contador de loop 'i' pode ser unboxed para int32_t nativo
for (let i: i32 = 0; i < 1000000; i = i + 1) {
    sum = sum + i;
}
```

---

## Design Modular do Interpretador

O interpretador é dividido em módulos focados para melhor manutenibilidade e extensibilidade.

### Responsabilidades dos Módulos

#### 1. Ambiente (`environment.c`) - 121 linhas

**Propósito:** Escopo de variáveis e resolução de nomes

**Funções principais:**
- `env_create()` - Criar novo ambiente com pai opcional
- `env_define()` - Definir nova variável no escopo atual
- `env_get()` - Buscar variável no escopo atual ou pai
- `env_set()` - Atualizar valor de variável existente
- `env_free()` - Liberar ambiente e todas as variáveis

**Design:**
- Escopos encadeados (cada ambiente tem ponteiro para pai)
- HashMap para busca rápida de variáveis
- Suporta escopo léxico para closures

#### 2. Valores (`values.c`) - 394 linhas

**Propósito:** Construtores de valores e gerenciamento de estruturas de dados

**Funções principais:**
- `value_create_*()` - Construtores para cada tipo de valor
- `value_copy()` - Lógica de cópia profunda/rasa
- `value_free()` - Limpeza e liberação de memória
- `value_to_string()` - Representação em string para impressão

**Estruturas de dados:**
- Objetos (array dinâmico de campos)
- Arrays (redimensionamento dinâmico)
- Buffers (ptr + length + capacity)
- Closures (função + ambiente capturado)
- Tasks e Channels (primitivas de concorrência)

#### 3. Tipos (`types.c`) - 440 linhas

**Propósito:** Sistema de tipos, conversões e duck typing

**Funções principais:**
- `type_check()` - Validação de tipos em tempo de execução
- `type_convert()` - Conversão/promoção de tipos implícita
- `duck_type_check()` - Verificação de tipos estruturais para objetos
- `type_name()` - Obter nome do tipo para impressão

**Recursos:**
- Hierarquia de promoção de tipos (i8 → i16 → i32 → i64 → f32 → f64, i64/u64 + f32 → f64)
- Verificação de intervalo para tipos numéricos
- Duck typing para definições de tipo de objeto
- Valores padrão para campos opcionais

#### 4. Builtins (`builtins.c`) - 955 linhas

**Propósito:** Funções builtin e registro global

**Funções principais:**
- `register_builtins()` - Registrar todas as funções e constantes builtin
- Implementações de funções builtin (print, typeof, alloc, free, etc.)
- Funções de tratamento de sinais
- Execução de comandos (exec)

**Categorias de builtins:**
- I/O: print, open, read_file, write_file
- Memória: alloc, free, memset, memcpy, realloc
- Tipos: typeof, assert
- Concorrência: spawn, join, detach, channel
- Sistema: exec, signal, raise, panic
- FFI: dlopen, dlsym, dlcall, dlclose

#### 5. I/O (`io.c`) - 449 linhas

**Propósito:** I/O de arquivos e serialização JSON

**Funções principais:**
- Métodos de objeto File (read, write, seek, tell, close)
- Serialização/deserialização JSON
- Detecção de referência circular

**Recursos:**
- Objetos file com atributos (path, mode, closed)
- I/O de texto com awareness de UTF-8
- Suporte a I/O binário
- Roundtrip JSON para objetos e arrays

#### 6. FFI (`ffi.c`) - Interface de Função Estrangeira

**Propósito:** Chamar funções C de bibliotecas compartilhadas

**Funções principais:**
- `dlopen()` - Carregar biblioteca compartilhada
- `dlsym()` - Obter ponteiro de função por nome
- `dlcall()` - Chamar função C com conversão de tipos
- `dlclose()` - Descarregar biblioteca

**Recursos:**
- Integração com libffi para chamadas de função dinâmicas
- Conversão automática de tipos (Hemlock ↔ tipos C)
- Suporte para todos os tipos primitivos
- Suporte para ponteiros e buffers

#### 7. Runtime (`runtime.c`) - 865 linhas

**Propósito:** Avaliação de expressões e execução de statements

**Funções principais:**
- `eval_expr()` - Avaliar expressões (recursivo)
- `eval_stmt()` - Executar statements
- Tratamento de fluxo de controle (if, while, for, switch, etc.)
- Tratamento de exceções (try/catch/finally/throw)

**Recursos:**
- Avaliação recursiva de expressões
- Avaliação short-circuit de booleanos
- Detecção de chamada de método e binding de `self`
- Propagação de exceções
- Tratamento de break/continue/return

### Benefícios do Design Modular

**1. Separação de Concerns**
- Cada módulo tem uma responsabilidade clara
- Fácil encontrar onde um recurso está implementado
- Reduz carga cognitiva ao fazer mudanças

**2. Builds Incrementais Mais Rápidos**
- Apenas módulos modificados precisam ser recompilados
- Compilação paralela possível
- Tempo de iteração mais curto durante desenvolvimento

**3. Testes e Debug Mais Fáceis**
- Módulos podem ser testados independentemente
- Erros localizados em subsistemas específicos
- Implementações mock possíveis para testes

**4. Extensibilidade**
- Novos recursos podem ser adicionados aos módulos apropriados
- Módulos podem ser refatorados independentemente
- Quantidade de código por arquivo permanece gerenciável

**5. Organização de Código**
- Agrupamento lógico de funcionalidades relacionadas
- Grafo de dependências claro
- Mais fácil de onboarding para novos contribuidores

---

## Arquitetura de Runtime

### Representação de Valores

Todos os valores em Hemlock são representados pela struct `Value` usando tagged union:

```c
typedef struct Value {
    ValueType type;  // Tag de tipo em runtime
    union {
        int32_t i32_value;
        int64_t i64_value;
        uint8_t u8_value;
        uint32_t u32_value;
        uint64_t u64_value;
        float f32_value;
        double f64_value;
        bool bool_value;
        char *string_value;
        uint32_t rune_value;
        void *ptr_value;
        Buffer *buffer_value;
        Array *array_value;
        Object *object_value;
        Function *function_value;
        File *file_value;
        Task *task_value;
        Channel *channel_value;
    };
} Value;
```

**Decisões de design:**
- **Tagged union** para type safety mantendo flexibilidade
- **Tag de tipo em runtime** habilita tipagem dinâmica com verificação de tipos
- **Armazenamento direto de valores** para tipos primitivos (sem boxing)
- **Armazenamento de ponteiros** para tipos alocados em heap (strings, objetos, arrays)

### Exemplos de Layout de Memória

**Inteiro (i32):**
```
Value {
    type: TYPE_I32,
    i32_value: 42
}
```
- Tamanho total: ~16 bytes (8 bytes tag + 8 bytes union)
- Alocado em stack
- Não requer alocação em heap

**String:**
```
Value {
    type: TYPE_STRING,
    string_value: 0x7f8a4c000000  // Ponteiro para heap
}

Heap: "hello\0" (6 bytes, UTF-8 terminado em null)
```
- Value ocupa 16 bytes em stack
- Dados da string são alocados em heap
- Deve ser liberado manualmente

**Objeto:**
```
Value {
    type: TYPE_OBJECT,
    object_value: 0x7f8a4c001000  // Ponteiro para heap
}

Heap: Object {
    type_name: "Person",
    fields: [
        { name: "name", value: Value{TYPE_STRING, "Alice"} },
        { name: "age", value: Value{TYPE_I32, 30} }
    ],
    field_count: 2,
    capacity: 4
}
```
- Estrutura Object em heap
- Campos armazenados em array dinâmico
- Valores de campos são structs Value embutidas

### Implementação de Ambiente

Variáveis são armazenadas em cadeia de ambientes:

```c
typedef struct Environment {
    HashMap *bindings;           // nome → Value
    struct Environment *parent;  // Escopo pai léxico
} Environment;
```

**Exemplo de cadeia de escopo:**
```
Escopo Global: { print: <builtin>, args: <array> }
    ↑
Escopo de Função: { x: 10, y: 20 }
    ↑
Escopo de Bloco: { i: 0 }
```

**Algoritmo de busca:**
1. Verificar hashmap do ambiente atual
2. Se não encontrado, verificar ambiente pai
3. Repetir até encontrar ou alcançar escopo global
4. Erro se não encontrado em nenhum escopo

---

## Implementação do Sistema de Tipos

### Estratégia de Verificação de Tipos

Hemlock usa **verificação de tipos em runtime** com **anotações de tipo opcionais**:

```hemlock
let x = 42;           // Sem verificação de tipo, inferido como i32
let y: u8 = 255;      // Verificação runtime: valor deve caber em u8
let z: i32 = x + y;   // Verificação runtime + promoção de tipo
```

**Fluxo de implementação:**
1. **Inferência de literal** - Lexer/parser determina tipo inicial do literal
2. **Verificação de anotação** - Se anotação presente, validar na atribuição
3. **Promoção** - Operações binárias promovem para tipo comum
4. **Conversão** - Conversões explícitas acontecem conforme necessário

### Implementação de Promoção de Tipos

A promoção de tipos segue hierarquia fixa e preserva precisão:

```c
// Lógica simplificada de promoção
ValueType promote_types(ValueType a, ValueType b) {
    // f64 sempre vence
    if (a == TYPE_F64 || b == TYPE_F64) return TYPE_F64;

    // f32 com i64/u64 promove para f64 (preservação de precisão)
    if (a == TYPE_F32 || b == TYPE_F32) {
        ValueType other = (a == TYPE_F32) ? b : a;
        if (other == TYPE_I64 || other == TYPE_U64) return TYPE_F64;
        return TYPE_F32;
    }

    // Tipo inteiro maior vence
    int rank_a = get_type_rank(a);
    int rank_b = get_type_rank(b);
    return (rank_a > rank_b) ? a : b;
}
```

**Ranks de tipo:**
- i8: 0
- u8: 1
- i16: 2
- u16: 3
- i32: 4
- u32: 5
- i64: 6
- u64: 7
- f32: 8
- f64: 9

### Implementação de Duck Typing

Verificação de tipos de objeto usa comparação estrutural:

```c
bool duck_type_check(Object *obj, TypeDef *type_def) {
    // Verificar todos os campos requeridos
    for (each field in type_def) {
        if (!object_has_field(obj, field.name)) {
            return false;  // Campo faltando
        }

        Value *field_value = object_get_field(obj, field.name);
        if (!type_matches(field_value, field.type)) {
            return false;  // Tipo errado
        }
    }

    return true;  // Todos os campos requeridos presentes e tipados corretamente
}
```

**Duck typing permite:**
- Campos extras em objetos (ignorados)
- Tipos de subestrutura (objetos podem ter mais do que requerido)
- Atribuição de nome de tipo após validação

---

## Gerenciamento de Memória

### Estratégia de Alocação

Hemlock usa **gerenciamento manual de memória** com duas primitivas de alocação:

**1. Ponteiros Brutos (`ptr`):**
```c
void *alloc(size_t bytes) {
    void *ptr = malloc(bytes);
    if (!ptr) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }
    return ptr;
}
```
- malloc/free direto
- Sem rastreamento
- Usuário responsável pela liberação

**2. Buffers (`buffer`):**
```c
typedef struct Buffer {
    void *data;
    size_t length;
    size_t capacity;
} Buffer;

Buffer *create_buffer(size_t size) {
    Buffer *buf = malloc(sizeof(Buffer));
    buf->data = malloc(size);
    buf->length = size;
    buf->capacity = size;
    return buf;
}
```
- Rastreia tamanho e capacidade
- Verificação de limites em acesso
- Ainda requer free manual

### Tipos Alocados em Heap

**Strings:**
- Array de bytes UTF-8 em heap
- Terminada em null para interop com C
- Mutáveis (podem ser modificadas in-place)
- Contagem de referência (liberadas automaticamente ao sair do escopo)

**Objetos:**
- Array dinâmico de campos
- Nomes e valores de campos em heap
- Contagem de referência (liberados automaticamente ao sair do escopo)
- Referências circulares possíveis (tratadas com visited-set tracking)

**Arrays:**
- Capacidade dinâmica com crescimento por dobra
- Elementos são structs Value embutidas
- Realocação automática em crescimento
- Contagem de referência (liberados automaticamente ao sair do escopo)

**Closures:**
- Capturam ambiente por referência
- Ambiente é alocado em heap
- Ambiente de closure liberado corretamente quando não mais referenciado

---

## Modelo de Concorrência

### Arquitetura de Threads

Hemlock usa modelo de **threads 1:1** com threads POSIX (pthreads):

```
Tasks de Usuário       Threads SO           Núcleos CPU
--------------         ----------           -----------
spawn(f1) ------>  pthread_create --> Core 0
spawn(f2) ------>  pthread_create --> Core 1
spawn(f3) ------>  pthread_create --> Core 2
```

**Características principais:**
- Cada `spawn()` cria um novo pthread
- Kernel agenda threads entre cores
- Execução paralela real (sem GIL)
- Multitarefa preemptiva

### Implementação de Tasks

```c
typedef struct Task {
    pthread_t thread;        // Handle da thread SO
    Value result;            // Valor de retorno
    char *error;             // Mensagem de exceção (se lançada)
    pthread_mutex_t lock;    // Protege estado
    TaskState state;         // RUNNING, FINISHED, ERROR
} Task;
```

**Ciclo de vida da task:**
1. `spawn(func, args)` → Cria Task, inicia pthread
2. Thread executa função com argumentos
3. No retorno: armazena resultado, define estado para FINISHED
4. Na exceção: armazena mensagem de erro, define estado para ERROR
5. `join(task)` → Espera thread, retorna resultado ou lança exceção

### Implementação de Channels

```c
typedef struct Channel {
    void **buffer;           // Buffer circular de Value*
    size_t capacity;         // Máximo de itens no buffer
    size_t count;            // Itens atuais no buffer
    size_t read_index;       // Próxima posição de leitura
    size_t write_index;      // Próxima posição de escrita
    bool closed;             // Flag de channel fechado
    pthread_mutex_t lock;    // Protege buffer
    pthread_cond_t not_full; // Sinaliza quando há espaço
    pthread_cond_t not_empty;// Sinaliza quando há dados
} Channel;
```

**Operação de envio:**
1. Trava mutex
2. Se buffer cheio espera (cond_wait em not_full)
3. Escreve valor em buffer[write_index]
4. Incrementa write_index (circular)
5. Sinaliza not_empty
6. Destrava mutex

**Operação de recebimento:**
1. Trava mutex
2. Se buffer vazio espera (cond_wait em not_empty)
3. Lê valor de buffer[read_index]
4. Incrementa read_index (circular)
5. Sinaliza not_full
6. Destrava mutex

**Garantias de sincronização:**
- Send/recv thread-safe (protegidos por mutex)
- Semântica bloqueante (produtor espera quando cheio, consumidor espera quando vazio)
- Entrega ordenada (FIFO dentro do channel)

---

## Planos Futuros

### Concluído: Backend do Compilador

O backend do compilador (`hemlockc`) está implementado:
- Geração de código C a partir do AST
- Verificação de tipos em compile-time (habilitada por padrão)
- Biblioteca de runtime (`libhemlock_runtime.a`)
- Paridade total com interpretador (98% taxa de aprovação em testes)
- Framework de otimização de unboxing

### Foco Atual: Melhorias no Sistema de Tipos

**Melhorias recentes:**
- Sistema unificado de verificação e inferência de tipos
- Verificação de tipos em compile-time habilitada por padrão
- Flag `--check` para validação apenas de tipos
- Contexto de tipos passado para geração de código para dicas de otimização

### Melhorias Futuras

**Possíveis adições:**
- Generics/templates
- Pattern matching
- Integração LSP para suporte de IDE com awareness de tipos
- Otimizações de unboxing mais agressivas
- Análise de escape para alocação em stack

### Otimizações de Longo Prazo

**Possíveis melhorias:**
- Cache inline para chamadas de método
- Compilação JIT para caminhos de código quentes
- Scheduler work-stealing para melhor concorrência
- Otimização guiada por profile

---

## Diretrizes de Implementação

### Adicionando Novos Recursos

Ao implementar novos recursos, siga estas diretrizes:

**1. Escolha o módulo correto:**
- Novos tipos de valor → `values.c`
- Conversões de tipo → `types.c`
- Funções builtin → `builtins.c`
- Operações I/O → `io.c`
- Fluxo de controle → `runtime.c`

**2. Atualize todas as camadas:**
- Adicione tipo de nó AST se necessário (`ast.h`, `ast.c`)
- Adicione token do lexer se necessário (`lexer.c`)
- Adicione regras do parser (`parser.c`)
- Implemente comportamento runtime (`runtime.c` ou módulo apropriado)
- Adicione testes (`tests/`)

**3. Mantenha consistência:**
- Siga estilo de código existente
- Use convenções de nomenclatura consistentes
- Documente APIs públicas em headers
- Mantenha mensagens de erro claras e consistentes

**4. Teste completamente:**
- Adicione casos de teste antes de implementar
- Teste caminhos de sucesso e erro
- Teste casos de borda
- Verifique que não há vazamentos de memória (valgrind)

### Considerações de Performance

**Gargalos atuais:**
- Busca em HashMap para acesso a variáveis
- Chamadas de função recursivas (sem TCO)
- Concatenação de strings (aloca nova string cada vez)
- Overhead de verificação de tipo por operação

**Oportunidades de otimização:**
- Cache de localização de variáveis (cache inline)
- Otimização de tail call
- String builder para concatenação
- Inferência de tipos para pular verificações runtime

### Dicas de Debug

**Ferramentas úteis:**
- `valgrind` - Detecção de vazamento de memória
- `gdb` - Debug de crashes
- Flag `-g` - Símbolos de debug
- Debug com `printf` - Simples mas efetivo

**Problemas comuns:**
- Segfault → Desreferência de ponteiro nulo (verifique valores de retorno)
- Vazamento de memória → Chamada free() faltando (verifique caminhos de value_free)
- Erros de tipo → Verifique lógica de type_convert() e type_check()
- Crash em thread → Condição de corrida (verifique uso de mutex)

---

## Resumo

A implementação do Hemlock prioriza:
- **Modularidade** - Separação clara de concerns
- **Simplicidade** - Implementação direta
- **Explicitude** - Sem mágica oculta
- **Manutenibilidade** - Fácil de entender e modificar

O interpretador tree-walking atual é intencionalmente simples para facilitar desenvolvimento rápido de recursos e experimentação. O backend do compilador futuro melhorará performance mantendo a mesma semântica.
