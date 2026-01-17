# Referencia de Comandos

Referencia completa de todos os comandos do hpm.

## Opcoes Globais

Estas opcoes se aplicam a qualquer comando:

| Opcao | Descricao |
|-------|-----------|
| `--help`, `-h` | Mostrar informacoes de ajuda |
| `--version`, `-v` | Mostrar versao do hpm |
| `--verbose` | Mostrar saida detalhada |

## Comandos

### hpm init

Cria um novo arquivo `package.json`.

```bash
hpm init        # Modo interativo
hpm init --yes  # Aceitar todos os valores padrao
hpm init -y     # Forma abreviada
```

**Opcoes:**

| Opcao | Descricao |
|-------|-----------|
| `--yes`, `-y` | Aceitar valores padrao para todos os prompts |

**Prompts Interativos:**
- Nome do pacote (formato owner/repo)
- Versao (padrao: 1.0.0)
- Descricao
- Autor
- Licenca (padrao: MIT)
- Arquivo principal (padrao: src/index.hml)

**Exemplo:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Instala dependencias ou adiciona novos pacotes.

```bash
hpm install                           # Instalar todas as dependencias do package.json
hpm install owner/repo                # Adicionar e instalar pacote
hpm install owner/repo@^1.0.0        # Com restricao de versao
hpm install owner/repo --dev         # Como dependencia de desenvolvimento
hpm i owner/repo                      # Forma abreviada
```

**Opcoes:**

| Opcao | Descricao |
|-------|-----------|
| `--dev`, `-D` | Adicionar a devDependencies |
| `--verbose` | Mostrar progresso detalhado |
| `--dry-run` | Visualizar sem instalar |
| `--offline` | Instalar apenas do cache (sem rede) |
| `--parallel` | Habilitar downloads paralelos (experimental) |

**Sintaxe de Restricao de Versao:**

| Sintaxe | Exemplo | Significado |
|---------|---------|-------------|
| (nenhuma) | `owner/repo` | Versao mais recente |
| Exata | `owner/repo@1.2.3` | Exatamente 1.2.3 |
| Circunflexo | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Til | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Intervalo | `owner/repo@>=1.0.0` | Pelo menos 1.0.0 |

**Exemplos:**

```bash
# Instalar todas as dependencias
hpm install

# Instalar pacote especifico
hpm install hemlang/json

# Instalar com restricao de versao
hpm install hemlang/sprout@^2.0.0

# Instalar como dependencia de desenvolvimento
hpm install hemlang/test-utils --dev

# Visualizar o que sera instalado
hpm install hemlang/sprout --dry-run

# Saida detalhada
hpm install --verbose

# Instalar apenas do cache (offline)
hpm install --offline
```

**Saida:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Remove um pacote.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Forma abreviada
hpm remove owner/repo      # Forma alternativa
```

**Exemplo:**

```bash
hpm uninstall hemlang/sprout
```

**Saida:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Atualiza pacotes para as versoes mais recentes dentro das restricoes.

```bash
hpm update              # Atualizar todos os pacotes
hpm update owner/repo   # Atualizar pacote especifico
hpm up owner/repo       # Forma abreviada
```

**Opcoes:**

| Opcao | Descricao |
|-------|-----------|
| `--verbose` | Mostrar progresso detalhado |
| `--dry-run` | Visualizar sem atualizar |

**Exemplos:**

```bash
# Atualizar todos os pacotes
hpm update

# Atualizar pacote especifico
hpm update hemlang/sprout

# Visualizar atualizacoes
hpm update --dry-run
```

**Saida:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Mostra pacotes instalados.

```bash
hpm list              # Mostrar arvore completa de dependencias
hpm list --depth=0    # Apenas dependencias diretas
hpm list --depth=1    # Um nivel de dependencias transitivas
hpm ls                # Forma abreviada
```

**Opcoes:**

| Opcao | Descricao |
|-------|-----------|
| `--depth=N` | Limitar profundidade da arvore (padrao: todas) |

**Exemplo:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Mostra pacotes com versoes mais recentes disponiveis.

```bash
hpm outdated
```

**Saida:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: Versao instalada
- **Wanted**: Versao mais alta que satisfaz a restricao
- **Latest**: Versao mais recente disponivel

---

### hpm run

Executa scripts do package.json.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Exemplo:**

Dado o seguinte package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Execute scripts:

```bash
hpm run start
hpm run test
hpm run build

# Passar argumentos para o script
hpm run test -- --verbose
```

---

### hpm test

Atalho para `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Equivalente a:

```bash
hpm run test
```

---

### hpm why

Explica por que um pacote foi instalado (mostra cadeia de dependencias).

```bash
hpm why owner/repo
```

**Exemplo:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Gerencia o cache global de pacotes.

```bash
hpm cache list    # Listar pacotes em cache
hpm cache clean   # Limpar todos os pacotes em cache
```

**Subcomandos:**

| Subcomando | Descricao |
|------------|-----------|
| `list` | Mostrar todos os pacotes em cache e tamanhos |
| `clean` | Remover todos os pacotes em cache |

**Exemplo:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Atalhos de Comandos

Para conveniencia, varios comandos tem aliases curtos:

| Comando | Atalhos |
|---------|---------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Exemplos:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Codigos de Saida

O hpm usa codigos de saida especificos para indicar diferentes condicoes de erro:

| Codigo | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Conflito de dependencias |
| 2 | Pacote nao encontrado |
| 3 | Versao nao encontrada |
| 4 | Erro de rede |
| 5 | package.json invalido |
| 6 | Verificacao de integridade falhou |
| 7 | Limite de taxa do GitHub excedido |
| 8 | Dependencia circular |

Usando codigos de saida em scripts:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## Variaveis de Ambiente

O hpm suporta as seguintes variaveis de ambiente:

| Variavel | Descricao |
|----------|-----------|
| `GITHUB_TOKEN` | Token de API do GitHub para autenticacao |
| `HPM_CACHE_DIR` | Substituir localizacao do diretorio de cache |
| `HOME` | Diretorio home do usuario (usado para config/cache) |

**Exemplos:**

```bash
# Usar token do GitHub para limites de taxa mais altos
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Usar diretorio de cache personalizado
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## Veja Tambem

- [Configuracao](configuration.md) - Arquivos de configuracao
- [Especificacao de Pacotes](package-spec.md) - Formato do package.json
- [Solucao de Problemas](troubleshooting.md) - Problemas comuns
