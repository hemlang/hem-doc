# Contribuire a Hemlock

Grazie per il tuo interesse a contribuire a Hemlock! Questa guida ti aiutera a capire come contribuire efficacemente mantenendo la filosofia di design del linguaggio e la qualita del codice.

---

## Indice

- [Prima di Iniziare](#prima-di-iniziare)
- [Flusso di Lavoro per i Contributi](#flusso-di-lavoro-per-i-contributi)
- [Linee Guida sullo Stile del Codice](#linee-guida-sullo-stile-del-codice)
- [Cosa Contribuire](#cosa-contribuire)
- [Cosa NON Contribuire](#cosa-non-contribuire)
- [Pattern Comuni](#pattern-comuni)
- [Aggiungere Nuove Funzionalita](#aggiungere-nuove-funzionalita)
- [Processo di Code Review](#processo-di-code-review)

---

## Prima di Iniziare

### Letture Obbligatorie

Prima di contribuire, leggi questi documenti nell'ordine indicato:

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Comprendi i principi fondamentali di Hemlock
2. **`/home/user/hemlock/docs/design/implementation.md`** - Impara la struttura del codebase
3. **`/home/user/hemlock/docs/contributing/testing.md`** - Comprendi i requisiti di testing
4. **Questo documento** - Impara le linee guida per i contributi

### Prerequisiti

**Conoscenze richieste:**
- Programmazione C (puntatori, gestione della memoria, struct)
- Basi di compilatori/interpreti (lexing, parsing, AST)
- Flusso di lavoro Git e GitHub
- Linea di comando Unix/Linux

**Strumenti richiesti:**
- Compilatore GCC o Clang
- Sistema di build Make
- Controllo versione Git
- Valgrind (per rilevare memory leak)
- Editor di testo o IDE di base

### Canali di Comunicazione

**Dove fare domande:**
- GitHub Issues - Segnalazioni di bug e richieste di funzionalita
- GitHub Discussions - Domande generali e discussioni sul design
- Commenti sulle Pull Request - Feedback specifico sul codice

---

## Flusso di Lavoro per i Contributi

### 1. Trova o Crea una Issue

**Prima di scrivere codice:**
- Verifica se esiste gia una issue per il tuo contributo
- Se non esiste, creane una descrivendo cosa vuoi fare
- Aspetta il feedback dei maintainer prima di iniziare modifiche importanti
- Piccole correzioni di bug possono saltare questo passaggio

**Una buona descrizione della issue include:**
- Descrizione del problema (cosa non funziona o manca)
- Soluzione proposta (come intendi risolverlo)
- Esempi (snippet di codice che mostrano il problema)
- Motivazione (perche questa modifica e in linea con la filosofia di Hemlock)

### 2. Fork e Clone

```bash
# Prima fai il fork del repository su GitHub, poi:
git clone https://github.com/TUO_USERNAME/hemlock.git
cd hemlock
git checkout -b feature/nome-della-tua-feature
```

### 3. Apporta le Tue Modifiche

Segui queste linee guida:
- Scrivi i test prima (approccio TDD)
- Implementa la funzionalita
- Assicurati che tutti i test passino
- Controlla la presenza di memory leak
- Aggiorna la documentazione

### 4. Testa le Tue Modifiche

```bash
# Esegui l'intera suite di test
make test

# Esegui una categoria di test specifica
./tests/run_tests.sh tests/category/

# Controlla i memory leak
valgrind ./hemlock tests/your_test.hml

# Compila e testa
make clean && make && make test
```

### 5. Esegui il Commit delle Modifiche

**Buoni messaggi di commit:**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**Formato del messaggio di commit:**
- Prima riga: Breve riepilogo (max 50 caratteri)
- Riga vuota
- Spiegazione dettagliata (a capo a 72 caratteri)
- Riferimento ai numeri delle issue

### 6. Invia una Pull Request

**Prima di inviare:**
- Rebase sull'ultimo branch main
- Assicurati che tutti i test passino
- Esegui valgrind per controllare i leak
- Aggiorna CLAUDE.md se aggiungi funzionalita visibili all'utente

**La descrizione della pull request dovrebbe includere:**
- Quale problema risolve
- Come lo risolve
- Modifiche che rompono la compatibilita (se presenti)
- Esempi della nuova sintassi o comportamento
- Riepilogo della copertura dei test

---

## Linee Guida sullo Stile del Codice

### Stile del Codice C

**Formattazione:**
```c
// Indenta con 4 spazi (niente tab)
// Stile K&R per le parentesi nelle funzioni
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // Parentesi sulla stessa riga per le strutture di controllo
        do_something();
    }
}

// Lunghezza riga: max 100 caratteri
// Usa spazi intorno agli operatori
int result = (a + b) * c;

// Asterisco del puntatore con il tipo
char *string;   // Corretto
char* string;   // Evitare
char * string;  // Evitare
```

**Convenzioni di denominazione:**
```c
// Funzioni: minuscolo_con_underscore
void eval_expression(ASTNode *node);

// Tipi: PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// Costanti: MAIUSCOLO_CON_UNDERSCORE
#define MAX_BUFFER_SIZE 4096

// Variabili: minuscolo_con_underscore
int item_count;
Value *current_value;

// Enum: PREFISSO_TIPO_NOME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**Commenti:**
```c
// Commenti su una riga per brevi spiegazioni
// Usa frasi complete con corretta maiuscola

/*
 * Commenti multi-riga per spiegazioni piu lunghe
 * Allinea gli asterischi per leggibilita
 */

/**
 * Commento di documentazione della funzione
 * @param node - Nodo AST da valutare
 * @return Valore valutato
 */
Value eval_expr(ASTNode *node);
```

**Gestione degli errori:**
```c
// Controlla tutte le chiamate malloc
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Error: Out of memory\n");
    exit(1);
}

// Fornisci contesto nei messaggi di errore
if (file == NULL) {
    fprintf(stderr, "Error: Failed to open '%s': %s\n",
            filename, strerror(errno));
    exit(1);
}

// Usa messaggi di errore significativi
// Male: "Error: Invalid value"
// Bene: "Error: Expected integer, got string"
```

**Gestione della memoria:**
```c
// Libera sempre cio che allochi
Value *val = value_create_i32(42);
// ... usa val
value_free(val);

// Imposta i puntatori a NULL dopo averli liberati (previene double-free)
free(ptr);
ptr = NULL;

// Documenta la proprieta nei commenti
// Questa funzione prende la proprieta di 'value' e lo liberera
void store_value(Value *value);

// Questa funzione NON prende la proprieta (il chiamante deve liberare)
Value *get_value(void);
```

### Organizzazione del Codice

**Struttura dei file:**
```c
// 1. Include (prima header di sistema, poi locali)
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. Costanti e macro
#define INITIAL_CAPACITY 16

// 3. Definizioni di tipo
typedef struct Foo Foo;

// 4. Dichiarazioni di funzioni statiche (helper interni)
static void helper_function(void);

// 5. Implementazioni delle funzioni pubbliche
void public_api_function(void)
{
    // Implementazione
}

// 6. Implementazioni delle funzioni statiche
static void helper_function(void)
{
    // Implementazione
}
```

**File header:**
```c
// Usa header guard
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// Dichiarazioni forward
typedef struct Value Value;

// Solo API pubblica negli header
void public_function(Value *val);

// Documenta parametri e valori di ritorno
/**
 * Valuta un nodo AST di espressione
 * @param node - Il nodo AST da valutare
 * @param env - L'ambiente corrente
 * @return Il valore risultante
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## Cosa Contribuire

### Contributi Incoraggiati

**Correzioni di bug:**
- Memory leak
- Segmentation fault
- Comportamenti errati
- Miglioramenti ai messaggi di errore

**Documentazione:**
- Commenti nel codice
- Documentazione delle API
- Guide utente e tutorial
- Programmi di esempio
- Documentazione dei casi di test

**Test:**
- Casi di test aggiuntivi per funzionalita esistenti
- Copertura dei casi limite
- Test di regressione per bug corretti
- Benchmark delle prestazioni

**Piccole aggiunte di funzionalita:**
- Nuove funzioni built-in (se si adattano alla filosofia)
- Metodi per stringhe/array
- Funzioni di utilita
- Miglioramenti alla gestione degli errori

**Miglioramenti delle prestazioni:**
- Algoritmi piu veloci (senza cambiare la semantica)
- Riduzione dell'uso della memoria
- Suite di benchmark
- Strumenti di profiling

**Strumenti:**
- Evidenziazione della sintassi per editor
- Language Server Protocol (LSP)
- Integrazione con debugger
- Miglioramenti al sistema di build

### Discuti Prima

**Funzionalita importanti:**
- Nuovi costrutti del linguaggio
- Modifiche al sistema di tipi
- Aggiunte alla sintassi
- Primitive di concorrenza

**Come discutere:**
1. Apri una issue o discussione su GitHub
2. Descrivi la funzionalita e la motivazione
3. Mostra codice di esempio
4. Spiega come si adatta alla filosofia di Hemlock
5. Aspetta il feedback dei maintainer
6. Itera sul design prima di implementare

---

## Cosa NON Contribuire

### Contributi Scoraggiati

**Non aggiungere funzionalita che:**
- Nascondono complessita all'utente
- Rendono il comportamento implicito o magico
- Rompono semantica o sintassi esistenti
- Aggiungono garbage collection o gestione automatica della memoria
- Violano il principio "esplicito piuttosto che implicito"

**Esempi di contributi rifiutati:**

**1. Inserimento automatico del punto e virgola**
```hemlock
// MALE: Questo verrebbe rifiutato
let x = 5  // Nessun punto e virgola
let y = 10 // Nessun punto e virgola
```
Perche: Rende la sintassi ambigua, nasconde gli errori

**2. RAII/distruttori**
```hemlock
// MALE: Questo verrebbe rifiutato
let f = open("file.txt");
// File chiuso automaticamente alla fine dello scope
```
Perche: Nasconde quando le risorse vengono rilasciate, non e esplicito

**3. Coercizione implicita di tipo che perde dati**
```hemlock
// MALE: Questo verrebbe rifiutato
let x: i32 = 3.14;  // Tronca silenziosamente a 3
```
Perche: La perdita di dati dovrebbe essere esplicita, non silenziosa

**4. Garbage collection**
```c
// MALE: Questo verrebbe rifiutato
void *gc_malloc(size_t size) {
    // Traccia l'allocazione per pulizia automatica
}
```
Perche: Nasconde la gestione della memoria, prestazioni imprevedibili

**5. Sistema di macro complesso**
```hemlock
// MALE: Questo verrebbe rifiutato
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
Perche: Troppa magia, rende il codice difficile da ragionare

### Motivi Comuni di Rifiuto

**"Questo e troppo implicito"**
- Soluzione: Rendi il comportamento esplicito e documentalo

**"Questo nasconde complessita"**
- Soluzione: Esponi la complessita ma rendila ergonomica

**"Questo rompe il codice esistente"**
- Soluzione: Trova un'alternativa non distruttiva o discuti il versioning

**"Questo non si adatta alla filosofia di Hemlock"**
- Soluzione: Rileggi philosophy.md e riconsidera l'approccio

---

## Pattern Comuni

### Pattern per la Gestione degli Errori

```c
// Usa questo pattern per errori recuperabili nel codice Hemlock
Value *divide(Value *a, Value *b)
{
    // Controlla le precondizioni
    if (b->type != TYPE_I32) {
        // Restituisci valore di errore o solleva eccezione
        return create_error("Expected integer divisor");
    }

    if (b->i32_value == 0) {
        return create_error("Division by zero");
    }

    // Esegui l'operazione
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### Pattern per la Gestione della Memoria

```c
// Pattern: Alloca, usa, libera
void process_data(void)
{
    // Alloca
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // Usa
    if (buf && str) {
        // ... fai il lavoro
    }

    // Libera (in ordine inverso rispetto all'allocazione)
    free(str);
    free_buffer(buf);
}
```

### Pattern per la Creazione di Valori

```c
// Crea valori usando i costruttori
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Out of memory\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### Pattern per il Controllo dei Tipi

```c
// Controlla i tipi prima delle operazioni
Value *add_values(Value *a, Value *b)
{
    // Controllo dei tipi
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Type mismatch");
    }

    // Sicuro procedere
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### Pattern per la Costruzione di Stringhe

```c
// Costruisci stringhe in modo efficiente
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Error: %s (line %d)", detail, line_number);
}
```

---

## Aggiungere Nuove Funzionalita

### Checklist per l'Aggiunta di Funzionalita

Quando aggiungi una nuova funzionalita, segui questi passaggi:

#### 1. Fase di Design

- [ ] Leggi philosophy.md per assicurarti dell'allineamento
- [ ] Crea una issue su GitHub che descrive la funzionalita
- [ ] Ottieni l'approvazione dei maintainer per il design
- [ ] Scrivi la specifica (sintassi, semantica, esempi)
- [ ] Considera i casi limite e le condizioni di errore

#### 2. Fase di Implementazione

**Se aggiungi un costrutto del linguaggio:**

- [ ] Aggiungi il tipo di token in `lexer.h` (se necessario)
- [ ] Aggiungi la regola del lexer in `lexer.c` (se necessario)
- [ ] Aggiungi il tipo di nodo AST in `ast.h`
- [ ] Aggiungi il costruttore AST in `ast.c`
- [ ] Aggiungi la regola del parser in `parser.c`
- [ ] Aggiungi il comportamento runtime in `runtime.c` o nel modulo appropriato
- [ ] Gestisci la pulizia nelle funzioni di free dell'AST

**Se aggiungi una funzione built-in:**

- [ ] Aggiungi l'implementazione della funzione in `builtins.c`
- [ ] Registra la funzione in `register_builtins()`
- [ ] Gestisci tutte le combinazioni di tipi di parametri
- [ ] Restituisci valori di errore appropriati
- [ ] Documenta parametri e tipo di ritorno

**Se aggiungi un tipo di valore:**

- [ ] Aggiungi l'enum del tipo in `values.h`
- [ ] Aggiungi il campo alla union Value
- [ ] Aggiungi il costruttore in `values.c`
- [ ] Aggiungi a `value_free()` per la pulizia
- [ ] Aggiungi a `value_copy()` per la copia
- [ ] Aggiungi a `value_to_string()` per la stampa
- [ ] Aggiungi regole di promozione del tipo se numerico

#### 3. Fase di Testing

- [ ] Scrivi casi di test (vedi testing.md)
- [ ] Testa i casi di successo
- [ ] Testa i casi di errore
- [ ] Testa i casi limite
- [ ] Esegui l'intera suite di test (`make test`)
- [ ] Controlla i memory leak con valgrind
- [ ] Testa su piu piattaforme (se possibile)

#### 4. Fase di Documentazione

- [ ] Aggiorna CLAUDE.md con la documentazione per l'utente
- [ ] Aggiungi commenti nel codice che spiegano l'implementazione
- [ ] Crea esempi in `examples/`
- [ ] Aggiorna i file docs/ pertinenti
- [ ] Documenta eventuali modifiche che rompono la compatibilita

#### 5. Fase di Invio

- [ ] Pulisci il codice di debug e i commenti
- [ ] Verifica la conformita allo stile del codice
- [ ] Rebase sull'ultimo main
- [ ] Crea la pull request con descrizione dettagliata
- [ ] Rispondi al feedback della code review

### Esempio: Aggiungere un Nuovo Operatore

Vediamo come aggiungere l'operatore modulo `%` come esempio:

**1. Lexer (lexer.c):**
```c
// Aggiungi allo switch statement in get_next_token()
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. Header del lexer (lexer.h):**
```c
typedef enum {
    // ... token esistenti
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h):**
```c
typedef enum {
    // ... operatori esistenti
    OP_MOD,
    // ...
} BinaryOp;
```

**4. Parser (parser.c):**
```c
// Aggiungi a parse_multiplicative() o al livello di precedenza appropriato
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. Runtime (runtime.c):**
```c
// Aggiungi a eval_binary_op()
case OP_MOD:
    // Controllo dei tipi
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Error: Modulo by zero\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... gestisci altre combinazioni di tipi
    break;
```

**6. Test (tests/operators/modulo.hml):**
```hemlock
// Modulo base
print(10 % 3);  // Expect: 2

// Modulo negativo
print(-10 % 3); // Expect: -1

// Caso di errore (dovrebbe fallire)
// print(10 % 0);  // Divisione per zero
```

**7. Documentazione (CLAUDE.md):**
```markdown
### Operatori Aritmetici
- `+` - Addizione
- `-` - Sottrazione
- `*` - Moltiplicazione
- `/` - Divisione
- `%` - Modulo (resto)
```

---

## Processo di Code Review

### Cosa Cercano i Reviewer

**1. Correttezza**
- Il codice fa quello che dichiara?
- I casi limite sono gestiti?
- Ci sono memory leak?
- Gli errori sono gestiti correttamente?

**2. Allineamento con la Filosofia**
- Questo si adatta ai principi di design di Hemlock?
- E esplicito o implicito?
- Nasconde complessita?

**3. Qualita del Codice**
- Il codice e leggibile e manutenibile?
- I nomi delle variabili sono descrittivi?
- Le funzioni hanno dimensioni ragionevoli?
- C'e documentazione adeguata?

**4. Testing**
- Ci sono casi di test sufficienti?
- I test coprono i percorsi di successo e fallimento?
- I casi limite sono testati?

**5. Documentazione**
- La documentazione per l'utente e aggiornata?
- I commenti nel codice sono chiari?
- Sono forniti esempi?

### Rispondere al Feedback

**Fai:**
- Ringrazia i reviewer per il loro tempo
- Fai domande di chiarimento se non capisci
- Spiega il tuo ragionamento se non sei d'accordo
- Apporta le modifiche richieste prontamente
- Aggiorna la descrizione della PR se cambia lo scope

**Non fare:**
- Prendere le critiche sul personale
- Discutere in modo difensivo
- Ignorare il feedback
- Fare force-push sopra i commenti della review (a meno che non stai facendo rebase)
- Aggiungere modifiche non correlate alla PR

### Far Mergiare la Tua PR

**Requisiti per il merge:**
- [ ] Tutti i test passano
- [ ] Nessun memory leak (valgrind pulito)
- [ ] Approvazione della code review dal maintainer
- [ ] Documentazione aggiornata
- [ ] Segue le linee guida sullo stile del codice
- [ ] Si allinea con la filosofia di Hemlock

**Tempistiche:**
- PR piccole (correzioni di bug): Di solito revisionate entro pochi giorni
- PR medie (nuove funzionalita): Possono richiedere 1-2 settimane
- PR grandi (modifiche importanti): Richiedono discussione approfondita

---

## Risorse Aggiuntive

### Risorse di Apprendimento

**Capire gli interpreti:**
- "Crafting Interpreters" di Robert Nystrom
- "Writing An Interpreter In Go" di Thorsten Ball
- "Modern Compiler Implementation in C" di Andrew Appel

**Programmazione C:**
- "The C Programming Language" di K&R
- "Expert C Programming" di Peter van der Linden
- "C Interfaces and Implementations" di David Hanson

**Gestione della memoria:**
- Documentazione di Valgrind
- "Understanding and Using C Pointers" di Richard Reese

### Comandi Utili

```bash
# Compila con simboli di debug
make clean && make CFLAGS="-g -O0"

# Esegui con valgrind
valgrind --leak-check=full ./hemlock script.hml

# Esegui una categoria di test specifica
./tests/run_tests.sh tests/strings/

# Genera file di tag per la navigazione del codice
ctags -R .

# Trova tutti i TODO e FIXME
grep -rn "TODO\|FIXME" src/ include/
```

---

## Domande?

Se hai domande su come contribuire:

1. Controlla la documentazione in `docs/`
2. Cerca nelle issue esistenti su GitHub
3. Chiedi nelle GitHub Discussions
4. Apri una nuova issue con la tua domanda

**Grazie per contribuire a Hemlock!**
