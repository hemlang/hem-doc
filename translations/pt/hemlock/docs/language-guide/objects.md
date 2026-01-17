# Objetos

Hemlock implementa objetos estilo JavaScript com alocação no heap, campos dinâmicos, métodos e duck typing. Objetos são estruturas de dados flexíveis que combinam dados e comportamento.

## Visão Geral

```hemlock
// Objeto anônimo
let person = { name: "Alice", age: 30, city: "NYC" };
print(person.name);  // "Alice"

// Objeto com métodos
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;
    }
};

counter.increment();
print(counter.count);  // 1
```

## Literais de Objeto

### Sintaxe Básica

```hemlock
let person = {
    name: "Alice",
    age: 30,
    city: "NYC"
};
```

**Sintaxe:**
- Chaves `{}` envolvem o objeto
- Pares chave-valor separados por vírgulas
- Chaves são identificadores (não precisam de aspas)
- Valores podem ser qualquer tipo

### Objeto Vazio

```hemlock
let obj = {};  // Objeto vazio

// Adicionar campos depois
obj.name = "Alice";
obj.age = 30;
```

### Objetos Aninhados

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

### Valores de Tipos Mistos

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

### Sintaxe de Propriedade Abreviada

Quando o nome da variável corresponde ao nome da propriedade, use sintaxe abreviada:

```hemlock
let name = "Alice";
let age = 30;
let active = true;

// Abreviado: { name } equivale a { name: name }
let person = { name, age, active };

print(person.name);   // "Alice"
print(person.age);    // 30
print(person.active); // true
```

**Misturando abreviado e propriedades regulares:**
```hemlock
let city = "NYC";
let obj = { name, age, city, role: "admin" };
```

### Operador Spread

O operador spread (`...`) copia todos os campos de um objeto para outro:

```hemlock
let base = { x: 1, y: 2 };
let extended = { ...base, z: 3 };

print(extended.x);  // 1
print(extended.y);  // 2
print(extended.z);  // 3
```

**Sobrescrevendo valores com spread:**
```hemlock
let defaults = { theme: "light", size: "medium", debug: false };
let custom = { ...defaults, theme: "dark" };

print(custom.theme);  // "dark" (sobrescrito)
print(custom.size);   // "medium" (de defaults)
print(custom.debug);  // false (de defaults)
```

**Múltiplos spreads (últimos sobrescrevem anteriores):**
```hemlock
let a = { x: 1 };
let b = { y: 2 };
let merged = { ...a, ...b, z: 3 };

print(merged.x);  // 1
print(merged.y);  // 2
print(merged.z);  // 3

// Spreads posteriores sobrescrevem anteriores
let first = { val: "first" };
let second = { val: "second" };
let combined = { ...first, ...second };
print(combined.val);  // "second"
```

**Combinando abreviado e spread:**
```hemlock
let status = "active";
let data = { id: 1, name: "Item" };
let full = { ...data, status };

print(full.id);      // 1
print(full.name);    // "Item"
print(full.status);  // "active"
```

**Padrão de sobrescrita de configuração:**
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

**Nota:** Spread executa cópia rasa. Objetos aninhados compartilham referência:
```hemlock
let nested = { inner: { val: 42 } };
let copied = { ...nested };
print(copied.inner.val);  // 42 (mesma referência que nested.inner)
```

## Acesso a Campos

### Sintaxe de Ponto

```hemlock
let person = { name: "Alice", age: 30 };

// Lendo campos
let name = person.name;      // "Alice"
let age = person.age;        // 30

// Modificando campos
person.age = 31;
print(person.age);           // 31
```

### Adição Dinâmica de Campos

Adicione novos campos em tempo de execução:

```hemlock
let person = { name: "Alice" };

// Adicionar novos campos
person.email = "alice@example.com";
person.phone = "555-1234";

print(person.email);  // "alice@example.com"
```

### Remoção de Campos

**Nota:** Remoção de campos não é suportada atualmente. Defina como `null` em vez disso:

```hemlock
let obj = { x: 10, y: 20 };

// Não pode remover campos (não suportado)
// obj.x = undefined;  // Não existe 'undefined' em Hemlock

// Alternativa: definir como null
obj.x = null;
```

## Métodos e `self`

### Definindo Métodos

Métodos são funções armazenadas em campos de objeto:

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

### Palavra-chave `self`

Quando uma função é chamada como método, `self` é automaticamente vinculado ao objeto:

