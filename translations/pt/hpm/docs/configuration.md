# Configuracao

Este guia cobre todas as opcoes de configuracao do hpm.

## Visao Geral

O hpm pode ser configurado atraves de:

1. **Variaveis de ambiente** - Para configuracoes em tempo de execucao
2. **Arquivo de configuracao global** - `~/.hpm/config.json`
3. **Arquivos do projeto** - `package.json` e `package-lock.json`

## Variaveis de Ambiente

### GITHUB_TOKEN

Token de API do GitHub para autenticacao.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Beneficios da autenticacao:**
- Limites de taxa de API mais altos (5000 vs 60 requisicoes/hora)
- Acesso a repositorios privados
- Resolucao de dependencias mais rapida

**Criando um token:**

1. Va para GitHub → Settings → Developer settings → Personal access tokens
2. Clique em "Generate new token (classic)"
3. Selecione os escopos:
   - `repo` - Para acesso a repositorios privados
   - `read:packages` - Para GitHub Packages (se usado)
4. Gere e copie o token

### HPM_CACHE_DIR

Substitui o diretorio de cache padrao.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

Padrao: `~/.hpm/cache`

**Casos de uso:**
- Sistemas CI/CD com localizacao de cache personalizada
- Compartilhamento de cache entre projetos
- Cache temporario para builds isoladas

### HOME

Diretorio home do usuario. Usado para localizar:
- Diretorio de configuracao: `$HOME/.hpm/`
- Diretorio de cache: `$HOME/.hpm/cache/`

Normalmente definido pelo sistema; substitua apenas se necessario.

### Exemplo .bashrc / .zshrc

```bash
# Autenticacao do GitHub (recomendado)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Localizacao de cache personalizada (opcional)
# export HPM_CACHE_DIR=/path/to/cache

# Adicionar hpm ao PATH (se usando local de instalacao personalizado)
export PATH="$HOME/.local/bin:$PATH"
```

## Arquivo de Configuracao Global

### Localizacao

`~/.hpm/config.json`

### Formato

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Criando o Arquivo de Configuracao

```bash
# Criar diretorio de configuracao
mkdir -p ~/.hpm

# Criar arquivo de configuracao
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Proteger o arquivo (recomendado)
chmod 600 ~/.hpm/config.json
```

### Prioridade do Token

Se ambos estiverem definidos, a variavel de ambiente tem precedencia:

1. Variavel de ambiente `GITHUB_TOKEN` (mais alta)
2. Campo `github_token` em `~/.hpm/config.json`
3. Sem autenticacao (padrao)

## Estrutura de Diretorios

### Diretorio Global

```
~/.hpm/
├── config.json          # Configuracao global
└── cache/               # Cache de pacotes
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Diretorio do Projeto

```
my-project/
├── package.json         # Manifesto do projeto
├── package-lock.json    # Arquivo de lock de dependencias
├── hem_modules/         # Pacotes instalados
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Codigo-fonte
└── test/                # Testes
```

## Cache de Pacotes

### Localizacao

Padrao: `~/.hpm/cache/`

Substitua com a variavel de ambiente `HPM_CACHE_DIR`

### Estrutura

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Gerenciando o Cache

```bash
# Ver pacotes em cache
hpm cache list

# Limpar todo o cache
hpm cache clean
```

### Comportamento do Cache

- Pacotes sao armazenados em cache apos o primeiro download
- Instalacoes subsequentes usam versoes em cache
- Use `--offline` para instalar apenas do cache
- O cache e compartilhado entre todos os projetos

## Limites de Taxa da API do GitHub

### Sem Autenticacao

- **60 requisicoes por hora**, por endereco IP
- Compartilhado entre todos os usuarios nao autenticados no mesmo IP
- Pode esgotar rapidamente em CI/CD ou com muitas dependencias

### Com Autenticacao

- **5000 requisicoes por hora**, por usuario autenticado
- Limite de taxa pessoal, nao compartilhado

### Lidando com Limites de Taxa

O hpm automaticamente:
- Tenta novamente com backoff exponencial (1s, 2s, 4s, 8s)
- Relata erros de limite de taxa com codigo de saida 7
- Sugere autenticacao se limitado

**Solucoes quando limitado:**

```bash
# Opcao 1: Autenticar com token do GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Opcao 2: Esperar o limite de taxa ser resetado
# (limite reseta a cada hora)

# Opcao 3: Usar modo offline (se pacotes estao em cache)
hpm install --offline
```

## Modo Offline

Instalar pacotes sem acesso a rede:

```bash
hpm install --offline
```

**Requisitos:**
- Todos os pacotes devem estar no cache
- Arquivo de lock deve existir com versoes exatas

**Casos de uso:**
- Ambientes com rede isolada
- Builds CI/CD mais rapidas (com cache quente)
- Evitar limites de taxa

## Configuracao CI/CD

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Instalar Hemlock (ajuste conforme sua configuracao)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copiar arquivos de pacote primeiro (para cache de camadas)
COPY package.json package-lock.json ./

# Instalar dependencias
RUN hpm install

# Copiar codigo-fonte
COPY . .

# Executar aplicacao
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Configuracao de Proxy

Para ambientes atras de um proxy, configure no nivel do sistema:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Melhores Praticas de Seguranca

### Seguranca do Token

1. **Nunca comite tokens** no controle de versao
2. **Use variaveis de ambiente** em CI/CD
3. **Limite escopos do token** ao minimo necessario
4. **Rotacione tokens regularmente**
5. **Proteja arquivos de configuracao**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Repositorios Privados

Para acessar pacotes privados:

1. Crie um token com escopo `repo`
2. Configure autenticacao (variavel de ambiente ou arquivo de configuracao)
3. Garanta que o token tem acesso ao repositorio

```bash
# Testar acesso
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Solucao de Problemas de Configuracao

### Verificando Configuracao

```bash
# Verificar se token esta definido
echo $GITHUB_TOKEN | head -c 10

# Verificar arquivo de configuracao
cat ~/.hpm/config.json

# Verificar diretorio de cache
ls -la ~/.hpm/cache/

# Testar com saida detalhada
hpm install --verbose
```

### Problemas Comuns

**"GitHub rate limit exceeded"**
- Configure autenticacao com `GITHUB_TOKEN`
- Espere o limite de taxa resetar
- Use `--offline` se pacotes estao em cache

**"Permission denied" no cache**
```bash
# Corrigir permissoes do cache
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Criar diretorio de configuracao
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## Veja Tambem

- [Instalacao](installation.md) - Instalando o hpm
- [Solucao de Problemas](troubleshooting.md) - Problemas comuns
- [Comandos](commands.md) - Referencia de comandos
