# Hemlock FFI (Interface de Funções Estrangeiras)

Hemlock oferece **FFI (Interface de Funções Estrangeiras)**, permitindo chamar funções C de bibliotecas compartilhadas usando libffi, possibilitando integração com bibliotecas C existentes e APIs do sistema.

## Índice

- [Visão Geral](#visão-geral)
- [Estado Atual](#estado-atual)
- [Tipos Suportados](#tipos-suportados)
- [Conceitos Básicos](#conceitos-básicos)
- [Exportando Funções FFI](#exportando-funções-ffi)
- [Casos de Uso](#casos-de-uso)
- [Desenvolvimento Futuro](#desenvolvimento-futuro)
- [Callbacks FFI](#callbacks-ffi)
- [Structs FFI](#structs-ffi)
- [Limitações Atuais](#limitações-atuais)
- [Melhores Práticas](#melhores-práticas)

## Visão Geral

A Interface de Funções Estrangeiras (FFI) permite que programas Hemlock:
- Chamem funções C de bibliotecas compartilhadas (.so, .dylib, .dll)
- Usem bibliotecas C existentes sem escrever código wrapper
- Acessem APIs do sistema diretamente
- Integrem com bibliotecas nativas de terceiros
- Façam ponte entre Hemlock e funcionalidade de baixo nível do sistema

**Capacidades Principais:**
- Carregamento dinâmico de bibliotecas
- Binding de funções C
- Conversão automática de tipos entre Hemlock e C
- Suporte a todos os tipos primitivos
- Implementação baseada em libffi para portabilidade

## Estado Atual

O suporte FFI em Hemlock possui as seguintes características:

**Implementado:**
- Chamar funções C de bibliotecas compartilhadas
- Suporte a todos os tipos primitivos (inteiros, floats, ponteiros)
- Conversão automática de tipos
- Implementação baseada em libffi
- Carregamento dinâmico de bibliotecas
- **Callbacks de ponteiro de função** - passar funções Hemlock para C
- **Exportar funções extern** - compartilhar bindings FFI entre módulos
- **Passagem e retorno de structs** - passar structs compatíveis com C por valor
- **Funções auxiliares de ponteiro completas** - ler/escrever todos os tipos (i8-i64, u8-u64, f32, f64, ptr)
- **Conversão buffer/ponteiro** - `buffer_ptr()`, `ptr_to_buffer()`
- **Tamanhos de tipo FFI** - `ffi_sizeof()` para tamanhos de tipo conscientes da plataforma
- **Tipos de plataforma** - suporte para `size_t`, `usize`, `isize`, `intptr_t`

**Em Desenvolvimento:**
- Helpers de marshaling de strings
- Melhorias no tratamento de erros

## Tipos Suportados

### Tipos Primitivos

Os seguintes tipos Hemlock podem ser passados para ou retornados de funções C:

| Tipo Hemlock | Tipo C | Tamanho | Descrição |
|--------------|--------|---------|-----------|
| `i8` | `int8_t` | 1 byte | Inteiro com sinal de 8 bits |
| `i16` | `int16_t` | 2 bytes | Inteiro com sinal de 16 bits |
| `i32` | `int32_t` | 4 bytes | Inteiro com sinal de 32 bits |
| `i64` | `int64_t` | 8 bytes | Inteiro com sinal de 64 bits |
| `u8` | `uint8_t` | 1 byte | Inteiro sem sinal de 8 bits |
| `u16` | `uint16_t` | 2 bytes | Inteiro sem sinal de 16 bits |
| `u32` | `uint32_t` | 4 bytes | Inteiro sem sinal de 32 bits |
| `u64` | `uint64_t` | 8 bytes | Inteiro sem sinal de 64 bits |
| `f32` | `float` | 4 bytes | Ponto flutuante de 32 bits |
| `f64` | `double` | 8 bytes | Ponto flutuante de 64 bits |
| `ptr` | `void*` | 8 bytes | Ponteiro bruto |

### Conversão de Tipos

**Conversão Automática:**
- Inteiros Hemlock -> Inteiros C (com verificação de range)
- Floats Hemlock -> Floats C
- Ponteiros Hemlock -> Ponteiros C
- Valores de retorno C -> Valores Hemlock

**Exemplos de Mapeamento de Tipos:**
```hemlock
// Hemlock -> C
let i: i32 = 42;         // -> int32_t (4 bytes)
let f: f64 = 3.14;       // -> double (8 bytes)
let p: ptr = alloc(64);  // -> void* (8 bytes)

// C -> Hemlock (valores de retorno)
// int32_t foo() -> i32
// double bar() -> f64
// void* baz() -> ptr
```

## Conceitos Básicos

### Bibliotecas Compartilhadas

FFI trabalha com bibliotecas compartilhadas compiladas:

**Linux:** arquivos `.so`
```
libexample.so
/usr/lib/libm.so
```

**macOS:** arquivos `.dylib`
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** arquivos `.dll`
```
example.dll
kernel32.dll
```

### Assinaturas de Função

Funções C devem ter assinaturas conhecidas para que FFI funcione:

```c
// Exemplos de assinaturas de funções C
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

Uma vez que a biblioteca é carregada e funções são vinculadas, elas podem ser chamadas do Hemlock.

### Compatibilidade de Plataforma

FFI usa **libffi** para portabilidade:
- Funciona em x86, x86-64, ARM, ARM64
- Trata convenções de chamada automaticamente
- Abstrai detalhes de ABI específicos da plataforma
- Suporta Linux, macOS, Windows (com libffi apropriada)

## Exportando Funções FFI

Funções FFI declaradas com `extern fn` podem ser exportadas de módulos, permitindo criar wrappers de biblioteca reutilizáveis que podem ser compartilhados entre múltiplos arquivos.

### Sintaxe Básica de Exportação

```hemlock
// string_utils.hml - módulo de biblioteca wrapping funções de string C
import "libc.so.6";

// Exportar funções extern diretamente
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// Você também pode exportar funções wrapper junto com funções extern
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### Importando Funções FFI Exportadas

```hemlock
// main.hml - usando funções FFI exportadas
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hello, World!";
print(strlen(msg));           // 13 - chamada extern direta
print(string_length(msg));    // 13 - função wrapper

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### Casos de Uso para Export Extern

**1. Abstração de Plataforma**
```hemlock
// platform.hml - abstrair diferenças de plataforma
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. Wrappers de Biblioteca**
```hemlock
// crypto_lib.hml - wrapping funções de biblioteca de criptografia
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Adicionar wrappers amigáveis ao Hemlock
export fn sha256_string(s: string): string {
    // Implementação usando funções extern
}
```

**3. Declarações FFI Centralizadas**
```hemlock
// libc.hml - módulo central para bindings libc
import "libc.so.6";

// Funções de string
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// Funções de memória
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// Funções de processo
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

Então use em todo o seu projeto:
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

## Casos de Uso

### 1. Bibliotecas do Sistema

Acessar funções da biblioteca C padrão:

**Funções Matemáticas:**
```hemlock
// Chamar sqrt de libm
let result = sqrt(16.0);  // 4.0
```

**Alocação de Memória:**
```hemlock
// Chamar malloc/free de libc
let ptr = malloc(1024);
free(ptr);
```

### 2. Bibliotecas de Terceiros

Usar bibliotecas C existentes:

**Exemplo: Processamento de Imagem**
```hemlock
// Carregar libpng ou libjpeg
// Processar imagens usando funções de biblioteca C
```

**Exemplo: Criptografia**
```hemlock
// Usar OpenSSL ou libsodium
// Criptografia/descriptografia via FFI
```

### 3. APIs do Sistema

Chamadas diretas ao sistema:

**Exemplo: API POSIX**
```hemlock
// Chamar getpid, getuid, etc.
// Acessar funcionalidade de baixo nível do sistema
```

### 4. Código Crítico para Desempenho

Chamar implementações C otimizadas:

```hemlock
// Usar bibliotecas C altamente otimizadas
// Operações SIMD, código vetorizado
// Funções aceleradas por hardware
```

## Callbacks FFI

Hemlock suporta passar funções como callbacks para código C usando closures libffi. Isso permite integração com APIs C que esperam ponteiros de função, como `qsort`, event loops e bibliotecas baseadas em callback.

### Criando Callbacks

Use `callback()` para criar um ponteiro de função chamável por C a partir de uma função Hemlock:

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**Parâmetros:**
- `function`: A função Hemlock a ser wrapped
- `param_types`: Array de strings de nomes de tipo (como `["ptr", "i32"]`)
- `return_type`: String de tipo de retorno (como `"i32"`, `"void"`)

**Tipos de Callback Suportados:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Inteiros com sinal
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Inteiros sem sinal
- `"f32"`, `"f64"` - Floats
- `"ptr"` - Ponteiros
- `"void"` - Sem retorno
- `"bool"` - Booleano

### Exemplo: qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// Função de comparação de inteiros (ordem crescente)
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// Alocar array de 5 inteiros
let arr = alloc(20);  // 5 * 4 bytes
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// Criar callback e ordenar
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// Array agora ordenado: [1, 2, 5, 8, 9]

// Limpar
callback_free(cmp);
free(arr);
```

### Funções Auxiliares de Ponteiro

Hemlock fornece funções auxiliares abrangentes para trabalhar com ponteiros brutos. Estas são essenciais para callbacks FFI e manipulação direta de memória.

#### Auxiliares de Tipo Inteiro

| Função | Descrição |
|--------|-----------|
| `ptr_deref_i8(ptr)` | Desreferenciar ponteiro, ler i8 |
| `ptr_deref_i16(ptr)` | Desreferenciar ponteiro, ler i16 |
| `ptr_deref_i32(ptr)` | Desreferenciar ponteiro, ler i32 |
| `ptr_deref_i64(ptr)` | Desreferenciar ponteiro, ler i64 |
| `ptr_deref_u8(ptr)` | Desreferenciar ponteiro, ler u8 |
| `ptr_deref_u16(ptr)` | Desreferenciar ponteiro, ler u16 |
| `ptr_deref_u32(ptr)` | Desreferenciar ponteiro, ler u32 |
| `ptr_deref_u64(ptr)` | Desreferenciar ponteiro, ler u64 |
| `ptr_write_i8(ptr, value)` | Escrever i8 na localização do ponteiro |
| `ptr_write_i16(ptr, value)` | Escrever i16 na localização do ponteiro |
| `ptr_write_i32(ptr, value)` | Escrever i32 na localização do ponteiro |
| `ptr_write_i64(ptr, value)` | Escrever i64 na localização do ponteiro |
| `ptr_write_u8(ptr, value)` | Escrever u8 na localização do ponteiro |
| `ptr_write_u16(ptr, value)` | Escrever u16 na localização do ponteiro |
| `ptr_write_u32(ptr, value)` | Escrever u32 na localização do ponteiro |
| `ptr_write_u64(ptr, value)` | Escrever u64 na localização do ponteiro |

#### Auxiliares de Tipo Float

| Função | Descrição |
|--------|-----------|
| `ptr_deref_f32(ptr)` | Desreferenciar ponteiro, ler f32 (float) |
| `ptr_deref_f64(ptr)` | Desreferenciar ponteiro, ler f64 (double) |
| `ptr_write_f32(ptr, value)` | Escrever f32 na localização do ponteiro |
| `ptr_write_f64(ptr, value)` | Escrever f64 na localização do ponteiro |

#### Auxiliares de Tipo Ponteiro

| Função | Descrição |
|--------|-----------|
| `ptr_deref_ptr(ptr)` | Desreferenciar ponteiro para ponteiro |
| `ptr_write_ptr(ptr, value)` | Escrever ponteiro na localização do ponteiro |
| `ptr_offset(ptr, index, size)` | Calcular offset: `ptr + index * size` |
| `ptr_read_i32(ptr)` | Ler i32 via ponteiro para ponteiro (para callbacks qsort) |
| `ptr_null()` | Obter constante ponteiro nulo |

#### Auxiliares de Conversão Buffer

| Função | Descrição |
|--------|-----------|
| `buffer_ptr(buffer)` | Obter ponteiro bruto de buffer |
| `ptr_to_buffer(ptr, size)` | Copiar dados de ponteiro para novo buffer |

#### Utilitários FFI

| Função | Descrição |
|--------|-----------|
| `ffi_sizeof(type_name)` | Obter tamanho em bytes de tipo FFI |

**Nomes de tipo suportados por `ffi_sizeof`:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Inteiros com sinal (1, 2, 4, 8 bytes)
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Inteiros sem sinal (1, 2, 4, 8 bytes)
- `"f32"`, `"f64"` - Floats (4, 8 bytes)
- `"ptr"` - Ponteiro (8 bytes em sistemas 64-bit)
- `"size_t"`, `"usize"` - Tipo de tamanho dependente da plataforma
- `"intptr_t"`, `"isize"` - Tipo de ponteiro com sinal dependente da plataforma

### Liberando Callbacks

**Importante:** Sempre libere callbacks após o uso para prevenir vazamentos de memória:

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ... usar callback ...
callback_free(cb);  // Liberar quando terminar de usar
```

Callbacks também são liberados automaticamente na saída do programa.

### Closures em Callbacks

Callbacks capturam seu ambiente de closure, então podem acessar variáveis do escopo externo:

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // Pode acessar 'multiplier' do escopo externo
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### Segurança de Thread

Invocações de callback são serializadas via mutex para garantir segurança de thread, pois o interpretador Hemlock não é completamente thread-safe. Isso significa:
- Apenas um callback pode executar por vez
- Seguro para usar com bibliotecas C multi-threaded
- Pode impactar desempenho se callbacks são chamados frequentemente de múltiplas threads

### Tratamento de Erros em Callbacks

Exceções lançadas em callbacks não podem propagar para código C. Em vez disso:
- Um aviso é impresso em stderr
- O callback retorna um valor padrão (0 ou NULL)
- A exceção é registrada mas não propagada

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Something went wrong";  // Imprime aviso, retorna 0
}
```

Para tratamento de erros robusto, valide entradas e evite lançar em callbacks.

## Structs FFI

Hemlock suporta passar structs por valor para funções C. Tipos de struct são automaticamente registrados para FFI quando você os define com anotações de tipo.

### Definindo Structs Compatíveis com FFI

Uma struct é compatível com FFI quando todos os campos têm anotações de tipo explícitas usando tipos compatíveis com FFI:

```hemlock
// Struct compatível com FFI
define Point {
    x: f64,
    y: f64,
}

// Struct compatível com FFI com múltiplos tipos de campo
define Rectangle {
    top_left: Point,      // Struct aninhada
    width: f64,
    height: f64,
}

// NÃO é compatível com FFI (campos sem anotações de tipo)
define DynamicObject {
    name,                 // Sem tipo - não pode usar para FFI
    value,
}
```

### Usando Structs com FFI

Declare funções extern que usam tipos de struct:

```hemlock
// Definir tipo de struct
define Vector2D {
    x: f64,
    y: f64,
}

// Importar biblioteca C
import "libmath.so";

// Declarar funções extern que aceitam/retornam structs
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// Usar naturalmente
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### Tipos de Campo Suportados

Campos de struct devem usar estes tipos compatíveis com FFI:

| Tipo Hemlock | Tipo C | Tamanho |
|--------------|--------|---------|
| `i8` | `int8_t` | 1 byte |
| `i16` | `int16_t` | 2 bytes |
| `i32` | `int32_t` | 4 bytes |
| `i64` | `int64_t` | 8 bytes |
| `u8` | `uint8_t` | 1 byte |
| `u16` | `uint16_t` | 2 bytes |
| `u32` | `uint32_t` | 4 bytes |
| `u64` | `uint64_t` | 8 bytes |
| `f32` | `float` | 4 bytes |
| `f64` | `double` | 8 bytes |
| `ptr` | `void*` | 8 bytes |
| `string` | `char*` | 8 bytes |
| `bool` | `int` | Variável |
| Struct aninhada | struct | Variável |

### Layout de Struct

Hemlock usa as regras de layout de struct nativo da plataforma (correspondendo ao ABI C):
- Campos são alinhados pelo seu tipo
- Padding é inserido conforme necessário
- Tamanho total é padded para alinhar com o maior membro

```hemlock
// Exemplo: Layout compatível com C
define Mixed {
    a: i8,    // Offset 0, tamanho 1
              // 3 bytes de padding
    b: i32,   // Offset 4, tamanho 4
}
// Tamanho total: 8 bytes (incluindo padding)

define Point3D {
    x: f64,   // Offset 0, tamanho 8
    y: f64,   // Offset 8, tamanho 8
    z: f64,   // Offset 16, tamanho 8
}
// Tamanho total: 24 bytes (sem padding necessário)
```

### Structs Aninhadas

Structs podem conter outras structs:

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### Retorno de Struct

Funções C podem retornar structs:

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### Limitações

- **Campos de struct devem ter anotações de tipo** - Campos sem tipo não são compatíveis com FFI
- **Sem arrays em structs** - Use ponteiros em vez disso
- **Sem unions** - Apenas tipos de struct são suportados
- **Callbacks não podem retornar structs** - Use ponteiros para valores de retorno de callback

## Limitações Atuais

FFI tem as seguintes limitações:

**1. Conversão de Tipo Manual**
- Conversão de string deve ser gerenciada manualmente
- Sem conversão automática Hemlock string <-> C string

**2. Tratamento de Erros Limitado**
- Relatório de erros básico
- Exceções em callbacks não podem propagar para C

**3. Carregamento Manual de Biblioteca**
- Bibliotecas devem ser carregadas manualmente
- Sem geração automática de bindings

**4. Código Específico de Plataforma**
- Caminhos de biblioteca variam por plataforma
- Deve tratar .so vs .dylib vs .dll

## Melhores Práticas

Embora documentação abrangente de FFI ainda esteja em desenvolvimento, aqui estão melhores práticas gerais:

### 1. Segurança de Tipos

```hemlock
// Seja explícito sobre tipos
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. Gerenciamento de Memória

```hemlock
// Lembre de liberar memória alocada
let ptr = c_malloc(1024);
// ... usar ptr
c_free(ptr);
```

### 3. Verificação de Erros

```hemlock
// Verifique valores de retorno
let result = c_function();
if (result == null) {
    print("C function failed");
}
```

### 4. Compatibilidade de Plataforma

```hemlock
// Trate diferenças de plataforma
// Use extensões de biblioteca apropriadas (.so, .dylib, .dll)
```

## Resumo

O FFI do Hemlock oferece:

- Chamar funções C de bibliotecas compartilhadas
- Suporte a tipos primitivos (i8-i64, u8-u64, f32, f64, ptr)
- Conversão automática de tipos
- Portabilidade baseada em libffi
- Base para integração com bibliotecas nativas
- **Callbacks de ponteiro de função** - passar funções Hemlock para C
- **Exportar funções extern** - compartilhar bindings FFI entre módulos
- **Passagem e retorno de struct** - passar structs compatíveis com C por valor
- **Exportar define** - compartilhar definições de tipo struct entre módulos (importados globalmente automaticamente)
- **Funções auxiliares de ponteiro completas** - ler/escrever todos os tipos (i8-i64, u8-u64, f32, f64, ptr)
- **Conversão buffer/ponteiro** - `buffer_ptr()`, `ptr_to_buffer()` para marshaling de dados
- **Tamanhos de tipo FFI** - `ffi_sizeof()` para tamanhos de tipo conscientes da plataforma
- **Tipos de plataforma** - suporte para `size_t`, `usize`, `isize`, `intptr_t`, `uintptr_t`

**Estado Atual:** FFI é funcionalmente completo com suporte a tipos primitivos, structs, callbacks, exportações de módulo e funções auxiliares de ponteiro completas

**Futuro:** Helpers de marshaling de strings

**Casos de Uso:** Bibliotecas de sistema, bibliotecas de terceiros, qsort, event loops, APIs baseadas em callback, wrappers de biblioteca reutilizáveis
