# HemlockScript: Hemlock → WASM via Emscripten

> Programas Hemlock portaveis que rodam no navegador.

## Objetivo

Adicionar um alvo de compilacao WASM ao `hemlockc` para que programas Hemlock possam rodar em navegadores e outros runtimes WASM (Node/Deno/Cloudflare Workers). A abordagem: compilar Hemlock → C (pipeline existente) → WASM (via Emscripten), com um shim de runtime compativel com navegador substituindo builtins apenas-POSIX.

**Nao-objetivo:** Reescrever o compilador ou runtime do zero. Aproveitamos o codegen C existente do `hemlockc` e o `libhemlock_runtime` o maximo possivel.

---

## Arquitetura

```
Fonte Hemlock (.hml)
        ↓
   hemlockc (frontend existente + codegen)
        ↓
   Codigo C gerado (existente)
        ↓
   emcc (Emscripten)  ←  libhemlock_runtime_wasm.a (runtime adaptado para WASM)
        ↓
   program.wasm + program.js (loader/glue)
        ↓
   Navegador / Node / Deno / runtime WASM
```

O insight chave: `hemlockc` ja emite C portavel. Nao precisamos de um novo backend -- precisamos de uma biblioteca de runtime compativel com WASM e um pipeline de build Emscripten.

---

## Fase 1: Build WASM Minimo (Apenas Linguagem Core)

**Resultado:** `make wasm` produz um bundle `.wasm` + `.js` que pode rodar programas Hemlock puramente computacionais no navegador.

### Entregaveis da Fase 1
- `make wasm-compile FILE=hello.hml` produz saida executavel no navegador
- Todos os recursos de computacao pura do Hemlock funcionam: variaveis, funcoes, closures, fluxo de controle, pattern matching, objetos, arrays, strings, matematica, sistema de tipos
- `print()` escreve no console do navegador / elemento HTML
- Recursos nao suportados (FFI, sockets, processos, sinais) encerram com mensagem clara

---

## Fase 2: I/O de Navegador e Stdlib

**Resultado:** Programas Hemlock podem fazer trabalho util no navegador -- acesso a arquivos (FS virtual), operacoes de tempo, e os modulos portaveis da stdlib funcionam.

### Entregaveis da Fase 2
- 22 modulos da stdlib funcionando em WASM
- Sistema de arquivos virtual para I/O de arquivos
- Funcoes de tempo funcionando
- `make wasm-test` executa testes da stdlib no runtime WASM do Node.js

---

## Fase 3: Bridge de Interop com JavaScript

**Resultado:** Programas WASM Hemlock podem chamar APIs do navegador e funcoes JavaScript, e JavaScript pode chamar funcoes Hemlock.

### Entregaveis da Fase 3
- Chamadas de funcao bidirecionais JS ↔ Hemlock
- Modulo `@wasm/browser` para APIs do navegador
- HTTP via fetch, WebSocket via WebSocket do navegador
- Criptografia via Web Crypto API
- Funcoes Hemlock exportadas chamaaveis do JS

---

## Fase 4: Async e Threading (Extensao)

**Resultado:** `spawn`/`await` do Hemlock funciona no navegador usando Web Workers.

### Entregaveis da Fase 4
- `spawn()` cria Web Workers
- Canais funcionam entre workers via SharedArrayBuffer
- `sleep()` e I/O bloqueante nao bloqueiam a thread principal

---

## O Que Funciona Imediatamente (Sem Mudancas Necessarias)

Estes recursos do Hemlock compilam para C padrao que o Emscripten trata nativamente:

- Todos os operadores aritmeticos, bit a bit, logicos
- Variaveis, escopos, closures
- Funcoes, recursao, funcoes com corpo de expressao
- if/else, while, for, loop, switch, pattern matching
- Objetos, arrays, strings (todos os 19+23 metodos)
- Anotacoes de tipo e verificacao de tipo em runtime
- Try/catch/finally/throw
- Defer
- Template strings
- Coalescencia nula (`??`, `?.`, `??=`)
- Argumentos nomeados
- Tipos compostos, aliases de tipo
- `print()`, `eprint()` (via mapeamento de console do Emscripten)
- `alloc()`/`free()`/`buffer()` (memoria linear)
- `typeof()`, `len()`, `sizeof()`
- Builtins matematicos (sin, cos, sqrt, etc.)
- Todo o gerenciamento de contagem de referencia / memoria

---

## Escopo Estimado por Fase

| Fase | Escopo | Dependencias |
|------|--------|--------------|
| **Fase 1** | ~800 linhas novo C, ~200 linhas guardas #ifdef, mudancas no Makefile | SDK Emscripten |
| **Fase 2** | ~200 linhas C, testes de stdlib, Makefile | Fase 1 |
| **Fase 3** | ~600 linhas C (bridge), ~200 linhas Hemlock (stdlib) | Fase 1 |
| **Fase 4** | ~1000 linhas C (threading Worker), complexo | Fase 1+3 |

Ordem recomendada: Fase 1 → Fase 2 → Fase 3 → Fase 4

A Fase 1 sozinha ja fornece um "Hemlock no navegador" util para cargas de trabalho computacionais. As Fases 2-4 adicionam I/O e interop incrementalmente.
