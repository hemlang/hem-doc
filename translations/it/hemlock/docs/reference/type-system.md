# Riferimento del Sistema di Tipi

Riferimento completo per il sistema di tipi di Hemlock, inclusi tutti i tipi primitivi e composti.

---

## Panoramica

Hemlock usa un **sistema di tipi dinamico** con tag di tipo a runtime e annotazioni di tipo opzionali. Ogni valore ha un tipo a runtime, e le conversioni di tipo seguono regole di promozione esplicite.

**Caratteristiche Principali:**
- Controllo dei tipi a runtime (interprete)
- Controllo dei tipi a compile-time (hemlockc - abilitato di default)
- Annotazioni di tipo opzionali
- Inferenza di tipo automatica per i letterali
- Regole di promozione dei tipi esplicite
- Nessuna conversione implicita che perde precisione

---

## Controllo dei Tipi a Compile-Time (hemlockc)

Il compilatore Hemlock (`hemlockc`) include un controllo dei tipi a compile-time che valida il codice prima di generare eseguibili. Questo cattura gli errori di tipo in anticipo senza bisogno di eseguire il programma.

### Comportamento Predefinito

Il controllo dei tipi è **abilitato di default** in hemlockc:

```bash
# Il controllo dei tipi avviene automaticamente
hemlockc programma.hml -o programma

# Gli errori sono riportati prima della compilazione
hemlockc tipi_errati.hml
# Output: 1 errore di tipo trovato
```

### Flag del Compilatore

| Flag | Descrizione |
|------|-------------|
| `--check` | Solo controllo tipi, non compila (esce dopo validazione) |
| `--no-type-check` | Disabilita controllo tipi (non raccomandato) |
| `--strict-types` | Abilita avvisi più rigidi sui tipi |

**Esempi:**

```bash
# Solo validare i tipi senza compilare
hemlockc --check programma.hml
# Output: programma.hml: nessun errore di tipo

# Disabilitare controllo tipi (usare con cautela)
hemlockc --no-type-check codice_dinamico.hml -o programma

# Abilitare avvisi rigidi per tipi any impliciti
hemlockc --strict-types programma.hml -o programma
```

### Cosa Valida il Controllo dei Tipi

1. **Annotazioni di tipo** - Assicura che i valori assegnati corrispondano ai tipi dichiarati
2. **Chiamate di funzione** - Valida i tipi degli argomenti rispetto ai tipi dei parametri
3. **Tipi di ritorno** - Verifica che le istruzioni return corrispondano al tipo di ritorno dichiarato
4. **Uso degli operatori** - Verifica che gli operandi siano compatibili
5. **Accesso alle proprietà** - Valida i tipi dei campi degli oggetti per oggetti tipizzati

### Conversioni Numeriche Permissive

Il controllo dei tipi permette conversioni di tipo numerico a compile-time, con validazione dell'intervallo a runtime:

```hemlock
let x: i8 = 100;      // OK - 100 sta in i8 (validato a runtime)
let y: u8 = 255;      // OK - nell'intervallo u8
let z: f64 = 42;      // OK - i32 a f64 è sicuro
```

### Supporto per Codice Dinamico

Il codice senza annotazioni di tipo è trattato come dinamico (tipo `any`) e passa sempre il controllo dei tipi:

```hemlock
let x = get_value();  // Dinamico - nessuna annotazione
process(x);           // OK - valori dinamici accettati ovunque
```

---

## Tipi Primitivi

### Tipi Numerici

#### Interi con Segno

| Tipo   | Dimensione | Intervallo                                   | Alias     |
|--------|------------|----------------------------------------------|-----------|
| `i8`   | 1 byte     | -128 a 127                                   | -         |
| `i16`  | 2 byte     | -32.768 a 32.767                             | -         |
| `i32`  | 4 byte     | -2.147.483.648 a 2.147.483.647               | `integer` |
| `i64`  | 8 byte     | -9.223.372.036.854.775.808 a 9.223.372.036.854.775.807 | - |

**Esempi:**
```hemlock
let a: i8 = 127;
let b: i16 = 32000;
let c: i32 = 1000000;
let d: i64 = 9223372036854775807;

// Alias di tipo
let x: integer = 42;  // Uguale a i32
```

