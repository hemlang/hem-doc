# Flusso di Controllo

Hemlock fornisce un flusso di controllo familiare in stile C con parentesi graffe obbligatorie e sintassi esplicita. Questa guida copre condizionali, cicli, istruzioni switch e operatori.

## Panoramica

Funzionalita del flusso di controllo disponibili:

- `if`/`else`/`else if` - Diramazioni condizionali
- Cicli `while` - Iterazione basata su condizione
- Cicli `for` - Stile C e iterazione for-in
- `loop` - Cicli infiniti (piu pulito di `while (true)`)
- Istruzioni `switch` - Diramazioni multiple
- `break`/`continue` - Controllo dei cicli
- Etichette dei cicli - break/continue mirati per cicli annidati
- `defer` - Esecuzione differita (pulizia)
- Operatori booleani: `&&`, `||`, `!`
- Operatori di confronto: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Operatori bit a bit: `&`, `|`, `^`, `<<`, `>>`, `~`

## Istruzioni If

### If/Else di Base

```hemlock
if (x > 10) {
    print("grande");
} else {
    print("piccolo");
}
```

**Regole:**
- Le parentesi graffe sono **sempre obbligatorie** per tutti i rami
- Le condizioni devono essere racchiuse tra parentesi tonde
- Niente parentesi graffe opzionali (a differenza del C)

### If Senza Else

```hemlock
if (x > 0) {
    print("positivo");
}
// Nessun ramo else necessario
```

### Catene Else-If

```hemlock
if (x > 100) {
    print("molto grande");
} else if (x > 50) {
    print("grande");
} else if (x > 10) {
    print("medio");
} else {
    print("piccolo");
}
```

**Nota:** `else if` e zucchero sintattico per istruzioni if annidate. Questi sono equivalenti:

```hemlock
// else if (zucchero sintattico)
if (a) {
    foo();
} else if (b) {
    bar();
}

// Equivalente if annidato
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### Istruzioni If Annidate

```hemlock
if (x > 0) {
    if (x < 10) {
        print("positivo a singola cifra");
    } else {
        print("positivo a piu cifre");
    }
} else {
    print("non positivo");
}
```

## Cicli While

Iterazione basata su condizione:

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**Cicli infiniti (vecchio stile):**
```hemlock
while (true) {
    // ... fai il lavoro
    if (should_exit) {
        break;
    }
}
```

**Nota:** Per i cicli infiniti, preferisci la parola chiave `loop` (vedi sotto).

## Loop (Ciclo Infinito)

La parola chiave `loop` fornisce una sintassi piu pulita per i cicli infiniti:

```hemlock
loop {
    // ... fai il lavoro
    if (should_exit) {
        break;
    }
}
```

**Equivalente a `while (true)` ma piu esplicito sull'intento.**

### Loop Base con Break

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Stampa: 0, 1, 2, 3, 4
```

### Loop con Continue

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // Salta la stampa di 3
    }
    print(i);
}
// Stampa: 1, 2, 4, 5
```

### Cicli Annidati

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
// Stampa: 0, 1, 2, 10, 11, 12
```

### Quando Usare Loop

- **Usa `loop`** per cicli intenzionalmente infiniti che escono tramite `break`
- **Usa `while`** quando c'e una condizione di terminazione naturale
- **Usa `for`** quando iteri un numero noto di volte o su una collezione

## Cicli For

### For in Stile C

Classico ciclo for a tre parti:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Componenti:**
- **Inizializzatore**: `let i = 0` - Eseguito una volta prima del ciclo
- **Condizione**: `i < 10` - Controllata prima di ogni iterazione
- **Aggiornamento**: `i = i + 1` - Eseguito dopo ogni iterazione

**Scope:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i non e accessibile qui (scope del ciclo)
```

### Cicli For-In

Itera sugli elementi di un array:

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // Stampa ogni elemento
}
```

**Con indice e valore:**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Indice: ${i}, Valore: ${arr[i]}`);
}
```

## Istruzioni Switch

Diramazioni multiple basate sul valore:

### Switch Base

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("uno");
        break;
    case 2:
        print("due");
        break;
    case 3:
        print("tre");
        break;
}
```

### Switch con Default

```hemlock
let color = "blu";

switch (color) {
    case "rosso":
        print("fermati");
        break;
    case "giallo":
        print("rallenta");
        break;
    case "verde":
        print("vai");
        break;
    default:
        print("colore sconosciuto");
        break;
}
```

**Regole:**
- `default` corrisponde quando nessun altro caso corrisponde
- `default` puo apparire ovunque nel corpo dello switch
- E permesso un solo caso default

### Comportamento Fall-Through

I casi senza `break` cadono nel caso successivo (comportamento in stile C). Questo e **intenzionale** e puo essere usato per raggruppare i casi:

```hemlock
let grade = 85;

switch (grade) {
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
        print("C o inferiore");
        break;
}
```

**Esempio di fallthrough esplicito:**
```hemlock
let day = 3;

switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Giorno feriale");
        break;
    case 6:
    case 7:
        print("Fine settimana");
        break;
}
```

**Importante:** A differenza di alcuni linguaggi moderni, Hemlock NON richiede una parola chiave `fallthrough` esplicita. I casi cadono automaticamente nel successivo a meno che non siano terminati da `break`, `return` o `throw`. Usa sempre `break` per prevenire fallthrough non intenzionali.

### Switch con Return

Nelle funzioni, `return` esce immediatamente dallo switch:

```hemlock
fn get_day_name(day: i32): string {
    switch (day) {
        case 1:
            return "Lunedi";
        case 2:
            return "Martedi";
        case 3:
            return "Mercoledi";
        default:
            return "Sconosciuto";
    }
}
```

### Tipi di Valore nello Switch

Switch funziona con qualsiasi tipo di valore:

```hemlock
// Interi
switch (count) {
    case 0: print("zero"); break;
    case 1: print("uno"); break;
}

// Stringhe
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// Booleani
switch (flag) {
    case true: print("acceso"); break;
    case false: print("spento"); break;
}
```

**Nota:** I casi sono confrontati usando l'uguaglianza di valore.

## Break e Continue

### Break

Esce dal ciclo o switch piu interno:

```hemlock
// Nei cicli
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // Esci dal ciclo
    }
    print(i);
    i = i + 1;
}

// Nello switch
switch (x) {
    case 1:
        print("uno");
        break;  // Esci dallo switch
    case 2:
        print("due");
        break;
}
```

### Continue

Salta alla prossima iterazione del ciclo:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // Salta l'iterazione quando i e 5
    }
    print(i);  // Stampa 0,1,2,3,4,6,7,8,9
}
```

**Differenza:**
- `break` - Esce completamente dal ciclo
- `continue` - Salta alla prossima iterazione

## Etichette dei Cicli

Le etichette dei cicli permettono a `break` e `continue` di mirare cicli esterni specifici invece del solo ciclo piu interno. Questo e utile per cicli annidati dove devi controllare un ciclo esterno da uno interno.

### Break con Etichetta

Esci da un ciclo esterno da un ciclo interno:

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // Esci dal ciclo while esterno
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// Stampa: 0, 1, 2, 10 (si ferma a i=1, j=1)
```

### Continue con Etichetta

Salta alla prossima iterazione di un ciclo esterno:

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // Salta il resto del ciclo interno, continua l'esterno
        }
        print(i * 10 + j);
    }
}
// Quando i=2, j=1: salta alla prossima iterazione esterna
```

### Etichette con Cicli For

Le etichette funzionano con tutti i tipi di ciclo:

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

### Etichette con Cicli For-In

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

### Etichette con la Parola Chiave Loop

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

### Etichette Multiple

