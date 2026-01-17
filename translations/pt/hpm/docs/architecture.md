# Arquitetura

Arquitetura interna e design do hpm. Este documento e destinado a contribuidores e pessoas interessadas em entender como o hpm funciona.

## Visao Geral

O hpm e escrito em Hemlock e consiste em varios modulos que lidam com diferentes aspectos do gerenciamento de pacotes:

```
src/
├── main.hml        # Ponto de entrada da CLI e roteamento de comandos
├── manifest.hml    # Processamento do package.json
├── lockfile.hml    # Processamento do package-lock.json
├── semver.hml      # Versionamento semantico
├── resolver.hml    # Resolucao de dependencias
├── github.hml      # Cliente da API do GitHub
├── installer.hml   # Download e extracao de pacotes
└── cache.hml       # Gerenciamento de cache global
```

## Responsabilidades dos Modulos

### main.hml

Ponto de entrada para a aplicacao CLI.

**Responsabilidades:**
- Analisar argumentos de linha de comando
- Rotear comandos para handlers apropriados
- Exibir ajuda e informacoes de versao
- Lidar com flags globais (--verbose, --dry-run, etc.)
- Sair com codigos apropriados

**Funcoes principais:**
- `main()` - Ponto de entrada, analisa args e despacha comandos
- `cmd_init()` - Trata `hpm init`
- `cmd_install()` - Trata `hpm install`
- `cmd_uninstall()` - Trata `hpm uninstall`
- `cmd_update()` - Trata `hpm update`
- `cmd_list()` - Trata `hpm list`
- `cmd_outdated()` - Trata `hpm outdated`
- `cmd_run()` - Trata `hpm run`
- `cmd_why()` - Trata `hpm why`
- `cmd_cache()` - Trata `hpm cache`

**Atalhos de comandos:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Lida com leitura e escrita de arquivos `package.json`.

**Responsabilidades:**
- Ler e escrever package.json
- Validar estrutura do pacote
- Gerenciar dependencias
- Analisar especificadores de pacotes (owner/repo@version)

**Funcoes principais:**
```hemlock
create_default(): Manifest           // Criar manifesto vazio
read_manifest(): Manifest            // Ler do arquivo
write_manifest(m: Manifest)          // Escrever no arquivo
validate(m: Manifest): bool          // Validar estrutura
get_all_dependencies(m): Map         // Obter deps + devDeps
add_dependency(m, pkg, ver, dev)     // Adicionar dependencia
remove_dependency(m, pkg)            // Remover dependencia
parse_specifier(spec): (name, ver)   // Analisar "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // Analisar "owner/repo"
```

**Estrutura do Manifest:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Gerencia o arquivo `package-lock.json` para instalacoes reproduziveis.

**Responsabilidades:**
- Criar/ler/escrever arquivo de lock
- Rastrear versoes resolvidas exatas
- Armazenar URLs de download e hashes de integridade
- Limpar dependencias orfas

**Funcoes principais:**
```hemlock
create_empty(): Lockfile              // Criar lockfile vazio
read_lockfile(): Lockfile             // Ler do arquivo
write_lockfile(l: Lockfile)           // Escrever no arquivo
create_entry(ver, url, hash, deps)    // Criar entrada de lock
get_locked(l, pkg): LockEntry?        // Obter versao travada
set_locked(l, pkg, entry)             // Definir versao travada
remove_locked(l, pkg)                 // Remover entrada
prune(l, keep: Set)                   // Remover orfaos
needs_update(l, m): bool              // Verificar se esta dessincronizado
```

**Estrutura do Lockfile:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // URL de download
    integrity: string,    // Hash SHA256
    dependencies: Map<string, string>
};
```

### semver.hml

Implementacao completa do Versionamento Semantico 2.0.0.

**Responsabilidades:**
- Analisar strings de versao
- Comparar versoes
- Analisar e avaliar restricoes de versao
- Encontrar versoes que satisfazem restricoes

**Funcoes principais:**
```hemlock
// Analise
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// Comparacao
compare(a, b: Version): int           // -1, 0, ou 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Restricoes
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // Verificar se v corresponde a c
max_satisfying(versions, c): Version?      // Encontrar mais alta que corresponde
sort(versions): [Version]                  // Ordenar em ordem crescente

