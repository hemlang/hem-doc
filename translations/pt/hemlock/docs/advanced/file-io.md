# Hemlock E/S de Arquivos

Hemlock oferece uma **API de objetos de arquivo** para operações com arquivos, com tratamento de erros apropriado e gerenciamento de recursos.

## Índice

- [Visão Geral](#visão-geral)
- [Abrindo Arquivos](#abrindo-arquivos)
- [Métodos de Arquivo](#métodos-de-arquivo)
- [Propriedades de Arquivo](#propriedades-de-arquivo)
- [Tratamento de Erros](#tratamento-de-erros)
- [Gerenciamento de Recursos](#gerenciamento-de-recursos)
- [Referência Completa da API](#referência-completa-da-api)
- [Padrões Comuns](#padrões-comuns)
- [Melhores Práticas](#melhores-práticas)

## Visão Geral

A API de objetos de arquivo oferece:

- **Gerenciamento explícito de recursos** - arquivos devem ser fechados manualmente
- **Múltiplos modos de abertura** - leitura, escrita, append, leitura+escrita
- **Operações de texto e binário** - ler e escrever dados de texto e binários
- **Suporte a posicionamento** - acesso aleatório dentro de arquivos
- **Mensagens de erro abrangentes** - relatório de erros com contexto

**Importante:** Arquivos não são fechados automaticamente. Você deve chamar `f.close()` para evitar vazamentos de descritores de arquivo.

## Abrindo Arquivos

Use `open(path, mode?)` para abrir um arquivo:

```hemlock
let f = open("data.txt", "r");     // Modo leitura (padrão)
let f2 = open("output.txt", "w");  // Modo escrita (trunca)
let f3 = open("log.txt", "a");     // Modo append
let f4 = open("data.bin", "r+");   // Modo leitura+escrita
```

### Modos de Abertura

| Modo | Descrição | Arquivo Deve Existir | Trunca | Posição |
|------|-----------|---------------------|--------|---------|
| `"r"` | Leitura (padrão) | Sim | Não | Início |
| `"w"` | Escrita | Não (cria) | Sim | Início |
| `"a"` | Append | Não (cria) | Não | Final |
| `"r+"` | Leitura+Escrita | Sim | Não | Início |
| `"w+"` | Leitura+Escrita | Não (cria) | Sim | Início |
| `"a+"` | Leitura e Append | Não (cria) | Não | Final |

### Exemplos

**Ler arquivo existente:**
```hemlock
let f = open("config.json", "r");
// Ou simplesmente:
let f = open("config.json");  // "r" é o padrão
```

**Criar novo arquivo para escrita:**
```hemlock
let f = open("output.txt", "w");  // Cria ou trunca
```

**Adicionar ao arquivo:**
```hemlock
let f = open("log.txt", "a");  // Cria se não existir
```

**Modo leitura+escrita:**
```hemlock
let f = open("data.bin", "r+");  // Arquivo existente, pode ler e escrever
```

## Métodos de Arquivo

### Leitura

#### read(size?: i32): string

Lê texto do arquivo (parâmetro size opcional).

**Sem size (lê tudo):**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // Lê da posição atual até EOF
f.close();
```

**Com size (lê bytes especificados):**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // Lê até 1024 bytes
let next = f.read(1024);   // Lê próximos 1024 bytes
f.close();
```

**Retorna:** String contendo os dados lidos, ou string vazia se no EOF

**Exemplo - Ler arquivo inteiro:**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**Exemplo - Ler em chunks:**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // Chunks de 4KB
    if (chunk == "") { break; }  // Chegou ao EOF
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

Lê dados binários (retorna buffer).

**Parâmetros:**
- `size` (i32) - número de bytes a ler

**Retorna:** Buffer contendo os bytes lidos

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // Lê 256 bytes
print(binary.length);  // 256 (ou menos se EOF)

// Acessar bytes individuais
let first_byte = binary[0];
print(first_byte);

f.close();
```

### Escrita

#### write(data: string): i32

Escreve texto no arquivo (retorna bytes escritos).

**Parâmetros:**
- `data` (string) - texto a escrever

**Retorna:** Número de bytes escritos (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hello, World!\n");
print("Wrote " + typeof(written) + " bytes");  // "Wrote 14 bytes"
f.close();
```

**Exemplo - Escrever múltiplas linhas:**
```hemlock
let f = open("output.txt", "w");
f.write("Line 1\n");
f.write("Line 2\n");
f.write("Line 3\n");
f.close();
```

**Exemplo - Adicionar ao arquivo de log:**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Application started\n");
f.write("[INFO] User logged in\n");
f.close();
```

#### write_bytes(data: buffer): i32

Escreve dados binários (retorna bytes escritos).

**Parâmetros:**
- `data` (buffer) - dados binários a escrever

**Retorna:** Número de bytes escritos (i32)

```hemlock
let f = open("output.bin", "w");

// Criar dados binários
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Wrote " + typeof(bytes) + " bytes");

f.close();
```

### Posicionamento

#### seek(position: i32): i32

Move para posição especificada (retorna nova posição).

**Parâmetros:**
- `position` (i32) - offset em bytes desde o início do arquivo

**Retorna:** Nova posição (i32)

```hemlock
let f = open("data.txt", "r");

// Mover para byte 100
f.seek(100);

// Ler da posição 100
let data = f.read(50);

// Resetar para o início
f.seek(0);

f.close();
```

**Exemplo - Acesso aleatório:**
```hemlock
let f = open("records.dat", "r");

// Ler registro no offset 1000
f.seek(1000);
let record1 = f.read_bytes(100);

// Ler registro no offset 2000
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Obtém posição atual no arquivo.

**Retorna:** Offset atual em bytes (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0 (no início)

f.read(100);
let pos2 = f.tell();  // 100 (após ler 100 bytes)

f.seek(500);
let pos3 = f.tell();  // 500 (após seek)

f.close();
```

### Fechamento

#### close()

Fecha o arquivo (idempotente, pode ser chamado múltiplas vezes).

```hemlock
let f = open("data.txt", "r");
// ... usar arquivo
f.close();
f.close();  // Seguro - segundo close não causa erro
```

**Notas importantes:**
- Sempre feche arquivos após o uso para evitar vazamentos de descritores
- Close é idempotente - pode ser chamado múltiplas vezes com segurança
- Após fechar, todas as outras operações causarão erro
- Use blocos `finally` para garantir que arquivos sejam fechados mesmo em caso de erro

## Propriedades de Arquivo

Objetos de arquivo têm três propriedades somente-leitura:

### path: string

O caminho do arquivo usado para abrir o arquivo.

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

O modo com que o arquivo foi aberto.

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Se o arquivo está fechado.

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Exemplo - Verificar se arquivo está aberto:**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... usar conteúdo
}

f.close();

if (f.closed) {
    print("File is now closed");
}
```

## Tratamento de Erros

Todas as operações de arquivo incluem mensagens de erro apropriadas com contexto.

### Erros Comuns

**Arquivo não encontrado:**
```hemlock
let f = open("missing.txt", "r");
// Erro: Failed to open 'missing.txt': No such file or directory
```

**Ler de arquivo fechado:**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Erro: Cannot read from closed file 'data.txt'
```

**Escrever em arquivo somente-leitura:**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Erro: Cannot write to file 'readonly.txt' opened in read-only mode
```

**Ler de arquivo somente-escrita:**
```hemlock
let f = open("output.txt", "w");
f.read();
// Erro: Cannot read from file 'output.txt' opened in write-only mode
```

### Usando try/catch

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Error reading file: " + e);
}
```

## Gerenciamento de Recursos

### Padrão Básico

Sempre feche arquivos explicitamente:

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Com Tratamento de Erros (Recomendado)

Use `finally` para garantir que arquivos sejam fechados mesmo em caso de erro:

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Sempre fecha, mesmo em caso de erro
}
```

### Múltiplos Arquivos

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Padrão com Função Auxiliar

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Uso:
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## Referência Completa da API

### Funções

| Função | Parâmetros | Retorno | Descrição |
|--------|------------|---------|-----------|
| `open(path, mode?)` | path: string, mode?: string | File | Abre arquivo (modo padrão "r") |

### Métodos

| Método | Parâmetros | Retorno | Descrição |
|--------|------------|---------|-----------|
| `read(size?)` | size?: i32 | string | Lê texto (tudo ou bytes especificados) |
| `read_bytes(size)` | size: i32 | buffer | Lê dados binários |
| `write(data)` | data: string | i32 | Escreve texto, retorna bytes escritos |
| `write_bytes(data)` | data: buffer | i32 | Escreve dados binários, retorna bytes escritos |
| `seek(position)` | position: i32 | i32 | Posiciona na posição, retorna nova posição |
| `tell()` | - | i32 | Obtém posição atual |
| `close()` | - | null | Fecha arquivo (idempotente) |

### Propriedades (Somente Leitura)

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `path` | string | Caminho do arquivo |
| `mode` | string | Modo de abertura |
| `closed` | bool | Se o arquivo está fechado |

## Padrões Comuns

### Ler Arquivo Inteiro

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### Escrever Arquivo Inteiro

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hello, World!");
```

### Adicionar ao Arquivo

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Event occurred\n");
```

### Ler Linhas

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Line " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Processar Arquivo Grande em Chunks

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // Chunks de 4KB
            if (chunk == "") { break; }

            // Processar chunk
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Copiar Arquivo Binário

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### Truncar Arquivo

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // Modo "w" trunca
    f.close();
}

truncate_file("empty_me.txt");
```

### Leitura com Acesso Aleatório

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

## Melhores Práticas

### 1. Sempre Use try/finally

```hemlock
// Bom
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// Ruim - arquivo pode não fechar em caso de erro
let f = open("data.txt", "r");
let content = f.read();
process(content);  // Se isso lançar, arquivo vaza
f.close();
```

### 2. Verifique Estado do Arquivo Antes de Operações

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... usar conteúdo
}

f.close();
```

### 3. Use o Modo Apropriado

```hemlock
// Apenas leitura? Use "r"
let f = open("config.json", "r");

// Substituir completamente? Use "w"
let f = open("output.txt", "w");

// Adicionar ao final? Use "a"
let f = open("log.txt", "a");
```

### 4. Trate Erros Graciosamente

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Warning: Could not read " + path + ": " + e);
        return "";
    }
}
```

### 5. Feche Arquivos na Ordem Inversa de Abertura

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... usar arquivos
} finally {
    // Fechar na ordem inversa
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Evite Ler Arquivos Grandes Completamente

```hemlock
// Ruim para arquivos grandes
let f = open("huge.log", "r");
let content = f.read();  // Carrega arquivo inteiro na memória
f.close();

// Bom - processar em chunks
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Resumo

A API de E/S de arquivos do Hemlock oferece:

- Operações de arquivo simples e explícitas
- Suporte a texto e binário
- Acesso aleatório com seek/tell
- Mensagens de erro claras com contexto
- Operação close idempotente

Lembre-se:
- Sempre feche arquivos manualmente
- Use try/finally para garantir segurança de recursos
- Escolha o modo de abertura apropriado
- Trate erros graciosamente
- Processe arquivos grandes em chunks
