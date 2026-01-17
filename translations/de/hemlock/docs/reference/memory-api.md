# Speicher-API-Referenz

Vollständige Referenz für Hemlocks Speicherverwaltungsfunktionen und Pointer-Typen.

---

## Übersicht

Hemlock bietet **manuelle Speicherverwaltung** mit expliziter Allokation und Deallokation. Speicher wird durch zwei Pointer-Typen verwaltet: Roh-Pointer (`ptr`) und sichere Buffer (`buffer`).

**Grundprinzipien:**
- Explizite Allokation und Deallokation
- Keine Garbage Collection
- Benutzer verantwortlich für Aufruf von `free()`
- Interne Referenzzaehlung für Scope/Neuzuweisungssicherheit (siehe unten)

### Interne Referenzzaehlung

Die Laufzeit verwendet Referenzzaehlung intern zur Verwaltung von Objektlebenszeiten über Scopes. Für die meisten lokalen Variablen ist die Bereinigung automatisch.

**Automatisch (kein `free()` nötig):**
- Lokale Variablen von referenzgezaehlten Typen (buffer, array, object, string) werden freigegeben wenn Scope endet
- Alte Werte werden freigegeben wenn Variablen neu zugewiesen werden
- Container-Elemente werden freigegeben wenn Container freigegeben werden

**Manuelles `free()` erforderlich:**
- Roh-Pointer von `alloc()` - immer
- Fruehe Bereinigung vor Scope-Ende
- Langlebige/globale Daten

Siehe [Speicherverwaltungs-Leitfaden](../language-guide/memory.md#internal-reference-counting) für Details.

---

## Pointer-Typen

### ptr (Roh-Pointer)

**Typ:** `ptr`

**Beschreibung:** Rohe Speicheradresse ohne Grenzenprüfung oder Verfolgung.

**Größe:** 8 Bytes

**Anwendungsfaelle:**
- Low-Level-Speicheroperationen
- FFI (Foreign Function Interface)
- Maximale Leistung (kein Overhead)

**Sicherheit:** Unsicher - keine Grenzenprüfung, Benutzer muss Lebensdauer verfolgen

**Beispiele:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);
```

---

### buffer (Sicherer Buffer)

**Typ:** `buffer`

**Beschreibung:** Sicherer Pointer-Wrapper mit Grenzenprüfung.

**Struktur:** Pointer + Länge + Kapazität + Referenzzaehler

**Eigenschaften:**
- `.length` - Buffergroesse (i32)
- `.capacity` - Allokierte Kapazität (i32)

**Anwendungsfaelle:**
- Die meisten Speicherallokationen
- Wenn Sicherheit wichtig ist
- Dynamische Arrays

**Sicherheit:** Grenzenprüfung bei Indexzugriff

**Referenzzaehlung:** Buffer sind intern referenzgezählt. Automatisch freigegeben wenn Scope endet oder Variable neu zugewiesen wird. Verwenden Sie `free()` für fruehe Bereinigung oder langlebige Daten.

**Beispiele:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // Grenzenprüfung
print(b.length);        // 64
free(b);
```

---

## Speicherallokationsfunktionen

### alloc

Allokiert Roh-Speicher.

**Signatur:**
```hemlock
alloc(size: i32): ptr
```

**Parameter:**
- `size` - Anzahl der zu allokierenden Bytes

**Rückgabe:** Pointer zum allokierten Speicher (`ptr`)

**Beispiele:**
```hemlock
let p = alloc(1024);        // 1KB allokieren
memset(p, 0, 1024);         // Auf Null initialisieren
free(p);                    // Wenn fertig freigeben

// Für Struktur allokieren
let struct_size = 16;
let p2 = alloc(struct_size);
```

**Verhalten:**
- Gibt uninitialisierten Speicher zurück
- Speicher muss manuell freigegeben werden
- Gibt `null` bei Allokationsfehler zurück (Aufrufer muss prüfen)

**Siehe auch:** `buffer()` für sicherere Alternative

---

### buffer

Allokiert sicheren Buffer mit Grenzenprüfung.

**Signatur:**
```hemlock
buffer(size: i32): buffer
```

**Parameter:**
- `size` - Buffergroesse in Bytes

**Rückgabe:** Buffer-Objekt

**Beispiele:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256
print(buf.capacity);        // 256

// Zugriff mit Grenzenprüfung
buf[0] = 65;                // 'A'
buf[255] = 90;              // 'Z'
// buf[256] = 0;            // FEHLER: außerhalb der Grenzen

