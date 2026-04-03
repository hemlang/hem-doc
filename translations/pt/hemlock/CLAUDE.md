# Filosofia de Design da Linguagem Hemlock

> "Uma linguagem pequena e não-segura, para escrever código não-seguro de forma segura."

Este documento registra os princípios de design centrais que assistentes de IA precisam conhecer ao trabalhar com Hemlock.
Para documentação detalhada, consulte `docs/README.md` e o diretório `stdlib/docs/`.

---

## Posicionamento Central

Hemlock é uma **linguagem de script de sistemas**, com gerenciamento manual de memória e controle explícito:
- Poder da linguagem C com conveniência de script moderno
- Concorrência assíncrona estruturada integrada
- Sem comportamentos ocultos ou mágica

**Hemlock não é:** Segura em memória, com coleta de lixo, nem esconde complexidade.
**Hemlock é:** Explícito é melhor que implícito, educacional, uma "camada de script C" para trabalho de sistemas.

---

## Princípios de Design

### 1. Explícito é Melhor que Implícito
- Ponto e vírgula é obrigatório (sem inserção automática)
- Gerenciamento manual de memória (alloc/free)
- Anotações de tipo opcionais, mas verificadas em runtime

### 2. Dinâmico por Padrão, Tipos Opcionais
- Todo valor tem tag de tipo em runtime
- Literais inferem tipos: `42` → i32, `5000000000` → i64, `3.14` → f64
- Anotações de tipo opcionais forçam verificação em runtime

### 3. Não-Seguro é um Recurso
- Aritmética de ponteiros é permitida (responsabilidade do usuário)
- `ptr` bruto não tem verificação de limites (use `buffer` para segurança)
- Double free é permitido causar crash

### 4. Concorrência Estruturada como Cidadã de Primeira Classe
- `async`/`await` integrados, paralelismo baseado em pthread
- Channels para comunicação
- `spawn`/`join`/`detach` para gerenciamento de tasks

### 5. Sintaxe Semelhante a C
- Blocos `{}` são sempre obrigatórios
- Comentários: `// linha` e `/* bloco */`
- Operadores como C: `+`, `-`, `*`, `%`, `&&`, `||`, `!`, `&`, `|`, `^`, `<<`, `>>`
- Incremento/decremento: `++x`, `x++`, `--x`, `x--` (prefixo e pós-fixo)
- Atribuição composta: `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`
- `/` sempre retorna ponto flutuante (use `divi()` para divisão inteira)
- Sintaxe de tipos: `let x: type = value;`

---

## Referência Rápida

### Tipos
```
Com sinal:     i8, i16, i32, i64
Sem sinal:    u8, u16, u32, u64
Ponto flut:   f32, f64
Outros:       bool, string, rune, array, ptr, buffer, null, object, file, task, channel
Aliases:      integer (i32), number (f64), byte (u8)
```

**Promoção de tipos:** i8 → i16 → i32 → i64 → f32 → f64 (ponto flutuante sempre vence, mas i64/u64 + f32 → f64 para manter precisão)

### Literais
```hemlock
let x = 42;              // i32
let big = 5000000000;    // i64 (> máx i32)
let hex = 0xDEADBEEF;    // Literal hexadecimal
let bin = 0b1010;        // Literal binário
let oct = 0o777;         // Literal octal
let sep = 1_000_000;     // Separador de dígitos permitido
let pi = 3.14;           // f64
let half = .5;           // f64 (sem zero inicial)
let s = "hello";         // string
let esc = "\x41\u{1F600}"; // Escapes hex e Unicode
let ch = 'A';            // rune
let emoji = '🚀';        // rune (Unicode)
let arr = [1, 2, 3];     // array
let obj = { x: 10 };     // object
```

### Conversão de Tipos
```hemlock
// Construtores de tipo - parsear strings para tipos
let n = i32("42");       // Parsear string para i32
let f = f64("3.14");     // Parsear string para f64
let b = bool("true");    // Parsear string para bool ("true" ou "false")

// Todos os tipos numéricos suportados
let a = i8("-128");      // i8, i16, i32, i64
let c = u8("255");       // u8, u16, u32, u64
let d = f32("1.5");      // f32, f64

// Hex e negativos
let hex = i32("0xFF");   // 255
let neg = i32("-42");    // -42

// Aliases de tipo também funcionam
let x = integer("100");  // Igual a i32("100")
let y = number("1.5");   // Igual a f64("1.5")
let z = byte("200");     // Igual a u8("200")

// Conversão entre tipos numéricos
let big = i64(42);       // i32 para i64
let truncated = i32(3.99); // f64 para i32 (trunca para 3)

// Anotações de tipo validam tipos (mas não parseiam strings)
let f: f64 = 100;        // i32 convertido para f64 via anotação (coerção numérica funciona)
// let n: i32 = "42";    // Erro - use i32("42") para parsear strings
```

### Introspecção
```hemlock
typeof(42);              // "i32"
typeof("hello");         // "string"
typeof([1, 2, 3]);       // "array"
typeof(null);            // "null"
len("hello");            // 5 (comprimento em bytes da string)
len([1, 2, 3]);          // 3 (comprimento do array)
```

### Memória
```hemlock
let p = alloc(64);       // Ponteiro bruto
let b = buffer(64);      // Buffer seguro (verificação de limites)
memset(p, 0, 64);
memcpy(dest, src, 64);
free(p);                 // Limpeza manual necessária
```

