# Kontrollfluss

Hemlock bietet vertrauten C-ähnlichen Kontrollfluss mit obligatorischen geschweiften Klammern und expliziter Syntax. Diese Anleitung behandelt Bedingungen, Schleifen, Switch-Anweisungen und Operatoren.

## Überblick

Verfuegbare Kontrollfluss-Funktionen:

- `if`/`else`/`else if` - Bedingte Verzweigungen
- `while`-Schleifen - Bedingungsbasierte Iteration
- `for`-Schleifen - C-artige und for-in-Iteration
- `loop` - Endlosschleifen (sauberer als `while (true)`)
- `switch`-Anweisungen - Mehrfachverzweigung
- `break`/`continue` - Schleifensteuerung
- Schleifen-Labels - Gezieltes break/continue für verschachtelte Schleifen
- `defer` - Verzögerte Ausführung (Bereinigung)
- Boolesche Operatoren: `&&`, `||`, `!`
- Vergleichsoperatoren: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Bitweise Operatoren: `&`, `|`, `^`, `<<`, `>>`, `~`

## If-Anweisungen

### Einfaches If/Else

```hemlock
if (x > 10) {
    print("groß");
} else {
    print("klein");
}
```

**Regeln:**
- Geschweifte Klammern sind **immer erforderlich** für alle Zweige
- Bedingungen müssen in Klammern eingeschlossen sein
- Keine optionalen geschweiften Klammern (anders als C)

### If ohne Else

```hemlock
if (x > 0) {
    print("positiv");
}
// Kein else-Zweig nötig
```

### Else-If-Ketten

```hemlock
if (x > 100) {
    print("sehr groß");
} else if (x > 50) {
    print("groß");
} else if (x > 10) {
    print("mittel");
} else {
    print("klein");
}
```

**Hinweis:** `else if` ist syntaktischer Zucker für verschachtelte if-Anweisungen. Diese sind äquivalent:

```hemlock
// else if (syntaktischer Zucker)
if (a) {
    foo();
} else if (b) {
    bar();
}

// Äquivalentes verschachteltes if
if (a) {
    foo();
} else {
    if (b) {
        bar();
    }
}
```

### Verschachtelte If-Anweisungen

```hemlock
if (x > 0) {
    if (x < 10) {
        print("einstellig positiv");
    } else {
        print("mehrstellig positiv");
    }
} else {
    print("nicht positiv");
}
```

## While-Schleifen

Bedingungsbasierte Iteration:

```hemlock
let i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

**Endlosschleifen (alter Stil):**
```hemlock
while (true) {
    // ... Arbeit erledigen
    if (should_exit) {
        break;
    }
}
```

**Hinweis:** Für Endlosschleifen bevorzugen Sie das `loop`-Schlüsselwort (siehe unten).

## Loop (Endlosschleife)

Das Schlüsselwort `loop` bietet eine sauberere Syntax für Endlosschleifen:

```hemlock
loop {
    // ... Arbeit erledigen
    if (should_exit) {
        break;
    }
}
```

**Äquivalent zu `while (true)`, aber expliziter in der Absicht.**

### Einfache Schleife mit Break

```hemlock
let i = 0;
loop {
    if (i >= 5) {
        break;
    }
    print(i);
    i = i + 1;
}
// Gibt aus: 0, 1, 2, 3, 4
```

### Schleife mit Continue

```hemlock
let i = 0;
loop {
    i = i + 1;
    if (i > 5) {
        break;
    }
    if (i == 3) {
        continue;  // Überspringt Ausgabe von 3
    }
    print(i);
}
// Gibt aus: 1, 2, 4, 5
```

### Verschachtelte Schleifen

```hemlock
let x = 0;
loop {
    if (x >= 2) { break; }
    let y = 0;
    loop {
        if (y >= 3) { break; }
        print(x * 10 + y);
        y = y + 1;
    }
    x = x + 1;
}
// Gibt aus: 0, 1, 2, 10, 11, 12
```

### Wann Loop verwenden

- **`loop` verwenden** für absichtlich unendliche Schleifen, die via `break` beendet werden
- **`while` verwenden** wenn es eine natuerliche Abbruchbedingung gibt
- **`for` verwenden** beim Iterieren einer bekannten Anzahl von Malen oder über eine Sammlung

## For-Schleifen

### C-artige For-Schleife

Klassische dreiteilige For-Schleife:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**Komponenten:**
- **Initialisierer**: `let i = 0` - Wird einmal vor der Schleife ausgeführt
- **Bedingung**: `i < 10` - Wird vor jeder Iteration geprüft
- **Aktualisierung**: `i = i + 1` - Wird nach jeder Iteration ausgeführt

**Gültigkeitsbereich:**
```hemlock
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
// i ist hier nicht zugänglich (schleifenbezogen)
```

### For-In-Schleifen

Über Array-Elemente iterieren:

```hemlock
let arr = [1, 2, 3, 4, 5];
for (let item in arr) {
    print(item);  // Gibt jedes Element aus
}
```

**Mit Index und Wert:**
```hemlock
let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i = i + 1) {
    print(`Index: ${i}, Wert: ${arr[i]}`);
}
```

## Switch-Anweisungen

Mehrfachverzweigung basierend auf Wert:

### Einfacher Switch

```hemlock
let x = 2;

