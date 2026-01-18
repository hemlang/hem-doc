# Riferimento degli Operatori

Riferimento completo per gli operatori di Hemlock, la precedenza e il comportamento dei tipi.

---

## Panoramica

Hemlock fornisce un insieme completo di operatori per aritmetica, confronto, logica e manipolazione bit a bit. Gli operatori seguono la sintassi in stile C con regole di precedenza chiare.

**Caratteristiche Principali:**
- Sintassi familiare in stile C
- Promozione automatica dei tipi nelle operazioni miste
- Operatori bit a bit per manipolazione interi
- Controllo preciso della precedenza

---

## Operatori Aritmetici

### Aritmetica Base

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `+` | Addizione | `5 + 3` | `8` |
| `-` | Sottrazione | `5 - 3` | `2` |
| `*` | Moltiplicazione | `5 * 3` | `15` |
| `/` | Divisione | `5 / 2` | `2.5` |
| `%` | Modulo | `5 % 3` | `2` |

**Esempi:**
```hemlock
// Aritmetica intera
let a = 10 + 5;     // 15
let b = 10 - 5;     // 5
let c = 10 * 5;     // 50
let d = 10 / 3;     // 3.333... (sempre float)
let e = 10 % 3;     // 1

// Aritmetica float
let f = 3.14 + 2.0; // 5.14
let g = 10.0 / 4.0; // 2.5

// Aritmetica mista
let h = 10 + 2.5;   // 12.5 (promosso a float)
```

### Divisione Intera

L'operatore `/` restituisce sempre un float. Per la divisione intera, usa `divi()`:

```hemlock
let a = 10 / 3;         // 3.333...
let b = divi(10, 3);    // 3 (troncato)

// Oppure usa conversione esplicita
let c: i32 = 10 / 3;    // 3 (troncato via annotazione di tipo)
```

### Negazione Unaria

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `-` | Negazione | `-5` | `-5` |

```hemlock
let x = 5;
let y = -x;         // -5
let z = --x;        // 5 (doppia negazione)
```

---

## Operatori di Incremento/Decremento

| Operatore | Nome | Esempio | Descrizione |
|-----------|------|---------|-------------|
| `++` | Pre-incremento | `++x` | Incrementa x, restituisce nuovo valore |
| `++` | Post-incremento | `x++` | Restituisce valore corrente, poi incrementa |
| `--` | Pre-decremento | `--x` | Decrementa x, restituisce nuovo valore |
| `--` | Post-decremento | `x--` | Restituisce valore corrente, poi decrementa |

**Esempi:**
```hemlock
let x = 5;

// Pre-incremento
let a = ++x;        // x = 6, a = 6

// Post-incremento
let b = x++;        // b = 6, x = 7

// Pre-decremento
let c = --x;        // x = 6, c = 6

// Post-decremento
let d = x--;        // d = 6, x = 5
```

---

## Operatori di Confronto

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `==` | Uguale a | `5 == 5` | `true` |
| `!=` | Diverso da | `5 != 3` | `true` |
| `<` | Minore di | `3 < 5` | `true` |
| `>` | Maggiore di | `5 > 3` | `true` |
| `<=` | Minore o uguale | `3 <= 3` | `true` |
| `>=` | Maggiore o uguale | `5 >= 5` | `true` |

**Esempi:**
```hemlock
// Confronto numeri
print(5 == 5);      // true
print(5 != 3);      // true
print(3 < 5);       // true
print(5 > 3);       // true
print(3 <= 3);      // true
print(5 >= 5);      // true

// Confronto stringhe
print("abc" == "abc");  // true
print("abc" < "abd");   // true (lessicografico)

// Confronto tipi misti
print(5 == 5.0);    // true (promosso a float)
print(5 != "5");    // true (tipi diversi)
```

---

## Operatori Logici

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `&&` | AND logico | `true && false` | `false` |
| `\|\|` | OR logico | `true \|\| false` | `true` |
| `!` | NOT logico | `!true` | `false` |

**Esempi:**
```hemlock
// Operazioni booleane
print(true && true);    // true
print(true && false);   // false
print(true || false);   // true
print(false || false);  // false
print(!true);           // false
print(!false);          // true

// Valutazione cortocircuito
let x = false && costoso();  // costoso() non viene chiamata
let y = true || costoso();   // costoso() non viene chiamata
```

### Valutazione Cortocircuito

`&&` e `||` usano la valutazione cortocircuito:

```hemlock
// AND: si ferma al primo false
let risultato = a() && b() && c();
// Se a() restituisce false, b() e c() non sono valutate

// OR: si ferma al primo true
let risultato = a() || b() || c();
// Se a() restituisce true, b() e c() non sono valutate
```

---

## Operatori Bit a Bit

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `&` | AND bit a bit | `5 & 3` | `1` |
| `\|` | OR bit a bit | `5 \| 3` | `7` |
| `^` | XOR bit a bit | `5 ^ 3` | `6` |
| `~` | NOT bit a bit | `~5` | `-6` |
| `<<` | Shift sinistra | `5 << 2` | `20` |
| `>>` | Shift destra | `20 >> 2` | `5` |

