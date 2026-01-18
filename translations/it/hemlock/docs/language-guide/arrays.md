# Array

Hemlock fornisce **array dinamici** con metodi completi per la manipolazione e l'elaborazione dei dati. Gli array possono contenere tipi misti e crescono automaticamente secondo necessita.

## Panoramica

```hemlock
// Letterali array
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipi misti consentiti
let mixed = [1, "ciao", true, null];

// Dimensionamento dinamico
arr.push(6);           // Cresce automaticamente
arr.push(7);
print(arr.length);     // 7
```

## Letterali array

### Sintassi di base

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["mela", "banana", "ciliegia"];
let booleans = [true, false, true];
```

### Array vuoti

```hemlock
let arr = [];  // Array vuoto

// Aggiungere elementi dopo
arr.push(1);
arr.push(2);
arr.push(3);
```

### Tipi misti

Gli array possono contenere tipi diversi:

```hemlock
let mixed = [
    42,
    "ciao",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "ciao"
print(mixed[4]);  // [1, 2, 3] (array annidato)
```

### Array annidati

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

### Array tipizzati

Gli array possono avere annotazioni di tipo per imporre i tipi degli elementi:

```hemlock
// Sintassi array tipizzato
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Verifica del tipo a runtime
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "due", 3]; // Errore runtime: tipo non corrispondente

// Array tipizzati annidati
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Comportamento dell'annotazione di tipo:**
- Gli elementi vengono verificati quando aggiunti all'array
- Le incompatibilita di tipo causano errori a runtime
- Senza annotazione di tipo, gli array accettano tipi misti

## Indicizzazione

### Lettura degli elementi

Accesso con indice da zero:

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (primo elemento)
print(arr[4]);  // 50 (ultimo elemento)

// Fuori dai limiti restituisce null (nessun errore)
print(arr[10]);  // null
```

### Scrittura degli elementi

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Modificare esistente
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Puo assegnare oltre la lunghezza attuale (fa crescere l'array)
arr[5] = 60;    // Crea [10, 20, 3, null, null, 60]
```

### Indici negativi

**Non supportati** - Usa solo indici positivi:

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // ERRORE o comportamento indefinito

// Usa length per l'ultimo elemento
print(arr[arr.length - 1]);  // 3
```

## Proprieta

### Proprieta `.length`

Restituisce il numero di elementi:

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Array vuoto
let empty = [];
print(empty.length);  // 0

// Dopo le modifiche
arr.push(6);
print(arr.length);  // 6
```

## Metodi array

Hemlock fornisce 18 metodi array per una manipolazione completa.

### Operazioni stack