Puoi avere etichette a diversi livelli di annidamento:

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // Salta alla prossima iterazione del ciclo medio
            }
            if (a == 1 && b == 1) {
                break outer;      // Esci dal ciclo piu esterno
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### Break/Continue Senza Etichetta con Cicli Etichettati

`break` e `continue` senza etichetta funzionano normalmente (influenzando il ciclo piu interno), anche quando i cicli esterni hanno etichette:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // Interrompe solo il ciclo interno
        }
        print(x * 10 + y);
    }
}
// Stampa: 0, 1, 10, 11, 20, 21
```

### Sintassi delle Etichette

- Le etichette sono identificatori seguiti da due punti
- Le etichette devono precedere immediatamente un'istruzione di ciclo (`while`, `for`, `loop`)
- I nomi delle etichette seguono le regole degli identificatori (lettere, cifre, underscore)
- Convenzioni comuni: `outer`, `inner`, `row`, `col`, nomi descrittivi

## Istruzione Defer

L'istruzione `defer` pianifica il codice da eseguire quando la funzione corrente ritorna. Questo e utile per operazioni di pulizia come chiudere file, liberare risorse o rilasciare lock.

### Defer Base

```hemlock
fn example() {
    print("inizio");
    defer print("pulizia");  // Eseguito quando la funzione ritorna
    print("fine");
}

example();
// Output:
// inizio
// fine
// pulizia
```

**Comportamento chiave:**
- Le istruzioni differite vengono eseguite **dopo** che il corpo della funzione e completato
- Le istruzioni differite vengono eseguite **prima** che la funzione ritorni al chiamante
- Le istruzioni differite vengono sempre eseguite, anche se la funzione lancia un'eccezione

### Defer Multipli (Ordine LIFO)

Quando si usano piu istruzioni `defer`, vengono eseguite in **ordine inverso** (Last-In-First-Out):

```hemlock
fn example() {
    defer print("primo");   // Eseguito per ultimo
    defer print("secondo"); // Eseguito secondo
    defer print("terzo");   // Eseguito per primo
    print("corpo");
}

example();
// Output:
// corpo
// terzo
// secondo
// primo
```

Questo ordine LIFO e intenzionale - corrisponde all'ordine naturale per la pulizia di risorse annidate (chiudi le risorse interne prima di quelle esterne).

### Defer con Return

Le istruzioni differite vengono eseguite prima che `return` trasferisca il controllo:

```hemlock
fn get_value(): i32 {
    defer print("pulizia");
    print("prima del return");
    return 42;
}

let result = get_value();
print("risultato:", result);
// Output:
// prima del return
// pulizia
// risultato: 42
```

### Defer con Eccezioni

Le istruzioni differite vengono eseguite anche quando viene lanciata un'eccezione:

```hemlock
fn risky() {
    defer print("pulizia 1");
    defer print("pulizia 2");
    print("prima del throw");
    throw "errore!";
    print("dopo il throw");  // Mai raggiunto
}

try {
    risky();
} catch (e) {
    print("Catturato:", e);
}
// Output:
// prima del throw
// pulizia 2
// pulizia 1
// Catturato: errore!
```

### Pattern per la Pulizia delle Risorse

Il caso d'uso principale per `defer` e assicurare che le risorse vengano pulite:

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // Chiude sempre, anche in caso di errore

    let content = file.read();
    // ... elabora il contenuto ...

    // Il file viene chiuso automaticamente quando la funzione ritorna
}
```

**Senza defer (soggetto a errori):**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // Se questo lancia, file.close() non viene mai chiamato!
    process(content);
    file.close();
}
```

### Defer con Closure

Defer puo usare closure per catturare lo stato:

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Rilascio risorsa");
        release(resource);
    }();  // Nota: espressione di funzione invocata immediatamente

    use_resource(resource);
}
```

### Quando Usare Defer

**Usa defer per:**
- Chiudere file e connessioni di rete
- Liberare memoria allocata
- Rilasciare lock e mutex
- Pulizia in qualsiasi funzione che acquisisce risorse

**Defer vs Finally:**
- `defer` e piu semplice per la pulizia di una singola risorsa
- `try/finally` e migliore per la gestione complessa degli errori con recupero

### Best Practice

1. **Posiziona defer immediatamente dopo l'acquisizione di una risorsa:**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... usa file ...
   ```

2. **Usa defer multipli per risorse multiple:**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // Entrambi i file saranno chiusi in ordine inverso
   ```

