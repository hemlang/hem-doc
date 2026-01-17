# Referencia de Funcoes Integradas

Documentacao completa de todas as funcoes integradas e constantes do Hemlock.

---

## Visao Geral

Hemlock fornece um conjunto de funcoes integradas para I/O, introspeccao de tipos, gerenciamento de memoria, concorrencia e interacao com o sistema. Todas as funcoes integradas estao disponiveis globalmente sem necessidade de importacao.

---

## Funcoes de I/O

### print

Imprime valores na saida padrao com nova linha.

**Assinatura:**
```hemlock
print(...values): null
```

**Parametros:**
- `...values` - Qualquer numero de valores para imprimir

**Retorna:** `null`

**Exemplo:**
```hemlock
print("Hello, World!");
print(42);
print(3.14);
print(true);
print([1, 2, 3]);
print({ x: 10, y: 20 });

// Multiplos valores
print("x =", 10, "y =", 20);
```

**Comportamento:**
- Converte todos os valores para strings
- Multiplos valores separados por espacos
- Adiciona nova linha no final
- Libera a saida padrao

---

### read_line

Le uma linha de texto da entrada padrao (entrada do usuario).

**Assinatura:**
```hemlock
read_line(): string | null
```

**Parametros:** Nenhum

**Retorna:**
- `string` - A linha lida da entrada padrao (sem nova linha)
- `null` - Em EOF (fim de arquivo/entrada)

**Exemplo:**
```hemlock
// Prompt simples
print("Qual e o seu nome?");
let name = read_line();
print("Ola, " + name + "!");

// Lendo numero (requer parsing manual)
print("Digite um numero:");
let input = read_line();
let num = parse_int(input);  // Veja parse_int abaixo
print("Dobro:", num * 2);

// Tratando EOF
let line = read_line();
if (line == null) {
    print("Fim da entrada");
}

// Lendo multiplas linhas
print("Digite linhas (Ctrl+D para parar):");
while (true) {
    let line = read_line();
    if (line == null) {
        break;
    }
    print("Voce disse:", line);
}
```

**Comportamento:**
- Bloqueia ate o usuario pressionar Enter
- Remove nova linha final (`\n`) e retorno de carro (`\r`)
- Retorna `null` em EOF (Ctrl+D no Unix, Ctrl+Z no Windows)
- Le apenas da entrada padrao (nao de arquivo)

**Parseando Entrada do Usuario:**

Como `read_line()` sempre retorna string, voce precisa parsear entrada numerica manualmente:

```hemlock
// Parser de inteiro simples
fn parse_int(s: string): i32 {
    let result: i32 = 0;
    let negative = false;
    let i = 0;

    if (s.length > 0 && s.char_at(0) == '-') {
        negative = true;
        i = 1;
    }

    while (i < s.length) {
        let c = s.char_at(i);
        let code: i32 = c;
        if (code >= 48 && code <= 57) {
            result = result * 10 + (code - 48);
        } else {
            break;
        }
        i = i + 1;
    }

    if (negative) {
        return -result;
    }
    return result;
}

// Uso
print("Digite sua idade:");
let age = parse_int(read_line());
print("Em 10 anos voce tera", age + 10);
```

**Veja Tambem:** [API de Arquivos](file-api.md) para ler de arquivos

---

### eprint

Imprime valores na saida de erro padrao com nova linha.

**Assinatura:**
```hemlock
eprint(value: any): null
```

**Parametros:**
- `value` - Valor unico para imprimir na saida de erro padrao

**Retorna:** `null`

**Exemplo:**
```hemlock
eprint("Erro: arquivo nao encontrado");
eprint(404);
eprint("Aviso: " + message);

// Padrao tipico de tratamento de erros
fn load_config(path: string) {
    if (!exists(path)) {
        eprint("Erro: arquivo de configuracao nao encontrado: " + path);
        return null;
    }
    // ...
}
```

**Comportamento:**
- Imprime na saida de erro padrao (stderr)
- Adiciona nova linha no final
- Aceita apenas um argumento (diferente de `print`)
- Util para mensagens de erro que nao devem misturar com saida normal