switch (x) {
    case 1:
        print("eins");
        break;
    case 2:
        print("zwei");
        break;
    case 3:
        print("drei");
        break;
}
```

### Switch mit Default

```hemlock
let color = "blue";

switch (color) {
    case "red":
        print("stop");
        break;
    case "yellow":
        print("langsam");
        break;
    case "green":
        print("los");
        break;
    default:
        print("unbekannte Farbe");
        break;
}
```

**Regeln:**
- `default` trifft zu, wenn kein anderer Fall zutrifft
- `default` kann überall im Switch-Körper erscheinen
- Nur ein default-Fall erlaubt

### Fall-Through-Verhalten

Faelle ohne `break` fallen durch zum nächsten Fall (C-artiges Verhalten). Dies ist **beabsichtigt** und kann zum Gruppieren von Faellen verwendet werden:

```hemlock
let grade = 85;

switch (grade) {
    case 100:
    case 95:
    case 90:
        print("A");
        break;
    case 85:
    case 80:
        print("B");
        break;
    default:
        print("C oder schlechter");
        break;
}
```

**Explizites Fall-Through-Beispiel:**
```hemlock
let day = 3;

switch (day) {
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        print("Wochentag");
        break;
    case 6:
    case 7:
        print("Wochenende");
        break;
}
```

**Wichtig:** Anders als einige moderne Sprachen erfordert Hemlock KEIN explizites `fallthrough`-Schlüsselwort. Faelle fallen automatisch durch, es sei denn, sie werden durch `break`, `return` oder `throw` beendet. Verwenden Sie immer `break`, um unbeabsichtigtes Fall-Through zu verhindern.

### Switch mit Return

In Funktionen beendet `return` den Switch sofort:

```hemlock
fn get_day_name(day: i32): string {
    switch (day) {
        case 1:
            return "Montag";
        case 2:
            return "Dienstag";
        case 3:
            return "Mittwoch";
        default:
            return "Unbekannt";
    }
}
```

### Switch-Werttypen

Switch funktioniert mit jedem Werttyp:

```hemlock
// Ganzzahlen
switch (count) {
    case 0: print("null"); break;
    case 1: print("eins"); break;
}

// Strings
switch (name) {
    case "Alice": print("A"); break;
    case "Bob": print("B"); break;
}

// Booleans
switch (flag) {
    case true: print("an"); break;
    case false: print("aus"); break;
}
```

**Hinweis:** Faelle werden mittels Wertgleichheit verglichen.

## Break und Continue

### Break

Verlasst die innerste Schleife oder Switch:

```hemlock
// In Schleifen
let i = 0;
while (true) {
    if (i >= 10) {
        break;  // Schleife verlassen
    }
    print(i);
    i = i + 1;
}

