# Nebenlaeufigkeits-API-Referenz

Vollstaendige Referenz fuer Hemlocks Async/Nebenlaeufigkeitssystem.

---

## Uebersicht

Hemlock bietet **strukturierte Nebenlaeufigkeit** mit echter Multi-Thread-Parallelitaet unter Verwendung von POSIX-Threads (pthreads). Jeder gestartete Task laeuft auf einem separaten OS-Thread, was echte parallele Ausfuehrung ueber mehrere CPU-Kerne ermoeglicht.

**Hauptmerkmale:**
- Echte Multi-Thread-Parallelitaet (keine Green Threads)
- Async-Funktionssyntax
- Task-Starten und -Beitreten
- Thread-sichere Kanaele
- Ausnahme-Propagierung

**Threading-Modell:**
- Echte OS-Threads (POSIX pthreads)
- Echte Parallelitaet (mehrere CPU-Kerne)
- Kernel-geplant (praeemptives Multitasking)
- Thread-sichere Synchronisation (Mutexes, Bedingungsvariablen)

---

## Async-Funktionen

### Async-Funktionsdeklaration

Funktionen koennen als `async` deklariert werden um anzuzeigen, dass sie fuer nebenlaeufige Ausfuehrung konzipiert sind.

**Syntax:**
```hemlock
async fn function_name(params): return_type {
    // Funktionskoerper
}
```

**Beispiele:**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

async fn process_data(data: string) {
    print("Verarbeite:", data);
    return null;
}
```

**Verhalten:**
- `async fn` deklariert eine asynchrone Funktion
- Kann synchron aufgerufen werden (laeuft im aktuellen Thread)
- Kann als nebenlaeufiger Task gestartet werden (laeuft auf neuem Thread)
- Wenn gestartet, laeuft auf eigenem OS-Thread

**Hinweis:** Das `await`-Schluesselwort ist fuer zukuenftige Verwendung reserviert, aber derzeit nicht implementiert.

---

## Task-Verwaltung

### spawn

Erstellt und startet einen neuen nebenlaeufigen Task.

**Signatur:**
```hemlock
spawn(async_fn: function, ...args): task
```

**Parameter:**
- `async_fn` - Auszufuehrende Async-Funktion
- `...args` - An die Funktion zu uebergebende Argumente

**Rueckgabe:** Task-Handle

**Beispiele:**
```hemlock
async fn compute(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Einzelnen Task starten
let t = spawn(compute, 1000);
let result = join(t);
print(result);

// Mehrere Tasks starten (laufen parallel!)
let t1 = spawn(compute, 100);
let t2 = spawn(compute, 200);
let t3 = spawn(compute, 300);

// Alle drei laufen gleichzeitig
let r1 = join(t1);
let r2 = join(t2);
let r3 = join(t3);
```

**Verhalten:**
- Erstellt neuen OS-Thread via `pthread_create()`
- Beginnt sofort mit der Ausfuehrung der Funktion
- Gibt Task-Handle fuer spaeteres Beitreten zurueck
- Tasks laufen parallel auf separaten CPU-Kernen

---

### join

Wartet auf Task-Abschluss und ruft Ergebnis ab.

**Signatur:**
```hemlock
join(task: task): any
```

**Parameter:**
- `task` - Task-Handle von `spawn()`

**Rueckgabe:** Rueckgabewert des Tasks

**Beispiele:**
```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

let t = spawn(factorial, 10);
let result = join(t);  // Blockiert bis Task fertig
print(result);         // 3628800
```

**Verhalten:**
- Blockiert aktuellen Thread bis Task abgeschlossen
- Gibt Rueckgabewert des Tasks zurueck
- Propagiert vom Task geworfene Ausnahmen
- Raeumt Task-Ressourcen nach Rueckkehr auf

**Fehlerbehandlung:**
```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task fehlgeschlagen!";
    }
    return 42;
}

