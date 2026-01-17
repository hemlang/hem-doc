# Referencia da API de Memoria

Documentacao completa das funcoes de gerenciamento de memoria e tipos de ponteiro do Hemlock.

---

## Visao Geral

Hemlock fornece **gerenciamento manual de memoria** com alocacao e liberacao explicitas. A memoria e gerenciada atraves de dois tipos de ponteiro: ponteiros brutos (`ptr`) e buffers seguros (`buffer`).

**Principios Fundamentais:**
- Alocacao e liberacao explicitas
- Sem coleta de lixo
- Usuario responsavel por chamar `free()`
- Contagem de referencias interna para seguranca de escopo/reatribuicao (veja abaixo)

### Contagem de Referencias Interna

O runtime usa contagem de referencias internamente para gerenciar tempos de vida de objetos dentro de escopos. Para a maioria das variaveis locais, a limpeza e automatica.

**Automatico (sem `free()` necessario):**
- Variaveis locais de tipos com contagem de referencias (buffer, array, object, string) sao liberadas ao sair do escopo
- Reatribuicao de variavel libera o valor antigo
- Elementos de container sao liberados quando o container e liberado

**Requer `free()` manual:**
- Ponteiros brutos de `alloc()` - sempre requerem
- Limpeza antecipada antes do fim do escopo
- Dados de longa duracao/globais

