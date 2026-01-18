# Design della Sintassi delle Firme

> Estensione del sistema di tipi di Hemlock con tipi funzione, modificatori nullable, alias di tipo, parametri const e firme di metodo.

**Stato:** Implementato (v1.7.0)
**Versione:** 1.0
**Autore:** Claude

---

## Panoramica

Questo documento propone cinque estensioni interconnesse del sistema di tipi che si basano sull'infrastruttura esistente di Hemlock:

1. **Annotazioni Tipo Funzione** - Tipi funzione di prima classe
2. **Modificatori Tipo Nullable** - Gestione esplicita del null (estende flag `nullable` esistente)
3. **Alias di Tipo** - Abbreviazioni di tipo con nome
4. **Parametri Const** - Contratti di immutabilità
5. **Firme di Metodo in Define** - Comportamento simile a interfacce

Queste funzionalità condividono la filosofia: **esplicito su implicito, opzionale ma applicato quando usato**.

---

## 1. Annotazioni Tipo Funzione

### Motivazione

Attualmente, non c'è modo di esprimere la firma di una funzione come tipo:

```hemlock
// Attuale: callback non ha informazioni di tipo
fn map(arr: array, callback) { ... }

// Proposto: tipo funzione esplicito
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Sintassi

```hemlock
// Tipo funzione base
fn(i32, i32): i32

// Con nomi parametri (solo documentazione, non applicati)
fn(a: i32, b: i32): i32

// Nessun valore ritorno (void)
fn(string): void
fn(string)              // Abbreviazione: ometti `: void`

// Ritorno nullable
fn(i32): string?

// Parametri opzionali
fn(nome: string, eta?: i32): void

// Parametri rest
fn(...args: array): i32

// Nessun parametro
fn(): bool

// Ordine superiore: funzione che restituisce funzione
fn(i32): fn(i32): i32

