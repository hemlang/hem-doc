# Language Server Protocol (LSP)

Hemlock включает встроенный LSP-сервер для интеграции с IDE, обеспечивающий диагностику в реальном времени, навигацию и автодополнение.

## Запуск сервера

```bash
hemlock lsp --stdio    # Транспорт stdio (рекомендуется)
hemlock lsp --tcp 5007 # Транспорт TCP на указанном порту
```

## Возможности

- **Диагностика** - Проверка синтаксических ошибок и типов в реальном времени
- **Наведение** - Информация о типах и документация по ключевым словам
- **Переход к определению** - Навигация к определениям функций и переменных
- **Поиск ссылок** - Поиск всех ссылок на символ
- **Символы документа** - Представление структуры функций и определений
- **Автодополнение** - Предложения автодополнения символов

## Настройка редактора

### VS Code

Используйте [расширение Hemlock для VS Code](../editors/vscode/) или создайте `.vscode/settings.json`:

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

Или используйте любое универсальное расширение LSP-клиента с командой `hemlock lsp --stdio`.

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

## Отладка

Захватите логи сервера, перенаправив stderr:

```bash
hemlock lsp --stdio 2>lsp.log
```
