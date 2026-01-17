# Empacotamento e Distribuição

Hemlock oferece ferramentas integradas para empacotar projetos multi-arquivo em um único arquivo distribuível e criar executáveis independentes.

## Visão Geral

| Comando | Saída | Caso de Uso |
|---------|-------|-------------|
| `--bundle` | `.hmlc` ou `.hmlb` | Distribuir bytecode (requer Hemlock instalado) |
| `--package` | executável | Binário independente (sem dependências) |
| `--compile` | `.hmlc` | Compilar arquivo único (sem resolução de imports) |

## Empacotamento (Bundle)

O empacotador resolve todas as declarações `import` a partir do ponto de entrada e as achata em um único arquivo.

### Uso Básico

```bash
# Empacotar app.hml e todos seus imports em app.hmlc
hemlock --bundle app.hml

# Especificar caminho de saída
hemlock --bundle app.hml -o dist/app.hmlc

# Criar pacote comprimido (.hmlb) - tamanho de arquivo menor
hemlock --bundle app.hml --compress -o app.hmlb

# Saída detalhada (mostra módulos resolvidos)
hemlock --bundle app.hml --verbose
```

### Formatos de Saída

**`.hmlc` (não comprimido)**
- Formato AST serializado
- Rápido para carregar e executar
- Formato de saída padrão

**`.hmlb` (comprimido)**
- `.hmlc` comprimido com zlib
- Tamanho de arquivo menor (tipicamente 50-70% de redução)
- Início ligeiramente mais lento devido à descompressão

### Executando Arquivos Empacotados

```bash
# Executar pacote não comprimido
hemlock app.hmlc

# Executar pacote comprimido
hemlock app.hmlb

# Passar argumentos
hemlock app.hmlc arg1 arg2
```

### Exemplo: Projeto Multi-módulo

```
myapp/
├── main.hml
├── lib/
│   ├── math.hml
│   └── utils.hml
└── config.hml
```

```hemlock
// main.hml
import { add, multiply } from "./lib/math.hml";
import { log } from "./lib/utils.hml";
import { VERSION } from "./config.hml";

log(`App v${VERSION}`);
print(add(2, 3));
```

```bash
hemlock --bundle myapp/main.hml -o myapp.hmlc
hemlock myapp.hmlc  # Executa com todas as dependências empacotadas
```

### Imports de stdlib

O empacotador resolve automaticamente imports `@stdlib/`:

```hemlock
import { HashMap } from "@stdlib/collections";
import { now } from "@stdlib/time";
```

Durante o empacotamento, módulos stdlib são incluídos na saída.

## Encapsulamento (Package)

O encapsulamento cria executáveis independentes incorporando o bytecode empacotado em uma cópia do interpretador Hemlock.

### Uso Básico

```bash
# Criar executável a partir de app.hml
hemlock --package app.hml

# Especificar nome de saída
hemlock --package app.hml -o myapp

# Pular compressão (início mais rápido, arquivo maior)
hemlock --package app.hml --no-compress

# Saída detalhada
hemlock --package app.hml --verbose
```

### Executando Executáveis Encapsulados

```bash
# Executáveis encapsulados rodam diretamente
./myapp

# Argumentos são passados para o script
./myapp arg1 arg2
```

### Formato do Pacote

Executáveis encapsulados usam o formato HMLP:

```
[binário hemlock][payload HMLB/HMLC][payload_size:u64][magic HMLP:u32]
```

Quando um executável encapsulado roda:
1. Verifica o final do arquivo para payload incorporado
2. Se encontrado, descomprime e executa o payload
3. Se não encontrado, executa como interpretador Hemlock normal

### Opções de Compressão

| Flag | Formato | Início | Tamanho |
|------|---------|--------|---------|
| (padrão) | HMLB | Normal | Menor |
| `--no-compress` | HMLC | Mais rápido | Maior |

Para ferramentas CLI onde tempo de início é importante, use `--no-compress`.

## Inspecionando Pacotes

Use `--info` para inspecionar arquivos compilados ou empacotados:

```bash
hemlock --info app.hmlc
```

Saída:
```
=== File Info: app.hmlc ===
Size: 12847 bytes
Format: HMLC (compiled AST)
Version: 1
Flags: 0x0001 [DEBUG]
Strings: 42
Statements: 156
```

```bash
hemlock --info app.hmlb
```

Saída:
```
=== File Info: app.hmlb ===
Size: 5234 bytes
Format: HMLB (compressed bundle)
Version: 1
Uncompressed: 12847 bytes
Compressed: 5224 bytes
Ratio: 59.3% reduction
```

## Compilação Nativa

Para executáveis verdadeiramente nativos (sem interpretador), use o compilador Hemlock:

```bash
# Compilar para executável nativo via C
hemlockc app.hml -o app

# Manter código C gerado
hemlockc app.hml -o app --keep-c

# Apenas gerar C (não compilar)
hemlockc app.hml -c -o app.c

# Níveis de otimização
hemlockc app.hml -o app -O2
```

O compilador gera código C e chama GCC para produzir um binário nativo. Isso requer:
- Biblioteca runtime Hemlock (`libhemlock_runtime`)
- Compilador C (GCC por padrão)

### Opções do Compilador

| Opção | Descrição |
|-------|-----------|
| `-o <file>` | Nome do arquivo executável de saída |
| `-c` | Apenas gerar código C |
| `--emit-c <file>` | Escrever C para arquivo especificado |
| `-k, --keep-c` | Manter C gerado após compilação |
| `-O<level>` | Nível de otimização (0-3) |
| `--cc <path>` | Compilador C a usar |
| `--runtime <path>` | Caminho para biblioteca runtime |
| `-v, --verbose` | Saída detalhada |

## Comparação

| Método | Portabilidade | Início | Tamanho | Dependências |
|--------|---------------|--------|---------|--------------|
| `.hml` | Apenas fonte | Tempo de parse | Mínimo | Hemlock |
| `.hmlc` | Apenas Hemlock | Rápido | Pequeno | Hemlock |
| `.hmlb` | Apenas Hemlock | Rápido | Menor | Hemlock |
| `--package` | Independente | Rápido | Maior | Nenhuma |
| `hemlockc` | Nativo | Mais rápido | Variável | Lib runtime |

## Melhores Práticas

1. **Desenvolvimento**: Executar arquivos `.hml` diretamente para iteração rápida
2. **Distribuição (com Hemlock)**: Empacotar com `--compress` para arquivos menores
3. **Distribuição (independente)**: Encapsular para deploy sem dependências
4. **Crítico para desempenho**: Usar `hemlockc` para compilação nativa

## Solução de Problemas

### "Cannot find stdlib"

O empacotador procura stdlib em:
1. `./stdlib` (relativo ao executável)
2. `../stdlib` (relativo ao executável)
3. `/usr/local/lib/hemlock/stdlib`

Certifique-se de que Hemlock está instalado corretamente ou execute do diretório fonte.

### Dependências Circulares

```
Error: Circular dependency detected when loading 'path/to/module.hml'
```

Refatore seus imports para quebrar o ciclo. Considere usar um módulo compartilhado para tipos comuns.

### Tamanho Grande do Pacote

- Use compressão padrão (não use `--no-compress`)
- Tamanho do pacote inclui interpretador completo (base ~500KB-1MB)
- Para tamanho mínimo, use `hemlockc` para compilação nativa