```hemlock
let counter = {
    count: 0,
    increment: fn() {
        self.count = self.count + 1;  // self aponta para counter
    }
};

counter.increment();  // self vinculado a counter
print(counter.count);  // 1
```

**Como funciona:**
- Detecção de chamada de método verifica se a expressão de função é acesso a propriedade
- `self` é automaticamente vinculado ao objeto no momento da chamada
- `self` é somente leitura (não pode reatribuir `self` em si)

### Detecção de Chamada de Método

```hemlock
let obj = {
    value: 10,
    method: fn() {
        return self.value;
    }
};

// Chamado como método - self é vinculado
print(obj.method());  // 10

// Chamado como função - self é null (erro)
let f = obj.method;
print(f());  // Erro: self não definido
```

### Métodos com Parâmetros

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

## Definições de Tipo com `define`

### Definição de Tipo Básica

Use `define` para definir estrutura de objeto:

```hemlock
define Person {
    name: string,
    age: i32,
    active: bool,
}

// Criar objeto e atribuir a variável tipada
let p = { name: "Alice", age: 30, active: true };
let typed_p: Person = p;  // Duck typing valida estrutura

print(typeof(typed_p));  // "Person"
```

**O que `define` faz:**
- Declara tipo com campos obrigatórios
- Habilita validação de duck typing
- Define nome do tipo do objeto para `typeof()`

### Duck Typing

Objetos são validados contra `define` usando **compatibilidade estrutural**:

```hemlock
define Person {
    name: string,
    age: i32,
}

// Correto: tem todos os campos obrigatórios
let p1: Person = { name: "Alice", age: 30 };

// Correto: campos extras permitidos
let p2: Person = {
    name: "Bob",
    age: 25,
    city: "NYC",
    active: true
};

// Erro: falta campo obrigatório 'age'
let p3: Person = { name: "Carol" };

// Erro: tipo errado para 'age'
let p4: Person = { name: "Dave", age: "thirty" };
```

**Regras de duck typing:**
- Todos os campos obrigatórios devem estar presentes
- Tipos de campo devem corresponder
- Campos extras são permitidos e preservados
- Validação ocorre na atribuição

### Campos Opcionais

Campos podem ser opcionais com valores padrão:

```hemlock
define Person {
    name: string,
    age: i32,
    active?: true,       // Opcional com valor padrão
    nickname?: string,   // Opcional, padrão null
}

// Objeto apenas com campos obrigatórios
let p = { name: "Alice", age: 30 };
let typed_p: Person = p;

print(typed_p.active);    // true (padrão aplicado)
print(typed_p.nickname);  // null (sem padrão)

// Pode sobrescrever campos opcionais
let p2: Person = { name: "Bob", age: 25, active: false };
print(p2.active);  // false (sobrescrito)
```

**Sintaxe de campos opcionais:**
- `field?: default_value` - Opcional com valor padrão
- `field?: type` - Opcional com anotação de tipo, padrão null
- Se campo opcional estiver faltando, é adicionado durante verificação de duck typing

### Verificação de Tipo

```hemlock
define Point {
    x: i32,
    y: i32,
}

let p = { x: 10, y: 20 };
let point: Point = p;  // Verificação de tipo ocorre aqui

print(typeof(point));  // "Point"
print(typeof(p));      // "object" (objeto original ainda é anônimo)
```

**Quando verificação de tipo ocorre:**
- Na atribuição a variável tipada
- Verifica se todos os campos obrigatórios existem
- Verifica se tipos de campo correspondem (com conversão implícita)
- Define nome do tipo do objeto

## Assinaturas de Método em Define

Blocos define podem especificar assinaturas de método, criando contratos tipo interface:

### Métodos Obrigatórios

```hemlock
define Comparable {
    value: i32,
    fn compare(other: Self): i32;  // Assinatura de método obrigatória
}

// Objeto deve fornecer métodos obrigatórios
let a: Comparable = {
    value: 10,
    compare: fn(other) { return self.value - other.value; }
};
```

### Métodos Opcionais

```hemlock
define Serializable {
    fn serialize(): string;       // Obrigatório
    fn pretty?(): string;         // Método opcional (pode não existir)
}
```

### Tipo `Self`

`Self` refere-se ao tipo sendo definido, suportando definições de tipo recursivas:

