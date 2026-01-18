# Stringhe

Le stringhe Hemlock sono **sequenze mutabili di prima classe UTF-8** con supporto completo Unicode e un ricco set di metodi per l'elaborazione del testo. A differenza di molti linguaggi, le stringhe Hemlock sono mutabili e lavorano nativamente con i codepoint Unicode.

## Panoramica

```hemlock
let s = "ciao";
s[0] = 'C';             // muta con rune (ora "Ciao")
print(s.length);        // 4 (conteggio codepoint)
let c = s[0];           // restituisce rune (codepoint Unicode)
let msg = s + " mondo"; // concatenazione
let emoji = "🚀";
print(emoji.length);    // 1 (un codepoint)
print(emoji.byte_length); // 4 (quattro byte UTF-8)
```

## Proprieta

Le stringhe Hemlock hanno queste caratteristiche chiave:

- **Codifica UTF-8** - Supporto completo Unicode (da U+0000 a U+10FFFF)
- **Mutabili** - A differenza delle stringhe Python, JavaScript e Java
- **Indicizzazione basata su codepoint** - Restituisce `rune` (codepoint Unicode), non byte
- **Allocate nell'heap** - Con tracciamento interno della capacita
- **Due proprieta di lunghezza**:
  - `.length` - Conteggio codepoint (numero di caratteri)
  - `.byte_length` - Conteggio byte (dimensione codifica UTF-8)

## Comportamento UTF-8

Tutte le operazioni sulle stringhe lavorano con i **codepoint** (caratteri), non con i byte:

```hemlock
let text = "Ciao🚀Mondo";
print(text.length);        // 10 (codepoint)
print(text.byte_length);   // 14 (byte, emoji e 4 byte)

// L'indicizzazione usa i codepoint
let c = text[0];           // 'C' (rune)
let rocket = text[4];      // '🚀' (rune)
```

**I caratteri multi-byte contano come uno:**
```hemlock
"Ciao".length;       // 4
"🚀".length;         // 1 (una emoji)
"你好".length;       // 2 (due caratteri cinesi)
"cafe".length;       // 4 (e e un codepoint)
```

## Letterali stringa

```hemlock
// Stringhe di base
let s1 = "ciao";
let s2 = "mondo";

// Con sequenze di escape
let s3 = "Riga 1\nRiga 2\ttabulata";
let s4 = "Virgolette: \"Ciao\"";
let s5 = "Barra rovesciata: \\";

// Caratteri Unicode
let s6 = "🚀 Emoji";
let s7 = "中文字符";
```

## Stringhe template (Interpolazione di stringhe)

Usa i backtick per le stringhe template con espressioni incorporate:

```hemlock
let name = "Alice";
let age = 30;

// Interpolazione di base
let greeting = `Ciao, ${name}!`;           // "Ciao, Alice!"
let info = `${name} ha ${age} anni`;       // "Alice ha 30 anni"

// Espressioni nell'interpolazione
let x = 5;
let y = 10;
let sum = `${x} + ${y} = ${x + y}`;        // "5 + 10 = 15"

// Chiamate di metodo
let upper = `Nome: ${name.to_upper()}`;    // "Nome: ALICE"

// Oggetti annidati
let person = { name: "Bob", city: "Roma" };
let desc = `${person.name} vive a ${person.city}`;  // "Bob vive a Roma"

// Multi-riga (preserva le nuove righe)
let multi = `Riga 1
Riga 2
Riga 3`;
```

**Caratteristiche delle stringhe template:**
- Le espressioni dentro `${...}` vengono valutate e convertite in stringhe
- Qualsiasi espressione valida puo essere usata (variabili, chiamate di funzione, aritmetica)
- Le stringhe con backtick supportano le stesse sequenze di escape delle stringhe normali
- Utili per costruire stringhe dinamiche senza concatenazione

### Escape nelle stringhe template

Per includere un letterale `${` in una stringa template, esegui l'escape del simbolo del dollaro:

```hemlock
let price = 100;
let text = `Prezzo: \${price} o ${price}`;
// "Prezzo: ${price} o 100"

// Backtick letterale
let code = `Usa \` per le stringhe template`;
// "Usa ` per le stringhe template"
```

### Espressioni complesse

Le stringhe template possono contenere qualsiasi espressione valida:

```hemlock
// Espressioni tipo ternario
let age = 25;
let status = `Stato: ${age >= 18 ? "adulto" : "minore"}`;

// Accesso array
let items = ["mela", "banana", "ciliegia"];
let first = `Primo elemento: ${items[0]}`;

