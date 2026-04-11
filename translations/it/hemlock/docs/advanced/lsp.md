# Language Server Protocol (LSP)

Hemlock include un server LSP integrato per l'integrazione con gli IDE, fornendo diagnostica in tempo reale, navigazione e completamento.

## Avvio del Server

```bash
hemlock lsp --stdio    # Trasporto stdio (raccomandato)
hemlock lsp --tcp 5007 # Trasporto TCP sulla porta specificata
```

## Funzionalità

- **Diagnostica** - Errori di sintassi e type checking in tempo reale
- **Hover** - Informazioni sui tipi e documentazione delle parole chiave
- **Vai alla Definizione** - Naviga alle definizioni di funzioni e variabili
- **Trova Riferimenti** - Trova tutti i riferimenti a un simbolo
- **Simboli del Documento** - Vista strutturale di funzioni e definizioni
- **Completamento** - Suggerimenti per il completamento dei simboli

## Configurazione Editor

### VS Code

Usa l'[estensione Hemlock per VS Code](../editors/vscode/) oppure crea `.vscode/settings.json`:

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

Oppure usa qualsiasi estensione client LSP generica con il comando `hemlock lsp --stdio`.

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

## Debug

Cattura i log del server reindirizzando stderr:

```bash
hemlock lsp --stdio 2>lsp.log
```
