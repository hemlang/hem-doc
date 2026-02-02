# Gestione degli Errori

Hemlock supporta la gestione degli errori basata su eccezioni con `try`, `catch`, `finally`, `throw` e `panic`. Questa guida copre gli errori recuperabili con le eccezioni e gli errori non recuperabili con panic.

## Panoramica

```hemlock
// Gestione base degli errori
try {
    risky_operation();
} catch (e) {
    print("Errore: " + e);
}

// Con pulizia
try {
    process_file();
} catch (e) {
    print("Fallito: " + e);
} finally {
    cleanup();
}

// Lanciare errori
fn divide(a, b) {
    if (b == 0) {
        throw "divisione per zero";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Sintassi

**Try/catch base:**
```hemlock
try {
    // codice rischioso
} catch (e) {
    // gestisci l'errore, e contiene il valore lanciato
}
```

**Try/finally:**
```hemlock
try {
    // codice rischioso
} finally {
    // viene sempre eseguito, anche se viene lanciata un'eccezione
}
```

**Try/catch/finally:**
```hemlock
try {
    // codice rischioso
} catch (e) {
    // gestisci l'errore
} finally {
    // codice di pulizia
}
```

### Blocco Try

Il blocco try esegue le istruzioni in sequenza:

```hemlock
try {
    print("Avvio...");
    risky_operation();
    print("Successo!");  // Solo se nessuna eccezione
}
```

**Comportamento:**
- Esegue le istruzioni in ordine
- Se viene lanciata un'eccezione: salta a `catch` o `finally`
- Se nessuna eccezione: esegue `finally` (se presente) poi continua

### Blocco Catch

Il blocco catch riceve il valore lanciato:

```hemlock
try {
    throw "oops";
} catch (error) {
    print("Catturato: " + error);  // error = "oops"
    // error accessibile solo qui
}
// error non accessibile qui
```

**Parametro catch:**
- Riceve il valore lanciato (qualsiasi tipo)
- Ha scope nel blocco catch
- Puo essere chiamato come vuoi (convenzionalmente `e`, `err` o `error`)

**Cosa puoi fare nel catch:**
```hemlock
try {
    risky_operation();
} catch (e) {
    // Registra l'errore
    print("Errore: " + e);

    // Rilancia lo stesso errore
    throw e;

    // Lancia un errore diverso
    throw "errore diverso";

    // Restituisci un valore di default
    return null;

    // Gestisci e continua
    // (nessun rilancio)
}
```

### Blocco Finally

Il blocco finally **viene sempre eseguito**:

```hemlock
try {
    print("1: blocco try");
    throw "errore";
} catch (e) {
    print("2: blocco catch");
} finally {
    print("3: blocco finally");  // Eseguito sempre
}
print("4: dopo try/catch/finally");

// Output: 1: blocco try, 2: blocco catch, 3: blocco finally, 4: dopo try/catch/finally
```

**Quando finally viene eseguito:**
- Dopo il blocco try (se nessuna eccezione)
- Dopo il blocco catch (se l'eccezione e stata catturata)
- Anche se try/catch contiene `return`, `break` o `continue`
- Prima che il flusso di controllo esca dal try/catch

**Finally con return:**
```hemlock
fn example() {
    try {
        return 1;  // Restituisce 1 dopo l'esecuzione di finally
    } finally {
        print("pulizia");  // Eseguito prima del return
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Il return di finally sovrascrive - restituisce 2
    }
}
```

**Finally con flusso di controllo:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Interrompe dopo l'esecuzione di finally
        }
    } finally {
        print("pulizia " + typeof(i));
    }
}
```

## Istruzione Throw

### Throw Base

Lancia qualsiasi valore come eccezione:

```hemlock
throw "messaggio di errore";
throw 404;
throw { code: 500, message: "Errore interno" };
throw null;
throw ["errore", "dettagli"];
```

**Esecuzione:**
1. Valuta l'espressione
2. Salta immediatamente al `catch` piu vicino
3. Se non c'e `catch`, si propaga sullo stack delle chiamate

### Lanciare Errori

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "L'eta non puo essere negativa";
    }
    if (age > 150) {
        throw "L'eta non e realistica";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Errore di validazione: " + e);
}
```

### Lanciare Oggetti Errore

Crea informazioni di errore strutturate:

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "Il file non esiste"
        };
    }
    // ... leggi il file
}

try {
    read_file("mancante.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("File non trovato: " + e.path);
    }
}
```

### Rilanciare

Cattura e rilancia errori:

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Registro errore: " + e);
        throw e;  // Rilancia al chiamante
    }
}

try {
    wrapper();
} catch (e) {
    print("Catturato nel main: " + e);
}
```

## Eccezioni Non Catturate

Se un'eccezione si propaga fino alla cima dello stack delle chiamate senza essere catturata:

```hemlock
fn foo() {
    throw "non catturata!";
}

