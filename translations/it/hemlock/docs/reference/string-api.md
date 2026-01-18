# Riferimento API delle Stringhe

Riferimento completo per il tipo stringa di Hemlock e tutti i suoi 19 metodi.

---

## Panoramica

Le stringhe in Hemlock sono sequenze **codificate in UTF-8, mutabili, allocate nell'heap** con supporto completo Unicode. Tutte le operazioni lavorano con **codepoint** (caratteri), non byte.

**Caratteristiche Principali:**
- Codifica UTF-8 (U+0000 a U+10FFFF)
- Mutabili (possono modificare i caratteri in loco)
- Indicizzazione basata sui codepoint
- 19 metodi integrati
- Concatenazione automatica con operatore `+`

---

## Tipo Stringa

**Tipo:** `string`

**Proprietà:**
- `.length` - Numero di codepoint (caratteri)
- `.byte_length` - Numero di byte UTF-8

**Sintassi Letterale:** Virgolette doppie `"testo"`

**Esempi:**
```hemlock
let s = "ciao";
print(s.length);        // 5 (codepoint)
print(s.byte_length);   // 5 (byte)

let emoji = "🚀";
print(emoji.length);        // 1 (un codepoint)
print(emoji.byte_length);   // 4 (quattro byte UTF-8)
```

---

## Indicizzazione

Le stringhe supportano l'indicizzazione basata sui codepoint usando `[]`:

**Accesso in Lettura:**
```hemlock
let s = "ciao";
let ch = s[0];          // Restituisce rune 'c'
```

**Accesso in Scrittura:**
```hemlock
let s = "ciao";
s[0] = 'C';             // Muta con rune (ora "Ciao")
```

**Esempio UTF-8:**
```hemlock
let testo = "Hi🚀!";
print(testo[0]);         // 'H'
print(testo[1]);         // 'i'
print(testo[2]);         // '🚀' (un codepoint)
print(testo[3]);         // '!'
```

---

## Concatenazione

Usa l'operatore `+` per concatenare stringhe e rune:

**Stringa + Stringa:**
```hemlock
let s = "ciao" + " " + "mondo";  // "ciao mondo"
let msg = "Conteggio: " + typeof(42); // "Conteggio: 42"
```

**Stringa + Rune:**
```hemlock
let saluto = "Ciao" + '!';       // "Ciao!"
let decorato = "Testo" + '✓';    // "Testo✓"
```

**Rune + Stringa:**
```hemlock
let prefisso = '>' + " Messaggio";   // "> Messaggio"
let punto = '•' + " Elemento";       // "• Elemento"
```

**Concatenazioni Multiple:**
```hemlock
let msg = "Ciao " + '👋' + " Mondo " + '🌍';  // "Ciao 👋 Mondo 🌍"
```

---

## Proprietà delle Stringhe

### .length

Ottiene il numero di codepoint Unicode (caratteri).

**Tipo:** `i32`

**Esempi:**
```hemlock
let s = "ciao";
print(s.length);        // 5

let emoji = "🚀";
print(emoji.length);    // 1 (un codepoint)

let testo = "Ciao 🌍!";
print(testo.length);    // 7 (6 ASCII + 1 emoji)
```

---

### .byte_length

Ottiene il numero di byte UTF-8.

**Tipo:** `i32`

**Esempi:**
```hemlock
let s = "ciao";
print(s.byte_length);   // 5 (1 byte per carattere ASCII)

let emoji = "🚀";
print(emoji.byte_length); // 4 (emoji è 4 byte UTF-8)

let testo = "Ciao 🌍!";
print(testo.byte_length);  // 11 (7 ASCII + 4 per emoji)
```

---

## Metodi delle Stringhe

### Sottostringa e Slicing

#### substr

Estrae una sottostringa per posizione e lunghezza.

**Firma:**
```hemlock
string.substr(inizio: i32, lunghezza: i32): string
```

**Parametri:**
- `inizio` - Indice del codepoint iniziale (base 0)
- `lunghezza` - Numero di codepoint da estrarre

**Restituisce:** Nuova stringa

**Esempi:**
```hemlock
let s = "ciao mondo";
let sub = s.substr(5, 5);       // "mondo"
let primo = s.substr(0, 4);     // "ciao"

// Esempio UTF-8
let testo = "Hi🚀!";
let emoji = testo.substr(2, 1);  // "🚀"
```