// Utilitarios
constraints_overlap(a, b: Constraint): bool  // Verificar compatibilidade
```

**Estrutura de Version:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // Ex: ["beta", "1"]
    build: string?          // Ex: "20230101"
};
```

**Tipos de Constraint:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Intervalos combinados
    | Any;                     // "*"
```

### resolver.hml

Implementa resolucao de dependencias estilo npm.

**Responsabilidades:**
- Resolver arvore de dependencias
- Detectar conflitos de versao
- Detectar dependencias circulares
- Construir arvore de visualizacao

**Funcoes principais:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Resolvedor principal: retorna mapa plano de todas as dependencias
    // com suas versoes resolvidas

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Encontrar versao que satisfaz todas as restricoes

detect_cycles(deps: Map): [Cycle]?
    // Usar DFS para encontrar dependencias circulares

build_tree(lockfile): Tree
    // Criar estrutura de arvore para exibicao

find_why(pkg, lockfile): [Chain]
    // Encontrar cadeias de dependencia explicando por que pkg esta instalado
```

**Algoritmo de Resolucao:**

1. **Coletar restricoes**: Percorrer manifesto e dependencias transitivas
2. **Resolver cada pacote**: Para cada pacote:
   - Obter todas as restricoes de versao dos dependentes
   - Buscar versoes disponiveis do GitHub
   - Encontrar versao mais alta que satisfaz todas as restricoes
   - Erro se nenhuma versao satisfaz todas (conflito)
3. **Detectar ciclos**: Executar DFS para encontrar dependencias circulares
4. **Retornar mapa plano**: Nome do pacote → informacao de versao resolvida

**Estrutura de ResolveResult:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

Cliente da API do GitHub para descoberta e download de pacotes.

**Responsabilidades:**
- Buscar versoes disponiveis (tags)
- Baixar package.json dos repositorios
- Baixar tarballs de release
- Lidar com autenticacao e limites de taxa

**Funcoes principais:**
```hemlock
get_token(): string?
    // Obter token do ambiente ou configuracao

github_request(url, headers?): Response
    // Requisicao de API com retentativas

get_tags(owner, repo): [string]
    // Obter tags de versao (v1.0.0, v1.1.0, etc.)

get_package_json(owner, repo, ref): Manifest
    // Obter package.json em uma tag/commit especifica

download_tarball(owner, repo, tag): bytes
    // Baixar arquivo de release

repo_exists(owner, repo): bool
    // Verificar se repositorio existe

get_repo_info(owner, repo): RepoInfo
    // Obter metadados do repositorio
```

**Logica de retentativa:**
- Backoff exponencial: 1s, 2s, 4s, 8s
- Condicoes de retentativa: 403 (limite de taxa), 5xx (erros de servidor), erros de rede
- Maximo de 4 tentativas
- Relata claramente erros de limite de taxa

**Endpoints de API usados:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Lida com download e extracao de pacotes.

**Responsabilidades:**
- Baixar pacotes do GitHub
- Extrair tarballs para hem_modules
- Verificar/usar pacotes em cache
- Instalar/desinstalar pacotes

**Funcoes principais:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Baixar e instalar um unico pacote

install_all(packages: Map, options): InstallResult
    // Instalar todos os pacotes resolvidos

uninstall_package(name: string): bool
    // Remover pacote do hem_modules

get_installed(): Map<string, string>
    // Listar pacotes atualmente instalados

verify_integrity(pkg): bool
    // Verificar integridade do pacote

prefetch_packages(packages: Map): void
    // Baixar para cache em paralelo (experimental)
```

**Processo de instalacao:**

1. Verificar se a versao correta ja esta instalada
2. Verificar tarball no cache
3. Se nao estiver em cache, baixar do GitHub
4. Armazenar no cache para uso futuro
5. Extrair para `hem_modules/owner/repo/`
6. Verificar instalacao

**Estrutura de diretorio criada:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Gerencia o cache global de pacotes.

**Responsabilidades:**
- Armazenar tarballs baixados
- Recuperar pacotes em cache
- Listar pacotes em cache
- Limpar cache
- Gerenciar configuracao

**Funcoes principais:**
```hemlock
get_cache_dir(): string
    // Obter diretorio de cache (respeita HPM_CACHE_DIR)

