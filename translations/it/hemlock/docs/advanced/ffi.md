# FFI (Interfaccia Funzioni Esterne) in Hemlock

Hemlock fornisce **FFI (Foreign Function Interface)** per chiamare funzioni C da librerie condivise usando libffi, consentendo l'integrazione con librerie C esistenti e API di sistema.

## Indice

- [Panoramica](#panoramica)
- [Stato Attuale](#stato-attuale)
- [Tipi Supportati](#tipi-supportati)
- [Concetti Base](#concetti-base)
- [Esportazione di Funzioni FFI](#esportazione-di-funzioni-ffi)
- [Casi d'Uso](#casi-duso)
- [Sviluppi Futuri](#sviluppi-futuri)
- [Callback FFI](#callback-ffi)
- [Struct FFI](#struct-ffi)
- [Esportazione di Tipi Struct](#esportazione-di-tipi-struct)
- [Limitazioni Attuali](#limitazioni-attuali)
- [Migliori Pratiche](#migliori-pratiche)

## Panoramica

L'Interfaccia Funzioni Esterne (FFI) permette ai programmi Hemlock di:
- Chiamare funzioni C da librerie condivise (.so, .dylib, .dll)
- Usare librerie C esistenti senza scrivere codice wrapper
- Accedere direttamente alle API di sistema
- Integrarsi con librerie native di terze parti
- Collegare Hemlock con funzionalita di sistema a basso livello

**Capacita principali:**
- Caricamento dinamico di librerie
- Binding di funzioni C
- Conversione automatica dei tipi tra Hemlock e tipi C
- Supporto per tutti i tipi primitivi
- Implementazione basata su libffi per portabilita

## Stato Attuale

Il supporto FFI e disponibile in Hemlock con le seguenti funzionalita:

**Implementato:**
- Chiamare funzioni C da librerie condivise
- Supporto per tutti i tipi primitivi (interi, float, puntatori)
- Conversione automatica dei tipi
- Implementazione basata su libffi
- Caricamento dinamico di librerie
- **Callback con puntatori a funzione** - Passare funzioni Hemlock a C
- **Esportazione di funzioni extern** - Condividere binding FFI tra moduli
- **Passaggio e restituzione di struct** - Passare struct compatibili con C per valore
- **Helper per puntatori completi** - Lettura/scrittura di tutti i tipi (i8-i64, u8-u64, f32, f64, ptr)
- **Conversione buffer/puntatore** - `buffer_ptr()`, `ptr_to_buffer()`
- **Dimensioni tipi FFI** - `ffi_sizeof()` per dimensioni tipi consapevoli della piattaforma
- **Tipi di piattaforma** - Supporto `size_t`, `usize`, `isize`, `intptr_t`

**In Sviluppo:**
- Helper per marshaling di stringhe
- Miglioramenti nella gestione degli errori

**Copertura Test:**
- Test FFI passati inclusi test callback
- Chiamata funzioni base verificata
- Conversione tipi testata
- Integrazione callback qsort testata

## Tipi Supportati

### Tipi Primitivi

I seguenti tipi Hemlock possono essere passati a/da funzioni C:

| Tipo Hemlock | Tipo C | Dimensione | Note |
|--------------|--------|------------|------|
| `i8` | `int8_t` | 1 byte | Intero con segno a 8 bit |
| `i16` | `int16_t` | 2 byte | Intero con segno a 16 bit |
| `i32` | `int32_t` | 4 byte | Intero con segno a 32 bit |
| `i64` | `int64_t` | 8 byte | Intero con segno a 64 bit |
| `u8` | `uint8_t` | 1 byte | Intero senza segno a 8 bit |
| `u16` | `uint16_t` | 2 byte | Intero senza segno a 16 bit |
| `u32` | `uint32_t` | 4 byte | Intero senza segno a 32 bit |
| `u64` | `uint64_t` | 8 byte | Intero senza segno a 64 bit |
| `f32` | `float` | 4 byte | Virgola mobile a 32 bit |
| `f64` | `double` | 8 byte | Virgola mobile a 64 bit |
| `ptr` | `void*` | 8 byte | Puntatore raw |

### Conversione dei Tipi

**Conversioni automatiche:**
- Interi Hemlock -> Interi C (con controllo range)
- Float Hemlock -> Float C
- Puntatori Hemlock -> Puntatori C
- Valori di ritorno C -> Valori Hemlock

**Esempio di mappatura tipi:**
```hemlock
// Hemlock -> C
let i: i32 = 42;         // -> int32_t (4 byte)
let f: f64 = 3.14;       // -> double (8 byte)
let p: ptr = alloc(64);  // -> void* (8 byte)

// C -> Hemlock (valori di ritorno)
// int32_t foo() -> i32
// double bar() -> f64
// void* baz() -> ptr
```

## Concetti Base

### Librerie Condivise

FFI funziona con librerie condivise compilate:

**Linux:** file `.so`
```
libexample.so
/usr/lib/libm.so
```

**macOS:** file `.dylib`
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** file `.dll`
```
example.dll
kernel32.dll
```

### Firme delle Funzioni

Le funzioni C devono avere firme note perche FFI funzioni correttamente:

```c
// Esempi di firme funzioni C
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

Queste possono essere chiamate da Hemlock una volta che la libreria e caricata e le funzioni sono legate.

### Compatibilita di Piattaforma

FFI usa **libffi** per la portabilita:
- Funziona su x86, x86-64, ARM, ARM64
- Gestisce automaticamente le convenzioni di chiamata
- Astrae i dettagli ABI specifici della piattaforma
- Supporta Linux, macOS, Windows (con libffi appropriato)

## Esportazione di Funzioni FFI

Le funzioni FFI dichiarate con `extern fn` possono essere esportate dai moduli, permettendo di creare wrapper di librerie riutilizzabili che possono essere condivisi tra piu file.

### Sintassi di Esportazione Base

```hemlock
// string_utils.hml - Un modulo libreria che wrappa funzioni stringa C
import "libc.so.6";

// Esporta direttamente la funzione extern
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// Puoi anche esportare funzioni wrapper insieme a funzioni extern
export fn lunghezza_stringa(s: string): i32 {
    return strlen(s);
}

export fn stringhe_uguali(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### Importazione di Funzioni FFI Esportate

```hemlock
// main.hml - Uso delle funzioni FFI esportate
import { strlen, lunghezza_stringa, stringhe_uguali } from "./string_utils.hml";

let msg = "Ciao, Mondo!";
print(strlen(msg));              // 12 - chiamata extern diretta
print(lunghezza_stringa(msg));   // 12 - funzione wrapper

print(stringhe_uguali("pippo", "pippo"));  // true
print(stringhe_uguali("pippo", "pluto"));  // false
```

### Casi d'Uso per Export Extern

**1. Astrazione di Piattaforma**
```hemlock
// platform.hml - Astrae differenze di piattaforma
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. Wrapper di Librerie**
```hemlock
// crypto_lib.hml - Wrappa funzioni libreria crypto
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Aggiungi wrapper Hemlock-friendly
export fn sha256_stringa(s: string): string {
    // Implementazione usando la funzione extern
}
```

**3. Dichiarazioni FFI Centralizzate**
```hemlock
// libc.hml - Modulo centrale per binding libc
import "libc.so.6";

// Funzioni stringa
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// Funzioni memoria
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// Funzioni processo
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

Poi usalo in tutto il progetto:
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

### Combinare con Esportazioni Regolari

Puoi mischiare funzioni extern esportate con esportazioni di funzioni regolari:

```hemlock
// math_extended.hml
import "libm.so.6";

// Esporta funzioni C raw
export extern fn sin(x: f64): f64;
export extern fn cos(x: f64): f64;
export extern fn tan(x: f64): f64;

// Esporta funzioni Hemlock che le usano
export fn gradi_a_radianti(gradi: f64): f64 {
    return gradi * 3.14159265359 / 180.0;
}

export fn sin_gradi(gradi: f64): f64 {
    return sin(gradi_a_radianti(gradi));
}
```

### Librerie Specifiche per Piattaforma

Quando esporti funzioni extern, ricorda che i nomi delle librerie differiscono per piattaforma:

```hemlock
// Per Linux
import "libc.so.6";

// Per macOS (approccio diverso necessario)
import "libSystem.B.dylib";
```

Attualmente, la sintassi `import "libreria"` di Hemlock usa percorsi di libreria statici, quindi potrebbero essere necessari moduli specifici per piattaforma per codice FFI cross-platform.

## Casi d'Uso

### 1. Librerie di Sistema

Accedi alle funzioni della libreria C standard:

**Funzioni matematiche:**
```hemlock
// Chiama sqrt da libm
let risultato = sqrt(16.0);  // 4.0
```

**Allocazione memoria:**
```hemlock
// Chiama malloc/free da libc
let ptr = malloc(1024);
free(ptr);
```

### 2. Librerie di Terze Parti

Usa librerie C esistenti:

**Esempio: Elaborazione immagini**
```hemlock
// Carica libpng o libjpeg
// Elabora immagini usando funzioni libreria C
```

**Esempio: Crittografia**
```hemlock
// Usa OpenSSL o libsodium
// Crittografia/decrittografia tramite FFI
```

### 3. API di Sistema

Chiamate di sistema dirette:

**Esempio: API POSIX**
```hemlock
// Chiama getpid, getuid, ecc.
// Accedi a funzionalita di sistema a basso livello
```

### 4. Codice Critico per le Prestazioni

Chiama implementazioni C ottimizzate:

```hemlock
// Usa librerie C altamente ottimizzate
// Operazioni SIMD, codice vettorizzato
// Funzioni accelerate hardware
```

### 5. Accesso Hardware

Interfaccia con librerie hardware:

```hemlock
// Controllo GPIO su sistemi embedded
// Comunicazione dispositivi USB
// Accesso porta seriale
```

### 6. Integrazione Codice Legacy

Riusa codebase C esistenti:

```hemlock
// Chiama funzioni da applicazioni C legacy
// Migra gradualmente a Hemlock
// Preserva codice C funzionante
```

## Sviluppi Futuri

### Funzionalita Pianificate

**1. Supporto Struct**
```hemlock
// Futuro: Passa/restituisci struct C
define Punto {
    x: f64,
    y: f64,
}

let p = Punto { x: 1.0, y: 2.0 };
funzione_c_con_struct(p);
```

**2. Gestione Array/Buffer**
```hemlock
// Futuro: Migliore passaggio array
let arr = [1, 2, 3, 4, 5];
elabora_array(arr);  // Passa a funzione C
```

**3. Callback con Puntatori a Funzione** (Implementato!)
```hemlock
// Passa funzioni Hemlock a C come callback
fn mio_confronto(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    return va - vb;
}

// Crea un puntatore a funzione chiamabile da C
let cmp = callback(mio_confronto, ["ptr", "ptr"], "i32");

// Usa con qsort o qualsiasi funzione C che si aspetta un callback
qsort(arr, conteggio, dim_elem, cmp);

// Pulisci quando finito
callback_free(cmp);
```

**4. Marshaling Stringhe**
```hemlock
// Futuro: Conversione automatica stringhe
let s = "ciao";
funzione_stringa_c(s);  // Auto-converti in stringa C
```

**5. Gestione Errori**
```hemlock
// Futuro: Migliore reporting errori
try {
    let risultato = funzione_c_rischiosa();
} catch (e) {
    print("Errore FFI: " + e);
}
```

**6. Type Safety**
```hemlock
// Futuro: Annotazioni di tipo per FFI
@ffi("libm.so")
fn sqrt(x: f64): f64;

let risultato = sqrt(16.0);  // Type-checked
```

### Funzionalita

**v1.0:**
- FFI base con tipi primitivi
- Caricamento dinamico librerie
- Chiamata funzioni
- Supporto callback tramite closure libffi

**Futuro:**
- Supporto struct
- Miglioramenti gestione array
- Generazione automatica binding

## Callback FFI

Hemlock supporta il passaggio di funzioni a codice C come callback usando closure libffi. Questo abilita l'integrazione con API C che si aspettano puntatori a funzione, come `qsort`, event loop e librerie basate su callback.

### Creazione di Callback

Usa `callback()` per creare un puntatore a funzione chiamabile da C da una funzione Hemlock:

```hemlock
// callback(funzione, tipi_param, tipo_ritorno) -> ptr
let cb = callback(mia_funzione, ["ptr", "ptr"], "i32");
```

**Parametri:**
- `funzione`: Una funzione Hemlock da wrappare
- `tipi_param`: Array di stringhe nomi tipo (es. `["ptr", "i32"]`)
- `tipo_ritorno`: Stringa tipo ritorno (es. `"i32"`, `"void"`)

**Tipi callback supportati:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Interi con segno
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Interi senza segno
- `"f32"`, `"f64"` - Virgola mobile
- `"ptr"` - Puntatore
- `"void"` - Nessun valore di ritorno
- `"bool"` - Booleano

### Esempio: qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// Funzione di confronto per interi (ordine crescente)
fn confronta_interi(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// Alloca array di 5 interi
let arr = alloc(20);  // 5 * 4 byte
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// Crea callback e ordina
let cmp = callback(confronta_interi, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// L'array e ora ordinato: [1, 2, 5, 8, 9]

// Pulisci
callback_free(cmp);
free(arr);
```

### Funzioni Helper per Puntatori

Hemlock fornisce funzioni helper complete per lavorare con puntatori raw. Queste sono essenziali per callback FFI e manipolazione diretta della memoria.

#### Helper per Tipi Interi

| Funzione | Descrizione |
|----------|-------------|
| `ptr_deref_i8(ptr)` | Dereferenzia puntatore, leggi i8 |
| `ptr_deref_i16(ptr)` | Dereferenzia puntatore, leggi i16 |
| `ptr_deref_i32(ptr)` | Dereferenzia puntatore, leggi i32 |
| `ptr_deref_i64(ptr)` | Dereferenzia puntatore, leggi i64 |
| `ptr_deref_u8(ptr)` | Dereferenzia puntatore, leggi u8 |
| `ptr_deref_u16(ptr)` | Dereferenzia puntatore, leggi u16 |
| `ptr_deref_u32(ptr)` | Dereferenzia puntatore, leggi u32 |
| `ptr_deref_u64(ptr)` | Dereferenzia puntatore, leggi u64 |
| `ptr_write_i8(ptr, valore)` | Scrivi i8 nella locazione puntatore |
| `ptr_write_i16(ptr, valore)` | Scrivi i16 nella locazione puntatore |
| `ptr_write_i32(ptr, valore)` | Scrivi i32 nella locazione puntatore |
| `ptr_write_i64(ptr, valore)` | Scrivi i64 nella locazione puntatore |
| `ptr_write_u8(ptr, valore)` | Scrivi u8 nella locazione puntatore |
| `ptr_write_u16(ptr, valore)` | Scrivi u16 nella locazione puntatore |
| `ptr_write_u32(ptr, valore)` | Scrivi u32 nella locazione puntatore |
| `ptr_write_u64(ptr, valore)` | Scrivi u64 nella locazione puntatore |

#### Helper per Tipi Float

| Funzione | Descrizione |
|----------|-------------|
| `ptr_deref_f32(ptr)` | Dereferenzia puntatore, leggi f32 (float) |
| `ptr_deref_f64(ptr)` | Dereferenzia puntatore, leggi f64 (double) |
| `ptr_write_f32(ptr, valore)` | Scrivi f32 nella locazione puntatore |
| `ptr_write_f64(ptr, valore)` | Scrivi f64 nella locazione puntatore |

#### Helper per Tipi Puntatore

| Funzione | Descrizione |
|----------|-------------|
| `ptr_deref_ptr(ptr)` | Dereferenzia puntatore-a-puntatore |
| `ptr_write_ptr(ptr, valore)` | Scrivi puntatore nella locazione puntatore |
| `ptr_offset(ptr, indice, dimensione)` | Calcola offset: `ptr + indice * dimensione` |
| `ptr_read_i32(ptr)` | Leggi i32 attraverso puntatore-a-puntatore (per callback qsort) |
| `ptr_null()` | Ottieni costante puntatore null |

#### Helper Conversione Buffer

| Funzione | Descrizione |
|----------|-------------|
| `buffer_ptr(buffer)` | Ottieni puntatore raw da un buffer |
| `ptr_to_buffer(ptr, dimensione)` | Copia dati da puntatore in un nuovo buffer |

#### Funzioni Utilita FFI

| Funzione | Descrizione |
|----------|-------------|
| `ffi_sizeof(nome_tipo)` | Ottieni dimensione in byte di un tipo FFI |

**Nomi tipo supportati per `ffi_sizeof`:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Interi con segno (1, 2, 4, 8 byte)
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Interi senza segno (1, 2, 4, 8 byte)
- `"f32"`, `"f64"` - Float (4, 8 byte)
- `"ptr"` - Puntatore (8 byte su 64 bit)
- `"size_t"`, `"usize"` - Tipo dimensione dipendente dalla piattaforma
- `"intptr_t"`, `"isize"` - Tipo puntatore con segno dipendente dalla piattaforma

#### Esempio: Lavorare con Tipi Diversi

```hemlock
let p = alloc(64);

// Scrivi e leggi interi
ptr_write_i8(p, 42);
print(ptr_deref_i8(p));  // 42

ptr_write_i64(ptr_offset(p, 1, 8), 9000000000);
print(ptr_deref_i64(ptr_offset(p, 1, 8)));  // 9000000000

// Scrivi e leggi float
ptr_write_f64(p, 3.14159);
print(ptr_deref_f64(p));  // 3.14159

// Puntatore-a-puntatore
let interno = alloc(4);
ptr_write_i32(interno, 999);
ptr_write_ptr(p, interno);
let recuperato = ptr_deref_ptr(p);
print(ptr_deref_i32(recuperato));  // 999

// Ottieni dimensioni tipi
print(ffi_sizeof("i64"));  // 8
print(ffi_sizeof("ptr"));  // 8 (su 64 bit)

// Conversione buffer
let buf = buffer(64);
ptr_write_i32(buffer_ptr(buf), 12345);
print(ptr_deref_i32(buffer_ptr(buf)));  // 12345

free(interno);
free(p);
```

### Liberazione dei Callback

**Importante:** Liberare sempre i callback quando finito per prevenire memory leak:

```hemlock
let cb = callback(mia_fn, ["ptr"], "void");
// ... usa callback ...
callback_free(cb);  // Libera quando finito
```

I callback vengono anche automaticamente liberati quando il programma termina.

### Closure nei Callback

I callback catturano il loro ambiente closure, quindi possono accedere a variabili dello scope esterno:

```hemlock
let moltiplicatore = 10;

fn scala(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // Puo accedere a 'moltiplicatore' dallo scope esterno
    return (va * moltiplicatore) - (vb * moltiplicatore);
}

let cmp = callback(scala, ["ptr", "ptr"], "i32");
```

### Thread Safety

Le invocazioni callback sono serializzate con un mutex per garantire thread safety, poiche l'interprete Hemlock non e completamente thread-safe. Questo significa:
- Solo un callback puo essere eseguito alla volta
- Sicuro da usare con librerie C multi-thread
- Potrebbe impattare le prestazioni se i callback vengono chiamati molto frequentemente da piu thread

### Gestione Errori nei Callback

Le eccezioni lanciate nei callback non possono propagarsi al codice C. Invece:
- Un avviso viene stampato su stderr
- Il callback restituisce un valore predefinito (0 o NULL)
- L'eccezione viene loggata ma non propagata

```hemlock
fn callback_rischioso(a: ptr): i32 {
    throw "Qualcosa e andato storto";  // Avviso stampato, restituisce 0
}
```

Per gestione errori robusta, valida gli input ed evita di lanciare eccezioni nei callback.

## Struct FFI

Hemlock supporta il passaggio di struct per valore a funzioni C. I tipi struct vengono automaticamente registrati per FFI quando li definisci con annotazioni di tipo.

### Definizione di Struct Compatibili con FFI

Una struct e compatibile con FFI quando tutti i campi hanno annotazioni di tipo esplicite usando tipi compatibili con FFI:

```hemlock
// Struct compatibile con FFI
define Punto {
    x: f64,
    y: f64,
}

// Struct compatibile con FFI con piu tipi di campo
define Rettangolo {
    in_alto_sinistra: Punto,      // Struct annidata
    larghezza: f64,
    altezza: f64,
}

// NON compatibile con FFI (campo senza annotazione di tipo)
define OggettoDinamico {
    nome,                 // Nessun tipo - non usabile in FFI
    valore,
}
```

### Uso di Struct in FFI

Dichiara funzioni extern che usano tipi struct:

```hemlock
// Definisci il tipo struct
define Vettore2D {
    x: f64,
    y: f64,
}

// Importa la libreria C
import "libmath.so";

// Dichiara funzione extern che prende/restituisce struct
extern fn vettore_somma(a: Vettore2D, b: Vettore2D): Vettore2D;
extern fn vettore_lunghezza(v: Vettore2D): f64;

// Usala naturalmente
let a: Vettore2D = { x: 3.0, y: 0.0 };
let b: Vettore2D = { x: 0.0, y: 4.0 };
let risultato = vettore_somma(a, b);
print(risultato.x);  // 3.0
print(risultato.y);  // 4.0

let lun = vettore_lunghezza(risultato);
print(lun);          // 5.0
```

### Tipi di Campo Supportati

I campi struct devono usare questi tipi compatibili con FFI:

| Tipo Hemlock | Tipo C | Dimensione |
|--------------|--------|------------|
| `i8` | `int8_t` | 1 byte |
| `i16` | `int16_t` | 2 byte |
| `i32` | `int32_t` | 4 byte |
| `i64` | `int64_t` | 8 byte |
| `u8` | `uint8_t` | 1 byte |
| `u16` | `uint16_t` | 2 byte |
| `u32` | `uint32_t` | 4 byte |
| `u64` | `uint64_t` | 8 byte |
| `f32` | `float` | 4 byte |
| `f64` | `double` | 8 byte |
| `ptr` | `void*` | 8 byte |
| `string` | `char*` | 8 byte |
| `bool` | `int` | varia |
| Struct annidata | struct | varia |

### Layout Struct

Hemlock usa le regole di layout struct native della piattaforma (corrispondente all'ABI C):
- I campi sono allineati secondo il loro tipo
- Padding inserito se necessario
- Dimensione totale con padding per allineare il membro piu grande

```hemlock
// Esempio: layout compatibile con C
define Misto {
    a: i8,    // offset 0, dimensione 1
              // 3 byte padding
    b: i32,   // offset 4, dimensione 4
}
// Dimensione totale: 8 byte (con padding)

define Punto3D {
    x: f64,   // offset 0, dimensione 8
    y: f64,   // offset 8, dimensione 8
    z: f64,   // offset 16, dimensione 8
}
// Dimensione totale: 24 byte (nessun padding necessario)
```

### Struct Annidate

Le struct possono contenere altre struct:

```hemlock
define Interno {
    x: i32,
    y: i32,
}

define Esterno {
    interno: Interno,
    z: i32,
}

import "mialibrary.so";
extern fn elabora_annidata(data: Esterno): i32;

let obj: Esterno = {
    interno: { x: 1, y: 2 },
    z: 3,
};
let risultato = elabora_annidata(obj);
```

### Valori di Ritorno Struct

Le funzioni C possono restituire struct:

```hemlock
define Punto {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn ottieni_origine(): Punto;

let p = ottieni_origine();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### Limitazioni

- **I campi struct devono avere annotazioni di tipo** - campi senza tipo non sono compatibili con FFI
- **Nessun array nelle struct** - usa puntatori invece
- **Nessuna union** - solo tipi struct sono supportati
- **I callback non possono restituire struct** - usa puntatori per valori di ritorno callback

### Esportazione di Tipi Struct

Puoi esportare definizioni di tipi struct da un modulo usando `export define`:

```hemlock
// geometria.hml
export define Vettore2 {
    x: f32,
    y: f32,
}

export define Rettangolo {
    x: f32,
    y: f32,
    larghezza: f32,
    altezza: f32,
}

export fn crea_rett(x: f32, y: f32, l: f32, a: f32): Rettangolo {
    return { x: x, y: y, larghezza: l, altezza: a };
}
```

**Importante:** I tipi struct esportati sono registrati **globalmente** quando il modulo viene caricato. Diventano disponibili automaticamente quando importi qualcosa dal modulo. NON devi (e non puoi) importarli esplicitamente per nome:

```hemlock
// main.hml

// BENE - i tipi struct sono auto-disponibili dopo qualsiasi import dal modulo
import { crea_rett } from "./geometria.hml";
let v: Vettore2 = { x: 1.0, y: 2.0 };      // Funziona - Vettore2 e globalmente disponibile
let r: Rettangolo = crea_rett(0.0, 0.0, 100.0, 50.0);  // Funziona

// MALE - non puoi importare esplicitamente tipi struct per nome
import { Vettore2 } from "./geometria.hml";  // Errore: Variabile 'Vettore2' non definita
```

Questo comportamento esiste perche i tipi struct sono registrati nel registro tipi globale quando il modulo viene caricato, piuttosto che essere memorizzati come valori nell'ambiente export del modulo. Il tipo diventa disponibile a tutto il codice che importa dal modulo.

## Limitazioni Attuali

FFI ha le seguenti limitazioni:

**1. Conversione Tipi Manuale**
- Devi gestire manualmente le conversioni stringa
- Nessuna conversione automatica stringa Hemlock <-> stringa C

**2. Gestione Errori Limitata**
- Reporting errori base
- Le eccezioni nei callback non possono propagarsi a C

**3. Caricamento Librerie Manuale**
- Devi caricare manualmente le librerie
- Nessuna generazione automatica di binding

**4. Codice Specifico per Piattaforma**
- I percorsi delle librerie differiscono per piattaforma
- Devi gestire .so vs .dylib vs .dll

## Migliori Pratiche

Mentre la documentazione FFI completa e ancora in sviluppo, ecco le migliori pratiche generali:

### 1. Type Safety

```hemlock
// Sii esplicito sui tipi
let x: i32 = 42;
let risultato: f64 = funzione_c(x);
```

### 2. Gestione Memoria

```hemlock
// Ricorda di liberare la memoria allocata
let ptr = c_malloc(1024);
// ... usa ptr
c_free(ptr);
```

### 3. Controllo Errori

```hemlock
// Controlla i valori di ritorno
let risultato = funzione_c();
if (risultato == null) {
    print("Funzione C fallita");
}
```

### 4. Compatibilita di Piattaforma

```hemlock
// Gestisci differenze di piattaforma
// Usa estensioni libreria appropriate (.so, .dylib, .dll)
```

## Esempi

Per esempi funzionanti, riferisciti a:
- Test callback: `/tests/ffi_callbacks/` - esempi callback qsort
- Uso FFI stdlib: `/stdlib/hash.hml`, `/stdlib/regex.hml`, `/stdlib/crypto.hml`
- Programmi esempio: `/examples/` (se disponibili)

## Ottenere Aiuto

FFI e una funzionalita piu recente in Hemlock. Per domande o problemi:

1. Controlla la suite di test per esempi funzionanti
2. Riferisciti alla documentazione libffi per dettagli di basso livello
3. Segnala bug o richiedi funzionalita tramite le issue del progetto

## Riepilogo

L'FFI di Hemlock fornisce:

- Chiamata funzioni C da librerie condivise
- Supporto tipi primitivi (i8-i64, u8-u64, f32, f64, ptr)
- Conversione automatica dei tipi
- Portabilita basata su libffi
- Base per integrazione librerie native
- **Callback con puntatori a funzione** - passa funzioni Hemlock a C
- **Esportazione funzioni extern** - condividi binding FFI tra moduli
- **Passaggio e ritorno struct** - passa struct compatibili C per valore
- **Export define** - condividi definizioni tipi struct tra moduli (auto-importati globalmente)
- **Helper puntatori completi** - lettura/scrittura tutti i tipi (i8-i64, u8-u64, f32, f64, ptr)
- **Conversione buffer/puntatore** - `buffer_ptr()`, `ptr_to_buffer()` per marshaling dati
- **Dimensioni tipi FFI** - `ffi_sizeof()` per dimensioni tipi consapevoli della piattaforma
- **Tipi piattaforma** - supporto `size_t`, `usize`, `isize`, `intptr_t`, `uintptr_t`

**Stato attuale:** FFI completamente funzionale con tipi primitivi, struct, callback, esportazioni modulo e funzioni helper puntatori complete

**Futuro:** Helper marshaling stringhe

**Casi d'uso:** Librerie di sistema, librerie terze parti, qsort, event loop, API basate su callback, wrapper librerie riutilizzabili

## Contribuire

La documentazione FFI e in espansione. Se lavori con FFI:
- Documenta i tuoi casi d'uso
- Condividi codice esempio
- Segnala problemi o limitazioni
- Suggerisci miglioramenti

Il sistema FFI e progettato per essere pratico e sicuro fornendo accesso a basso livello quando necessario, seguendo la filosofia di Hemlock di "esplicito piuttosto che implicito" e "unsafe e una funzionalita, non un bug."
