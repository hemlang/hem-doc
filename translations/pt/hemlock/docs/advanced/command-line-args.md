# Hemlock Argumentos de Linha de Comando

Programas Hemlock podem acessar argumentos de linha de comando através do **array `args` integrado**, que é automaticamente preenchido na inicialização do programa.

## Índice

- [Visão Geral](#visão-geral)
- [Array args](#array-args)
- [Propriedades](#propriedades)
- [Padrões de Iteração](#padrões-de-iteração)
- [Casos de Uso Comuns](#casos-de-uso-comuns)
- [Padrões de Parse de Argumentos](#padrões-de-parse-de-argumentos)
- [Melhores Práticas](#melhores-práticas)
- [Exemplos Completos](#exemplos-completos)

## Visão Geral

O array `args` fornece acesso aos argumentos de linha de comando passados para um programa Hemlock:

- **Sempre disponível** - variável global integrada em todos os programas Hemlock
- **Inclui nome do script** - `args[0]` sempre contém o caminho/nome do script
- **Array de strings** - todos os argumentos são strings
- **Indexação base zero** - indexação de array padrão (0, 1, 2, ...)

## Array args

### Estrutura Básica

```hemlock
// args[0] é sempre o nome do arquivo do script
// args[1] até args[n-1] são os argumentos reais
print(args[0]);        // "script.hml"
print(args.length);    // Número total de argumentos (incluindo nome do script)
```

### Exemplo de Uso

**Comando:**
```bash
./hemlock script.hml hello world "test 123"
```

**Em script.hml:**
```hemlock
print("Script name: " + args[0]);     // "script.hml"
print("Total args: " + typeof(args.length));  // "4"
print("First arg: " + args[1]);       // "hello"
print("Second arg: " + args[2]);      // "world"
print("Third arg: " + args[3]);       // "test 123"
```

### Referência de Índices

| Índice | Contém | Valor de Exemplo |
|--------|--------|------------------|
| `args[0]` | Caminho/nome do script | `"script.hml"` ou `"./script.hml"` |
| `args[1]` | Primeiro argumento | `"hello"` |
| `args[2]` | Segundo argumento | `"world"` |
| `args[3]` | Terceiro argumento | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Último argumento | (varia) |

## Propriedades

### Sempre Presente

`args` é um array global disponível em **todos** os programas Hemlock:

```hemlock
// Não precisa declarar ou importar
print(args.length);  // Disponível imediatamente
```

### Inclui Nome do Script

`args[0]` sempre contém o caminho/nome do script:

```hemlock
print("Running: " + args[0]);
```

**Valores possíveis para args[0]:**
- `"script.hml"` - apenas nome do arquivo
- `"./script.hml"` - caminho relativo
- `"/home/user/script.hml"` - caminho absoluto
- Depende de como o script foi invocado

### Tipo: Array de Strings

Todos os argumentos são armazenados como strings:

```hemlock
// Argumentos: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (string, não número)
print(args[2]);  // "3.14" (string, não número)
print(args[3]);  // "true" (string, não booleano)

// Converter conforme necessário:
let num = 42;  // Parsear manualmente se necessário
```

### Comprimento Mínimo

Sempre pelo menos 1 (o nome do script):

```hemlock
print(args.length);  // Mínimo: 1
```

**Mesmo sem argumentos:**
```bash
./hemlock script.hml
```

```hemlock
// Em script.hml:
print(args.length);  // 1 (apenas nome do script)
```

### Comportamento no REPL

No REPL, `args.length` é 0 (array vazio):

```hemlock
# Sessão REPL
> print(args.length);
0
```

## Padrões de Iteração

### Iteração Básica

Pular `args[0]` (nome do script) e processar argumentos reais:

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**Saída para `./hemlock script.hml foo bar baz`:**
```
Argument 1: foo
Argument 2: bar
Argument 3: baz
```

### Iteração For-In (Inclui Nome do Script)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Saída:**
```
script.hml
foo
bar
baz
```

### Verificar Número de Argumentos

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <argument>");
    // Sair ou retornar
} else {
    let arg = args[1];
    // Processar arg
}
```

### Processar Todos Exceto Nome do Script

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Processing: " + arg);
}
```

## Casos de Uso Comuns

### 1. Processamento Simples de Argumentos

Verificar argumento obrigatório:

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Processing file: " + filename);
    // ... processar arquivo
}
```

**Uso:**
```bash
./hemlock script.hml data.txt
# Saída: Processing file: data.txt
```

### 2. Múltiplos Argumentos

```hemlock
if (args.length < 3) {
    print("Usage: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Input: " + input_file);
    print("Output: " + output_file);

    // Processar arquivos...
}
```

**Uso:**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. Número Variável de Argumentos

Processar todos os argumentos fornecidos:

```hemlock
if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**Uso:**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Mensagem de Ajuda

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show this help message");
    print("  -v, --verbose  Enable verbose output");
} else {
    // Processamento normal
}
```

### 5. Validação de Argumentos

```hemlock
fn validate_file(filename: string): bool {
    // Verificar se arquivo existe (exemplo)
    return filename != "";
}

if (args.length < 2) {
    print("Error: No filename provided");
} else if (!validate_file(args[1])) {
    print("Error: Invalid file: " + args[1]);
} else {
    print("Processing: " + args[1]);
}
```

## Padrões de Parse de Argumentos

### Argumentos Nomeados (Flags)

Padrão simples para argumentos nomeados:

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Verbose mode enabled");
}
print("Input: " + input_file);
print("Output: " + output_file);
```

**Uso:**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Flags Booleanas

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### Argumentos com Valor

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // Precisa parsear string para inteiro
        }
    }
    i = i + 1;
}
```

### Misturando Posicionais e Nomeados

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // Tratar como argumento posicional
        positional.push(args[i]);
    }
    i = i + 1;
}

// Atribuir argumentos posicionais
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### Função Auxiliar de Parser de Argumentos

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // Argumento posicional
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose: " + typeof(opts.verbose));
print("Output: " + opts.output);
print("Files: " + typeof(opts.files.length));
```

## Melhores Práticas

### 1. Sempre Verifique Número de Argumentos

```hemlock
// Boa prática
if (args.length < 2) {
    print("Usage: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// Má prática - pode crashar se não houver argumentos
process_file(args[1]);  // Erro se args.length == 1
```

### 2. Forneça Informação de Uso

```hemlock
fn show_usage() {
    print("Usage: " + args[0] + " [OPTIONS] <file>");
    print("Options:");
    print("  -h, --help     Show help");
    print("  -v, --verbose  Verbose output");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. Valide Argumentos

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Error: Missing required argument");
        return false;
    }

    if (args[1] == "") {
        print("Error: Empty argument");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // Sair ou mostrar uso
}
```

### 4. Use Nomes de Variáveis Descritivos

```hemlock
// Bom
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// Ruim
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Trate Argumentos com Aspas e Espaços

O shell trata isso automaticamente:

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. Crie Objeto de Argumentos

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Input: " + arguments.input);
```

## Exemplos Completos

### Exemplo 1: Processador de Arquivos

```hemlock
// Uso: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Usage: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Processing " + input + " -> " + output);

    // Processar arquivo
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // Processamento de exemplo
        f_out.write(processed);

        print("Done!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Exemplo 2: Processador de Arquivos em Lote

```hemlock
// Uso: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Usage: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Processing " + typeof(args.length - 1) + " files:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Processing: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // Processar conteúdo...
            print("    " + typeof(content.length) + " bytes");
        } catch (e) {
            print("    Error: " + e);
        }

        i = i + 1;
    }

    print("Done!");
}
```

### Exemplo 3: Parser de Argumentos Avançado

```hemlock
// Uso: ./hemlock app.hml [OPTIONS] <files...>
// Opções:
//   --verbose, -v     Habilitar saída detalhada
//   --output, -o FILE Definir arquivo de saída
//   --help, -h        Mostrar ajuda

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Error: --output requires a value");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Error: Unknown option: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Usage: " + args[0] + " [OPTIONS] <files...>");
    print("Options:");
    print("  --verbose, -v     Enable verbose output");
    print("  --output, -o FILE Set output file");
    print("  --help, -h        Show this help");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Error: No input files specified");
    show_help();
} else {
    if (config.verbose) {
        print("Verbose mode enabled");
        print("Output file: " + config.output);
        print("Input files: " + typeof(config.files.length));
    }

    // Processar arquivos
    for (let file in config.files) {
        if (config.verbose) {
            print("Processing: " + file);
        }
        // ... processar arquivo
    }
}
```

### Exemplo 4: Ferramenta de Configuração

```hemlock
// Uso: ./hemlock config.hml <action> [arguments]
// Ações:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Usage: " + args[0] + " <action> [arguments]");
    print("Actions:");
    print("  get <key>         Get configuration value");
    print("  set <key> <value> Set configuration value");
    print("  list              List all configuration");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Error: 'get' requires a key");
        } else {
            let key = args[2];
            print("Getting: " + key);
            // ... obter da configuração
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Error: 'set' requires key and value");
        } else {
            let key = args[2];
            let value = args[3];
            print("Setting " + key + " = " + value);
            // ... definir configuração
        }
    } else if (action == "list") {
        print("Listing all configuration:");
        // ... listar configuração
    } else {
        print("Error: Unknown action: " + action);
        show_usage();
    }
}
```

## Resumo

O suporte a argumentos de linha de comando do Hemlock oferece:

- Array `args` integrado globalmente disponível
- Acesso simples baseado em array
- Nome do script em `args[0]`
- Todos os argumentos são strings
- Métodos de array disponíveis (.length, .slice, etc.)

Lembre-se:
- Sempre verifique `args.length` antes de acessar elementos
- `args[0]` é o nome do script
- Argumentos reais começam em `args[1]`
- Todos os argumentos são strings - converta conforme necessário
- Forneça informação de uso para ferramentas amigáveis ao usuário
- Valide argumentos antes de processar

Padrões comuns:
- Argumentos posicionais simples
- Argumentos nomeados/flags (--flag)
- Argumentos com valor (--option value)
- Informação de ajuda (--help)
- Validação de argumentos