### Fluxo de Controle
```hemlock
if (x > 0) { } else if (x < 0) { } else { }
while (cond) { break; continue; }
for (let i = 0; i < 10; i++) { }
for (item in array) { }
loop { if (done) { break; } }   // Loop infinito (mais claro que while(true))
switch (x) { case 1: break; default: break; }  // Fall-through estilo C
defer cleanup();         // Executa quando função retorna

// Labels de loop para break/continue direcionado em loops aninhados
outer: while (cond) {
    inner: for (let i = 0; i < 10; i++) {
        if (i == 5) { break outer; }     // Sai do loop externo
        if (i == 3) { continue outer; }  // Continua loop externo
    }
}
```

### Pattern Matching
```hemlock
// Expressão match - retorna um valor
let result = match (value) {
    0 => "zero",                    // Padrão literal
    1 | 2 | 3 => "small",           // Padrão OR
    n if n < 10 => "medium",        // Expressão guard
    n => "large: " + n              // Binding de variável
};

// Padrões de tipo
match (val) {
    n: i32 => "integer",
    s: string => "string",
    _ => "other"                    // Wildcard
}

// Desestruturação de objeto
match (point) {
    { x: 0, y: 0 } => "origin",
    { x, y } => "at " + x + "," + y
}

// Desestruturação de array com rest
match (arr) {
    [] => "empty",
    [first, ...rest] => "head: " + first,
    _ => "other"
}

// Padrões aninhados
match (user) {
    { name, address: { city } } => name + " in " + city
}
```

Veja `docs/language-guide/pattern-matching.md` para documentação completa.

### Operadores de Coalescência Nula
```hemlock
// Coalescência nula (??) - retorna lado esquerdo se não-null, senão lado direito
let name = user.name ?? "Anonymous";
let first = a ?? b ?? c ?? "fallback";

// Atribuição de coalescência nula (??=) - atribui apenas se null
let config = null;
config ??= { timeout: 30 };    // config agora é { timeout: 30 }
config ??= { timeout: 60 };    // config não muda (não-null)

// Funciona com propriedades e índices
obj.field ??= "default";
arr[0] ??= "first";

// Navegação segura (?.) - retorna null se objeto é null
let city = user?.address?.city;  // null se qualquer parte é null
let upper = name?.to_upper();    // Chamada de método segura
let item = arr?.[0];             // Indexação segura
```

### Funções
```hemlock
fn add(a: i32, b: i32): i32 { return a + b; }
fn greet(name: string, msg?: "Hello") { print(msg + " " + name); }
let f = fn(x) { return x * 2; };  // Anônima/closure

// Funções com corpo de expressão (sintaxe arrow)
fn double(x: i32): i32 => x * 2;
fn max(a: i32, b: i32): i32 => a > b ? a : b;
let square = fn(x: i32): i32 => x * x;  // Corpo de expressão anônimo

// Modificadores de parâmetros
fn swap(ref a: i32, ref b: i32) { let t = a; a = b; b = t; }  // Passagem por referência
fn print_all(const items: array) { for (i in items) { print(i); } }  // Imutável
```

### Parâmetros Nomeados
```hemlock
// Funções podem ser chamadas com parâmetros nomeados
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " is " + age + " years old");
}

// Parâmetros posicionais (tradicional)
create_user("Alice", 25, false);

// Parâmetros nomeados - qualquer ordem
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);

// Pular parâmetros opcionais nomeando os desejados
create_user("David", active: false);  // Usa age=18 padrão

// Parâmetros nomeados devem vir depois dos posicionais
create_user("Eve", age: 21);          // OK: posicional primeiro, nomeado depois
// create_user(name: "Bad", 25);      // Erro: posicional depois de nomeado
```

**Regras:**
- Parâmetros nomeados usam sintaxe `name: value`
- Podem aparecer em qualquer ordem após parâmetros posicionais
- Parâmetros posicionais não podem seguir nomeados
- Funcionam com parâmetros padrão/opcionais
- Nomes de parâmetros desconhecidos causam erro de runtime

### Objetos e Enums
```hemlock
define Person { name: string, age: i32, active?: true }
let p: Person = { name: "Alice", age: 30 };
let json = p.serialize();
let restored = json.deserialize();

// Sintaxe abreviada de objeto (estilo ES6)
let name = "Alice";
let age = 30;
let person = { name, age };         // Igual a { name: name, age: age }

// Operador spread de objeto
let defaults = { theme: "dark", size: "medium" };
let config = { ...defaults, size: "large" };  // Copia defaults, sobrescreve size

enum Color { RED, GREEN, BLUE }
enum Status { OK = 0, ERROR = 1 }
```

### Tipos Compostos (Interseção/Duck Typing)
```hemlock
// Definir tipos estruturais
define HasName { name: string }
define HasAge { age: i32 }
define HasEmail { email: string }

// Tipo composto: objeto deve satisfazer todos os tipos
let person: HasName & HasAge = { name: "Alice", age: 30 };

// Parâmetros de função com tipos compostos
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

// Três ou mais tipos
fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}

// Campos extras permitidos (duck typing)
let employee: HasName & HasAge = {
    name: "Bob",
    age: 25,
    department: "Engineering"  // OK - campos extras ignorados
};
```