foo();  // Crash con: Runtime error: non catturata!
```

**Comportamento:**
- Il programma crasha
- Stampa messaggio di errore su stderr
- Esce con codice di stato non-zero
- Stack trace da aggiungere nelle versioni future

## Panic - Errori Non Recuperabili

### Cos'e Panic?

`panic()` e per **errori non recuperabili** che dovrebbero terminare immediatamente il programma:

```hemlock
panic();                    // Messaggio default: "panic!"
panic("messaggio custom");  // Messaggio personalizzato
panic(42);                  // Valori non-stringa vengono stampati
```

**Semantica:**
- **Esce immediatamente** dal programma con codice di uscita 1
- Stampa messaggio di errore su stderr: `panic: <messaggio>`
- **NON catturabile** con try/catch
- Usa per bug ed errori non recuperabili

### Panic vs Throw

```hemlock
// throw - Errore recuperabile (puo essere catturato)
try {
    throw "errore recuperabile";
} catch (e) {
    print("Catturato: " + e);  // Catturato con successo
}

// panic - Errore non recuperabile (non puo essere catturato)
try {
    panic("errore non recuperabile");  // Il programma esce immediatamente
} catch (e) {
    print("Questo non viene mai eseguito");  // Mai eseguito
}
```

### Quando Usare Panic

**Usa panic per:**
- **Bug**: Codice non raggiungibile e stato raggiunto
- **Stato non valido**: Rilevata corruzione della struttura dati
- **Errori non recuperabili**: Risorsa critica non disponibile
- **Fallimenti di asserzione**: Quando `assert()` non e sufficiente

**Esempi:**
```hemlock
// Codice non raggiungibile
fn process_state(state: i32) {
    if (state == 1) {
        return "pronto";
    } else if (state == 2) {
        return "in esecuzione";
    } else if (state == 3) {
        return "fermato";
    } else {
        panic("stato non valido: " + typeof(state));  // Non dovrebbe mai succedere
    }
}

// Controllo risorsa critica
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json non trovato - impossibile avviare");
    }
    // ...
}

// Invariante della struttura dati
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() chiamato su stack vuoto");
    }
    return stack.pop();
}
```

### Quando NON Usare Panic

**Usa throw invece per:**
- Validazione input utente
- File non trovato
- Errori di rete
- Condizioni di errore attese

```hemlock
// MALE: Panic per errori attesi
fn divide(a, b) {
    if (b == 0) {
        panic("divisione per zero");  // Troppo drastico
    }
    return a / b;
}

// BENE: Throw per errori attesi
fn divide(a, b) {
    if (b == 0) {
        throw "divisione per zero";  // Recuperabile
    }
    return a / b;
}
```

## Interazioni con il Flusso di Controllo

### Return Dentro Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Restituisce 1 dopo l'esecuzione di finally
    } finally {
        print("pulizia");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Il return di finally sovrascrive il return di try - restituisce 2
    }
}
```

**Regola:** I valori di return del blocco finally sovrascrivono i valori di return di try/catch.

### Break/Continue Dentro Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Interrompe dopo l'esecuzione di finally
    } finally {
        print("pulizia " + typeof(i));
    }
}
```

**Regola:** Break/continue vengono eseguiti dopo il blocco finally.

### Try/Catch Annidati

```hemlock
try {
    try {
        throw "interno";
    } catch (e) {
        print("Catturato: " + e);  // Stampa: Catturato: interno
        throw "esterno";  // Rilancia errore diverso
    }
} catch (e) {
    print("Catturato: " + e);  // Stampa: Catturato: esterno
}
```

**Regola:** I blocchi try/catch annidati funzionano come previsto, i catch interni vengono eseguiti prima.

## Pattern Comuni

### Pattern: Pulizia Risorse

Usa sempre `finally` per la pulizia:

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Errore nell'elaborazione del file: " + e);
    } finally {
        if (file != null) {
            file.close();  // Chiude sempre, anche in caso di errore
        }
    }
}
```

### Pattern: Wrapping degli Errori

Avvolgi errori di livello inferiore con contesto:

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Impossibile caricare config da " + path + ": " + e;
    }
}
```

### Pattern: Recupero dagli Errori

Fornisci un fallback in caso di errore:

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "divisione per zero";
        }
        return a / b;
    } catch (e) {
        print("Errore: " + e);
        return null;  // Valore di fallback
    }
}
```

### Pattern: Validazione

Usa le eccezioni per la validazione:

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Nome obbligatorio";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Eta non valida";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Email non valida";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "non_valida" });
} catch (e) {
    print("Validazione fallita: " + e);
}
```

### Pattern: Tipi di Errore Multipli

Usa oggetti errore per distinguere i tipi di errore:

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "I dati sono null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Atteso array" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "L'array e vuoto" };
    }

    // ... elabora
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("Nessun dato fornito");
    } else if (e.type == "TypeError") {
        print("Tipo di dato errato: " + e.message);
    } else {
        print("Errore: " + e.message);
    }
}
```

