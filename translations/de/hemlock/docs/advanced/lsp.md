# Language Server Protocol (LSP)

Hemlock enthält einen eingebauten LSP-Server für IDE-Integration, der Echtzeit-Diagnosen, Navigation und Vervollständigung bietet.

## Server starten

```bash
hemlock lsp --stdio    # Stdio-Transport (empfohlen)
hemlock lsp --tcp 5007 # TCP-Transport auf angegebenem Port
```

## Funktionen

- **Diagnosen** - Echtzeit-Syntaxfehler und Typprüfung
- **Hover** - Typinformationen und Schlüsselwort-Dokumentation
- **Gehe zu Definition** - Zu Funktions- und Variablendefinitionen navigieren
- **Referenzen finden** - Alle Referenzen eines Symbols finden
- **Dokumentsymbole** - Gliederungsansicht von Funktionen und Definitionen
- **Vervollständigung** - Symbolvervollständigungs-Vorschläge

## Editor-Einrichtung

### VS Code

Verwenden Sie die [Hemlock VS Code-Erweiterung](../editors/vscode/) oder erstellen Sie `.vscode/settings.json`:

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

Oder verwenden Sie eine beliebige generische LSP-Client-Erweiterung mit dem Befehl `hemlock lsp --stdio`.

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

## Debugging

Server-Logs durch Umleitung von stderr erfassen:

```bash
hemlock lsp --stdio 2>lsp.log
```
