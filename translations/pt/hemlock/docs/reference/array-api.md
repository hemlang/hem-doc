# Referencia da API de Arrays

Documentacao completa do tipo array do Hemlock e todos os seus 28 metodos de array.

---

## Visao Geral

Arrays em Hemlock sao sequencias **dinamicas, alocadas no heap** que podem armazenar tipos mistos. Eles fornecem metodos abrangentes para manipulacao e processamento de dados.

**Caracteristicas Principais:**
- Tamanho dinamico (cresce automaticamente)
- Indexacao comecando em zero
- Permite tipos mistos
- 28 metodos integrados
- Alocado no heap e rastreia capacidade

---

## Tipo Array

**Tipo:** `array`

**Propriedades:**
- `.length` - Numero de elementos (i32)

**Sintaxe Literal:** Colchetes `[elem1, elem2, ...]`

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// Tipos mistos
let mixed = [1, "hello", true, null];
print(mixed.length);   // 4

// Array vazio
let empty = [];
print(empty.length);   // 0
```

---

## Indexacao

Arrays suportam indexacao baseada em zero usando `[]`:

**Acesso de Leitura:**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**Acesso de Escrita:**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**Nota:** A indexacao direta nao verifica limites. Use metodos para seguranca.

---

## Propriedades do Array

### .length

Obtem o numero de elementos no array.

**Tipo:** `i32`

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let empty = [];
print(empty.length);   // 0

// O comprimento muda dinamicamente
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## Metodos do Array

### Operacoes de Pilha

#### push

Adiciona um elemento ao final do array.

**Assinatura:**
```hemlock
array.push(value: any): null
```

**Parametros:**
- `value` - O elemento a ser adicionado

**Retorna:** `null`

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("hello");     // [1, 2, 3, 4, 5, "hello"]
```

---

#### pop

Remove e retorna o ultimo elemento.

**Assinatura:**
```hemlock
array.pop(): any
```

**Retorna:** O ultimo elemento (removido do array)

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
let last = arr.pop();  // 3
print(arr);            // [1, 2]

let last2 = arr.pop(); // 2
print(arr);            // [1]
```

**Erro:** Lanca erro de tempo de execucao se o array estiver vazio.

---

### Operacoes de Fila

#### shift

Remove e retorna o primeiro elemento.

**Assinatura:**
```hemlock
array.shift(): any
```

**Retorna:** O primeiro elemento (removido do array)

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();  // 1
print(arr);               // [2, 3]

let first2 = arr.shift(); // 2
print(arr);               // [3]
```

**Erro:** Lanca erro de tempo de execucao se o array estiver vazio.

---

#### unshift

Adiciona um elemento ao inicio do array.

**Assinatura:**
```hemlock
array.unshift(value: any): null
```

**Parametros:**
- `value` - O elemento a ser adicionado

**Retorna:** `null`

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### Insercao e Remocao

#### insert

Insere um elemento em um indice especificado.

**Assinatura:**
```hemlock
array.insert(index: i32, value: any): null
```

**Parametros:**
- `index` - Posicao de insercao (baseada em 0)
- `value` - Elemento a ser inserido

**Retorna:** `null`

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// Insere no final
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**Comportamento:** Desloca elementos no indice e apos para a direita.

---

#### remove

Remove e retorna o elemento em um indice especificado.

**Assinatura:**
```hemlock
array.remove(index: i32): any
```

**Parametros:**
- `index` - Posicao a ser removida (baseada em 0)

**Retorna:** O elemento removido

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let removed2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**Comportamento:** Desloca elementos apos o indice para a esquerda.

**Erro:** Lanca erro de tempo de execucao se o indice estiver fora dos limites.

---

### Busca e Localizacao

#### find

Encontra a primeira ocorrencia de um valor.

**Assinatura:**
```hemlock
array.find(value: any): i32
```

**Parametros:**
- `value` - O valor a ser buscado

**Retorna:** Indice da primeira ocorrencia, ou `-1` se nao encontrado

**Exemplo:**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1 (nao encontrado)

