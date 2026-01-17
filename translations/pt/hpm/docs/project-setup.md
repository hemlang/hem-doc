# Configuracao do Projeto

Guia completo para configurar projetos Hemlock com hpm.

## Criando um Novo Projeto

### Configuracao Basica

Crie um novo projeto do zero:

```bash
# Criar diretorio do projeto
mkdir my-project
cd my-project

# Inicializar package.json
hpm init

# Criar estrutura de diretorios
mkdir -p src test
```

### Templates de Projeto

Aqui estao estruturas de projeto comuns para diferentes casos de uso:

#### Biblioteca de Pacotes

Para bibliotecas reutilizaveis:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Entrada principal, exporta API publica
│   ├── core.hml           # Funcionalidade principal
│   ├── utils.hml          # Funcoes utilitarias
│   └── types.hml          # Definicoes de tipos
└── test/
    ├── framework.hml      # Framework de testes
    ├── run.hml            # Executor de testes
    └── test_core.hml      # Testes
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Aplicacao

Para aplicacoes standalone:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Ponto de entrada da aplicacao
│   ├── config.hml         # Configuracao
│   ├── commands/          # Comandos CLI
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Bibliotecas internas
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Arquivos de dados
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Aplicacao Web

Para servidores web:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Ponto de entrada do servidor
│   ├── routes/            # Handlers de rotas
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Modelos de dados
│   │   └── user.hml
│   └── services/          # Logica de negocios
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Arquivos estaticos
│   ├── css/
│   └── js/
└── views/                 # Templates
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## Arquivo package.json

### Campos Obrigatorios

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### Todos os Campos

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
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

### Referencia de Campos

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `name` | string | Nome do pacote no formato owner/repo (obrigatorio) |
| `version` | string | Versao semantica (obrigatorio) |
| `description` | string | Descricao curta |
| `author` | string | Nome e email do autor |
| `license` | string | Identificador da licenca (MIT, Apache-2.0, etc.) |
| `repository` | string | URL do repositorio |
| `homepage` | string | Pagina inicial do projeto |
| `bugs` | string | URL do rastreador de issues |
| `main` | string | Arquivo de ponto de entrada (padrao: src/index.hml) |
| `keywords` | array | Palavras-chave para busca |
| `dependencies` | object | Dependencias de tempo de execucao |
| `devDependencies` | object | Dependencias de desenvolvimento |
| `scripts` | object | Scripts nomeados |
| `files` | array | Arquivos a incluir na publicacao |
| `native` | object | Requisitos de bibliotecas nativas |

## Arquivo package-lock.json

O arquivo de lock e gerado automaticamente e deve ser commitado no controle de versao. Ele garante instalacoes reproduziveis.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Melhores Praticas do Arquivo de Lock

- **Comite** package-lock.json no controle de versao
- **Nao edite manualmente** - e gerado automaticamente
- **Execute `hpm install`** apos puxar alteracoes
- **Delete e regenere** se corrompido:
  ```bash
  rm package-lock.json
  hpm install
  ```

## Diretorio hem_modules

Pacotes instalados sao armazenados em `hem_modules/`:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### Melhores Praticas do hem_modules

- **Adicione ao .gitignore** - Nao comite dependencias
- **Nao modifique** - Alteracoes serao sobrescritas
- **Delete para reinstalar**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

.gitignore recomendado para projetos Hemlock:

```gitignore
# Dependencias
hem_modules/

# Saida de build
dist/
*.hmlc

# Arquivos de IDE
.idea/
.vscode/
*.swp
*.swo

# Arquivos do OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Ambiente
.env
.env.local

# Cobertura de testes
coverage/
```

## Trabalhando com Dependencias

### Adicionando Dependencias

```bash
# Adicionar dependencia de tempo de execucao
hpm install hemlang/json

# Adicionar com restricao de versao
hpm install hemlang/sprout@^2.0.0

# Adicionar dependencia de desenvolvimento
hpm install hemlang/test-utils --dev
```

### Importando Dependencias

```hemlock
// Importar de pacote (usa entrada "main")
import { parse, stringify } from "hemlang/json";

// Importar de subcaminho
import { Router } from "hemlang/sprout/router";

// Importar biblioteca padrao
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Resolucao de Imports

O hpm resolve imports na seguinte ordem:

1. **Biblioteca padrao**: Imports `@stdlib/*` carregam modulos embutidos
2. **Raiz do pacote**: `owner/repo` usa o campo `main`
3. **Subcaminho**: `owner/repo/path` verifica:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Scripts

### Definindo Scripts

Adicione scripts no package.json:

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

### Executando Scripts

```bash
hpm run start
hpm run dev
hpm run build

# Atalho para test
hpm test

# Passar argumentos
hpm run test -- --verbose --filter=unit
```

### Convencoes de Nomeacao de Scripts

| Script | Proposito |
|--------|-----------|
| `start` | Executar a aplicacao |
| `dev` | Executar em modo de desenvolvimento |
| `test` | Executar todos os testes |
| `build` | Compilar para producao |
| `clean` | Remover arquivos gerados |
| `lint` | Verificar estilo de codigo |
| `format` | Formatar codigo |

## Fluxo de Trabalho de Desenvolvimento

### Configuracao Inicial

```bash
# Clonar projeto
git clone https://github.com/yourusername/my-project.git
cd my-project

# Instalar dependencias
hpm install

# Executar testes
hpm test

# Iniciar desenvolvimento
hpm run dev
```

### Fluxo de Trabalho Diario

```bash
# Puxar ultimas alteracoes
git pull

# Instalar quaisquer novas dependencias
hpm install

# Fazer alteracoes...

# Executar testes
hpm test

# Commitar
git add .
git commit -m "Add feature"
git push
```

### Adicionando Nova Funcionalidade

```bash
# Criar branch de feature
git checkout -b feature/new-feature

# Adicionar novas dependencias se necessario
hpm install hemlang/new-lib

# Implementar funcionalidade...

# Testar
hpm test

# Commitar e enviar
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## Configuracao Especifica por Ambiente

### Usando Variaveis de Ambiente

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### Arquivo de Configuracao

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## Veja Tambem

- [Inicio Rapido](quick-start.md) - Introducao rapida
- [Comandos](commands.md) - Referencia de comandos
- [Criacao de Pacotes](creating-packages.md) - Publicar pacotes
- [Configuracao](configuration.md) - Configuracao do hpm
