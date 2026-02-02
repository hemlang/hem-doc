# Архитектура

Внутренняя архитектура и дизайн hpm. Этот документ предназначен для контрибьюторов и тех, кто хочет понять, как работает hpm.

## Обзор

hpm написан на Hemlock и состоит из нескольких модулей, которые обрабатывают различные аспекты управления пакетами:

```
src/
├── main.hml        # Точка входа CLI и маршрутизация команд
├── manifest.hml    # Работа с package.json
├── lockfile.hml    # Работа с package-lock.json
├── semver.hml      # Семантическое версионирование
├── resolver.hml    # Разрешение зависимостей
├── github.hml      # Клиент GitHub API
├── installer.hml   # Загрузка и извлечение пакетов
└── cache.hml       # Управление глобальным кэшем
```

## Ответственность модулей

### main.hml

Точка входа для CLI-приложения.

**Ответственность:**
- Разбор аргументов командной строки
- Маршрутизация команд к соответствующим обработчикам
- Отображение справки и информации о версии
- Обработка глобальных флагов (--verbose, --dry-run и т.д.)
- Выход с соответствующими кодами

**Ключевые функции:**
- `main()` — Точка входа, разбирает аргументы и распределяет команды
- `cmd_init()` — Обработка `hpm init`
- `cmd_install()` — Обработка `hpm install`
- `cmd_uninstall()` — Обработка `hpm uninstall`
- `cmd_update()` — Обработка `hpm update`
- `cmd_list()` — Обработка `hpm list`
- `cmd_outdated()` — Обработка `hpm outdated`
- `cmd_run()` — Обработка `hpm run`
- `cmd_why()` — Обработка `hpm why`
- `cmd_cache()` — Обработка `hpm cache`

**Сокращения команд:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Обработка чтения и записи файлов `package.json`.

**Ответственность:**
- Чтение/запись package.json
- Валидация структуры пакета
- Управление зависимостями
- Разбор спецификаторов пакетов (owner/repo@version)

**Ключевые функции:**
```hemlock
create_default(): Manifest           // Создать пустой манифест
read_manifest(): Manifest            // Прочитать из файла
write_manifest(m: Manifest)          // Записать в файл
validate(m: Manifest): bool          // Валидировать структуру
get_all_dependencies(m): Map         // Получить deps + devDeps
add_dependency(m, pkg, ver, dev)     // Добавить зависимость
remove_dependency(m, pkg)            // Удалить зависимость
parse_specifier(spec): (name, ver)   // Разобрать "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // Разобрать "owner/repo"
```

**Структура Manifest:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Управление файлом `package-lock.json` для воспроизводимых установок.

**Ответственность:**
- Создание/чтение/запись файлов блокировки
- Отслеживание точных разрешённых версий
- Хранение URL загрузки и хешей целостности
- Удаление осиротевших зависимостей

**Ключевые функции:**
```hemlock
create_empty(): Lockfile              // Создать пустой lockfile
read_lockfile(): Lockfile             // Прочитать из файла
write_lockfile(l: Lockfile)           // Записать в файл
create_entry(ver, url, hash, deps)    // Создать запись блокировки
get_locked(l, pkg): LockEntry?        // Получить заблокированную версию
set_locked(l, pkg, entry)             // Установить заблокированную версию
remove_locked(l, pkg)                 // Удалить запись
prune(l, keep: Set)                   // Удалить осиротевшие
needs_update(l, m): bool              // Проверить синхронизацию
```

**Структура Lockfile:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // URL загрузки
    integrity: string,    // SHA256 хеш
    dependencies: Map<string, string>
};
```

### semver.hml

Полная реализация Semantic Versioning 2.0.0.

**Ответственность:**
- Разбор строк версий
- Сравнение версий
- Разбор и вычисление ограничений версий
- Поиск версий, удовлетворяющих ограничениям

**Ключевые функции:**
```hemlock
// Разбор
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// Сравнение
compare(a, b: Version): int           // -1, 0 или 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Ограничения
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // Проверка соответствия v ограничению c
max_satisfying(versions, c): Version?      // Найти максимальное соответствие
sort(versions): [Version]                  // Сортировка по возрастанию

