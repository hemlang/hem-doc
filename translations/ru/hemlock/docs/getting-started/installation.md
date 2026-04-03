# Установка

Это руководство поможет вам собрать и установить Hemlock на вашей системе.

## Быстрая установка (Рекомендуется)

Самый простой способ установить Hemlock - использовать однострочный скрипт установки:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash
```

Скрипт загружает и устанавливает последний предварительно собранный бинарный файл для вашей платформы (Linux или macOS, x86_64 или arm64).

### Параметры установки

```bash
# Установка в пользовательский префикс (по умолчанию: ~/.local)
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --prefix /usr/local

# Установка определённой версии
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --version v1.6.0

# Установка с автоматическим обновлением PATH в оболочке
curl -fsSL https://raw.githubusercontent.com/hemlang/hemlock/main/install.sh | bash -s -- --update-path
```

После установки проверьте работоспособность:

```bash
hemlock --version
```

---

## Сборка из исходного кода

Если вы предпочитаете собирать из исходного кода или предварительно собранные бинарные файлы не работают на вашей системе, следуйте инструкциям ниже.

## Требования

### Необходимые зависимости

Для сборки Hemlock требуются следующие зависимости:

- **Компилятор C**: GCC или Clang (стандарт C11)
- **Make**: GNU Make
- **libffi**: Библиотека Foreign Function Interface (для поддержки FFI)
- **OpenSSL**: Криптографическая библиотека (для хеш-функций: md5, sha1, sha256)
- **libwebsockets**: Поддержка WebSocket и HTTP клиента/сервера
- **zlib**: Библиотека сжатия

### Установка зависимостей

**macOS:**
```bash
# Установите Homebrew, если ещё не установлен
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установите Xcode Command Line Tools
xcode-select --install

# Установите зависимости через Homebrew
brew install libffi openssl@3 libwebsockets
```

**Примечание для пользователей macOS**: Makefile автоматически определяет установки Homebrew и устанавливает правильные пути к заголовочным файлам и библиотекам. Hemlock поддерживает архитектуры Intel (x86_64) и Apple Silicon (arm64).

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential libffi-dev libssl-dev libwebsockets-dev zlib1g-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install gcc make libffi-devel openssl-devel libwebsockets-devel zlib-devel
```

**Arch Linux:**
```bash
sudo pacman -S base-devel libffi openssl libwebsockets zlib
```

## Сборка из исходного кода

### 1. Клонирование репозитория

```bash
git clone https://github.com/hemlang/hemlock.git
cd hemlock
```

### 2. Сборка Hemlock

```bash
make
```

Это скомпилирует интерпретатор Hemlock и поместит исполняемый файл в текущую директорию.

### 3. Проверка установки

```bash
./hemlock --version
```

Вы должны увидеть информацию о версии Hemlock.

### 4. Тестирование сборки

Запустите набор тестов, чтобы убедиться, что всё работает правильно:

```bash
make test
```

Все тесты должны пройти успешно. Если вы видите ошибки, пожалуйста, сообщите о них как о проблеме.

## Общесистемная установка (Опционально)

Для общесистемной установки Hemlock (например, в `/usr/local/bin`):

```bash
sudo make install
```

Это позволит запускать `hemlock` из любого места без указания полного пути.

## Запуск Hemlock

### Интерактивный REPL

Запустите цикл чтения-вычисления-вывода (Read-Eval-Print Loop):

```bash
./hemlock
```

Вы увидите приглашение, где можно вводить код Hemlock:

```
Hemlock REPL
> print("Hello, World!");
Hello, World!
> let x = 42;
> print(x * 2);
84
>
```

Выйдите из REPL с помощью `Ctrl+D` или `Ctrl+C`.

### Запуск программ

Выполните скрипт Hemlock:

```bash
./hemlock program.hml
```

С аргументами командной строки:

```bash
./hemlock program.hml arg1 arg2 "аргумент с пробелами"
```

## Структура директорий

После сборки ваша директория Hemlock будет выглядеть так:

