# Proposta: `@stdlib/vector` — Modulo di Ricerca per Similarità Vettoriale

**Stato:** Esplorazione / RFC
**Data:** 2026-02-07

---

## Sommario

Aggiungere un modulo `@stdlib/vector` che fornisca ricerca per similarità vettoriale in-process (lookup del vicino più prossimo). Questo abilita ricerca basata su embedding, sistemi di raccomandazione e workflow AI/ML direttamente da Hemlock senza richiedere un server esterno.

---

## Opzioni Valutate

Dieci opzioni di database/libreria vettoriale sono state valutate rispetto a questi criteri:

| Criterio | Peso | Motivazione |
|----------|------|-------------|
| Qualità API C | Critico | La FFI di Hemlock richiede linkage C (`extern fn`) a librerie `.so` |
| Integrabile (in-process) | Critico | I moduli stdlib di Hemlock sono librerie, non protocolli client-server |
| Peso dipendenze | Alto | Dipendenze minime preferite (come sqlite — un solo `.so`) |
| Semplicità API | Alto | Hemlock valuta API esplicite e piccole |
| Prestazioni | Medio | Sufficienti per 1M+ vettori; non necessita scala miliardaria |
| Persistenza | Medio | Salvataggio/caricamento indici su disco |
| Licenza | Medio | Deve essere permissiva (Apache-2.0, MIT, BSD) |

### Risultati

| Opzione | API C | Integrabile | Dipendenze | Prestazioni | Verdetto |
|---------|-------|-------------|------------|-------------|---------|
| **USearch** | C99 di prima classe | Sì | Zero | HNSW + SIMD | **PRIMARIO** |
| **sqlite-vec** | Via SQL | Sì | Zero (C puro) | Forza bruta | **SECONDARIO** |
| hnswlib | Solo C++ | Sì | Zero | HNSW | Nessuna API C — saltato |
| FAISS | API C (faiss_c) | Sì | BLAS richiesto | Stato dell'arte | Troppo pesante |
| pgvector | N/A | No (necessita PG) | PostgreSQL | Buone | Richiede server — saltato |
| Qdrant | Nessuna | No (server) | Pesanti | Eccellenti | Richiede server — saltato |
| Milvus | SDK C++ | No (distribuito) | Molto pesanti | Eccellenti | Sistema distribuito — saltato |
| Annoy | Solo C++ | Sì | Zero | Moderate | Obsoleto, nessuna API C |
| LanceDB | Solo C community | Sì | Moderate (Rust) | Buone | Nessuna API C ufficiale |
| ChromaDB | Nessuna | Limitato | Pesanti | Moderate | Nessuna API C |

---

## Raccomandazione: USearch (primario) + sqlite-vec (alternativa leggera)

### Perché NON pgvector

pgvector richiede un server PostgreSQL in esecuzione. I moduli stdlib di Hemlock sono librerie integrabili caricate via FFI (`import "libfoo.so"`), non protocolli client-server. Richiedere agli utenti di installare, configurare e far girare PostgreSQL per la ricerca vettoriale è fondamentalmente disallineato con il pattern stdlib. Il modulo sqlite funziona precisamente perché SQLite è una libreria in-process con zero requisiti server.

### Primario: USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) è una libreria di ricerca per similarità vettoriale open-source (Apache-2.0) con un'API C99 di prima classe. Usa l'algoritmo HNSW (Hierarchical Navigable Small World) con ottimizzazione SIMD.

**Perché USearch si adatta a Hemlock:**

1. **L'API C99 mappa direttamente alla FFI di Hemlock.** Il pattern è identico a `@stdlib/sqlite`.
2. **Zero dipendenze obbligatorie.** Compila in un singolo `.so` senza BLAS, LAPACK o altri requisiti esterni.
3. **In-process e persistente.** Supporto file memory-mapped — gli indici salvati su disco, caricati senza leggere tutto in RAM.
4. **API piccola ed esplicita.** ~20 funzioni C che coprono: init, add, search, remove, save, load, free. Si adatta alla filosofia "esplicito piuttosto che implicito" di Hemlock.
5. **Collaudato in produzione.** Usato da ScyllaDB e YugabyteDB per l'indicizzazione vettoriale.
6. **Prestazioni.** Algoritmo HNSW con SIMD (AVX-512, NEON). Supporta f32, f64, f16 e quantizzazione int8.

---

## Design API Proposto (`@stdlib/vector`)

Seguendo i pattern stabiliti da `@stdlib/sqlite` (wrapper FFI con API idiomatica Hemlock):

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Crea un indice
let idx = create_index(dimensions: 384, metric: "cosine");

// Aggiungi vettori (chiave + array di float)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// Cerca i k vicini più prossimi
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// restituisce: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Persistenza
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Ricerca filtrata (con predicato)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;  // trova solo chiavi > 100
});

// Info
print(idx.size());       // numero di vettori
print(idx.dimensions()); // dimensionalità
print(idx.contains(42)); // verifica appartenenza

// Pulizia
idx.remove(2);
idx.free();
```

### Export del modulo

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // memory-mapped, sola lettura

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

distance(a, b, metric?)  // calcolo distanza standalone

// Metriche di distanza
METRIC_COSINE
METRIC_L2SQ       // Euclidea (L2 al quadrato)
METRIC_IP          // Prodotto interno (prodotto scalare)
METRIC_HAMMING
METRIC_JACCARD

// Tipi scalari
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

### Requisiti di sistema

```
# Debian/Ubuntu
sudo apt install libusearch-dev

# Da sorgente
git clone https://github.com/unum-cloud/usearch
cd usearch && cmake -B build && cmake --build build
sudo cmake --install build
```

---

## Piano di Implementazione

1. **Scrivere binding FFI** — dichiarazioni `extern fn` per l'API C di USearch (~20 funzioni)
2. **Implementare wrapper Hemlock** — `create_index()`, define `VectorIndex` con metodi
3. **Gestire la memoria** — Appropriato `alloc`/`free` per il marshaling dei dati vettoriali, pulizia delle stringhe di errore
4. **Aggiungere documentazione** — `stdlib/docs/vector.md` seguendo il pattern di sqlite.md
5. **Aggiungere test** — `tests/stdlib_vector/` con CRUD base, persistenza, accuratezza della ricerca
6. **Aggiungere test di parità** — Se necessario supporto compilatore per i pattern FFI usati

Scope stimato: ~400-600 righe di Hemlock (paragonabile a `sqlite.hml` con 968 righe, ma superficie API più semplice).

---

## Domande Aperte

1. **Nome del modulo:** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`?
2. **Integrazione sqlite-vec:** Distribuire come parte di `@stdlib/sqlite` (caricamento estensione) o modulo separato?
3. **API di quantizzazione:** Esporre la quantizzazione int8/f16 di USearch, o usare f32 di default e mantenere la semplicità?
4. **Operazioni batch:** Aggiungere `add_batch()` / `search_batch()` per operazioni in blocco, o mantenere l'API per singolo elemento?
5. **Configurazione indice:** Quanto del tuning HNSW di USearch (connectivity, fattori di espansione) esporre?