Tipos compostos fornecem comportamento similar a interfaces sem palavra-chave `interface` separada,
construindo sobre os paradigmas existentes de `define` e duck typing.

### Aliases de Tipo
```hemlock
// Alias de tipo simples
type Integer = i32;
type Text = string;

// Aliases de tipo de função
type Callback = fn(i32): void;
type Predicate = fn(i32): bool;
type AsyncHandler = async fn(string): i32;

// Aliases de tipo composto (bom para interfaces reutilizáveis)
define HasName { name: string }
define HasAge { age: i32 }
type Person = HasName & HasAge;

// Aliases de tipo genérico
type Pair<T> = { first: T, second: T };

// Usando aliases de tipo
let x: Integer = 42;
let cb: Callback = fn(n) { print(n); };
let p: Person = { name: "Alice", age: 30 };
```

Aliases de tipo criam atalhos nomeados para tipos complexos, melhorando legibilidade e manutenibilidade.

### Tipos de Função
```hemlock
// Anotações de tipo de função para parâmetros
fn apply_fn(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Funções de alta ordem que retornam funções
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tipos de função async
fn run_async(handler: async fn(): void) {
    spawn(handler);
}

// Tipos de função com múltiplos parâmetros
type BinaryOp = fn(i32, i32): i32;
let add: BinaryOp = fn(a, b) { return a + b; };
```

### Parâmetros Const
```hemlock
// Parâmetros const - imutabilidade profunda
fn print_all(const items: array) {
    // items.push(4);  // Erro: não pode modificar parâmetro const
    for (item in items) {
        print(item);
    }
}

// Const em objetos - não pode modificar por nenhum caminho
fn describe(const person: object) {
    print(person.name);       // OK: leitura permitida
    // person.name = "Bob";   // Erro: não pode modificar
}

// Acesso de leitura aninhado permitido
fn get_city(const user: object) {
    return user.address.city;  // OK: leitura de propriedade aninhada
}
```

O modificador `const` previne qualquer modificação ao parâmetro, incluindo propriedades aninhadas.
Isso fornece segurança em tempo de compilação para funções que não devem modificar suas entradas.

### Parâmetros Ref (Passagem por Referência)
```hemlock
// Parâmetros ref - modificar variável do chamador diretamente
fn increment(ref x: i32) {
    x = x + 1;  // Modifica variável original
}

let count = 10;
increment(count);
print(count);  // 11 - valor original modificado

// Função swap clássica
fn swap(ref a: i32, ref b: i32) {
    let temp = a;
    a = b;
    b = temp;
}

let x = 1;
let y = 2;
swap(x, y);
print(x, y);  // 2 1

// Misturando parâmetros ref e normais
fn add_to(ref target: i32, amount: i32) {
    target = target + amount;
}

let total = 100;
add_to(total, 50);
print(total);  // 150
```

O modificador `ref` passa uma referência à variável do chamador, permitindo que a função a modifique diretamente.
Sem `ref`, tipos primitivos são passados por valor (copiados). Use `ref` quando precisar
modificar estado do chamador sem retornar um valor.

**Regras:**
- Parâmetros `ref` devem receber variáveis, não literais ou expressões
- Funciona com todos os tipos (primitivos, arrays, objetos)
- Combina com anotações de tipo: `ref x: i32`
- Não pode combinar com `const` (são opostos)

### Assinaturas de Método em Define
```hemlock
// Define com assinaturas de método (padrão interface)
define Comparable {
    value: i32,
    fn compare(other: Self): i32   // Assinatura de método requerida
}

// Objetos devem fornecer métodos requeridos
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Use ? para métodos opcionais
define Serializable {
    fn serialize(): string,        // Requerido
    fn pretty?(): string           // Método opcional
}

// Tipo Self refere-se ao tipo definido
define Cloneable {
    fn clone(): Self   // Retorna mesmo tipo que o objeto
}
```

Assinaturas de método em blocos `define` são separadas por vírgula (similar a interfaces TypeScript),
estabelecendo contratos que objetos devem satisfazer e habilitando padrões de programação tipo-interface
através do sistema de duck typing do Hemlock.

### Tratamento de Erros
```hemlock
try { throw "error"; } catch (e) { print(e); } finally { cleanup(); }
panic("unrecoverable");  // Sai imediatamente, não pode ser capturado
```

### Async/Concorrência
```hemlock
async fn compute(n: i32): i32 { return n * n; }
let task = spawn(compute, 42);
let result = await task;     // Ou join(task)
detach(spawn(background_work));

let ch = channel(10);
ch.send(value);
let val = ch.recv();
ch.close();
```

**Ownership de memória:** Tasks recebem cópias de valores primitivos, mas compartilham ponteiros. Se você passa um `ptr` para uma task gerada,
você deve garantir que a memória permanece válida até a task completar. Use `join()` antes de `free()`,
ou use channels para sinalizar conclusão.

### Entrada de Usuário
```hemlock
let name = read_line();          // Lê linha de stdin (bloqueante)
print("Hello, " + name);
write("sem quebra de linha");    // Imprimir sem quebra de linha final
eprint("Error message");         // Saída para stderr

// read_line() retorna null em EOF
while (true) {
    let line = read_line();
    if (line == null) { break; }
    print("Got:", line);
}
```