// In Switch
switch (x) {
    case 1:
        print("eins");
        break;  // Switch verlassen
    case 2:
        print("zwei");
        break;
}
```

### Continue

Springt zur nächsten Iteration der Schleife:

```hemlock
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) {
        continue;  // Iteration überspringen wenn i 5 ist
    }
    print(i);  // Gibt aus: 0,1,2,3,4,6,7,8,9
}
```

**Unterschied:**
- `break` - Verlasst Schleife vollständig
- `continue` - Springt zur nächsten Iteration

## Schleifen-Labels

Schleifen-Labels erlauben `break` und `continue`, spezifische äußere Schleifen anzusprechen, statt nur die innerste Schleife. Dies ist nützlich für verschachtelte Schleifen, wo Sie eine äußere Schleife von einer inneren aus steuern müssen.

### Labeled Break

Eine äußere Schleife von einer inneren verlassen:

```hemlock
outer: while (i < 3) {
    let j = 0;
    while (j < 3) {
        if (i == 1 && j == 1) {
            break outer;  // Äußere while-Schleife verlassen
        }
        print(i * 10 + j);
        j = j + 1;
    }
    i = i + 1;
}
// Gibt aus: 0, 1, 2, 10 (stoppt bei i=1, j=1)
```

### Labeled Continue

Zur nächsten Iteration einer äußeren Schleife springen:

```hemlock
let i = 0;
outer: while (i < 3) {
    i = i + 1;
    let j = 0;
    while (j < 3) {
        j = j + 1;
        if (i == 2 && j == 1) {
            continue outer;  // Rest der inneren Schleife überspringen, äußere fortsetzen
        }
        print(i * 10 + j);
    }
}
// Wenn i=2, j=1: springt zur nächsten äußeren Iteration
```

### Labels mit For-Schleifen

Labels funktionieren mit allen Schleifentypen:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 3; y = y + 1) {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
    }
}
```

### Labels mit For-In-Schleifen

```hemlock
let arr1 = [1, 2, 3];
let arr2 = [10, 20, 30];

outer: for (let a in arr1) {
    for (let b in arr2) {
        if (a == 2 && b == 20) {
            break outer;
        }
        print(a * 100 + b);
    }
}
```

### Labels mit Loop-Schlüsselwort

```hemlock
let x = 0;
outer: loop {
    let y = 0;
    loop {
        if (x == 1 && y == 1) {
            break outer;
        }
        print(x * 10 + y);
        y = y + 1;
        if (y >= 3) { break; }
    }
    x = x + 1;
    if (x >= 3) { break; }
}
```

### Mehrere Labels

Sie können Labels auf verschiedenen Verschachtelungsebenen haben:

```hemlock
outer: for (let a = 0; a < 2; a = a + 1) {
    inner: for (let b = 0; b < 3; b = b + 1) {
        for (let c = 0; c < 3; c = c + 1) {
            if (c == 1) {
                continue inner;  // Zur nächsten Iteration der mittleren Schleife springen
            }
            if (a == 1 && b == 1) {
                break outer;      // Äußerste Schleife verlassen
            }
            print(a * 100 + b * 10 + c);
        }
    }
}
```

### Unlabeled Break/Continue mit gelabelten Schleifen

Unlabeled `break` und `continue` funktionieren weiterhin normal (betreffen die innerste Schleife), auch wenn äußere Schleifen Labels haben:

```hemlock
outer: for (let x = 0; x < 3; x = x + 1) {
    for (let y = 0; y < 5; y = y + 1) {
        if (y == 2) {
            break;  // Bricht nur innere Schleife ab
        }
        print(x * 10 + y);
    }
}
// Gibt aus: 0, 1, 10, 11, 20, 21
```

### Label-Syntax

- Labels sind Bezeichner gefolgt von einem Doppelpunkt
- Labels müssen direkt vor einer Schleifenanweisung stehen (`while`, `for`, `loop`)
- Label-Namen folgen Bezeichnerregeln (Buchstaben, Ziffern, Unterstriche)
- Gängige Konventionen: `outer`, `inner`, `row`, `col`, beschreibende Namen

