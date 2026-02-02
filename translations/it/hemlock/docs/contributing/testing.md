# Guida ai Test per Hemlock

Questa guida spiega la filosofia di testing di Hemlock, come scrivere test e come eseguire la suite di test.

---

## Indice

- [Filosofia di Testing](#filosofia-di-testing)
- [Struttura della Suite di Test](#struttura-della-suite-di-test)
- [Eseguire i Test](#eseguire-i-test)
- [Scrivere Test](#scrivere-test)
- [Categorie di Test](#categorie-di-test)
- [Test di Memory Leak](#test-di-memory-leak)
- [Integrazione Continua](#integrazione-continua)
- [Best Practice](#best-practice)

---

## Filosofia di Testing

### Principi Fondamentali

**1. Test-Driven Development (TDD)**

Scrivi i test **prima** di implementare le funzionalita:

```
1. Scrivi un test che fallisce
2. Implementa la funzionalita
3. Esegui il test (dovrebbe passare)
4. Refactoring se necessario
5. Ripeti
```

**Benefici:**
- Assicura che le funzionalita funzionino davvero
- Previene regressioni
- Documenta il comportamento atteso
- Rende il refactoring piu sicuro

**2. Copertura Completa**

Testa sia i casi di successo che di fallimento:

```hemlock
// Caso di successo
let x: u8 = 255;  // Dovrebbe funzionare

// Caso di fallimento
let y: u8 = 256;  // Dovrebbe generare un errore
```

**3. Testa Presto e Spesso**

Esegui i test:
- Prima di fare commit del codice
- Dopo aver apportato modifiche
- Prima di inviare pull request
- Durante la code review

**Regola:** Tutti i test devono passare prima del merge.

### Cosa Testare

**Testa sempre:**
- Funzionalita di base (percorso felice)
- Condizioni di errore (percorso triste)
- Casi limite (condizioni al contorno)
- Controllo e conversione dei tipi
- Gestione della memoria (nessun leak)
- Concorrenza e race condition

**Esempio di copertura dei test:**
```hemlock
// Funzionalita: String.substr(start, length)

// Percorso felice
print("hello".substr(0, 5));  // "hello"

// Casi limite
print("hello".substr(0, 0));  // "" (vuoto)
print("hello".substr(5, 0));  // "" (alla fine)
print("hello".substr(2, 100)); // "llo" (oltre la fine)

// Casi di errore
// "hello".substr(-1, 5);  // Errore: indice negativo
// "hello".substr(0, -1);  // Errore: lunghezza negativa
```

---

## Struttura della Suite di Test

### Organizzazione delle Directory

```
tests/
├── run_tests.sh          # Script principale per l'esecuzione dei test
├── primitives/           # Test del sistema di tipi
│   ├── integers.hml
│   ├── floats.hml
│   ├── booleans.hml
│   ├── i64.hml
│   └── u64.hml
├── conversions/          # Test di conversione dei tipi
│   ├── int_to_float.hml
│   ├── promotion.hml
│   └── rune_conversions.hml
├── memory/               # Test di puntatori/buffer
│   ├── alloc.hml
│   ├── buffer.hml
│   └── memcpy.hml
├── strings/              # Test delle operazioni sulle stringhe
│   ├── concat.hml
│   ├── methods.hml
│   ├── utf8.hml
│   └── runes.hml
├── control/              # Test del flusso di controllo
│   ├── if.hml
│   ├── switch.hml
│   └── while.hml
├── functions/            # Test di funzioni e closure
│   ├── basics.hml
│   ├── closures.hml
│   └── recursion.hml
├── objects/              # Test degli oggetti
│   ├── literals.hml
│   ├── methods.hml
│   ├── duck_typing.hml
│   └── serialization.hml
├── arrays/               # Test delle operazioni sugli array
│   ├── basics.hml
│   ├── methods.hml
│   └── slicing.hml
├── loops/                # Test dei cicli
│   ├── for.hml
│   ├── while.hml
│   ├── break.hml
│   └── continue.hml
├── exceptions/           # Test della gestione degli errori
│   ├── try_catch.hml
│   ├── finally.hml
│   └── throw.hml
├── io/                   # Test di I/O su file
│   ├── file_object.hml
│   ├── read_write.hml
│   └── seek.hml
├── async/                # Test di concorrenza
│   ├── spawn_join.hml
│   ├── channels.hml
│   └── exceptions.hml
├── ffi/                  # Test FFI
│   ├── basic_call.hml
│   ├── types.hml
│   └── dlopen.hml
├── signals/              # Test della gestione dei segnali
│   ├── basic.hml
│   ├── handlers.hml
│   └── raise.hml
└── args/                 # Test degli argomenti da riga di comando
    └── basic.hml
```

### Nomenclatura dei File di Test

**Convenzioni:**
- Usa nomi descrittivi: `method_chaining.hml` non `test1.hml`
- Raggruppa test correlati: `string_substr.hml`, `string_slice.hml`
- Un'area di funzionalita per file
- Mantieni i file focalizzati e piccoli

---

## Eseguire i Test

### Esegui Tutti i Test

```bash
# Dalla directory root di hemlock
make test

# Oppure direttamente
./tests/run_tests.sh
```

**Output:**
```
Running tests in tests/primitives/...
  ✓ integers.hml
  ✓ floats.hml
  ✓ booleans.hml

Running tests in tests/strings/...
  ✓ concat.hml
  ✓ methods.hml

...

Total: 251 tests
Passed: 251
Failed: 0
```

### Esegui una Categoria Specifica

```bash
# Esegui solo i test delle stringhe
./tests/run_tests.sh tests/strings/

# Esegui solo un file di test
./tests/run_tests.sh tests/strings/concat.hml

# Esegui piu categorie
./tests/run_tests.sh tests/strings/ tests/arrays/
```

### Esegui con Valgrind (Controllo Memory Leak)

```bash
# Controlla un singolo test per leak
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml

# Controlla tutti i test (lento!)
for test in tests/**/*.hml; do
    echo "Testing $test"
    valgrind --leak-check=full --error-exitcode=1 ./hemlock "$test"
done
```

### Debug dei Test Falliti

```bash
# Esegui con output verboso
./hemlock tests/failing_test.hml

# Esegui con gdb
gdb --args ./hemlock tests/failing_test.hml
(gdb) run
(gdb) backtrace  # se crasha
```

---

## Scrivere Test

### Formato dei File di Test

I file di test sono semplicemente programmi Hemlock con output atteso:

**Esempio: tests/primitives/integers.hml**
```hemlock
// Test dei literal interi di base
let x = 42;
print(x);  // Expect: 42

let y: i32 = 100;
print(y);  // Expect: 100

// Test dell'aritmetica
let sum = x + y;
print(sum);  // Expect: 142

// Test dell'inferenza di tipo
let small = 10;
print(typeof(small));  // Expect: i32

let large = 5000000000;
print(typeof(large));  // Expect: i64
```

**Come funzionano i test:**
1. Il test runner esegue il file .hml
2. Cattura l'output su stdout
3. Confronta con l'output atteso (da commenti o file .out separato)
4. Riporta pass/fail

### Metodi per l'Output Atteso

**Metodo 1: Commenti inline (consigliato per test semplici)**

```hemlock
print("hello");  // Expect: hello
print(42);       // Expect: 42
```

Il test runner analizza i commenti `// Expect: ...`.

**Metodo 2: File .out separato**

Crea `nome_test.hml.out` con l'output atteso:

**nome_test.hml:**
```hemlock
print("line 1");
print("line 2");
print("line 3");
```

**nome_test.hml.out:**
```
line 1
line 2
line 3
```

### Testare i Casi di Errore

I test di errore dovrebbero far uscire il programma con stato non-zero:

**Esempio: tests/primitives/range_error.hml**
```hemlock
// Questo dovrebbe fallire con un errore di tipo
let x: u8 = 256;  // Fuori range per u8
```

**Comportamento atteso:**
- Il programma esce con stato non-zero
- Stampa messaggio di errore su stderr

**Gestione del test runner:**
- I test che si aspettano errori dovrebbero essere in file separati
- Usa la convenzione di nomenclatura: `*_error.hml` o `*_fail.hml`
- Documenta l'errore atteso nei commenti

### Testare i Casi di Successo

**Esempio: tests/strings/methods.hml**
```hemlock
// Test di substr
let s = "hello world";
let sub = s.substr(6, 5);
print(sub);  // Expect: world

// Test di find
let pos = s.find("world");
print(pos);  // Expect: 6

// Test di contains
let has = s.contains("lo");
print(has);  // Expect: true

// Test di trim
let padded = "  hello  ";
let trimmed = padded.trim();
print(trimmed);  // Expect: hello
```

### Testare i Casi Limite

**Esempio: tests/arrays/edge_cases.hml**
```hemlock
// Array vuoto
let empty = [];
print(empty.length);  // Expect: 0

// Singolo elemento
let single = [42];
print(single[0]);  // Expect: 42

// Indice negativo (dovrebbe dare errore in un file di test separato)
// print(single[-1]);  // Errore

// Indice oltre la fine (dovrebbe dare errore)
// print(single[100]);  // Errore

// Condizioni al contorno
let arr = [1, 2, 3];
print(arr.slice(0, 0));  // Expect: [] (vuoto)
print(arr.slice(3, 3));  // Expect: [] (vuoto)
print(arr.slice(1, 2));  // Expect: [2]
```

### Testare il Sistema di Tipi

**Esempio: tests/conversions/promotion.hml**
```hemlock
// Test della promozione di tipo nelle operazioni binarie

// i32 + i64 -> i64
let a: i32 = 10;
let b: i64 = 20;
let c = a + b;
print(typeof(c));  // Expect: i64

// i32 + f32 -> f32
let d: i32 = 10;
let e: f32 = 3.14;
let f = d + e;
print(typeof(f));  // Expect: f32

// u8 + i32 -> i32
let g: u8 = 5;
let h: i32 = 10;
let i = g + h;
print(typeof(i));  // Expect: i32
```

### Testare la Concorrenza

**Esempio: tests/async/basic.hml**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Avvia task
let t1 = spawn(compute, 10);
let t2 = spawn(compute, 20);

// Join e stampa risultati
let r1 = join(t1);
let r2 = join(t2);
print(r1);  // Expect: 45
print(r2);  // Expect: 190
```

### Testare le Eccezioni

**Esempio: tests/exceptions/try_catch.hml**
```hemlock
// Test di base try/catch
try {
    throw "error message";
} catch (e) {
    print("Caught: " + e);  // Expect: Caught: error message
}

// Test di finally
let executed = false;
try {
    print("try");  // Expect: try
} finally {
    executed = true;
    print("finally");  // Expect: finally
}

// Test della propagazione delle eccezioni
fn risky(): i32 {
    throw "failure";
}

try {
    risky();
} catch (e) {
    print(e);  // Expect: failure
}
```

---

## Categorie di Test

### Test dei Primitivi

**Cosa testare:**
- Tipi interi (i8, i16, i32, i64, u8, u16, u32, u64)
- Tipi float (f32, f64)
- Tipo boolean
- Tipo string
- Tipo rune
- Tipo null

**Aree di esempio:**
- Sintassi dei literal
- Inferenza di tipo
- Controllo del range
- Comportamento di overflow
- Annotazioni di tipo

### Test delle Conversioni

**Cosa testare:**
- Promozione implicita di tipo
- Conversione esplicita di tipo
- Conversioni con perdita di dati (dovrebbero dare errore)
- Promozione di tipo nelle operazioni
- Confronti tra tipi diversi

### Test della Memoria

**Cosa testare:**
- Correttezza di alloc/free
- Creazione e accesso ai buffer
- Controllo dei limiti sui buffer
- memset, memcpy, realloc
- Rilevamento di memory leak (valgrind)

### Test delle Stringhe

**Cosa testare:**
- Concatenazione
- Tutti i 18 metodi delle stringhe
- Gestione UTF-8
- Indicizzazione con rune
- Concatenazione string + rune
- Casi limite (stringhe vuote, singolo carattere, ecc.)

### Test del Flusso di Controllo

**Cosa testare:**
- if/else/else if
- Cicli while
- Cicli for
- Istruzioni switch
- break/continue
- Istruzioni return

### Test delle Funzioni

**Cosa testare:**
- Definizione e chiamata di funzioni
- Passaggio dei parametri
- Valori di ritorno
- Ricorsione
- Closure e cattura
- Funzioni di prima classe
- Funzioni anonime

### Test degli Oggetti

**Cosa testare:**
- Literal degli oggetti
- Accesso e assegnazione dei campi
- Metodi e binding di self
- Duck typing
- Campi opzionali
- Serializzazione/deserializzazione JSON
- Rilevamento di riferimenti circolari

### Test degli Array

**Cosa testare:**
- Creazione di array
- Indicizzazione e assegnazione
- Tutti i 15 metodi degli array
- Tipi misti
- Ridimensionamento dinamico
- Casi limite (vuoto, singolo elemento)

### Test delle Eccezioni

**Cosa testare:**
- try/catch/finally
- Istruzione throw
- Propagazione delle eccezioni
- try/catch annidati
- Return in try/catch/finally
- Eccezioni non catturate

### Test di I/O

**Cosa testare:**
- Modalita di apertura file
- Operazioni di lettura/scrittura
- Seek/tell
- Proprieta dei file
- Gestione degli errori (file mancanti, ecc.)
- Pulizia delle risorse

### Test Async

**Cosa testare:**
- spawn/join/detach
- send/recv sui canali
- Propagazione delle eccezioni nei task
- Task concorrenti multipli
- Comportamento di blocco dei canali

### Test FFI

**Cosa testare:**
- dlopen/dlclose
- dlsym
- dlcall con vari tipi
- Conversione di tipo
- Gestione degli errori

---

## Test di Memory Leak

### Usare Valgrind

**Uso di base:**
```bash
valgrind --leak-check=full ./hemlock test.hml
```

**Esempio di output (nessun leak):**
```
==12345== HEAP SUMMARY:
==12345==     in use at exit: 0 bytes in 0 blocks
==12345==   total heap usage: 10 allocs, 10 frees, 1,024 bytes allocated
==12345==
==12345== All heap blocks were freed -- no leaks are possible
```

**Esempio di output (con leak):**
```
==12345== LEAK SUMMARY:
==12345==    definitely lost: 64 bytes in 1 blocks
==12345==    indirectly lost: 0 bytes in 0 blocks
==12345==      possibly lost: 0 bytes in 0 blocks
==12345==    still reachable: 0 bytes in 0 blocks
==12345==         suppressed: 0 bytes in 0 blocks
```

### Fonti Comuni di Leak

**1. Chiamate free() mancanti:**
```c
// MALE
char *str = malloc(100);
// ... usa str
// Dimenticato di liberare!

// BENE
char *str = malloc(100);
// ... usa str
free(str);
```

**2. Puntatori persi:**
```c
// MALE
char *ptr = malloc(100);
ptr = malloc(200);  // Perso il riferimento alla prima allocazione!

// BENE
char *ptr = malloc(100);
free(ptr);
ptr = malloc(200);
```

**3. Percorsi di eccezione:**
```c
// MALE
void func() {
    char *data = malloc(100);
    if (error_condition) {
        return;  // Leak!
    }
    free(data);
}

// BENE
void func() {
    char *data = malloc(100);
    if (error_condition) {
        free(data);
        return;
    }
    free(data);
}
```

### Leak Accettabili Conosciuti

Alcuni piccoli "leak" sono allocazioni intenzionali all'avvio:

**Built-in globali:**
```hemlock
// Funzioni built-in, tipi FFI e costanti sono allocati all'avvio
// e non liberati all'uscita (tipicamente ~200 byte)
```

Questi non sono veri leak - sono allocazioni una tantum che persistono per tutta la vita del programma e vengono pulite dal sistema operativo all'uscita.

---

## Integrazione Continua

### GitHub Actions (Futuro)

Una volta impostata la CI, tutti i test verranno eseguiti automaticamente su:
- Push sul branch main
- Creazione/aggiornamento di pull request
- Esecuzioni giornaliere programmate

**Flusso di lavoro CI:**
1. Compila Hemlock
2. Esegui la suite di test
3. Controlla i memory leak (valgrind)
4. Riporta i risultati sulla PR

### Controlli Pre-Commit

Prima di fare commit, esegui:

```bash
# Compila da zero
make clean && make

# Esegui tutti i test
make test

# Controlla alcuni test per leak
valgrind --leak-check=full ./hemlock tests/memory/alloc.hml
valgrind --leak-check=full ./hemlock tests/strings/concat.hml
```

---

## Best Practice

### Da Fare

- **Scrivi i test prima (TDD)**
```bash
1. Crea tests/feature/new_feature.hml
2. Implementa la funzionalita in src/
3. Esegui i test finche non passano
```

- **Testa sia successo che fallimento**
```hemlock
// Successo: tests/feature/success.hml
let result = do_thing();
print(result);  // Expect: valore atteso

// Fallimento: tests/feature/failure.hml
do_invalid_thing();  // Dovrebbe dare errore
```

- **Usa nomi di test descrittivi**
```
Bene: tests/strings/substr_utf8_boundary.hml
Male: tests/test1.hml
```

- **Mantieni i test focalizzati**
- Un'area di funzionalita per file
- Setup e asserzioni chiare
- Codice minimo

- **Aggiungi commenti che spiegano test complicati**
```hemlock
// Test che la closure cattura la variabile esterna per riferimento
fn outer() {
    let x = 10;
    let f = fn() { return x; };
    x = 20;  // Modifica dopo la creazione della closure
    return f();  // Dovrebbe restituire 20, non 10
}
```

- **Testa i casi limite**
- Input vuoti
- Valori null
- Valori al contorno (min/max)
- Input grandi
- Valori negativi

### Da Non Fare

- **Non saltare i test**
- Tutti i test devono passare prima del merge
- Non commentare i test che falliscono
- Correggi il bug o rimuovi la funzionalita

- **Non scrivere test che dipendono l'uno dall'altro**
```hemlock
// MALE: test2.hml dipende dall'output di test1.hml
// I test dovrebbero essere indipendenti
```

- **Non usare valori casuali nei test**
```hemlock
// MALE: Non deterministico
let x = random();
print(x);  // Non puoi prevedere l'output

// BENE: Deterministico
let x = 42;
print(x);  // Expect: 42
```

- **Non testare dettagli implementativi**
```hemlock
// MALE: Testare la struttura interna
let obj = { x: 10 };
// Non controllare l'ordine interno dei campi, capacita, ecc.

// BENE: Testare il comportamento
print(obj.x);  // Expect: 10
```

- **Non ignorare i memory leak**
- Tutti i test dovrebbero essere puliti a valgrind
- Documenta i leak conosciuti/accettabili
- Correggi i leak prima del merge

### Manutenzione dei Test

**Quando aggiornare i test:**
- Il comportamento della funzionalita cambia
- Le correzioni di bug richiedono nuovi casi di test
- Vengono scoperti casi limite
- Miglioramenti delle prestazioni

**Quando rimuovere i test:**
- Funzionalita rimossa dal linguaggio
- Il test duplica copertura esistente
- Il test era errato

**Refactoring dei test:**
- Raggruppa test correlati insieme
- Estrai codice di setup comune
- Usa nomenclatura consistente
- Mantieni i test semplici e leggibili

---

## Esempio di Sessione di Test

Ecco un esempio completo di aggiunta di una funzionalita con test:

### Funzionalita: Aggiungere il metodo `array.first()`

**1. Scrivi prima il test:**

```bash
# Crea il file di test
cat > tests/arrays/first_method.hml << 'EOF'
// Test del metodo array.first()

// Caso base
let arr = [1, 2, 3];
print(arr.first());  // Expect: 1

// Singolo elemento
let single = [42];
print(single.first());  // Expect: 42

// Array vuoto (dovrebbe dare errore - file di test separato)
// let empty = [];
// print(empty.first());  // Errore
EOF
```

**2. Esegui il test (dovrebbe fallire):**

```bash
./hemlock tests/arrays/first_method.hml
# Error: Method 'first' not found on array
```

**3. Implementa la funzionalita:**

Modifica `src/interpreter/builtins.c`:

```c
// Aggiungi il metodo array_first
Value *array_first(Value *self, Value **args, int arg_count)
{
    if (self->array_value->length == 0) {
        fprintf(stderr, "Error: Cannot get first element of empty array\n");
        exit(1);
    }

    return value_copy(&self->array_value->elements[0]);
}

// Registra nella tabella dei metodi array
// ... aggiungi alla registrazione dei metodi array
```

**4. Esegui il test (dovrebbe passare):**

```bash
./hemlock tests/arrays/first_method.hml
1
42
# Successo!
```

**5. Controlla i memory leak:**

```bash
valgrind --leak-check=full ./hemlock tests/arrays/first_method.hml
# All heap blocks were freed -- no leaks are possible
```

**6. Esegui l'intera suite di test:**

```bash
make test
# Total: 252 tests (251 + nuovo)
# Passed: 252
# Failed: 0
```

**7. Commit:**

```bash
git add tests/arrays/first_method.hml src/interpreter/builtins.c
git commit -m "Add array.first() method with tests"
```

---

## Riepilogo

**Ricorda:**
- Scrivi i test prima (TDD)
- Testa i casi di successo e fallimento
- Esegui tutti i test prima di fare commit
- Controlla i memory leak
- Documenta i problemi noti
- Mantieni i test semplici e focalizzati

**La qualita dei test e importante quanto la qualita del codice!**
