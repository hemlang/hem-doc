# Установка

В этом руководстве описано, как установить hpm на вашу систему.

## Быстрая установка (рекомендуется)

Установите последнюю версию одной командой:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

Это автоматически:
- Определяет вашу операционную систему (Linux, macOS)
- Определяет вашу архитектуру (x86_64, arm64)
- Загружает соответствующий предварительно собранный бинарный файл
- Устанавливает в `/usr/local/bin` (или использует sudo при необходимости)

### Параметры установки

```bash
# Установка в пользовательскую директорию (sudo не требуется)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Установка определённой версии
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Комбинирование параметров
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Поддерживаемые платформы

| Платформа | Архитектура | Статус |
|-----------|-------------|--------|
| Linux    | x86_64       | ✓ Поддерживается |
| macOS    | x86_64       | ✓ Поддерживается |
| macOS    | arm64 (M1/M2/M3) | ✓ Поддерживается |
| Linux    | arm64        | Сборка из исходников |

## Сборка из исходников

Если вы предпочитаете собрать из исходников или вам нужна платформа, для которой нет предварительно собранных бинарных файлов, следуйте этим инструкциям.

### Предварительные требования

hpm требует, чтобы [Hemlock](https://github.com/hemlang/hemlock) был установлен первым. Следуйте инструкциям по установке Hemlock перед продолжением.

Проверьте, что Hemlock установлен:

```bash
hemlock --version
```

## Методы установки

### Метод 1: Make Install

Сборка из исходников и установка.

```bash
# Клонирование репозитория
git clone https://github.com/hemlang/hpm.git
cd hpm

# Установка в /usr/local/bin (требуется sudo)
sudo make install
```

После установки проверьте работоспособность:

```bash
hpm --version
```

### Метод 2: Пользовательское расположение

Установка в пользовательскую директорию (sudo не требуется):

```bash
# Клонирование репозитория
git clone https://github.com/hemlang/hpm.git
cd hpm

# Установка в ~/.local/bin
make install PREFIX=$HOME/.local

# Или любое другое расположение
make install PREFIX=/opt/hemlock
```

Убедитесь, что ваша пользовательская директория bin находится в PATH:

```bash
# Добавьте в ~/.bashrc или ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Метод 3: Запуск без установки

Вы можете запускать hpm напрямую без установки:

```bash
# Клонирование репозитория
git clone https://github.com/hemlang/hpm.git
cd hpm

# Создание локального скрипта-обёртки
make

# Запуск из директории hpm
./hpm --help

# Или запуск через hemlock напрямую
hemlock src/main.hml --help
```

### Метод 4: Ручная установка

Создайте свой собственный скрипт-обёртку:

```bash
# Клонирование в постоянное расположение
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Создание скрипта-обёртки
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Переменные установки

Makefile поддерживает следующие переменные:

| Переменная | По умолчанию | Описание |
|------------|--------------|----------|
| `PREFIX` | `/usr/local` | Префикс установки |
| `BINDIR` | `$(PREFIX)/bin` | Директория бинарных файлов |
| `HEMLOCK` | `hemlock` | Путь к интерпретатору hemlock |

Пример с пользовательскими переменными:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## Как это работает

Установщик создаёт shell-скрипт-обёртку, который вызывает интерпретатор Hemlock с исходным кодом hpm:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

Этот подход:
- Не требует компиляции
- Всегда запускает последний исходный код
- Надёжно работает на всех платформах

## Обновление hpm

Чтобы обновить hpm до последней версии:

```bash
cd /path/to/hpm
git pull origin main

# Переустановите, если путь изменился
sudo make install
```

## Удаление

Удаление hpm из вашей системы:

```bash
cd /path/to/hpm
sudo make uninstall
```

Или удалите вручную:

```bash
sudo rm /usr/local/bin/hpm
```

## Проверка установки

После установки проверьте, что всё работает:

```bash
# Проверка версии
hpm --version

# Просмотр справки
hpm --help

# Тестовая инициализация (в пустой директории)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Устранение неполадок

### "hemlock: command not found"

Hemlock не установлен или не находится в PATH. Сначала установите Hemlock:

```bash
# Проверка существования hemlock
which hemlock

# Если не найден, установите Hemlock с https://github.com/hemlang/hemlock
```

### "Permission denied"

Используйте sudo для системной установки или установите в пользовательскую директорию:

```bash
# Вариант 1: Использовать sudo
sudo make install

# Вариант 2: Установка в пользовательскую директорию
make install PREFIX=$HOME/.local
```

### "hpm: command not found" после установки

Ваш PATH может не включать директорию установки:

```bash
# Проверьте, куда установлен hpm
ls -la /usr/local/bin/hpm

# Добавьте в PATH, если используете пользовательское расположение
export PATH="$HOME/.local/bin:$PATH"
```

## Примечания для конкретных платформ

### Linux

Стандартная установка работает на всех дистрибутивах Linux. Некоторые дистрибутивы могут требовать:

```bash
# Debian/Ubuntu: Установка необходимых инструментов сборки
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

Стандартная установка работает. При использовании Homebrew:

```bash
# Установка инструментов командной строки Xcode
xcode-select --install
```

### Windows (WSL)

hpm работает в подсистеме Windows для Linux:

```bash
# В терминале WSL
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Следующие шаги

После установки:

1. [Быстрый старт](quick-start.md) — Создайте свой первый проект
2. [Справочник команд](commands.md) — Изучите все команды
3. [Конфигурация](configuration.md) — Настройте hpm
