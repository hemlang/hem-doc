# Sistema de Módulos do Hemlock

Este documento descreve o sistema de módulos import/export no estilo ES6 implementado para Hemlock.

## Visao Geral

Hemlock suporta um sistema de módulos baseado em arquivos usando sintaxe de import/export no estilo ES6. Módulos têm as seguintes características:
- **Singleton**: Cada módulo é carregado apenas uma vez e armazenado em cache
- **Baseado em arquivo**: Módulos correspondem a arquivos .hml no disco
- **Imports explícitos**: Dependências são declaradas através de declarações import
- **Execução topológica**: Dependências executam antes dos dependentes

Para gerenciamento de pacotes e dependências de terceiros, veja [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Sintaxe

### Declarações Export

**Exports nomeados inline:**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let contador = 0;
```

**Lista de exports:**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Exportando Extern (funções FFI):**
```hemlock
import "libc.so.6";

// Exporta funções FFI para uso de outros módulos
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

Para mais detalhes sobre exportar funções FFI, veja a [documentação FFI](../advanced/ffi.md#exporting-ffi-functions).

**Exportando Define (tipos struct):**
```hemlock
// Exporta definições de tipo struct
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**Nota importante:** Tipos struct exportados são registrados globalmente quando o módulo é carregado. Eles ficam automaticamente disponíveis quando você importa qualquer coisa do módulo - você não precisa (e não pode) importá-los explicitamente por nome:

```hemlock
// Correto - tipos struct ficam disponíveis automaticamente após qualquer import
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Funciona!

// Errado - não pode importar tipos struct explicitamente
import { Vector2 } from "./my_module.hml";  // Erro: variável 'Vector2' indefinida
```

Para mais detalhes sobre exportar tipos struct, veja a [documentação FFI](../advanced/ffi.md#exporting-struct-types).

**Re-exports:**
```hemlock
// Re-exporta de outro módulo
export { add, subtract } from "./math.hml";
```

### Declarações Import

**Imports nomeados:**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Import de namespace:**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**Aliases:**
```hemlock
import { add as soma, subtract as subtrair } from "./math.hml";
print(soma(1, 2));  // 3
```

## Resolução de Módulos

### Tipos de Caminho

**Caminhos relativos:**
```hemlock
import { foo } from "./module.hml";       // Mesmo diretório
import { bar } from "../parent.hml";      // Diretório pai
import { baz } from "./sub/nested.hml";   // Subdiretório
```

**Caminhos absolutos:**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Tratamento de extensão:**
- Extensão `.hml` pode ser omitida - será adicionada automaticamente
- `./math` resolve para `./math.hml`

## Recursos

### Detecção de Dependência Circular

O sistema de módulos detecta dependências circulares e reporta erros:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Cache de Módulos

Módulos são carregados apenas uma vez e armazenados em cache. Múltiplos imports do mesmo módulo retornam a mesma instância:

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // Mesma instância!
print(count);  // Ainda 1 (estado compartilhado)
```

### Imutabilidade de Imports

Bindings importados não podem ser reatribuídos:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // Erro: não pode reatribuir binding importado
```

## Detalhes de Implementação

### Arquitetura

**Arquivos:**
- `include/module.h` - API do sistema de módulos
- `src/module.c` - Carregamento, cache e execução de módulos
- Suporte de parser em `src/parser.c`
- Suporte de runtime em `src/interpreter/runtime.c`

**Componentes principais:**
1. **ModuleCache**: Mantém módulos carregados indexados por caminho absoluto
2. **Module**: Representa um módulo carregado com AST e exports
3. **Resolução de caminho**: Resolve caminhos relativos/absolutos para caminhos canônicos
4. **Execução topológica**: Executa módulos em ordem de dependência

### Processo de Carregamento de Módulos

1. **Fase de parse**: Análise léxica e sintática do arquivo de módulo
2. **Resolução de dependências**: Carrega recursivamente módulos importados
3. **Detecção de ciclos**: Verifica se módulo já está sendo carregado
4. **Caching**: Armazena módulo no cache por caminho absoluto
5. **Fase de execução**: Executa em ordem topológica (dependências primeiro)

### API

```c
// API de alto nível
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// API de baixo nível
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Testes

Módulos de teste estão localizados em `tests/modules/` e `tests/parity/modules/`:

- `math.hml` - Módulo básico com exports
- `test_import_named.hml` - Teste de imports nomeados
- `test_import_namespace.hml` - Teste de import de namespace
- `test_import_alias.hml` - Teste de alias de import
- `export_extern.hml` - Teste de export de funções FFI extern (Linux)

## Imports de Pacotes (hpm)

Com [hpm](https://github.com/hemlang/hpm) instalado, você pode importar pacotes de terceiros do GitHub:

```hemlock
// Importa da raiz do pacote (usando "main" do package.json)
import { app, router } from "hemlang/sprout";

// Importa de subcaminho
import { middleware } from "hemlang/sprout/middleware";

// Biblioteca padrão (embutida no Hemlock)
import { HashMap } from "@stdlib/collections";
```

Pacotes são instalados em `hem_modules/` e resolvidos usando sintaxe `owner/repo` do GitHub.

```bash
# Instalar pacote
hpm install hemlang/sprout

# Instalar com restrição de versão
hpm install hemlang/sprout@^1.0.0
```

Para detalhes completos, veja a [documentação do hpm](https://github.com/hemlang/hpm).

## Limitações Atuais

1. **Sem imports dinâmicos**: `import()` como função de runtime não é suportado
2. **Sem exports condicionais**: Exports devem estar no nível superior
3. **Caminhos de biblioteca estáticos**: Imports de biblioteca FFI usam caminhos estáticos (específicos de plataforma)

## Trabalho Futuro

- Imports dinâmicos usando função `import()`
- Exports condicionais
- Metadados de módulo (`import.meta`)
- Tree shaking e eliminação de código morto

## Exemplos

Para exemplos funcionais do sistema de módulos, veja `tests/modules/`.

Estrutura de módulo de exemplo:
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (módulo barrel)
└── utils/
    └── helpers.hml
```

Uso de exemplo:
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
