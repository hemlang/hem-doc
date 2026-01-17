# Speicherverwaltung

Hemlock setzt auf **manuelle Speicherverwaltung** mit expliziter Kontrolle über Allokation und Deallokation. Dieser Leitfaden behandelt Hemlocks Speichermodell, die zwei Zeigertypen und die vollständige Speicher-API.

---

## Speicher 101: Die Grundlagen

**Neu in der Programmierung?** Beginnen Sie hier. Wenn Sie Speicherverwaltung bereits verstehen, springen Sie zu [Philosophie](#philosophie).

### Was ist Speicherverwaltung?

Wenn Ihr Programm Daten speichern muss (Text, Zahlen, Listen), braucht es Platz dafuer. Dieser Platz kommt aus dem Arbeitsspeicher Ihres Computers (RAM). Bei der Speicherverwaltung geht es um:

1. **Platz bekommen** - Speicher anfordern, wenn Sie ihn brauchen
2. **Platz nutzen** - Ihre Daten lesen und schreiben
3. **Zurückgeben** - Speicher zurückgeben, wenn Sie fertig sind

### Warum ist das wichtig?

Stellen Sie sich eine Bibliothek mit begrenzten Buechern vor:
- Wenn Sie ständig Buecher ausleihen und nie zurückgeben, gibt es irgendwann keine mehr
- Wenn Sie versuchen, ein bereits zurueckgegebenes Buch zu lesen, werden Sie verwirrt oder verursachen Probleme

Speicher funktioniert genauso. Wenn Sie vergessen, Speicher zurückzugeben, verbraucht Ihr Programm langsam immer mehr (ein "Speicherleck"). Wenn Sie versuchen, Speicher nach der Rückgabe zu nutzen, passieren schlimme Dinge.

### Die gute Nachricht

**Meistens müssen Sie nicht darueber nachdenken!**

Hemlock raumt die meisten gaengigen Typen automatisch auf:

```hemlock
fn example() {
    let name = "Alice";       // Hemlock verwaltet dies
    let numbers = [1, 2, 3];  // Und dies
    let person = { age: 30 }; // Und dies auch

    // Wenn die Funktion endet, wird alles automatisch aufgeraeumt!
}
```

### Wann Sie darueber nachdenken MUESSEN

Sie brauchen manuelle Speicherverwaltung nur bei der Verwendung von:

1. **`alloc()`** - rohe Speicherallokation (gibt `ptr` zurück)
2. **`buffer()`** - wenn Sie frueh freigeben möchten (optional - wird am Scope-Ende automatisch freigegeben)

```hemlock
// Dies braucht manuelle Bereinigung:
let raw = alloc(100);   // Roher Speicher - SIE müssen ihn freigeben
// ... raw verwenden ...
free(raw);              // Erforderlich! Sonst haben Sie ein Speicherleck

// Dies wird automatisch aufgeraeumt (aber Sie KOENNEN frueh freigeben):
let buf = buffer(100);  // Sicherer Buffer
// ... buf verwenden ...
// free(buf);           // Optional - wird automatisch freigegeben wenn Scope endet
```

### Die einfache Regel

> **Wenn Sie `alloc()` aufrufen, müssen Sie `free()` aufrufen.**
>
> Alles andere wird für Sie erledigt.

### Was sollten Sie verwenden?

| Situation | Verwenden Sie dies | Warum |
|-----------|-------------------|-------|
| **Gerade erst angefangen** | `buffer()` | Sicher, mit Bereichsprüfung, automatische Bereinigung |
| **Byte-Speicherung benötigt** | `buffer()` | Sicher und einfach |
| **Arbeit mit C-Bibliotheken (FFI)** | `alloc()` / `ptr` | Erforderlich für C-Interop |
| **Maximale Leistung** | `alloc()` / `ptr` | Kein Overhead durch Bereichsprüfung |
| **Nicht sicher** | `buffer()` | Immer die sicherere Wahl |

### Schnelles Beispiel: Sicher vs Roh

```hemlock
// EMPFOHLEN: Sicherer Buffer
fn safe_example() {
    let data = buffer(10);
    data[0] = 65;           // OK
    data[5] = 66;           // OK
    // data[100] = 67;      // FEHLER - Hemlock stoppt Sie (Bereichsprüfung)
    free(data);             // Aufraeumen
}

// FORTGESCHRITTEN: Roher Zeiger (nur wenn Sie ihn brauchen)
fn raw_example() {
    let data = alloc(10);
    *data = 65;             // OK
    *(data + 5) = 66;       // OK
    *(data + 100) = 67;     // GEFAHR - Keine Bereichsprüfung, beschaedigt Speicher!
    free(data);             // Aufraeumen
}
```

**Beginnen Sie mit `buffer()`. Verwenden Sie `alloc()` nur, wenn Sie speziell rohe Zeiger brauchen.**

---

## Philosophie

Hemlock folgt dem Prinzip der expliziten Speicherverwaltung mit vernuenftigen Standardeinstellungen:
- Keine Garbage Collection (keine unvorhersehbaren Pausen)
- Internes Referenzzaehlen für gängige Typen (String, Array, Object, Buffer)
- Rohe Zeiger (`ptr`) erfordern manuelles `free()`

Dieser hybride Ansatz gibt Ihnen vollständige Kontrolle, wenn nötig (rohe Zeiger), während er gängige Fehler für typische Anwendungsfaelle verhindert (referenzgezaehlte Typen werden beim Scope-Ende automatisch freigegeben).

## Internes Referenzzaehlen

Die Laufzeitumgebung verwendet **internes Referenzzaehlen** zur Verwaltung von Objektlebenszeiten. Für die meisten lokalen Variablen referenzgezaehlter Typen ist die Bereinigung automatisch und deterministisch.

### Was Referenzzaehlen handhabt

Die Laufzeitumgebung verwaltet Referenzzaehler automatisch, wenn:

1. **Variablen neu zugewiesen werden** - der alte Wert wird freigegeben:
   ```hemlock
   let x = "first";   // ref_count = 1
   x = "second";      // "first" wird intern freigegeben, "second" ref_count = 1
   ```

2. **Scopes beendet werden** - lokale Variablen werden freigegeben:
   ```hemlock
   fn example() {
       let arr = [1, 2, 3];  // ref_count = 1
   }  // arr wird freigegeben wenn Funktion zurückkehrt
   ```

3. **Container freigegeben werden** - Elemente werden freigegeben:
   ```hemlock
   let arr = [obj1, obj2];
   free(arr);  // ref_counts von obj1 und obj2 werden dekrementiert
   ```

### Wann Sie `free()` brauchen vs Wann es automatisch ist

**Automatisch (kein `free()` nötig):** Lokale Variablen referenzgezaehlter Typen werden freigegeben, wenn der Scope endet:

```hemlock
fn process_data() {
    let arr = [1, 2, 3];
    let obj = { name: "test" };
    let buf = buffer(64);
    // ... verwenden ...
}  // Alles wird automatisch freigegeben wenn Funktion zurückkehrt - kein free() nötig
```

**Manuelles `free()` erforderlich:**

1. **Rohe Zeiger** - `alloc()` hat kein Referenzzaehlen:
   ```hemlock
   let p = alloc(64);
   // ... p verwenden ...
   free(p);  // Immer erforderlich - leckt sonst
   ```

2. **Fruehe Bereinigung** - vor Scope-Ende freigeben um Speicher frueher freizugeben:
   ```hemlock
   fn long_running() {
       let big = buffer(10000000);  // 10MB
       // ... fertig mit big ...
       free(big);  // Jetzt freigeben, nicht auf Funktionsrueckkehr warten
       // ... mehr Arbeit die big nicht braucht ...
   }
   ```

3. **Langlebige Daten** - globale oder in persistenten Strukturen gespeicherte Daten:
   ```hemlock
   let cache = {};  // Modul-Ebene, lebt bis Programmende wenn nicht freigegeben

   fn cleanup() {
       free(cache);  // Manuelle Bereinigung für langlebige Daten
   }
   ```

### Referenzzaehlen vs Garbage Collection

| Aspekt | Hemlock Referenzzaehlen | Garbage Collection |
|--------|------------------------|-------------------|
| Bereinigungszeitpunkt | Deterministisch (sofort wenn ref 0 erreicht) | Nicht-deterministisch (GC entscheidet wann) |
| Benutzerverantwortung | Muss `free()` aufrufen | Vollautomatisch |
| Laufzeitpausen | Keine | "Stop the World"-Pausen |
| Sichtbarkeit | Verstecktes Implementierungsdetail | Normalerweise unsichtbar |
| Zyklen | Mit visited-set Tracking behandelt | Durch Tracing behandelt |

### Welche Typen haben Referenzzaehlen

| Typ | Referenzgezählt | Anmerkungen |
|-----|-----------------|-------------|
| `ptr` | Nein | Erfordert immer manuelles `free()` |
| `buffer` | Ja | Auto-Freigabe bei Scope-Ende; manuelles `free()` für fruehe Bereinigung |
| `array` | Ja | Auto-Freigabe bei Scope-Ende; manuelles `free()` für fruehe Bereinigung |
| `object` | Ja | Auto-Freigabe bei Scope-Ende; manuelles `free()` für fruehe Bereinigung |
| `string` | Ja | Vollautomatisch, kein `free()` nötig |
| `function` | Ja | Vollautomatisch (Closure-Umgebungen) |
| `task` | Ja | Thread-sicheres atomares Referenzzaehlen |
| `channel` | Ja | Thread-sicheres atomares Referenzzaehlen |
| Primitive | Nein | Stack-allokiert, keine Heap-Allokation |

### Warum dieses Design?

Dieser hybride Ansatz gibt Ihnen:
- **Explizite Kontrolle** - Sie entscheiden, wann deallokiert wird
- **Sicherheit vor Scope-Fehlern** - Neuzuweisung leckt nicht
- **Vorhersagbare Leistung** - Keine GC-Pausen
- **Closure-Unterstützung** - Funktionen können sicher Variablen erfassen

Die Philosophie bleibt: Sie haben die Kontrolle, aber die Laufzeit hilft, gängige Fehler wie Lecks bei Neuzuweisung oder Doppel-Freigabe in Containern zu verhindern.

## Die zwei Zeigertypen

Hemlock bietet zwei unterschiedliche Zeigertypen, jeder mit verschiedenen Sicherheitseigenschaften:

### `ptr` - Roher Zeiger (Gefaehrlich)

Rohe Zeiger sind **nur Adressen** mit minimalen Sicherheitsgarantien:

```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Sie müssen daran denken freizugeben
```

**Eigenschaften:**
- Nur eine 8-Byte-Adresse
- Keine Bereichsprüfung
- Keine Laengenverfolgung
- Benutzer verwaltet Lebensdauer vollständig
- Für Experten und FFI

**Anwendungsfaelle:**
- Low-Level-Systemprogrammierung
- Foreign Function Interface (FFI)
- Leistungskritischer Code
- Wenn Sie vollständige Kontrolle brauchen

**Gefahren:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Weit über Allokation hinaus - erlaubt aber gefaehrlich
free(p);
let x = *p;       // Dangling Pointer - undefiniertes Verhalten
free(p);          // Double-Free - wird abstuerzen
```

### `buffer` - Sichere Huelle (Empfohlen)

Buffer bieten **bereichsgeprueften Zugriff** während sie weiterhin manuelle Deallokation erfordern:

```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // bereichsgeprueft
print(b.length);        // 64
free(b);                // weiterhin manuell
```

**Eigenschaften:**
- Zeiger + Länge + Kapazität
- Bereichsgeprueft bei Zugriff
- Erfordert weiterhin manuelles `free()`
- Bessere Standardwahl für den meisten Code

**Properties:**
```hemlock
let buf = buffer(100);
print(buf.length);      // 100 (aktuelle Größe)
print(buf.capacity);    // 100 (allokierte Kapazität)
```

**Bereichsprüfung:**
```hemlock
let buf = buffer(10);
buf[5] = 42;      // OK
buf[100] = 42;    // FEHLER: Index außerhalb der Grenzen
```

## Speicher-API

### Kernallokation

**`alloc(bytes)` - Rohen Speicher allokieren**
```hemlock
let p = alloc(1024);  // 1KB allokieren, gibt ptr zurück
// ... Speicher verwenden
free(p);
```

**`buffer(size)` - Sicheren Buffer allokieren**
```hemlock
let buf = buffer(256);  // 256-Byte-Buffer allokieren
buf[0] = 65;            // 'A'
buf[1] = 66;            // 'B'
free(buf);
```

**`free(ptr)` - Speicher freigeben**
```hemlock
let p = alloc(100);
free(p);  // Muss freigegeben werden um Speicherleck zu vermeiden

let buf = buffer(100);
free(buf);  // Funktioniert sowohl für ptr als auch buffer
```

**Wichtig:** `free()` funktioniert sowohl für `ptr`- als auch für `buffer`-Typen.

### Speicheroperationen

**`memset(ptr, byte, size)` - Speicher fuellen**
```hemlock
let p = alloc(100);
memset(p, 0, 100);     // 100 Bytes nullen
memset(p, 65, 10);     // Erste 10 Bytes mit 'A' fuellen
free(p);
```

**`memcpy(dest, src, size)` - Speicher kopieren**
```hemlock
let src = alloc(50);
let dst = alloc(50);
memset(src, 42, 50);
memcpy(dst, src, 50);  // 50 Bytes von src nach dst kopieren
free(src);
free(dst);
```

**`realloc(ptr, size)` - Allokation anpassen**
```hemlock
let p = alloc(100);
// ... 100 Bytes verwenden
p = realloc(p, 200);   // Auf 200 Bytes anpassen
// ... 200 Bytes verwenden
free(p);
```

**Hinweis:** Nach `realloc()` kann der alte Zeiger ungültig sein. Verwenden Sie immer den zurueckgegebenen Zeiger.

### Typisierte Allokation

Hemlock bietet typisierte Allokationshelfer für Bequemlichkeit:

```hemlock
let arr = talloc(i32, 100);  // 100 i32-Werte allokieren (400 Bytes)
let size = sizeof(i32);      // Gibt 4 zurück (Bytes)
```

**`sizeof(type)`** gibt die Größe in Bytes eines Typs zurück:
- `sizeof(i8)` / `sizeof(u8)` -> 1
- `sizeof(i16)` / `sizeof(u16)` -> 2
- `sizeof(i32)` / `sizeof(u32)` / `sizeof(f32)` -> 4
- `sizeof(i64)` / `sizeof(u64)` / `sizeof(f64)` -> 8
- `sizeof(ptr)` -> 8 (auf 64-Bit-Systemen)

**`talloc(type, count)`** allokiert `count` Elemente vom Typ `type`:

```hemlock
let ints = talloc(i32, 10);   // 40 Bytes für 10 i32-Werte
let floats = talloc(f64, 5);  // 40 Bytes für 5 f64-Werte
free(ints);
free(floats);
```

## Gängige Muster

### Muster: Allokieren, Verwenden, Freigeben

Das grundlegende Muster für Speicherverwaltung:

```hemlock
// 1. Allokieren
let data = alloc(1024);

// 2. Verwenden
memset(data, 0, 1024);
// ... Arbeit erledigen

// 3. Freigeben
free(data);
```

### Muster: Sichere Buffer-Verwendung

Bevorzugen Sie Buffer für bereichsgeprueften Zugriff:

```hemlock
let buf = buffer(256);

// Sichere Iteration
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

free(buf);
```

### Muster: Ressourcenverwaltung mit try/finally

Sicherstellen der Bereinigung auch bei Fehlern:

```hemlock
let data = alloc(1024);
try {
    // ... riskante Operationen
    process(data);
} finally {
    free(data);  // Immer freigegeben, auch bei Fehler
}
```

## Ueberlegungen zur Speichersicherheit

### Double-Free

**Erlaubt aber wird abstuerzen:**
```hemlock
let p = alloc(100);
free(p);
free(p);  // ABSTURZ: Double-Free erkannt
```

**Praevention:**
```hemlock
let p = alloc(100);
free(p);
p = null;  // Nach Freigabe auf null setzen

if (p != null) {
    free(p);  // Wird nicht ausgeführt
}
```

### Dangling Pointers

**Erlaubt aber undefiniertes Verhalten:**
```hemlock
let p = alloc(100);
*p = 42;      // OK
free(p);
let x = *p;   // UNDEFINIERT: Lesen von freigegebenem Speicher
```

**Praevention:** Greifen Sie nach der Freigabe nicht auf Speicher zu.

### Speicherlecks

**Leicht zu erstellen, schwer zu debuggen:**
```hemlock
fn leak_memory() {
    let p = alloc(1000);
    // Vergessen freizugeben!
    return;  // Speicher leckt
}
```

**Praevention:** Paaren Sie immer `alloc()` mit `free()`:
```hemlock
fn safe_function() {
    let p = alloc(1000);
    try {
        // ... p verwenden
    } finally {
        free(p);  // Immer freigegeben
    }
}
```

### Zeigerarithmetik

**Erlaubt aber gefaehrlich:**
```hemlock
let p = alloc(10);
let q = p + 100;  // Weit über Allokationsgrenze hinaus
*q = 42;          // UNDEFINIERT: Schreiben außerhalb der Grenzen
free(p);
```

**Verwenden Sie Buffer für Bereichsprüfung:**
```hemlock
let buf = buffer(10);
buf[100] = 42;  // FEHLER: Bereichsprüfung verhindert Überlauf
```

## Best Practices

1. **Standardmäßig `buffer`** - Verwenden Sie `buffer` außer Sie brauchen speziell rohe `ptr`
2. **alloc/free abgleichen** - Jedes `alloc()` sollte genau ein `free()` haben
3. **try/finally verwenden** - Bereinigung mit Ausnahmebehandlung sicherstellen
4. **Nach free auf null setzen** - Zeiger nach Freigabe auf `null` setzen um Use-after-free zu erkennen
5. **Bereichsprüfung** - Buffer-Indexierung für automatische Bereichsprüfung verwenden
6. **Ownership dokumentieren** - Klar machen, welcher Code jede Allokation besitzt und freigibt

## Beispiele

### Beispiel: Dynamischer String Builder

```hemlock
fn build_message(count: i32): ptr {
    let size = count * 10;
    let buf = alloc(size);

    let i = 0;
    while (i < count) {
        memset(buf + (i * 10), 65 + i, 10);
        i = i + 1;
    }

    return buf;  // Aufrufer muss freigeben
}

let msg = build_message(5);
// ... msg verwenden
free(msg);
```

### Beispiel: Sichere Array-Operationen

```hemlock
fn process_array(size: i32) {
    let arr = buffer(size);

    try {
        // Array fuellen
        let i = 0;
        while (i < arr.length) {
            arr[i] = i * 2;
            i = i + 1;
        }

        // Verarbeiten
        i = 0;
        while (i < arr.length) {
            print(arr[i]);
            i = i + 1;
        }
    } finally {
        free(arr);  // Immer aufraeumen
    }
}
```

### Beispiel: Memory Pool Muster

```hemlock
// Einfacher Memory Pool (vereinfacht)
let pool = alloc(10000);
let pool_offset = 0;

fn pool_alloc(size: i32): ptr {
    if (pool_offset + size > 10000) {
        throw "Pool erschoepft";
    }

    let ptr = pool + pool_offset;
    pool_offset = pool_offset + size;
    return ptr;
}

// Pool verwenden
let p1 = pool_alloc(100);
let p2 = pool_alloc(200);

// Gesamten Pool auf einmal freigeben
free(pool);
```

## Einschränkungen

Aktuelle Einschränkungen, die zu beachten sind:

- **Rohe Zeiger erfordern manuelles free** - `alloc()` gibt `ptr` ohne Referenzzaehlen zurück
- **Keine benutzerdefinierten Allokatoren** - Nur System malloc/free

**Hinweis:** Referenzgezaehlte Typen (String, Array, Object, Buffer) werden automatisch freigegeben, wenn der Scope endet. Nur rohe `ptr` von `alloc()` erfordert explizites `free()`.

## Verwandte Themen

- [Strings](strings.md) - String-Speicherverwaltung und UTF-8-Kodierung
- [Arrays](arrays.md) - Dynamische Arrays und ihre Speichereigenschaften
- [Objects](objects.md) - Objekt-Allokation und Lebensdauer
- [Error Handling](error-handling.md) - Verwendung von try/finally für Bereinigung

## Siehe auch

- **Design-Philosophie**: Siehe CLAUDE.md Abschnitt "Memory Management"
- **Typsystem**: Siehe [Types](types.md) für `ptr` und `buffer` Typdetails
- **FFI**: Rohe Zeiger sind essentiell für Foreign Function Interface
