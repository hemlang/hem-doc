# Fluxo de Controle

Hemlock fornece fluxo de controle familiar no estilo C, exigindo o uso obrigatório de chaves e sintaxe explícita. Este guia abrange declarações condicionais, loops, declarações switch e operadores.

## Visao Geral

Recursos de fluxo de controle disponíveis:

- `if`/`else`/`else if` - Ramificação condicional
- `while` loops - Iteração baseada em condição
- `for` loops - Estilo C e iteração for-in
- `loop` - Loop infinito (mais claro que `while (true)`)
- Declarações `switch` - Ramificação múltipla
- `break`/`continue` - Controle de loop
- Rótulos de loop - break/continue direcionado para loops aninhados
- `defer` - Execução adiada (limpeza)
- Operadores booleanos: `&&`, `||`, `!`
- Operadores de comparação: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Operadores bit a bit: `&`, `|`, `^`, `<<`, `>>`, `~`

## Declarações If

### If/Else Básico

```hemlock
if (x > 10) {
    print("grande");
} else {
    print("pequeno");
}
```

**Regras:**
- Todas as ramificações **devem** usar chaves
- Condições devem estar entre parênteses
- Chaves opcionais não são suportadas (diferente de C)

### If Sem Else

```hemlock
if (x > 0) {
    print("positivo");
}
// Ramificação else não é necessária
```

### Cadeia Else-If

```hemlock
if (x > 100) {
    print("muito grande");
} else if (x > 50) {
    print("grande");
} else if (x > 10) {
    print("médio");
} else {
    print("pequeno");
}
```

**Nota:** `else if` é açúcar sintático para declarações if aninhadas. As duas formas a seguir são equivalentes:

```hemlock
// else if (açúcar sintático)
if (a) {
    foo();
} else if (b) {
    bar();
}

// if aninhado equivalente
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### Declarações If Aninhadas

```hemlock
if (x > 0) {
    if (x < 10) {
        print("dígito único positivo");
    } else {
        print("múltiplos dígitos positivos");
    }
} else {
    print("não positivo");
}
```

## Loops While

Iteração baseada em condição:

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**Loop infinito (estilo antigo):**
```hemlock
while (true) {
    // ... executar trabalho
    if (should_exit) {
        break;
    }
}
```

**Nota:** Para loops infinitos, recomenda-se usar a palavra-chave `loop` (veja abaixo).

## Loop (Loop Infinito)

A palavra-chave `loop` fornece uma sintaxe mais clara para loops infinitos:

```hemlock
loop {
    // ... executar trabalho
    if (should_exit) {
        break;
    }
}
```

**Equivalente a `while (true)`, mas com intenção mais clara.**

### Loop Básico com Break

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Saída: 0, 1, 2, 3, 4
```

### Loop com Continue

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // Pula a impressão de 3
    }
    print(i);
}
// Saída: 1, 2, 4, 5
```

### Loops Aninhados

```hemlock
let x = 0;
loop {
    if (x >= 2) { break; }
    let y = 0;
    loop {
        if (y >= 3) { break; }
        print(x * 10 + y);
        y = y + 1;
    }
    x = x + 1;
}
// Saída: 0, 1, 2, 10, 11, 12
```

### Quando Usar Loop

- **Use `loop`** - Para loops infinitos intencionais, saindo com `break`
- **Use `while`** - Quando há uma condição natural de término
- **Use `for`** - Ao iterar um número conhecido de vezes ou sobre coleções

## Loops For

### For Estilo C

Loop for clássico de três partes:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Componentes:**
- **Inicializador**: `let i = 0` - Executa uma vez antes do loop
- **Condição**: `i < 10` - Verificada antes de cada iteração
- **Atualização**: `i = i + 1` - Executa após cada iteração

**Escopo:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i não é acessível aqui (escopo do loop)
```

### Loops For-In

Itera sobre elementos de array:

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // Imprime cada elemento
}
```

**Com índice e valor:**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Índice: ${i}, Valor: ${arr[i]}`);
}
```

## Declarações Switch

Ramificação múltipla baseada em valor:

### Switch Básico

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("um");
        break;
    case 2:
        print("dois");
        break;
    case 3:
        print("três");
        break;
}
```

### Switch com Default

