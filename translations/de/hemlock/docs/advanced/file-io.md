# Datei-I/O in Hemlock

Hemlock bietet eine **Dateiobjekt-API** für Dateioperationen mit ordnungsgemäßer Fehlerbehandlung und Ressourcenverwaltung.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Dateien öffnen](#dateien-öffnen)
- [Dateimethoden](#dateimethoden)
- [Dateieigenschaften](#dateieigenschaften)
- [Fehlerbehandlung](#fehlerbehandlung)
- [Ressourcenverwaltung](#ressourcenverwaltung)
- [Vollständige API-Referenz](#vollständige-api-referenz)
- [Häufige Muster](#häufige-muster)
- [Best Practices](#best-practices)

## Überblick

Die Dateiobjekt-API bietet:

- **Explizite Ressourcenverwaltung** - Dateien müssen manuell geschlossen werden
- **Mehrere Öffnungsmodi** - Lesen, Schreiben, Anhängen, Lesen/Schreiben
- **Text- und Binäroperationen** - Sowohl Text- als auch Binärdaten lesen/schreiben
- **Seek-Unterstützung** - Wahlfreier Zugriff innerhalb von Dateien
- **Umfassende Fehlermeldungen** - Kontextbewusste Fehlerberichterstattung

**Wichtig:** Dateien werden nicht automatisch geschlossen. Sie müssen `f.close()` aufrufen, um Dateideskriptor-Lecks zu vermeiden.

## Dateien öffnen

Verwenden Sie `open(path, mode?)`, um eine Datei zu öffnen:

```hemlock
let f = open("data.txt", "r");     // Lesemodus (Standard)
let f2 = open("output.txt", "w");  // Schreibmodus (abschneiden)
let f3 = open("log.txt", "a");     // Anhängemodus
let f4 = open("data.bin", "r+");   // Lese-/Schreibmodus
```

### Öffnungsmodi

| Modus | Beschreibung | Datei muss existieren | Schneidet ab | Position |
|-------|--------------|----------------------|--------------|----------|
| `"r"` | Lesen (Standard) | Ja | Nein | Anfang |
| `"w"` | Schreiben | Nein (erstellt) | Ja | Anfang |
| `"a"` | Anhängen | Nein (erstellt) | Nein | Ende |
| `"r+"` | Lesen und Schreiben | Ja | Nein | Anfang |
| `"w+"` | Lesen und Schreiben | Nein (erstellt) | Ja | Anfang |
| `"a+"` | Lesen und Anhängen | Nein (erstellt) | Nein | Ende |

### Beispiele

**Bestehende Datei lesen:**
```hemlock
let f = open("config.json", "r");
// oder einfach:
let f = open("config.json");  // "r" ist Standard
```

**Neue Datei zum Schreiben erstellen:**
```hemlock
let f = open("output.txt", "w");  // Erstellt oder schneidet ab
```

**An Datei anhängen:**
```hemlock
let f = open("log.txt", "a");  // Erstellt wenn nicht existiert
```

**Lese- und Schreibmodus:**
```hemlock
let f = open("data.bin", "r+");  // Bestehende Datei, kann lesen/schreiben
```

## Dateimethoden

### Lesen

#### read(size?: i32): string

Text aus Datei lesen (optionaler size-Parameter).

**Ohne size (alles lesen):**
```hemlock
let f = open("data.txt", "r");
let all = f.read();  // Von aktueller Position bis EOF lesen
f.close();
```

**Mit size (bestimmte Bytes lesen):**
```hemlock
let f = open("data.txt", "r");
let chunk = f.read(1024);  // Bis zu 1024 Bytes lesen
let next = f.read(1024);   // Nächste 1024 Bytes lesen
f.close();
```

**Rückgabe:** String mit den gelesenen Daten, oder leerer String bei EOF

**Beispiel - Gesamte Datei lesen:**
```hemlock
let f = open("poem.txt", "r");
let content = f.read();
print(content);
f.close();
```

**Beispiel - In Chunks lesen:**
```hemlock
let f = open("large.txt", "r");
while (true) {
    let chunk = f.read(4096);  // 4KB Chunks
    if (chunk == "") { break; }  // EOF erreicht
    process(chunk);
}
f.close();
```

#### read_bytes(size: i32): buffer

Binärdaten lesen (gibt Buffer zurück).

**Parameter:**
- `size` (i32) - Anzahl der zu lesenden Bytes

**Rückgabe:** Buffer mit den gelesenen Bytes

```hemlock
let f = open("image.png", "r");
let binary = f.read_bytes(256);  // 256 Bytes lesen
print(binary.length);  // 256 (oder weniger bei EOF)

// Auf einzelne Bytes zugreifen
let first_byte = binary[0];
print(first_byte);

f.close();
```

**Beispiel - Gesamte Binärdatei lesen:**
```hemlock
let f = open("data.bin", "r");
let size = 10240;  // Erwartete Größe
let data = f.read_bytes(size);
f.close();

// Binärdaten verarbeiten
let i = 0;
while (i < data.length) {
    let byte = data[i];
    // ... Byte verarbeiten
    i = i + 1;
}
```

### Schreiben

#### write(data: string): i32

Text in Datei schreiben (gibt geschriebene Bytes zurück).

**Parameter:**
- `data` (string) - Zu schreibender Text

**Rückgabe:** Anzahl der geschriebenen Bytes (i32)

```hemlock
let f = open("output.txt", "w");
let written = f.write("Hallo, Welt!\n");
print("Schrieb " + typeof(written) + " Bytes");  // "Schrieb 13 Bytes"
f.close();
```

**Beispiel - Mehrere Zeilen schreiben:**
```hemlock
let f = open("output.txt", "w");
f.write("Zeile 1\n");
f.write("Zeile 2\n");
f.write("Zeile 3\n");
f.close();
```

**Beispiel - An Log-Datei anhängen:**
```hemlock
let f = open("app.log", "a");
f.write("[INFO] Anwendung gestartet\n");
f.write("[INFO] Benutzer angemeldet\n");
f.close();
```

#### write_bytes(data: buffer): i32

Binärdaten schreiben (gibt geschriebene Bytes zurück).

**Parameter:**
- `data` (buffer) - Zu schreibende Binärdaten

**Rückgabe:** Anzahl der geschriebenen Bytes (i32)

```hemlock
let f = open("output.bin", "w");

// Binärdaten erstellen
let buf = buffer(10);
buf[0] = 65;  // 'A'
buf[1] = 66;  // 'B'
buf[2] = 67;  // 'C'

let bytes = f.write_bytes(buf);
print("Schrieb " + typeof(bytes) + " Bytes");

f.close();
```

**Beispiel - Binärdatei kopieren:**
```hemlock
let src = open("input.bin", "r");
let dst = open("output.bin", "w");

let data = src.read_bytes(1024);
while (data.length > 0) {
    dst.write_bytes(data);
    data = src.read_bytes(1024);
}

src.close();
dst.close();
```

### Positionierung

#### seek(position: i32): i32

Zu bestimmter Position bewegen (gibt neue Position zurück).

**Parameter:**
- `position` (i32) - Byte-Offset vom Dateianfang

**Rückgabe:** Neue Position (i32)

```hemlock
let f = open("data.txt", "r");

// Zu Byte 100 bewegen
f.seek(100);

// Ab Position 100 lesen
let data = f.read(50);

// Zum Anfang zurücksetzen
f.seek(0);

f.close();
```

**Beispiel - Wahlfreier Zugriff:**
```hemlock
let f = open("records.dat", "r");

// Datensatz an Offset 1000 lesen
f.seek(1000);
let record1 = f.read_bytes(100);

// Datensatz an Offset 2000 lesen
f.seek(2000);
let record2 = f.read_bytes(100);

f.close();
```

#### tell(): i32

Aktuelle Position in Datei erhalten.

**Rückgabe:** Aktueller Byte-Offset (i32)

```hemlock
let f = open("data.txt", "r");

let pos1 = f.tell();  // 0 (am Anfang)

f.read(100);
let pos2 = f.tell();  // 100 (nach Lesen von 100 Bytes)

f.seek(500);
let pos3 = f.tell();  // 500 (nach Seek)

f.close();
```

**Beispiel - Gelesene Menge messen:**
```hemlock
let f = open("data.txt", "r");

let start = f.tell();
let content = f.read();
let end = f.tell();

let bytes_read = end - start;
print("Las " + typeof(bytes_read) + " Bytes");

f.close();
```

### Schließen

#### close()

Datei schließen (idempotent, kann mehrfach aufgerufen werden).

```hemlock
let f = open("data.txt", "r");
// ... Datei verwenden
f.close();
f.close();  // Sicher - kein Fehler beim zweiten Schließen
```

**Wichtige Hinweise:**
- Dateien immer schließen wenn fertig, um Dateideskriptor-Lecks zu vermeiden
- Schließen ist idempotent - kann mehrfach sicher aufgerufen werden
- Nach dem Schließen werden alle anderen Operationen einen Fehler verursachen
- `finally`-Blöcke verwenden, um sicherzustellen, dass Dateien auch bei Fehlern geschlossen werden

## Dateieigenschaften

Dateiobjekte haben drei schreibgeschützte Eigenschaften:

### path: string

Der zum Öffnen der Datei verwendete Dateipfad.

```hemlock
let f = open("/path/to/file.txt", "r");
print(f.path);  // "/path/to/file.txt"
f.close();
```

### mode: string

Der Modus, mit dem die Datei geöffnet wurde.

```hemlock
let f = open("data.txt", "r");
print(f.mode);  // "r"
f.close();

let f2 = open("output.txt", "w");
print(f2.mode);  // "w"
f2.close();
```

### closed: bool

Ob die Datei geschlossen ist.

```hemlock
let f = open("data.txt", "r");
print(f.closed);  // false

f.close();
print(f.closed);  // true
```

**Beispiel - Prüfen ob Datei geöffnet ist:**
```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... Inhalt verarbeiten
}

f.close();

if (f.closed) {
    print("Datei ist jetzt geschlossen");
}
```

## Fehlerbehandlung

Alle Dateioperationen enthalten ordnungsgemäße Fehlermeldungen mit Kontext.

### Häufige Fehler

**Datei nicht gefunden:**
```hemlock
let f = open("missing.txt", "r");
// Fehler: Konnte 'missing.txt' nicht öffnen: Keine solche Datei oder Verzeichnis
```

**Von geschlossener Datei lesen:**
```hemlock
let f = open("data.txt", "r");
f.close();
f.read();
// Fehler: Kann nicht von geschlossener Datei 'data.txt' lesen
```

**In schreibgeschützte Datei schreiben:**
```hemlock
let f = open("readonly.txt", "r");
f.write("data");
// Fehler: Kann nicht in Datei 'readonly.txt' schreiben, die im Nur-Lese-Modus geöffnet wurde
```

**Von schreibgeschützter Datei lesen:**
```hemlock
let f = open("output.txt", "w");
f.read();
// Fehler: Kann nicht von Datei 'output.txt' lesen, die im Nur-Schreib-Modus geöffnet wurde
```

### try/catch verwenden

```hemlock
try {
    let f = open("data.txt", "r");
    let content = f.read();
    f.close();
    process(content);
} catch (e) {
    print("Fehler beim Lesen der Datei: " + e);
}
```

## Ressourcenverwaltung

### Grundmuster

Dateien immer explizit schließen:

```hemlock
let f = open("data.txt", "r");
let content = f.read();
f.close();
```

### Mit Fehlerbehandlung (empfohlen)

`finally` verwenden, um sicherzustellen, dass Dateien auch bei Fehlern geschlossen werden:

```hemlock
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();  // Immer schließen, auch bei Fehler
}
```

### Mehrere Dateien

```hemlock
let src = null;
let dst = null;

try {
    src = open("input.txt", "r");
    dst = open("output.txt", "w");

    let content = src.read();
    dst.write(content);
} finally {
    if (src != null) { src.close(); }
    if (dst != null) { dst.close(); }
}
```

### Hilfsfunktions-Muster

```hemlock
fn with_file(path: string, mode: string, callback) {
    let f = open(path, mode);
    try {
        return callback(f);
    } finally {
        f.close();
    }
}

// Verwendung:
with_file("data.txt", "r", fn(f) {
    return f.read();
});
```

## Vollständige API-Referenz

### Funktionen

| Funktion | Parameter | Rückgabe | Beschreibung |
|----------|-----------|----------|--------------|
| `open(path, mode?)` | path: string, mode?: string | File | Datei öffnen (mode Standard ist "r") |

### Methoden

| Methode | Parameter | Rückgabe | Beschreibung |
|---------|-----------|----------|--------------|
| `read(size?)` | size?: i32 | string | Text lesen (alles oder bestimmte Bytes) |
| `read_bytes(size)` | size: i32 | buffer | Binärdaten lesen |
| `write(data)` | data: string | i32 | Text schreiben, gibt geschriebene Bytes zurück |
| `write_bytes(data)` | data: buffer | i32 | Binärdaten schreiben, gibt geschriebene Bytes zurück |
| `seek(position)` | position: i32 | i32 | Zu Position springen, gibt neue Position zurück |
| `tell()` | - | i32 | Aktuelle Position erhalten |
| `close()` | - | null | Datei schließen (idempotent) |

### Eigenschaften (schreibgeschützt)

| Eigenschaft | Typ | Beschreibung |
|-------------|-----|--------------|
| `path` | string | Dateipfad |
| `mode` | string | Öffnungsmodus |
| `closed` | bool | Ob Datei geschlossen ist |

## Häufige Muster

### Gesamte Datei lesen

```hemlock
fn read_file(path: string): string {
    let f = open(path, "r");
    try {
        return f.read();
    } finally {
        f.close();
    }
}

let content = read_file("config.json");
```

### Gesamte Datei schreiben

```hemlock
fn write_file(path: string, content: string) {
    let f = open(path, "w");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

write_file("output.txt", "Hallo, Welt!");
```

### An Datei anhängen

```hemlock
fn append_file(path: string, content: string) {
    let f = open(path, "a");
    try {
        f.write(content);
    } finally {
        f.close();
    }
}

append_file("log.txt", "[INFO] Ereignis aufgetreten\n");
```

### Zeilen lesen

```hemlock
fn read_lines(path: string) {
    let f = open(path, "r");
    try {
        let content = f.read();
        return content.split("\n");
    } finally {
        f.close();
    }
}

let lines = read_lines("data.txt");
let i = 0;
while (i < lines.length) {
    print("Zeile " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Große Dateien in Chunks verarbeiten

```hemlock
fn process_large_file(path: string) {
    let f = open(path, "r");
    try {
        while (true) {
            let chunk = f.read(4096);  // 4KB Chunks
            if (chunk == "") { break; }

            // Chunk verarbeiten
            process_chunk(chunk);
        }
    } finally {
        f.close();
    }
}
```

### Binärdatei kopieren

```hemlock
fn copy_file(src_path: string, dst_path: string) {
    let src = null;
    let dst = null;

    try {
        src = open(src_path, "r");
        dst = open(dst_path, "w");

        while (true) {
            let chunk = src.read_bytes(4096);
            if (chunk.length == 0) { break; }

            dst.write_bytes(chunk);
        }
    } finally {
        if (src != null) { src.close(); }
        if (dst != null) { dst.close(); }
    }
}

copy_file("input.dat", "output.dat");
```

### Datei abschneiden

```hemlock
fn truncate_file(path: string) {
    let f = open(path, "w");  // "w"-Modus schneidet ab
    f.close();
}

truncate_file("empty_me.txt");
```

### Wahlfreies Lesen

```hemlock
fn read_at_offset(path: string, offset: i32, size: i32): string {
    let f = open(path, "r");
    try {
        f.seek(offset);
        return f.read(size);
    } finally {
        f.close();
    }
}

let data = read_at_offset("records.dat", 1000, 100);
```

### Dateigröße

```hemlock
fn file_size(path: string): i32 {
    let f = open(path, "r");
    try {
        // Zum Ende springen
        let end = f.seek(999999999);  // Große Zahl
        f.seek(0);  // Zurücksetzen
        return end;
    } finally {
        f.close();
    }
}

let size = file_size("data.txt");
print("Dateigröße: " + typeof(size) + " Bytes");
```

### Bedingtes Lesen/Schreiben

```hemlock
fn update_file(path: string, condition, new_content: string) {
    let f = open(path, "r+");
    try {
        let content = f.read();

        if (condition(content)) {
            f.seek(0);  // Zum Anfang zurücksetzen
            f.write(new_content);
        }
    } finally {
        f.close();
    }
}
```

## Best Practices

### 1. Immer try/finally verwenden

```hemlock
// Gut
let f = open("data.txt", "r");
try {
    let content = f.read();
    process(content);
} finally {
    f.close();
}

// Schlecht - Datei wird bei Fehler möglicherweise nicht geschlossen
let f = open("data.txt", "r");
let content = f.read();
process(content);  // Wenn das wirft, Datei-Leck
f.close();
```

### 2. Dateizustand vor Operationen prüfen

```hemlock
let f = open("data.txt", "r");

if (!f.closed) {
    let content = f.read();
    // ... Inhalt verwenden
}

f.close();
```

### 3. Geeignete Modi verwenden

```hemlock
// Nur Lesen? "r" verwenden
let f = open("config.json", "r");

// Komplett ersetzen? "w" verwenden
let f = open("output.txt", "w");

// Am Ende hinzufügen? "a" verwenden
let f = open("log.txt", "a");
```

### 4. Fehler elegant behandeln

```hemlock
fn safe_read_file(path: string): string {
    try {
        let f = open(path, "r");
        try {
            return f.read();
        } finally {
            f.close();
        }
    } catch (e) {
        print("Warnung: Konnte " + path + " nicht lesen: " + e);
        return "";
    }
}
```

### 5. Dateien in umgekehrter Reihenfolge des Öffnens schließen

```hemlock
let f1 = null;
let f2 = null;
let f3 = null;

try {
    f1 = open("file1.txt", "r");
    f2 = open("file2.txt", "r");
    f3 = open("file3.txt", "r");

    // ... Dateien verwenden
} finally {
    // In umgekehrter Reihenfolge schließen
    if (f3 != null) { f3.close(); }
    if (f2 != null) { f2.close(); }
    if (f1 != null) { f1.close(); }
}
```

### 6. Große Dateien nicht vollständig lesen

```hemlock
// Schlecht für große Dateien
let f = open("huge.log", "r");
let content = f.read();  // Lädt gesamte Datei in Speicher
f.close();

// Gut - in Chunks verarbeiten
let f = open("huge.log", "r");
try {
    while (true) {
        let chunk = f.read(4096);
        if (chunk == "") { break; }
        process_chunk(chunk);
    }
} finally {
    f.close();
}
```

## Zusammenfassung

Hemlocks Datei-I/O-API bietet:

- ✅ Einfache, explizite Dateioperationen
- ✅ Text- und Binärunterstützung
- ✅ Wahlfreier Zugriff mit seek/tell
- ✅ Klare Fehlermeldungen mit Kontext
- ✅ Idempotente close-Operation

Denken Sie daran:
- Dateien immer manuell schließen
- try/finally für Ressourcensicherheit verwenden
- Geeignete Öffnungsmodi wählen
- Fehler elegant behandeln
- Große Dateien in Chunks verarbeiten
