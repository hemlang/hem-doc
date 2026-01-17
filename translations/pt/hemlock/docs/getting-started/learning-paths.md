# Caminhos de Aprendizado

Objetivos diferentes requerem conhecimentos diferentes. Escolha o caminho que corresponde ao que voce deseja construir.

---

## Caminho 1: Scripts Rapidos e Automacao

**Objetivo:** Escrever scripts para automatizar tarefas, processar arquivos e fazer o trabalho.

**Tempo para produtividade:** Rapido - voce pode comecar a escrever scripts uteis imediatamente.

### O Que Voce Aprendera

1. **[Inicio Rapido](quick-start.md)** - Seu primeiro programa, sintaxe basica
2. **[Strings](../language-guide/strings.md)** - Processamento de texto, divisao, busca
3. **[Arrays](../language-guide/arrays.md)** - Listas, filtragem, transformacao de dados
4. **[E/S de Arquivos](../advanced/file-io.md)** - Ler e escrever arquivos
5. **[Argumentos de Linha de Comando](../advanced/command-line-args.md)** - Obter entrada do usuario

### Pule Por Enquanto

- Gerenciamento de memoria (scripts lidam automaticamente)
- Async/concorrencia (muito complexo para scripts simples)
- FFI (so necessario quando precisar de interoperabilidade com C)

### Projeto de Exemplo: Renomeador de Arquivos

```hemlock
import { list_dir, rename } from "@stdlib/fs";

// Renomeia todos os arquivos .txt para .md
let files = list_dir(".");
for (file in files) {
    if (file.ends_with(".txt")) {
        let new_name = file.replace(".txt", ".md");
        rename(file, new_name);
        print(`Renomeado: ${file} -> ${new_name}`);
    }
}
```

---

## Caminho 2: Processamento e Analise de Dados

**Objetivo:** Analisar dados, transforma-los e gerar relatorios.

**Tempo para produtividade:** Rapido - os metodos de string e array do Hemlock tornam isso facil.

### O Que Voce Aprendera

1. **[Inicio Rapido](quick-start.md)** - Fundamentos
2. **[Strings](../language-guide/strings.md)** - Analise, divisao, formatacao
3. **[Arrays](../language-guide/arrays.md)** - map, filter, reduce para transformacao de dados
4. **[Objetos](../language-guide/objects.md)** - Dados estruturados
5. **Biblioteca Padrao:**
   - **[@stdlib/json](../../stdlib/docs/json.md)** - Analise de JSON
   - **[@stdlib/csv](../../stdlib/docs/csv.md)** - Arquivos CSV
   - **[@stdlib/fs](../../stdlib/docs/fs.md)** - Operacoes de arquivo

### Projeto de Exemplo: Analisador de CSV

```hemlock
import { read_file } from "@stdlib/fs";
import { parse } from "@stdlib/csv";

let data = parse(read_file("sales.csv"));

// Calcular vendas totais
let total = 0;
for (row in data) {
    total = total + f64(row.amount);
}

print(`Vendas totais: R$${total}`);

// Encontrar maior venda
let top = data[0];
for (row in data) {
    if (f64(row.amount) > f64(top.amount)) {
        top = row;
    }
}

print(`Maior venda: ${top.product} - R$${top.amount}`);
```

---

## Caminho 3: Programacao Web e de Rede

**Objetivo:** Construir clientes HTTP, usar APIs, criar servidores.

**Tempo para produtividade:** Medio - requer entender o basico de async.

### O Que Voce Aprendera

1. **[Inicio Rapido](quick-start.md)** - Fundamentos
2. **[Funcoes](../language-guide/functions.md)** - Callbacks e closures
3. **[Tratamento de Erros](../language-guide/error-handling.md)** - try/catch para erros de rede
4. **[Async e Concorrencia](../advanced/async-concurrency.md)** - spawn, await, channels
5. **Biblioteca Padrao:**
   - **[@stdlib/http](../../stdlib/docs/http.md)** - Requisicoes HTTP
   - **[@stdlib/json](../../stdlib/docs/json.md)** - JSON para APIs
   - **[@stdlib/net](../../stdlib/docs/net.md)** - Sockets TCP/UDP
   - **[@stdlib/url](../../stdlib/docs/url.md)** - Analise de URL