free(buf);
```

**Eigenschaften:**
- `.length` - Aktuelle Größe (i32)
- `.capacity` - Allokierte Kapazität (i32)

**Verhalten:**
- Initialisiert Speicher auf Null
- Bietet Grenzenprüfung bei Indexzugriff
- Gibt `null` bei Allokationsfehler zurück (Aufrufer muss prüfen)
- Muss manuell freigegeben werden

---

### free

Gibt allokierten Speicher frei.

**Signatur:**
```hemlock
free(ptr: ptr | buffer): null
```

**Parameter:**
- `ptr` - Pointer oder Buffer zum Freigeben

**Rückgabe:** `null`

**Beispiele:**
```hemlock
// Roh-Pointer freigeben
let p = alloc(1024);
free(p);

// Buffer freigeben
let buf = buffer(256);
free(buf);
```

**Verhalten:**
- Gibt mit `alloc()` oder `buffer()` allokierten Speicher frei
- Doppeltes Freigeben verursacht Absturz (Benutzerverantwortung zu vermeiden)
- Freigeben ungültiger Pointer verursacht undefiniertes Verhalten

**Wichtig:** Was Sie allokieren, geben Sie frei. Keine automatische Bereinigung.

---

### realloc

Aendert Größe von allokiertem Speicher.

**Signatur:**
```hemlock
realloc(ptr: ptr, new_size: i32): ptr
```

**Parameter:**
- `ptr` - Pointer zur Groessenaenderung
- `new_size` - Neue Größe in Bytes

**Rückgabe:** Pointer zum vergroesserten Speicher (kann andere Adresse sein)

**Beispiele:**
```hemlock
let p = alloc(100);
// ... Speicher verwenden ...

// Mehr Platz benötigt
p = realloc(p, 200);        // Jetzt 200 Bytes
// ... erweiterten Speicher verwenden ...

free(p);
```

**Verhalten:**
- Kann Speicher an neue Position verschieben
- Erhält vorhandene Daten (bis Minimum aus alter/neuer Größe)
- Alter Pointer ist nach erfolgreichem realloc ungültig (zurueckgegebenen Pointer verwenden)
- Wenn new_size kleiner, werden Daten abgeschnitten
- Gibt `null` bei Allokationsfehler zurück (Original-Pointer bleibt gültig)

**Wichtig:** Immer auf `null` prüfen und Pointer-Variable mit Ergebnis aktualisieren.

---

## Speicheroperationen

### memset

Fuellt Speicher mit Byte-Wert.

**Signatur:**
```hemlock
memset(ptr: ptr, byte: i32, size: i32): null
```

**Parameter:**
- `ptr` - Pointer zum Speicher
- `byte` - Byte-Wert zum Fuellen (0-255)
- `size` - Anzahl der zu fuellenden Bytes

**Rückgabe:** `null`

**Beispiele:**
```hemlock
let p = alloc(100);

// Speicher nullen
memset(p, 0, 100);

// Mit bestimmtem Wert fuellen
memset(p, 0xFF, 100);

// Buffer initialisieren
let buf = alloc(256);
memset(buf, 65, 256);       // Mit 'A' fuellen

free(p);
free(buf);
```

**Verhalten:**
- Schreibt Byte-Wert in jedes Byte im Bereich
- Byte-Wert wird auf 8 Bits abgeschnitten (0-255)
- Keine Grenzenprüfung (unsicher)

---

### memcpy

Kopiert Speicher von Quelle zu Ziel.

**Signatur:**
```hemlock
memcpy(dest: ptr, src: ptr, size: i32): null
```

**Parameter:**
- `dest` - Ziel-Pointer
- `src` - Quell-Pointer
- `size` - Anzahl der zu kopierenden Bytes

**Rückgabe:** `null`

**Beispiele:**
```hemlock
let src = alloc(100);
let dest = alloc(100);

// Quelle initialisieren
memset(src, 65, 100);

// Zum Ziel kopieren
memcpy(dest, src, 100);

// dest enthält jetzt gleiche Daten wie src