// Chiamate di funzione con argomenti
fn format_price(p) { return p + " euro"; }
let msg = `Totale: ${format_price(99.99)}`;  // "Totale: 99.99 euro"

// Chiamate di metodo concatenate
let name = "alice";
let formatted = `Ciao, ${name.to_upper().slice(0, 1)}${name.slice(1)}!`;
// "Ciao, Alice!"
```

### Stringhe template vs Concatenazione

Le stringhe template sono spesso piu pulite della concatenazione:

```hemlock
// Concatenazione (piu difficile da leggere)
let msg1 = "Ciao, " + name + "! Hai " + count + " messaggi.";

// Stringa template (piu facile da leggere)
let msg2 = `Ciao, ${name}! Hai ${count} messaggi.`;
```

## Indicizzazione e mutazione

### Lettura dei caratteri

L'indicizzazione restituisce una `rune` (codepoint Unicode):

```hemlock
let s = "Ciao";
let first = s[0];      // 'C' (rune)
let last = s[3];       // 'o' (rune)

// Esempio UTF-8
let emoji = "Hi🚀!";
let rocket = emoji[2];  // '🚀' (rune all'indice codepoint 2)
```

### Scrittura dei caratteri

Le stringhe sono mutabili - puoi modificare i singoli caratteri:

```hemlock
let s = "ciao";
s[0] = 'C';            // Ora "Ciao"
s[3] = '!';            // Ora "Cia!"

// Con Unicode
let msg = "Vai!";
msg[0] = '🚀';         // Ora "🚀ai!"
```

## Concatenazione

Usa `+` per concatenare le stringhe:

```hemlock
let greeting = "Ciao" + " " + "Mondo";  // "Ciao Mondo"

// Con variabili
let name = "Alice";
let msg = "Ciao, " + name + "!";  // "Ciao, Alice!"

// Con rune (vedi documentazione Rune)
let s = "Ciao" + '!';              // "Ciao!"
```

## Metodi stringa

Hemlock fornisce 19 metodi stringa per una manipolazione completa del testo.

### Sottostringa e Slicing

**`substr(start, length)`** - Estrae sottostringa per posizione e lunghezza:
```hemlock
let s = "ciao mondo";
let sub = s.substr(5, 5);       // "mondo" (inizia a 5, lunghezza 5)
let first = s.substr(0, 4);     // "ciao"

// Esempio UTF-8
let text = "Hi🚀!";
let emoji = text.substr(2, 1);  // "🚀" (posizione 2, lunghezza 1)
```

**`slice(start, end)`** - Estrae sottostringa per intervallo (end esclusivo):
```hemlock
let s = "ciao mondo";
let slice = s.slice(0, 4);      // "ciao" (indice da 0 a 3)
let slice2 = s.slice(5, 10);    // "mondo"
```

**Differenza:**
- `substr(start, length)` - Usa parametro lunghezza
- `slice(start, end)` - Usa indice finale (esclusivo)

### Ricerca e Trova

**`find(needle)`** - Trova la prima occorrenza:
```hemlock
let s = "ciao mondo";
let pos = s.find("mondo");      // 5 (indice della prima occorrenza)
let pos2 = s.find("foo");       // -1 (non trovato)
let pos3 = s.find("o");         // 3 (primo 'o')
```

**`contains(needle)`** - Verifica se la stringa contiene la sottostringa:
```hemlock
let s = "ciao mondo";
let has = s.contains("mondo");  // true
let has2 = s.contains("foo");   // false
```

### Split e Trim

**`split(delimiter)`** - Divide in array di stringhe:
```hemlock
let csv = "mela,banana,ciliegia";
let parts = csv.split(",");     // ["mela", "banana", "ciliegia"]

let words = "uno due tre".split(" ");  // ["uno", "due", "tre"]

// Delimitatore vuoto divide per carattere
let chars = "abc".split("");    // ["a", "b", "c"]
```

**`trim()`** - Rimuove spazi bianchi iniziali/finali:
```hemlock
let s = "  ciao  ";
let clean = s.trim();           // "ciao"

let s2 = "\t\ntesto\n\t";
let clean2 = s2.trim();         // "testo"
```

### Conversione maiuscole/minuscole

**`to_upper()`** - Converte in maiuscolo:
```hemlock
let s = "ciao mondo";
let upper = s.to_upper();       // "CIAO MONDO"

