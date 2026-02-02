# Настройка проекта

Полное руководство по настройке проектов Hemlock с hpm.

## Создание нового проекта

### Базовая настройка

Создайте новый проект с нуля:

```bash
# Создание директории проекта
mkdir my-project
cd my-project

# Инициализация package.json
hpm init

# Создание структуры директорий
mkdir -p src test
```

### Шаблоны проектов

Вот типичные структуры проектов для различных случаев использования:

#### Библиотека

Для переиспользуемых библиотек:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Главная точка входа, экспортирует публичный API
│   ├── core.hml           # Основная функциональность
│   ├── utils.hml          # Утилиты
│   └── types.hml          # Определения типов
└── test/
    ├── framework.hml      # Тестовый фреймворк
    ├── run.hml            # Запуск тестов
    └── test_core.hml      # Тесты
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Приложение

Для автономных приложений:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Точка входа приложения
│   ├── config.hml         # Конфигурация
│   ├── commands/          # CLI команды
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Внутренние библиотеки
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Файлы данных
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Веб-приложение

Для веб-серверов:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Точка входа сервера
│   ├── routes/            # Обработчики маршрутов
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Промежуточное ПО
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Модели данных
│   │   └── user.hml
│   └── services/          # Бизнес-логика
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Статические файлы
│   ├── css/
│   └── js/
└── views/                 # Шаблоны
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## Файл package.json

### Обязательные поля

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### Все поля

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
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

### Справочник полей

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | string | Имя пакета в формате owner/repo (обязательно) |
| `version` | string | Семантическая версия (обязательно) |
| `description` | string | Краткое описание |
| `author` | string | Имя и email автора |
| `license` | string | Идентификатор лицензии (MIT, Apache-2.0 и т.д.) |
| `repository` | string | URL репозитория |
| `homepage` | string | Домашняя страница проекта |
| `bugs` | string | URL баг-трекера |
| `main` | string | Файл точки входа (по умолчанию: src/index.hml) |
| `keywords` | array | Ключевые слова для поиска |
| `dependencies` | object | Зависимости времени выполнения |
| `devDependencies` | object | Зависимости разработки |
| `scripts` | object | Именованные скрипты |
| `files` | array | Файлы для включения при публикации |
| `native` | object | Требования нативных библиотек |

## Файл package-lock.json

Файл блокировки генерируется автоматически и должен быть закоммичен в систему контроля версий. Он обеспечивает воспроизводимые установки.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Лучшие практики для файла блокировки

- **Коммитьте** package-lock.json в систему контроля версий
- **Не редактируйте** вручную — он генерируется автоматически
- **Запускайте `hpm install`** после получения изменений
- **Удалите и регенерируйте** при повреждении:
  ```bash
  rm package-lock.json
  hpm install
  ```

## Директория hem_modules

Установленные пакеты хранятся в `hem_modules/`:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### Лучшие практики для hem_modules

- **Добавьте в .gitignore** — не коммитьте зависимости
- **Не модифицируйте** — изменения будут перезаписаны
- **Удалите для чистой переустановки**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Рекомендуемый .gitignore для проектов Hemlock:

```gitignore
# Зависимости
hem_modules/

# Результаты сборки
dist/
*.hmlc

# Файлы IDE
.idea/
.vscode/
*.swp
*.swo

# Файлы ОС
.DS_Store
Thumbs.db

# Логи
*.log
logs/

# Окружение
.env
.env.local

# Покрытие тестов
coverage/
```

## Работа с зависимостями

### Добавление зависимостей

```bash
# Добавить зависимость времени выполнения
hpm install hemlang/json

# Добавить с ограничением версии
hpm install hemlang/sprout@^2.0.0

# Добавить зависимость разработки
hpm install hemlang/test-utils --dev
```

### Импорт зависимостей

```hemlock
// Импорт из пакета (использует запись "main")
import { parse, stringify } from "hemlang/json";

// Импорт из подпути
import { Router } from "hemlang/sprout/router";

// Импорт стандартной библиотеки
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Разрешение импортов

hpm разрешает импорты в следующем порядке:

1. **Стандартная библиотека**: Импорты `@stdlib/*` загружают встроенные модули
2. **Корень пакета**: `owner/repo` использует поле `main`
3. **Подпуть**: `owner/repo/path` проверяет:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Скрипты

### Определение скриптов

Добавьте скрипты в package.json:

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

### Запуск скриптов

```bash
hpm run start
hpm run dev
hpm run build

# Сокращение для test
hpm test

# Передача аргументов
hpm run test -- --verbose --filter=unit
```

### Соглашения об именовании скриптов

| Скрипт | Назначение |
|--------|------------|
| `start` | Запуск приложения |
| `dev` | Запуск в режиме разработки |
| `test` | Запуск всех тестов |
| `build` | Сборка для продакшена |
| `clean` | Удаление сгенерированных файлов |
| `lint` | Проверка стиля кода |
| `format` | Форматирование кода |

## Рабочий процесс разработки

### Начальная настройка

```bash
# Клонирование проекта
git clone https://github.com/yourusername/my-project.git
cd my-project

# Установка зависимостей
hpm install

# Запуск тестов
hpm test

# Начало разработки
hpm run dev
```

### Ежедневный рабочий процесс

```bash
# Получение последних изменений
git pull

# Установка новых зависимостей
hpm install

# Внесение изменений...

# Запуск тестов
hpm test

# Коммит
git add .
git commit -m "Add feature"
git push
```

### Добавление новой функции

```bash
# Создание ветки функции
git checkout -b feature/new-feature

# Добавление новой зависимости при необходимости
hpm install hemlang/new-lib

# Реализация функции...

# Тестирование
hpm test

# Коммит и пуш
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## Конфигурация для разных окружений

### Использование переменных окружения

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### Файл конфигурации

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## См. также

- [Быстрый старт](quick-start.md) — Быстрое начало работы
- [Команды](commands.md) — Справочник команд
- [Создание пакетов](creating-packages.md) — Публикация пакетов
- [Конфигурация](configuration.md) — Конфигурация hpm
