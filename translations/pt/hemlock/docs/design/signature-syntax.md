# Design de Sintaxe de Assinaturas

> Estendendo o sistema de tipos do Hemlock com tipos de função, modificadores nullable, aliases de tipo, parâmetros const e assinaturas de método.

**Status:** Implementado (v1.7.0)
**Versão:** 1.0
**Autor:** Claude

---

## Visão Geral

Este documento propõe cinco extensões inter-relacionadas do sistema de tipos que se baseiam na infraestrutura existente do Hemlock:

1. **Anotações de Tipo de Função** - Tipos de função de primeira classe
2. **Modificador de Tipo Nullable** - Tratamento explícito de null (estendendo flag `nullable` existente)
3. **Aliases de Tipo** - Abreviações de tipo nomeadas
4. **Parâmetros Const** - Contratos de imutabilidade
5. **Assinaturas de Método em Define** - Comportamento de interface

Estes recursos compartilham a mesma filosofia: **explícito é melhor que implícito, opcional mas aplicado quando usado**.

---

## 1. Anotações de Tipo de Função

### Motivação

Atualmente, não há como expressar a assinatura de uma função como um tipo:

```hemlock
// Atual: callback não tem informação de tipo
fn map(arr: array, callback) { ... }

// Proposto: tipo de função explícito
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Sintaxe

```hemlock
// Tipo de função básico
fn(i32, i32): i32

// Com nomes de parâmetros (apenas documentação, não aplicado)
fn(a: i32, b: i32): i32

// Sem retorno (void)
fn(string): void
fn(string)              // Abreviação: omitir `: void`

// Retorno nullable
fn(i32): string?

// Parâmetros opcionais
fn(name: string, age?: i32): void

// Parâmetros rest
fn(...args: array): i32

// Sem parâmetros
fn(): bool

// Alta ordem: função que retorna função
fn(i32): fn(i32): i32

// Tipo de função async
async fn(i32): i32
```

### Exemplos de Uso

```hemlock
// Variável com tipo de função
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parâmetro de função
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Tipo de retorno é uma função
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Array de funções
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// Campo de objeto
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### Mudanças no AST

```c
// No enum TypeKind (include/ast.h)
typedef enum {
    // ... tipos existentes ...
    TYPE_FUNCTION,      // Novo: tipo de função
} TypeKind;

// Na struct Type (include/ast.h)
struct Type {
    TypeKind kind;
    // ... campos existentes ...

    // Para TYPE_FUNCTION:
    struct Type **param_types;      // Tipos de parâmetros
    char **param_names;             // Nomes de parâmetros opcionais (documentação)
    int *param_optional;            // Quais parâmetros são opcionais
    int num_params;
    char *rest_param_name;          // Nome do parâmetro rest ou NULL
    struct Type *rest_param_type;   // Tipo do parâmetro rest
    struct Type *return_type;       // Tipo de retorno (NULL = void)
    int is_async;                   // Tipo fn async
};
```

### Parsing

Tipos de função começam com `fn` (ou `async fn`) seguido por lista de parâmetros:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Desambiguação:** Ao fazer parse de tipo e encontrar `fn`:
- Se seguido por `(`, é um tipo de função
- Caso contrário, erro de sintaxe (`fn` isolado não é tipo válido)

### Compatibilidade de Tipos

```hemlock
// Tipos de função requerem correspondência exata
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Contravariância de parâmetros (aceitar tipo mais amplo é ok)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Covariância de retorno (retornar tipo mais estreito é ok)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Número de parâmetros deve corresponder
let bad: fn(i32): i32 = fn(a, b) { return a; };       // Erro: número de parâmetros não corresponde

// Parâmetros opcionais compatíveis com requeridos
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Modificador de Tipo Nullable

### Motivação

O sufixo `?` torna a aceitação de null explícita nas assinaturas:

```hemlock
// Atual: não está claro se null é válido
fn find(arr: array, val: any): i32 { ... }