```hemlock
let color = "azul";

switch (color) {
    case "vermelho":
        print("parar");
        break;
    case "amarelo":
        print("desacelerar");
        break;
    case "verde":
        print("seguir");
        break;
    default:
        print("cor desconhecida");
        break;
}
```

**Regras:**
- `default` executa quando nenhum outro case corresponde
- `default` pode aparecer em qualquer posição no corpo do switch
- Apenas um case default é permitido

### Comportamento de Fall-through

Cases sem `break` passam para o próximo case (comportamento estilo C). Isso é **intencional** e pode ser usado para agrupar cases:

```hemlock
let nota = 85;

switch (nota) {
    case 100:
    case 95:
    case 90:
        print("A");
        break;
    case 85:
    case 80:
        print("B");
        break;
    default:
        print("C ou abaixo");
        break;
}
```

**Exemplo de fall-through explícito:**
```hemlock
let dia = 3;

switch (dia) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Dia de semana");
        break;
    case 6:
    case 7:
        print("Fim de semana");
        break;
}
```

**Importante:** Diferente de algumas linguagens modernas, Hemlock não requer uma palavra-chave `fallthrough` explícita. A menos que terminados com `break`, `return` ou `throw`, cases passam automaticamente para o próximo. Sempre use `break` para evitar fall-through acidental.

### Switch com Return

Em funções, `return` sai imediatamente do switch:

```hemlock
fn get_day_name(dia: i32): string {
    switch (dia) {
        case 1:
            return "Segunda";
        case 2:
            return "Terça";
        case 3:
            return "Quarta";
        default:
            return "Desconhecido";
    }
}
```

### Tipos de Valor em Switch

Switch funciona com qualquer tipo de valor:

```hemlock
// Inteiros
switch (contador) {
    case 0: print("zero"); break;
    case 1: print("um"); break;
}

// Strings
switch (nome) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// Booleanos
switch (flag) {
    case true: print("ligado"); break;
    case false: print("desligado"); break;
}
```

**Nota:** Cases usam igualdade de valor para comparação.

## Break e Continue

### Break

Sai do loop ou switch mais interno:

```hemlock
// Em loop
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // Sai do loop
    }
    print(i);
    i = i + 1;
}

// Em switch
switch (x) {
    case 1:
        print("um");
        break;  // Sai do switch
    case 2:
        print("dois");
        break;
}
```

### Continue

Pula para a próxima iteração do loop:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // Pula quando i é 5
    }
    print(i);  // Imprime 0,1,2,3,4,6,7,8,9
}
```

**Diferença:**
- `break` - Sai completamente do loop
- `continue` - Pula para a próxima iteração

## Rótulos de Loop

Rótulos de loop permitem que `break` e `continue` direcionem loops externos específicos, não apenas o loop mais interno. Isso é útil em loops aninhados onde você precisa controlar o loop externo a partir do loop interno.

### Break com Rótulo

Sai do loop externo a partir do loop interno:

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // Sai do while externo
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// Saída: 0, 1, 2, 10 (para em i=1, j=1)
```

### Continue com Rótulo

Pula para a próxima iteração do loop externo:

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // Pula o resto do loop interno, continua o externo
        }
        print(i * 10 + j);
    }
}
// Quando i=2, j=1: pula para a próxima iteração do loop externo
```

### Rótulos em Loops For

Rótulos funcionam com todos os tipos de loop:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 3; y = y + 1) {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
    }
}
```

### Rótulos em Loops For-In

```hemlock
let arr1 = [1, 2, 3];
let arr2 = [10, 20, 30];

outer: for (let a in arr1) {
    for (let b in arr2) {
        if (a == 2 && b == 20) {
            break outer;
        }
        print(a * 100 + b);
    }
}
```

### Rótulos com Palavra-chave Loop

```hemlock
let x = 0;
outer: loop {
    let y = 0;
    loop {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
        y = y + 1;
        if (y >= 3) { break; }
    }
    x = x + 1;
    if (x >= 3) { break; }
}
```

### Múltiplos Rótulos

