# Befehlsausführung in Hemlock

Hemlock bietet die **eingebaute Funktion `exec()`**, um Shell-Befehle auszuführen und ihre Ausgabe zu erfassen.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Die exec()-Funktion](#die-exec-funktion)
- [Ergebnisobjekt](#ergebnisobjekt)
- [Grundlegende Verwendung](#grundlegende-verwendung)
- [Fortgeschrittene Beispiele](#fortgeschrittene-beispiele)
- [Fehlerbehandlung](#fehlerbehandlung)
- [Implementierungsdetails](#implementierungsdetails)
- [Sicherheitsüberlegungen](#sicherheitsüberlegungen)
- [Einschränkungen](#einschränkungen)
- [Anwendungsfälle](#anwendungsfälle)
- [Best Practices](#best-practices)
- [Vollständige Beispiele](#vollständige-beispiele)

## Überblick

Die `exec()`-Funktion ermöglicht Hemlock-Programmen:
- Shell-Befehle auszuführen
- Standardausgabe (stdout) zu erfassen
- Exit-Statuscodes zu prüfen
- Shell-Funktionen zu nutzen (Pipes, Umleitungen, etc.)
- Mit System-Dienstprogrammen zu integrieren

**Wichtig:** Befehle werden über `/bin/sh` ausgeführt, was volle Shell-Funktionalität bietet, aber auch Sicherheitsüberlegungen mit sich bringt.

## Die exec()-Funktion

### Signatur

```hemlock
exec(command: string): object
```

**Parameter:**
- `command` (string) - Auszuführender Shell-Befehl

**Rückgabe:** Ein Objekt mit zwei Feldern:
- `output` (string) - Die stdout-Ausgabe des Befehls
- `exit_code` (i32) - Der Exit-Statuscode des Befehls

### Einfaches Beispiel

```hemlock
let result = exec("echo hello");
print(result.output);      // "hello\n"
print(result.exit_code);   // 0
```

## Ergebnisobjekt

Das von `exec()` zurückgegebene Objekt hat folgende Struktur:

```hemlock
{
    output: string,      // Befehl stdout (erfasste Ausgabe)
    exit_code: i32       // Prozess-Exit-Status (0 = Erfolg)
}
```

### output-Feld

Enthält den gesamten Text, der vom Befehl auf stdout geschrieben wurde.

**Eigenschaften:**
- Leerer String, wenn Befehl keine Ausgabe erzeugt
- Enthält Zeilenumbrüche und Leerzeichen wie vorhanden
- Mehrzeilige Ausgabe bleibt erhalten
- Nicht größenbeschränkt (dynamisch alloziert)

**Beispiele:**
```hemlock
let r1 = exec("echo test");
print(r1.output);  // "test\n"

let r2 = exec("ls");
print(r2.output);  // Verzeichnisliste mit Zeilenumbrüchen

let r3 = exec("true");
print(r3.output);  // "" (leerer String)
```

### exit_code-Feld

Der Exit-Statuscode des Befehls.

**Werte:**
- `0` zeigt typischerweise Erfolg an
- `1-255` zeigen Fehler an (Konvention variiert nach Befehl)
- `-1` wenn Befehl nicht ausgeführt werden konnte oder abnormal beendet wurde

**Beispiele:**
```hemlock
let r1 = exec("true");
print(r1.exit_code);  // 0 (Erfolg)

let r2 = exec("false");
print(r2.exit_code);  // 1 (Fehler)

let r3 = exec("ls /nonexistent");
print(r3.exit_code);  // 2 (Datei nicht gefunden, variiert nach Befehl)
```

## Grundlegende Verwendung

### Einfacher Befehl

```hemlock
let r = exec("ls -la");
print(r.output);
print("Exit-Code: " + typeof(r.exit_code));
```

### Exit-Status prüfen

```hemlock
let r = exec("grep pattern file.txt");
if (r.exit_code == 0) {
    print("Gefunden: " + r.output);
} else {
    print("Muster nicht gefunden");
}
```

### Befehle mit Pipes

```hemlock
let r = exec("ps aux | grep hemlock");
print(r.output);
```

### Mehrere Befehle

```hemlock
let r = exec("cd /tmp && ls -la");
print(r.output);
```

### Befehlsersetzung

```hemlock
let r = exec("echo $(date)");
print(r.output);  // Aktuelles Datum
```

## Fortgeschrittene Beispiele

### Fehler behandeln

```hemlock
let r = exec("ls /nonexistent");
if (r.exit_code != 0) {
    print("Befehl fehlgeschlagen mit Code: " + typeof(r.exit_code));
    print("Fehlerausgabe: " + r.output);  // Hinweis: stderr wird nicht erfasst
}
```

### Mehrzeilige Ausgabe verarbeiten

```hemlock
let r = exec("cat file.txt");
let lines = r.output.split("\n");
let i = 0;
while (i < lines.length) {
    print("Zeile " + typeof(i) + ": " + lines[i]);
    i = i + 1;
}
```

### Befehlsverkettung

**Mit && (UND):**
```hemlock
let r1 = exec("mkdir -p /tmp/test && touch /tmp/test/file.txt");
if (r1.exit_code == 0) {
    print("Setup abgeschlossen");
}
```

**Mit || (ODER):**
```hemlock
let r = exec("command1 || command2");
// Führt command2 nur aus, wenn command1 fehlschlägt
```

**Mit ; (Sequenz):**
```hemlock
let r = exec("command1; command2");
// Führt beide aus, unabhängig von Erfolg/Fehler
```

### Pipes verwenden

```hemlock
let r = exec("echo 'data' | base64");
print("Base64: " + r.output);
```

**Komplexe Pipelines:**
```hemlock
let r = exec("cat /etc/passwd | grep root | cut -d: -f1");
print(r.output);
```

### Exit-Code-Muster

Verschiedene Exit-Codes zeigen verschiedene Bedingungen an:

```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Datei existiert");
} else if (r.exit_code == 1) {
    print("Datei existiert nicht");
} else {
    print("Test-Befehl fehlgeschlagen: " + typeof(r.exit_code));
}
```

### Ausgabe-Umleitungen

```hemlock
// stdout in Datei umleiten (innerhalb der Shell)
let r1 = exec("echo 'test' > /tmp/output.txt");

// stderr zu stdout umleiten (Hinweis: stderr wird von Hemlock immer noch nicht erfasst)
let r2 = exec("command 2>&1");
```

### Umgebungsvariablen

```hemlock
let r = exec("export VAR=value && echo $VAR");
print(r.output);  // "value\n"
```

### Arbeitsverzeichnis-Änderungen

```hemlock
let r = exec("cd /tmp && pwd");
print(r.output);  // "/tmp\n"
```

## Fehlerbehandlung

### Wann exec() Ausnahmen wirft

Die `exec()`-Funktion wirft eine Ausnahme, wenn der Befehl nicht ausgeführt werden kann:

```hemlock
try {
    let r = exec("nonexistent_command_xyz");
} catch (e) {
    print("Ausführung fehlgeschlagen: " + e);
}
```

**Ausnahmen werden geworfen wenn:**
- `popen()` fehlschlägt (z.B. Pipe kann nicht erstellt werden)
- Systemressourcengrenzen überschritten werden
- Speicherallokationsfehler auftreten

### Wann exec() NICHT wirft

```hemlock
// Befehl läuft, gibt aber Nicht-Null-Exit-Code zurück
let r1 = exec("false");
print(r1.exit_code);  // 1 (keine Ausnahme)

// Befehl erzeugt keine Ausgabe
let r2 = exec("true");
print(r2.output);  // "" (keine Ausnahme)

// Befehl von Shell nicht gefunden
let r3 = exec("nonexistent_cmd");
print(r3.exit_code);  // 127 (keine Ausnahme)
```

### Sicheres Ausführungsmuster

```hemlock
fn safe_exec(command: string) {
    try {
        let r = exec(command);
        if (r.exit_code != 0) {
            print("Warnung: Befehl fehlgeschlagen mit Code " + typeof(r.exit_code));
            return "";
        }
        return r.output;
    } catch (e) {
        print("Fehler beim Ausführen des Befehls: " + e);
        return "";
    }
}

let output = safe_exec("ls -la");
```

## Implementierungsdetails

### Wie es funktioniert

**Unter der Haube:**
- Verwendet `popen()`, um Befehle über `/bin/sh` auszuführen
- Erfasst nur stdout (stderr wird nicht erfasst)
- Ausgabe wird dynamisch gepuffert (beginnt bei 4KB, wächst bei Bedarf)
- Exit-Status wird mit `WIFEXITED()` und `WEXITSTATUS()` Makros extrahiert
- Ausgabe-String wird korrekt null-terminiert

**Prozessablauf:**
1. `popen(command, "r")` erstellt Pipe und forkt Prozess
2. Kindprozess führt `/bin/sh -c "command"` aus
3. Elternprozess liest stdout über Pipe in wachsenden Puffer
4. `pclose()` wartet auf Kind und gibt Exit-Status zurück
5. Exit-Status wird extrahiert und im Ergebnisobjekt gespeichert

### Leistungsüberlegungen

**Kosten:**
- Erstellt einen neuen Shell-Prozess für jeden Aufruf (~1-5ms Overhead)
- Ausgabe wird vollständig im Speicher gehalten (nicht gestreamt)
- Keine Streaming-Unterstützung (wartet auf Befehlsabschluss)
- Geeignet für Befehle mit vernünftigen Ausgabegrößen

**Optimierungen:**
- Puffer beginnt bei 4KB und verdoppelt sich bei Füllung (effiziente Speichernutzung)
- Einzelne Leseschleife minimiert Systemaufrufe
- Kein zusätzliches String-Kopieren

**Wann zu verwenden:**
- Kurz laufende Befehle (< 1 Sekunde)
- Moderate Ausgabegröße (< 10MB)
- Batch-Operationen mit vernünftigen Intervallen

**Wann NICHT zu verwenden:**
- Lang laufende Daemons oder Dienste
- Befehle, die Gigabytes an Ausgabe erzeugen
- Echtzeit-Streaming-Datenverarbeitung
- Hochfrequente Ausführung (> 100 Aufrufe/Sekunde)

## Sicherheitsüberlegungen

### Shell-Injection-Risiko

⚠️ **KRITISCH:** Befehle werden von der Shell (`/bin/sh`) ausgeführt, was bedeutet, dass **Shell-Injection möglich** ist.

**Verwundbarer Code:**
```hemlock
// GEFÄHRLICH - TUN SIE DAS NICHT
let filename = args[1];  // Benutzereingabe
let r = exec("cat " + filename);  // Shell-Injection!
```

**Angriff:**
```bash
./hemlock script.hml "; rm -rf /; echo pwned"
# Führt aus: cat ; rm -rf /; echo pwned
```

### Sichere Praktiken

**1. Niemals unsanitisierte Benutzereingaben verwenden:**
```hemlock
// Schlecht
let user_input = args[1];
let r = exec("process " + user_input);  // GEFÄHRLICH

// Gut - zuerst validieren
fn is_safe_filename(name: string): bool {
    // Nur alphanumerische Zeichen, Bindestrich, Unterstrich, Punkt erlauben
    let i = 0;
    while (i < name.length) {
        let c = name[i];
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

let filename = args[1];
if (is_safe_filename(filename)) {
    let r = exec("cat " + filename);
} else {
    print("Ungültiger Dateiname");
}
```

**2. Allowlists verwenden, nicht Denylists:**
```hemlock
// Gut - strikte Allowlist
let allowed_commands = ["status", "start", "stop", "restart"];
let cmd = args[1];

let found = false;
for (let allowed in allowed_commands) {
    if (cmd == allowed) {
        found = true;
        break;
    }
}

if (found) {
    exec("service myapp " + cmd);
} else {
    print("Ungültiger Befehl");
}
```

**3. Sonderzeichen escapen:**
```hemlock
fn shell_escape(s: string): string {
    // Einfaches Escapen - in einfache Anführungszeichen setzen und einfache Anführungszeichen escapen
    let escaped = s.replace_all("'", "'\\''");
    return "'" + escaped + "'";
}

let user_file = args[1];
let safe = shell_escape(user_file);
let r = exec("cat " + safe);
```

**4. exec() für Dateioperationen vermeiden:**
```hemlock
// Schlecht - exec für Dateioperationen verwenden
let r = exec("cat file.txt");

// Gut - Hemlocks Datei-API verwenden
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### Berechtigungsüberlegungen

Befehle laufen mit den gleichen Berechtigungen wie der Hemlock-Prozess:

```hemlock
// Wenn Hemlock als root läuft, laufen exec()-Befehle auch als root!
let r = exec("rm -rf /important");  // GEFÄHRLICH wenn als root
```

**Best Practice:** Hemlock mit den geringstmöglichen Rechten ausführen.

## Einschränkungen

### 1. Keine stderr-Erfassung

Nur stdout wird erfasst, stderr geht zum Terminal:

```hemlock
let r = exec("ls /nonexistent");
// r.output ist leer
// Fehlermeldung erscheint im Terminal, wird nicht erfasst
```

**Workaround - stderr zu stdout umleiten:**
```hemlock
let r = exec("ls /nonexistent 2>&1");
// Jetzt sind Fehlermeldungen in r.output
```

### 2. Kein Streaming

Muss auf Befehlsabschluss warten:

```hemlock
let r = exec("long_running_command");
// Blockiert bis Befehl fertig
// Kann Ausgabe nicht inkrementell verarbeiten
```

### 3. Kein Timeout

Befehle können unbegrenzt laufen:

```hemlock
let r = exec("sleep 1000");
// Blockiert für 1000 Sekunden
// Keine Möglichkeit für Timeout oder Abbruch
```

**Workaround - timeout-Befehl verwenden:**
```hemlock
let r = exec("timeout 5 long_command");
// Timeout nach 5 Sekunden
```

### 4. Keine Signalbehandlung

Kann keine Signale an laufende Befehle senden:

```hemlock
let r = exec("long_command");
// Kann SIGINT, SIGTERM, etc. nicht an den Befehl senden
```

### 5. Keine Prozesssteuerung

Kann nicht mit Befehl nach dem Start interagieren:

```hemlock
let r = exec("interactive_program");
// Kann keine Eingabe an das Programm senden
// Kann Ausführung nicht steuern
```

## Anwendungsfälle

### Gute Anwendungsfälle

**1. System-Dienstprogramme ausführen:**
```hemlock
let r = exec("ls -la");
let r = exec("grep pattern file.txt");
let r = exec("find /path -name '*.txt'");
```

**2. Schnelle Datenverarbeitung mit Unix-Tools:**
```hemlock
let r = exec("cat data.txt | sort | uniq | wc -l");
print("Eindeutige Zeilen: " + r.output);
```

**3. Systemstatus prüfen:**
```hemlock
let r = exec("df -h");
print("Festplattennutzung:\n" + r.output);
```

**4. Dateiexistenz-Prüfungen:**
```hemlock
let r = exec("test -f myfile.txt");
if (r.exit_code == 0) {
    print("Datei existiert");
}
```

**5. Berichte generieren:**
```hemlock
let r = exec("ps aux | grep myapp | wc -l");
let count = r.output.trim();
print("Laufende Instanzen: " + count);
```

**6. Automatisierungsskripte:**
```hemlock
exec("git add .");
exec("git commit -m 'Auto commit'");
let r = exec("git push");
if (r.exit_code != 0) {
    print("Push fehlgeschlagen");
}
```

### Nicht empfohlen für

**1. Lang laufende Dienste:**
```hemlock
// Schlecht
let r = exec("nginx");  // Blockiert für immer
```

**2. Interaktive Befehle:**
```hemlock
// Schlecht - kann keine Eingabe bereitstellen
let r = exec("ssh user@host");
```

**3. Befehle mit riesiger Ausgabe:**
```hemlock
// Schlecht - lädt gesamte Ausgabe in Speicher
let r = exec("cat 10GB_file.log");
```

**4. Echtzeit-Streaming:**
```hemlock
// Schlecht - kann Ausgabe nicht inkrementell verarbeiten
let r = exec("tail -f /var/log/app.log");
```

**5. Missionskritische Fehlerbehandlung:**
```hemlock
// Schlecht - stderr wird nicht erfasst
let r = exec("critical_operation");
// Kann detaillierte Fehlermeldungen nicht sehen
```

## Best Practices

### 1. Immer Exit-Codes prüfen

```hemlock
let r = exec("important_command");
if (r.exit_code != 0) {
    print("Befehl fehlgeschlagen!");
    // Fehler behandeln
}
```

### 2. Ausgabe bei Bedarf trimmen

```hemlock
let r = exec("echo test");
let clean = r.output.trim();  // Abschließenden Zeilenumbruch entfernen
print(clean);  // "test" (kein Zeilenumbruch)
```

### 3. Vor dem Ausführen validieren

```hemlock
fn is_valid_command(cmd: string): bool {
    // Validieren, dass Befehl sicher ist
    return true;  // Ihre Validierungslogik
}

if (is_valid_command(user_cmd)) {
    exec(user_cmd);
}
```

### 4. try/catch für kritische Operationen verwenden

```hemlock
try {
    let r = exec("critical_command");
    if (r.exit_code != 0) {
        throw "Befehl fehlgeschlagen";
    }
} catch (e) {
    print("Fehler: " + e);
    // Bereinigung oder Wiederherstellung
}
```

### 5. Hemlock-APIs gegenüber exec() bevorzugen

```hemlock
// Schlecht - exec für Dateioperationen verwenden
let r = exec("cat file.txt");

// Gut - Hemlocks Datei-API verwenden
let f = open("file.txt", "r");
let content = f.read();
f.close();
```

### 6. stderr bei Bedarf erfassen

```hemlock
// stderr zu stdout umleiten
let r = exec("command 2>&1");
// Jetzt enthält r.output sowohl stdout als auch stderr
```

### 7. Shell-Funktionen weise nutzen

```hemlock
// Pipes für Effizienz verwenden
let r = exec("cat large.txt | grep pattern | head -n 10");

// Befehlsersetzung verwenden
let r = exec("echo Aktueller Benutzer: $(whoami)");

// Bedingte Ausführung verwenden
let r = exec("test -f file.txt && cat file.txt");
```

## Vollständige Beispiele

### Beispiel 1: Systeminformationen sammeln

```hemlock
fn get_system_info() {
    print("=== Systeminformationen ===");

    // Hostname
    let r1 = exec("hostname");
    print("Hostname: " + r1.output.trim());

    // Betriebszeit
    let r2 = exec("uptime");
    print("Betriebszeit: " + r2.output.trim());

    // Festplattennutzung
    let r3 = exec("df -h /");
    print("\nFestplattennutzung:");
    print(r3.output);

    // Speichernutzung
    let r4 = exec("free -h");
    print("Speichernutzung:");
    print(r4.output);
}

get_system_info();
```

### Beispiel 2: Log-Analysator

```hemlock
fn analyze_log(logfile: string) {
    print("Analysiere Log: " + logfile);

    // Gesamtzeilen zählen
    let r1 = exec("wc -l " + logfile);
    print("Gesamtzeilen: " + r1.output.trim());

    // Fehler zählen
    let r2 = exec("grep -c ERROR " + logfile + " 2>/dev/null");
    let errors = r2.output.trim();
    if (r2.exit_code == 0) {
        print("Fehler: " + errors);
    } else {
        print("Fehler: 0");
    }

    // Warnungen zählen
    let r3 = exec("grep -c WARN " + logfile + " 2>/dev/null");
    let warnings = r3.output.trim();
    if (r3.exit_code == 0) {
        print("Warnungen: " + warnings);
    } else {
        print("Warnungen: 0");
    }

    // Letzte Fehler
    print("\nLetzte Fehler:");
    let r4 = exec("grep ERROR " + logfile + " | tail -n 5");
    print(r4.output);
}

if (args.length < 2) {
    print("Verwendung: " + args[0] + " <logfile>");
} else {
    analyze_log(args[1]);
}
```

### Beispiel 3: Git-Helfer

```hemlock
fn git_status() {
    let r = exec("git status --short");
    if (r.exit_code != 0) {
        print("Fehler: Kein Git-Repository");
        return;
    }

    if (r.output == "") {
        print("Arbeitsverzeichnis sauber");
    } else {
        print("Änderungen:");
        print(r.output);
    }
}

fn git_quick_commit(message: string) {
    print("Füge alle Änderungen hinzu...");
    let r1 = exec("git add -A");
    if (r1.exit_code != 0) {
        print("Fehler beim Hinzufügen von Dateien");
        return;
    }

    print("Committe...");
    let safe_msg = message.replace_all("'", "'\\''");
    let r2 = exec("git commit -m '" + safe_msg + "'");
    if (r2.exit_code != 0) {
        print("Fehler beim Committen");
        return;
    }

    print("Erfolgreich committed");
    print(r2.output);
}

// Verwendung
git_status();
if (args.length > 1) {
    git_quick_commit(args[1]);
}
```

### Beispiel 4: Backup-Skript

```hemlock
fn backup_directory(source: string, dest: string) {
    print("Sichere " + source + " nach " + dest);

    // Backup-Verzeichnis erstellen
    let r1 = exec("mkdir -p " + dest);
    if (r1.exit_code != 0) {
        print("Fehler beim Erstellen des Backup-Verzeichnisses");
        return false;
    }

    // Tarball mit Zeitstempel erstellen
    let r2 = exec("date +%Y%m%d_%H%M%S");
    let timestamp = r2.output.trim();
    let backup_file = dest + "/backup_" + timestamp + ".tar.gz";

    print("Erstelle Archiv: " + backup_file);
    let r3 = exec("tar -czf " + backup_file + " " + source + " 2>&1");
    if (r3.exit_code != 0) {
        print("Fehler beim Erstellen des Backups:");
        print(r3.output);
        return false;
    }

    print("Backup erfolgreich abgeschlossen");

    // Backup-Größe anzeigen
    let r4 = exec("du -h " + backup_file);
    print("Backup-Größe: " + r4.output.trim());

    return true;
}

if (args.length < 3) {
    print("Verwendung: " + args[0] + " <source> <destination>");
} else {
    backup_directory(args[1], args[2]);
}
```

## Zusammenfassung

Hemlocks `exec()`-Funktion bietet:

- ✅ Einfache Shell-Befehlsausführung
- ✅ Ausgabeerfassung (stdout)
- ✅ Exit-Code-Prüfung
- ✅ Voller Zugang zu Shell-Funktionen (Pipes, Umleitungen, etc.)
- ✅ Integration mit System-Dienstprogrammen

Denken Sie daran:
- Immer Exit-Codes prüfen
- Sich der Sicherheitsimplikationen bewusst sein (Shell-Injection)
- Benutzereingaben vor der Verwendung in Befehlen validieren
- Hemlock-APIs gegenüber exec() bevorzugen, wenn verfügbar
- stderr wird nicht erfasst (verwenden Sie `2>&1` zum Umleiten)
- Befehle blockieren bis zur Fertigstellung
- Für kurz laufende Dienstprogramme verwenden, nicht für lang laufende Dienste

**Sicherheitscheckliste:**
- ❌ Niemals unsanitisierte Benutzereingaben verwenden
- ✅ Alle Eingaben validieren
- ✅ Allowlists für Befehle verwenden
- ✅ Sonderzeichen bei Bedarf escapen
- ✅ Mit geringstmöglichen Rechten ausführen
- ✅ Hemlock-APIs gegenüber Shell-Befehlen bevorzugen
