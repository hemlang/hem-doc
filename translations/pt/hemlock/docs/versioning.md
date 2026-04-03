# Versionamento do Hemlock

Este documento descreve a estrategia de versionamento do Hemlock.

## Formato de Versao

O Hemlock utiliza o **Versionamento Semantico** (SemVer):

```
MAJOR.MINOR.PATCH
```

| Componente | Quando Incrementar |
|------------|-------------------|
| **MAJOR** | Mudancas incompativeis na semantica da linguagem, API da stdlib ou formatos binarios |
| **MINOR** | Novos recursos, adicoes retrocompativeis |
| **PATCH** | Correcoes de bugs, melhorias de desempenho, documentacao |

## Versionamento Unificado

Todos os componentes do Hemlock compartilham um **unico numero de versao**:

- **Interpretador** (`hemlock`)
- **Compilador** (`hemlockc`)
- **Servidor LSP** (`hemlock --lsp`)
- **Biblioteca Padrao** (`@stdlib/*`)

A versao e definida em `include/version.h`:

```c
#define HEMLOCK_VERSION_MAJOR 1
#define HEMLOCK_VERSION_MINOR 8
#define HEMLOCK_VERSION_PATCH 7

#define HEMLOCK_VERSION "1.8.7"
```

### Verificando Versoes

```bash
# Versao do interpretador
hemlock --version

# Versao do compilador
hemlockc --version
```

## Garantias de Compatibilidade

### Dentro de uma Versao MAJOR

- Codigo-fonte que funciona em `1.x.0` funcionara em `1.x.y` (qualquer patch)
- Codigo-fonte que funciona em `1.0.x` funcionara em `1.y.z` (qualquer minor/patch)
- Pacotes `.hmlb` compilados sao compativeis dentro da mesma versao MAJOR
- As APIs da biblioteca padrao sao estaveis (apenas adicoes, sem remocoes)

### Entre Versoes MAJOR

- Mudancas incompativeis sao documentadas nas notas de lancamento
- Guias de migracao sao fornecidos para mudancas significativas
- Recursos obsoletos sao sinalizados com aviso por pelo menos uma versao minor antes da remocao

## Versionamento de Formato Binario

O Hemlock utiliza numeros de versao separados para formatos binarios:

| Formato | Versao | Localizacao |
|---------|--------|-------------|
| `.hmlc` (pacote AST) | `HMLC_VERSION` | `include/ast_serialize.h` |
| `.hmlb` (pacote comprimido) | Mesmo que HMLC | Utiliza compressao zlib |
| `.hmlp` (executavel empacotado) | Magic: `HMLP` | Formato autocontido |

As versoes de formato binario sao incrementadas independentemente quando a serializacao muda.

## Versionamento da Biblioteca Padrao

A biblioteca padrao (`@stdlib/*`) e versionada **junto com o lancamento principal**:

```hemlock
// Sempre utiliza a stdlib empacotada com sua instalacao do Hemlock
import { HashMap } from "@stdlib/collections";
import { sin, cos } from "@stdlib/math";
```

### Compatibilidade da Stdlib

- Novos modulos podem ser adicionados em lancamentos MINOR
- Novas funcoes podem ser adicionadas a modulos existentes em lancamentos MINOR
- Assinaturas de funcoes sao estaveis dentro de uma versao MAJOR
- Funcoes obsoletas sao marcadas e documentadas antes da remocao

## Historico de Versoes