// Encontra primeira duplicata
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1 (primeira ocorrencia)
```

**Comparacao:** Usa igualdade de valor para tipos primitivos e strings.

---

#### contains

Verifica se o array contem um valor.

**Assinatura:**
```hemlock
array.contains(value: any): bool
```

**Parametros:**
- `value` - O valor a ser buscado

**Retorna:** `true` se encontrado, caso contrario `false`

**Exemplo:**
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false

// Funciona com strings tambem
let words = ["hello", "world"];
let has3 = words.contains("hello");  // true
```

---

### Fatiamento e Extracao

#### slice

Extrai um sub-array por intervalo (final exclusivo).

**Assinatura:**
```hemlock
array.slice(start: i32, end?: i32): array
```

**Parametros:**
- `start` - Indice inicial (baseado em 0, inclusivo)
- `end` - Indice final (exclusivo). Padrao e `array.length` se omitido.

**Retorna:** Novo array contendo elementos no intervalo [start, end)

**Modifica o Original:** Nao (retorna novo array)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4]
let first_three = arr.slice(0, 3);  // [1, 2, 3]
let last_two = arr.slice(3, 5);     // [4, 5]

// Argumento unico: do indice ate o final
let tail = arr.slice(2);     // [3, 4, 5]
let copy = arr.slice(0);     // [1, 2, 3, 4, 5] (copia rasa)

// Fatia vazia
let empty = arr.slice(2, 2); // []
```

---

#### first

Obtem o primeiro elemento sem remover.

**Assinatura:**
```hemlock
array.first(): any
```

**Retorna:** O primeiro elemento

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3] (inalterado)
```

**Erro:** Lanca erro de tempo de execucao se o array estiver vazio.

---

#### last

Obtem o ultimo elemento sem remover.

**Assinatura:**
```hemlock
array.last(): any
```

**Retorna:** O ultimo elemento

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3] (inalterado)
```

**Erro:** Lanca erro de tempo de execucao se o array estiver vazio.

---

### Operacoes com Arrays

#### reverse

Inverte o array no local.

**Assinatura:**
```hemlock
array.reverse(): null
```

**Retorna:** `null`

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let words = ["hello", "world"];
words.reverse();             // ["world", "hello"]
```

---

#### clear

Remove todos os elementos do array.

**Assinatura:**
```hemlock
array.clear(): null
```

**Retorna:** `null`

**Modifica o Original:** Sim (modifica o array no local)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### Combinacao de Arrays

#### concat

Concatena com outro array.

**Assinatura:**
```hemlock
array.concat(other: array): array
```

**Parametros:**
- `other` - O array a ser concatenado

**Retorna:** Novo array contendo elementos de ambos os arrays

**Modifica o Original:** Nao (retorna novo array)

**Exemplo:**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                    // [1, 2, 3] (inalterado)
print(b);                    // [4, 5, 6] (inalterado)

// Concatenacao em cadeia
let c = [7, 8];
let all = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### Operacoes Funcionais

#### map

Transforma cada elemento usando uma funcao callback.

**Assinatura:**
```hemlock
array.map(callback: fn): array
```

**Parametros:**
- `callback` - Funcao que recebe um elemento e retorna o valor transformado

**Retorna:** Novo array contendo elementos transformados

**Modifica o Original:** Nao (retorna novo array)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let doubled = arr.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

let names = ["alice", "bob"];
let upper = names.map(fn(s) { return s.to_upper(); });
print(upper);  // ["ALICE", "BOB"]
```

---

#### filter

Seleciona elementos que correspondem a um predicado.

**Assinatura:**
```hemlock
array.filter(predicate: fn): array
```

**Parametros:**
- `predicate` - Funcao que recebe um elemento e retorna bool

**Retorna:** Novo array contendo elementos para os quais o predicado retorna true

**Modifica o Original:** Nao (retorna novo array)

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let evens = arr.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4, 6]

let words = ["hello", "hi", "hey", "goodbye"];
let short = words.filter(fn(s) { return s.length < 4; });
print(short);  // ["hi", "hey"]
```

---

#### reduce

Reduz o array a um unico valor usando um acumulador.

**Assinatura:**
```hemlock
array.reduce(callback: fn, initial: any): any
```

