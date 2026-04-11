# Otimizacoes do Compilador

O compilador Hemlock (`hemlockc`) aplica diversos passes de otimizacao ao gerar codigo C. Essas otimizacoes sao automaticas e nao requerem intervencao do usuario, mas entende-las ajuda a explicar as caracteristicas de performance.

---

## Visao Geral

```
Fonte (.hml)
    ↓
  Parse → AST
    ↓
  Verificacao de Tipos (opcional)
    ↓
  Passe de Otimizacao do AST
    ↓
  Geracao de Codigo C (com inlining + unboxing)
    ↓
  Compilacao GCC/Clang
```

---

## Unboxing de Expressoes

O runtime do Hemlock representa todos os valores como structs `HmlValue` com tags. No interpretador, toda operacao aritmetica faz boxing e unboxing dos valores atraves de dispatch em runtime. O compilador elimina esse overhead para expressoes com tipos primitivos conhecidos.

**Antes (codegen ingenue):**
```c
// x + 1 onde x e i32
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 chamadas de boxing + dispatch em runtime
```

**Depois (com unboxing de expressao):**
```c
// x + 1 onde x e i32
hml_val_i32((x + 1))  // Aritmetica C pura, unico box no final
```

### O Que Sofre Unboxing

- Aritmetica binaria: `+`, `-`, `*`, `%`
- Operacoes bit a bit: `&`, `|`, `^`, `<<`, `>>`
- Comparacoes: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Operacoes unarias: `-`, `~`, `!`
- Variaveis com anotacao de tipo e contadores de loop

### O Que Volta ao HmlValue

- Chamadas de funcao (tipo de retorno pode ser dinamico)
- Acesso a array/objeto (tipo do elemento desconhecido em compile-time)
- Variaveis sem anotacoes de tipo e sem tipo inferido

### Dica

Adicionar anotacoes de tipo em variaveis no caminho quente ajuda o compilador a aplicar unboxing:

```hemlock
// O compilador pode fazer unboxing de toda esta expressao
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## Inlining de Funcoes Multi-Nivel

O compilador faz inline de funcoes pequenas nos pontos de chamada, substituindo o overhead de chamada de funcao por codigo direto. Hemlock suporta inlining multi-nivel ate profundidade 3, significando que chamadas de helpers aninhados tambem sao inlined.

### Como Funciona

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // Tanto ep0 QUANTO rotr sao inlined aqui
    // ...
}
```

Na profundidade 1, `ep0()` e inlined em `sha256_round()`. Na profundidade 2, as chamadas `rotr()` dentro de `ep0()` tambem sao inlined. O resultado e um unico bloco de aritmetica nativa sem overhead de chamada de funcao.

### Criterios de Inlining

Funcoes sao inlined quando:
- O corpo da funcao e pequeno (expressao unica ou poucas instrucoes)
- A funcao nao e recursiva
- A profundidade atual de inline e menor que 3

### Controlando Inlining com Anotacoes

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // Funcao complexa que nao deve ser duplicada
    return x;
}
```

---

## Unboxing de Acumulador em While-Loop

Para loops while de nivel superior, o compilador detecta variaveis de contador e acumulador e as substitui por variaveis C nativas locais, eliminando o overhead de boxing/unboxing a cada iteracao.

### O Que e Otimizado

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

O compilador detecta que `sum` e `i` sao acumuladores inteiros usados apenas dentro do loop, e gera variaveis `int32_t` nativas em vez de operacoes `HmlValue`. Isso elimina overhead de retain/release e dispatch de tipo a cada iteracao.

### Impacto na Performance

Melhorias de benchmark com essas otimizacoes (medidas em cargas de trabalho tipicas):

| Benchmark | Antes | Depois | Melhoria |
|-----------|-------|--------|----------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## Anotacoes Auxiliares

O compilador suporta 10 anotacoes de otimizacao que mapeiam para atributos GCC/Clang:

| Anotacao | Efeito |
|----------|--------|
| `@inline` | Incentiva inlining da funcao |
| `@noinline` | Impede inlining da funcao |
| `@hot` | Marca como frequentemente executada (predicao de branch) |
| `@cold` | Marca como raramente executada |
| `@pure` | Funcao sem efeitos colaterais (le estado externo) |
| `@const` | Funcao depende apenas dos argumentos (sem estado externo) |
| `@flatten` | Faz inline de todas as chamadas dentro da funcao |
| `@optimize(level)` | Nivel de otimizacao por funcao ("0"-"3", "s", "fast") |
| `@warn_unused` | Avisa se valor de retorno for ignorado |
| `@section(name)` | Coloca funcao em secao ELF personalizada |

### Exemplo

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // Funcao de hashing no caminho quente
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## Pools de Alocacao

O runtime usa pools de objetos pre-alocados para evitar overhead de `malloc`/`free` para objetos de curta duracao criados frequentemente:

| Pool | Slots | Descricao |
|------|-------|-----------|
| Pool de ambientes | 1024 | Ambientes de escopo de closure/funcao (ate 16 variaveis cada) |
| Pool de objetos | 512 | Objetos anonimos com ate 8 campos |
| Pool de funcoes | 512 | Structs de closure para funcoes capturadas |

Pools usam pilhas de lista livre para alocacao e desalocacao O(1). Quando um pool se esgota, o runtime recorre ao `malloc`. Objetos que ultrapassam seu slot de pool (ex.: um objeto ganhando um 9o campo) sao migrados transparentemente para armazenamento no heap.

### Parametros Emprestados do AST

Closures emprestam metadados de parametros diretamente do AST em vez de fazer copia profunda, eliminando aproximadamente 6 chamadas `malloc` + N `strdup` por criacao de closure. Hashes de nomes de parametros sao calculados preguicosamente e armazenados em cache no no do AST.

---

## Verificacao de Tipos

O compilador inclui verificacao de tipos em compile-time (habilitada por padrao):

```bash
hemlockc program.hml -o program       # Verifica tipos + compila
hemlockc --check program.hml          # Apenas verifica tipos
hemlockc --no-type-check program.hml  # Pula verificacao de tipos
hemlockc --strict-types program.hml   # Avisa sobre tipos 'any' implicitos
```

Codigo sem tipos e tratado como dinamico (tipo `any`) e sempre passa na verificacao de tipos. Anotacoes de tipo fornecem dicas de otimizacao que habilitam unboxing.

---

## Veja Tambem

- [Proposta de Anotacoes Auxiliares](../proposals/compiler-helper-annotations.md) - Referencia detalhada de anotacoes
- [API de Memoria](../reference/memory-api.md) - Operacoes de buffer e ponteiro
- [Funcoes](../language-guide/functions.md) - Anotacoes de tipo e funcoes com corpo de expressao