| Versao | Data | Destaques |
|--------|------|-----------|
| **1.8.7** | 2026 | Correcao do print/eprint com multiplos argumentos no codegen do compilador |
| **1.8.6** | 2026 | Correcao de segfault em hml_string_append_inplace para strings SSO |
| **1.8.5** | 2026 | 5 novos metodos de array (every, some, indexOf, sort, fill), grandes otimizacoes de desempenho, correcoes de vazamento de memoria |
| **1.8.4** | 2026 | Tratamento adequado de palavras reservadas (def, func, var, class), correcao de testes CI intermitentes |
| **1.8.3** | 2026 | Polimento de codigo: consolidacao de numeros magicos, padronizacao de mensagens de erro |
| **1.8.2** | 2026 | Prevencao de vazamento de memoria: eval seguro contra excecoes, limpeza de task/channel, correcoes do otimizador |
| **1.8.1** | 2026 | Correcao de bug de uso apos liberacao no tratamento de valor de retorno de funcao |
| **1.8.0** | 2026 | Pattern matching, alocador arena, correcoes de vazamento de memoria |
| **1.7.5** | 2026 | Correcao de bug de indentacao else-if no formatador |
| **1.7.4** | 2026 | Melhorias no formatador: quebra de linha em parametros de funcao, expressoes binarias, imports e encadeamento de metodos |
| **1.7.3** | 2026 | Correcao da preservacao de comentarios e linhas em branco no formatador |
| **1.7.2** | 2026 | Lancamento de manutencao |
| **1.7.1** | 2026 | Instrucoes if/while/for em linha unica (sintaxe sem chaves) |
| **1.7.0** | 2026 | Aliases de tipo, tipos de funcao, parametros const, assinaturas de metodo, rotulos de loop, argumentos nomeados, coalescencia nula |
| **1.6.7** | 2026 | Literais octais, comentarios de bloco, escapes hex/unicode, separadores numericos |
| **1.6.6** | 2026 | Literais float sem zero inicial, correcao de bug de reducao de forca |
| **1.6.5** | 2026 | Correcao da sintaxe de loop for-in sem palavra-chave 'let' |
| **1.6.4** | 2026 | Lancamento de correcao urgente |
| **1.6.3** | 2026 | Correcao do despacho de metodo em tempo de execucao para tipos file, channel, socket |
| **1.6.2** | 2026 | Lancamento de correcao |
| **1.6.1** | 2026 | Lancamento de correcao |
| **1.6.0** | 2025 | Verificacao de tipos em tempo de compilacao no hemlockc, integracao LSP, operadores compostos bit a bit (`&=`, `\|=`, `^=`, `<<=`, `>>=`, `%=`) |
| **1.5.0** | 2024 | Sistema de tipos completo, async/await, atomics, 39 modulos stdlib, suporte a struct FFI, 99 testes de paridade |
| **1.3.0** | 2025 | Escopo de bloco lexico adequado (semantica let/const estilo JS), closures por iteracao de loop |
| **1.2.3** | 2025 | Sintaxe import star (`import * from`) |
| **1.2.2** | 2025 | Suporte a `export extern`, correcoes de testes multiplataforma |
| **1.2.1** | 2025 | Correcao de falhas de teste no macOS (geracao de chave RSA, symlinks de diretorio) |
| **1.2.0** | 2025 | Otimizador AST, builtin apply(), canais sem buffer, 7 novos modulos stdlib, 97 testes de paridade |
| **1.1.3** | 2025 | Atualizacoes de documentacao, correcoes de consistencia |
| **1.1.1** | 2025 | Correcoes de bugs e melhorias |
| **1.1.0** | 2024 | Versionamento unificado em todos os componentes |
| **1.0.x** | 2024 | Serie de lancamento inicial |

## Processo de Lancamento

1. Atualizacao de versao em `include/version.h`
2. Atualizacao do changelog
3. Execucao da suite completa de testes (`make test-all`)
4. Tag do lancamento no git
5. Construcao dos artefatos de lancamento

## Verificando Compatibilidade

Para verificar se seu codigo funciona com uma versao especifica do Hemlock:

```bash
# Executar testes contra a versao instalada
make test

# Verificar paridade entre interpretador e compilador
make parity
```

## Futuro: Manifestos de Projeto

Um lancamento futuro podera introduzir manifestos de projeto opcionais para restricoes de versao:

```hemlock
// Hipotetico project.hml
define Project {
    name: "my-app",
    version: "1.0.0",
    hemlock: ">=1.1.0"
}
```

Isto ainda nao esta implementado, mas faz parte do roteiro.
