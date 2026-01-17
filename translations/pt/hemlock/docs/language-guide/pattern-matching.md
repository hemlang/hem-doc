# Correspondencia de Padroes

Hemlock fornece correspondencia de padroes poderosa atraves de expressoes `match`, oferecendo uma forma concisa de desestruturar valores, verificar tipos e tratar multiplos casos.

## Sintaxe Basica

```hemlock
let resultado = match (valor) {
    padrao1 => expressao1,
    padrao2 => expressao2,
    _ => expressao_padrao
};
```

A expressao match compara `valor` com cada padrao em ordem, retornando o resultado da expressao do primeiro branch que corresponder.

## Tipos de Padroes

### Padroes Literais

Corresponde a valores exatos:

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "um",
    42 => "a resposta",
    _ => "outro"
};
print(msg);  // "a resposta"
```

Literais suportados:
- **Inteiros**: `0`, `42`, `-5`
- **Ponto flutuante**: `3.14`, `-0.5`
- **Strings**: `"hello"`, `"world"`
- **Booleanos**: `true`, `false`
- **Nulo**: `null`

### Padrao Curinga (`_`)

Corresponde a qualquer valor mas nao vincula:

```hemlock
let x = "qualquer coisa";
let resultado = match (x) {
    "especifico" => "encontrei",
    _ => "curinga correspondeu"
};
```

### Padrao de Vinculacao de Variavel

Vincula o valor correspondido a uma variavel:

```hemlock
let x = 100;
let resultado = match (x) {
    0 => "zero",
    n => "valor e " + n  // n vinculado a 100
};
print(resultado);  // "valor e 100"
```

### Padroes OR (`|`)

Corresponde a multiplas alternativas:

```hemlock
let x = 2;
let tamanho = match (x) {
    1 | 2 | 3 => "pequeno",
    4 | 5 | 6 => "medio",
    _ => "grande"
};

// Tambem funciona com strings
let cmd = "quit";
let acao = match (cmd) {
    "exit" | "quit" | "q" => "saindo",
    "help" | "h" | "?" => "mostrando ajuda",
    _ => "desconhecido"
};
```

### Expressoes de Guarda (`if`)

Adiciona condicoes aos padroes:

```hemlock
let x = 15;
let categoria = match (x) {
    n if n < 0 => "negativo",
    n if n == 0 => "zero",
    n if n < 10 => "pequeno",
    n if n < 100 => "medio",
    n => "grande: " + n
};
print(categoria);  // "medio"

// Guardas complexas
let y = 12;
let resultado = match (y) {
    n if n % 2 == 0 && n > 10 => "par e maior que 10",
    n if n % 2 == 0 => "par",
    n => "impar"
};
```

### Padroes de Tipo

Verifica e vincula baseado em tipo:

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "inteiro: " + num,
    str: string => "string: " + str,
    flag: bool => "booleano: " + flag,
    _ => "outro tipo"
};
print(desc);  // "inteiro: 42"
```

Tipos suportados: `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Padroes de Desestruturacao

### Desestruturacao de Objetos

Extrai campos de objetos:

```hemlock
let ponto = { x: 10, y: 20 };
let resultado = match (ponto) {
    { x, y } => "ponto em " + x + "," + y
};
print(resultado);  // "ponto em 10,20"

// Com valores literais de campos
let origem = { x: 0, y: 0 };
let nome = match (origem) {
    { x: 0, y: 0 } => "origem",
    { x: 0, y } => "no eixo y em " + y,
    { x, y: 0 } => "no eixo x em " + x,
    { x, y } => "ponto em " + x + "," + y
};
print(nome);  // "origem"
```

### Desestruturacao de Arrays

Corresponde a estrutura e elementos de arrays:

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "vazio",
    [x] => "unico: " + x,
    [x, y] => "par: " + x + "," + y,
    [x, y, z] => "tripla: " + x + "," + y + "," + z,
    _ => "muitos elementos"
};
print(desc);  // "tripla: 1,2,3"

// Com valores literais
let par = [1, 2];
let resultado = match (par) {
    [0, 0] => "ambos zero",
    [1, x] => "comeca com 1, segundo e " + x,
    [x, 1] => "termina com 1",
    _ => "outro"
};
print(resultado);  // "comeca com 1, segundo e 2"
```

### Padrao Rest de Array (`...`)

Captura elementos restantes:

```hemlock
let nums = [1, 2, 3, 4, 5];

// Cabeca e cauda
let resultado = match (nums) {
    [primeiro, ...resto] => "primeiro: " + primeiro,
    [] => "vazio"
};
print(resultado);  // "primeiro: 1"

// Dois primeiros elementos
let resultado2 = match (nums) {
    [a, b, ...resto] => "dois primeiros: " + a + "," + b,
    _ => "muito curto"
};
print(resultado2);  // "dois primeiros: 1,2"
```

### Desestruturacao Aninhada

Combina padroes para dados complexos:

```hemlock
let usuario = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let resultado = match (usuario) {
    { name, address: { city, zip } } => name + " mora em " + city,
    _ => "desconhecido"
};
print(resultado);  // "Alice mora em NYC"

// Objeto contendo array
let dados = { items: [1, 2, 3], count: 3 };
let resultado2 = match (dados) {
    { items: [primeiro, ...resto], count } => "primeiro: " + primeiro + ", total: " + count,
    _ => "sem items"
};
print(resultado2);  // "primeiro: 1, total: 3"
```

## Match como Expressao

Match e uma expressao que retorna um valor:

```hemlock
// Atribuicao direta
let nota = 85;
let letra = match (nota) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// Em concatenacao de string
let msg = "Nota: " + match (nota) {
    n if n >= 70 => "aprovado",
    _ => "reprovado"
};

// Em retorno de funcao
fn classificar(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positivo",
        _ => "negativo"
    };
}
```

## Melhores Praticas de Correspondencia de Padroes

1. **Ordem importa**: Padroes sao verificados de cima para baixo; coloque padroes especificos antes dos genericos
2. **Use curinga para completude**: Sempre inclua fallback `_` a menos que tenha certeza de que todos os casos estao cobertos
3. **Prefira guardas a condicoes aninhadas**: Guardas tornam a intencao mais clara
4. **Use desestruturacao em vez de acesso manual a campos**: Mais conciso e seguro

```hemlock
// Bom: use guardas para verificacao de intervalos
match (pontuacao) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "abaixo de B"
}

// Bom: desestruturacao em vez de acessar campos
match (ponto) {
    { x: 0, y: 0 } => "origem",
    { x, y } => "em " + x + "," + y
}

// Evite: padroes aninhados muito complexos
// Considere dividir em multiplos match ou usar guardas
```

## Comparacao com Outras Linguagens

| Recurso | Hemlock | Rust | JavaScript |
|---------|---------|------|------------|
| Match basico | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Desestruturacao | Sim | Sim | Parcial (switch nao desestrutura) |
| Guardas | `n if n > 0 =>` | `n if n > 0 =>` | N/A |
| Padroes OR | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Padroes rest | `[a, ...resto]` | `[a, resto @ ..]` | N/A |
| Padroes de tipo | `n: i32` | Via tipos em branches `match` | N/A |
| Retorna valor | Sim | Sim | Nao (declaracao) |

## Notas de Implementacao

Correspondencia de padroes e implementada tanto no interpretador quanto no backend do compilador com paridade completa - ambos produzem resultados identicos para a mesma entrada. O recurso esta disponivel no Hemlock v1.8.0+.