### Projeto de Exemplo: Cliente de API

```hemlock
import { http_get, http_post } from "@stdlib/http";
import { parse, stringify } from "@stdlib/json";

// Requisicao GET
let response = http_get("https://api.example.com/users");
let users = parse(response.body);

for (user in users) {
    print(`${user.name}: ${user.email}`);
}

// Requisicao POST
let new_user = { name: "Alice", email: "alice@example.com" };
let result = http_post("https://api.example.com/users", {
    body: stringify(new_user),
    headers: { "Content-Type": "application/json" }
});

print(`ID do usuario criado: ${parse(result.body).id}`);
```

---

## Caminho 4: Programacao de Sistemas

**Objetivo:** Escrever codigo de baixo nivel, manipular memoria, interagir com bibliotecas C.

**Tempo para produtividade:** Mais longo - requer entender gerenciamento de memoria.

### O Que Voce Aprendera

1. **[Inicio Rapido](quick-start.md)** - Fundamentos
2. **[Tipos](../language-guide/types.md)** - Entender i32, u8, ptr, etc.
3. **[Gerenciamento de Memoria](../language-guide/memory.md)** - alloc, free, buffers
4. **[FFI](../advanced/ffi.md)** - Chamar funcoes C
5. **[Sinais](../advanced/signals.md)** - Tratamento de sinais

### Conceitos-Chave

**Lista de Verificacao de Seguranca de Memoria:**
- [ ] Cada `alloc()` tem um `free()` correspondente
- [ ] Use `buffer()` a menos que precise de `ptr` bruto
- [ ] Defina ponteiros para `null` apos liberar
- [ ] Use `try/finally` para garantir limpeza

**Mapeamento de Tipos FFI:**
| Hemlock | C |
|---------|---|
| `i8` | `char` / `int8_t` |
| `i32` | `int` |
| `i64` | `long` (64-bit) |
| `u8` | `unsigned char` |
| `f64` | `double` |
| `ptr` | `void*` |

### Projeto de Exemplo: Pool de Memoria Personalizado

```hemlock
// Alocador bump simples
let pool_size = 1024 * 1024;  // 1MB
let pool = alloc(pool_size);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > pool_size) {
        throw "Pool de memoria esgotado";
    }
    let p = pool + pool_offset;
    pool_offset = pool_offset + size;
    return p;
}

fn pool_reset() {
    pool_offset = 0;
}

fn pool_destroy() {
    free(pool);
}

// Usando
let a = pool_alloc(100);
let b = pool_alloc(200);
memset(a, 0, 100);
memset(b, 0, 200);

pool_reset();  // Reutilizar toda a memoria
pool_destroy();  // Limpar
```

---

## Caminho 5: Programas Paralelos e Concorrentes

**Objetivo:** Executar codigo em multiplos nucleos de CPU, construir aplicacoes responsivas.

**Tempo para produtividade:** Medio - a sintaxe async e simples, mas o pensamento paralelo requer pratica.

### O Que Voce Aprendera

1. **[Inicio Rapido](quick-start.md)** - Fundamentos
2. **[Funcoes](../language-guide/functions.md)** - Closures (importantes para async)
3. **[Async e Concorrencia](../advanced/async-concurrency.md)** - Aprofundamento completo
4. **[Operacoes Atomicas](../advanced/atomics.md)** - Programacao lock-free

### Conceitos-Chave

**Modelo Async do Hemlock:**
- `async fn` - Define uma funcao que pode executar em outra thread
- `spawn(fn, args...)` - Inicia a execucao, retorna um handle de tarefa
- `join(task)` ou `await task` - Espera completar, obtem o resultado
- `channel(size)` - Cria uma fila para enviar dados entre tarefas

**Importante:** Tarefas recebem *copias* dos valores. Se voce passar um ponteiro, e responsavel por garantir que a memoria permaneca valida ate a tarefa terminar.

### Projeto de Exemplo: Processador de Arquivos Paralelo