// Preserva non-ASCII
let s2 = "cafe";
let upper2 = s2.to_upper();     // "CAFE"
```

**`to_lower()`** - Converte in minuscolo:
```hemlock
let s = "CIAO MONDO";
let lower = s.to_lower();       // "ciao mondo"
```

### Controllo prefisso/suffisso

**`starts_with(prefix)`** - Verifica se inizia con il prefisso:
```hemlock
let s = "ciao mondo";
let starts = s.starts_with("ciao");  // true
let starts2 = s.starts_with("mondo"); // false
```

**`ends_with(suffix)`** - Verifica se finisce con il suffisso:
```hemlock
let s = "ciao mondo";
let ends = s.ends_with("mondo");      // true
let ends2 = s.ends_with("ciao");      // false
```

### Sostituzione

**`replace(old, new)`** - Sostituisce la prima occorrenza:
```hemlock
let s = "ciao mondo";
let s2 = s.replace("mondo", "amico");      // "ciao amico"

let s3 = "foo foo foo";
let s4 = s3.replace("foo", "bar");         // "bar foo foo" (solo il primo)
```

**`replace_all(old, new)`** - Sostituisce tutte le occorrenze:
```hemlock
let s = "foo foo foo";
let s2 = s.replace_all("foo", "bar");      // "bar bar bar"

let s3 = "ciao mondo, mondo!";
let s4 = s3.replace_all("mondo", "hemlock"); // "ciao hemlock, hemlock!"
```

### Ripetizione

**`repeat(count)`** - Ripete la stringa n volte:
```hemlock
let s = "ah";
let laugh = s.repeat(3);        // "ahahah"

let line = "=".repeat(40);      // "========================================"
```

### Accesso a caratteri e byte

**`char_at(index)`** - Ottiene il codepoint Unicode all'indice (restituisce rune):
```hemlock
let s = "ciao";
let char = s.char_at(0);        // 'c' (rune)

// Esempio UTF-8
let emoji = "🚀";
let rocket = emoji.char_at(0);  // Restituisce rune U+1F680
```

**`chars()`** - Converte in array di rune (codepoint):
```hemlock
let s = "ciao";
let chars = s.chars();          // ['c', 'i', 'a', 'o'] (array di rune)

// Esempio UTF-8
let text = "Hi🚀";
let chars2 = text.chars();      // ['H', 'i', '🚀']
```

**`byte_at(index)`** - Ottiene il valore byte all'indice (restituisce u8):
```hemlock
let s = "ciao";
let byte = s.byte_at(0);        // 99 (valore ASCII di 'c')

// Esempio UTF-8
let emoji = "🚀";
let first_byte = emoji.byte_at(0);  // 240 (primo byte UTF-8)
```

**`bytes()`** - Converte in array di byte (valori u8):
```hemlock
let s = "ciao";
let bytes = s.bytes();          // [99, 105, 97, 111] (array di u8)

// Esempio UTF-8
let emoji = "🚀";
let bytes2 = emoji.bytes();     // [240, 159, 154, 128] (4 byte UTF-8)
```

**`to_bytes()`** - Converte in buffer per accesso a basso livello:
```hemlock
let s = "ciao";
let buf = s.to_bytes();         // Restituisce buffer con byte UTF-8
print(buf.length);              // 4
free(buf);                      // Ricorda di liberare
```

## Concatenamento dei metodi

Tutti i metodi stringa restituiscono nuove stringhe, consentendo il concatenamento:

```hemlock
let result = "  Ciao Mondo  "
    .trim()
    .to_lower()
    .replace("mondo", "hemlock");  // "ciao hemlock"

let processed = "foo,bar,baz"
    .split(",")
    .join(" | ")
    .to_upper();                    // "FOO | BAR | BAZ"
```

## Riferimento completo dei metodi

| Metodo | Parametri | Restituisce | Descrizione |
|--------|-----------|-------------|-------------|
| `substr(start, length)` | i32, i32 | string | Estrae sottostringa per posizione e lunghezza |
| `slice(start, end)` | i32, i32 | string | Estrae sottostringa per intervallo (end esclusivo) |
| `find(needle)` | string | i32 | Trova prima occorrenza (-1 se non trovato) |
| `contains(needle)` | string | bool | Verifica se contiene sottostringa |
| `split(delimiter)` | string | array | Divide in array di stringhe |
| `trim()` | - | string | Rimuove spazi bianchi iniziali/finali |
| `to_upper()` | - | string | Converte in maiuscolo |
| `to_lower()` | - | string | Converte in minuscolo |
| `starts_with(prefix)` | string | bool | Verifica se inizia con prefisso |
| `ends_with(suffix)` | string | bool | Verifica se finisce con suffisso |
| `replace(old, new)` | string, string | string | Sostituisce prima occorrenza |
| `replace_all(old, new)` | string, string | string | Sostituisce tutte le occorrenze |
| `repeat(count)` | i32 | string | Ripete stringa n volte |
| `char_at(index)` | i32 | rune | Ottiene codepoint all'indice |
| `byte_at(index)` | i32 | u8 | Ottiene valore byte all'indice |
| `chars()` | - | array | Converte in array di rune |
| `bytes()` | - | array | Converte in array di byte u8 |
| `to_bytes()` | - | buffer | Converte in buffer (deve essere liberato) |

## Esempi

### Esempio: Elaborazione del testo

```hemlock
fn process_input(text: string): string {
    return text
        .trim()
        .to_lower()
        .replace_all("  ", " ");  // Normalizza gli spazi bianchi
}