**Diferenca de print:**
- `print()` -> stdout (saida normal, redirecionada com `>`)
- `eprint()` -> stderr (saida de erro, redirecionada com `2>`)

```bash
# Exemplo no shell: separando stdout e stderr
./hemlock script.hml > output.txt 2> errors.txt
```

---

## Introspeccao de Tipos

### typeof

Obtem o nome do tipo de um valor.

**Assinatura:**
```hemlock
typeof(value: any): string
```

**Parametros:**
- `value` - Qualquer valor

**Retorna:** String com o nome do tipo

**Exemplo:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("hello"));         // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof(null));            // "null"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

// Objetos tipados
define Person { name: string }
let p: Person = { name: "Alice" };
print(typeof(p));               // "Person"

// Outros tipos
print(typeof(alloc(10)));       // "ptr"
print(typeof(buffer(10)));      // "buffer"
print(typeof(open("file.txt"))); // "file"
```

**Nomes de Tipos:**
- Tipos primitivos: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Tipos compostos: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Tipos especiais: `"file"`, `"task"`, `"channel"`
- Tipos personalizados: Nomes de tipo definidos pelo usuario de `define`

**Veja Tambem:** [Sistema de Tipos](type-system.md)

---

## Execucao de Comandos

### exec

Executa um comando shell e captura a saida.

**Assinatura:**
```hemlock
exec(command: string): object
```

**Parametros:**
- `command` - O comando shell a executar

**Retorna:** Objeto contendo:
- `output` (string) - Saida padrao do comando
- `exit_code` (i32) - Codigo de saida (0 = sucesso)

**Exemplo:**
```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0

// Verifica status de saida
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Encontrado:", r.output);
} else {
    print("Padrao nao encontrado");
}

// Tratando saida multi-linha
let r2 = exec("ls -la");
let lines = r2.output.split("\n");
```

**Comportamento:**
- Executa comando via `/bin/sh`
- Captura apenas stdout (stderr vai para o terminal)
- Bloqueia ate o comando completar
- Retorna string vazia se nao houver saida

**Tratamento de Erros:**
```hemlock
try {
    let r = exec("comando_inexistente");
} catch (e) {
    print("Falha ao executar:", e);
}
```

**Aviso de Seguranca:** Risco de injecao de shell. Sempre valide/sanitize entrada do usuario.

**Limitacoes:**
- Sem captura de stderr
- Sem streaming
- Sem timeout
- Sem tratamento de sinais

---

### exec_argv

Executa um comando com array explicito de argumentos (sem interpretacao de shell).

**Assinatura:**
```hemlock
exec_argv(argv: array): object
```

**Parametros:**
- `argv` - Array de strings: `[comando, arg1, arg2, ...]`

**Retorna:** Objeto contendo:
- `output` (string) - Saida padrao do comando
- `exit_code` (i32) - Codigo de saida (0 = sucesso)

**Exemplo:**
```hemlock
// Comando simples
let result = exec_argv(["ls", "-la"]);
print(result.output);

// Argumentos com espacos (seguro!)
let r = exec_argv(["grep", "hello world", "file.txt"]);

// Executar script com argumentos
let r2 = exec_argv(["python", "script.py", "--input", "data.json"]);
print(r2.exit_code);
```

**Diferenca de exec:**
```hemlock
// exec() usa shell - inseguro para entrada do usuario
exec("ls " + user_input);  // Risco de injecao de shell!

// exec_argv() ignora shell - seguro
exec_argv(["ls", user_input]);  // Injecao impossivel
```

**Quando usar:**
- Quando argumentos contem espacos, aspas ou caracteres especiais
- Ao tratar entrada do usuario (seguranca)
- Quando voce precisa de parsing previsivel de argumentos

**Veja Tambem:** `exec()` para comandos de shell simples

---

## Tratamento de Erros

### throw

Lanca uma excecao.

**Assinatura:**
```hemlock
throw expression
```

**Parametros:**
- `expression` - Valor a ser lancado (qualquer tipo)

**Retorna:** Nunca retorna (transfere controle)

**Exemplo:**
```hemlock
throw "mensagem de erro";
throw 404;
throw { code: 500, message: "Erro interno" };
throw null;
```

**Veja Tambem:** Instrucao try/catch/finally

---

### panic

Encerra o programa imediatamente com mensagem de erro (irrecuperavel).

**Assinatura:**
```hemlock
panic(message?: any): never
```

**Parametros:**
- `message` (opcional) - Mensagem de erro a imprimir

**Retorna:** Nunca retorna (programa termina)

**Exemplo:**
```hemlock
panic();                          // Padrao: "panic!"
panic("codigo inalcancavel atingido");
panic(42);