// Proposto: retorno nullable explícito
fn find(arr: array, val: any): i32? { ... }
```

### Sintaxe

```hemlock
// Tipo nullable com sufixo ?
string?           // string ou null
i32?              // i32 ou null
User?             // User ou null
array<i32>?       // array ou null
fn(i32): i32?     // Função que retorna i32 ou null

// Combinação com tipos de função
fn(string?): i32          // Aceita string ou null
fn(string): i32?          // Retorna i32 ou null
fn(string?): i32?         // Ambos nullable

// Em define
define Result {
    value: any?;
    error: string?;
}
```

### Notas de Implementação

**Já existe:** Flag `Type.nullable` já existe no AST. Este recurso principalmente requer:
1. Suporte do parser para sufixo `?` em qualquer tipo (validar/estender)
2. Combinação adequada com tipos de função
3. Aplicação em runtime

### Compatibilidade de Tipos

```hemlock
// Não-null pode ser atribuído a nullable
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullable não pode ser atribuído a não-null
let z: i32 = x;             // Erro: x pode ser null

// Coalescência de null para desempacotar
let z: i32 = x ?? 0;        // OK: ?? fornece valor padrão

// Encadeamento opcional retorna nullable
let name: string? = user?.name;
```

---

## 3. Aliases de Tipo

### Motivação

Tipos complexos se beneficiam de abreviações nomeadas:

```hemlock
// Atual: tipos compostos repetidos
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// Proposto: alias nomeado
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### Sintaxe

```hemlock
// Alias básico
type Integer = i32;
type Text = string;

// Alias de tipo composto
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// Alias de tipo de função
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Alias nullable
type OptionalString = string?;

// Alias genérico (se suportarmos aliases de tipo genéricos)
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Alias de tipo array
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### Escopo e Visibilidade

```hemlock
// Escopo de módulo por padrão
type Callback = fn(Event): void;

// Exportável
export type Handler = fn(Request): Response;

// Em outro arquivo
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### Mudanças no AST

```c
// Novo tipo de statement
typedef enum {
    // ... statements existentes ...
    STMT_TYPE_ALIAS,    // Novo
} StmtKind;

// Na union Stmt
struct {
    char *name;                 // Nome do alias
    char **type_params;         // Parâmetros genéricos: <T, U>
    int num_type_params;
    Type *aliased_type;         // Tipo real
} type_alias;
```

### Parsing

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Nota:** `type` é uma nova palavra-chave. Verificar conflitos com identificadores existentes.

### Resolução

Aliases de tipo são resolvidos em:
- **Tempo de parse:** Alias é registrado no ambiente de tipos
- **Tempo de verificação:** Alias é expandido para tipo subjacente
- **Runtime:** Alias é transparente (mesmo que tipo subjacente)

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32" (não "MyInt")
```

---

## 4. Parâmetros Const

### Motivação

Expressar intenção de imutabilidade nas assinaturas de função:

```hemlock
// Atual: não está claro se array será modificado
fn print_all(items: array) { ... }

// Proposto: contrato de imutabilidade explícito
fn print_all(const items: array) { ... }
```

### Sintaxe

```hemlock
// Parâmetro const
fn process(const data: buffer) {
    // data[0] = 0;        // Erro: não pode modificar const
    let x = data[0];       // OK: leitura permitida
    return x;
}

// Múltiplos parâmetros const
fn compare(const a: array, const b: array): bool { ... }

// Misturando const e mutável
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK: target é mutável
    }
}

// Const com inferência de tipo
fn log(const msg) {
    print(msg);
}

// Const em tipo de função
type Reader = fn(const buffer): i32;
```

### Operações que Const Impede

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // Erro: método modificador
    arr.pop();           // Erro: método modificador
    arr[0] = 5;          // Erro: atribuição por índice
    arr.clear();         // Erro: método modificador
}

fn ok(const arr: array) {
    let x = arr[0];      // OK: leitura
    let len = len(arr);  // OK: verificar comprimento
    let copy = arr.slice(0, 10);  // OK: cria novo array
    for (item in arr) {  // OK: iteração
        print(item);
    }
}
```