**Parametros:**
- `callback` - Funcao que recebe (acumulador, elemento) e retorna novo acumulador
- `initial` - Valor inicial do acumulador

**Retorna:** Valor acumulado final

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sum = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

let product = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(product);  // 120

// Encontra o maximo
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

#### every

Verifica se todos os elementos satisfazem um predicado.

**Assinatura:**
```hemlock
array.every(predicate: fn): bool
```

**Parametros:**
- `predicate` - Funcao que recebe um elemento e retorna um valor verdadeiro/falso

**Retorna:** `true` se todos os elementos corresponderem, `false` caso contrario. Arrays vazios retornam `true` (verdade vacua).

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [2, 4, 6, 8];
let all_even = arr.every(fn(x) { return x % 2 == 0; });
print(all_even);  // true

let arr2 = [2, 3, 6, 8];
let all_even2 = arr2.every(fn(x) { return x % 2 == 0; });
print(all_even2);  // false
```

---

#### some

Verifica se algum elemento satisfaz um predicado.

**Assinatura:**
```hemlock
array.some(predicate: fn): bool
```

**Parametros:**
- `predicate` - Funcao que recebe um elemento e retorna um valor verdadeiro/falso

**Retorna:** `true` se algum elemento corresponder, `false` caso contrario. Arrays vazios retornam `false`.

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 3, 5, 6];
let has_even = arr.some(fn(x) { return x % 2 == 0; });
print(has_even);  // true

let arr2 = [1, 3, 5, 7];
let has_even2 = arr2.some(fn(x) { return x % 2 == 0; });
print(has_even2);  // false
```

---

#### indexOf

Encontra o primeiro indice de um valor.

**Assinatura:**
```hemlock
array.indexOf(value: any): i32
```

**Parametros:**
- `value` - Valor a ser buscado

**Retorna:** Indice da primeira ocorrencia, ou `-1` se nao encontrado

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = ["a", "b", "c", "b"];
print(arr.indexOf("b"));   // 1
print(arr.indexOf("z"));   // -1
```

---

#### lastIndexOf

Encontra o ultimo indice de um valor.

**Assinatura:**
```hemlock
array.lastIndexOf(value: any): i32
```

**Parametros:**
- `value` - Valor a ser buscado

**Retorna:** Indice da ultima ocorrencia, ou `-1` se nao encontrado

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = ["a", "b", "c", "b"];
print(arr.lastIndexOf("b"));   // 3
print(arr.lastIndexOf("z"));   // -1
```

---

#### findIndex

Encontra o indice do primeiro elemento que satisfaz um predicado.

**Assinatura:**
```hemlock
array.findIndex(predicate: fn): i32
```

**Parametros:**
- `predicate` - Funcao que recebe um elemento e retorna bool

**Retorna:** Indice do primeiro elemento correspondente, ou `-1` se nenhum encontrado

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 3, 5, 6, 7];
let idx = arr.findIndex(fn(x) { return x % 2 == 0; });
print(idx);  // 3
```

---

#### sort

Ordena o array no local com comparador opcional.

**Assinatura:**
```hemlock
array.sort(compare?: fn): null
```

**Parametros:**
- `compare` (opcional) - Funcao comparadora que recebe (a, b), retornando negativo se a < b, 0 se iguais, positivo se a > b

**Retorna:** `null`

**Modifica o Original:** Sim

**Exemplo:**
```hemlock
let arr = [3, 1, 4, 1, 5];
arr.sort();
print(arr);  // [1, 1, 3, 4, 5]

// Comparador personalizado (descendente)
let arr2 = [3, 1, 4, 1, 5];
arr2.sort(fn(a, b) { return b - a; });
print(arr2);  // [5, 4, 3, 1, 1]
```

---

#### fill

Preenche elementos do array com um valor, opcionalmente dentro de um intervalo.

**Assinatura:**
```hemlock
array.fill(value: any, start?: i32, end?: i32): null
```

**Parametros:**
- `value` - Valor para preencher
- `start` (opcional) - Indice inicial (padrao: 0). Indices negativos contam do final.
- `end` (opcional) - Indice final, exclusivo (padrao: comprimento do array). Indices negativos contam do final.

**Retorna:** `null`

**Modifica o Original:** Sim

**Exemplo:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.fill(0);
print(arr);  // [0, 0, 0, 0, 0]

let arr2 = [1, 2, 3, 4, 5];
arr2.fill(9, 1, 4);
print(arr2);  // [1, 9, 9, 9, 5]
```

