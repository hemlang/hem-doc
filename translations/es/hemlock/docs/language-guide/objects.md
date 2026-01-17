# Objetos

Hemlock implementa objetos estilo JavaScript con asignacion en heap, campos dinamicos, metodos y duck typing. Los objetos son estructuras de datos flexibles que combinan datos y comportamiento.

## Resumen

```hemlock
// Objeto anonimo
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// Objeto con metodos
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Literales de Objeto

### Sintaxis Basica

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**Sintaxis:**
- Llaves `{}` encierran el objeto
- Pares clave-valor separados por comas
- Las claves son identificadores (no necesitan comillas)
- Los valores pueden ser de cualquier tipo

### Objetos Vacios

```hemlock
let obj = {};  // Objeto vacio

// Agregar campos despues
obj.name = "Alice";
obj.age = 30;
```

### Objetos Anidados

```hemlock
let user = {
    info: {
        name: "Bob",
        age: 25
    },
    active: true,
    settings: {
        theme: "dark",
        notifications: true
    }
};

print(user.info.name);           // "Bob"
print(user.settings.theme);      // "dark"
```

### Tipos de Valor Mezclados

```hemlock
let mixed = {
    number: 42,
    text: "hello",
    flag: true,
    data: null,
    items: [1, 2, 3],
    config: { x: 10, y: 20 }
};
```

### Sintaxis de Propiedad Abreviada

Cuando el nombre de variable coincide con el nombre de propiedad, usa sintaxis abreviada:

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Abreviado: { name } es equivalente a { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Mezclar abreviado con propiedades regulares:**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### Operador Spread

El operador spread (`...`) copia todos los campos de un objeto a otro:

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Sobrescribir valores con spread:**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (sobrescrito)
print(custom.size);   // "medium" (de defaults)
print(custom.debug);  // false (de defaults)
```

**Multiples spreads (los posteriores sobrescriben a los anteriores):**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// El spread posterior sobrescribe al anterior
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**Combinar abreviado y spread:**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**Patron de sobrescritura de configuracion:**
```hemlock
let defaultConfig = {
    debug: false,
    timeout: 30,
    retries: 3
};

let prodConfig = { ...defaultConfig, timeout: 60 };
let devConfig = { ...defaultConfig, debug: true };

print(prodConfig.timeout);  // 60
print(devConfig.debug);     // true
```

**Nota:** Spread realiza una copia superficial. Los objetos anidados comparten referencias:
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (misma referencia que nested.inner)
```

## Acceso a Campos

### Notacion de Punto

```hemlock
let person = { name: "Alice", age: 30 };

// Leer campo
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Modificar campo
person.age = 31;
print(person.age);           // 31
```

### Adicion Dinamica de Campos

Agregar nuevos campos en tiempo de ejecucion:

```hemlock
let person = { name: "Alice" };

// Agregar nuevo campo
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Eliminacion de Campos

**Nota:** La eliminacion de campos no esta soportada actualmente. Establece a `null` en su lugar:

```hemlock
let obj = { x: 10, y: 20 };

// No se pueden eliminar campos (no soportado)
// obj.x = undefined;  // No hay 'undefined' en Hemlock

// Alternativa: Establecer a null
obj.x = null;
```

## Metodos y `self`

### Definiendo Metodos

Los metodos son funciones almacenadas en campos de objeto:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    },
    decrement: fn() {
        self.count = self.count - 1;
    },
    get: fn() {
        return self.count;
    }
};
```

### La Palabra Clave `self`

Cuando una funcion se llama como metodo, `self` se vincula automaticamente al objeto:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self se refiere a counter
    }
};

counter.increment();  // self se vincula a counter
print(counter.count);  // 1
```

**Como funciona:**
- Las llamadas a metodos se detectan verificando si la expresion de funcion es acceso a propiedad
- `self` se vincula automaticamente al objeto en el momento de la llamada
- `self` es de solo lectura (no se puede reasignar `self` en si)

### Deteccion de Llamada a Metodo

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Llamado como metodo - self se vincula
print(obj.method());  // 10

// Llamado como funcion - self es null (error)
let f = obj.method;
print(f());  // ERROR: self no esta definido
```

### Metodos con Parametros

```hemlock
let calculator = {
    result: 0,
    add: fn(x) {
        self.result = self.result + x;
    },
    multiply: fn(x) {
        self.result = self.result * x;
    },
    get: fn() {
        return self.result;
    }
};