**Esempi:**
```hemlock
// AND: 0101 & 0011 = 0001
print(5 & 3);           // 1

// OR: 0101 | 0011 = 0111
print(5 | 3);           // 7

// XOR: 0101 ^ 0011 = 0110
print(5 ^ 3);           // 6

// NOT: ~0101 = ...1010 (complemento a due)
print(~5);              // -6

// Shift sinistra: 0101 << 2 = 10100
print(5 << 2);          // 20

// Shift destra: 10100 >> 2 = 00101
print(20 >> 2);         // 5
```

### Tecniche Bit a Bit

```hemlock
// Impostare un bit
let flag = 1 << 3;          // Bit 3: 0b1000 = 8

// Verificare un bit
let ha_bit = (valore & flag) != 0;

// Pulire un bit
let pulito = valore & ~flag;

// Attivare/disattivare un bit
let attivato = valore ^ flag;

// Verifica potenza di 2
let e_pot2 = n != 0 && (n & (n - 1)) == 0;
```

---

## Operatori di Assegnazione

### Assegnazione Semplice

| Operatore | Nome | Esempio | Equivalente |
|-----------|------|---------|-------------|
| `=` | Assegnazione | `x = 5` | - |

### Assegnazione Composta

| Operatore | Nome | Esempio | Equivalente |
|-----------|------|---------|-------------|
| `+=` | Addizione assegnazione | `x += 5` | `x = x + 5` |
| `-=` | Sottrazione assegnazione | `x -= 5` | `x = x - 5` |
| `*=` | Moltiplicazione assegnazione | `x *= 5` | `x = x * 5` |
| `/=` | Divisione assegnazione | `x /= 5` | `x = x / 5` |
| `%=` | Modulo assegnazione | `x %= 5` | `x = x % 5` |
| `&=` | AND assegnazione | `x &= 5` | `x = x & 5` |
| `\|=` | OR assegnazione | `x \|= 5` | `x = x \| 5` |
| `^=` | XOR assegnazione | `x ^= 5` | `x = x ^ 5` |
| `<<=` | Shift sinistra assegnazione | `x <<= 2` | `x = x << 2` |
| `>>=` | Shift destra assegnazione | `x >>= 2` | `x = x >> 2` |

**Esempi:**
```hemlock
let x = 10;
x += 5;         // x = 15
x -= 3;         // x = 12
x *= 2;         // x = 24
x /= 4;         // x = 6.0
x %= 4;         // x = 2

let flags = 0;
flags |= 0b0100;    // Imposta bit 2
flags &= ~0b0010;   // Pulisci bit 1
flags ^= 0b1000;    // Attiva bit 3
```

---

## Operatore Ternario

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `? :` | Condizionale | `x > 0 ? "pos" : "non-pos"` | Dipende da x |

**Esempi:**
```hemlock
let x = 5;
let segno = x > 0 ? "positivo" : "non-positivo";
print(segno);       // "positivo"

// Ternario annidato
let categoria = x > 10 ? "grande" :
                x > 5 ? "medio" : "piccolo";

// Come espressione
print(x % 2 == 0 ? "pari" : "dispari");
```

---

## Concatenazione di Stringhe

| Operatore | Nome | Esempio | Risultato |
|-----------|------|---------|-----------|
| `+` | Concatenazione | `"ciao" + " mondo"` | `"ciao mondo"` |

**Esempi:**
```hemlock
let saluto = "Ciao" + " " + "Mondo";
print(saluto);      // "Ciao Mondo"

// Stringa + Rune
let msg = "Fatto" + '!';
print(msg);         // "Fatto!"

// Stringa + altri tipi (conversione automatica)
let conteggio = "Totale: " + 42;
print(conteggio);   // "Totale: 42"
```

---

## Operatori di Accesso

### Accesso ad Array

| Operatore | Nome | Esempio | Descrizione |
|-----------|------|---------|-------------|
| `[]` | Indicizzazione | `arr[0]` | Ottiene elemento all'indice |

**Esempi:**
```hemlock
let arr = [10, 20, 30];
print(arr[0]);      // 10
arr[1] = 25;        // Modifica elemento
print(arr[1]);      // 25
```

### Accesso a Campi

| Operatore | Nome | Esempio | Descrizione |
|-----------|------|---------|-------------|
| `.` | Accesso campo | `obj.campo` | Ottiene proprietà dell'oggetto |

**Esempi:**
```hemlock
let persona = { nome: "Alice", eta: 30 };
print(persona.nome);    // "Alice"
persona.eta = 31;       // Modifica campo
```

### Chiamata di Funzione

| Operatore | Nome | Esempio | Descrizione |
|-----------|------|---------|-------------|
| `()` | Chiamata | `func(a, b)` | Chiama funzione con argomenti |

**Esempi:**
```hemlock
fn somma(a, b) {
    return a + b;
}
print(somma(3, 4));     // 7

// Chiamata di metodo
let s = "ciao";
print(s.to_upper());    // "CIAO"
```

