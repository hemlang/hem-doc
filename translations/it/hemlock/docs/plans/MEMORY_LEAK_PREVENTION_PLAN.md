# Piano di Prevenzione dei Memory Leak

> Garantire che il runtime di Hemlock sia privo di memory leak e rispetti il contratto con il programmatore.

**Data:** 2026-01-16
**Stato:** Completato (implementato nella v1.8.3)
**Versione:** 1.0

---

## Sommario Esecutivo

La filosofia di design di Hemlock afferma: *"Ti diamo gli strumenti per essere sicuro, ma non ti obblighiamo a usarli."* Questo significa che il **runtime stesso** deve essere privo di leak anche quando il codice utente usa funzionalità non sicure. Il contratto del programmatore è:

1. **Le allocazioni dell'utente** (`alloc`, `buffer`) sono responsabilità del programmatore da liberare con `free`
2. **Le allocazioni interne del runtime** (stringhe, array, oggetti, closure) sono gestite automaticamente tramite conteggio dei riferimenti
3. **Errori ed eccezioni** non devono causare memory leak
4. **I task asincroni** hanno semantiche di ownership chiare
5. **Il runtime non nasconde mai allocazioni** al programmatore

Questo piano identifica le lacune nell'infrastruttura attuale e propone miglioramenti sistematici.

---

## Indice

