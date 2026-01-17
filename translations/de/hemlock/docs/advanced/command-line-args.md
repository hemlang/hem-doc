# Kommandozeilenargumente in Hemlock

Hemlock-Programme können auf Kommandozeilenargumente über ein eingebautes **`args`-Array** zugreifen, das automatisch beim Programmstart befüllt wird.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Das args-Array](#das-args-array)
- [Eigenschaften](#eigenschaften)
- [Iterationsmuster](#iterationsmuster)
- [Häufige Anwendungsfälle](#häufige-anwendungsfälle)
- [Argument-Parsing-Muster](#argument-parsing-muster)
- [Best Practices](#best-practices)
- [Vollständige Beispiele](#vollständige-beispiele)

## Überblick

Das `args`-Array bietet Zugriff auf Kommandozeilenargumente, die an Ihr Hemlock-Programm übergeben werden:

- **Immer verfügbar** - Eingebaute globale Variable in allen Hemlock-Programmen
- **Skriptname enthalten** - `args[0]` enthält immer den Skriptpfad/-namen
- **Array von Strings** - Alle Argumente sind Strings
- **Nullbasiert** - Standardmäßige Array-Indizierung (0, 1, 2, ...)

## Das args-Array

### Grundstruktur

```hemlock
// args[0] ist immer der Skript-Dateiname
// args[1] bis args[n-1] sind die eigentlichen Argumente
print(args[0]);        // "script.hml"
print(args.length);    // Gesamtzahl der Argumente (einschließlich Skriptname)
```

### Beispielverwendung

**Befehl:**
```bash
./hemlock script.hml hello world "test 123"
```

**In script.hml:**
```hemlock
print("Skriptname: " + args[0]);     // "script.hml"
print("Anzahl args: " + typeof(args.length));  // "4"
print("Erstes arg: " + args[1]);       // "hello"
print("Zweites arg: " + args[2]);      // "world"
print("Drittes arg: " + args[3]);      // "test 123"
```

### Index-Referenz

| Index | Enthält | Beispielwert |
|-------|---------|--------------|
| `args[0]` | Skriptpfad/-name | `"script.hml"` oder `"./script.hml"` |
| `args[1]` | Erstes Argument | `"hello"` |
| `args[2]` | Zweites Argument | `"world"` |
| `args[3]` | Drittes Argument | `"test 123"` |
| ... | ... | ... |
| `args[n-1]` | Letztes Argument | (variiert) |

## Eigenschaften

### Immer vorhanden

`args` ist ein globales Array, das in **allen** Hemlock-Programmen verfügbar ist:

```hemlock
// Keine Deklaration oder Import erforderlich
print(args.length);  // Funktioniert sofort
```

### Skriptname enthalten

`args[0]` enthält immer den Skriptpfad/-namen:

```hemlock
print("Führe aus: " + args[0]);
```

**Mögliche Werte für args[0]:**
- `"script.hml"` - Nur der Dateiname
- `"./script.hml"` - Relativer Pfad
- `"/home/user/script.hml"` - Absoluter Pfad
- Hängt davon ab, wie das Skript aufgerufen wurde

### Typ: Array von Strings

Alle Argumente werden als Strings gespeichert:

```hemlock
// Argumente: ./hemlock script.hml 42 3.14 true

print(args[1]);  // "42" (String, keine Zahl)
print(args[2]);  // "3.14" (String, keine Zahl)
print(args[3]);  // "true" (String, kein Boolean)

// Bei Bedarf konvertieren:
let num = 42;  // Bei Bedarf manuell parsen
```

### Minimale Länge

Immer mindestens 1 (der Skriptname):

```hemlock
print(args.length);  // Minimum: 1
```

**Auch ohne Argumente:**
```bash
./hemlock script.hml
```

```hemlock
// In script.hml:
print(args.length);  // 1 (nur Skriptname)
```

### REPL-Verhalten

Im REPL ist `args.length` 0 (leeres Array):

```hemlock
# REPL-Sitzung
> print(args.length);
0
```

## Iterationsmuster

### Einfache Iteration

`args[0]` (Skriptname) überspringen und eigentliche Argumente verarbeiten:

```hemlock
let i = 1;
while (i < args.length) {
    print("Argument " + typeof(i) + ": " + args[i]);
    i = i + 1;
}
```

**Ausgabe für: `./hemlock script.hml foo bar baz`**
```
Argument 1: foo
Argument 2: bar
Argument 3: baz
```

### For-In-Iteration (einschließlich Skriptname)

```hemlock
for (let arg in args) {
    print(arg);
}
```

**Ausgabe:**
```
script.hml
foo
bar
baz
```

### Argumentanzahl prüfen

```hemlock
if (args.length < 2) {
    print("Verwendung: " + args[0] + " <argument>");
    // exit oder return
} else {
    let arg = args[1];
    // arg verarbeiten
}
```

### Alle Argumente außer Skriptname verarbeiten

```hemlock
let actual_args = args.slice(1, args.length);

for (let arg in actual_args) {
    print("Verarbeite: " + arg);
}
```

## Häufige Anwendungsfälle

### 1. Einfache Argumentverarbeitung

Auf erforderliches Argument prüfen:

```hemlock
if (args.length < 2) {
    print("Verwendung: " + args[0] + " <filename>");
} else {
    let filename = args[1];
    print("Verarbeite Datei: " + filename);
    // ... Datei verarbeiten
}
```

**Verwendung:**
```bash
./hemlock script.hml data.txt
# Ausgabe: Verarbeite Datei: data.txt
```

### 2. Mehrere Argumente

```hemlock
if (args.length < 3) {
    print("Verwendung: " + args[0] + " <input> <output>");
} else {
    let input_file = args[1];
    let output_file = args[2];

    print("Eingabe: " + input_file);
    print("Ausgabe: " + output_file);

    // Dateien verarbeiten...
}
```

**Verwendung:**
```bash
./hemlock convert.hml input.txt output.txt
```

### 3. Variable Anzahl von Argumenten

Alle bereitgestellten Argumente verarbeiten:

```hemlock
if (args.length < 2) {
    print("Verwendung: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Verarbeite " + typeof(args.length - 1) + " Dateien:");

    let i = 1;
    while (i < args.length) {
        print("  " + args[i]);
        process_file(args[i]);
        i = i + 1;
    }
}
```

**Verwendung:**
```bash
./hemlock batch.hml file1.txt file2.txt file3.txt
```

### 4. Hilfenachricht

```hemlock
if (args.length < 2 || args[1] == "--help" || args[1] == "-h") {
    print("Verwendung: " + args[0] + " [OPTIONEN] <file>");
    print("Optionen:");
    print("  -h, --help     Diese Hilfenachricht anzeigen");
    print("  -v, --verbose  Ausführliche Ausgabe aktivieren");
} else {
    // Normal verarbeiten
}
```

### 5. Argumentvalidierung

```hemlock
fn validate_file(filename: string): bool {
    // Prüfen, ob Datei existiert (Beispiel)
    return filename != "";
}

if (args.length < 2) {
    print("Fehler: Kein Dateiname angegeben");
} else if (!validate_file(args[1])) {
    print("Fehler: Ungültige Datei: " + args[1]);
} else {
    print("Verarbeite: " + args[1]);
}
```

## Argument-Parsing-Muster

### Benannte Argumente (Flags)

Einfaches Muster für benannte Argumente:

```hemlock
let verbose = false;
let output_file = "";
let input_file = "";

let i = 1;
while (i < args.length) {
    if (args[i] == "--verbose" || args[i] == "-v") {
        verbose = true;
    } else if (args[i] == "--output" || args[i] == "-o") {
        i = i + 1;
        if (i < args.length) {
            output_file = args[i];
        }
    } else {
        input_file = args[i];
    }
    i = i + 1;
}

if (verbose) {
    print("Ausführlicher Modus aktiviert");
}
print("Eingabe: " + input_file);
print("Ausgabe: " + output_file);
```

**Verwendung:**
```bash
./hemlock script.hml --verbose --output out.txt input.txt
./hemlock script.hml -v -o out.txt input.txt
```

### Boolean-Flags

```hemlock
let debug = false;
let verbose = false;
let force = false;

let i = 1;
while (i < args.length) {
    if (args[i] == "--debug") {
        debug = true;
    } else if (args[i] == "--verbose") {
        verbose = true;
    } else if (args[i] == "--force") {
        force = true;
    }
    i = i + 1;
}
```

### Wert-Argumente

```hemlock
let config_file = "default.conf";
let port = 8080;

let i = 1;
while (i < args.length) {
    if (args[i] == "--config") {
        i = i + 1;
        if (i < args.length) {
            config_file = args[i];
        }
    } else if (args[i] == "--port") {
        i = i + 1;
        if (i < args.length) {
            port = 8080;  // Müsste String zu Int parsen
        }
    }
    i = i + 1;
}
```

### Gemischte positionelle und benannte Argumente

```hemlock
let input_file = "";
let output_file = "";
let verbose = false;

let i = 1;
let positional = [];

while (i < args.length) {
    if (args[i] == "--verbose") {
        verbose = true;
    } else {
        // Als positionelles Argument behandeln
        positional.push(args[i]);
    }
    i = i + 1;
}

// Positionelle Argumente zuweisen
if (positional.length > 0) {
    input_file = positional[0];
}
if (positional.length > 1) {
    output_file = positional[1];
}
```

### Argument-Parser-Hilfsfunktion

```hemlock
fn parse_args() {
    let options = {
        verbose: false,
        output: "",
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            options.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                options.output = args[i];
            }
        } else {
            // Positionelles Argument
            options.files.push(arg);
        }

        i = i + 1;
    }

    return options;
}

let opts = parse_args();
print("Verbose: " + typeof(opts.verbose));
print("Ausgabe: " + opts.output);
print("Dateien: " + typeof(opts.files.length));
```

## Best Practices

### 1. Immer Argumentanzahl prüfen

```hemlock
// Gut
if (args.length < 2) {
    print("Verwendung: " + args[0] + " <file>");
} else {
    process_file(args[1]);
}

// Schlecht - kann abstürzen wenn keine Argumente
process_file(args[1]);  // Fehler wenn args.length == 1
```

### 2. Verwendungsinformationen bereitstellen

```hemlock
fn show_usage() {
    print("Verwendung: " + args[0] + " [OPTIONEN] <file>");
    print("Optionen:");
    print("  -h, --help     Hilfe anzeigen");
    print("  -v, --verbose  Ausführliche Ausgabe");
}

if (args.length < 2) {
    show_usage();
}
```

### 3. Argumente validieren

```hemlock
fn validate_args() {
    if (args.length < 2) {
        print("Fehler: Erforderliches Argument fehlt");
        return false;
    }

    if (args[1] == "") {
        print("Fehler: Leeres Argument");
        return false;
    }

    return true;
}

if (!validate_args()) {
    // exit oder Verwendung anzeigen
}
```

### 4. Aussagekräftige Variablennamen verwenden

```hemlock
// Gut
let input_filename = args[1];
let output_filename = args[2];
let max_iterations = args[3];

// Schlecht
let a = args[1];
let b = args[2];
let c = args[3];
```

### 5. Argumente mit Leerzeichen in Anführungszeichen behandeln

Shell behandelt dies automatisch:

```bash
./hemlock script.hml "file with spaces.txt"
```

```hemlock
print(args[1]);  // "file with spaces.txt"
```

### 6. Argumentobjekte erstellen

```hemlock
fn get_args() {
    return {
        script: args[0],
        input: args[1],
        output: args[2]
    };
}

let arguments = get_args();
print("Eingabe: " + arguments.input);
```

## Vollständige Beispiele

### Beispiel 1: Dateiverarbeiter

```hemlock
// Verwendung: ./hemlock process.hml <input> <output>

fn show_usage() {
    print("Verwendung: " + args[0] + " <input_file> <output_file>");
}

if (args.length < 3) {
    show_usage();
} else {
    let input = args[1];
    let output = args[2];

    print("Verarbeite " + input + " -> " + output);

    // Dateien verarbeiten
    let f_in = open(input, "r");
    let f_out = open(output, "w");

    try {
        let content = f_in.read();
        let processed = content.to_upper();  // Beispielverarbeitung
        f_out.write(processed);

        print("Fertig!");
    } finally {
        f_in.close();
        f_out.close();
    }
}
```

### Beispiel 2: Stapel-Dateiverarbeiter

```hemlock
// Verwendung: ./hemlock batch.hml <file1> <file2> <file3> ...

if (args.length < 2) {
    print("Verwendung: " + args[0] + " <file1> [file2] [file3] ...");
} else {
    print("Verarbeite " + typeof(args.length - 1) + " Dateien:");

    let i = 1;
    while (i < args.length) {
        let filename = args[i];
        print("  Verarbeite: " + filename);

        try {
            let f = open(filename, "r");
            let content = f.read();
            f.close();

            // Inhalt verarbeiten...
            print("    " + typeof(content.length) + " Bytes");
        } catch (e) {
            print("    Fehler: " + e);
        }

        i = i + 1;
    }

    print("Fertig!");
}
```

### Beispiel 3: Fortgeschrittener Argument-Parser

```hemlock
// Verwendung: ./hemlock app.hml [OPTIONEN] <files...>
// Optionen:
//   --verbose, -v     Ausführliche Ausgabe aktivieren
//   --output, -o FILE Ausgabedatei festlegen
//   --help, -h        Hilfe anzeigen

fn parse_arguments() {
    let config = {
        verbose: false,
        output: "output.txt",
        help: false,
        files: []
    };

    let i = 1;
    while (i < args.length) {
        let arg = args[i];

        if (arg == "--verbose" || arg == "-v") {
            config.verbose = true;
        } else if (arg == "--output" || arg == "-o") {
            i = i + 1;
            if (i < args.length) {
                config.output = args[i];
            } else {
                print("Fehler: --output erfordert einen Wert");
            }
        } else if (arg == "--help" || arg == "-h") {
            config.help = true;
        } else if (arg.starts_with("--")) {
            print("Fehler: Unbekannte Option: " + arg);
        } else {
            config.files.push(arg);
        }

        i = i + 1;
    }

    return config;
}

fn show_help() {
    print("Verwendung: " + args[0] + " [OPTIONEN] <files...>");
    print("Optionen:");
    print("  --verbose, -v     Ausführliche Ausgabe aktivieren");
    print("  --output, -o FILE Ausgabedatei festlegen");
    print("  --help, -h        Diese Hilfe anzeigen");
}

let config = parse_arguments();

if (config.help) {
    show_help();
} else if (config.files.length == 0) {
    print("Fehler: Keine Eingabedateien angegeben");
    show_help();
} else {
    if (config.verbose) {
        print("Ausführlicher Modus aktiviert");
        print("Ausgabedatei: " + config.output);
        print("Eingabedateien: " + typeof(config.files.length));
    }

    // Dateien verarbeiten
    for (let file in config.files) {
        if (config.verbose) {
            print("Verarbeite: " + file);
        }
        // ... Datei verarbeiten
    }
}
```

### Beispiel 4: Konfigurationswerkzeug

```hemlock
// Verwendung: ./hemlock config.hml <action> [arguments]
// Aktionen:
//   get <key>
//   set <key> <value>
//   list

fn show_usage() {
    print("Verwendung: " + args[0] + " <action> [arguments]");
    print("Aktionen:");
    print("  get <key>         Konfigurationswert abrufen");
    print("  set <key> <value> Konfigurationswert setzen");
    print("  list              Alle Konfigurationen auflisten");
}

if (args.length < 2) {
    show_usage();
} else {
    let action = args[1];

    if (action == "get") {
        if (args.length < 3) {
            print("Fehler: 'get' erfordert einen Schlüssel");
        } else {
            let key = args[2];
            print("Hole: " + key);
            // ... aus Konfiguration holen
        }
    } else if (action == "set") {
        if (args.length < 4) {
            print("Fehler: 'set' erfordert Schlüssel und Wert");
        } else {
            let key = args[2];
            let value = args[3];
            print("Setze " + key + " = " + value);
            // ... in Konfiguration setzen
        }
    } else if (action == "list") {
        print("Liste alle Konfigurationen auf:");
        // ... Konfiguration auflisten
    } else {
        print("Fehler: Unbekannte Aktion: " + action);
        show_usage();
    }
}
```

## Zusammenfassung

Hemlocks Kommandozeilenargument-Unterstützung bietet:

- ✅ Eingebautes `args`-Array global verfügbar
- ✅ Einfacher Array-basierter Zugriff auf Argumente
- ✅ Skriptname in `args[0]`
- ✅ Alle Argumente als Strings
- ✅ Array-Methoden verfügbar (.length, .slice, etc.)

Denken Sie daran:
- Immer `args.length` prüfen, bevor auf Elemente zugegriffen wird
- `args[0]` ist der Skriptname
- Eigentliche Argumente beginnen bei `args[1]`
- Alle Argumente sind Strings - bei Bedarf konvertieren
- Verwendungsinformationen für benutzerfreundliche Tools bereitstellen
- Argumente vor der Verarbeitung validieren

Häufige Muster:
- Einfache positionelle Argumente
- Benannte/Flag-Argumente (--flag)
- Wert-Argumente (--option wert)
- Hilfenachrichten (--help)
- Argumentvalidierung