calculator.add(5);
calculator.multiply(2);
print(calculator.get());  // 10
```

## Definiciones de Tipo con `define`

### Definicion de Tipo Basica

Define formas de objeto con `define`:

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Crear objeto y asignar a variable tipada
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Duck typing valida la estructura

print(typeof(typed_p));  // "Person"
```

**Que hace `define`:**
- Declara un tipo con campos requeridos
- Habilita validacion por duck typing
- Establece el nombre de tipo del objeto para `typeof()`

### Duck Typing

Los objetos se validan contra `define` usando **compatibilidad estructural**:

```hemlock
define Person {
    name: string,
    age: i32,
}

// OK: Tiene todos los campos requeridos
let p1: Person = { name: "Alice", age: 30 };

// OK: Campos extra estan permitidos
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// ERROR: Falta campo requerido 'age'
let p3: Person = { name: "Carol" };

// ERROR: Tipo incorrecto para 'age'
let p4: Person = { name: "Dave", age: "thirty" };
```

**Reglas de duck typing:**
- Todos los campos requeridos deben estar presentes
- Los tipos de campo deben coincidir
- Los campos extra estan permitidos y se preservan
- La validacion ocurre en el momento de la asignacion

### Campos Opcionales

Los campos pueden ser opcionales con valores por defecto:

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Opcional con valor por defecto
    nickname?: string,   // Opcional, por defecto null
}

// Objeto con solo campos requeridos
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (por defecto aplicado)
print(typed_p.nickname);  // null (sin por defecto)

// Puede sobrescribir campos opcionales
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (sobrescrito)
```

**Sintaxis de campo opcional:**
- `field?: default_value` - Opcional con valor por defecto
- `field?: type` - Opcional con anotacion de tipo, por defecto null
- Los campos opcionales se agregan durante duck typing si faltan

### Verificacion de Tipos

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // Verificacion de tipo ocurre aqui

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (el original sigue siendo anonimo)
```

**Cuando ocurre la verificacion de tipo:**
- En el momento de asignacion a variable tipada
- Valida que todos los campos requeridos esten presentes
- Valida que los tipos de campo coincidan (con conversiones implicitas)
- Establece el nombre de tipo del objeto

## Firmas de Metodo en Define

Los bloques define pueden especificar firmas de metodo, creando contratos tipo interfaz:

### Metodos Requeridos

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Firma de metodo requerida
}

// Los objetos deben proporcionar el metodo requerido
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Metodos Opcionales

```hemlock
define Serializable {
    fn serialize(): string;       // Requerido
    fn pretty?(): string;         // Metodo opcional (puede estar ausente)
}
```

### El Tipo `Self`

`Self` se refiere al tipo que se esta definiendo, habilitando definiciones de tipo recursivas:

```hemlock
define Cloneable {
    fn clone(): Self;  // Retorna el mismo tipo que el objeto
}

define Comparable {
    fn compare(other: Self): i32;  // Toma el mismo tipo como parametro
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Campos y Metodos Mezclados

```hemlock
define Entity {
    id: i32,
    name: string,
    fn validate(): bool;
    fn serialize(): string;
}

let user: Entity = {
    id: 1,
    name: "Alice",
    validate: fn() { return self.id > 0 && self.name != ""; },
    serialize: fn() { return '{"id":' + self.id + ',"name":"' + self.name + '"}'; }
};
```

## Tipos Compuestos (Tipos de Interseccion)

Los tipos compuestos usan `&` para requerir que un objeto satisfaga multiples definiciones de tipo:

### Tipos Compuestos Basicos

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Tipo compuesto: el objeto debe satisfacer TODOS los tipos
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Parametros de Funcion con Tipos Compuestos

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // Campos extra OK
```

### Tres o Mas Tipos

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Alias de Tipo para Tipos Compuestos

```hemlock
// Crear un alias nombrado para un tipo compuesto
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Duck typing con compuestos:** Los campos extra siempre estan permitidos - el objeto solo necesita tener al menos los campos requeridos por todos los tipos componentes.

## Serializacion JSON

### Serializar a JSON

Convertir objetos a cadenas JSON:

```hemlock
// obj.serialize() - Convertir objeto a cadena JSON
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Objetos anidados
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Deserializar desde JSON