// Caso de uso comum
fn process_state(state: i32): string {
    if (state == 1) { return "pronto"; }
    if (state == 2) { return "executando"; }
    panic("estado invalido: " + typeof(state));
}
```

**Comportamento:**
- Imprime erro na saida de erro padrao: `panic: <mensagem>`
- Termina com codigo 1
- **Nao pode** ser capturado com try/catch
- Use para bugs e erros irrecuperaveis

**panic vs throw:**
- `panic()` - Erro irrecuperavel, termina imediatamente
- `throw` - Erro recuperavel, pode ser capturado

---

### assert

Asserta que uma condicao e verdadeira, caso contrario termina com mensagem de erro.

**Assinatura:**
```hemlock
assert(condition: any, message?: string): null
```

**Parametros:**
- `condition` - Valor a verificar como verdadeiro
- `message` (opcional) - Mensagem de erro personalizada se assert falhar

**Retorna:** `null` (se assert passar)

**Exemplo:**
```hemlock
// Assert basico
assert(x > 0);
assert(name != null);
assert(arr.length > 0, "Array nao pode estar vazio");

// Com mensagem personalizada
fn divide(a: i32, b: i32): f64 {
    assert(b != 0, "Divisao por zero");
    return a / b;
}

// Validando argumentos de funcao
fn process_data(data: array) {
    assert(data != null, "data nao pode ser null");
    assert(data.length > 0, "data nao pode estar vazio");
    // ...
}
```

**Comportamento:**
- Se condicao for verdadeira: retorna `null`, continua execucao
- Se condicao for falsa: imprime erro e termina com codigo 1
- Valores falsos: `false`, `0`, `0.0`, `null`, `""` (string vazia)
- Valores verdadeiros: todo o resto

**Saida em Falha:**
```
Assertion failed: Array nao pode estar vazio
```

**Quando usar:**
- Validando pre-condicoes de funcoes
- Verificando invariantes durante desenvolvimento
- Capturando erros de programador cedo

**assert vs panic:**
- `assert(cond, msg)` - Verifica condicao, falha se falso
- `panic(msg)` - Falha incondicionalmente

---

## Tratamento de Sinais

### signal

Registra ou reseta um handler de sinal.

**Assinatura:**
```hemlock
signal(signum: i32, handler: function | null): function | null
```

**Parametros:**
- `signum` - Numero do sinal (use constantes como `SIGINT`)
- `handler` - Funcao a chamar quando sinal for recebido, ou `null` para resetar ao padrao

**Retorna:** Funcao handler anterior, ou `null`

**Exemplo:**
```hemlock
fn handle_interrupt(sig) {
    print("Capturado SIGINT!");
}

signal(SIGINT, handle_interrupt);

// Reseta ao padrao
signal(SIGINT, null);
```

**Assinatura do Handler:**
```hemlock
fn handler(signum: i32) {
    // signum contem o numero do sinal
}
```

**Veja Tambem:**
- [Constantes de Sinal](#constantes-de-sinal)
- `raise()`

---

### raise

Envia um sinal para o processo atual.

**Assinatura:**
```hemlock
raise(signum: i32): null
```

**Parametros:**
- `signum` - Numero do sinal a enviar

**Retorna:** `null`

**Exemplo:**
```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

raise(SIGUSR1);
raise(SIGUSR1);
print(count);  // 2
```

---

## Variaveis Globais

### args

Array de argumentos de linha de comando.

**Tipo:** `array` de strings

**Estrutura:**
- `args[0]` - Nome do arquivo do script
- `args[1..n]` - Argumentos de linha de comando

**Exemplo:**
```bash
# Comando: ./hemlock script.hml hello world
```

```hemlock
print(args[0]);        // "script.hml"
print(args.length);    // 3
print(args[1]);        // "hello"
print(args[2]);        // "world"

