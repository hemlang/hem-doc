# Argomenti da Riga di Comando in Hemlock

I programmi Hemlock possono accedere agli argomenti da riga di comando tramite un **array `args` built-in** che viene automaticamente popolato all'avvio del programma.

## Indice

- [Panoramica](#panoramica)
- [L'Array args](#larray-args)
- [Proprieta](#proprieta)
- [Pattern di Iterazione](#pattern-di-iterazione)
- [Casi d'Uso Comuni](#casi-duso-comuni)
- [Pattern di Parsing degli Argomenti](#pattern-di-parsing-degli-argomenti)
- [Migliori Pratiche](#migliori-pratiche)
- [Esempi Completi](#esempi-completi)

## Panoramica

L'array `args` fornisce accesso agli argomenti da riga di comando passati al tuo programma Hemlock:

- **Sempre disponibile** - Variabile globale built-in in tutti i programmi Hemlock
- **Nome script incluso** - `args[0]` contiene sempre il percorso/nome dello script
- **Array di stringhe** - Tutti gli argomenti sono stringhe
- **Indicizzato da zero** - Indicizzazione standard degli array (0, 1, 2, ...)

## L'Array args

### Struttura Base

```hemlock
// args[0] e sempre il nome del file script
// args[1] fino a args[n-1] sono gli argomenti effettivi
print(args[0]);        // "script.hml"
print(args.length);    // Numero totale di argomenti (incluso nome script)
```

### Esempio di Utilizzo

**Comando:**
```bash
./hemlock script.hml ciao mondo "test 123"
```

**In script.hml:**
```hemlock
print("Nome script: " + args[0]);     // "script.hml"
print("Totale args: " + typeof(args.length));  // "4"
print("Primo arg: " + args[1]);       // "ciao"
print("Secondo arg: " + args[2]);     // "mondo"
print("Terzo arg: " + args[3]);       // "test 123"
```

### Riferimento Indici

| Indice | Contiene | Valore Esempio |
|--------|----------|----------------|
| `args[0]` | Percorso/nome script | `"script.hml"` o `"./script.hml"` |
| `args[1]` | Primo argomento | `"ciao"` |
| `args[2]` | Secondo argomento | `"mondo"` |
| `args[3]` | Terzo argomento | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Ultimo argomento | (varia) |

## Proprieta

### Sempre Presente

`args` e un array globale disponibile in **tutti** i programmi Hemlock:

```hemlock
// Nessun bisogno di dichiarare o importare
print(args.length);  // Funziona immediatamente
```

### Nome Script Incluso

`args[0]` contiene sempre il percorso/nome dello script:

```hemlock
print("In esecuzione: " + args[0]);
```

**Possibili valori per args[0]:**
- `"script.hml"` - Solo il nome del file
- `"./script.hml"` - Percorso relativo
- `"/home/utente/script.hml"` - Percorso assoluto
- Dipende da come lo script e stato invocato

### Tipo: Array di Stringhe

Tutti gli argomenti sono memorizzati come stringhe:

```hemlock
// Argomenti: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (stringa, non numero)
print(args[2]);  // "3.14" (stringa, non numero)
print(args[3]);  // "true" (stringa, non booleano)

// Converti se necessario:
let num = 42;  // Parsa manualmente se necessario
```

### Lunghezza Minima

Sempre almeno 1 (il nome dello script):

```hemlock
print(args.length);  // Minimo: 1
```

**Anche senza argomenti:**
```bash
./hemlock script.hml
```

```hemlock
// In script.hml:
print(args.length);  // 1 (solo nome script)
```

### Comportamento REPL

Nel REPL, `args.length` e 0 (array vuoto):

```hemlock
# Sessione REPL
> print(args.length);
0
```

## Pattern di Iterazione

### Iterazione Base

Salta `args[0]` (nome script) ed elabora gli argomenti effettivi:

```hemlock
let i = 1;
while (i < args.length) {
    print("Argomento " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**Output per: `./hemlock script.hml pippo pluto paperino`**
```
Argomento 1: pippo
Argomento 2: pluto
Argomento 3: paperino
```

### Iterazione For-In (Incluso Nome Script)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Output:**
```
script.hml
pippo
pluto
paperino
```

### Controllo del Conteggio Argomenti

```hemlock
if (args.length < 2) {
    print("Uso: " + args[0] + " <argomento>");
    // exit o return
} else {
    let arg = args[1];
    // elabora arg
}
```

### Elaborazione di Tutti gli Argomenti Tranne il Nome Script

```hemlock
let args_effettivi = args.slice(1, args.length);

for (let arg in args_effettivi) {
    print("Elaborazione: " + arg);
}
```

## Casi d'Uso Comuni

### 1. Elaborazione Semplice di Argomenti

Controllo per argomento richiesto:

```hemlock
if (args.length < 2) {
    print("Uso: " + args[0] + " <nomefile>");
} else {
    let nomefile = args[1];
    print("Elaborazione file: " + nomefile);
    // ... elabora file
}
```

**Utilizzo:**
```bash
./hemlock script.hml dati.txt
# Output: Elaborazione file: dati.txt
```

### 2. Argomenti Multipli

```hemlock
if (args.length < 3) {
    print("Uso: " + args[0] + " <input> <output>");
} else {
    let file_input = args[1];
    let file_output = args[2];

    print("Input: " + file_input);
    print("Output: " + file_output);

    // Elabora file...
}
```

**Utilizzo:**
```bash
./hemlock converti.hml input.txt output.txt
```

### 3. Numero Variabile di Argomenti

Elabora tutti gli argomenti forniti:

```hemlock
if (args.length < 2) {
    print("Uso: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Elaborazione " + typeof(args.length - 1) + " file:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        elabora_file(args[i]);
        i = i + 1;
    }
}
```

**Utilizzo:**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Messaggio di Aiuto

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Uso: " + args[0] + " [OPZIONI] <file>");
    print("Opzioni:");
    print("  -h, --help     Mostra questo messaggio di aiuto");
    print("  -v, --verbose  Abilita output verboso");
} else {
    // Elabora normalmente
}
```

### 5. Validazione degli Argomenti

```hemlock
fn valida_file(nomefile: string): bool {
    // Controlla se il file esiste (esempio)
    return nomefile != "";
}

if (args.length < 2) {
    print("Errore: Nessun nome file fornito");
} else if (!valida_file(args[1])) {
    print("Errore: File non valido: " + args[1]);
} else {
    print("Elaborazione: " + args[1]);
}
```

## Pattern di Parsing degli Argomenti

### Argomenti con Nome (Flag)

Pattern semplice per argomenti con nome:

```hemlock
let verboso = false;
let file_output = "";
let file_input = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verboso = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            file_output = args[i];
        }
    } else {
        file_input = args[i];
    }
    i = i + 1;
}

if (verboso) {
    print("Modalita verbosa abilitata");
}
print("Input: " + file_input);
print("Output: " + file_output);
```

**Utilizzo:**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Flag Booleani

```hemlock
let debug = false;
let verboso = false;
let forza = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verboso = true;
    } else if (args[i] == "--force") {
        forza = true;
    }
    i = i + 1;
}
```

### Argomenti con Valore

```hemlock
let file_config = "default.conf";
let porta = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            file_config = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            porta = 8080;  // Dovrebbe parsare la stringa in int
        }
    }
    i = i + 1;
}
```

### Argomenti Posizionali e con Nome Misti

```hemlock
let file_input = "";
let file_output = "";
let verboso = false;

let i = 1;
let posizionali = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verboso = true;
    } else {
        // Tratta come argomento posizionale
        posizionali.push(args[i]);
    }
    i = i + 1;
}

// Assegna argomenti posizionali
if (posizionali.length > 0) {
    file_input = posizionali[0];
}
if (posizionali.length > 1) {
    file_output = posizionali[1];
}
```

### Funzione Helper per Parser di Argomenti

```hemlock
fn parsa_args() {
    let opzioni = {
        verboso: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            opzioni.verboso = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                opzioni.output = args[i];
            }
        } else {
            // Argomento posizionale
            opzioni.files.push(arg);
        }

        i = i + 1;
    }

    return opzioni;
}

let opts = parsa_args();
print("Verboso: " + typeof(opts.verboso));
print("Output: " + opts.output);
print("File: " + typeof(opts.files.length));
```

## Migliori Pratiche

### 1. Controllare Sempre il Conteggio degli Argomenti

```hemlock
// Bene
if (args.length < 2) {
    print("Uso: " + args[0] + " <file>");
} else {
    elabora_file(args[1]);
}

// Male - potrebbe crashare se nessun argomento
elabora_file(args[1]);  // Errore se args.length == 1
```

### 2. Fornire Informazioni di Utilizzo

```hemlock
fn mostra_uso() {
    print("Uso: " + args[0] + " [OPZIONI] <file>");
    print("Opzioni:");
    print("  -h, --help     Mostra aiuto");
    print("  -v, --verbose  Output verboso");
}

if (args.length < 2) {
    mostra_uso();
}
```

### 3. Validare gli Argomenti

```hemlock
fn valida_args() {
    if (args.length < 2) {
        print("Errore: Argomento richiesto mancante");
        return false;
    }

    if (args[1] == "") {
        print("Errore: Argomento vuoto");
        return false;
    }

    return true;
}

if (!valida_args()) {
    // exit o mostra uso
}
```

### 4. Usare Nomi di Variabili Descrittivi

```hemlock
// Bene
let nome_file_input = args[1];
let nome_file_output = args[2];
let max_iterazioni = args[3];

// Male
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Gestire Argomenti tra Virgolette con Spazi

La shell gestisce questo automaticamente:

```bash
./hemlock script.hml "file con spazi.txt"
```

```hemlock
print(args[1]);  // "file con spazi.txt"
```

### 6. Creare Oggetti Argomento

```hemlock
fn ottieni_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let argomenti = ottieni_args();
print("Input: " + argomenti.input);
```

## Esempi Completi

### Esempio 1: Elaboratore di File

```hemlock
// Uso: ./hemlock elabora.hml <input> <output>

fn mostra_uso() {
    print("Uso: " + args[0] + " <file_input> <file_output>");
}

if (args.length < 3) {
    mostra_uso();
} else {
    let input = args[1];
    let output = args[2];

    print("Elaborazione " + input + " -> " + output);

    // Elabora file
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let contenuto = f_in.read();
        let elaborato = contenuto.to_upper();  // Elaborazione di esempio
        f_out.write(elaborato);

        print("Fatto!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Esempio 2: Elaboratore Batch di File

```hemlock
// Uso: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Uso: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Elaborazione " + typeof(args.length - 1) + " file:");

    let i = 1;
    while (i < args.length) {
        let nomefile = args[i];
        print("  Elaborazione: " + nomefile);

        try {
            let f = open(nomefile, "r");
            let contenuto = f.read();
            f.close();

            // Elabora contenuto...
            print("    " + typeof(contenuto.length) + " byte");
        } catch (e) {
            print("    Errore: " + e);
        }

        i = i + 1;
    }

    print("Fatto!");
}
```

### Esempio 3: Parser di Argomenti Avanzato

```hemlock
// Uso: ./hemlock app.hml [OPZIONI] <files...>
// Opzioni:
//   --verbose, -v     Abilita output verboso
//   --output, -o FILE Imposta file di output
//   --help, -h        Mostra aiuto

fn parsa_argomenti() {
    let config = {
        verboso: false,
        output: "output.txt",
        aiuto: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verboso = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Errore: --output richiede un valore");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.aiuto = true;
        } else if (arg.starts_with("--")) {
            print("Errore: Opzione sconosciuta: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn mostra_aiuto() {
    print("Uso: " + args[0] + " [OPZIONI] <files...>");
    print("Opzioni:");
    print("  --verbose, -v     Abilita output verboso");
    print("  --output, -o FILE Imposta file di output");
    print("  --help, -h        Mostra questo aiuto");
}

let config = parsa_argomenti();

if (config.aiuto) {
    mostra_aiuto();
} else if (config.files.length == 0) {
    print("Errore: Nessun file di input specificato");
    mostra_aiuto();
} else {
    if (config.verboso) {
        print("Modalita verbosa abilitata");
        print("File di output: " + config.output);
        print("File di input: " + typeof(config.files.length));
    }

    // Elabora file
    for (let file in config.files) {
        if (config.verboso) {
            print("Elaborazione: " + file);
        }
        // ... elabora file
    }
}
```

### Esempio 4: Strumento di Configurazione

```hemlock
// Uso: ./hemlock config.hml <azione> [argomenti]
// Azioni:
//   get <chiave>
//   set <chiave> <valore>
//   list

fn mostra_uso() {
    print("Uso: " + args[0] + " <azione> [argomenti]");
    print("Azioni:");
    print("  get <chiave>         Ottieni valore di configurazione");
    print("  set <chiave> <valore> Imposta valore di configurazione");
    print("  list                 Lista tutta la configurazione");
}

if (args.length < 2) {
    mostra_uso();
} else {
    let azione = args[1];

    if (azione == "get") {
        if (args.length < 3) {
            print("Errore: 'get' richiede una chiave");
        } else {
            let chiave = args[2];
            print("Ottenimento: " + chiave);
            // ... ottieni da config
        }
    } else if (azione == "set") {
        if (args.length < 4) {
            print("Errore: 'set' richiede chiave e valore");
        } else {
            let chiave = args[2];
            let valore = args[3];
            print("Impostazione " + chiave + " = " + valore);
            // ... imposta in config
        }
    } else if (azione == "list") {
        print("Lista di tutta la configurazione:");
        // ... lista config
    } else {
        print("Errore: Azione sconosciuta: " + azione);
        mostra_uso();
    }
}
```

## Riepilogo

Il supporto agli argomenti da riga di comando di Hemlock fornisce:

- Array `args` built-in disponibile globalmente
- Semplice accesso basato su array agli argomenti
- Nome script in `args[0]`
- Tutti gli argomenti come stringhe
- Metodi array disponibili (.length, .slice, ecc.)

Ricorda:
- Controllare sempre `args.length` prima di accedere agli elementi
- `args[0]` e il nome dello script
- Gli argomenti effettivi iniziano da `args[1]`
- Tutti gli argomenti sono stringhe - converti se necessario
- Fornire informazioni di utilizzo per strumenti user-friendly
- Validare gli argomenti prima dell'elaborazione

Pattern comuni:
- Argomenti posizionali semplici
- Argomenti con nome/flag (--flag)
- Argomenti con valore (--opzione valore)
- Messaggi di aiuto (--help)
- Validazione degli argomenti