Analizar cadenas JSON de vuelta a objetos:

```hemlock
// json.deserialize() - Analizar cadena JSON a objeto
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Deteccion de Ciclos

Las referencias circulares se detectan y causan errores:

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Crear referencia circular

obj.serialize();  // ERROR: serialize() detecto referencia circular
```

### Tipos Soportados

La serializacion JSON soporta:

- **Numeros**: i8-i32, u8-u32, f32, f64
- **Booleanos**: true, false
- **Cadenas**: Con secuencias de escape
- **Null**: valor null
- **Objetos**: Objetos anidados
- **Arrays**: Arrays anidados

**No soportado:**
- Funciones (omitidas silenciosamente)
- Punteros (error)
- Buffers (error)

### Manejo de Errores

La serializacion y deserializacion pueden lanzar errores:

```hemlock
// JSON invalido lanza un error
try {
    let bad = "not valid json".deserialize();
} catch (e) {
    print("Parse error:", e);
}

// Los punteros no se pueden serializar
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialize error:", e);
}
```

### Ejemplo de Ida y Vuelta

Ejemplo completo de serializar y deserializar:

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Crear y serializar
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Deserializar de vuelta
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Funciones Integradas

### `typeof(value)`

Retorna el nombre del tipo como cadena:

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Valores de retorno:**
- Objetos anonimos: `"object"`
- Objetos tipados: Nombre de tipo personalizado (ej., `"Person"`)

## Detalles de Implementacion

### Modelo de Memoria

- **Asignado en heap** - Todos los objetos se asignan en el heap
- **Copia superficial** - La asignacion copia la referencia, no el objeto
- **Campos dinamicos** - Almacenados como arrays dinamicos de pares nombre/valor
- **Conteo de referencias** - Los objetos se liberan automaticamente cuando el alcance termina

### Semantica de Referencia

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copia superficial (misma referencia)

obj2.x = 20;
print(obj1.x);  // 20 (ambos refieren al mismo objeto)
```

### Almacenamiento de Metodos

Los metodos son simplemente funciones almacenadas en campos:

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method es una funcion almacenada en obj.method
print(typeof(obj.method));  // "function"
```

## Patrones Comunes

### Patron: Funcion Constructora

```hemlock
fn createPerson(name: string, age: i32) {
    return {
        name: name,
        age: age,
        greet: fn() {
            return "Hi, I'm " + self.name;
        }
    };
}

let person = createPerson("Alice", 30);
print(person.greet());  // "Hi, I'm Alice"
```

### Patron: Constructor de Objetos

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Habilitar encadenamiento
        },

        setAge: fn(a) {
            self.age = a;
            return self;
        },

        build: fn() {
            return { name: self.name, age: self.age };
        }
    };
}

let person = PersonBuilder()
    .setName("Alice")
    .setAge(30)
    .build();
```

### Patron: Objeto de Estado

```hemlock
let state = {
    status: "idle",
    data: null,
    error: null,

    setState: fn(new_status) {
        self.status = new_status;
    },

    setData: fn(new_data) {
        self.data = new_data;
        self.status = "success";
    },

    setError: fn(err) {
        self.error = err;
        self.status = "error";
    }
};
```

### Patron: Objeto de Configuracion

```hemlock
let config = {
    defaults: {
        timeout: 30,
        retries: 3,
        debug: false
    },

    get: fn(key) {
        if (self.defaults[key] != null) {
            return self.defaults[key];
        }
        return null;
    },

    set: fn(key, value) {
        self.defaults[key] = value;
    }
};
```

## Mejores Practicas

1. **Usar `define` para estructura** - Documentar formas esperadas de objetos
2. **Preferir funciones fabrica** - Crear objetos con constructores
3. **Mantener objetos simples** - No anidar demasiado profundamente
4. **Documentar uso de `self`** - Hacer claro el comportamiento de metodos
5. **Validar en asignacion** - Usar duck typing para detectar errores temprano
6. **Evitar referencias circulares** - Causaran errores de serializacion
7. **Usar campos opcionales** - Proporcionar valores por defecto sensatos

## Errores Comunes

### Error: Referencia vs. Valor

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Copia superficial

obj2.x = 20;
print(obj1.x);  // 20 (sorpresa! ambos cambiaron)

// Para evitar: Crear nuevo objeto
let obj3 = { x: obj1.x };  // Copia profunda (manual)
```