Você pode usar rótulos em diferentes níveis de aninhamento:

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // Pula para a próxima iteração do loop do meio
            }
            if (a == 1 && b == 1) {
                break outer;      // Sai do loop mais externo
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### Break/Continue Sem Rótulo em Loops com Rótulo

`break` e `continue` sem rótulo ainda funcionam normalmente (afetam o loop mais interno), mesmo quando loops externos têm rótulos:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // Sai apenas do loop interno
        }
        print(x * 10 + y);
    }
}
// Saída: 0, 1, 10, 11, 20, 21
```

### Sintaxe de Rótulos

- Rótulos são identificadores seguidos de dois-pontos
- Rótulos devem preceder imediatamente a declaração do loop (`while`, `for`, `loop`)
- Nomes de rótulos seguem regras de identificadores (letras, números, sublinhados)
- Convenções comuns: `outer`, `inner`, `row`, `col`, nomes descritivos

## Declaração Defer

A declaração `defer` agenda código para ser executado quando a função atual retorna. Isso é útil para operações de limpeza como fechar arquivos, liberar recursos ou desbloquear.

### Defer Básico

```hemlock
fn example() {
    print("início");
    defer print("limpeza");  // Executa quando a função retorna
    print("fim");
}

example();
// Saída:
// início
// fim
// limpeza
```

**Comportamento chave:**
- Declarações defer executam **após** o corpo da função completar
- Declarações defer executam **antes** da função retornar ao chamador
- Declarações defer sempre executam mesmo se a função lançar uma exceção

### Múltiplos Defer (Ordem LIFO)

Quando usando múltiplas declarações `defer`, elas executam em **ordem reversa** (último a entrar, primeiro a sair):

```hemlock
fn example() {
    defer print("primeiro");   // Executa por último
    defer print("segundo");    // Executa em segundo
    defer print("terceiro");   // Executa primeiro
    print("corpo");
}

example();
// Saída:
// corpo
// terceiro
// segundo
// primeiro
```

Esta ordem LIFO é intencional - corresponde à ordem natural de limpeza de recursos aninhados (fechar recursos internos antes dos externos).

### Defer com Return

Declarações defer executam antes de `return` transferir controle:

```hemlock
fn get_value(): i32 {
    defer print("limpeza");
    print("antes do return");
    return 42;
}

let resultado = get_value();
print("resultado:", resultado);
// Saída:
// antes do return
// limpeza
// resultado: 42
```

### Defer com Exceções

Declarações defer executam mesmo se uma exceção for lançada:

```hemlock
fn arriscado() {
    defer print("limpeza 1");
    defer print("limpeza 2");
    print("antes do throw");
    throw "erro!";
    print("depois do throw");  // Nunca executa
}

try {
    arriscado();
} catch (e) {
    print("Capturado:", e);
}
// Saída:
// antes do throw
// limpeza 2
// limpeza 1
// Capturado: erro!
```

### Padrão de Limpeza de Recursos

O principal caso de uso para `defer` é garantir que recursos sejam limpos:

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // Sempre fecha, mesmo em erro

    let content = file.read();
    // ... processar conteúdo ...

    // Arquivo fecha automaticamente quando a função retorna
}
```

**Sem defer (propenso a erros):**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // Se lançar aqui, file.close() nunca é chamado!
    process(content);
    file.close();
}
```

### Defer com Closures

Defer pode usar closures para capturar estado:

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Liberando recurso");
        release(resource);
    }();  // Nota: expressão de função imediatamente invocada

    use_resource(resource);
}
```

### Quando Usar Defer

**Use defer para:**
- Fechar arquivos e conexões de rede
- Liberar memória alocada
- Liberar locks e mutexes
- Limpeza em qualquer função que adquire recursos

**Defer vs Finally:**
- `defer` é mais simples para limpeza de único recurso
- `try/finally` é melhor para tratamento de erros complexo com recuperação

### Melhores Práticas

1. **Use defer imediatamente após adquirir o recurso:**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... usar arquivo ...
   ```

2. **Use múltiplos defer para múltiplos recursos:**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // Ambos os arquivos fecharão em ordem reversa
   ```

