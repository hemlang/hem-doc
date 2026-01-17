# Willkommen bei Hemlock

> "Eine kleine, unsichere Sprache zum sicheren Schreiben unsicherer Dinge."

**Hemlock** ist eine System-Skriptsprache, die die Leistungsfähigkeit von C mit modernen Skript-Annehmlichkeiten verbindet. Sie bietet manuelle Speicherverwaltung, explizite Kontrolle und eingebaute strukturierte asynchrone Nebenläufigkeit.

## Was ist Hemlock?

Hemlock ist für Programmierer konzipiert, die Folgendes wünschen:

- **Explizite Kontrolle** über Speicher und Ausführung
- **C-ähnliche Syntax** mit modernen Annehmlichkeiten
- **Kein verstecktes Verhalten** oder Magie
- **Echte parallele Asynchronität** mit pthread-basierter Nebenläufigkeit

Hemlock ist keine speichersichere Sprache mit Garbage Collection. Stattdessen gibt es Ihnen die Werkzeuge zur Sicherheit (`buffer`, Typ-Annotationen, Grenzprüfungen), zwingt Sie aber nicht, diese zu verwenden (`ptr`, manuelle Speicherverwaltung, unsichere Operationen).

## Schnelles Beispiel

```hemlock
// Hallo, Hemlock!
fn greet(name: string): string {
    return `Hallo, ${name}!`;
}

let message = greet("Welt");
print(message);

// Manuelle Speicherverwaltung
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Funktionen auf einen Blick

| Funktion | Beschreibung |
|----------|--------------|
| **Typsystem** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Speicher** | Manuelle Verwaltung mit `alloc()`, `buffer()`, `free()` |
| **Async** | Eingebautes `async`/`await` mit echter pthread-Parallelität |
| **FFI** | C-Funktionen direkt aus gemeinsam genutzten Bibliotheken aufrufen |
| **Standardbibliothek** | 40 Module einschließlich crypto, http, sqlite, json und mehr |

## Erste Schritte

Bereit loszulegen? So beginnen Sie:

1. **[Installation](#getting-started-installation)** - Hemlock herunterladen und einrichten
2. **[Schnellstart](#getting-started-quick-start)** - Schreiben Sie Ihr erstes Programm in Minuten
3. **[Tutorial](#getting-started-tutorial)** - Lernen Sie Hemlock Schritt für Schritt

## Dokumentationsabschnitte

- **Erste Schritte** - Installation, Schnellstartanleitung und Tutorials
- **Sprachhandbuch** - Tiefgehende Einblicke in Syntax, Typen, Funktionen und mehr
- **Fortgeschrittene Themen** - Asynchrone Programmierung, FFI, Signale und Atomics
- **API-Referenz** - Vollständige Referenz für eingebaute Funktionen und Standardbibliothek
- **Design & Philosophie** - Verstehen Sie, warum Hemlock so ist, wie es ist

## Paketmanager

Hemlock wird mit **hpm** geliefert, einem Paketmanager zur Verwaltung von Abhängigkeiten:

```bash
hpm init my-project
hpm add some-package
hpm run
```

Weitere Details finden Sie in den hpm-Dokumentationsabschnitten.

---

Verwenden Sie die Navigation auf der linken Seite, um die Dokumentation zu erkunden, oder nutzen Sie die Suchleiste, um bestimmte Themen zu finden.