// Tipo funzione async
async fn(i32): i32
```

### Esempi d'Uso

```hemlock
// Variabile con tipo funzione
let somma: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parametro funzione
fn applica(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// Tipo ritorno è funzione
fn crea_sommatore(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Array di funzioni
let ops: array<fn(i32, i32): i32> = [somma, sottrai, moltiplica];

// Campo oggetto
define EventHandler {
    nome: string;
    callback: fn(Event): void;
}
```

### Modifiche AST

```c
// In enum TypeKind (include/ast.h)
typedef enum {
    // ... tipi esistenti ...
    TYPE_FUNCTION,      // NUOVO: Tipo funzione
} TypeKind;

// In struct Type (include/ast.h)
struct Type {
    TypeKind kind;
    // ... campi esistenti ...

    // Per TYPE_FUNCTION:
    struct Type **param_types;      // Tipi parametri
    char **param_names;             // Nomi parametri opzionali (docs)
    int *param_optional;            // Quali param sono opzionali
    int num_params;
    char *rest_param_name;          // Nome parametro rest o NULL
    struct Type *rest_param_type;   // Tipo parametro rest
    struct Type *return_type;       // Tipo ritorno (NULL = void)
    int is_async;                   // tipo fn async
};
```

### Parsing

I tipi funzione iniziano con `fn` (o `async fn`) seguito dalla lista parametri:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Disambiguazione:** Quando si parsa un tipo e si incontra `fn`:
- Se seguito da `(`, è un tipo funzione
- Altrimenti, errore di sintassi (`fn` da solo non è un tipo valido)

### Compatibilità Tipi

```hemlock
// Match esatto richiesto per tipi funzione
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Controvarianza parametri (accettare tipi più ampi è OK)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Covarianza ritorno (restituire tipi più ristretti è OK)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Arità deve corrispondere
let bad: fn(i32): i32 = fn(a, b) { return a; };       // ERRORE: mismatch arità

// Parametri opzionali compatibili con richiesti
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Modificatori Tipo Nullable

### Motivazione

Il suffisso `?` rende esplicita l'accettazione del null nelle firme:

```hemlock
// Attuale: non chiaro se null è valido
fn trova(arr: array, val: any): i32 { ... }

// Proposto: ritorno nullable esplicito
fn trova(arr: array, val: any): i32? { ... }
```

### Sintassi

```hemlock
// Tipi nullable con suffisso ?
string?           // stringa o null
i32?              // i32 o null
Utente?           // Utente o null
array<i32>?       // array o null
fn(i32): i32?     // funzione che restituisce i32 o null

// Composizione con tipi funzione
fn(string?): i32          // Accetta stringa o null
fn(string): i32?          // Restituisce i32 o null
fn(string?): i32?         // Entrambi nullable

// In define
define Risultato {
    valore: any?;
    errore: string?;
}
```

### Note Implementazione

**Già esiste:** Il flag `Type.nullable` è già nell'AST. Questa funzionalità necessita principalmente:
1. Supporto parser per suffisso `?` su qualsiasi tipo (verificare/estendere)
2. Composizione corretta con tipi funzione
3. Applicazione runtime

### Compatibilità Tipi

```hemlock
// Non-nullable assegnabile a nullable
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullable NON assegnabile a non-nullable
let z: i32 = x;             // ERRORE: x potrebbe essere null

// Null coalescing per unwrap
let z: i32 = x ?? 0;        // OK: ?? fornisce default

// Optional chaining restituisce nullable
let nome: string? = utente?.nome;
```

---

## 3. Alias di Tipo

### Motivazione

Tipi complessi beneficiano di abbreviazioni con nome:

```hemlock
// Attuale: tipi composti ripetitivi
fn elabora(entita: HaNome & HaId & HaTimestamp) { ... }
fn valida(entita: HaNome & HaId & HaTimestamp) { ... }

// Proposto: alias con nome
type Entita = HaNome & HaId & HaTimestamp;
fn elabora(entita: Entita) { ... }
fn valida(entita: Entita) { ... }
```

### Sintassi

```hemlock
// Alias base
type Intero = i32;
type Testo = string;

// Alias tipo composto
type Entita = HaNome & HaId;
type Auditabile = HaCreatoIl & HaModificatoIl & HaCreadaDa;

// Alias tipo funzione
type Callback = fn(Evento): void;
type Predicato = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type TaskAsync = async fn(): any;

// Alias nullable
type StringaOpzionale = string?;

// Alias generico (se supportiamo alias tipo generici)
type Coppia<T> = { primo: T, secondo: T };
type Risultato<T, E> = { valore: T?, errore: E? };

// Alias tipo array
type ArrayInt = array<i32>;
type Matrice = array<array<f64>>;
```

### Scope e Visibilità

```hemlock
// Scope modulo di default
type Callback = fn(Evento): void;

// Esportabile
export type Handler = fn(Request): Response;

// In altro file
import { Handler } from "./handlers.hml";
fn registra(h: Handler) { ... }
```

### Modifiche AST

```c
// Nuovo tipo istruzione
typedef enum {
    // ... istruzioni esistenti ...
    STMT_TYPE_ALIAS,    // NUOVO
} StmtKind;

// In union Stmt
struct {
    char *name;                 // Nome alias
    char **type_params;         // Param generici: <T, U>
    int num_type_params;
    Type *aliased_type;         // Il tipo effettivo
} type_alias;
```

### Parsing

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Nota:** `type` è una nuova parola chiave. Verifica conflitti con identificatori esistenti.

### Risoluzione

Gli alias di tipo sono risolti a:
- **Tempo di parse:** Alias registrato in type environment
- **Tempo di controllo:** Alias espanso a tipo sottostante
- **Runtime:** Alias è trasparente (stesso del tipo sottostante)

```hemlock
type MioInt = i32;
let x: MioInt = 42;
typeof(x);           // "i32" (non "MioInt")
```

---

## 4. Parametri Const

### Motivazione

Segnala l'intento di immutabilità nelle firme di funzione:

```hemlock
// Attuale: non chiaro se array sarà modificato
fn stampa_tutti(elementi: array) { ... }

// Proposto: contratto di immutabilità esplicito
fn stampa_tutti(const elementi: array) { ... }
```

### Sintassi

```hemlock
// Parametro const
fn elabora(const dati: buffer) {
    // dati[0] = 0;        // ERRORE: non può mutare const
    let x = dati[0];       // OK: lettura permessa
    return x;
}

// Più parametri const
fn confronta(const a: array, const b: array): bool { ... }

// Const e mutabile misti
fn aggiorna(const sorgente: array, destinazione: array) {
    for (elem in sorgente) {
        destinazione.push(elem);   // OK: destinazione è mutabile
    }
}

// Const con inferenza tipo
fn log(const msg) {
    print(msg);
}

// Const in tipi funzione
type Lettore = fn(const buffer): i32;
```

### Cosa Previene Const

```hemlock
fn cattivo(const arr: array) {
    arr.push(1);         // ERRORE: metodo mutante
    arr.pop();           // ERRORE: metodo mutante
    arr[0] = 5;          // ERRORE: assegnazione indice
    arr.clear();         // ERRORE: metodo mutante
}

fn buono(const arr: array) {
    let x = arr[0];      // OK: lettura
    let lun = len(arr);  // OK: controllo lunghezza
    let copia = arr.slice(0, 10);  // OK: crea nuovo array
    for (elem in arr) {  // OK: iterazione
        print(elem);
    }
}
```

### Metodi Mutanti vs Non-Mutanti

| Tipo | Mutanti (bloccati da const) | Non-Mutanti (permessi) |
|------|----------------------------|------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (in-place) | slice, concat, map, filter, find, contains, first, last, join |
| string | assegnazione indice (`s[0] = 'x'`) | tutti i metodi (restituiscono nuove stringhe) |
| buffer | assegnazione indice, memset, memcpy (verso) | lettura indice, slice |
| object | assegnazione campo | lettura campo |

### Modifiche AST

```c
// In espressione funzione (include/ast.h)
struct {
    // ... campi esistenti ...
    int *param_is_const;    // NUOVO: 1 se const, 0 altrimenti
} function;

// In struct Type per tipi funzione
struct Type {
    // ... campi esistenti ...
    int *param_is_const;    // Per TYPE_FUNCTION
};
```

### Applicazione

**Interprete:**
- Traccia const-ness nei binding variabili
- Verifica prima delle operazioni di mutazione
- Errore runtime su violazione const

**Compilatore:**
- Emetti variabili C const-qualified dove benefico
- Analisi statica per violazioni const
- Warning/errore a compile-time

---

## 5. Firme di Metodo in Define

### Motivazione

Permette ai blocchi `define` di specificare metodi attesi, non solo campi dati:

```hemlock
// Attuale: solo campi dati
define Utente {
    nome: string;
    eta: i32;
}

// Proposto: firme metodo
define Comparabile {
    fn confronta(altro: Self): i32;
}

define Serializzabile {
    fn serializza(): string;
    fn deserializza(dati: string): Self;  // Metodo statico
}
```

### Sintassi

```hemlock
// Firma metodo (nessun corpo)
define Hashable {
    fn hash(): i32;
}

// Metodi multipli
define Collezione {
    fn dimensione(): i32;
    fn e_vuota(): bool;
    fn contiene(elemento: any): bool;
}

// Campi e metodi misti
define Entita {
    id: i32;
    nome: string;
    fn valida(): bool;
    fn serializza(): string;
}

// Usando tipo Self
define Clonabile {
    fn clona(): Self;
}

define Comparabile {
    fn confronta(altro: Self): i32;
    fn uguale(altro: Self): bool;
}

// Metodi opzionali
define Stampabile {
    fn to_string(): string;
    fn debug_string?(): string;  // Metodo opzionale (può essere assente)
}

// Metodi con implementazione default
define Ordinato {
    fn confronta(altro: Self): i32;  // Richiesto

    // Implementazioni default (ereditate se non sovrascritte)
    fn minore_di(altro: Self): bool {
        return self.confronta(altro) < 0;
    }
    fn maggiore_di(altro: Self): bool {
        return self.confronta(altro) > 0;
    }
    fn uguale(altro: Self): bool {
        return self.confronta(altro) == 0;
    }
}
```

### Il Tipo `Self`

`Self` si riferisce al tipo concreto che implementa l'interfaccia:

```hemlock
define Sommabile {
    fn somma(altro: Self): Self;
}

// Quando usato:
let a: Sommabile = {
    valore: 10,
    somma: fn(altro) {
        return { valore: self.valore + altro.valore, somma: self.somma };
    }
};
```

### Tipizzazione Strutturale (Duck Typing)

Le firme metodo usano lo stesso duck typing dei campi:

```hemlock
define Stringificabile {
    fn to_string(): string;
}

// Qualsiasi oggetto con metodo to_string() soddisfa Stringificabile
let x: Stringificabile = {
    nome: "test",
    to_string: fn() { return self.nome; }
};

// Tipi composti con metodi
define Nominato { nome: string; }
define Stampabile { fn to_string(): string; }

type NominatoStampabile = Nominato & Stampabile;

let y: NominatoStampabile = {
    nome: "Alice",
    to_string: fn() { return "Nome: " + self.nome; }
};
```

### Modifiche AST

```c
// Estendi define_object in union Stmt
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Campi (esistenti)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Metodi (NUOVO)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Metodi opzionali (fn nome?(): tipo)
    Expr **method_defaults;     // Implementazioni default (NULL se solo firma)
    int num_methods;
} define_object;
```

### Controllo Tipi

Quando si controlla `valore: TipoInterfaccia`:
1. Verifica tutti i campi richiesti esistano con tipi compatibili
2. Verifica tutti i metodi richiesti esistano con firme compatibili
3. Campi/metodi opzionali possono essere assenti

```hemlock
define Ordinabile {
    fn confronta(altro: Self): i32;
}

// Valido: ha metodo confronta
let valido: Ordinabile = {
    valore: 10,
    confronta: fn(altro) { return self.valore - altro.valore; }
};

// Non valido: manca confronta
let invalido: Ordinabile = { valore: 10 };  // ERRORE: metodo 'confronta' mancante

// Non valido: firma sbagliata
let sbagliato: Ordinabile = {
    confronta: fn() { return 0; }  // ERRORE: atteso (Self): i32
};
```

---

## Esempi di Interazione

### Combinare Tutte le Funzionalità

```hemlock
// Alias tipo per tipo funzione complesso
type CallbackEvento = fn(evento: Evento, contesto: Contesto?): bool;

// Alias tipo per interfaccia composta
type Entita = HaId & HaNome & Serializzabile;

// Define con firme metodo
define Repository<T> {
    fn trova(id: i32): T?;
    fn salva(const entita: T): bool;
    fn elimina(id: i32): bool;
    fn trova_tutti(predicato: fn(T): bool): array<T>;
}

// Usare tutto insieme
fn crea_repo_utente(): Repository<Utente> {
    let utenti: array<Utente> = [];

    return {
        trova: fn(id) {
            for (u in utenti) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        salva: fn(const entita) {
            utenti.push(entita);
            return true;
        },
        elimina: fn(id) {
            // ...
            return true;
        },
        trova_tutti: fn(predicato) {
            return utenti.filter(predicato);
        }
    };
}
```

### Callback con Tipi Espliciti

```hemlock
type ClickHandler = fn(evento: MouseEvent): void;
type KeyHandler = fn(evento: KeyEvent, modificatori: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn crea_pulsante(etichetta: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Tipi Funzione Nullable

```hemlock
// Callback opzionale
fn fetch(url: string, on_completo: fn(Response): void?): void {
    let risposta = http_get(url);
    if (on_completo != null) {
        on_completo(risposta);
    }
}

// Ritorno nullable da tipo funzione
type Parser = fn(input: string): AST?;

fn prova_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let risultato = p(input);
        if (risultato != null) {
            return risultato;
        }
    }
    return null;
}
```

---

## Roadmap Implementazione

### Fase 1: Infrastruttura Core
1. Aggiungere `TYPE_FUNCTION` a enum TypeKind
2. Estendere struct Type con campi tipo funzione
3. Aggiungere `CHECKED_FUNCTION` al type checker del compilatore
4. Aggiungere supporto tipo `Self` (TYPE_SELF)

### Fase 2: Parsing
1. Implementare `parse_function_type()` nel parser
2. Gestire `fn(...)` in posizione tipo
3. Aggiungere parola chiave `type` e parsing `STMT_TYPE_ALIAS`
4. Aggiungere parsing modificatore parametro `const`
5. Estendere parsing define per firme metodo

### Fase 3: Controllo Tipi
1. Regole compatibilità tipi funzione
2. Risoluzione ed espansione alias tipo
3. Controllo mutazione parametri const
4. Validazione firme metodo in tipi define
5. Risoluzione tipo Self

### Fase 4: Runtime
1. Validazione tipo funzione ai call site
2. Rilevamento violazione const
3. Trasparenza alias tipo

### Fase 5: Test Parità
1. Test annotazione tipo funzione
2. Test composizione nullable
3. Test alias tipo
4. Test parametri const
5. Test firme metodo

---

## Decisioni di Design

### 1. Alias Tipo Generici: **SÌ**

Gli alias tipo supportano parametri generici:

```hemlock
// Alias tipo generici
type Coppia<T> = { primo: T, secondo: T };
type Risultato<T, E> = { valore: T?, errore: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Uso
let coord: Coppia<f64> = { primo: 3.14, secondo: 2.71 };
let risultato: Risultato<Utente, string> = { valore: utente, errore: null };
let trasforma: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Propagazione Const: **PROFONDA**

I parametri const sono completamente immutabili - nessuna mutazione attraverso nessun percorso:

```hemlock
fn elabora(const arr: array<object>) {
    arr.push({});        // ERRORE: non può mutare array const
    arr[0] = {};         // ERRORE: non può mutare array const
    arr[0].x = 5;        // ERRORE: non può mutare attraverso const (PROFONDO)

    let x = arr[0].x;    // OK: lettura è permessa
    let copia = arr[0];  // OK: crea una copia
    copia.x = 5;         // OK: copia non è const
}

fn annidato(const obj: object) {
    obj.utente.nome = "x"; // ERRORE: const profondo previene mutazione annidata
    obj.elementi[0] = 1;   // ERRORE: const profondo previene mutazione annidata
}
```

**Motivazione:** Const profondo fornisce garanzie più forti ed è più utile per
assicurare l'integrità dei dati. Se devi mutare dati annidati, fai prima una copia.

### 3. Self in Alias Tipo Standalone: **NO**

`Self` è valido solo dentro blocchi `define` dove ha significato chiaro:

```hemlock
// Valido: Self si riferisce al tipo definito
define Comparabile {
    fn confronta(altro: Self): i32;
}

// Non valido: Self non ha significato qui
type Clonatore = fn(Self): Self;  // ERRORE: Self fuori contesto define

// Invece, usa generici:
type Clonatore<T> = fn(T): T;
```

### 4. Implementazioni Metodo Default: **SÌ (Solo Semplici)**

Permetti implementazioni default per metodi semplici/utility:

```hemlock
define Comparabile {
    // Richiesto: deve essere implementato
    fn confronta(altro: Self): i32;

    // Implementazioni default (metodi convenience semplici)
    fn uguale(altro: Self): bool {
        return self.confronta(altro) == 0;
    }
    fn minore_di(altro: Self): bool {
        return self.confronta(altro) < 0;
    }
    fn maggiore_di(altro: Self): bool {
        return self.confronta(altro) > 0;
    }
}

define Stampabile {
    fn to_string(): string;

    // Default: delega a metodo richiesto
    fn stampa() {
        print(self.to_string());
    }
    fn stampa_ln() {
        print(self.to_string() + "\n");
    }
}

// L'oggetto deve solo implementare i metodi richiesti
let elemento: Comparabile = {
    valore: 42,
    confronta: fn(altro) { return self.valore - altro.valore; }
    // uguale, minore_di, maggiore_di sono ereditati dai default
};

elemento.minore_di({ valore: 50, confronta: elemento.confronta });  // true
```

**Linee guida per i default:**
- Mantienili semplici (1-3 righe)
- Dovrebbero delegare a metodi richiesti
- Nessuna logica complessa o effetti collaterali
- Solo primitive e composizioni dirette

### 5. Varianza: **INFERITA (Nessuna Annotazione Esplicita)**

La varianza è inferita da come sono usati i parametri tipo:

```hemlock
// La varianza è automatica in base alla posizione
type Produttore<T> = fn(): T;           // T in ritorno = covariante
type Consumatore<T> = fn(T): void;      // T in parametro = controvariante
type Trasformatore<T> = fn(T): T;       // T in entrambi = invariante

// Esempio: Cane <: Animale (Cane è sottotipo di Animale)
let produttore_cane: Produttore<Cane> = fn() { return nuovo_cane(); };
let produttore_animale: Produttore<Animale> = produttore_cane;  // OK: covariante

let consumatore_animale: Consumatore<Animale> = fn(a) { print(a); };
let consumatore_cane: Consumatore<Cane> = consumatore_animale;  // OK: controvariante
```

**Perché inferire?**
- Meno boilerplate (`<out T>` / `<in T>` aggiunge rumore)
- Segue "esplicito su implicito" - la posizione È esplicita
- Corrisponde a come la maggior parte dei linguaggi gestisce la varianza dei tipi funzione
- Gli errori sono chiari quando le regole di varianza sono violate

---

## Appendice: Modifiche Grammatica

```ebnf
(* Tipi *)
type := simple_type | compound_type | function_type
simple_type := base_type ["?"] | identifier ["<" type_args ">"] ["?"]
compound_type := simple_type ("&" simple_type)+
function_type := ["async"] "fn" "(" [param_types] ")" [":" type]

base_type := "i8" | "i16" | "i32" | "i64"
           | "u8" | "u16" | "u32" | "u64"
           | "f32" | "f64" | "bool" | "string" | "rune"
           | "ptr" | "buffer" | "void" | "null"
           | "array" ["<" type ">"]
           | "object"
           | "Self"

param_types := param_type ("," param_type)*
param_type := ["const"] [identifier ":"] ["?"] type
            | "..." [identifier] [":" type]

type_args := type ("," type)*

(* Istruzioni *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" marca metodo opzionale, block fornisce implementazione default *)

(* Parametri *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