### I/O de Arquivos
```hemlock
let f = open("file.txt", "r");  // Modos: r, w, a, r+, w+, a+
let content = f.read();
f.write("data");
f.seek(0);
f.close();
```

### Sinais
```hemlock
signal(SIGINT, fn(sig) { print("Interrupted"); });
raise(SIGUSR1);
```

---

## Métodos de String (19)

`substr`, `slice`, `find`, `contains`, `split`, `trim`, `to_upper`, `to_lower`,
`starts_with`, `ends_with`, `replace`, `replace_all`, `repeat`, `char_at`,
`byte_at`, `chars`, `bytes`, `to_bytes`, `deserialize`

Template strings: `` `Hello ${name}!` ``

**Mutabilidade de strings:** Strings são mutáveis via atribuição por índice (`s[0] = 'H'`), mas todos os métodos de string
retornam novas strings sem modificar a original. Isso permite modificação in-place quando necessário enquanto mantém
estilo funcional para encadeamento de métodos.

**Propriedades de comprimento de string:**
```hemlock
let s = "hello 🚀";
print(s.length);       // 7 (contagem de caracteres/runes)
print(s.byte_length);  // 10 (contagem de bytes - emoji é 4 bytes UTF-8)
```

## Métodos de Array (23)

`push`, `pop`, `shift`, `unshift`, `insert`, `remove`, `find`, `contains`,
`slice`, `join`, `concat`, `reverse`, `first`, `last`, `clear`, `map`, `filter`, `reduce`,
`every`, `some`, `indexOf`, `sort`, `fill`

```hemlock
// every(predicate) - true se todos os elementos satisfazem o predicado
let allPositive = [1, 2, 3].every(fn(x) { return x > 0; });  // true

// some(predicate) - true se algum elemento satisfaz o predicado
let hasEven = [1, 2, 3].some(fn(x) { return x % 2 == 0; });  // true

// indexOf(value) - encontra primeiro indice do valor, ou -1
let idx = ["a", "b", "c"].indexOf("b");  // 1

// sort(comparator?) - ordena in-place, comparador opcional
let nums = [3, 1, 4, 1, 5];
nums.sort();                              // [1, 1, 3, 4, 5]
nums.sort(fn(a, b) { return b - a; });    // descendente

// fill(value, start?, end?) - preenche com valor
let arr = [1, 2, 3, 4, 5];
arr.fill(0);        // [0, 0, 0, 0, 0]
arr.fill(9, 2);     // [0, 0, 9, 9, 9]
arr.fill(7, 1, 4);  // [0, 7, 7, 7, 9]
```

Arrays tipados: `let nums: array<i32> = [1, 2, 3];`

---

## Biblioteca Padrão (42 módulos)

Importar com prefixo `@stdlib/`:
```hemlock
import { sin, cos, PI } from "@stdlib/math";
import { HashMap, Queue, Set } from "@stdlib/collections";
import { read_file, write_file } from "@stdlib/fs";
import { TcpStream, UdpSocket } from "@stdlib/net";
```

| Módulo | Descrição |
|--------|-----------|
| `arena` | Alocador de memória arena (alocação bump) |
| `args` | Parsing de argumentos de linha de comando |
| `assert` | Utilitários de asserção |
| `async` | ThreadPool, parallel_map |
| `async_fs` | Operações de I/O de arquivos assíncronas |
| `collections` | HashMap, Queue, Stack, Set, LinkedList, LRUCache |
| `compression` | gzip, gunzip, deflate |
| `crypto` | aes_encrypt, rsa_sign, random_bytes |
| `csv` | Parsing e geração de CSV |
| `datetime` | Classe DateTime, formatação, parsing |
| `encoding` | base64_encode, hex_encode, url_encode |
| `env` | getenv, setenv, exit, get_pid |
| `fmt` | Utilitários de formatação de string |
| `fs` | read_file, write_file, list_dir, exists |
| `glob` | Matching de padrões de arquivo |
| `hash` | sha256, sha512, md5, djb2 |
| `http` | http_get, http_post, http_request |
| `ipc` | Comunicação entre processos |
| `iter` | Utilitários de iterador |
| `json` | parse, stringify, pretty, get, set |
| `logging` | Logger com níveis |
| `math` | sin, cos, sqrt, pow, rand, PI, E |
| `net` | TcpListener, TcpStream, UdpSocket |
| `os` | platform, arch, cpu_count, hostname |
| `path` | Manipulação de caminhos de arquivo |
| `process` | fork, exec, wait, kill |
| `random` | Geração de números aleatórios |
| `regex` | compile, test (POSIX ERE) |
| `retry` | Lógica de retry com backoff |
| `semver` | Versionamento semântico |
| `shell` | Utilitários de comandos shell |
| `sqlite` | SQLite database, query, exec, transações |
| `strings` | pad_left, is_alpha, reverse, lines |
| `terminal` | Cores e estilos ANSI |
| `termios` | Entrada de terminal bruta, detecção de teclas |
| `testing` | describe, test, expect |
| `time` | now, time_ms, sleep, clock |
| `toml` | Parsing e geração de TOML |
| `url` | Parsing e manipulação de URL |
| `uuid` | Geração de UUID |
| `vector` | Busca de similaridade vetorial (USearch ANN) |
| `websocket` | Cliente WebSocket |

