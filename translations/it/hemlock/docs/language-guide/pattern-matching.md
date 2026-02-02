# Pattern Matching

Hemlock fornisce un potente pattern matching tramite le espressioni `match`, offrendo un modo conciso per destrutturare valori, controllare tipi e gestire casi multipli.

## Sintassi Base

```hemlock
let result = match (value) {
    pattern1 => expression1,
    pattern2 => expression2,
    _ => default_expression
};
```

Le espressioni match valutano `value` rispetto a ogni pattern in ordine, restituendo il risultato dell'espressione del primo ramo che corrisponde.

## Tipi di Pattern

### Pattern Letterali

Confronta con valori esatti:

```hemlock
let x = 42;
let msg = match (x) {
    0 => "zero",
    1 => "uno",
    42 => "la risposta",
    _ => "altro"
};
print(msg);  // "la risposta"
```

Letterali supportati:
- **Interi**: `0`, `42`, `-5`
- **Float**: `3.14`, `-0.5`
- **Stringhe**: `"hello"`, `"world"`
- **Booleani**: `true`, `false`
- **Null**: `null`

### Pattern Wildcard (`_`)

Corrisponde a qualsiasi valore senza binding:

```hemlock
let x = "qualsiasi cosa";
let result = match (x) {
    "specifico" => "trovato",
    _ => "wildcard corrispondente"
};
```

### Pattern con Binding di Variabile

Associa il valore corrispondente a una variabile:

```hemlock
let x = 100;
let result = match (x) {
    0 => "zero",
    n => "il valore e " + n  // n viene associato a 100
};
print(result);  // "il valore e 100"
```

### Pattern OR (`|`)

Corrisponde a alternative multiple:

```hemlock
let x = 2;
let size = match (x) {
    1 | 2 | 3 => "piccolo",
    4 | 5 | 6 => "medio",
    _ => "grande"
};

// Funziona anche con le stringhe
let cmd = "quit";
let action = match (cmd) {
    "exit" | "quit" | "q" => "esco",
    "help" | "h" | "?" => "mostro aiuto",
    _ => "sconosciuto"
};
```

### Espressioni Guard (`if`)

Aggiungi condizioni ai pattern:

```hemlock
let x = 15;
let category = match (x) {
    n if n < 0 => "negativo",
    n if n == 0 => "zero",
    n if n < 10 => "piccolo",
    n if n < 100 => "medio",
    n => "grande: " + n
};
print(category);  // "medio"

// Guard complesse
let y = 12;
let result = match (y) {
    n if n % 2 == 0 && n > 10 => "pari e maggiore di 10",
    n if n % 2 == 0 => "pari",
    n => "dispari"
};
```

### Pattern di Tipo

Controlla e associa in base al tipo:

```hemlock
let val = 42;
let desc = match (val) {
    num: i32 => "intero: " + num,
    str: string => "stringa: " + str,
    flag: bool => "booleano: " + flag,
    _ => "altro tipo"
};
print(desc);  // "intero: 42"
```

Tipi supportati: `i8`, `i16`, `i32`, `i64`, `u8`, `u16`, `u32`, `u64`, `f32`, `f64`, `bool`, `string`, `array`, `object`

## Pattern di Destrutturazione

### Destrutturazione di Oggetti

Estrai campi dagli oggetti:

```hemlock
let point = { x: 10, y: 20 };
let result = match (point) {
    { x, y } => "punto a " + x + "," + y
};
print(result);  // "punto a 10,20"

// Con valori di campo letterali
let origin = { x: 0, y: 0 };
let name = match (origin) {
    { x: 0, y: 0 } => "origine",
    { x: 0, y } => "sull'asse y a " + y,
    { x, y: 0 } => "sull'asse x a " + x,
    { x, y } => "punto a " + x + "," + y
};
print(name);  // "origine"
```

### Destrutturazione di Array

Confronta struttura ed elementi dell'array:

