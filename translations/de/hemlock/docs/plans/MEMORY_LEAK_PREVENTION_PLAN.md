# Speicherleck-Präventionsplan

> Sicherstellung, dass die Hemlock-Laufzeit frei von Speicherlecks ist und ihren Vertrag mit dem Programmierer einhält.

**Datum:** 2026-01-16
**Status:** Abgeschlossen (implementiert in v1.8.3)
**Version:** 1.0

---

## Zusammenfassung

Hemlocks Designphilosophie besagt: *"Wir geben dir die Werkzeuge, um sicher zu sein, aber wir zwingen dich nicht, sie zu verwenden."* Das bedeutet, die **Laufzeit selbst** muss leckfrei sein, auch wenn Benutzercode unsichere Features verwendet. Der Programmierer-Vertrag lautet:

1. **Benutzer-Allokationen** (`alloc`, `buffer`) liegen in der Verantwortung des Programmierers zum `free`-Aufrufen
2. **Laufzeit-interne Allokationen** (Strings, Arrays, Objekte, Closures) werden automatisch per Referenzzählung verwaltet
3. **Fehler und Ausnahmen** dürfen keinen Speicher leaken
4. **Async-Tasks** haben klare Eigentumssemantik
5. **Die Laufzeit verbirgt keine Allokationen** vor dem Programmierer

Dieser Plan identifiziert Lücken in der aktuellen Infrastruktur und schlägt systematische Verbesserungen vor.

---

## Inhaltsverzeichnis

