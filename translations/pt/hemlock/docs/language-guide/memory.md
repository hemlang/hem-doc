# Gerenciamento de Memoria

Hemlock adota **gerenciamento manual de memoria**, com controle explicito sobre alocacao e liberacao. Este guia abrange o modelo de memoria do Hemlock, os dois tipos de ponteiros e a API completa de memoria.

---

## Fundamentos de Memoria 101

**Novo em programacao?** Comece aqui. Se voce ja entende gerenciamento de memoria, pode pular para [Filosofia de Design](#filosofia-de-design).

### O que e Gerenciamento de Memoria?

Quando seu programa precisa armazenar dados (texto, numeros, listas), ele precisa de espaco para colocar esses dados. Este espaco vem da memoria do computador (RAM). Gerenciamento de memoria envolve:

1. **Obter espaco** - Solicitar memoria quando necessario
2. **Usar espaco** - Ler e escrever dados
3. **Devolver espaco** - Retornar memoria quando terminar

### Por que Isso Importa?

Imagine uma biblioteca com livros limitados:
- Se voce continua emprestando livros e nunca devolve, eventualmente nao havera livros disponiveis
- Se voce tentar ler um livro que ja devolveu, havera confusao ou problemas

Memoria funciona da mesma forma. Se voce esquecer de devolver memoria, seu programa usara cada vez mais memoria ("vazamento de memoria"). Se voce tentar usar memoria apos devolve-la, coisas ruins acontecerao.

### A Boa Noticia

**Na maior parte do tempo, voce nao precisa pensar nisso!**

Hemlock limpa automaticamente a maioria dos tipos comuns:

```hemlock
fn example() {
    let nome = "Alice";       // Hemlock gerencia isso
    let numeros = [1, 2, 3];  // E isso tambem
    let pessoa = { age: 30 }; // E isso tambem

    // Quando a funcao termina, tudo e limpo automaticamente!
}
```

### Quando Voce Precisa Pensar Nisso

Voce so precisa de gerenciamento manual de memoria ao usar:

1. **`alloc()`** - Alocacao de memoria bruta (retorna `ptr`)
2. **`buffer()`** - Quando voce quer liberar antecipadamente (opcional - libera automaticamente no fim do escopo)

```hemlock
// Isso requer limpeza manual:
let raw = alloc(100);   // Memoria bruta - voce deve liberar
// ... usar raw ...
free(raw);              // Obrigatorio! Caso contrario, vazamento de memoria

// Isso limpa automaticamente (mas voce pode liberar antes):
let buf = buffer(100);  // Buffer seguro
// ... usar buf ...
// free(buf);           // Opcional - libera automaticamente no fim do escopo
```

### Regra Simples

> **Se voce chamar `alloc()`, voce deve chamar `free()`.**
>
> Todo o resto e tratado para voce.

### Qual Devo Usar?

| Cenario | Use Isso | Por Que |
|---------|----------|---------|
| **Comecando a aprender** | `buffer()` | Seguro, com verificacao de limites, limpeza automatica |
| **Precisa de armazenamento de bytes** | `buffer()` | Seguro e simples |
| **Interagindo com bibliotecas C (FFI)** | `alloc()` / `ptr` | Necessario para interoperabilidade C |
| **Performance maxima** | `alloc()` / `ptr` | Sem overhead de verificacao de limites |
| **Nao tem certeza** | `buffer()` | Sempre a escolha mais segura |

### Exemplo Rapido: Seguro vs Bruto

```hemlock
// Recomendado: buffer seguro
fn exemplo_seguro() {
    let data = buffer(10);
    data[0] = 65;           // OK
    data[5] = 66;           // OK
    // data[100] = 67;      // Erro - Hemlock impede (verificacao de limites)
    free(data);             // Limpeza
}

// Avancado: ponteiro bruto (use apenas quando necessario)
fn exemplo_bruto() {
    let data = alloc(10);
    *data = 65;             // OK
    *(data + 5) = 66;       // OK
    *(data + 100) = 67;     // Perigoso - sem verificacao de limites, corrompe memoria!
    free(data);             // Limpeza
}
```

**Comece com `buffer()`. So use `alloc()` quando precisar especificamente de ponteiros brutos.**

---

## Filosofia de Design

Hemlock segue gerenciamento explicito de memoria com padroes sensiveis:
- Sem coleta de lixo (sem pausas imprevisiveis)
- Contagem de referencias interna para tipos comuns (string, array, object, buffer)
- Ponteiros brutos (`ptr`) requerem `free()` manual

Esta abordagem hibrida oferece controle total quando necessario (ponteiros brutos), enquanto previne erros comuns em casos de uso tipicos (tipos com contagem de referencias liberam automaticamente ao sair do escopo).

## Contagem de Referencias Interna

O runtime usa **contagem de referencias interna** para gerenciar ciclos de vida de objetos. Para a maioria das variaveis locais de tipos com contagem de referencias, a limpeza e automatica e deterministica.

### O que a Contagem de Referencias Trata

O runtime gerencia automaticamente contagem de referencias quando:

1. **Reatribuicao de variavel** - Valor antigo e liberado:
   ```hemlock
   let x = "primeiro";   // ref_count = 1
   x = "segundo";        // "primeiro" liberado internamente, "segundo" ref_count = 1
   ```

2. **Saida de escopo** - Variaveis locais sao liberadas:
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // arr liberado quando funcao retorna
   ```

3. **Container liberado** - Elementos sao liberados:
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // ref_count de obj1 e obj2 decrementado
   ```

### Quando `free()` e Necessario vs Automatico

**Automatico (nao precisa de `free()`):** Variaveis locais de tipos com contagem de referencias sao liberadas ao sair do escopo:

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... usar eles ...
}  // Todos liberados automaticamente quando funcao retorna - nao precisa de free()
```

**Requer `free()` manual:**

1. **Ponteiros brutos** - `alloc()` nao tem contagem de referencias:
   ```hemlock
   let p = alloc(64);
   // ... usar p ...
   free(p);  // Sempre necessario - caso contrario vaza
   ```

2. **Limpeza antecipada** - Libera antes do fim do escopo para liberar memoria mais cedo:
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10MB
       // ... terminou com big ...
       free(big);  // Libera agora, nao espera funcao retornar
       // ... mais trabalho que nao precisa de big ...
   }
   ```