---

#### slice

Estrae una sottostringa per intervallo (fine esclusiva).

**Firma:**
```hemlock
string.slice(inizio: i32, fine: i32): string
```

**Parametri:**
- `inizio` - Indice del codepoint iniziale (base 0)
- `fine` - Indice del codepoint finale (esclusivo)

**Restituisce:** Nuova stringa

**Esempi:**
```hemlock
let s = "ciao mondo";
let sub = s.slice(0, 4);        // "ciao"
let mondo = s.slice(5, 10);     // "mondo"

// Esempio UTF-8
let testo = "Hi🚀!";
let primi_tre = testo.slice(0, 3);  // "Hi🚀"
```

---

### Ricerca e Trova

#### find

Trova la prima occorrenza di una sottostringa.

**Firma:**
```hemlock
string.find(ago: string): i32
```

**Parametri:**
- `ago` - Sottostringa da cercare

**Restituisce:** Indice del codepoint della prima occorrenza, o `-1` se non trovata

**Esempi:**
```hemlock
let s = "ciao mondo";
let pos = s.find("mondo");      // 5
let pos2 = s.find("foo");       // -1 (non trovato)
let pos3 = s.find("o");         // 3 (primo 'o')
```

---

#### contains

Verifica se la stringa contiene una sottostringa.

**Firma:**
```hemlock
string.contains(ago: string): bool
```

**Parametri:**
- `ago` - Sottostringa da cercare

**Restituisce:** `true` se trovata, `false` altrimenti

**Esempi:**
```hemlock
let s = "ciao mondo";
let ha = s.contains("mondo");   // true
let ha2 = s.contains("foo");    // false
```

---

### Split e Join

#### split

Divide la stringa in array per delimitatore.

**Firma:**
```hemlock
string.split(delimitatore: string): array
```

**Parametri:**
- `delimitatore` - Stringa su cui dividere

**Restituisce:** Array di stringhe

**Esempi:**
```hemlock
let csv = "a,b,c";
let parti = csv.split(",");     // ["a", "b", "c"]

let percorso = "/usr/local/bin";
let dir = percorso.split("/");  // ["", "usr", "local", "bin"]

let testo = "ciao mondo foo";
let parole = testo.split(" ");  // ["ciao", "mondo", "foo"]
```

---

#### trim

Rimuove gli spazi bianchi iniziali e finali.

**Firma:**
```hemlock
string.trim(): string
```

**Restituisce:** Nuova stringa con spazi bianchi rimossi

**Esempi:**
```hemlock
let s = "  ciao  ";
let pulito = s.trim();           // "ciao"

let testo = "\n\t  mondo  \n";
let pulito2 = testo.trim();      // "mondo"
```

---

### Conversione Maiuscole/Minuscole

#### to_upper

Converte la stringa in maiuscolo.

**Firma:**
```hemlock
string.to_upper(): string
```

**Restituisce:** Nuova stringa in maiuscolo

**Esempi:**
```hemlock
let s = "ciao mondo";
let maiuscolo = s.to_upper();    // "CIAO MONDO"

let misto = "CiAo";
let maiuscolo2 = misto.to_upper();  // "CIAO"
```

---

#### to_lower

Converte la stringa in minuscolo.

**Firma:**
```hemlock
string.to_lower(): string
```

**Restituisce:** Nuova stringa in minuscolo

**Esempi:**
```hemlock
let s = "CIAO MONDO";
let minuscolo = s.to_lower();    // "ciao mondo"

let misto = "CiAo";
let minuscolo2 = misto.to_lower();  // "ciao"
```

---

### Prefisso e Suffisso

#### starts_with

Verifica se la stringa inizia con un prefisso.

**Firma:**
```hemlock
string.starts_with(prefisso: string): bool
```

**Parametri:**
- `prefisso` - Prefisso da verificare

**Restituisce:** `true` se la stringa inizia con il prefisso, `false` altrimenti

**Esempi:**
```hemlock
let s = "ciao mondo";
let inizia = s.starts_with("ciao");   // true
let inizia2 = s.starts_with("mondo"); // false
```

---

#### ends_with

Verifica se la stringa termina con un suffisso.