```
hemlock/
├── hemlock           # Скомпилированный исполняемый файл интерпретатора
├── src/              # Исходный код
├── include/          # Заголовочные файлы
├── tests/            # Набор тестов
├── examples/         # Примеры программ
├── docs/             # Документация
├── stdlib/           # Стандартная библиотека
├── Makefile          # Конфигурация сборки
└── README.md         # README проекта
```

## Сборка WebAssembly (WASM)

Hemlock можно скомпилировать в WebAssembly через [Emscripten](https://emscripten.org/), что позволяет полному интерпретатору работать в веб-браузере или Node.js.

### Установка Emscripten

Emscripten SDK (`emsdk`) предоставляет компилятор `emcc`, используемый для сборки WASM-интерпретатора.

**Все платформы (Linux, macOS, Windows WSL):**

```bash
# Clone the emsdk repository
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk

# Install and activate the latest SDK
./emsdk install latest
./emsdk activate latest

# Add emcc to your PATH (run this in every new terminal, or add to your shell profile)
source ./emsdk_env.sh
```

Проверьте установку:

```bash
emcc --version
```

Вы должны увидеть вывод вроде `emcc (Emscripten gcc/clang-like replacement ...) 3.x.x`.

Подробные инструкции см. в [руководстве по началу работы с Emscripten](https://emscripten.org/docs/getting_started/downloads.html).

**Необязательно: Добавление в профиль оболочки**

Чтобы не выполнять `source emsdk_env.sh` каждый раз, добавьте его в профиль вашей оболочки:

```bash
# For bash (~/.bashrc or ~/.bash_profile)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.bashrc

# For zsh (~/.zshrc)
echo 'source /path/to/emsdk/emsdk_env.sh' >> ~/.zshrc
```

### Зависимости WASM

WASM-сборка имеет меньше зависимостей, чем нативная сборка. Emscripten предоставляет собственные версии стандартных библиотек C. Следующие нативные библиотеки **не нужны** (и недоступны) в WASM-сборке:

| Библиотека | Нативная | WASM | Примечания |
|---------|--------|------|-------|
| libffi | Требуется | Заглушка | FFI недоступен в WASM |
| OpenSSL | Требуется | Заглушка | Встроенные криптофункции возвращают ошибки в WASM |
| libwebsockets | Опционально | Заглушка | Поддержка WebSocket недоступна |
| zlib | Требуется | Emscripten предоставляет | Автоматически подключается с `-sUSE_ZLIB=1` |
| pthreads | Требуется | Опционально | Доступно с потоковой сборкой (требуется SharedArrayBuffer) |

**Коротко:** Вам нужен только установленный Emscripten SDK. Для WASM-сборки не требуются дополнительные системные библиотеки.

### Сборка WASM-интерпретатора

```bash
# Build the interpreter as WebAssembly
make wasm-interpreter
```

Это создаёт два файла в директории `wasm/`:

| Файл | Описание |
|------|-------------|
| `wasm/hemlock.js` | JavaScript-загрузчик и связующий код Emscripten |
| `wasm/hemlock.wasm` | Бинарный модуль WebAssembly |

### Запуск в Node.js

```bash
node -- wasm/hemlock.js -e 'print("Hello from WASM!");'
node -- wasm/hemlock.js examples/fibonacci.hml
```

### Запуск в браузере

WASM-файлы должны раздаваться по HTTP с правильным MIME-типом (`application/wasm`). Открытие HTML-файла напрямую через `file://` не будет работать.

**С использованием включённого примера:**

```bash
make wasm-browser-example
# Opens http://localhost:8080/examples/wasm-browser/index.html
```

**Или вручную с Python:**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/wasm/playground.html
```

**Или вручную с Node.js:**

```bash
npx serve .
# Open the URL shown in the terminal
```

См. `examples/wasm-browser/` для полного примера интеграции с браузером с интерактивным редактором кода.

### Ограничения WASM

Некоторые функции недоступны в среде WASM:

- **FFI** - Невозможна загрузка разделяемых библиотек (`dlopen`/`dlsym`)
- **Криптография** - Нет OpenSSL (`sha256`, `md5` и т.д. возвращают ошибки)
- **Файловый ввод/вывод** - Нет доступа к нативной файловой системе (только виртуальная ФС Emscripten)
- **Сеть** - Нет сырых сокетов или HTTP-клиента
- **Сигналы** - Нет обработки сигналов POSIX
- **Процессы** - Нет `fork`, `exec` или управления процессами
- **Потоки** - `spawn`/`join`/каналы требуют потоковой WASM-сборки с `SharedArrayBuffer`

Все основные возможности языка работают: переменные, функции, замыкания, объекты, массивы, сопоставление с образцом, аннотации типов, try/catch и полная стандартная библиотека чистых Hemlock-модулей.

### Компиляция программ Hemlock в WASM

Помимо запуска интерпретатора в WASM, вы можете компилировать отдельные программы Hemlock в автономные WASM-бинарные файлы, используя бэкенд компилятора:

```bash
# Compile a Hemlock program to WASM (requires both hemlockc and Emscripten)
make wasm-compile FILE=program.hml

# With threading support
make wasm-compile-threaded FILE=program.hml
```

Это использует `hemlockc` для генерации C-кода, затем Emscripten для компиляции его в WASM.

## Параметры сборки

### Отладочная сборка

Сборка с отладочными символами и без оптимизации:

```bash
make debug
```

### Чистая сборка

Удаление всех скомпилированных файлов:

```bash
make clean
```

Пересборка с нуля:

```bash
make clean && make
```

## Устранение неполадок

### macOS: Ошибки "Library Not Found"

Если вы получаете ошибки об отсутствующих библиотеках (`-lcrypto`, `-lffi` и т.д.):

1. Убедитесь, что зависимости Homebrew установлены:
   ```bash
   brew install libffi openssl@3 libwebsockets
   ```

2. Проверьте пути Homebrew:
   ```bash
   brew --prefix libffi
   brew --prefix openssl
   ```

3. Makefile должен автоматически определить эти пути. Если этого не происходит, убедитесь, что `brew` находится в вашем PATH:
   ```bash
   which brew
   ```

### macOS: Ошибки типов BSD (`u_int`, `u_char` не найдены)

Если вы видите ошибки о неизвестных именах типов, таких как `u_int` или `u_char`:

1. Это исправлено в версии v1.0.0+ использованием `_DARWIN_C_SOURCE` вместо `_POSIX_C_SOURCE`
2. Убедитесь, что у вас последняя версия кода
3. Очистите и пересоберите:
   ```bash
   make clean && make
   ```

### Linux: libffi не найдена

Если вы получаете ошибки об отсутствующем `ffi.h` или `-lffi`:

1. Убедитесь, что `libffi-dev` установлен (см. зависимости выше)
2. Проверьте, может ли `pkg-config` найти её:
   ```bash
   pkg-config --cflags --libs libffi
   ```
3. Если не найдена, возможно, нужно установить `PKG_CONFIG_PATH`:
   ```bash
   export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
   ```

### Ошибки компиляции

Если вы столкнулись с ошибками компиляции:

1. Убедитесь, что у вас компилятор, совместимый с C11
2. На macOS попробуйте использовать Clang (по умолчанию):
   ```bash
   make CC=clang
   ```
3. На Linux попробуйте использовать GCC:
   ```bash
   make CC=gcc
   ```
4. Проверьте, что все зависимости установлены
5. Попробуйте пересобрать с нуля:
   ```bash
   make clean && make
   ```

### Ошибки тестов

Если тесты не проходят:

1. Убедитесь, что у вас последняя версия кода
2. Попробуйте пересобрать с нуля:
   ```bash
   make clean && make test
   ```
3. На macOS убедитесь, что у вас последняя версия Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
4. Сообщите о проблеме на GitHub с указанием:
   - Вашей платформы (версия macOS / дистрибутив Linux)
   - Архитектуры (x86_64 / arm64)
   - Вывода тестов
   - Вывода `make -v` и `gcc --version` (или `clang --version`)

## Следующие шаги

- [Быстрый старт](quick-start.md) - Напишите свою первую программу на Hemlock
- [Учебник](tutorial.md) - Изучайте Hemlock шаг за шагом
- [Руководство по языку](../language-guide/syntax.md) - Исследуйте возможности Hemlock
