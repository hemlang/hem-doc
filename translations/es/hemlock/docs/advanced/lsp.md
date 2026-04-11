# Protocolo de Servidor de Lenguaje (LSP)

Hemlock incluye un servidor LSP integrado para integracion con IDEs, proporcionando diagnosticos en tiempo real, navegacion y completado.

## Iniciar el Servidor

```bash
hemlock lsp --stdio    # Transporte Stdio (recomendado)
hemlock lsp --tcp 5007 # Transporte TCP en puerto especificado
```

## Caracteristicas

- **Diagnosticos** - Verificacion de errores de sintaxis y tipos en tiempo real
- **Hover** - Informacion de tipos y documentacion de palabras clave
- **Ir a Definicion** - Navegar a definiciones de funciones y variables
- **Buscar Referencias** - Encontrar todas las referencias a un simbolo
- **Simbolos del Documento** - Vista de esquema de funciones y definiciones
- **Completado** - Sugerencias de completado de simbolos

## Configuracion del Editor

### VS Code

Use la [extension de Hemlock para VS Code](../editors/vscode/) o cree `.vscode/settings.json`:

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

O use cualquier extension de cliente LSP generico con el comando `hemlock lsp --stdio`.

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

## Depuracion

Capture los registros del servidor redirigiendo stderr:

```bash
hemlock lsp --stdio 2>lsp.log
```
