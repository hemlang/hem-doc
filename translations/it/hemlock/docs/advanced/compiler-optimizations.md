# Ottimizzazioni del Compilatore

Il compilatore Hemlock (`hemlockc`) applica diversi passaggi di ottimizzazione durante la generazione del codice C. Queste ottimizzazioni sono automatiche e non richiedono intervento da parte dell'utente, ma comprenderle aiuta a spiegare le caratteristiche di prestazione.

---

## Panoramica

```
Sorgente (.hml)
    ↓
  Parse → AST
    ↓
  Type Check (opzionale)
    ↓
  Passaggio Ottimizzazione AST
    ↓
  Generazione Codice C (con inlining + unboxing)
    ↓
  Compilazione GCC/Clang
```

---

## Unboxing a Livello di Espressione

Il runtime di Hemlock rappresenta tutti i valori come struct `HmlValue` con tag. Nell'interprete, ogni operazione aritmetica esegue boxing e unboxing dei valori attraverso il dispatch a runtime. Il compilatore elimina questo overhead per le espressioni con tipi primitivi conosciuti.

**Prima (codegen naïve):**
```c
// x + 1 dove x è i32
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 chiamate di boxing + dispatch runtime
```

**Dopo (con unboxing delle espressioni):**
```c
// x + 1 dove x è i32
hml_val_i32((x + 1))  // Aritmetica C pura, singolo boxing alla fine
```

### Cosa Viene Unboxato

- Aritmetica binaria: `+`, `-`, `*`, `%`
- Operazioni bit a bit: `&`, `|`, `^`, `<<`, `>>`
- Confronti: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Operazioni unarie: `-`, `~`, `!`
- Variabili con annotazione di tipo e contatori di ciclo

### Cosa Ricade su HmlValue

- Chiamate di funzione (il tipo di ritorno potrebbe essere dinamico)
- Accesso a array/oggetti (tipo dell'elemento sconosciuto a compile time)
- Variabili senza annotazioni di tipo e senza tipo inferito

### Suggerimento

Aggiungere annotazioni di tipo alle variabili nei percorsi critici aiuta il compilatore ad applicare l'unboxing:

```hemlock
// Il compilatore può eseguire l'unboxing dell'intera espressione
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## Inlining Multi-Livello delle Funzioni

Il compilatore esegue l'inlining delle funzioni piccole nei siti di chiamata, sostituendo l'overhead della chiamata di funzione con codice diretto. Hemlock supporta l'inlining multi-livello fino a profondità 3, il che significa che anche le chiamate helper annidate vengono inlinate.

### Come Funziona

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // Sia ep0 CHE rotr vengono inlinate qui
    // ...
}
```

A profondità 1, `ep0()` viene inlinata in `sha256_round()`. A profondità 2, le chiamate `rotr()` dentro `ep0()` vengono anch'esse inlinate. Il risultato è un singolo blocco di aritmetica nativa senza overhead di chiamata di funzione.

### Criteri di Inlining

Le funzioni vengono inlinate quando:
- Il corpo della funzione è piccolo (singola espressione o poche istruzioni)
- La funzione non è ricorsiva
- La profondità corrente di inlining è inferiore a 3

### Controllare l'Inlining con le Annotazioni

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // Funzione complessa che non dovrebbe essere duplicata
    return x;
}
```

---

## Unboxing degli Accumulatori nei Cicli While

Per i cicli while al livello superiore, il compilatore rileva le variabili contatore e accumulatore e le sostituisce con variabili locali C native, eliminando l'overhead di boxing/unboxing ad ogni iterazione.

### Cosa Viene Ottimizzato

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

Il compilatore rileva che `sum` e `i` sono accumulatori interi usati solo all'interno del ciclo, e genera variabili locali `int32_t` native invece di operazioni `HmlValue`. Questo elimina l'overhead di retain/release e il dispatch dei tipi ad ogni iterazione.

### Impatto sulle Prestazioni

Miglioramenti benchmark da queste ottimizzazioni (misurati su carichi di lavoro tipici):

| Benchmark | Prima | Dopo | Miglioramento |
|-----------|-------|------|---------------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## Annotazioni Helper

Il compilatore supporta 10 annotazioni di ottimizzazione che mappano agli attributi GCC/Clang:

| Annotazione | Effetto |
|-------------|---------|
| `@inline` | Incoraggia l'inlining della funzione |
| `@noinline` | Impedisce l'inlining della funzione |
| `@hot` | Segna come eseguita frequentemente (predizione dei branch) |
| `@cold` | Segna come eseguita raramente |
| `@pure` | La funzione non ha effetti collaterali (legge stato esterno) |
| `@const` | La funzione dipende solo dagli argomenti (nessuno stato esterno) |
| `@flatten` | Esegue l'inlining di tutte le chiamate nella funzione |
| `@optimize(level)` | Livello di ottimizzazione per funzione ("0"-"3", "s", "fast") |
| `@warn_unused` | Avvisa se il valore di ritorno viene ignorato |
| `@section(name)` | Posiziona la funzione in una sezione ELF personalizzata |

### Esempio

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // Funzione di hashing nel percorso critico
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## Pool di Allocazione

Il runtime usa pool di oggetti pre-allocati per evitare l'overhead di `malloc`/`free` per oggetti a vita breve creati frequentemente:

| Pool | Slot | Descrizione |
|------|------|-------------|
| Pool ambienti | 1024 | Ambienti scope di closure/funzione (fino a 16 variabili ciascuno) |
| Pool oggetti | 512 | Oggetti anonimi con fino a 8 campi |
| Pool funzioni | 512 | Struct closure per funzioni catturate |

I pool usano stack di free-list per allocazione e deallocazione O(1). Quando un pool è esaurito, il runtime ricade su `malloc`. Gli oggetti che superano il proprio slot nel pool (es., un oggetto che acquisisce un 9° campo) vengono migrati in modo trasparente allo storage nell'heap.

### Parametri Presi in Prestito dall'AST

Le closure prendono in prestito i metadati dei parametri direttamente dall'AST invece di eseguire una copia profonda, eliminando circa 6 `malloc` + N `strdup` chiamate per creazione di closure. Gli hash dei nomi dei parametri vengono calcolati pigramente e cachati nel nodo AST.

---

## Type Checking

Il compilatore include il type checking a compile-time (abilitato di default):

```bash
hemlockc program.hml -o program       # Type check + compila
hemlockc --check program.hml          # Solo type check
hemlockc --no-type-check program.hml  # Salta il type checking
hemlockc --strict-types program.hml   # Avvisa sui tipi 'any' impliciti
```

Il codice senza annotazioni di tipo viene trattato come dinamico (tipo `any`) e supera sempre il type checking. Le annotazioni di tipo forniscono suggerimenti di ottimizzazione che abilitano l'unboxing.

---

## Vedi Anche

- [Proposta Annotazioni Helper](../proposals/compiler-helper-annotations.md) - Riferimento dettagliato sulle annotazioni
- [API della Memoria](../reference/memory-api.md) - Operazioni su buffer e puntatori
- [Funzioni](../language-guide/functions.md) - Annotazioni di tipo e funzioni con corpo espressione