let t = spawn(risky_operation, 1);
try {
    let result = join(t);
} catch (e) {
    print("Abgefangen:", e);  // "Abgefangen: Task fehlgeschlagen!"
}
```

---

### detach

Loest Task ab (Fire-and-Forget-Ausfuehrung).

**Signatur:**
```hemlock
detach(task: task): null
```

**Parameter:**
- `task` - Task-Handle von `spawn()`

**Rueckgabe:** `null`

**Beispiele:**
```hemlock
async fn background_work() {
    print("Arbeite im Hintergrund...");
    return null;
}

let t = spawn(background_work);
detach(t);  // Task laeuft unabhaengig weiter

// Kann abgeloesten Task nicht beitreten
// join(t);  // FEHLER
```

**Verhalten:**
- Task laeuft unabhaengig weiter
- Kann abgeloesten Task nicht `join()`en
- Task und Thread werden automatisch aufgeraeumt wenn Task abgeschlossen

**Anwendungsfaelle:**
- Fire-and-Forget-Hintergrundtasks
- Logging/Monitoring-Tasks
- Tasks die keine Werte zurueckgeben muessen

---

## Kanaele

Kanaele bieten thread-sichere Kommunikation zwischen Tasks.

### channel

Erstellt einen gepufferten Kanal.

**Signatur:**
```hemlock
channel(capacity: i32): channel
```

**Parameter:**
- `capacity` - Puffergroesse (Anzahl der Werte)

**Rueckgabe:** Kanal-Objekt

**Beispiele:**
```hemlock
let ch = channel(10);  // Gepufferter Kanal mit Kapazitaet 10
let ch2 = channel(1);  // Minimaler Puffer (synchron)
let ch3 = channel(100); // Grosser Puffer
```

**Verhalten:**
- Erstellt thread-sicheren Kanal
- Verwendet pthread-Mutexes zur Synchronisation
- Kapazitaet ist bei Erstellung fest

---

### Kanal-Methoden

#### send

Sendet Wert an Kanal (blockiert wenn voll).

**Signatur:**
```hemlock
channel.send(value: any): null
```

**Parameter:**
- `value` - Zu sendender Wert (beliebiger Typ)

**Rueckgabe:** `null`

**Beispiele:**
```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

let ch = channel(10);
let t = spawn(producer, ch, 5);
```

**Verhalten:**
- Sendet Wert an Kanal
- Blockiert wenn Kanal voll
- Thread-sicher (verwendet Mutex)
- Gibt zurueck nachdem Wert gesendet wurde

---

#### recv

Empfaengt Wert von Kanal (blockiert wenn leer).

**Signatur:**
```hemlock
channel.recv(): any
```

**Rueckgabe:** Wert vom Kanal, oder `null` wenn Kanal geschlossen und leer

**Beispiele:**
```hemlock
async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(10);
let t = spawn(consumer, ch, 5);
```

**Verhalten:**
- Empfaengt Wert vom Kanal
- Blockiert wenn Kanal leer
- Gibt `null` zurueck wenn Kanal geschlossen und leer
- Thread-sicher (verwendet Mutex)

---

#### close

Schliesst Kanal (keine weiteren Sends erlaubt).

**Signatur:**
```hemlock
channel.close(): null
```

**Rueckgabe:** `null`

**Beispiele:**
```hemlock
async fn producer(ch) {
    ch.send(1);
    ch.send(2);
    ch.send(3);
    ch.close();  // Signalisiert keine weiteren Werte
    return null;
}

async fn consumer(ch) {
    while (true) {
        let val = ch.recv();
        if (val == null) {
            break;  // Kanal geschlossen
        }
        print(val);
    }
    return null;
}
```

**Verhalten:**
- Schliesst Kanal
- Keine weiteren Sends erlaubt
- `recv()` gibt `null` zurueck wenn Kanal leer
- Thread-sicher

---

## Vollstaendiges Nebenlaeufigkeitsbeispiel

### Producer-Consumer-Muster

```hemlock
async fn producer(ch, count: i32) {
    let i = 0;
    while (i < count) {
        print("Produziere:", i);
        ch.send(i * 10);
        i = i + 1;
    }
    ch.close();
    return null;
}

