# Async/Nebenläufigkeit in Hemlock

Hemlock bietet **strukturierte Nebenläufigkeit** mit async/await-Syntax, Task-Spawning und Channels zur Kommunikation. Die Implementierung verwendet POSIX-Threads (pthreads) für **echte Multithread-Parallelität**.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Threading-Modell](#threading-modell)
- [Async-Funktionen](#async-funktionen)
- [Task-Spawning](#task-spawning)
- [Channels](#channels)
- [Ausnahmeweiterleitung](#ausnahmeweiterleitung)
- [Implementierungsdetails](#implementierungsdetails)
- [Best Practices](#best-practices)
- [Leistungsmerkmale](#leistungsmerkmale)
- [Aktuelle Einschränkungen](#aktuelle-einschränkungen)

## Überblick

**Was das bedeutet:**
- ✅ **Echte OS-Threads** - Jeder gespawnte Task läuft auf einem separaten pthread (POSIX-Thread)
- ✅ **Echte Parallelität** - Tasks werden gleichzeitig auf mehreren CPU-Kernen ausgeführt
- ✅ **Kernel-geplant** - Der OS-Scheduler verteilt Tasks auf verfügbare Kerne
- ✅ **Thread-sichere Channels** - Verwendet pthread-Mutexe und Bedingungsvariablen zur Synchronisation

**Was das NICHT ist:**
- ❌ **KEINE Green Threads** - Kein User-Space-kooperatives Multitasking
- ❌ **KEINE async/await-Coroutinen** - Keine Single-Threaded Event-Loop wie JavaScript/Python asyncio
- ❌ **KEINE emulierte Nebenläufigkeit** - Keine simulierte Parallelität

Dies ist das **gleiche Threading-Modell wie C, C++ und Rust** bei Verwendung von OS-Threads. Sie erhalten echte parallele Ausführung über mehrere Kerne.

## Threading-Modell

### 1:1 Threading

Hemlock verwendet ein **1:1 Threading-Modell**, wobei:
- Jeder gespawnte Task einen dedizierten OS-Thread über `pthread_create()` erstellt
- Der OS-Kernel Threads auf verfügbare CPU-Kerne verteilt
- Präemptives Multitasking - das OS kann Threads unterbrechen und zwischen ihnen wechseln
- **Kein GIL** - Anders als Python gibt es keinen Global Interpreter Lock, der die Parallelität einschränkt

### Synchronisationsmechanismen

- **Mutexe** - Channels verwenden `pthread_mutex_t` für thread-sicheren Zugriff
- **Bedingungsvariablen** - Blockierendes send/recv verwendet `pthread_cond_t` für effizientes Warten
- **Lock-freie Operationen** - Task-Zustandsübergänge sind atomar

## Async-Funktionen

Funktionen können als `async` deklariert werden, um anzuzeigen, dass sie für nebenläufige Ausführung konzipiert sind:

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
```

### Wichtige Punkte

- `async fn` deklariert eine asynchrone Funktion
- Async-Funktionen können als nebenläufige Tasks mit `spawn()` gestartet werden
- Async-Funktionen können auch direkt aufgerufen werden (läuft synchron im aktuellen Thread)
- Wenn gespawnt, läuft jeder Task auf seinem **eigenen OS-Thread** (keine Coroutine!)
- Das `await`-Schlüsselwort ist für zukünftige Verwendung reserviert

### Beispiel: Direkter Aufruf vs Spawn

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Direkter Aufruf - läuft synchron
let result1 = factorial(5);  // 120

// Gespawnter Task - läuft auf separatem Thread
let task = spawn(factorial, 5);
let result2 = join(task);  // 120
```

## Task-Spawning

Verwenden Sie `spawn()`, um async-Funktionen **parallel auf separaten OS-Threads** auszuführen:

```hemlock
async fn factorial(n: i32): i32 {
    if (n <= 1) { return 1; }
    return n * factorial(n - 1);
}

// Mehrere Tasks spawnen - diese laufen PARALLEL auf verschiedenen CPU-Kernen!
let t1 = spawn(factorial, 5);  // Thread 1
let t2 = spawn(factorial, 6);  // Thread 2
let t3 = spawn(factorial, 7);  // Thread 3

// Alle drei rechnen gerade gleichzeitig!

// Auf Ergebnisse warten
let f5 = join(t1);  // 120
let f6 = join(t2);  // 720
let f7 = join(t3);  // 5040
```

### Eingebaute Funktionen

#### spawn(async_fn, arg1, arg2, ...)

Erstellt einen neuen Task auf einem neuen pthread, gibt Task-Handle zurück.

**Parameter:**
- `async_fn` - Die auszuführende async-Funktion
- `arg1, arg2, ...` - Argumente, die an die Funktion übergeben werden

**Rückgabe:** Task-Handle (opaker Wert, der mit `join()` oder `detach()` verwendet wird)

**Beispiel:**
```hemlock
async fn process(data: string, count: i32): i32 {
    // ... Verarbeitungslogik
    return count * 2;
}

let task = spawn(process, "test", 42);
```

#### join(task)

Warte auf Task-Abschluss (blockiert bis Thread fertig ist), gibt Ergebnis zurück.

**Parameter:**
- `task` - Task-Handle, das von `spawn()` zurückgegeben wurde

**Rückgabe:** Der von der async-Funktion zurückgegebene Wert

**Beispiel:**
```hemlock
let task = spawn(compute, 1000);
let result = join(task);  // Blockiert bis compute() fertig ist
print(result);
```

**Wichtig:** Jeder Task kann nur einmal gejoined werden. Nachfolgende Joins werden einen Fehler verursachen.

#### detach(task)

Fire-and-Forget-Ausführung (Thread läuft unabhängig, kein Join erlaubt).

**Parameter:**
- `task` - Task-Handle, das von `spawn()` zurückgegeben wurde

**Rückgabe:** `null`

**Beispiel:**
```hemlock
async fn background_work() {
    // Lang laufender Hintergrund-Task
    // ...
}

let task = spawn(background_work);
detach(task);  // Task läuft unabhängig, kann nicht gejoined werden
```

**Wichtig:** Losgelöste Tasks können nicht gejoined werden. Sowohl der pthread als auch die Task-Struktur werden automatisch bereinigt, wenn der Task abgeschlossen ist.

## Channels

Channels bieten thread-sichere Kommunikation zwischen Tasks unter Verwendung eines begrenzten Puffers mit blockierender Semantik.

### Channels erstellen

```hemlock
let ch = channel(10);  // Channel mit Puffergröße 10 erstellen
```

**Parameter:**
- `capacity` (i32) - Maximale Anzahl von Werten, die der Channel halten kann

**Rückgabe:** Channel-Objekt

### Channel-Methoden

#### send(value)

Sende Wert an Channel (blockiert wenn voll).

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
let task = spawn(producer, ch, 5);
```

**Verhalten:**
- Wenn Channel Platz hat, wird Wert sofort hinzugefügt
- Wenn Channel voll ist, blockiert der Sender bis Platz verfügbar wird
- Wenn Channel geschlossen ist, wird Ausnahme geworfen

#### recv()

Empfange Wert von Channel (blockiert wenn leer).

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
let task = spawn(consumer, ch, 5);
```

**Verhalten:**
- Wenn Channel Werte hat, wird nächster Wert sofort zurückgegeben
- Wenn Channel leer ist, blockiert der Empfänger bis Wert verfügbar
- Wenn Channel geschlossen und leer ist, gibt `null` zurück

#### close()

Schließe Channel (recv auf geschlossenem Channel gibt null zurück).

```hemlock
ch.close();
```

**Verhalten:**
- Verhindert weitere `send()`-Operationen (wirft Ausnahme)
- Erlaubt ausstehenden `recv()`-Operationen abzuschließen
- Sobald leer, gibt `recv()` `null` zurück

### Multiplexing mit select()

Die `select()`-Funktion ermöglicht das gleichzeitige Warten auf mehrere Channels und gibt zurück, wenn ein Channel Daten verfügbar hat.

**Signatur:**
```hemlock
select(channels: array, timeout_ms?: i32): object | null
```

**Parameter:**
- `channels` - Array von Channel-Werten
- `timeout_ms` (optional) - Timeout in Millisekunden (-1 oder weglassen für unendliches Warten)

**Rückgabe:**
- `{ channel, value }` - Objekt mit dem Channel, der Daten hatte, und dem empfangenen Wert
- `null` - Bei Timeout (wenn Timeout angegeben wurde)

**Beispiel:**
```hemlock
let ch1 = channel(1);
let ch2 = channel(1);

// Producer-Tasks
spawn(fn() {
    sleep(100);
    ch1.send("von Channel 1");
});

spawn(fn() {
    sleep(50);
    ch2.send("von Channel 2");
});

// Auf erstes Ergebnis warten (ch2 sollte schneller sein)
let result = select([ch1, ch2]);
print(result.value);  // "von Channel 2"

// Auf zweites Ergebnis warten
let result2 = select([ch1, ch2]);
print(result2.value);  // "von Channel 1"
```

**Mit Timeout:**
```hemlock
let ch = channel(1);

// Kein Sender, wird Timeout erreichen
let result = select([ch], 100);  // 100ms Timeout
if (result == null) {
    print("Timeout!");
}
```

**Anwendungsfälle:**
- Warten auf die schnellste von mehreren Datenquellen
- Implementierung von Timeouts bei Channel-Operationen
- Event-Loop-Muster mit mehreren Ereignisquellen
- Fan-in: Zusammenführen mehrerer Channels zu einem

**Fan-in-Muster:**
```hemlock
fn fan_in(channels: array, output: channel) {
    while (true) {
        let result = select(channels);
        if (result == null) {
            break;  // Alle Channels geschlossen
        }
        output.send(result.value);
    }
    output.close();
}
```

### Vollständiges Producer-Consumer-Beispiel

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

// Channel mit Puffergröße erstellen
let ch = channel(10);

// Producer und Consumer spawnen
let p = spawn(producer, ch, 5);
let c = spawn(consumer, ch, 5);

// Auf Abschluss warten
join(p);
let total = join(c);  // 100 (0+10+20+30+40)
print(total);
```

### Multi-Producer, Multi-Consumer

Channels können sicher zwischen mehreren Producern und Consumern geteilt werden:

```hemlock
async fn producer(id: i32, ch, count: i32) {
    let i = 0;
    while (i < count) {
        ch.send(id * 100 + i);
        i = i + 1;
    }
}

async fn consumer(id: i32, ch, count: i32): i32 {
    let sum = 0;
    let i = 0;
    while (i < count) {
        let val = ch.recv();
        sum = sum + val;
        i = i + 1;
    }
    return sum;
}

let ch = channel(20);

// Mehrere Producer
let p1 = spawn(producer, 1, ch, 5);
let p2 = spawn(producer, 2, ch, 5);

// Mehrere Consumer
let c1 = spawn(consumer, 1, ch, 5);
let c2 = spawn(consumer, 2, ch, 5);

// Auf alle warten
join(p1);
join(p2);
let sum1 = join(c1);
let sum2 = join(c2);
print(sum1 + sum2);
```

## Ausnahmeweiterleitung

Ausnahmen, die in gespawnten Tasks geworfen werden, werden beim Join weitergeleitet:

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
    print("Gefangen: " + e);  // "Gefangen: Task fehlgeschlagen!"
}
```

### Ausnahmebehandlungsmuster

**Muster 1: Im Task behandeln**
```hemlock
async fn safe_task() {
    try {
        // riskante Operation
    } catch (e) {
        print("Fehler im Task: " + e);
        return null;
    }
}

let task = spawn(safe_task);
join(task);  // Keine Ausnahme weitergeleitet
```

**Muster 2: An Aufrufer weiterleiten**
```hemlock
async fn task_that_throws() {
    throw "fehler";
}

let task = spawn(task_that_throws);
try {
    join(task);
} catch (e) {
    print("Von Task gefangen: " + e);
}
```

**Muster 3: Losgelöste Tasks mit Ausnahmen**
```hemlock
async fn detached_task() {
    try {
        // Arbeit
    } catch (e) {
        // Muss intern behandelt werden - kann nicht weitergeleitet werden
        print("Fehler: " + e);
    }
}

let task = spawn(detached_task);
detach(task);  // Kann keine Ausnahmen von losgelösten Tasks fangen
```

## Implementierungsdetails

### Threading-Architektur

- **1:1 Threading** - Jeder gespawnte Task erstellt einen dedizierten OS-Thread über `pthread_create()`
- **Kernel-geplant** - Der OS-Kernel verteilt Threads auf verfügbare CPU-Kerne
- **Präemptives Multitasking** - Das OS kann Threads unterbrechen und zwischen ihnen wechseln
- **Kein GIL** - Anders als Python gibt es keinen Global Interpreter Lock, der die Parallelität einschränkt

### Channel-Implementierung

Channels verwenden einen Ringpuffer mit pthread-Synchronisation:

```
Channel-Struktur:
- buffer[] - Array fester Größe von Values
- capacity - Maximale Anzahl von Elementen
- size - Aktuelle Anzahl von Elementen
- head - Leseposition
- tail - Schreibposition
- mutex - pthread_mutex_t für thread-sicheren Zugriff
- not_empty - pthread_cond_t für blockierendes recv
- not_full - pthread_cond_t für blockierendes send
- closed - Boolean-Flag
- refcount - Referenzzähler für Bereinigung
```

**Blockierendes Verhalten:**
- `send()` auf vollem Channel: wartet auf `not_full` Bedingungsvariable
- `recv()` auf leerem Channel: wartet auf `not_empty` Bedingungsvariable
- Beide werden durch die gegenteilige Operation entsprechend signalisiert

### Speicher & Bereinigung

- **Gejoinede Tasks:** Werden automatisch bereinigt, nachdem `join()` zurückkehrt
- **Losgelöste Tasks:** Werden automatisch bereinigt, wenn der Task abgeschlossen ist
- **Channels:** Referenzgezählt und freigegeben, wenn nicht mehr verwendet

## Best Practices

### 1. Channels immer schließen

```hemlock
async fn producer(ch) {
    // ... Werte senden
    ch.close();  // Wichtig: signalisiert, dass keine weiteren Werte kommen
}
```

### 2. Strukturierte Nebenläufigkeit verwenden

Tasks spawnen und im selben Scope joinen:

```hemlock
fn process_data(data) {
    // Tasks spawnen
    let t1 = spawn(worker, data);
    let t2 = spawn(worker, data);

    // Immer vor dem Rückgeben joinen
    let r1 = join(t1);
    let r2 = join(t2);

    return r1 + r2;
}
```

### 3. Ausnahmen angemessen behandeln

```hemlock
async fn task() {
    try {
        // riskante Operation
    } catch (e) {
        // Fehler loggen
        throw e;  // Erneut werfen, wenn Aufrufer es wissen soll
    }
}
```

### 4. Angemessene Channel-Kapazität verwenden

- **Kleine Kapazität (1-10):** Für Koordination/Signalisierung
- **Mittlere Kapazität (10-100):** Für allgemeines Producer-Consumer
- **Große Kapazität (100+):** Für Hochdurchsatz-Szenarien

```hemlock
let signal_ch = channel(1);      // Koordination
let work_ch = channel(50);       // Arbeits-Warteschlange
let buffer_ch = channel(1000);   // Hoher Durchsatz
```

### 5. Nur bei Bedarf loslösen

Bevorzugen Sie `join()` gegenüber `detach()` für besseres Ressourcenmanagement:

```hemlock
// Gut: Join und Ergebnis erhalten
let task = spawn(work);
let result = join(task);

// Detach nur für echtes Fire-and-Forget verwenden
let bg_task = spawn(background_logging);
detach(bg_task);  // Läuft unabhängig
```

## Leistungsmerkmale

### Echte Parallelität

- **N gespawnte Tasks können N CPU-Kerne gleichzeitig nutzen**
- Nachgewiesene Beschleunigung - Stresstests zeigen 8-9x CPU-Zeit vs Wandzeit (mehrere Kerne arbeiten)
- Lineare Skalierung mit Anzahl der Kerne (bis zur Thread-Anzahl)

### Thread-Overhead

- Jeder Task hat ~8KB Stack + pthread-Overhead
- Thread-Erstellungskosten: ~10-20μs
- Kontextwechselkosten: ~1-5μs

### Wann Async verwenden

**Gute Anwendungsfälle:**
- CPU-intensive Berechnungen, die parallelisiert werden können
- I/O-gebundene Operationen (obwohl I/O immer noch blockiert)
- Nebenläufige Verarbeitung unabhängiger Daten
- Pipeline-Architekturen mit Channels

**Nicht ideal für:**
- Sehr kurze Tasks (Thread-Overhead dominiert)
- Tasks mit starker Synchronisation (Contention-Overhead)
- Single-Core-Systeme (kein Parallelitätsvorteil)

### Blockierendes I/O sicher

Blockierende Operationen in einem Task blockieren keine anderen:

```hemlock
async fn reader(filename: string) {
    let f = open(filename, "r");  // Blockiert nur diesen Thread
    let content = f.read();       // Blockiert nur diesen Thread
    f.close();
    return content;
}

// Beide lesen nebenläufig (auf verschiedenen Threads)
let t1 = spawn(reader, "file1.txt");
let t2 = spawn(reader, "file2.txt");

let c1 = join(t1);
let c2 = join(t2);
```

## Thread-Sicherheitsmodell

Hemlock verwendet ein **Message-Passing**-Nebenläufigkeitsmodell, bei dem Tasks über Channels kommunizieren, anstatt gemeinsamen veränderlichen Zustand zu verwenden.

### Argument-Isolation

Wenn Sie einen Task spawnen, werden **Argumente tief kopiert**, um Data Races zu verhindern:

```hemlock
async fn modify_array(arr: array): array {
    arr.push(999);    // Modifiziert die KOPIE, nicht das Original
    arr[0] = -1;
    return arr;
}

let original = [1, 2, 3];
let task = spawn(modify_array, original);
let modified = join(task);

print(original.length);  // 3 - unverändert!
print(modified.length);  // 4 - hat neues Element
```

**Was tief kopiert wird:**
- Arrays (und alle Elemente rekursiv)
- Objekte (und alle Felder rekursiv)
- Strings
- Buffer

**Was geteilt wird (Referenz beibehalten):**
- Channels (der Kommunikationsmechanismus - absichtlich geteilt)
- Task-Handles (für Koordination)
- Funktionen (Code ist unveränderlich)
- Datei-Handles (OS verwaltet nebenläufigen Zugriff)
- Socket-Handles (OS verwaltet nebenläufigen Zugriff)

**Was nicht übergeben werden kann:**
- Rohe Pointer (`ptr`) - verwenden Sie stattdessen `buffer`

### Warum Message-Passing?

Dies folgt Hemlocks "explizit statt implizit"-Philosophie:

```hemlock
// SCHLECHT: Gemeinsamer veränderlicher Zustand (würde Data Races verursachen)
let counter = { value: 0 };
let t1 = spawn(fn() { counter.value = counter.value + 1; });  // Race!
let t2 = spawn(fn() { counter.value = counter.value + 1; });  // Race!

// GUT: Message-Passing über Channels
async fn increment(ch) {
    let val = ch.recv();
    ch.send(val + 1);
}

let ch = channel(1);
ch.send(0);
let t1 = spawn(increment, ch);
join(t1);
let result = ch.recv();  // 1 - keine Race Condition
```

### Thread-Sicherheit der Referenzzählung

Alle Referenzzählungsoperationen verwenden **atomare Operationen**, um Use-after-Free-Bugs zu verhindern:
- `string_retain/release` - atomar
- `array_retain/release` - atomar
- `object_retain/release` - atomar
- `buffer_retain/release` - atomar
- `function_retain/release` - atomar
- `channel_retain/release` - atomar
- `task_retain/release` - atomar

Dies gewährleistet sicheres Speichermanagement auch wenn Werte über Threads geteilt werden.

### Closure-Umgebungszugriff

Tasks haben Zugriff auf die Closure-Umgebung für:
- Eingebaute Funktionen (`print`, `len`, etc.)
- Globale Funktionsdefinitionen
- Konstanten und Variablen

Die Closure-Umgebung wird durch einen pro-Umgebung-Mutex geschützt, was
nebenläufige Lese- und Schreibzugriffe thread-sicher macht:

```hemlock
let x = 10;

async fn read_closure(): i32 {
    return x;  // OK: Lesen von Closure-Variable (thread-sicher)
}

async fn modify_closure() {
    x = 20;  // OK: Schreiben von Closure-Variable (synchronisiert mit Mutex)
}
```

**Hinweis:** Obwohl nebenläufiger Zugriff synchronisiert ist, kann das Modifizieren von gemeinsam genutztem Zustand aus mehreren Tasks immer noch zu logischen Race Conditions führen (nicht-deterministische Reihenfolge). Für vorhersehbares Verhalten verwenden Sie Channels für Task-Kommunikation oder Rückgabewerte von Tasks.

Wenn Sie Daten von einem Task zurückgeben müssen, verwenden Sie den Rückgabewert oder Channels.

## Aktuelle Einschränkungen

### 1. Kein Work-Stealing-Scheduler

Verwendet 1 Thread pro Task, was bei vielen kurzen Tasks ineffizient sein kann.

**Aktuell:** 1000 Tasks = 1000 Threads (hoher Overhead)

**Geplant:** Thread-Pool mit Work-Stealing für bessere Effizienz

### 3. Keine Async-I/O-Integration

Datei-/Netzwerkoperationen blockieren immer noch den Thread:

```hemlock
async fn read_file(path: string) {
    let f = open(path, "r");
    let content = f.read();  // Blockiert den Thread
    f.close();
    return content;
}
```

**Workaround:** Verwenden Sie mehrere Threads für nebenläufige I/O-Operationen

### 4. Feste Channel-Kapazität

Channel-Kapazität wird bei der Erstellung festgelegt und kann nicht geändert werden:

```hemlock
let ch = channel(10);
// Kann nicht dynamisch auf 20 geändert werden
```

### 5. Channel-Größe ist fest

Channel-Puffergröße kann nach der Erstellung nicht geändert werden.

## Häufige Muster

### Paralleles Map

```hemlock
async fn map_worker(ch_in, ch_out, fn_transform) {
    while (true) {
        let val = ch_in.recv();
        if (val == null) { break; }

        let result = fn_transform(val);
        ch_out.send(result);
    }
    ch_out.close();
}

fn parallel_map(data, fn_transform, workers: i32) {
    let ch_in = channel(100);
    let ch_out = channel(100);

    // Worker spawnen
    let tasks = [];
    let i = 0;
    while (i < workers) {
        tasks.push(spawn(map_worker, ch_in, ch_out, fn_transform));
        i = i + 1;
    }

    // Daten senden
    let i = 0;
    while (i < data.length) {
        ch_in.send(data[i]);
        i = i + 1;
    }
    ch_in.close();

    // Ergebnisse sammeln
    let results = [];
    let i = 0;
    while (i < data.length) {
        results.push(ch_out.recv());
        i = i + 1;
    }

    // Auf Worker warten
    let i = 0;
    while (i < tasks.length) {
        join(tasks[i]);
        i = i + 1;
    }

    return results;
}
```

### Pipeline-Architektur

```hemlock
async fn stage1(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val * 2);
    }
    output_ch.close();
}

async fn stage2(input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }
        output_ch.send(val + 10);
    }
    output_ch.close();
}

// Pipeline erstellen
let ch1 = channel(10);
let ch2 = channel(10);
let ch3 = channel(10);

let s1 = spawn(stage1, ch1, ch2);
let s2 = spawn(stage2, ch2, ch3);

// Eingabe einspeisen
ch1.send(1);
ch1.send(2);
ch1.send(3);
ch1.close();

// Ausgabe sammeln
print(ch3.recv());  // 12 (1 * 2 + 10)
print(ch3.recv());  // 14 (2 * 2 + 10)
print(ch3.recv());  // 16 (3 * 2 + 10)

join(s1);
join(s2);
```

### Fan-Out, Fan-In

```hemlock
async fn worker(id: i32, input_ch, output_ch) {
    while (true) {
        let val = input_ch.recv();
        if (val == null) { break; }

        // Wert verarbeiten
        let result = val * id;
        output_ch.send(result);
    }
}

let input = channel(10);
let output = channel(10);

// Fan-out: Mehrere Worker
let workers = 4;
let tasks = [];
let i = 0;
while (i < workers) {
    tasks.push(spawn(worker, i, input, output));
    i = i + 1;
}

// Arbeit senden
let i = 0;
while (i < 10) {
    input.send(i);
    i = i + 1;
}
input.close();

// Fan-in: Alle Ergebnisse sammeln
let results = [];
let i = 0;
while (i < 10) {
    results.push(output.recv());
    i = i + 1;
}

// Auf alle Worker warten
let i = 0;
while (i < tasks.length) {
    join(tasks[i]);
    i = i + 1;
}
```

## Zusammenfassung

Hemlocks Async/Nebenläufigkeitsmodell bietet:

- ✅ Echte Multithread-Parallelität mit OS-Threads
- ✅ Einfache, strukturierte Nebenläufigkeitsprimitive
- ✅ Thread-sichere Channels für Kommunikation
- ✅ Ausnahmeweiterleitung über Tasks
- ✅ Nachgewiesene Leistung auf Multi-Core-Systemen
- ✅ **Argument-Isolation** - Tiefe Kopie verhindert Data Races
- ✅ **Atomare Referenzzählung** - Sicheres Speichermanagement über Threads

Dies macht Hemlock geeignet für:
- Parallele Berechnungen
- Nebenläufige I/O-Operationen
- Pipeline-Architekturen
- Producer-Consumer-Muster

Während die Komplexität vermieden wird von:
- Manuellem Thread-Management
- Low-Level-Synchronisationsprimitiven
- Deadlock-anfälligen Lock-basierten Designs
- Bugs durch gemeinsamen veränderlichen Zustand