// Itera sobre argumentos
let i = 1;
while (i < args.length) {
    print("Argumento", i, ":", args[i]);
    i = i + 1;
}
```

**Comportamento no REPL:** No REPL, `args.length` e 0 (array vazio)

---

## Constantes de Sinal

Constantes de sinal POSIX padrao (valores i32):

### Interrupcao e Terminacao

| Constante  | Valor | Descricao                              |
|------------|-------|----------------------------------------|
| `SIGINT`   | 2     | Interrupcao do teclado (Ctrl+C)        |
| `SIGTERM`  | 15    | Requisicao de terminacao               |
| `SIGQUIT`  | 3     | Quit do teclado (Ctrl+\)               |
| `SIGHUP`   | 1     | Hangup detectado no terminal de controle |
| `SIGABRT`  | 6     | Sinal de abort                         |

### Definidos pelo Usuario

| Constante  | Valor | Descricao                   |
|------------|-------|-----------------------------|
| `SIGUSR1`  | 10    | Sinal definido pelo usuario 1 |
| `SIGUSR2`  | 12    | Sinal definido pelo usuario 2 |

### Controle de Processo

| Constante  | Valor | Descricao                        |
|------------|-------|----------------------------------|
| `SIGALRM`  | 14    | Timer de alarme                  |
| `SIGCHLD`  | 17    | Mudanca de status do filho       |
| `SIGCONT`  | 18    | Continua se parado               |
| `SIGSTOP`  | 19    | Para processo (nao pode ser capturado) |
| `SIGTSTP`  | 20    | Stop do terminal (Ctrl+Z)        |

### I/O

| Constante  | Valor | Descricao                       |
|------------|-------|---------------------------------|
| `SIGPIPE`  | 13    | Pipe quebrado                   |
| `SIGTTIN`  | 21    | Leitura de terminal em segundo plano |
| `SIGTTOU`  | 22    | Escrita em terminal em segundo plano |

**Exemplo:**
```hemlock
fn handle_signal(sig) {
    if (sig == SIGINT) {
        print("Interrupcao detectada");
    }
    if (sig == SIGTERM) {
        print("Terminacao solicitada");
    }
}

signal(SIGINT, handle_signal);
signal(SIGTERM, handle_signal);
```

**Nota:** `SIGKILL` (9) e `SIGSTOP` (19) nao podem ser capturados ou ignorados.

---

## Funcoes Matematicas/Aritmeticas

### div

Retorna divisao inteira (floor) como ponto flutuante.

**Assinatura:**
```hemlock
div(a: number, b: number): f64
```

**Parametros:**
- `a` - Dividendo
- `b` - Divisor

**Retorna:** Floor de `a / b`, como ponto flutuante (f64)

**Exemplo:**
```hemlock
let result = div(7, 2);    // 3.0 (nao 3.5)
let result2 = div(10, 3);  // 3.0
let result3 = div(-7, 2);  // -4.0 (floor em direcao a -infinito)
```

**Nota:** Em Hemlock, o operador `/` sempre retorna ponto flutuante. Use `div()` quando precisar da parte inteira como float, ou `divi()` quando precisar de resultado inteiro.

---

### divi

Retorna divisao inteira (floor) como inteiro.

**Assinatura:**
```hemlock
divi(a: number, b: number): i64
```

**Parametros:**
- `a` - Dividendo
- `b` - Divisor

**Retorna:** Floor de `a / b`, como inteiro (i64)

**Exemplo:**
```hemlock
let result = divi(7, 2);    // 3
let result2 = divi(10, 3);  // 3
let result3 = divi(-7, 2);  // -4 (floor em direcao a -infinito)
```

**Comparacao:**
```hemlock
print(7 / 2);      // 3.5 (divisao regular, sempre float)
print(div(7, 2));  // 3.0 (divisao floor, resultado float)
print(divi(7, 2)); // 3   (divisao floor, resultado inteiro)
```

---

## Funcoes de Gerenciamento de Memoria

Veja [API de Memoria](memory-api.md) para referencia completa:
- `alloc(size)` - Aloca memoria bruta
- `free(ptr)` - Libera memoria
- `buffer(size)` - Aloca buffer seguro
- `memset(ptr, byte, size)` - Preenche memoria
- `memcpy(dest, src, size)` - Copia memoria
- `realloc(ptr, new_size)` - Redimensiona alocacao

### sizeof

Obtem o tamanho em bytes de um tipo.

**Assinatura:**
```hemlock
sizeof(type): i32
```

**Parametros:**
- `type` - Constante de tipo (`i32`, `f64`, `ptr`, etc.) ou nome de tipo como string

**Retorna:** Tamanho em bytes, como `i32`

**Exemplo:**
```hemlock
print(sizeof(i8));       // 1
print(sizeof(i16));      // 2
print(sizeof(i32));      // 4
print(sizeof(i64));      // 8
print(sizeof(f32));      // 4
print(sizeof(f64));      // 8
print(sizeof(ptr));      // 8
print(sizeof(rune));     // 4

