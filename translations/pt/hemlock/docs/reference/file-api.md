# Referencia da API de Arquivos

Documentacao completa do sistema de I/O de arquivos do Hemlock.

---

## Visao Geral

Hemlock fornece uma **API de objeto de arquivo** para operacoes de arquivo com tratamento de erros e gerenciamento de recursos adequados. Arquivos devem ser abertos e fechados manualmente.

**Caracteristicas Principais:**
- Objetos de arquivo com metodos
- Leitura e escrita de texto e dados binarios
- Operacoes de posicionamento
- Mensagens de erro adequadas
- Gerenciamento manual de recursos (sem RAII)

---

## Tipo File

**Tipo:** `file`

**Descricao:** Handle de arquivo para operacoes de I/O

**Propriedades (somente leitura):**
- `.path` - Caminho do arquivo (string)
- `.mode` - Modo de abertura (string)
- `.closed` - Se o arquivo esta fechado (bool)

---

## Abrindo Arquivos

### open

Abre um arquivo para leitura, escrita ou ambos.

**Assinatura:**
```hemlock
open(path: string, mode?: string): file
```

**Parametros:**
- `path` - Caminho do arquivo (relativo ou absoluto)
- `mode` (opcional) - Modo de abertura (padrao: `"r"`)

**Retorna:** Objeto de arquivo

**Modos:**
- `"r"` - Leitura (padrao)
- `"w"` - Escrita (trunca arquivo existente)
- `"a"` - Acrescentar
- `"r+"` - Leitura e escrita
- `"w+"` - Leitura e escrita (trunca)
- `"a+"` - Leitura e acrescentar

**Exemplo:**
```hemlock
// Modo de leitura (padrao)
let f = open("data.txt");
let f_read = open("data.txt", "r");

// Modo de escrita (trunca)
let f_write = open("output.txt", "w");

// Modo de acrescentar
let f_append = open("log.txt", "a");

// Modo de leitura e escrita
let f_rw = open("data.bin", "r+");

// Leitura e escrita (trunca)
let f_rw_trunc = open("output.bin", "w+");

// Leitura e acrescentar
let f_ra = open("log.txt", "a+");
```

**Tratamento de Erros:**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Falha ao abrir:", e);
    // Erro: Failed to open 'missing.txt': No such file or directory
}
```

**Importante:** Arquivos devem ser fechados manualmente usando `f.close()` para evitar vazamento de descritores de arquivo.

---

## Metodos de Arquivo

### Leitura

#### read

Le texto de um arquivo.

**Assinatura:**
```hemlock
file.read(size?: i32): string
```

**Parametros:**
- `size` (opcional) - Numero de bytes a ler (se omitido, le ate o fim do arquivo)

**Retorna:** String contendo o conteudo do arquivo

**Exemplo:**
```hemlock
let f = open("data.txt", "r");

// Le o arquivo inteiro
let all = f.read();
print(all);

// Le quantidade especificada de bytes
let chunk = f.read(1024);

f.close();
```

**Comportamento:**
- Le a partir da posicao atual do arquivo
- Retorna string vazia no fim do arquivo
- Avanca a posicao do arquivo

**Erros:**
- Ler de arquivo fechado
- Ler de arquivo somente escrita

---

#### read_bytes

Le dados binarios de um arquivo.

**Assinatura:**
```hemlock
file.read_bytes(size: i32): buffer
```

**Parametros:**
- `size` - Numero de bytes a ler

**Retorna:** Buffer contendo dados binarios

**Exemplo:**
```hemlock
let f = open("data.bin", "r");

// Le 256 bytes
let binary = f.read_bytes(256);
print(binary.length);       // 256

// Processa dados binarios
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**Comportamento:**
- Le quantidade exata de bytes
- Retorna buffer (nao string)
- Avanca a posicao do arquivo

---

### Escrita

#### write

Escreve texto em um arquivo.

**Assinatura:**
```hemlock
file.write(data: string): i32
```

**Parametros:**
- `data` - String a ser escrita

**Retorna:** Numero de bytes escritos (i32)

**Exemplo:**
```hemlock
let f = open("output.txt", "w");

// Escreve texto
let written = f.write("Hello, World!\n");
print("Escreveu", written, "bytes");

// Multiplas escritas
f.write("Linha 1\n");
f.write("Linha 2\n");
f.write("Linha 3\n");

f.close();
```

**Comportamento:**
- Escreve na posicao atual do arquivo
- Retorna numero de bytes escritos
- Avanca a posicao do arquivo

**Erros:**
- Escrever em arquivo fechado
- Escrever em arquivo somente leitura

---

#### write_bytes

Escreve dados binarios em um arquivo.

**Assinatura:**
```hemlock
file.write_bytes(data: buffer): i32
```

**Parametros:**
- `data` - Buffer a ser escrito

**Retorna:** Numero de bytes escritos (i32)

**Exemplo:**
```hemlock
let f = open("output.bin", "w");

// Cria buffer
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Escreve buffer
let written = f.write_bytes(buf);
print("Escreveu", written, "bytes");

f.close();
```

**Comportamento:**
- Escreve conteudo do buffer no arquivo
- Retorna numero de bytes escritos
- Avanca a posicao do arquivo

---

### Posicionamento

#### seek

Move a posicao do arquivo para um deslocamento de byte especificado.

**Assinatura:**
```hemlock
file.seek(position: i32): i32
```