3. **Lembre da ordem LIFO para recursos dependentes:**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner é liberado antes de outer (ordem de dependência correta)
   ```

## Operadores Booleanos

### E Lógico (`&&`)

Ambas as condições devem ser verdadeiras:

```hemlock
if (x > 0 && x < 10) {
    print("dígito único positivo");
}
```

**Avaliação de curto-circuito:**
```hemlock
if (false && expensive_check()) {
    // expensive_check() nunca é chamada
}
```

### OU Lógico (`||`)

Pelo menos uma condição deve ser verdadeira:

```hemlock
if (x < 0 || x > 100) {
    print("fora do intervalo");
}
```

**Avaliação de curto-circuito:**
```hemlock
if (true || expensive_check()) {
    // expensive_check() nunca é chamada
}
```

### NAO Lógico (`!`)

Nega valor booleano:

```hemlock
if (!is_valid) {
    print("inválido");
}

if (!(x > 10)) {
    // Equivalente a: if (x <= 10)
}
```

## Operadores de Comparação

### Igualdade

```hemlock
if (x == 10) { }    // Igual a
if (x != 10) { }    // Diferente de
```

Funciona com todos os tipos:
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### Operadores Relacionais

```hemlock
if (x < 10) { }     // Menor que
if (x > 10) { }     // Maior que
if (x <= 10) { }    // Menor ou igual
if (x >= 10) { }    // Maior ou igual
```

**Promoção de tipo se aplica:**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true (i32 promovido para i64)
```

## Operadores Bit a Bit

Hemlock fornece operadores bit a bit para manipulação de inteiros. Estes **só podem ser usados com tipos inteiros** (i8-i64, u8-u64).

### Operadores Bit a Bit Binários

**E bit a bit (`&`)**
```hemlock
let a = 12;  // Binário 1100
let b = 10;  // Binário 1010
print(a & b);   // 8 (1000)
```

