# Спецификация пакетов

Полный справочник по формату файла `package.json`.

## Обзор

Каждый пакет hpm требует файл `package.json` в корне проекта. Этот файл определяет метаданные пакета, зависимости и скрипты.

## Минимальный пример

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Полный пример

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

## Справочник полей

### name (обязательно)

Имя пакета в формате `owner/repo`.

```json
{
  "name": "hemlang/sprout"
}
```

**Требования:**
- Должно быть в формате `owner/repo`
- `owner` должен быть вашим именем пользователя или организацией на GitHub
- `repo` должен быть именем репозитория
- Используйте строчные буквы, цифры и дефисы
- Максимум 214 символов

**Допустимые имена:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Недопустимые имена:**
```
my-package          # Отсутствует owner
hemlang/My_Package  # Заглавные буквы и подчёркивание
hemlang             # Отсутствует repo
```

### version (обязательно)

Версия пакета по [Семантическому версионированию](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Формат:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Допустимые версии:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Краткое описание пакета.

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- Держите менее 200 символов
- Описывайте, что делает пакет, а не как

### author

Информация об авторе пакета.

```json
{
  "author": "Your Name <email@example.com>"
}
```

**Принимаемые форматы:**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

Идентификатор лицензии.

```json
{
  "license": "MIT"
}
```

**Распространённые лицензии:**
- `MIT` — Лицензия MIT
- `Apache-2.0` — Лицензия Apache 2.0
- `GPL-3.0` — GNU General Public License v3.0
- `BSD-3-Clause` — BSD 3-Clause License
- `ISC` — ISC License
- `UNLICENSED` — Проприетарная/приватная

По возможности используйте [идентификаторы SPDX](https://spdx.org/licenses/).

### repository

Ссылка на исходный репозиторий.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

URL домашней страницы проекта.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

URL трекера ошибок.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Файл точки входа для пакета.

```json
{
  "main": "src/index.hml"
}
```

**По умолчанию:** `src/index.hml`

Когда пользователи импортируют ваш пакет:
```hemlock
import { x } from "owner/repo";
```

hpm загружает файл, указанный в `main`.

**Порядок разрешения для импортов:**
1. Точный путь: `src/index.hml`
2. С расширением .hml: `src/index` → `src/index.hml`
3. Файл index: `src/index/` → `src/index/index.hml`

### keywords

Массив ключевых слов для поиска.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Используйте нижний регистр
- Будьте конкретны и релевантны
- Включите язык ("hemlock") при необходимости

### dependencies

Зависимости времени выполнения, необходимые для работы пакета.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Ключ:** Имя пакета (`owner/repo`)
**Значение:** Ограничение версии

**Синтаксис ограничений версий:**

| Ограничение | Значение |
|-------------|----------|
| `1.2.3` | Точная версия |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | Минимум 1.0.0 |
| `>=1.0.0 <2.0.0` | Диапазон |
| `*` | Любая версия |

### devDependencies

Зависимости только для разработки (тестирование, сборка и т.д.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Dev-зависимости:
- Устанавливаются во время разработки
- Не устанавливаются, когда пакет используется как зависимость
- Используются для тестирования, сборки, линтинга и т.д.

### scripts

Именованные команды, которые можно запускать с помощью `hpm run`.

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

**Запуск скриптов:**
```bash
hpm run start
hpm run build
hpm test        # Сокращение для 'hpm run test'
```

**Передача аргументов:**
```bash
hpm run test -- --verbose --filter=unit
```

**Распространённые скрипты:**

| Скрипт | Назначение |
|--------|------------|
| `start` | Запуск приложения |
| `dev` | Режим разработки с горячей перезагрузкой |
| `test` | Запуск тестов |
| `build` | Сборка для продакшена |
| `clean` | Удаление артефактов сборки |
| `lint` | Проверка стиля кода |
| `format` | Форматирование кода |

### files

Файлы и директории для включения при установке пакета.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Поведение по умолчанию:** Если не указано, включает:
- Все файлы в репозитории
- Исключает `.git/`, `node_modules/`, `hem_modules/`

**Используйте для:**
- Уменьшения размера пакета
- Исключения тестовых файлов из распространения
- Включения только необходимых файлов

### native

Требования нативных библиотек.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Документирует нативные зависимости, которые должны быть установлены в системе.

## Валидация

hpm валидирует package.json при различных операциях. Распространённые ошибки валидации:

### Отсутствуют обязательные поля

```
Error: package.json missing required field: name
```

**Решение:** Добавьте обязательное поле.

### Недопустимый формат имени

```
Error: Invalid package name. Must be in owner/repo format.
```

**Решение:** Используйте формат `owner/repo`.

### Недопустимая версия

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Решение:** Используйте полный формат semver (`1.0.0`).

### Недопустимый JSON

```
Error: package.json is not valid JSON
```

**Решение:** Проверьте синтаксис JSON (запятые, кавычки, скобки).

## Создание package.json

### Интерактивно

```bash
hpm init
```

Запрашивает каждое поле интерактивно.

### С параметрами по умолчанию

```bash
hpm init --yes
```

Создаёт со значениями по умолчанию:
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Вручную

Создайте файл вручную:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Лучшие практики

1. **Всегда указывайте main** — Не полагайтесь на значение по умолчанию
2. **Используйте caret-диапазоны** — `^1.0.0` для большинства зависимостей
3. **Разделяйте dev-зависимости** — Держите тестовые/сборочные зависимости в devDependencies
4. **Включайте ключевые слова** — Помогите пользователям найти ваш пакет
5. **Документируйте скрипты** — Называйте скрипты понятно
6. **Указывайте лицензию** — Обязательно для open source
7. **Добавьте описание** — Помогите пользователям понять назначение

## См. также

- [Создание пакетов](creating-packages.md) — Руководство по публикации
- [Версионирование](versioning.md) — Ограничения версий
- [Настройка проекта](project-setup.md) — Структура проекта
