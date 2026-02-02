# Устранение неполадок

Решения распространённых проблем hpm.

## Проблемы установки

### "hemlock: command not found"

**Причина:** Hemlock не установлен или не в PATH.

**Решение:**

```bash
# Проверить, существует ли hemlock
which hemlock

# Если не найден, сначала установите Hemlock
# Посетите: https://github.com/hemlang/hemlock

# После установки проверьте
hemlock --version
```

### "hpm: command not found"

**Причина:** hpm не установлен или не в PATH.

**Решение:**

```bash
# Проверить, куда установлен hpm
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# Если используете пользовательское расположение, добавьте в PATH
export PATH="$HOME/.local/bin:$PATH"

# Добавьте в ~/.bashrc или ~/.zshrc для постоянного эффекта
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# При необходимости переустановите
cd /path/to/hpm
sudo make install
```

### "Permission denied" при установке

**Причина:** Нет прав на запись в директорию установки.

**Решение:**

```bash
# Вариант 1: Использовать sudo для системной установки
sudo make install

# Вариант 2: Установить в пользовательскую директорию (без sudo)
make install PREFIX=$HOME/.local
```

## Проблемы с зависимостями

### "Package not found" (код выхода 2)

**Причина:** Пакет не существует на GitHub.

**Решение:**

```bash
# Проверить, существует ли пакет
# Проверьте: https://github.com/owner/repo

# Проверить орфографию
hpm install hemlang/sprout  # Правильно
hpm install hemlan/sprout   # Неправильный owner
hpm install hemlang/spout   # Неправильный repo

# Проверить опечатки в package.json
cat package.json | grep -A 5 dependencies
```

### "Version not found" (код выхода 3)

**Причина:** Ни один релиз не соответствует ограничению версии.

**Решение:**

```bash
# Проверить доступные версии (проверьте релизы/теги на GitHub)
# Теги должны начинаться с 'v' (например, v1.0.0)

# Использовать допустимое ограничение версии
hpm install owner/repo@^1.0.0

# Попробовать последнюю версию
hpm install owner/repo

# Проверить доступные теги на GitHub
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (код выхода 1)

**Причина:** Два пакета требуют несовместимых версий зависимости.

**Решение:**

```bash
# Увидеть конфликт
hpm install --verbose

# Проверить, что требует зависимость
hpm why conflicting/package

# Решения:
# 1. Обновить конфликтующий пакет
hpm update problem/package

# 2. Изменить ограничения версий в package.json
# Отредактировать для разрешения совместимых версий

# 3. Удалить один из конфликтующих пакетов
hpm uninstall one/package
```

### "Circular dependency" (код выхода 8)

**Причина:** Пакет A зависит от B, который зависит от A.

**Решение:**

```bash
# Определить цикл
hpm install --verbose

# Обычно это баг в пакетах
# Свяжитесь с мейнтейнерами пакетов

# Обходной путь: избегайте один из пакетов
```

## Сетевые проблемы

### "Network error" (код выхода 4)

**Причина:** Невозможно подключиться к GitHub API.

**Решение:**

```bash
# Проверить интернет-соединение
ping github.com

# Проверить доступность GitHub API
curl -I https://api.github.com

# Попробовать снова (hpm повторяет автоматически)
hpm install

# Использовать офлайн-режим, если пакеты в кэше
hpm install --offline

# Проверить настройки прокси, если за файрволом
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (код выхода 7)

**Причина:** Слишком много API-запросов без аутентификации.

**Решение:**

```bash
# Вариант 1: Аутентификация с токеном GitHub (рекомендуется)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Создать токен: GitHub → Settings → Developer settings → Personal access tokens

# Вариант 2: Сохранить токен в файле конфигурации
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Вариант 3: Дождаться сброса лимита (сбрасывается ежечасно)

# Вариант 4: Использовать офлайн-режим
hpm install --offline
```

### Тайм-аут соединения

**Причина:** Медленная сеть или проблемы GitHub API.

**Решение:**

```bash
# hpm автоматически повторяет с экспоненциальной задержкой

# Проверить, есть ли проблемы у GitHub
# Посетите: https://www.githubstatus.com

# Попробовать позже
hpm install

# Использовать кэшированные пакеты
hpm install --offline
```

## Проблемы с Package.json

### "Invalid package.json" (код выхода 5)

**Причина:** Неправильный формат или отсутствуют обязательные поля.

**Решение:**

```bash
# Проверить синтаксис JSON
cat package.json | python -m json.tool

# Проверить обязательные поля
cat package.json

# Обязательные поля:
# - "name": формат "owner/repo"
# - "version": формат "X.Y.Z"

# При необходимости регенерировать
rm package.json
hpm init
```

### Ошибка формата "name"

**Причина:** Имя пакета не в формате `owner/repo`.

**Решение:**

