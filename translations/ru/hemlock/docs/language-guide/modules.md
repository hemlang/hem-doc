# Система модулей Hemlock

Этот документ описывает систему модулей с импортом/экспортом в стиле ES6, реализованную для Hemlock.

## Обзор

Hemlock поддерживает файловую систему модулей с синтаксисом импорта/экспорта в стиле ES6. Модули:
- **Синглтоны**: Каждый модуль загружается один раз и кэшируется
- **Файловые**: Модули соответствуют файлам .hml на диске
- **Явно импортируемые**: Зависимости объявляются операторами импорта
- **Топологически выполняемые**: Зависимости выполняются до зависящих от них

Для управления пакетами и сторонних зависимостей см. [hpm (Hemlock Package Manager)](https://github.com/hemlang/hpm).

## Синтаксис

### Операторы экспорта

**Встроенные именованные экспорты:**
```hemlock
export fn add(a, b) {
    return a + b;
}

export const PI = 3.14159;
export let counter = 0;
```

**Список экспорта:**
```hemlock
fn add(a, b) { return a + b; }
fn subtract(a, b) { return a - b; }

export { add, subtract };
```

**Экспорт Extern (FFI функции):**
```hemlock
import "libc.so.6";

// Экспорт FFI функций для использования в других модулях
export extern fn strlen(s: string): i32;
export extern fn getpid(): i32;
```

См. [Документацию FFI](../advanced/ffi.md#exporting-ffi-functions) для деталей экспорта FFI функций.

**Экспорт Define (типы структур):**
```hemlock
// Экспорт определений типов структур
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}
```

**Важно:** Экспортированные типы структур регистрируются глобально при загрузке модуля. Они становятся доступными автоматически когда вы импортируете что-либо из модуля - вам НЕ нужно (и нельзя) явно импортировать их по имени:

```hemlock
// ХОРОШО - типы структур авто-доступны после любого импорта
import { some_function } from "./my_module.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };  // Работает!

// ПЛОХО - нельзя явно импортировать типы структур
import { Vector2 } from "./my_module.hml";  // Ошибка: Undefined variable 'Vector2'
```

См. [Документацию FFI](../advanced/ffi.md#exporting-struct-types) для деталей экспорта типов структур.

**Реэкспорты:**
```hemlock
// Реэкспорт из другого модуля
export { add, subtract } from "./math.hml";
```

### Операторы импорта

**Именованные импорты:**
```hemlock
import { add, subtract } from "./math.hml";
print(add(1, 2));  // 3
```

**Импорт пространства имен:**
```hemlock
import * as math from "./math.hml";
print(math.add(1, 2));  // 3
print(math.PI);  // 3.14159
```

**Псевдонимы:**
```hemlock
import { add as sum, subtract as diff } from "./math.hml";
print(sum(1, 2));  // 3
```

## Разрешение модулей

### Типы путей

**Относительные пути:**
```hemlock
import { foo } from "./module.hml";       // Та же директория
import { bar } from "../parent.hml";      // Родительская директория
import { baz } from "./sub/nested.hml";   // Поддиректория
```

**Абсолютные пути:**
```hemlock
import { foo } from "/absolute/path/to/module.hml";
```

**Обработка расширений:**
- Расширение `.hml` можно опустить - оно будет добавлено автоматически
- `./math` разрешается в `./math.hml`

## Возможности

### Обнаружение циклических зависимостей

Система модулей обнаруживает циклические зависимости и сообщает об ошибке:

```
Error: Circular dependency detected when loading '/path/to/a.hml'
```

### Кэширование модулей

Модули загружаются один раз и кэшируются. Множественные импорты того же модуля возвращают тот же экземпляр:

```hemlock
// counter.hml
export let count = 0;
export fn increment() {
    count = count + 1;
}

// a.hml
import { count, increment } from "./counter.hml";
increment();
print(count);  // 1

// b.hml
import { count } from "./counter.hml";  // Тот же экземпляр!
print(count);  // Все еще 1 (разделяемое состояние)
```

### Неизменяемость импортов

Импортированные связывания нельзя переназначать:

```hemlock
import { add } from "./math.hml";
add = fn() { };  // ОШИБКА: cannot reassign imported binding
```

## Детали реализации

### Архитектура

**Файлы:**
- `include/module.h` - API системы модулей
- `src/module.c` - Загрузка, кэширование и выполнение модулей
- Поддержка парсера в `src/parser.c`
- Поддержка времени выполнения в `src/interpreter/runtime.c`

**Ключевые компоненты:**
1. **ModuleCache**: Поддерживает загруженные модули, индексированные по абсолютному пути
2. **Module**: Представляет загруженный модуль с его AST и экспортами
3. **Разрешение путей**: Разрешает относительные/абсолютные пути в канонические пути
4. **Топологическое выполнение**: Выполняет модули в порядке зависимостей

### Процесс загрузки модуля

1. **Фаза разбора**: Токенизация и разбор файла модуля
2. **Разрешение зависимостей**: Рекурсивная загрузка импортируемых модулей
3. **Обнаружение циклов**: Проверка, не загружается ли уже модуль
4. **Кэширование**: Сохранение модуля в кэше по абсолютному пути
5. **Фаза выполнения**: Выполнение в топологическом порядке (сначала зависимости)

### API

```c
// Высокоуровневый API
int execute_file_with_modules(const char *file_path,
                               int argc, char **argv,
                               ExecutionContext *ctx);

// Низкоуровневый API
ModuleCache* module_cache_new(const char *initial_dir);
void module_cache_free(ModuleCache *cache);
Module* load_module(ModuleCache *cache, const char *module_path, ExecutionContext *ctx);
void execute_module(Module *module, ModuleCache *cache, ExecutionContext *ctx);
```

## Тестирование

Тестовые модули находятся в `tests/modules/` и `tests/parity/modules/`:

- `math.hml` - Базовый модуль с экспортами
- `test_import_named.hml` - Тест именованного импорта
- `test_import_namespace.hml` - Тест импорта пространства имен
- `test_import_alias.hml` - Тест псевдонимов импорта
- `export_extern.hml` - Тест экспорта extern FFI функций (Linux)

## Импорты пакетов (hpm)

С установленным [hpm](https://github.com/hemlang/hpm) можно импортировать сторонние пакеты с GitHub:

```hemlock
// Импорт из корня пакета (использует "main" из package.json)
import { app, router } from "hemlang/sprout";

// Импорт из подпути
import { middleware } from "hemlang/sprout/middleware";

// Стандартная библиотека (встроена в Hemlock)
import { HashMap } from "@stdlib/collections";
```

Пакеты устанавливаются в `hem_modules/` и разрешаются используя синтаксис GitHub `owner/repo`.

```bash
# Установка пакета
hpm install hemlang/sprout

# Установка с ограничением версии
hpm install hemlang/sprout@^1.0.0
```

См. [документацию hpm](https://github.com/hemlang/hpm) для полной информации.

## Текущие ограничения

1. **Нет динамических импортов**: `import()` как функция времени выполнения не поддерживается
2. **Нет условных экспортов**: Экспорты должны быть на верхнем уровне
3. **Статические пути библиотек**: Импорты FFI библиотек используют статические пути (специфичные для платформы)

## Будущая работа

- Динамические импорты с функцией `import()`
- Условные экспорты
- Метаданные модулей (`import.meta`)
- Tree shaking и удаление мертвого кода

## Примеры

См. `tests/modules/` для рабочих примеров системы модулей.

Пример структуры модулей:
```
project/
├── main.hml
├── lib/
│   ├── math.hml
│   ├── string.hml
│   └── index.hml (barrel module)
└── utils/
    └── helpers.hml
```

Пример использования:
```hemlock
// lib/math.hml
export fn add(a, b) { return a + b; }
export fn multiply(a, b) { return a * b; }

// lib/index.hml (barrel)
export { add, multiply } from "./math.hml";

// main.hml
import { add } from "./lib/index.hml";
print(add(2, 3));  // 5
```
