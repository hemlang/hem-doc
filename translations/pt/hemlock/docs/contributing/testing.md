# Guia de Testes do Hemlock

Este guia explica a filosofia de testes do Hemlock, como escrever testes e como executar a suíte de testes.

---

## Sumário

- [Filosofia de Testes](#filosofia-de-testes)
- [Estrutura da Suíte de Testes](#estrutura-da-suíte-de-testes)
- [Executando Testes](#executando-testes)
- [Escrevendo Testes](#escrevendo-testes)
- [Categorias de Testes](#categorias-de-testes)
- [Testes de Vazamento de Memória](#testes-de-vazamento-de-memória)
- [Integração Contínua](#integração-contínua)
- [Melhores Práticas](#melhores-práticas)

---

## Filosofia de Testes

### Princípios Centrais

**1. Desenvolvimento Orientado a Testes (TDD)**

Escreva testes **antes** de implementar recursos:

```
1. Escrever um teste que falha
2. Implementar o recurso
3. Executar teste (deve passar)
4. Refatorar se necessário
5. Repetir
```

**Benefícios:**
- Garante que o recurso realmente funciona
- Previne regressões
- Documenta comportamento esperado
- Torna refatoração mais segura

**2. Cobertura Abrangente**

Testar casos de sucesso e falha:

```hemlock
// Caso de sucesso
let x: u8 = 255;  // Deveria funcionar

// Caso de falha
let y: u8 = 256;  // Deveria dar erro
```

**3. Testar Cedo e Frequentemente**

Executar testes:
- Antes de commitar código
- Depois de fazer mudanças
- Antes de submeter pull request
- Durante code review

**Regra:** Todos os testes devem passar antes do merge.

### O que Testar

**Sempre teste:**
- Funcionalidade básica (caminho feliz)
- Condições de erro (caminho de exceção)
- Casos de borda (condições limite)
- Verificação e conversão de tipos
- Gerenciamento de memória (sem vazamentos)
- Concorrência e condições de corrida

**Exemplo de cobertura de testes:**
```hemlock
// Recurso: String.substr(start, length)

// Caminho feliz
print("hello".substr(0, 5));  // "hello"

// Casos de borda
print("hello".substr(0, 0));  // "" (vazio)
print("hello".substr(5, 0));  // "" (no final)
print("hello".substr(2, 100)); // "llo" (além do final)

// Casos de erro
// "hello".substr(-1, 5);  // Erro: índice negativo
// "hello".substr(0, -1);  // Erro: comprimento negativo
```

---

## Estrutura da Suíte de Testes

### Organização de Diretórios

```
tests/
├── run_tests.sh          # Script principal de execução de testes
├── primitives/           # Testes do sistema de tipos
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # Testes de conversão de tipos
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # Testes de ponteiro/buffer
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # Testes de manipulação de strings
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # Testes de fluxo de controle
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # Testes de funções e closures
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # Testes de objetos
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # Testes de operações de arrays
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # Testes de loops
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # Testes de tratamento de erros
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # Testes de I/O de arquivos
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # Testes de concorrência
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # Testes de FFI
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # Testes de tratamento de sinais
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # Testes de argumentos de linha de comando
    └── basic.hml
```

### Nomenclatura de Arquivos de Teste

**Convenções:**
- Usar nomes descritivos: `method_chaining.hml` ao invés de `test1.hml`
- Agrupar testes relacionados: `string_substr.hml`, `string_slice.hml`
- Uma área funcional por arquivo
- Manter arquivos focados e pequenos

---

## Executando Testes

### Executar Todos os Testes

```bash
# Do diretório raiz do hemlock
make test

# Ou diretamente
./tests/run_tests.sh
```

**Saída:**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### Executar Categoria Específica

```bash
# Apenas testes de strings
./tests/run_tests.sh tests/strings/

# Apenas um arquivo de teste
./tests/run_tests.sh tests/strings/concat.hml

# Múltiplas categorias
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Executar com Valgrind (Verificação de Vazamento de Memória)

```bash
# Verificar vazamentos em um único teste
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# Verificar todos os testes (muito lento!)
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### Debugando Testes que Falham

```bash
# Executar com saída verbosa
./hemlock tests/failing_test.hml

# Executar com gdb
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # Se crashar
```

---

## Escrevendo Testes

### Formato de Arquivo de Teste

Arquivos de teste são simplesmente programas Hemlock com saída esperada:

**Exemplo: tests/primitives/integers.hml**
```hemlock
// Testar literais inteiros básicos
let x = 42;
print(x);  // Expect: 42

let y: i32 = 100;
print(y);  // Expect: 100

// Testar aritmética
let sum = x + y;
print(sum);  // Expect: 142

// Testar inferência de tipos
let small = 10;
print(typeof(small));  // Expect: i32

let large = 5000000000;
print(typeof(large));  // Expect: i64
```

**Como os testes funcionam:**
1. O executor de testes executa o arquivo .hml
2. Captura saída stdout
3. Compara com saída esperada (de comentários ou arquivo .out separado)
4. Reporta passou/falhou

### Métodos de Saída Esperada

**Método 1: Comentários Inline (recomendado para testes simples)**

```hemlock
print("hello");  // Expect: hello
print(42);       // Expect: 42
```

O executor de testes faz parse de comentários `// Expect: ...`.

**Método 2: Arquivo .out Separado**

Criar `test_name.hml.out` com saída esperada:

**test_name.hml:**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**test_name.hml.out:**
```
line 1
line 2
line 3
```

### Testando Casos de Erro

Testes de erro devem fazer o programa sair com status não-zero:

**Exemplo: tests/primitives/range_error.hml**
```hemlock
// Isso deveria falhar com erro de tipo
let x: u8 = 256;  // Fora do intervalo de u8
```

**Comportamento esperado:**
- Programa sai com status não-zero
- Imprime mensagem de erro em stderr

**Tratamento do executor de testes:**
- Testes esperados a dar erro devem estar em arquivos separados
- Usar convenção de nomenclatura: `*_error.hml` ou `*_fail.hml`
- Documentar erro esperado em comentário

### Testando Casos de Sucesso

**Exemplo: tests/strings/methods.hml**
```hemlock
// Testar substr
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Expect: world

// Testar find
let pos = s.find("world");
print(pos);  // Expect: 6

// Testar contains
let has = s.contains("lo");
print(has);  // Expect: true

// Testar trim
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Expect: hello
```

### Testando Casos de Borda

**Exemplo: tests/arrays/edge_cases.hml**
```hemlock
// Array vazio
let empty = [];
print(empty.length);  // Expect: 0

// Único elemento
let single = [42];
print(single[0]);  // Expect: 42

// Índice negativo (deveria dar erro em arquivo de teste separado)
// print(single[-1]);  // Erro

// Índice além do final (deveria dar erro)
// print(single[100]);  // Erro

// Condições de borda
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Expect: [] (vazio)
print(arr.slice(3, 3));  // Expect: [] (vazio)
print(arr.slice(1, 2));  // Expect: [2]
```

### Testando Sistema de Tipos

**Exemplo: tests/conversions/promotion.hml**
```hemlock
// Testar promoção de tipos em operações binárias

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Expect: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Expect: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Expect: i32
```

### Testando Concorrência

**Exemplo: tests/async/basic.hml**
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

// Spawn tasks
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// Esperar e imprimir resultados
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Expect: 45
print(r2);  // Expect: 190
```

### Testando Exceções

**Exemplo: tests/exceptions/try_catch.hml**
```hemlock
// Testar try/catch básico
try {
    throw "error message";
} catch (e) {
    print("Caught: " + e);  // Expect: Caught: error message
}

// Testar finally
let executed = false;
try {
    print("try");  // Expect: try
} finally {
    executed = true;
    print("finally");  // Expect: finally
}

// Testar propagação de exceção
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // Expect: failure
}
```

---

## Categorias de Testes

### Testes de Tipos Primitivos

**O que testar:**
- Tipos inteiros (i8, i16, i32, i64, u8, u16, u32, u64)
- Tipos de ponto flutuante (f32, f64)
- Tipo booleano
- Tipo string
- Tipo rune
- Tipo null

**Áreas de exemplo:**
- Sintaxe de literais
- Inferência de tipos
- Verificação de intervalos
- Comportamento de overflow
- Anotações de tipo

### Testes de Conversões

**O que testar:**
- Promoção de tipos implícita
- Conversão de tipos explícita
- Conversões com perda (deveriam dar erro)
- Promoção de tipos em operações
- Comparações entre tipos

### Testes de Memória

**O que testar:**
- Corretude de alloc/free
- Criação e acesso de Buffer
- Verificação de limites de buffer
- memset, memcpy, realloc
- Detecção de vazamento de memória (valgrind)

### Testes de Strings

**O que testar:**
- Concatenação
- Todos os 18 métodos de string
- Tratamento de UTF-8
- Indexação de runes
- Concatenação string + rune
- Casos de borda (string vazia, único caractere, etc.)

### Testes de Fluxo de Controle

**O que testar:**
- if/else/else if
- Loops while
- Loops for
- Statements switch
- break/continue
- Statements return

### Testes de Funções

**O que testar:**
- Definição e chamada de funções
- Passagem de parâmetros
- Valores de retorno
- Recursão
- Closures e captura
- Funções de primeira classe
- Funções anônimas

### Testes de Objetos

**O que testar:**
- Literais de objeto
- Acesso e atribuição de campos
- Métodos e binding de self
- Duck typing
- Campos opcionais
- Serialização/deserialização JSON
- Detecção de referência circular

### Testes de Arrays

**O que testar:**
- Criação de arrays
- Indexação e atribuição
- Todos os 15 métodos de array
- Tipos misturados
- Redimensionamento dinâmico
- Casos de borda (vazio, único elemento)

### Testes de Exceções

**O que testar:**
- try/catch/finally
- Statement throw
- Propagação de exceções
- try/catch aninhado
- return em try/catch/finally
- Exceções não capturadas

### Testes de I/O

**O que testar:**
- Modos de abertura de arquivo
- Operações de leitura/escrita
- Seek/tell
- Atributos de arquivo
- Tratamento de erros (arquivo faltando, etc.)
- Limpeza de recursos

### Testes de Async

**O que testar:**
- spawn/join/detach
- Channel send/recv
- Propagação de exceções em tasks
- Múltiplas tasks concorrentes
- Comportamento de bloqueio de channels

### Testes de FFI

**O que testar:**
- dlopen/dlclose
- dlsym
- dlcall com vários tipos
- Conversão de tipos
- Tratamento de erros

---

## Testes de Vazamento de Memória

### Usando Valgrind

**Uso básico:**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**Exemplo de saída (sem vazamentos):**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**Exemplo de saída (com vazamentos):**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### Fontes Comuns de Vazamentos

**1. Chamadas free() faltando:**
```c
// Ruim
char *str = malloc(100);
// ... usar str
// Esqueceu de liberar!

// Bom
char *str = malloc(100);
// ... usar str
free(str);
```

**2. Ponteiros perdidos:**
```c
// Ruim
char *ptr = malloc(100);
ptr = malloc(200);  // Perdeu referência para primeira alocação!

// Bom
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. Caminhos de exceção:**
```c
// Ruim
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // Vazamento!
    }
    free(data);
}

// Bom
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### Vazamentos Conhecidos e Aceitáveis

Alguns pequenos "vazamentos" são alocações de inicialização intencionais:

**Builtins globais:**
```hemlock
// Funções builtin, tipos FFI e constantes são alocados na inicialização
// e não são liberados na saída (geralmente ~200 bytes)
```

Estes não são vazamentos reais - são alocações únicas que duram toda a vida do programa e são limpas pelo SO na saída.

---

## Integração Contínua

### GitHub Actions (Futuro)

Uma vez que CI esteja configurado, todos os testes executarão automaticamente em:
- Push para branch main
- Criação/atualização de Pull Request
- Execução agendada diária

**Workflow de CI:**
1. Build do Hemlock
2. Executar suíte de testes
3. Verificar vazamentos de memória (valgrind)
4. Reportar resultados no PR

### Verificações Pré-Commit

Antes de commitar, execute:

```bash
# Build limpo
make clean && make

# Executar todos os testes
make test

# Verificar vazamentos em alguns testes
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## Melhores Práticas

### Faça

**Escreva testes primeiro (TDD)**
```bash
1. Criar tests/feature/new_feature.hml
2. Implementar recurso em src/
3. Executar testes até passar
```

**Teste casos de sucesso e falha**
```hemlock
// Sucesso: tests/feature/success.hml
let result = do_thing();
print(result);  // Expect: expected value

// Falha: tests/feature/failure.hml
do_invalid_thing();  // Deveria dar erro
```

**Use nomes de teste descritivos**
```
Bom: tests/strings/substr_utf8_boundary.hml
Ruim: tests/test1.hml
```

**Mantenha testes focados**
- Uma área funcional por arquivo
- Setup e assertivas claras
- Código mínimo

**Adicione comentários explicando testes complicados**
```hemlock
// Testar que closures capturam variáveis externas por referência
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // Modificar após criação da closure
    return f();  // Deveria retornar 20, não 10
}
```

**Teste casos de borda**
- Entradas vazias
- Valores null
- Valores de fronteira (min/max)
- Entradas grandes
- Valores negativos

### Não Faça

**Não pule testes**
- Todos os testes devem passar antes do merge
- Não comente testes que falham
- Corrija o bug ou remova o recurso

**Não escreva testes que dependem uns dos outros**
```hemlock
// Ruim: test2.hml depende da saída de test1.hml
// Testes devem ser independentes
```

**Não use valores aleatórios em testes**
```hemlock
// Ruim: não-determinístico
let x = random();
print(x);  // Não pode prever saída

// Bom: determinístico
let x = 42;
print(x);  // Expect: 42
```

**Não teste detalhes de implementação**
```hemlock
// Ruim: testa estrutura interna
let obj = { x: 10 };
// Não verifique ordem interna de campos, capacidade, etc.

// Bom: testa comportamento
print(obj.x);  // Expect: 10
```

**Não ignore vazamentos de memória**
- Todos os testes devem estar limpos no valgrind
- Documente vazamentos conhecidos/aceitáveis
- Corrija vazamentos antes do merge

### Manutenção de Testes

**Quando atualizar testes:**
- Comportamento de recurso muda
- Correção de bug precisa de novo caso de teste
- Caso de borda é descoberto
- Melhorias de performance

**Quando remover testes:**
- Recurso é removido da linguagem
- Teste duplica cobertura existente
- Teste está incorreto

**Refatorando testes:**
- Agrupar testes relacionados juntos
- Extrair código de setup comum
- Usar nomenclatura consistente
- Manter testes simples e legíveis

---

## Exemplo de Sessão de Teste

Aqui está um exemplo completo de adicionar um recurso com testes:

### Recurso: Adicionar Método `array.first()`

**1. Escrever teste primeiro:**

```bash
# Criar arquivo de teste
cat > tests/arrays/first_method.hml << 'EOF'
// Testar método array.first()

// Caso básico
let arr = [1, 2, 3];
print(arr.first());  // Expect: 1

// Único elemento
let single = [42];
print(single.first());  // Expect: 42

// Array vazio (deveria dar erro - arquivo de teste separado)
// let empty = [];
// print(empty.first());  // Erro
EOF
```

**2. Executar teste (deveria falhar):**

```bash
./hemlock tests/arrays/first_method.hml
# Error: Method 'first' not found on array
```

**3. Implementar recurso:**

Editar `src/interpreter/builtins.c`:

```c
// Adicionar método array_first
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Error: Cannot get first element of empty array\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// Registrar na tabela de métodos de array
// ... adicionar ao registro de métodos de array
```

**4. Executar teste (deveria passar):**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# Sucesso!
```

**5. Verificar vazamentos de memória:**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. Executar suíte de testes completa:**

```bash
make test
# Total: 252 tests (251 + novo)
# Passed: 252
# Failed: 0
```

**7. Commitar:**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## Resumo

**Lembre-se:**
- Escrever testes primeiro (TDD)
- Testar casos de sucesso e falha
- Executar todos os testes antes de commitar
- Verificar vazamentos de memória
- Documentar problemas conhecidos
- Manter testes simples e focados

**Qualidade de testes é tão importante quanto qualidade de código!**