3. **Ricorda l'ordine LIFO per risorse dipendenti:**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner rilasciato prima di outer (ordine di dipendenza corretto)
   ```

## Operatori Booleani

### AND Logico (`&&`)

Entrambe le condizioni devono essere vere:

```hemlock
if (x > 0 && x < 10) {
    print("positivo a singola cifra");
}
```

**Valutazione short-circuit:**
```hemlock
if (false && expensive_check()) {
    // expensive_check() mai chiamata
}
```

### OR Logico (`||`)

Almeno una condizione deve essere vera:

```hemlock
if (x < 0 || x > 100) {
    print("fuori range");
}
```

**Valutazione short-circuit:**
```hemlock
if (true || expensive_check()) {
    // expensive_check() mai chiamata
}
```

### NOT Logico (`!`)

Nega il valore booleano:

```hemlock
if (!is_valid) {
    print("non valido");
}

if (!(x > 10)) {
    // Uguale a: if (x <= 10)
}
```

## Operatori di Confronto

### Uguaglianza

```hemlock
if (x == 10) { }    // Uguale
if (x != 10) { }    // Diverso
```

Funziona con tutti i tipi:
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### Relazionali

```hemlock
if (x < 10) { }     // Minore di
if (x > 10) { }     // Maggiore di
if (x <= 10) { }    // Minore o uguale
if (x >= 10) { }    // Maggiore o uguale
```

**Si applica la promozione di tipo:**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true (i32 promosso a i64)
```

## Operatori Bit a Bit

Hemlock fornisce operatori bit a bit per la manipolazione degli interi. Questi funzionano **solo con tipi interi** (i8-i64, u8-u64).

### Operatori Bit a Bit Binari

**AND bit a bit (`&`)**
```hemlock
let a = 12;  // 1100 in binario
let b = 10;  // 1010 in binario
print(a & b);   // 8 (1000)
```