## Defer-Anweisung

Die `defer`-Anweisung plant Code zur Ausführung, wenn die aktuelle Funktion zurückkehrt. Dies ist nützlich für Bereinigungsoperationen wie Dateien schließen, Ressourcen freigeben oder Sperren lösen.

### Einfaches Defer

```hemlock
fn example() {
    print("start");
    defer print("bereinigung");  // Wird ausgeführt, wenn Funktion zurückkehrt
    print("ende");
}

example();
// Ausgabe:
// start
// ende
// bereinigung
```

**Kernverhalten:**
- Deferred-Anweisungen werden **nach** Abschluss des Funktionskoerpers ausgeführt
- Deferred-Anweisungen werden **vor** der Rückkehr der Funktion an ihren Aufrufer ausgeführt
- Deferred-Anweisungen werden immer ausgeführt, auch wenn die Funktion eine Ausnahme wirft

### Mehrere Defers (LIFO-Reihenfolge)

Wenn mehrere `defer`-Anweisungen verwendet werden, werden sie in **umgekehrter Reihenfolge** ausgeführt (Last-In-First-Out):

```hemlock
fn example() {
    defer print("erstes");   // Wird zuletzt ausgeführt
    defer print("zweites");  // Wird als zweites ausgeführt
    defer print("drittes");  // Wird zuerst ausgeführt
    print("körper");
}

example();
// Ausgabe:
// körper
// drittes
// zweites
// erstes
```

Diese LIFO-Reihenfolge ist beabsichtigt - sie entspricht der natuerlichen Reihenfolge für verschachtelte Ressourcenbereinigung (innere Ressourcen vor äußeren schließen).

### Defer mit Return

Deferred-Anweisungen werden ausgeführt, bevor `return` die Kontrolle übergibt:

```hemlock
fn get_value(): i32 {
    defer print("bereinigung");
    print("vor return");
    return 42;
}

let result = get_value();
print("ergebnis:", result);
// Ausgabe:
// vor return
// bereinigung
// ergebnis: 42
```

### Defer mit Ausnahmen

Deferred-Anweisungen werden auch ausgeführt, wenn eine Ausnahme geworfen wird:

```hemlock
fn risky() {
    defer print("bereinigung 1");
    defer print("bereinigung 2");
    print("vor throw");
    throw "fehler!";
    print("nach throw");  // Wird nie erreicht
}

try {
    risky();
} catch (e) {
    print("Gefangen:", e);
}
// Ausgabe:
// vor throw
// bereinigung 2
// bereinigung 1
// Gefangen: fehler!
```

### Ressourcenbereinigungsmuster

Der Hauptanwendungsfall für `defer` ist sicherzustellen, dass Ressourcen bereinigt werden:

```hemlock
fn process_file(filename: string) {
    let file = open(filename, "r");
    defer file.close();  // Schliesst immer, auch bei Fehler

    let content = file.read();
    // ... Inhalt verarbeiten ...

    // Datei wird automatisch geschlossen, wenn Funktion zurückkehrt
}
```

**Ohne defer (fehleranfaellig):**
```hemlock
fn process_file_bad(filename: string) {
    let file = open(filename, "r");
    let content = file.read();
    // Wenn dies wirft, wird file.close() nie aufgerufen!
    process(content);
    file.close();
}
```

### Defer mit Closures

Defer kann Closures verwenden, um Zustand zu erfassen:

```hemlock
fn example() {
    let resource = acquire_resource();
    defer fn() {
        print("Ressource freigeben");
        release(resource);
    }();  // Hinweis: sofort aufgerufener Funktionsausdruck

    use_resource(resource);
}
```

### Wann Defer verwenden

**Defer verwenden für:**
- Dateien und Netzwerkverbindungen schließen
- Allokierten Speicher freigeben
- Sperren und Mutexe freigeben
- Bereinigung in jeder Funktion, die Ressourcen erwirbt

