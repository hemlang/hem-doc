# Profiling

Hemlock enthält einen integrierten Profiler für **CPU-Zeit-Analyse**, **Speicherverfolgung** und **Leak-Erkennung**. Der Profiler hilft dabei, Leistungsengpässe und Speicherprobleme in Ihren Programmen zu identifizieren.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Schnellstart](#schnellstart)
- [Profiling-Modi](#profiling-modi)
- [Ausgabeformate](#ausgabeformate)
- [Leak-Erkennung](#leak-erkennung)
- [Berichte verstehen](#berichte-verstehen)
- [Flamegraph-Generierung](#flamegraph-generierung)
- [Best Practices](#best-practices)

---

## Überblick

Der Profiler wird über den `profile`-Unterbefehl aufgerufen:

```bash
hemlock profile [OPTIONEN] <DATEI>
```

**Hauptfunktionen:**
- **CPU-Profiling** - Zeit messen, die in jeder Funktion verbracht wird (Self-Time und Total-Time)
- **Speicher-Profiling** - Alle Allokationen mit Quellcode-Positionen verfolgen
- **Leak-Erkennung** - Speicher identifizieren, der nie freigegeben wurde
- **Mehrere Ausgabeformate** - Text, JSON und Flamegraph-kompatible Ausgabe
- **Pro-Funktion-Speicherstatistiken** - Sehen, welche Funktionen am meisten Speicher allozieren

---

## Schnellstart

### CPU-Zeit profilen (Standard)

```bash
hemlock profile script.hml
```

### Speicherallokationen profilen

```bash
hemlock profile --memory script.hml
```

### Speicherlecks erkennen

```bash
hemlock profile --leaks script.hml
```

### Flamegraph-Daten generieren

```bash
hemlock profile --flamegraph script.hml > profile.folded
flamegraph.pl profile.folded > profile.svg
```

---

## Profiling-Modi

### CPU-Profiling (Standard)

Misst Zeit, die in jeder Funktion verbracht wird, unterscheidend zwischen:
- **Self-Time** - Zeit, die mit der Ausführung des eigenen Codes der Funktion verbracht wird
- **Total-Time** - Self-Time plus Zeit in aufgerufenen Funktionen

```bash
hemlock profile script.hml
hemlock profile --cpu script.hml  # Explizit
```

**Beispielausgabe:**
```
=== Hemlock Profiler-Bericht ===

Gesamtzeit: 1.234ms
Aufgerufene Funktionen: 5 eindeutige

--- Top 5 nach Self-Time ---

Funktion                        Self      Total   Aufrufe
--------                        ----      -----   -------
expensive_calc              0.892ms    0.892ms     100  (72.3%)
process_data                0.234ms    1.126ms      10  (19.0%)
helper                      0.067ms    0.067ms     500  (5.4%)
main                        0.041ms    1.234ms       1  (3.3%)
```

---

### Speicher-Profiling

Verfolgt alle Speicherallokationen (`alloc`, `buffer`, `talloc`, `realloc`) mit Quellcode-Positionen.

```bash
hemlock profile --memory script.hml
```

**Beispielausgabe:**
```
=== Hemlock Profiler-Bericht ===

Gesamtzeit: 0.543ms
Aufgerufene Funktionen: 3 eindeutige
Gesamte Allokationen: 15 (4.2KB)

--- Top 3 nach Self-Time ---

Funktion                        Self      Total   Aufrufe      Allok      Anzahl
--------                        ----      -----   -------      -----      ------
allocator                   0.312ms    0.312ms      10      3.2KB         10  (57.5%)
buffer_ops                  0.156ms    0.156ms       5       1KB          5  (28.7%)
main                        0.075ms    0.543ms       1        0B          0  (13.8%)

--- Top 10 Allokationsstellen ---

Position                                      Gesamt   Anzahl
--------                                      ------   ------
src/data.hml:42                               1.5KB        5
src/data.hml:67                               1.0KB       10
src/main.hml:15                               512B         1
```

---

### Aufrufzähler-Modus

Minimaler Overhead-Modus, der nur Funktionsaufrufe zählt (keine Zeitmessung).

```bash
hemlock profile --calls script.hml
```

---

## Ausgabeformate

### Text (Standard)

Menschenlesbare Zusammenfassung mit Tabellen.

```bash
hemlock profile script.hml
```

---

### JSON

Maschinenlesbares Format für Integration mit anderen Werkzeugen.

```bash
hemlock profile --json script.hml
```

**Beispielausgabe:**
```json
{
  "total_time_ns": 1234567,
  "function_count": 5,
  "total_alloc_bytes": 4096,
  "total_alloc_count": 15,
  "functions": [
    {
      "name": "expensive_calc",
      "source_file": "script.hml",
      "line": 10,
      "self_time_ns": 892000,
      "total_time_ns": 892000,
      "call_count": 100,
      "alloc_bytes": 0,
      "alloc_count": 0
    }
  ],
  "alloc_sites": [
    {
      "source_file": "script.hml",
      "line": 42,
      "total_bytes": 1536,
      "alloc_count": 5,
      "current_bytes": 0
    }
  ]
}
```

---

### Flamegraph

Generiert zusammengeklapptes Stack-Format, kompatibel mit [flamegraph.pl](https://github.com/brendangregg/FlameGraph).

```bash
hemlock profile --flamegraph script.hml > profile.folded

# SVG mit flamegraph.pl generieren
flamegraph.pl profile.folded > profile.svg
```

**Beispiel zusammengeklappte Ausgabe:**
```
main;process_data;expensive_calc 892
main;process_data;helper 67
main;process_data 234
main 41
```

---

## Leak-Erkennung

Das `--leaks`-Flag zeigt nur Allokationen, die nie freigegeben wurden, was das Identifizieren von Speicherlecks erleichtert.

```bash
hemlock profile --leaks script.hml
```

**Beispielprogramm mit Lecks:**
```hemlock
fn leaky() {
    let p1 = alloc(100);    // Leck - nie freigegeben
    let p2 = alloc(200);    // OK - unten freigegeben
    free(p2);
}

fn clean() {
    let b = buffer(64);
    free(b);                // Ordnungsgemäß freigegeben
}

leaky();
clean();
```

**Ausgabe mit --leaks:**
```
=== Hemlock Profiler-Bericht ===

Gesamtzeit: 0.034ms
Aufgerufene Funktionen: 2 eindeutige
Gesamte Allokationen: 3 (388B)

--- Top 2 nach Self-Time ---

Funktion                        Self      Total   Aufrufe      Allok      Anzahl
--------                        ----      -----   -------      -----      ------
leaky                       0.021ms    0.021ms       1       300B          2  (61.8%)
clean                       0.013ms    0.013ms       1        88B          1  (38.2%)

--- Speicherlecks (1 Stelle) ---

Position                                     Leck        Gesamt    Anzahl
--------                                     ----        ------    ------
script.hml:2                                 100B        100B         1
```

Der Leak-Bericht zeigt:
- **Leck** - Bytes, die bei Programmende noch nicht freigegeben sind
- **Gesamt** - Gesamte jemals an dieser Stelle allozierte Bytes
- **Anzahl** - Anzahl der Allokationen an dieser Stelle

---

## Berichte verstehen

### Funktionsstatistiken

| Spalte | Beschreibung |
|--------|--------------|
| Funktion | Funktionsname |
| Self | Zeit in Funktion ohne aufgerufene Funktionen |
| Total | Zeit einschließlich aller aufgerufenen Funktionen |
| Aufrufe | Anzahl der Funktionsaufrufe |
| Allok | Gesamte von dieser Funktion allozierte Bytes |
| Anzahl | Anzahl der Allokationen durch diese Funktion |
| (%) | Prozentsatz der gesamten Programmzeit |

### Allokationsstellen

| Spalte | Beschreibung |
|--------|--------------|
| Position | Quelldatei und Zeilennummer |
| Gesamt | Gesamte an dieser Position allozierte Bytes |
| Anzahl | Anzahl der Allokationen |
| Leck | Bytes, die bei Programmende noch alloziert sind (nur --leaks) |

### Zeiteinheiten

Der Profiler wählt automatisch geeignete Einheiten:
- `ns` - Nanosekunden (< 1us)
- `us` - Mikrosekunden (< 1ms)
- `ms` - Millisekunden (< 1s)
- `s` - Sekunden

---

## Befehlsreferenz

```
hemlock profile [OPTIONEN] <DATEI>

OPTIONEN:
    --cpu           CPU/Zeit-Profiling (Standard)
    --memory        Speicherallokations-Profiling
    --calls         Nur Aufrufzählung (minimaler Overhead)
    --leaks         Nur nicht freigegebene Allokationen zeigen (impliziert --memory)
    --json          Ausgabe im JSON-Format
    --flamegraph    Ausgabe im Flamegraph-kompatiblen Format
    --top N         Top N Einträge zeigen (Standard: 20)
```

---

## Flamegraph-Generierung

Flamegraphs visualisieren, wo Ihr Programm Zeit verbringt, wobei breitere Balken mehr verbrachte Zeit anzeigen.

### Flamegraph generieren

1. flamegraph.pl installieren:
   ```bash
   git clone https://github.com/brendangregg/FlameGraph
   ```

2. Ihr Programm profilen:
   ```bash
   hemlock profile --flamegraph script.hml > profile.folded
   ```

3. SVG generieren:
   ```bash
   ./FlameGraph/flamegraph.pl profile.folded > profile.svg
   ```

4. `profile.svg` im Browser öffnen für eine interaktive Visualisierung.

### Flamegraphs lesen

- **X-Achse**: Prozentsatz der Gesamtzeit (Breite = Zeitanteil)
- **Y-Achse**: Call-Stack-Tiefe (unten = Einstiegspunkt, oben = Blattfunktionen)
- **Farbe**: Zufällig, nur zur visuellen Unterscheidung
- **Klick**: In eine Funktion hineinzoomen, um ihre aufgerufenen Funktionen zu sehen

---

## Best Practices

### 1. Repräsentative Workloads profilen

Mit realistischen Daten und Nutzungsmustern profilen. Kleine Testfälle enthüllen möglicherweise nicht die echten Engpässe.

```bash
# Gut: Mit produktionsähnlichen Daten profilen
hemlock profile --memory process_large_file.hml large_input.txt

# Weniger nützlich: Kleiner Testfall
hemlock profile quick_test.hml
```

### 2. --leaks während der Entwicklung verwenden

Leak-Erkennung regelmäßig ausführen, um Speicherlecks früh zu finden:

```bash
hemlock profile --leaks my_program.hml
```

### 3. Vorher und Nachher vergleichen

Vor und nach Optimierungen profilen, um die Auswirkung zu messen:

```bash
# Vor Optimierung
hemlock profile --json script.hml > before.json

# Nach Optimierung
hemlock profile --json script.hml > after.json

# Ergebnisse vergleichen
```

### 4. --top für große Programme verwenden

Ausgabe begrenzen, um sich auf die wichtigsten Funktionen zu konzentrieren:

```bash
hemlock profile --top 10 large_program.hml
```

### 5. Mit Flamegraphs kombinieren

Für komplexe Aufrufmuster bieten Flamegraphs eine bessere Visualisierung als Textausgabe:

```bash
hemlock profile --flamegraph complex_app.hml > app.folded
flamegraph.pl app.folded > app.svg
```

---

## Profiler-Overhead

Der Profiler fügt etwas Overhead zur Programmausführung hinzu:

| Modus | Overhead | Anwendungsfall |
|-------|----------|----------------|
| `--calls` | Minimal | Nur Funktionsaufrufe zählen |
| `--cpu` | Niedrig | Allgemeines Leistungs-Profiling |
| `--memory` | Moderat | Speicheranalyse und Leak-Erkennung |

Für die genauesten Ergebnisse mehrfach profilen und nach konsistenten Mustern suchen.

---

## Siehe auch

- [Speicherverwaltung](../language-guide/memory.md) - Pointer und Buffer
- [Speicher-API](../reference/memory-api.md) - alloc, free, buffer-Funktionen
- [Async/Nebenläufigkeit](async-concurrency.md) - Async-Code profilen