### Métodos Modificadores vs Não-Modificadores

| Tipo | Modificadores (bloqueados por const) | Não-Modificadores (permitidos) |
|------|--------------------------------------|--------------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (in-place) | slice, concat, map, filter, find, contains, first, last, join |
| string | Atribuição por índice (`s[0] = 'x'`) | Todos os métodos (retornam nova string) |
| buffer | Atribuição por índice, memset, memcpy (destino) | Leitura por índice, slice |
| object | Atribuição de campo | Leitura de campo |

### Mudanças no AST

```c
// Na expressão de função (include/ast.h)
struct {
    // ... campos existentes ...
    int *param_is_const;    // Novo: 1 para const, 0 caso contrário
} function;

// Na struct Type para tipo de função
struct Type {
    // ... campos existentes ...
    int *param_is_const;    // Para TYPE_FUNCTION
};
```

### Aplicação

**Interpretador:**
- Rastrear const-ness em binding de variáveis
- Verificar antes de operações modificadoras
- Erro runtime em violação de const

**Compilador:**
- Gerar variáveis C qualificadas com const quando benéfico
- Análise estática para violações de const
- Avisos/erros em tempo de compilação

---

## 5. Assinaturas de Método em Define

### Motivação

Permitir que blocos `define` especifiquem métodos esperados, não apenas campos de dados:

```hemlock
// Atual: apenas campos de dados
define User {
    name: string;
    age: i32;
}

// Proposto: assinaturas de método
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // Método estático
}
```

### Sintaxe

```hemlock
// Assinatura de método (sem corpo)
define Hashable {
    fn hash(): i32;
}

// Múltiplos métodos
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// Misturando campos e métodos
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Usando tipo Self
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// Método opcional
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // Método opcional (pode não existir)
}

// Método com implementação padrão
define Ordered {
    fn compare(other: Self): i32;  // Requerido

    // Implementação padrão (herdada se não sobrescrita)
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### Tipo `Self`

`Self` refere-se ao tipo concreto que implementa a interface:

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// Ao usar:
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### Tipagem Estrutural (Duck Typing)

Assinaturas de método usam o mesmo duck typing que campos:

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// Qualquer objeto com método to_string() satisfaz Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// Tipos compostos com métodos
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### Mudanças no AST

```c
// Estendendo define_object na union Stmt
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Campos (existentes)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Métodos (novos)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Métodos opcionais (fn name?(): type)
    Expr **method_defaults;     // Implementação padrão (NULL se apenas assinatura)
    int num_methods;
} define_object;
```

### Verificação de Tipos

Ao verificar `value: InterfaceType`:
1. Verificar que todos os campos requeridos existem e tipos são compatíveis
2. Verificar que todos os métodos requeridos existem e assinaturas são compatíveis
3. Campos/métodos opcionais podem estar ausentes

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// Válido: tem método compare
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Inválido: falta compare
let invalid: Sortable = { value: 10 };  // Erro: falta método 'compare'

// Inválido: assinatura errada
let wrong: Sortable = {
    compare: fn() { return 0; }  // Erro: esperava (Self): i32
};
```

---

## Exemplos de Interação

### Combinando Todos os Recursos

```hemlock
// Alias de tipo para tipo de função complexo
type EventCallback = fn(event: Event, context: Context?): bool;

// Alias de tipo para interface composta
type Entity = HasId & HasName & Serializable;

// Define com assinaturas de método
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// Usando tudo junto
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### Callbacks com Tipos Explícitos

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Tipos de Função Nullable

```hemlock
// Callback opcional
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// Retorno nullable de tipo de função
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## Roteiro de Implementação

### Fase 1: Infraestrutura Core
1. Adicionar `TYPE_FUNCTION` ao enum TypeKind
2. Estender struct Type com campos de tipo de função
3. Adicionar `CHECKED_FUNCTION` ao type checker do compilador
4. Adicionar suporte a tipo `Self` (TYPE_SELF)

