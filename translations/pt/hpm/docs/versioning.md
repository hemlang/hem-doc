# Versionamento

Guia completo de versionamento semantico no hpm.

## Versionamento Semantico

O hpm usa [Versionamento Semantico 2.0.0](https://semver.org/) (semver) para versoes de pacotes.

### Formato de Versao

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Exemplos:**
```
1.0.0           # Versao de release
2.1.3           # Versao de release
1.0.0-alpha     # Pre-release
1.0.0-beta.1    # Pre-release numerado
1.0.0-rc.1      # Release candidate
1.0.0+20231201  # Com metadados de build
1.0.0-beta+exp  # Pre-release com metadados de build
```

### Componentes da Versao

| Componente | Descricao | Exemplo |
|------------|-----------|---------|
| MAJOR | Mudancas incompativeis | `1.0.0` → `2.0.0` |
| MINOR | Novos recursos (compativel) | `1.0.0` → `1.1.0` |
| PATCH | Correcoes de bugs (compativel) | `1.0.0` → `1.0.1` |
| PRERELEASE | Identificador de pre-release | `1.0.0-alpha` |
| BUILD | Metadados de build (ignorado na comparacao) | `1.0.0+build123` |

### Quando Incrementar

| Tipo de Mudanca | Incremento | Exemplo |
|-----------------|------------|---------|
| Mudanca incompativel de API | MAJOR | Remover funcao |
| Renomear funcao publica | MAJOR | `parse()` → `decode()` |
| Mudar assinatura de funcao | MAJOR | Adicionar parametro obrigatorio |
| Adicionar nova funcao | MINOR | Adicionar `validate()` |
| Adicionar parametro opcional | MINOR | Novo parametro `options` opcional |
| Correcao de bug | PATCH | Corrigir null pointer |
| Melhoria de performance | PATCH | Algoritmo mais rapido |
| Refatoracao interna | PATCH | Sem mudanca de API |

## Restricoes de Versao

### Sintaxe de Restricoes

| Sintaxe | Significado | Resolve para |
|---------|-------------|--------------|
| `1.2.3` | Versao exata | Apenas 1.2.3 |
| `^1.2.3` | Circunflexo (compativel) | >=1.2.3 e <2.0.0 |
| `~1.2.3` | Til (atualizacoes de patch) | >=1.2.3 e <1.3.0 |
| `>=1.0.0` | Pelo menos | 1.0.0 ou superior |
| `>1.0.0` | Maior que | Superior a 1.0.0 |
| `<2.0.0` | Menor que | Inferior a 2.0.0 |
| `<=2.0.0` | No maximo | 2.0.0 ou inferior |
| `>=1.0.0 <2.0.0` | Intervalo | Entre 1.0.0 e 2.0.0 |
| `*` | Qualquer | Qualquer versao |

### Intervalo de Circunflexo (^)

O circunflexo (`^`) permite mudancas que nao modificam o digito nao-zero mais a esquerda:

```
^1.2.3  →  >=1.2.3 <2.0.0   # Permite 1.x.x
^0.2.3  →  >=0.2.3 <0.3.0   # Permite 0.2.x
^0.0.3  →  >=0.0.3 <0.0.4   # Permite apenas 0.0.3
```

**Caso de uso:** Voce quer atualizacoes compativeis dentro da versao major.

**Restricao mais comum** - Recomendada para a maioria das dependencias.

### Intervalo de Til (~)

O til (`~`) permite apenas mudancas de patch:

```
~1.2.3  →  >=1.2.3 <1.3.0   # Permite 1.2.x
~1.2    →  >=1.2.0 <1.3.0   # Permite 1.2.x
~1      →  >=1.0.0 <2.0.0   # Permite 1.x.x
```

**Caso de uso:** Voce quer apenas correcoes de bugs, sem novos recursos.

### Intervalos de Comparacao

Combine operadores de comparacao para controle preciso:

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### Qualquer Versao (*)

Corresponde a qualquer versao:

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**Aviso:** Nao recomendado para producao. Sempre obtera a versao mais recente.

## Versoes Pre-release

### Identificadores Pre-release

Versoes pre-release tem menor precedencia que versoes de release:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Tags Pre-release Comuns

| Tag | Significado | Estagio |
|-----|-------------|---------|
| `alpha` | Desenvolvimento inicial | Muito instavel |
| `beta` | Feature-complete | Em testes |
| `rc` | Release candidate | Testes finais |
| `dev` | Snapshot de desenvolvimento | Instavel |

### Pre-release em Restricoes

Restricoes nao correspondem a versoes pre-release por padrao:

```
^1.0.0    # Nao corresponde a 1.1.0-beta
>=1.0.0   # Nao corresponde a 2.0.0-alpha
```

Para incluir versoes pre-release, referencie-as explicitamente:

```
>=1.0.0-alpha <2.0.0   # Inclui todos os pre-releases 1.x
```

## Comparacao de Versoes

### Regras de Comparacao

1. Compare MAJOR, MINOR, PATCH numericamente
2. Release > pre-release com mesmo numero de versao
3. Pre-releases sao comparados alfanumericamente
4. Metadados de build sao ignorados

### Exemplos

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Metadados de build ignorados
```

### Ordenacao

Versoes sao ordenadas em ordem crescente:

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Resolucao de Versoes

### Algoritmo de Resolucao

Quando multiplos pacotes requerem a mesma dependencia:

1. Coletar todas as restricoes
2. Encontrar intersecao de todos os intervalos
3. Selecionar a versao mais alta na intersecao
4. Erro se nenhuma versao satisfizer todas as restricoes

### Exemplo de Resolucao

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Intersecao: >=1.2.0 <1.3.0
Disponiveis: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Resolvido: 1.2.5 (mais alta na intersecao)
```

### Deteccao de Conflitos

Conflitos ocorrem quando nenhuma versao satisfaz todas as restricoes:

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Intersecao: (vazia)
Resultado: CONFLITO - nenhuma versao satisfaz ambas
```

## Melhores Praticas

### Para Consumidores de Pacotes

1. **Use intervalos de circunflexo para a maioria das dependencias**:
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Use intervalos de til para dependencias criticas**:
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **Trave versoes apenas quando necessario**:
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **Comite arquivo de lock** para builds reproduziveis

5. **Atualize regularmente** para obter correcoes de seguranca:
   ```bash
   hpm update
   hpm outdated
   ```

### Para Autores de Pacotes

1. **Comece com 0.1.0 para desenvolvimento inicial**:
   - API pode mudar frequentemente
   - Usuarios esperam instabilidade

2. **Avance para 1.0.0 quando a API estiver estavel**:
   - Compromisso publico com estabilidade
   - Mudancas incompativeis requerem incremento de major

3. **Siga semver estritamente**:
   - Mudancas incompativeis = MAJOR
   - Novos recursos = MINOR
   - Correcoes de bugs = PATCH

4. **Use versoes pre-release para testes**:
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Documente mudancas incompativeis** no CHANGELOG

## Publicando Versoes

### Criando uma Release

```bash
# Atualizar versao no package.json
# Editar package.json: "version": "1.1.0"

# Commitar mudanca de versao
git add package.json
git commit -m "Bump version to 1.1.0"

# Criar e enviar tag
git tag v1.1.0
git push origin main --tags
```

### Formato de Tag

Tags **devem** comecar com `v`:

```
v1.0.0      Correto
v1.0.0-beta Correto
1.0.0       Nao sera reconhecido
```

### Fluxo de Trabalho de Release

```bash
# 1. Garantir que testes passam
hpm test

# 2. Atualizar versao no package.json
# 3. Atualizar CHANGELOG.md
# 4. Commitar mudancas
git add -A
git commit -m "Release v1.2.0"

# 5. Criar tag
git tag v1.2.0

# 6. Enviar tudo
git push origin main --tags
```

## Verificando Versoes

### Listar Versoes Instaladas

```bash
hpm list
```

### Verificar Atualizacoes

```bash
hpm outdated
```

Saida:
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current**: Versao instalada
- **Wanted**: Versao mais alta que satisfaz a restricao
- **Latest**: Versao mais recente disponivel

### Atualizar Pacotes

```bash
# Atualizar todos
hpm update

# Atualizar pacote especifico
hpm update hemlang/json
```

## Veja Tambem

- [Criacao de Pacotes](creating-packages.md) - Guia de publicacao
- [Especificacao de Pacotes](package-spec.md) - Formato do package.json
- [Comandos](commands.md) - Referencia da CLI
