# Tratamento de Erros

Hemlock suporta tratamento de erros baseado em exceções através de `try`, `catch`, `finally`, `throw` e `panic`. Este guia abrange o uso de exceções para erros recuperáveis e panic para erros irrecuperáveis.

## Visao Geral

```hemlock
// Tratamento básico de erros
try {
    operacao_arriscada();
} catch (e) {
    print("Erro: " + e);
}

// Com operação de limpeza
try {
    process_file();
} catch (e) {
    print("Falhou: " + e);
} finally {
    cleanup();
}

// Lançando erros
fn divide(a, b) {
    if (b == 0) {
        throw "divisão por zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Sintaxe

**Try/catch básico:**
```hemlock
try {
    // Código arriscado
} catch (e) {
    // Trata erro, e contém o valor lançado
}
```

**Try/finally:**
```hemlock
try {
    // Código arriscado
} finally {
    // Sempre executa, mesmo se exceção for lançada
}
```

**Try/catch/finally:**
```hemlock
try {
    // Código arriscado
} catch (e) {
    // Trata erro
} finally {
    // Código de limpeza
}
```

### Bloco Try

O bloco try executa declarações em sequência:

```hemlock
try {
    print("Iniciando...");
    operacao_arriscada();
    print("Sucesso!");  // Só executa se não houver exceção
}
```

**Comportamento:**
- Executa declarações em sequência
- Se exceção for lançada: pula para `catch` ou `finally`
- Se não houver exceção: executa `finally` (se presente) e continua

### Bloco Catch

O bloco catch recebe o valor lançado:

```hemlock
try {
    throw "ops";
} catch (erro) {
    print("Capturado: " + erro);  // erro = "ops"
    // erro só é acessível aqui
}
// erro não é acessível aqui
```

**Parâmetro catch:**
- Recebe o valor lançado (qualquer tipo)
- Escopo limitado ao bloco catch
- Pode ter qualquer nome (comumente `e`, `err` ou `error`)

**O que você pode fazer no catch:**
```hemlock
try {
    operacao_arriscada();
} catch (e) {
    // Registrar erro
    print("Erro: " + e);

    // Relançar mesmo erro
    throw e;

    // Lançar erro diferente
    throw "erro diferente";

    // Retornar valor padrão
    return null;

    // Tratar e continuar
    // (sem relançar)
}
```

### Bloco Finally

O bloco finally **sempre executa**:

```hemlock
try {
    print("1: try");
    throw "erro";
} catch (e) {
    print("2: catch");
} finally {
    print("3: finally");  // Sempre executa
}
print("4: depois");

// Saída: 1: try, 2: catch, 3: finally, 4: depois
```

**Quando finally executa:**
- Após bloco try (se não houver exceção)
- Após bloco catch (se exceção foi capturada)
- Mesmo se try/catch contiver `return`, `break` ou `continue`
- Antes do fluxo de controle sair do try/catch

**Finally com return:**
```hemlock
fn example() {
    try {
        return 1;  // Retorna 1 após finally executar
    } finally {
        print("limpeza");  // Executa antes de retornar
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // return do finally sobrescreve - retorna 2
    }
}
```

**Finally com fluxo de controle:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Break após finally executar
        }
    } finally {
        print("limpeza " + typeof(i));
    }
}
```

## Declaração Throw

### Throw Básico

Lança qualquer valor como exceção:

```hemlock
throw "mensagem de erro";
throw 404;
throw { code: 500, message: "Erro interno" };
throw null;
throw ["erro", "detalhes"];
```

**Processo de execução:**
1. Avalia a expressão
2. Pula imediatamente para o `catch` mais próximo
3. Se não houver `catch`, propaga pela pilha de chamadas

### Lançando Erros

```hemlock
fn validate_age(idade: i32) {
    if (idade < 0) {
        throw "Idade não pode ser negativa";
    }
    if (idade > 150) {
        throw "Idade não é realista";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Erro de validação: " + e);
}
```

