# Diseno de Sintaxis de Firmas

> Extendiendo el sistema de tipos de Hemlock con tipos de funcion, modificadores nullables, alias de tipos, parametros const y firmas de metodos.

**Estado:** Implementado (v1.7.0)
**Version:** 1.0
**Autor:** Claude

---

## Vision General

Este documento propone cinco extensiones interconectadas del sistema de tipos que se construyen sobre la infraestructura existente de Hemlock:

1. **Anotaciones de Tipos de Funcion** - Tipos de funcion de primera clase
2. **Modificadores de Tipo Nullable** - Manejo explicito de null (extiende la bandera `nullable` existente)
3. **Alias de Tipos** - Abreviaciones de tipos con nombre
4. **Parametros Const** - Contratos de inmutabilidad
5. **Firmas de Metodos en Define** - Comportamiento similar a interfaces

Estas caracteristicas comparten la filosofia: **explicito sobre implicito, opcional pero aplicado cuando se usa**.

---

## 1. Anotaciones de Tipos de Funcion

### Motivacion

Actualmente, no hay forma de expresar la firma de una funcion como un tipo:

```hemlock
// Actual: callback no tiene informacion de tipo
fn map(arr: array, callback) { ... }

// Propuesto: tipo de funcion explicito
fn map(arr: array, callback: fn(any, i32): any): array { ... }
```

### Sintaxis

```hemlock
// Tipo de funcion basico
fn(i32, i32): i32

// Con nombres de parametros (solo documentacion, no se aplica)
fn(a: i32, b: i32): i32

// Sin valor de retorno (void)
fn(string): void
fn(string)              // Abreviatura: omitir `: void`

// Retorno nullable
fn(i32): string?

// Parametros opcionales
fn(name: string, age?: i32): void

// Parametros rest
fn(...args: array): i32

// Sin parametros
fn(): bool

// Orden superior: funcion que retorna funcion
fn(i32): fn(i32): i32

// Tipo de funcion async
async fn(i32): i32
```

### Ejemplos de Uso

```hemlock
// Variable con tipo de funcion
let add: fn(i32, i32): i32 = fn(a, b) { return a + b; };

// Parametro de funcion
fn apply(f: fn(i32): i32, x: i32): i32 {
    return f(x);
}

// El tipo de retorno es una funcion
fn make_adder(n: i32): fn(i32): i32 {
    return fn(x) { return x + n; };
}

// Array de funciones
let ops: array<fn(i32, i32): i32> = [add, subtract, multiply];

// Campo de objeto
define EventHandler {
    name: string;
    callback: fn(Event): void;
}
```

### Cambios en el AST

```c
// En enum TypeKind (include/ast.h)
typedef enum {
    // ... tipos existentes ...
    TYPE_FUNCTION,      // NUEVO: Tipo de funcion
} TypeKind;

// En struct Type (include/ast.h)
struct Type {
    TypeKind kind;
    // ... campos existentes ...

    // Para TYPE_FUNCTION:
    struct Type **param_types;      // Tipos de parametros
    char **param_names;             // Nombres de parametros opcionales (docs)
    int *param_optional;            // Cuales parametros son opcionales
    int num_params;
    char *rest_param_name;          // Nombre de parametro rest o NULL
    struct Type *rest_param_type;   // Tipo de parametro rest
    struct Type *return_type;       // Tipo de retorno (NULL = void)
    int is_async;                   // tipo fn async
};
```

### Parsing

Los tipos de funcion comienzan con `fn` (o `async fn`) seguido de lista de parametros:

```
function_type := ["async"] "fn" "(" [param_type_list] ")" [":" type]
param_type_list := param_type ("," param_type)*
param_type := [identifier ":"] ["?"] type | "..." [identifier] [":" type]
```

**Desambiguacion:** Al parsear un tipo y encontrar `fn`:
- Si va seguido de `(`, es un tipo de funcion
- De lo contrario, error de sintaxis (`fn` solo no es un tipo valido)

