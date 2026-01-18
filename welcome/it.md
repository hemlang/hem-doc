# Benvenuto in Hemlock

> "Un piccolo linguaggio non sicuro per scrivere cose non sicure in modo sicuro."

**Hemlock** è un linguaggio di scripting di sistema che combina la potenza del C con l'ergonomia dei moderni linguaggi di scripting. Offre gestione manuale della memoria, controllo esplicito e concorrenza asincrona strutturata integrata.

## Cos'è Hemlock?

Hemlock è progettato per programmatori che vogliono:

- **Controllo esplicito** sulla memoria e l'esecuzione
- **Sintassi simile al C** con comodità moderne
- **Nessun comportamento nascosto** o magia
- **Vera concorrenza asincrona parallela** con concorrenza basata su pthread

Hemlock NON è un linguaggio a memoria sicura con garbage collection. Invece, ti fornisce gli strumenti per essere sicuro (`buffer`, annotazioni di tipo, controllo dei limiti) senza obbligarti a usarli (`ptr`, memoria manuale, operazioni non sicure).

## Esempio Rapido

```hemlock
// Ciao, Hemlock!
fn greet(name: string): string {
    return `Ciao, ${name}!`;
}

let message = greet("Mondo");
print(message);

// Gestione manuale della memoria
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Funzionalità in Breve

| Funzionalità | Descrizione |
|--------------|-------------|
| **Sistema di Tipi** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Memoria** | Gestione manuale con `alloc()`, `buffer()`, `free()` |
| **Async** | `async`/`await` integrato con vero parallelismo pthread |
| **FFI** | Chiamare funzioni C direttamente da librerie condivise |
| **Libreria Standard** | 40 moduli inclusi crypto, http, sqlite, json e altro |

## Primi Passi

Pronto a iniziare? Ecco come cominciare:

1. **[Installazione](#getting-started-installation)** - Scarica e configura Hemlock
2. **[Avvio Rapido](#getting-started-quick-start)** - Scrivi il tuo primo programma in pochi minuti
3. **[Tutorial](#getting-started-tutorial)** - Impara Hemlock passo dopo passo

## Sezioni della Documentazione

- **Primi Passi** - Installazione, guida all'avvio rapido e tutorial
- **Guida al Linguaggio** - Approfondimento su sintassi, tipi, funzioni e altro
- **Argomenti Avanzati** - Programmazione asincrona, FFI, segnali e atomiche
- **Riferimento API** - Riferimento completo per le funzioni integrate e la libreria standard
- **Design e Filosofia** - Comprendere perché Hemlock è così com'è

## Gestore di Pacchetti

Hemlock include **hpm**, un gestore di pacchetti per gestire le dipendenze:

```bash
hpm init mio-progetto
hpm add un-pacchetto
hpm run
```

Consulta le sezioni della documentazione di hpm per maggiori dettagli.

---

Usa la navigazione a sinistra per esplorare la documentazione, oppure usa la barra di ricerca per trovare argomenti specifici.