// Утилиты
constraints_overlap(a, b: Constraint): bool  // Проверка совместимости
```

**Структура Version:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // например, ["beta", "1"]
    build: string?          // например, "20230101"
};
```

**Типы Constraint:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Комбинированные диапазоны
    | Any;                     // "*"
```

### resolver.hml

Реализует разрешение зависимостей в стиле npm.

**Ответственность:**
- Разрешение деревьев зависимостей
- Обнаружение конфликтов версий
- Обнаружение циклических зависимостей
- Построение деревьев для визуализации

**Ключевые функции:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Главный резолвер: возвращает плоскую карту всех зависимостей с разрешёнными версиями

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Найти версию, удовлетворяющую всем ограничениям

detect_cycles(deps: Map): [Cycle]?
    // Найти циклические зависимости с помощью DFS

build_tree(lockfile): Tree
    // Создать древовидную структуру для отображения

find_why(pkg, lockfile): [Chain]
    // Найти цепочки зависимостей, объясняющие, почему установлен pkg
```

**Алгоритм разрешения:**

1. **Сбор ограничений**: Обход манифеста и транзитивных зависимостей
2. **Разрешение каждого пакета**: Для каждого пакета:
   - Получить все ограничения версий от зависящих пакетов
   - Получить доступные версии с GitHub
   - Найти максимальную версию, удовлетворяющую ВСЕМ ограничениям
   - Ошибка, если ни одна версия не удовлетворяет всем (конфликт)
3. **Обнаружение циклов**: Запуск DFS для поиска циклических зависимостей
4. **Возврат плоской карты**: Имя пакета → информация о разрешённой версии

**Структура ResolveResult:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

Клиент GitHub API для обнаружения и загрузки пакетов.

**Ответственность:**
- Получение доступных версий (тегов)
- Загрузка package.json из репозиториев
- Загрузка архивов релизов
- Обработка аутентификации и лимитов запросов

**Ключевые функции:**
```hemlock
get_token(): string?
    // Получить токен из env или config

github_request(url, headers?): Response
    // Выполнить API-запрос с повторами

get_tags(owner, repo): [string]
    // Получить теги версий (v1.0.0, v1.1.0 и т.д.)

get_package_json(owner, repo, ref): Manifest
    // Получить package.json по определённому тегу/коммиту

download_tarball(owner, repo, tag): bytes
    // Загрузить архив релиза

repo_exists(owner, repo): bool
    // Проверить существование репозитория

get_repo_info(owner, repo): RepoInfo
    // Получить метаданные репозитория
```

**Логика повторов:**
- Экспоненциальная задержка: 1с, 2с, 4с, 8с
- Повторы при: 403 (лимит), 5xx (ошибка сервера), сетевых ошибках
- Максимум 4 повтора
- Чёткое сообщение об ошибках лимита

**Используемые API-эндпоинты:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Обработка загрузки и извлечения пакетов.

**Ответственность:**
- Загрузка пакетов с GitHub
- Извлечение архивов в hem_modules
- Проверка/использование кэшированных пакетов
- Установка/удаление пакетов

**Ключевые функции:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Загрузить и установить один пакет

install_all(packages: Map, options): InstallResult
    // Установить все разрешённые пакеты

uninstall_package(name: string): bool
    // Удалить пакет из hem_modules

get_installed(): Map<string, string>
    // Список установленных пакетов

verify_integrity(pkg): bool
    // Проверить целостность пакета

prefetch_packages(packages: Map): void
    // Параллельная загрузка в кэш (экспериментально)
```

**Процесс установки:**

1. Проверить, установлен ли уже с правильной версией
2. Проверить кэш на наличие архива
3. Если не в кэше, загрузить с GitHub
4. Сохранить в кэш для будущего использования
5. Извлечь в `hem_modules/owner/repo/`
6. Проверить установку

**Создаваемая структура директорий:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Управление глобальным кэшем пакетов.

**Ответственность:**
- Хранение загруженных архивов
- Получение кэшированных пакетов
- Вывод списка кэшированных пакетов
- Очистка кэша
- Управление конфигурацией

**Ключевые функции:**
```hemlock
get_cache_dir(): string
    // Получить директорию кэша (учитывает HPM_CACHE_DIR)