### Lançando Objetos de Erro

Crie informações de erro estruturadas:

```hemlock
fn read_file(caminho: string) {
    if (!file_exists(caminho)) {
        throw {
            type: "FileNotFound",
            path: caminho,
            message: "Arquivo não existe"
        };
    }
    // ... ler arquivo
}

try {
    read_file("faltando.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("Arquivo não encontrado: " + e.path);
    }
}
```

### Relançando

Captura e relança erros:

```hemlock
fn wrapper() {
    try {
        operacao_arriscada();
    } catch (e) {
        print("Registrando erro: " + e);
        throw e;  // Relança para o chamador
    }
}

try {
    wrapper();
} catch (e) {
    print("Capturado no main: " + e);
}
```

## Exceções Não Capturadas

Se uma exceção propaga até o topo da pilha de chamadas sem ser capturada:

```hemlock
fn foo() {
    throw "não capturada!";
}

foo();  // Crash com: Runtime error: não capturada!
```

**Comportamento:**
- Programa termina
- Imprime mensagem de erro no stderr
- Sai com código de status não-zero
- Stack trace será adicionado em versões futuras

## Panic - Erros Irrecuperáveis

### O que é Panic?

`panic()` é usado para **erros irrecuperáveis** que devem terminar o programa imediatamente:

```hemlock
panic();                    // Mensagem padrão: "panic!"
panic("mensagem custom");   // Mensagem personalizada
panic(42);                  // Valores não-string serão impressos
```

**Semântica:**
- **Sai imediatamente** do programa com código de saída 1
- Imprime mensagem de erro no stderr: `panic: <mensagem>`
- **Não pode** ser capturado por try/catch
- Usado para bugs e erros irrecuperáveis

### Panic vs Throw

```hemlock
// throw - erro recuperável (pode ser capturado)
try {
    throw "erro recuperável";
} catch (e) {
    print("Capturado: " + e);  // Captura com sucesso
}

// panic - erro irrecuperável (não pode ser capturado)
try {
    panic("erro irrecuperável");  // Programa sai imediatamente
} catch (e) {
    print("Isso nunca executa");   // Nunca executa
}
```

### Quando Usar Panic

**Use panic para:**
- **Bugs**: Código alcançado que não deveria ser
- **Estado inválido**: Estrutura de dados corrompida detectada
- **Erros irrecuperáveis**: Recurso crítico indisponível
- **Falhas de asserção**: Quando `assert()` não é suficiente

**Exemplos:**
```hemlock
// Código inalcançável
fn process_state(estado: i32) {
    if (estado == 1) {
        return "pronto";
    } else if (estado == 2) {
        return "executando";
    } else if (estado == 3) {
        return "parado";
    } else {
        panic("estado inválido: " + typeof(estado));  // Não deveria acontecer
    }
}

// Verificação de recurso crítico
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json não encontrado - não pode iniciar");
    }
    // ...
}

// Invariante de estrutura de dados
fn pop_stack(pilha) {
    if (pilha.length == 0) {
        panic("pop() chamado em pilha vazia");
    }
    return pilha.pop();
}
```

### Quando Não Usar Panic

**Use throw para:**
- Validação de entrada do usuário
- Arquivo não encontrado
- Erros de rede
- Condições de erro esperadas

```hemlock
// Ruim: usar panic para erros esperados
fn divide(a, b) {
    if (b == 0) {
        panic("divisão por zero");  // Muito severo
    }
    return a / b;
}

// Bom: usar throw para erros esperados
fn divide(a, b) {
    if (b == 0) {
        throw "divisão por zero";  // Recuperável
    }
    return a / b;
}
```

## Interação com Fluxo de Controle

