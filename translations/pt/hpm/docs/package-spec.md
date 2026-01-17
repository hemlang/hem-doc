# Especificacao de Pacotes

Referencia completa do formato do arquivo `package.json`.

## Visao Geral

Todo pacote hpm requer um arquivo `package.json` na raiz do projeto. Este arquivo define metadados do pacote, dependencias e scripts.

## Exemplo Minimo

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Exemplo Completo

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

## Referencia de Campos

### name (obrigatorio)

Nome do pacote no formato `owner/repo`.

```json
{
  "name": "hemlang/sprout"
}
```

**Requisitos:**
- Deve estar no formato `owner/repo`
- `owner` deve ser seu nome de usuario ou organizacao do GitHub
- `repo` deve ser o nome do repositorio
- Use letras minusculas, numeros e hifens
- Maximo de 214 caracteres no total

**Nomes validos:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Nomes invalidos:**
```
my-package          # Falta owner
hemlang/My_Package  # Maiusculas e underscores
hemlang             # Falta repo
```

### version (obrigatorio)

Versao do pacote seguindo [Versionamento Semantico](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Formato:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Versoes validas:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Descricao curta do pacote.

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- Mantenha abaixo de 200 caracteres
- Descreva o que o pacote faz, nao como

### author

Informacoes do autor do pacote.

```json
{
  "author": "Your Name <email@example.com>"
}
```

**Formatos aceitos:**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

Identificador da licenca.

```json
{
  "license": "MIT"
}
```

**Licencas comuns:**
- `MIT` - Licenca MIT
- `Apache-2.0` - Licenca Apache 2.0
- `GPL-3.0` - GNU General Public License v3.0
- `BSD-3-Clause` - Licenca BSD 3-Clause
- `ISC` - Licenca ISC
- `UNLICENSED` - Proprietario/privado

Use [identificadores SPDX](https://spdx.org/licenses/) quando possivel.

### repository

Link para o repositorio fonte.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

URL da pagina inicial do projeto.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

URL do rastreador de issues.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Arquivo de ponto de entrada do pacote.

```json
{
  "main": "src/index.hml"
}
```

**Padrao:** `src/index.hml`

Quando usuarios importam seu pacote:
```hemlock
import { x } from "owner/repo";
```

O hpm carrega o arquivo especificado em `main`.

**Ordem de resolucao de imports:**
1. Caminho exato: `src/index.hml`
2. Com extensao .hml: `src/index` → `src/index.hml`
3. Arquivo index: `src/index/` → `src/index/index.hml`

### keywords

Array de palavras-chave para descoberta.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Use minusculas
- Seja especifico e relevante
- Inclua a linguagem ("hemlock") se apropriado

### dependencies

Dependencias de tempo de execucao necessarias para o pacote funcionar.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Chave:** Nome do pacote (`owner/repo`)
**Valor:** Restricao de versao

**Sintaxe de restricao de versao:**

| Restricao | Significado |
|-----------|-------------|
| `1.2.3` | Versao exata |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Pelo menos 1.0.0 |
| `>=1.0.0 <2.0.0` | Intervalo |
| `*` | Qualquer versao |

### devDependencies

Dependencias apenas para desenvolvimento (testes, build, etc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Dependencias de desenvolvimento sao:
- Instaladas durante o desenvolvimento
- Nao instaladas quando o pacote e usado como dependencia
- Usadas para testes, build, linting, etc.

### scripts

Comandos nomeados que podem ser executados com `hpm run`.

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

**Executando scripts:**
```bash
hpm run start
hpm run build
hpm test        # Atalho para 'hpm run test'
```

**Passando argumentos:**
```bash
hpm run test -- --verbose --filter=unit
```

**Scripts comuns:**

| Script | Proposito |
|--------|-----------|
| `start` | Iniciar a aplicacao |
| `dev` | Modo de desenvolvimento com hot reload |
| `test` | Executar testes |
| `build` | Compilar para producao |
| `clean` | Remover artefatos de build |
| `lint` | Verificar estilo de codigo |
| `format` | Formatar codigo |

### files

Arquivos e diretorios a incluir quando o pacote e instalado.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Comportamento padrao:** Se nao especificado, inclui:
- Todos os arquivos no repositorio
- Exclui `.git/`, `node_modules/`, `hem_modules/`

**Usado para:**
- Reduzir tamanho do pacote
- Excluir arquivos de teste da distribuicao
- Incluir apenas arquivos necessarios

### native

Requisitos de bibliotecas nativas.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Documenta dependencias nativas que devem estar instaladas no sistema.

## Validacao

O hpm valida package.json durante varias operacoes. Erros comuns de validacao:

### Campo obrigatorio ausente

```
Error: package.json missing required field: name
```

**Correcao:** Adicionar campo obrigatorio.

### Formato de nome invalido

```
Error: Invalid package name. Must be in owner/repo format.
```

**Correcao:** Usar formato `owner/repo`.

### Versao invalida

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Correcao:** Usar formato semver completo (`1.0.0`).

### JSON invalido

```
Error: package.json is not valid JSON
```

**Correcao:** Verificar sintaxe JSON (virgulas, aspas, chaves).

## Criando package.json

### Interativo

```bash
hpm init
```

Solicita interativamente cada campo.

### Com valores padrao

```bash
hpm init --yes
```

Cria com valores padrao:
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Manual

Criar arquivo manualmente:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Melhores Praticas

1. **Sempre especifique main** - Nao dependa do padrao
2. **Use intervalos de circunflexo** - `^1.0.0` para a maioria das dependencias
3. **Separe dependencias de desenvolvimento** - Coloque dependencias de teste/build em devDependencies
4. **Inclua palavras-chave** - Ajude usuarios a encontrar seu pacote
5. **Documente scripts** - Nomeie scripts claramente
6. **Especifique licenca** - Obrigatorio para projetos open source
7. **Adicione descricao** - Ajude usuarios a entender o proposito

## Veja Tambem

- [Criacao de Pacotes](creating-packages.md) - Guia de publicacao
- [Versionamento](versioning.md) - Restricoes de versao
- [Configuracao do Projeto](project-setup.md) - Estrutura do projeto