**`push(value)`** - Aggiunge elemento alla fine:
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Rimuove e restituisce l'ultimo elemento:
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Restituisce 5, arr e ora [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Operazioni coda

**`shift()`** - Rimuove e restituisce il primo elemento:
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Restituisce 1, arr e ora [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Aggiunge elemento all'inizio:
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Inserimento e rimozione

**`insert(index, value)`** - Inserisce elemento all'indice:
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // Inserisce 3 all'indice 2: [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Inserisce all'inizio: [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Rimuove e restituisce elemento all'indice:
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Restituisce 3, arr e ora [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Operazioni di ricerca

**`find(value)`** - Trova la prima occorrenza:
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (indice della prima occorrenza)
let idx2 = arr.find(99);     // -1 (non trovato)

// Funziona con qualsiasi tipo
let words = ["mela", "banana", "ciliegia"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - Verifica se l'array contiene il valore:
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Operazioni di estrazione

**`slice(start, end)`** - Estrae sottoarray (end esclusivo):
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (indici 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Originale invariato
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Ottiene il primo elemento (senza rimuovere):
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (senza rimuovere)
print(arr);                  // [1, 2, 3] (invariato)
```

**`last()`** - Ottiene l'ultimo elemento (senza rimuovere):
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (senza rimuovere)
print(arr);                  // [1, 2, 3] (invariato)
```

### Operazioni di trasformazione

**`reverse()`** - Inverte l'array sul posto:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (modificato)
```

**`join(delimiter)`** - Unisce gli elementi in una stringa:
```hemlock
let words = ["ciao", "mondo", "foo"];
let joined = words.join(" ");  // "ciao mondo foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Funziona con tipi misti
let mixed = [1, "ciao", true, null];
print(mixed.join(" | "));  // "1 | ciao | true | null"
```

**`concat(other)`** - Concatena con un altro array:
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (nuovo array)

// Originali invariati
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Operazioni di utilita

**`clear()`** - Rimuove tutti gli elementi:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Concatenamento dei metodi

I metodi che restituiscono array o valori consentono il concatenamento:

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["mela", "banana", "ciliegia"]
    .slice(0, 2)
    .join(" e ");  // "mela e banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Riferimento completo dei metodi

| Metodo | Parametri | Restituisce | Muta | Descrizione |
|--------|-----------|-------------|------|-------------|
| `push(value)` | any | void | Si | Aggiunge elemento alla fine |
| `pop()` | - | any | Si | Rimuove e restituisce l'ultimo |
| `shift()` | - | any | Si | Rimuove e restituisce il primo |
| `unshift(value)` | any | void | Si | Aggiunge elemento all'inizio |
| `insert(index, value)` | i32, any | void | Si | Inserisce all'indice |
| `remove(index)` | i32 | any | Si | Rimuove e restituisce all'indice |
| `find(value)` | any | i32 | No | Trova prima occorrenza (-1 se non trovato) |
| `contains(value)` | any | bool | No | Verifica se contiene il valore |
| `slice(start, end)` | i32, i32 | array | No | Estrae sottoarray (nuovo array) |
| `join(delimiter)` | string | string | No | Unisce in stringa |
| `concat(other)` | array | array | No | Concatena (nuovo array) |
| `reverse()` | - | void | Si | Inverte sul posto |
| `first()` | - | any | No | Ottiene primo elemento |
| `last()` | - | any | No | Ottiene ultimo elemento |
| `clear()` | - | void | Si | Rimuove tutti gli elementi |
| `map(callback)` | fn | array | No | Trasforma ogni elemento |
| `filter(predicate)` | fn | array | No | Seleziona elementi corrispondenti |
| `reduce(callback, initial)` | fn, any | any | No | Riduce a singolo valore |

## Dettagli di implementazione

### Modello di memoria

- **Allocato nell'heap** - Capacita dinamica
- **Crescita automatica** - Raddoppia la capacita quando superata
- **Nessun restringimento automatico** - La capacita non diminuisce
- **Nessun controllo dei limiti sull'indicizzazione** - Usa i metodi per la sicurezza

### Gestione della capacita

```hemlock
let arr = [];  // Capacita iniziale: 0

arr.push(1);   // Cresce a capacita 1
arr.push(2);   // Cresce a capacita 2
arr.push(3);   // Cresce a capacita 4 (raddoppia)
arr.push(4);   // Ancora capacita 4
arr.push(5);   // Cresce a capacita 8 (raddoppia)
```

### Confronto dei valori

`find()` e `contains()` usano l'uguaglianza di valore:

```hemlock
// Primitivi: confronto per valore
let arr = [1, 2, 3];
arr.contains(2);  // true

// Stringhe: confronto per valore
let words = ["ciao", "mondo"];
words.contains("ciao");  // true

// Oggetti: confronto per riferimento
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (stesso riferimento)
arr2.contains(obj2);  // false (riferimento diverso)
```

## Pattern comuni

### Operazioni funzionali (map/filter/reduce)

Gli array hanno metodi integrati `map`, `filter` e `reduce`:

```hemlock
// map - trasforma ogni elemento
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - seleziona elementi corrispondenti
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - accumula in singolo valore
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Concatenamento di operazioni funzionali
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Pattern: Array come stack

```hemlock
let stack = [];

// Push sullo stack
stack.push(1);
stack.push(2);
stack.push(3);

// Pop dallo stack
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Pattern: Array come coda

```hemlock
let queue = [];

// Enqueue (aggiungi alla fine)
queue.push(1);
queue.push(2);
queue.push(3);

// Dequeue (rimuovi dalla testa)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Buone pratiche

1. **Usa i metodi invece dell'indicizzazione diretta** - Controllo dei limiti e chiarezza
2. **Controlla i limiti** - L'indicizzazione diretta non controlla i limiti
3. **Preferisci operazioni immutabili** - Usa `slice()` e `concat()` invece della mutazione
4. **Inizializza con capacita** - Se conosci la dimensione (non attualmente supportato)
5. **Usa `contains()` per l'appartenenza** - Piu chiaro dei cicli manuali
6. **Concatena i metodi** - Piu leggibile delle chiamate annidate

## Trabocchetti comuni

### Trabocchetto: Indice diretto fuori dai limiti

```hemlock
let arr = [1, 2, 3];

// Nessun controllo dei limiti!
arr[10] = 99;  // Crea array sparso con null
print(arr.length);  // 11 (non 3!)

// Meglio: Usa push() o controlla la lunghezza
if (arr.length <= 10) {
    arr.push(99);
}
```

### Trabocchetto: Mutazione vs. Nuovo array

```hemlock
let arr = [1, 2, 3];

// Muta l'originale
arr.reverse();
print(arr);  // [3, 2, 1]

// Restituisce nuovo array
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (invariato)
print(sub);  // [3, 2]
```

### Trabocchetto: Uguaglianza per riferimento

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Stesso riferimento: true
arr.contains(obj);  // true

// Riferimento diverso: false
arr.contains({ x: 10 });  // false (oggetto diverso)
```

### Trabocchetto: Array a lunga durata

```hemlock
// Gli array nello scope locale vengono liberati automaticamente, ma gli array globali/a lunga durata richiedono attenzione
let global_cache = [];  // Livello modulo, persiste fino alla fine del programma

fn add_to_cache(item) {
    global_cache.push(item);  // Cresce indefinitamente
}

// Per dati a lunga durata, considera:
// - Svuotare l'array periodicamente: global_cache.clear();
// - Liberare anticipatamente quando finito: free(global_cache);
```

## Esempi

### Esempio: Statistiche array

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

### Esempio: Deduplicazione array

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

### Esempio: Suddivisione in chunk

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

### Esempio: Appiattimento array

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Array annidato - appiattiscilo
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

### Esempio: Ordinamento (Bubble Sort)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Scambia
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
sort(numbers);  // Modifica sul posto
print(numbers);  // [1, 2, 5, 8, 9]
```

## Limitazioni

Limitazioni attuali:

- **Nessun controllo dei limiti sull'indicizzazione** - L'accesso diretto non e controllato
- **Uguaglianza per riferimento per gli oggetti** - `find()` e `contains()` usano confronto per riferimento
- **Nessuna destrutturazione array** - Nessuna sintassi `let [a, b] = arr`
- **Nessun operatore spread** - Nessuna sintassi `[...arr1, ...arr2]`

**Nota:** Gli array sono conteggiati per riferimento e liberati automaticamente quando lo scope termina. Vedi [Gestione della memoria](memory.md#conteggio-interno-dei-riferimenti) per i dettagli.

## Argomenti correlati

- [Stringhe](strings.md) - Metodi stringa simili ai metodi array
- [Oggetti](objects.md) - Gli array sono anche simili agli oggetti
- [Funzioni](functions.md) - Funzioni di ordine superiore con array
- [Flusso di controllo](control-flow.md) - Iterazione sugli array

## Vedi anche

- **Dimensionamento dinamico**: Gli array crescono automaticamente con raddoppio della capacita
- **Metodi**: 18 metodi completi per la manipolazione inclusi map/filter/reduce
- **Memoria**: Vedi [Memoria](memory.md) per i dettagli sull'allocazione degli array
