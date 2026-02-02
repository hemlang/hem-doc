# Справочник команд

Полный справочник по всем командам hpm.

## Глобальные параметры

Эти параметры работают с любой командой:

| Параметр | Описание |
|----------|----------|
| `--help`, `-h` | Показать справочное сообщение |
| `--version`, `-v` | Показать версию hpm |
| `--verbose` | Показать подробный вывод |

## Команды

### hpm init

Создание нового файла `package.json`.

```bash
hpm init        # Интерактивный режим
hpm init --yes  # Принять все значения по умолчанию
hpm init -y     # Краткая форма
```

**Параметры:**

| Параметр | Описание |
|----------|----------|
| `--yes`, `-y` | Принять значения по умолчанию для всех запросов |

**Интерактивные запросы:**
- Имя пакета (формат owner/repo)
- Версия (по умолчанию: 1.0.0)
- Описание
- Автор
- Лицензия (по умолчанию: MIT)
- Главный файл (по умолчанию: src/index.hml)

**Пример:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Установка зависимостей или добавление новых пакетов.

```bash
hpm install                           # Установить все из package.json
hpm install owner/repo                # Добавить и установить пакет
hpm install owner/repo@^1.0.0        # С ограничением версии
hpm install owner/repo --dev         # Как зависимость разработки
hpm i owner/repo                      # Краткая форма
```

**Параметры:**

| Параметр | Описание |
|----------|----------|
| `--dev`, `-D` | Добавить в devDependencies |
| `--verbose` | Показать подробный прогресс |
| `--dry-run` | Предпросмотр без установки |
| `--offline` | Установить только из кэша (без сети) |
| `--parallel` | Включить параллельные загрузки (экспериментально) |

**Синтаксис ограничений версий:**

| Синтаксис | Пример | Значение |
|-----------|--------|----------|
| (нет) | `owner/repo` | Последняя версия |
| Точная | `owner/repo@1.2.3` | Ровно 1.2.3 |
| Caret | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Диапазон | `owner/repo@>=1.0.0` | Минимум 1.0.0 |

**Примеры:**

```bash
# Установить все зависимости
hpm install

# Установить конкретный пакет
hpm install hemlang/json

# Установить с ограничением версии
hpm install hemlang/sprout@^2.0.0

# Установить как зависимость разработки
hpm install hemlang/test-utils --dev

# Предпросмотр того, что будет установлено
hpm install hemlang/sprout --dry-run

# Подробный вывод
hpm install --verbose

# Установить только из кэша (офлайн)
hpm install --offline
```

**Вывод:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Удаление пакета.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Краткая форма
hpm remove owner/repo      # Альтернатива
```

**Примеры:**

```bash
hpm uninstall hemlang/sprout
```

**Вывод:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Обновление пакетов до последних версий в рамках ограничений.

```bash
hpm update              # Обновить все пакеты
hpm update owner/repo   # Обновить конкретный пакет
hpm up owner/repo       # Краткая форма
```

**Параметры:**

| Параметр | Описание |
|----------|----------|
| `--verbose` | Показать подробный прогресс |
| `--dry-run` | Предпросмотр без обновления |

**Примеры:**

```bash
# Обновить все пакеты
hpm update

# Обновить конкретный пакет
hpm update hemlang/sprout

# Предпросмотр обновлений
hpm update --dry-run
```

**Вывод:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Показать установленные пакеты.

```bash
hpm list              # Показать полное дерево зависимостей
hpm list --depth=0    # Только прямые зависимости
hpm list --depth=1    # Один уровень транзитивных зависимостей
hpm ls                # Краткая форма
```

**Параметры:**

| Параметр | Описание |
|----------|----------|
| `--depth=N` | Ограничить глубину дерева (по умолчанию: все) |

**Примеры:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Показать пакеты с доступными более новыми версиями.

```bash
hpm outdated
```

**Вывод:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: Установленная версия
- **Wanted**: Наивысшая версия, соответствующая ограничению
- **Latest**: Последняя доступная версия

---

### hpm run

Выполнение скрипта из package.json.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Примеры:**

Для данного package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Запуск скриптов:

```bash
hpm run start
hpm run test
hpm run build

# Передача аргументов скрипту
hpm run test -- --verbose
```

---

### hpm test

Сокращение для `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Эквивалентно:

```bash
hpm run test
```

---

### hpm why

Объяснение, почему пакет установлен (показать цепочку зависимостей).

```bash
hpm why owner/repo
```

**Пример:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Управление глобальным кэшем пакетов.

```bash
hpm cache list    # Показать кэшированные пакеты
hpm cache clean   # Очистить все кэшированные пакеты
```

**Подкоманды:**

| Подкоманда | Описание |
|------------|----------|
| `list` | Показать все кэшированные пакеты и их размеры |
| `clean` | Удалить все кэшированные пакеты |

**Примеры:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Сокращения команд

Для удобства несколько команд имеют короткие псевдонимы:

| Команда | Сокращения |
|---------|------------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Примеры:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Коды выхода

hpm использует специфические коды выхода для обозначения различных условий ошибок:

| Код | Значение |
|-----|----------|
| 0 | Успех |
| 1 | Конфликт зависимостей |
| 2 | Пакет не найден |
| 3 | Версия не найдена |
| 4 | Сетевая ошибка |
| 5 | Недопустимый package.json |
| 6 | Проверка целостности не пройдена |
| 7 | Превышен лимит запросов GitHub |
| 8 | Циклическая зависимость |

Использование кодов выхода в скриптах:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## Переменные окружения

hpm учитывает следующие переменные окружения:

| Переменная | Описание |
|------------|----------|
| `GITHUB_TOKEN` | Токен GitHub API для аутентификации |
| `HPM_CACHE_DIR` | Переопределить расположение директории кэша |
| `HOME` | Домашняя директория пользователя (для конфигурации/кэша) |

**Примеры:**

```bash
# Использовать токен GitHub для более высоких лимитов запросов
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Использовать пользовательскую директорию кэша
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## См. также

- [Конфигурация](configuration.md) — Файлы конфигурации
- [Спецификация пакетов](package-spec.md) — Формат package.json
- [Устранение неполадок](troubleshooting.md) — Распространённые проблемы