Veja o [Guia de Gerenciamento de Memoria](../language-guide/memory.md#internal-reference-counting) para detalhes.

---

## Tipos de Ponteiro

### ptr (Ponteiro Bruto)

**Tipo:** `ptr`

**Descricao:** Endereco de memoria bruto sem verificacao de limites ou rastreamento.

**Tamanho:** 8 bytes

**Casos de Uso:**
- Operacoes de memoria de baixo nivel
- FFI (Interface de Funcao Estrangeira)
- Performance maxima (sem overhead)

**Seguranca:** Inseguro - sem verificacao de limites, usuario deve rastrear tempo de vida

**Exemplo:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer (Buffer Seguro)

**Tipo:** `buffer`

**Descricao:** Wrapper de ponteiro seguro com verificacao de limites.

**Estrutura:** Ponteiro + comprimento + capacidade + contagem de referencias

**Propriedades:**
- `.length` - Tamanho do buffer (i32)
- `.capacity` - Capacidade alocada (i32)

**Casos de Uso:**
- Maioria das alocacoes de memoria
- Quando seguranca e importante
- Arrays dinamicos

**Seguranca:** Verificacao de limites em acesso indexado

**Contagem de Referencias:** Buffers sao contados por referencia internamente. Liberacao automatica ao sair do escopo ou reatribuir variavel. Use `free()` para limpeza antecipada ou dados de longa duracao.

**Exemplo:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Verificacao de limites
print(b.length);        // 64
free(b);
```

---

## Funcoes de Alocacao de Memoria

### alloc

Aloca memoria bruta.

**Assinatura:**
```hemlock
alloc(size: i32): ptr
```

**Parametros:**
- `size` - Numero de bytes a alocar

**Retorna:** Ponteiro para memoria alocada (`ptr`)

**Exemplo:**
```hemlock
let p = alloc(1024);        // Aloca 1KB
memset(p, 0, 1024);         // Inicializa com zeros
free(p);                    // Libera quando terminar

// Aloca para estrutura
let struct_size = 16;
let p2 = alloc(struct_size);
```

**Comportamento:**
- Retorna memoria nao inicializada
- Memoria deve ser liberada manualmente
- Retorna `null` em falha de alocacao (chamador deve verificar)

**Veja Tambem:** `buffer()` para alternativa mais segura

---

### buffer

Aloca buffer seguro com verificacao de limites.

**Assinatura:**
```hemlock
buffer(size: i32): buffer
```

**Parametros:**
- `size` - Tamanho do buffer (bytes)

**Retorna:** Objeto buffer

**Exemplo:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// Acesso com verificacao de limites
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // Erro: fora dos limites

free(buf);
```

**Propriedades:**
- `.length` - Tamanho atual (i32)
- `.capacity` - Capacidade alocada (i32)

**Comportamento:**
- Inicializa memoria com zeros
- Fornece verificacao de limites em acesso indexado
- Retorna `null` em falha de alocacao (chamador deve verificar)
- Deve ser liberado manualmente

---

### free

Libera memoria alocada.

**Assinatura:**
```hemlock
free(ptr: ptr | buffer): null
```

**Parametros:**
- `ptr` - Ponteiro ou buffer a liberar

**Retorna:** `null`

**Exemplo:**
```hemlock
// Libera ponteiro bruto
let p = alloc(1024);
free(p);

// Libera buffer
let buf = buffer(256);
free(buf);
```

**Comportamento:**
- Libera memoria alocada por `alloc()` ou `buffer()`
- Liberacao dupla causa crash (responsabilidade do usuario evitar)
- Liberar ponteiro invalido causa comportamento indefinido

**Importante:** Voce aloca, voce libera. Sem limpeza automatica.

---

### realloc

Redimensiona memoria alocada.

**Assinatura:**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**Parametros:**
- `ptr` - Ponteiro a redimensionar
- `new_size` - Novo tamanho (bytes)

**Retorna:** Ponteiro para memoria redimensionada (pode ser endereco diferente)

**Exemplo:**
```hemlock
let p = alloc(100);
// ... usa memoria ...

// Precisa de mais espaco
p = realloc(p, 200);        // Agora 200 bytes
// ... usa memoria expandida ...

free(p);
```

**Comportamento:**
- Pode mover memoria para novo local
- Preserva dados existentes (ate o minimo do tamanho antigo/novo)
- Ponteiro antigo invalido apos realloc bem-sucedido (use o ponteiro retornado)
- Se new_size for menor, dados sao truncados
- Retorna `null` em falha de alocacao (ponteiro original ainda valido)

**Importante:** Sempre verifique `null` e atualize variavel de ponteiro com o resultado.

---

## Operacoes de Memoria

### memset

Preenche memoria com um valor de byte.

**Assinatura:**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**Parametros:**
- `ptr` - Ponteiro para memoria
- `byte` - Valor de byte a preencher (0-255)
- `size` - Numero de bytes a preencher

**Retorna:** `null`

**Exemplo:**
```hemlock
let p = alloc(100);

// Zera memoria
memset(p, 0, 100);

// Preenche com valor especifico
memset(p, 0xFF, 100);

// Inicializa buffer
let buf = alloc(256);
memset(buf, 65, 256);       // Preenche com 'A'

free(p);
free(buf);
```

**Comportamento:**
- Escreve valor de byte em cada byte no intervalo
- Valor de byte truncado para 8 bits (0-255)
- Sem verificacao de limites (inseguro)

---

### memcpy

Copia memoria da origem para o destino.

**Assinatura:**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**Parametros:**
- `dest` - Ponteiro de destino
- `src` - Ponteiro de origem
- `size` - Numero de bytes a copiar

**Retorna:** `null`

**Exemplo:**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// Inicializa origem
memset(src, 65, 100);

// Copia para destino
memcpy(dest, src, 100);

// dest agora contem os mesmos dados que src

free(src);
free(dest);
```

**Comportamento:**
- Copia byte a byte de src para dest
- Sem verificacao de limites (inseguro)
- Comportamento indefinido para regioes sobrepostas (use com cuidado)

---

## Operacoes de Memoria Tipadas

### sizeof

Obtem o tamanho em bytes de um tipo.

**Assinatura:**
```hemlock
sizeof(type): i32
```

**Parametros:**
- `type` - Identificador de tipo (ex: `i32`, `f64`, `ptr`)

**Retorna:** Tamanho em bytes (i32)

**Tamanhos de Tipos:**

| Tipo | Tamanho (bytes) |
|------|-----------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**Exemplo:**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// Calcula tamanho de alocacao de array
let count = 100;
let total = sizeof(i32) * count; // 400 bytes
```

**Comportamento:**
- Retorna 0 para tipo desconhecido
- Aceita identificadores de tipo e strings de tipo

---

### talloc

Aloca array de valores tipados.

**Assinatura:**
```hemlock
talloc(type, count: i32): ptr
```

**Parametros:**
- `type` - Tipo a alocar (ex: `i32`, `f64`, `ptr`)
- `count` - Numero de elementos (deve ser positivo)

**Retorna:** Ponteiro para array alocado, ou `null` em falha de alocacao

**Exemplo:**
```hemlock
let arr = talloc(i32, 100);      // Array de 100 i32 (400 bytes)
let floats = talloc(f64, 50);    // Array de 50 f64 (400 bytes)
let bytes = talloc(u8, 1024);    // Array de 1024 bytes

// Sempre verifique falha de alocacao
if (arr == null) {
    panic("alocacao falhou");
}

// Usa memoria alocada
// ...

free(arr);
free(floats);
free(bytes);
```

**Comportamento:**
- Aloca `sizeof(type) * count` bytes
- Retorna memoria nao inicializada
- Memoria deve ser liberada manualmente com `free()`
- Retorna `null` em falha de alocacao (chamador deve verificar)
- Panic se count nao for positivo

---

## Propriedades de Buffer

### .length

Obtem o tamanho do buffer.

**Tipo:** `i32`

**Acesso:** Somente leitura

**Exemplo:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

Obtem a capacidade do buffer.

**Tipo:** `i32`

**Acesso:** Somente leitura

**Exemplo:**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**Nota:** Atualmente, `.length` e `.capacity` sao iguais para buffers criados com `buffer()`.

---

## Padroes de Uso

### Padrao de Alocacao Basica

```hemlock
// Aloca
let p = alloc(1024);
if (p == null) {
    panic("alocacao falhou");
}

// Usa
memset(p, 0, 1024);

// Libera
free(p);
```

### Padrao de Buffer Seguro

```hemlock
// Aloca buffer
let buf = buffer(256);
if (buf == null) {
    panic("alocacao de buffer falhou");
}

// Usa com verificacao de limites
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// Libera
free(buf);
```

### Padrao de Crescimento Dinamico

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("alocacao falhou");
}