Veja `stdlib/docs/` para documentação detalhada dos módulos.

---

## FFI (Interface de Função Estrangeira)

Declarar e chamar funções C de bibliotecas compartilhadas:
```hemlock
import "libc.so.6";

extern fn strlen(s: string): i32;
extern fn getpid(): i32;

let len = strlen("Hello!");  // 6
let pid = getpid();
```

Exportar funções FFI de módulos:
```hemlock
// string_utils.hml
import "libc.so.6";

export extern fn strlen(s: string): i32;
export fn string_length(s: string): i32 {
    return strlen(s);
}
```

FFI dinâmico (binding em runtime):
```hemlock
let lib = ffi_open("libc.so.6");
let puts = ffi_bind(lib, "puts", [FFI_POINTER], FFI_INT);
puts("Hello from C!");
ffi_close(lib);
```

Tipos: `FFI_INT`, `FFI_DOUBLE`, `FFI_POINTER`, `FFI_STRING`, `FFI_VOID`, etc.

---

## Operações Atômicas

Use operações atômicas para programação concorrente sem locks:

```hemlock
// Alocar memória para i32 atômico
let p = alloc(4);
ptr_write_i32(p, 0);

// Load/store atômico
let val = atomic_load_i32(p);        // Leitura atômica
atomic_store_i32(p, 42);             // Escrita atômica

// Operações fetch-and-modify (retornam valor antigo)
let old = atomic_add_i32(p, 10);     // Adiciona, retorna antigo
old = atomic_sub_i32(p, 5);          // Subtrai, retorna antigo
old = atomic_and_i32(p, 0xFF);       // AND bit a bit
old = atomic_or_i32(p, 0x10);        // OR bit a bit
old = atomic_xor_i32(p, 0x0F);       // XOR bit a bit

// Compare-and-swap (CAS)
let success = atomic_cas_i32(p, 42, 100);  // Se *p == 42, seta para 100
// Retorna true se swap ocorreu, false caso contrário

// Atomic exchange
old = atomic_exchange_i32(p, 999);   // Troca, retorna antigo

free(p);

// Variantes i64 disponíveis (atomic_load_i64, atomic_add_i64, etc.)

// Barreira de memória (barreira completa)
atomic_fence();
```

Todas as operações usam consistência sequencial (`memory_order_seq_cst`).

---

## Estrutura do Projeto

```
hemlock/
├── src/
│   ├── frontend/         # Compartilhado: lexer, parser, AST, módulos
│   ├── backends/
│   │   ├── interpreter/  # hemlock: interpretador tree-walking
│   │   └── compiler/     # hemlockc: gerador de código C
│   ├── tools/
│   │   ├── lsp/          # Language Server Protocol
│   │   └── bundler/      # Ferramenta de bundling/pacotes
├── runtime/              # Runtime de programas compilados (libhemlock_runtime.a)
├── stdlib/               # Biblioteca padrão (42 módulos)
│   └── docs/             # Documentação dos módulos
├── docs/                 # Documentação completa
│   ├── language-guide/   # Tipos, strings, arrays, etc.
│   ├── reference/        # Referência de API
│   └── advanced/         # Async, FFI, sinais, etc.
├── tests/                # 625+ testes
└── examples/             # Programas de exemplo
```

---

## Guia de Estilo de Código

### Constantes e Números Mágicos

Ao adicionar constantes numéricas ao código C, siga estas diretrizes:

1. **Definir constantes em `include/hemlock_limits.h`** - Este arquivo é o local centralizado para todos os limites de compile-time e runtime, capacidades e constantes nomeadas.

2. **Usar nomes descritivos com prefixo `HML_`** - Todas as constantes devem ser prefixadas com `HML_` para namespace claro.

3. **Evitar números mágicos** - Substituir valores numéricos hardcoded com constantes nomeadas. Exemplos:
   - Limites de intervalo de tipos: `HML_I8_MIN`, `HML_I8_MAX`, `HML_U32_MAX`
   - Capacidades de buffer: `HML_INITIAL_ARRAY_CAPACITY`, `HML_INITIAL_LEXER_BUFFER_CAPACITY`
   - Conversões de tempo: `HML_NANOSECONDS_PER_SECOND`, `HML_MILLISECONDS_PER_SECOND`
   - Seeds de hash: `HML_DJB2_HASH_SEED`
   - Valores ASCII: `HML_ASCII_CASE_OFFSET`, `HML_ASCII_PRINTABLE_START`

4. **Incluir `hemlock_limits.h`** - Arquivos fonte devem incluir este header (tipicamente via `internal.h`) para acessar constantes.

5. **Documentar propósito** - Adicionar comentários explicando o que cada constante representa.

---

## Proibições

- Adicionar comportamento implícito (ASI, GC, limpeza automática)
- Esconder complexidade (otimizações mágicas, contagem de referência oculta)
- Quebrar semântica existente (ponto e vírgula, memória manual, strings mutáveis)
- Perder precisão em conversões implícitas
- Usar números mágicos - em vez disso, defina constantes nomeadas em `hemlock_limits.h`

---

## Testes

```bash
make test              # Executar testes do interpretador
make test-compiler     # Executar testes do compilador
make parity            # Executar testes de paridade (ambos devem coincidir)
make test-all          # Executar todas as suítes de teste
```

