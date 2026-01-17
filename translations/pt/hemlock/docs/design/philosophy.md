# Filosofia de Design da Linguagem Hemlock

> "Uma linguagem pequena e não-segura, para escrever código não-seguro de forma segura."

Este documento registra os princípios e filosofia de design centrais do Hemlock. Por favor, leia este documento antes de fazer qualquer alteração ou adição à linguagem.

---

## Sumário

- [Posicionamento Central](#posicionamento-central)
- [Princípios de Design](#princípios-de-design)
- [Filosofia de Segurança](#filosofia-de-segurança)
- [Recursos que Não Devem Ser Adicionados](#recursos-que-não-devem-ser-adicionados)
- [Considerações Futuras](#considerações-futuras)
- [Conclusão](#conclusão)

---

## Posicionamento Central

Hemlock é uma **linguagem de script de sistemas**, com gerenciamento manual de memória e controle explícito. Foi projetada para programadores que precisam de:

- O poder da linguagem C
- A facilidade de uso de linguagens de script modernas
- Concorrência assíncrona estruturada integrada
- Sem comportamentos ocultos ou mágica

### O que Hemlock Não É

- **Segura em relação à memória** (ponteiros pendurados são sua responsabilidade)
- **Substituta de Rust, Go ou Lua**
- **Uma linguagem que esconde complexidade de você**

### O que Hemlock É

- **Sempre explícito é melhor que implícito**
- **Educacional e experimental**
- **Uma "camada de script C" para trabalho de sistemas**
- **Honesta sobre os trade-offs**

---

## Princípios de Design

### 1. Explícito é Melhor que Implícito

Hemlock favorece o explícito em todas as construções da linguagem. Não deve haver surpresas, mágica ou comportamentos ocultos.

**Prática ruim (implícita):**
```hemlock
let x = 5  // Ponto e vírgula faltando - deveria dar erro
```

**Boa prática (explícita):**
```hemlock
let x = 5;
free(ptr);  // Você alocou, você libera
```

**Pontos-chave:**
- Ponto e vírgula é obrigatório (sem inserção automática de ponto e vírgula)
- Sem coleta de lixo
- Gerenciamento manual de memória (alloc/free)
- Anotações de tipo são opcionais, mas são verificadas em tempo de execução
- Sem limpeza automática de recursos (sem RAII), mas `defer` oferece limpeza explícita

### 2. Dinâmico por Padrão, Tipos Opcionais

Cada valor tem uma tag de tipo em tempo de execução, mas o sistema foi projetado para ser flexível enquanto ainda captura erros.

**Inferência de tipos:**
- Inteiros pequenos (cabem em i32): `42` → `i32`
- Inteiros grandes (excedem o intervalo de i32): `9223372036854775807` → `i64`
- Ponto flutuante: `3.14` → `f64`

**Tipos explícitos quando necessário:**
```hemlock
let x = 42;              // Inferido como i32 (valor pequeno)
let y: u8 = 255;         // u8 explícito
let z = x + y;           // Promovido para i32
let big = 5000000000;    // Inferido como i64 (excede máximo de i32)
```

**Regras de promoção de tipos** seguem uma hierarquia clara do menor para o maior, com ponto flutuante sempre tendo prioridade sobre inteiros.

### 3. Não-Seguro é um Recurso, Não um Defeito

Hemlock não tenta prevenir todos os erros. Em vez disso, oferece ferramentas seguras enquanto permite que você opte por comportamento não-seguro quando necessário.

**Exemplos de não-segurança intencional:**
- Aritmética de ponteiros pode estourar (responsabilidade do usuário)
- `ptr` bruto não tem verificação de limites (use `buffer` se precisar de segurança)
- Double free é permitido causar crash (gerenciamento manual de memória)
- Sistema de tipos previne acidentes mas permite operações perigosas quando necessário

```hemlock
let p = alloc(10);
let q = p + 100;  // Muito além da alocação - permitido mas perigoso
```

**Filosofia:** O sistema de tipos deve prevenir *acidentes*, mas permitir operações não-seguras *intencionais*.

### 4. Concorrência Estruturada como Cidadã de Primeira Classe

Concorrência não é uma reflexão tardia em Hemlock. Está integrada na linguagem desde o início.

**Recursos principais:**
- `async`/`await` integrados na linguagem
- Channels para comunicação
- `spawn`/`join`/`detach` para gerenciamento de tarefas
- Sem threads brutas, sem locks - apenas estruturado
- Usa threads POSIX para paralelismo real multi-thread

**Não é um event loop ou green threads** - Hemlock usa threads reais do sistema operacional para paralelismo verdadeiro em múltiplos núcleos de CPU.

### 5. Sintaxe Semelhante a C, Baixa Cerimônia

Hemlock deve parecer familiar para programadores de sistemas, enquanto reduz código boilerplate.

**Escolhas de design:**
- Sempre usa blocos `{}`, sem chaves opcionais
- Operadores correspondem a C: `+`, `-`, `*`, `/`, `&&`, `||`, `!`
- Sintaxe de tipos corresponde a Rust/TypeScript: `let x: type = value;`
- Funções são valores de primeira classe
- Mínimo de palavras-chave e formas especiais

---

## Filosofia de Segurança

**A visão do Hemlock sobre segurança:**

> "Nós damos a você ferramentas seguras (`buffer`, anotações de tipo, verificação de limites), mas não forçamos você a usá-las (`ptr`, memória manual, operações não-seguras).
>
> O padrão deve guiar para segurança, mas escotilhas de escape devem estar sempre disponíveis."

### Ferramentas de Segurança Oferecidas

**1. Tipo buffer seguro:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificação de limites
print(b.length);        // 64
free(b);                // Ainda é manual
```

**2. Ponteiros brutos não-seguros:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Você deve lembrar de liberar
```

**3. Anotações de tipo:**
```hemlock
let x: u8 = 255;   // Correto
let y: u8 = 256;   // Erro: fora do intervalo
```

**4. Verificação de tipos em tempo de execução:**
```hemlock
let val = some_function();
if (typeof(val) == "i32") {
    // Pode usar com segurança como inteiro
}
```

### Princípios Orientadores

1. **Usar modo seguro por padrão na documentação** - Mostrar `buffer` antes de `ptr`, encorajar anotações de tipo
2. **Tornar operações não-seguras visíveis** - Aritmética de ponteiros brutos deve parecer intencional
3. **Oferecer escotilhas de escape** - Não impedir usuários experientes de fazer trabalho de baixo nível
4. **Ser honesto sobre trade-offs** - Documentar o que pode dar errado

### Exemplos de Seguro vs Não-Seguro

| Modo Seguro | Modo Não-Seguro | Quando Usar Não-Seguro |
|-------------|-----------------|------------------------|
| Tipo `buffer` | Tipo `ptr` | FFI, código crítico para performance |
| Anotações de tipo | Sem anotações | Interfaces externas, validação |
| Acesso com verificação de limites | Aritmética de ponteiros | Operações de memória de baixo nível |
| Tratamento de exceções | Retornar null/código de erro | Quando exceções são muito pesadas |

---

## Recursos que Não Devem Ser Adicionados

Entender o que **não** deve ser adicionado é tão importante quanto saber o que deve ser adicionado.

### Não Adicione Comportamentos Implícitos

**Exemplos ruins:**

```hemlock
// Ruim: inserção automática de ponto e vírgula
let x = 5
let y = 10

// Ruim: conversão de tipo implícita com perda de precisão
let x: i32 = 3.14  // Deveria truncar ou dar erro?
```

**Motivo:** Comportamentos implícitos causam surpresas e tornam o código mais difícil de entender.

### Não Esconda Complexidade

**Exemplos ruins:**

```hemlock
// Ruim: otimizações mágicas por trás dos panos
let arr = [1, 2, 3]  // Isso é stack ou heap? O usuário deveria saber! (heap, contagem de referência)

// Ruim: liberação automática de ponteiros brutos
let p = alloc(100)  // Isso será liberado automaticamente? Não! Ponteiros brutos sempre precisam de free()
```

**Nota sobre contagem de referência:** Hemlock usa contagem de referência interna para strings, arrays, objetos e buffers - estes são liberados automaticamente quando saem do escopo. Isso é explícito e previsível (limpeza determinística quando a contagem chega a 0, sem pausas de GC). Ponteiros brutos (`ptr` de `alloc()`) não são contados por referência e sempre precisam de `free()` manual.

**Motivo:** Complexidade oculta torna impossível prever performance e depurar problemas.

### Não Quebre Semânticas Existentes

**Nunca mude estas decisões centrais:**
- Ponto e vírgula é obrigatório - não torná-lo opcional
- Gerenciamento manual de memória - não adicionar GC
- Strings mutáveis - não torná-las imutáveis
- Verificação de tipos em tempo de execução - não removê-la

**Motivo:** Consistência e estabilidade são mais importantes que recursos da moda.

### Não Adicione Recursos de "Conveniência" que Reduzam Explicitude

**Exemplos de recursos a evitar:**
- Sobrecarga de operadores (tipos de usuário talvez ok, mas com cuidado)
- Coerção de tipo implícita que perde informação
- Limpeza automática de recursos (RAII)
- Encadeamento de métodos que esconde complexidade
- DSLs e sintaxe mágica

**Exceção:** Se um recurso de conveniência é **açúcar sintático explícito** para operações simples, pode ser ok:
- `else if` é ok (é apenas if aninhado)
- Interpolação de strings pode ser ok, se for obviamente açúcar sintático
- Sintaxe de métodos para objetos é ok (é explícito o que faz)

---

## Considerações Futuras

### Pode Ser Adicionado (Em Discussão)

Estes recursos se alinham com a filosofia do Hemlock, mas precisam de design cuidadoso:

**1. Pattern Matching**
```hemlock
match (value) {
    case i32: print("inteiro");
    case string: print("texto");
    case _: print("outro");
}
```
- Verificação de tipos explícita
- Sem custos ocultos
- Possível verificação de exaustividade em tempo de compilação

**2. Tipos de Erro (`Result<T, E>`)**
```hemlock
fn divide(a: i32, b: i32): Result<i32, string> {
    if (b == 0) {
        return Err("divisão por zero");
    }
    return Ok(a / b);
}
```
- Tratamento de erros explícito
- Força o usuário a considerar erros
- Alternativa a exceções

**3. Tipos de Array/Slice**
- Já tem arrays dinâmicos
- Pode adicionar arrays de tamanho fixo para alocação em stack
- Precisa ser explícito sobre stack vs heap

**4. Ferramentas de Segurança de Memória Melhoradas**
- Flag opcional de verificação de limites
- Detecção de vazamento de memória em builds de debug
- Integração com sanitizers

### Provavelmente Nunca Será Adicionado

Estes recursos violam princípios centrais:

**1. Coleta de Lixo**
- Esconde complexidade de gerenciamento de memória
- Performance imprevisível
- Viola princípio de controle explícito

**2. Gerenciamento Automático de Memória**
- Mesmas razões que GC
- Contagem de referência pode ser ok se explícita

**3. Conversões de Tipo Implícitas que Perdem Dados**
- Viola "explícito é melhor que implícito"
- Fonte de erros sutis

**4. Macros (Complexas)**
- Muito poder, muita complexidade
- Sistema de macros simples pode ser ok
- Prefira geração de código ou funções

**5. Orientação a Objetos Baseada em Classes com Herança**
- Muitos comportamentos implícitos
- Duck typing e objetos são suficientes
- Composição sobre herança

**6. Sistema de Módulos com Resolução Complexa**
- Manter imports simples e explícitos
- Sem caminhos de busca mágicos
- Sem resolução de versões (use gerenciador de pacotes do SO)

---

## Conclusão

### Confiança e Responsabilidade

Hemlock é sobre **confiança e responsabilidade**. Nós confiamos que os programadores podem:

- Gerenciar memória corretamente
- Usar tipos apropriadamente
- Tratar erros corretamente
- Entender trade-offs

Em troca, Hemlock oferece:

- Sem custos ocultos
- Sem comportamentos inesperados
- Controle total quando necessário
- Ferramentas seguras quando necessário

### Perguntas Orientadoras

**Ao considerar um novo recurso, pergunte:**

> "Isso dá ao programador mais controle explícito, ou esconde algo?"

- Se **aumenta controle explícito** → Provavelmente cabe no Hemlock
- Se **esconde complexidade** → Provavelmente não pertence aqui
- Se é **açúcar sintático opcional** com documentação clara → Talvez ok

### Bons Exemplos de Adições

- **Switch statement** - Fluxo de controle explícito, sem mágica, semântica clara

- **Async/await com pthreads** - Concorrência explícita, paralelismo real, usuário controla spawn

- **Tipo Buffer junto com ptr** - Oferece escolha entre seguro e não-seguro

- **Anotações de tipo opcionais** - Ajuda a capturar erros sem forçar rigidez

- **Try/catch/finally** - Tratamento de erros explícito com fluxo de controle claro

### Maus Exemplos de Adições

- **Inserção automática de ponto e vírgula** - Esconde erros de sintaxe, torna código obscuro

- **RAII/Destrutores** - Limpeza automática esconde quando recursos são liberados

- **Coalescência de null implícita** - Esconde verificações de null, torna código mais difícil de entender

- **Strings com crescimento automático** - Esconde alocação de memória, performance imprevisível

---

## Resumo

Hemlock não tenta ser a linguagem mais segura, a mais rápida ou a mais rica em recursos.

**Hemlock tenta ser a linguagem mais *honesta*.**

Ela diz exatamente o que está fazendo, dá controle quando você precisa, e não esconde arestas cortantes. É uma linguagem para quem quer entender código em nível baixo enquanto ainda aproveita conveniências modernas.

Se você não tem certeza se um recurso pertence ao Hemlock, lembre-se:

> **Sempre explícito é melhor que implícito.**
> **Não-seguro é um recurso, não um defeito.**
> **O usuário é responsável, e isso está ok.**
