# Предложение: `@stdlib/vector` — модуль поиска векторного сходства

**Статус:** Исследование / RFC
**Дата:** 07.02.2026

---

## Описание

Добавить модуль `@stdlib/vector`, предоставляющий встроенный поиск векторного сходства (поиск ближайших соседей). Это позволяет выполнять поиск на основе эмбеддингов, рекомендательные системы и AI/ML-рабочие процессы непосредственно из Hemlock без необходимости внешнего сервера.

---

## Рекомендация: USearch (основной) + sqlite-vec (облегчённая альтернатива)

### Почему НЕ pgvector

pgvector требует работающий сервер PostgreSQL. Модули stdlib Hemlock — это встраиваемые библиотеки, загружаемые через FFI (`import "libfoo.so"`), а не протоколы клиент-сервер. Требование установки и настройки PostgreSQL для поиска векторов фундаментально не соответствует паттерну stdlib.

### Основной: USearch (`libusearch_c.so`)

[USearch](https://github.com/unum-cloud/USearch) — это библиотека поиска векторного сходства с открытым исходным кодом (Apache-2.0) и первоклассным C99 API. Использует алгоритм HNSW с SIMD-оптимизацией.

**Почему USearch подходит Hemlock:**

1. **C99 API напрямую отображается на Hemlock FFI**
2. **Ноль обязательных зависимостей** — компилируется в единый `.so`
3. **Встроенный и персистентный** — поддержка файлов с отображением в память
4. **Маленький, явный API** — ~20 C-функций
5. **Проверен в продакшене** — используется ScyllaDB и YugabyteDB
6. **Производительность** — HNSW с SIMD (AVX-512, NEON)

### Вторичный: sqlite-vec (расширение для `@stdlib/sqlite`)

[sqlite-vec](https://github.com/asg017/sqlite-vec) — расширение SQLite для поиска векторов через SQL.

---

## Предложенный дизайн API (`@stdlib/vector`)

```hemlock
import { VectorIndex, create_index, load_index } from "@stdlib/vector";

// Создание индекса
let idx = create_index(dimensions: 384, metric: "cosine");

// Добавление векторов (ключ + массив float)
idx.add(1, [0.1, 0.2, 0.3, ...]);
idx.add(2, [0.4, 0.5, 0.6, ...]);

// Поиск k ближайших соседей
let results = idx.search([0.15, 0.25, 0.35, ...], k: 10);
// возвращает: [{ key: 1, distance: 0.023 }, { key: 3, distance: 0.15 }, ...]

// Персистентность
idx.save("embeddings.usearch");
let loaded = load_index("embeddings.usearch", dimensions: 384);

// Фильтрованный поиск (с предикатом)
let filtered = idx.search_filtered([0.1, ...], k: 5, filter: fn(key) {
    return key > 100;
});

// Информация
print(idx.size());       // количество векторов
print(idx.dimensions()); // размерность
print(idx.contains(42)); // проверка наличия

// Очистка
idx.remove(2);
idx.free();
```

### Экспорты модуля

```
create_index(dimensions, metric?, connectivity?, expansion_add?, expansion_search?)
load_index(path, dimensions?, metric?)
view_index(path)  // отображение в память, только чтение

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

distance(a, b, metric?)  // отдельное вычисление расстояния

// Метрики расстояния
METRIC_COSINE
METRIC_L2SQ       // Евклидово (L2 квадрат)
METRIC_IP          // Скалярное произведение
METRIC_HAMMING
METRIC_JACCARD

// Скалярные типы
SCALAR_F32
SCALAR_F64
SCALAR_F16
SCALAR_I8
```

---

## Открытые вопросы

1. **Имя модуля:** `@stdlib/vector` vs `@stdlib/vectordb` vs `@stdlib/similarity`?
2. **Интеграция sqlite-vec:** Поставлять как часть `@stdlib/sqlite` или отдельный модуль?
3. **API квантизации:** Выставлять int8/f16 квантизацию USearch или по умолчанию f32?
4. **Пакетные операции:** Добавить `add_batch()` / `search_batch()` для массовых операций?
5. **Конфигурация индекса:** Сколько параметров настройки HNSW USearch выставлять?