#### Interi senza Segno

| Tipo   | Dimensione | Intervallo                  | Alias  |
|--------|------------|-----------------------------|--------|
| `u8`   | 1 byte     | 0 a 255                     | `byte` |
| `u16`  | 2 byte     | 0 a 65.535                  | -      |
| `u32`  | 4 byte     | 0 a 4.294.967.295           | -      |
| `u64`  | 8 byte     | 0 a 18.446.744.073.709.551.615 | -   |

**Esempi:**
```hemlock
let a: u8 = 255;
let b: u16 = 65535;
let c: u32 = 4294967295;
let d: u64 = 18446744073709551615;

// Alias di tipo
let val_byte: byte = 65;  // Uguale a u8
```

#### Virgola Mobile

| Tipo   | Dimensione | Precisione   | Alias    |
|--------|------------|--------------|----------|
| `f32`  | 4 byte     | ~7 cifre     | -        |
| `f64`  | 8 byte     | ~15 cifre    | `number` |

**Esempi:**
```hemlock
let pi: f32 = 3.14159;
let preciso: f64 = 3.14159265359;

// Alias di tipo
let x: number = 2.718;  // Uguale a f64
```

---

### Inferenza dei Letterali Interi

I letterali interi sono tipizzati automaticamente in base al loro valore:

**Regole:**
- Valori nell'intervallo i32 (-2.147.483.648 a 2.147.483.647): inferiti come `i32`
- Valori fuori dall'intervallo i32 ma nell'intervallo i64: inferiti come `i64`
- Usa annotazioni di tipo esplicite per altri tipi (i8, i16, u8, u16, u32, u64)

**Esempi:**
```hemlock
let piccolo = 42;                    // i32 (sta in i32)
let grande = 5000000000;             // i64 (> max i32)
let max_i64 = 9223372036854775807;   // i64 (INT64_MAX)
let esplicito: u32 = 100;            // u32 (annotazione sovrascrive)
```

---

### Tipo Booleano

**Tipo:** `bool`

**Valori:** `true`, `false`

**Dimensione:** 1 byte (internamente)

**Esempi:**
```hemlock
let attivo: bool = true;
let fatto = false;

if (attivo && !fatto) {
    print("lavorando");
}
```

---

### Tipi Carattere

#### Rune

**Tipo:** `rune`

**Descrizione:** Codepoint Unicode (U+0000 a U+10FFFF)

**Dimensione:** 4 byte (valore 32-bit)

**Intervallo:** 0 a 0x10FFFF (1.114.111)

**Sintassi Letterale:** Apici singoli `'x'`

**Esempi:**
```hemlock
// ASCII
let a = 'A';
let cifra = '0';

// UTF-8 multi-byte
let razzo = '🚀';      // U+1F680
let cuore = '❤';       // U+2764
let cinese = '中';     // U+4E2D

// Sequenze di escape
let newline = '\n';
let tab = '\t';
let backslash = '\\';
let apice = '\'';
let null_char = '\0';

// Escape Unicode
let emoji = '\u{1F680}';   // Fino a 6 cifre hex
let max = '\u{10FFFF}';    // Codepoint massimo
```

**Conversioni di Tipo:**
```hemlock
// Intero a rune
let codice: rune = 65;        // 'A'
let r: rune = 128640;         // 🚀

// Rune a intero
let valore: i32 = 'Z';        // 90

// Rune a stringa
let s: string = 'H';          // "H"

// u8 a rune
let byte_val: u8 = 65;
let rune_val: rune = byte_val;  // 'A'
```

**Vedi Anche:** [API delle Stringhe](string-api.md) per concatenazione stringa + rune

---

### Tipo Stringa

**Tipo:** `string`

**Descrizione:** Testo codificato UTF-8, mutabile, allocato nell'heap

**Codifica:** UTF-8 (U+0000 a U+10FFFF)

**Mutabilità:** Mutabile (diversamente dalla maggior parte dei linguaggi)

**Proprietà:**
- `.length` - Conteggio codepoint (numero di caratteri)
- `.byte_length` - Conteggio byte (dimensione codifica UTF-8)

**Sintassi Letterale:** Virgolette doppie `"testo"`

