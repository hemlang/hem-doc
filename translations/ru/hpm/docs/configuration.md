# Конфигурация

В этом руководстве описаны все параметры конфигурации hpm.

## Обзор

hpm можно настроить через:

1. **Переменные окружения** — Для настроек времени выполнения
2. **Глобальный файл конфигурации** — `~/.hpm/config.json`
3. **Файлы проекта** — `package.json` и `package-lock.json`

## Переменные окружения

### GITHUB_TOKEN

Токен GitHub API для аутентификации.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Преимущества аутентификации:**
- Более высокие лимиты API-запросов (5000 против 60 запросов/час)
- Доступ к приватным репозиториям
- Более быстрое разрешение зависимостей

**Создание токена:**

1. Перейдите в GitHub → Settings → Developer settings → Personal access tokens
2. Нажмите "Generate new token (classic)"
3. Выберите области доступа:
   - `repo` — Для доступа к приватным репозиториям
   - `read:packages` — Для GitHub Packages (если используется)
4. Сгенерируйте и скопируйте токен

### HPM_CACHE_DIR

Переопределение директории кэша по умолчанию.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

По умолчанию: `~/.hpm/cache`

**Случаи использования:**
- CI/CD системы с пользовательскими расположениями кэша
- Общий кэш для нескольких проектов
- Временный кэш для изолированных сборок

### HOME

Домашняя директория пользователя. Используется для определения расположения:
- Директории конфигурации: `$HOME/.hpm/`
- Директории кэша: `$HOME/.hpm/cache/`

Обычно устанавливается системой; переопределяйте только при необходимости.

### Пример .bashrc / .zshrc

```bash
# Аутентификация GitHub (рекомендуется)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Пользовательское расположение кэша (опционально)
# export HPM_CACHE_DIR=/path/to/cache

# Добавление hpm в PATH (если используется пользовательское расположение установки)
export PATH="$HOME/.local/bin:$PATH"
```

## Глобальный файл конфигурации

### Расположение

`~/.hpm/config.json`

### Формат

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Создание файла конфигурации

```bash
# Создание директории конфигурации
mkdir -p ~/.hpm

# Создание файла конфигурации
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Защита файла (рекомендуется)
chmod 600 ~/.hpm/config.json
```

### Приоритет токена

Если установлены оба источника, переменная окружения имеет приоритет:

1. Переменная окружения `GITHUB_TOKEN` (высший приоритет)
2. Поле `github_token` в `~/.hpm/config.json`
3. Без аутентификации (по умолчанию)

## Структура директорий

### Глобальные директории

```
~/.hpm/
├── config.json          # Глобальная конфигурация
└── cache/               # Кэш пакетов
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Директории проекта

```
my-project/
├── package.json         # Манифест проекта
├── package-lock.json    # Файл блокировки зависимостей
├── hem_modules/         # Установленные пакеты
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Исходный код
└── test/                # Тесты
```

## Кэш пакетов

### Расположение

По умолчанию: `~/.hpm/cache/`

Переопределяется переменной окружения: `HPM_CACHE_DIR`

### Структура

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Управление кэшем

```bash
# Просмотр кэшированных пакетов
hpm cache list

# Очистка всего кэша
hpm cache clean
```

### Поведение кэша

- Пакеты кэшируются после первой загрузки
- Последующие установки используют кэшированные версии
- Используйте `--offline` для установки только из кэша
- Кэш общий для всех проектов

## Лимиты запросов GitHub API

### Без аутентификации

- **60 запросов в час** на IP-адрес
- Общий для всех неаутентифицированных пользователей на одном IP
- Быстро исчерпывается в CI/CD или при большом количестве зависимостей

### С аутентификацией

- **5000 запросов в час** на аутентифицированного пользователя
- Персональный лимит, не общий

### Обработка лимитов

hpm автоматически:
- Повторяет попытки с экспоненциальной задержкой (1с, 2с, 4с, 8с)
- Сообщает об ошибках лимита с кодом выхода 7
- Предлагает аутентификацию при достижении лимита

**Решения при превышении лимита:**

```bash
# Вариант 1: Аутентификация с токеном GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Вариант 2: Дождаться сброса лимита
# (Лимиты сбрасываются ежечасно)

# Вариант 3: Использовать офлайн-режим (если пакеты в кэше)
hpm install --offline
```

## Офлайн-режим

Установка пакетов без сетевого доступа:

```bash
hpm install --offline
```

**Требования:**
- Все пакеты должны быть в кэше
- Файл блокировки должен существовать с точными версиями

**Случаи использования:**
- Изолированные среды
- Более быстрые сборки CI/CD (с прогретым кэшем)
- Избежание лимитов запросов

## Конфигурация CI/CD

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Установка Hemlock (настройте под вашу среду)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Сначала копируем файлы пакета (для кэширования слоёв)
COPY package.json package-lock.json ./

# Установка зависимостей
RUN hpm install

# Копирование исходного кода
COPY . .

# Запуск приложения
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Конфигурация прокси

Для сред за прокси-сервером настройте на системном уровне:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Лучшие практики безопасности

### Безопасность токена

1. **Никогда не коммитьте токены** в систему контроля версий
2. **Используйте переменные окружения** в CI/CD
3. **Ограничивайте области токена** до минимально необходимых
4. **Регулярно меняйте токены**
5. **Защитите файл конфигурации**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Приватные репозитории

Для доступа к приватным пакетам:

1. Создайте токен с областью `repo`
2. Настройте аутентификацию (переменная окружения или файл конфигурации)
3. Убедитесь, что токен имеет доступ к репозиторию

```bash
# Проверка доступа
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Устранение проблем конфигурации

### Проверка конфигурации

```bash
# Проверка, установлен ли токен
echo $GITHUB_TOKEN | head -c 10

# Проверка файла конфигурации
cat ~/.hpm/config.json

# Проверка директории кэша
ls -la ~/.hpm/cache/

# Тест с подробным выводом
hpm install --verbose
```

### Распространённые проблемы

**"GitHub rate limit exceeded"**
- Настройте аутентификацию с `GITHUB_TOKEN`
- Дождитесь сброса лимита
- Используйте `--offline`, если пакеты в кэше

**"Permission denied" для кэша**
```bash
# Исправление прав доступа к кэшу
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Создание директории конфигурации
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## См. также

- [Установка](installation.md) — Установка hpm
- [Устранение неполадок](troubleshooting.md) — Распространённые проблемы
- [Команды](commands.md) — Справочник команд