**Defer vs. Finally:**
- `defer` ist einfacher für Einzelressourcen-Bereinigung
- `try/finally` ist besser für komplexe Fehlerbehandlung mit Wiederherstellung

### Best Practices

1. **Defer sofort nach Ressourcenerwerb platzieren:**
   ```hemlock
   let file = open("data.txt", "r");
   defer file.close();
   // ... Datei verwenden ...
   ```

2. **Mehrere Defers für mehrere Ressourcen verwenden:**
   ```hemlock
   let file1 = open("input.txt", "r");
   defer file1.close();

   let file2 = open("output.txt", "w");
   defer file2.close();

   // Beide Dateien werden in umgekehrter Reihenfolge geschlossen
   ```

3. **LIFO-Reihenfolge für abhaengige Ressourcen beachten:**
   ```hemlock
   let outer = acquire_outer();
   defer release_outer(outer);

   let inner = acquire_inner(outer);
   defer release_inner(inner);

   // inner wird vor outer freigegeben (korrekte Abhaengigkeitsreihenfolge)
   ```

## Boolesche Operatoren

### Logisches UND (`&&`)

Beide Bedingungen müssen wahr sein:

```hemlock
if (x > 0 && x < 10) {
    print("einstellig positiv");
}
```

**Kurzschlussauswertung:**
```hemlock
if (false && expensive_check()) {
    // expensive_check() wird nie aufgerufen
}
```

### Logisches ODER (`||`)

Mindestens eine Bedingung muss wahr sein:

```hemlock
if (x < 0 || x > 100) {
    print("außerhalb des Bereichs");
}
```

**Kurzschlussauswertung:**
```hemlock
if (true || expensive_check()) {
    // expensive_check() wird nie aufgerufen
}
```

### Logisches NICHT (`!`)

Negiert booleschen Wert:

```hemlock
if (!is_valid) {
    print("ungültig");
}

if (!(x > 10)) {
    // Gleich wie: if (x <= 10)
}
```

## Vergleichsoperatoren

### Gleichheit

```hemlock
if (x == 10) { }    // Gleich
if (x != 10) { }    // Ungleich
```

Funktioniert mit allen Typen:
```hemlock
"hello" == "hello"  // true
true == false       // false
null == null        // true
```

### Relational

```hemlock
if (x < 10) { }     // Kleiner als
if (x > 10) { }     // Größer als
if (x <= 10) { }    // Kleiner oder gleich
if (x >= 10) { }    // Größer oder gleich
```

**Typpromotion gilt:**
```hemlock
let a: i32 = 10;
let b: i64 = 10;
if (a == b) { }     // true (i32 wird zu i64 befördert)
```

## Bitweise Operatoren

Hemlock bietet bitweise Operatoren für Ganzzahlmanipulation. Diese funktionieren **nur mit Ganzzahltypen** (i8-i64, u8-u64).

### Binäre bitweise Operatoren

**Bitweises UND (`&`)**
```hemlock
let a = 12;  // 1100 in binär
let b = 10;  // 1010 in binär
print(a & b);   // 8 (1000)
```

**Bitweises ODER (`|`)**
```hemlock
print(a | b);   // 14 (1110)
```

**Bitweises XOR (`^`)**
```hemlock
print(a ^ b);   // 6 (0110)
```

**Linksshift (`<<`)**
```hemlock
print(a << 2);  // 48 (110000) - 2 nach links schieben
```

**Rechtsshift (`>>`)**
```hemlock
print(a >> 1);  // 6 (110) - 1 nach rechts schieben
```

### Unaerer bitweiser Operator

**Bitweises NICHT (`~`)**
```hemlock
let a = 12;
print(~a);      // -13 (Zweierkomplement)

let c: u8 = 15;   // 00001111 in binär
print(~c);        // 240 (11110000) in u8
```

### Bitweise Beispiele

