# Datei-API-Referenz

Vollstaendige Referenz fuer Hemlocks Datei-I/O-System.

---

## Uebersicht

Hemlock bietet eine **Dateiobjekt-API** fuer Dateioperationen mit ordnungsgemaesser Fehlerbehandlung und Ressourcenverwaltung. Dateien muessen manuell geoeffnet und geschlossen werden.

**Hauptmerkmale:**
- Dateiobjekt mit Methoden
- Text- und Binaerdaten lesen/schreiben
- Positionierung und Suchen
- Ordnungsgemaesse Fehlermeldungen
- Manuelle Ressourcenverwaltung (kein RAII)

---

## Datei-Typ

**Typ:** `file`

**Beschreibung:** Dateihandle fuer I/O-Operationen

**Eigenschaften (Nur-Lesen):**
- `.path` - Dateipfad (string)
- `.mode` - Oeffnungsmodus (string)
- `.closed` - Ob Datei geschlossen (bool)

---

## Dateien oeffnen

### open

Oeffnet eine Datei zum Lesen, Schreiben oder beides.

**Signatur:**
```hemlock
open(path: string, mode?: string): file
```

**Parameter:**
- `path` - Dateipfad (relativ oder absolut)
- `mode` (optional) - Oeffnungsmodus (Standard: `"r"`)

**Rueckgabe:** Dateiobjekt

**Modi:**
- `"r"` - Lesen (Standard)
- `"w"` - Schreiben (bestehende Datei abschneiden)
- `"a"` - Anhaengen
- `"r+"` - Lesen und Schreiben
- `"w+"` - Lesen und Schreiben (abschneiden)
- `"a+"` - Lesen und Anhaengen

**Beispiele:**
```hemlock
// Lesemodus (Standard)
let f = open("data.txt");
let f_read = open("data.txt", "r");

// Schreibmodus (abschneiden)
let f_write = open("output.txt", "w");

// Anhaengemodus
let f_append = open("log.txt", "a");

// Lesen/Schreiben-Modus
let f_rw = open("data.bin", "r+");

// Lesen/Schreiben (abschneiden)
let f_rw_trunc = open("output.bin", "w+");

// Lesen/Anhaengen
let f_ra = open("log.txt", "a+");
```

**Fehlerbehandlung:**
```hemlock
try {
    let f = open("missing.txt", "r");
} catch (e) {
    print("Oeffnen fehlgeschlagen:", e);
    // Fehler: Konnte 'missing.txt' nicht oeffnen: Datei oder Verzeichnis nicht gefunden
}
```

**Wichtig:** Dateien muessen manuell mit `f.close()` geschlossen werden um Dateideskriptor-Lecks zu vermeiden.

---

## Datei-Methoden

### Lesen

#### read

Liest Text aus Datei.

**Signatur:**
```hemlock
file.read(size?: i32): string
```

**Parameter:**
- `size` (optional) - Anzahl der zu lesenden Bytes (wenn weggelassen, bis EOF lesen)

**Rueckgabe:** String mit Dateiinhalt

**Beispiele:**
```hemlock
let f = open("data.txt", "r");

// Gesamte Datei lesen
let all = f.read();
print(all);

// Bestimmte Anzahl Bytes lesen
let chunk = f.read(1024);

f.close();
```

**Verhalten:**
- Liest ab aktueller Dateiposition
- Gibt leeren String bei EOF zurueck
- Bewegt Dateiposition vorwaerts

**Fehler:**
- Lesen aus geschlossener Datei
- Lesen aus Nur-Schreiben-Datei

---

#### read_bytes

Liest Binaerdaten aus Datei.

**Signatur:**
```hemlock
file.read_bytes(size: i32): buffer
```

**Parameter:**
- `size` - Anzahl der zu lesenden Bytes

**Rueckgabe:** Buffer mit Binaerdaten

**Beispiele:**
```hemlock
let f = open("data.bin", "r");

// 256 Bytes lesen
let binary = f.read_bytes(256);
print(binary.length);       // 256

// Binaerdaten verarbeiten
let i = 0;
while (i < binary.length) {
    print(binary[i]);
    i = i + 1;
}

f.close();
```

**Verhalten:**
- Liest exakte Anzahl Bytes
- Gibt Buffer zurueck (kein String)
- Bewegt Dateiposition vorwaerts

---

### Schreiben

#### write

Schreibt Text in Datei.

**Signatur:**
```hemlock
file.write(data: string): i32
```

**Parameter:**
- `data` - Zu schreibender String

**Rueckgabe:** Anzahl geschriebener Bytes (i32)

**Beispiele:**
```hemlock
let f = open("output.txt", "w");

// Text schreiben
let written = f.write("Hello, World!\n");
print("Geschrieben", written, "Bytes");

// Mehrere Schreibvorgaenge
f.write("Zeile 1\n");
f.write("Zeile 2\n");
f.write("Zeile 3\n");

f.close();
```

