# Signalbehandlung in Hemlock

Hemlock bietet **POSIX-Signalbehandlung** für die Verwaltung von Systemsignalen wie SIGINT (Strg+C), SIGTERM und benutzerdefinierten Signalen. Dies ermöglicht Low-Level-Prozesssteuerung und Inter-Prozess-Kommunikation.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Signal-API](#signal-api)
- [Signal-Konstanten](#signal-konstanten)
- [Grundlegende Signalbehandlung](#grundlegende-signalbehandlung)
- [Fortgeschrittene Muster](#fortgeschrittene-muster)
- [Signal-Handler-Verhalten](#signal-handler-verhalten)
- [Sicherheitsüberlegungen](#sicherheitsüberlegungen)
- [Häufige Anwendungsfälle](#häufige-anwendungsfälle)
- [Vollständige Beispiele](#vollständige-beispiele)

## Überblick

Signalbehandlung ermöglicht Programmen:
- Auf Benutzerunterbrechungen reagieren (Strg+C, Strg+Z)
- Graceful Shutdown implementieren
- Beendigungsanfragen behandeln
- Benutzerdefinierte Signale für Inter-Prozess-Kommunikation verwenden
- Alarm-/Timer-Mechanismen erstellen

**Wichtig:** Signalbehandlung ist in Hemlocks Philosophie **inhärent unsicher**. Handler können jederzeit aufgerufen werden und die normale Ausführung unterbrechen. Der Benutzer ist für die ordnungsgemäße Synchronisation verantwortlich.

## Signal-API

### signal(signum, handler_fn)

Einen Signal-Handler registrieren.

**Parameter:**
- `signum` (i32) - Signalnummer (Konstante wie SIGINT, SIGTERM)
- `handler_fn` (function oder null) - Funktion, die aufgerufen wird wenn Signal empfangen wird, oder `null` um auf Standard zurückzusetzen

**Rückgabe:** Der vorherige Handler (oder `null` wenn keiner)

**Beispiel:**
```hemlock
fn my_handler(sig) {
    print("Signal empfangen: " + typeof(sig));
}

let old_handler = signal(SIGINT, my_handler);
```

**Auf Standard zurücksetzen:**
```hemlock
signal(SIGINT, null);  // SIGINT auf Standardverhalten zurücksetzen
```

### raise(signum)

Ein Signal an den aktuellen Prozess senden.

**Parameter:**
- `signum` (i32) - Zu sendende Signalnummer

**Rückgabe:** `null`

**Beispiel:**
```hemlock
raise(SIGUSR1);  // SIGUSR1-Handler auslösen
```

## Signal-Konstanten

Hemlock bietet Standard-POSIX-Signal-Konstanten als i32-Werte.

### Unterbrechung & Beendigung

| Konstante | Wert | Beschreibung | Häufiger Auslöser |
|-----------|------|--------------|-------------------|
| `SIGINT` | 2 | Unterbrechung von Tastatur | Strg+C |
| `SIGTERM` | 15 | Beendigungsanfrage | `kill`-Befehl |
| `SIGQUIT` | 3 | Beenden von Tastatur | Strg+\ |
| `SIGHUP` | 1 | Hangup erkannt | Terminal geschlossen |
| `SIGABRT` | 6 | Abort-Signal | `abort()`-Funktion |

**Beispiele:**
```hemlock
signal(SIGINT, handle_interrupt);   // Strg+C
signal(SIGTERM, handle_terminate);  // kill-Befehl
signal(SIGHUP, handle_hangup);      // Terminal schließt
```

### Benutzerdefinierte Signale

| Konstante | Wert | Beschreibung | Anwendungsfall |
|-----------|------|--------------|----------------|
| `SIGUSR1` | 10 | Benutzerdefiniertes Signal 1 | Benutzerdefinierte IPC |
| `SIGUSR2` | 12 | Benutzerdefiniertes Signal 2 | Benutzerdefinierte IPC |

**Beispiele:**
```hemlock
// Für benutzerdefinierte Kommunikation verwenden
signal(SIGUSR1, reload_config);
signal(SIGUSR2, rotate_logs);
```

### Prozesssteuerung

| Konstante | Wert | Beschreibung | Hinweise |
|-----------|------|--------------|----------|
| `SIGALRM` | 14 | Alarm-Timer | Nach `alarm()` |
| `SIGCHLD` | 17 | Kindprozess-Statusänderung | Prozessverwaltung |
| `SIGCONT` | 18 | Fortsetzen wenn gestoppt | Nach SIGSTOP fortsetzen |
| `SIGSTOP` | 19 | Prozess stoppen | **Kann nicht abgefangen werden** |
| `SIGTSTP` | 20 | Terminal-Stop | Strg+Z |

**Beispiele:**
```hemlock
signal(SIGALRM, handle_timeout);
signal(SIGCHLD, handle_child_exit);
```

### I/O-Signale

| Konstante | Wert | Beschreibung | Wann gesendet |
|-----------|------|--------------|---------------|
| `SIGPIPE` | 13 | Gebrochene Pipe | Schreiben in geschlossene Pipe |
| `SIGTTIN` | 21 | Hintergrund-Lesen von Terminal | BG-Prozess liest TTY |
| `SIGTTOU` | 22 | Hintergrund-Schreiben zu Terminal | BG-Prozess schreibt TTY |

**Beispiele:**
```hemlock
signal(SIGPIPE, handle_broken_pipe);
```

## Grundlegende Signalbehandlung

### Strg+C abfangen

```hemlock
let interrupted = false;

fn handle_interrupt(sig) {
    print("SIGINT empfangen!");
    interrupted = true;
}

signal(SIGINT, handle_interrupt);

// Programm läuft weiter...
// Benutzer drückt Strg+C -> handle_interrupt() wird aufgerufen

while (!interrupted) {
    // Arbeit erledigen...
}

print("Beende wegen Unterbrechung");
```

### Handler-Funktionssignatur

Signal-Handler empfangen ein Argument: die Signalnummer (i32)

```hemlock
fn my_handler(signum) {
    print("Signal empfangen: " + typeof(signum));
    // signum enthält die Signalnummer (z.B. 2 für SIGINT)

    if (signum == SIGINT) {
        print("Das ist SIGINT");
    }
}

signal(SIGINT, my_handler);
signal(SIGTERM, my_handler);  // Gleicher Handler für mehrere Signale
```

### Mehrere Signal-Handler

Verschiedene Handler für verschiedene Signale:

```hemlock
fn handle_int(sig) {
    print("SIGINT empfangen");
}

fn handle_term(sig) {
    print("SIGTERM empfangen");
}

fn handle_usr1(sig) {
    print("SIGUSR1 empfangen");
}

signal(SIGINT, handle_int);
signal(SIGTERM, handle_term);
signal(SIGUSR1, handle_usr1);
```

### Auf Standardverhalten zurücksetzen

`null` als Handler übergeben, um auf Standardverhalten zurückzusetzen:

```hemlock
// Benutzerdefinierten Handler registrieren
signal(SIGINT, my_handler);

// Später, auf Standard zurücksetzen (bei SIGINT beenden)
signal(SIGINT, null);
```

### Signale manuell auslösen

Signale an den eigenen Prozess senden:

```hemlock
let count = 0;

fn increment(sig) {
    count = count + 1;
}

signal(SIGUSR1, increment);

// Handler manuell auslösen
raise(SIGUSR1);
raise(SIGUSR1);

print(count);  // 2
```

## Fortgeschrittene Muster

### Graceful-Shutdown-Muster

Häufiges Muster für Bereinigung bei Beendigung:

```hemlock
let should_exit = false;

fn handle_shutdown(sig) {
    print("Fahre graceful herunter...");
    should_exit = true;
}

signal(SIGINT, handle_shutdown);
signal(SIGTERM, handle_shutdown);

// Hauptschleife
while (!should_exit) {
    // Arbeit erledigen...
    // should_exit-Flag regelmäßig prüfen
}

print("Bereinigung abgeschlossen");
```

### Signal-Zähler

Anzahl empfangener Signale verfolgen:

```hemlock
let signal_count = 0;

fn count_signals(sig) {
    signal_count = signal_count + 1;
    print(typeof(signal_count) + " Signale empfangen");
}

signal(SIGUSR1, count_signals);

// Später...
print("Gesamte Signale: " + typeof(signal_count));
```

### Konfiguration bei Signal neu laden

```hemlock
let config = load_config();

fn reload_config(sig) {
    print("Lade Konfiguration neu...");
    config = load_config();
    print("Konfiguration neu geladen");
}

signal(SIGHUP, reload_config);  // Bei SIGHUP neu laden

// SIGHUP an Prozess senden, um Konfiguration neu zu laden
// Von Shell: kill -HUP <pid>
```

### Timeout mit SIGALRM

```hemlock
let timed_out = false;

fn handle_alarm(sig) {
    print("Timeout!");
    timed_out = true;
}

signal(SIGALRM, handle_alarm);

// Alarm setzen (noch nicht in Hemlock implementiert, nur Beispiel)
// alarm(5);  // 5 Sekunden Timeout

while (!timed_out) {
    // Arbeit mit Timeout erledigen
}
```

### Signal-basierte Zustandsmaschine

```hemlock
let state = 0;

fn next_state(sig) {
    state = (state + 1) % 3;
    print("Zustand: " + typeof(state));
}

fn prev_state(sig) {
    state = (state - 1 + 3) % 3;
    print("Zustand: " + typeof(state));
}

signal(SIGUSR1, next_state);  // Zustand vorwärts
signal(SIGUSR2, prev_state);  // Zustand zurück

// Zustandsmaschine steuern:
// kill -USR1 <pid>  # Nächster Zustand
// kill -USR2 <pid>  # Vorheriger Zustand
```

## Signal-Handler-Verhalten

### Wichtige Hinweise

**Handler-Ausführung:**
- Handler werden **synchron** aufgerufen, wenn das Signal empfangen wird
- Handler werden im aktuellen Prozesskontext ausgeführt
- Signal-Handler teilen die Closure-Umgebung der Funktion, in der sie definiert wurden
- Handler können auf äußere Scope-Variablen zugreifen und diese modifizieren (wie Globals oder erfasste Variablen)

**Best Practices:**
- Handler einfach und schnell halten - lange Operationen vermeiden
- Flags setzen statt komplexe Logik auszuführen
- Funktionen vermeiden, die möglicherweise Locks nehmen
- Bewusst sein, dass Handler jede Operation unterbrechen können

### Welche Signale abgefangen werden können

**Kann abfangen und behandeln:**
- SIGINT, SIGTERM, SIGUSR1, SIGUSR2, SIGHUP, SIGQUIT
- SIGALRM, SIGCHLD, SIGCONT, SIGTSTP
- SIGPIPE, SIGTTIN, SIGTTOU
- SIGABRT (aber Programm wird nach Handler-Rückkehr abbrechen)

**Kann nicht abfangen:**
- `SIGKILL` (9) - Beendet Prozess immer
- `SIGSTOP` (19) - Stoppt Prozess immer

**Systemabhängig:**
- Einige Signale haben Standardverhalten, die je nach System unterschiedlich sein können
- Prüfen Sie die Signal-Dokumentation Ihrer Plattform für Details

### Handler-Einschränkungen

```hemlock
fn complex_handler(sig) {
    // Vermeiden Sie diese in Signal-Handlern:

    // ❌ Lang laufende Operationen
    // process_large_file();

    // ❌ Blockierende I/O
    // let f = open("log.txt", "a");
    // f.write("Signal empfangen\n");

    // ❌ Komplexe Zustandsänderungen
    // rebuild_entire_data_structure();

    // ✅ Einfaches Flag-Setzen ist sicher
    let should_stop = true;

    // ✅ Einfache Zähler-Updates sind normalerweise sicher
    let signal_count = signal_count + 1;
}
```

## Sicherheitsüberlegungen

Signalbehandlung ist in Hemlocks Philosophie **inhärent unsicher**.

### Race Conditions

Handler können jederzeit aufgerufen werden und normale Ausführung unterbrechen:

```hemlock
let counter = 0;

fn increment(sig) {
    counter = counter + 1;  // Race Condition wenn während counter-Update aufgerufen
}

signal(SIGUSR1, increment);

// Hauptcode modifiziert auch counter
counter = counter + 1;  // Könnte von Signal-Handler unterbrochen werden
```

**Problem:** Wenn Signal ankommt während Hauptcode `counter` aktualisiert, ist das Ergebnis unvorhersehbar.

### Async-Signal-Sicherheit

Hemlock garantiert **keine** Async-Signal-Sicherheit:
- Handler können jeden Hemlock-Code aufrufen (anders als Cs eingeschränkte async-signal-sichere Funktionen)
- Dies bietet Flexibilität, erfordert aber Benutzer-Vorsicht
- Race Conditions sind möglich, wenn Handler gemeinsamen Zustand modifiziert

### Best Practices für sichere Signalbehandlung

**1. Atomare Flags verwenden**

Einfache Boolean-Zuweisungen sind im Allgemeinen sicher:

```hemlock
let should_exit = false;

fn handler(sig) {
    should_exit = true;  // Einfache Zuweisung ist sicher
}

signal(SIGINT, handler);

while (!should_exit) {
    // Arbeit...
}
```

**2. Gemeinsamen Zustand minimieren**

```hemlock
let interrupt_count = 0;

fn handler(sig) {
    // Nur diese eine Variable modifizieren
    interrupt_count = interrupt_count + 1;
}
```

**3. Komplexe Operationen aufschieben**

```hemlock
let pending_reload = false;

fn signal_reload(sig) {
    pending_reload = true;  // Nur Flag setzen
}

signal(SIGHUP, signal_reload);

// In Hauptschleife:
while (true) {
    if (pending_reload) {
        reload_config();  // Komplexe Arbeit hier erledigen
        pending_reload = false;
    }

    // Normale Arbeit...
}
```

**4. Wiedereintrittsprobleme vermeiden**

```hemlock
let in_critical_section = false;
let data = [];

fn careful_handler(sig) {
    if (in_critical_section) {
        // Daten nicht modifizieren während Hauptcode sie verwendet
        return;
    }
    // Sicher fortzufahren
}
```

## Häufige Anwendungsfälle

### 1. Graceful Server-Shutdown

```hemlock
let running = true;

fn shutdown(sig) {
    print("Shutdown-Signal empfangen");
    running = false;
}

signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Server-Hauptschleife
while (running) {
    handle_client_request();
}

cleanup_resources();
print("Server gestoppt");
```

### 2. Konfiguration neu laden (ohne Neustart)

```hemlock
let config = load_config("app.conf");
let reload_needed = false;

fn trigger_reload(sig) {
    reload_needed = true;
}

signal(SIGHUP, trigger_reload);

while (true) {
    if (reload_needed) {
        print("Lade Konfiguration neu...");
        config = load_config("app.conf");
        reload_needed = false;
    }

    // config verwenden...
}
```

### 3. Log-Rotation

```hemlock
let log_file = open("app.log", "a");
let rotate_needed = false;

fn trigger_rotate(sig) {
    rotate_needed = true;
}

signal(SIGUSR1, trigger_rotate);

while (true) {
    if (rotate_needed) {
        log_file.close();
        // Altes Log umbenennen, neues öffnen
        exec("mv app.log app.log.old");
        log_file = open("app.log", "a");
        rotate_needed = false;
    }

    // Normales Logging...
    log_file.write("Log-Eintrag\n");
}
```

### 4. Statusberichterstattung

```hemlock
let requests_handled = 0;

fn report_status(sig) {
    print("Status: " + typeof(requests_handled) + " Anfragen bearbeitet");
}

signal(SIGUSR1, report_status);

while (true) {
    handle_request();
    requests_handled = requests_handled + 1;
}

// Von Shell: kill -USR1 <pid>
```

### 5. Debug-Modus umschalten

```hemlock
let debug_mode = false;

fn toggle_debug(sig) {
    debug_mode = !debug_mode;
    if (debug_mode) {
        print("Debug-Modus: AN");
    } else {
        print("Debug-Modus: AUS");
    }
}

signal(SIGUSR2, toggle_debug);

// Von Shell: kill -USR2 <pid> zum Umschalten
```

## Vollständige Beispiele

### Beispiel 1: Unterbrechungs-Handler mit Bereinigung

```hemlock
let running = true;
let signal_count = 0;

fn handle_signal(signum) {
    signal_count = signal_count + 1;

    if (signum == SIGINT) {
        print("Unterbrechung erkannt (Strg+C)");
        running = false;
    }

    if (signum == SIGUSR1) {
        print("Benutzersignal 1 empfangen");
    }
}

// Handler registrieren
signal(SIGINT, handle_signal);
signal(SIGUSR1, handle_signal);

// Arbeit simulieren
let i = 0;
while (running && i < 100) {
    print("Arbeite... " + typeof(i));

    // SIGUSR1 alle 10 Iterationen auslösen
    if (i == 10 || i == 20) {
        raise(SIGUSR1);
    }

    i = i + 1;
}

print("Gesamte empfangene Signale: " + typeof(signal_count));
```

### Beispiel 2: Multi-Signal-Zustandsmaschine

```hemlock
let state = "idle";
let request_count = 0;

fn start_processing(sig) {
    state = "processing";
    print("Zustand: " + state);
}

fn stop_processing(sig) {
    state = "idle";
    print("Zustand: " + state);
}

fn report_stats(sig) {
    print("Zustand: " + state);
    print("Anfragen: " + typeof(request_count));
}

signal(SIGUSR1, start_processing);
signal(SIGUSR2, stop_processing);
signal(SIGHUP, report_stats);

while (true) {
    if (state == "processing") {
        // Arbeit erledigen
        request_count = request_count + 1;
    }

    // Bei jeder Iteration prüfen...
}
```

### Beispiel 3: Worker-Pool-Controller

```hemlock
let worker_count = 4;
let should_exit = false;

fn increase_workers(sig) {
    worker_count = worker_count + 1;
    print("Worker: " + typeof(worker_count));
}

fn decrease_workers(sig) {
    if (worker_count > 1) {
        worker_count = worker_count - 1;
    }
    print("Worker: " + typeof(worker_count));
}

fn shutdown(sig) {
    print("Fahre herunter...");
    should_exit = true;
}

signal(SIGUSR1, increase_workers);
signal(SIGUSR2, decrease_workers);
signal(SIGINT, shutdown);
signal(SIGTERM, shutdown);

// Hauptschleife passt Worker-Pool basierend auf worker_count an
while (!should_exit) {
    // Worker basierend auf worker_count verwalten
    // ...
}
```

### Beispiel 4: Timeout-Muster

```hemlock
let operation_complete = false;
let timed_out = false;

fn timeout_handler(sig) {
    timed_out = true;
}

signal(SIGALRM, timeout_handler);

// Lange Operation starten
async fn long_operation() {
    // ... Arbeit
    operation_complete = true;
}

let task = spawn(long_operation);

// Mit Timeout warten (manuelle Prüfung)
let elapsed = 0;
while (!operation_complete && elapsed < 1000) {
    // Schlafen oder prüfen
    elapsed = elapsed + 1;
}

if (!operation_complete) {
    print("Operation hat Timeout erreicht");
    detach(task);  // Warten aufgeben
} else {
    join(task);
    print("Operation abgeschlossen");
}
```

## Signal-Handler debuggen

### Diagnose-Prints hinzufügen

```hemlock
fn debug_handler(sig) {
    print("Handler aufgerufen für Signal: " + typeof(sig));
    print("Stack: (noch nicht verfügbar)");

    // Ihre Handler-Logik...
}

signal(SIGINT, debug_handler);
```

### Signal-Aufrufe zählen

```hemlock
let handler_calls = 0;

fn counting_handler(sig) {
    handler_calls = handler_calls + 1;
    print("Handler-Aufruf #" + typeof(handler_calls));

    // Ihre Handler-Logik...
}
```

### Mit raise() testen

```hemlock
fn test_handler(sig) {
    print("Test-Signal empfangen: " + typeof(sig));
}

signal(SIGUSR1, test_handler);

// Durch manuelles Auslösen testen
raise(SIGUSR1);
print("Handler sollte aufgerufen worden sein");
```

## Zusammenfassung

Hemlocks Signalbehandlung bietet:

- ✅ POSIX-Signalbehandlung für Low-Level-Prozesssteuerung
- ✅ 15 Standard-Signal-Konstanten
- ✅ Einfache signal()- und raise()-API
- ✅ Flexible Handler-Funktionen mit Closure-Unterstützung
- ✅ Mehrere Signale können Handler teilen

Denken Sie daran:
- Signalbehandlung ist inhärent unsicher - mit Vorsicht verwenden
- Handler einfach und schnell halten
- Flags für Zustandsänderungen verwenden, nicht komplexe Operationen
- Handler können Ausführung jederzeit unterbrechen
- SIGKILL oder SIGSTOP können nicht abgefangen werden
- Handler gründlich mit raise() testen

Häufige Muster:
- Graceful Shutdown (SIGINT, SIGTERM)
- Konfiguration neu laden (SIGHUP)
- Log-Rotation (SIGUSR1)
- Statusberichterstattung (SIGUSR1/SIGUSR2)
- Debug-Modus umschalten (SIGUSR2)