### Compatibilidad de Tipos

```hemlock
// Se requiere coincidencia exacta para tipos de funcion
let f: fn(i32): i32 = fn(x: i32): i32 { return x; };  // OK

// Contravarianza de parametros (aceptar tipos mas amplios esta bien)
let g: fn(any): i32 = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// Covarianza de retorno (retornar tipos mas estrechos esta bien)
let h: fn(i32): any = fn(x: i32): i32 { return x; };  // OK: i32 <: any

// La aridad debe coincidir
let bad: fn(i32): i32 = fn(a, b) { return a; };       // ERROR: aridad no coincide

// Parametros opcionales compatibles con requeridos
let opt: fn(i32, i32?): i32 = fn(a, b?: 0) { return a + b; };  // OK
```

---

## 2. Modificadores de Tipo Nullable

### Motivacion

El sufijo `?` hace explicita la aceptacion de null en las firmas:

```hemlock
// Actual: no esta claro si null es valido
fn find(arr: array, val: any): i32 { ... }

// Propuesto: retorno nullable explicito
fn find(arr: array, val: any): i32? { ... }
```

### Sintaxis

```hemlock
// Tipos nullables con sufijo ?
string?           // string o null
i32?              // i32 o null
User?             // User o null
array<i32>?       // array o null
fn(i32): i32?     // funcion que retorna i32 o null

// Composicion con tipos de funcion
fn(string?): i32          // Acepta string o null
fn(string): i32?          // Retorna i32 o null
fn(string?): i32?         // Ambos nullables

// En define
define Result {
    value: any?;
    error: string?;
}
```

### Notas de Implementacion

**Ya existe:** La bandera `Type.nullable` ya esta en el AST. Esta caracteristica principalmente necesita:
1. Soporte del parser para sufijo `?` en cualquier tipo (verificar/extender)
2. Composicion adecuada con tipos de funcion
3. Aplicacion en tiempo de ejecucion

### Compatibilidad de Tipos

```hemlock
// No-nullable asignable a nullable
let x: i32? = 42;           // OK
let y: i32? = null;         // OK

// Nullable NO asignable a no-nullable
let z: i32 = x;             // ERROR: x podria ser null

// Coalescencia null para desenvolver
let z: i32 = x ?? 0;        // OK: ?? proporciona valor por defecto

// Encadenamiento opcional retorna nullable
let name: string? = user?.name;
```

---

## 3. Alias de Tipos

### Motivacion

Los tipos complejos se benefician de abreviaciones con nombre:

```hemlock
// Actual: tipos compuestos repetitivos
fn process(entity: HasName & HasId & HasTimestamp) { ... }
fn validate(entity: HasName & HasId & HasTimestamp) { ... }

// Propuesto: alias con nombre
type Entity = HasName & HasId & HasTimestamp;
fn process(entity: Entity) { ... }
fn validate(entity: Entity) { ... }
```

### Sintaxis

```hemlock
// Alias basico
type Integer = i32;
type Text = string;

// Alias de tipo compuesto
type Entity = HasName & HasId;
type Auditable = HasCreatedAt & HasUpdatedAt & HasCreatedBy;

// Alias de tipo de funcion
type Callback = fn(Event): void;
type Predicate = fn(any): bool;
type Reducer = fn(acc: any, val: any): any;
type AsyncTask = async fn(): any;

// Alias nullable
type OptionalString = string?;

// Alias generico (si soportamos alias de tipos genericos)
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };

// Alias de tipo array
type IntArray = array<i32>;
type Matrix = array<array<f64>>;
```

### Alcance y Visibilidad

```hemlock
// Alcance de modulo por defecto
type Callback = fn(Event): void;

// Exportable
export type Handler = fn(Request): Response;

// En otro archivo
import { Handler } from "./handlers.hml";
fn register(h: Handler) { ... }
```

### Cambios en el AST