### Return em Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Retorna 1 após finally executar
    } finally {
        print("limpeza");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // return do finally sobrescreve - retorna 2
    }
}
```

**Regra:** O valor de retorno do bloco finally sobrescreve o retorno do try/catch.

### Break/Continue em Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Break após finally executar
    } finally {
        print("limpeza " + typeof(i));
    }
}
```

**Regra:** break/continue executa após o bloco finally.

### Try/Catch Aninhado

```hemlock
try {
    try {
        throw "interno";
    } catch (e) {
        print("Capturado: " + e);  // Imprime: Capturado: interno
        throw "externo";  // Relança erro diferente
    }
} catch (e) {
    print("Capturado: " + e);  // Imprime: Capturado: externo
}
```

**Regra:** Blocos try/catch aninhados funcionam como esperado, catch interno executa primeiro.

## Padrões Comuns

### Padrão: Limpeza de Recursos

Sempre use `finally` para limpeza:

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Erro processando arquivo: " + e);
    } finally {
        if (file != null) {
            file.close();  // Fecha mesmo em erro
        }
    }
}
```

### Padrão: Encapsulamento de Erro

Encapsula erros de baixo nível com contexto:

```hemlock
fn load_config(caminho) {
    try {
        let content = read_file(caminho);
        return parse_json(content);
    } catch (e) {
        throw "Falha ao carregar config de " + caminho + ": " + e;
    }
}
```

### Padrão: Recuperação de Erro

Fornece valor de fallback em caso de erro:

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "divisão por zero";
        }
        return a / b;
    } catch (e) {
        print("Erro: " + e);
        return null;  // Valor de fallback
    }
}
```

### Padrão: Validação

Use exceções para validação:

```hemlock
fn validate_user(usuario) {
    if (usuario.name == null || usuario.name == "") {
        throw "Nome é obrigatório";
    }
    if (usuario.age < 0 || usuario.age > 150) {
        throw "Idade inválida";
    }
    if (usuario.email == null || !usuario.email.contains("@")) {
        throw "Email inválido";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "inválido" });
} catch (e) {
    print("Validação falhou: " + e);
}
```

### Padrão: Múltiplos Tipos de Erro

Use objetos de erro para distinguir tipos de erro:

```hemlock
fn process_data(dados) {
    if (dados == null) {
        throw { type: "NullData", message: "Dados são nulos" };
    }

    if (typeof(dados) != "array") {
        throw { type: "TypeError", message: "Esperado array" };
    }

    if (dados.length == 0) {
        throw { type: "EmptyData", message: "Array está vazio" };
    }

    // ... processar
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("Nenhum dado fornecido");
    } else if (e.type == "TypeError") {
        print("Tipo de dados errado: " + e.message);
    } else {
        print("Erro: " + e.message);
    }
}
```

## Melhores Práticas

1. **Use exceções para situações excepcionais** - Não use para fluxo de controle normal
2. **Lance erros significativos** - Use strings ou objetos com contexto
3. **Sempre use finally para limpeza** - Garanta que recursos sejam liberados
4. **Não capture e ignore** - Pelo menos registre o erro
5. **Relance quando apropriado** - Se você não pode tratar, deixe o chamador tratar
6. **Use panic para bugs** - Use panic para erros irrecuperáveis
7. **Documente exceções** - Deixe claro quais funções podem lançar exceções

## Armadilhas Comuns

### Armadilha: Engolir Erros

```hemlock
// Ruim: falha silenciosa
try {
    operacao_arriscada();
} catch (e) {
    // Erro ignorado - falha silenciosa
}

// Bom: registrar ou tratar
try {
    operacao_arriscada();
} catch (e) {
    print("Operação falhou: " + e);
    // Tratar apropriadamente
}
```

### Armadilha: Sobrescrita do Finally

```hemlock
// Ruim: finally sobrescreve valor de retorno
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Retorna 0, não 42!
    }
}

// Bom: não retorne no finally
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Apenas limpeza, sem retorno
    }
}
```

