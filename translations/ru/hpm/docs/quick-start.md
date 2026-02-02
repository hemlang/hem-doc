# Быстрый старт

Начните работу с hpm за 5 минут.

## Установка hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Для дополнительных вариантов установки см. [Руководство по установке](installation.md).

## Создание нового проекта

Начните с создания новой директории и инициализации пакета:

```bash
mkdir my-project
cd my-project
hpm init
```

Вам будут заданы вопросы о деталях проекта:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Используйте `--yes` для принятия всех значений по умолчанию:

```bash
hpm init --yes
```

## Структура проекта

Создайте базовую структуру проекта:

```
my-project/
├── package.json        # Манифест проекта
├── src/
│   └── index.hml      # Главная точка входа
└── test/
    └── test.hml       # Тесты
```

Создайте главный файл:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Главная точка входа
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## Установка зависимостей

Ищите пакеты на GitHub (пакеты используют формат `owner/repo`):

```bash
# Установка пакета
hpm install hemlang/sprout

# Установка с ограничением версии
hpm install hemlang/json@^1.0.0

# Установка как зависимость разработки
hpm install hemlang/test-utils --dev
```

После установки структура вашего проекта включает `hem_modules/`:

```
my-project/
├── package.json
├── package-lock.json   # Файл блокировки (генерируется автоматически)
├── hem_modules/        # Установленные пакеты
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Использование установленных пакетов

Импортируйте пакеты, используя их путь на GitHub:

```hemlock
// Импорт из установленного пакета
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Импорт из подпути
import { middleware } from "hemlang/sprout/middleware";

// Стандартная библиотека (встроенная)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Добавление скриптов

Добавьте скрипты в ваш `package.json`:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Запускайте скрипты с помощью `hpm run`:

```bash
hpm run start
hpm run build

# Сокращение для test
hpm test
```

## Типичные рабочие процессы

### Установка всех зависимостей

Когда вы клонируете проект с `package.json`:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Обновление зависимостей

Обновление всех пакетов до последних версий в рамках ограничений:

```bash
hpm update
```

Обновление конкретного пакета:

```bash
hpm update hemlang/sprout
```

### Просмотр установленных пакетов

Список всех установленных пакетов:

```bash
hpm list
```

Вывод показывает дерево зависимостей:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Проверка обновлений

Посмотрите, какие пакеты имеют более новые версии:

```bash
hpm outdated
```

### Удаление пакета

```bash
hpm uninstall hemlang/sprout
```

## Пример: Веб-приложение

Вот полный пример использования веб-фреймворка:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

Запуск приложения:

```bash
hpm install
hpm run start
```

## Следующие шаги

- [Справочник команд](commands.md) — Изучите все команды hpm
- [Создание пакетов](creating-packages.md) — Публикуйте свои собственные пакеты
- [Конфигурация](configuration.md) — Настройте hpm и токены GitHub
- [Настройка проекта](project-setup.md) — Детальная конфигурация проекта