free(src);
free(dest);
```

**Verhalten:**
- Kopiert Byte für Byte von src zu dest
- Keine Grenzenprüfung (unsicher)
- Ueberlappende Bereiche haben undefiniertes Verhalten (vorsichtig verwenden)

---

## Typisierte Speicheroperationen

### sizeof

Gibt Größe eines Typs in Bytes zurück.

**Signatur:**
```hemlock
sizeof(type): i32
```

**Parameter:**
- `type` - Typ-Bezeichner (z.B. `i32`, `f64`, `ptr`)

**Rückgabe:** Größe in Bytes (i32)

**Typgroessen:**

| Typ | Größe (Bytes) |
|-----|-----------------|
| `i8` | 1 |
| `i16` | 2 |
| `i32`, `integer` | 4 |
| `i64` | 8 |
| `u8`, `byte` | 1 |
| `u16` | 2 |
| `u32` | 4 |
| `u64` | 8 |
| `f32` | 4 |
| `f64`, `number` | 8 |
| `bool` | 1 |
| `ptr` | 8 |
| `rune` | 4 |

**Beispiele:**
```hemlock
let int_size = sizeof(i32);      // 4
let ptr_size = sizeof(ptr);      // 8
let float_size = sizeof(f64);    // 8
let byte_size = sizeof(u8);      // 1
let rune_size = sizeof(rune);    // 4

// Array-Allokationsgroesse berechnen
let count = 100;
let total = sizeof(i32) * count; // 400 Bytes
```

**Verhalten:**
- Gibt 0 für unbekannte Typen zurück
- Akzeptiert sowohl Typ-Bezeichner als auch Typ-Strings

---

### talloc

Allokiert Array von typisierten Werten.

**Signatur:**
```hemlock
talloc(type, count: i32): ptr
```

**Parameter:**
- `type` - Zu allokierender Typ (z.B. `i32`, `f64`, `ptr`)
- `count` - Anzahl der Elemente (muss positiv sein)

**Rückgabe:** Pointer zum allokierten Array, oder `null` bei Allokationsfehler

**Beispiele:**
```hemlock
let arr = talloc(i32, 100);      // Array von 100 i32s (400 Bytes)
let floats = talloc(f64, 50);    // Array von 50 f64s (400 Bytes)
let bytes = talloc(u8, 1024);    // Array von 1024 Bytes

// Immer auf Allokationsfehler prüfen
if (arr == null) {
    panic("Allokation fehlgeschlagen");
}

// Allokierten Speicher verwenden
// ...

free(arr);
free(floats);
free(bytes);
```

**Verhalten:**
- Allokiert `sizeof(type) * count` Bytes
- Gibt uninitialisierten Speicher zurück
- Speicher muss manuell mit `free()` freigegeben werden
- Gibt `null` bei Allokationsfehler zurück (Aufrufer muss prüfen)
- Bricht ab wenn count nicht positiv ist

---

## Buffer-Eigenschaften

### .length

Gibt Buffergroesse zurück.

**Typ:** `i32`

**Zugriff:** Nur-Lesen

**Beispiele:**
```hemlock
let buf = buffer(256);
print(buf.length);          // 256

let buf2 = buffer(1024);
print(buf2.length);         // 1024
```

---

### .capacity

Gibt Bufferkapazitaet zurück.

**Typ:** `i32`

**Zugriff:** Nur-Lesen

**Beispiele:**
```hemlock
let buf = buffer(256);
print(buf.capacity);        // 256
```

**Hinweis:** Derzeit sind `.length` und `.capacity` für mit `buffer()` erstellte Buffer gleich.

---

## Verwendungsmuster

### Grundlegendes Allokationsmuster

```hemlock
// Allokieren
let p = alloc(1024);
if (p == null) {
    panic("Allokation fehlgeschlagen");
}

// Verwenden
memset(p, 0, 1024);

// Freigeben
free(p);
```

### Sicheres Buffer-Muster

```hemlock
// Buffer allokieren
let buf = buffer(256);
if (buf == null) {
    panic("Buffer-Allokation fehlgeschlagen");
}

// Mit Grenzenprüfung verwenden
let i = 0;
while (i < buf.length) {
    buf[i] = i;
    i = i + 1;
}

// Freigeben
free(buf);
```

### Dynamisches Wachstumsmuster

```hemlock
let size = 100;
let p = alloc(size);
if (p == null) {
    panic("Allokation fehlgeschlagen");
}

// ... Speicher verwenden ...

// Mehr Platz benötigt - auf Fehler prüfen
let new_p = realloc(p, 200);
if (new_p == null) {
    // Original-Pointer noch gültig, aufraeumen
    free(p);
    panic("Realloc fehlgeschlagen");
}
p = new_p;
size = 200;

// ... erweiterten Speicher verwenden ...

free(p);
```

### Speicherkopie-Muster

```hemlock
let original = alloc(100);
memset(original, 65, 100);

// Kopie erstellen
let copy = alloc(100);
memcpy(copy, original, 100);