```json
// Неправильно
{
  "name": "my-package"
}

// Правильно
{
  "name": "yourusername/my-package"
}
```

### Ошибка формата "version"

**Причина:** Версия не в формате semver.

**Решение:**

```json
// Неправильно
{
  "version": "1.0"
}

// Правильно
{
  "version": "1.0.0"
}
```

## Проблемы с файлом блокировки

### Файл блокировки не синхронизирован

**Причина:** package.json изменён без запуска install.

**Решение:**

```bash
# Регенерировать файл блокировки
rm package-lock.json
hpm install
```

### Повреждённый файл блокировки

**Причина:** Недопустимый JSON или ручные правки.

**Решение:**

```bash
# Проверить валидность JSON
cat package-lock.json | python -m json.tool

# Регенерировать
rm package-lock.json
hpm install
```

## Проблемы с hem_modules

### Пакеты не устанавливаются

**Причина:** Различные возможные проблемы.

**Решение:**

```bash
# Очистить и переустановить
rm -rf hem_modules
hpm install

# Проверить подробный вывод
hpm install --verbose
```

### Импорт не работает

**Причина:** Пакет не установлен правильно или неверный путь импорта.

**Решение:**

```bash
# Проверить, установлен ли пакет
ls hem_modules/owner/repo/

# Проверить поле main в package.json
cat hem_modules/owner/repo/package.json

# Правильный формат импорта
import { x } from "owner/repo";          # Использует main entry
import { y } from "owner/repo/subpath";  # Импорт из подпути
```

### Ошибка "Module not found"

**Причина:** Путь импорта не разрешается в файл.

**Решение:**

```bash
# Проверить путь импорта
ls hem_modules/owner/repo/src/

# Проверить наличие index.hml
ls hem_modules/owner/repo/src/index.hml

# Проверить поле main в package.json
cat hem_modules/owner/repo/package.json | grep main
```

## Проблемы с кэшем

### Кэш занимает слишком много места

**Решение:**

```bash
# Просмотр размера кэша
hpm cache list

# Очистка кэша
hpm cache clean
```

### Права доступа к кэшу

**Решение:**

```bash
# Исправить права доступа
chmod -R u+rw ~/.hpm/cache

# Или удалить и переустановить
rm -rf ~/.hpm/cache
hpm install
```

### Использование неправильного кэша

**Решение:**

```bash
# Проверить расположение кэша
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Очистить переменную окружения, если неверная
unset HPM_CACHE_DIR
```

## Проблемы со скриптами

### "Script not found"

**Причина:** Имя скрипта не существует в package.json.

**Решение:**

```bash
# Список доступных скриптов
cat package.json | grep -A 20 scripts

# Проверить орфографию
hpm run test    # Правильно
hpm run tests   # Неправильно, если скрипт называется "test"
```

### Скрипт завершается с ошибкой

**Причина:** Ошибка в команде скрипта.

**Решение:**

```bash
# Запустить команду напрямую, чтобы увидеть ошибку
hemlock test/run.hml

# Проверить определение скрипта
cat package.json | grep test
```

## Отладка

### Включить подробный вывод

```bash
hpm install --verbose
```

### Проверить версию hpm

```bash
hpm --version
```

### Проверить версию hemlock

```bash
hemlock --version
```

### Пробный запуск

Предпросмотр без внесения изменений:

```bash
hpm install --dry-run
```

### Чистый старт

Начать заново:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Получение помощи

### Справка по командам

```bash
hpm --help
hpm install --help
```

### Сообщение о проблемах

Если вы столкнулись с багом:

1. Проверьте существующие issue: https://github.com/hemlang/hpm/issues
2. Создайте новую issue с:
   - Версией hpm (`hpm --version`)
   - Версией Hemlock (`hemlock --version`)
   - Операционной системой
   - Шагами воспроизведения
   - Сообщением об ошибке (используйте `--verbose`)

## Справочник кодов выхода

| Код | Значение | Типичное решение |
|-----|----------|------------------|
| 0 | Успех | - |
| 1 | Конфликт зависимостей | Обновить или изменить ограничения |
| 2 | Пакет не найден | Проверить орфографию, убедиться, что репо существует |
| 3 | Версия не найдена | Проверить доступные версии на GitHub |
| 4 | Сетевая ошибка | Проверить соединение, повторить |
| 5 | Недопустимый package.json | Исправить синтаксис JSON и обязательные поля |
| 6 | Проверка целостности не пройдена | Очистить кэш, переустановить |
| 7 | Лимит GitHub | Добавить GITHUB_TOKEN |
| 8 | Циклическая зависимость | Связаться с мейнтейнерами пакетов |

## См. также

- [Установка](installation.md) — Руководство по установке
- [Конфигурация](configuration.md) — Параметры конфигурации
- [Команды](commands.md) — Справочник команд
