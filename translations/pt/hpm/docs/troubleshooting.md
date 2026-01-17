# Solucao de Problemas

Solucoes para problemas comuns do hpm.

## Problemas de Instalacao

### "hemlock: command not found"

**Causa:** O Hemlock nao esta instalado ou nao esta no PATH.

**Solucao:**

```bash
# Verificar se hemlock existe
which hemlock

# Se nao encontrado, instale o Hemlock primeiro
# Visite: https://github.com/hemlang/hemlock

# Apos a instalacao, verifique
hemlock --version
```

### "hpm: command not found"

**Causa:** O hpm nao esta instalado ou nao esta no PATH.

**Solucao:**

```bash
# Verificar localizacao da instalacao do hpm
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Se usando local personalizado, adicionar ao PATH
export PATH="$HOME/.local/bin:$PATH"

# Adicionar ao ~/.bashrc ou ~/.zshrc para persistir
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Se necessario, reinstale
cd /path/to/hpm
sudo make install
```

### "Permission denied" durante instalacao

**Causa:** Sem permissao de escrita no diretorio de instalacao.

**Solucao:**

```bash
# Opcao 1: Usar sudo para instalacao em todo o sistema
sudo make install

# Opcao 2: Instalar no diretorio do usuario (sem sudo)
make install PREFIX=$HOME/.local
```

## Problemas de Dependencias

### "Package not found" (codigo de saida 2)

**Causa:** O pacote nao existe no GitHub.

**Solucao:**

```bash
# Verificar se o pacote existe
# Visite: https://github.com/owner/repo

# Verificar ortografia
hpm install hemlang/sprout  # Correto
hpm install hemlan/sprout   # Owner errado
hpm install hemlang/spout   # Repo errado

# Verificar erros de digitacao no package.json
cat package.json | grep -A 5 dependencies
```

### "Version not found" (codigo de saida 3)

**Causa:** Nenhuma versao publicada corresponde a restricao de versao.

**Solucao:**

```bash
# Listar versoes disponiveis (verificar releases/tags do GitHub)
# Tags devem comecar com 'v' (ex: v1.0.0)

# Usar uma restricao de versao valida
hpm install owner/repo@^1.0.0

# Tentar a versao mais recente
hpm install owner/repo

# Verificar tags disponiveis no GitHub
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (codigo de saida 1)

**Causa:** Dois pacotes requerem versoes incompativeis de uma dependencia.

**Solucao:**

```bash
# Ver conflitos
hpm install --verbose

# Verificar o que requer a dependencia
hpm why conflicting/package

# Solucoes:
# 1. Atualizar pacotes conflitantes
hpm update problem/package

# 2. Alterar restricoes de versao no package.json
# Editar para permitir versoes compativeis

# 3. Remover um dos pacotes conflitantes
hpm uninstall one/package
```

### "Circular dependency" (codigo de saida 8)

**Causa:** Pacote A depende de B, e B depende de A.

**Solucao:**

```bash
# Identificar o ciclo
hpm install --verbose

# Isso geralmente e um bug no pacote
# Contatar o mantenedor do pacote

# Solucao alternativa: evitar usar um dos pacotes
```

## Problemas de Rede

### "Network error" (codigo de saida 4)

**Causa:** Nao foi possivel conectar a API do GitHub.

**Solucao:**

```bash
# Verificar conexao de rede
ping github.com

# Verificar se API do GitHub esta acessivel
curl -I https://api.github.com

# Tentar novamente (hpm tenta automaticamente)
hpm install

# Se pacotes estao em cache, usar modo offline
hpm install --offline

# Se atras de firewall, verificar configuracoes de proxy
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (codigo de saida 7)

**Causa:** Muitas requisicoes de API sem autenticacao.

**Solucao:**

```bash
# Opcao 1: Autenticar com token do GitHub (recomendado)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Criar token: GitHub → Settings → Developer settings → Personal access tokens

# Opcao 2: Salvar token no arquivo de configuracao
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Opcao 3: Esperar limite de taxa resetar (reseta a cada hora)

# Opcao 4: Usar modo offline
hpm install --offline
```

### Timeout de conexao

**Causa:** Rede lenta ou problemas na API do GitHub.

**Solucao:**

```bash
# hpm tenta automaticamente com backoff exponencial

# Verificar se GitHub esta com problemas
# Visite: https://www.githubstatus.com

# Tentar novamente mais tarde
hpm install

# Usar pacotes em cache
hpm install --offline
```

## Problemas do Package.json

### "Invalid package.json" (codigo de saida 5)

**Causa:** Formato incorreto ou campos obrigatorios ausentes.

**Solucao:**

```bash
# Validar sintaxe JSON
cat package.json | python -m json.tool

# Verificar campos obrigatorios
cat package.json

# Campos obrigatorios:
# - "name": formato owner/repo
# - "version": formato X.Y.Z

# Se necessario, regenerar
rm package.json
hpm init
```

### Formato incorreto do "name"