**Importante:** Testes podem travar devido a problemas de async/concorrência. Sempre use timeout ao executar testes:
```bash
timeout 60 make test   # Timeout de 60 segundos
timeout 120 make parity
```

Categorias de testes: primitives, memory, strings, arrays, functions, objects, async, ffi, defer, signals, switch, bitwise, typed_arrays, modules, stdlib_*

---

## Arquitetura Compilador/Interpretador

Hemlock tem dois backends de execução que compartilham um frontend comum:

```
Fonte (.hml)
    ↓
┌─────────────────────────────┐
│  Frontend Compartilhado      │
│  - Lexer (src/frontend/)     │
│  - Parser (src/frontend/)    │
│  - AST (src/frontend/)       │
└─────────────────────────────┘
    ↓                    ↓
┌────────────┐    ┌────────────┐
│ Interpretador │  │ Compilador  │
│ (hemlock)     │  │ (hemlockc)  │
│               │  │             │
│ Tree-walking  │  │ Type check  │
│ Avaliação     │  │ AST → C     │
│               │  │ gcc link    │
└────────────┘    └────────────┘
```

### Verificação de Tipos do Compilador

O compilador (`hemlockc`) inclui verificação de tipos em compile-time, **habilitada por padrão**:

```bash
hemlockc program.hml -o program    # Verifica tipos, depois compila
hemlockc --check program.hml       # Apenas verifica tipos, não compila
hemlockc --no-type-check prog.hml  # Desabilita verificação de tipos
hemlockc --strict-types prog.hml   # Avisa sobre tipos 'any' implícitos
```

O verificador de tipos:
- Valida anotações de tipo em compile-time
- Trata código sem tipos como dinâmico (tipo `any`) - sempre válido
- Fornece dicas de otimização para unboxing
- Usa conversão numérica permissiva (intervalos validados em runtime)

### Estrutura de Diretórios

```
hemlock/
├── src/
│   ├── frontend/           # Compartilhado: lexer, parser, AST, módulos
│   │   ├── lexer.c
│   │   ├── parser/
│   │   ├── ast.c
│   │   └── module.c
│   ├── backends/
│   │   ├── interpreter/    # hemlock: interpretador tree-walking
│   │   │   ├── main.c
│   │   │   ├── runtime/
│   │   │   └── builtins/
│   │   └── compiler/       # hemlockc: gerador de código C
│   │       ├── main.c
│   │       └── codegen/
│   ├── tools/
│   │   ├── lsp/            # Language server
│   │   └── bundler/        # Ferramenta de bundling/pacotes
├── runtime/                # libhemlock_runtime.a para programas compilados
├── stdlib/                 # Biblioteca padrão compartilhada
└── tests/
    ├── parity/             # Testes que devem passar em ambos backends
    ├── interpreter/        # Testes específicos do interpretador
    └── compiler/           # Testes específicos do compilador
```

---

## Desenvolvimento Parity-First

**Interpretador e compilador devem produzir saída idêntica para a mesma entrada.**

### Estratégia de Desenvolvimento

Ao adicionar ou modificar recursos da linguagem:

1. **Design** - Definir mudanças de AST/semântica no frontend compartilhado
2. **Implementar Interpretador** - Adicionar avaliação tree-walking
3. **Implementar Compilador** - Adicionar geração de código C
4. **Adicionar Testes de Paridade** - Escrever testes em `tests/parity/` com arquivos `.expected`
5. **Verificar** - Executar `make parity` antes de merge

### Estrutura de Testes de Paridade

```
tests/parity/
├── language/       # Recursos core da linguagem (fluxo de controle, closures, etc.)
├── builtins/       # Funções builtin (print, typeof, memory, etc.)
├── methods/        # Métodos de string e array
└── modules/        # import/export, imports de stdlib
```

Cada teste tem dois arquivos:
- `feature.hml` - Programa de teste
- `feature.expected` - Saída esperada (ambos backends devem coincidir)

### Resultados de Testes de Paridade

| Status | Significado |
|--------|-------------|
| `PASSED` | Interpretador e compilador coincidem com saída esperada |
| `INTERP_ONLY` | Interpretador funciona, compilador falha (precisa corrigir compilador) |
| `COMPILER_ONLY` | Compilador funciona, interpretador falha (raro) |
| `FAILED` | Ambos falham (erro de teste ou implementação) |

### O que Precisa de Paridade

- Todas as construções de linguagem (if, while, for, switch, defer, try/catch)
- Todos os operadores (aritméticos, bit a bit, lógicos, comparação)
- Todas as funções builtin (print, typeof, alloc, etc.)
- Todos os métodos de string e array
- Regras de coerção e promoção de tipos
- Mensagens de erro para erros de runtime

### O que Pode Diferir

- Características de performance
- Detalhes de layout de memória
- Formato de debug/stack trace
- Erros de compilação (compilador pode capturar mais em compile-time)

### Adicionando Testes de Paridade

```bash
# 1. Criar arquivo de teste
cat > tests/parity/language/my_feature.hml << 'EOF'
// Descrição do teste
let x = some_feature();
print(x);
EOF

# 2. Gerar saída esperada do interpretador
./hemlock tests/parity/language/my_feature.hml > tests/parity/language/my_feature.expected

# 3. Verificar paridade
make parity
```