3. **Dados de longa duracao** - Dados globais ou armazenados em estruturas persistentes:
   ```hemlock
   let cache = {};  // Nivel de modulo, vive ate o programa terminar a menos que liberado

   fn cleanup() {
       free(cache);  // Limpeza manual para dados de longa duracao
   }
   ```

### Contagem de Referencias vs Coleta de Lixo

| Aspecto | Contagem de Referencias Hemlock | Coleta de Lixo |
|---------|--------------------------------|----------------|
| Quando limpa | Deterministico (imediatamente quando ref chega a 0) | Nao-deterministico (GC decide quando) |
| Responsabilidade do usuario | Deve chamar `free()` | Totalmente automatico |
| Pausas de runtime | Nenhuma | Pausas "stop-the-world" |
| Visibilidade | Detalhe de implementacao oculto | Geralmente invisivel |
| Referencias circulares | Tratadas via rastreamento de conjunto visitado | Tratadas via rastreamento |

### Quais Tipos Tem Contagem de Referencias

| Tipo | Contagem de Referencias | Notas |
|------|------------------------|-------|
| `ptr` | Nao | Sempre requer `free()` manual |
| `buffer` | Sim | Liberado automaticamente ao sair do escopo; `free()` manual para limpeza antecipada |
| `array` | Sim | Liberado automaticamente ao sair do escopo; `free()` manual para limpeza antecipada |
| `object` | Sim | Liberado automaticamente ao sair do escopo; `free()` manual para limpeza antecipada |
| `string` | Sim | Totalmente automatico, nao precisa de `free()` |
| `function` | Sim | Totalmente automatico (ambiente de closure) |
| `task` | Sim | Contagem de referencias atomica thread-safe |
| `channel` | Sim | Contagem de referencias atomica thread-safe |
| Primitivos | Nao | Alocados na stack, sem alocacao heap |

### Por Que Este Design?