**Firma:**
```hemlock
string.ends_with(suffisso: string): bool
```

**Parametri:**
- `suffisso` - Suffisso da verificare

**Restituisce:** `true` se la stringa termina con il suffisso, `false` altrimenti

**Esempi:**
```hemlock
let s = "ciao mondo";
let termina = s.ends_with("mondo");  // true
let termina2 = s.ends_with("ciao");  // false
```

---

### Sostituzione

#### replace

Sostituisce la prima occorrenza di una sottostringa.

**Firma:**
```hemlock
string.replace(vecchio: string, nuovo: string): string
```

**Parametri:**
- `vecchio` - Sottostringa da sostituire
- `nuovo` - Stringa di sostituzione

**Restituisce:** Nuova stringa con la prima occorrenza sostituita

**Esempi:**
```hemlock
let s = "ciao mondo";
let s2 = s.replace("mondo", "italia");  // "ciao italia"

let testo = "foo foo foo";
let testo2 = testo.replace("foo", "bar"); // "bar foo foo" (solo la prima)
```

---

#### replace_all

Sostituisce tutte le occorrenze di una sottostringa.

**Firma:**
```hemlock
string.replace_all(vecchio: string, nuovo: string): string
```

**Parametri:**
- `vecchio` - Sottostringa da sostituire
- `nuovo` - Stringa di sostituzione

**Restituisce:** Nuova stringa con tutte le occorrenze sostituite

**Esempi:**
```hemlock
let testo = "foo foo foo";
let testo2 = testo.replace_all("foo", "bar"); // "bar bar bar"

let s = "ciao mondo ciao";
let s2 = s.replace_all("ciao", "salve");      // "salve mondo salve"
```

---

### Ripetizione

#### repeat

Ripete la stringa n volte.

**Firma:**
```hemlock
string.repeat(conteggio: i32): string
```

**Parametri:**
- `conteggio` - Numero di ripetizioni

**Restituisce:** Nuova stringa ripetuta conteggio volte

**Esempi:**
```hemlock
let s = "ah";
let ripetuto = s.repeat(3);     // "ahahah"

let linea = "-";
let separatore = linea.repeat(40); // "----------------------------------------"
```

---

### Accesso ai Caratteri

#### char_at

Ottiene il codepoint Unicode all'indice.

**Firma:**
```hemlock
string.char_at(indice: i32): rune
```

**Parametri:**
- `indice` - Indice del codepoint (base 0)

**Restituisce:** Rune (codepoint Unicode)

**Esempi:**
```hemlock
let s = "ciao";
let ch = s.char_at(0);          // 'c'
let ch2 = s.char_at(1);         // 'i'

// Esempio UTF-8
let emoji = "🚀";
let ch3 = emoji.char_at(0);     // U+1F680 (razzo)
```

---

#### chars

Converte la stringa in array di rune.

**Firma:**
```hemlock
string.chars(): array
```

**Restituisce:** Array di rune (codepoint)

**Esempi:**
```hemlock
let s = "ciao";
let caratteri = s.chars();          // ['c', 'i', 'a', 'o']

// Esempio UTF-8
let testo = "Hi🚀!";
let caratteri2 = testo.chars();     // ['H', 'i', '🚀', '!']
```

---

### Accesso ai Byte

#### byte_at

Ottiene il valore del byte all'indice.

**Firma:**
```hemlock
string.byte_at(indice: i32): u8
```

**Parametri:**
- `indice` - Indice del byte (base 0, NON indice del codepoint)

**Restituisce:** Valore del byte (u8)

**Esempi:**
```hemlock
let s = "ciao";
let byte = s.byte_at(0);        // 99 (ASCII 'c')
let byte2 = s.byte_at(1);       // 105 (ASCII 'i')

// Esempio UTF-8
let emoji = "🚀";
let byte3 = emoji.byte_at(0);   // 240 (primo byte UTF-8)
```

---

#### bytes

Converte la stringa in array di byte.

**Firma:**
```hemlock
string.bytes(): array
```

**Restituisce:** Array di byte u8

**Esempi:**
```hemlock
let s = "ciao";
let bytes = s.bytes();          // [99, 105, 97, 111]

// Esempio UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 byte UTF-8)
```

---

#### to_bytes

Converte la stringa in buffer.

