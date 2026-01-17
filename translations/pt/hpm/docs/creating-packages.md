# Criacao de Pacotes

Este guia explica como criar, organizar e publicar pacotes Hemlock.

## Visao Geral

O hpm usa o GitHub como seu registro de pacotes. Os pacotes sao identificados pelo caminho `owner/repo` do GitHub, e as versoes sao tags Git. Publicar e simplesmente enviar releases com tags.

## Criando um Novo Pacote

### 1. Inicializar o Pacote

Crie um novo diretorio e inicialize:

```bash
mkdir my-package
cd my-package
hpm init
```

Responda aos prompts:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Criar Estrutura do Projeto

Estrutura recomendada para um pacote:

```
my-package/
├── package.json          # Manifesto do pacote
├── README.md             # Documentacao
├── LICENSE               # Arquivo de licenca
├── src/
│   ├── index.hml         # Ponto de entrada principal (exporta API publica)
│   ├── utils.hml         # Utilitarios internos
│   └── types.hml         # Definicoes de tipos
└── test/
    ├── framework.hml     # Framework de testes
    └── test_utils.hml    # Testes
```

### 3. Definir sua API Publica

**src/index.hml** - Ponto de entrada principal:

```hemlock
// Re-exportar API publica
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Exports diretos
export fn create(options: Options): Config {
    // Implementacao
}

export fn validate(config: Config): bool {
    // Implementacao
}
```

### 4. Escrever seu package.json

Exemplo completo de package.json:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Nomeacao de Pacotes

### Requisitos

- Deve estar no formato `owner/repo`
- `owner` deve ser seu nome de usuario ou organizacao do GitHub
- `repo` deve ser o nome do repositorio
- Use letras minusculas e hifens para nomes com varias palavras

### Bons Nomes

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### Evite

```
my-package          # Falta owner
alice/MyPackage     # PascalCase
alice/my_package    # Underscores
```

## Melhores Praticas de Estrutura de Pacotes

### Ponto de Entrada

O campo `main` no package.json especifica o ponto de entrada:

```json
{
  "main": "src/index.hml"
}
```

Este arquivo deve exportar sua API publica:

```hemlock
// Exportar tudo que os usuarios precisam
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Tipos
export type { Config, Options } from "./types.hml";
```

### Interno vs Publico

Mantenha detalhes de implementacao interna privados:

```
src/
├── index.hml          # Publico: API exportada
├── parser.hml         # Publico: usado pelo index.hml
├── formatter.hml      # Publico: usado pelo index.hml
└── internal/
    ├── helpers.hml    # Privado: apenas para uso interno
    └── constants.hml  # Privado: apenas para uso interno
```

Usuarios importam da raiz do seu pacote:

```hemlock
// Bom - importa da API publica
import { parse, Parser } from "yourusername/my-package";

// Tambem funciona - import de subcaminho
import { validate } from "yourusername/my-package/validator";

// Desencorajado - acessando internos
import { helper } from "yourusername/my-package/internal/helpers";
```

### Exports de Subcaminho

Suporte imports de subcaminhos:

```
src/
├── index.hml              # Entrada principal
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Usuarios podem importar:

```hemlock
import { parse } from "yourusername/my-package";           // Principal
import { Parser } from "yourusername/my-package/parser";   // Subcaminho
import { format } from "yourusername/my-package/formatter";
```

## Dependencias

### Adicionando Dependencias

```bash
# Dependencias de tempo de execucao
hpm install hemlang/json

# Dependencias de desenvolvimento
hpm install hemlang/test-utils --dev
```

### Melhores Praticas para Dependencias

1. **Use intervalos de circunflexo para a maioria das dependencias**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Trave versoes apenas quando necessario** (API instavel):
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Evite intervalos muito restritivos**:
   ```json
   // Ruim: muito restritivo
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Bom: permite atualizacoes compativeis
   "hemlang/json": "^1.2.3"
   ```

4. **Separe dependencias de desenvolvimento**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Testando seu Pacote

### Escrevendo Testes

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Executando Testes

Adicione um script de teste:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Execute:

```bash
hpm test
```

## Publicacao

### Pre-requisitos

1. Crie um repositorio GitHub que corresponda ao nome do seu pacote
2. Garanta que `package.json` esta completo e valido
3. Todos os testes passando

### Processo de Publicacao

Publicar e simplesmente enviar tags Git:

```bash
# 1. Garanta que tudo esta commitado
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Criar tag de versao (deve comecar com 'v')
git tag v1.0.0

# 3. Enviar codigo e tags
git push origin main
git push origin v1.0.0
# Ou enviar todas as tags de uma vez
git push origin main --tags
```

### Tags de Versao

Tags devem seguir o formato `vX.Y.Z`:

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Patch
git tag v1.1.0      # Minor
git tag v2.0.0      # Major
git tag v1.0.0-beta.1  # Pre-release
```

### Checklist de Publicacao

Antes de publicar uma nova versao:

1. **Atualizar** versao no package.json
2. **Executar testes**: `hpm test`
3. **Atualizar CHANGELOG** (se tiver)
4. **Atualizar README** (se a API mudou)
5. **Commitar alteracoes**
6. **Criar tag**
7. **Enviar para o GitHub**

### Exemplo de Automacao

Criar um script de release:

```bash
#!/bin/bash
# release.sh - Publicar uma nova versao

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Executar testes
hpm test || exit 1

# Atualizar versao no package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Commitar e criar tag
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Enviar
git push origin main --tags

echo "Released v$VERSION"
```

## Usuarios Instalando seu Pacote

Apos a publicacao, usuarios podem instalar:

```bash
# Versao mais recente
hpm install yourusername/my-package

# Versao especifica
hpm install yourusername/my-package@1.0.0

# Restricao de versao
hpm install yourusername/my-package@^1.0.0
```

E importar:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Documentacao

### README.md

Todo pacote deve ter um README:

```markdown
# my-package

A brief description of what this package does.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Usage

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Parses the input string.

### stringify(obj: any): string

Converts object to string.

## License

MIT
```

### Documentacao da API

Documente todos os exports publicos:

```hemlock
/// Analisa a string de entrada em um Result estruturado.
///
/// # Argumentos
/// * `input` - A string a ser analisada
///
/// # Retorna
/// Um Result contendo os dados analisados ou um erro
///
/// # Exemplo
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementacao
}
```

## Guia de Versionamento

Siga o [Versionamento Semantico](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Mudancas incompativeis
- **MINOR** (1.0.0 → 1.1.0): Novos recursos, compativel com versoes anteriores
- **PATCH** (1.0.0 → 1.0.1): Correcoes de bugs, compativel com versoes anteriores

### Quando Incrementar

| Tipo de Mudanca | Incremento de Versao |
|-----------------|---------------------|
| Mudanca incompativel de API | MAJOR |
| Remocao de funcao/tipo | MAJOR |
| Alteracao de assinatura de funcao | MAJOR |
| Adicionar nova funcao | MINOR |
| Adicionar novo recurso | MINOR |
| Correcao de bug | PATCH |
| Atualizacao de documentacao | PATCH |
| Refatoracao interna | PATCH |

## Veja Tambem

- [Especificacao de Pacotes](package-spec.md) - Referencia completa do package.json
- [Versionamento](versioning.md) - Detalhes do versionamento semantico
- [Configuracao](configuration.md) - Autenticacao do GitHub
