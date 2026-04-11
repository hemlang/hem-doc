# Compiler-Hilfsannotationen: Analyse und Vorschlag

**Autor:** Claude
**Datum:** 2026-01-08
**Status:** Teilweise implementiert (Phase 1-2 abgeschlossen in v1.9.0; Phase 3-5 bleiben Vorschläge)
**Bezug:** Issue #TBD

## Inhaltsverzeichnis

1. [Zusammenfassung](#zusammenfassung)
2. [Aktuelle Zustandsanalyse](#aktuelle-zustandsanalyse)
3. [Vorgeschlagene Annotationen](#vorgeschlagene-annotationen)
4. [Implementierungsplan](#implementierungsplan)
5. [Beispiele](#beispiele)
6. [Teststrategie](#teststrategie)
7. [Zukunftsüberlegungen](#zukunftsüberlegungen)

---

## Zusammenfassung

Hemlocks Annotationssystem bietet eine robuste Grundlage für die Hinzufügung von Compiler-Hinweisen und -Direktiven. Dieser Vorschlag erweitert die bestehende Annotationsinfrastruktur um **15 neue Compiler-Hilfsannotationen**, organisiert in fünf Kategorien:

- **Optimierungshinweise** (7 Annotationen)
- **Speicherverwaltung** (3 Annotationen)
- **Codegenerierungssteuerung** (2 Annotationen)
- **Fehlerprüfung** (2 Annotationen)
- **FFI/Interop** (1 Annotation)

Diese Annotationen ermöglichen es Entwicklern, dem Compiler (`hemlockc`) explizite Anweisungen zu geben, während die Abwärtskompatibilität mit dem Interpreter gewahrt bleibt.

---

## Aktuelle Zustandsanalyse

### 1. Annotationsinfrastruktur

Das Annotationssystem ist vollständig implementiert mit drei Hauptkomponenten:

**Parser** (`src/frontend/parser/statements.c`):
- Parst `@name` und `@name(args...)` Syntax
- Unterstützt positionelle und benannte Argumente
- Hängt Annotationen an Deklarationen an (let, const, define, enum)

**Validator** (`src/frontend/annotations.c`):
- Validiert Annotationsziele (Funktion, Typ, Variable, etc.)
- Prüft Argumentanzahl und -typen
- Warnt bei unbekannten oder doppelten Annotationen

**Resolver** (`src/frontend/resolver.c`):
- Speichert Annotationen neben Variablendefinitionen
- Ermöglicht Annotations-Lookup während der semantischen Analyse
- Ermöglicht `@deprecated`-Warnungen bei Variablennutzung

### 2. Aktuell implementierte Annotationen

```c
// Sicherheitsannotationen (für Tricycle-Speicherprüfer)
@safe       // Funktion ist speichersicher
@unsafe     // Funktion enthält unsichere Operationen
@trusted    // Funktion ist trotz unsicherer Operationen vertrauenswürdig

// Compiler-Optimierungshinweise (IMPLEMENTIERT in v1.9.0)
@inline     // Inlining dieser Funktion vorschlagen
@noinline   // Inlining dieser Funktion verhindern
@cold       // Funktion wird selten ausgeführt
@hot        // Funktion wird häufig ausgeführt
@pure       // Funktion hat keine Seiteneffekte

// Andere Annotationen
@deprecated      // Als veraltet markieren mit optionaler Nachricht
@test, @skip     // Test-Framework-Annotationen
@author, @since  // Dokumentationsannotationen
```

---

## Vorgeschlagene Annotationen

### Kategorie 1: Optimierungshinweise

#### `@unroll(count?: number)`
**Ziel:** Schleifen (for, while)
**Argumente:** Optionaler Entrollungsfaktor (Standard: Compiler entscheidet)

Schlägt Schleifenentrollung für leistungskritische enge Schleifen vor.

```hemlock
@unroll(4)
for (let i = 0; i < 1024; i++) {
    buffer[i] = buffer[i] * 2;
}
```

#### `@simd` / `@nosimd`
**Ziel:** Funktionen, Schleifen

SIMD-Vektorisierung aktivieren oder deaktivieren.

#### `@likely` / `@unlikely`
**Ziel:** If-Anweisungen, Bedingungen

Branch-Prediction-Hinweise für heiße Pfade.

#### `@const`
**Ziel:** Funktionen

Funktion gibt immer dasselbe Ergebnis für dieselben Eingaben zurück (stärker als `@pure`).

#### `@tail_call`
**Ziel:** Funktionsaufrufe

Fordert Tail-Call-Optimierung (TCO) an.

#### `@flatten`
**Ziel:** Funktionen

Alle Aufrufe innerhalb dieser Funktion inlinen.

#### `@optimize(level: string)`
**Ziel:** Funktionen
**Argumente:** Optimierungsstufe ("0", "1", "2", "3", "s", "fast")

Globale Optimierungsstufe für bestimmte Funktion überschreiben.

### Kategorie 2: Speicherverwaltung

#### `@stack`
Auf dem Stack statt auf dem Heap allokieren (wo möglich).

#### `@noalias`
Verspricht, dass der Pointer nicht mit anderen Pointern aliased.

#### `@aligned(bytes: number)`
Speicherausrichtungsanforderungen spezifizieren.

### Kategorie 3: Codegenerierungssteuerung

#### `@extern(name?: string, abi?: string)`
Funktion für externe Verlinkung oder FFI-Export markieren.

#### `@section(name: string)`
Symbol in bestimmter ELF/Mach-O-Sektion platzieren.

### Kategorie 4: Fehlerprüfung

#### `@bounds_check` / `@no_bounds_check`
Globale Grenzenprüfungsrichtlinie überschreiben.

#### `@warn_unused`
Warnung wenn Aufrufer den Rückgabewert ignoriert.

### Kategorie 5: FFI/Interop

#### `@packed`
Gepackte Struktur ohne Padding erstellen (für C-Interop).

---

## Vollständige Annotationsreferenz-Tabelle

| Annotation | Ziel | Args | Beschreibung | C-Attribut |
|------------|------|------|--------------|------------|
| `@inline` | fn | 0 | Inlining erzwingen | `always_inline` |
| `@noinline` | fn | 0 | Inlining verhindern | `noinline` |
| `@cold` | fn | 0 | Selten ausgeführt | `cold` |
| `@hot` | fn | 0 | Häufig ausgeführt | `hot` |
| `@pure` | fn | 0 | Keine Seiteneffekte, kann Globals lesen | `pure` |
| `@const` | fn | 0 | Keine Seiteneffekte, keine Globals-Lesezugriffe | `const` |
| `@flatten` | fn | 0 | Alle Aufrufe innerhalb der Funktion inlinen | `flatten` |
| `@tail_call` | fn | 0 | Tail-Call-Optimierung anfordern | Benutzerdefiniert |
| `@optimize(level)` | fn | 1 | Optimierungsstufe überschreiben | `optimize("OX")` |
| `@unroll(factor?)` | Schleife | 0-1 | Schleifenentrollungshinweis | `#pragma unroll` |
| `@simd` | fn, Schleife | 0 | SIMD-Vektorisierung aktivieren | `#pragma omp simd` |
| `@nosimd` | fn, Schleife | 0 | SIMD deaktivieren | Benutzerdefiniert |
| `@likely` | if | 0 | Branch wird wahrscheinlich genommen | `__builtin_expect` |
| `@unlikely` | if | 0 | Branch wird unwahrscheinlich genommen | `__builtin_expect` |
| `@stack` | let | 0 | Stack-Allokation | Benutzerdefiniert |
| `@noalias` | param | 0 | Kein Pointer-Aliasing | `noalias` |
| `@aligned(N)` | let, fn | 1 | Speicherausrichtung | `aligned(N)` |
| `@extern(name?, abi?)` | fn | 0-2 | Externe Verlinkung | `extern "C"` |
| `@section(name)` | fn, let | 1 | In bestimmter Sektion platzieren | `section("X")` |
| `@bounds_check` | fn | 0 | Grenzenprüfung erzwingen | Benutzerdefiniert |
| `@no_bounds_check` | fn | 0 | Grenzenprüfung deaktivieren | Benutzerdefiniert |
| `@warn_unused` | fn | 0 | Bei ungenutztem Rückgabewert warnen | `warn_unused_result` |
| `@packed` | define | 0 | Kein Struct-Padding | `packed` |