**Esempi:**
```hemlock
let s = "ciao";
s[0] = 'C';             // Muta (ora "Ciao")
print(s.length);        // 5 (conteggio codepoint)
print(s.byte_length);   // 5 (byte UTF-8)

let emoji = "🚀";
print(emoji.length);        // 1 (un codepoint)
print(emoji.byte_length);   // 4 (quattro byte UTF-8)
```

**Indicizzazione:**
```hemlock
let s = "ciao";
let ch = s[0];          // Restituisce rune 'c'
s[0] = 'C';             // Imposta con rune
```

**Vedi Anche:** [API delle Stringhe](string-api.md) per riferimento completo dei metodi

---

### Tipo Null

**Tipo:** `null`

**Descrizione:** Il valore null (assenza di valore)

**Dimensione:** 8 byte (internamente)

**Valore:** `null`

**Esempi:**
```hemlock
let x = null;
let y: i32 = null;  // ERRORE: mismatch di tipo

if (x == null) {
    print("x è null");
}
```

---

## Tipi Composti

### Tipo Array

**Tipo:** `array`

**Descrizione:** Array dinamico, allocato nell'heap, a tipi misti

**Proprietà:**
- `.length` - Numero di elementi

**Indicizzazione a base zero:** Sì

**Sintassi Letterale:** `[elem1, elem2, ...]`

**Esempi:**
```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Tipi misti
let misto = [1, "ciao", true, null];
```

**Vedi Anche:** [API degli Array](array-api.md) per riferimento completo dei metodi

---

### Tipo Oggetto

**Tipo:** `object`

**Descrizione:** Oggetto stile JavaScript con campi dinamici

**Sintassi Letterale:** `{ campo: valore, ... }`

**Esempi:**
```hemlock
let persona = { nome: "Alice", eta: 30 };
print(persona.nome);  // "Alice"

// Aggiunge campo dinamicamente
persona.email = "alice@esempio.com";
```

**Definizioni di Tipo:**
```hemlock
define Persona {
    nome: string,
    eta: i32,
    attivo?: bool,  // Campo opzionale
}

let p: Persona = { nome: "Bob", eta: 25 };
print(typeof(p));  // "Persona"
```

---

### Tipi Puntatore

#### Puntatore Grezzo (ptr)

**Tipo:** `ptr`

**Descrizione:** Indirizzo di memoria grezzo (non sicuro)

**Dimensione:** 8 byte

**Controllo Limiti:** Nessuno

**Esempi:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

#### Buffer (buffer)

**Tipo:** `buffer`

**Descrizione:** Wrapper sicuro del puntatore con controllo limiti

**Struttura:** Puntatore + lunghezza + capacità

**Proprietà:**
- `.length` - Dimensione buffer
- `.capacity` - Capacità allocata

**Esempi:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Con controllo limiti
print(b.length);        // 64
free(b);
```

**Vedi Anche:** [API della Memoria](memory-api.md) per funzioni di allocazione

---

## Tipi Speciali

### Tipo File

**Tipo:** `file`

**Descrizione:** Handle di file per operazioni di I/O

**Proprietà:**
- `.path` - Percorso del file (string)
- `.mode` - Modalità di apertura (string)
- `.closed` - Se il file è chiuso (bool)

**Vedi Anche:** [API dei File](file-api.md)

---

### Tipo Task

**Tipo:** `task`

**Descrizione:** Handle per task concorrente

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

### Tipo Channel

**Tipo:** `channel`

**Descrizione:** Canale di comunicazione thread-safe

**Vedi Anche:** [API di Concorrenza](concurrency-api.md)

---

### Tipo Funzione

**Tipo:** `function`

**Descrizione:** Valore funzione di prima classe

**Esempi:**
```hemlock
fn somma(a, b) {
    return a + b;
}

let moltiplica = fn(x, y) {
    return x * y;
};

print(typeof(somma));      // "function"
print(typeof(moltiplica)); // "function"
```

---

### Tipo Void

**Tipo:** `void`

**Descrizione:** Assenza di valore di ritorno (uso interno)

---

## Regole di Promozione dei Tipi

Quando si mescolano tipi nelle operazioni, Hemlock promuove al tipo "superiore":

**Gerarchia di Promozione:**
```
f64 (precisione massima)
 ↑
f32
 ↑
u64
 ↑