// Usando alias de tipo
print(sizeof(byte));     // 1 (mesmo que u8)
print(sizeof(integer));  // 4 (mesmo que i32)
print(sizeof(number));   // 8 (mesmo que f64)

// Forma de string tambem funciona
print(sizeof("i32"));    // 4
```

**Tipos Suportados:**
| Tipo | Tamanho | Alias |
|------|---------|-------|
| `i8` | 1 | - |
| `i16` | 2 | - |
| `i32` | 4 | `integer` |
| `i64` | 8 | - |
| `u8` | 1 | `byte` |
| `u16` | 2 | - |
| `u32` | 4 | - |
| `u64` | 8 | - |
| `f32` | 4 | - |
| `f64` | 8 | `number` |
| `ptr` | 8 | - |
| `rune` | 4 | - |
| `bool` | 1 | - |

**Veja Tambem:** `talloc()` para alocacao tipada

---

### talloc

Aloca memoria para array tipado (alocacao type-aware).

**Assinatura:**
```hemlock
talloc(type, count: i32): ptr
```

**Parametros:**
- `type` - Constante de tipo (`i32`, `f64`, `ptr`, etc.)
- `count` - Numero de elementos a alocar

**Retorna:** `ptr` para memoria alocada, ou `null` em falha

**Exemplo:**
```hemlock
// Aloca array de 10 i32 (40 bytes)
let int_arr = talloc(i32, 10);
ptr_write_i32(int_arr, 42);
ptr_write_i32(ptr_offset(int_arr, 1, 4), 100);

// Aloca array de 5 f64 (40 bytes)
let float_arr = talloc(f64, 5);

// Aloca array de 100 bytes
let byte_arr = talloc(u8, 100);

// Nao esqueca de liberar!
free(int_arr);
free(float_arr);
free(byte_arr);
```

**Comparacao com alloc:**
```hemlock
// Estes sao equivalentes:
let p1 = talloc(i32, 10);      // Type-aware: 10 i32
let p2 = alloc(sizeof(i32) * 10);  // Calculo manual

// talloc e mais claro e menos propenso a erros
```

**Tratamento de Erros:**
- Retorna `null` em falha de alocacao
- Termina com erro se count nao for positivo
- Verifica overflow de tamanho (count * element_size)

**Veja Tambem:** `alloc()`, `sizeof()`, `free()`

---

## Helpers de Ponteiro FFI

Estas funcoes ajudam a ler e escrever valores tipados em memoria bruta, uteis para FFI e operacoes de memoria de baixo nivel.

### ptr_null

Cria um ponteiro nulo.

**Assinatura:**
```hemlock
ptr_null(): ptr
```

**Retorna:** Ponteiro nulo

**Exemplo:**
```hemlock
let p = ptr_null();
if (p == null) {
    print("Ponteiro e nulo");
}
```

---

### ptr_offset

Calcula deslocamento de ponteiro (aritmetica de ponteiros).

**Assinatura:**
```hemlock
ptr_offset(ptr: ptr, index: i32, element_size: i32): ptr
```

**Parametros:**
- `ptr` - Ponteiro base
- `index` - Indice do elemento
- `element_size` - Tamanho de cada elemento em bytes

**Retorna:** Ponteiro para elemento no indice dado

**Exemplo:**
```hemlock
let arr = talloc(i32, 10);
ptr_write_i32(arr, 100);                      // arr[0] = 100
ptr_write_i32(ptr_offset(arr, 1, 4), 200);    // arr[1] = 200
ptr_write_i32(ptr_offset(arr, 2, 4), 300);    // arr[2] = 300

