# Filosofia di Progettazione del Linguaggio Hemlock

> "Un linguaggio piccolo e non sicuro per scrivere cose non sicure in modo sicuro."

Questo documento cattura i principi fondamentali di progettazione e la filosofia di Hemlock. Leggi questo prima di apportare modifiche o aggiunte al linguaggio.

---

## Sommario

- [Identità Fondamentale](#identità-fondamentale)
- [Principi di Progettazione](#principi-di-progettazione)
- [Filosofia sulla Sicurezza](#filosofia-sulla-sicurezza)
- [Cosa NON Aggiungere](#cosa-non-aggiungere)
- [Considerazioni Future](#considerazioni-future)
- [Riflessioni Finali](#riflessioni-finali)

---

## Identità Fondamentale

Hemlock è un **linguaggio di scripting per sistemi** che abbraccia la gestione manuale della memoria e il controllo esplicito. È progettato per programmatori che vogliono:

- La potenza del C
- L'ergonomia dei moderni linguaggi di scripting
- Concorrenza asincrona strutturata integrata
- Nessun comportamento nascosto o magia

### Cosa Hemlock NON È

- **Memory-safe** (i puntatori dangling sono responsabilità tua)
- **Un sostituto di Rust, Go o Lua**
- **Un linguaggio che nasconde la complessità**

### Cosa Hemlock È

- **Esplicito su implicito, sempre**
- **Educativo e sperimentale**
- **Un "livello di scripting C" per lavoro sui sistemi**
- **Onesto sui compromessi**

---

## Principi di Progettazione

### 1. Esplicito su Implicito

Hemlock favorisce l'esplicitezza in tutti i costrutti del linguaggio. Non dovrebbero esserci sorprese, magie o comportamenti nascosti.

**Male (implicito):**
```hemlock
let x = 5  // Punto e virgola mancante - dovrebbe dare errore
```

**Bene (esplicito):**
```hemlock
let x = 5;
free(ptr);  // Lo hai allocato tu, lo liberi tu
```

**Aspetti chiave:**
- I punti e virgola sono obbligatori (nessuna inserzione automatica)
- Nessun garbage collection
- Gestione manuale della memoria (alloc/free)
- Le annotazioni di tipo sono opzionali ma verificate a runtime
- Nessuna pulizia automatica delle risorse (no RAII), ma `defer` fornisce pulizia esplicita

### 2. Dinamico di Default, Tipizzato per Scelta

Ogni valore ha un tag di tipo a runtime, ma il sistema è progettato per essere flessibile pur catturando gli errori.

**Inferenza dei tipi:**
- Interi piccoli (stanno in i32): `42` → `i32`
- Interi grandi (> intervallo i32): `9223372036854775807` → `i64`
- Float: `3.14` → `f64`

**Tipizzazione esplicita quando necessaria:**
```hemlock
let x = 42;              // i32 inferito (valore piccolo)
let y: u8 = 255;         // u8 esplicito
let z = x + y;           // promuove a i32
let grande = 5000000000; // i64 inferito (> max i32)
```

**Le regole di promozione dei tipi** seguono una gerarchia chiara dal più piccolo al più grande, con i float che vincono sempre sugli interi.

### 3. Non Sicuro è una Caratteristica, Non un Bug

Hemlock non cerca di prevenire tutti gli errori. Invece, ti dà gli strumenti per essere sicuro permettendoti di optare per comportamenti non sicuri quando necessario.

**Esempi di non sicurezza intenzionale:**
- L'aritmetica dei puntatori può causare overflow (responsabilità dell'utente)
- Nessun controllo dei limiti sui `ptr` grezzi (usa `buffer` se vuoi sicurezza)
- I double-free causano crash (gestione manuale della memoria)
- Il sistema dei tipi previene gli incidenti ma permette operazioni rischiose quando necessario

```hemlock
let p = alloc(10);
let q = p + 100;  // Molto oltre l'allocazione - permesso ma pericoloso
```

**La filosofia:** Il sistema dei tipi dovrebbe prevenire gli *incidenti* ma permettere operazioni non sicure *intenzionali*.

### 4. Concorrenza Strutturata di Prima Classe

La concorrenza non è un ripensamento in Hemlock. È integrata nel linguaggio dalle fondamenta.

**Caratteristiche chiave:**
- `async`/`await` integrati nel linguaggio
- Canali per la comunicazione
- `spawn`/`join`/`detach` per la gestione dei task
- Nessun thread grezzo, nessun lock - solo strutturato
- Vero parallelismo multi-thread usando thread POSIX

**Non un event loop o green thread** - Hemlock usa veri thread del sistema operativo per un vero parallelismo su più core CPU.

### 5. Sintassi Simile al C, Poca Cerimonia

Hemlock dovrebbe risultare familiare ai programmatori di sistemi riducendo il boilerplate.

**Scelte di progettazione:**
- Blocchi `{}` sempre, nessuna parentesi opzionale
- Gli operatori corrispondono al C: `+`, `-`, `*`, `/`, `&&`, `||`, `!`
- La sintassi dei tipi corrisponde a Rust/TypeScript: `let x: tipo = valore;`
- Le funzioni sono valori di prima classe
- Parole chiave e forme speciali minimali

---

## Filosofia sulla Sicurezza

**La posizione di Hemlock sulla sicurezza:**

> "Ti diamo gli strumenti per essere sicuro (`buffer`, annotazioni di tipo, controllo dei limiti) ma non ti obblighiamo a usarli (`ptr`, memoria manuale, operazioni non sicure).
>
> Il default dovrebbe guidare verso la sicurezza, ma la via d'uscita dovrebbe essere sempre disponibile."

### Strumenti di Sicurezza Forniti

**1. Tipo buffer sicuro:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // controllo dei limiti
print(b.length);        // 64
free(b);                // ancora manuale
```

**2. Puntatori grezzi non sicuri:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Devi ricordarti di liberare
```

**3. Annotazioni di tipo:**
```hemlock
let x: u8 = 255;   // OK
let y: u8 = 256;   // ERRORE: fuori intervallo
```

**4. Controllo dei tipi a runtime:**
```hemlock
let val = qualche_funzione();
if (typeof(val) == "i32") {
    // Sicuro da usare come intero
}
```

### Principi Guida

1. **Default a pattern sicuri nella documentazione** - Mostra `buffer` prima di `ptr`, incoraggia le annotazioni di tipo
2. **Rendi ovvie le operazioni non sicure** - L'aritmetica dei puntatori grezzi dovrebbe sembrare intenzionale
3. **Fornisci vie d'uscita** - Non impedire agli utenti esperti di fare lavoro a basso livello
4. **Sii onesto sui compromessi** - Documenta cosa può andare storto

### Esempi di Sicurezza vs. Non Sicurezza

| Pattern Sicuro | Pattern Non Sicuro | Quando Usare Non Sicuro |
|----------------|-------------------|------------------------|
| tipo `buffer` | tipo `ptr` | FFI, codice critico per le prestazioni |
| Annotazioni di tipo | Nessuna annotazione | Interfacce esterne, validazione |
| Accesso con controllo limiti | Aritmetica puntatori | Operazioni memoria a basso livello |
| Gestione eccezioni | Restituzione null/codici errore | Quando le eccezioni sono troppo pesanti |

---

## Cosa NON Aggiungere

Capire cosa **non** aggiungere è importante quanto sapere cosa aggiungere.

### Non Aggiungere Comportamento Implicito

**Esempi negativi:**

```hemlock
// MALE: Inserzione automatica punto e virgola
let x = 5
let y = 10

// MALE: Conversioni di tipo implicite che perdono precisione
let x: i32 = 3.14  // Dovrebbe troncare o dare errore?
```

**Perché:** Il comportamento implicito crea sorprese e rende il codice più difficile da ragionare.

### Non Nascondere la Complessità

**Esempi negativi:**

```hemlock
// MALE: Ottimizzazione magica dietro le quinte
let arr = [1, 2, 3]  // È sullo stack o nell'heap? L'utente dovrebbe saperlo! (Heap, refcounted)

// MALE: Puntatore grezzo liberato automaticamente
let p = alloc(100)  // Si libera automaticamente? NO! I ptr grezzi richiedono sempre free()
```

**Nota sul refcounting:** Hemlock usa il refcounting interno per stringhe, array, oggetti e buffer - questi SONO liberati automaticamente quando lo scope esce. Questo è esplicito e prevedibile (pulizia deterministica quando ref raggiunge 0, nessuna pausa GC). I puntatori grezzi (`ptr` da `alloc()`) NON sono refcounted e richiedono sempre `free()` manuale.

**Perché:** La complessità nascosta rende impossibile prevedere le prestazioni e debuggare i problemi.

### Non Rompere la Semantica Esistente

**Non cambiare mai queste decisioni fondamentali:**
- I punti e virgola sono obbligatori - non renderli opzionali
- Gestione manuale della memoria - non aggiungere GC
- Stringhe mutabili - non renderle immutabili
- Controllo dei tipi a runtime - non rimuoverlo

**Perché:** Consistenza e stabilità sono più importanti delle funzionalità alla moda.

### Non Aggiungere Funzionalità "Comode" Che Riducono l'Esplicitezza

**Esempi di funzionalità da evitare:**
- Overloading degli operatori (forse per tipi utente, ma con attenzione)
- Coercizione di tipo implicita che perde informazioni
- Pulizia automatica delle risorse (RAII)
- Concatenamento di metodi che nasconde complessità
- DSL e sintassi magica

**Eccezione:** Le funzionalità comode vanno bene se sono **zucchero sintattico esplicito** su operazioni semplici:
- `else if` va bene (sono solo istruzioni if annidate)
- L'interpolazione di stringhe potrebbe andare bene se è chiaramente zucchero sintattico
- La sintassi dei metodi per gli oggetti va bene (è esplicito cosa fa)

---

## Considerazioni Future

### Forse Aggiungere (In Discussione)

Queste funzionalità si allineano con la filosofia di Hemlock ma necessitano di progettazione attenta:

**1. Pattern matching**
```hemlock
match (valore) {
    case i32: print("intero");
    case string: print("testo");
    case _: print("altro");
}
```
- Controllo dei tipi esplicito
- Nessun costo nascosto
- Possibile controllo esaustività a compile-time

**2. Tipi errore (`Result<T, E>`)**
```hemlock
fn dividi(a: i32, b: i32): Result<i32, string> {
    if (b == 0) {
        return Err("divisione per zero");
    }
    return Ok(a / b);
}
```
- Gestione errori esplicita
- Forza gli utenti a pensare agli errori
- Alternativa alle eccezioni

**3. Tipi array/slice**
- Abbiamo già array dinamici
- Potremmo aggiungere array di dimensione fissa per allocazione sullo stack
- Dovrebbe essere esplicito su stack vs. heap

**4. Strumenti di sicurezza memoria migliorati**
- Flag opzionale per controllo limiti
- Rilevamento memory leak nelle build di debug
- Integrazione sanitizer

### Probabilmente Mai Aggiungere

Queste funzionalità violano i principi fondamentali:

**1. Garbage collection**
- Nasconde la complessità della gestione memoria
- Prestazioni imprevedibili
- Contro il principio del controllo esplicito

**2. Gestione automatica della memoria**
- Stesse ragioni del GC
- Il reference counting potrebbe andare bene se esplicito

**3. Conversioni di tipo implicite che perdono dati**
- Va contro "esplicito su implicito"
- Fonte di bug sottili

**4. Macro (complesse)**
- Troppa potenza, troppa complessità
- Un sistema macro semplice potrebbe andare bene
- Preferisci generazione di codice o funzioni

**5. OOP basata su classi con ereditarietà**
- Troppo comportamento implicito
- Duck typing e oggetti sono sufficienti
- Composizione su ereditarietà

**6. Sistema di moduli con risoluzione complessa**
- Mantieni gli import semplici ed espliciti
- Nessun percorso di ricerca magico
- Nessuna risoluzione versioni (usa il package manager del sistema operativo)

---

## Riflessioni Finali

### Fiducia e Responsabilità

Hemlock riguarda **fiducia e responsabilità**. Ci fidiamo del programmatore per:

- Gestire la memoria correttamente
- Usare i tipi appropriatamente
- Gestire gli errori propriamente
- Capire i compromessi

In cambio, Hemlock fornisce:

- Nessun costo nascosto
- Nessun comportamento sorprendente
- Controllo completo quando necessario
- Strumenti di sicurezza quando voluti

### La Domanda Guida

**Quando si considera una nuova funzionalità, chiedi:**

> "Questo dà al programmatore più controllo esplicito, o nasconde qualcosa?"

- Se **aggiunge controllo esplicito** → probabilmente adatto a Hemlock
- Se **nasconde complessità** → probabilmente non appartiene
- Se è **zucchero opzionale** chiaramente documentato → potrebbe andare bene

### Esempi di Buone Aggiunte

- **Istruzioni switch** - Flusso di controllo esplicito, nessuna magia, semantica chiara

- **Async/await con pthread** - Concorrenza esplicita, vero parallelismo, l'utente controlla lo spawning

- **Tipo buffer insieme a ptr** - Dà scelta tra sicuro e non sicuro

- **Annotazioni di tipo opzionali** - Aiuta a catturare bug senza forzare rigidità

- **Try/catch/finally** - Gestione errori esplicita con flusso di controllo chiaro

### Esempi di Cattive Aggiunte

- **Inserzione automatica punto e virgola** - Nasconde errori di sintassi, rende il codice ambiguo

- **RAII/distruttori** - Pulizia automatica nasconde quando le risorse vengono rilasciate

- **Null coalescing implicito** - Nasconde i controlli null, rende il codice più difficile da ragionare

- **Stringhe che crescono automaticamente** - Nasconde allocazione memoria, prestazioni imprevedibili

---

## Conclusione

Hemlock non cerca di essere il linguaggio più sicuro, il più veloce, o il più ricco di funzionalità.

**Hemlock cerca di essere il linguaggio più *onesto*.**

Ti dice esattamente cosa sta facendo, ti dà controllo quando ne hai bisogno, e non nasconde gli spigoli affilati. È un linguaggio per persone che vogliono capire il loro codice a basso livello godendo comunque di ergonomia moderna.

Se non sei sicuro se una funzionalità appartiene a Hemlock, ricorda:

> **Esplicito su implicito, sempre.**
> **Non sicuro è una caratteristica, non un bug.**
> **L'utente è responsabile, e va bene così.**
