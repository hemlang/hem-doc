# Filosofia de Diseno del Lenguaje Hemlock

> "Un lenguaje pequeno e inseguro para escribir cosas inseguras de forma segura."

Este documento captura los principios fundamentales de diseno y la filosofia de Hemlock. Lea esto primero antes de realizar cualquier cambio o adicion al lenguaje.

---

## Tabla de Contenidos

- [Identidad Central](#identidad-central)
- [Principios de Diseno](#principios-de-diseno)
- [Filosofia sobre la Seguridad](#filosofia-sobre-la-seguridad)
- [Que NO Agregar](#que-no-agregar)
- [Consideraciones Futuras](#consideraciones-futuras)
- [Reflexiones Finales](#reflexiones-finales)

---

## Identidad Central

Hemlock es un **lenguaje de scripting para sistemas** que adopta la gestion manual de memoria y el control explicito. Esta disenado para programadores que desean:

- El poder de C
- La ergonomia de los lenguajes de scripting modernos
- Concurrencia asincrona estructurada integrada
- Sin comportamientos ocultos ni magia

### Lo que Hemlock NO ES

- **Seguro en memoria** (los punteros colgantes son su responsabilidad)
- **Un reemplazo para Rust, Go o Lua**
- **Un lenguaje que oculta la complejidad**

### Lo que Hemlock SI ES

- **Explicito sobre implicito, siempre**
- **Educativo y experimental**
- **Una "capa de scripting tipo C" para trabajo de sistemas**
- **Honesto sobre las compensaciones**

---

## Principios de Diseno

### 1. Explicito Sobre Implicito

Hemlock favorece la explicitud en todas las construcciones del lenguaje. No debe haber sorpresas, ni magia, ni comportamientos ocultos.

**Malo (implicito):**
```hemlock
let x = 5  // Falta punto y coma - deberia dar error
```

**Bueno (explicito):**
```hemlock
let x = 5;
free(ptr);  // Usted lo asigno, usted lo libera
```

**Aspectos clave:**
- Los puntos y coma son obligatorios (sin insercion automatica de punto y coma)
- Sin recoleccion de basura
- Gestion manual de memoria (alloc/free)
- Las anotaciones de tipo son opcionales pero se verifican en tiempo de ejecucion
- Sin limpieza automatica de recursos (sin RAII), pero `defer` proporciona limpieza explicita

### 2. Dinamico por Defecto, Tipado por Eleccion

Cada valor tiene una etiqueta de tipo en tiempo de ejecucion, pero el sistema esta disenado para ser flexible mientras aun detecta errores.

**Inferencia de tipos:**
- Enteros pequenos (caben en i32): `42` -> `i32`
- Enteros grandes (> rango de i32): `9223372036854775807` -> `i64`
- Flotantes: `3.14` -> `f64`

**Tipado explicito cuando es necesario:**
```hemlock
let x = 42;              // i32 inferido (valor pequeno)
let y: u8 = 255;         // u8 explicito
let z = x + y;           // se promueve a i32
let big = 5000000000;    // i64 inferido (> maximo de i32)
```

**Las reglas de promocion de tipos** siguen una jerarquia clara de menor a mayor, con los flotantes siempre ganando sobre los enteros.

### 3. Lo Inseguro es una Caracteristica, No un Defecto

Hemlock no intenta prevenir todos los errores. En cambio, le proporciona las herramientas para ser seguro mientras le permite optar por comportamientos inseguros cuando es necesario.

**Ejemplos de inseguridad intencional:**
- La aritmetica de punteros puede desbordarse (responsabilidad del usuario)
- Sin verificacion de limites en `ptr` crudo (use `buffer` si desea seguridad)
- Se permiten bloqueos por doble liberacion (gestion manual de memoria)
- El sistema de tipos previene accidentes pero permite riesgos cuando es necesario

```hemlock
let p = alloc(10);
let q = p + 100;  // Muy lejos de la asignacion - permitido pero peligroso
```

**La filosofia:** El sistema de tipos debe prevenir *accidentes* pero permitir operaciones inseguras *intencionales*.

### 4. Concurrencia Estructurada de Primera Clase

La concurrencia no es una ocurrencia tardia en Hemlock. Esta integrada en el lenguaje desde la base.

**Caracteristicas clave:**
- `async`/`await` integrados en el lenguaje
- Canales para comunicacion
- `spawn`/`join`/`detach` para gestion de tareas
- Sin hilos crudos, sin bloqueos - solo estructurado
- Verdadero paralelismo multi-hilo usando hilos POSIX

**No es un bucle de eventos ni hilos verdes** - Hemlock usa hilos reales del sistema operativo para verdadero paralelismo a traves de multiples nucleos de CPU.

### 5. Sintaxis Similar a C, Poca Ceremonia

Hemlock debe resultar familiar a los programadores de sistemas mientras reduce el codigo repetitivo.

**Decisiones de diseno:**
- Bloques `{}` siempre, sin llaves opcionales
- Los operadores coinciden con C: `+`, `-`, `*`, `/`, `&&`, `||`, `!`
- Sintaxis de tipos coincide con Rust/TypeScript: `let x: type = value;`
- Las funciones son valores de primera clase
- Palabras clave y formas especiales minimas

---

## Filosofia sobre la Seguridad

**La postura de Hemlock sobre la seguridad:**

> "Le damos las herramientas para ser seguro (`buffer`, anotaciones de tipo, verificacion de limites) pero no le obligamos a usarlas (`ptr`, memoria manual, operaciones inseguras).
>
> El valor predeterminado debe guiar hacia la seguridad, pero la escotilla de escape siempre debe estar disponible."

### Herramientas de Seguridad Proporcionadas

**1. Tipo buffer seguro:**
```hemlock
let b: buffer = buffer(64);
b[0] = 65;              // con verificacion de limites
print(b.length);        // 64
free(b);                // aun manual
```

**2. Punteros crudos inseguros:**
```hemlock
let p: ptr = alloc(64);
memset(p, 0, 64);
free(p);  // Debe recordar liberar
```

**3. Anotaciones de tipo:**
```hemlock
let x: u8 = 255;   // OK
let y: u8 = 256;   // ERROR: fuera de rango
```

**4. Verificacion de tipos en tiempo de ejecucion:**
```hemlock
let val = some_function();
if (typeof(val) == "i32") {
    // Seguro de usar como entero
}
```

### Principios Guia

1. **Usar patrones seguros por defecto en la documentacion** - Mostrar `buffer` antes de `ptr`, fomentar anotaciones de tipo
2. **Hacer obvias las operaciones inseguras** - La aritmetica de punteros crudos debe parecer intencional
3. **Proporcionar escotillas de escape** - No prevenir que usuarios experimentados hagan trabajo de bajo nivel
4. **Ser honesto sobre las compensaciones** - Documentar que puede salir mal

### Ejemplos de Seguridad vs. Inseguridad

| Patron Seguro | Patron Inseguro | Cuando Usar Inseguro |
|---------------|-----------------|---------------------|
| Tipo `buffer` | Tipo `ptr` | FFI, codigo critico para rendimiento |
| Anotaciones de tipo | Sin anotaciones | Interfaces externas, validacion |
| Acceso con verificacion de limites | Aritmetica de punteros | Operaciones de memoria de bajo nivel |
| Manejo de excepciones | Retornar null/codigos de error | Cuando las excepciones son muy pesadas |

---

## Que NO Agregar

Entender que **no** agregar es tan importante como saber que agregar.

### No Agregar Comportamiento Implicito

**Malos ejemplos:**

```hemlock
// MALO: Insercion automatica de punto y coma
let x = 5
let y = 10

// MALO: Conversiones de tipo implicitas que pierden precision
let x: i32 = 3.14  // ¿Deberia truncar o dar error?
```

**Por que:** El comportamiento implicito crea sorpresas y hace que el codigo sea mas dificil de razonar.

### No Ocultar la Complejidad

**Malos ejemplos:**

```hemlock
// MALO: Optimizacion magica detras de escena
let arr = [1, 2, 3]  // ¿Esta en la pila o en el heap? ¡El usuario debe saberlo! (Heap, con conteo de referencias)

// MALO: Puntero crudo auto-liberado
let p = alloc(100)  // ¿Se auto-libera? ¡NO! Los ptrs crudos siempre necesitan free()
```

**Nota sobre conteo de referencias:** Hemlock usa conteo de referencias interno para strings, arrays, objetos y buffers - estos SI se auto-liberan cuando el ambito termina. Esto es explicito y predecible (limpieza determinista cuando la referencia llega a 0, sin pausas de GC). Los punteros crudos (`ptr` de `alloc()`) NO tienen conteo de referencias y siempre requieren `free()` manual.

**Por que:** La complejidad oculta hace imposible predecir el rendimiento y depurar problemas.

### No Romper la Semantica Existente

**Nunca cambiar estas decisiones fundamentales:**
- Los puntos y coma son obligatorios - no hacerlos opcionales
- Gestion manual de memoria - no agregar GC
- Strings mutables - no hacerlos inmutables
- Verificacion de tipos en tiempo de ejecucion - no eliminarla

**Por que:** La consistencia y estabilidad son mas importantes que las caracteristicas de moda.

### No Agregar Caracteristicas "Convenientes" que Reducen la Explicitud

**Ejemplos de caracteristicas a evitar:**
- Sobrecarga de operadores (quizas para tipos de usuario, pero con cuidado)
- Coercion de tipos implicita que pierde informacion
- Limpieza automatica de recursos (RAII)
- Encadenamiento de metodos que oculta complejidad
- DSLs y sintaxis magica

**Excepcion:** Las caracteristicas de conveniencia estan bien si son **azucar explicito** sobre operaciones simples:
- `else if` esta bien (son solo sentencias if anidadas)
- La interpolacion de strings podria estar bien si es claramente azucar sintactico
- La sintaxis de metodos para objetos esta bien (es explicito lo que hace)

---

## Consideraciones Futuras

### Quizas Agregar (En Discusion)

Estas caracteristicas se alinean con la filosofia de Hemlock pero necesitan diseno cuidadoso:

**1. Coincidencia de patrones**
```hemlock
match (value) {
    case i32: print("entero");
    case string: print("texto");
    case _: print("otro");
}
```
- Verificacion de tipos explicita
- Sin costos ocultos
- Posible verificacion de exhaustividad en tiempo de compilacion

**2. Tipos de error (`Result<T, E>`)**
```hemlock
fn divide(a: i32, b: i32): Result<i32, string> {
    if (b == 0) {
        return Err("division por cero");
    }
    return Ok(a / b);
}
```
- Manejo de errores explicito
- Obliga a los usuarios a pensar en los errores
- Alternativa a las excepciones

**3. Tipos de array/slice**
- Ya tenemos arrays dinamicos
- Podriamos agregar arrays de tamano fijo para asignacion en pila
- Necesitaria ser explicito sobre pila vs. heap

**4. Herramientas mejoradas de seguridad de memoria**
- Bandera opcional de verificacion de limites
- Deteccion de fugas de memoria en compilaciones de depuracion
- Integracion con sanitizadores

### Probablemente Nunca Agregar

Estas caracteristicas violan los principios fundamentales:

**1. Recoleccion de basura**
- Oculta la complejidad de gestion de memoria
- Rendimiento impredecible
- Contra el principio de control explicito

**2. Gestion automatica de memoria**
- Mismas razones que GC
- El conteo de referencias podria estar bien si es explicito

**3. Conversiones de tipo implicitas que pierden datos**
- Va contra "explicito sobre implicito"
- Fuente de errores sutiles

**4. Macros (complejas)**
- Demasiado poder, demasiada complejidad
- Un sistema de macros simple podria estar bien
- Preferir generacion de codigo o funciones

**5. POO basada en clases con herencia**
- Demasiado comportamiento implicito
- El duck typing y los objetos son suficientes
- Composicion sobre herencia

**6. Sistema de modulos con resolucion compleja**
- Mantener las importaciones simples y explicitas
- Sin rutas de busqueda magicas
- Sin resolucion de versiones (usar el gestor de paquetes del SO)

---

## Reflexiones Finales

### Confianza y Responsabilidad

Hemlock trata sobre **confianza y responsabilidad**. Confiamos en que el programador:

- Gestione la memoria correctamente
- Use los tipos apropiadamente
- Maneje los errores adecuadamente
- Entienda las compensaciones

A cambio, Hemlock proporciona:

- Sin costos ocultos
- Sin comportamiento sorpresa
- Control total cuando es necesario
- Herramientas de seguridad cuando se desean

### La Pregunta Guia

**Al considerar una nueva caracteristica, pregunte:**

> "¿Esto le da al programador mas control explicito, o oculta algo?"

- Si **agrega control explicito** -> probablemente encaja en Hemlock
- Si **oculta complejidad** -> probablemente no pertenece
- Si es **azucar opcional** que esta claramente documentado -> podria estar bien

### Ejemplos de Buenas Adiciones

Sentencias switch - Flujo de control explicito, sin magia, semantica clara

Async/await con pthreads - Concurrencia explicita, verdadero paralelismo, el usuario controla el spawn

Tipo buffer junto con ptr - Da eleccion entre seguro e inseguro

Anotaciones de tipo opcionales - Ayuda a detectar errores sin forzar rigidez

Try/catch/finally - Manejo de errores explicito con flujo de control claro

### Ejemplos de Malas Adiciones

Insercion automatica de punto y coma - Oculta errores de sintaxis, hace el codigo ambiguo

RAII/destructores - La limpieza automatica oculta cuando se liberan los recursos

Coalescencia null implicita - Oculta verificaciones de null, hace el codigo mas dificil de razonar

Strings auto-crecientes - Oculta asignacion de memoria, rendimiento impredecible

---

## Conclusion

Hemlock no intenta ser el lenguaje mas seguro, el lenguaje mas rapido, o el lenguaje con mas caracteristicas.

**Hemlock intenta ser el lenguaje mas *honesto*.**

Le dice exactamente lo que esta haciendo, le da control cuando lo necesita, y no oculta los bordes afilados. Es un lenguaje para personas que quieren entender su codigo a bajo nivel mientras aun disfrutan de ergonomia moderna.

Si no esta seguro de si una caracteristica pertenece a Hemlock, recuerde:

> **Explicito sobre implicito, siempre.**
> **Lo inseguro es una caracteristica, no un defecto.**
> **El usuario es responsable, y eso esta bien.**