Esta abordagem hibrida oferece:
- **Controle explicito** - Voce decide quando liberar
- **Seguranca de escopo** - Reatribuicao nao vaza
- **Performance previsivel** - Sem pausas de GC
- **Suporte a closures** - Funcoes podem capturar variaveis com seguranca

A filosofia permanece: voce esta no controle, mas o runtime ajuda a prevenir erros comuns como vazamentos em reatribuicao ou double-free em containers.

## Dois Tipos de Ponteiros

Hemlock fornece dois tipos distintos de ponteiros com diferentes caracteristicas de seguranca:

### `ptr` - Ponteiro Bruto (Perigoso)

Ponteiros brutos sao **apenas enderecos**, com garantias minimas de seguranca:

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Voce deve lembrar de liberar
```

**Caracteristicas:**
- Apenas um endereco de 8 bytes
- Sem verificacao de limites
- Sem rastreamento de tamanho
- Ciclo de vida totalmente gerenciado pelo usuario
- Adequado para especialistas e FFI

**Casos de uso:**
- Programacao de sistemas de baixo nivel
- Interface de Funcao Estrangeira (FFI)
- Codigo critico de performance
- Quando controle total e necessario

**Perigos:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Muito alem da alocacao - permitido mas perigoso
free(p);
let x = *p;       // Ponteiro dangling - comportamento indefinido
free(p);          // Double free - vai crashar
```

### `buffer` - Wrapper Seguro (Recomendado)

Buffer fornece **acesso com verificacao de limites** enquanto ainda requer liberacao manual:

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificacao de limites
print(b.length);        // 64
free(b);                // Ainda e manual
```

**Caracteristicas:**
- Ponteiro + tamanho + capacidade
- Verificacao de limites no acesso
- Ainda requer `free()` manual
- Padrao melhor para a maioria do codigo

**Propriedades:**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100 (tamanho atual)
print(buf.capacity);    // 100 (capacidade alocada)
```

**Verificacao de limites:**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // OK
buf[100] = 42;    // Erro: indice fora dos limites
```

## API de Memoria

### Alocacao Principal

**`alloc(bytes)` - Aloca memoria bruta**
```hemlock
let p = alloc(1024);  // Aloca 1KB, retorna ptr
// ... usar memoria
free(p);
```

**`buffer(size)` - Aloca buffer seguro**
```hemlock
let buf = buffer(256);  // Aloca buffer de 256 bytes
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - Libera memoria**
```hemlock
let p = alloc(100);
free(p);  // Deve liberar para evitar vazamento de memoria

let buf = buffer(100);
free(buf);  // Funciona para ptr e buffer
```

**Importante:** `free()` funciona para tipos `ptr` e `buffer`.

### Operacoes de Memoria

**`memset(ptr, byte, size)` - Preenche memoria**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // Zera 100 bytes
memset(p, 65, 10);     // Preenche primeiros 10 bytes com 'A'
free(p);
```

**`memcpy(dest, src, size)` - Copia memoria**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // Copia 50 bytes de src para dst
free(src);
free(dst);
```

**`realloc(ptr, size)` - Redimensiona alocacao**
```hemlock
let p = alloc(100);
// ... usar 100 bytes
p = realloc(p, 200);   // Redimensiona para 200 bytes
// ... usar 200 bytes
free(p);
```

**Nota:** Apos `realloc()`, o ponteiro antigo pode ser invalido. Sempre use o ponteiro retornado.

### Alocacao Tipada

Hemlock fornece helpers de alocacao tipada para conveniencia:

```hemlock
let arr = talloc(i32, 100);  // Aloca 100 valores i32 (400 bytes)
let size = sizeof(i32);      // Retorna 4 (bytes)
```

**`sizeof(type)`** retorna o tamanho em bytes de um tipo:
- `sizeof(i8)` / `sizeof(u8)` -> 1
- `sizeof(i16)` / `sizeof(u16)` -> 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` -> 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` -> 8
- `sizeof(ptr)` -> 8 (sistemas 64-bit)

**`talloc(type, count)`** aloca `count` elementos do `type`:

```hemlock
let ints = talloc(i32, 10);   // 40 bytes para 10 valores i32
let floats = talloc(f64, 5);  // 40 bytes para 5 valores f64
free(ints);
free(floats);
```

## Padroes Comuns