**Mit vorzeichenlosen Typen:**
```hemlock
let c: u8 = 15;   // 00001111 in binär
let d: u8 = 7;    // 00000111 in binär

print(c & d);     // 7  (00000111)
print(c | d);     // 15 (00001111)
print(c ^ d);     // 8  (00001000)
print(~c);        // 240 (11110000) - in u8
```

**Typerhaltung:**
```hemlock
// Bitweise Operationen erhalten den Typ der Operanden
let x: u8 = 255;
let result = ~x;  // result ist u8 mit Wert 0

let y: i32 = 100;
let result2 = y << 2;  // result2 ist i32 mit Wert 400
```

**Gängige Muster:**
```hemlock
// Prüfen, ob Bit gesetzt ist
if (flags & 0x04) {
    print("Bit 2 ist gesetzt");
}

// Bit setzen
flags = flags | 0x08;

// Bit löschen
flags = flags & ~0x02;

// Bit umschalten
flags = flags ^ 0x01;
```

### Operatorpraezedenz

Bitweise Operatoren folgen C-artiger Präzedenz:

1. `~` (unaeres NICHT) - hoechste, gleiche Ebene wie `!` und `-`
2. `<<`, `>>` (Shifts) - höher als Vergleiche, niedriger als `+`/`-`
3. `&` (bitweises UND) - höher als `^` und `|`
4. `^` (bitweises XOR) - zwischen `&` und `|`
5. `|` (bitweises ODER) - niedriger als `&` und `^`, höher als `&&`
6. `&&`, `||` (logisch) - niedrigste Präzedenz

**Beispiele:**
```hemlock
// & hat höhere Präzedenz als |
let result1 = 12 | 10 & 8;  // (10 & 8) | 12 = 8 | 12 = 12

// Shift hat höhere Präzedenz als bitweise Operatoren
let result2 = 8 | 1 << 2;   // 8 | (1 << 2) = 8 | 4 = 12

// Klammern für Klarheit verwenden
let result3 = (5 & 3) | (2 << 1);  // 1 | 4 = 5
```

**Wichtige Hinweise:**
- Bitweise Operatoren funktionieren nur mit Ganzzahltypen (nicht Floats, Strings, etc.)
- Typpromotion folgt Standardregeln (kleinere Typen werden zu groesseren befördert)
- Rechtsshift (`>>`) ist arithmetisch für vorzeichenbehaftete Typen, logisch für vorzeichenlose
- Shift-Betraege werden nicht bereichsgeprueft (Verhalten ist plattformabhaengig für große Shifts)

## Operatorpraezedenz (Vollständig)

Von hoechster zu niedrigster Präzedenz:

1. **Unaer**: `!`, `-`, `~`
2. **Multiplikativ**: `*`, `/`, `%`
3. **Additiv**: `+`, `-`
4. **Shift**: `<<`, `>>`
5. **Relational**: `<`, `>`, `<=`, `>=`
6. **Gleichheit**: `==`, `!=`
7. **Bitweises UND**: `&`
8. **Bitweises XOR**: `^`
9. **Bitweises ODER**: `|`
10. **Logisches UND**: `&&`
11. **Logisches ODER**: `||`

**Klammern für Klarheit verwenden:**
```hemlock
// Unklar
if (a || b && c) { }

// Klar
if (a || (b && c)) { }
if ((a || b) && c) { }
```

## Gängige Muster

### Muster: Eingabevalidierung

```hemlock
fn validate_age(age: i32): bool {
    if (age < 0 || age > 150) {
        return false;
    }
    return true;
}
```

### Muster: Bereichsprüfung

```hemlock
fn in_range(value: i32, min: i32, max: i32): bool {
    return value >= min && value <= max;
}

if (in_range(score, 0, 100)) {
    print("gueltige Punktzahl");
}
```

### Muster: Zustandsmaschine

```hemlock
let state = "start";

while (true) {
    switch (state) {
        case "start":
            print("Starte...");
            state = "running";
            break;

        case "running":
            if (should_pause) {
                state = "paused";
            } else if (should_stop) {
                state = "stopped";
            }
            break;

        case "paused":
            if (should_resume) {
                state = "running";
            }
            break;

        case "stopped":
            print("Gestoppt");
            break;
    }

    if (state == "stopped") {
        break;
    }
}
```