```hemlock
define Cloneable {
    fn clone(): Self;  // Retorna mesmo tipo que o objeto
}

define Comparable {
    fn compare(other: Self): i32;  // Aceita mesmo tipo como parâmetro
    fn equals(other: Self): bool;
}

let item: Cloneable = {
    value: 42,
    clone: fn() {
        return { value: self.value, clone: self.clone };
    }
};
```

### Misturando Campos e Métodos

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

## Tipos Compostos (Tipos de Interseção)

Tipos compostos usam `&` para exigir que objetos satisfaçam múltiplas definições de tipo:

### Tipo Composto Básico

```hemlock
define HasName { name: string }
define HasAge { age: i32 }

// Tipo composto: objeto deve satisfazer todos os tipos
let person: HasName & HasAge = { name: "Alice", age: 30 };
```

### Parâmetros de Função com Tipos Compostos

```hemlock
fn greet(p: HasName & HasAge) {
    print(p.name + " is " + p.age);
}

greet({ name: "Bob", age: 25, city: "NYC" });  // Campos extras permitidos
```

### Três ou Mais Tipos

```hemlock
define HasEmail { email: string }

fn describe(p: HasName & HasAge & HasEmail) {
    print(p.name + " <" + p.email + ">");
}
```

### Aliases de Tipo para Tipos Compostos

```hemlock
// Criar alias nomeado para tipo composto
type Person = HasName & HasAge;
type Employee = HasName & HasAge & HasEmail;

let emp: Employee = {
    name: "Charlie",
    age: 35,
    email: "charlie@example.com"
};
```

**Duck typing de tipos compostos:** Campos extras são sempre permitidos - objetos só precisam ter pelo menos todos os campos requeridos por todos os tipos componentes.

## Serialização JSON

### Serializando para JSON

Converta objetos para string JSON:

```hemlock
// obj.serialize() - converte objeto para string JSON
let obj = { x: 10, y: 20, name: "test" };
let json = obj.serialize();
print(json);  // {"x":10,"y":20,"name":"test"}

// Objetos aninhados
let nested = { inner: { a: 1, b: 2 }, outer: 3 };
print(nested.serialize());  // {"inner":{"a":1,"b":2},"outer":3}
```

### Desserializando de JSON

Parse string JSON de volta para objeto:

```hemlock
// json.deserialize() - parse string JSON para objeto
let json_str = '{"x":10,"y":20,"name":"test"}';
let obj = json_str.deserialize();

print(obj.name);   // "test"
print(obj.x);      // 10
```

### Detecção de Referência Circular

Referências circulares são detectadas e causam erro:

```hemlock
let obj = { x: 10 };
obj.me = obj;  // Cria referência circular

obj.serialize();  // Erro: serialize() detectou referência circular
```

### Tipos Suportados

Serialização JSON suporta:

- **Números**: i8-i32, u8-u32, f32, f64
- **Booleanos**: true, false
- **Strings**: com sequências de escape
- **Null**: valor null
- **Objetos**: objetos aninhados
- **Arrays**: arrays aninhados

**Não suportados:**
- Funções (omitidas silenciosamente)
- Ponteiros (erro)
- Buffer (erro)

### Tratamento de Erros

Serialização e desserialização podem lançar erros:

```hemlock
// JSON inválido lança erro
try {
    let bad = "not valid json".deserialize();
} catch (e) {
    print("Parse error:", e);
}

// Ponteiros não podem ser serializados
let obj = { ptr: alloc(10) };
try {
    obj.serialize();
} catch (e) {
    print("Serialize error:", e);
}
```

### Exemplo de Ida e Volta

Exemplo completo de serialização e desserialização:

```hemlock
define Config {
    host: string,
    port: i32,
    debug: bool
}

// Criar e serializar
let config: Config = {
    host: "localhost",
    port: 8080,
    debug: true
};
let json = config.serialize();
print(json);  // {"host":"localhost","port":8080,"debug":true}

// Desserializar
let restored = json.deserialize();
print(restored.host);  // "localhost"
print(restored.port);  // 8080
```

## Funções Embutidas

### `typeof(value)`

Retorna nome do tipo como string:

```hemlock
let obj = { x: 10 };
print(typeof(obj));  // "object"

define Person { name: string, age: i32 }
let p: Person = { name: "Alice", age: 30 };
print(typeof(p));    // "Person"
```

**Valores de retorno:**
- Objeto anônimo: `"object"`
- Objeto tipado: nome do tipo personalizado (ex: `"Person"`)

## Detalhes de Implementação