## Best Practice

1. **Usa le eccezioni per casi eccezionali** - Non per il flusso di controllo normale
2. **Lancia errori significativi** - Usa stringhe o oggetti con contesto
3. **Usa sempre finally per la pulizia** - Assicura che le risorse vengano liberate
4. **Non catturare e ignorare** - Almeno registra l'errore
5. **Rilancia quando appropriato** - Lascia gestire al chiamante se non puoi
6. **Panic per i bug** - Usa panic per errori non recuperabili
7. **Documenta le eccezioni** - Rendi chiaro cosa possono lanciare le funzioni

## Insidie Comuni

### Insidia: Ingoiare gli Errori

```hemlock
// MALE: Fallimento silenzioso
try {
    risky_operation();
} catch (e) {
    // Errore ignorato - fallimento silenzioso
}

// BENE: Registra o gestisci
try {
    risky_operation();
} catch (e) {
    print("Operazione fallita: " + e);
    // Gestisci appropriatamente
}
```

### Insidia: Override di Finally

```hemlock
// MALE: Finally sovrascrive il return
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Restituisce 0, non 42!
    }
}

// BENE: Non fare return nel finally
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Solo pulizia, nessun return
    }
}
```

### Insidia: Dimenticare la Pulizia

```hemlock
// MALE: Il file potrebbe non essere chiuso in caso di errore
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Potrebbe lanciare
    file.close();  // Mai raggiunto se c'e errore
}

// BENE: Usa finally
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Insidia: Usare Panic per Errori Attesi

```hemlock
// MALE: Panic per errore atteso
fn read_config(path) {
    if (!file_exists(path)) {
        panic("File di config non trovato");  // Troppo drastico
    }
    return read_file(path);
}

// BENE: Throw per errore atteso
fn read_config(path) {
    if (!file_exists(path)) {
        throw "File di config non trovato: " + path;  // Recuperabile
    }
    return read_file(path);
}
```

## Esempi

### Esempio: Gestione Errori Base

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "divisione per zero";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Errore: " + e);  // Stampa: Errore: divisione per zero
}
```

### Esempio: Gestione Risorse

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("File copiato con successo");
    } catch (e) {
        print("Impossibile copiare il file: " + e);
        throw e;  // Rilancia
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Esempio: Gestione Errori Annidata

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Impossibile elaborare utente: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Elaborati: " + typeof(success_count) + " successi, " + typeof(error_count) + " errori");
}
```

### Esempio: Tipi di Errore Personalizzati

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a deve essere un numero", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b deve essere un numero", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Impossibile dividere per zero", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Dettagli: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Esempio: Logica di Retry

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // Successo!
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operazione fallita dopo " + typeof(max_attempts) + " tentativi: " + e;
            }
            print("Tentativo " + typeof(attempt) + " fallito, riprovo...");
        }
    }
}

fn unreliable_operation() {
    // Operazione inaffidabile simulata
    if (random() < 0.7) {
        throw "Operazione fallita";
    }
    return "Successo";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("Tutti i tentativi falliti: " + e);
}
```

## Ordine di Esecuzione

Comprendere l'ordine di esecuzione:

```hemlock
try {
    print("1: inizio blocco try");
    throw "errore";
    print("2: mai raggiunto");
} catch (e) {
    print("3: blocco catch");
} finally {
    print("4: blocco finally");
}
print("5: dopo try/catch/finally");

// Output:
// 1: inizio blocco try
// 3: blocco catch
// 4: blocco finally
// 5: dopo try/catch/finally
```

## Limitazioni Attuali

- **Nessuno stack trace** - Le eccezioni non catturate non mostrano lo stack trace (pianificato)
- **Alcune funzioni built-in chiamano exit** - Alcune funzioni built-in ancora chiamano `exit()` invece di lanciare (da rivedere)
- **Nessun tipo di eccezione personalizzato** - Qualsiasi valore puo essere lanciato, ma non c'e una gerarchia formale di eccezioni

## Argomenti Correlati

- [Funzioni](functions.md) - Eccezioni e return delle funzioni
- [Flusso di Controllo](control-flow.md) - Come le eccezioni influenzano il flusso di controllo
- [Memoria](memory.md) - Usare finally per la pulizia della memoria

## Vedi Anche

- **Semantica delle Eccezioni**: Vedi la sezione "Error Handling" in CLAUDE.md
- **Panic vs Throw**: Casi d'uso diversi per tipi di errore diversi
- **Garanzia di Finally**: Viene sempre eseguito, anche con return/break/continue