---

#### reserve

Pre-aloca capacidade para insercoes em massa.

**Assinatura:**
```hemlock
array.reserve(n: i32): null
```

**Parametros:**
- `n` - Capacidade minima a garantir

**Retorna:** `null`

**Modifica o Original:** Sim (pode alterar capacidade interna)

**Exemplo:**
```hemlock
let arr = [];
arr.reserve(1000);  // Pre-aloca espaco para 1000 elementos

for (let i = 0; i < 1000; i++) {
    arr.push(i);    // Nenhuma realocacao necessaria
}
```

---

#### flat

Achata um nivel de arrays aninhados.

**Assinatura:**
```hemlock
array.flat(): array
```

**Retorna:** Novo array com arrays aninhados achatados por um nivel

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [[1, 2], [3, 4], [5]];
let flat = arr.flat();
print(flat);  // [1, 2, 3, 4, 5]

// Elementos nao-array sao mantidos como estao
let mixed = [1, [2, 3], 4, [5]];
let flat2 = mixed.flat();
print(flat2);  // [1, 2, 3, 4, 5]

// Apenas achata um nivel
let deep = [[1, [2, 3]], [4]];
let flat3 = deep.flat();
print(flat3);  // [1, [2, 3], 4]
```

---

#### serialize

Converte array para representacao de string JSON.

**Assinatura:**
```hemlock
array.serialize(): string
```

**Retorna:** String JSON representando o array

**Modifica o Original:** Nao

**Exemplo:**
```hemlock
let arr = [1, 2, 3];
let json = arr.serialize();
print(json);  // [1,2,3]

let mixed = ["hello", true, null, 42];
let json2 = mixed.serialize();
print(json2);  // ["hello",true,null,42]
```

---

### Conversao para String

#### join

Junta elementos em uma string usando um delimitador.

**Assinatura:**
```hemlock
array.join(delimiter: string): string
```

**Parametros:**
- `delimiter` - String a ser colocada entre os elementos

**Retorna:** String concatenando todos os elementos

**Exemplo:**
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funciona com tipos mistos tambem
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"

// Delimitador vazio
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**Comportamento:** Converte automaticamente todos os elementos para strings, incluindo valores rune retornados por `string.chars()`.

```hemlock
// Join em arrays de runes (de chars())
let chars = "hello".chars();
print(chars.join("-"));   // "h-e-l-l-o"

