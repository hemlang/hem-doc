# Compiler-Optimierungen

Der Hemlock-Compiler (`hemlockc`) wendet mehrere Optimierungsdurchläufe bei der C-Code-Generierung an. Diese Optimierungen erfolgen automatisch und erfordern kein Eingreifen des Benutzers, aber ihr Verständnis hilft, Leistungscharakteristiken zu erklären.

---

## Überblick

```
Quelle (.hml)
    ↓
  Parse → AST
    ↓
  Typprüfung (optional)
    ↓
  AST-Optimierungsdurchlauf
    ↓
  C-Code-Generierung (mit Inlining + Unboxing)
    ↓
  GCC/Clang-Kompilierung
```

---

## Ausdrucks-Level-Unboxing

Hemlocks Laufzeit repräsentiert alle Werte als getaggte `HmlValue`-Strukturen. Im Interpreter boxed und unboxed jede arithmetische Operation Werte durch Laufzeit-Dispatch. Der Compiler eliminiert diesen Overhead für Ausdrücke mit bekannten primitiven Typen.

**Vorher (naive Codegen):**
```c
// x + 1 wobei x i32 ist
hml_i32_add(hml_val_i32(x), hml_val_i32(1))  // 2 Boxing-Aufrufe + Laufzeit-Dispatch
```

**Nachher (mit Ausdrucks-Unboxing):**
```c
// x + 1 wobei x i32 ist
hml_val_i32((x + 1))  // Pure C-Arithmetik, einmaliges Boxing am Ende
```

### Was unboxed wird

- Binäre Arithmetik: `+`, `-`, `*`, `%`
- Bitweise Operationen: `&`, `|`, `^`, `<<`, `>>`
- Vergleiche: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Unäre Operationen: `-`, `~`, `!`
- Typannotierte Variablen und Schleifenzähler

### Was auf HmlValue zurückfällt

- Funktionsaufrufe (Rückgabetyp kann dynamisch sein)
- Array-/Objektzugriffe (Elementtyp zur Kompilierzeit unbekannt)
- Variablen ohne Typannotationen und ohne inferierten Typ

### Tipp

Das Hinzufügen von Typannotationen zu Variablen in heißen Pfaden hilft dem Compiler beim Unboxing:

```hemlock
// Der Compiler kann diesen gesamten Ausdruck unboxen
fn dot(a: i32, b: i32, c: i32, d: i32): i32 {
    return a * c + b * d;
}
```

---

## Mehrstufiges Funktions-Inlining

Der Compiler inlined kleine Funktionen an Aufrufstellen und ersetzt Funktionsaufruf-Overhead durch direkten Code. Hemlock unterstützt mehrstufiges Inlining bis Tiefe 3, was bedeutet, dass verschachtelte Hilfsaufrufe ebenfalls inlined werden.

### Funktionsweise

```hemlock
fn rotr(x: u32, n: i32): u32 => (x >> n) | (x << (32 - n));

fn ep0(x: u32): u32 => rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);

fn sha256_round(a: u32, ...): u32 {
    let s0 = ep0(a);  // Sowohl ep0 ALS AUCH rotr werden hier inlined
    // ...
}
```

Auf Tiefe 1 wird `ep0()` in `sha256_round()` inlined. Auf Tiefe 2 werden die `rotr()`-Aufrufe innerhalb von `ep0()` ebenfalls inlined. Das Ergebnis ist ein einzelner Block nativer Arithmetik ohne Funktionsaufruf-Overhead.

### Inlining-Kriterien

Funktionen werden inlined wenn:
- Der Funktionskörper klein ist (einzelner Ausdruck oder wenige Anweisungen)
- Die Funktion nicht rekursiv ist
- Die aktuelle Inline-Tiefe kleiner als 3 ist

### Inlining mit Annotationen steuern

```hemlock
@inline
fn always_inline(x: i32): i32 => x * 2;

@noinline
fn never_inline(x: i32): i32 {
    // Komplexe Funktion, die nicht dupliziert werden sollte
    return x;
}
```

---

## While-Schleifen-Akkumulator-Unboxing

Für Top-Level-While-Schleifen erkennt der Compiler Zähler- und Akkumulatorvariablen und überschattet sie mit nativen C-Lokals, wodurch Boxing/Unboxing-Overhead bei jeder Iteration eliminiert wird.

### Was optimiert wird

```hemlock
let sum = 0;
let i = 0;
while (i < 1000000) {
    sum += i;
    i++;
}
print(sum);
```