async fn consumer(ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        print("Konsumiere:", val);
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

// Kanal erstellen
let ch = channel(10);

// Producer und Consumer starten
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Auf Abschluss warten
join(p);
let total = join(c);
print("Gesamt:", total);  // 0+10+20+30+40 = 100
```

---

## Parallele Berechnung

### Beispiel mit mehreren Tasks

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Mehrere Tasks starten (laufen parallel!)
let t1 = spawn(factorial, 5);   // Thread 1
let t2 = spawn(factorial, 6);   // Thread 2
let t3 = spawn(factorial, 7);   // Thread 3
let t4 = spawn(factorial, 8);   // Thread 4

// Alle vier berechnen gleichzeitig!

// Auf Ergebnisse warten
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
let f8 = join(t4);  // 40320

print(f5, f6, f7, f8);
```

---

## Task-Lebenszyklus

### Zustandsuebergaenge

1. **Erstellt** - Task gestartet aber noch nicht laufend
2. **Laufend** - Task laeuft auf OS-Thread
3. **Abgeschlossen** - Task beendet (Ergebnis verfuegbar)
4. **Beigetreten** - Ergebnis abgerufen, Ressourcen aufgeraeumt
5. **Abgeloest** - Task laeuft unabhaengig weiter

### Lebenszyklus-Beispiel

```hemlock
async fn work(n: i32): i32 {
    return n * 2;
}

// 1. Task erstellen
let t = spawn(work, 21);  // Zustand: Laufend

// Task laeuft auf separatem Thread...

// 2. Task beitreten
let result = join(t);     // Zustand: Abgeschlossen → Beigetreten
print(result);            // 42

// Task-Ressourcen nach join aufgeraeumt
```

### Abgeloester Lebenszyklus

```hemlock
async fn background() {
    print("Hintergrund-Task laeuft");
    return null;
}

// 1. Task erstellen
let t = spawn(background);  // Zustand: Laufend

// 2. Task abloesen
detach(t);                  // Zustand: Abgeloest

// Task laeuft unabhaengig weiter
// Ressourcen werden vom OS aufgeraeumt wenn fertig
```

---

## Fehlerbehandlung

### Ausnahme-Propagierung

Ausnahmen die in Tasks geworfen werden, werden beim Beitreten propagiert:

```hemlock
async fn risky_operation(should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task fehlgeschlagen!";
    }
    return 42;
}

// Task der erfolgreich ist
let t1 = spawn(risky_operation, 0);
let result1 = join(t1);  // 42

// Task der fehlschlaegt
let t2 = spawn(risky_operation, 1);
try {
    let result2 = join(t2);
} catch (e) {
    print("Abgefangen:", e);  // "Abgefangen: Task fehlgeschlagen!"
}
```

### Umgang mit mehreren Tasks

```hemlock
async fn work(id: i32, should_fail: i32): i32 {
    if (should_fail == 1) {
        throw "Task " + typeof(id) + " fehlgeschlagen";
    }
    return id * 10;
}

let t1 = spawn(work, 1, 0);
let t2 = spawn(work, 2, 1);  // Wird fehlschlagen
let t3 = spawn(work, 3, 0);

// Beitreten mit Fehlerbehandlung
try {
    let r1 = join(t1);  // OK
    print("Task 1:", r1);

    let r2 = join(t2);  // Wirft
    print("Task 2:", r2);  // Nie erreicht
} catch (e) {
    print("Fehler:", e);  // "Fehler: Task 2 fehlgeschlagen"
}

// Kann verbleibenden Task noch beitreten
let r3 = join(t3);
print("Task 3:", r3);
```

---

## Leistungscharakteristiken

### Echte Parallelitaet

```hemlock
async fn cpu_intensive(n: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// Sequentielle Ausfuehrung
let start = get_time();
let r1 = cpu_intensive(10000000);
let r2 = cpu_intensive(10000000);
let sequential_time = get_time() - start;

// Parallele Ausfuehrung
let start2 = get_time();
let t1 = spawn(cpu_intensive, 10000000);
let t2 = spawn(cpu_intensive, 10000000);
join(t1);
join(t2);
let parallel_time = get_time() - start2;

// parallel_time sollte ~50% von sequential_time auf Multi-Core-Systemen sein
```

**Bewiesene Charakteristiken:**
- N Tasks koennen N CPU-Kerne gleichzeitig nutzen
- Stresstests zeigen 8-9x CPU-Zeit vs. Wandzeit (Beweis der Parallelitaet)
- Thread-Overhead: ~8KB Stack + pthread-Overhead pro Task
- Blockierende Operationen in einem Task blockieren andere nicht

---

## Implementierungsdetails

### Threading-Modell

- **1:1 Threading** - Jeder Task = 1 OS-Thread (`pthread`)
- **Kernel-geplant** - OS-Kernel verteilt Threads auf Kerne
- **Praeemptives Multitasking** - OS kann Threads unterbrechen und wechseln
- **Kein GIL** - Kein Global Interpreter Lock (anders als Python)

### Synchronisation

- **Mutexes** - Kanaele verwenden `pthread_mutex_t`
- **Bedingungsvariablen** - Blockierendes send/recv verwendet `pthread_cond_t`
- **Lock-freie Operationen** - Task-Zustandsuebergaenge sind atomar

### Speicher & Aufraeumen

- **Beigetretene Tasks** - Automatisch aufgeraeumt nach `join()`
- **Abgeloeste Tasks** - Automatisch aufgeraeumt wenn Task abgeschlossen
- **Kanaele** - Referenzgezaehlt, freigegeben wenn nicht mehr verwendet

---

## Einschraenkungen

- Kein `select()` fuer Multiplexen mehrerer Kanaele
- Kein Work-Stealing-Scheduler (1 Thread pro Task)
- Keine async I/O-Integration (Datei/Netzwerk-Operationen blockieren)
- Kanalkapazitaet bei Erstellung fest

---

## Vollstaendige API-Zusammenfassung

### Funktionen

| Funktion  | Signatur                          | Rueckgabe | Beschreibung                     |
|-----------|-----------------------------------|-----------|----------------------------------|
| `spawn`   | `(async_fn: function, ...args)`   | `task`    | Nebenlaeufigen Task erstellen und starten |
| `join`    | `(task: task)`                    | `any`     | Auf Task warten, Ergebnis holen  |
| `detach`  | `(task: task)`                    | `null`    | Task abloesen (Fire-and-Forget)  |
| `channel` | `(capacity: i32)`                 | `channel` | Thread-sicheren Kanal erstellen  |

### Kanal-Methoden

| Methode | Signatur        | Rueckgabe | Beschreibung                       |
|---------|-----------------|-----------|-----------------------------------|
| `send`  | `(value: any)`  | `null`    | Wert senden (blockiert wenn voll) |
| `recv`  | `()`            | `any`     | Wert empfangen (blockiert wenn leer) |
| `close` | `()`            | `null`    | Kanal schliessen                  |

### Typen

| Typ       | Beschreibung                         |
|-----------|--------------------------------------|
| `task`    | Handle fuer nebenlaeufigen Task      |
| `channel` | Thread-sicherer Kommunikationskanal  |

---

## Best Practices

### Empfohlen

- Verwenden Sie Kanaele fuer Kommunikation zwischen Tasks
- Behandeln Sie Ausnahmen von beigetretenen Tasks
- Schliessen Sie Kanaele wenn Senden beendet
- Verwenden Sie `join()` um Ergebnisse zu holen und aufzuraeumen
- Starten Sie nur async-Funktionen

### Vermeiden

- Teilen Sie keinen veraenderbaren Zustand ohne Synchronisation
- Treten Sie demselben Task nicht zweimal bei
- Senden Sie nicht auf geschlossenen Kanaelen
- Starten Sie keine nicht-async-Funktionen
- Vergessen Sie nicht Tasks beizutreten (ausser wenn abgeloest)

---

## Siehe auch

- [Eingebaute Funktionen](builtins.md) - `spawn()`, `join()`, `detach()`, `channel()`
- [Typsystem](type-system.md) - Task- und Kanal-Typen