```c
// Nuevo tipo de sentencia
typedef enum {
    // ... sentencias existentes ...
    STMT_TYPE_ALIAS,    // NUEVO
} StmtKind;

// En union Stmt
struct {
    char *name;                 // Nombre del alias
    char **type_params;         // Parametros genericos: <T, U>
    int num_type_params;
    Type *aliased_type;         // El tipo real
} type_alias;
```

### Parsing

```
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"
```

**Nota:** `type` es una nueva palabra clave. Verificar conflictos con identificadores existentes.

### Resolucion

Los alias de tipos se resuelven en:
- **Tiempo de parsing:** Alias registrado en entorno de tipos
- **Tiempo de verificacion:** Alias expandido al tipo subyacente
- **Tiempo de ejecucion:** Alias es transparente (igual que el tipo subyacente)

```hemlock
type MyInt = i32;
let x: MyInt = 42;
typeof(x);           // "i32" (no "MyInt")
```

---

## 4. Parametros Const

### Motivacion

Senalar la intencion de inmutabilidad en firmas de funcion:

```hemlock
// Actual: no esta claro si el array se modificara
fn print_all(items: array) { ... }

// Propuesto: contrato de inmutabilidad explicito
fn print_all(const items: array) { ... }
```

### Sintaxis

```hemlock
// Parametro const
fn process(const data: buffer) {
    // data[0] = 0;        // ERROR: no puede mutar const
    let x = data[0];       // OK: lectura permitida
    return x;
}

// Multiples parametros const
fn compare(const a: array, const b: array): bool { ... }

// Mezcla de const y mutable
fn update(const source: array, target: array) {
    for (item in source) {
        target.push(item);   // OK: target es mutable
    }
}

// Const con inferencia de tipos
fn log(const msg) {
    print(msg);
}

// Const en tipos de funcion
type Reader = fn(const buffer): i32;
```

### Que Previene Const

```hemlock
fn bad(const arr: array) {
    arr.push(1);         // ERROR: metodo mutante
    arr.pop();           // ERROR: metodo mutante
    arr[0] = 5;          // ERROR: asignacion por indice
    arr.clear();         // ERROR: metodo mutante
}

fn ok(const arr: array) {
    let x = arr[0];      // OK: lectura
    let len = len(arr);  // OK: verificacion de longitud
    let copy = arr.slice(0, 10);  // OK: crea nuevo array
    for (item in arr) {  // OK: iteracion
        print(item);
    }
}
```

### Metodos Mutantes vs No-Mutantes

| Tipo | Mutante (bloqueado por const) | No-Mutante (permitido) |
|------|------------------------------|------------------------|
| array | push, pop, shift, unshift, insert, remove, clear, reverse (in-place) | slice, concat, map, filter, find, contains, first, last, join |
| string | asignacion por indice (`s[0] = 'x'`) | todos los metodos (retornan nuevos strings) |
| buffer | asignacion por indice, memset, memcpy (hacia) | lectura por indice, slice |
| object | asignacion de campo | lectura de campo |

### Cambios en el AST

```c
// En expresion de funcion (include/ast.h)
struct {
    // ... campos existentes ...
    int *param_is_const;    // NUEVO: 1 si es const, 0 en caso contrario
} function;

// En struct Type para tipos de funcion
struct Type {
    // ... campos existentes ...
    int *param_is_const;    // Para TYPE_FUNCTION
};
```

### Aplicacion

**Interprete:**
- Rastrear estado const en vinculaciones de variables
- Verificar antes de operaciones de mutacion
- Error en tiempo de ejecucion por violacion de const

**Compilador:**
- Emitir variables C calificadas con const donde sea beneficioso
- Analisis estatico para violaciones de const
- Advertencia/error en tiempo de compilacion

---

## 5. Firmas de Metodos en Define

### Motivacion

Permitir que los bloques `define` especifiquen metodos esperados, no solo campos de datos:

```hemlock
// Actual: solo campos de datos
define User {
    name: string;
    age: i32;
}

// Propuesto: firmas de metodos
define Comparable {
    fn compare(other: Self): i32;
}

define Serializable {
    fn serialize(): string;
    fn deserialize(data: string): Self;  // Metodo estatico
}
```

### Sintaxis

```hemlock
// Firma de metodo (sin cuerpo)
define Hashable {
    fn hash(): i32;
}

// Multiples metodos
define Collection {
    fn size(): i32;
    fn is_empty(): bool;
    fn contains(item: any): bool;
}

// Campos y metodos mezclados
define Entity {
    id: i32;
    name: string;
    fn validate(): bool;
    fn serialize(): string;
}

// Usando tipo Self
define Cloneable {
    fn clone(): Self;
}

define Comparable {
    fn compare(other: Self): i32;
    fn equals(other: Self): bool;
}

// Metodos opcionales
define Printable {
    fn to_string(): string;
    fn debug_string?(): string;  // Metodo opcional (puede estar ausente)
}

// Metodos con implementaciones por defecto
define Ordered {
    fn compare(other: Self): i32;  // Requerido

    // Implementaciones por defecto (heredadas si no se sobrescriben)
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
}
```

### El Tipo `Self`

`Self` se refiere al tipo concreto que implementa la interfaz:

```hemlock
define Addable {
    fn add(other: Self): Self;
}

// Cuando se usa:
let a: Addable = {
    value: 10,
    add: fn(other) {
        return { value: self.value + other.value, add: self.add };
    }
};
```

### Tipado Estructural (Duck Typing)

Las firmas de metodos usan el mismo duck typing que los campos:

```hemlock
define Stringifiable {
    fn to_string(): string;
}

// Cualquier objeto con metodo to_string() satisface Stringifiable
let x: Stringifiable = {
    name: "test",
    to_string: fn() { return self.name; }
};

// Tipos compuestos con metodos
define Named { name: string; }
define Printable { fn to_string(): string; }

type NamedPrintable = Named & Printable;

let y: NamedPrintable = {
    name: "Alice",
    to_string: fn() { return "Name: " + self.name; }
};
```

### Cambios en el AST

```c
// Extender define_object en union Stmt
struct {
    char *name;
    char **type_params;
    int num_type_params;

    // Campos (existentes)
    char **field_names;
    Type **field_types;
    int *field_optional;
    Expr **field_defaults;
    int num_fields;

    // Metodos (NUEVO)
    char **method_names;
    Type **method_types;        // TYPE_FUNCTION
    int *method_optional;       // Metodos opcionales (fn name?(): type)
    Expr **method_defaults;     // Implementaciones por defecto (NULL si solo firma)
    int num_methods;
} define_object;
```

### Verificacion de Tipos

Al verificar `value: InterfaceType`:
1. Verificar que todos los campos requeridos existen con tipos compatibles
2. Verificar que todos los metodos requeridos existen con firmas compatibles
3. Campos/metodos opcionales pueden estar ausentes

```hemlock
define Sortable {
    fn compare(other: Self): i32;
}

// Valido: tiene metodo compare
let valid: Sortable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};

// Invalido: falta compare
let invalid: Sortable = { value: 10 };  // ERROR: falta metodo 'compare'

// Invalido: firma incorrecta
let wrong: Sortable = {
    compare: fn() { return 0; }  // ERROR: se esperaba (Self): i32
};
```

---

## Ejemplos de Interaccion

### Combinando Todas las Caracteristicas

```hemlock
// Alias de tipo para tipo de funcion complejo
type EventCallback = fn(event: Event, context: Context?): bool;

// Alias de tipo para interfaz compuesta
type Entity = HasId & HasName & Serializable;

// Define con firmas de metodos
define Repository<T> {
    fn find(id: i32): T?;
    fn save(const entity: T): bool;
    fn delete(id: i32): bool;
    fn find_all(predicate: fn(T): bool): array<T>;
}

// Usando todo junto
fn create_user_repo(): Repository<User> {
    let users: array<User> = [];

    return {
        find: fn(id) {
            for (u in users) {
                if (u.id == id) { return u; }
            }
            return null;
        },
        save: fn(const entity) {
            users.push(entity);
            return true;
        },
        delete: fn(id) {
            // ...
            return true;
        },
        find_all: fn(predicate) {
            return users.filter(predicate);
        }
    };
}
```

