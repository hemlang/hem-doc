# Hemlock Execução de Comandos

Hemlock oferece a **função integrada `exec()`** para executar comandos shell e capturar a saída.

## Índice

- [Visão Geral](#visão-geral)
- [Função exec()](#função-exec)
- [Objeto de Resultado](#objeto-de-resultado)
- [Uso Básico](#uso-básico)
- [Exemplos Avançados](#exemplos-avançados)
- [Tratamento de Erros](#tratamento-de-erros)
- [Detalhes de Implementação](#detalhes-de-implementação)
- [Considerações de Segurança](#considerações-de-segurança)
- [Limitações](#limitações)
- [Casos de Uso](#casos-de-uso)
- [Melhores Práticas](#melhores-práticas)
- [Exemplos Completos](#exemplos-completos)

## Visão Geral

A função `exec()` permite que programas Hemlock:
- Executem comandos shell
- Capturem a saída padrão (stdout)
- Verifiquem códigos de saída
- Usem recursos do shell (pipes, redirecionamento, etc.)
- Integrem com ferramentas do sistema

**Importante:** Comandos são executados via `/bin/sh`, fornecendo funcionalidade completa de shell, mas também introduzindo considerações de segurança.

## Função exec()

### Assinatura

```hemlock
exec(command: string): object
```

**Parâmetros:**
- `command` (string) - o comando shell a executar

**Retorna:** Um objeto com dois campos:
- `output` (string) - saída stdout do comando
- `exit_code` (i32) - código de status de saída do comando

### Exemplo Básico

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## Objeto de Resultado

O objeto retornado por `exec()` tem a seguinte estrutura:

```hemlock
{
    output: string,      // stdout do comando (saída capturada)
    exit_code: i32       // status de saída do processo (0 = sucesso)
}
```

### Campo output

Contém todo o texto que o comando escreveu no stdout.

**Propriedades:**
- String vazia se o comando não produziu saída
- Inclui newlines e espaços em branco como estão
- Saída multi-linha é preservada
- Sem limite de tamanho (alocação dinâmica)

**Exemplos:**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Listagem de diretório com newlines

let r3 = exec("true");
print(r3.output);  // "" (string vazia)
```

### Campo exit_code

O código de status de saída do comando.

**Valores:**
- `0` tipicamente indica sucesso
- `1-255` indicam erro (convenção varia por comando)
- `-1` se o comando não pôde ser executado ou terminou anormalmente

**Exemplos:**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (sucesso)

let r2 = exec("false");
print(r2.exit_code);  // 1 (falha)

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2 (arquivo não encontrado, varia por comando)
```

## Uso Básico

### Comandos Simples

```hemlock
let r = exec("ls -la");
print(r.output);
print("Exit code: " + typeof(r.exit_code));
```

### Verificando Status de Saída

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Found: " + r.output);
} else {
    print("Pattern not found");
}
```

### Comandos com Pipes

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Múltiplos Comandos

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Substituição de Comando

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Data atual
```

## Exemplos Avançados

### Tratando Falhas

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Command failed with code: " + typeof(r.exit_code));
    print("Error output: " + r.output);  // Nota: stderr não é capturado
}
```

### Processando Saída Multi-linha

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Encadeamento de Comandos

**Usando && (E):**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup complete");
}
```

**Usando || (OU):**
```hemlock
let r = exec("command1 || command2");
// Executa command2 apenas se command1 falhar
```

**Usando ; (sequencial):**
```hemlock
let r = exec("command1; command2");
// Executa ambos independentemente de sucesso/falha
```

### Usando Pipes

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**Pipes Complexos:**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Padrões de Código de Saída

Diferentes códigos de saída indicam diferentes condições:

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
} else if (r.exit_code == 1) {
    print("File does not exist");
} else {
    print("Test command failed: " + typeof(r.exit_code));
}
```

### Redirecionamento de Saída

```hemlock
// Redirecionar stdout para arquivo (dentro do shell)
let r1 = exec("echo 'test' > /tmp/output.txt");

// Redirecionar stderr para stdout (nota: Hemlock ainda não captura stderr)
let r2 = exec("command 2>&1");
```

### Variáveis de Ambiente

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### Mudança de Diretório de Trabalho

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Tratamento de Erros

### Quando exec() Lança Exceção

A função `exec()` lançará uma exceção se o comando não puder ser executado:

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Failed to execute: " + e);
}
```

**Condições que lançam:**
- `popen()` falha (ex: não pode criar pipe)
- Limites de recursos do sistema excedidos
- Falha na alocação de memória

### Quando exec() Não Lança Exceção

```hemlock
// Comando executa mas retorna código de saída não-zero
let r1 = exec("false");
print(r1.exit_code);  // 1 (não é exceção)

// Comando não tem saída
let r2 = exec("true");
print(r2.output);  // "" (não é exceção)

// Shell não pode encontrar comando
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127 (não é exceção)
```

### Padrão de Execução Segura

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Warning: Command failed with code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Error executing command: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## Detalhes de Implementação

### Como Funciona

**Implementação subjacente:**
- Usa `popen()` para executar comandos via `/bin/sh`
- Apenas stdout é capturado (stderr não é capturado)
- Saída é bufferizada dinamicamente (começa com 4KB, cresce conforme necessário)
- Status de saída é extraído usando macros `WIFEXITED()` e `WEXITSTATUS()`
- String de saída é corretamente terminada em null

**Fluxo do processo:**
1. `popen(command, "r")` cria pipe e faz fork do processo
2. Processo filho executa `/bin/sh -c "command"`
3. Processo pai lê stdout via pipe para buffer crescente
4. `pclose()` espera o filho e retorna status de saída
5. Status de saída é extraído e armazenado no objeto resultado

### Considerações de Desempenho

**Overhead:**
- Cada chamada cria um novo processo shell (~1-5ms de overhead)
- Saída é completamente armazenada em memória (não streaming)
- Streaming não é suportado (espera comando completar)
- Adequado para comandos com tamanho de saída razoável

**Otimizações:**
- Buffer começa com 4KB, dobra quando cheio (uso eficiente de memória)
- Loop de leitura único minimiza chamadas de sistema
- Sem cópias extras de string

**Quando usar:**
- Comandos de curta duração (< 1 segundo)
- Tamanho de saída moderado (< 10MB)
- Operações em lote com intervalos razoáveis

**Quando não usar:**
- Daemons ou serviços de longa duração
- Comandos que produzem saída em GB
- Processamento de dados streaming em tempo real
- Execução de alta frequência (> 100 vezes/segundo)

## Considerações de Segurança

### Risco de Injeção de Shell

**Crítico:** Comandos são executados pelo shell (`/bin/sh`), o que significa que **injeção de shell é possível**.

**Código Vulnerável:**
```hemlock
// PERIGO - NÃO FAÇA ISSO
let filename = args[1];  // Entrada do usuário
let r = exec("cat " + filename);  // Injeção de shell!
```

**Ataque:**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Executa: cat ; rm -rf /; echo pwned
```

### Práticas Seguras

**1. Nunca use entrada de usuário não sanitizada:**
```hemlock
// Ruim
let user_input = args[1];
let r = exec("process " + user_input);  // Perigoso

// Bom - validar primeiro
fn is_safe_filename(name: string): bool {
    // Apenas permitir alfanuméricos, hífen, sublinhado, ponto
    let i = 0;
    while (i < name.length) {
        let c = name[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Invalid filename");
}
```

**2. Use whitelist, não blacklist:**
```hemlock
// Bom - whitelist estrita
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Invalid command");
}
```

**3. Escape caracteres especiais:**
```hemlock
fn shell_escape(s: string): string {
    // Escape simples - envolver em aspas simples e escapar aspas simples
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. Evite exec() para operações de arquivo:**
```hemlock
// Ruim - usando exec para operações de arquivo
let r = exec("cat file.txt");

// Bom - usar API de arquivo do Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### Considerações de Permissão

Comandos executam com as mesmas permissões que o processo Hemlock:

```hemlock
// Se Hemlock está rodando como root, comandos exec() também rodam como root!
let r = exec("rm -rf /important");  // Perigoso se rodando como root
```

**Melhor prática:** Execute Hemlock com privilégios mínimos necessários.

## Limitações

### 1. Sem Captura de stderr

Apenas stdout é capturado, stderr vai para o terminal:

```hemlock
let r = exec("ls /nonexistent");
// r.output está vazio
// Mensagem de erro aparece no terminal, não capturada
```

**Workaround - redirecionar stderr para stdout:**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// Agora a mensagem de erro está em r.output
```

### 2. Sem Streaming

Deve esperar o comando completar:

```hemlock
let r = exec("long_running_command");
// Bloqueia até o comando terminar
// Não pode processar saída incrementalmente
```

### 3. Sem Timeout

Comandos podem rodar indefinidamente:

```hemlock
let r = exec("sleep 1000");
// Bloqueia por 1000 segundos
// Não pode timeout ou cancelar
```

**Workaround - usar comando timeout:**
```hemlock
let r = exec("timeout 5 long_command");
// Timeout após 5 segundos
```

### 4. Sem Tratamento de Sinais

Não pode enviar sinais para comandos em execução:

```hemlock
let r = exec("long_command");
// Não pode enviar SIGINT, SIGTERM, etc para o comando
```

### 5. Sem Controle de Processo

Não pode interagir com o comando após iniciar:

```hemlock
let r = exec("interactive_program");
// Não pode enviar entrada para o programa
// Não pode controlar a execução
```

## Casos de Uso

### Bons Casos de Uso

**1. Executar ferramentas do sistema:**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Processamento rápido de dados com ferramentas Unix:**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Unique lines: " + r.output);
```

**3. Verificar status do sistema:**
```hemlock
let r = exec("df -h");
print("Disk usage:\n" + r.output);
```

**4. Verificação de existência de arquivo:**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("File exists");
}
```

**5. Gerar relatórios:**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Running instances: " + count);
```

**6. Scripts de automação:**
```hemlock
exec("git add .");
exec("git commit -m 'Auto commit'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push failed");
}
```

### Casos de Uso Não Recomendados

**1. Serviços de longa duração:**
```hemlock
// Ruim
let r = exec("nginx");  // Bloqueia para sempre
```

**2. Comandos interativos:**
```hemlock
// Ruim - não pode fornecer entrada
let r = exec("ssh user@host");
```

**3. Comandos com saída enorme:**
```hemlock
// Ruim - carrega saída inteira na memória
let r = exec("cat 10GB_file.log");
```

**4. Streaming em tempo real:**
```hemlock
// Ruim - não pode processar saída incrementalmente
let r = exec("tail -f /var/log/app.log");
```

**5. Tratamento de erros de missão crítica:**
```hemlock
// Ruim - stderr não é capturado
let r = exec("critical_operation");
// Não pode ver mensagens de erro detalhadas
```

## Melhores Práticas

### 1. Sempre Verifique Código de Saída

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Command failed!");
    // Tratar erro
}
```

### 2. Trim Saída Quando Necessário

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // Remove newline final
print(clean);  // "test" (sem newline)
```

### 3. Valide Antes de Executar

```hemlock
fn is_valid_command(cmd: string): bool {
    // Validar se comando é seguro
    return true;  // Sua lógica de validação
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. Use try/catch para Operações Críticas

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Command failed";
    }
} catch (e) {
    print("Error: " + e);
    // Limpeza ou recuperação
}
```

### 5. Prefira APIs Hemlock sobre exec()

```hemlock
// Ruim - usar exec para operações de arquivo
let r = exec("cat file.txt");

// Bom - usar API de arquivo do Hemlock
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. Capture stderr Quando Necessário

```hemlock
// Redirecionar stderr para stdout
let r = exec("command 2>&1");
// Agora r.output contém tanto stdout quanto stderr
```

### 7. Use Recursos do Shell com Sabedoria

```hemlock
// Usar pipes para eficiência
let r = exec("cat large.txt | grep pattern | head -n 10");

// Usar substituição de comando
let r = exec("echo Current user: $(whoami)");

// Usar execução condicional
let r = exec("test -f file.txt && cat file.txt");
```

## Exemplos Completos

### Exemplo 1: Coletor de Informações do Sistema

```hemlock
fn get_system_info() {
    print("=== System Information ===");

    // Hostname
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // Uptime
    let r2 = exec("uptime");
    print("Uptime: " + r2.output.trim());

    // Uso de disco
    let r3 = exec("df -h /");
    print("\nDisk Usage:");
    print(r3.output);

    // Uso de memória
    let r4 = exec("free -h");
    print("Memory Usage:");
    print(r4.output);
}

get_system_info();
```

### Exemplo 2: Analisador de Logs

```hemlock
fn analyze_log(logfile: string) {
    print("Analyzing log: " + logfile);

    // Contar linhas totais
    let r1 = exec("wc -l " + logfile);
    print("Total lines: " + r1.output.trim());

    // Contar erros
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Errors: " + errors);
    } else {
        print("Errors: 0");
    }

    // Contar avisos
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Warnings: " + warnings);
    } else {
        print("Warnings: 0");
    }

    // Erros recentes
    print("\nRecent errors:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Usage: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### Exemplo 3: Auxiliar Git

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Error: Not a git repository");
        return;
    }

    if (r.output == "") {
        print("Working directory clean");
    } else {
        print("Changes:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Adding all changes...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Error adding files");
        return;
    }

    print("Committing...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Error committing");
        return;
    }

    print("Committed successfully");
    print(r2.output);
}

// Uso
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### Exemplo 4: Script de Backup

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Backing up " + source + " to " + dest);

    // Criar diretório de backup
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Error creating backup directory");
        return false;
    }

    // Criar arquivo com timestamp
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Creating archive: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Error creating backup:");
        print(r3.output);
        return false;
    }

    print("Backup completed successfully");

    // Mostrar tamanho do backup
    let r4 = exec("du -h " + backup_file);
    print("Backup size: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Usage: " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Resumo

A função `exec()` do Hemlock oferece:

- Execução simples de comandos shell
- Captura de saída (stdout)
- Verificação de código de saída
- Acesso completo a recursos do shell (pipes, redirecionamento, etc.)
- Integração com ferramentas do sistema

Lembre-se:
- Sempre verifique códigos de saída
- Esteja ciente das implicações de segurança (injeção de shell)
- Valide entrada do usuário antes de usar em comandos
- Prefira APIs Hemlock sobre exec() quando disponíveis
- stderr não é capturado (use `2>&1` para redirecionar)
- Comandos bloqueiam até completar
- Use para ferramentas de curta duração, não serviços de longa duração

**Checklist de Segurança:**
- Nunca use entrada de usuário não sanitizada
- Valide toda entrada
- Use whitelist para comandos
- Escape caracteres especiais quando necessário
- Execute com privilégios mínimos
- Prefira APIs Hemlock sobre comandos shell