print(ptr_read_i32(ptr_offset(arr, 1, 4)));   // 200
free(arr);
```

---

### Funcoes de Leitura de Ponteiro

Le valores tipados da memoria.

| Funcao | Assinatura | Retorna | Descricao |
|--------|------------|---------|-----------|
| `ptr_read_i8` | `(ptr)` | `i8` | Le inteiro 8-bit com sinal |
| `ptr_read_i16` | `(ptr)` | `i16` | Le inteiro 16-bit com sinal |
| `ptr_read_i32` | `(ptr)` | `i32` | Le inteiro 32-bit com sinal |
| `ptr_read_i64` | `(ptr)` | `i64` | Le inteiro 64-bit com sinal |
| `ptr_read_u8` | `(ptr)` | `u8` | Le inteiro 8-bit sem sinal |
| `ptr_read_u16` | `(ptr)` | `u16` | Le inteiro 16-bit sem sinal |
| `ptr_read_u32` | `(ptr)` | `u32` | Le inteiro 32-bit sem sinal |
| `ptr_read_u64` | `(ptr)` | `u64` | Le inteiro 64-bit sem sinal |
| `ptr_read_f32` | `(ptr)` | `f32` | Le float 32-bit |
| `ptr_read_f64` | `(ptr)` | `f64` | Le float 64-bit |
| `ptr_read_ptr` | `(ptr)` | `ptr` | Le valor de ponteiro |

**Exemplo:**
```hemlock
let p = alloc(8);
ptr_write_f64(p, 3.14159);
let value = ptr_read_f64(p);
print(value);  // 3.14159
free(p);
```

---

### Funcoes de Escrita de Ponteiro

Escreve valores tipados na memoria.

| Funcao | Assinatura | Retorna | Descricao |
|--------|------------|---------|-----------|
| `ptr_write_i8` | `(ptr, value)` | `null` | Escreve inteiro 8-bit com sinal |
| `ptr_write_i16` | `(ptr, value)` | `null` | Escreve inteiro 16-bit com sinal |
| `ptr_write_i32` | `(ptr, value)` | `null` | Escreve inteiro 32-bit com sinal |
| `ptr_write_i64` | `(ptr, value)` | `null` | Escreve inteiro 64-bit com sinal |
| `ptr_write_u8` | `(ptr, value)` | `null` | Escreve inteiro 8-bit sem sinal |
| `ptr_write_u16` | `(ptr, value)` | `null` | Escreve inteiro 16-bit sem sinal |
| `ptr_write_u32` | `(ptr, value)` | `null` | Escreve inteiro 32-bit sem sinal |
| `ptr_write_u64` | `(ptr, value)` | `null` | Escreve inteiro 64-bit sem sinal |
| `ptr_write_f32` | `(ptr, value)` | `null` | Escreve float 32-bit |
| `ptr_write_f64` | `(ptr, value)` | `null` | Escreve float 64-bit |
| `ptr_write_ptr` | `(ptr, value)` | `null` | Escreve valor de ponteiro |

**Exemplo:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);
print(ptr_read_i32(p));  // 42
free(p);
```

---

### Conversao Buffer/Ponteiro

#### buffer_ptr

Obtem ponteiro bruto de um buffer.

**Assinatura:**
```hemlock
buffer_ptr(buf: buffer): ptr
```

**Exemplo:**
```hemlock
let buf = buffer(64);
let p = buffer_ptr(buf);
// Agora p aponta para a mesma memoria que buf
```

#### ptr_to_buffer

Cria wrapper de buffer em torno de ponteiro bruto.