**Causa:** Nome do pacote nao esta no formato `owner/repo`.

**Solucao:**

```json
// Errado
{
  "name": "my-package"
}

// Correto
{
  "name": "yourusername/my-package"
}
```

### Formato incorreto da "version"

**Causa:** Versao nao esta no formato semver.

**Solucao:**

```json
// Errado
{
  "version": "1.0"
}

// Correto
{
  "version": "1.0.0"
}
```

## Problemas do Arquivo de Lock

### Arquivo de lock dessincronizado

**Causa:** package.json foi modificado sem executar install.

**Solucao:**

```bash
# Regenerar arquivo de lock
rm package-lock.json
hpm install
```

### Arquivo de lock corrompido

**Causa:** JSON invalido ou edicao manual.

**Solucao:**

```bash
# Verificar validade do JSON
cat package-lock.json | python -m json.tool

# Regenerar
rm package-lock.json
hpm install
```

## Problemas do hem_modules

### Pacote nao instalado

**Causa:** Varios problemas possiveis.

**Solucao:**

```bash
# Limpar e reinstalar
rm -rf hem_modules
hpm install

# Verificar saida detalhada
hpm install --verbose
```

### Import nao funciona

**Causa:** Pacote nao instalado corretamente ou caminho de import errado.

**Solucao:**

```bash
# Verificar se pacote esta instalado
ls hem_modules/owner/repo/

# Verificar campo main do package.json
cat hem_modules/owner/repo/package.json

# Formato correto de import
import { x } from "owner/repo";          # Usa entrada main
import { y } from "owner/repo/subpath";  # Import de subcaminho
```

### Erro "Module not found"

**Causa:** Caminho de import nao resolve para um arquivo.

**Solucao:**

```bash
# Verificar caminho de import
ls hem_modules/owner/repo/src/

# Verificar index.hml
ls hem_modules/owner/repo/src/index.hml

# Verificar campo main no package.json
cat hem_modules/owner/repo/package.json | grep main
```

## Problemas de Cache

### Cache ocupando muito espaco

**Solucao:**

```bash
# Ver tamanho do cache
hpm cache list

# Limpar cache
hpm cache clean
```

### Permissoes do cache

**Solucao:**

```bash
# Corrigir permissoes
chmod -R u+rw ~/.hpm/cache

# Ou remover e reinstalar
rm -rf ~/.hpm/cache
hpm install
```

### Usando cache errado

**Solucao:**

```bash
# Verificar localizacao do cache
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Se incorreto, limpar variavel de ambiente
unset HPM_CACHE_DIR
```

## Problemas de Scripts

### "Script not found"

**Causa:** Nome do script nao existe no package.json.

**Solucao:**

```bash
# Listar scripts disponiveis
cat package.json | grep -A 20 scripts

# Verificar ortografia
hpm run test    # Correto
hpm run tests   # Errado se o script e chamado "test"
```

### Script falha

**Causa:** Erro no comando do script.

**Solucao:**

```bash
# Executar comando diretamente para ver erro
hemlock test/run.hml

# Verificar definicao do script
cat package.json | grep test
```

## Depuracao

### Habilitar saida detalhada

```bash
hpm install --verbose
```

### Verificar versao do hpm

```bash
hpm --version
```

### Verificar versao do hemlock

```bash
hemlock --version
```

### Execucao simulada

Visualizar sem fazer alteracoes:

```bash
hpm install --dry-run
```

### Comecar do zero

Reiniciar completamente:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Obtendo Ajuda

### Ajuda de comandos

```bash
hpm --help
hpm install --help
```

### Reportando problemas

Se encontrar um bug:

1. Verifique issues existentes: https://github.com/hemlang/hpm/issues
2. Crie um novo issue incluindo:
   - Versao do hpm (`hpm --version`)
   - Versao do Hemlock (`hemlock --version`)
   - Sistema operacional
   - Passos para reproduzir
   - Mensagem de erro (use `--verbose`)

## Referencia de Codigos de Saida

| Codigo | Significado | Solucao Comum |
|--------|-------------|---------------|
| 0 | Sucesso | - |
| 1 | Conflito de dependencias | Atualizar ou alterar restricoes |
| 2 | Pacote nao encontrado | Verificar ortografia, confirmar que repo existe |
| 3 | Versao nao encontrada | Verificar versoes disponiveis no GitHub |
| 4 | Erro de rede | Verificar conexao, tentar novamente |
| 5 | package.json invalido | Corrigir sintaxe JSON e campos obrigatorios |
| 6 | Verificacao de integridade falhou | Limpar cache, reinstalar |
| 7 | Limite de taxa do GitHub | Adicionar GITHUB_TOKEN |
| 8 | Dependencia circular | Contatar mantenedor do pacote |

## Veja Tambem

- [Instalacao](installation.md) - Guia de instalacao
- [Configuracao](configuration.md) - Opcoes de configuracao
- [Comandos](commands.md) - Referencia de comandos
