# Gestione dei Segnali in Hemlock

Hemlock fornisce **gestione dei segnali POSIX** per gestire segnali di sistema come SIGINT (Ctrl+C), SIGTERM e segnali personalizzati. Questo abilita il controllo di processo a basso livello e la comunicazione inter-processo.

## Indice

- [Panoramica](#panoramica)
- [API Segnali](#api-segnali)
- [Costanti dei Segnali](#costanti-dei-segnali)
- [Gestione Base dei Segnali](#gestione-base-dei-segnali)
- [Pattern Avanzati](#pattern-avanzati)
- [Comportamento del Gestore di Segnali](#comportamento-del-gestore-di-segnali)
- [Considerazioni sulla Sicurezza](#considerazioni-sulla-sicurezza)
- [Casi d'Uso Comuni](#casi-duso-comuni)
- [Esempi Completi](#esempi-completi)

## Panoramica

La gestione dei segnali permette ai programmi di:
- Rispondere a interruzioni dell'utente (Ctrl+C, Ctrl+Z)
- Implementare shutdown graceful
- Gestire richieste di terminazione
- Usare segnali personalizzati per comunicazione inter-processo
- Creare meccanismi di alarm/timer

**Importante:** La gestione dei segnali e **intrinsecamente unsafe** nella filosofia di Hemlock. I gestori possono essere chiamati in qualsiasi momento, interrompendo l'esecuzione normale. L'utente e responsabile della corretta sincronizzazione.

## API Segnali

### signal(signum, funzione_gestore)

Registra una funzione gestore di segnali.

**Parametri:**
- `signum` (i32) - Numero del segnale (costante come SIGINT, SIGTERM)
- `funzione_gestore` (funzione o null) - Funzione da chiamare quando il segnale viene ricevuto, o `null` per ripristinare il predefinito

**Restituisce:** La precedente funzione gestore (o `null` se nessuna)

**Esempio:**
```hemlock
fn mio_gestore(sig) {
    print("Catturato segnale: " + typeof(sig));
}

let vecchio_gestore = signal(SIGINT, mio_gestore);
```

**Ripristino al predefinito:**
```hemlock
signal(SIGINT, null);  // Ripristina SIGINT al comportamento predefinito
```

### raise(signum)

Invia un segnale al processo corrente.

**Parametri:**
- `signum` (i32) - Numero del segnale da inviare

**Restituisce:** `null`

**Esempio:**
```hemlock
raise(SIGUSR1);  // Attiva il gestore SIGUSR1
```

## Costanti dei Segnali

Hemlock fornisce costanti di segnali POSIX standard come valori i32.

### Interruzione e Terminazione

| Costante | Valore | Descrizione | Trigger Comune |
|----------|--------|-------------|----------------|
| `SIGINT` | 2 | Interrupt da tastiera | Ctrl+C |
| `SIGTERM` | 15 | Richiesta di terminazione | Comando `kill` |
| `SIGQUIT` | 3 | Quit da tastiera | Ctrl+\ |
| `SIGHUP` | 1 | Hangup rilevato | Terminale chiuso |
| `SIGABRT` | 6 | Segnale abort | Funzione `abort()` |

**Esempi:**
```hemlock
signal(SIGINT, gestisci_interrupt);   // Ctrl+C
signal(SIGTERM, gestisci_termina);    // Comando kill
signal(SIGHUP, gestisci_hangup);      // Terminale si chiude
```

### Segnali Definiti dall'Utente

| Costante | Valore | Descrizione | Caso d'Uso |
|----------|--------|-------------|------------|
| `SIGUSR1` | 10 | Segnale definito dall'utente 1 | IPC personalizzato |
| `SIGUSR2` | 12 | Segnale definito dall'utente 2 | IPC personalizzato |

**Esempi:**
```hemlock
// Usa per comunicazione personalizzata
signal(SIGUSR1, ricarica_config);
signal(SIGUSR2, ruota_log);
```

### Controllo Processo

| Costante | Valore | Descrizione | Note |
|----------|--------|-------------|------|
| `SIGALRM` | 14 | Timer alarm | Dopo `alarm()` |
| `SIGCHLD` | 17 | Cambio stato processo figlio | Gestione processi |
| `SIGCONT` | 18 | Continua se fermato | Riprendi dopo SIGSTOP |
| `SIGSTOP` | 19 | Ferma processo | **Non puo essere catturato** |
| `SIGTSTP` | 20 | Stop da terminale | Ctrl+Z |

**Esempi:**
```hemlock
signal(SIGALRM, gestisci_timeout);
signal(SIGCHLD, gestisci_uscita_figlio);
```

### Segnali I/O

| Costante | Valore | Descrizione | Quando Inviato |
|----------|--------|-------------|----------------|
| `SIGPIPE` | 13 | Pipe rotta | Scrittura su pipe chiusa |
| `SIGTTIN` | 21 | Lettura background da terminale | Processo BG legge TTY |
| `SIGTTOU` | 22 | Scrittura background a terminale | Processo BG scrive TTY |

**Esempi:**
```hemlock
signal(SIGPIPE, gestisci_pipe_rotta);
```

## Gestione Base dei Segnali

### Catturare Ctrl+C

```hemlock
let interrotto = false;

fn gestisci_interrupt(sig) {
    print("Catturato SIGINT!");
    interrotto = true;
}

signal(SIGINT, gestisci_interrupt);

// Il programma continua l'esecuzione...
// L'utente preme Ctrl+C -> gestisci_interrupt() viene chiamato

while (!interrotto) {
    // Fai lavoro...
}

print("Uscita per interrupt");
```

### Firma della Funzione Gestore

I gestori di segnali ricevono un argomento: il numero del segnale (i32)

```hemlock
fn mio_gestore(signum) {
    print("Ricevuto segnale: " + typeof(signum));
    // signum contiene il numero del segnale (es. 2 per SIGINT)

    if (signum == SIGINT) {
        print("Questo e SIGINT");
    }
}

signal(SIGINT, mio_gestore);
signal(SIGTERM, mio_gestore);  // Stesso gestore per segnali multipli
```

### Gestori di Segnali Multipli

Gestori diversi per segnali diversi:

```hemlock
fn gestisci_int(sig) {
    print("SIGINT ricevuto");
}

fn gestisci_term(sig) {
    print("SIGTERM ricevuto");
}

fn gestisci_usr1(sig) {
    print("SIGUSR1 ricevuto");
}

signal(SIGINT, gestisci_int);
signal(SIGTERM, gestisci_term);
signal(SIGUSR1, gestisci_usr1);
```

### Ripristino al Comportamento Predefinito

Passa `null` come gestore per ripristinare il comportamento predefinito:

```hemlock
// Registra gestore personalizzato
signal(SIGINT, mio_gestore);

// Dopo, ripristina al predefinito (termina su SIGINT)
signal(SIGINT, null);
```

### Invio Manuale di Segnali

Invia segnali al tuo stesso processo:

```hemlock
let conteggio = 0;

fn incrementa(sig) {
    conteggio = conteggio + 1;
}

signal(SIGUSR1, incrementa);

// Attiva gestore manualmente
raise(SIGUSR1);
raise(SIGUSR1);

print(conteggio);  // 2
```

## Pattern Avanzati

### Pattern Shutdown Graceful

Pattern comune per pulizia alla terminazione:

```hemlock
let deve_uscire = false;

fn gestisci_shutdown(sig) {
    print("Shutdown graceful in corso...");
    deve_uscire = true;
}

signal(SIGINT, gestisci_shutdown);
signal(SIGTERM, gestisci_shutdown);

// Loop principale
while (!deve_uscire) {
    // Fai lavoro...
    // Controlla flag deve_uscire periodicamente
}

print("Pulizia completata");
```

### Contatore di Segnali

Traccia numero di segnali ricevuti:

```hemlock
let conteggio_segnali = 0;

fn conta_segnali(sig) {
    conteggio_segnali = conteggio_segnali + 1;
    print("Ricevuti " + typeof(conteggio_segnali) + " segnali");
}

signal(SIGUSR1, conta_segnali);

// Dopo...
print("Segnali totali: " + typeof(conteggio_segnali));
```

### Ricarica Configurazione su Segnale

```hemlock
let config = carica_config();

fn ricarica_config(sig) {
    print("Ricarica configurazione in corso...");
    config = carica_config();
    print("Configurazione ricaricata");
}

signal(SIGHUP, ricarica_config);  // Ricarica su SIGHUP

// Invia SIGHUP al processo per ricaricare config
// Da shell: kill -HUP <pid>
```

### Timeout Usando SIGALRM

```hemlock
let scaduto = false;

fn gestisci_alarm(sig) {
    print("Timeout!");
    scaduto = true;
}

signal(SIGALRM, gestisci_alarm);

// Imposta alarm (non ancora implementato in Hemlock, solo esempio)
// alarm(5);  // timeout 5 secondi

while (!scaduto) {
    // Fai lavoro con timeout
}
```

### Macchina a Stati Basata su Segnali

```hemlock
let stato = 0;

fn stato_successivo(sig) {
    stato = (stato + 1) % 3;
    print("Stato: " + typeof(stato));
}

fn stato_precedente(sig) {
    stato = (stato - 1 + 3) % 3;
    print("Stato: " + typeof(stato));
}

signal(SIGUSR1, stato_successivo);  // Avanza stato
signal(SIGUSR2, stato_precedente);  // Torna indietro

// Controlla macchina a stati:
// kill -USR1 <pid>  # Stato successivo
// kill -USR2 <pid>  # Stato precedente
```

## Comportamento del Gestore di Segnali

### Note Importanti

**Esecuzione del Gestore:**
- I gestori sono chiamati **sincronamente** quando il segnale viene ricevuto
- I gestori vengono eseguiti nel contesto del processo corrente
- I gestori di segnali condividono l'ambiente closure della funzione in cui sono definiti
- I gestori possono accedere e modificare variabili dello scope esterno (come globali o variabili catturate)

**Migliori Pratiche:**
- Mantieni i gestori semplici e veloci - evita operazioni a lunga esecuzione
- Imposta flag piuttosto che eseguire logica complessa
- Evita di chiamare funzioni che potrebbero prendere lock
- Sii consapevole che i gestori possono interrompere qualsiasi operazione

### Quali Segnali Possono Essere Catturati

**Possono essere catturati e gestiti:**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (ma il programma abortira dopo che il gestore ritorna)

**Non possono essere catturati:**
- `SIGKILL` (9) - Termina sempre il processo
- `SIGSTOP` (19) - Ferma sempre il processo

**Dipendenti dal sistema:**
- Alcuni segnali hanno comportamenti predefiniti che possono differire per sistema
- Controlla la documentazione dei segnali della tua piattaforma per specifiche

### Limitazioni dei Gestori

```hemlock
fn gestore_complesso(sig) {
    // Evita questi nei gestori di segnali:

    // ❌ Operazioni a lunga esecuzione
    // elabora_file_grande();

    // ❌ I/O bloccante
    // let f = open("log.txt", "a");
    // f.write("Segnale ricevuto\n");

    // ❌ Cambiamenti di stato complessi
    // ricostruisci_intera_struttura_dati();

    // ✓ Semplice impostazione flag e sicura
    let deve_fermarsi = true;

    // ✓ Semplici aggiornamenti contatore sono generalmente sicuri
    let conteggio_segnali = conteggio_segnali + 1;
}
```

## Considerazioni sulla Sicurezza

La gestione dei segnali e **intrinsecamente unsafe** nella filosofia di Hemlock.

### Race Condition

I gestori possono essere chiamati in qualsiasi momento, interrompendo l'esecuzione normale:

```hemlock
let contatore = 0;

fn incrementa(sig) {
    contatore = contatore + 1;  // Race condition se chiamato durante aggiornamento contatore
}

signal(SIGUSR1, incrementa);

// Il codice principale modifica anche il contatore
contatore = contatore + 1;  // Potrebbe essere interrotto dal gestore di segnali
```

**Problema:** Se il segnale arriva mentre il codice principale sta aggiornando `contatore`, il risultato e imprevedibile.

### Async-Signal-Safety

Hemlock **non** garantisce async-signal-safety:
- I gestori possono chiamare qualsiasi codice Hemlock (a differenza delle funzioni C async-signal-safe limitate)
- Questo fornisce flessibilita ma richiede cautela dell'utente
- Race condition sono possibili se il gestore modifica stato condiviso

### Migliori Pratiche per Gestione Segnali Sicura

**1. Usa Flag Atomici**

Semplici assegnazioni booleane sono generalmente sicure:

```hemlock
let deve_uscire = false;

fn gestore(sig) {
    deve_uscire = true;  // Semplice assegnazione e sicura
}

signal(SIGINT, gestore);

while (!deve_uscire) {
    // lavoro...
}
```

**2. Minimizza Stato Condiviso**

```hemlock
let conteggio_interrupt = 0;

fn gestore(sig) {
    // Modifica solo questa variabile
    conteggio_interrupt = conteggio_interrupt + 1;
}
```

**3. Rinvia Operazioni Complesse**

```hemlock
let ricarica_pendente = false;

fn segnala_ricarica(sig) {
    ricarica_pendente = true;  // Solo imposta flag
}

signal(SIGHUP, segnala_ricarica);

// Nel loop principale:
while (true) {
    if (ricarica_pendente) {
        ricarica_config();  // Fai lavoro complesso qui
        ricarica_pendente = false;
    }

    // Lavoro normale...
}
```

**4. Evita Problemi di Rientranza**

```hemlock
let in_sezione_critica = false;
let dati = [];

fn gestore_attento(sig) {
    if (in_sezione_critica) {
        // Non modificare dati mentre il codice principale li sta usando
        return;
    }
    // Sicuro procedere
}
```

## Casi d'Uso Comuni

### 1. Shutdown Graceful del Server

```hemlock
let in_esecuzione = true;

fn shutdown(sig) {
    print("Segnale shutdown ricevuto");
    in_esecuzione = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Loop principale server
while (in_esecuzione) {
    gestisci_richiesta_client();
}

pulisci_risorse();
print("Server fermato");
```

### 2. Ricarica Configurazione (Senza Riavvio)

```hemlock
let config = carica_config("app.conf");
let ricarica_necessaria = false;

fn attiva_ricarica(sig) {
    ricarica_necessaria = true;
}

signal(SIGHUP, attiva_ricarica);

while (true) {
    if (ricarica_necessaria) {
        print("Ricarica configurazione in corso...");
        config = carica_config("app.conf");
        ricarica_necessaria = false;
    }

    // Usa config...
}
```

### 3. Rotazione Log

```hemlock
let file_log = open("app.log", "a");
let rotazione_necessaria = false;

fn attiva_rotazione(sig) {
    rotazione_necessaria = true;
}

signal(SIGUSR1, attiva_rotazione);

while (true) {
    if (rotazione_necessaria) {
        file_log.close();
        // Rinomina vecchio log, apri nuovo
        exec("mv app.log app.log.old");
        file_log = open("app.log", "a");
        rotazione_necessaria = false;
    }

    // Logging normale...
    file_log.write("Voce log\n");
}
```

### 4. Report di Stato

```hemlock
let richieste_gestite = 0;

fn riporta_stato(sig) {
    print("Stato: " + typeof(richieste_gestite) + " richieste gestite");
}

signal(SIGUSR1, riporta_stato);

while (true) {
    gestisci_richiesta();
    richieste_gestite = richieste_gestite + 1;
}

// Da shell: kill -USR1 <pid>
```

### 5. Toggle Modalita Debug

```hemlock
let modalita_debug = false;

fn toggle_debug(sig) {
    modalita_debug = !modalita_debug;
    if (modalita_debug) {
        print("Modalita debug: ON");
    } else {
        print("Modalita debug: OFF");
    }
}

signal(SIGUSR2, toggle_debug);

// Da shell: kill -USR2 <pid> per toggle
```

## Esempi Completi

### Esempio 1: Gestore Interrupt con Pulizia

```hemlock
let in_esecuzione = true;
let conteggio_segnali = 0;

fn gestisci_segnale(signum) {
    conteggio_segnali = conteggio_segnali + 1;

    if (signum == SIGINT) {
        print("Interrupt rilevato (Ctrl+C)");
        in_esecuzione = false;
    }

    if (signum == SIGUSR1) {
        print("Segnale utente 1 ricevuto");
    }
}

// Registra gestori
signal(SIGINT, gestisci_segnale);
signal(SIGUSR1, gestisci_segnale);

// Simula del lavoro
let i = 0;
while (in_esecuzione && i < 100) {
    print("Lavoro in corso... " + typeof(i));

    // Attiva SIGUSR1 ogni 10 iterazioni
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Segnali totali ricevuti: " + typeof(conteggio_segnali));
```

### Esempio 2: Macchina a Stati Multi-Segnale

```hemlock
let stato = "idle";
let conteggio_richieste = 0;

fn inizia_elaborazione(sig) {
    stato = "elaborazione";
    print("Stato: " + stato);
}

fn ferma_elaborazione(sig) {
    stato = "idle";
    print("Stato: " + stato);
}

fn riporta_statistiche(sig) {
    print("Stato: " + stato);
    print("Richieste: " + typeof(conteggio_richieste));
}

signal(SIGUSR1, inizia_elaborazione);
signal(SIGUSR2, ferma_elaborazione);
signal(SIGHUP, riporta_statistiche);

while (true) {
    if (stato == "elaborazione") {
        // Fai lavoro
        conteggio_richieste = conteggio_richieste + 1;
    }

    // Controlla ogni iterazione...
}
```

### Esempio 3: Controller Pool di Worker

```hemlock
let conteggio_worker = 4;
let deve_uscire = false;

fn aumenta_worker(sig) {
    conteggio_worker = conteggio_worker + 1;
    print("Worker: " + typeof(conteggio_worker));
}

fn diminuisci_worker(sig) {
    if (conteggio_worker > 1) {
        conteggio_worker = conteggio_worker - 1;
    }
    print("Worker: " + typeof(conteggio_worker));
}

fn shutdown(sig) {
    print("Shutdown in corso...");
    deve_uscire = true;
}

signal(SIGUSR1, aumenta_worker);
signal(SIGUSR2, diminuisci_worker);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Il loop principale regola il pool worker basandosi su conteggio_worker
while (!deve_uscire) {
    // Gestisci worker basandoti su conteggio_worker
    // ...
}
```

### Esempio 4: Pattern Timeout

```hemlock
let operazione_completata = false;
let scaduto = false;

fn gestore_timeout(sig) {
    scaduto = true;
}

signal(SIGALRM, gestore_timeout);

// Avvia operazione lunga
async fn operazione_lunga() {
    // ... lavoro
    operazione_completata = true;
}

let task = spawn(operazione_lunga);

// Attendi con timeout (controllo manuale)
let trascorso = 0;
while (!operazione_completata && trascorso < 1000) {
    // Sleep o controlla
    trascorso = trascorso + 1;
}

if (!operazione_completata) {
    print("Operazione scaduta");
    detach(task);  // Rinuncia ad aspettare
} else {
    join(task);
    print("Operazione completata");
}
```

## Debug dei Gestori di Segnali

### Aggiungi Print Diagnostici

```hemlock
fn gestore_debug(sig) {
    print("Gestore chiamato per segnale: " + typeof(sig));
    print("Stack: (non ancora disponibile)");

    // La tua logica del gestore...
}

signal(SIGINT, gestore_debug);
```

### Conta Chiamate al Gestore

```hemlock
let chiamate_gestore = 0;

fn gestore_contatore(sig) {
    chiamate_gestore = chiamate_gestore + 1;
    print("Chiamata gestore #" + typeof(chiamate_gestore));

    // La tua logica del gestore...
}
```

### Testa con raise()

```hemlock
fn gestore_test(sig) {
    print("Segnale test ricevuto: " + typeof(sig));
}

signal(SIGUSR1, gestore_test);

// Testa invocando manualmente
raise(SIGUSR1);
print("Il gestore avrebbe dovuto essere chiamato");
```

## Riepilogo

La gestione dei segnali di Hemlock fornisce:

- Gestione segnali POSIX per controllo processo a basso livello
- 15 costanti segnali standard
- Semplice API signal() e raise()
- Funzioni gestore flessibili con supporto closure
- Segnali multipli possono condividere gestori

Ricorda:
- La gestione dei segnali e intrinsecamente unsafe - usare con cautela
- Mantieni i gestori semplici e veloci
- Usa flag per cambiamenti di stato, non operazioni complesse
- I gestori possono interrompere l'esecuzione in qualsiasi momento
- Non si possono catturare SIGKILL o SIGSTOP
- Testa i gestori accuratamente con raise()

Pattern comuni:
- Shutdown graceful (SIGINT, SIGTERM)
- Ricarica configurazione (SIGHUP)
- Rotazione log (SIGUSR1)
- Report di stato (SIGUSR1/SIGUSR2)
- Toggle modalita debug (SIGUSR2)
