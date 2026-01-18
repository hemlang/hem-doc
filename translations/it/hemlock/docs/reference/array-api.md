# Riferimento API degli Array

Riferimento completo per il tipo array di Hemlock e tutti i suoi 18 metodi.

---

## Panoramica

Gli array in Hemlock sono sequenze **dinamiche, allocate nell'heap** che possono contenere tipi misti. Forniscono metodi completi per la manipolazione e l'elaborazione dei dati.

**Caratteristiche Principali:**
- Dimensionamento dinamico (crescita automatica)
- Indicizzazione a base zero
- Tipi misti consentiti
- 18 metodi integrati
- Allocati nell'heap con tracciamento della capacità

---

## Tipo Array

**Tipo:** `array`

**Proprietà:**
- `.length` - Numero di elementi (i32)

**Sintassi Letterale:** Parentesi quadre `[elem1, elem2, ...]`

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);     // 5

// Tipi misti
let misto = [1, "ciao", true, null];
print(misto.length);   // 4

// Array vuoto
let vuoto = [];
print(vuoto.length);   // 0
```

---

## Indicizzazione

Gli array supportano l'indicizzazione a base zero usando `[]`:

**Accesso in Lettura:**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);         // 10
print(arr[1]);         // 20
print(arr[2]);         // 30
```

**Accesso in Scrittura:**
```hemlock
let arr = [10, 20, 30];
arr[0] = 99;
arr[1] = 88;
print(arr);            // [99, 88, 30]
```

**Nota:** L'indicizzazione diretta non ha controllo dei limiti. Usa i metodi per maggiore sicurezza.

---

## Proprietà degli Array

### .length

Ottiene il numero di elementi nell'array.

**Tipo:** `i32`

**Esempi:**
```hemlock
let arr = [1, 2, 3];
print(arr.length);     // 3

let vuoto = [];
print(vuoto.length);   // 0

// La lunghezza cambia dinamicamente
arr.push(4);
print(arr.length);     // 4

arr.pop();
print(arr.length);     // 3
```

---

## Metodi degli Array

### Operazioni di Stack

#### push

Aggiunge un elemento alla fine dell'array.

**Firma:**
```hemlock
array.push(valore: any): null
```

**Parametri:**
- `valore` - Elemento da aggiungere

**Restituisce:** `null`

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]
arr.push("ciao");      // [1, 2, 3, 4, 5, "ciao"]
```

---

#### pop

Rimuove e restituisce l'ultimo elemento.

**Firma:**
```hemlock
array.pop(): any
```

**Restituisce:** Ultimo elemento (rimosso dall'array)

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3];
let ultimo = arr.pop();  // 3
print(arr);              // [1, 2]

let ultimo2 = arr.pop(); // 2
print(arr);              // [1]
```

**Errore:** Errore a runtime se l'array è vuoto.

---

### Operazioni di Coda

#### shift

Rimuove e restituisce il primo elemento.

**Firma:**
```hemlock
array.shift(): any
```

**Restituisce:** Primo elemento (rimosso dall'array)

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3];
let primo = arr.shift();   // 1
print(arr);                // [2, 3]

let primo2 = arr.shift();  // 2
print(arr);                // [3]
```

**Errore:** Errore a runtime se l'array è vuoto.

---

#### unshift

Aggiunge un elemento all'inizio dell'array.

**Firma:**
```hemlock
array.unshift(valore: any): null
```

**Parametri:**
- `valore` - Elemento da aggiungere

**Restituisce:** `null`

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [2, 3];
arr.unshift(1);        // [1, 2, 3]
arr.unshift(0);        // [0, 1, 2, 3]
```

---

### Inserimento e Rimozione

#### insert

Inserisce un elemento a un indice specifico.

**Firma:**
```hemlock
array.insert(indice: i32, valore: any): null
```

**Parametri:**
- `indice` - Posizione di inserimento (base 0)
- `valore` - Elemento da inserire

**Restituisce:** `null`

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // [1, 2, 3, 4, 5]

let arr2 = [1, 3];
arr2.insert(1, 2);     // [1, 2, 3]