// Idioma de reversao de string
let reversed = "hello".chars();
reversed.reverse();
print(reversed.join(""));  // "olleh"
```

---

## Encadeamento de Metodos

Metodos de array podem ser encadeados para operacoes concisas:

**Exemplo:**
```hemlock
// Encadeando slice e join
let result = ["apple", "banana", "cherry", "date"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

// Encadeando concat e slice
let combined = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// Encadeamento complexo
let words = ["hello", "world", "foo", "bar"];
let result2 = words
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "hello-world-foo-baz"
```

---

## Resumo Completo dos Metodos

### Metodos que Modificam

Metodos que modificam o array no local:

| Metodo     | Assinatura                   | Retorna   | Descricao                      |
|------------|------------------------------|-----------|--------------------------------|
| `push`     | `(value: any)`               | `null`    | Adiciona ao final              |
| `pop`      | `()`                         | `any`     | Remove do final                |
| `shift`    | `()`                         | `any`     | Remove do inicio               |
| `unshift`  | `(value: any)`               | `null`    | Adiciona ao inicio             |
| `insert`   | `(index: i32, value: any)`   | `null`    | Insere no indice               |
| `remove`   | `(index: i32)`               | `any`     | Remove no indice               |
| `reverse`  | `()`                         | `null`    | Inverte no local               |
| `clear`    | `()`                         | `null`    | Remove todos os elementos      |
| `reserve`  | `(n: i32)`                   | `null`    | Pre-aloca capacidade           |
| `sort`     | `(compare?: fn)`             | `null`    | Ordena no local (comparador opcional) |
| `fill`     | `(value: any, start?: i32, end?: i32)` | `null` | Preenche elementos com valor |

### Metodos que Nao Modificam

Metodos que retornam novos valores sem modificar o original:

| Metodo     | Assinatura                       | Retorna   | Descricao                      |
|------------|----------------------------------|-----------|--------------------------------|
| `find`     | `(value: any)`                   | `i32`     | Encontra primeira ocorrencia   |
| `findIndex`| `(predicate: fn)`                | `i32`     | Encontra indice por predicado  |
| `indexOf`  | `(value: any)`                   | `i32`     | Encontra indice do valor (-1 se nao encontrado) |
| `lastIndexOf` | `(value: any)`                | `i32`     | Encontra ultimo indice do valor |
| `contains` | `(value: any)`                   | `bool`    | Verifica se contem valor       |
| `slice`    | `(start: i32, end: i32)`         | `array`   | Extrai sub-array               |
| `first`    | `()`                             | `any`     | Obtem primeiro elemento        |
| `last`     | `()`                             | `any`     | Obtem ultimo elemento          |
| `concat`   | `(other: array)`                 | `array`   | Concatena arrays               |
| `flat`     | `()`                             | `array`   | Achata um nivel de aninhamento |
| `join`     | `(delimiter: string)`            | `string`  | Junta elementos em string      |
| `map`      | `(callback: fn)`                 | `array`   | Transforma cada elemento       |
| `filter`   | `(predicate: fn)`                | `array`   | Seleciona elementos            |
| `reduce`   | `(callback: fn, initial: any)`   | `any`     | Reduz a um unico valor         |
| `every`    | `(predicate: fn)`                | `bool`    | Verifica se todos correspondem |
| `some`     | `(predicate: fn)`                | `bool`    | Verifica se algum corresponde  |
| `serialize`| `()`                             | `string`  | Converte para string JSON      |

---

## Padroes de Uso

### Uso como Pilha

```hemlock
let stack = [];

// Empilhar
stack.push(1);
stack.push(2);
stack.push(3);

// Desempilhar
while (stack.length > 0) {
    let item = stack.pop();
    print(item);  // 3, 2, 1
}
```

### Uso como Fila

```hemlock
let queue = [];

// Enfileirar
queue.push(1);
queue.push(2);
queue.push(3);

// Desenfileirar
while (queue.length > 0) {
    let item = queue.shift();
    print(item);  // 1, 2, 3
}
```

### Transformacao de Array

```hemlock
// Filtragem (modo manual)
let numbers = [1, 2, 3, 4, 5, 6];
let evens = [];
let i = 0;
while (i < numbers.length) {
    if (numbers[i] % 2 == 0) {
        evens.push(numbers[i]);
    }
    i = i + 1;
}

// Mapeamento (modo manual)
let numbers2 = [1, 2, 3, 4, 5];
let doubled = [];
let j = 0;
while (j < numbers2.length) {
    doubled.push(numbers2[j] * 2);
    j = j + 1;
}
```

### Construindo Arrays

```hemlock
let arr = [];

// Construir array com loop
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## Detalhes de Implementacao

**Gerenciamento de Capacidade:**
- Arrays crescem automaticamente conforme necessario
- Capacidade dobra quando excedida
- Use `reserve(n)` para pre-alocar capacidade para insercoes em massa

**Comparacao de Valores:**
- `find()` e `contains()` usam igualdade de valor
- Funciona corretamente para tipos primitivos e strings
- Objetos/arrays sao comparados por referencia

**Memoria:**
- Alocado no heap
- Sem liberacao automatica (gerenciamento manual de memoria)
- Acesso direto por indice nao verifica limites

---

## Veja Tambem

- [Sistema de Tipos](type-system.md) - Detalhes do tipo array
- [API de Strings](string-api.md) - Resultado do join() em strings
- [Operadores](operators.md) - Operador de indexacao de array