---

## Versão

**v1.9.2** - Recursos da versão atual:
- **Correção do contador de loop unboxed do compilador** - Corrigido um bug crítico de codegen onde contadores de loop otimizados (native `int32_t`) eram usados diretamente como inicializadores `HmlValue` sem boxing. A verificação `codegen_is_main_var` impedia incorretamente a emissão do wrapper de boxing (`hml_val_i32()`) quando uma variável de nível main sombreava um contador de loop unboxed dentro de uma função módulo/closure. Corrige compilação de `@stdlib/collections` e `@stdlib/encoding`.
- **Dispatch de método de objeto `clear()`** - O compilador agora despacha corretamente `.clear()` para métodos de objeto quando chamado em tipos não-array. Anteriormente, `.clear()` sempre gerava `hml_array_clear()` independentemente do tipo do receptor.
- **Correção de shadowing de import `exec()`** - O handler builtin `exec()` do compilador agora verifica bindings de import e funções locais do módulo antes de despachar para o builtin exec do sistema. Corrige `@stdlib/sqlite` que exporta sua própria função `exec()`.

**v1.9.1** - Versão anterior com:
- **Builtin `write()`** - Imprimir sem quebra de linha final (`write("hello"); write(" world");` imprime em uma linha). Inclui `fflush(stdout)` para saída imediata. Paridade total entre interpretador e compilador.
- **`slice()` de argumento único** - `arr.slice(n)` e `str.slice(n)` agora usam o comprimento como fim padrão, correspondendo ao comportamento JS/Python. A forma de dois argumentos permanece inalterada.
- **`join()` em arrays de runes** - `"hello".chars().join("")` agora produz corretamente `"hello"` em vez de `"[object][object]..."`. Permite inversão idiomática de string: `str.chars().reverse().join("")`.
- **Coerção de chaves numéricas HashMap** - Chaves de tipos numéricos diferentes agora correspondem (ex.: chave `i32` encontrada por lookup `i64`). Anteriormente, o guard `typeof()` em `keys_equal()` rejeitava correspondências cross-type válidas.
- **Melhorias HemBench** - Definições de tarefas corrigidas (arredondamento L1-M-02, precisão L2-E-01), parou de vazar saída esperada para tarefas benchmark L5/L6.
- **Builtins `ptr_read_*` completos** - Adicionados `ptr_read_i8`, `ptr_read_i16`, `ptr_read_i64`, `ptr_read_u8`, `ptr_read_u16`, `ptr_read_u32`, `ptr_read_u64`, `ptr_read_f32`, `ptr_read_f64`, `ptr_read_ptr` para complementar funções `ptr_write_*` existentes. Corrigido `ptr_read_i32` para dereferência direta (era dereferência dupla). Paridade total entre interpretador e compilador.
- **Carregamento de bibliotecas FFI macOS** - `dlopen` agora busca em `/usr/local/lib` e `/opt/homebrew/lib` como caminhos de fallback no macOS, corrigindo erros de biblioteca não encontrada para bibliotecas compartilhadas instaladas pelo usuário (ex.: libusearch_c).
- **Correção `@stdlib/vector` USearch v2** - `create_index()` agora chama `usearch_reserve()` após init, corrigindo segfault com USearch v2.24+ que requer pré-alocação antes de adicionar vetores.

**v1.9.0** - Versão anterior com:
- **Artefato de release do interpretador WASM** - Interpretador WASM pré-compilado incluído nas releases do GitHub para uso em navegador/Node.js
- **Correções de inlining do compilador** - Corrigida corrupção de argumentos de chamada aninhada e colisão de unboxing com contadores de loop durante inlining de função (corrige compilação do hemloco)
- **Subtração de ponteiros** - O verificador de tipos do compilador agora permite `ptr - integer` para aritmética de ponteiros
- **Exceções `open()` capturáveis** - `open()` agora lança via `hml_throw()` em vez de `exit(1)`, habilitando tratamento de erros com try/catch
- **Correção de print/eprint multi-argumento** - Corrigido codegen do compilador para `print()` e `eprint()` com múltiplos argumentos (ex.: `print("x:", x, y)`)
- **Correção de string SSO** - Corrigido segfault em `hml_string_append_inplace` ao crescer strings usando Small String Optimization
- **Módulo `@stdlib/termios`** - Entrada de terminal bruta cross-platform (Linux/macOS):
  - `enable_raw_mode()` / `disable_raw_mode()` para teclas instantâneas
  - `read_key()` / `read_key_timeout(ms)` para leitura de tecla única
  - Detecção de teclas de seta, teclas de função, teclas de controle
  - `is_terminal()` para verificar se stdin é um TTY
  - Documentação em `stdlib/docs/termios.md`
- **Prevenção de vazamento de memória** - Correções abrangentes garantindo que o runtime é livre de vazamentos:
  - Avaliação de expressão segura contra exceções (arrays, objetos, chamadas de função)
  - Retain/release correto do resultado de task em join()
  - Drenagem de channel ao fechar (libera valores bufferizados)
  - Limpeza do otimizador para constant folding de coalescência nula
  - Suite de testes de regressão de vazamentos (`make leak-regression`)
  - Documentação de ownership de memória (`docs/advanced/memory-ownership.md`)
