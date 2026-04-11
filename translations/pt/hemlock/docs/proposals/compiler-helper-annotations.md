# Anotacoes Auxiliares do Compilador: Analise e Proposta

**Autor:** Claude
**Data:** 2026-01-08
**Status:** Parcialmente Implementado (Fases 1-2 concluidas na v1.9.0; Fases 3-5 permanecem como propostas)
**Relacionado:** Issue #TBD

## Indice

1. [Resumo Executivo](#resumo-executivo)
2. [Analise do Estado Atual](#analise-do-estado-atual)
3. [Anotacoes Propostas](#anotacoes-propostas)
4. [Plano de Implementacao](#plano-de-implementacao)
5. [Exemplos](#exemplos)
6. [Estrategia de Testes](#estrategia-de-testes)
7. [Consideracoes Futuras](#consideracoes-futuras)

---

## Resumo Executivo

O sistema de anotacoes do Hemlock fornece uma base robusta para adicionar dicas e diretivas do compilador. Esta proposta estende a infraestrutura de anotacoes atual com **15 novas anotacoes auxiliares do compilador** organizadas em cinco categorias:

- **Dicas de Otimizacao** (7 anotacoes)
- **Gerenciamento de Memoria** (3 anotacoes)
- **Controle de Geracao de Codigo** (2 anotacoes)
- **Verificacao de Erros** (2 anotacoes)
- **FFI/Interop** (1 anotacao)

Essas anotacoes permitirao que desenvolvedores fornecam orientacao explicita ao compilador (`hemlockc`) mantendo compatibilidade retroativa com o interpretador.

---

## Analise do Estado Atual

### Anotacoes Atualmente Implementadas

```c
// Anotacoes de seguranca (para verificador de memoria Tricycle)
@safe       // Funcao e segura em memoria
@unsafe     // Funcao contem operacoes inseguras
@trusted    // Funcao e confiavel apesar de operacoes inseguras

// Dicas de otimizacao do compilador (IMPLEMENTADAS na v1.9.0)
@inline     // Sugere inlining desta funcao
@noinline   // Impede inlining desta funcao
@cold       // Funcao raramente executada
@hot        // Funcao frequentemente executada
@pure       // Funcao sem efeitos colaterais

// Outras anotacoes
@deprecated      // Marca como obsoleto com mensagem opcional
@test, @skip     // Anotacoes do framework de testes
@author, @since  // Anotacoes de documentacao
```

**Atualizacao (v1.9.0):** As anotacoes de nivel de funcao (`@inline`, `@noinline`, `@hot`, `@cold`, `@pure`, `@const`, `@flatten`, `@optimize`, `@warn_unused`, `@section`) estao totalmente implementadas no backend do compilador. As propostas restantes (anotacoes de loop, anotacoes de memoria) nas Fases 3-5 abaixo ainda nao estao implementadas.

---

## Anotacoes Propostas

### Categoria 1: Dicas de Otimizacao

- **`@unroll(count?)`** - Sugere desenrolamento de loop
- **`@simd` / `@nosimd`** - Habilita ou desabilita vetorizacao SIMD
- **`@likely` / `@unlikely`** - Dicas de predicao de branch
- **`@const`** - Funcao depende apenas dos argumentos (mais forte que `@pure`)
- **`@tail_call`** - Solicita otimizacao de chamada de cauda
- **`@flatten`** - Faz inline de todas as chamadas dentro da funcao
- **`@optimize(level)`** - Nivel de otimizacao por funcao

### Categoria 2: Gerenciamento de Memoria

- **`@stack`** - Aloca na pilha em vez do heap
- **`@noalias`** - Ponteiro nao faz alias com outros ponteiros
- **`@aligned(bytes)`** - Especifica requisitos de alinhamento de memoria

### Categoria 3: Controle de Geracao de Codigo

- **`@extern(name?, abi?)`** - Marca funcao para linkagem externa ou exportacao FFI
- **`@section(name)`** - Coloca simbolo em secao ELF/Mach-O especifica

### Categoria 4: Verificacao de Erros

- **`@bounds_check` / `@no_bounds_check`** - Sobrescreve politica global de verificacao de limites
- **`@warn_unused`** - Avisa se valor de retorno for ignorado

### Categoria 5: FFI/Interop

- **`@packed`** - Cria struct empacotada sem preenchimento (para interop com C)

---

## Tabela de Referencia Completa de Anotacoes

| Anotacao | Alvo | Args | Descricao | Atributo C |
|----------|------|------|-----------|------------|
| `@inline` | fn | 0 | Forca inlining | `always_inline` |
| `@noinline` | fn | 0 | Impede inlining | `noinline` |
| `@cold` | fn | 0 | Raramente executada | `cold` |
| `@hot` | fn | 0 | Frequentemente executada | `hot` |
| `@pure` | fn | 0 | Sem efeitos colaterais, pode ler globais | `pure` |
| `@const` | fn | 0 | Sem efeitos colaterais, sem leitura de globais | `const` |
| `@flatten` | fn | 0 | Inline todas as chamadas dentro da funcao | `flatten` |
| `@tail_call` | fn | 0 | Solicita otimizacao de chamada de cauda | Customizado |
| `@optimize(level)` | fn | 1 | Sobrescreve nivel de otimizacao | `optimize("OX")` |
| `@unroll(factor?)` | loop | 0-1 | Dica de desenrolamento de loop | `#pragma unroll` |
| `@simd` | fn, loop | 0 | Habilita vetorizacao SIMD | `#pragma omp simd` |
| `@nosimd` | fn, loop | 0 | Desabilita SIMD | Customizado |
| `@likely` | if | 0 | Branch provavelmente tomado | `__builtin_expect` |
| `@unlikely` | if | 0 | Branch improvavel | `__builtin_expect` |
| `@stack` | let | 0 | Alocacao na pilha | Customizado |
| `@noalias` | param | 0 | Sem aliasing de ponteiro | `noalias` |
| `@aligned(N)` | let, fn | 1 | Alinhamento de memoria | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | Linkagem externa | `extern "C"` |
| `@section(name)` | fn, let | 1 | Coloca em secao especifica | `section("X")` |
| `@bounds_check` | fn | 0 | Forca verificacao de limites | Customizado |
| `@no_bounds_check` | fn | 0 | Desabilita verificacao de limites | Customizado |
| `@warn_unused` | fn | 0 | Avisa sobre retorno nao utilizado | `warn_unused_result` |
| `@packed` | define | 0 | Sem preenchimento em struct | `packed` |

---

## Conclusao

Esta proposta adiciona **15 novas anotacoes auxiliares do compilador** ao Hemlock, permitindo que desenvolvedores fornecam dicas de otimizacao explicitas mantendo a filosofia de "explicito sobre implicito" da linguagem.

**Beneficios Principais:**

1. **Performance:** Speedups de 2-10x para caminhos criticos com SIMD, desenrolamento, inlining
2. **Controle:** Desenvolvedores podem sobrescrever heuristicas padrao do compilador
3. **Interop:** Melhor suporte FFI com @extern, @packed, @aligned
4. **Seguranca:** @bounds_check/@no_bounds_check explicito torna trocas de seguranca visiveis
5. **Explicito:** Se encaixa na filosofia do Hemlock - sem magia, apenas diretivas claras