get_config_dir(): string
    // Получить директорию конфигурации (~/.hpm)

is_cached(owner, repo, version): bool
    // Проверить, есть ли архив в кэше

get_cached_path(owner, repo, version): string
    // Получить путь к кэшированному архиву

store_tarball_file(owner, repo, version, data): void
    // Сохранить архив в кэш

list_cached(): [CachedPackage]
    // Список всех кэшированных пакетов

clear_cache(): int
    // Удалить все кэшированные пакеты, вернуть освобождённые байты

get_cache_size(): int
    // Вычислить общий размер кэша

read_config(): Config
    // Прочитать ~/.hpm/config.json

write_config(c: Config): void
    // Записать файл конфигурации
```

**Структура кэша:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Поток данных

### Поток команды Install

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Разбор аргументов, вызов cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Чтение package.json, добавление зависимости
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Разрешение всех зависимостей
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Получение версий, поиск подходящей
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Загрузка и извлечение пакетов
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Загрузка или использование кэша
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Обновление package-lock.json
    └──────────┘
```

### Детали алгоритма разрешения

```
Вход: manifest.dependencies, manifest.devDependencies, существующий lockfile

1. Инициализация:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [прямые зависимости]

2. Пока очередь не пуста:
   a. pkg = queue.pop()
   b. Если pkg уже разрешён, пропустить
   c. Получить все ограничения для pkg от зависящих пакетов
   d. Получить доступные версии с GitHub (кэшированные)
   e. Найти максимальную версию, удовлетворяющую всем ограничениям
   f. Если не найдена: КОНФЛИКТ
   g. resolved[pkg] = {version, url, deps}
   h. Добавить зависимости pkg в очередь

3. Обнаружение циклов в разрешённом графе
   - Если цикл найден: ОШИБКА

4. Вернуть разрешённую карту
```

## Обработка ошибок

### Коды выхода

Определены в main.hml:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Распространение ошибок

Ошибки поднимаются через возвращаемые значения:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? распространяет
    // ...
}
```

## Тестирование

### Тестовый фреймворк

Пользовательский тестовый фреймворк в `test/framework.hml`:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### Тестовые файлы

- `test/test_semver.hml` — Разбор версий, сравнение, ограничения
- `test/test_manifest.hml` — Чтение/запись манифеста, валидация
- `test/test_lockfile.hml` — Операции с lockfile
- `test/test_cache.hml` — Управление кэшем

### Запуск тестов

```bash
# Все тесты
make test

# Конкретные тесты
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Планы на будущее

### Планируемые возможности

1. **Проверка целостности** — Полная проверка SHA256 хешей
2. **Workspaces** — Поддержка монорепозиториев
3. **Система плагинов** — Расширяемые команды
4. **Аудит** — Проверка уязвимостей безопасности
5. **Приватный реестр** — Самохостинг пакетов

### Известные ограничения

1. **Баг бандлера** — Невозможно создать автономный исполняемый файл
2. **Параллельные загрузки** — Экспериментально, возможны race conditions
3. **Целостность** — SHA256 не полностью реализован

## Участие в разработке

### Стиль кода

- Используйте отступ в 4 пробела
- Функции должны делать одну вещь
- Комментируйте сложную логику
- Пишите тесты для новых возможностей

### Добавление команды

1. Добавьте обработчик в `main.hml`:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Реализация
   }
   ```

2. Добавьте в диспетчер команд:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Обновите текст справки

### Добавление модуля

1. Создайте `src/newmodule.hml`
2. Экспортируйте публичный интерфейс
3. Импортируйте в модулях, которым он нужен
4. Добавьте тесты в `test/test_newmodule.hml`

## См. также

- [Команды](commands.md) — Справочник CLI
- [Создание пакетов](creating-packages.md) — Разработка пакетов
- [Версионирование](versioning.md) — Семантическое версионирование