- **Pattern Matching** (expressões `match`) - Desestruturação poderosa e fluxo de controle:
  - Padrões literal, wildcard e binding de variável
  - Padrões OR (`1 | 2 | 3`)
  - Expressões guard (`n if n > 0`)
  - Desestruturação de objeto (`{ x, y }`)
  - Desestruturação de array com rest (`[first, ...rest]`)
  - Padrões de tipo (`n: i32`)
  - Paridade total entre interpretador e compilador
- **Anotações de Assistência ao Compilador** - 11 anotações de otimização para controle de GCC/Clang:
  - `@inline`, `@noinline` - Controle de inlining de função
  - `@hot`, `@cold` - Dicas de predição de branch
  - `@pure`, `@const` - Anotações de side-effect
  - `@flatten` - Inline todas as chamadas dentro da função
  - `@optimize(level)` - Nível de otimização por função ("0", "1", "2", "3", "s", "fast")
  - `@warn_unused` - Aviso quando valor de retorno é ignorado
  - `@section(name)` - Colocação de seção ELF customizada (ex: `@section(".text.hot")`)
- **Funções com corpo de expressão** (`fn double(x): i32 => x * 2;`) - Sintaxe concisa para funções de expressão única
- **Statements de linha única** - Sintaxe sem chaves para `if`, `while`, `for` (ex: `if (x > 0) print(x);`)
- **Aliases de tipo** (`type Name = Type;`) - Atalhos nomeados para tipos complexos
- **Anotações de tipo de função** (`fn(i32): i32`) - Tipos de função de primeira classe
- **Parâmetros const** (`fn(const x: array)`) - Imutabilidade profunda para parâmetros
- **Parâmetros ref** (`fn(ref x: i32)`) - Passagem por referência para modificar chamador diretamente
- **Assinaturas de método em define** (`fn method(): Type`) - Contratos tipo-interface (separados por vírgula)
- **Tipo Self** em assinaturas de método - Referência ao tipo definido
- **Palavra-chave loop** (`loop { }`) - Loop infinito mais claro, substitui `while (true)`
- **Labels de loop** (`outer: while`) - Break/continue direcionado para loops aninhados
- **Abreviação de objeto** (`{ name }`) - Sintaxe de propriedade abreviada estilo ES6
- **Spread de objeto** (`{ ...obj }`) - Copiar e mesclar campos de objeto
- **Duck typing composto** (`A & B & C`) - Tipos de interseção para tipos estruturais
- **Parâmetros nomeados** para chamadas de função (`foo(name: "value", age: 30)`)
- **Operadores de coalescência nula** (`??`, `??=`, `?.`) para tratamento seguro de null
- **Literais octais** (`0o777`, `0O123`)
- **Separadores de dígitos** (`1_000_000`, `0xFF_FF`, `0b1111_0000`)
- **Comentários de bloco** (`/* ... */`)
- **Sequências de escape hex** em strings/runes (`\x41` = 'A')
- **Sequências de escape Unicode** em strings (`\u{1F600}` = 😀)
- **Literais float sem zero inicial** (`.5`, `.123`, `.5e2`)
- **Verificação de tipos em compile-time** em hemlockc (habilitada por padrão)
- **Integração LSP** com verificação de tipos com diagnósticos em tempo real
- **Operadores de atribuição composta** (`+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `<<=`, `>>=`)
- **Operadores de incremento/decremento** (`++x`, `x++`, `--x`, `x--`)
- **Correção de precisão de tipos**: i64/u64 + f32 → f64 para manter precisão
- Sistema de tipos unificado com dicas de otimização de unboxing
- Sistema de tipos completo (i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object, enum, file, task, channel)
- Strings UTF-8 com 19 métodos
- Arrays com 23 métodos incluindo map/filter/reduce/every/some/indexOf/sort/fill
- Gerenciamento manual de memória com `talloc()` e `sizeof()`
- Async/await com paralelismo pthread real
- Operações atômicas para programação concorrente sem locks
- 42 módulos de stdlib (+ arena, assert, semver, toml, retry, iter, random, shell, termios, vector)
- FFI para interop com C, com `export extern fn` para wrappers de biblioteca reutilizáveis
- Suporte a struct FFI no compilador (passando structs C por valor)
- Helpers de ponteiro FFI (`ptr_null`, `ptr_read_*`, `ptr_write_*`)
- defer, try/catch/finally/throw, panic
- I/O de arquivos, tratamento de sinais, execução de comandos
- Gerenciador de pacotes [hpm](https://github.com/hemlang/hpm) com registry baseado em GitHub
- Backend de compilador (geração de código C), 100% paridade com interpretador
- Servidor LSP com jump-to-definition e find-references
- Passes de otimização de AST e resolução de variáveis para lookup O(1)
- Builtin apply() para chamadas de função dinâmicas
- Channels sem buffer e suporte a múltiplos argumentos
- 159 testes de paridade (100% taxa de aprovação)

---

## Filosofia

> Nós fornecemos ferramentas seguras (`buffer`, anotações de tipo, verificação de limites), mas não forçamos você a usá-las (`ptr`, memória manual, operações não-seguras).

**Se você não tem certeza se um recurso cabe no Hemlock, pergunte-se: "Isso dá ao programador mais controle explícito, ou esconde algo?"**

Se esconde, provavelmente não pertence ao Hemlock.