### Muster: Iteration mit Filterung

```hemlock
let arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Nur gerade Zahlen ausgeben
for (let i = 0; i < arr.length; i = i + 1) {
    if (arr[i] % 2 != 0) {
        continue;  // Ungerade Zahlen überspringen
    }
    print(arr[i]);
}
```

### Muster: Fruehes Beenden

```hemlock
fn find_first_negative(arr: array): i32 {
    for (let i = 0; i < arr.length; i = i + 1) {
        if (arr[i] < 0) {
            return i;  // Fruehes Beenden
        }
    }
    return -1;  // Nicht gefunden
}
```

## Best Practices

1. **Immer geschweifte Klammern verwenden** - Auch für einzeilige Blöcke (durch Syntax erzwungen)
2. **Explizite Bedingungen** - `x == 0` statt `!x` für Klarheit verwenden
3. **Tiefe Verschachtelung vermeiden** - Verschachtelte Bedingungen in Funktionen extrahieren
4. **Fruehe Returns verwenden** - Verschachtelung mit Guard-Klauseln reduzieren
5. **Komplexe Bedingungen aufteilen** - In benannte boolesche Variablen aufteilen
6. **Default in Switch** - Immer einen Default-Fall einschliessen
7. **Fall-Through kommentieren** - Beabsichtigtes Fall-Through explizit machen

## Häufige Fallstricke

### Fallstrick: Zuweisung in Bedingung

```hemlock
// Das ist NICHT erlaubt (keine Zuweisung in Bedingungen)
if (x = 10) { }  // FEHLER: Syntaxfehler

// Vergleich stattdessen verwenden
if (x == 10) { }  // OK
```

### Fallstrick: Fehlendes Break in Switch

```hemlock
// Unbeabsichtigtes Fall-Through
switch (x) {
    case 1:
        print("eins");
        // Fehlendes break - faellt durch!
    case 2:
        print("zwei");  // Wird für 1 und 2 ausgeführt
        break;
}

// Korrektur: Break hinzufügen
switch (x) {
    case 1:
        print("eins");
        break;  // Jetzt korrekt
    case 2:
        print("zwei");
        break;
}
```

### Fallstrick: Schleifenvariablen-Gültigkeitsbereich

```hemlock
// i ist auf die Schleife beschränkt
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
print(i);  // FEHLER: i ist hier nicht definiert
```

## Beispiele

### Beispiel: FizzBuzz

```hemlock
for (let i = 1; i <= 100; i = i + 1) {
    if (i % 15 == 0) {
        print("FizzBuzz");
    } else if (i % 3 == 0) {
        print("Fizz");
    } else if (i % 5 == 0) {
        print("Buzz");
    } else {
        print(i);
    }
}
```

### Beispiel: Primzahlpruefung

```hemlock
fn is_prime(n: i32): bool {
    if (n < 2) {
        return false;
    }

    let i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }

    return true;
}
```

### Beispiel: Menuesystem

```hemlock
fn menu() {
    while (true) {
        print("1. Start");
        print("2. Einstellungen");
        print("3. Beenden");

        let choice = get_input();

        switch (choice) {
            case 1:
                start_game();
                break;
            case 2:
                show_settings();
                break;
            case 3:
                print("Auf Wiedersehen!");
                return;
            default:
                print("Ungueltige Auswahl");
                break;
        }
    }
}
```

## Verwandte Themen

- [Functions](functions.md) - Kontrollfluss mit Funktionsaufrufen und Returns
- [Error Handling](error-handling.md) - Kontrollfluss mit Ausnahmen
- [Types](types.md) - Typkonvertierungen in Bedingungen

## Siehe auch

- **Syntax**: Siehe [Syntax](syntax.md) für Anweisungssyntax-Details
- **Operatoren**: Siehe [Types](types.md) für Typpromotion bei Operationen
