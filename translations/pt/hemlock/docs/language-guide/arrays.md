# Arrays

Hemlock fornece **arrays dinâmicos** com métodos abrangentes para manipulação e processamento de dados. Arrays podem armazenar tipos mistos e crescem automaticamente conforme necessário.

## Visão Geral

```hemlock
// Literal de array
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipos mistos permitidos
let mixed = [1, "hello", true, null];

// Redimensionamento dinâmico
arr.push(6);           // Cresce automaticamente
arr.push(7);
print(arr.length);     // 7
```

## Literais de Array

### Sintaxe Básica

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### Array Vazio

```hemlock
let arr = [];  // Array vazio

// Adicionar elementos depois
arr.push(1);
arr.push(2);
arr.push(3);
```

### Tipos Mistos

Arrays podem conter tipos diferentes:

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3] (array aninhado)
```

### Arrays Aninhados

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### Arrays Tipados

Arrays podem usar anotações de tipo para forçar tipo de elemento:

```hemlock
// Sintaxe de array tipado
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Verificação de tipo em tempo de execução
let valid: array<i32> = [1, 2, 3];       // Correto
let invalid: array<i32> = [1, "two", 3]; // Erro em execução: incompatibilidade de tipo

// Arrays tipados aninhados
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Comportamento de anotação de tipo:**
- Elementos são verificados quando adicionados ao array
- Incompatibilidade de tipo causa erro em tempo de execução
- Sem anotação de tipo, arrays aceitam tipos mistos

## Indexação

### Lendo Elementos

Acesso com índice baseado em zero:

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (primeiro elemento)
print(arr[4]);  // 50 (último elemento)

// Acesso fora dos limites retorna null (sem erro)
print(arr[10]);  // null
```

### Escrevendo Elementos

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Modifica elemento existente
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Pode atribuir além do comprimento atual (array cresce)
arr[5] = 60;    // Cria [10, 20, 3, null, null, 60]
```

### Índices Negativos

**Não suportados** - use apenas índices positivos:

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // Erro ou comportamento indefinido

// Use length para obter último elemento
print(arr[arr.length - 1]);  // 3
```

## Propriedades

### Propriedade `.length`

Retorna o número de elementos:

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Array vazio
let empty = [];
print(empty.length);  // 0

// Após modificação
arr.push(6);
print(arr.length);  // 6
```

## Métodos de Array

Hemlock fornece 18 métodos de array para operações abrangentes.

### Operações de Pilha