---

## Operatori Null-Coalescing

| Operatore | Nome | Esempio | Descrizione |
|-----------|------|---------|-------------|
| `??` | Null coalescing | `a ?? b` | Restituisce a se non-null, altrimenti b |
| `??=` | Null assegnazione | `a ??= b` | Assegna b ad a solo se a è null |
| `?.` | Navigazione sicura | `obj?.campo` | Restituisce null se obj è null |

**Esempi:**
```hemlock
// Null coalescing
let nome = utente.nome ?? "Anonimo";
let primo = a ?? b ?? c ?? "predefinito";

// Assegnazione null coalescing
let config = null;
config ??= { timeout: 30 };     // config ora è { timeout: 30 }
config ??= { timeout: 60 };     // config invariato (non null)

// Navigazione sicura
let citta = utente?.indirizzo?.citta;  // null se qualsiasi parte è null
let maiusc = nome?.to_upper();          // chiamata metodo sicura
let elem = arr?.[0];                    // indicizzazione sicura
```

---

## Precedenza degli Operatori

Dalla precedenza più bassa a quella più alta:

| Livello | Operatori | Associatività | Descrizione |
|---------|-----------|---------------|-------------|
| 1 | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `\|=`, `^=`, `<<=`, `>>=`, `??=` | Destra | Assegnazione |
| 2 | `??` | Sinistra | Null coalescing |
| 3 | `? :` | Destra | Condizionale |
| 4 | `\|\|` | Sinistra | OR logico |
| 5 | `&&` | Sinistra | AND logico |
| 6 | `\|` | Sinistra | OR bit a bit |
| 7 | `^` | Sinistra | XOR bit a bit |
| 8 | `&` | Sinistra | AND bit a bit |
| 9 | `==`, `!=` | Sinistra | Uguaglianza |
| 10 | `<`, `>`, `<=`, `>=` | Sinistra | Confronto |
| 11 | `<<`, `>>` | Sinistra | Shift |
| 12 | `+`, `-` | Sinistra | Addizione/Sottrazione |
| 13 | `*`, `/`, `%` | Sinistra | Moltiplicazione/Divisione |
| 14 | `!`, `-`, `~`, `++`, `--` | Destra | Unario |
| 15 | `()`, `[]`, `.`, `?.` | Sinistra | Chiamata/Accesso |

**Esempi:**
```hemlock
// La moltiplicazione lega più stretto dell'addizione
let x = 2 + 3 * 4;      // 14, non 20

// AND logico lega più stretto di OR
let y = true || false && false;  // true

// Usa parentesi per chiarezza
let z = (2 + 3) * 4;    // 20
let w = (a || b) && c;  // (a || b) valutato prima

// Accesso a campo lega più stretto di operatori aritmetici
let lunghezza = arr.length * 2;  // (arr.length) * 2
```

---

## Promozione dei Tipi

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
2. Dimensione maggiore vince nella stessa categoria
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

---

## Riepilogo Completo degli Operatori

### Operatori Aritmetici
| Operatore | Descrizione |
|-----------|-------------|
| `+` | Addizione |
| `-` | Sottrazione |
| `*` | Moltiplicazione |
| `/` | Divisione (restituisce float) |
| `%` | Modulo |
| `-` (unario) | Negazione |
| `++` | Incremento |
| `--` | Decremento |

### Operatori di Confronto
| Operatore | Descrizione |
|-----------|-------------|
| `==` | Uguale a |
| `!=` | Diverso da |
| `<` | Minore di |
| `>` | Maggiore di |
| `<=` | Minore o uguale |
| `>=` | Maggiore o uguale |

### Operatori Logici
| Operatore | Descrizione |
|-----------|-------------|
| `&&` | AND logico |
| `\|\|` | OR logico |
| `!` | NOT logico |

### Operatori Bit a Bit
| Operatore | Descrizione |
|-----------|-------------|
| `&` | AND bit a bit |
| `\|` | OR bit a bit |
| `^` | XOR bit a bit |
| `~` | NOT bit a bit |
| `<<` | Shift sinistra |
| `>>` | Shift destra |

### Operatori di Assegnazione
| Operatore | Descrizione |
|-----------|-------------|
| `=` | Assegnazione |
| `+=`, `-=`, `*=`, `/=`, `%=` | Aritmetica composta |
| `&=`, `\|=`, `^=`, `<<=`, `>>=` | Bit a bit composta |
| `??=` | Null assegnazione |

### Altri Operatori
| Operatore | Descrizione |
|-----------|-------------|
| `? :` | Condizionale |
| `??` | Null coalescing |
| `?.` | Navigazione sicura |
| `[]` | Indicizzazione |
| `.` | Accesso campo |
| `()` | Chiamata funzione |

---

## Vedi Anche

- [Sistema di Tipi](type-system.md) - Regole di promozione dei tipi
- [Funzioni Integrate](builtins.md) - Funzioni come `divi()`
- [API delle Stringhe](string-api.md) - Concatenazione stringhe
- [API degli Array](array-api.md) - Indicizzazione array