get_config_dir(): string
    // Obter diretorio de configuracao (~/.hpm)

is_cached(owner, repo, version): bool
    // Verificar se tarball esta em cache

get_cached_path(owner, repo, version): string
    // Obter caminho para tarball em cache

store_tarball_file(owner, repo, version, data): void
    // Salvar tarball no cache

list_cached(): [CachedPackage]
    // Listar todos os pacotes em cache

clear_cache(): int
    // Remover todos os pacotes em cache, retorna bytes liberados

get_cache_size(): int
    // Calcular tamanho total do cache

read_config(): Config
    // Ler ~/.hpm/config.json

write_config(c: Config): void
    // Escrever arquivo de configuracao
```

**Estrutura do cache:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Fluxo de Dados

### Fluxo do Comando Install

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Analisa args, chama cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Le package.json, adiciona dependencia
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Resolve todas as dependencias
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Busca versoes, encontra satisfazendo
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Baixa e extrai pacotes
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Baixa ou usa cache
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Atualiza package-lock.json
    └──────────┘
```

### Detalhes do Algoritmo de Resolucao

```
Entrada: manifest.dependencies, manifest.devDependencies, lockfile existente

1. Inicializar:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [dependencias diretas]

2. Enquanto queue nao estiver vazia:
   a. pkg = queue.pop()
   b. Se pkg ja esta resolvido, pular
   c. Obter todas as restricoes para pkg dos dependentes
   d. Buscar versoes disponiveis do GitHub (em cache)
   e. Encontrar versao mais alta que satisfaz todas as restricoes
   f. Se nao encontrada: conflito
   g. resolved[pkg] = {version, url, deps}
   h. Adicionar dependencias de pkg a queue

3. Detectar ciclos no grafo resolvido
   - Se ciclos encontrados: erro

4. Retornar mapa resolvido
```

## Tratamento de Erros

### Codigos de Saida

Definidos em main.hml:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Propagacao de Erros

Erros borbulham atraves de valores de retorno:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propaga erros
    // ...
}
```

## Testes

### Framework de Testes

Framework de testes personalizado em `test/framework.hml`:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### Arquivos de Teste

- `test/test_semver.hml` - Analise de versao, comparacao, restricoes
- `test/test_manifest.hml` - Leitura/escrita de manifesto, validacao
- `test/test_lockfile.hml` - Operacoes de lockfile
- `test/test_cache.hml` - Gerenciamento de cache

### Executando Testes

```bash
# Todos os testes
make test

# Testes especificos
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Melhorias Futuras

### Recursos Planejados

1. **Verificacao de integridade** - Verificacao completa de hash SHA256
2. **Workspaces** - Suporte a monorepo
3. **Sistema de plugins** - Comandos extensiveis
4. **Auditoria** - Verificacao de vulnerabilidades de seguranca
5. **Registro privado** - Hospedagem de pacotes auto-hospedada

### Limitacoes Conhecidas

1. **Bug do bundler** - Nao consegue criar executaveis standalone
2. **Downloads paralelos** - Experimental, pode ter condicoes de corrida
3. **Integridade** - SHA256 nao totalmente implementado

## Contribuindo

### Estilo de Codigo

- Use indentacao de 4 espacos
- Funcoes devem fazer apenas uma coisa
- Comente logica complexa
- Escreva testes para novos recursos

### Adicionando Comandos

1. Adicionar handler em `main.hml`:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementacao
   }
   ```

2. Adicionar ao despacho de comandos:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Atualizar texto de ajuda

### Adicionando Modulos

1. Criar `src/newmodule.hml`
2. Exportar interface publica
3. Importar nos modulos que precisam
4. Adicionar testes em `test/test_newmodule.hml`

## Veja Tambem

- [Comandos](commands.md) - Referencia da CLI
- [Criacao de Pacotes](creating-packages.md) - Desenvolvimento de pacotes
- [Versionamento](versioning.md) - Versionamento semantico
