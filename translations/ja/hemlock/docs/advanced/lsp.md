# Language Server Protocol (LSP)

Hemlockには、IDE統合のためのリアルタイム診断、ナビゲーション、補完を提供する組み込みLSPサーバーが含まれています。

## サーバーの起動

```bash
hemlock lsp --stdio    # Stdioトランスポート（推奨）
hemlock lsp --tcp 5007 # 指定ポートでのTCPトランスポート
```

## 機能

- **診断** - リアルタイムの構文エラーと型チェック
- **ホバー** - 型情報とキーワードドキュメント
- **定義へ移動** - 関数と変数の定義へのナビゲーション
- **参照の検索** - シンボルのすべての参照を検索
- **ドキュメントシンボル** - 関数と定義のアウトラインビュー
- **補完** - シンボル補完の提案

## エディタ設定

### VS Code

[Hemlock VS Code拡張機能](../editors/vscode/)を使用するか、`.vscode/settings.json`を作成：

```json
{
  "hemlock.lsp.path": "/path/to/hemlock",
  "hemlock.lsp.args": ["lsp", "--stdio"]
}
```

または汎用LSPクライアント拡張機能でコマンド`hemlock lsp --stdio`を使用。

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

## デバッグ

stderrをリダイレクトしてサーバーログをキャプチャ：

```bash
hemlock lsp --stdio 2>lsp.log
```