**Verhalten:**
- Schreibt an aktueller Dateiposition
- Gibt Anzahl geschriebener Bytes zurueck
- Bewegt Dateiposition vorwaerts

**Fehler:**
- Schreiben in geschlossene Datei
- Schreiben in Nur-Lesen-Datei

---

#### write_bytes

Schreibt Binaerdaten in Datei.

**Signatur:**
```hemlock
file.write_bytes(data: buffer): i32
```

**Parameter:**
- `data` - Zu schreibender Buffer

**Rueckgabe:** Anzahl geschriebener Bytes (i32)

**Beispiele:**
```hemlock
let f = open("output.bin", "w");

// Buffer erstellen
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

// Buffer schreiben
let written = f.write_bytes(buf);
print("Geschrieben", written, "Bytes");

f.close();
```

**Verhalten:**
- Schreibt Buffer-Inhalt in Datei
- Gibt Anzahl geschriebener Bytes zurueck
- Bewegt Dateiposition vorwaerts

---

### Positionieren

#### seek

Bewegt Dateiposition zu bestimmtem Byte-Offset.

**Signatur:**
```hemlock
file.seek(position: i32): i32
```

**Parameter:**
- `position` - Byte-Offset vom Dateianfang

**Rueckgabe:** Neue Dateiposition (i32)

**Beispiele:**
```hemlock
let f = open("data.txt", "r");

// Zu Byte 100 springen
f.seek(100);

// Von dieser Position lesen
let chunk = f.read(50);

// Zum Anfang zuruecksetzen
f.seek(0);

// Vom Anfang lesen
let all = f.read();

f.close();
```

**Verhalten:**
- Setzt Dateiposition auf absoluten Offset
- Gibt neue Position zurueck
- Suchen hinter EOF ist erlaubt (erzeugt Loch in Datei beim Schreiben)

---

#### tell

Gibt aktuelle Dateiposition zurueck.

**Signatur:**
```hemlock
file.tell(): i32
```

**Rueckgabe:** Aktueller Byte-Offset vom Dateianfang (i32)

**Beispiele:**
```hemlock
let f = open("data.txt", "r");

print(f.tell());        // 0 (am Anfang)

f.read(100);
print(f.tell());        // 100 (nach Lesen)

f.seek(50);
print(f.tell());        // 50 (nach Suchen)

f.close();
```

---

### Schliessen

#### close

Schliesst Datei (idempotent).

**Signatur:**
```hemlock
file.close(): null
```

**Rueckgabe:** `null`

**Beispiele:**
```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();

// Sicher mehrmals aufzurufen
f.close();  // Kein Fehler
f.close();  // Kein Fehler
```

**Verhalten:**
- Schliesst Dateihandle
- Leert ausstehende Schreibvorgaenge
- Idempotent (sicher mehrmals aufzurufen)
- Setzt `.closed`-Eigenschaft auf `true`

**Wichtig:** Schliessen Sie Dateien immer wenn fertig um Dateideskriptor-Lecks zu vermeiden.

---

## Datei-Eigenschaften

### .path

Gibt Dateipfad zurueck.

**Typ:** `string`

**Zugriff:** Nur-Lesen

**Beispiele:**
```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);          // "/path/to/file.txt"
f.close();
```

---

### .mode

Gibt Oeffnungsmodus zurueck.

**Typ:** `string`

**Zugriff:** Nur-Lesen

**Beispiele:**
```hemlock
let f = open("data.txt", "r");
print(f.mode);          // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);         // "w"
f2.close();
```

---

### .closed

Prueft ob Datei geschlossen ist.

**Typ:** `bool`

**Zugriff:** Nur-Lesen

**Beispiele:**
```hemlock
let f = open("data.txt", "r");
print(f.closed);        // false

f.close();
print(f.closed);        // true
```

---

## Fehlerbehandlung

Alle Dateioperationen enthalten ordnungsgemaesse Fehlermeldungen mit Kontext:

### Datei nicht gefunden
```hemlock
let f = open("missing.txt", "r");
// Fehler: Konnte 'missing.txt' nicht oeffnen: Datei oder Verzeichnis nicht gefunden
```

### Lesen aus geschlossener Datei
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Fehler: Kann nicht aus geschlossener Datei 'data.txt' lesen
```

### Schreiben in Nur-Lesen-Datei
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Fehler: Kann nicht in Datei 'readonly.txt' schreiben, die im Nur-Lesen-Modus geoeffnet wurde
```

### Mit try/catch
```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    print(content);
} catch (e) {
    print("Dateifehler:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Ressourcenverwaltungsmuster

### Grundmuster

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Mit Fehlerbehandlung

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Immer schliessen, auch bei Fehler
}
```