### Modelo de Memória

- **Alocação no heap** - Todos os objetos são alocados no heap
- **Cópia rasa** - Atribuição copia referência, não objeto
- **Campos dinâmicos** - Armazenados como array dinâmico de pares nome/valor
- **Contagem de referência** - Objetos são liberados automaticamente ao sair do escopo

### Semântica de Referência

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Cópia rasa (mesma referência)

obj2.x = 20;
print(obj1.x);  // 20 (ambos apontam para mesmo objeto)
```

### Armazenamento de Métodos

Métodos são apenas funções armazenadas em campos:

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// method é uma função armazenada em obj.method
print(typeof(obj.method));  // "function"
```

## Padrões Comuns

### Padrão: Construtor

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

### Padrão: Builder de Objeto

```hemlock
fn PersonBuilder() {
    return {
        name: null,
        age: null,

        setName: fn(n) {
            self.name = n;
            return self;  // Suporta encadeamento
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

### Padrão: Objeto de Estado

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

### Padrão: Objeto de Configuração

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

## Melhores Práticas

1. **Use `define` para estruturas** - Documente formas de objeto esperadas
2. **Prefira funções de fábrica** - Use construtores para criar objetos
3. **Mantenha objetos simples** - Não aninhe muito profundamente
4. **Documente uso de `self`** - Deixe comportamento de método claro
5. **Valide na atribuição** - Use duck typing para detectar erros cedo
6. **Evite referências circulares** - Causam erros de serialização
7. **Use campos opcionais** - Forneça padrões razoáveis

## Armadilhas Comuns

### Armadilha: Referência vs Valor

```hemlock
let obj1 = { x: 10 };
let obj2 = obj1;  // Cópia rasa

obj2.x = 20;
print(obj1.x);  // 20 (inesperado! ambos mudaram)

// Evitar: criar novo objeto
let obj3 = { x: obj1.x };  // Cópia profunda (manual)
```

### Armadilha: `self` em Chamadas Não-método

```hemlock
let obj = {
    value: 10,
    method: fn() { return self.value; }
};

// Válido: chamado como método
print(obj.method());  // 10

// Erro: chamado como função
let f = obj.method;
print(f());  // Erro: self não definido
```

### Armadilha: Ponteiros Brutos em Objetos

```hemlock
// Objetos são liberados automaticamente, mas ponteiros brutos neles não
fn create_objects() {
    let obj = { data: alloc(1000) };  // Ponteiro bruto precisa de free manual
    // obj liberado automaticamente ao sair do escopo, mas obj.data vaza!
}

// Solução: libere ponteiros brutos antes de sair do escopo
fn safe_create() {
    let obj = { data: alloc(1000) };
    // ... use obj.data ...
    free(obj.data);  // Libere ponteiro bruto explicitamente
}  // obj em si é liberado automaticamente
```

### Armadilha: Confusão de Tipo

```hemlock
let obj = { x: 10 };

define Point { x: i32, y: i32 }

// Erro: falta campo obrigatório 'y'
let p: Point = obj;
```

## Exemplos

### Exemplo: Matemática Vetorial

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

### Exemplo: Banco de Dados Simples

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

### Exemplo: Emissor de Eventos

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

## Limitações

Limitações atuais:

- **Sem cópia profunda** - Deve copiar objetos aninhados manualmente (spread é cópia rasa)
- **Sem passagem por valor** - Objetos são sempre passados por referência
- **Sem propriedades computadas** - Sintaxe `{[key]: value}` não suportada
- **`self` é somente leitura** - Não pode reatribuir `self` em métodos
- **Sem remoção de propriedade** - Campos não podem ser removidos depois de adicionados

**Nota:** Objetos usam contagem de referência, sendo liberados automaticamente ao sair do escopo. Veja [Gerenciamento de Memória](memory.md#internal-reference-counting) para detalhes.

## Tópicos Relacionados

- [Funções](functions.md) - Métodos são funções armazenadas em objetos
- [Arrays](arrays.md) - Arrays também são tipo objeto
- [Tipos](types.md) - Duck typing e definições de tipo
- [Tratamento de Erros](error-handling.md) - Lançando objetos de erro

## Veja Também

- **Duck typing**: Veja seção "Objects" em CLAUDE.md para detalhes de duck typing
- **JSON**: Veja CLAUDE.md para detalhes de serialização JSON
- **Memória**: Veja [Memória](memory.md) para alocação de objetos
