# Documentacao do Hemlock

Bem-vindo a documentacao da linguagem de programacao Hemlock!

> Uma linguagem pequena e nao-segura para escrever coisas nao-seguras de forma segura.

## Indice

### Primeiros Passos
- [Instalacao](getting-started/installation.md) - Compilar e instalar o Hemlock
- [Inicio Rapido](getting-started/quick-start.md) - Seu primeiro programa Hemlock
- [Tutorial](getting-started/tutorial.md) - Guia passo a passo dos fundamentos do Hemlock
- [Caminhos de Aprendizado](getting-started/learning-paths.md) - Escolha sua jornada de aprendizado com base nos seus objetivos

### Novo na Programacao?
- [Glossario](glossary.md) - Definicoes em linguagem simples de termos de programacao

### Guia da Linguagem
- [Visao Geral da Sintaxe](language-guide/syntax.md) - Sintaxe e estrutura basicas
- [Sistema de Tipos](language-guide/types.md) - Tipos primitivos, inferencia de tipos e conversoes
- [Gerenciamento de Memoria](language-guide/memory.md) - Ponteiros, buffers e memoria manual
- [Strings](language-guide/strings.md) - Strings UTF-8 e operacoes
- [Runes](language-guide/runes.md) - Codepoints Unicode e manipulacao de caracteres
- [Fluxo de Controle](language-guide/control-flow.md) - if/else, loops, switch e operadores
- [Funcoes](language-guide/functions.md) - Funcoes, closures e recursao
- [Objetos](language-guide/objects.md) - Literais de objeto, metodos e duck typing
- [Arrays](language-guide/arrays.md) - Arrays dinamicos e operacoes
- [Tratamento de Erros](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [Modulos](language-guide/modules.md) - Sistema de import/export e importacao de pacotes

### Topicos Avancados
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Execute Hemlock no navegador via Emscripten
- [Async e Concorrencia](advanced/async-concurrency.md) - Multi-threading real com async/await
- [Bundling e Empacotamento](advanced/bundling-packaging.md) - Criar bundles e executaveis independentes
- [Interface de Funcoes Estrangeiras](advanced/ffi.md) - Chamar funcoes C de bibliotecas compartilhadas
- [E/S de Arquivos](advanced/file-io.md) - Operacoes de arquivo e gerenciamento de recursos
- [Tratamento de Sinais](advanced/signals.md) - Tratamento de sinais POSIX
- [Argumentos de Linha de Comando](advanced/command-line-args.md) - Acessar argumentos do programa
- [Execucao de Comandos](advanced/command-execution.md) - Executar comandos shell
- [Profiling](advanced/profiling.md) - Tempo de CPU, rastreamento de memoria e deteccao de vazamentos

### Referencia da API
- [Referencia do Sistema de Tipos](reference/type-system.md) - Referencia completa de tipos
- [Referencia de Operadores](reference/operators.md) - Todos os operadores e precedencia
- [Funcoes Integradas](reference/builtins.md) - Funcoes e constantes globais
- [API de Strings](reference/string-api.md) - Metodos e propriedades de strings
- [API de Arrays](reference/array-api.md) - Metodos e propriedades de arrays
- [API de Memoria](reference/memory-api.md) - Alocacao e manipulacao de memoria
- [API de Arquivos](reference/file-api.md) - Metodos de E/S de arquivos
- [API de Concorrencia](reference/concurrency-api.md) - Tasks e channels

### Design e Filosofia
- [Filosofia de Design](design/philosophy.md) - Principios e objetivos centrais
- [Detalhes de Implementacao](design/implementation.md) - Como o Hemlock funciona internamente

### Contribuindo
- [Diretrizes de Contribuicao](contributing/guidelines.md) - Como contribuir
- [Guia de Testes](contributing/testing.md) - Escrevendo e executando testes

## Referencia Rapida

### Hello World
```hemlock
print("Hello, World!");
```

### Tipos Basicos
```hemlock
let x: i32 = 42;           // 32-bit signed integer
let y: u8 = 255;           // 8-bit unsigned integer
let pi: f64 = 3.14159;     // 64-bit float
let name: string = "Alice"; // UTF-8 string
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode codepoint
```

### Gerenciamento de Memoria
```hemlock
// Safe buffer (recommended)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Raw pointer (for experts)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### Async/Concorrencia
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## Filosofia

Hemlock e **explicito sobre implicito**, sempre:
- Ponto e virgula e obrigatorio
- Gerenciamento manual de memoria (sem GC)
- Anotacoes de tipo opcionais com verificacao em runtime
- Operacoes nao-seguras sao permitidas (sua responsabilidade)

Nos fornecemos as ferramentas para ser seguro (`buffer`, anotacoes de tipo, verificacao de limites) mas nao forcamos voce a usa-las (`ptr`, memoria manual, operacoes nao-seguras).

## Obtendo Ajuda

- **Codigo-Fonte**: [Repositorio GitHub](https://github.com/hemlang/hemlock)
- **Gerenciador de Pacotes**: [hpm](https://github.com/hemlang/hpm) - Gerenciador de Pacotes Hemlock
- **Issues**: Reporte bugs e solicite funcionalidades
- **Exemplos**: Veja o diretorio `examples/`
- **Testes**: Veja o diretorio `tests/` para exemplos de uso

## Licenca

Hemlock e liberado sob a Licenca MIT.