### Padrao: Alocar, Usar, Liberar

O padrao basico de gerenciamento de memoria:

```hemlock
// 1. Alocar
let data = alloc(1024);

// 2. Usar
memset(data, 0, 1024);
// ... fazer trabalho

// 3. Liberar
free(data);
```

### Padrao: Uso Seguro de Buffer

Prefira buffer para acesso com verificacao de limites:

```hemlock
let buf = buffer(256);

// Iteracao segura
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### Padrao: Gerenciamento de Recursos com try/finally

Garante limpeza mesmo em erros:

```hemlock
let data = alloc(1024);
try {
    // ... operacoes arriscadas
    process(data);
} finally {
    free(data);  // Libera mesmo em erro
}
```

## Consideracoes de Seguranca de Memoria

### Double Free

**Permitido mas vai crashar:**
```hemlock
let p = alloc(100);
free(p);
free(p);  // Crash: double free detectado
```

**Prevencao:**
```hemlock
let p = alloc(100);
free(p);
p = null;  // Define como null apos liberar

if (p != null) {
    free(p);  // Nao vai executar
}
```

### Ponteiro Dangling

**Permitido mas comportamento indefinido:**
```hemlock
let p = alloc(100);
*p = 42;      // OK
free(p);
let x = *p;   // Indefinido: lendo memoria liberada
```

**Prevencao:** Nao acesse memoria apos liberar.

### Vazamento de Memoria

**Facil de criar, dificil de debugar:**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // Esqueceu de liberar!
    return;  // Vazamento de memoria
}
```

**Prevencao:** Sempre pareie `alloc()` com `free()`:
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... usar p
    } finally {
        free(p);  // Sempre libera
    }
}
```

### Aritmetica de Ponteiros

**Permitida mas perigosa:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Muito alem dos limites da alocacao
*q = 42;          // Indefinido: escrita fora dos limites
free(p);
```

**Use buffer para verificacao de limites:**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // Erro: verificacao de limites previne overflow
```

## Melhores Praticas

1. **Use `buffer` por padrao** - Use `buffer` a menos que precise especificamente de `ptr` bruto
2. **Pareie alloc/free** - Cada `alloc()` deve ter exatamente um `free()`
3. **Use try/finally** - Use tratamento de excecoes para garantir limpeza
4. **Null apos free** - Defina ponteiros como `null` apos liberar para capturar uso-apos-liberar
5. **Verificacao de limites** - Use indexacao de buffer para verificacao automatica de limites
6. **Documente propriedade** - Deixe claro qual codigo possui e libera cada alocacao

## Exemplos

### Exemplo: Construtor de String Dinamico

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // Chamador deve liberar
}

let msg = build_message(5);
// ... usar msg
free(msg);
```

### Exemplo: Operacoes Seguras de Array

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // Preencher array
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // Processar
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // Sempre limpa
    }
}
```

### Exemplo: Padrao de Pool de Memoria

```hemlock
// Pool de memoria simples (simplificado)
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool esgotado";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// Usar pool
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// Liberar pool inteiro de uma vez
free(pool);
```

## Limitacoes

Limitacoes atuais a serem observadas:

- **Ponteiros brutos requerem liberacao manual** - `alloc()` retorna `ptr` sem contagem de referencias
- **Sem alocadores customizados** - Apenas malloc/free do sistema

**Nota:** Tipos com contagem de referencias (string, array, object, buffer) liberam automaticamente ao sair do escopo. Apenas `ptr` bruto de `alloc()` requer `free()` explicito.

## Topicos Relacionados

- [Strings](strings.md) - Gerenciamento de memoria de strings e codificacao UTF-8
- [Arrays](arrays.md) - Arrays dinamicos e suas caracteristicas de memoria
- [Objetos](objects.md) - Alocacao e ciclo de vida de objetos
- [Tratamento de Erros](error-handling.md) - Limpeza com try/finally

## Veja Tambem

- **Filosofia de Design**: Veja secao "Memory Management" em CLAUDE.md
- **Sistema de Tipos**: Veja [Tipos](types.md) para detalhes dos tipos `ptr` e `buffer`
- **FFI**: Ponteiros brutos sao essenciais para Interface de Funcao Estrangeira