Der Compiler erkennt, dass `sum` und `i` Integer-Akkumulatoren sind, die nur innerhalb der Schleife verwendet werden, und generiert native `int32_t`-Lokals anstelle von `HmlValue`-Operationen. Dies eliminiert Retain/Release-Overhead und Typ-Dispatch bei jeder Iteration.

### Leistungsauswirkung

Benchmark-Verbesserungen durch diese Optimierungen (gemessen an typischen Workloads):

| Benchmark | Vorher | Nachher | Verbesserung |
|-----------|--------|---------|--------------|
| primes_sieve | 10ms | 6ms | -40% |
| binary_tree | 11ms | 8ms | -27% |
| json_serialize | 8ms | 5ms | -37% |
| json_deserialize | 10ms | 7ms | -30% |
| fibonacci | 29ms | 24ms | -17% |
| array_sum | 41ms | 36ms | -12% |

---

## Hilfs-Annotationen

Der Compiler unterstützt 10 Optimierungs-Annotationen, die auf GCC/Clang-Attribute abgebildet werden:

| Annotation | Effekt |
|------------|--------|
| `@inline` | Funktions-Inlining fördern |
| `@noinline` | Funktions-Inlining verhindern |
| `@hot` | Als häufig ausgeführt markieren (Branch-Prediction) |
| `@cold` | Als selten ausgeführt markieren |
| `@pure` | Funktion hat keine Seiteneffekte (liest externen Zustand) |
| `@const` | Funktion hängt nur von Argumenten ab (kein externer Zustand) |
| `@flatten` | Alle Aufrufe innerhalb der Funktion inlinen |
| `@optimize(level)` | Pro-Funktion-Optimierungsstufe ("0"-"3", "s", "fast") |
| `@warn_unused` | Warnung wenn Rückgabewert ignoriert wird |
| `@section(name)` | Funktion in benutzerdefinierter ELF-Sektion platzieren |

### Beispiel

```hemlock
@hot @inline
fn fast_hash(key: string): u32 {
    // Hot-Path-Hash-Funktion
    let h: u32 = 5381;
    for (ch in key.chars()) {
        h = ((h << 5) + h) + ch;
    }
    return h;
}

@cold
fn handle_error(msg: string) {
    eprint("Error: " + msg);
    panic(msg);
}
```

---

## Allokationspools

Die Laufzeit verwendet vorallokierte Objekt-Pools, um `malloc`/`free`-Overhead für häufig erstellte kurzlebige Objekte zu vermeiden:

| Pool | Slots | Beschreibung |
|------|-------|--------------|
| Umgebungspool | 1024 | Closure/Funktions-Scope-Umgebungen (bis zu 16 Variablen jeweils) |
| Objektpool | 512 | Anonyme Objekte mit bis zu 8 Feldern |
| Funktionspool | 512 | Closure-Strukturen für erfasste Funktionen |

Pools verwenden Free-List-Stacks für O(1)-Allokation und -Deallokation. Wenn ein Pool erschöpft ist, fällt die Laufzeit auf `malloc` zurück. Objekte, die ihren Pool-Slot überschreiten (z.B. ein Objekt, das ein 9. Feld bekommt), werden transparent in Heap-Speicher migriert.

### AST-geborgte Parameter

Closures borgen Parametermetadaten direkt vom AST, anstatt sie tief zu kopieren, wodurch circa 6 `malloc` + N `strdup`-Aufrufe pro Closure-Erstellung eliminiert werden. Parameter-Name-Hashes werden lazily berechnet und auf dem AST-Knoten gecacht.

---

## Typprüfung

Der Compiler beinhaltet Kompilierzeit-Typprüfung (standardmäßig aktiviert):

```bash
hemlockc program.hml -o program       # Typprüfung + Kompilierung
hemlockc --check program.hml          # Nur Typprüfung
hemlockc --no-type-check program.hml  # Typprüfung überspringen
hemlockc --strict-types program.hml   # Bei impliziten 'any'-Typen warnen
```

Untypisierter Code wird als dynamisch (`any`-Typ) behandelt und besteht die Typprüfung immer. Typannotationen bieten Optimierungshinweise, die Unboxing ermöglichen.

---

## Siehe auch

- [Hilfs-Annotationen-Vorschlag](../proposals/compiler-helper-annotations.md) - Detaillierte Annotationsreferenz
- [Speicher-API](../reference/memory-api.md) - Buffer- und Pointer-Operationen
- [Funktionen](../language-guide/functions.md) - Typannotationen und Ausdruckskörper-Funktionen
