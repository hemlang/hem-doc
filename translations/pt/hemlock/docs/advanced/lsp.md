# Language Server Protocol (LSP)

Hemlock inclui um servidor LSP integrado para integracao com IDEs, fornecendo diagnosticos em tempo real, navegacao e completacao.

## Iniciando o Servidor

```bash
hemlock lsp --stdio    # Transporte Stdio (recomendado)
hemlock lsp --tcp 5007 # Transporte TCP na porta especificada
```

## Funcionalidades

- **Diagnosticos** - Verificacao de erros de sintaxe e tipos em tempo real
- **Hover** - Informacoes de tipo e documentacao de palavras-chave
- **Ir para Definicao** - Navegar para definicoes de funcoes e variaveis
- **Encontrar Referencias** - Encontrar todas as referencias a um simbolo
- **Simbolos do Documento** - Visao geral de funcoes e definicoes
- **Completacao** - Sugestoes de completacao de simbolos

## Configuracao do Editor

### VS Code

Use a [extensao Hemlock para VS Code](../editors/vscode/) ou crie `.vscode/settings.json`:

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

Ou use qualquer extensao cliente LSP generica com o comando `hemlock lsp --stdio`.

### Neovim (nvim-lspconfig)

```lua
local lspconfig = require('lspconfig')
local configs = require('lspconfig.configs')

if not configs.hemlock then
  configs.hemlock = {
    default_config = {
      cmd = { 'hemlock', 'lsp', '--stdio' },
      filetypes = { 'hemlock' },
      root_dir = lspconfig.util.root_pattern('.git', 'hemlock.toml'),
      settings = {},
    },
  }
end

lspconfig.hemlock.setup({})
```

### Vim (vim-lsp)

```vim
if executable('hemlock')
  au User lsp_setup call lsp#register_server({
    \ 'name': 'hemlock',
    \ 'cmd': {server_info->['hemlock', 'lsp', '--stdio']},
    \ 'allowlist': ['hemlock'],
    \ })
endif
```

### Emacs (lsp-mode)

```elisp
(with-eval-after-load 'lsp-mode
  (add-to-list 'lsp-language-id-configuration '(hemlock-mode . "hemlock"))
  (lsp-register-client
   (make-lsp-client
    :new-connection (lsp-stdio-connection '("hemlock" "lsp" "--stdio"))
    :major-modes '(hemlock-mode)
    :server-id 'hemlock-lsp)))
```

## Depuracao

Capture logs do servidor redirecionando stderr:

```bash
hemlock lsp --stdio 2>lsp.log
```
