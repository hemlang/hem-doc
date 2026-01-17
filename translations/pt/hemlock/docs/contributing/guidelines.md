# Diretrizes de Contribuição do Hemlock

Obrigado pelo seu interesse em contribuir para o Hemlock! Este guia ajudará você a entender como contribuir código de forma efetiva, mantendo a filosofia de design e qualidade de código da linguagem.

---

## Sumário

- [Antes de Começar](#antes-de-começar)
- [Fluxo de Trabalho de Contribuição](#fluxo-de-trabalho-de-contribuição)
- [Guia de Estilo de Código](#guia-de-estilo-de-código)
- [O que Contribuir](#o-que-contribuir)
- [O que Não Contribuir](#o-que-não-contribuir)
- [Padrões Comuns](#padrões-comuns)
- [Adicionando Novos Recursos](#adicionando-novos-recursos)
- [Processo de Code Review](#processo-de-code-review)

---

## Antes de Começar

### Documentação Obrigatória

Antes de contribuir, por favor leia os seguintes documentos na ordem:

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Entender os princípios centrais do Hemlock
2. **`/home/user/hemlock/docs/design/implementation.md`** - Aprender a estrutura do código
3. **`/home/user/hemlock/docs/contributing/testing.md`** - Entender os requisitos de teste
4. **Este documento** - Aprender as diretrizes de contribuição

### Pré-requisitos

**Conhecimento necessário:**
- Programação C (ponteiros, gerenciamento de memória, structs)
- Fundamentos de compiladores/interpretadores (análise léxica, sintática, AST)
- Fluxo de trabalho Git e GitHub
- Linha de comando Unix/Linux

**Ferramentas necessárias:**
- Compilador GCC ou Clang
- Sistema de build Make
- Controle de versão Git
- Valgrind (para detecção de vazamento de memória)
- Editor de texto ou IDE básico

### Canais de Comunicação

**Onde perguntar:**
- GitHub Issues - Relatórios de bug e solicitações de recursos
- GitHub Discussions - Perguntas gerais e discussões de design
- Comentários em Pull Request - Feedback específico de código

---

## Fluxo de Trabalho de Contribuição

### 1. Encontrar ou Criar uma Issue

**Antes de escrever código:**
- Verificar se já existe uma issue relacionada à sua contribuição
- Se não existir, criar uma issue descrevendo o que você quer fazer
- Esperar feedback dos mantenedores antes de começar grandes mudanças
- Pequenas correções de bugs podem pular esta etapa

**Uma boa descrição de issue inclui:**
- Declaração do problema (o que está quebrado ou faltando)
- Solução proposta (como você planeja corrigir)
- Exemplos (trechos de código mostrando o problema)
- Justificativa (por que esta mudança está alinhada com a filosofia do Hemlock)

### 2. Fork e Clone

```bash
# Primeiro faça fork do repositório no GitHub, então:
git clone https://github.com/SEU_USUARIO/hemlock.git
cd hemlock
git checkout -b feature/nome-do-seu-recurso
```

### 3. Fazer Mudanças

Siga estas diretrizes:
- Escrever testes primeiro (abordagem TDD)
- Implementar o recurso
- Garantir que todos os testes passem
- Verificar vazamentos de memória
- Atualizar documentação

### 4. Testar Suas Mudanças

```bash
# Executar suíte de testes completa
make test

# Executar categoria específica de testes
./tests/run_tests.sh tests/category/

# Verificar vazamentos de memória
valgrind ./hemlock tests/your_test.hml

# Build e teste
make clean && make && make test
```

### 5. Commitar Suas Mudanças

**Boas mensagens de commit:**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**Formato da mensagem de commit:**
- Primeira linha: resumo curto (máximo 50 caracteres)
- Linha em branco
- Descrição detalhada (quebra de linha em 72 caracteres)
- Referenciar número da issue

### 6. Submeter Pull Request

**Antes de submeter:**
- Rebase no main mais recente
- Garantir que todos os testes passam
- Executar valgrind para verificar vazamentos
- Atualizar CLAUDE.md se adicionar recursos voltados ao usuário

**A descrição do pull request deve incluir:**
- Que problema isso resolve
- Como foi resolvido
- Breaking changes (se houver)
- Exemplos de nova sintaxe ou comportamento
- Resumo da cobertura de testes

---

## Guia de Estilo de Código

### Estilo de Código C

**Formatação:**
```c
// Use 4 espaços para indentação (não tabs)
// Estilo K&R para chaves em funções
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // Chaves de estruturas de controle na mesma linha
        do_something();
    }
}

// Comprimento de linha: máximo 100 caracteres
// Espaços ao redor de operadores
int result = (a + b) * c;

// Asterisco de ponteiro junto ao tipo
char *string;   // Correto
char* string;   // Evitar
char * string;  // Evitar
```

**Convenções de Nomenclatura:**
```c
// Funções: minúsculas com underscores
void eval_expression(ASTNode *node);

// Tipos: PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// Constantes: maiúsculas com underscores
#define MAX_BUFFER_SIZE 4096

// Variáveis: minúsculas com underscores
int item_count;
Value *current_value;

// Enums: TYPE_PREFIX_NAME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**Comentários:**
```c
// Comentários de linha única para explicações breves
// Use frases completas e capitalização correta

/*
 * Comentários de múltiplas linhas para explicações mais longas
 * Alinhe os asteriscos para melhor legibilidade
 */

/**
 * Comentário de documentação de função
 * @param node - Nó AST a ser avaliado
 * @return Valor avaliado
 */
Value eval_expr(ASTNode *node);
```

**Tratamento de Erros:**
```c
// Verificar todas as chamadas malloc
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Error: Out of memory\n");
    exit(1);
}

// Fornecer contexto nas mensagens de erro
if (file == NULL) {
    fprintf(stderr, "Error: Failed to open '%s': %s\n",
            filename, strerror(errno));
    exit(1);
}

// Usar mensagens de erro significativas
// Ruim: Error: Invalid value
// Bom: Error: Expected integer, got string
```

**Gerenciamento de Memória:**
```c
// Sempre liberar memória que você alocou
Value *val = value_create_i32(42);
// ... usar val
value_free(val);

// Definir ponteiros como NULL após liberar (previne double free)
free(ptr);
ptr = NULL;

// Documentar ownership em comentários
// Esta função assume ownership de 'value' e irá liberá-lo
void store_value(Value *value);

// Esta função não assume ownership (chamador deve liberar)
Value *get_value(void);
```

### Organização de Código

**Estrutura de Arquivos:**
```c
// 1. Includes (headers de sistema primeiro, depois locais)
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. Constantes e macros
#define INITIAL_CAPACITY 16

// 3. Definições de tipos
typedef struct Foo Foo;

// 4. Declarações de funções estáticas (helpers internos)
static void helper_function(void);

// 5. Implementação de funções públicas
void public_api_function(void)
{
    // Implementação
}

// 6. Implementação de funções estáticas
static void helper_function(void)
{
    // Implementação
}
```

**Arquivos Header:**
```c
// Usar include guards
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// Declarações forward
typedef struct Value Value;

// Apenas API pública em headers
void public_function(Value *val);

// Documentar parâmetros e valores de retorno
/**
 * Avalia nó AST de expressão
 * @param node - Nó AST a ser avaliado
 * @param env - Ambiente atual
 * @return Valor resultante
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## O que Contribuir

### Contribuições Encorajadas

**Correções de Bugs:**
- Vazamentos de memória
- Segfaults
- Comportamento incorreto
- Melhorias em mensagens de erro

**Documentação:**
- Comentários de código
- Documentação de API
- Guias de usuário e tutoriais
- Programas de exemplo
- Documentação de casos de teste

**Testes:**
- Casos de teste adicionais para recursos existentes
- Cobertura de casos de borda
- Testes de regressão para bugs corrigidos
- Benchmarks de performance

**Pequenas Adições de Recursos:**
- Novas funções builtin (se alinhadas com a filosofia)
- Métodos de string/array
- Funções utilitárias
- Melhorias no tratamento de erros

**Melhorias de Performance:**
- Algoritmos mais rápidos (sem mudar semântica)
- Redução de uso de memória
- Suíte de benchmarks
- Ferramentas de profiling

**Ferramentas:**
- Syntax highlighting para editores
- Language Server Protocol (LSP)
- Integração com debugger
- Melhorias no sistema de build

### Discutir Primeiro

**Recursos Maiores:**
- Novas construções de linguagem
- Mudanças no sistema de tipos
- Adições de sintaxe
- Primitivas de concorrência

**Como Discutir:**
1. Abrir issue ou discussion no GitHub
2. Descrever o recurso e justificativa
3. Mostrar código de exemplo
4. Explicar como se alinha com a filosofia do Hemlock
5. Aguardar feedback dos mantenedores
6. Iterar no design antes de implementar

---

## O que Não Contribuir

### Contribuições Desencorajadas

**Não adicione recursos que:**
- Escondem complexidade do usuário
- Tornam comportamento implícito ou mágico
- Quebram semântica ou sintaxe existente
- Adicionam coleta de lixo ou gerenciamento automático de memória
- Violam o princípio "explícito é melhor que implícito"

**Exemplos de contribuições que serão rejeitadas:**

**1. Inserção Automática de Ponto e Vírgula**
```hemlock
// Ruim: isso será rejeitado
let x = 5  // Sem ponto e vírgula
let y = 10 // Sem ponto e vírgula
```
Motivo: Torna sintaxe ambígua, esconde erros

**2. RAII/Destrutores**
```hemlock
// Ruim: isso será rejeitado
let f = open("file.txt");
// Arquivo fechado automaticamente ao sair do escopo
```
Motivo: Esconde quando recursos são liberados, não é explícito o suficiente

**3. Conversões de Tipo Implícitas com Perda de Dados**
```hemlock
// Ruim: isso será rejeitado
let x: i32 = 3.14;  // Trunca silenciosamente para 3
```
Motivo: Perda de dados deveria ser explícita, não silenciosa

**4. Coleta de Lixo**
```c
// Ruim: isso será rejeitado
void *gc_malloc(size_t size) {
    // Rastrear alocações para limpeza automática
}
```
Motivo: Esconde gerenciamento de memória, performance imprevisível

**5. Sistema de Macros Complexo**
```hemlock
// Ruim: isso será rejeitado
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
Motivo: Muita mágica, torna código difícil de raciocinar

### Motivos Comuns de Rejeição

**"Isso é muito implícito"**
- Solução: Tornar comportamento explícito e documentar

**"Isso esconde complexidade"**
- Solução: Expor complexidade mas torná-la ergonômica

**"Isso quebra código existente"**
- Solução: Encontrar alternativa não-breaking ou discutir versionamento

**"Isso não se alinha com a filosofia do Hemlock"**
- Solução: Reler philosophy.md e reconsiderar abordagem

---

## Padrões Comuns

### Padrão de Tratamento de Erros

```c
// Use este padrão para erros recuperáveis em código Hemlock
Value *divide(Value *a, Value *b)
{
    // Verificar pré-condições
    if (b->type != TYPE_I32) {
        // Retornar valor de erro ou lançar exceção
        return create_error("Expected integer divisor");
    }

    if (b->i32_value == 0) {
        return create_error("Division by zero");
    }

    // Executar operação
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### Padrão de Gerenciamento de Memória

```c
// Padrão: alocar, usar, liberar
void process_data(void)
{
    // Alocar
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // Usar
    if (buf && str) {
        // ... fazer trabalho
    }

    // Liberar (na ordem reversa da alocação)
    free(str);
    free_buffer(buf);
}
```

### Padrão de Criação de Valores

```c
// Usar construtores para criar valores
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### Padrão de Verificação de Tipos

```c
// Verificar tipos antes de operações
Value *add_values(Value *a, Value *b)
{
    // Verificação de tipos
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Type mismatch");
    }

    // Pode prosseguir com segurança
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### Padrão de Construção de Strings

```c
// Construir strings eficientemente
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Error: %s (line %d)", detail, line_number);
}
```

---

## Adicionando Novos Recursos

### Checklist de Adição de Recursos

Ao adicionar um novo recurso, por favor siga estes passos:

#### 1. Fase de Design

- [ ] Ler philosophy.md para garantir alinhamento
- [ ] Criar issue no GitHub descrevendo o recurso
- [ ] Obter aprovação dos mantenedores no design
- [ ] Escrever especificação (sintaxe, semântica, exemplos)
- [ ] Considerar casos de borda e condições de erro

#### 2. Fase de Implementação

**Se adicionando construção de linguagem:**

- [ ] Adicionar tipo de token em `lexer.h` (se necessário)
- [ ] Adicionar regra léxica em `lexer.c` (se necessário)
- [ ] Adicionar tipo de nó AST em `ast.h`
- [ ] Adicionar construtor AST em `ast.c`
- [ ] Adicionar regra de parsing em `parser.c`
- [ ] Adicionar comportamento runtime em `runtime.c` ou módulo apropriado
- [ ] Tratar limpeza em funções de liberação de AST

**Se adicionando função builtin:**

- [ ] Adicionar implementação da função em `builtins.c`
- [ ] Registrar função em `register_builtins()`
- [ ] Tratar todas as combinações de tipos de argumentos
- [ ] Retornar valores de erro apropriados
- [ ] Documentar parâmetros e tipos de retorno

**Se adicionando tipo de valor:**

- [ ] Adicionar enum de tipo em `values.h`
- [ ] Adicionar campo à union Value
- [ ] Adicionar construtor em `values.c`
- [ ] Adicionar a `value_free()` para limpeza
- [ ] Adicionar a `value_copy()` para cópia
- [ ] Adicionar a `value_to_string()` para impressão
- [ ] Adicionar regras de promoção de tipo se numérico

#### 3. Fase de Testes

- [ ] Escrever casos de teste (veja testing.md)
- [ ] Testar casos de sucesso
- [ ] Testar casos de erro
- [ ] Testar casos de borda
- [ ] Executar suíte de testes completa (`make test`)
- [ ] Verificar vazamentos de memória com valgrind
- [ ] Testar em múltiplas plataformas (se possível)

#### 4. Fase de Documentação

- [ ] Atualizar CLAUDE.md com documentação voltada ao usuário
- [ ] Adicionar comentários de código explicando implementação
- [ ] Criar exemplos em `examples/`
- [ ] Atualizar arquivos docs/ relevantes
- [ ] Documentar quaisquer breaking changes

#### 5. Fase de Submissão

- [ ] Limpar código de debug e comentários
- [ ] Verificar conformidade com estilo de código
- [ ] Rebase no main mais recente
- [ ] Criar pull request com descrição detalhada
- [ ] Responder ao feedback do code review

### Exemplo: Adicionando Novo Operador

Vamos usar o exemplo de adicionar o operador módulo `%`:

**1. Lexer (lexer.c):**
```c
// Adicionar ao switch statement em get_next_token()
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. Header do Lexer (lexer.h):**
```c
typedef enum {
    // ... tokens existentes
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h):**
```c
typedef enum {
    // ... operadores existentes
    OP_MOD,
    // ...
} BinaryOp;
```

**4. Parser (parser.c):**
```c
// Adicionar a parse_multiplicative() ou nível de precedência apropriado
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. Runtime (runtime.c):**
```c
// Adicionar a eval_binary_op()
case OP_MOD:
    // Verificação de tipos
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Error: Modulo by zero\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... tratar outras combinações de tipos
    break;
```

**6. Teste (tests/operators/modulo.hml):**
```hemlock
// Módulo básico
print(10 % 3);  // Expect: 2

// Módulo com negativos
print(-10 % 3); // Expect: -1

// Caso de erro (deveria falhar)
// print(10 % 0);  // Divisão por zero
```

**7. Documentação (CLAUDE.md):**
```markdown
### Operadores Aritméticos
- `+` - Adição
- `-` - Subtração
- `*` - Multiplicação
- `/` - Divisão
- `%` - Módulo (resto)
```

---

## Processo de Code Review

### O que os Revisores Procuram

**1. Corretude**
- O código faz o que diz fazer?
- Casos de borda são tratados?
- Há vazamentos de memória?
- Erros são tratados corretamente?

**2. Alinhamento com Filosofia**
- Isso está alinhado com os princípios de design do Hemlock?
- É explícito ou implícito?
- Esconde complexidade?

**3. Qualidade de Código**
- O código é legível e manutenível?
- Nomes de variáveis são descritivos?
- Funções têm tamanho razoável?
- Há documentação suficiente?

**4. Testes**
- Há casos de teste suficientes?
- Testes cobrem caminhos de sucesso e falha?
- Casos de borda são testados?

**5. Documentação**
- Documentação voltada ao usuário está atualizada?
- Comentários de código são claros?
- Exemplos são fornecidos?

### Respondendo ao Feedback

**Faça:**
- Agradecer o tempo do revisor
- Fazer perguntas de esclarecimento se não entender
- Explicar seu raciocínio se discordar
- Fazer mudanças solicitadas prontamente
- Atualizar descrição do PR se escopo mudar

**Não faça:**
- Levar críticas para o lado pessoal
- Argumentar defensivamente
- Ignorar feedback
- Fazer force push em comentários de review (exceto rebase)
- Adicionar mudanças não relacionadas ao PR

### Fazendo Seu PR Ser Aceito

**Requisitos para merge:**
- [ ] Todos os testes passam
- [ ] Sem vazamentos de memória (valgrind limpo)
- [ ] Aprovação de code review do mantenedor
- [ ] Documentação atualizada
- [ ] Guia de estilo de código seguido
- [ ] Alinhado com a filosofia do Hemlock

**Timeline:**
- PRs pequenos (correções de bugs): Geralmente revisados em poucos dias
- PRs médios (novos recursos): Pode levar 1-2 semanas
- PRs grandes (mudanças maiores): Requer discussão extensa

---

## Recursos Adicionais

### Recursos de Aprendizado

**Entendendo Interpretadores:**
- "Crafting Interpreters" por Robert Nystrom
- "Writing An Interpreter In Go" por Thorsten Ball
- "Modern Compiler Implementation in C" por Andrew Appel

**Programação C:**
- "The C Programming Language" por K&R
- "Expert C Programming" por Peter van der Linden
- "C Interfaces and Implementations" por David Hanson

**Gerenciamento de Memória:**
- Documentação do Valgrind
- "Understanding and Using C Pointers" por Richard Reese

### Comandos Úteis

```bash
# Build com símbolos de debug
make clean && make CFLAGS="-g -O0"

# Executar com valgrind
valgrind --leak-check=full ./hemlock script.hml

# Executar categoria específica de testes
./tests/run_tests.sh tests/strings/

# Gerar arquivo tags para navegação de código
ctags -R .

# Encontrar todos os TODO e FIXME
grep -rn "TODO\|FIXME" src/ include/
```

---

## Dúvidas?

Se você tem perguntas sobre contribuir:

1. Verificar documentação em `docs/`
2. Pesquisar issues existentes no GitHub
3. Perguntar no GitHub Discussions
4. Abrir uma nova issue com sua pergunta

**Obrigado por contribuir para o Hemlock!**
