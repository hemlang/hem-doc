# Plan de Prevencion de Fugas de Memoria

> Asegurar que el runtime de Hemlock este libre de fugas de memoria y mantenga su contrato con el programador.

**Fecha:** 2026-01-16
**Estado:** Completado (implementado en v1.8.3)
**Version:** 1.0

---

## Resumen Ejecutivo

La filosofia de diseno de Hemlock establece: *"Te damos las herramientas para ser seguro, pero no te obligamos a usarlas."* Esto significa que el **runtime en si** debe estar libre de fugas incluso cuando el codigo del usuario usa caracteristicas inseguras. El contrato del programador es:

1. **Las asignaciones del usuario** (`alloc`, `buffer`) son responsabilidad del programador para `free`
2. **Las asignaciones internas del runtime** (strings, arrays, objetos, clausuras) se gestionan automaticamente via conteo de referencias
3. **Los errores y excepciones** no deben fugar memoria
4. **Las tareas async** tienen semantica de propiedad clara
5. **El runtime nunca oculta asignaciones** del programador

Este plan identifica brechas en la infraestructura actual y propone mejoras sistematicas.

---

## Tabla de Contenidos

1. [Evaluacion del Estado Actual](#evaluacion-del-estado-actual)
2. [Brechas Identificadas](#brechas-identificadas)
3. [Mejoras Propuestas](#mejoras-propuestas)
4. [Estrategia de Pruebas](#estrategia-de-pruebas)
5. [Requisitos de Documentacion](#requisitos-de-documentacion)
6. [Fases de Implementacion](#fases-de-implementacion)
7. [Criterios de Exito](#criterios-de-exito)

---

## Evaluacion del Estado Actual

### Fortalezas

| Componente | Implementacion | Ubicacion |
|-----------|---------------|----------|
| Conteo de referencias | Ops atomicas con `__ATOMIC_SEQ_CST` | `src/backends/interpreter/values.c:413-550` |
| Deteccion de ciclos | VisitedSet para recorrido de grafos | `src/backends/interpreter/values.c:1345-1480` |
| Aislamiento de hilos | Copia profunda en spawn | `src/backends/interpreter/values.c:1687-1859` |
| Perfilador con deteccion de fugas | Rastreo de AllocSite | `src/backends/interpreter/profiler/` |
| Integracion ASAN | Pipeline CI con deteccion de fugas | `.github/workflows/tests.yml` |
| Soporte Valgrind | Multiples objetivos en Makefile | `Makefile:189-327` |
| Script de prueba completo | Pruebas basadas en categorias | `tests/leak_check.sh` |

### Modelo de Propiedad de Memoria Actual

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILIDAD DEL PROGRAMADOR               │
├─────────────────────────────────────────────────────────────────┤
│  alloc(size)  ────────────────────────────────►  free(ptr)      │
│  buffer(size) ────────────────────────────────►  free(buf)      │
│  aritmetica ptr ──────────────────────────────►  seguridad limites │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSABILIDAD DEL RUNTIME                   │
├─────────────────────────────────────────────────────────────────┤
│  Literales/operaciones de string ─────► refcount + auto-release │
│  Literales/operaciones de array ──────► refcount + auto-release │
│  Literales/operaciones de objeto ─────► refcount + auto-release │
│  Clausuras de funciones ──────────────► refcount + liberacion env│
│  Resultados de tareas ────────────────► liberados despues de join() │
│  Buffers de canales ──────────────────► liberados en close()    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Brechas Identificadas

### Brecha 1: Limpieza en Rutas de Error (ALTA PRIORIDAD)

**Problema:** Cuando ocurren excepciones a mitad de ejecucion, los temporales asignados pueden fugar.

**Escenario de Ejemplo:**
```hemlock
fn process_data() {
    let arr = [1, 2, 3];           // Array asignado
    let transformed = arr.map(fn(x) {
        if (x == 2) { throw "error"; }  // Excepcion lanzada
        return x * 2;
    });
    // 'transformed' parcialmente asignado, 'arr' puede no liberarse
}
```

**Estado Actual:** El manejo de excepciones del interprete desenrolla la pila de llamadas pero puede no liberar todos los temporales creados durante la evaluacion de expresiones.

### Brecha 2: Propiedad de Resultados de Tareas Desvinculadas (MEDIA PRIORIDAD)

**Problema:** `detach(task)` permite ejecucion de disparar y olvidar, pero el resultado de la tarea puede nunca recolectarse.

### Brecha 3: Semantica de Cierre vs. Drenaje de Canales (MEDIA PRIORIDAD)

**Problema:** Cuando un canal se cierra con valores en buffer restantes, esos valores deben liberarse apropiadamente.

### Brecha 4: Fuga de AST en Coalescencia Null (CORREGIDA)

**Problema:** El optimizador estaba optimizando expresiones de coalescencia null cuando el resultado era conocido en tiempo de compilacion, pero no liberaba los nodos AST descartados.

**Correccion:** Se agrego limpieza apropiada en el optimizador para liberar nodos descartados.

### Brecha 5: Granularidad de Lista de Captura de Clausuras (BAJA PRIORIDAD)

**Problema:** Las clausuras capturan toda la cadena de entorno en lugar de solo las variables referenciadas, extendiendo potencialmente los tiempos de vida innecesariamente.

### Brecha 6: Referencia Ciclica en Coordinacion Async (BAJA PRIORIDAD)

**Problema:** Tareas que referencian canales que referencian tareas podrian crear ciclos.

### Brecha 7: Documentacion de Limites de Memoria FFI (DOCUMENTACION)

**Problema:** La transferencia de propiedad a traves de limites FFI no esta formalmente documentada.

---

## Mejoras Propuestas

### Fase 1: Correcciones Criticas (Semanas 1-2)

#### 1.1 Evaluacion de Expresiones Segura ante Excepciones

**Enfoque:** Implementar una "pila de valores temporales" que rastree asignaciones durante la evaluacion de expresiones.

#### 1.2 Limpieza de Resultados de Tareas Desvinculadas

**Enfoque:** Las tareas desvinculadas liberan su propio resultado al completar.

#### 1.3 Drenaje de Canal al Cerrar

**Enfoque:** `channel_close()` y `channel_free()` deben drenar los valores restantes.

### Fase 2: Correcciones de Problemas Conocidos (Semanas 3-4)

#### 2.1 Correccion de AST de Coalescencia Null

#### 2.2 Optimizacion de Captura de Clausuras (Opcional)

### Fase 3: Endurecimiento de Infraestructura de Pruebas (Semanas 5-6)

#### 3.1 Suite de Regresion de Fugas

#### 3.2 Monitoreo Continuo de Fugas

#### 3.3 Pruebas Fuzz para Seguridad de Memoria

### Fase 4: Documentacion y Contrato (Semana 7)

#### 4.1 Documentacion de Propiedad de Memoria

---

## Fases de Implementacion

| Fase | Enfoque | Duracion | Prioridad |
|------|---------|----------|-----------|
| 1 | Correcciones criticas (excepciones, detach, canal) | 2 semanas | ALTA |
| 2 | Correcciones de problemas conocidos (coalescencia null, capturas) | 2 semanas | MEDIA |
| 3 | Infraestructura de pruebas | 2 semanas | ALTA |
| 4 | Documentacion | 1 semana | MEDIA |

---

## Criterios de Exito

### Cuantitativos

- [ ] Cero fugas reportadas por ASAN en toda la suite de pruebas
- [ ] Cero fugas reportadas por Valgrind en toda la suite de pruebas
- [ ] Linea base de fugas establecida e impuesta en CI
- [ ] 100% de las brechas identificadas abordadas o documentadas como aceptables

### Cualitativos

- [ ] Propiedad de memoria documentada en `docs/advanced/memory-ownership.md`
- [ ] Reglas de propiedad FFI documentadas
- [ ] Prueba de regresion para cada fuga corregida
- [ ] Pruebas fuzz integradas en CI

### Verificacion del Contrato del Runtime

Las siguientes garantias deben cumplirse despues de la implementacion:

1. **Sin fugas en ejecucion normal**: Ejecutar cualquier programa valido y salir normalmente no fuga memoria (interna del runtime).
2. **Sin fugas en excepciones**: Lanzar y capturar excepciones no fuga memoria.
3. **Sin fugas al completar tareas**: Las tareas completadas (unidas o desvinculadas) no fugan memoria.
4. **Sin fugas al cerrar canales**: Cerrar canales libera todos los valores en buffer.
5. **Limpieza determinista**: El orden de llamadas a destructores es predecible (LIFO para defer, topologico para objetos).

---

## Referencias

- Perfilador actual: `src/backends/interpreter/profiler/profiler.c`
- Conteo de referencias: `src/backends/interpreter/values.c:413-550`
- Gestion de tareas: `src/backends/interpreter/builtins/concurrency.c`
- Documentacion ASAN: https://clang.llvm.org/docs/AddressSanitizer.html
- Valgrind memcheck: https://valgrind.org/docs/manual/mc-manual.html