free(original);
free(copy);
```

---

## Sicherheitsueberlegungen

**Hemlocks Speicherverwaltung ist UNSICHER by Design:**

### Häufige Fallstricke

**1. Speicherlecks**
```hemlock
// SCHLECHT: Speicherleck
fn create_buffer() {
    let p = alloc(1024);
    return null;  // Speicher geleakt!
}

// GUT: Ordnungsgemaesse Bereinigung
fn create_buffer() {
    let p = alloc(1024);
    // ... Speicher verwenden ...
    free(p);
    return null;
}
```

**2. Verwendung nach Freigabe**
```hemlock
// SCHLECHT: Verwendung nach Freigabe
let p = alloc(100);
free(p);
memset(p, 0, 100);  // ABSTURZ: Verwendung von freigegebenem Speicher

// GUT: Nach Freigabe nicht verwenden
let p2 = alloc(100);
memset(p2, 0, 100);
free(p2);
// p2 nach hier nicht beruehren
```

**3. Doppelte Freigabe**
```hemlock
// SCHLECHT: Doppelte Freigabe
let p = alloc(100);
free(p);
free(p);  // ABSTURZ: Doppelte Freigabe

// GUT: Einmal freigeben
let p2 = alloc(100);
free(p2);
```

**4. Buffer-Überlauf (ptr)**
```hemlock
// SCHLECHT: Buffer-Überlauf mit ptr
let p = alloc(10);
memset(p, 65, 100);  // ABSTURZ: Schreiben über Allokation hinaus

// GUT: Buffer für Grenzenprüfung verwenden
let buf = buffer(10);
// buf[100] = 65;  // FEHLER: Grenzenprüfung schlaegt fehl
```

**5. Haengende Pointer**
```hemlock
// SCHLECHT: Haengender Pointer
let p1 = alloc(100);
let p2 = p1;
free(p1);
memset(p2, 0, 100);  // ABSTURZ: p2 haengt

// GUT: Eigentum sorgfaeltig verfolgen
let p = alloc(100);
// ... p verwenden ...
free(p);
// Keine anderen Referenzen auf p behalten
```

**6. Ungeprüfter Allokationsfehler**
```hemlock
// SCHLECHT: Nicht auf null prüfen
let p = alloc(1000000000);  // Kann bei wenig Speicher fehlschlagen
memset(p, 0, 1000000000);   // ABSTURZ: p ist null

// GUT: Immer Allokationsergebnis prüfen
let p2 = alloc(1000000000);
if (p2 == null) {
    panic("Speicher erschoepft");
}
memset(p2, 0, 1000000000);
free(p2);
```

---

## Wann was verwenden

### `buffer()` verwenden wenn:
- Sie Grenzenprüfung benötigen
- Mit dynamischen Daten arbeiten
- Sicherheit wichtig ist
- Hemlock lernen

### `alloc()` verwenden wenn:
- Maximale Leistung benötigt
- FFI/Schnittstelle zu C
- Sie exaktes Speicherlayout kennen
- Sie ein Experte sind

### `realloc()` verwenden wenn:
- Allokationen vergroessern/verkleinern
- Dynamische Arrays
- Sie Daten erhalten müssen

---

## Vollständige Funktionsuebersicht

| Funktion  | Signatur                               | Rückgabe | Beschreibung               |
|-----------|----------------------------------------|-----------|----------------------------|
| `alloc`   | `(size: i32)`                          | `ptr`     | Roh-Speicher allokieren    |
| `buffer`  | `(size: i32)`                          | `buffer`  | Sicheren Buffer allokieren |
| `free`    | `(ptr: ptr \| buffer)`                 | `null`    | Speicher freigeben         |
| `realloc` | `(ptr: ptr, new_size: i32)`            | `ptr`     | Allokation vergroessern    |
| `memset`  | `(ptr: ptr, byte: i32, size: i32)`     | `null`    | Speicher fuellen           |
| `memcpy`  | `(dest: ptr, src: ptr, size: i32)`     | `null`    | Speicher kopieren          |
| `sizeof`  | `(type)`                               | `i32`     | Typgroesse in Bytes holen  |
| `talloc`  | `(type, count: i32)`                   | `ptr`     | Typisiertes Array allokieren |

---

## Siehe auch

- [Typsystem](type-system.md) - Pointer- und Buffer-Typen
- [Eingebaute Funktionen](builtins.md) - Alle eingebauten Funktionen
- [String-API](string-api.md) - String `.to_bytes()`-Methode
