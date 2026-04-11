# Vorschlag: `@stdlib/vector` -- Vektor-Ähnlichkeitssuche-Modul

**Status:** Erkundung / RFC
**Datum:** 2026-02-07

---

## Zusammenfassung

Ein `@stdlib/vector`-Modul hinzufügen, das in-process Vektor-Ähnlichkeitssuche (Nearest-Neighbor-Lookup) bietet. Dies ermöglicht embedding-basierte Suche, Empfehlungssysteme und KI/ML-Workflows direkt aus Hemlock ohne externen Server.

---

## Bewertete Optionen

Zehn Vektordatenbank-/Bibliotheksoptionen wurden anhand dieser Kriterien bewertet:

| Kriterium | Gewicht | Begründung |
|-----------|---------|------------|
| C-API-Qualität | Kritisch | Hemlock FFI erfordert C-Verlinkung (`extern fn`) zu `.so`-Bibliotheken |
| Einbettbar (in-process) | Kritisch | Hemlock-Stdlib-Module sind Bibliotheken, keine Client-Server-Protokolle |
| Abhängigkeitsgewicht | Hoch | Minimale Abhängigkeiten bevorzugt (wie sqlite -- nur eine `.so`) |
| API-Einfachheit | Hoch | Hemlock schätzt explizite, kleine APIs |
| Leistung | Mittel | Ausreichend für 1M+ Vektoren; braucht keine Milliarden-Skalierung |
| Persistenz | Mittel | Indizes auf Festplatte speichern/laden |
| Lizenz | Mittel | Muss permissiv sein (Apache-2.0, MIT, BSD) |

### Ergebnisse

| Option | C-API | Einbettbar | Abhängigkeiten | Leistung | Urteil |
|--------|-------|------------|----------------|----------|--------|
| **USearch** | C99 erstklassig | Ja | Null | HNSW + SIMD | **PRIMÄR** |
| **sqlite-vec** | Via SQL | Ja | Null (reines C) | Brute-Force | **SEKUNDÄR** |
| hnswlib | Nur C++ | Ja | Null | HNSW | Keine C-API -- übersprungen |
| FAISS | C-API (faiss_c) | Ja | BLAS erforderlich | Stand der Technik | Zu schwer |
| pgvector | N/A | Nein (braucht PG) | PostgreSQL | Gut | Server erforderlich -- übersprungen |

---

## Empfehlung: USearch (primär) + sqlite-vec (leichtgewichtige Alternative)

### Warum NICHT pgvector

pgvector erfordert einen laufenden PostgreSQL-Server. Hemlocks Stdlib-Module sind einbettbare Bibliotheken, die über FFI geladen werden (`import "libfoo.so"`), keine Client-Server-Protokolle. Benutzer zur Installation, Konfiguration und zum Betrieb von PostgreSQL für Vektorsuche zu zwingen, ist grundlegend inkompatibel mit dem Stdlib-Muster.

### Primär: USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) ist eine Open-Source-Bibliothek (Apache-2.0) für Vektor-Ähnlichkeitssuche mit einer erstklassigen C99-API. Sie verwendet den HNSW-Algorithmus (Hierarchical Navigable Small World) mit SIMD-Optimierung.

---

## Vorgeschlagenes API-Design (`@stdlib/vector`)

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Index erstellen
let idx = create_index(dimensions: 384, metric: "cosine");

// Vektoren hinzufügen (Schlüssel + Float-Array)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);
idx.add(3, [0.7, 0.8, 0.9, ...]);

// Nach k nächsten Nachbarn suchen
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// gibt zurück: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Persistenz
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Gefilterte Suche (mit Prädikat)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;  // nur Schlüssel > 100 abgleichen
});

// Info
print(idx.size());       // Anzahl der Vektoren
print(idx.dimensions()); // Dimensionalität
print(idx.contains(42)); // Mitgliedschaftsprüfung

// Bereinigung
idx.remove(2);
idx.free();
```

### Modulexporte

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // memory-mapped, schreibgeschützt

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

distance(a, b, metric?)  // eigenständige Distanzberechnung

// Distanzmetriken
METRIC_COSINE
METRIC_L2SQ       // Euklidisch (L2 quadriert)
METRIC_IP          // Inneres Produkt (Skalarprodukt)
METRIC_HAMMING
METRIC_JACCARD

// Skalartypen
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

---

## Offene Fragen

1. **Modulname:** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`?
2. **sqlite-vec-Integration:** Als Teil von `@stdlib/sqlite` (Erweiterungsladen) oder separates Modul?
3. **Quantisierungs-API:** USearchs int8/f16-Quantisierung exponieren, oder Standard f32 und einfach halten?
4. **Batch-Operationen:** `add_batch()` / `search_batch()` für Massenoperationen hinzufügen, oder bei Einzelelement-API bleiben?
5. **Index-Konfiguration:** Wie viel von USearchs HNSW-Tuning (Konnektivität, Expansionsfaktoren) exponieren?