i64
 ↑
u32
 ↑
i32
 ↑
u16
 ↑
i16
 ↑
u8
 ↑
i8 (minima)
```

**Regole:**
1. Il float vince sempre sull'intero
2. Dimensione maggiore vince nella stessa categoria (int/uint/float)
3. Entrambi gli operandi sono promossi al tipo risultato
4. **Preservazione precisione:** i64/u64 + f32 promuove a f64 (non f32)

**Esempi:**
```hemlock
// Promozione dimensione
u8 + i32    → i32    // Dimensione maggiore vince
i32 + i64   → i64    // Dimensione maggiore vince
u32 + u64   → u64    // Dimensione maggiore vince

// Promozione float
i32 + f32   → f32    // Float vince, f32 sufficiente per i32
i64 + f32   → f64    // Promuove a f64 per preservare precisione i64
i64 + f64   → f64    // Float vince sempre
i8 + f64    → f64    // Float + più grande vince
```

**Perché i64 + f32 → f64?**

f32 ha solo una mantissa di 24 bit, che non può rappresentare precisamente interi
più grandi di 2^24 (16.777.216). Poiché i64 può contenere valori fino a 2^63,
mescolare i64 con f32 causerebbe grave perdita di precisione. Hemlock promuove
a f64 (mantissa 53 bit) invece.

---

## Controllo dell'Intervallo

Le annotazioni di tipo impongono controlli dell'intervallo all'assegnazione:

**Assegnazioni Valide:**
```hemlock
let x: u8 = 255;             // OK
let y: i8 = 127;             // OK
let a: i64 = 2147483647;     // OK
let b: u64 = 4294967295;     // OK
```

**Assegnazioni Non Valide (Errore a Runtime):**
```hemlock
let x: u8 = 256;             // ERRORE: fuori intervallo
let y: i8 = 128;             // ERRORE: max è 127
let z: u64 = -1;             // ERRORE: u64 non può essere negativo
```

---

## Introspezione dei Tipi

### typeof(valore)

Restituisce il nome del tipo come stringa.

**Firma:**
```hemlock
typeof(valore: any): string
```

**Restituisce:**
- Tipi primitivi: `"i8"`, `"i16"`, `"i32"`, `"i64"`, `"u8"`, `"u16"`, `"u32"`, `"u64"`, `"f32"`, `"f64"`, `"bool"`, `"string"`, `"rune"`, `"null"`
- Tipi composti: `"array"`, `"object"`, `"ptr"`, `"buffer"`, `"function"`
- Tipi speciali: `"file"`, `"task"`, `"channel"`
- Oggetti tipizzati: Nome del tipo personalizzato (es. `"Persona"`)

**Esempi:**
```hemlock
print(typeof(42));              // "i32"
print(typeof(3.14));            // "f64"
print(typeof("ciao"));          // "string"
print(typeof('A'));             // "rune"
print(typeof(true));            // "bool"
print(typeof([1, 2, 3]));       // "array"
print(typeof({ x: 10 }));       // "object"

define Persona { nome: string }
let p: Persona = { nome: "Alice" };
print(typeof(p));               // "Persona"
```

**Vedi Anche:** [Funzioni Integrate](builtins.md#typeof)

---

## Conversioni di Tipo

### Conversioni Implicite

Hemlock esegue conversioni di tipo implicite nelle operazioni aritmetiche seguendo le regole di promozione dei tipi.

**Esempi:**
```hemlock
let a: u8 = 10;
let b: i32 = 20;
let risultato = a + b;     // risultato è i32 (promosso)
```

### Conversioni Esplicite

Usa le annotazioni di tipo per conversioni esplicite:

**Esempi:**
```hemlock
// Intero a float
let i: i32 = 42;
let f: f64 = i;         // 42.0

// Float a intero (tronca)
let x: f64 = 3.14;
let y: i32 = x;         // 3

// Intero a rune
let codice: rune = 65;  // 'A'

// Rune a intero
let valore: i32 = 'Z';  // 90