1. [Aktuelle Zustandsbewertung](#aktuelle-zustandsbewertung)
2. [Identifizierte Lücken](#identifizierte-lücken)
3. [Vorgeschlagene Verbesserungen](#vorgeschlagene-verbesserungen)
4. [Teststrategie](#teststrategie)
5. [Dokumentationsanforderungen](#dokumentationsanforderungen)
6. [Implementierungsphasen](#implementierungsphasen)
7. [Erfolgskriterien](#erfolgskriterien)

---

## Aktuelle Zustandsbewertung

### Stärken

| Komponente | Implementierung | Speicherort |
|------------|----------------|-------------|
| Referenzzählung | Atomare Operationen mit `__ATOMIC_SEQ_CST` | `src/backends/interpreter/values.c:413-550` |
| Zyklenerkennung | VisitedSet für Graph-Traversierung | `src/backends/interpreter/values.c:1345-1480` |
| Thread-Isolation | Tiefe Kopie bei Spawn | `src/backends/interpreter/values.c:1687-1859` |
| Profiler mit Leck-Erkennung | AllocSite-Tracking | `src/backends/interpreter/profiler/` |
| ASAN-Integration | CI-Pipeline mit Leck-Erkennung | `.github/workflows/tests.yml` |
| Valgrind-Unterstützung | Mehrere Makefile-Targets | `Makefile:189-327` |
| Umfassendes Testskript | Kategorie-basiertes Testen | `tests/leak_check.sh` |

### Aktuelles Speicher-Eigentumsmodell

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROGRAMMIERER-VERANTWORTUNG                    │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  ptr-Arithmetik ──────────────────────────────►  Grenzsicherheit│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    LAUFZEIT-VERANTWORTUNG                        │
├─────────────────────────────────────────────────────────────────┤
│  String-Literale/-Operationen ────────► refcount + auto-release │
│  Array-Literale/-Operationen ─────────► refcount + auto-release │
│  Objekt-Literale/-Operationen ────────► refcount + auto-release │
│  Funktions-Closures ─────────────────► refcount + env-Release   │
│  Task-Ergebnisse ────────────────────► freigegeben nach join()  │
│  Kanal-Puffer ───────────────────────► freigegeben bei close()  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Identifizierte Lücken

### Lücke 1: Fehlerpfad-Bereinigung (HOHE PRIORITÄT)

**Problem:** Wenn Ausnahmen mitten in der Ausführung auftreten, können allokierte Temporäre leaken.

**Beispielszenario:**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // Array allokiert
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // Ausnahme geworfen
        return x * 2;
    });
    // 'transformed' teilweise allokiert, 'arr' wird möglicherweise nicht freigegeben
}
```

**Aktueller Zustand:** Die Ausnahmebehandlung des Interpreters wickelt den Aufrufstapel ab, gibt aber möglicherweise nicht alle während der Ausdrucksauswertung erstellten Temporäre frei.

**Betroffene Dateien:**
- `src/backends/interpreter/runtime/evaluator.c` (Ausdrucksauswertung)
- `src/backends/interpreter/runtime/context.c` (Ausnahmebehandlung)

### Lücke 2: Eigentum an abgelösten Task-Ergebnissen (MITTLERE PRIORITÄT)

**Problem:** `detach(task)` erlaubt Fire-and-Forget-Ausführung, aber das Ergebnis des Tasks wird möglicherweise nie eingesammelt.

**Aktuelles Verhalten:**
```hemlock
let task = spawn(compute_something);
detach(task);  // Task läuft im Hintergrund
// Was passiert mit dem Rückgabewert wenn der Task abgeschlossen ist?
```

**Betroffene Dateien:**
- `src/backends/interpreter/builtins/concurrency.c:148-165` (Task-Abschluss)
- `src/backends/interpreter/values.c:745-780` (task_free)

### Lücke 3: Kanal-Schließen vs. Drain-Semantik (MITTLERE PRIORITÄT)

**Problem:** Wenn ein Kanal mit verbleibenden gepufferten Werten geschlossen wird, werden diese Werte ordnungsgemäß freigegeben?

**Szenario:**
```hemlock
let ch = channel(10);
ch.send("a");
ch.send("b");
ch.close();  // Werden "a" und "b" freigegeben?
```

**Betroffene Dateien:**
- `src/backends/interpreter/values.c:850-915` (channel_close, channel_free)

### Lücke 4: Null-Koaleszenz-AST-Leck (BEHOBEN)

**Problem:** Der Optimizer optimierte Null-Koaleszenz-Ausdrücke weg, wenn das Ergebnis zur Kompilierzeit bekannt war, gab aber die verworfenen AST-Knoten nicht frei.

**Ursache:** In `optimizer.c`, wenn `??` optimiert wurde (z.B. `"value" ?? "default"` → `"value"`), gab der Optimizer das behaltene Kind zurück, ohne den Eltern-`EXPR_NULL_COALESCE`-Knoten oder das verworfene Kind freizugeben.

**Lösung:** Ordnungsgemäße Bereinigung im Optimizer hinzugefügt, um verworfene Knoten freizugeben:
- Ergebnis-Kind speichern
- Ungenutztes Kind mit `expr_free()` freigeben
- Elternknotenstruktur freigeben
- Gespeichertes Ergebnis zurückgeben

**Modifizierte Dateien:**
- `src/frontend/optimizer/optimizer.c` (Null-Koaleszenz-Optimierungsbereinigung)

### Lücke 5: Closure-Erfassungslisten-Granularität (NIEDRIGE PRIORITÄT)

**Problem:** Closures erfassen die gesamte Umgebungskette statt nur referenzierter Variablen, was Lebenszeiten unnötig verlängern kann.

**Beispiel:**
```hemlock
fn outer() {
    let large_data = buffer(1000000);  // 1MB
    let counter = 0;

    return fn() {
        return counter;  // Verwendet nur 'counter', aber 'large_data' wird auch erfasst
    };
}
let f = outer();  // 'large_data' bleibt am Leben bis 'f' freigegeben wird
```

**Betroffene Dateien:**
- `src/backends/interpreter/values.c` (function_new, Closure-Erstellung)
- `src/frontend/parser/` (Variablen-Erfassungsanalyse)

### Lücke 6: Zyklische Referenz in Async-Koordination (NIEDRIGE PRIORITÄT)

**Problem:** Tasks, die Kanäle referenzieren, die Tasks referenzieren, könnten Zyklen erzeugen.

**Szenario:**
```hemlock
let ch = channel(1);
let task = spawn(fn() {
    ch.send(task);  // Task sendet sich selbst durch den Kanal
});
```

**Aktuelle Abhilfe:** Tiefe Kopie beim Senden verhindert diesen spezifischen Fall, aber Objektzyklen sind möglich.

### Lücke 7: FFI-Speichergrenze-Dokumentation (DOKUMENTATION)

**Problem:** Eigentumsübertragung über die FFI-Grenze ist nicht formal dokumentiert.

**Zu klärende Fragen:**
- Wem gehört der von externen Funktionen zurückgegebene Speicher?
- Was passiert mit Strings, die an C-Funktionen übergeben werden?
- Wie sollten Callbacks Speicher handhaben?

---

## Vorgeschlagene Verbesserungen

### Phase 1: Kritische Fixes (Wochen 1-2)

#### 1.1 Ausnahmesichere Ausdrucksauswertung

**Ansatz:** Implementierung eines "Temporäre-Werte-Stacks", der Allokationen während der Ausdrucksauswertung verfolgt.

```c
// In evaluator.c
typedef struct {
    Value *temps;
    int count;
    int capacity;
} TempStack;

// Temporäres vor Rückkehr aus Teilausdruck pushen
Value eval_binary_op(Evaluator *e, BinaryExpr *expr) {
    Value left = eval_expr(e, expr->left);
    temp_stack_push(e->temps, left);  // Verfolgen

    Value right = eval_expr(e, expr->right);
    temp_stack_push(e->temps, right);  // Verfolgen

    Value result = perform_op(left, right);

    temp_stack_pop(e->temps, 2);  // Bei Erfolg freigeben
    return result;
}

// Bei Ausnahme gibt Cleanup alle verfolgten Temps frei
void exception_cleanup(Evaluator *e) {
    while (e->temps->count > 0) {
        Value v = temp_stack_pop(e->temps, 1);
        value_release(v);
    }
}
```

#### 1.2 Bereinigung abgelöster Task-Ergebnisse

**Ansatz:** Abgelöste Tasks geben ihr eigenes Ergebnis bei Abschluss frei.

```c
// In concurrency.c - Task-Abschluss-Handler
void task_complete(Task *task, Value result) {
    pthread_mutex_lock(task->task_mutex);
    task->result = result;
    value_retain(task->result);  // Task besitzt Ergebnis
    task->state = TASK_COMPLETED;

    if (task->detached) {
        // Niemand wird join() aufrufen, also Ergebnis jetzt freigeben
        value_release(task->result);
        task->result = VAL_NULL;
    }
    pthread_mutex_unlock(task->task_mutex);
}
```

#### 1.3 Kanal-Drain beim Schließen

**Ansatz:** `channel_close()` und `channel_free()` müssen verbleibende Werte drainieren.

```c
// In values.c
void channel_free(Channel *ch) {
    pthread_mutex_lock(ch->mutex);

    // Gepufferte Werte drainieren
    while (ch->count > 0) {
        Value v = ch->buffer[ch->head];
        value_release(v);
        ch->head = (ch->head + 1) % ch->capacity;
        ch->count--;
    }

    pthread_mutex_unlock(ch->mutex);

    // Synchronisationsprimitive freigeben
    pthread_mutex_destroy(ch->mutex);
    pthread_cond_destroy(ch->not_empty);
    pthread_cond_destroy(ch->not_full);
    pthread_cond_destroy(ch->rendezvous);

    free(ch->buffer);
    free(ch);
}
```

### Phase 2: Bekannte Problem-Fixes (Wochen 3-4)

#### 2.1 Null-Koaleszenz-AST-Fix

**Ansatz:** Sicherstellen, dass AST-Knoten für kurzgeschlossene Ausdrücke noch für Bereinigung besucht werden, oder wertbasierte Darstellung anstelle von AST-Referenzen zur Auswertungszeit verwenden.

#### 2.2 Closure-Erfassungsoptimierung (Optional)

**Ansatz:** Variablenreferenzen im Funktionskörper analysieren und minimale Erfassungsliste erstellen.

### Phase 3: Testinfrastruktur-Härtung (Wochen 5-6)

#### 3.1 Leck-Regressionssuite

Erstellung einer dedizierten Leck-Regressions-Testsuite, die jede Lücke spezifisch testet:

```
tests/memory/
├── regression/
│   ├── exception_in_map.hml
│   ├── exception_in_filter.hml
│   ├── exception_in_reduce.hml
│   ├── exception_in_nested_call.hml
│   ├── detached_task_result.hml
│   ├── detached_task_spawn_loop.hml
│   ├── channel_close_with_values.hml
│   ├── channel_gc_stress.hml
│   ├── null_coalesce_literal.hml
│   ├── closure_large_capture.hml
│   └── cyclic_object_channel.hml
```

### Phase 4: Dokumentation & Vertrag (Woche 7)

#### 4.1 Speicher-Eigentumsdokumentation

Erstellen von `docs/advanced/memory-ownership.md`.

---

## Implementierungsphasen

| Phase | Fokus | Dauer | Priorität |
|-------|-------|-------|-----------|
| 1 | Kritische Fixes (Ausnahme, Detach, Kanal) | 2 Wochen | HOCH |
| 2 | Bekannte Problem-Fixes (Null-Koaleszenz, Erfassungen) | 2 Wochen | MITTEL |
| 3 | Testinfrastruktur | 2 Wochen | HOCH |
| 4 | Dokumentation | 1 Woche | MITTEL |

---

## Erfolgskriterien

### Quantitativ

- [ ] Null Lecks von ASAN auf vollständiger Testsuite gemeldet
- [ ] Null Lecks von Valgrind auf vollständiger Testsuite gemeldet
- [ ] Leck-Baseline etabliert und in CI erzwungen
- [ ] 100% der identifizierten Lücken behoben oder als akzeptabel dokumentiert

### Qualitativ

- [ ] Speicher-Eigentum in `docs/advanced/memory-ownership.md` dokumentiert
- [ ] FFI-Eigentumsregeln dokumentiert
- [ ] Regressionstest für jedes behobene Leck
- [ ] Fuzz-Testing in CI integriert

### Laufzeit-Vertragsverifizierung

Die folgenden Garantien müssen nach der Implementierung gelten:

1. **Kein Leck bei normaler Ausführung**: Jedes gültige Programm ausführen und normal beenden verursacht kein Leck (laufzeit-intern).
2. **Kein Leck bei Ausnahme**: Ausnahmen werfen und fangen verursacht kein Leck.
3. **Kein Leck bei Task-Abschluss**: Abgeschlossene Tasks (beigetreten oder abgelöst) verursachen kein Leck.
4. **Kein Leck beim Kanal-Schließen**: Kanäle schließen gibt alle gepufferten Werte frei.
5. **Deterministische Bereinigung**: Reihenfolge der Destruktoraufrufe ist vorhersagbar (LIFO für defer, topologisch für Objekte).

---

## Referenzen

- Aktueller Profiler: `src/backends/interpreter/profiler/profiler.c`
- Referenzzählung: `src/backends/interpreter/values.c:413-550`
- Task-Verwaltung: `src/backends/interpreter/builtins/concurrency.c`
- ASAN-Dokumentation: https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck: https://valgrind.org/docs/manual/mc-manual.html
