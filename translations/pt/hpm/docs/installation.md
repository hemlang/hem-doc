# Instalacao

Este guia explica como instalar o hpm no seu sistema.

## Instalacao Rapida (Recomendada)

Instale a versao mais recente com um unico comando:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Isso automaticamente:
- Detecta seu sistema operacional (Linux, macOS)
- Detecta sua arquitetura (x86_64, arm64)
- Baixa o binario pre-compilado correspondente
- Instala em `/usr/local/bin` (usa sudo se necessario)

### Opcoes de Instalacao

```bash
# Instalar em local personalizado (sem sudo)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Instalar versao especifica
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Combinar opcoes
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Plataformas Suportadas

| Plataforma | Arquitetura | Status |
|------------|-------------|--------|
| Linux      | x86_64      | Suportado |
| macOS      | x86_64      | Suportado |
| macOS      | arm64 (M1/M2/M3) | Suportado |
| Linux      | arm64       | Compilar do codigo-fonte |

## Compilando do Codigo-Fonte

Se voce prefere compilar do codigo-fonte, ou precisa de uma plataforma nao coberta pelos binarios pre-compilados, siga estas instrucoes.

### Pre-requisitos

O hpm requer que o [Hemlock](https://github.com/hemlang/hemlock) esteja instalado. Por favor, siga as instrucoes de instalacao do Hemlock primeiro.

Verifique se o Hemlock esta instalado:

```bash
hemlock --version
```

## Metodos de Instalacao

### Metodo 1: Make Install

Compile e instale a partir do codigo-fonte.

```bash
# Clonar o repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Instalar em /usr/local/bin (requer sudo)
sudo make install
```

Apos a instalacao, verifique se esta funcionando:

```bash
hpm --version
```

### Metodo 2: Local Personalizado

Instale em um diretorio personalizado (sem sudo):

```bash
# Clonar o repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Instalar em ~/.local/bin
make install PREFIX=$HOME/.local

# Ou qualquer local personalizado
make install PREFIX=/opt/hemlock
```

Certifique-se de que seu diretorio bin personalizado esta no PATH:

```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Metodo 3: Executar Sem Instalar

Voce pode executar o hpm diretamente sem instalar:

```bash
# Clonar o repositorio
git clone https://github.com/hemlang/hpm.git
cd hpm

# Criar script wrapper local
make

# Executar do diretorio hpm
./hpm --help

# Ou executar diretamente via hemlock
hemlock src/main.hml --help
```

### Metodo 4: Instalacao Manual

Crie seu proprio script wrapper:

```bash
# Clonar para um local permanente
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Criar script wrapper
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Variaveis de Instalacao

O Makefile suporta as seguintes variaveis:

| Variavel | Padrao | Descricao |
|----------|--------|-----------|
| `PREFIX` | `/usr/local` | Prefixo de instalacao |
| `BINDIR` | `$(PREFIX)/bin` | Diretorio de binarios |
| `HEMLOCK` | `hemlock` | Caminho do interpretador hemlock |

Exemplo usando variaveis personalizadas:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Como Funciona

O instalador cria um script shell wrapper que invoca o interpretador Hemlock com o codigo-fonte do hpm:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

Esta abordagem:
- Nao requer compilacao
- Sempre executa o codigo-fonte mais recente
- Funciona de forma confiavel em todas as plataformas

## Atualizando o hpm

Para atualizar o hpm para a versao mais recente:

```bash
cd /path/to/hpm
git pull origin main

# Reinstalar se o caminho mudou
sudo make install
```

## Desinstalacao

Para remover o hpm do sistema:

```bash
cd /path/to/hpm
sudo make uninstall
```

Ou remova manualmente:

```bash
sudo rm /usr/local/bin/hpm
```

## Verificando a Instalacao

Apos a instalacao, verifique se tudo esta funcionando:

```bash
# Verificar versao
hpm --version

# Ver ajuda
hpm --help

# Testar inicializacao (em um diretorio vazio)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Solucao de Problemas

### "hemlock: command not found"

O Hemlock nao esta instalado ou nao esta no PATH. Instale o Hemlock primeiro:

```bash
# Verificar se hemlock existe
which hemlock

# Se nao encontrado, instale o Hemlock de https://github.com/hemlang/hemlock
```

### "Permission denied"

Use sudo para instalacao em todo o sistema, ou instale no diretorio do usuario:

```bash
# Opcao 1: Usar sudo
sudo make install

# Opcao 2: Instalar no diretorio do usuario
make install PREFIX=$HOME/.local
```

### "hpm: command not found" apos instalacao

Seu PATH pode nao incluir o diretorio de instalacao:

```bash
# Verificar onde o hpm foi instalado
ls -la /usr/local/bin/hpm

# Se usando local personalizado, adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"
```

## Notas Especificas por Plataforma

### Linux

A instalacao padrao funciona em todas as distribuicoes Linux. Algumas distribuicoes podem precisar:

```bash
# Debian/Ubuntu: garantir que ferramentas de compilacao estao instaladas
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

A instalacao padrao funciona. Se usar Homebrew:

```bash
# Garantir que as ferramentas de linha de comando do Xcode estao instaladas
xcode-select --install
```

### Windows (WSL)

O hpm funciona no Windows Subsystem for Linux:

```bash
# No terminal WSL
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Proximos Passos

Apos a instalacao:

1. [Inicio Rapido](quick-start.md) - Crie seu primeiro projeto
2. [Referencia de Comandos](commands.md) - Aprenda todos os comandos
3. [Configuracao](configuration.md) - Configure o hpm