// Inserisci alla fine
arr2.insert(arr2.length, 4);  // [1, 2, 3, 4]
```

**Comportamento:** Sposta gli elementi dall'indice in poi verso destra.

---

#### remove

Rimuove e restituisce l'elemento all'indice specificato.

**Firma:**
```hemlock
array.remove(indice: i32): any
```

**Parametri:**
- `indice` - Posizione da cui rimuovere (base 0)

**Restituisce:** Elemento rimosso

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let rimosso = arr.remove(0);  // 1
print(arr);                   // [2, 3, 4, 5]

let rimosso2 = arr.remove(2); // 4
print(arr);                   // [2, 3, 5]
```

**Comportamento:** Sposta gli elementi dopo l'indice verso sinistra.

**Errore:** Errore a runtime se l'indice è fuori dai limiti.

---

### Ricerca e Trova

#### find

Trova la prima occorrenza di un valore.

**Firma:**
```hemlock
array.find(valore: any): i32
```

**Parametri:**
- `valore` - Valore da cercare

**Restituisce:** Indice della prima occorrenza, o `-1` se non trovato

**Esempi:**
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2
let idx2 = arr.find(99);     // -1 (non trovato)

// Trova il primo duplicato
let arr2 = [1, 2, 3, 2, 4];
let idx3 = arr2.find(2);     // 1 (prima occorrenza)
```

**Confronto:** Usa l'uguaglianza di valore per i primitivi e le stringhe.

---

#### contains

Verifica se l'array contiene un valore.

**Firma:**
```hemlock
array.contains(valore: any): bool
```

**Parametri:**
- `valore` - Valore da cercare

**Restituisce:** `true` se trovato, `false` altrimenti

**Esempi:**
```hemlock
let arr = [10, 20, 30, 40];
let ha = arr.contains(20);   // true
let ha2 = arr.contains(99);  // false

// Funziona con le stringhe
let parole = ["ciao", "mondo"];
let ha3 = parole.contains("ciao");  // true
```

---

### Slicing ed Estrazione

#### slice

Estrae un sottoarray per intervallo (fine esclusiva).

**Firma:**
```hemlock
array.slice(inizio: i32, fine: i32): array
```

**Parametri:**
- `inizio` - Indice iniziale (base 0, inclusivo)
- `fine` - Indice finale (esclusivo)

**Restituisce:** Nuovo array con elementi da [inizio, fine)

**Modifica:** No (restituisce un nuovo array)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);       // [2, 3, 4]
let primi_tre = arr.slice(0, 3); // [1, 2, 3]
let ultimi_due = arr.slice(3, 5);// [4, 5]

// Slice vuoto
let vuoto = arr.slice(2, 2);     // []
```

---

#### first

Ottiene il primo elemento senza rimuoverlo.

**Firma:**
```hemlock
array.first(): any
```

**Restituisce:** Primo elemento

**Modifica:** No

**Esempi:**
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1
print(arr);                  // [1, 2, 3] (invariato)
```

**Errore:** Errore a runtime se l'array è vuoto.

---

#### last

Ottiene l'ultimo elemento senza rimuoverlo.

**Firma:**
```hemlock
array.last(): any
```

**Restituisce:** Ultimo elemento

**Modifica:** No

**Esempi:**
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3
print(arr);                  // [1, 2, 3] (invariato)
```

**Errore:** Errore a runtime se l'array è vuoto.

---

### Manipolazione degli Array

#### reverse

Inverte l'array in loco.

**Firma:**
```hemlock
array.reverse(): null
```

**Restituisce:** `null`

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]
print(arr);                  // [5, 4, 3, 2, 1]

let parole = ["ciao", "mondo"];
parole.reverse();            // ["mondo", "ciao"]
```

---

#### clear

Rimuove tutti gli elementi dall'array.

**Firma:**
```hemlock
array.clear(): null
```

**Restituisce:** `null`

**Modifica:** Sì (modifica l'array in loco)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();
print(arr);                  // []
print(arr.length);           // 0
```

---

### Combinazione di Array

#### concat

Concatena con un altro array.

**Firma:**
```hemlock
array.concat(altro: array): array
```

**Parametri:**
- `altro` - Array da concatenare

**Restituisce:** Nuovo array con elementi da entrambi gli array

