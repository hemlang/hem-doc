# Documentacao do hpm

Bem-vindo a documentacao do hpm (Hemlock Package Manager). O hpm e o gerenciador de pacotes oficial da linguagem de programacao [Hemlock](https://github.com/hemlang/hemlock).

## Visao Geral

O hpm utiliza o GitHub como seu registro de pacotes, onde os pacotes sao identificados pelo caminho do repositorio GitHub (por exemplo, `hemlang/sprout`). Isso significa:

- **Sem registro central** - Os pacotes ficam em repositorios do GitHub
- **Tags de versao** - As versoes sao identificadas por tags Git (por exemplo, `v1.0.0`)
- **Publicacao via git** - Enviar uma tag publica uma nova versao

## Documentacao

### Guia de Introducao

- [Instalacao](installation.md) - Como instalar o hpm
- [Inicio Rapido](quick-start.md) - Comece a usar em 5 minutos
- [Configuracao do Projeto](project-setup.md) - Configurar um novo projeto Hemlock

### Guia do Usuario

- [Referencia de Comandos](commands.md) - Referencia completa de todos os comandos do hpm
- [Configuracao](configuration.md) - Arquivos de configuracao e variaveis de ambiente
- [Solucao de Problemas](troubleshooting.md) - Problemas comuns e solucoes

### Desenvolvimento de Pacotes

- [Criacao de Pacotes](creating-packages.md) - Como criar e publicar pacotes
- [Especificacao de Pacotes](package-spec.md) - Formato do package.json
- [Versionamento](versioning.md) - Versionamento semantico e restricoes de versao

### Referencia

- [Arquitetura](architecture.md) - Arquitetura interna e design
- [Codigos de Saida](exit-codes.md) - Referencia dos codigos de saida da CLI

## Referencia Rapida

### Comandos Basicos

```bash
hpm init                              # Criar novo package.json
hpm install                           # Instalar todas as dependencias
hpm install owner/repo                # Adicionar e instalar um pacote
hpm install owner/repo@^1.0.0        # Instalar com restricao de versao
hpm uninstall owner/repo              # Remover um pacote
hpm update                            # Atualizar todos os pacotes
hpm list                              # Mostrar pacotes instalados
hpm run <script>                      # Executar script do pacote
```

### Identificacao de Pacotes

Os pacotes usam o formato `owner/repo` do GitHub:

```
hemlang/sprout          # Framework web
hemlang/json            # Biblioteca de utilitarios JSON
alice/http-client       # Biblioteca cliente HTTP
```

### Restricoes de Versao

| Sintaxe | Significado |
|---------|-------------|
| `1.0.0` | Versao exata |
| `^1.2.3` | Versao compativel (>=1.2.3 <2.0.0) |
| `~1.2.3` | Atualizacao de patch (>=1.2.3 <1.3.0) |
| `>=1.0.0` | Pelo menos 1.0.0 |
| `*` | Qualquer versao |

## Obtendo Ajuda

- Use `hpm --help` para ajuda na linha de comando
- Use `hpm <command> --help` para ajuda de comandos especificos
- Reporte problemas em [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## Licenca

O hpm e distribuido sob a licenca MIT.
