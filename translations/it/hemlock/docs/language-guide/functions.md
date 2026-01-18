# Funzioni

Le funzioni in Hemlock sono **valori di prima classe** che possono essere assegnate a variabili, passate come argomenti e restituite da altre funzioni. Questa guida copre la sintassi delle funzioni, le closure, la ricorsione e i pattern avanzati.

## Panoramica

```hemlock
// Sintassi funzione con nome
fn add(a: i32, b: i32): i32 {
    return a + b;
}

// Funzione anonima
let multiply = fn(x, y) {
    return x * y;
};

// Closure
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
print(add5(3));  // 8
```

## Dichiarazione di funzione

### Funzioni con nome

```hemlock
fn greet(name: string): string {
    return "Ciao, " + name;
}

let msg = greet("Alice");  // "Ciao, Alice"
```

**Componenti:**
- `fn` - Parola chiave funzione
- `greet` - Nome della funzione
- `(name: string)` - Parametri con tipi opzionali
- `: string` - Tipo di ritorno opzionale
- `{ ... }` - Corpo della funzione

### Funzioni anonime

Funzioni senza nome, assegnate a variabili:

```hemlock
let square = fn(x) {
    return x * x;
};

print(square(5));  // 25
```

**Con nome vs. Anonima:**
```hemlock
// Queste due sono equivalenti:
fn add(a, b) { return a + b; }

let add = fn(a, b) { return a + b; };
```

**Nota:** Le funzioni con nome si trasformano in assegnazioni di variabili con funzioni anonime.

## Parametri

### Parametri di base

```hemlock
fn example(a, b, c) {
    return a + b + c;
}

let result = example(1, 2, 3);  // 6
```

### Annotazioni di tipo

Annotazioni di tipo opzionali sui parametri:

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);      // OK
add(5, 10.5);    // La verifica dei tipi a runtime promuove a f64
```

**Verifica dei tipi:**
- I tipi dei parametri vengono verificati alla chiamata se annotati
- Le conversioni di tipo implicite seguono le regole di promozione standard
- Le incompatibilita di tipo causano errori a runtime

### Passaggio per valore

Tutti gli argomenti vengono **copiati** (passaggio per valore):

```hemlock
fn modify(x) {
    x = 100;  // Modifica solo la copia locale
}

let a = 10;
modify(a);
print(a);  // Ancora 10 (invariato)
```

**Nota:** Gli oggetti e gli array vengono passati per riferimento (il riferimento viene copiato), quindi il loro contenuto puo essere modificato:

```hemlock
fn modify_array(arr) {
    arr[0] = 99;  // Modifica l'array originale
}