### Sicheres Muster

```hemlock
let f = null;
try {
    f = open("data.txt", "r");
    let content = f.read();
    // ... Inhalt verarbeiten ...
} catch (e) {
    print("Fehler:", e);
} finally {
    if (f != null && !f.closed) {
        f.close();
    }
}
```

---

## Verwendungsbeispiele

### Gesamte Datei lesen

```hemlock
fn read_file(filename: string): string {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content;
}

let text = read_file("data.txt");
print(text);
```

### Textdatei schreiben

```hemlock
fn write_file(filename: string, content: string) {
    let f = open(filename, "w");
    f.write(content);
    f.close();
}

write_file("output.txt", "Hello, World!\n");
```

### An Datei anhaengen

```hemlock
fn append_file(filename: string, line: string) {
    let f = open(filename, "a");
    f.write(line + "\n");
    f.close();
}

append_file("log.txt", "Log-Eintrag 1");
append_file("log.txt", "Log-Eintrag 2");
```

### Binaerdatei lesen

```hemlock
fn read_binary(filename: string, size: i32): buffer {
    let f = open(filename, "r");
    let data = f.read_bytes(size);
    f.close();
    return data;
}

let binary = read_binary("data.bin", 256);
print("Gelesen", binary.length, "Bytes");
```

### Binaerdatei schreiben

```hemlock
fn write_binary(filename: string, data: buffer) {
    let f = open(filename, "w");
    f.write_bytes(data);
    f.close();
}

let buf = buffer(10);
buf[0] = 65;
write_binary("output.bin", buf);
```

### Datei Zeile fuer Zeile lesen

```hemlock
fn read_lines(filename: string): array {
    let f = open(filename, "r");
    let content = f.read();
    f.close();
    return content.split("\n");
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Zeile", i, ":", lines[i]);
    i = i + 1;
}
```

### Datei kopieren

```hemlock
fn copy_file(src: string, dest: string) {
    let f_in = open(src, "r");
    let f_out = open(dest, "w");

    let content = f_in.read();
    f_out.write(content);

    f_in.close();
    f_out.close();
}

copy_file("input.txt", "output.txt");
```

### Datei in Stuecken lesen

```hemlock
fn process_chunks(filename: string) {
    let f = open(filename, "r");

    while (true) {
        let chunk = f.read(1024);  // 1KB auf einmal lesen
        if (chunk.length == 0) {
            break;  // EOF
        }

        // Stueck verarbeiten
        print("Verarbeite", chunk.length, "Bytes");
    }

    f.close();
}

process_chunks("large_file.txt");
```

---

## Vollstaendige Methodenuebersicht

| Methode       | Signatur                 | Rueckgabe | Beschreibung                 |
|---------------|--------------------------|-----------|------------------------------|
| `read`        | `(size?: i32)`           | `string`  | Text lesen                   |
| `read_bytes`  | `(size: i32)`            | `buffer`  | Binaerdaten lesen            |
| `write`       | `(data: string)`         | `i32`     | Text schreiben               |
| `write_bytes` | `(data: buffer)`         | `i32`     | Binaerdaten schreiben        |
| `seek`        | `(position: i32)`        | `i32`     | Dateiposition setzen         |
| `tell`        | `()`                     | `i32`     | Dateiposition holen          |
| `close`       | `()`                     | `null`    | Datei schliessen (idempotent)|

---

## Vollstaendige Eigenschaftsuebersicht

| Eigenschaft | Typ      | Zugriff    | Beschreibung             |
|-------------|----------|------------|--------------------------|
| `.path`     | `string` | Nur-Lesen  | Dateipfad                |
| `.mode`     | `string` | Nur-Lesen  | Oeffnungsmodus           |
| `.closed`   | `bool`   | Nur-Lesen  | Ob Datei geschlossen     |

---

## Migration von alter API

**Alte API (Entfernt):**
- `read_file(path)` - Verwenden Sie `open(path, "r").read()`
- `write_file(path, data)` - Verwenden Sie `open(path, "w").write(data)`
- `append_file(path, data)` - Verwenden Sie `open(path, "a").write(data)`
- `file_exists(path)` - Noch kein Ersatz

**Migrationsbeispiel:**
```hemlock
// Alt (v0.0)
let content = read_file("data.txt");
write_file("output.txt", content);

// Neu (v0.1)
let f = open("data.txt", "r");
let content = f.read();
f.close();

let f2 = open("output.txt", "w");
f2.write(content);
f2.close();
```

---

## Siehe auch

- [Eingebaute Funktionen](builtins.md) - `open()`-Funktion
- [Speicher-API](memory-api.md) - Buffer-Typ
- [String-API](string-api.md) - String-Methoden zur Textverarbeitung