// ... usa memoria ...

// Precisa de mais espaco - verifica falha
let new_p = realloc(p, 200);
if (new_p == null) {
    // Ponteiro original ainda valido, limpa
    free(p);
    panic("realloc falhou");
}
p = new_p;
size = 200;

// ... usa memoria expandida ...

free(p);
```

### Padrao de Copia de Memoria

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// Cria copia
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## Consideracoes de Seguranca

**Gerenciamento de memoria Hemlock e inseguro por design:**

### Armadilhas Comuns

**1. Vazamento de Memoria**
```hemlock
// Errado: vazamento de memoria
fn create_buffer() {
    let p = alloc(1024);
    return null;  // Memoria vazou!
}

// Correto: limpeza adequada
fn create_buffer() {
    let p = alloc(1024);
    // ... usa memoria ...
    free(p);
    return null;
}
```

**2. Uso Apos Liberacao**
```hemlock
// Errado: uso apos liberacao
let p = alloc(100);
free(p);
memset(p, 0, 100);  // Crash: usando memoria liberada

// Correto: nao usa apos liberar
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// Nao usa p2 depois disso
```

**3. Liberacao Dupla**
```hemlock
// Errado: liberacao dupla
let p = alloc(100);
free(p);
free(p);  // Crash: liberacao dupla

// Correto: libera apenas uma vez
let p2 = alloc(100);
free(p2);
```

**4. Estouro de Buffer (ptr)**
```hemlock
// Errado: estouro de buffer para ptr
let p = alloc(10);
memset(p, 65, 100);  // Crash: escrevendo alem da alocacao

// Correto: usa buffer para verificacao de limites
let buf = buffer(10);
// buf[100] = 65;  // Erro: verificacao de limites falha
```

**5. Ponteiro Pendurado**
```hemlock
// Errado: ponteiro pendurado
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // Crash: p2 esta pendurado

// Correto: rastreia propriedade cuidadosamente
let p = alloc(100);
// ... usa p ...
free(p);
// Nao mantem outras referencias para p
```

**6. Falha de Alocacao Nao Verificada**
```hemlock
// Errado: nao verifica null
let p = alloc(1000000000);  // Pode falhar em pouca memoria
memset(p, 0, 1000000000);   // Crash: p e null

// Correto: sempre verifica resultado de alocacao
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("sem memoria");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## Quando Usar O Que

### Use `buffer()` quando:
- Verificacao de limites e necessaria
- Trabalhando com dados dinamicos
- Seguranca e importante
- Aprendendo Hemlock

### Use `alloc()` quando:
- Performance maxima e necessaria
- FFI/interfaceando com C
- Voce sabe o layout exato de memoria
- Voce e um especialista

### Use `realloc()` quando:
- Crescendo/diminuindo alocacoes
- Arrays dinamicos
- Dados precisam ser preservados

---

## Resumo Completo das Funcoes

| Funcao    | Assinatura                                 | Retorna  | Descricao                  |
|-----------|--------------------------------------------|----------|----------------------------|
| `alloc`   | `(size: i32)`                              | `ptr`    | Aloca memoria bruta        |
| `buffer`  | `(size: i32)`                              | `buffer` | Aloca buffer seguro        |
| `free`    | `(ptr: ptr \| buffer)`                     | `null`   | Libera memoria             |
| `realloc` | `(ptr: ptr, new_size: i32)`                | `ptr`    | Redimensiona alocacao      |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`         | `null`   | Preenche memoria           |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`         | `null`   | Copia memoria              |
| `sizeof`  | `(type)`                                   | `i32`    | Obtem tamanho do tipo      |
| `talloc`  | `(type, count: i32)`                       | `ptr`    | Aloca array tipado         |

---

## Veja Tambem

- [Sistema de Tipos](type-system.md) - Tipos de ponteiro e buffer
- [Funcoes Integradas](builtins.md) - Todas as funcoes integradas
- [API de Strings](string-api.md) - Metodo `.to_bytes()` de strings