```hemlock
import { list_dir, read_file } from "@stdlib/fs";

async fn process_file(path: string): i32 {
    let content = read_file(path);
    let lines = content.split("\n");
    return lines.length;
}

// Processar todos os arquivos em paralelo
let files = list_dir("data/");
let tasks = [];

for (file in files) {
    if (file.ends_with(".txt")) {
        let task = spawn(process_file, "data/" + file);
        tasks.push({ name: file, task: task });
    }
}

// Coletar resultados
let total_lines = 0;
for (item in tasks) {
    let count = join(item.task);
    print(`${item.name}: ${count} linhas`);
    total_lines = total_lines + count;
}

print(`Total: ${total_lines} linhas`);
```

---

## O Que Aprender Primeiro em Qualquer Caminho

Independente do seu objetivo, comece com estes fundamentos:

### Semana 1: Fundamentos Essenciais
1. **[Inicio Rapido](quick-start.md)** - Escreva e execute seu primeiro programa
2. **[Sintaxe](../language-guide/syntax.md)** - Variaveis, operadores, fluxo de controle
3. **[Funcoes](../language-guide/functions.md)** - Definir e chamar funcoes

### Semana 2: Processamento de Dados
4. **[Strings](../language-guide/strings.md)** - Manipulacao de texto
5. **[Arrays](../language-guide/arrays.md)** - Colecoes e iteracao
6. **[Objetos](../language-guide/objects.md)** - Dados estruturados

### Semana 3: Robustez
7. **[Tratamento de Erros](../language-guide/error-handling.md)** - try/catch/throw
8. **[Modulos](../language-guide/modules.md)** - import/export, usando a biblioteca padrao

### Depois: Escolha seu Caminho Acima

---

## Guia Rapido: Vindo de Outras Linguagens

### Vindo do Python

| Python | Hemlock | Notas |
|--------|---------|-------|
| `x = 42` | `let x = 42;` | Ponto e virgula obrigatorio |
| `def fn():` | `fn name() { }` | Chaves obrigatorias |
| `if x:` | `if (x) { }` | Parenteses e chaves obrigatorios |
| `for i in range(10):` | `for (let i = 0; i < 10; i++) { }` | Laco for estilo C |
| `for item in list:` | `for (item in array) { }` | for-in igual |
| `list.append(x)` | `array.push(x);` | Nomes de metodos diferentes |
| `len(s)` | `s.length` ou `len(s)` | Ambos funcionam |
| Memoria automatica | `ptr` requer gerenciamento manual | A maioria dos tipos e limpa automaticamente |

### Vindo do JavaScript

| JavaScript | Hemlock | Notas |
|------------|---------|-------|
| `let x = 42` | `let x = 42;` | Igual (ponto e virgula obrigatorio) |
| `const x = 42` | `let x = 42;` | Sem palavra-chave const |
| `function fn()` | `fn name() { }` | Palavra-chave diferente |
| `() => x` | `fn() { return x; }` | Sem arrow functions |
| `async/await` | `async/await` | Mesma sintaxe |
| `Promise` | `spawn/join` | Modelo diferente |
| GC automatico | `ptr` requer gerenciamento manual | A maioria dos tipos e limpa automaticamente |

### Vindo do C/C++

| C | Hemlock | Notas |
|---|---------|-------|
| `int x = 42;` | `let x: i32 = 42;` | Tipo apos dois-pontos |
| `malloc(n)` | `alloc(n)` | Mesmo conceito |
| `free(p)` | `free(p)` | Igual |
| `char* s = "hi"` | `let s = "hi";` | Strings sao gerenciadas |
| `#include` | `import { } from` | Importacao de modulos |
| Tudo manual | A maioria automatica | Apenas `ptr` requer gerenciamento manual |

---

## Obtendo Ajuda

- **[Glossario](../glossary.md)** - Definicoes de termos de programacao
- **[Exemplos](../../examples/)** - Programas funcionais completos
- **[Testes](../../tests/)** - Veja como os recursos sao usados
- **Issues no GitHub** - Faca perguntas, reporte bugs

---

## Niveis de Dificuldade

Ao longo da documentacao, voce vera estas marcacoes:

| Marcacao | Significado |
|----------|-------------|
| **Iniciante** | Nao requer experiencia previa em programacao |
| **Intermediario** | Assume conhecimento basico de programacao |
| **Avancado** | Requer entendimento de conceitos de sistemas |

Se algo marcado como "Iniciante" estiver confuso, consulte o [Glossario](../glossary.md) para definicoes de termos.
