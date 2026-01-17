# Codigos de Saida

Referencia dos codigos de saida do hpm e seus significados.

## Tabela de Codigos de Saida

| Codigo | Nome | Descricao |
|--------|------|-----------|
| 0 | SUCCESS | Comando completado com sucesso |
| 1 | CONFLICT | Conflito de versao de dependencias |
| 2 | NOT_FOUND | Pacote nao encontrado |
| 3 | VERSION_NOT_FOUND | Versao solicitada nao encontrada |
| 4 | NETWORK | Erro de rede |
| 5 | INVALID_MANIFEST | package.json invalido |
| 6 | INTEGRITY | Verificacao de integridade falhou |
| 7 | RATE_LIMIT | Limite de taxa da API do GitHub excedido |
| 8 | CIRCULAR | Dependencia circular detectada |

## Descricoes Detalhadas

### Codigo de Saida 0: SUCCESS

Comando completado com sucesso.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Codigo de Saida 1: CONFLICT

Dois ou mais pacotes requerem versoes incompativeis de uma dependencia.

**Exemplo:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Solucao:**
1. Verificar quais pacotes estao em conflito:
   ```bash
   hpm why hemlang/json
   ```
2. Atualizar os pacotes conflitantes:
   ```bash
   hpm update package-a
   ```
3. Relaxar restricoes de versao no package.json
4. Remover um dos pacotes conflitantes

### Codigo de Saida 2: NOT_FOUND

O pacote especificado nao existe no GitHub.

**Exemplo:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Solucao:**
1. Verificar ortografia do nome do pacote
2. Verificar se o repositorio existe: `https://github.com/owner/repo`
3. Verificar se voce tem acesso (para repositorios privados, configurar GITHUB_TOKEN)

### Codigo de Saida 3: VERSION_NOT_FOUND

Nenhuma versao corresponde a restricao especificada.

**Exemplo:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Solucao:**
1. Verificar versoes disponiveis em releases/tags do GitHub
2. Usar uma restricao de versao valida
3. Tags de versao devem comecar com 'v' (ex: `v1.0.0`)

### Codigo de Saida 4: NETWORK

Ocorreu um erro relacionado a rede.

**Exemplo:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Solucao:**
1. Verificar conexao de rede
2. Verificar se o GitHub esta acessivel
3. Se atras de firewall, verificar configuracoes de proxy
4. Se pacotes estao em cache, usar `--offline`:
   ```bash
   hpm install --offline
   ```
5. Esperar e tentar novamente (hpm tenta automaticamente)

### Codigo de Saida 5: INVALID_MANIFEST

Arquivo package.json e invalido ou malformado.

**Exemplo:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Solucao:**
1. Verificar sintaxe JSON (usar validador JSON)
2. Garantir que campos obrigatorios existem (`name`, `version`)
3. Verificar formatos dos campos:
   - name: formato `owner/repo`
   - version: formato semver `X.Y.Z`
4. Regenerar:
   ```bash
   rm package.json
   hpm init
   ```

### Codigo de Saida 6: INTEGRITY

Verificacao de integridade do pacote falhou.

**Exemplo:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Solucao:**
1. Limpar cache e reinstalar:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Verificar problemas de rede (download parcial)
3. Verificar se o pacote nao foi adulterado

### Codigo de Saida 7: RATE_LIMIT

Limite de taxa da API do GitHub excedido.

**Exemplo:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Solucao:**
1. **Usar autenticacao do GitHub** (recomendado):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Esperar limite de taxa resetar (reseta a cada hora)
3. Se pacotes estao em cache, usar modo offline:
   ```bash
   hpm install --offline
   ```

### Codigo de Saida 8: CIRCULAR

Dependencia circular detectada no grafo de dependencias.

**Exemplo:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**Solucao:**
1. Isso geralmente e um bug no proprio pacote
2. Contatar o mantenedor do pacote
3. Evitar usar um dos pacotes circulares

## Usando Codigos de Saida em Scripts

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## Solucao de Problemas por Codigo de Saida

### Referencia Rapida

| Codigo | Verificar Primeiro |
|--------|-------------------|
| 1 | Executar `hpm why <package>` para ver conflitos |
| 2 | Verificar nome do pacote no GitHub |
| 3 | Verificar versoes disponiveis nas tags do GitHub |
| 4 | Verificar conexao de rede |
| 5 | Validar sintaxe do package.json |
| 6 | Executar `hpm cache clean && hpm install` |
| 7 | Definir variavel de ambiente `GITHUB_TOKEN` |
| 8 | Contatar mantenedor do pacote |

## Veja Tambem

- [Solucao de Problemas](troubleshooting.md) - Solucoes detalhadas
- [Comandos](commands.md) - Referencia de comandos
- [Configuracao](configuration.md) - Configurar token do GitHub
