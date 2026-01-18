# Esecuzione di Comandi in Hemlock

Hemlock fornisce la **funzione built-in `exec()`** per eseguire comandi shell e catturare il loro output.

## Indice

- [Panoramica](#panoramica)
- [La Funzione exec()](#la-funzione-exec)
- [Oggetto Risultato](#oggetto-risultato)
- [Uso Base](#uso-base)
- [Esempi Avanzati](#esempi-avanzati)
- [Gestione degli Errori](#gestione-degli-errori)
- [Dettagli di Implementazione](#dettagli-di-implementazione)
- [Considerazioni sulla Sicurezza](#considerazioni-sulla-sicurezza)
- [Limitazioni](#limitazioni)
- [Casi d'Uso](#casi-duso)
- [Migliori Pratiche](#migliori-pratiche)
- [Esempi Completi](#esempi-completi)

## Panoramica

La funzione `exec()` permette ai programmi Hemlock di:
- Eseguire comandi shell
- Catturare lo standard output (stdout)
- Controllare i codici di stato di uscita
- Usare funzionalita della shell (pipe, redirect, ecc.)
- Integrarsi con utilita di sistema

**Importante:** I comandi vengono eseguiti tramite `/bin/sh`, fornendo capacita complete della shell ma introducendo anche considerazioni sulla sicurezza.

## La Funzione exec()

### Firma

```hemlock
exec(comando: string): object
```

**Parametri:**
- `comando` (string) - Comando shell da eseguire

**Restituisce:** Un oggetto con due campi:
- `output` (string) - L'output stdout del comando
- `exit_code` (i32) - Il codice di stato di uscita del comando

### Esempio Base

```hemlock
let risultato = exec("echo ciao");
print(risultato.output);      // "ciao\n"
print(risultato.exit_code);   // 0
```

## Oggetto Risultato

L'oggetto restituito da `exec()` ha la seguente struttura:

```hemlock
{
    output: string,      // Stdout del comando (output catturato)
    exit_code: i32       // Stato di uscita del processo (0 = successo)
}
```

### Campo output

Contiene tutto il testo scritto su stdout dal comando.

**Proprieta:**
- Stringa vuota se il comando non produce output
- Include newline e spazi cosi come sono
- Output multi-linea preservato
- Nessun limite di dimensione (allocato dinamicamente)

**Esempi:**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Lista directory con newline

let r3 = exec("true");
print(r3.output);  // "" (stringa vuota)
```

### Campo exit_code

Il codice di stato di uscita del comando.

**Valori:**
- `0` tipicamente indica successo
- `1-255` indicano errori (la convenzione varia per comando)
- `-1` se il comando non ha potuto essere eseguito o e terminato in modo anomalo

**Esempi:**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (successo)

let r2 = exec("false");
print(r2.exit_code);  // 1 (fallimento)

let r3 = exec("ls /inesistente");
print(r3.exit_code);  // 2 (file non trovato, varia per comando)
```

## Uso Base

### Comando Semplice

```hemlock
let r = exec("ls -la");
print(r.output);
print("Codice di uscita: " + typeof(r.exit_code));
```

### Controllo Stato di Uscita

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Trovato: " + r.output);
} else {
    print("Pattern non trovato");
}
```

### Comandi con Pipe

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Comandi Multipli

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Sostituzione di Comando

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Data corrente
```

## Esempi Avanzati

### Gestione dei Fallimenti

```hemlock
let r = exec("ls /inesistente");
if (r.exit_code != 0) {
    print("Comando fallito con codice: " + typeof(r.exit_code));
    print("Output errore: " + r.output);  // Nota: stderr non catturato
}
```

### Elaborazione di Output Multi-Linea

```hemlock
let r = exec("cat file.txt");
let righe = r.output.split("\n");
let i = 0;
while (i < righe.length) {
    print("Riga " + typeof(i) + ": " + righe[i]);
    i = i + 1;
}
```

### Concatenamento di Comandi

**Con && (AND):**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup completato");
}
```

**Con || (OR):**
```hemlock
let r = exec("comando1 || comando2");
// Esegue comando2 solo se comando1 fallisce
```

**Con ; (sequenza):**
```hemlock
let r = exec("comando1; comando2");
// Esegue entrambi indipendentemente da successo/fallimento
```

### Uso di Pipe

```hemlock
let r = exec("echo 'dati' | base64");
print("Base64: " + r.output);
```

**Pipeline complesse:**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Pattern di Codici di Uscita

Diversi codici di uscita indicano condizioni diverse:

```hemlock
let r = exec("test -f miofile.txt");
if (r.exit_code == 0) {
    print("Il file esiste");
} else if (r.exit_code == 1) {
    print("Il file non esiste");
} else {
    print("Comando test fallito: " + typeof(r.exit_code));
}
```

### Redirect dell'Output

```hemlock
// Redirect stdout su file (all'interno della shell)
let r1 = exec("echo 'test' > /tmp/output.txt");

// Redirect stderr su stdout (Nota: stderr comunque non catturato da Hemlock)
let r2 = exec("comando 2>&1");
```

### Variabili d'Ambiente

```hemlock
let r = exec("export VAR=valore && echo $VAR");
print(r.output);  // "valore\n"
```

### Cambi di Directory di Lavoro

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Gestione degli Errori

### Quando exec() Lancia Eccezioni

La funzione `exec()` lancia un'eccezione se il comando non puo essere eseguito:

```hemlock
try {
    let r = exec("comando_inesistente_xyz");
} catch (e) {
    print("Esecuzione fallita: " + e);
}
```

**Eccezioni lanciate quando:**
- `popen()` fallisce (es. impossibile creare pipe)
- Limiti delle risorse di sistema superati
- Fallimenti nell'allocazione di memoria

### Quando exec() NON Lancia

```hemlock
// Il comando viene eseguito ma restituisce codice di uscita non zero
let r1 = exec("false");
print(r1.exit_code);  // 1 (non un'eccezione)

// Il comando non produce output
let r2 = exec("true");
print(r2.output);  // "" (non un'eccezione)

// Comando non trovato dalla shell
let r3 = exec("cmd_inesistente");
print(r3.exit_code);  // 127 (non un'eccezione)
```

### Pattern di Esecuzione Sicura

```hemlock
fn esecuzione_sicura(comando: string) {
    try {
        let r = exec(comando);
        if (r.exit_code != 0) {
            print("Attenzione: Comando fallito con codice " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Errore nell'esecuzione del comando: " + e);
        return "";
    }
}

let output = esecuzione_sicura("ls -la");
```

## Dettagli di Implementazione

### Come Funziona

**Internamente:**
- Usa `popen()` per eseguire comandi tramite `/bin/sh`
- Cattura solo stdout (stderr non viene catturato)
- Output bufferizzato dinamicamente (inizia a 4KB, cresce se necessario)
- Stato di uscita estratto usando macro `WIFEXITED()` e `WEXITSTATUS()`
- Stringa output correttamente terminata con null

**Flusso del processo:**
1. `popen(comando, "r")` crea pipe e fa fork del processo
2. Il processo figlio esegue `/bin/sh -c "comando"`
3. Il processo padre legge stdout tramite pipe in un buffer che cresce
4. `pclose()` attende il figlio e restituisce lo stato di uscita
5. Lo stato di uscita viene estratto e memorizzato nell'oggetto risultato

### Considerazioni sulle Prestazioni

**Costi:**
- Crea un nuovo processo shell per ogni chiamata (~1-5ms di overhead)
- Output memorizzato interamente in memoria (non in streaming)
- Nessun supporto streaming (attende il completamento del comando)
- Adatto per comandi con dimensioni di output ragionevoli

**Ottimizzazioni:**
- Il buffer inizia a 4KB e raddoppia quando pieno (uso efficiente della memoria)
- Singolo ciclo di lettura minimizza le chiamate di sistema
- Nessuna copia aggiuntiva di stringhe

**Quando usare:**
- Comandi di breve durata (< 1 secondo)
- Dimensione output moderata (< 10MB)
- Operazioni batch con intervalli ragionevoli

**Quando NON usare:**
- Daemon o servizi a lunga esecuzione
- Comandi che producono gigabyte di output
- Elaborazione dati in streaming in tempo reale
- Esecuzione ad alta frequenza (> 100 chiamate/secondo)

## Considerazioni sulla Sicurezza

### Rischio di Shell Injection

**CRITICO:** I comandi vengono eseguiti dalla shell (`/bin/sh`), il che significa che **l'iniezione shell e possibile**.

**Codice vulnerabile:**
```hemlock
// PERICOLOSO - NON FARLO
let nomefile = args[1];  // Input utente
let r = exec("cat " + nomefile);  // Shell injection!
```

**Attacco:**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Esegue: cat ; rm -rf /; echo pwned
```

### Pratiche Sicure

**1. Mai usare input utente non sanitizzato:**
```hemlock
// Male
let input_utente = args[1];
let r = exec("elabora " + input_utente);  // PERICOLOSO

// Bene - valida prima
fn e_nomefile_sicuro(nome: string): bool {
    // Permetti solo alfanumerici, trattino, underscore, punto
    let i = 0;
    while (i < nome.length) {
        let c = nome[i];
        if (!(c >= 'a' && c <= 'z') &&
            !(c >= 'A' && c <= 'Z') &&
            !(c >= '0' && c <= '9') &&
            c != '-' && c != '_' && c != '.') {
            return false;
        }
        i = i + 1;
    }
    return true;
}

let nomefile = args[1];
if (e_nomefile_sicuro(nomefile)) {
    let r = exec("cat " + nomefile);
} else {
    print("Nome file non valido");
}
```

**2. Usare allowlist, non denylist:**
```hemlock
// Bene - allowlist rigorosa
let comandi_permessi = ["status", "start", "stop", "restart"];
let cmd = args[1];

let trovato = false;
for (let permesso in comandi_permessi) {
    if (cmd == permesso) {
        trovato = true;
        break;
    }
}

if (trovato) {
    exec("service miaapp " + cmd);
} else {
    print("Comando non valido");
}
```

**3. Eseguire escape dei caratteri speciali:**
```hemlock
fn shell_escape(s: string): string {
    // Escape semplice - racchiudi in apici singoli ed esegui escape degli apici singoli
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let file_utente = args[1];
let sicuro = shell_escape(file_utente);
let r = exec("cat " + sicuro);
```

**4. Evitare exec() per operazioni sui file:**
```hemlock
// Male - usa exec per operazioni sui file
let r = exec("cat file.txt");

// Bene - usa l'API file di Hemlock
let f = open("file.txt", "r");
let contenuto = f.read();
f.close();
```

### Considerazioni sui Permessi

I comandi vengono eseguiti con gli stessi permessi del processo Hemlock:

```hemlock
// Se Hemlock viene eseguito come root, i comandi exec() vengono eseguiti come root!
let r = exec("rm -rf /importante");  // PERICOLOSO se eseguito come root
```

**Migliore pratica:** Eseguire Hemlock con il minimo privilegio necessario.

## Limitazioni

### 1. Nessuna Cattura di stderr

Viene catturato solo stdout, stderr va al terminale:

```hemlock
let r = exec("ls /inesistente");
// r.output e vuoto
// Messaggio di errore appare sul terminale, non catturato
```

**Workaround - redirect stderr su stdout:**
```hemlock
let r = exec("ls /inesistente 2>&1");
// Ora i messaggi di errore sono in r.output
```

### 2. Nessuno Streaming

Deve attendere il completamento del comando:

```hemlock
let r = exec("comando_lungo");
// Blocca fino al termine del comando
// Impossibile elaborare output in modo incrementale
```

### 3. Nessun Timeout

I comandi possono essere eseguiti indefinitamente:

```hemlock
let r = exec("sleep 1000");
// Blocca per 1000 secondi
// Nessun modo per fare timeout o annullare
```

**Workaround - usa comando timeout:**
```hemlock
let r = exec("timeout 5 comando_lungo");
// Fara timeout dopo 5 secondi
```

### 4. Nessuna Gestione Segnali

Impossibile inviare segnali ai comandi in esecuzione:

```hemlock
let r = exec("comando_lungo");
// Impossibile inviare SIGINT, SIGTERM, ecc. al comando
```

### 5. Nessun Controllo del Processo

Impossibile interagire con il comando dopo l'avvio:

```hemlock
let r = exec("programma_interattivo");
// Impossibile inviare input al programma
// Impossibile controllare l'esecuzione
```

## Casi d'Uso

### Buoni Casi d'Uso

**1. Esecuzione di utilita di sistema:**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /percorso -name '*.txt'");
```

**2. Elaborazione rapida di dati con strumenti Unix:**
```hemlock
let r = exec("cat dati.txt | sort | uniq | wc -l");
print("Righe uniche: " + r.output);
```

**3. Controllo stato del sistema:**
```hemlock
let r = exec("df -h");
print("Uso disco:\n" + r.output);
```

**4. Controlli esistenza file:**
```hemlock
let r = exec("test -f miofile.txt");
if (r.exit_code == 0) {
    print("Il file esiste");
}
```

**5. Generazione di report:**
```hemlock
let r = exec("ps aux | grep miaapp | wc -l");
let conteggio = r.output.trim();
print("Istanze in esecuzione: " + conteggio);
```

**6. Script di automazione:**
```hemlock
exec("git add .");
exec("git commit -m 'Commit automatico'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push fallito");
}
```

### Non Raccomandato Per

**1. Servizi a lunga esecuzione:**
```hemlock
// Male
let r = exec("nginx");  // Blocca per sempre
```

**2. Comandi interattivi:**
```hemlock
// Male - impossibile fornire input
let r = exec("ssh utente@host");
```

**3. Comandi che producono output enorme:**
```hemlock
// Male - carica intero output in memoria
let r = exec("cat file_10GB.log");
```

**4. Streaming in tempo reale:**
```hemlock
// Male - impossibile elaborare output in modo incrementale
let r = exec("tail -f /var/log/app.log");
```

**5. Gestione errori mission-critical:**
```hemlock
// Male - stderr non catturato
let r = exec("operazione_critica");
// Impossibile vedere messaggi di errore dettagliati
```

## Migliori Pratiche

### 1. Controllare Sempre i Codici di Uscita

```hemlock
let r = exec("comando_importante");
if (r.exit_code != 0) {
    print("Comando fallito!");
    // Gestisci errore
}
```

### 2. Rimuovere Spazi dall'Output Quando Necessario

```hemlock
let r = exec("echo test");
let pulito = r.output.trim();  // Rimuove newline finale
print(pulito);  // "test" (senza newline)
```

### 3. Validare Prima di Eseguire

```hemlock
fn e_comando_valido(cmd: string): bool {
    // Valida che il comando sia sicuro
    return true;  // La tua logica di validazione
}

if (e_comando_valido(cmd_utente)) {
    exec(cmd_utente);
}
```

### 4. Usare try/catch per Operazioni Critiche

```hemlock
try {
    let r = exec("comando_critico");
    if (r.exit_code != 0) {
        throw "Comando fallito";
    }
} catch (e) {
    print("Errore: " + e);
    // Pulizia o recovery
}
```

### 5. Preferire API Hemlock a exec()

```hemlock
// Male - usa exec per operazioni sui file
let r = exec("cat file.txt");

// Bene - usa l'API File di Hemlock
let f = open("file.txt", "r");
let contenuto = f.read();
f.close();
```

### 6. Catturare stderr Quando Necessario

```hemlock
// Redirect stderr su stdout
let r = exec("comando 2>&1");
// Ora r.output contiene sia stdout che stderr
```

### 7. Usare Funzionalita Shell con Saggezza

```hemlock
// Usa pipe per efficienza
let r = exec("cat grande.txt | grep pattern | head -n 10");

// Usa sostituzione di comando
let r = exec("echo Utente corrente: $(whoami)");

// Usa esecuzione condizionale
let r = exec("test -f file.txt && cat file.txt");
```

## Esempi Completi

### Esempio 1: Raccoglitore di Informazioni di Sistema

```hemlock
fn ottieni_info_sistema() {
    print("=== Informazioni Sistema ===");

    // Hostname
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // Uptime
    let r2 = exec("uptime");
    print("Uptime: " + r2.output.trim());

    // Uso disco
    let r3 = exec("df -h /");
    print("\nUso Disco:");
    print(r3.output);

    // Uso memoria
    let r4 = exec("free -h");
    print("Uso Memoria:");
    print(r4.output);
}

ottieni_info_sistema();
```

### Esempio 2: Analizzatore di Log

```hemlock
fn analizza_log(file_log: string) {
    print("Analisi log: " + file_log);

    // Conta righe totali
    let r1 = exec("wc -l " + file_log);
    print("Righe totali: " + r1.output.trim());

    // Conta errori
    let r2 = exec("grep -c ERROR " + file_log + " 2>/dev/null");
    let errori = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Errori: " + errori);
    } else {
        print("Errori: 0");
    }

    // Conta avvisi
    let r3 = exec("grep -c WARN " + file_log + " 2>/dev/null");
    let avvisi = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Avvisi: " + avvisi);
    } else {
        print("Avvisi: 0");
    }

    // Errori recenti
    print("\nErrori recenti:");
    let r4 = exec("grep ERROR " + file_log + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Uso: " + args[0] + " <file_log>");
} else {
    analizza_log(args[1]);
}
```

### Esempio 3: Helper Git

```hemlock
fn stato_git() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Errore: Non e un repository git");
        return;
    }

    if (r.output == "") {
        print("Directory di lavoro pulita");
    } else {
        print("Modifiche:");
        print(r.output);
    }
}

fn commit_veloce_git(messaggio: string) {
    print("Aggiunta di tutte le modifiche...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Errore nell'aggiunta dei file");
        return;
    }

    print("Commit in corso...");
    let msg_sicuro = messaggio.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + msg_sicuro + "'");
    if (r2.exit_code != 0) {
        print("Errore nel commit");
        return;
    }

    print("Commit eseguito con successo");
    print(r2.output);
}

// Utilizzo
stato_git();
if (args.length > 1) {
    commit_veloce_git(args[1]);
}
```

### Esempio 4: Script di Backup

```hemlock
fn backup_directory(sorgente: string, destinazione: string) {
    print("Backup di " + sorgente + " in " + destinazione);

    // Crea directory di backup
    let r1 = exec("mkdir -p " + destinazione);
    if (r1.exit_code != 0) {
        print("Errore nella creazione della directory di backup");
        return false;
    }

    // Crea tarball con timestamp
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let file_backup = destinazione + "/backup_" + timestamp + ".tar.gz";

    print("Creazione archivio: " + file_backup);
    let r3 = exec("tar -czf " + file_backup + " " + sorgente + " 2>&1");
    if (r3.exit_code != 0) {
        print("Errore nella creazione del backup:");
        print(r3.output);
        return false;
    }

    print("Backup completato con successo");

    // Mostra dimensione backup
    let r4 = exec("du -h " + file_backup);
    print("Dimensione backup: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Uso: " + args[0] + " <sorgente> <destinazione>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Riepilogo

La funzione `exec()` di Hemlock fornisce:

- Semplice esecuzione di comandi shell
- Cattura dell'output (stdout)
- Controllo dei codici di uscita
- Accesso completo alle funzionalita della shell (pipe, redirect, ecc.)
- Integrazione con utilita di sistema

Ricorda:
- Controllare sempre i codici di uscita
- Essere consapevoli delle implicazioni di sicurezza (shell injection)
- Validare l'input utente prima di usarlo nei comandi
- Preferire le API Hemlock a exec() quando disponibili
- stderr non viene catturato (usa `2>&1` per il redirect)
- I comandi bloccano fino al completamento
- Usare per utilita di breve durata, non per servizi a lunga esecuzione

**Checklist di sicurezza:**
- Mai usare input utente non sanitizzato
- Validare tutto l'input
- Usare allowlist per i comandi
- Eseguire escape dei caratteri speciali quando necessario
- Eseguire con il minimo privilegio
- Preferire le API Hemlock ai comandi shell