let a = [1, 2, 3];
modify_array(a);
print(a[0]);  // 99 (modificato)
```

## Valori di ritorno

### Istruzione return

```hemlock
fn get_max(a: i32, b: i32): i32 {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

### Annotazioni del tipo di ritorno

Annotazione di tipo opzionale per il valore di ritorno:

```hemlock
fn calculate(): f64 {
    return 3.14159;
}

fn get_name(): string {
    return "Alice";
}
```

**Verifica dei tipi:**
- I tipi di ritorno vengono verificati quando la funzione ritorna (se annotati)
- Le conversioni di tipo seguono le regole di promozione standard

### Ritorno implicito

Le funzioni senza annotazione del tipo di ritorno restituiscono implicitamente `null`:

```hemlock
fn print_message(msg) {
    print(msg);
    // Restituisce implicitamente null
}

let result = print_message("ciao");  // result e null
```

### Ritorno anticipato

```hemlock
fn find_first_negative(arr) {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Uscita anticipata
        }
    }
    return -1;  // Non trovato
}
```

### Ritorno senza valore

`return;` senza valore restituisce `null`:

```hemlock
fn maybe_process(value) {
    if (value < 0) {
        return;  // Restituisce null
    }
    return value * 2;
}
```

## Funzioni di prima classe

Le funzioni possono essere assegnate, passate e restituite come qualsiasi altro valore.

### Funzioni come variabili

```hemlock
let operation = fn(x, y) { return x + y; };

print(operation(5, 3));  // 8

// Riassegnare
operation = fn(x, y) { return x * y; };
print(operation(5, 3));  // 15
```

### Funzioni come argomenti

```hemlock
fn apply(f, x) {
    return f(x);
}

fn double(n) {
    return n * 2;
}

let result = apply(double, 5);  // 10
```

### Funzioni come valori di ritorno

```hemlock
fn get_operation(op: string) {
    if (op == "add") {
        return fn(a, b) { return a + b; };
    } else if (op == "multiply") {
        return fn(a, b) { return a * b; };
    } else {
        return fn(a, b) { return 0; };
    }
}

let add = get_operation("add");
print(add(5, 3));  // 8
```

## Closure

Le funzioni catturano il loro ambiente di definizione (scope lessicale).

### Closure di base

```hemlock
fn makeCounter() {
    let count = 0;
    return fn() {
        count = count + 1;
        return count;
    };
}

let counter = makeCounter();
print(counter());  // 1
print(counter());  // 2
print(counter());  // 3
```

**Come funziona:**
- La funzione interna cattura `count` dallo scope esterno
- `count` persiste attraverso le chiamate alla funzione restituita
- Ogni chiamata a `makeCounter()` crea una nuova closure con il proprio `count`

### Closure con parametri

```hemlock
fn makeAdder(x) {
    return fn(y) {
        return x + y;
    };
}

let add5 = makeAdder(5);
let add10 = makeAdder(10);

print(add5(3));   // 8
print(add10(3));  // 13
```

### Closure multiple

```hemlock
fn makeOperations(x) {
    let add = fn(y) { return x + y; };
    let multiply = fn(y) { return x * y; };

    return { add: add, multiply: multiply };
}

let ops = makeOperations(5);
print(ops.add(3));       // 8
print(ops.multiply(3));  // 15
```

### Scope lessicale

Le funzioni possono accedere alle variabili dello scope esterno tramite lo scope lessicale:

```hemlock
let global = 10;

fn outer() {
    let outer_var = 20;

    fn inner() {
        // Puo leggere global e outer_var
        print(global);      // 10
        print(outer_var);   // 20
    }

    inner();
}

outer();
```

Le closure catturano le variabili per riferimento, permettendo la lettura e la modifica delle variabili dello scope esterno (come mostrato nell'esempio `makeCounter` sopra).

## Ricorsione

Le funzioni possono chiamare se stesse.

### Ricorsione di base

```hemlock
fn factorial(n: i32): i32 {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));  // 120
```

### Ricorsione mutua

Le funzioni possono chiamarsi a vicenda:

```hemlock
fn is_even(n: i32): bool {
    if (n == 0) {
        return true;
    }
    return is_odd(n - 1);
}

fn is_odd(n: i32): bool {
    if (n == 0) {
        return false;
    }
    return is_even(n - 1);
}

print(is_even(4));  // true
print(is_odd(4));   // false
```

### Elaborazione dati ricorsiva

```hemlock
fn sum_array(arr: array, index: i32): i32 {
    if (index >= arr.length) {
        return 0;
    }
    return arr[index] + sum_array(arr, index + 1);
}

let numbers = [1, 2, 3, 4, 5];
print(sum_array(numbers, 0));  // 15
```

**Nota:** Nessuna ottimizzazione della ricorsione in coda ancora - la ricorsione profonda puo causare overflow dello stack.

## Funzioni di ordine superiore

Funzioni che prendono o restituiscono altre funzioni.

### Pattern Map

```hemlock
fn map(arr, f) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        result.push(f(arr[i]));
        i = i + 1;
    }
    return result;
}

fn double(x) { return x * 2; }

let numbers = [1, 2, 3, 4, 5];
let doubled = map(numbers, double);  // [2, 4, 6, 8, 10]
```

### Pattern Filter

```hemlock
fn filter(arr, predicate) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (predicate(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

fn is_even(x) { return x % 2 == 0; }

let numbers = [1, 2, 3, 4, 5, 6];
let evens = filter(numbers, is_even);  // [2, 4, 6]
```

### Pattern Reduce

```hemlock
fn reduce(arr, f, initial) {
    let accumulator = initial;
    let i = 0;
    while (i < arr.length) {
        accumulator = f(accumulator, arr[i]);
        i = i + 1;
    }
    return accumulator;
}

fn add(a, b) { return a + b; }

let numbers = [1, 2, 3, 4, 5];
let sum = reduce(numbers, add, 0);  // 15
```

### Composizione di funzioni

```hemlock
fn compose(f, g) {
    return fn(x) {
        return f(g(x));
    };
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }

let double_then_increment = compose(increment, double);
print(double_then_increment(5));  // 11 (5*2 + 1)
```

## Pattern comuni

### Pattern: Funzioni factory

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Ciao, sono " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Ciao, sono Alice"
```

### Pattern: Funzioni callback

```hemlock
fn process_async(data, callback) {
    // ... fare l'elaborazione
    callback(data);
}

process_async("test", fn(result) {
    print("Elaborazione completata: " + result);
});
```

### Pattern: Applicazione parziale

```hemlock
fn partial(f, x) {
    return fn(y) {
        return f(x, y);
    };
}

fn multiply(a, b) {
    return a * b;
}

let double = partial(multiply, 2);
let triple = partial(multiply, 3);

print(double(5));  // 10
print(triple(5));  // 15
```

### Pattern: Memoizzazione

```hemlock
fn memoize(f) {
    let cache = {};

    return fn(x) {
        if (cache.has(x)) {
            return cache[x];
        }

        let result = f(x);
        cache[x] = result;
        return result;
    };
}

fn expensive_fibonacci(n) {
    if (n <= 1) { return n; }
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2);
}

let fast_fib = memoize(expensive_fibonacci);
print(fast_fib(10));  // Molto piu veloce con la cache
```

## Semantica delle funzioni

### Requisiti del tipo di ritorno

Le funzioni con annotazione del tipo di ritorno **devono** restituire un valore:

```hemlock
fn get_value(): i32 {
    // ERRORE: Istruzione return mancante
}

fn get_value(): i32 {
    return 42;  // OK
}
```

### Verifica dei tipi

```hemlock
fn add(a: i32, b: i32): i32 {
    return a + b;
}

add(5, 10);        // OK
add(5.5, 10.5);    // Promuove a f64, restituisce f64
add("a", "b");     // Errore runtime: tipo non corrispondente
```

### Regole di scope

```hemlock
let global = "global";

fn outer() {
    let outer_var = "outer";

    fn inner() {
        let inner_var = "inner";
        // Puo accedere: inner_var, outer_var, global
    }

    // Puo accedere: outer_var, global
    // Non puo accedere: inner_var
}

// Puo accedere: global
// Non puo accedere: outer_var, inner_var
```

## Buone pratiche

1. **Usa annotazioni di tipo** - Aiuta a catturare errori e documenta l'intenzione
2. **Mantieni le funzioni piccole** - Ogni funzione dovrebbe fare una sola cosa
3. **Preferisci le funzioni pure** - Evita gli effetti collaterali quando possibile
4. **Nomina le funzioni chiaramente** - Usa nomi di verbi descrittivi
5. **Ritorna presto** - Usa clausole di guardia per ridurre l'annidamento
6. **Documenta le closure complesse** - Rendi esplicite le variabili catturate
7. **Evita la ricorsione profonda** - Nessuna ottimizzazione della ricorsione in coda ancora

## Trabocchetti comuni

### Trabocchetto: Profondita della ricorsione

```hemlock
// La ricorsione profonda puo causare overflow dello stack
fn count_down(n) {
    if (n == 0) { return; }
    count_down(n - 1);
}

count_down(100000);  // Potrebbe crashare con overflow dello stack
```

### Trabocchetto: Modifica delle variabili catturate

```hemlock
fn make_counter() {
    let count = 0;
    return fn() {
        count = count + 1;  // Puo leggere e modificare le variabili catturate
        return count;
    };
}
```

**Nota:** Questo funziona, ma sii consapevole che tutte le closure condividono lo stesso ambiente catturato.

## Esempi

### Esempio: Pipeline di funzioni

```hemlock
fn pipeline(value, ...functions) {
    let result = value;
    for (f in functions) {
        result = f(result);
    }
    return result;
}

fn double(x) { return x * 2; }
fn increment(x) { return x + 1; }
fn square(x) { return x * x; }

let result = pipeline(3, double, increment, square);
print(result);  // 49 ((3*2+1)^2)
```

### Esempio: Gestore di eventi

```hemlock
let handlers = [];

fn on_event(name: string, handler) {
    handlers.push({ name: name, handler: handler });
}

fn trigger_event(name: string, data) {
    let i = 0;
    while (i < handlers.length) {
        if (handlers[i].name == name) {
            handlers[i].handler(data);
        }
        i = i + 1;
    }
}

on_event("click", fn(data) {
    print("Clic: " + data);
});

trigger_event("click", "button1");
```

### Esempio: Ordinamento con comparatore personalizzato

```hemlock
fn sort(arr, compare) {
    // Bubble sort con comparatore personalizzato
    let n = arr.length;
    let i = 0;
    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (compare(arr[j], arr[j + 1]) > 0) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

fn ascending(a, b) {
    if (a < b) { return -1; }
    if (a > b) { return 1; }
    return 0;
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers, ascending);
print(numbers);  // [1, 2, 5, 8, 9]
```

## Parametri opzionali (argomenti predefiniti)

Le funzioni possono avere parametri opzionali con valori predefiniti usando la sintassi `?:`:

```hemlock
fn greet(name, greeting?: "Ciao") {
    return greeting + " " + name;
}

print(greet("Alice"));           // "Ciao Alice"
print(greet("Bob", "Salve"));    // "Salve Bob"

fn add(a, b?: 10, c?: 100) {
    return a + b + c;
}

print(add(1));          // 111 (1 + 10 + 100)
print(add(1, 2));       // 103 (1 + 2 + 100)
print(add(1, 2, 3));    // 6   (1 + 2 + 3)
```

**Regole:**
- I parametri opzionali devono venire dopo i parametri richiesti
- I valori predefiniti possono essere qualsiasi espressione
- Gli argomenti omessi usano il valore predefinito

## Funzioni variadiche (parametri rest)

Le funzioni possono accettare un numero variabile di argomenti usando i parametri rest (`...`):

```hemlock
fn sum(...args) {
    let total = 0;
    for (arg in args) {
        total = total + arg;
    }
    return total;
}

print(sum(1, 2, 3));        // 6
print(sum(1, 2, 3, 4, 5));  // 15
print(sum());               // 0

fn log(prefix, ...messages) {
    for (msg in messages) {
        print(prefix + ": " + msg);
    }
}

log("INFO", "Avvio", "Esecuzione", "Terminato");
// INFO: Avvio
// INFO: Esecuzione
// INFO: Terminato
```

**Regole:**
- Il parametro rest deve essere l'ultimo parametro
- Il parametro rest raccoglie tutti gli argomenti rimanenti in un array
- Puo essere combinato con parametri regolari e opzionali

## Annotazioni di tipo funzione

I tipi funzione permettono di specificare la firma esatta attesa per i parametri di funzione e i valori di ritorno:

### Tipi funzione di base

```hemlock
// Sintassi tipo funzione: fn(param_types): return_type
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

let double = fn(n) { return n * 2; };
let result = apply(double, 5);  // 10
```

### Tipi funzione di ordine superiore

```hemlock
// Funzione che restituisce una funzione
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

let add5 = make_adder(5);
print(add5(10));  // 15
```

### Tipi funzione asincrona

```hemlock
// Tipo funzione asincrona
fn run_task(handler: async fn(): void) {
    spawn(handler);
}

run_task(async fn() {
    print("Esecuzione asincrona!");
});
```

### Alias di tipo funzione

```hemlock
// Crea tipi funzione con nome per chiarezza
type Callback = fn(i32): void;
type Predicate = fn(any): bool;
type BinaryOp = fn(i32, i32): i32;

fn filter_with(arr: array, pred: Predicate): array {
    return arr.filter(pred);
}
```

## Parametri const

Il modificatore `const` impedisce che un parametro venga modificato nella funzione:

### Parametri const di base

```hemlock
fn print_all(const items: array) {
    // items.push(4);  // ERRORE: impossibile modificare parametro const
    for (item in items) {
        print(item);   // OK: la lettura e consentita
    }
}

let nums = [1, 2, 3];
print_all(nums);
```

### Immutabilita profonda

I parametri const impongono immutabilita profonda - nessuna modifica attraverso alcun percorso:

```hemlock
fn describe(const person: object) {
    print(person.name);       // OK: la lettura e consentita
    // person.name = "Bob";   // ERRORE: impossibile modificare
    // person.address.city = "Roma";  // ERRORE: const profondo
}
```

### Cosa impedisce const

| Tipo | Bloccato da const | Consentito |
|------|-------------------|------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse | slice, concat, map, filter, find, contains |
| object | assegnazione campo | lettura campo |
| buffer | assegnazione indice | lettura indice |
| string | assegnazione indice | tutti i metodi (restituiscono nuove stringhe) |

## Argomenti con nome

Le funzioni possono essere chiamate con argomenti con nome per maggiore chiarezza e flessibilita:

### Argomenti con nome di base

```hemlock
fn create_user(name: string, age?: 18, active?: true) {
    print(name + " ha " + age + " anni");
}

// Argomenti posizionali (tradizionale)
create_user("Alice", 25, false);

// Argomenti con nome - possono essere in qualsiasi ordine
create_user(name: "Bob", age: 30);
create_user(age: 25, name: "Charlie", active: false);
```

### Mescolare posizionale e con nome

```hemlock
// Salta i parametri opzionali nominando cio di cui hai bisogno
create_user("David", active: false);  // Usa age predefinito=18

// Gli argomenti con nome devono venire dopo i posizionali
create_user("Eve", age: 21);          // OK
// create_user(name: "Bad", 25);      // ERRORE: posizionale dopo nominato
```

### Regole per gli argomenti con nome

- Usa la sintassi `nome: valore` per gli argomenti con nome
- Gli argomenti con nome possono apparire in qualsiasi ordine dopo gli argomenti posizionali
- Gli argomenti posizionali non possono seguire gli argomenti con nome
- Funziona con i parametri predefiniti/opzionali
- I nomi di parametro sconosciuti causano errori a runtime

## Limitazioni

Limitazioni attuali da conoscere:

- **Nessun passaggio per riferimento** - Parola chiave `ref` analizzata ma non implementata
- **Nessun overloading di funzione** - Una funzione per nome
- **Nessuna ottimizzazione della ricorsione in coda** - Ricorsione profonda limitata dalla dimensione dello stack

## Argomenti correlati

- [Flusso di controllo](control-flow.md) - Uso delle funzioni con le strutture di controllo
- [Oggetti](objects.md) - I metodi sono funzioni memorizzate negli oggetti
- [Gestione degli errori](error-handling.md) - Funzioni e gestione delle eccezioni
- [Tipi](types.md) - Annotazioni di tipo e conversioni

## Vedi anche

- **Closure**: Vedi la sezione "Functions" di CLAUDE.md per la semantica delle closure
- **Valori di prima classe**: Le funzioni sono valori come qualsiasi altro
- **Scope lessicale**: Le funzioni catturano il loro ambiente di definizione
