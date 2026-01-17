# Hemlock Tratamento de Sinais

Hemlock oferece **tratamento de sinais POSIX** para gerenciar sinais do sistema como SIGINT (Ctrl+C), SIGTERM e sinais personalizados. Isso permite controle de processo de baixo nível e comunicação entre processos.

## Índice

- [Visão Geral](#visão-geral)
- [API de Sinais](#api-de-sinais)
- [Constantes de Sinais](#constantes-de-sinais)
- [Tratamento Básico de Sinais](#tratamento-básico-de-sinais)
- [Padrões Avançados](#padrões-avançados)
- [Comportamento de Handlers de Sinais](#comportamento-de-handlers-de-sinais)
- [Considerações de Segurança](#considerações-de-segurança)
- [Casos de Uso Comuns](#casos-de-uso-comuns)
- [Exemplos Completos](#exemplos-completos)

## Visão Geral

O tratamento de sinais permite que programas:
- Respondam a interrupções do usuário (Ctrl+C, Ctrl+Z)
- Implementem shutdown gracioso
- Tratem requisições de terminação
- Usem sinais personalizados para comunicação entre processos
- Criem mecanismos de alarme/timer

**Importante:** Seguindo a filosofia do Hemlock, o tratamento de sinais é **inerentemente inseguro**. Handlers podem ser chamados a qualquer momento, interrompendo a execução normal. O usuário é responsável pela sincronização apropriada.

## API de Sinais

### signal(signum, handler_fn)

Registra uma função de tratamento de sinal.

**Parâmetros:**
- `signum` (i32) - número do sinal (ex: constantes SIGINT, SIGTERM)
- `handler_fn` (function ou null) - função a chamar quando o sinal é recebido, ou `null` para resetar ao padrão

**Retorna:** Função handler anterior (ou `null` se nenhuma)

**Exemplo:**
```hemlock
fn my_handler(sig) {
    print("Caught signal: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**Resetar para padrão:**
```hemlock
signal(SIGINT, null);  // Reseta SIGINT para comportamento padrão
```

### raise(signum)

Envia um sinal para o processo atual.

**Parâmetros:**
- `signum` (i32) - número do sinal a enviar

**Retorna:** `null`

**Exemplo:**
```hemlock
raise(SIGUSR1);  // Dispara handler SIGUSR1
```

## Constantes de Sinais

Hemlock fornece constantes de sinais POSIX padrão como valores i32.

### Interrupção e Terminação

| Constante | Valor | Descrição | Gatilho Comum |
|-----------|-------|-----------|---------------|
| `SIGINT` | 2 | Interrupção do teclado | Ctrl+C |
| `SIGTERM` | 15 | Requisição de terminação | Comando `kill` |
| `SIGQUIT` | 3 | Quit do teclado | Ctrl+\ |
| `SIGHUP` | 1 | Hangup detectado | Terminal fechado |
| `SIGABRT` | 6 | Sinal de abort | Função `abort()` |

**Exemplo:**
```hemlock
signal(SIGINT, handle_interrupt);   // Ctrl+C
signal(SIGTERM, handle_terminate);  // Comando kill
signal(SIGHUP, handle_hangup);      // Terminal fechado
```

### Sinais Definidos pelo Usuário

| Constante | Valor | Descrição | Caso de Uso |
|-----------|-------|-----------|-------------|
| `SIGUSR1` | 10 | Sinal definido pelo usuário 1 | IPC personalizado |
| `SIGUSR2` | 12 | Sinal definido pelo usuário 2 | IPC personalizado |

**Exemplo:**
```hemlock
// Para comunicação personalizada
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### Controle de Processo

| Constante | Valor | Descrição | Nota |
|-----------|-------|-----------|------|
| `SIGALRM` | 14 | Timer de alarme | Após `alarm()` |
| `SIGCHLD` | 17 | Mudança de estado do filho | Gerenciamento de processo |
| `SIGCONT` | 18 | Continuar se parado | Retomar após SIGSTOP |
| `SIGSTOP` | 19 | Parar processo | **Não pode ser capturado** |
| `SIGTSTP` | 20 | Stop do terminal | Ctrl+Z |

**Exemplo:**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### Sinais de I/O

| Constante | Valor | Descrição | Quando Enviado |
|-----------|-------|-----------|----------------|
| `SIGPIPE` | 13 | Pipe quebrado | Escrita em pipe fechado |
| `SIGTTIN` | 21 | Leitura de background do terminal | Processo em background lê TTY |
| `SIGTTOU` | 22 | Escrita de background no terminal | Processo em background escreve TTY |

**Exemplo:**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## Tratamento Básico de Sinais

### Capturando Ctrl+C

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("Caught SIGINT!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// Programa continua executando...
// Usuário pressiona Ctrl+C -> handle_interrupt() é chamado

while (!interrupted) {
    // Fazer trabalho...
}

print("Exiting due to interrupt");
```

### Assinatura da Função Handler

Handlers de sinal recebem um argumento: o número do sinal (i32)

```hemlock
fn my_handler(signum) {
    print("Received signal: " + typeof(signum));
    // signum contém o número do sinal (ex: 2 para SIGINT)

    if (signum == SIGINT) {
        print("This is SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // Mesmo handler para múltiplos sinais
```

### Múltiplos Handlers de Sinal

Diferentes handlers para diferentes sinais:

```hemlock
fn handle_int(sig) {
    print("SIGINT received");
}

fn handle_term(sig) {
    print("SIGTERM received");
}

fn handle_usr1(sig) {
    print("SIGUSR1 received");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### Resetar para Comportamento Padrão

Passe `null` como handler para resetar para comportamento padrão:

```hemlock
// Registrar handler personalizado
signal(SIGINT, my_handler);

// Depois, resetar para padrão (terminar em SIGINT)
signal(SIGINT, null);
```

### Disparar Sinal Manualmente

Envie um sinal para seu próprio processo:

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// Disparar handler manualmente
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## Padrões Avançados

### Padrão de Shutdown Gracioso

Padrão comum para limpeza na terminação:

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Shutting down gracefully...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// Loop principal
while (!should_exit) {
    // Fazer trabalho...
    // Verificar flag should_exit periodicamente
}

print("Cleanup complete");
```

### Contador de Sinais

Rastrear número de sinais recebidos:

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print("Received " + typeof(signal_count) + " signals");
}

signal(SIGUSR1, count_signals);

// Depois...
print("Total signals: " + typeof(signal_count));
```

### Recarregar Configuração por Sinal

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Reloading configuration...");
    config = load_config();
    print("Configuration reloaded");
}

signal(SIGHUP, reload_config);  // Recarregar ao receber SIGHUP

// Do shell, envie SIGHUP para o processo para recarregar config
// kill -HUP <pid>
```

### Timeout com SIGALRM

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// Definir alarme (ainda não implementado em Hemlock, apenas exemplo)
// alarm(5);  // timeout de 5 segundos

while (!timed_out) {
    // Trabalho com timeout
}
```

### Máquina de Estados Baseada em Sinais

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("State: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("State: " + typeof(state));
}

signal(SIGUSR1, next_state);  // Avançar estado
signal(SIGUSR2, prev_state);  // Retroceder estado

// Controlar máquina de estados:
// kill -USR1 <pid>  # próximo estado
// kill -USR2 <pid>  # estado anterior
```

## Comportamento de Handlers de Sinais

### Notas Importantes

**Execução de Handler:**
- Handlers são chamados **sincronamente** quando o sinal é recebido
- Handlers executam no contexto do processo atual
- Handlers de sinal compartilham o ambiente de closure da função que os definiu
- Handlers podem acessar e modificar variáveis do escopo externo (como globais ou variáveis capturadas)

**Melhores Práticas:**
- Mantenha handlers simples e rápidos - evite operações de longa duração
- Defina flags em vez de executar lógica complexa
- Evite chamar funções que podem adquirir locks
- Esteja ciente de que handlers podem interromper qualquer operação

### Quais Sinais Podem Ser Capturados

**Podem ser capturados e tratados:**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (mas o programa abortará após o handler retornar)

**Não podem ser capturados:**
- `SIGKILL` (9) - sempre termina o processo
- `SIGSTOP` (19) - sempre para o processo

**Dependentes do Sistema:**
- Comportamento padrão de alguns sinais pode variar entre sistemas
- Consulte a documentação de sinais da sua plataforma para detalhes

### Limitações de Handlers

```hemlock
fn complex_handler(sig) {
    // Evite isso em handlers de sinal:

    // ❌ Operações de longa duração
    // process_large_file();

    // ❌ I/O bloqueante
    // let f = open("log.txt", "a");
    // f.write("Signal received\n");

    // ❌ Mudanças complexas de estado
    // rebuild_entire_data_structure();

    // ✅ Definir flag simples é seguro
    let should_stop = true;

    // ✅ Atualização simples de contador geralmente é seguro
    let signal_count = signal_count + 1;
}
```

## Considerações de Segurança

Seguindo a filosofia do Hemlock, o tratamento de sinais é **inerentemente inseguro**.

### Condições de Corrida

Handlers podem ser chamados a qualquer momento, interrompendo a execução normal:

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // Condição de corrida se chamado durante atualização de counter
}

signal(SIGUSR1, increment);

// Código principal também modifica counter
counter = counter + 1;  // Pode ser interrompido pelo handler de sinal
```

**Problema:** Se o sinal chega enquanto o código principal está atualizando `counter`, o resultado é imprevisível.

### Segurança de Sinal Assíncrono

Hemlock **não** garante segurança de sinal assíncrono:
- Handlers podem chamar qualquer código Hemlock (diferente de funções C restritas async-signal-safe)
- Isso fornece flexibilidade mas requer cuidado do usuário
- Condições de corrida podem ocorrer se handlers modificam estado compartilhado

### Melhores Práticas para Tratamento Seguro de Sinais

**1. Use Flags Atômicas**

Atribuições booleanas simples geralmente são seguras:

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // Atribuição simples é segura
}

signal(SIGINT, handler);

while (!should_exit) {
    // Trabalho...
}
```

**2. Minimize Estado Compartilhado**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // Modifique apenas esta variável
    interrupt_count = interrupt_count + 1;
}
```

**3. Adie Operações Complexas**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // Apenas define flag
}

signal(SIGHUP, signal_reload);

// No loop principal:
while (true) {
    if (pending_reload) {
        reload_config();  // Faz trabalho complexo aqui
        pending_reload = false;
    }

    // Trabalho normal...
}
```

**4. Evite Problemas de Reentrância**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // Não modifique dados enquanto código principal os usa
        return;
    }
    // Pode continuar com segurança
}
```

## Casos de Uso Comuns

### 1. Shutdown Gracioso de Servidor

```hemlock
let running = true;

fn shutdown(sig) {
    print("Shutdown signal received");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Loop principal do servidor
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Server stopped");
```

### 2. Recarregar Configuração (Sem Reiniciar)

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Reloading configuration...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // Usar configuração...
}
```

### 3. Rotação de Logs

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // Renomear log antigo, abrir novo
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // Logging normal...
    log_file.write("Log entry\n");
}
```

### 4. Relatório de Status

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Status: " + typeof(requests_handled) + " requests handled");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// Do shell: kill -USR1 <pid>
```

### 5. Alternar Modo Debug

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Debug mode: ON");
    } else {
        print("Debug mode: OFF");
    }
}

signal(SIGUSR2, toggle_debug);

// Do shell: kill -USR2 <pid> para alternar
```

## Exemplos Completos

### Exemplo 1: Handler de Interrupção com Limpeza

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Interrupt detected (Ctrl+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("User signal 1 received");
    }
}

// Registrar handlers
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// Simular algum trabalho
let i = 0;
while (running && i < 100) {
    print("Working... " + typeof(i));

    // Disparar SIGUSR1 a cada 10 iterações
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Total signals received: " + typeof(signal_count));
```

### Exemplo 2: Máquina de Estados Multi-sinal

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("State: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("State: " + state);
}

fn report_stats(sig) {
    print("State: " + state);
    print("Requests: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // Fazer trabalho
        request_count = request_count + 1;
    }

    // Verificar a cada iteração...
}
```

### Exemplo 3: Controlador de Pool de Workers

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Workers: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Workers: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Shutting down...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Loop principal ajusta pool de workers baseado em worker_count
while (!should_exit) {
    // Gerenciar workers baseado em worker_count
    // ...
}
```

## Depurando Handlers de Sinal

### Adicionar Prints de Diagnóstico

```hemlock
fn debug_handler(sig) {
    print("Handler called for signal: " + typeof(sig));
    print("Stack: (not yet available)");

    // Sua lógica de handler...
}

signal(SIGINT, debug_handler);
```

### Contar Chamadas de Handler

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Handler call #" + typeof(handler_calls));

    // Sua lógica de handler...
}
```

### Testar Usando raise()

```hemlock
fn test_handler(sig) {
    print("Test signal received: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// Testar disparando manualmente
raise(SIGUSR1);
print("Handler should have been called");
```

## Resumo

O tratamento de sinais do Hemlock oferece:

- Tratamento de sinais POSIX para controle de processo de baixo nível
- 15 constantes de sinais padrão
- API simples signal() e raise()
- Funções handler flexíveis com suporte a closures
- Múltiplos sinais podem compartilhar um handler

Lembre-se:
- O tratamento de sinais é inerentemente inseguro - use com cuidado
- Mantenha handlers simples e rápidos
- Use flags para mudanças de estado, não operações complexas
- Handlers podem interromper a execução a qualquer momento
- SIGKILL ou SIGSTOP não podem ser capturados
- Use raise() para testar handlers completamente

Padrões comuns:
- Shutdown gracioso (SIGINT, SIGTERM)
- Recarregar configuração (SIGHUP)
- Rotação de logs (SIGUSR1)
- Relatório de status (SIGUSR1/SIGUSR2)
- Alternar modo debug (SIGUSR2)
