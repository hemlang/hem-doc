# 语言服务器协议（LSP）

Hemlock 包含内置 LSP 服务器，用于 IDE 集成，提供实时诊断、导航和代码补全。

## 启动服务器

```bash
hemlock lsp --stdio    # Stdio 传输（推荐）
hemlock lsp --tcp 5007 # TCP 传输，指定端口
```

## 功能

- **诊断** - 实时语法错误和类型检查
- **悬停** - 类型信息和关键字文档
- **跳转到定义** - 导航到函数和变量的定义
- **查找引用** - 查找符号的所有引用
- **文档符号** - 函数和定义的大纲视图
- **代码补全** - 符号补全建议

## 编辑器配置

### VS Code

使用 [Hemlock VS Code 扩展](../editors/vscode/) 或创建 `.vscode/settings.json`：

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

或使用任何通用 LSP 客户端扩展，命令为 `hemlock lsp --stdio`。

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

## 调试

通过重定向 stderr 来捕获服务器日志：

```bash
hemlock lsp --stdio 2>lsp.log
```