**Modifica:** No (restituisce un nuovo array)

**Esempi:**
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combinato = a.concat(b);  // [1, 2, 3, 4, 5, 6]
print(a);                     // [1, 2, 3] (invariato)
print(b);                     // [4, 5, 6] (invariato)

// Concatenazione a catena
let c = [7, 8];
let tutti = a.concat(b).concat(c);  // [1, 2, 3, 4, 5, 6, 7, 8]
```

---

### Operazioni Funzionali

#### map

Trasforma ogni elemento usando una funzione callback.

**Firma:**
```hemlock
array.map(callback: fn): array
```

**Parametri:**
- `callback` - Funzione che prende un elemento e restituisce il valore trasformato

**Restituisce:** Nuovo array con elementi trasformati

**Modifica:** No (restituisce un nuovo array)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let raddoppiato = arr.map(fn(x) { return x * 2; });
print(raddoppiato);  // [2, 4, 6, 8, 10]

let nomi = ["alice", "bob"];
let maiuscolo = nomi.map(fn(s) { return s.to_upper(); });
print(maiuscolo);  // ["ALICE", "BOB"]
```

---

#### filter

Seleziona gli elementi che corrispondono a un predicato.

**Firma:**
```hemlock
array.filter(predicato: fn): array
```

**Parametri:**
- `predicato` - Funzione che prende un elemento e restituisce bool

**Restituisce:** Nuovo array con elementi per cui il predicato ha restituito true

**Modifica:** No (restituisce un nuovo array)

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5, 6];
let pari = arr.filter(fn(x) { return x % 2 == 0; });
print(pari);  // [2, 4, 6]

let parole = ["ciao", "io", "hey", "arrivederci"];
let corte = parole.filter(fn(s) { return s.length < 4; });
print(corte);  // ["io", "hey"]
```

---

#### reduce

Riduce l'array a un singolo valore usando un accumulatore.

**Firma:**
```hemlock
array.reduce(callback: fn, iniziale: any): any
```

**Parametri:**
- `callback` - Funzione che prende (accumulatore, elemento) e restituisce il nuovo accumulatore
- `iniziale` - Valore iniziale per l'accumulatore

**Restituisce:** Valore finale accumulato

**Modifica:** No

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
let somma = arr.reduce(fn(acc, x) { return acc + x; }, 0);
print(somma);  // 15

let prodotto = arr.reduce(fn(acc, x) { return acc * x; }, 1);
print(prodotto);  // 120

// Trova il valore massimo
let max = arr.reduce(fn(acc, x) {
    if (x > acc) { return x; }
    return acc;
}, arr[0]);
print(max);  // 5
```

---

### Conversione a Stringa

#### join

Unisce gli elementi in una stringa con un delimitatore.

**Firma:**
```hemlock
array.join(delimitatore: string): string
```

**Parametri:**
- `delimitatore` - Stringa da inserire tra gli elementi

**Restituisce:** Stringa con tutti gli elementi uniti

**Esempi:**
```hemlock
let parole = ["ciao", "mondo", "foo"];
let unito = parole.join(" ");  // "ciao mondo foo"

let numeri = [1, 2, 3];
let csv = numeri.join(",");    // "1,2,3"

// Funziona con tipi misti
let misto = [1, "ciao", true, null];
print(misto.join(" | "));  // "1 | ciao | true | null"

// Delimitatore vuoto
let arr = ["a", "b", "c"];
let s = arr.join("");          // "abc"
```

**Comportamento:** Converte automaticamente tutti gli elementi in stringhe.

---

## Concatenamento di Metodi

I metodi degli array possono essere concatenati per operazioni concise:

**Esempi:**
```hemlock
// Concatena slice e join
let risultato = ["mela", "banana", "ciliegia", "dattero"]
    .slice(0, 2)
    .join(" e ");  // "mela e banana"

// Concatena concat e slice
let combinato = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);    // [3, 4, 5]

// Concatenamento complesso
let parole = ["ciao", "mondo", "foo", "bar"];
let risultato2 = parole
    .slice(0, 3)
    .concat(["baz"])
    .join("-");      // "ciao-mondo-foo-baz"
```

---

