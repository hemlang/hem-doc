# Fehlerbehandlung

Hemlock unterstützt ausnahmebasierte Fehlerbehandlung mit `try`, `catch`, `finally`, `throw` und `panic`. Diese Anleitung behandelt behebbare Fehler mit Ausnahmen und nicht behebbare Fehler mit panic.

## Überblick

```hemlock
// Grundlegende Fehlerbehandlung
try {
    risky_operation();
} catch (e) {
    print("Fehler: " + e);
}

// Mit Bereinigung
try {
    process_file();
} catch (e) {
    print("Fehlgeschlagen: " + e);
} finally {
    cleanup();
}

// Fehler werfen
fn divide(a, b) {
    if (b == 0) {
        throw "Division durch Null";
    }
    return a / b;
}
```

## Try-Catch-Finally

### Syntax

**Einfaches try/catch:**
```hemlock
try {
    // riskanter Code
} catch (e) {
    // Fehler behandeln, e enthält den geworfenen Wert
}
```

**Try/finally:**
```hemlock
try {
    // riskanter Code
} finally {
    // wird immer ausgeführt, auch wenn Ausnahme geworfen
}
```

**Try/catch/finally:**
```hemlock
try {
    // riskanter Code
} catch (e) {
    // Fehler behandeln
} finally {
    // Bereinigungscode
}
```

### Try-Block

Der try-Block führt Anweisungen sequentiell aus:

```hemlock
try {
    print("Starte...");
    risky_operation();
    print("Erfolg!");  // Nur wenn keine Ausnahme
}
```

**Verhalten:**
- Fuehrt Anweisungen der Reihe nach aus
- Wenn Ausnahme geworfen: springt zu `catch` oder `finally`
- Wenn keine Ausnahme: führt `finally` aus (falls vorhanden), dann weiter

### Catch-Block

Der catch-Block empfaengt den geworfenen Wert:

```hemlock
try {
    throw "hoppla";
} catch (error) {
    print("Gefangen: " + error);  // error = "hoppla"
    // error nur hier zugänglich
}
// error hier nicht zugänglich
```

**Catch-Parameter:**
- Empfaengt den geworfenen Wert (beliebiger Typ)
- Auf den catch-Block beschränkt
- Kann beliebig benannt werden (konventionell `e`, `err` oder `error`)

**Was Sie im catch tun können:**
```hemlock
try {
    risky_operation();
} catch (e) {
    // Fehler protokollieren
    print("Fehler: " + e);

    // Gleichen Fehler erneut werfen
    throw e;

    // Anderen Fehler werfen
    throw "anderer Fehler";

    // Standardwert zurückgeben
    return null;

    // Behandeln und fortfahren
    // (kein erneutes Werfen)
}
```

### Finally-Block

Der finally-Block wird **immer ausgeführt**:

```hemlock
try {
    print("1: try-Block");
    throw "Fehler";
} catch (e) {
    print("2: catch-Block");
} finally {
    print("3: finally-Block");  // Wird immer ausgeführt
}
print("4: nach try/catch/finally");

// Ausgabe: 1: try-Block, 2: catch-Block, 3: finally-Block, 4: nach try/catch/finally
```

**Wann finally ausgeführt wird:**
- Nach dem try-Block (wenn keine Ausnahme)
- Nach dem catch-Block (wenn Ausnahme gefangen)
- Auch wenn try/catch `return`, `break` oder `continue` enthält
- Bevor der Kontrollfluss try/catch verlässt

**Finally mit return:**
```hemlock
fn example() {
    try {
        return 1;  // Gibt 1 zurück nach finally-Ausführung
    } finally {
        print("bereinigung");  // Wird vor Rückgabe ausgeführt
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Finally-return überschreibt - gibt 2 zurück
    }
}
```

