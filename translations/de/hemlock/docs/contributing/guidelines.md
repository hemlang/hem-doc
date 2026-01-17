# Beitragen zu Hemlock

Vielen Dank für Ihr Interesse, zu Hemlock beizutragen! Diese Anleitung hilft Ihnen zu verstehen, wie Sie effektiv beitragen können, während Sie die Designphilosophie und Codequalität der Sprache beibehalten.

---

## Inhaltsverzeichnis

- [Bevor Sie beginnen](#bevor-sie-beginnen)
- [Beitrags-Workflow](#beitrags-workflow)
- [Code-Stilrichtlinien](#code-stilrichtlinien)
- [Was Sie beitragen können](#was-sie-beitragen-können)
- [Was Sie NICHT beitragen sollten](#was-sie-nicht-beitragen-sollten)
- [Häufige Muster](#häufige-muster)
- [Neue Funktionen hinzufügen](#neue-funktionen-hinzufügen)
- [Code-Review-Prozess](#code-review-prozess)

---

## Bevor Sie beginnen

### Erforderliche Lektüre

Bevor Sie beitragen, lesen Sie bitte diese Dokumente in der angegebenen Reihenfolge:

1. **`/home/user/hemlock/docs/design/philosophy.md`** - Verstehen Sie Hemlocks Kernprinzipien
2. **`/home/user/hemlock/docs/design/implementation.md`** - Lernen Sie die Codebase-Struktur kennen
3. **`/home/user/hemlock/docs/contributing/testing.md`** - Verstehen Sie die Testanforderungen
4. **Dieses Dokument** - Lernen Sie die Beitragsrichtlinien kennen

### Voraussetzungen

**Erforderliches Wissen:**
- C-Programmierung (Zeiger, Speicherverwaltung, Strukturen)
- Compiler-/Interpreter-Grundlagen (Lexing, Parsing, AST)
- Git- und GitHub-Workflow
- Unix/Linux-Kommandozeile

**Erforderliche Werkzeuge:**
- GCC- oder Clang-Compiler
- Make-Build-System
- Git-Versionskontrolle
- Valgrind (zur Erkennung von Speicherlecks)
- Einfacher Texteditor oder IDE

### Kommunikationskanäle

**Wo Sie Fragen stellen können:**
- GitHub Issues - Fehlerberichte und Feature-Anfragen
- GitHub Discussions - Allgemeine Fragen und Design-Diskussionen
- Pull-Request-Kommentare - Spezifisches Code-Feedback

---

## Beitrags-Workflow

### 1. Ein Issue finden oder erstellen

**Bevor Sie Code schreiben:**
- Prüfen Sie, ob ein Issue für Ihren Beitrag existiert
- Falls nicht, erstellen Sie eines, das beschreibt, was Sie tun möchten
- Warten Sie auf Feedback der Maintainer, bevor Sie große Änderungen beginnen
- Kleine Fehlerbehebungen können diesen Schritt überspringen

**Gute Issue-Beschreibungen enthalten:**
- Problembeschreibung (was defekt ist oder fehlt)
- Vorgeschlagene Lösung (wie Sie es beheben möchten)
- Beispiele (Code-Snippets, die das Problem zeigen)
- Begründung (warum diese Änderung zu Hemlocks Philosophie passt)

### 2. Fork und Clone

```bash
# Forken Sie zuerst das Repository auf GitHub, dann:
git clone https://github.com/IHR_BENUTZERNAME/hemlock.git
cd hemlock
git checkout -b feature/ihr-feature-name
```

### 3. Ihre Änderungen vornehmen

Befolgen Sie diese Richtlinien:
- Schreiben Sie zuerst Tests (TDD-Ansatz)
- Implementieren Sie das Feature
- Stellen Sie sicher, dass alle Tests bestehen
- Prüfen Sie auf Speicherlecks
- Aktualisieren Sie die Dokumentation

### 4. Ihre Änderungen testen

```bash
# Führen Sie die vollständige Test-Suite aus
make test

# Führen Sie eine bestimmte Testkategorie aus
./tests/run_tests.sh tests/category/

# Prüfen Sie auf Speicherlecks
valgrind ./hemlock tests/your_test.hml

# Bauen und testen
make clean && make && make test
```

### 5. Ihre Änderungen committen

**Gute Commit-Nachrichten:**
```
Add bitwise operators for integer types

- Implement &, |, ^, <<, >>, ~ operators
- Add type checking to ensure integer-only operations
- Update operator precedence table
- Add comprehensive tests for all operators

Closes #42
```

**Commit-Nachrichten-Format:**
- Erste Zeile: Kurze Zusammenfassung (max. 50 Zeichen)
- Leerzeile
- Detaillierte Erklärung (Zeilenumbruch bei 72 Zeichen)
- Issue-Nummern referenzieren

### 6. Einen Pull Request einreichen

**Vor dem Einreichen:**
- Rebasen Sie auf den neuesten Main-Branch
- Stellen Sie sicher, dass alle Tests bestehen
- Führen Sie Valgrind aus, um auf Lecks zu prüfen
- Aktualisieren Sie CLAUDE.md, wenn Sie benutzersichtbare Features hinzufügen

**Die Pull-Request-Beschreibung sollte enthalten:**
- Welches Problem dies löst
- Wie es gelöst wird
- Breaking Changes (falls vorhanden)
- Beispiele für neue Syntax oder Verhaltensweisen
- Testabdeckungs-Zusammenfassung

---

## Code-Stilrichtlinien

### C-Code-Stil

**Formatierung:**
```c
// Mit 4 Leerzeichen einrücken (keine Tabs)
// K&R-Klammerstil für Funktionen
void function_name(int arg1, char *arg2)
{
    if (condition) {
        // Klammer auf derselben Zeile für Kontrollstrukturen
        do_something();
    }
}

// Zeilenlänge: maximal 100 Zeichen
// Leerzeichen um Operatoren verwenden
int result = (a + b) * c;

// Zeiger-Sternchen beim Typ
char *string;   // Gut
char* string;   // Vermeiden
char * string;  // Vermeiden
```

**Namenskonventionen:**
```c
// Funktionen: kleinbuchstaben_mit_unterstrichen
void eval_expression(ASTNode *node);

// Typen: PascalCase
typedef struct Value Value;
typedef enum ValueType ValueType;

// Konstanten: GROSSBUCHSTABEN_MIT_UNTERSTRICHEN
#define MAX_BUFFER_SIZE 4096

// Variablen: kleinbuchstaben_mit_unterstrichen
int item_count;
Value *current_value;

// Enums: TYP_PRAEFIX_NAME
typedef enum {
    TYPE_I32,
    TYPE_STRING,
    TYPE_OBJECT
} ValueType;
```

**Kommentare:**
```c
// Einzeilige Kommentare für kurze Erklärungen
// Vollständige Sätze mit korrekter Großschreibung verwenden

/*
 * Mehrzeilige Kommentare für längere Erklärungen
 * Sternchen für Lesbarkeit ausrichten
 */

/**
 * Funktionsdokumentations-Kommentar
 * @param node - AST-Knoten zur Auswertung
 * @return Ausgewerteter Wert
 */
Value eval_expr(ASTNode *node);
```

**Fehlerbehandlung:**
```c
// Alle malloc-Aufrufe prüfen
char *buffer = malloc(size);
if (!buffer) {
    fprintf(stderr, "Fehler: Speicher erschöpft\n");
    exit(1);
}

// Kontext in Fehlermeldungen bereitstellen
if (file == NULL) {
    fprintf(stderr, "Fehler: Konnte '%s' nicht öffnen: %s\n",
            filename, strerror(errno));
    exit(1);
}

// Aussagekräftige Fehlermeldungen verwenden
// Schlecht: "Fehler: Ungültiger Wert"
// Gut: "Fehler: Integer erwartet, String erhalten"
```

**Speicherverwaltung:**
```c
// Immer freigeben, was Sie allokieren
Value *val = value_create_i32(42);
// ... val verwenden
value_free(val);

// Zeiger nach dem Freigeben auf NULL setzen (verhindert Double-Free)
free(ptr);
ptr = NULL;

// Eigentümerschaft in Kommentaren dokumentieren
// Diese Funktion übernimmt das Eigentum von 'value' und wird es freigeben
void store_value(Value *value);

// Diese Funktion übernimmt NICHT das Eigentum (Aufrufer muss freigeben)
Value *get_value(void);
```

### Code-Organisation

**Dateistruktur:**
```c
// 1. Includes (System-Header zuerst, dann lokale)
#include <stdio.h>
#include <stdlib.h>
#include "internal.h"
#include "values.h"

// 2. Konstanten und Makros
#define INITIAL_CAPACITY 16

// 3. Typdefinitionen
typedef struct Foo Foo;

// 4. Statische Funktionsdeklarationen (interne Hilfsfunktionen)
static void helper_function(void);

// 5. Öffentliche Funktionsimplementierungen
void public_api_function(void)
{
    // Implementierung
}

// 6. Statische Funktionsimplementierungen
static void helper_function(void)
{
    // Implementierung
}
```

**Header-Dateien:**
```c
// Header-Guards verwenden
#ifndef HEMLOCK_MODULE_H
#define HEMLOCK_MODULE_H

// Forward-Deklarationen
typedef struct Value Value;

// Nur öffentliche API in Headern
void public_function(Value *val);

// Parameter und Rückgabewerte dokumentieren
/**
 * Wertet einen Ausdrucks-AST-Knoten aus
 * @param node - Der auszuwertende AST-Knoten
 * @param env - Die aktuelle Umgebung
 * @return Der Ergebniswert
 */
Value *eval_expr(ASTNode *node, Environment *env);

#endif // HEMLOCK_MODULE_H
```

---

## Was Sie beitragen können

### Erwünschte Beiträge

**Fehlerbehebungen:**
- Speicherlecks
- Segmentation Faults
- Fehlerhaftes Verhalten
- Verbesserungen von Fehlermeldungen

**Dokumentation:**
- Code-Kommentare
- API-Dokumentation
- Benutzerhandbücher und Tutorials
- Beispielprogramme
- Testfall-Dokumentation

**Tests:**
- Zusätzliche Testfälle für bestehende Features
- Abdeckung von Randfällen
- Regressionstests für behobene Fehler
- Performance-Benchmarks

**Kleine Feature-Ergänzungen:**
- Neue eingebaute Funktionen (wenn sie zur Philosophie passen)
- String-/Array-Methoden
- Hilfsfunktionen
- Verbesserungen der Fehlerbehandlung

**Performance-Verbesserungen:**
- Schnellere Algorithmen (ohne Änderung der Semantik)
- Reduzierung des Speicherverbrauchs
- Benchmark-Suite
- Profiling-Werkzeuge

**Tooling:**
- Editor-Syntaxhervorhebung
- Language Server Protocol (LSP)
- Debugger-Integration
- Build-System-Verbesserungen

### Erst diskutieren

**Größere Features:**
- Neue Sprachkonstrukte
- Typsystem-Änderungen
- Syntax-Ergänzungen
- Nebenläufigkeits-Primitive

**Wie diskutieren:**
1. Eröffnen Sie ein GitHub-Issue oder eine Diskussion
2. Beschreiben Sie das Feature und die Begründung
3. Zeigen Sie Beispielcode
4. Erklären Sie, wie es zu Hemlocks Philosophie passt
5. Warten Sie auf Feedback der Maintainer
6. Iterieren Sie am Design vor der Implementierung

---

## Was Sie NICHT beitragen sollten

### Unerwünschte Beiträge

**Fügen Sie keine Features hinzu, die:**
- Komplexität vor dem Benutzer verstecken
- Verhalten implizit oder magisch machen
- Bestehende Semantik oder Syntax brechen
- Garbage Collection oder automatische Speicherverwaltung hinzufügen
- Das Prinzip "explizit vor implizit" verletzen

**Beispiele für abgelehnte Beiträge:**

**1. Automatisches Einfügen von Semikolons**
```hemlock
// SCHLECHT: Dies würde abgelehnt werden
let x = 5  // Kein Semikolon
let y = 10 // Kein Semikolon
```
Warum: Macht Syntax mehrdeutig, versteckt Fehler

**2. RAII/Destruktoren**
```hemlock
// SCHLECHT: Dies würde abgelehnt werden
let f = open("file.txt");
// Datei wird automatisch am Ende des Scopes geschlossen
```
Warum: Versteckt, wann Ressourcen freigegeben werden, nicht explizit

**3. Implizite Typkonvertierung mit Datenverlust**
```hemlock
// SCHLECHT: Dies würde abgelehnt werden
let x: i32 = 3.14;  // Schneidet stillschweigend auf 3 ab
```
Warum: Datenverlust sollte explizit sein, nicht stillschweigend

**4. Garbage Collection**
```c
// SCHLECHT: Dies würde abgelehnt werden
void *gc_malloc(size_t size) {
    // Allokation für automatische Bereinigung verfolgen
}
```
Warum: Versteckt Speicherverwaltung, unvorhersehbare Performance

**5. Komplexes Makrosystem**
```hemlock
// SCHLECHT: Dies würde abgelehnt werden
macro repeat($n, $block) {
    for (let i = 0; i < $n; i++) $block
}
```
Warum: Zu viel Magie, macht Code schwer nachvollziehbar

### Häufige Ablehnungsgründe

**"Das ist zu implizit"**
- Lösung: Machen Sie das Verhalten explizit und dokumentieren Sie es

**"Das versteckt Komplexität"**
- Lösung: Legen Sie die Komplexität offen, aber machen Sie sie ergonomisch

**"Das bricht bestehenden Code"**
- Lösung: Finden Sie eine nicht-brechende Alternative oder diskutieren Sie Versionierung

**"Das passt nicht zu Hemlocks Philosophie"**
- Lösung: Lesen Sie philosophy.md erneut und überdenken Sie den Ansatz

---

## Häufige Muster

### Fehlerbehandlungsmuster

```c
// Verwenden Sie dieses Muster für behebbare Fehler im Hemlock-Code
Value *divide(Value *a, Value *b)
{
    // Vorbedingungen prüfen
    if (b->type != TYPE_I32) {
        // Fehlerwert zurückgeben oder Exception werfen
        return create_error("Integer-Divisor erwartet");
    }

    if (b->i32_value == 0) {
        return create_error("Division durch Null");
    }

    // Operation ausführen
    return value_create_i32(a->i32_value / b->i32_value);
}
```

### Speicherverwaltungsmuster

```c
// Muster: Allokieren, verwenden, freigeben
void process_data(void)
{
    // Allokieren
    Buffer *buf = create_buffer(1024);
    char *str = malloc(256);

    // Verwenden
    if (buf && str) {
        // ... Arbeit erledigen
    }

    // Freigeben (in umgekehrter Reihenfolge der Allokation)
    free(str);
    free_buffer(buf);
}
```

### Wert-Erstellungsmuster

```c
// Werte mit Konstruktoren erstellen
Value *create_integer(int32_t n)
{
    Value *val = malloc(sizeof(Value));
    if (!val) {
        fprintf(stderr, "Speicher erschöpft\n");
        exit(1);
    }

    val->type = TYPE_I32;
    val->i32_value = n;
    return val;
}
```

### Typprüfungsmuster

```c
// Typen vor Operationen prüfen
Value *add_values(Value *a, Value *b)
{
    // Typprüfung
    if (a->type != TYPE_I32 || b->type != TYPE_I32) {
        return create_error("Typkonflikt");
    }

    // Sicher fortzufahren
    return value_create_i32(a->i32_value + b->i32_value);
}
```

### String-Aufbaumuster

```c
// Strings effizient aufbauen
void build_error_message(char *buffer, size_t size, const char *detail)
{
    snprintf(buffer, size, "Fehler: %s (Zeile %d)", detail, line_number);
}
```

---

## Neue Funktionen hinzufügen

### Checkliste für Feature-Ergänzungen

Beim Hinzufügen eines neuen Features befolgen Sie diese Schritte:

#### 1. Design-Phase

- [ ] Lesen Sie philosophy.md, um die Ausrichtung sicherzustellen
- [ ] Erstellen Sie ein GitHub-Issue, das das Feature beschreibt
- [ ] Holen Sie Maintainer-Genehmigung für das Design ein
- [ ] Schreiben Sie eine Spezifikation (Syntax, Semantik, Beispiele)
- [ ] Berücksichtigen Sie Randfälle und Fehlerbedingungen

#### 2. Implementierungsphase

**Wenn Sie ein Sprachkonstrukt hinzufügen:**

- [ ] Fügen Sie Token-Typ zu `lexer.h` hinzu (falls nötig)
- [ ] Fügen Sie Lexer-Regel in `lexer.c` hinzu (falls nötig)
- [ ] Fügen Sie AST-Knotentyp in `ast.h` hinzu
- [ ] Fügen Sie AST-Konstruktor in `ast.c` hinzu
- [ ] Fügen Sie Parser-Regel in `parser.c` hinzu
- [ ] Fügen Sie Laufzeitverhalten in `runtime.c` oder dem entsprechenden Modul hinzu
- [ ] Behandeln Sie Aufräumen in AST-Free-Funktionen

**Wenn Sie eine eingebaute Funktion hinzufügen:**

- [ ] Fügen Sie Funktionsimplementierung in `builtins.c` hinzu
- [ ] Registrieren Sie die Funktion in `register_builtins()`
- [ ] Behandeln Sie alle Parameter-Typ-Kombinationen
- [ ] Geben Sie entsprechende Fehlerwerte zurück
- [ ] Dokumentieren Sie Parameter und Rückgabetyp

**Wenn Sie einen Werttyp hinzufügen:**

- [ ] Fügen Sie Typ-Enum in `values.h` hinzu
- [ ] Fügen Sie Feld zur Value-Union hinzu
- [ ] Fügen Sie Konstruktor in `values.c` hinzu
- [ ] Fügen Sie zu `value_free()` für Aufräumen hinzu
- [ ] Fügen Sie zu `value_copy()` für Kopieren hinzu
- [ ] Fügen Sie zu `value_to_string()` für Ausgabe hinzu
- [ ] Fügen Sie Typ-Promotion-Regeln hinzu, falls numerisch

#### 3. Testphase

- [ ] Schreiben Sie Testfälle (siehe testing.md)
- [ ] Testen Sie Erfolgsfälle
- [ ] Testen Sie Fehlerfälle
- [ ] Testen Sie Randfälle
- [ ] Führen Sie die vollständige Test-Suite aus (`make test`)
- [ ] Prüfen Sie auf Speicherlecks mit Valgrind
- [ ] Testen Sie auf mehreren Plattformen (wenn möglich)

#### 4. Dokumentationsphase

- [ ] Aktualisieren Sie CLAUDE.md mit benutzersichtbarer Dokumentation
- [ ] Fügen Sie Code-Kommentare hinzu, die die Implementierung erklären
- [ ] Erstellen Sie Beispiele in `examples/`
- [ ] Aktualisieren Sie relevante docs/-Dateien
- [ ] Dokumentieren Sie alle Breaking Changes

#### 5. Einreichungsphase

- [ ] Bereinigen Sie Debug-Code und Kommentare
- [ ] Überprüfen Sie die Einhaltung des Code-Stils
- [ ] Rebasen Sie auf den neuesten Main-Branch
- [ ] Erstellen Sie einen Pull Request mit detaillierter Beschreibung
- [ ] Reagieren Sie auf Code-Review-Feedback

### Beispiel: Einen neuen Operator hinzufügen

Lassen Sie uns das Hinzufügen des Modulo-Operators `%` als Beispiel durchgehen:

**1. Lexer (lexer.c):**
```c
// Zur Switch-Anweisung in get_next_token() hinzufügen
case '%':
    return create_token(TOKEN_PERCENT, "%", line);
```

**2. Lexer-Header (lexer.h):**
```c
typedef enum {
    // ... bestehende Token
    TOKEN_PERCENT,
    // ...
} TokenType;
```

**3. AST (ast.h):**
```c
typedef enum {
    // ... bestehende Operatoren
    OP_MOD,
    // ...
} BinaryOp;
```

**4. Parser (parser.c):**
```c
// Zu parse_multiplicative() oder entsprechender Präzedenzebene hinzufügen
if (match(TOKEN_PERCENT)) {
    BinaryOp op = OP_MOD;
    ASTNode *right = parse_unary();
    left = create_binary_op_node(op, left, right);
}
```

**5. Laufzeit (runtime.c):**
```c
// Zu eval_binary_op() hinzufügen
case OP_MOD:
    // Typprüfung
    if (left->type == TYPE_I32 && right->type == TYPE_I32) {
        if (right->i32_value == 0) {
            fprintf(stderr, "Fehler: Modulo durch Null\n");
            exit(1);
        }
        return value_create_i32(left->i32_value % right->i32_value);
    }
    // ... andere Typkombinationen behandeln
    break;
```

**6. Tests (tests/operators/modulo.hml):**
```hemlock
// Grundlegendes Modulo
print(10 % 3);  // Erwartet: 2

// Negatives Modulo
print(-10 % 3); // Erwartet: -1

// Fehlerfall (sollte fehlschlagen)
// print(10 % 0);  // Division durch Null
```

**7. Dokumentation (CLAUDE.md):**
```markdown
### Arithmetische Operatoren
- `+` - Addition
- `-` - Subtraktion
- `*` - Multiplikation
- `/` - Division
- `%` - Modulo (Rest)
```

---

## Code-Review-Prozess

### Worauf Reviewer achten

**1. Korrektheit**
- Macht der Code, was er behauptet?
- Werden Randfälle behandelt?
- Gibt es Speicherlecks?
- Werden Fehler richtig behandelt?

**2. Philosophie-Ausrichtung**
- Passt dies zu Hemlocks Designprinzipien?
- Ist es explizit oder implizit?
- Versteckt es Komplexität?

**3. Code-Qualität**
- Ist der Code lesbar und wartbar?
- Sind Variablennamen aussagekräftig?
- Haben Funktionen eine angemessene Größe?
- Gibt es ausreichende Dokumentation?

**4. Tests**
- Gibt es ausreichende Testfälle?
- Decken Tests Erfolgs- und Fehlerpfade ab?
- Werden Randfälle getestet?

**5. Dokumentation**
- Ist die benutzersichtbare Dokumentation aktualisiert?
- Sind Code-Kommentare klar?
- Werden Beispiele bereitgestellt?

### Auf Feedback reagieren

**Tun Sie:**
- Danken Sie Reviewern für ihre Zeit
- Stellen Sie klärende Fragen, wenn Sie etwas nicht verstehen
- Erklären Sie Ihre Begründung, wenn Sie anderer Meinung sind
- Nehmen Sie angeforderte Änderungen zeitnah vor
- Aktualisieren Sie die PR-Beschreibung, wenn sich der Umfang ändert

**Tun Sie nicht:**
- Kritik persönlich nehmen
- Defensiv argumentieren
- Feedback ignorieren
- Force-Push über Review-Kommentare (außer beim Rebasen)
- Nicht zusammenhängende Änderungen zum PR hinzufügen

### Ihren PR gemergt bekommen

**Anforderungen für Merge:**
- [ ] Alle Tests bestehen
- [ ] Keine Speicherlecks (Valgrind-sauber)
- [ ] Code-Review-Genehmigung vom Maintainer
- [ ] Dokumentation aktualisiert
- [ ] Befolgt Code-Stilrichtlinien
- [ ] Passt zu Hemlocks Philosophie

**Zeitrahmen:**
- Kleine PRs (Fehlerbehebungen): Normalerweise innerhalb weniger Tage geprüft
- Mittlere PRs (neue Features): Kann 1-2 Wochen dauern
- Große PRs (größere Änderungen): Erfordert ausführliche Diskussion

---

## Zusätzliche Ressourcen

### Lernressourcen

**Interpreter verstehen:**
- "Crafting Interpreters" von Robert Nystrom
- "Writing An Interpreter In Go" von Thorsten Ball
- "Modern Compiler Implementation in C" von Andrew Appel

**C-Programmierung:**
- "The C Programming Language" von K&R
- "Expert C Programming" von Peter van der Linden
- "C Interfaces and Implementations" von David Hanson

**Speicherverwaltung:**
- Valgrind-Dokumentation
- "Understanding and Using C Pointers" von Richard Reese

### Nützliche Befehle

```bash
# Mit Debug-Symbolen bauen
make clean && make CFLAGS="-g -O0"

# Mit Valgrind ausführen
valgrind --leak-check=full ./hemlock script.hml

# Bestimmte Testkategorie ausführen
./tests/run_tests.sh tests/strings/

# Tags-Datei für Code-Navigation generieren
ctags -R .

# Alle TODOs und FIXMEs finden
grep -rn "TODO\|FIXME" src/ include/
```

---

## Fragen?

Wenn Sie Fragen zum Beitragen haben:

1. Prüfen Sie die Dokumentation in `docs/`
2. Suchen Sie in bestehenden GitHub-Issues
3. Fragen Sie in GitHub Discussions
4. Eröffnen Sie ein neues Issue mit Ihrer Frage

**Vielen Dank für Ihren Beitrag zu Hemlock!**