## Riepilogo Completo dei Metodi

### Metodi Modificanti

Metodi che modificano l'array in loco:

| Metodo     | Firma                      | Restituisce | Descrizione                    |
|------------|----------------------------|-------------|--------------------------------|
| `push`     | `(valore: any)`            | `null`      | Aggiunge alla fine             |
| `pop`      | `()`                       | `any`       | Rimuove dalla fine             |
| `shift`    | `()`                       | `any`       | Rimuove dall'inizio            |
| `unshift`  | `(valore: any)`            | `null`      | Aggiunge all'inizio            |
| `insert`   | `(indice: i32, valore: any)` | `null`    | Inserisce all'indice           |
| `remove`   | `(indice: i32)`            | `any`       | Rimuove all'indice             |
| `reverse`  | `()`                       | `null`      | Inverte in loco                |
| `clear`    | `()`                       | `null`      | Rimuove tutti gli elementi     |

### Metodi Non Modificanti

Metodi che restituiscono nuovi valori senza modificare l'originale:

| Metodo     | Firma                      | Restituisce | Descrizione                    |
|------------|----------------------------|-------------|--------------------------------|
| `find`     | `(valore: any)`            | `i32`       | Trova la prima occorrenza      |
| `contains` | `(valore: any)`            | `bool`      | Verifica se contiene il valore |
| `slice`    | `(inizio: i32, fine: i32)` | `array`     | Estrae sottoarray              |
| `first`    | `()`                       | `any`       | Ottiene il primo elemento      |
| `last`     | `()`                       | `any`       | Ottiene l'ultimo elemento      |
| `concat`   | `(altro: array)`           | `array`     | Concatena array                |
| `join`     | `(delimitatore: string)`   | `string`    | Unisce elementi in stringa     |
| `map`      | `(callback: fn)`           | `array`     | Trasforma ogni elemento        |
| `filter`   | `(predicato: fn)`          | `array`     | Seleziona elementi corrispondenti |
| `reduce`   | `(callback: fn, iniziale: any)` | `any`  | Riduce a un singolo valore     |

---

## Pattern di Utilizzo

### Uso come Stack

```hemlock
let stack = [];

// Push degli elementi
stack.push(1);
stack.push(2);
stack.push(3);

// Pop degli elementi
while (stack.length > 0) {
    let elemento = stack.pop();
    print(elemento);  // 3, 2, 1
}
```

### Uso come Coda

```hemlock
let coda = [];

// Accodamento
coda.push(1);
coda.push(2);
coda.push(3);

// Decodifica
while (coda.length > 0) {
    let elemento = coda.shift();
    print(elemento);  // 1, 2, 3
}
```

### Trasformazione di Array

```hemlock
// Filtro (manuale)
let numeri = [1, 2, 3, 4, 5, 6];
let pari = [];
let i = 0;
while (i < numeri.length) {
    if (numeri[i] % 2 == 0) {
        pari.push(numeri[i]);
    }
    i = i + 1;
}

// Map (manuale)
let numeri2 = [1, 2, 3, 4, 5];
let raddoppiato = [];
let j = 0;
while (j < numeri2.length) {
    raddoppiato.push(numeri2[j] * 2);
    j = j + 1;
}
```

### Costruzione di Array

```hemlock
let arr = [];

// Costruisci array con ciclo
let i = 0;
while (i < 10) {
    arr.push(i * 10);
    i = i + 1;
}

print(arr);  // [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
```

---

## Dettagli di Implementazione

**Gestione della Capacità:**
- Gli array crescono automaticamente quando necessario
- La capacità raddoppia quando viene superata
- Nessun controllo manuale della capacità

**Confronto dei Valori:**
- `find()` e `contains()` usano l'uguaglianza di valore
- Funziona correttamente per primitivi e stringhe
- Oggetti/array confrontati per riferimento

**Memoria:**
- Allocati nell'heap
- Nessuna liberazione automatica (gestione manuale della memoria)
- Nessun controllo dei limiti sull'accesso diretto all'indice

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Dettagli sul tipo array
- [API delle Stringhe](string-api.md) - Risultati di string join()
- [Operatori](operators.md) - Operatore di indicizzazione degli array