1. [Valutazione dello Stato Attuale](#valutazione-dello-stato-attuale)
2. [Lacune Identificate](#lacune-identificate)
3. [Miglioramenti Proposti](#miglioramenti-proposti)
4. [Strategia di Testing](#strategia-di-testing)
5. [Requisiti di Documentazione](#requisiti-di-documentazione)
6. [Fasi di Implementazione](#fasi-di-implementazione)
7. [Criteri di Successo](#criteri-di-successo)

---

## Valutazione dello Stato Attuale

### Punti di Forza

| Componente | Implementazione | Posizione |
|------------|----------------|-----------|
| Conteggio riferimenti | Operazioni atomiche con `__ATOMIC_SEQ_CST` | `src/backends/interpreter/values.c:413-550` |
| Rilevamento cicli | VisitedSet per attraversamento grafo | `src/backends/interpreter/values.c:1345-1480` |
| Isolamento thread | Copia profonda allo spawn | `src/backends/interpreter/values.c:1687-1859` |
| Profiler con rilevamento leak | Tracciamento AllocSite | `src/backends/interpreter/profiler/` |
| Integrazione ASAN | Pipeline CI con rilevamento leak | `.github/workflows/tests.yml` |
| Supporto Valgrind | Target multipli nel Makefile | `Makefile:189-327` |
| Script test completo | Testing basato su categorie | `tests/leak_check.sh` |

### Modello Attuale di Ownership della Memoria

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILITA' DEL PROGRAMMATORE             │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  aritmetica ptr ──────────────────────────────►  sicurezza limiti│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILITA' DEL RUNTIME                   │
├─────────────────────────────────────────────────────────────────┤
│  Letterali/operazioni stringa ────────► refcount + auto-release │
│  Letterali/operazioni array ──────────► refcount + auto-release │
│  Letterali/operazioni oggetto ────────► refcount + auto-release │
│  Closure funzione ────────────────────► refcount + rilascio env │
│  Risultati task ──────────────────────► rilasciati dopo join()  │
│  Buffer canale ───────────────────────► rilasciati su close()   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lacune Identificate

### Lacuna 1: Pulizia nei Percorsi di Errore (ALTA PRIORITA')

**Problema:** Quando si verificano eccezioni durante l'esecuzione, i temporanei allocati possono causare leak.

**Scenario di Esempio:**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // Array allocato
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // Eccezione lanciata
        return x * 2;
    });
    // 'transformed' parzialmente allocato, 'arr' potrebbe non essere rilasciato
}
```

**Stato Attuale:** La gestione delle eccezioni dell'interprete srotola lo stack delle chiamate ma potrebbe non rilasciare tutti i temporanei creati durante la valutazione delle espressioni.

**File Interessati:**
- `src/backends/interpreter/runtime/evaluator.c` (valutazione espressioni)
- `src/backends/interpreter/runtime/context.c` (gestione eccezioni)

### Lacuna 2: Ownership del Risultato dei Task Detached (MEDIA PRIORITA')

**Problema:** `detach(task)` permette l'esecuzione fire-and-forget, ma il risultato del task potrebbe non essere mai raccolto.

**Comportamento Attuale:**
```hemlock
let task = spawn(compute_something);
detach(task);  // Il task esegue in background
// Cosa succede al valore di ritorno quando il task completa?
```

**File Interessati:**
- `src/backends/interpreter/builtins/concurrency.c:148-165` (completamento task)
- `src/backends/interpreter/values.c:745-780` (task_free)

### Lacuna 3: Semantiche di Close vs. Drain del Canale (MEDIA PRIORITA')

**Problema:** Quando un canale viene chiuso con valori ancora nel buffer, quei valori vengono propriamente rilasciati?

**Scenario:**
```hemlock
let ch = channel(10);
ch.send("a");
ch.send("b");
ch.close();  // "a" e "b" vengono rilasciati?
```

**File Interessati:**
- `src/backends/interpreter/values.c:850-915` (channel_close, channel_free)

### Lacuna 4: Leak AST del Null Coalescing (CORRETTA)

**Problema:** L'ottimizzatore stava ottimizzando le espressioni null coalescing quando il risultato era conosciuto a compile time, ma senza liberare i nodi AST scartati.

**Causa Radice:** In `optimizer.c`, quando `??` veniva ottimizzato (es., `"value" ?? "default"` → `"value"`), l'ottimizzatore restituiva il figlio mantenuto senza liberare il nodo padre `EXPR_NULL_COALESCE` o il figlio scartato.

**Correzione:** Aggiunta pulizia appropriata nell'ottimizzatore per liberare i nodi scartati:
- Salvare il figlio risultato
- Liberare il figlio inutilizzato con `expr_free()`
- Liberare la struttura del nodo padre
- Restituire il risultato salvato

**File Modificati:**
- `src/frontend/optimizer/optimizer.c` (pulizia ottimizzazione null coalescing)

### Lacuna 5: Granularità della Lista di Cattura delle Closure (BASSA PRIORITA')

**Problema:** Le closure catturano l'intera catena di ambienti piuttosto che solo le variabili referenziate, potenzialmente estendendo i tempi di vita inutilmente.

**Esempio:**
```hemlock
fn outer() {
    let large_data = buffer(1000000);  // 1MB
    let counter = 0;

    return fn() {
        return counter;  // Usa solo 'counter', ma 'large_data' viene catturato anch'esso
    };
}
let f = outer();  // 'large_data' mantenuto vivo finché 'f' non viene rilasciato
```

**File Interessati:**
- `src/backends/interpreter/values.c` (function_new, creazione closure)
- `src/frontend/parser/` (analisi cattura variabili)

### Lacuna 6: Riferimento Ciclico nella Coordinazione Async (BASSA PRIORITA')

**Problema:** Task che referenziano canali che referenziano task potrebbero creare cicli.

**Scenario:**
```hemlock
let ch = channel(1);
let task = spawn(fn() {
    ch.send(task);  // Il task invia se stesso attraverso il canale
});
```

**Mitigazione attuale:** La copia profonda all'invio previene questo caso specifico, ma i cicli tra oggetti sono possibili.

### Lacuna 7: Documentazione del Confine di Memoria FFI (DOCUMENTAZIONE)

**Problema:** Il trasferimento di ownership attraverso il confine FFI non è formalmente documentato.

**Domande da chiarire:**
- Chi possiede la memoria restituita dalle funzioni extern?
- Cosa succede alle stringhe passate alle funzioni C?
- Come dovrebbero i callback gestire la memoria?

---

## Miglioramenti Proposti

### Fase 1: Correzioni Critiche (Settimane 1-2)

#### 1.1 Valutazione Espressioni Exception-Safe

**Approccio:** Implementare uno "stack di valori temporanei" che traccia le allocazioni durante la valutazione delle espressioni.

```c
// In evaluator.c
typedef struct {
    Value *temps;
    int count;
    int capacity;
} TempStack;

// Push temporaneo prima di ritornare dalla sotto-espressione
Value eval_binary_op(Evaluator *e, BinaryExpr *expr) {
    Value left = eval_expr(e, expr->left);
    temp_stack_push(e->temps, left);  // Traccia

    Value right = eval_expr(e, expr->right);
    temp_stack_push(e->temps, right);  // Traccia

    Value result = perform_op(left, right);

    temp_stack_pop(e->temps, 2);  // Rilascia in caso di successo
    return result;
}

// In caso di eccezione, cleanup rilascia tutti i temporanei tracciati
void exception_cleanup(Evaluator *e) {
    while (e->temps->count > 0) {
        Value v = temp_stack_pop(e->temps, 1);
        value_release(v);
    }
}
```

**Testing:**
- Aggiungere test in `tests/memory/exception_cleanup.hml`
- Verifica ASAN dei percorsi di eccezione

#### 1.2 Pulizia Risultato Task Detached

**Approccio:** I task detached rilasciano il proprio risultato quando completano.

```c
// In concurrency.c - handler di completamento task
void task_complete(Task *task, Value result) {
    pthread_mutex_lock(task->task_mutex);
    task->result = result;
    value_retain(task->result);  // Il task possiede il risultato
    task->state = TASK_COMPLETED;

    if (task->detached) {
        // Nessuno farà join(), quindi rilascia il risultato ora
        value_release(task->result);
        task->result = VAL_NULL;
    }
    pthread_mutex_unlock(task->task_mutex);
}
```

**Testing:**
- Estendere `tests/manual/stress_memory_leak.hml` con stress test su task detached
- Verificare nessuna crescita nel report leak ASAN

#### 1.3 Drain del Canale alla Chiusura

**Approccio:** `channel_close()` e `channel_free()` devono svuotare i valori rimanenti.

```c
// In values.c
void channel_free(Channel *ch) {
    pthread_mutex_lock(ch->mutex);

    // Svuota i valori nel buffer
    while (ch->count > 0) {
        Value v = ch->buffer[ch->head];
        value_release(v);
        ch->head = (ch->head + 1) % ch->capacity;
        ch->count--;
    }

    pthread_mutex_unlock(ch->mutex);

    // Libera le primitive di sincronizzazione
    pthread_mutex_destroy(ch->mutex);
    pthread_cond_destroy(ch->not_empty);
    pthread_cond_destroy(ch->not_full);
    pthread_cond_destroy(ch->rendezvous);

    free(ch->buffer);
    free(ch);
}
```

**Testing:**
- Aggiungere `tests/memory/channel_drain.hml`

### Fase 2: Correzioni Problemi Noti (Settimane 3-4)

#### 2.1 Correzione AST Null Coalescing

**Approccio:** Assicurarsi che i nodi AST per espressioni cortocircuitate siano comunque visitati per la pulizia, oppure usare una rappresentazione basata sui valori invece di riferimenti AST al momento della valutazione.

**Investigazione necessaria:** Determinare se i nodi AST dovrebbero appartenere al parser o essere copiati durante la valutazione.

#### 2.2 Ottimizzazione Cattura Closure (Opzionale)

**Approccio:** Analizzare i riferimenti alle variabili nel corpo della funzione e creare una lista di cattura minimale.

```c
// Durante il parsing della funzione
typedef struct {
    char **captured_names;
    int count;
} CaptureList;

CaptureList *analyze_captures(FunctionExpr *fn, Environment *env) {
    CaptureList *list = capture_list_new();
    visit_expr(fn->body, fn->params, env, list);  // Raccoglie variabili libere referenziate
    return list;
}
```

**Nota:** Questa è un'ottimizzazione, non una correzione di correttezza. Potrebbe essere differita.

### Fase 3: Irrobustimento dell'Infrastruttura di Testing (Settimane 5-6)

#### 3.1 Suite di Regressione Leak

Creare una suite di test di regressione leak dedicata che mira specificamente a ogni lacuna:

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

#### 3.2 Monitoraggio Continuo dei Leak

**Miglioramento a `tests/leak_check.sh`:**

```bash
# Aggiungere confronto con baseline
BASELINE_FILE="tests/memory/baseline_leaks.txt"

check_regression() {
    local current_leaks=$(count_leaks)
    local baseline_leaks=$(cat "$BASELINE_FILE" 2>/dev/null || echo "0")

    if [ "$current_leaks" -gt "$baseline_leaks" ]; then
        echo "REGRESSIONE LEAK: $current_leaks > $baseline_leaks"
        exit 1
    fi
}
```

#### 3.3 Fuzz Testing per la Sicurezza della Memoria

Integrare libFuzzer o AFL per il fuzz testing della sicurezza della memoria:

```c
// fuzz_evaluator.c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char *source = malloc(size + 1);
    memcpy(source, data, size);
    source[size] = '\0';

    // Parse e valuta con ASAN attivo
    AST *ast = parse(source);
    if (ast) {
        ExecutionContext *ctx = ctx_new();
        evaluate(ctx, ast);  // ASAN catturerà leak/UAF
        ctx_free(ctx);
        ast_free(ast);
    }

    free(source);
    return 0;
}
```

### Fase 4: Documentazione e Contratto (Settimana 7)

#### 4.1 Documentazione dell'Ownership della Memoria

Creare `docs/advanced/memory-ownership.md`:

```markdown
# Ownership della Memoria in Hemlock

## Il Contratto

1. **Tu allochi, tu liberi**: `alloc()` e `buffer()` restituiscono memoria che possiedi.
2. **Il runtime gestisce i valori**: Stringhe, array, oggetti hanno conteggio riferimenti.
3. **Le eccezioni puliscono**: Lanciare non causa leak (dopo la correzione della Fase 1).
4. **I task copiano gli argomenti**: I task spawnati ricevono la propria copia dei dati.
5. **I canali trasferiscono ownership**: `send()` trasferisce, `recv()` riceve.

## Punti di Trasferimento dell'Ownership

| Operazione | Da | A |
|-----------|------|------|
| `let x = expr` | valutazione expr | binding variabile |
| `return val` | funzione | chiamante |
| `ch.send(val)` | mittente | buffer canale |
| `ch.recv()` | buffer canale | ricevitore |
| `spawn(fn, args)` | chiamante (copie) | task |
| `join(task)` | task | chiamante |

## Regole di Ownership FFI

1. **Passaggio al C**: Hemlock mantiene l'ownership a meno che non si usi il qualificatore `move`
2. **Ricezione dal C**: Hemlock assume l'ownership, libererà quando refcount→0
3. **Callback**: Gli argomenti appartengono al C, il valore di ritorno appartiene a Hemlock
```

---

## Strategia di Testing

### Categorie di Test

| Categoria | Descrizione | Strumento |
|-----------|-------------|-----------|
| Unitari | Test leak su singole funzioni | ASAN |
| Integrazione | Scenari multi-componente | ASAN + Valgrind |
| Stress | Cicli di allocazione/liberazione ad alto volume | ASAN (leak-check=no) |
| Fuzz | Sicurezza memoria con input casuali | libFuzzer + ASAN |
| Regressione | Scenari di leak già corretti | ASAN + baseline |

### Miglioramento Pipeline CI

```yaml
# .github/workflows/memory.yml
memory-safety:
  runs-on: ubuntu-latest
  steps:
    - name: Build con ASAN
      run: make asan

    - name: Esegui suite regressione leak
      run: make leak-regression

    - name: Confronta con baseline
      run: |
        ./tests/leak_check.sh --baseline
        if [ $? -ne 0 ]; then
          echo "::error::Regressione leak rilevata"
          exit 1
        fi

    - name: Fuzz test (5 minuti)
      run: make fuzz-test FUZZ_TIME=300
```

---

## Fasi di Implementazione

| Fase | Focus | Durata | Priorità |
|------|-------|--------|----------|
| 1 | Correzioni critiche (eccezione, detach, canale) | 2 settimane | ALTA |
| 2 | Correzioni problemi noti (null coalesce, catture) | 2 settimane | MEDIA |
| 3 | Infrastruttura di testing | 2 settimane | ALTA |
| 4 | Documentazione | 1 settimana | MEDIA |

### Dipendenze

```
Fase 1 ──────► Fase 3 (i test verificano le correzioni)
    │
    └──────► Fase 4 (documenta le nuove garanzie)

Fase 2 ──────► Fase 3 (aggiungi test di regressione)
```

---

## Criteri di Successo

### Quantitativi

- [ ] Zero leak segnalati da ASAN sulla suite di test completa
- [ ] Zero leak segnalati da Valgrind sulla suite di test completa
- [ ] Baseline leak stabilita e applicata nella CI
- [ ] 100% delle lacune identificate affrontate o documentate come accettabili

### Qualitativi

- [ ] Ownership della memoria documentata in `docs/advanced/memory-ownership.md`
- [ ] Regole di ownership FFI documentate
- [ ] Test di regressione per ogni leak corretto
- [ ] Fuzz testing integrato nella CI

### Verifica del Contratto del Runtime

Le seguenti garanzie devono valere dopo l'implementazione:

1. **Nessun leak in esecuzione normale**: L'esecuzione di qualsiasi programma valido e l'uscita normale non causano leak di memoria (interna al runtime).

2. **Nessun leak sulle eccezioni**: Lanciare e catturare eccezioni non causa leak di memoria.

3. **Nessun leak al completamento dei task**: I task completati (joinati o detached) non causano leak di memoria.

4. **Nessun leak alla chiusura dei canali**: Chiudere i canali rilascia tutti i valori nel buffer.

5. **Pulizia deterministica**: L'ordine delle chiamate ai distruttori è prevedibile (LIFO per defer, topologico per oggetti).

---

## Appendice: File che Richiedono Modifica

| File | Modifiche |
|------|----------|
| `src/backends/interpreter/runtime/evaluator.c` | Aggiungere TempStack per valutazione exception-safe |
| `src/backends/interpreter/runtime/context.c` | Integrazione pulizia eccezioni |
| `src/backends/interpreter/builtins/concurrency.c` | Pulizia risultato task detached |
| `src/backends/interpreter/values.c` | Drain canale, ottimizzazione cattura |
| `tests/leak_check.sh` | Confronto con baseline |
| `.github/workflows/tests.yml` | Aggiungere job regressione memoria |
| `docs/advanced/memory-ownership.md` | Nuova documentazione |
| `CLAUDE.md` | Aggiornare con garanzie di ownership |

---

## Riferimenti

- Profiler attuale: `src/backends/interpreter/profiler/profiler.c`
- Conteggio riferimenti: `src/backends/interpreter/values.c:413-550`
- Gestione task: `src/backends/interpreter/builtins/concurrency.c`
- Documentazione ASAN: https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck: https://valgrind.org/docs/manual/mc-manual.html
