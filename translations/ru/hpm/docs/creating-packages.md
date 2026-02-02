# Создание пакетов

В этом руководстве описано, как создавать, структурировать и публиковать пакеты Hemlock.

## Обзор

hpm использует GitHub в качестве реестра пакетов. Пакеты идентифицируются по пути GitHub `owner/repo`, а версии — это Git-теги. Публикация — это просто отправка тегированного релиза.

## Создание нового пакета

### 1. Инициализация пакета

Создайте новую директорию и инициализируйте:

```bash
mkdir my-package
cd my-package
hpm init
```

Ответьте на запросы:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Создание структуры проекта

Рекомендуемая структура для пакетов:

```
my-package/
├── package.json          # Манифест пакета
├── README.md             # Документация
├── LICENSE               # Файл лицензии
├── src/
│   ├── index.hml         # Главная точка входа (экспортирует публичный API)
│   ├── utils.hml         # Внутренние утилиты
│   └── types.hml         # Определения типов
└── test/
    ├── framework.hml     # Тестовый фреймворк
    └── test_utils.hml    # Тесты
```

### 3. Определение публичного API

**src/index.hml** — Главная точка входа:

```hemlock
// Реэкспорт публичного API
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Прямые экспорты
export fn create(options: Options): Config {
    // Реализация
}

export fn validate(config: Config): bool {
    // Реализация
}
```

### 4. Написание package.json

Полный пример package.json:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Именование пакетов

### Требования

- Должно быть в формате `owner/repo`
- `owner` должен быть вашим именем пользователя или организацией на GitHub
- `repo` должен быть именем репозитория
- Используйте нижний регистр с дефисами для многословных названий

### Хорошие имена

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### Избегайте

```
my-package          # Отсутствует owner
alice/MyPackage     # PascalCase
alice/my_package    # Подчёркивания
```

## Лучшие практики структуры пакета

### Точка входа

Поле `main` в package.json указывает точку входа:

```json
{
  "main": "src/index.hml"
}
```

Этот файл должен экспортировать ваш публичный API:

```hemlock
// Экспортируйте всё, что нужно пользователям
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Типы
export type { Config, Options } from "./types.hml";
```

### Внутреннее vs публичное

Держите детали внутренней реализации приватными:

```
src/
├── index.hml          # Публичный: экспортируемый API
├── parser.hml         # Публичный: используется в index.hml
├── formatter.hml      # Публичный: используется в index.hml
└── internal/
    ├── helpers.hml    # Приватный: только для внутреннего использования
    └── constants.hml  # Приватный: только для внутреннего использования
```

Пользователи импортируют из корня вашего пакета:

```hemlock
// Хорошо - импорт из публичного API
import { parse, Parser } from "yourusername/my-package";

// Тоже работает - импорт из подпути
import { validate } from "yourusername/my-package/validator";

// Не рекомендуется - доступ к внутренним компонентам
import { helper } from "yourusername/my-package/internal/helpers";
```

### Экспорт подпутей

Поддержка импорта из подпутей:

```
src/
├── index.hml              # Главная точка входа
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Пользователи могут импортировать:

```hemlock
import { parse } from "yourusername/my-package";           // Главный
import { Parser } from "yourusername/my-package/parser";   // Подпуть
import { format } from "yourusername/my-package/formatter";
```

## Зависимости

### Добавление зависимостей

```bash
# Зависимость времени выполнения
hpm install hemlang/json

# Зависимость разработки
hpm install hemlang/test-utils --dev
```

### Лучшие практики для зависимостей

1. **Используйте caret-диапазоны** для большинства зависимостей:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Фиксируйте версии** только при необходимости (нестабильность API):
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Избегайте слишком строгих диапазонов**:
   ```json
   // Плохо: слишком строго
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Хорошо: позволяет совместимые обновления
   "hemlang/json": "^1.2.3"
   ```

4. **Разделяйте dev-зависимости**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Тестирование пакета

### Написание тестов

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Запуск тестов

Добавьте скрипт test:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Запуск:

```bash
hpm test
```

## Публикация

### Предварительные требования

1. Создайте GitHub-репозиторий, соответствующий имени вашего пакета
2. Убедитесь, что `package.json` полный и валидный
3. Все тесты проходят

### Процесс публикации

Публикация — это просто отправка Git-тега:

```bash
# 1. Убедитесь, что всё закоммичено
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Создайте тег версии (должен начинаться с 'v')
git tag v1.0.0

# 3. Отправьте код и теги
git push origin main
git push origin v1.0.0
# Или отправьте все теги сразу
git push origin main --tags
```

### Теги версий

Теги должны следовать формату `vX.Y.Z`:

```bash
git tag v1.0.0      # Релиз
git tag v1.0.1      # Патч
git tag v1.1.0      # Минорный
git tag v2.0.0      # Мажорный
git tag v1.0.0-beta.1  # Пре-релиз
```

### Чек-лист релиза

Перед публикацией новой версии:

1. **Обновите версию** в package.json
2. **Запустите тесты**: `hpm test`
3. **Обновите CHANGELOG** (если есть)
4. **Обновите README** при изменении API
5. **Закоммитьте изменения**
6. **Создайте тег**
7. **Отправьте на GitHub**

### Пример автоматизации

Создайте скрипт релиза:

```bash
#!/bin/bash
# release.sh - Выпуск новой версии

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Запуск тестов
hpm test || exit 1

# Обновление версии в package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Коммит и тег
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Отправка
git push origin main --tags

echo "Released v$VERSION"
```

## Установка вашего пакета пользователями

После публикации пользователи могут установить:

```bash
# Последняя версия
hpm install yourusername/my-package

# Конкретная версия
hpm install yourusername/my-package@1.0.0

# Ограничение версии
hpm install yourusername/my-package@^1.0.0
```

И импортировать:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Документация

### README.md

Каждый пакет должен иметь README:

```markdown
# my-package

Краткое описание того, что делает этот пакет.

## Установка

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Использование

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Парсит входную строку.

### stringify(obj: any): string

Преобразует объект в строку.

## Лицензия

MIT
```

### Документация API

Документируйте все публичные экспорты:

```hemlock
/// Парсит входную строку в структурированный Result.
///
/// # Аргументы
/// * `input` - Строка для парсинга
///
/// # Возвращает
/// Result, содержащий распарсенные данные или ошибку
///
/// # Пример
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Реализация
}
```

## Рекомендации по версионированию

Следуйте [Семантическому версионированию](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Несовместимые изменения
- **MINOR** (1.0.0 → 1.1.0): Новые возможности, обратно совместимые
- **PATCH** (1.0.0 → 1.0.1): Исправления ошибок, обратно совместимые

### Когда увеличивать

| Тип изменения | Увеличение версии |
|---------------|-------------------|
| Несовместимое изменение API | MAJOR |
| Удаление функции/типа | MAJOR |
| Изменение сигнатуры функции | MAJOR |
| Добавление новой функции | MINOR |
| Добавление новой возможности | MINOR |
| Исправление ошибки | PATCH |
| Обновление документации | PATCH |
| Внутренний рефакторинг | PATCH |

## См. также

- [Спецификация пакетов](package-spec.md) — Полный справочник package.json
- [Версионирование](versioning.md) — Детали семантического версионирования
- [Конфигурация](configuration.md) — Аутентификация GitHub