### Callbacks con Tipos Explicitos

```hemlock
type ClickHandler = fn(event: MouseEvent): void;
type KeyHandler = fn(event: KeyEvent, modifiers: i32): bool;

define Widget {
    x: i32;
    y: i32;
    on_click: ClickHandler?;
    on_key: KeyHandler?;
}

fn create_button(label: string, handler: ClickHandler): Widget {
    return {
        x: 0, y: 0,
        on_click: handler,
        on_key: null
    };
}
```

### Tipos de Funcion Nullables

```hemlock
// Callback opcional
fn fetch(url: string, on_complete: fn(Response): void?): void {
    let response = http_get(url);
    if (on_complete != null) {
        on_complete(response);
    }
}

// Retorno nullable de tipo de funcion
type Parser = fn(input: string): AST?;

fn try_parse(parsers: array<Parser>, input: string): AST? {
    for (p in parsers) {
        let result = p(input);
        if (result != null) {
            return result;
        }
    }
    return null;
}
```

---

## Hoja de Ruta de Implementacion

### Fase 1: Infraestructura Central
1. Agregar `TYPE_FUNCTION` al enum TypeKind
2. Extender struct Type con campos de tipo de funcion
3. Agregar `CHECKED_FUNCTION` al verificador de tipos del compilador
4. Agregar soporte de tipo `Self` (TYPE_SELF)

### Fase 2: Parsing
1. Implementar `parse_function_type()` en el parser
2. Manejar `fn(...)` en posicion de tipo
3. Agregar palabra clave `type` y parsing de `STMT_TYPE_ALIAS`
4. Agregar parsing de modificador de parametro `const`
5. Extender parsing de define para firmas de metodos

### Fase 3: Verificacion de Tipos
1. Reglas de compatibilidad de tipos de funcion
2. Resolucion y expansion de alias de tipos
3. Verificacion de mutacion de parametros const
4. Validacion de firmas de metodos en tipos define
5. Resolucion de tipo Self

### Fase 4: Runtime
1. Validacion de tipo de funcion en sitios de llamada
2. Deteccion de violacion de const
3. Transparencia de alias de tipos

### Fase 5: Pruebas de Paridad
1. Pruebas de anotacion de tipos de funcion
2. Pruebas de composicion nullable
3. Pruebas de alias de tipos
4. Pruebas de parametros const
5. Pruebas de firmas de metodos

---

## Decisiones de Diseno

### 1. Alias de Tipos Genericos: **SI**

Los alias de tipos soportan parametros genericos:

```hemlock
// Alias de tipos genericos
type Pair<T> = { first: T, second: T };
type Result<T, E> = { value: T?, error: E? };
type Mapper<T, U> = fn(T): U;
type AsyncResult<T> = async fn(): T?;

// Uso
let coords: Pair<f64> = { first: 3.14, second: 2.71 };
let result: Result<User, string> = { value: user, error: null };
let transform: Mapper<i32, string> = fn(n) { return n.to_string(); };
```

### 2. Propagacion de Const: **PROFUNDA**

Los parametros const son completamente inmutables - sin mutacion a traves de ninguna ruta:

```hemlock
fn process(const arr: array<object>) {
    arr.push({});        // ERROR: no puede mutar array const
    arr[0] = {};         // ERROR: no puede mutar array const
    arr[0].x = 5;        // ERROR: no puede mutar a traves de const (PROFUNDO)

    let x = arr[0].x;    // OK: leer esta bien
    let copy = arr[0];   // OK: crea una copia
    copy.x = 5;          // OK: copy no es const
}

fn nested(const obj: object) {
    obj.user.name = "x"; // ERROR: const profundo previene mutacion anidada
    obj.items[0] = 1;    // ERROR: const profundo previene mutacion anidada
}
```

