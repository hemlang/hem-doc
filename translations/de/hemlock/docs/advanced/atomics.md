# Atomare Operationen

Hemlock bietet atomare Operationen für **lock-freie nebenläufige Programmierung**. Diese Operationen ermöglichen sichere Manipulation von gemeinsamem Speicher über mehrere Threads ohne traditionelle Locks oder Mutexe.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Wann Atomics verwenden](#wann-atomics-verwenden)
- [Speichermodell](#speichermodell)
- [Atomares Laden und Speichern](#atomares-laden-und-speichern)
- [Fetch-and-Modify-Operationen](#fetch-and-modify-operationen)
- [Compare-and-Swap (CAS)](#compare-and-swap-cas)
- [Atomarer Austausch](#atomarer-austausch)
- [Speicherbarriere](#speicherbarriere)
- [Funktionsreferenz](#funktionsreferenz)
- [Häufige Muster](#häufige-muster)
- [Best Practices](#best-practices)
- [Einschränkungen](#einschränkungen)

---

## Überblick

Atomare Operationen sind **unteilbare** Operationen, die ohne Möglichkeit der Unterbrechung abgeschlossen werden. Wenn ein Thread eine atomare Operation ausführt, kann kein anderer Thread die Operation in einem teilweise abgeschlossenen Zustand beobachten.

**Hauptmerkmale:**
- Alle Operationen verwenden **sequenzielle Konsistenz** (`memory_order_seq_cst`)
- Unterstützte Typen: **i32** und **i64**
- Operationen arbeiten mit Rohpointern, die mit `alloc()` alloziert wurden
- Thread-sicher ohne explizite Locks

**Verfügbare Operationen:**
- Load/Store - Werte atomar lesen und schreiben
- Add/Sub - Arithmetische Operationen, die den alten Wert zurückgeben
- And/Or/Xor - Bitweise Operationen, die den alten Wert zurückgeben
- CAS - Compare-and-Swap für bedingte Aktualisierungen
- Exchange - Werte atomar tauschen
- Fence - Vollständige Speicherbarriere

---

## Wann Atomics verwenden

**Verwenden Sie Atomics für:**
- Zähler, die über Tasks geteilt werden (z.B. Anfragezähler, Fortschrittsverfolgung)
- Flags und Statusindikatoren
- Lock-freie Datenstrukturen
- Einfache Synchronisationsprimitive
- Leistungskritischen nebenläufigen Code

**Verwenden Sie stattdessen Channels wenn:**
- Komplexe Daten zwischen Tasks übergeben werden
- Producer-Consumer-Muster implementiert werden
- Message-Passing-Semantik benötigt wird

**Beispiel-Anwendungsfall - Geteilter Zähler:**
```hemlock
// Geteilten Zähler allozieren
let counter = alloc(4);
ptr_write_i32(counter, 0);

async fn worker(counter: ptr, id: i32) {
    let i = 0;
    while (i < 1000) {
        atomic_add_i32(counter, 1);
        i = i + 1;
    }
}

// Mehrere Worker spawnen
let t1 = spawn(worker, counter, 1);
let t2 = spawn(worker, counter, 2);
let t3 = spawn(worker, counter, 3);

join(t1);
join(t2);
join(t3);

// Zähler wird exakt 3000 sein (keine Data Races)
print(atomic_load_i32(counter));

free(counter);
```

---

## Speichermodell

Alle atomaren Operationen in Hemlock verwenden **sequenzielle Konsistenz** (`memory_order_seq_cst`), was die stärksten Speicherordnungsgarantien bietet:

1. **Atomarität**: Jede Operation ist unteilbar
2. **Totale Ordnung**: Alle Threads sehen die gleiche Reihenfolge von Operationen
3. **Keine Umordnung**: Operationen werden nicht vom Compiler oder der CPU umgeordnet

Dies macht das Nachdenken über nebenläufigen Code einfacher, auf Kosten von etwas potentieller Leistung im Vergleich zu schwächeren Speicherordnungen.

---

## Atomares Laden und Speichern

### atomic_load_i32 / atomic_load_i64

Atomar einen Wert aus dem Speicher lesen.

**Signatur:**
```hemlock
atomic_load_i32(ptr: ptr): i32
atomic_load_i64(ptr: ptr): i64
```

**Parameter:**
- `ptr` - Pointer auf die Speicherstelle (muss korrekt ausgerichtet sein)

**Rückgabe:** Der Wert an der Speicherstelle

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 42);

let value = atomic_load_i32(p);
print(value);  // 42

free(p);
```

---

### atomic_store_i32 / atomic_store_i64

Atomar einen Wert in den Speicher schreiben.

**Signatur:**
```hemlock
atomic_store_i32(ptr: ptr, value: i32): null
atomic_store_i64(ptr: ptr, value: i64): null
```

**Parameter:**
- `ptr` - Pointer auf die Speicherstelle
- `value` - Zu speichernder Wert

**Rückgabe:** `null`

**Beispiel:**
```hemlock
let p = alloc(8);

atomic_store_i64(p, 5000000000);
print(atomic_load_i64(p));  // 5000000000

free(p);
```

---

## Fetch-and-Modify-Operationen

Diese Operationen modifizieren atomar einen Wert und geben den **alten** (vorherigen) Wert zurück.

### atomic_add_i32 / atomic_add_i64

Atomar zu einem Wert addieren.

**Signatur:**
```hemlock
atomic_add_i32(ptr: ptr, value: i32): i32
atomic_add_i64(ptr: ptr, value: i64): i64
```

**Rückgabe:** Der **alte** Wert (vor der Addition)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_add_i32(p, 10);
print(old);                    // 100 (alter Wert)
print(atomic_load_i32(p));     // 110 (neuer Wert)

free(p);
```

---

### atomic_sub_i32 / atomic_sub_i64

Atomar von einem Wert subtrahieren.

**Signatur:**
```hemlock
atomic_sub_i32(ptr: ptr, value: i32): i32
atomic_sub_i64(ptr: ptr, value: i64): i64
```

**Rückgabe:** Der **alte** Wert (vor der Subtraktion)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_sub_i32(p, 25);
print(old);                    // 100 (alter Wert)
print(atomic_load_i32(p));     // 75 (neuer Wert)

free(p);
```

---

### atomic_and_i32 / atomic_and_i64

Atomar bitweises UND ausführen.

**Signatur:**
```hemlock
atomic_and_i32(ptr: ptr, value: i32): i32
atomic_and_i64(ptr: ptr, value: i64): i64
```

**Rückgabe:** Der **alte** Wert (vor dem UND)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xFF);  // 255 in binär: 11111111

let old = atomic_and_i32(p, 0x0F);  // UND mit 00001111
print(old);                    // 255 (alter Wert)
print(atomic_load_i32(p));     // 15 (0xFF & 0x0F = 0x0F)

free(p);
```

---

### atomic_or_i32 / atomic_or_i64

Atomar bitweises ODER ausführen.

**Signatur:**
```hemlock
atomic_or_i32(ptr: ptr, value: i32): i32
atomic_or_i64(ptr: ptr, value: i64): i64
```

**Rückgabe:** Der **alte** Wert (vor dem ODER)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0x0F);  // 15 in binär: 00001111

let old = atomic_or_i32(p, 0xF0);  // ODER mit 11110000
print(old);                    // 15 (alter Wert)
print(atomic_load_i32(p));     // 255 (0x0F | 0xF0 = 0xFF)

free(p);
```

---

### atomic_xor_i32 / atomic_xor_i64

Atomar bitweises XOR ausführen.

**Signatur:**
```hemlock
atomic_xor_i32(ptr: ptr, value: i32): i32
atomic_xor_i64(ptr: ptr, value: i64): i64
```

**Rückgabe:** Der **alte** Wert (vor dem XOR)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 0xAA);  // 170 in binär: 10101010

let old = atomic_xor_i32(p, 0xFF);  // XOR mit 11111111
print(old);                    // 170 (alter Wert)
print(atomic_load_i32(p));     // 85 (0xAA ^ 0xFF = 0x55)

free(p);
```

---

## Compare-and-Swap (CAS)

Die mächtigste atomare Operation. Vergleicht atomar den aktuellen Wert mit einem erwarteten Wert und ersetzt ihn bei Übereinstimmung durch einen neuen Wert.

### atomic_cas_i32 / atomic_cas_i64

**Signatur:**
```hemlock
atomic_cas_i32(ptr: ptr, expected: i32, desired: i32): bool
atomic_cas_i64(ptr: ptr, expected: i64, desired: i64): bool
```

**Parameter:**
- `ptr` - Pointer auf die Speicherstelle
- `expected` - Wert, den wir erwarten vorzufinden
- `desired` - Wert, der gespeichert wird, wenn die Erwartung übereinstimmt

**Rückgabe:**
- `true` - Tausch erfolgreich (Wert war `expected`, ist jetzt `desired`)
- `false` - Tausch fehlgeschlagen (Wert war nicht `expected`, unverändert)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

// CAS erfolgreich: Wert ist 100, tausche zu 999
let success1 = atomic_cas_i32(p, 100, 999);
print(success1);               // true
print(atomic_load_i32(p));     // 999

// CAS fehlgeschlagen: Wert ist 999, nicht 100
let success2 = atomic_cas_i32(p, 100, 888);
print(success2);               // false
print(atomic_load_i32(p));     // 999 (unverändert)

free(p);
```

**Anwendungsfälle:**
- Implementierung von Locks und Semaphoren
- Lock-freie Datenstrukturen
- Optimistische Nebenläufigkeitskontrolle
- Atomare bedingte Aktualisierungen

---

## Atomarer Austausch

Atomar einen Wert tauschen und den alten Wert zurückgeben.

### atomic_exchange_i32 / atomic_exchange_i64

**Signatur:**
```hemlock
atomic_exchange_i32(ptr: ptr, value: i32): i32
atomic_exchange_i64(ptr: ptr, value: i64): i64
```

**Parameter:**
- `ptr` - Pointer auf die Speicherstelle
- `value` - Neuer zu speichernder Wert

**Rückgabe:** Der **alte** Wert (vor dem Austausch)

**Beispiel:**
```hemlock
let p = alloc(4);
ptr_write_i32(p, 100);

let old = atomic_exchange_i32(p, 200);
print(old);                    // 100 (alter Wert)
print(atomic_load_i32(p));     // 200 (neuer Wert)

free(p);
```

---

## Speicherbarriere

Eine vollständige Speicherbarriere, die sicherstellt, dass alle Speicheroperationen vor der Barriere für alle Threads sichtbar sind, bevor irgendwelche Operationen nach der Barriere.

### atomic_fence

**Signatur:**
```hemlock
atomic_fence(): null
```

**Rückgabe:** `null`

**Beispiel:**
```hemlock
// Sicherstellen, dass alle vorherigen Schreiboperationen sichtbar sind
atomic_fence();
```

**Hinweis:** In den meisten Fällen benötigen Sie keine expliziten Barrieren, da alle atomaren Operationen bereits sequenzielle Konsistenz verwenden. Barrieren sind nützlich, wenn Sie nicht-atomare Speicheroperationen synchronisieren müssen.

---

## Funktionsreferenz

### i32-Operationen

| Funktion | Signatur | Rückgabe | Beschreibung |
|----------|----------|----------|--------------|
| `atomic_load_i32` | `(ptr)` | `i32` | Wert atomar laden |
| `atomic_store_i32` | `(ptr, value)` | `null` | Wert atomar speichern |
| `atomic_add_i32` | `(ptr, value)` | `i32` | Addieren und alten Wert zurückgeben |
| `atomic_sub_i32` | `(ptr, value)` | `i32` | Subtrahieren und alten Wert zurückgeben |
| `atomic_and_i32` | `(ptr, value)` | `i32` | Bitweises UND und alten Wert zurückgeben |
| `atomic_or_i32` | `(ptr, value)` | `i32` | Bitweises ODER und alten Wert zurückgeben |
| `atomic_xor_i32` | `(ptr, value)` | `i32` | Bitweises XOR und alten Wert zurückgeben |
| `atomic_cas_i32` | `(ptr, expected, desired)` | `bool` | Compare-and-Swap |
| `atomic_exchange_i32` | `(ptr, value)` | `i32` | Austauschen und alten Wert zurückgeben |

### i64-Operationen

| Funktion | Signatur | Rückgabe | Beschreibung |
|----------|----------|----------|--------------|
| `atomic_load_i64` | `(ptr)` | `i64` | Wert atomar laden |
| `atomic_store_i64` | `(ptr, value)` | `null` | Wert atomar speichern |
| `atomic_add_i64` | `(ptr, value)` | `i64` | Addieren und alten Wert zurückgeben |
| `atomic_sub_i64` | `(ptr, value)` | `i64` | Subtrahieren und alten Wert zurückgeben |
| `atomic_and_i64` | `(ptr, value)` | `i64` | Bitweises UND und alten Wert zurückgeben |
| `atomic_or_i64` | `(ptr, value)` | `i64` | Bitweises ODER und alten Wert zurückgeben |
| `atomic_xor_i64` | `(ptr, value)` | `i64` | Bitweises XOR und alten Wert zurückgeben |
| `atomic_cas_i64` | `(ptr, expected, desired)` | `bool` | Compare-and-Swap |
| `atomic_exchange_i64` | `(ptr, value)` | `i64` | Austauschen und alten Wert zurückgeben |

### Speicherbarriere

| Funktion | Signatur | Rückgabe | Beschreibung |
|----------|----------|----------|--------------|
| `atomic_fence` | `()` | `null` | Vollständige Speicherbarriere |

---

## Häufige Muster

### Muster: Atomarer Zähler

```hemlock
// Thread-sicherer Zähler
let counter = alloc(4);
ptr_write_i32(counter, 0);

fn increment(): i32 {
    return atomic_add_i32(counter, 1);
}

fn decrement(): i32 {
    return atomic_sub_i32(counter, 1);
}

fn get_count(): i32 {
    return atomic_load_i32(counter);
}

// Verwendung
increment();  // Gibt 0 zurück (alter Wert)
increment();  // Gibt 1 zurück
increment();  // Gibt 2 zurück
print(get_count());  // 3

free(counter);
```

### Muster: Spinlock

```hemlock
// Einfache Spinlock-Implementierung
let lock = alloc(4);
ptr_write_i32(lock, 0);  // 0 = entsperrt, 1 = gesperrt

fn acquire() {
    // Drehen bis wir erfolgreich Lock von 0 auf 1 setzen
    while (!atomic_cas_i32(lock, 0, 1)) {
        // Busy-Wait
    }
}

fn release() {
    atomic_store_i32(lock, 0);
}

// Verwendung
acquire();
// ... kritischer Abschnitt ...
release();

free(lock);
```

### Muster: Einmalige Initialisierung

```hemlock
let initialized = alloc(4);
ptr_write_i32(initialized, 0);  // 0 = nicht initialisiert, 1 = initialisiert

fn ensure_initialized() {
    // Versuchen, derjenige zu sein, der initialisiert
    if (atomic_cas_i32(initialized, 0, 1)) {
        // Wir haben das Rennen gewonnen, führe Initialisierung durch
        do_expensive_init();
    }
    // Andernfalls bereits initialisiert
}
```

### Muster: Atomares Flag

```hemlock
let flag = alloc(4);
ptr_write_i32(flag, 0);

fn set_flag() {
    atomic_store_i32(flag, 1);
}

fn clear_flag() {
    atomic_store_i32(flag, 0);
}

fn test_and_set(): bool {
    // Gibt true zurück, wenn Flag bereits gesetzt war
    return atomic_exchange_i32(flag, 1) == 1;
}

fn check_flag(): bool {
    return atomic_load_i32(flag) == 1;
}
```

### Muster: Begrenzter Zähler

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);
let max_value = 100;

fn try_increment(): bool {
    while (true) {
        let current = atomic_load_i32(counter);
        if (current >= max_value) {
            return false;  // Am Maximum
        }
        if (atomic_cas_i32(counter, current, current + 1)) {
            return true;  // Erfolgreich inkrementiert
        }
        // CAS fehlgeschlagen, ein anderer Thread hat modifiziert - erneut versuchen
    }
}
```

---

## Best Practices

### 1. Korrekte Ausrichtung verwenden

Pointer müssen für den Datentyp korrekt ausgerichtet sein:
- i32: 4-Byte-Ausrichtung
- i64: 8-Byte-Ausrichtung

Speicher von `alloc()` ist typischerweise korrekt ausgerichtet.

### 2. Abstraktionen höherer Ebene bevorzugen

Wenn möglich, verwenden Sie Channels für Inter-Task-Kommunikation. Atomics sind auf niedrigerer Ebene und erfordern sorgfältiges Nachdenken.

```hemlock
// Bevorzugen Sie dies:
let ch = channel(10);
spawn(fn() { ch.send(result); });
let value = ch.recv();

// Gegenüber manueller atomarer Koordination, wenn angemessen
```

### 3. ABA-Problem beachten

CAS kann unter dem ABA-Problem leiden: ein Wert ändert sich von A zu B und zurück zu A. Ihr CAS ist erfolgreich, aber der Zustand könnte sich dazwischen geändert haben.

### 4. Vor dem Teilen initialisieren

Initialisieren Sie atomare Variablen immer, bevor Sie Tasks spawnen, die auf sie zugreifen:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);  // Initialisieren VOR dem Spawnen

let task = spawn(worker, counter);
```

### 5. Nach Abschluss aller Tasks freigeben

Geben Sie atomaren Speicher nicht frei, während Tasks möglicherweise noch darauf zugreifen:

```hemlock
let counter = alloc(4);
ptr_write_i32(counter, 0);

let t1 = spawn(worker, counter);
let t2 = spawn(worker, counter);

join(t1);
join(t2);

// Jetzt sicher zum Freigeben
free(counter);
```

---

## Einschränkungen

### Aktuelle Einschränkungen

1. **Nur i32 und i64 unterstützt** - Keine atomaren Operationen für andere Typen
2. **Keine Pointer-Atomics** - Können Pointer nicht atomar laden/speichern
3. **Nur sequenzielle Konsistenz** - Keine schwächeren Speicherordnungen verfügbar
4. **Keine atomaren Fließkommazahlen** - Verwenden Sie bei Bedarf Integer-Darstellung

### Plattformhinweise

- Atomare Operationen verwenden unter der Haube C11 `<stdatomic.h>`
- Verfügbar auf allen Plattformen, die POSIX-Threads unterstützen
- Garantiert lock-frei auf modernen 64-Bit-Systemen

---

## Siehe auch

- [Async/Nebenläufigkeit](async-concurrency.md) - Task-Spawning und Channels
- [Speicherverwaltung](../language-guide/memory.md) - Pointer- und Buffer-Allokation
- [Speicher-API](../reference/memory-api.md) - Allokationsfunktionen
