# Referencia de Operadores

Referencia completa de todos os operadores em Hemlock, incluindo precedencia, associatividade e comportamento.

---

## Visao Geral

Hemlock fornece operadores estilo C com regras de precedencia claras. Todos os operadores seguem regras de tipo estritas com promocao automatica de tipo quando aplicavel.

---

## Operadores Aritmeticos

### Aritmetica Binaria

| Operador | Nome       | Exemplo    | Descricao         |
|----------|------------|------------|-------------------|
| `+`      | Adicao     | `a + b`    | Soma dois valores |
| `-`      | Subtracao  | `a - b`    | Subtrai b de a    |
| `*`      | Multiplicacao | `a * b` | Multiplica dois valores |
| `/`      | Divisao    | `a / b`    | Divide a por b    |

**Promocao de Tipo:**
O resultado segue as regras de promocao de tipo (veja [Sistema de Tipos](type-system.md#type-promotion-rules)).

**Exemplo:**
```hemlock
let a = 10 + 5;        // 15 (i32)
let b = 10 - 3;        // 7 (i32)
let c = 4 * 5;         // 20 (i32)
let d = 20 / 4;        // 5 (i32)

// Divisao float
let e = 10.0 / 3.0;    // 3.333... (f64)

// Tipos mistos
let f: u8 = 10;
let g: i32 = 20;
let h = f + g;         // 30 (i32, promovido)
```

**Divisao por Zero:**
- Inteiro dividido por zero: erro de runtime
- Float dividido por zero: retorna `inf` ou `-inf`

---

### Aritmetica Unaria

| Operador | Nome     | Exemplo | Descricao       |
|----------|----------|---------|-----------------|
| `-`      | Negacao  | `-a`    | Nega valor      |
| `+`      | Positivo | `+a`    | Identidade (noop) |

**Exemplo:**
```hemlock
let a = 5;
let b = -a;            // -5
let c = +a;            // 5 (sem mudanca)

let x = -3.14;         // -3.14
```

---

## Operadores de Comparacao

| Operador | Nome            | Exemplo    | Retorna  |
|----------|-----------------|------------|----------|
| `==`     | Igual           | `a == b`   | `bool`   |
| `!=`     | Diferente       | `a != b`   | `bool`   |
| `<`      | Menor que       | `a < b`    | `bool`   |
| `>`      | Maior que       | `a > b`    | `bool`   |
| `<=`     | Menor ou igual  | `a <= b`   | `bool`   |
| `>=`     | Maior ou igual  | `a >= b`   | `bool`   |

**Promocao de Tipo:**
Operandos sao promovidos antes da comparacao.

**Exemplo:**
```hemlock
print(5 == 5);         // true
print(10 != 5);        // true
print(3 < 7);          // true
print(10 > 5);         // true
print(5 <= 5);         // true
print(10 >= 5);        // true

// Comparacao de string
print("hello" == "hello");  // true
print("abc" < "def");       // true (lexicografica)

// Tipos mistos
let a: u8 = 10;
let b: i32 = 10;
print(a == b);         // true (promovido para i32)
```

---

## Operadores Logicos

| Operador | Nome      | Exemplo      | Descricao                  |
|----------|-----------|--------------|----------------------------|
| `&&`     | E logico  | `a && b`     | True se ambos forem true   |
| `||`     | Ou logico | `a || b`     | True se qualquer for true  |
| `!`      | Nao logico| `!a`         | Inverte booleano           |

**Avaliacao Curto-Circuito:**
- `&&` - Para no primeiro valor falso
- `||` - Para no primeiro valor verdadeiro

**Exemplo:**
```hemlock
let a = true;
let b = false;

print(a && b);         // false
print(a || b);         // true
print(!a);             // false
print(!b);             // true

// Curto-circuito
if (x != 0 && (10 / x) > 2) {
    print("seguro");
}

if (x == 0 || (10 / x) > 2) {
    print("seguro");
}
```

---

## Operadores Bit a Bit

**Restricao:** Apenas para tipos inteiros (i8-i64, u8-u64)

### Bit a Bit Binarios

| Operador | Nome         | Exemplo    | Descricao               |
|----------|--------------|------------|-------------------------|
| `&`      | E bit a bit  | `a & b`    | E em cada bit           |
| `|`      | Ou bit a bit | `a | b`    | Ou em cada bit          |
| `^`      | Xor bit a bit| `a ^ b`    | Ou exclusivo em cada bit|
| `<<`     | Shift esquerda | `a << b` | Desloca bits a esquerda |
| `>>`     | Shift direita | `a >> b`  | Desloca bits a direita  |

**Preservacao de Tipo:**
O tipo do resultado corresponde ao tipo do operando (apos promocao).

**Exemplo:**
```hemlock
let a = 12;  // 1100 em binario
let b = 10;  // 1010 em binario

print(a & b);          // 8  (1000)
print(a | b);          // 14 (1110)
print(a ^ b);          // 6  (0110)
print(a << 2);         // 48 (110000)
print(a >> 1);         // 6  (110)
```

**Exemplo Sem Sinal:**
```hemlock
let c: u8 = 15;        // 00001111
let d: u8 = 7;         // 00000111

print(c & d);          // 7  (00000111)
print(c | d);          // 15 (00001111)
print(c ^ d);          // 8  (00001000)
```

**Comportamento de Shift Direita:**
- Tipos com sinal: shift aritmetico (extensao de sinal)
- Tipos sem sinal: shift logico (preenche com zeros)

---

### Bit a Bit Unario

| Operador | Nome             | Exemplo | Descricao          |
|----------|------------------|---------|---------------------|
| `~`      | Complemento bit a bit | `~a` | Inverte todos os bits |

**Exemplo:**
```hemlock
let a = 12;            // 00001100 (i32)
print(~a);             // -13 (complemento de dois)

let b: u8 = 15;        // 00001111
print(~b);             // 240 (11110000)
```

---

## Operadores de String

### Concatenacao

| Operador | Nome         | Exemplo    | Descricao        |
|----------|--------------|------------|------------------|
| `+`      | Concatenacao | `a + b`    | Concatena strings|

**Exemplo:**
```hemlock
let s = "hello" + " " + "world";  // "hello world"
let msg = "Contagem: " + typeof(42); // "Contagem: 42"

// String + rune
let greeting = "Hello" + '!';      // "Hello!"

// Rune + string
let prefix = '>' + " Mensagem";    // "> Mensagem"
```

---

## Operadores de Atribuicao

### Atribuicao Basica

| Operador | Nome       | Exemplo    | Descricao              |
|----------|------------|------------|------------------------|
| `=`      | Atribuicao | `a = b`    | Atribui valor a variavel |

**Exemplo:**
```hemlock
let x = 10;
x = 20;

let arr = [1, 2, 3];
arr[0] = 99;

let obj = { x: 10 };
obj.x = 20;
```

### Atribuicao Composta

#### Atribuicao Composta Aritmetica

| Operador | Nome             | Exemplo    | Equivalente        |
|----------|------------------|------------|--------------------|
| `+=`     | Adicao atribuicao | `a += b`  | `a = a + b`        |
| `-=`     | Subtracao atribuicao | `a -= b` | `a = a - b`       |
| `*=`     | Multiplicacao atribuicao | `a *= b` | `a = a * b`   |
| `/=`     | Divisao atribuicao | `a /= b` | `a = a / b`       |
| `%=`     | Modulo atribuicao | `a %= b`  | `a = a % b`        |

**Exemplo:**
```hemlock
let x = 10;
x += 5;      // x agora e 15
x -= 3;      // x agora e 12
x *= 2;      // x agora e 24
x /= 4;      // x agora e 6

let count = 0;
count += 1;  // Incrementa por 1
```

#### Atribuicao Composta Bit a Bit

| Operador | Nome              | Exemplo     | Equivalente         |
|----------|-------------------|-------------|---------------------|
| `&=`     | E atribuicao      | `a &= b`    | `a = a & b`         |
| `\|=`    | Ou atribuicao     | `a \|= b`   | `a = a \| b`        |
| `^=`     | Xor atribuicao    | `a ^= b`    | `a = a ^ b`         |
| `<<=`    | Shift esq atribuicao | `a <<= b` | `a = a << b`      |
| `>>=`    | Shift dir atribuicao | `a >>= b` | `a = a >> b`      |

**Exemplo:**
```hemlock
let flags = 0b1111;
flags &= 0b0011;   // flags agora e 0b0011 (mascara bits superiores)
flags |= 0b1000;   // flags agora e 0b1011 (define um bit)
flags ^= 0b0001;   // flags agora e 0b1010 (alterna um bit)

let x = 1;
x <<= 4;           // x agora e 16 (shift esquerda por 4)
x >>= 2;           // x agora e 4 (shift direita por 2)
```

### Incremento/Decremento

| Operador | Nome       | Exemplo | Descricao        |
|----------|------------|---------|------------------|
| `++`     | Incremento | `a++`   | Adiciona 1 (sufixo) |
| `--`     | Decremento | `a--`   | Subtrai 1 (sufixo) |

**Exemplo:**
```hemlock
let i = 0;
i++;         // i agora e 1
i++;         // i agora e 2
i--;         // i agora e 1

// Comum em loops
for (let j = 0; j < 10; j++) {
    print(j);
}
```

**Nota:** `++` e `--` sao ambos operadores sufixo (retornam valor antes de incrementar/decrementar)

---

## Operadores Null-Safe

### Coalescencia Nula (`??`)

Retorna operando esquerdo se nao for null, caso contrario retorna direito.

| Operador | Nome               | Exemplo      | Descricao                          |
|----------|--------------------|--------------|------------------------------------|
| `??`     | Coalescencia nula  | `a ?? b`     | Retorna a se nao-null, senao b    |

**Exemplo:**
```hemlock
let name = null;
let display = name ?? "Anonimo";  // "Anonimo"

let value = 42;
let result = value ?? 0;            // 42

// Encadeamento
let a = null;
let b = null;
let c = "encontrado";
let result2 = a ?? b ?? c;          // "encontrado"

// Com chamadas de funcao
fn get_config() { return null; }
let config = get_config() ?? { default: true };
```

---

### Encadeamento Opcional (`?.`)

Acessa propriedades ou chama metodos com seguranca em valores potencialmente nulos.

| Operador | Nome                | Exemplo        | Descricao                                |
|----------|---------------------|----------------|------------------------------------------|
| `?.`     | Encadeamento opcional | `a?.b`       | Retorna a.b se a nao-null, senao null   |
| `?.[`    | Indice opcional     | `a?.[0]`       | Retorna a[0] se a nao-null, senao null  |
| `?.(`    | Chamada opcional    | `a?.()`        | Chama a() se a nao-null, senao null     |

**Exemplo:**
```hemlock
let user = null;
let name = user?.name;              // null (sem erro)

let person = { name: "Alice", address: null };
let city = person?.address?.city;   // null (navegacao segura)

// Com arrays
let arr = null;
let first = arr?.[0];               // null

let items = [1, 2, 3];
let second = items?.[1];            // 2

// Com chamadas de metodo
let obj = { greet: fn() { return "Ola"; } };
let greeting = obj?.greet?.();      // "Ola"

let empty = null;
let result = empty?.method?.();     // null
```

**Comportamento:**
- Se operando esquerdo for null, toda a expressao curto-circuita para null
- Se operando esquerdo nao for null, procede com acesso normalmente
- Pode ser encadeado para acesso profundo de propriedades

---

## Operadores de Acesso a Membros

### Operador Ponto

| Operador | Nome             | Exemplo      | Descricao            |
|----------|------------------|--------------|----------------------|
| `.`      | Acesso a membro  | `obj.field`  | Acessa campo do objeto |
| `.`      | Acesso a propriedade | `arr.length` | Acessa propriedade |

**Exemplo:**
```hemlock
// Acesso a campo de objeto
let person = { name: "Alice", age: 30 };
print(person.name);        // "Alice"

// Propriedade de array
let arr = [1, 2, 3];
print(arr.length);         // 3

// Propriedade de string
let s = "hello";
print(s.length);           // 5

// Chamada de metodo
let result = s.to_upper(); // "HELLO"
```

---

### Operador de Indice

| Operador | Nome   | Exemplo   | Descricao      |
|----------|--------|-----------|----------------|
| `[]`     | Indice | `arr[i]`  | Acessa elemento |

**Exemplo:**
```hemlock
// Indexacao de array
let arr = [10, 20, 30];
print(arr[0]);             // 10
arr[1] = 99;

// Indexacao de string (retorna rune)
let s = "hello";
print(s[0]);               // 'h'
s[0] = 'H';                // "Hello"

// Indexacao de buffer
let buf = buffer(10);
buf[0] = 65;
print(buf[0]);             // 65
```

---

## Operador de Chamada de Funcao

| Operador | Nome            | Exemplo      | Descricao      |
|----------|-----------------|--------------|----------------|
| `()`     | Chamada de funcao | `f(a, b)`  | Chama funcao   |

**Exemplo:**
```hemlock
fn add(a, b) {
    return a + b;
}

let result = add(5, 3);    // 8

// Chamada de metodo
let s = "hello";
let upper = s.to_upper();  // "HELLO"

// Chamada de funcao integrada
print("mensagem");
```

---

## Precedencia de Operadores

Operadores listados da maior para a menor precedencia:

| Precedencia | Operadores                     | Descricao                            | Associatividade |
|-------------|--------------------------------|--------------------------------------|-----------------|
| 1           | `()` `[]` `.` `?.`             | Chamada, indice, membro, opcional    | Esquerda para direita |
| 2           | `++` `--`                      | Incremento/decremento sufixo         | Esquerda para direita |
| 3           | `!` `~` `-` (unario) `+` (unario) | Nao logico, complemento, negacao  | Direita para esquerda |
| 4           | `*` `/` `%`                    | Multiplicacao, divisao, modulo       | Esquerda para direita |
| 5           | `+` `-`                        | Adicao, subtracao                    | Esquerda para direita |
| 6           | `<<` `>>`                      | Shifts bit a bit                     | Esquerda para direita |
| 7           | `<` `<=` `>` `>=`              | Relacional                           | Esquerda para direita |
| 8           | `==` `!=`                      | Igualdade                            | Esquerda para direita |
| 9           | `&`                            | E bit a bit                          | Esquerda para direita |
| 10          | `^`                            | Xor bit a bit                        | Esquerda para direita |
| 11          | `|`                            | Ou bit a bit                         | Esquerda para direita |
| 12          | `&&`                           | E logico                             | Esquerda para direita |
| 13          | `||`                           | Ou logico                            | Esquerda para direita |
| 14          | `??`                           | Coalescencia nula                    | Esquerda para direita |
| 15          | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | Atribuicao | Direita para esquerda |

---

## Exemplos de Precedencia

### Exemplo 1: Aritmetica e Comparacao
```hemlock
let result = 5 + 3 * 2;
// Avaliado como: 5 + (3 * 2) = 11
// Multiplicacao tem maior precedencia que adicao

let cmp = 10 > 5 + 3;
// Avaliado como: 10 > (5 + 3) = true
// Adicao tem maior precedencia que comparacao
```

### Exemplo 2: Operadores Bit a Bit
```hemlock
let result1 = 12 | 10 & 8;
// Avaliado como: 12 | (10 & 8) = 12 | 8 = 12
// & tem maior precedencia que |

let result2 = 8 | 1 << 2;
// Avaliado como: 8 | (1 << 2) = 8 | 4 = 12
// Shift tem maior precedencia que ou bit a bit

// Use parenteses para clareza
let result3 = (5 & 3) | (2 << 1);
// Avaliado como: 1 | 4 = 5
```

### Exemplo 3: Operadores Logicos
```hemlock
let result = true || false && false;
// Avaliado como: true || (false && false) = true
// && tem maior precedencia que ||

let cmp = 5 < 10 && 10 < 20;
// Avaliado como: (5 < 10) && (10 < 20) = true
// Comparacao tem maior precedencia que &&
```

### Exemplo 4: Usando Parenteses
```hemlock
// Sem parenteses
let a = 2 + 3 * 4;        // 14

// Com parenteses
let b = (2 + 3) * 4;      // 20

// Expressao complexa
let c = (a + b) * (a - b);
```

---

## Comportamento de Operadores Especificos por Tipo

### Divisao (Sempre Retorna Float)

O operador `/` **sempre retorna ponto flutuante** (f64), independente dos tipos dos operandos:

```hemlock
print(10 / 3);             // 3.333... (f64)
print(5 / 2);              // 2.5 (f64)
print(10.0 / 4.0);         // 2.5 (f64)
print(-7 / 3);             // -2.333... (f64)
```

Isso previne erros comuns de truncamento inteiro inesperado.

### Divisao Floor (div / divi)

Para divisao floor (similar a divisao inteira em outras linguagens), use as funcoes `div()` e `divi()`:

```hemlock
// div(a, b) - divisao floor retornando float
print(div(5, 2));          // 2 (f64)
print(div(-7, 3));         // -3 (f64)  -- floor em direcao a -infinito

// divi(a, b) - divisao floor retornando inteiro
print(divi(5, 2));         // 2 (i64)
print(divi(-7, 3));        // -3 (i64)
print(typeof(divi(5, 2))); // i64
```

**Funcoes matematicas que retornam inteiro:**
Para outras operacoes de arredondamento que retornam inteiro:

```hemlock
print(floori(3.7));        // 3 (i64)
print(ceili(3.2));         // 4 (i64)
print(roundi(3.5));        // 4 (i64)
print(trunci(3.9));        // 3 (i64)

// Podem ser usados diretamente como indices de array
let arr = [10, 20, 30, 40];
print(arr[floori(1.9)]);   // 20 (indice 1)
```

### Comparacao de Strings

Strings sao comparadas lexicograficamente:

```hemlock
print("abc" < "def");      // true
print("apple" > "banana"); // false
print("hello" == "hello"); // true
```

### Comparacao com Null

```hemlock
let x = null;

print(x == null);          // true
print(x != null);          // false
```

### Erros de Tipo

Certas operacoes nao sao permitidas entre tipos incompativeis:

```hemlock
// ERRO: Nao pode usar operadores bit a bit em floats
let x = 3.14 & 2.71;

// ERRO: Nao pode usar operadores bit a bit em strings
let y = "hello" & "world";

// OK: Promocao de tipo para aritmetica
let a: u8 = 10;
let b: i32 = 20;
let c = a + b;             // i32 (promovido)
```

---

## Veja Tambem

- [Sistema de Tipos](type-system.md) - Regras de promocao e conversao de tipos
- [Funcoes Integradas](builtins.md) - Operacoes integradas
- [API de Strings](string-api.md) - Concatenacao e metodos de string
