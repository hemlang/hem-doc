# Perfilamento

Hemlock inclui um profiler integrado para **análise de tempo de CPU**, **rastreamento de memória** e **detecção de vazamentos**. O profiler ajuda a identificar gargalos de desempenho e problemas de memória em seus programas.

## Índice

- [Visão Geral](#visão-geral)
- [Início Rápido](#início-rápido)
- [Modos de Perfilamento](#modos-de-perfilamento)
- [Formatos de Saída](#formatos-de-saída)
- [Detecção de Vazamentos](#detecção-de-vazamentos)
- [Entendendo os Relatórios](#entendendo-os-relatórios)
- [Geração de Flamegraph](#geração-de-flamegraph)
- [Melhores Práticas](#melhores-práticas)

---

## Visão Geral

O profiler é acessado através do subcomando `profile`:

```bash
hemlock profile [OPTIONS] <FILE>
```

**Recursos Principais:**
- **Perfilamento de CPU** - mede tempo gasto em cada função (self time e total time)
- **Perfilamento de Memória** - rastreia todas as alocações e suas localizações de origem
- **Detecção de Vazamentos** - identifica memória que nunca foi liberada
- **Múltiplos Formatos de Saída** - texto, JSON e saída compatível com flamegraph
- **Estatísticas de Memória por Função** - veja quais funções alocam mais memória

---

## Início Rápido

### Perfilar Tempo de CPU (Padrão)

```bash
hemlock profile script.hml
```

### Perfilar Alocações de Memória

```bash
hemlock profile --memory script.hml
```

### Detectar Vazamentos de Memória

```bash
hemlock profile --leaks script.hml
```

### Gerar Dados de Flamegraph

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## Modos de Perfilamento

### Perfilamento de CPU (Padrão)

Mede tempo gasto em cada função, distinguindo:
- **Self time** - tempo gasto executando o código da própria função
- **Total time** - self time mais tempo gasto em funções chamadas

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # Explícito
```

**Saída de Exemplo:**
```
=== Hemlock Profiler Report ===

Total time: 1.234ms
Functions called: 5 unique

--- Top 5 by Self Time ---

Function                        Self      Total   Calls
--------                        ----      -----   -----
expensive_calc              0.892ms    0.892ms     100  (72.3%)
process_data                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### Perfilamento de Memória

Rastreia todas as alocações de memória (`alloc`, `buffer`, `talloc`, `realloc`) e suas localizações de origem.

```bash
hemlock profile --memory script.hml
```

**Saída de Exemplo:**
```
=== Hemlock Profiler Report ===

Total time: 0.543ms
Functions called: 3 unique
Total allocations: 15 (4.2KB)

--- Top 3 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
allocator                   0.312ms    0.312ms      10      3.2KB         10  (57.5%)
buffer_ops                  0.156ms    0.156ms       5       1KB          5  (28.7%)
main                        0.075ms    0.543ms       1        0B          0  (13.8%)

--- Top 10 Allocation Sites ---

Location                                      Total    Count
--------                                      -----    -----
src/data.hml:42                               1.5KB        5
src/data.hml:67                               1.0KB       10
src/main.hml:15                               512B         1
```

---

### Modo de Contagem de Chamadas

Modo de overhead mínimo que apenas conta chamadas de função (sem cronometragem).

```bash
hemlock profile --calls script.hml
```

---

## Formatos de Saída

### Texto (Padrão)

Resumo legível por humanos com tabelas.

```bash
hemlock profile script.hml
```

---

### JSON

Formato legível por máquina para integração com outras ferramentas.

```bash
hemlock profile --json script.hml
```

**Saída de Exemplo:**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "expensive_calc",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### Flamegraph

Gera formato de stack colapsado compatível com [flamegraph.pl](https://github.com/brendangregg/FlameGraph).

```bash
hemlock profile --flamegraph script.hml > profile.folded

# Gerar SVG usando flamegraph.pl
flamegraph.pl profile.folded > profile.svg
```

**Saída Colapsada de Exemplo:**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## Detecção de Vazamentos

A flag `--leaks` mostra apenas alocações que nunca foram liberadas, facilitando a identificação de vazamentos de memória.

```bash
hemlock profile --leaks script.hml
```

**Programa de Exemplo com Vazamentos:**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // Vazamento - nunca liberado
    let p2 = alloc(200);    // OK - liberado abaixo
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // Liberado corretamente
}

leaky();
clean();
```

**Saída com --leaks:**
```
=== Hemlock Profiler Report ===

Total time: 0.034ms
Functions called: 2 unique
Total allocations: 3 (388B)

--- Top 2 by Self Time ---

Function                        Self      Total   Calls      Alloc      Count
--------                        ----      -----   -----      -----      -----
leaky                       0.021ms    0.021ms       1       300B          2  (61.8%)
clean                       0.013ms    0.013ms       1        88B          1  (38.2%)

--- Memory Leaks (1 site) ---

Location                                     Leaked      Total    Count
--------                                     ------      -----    -----
script.hml:2                                   100B       100B        1
```

O relatório de vazamentos mostra:
- **Leaked** - bytes atualmente não liberados na saída do programa
- **Total** - total de bytes alocados nesta localização
- **Count** - número de alocações nesta localização

---

## Entendendo os Relatórios

### Estatísticas de Função

| Coluna | Descrição |
|--------|-----------|
| Function | Nome da função |
| Self | Tempo gasto na função (excluindo chamadas) |
| Total | Tempo incluindo todas as funções chamadas |
| Calls | Número de vezes que a função foi chamada |
| Alloc | Total de bytes alocados por esta função |
| Count | Número de alocações por esta função |
| (%) | Porcentagem do tempo total do programa |

### Sites de Alocação

| Coluna | Descrição |
|--------|-----------|
| Location | Arquivo fonte e número da linha |
| Total | Total de bytes alocados nesta localização |
| Count | Número de alocações |
| Leaked | Bytes ainda alocados na saída do programa (apenas --leaks) |

### Unidades de Tempo

O profiler escolhe automaticamente unidades apropriadas:
- `ns` - nanosegundos (< 1 microssegundo)
- `us` - microssegundos (< 1 milissegundo)
- `ms` - milissegundos (< 1 segundo)
- `s` - segundos

---

## Referência de Comandos

```
hemlock profile [OPTIONS] <FILE>

OPTIONS:
    --cpu           Perfilamento de CPU/tempo (padrão)
    --memory        Perfilamento de alocação de memória
    --calls         Apenas contagem de chamadas (overhead mínimo)
    --leaks         Mostrar apenas alocações não liberadas (implica --memory)
    --json          Saída em formato JSON
    --flamegraph    Saída em formato compatível com flamegraph
    --top N         Mostrar top N entradas (padrão: 20)
```

---

## Geração de Flamegraph

Flamegraphs visualizam onde seu programa gasta tempo, com barras mais largas representando mais tempo.

### Gerando um Flamegraph

1. Instalar flamegraph.pl:
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. Perfilar seu programa:
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. Gerar SVG:
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. Abrir `profile.svg` em um navegador para visualização interativa.

### Lendo Flamegraphs

- **Eixo X**: Porcentagem do tempo total (largura = proporção do tempo)
- **Eixo Y**: Profundidade da call stack (fundo = ponto de entrada, topo = funções folha)
- **Cores**: Aleatórias, apenas para distinção visual
- **Clique**: Zoom em uma função para ver suas chamadas

---

## Melhores Práticas

### 1. Perfile Cargas de Trabalho Representativas

Use dados e padrões de uso reais para perfilar. Casos de teste pequenos podem não revelar os verdadeiros gargalos.

```bash
# Bom: perfilar com dados semelhantes a produção
hemlock profile --memory process_large_file.hml large_input.txt

# Menos útil: casos de teste minúsculos
hemlock profile quick_test.hml
```

### 2. Use --leaks Durante o Desenvolvimento

Execute detecção de vazamentos regularmente para encontrar vazamentos de memória cedo:

```bash
hemlock profile --leaks my_program.hml
```

### 3. Compare Antes e Depois das Otimizações

Perfile antes e depois de otimizações para medir o impacto:

```bash
# Antes
hemlock profile --json script.hml > before.json

# Depois
hemlock profile --json script.hml > after.json

# Comparar resultados
```

### 4. Use --top para Programas Grandes

Limite a saída para focar nas funções mais importantes:

```bash
hemlock profile --top 10 large_program.hml
```

### 5. Combine com Flamegraphs

Para padrões de chamada complexos, flamegraphs fornecem melhor visualização do que saída de texto:

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## Overhead do Profiler

O profiler adiciona algum overhead à execução do programa:

| Modo | Overhead | Caso de Uso |
|------|----------|-------------|
| `--calls` | Mínimo | Apenas contagem de chamadas de função |
| `--cpu` | Baixo | Perfilamento de desempenho geral |
| `--memory` | Moderado | Análise de memória e detecção de vazamentos |

Para resultados mais precisos, perfile múltiplas vezes e procure padrões consistentes.

---

## Veja Também

- [Gerenciamento de Memória](../language-guide/memory.md) - Ponteiros e buffers
- [API de Memória](../reference/memory-api.md) - Funções alloc, free, buffer
- [Assincronismo/Concorrência](async-concurrency.md) - Perfilando código assíncrono
