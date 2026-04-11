# Proposta: `@stdlib/vector` — Modulo de Busca de Similaridade Vetorial

**Status:** Exploracao / RFC
**Data:** 2026-02-07

---

## Resumo

Adicionar um modulo `@stdlib/vector` fornecendo busca de similaridade vetorial em processo (busca de vizinhos mais proximos). Isso habilita busca baseada em embeddings, sistemas de recomendacao e fluxos de trabalho de IA/ML diretamente do Hemlock sem necessidade de um servidor externo.

---

## Opcoes Avaliadas

Dez opcoes de banco de dados / biblioteca vetorial foram avaliadas contra estes criterios:

| Criterio | Peso | Justificativa |
|----------|------|---------------|
| Qualidade da API C | Critico | FFI do Hemlock requer linkagem C (`extern fn`) para bibliotecas `.so` |
| Embutivel (em processo) | Critico | Modulos da stdlib do Hemlock sao bibliotecas, nao protocolos cliente-servidor |
| Peso de dependencias | Alto | Dependencias minimas preferidas (como sqlite -- apenas um `.so`) |
| Simplicidade da API | Alto | Hemlock valoriza APIs explicitas e pequenas |
| Performance | Medio | Bom o suficiente para 1M+ vetores; nao precisa escala de bilhoes |
| Persistencia | Medio | Salvar/carregar indices no disco |
| Licenca | Medio | Deve ser permissiva (Apache-2.0, MIT, BSD) |

### Resultados

| Opcao | API C | Embutivel | Deps | Performance | Veredicto |
|-------|-------|-----------|------|-------------|-----------|
| **USearch** | C99 primeira classe | Sim | Zero | HNSW + SIMD | **PRIMARIO** |
| **sqlite-vec** | Via SQL | Sim | Zero (C puro) | Forca bruta | **SECUNDARIO** |
| hnswlib | Apenas C++ | Sim | Zero | HNSW | Sem API C -- pular |
| FAISS | API C (faiss_c) | Sim | BLAS necessario | Estado da arte | Muito pesado |
| pgvector | N/A | Nao (precisa PG) | PostgreSQL | Bom | Servidor necessario -- pular |

---

## Recomendacao: USearch (primario) + sqlite-vec (alternativa leve)

### Por Que NAO pgvector

pgvector requer um servidor PostgreSQL em execucao. Os modulos stdlib do Hemlock sao bibliotecas embutiveis carregadas via FFI (`import "libfoo.so"`), nao protocolos cliente-servidor. Exigir que usuarios instalem, configurem e executem PostgreSQL para busca vetorial e fundamentalmente desalinhado com o padrao da stdlib.

### Primario: USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) e uma biblioteca de busca de similaridade vetorial open-source (Apache-2.0) com uma API C99 primeira classe. Usa o algoritmo HNSW (Hierarchical Navigable Small World) com otimizacao SIMD.

---

## Design de API Proposto (`@stdlib/vector`)

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Criar um indice
let idx = create_index(dimensions: 384, metric: "cosine");

// Adicionar vetores (chave + array de floats)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);

// Buscar k vizinhos mais proximos
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// retorna: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Persistencia
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Busca filtrada (com predicado)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;
});

// Informacoes
print(idx.size());       // numero de vetores
print(idx.dimensions()); // dimensionalidade
print(idx.contains(42)); // verificacao de pertinencia

// Limpeza
idx.remove(2);
idx.free();
```

### Exportacoes do Modulo

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // memory-mapped, somente leitura

VectorIndex.add(key, vector)
VectorIndex.search(query, k?)
VectorIndex.search_filtered(query, k?, filter)
VectorIndex.remove(key)
VectorIndex.contains(key)
VectorIndex.count()
VectorIndex.size()
VectorIndex.dimensions()
VectorIndex.save(path)
VectorIndex.free()

distance(a, b, metric?)  // calculo de distancia avulso

// Metricas de distancia
METRIC_COSINE
METRIC_L2SQ       // Euclidiana (L2 ao quadrado)
METRIC_IP          // Produto interno (produto escalar)
METRIC_HAMMING
METRIC_JACCARD

// Tipos escalares
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

---

## Plano de Implementacao

1. **Escrever bindings FFI** -- declaracoes `extern fn` para a API C do USearch (~20 funcoes)
2. **Implementar wrapper Hemlock** -- `create_index()`, `VectorIndex` define com metodos
3. **Tratar memoria** -- `alloc`/`free` correto para marshaling de dados vetoriais, limpeza de strings de erro
4. **Adicionar documentacao** -- `stdlib/docs/vector.md` seguindo padrao de sqlite.md
5. **Adicionar testes** -- `tests/stdlib_vector/` com CRUD basico, persistencia, precisao de busca
6. **Adicionar testes de paridade** -- Se suporte do compilador for necessario para padroes FFI usados

Escopo estimado: ~400-600 linhas de Hemlock (comparavel a `sqlite.hml` com 968 linhas, mas superficie de API mais simples).

---

## Questoes Abertas

1. **Nome do modulo:** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`?
2. **Integracao sqlite-vec:** Distribuir como parte de `@stdlib/sqlite` (carregamento de extensao) ou modulo separado?
3. **API de quantizacao:** Expor quantizacao int8/f16 do USearch, ou padronizar para f32 e manter simples?
4. **Operacoes em lote:** Adicionar `add_batch()` / `search_batch()` para operacoes em massa, ou manter API de item unico?
5. **Configuracao de indice:** Quanto da configuracao HNSW do USearch (conectividade, fatores de expansao) expor?