**OR bit a bit (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**XOR bit a bit (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**Shift a sinistra (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - shift a sinistra di 2
```

**Shift a destra (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - shift a destra di 1
```

### Operatore Bit a Bit Unario

**NOT bit a bit (`~`)**
```hemlock
let a = 12;
print(~a);      // -13 (complemento a due)

let c: u8 = 15;   // 00001111 in binario
print(~c);        // 240 (11110000) in u8
```

### Esempi Bit a Bit

**Con tipi unsigned:**
```hemlock
let c: u8 = 15;   // 00001111 in binario
let d: u8 = 7;    // 00000111 in binario

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - in u8
```

**Preservazione del tipo:**
```hemlock
// Le operazioni bit a bit preservano il tipo degli operandi
let x: u8 = 255;
let result = ~x;  // result e u8 con valore 0

let y: i32 = 100;
let result2 = y << 2;  // result2 e i32 con valore 400
```

**Pattern comuni:**
```hemlock
// Controlla se un bit e impostato
if (flags & 0x04) {
    print("bit 2 impostato");
}

// Imposta un bit
flags = flags | 0x08;

// Cancella un bit
flags = flags & ~0x02;

// Inverte un bit
flags = flags ^ 0x01;
```

### Precedenza degli Operatori

Gli operatori bit a bit seguono la precedenza in stile C:

1. `~` (NOT unario) - piu alta, stesso livello di `!` e `-`
2. `<<`, `>>` (shift) - piu alta dei confronti, piu bassa di `+`/`-`
3. `&` (AND bit a bit) - piu alta di `^` e `|`
4. `^` (XOR bit a bit) - tra `&` e `|`
5. `|` (OR bit a bit) - piu bassa di `&` e `^`, piu alta di `&&`
6. `&&`, `||` (logici) - precedenza piu bassa

**Esempi:**
```hemlock
// & ha precedenza piu alta di |
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// Shift ha precedenza piu alta degli operatori bit a bit
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// Usa le parentesi per chiarezza
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**Note importanti:**
- Gli operatori bit a bit funzionano solo con tipi interi (non float, stringhe, ecc.)
- La promozione di tipo segue le regole standard (tipi piu piccoli promossi a piu grandi)
- Lo shift a destra (`>>`) e aritmetico per i tipi signed, logico per unsigned
- Le quantita di shift non sono controllate per il range (il comportamento dipende dalla piattaforma per shift grandi)

## Precedenza degli Operatori (Completa)

Dalla precedenza piu alta alla piu bassa:

1. **Unari**: `!`, `-`, `~`
2. **Moltiplicativi**: `*`, `/`, `%`
3. **Additivi**: `+`, `-`
4. **Shift**: `<<`, `>>`
5. **Relazionali**: `<`, `>`, `<=`, `>=`
6. **Uguaglianza**: `==`, `!=`
7. **AND bit a bit**: `&`
8. **XOR bit a bit**: `^`
9. **OR bit a bit**: `|`
10. **AND logico**: `&&`
11. **OR logico**: `||`

**Usa le parentesi per chiarezza:**
```hemlock
// Non chiaro
if (a || b && c) { }

// Chiaro
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## Pattern Comuni

### Pattern: Validazione Input

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### Pattern: Controllo del Range

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("punteggio valido");
}
```

### Pattern: Macchina a Stati

```hemlock
let state = "start";

while (true) {
    switch (state) {
        case "start":
            print("Avvio...");
            state = "running";
            break;

        case "running":
            if (should_pause) {
                state = "paused";
            } else if (should_stop) {
                state = "stopped";
            }
            break;

        case "paused":
            if (should_resume) {
                state = "running";
            }
            break;

        case "stopped":
            print("Fermato");
            break;
    }

    if (state == "stopped") {
        break;
    }
}
```

### Pattern: Iterazione con Filtro

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Stampa solo i numeri pari
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // Salta i numeri dispari
    }
    print(arr[i]);
}
```

### Pattern: Uscita Anticipata

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Uscita anticipata
        }
    }
    return -1;  // Non trovato
}
```

## Best Practice

1. **Usa sempre le parentesi graffe** - Anche per blocchi a singola istruzione (imposto dalla sintassi)
2. **Condizioni esplicite** - Usa `x == 0` invece di `!x` per chiarezza
3. **Evita l'annidamento profondo** - Estrai condizioni annidate in funzioni
4. **Usa return anticipati** - Riduci l'annidamento con clausole di guardia
5. **Spezza condizioni complesse** - Dividi in variabili booleane con nome
6. **Default nello switch** - Includi sempre un caso default
7. **Commenta il fall-through** - Rendi esplicito il fall-through intenzionale

## Insidie Comuni

### Insidia: Assegnazione nella Condizione

```hemlock
// Questo NON e permesso (niente assegnazione nelle condizioni)
if (x = 10) { }  // ERRORE: Errore di sintassi

// Usa il confronto invece
if (x == 10) { }  // OK
```

### Insidia: Break Mancante nello Switch

```hemlock
// Fall-through non intenzionale
switch (x) {
    case 1:
        print("uno");
        // Break mancante - cade nel successivo!
    case 2:
        print("due");  // Eseguito sia per 1 che per 2
        break;
}

// Corretto: Aggiungi break
switch (x) {
    case 1:
        print("uno");
        break;  // Ora corretto
    case 2:
        print("due");
        break;
}
```

### Insidia: Scope della Variabile del Ciclo

```hemlock
// i ha scope nel ciclo
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // ERRORE: i non definito qui
```

## Esempi

### Esempio: FizzBuzz

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

### Esempio: Controllo Numero Primo

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

### Esempio: Sistema di Menu

```hemlock
fn menu() {
    while (true) {
        print("1. Avvia");
        print("2. Impostazioni");
        print("3. Esci");

        let choice = get_input();

        switch (choice) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Arrivederci!");
                return;
            default:
                print("Scelta non valida");
                break;
        }
    }
}
```

## Argomenti Correlati

- [Funzioni](functions.md) - Flusso di controllo con chiamate a funzione e return
- [Gestione degli Errori](error-handling.md) - Flusso di controllo con eccezioni
- [Tipi](types.md) - Conversioni di tipo nelle condizioni

## Vedi Anche

- **Sintassi**: Vedi [Sintassi](syntax.md) per dettagli sulla sintassi delle istruzioni
- **Operatori**: Vedi [Tipi](types.md) per la promozione di tipo nelle operazioni