**Finally mit Kontrollfluss:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) {
            break;  // Bricht nach finally-Ausführung ab
        }
    } finally {
        print("bereinigung " + typeof(i));
    }
}
```

## Throw-Anweisung

### Einfaches Throw

Jeden Wert als Ausnahme werfen:

```hemlock
throw "Fehlermeldung";
throw 404;
throw { code: 500, message: "Interner Fehler" };
throw null;
throw ["fehler", "details"];
```

**Ausführung:**
1. Wertet den Ausdruck aus
2. Springt sofort zum nächsten umschliessenden `catch`
3. Wenn kein `catch`, propagiert nach oben im Aufrufstapel

### Fehler werfen

```hemlock
fn validate_age(age: i32) {
    if (age < 0) {
        throw "Alter kann nicht negativ sein";
    }
    if (age > 150) {
        throw "Alter ist unrealistisch";
    }
}

try {
    validate_age(-5);
} catch (e) {
    print("Validierungsfehler: " + e);
}
```

### Fehlerobjekte werfen

Strukturierte Fehlerinformationen erstellen:

```hemlock
fn read_file(path: string) {
    if (!file_exists(path)) {
        throw {
            type: "FileNotFound",
            path: path,
            message: "Datei existiert nicht"
        };
    }
    // ... Datei lesen
}

try {
    read_file("missing.txt");
} catch (e) {
    if (e.type == "FileNotFound") {
        print("Datei nicht gefunden: " + e.path);
    }
}
```

### Erneutes Werfen

Fehler fangen und erneut werfen:

```hemlock
fn wrapper() {
    try {
        risky_operation();
    } catch (e) {
        print("Fehler protokollieren: " + e);
        throw e;  // An Aufrufer erneut werfen
    }
}

try {
    wrapper();
} catch (e) {
    print("In main gefangen: " + e);
}
```

## Nicht gefangene Ausnahmen

Wenn eine Ausnahme ohne gefangen zu werden bis zum Anfang des Aufrufstapels propagiert:

```hemlock
fn foo() {
    throw "nicht gefangen!";
}

foo();  // Stuerzt ab mit: Laufzeitfehler: nicht gefangen!
```

**Verhalten:**
- Programm stuerzt ab
- Gibt Fehlermeldung auf stderr aus
- Beendet mit nicht-null Statuscode
- Stack-Trace wird in zukuenftigen Versionen hinzugefügt

## Panic - Nicht behebbare Fehler

### Was ist Panic?

`panic()` ist für **nicht behebbare Fehler**, die das Programm sofort beenden sollen:

```hemlock
panic();                    // Standardmeldung: "panic!"
panic("benutzerdefinierte Meldung");    // Benutzerdefinierte Meldung
panic(42);                  // Nicht-String-Werte werden ausgegeben
```

**Semantik:**
- **Beendet sofort** das Programm mit Exit-Code 1
- Gibt Fehlermeldung auf stderr aus: `panic: <meldung>`
- **NICHT fangbar** mit try/catch
- Für Bugs und nicht behebbare Fehler verwenden

### Panic vs. Throw

```hemlock
// throw - Behebbarer Fehler (kann gefangen werden)
try {
    throw "behebbarer Fehler";
} catch (e) {
    print("Gefangen: " + e);  // Erfolgreich gefangen
}

// panic - Nicht behebbarer Fehler (kann nicht gefangen werden)
try {
    panic("nicht behebbarer Fehler");  // Programm beendet sofort
} catch (e) {
    print("Das wird nie ausgeführt");       // Wird nie ausgeführt
}
```

### Wann Panic verwenden

**Panic verwenden für:**
- **Bugs**: Unerreichbarer Code wurde erreicht
- **Ungueltiger Zustand**: Datenstrukturkorruption erkannt
- **Nicht behebbare Fehler**: Kritische Ressource nicht verfügbar
- **Assertionsfehler**: Wenn `assert()` nicht ausreicht

**Beispiele:**
```hemlock
// Unerreichbarer Code
fn process_state(state: i32) {
    if (state == 1) {
        return "ready";
    } else if (state == 2) {
        return "running";
    } else if (state == 3) {
        return "stopped";
    } else {
        panic("ungueltiger Zustand: " + typeof(state));  // Sollte nie passieren
    }
}

