# Hemlock Sprachdesign-Philosophie

> "Eine kleine, unsichere Sprache, um unsichere Dinge sicher zu schreiben."

Dieses Dokument beschreibt die grundlegenden Designprinzipien und die Philosophie von Hemlock. Lesen Sie dies zuerst, bevor Sie Änderungen oder Ergänzungen an der Sprache vornehmen.

---

## Inhaltsverzeichnis

- [Kernidentität](#kernidentität)
- [Designprinzipien](#designprinzipien)
- [Philosophie zur Sicherheit](#philosophie-zur-sicherheit)
- [Was NICHT hinzugefügt werden sollte](#was-nicht-hinzugefügt-werden-sollte)
- [Zukünftige Überlegungen](#zukünftige-überlegungen)
- [Abschließende Gedanken](#abschließende-gedanken)

---

## Kernidentität

Hemlock ist eine **Systemskripting-Sprache**, die manuelle Speicherverwaltung und explizite Kontrolle umfasst. Sie ist für Programmierer konzipiert, die Folgendes wollen:

- Die Leistungsfähigkeit von C
- Die Ergonomie moderner Skriptsprachen
- Eingebaute strukturierte asynchrone Nebenläufigkeit
- Kein verstecktes Verhalten oder Magie

### Was Hemlock NICHT ist

- **Speichersicher** (baumelnde Zeiger sind Ihre Verantwortung)
- **Ein Ersatz für Rust, Go oder Lua**
- **Eine Sprache, die Komplexität vor Ihnen verbirgt**

### Was Hemlock IST

- **Explizit statt implizit, immer**
- **Lehrreich und experimentell**
- **Eine "C-Skriptschicht" für Systemarbeit**
- **Ehrlich über Kompromisse**

---

## Designprinzipien

### 1. Explizit statt implizit

Hemlock bevorzugt Explizitheit in allen Sprachkonstrukten. Es sollte keine Überraschungen, keine Magie und kein verstecktes Verhalten geben.

**Schlecht (implizit):**
```hemlock
let x = 5  // Fehlendes Semikolon - sollte einen Fehler erzeugen
```

**Gut (explizit):**
```hemlock
let x = 5;
free(ptr);  // Sie haben es allokiert, Sie geben es frei
```

**Schlüsselaspekte:**
- Semikolons sind obligatorisch (keine automatische Semikolon-Einfügung)
- Keine Garbage Collection
- Manuelle Speicherverwaltung (alloc/free)
- Typannotationen sind optional, werden aber zur Laufzeit geprüft
- Keine automatische Ressourcenbereinigung (kein RAII), aber `defer` bietet explizite Bereinigung

### 2. Dynamisch standardmäßig, typisiert nach Wahl

Jeder Wert hat ein Laufzeit-Typ-Tag, aber das System ist so konzipiert, dass es flexibel ist und dennoch Fehler erkennt.

**Typinferenz:**
- Kleine Ganzzahlen (passen in i32): `42` → `i32`
- Große Ganzzahlen (> i32-Bereich): `9223372036854775807` → `i64`
- Gleitkommazahlen: `3.14` → `f64`

**Explizite Typisierung bei Bedarf:**
```hemlock
let x = 42;              // i32 inferiert (kleiner Wert)
let y: u8 = 255;         // explizites u8
let z = x + y;           // wird zu i32 hochgestuft
let big = 5000000000;    // i64 inferiert (> i32 max)
```

**Typpromotionsregeln** folgen einer klaren Hierarchie vom kleinsten zum größten, wobei Gleitkommazahlen immer über Ganzzahlen gewinnen.

### 3. Unsicherheit ist ein Feature, kein Bug

Hemlock versucht nicht, alle Fehler zu verhindern. Stattdessen gibt es Ihnen die Werkzeuge, um sicher zu sein, während Sie bei Bedarf unsicheres Verhalten wählen können.

**Beispiele für beabsichtigte Unsicherheit:**
- Zeigerarithmetik kann überlaufen (Verantwortung des Benutzers)
- Keine Bereichsprüfung bei rohem `ptr` (verwenden Sie `buffer`, wenn Sie Sicherheit wollen)
- Double-free-Abstürze sind erlaubt (manuelle Speicherverwaltung)
- Das Typsystem verhindert Unfälle, erlaubt aber Risiken bei Bedarf

```hemlock
let p = alloc(10);
let q = p + 100;  // Weit über die Allokation hinaus - erlaubt, aber gefährlich
```

**Die Philosophie:** Das Typsystem sollte *Unfälle* verhindern, aber *beabsichtigte* unsichere Operationen erlauben.

### 4. Strukturierte Nebenläufigkeit erstklassig

Nebenläufigkeit ist in Hemlock kein nachträglicher Gedanke. Sie ist von Grund auf in die Sprache eingebaut.

**Schlüsselfunktionen:**
- `async`/`await` in die Sprache eingebaut
- Kanäle für Kommunikation
- `spawn`/`join`/`detach` für Aufgabenverwaltung
- Keine rohen Threads, keine Sperren - nur strukturiert
- Echte Mehrfaden-Parallelität mit POSIX-Threads

**Kein Event-Loop oder Green Threads** - Hemlock verwendet echte Betriebssystem-Threads für echte Parallelität über mehrere CPU-Kerne.

### 5. C-ähnliche Syntax, wenig Zeremonie

Hemlock sollte Systemprogrammierern vertraut vorkommen und gleichzeitig Boilerplate reduzieren.

**Designentscheidungen:**
- `{}`-Blöcke immer, keine optionalen Klammern
- Operatoren entsprechen C: `+`, `-`, `*`, `/`, `&&`, `||`, `!`
- Typsyntax entspricht Rust/TypeScript: `let x: type = value;`
- Funktionen sind erstklassige Werte
- Minimale Schlüsselwörter und Sonderformen

---

## Philosophie zur Sicherheit

**Hemlocks Haltung zur Sicherheit:**

> "Wir geben Ihnen die Werkzeuge, um sicher zu sein (`buffer`, Typannotationen, Bereichsprüfung), aber wir zwingen Sie nicht, sie zu verwenden (`ptr`, manuelle Speicherverwaltung, unsichere Operationen).
>
> Der Standard sollte zur Sicherheit führen, aber die Hintertür sollte immer verfügbar sein."

### Bereitgestellte Sicherheitswerkzeuge

**1. Sicherer Buffer-Typ:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // bereichsgeprüft
print(b.length);        // 64
free(b);                // immer noch manuell
```

**2. Unsichere rohe Zeiger:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Sie müssen daran denken, free aufzurufen
```

**3. Typannotationen:**
```hemlock
let x: u8 = 255;   // OK
let y: u8 = 256;   // FEHLER: außerhalb des Bereichs
```

**4. Laufzeit-Typprüfung:**
```hemlock
let val = some_function();
if (typeof(val) == "i32") {
    // Sicher als Ganzzahl zu verwenden
}
```

### Leitprinzipien

1. **Standard auf sichere Muster in der Dokumentation** - Zeigen Sie `buffer` vor `ptr`, ermutigen Sie zu Typannotationen
2. **Machen Sie unsichere Operationen offensichtlich** - Rohe Zeigerarithmetik sollte beabsichtigt aussehen
3. **Bieten Sie Hintertüren** - Verhindern Sie nicht, dass erfahrene Benutzer Low-Level-Arbeit leisten
4. **Seien Sie ehrlich über Kompromisse** - Dokumentieren Sie, was schiefgehen kann

### Beispiele für Sicherheit vs. Unsicherheit

| Sicheres Muster | Unsicheres Muster | Wann unsicher verwenden |
|-----------------|-------------------|-------------------------|
| `buffer`-Typ | `ptr`-Typ | FFI, leistungskritischer Code |
| Typannotationen | Keine Annotationen | Externe Schnittstellen, Validierung |
| Bereichsgeprüfter Zugriff | Zeigerarithmetik | Low-Level-Speicheroperationen |
| Ausnahmebehandlung | Rückgabe von null/Fehlercodes | Wenn Ausnahmen zu schwergewichtig sind |

---

## Was NICHT hinzugefügt werden sollte

Zu verstehen, was **nicht** hinzugefügt werden sollte, ist genauso wichtig wie zu wissen, was hinzugefügt werden soll.

### Kein implizites Verhalten hinzufügen

**Schlechte Beispiele:**

```hemlock
// SCHLECHT: Automatische Semikolon-Einfügung
let x = 5
let y = 10

// SCHLECHT: Implizite Typkonvertierungen, die Präzision verlieren
let x: i32 = 3.14  // Sollte abschneiden oder Fehler erzeugen?
```

**Warum:** Implizites Verhalten erzeugt Überraschungen und macht Code schwerer nachvollziehbar.

### Keine Komplexität verbergen

**Schlechte Beispiele:**

```hemlock
// SCHLECHT: Magische Hinter-den-Kulissen-Optimierung
let arr = [1, 2, 3]  // Ist das Stack oder Heap? Der Benutzer sollte es wissen! (Heap, refgezählt)

// SCHLECHT: Roher Zeiger automatisch freigegeben
let p = alloc(100)  // Wird das automatisch freigegeben? NEIN! Rohe Zeiger brauchen immer free()
```

**Hinweis zum Refcounting:** Hemlock verwendet internes Refcounting für Strings, Arrays, Objekte und Buffer - diese WERDEN automatisch freigegeben, wenn der Scope verlassen wird. Dies ist explizit und vorhersehbar (deterministische Bereinigung, wenn ref 0 erreicht, keine GC-Pausen). Rohe Zeiger (`ptr` von `alloc()`) sind NICHT refgezählt und erfordern immer manuelles `free()`.

**Warum:** Versteckte Komplexität macht es unmöglich, Leistung vorherzusagen und Probleme zu debuggen.

### Keine bestehenden Semantiken brechen

**Ändern Sie niemals diese Kernentscheidungen:**
- Semikolons sind obligatorisch - machen Sie sie nicht optional
- Manuelle Speicherverwaltung - fügen Sie keine GC hinzu
- Veränderbare Strings - machen Sie sie nicht unveränderbar
- Laufzeit-Typprüfung - entfernen Sie sie nicht

**Warum:** Konsistenz und Stabilität sind wichtiger als trendige Features.

### Keine "praktischen" Features hinzufügen, die Explizitheit reduzieren

**Beispiele für zu vermeidende Features:**
- Operatorüberladung (vielleicht für Benutzertypen, aber vorsichtig)
- Implizite Typumwandlung, die Informationen verliert
- Automatische Ressourcenbereinigung (RAII)
- Methodenverkettung, die Komplexität verbirgt
- DSLs und magische Syntax

**Ausnahme:** Praktische Features sind OK, wenn sie **expliziter Zucker** über einfache Operationen sind:
- `else if` ist in Ordnung (es sind nur verschachtelte if-Anweisungen)
- String-Interpolation könnte OK sein, wenn es klar syntaktischer Zucker ist
- Methodensyntax für Objekte ist in Ordnung (es ist explizit, was es tut)

---

## Zukünftige Überlegungen

### Vielleicht hinzufügen (in Diskussion)

Diese Features passen zur Philosophie von Hemlock, benötigen aber sorgfältiges Design:

**1. Pattern Matching**
```hemlock
match (value) {
    case i32: print("Ganzzahl");
    case string: print("Text");
    case _: print("anderes");
}
```
- Explizite Typprüfung
- Keine versteckten Kosten
- Kompilierzeit-Vollständigkeitsprüfung möglich

**2. Fehlertypen (`Result<T, E>`)**
```hemlock
fn divide(a: i32, b: i32): Result<i32, string> {
    if (b == 0) {
        return Err("Division durch Null");
    }
    return Ok(a / b);
}
```
- Explizite Fehlerbehandlung
- Zwingt Benutzer, über Fehler nachzudenken
- Alternative zu Ausnahmen

**3. Array/Slice-Typen**
- Haben bereits dynamische Arrays
- Könnten Arrays fester Größe für Stack-Allokation hinzufügen
- Müsste explizit über Stack vs. Heap sein

**4. Verbesserte Speichersicherheitswerkzeuge**
- Optionales Bereichsprüfungs-Flag
- Speicherleckerkennung in Debug-Builds
- Sanitizer-Integration

### Wahrscheinlich niemals hinzufügen

Diese Features verletzen Kernprinzipien:

**1. Garbage Collection**
- Verbirgt Speicherverwaltungskomplexität
- Unvorhersehbare Leistung
- Gegen das Prinzip der expliziten Kontrolle

**2. Automatische Speicherverwaltung**
- Gleiche Gründe wie GC
- Reference Counting könnte OK sein, wenn explizit

**3. Implizite Typkonvertierungen, die Daten verlieren**
- Widerspricht "explizit statt implizit"
- Quelle subtiler Bugs

**4. Makros (komplexe)**
- Zu viel Macht, zu viel Komplexität
- Einfaches Makrosystem könnte OK sein
- Bevorzugen Sie Codegenerierung oder Funktionen

**5. Klassenbasierte OOP mit Vererbung**
- Zu viel implizites Verhalten
- Duck Typing und Objekte sind ausreichend
- Komposition statt Vererbung

**6. Modulsystem mit komplexer Auflösung**
- Halten Sie Importe einfach und explizit
- Keine magischen Suchpfade
- Keine Versionsauflösung (verwenden Sie den OS-Paketmanager)

---

## Abschließende Gedanken

### Vertrauen und Verantwortung

Bei Hemlock geht es um **Vertrauen und Verantwortung**. Wir vertrauen dem Programmierer:

- Speicher korrekt zu verwalten
- Typen angemessen zu verwenden
- Fehler ordnungsgemäß zu behandeln
- Die Kompromisse zu verstehen

Im Gegenzug bietet Hemlock:

- Keine versteckten Kosten
- Kein überraschendes Verhalten
- Volle Kontrolle bei Bedarf
- Sicherheitswerkzeuge bei Wunsch

### Die Leitfrage

**Wenn Sie ein neues Feature in Betracht ziehen, fragen Sie:**

> "Gibt dies dem Programmierer mehr explizite Kontrolle, oder verbirgt es etwas?"

- Wenn es **explizite Kontrolle hinzufügt** → passt wahrscheinlich zu Hemlock
- Wenn es **Komplexität verbirgt** → gehört wahrscheinlich nicht dazu
- Wenn es **optionaler Zucker** ist, der klar dokumentiert ist → könnte OK sein

### Beispiele für gute Ergänzungen

- **Switch-Anweisungen** - Expliziter Kontrollfluss, keine Magie, klare Semantik

- **Async/await mit pthreads** - Explizite Nebenläufigkeit, echte Parallelität, Benutzer kontrolliert das Spawning

- **Buffer-Typ neben ptr** - Gibt Wahl zwischen sicher und unsicher

- **Optionale Typannotationen** - Hilft Bugs zu erkennen, ohne Striktheit zu erzwingen

- **Try/catch/finally** - Explizite Fehlerbehandlung mit klarem Kontrollfluss

### Beispiele für schlechte Ergänzungen

- **Automatische Semikolon-Einfügung** - Verbirgt Syntaxfehler, macht Code mehrdeutig

- **RAII/Destruktoren** - Automatische Bereinigung verbirgt, wann Ressourcen freigegeben werden

- **Implizite Null-Koaleszenz** - Verbirgt Null-Prüfungen, macht Code schwerer nachvollziehbar

- **Automatisch wachsende Strings** - Verbirgt Speicherallokation, unvorhersehbare Leistung

---

## Fazit

Hemlock versucht nicht, die sicherste Sprache, die schnellste Sprache oder die funktionsreichste Sprache zu sein.

**Hemlock versucht, die *ehrlichste* Sprache zu sein.**

Sie sagt Ihnen genau, was sie tut, gibt Ihnen Kontrolle, wenn Sie sie brauchen, und verbirgt die scharfen Kanten nicht. Es ist eine Sprache für Menschen, die ihren Code auf niedriger Ebene verstehen wollen, während sie moderne Ergonomie genießen.

Wenn Sie sich nicht sicher sind, ob ein Feature zu Hemlock gehört, denken Sie daran:

> **Explizit statt implizit, immer.**
> **Unsicherheit ist ein Feature, kein Bug.**
> **Der Benutzer ist verantwortlich, und das ist OK.**