```hemlock
let arr = [1, 2, 3];
let desc = match (arr) {
    [] => "vuoto",
    [x] => "singolo: " + x,
    [x, y] => "coppia: " + x + "," + y,
    [x, y, z] => "tripla: " + x + "," + y + "," + z,
    _ => "molti elementi"
};
print(desc);  // "tripla: 1,2,3"

// Con valori letterali
let pair = [1, 2];
let result = match (pair) {
    [0, 0] => "entrambi zero",
    [1, x] => "inizia con 1, secondo e " + x,
    [x, 1] => "finisce con 1",
    _ => "altro"
};
print(result);  // "inizia con 1, secondo e 2"
```

### Pattern Rest per Array (`...`)

Cattura gli elementi rimanenti:

```hemlock
let nums = [1, 2, 3, 4, 5];

// Testa e coda
let result = match (nums) {
    [first, ...rest] => "primo: " + first,
    [] => "vuoto"
};
print(result);  // "primo: 1"

// Primi due elementi
let result2 = match (nums) {
    [a, b, ...rest] => "primi due: " + a + "," + b,
    _ => "troppo corto"
};
print(result2);  // "primi due: 1,2"
```

### Destrutturazione Annidata

Combina pattern per dati complessi:

```hemlock
let user = {
    name: "Alice",
    address: { city: "NYC", zip: 10001 }
};

let result = match (user) {
    { name, address: { city, zip } } => name + " vive a " + city,
    _ => "sconosciuto"
};
print(result);  // "Alice vive a NYC"

// Oggetto che contiene array
let data = { items: [1, 2, 3], count: 3 };
let result2 = match (data) {
    { items: [first, ...rest], count } => "primo: " + first + ", totale: " + count,
    _ => "nessun elemento"
};
print(result2);  // "primo: 1, totale: 3"
```

## Match come Espressione

Match e un'espressione che restituisce un valore:

```hemlock
// Assegnazione diretta
let grade = 85;
let letter = match (grade) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    n if n >= 70 => "C",
    n if n >= 60 => "D",
    _ => "F"
};

// In concatenazione di stringhe
let msg = "Voto: " + match (grade) {
    n if n >= 70 => "sufficiente",
    _ => "insufficiente"
};

// Nel return di funzione
fn classify(n: i32): string {
    return match (n) {
        0 => "zero",
        n if n > 0 => "positivo",
        _ => "negativo"
    };
}
```

## Best Practice per il Pattern Matching

1. **L'ordine conta**: I pattern vengono controllati dall'alto in basso; metti i pattern specifici prima di quelli generali
2. **Usa wildcard per la completezza**: Includi sempre un fallback `_` a meno che tu non sia certo che tutti i casi siano coperti
3. **Preferisci guard a condizioni annidate**: Le guard rendono l'intento piu chiaro
4. **Usa la destrutturazione invece dell'accesso manuale ai campi**: Piu conciso e sicuro

```hemlock
// Bene: Guard per il controllo del range
match (score) {
    n if n >= 90 => "A",
    n if n >= 80 => "B",
    _ => "sotto B"
}

// Bene: Destruttura invece di accedere ai campi
match (point) {
    { x: 0, y: 0 } => "origine",
    { x, y } => "a " + x + "," + y
}

// Evita: Pattern annidati eccessivamente complessi
// Considera invece di suddividere in match multipli o usare guard
```

## Confronto con Altri Linguaggi

| Funzionalita | Hemlock | Rust | JavaScript |
|---------|---------|------|------------|
| Matching base | `match (x) { ... }` | `match x { ... }` | `switch (x) { ... }` |
| Destrutturazione | Si | Si | Parziale (switch non destruttura) |
| Guard | `n if n > 0 =>` | `n if n > 0 =>` | N/D |
| Pattern OR | `1 \| 2 \| 3 =>` | `1 \| 2 \| 3 =>` | `case 1: case 2: case 3:` |
| Pattern rest | `[a, ...rest]` | `[a, rest @ ..]` | N/D |
| Pattern di tipo | `n: i32` | Tipo tramite ramo `match` | N/D |
| Restituisce valore | Si | Si | No (istruzione) |

## Note Implementative

Il pattern matching e implementato sia nel backend dell'interprete che in quello del compilatore con piena parita - entrambi producono risultati identici per lo stesso input. La funzionalita e disponibile in Hemlock v1.8.0+.