**Justificacion:** Const profundo proporciona garantias mas fuertes y es mas util para
asegurar integridad de datos. Si necesita mutar datos anidados, haga una copia primero.

### 3. Self en Alias de Tipos Independientes: **NO**

`Self` solo es valido dentro de bloques `define` donde tiene un significado claro:

```hemlock
// Valido: Self se refiere al tipo definido
define Comparable {
    fn compare(other: Self): i32;
}

// Invalido: Self no tiene significado aqui
type Cloner = fn(Self): Self;  // ERROR: Self fuera de contexto define

// En su lugar, usar genericos:
type Cloner<T> = fn(T): T;
```

### 4. Implementaciones por Defecto de Metodos: **SI (Solo Simples)**

Permitir implementaciones por defecto para metodos simples/utilitarios:

```hemlock
define Comparable {
    // Requerido: debe ser implementado
    fn compare(other: Self): i32;

    // Implementaciones por defecto (metodos de conveniencia simples)
    fn equals(other: Self): bool {
        return self.compare(other) == 0;
    }
    fn less_than(other: Self): bool {
        return self.compare(other) < 0;
    }
    fn greater_than(other: Self): bool {
        return self.compare(other) > 0;
    }
}

define Printable {
    fn to_string(): string;

    // Por defecto: delega al metodo requerido
    fn print() {
        print(self.to_string());
    }
    fn println() {
        print(self.to_string() + "\n");
    }
}

// El objeto solo necesita implementar metodos requeridos
let item: Comparable = {
    value: 42,
    compare: fn(other) { return self.value - other.value; }
    // equals, less_than, greater_than se heredan de los valores por defecto
};

item.less_than({ value: 50, compare: item.compare });  // true
```

**Directrices para valores por defecto:**
- Mantenerlos simples (1-3 lineas)
- Deben delegar a metodos requeridos
- Sin logica compleja ni efectos secundarios
- Solo primitivas y composiciones directas

### 5. Varianza: **INFERIDA (Sin Anotaciones Explicitas)**

La varianza se infiere de como se usan los parametros de tipo:

```hemlock
// La varianza es automatica basada en posicion
type Producer<T> = fn(): T;           // T en retorno = covariante
type Consumer<T> = fn(T): void;       // T en parametro = contravariante
type Transformer<T> = fn(T): T;       // T en ambos = invariante

// Ejemplo: Dog <: Animal (Dog es subtipo de Animal)
let dog_producer: Producer<Dog> = fn() { return new_dog(); };
let animal_producer: Producer<Animal> = dog_producer;  // OK: covariante

let animal_consumer: Consumer<Animal> = fn(a) { print(a); };
let dog_consumer: Consumer<Dog> = animal_consumer;     // OK: contravariante
```

**¿Por que inferir?**
- Menos codigo repetitivo (`<out T>` / `<in T>` agrega ruido)
- Sigue "explicito sobre implicito" - la posicion ES explicita
- Coincide con como la mayoria de los lenguajes manejan la varianza de tipos de funcion
- Los errores son claros cuando se violan las reglas de varianza

---

## Apendice: Cambios en la Gramatica

```ebnf
(* Tipos *)
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

(* Sentencias *)
type_alias := "type" identifier ["<" type_params ">"] "=" type ";"

define_stmt := "define" identifier ["<" type_params ">"] "{" define_members "}"
define_members := (field_def | method_def)*
field_def := identifier (":" type ["=" expr] | "?:" (type | expr)) ";"?
method_def := "fn" identifier ["?"] "(" [param_types] ")" [":" type] (block | ";")
            (* "?" marca metodo opcional, block proporciona implementacion por defecto *)

(* Parametros *)
param := ["const"] ["ref"] identifier [":" type] ["?:" expr]
       | "..." identifier [":" type]
```
