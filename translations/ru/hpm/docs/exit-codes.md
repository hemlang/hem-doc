# Коды выхода

Справочник по кодам выхода hpm и их значениям.

## Таблица кодов выхода

| Код | Название | Описание |
|-----|----------|----------|
| 0 | SUCCESS | Команда выполнена успешно |
| 1 | CONFLICT | Конфликт версий зависимостей |
| 2 | NOT_FOUND | Пакет не найден |
| 3 | VERSION_NOT_FOUND | Запрошенная версия не найдена |
| 4 | NETWORK | Сетевая ошибка |
| 5 | INVALID_MANIFEST | Недопустимый package.json |
| 6 | INTEGRITY | Проверка целостности не пройдена |
| 7 | RATE_LIMIT | Превышен лимит GitHub API |
| 8 | CIRCULAR | Обнаружена циклическая зависимость |

## Подробные описания

### Код выхода 0: SUCCESS

Команда выполнена успешно.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Код выхода 1: CONFLICT

Два или более пакетов требуют несовместимых версий зависимости.

**Пример:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Решения:**
1. Проверить, какие пакеты в конфликте:
   ```bash
   hpm why hemlang/json
   ```
2. Обновить конфликтующий пакет:
   ```bash
   hpm update package-a
   ```
3. Ослабить ограничения версий в package.json
4. Удалить один из конфликтующих пакетов

### Код выхода 2: NOT_FOUND

Указанный пакет не существует на GitHub.

**Пример:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Решения:**
1. Проверить орфографию имени пакета
2. Убедиться, что репозиторий существует: `https://github.com/owner/repo`
3. Проверить доступ (для приватных репозиториев установите GITHUB_TOKEN)

### Код выхода 3: VERSION_NOT_FOUND

Ни одна версия не соответствует указанному ограничению.

**Пример:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Решения:**
1. Проверить доступные версии в релизах/тегах на GitHub
2. Использовать допустимое ограничение версии
3. Теги версий должны начинаться с 'v' (например, `v1.0.0`)

### Код выхода 4: NETWORK

Произошла сетевая ошибка.

**Пример:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Решения:**
1. Проверить интернет-соединение
2. Проверить доступность GitHub
3. Проверить настройки прокси, если за файрволом
4. Использовать `--offline`, если пакеты в кэше:
   ```bash
   hpm install --offline
   ```
5. Подождать и повторить (hpm повторяет автоматически)

### Код выхода 5: INVALID_MANIFEST

Файл package.json недопустим или имеет неправильный формат.

**Пример:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Решения:**
1. Проверить синтаксис JSON (используйте JSON-валидатор)
2. Убедиться, что обязательные поля существуют (`name`, `version`)
3. Проверить форматы полей:
   - name: формат `owner/repo`
   - version: формат semver `X.Y.Z`
4. Регенерировать:
   ```bash
   rm package.json
   hpm init
   ```

### Код выхода 6: INTEGRITY

Проверка целостности пакета не пройдена.

**Пример:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Решения:**
1. Очистить кэш и переустановить:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Проверить сетевые проблемы (неполные загрузки)
3. Убедиться, что пакет не был изменён

### Код выхода 7: RATE_LIMIT

Превышен лимит запросов GitHub API.

**Пример:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Решения:**
1. **Аутентификация с GitHub** (рекомендуется):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Дождаться сброса лимита (сбрасывается ежечасно)
3. Использовать офлайн-режим, если пакеты в кэше:
   ```bash
   hpm install --offline
   ```

### Код выхода 8: CIRCULAR

Обнаружена циклическая зависимость в графе зависимостей.

**Пример:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**Решения:**
1. Обычно это баг в самих пакетах
2. Свяжитесь с мейнтейнерами пакетов
3. Избегайте использования одного из циклических пакетов

## Использование кодов выхода в скриптах

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## Устранение неполадок по коду выхода

### Краткий справочник

| Код | Что проверить в первую очередь |
|-----|--------------------------------|
| 1 | Запустить `hpm why <package>` для просмотра конфликта |
| 2 | Проверить имя пакета на GitHub |
| 3 | Проверить доступные версии в тегах на GitHub |
| 4 | Проверить интернет-соединение |
| 5 | Проверить синтаксис package.json |
| 6 | Запустить `hpm cache clean && hpm install` |
| 7 | Установить переменную окружения `GITHUB_TOKEN` |
| 8 | Связаться с мейнтейнерами пакетов |

## См. также

- [Устранение неполадок](troubleshooting.md) — Детальные решения
- [Команды](commands.md) — Справочник команд
- [Конфигурация](configuration.md) — Настройка токена GitHub