**Assinatura:**
```hemlock
ptr_to_buffer(ptr: ptr, size: i32): buffer
```

**Exemplo:**
```hemlock
let p = alloc(64);
let buf = ptr_to_buffer(p, 64);
buf[0] = 65;  // Agora tem verificacao de limites
// Nota: liberar buf liberara a memoria subjacente
```

---

## Funcoes de I/O de Arquivo

Veja [API de Arquivos](file-api.md) para referencia completa:
- `open(path, mode?)` - Abre arquivo

---

## Funcoes de Concorrencia

Veja [API de Concorrencia](concurrency-api.md) para referencia completa:
- `spawn(fn, args...)` - Cria tarefa
- `join(task)` - Aguarda tarefa
- `detach(task)` - Desanexa tarefa
- `channel(capacity)` - Cria canal

### apply

Chama uma funcao dinamicamente com array de argumentos.

**Assinatura:**
```hemlock
apply(fn: function, args: array): any
```

**Parametros:**
- `fn` - A funcao a chamar
- `args` - Array de argumentos a passar para a funcao

**Retorna:** Valor de retorno da funcao chamada

**Exemplo:**
```hemlock
fn add(a, b) {
    return a + b;
}

// Chama com array de argumentos
let result = apply(add, [2, 3]);
print(result);  // 5

// Despacho dinamico
let operations = {
    add: fn(a, b) { return a + b; },
    mul: fn(a, b) { return a * b; },
    sub: fn(a, b) { return a - b; }
};

fn calculate(op: string, args: array) {
    return apply(operations[op], args);
}

print(calculate("add", [10, 5]));  // 15
print(calculate("mul", [10, 5]));  // 50
print(calculate("sub", [10, 5]));  // 5

// Argumentos variaveis
fn sum(...nums) {
    let total = 0;
    for (n in nums) {
        total = total + n;
    }
    return total;
}

let numbers = [1, 2, 3, 4, 5];
print(apply(sum, numbers));  // 15
```

**Casos de Uso:**
- Despacho dinamico de funcoes baseado em valores de runtime
- Chamando funcoes com listas de argumentos variaveis
- Implementando utilitarios de ordem superior (map, filter, etc.)
- Sistemas de plugins/extensoes

---

### select

Aguarda dados em multiplos canais, retorna quando qualquer canal tem dados.

**Assinatura:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parametros:**
- `channels` - Array de valores de canal
- `timeout_ms` (opcional) - Timeout em milissegundos (-1 ou omitido para esperar infinitamente)

**Retorna:**
- `{ channel, value }` - Objeto contendo o canal que tinha dados e o valor recebido
- `null` - Em timeout

