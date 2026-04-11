# Plano de Prevencao de Vazamento de Memoria

> Garantindo que o runtime Hemlock seja livre de vazamentos de memoria e cumpra seu contrato com o programador.

**Data:** 2026-01-16
**Status:** Concluido (implementado na v1.8.3)
**Versao:** 1.0

---

## Resumo Executivo

A filosofia de design do Hemlock afirma: *"Nos fornecemos as ferramentas para ser seguro, mas nao forcamos voce a usa-las."* Isso significa que o **runtime em si** deve ser livre de vazamentos, mesmo quando o codigo do usuario utiliza recursos inseguros. O contrato do programador e:

1. **Alocacoes do usuario** (`alloc`, `buffer`) sao responsabilidade do programador liberar com `free`
2. **Alocacoes internas do runtime** (strings, arrays, objetos, closures) sao gerenciadas automaticamente via contagem de referencias
3. **Erros e excecoes** nao devem vazar memoria
4. **Tarefas assincronas** tem semanticas de ownership claras
5. **O runtime nunca esconde alocacoes** do programador

Este plano identifica lacunas na infraestrutura atual e propoe melhorias sistematicas.

---

## Indice

1. [Avaliacao do Estado Atual](#avaliacao-do-estado-atual)
2. [Lacunas Identificadas](#lacunas-identificadas)
3. [Melhorias Propostas](#melhorias-propostas)
4. [Estrategia de Testes](#estrategia-de-testes)
5. [Requisitos de Documentacao](#requisitos-de-documentacao)
6. [Fases de Implementacao](#fases-de-implementacao)
7. [Criterios de Sucesso](#criterios-de-sucesso)

---

## Avaliacao do Estado Atual

### Pontos Fortes

| Componente | Implementacao | Localizacao |
|------------|---------------|-------------|
| Contagem de referencias | Ops atomicas com `__ATOMIC_SEQ_CST` | `src/backends/interpreter/values.c:413-550` |
| Deteccao de ciclos | VisitedSet para travessia de grafo | `src/backends/interpreter/values.c:1345-1480` |
| Isolamento de threads | Copia profunda no spawn | `src/backends/interpreter/values.c:1687-1859` |
| Profiler com deteccao de vazamentos | Rastreamento de AllocSite | `src/backends/interpreter/profiler/` |
| Integracao ASAN | Pipeline de CI com deteccao de vazamentos | `.github/workflows/tests.yml` |
| Suporte Valgrind | Multiplos targets no Makefile | `Makefile:189-327` |
| Script de testes abrangente | Testes baseados em categorias | `tests/leak_check.sh` |

### Modelo Atual de Ownership de Memoria

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILIDADE DO PROGRAMADOR               │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  aritmetica de ptr ──────────────────────────►  seguranca       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILIDADE DO RUNTIME                   │
├─────────────────────────────────────────────────────────────────┤
│  Literais/operacoes de string ───────► refcount + auto-release  │
│  Literais/operacoes de array ────────► refcount + auto-release  │
│  Literais/operacoes de objeto ───────► refcount + auto-release  │
│  Closures de funcao ─────────────────► refcount + env release   │
│  Resultados de tarefa ───────────────► liberados apos join()    │
│  Buffers de canal ───────────────────► liberados no close()     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lacunas Identificadas

### Lacuna 1: Limpeza em Caminhos de Erro (ALTA PRIORIDADE)

**Problema:** Quando excecoes ocorrem no meio da execucao, temporarios alocados podem vazar.

**Cenario de Exemplo:**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // Array alocado
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // Excecao lancada
        return x * 2;
    });
    // 'transformed' parcialmente alocado, 'arr' pode nao ser liberado
}
```

### Lacuna 2: Ownership de Resultado de Tarefa Desanexada (MEDIA PRIORIDADE)

**Problema:** `detach(task)` permite execucao fire-and-forget, mas o resultado da tarefa pode nunca ser coletado.

### Lacuna 3: Semantica de Close vs. Drenagem de Canal (MEDIA PRIORIDADE)

**Problema:** Quando um canal e fechado com valores no buffer restantes, esses valores sao liberados corretamente?

### Lacuna 4: Vazamento de AST de Coalescencia Nula (CORRIGIDO)

**Problema:** O otimizador otimizava expressoes de coalescencia nula quando o resultado era conhecido em compile-time, mas nao liberava os nos AST descartados.

### Lacuna 5: Granularidade da Lista de Captura de Closures (BAIXA PRIORIDADE)

**Problema:** Closures capturam a cadeia de ambiente inteira em vez de apenas variaveis referenciadas, potencialmente estendendo tempos de vida desnecessariamente.

### Lacuna 6: Referencia Ciclica em Coordenacao Assincrona (BAIXA PRIORIDADE)

**Problema:** Tarefas referenciando canais que referenciam tarefas podem criar ciclos.

### Lacuna 7: Documentacao de Fronteira de Memoria FFI (DOCUMENTACAO)

**Problema:** Transferencia de ownership atraves da fronteira FFI nao e formalmente documentada.

---

## Melhorias Propostas

### Fase 1: Correcoes Criticas (Semanas 1-2)

#### 1.1 Avaliacao de Expressao Segura contra Excecoes

**Abordagem:** Implementar uma "pilha de valores temporarios" que rastreia alocacoes durante avaliacao de expressoes.

#### 1.2 Limpeza de Resultado de Tarefa Desanexada

**Abordagem:** Tarefas desanexadas liberam seu proprio resultado quando completam.

#### 1.3 Drenagem de Canal no Close

**Abordagem:** `channel_close()` e `channel_free()` devem drenar valores restantes.

### Fase 2: Correcoes de Problemas Conhecidos (Semanas 3-4)

#### 2.1 Correcao de AST de Coalescencia Nula

#### 2.2 Otimizacao de Captura de Closures (Opcional)

### Fase 3: Fortalecimento da Infraestrutura de Testes (Semanas 5-6)

#### 3.1 Suite de Regressao de Vazamentos

#### 3.2 Monitoramento Continuo de Vazamentos

#### 3.3 Testes Fuzz para Seguranca de Memoria

### Fase 4: Documentacao e Contrato (Semana 7)

#### 4.1 Documentacao de Ownership de Memoria

---

## Estrategia de Testes

### Categorias de Teste

| Categoria | Descricao | Ferramenta |
|-----------|-----------|------------|
| Unitario | Testes individuais de vazamento de funcao | ASAN |
| Integracao | Cenarios multi-componente | ASAN + Valgrind |
| Estresse | Ciclos de alocacao/liberacao de alto volume | ASAN (leak-check=no) |
| Fuzz | Seguranca de memoria com entrada aleatoria | libFuzzer + ASAN |
| Regressao | Cenarios de vazamentos ja corrigidos | ASAN + baseline |

---

## Fases de Implementacao

| Fase | Foco | Duracao | Prioridade |
|------|------|---------|------------|
| 1 | Correcoes criticas (excecao, detach, canal) | 2 semanas | ALTA |
| 2 | Correcoes de problemas conhecidos (null coalesce, capturas) | 2 semanas | MEDIA |
| 3 | Infraestrutura de testes | 2 semanas | ALTA |
| 4 | Documentacao | 1 semana | MEDIA |

---

## Criterios de Sucesso

### Quantitativos

- [ ] Zero vazamentos reportados pelo ASAN na suite de testes completa
- [ ] Zero vazamentos reportados pelo Valgrind na suite de testes completa
- [ ] Baseline de vazamentos estabelecido e aplicado no CI
- [ ] 100% das lacunas identificadas tratadas ou documentadas como aceitaveis

### Qualitativos

- [ ] Ownership de memoria documentado em `docs/advanced/memory-ownership.md`
- [ ] Regras de ownership FFI documentadas
- [ ] Teste de regressao para cada vazamento corrigido
- [ ] Testes fuzz integrados ao CI

### Verificacao do Contrato do Runtime

As seguintes garantias devem ser mantidas apos a implementacao:

1. **Sem vazamento em execucao normal**: Executar qualquer programa valido e sair normalmente nao vaza memoria (interna do runtime).
2. **Sem vazamento em excecao**: Lancar e capturar excecoes nao vaza memoria.
3. **Sem vazamento na conclusao de tarefa**: Tarefas concluidas (unidas ou desanexadas) nao vazam memoria.
4. **Sem vazamento no fechamento de canal**: Fechar canais libera todos os valores no buffer.
5. **Limpeza deterministica**: A ordem das chamadas de destrutor e previsivel (LIFO para defer, topologica para objetos).

---

## Referencias

- Profiler atual: `src/backends/interpreter/profiler/profiler.c`
- Contagem de referencias: `src/backends/interpreter/values.c:413-550`
- Gerenciamento de tarefas: `src/backends/interpreter/builtins/concurrency.c`
- Documentacao ASAN: https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck: https://valgrind.org/docs/manual/mc-manual.html