// Rune a stringa
let s: string = 'H';    // "H"
```

---

## Alias di Tipo

### Alias Integrati

Hemlock fornisce alias di tipo integrati per tipi comuni:

| Alias     | Tipo Effettivo | Uso                      |
|-----------|----------------|--------------------------|
| `integer` | `i32`          | Interi generici          |
| `number`  | `f64`          | Float generici           |
| `byte`    | `u8`           | Valori byte              |

**Esempi:**
```hemlock
let conteggio: integer = 100;       // Uguale a i32
let prezzo: number = 19.99;         // Uguale a f64
let b: byte = 255;                  // Uguale a u8
```

### Alias di Tipo Personalizzati

Definisci alias di tipo personalizzati usando la parola chiave `type`:

```hemlock
// Alias semplici
type Intero = i32;
type Testo = string;

// Alias di tipo funzione
type Callback = fn(i32): void;
type Predicato = fn(any): bool;
type OpBinaria = fn(i32, i32): i32;

// Alias di tipo composto
define HaNome { nome: string }
define HaEta { eta: i32 }
type Persona = HaNome & HaEta;

// Alias di tipo generico
type Coppia<T> = { primo: T, secondo: T };
type Risultato<T, E> = { valore: T?, errore: E? };
```

**Usando alias personalizzati:**
```hemlock
let cb: Callback = fn(n) { print(n); };
let p: Persona = { nome: "Alice", eta: 30 };
let coord: Coppia<f64> = { primo: 3.14, secondo: 2.71 };
```

**Nota:** Gli alias di tipo sono trasparenti - `typeof()` restituisce il nome del tipo sottostante.

---

## Tipi Funzione

I tipi funzione specificano la firma dei valori funzione:

### Sintassi

```hemlock
fn(tipi_parametri): tipo_ritorno
```

### Esempi

```hemlock
// Tipo funzione base
let somma: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parametro funzione
fn applica(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Funzione di ordine superiore che restituisce funzione
fn crea_sommatore(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Tipo funzione async
fn esegui_async(handler: async fn(): void) {
    spawn(handler);
}
```

---

## Tipi Composti (Intersezione)

I tipi composti usano `&` per richiedere vincoli di tipo multipli:

```hemlock
define HaNome { nome: string }
define HaEta { eta: i32 }
define HaEmail { email: string }

// L'oggetto deve soddisfare tutti i tipi
let persona: HaNome & HaEta = { nome: "Alice", eta: 30 };

// Tre o più tipi
fn descrivi(p: HaNome & HaEta & HaEmail) {
    print(p.nome + " <" + p.email + ">");
}
```

---

## Tabella Riassuntiva

| Tipo       | Dim.     | Mutabile | Heap   | Descrizione                    |
|------------|----------|----------|--------|--------------------------------|
| `i8`-`i64` | 1-8 byte | No       | No     | Interi con segno               |
| `u8`-`u64` | 1-8 byte | No       | No     | Interi senza segno             |
| `f32`      | 4 byte   | No       | No     | Float singola precisione       |
| `f64`      | 8 byte   | No       | No     | Float doppia precisione        |
| `bool`     | 1 byte   | No       | No     | Booleano                       |
| `rune`     | 4 byte   | No       | No     | Codepoint Unicode              |
| `string`   | Variabile| Sì       | Sì     | Testo UTF-8                    |
| `array`    | Variabile| Sì       | Sì     | Array dinamico                 |
| `object`   | Variabile| Sì       | Sì     | Oggetto dinamico               |
| `ptr`      | 8 byte   | No       | No     | Puntatore grezzo               |
| `buffer`   | Variabile| Sì       | Sì     | Wrapper puntatore sicuro       |
| `file`     | Opaco    | Sì       | Sì     | Handle file                    |
| `task`     | Opaco    | No       | Sì     | Handle task concorrente        |
| `channel`  | Opaco    | Sì       | Sì     | Canale thread-safe             |
| `function` | Opaco    | No       | Sì     | Valore funzione                |
| `null`     | 8 byte   | No       | No     | Valore null                    |

---

## Vedi Anche

- [Riferimento Operatori](operators.md) - Comportamento dei tipi nelle operazioni
- [Funzioni Integrate](builtins.md) - Introspezione e conversione tipi
- [API delle Stringhe](string-api.md) - Metodi del tipo stringa
- [API degli Array](array-api.md) - Metodi del tipo array
- [API della Memoria](memory-api.md) - Operazioni su puntatori e buffer