let input = "  CIAO   MONDO  ";
let clean = process_input(input);  // "ciao mondo"
```

### Esempio: Parser CSV

```hemlock
fn parse_csv_line(line: string): array {
    let trimmed = line.trim();
    let fields = trimmed.split(",");

    let result = [];
    let i = 0;
    while (i < fields.length) {
        result.push(fields[i].trim());
        i = i + 1;
    }

    return result;
}

let csv = "mela, banana , ciliegia";
let fields = parse_csv_line(csv);  // ["mela", "banana", "ciliegia"]
```

### Esempio: Contatore di parole

```hemlock
fn count_words(text: string): i32 {
    let words = text.trim().split(" ");
    return words.length;
}

let sentence = "La volpe veloce e marrone";
let count = count_words(sentence);  // 5
```

### Esempio: Validazione stringa

```hemlock
fn is_valid_email(email: string): bool {
    if (!email.contains("@")) {
        return false;
    }

    if (!email.contains(".")) {
        return false;
    }

    if (email.starts_with("@") || email.ends_with("@")) {
        return false;
    }

    return true;
}

print(is_valid_email("user@example.com"));  // true
print(is_valid_email("invalid"));            // false
```

## Gestione della memoria

Le stringhe sono allocate nell'heap con conteggio interno dei riferimenti:

- **Creazione**: Allocate nell'heap con tracciamento della capacita
- **Concatenazione**: Crea nuova stringa (stringhe vecchie invariate)
- **Metodi**: La maggior parte dei metodi restituisce nuove stringhe
- **Ciclo di vita**: Le stringhe sono conteggiate per riferimento e liberate automaticamente quando lo scope termina

**Pulizia automatica:**
```hemlock
fn create_strings() {
    let s = "ciao";
    let s2 = s + " mondo";  // Nuova allocazione
}  // Sia s che s2 vengono liberati automaticamente quando la funzione ritorna
```

**Nota:** Le variabili stringa locali vengono pulite automaticamente quando escono dallo scope. Usa `free()` solo per la pulizia anticipata prima della fine dello scope o per dati globali/a lunga durata. Vedi [Gestione della memoria](memory.md#conteggio-interno-dei-riferimenti) per i dettagli.

## Buone pratiche

1. **Usa l'indicizzazione per codepoint** - Le stringhe usano posizioni codepoint, non offset di byte
2. **Testa con Unicode** - Testa sempre le operazioni sulle stringhe con caratteri multi-byte
3. **Preferisci operazioni immutabili** - Usa metodi che restituiscono nuove stringhe piuttosto che la mutazione
4. **Controlla i limiti** - L'indicizzazione delle stringhe non controlla i limiti (restituisce null/errore su indice non valido)
5. **Normalizza l'input** - Usa `trim()` e `to_lower()` per l'input utente

## Trabocchetti comuni

### Trabocchetto: Confusione byte vs. codepoint

```hemlock
let emoji = "🚀";
print(emoji.length);        // 1 (codepoint)
print(emoji.byte_length);   // 4 (byte)

// Non mescolare operazioni su byte e codepoint
let byte = emoji.byte_at(0);  // 240 (primo byte)
let char = emoji.char_at(0);  // '🚀' (codepoint completo)
```

### Trabocchetto: Sorprese nella mutazione

```hemlock
let s1 = "ciao";
let s2 = s1;       // Copia superficiale
s1[0] = 'C';       // Muta s1
print(s2);         // Ancora "ciao" (le stringhe sono tipi valore)
```

## Argomenti correlati

- [Rune](runes.md) - Tipo codepoint Unicode usato nell'indicizzazione delle stringhe
- [Array](arrays.md) - I metodi stringa spesso restituiscono o lavorano con array
- [Tipi](types.md) - Dettagli sul tipo stringa e conversioni

## Vedi anche

- **Codifica UTF-8**: Vedi sezione "Strings" di CLAUDE.md
- **Conversioni di tipo**: Vedi [Tipi](types.md) per le conversioni di stringa
- **Memoria**: Vedi [Memoria](memory.md) per i dettagli sull'allocazione delle stringhe