### Fase 2: Parsing
1. Implementar `parse_function_type()` no parser
2. Tratar `fn(...)` em posição de tipo
3. Adicionar palavra-chave `type` e parsing de `STMT_TYPE_ALIAS`
4. Adicionar parsing de modificador de parâmetro `const`
5. Estender parsing de define para suportar assinaturas de método

### Fase 3: Verificação de Tipos
1. Regras de compatibilidade de tipos de função
2. Resolução e expansão de aliases de tipo
3. Verificação de modificação de parâmetros const
4. Validação de assinatura de método em tipos define
5. Resolução de tipo Self

### Fase 4: Runtime
1. Validação de tipo de função em ponto de chamada
2. Detecção de violação de const
3. Transparência de alias de tipo

### Fase 5: Testes de Paridade
1. Testes de anotação de tipo de função
2. Testes de combinação nullable
3. Testes de alias de tipo
4. Testes de parâmetros const
5. Testes de assinatura de método

---

## Decisões de Design

### 1. Aliases de Tipo Genéricos: **Sim**

Aliases de tipo suportam parâmetros genéricos:

```hemlock
// Aliases de tipo genéricos
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Uso
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Propagação de Const: **Profunda**

Parâmetros const são totalmente imutáveis - não podem ser modificados por nenhum caminho:

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // Erro: não pode modificar array const
    arr[0] = {};         // Erro: não pode modificar array const
    arr[0].x = 5;        // Erro: não pode modificar através de const (profundo)

    let x = arr[0].x;    // OK: leitura é permitida
    let copy = arr[0];   // OK: criar cópia
    copy.x = 5;          // OK: cópia não é const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // Erro: const profundo impede modificação aninhada
    obj.items[0] = 1;    // Erro: const profundo impede modificação aninhada
}
```

**Justificativa:** Const profundo fornece garantias mais fortes e é mais útil para garantir integridade de dados. Se você precisa modificar dados aninhados, faça uma cópia primeiro.

### 3. Self em Aliases de Tipo Standalone: **Não**

`Self` só é válido dentro de blocos `define` onde tem significado claro:

```hemlock
// Válido: Self refere-se ao tipo definido
define Comparable {
    fn compare(other: Self): i32;
}

// Inválido: Self não tem significado aqui
type Cloner = fn(Self): Self;  // Erro: Self fora de contexto define

// Use genérico em vez disso:
type Cloner<T> = fn(T): T;
```

### 4. Implementações Padrão de Método: **Sim (apenas simples)**

Permitir implementação padrão para métodos simples/utilitários:

```hemlock
define Comparable {
    // Requerido: deve ser implementado
    fn compare(other: Self): i32;

    // Implementação padrão (métodos de conveniência simples)
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // Padrão: delegar para método requerido
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// Objetos só precisam implementar métodos requeridos
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_than herdados dos padrões
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**Diretrizes para implementações padrão:**
- Manter simples (1-3 linhas)
- Devem delegar para métodos requeridos
- Sem lógica complexa ou efeitos colaterais
- Apenas tipos primitivos e composição direta

### 5. Variância: **Inferida (sem anotações explícitas)**

Variância é inferida com base em como parâmetros de tipo são usados:

```hemlock
// Variância determinada automaticamente pela posição
type Producer<T> = fn(): T;           // T em posição de retorno = covariante
type Consumer<T> = fn(T): void;       // T em posição de parâmetro = contravariante
type Transformer<T> = fn(T): T;       // T em ambas posições = invariante

// Exemplo: Dog <: Animal (Dog é subtipo de Animal)
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK: covariante

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK: contravariante
```

**Por que inferida?**
- Menos boilerplate (`<out T>` / `<in T>` adiciona ruído)
- Segue "explícito é melhor que implícito" - a posição em si é explícita
- Consistente com como a maioria das linguagens trata variância de tipo de função
- Erros claros quando regras de variância são violadas

---

## Apêndice: Mudanças de Sintaxe

```ebnf
(* Tipos *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* Statements *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" marca método opcional, block fornece implementação padrão *)

(* Parâmetros *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
