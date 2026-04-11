# Plan de prevention des fuites memoire

> Garantir que le runtime Hemlock est exempt de fuites memoire et respecte son contrat avec le programmeur.

**Date :** 2026-01-16
**Statut :** Termine (implemente dans v1.8.3)
**Version :** 1.0

---

## Resume executif

La philosophie de conception de Hemlock stipule : *"Nous vous donnons les outils pour etre en securite, mais nous ne vous forcons pas a les utiliser."* Cela signifie que le **runtime lui-meme** doit etre exempt de fuites meme quand le code utilisateur utilise des fonctionnalites non securisees. Le contrat du programmeur est :

1. **Les allocations utilisateur** (`alloc`, `buffer`) sont la responsabilite du programmeur de `free`
2. **Les allocations internes du runtime** (chaines, tableaux, objets, closures) sont gerees automatiquement via le comptage de references
3. **Les erreurs et exceptions** ne doivent pas provoquer de fuites memoire
4. **Les taches async** ont une semantique de propriete claire
5. **Le runtime ne cache jamais d'allocations** au programmeur

Ce plan identifie les lacunes dans l'infrastructure actuelle et propose des ameliorations systematiques.

---

## Table des matieres

1. [Evaluation de l'etat actuel](#evaluation-de-letat-actuel)
2. [Lacunes identifiees](#lacunes-identifiees)
3. [Ameliorations proposees](#ameliorations-proposees)
4. [Strategie de test](#strategie-de-test)
5. [Exigences de documentation](#exigences-de-documentation)
6. [Phases d'implementation](#phases-dimplementation)
7. [Criteres de succes](#criteres-de-succes)

---

## Evaluation de l'etat actuel

### Points forts

| Composant | Implementation | Emplacement |
|-----------|---------------|------------|
| Comptage de references | Operations atomiques avec `__ATOMIC_SEQ_CST` | `src/backends/interpreter/values.c:413-550` |
| Detection de cycles | VisitedSet pour le parcours de graphe | `src/backends/interpreter/values.c:1345-1480` |
| Isolation des threads | Copie profonde au spawn | `src/backends/interpreter/values.c:1687-1859` |
| Profilage avec detection de fuites | Suivi AllocSite | `src/backends/interpreter/profiler/` |
| Integration ASAN | Pipeline CI avec detection de fuites | `.github/workflows/tests.yml` |
| Support Valgrind | Multiples cibles Makefile | `Makefile:189-327` |
| Script de test complet | Tests par categorie | `tests/leak_check.sh` |

### Modele de propriete memoire actuel

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILITE DU PROGRAMMEUR                  │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  arithmetique ptr ────────────────────────────►  securite limites│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILITE DU RUNTIME                     │
├─────────────────────────────────────────────────────────────────┤
│  Litteraux/operations de chaine ─────► refcount + liberation auto│
│  Litteraux/operations de tableau ────► refcount + liberation auto│
│  Litteraux/operations d'objet ───────► refcount + liberation auto│
│  Closures de fonctions ─────────────► refcount + liberation env  │
│  Resultats de taches ───────────────► libere apres join()        │
│  Buffers de canaux ─────────────────► libere a close()           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Lacunes identifiees

### Lacune 1 : Nettoyage dans les chemins d'erreur (HAUTE PRIORITE)

**Probleme :** Quand des exceptions se produisent en cours d'execution, les temporaires alloues peuvent fuir.

**Scenario d'exemple :**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // Tableau alloue
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // Exception lancee
        return x * 2;
    });
    // 'transformed' partiellement alloue, 'arr' peut ne pas etre libere
}
```

**Etat actuel :** La gestion des exceptions de l'interpreteur deroule la pile d'appels mais peut ne pas liberer tous les temporaires crees pendant l'evaluation des expressions.

**Fichiers concernes :**
- `src/backends/interpreter/runtime/evaluator.c` (evaluation des expressions)
- `src/backends/interpreter/runtime/context.c` (gestion des exceptions)

### Lacune 2 : Propriete du resultat des taches detachees (PRIORITE MOYENNE)

**Probleme :** `detach(task)` permet une execution fire-and-forget, mais le resultat de la tache peut ne jamais etre collecte.

**Comportement actuel :**
```hemlock
let task = spawn(compute_something);
detach(task);  // La tache s'execute en arriere-plan
// Que se passe-t-il avec la valeur de retour quand la tache se termine ?
```

**Fichiers concernes :**
- `src/backends/interpreter/builtins/concurrency.c:148-165` (completion de tache)
- `src/backends/interpreter/values.c:745-780` (task_free)

### Lacune 3 : Semantique de fermeture vs drainage des canaux (PRIORITE MOYENNE)

**Probleme :** Quand un canal est ferme avec des valeurs bufferisees restantes, ces valeurs sont-elles correctement liberees ?

**Scenario :**
```hemlock
let ch = channel(10);
ch.send("a");
ch.send("b");
ch.close();  // "a" et "b" sont-ils liberes ?
```

**Fichiers concernes :**
- `src/backends/interpreter/values.c:850-915` (channel_close, channel_free)

### Lacune 4 : Fuite AST de coalescence null (CORRIGE)

**Probleme :** L'optimiseur optimisait les expressions de coalescence null quand le resultat etait connu a la compilation, mais ne liberait pas les noeuds AST abandonnes.

**Cause racine :** Dans `optimizer.c`, quand `??` etait optimise (par ex., `"value" ?? "default"` → `"value"`), l'optimiseur retournait l'enfant conserve sans liberer le noeud parent `EXPR_NULL_COALESCE` ni l'enfant abandonne.

**Correction :** Ajout d'un nettoyage correct dans l'optimiseur pour liberer les noeuds abandonnes :
- Sauvegarder l'enfant resultat
- Liberer l'enfant inutilise avec `expr_free()`
- Liberer la structure du noeud parent
- Retourner le resultat sauvegarde

**Fichiers modifies :**
- `src/frontend/optimizer/optimizer.c` (nettoyage de l'optimisation de coalescence null)

### Lacune 5 : Granularite de la liste de capture des closures (BASSE PRIORITE)

**Probleme :** Les closures capturent toute la chaine d'environnement plutot que seulement les variables referencees, prolongeant potentiellement les durees de vie inutilement.

**Exemple :**
```hemlock
fn outer() {
    let large_data = buffer(1000000);  // 1 Mo
    let counter = 0;

    return fn() {
        return counter;  // N'utilise que 'counter', mais 'large_data' est aussi capture
    };
}
let f = outer();  // 'large_data' reste vivant jusqu'a ce que 'f' soit libere
```

**Fichiers concernes :**
- `src/backends/interpreter/values.c` (function_new, creation de closure)
- `src/frontend/parser/` (analyse de capture de variables)

### Lacune 6 : Reference cyclique dans la coordination async (BASSE PRIORITE)

**Probleme :** Les taches referencant des canaux qui referencent des taches pourraient creer des cycles.

**Scenario :**
```hemlock
let ch = channel(1);
let task = spawn(fn() {
    ch.send(task);  // La tache s'envoie elle-meme a travers le canal
});
```

**Attenuation actuelle :** La copie profonde a l'envoi empeche ce cas specifique, mais les cycles d'objets sont possibles.

### Lacune 7 : Documentation de la frontiere memoire FFI (DOCUMENTATION)

**Probleme :** Le transfert de propriete a travers la frontiere FFI n'est pas formellement documente.

**Questions a clarifier :**
- Qui possede la memoire retournee par les fonctions extern ?
- Que se passe-t-il avec les chaines passees aux fonctions C ?
- Comment les callbacks doivent-ils gerer la memoire ?

---

## Ameliorations proposees

### Phase 1 : Corrections critiques (Semaines 1-2)

#### 1.1 Evaluation d'expressions securisee contre les exceptions

**Approche :** Implementer une "pile de valeurs temporaires" qui suit les allocations pendant l'evaluation des expressions.

```c
// Dans evaluator.c
typedef struct {
    Value *temps;
    int count;
    int capacity;
} TempStack;

// Empiler le temporaire avant de retourner depuis la sous-expression
Value eval_binary_op(Evaluator *e, BinaryExpr *expr) {
    Value left = eval_expr(e, expr->left);
    temp_stack_push(e->temps, left);  // Suivre

    Value right = eval_expr(e, expr->right);
    temp_stack_push(e->temps, right);  // Suivre

    Value result = perform_op(left, right);

    temp_stack_pop(e->temps, 2);  // Liberer en cas de succes
    return result;
}

// En cas d'exception, le nettoyage libere tous les temporaires suivis
void exception_cleanup(Evaluator *e) {
    while (e->temps->count > 0) {
        Value v = temp_stack_pop(e->temps, 1);
        value_release(v);
    }
}
```

**Tests :**
- Ajouter des tests dans `tests/memory/exception_cleanup.hml`
- Verification ASAN des chemins d'exception

#### 1.2 Nettoyage du resultat des taches detachees

**Approche :** Les taches detachees liberent leur propre resultat a la completion.

```c
// Dans concurrency.c - handler de completion de tache
void task_complete(Task *task, Value result) {
    pthread_mutex_lock(task->task_mutex);
    task->result = result;
    value_retain(task->result);  // La tache possede le resultat
    task->state = TASK_COMPLETED;

    if (task->detached) {
        // Personne ne fera join(), donc liberer le resultat maintenant
        value_release(task->result);
        task->result = VAL_NULL;
    }
    pthread_mutex_unlock(task->task_mutex);
}
```

**Tests :**
- Etendre `tests/manual/stress_memory_leak.hml` avec un stress de taches detachees
- Verifier aucune croissance dans le rapport de fuites ASAN

#### 1.3 Drainage du canal a la fermeture

**Approche :** `channel_close()` et `channel_free()` doivent drainer les valeurs restantes.

```c
// Dans values.c
void channel_free(Channel *ch) {
    pthread_mutex_lock(ch->mutex);

    // Drainer les valeurs bufferisees
    while (ch->count > 0) {
        Value v = ch->buffer[ch->head];
        value_release(v);
        ch->head = (ch->head + 1) % ch->capacity;
        ch->count--;
    }

    pthread_mutex_unlock(ch->mutex);

    // Liberer les primitives de synchronisation
    pthread_mutex_destroy(ch->mutex);
    pthread_cond_destroy(ch->not_empty);
    pthread_cond_destroy(ch->not_full);
    pthread_cond_destroy(ch->rendezvous);

    free(ch->buffer);
    free(ch);
}
```

**Tests :**
- Ajouter `tests/memory/channel_drain.hml`

### Phase 2 : Corrections de problemes connus (Semaines 3-4)

#### 2.1 Correction AST de coalescence null

**Approche :** S'assurer que les noeuds AST pour les expressions court-circuitees sont toujours visites pour le nettoyage, ou utiliser une representation basee sur les valeurs au lieu de references AST au moment de l'evaluation.

**Investigation necessaire :** Determiner si les noeuds AST doivent etre possedes par le parser ou copies pendant l'evaluation.

#### 2.2 Optimisation de capture des closures (Optionnel)

**Approche :** Analyser les references de variables dans le corps de la fonction et creer une liste de capture minimale.

```c
// Pendant le parsing de la fonction
typedef struct {
    char **captured_names;
    int count;
} CaptureList;

CaptureList *analyze_captures(FunctionExpr *fn, Environment *env) {
    CaptureList *list = capture_list_new();
    visit_expr(fn->body, fn->params, env, list);  // Collecter les variables libres referencees
    return list;
}
```

**Note :** C'est une optimisation, pas une correction. Peut etre reporte.

### Phase 3 : Renforcement de l'infrastructure de test (Semaines 5-6)

#### 3.1 Suite de regression de fuites

Creer une suite de tests de regression dediee qui cible specifiquement chaque lacune :

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

#### 3.2 Surveillance continue des fuites

**Amelioration de `tests/leak_check.sh` :**

```bash
# Ajouter la comparaison de ligne de base
BASELINE_FILE="tests/memory/baseline_leaks.txt"

check_regression() {
    local current_leaks=$(count_leaks)
    local baseline_leaks=$(cat "$BASELINE_FILE" 2>/dev/null || echo "0")

    if [ "$current_leaks" -gt "$baseline_leaks" ]; then
        echo "REGRESSION DE FUITE: $current_leaks > $baseline_leaks"
        exit 1
    fi
}
```

#### 3.3 Tests de fuzzing pour la securite memoire

Integrer libFuzzer ou AFL pour le fuzzing de securite memoire :

```c
// fuzz_evaluator.c
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    char *source = malloc(size + 1);
    memcpy(source, data, size);
    source[size] = '\0';

    // Parser et evaluer avec ASAN actif
    AST *ast = parse(source);
    if (ast) {
        ExecutionContext *ctx = ctx_new();
        evaluate(ctx, ast);  // ASAN detectera les fuites/UAF
        ctx_free(ctx);
        ast_free(ast);
    }

    free(source);
    return 0;
}
```

### Phase 4 : Documentation et contrat (Semaine 7)

#### 4.1 Documentation de la propriete memoire

Creer `docs/advanced/memory-ownership.md` :

```markdown
# Propriete memoire dans Hemlock

## Le contrat

1. **Vous allouez, vous liberez** : `alloc()` et `buffer()` retournent de la memoire que vous possedez.
2. **Le runtime gere les valeurs** : Chaines, tableaux, objets sont a comptage de references.
3. **Les exceptions nettoient** : Lancer ne provoque pas de fuite (apres la correction Phase 1).
4. **Les taches copient les arguments** : Les taches lancees obtiennent leur propre copie des donnees.
5. **Les canaux transferent la propriete** : `send()` transfere, `recv()` recoit.

## Points de transfert de propriete

| Operation | De | Vers |
|-----------|----|----|
| `let x = expr` | evaluation expr | liaison de variable |
| `return val` | fonction | appelant |
| `ch.send(val)` | emetteur | buffer du canal |
| `ch.recv()` | buffer du canal | recepteur |
| `spawn(fn, args)` | appelant (copies) | tache |
| `join(task)` | tache | appelant |

## Regles de propriete FFI

1. **Passage vers C** : Hemlock conserve la propriete sauf si le qualificateur `move` est utilise
2. **Reception depuis C** : Hemlock prend la propriete, liberera quand refcount→0
3. **Callbacks** : Arguments possedes par C, valeur de retour possedee par Hemlock
```

---

## Strategie de test

### Categories de tests

| Categorie | Description | Outil |
|-----------|-------------|-------|
| Unite | Tests de fuite de fonctions individuelles | ASAN |
| Integration | Scenarios multi-composants | ASAN + Valgrind |
| Stress | Cycles d'allocation/liberation a haut volume | ASAN (leak-check=no) |
| Fuzz | Securite memoire avec entrees aleatoires | libFuzzer + ASAN |
| Regression | Scenarios de fuites deja corrigees | ASAN + ligne de base |

### Amelioration du pipeline CI

```yaml
# .github/workflows/memory.yml
memory-safety:
  runs-on: ubuntu-latest
  steps:
    - name: Build with ASAN
      run: make asan

    - name: Run leak regression suite
      run: make leak-regression

    - name: Compare to baseline
      run: |
        ./tests/leak_check.sh --baseline
        if [ $? -ne 0 ]; then
          echo "::error::Regression de fuite detectee"
          exit 1
        fi

    - name: Fuzz test (5 minutes)
      run: make fuzz-test FUZZ_TIME=300
```

---

## Phases d'implementation

| Phase | Focus | Duree | Priorite |
|-------|-------|-------|----------|
| 1 | Corrections critiques (exception, detach, canal) | 2 semaines | HAUTE |
| 2 | Corrections de problemes connus (coalescence null, captures) | 2 semaines | MOYENNE |
| 3 | Infrastructure de test | 2 semaines | HAUTE |
| 4 | Documentation | 1 semaine | MOYENNE |

### Dependances

```
Phase 1 ──────► Phase 3 (les tests verifient les corrections)
    │
    └──────► Phase 4 (documenter les nouvelles garanties)

Phase 2 ──────► Phase 3 (ajouter des tests de regression)
```

---

## Criteres de succes

### Quantitatifs

- [ ] Zero fuite rapportee par ASAN sur la suite de tests complete
- [ ] Zero fuite rapportee par Valgrind sur la suite de tests complete
- [ ] Ligne de base de fuites etablie et appliquee dans le CI
- [ ] 100% des lacunes identifiees traitees ou documentees comme acceptables

### Qualitatifs

- [ ] Propriete memoire documentee dans `docs/advanced/memory-ownership.md`
- [ ] Regles de propriete FFI documentees
- [ ] Test de regression pour chaque fuite corrigee
- [ ] Tests de fuzzing integres dans le CI

### Verification du contrat du runtime

Les garanties suivantes doivent etre maintenues apres l'implementation :

1. **Pas de fuite en execution normale** : Executer tout programme valide et quitter normalement ne provoque pas de fuite memoire (interne au runtime).

2. **Pas de fuite en cas d'exception** : Lancer et attraper des exceptions ne provoque pas de fuite memoire.

3. **Pas de fuite a la completion de tache** : Les taches terminees (jointes ou detachees) ne provoquent pas de fuite memoire.

4. **Pas de fuite a la fermeture de canal** : Fermer les canaux libere toutes les valeurs bufferisees.

5. **Nettoyage deterministe** : L'ordre des appels de destructeur est predictible (LIFO pour defer, topologique pour les objets).

---

## Annexe : Fichiers necessitant des modifications

| Fichier | Modifications |
|---------|-------------|
| `src/backends/interpreter/runtime/evaluator.c` | Ajouter TempStack pour l'evaluation securisee contre les exceptions |
| `src/backends/interpreter/runtime/context.c` | Integration du nettoyage des exceptions |
| `src/backends/interpreter/builtins/concurrency.c` | Nettoyage du resultat des taches detachees |
| `src/backends/interpreter/values.c` | Drainage de canal, optimisation de capture |
| `tests/leak_check.sh` | Comparaison de ligne de base |
| `.github/workflows/tests.yml` | Ajouter un job de regression memoire |
| `docs/advanced/memory-ownership.md` | Nouvelle documentation |
| `CLAUDE.md` | Mettre a jour avec les garanties de propriete |

---

## References

- Profilage actuel : `src/backends/interpreter/profiler/profiler.c`
- Comptage de references : `src/backends/interpreter/values.c:413-550`
- Gestion des taches : `src/backends/interpreter/builtins/concurrency.c`
- Documentation ASAN : https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck : https://valgrind.org/docs/manual/mc-manual.html