### Armadilha: Esquecer Limpeza

```hemlock
// Ruim: arquivo pode não fechar em erro
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Pode lançar
    file.close();  // Nunca alcançado se erro
}

// Bom: usar finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Armadilha: Usar Panic para Erros Esperados

```hemlock
// Ruim: usar panic para erros esperados
fn read_config(caminho) {
    if (!file_exists(caminho)) {
        panic("Arquivo de config não encontrado");  // Muito severo
    }
    return read_file(caminho);
}

// Bom: usar throw para erros esperados
fn read_config(caminho) {
    if (!file_exists(caminho)) {
        throw "Arquivo de config não encontrado: " + caminho;  // Recuperável
    }
    return read_file(caminho);
}
```

## Exemplos

### Exemplo: Tratamento Básico de Erros

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "divisão por zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Erro: " + e);  // Imprime: Erro: divisão por zero
}
```

### Exemplo: Gerenciamento de Recursos

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("Arquivo copiado com sucesso");
    } catch (e) {
        print("Falha ao copiar arquivo: " + e);
        throw e;  // Relança
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Exemplo: Tratamento de Erros Aninhado

```hemlock
fn process_users(usuarios) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < usuarios.length) {
        try {
            validate_user(usuarios[i]);
            save_user(usuarios[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Falha ao processar usuário: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Processados: " + typeof(success_count) + " sucesso, " + typeof(error_count) + " erros");
}
```

### Exemplo: Tipos de Erro Personalizados

```hemlock
fn create_error(tipo, mensagem, detalhes) {
    return {
        type: tipo,
        message: mensagem,
        details: detalhes,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a deve ser um número", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b deve ser um número", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Não pode dividir por zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Detalhes: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Exemplo: Lógica de Retry

```hemlock
fn retry(operacao, max_tentativas) {
    let tentativa = 0;

    while (tentativa < max_tentativas) {
        try {
            return operacao();  // Sucesso!
        } catch (e) {
            tentativa = tentativa + 1;
            if (tentativa >= max_tentativas) {
                throw "Operação falhou após " + typeof(max_tentativas) + " tentativas: " + e;
            }
            print("Tentativa " + typeof(tentativa) + " falhou, tentando novamente...");
        }
    }
}

fn operacao_instavel() {
    // Simula operação instável
    if (random() < 0.7) {
        throw "Operação falhou";
    }
    return "Sucesso";
}

try {
    let resultado = retry(operacao_instavel, 3);
    print(resultado);
} catch (e) {
    print("Todas as tentativas falharam: " + e);
}
```

## Ordem de Execução

Entenda a ordem de execução:

```hemlock
try {
    print("1: início do bloco try");
    throw "erro";
    print("2: nunca alcançado");
} catch (e) {
    print("3: bloco catch");
} finally {
    print("4: bloco finally");
}
print("5: depois do try/catch/finally");

// Saída:
// 1: início do bloco try
// 3: bloco catch
// 4: bloco finally
// 5: depois do try/catch/finally
```

## Limitações Atuais

- **Sem stack trace** - Exceções não capturadas não mostram stack trace (planejado)
- **Algumas funções built-in usam exit** - Algumas funções built-in ainda usam `exit()` em vez de lançar (a ser revisado)
- **Sem tipos de exceção customizados** - Qualquer valor pode ser lançado, mas não há hierarquia formal de exceções

## Tópicos Relacionados

- [Funções](functions.md) - Exceções e retorno de funções
- [Fluxo de Controle](control-flow.md) - Como exceções afetam fluxo de controle
- [Memória](memory.md) - Limpeza de memória com finally

## Veja Também

- **Semântica de Exceções**: Veja seção "Tratamento de Erros" em CLAUDE.md
- **Panic vs Throw**: Diferentes casos de uso para diferentes tipos de erro
- **Garantias do Finally**: Sempre executa, mesmo com return/break/continue