// Kritische Ressourcenpruefung
fn init_system() {
    let config = read_file("config.json");
    if (config == null) {
        panic("config.json nicht gefunden - kann nicht starten");
    }
    // ...
}

// Datenstruktur-Invariante
fn pop_stack(stack) {
    if (stack.length == 0) {
        panic("pop() auf leerem Stack aufgerufen");
    }
    return stack.pop();
}
```

### Wann NICHT Panic verwenden

**Throw stattdessen verwenden für:**
- Benutzereingabe-Validierung
- Datei nicht gefunden
- Netzwerkfehler
- Erwartete Fehlerbedingungen

```hemlock
// SCHLECHT: Panic für erwartete Fehler
fn divide(a, b) {
    if (b == 0) {
        panic("Division durch Null");  // Zu hart
    }
    return a / b;
}

// GUT: Throw für erwartete Fehler
fn divide(a, b) {
    if (b == 0) {
        throw "Division durch Null";  // Behebbar
    }
    return a / b;
}
```

## Kontrollfluss-Interaktionen

### Return innerhalb Try/Catch/Finally

```hemlock
fn example() {
    try {
        return 1;  // Gibt 1 zurück nach finally-Ausführung
    } finally {
        print("bereinigung");
    }
}

fn example2() {
    try {
        return 1;
    } finally {
        return 2;  // Finally-return überschreibt try-return - gibt 2 zurück
    }
}
```

**Regel:** Finally-Block-Rueckgabewerte ueberschreiben try/catch-Rueckgabewerte.

### Break/Continue innerhalb Try/Catch/Finally

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    try {
        if (i == 5) { break; }  // Bricht nach finally-Ausführung ab
    } finally {
        print("bereinigung " + typeof(i));
    }
}
```

**Regel:** Break/continue werden nach dem finally-Block ausgeführt.

### Verschachteltes Try/Catch

```hemlock
try {
    try {
        throw "inner";
    } catch (e) {
        print("Gefangen: " + e);  // Gibt aus: Gefangen: inner
        throw "outer";  // Anderen Fehler erneut werfen
    }
} catch (e) {
    print("Gefangen: " + e);  // Gibt aus: Gefangen: outer
}
```

**Regel:** Verschachtelte try/catch-Blöcke funktionieren wie erwartet, innere catches geschehen zuerst.

## Gängige Muster

### Muster: Ressourcenbereinigung

Immer `finally` für Bereinigung verwenden:

```hemlock
fn process_file(filename) {
    let file = null;
    try {
        file = open(filename);
        let content = file.read();
        process(content);
    } catch (e) {
        print("Fehler beim Verarbeiten der Datei: " + e);
    } finally {
        if (file != null) {
            file.close();  // Schliesst immer, auch bei Fehler
        }
    }
}
```

### Muster: Fehler-Wrapping

Niedrigstufige Fehler mit Kontext umwickeln:

```hemlock
fn load_config(path) {
    try {
        let content = read_file(path);
        return parse_json(content);
    } catch (e) {
        throw "Fehler beim Laden der Konfiguration von " + path + ": " + e;
    }
}
```

### Muster: Fehlerwiederherstellung

Fallback bei Fehler bereitstellen:

```hemlock
fn safe_divide(a, b) {
    try {
        if (b == 0) {
            throw "Division durch Null";
        }
        return a / b;
    } catch (e) {
        print("Fehler: " + e);
        return null;  // Fallback-Wert
    }
}
```

### Muster: Validierung

Ausnahmen für Validierung verwenden:

```hemlock
fn validate_user(user) {
    if (user.name == null || user.name == "") {
        throw "Name ist erforderlich";
    }
    if (user.age < 0 || user.age > 150) {
        throw "Ungueltiges Alter";
    }
    if (user.email == null || !user.email.contains("@")) {
        throw "Ungueltige E-Mail";
    }
}

try {
    validate_user({ name: "Alice", age: -5, email: "ungültig" });
} catch (e) {
    print("Validierung fehlgeschlagen: " + e);
}
```

### Muster: Mehrere Fehlertypen

Fehlerobjekte verwenden, um Fehlertypen zu unterscheiden:

```hemlock
fn process_data(data) {
    if (data == null) {
        throw { type: "NullData", message: "Daten sind null" };
    }

    if (typeof(data) != "array") {
        throw { type: "TypeError", message: "Array erwartet" };
    }

    if (data.length == 0) {
        throw { type: "EmptyData", message: "Array ist leer" };
    }

    // ... verarbeiten
}

try {
    process_data(null);
} catch (e) {
    if (e.type == "NullData") {
        print("Keine Daten bereitgestellt");
    } else if (e.type == "TypeError") {
        print("Falscher Datentyp: " + e.message);
    } else {
        print("Fehler: " + e.message);
    }
}
```

## Best Practices

1. **Ausnahmen für Ausnahmefaelle verwenden** - Nicht für normalen Kontrollfluss
2. **Aussagekraeftige Fehler werfen** - Strings oder Objekte mit Kontext verwenden
3. **Immer finally für Bereinigung verwenden** - Stellt sicher, dass Ressourcen freigegeben werden
4. **Nicht fangen und ignorieren** - Mindestens den Fehler protokollieren
5. **Bei Bedarf erneut werfen** - Aufrufer behandeln lassen, wenn Sie nicht können
6. **Panic für Bugs** - Panic für nicht behebbare Fehler verwenden
7. **Ausnahmen dokumentieren** - Klar machen, welche Funktionen werfen können

## Häufige Fallstricke

### Fallstrick: Fehler verschlucken

```hemlock
// SCHLECHT: Stilles Scheitern
try {
    risky_operation();
} catch (e) {
    // Fehler ignoriert - stilles Scheitern
}

// GUT: Protokollieren oder behandeln
try {
    risky_operation();
} catch (e) {
    print("Operation fehlgeschlagen: " + e);
    // Angemessen behandeln
}
```

### Fallstrick: Finally-Ueberschreibung

```hemlock
// SCHLECHT: Finally überschreibt return
fn get_value() {
    try {
        return 42;
    } finally {
        return 0;  // Gibt 0 zurück, nicht 42!
    }
}

// GUT: Nicht in finally returnen
fn get_value() {
    try {
        return 42;
    } finally {
        cleanup();  // Nur bereinigen, kein return
    }
}
```

### Fallstrick: Bereinigung vergessen

```hemlock
// SCHLECHT: Datei wird bei Fehler moeglicherweise nicht geschlossen
fn process() {
    let file = open("data.txt");
    let content = file.read();  // Kann werfen
    file.close();  // Wird bei Fehler nie erreicht
}

// GUT: Finally verwenden
fn process() {
    let file = null;
    try {
        file = open("data.txt");
        let content = file.read();
    } finally {
        if (file != null) {
            file.close();
        }
    }
}
```

### Fallstrick: Panic für erwartete Fehler verwenden

```hemlock
// SCHLECHT: Panic für erwarteten Fehler
fn read_config(path) {
    if (!file_exists(path)) {
        panic("Konfigurationsdatei nicht gefunden");  // Zu hart
    }
    return read_file(path);
}

// GUT: Throw für erwarteten Fehler
fn read_config(path) {
    if (!file_exists(path)) {
        throw "Konfigurationsdatei nicht gefunden: " + path;  // Behebbar
    }
    return read_file(path);
}
```

## Beispiele

### Beispiel: Grundlegende Fehlerbehandlung

```hemlock
fn divide(a, b) {
    if (b == 0) {
        throw "Division durch Null";
    }
    return a / b;
}

try {
    print(divide(10, 0));
} catch (e) {
    print("Fehler: " + e);  // Gibt aus: Fehler: Division durch Null
}
```

### Beispiel: Ressourcenverwaltung

```hemlock
fn copy_file(src, dst) {
    let src_file = null;
    let dst_file = null;

    try {
        src_file = open(src, "r");
        dst_file = open(dst, "w");

        let content = src_file.read();
        dst_file.write(content);

        print("Datei erfolgreich kopiert");
    } catch (e) {
        print("Fehler beim Kopieren der Datei: " + e);
        throw e;  // Erneut werfen
    } finally {
        if (src_file != null) { src_file.close(); }
        if (dst_file != null) { dst_file.close(); }
    }
}
```