### Error: `self` en Llamadas No-Metodo

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Funciona: Llamado como metodo
print(obj.method());  // 10

// ERROR: Llamado como funcion
let f = obj.method;
print(f());  // ERROR: self no esta definido
```

### Error: Punteros Crudos en Objetos

```hemlock
// Los objetos se liberan automaticamente, pero los punteros crudos dentro NO
fn create_objects() {
    let obj = { data: alloc(1000) };  // ptr crudo necesita free manual
    // obj se libera automaticamente cuando el alcance termina, pero obj.data tiene fuga!
}

// Solucion: Liberar punteros crudos antes de que termine el alcance
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... usar obj.data ...
    free(obj.data);  // Liberar el puntero crudo explicitamente
}  // obj en si se libera automaticamente
```

### Error: Confusion de Tipos

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// ERROR: Falta campo requerido 'y'
let p: Point = obj;
```

## Ejemplos

### Ejemplo: Matematica Vectorial

```hemlock
fn createVector(x, y) {
    return {
        x: x,
        y: y,

        add: fn(other) {
            return createVector(
                self.x + other.x,
                self.y + other.y
            );
        },

        length: fn() {
            return sqrt(self.x * self.x + self.y * self.y);
        },

        toString: fn() {
            return "(" + typeof(self.x) + ", " + typeof(self.y) + ")";
        }
    };
}

let v1 = createVector(3, 4);
let v2 = createVector(1, 2);
let v3 = v1.add(v2);

print(v3.toString());  // "(4, 6)"
```

### Ejemplo: Base de Datos Simple

```hemlock
fn createDatabase() {
    let records = [];
    let next_id = 1;

    return {
        insert: fn(data) {
            let record = { id: next_id, data: data };
            records.push(record);
            next_id = next_id + 1;
            return record.id;
        },

        find: fn(id) {
            let i = 0;
            while (i < records.length) {
                if (records[i].id == id) {
                    return records[i];
                }
                i = i + 1;
            }
            return null;
        },

        count: fn() {
            return records.length;
        }
    };
}

let db = createDatabase();
let id = db.insert({ name: "Alice", age: 30 });
let record = db.find(id);
print(record.data.name);  // "Alice"
```

### Ejemplo: Emisor de Eventos

```hemlock
fn createEventEmitter() {
    let listeners = {};

    return {
        on: fn(event, handler) {
            if (listeners[event] == null) {
                listeners[event] = [];
            }
            listeners[event].push(handler);
        },

        emit: fn(event, data) {
            if (listeners[event] != null) {
                let i = 0;
                while (i < listeners[event].length) {
                    listeners[event][i](data);
                    i = i + 1;
                }
            }
        }
    };
}

let emitter = createEventEmitter();

emitter.on("message", fn(data) {
    print("Received: " + data);
});

emitter.emit("message", "Hello!");
```

## Limitaciones

Limitaciones actuales:

- **Sin copia profunda** - Debe copiar manualmente objetos anidados (spread es superficial)
- **Sin paso por valor** - Los objetos siempre se pasan por referencia
- **Sin propiedades computadas** - Sin sintaxis `{[key]: value}`
- **`self` es de solo lectura** - No se puede reasignar `self` en metodos
- **Sin eliminacion de propiedades** - No se pueden remover campos una vez agregados

**Nota:** Los objetos tienen conteo de referencias y se liberan automaticamente cuando el alcance termina. Ver [Gestion de Memoria](memory.md#conteo-de-referencias-interno) para detalles.

## Temas Relacionados

- [Functions](functions.md) - Los metodos son funciones almacenadas en objetos
- [Arrays](arrays.md) - Los arrays tambien son tipo objeto
- [Types](types.md) - Duck typing y definiciones de tipo
- [Error Handling](error-handling.md) - Lanzar objetos de error

## Ver Tambien

- **Duck Typing**: Ver seccion "Objects" en CLAUDE.md para detalles de duck typing
- **JSON**: Ver CLAUDE.md para detalles de serializacion JSON
- **Memoria**: Ver [Memory](memory.md) para asignacion de objetos
