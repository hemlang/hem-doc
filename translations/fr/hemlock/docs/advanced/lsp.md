# Language Server Protocol (LSP)

Hemlock inclut un serveur LSP integre pour l'integration IDE, fournissant des diagnostics en temps reel, la navigation et la completion.

## Demarrage du serveur

```bash
hemlock lsp --stdio    # Transport Stdio (recommande)
hemlock lsp --tcp 5007 # Transport TCP sur le port specifie
```

## Fonctionnalites

- **Diagnostics** - Verification des erreurs de syntaxe et de type en temps reel
- **Survol** - Informations de type et documentation des mots-cles
- **Aller a la definition** - Naviguer vers les definitions de fonctions et variables
- **Trouver les references** - Trouver toutes les references a un symbole
- **Symboles du document** - Vue d'ensemble des fonctions et definitions
- **Completion** - Suggestions de completion de symboles

## Configuration de l'editeur

### VS Code

Utilisez l'[extension Hemlock pour VS Code](../editors/vscode/) ou creez `.vscode/settings.json` :

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

Ou utilisez n'importe quelle extension client LSP generique avec la commande `hemlock lsp --stdio`.

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

## Debogage

Capturez les logs du serveur en redirigeant stderr :

```bash
hemlock lsp --stdio 2>lsp.log
```
