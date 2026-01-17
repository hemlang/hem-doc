# Inicio Rapido

Comece a usar o hpm em 5 minutos.

## Instalar o hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Veja o [Guia de Instalacao](installation.md) para mais opcoes de instalacao.

## Criar um Novo Projeto

Primeiro, crie um novo diretorio e inicialize o pacote:

```bash
mkdir my-project
cd my-project
hpm init
```

O sistema solicitara os detalhes do projeto:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Use `--yes` para aceitar todos os valores padrao:

```bash
hpm init --yes
```

## Estrutura do Projeto

Crie a estrutura basica do projeto:

```
my-project/
├── package.json        # Manifesto do projeto
├── src/
│   └── index.hml      # Ponto de entrada principal
└── test/
    └── test.hml       # Arquivo de testes
```

Crie o arquivo principal:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Ponto de entrada principal
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## Instalar Dependencias

Pesquise pacotes no GitHub (pacotes usam o formato `owner/repo`):

```bash
# Instalar um pacote
hpm install hemlang/sprout

# Instalar com restricao de versao
hpm install hemlang/json@^1.0.0

# Instalar como dependencia de desenvolvimento
hpm install hemlang/test-utils --dev
```

Apos a instalacao, a estrutura do seu projeto incluira `hem_modules/`:

```
my-project/
├── package.json
├── package-lock.json   # Arquivo de lock (gerado automaticamente)
├── hem_modules/        # Pacotes instalados
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Usando Pacotes Instalados

Importe pacotes usando o caminho do GitHub:

```hemlock
// Importar de pacote instalado
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Importar de subcaminho
import { middleware } from "hemlang/sprout/middleware";

// Biblioteca padrao (embutida)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Adicionar Scripts

Adicione scripts no `package.json`:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Execute scripts com `hpm run`:

```bash
hpm run start
hpm run build

# Atalho para test
hpm test
```

## Fluxos de Trabalho Comuns

### Instalar Todas as Dependencias

Quando voce clona um projeto com `package.json`:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Atualizar Dependencias

Atualize todos os pacotes para as versoes mais recentes dentro das restricoes:

```bash
hpm update
```

Atualize pacotes especificos:

```bash
hpm update hemlang/sprout
```

### Ver Pacotes Instalados

Liste todos os pacotes instalados:

```bash
hpm list
```

A saida mostra a arvore de dependencias:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Verificar Atualizacoes

Veja quais pacotes tem versoes mais recentes disponiveis:

```bash
hpm outdated
```

### Remover Pacotes

```bash
hpm uninstall hemlang/sprout
```

## Exemplo: Aplicacao Web

Aqui esta um exemplo completo usando um framework web:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

Execute a aplicacao:

```bash
hpm install
hpm run start
```

## Proximos Passos

- [Referencia de Comandos](commands.md) - Aprenda todos os comandos do hpm
- [Criacao de Pacotes](creating-packages.md) - Publique seus proprios pacotes
- [Configuracao](configuration.md) - Configure o hpm e o token do GitHub
- [Configuracao do Projeto](project-setup.md) - Configuracao detalhada do projeto