**Firma:**
```hemlock
string.to_bytes(): buffer
```

**Restituisce:** Buffer contenente i byte UTF-8

**Esempi:**
```hemlock
let s = "ciao";
let buf = s.to_bytes();
print(buf.length);              // 5

// Esempio UTF-8
let emoji = "🚀";
let buf2 = emoji.to_bytes();
print(buf2.length);             // 4
```

**Nota:** Questo è un metodo legacy. Preferisci `.bytes()` per la maggior parte dei casi d'uso.

---

### Deserializzazione JSON

#### deserialize

Analizza una stringa JSON in un valore.

**Firma:**
```hemlock
string.deserialize(): any
```

**Restituisce:** Valore analizzato (oggetto, array, numero, stringa, bool o null)

**Esempi:**
```hemlock
let json = '{"x":10,"y":20}';
let obj = json.deserialize();
print(obj.x);                   // 10
print(obj.y);                   // 20

let arr_json = '[1,2,3]';
let arr = arr_json.deserialize();
print(arr[0]);                  // 1

let num_json = '42';
let num = num_json.deserialize();
print(num);                     // 42
```

**Tipi Supportati:**
- Oggetti: `{"chiave": valore}`
- Array: `[1, 2, 3]`
- Numeri: `42`, `3.14`
- Stringhe: `"testo"`
- Booleani: `true`, `false`
- Null: `null`

**Vedi Anche:** Metodo `.serialize()` degli oggetti

---

## Concatenamento di Metodi

I metodi delle stringhe possono essere concatenati per operazioni concise:

**Esempi:**
```hemlock
let risultato = "  Ciao Mondo  "
    .trim()
    .to_lower()
    .replace("mondo", "hemlock");  // "ciao hemlock"

let elaborato = "foo,bar,baz"
    .split(",")
    .join(" | ");                  // "foo | bar | baz"

let pulito = "  CIAO  "
    .trim()
    .to_lower();                   // "ciao"
```

---

## Riepilogo Completo dei Metodi

| Metodo         | Firma                                    | Restituisce | Descrizione                           |
|----------------|------------------------------------------|-------------|---------------------------------------|
| `substr`       | `(inizio: i32, lunghezza: i32)`          | `string`    | Estrae sottostringa per posizione/lunghezza |
| `slice`        | `(inizio: i32, fine: i32)`               | `string`    | Estrae sottostringa per intervallo    |
| `find`         | `(ago: string)`                          | `i32`       | Trova prima occorrenza (-1 se non trovata) |
| `contains`     | `(ago: string)`                          | `bool`      | Verifica se contiene sottostringa     |
| `split`        | `(delimitatore: string)`                 | `array`     | Divide in array                       |
| `trim`         | `()`                                     | `string`    | Rimuove spazi bianchi                 |
| `to_upper`     | `()`                                     | `string`    | Converte in maiuscolo                 |
| `to_lower`     | `()`                                     | `string`    | Converte in minuscolo                 |
| `starts_with`  | `(prefisso: string)`                     | `bool`      | Verifica se inizia con prefisso       |
| `ends_with`    | `(suffisso: string)`                     | `bool`      | Verifica se termina con suffisso      |
| `replace`      | `(vecchio: string, nuovo: string)`       | `string`    | Sostituisce prima occorrenza          |
| `replace_all`  | `(vecchio: string, nuovo: string)`       | `string`    | Sostituisce tutte le occorrenze       |
| `repeat`       | `(conteggio: i32)`                       | `string`    | Ripete la stringa n volte             |
| `char_at`      | `(indice: i32)`                          | `rune`      | Ottiene codepoint all'indice          |
| `byte_at`      | `(indice: i32)`                          | `u8`        | Ottiene byte all'indice               |
| `chars`        | `()`                                     | `array`     | Converte in array di rune             |
| `bytes`        | `()`                                     | `array`     | Converte in array di byte             |
| `to_bytes`     | `()`                                     | `buffer`    | Converte in buffer (legacy)           |
| `deserialize`  | `()`                                     | `any`       | Analizza stringa JSON                 |

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Dettagli sul tipo stringa
- [API degli Array](array-api.md) - Metodi degli array per risultati di split()
- [Operatori](operators.md) - Operatore di concatenazione stringhe