### Beispiel: Verschachtelte Fehlerbehandlung

```hemlock
fn process_users(users) {
    let success_count = 0;
    let error_count = 0;

    let i = 0;
    while (i < users.length) {
        try {
            validate_user(users[i]);
            save_user(users[i]);
            success_count = success_count + 1;
        } catch (e) {
            print("Fehler beim Verarbeiten des Benutzers: " + e);
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    print("Verarbeitet: " + typeof(success_count) + " erfolgreich, " + typeof(error_count) + " Fehler");
}
```

### Beispiel: Benutzerdefinierte Fehlertypen

```hemlock
fn create_error(type, message, details) {
    return {
        type: type,
        message: message,
        details: details,
        toString: fn() {
            return self.type + ": " + self.message;
        }
    };
}

fn divide(a, b) {
    if (typeof(a) != "i32" && typeof(a) != "f64") {
        throw create_error("TypeError", "a muss eine Zahl sein", { value: a });
    }
    if (typeof(b) != "i32" && typeof(b) != "f64") {
        throw create_error("TypeError", "b muss eine Zahl sein", { value: b });
    }
    if (b == 0) {
        throw create_error("DivisionByZero", "Division durch Null nicht möglich", { a: a, b: b });
    }
    return a / b;
}

try {
    divide(10, 0);
} catch (e) {
    print(e.toString());
    if (e.type == "DivisionByZero") {
        print("Details: a=" + typeof(e.details.a) + ", b=" + typeof(e.details.b));
    }
}
```

### Beispiel: Wiederholungslogik

```hemlock
fn retry(operation, max_attempts) {
    let attempt = 0;

    while (attempt < max_attempts) {
        try {
            return operation();  // Erfolg!
        } catch (e) {
            attempt = attempt + 1;
            if (attempt >= max_attempts) {
                throw "Operation fehlgeschlagen nach " + typeof(max_attempts) + " Versuchen: " + e;
            }
            print("Versuch " + typeof(attempt) + " fehlgeschlagen, wiederhole...");
        }
    }
}

fn unreliable_operation() {
    // Simulierte unzuverlaessige Operation
    if (random() < 0.7) {
        throw "Operation fehlgeschlagen";
    }
    return "Erfolg";
}

try {
    let result = retry(unreliable_operation, 3);
    print(result);
} catch (e) {
    print("Alle Wiederholungen fehlgeschlagen: " + e);
}
```

## Ausfuehrungsreihenfolge

Verständnis der Ausfuehrungsreihenfolge:

```hemlock
try {
    print("1: try-Block Start");
    throw "fehler";
    print("2: nie erreicht");
} catch (e) {
    print("3: catch-Block");
} finally {
    print("4: finally-Block");
}
print("5: nach try/catch/finally");

// Ausgabe:
// 1: try-Block Start
// 3: catch-Block
// 4: finally-Block
// 5: nach try/catch/finally
```

## Aktuelle Einschränkungen

- **Kein Stack-Trace** - Nicht gefangene Ausnahmen zeigen keinen Stack-Trace (geplant)
- **Einige Builtins beenden** - Einige eingebaute Funktionen rufen noch `exit()` statt zu werfen auf (wird überprüft)
- **Keine benutzerdefinierten Ausnahmetypen** - Jeder Wert kann geworfen werden, aber keine formale Ausnahmehierarchie

## Verwandte Themen

- [Functions](functions.md) - Ausnahmen und Funktionsrueckgaben
- [Control Flow](control-flow.md) - Wie Ausnahmen den Kontrollfluss beeinflussen
- [Memory](memory.md) - Finally für Speicherbereinigung verwenden

## Siehe auch

- **Ausnahmesemantik**: Siehe CLAUDE.md Abschnitt "Error Handling"
- **Panic vs. Throw**: Verschiedene Anwendungsfaelle für verschiedene Fehlertypen
- **Finally-Garantie**: Wird immer ausgeführt, auch bei return/break/continue
