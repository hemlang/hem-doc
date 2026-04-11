# Propuesta: `@stdlib/vector` — Modulo de Busqueda de Similitud Vectorial

**Estado:** Exploracion / RFC
**Fecha:** 2026-02-07

---

## Resumen

Agregar un modulo `@stdlib/vector` que proporcione busqueda de similitud vectorial en proceso (busqueda de vecinos mas cercanos). Esto habilita busqueda basada en embeddings, sistemas de recomendacion y flujos de trabajo de IA/ML directamente desde Hemlock sin requerir un servidor externo.

---

## Opciones Evaluadas

Se evaluaron diez opciones de base de datos / biblioteca vectorial contra estos criterios:

| Criterio | Peso | Razon |
|----------|------|-------|
| Calidad de API C | Critico | FFI de Hemlock requiere enlace C (`extern fn`) a bibliotecas `.so` |
| Embebible (en proceso) | Critico | Los modulos stdlib de Hemlock son bibliotecas, no protocolos cliente-servidor |
| Peso de dependencias | Alto | Minimas dependencias preferidas (como sqlite -- solo un `.so`) |
| Simplicidad de API | Alto | Hemlock valora APIs explicitas y pequenas |
| Rendimiento | Medio | Suficientemente bueno para 1M+ vectores; no necesita escala de billones |
| Persistencia | Medio | Guardar/cargar indices a disco |
| Licencia | Medio | Debe ser permisiva (Apache-2.0, MIT, BSD) |

### Resultados

| Opcion | API C | Embebible | Deps | Rendimiento | Veredicto |
|--------|-------|-----------|------|-------------|-----------|
| **USearch** | C99 de primera clase | Si | Cero | HNSW + SIMD | **PRIMARIO** |
| **sqlite-vec** | Via SQL | Si | Cero (C puro) | Fuerza bruta | **SECUNDARIO** |
| hnswlib | Solo C++ | Si | Cero | HNSW | Sin API C -- omitir |
| FAISS | API C (faiss_c) | Si | BLAS requerido | Estado del arte | Demasiado pesado |
| pgvector | N/A | No (necesita PG) | PostgreSQL | Bueno | Requiere servidor -- omitir |
| Qdrant | Ninguna | No (servidor) | Pesado | Excelente | Requiere servidor -- omitir |
| Milvus | SDK C++ | No (distribuido) | Muy pesado | Excelente | Sistema distribuido -- omitir |
| Annoy | Solo C++ | Si | Cero | Moderado | Obsoleto, sin API C |
| LanceDB | Solo C comunitario | Si | Moderado (Rust) | Bueno | Sin API C oficial |
| ChromaDB | Ninguna | Limitado | Pesado | Moderado | Sin API C |

---

## Recomendacion: USearch (primario) + sqlite-vec (alternativa ligera)

### Por que NO pgvector

pgvector requiere un servidor PostgreSQL en ejecucion. Los modulos stdlib de Hemlock son bibliotecas embebibles cargadas via FFI (`import "libfoo.so"`), no protocolos cliente-servidor. Requerir que los usuarios instalen, configuren y ejecuten PostgreSQL para busqueda vectorial esta fundamentalmente desalineado con el patron de stdlib.

### Primario: USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) es una biblioteca de busqueda de similitud vectorial de codigo abierto (Apache-2.0) con una API C99 de primera clase. Usa el algoritmo HNSW (Hierarchical Navigable Small World) con optimizacion SIMD.

**Por que USearch se ajusta a Hemlock:**

1. **La API C99 mapea directamente al FFI de Hemlock.**
2. **Cero dependencias obligatorias.**
3. **En proceso y persistente.**
4. **API pequena y explicita.** ~20 funciones C.
5. **Probado en produccion.** Usado por ScyllaDB y YugabyteDB.
6. **Rendimiento.** Algoritmo HNSW con SIMD (AVX-512, NEON).

---

## Diseno de API Propuesto (`@stdlib/vector`)

Siguiendo los patrones establecidos por `@stdlib/sqlite`:

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Crear un indice
let idx = create_index(dimensions: 384, metric: "cosine");

// Agregar vectores (clave + array de flotantes)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// Buscar k vecinos mas cercanos
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// retorna: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Persistencia
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Busqueda filtrada (con predicado)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;
});

// Informacion
print(idx.size());       // numero de vectores
print(idx.dimensions()); // dimensionalidad
print(idx.contains(42)); // verificacion de pertenencia

// Limpieza
idx.remove(2);
idx.free();
```

### Exportaciones del modulo

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // mapeado en memoria, solo lectura

VectorIndex.add(key, vector)
VectorIndex.search(query, k?)
VectorIndex.search_filtered(query, k?, filter)
VectorIndex.remove(key)
VectorIndex.contains(key)
VectorIndex.count()
VectorIndex.size()
VectorIndex.dimensions()
VectorIndex.save(path)
VectorIndex.free()

distance(a, b, metric?)  // calculo de distancia independiente

// Metricas de distancia
METRIC_COSINE
METRIC_L2SQ       // Euclidiana (L2 al cuadrado)
METRIC_IP          // Producto interno (producto punto)
METRIC_HAMMING
METRIC_JACCARD

// Tipos escalares
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

---

## Plan de Implementacion

1. **Escribir enlaces FFI** -- declaraciones `extern fn` para la API C de USearch (~20 funciones)
2. **Implementar wrapper Hemlock** -- `create_index()`, `VectorIndex` define con metodos
3. **Manejar memoria** -- `alloc`/`free` apropiados para marshaling de datos vectoriales
4. **Agregar documentacion** -- `stdlib/docs/vector.md` siguiendo el patron de sqlite.md
5. **Agregar pruebas** -- `tests/stdlib_vector/` con CRUD basico, persistencia, precision de busqueda
6. **Agregar pruebas de paridad** -- Si se necesita soporte del compilador para patrones FFI usados

Alcance estimado: ~400-600 lineas de Hemlock.

---

## Preguntas Abiertas

1. **Nombre del modulo:** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`?
2. **Integracion sqlite-vec:** Enviar como parte de `@stdlib/sqlite` o modulo separado?
3. **API de cuantizacion:** Exponer la cuantizacion int8/f16 de USearch, o mantener f32 por defecto?
4. **Operaciones por lotes:** Agregar `add_batch()` / `search_batch()` o mantener API de un solo elemento?
5. **Configuracion de indice:** Cuanto de la configuracion HNSW de USearch exponer?