**Exemplo:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Tarefas produtoras
spawn(fn() {
    sleep(100);
    ch1.send("do canal 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("do canal 2");
});

// Aguarda primeira mensagem
let result = select([ch1, ch2]);
print(result.value);  // "do canal 2" (chegou primeiro)

// Com timeout
let result2 = select([ch1, ch2], 1000);  // Aguarda no maximo 1 segundo
if (result2 == null) {
    print("Timeout - nenhum dado recebido");
} else {
    print("Recebido:", result2.value);
}

// Loop de select continuo
while (true) {
    let msg = select([ch1, ch2], 5000);
    if (msg == null) {
        print("Sem atividade por 5 segundos");
        break;
    }
    print("Recebeu mensagem:", msg.value);
}
```

**Comportamento:**
- Bloqueia ate um canal ter dados ou timeout expirar
- Retorna imediatamente se canal ja tiver dados
- Se canal estiver fechado e vazio, retorna `{ channel, value: null }`
- Faz polling de canais em ordem (primeiro pronto vence)

**Casos de Uso:**
- Multiplexando multiplos produtores
- Implementando timeouts em operacoes de canal
- Construindo loops de eventos com multiplas fontes

---

## Tabela de Resumo

### Funcoes

| Funcao     | Categoria        | Retorna      | Descricao                         |
|------------|------------------|--------------|-----------------------------------|
| `print`    | I/O              | `null`       | Imprime na saida padrao           |
| `read_line`| I/O              | `string?`    | Le linha da entrada padrao        |
| `eprint`   | I/O              | `null`       | Imprime na saida de erro padrao   |
| `typeof`   | Tipo             | `string`     | Obtem nome do tipo                |
| `exec`     | Comando          | `object`     | Executa comando shell             |
| `exec_argv`| Comando          | `object`     | Executa com array de argumentos   |
| `assert`   | Erro             | `null`       | Asserta condicao ou termina       |
| `panic`    | Erro             | `never`      | Erro irrecuperavel (termina)      |
| `signal`   | Sinal            | `function?`  | Registra handler de sinal         |
| `raise`    | Sinal            | `null`       | Envia sinal para processo         |
| `alloc`    | Memoria          | `ptr`        | Aloca memoria bruta               |
| `talloc`   | Memoria          | `ptr`        | Alocacao tipada                   |
| `sizeof`   | Memoria          | `i32`        | Obtem tamanho do tipo             |
| `free`     | Memoria          | `null`       | Libera memoria                    |
| `buffer`   | Memoria          | `buffer`     | Aloca buffer seguro               |
| `memset`   | Memoria          | `null`       | Preenche memoria                  |
| `memcpy`   | Memoria          | `null`       | Copia memoria                     |
| `realloc`  | Memoria          | `ptr`        | Redimensiona alocacao             |
| `open`     | I/O de Arquivo   | `file`       | Abre arquivo                      |
| `spawn`    | Concorrencia     | `task`       | Cria tarefa concorrente           |
| `join`     | Concorrencia     | `any`        | Aguarda resultado da tarefa       |
| `detach`   | Concorrencia     | `null`       | Desanexa tarefa                   |
| `channel`  | Concorrencia     | `channel`    | Cria canal de comunicacao         |
| `select`   | Concorrencia     | `object?`    | Aguarda multiplos canais          |
| `apply`    | Funcao           | `any`        | Chama funcao com array de args    |

### Variaveis Globais

| Variavel   | Tipo     | Descricao                         |
|------------|----------|-----------------------------------|
| `args`     | `array`  | Argumentos de linha de comando    |

### Constantes

| Constante  | Tipo  | Categoria | Valor | Descricao                |
|------------|-------|-----------|-------|--------------------------|
| `SIGINT`   | `i32` | Sinal     | 2     | Interrupcao do teclado   |
| `SIGTERM`  | `i32` | Sinal     | 15    | Requisicao de terminacao |
| `SIGQUIT`  | `i32` | Sinal     | 3     | Quit do teclado          |
| `SIGHUP`   | `i32` | Sinal     | 1     | Hangup                   |
| `SIGABRT`  | `i32` | Sinal     | 6     | Abort                    |
| `SIGUSR1`  | `i32` | Sinal     | 10    | Definido pelo usuario 1  |
| `SIGUSR2`  | `i32` | Sinal     | 12    | Definido pelo usuario 2  |
| `SIGALRM`  | `i32` | Sinal     | 14    | Timer de alarme          |
| `SIGCHLD`  | `i32` | Sinal     | 17    | Mudanca de status do filho |
| `SIGCONT`  | `i32` | Sinal     | 18    | Continua                 |
| `SIGSTOP`  | `i32` | Sinal     | 19    | Para (nao pode capturar) |
| `SIGTSTP`  | `i32` | Sinal     | 20    | Stop do terminal         |
| `SIGPIPE`  | `i32` | Sinal     | 13    | Pipe quebrado            |
| `SIGTTIN`  | `i32` | Sinal     | 21    | Leitura de terminal bg   |
| `SIGTTOU`  | `i32` | Sinal     | 22    | Escrita em terminal bg   |

---

## Veja Tambem

- [Sistema de Tipos](type-system.md) - Tipos e conversoes
- [API de Memoria](memory-api.md) - Funcoes de alocacao de memoria
- [API de Arquivos](file-api.md) - Funcoes de I/O de arquivo
- [API de Concorrencia](concurrency-api.md) - Funcoes async/concorrencia
- [API de Strings](string-api.md) - Metodos de string
- [API de Arrays](array-api.md) - Metodos de array