**OU bit a bit (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**XOR bit a bit (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**Deslocamento à esquerda (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - desloca 2 bits à esquerda
```

**Deslocamento à direita (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - desloca 1 bit à direita
```

### Operador Bit a Bit Unário

**Complemento bit a bit (`~`)**
```hemlock
let a = 12;
print(~a);      // -13 (complemento de dois)

let c: u8 = 15;   // Binário 00001111
print(~c);        // 240 (11110000), tipo u8
```

### Exemplos de Operações Bit a Bit

**Usando tipos sem sinal:**
```hemlock
let c: u8 = 15;   // Binário 00001111
let d: u8 = 7;    // Binário 00000111

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - tipo u8
```

**Preservação de tipo:**
```hemlock
// Operações bit a bit preservam o tipo dos operandos
let x: u8 = 255;
let resultado = ~x;  // resultado é u8, valor 0

let y: i32 = 100;
let resultado2 = y << 2;  // resultado2 é i32, valor 400
```

**Padrões comuns:**
```hemlock
// Verificar se bit está definido
if (flags & 0x04) {
    print("bit 2 está definido");
}

// Definir bit
flags = flags | 0x08;

// Limpar bit
flags = flags & ~0x02;

// Alternar bit
flags = flags ^ 0x01;
```

### Precedência de Operadores

Operadores bit a bit seguem precedência estilo C:

1. `~` (negação unária) - Mais alta, mesmo nível que `!` e `-`
2. `<<`, `>>` (deslocamento) - Acima de comparação, abaixo de `+`/`-`
3. `&` (E bit a bit) - Acima de `^` e `|`
4. `^` (XOR bit a bit) - Entre `&` e `|`
5. `|` (OU bit a bit) - Abaixo de `&` e `^`, acima de `&&`
6. `&&`, `||` (lógicos) - Precedência mais baixa

**Exemplos:**
```hemlock
// & tem precedência maior que |
let resultado1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// Deslocamento tem precedência maior que operadores bit a bit
let resultado2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// Use parênteses para clareza
let resultado3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**Notas importantes:**
- Operadores bit a bit só funcionam com tipos inteiros (não float, string, etc.)
- Promoção de tipo segue regras padrão (tipos menores promovidos para maiores)
- Deslocamento à direita (`>>`) é aritmético para tipos com sinal, lógico para sem sinal
- Quantidade de deslocamento não é verificada por intervalo (comportamento depende da plataforma)

## Precedência de Operadores (Completa)

Da maior para a menor precedência:

1. **Unário**: `!`, `-`, `~`
2. **Multiplicativo**: `*`, `/`, `%`
3. **Aditivo**: `+`, `-`
4. **Deslocamento**: `<<`, `>>`
5. **Relacional**: `<`, `>`, `<=`, `>=`
6. **Igualdade**: `==`, `!=`
7. **E bit a bit**: `&`
8. **XOR bit a bit**: `^`
9. **OU bit a bit**: `|`
10. **E lógico**: `&&`
11. **OU lógico**: `||`

**Use parênteses para clareza:**
```hemlock
// Não claro
if (a || b && c) { }

// Claro
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## Padrões Comuns

### Padrão: Validação de Entrada

```hemlock
fn validate_age(idade: i32): bool {
    if (idade < 0 || idade > 150) {
        return false;
    }
    return true;
}
```

### Padrão: Verificação de Intervalo

```hemlock
fn in_range(valor: i32, min: i32, max: i32): bool {
    return valor >= min && valor <= max;
}

if (in_range(pontuacao, 0, 100)) {
    print("pontuação válida");
}
```

### Padrão: Máquina de Estados

```hemlock
let estado = "inicio";

while (true) {
    switch (estado) {
        case "inicio":
            print("Iniciando...");
            estado = "executando";
            break;

        case "executando":
            if (should_pause) {
                estado = "pausado";
            } else if (should_stop) {
                estado = "parado";
            }
            break;

        case "pausado":
            if (should_resume) {
                estado = "executando";
            }
            break;

        case "parado":
            print("Parado");
            break;
    }

    if (estado == "parado") {
        break;
    }
}
```

### Padrão: Iteração com Filtro

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Imprime apenas números pares
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // Pula ímpares
    }
    print(arr[i]);
}
```

### Padrão: Saída Antecipada

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Saída antecipada
        }
    }
    return -1;  // Não encontrado
}
```

## Melhores Práticas

1. **Sempre use chaves** - Mesmo para blocos de única declaração (sintaxe força)
2. **Condições explícitas** - Use `x == 0` em vez de `!x` para clareza
3. **Evite aninhamento profundo** - Extraia condições aninhadas para funções
4. **Use retorno antecipado** - Use cláusulas de guarda para reduzir aninhamento
5. **Decomponha condições complexas** - Divida em variáveis booleanas nomeadas
6. **Use default em switch** - Sempre inclua case default
7. **Comente fall-through** - Torne fall-through intencional explícito

## Armadilhas Comuns

### Armadilha: Atribuição em Condição

```hemlock
// Isso não é permitido (não pode atribuir em condição)
if (x = 10) { }  // Erro: erro de sintaxe

// Use comparação em vez disso
if (x == 10) { }  // OK
```

### Armadilha: Break Faltando em Switch

```hemlock
// Fall-through acidental
switch (x) {
    case 1:
        print("um");
        // Break faltando - vai passar para o próximo!
    case 2:
        print("dois");  // Executa para 1 e 2
        break;
}

// Corrigido: adicione break
switch (x) {
    case 1:
        print("um");
        break;  // Agora correto
    case 2:
        print("dois");
        break;
}
```

### Armadilha: Escopo de Variável de Loop

```hemlock
// i tem escopo limitado ao loop
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // Erro: i não está definido aqui
```

## Exemplos

### Exemplo: FizzBuzz

```hemlock
for (let i = 1; i <= 100; i = i + 1) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else if (i % 3 == 0) {
        print("Fizz");
    } else if (i % 5 == 0) {
        print("Buzz");
    } else {
        print(i);
    }
}
```

### Exemplo: Verificação de Número Primo

```hemlock
fn is_prime(n: i32): bool {
    if (n < 2) {
        return false;
    }

    let i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
```

### Exemplo: Sistema de Menu

```hemlock
fn menu() {
    while (true) {
        print("1. Iniciar");
        print("2. Configurações");
        print("3. Sair");

        let escolha = get_input();

        switch (escolha) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Até logo!");
                return;
            default:
                print("Escolha inválida");
                break;
        }
    }
}
```

## Tópicos Relacionados

- [Funções](functions.md) - Fluxo de controle de chamadas e retornos de função
- [Tratamento de Erros](error-handling.md) - Fluxo de controle de exceções
- [Tipos](types.md) - Conversão de tipos em condições

## Veja Também

- **Sintaxe**: Veja [Sintaxe](syntax.md) para detalhes de sintaxe de declarações
- **Operadores**: Veja [Tipos](types.md) para promoção de tipos em operações