**`push(value)`** - Adiciona elemento no final:
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Remove e retorna o último elemento:
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Retorna 5, arr agora é [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Operações de Fila

**`shift()`** - Remove e retorna o primeiro elemento:
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Retorna 1, arr agora é [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Adiciona elemento no início:
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Inserção e Remoção

**`insert(index, value)`** - Insere elemento no índice especificado:
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // Insere 3 no índice 2: [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Insere no início: [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Remove e retorna elemento no índice especificado:
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Retorna 3, arr agora é [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Operações de Busca

**`find(value)`** - Encontra a primeira ocorrência:
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (índice da primeira ocorrência)
let idx2 = arr.find(99);     // -1 (não encontrado)

// Funciona com qualquer tipo
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - Verifica se array contém valor:
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Operações de Extração

**`slice(start, end)`** - Extrai subarray (end não incluído):
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (índices 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Array original não muda
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Obtém o primeiro elemento (sem remover):
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (sem remover)
print(arr);                  // [1, 2, 3] (inalterado)
```

**`last()`** - Obtém o último elemento (sem remover):
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (sem remover)
print(arr);                  // [1, 2, 3] (inalterado)
```

### Operações de Transformação

**`reverse()`** - Inverte o array no local:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (modificado)
```

**`join(delimiter)`** - Une elementos em uma string:
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funciona com tipos mistos
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - Concatena com outro array:
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (novo array)

// Arrays originais não mudam
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Operações Utilitárias

**`clear()`** - Remove todos os elementos:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Encadeamento de Métodos

Métodos que retornam arrays ou valores podem ser encadeados:

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Referência Completa de Métodos

| Método | Parâmetros | Retorno | Modifica Original | Descrição |
|--------|-----------|---------|---------|-------------|
| `push(value)` | any | void | Sim | Adiciona elemento no final |
| `pop()` | - | any | Sim | Remove e retorna último elemento |
| `shift()` | - | any | Sim | Remove e retorna primeiro elemento |
| `unshift(value)` | any | void | Sim | Adiciona elemento no início |
| `insert(index, value)` | i32, any | void | Sim | Insere no índice especificado |
| `remove(index)` | i32 | any | Sim | Remove e retorna elemento no índice |
| `find(value)` | any | i32 | Não | Encontra primeira ocorrência (retorna -1 se não encontrado) |
| `contains(value)` | any | bool | Não | Verifica se contém valor |
| `slice(start, end)` | i32, i32 | array | Não | Extrai subarray (novo array) |
| `join(delimiter)` | string | string | Não | Une em string |
| `concat(other)` | array | array | Não | Concatena arrays (novo array) |
| `reverse()` | - | void | Sim | Inverte no local |
| `first()` | - | any | Não | Obtém primeiro elemento |
| `last()` | - | any | Não | Obtém último elemento |
| `clear()` | - | void | Sim | Remove todos os elementos |
| `map(callback)` | fn | array | Não | Transforma cada elemento |
| `filter(predicate)` | fn | array | Não | Seleciona elementos correspondentes |
| `reduce(callback, initial)` | fn, any | any | Não | Reduz a um único valor |

## Detalhes de Implementação

### Modelo de Memória

- **Alocação no heap** - Capacidade dinâmica
- **Crescimento automático** - Dobra quando excede capacidade
- **Sem encolhimento automático** - Capacidade não diminui
- **Sem verificação de limites no índice** - Use métodos para segurança

### Gerenciamento de Capacidade

```hemlock
let arr = [];  // Capacidade inicial: 0

arr.push(1);   // Cresce para capacidade 1
arr.push(2);   // Cresce para capacidade 2
arr.push(3);   // Cresce para capacidade 4 (dobra)
arr.push(4);   // Ainda capacidade 4
arr.push(5);   // Cresce para capacidade 8 (dobra)
```

### Comparação de Valores

`find()` e `contains()` usam comparação de igualdade de valor:

```hemlock
// Tipos primitivos: compara por valor
let arr = [1, 2, 3];
arr.contains(2);  // true

// Strings: compara por valor
let words = ["hello", "world"];
words.contains("hello");  // true

// Objetos: compara por referência
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (mesma referência)
arr2.contains(obj2);  // false (referência diferente)
```

## Padrões Comuns

### Operações Funcionais (map/filter/reduce)

Arrays têm métodos `map`, `filter` e `reduce` embutidos:

```hemlock
// map - transforma cada elemento
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - seleciona elementos correspondentes
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - reduz a um único valor
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Encadeando operações funcionais
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Padrão: Array como Pilha

```hemlock
let stack = [];

// Empilhar
stack.push(1);
stack.push(2);
stack.push(3);

// Desempilhar
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Padrão: Array como Fila

```hemlock
let queue = [];

// Enfileirar (adicionar no final)
queue.push(1);
queue.push(2);
queue.push(3);

// Desenfileirar (remover do início)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Melhores Práticas

1. **Use métodos em vez de índice direto** - Verificação de limites e clareza de código
2. **Verifique limites** - Indexação direta não verifica limites
3. **Prefira operações imutáveis** - Use `slice()` e `concat()` em vez de modificar original
4. **Pré-inicialize capacidade** - Se souber o tamanho (não suportado atualmente)
5. **Use `contains()` para verificar pertinência** - Mais claro que loop manual
6. **Encadeie métodos** - Mais legível que chamadas aninhadas

## Armadilhas Comuns

### Armadilha: Índice Direto Fora dos Limites

```hemlock
let arr = [1, 2, 3];

// Sem verificação de limites!
arr[10] = 99;  // Cria array esparso com null
print(arr.length);  // 11 (não 3!)

// Melhor: use push() ou verifique length
if (arr.length <= 10) {
    arr.push(99);
}
```

### Armadilha: Modificação vs Novo Array

```hemlock
let arr = [1, 2, 3];

// Modifica original
arr.reverse();
print(arr);  // [3, 2, 1]

// Retorna novo array
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (inalterado)
print(sub);  // [3, 2]
```

### Armadilha: Igualdade de Referência

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Mesma referência: true
arr.contains(obj);  // true

// Referência diferente: false
arr.contains({ x: 10 });  // false (objeto diferente)
```

### Armadilha: Arrays de Longa Duração

```hemlock
// Arrays em escopo local são liberados automaticamente, mas arrays globais/de longa duração precisam atenção
let global_cache = [];  // Nível de módulo, persiste até fim do programa

fn add_to_cache(item) {
    global_cache.push(item);  // Cresce infinitamente
}

// Para dados de longa duração, considere:
// - Limpar o array periodicamente: global_cache.clear();
// - Liberar antecipadamente: free(global_cache);
```

## Exemplos

### Exemplo: Estatísticas de Array

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### Exemplo: Remoção de Duplicados

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### Exemplo: Dividir em Blocos

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### Exemplo: Achatar Array

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Array aninhado - achatar
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### Exemplo: Ordenação (Bubble Sort)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Troca
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // Modifica no local
print(numbers);  // [1, 2, 5, 8, 9]
```

## Limitações

Limitações atuais:

- **Sem verificação de limites no índice** - Acesso direto não verifica limites
- **Objetos usam igualdade de referência** - `find()` e `contains()` usam comparação de referência
- **Sem desestruturação de array** - Sintaxe `let [a, b] = arr` não suportada
- **Sem operador spread** - Sintaxe `[...arr1, ...arr2]` não suportada

**Nota:** Arrays usam contagem de referência, sendo liberados automaticamente ao sair do escopo. Veja [Gerenciamento de Memória](memory.md#internal-reference-counting) para detalhes.

## Tópicos Relacionados

- [Strings](strings.md) - Métodos de string são similares aos de array
- [Objetos](objects.md) - Arrays também são tipo objeto
- [Funções](functions.md) - Arrays e funções de ordem superior
- [Fluxo de Controle](control-flow.md) - Iteração sobre arrays

## Veja Também

- **Tamanho dinâmico**: Arrays crescem automaticamente dobrando capacidade
- **Métodos**: 18 métodos abrangentes de operação, incluindo map/filter/reduce
- **Memória**: Veja [Memória](memory.md) para detalhes de alocação de arrays
