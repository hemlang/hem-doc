# Guia de Instalacao

Este guia ira ajuda-lo a compilar e instalar o Hemlock em seu sistema.

## Instalacao Rapida (Recomendado)

A maneira mais simples de instalar o Hemlock e usando o script de instalacao de uma linha:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Isso ira baixar e instalar o binario pre-compilado mais recente para sua plataforma (Linux ou macOS, x86_64 ou arm64).

### Opcoes de Instalacao

```bash
# Instalar em um prefixo personalizado (padrao: ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Instalar uma versao especifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Instalar e atualizar automaticamente o PATH do shell
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

Apos a instalacao, verifique se esta funcionando corretamente:

```bash
hemlock --version
```

---

## Compilar a Partir do Codigo-Fonte

Se voce preferir compilar a partir do codigo-fonte, ou se os binarios pre-compilados nao estao disponiveis para seu sistema, siga as instrucoes abaixo.

## Pre-requisitos

### Dependencias Necessarias

A compilacao do Hemlock requer as seguintes dependencias:

- **Compilador C**: GCC ou Clang (padrao C11)
- **Make**: GNU Make
- **libffi**: Biblioteca de interface de funcoes externas (para suporte FFI)
- **OpenSSL**: Biblioteca de criptografia (para funcoes hash: md5, sha1, sha256)
- **libwebsockets**: Suporte a WebSocket e cliente/servidor HTTP
- **zlib**: Biblioteca de compressao

### Instalando Dependencias

**macOS:**
```bash
# Se ainda nao estiver instalado, instale o Homebrew primeiro
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale as ferramentas de linha de comando do Xcode
xcode-select --install

# Instale as dependencias via Homebrew
brew install libffi openssl@3 libwebsockets
```

**Nota para usuarios macOS**: O Makefile detecta automaticamente a instalacao do Homebrew e configura os caminhos corretos de include/library. O Hemlock suporta arquiteturas Intel (x86_64) e Apple Silicon (arm64).

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Compilar a Partir do Codigo-Fonte

### 1. Clonar o Repositorio

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Compilar o Hemlock

```bash
make
```

Isso ira compilar o interpretador Hemlock e colocar o executavel no diretorio atual.

### 3. Verificar a Instalacao

```bash
./hemlock --version
```

Voce devera ver as informacoes de versao do Hemlock.

### 4. Testar a Compilacao

Execute a suite de testes para garantir que tudo esta funcionando corretamente:

```bash
make test
```

Todos os testes devem passar. Se voce encontrar alguma falha, por favor reporte como uma issue.

## Instalacao em Nivel de Sistema (Opcional)

Para instalar o Hemlock em nivel de sistema (por exemplo, em `/usr/local/bin`):

```bash
sudo make install
```

Isso permite executar `hemlock` de qualquer local sem especificar o caminho completo.

## Executar o Hemlock

### REPL Interativo

Inicie o laco de leitura-avaliacao-impressao (REPL):

```bash
./hemlock
```

Voce vera um prompt onde pode digitar codigo Hemlock:

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

Use `Ctrl+D` ou `Ctrl+C` para sair do REPL.

### Executar Programas

Execute um script Hemlock:

```bash
./hemlock program.hml
```

Com argumentos de linha de comando:

```bash
./hemlock program.hml arg1 arg2 "argumento com espacos"
```

## Estrutura de Diretorios

Apos a compilacao, seu diretorio Hemlock tera esta aparencia:

```
hemlock/
├── hemlock           # Executavel do interpretador compilado
├── src/              # Codigo-fonte
├── include/          # Arquivos de cabecalho
├── tests/            # Suite de testes
├── examples/         # Programas de exemplo
├── docs/             # Documentacao
├── stdlib/           # Biblioteca padrao
├── Makefile          # Configuracao de compilacao
└── README.md         # Descricao do projeto
```

## Opcoes de Compilacao

### Compilacao de Depuracao

Compilar com simbolos de depuracao e sem otimizacao:

```bash
make debug
```

### Limpar Compilacao

Remover todos os arquivos compilados:

```bash
make clean
```

Recompilar do zero:

```bash
make clean && make
```

## Solucao de Problemas

### macOS: Erro de Biblioteca Nao Encontrada

Se voce receber erros sobre bibliotecas ausentes (`-lcrypto`, `-lffi`, etc.):

1. Certifique-se de que as dependencias do Homebrew estao instaladas:
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Verifique os caminhos do Homebrew:
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. O Makefile deve detectar esses caminhos automaticamente. Se nao detectar, verifique se `brew` esta no seu PATH:
   ```bash
   which brew
   ```

### macOS: Erros de Tipo BSD (`u_int`, `u_char` nao encontrados)

Se voce ver erros sobre nomes de tipo desconhecidos como `u_int` ou `u_char`:

1. Isso foi corrigido na versao v1.0.0+ usando `_DARWIN_C_SOURCE` em vez de `_POSIX_C_SOURCE`
2. Certifique-se de ter a versao mais recente do codigo
3. Limpe e recompile:
   ```bash
   make clean && make
   ```

### Linux: libffi Nao Encontrada

Se voce receber erros sobre `ffi.h` ou `-lffi` ausentes:

1. Certifique-se de que `libffi-dev` esta instalado (veja as dependencias acima)
2. Verifique se `pkg-config` consegue encontra-la:
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. Se nao for encontrada, voce pode precisar definir `PKG_CONFIG_PATH`:
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Erros de Compilacao

Se voce encontrar erros de compilacao:

1. Certifique-se de ter um compilador compativel com C11
2. No macOS, tente usar Clang (padrao):
   ```bash
   make CC=clang
   ```
3. No Linux, tente usar GCC:
   ```bash
   make CC=gcc
   ```
4. Verifique se todas as dependencias estao instaladas
5. Tente recompilar do zero:
   ```bash
   make clean && make
   ```

### Falha nos Testes

Se os testes falharem:

1. Verifique se voce tem a versao mais recente do codigo
2. Tente recompilar do zero:
   ```bash
   make clean && make test
   ```
3. No macOS, certifique-se de ter as ferramentas de linha de comando do Xcode mais recentes:
   ```bash
   xcode-select --install
   ```
4. Reporte a issue no GitHub, incluindo:
   - Sua plataforma (versao do macOS / distribuicao Linux)
   - Arquitetura (x86_64 / arm64)
   - Saida do teste
   - Saida de `make -v` e `gcc --version` (ou `clang --version`)

## Proximos Passos

- [Guia de Inicio Rapido](quick-start.md) - Escreva seu primeiro programa Hemlock
- [Tutorial](tutorial.md) - Aprenda Hemlock passo a passo
- [Guia da Linguagem](../language-guide/syntax.md) - Explore os recursos do Hemlock
