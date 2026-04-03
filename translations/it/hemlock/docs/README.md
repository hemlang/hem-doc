# Documentazione di Hemlock

Benvenuto nella documentazione del linguaggio di programmazione Hemlock!

> Un piccolo linguaggio non sicuro per scrivere cose non sicure in modo sicuro.

## Indice

### Per Iniziare
- [Installazione](getting-started/installation.md) - Compilare e installare Hemlock
- [Avvio Rapido](getting-started/quick-start.md) - Il tuo primo programma Hemlock
- [Tutorial](getting-started/tutorial.md) - Guida passo-passo alle basi di Hemlock
- [Percorsi di Apprendimento](getting-started/learning-paths.md) - Scegli il tuo percorso di apprendimento in base ai tuoi obiettivi

### Nuovo alla Programmazione?
- [Glossario](glossary.md) - Definizioni in linguaggio semplice dei termini di programmazione

### Guida al Linguaggio
- [Panoramica della Sintassi](language-guide/syntax.md) - Sintassi e struttura di base
- [Sistema di Tipi](language-guide/types.md) - Tipi primitivi, inferenza dei tipi e conversioni
- [Gestione della Memoria](language-guide/memory.md) - Puntatori, buffer e memoria manuale
- [Stringhe](language-guide/strings.md) - Stringhe UTF-8 e operazioni
- [Rune](language-guide/runes.md) - Codepoint Unicode e gestione dei caratteri
- [Flusso di Controllo](language-guide/control-flow.md) - if/else, cicli, switch e operatori
- [Funzioni](language-guide/functions.md) - Funzioni, closure e ricorsione
- [Oggetti](language-guide/objects.md) - Letterali oggetto, metodi e duck typing
- [Array](language-guide/arrays.md) - Array dinamici e operazioni
- [Gestione degli Errori](language-guide/error-handling.md) - try/catch/finally/throw/panic
- [Moduli](language-guide/modules.md) - Sistema import/export e importazioni di pacchetti

### Argomenti Avanzati
- [WebAssembly (WASM)](getting-started/installation.md#webassembly-wasm-build) - Eseguire Hemlock nel browser tramite Emscripten
- [Async e Concorrenza](advanced/async-concurrency.md) - Vero multi-threading con async/await
- [Bundling e Pacchettizzazione](advanced/bundling-packaging.md) - Creare bundle ed eseguibili standalone
- [Interfaccia Funzioni Esterne](advanced/ffi.md) - Chiamare funzioni C da librerie condivise
- [I/O su File](advanced/file-io.md) - Operazioni sui file e gestione delle risorse
- [Gestione dei Segnali](advanced/signals.md) - Gestione segnali POSIX
- [Argomenti da Riga di Comando](advanced/command-line-args.md) - Accesso agli argomenti del programma
- [Esecuzione di Comandi](advanced/command-execution.md) - Esecuzione di comandi shell
- [Profilazione](advanced/profiling.md) - Tempo CPU, tracciamento memoria e rilevamento leak

### Riferimento API
- [Riferimento Sistema di Tipi](reference/type-system.md) - Riferimento completo dei tipi
- [Riferimento Operatori](reference/operators.md) - Tutti gli operatori e la precedenza
- [Funzioni Integrate](reference/builtins.md) - Funzioni globali e costanti
- [API delle Stringhe](reference/string-api.md) - Metodi e proprietà delle stringhe
- [API degli Array](reference/array-api.md) - Metodi e proprietà degli array
- [API della Memoria](reference/memory-api.md) - Allocazione e manipolazione della memoria
- [API dei File](reference/file-api.md) - Metodi I/O su file
- [API di Concorrenza](reference/concurrency-api.md) - Task e canali

### Design e Filosofia
- [Filosofia di Design](design/philosophy.md) - Principi e obiettivi fondamentali
- [Dettagli di Implementazione](design/implementation.md) - Come funziona Hemlock internamente

### Contribuire
- [Linee Guida per i Contributi](contributing/guidelines.md) - Come contribuire
- [Guida ai Test](contributing/testing.md) - Scrivere ed eseguire test

## Riferimento Rapido

### Hello World
```hemlock
print("Hello, World!");
```

### Tipi Base
```hemlock
let x: i32 = 42;           // 32-bit signed integer
let y: u8 = 255;           // 8-bit unsigned integer
let pi: f64 = 3.14159;     // 64-bit float
let name: string = "Alice"; // UTF-8 string
let flag: bool = true;     // Boolean
let ch: rune = '🚀';       // Unicode codepoint
```

### Gestione della Memoria
```hemlock
// Buffer sicuro (raccomandato)
let buf = buffer(64);
buf[0] = 65;
free(buf);

// Puntatore raw (per esperti)
let ptr = alloc(64);
memset(ptr, 0, 64);
free(ptr);
```

### Async/Concorrenza
```hemlock
async fn compute(n: i32): i32 {
    return n * n;
}

let task = spawn(compute, 42);
let result = join(task);  // 1764
```

## Filosofia

Hemlock e **esplicito piuttosto che implicito**, sempre:
- Il punto e virgola e obbligatorio
- Gestione manuale della memoria (nessun GC)
- Annotazioni di tipo opzionali con controlli a runtime
- Le operazioni non sicure sono permesse (responsabilita tua)

Ti diamo gli strumenti per essere sicuro (`buffer`, annotazioni di tipo, controllo dei limiti) ma non ti obblighiamo a usarli (`ptr`, memoria manuale, operazioni non sicure).

## Ottenere Aiuto

- **Codice Sorgente**: [Repository GitHub](https://github.com/hemlang/hemlock)
- **Gestore Pacchetti**: [hpm](https://github.com/hemlang/hpm) - Hemlock Package Manager
- **Segnalazioni**: Segnala bug e richiedi funzionalita
- **Esempi**: Vedi la directory `examples/`
- **Test**: Vedi la directory `tests/` per esempi di utilizzo

## Licenza

Hemlock e rilasciato sotto la Licenza MIT.