**Parametros:**
- `position` - Deslocamento em bytes a partir do inicio do arquivo

**Retorna:** Nova posicao do arquivo (i32)

**Exemplo:**
```hemlock
let f = open("data.txt", "r");

// Pula para o byte 100
f.seek(100);

// Le a partir dessa posicao
let chunk = f.read(50);

// Volta ao inicio
f.seek(0);

// Le a partir do inicio
let all = f.read();

f.close();
```

**Comportamento:**
- Define a posicao do arquivo como deslocamento absoluto
- Retorna a nova posicao
- Permite posicionar alem do fim do arquivo (criar buracos ao escrever)

---

#### tell

Obtem a posicao atual do arquivo.

**Assinatura:**
```hemlock
file.tell(): i32
```

**Retorna:** Deslocamento atual em bytes a partir do inicio do arquivo (i32)

**Exemplo:**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0 (no inicio)

f.read(100);
print(f.tell());        // 100 (apos ler)

f.seek(50);
print(f.tell());        // 50 (apos seek)

f.close();
```

---

### Fechamento

#### close

Fecha o arquivo (idempotente).

**Assinatura:**
```hemlock
file.close(): null
```

**Retorna:** `null`

**Exemplo:**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// Pode ser chamado multiplas vezes com seguranca
f.close();  // Sem erro
f.close();  // Sem erro
```

**Comportamento:**
- Fecha o handle do arquivo
- Libera qualquer escrita pendente
- Idempotente (pode ser chamado multiplas vezes com seguranca)
- Define a propriedade `.closed` como `true`

**Importante:** Sempre feche arquivos quando terminar para evitar vazamento de descritores de arquivo.

---

## Propriedades de Arquivo

### .path

Obtem o caminho do arquivo.

**Tipo:** `string`

**Acesso:** Somente leitura

**Exemplo:**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

Obtem o modo de abertura.

**Tipo:** `string`

**Acesso:** Somente leitura

**Exemplo:**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Verifica se o arquivo esta fechado.

**Tipo:** `bool`

**Acesso:** Somente leitura

**Exemplo:**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Tratamento de Erros

Todas as operacoes de arquivo incluem mensagens de erro adequadas com contexto:

### Arquivo Nao Encontrado
```hemlock
let f = open("missing.txt", "r");
// Erro: Failed to open 'missing.txt': No such file or directory
```

### Ler de Arquivo Fechado
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Erro: Cannot read from closed file 'data.txt'
```

### Escrever em Arquivo Somente Leitura
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Erro: Cannot write to file 'readonly.txt' opened in read-only mode
```

### Usando try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("Erro de arquivo:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Padroes de Gerenciamento de Recursos

### Padrao Basico

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Com Tratamento de Erros

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Sempre fecha, mesmo com erro
}
```

### Padrao Seguro

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... processa conteudo ...
} catch (e) {
    print("Erro:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Exemplos de Uso

### Ler Arquivo Inteiro

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### Escrever Arquivo de Texto

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### Acrescentar a Arquivo

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Entrada de log 1");
append_file("log.txt", "Entrada de log 2");
```

### Ler Arquivo Binario

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Leu", binary.length, "bytes");
```

### Escrever Arquivo Binario

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### Ler Arquivo Linha por Linha

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Linha", i, ":", lines[i]);
    i = i + 1;
}
```

### Copiar Arquivo

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### Ler Arquivo em Pedacos

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // Le 1KB por vez
        if (chunk.length == 0) {
            break;  // Fim do arquivo
        }

        // Processa pedaco
        print("Processando", chunk.length, "bytes");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## Resumo Completo dos Metodos

| Metodo        | Assinatura               | Retorna   | Descricao                        |
|---------------|--------------------------|-----------|----------------------------------|
| `read`        | `(size?: i32)`           | `string`  | Le texto                         |
| `read_bytes`  | `(size: i32)`            | `buffer`  | Le dados binarios                |
| `write`       | `(data: string)`         | `i32`     | Escreve texto                    |
| `write_bytes` | `(data: buffer)`         | `i32`     | Escreve dados binarios           |
| `seek`        | `(position: i32)`        | `i32`     | Define posicao do arquivo        |
| `tell`        | `()`                     | `i32`     | Obtem posicao do arquivo         |
| `close`       | `()`                     | `null`    | Fecha arquivo (idempotente)      |

---

## Resumo Completo das Propriedades

| Propriedade | Tipo     | Acesso        | Descricao              |
|-------------|----------|---------------|------------------------|
| `.path`     | `string` | Somente leitura | Caminho do arquivo   |
| `.mode`     | `string` | Somente leitura | Modo de abertura     |
| `.closed`   | `bool`   | Somente leitura | Se o arquivo esta fechado |

---

## Migrando da API Antiga

**API Antiga (removida):**
- `read_file(path)` - Use `open(path, "r").read()`
- `write_file(path, data)` - Use `open(path, "w").write(data)`
- `append_file(path, data)` - Use `open(path, "a").write(data)`
- `file_exists(path)` - Sem substituto por enquanto

**Exemplo de Migracao:**
```hemlock
// Antigo (v0.0)
let content = read_file("data.txt");
write_file("output.txt", content);

// Novo (v0.1)
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## Veja Tambem

- [Funcoes Integradas](builtins.md) - Funcao `open()`
- [API de Memoria](memory-api.md) - Tipo buffer
- [API de Strings](string-api.md) - Metodos de string para processamento de texto
