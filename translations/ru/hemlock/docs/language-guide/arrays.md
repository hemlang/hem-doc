# Массивы

Hemlock предоставляет **динамические массивы** с обширным набором методов для манипуляции и обработки данных. Массивы могут содержать смешанные типы и автоматически увеличиваются по мере необходимости.

## Обзор

```hemlock
// Литералы массивов
let arr = [1, 2, 3, 4, 5];
print(arr[0]);         // 1
print(arr.length);     // 5

// Смешанные типы разрешены
let mixed = [1, "hello", true, null];

// Динамический размер
arr.push(6);           // Автоматически увеличивается
arr.push(7);
print(arr.length);     // 7
```

## Литералы массивов

### Базовый синтаксис

```hemlock
let numbers = [1, 2, 3, 4, 5];
let strings = ["apple", "banana", "cherry"];
let booleans = [true, false, true];
```

### Пустые массивы

```hemlock
let arr = [];  // Пустой массив

// Добавление элементов позже
arr.push(1);
arr.push(2);
arr.push(3);
```

### Смешанные типы

Массивы могут содержать разные типы:

```hemlock
let mixed = [
    42,
    "hello",
    true,
    null,
    [1, 2, 3],
    { x: 10, y: 20 }
];

print(mixed[0]);  // 42
print(mixed[1]);  // "hello"
print(mixed[4]);  // [1, 2, 3] (вложенный массив)
```

### Вложенные массивы

```hemlock
let matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

print(matrix[0][0]);  // 1
print(matrix[1][2]);  // 6
print(matrix[2][1]);  // 8
```

### Типизированные массивы

Массивы могут иметь аннотации типов для обеспечения типов элементов:

```hemlock
// Синтаксис типизированного массива
let nums: array<i32> = [1, 2, 3, 4, 5];
let names: array<string> = ["Alice", "Bob", "Carol"];
let flags: array<bool> = [true, false, true];

// Проверка типов во время выполнения
let valid: array<i32> = [1, 2, 3];       // OK
let invalid: array<i32> = [1, "two", 3]; // Ошибка времени выполнения: несоответствие типов

// Вложенные типизированные массивы
let matrix: array<array<i32>> = [
    [1, 2, 3],
    [4, 5, 6]
];
```

**Поведение аннотации типа:**
- Элементы проверяются при добавлении в массив
- Несоответствия типов вызывают ошибки времени выполнения
- Без аннотации типа массивы принимают смешанные типы

## Индексация

### Чтение элементов

Доступ с нуля:

```hemlock
let arr = [10, 20, 30, 40, 50];

print(arr[0]);  // 10 (первый элемент)
print(arr[4]);  // 50 (последний элемент)

// Выход за границы возвращает null (без ошибки)
print(arr[10]);  // null
```

### Запись элементов

```hemlock
let arr = [1, 2, 3];

arr[0] = 10;    // Изменение существующего
arr[1] = 20;
print(arr);     // [10, 20, 3]

// Можно присваивать за пределами текущей длины (массив увеличивается)
arr[5] = 60;    // Создает [10, 20, 3, null, null, 60]
```

### Отрицательные индексы

**Не поддерживаются** - Используйте только положительные индексы:

```hemlock
let arr = [1, 2, 3];
print(arr[-1]);  // ОШИБКА или неопределенное поведение

// Используйте length для последнего элемента
print(arr[arr.length - 1]);  // 3
```

## Свойства

### Свойство `.length`

Возвращает количество элементов:

```hemlock
let arr = [1, 2, 3, 4, 5];
print(arr.length);  // 5

// Пустой массив
let empty = [];
print(empty.length);  // 0

// После модификаций
arr.push(6);
print(arr.length);  // 6
```

## Методы массивов

Hemlock предоставляет 18 методов массивов для комплексной манипуляции.

### Операции стека

**`push(value)`** - Добавить элемент в конец:
```hemlock
let arr = [1, 2, 3];
arr.push(4);           // [1, 2, 3, 4]
arr.push(5);           // [1, 2, 3, 4, 5]

print(arr.length);     // 5
```

**`pop()`** - Удалить и вернуть последний элемент:
```hemlock
let arr = [1, 2, 3, 4, 5];
let last = arr.pop();  // Возвращает 5, arr теперь [1, 2, 3, 4]

print(last);           // 5
print(arr.length);     // 4
```

### Операции очереди

**`shift()`** - Удалить и вернуть первый элемент:
```hemlock
let arr = [1, 2, 3];
let first = arr.shift();   // Возвращает 1, arr теперь [2, 3]

print(first);              // 1
print(arr);                // [2, 3]
```

**`unshift(value)`** - Добавить элемент в начало:
```hemlock
let arr = [2, 3];
arr.unshift(1);            // [1, 2, 3]
arr.unshift(0);            // [0, 1, 2, 3]
```

### Вставка и удаление

**`insert(index, value)`** - Вставить элемент по индексу:
```hemlock
let arr = [1, 2, 4, 5];
arr.insert(2, 3);      // Вставить 3 по индексу 2: [1, 2, 3, 4, 5]

arr.insert(0, 0);      // Вставить в начало: [0, 1, 2, 3, 4, 5]
```

**`remove(index)`** - Удалить и вернуть элемент по индексу:
```hemlock
let arr = [1, 2, 3, 4, 5];
let removed = arr.remove(2);  // Возвращает 3, arr теперь [1, 2, 4, 5]

print(removed);               // 3
print(arr);                   // [1, 2, 4, 5]
```

### Операции поиска

**`find(value)`** - Найти первое вхождение:
```hemlock
let arr = [10, 20, 30, 40];
let idx = arr.find(30);      // 2 (индекс первого вхождения)
let idx2 = arr.find(99);     // -1 (не найдено)

// Работает с любым типом
let words = ["apple", "banana", "cherry"];
let idx3 = words.find("banana");  // 1
```

**`contains(value)`** - Проверить, содержит ли массив значение:
```hemlock
let arr = [10, 20, 30, 40];
let has = arr.contains(20);  // true
let has2 = arr.contains(99); // false
```

### Операции извлечения

**`slice(start, end)`** - Извлечь подмассив (end не включается):
```hemlock
let arr = [1, 2, 3, 4, 5];
let sub = arr.slice(1, 4);   // [2, 3, 4] (индексы 1, 2, 3)
let first = arr.slice(0, 2); // [1, 2]

// Оригинал не изменяется
print(arr);                  // [1, 2, 3, 4, 5]
```

**`first()`** - Получить первый элемент (без удаления):
```hemlock
let arr = [1, 2, 3];
let f = arr.first();         // 1 (без удаления)
print(arr);                  // [1, 2, 3] (без изменений)
```

**`last()`** - Получить последний элемент (без удаления):
```hemlock
let arr = [1, 2, 3];
let l = arr.last();          // 3 (без удаления)
print(arr);                  // [1, 2, 3] (без изменений)
```

### Операции преобразования

**`reverse()`** - Развернуть массив на месте:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.reverse();               // [5, 4, 3, 2, 1]

print(arr);                  // [5, 4, 3, 2, 1] (изменен)
```

**`join(delimiter)`** - Объединить элементы в строку:
```hemlock
let words = ["hello", "world", "foo"];
let joined = words.join(" ");  // "hello world foo"

let numbers = [1, 2, 3];
let csv = numbers.join(",");   // "1,2,3"

// Работает со смешанными типами
let mixed = [1, "hello", true, null];
print(mixed.join(" | "));  // "1 | hello | true | null"
```

**`concat(other)`** - Объединить с другим массивом:
```hemlock
let a = [1, 2, 3];
let b = [4, 5, 6];
let combined = a.concat(b);  // [1, 2, 3, 4, 5, 6] (новый массив)

// Оригиналы не изменяются
print(a);                    // [1, 2, 3]
print(b);                    // [4, 5, 6]
```

### Служебные операции

**`clear()`** - Удалить все элементы:
```hemlock
let arr = [1, 2, 3, 4, 5];
arr.clear();                 // []

print(arr.length);           // 0
print(arr);                  // []
```

## Цепочка методов

Методы, возвращающие массивы или значения, позволяют создавать цепочки:

```hemlock
let result = [1, 2, 3]
    .concat([4, 5, 6])
    .slice(2, 5);  // [3, 4, 5]

let text = ["apple", "banana", "cherry"]
    .slice(0, 2)
    .join(" and ");  // "apple and banana"

let numbers = [5, 3, 8, 1, 9]
    .slice(1, 4)
    .concat([10, 11]);  // [3, 8, 1, 10, 11]
```

## Полная справка по методам

| Метод | Параметры | Возвращает | Изменяет | Описание |
|-------|-----------|------------|----------|----------|
| `push(value)` | any | void | Да | Добавить элемент в конец |
| `pop()` | - | any | Да | Удалить и вернуть последний |
| `shift()` | - | any | Да | Удалить и вернуть первый |
| `unshift(value)` | any | void | Да | Добавить элемент в начало |
| `insert(index, value)` | i32, any | void | Да | Вставить по индексу |
| `remove(index)` | i32 | any | Да | Удалить и вернуть по индексу |
| `find(value)` | any | i32 | Нет | Найти первое вхождение (-1 если не найдено) |
| `contains(value)` | any | bool | Нет | Проверить наличие значения |
| `slice(start, end)` | i32, i32 | array | Нет | Извлечь подмассив (новый массив) |
| `join(delimiter)` | string | string | Нет | Объединить в строку |
| `concat(other)` | array | array | Нет | Объединить (новый массив) |
| `reverse()` | - | void | Да | Развернуть на месте |
| `first()` | - | any | Нет | Получить первый элемент |
| `last()` | - | any | Нет | Получить последний элемент |
| `clear()` | - | void | Да | Удалить все элементы |
| `map(callback)` | fn | array | Нет | Преобразовать каждый элемент |
| `filter(predicate)` | fn | array | Нет | Выбрать подходящие элементы |
| `reduce(callback, initial)` | fn, any | any | Нет | Свернуть к одному значению |

## Детали реализации

### Модель памяти

- **Размещение в куче** - Динамическая емкость
- **Автоматический рост** - Емкость удваивается при превышении
- **Нет автоматического сжатия** - Емкость не уменьшается
- **Нет проверки границ при индексации** - Используйте методы для безопасности

### Управление емкостью

```hemlock
let arr = [];  // Начальная емкость: 0

arr.push(1);   // Емкость увеличивается до 1
arr.push(2);   // Емкость увеличивается до 2
arr.push(3);   // Емкость увеличивается до 4 (удваивается)
arr.push(4);   // Все еще емкость 4
arr.push(5);   // Емкость увеличивается до 8 (удваивается)
```

### Сравнение значений

`find()` и `contains()` используют равенство значений:

```hemlock
// Примитивы: сравнение по значению
let arr = [1, 2, 3];
arr.contains(2);  // true

// Строки: сравнение по значению
let words = ["hello", "world"];
words.contains("hello");  // true

// Объекты: сравнение по ссылке
let obj1 = { x: 10 };
let obj2 = { x: 10 };
let arr2 = [obj1];
arr2.contains(obj1);  // true (та же ссылка)
arr2.contains(obj2);  // false (другая ссылка)
```

## Распространенные паттерны

### Функциональные операции (map/filter/reduce)

Массивы имеют встроенные методы `map`, `filter` и `reduce`:

```hemlock
// map - преобразовать каждый элемент
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(fn(x) { return x * 2; });
print(doubled);  // [2, 4, 6, 8, 10]

// filter - выбрать подходящие элементы
let evens = numbers.filter(fn(x) { return x % 2 == 0; });
print(evens);  // [2, 4]

// reduce - свернуть к одному значению
let sum = numbers.reduce(fn(acc, x) { return acc + x; }, 0);
print(sum);  // 15

// Цепочка функциональных операций
let result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    .filter(fn(x) { return x % 2 == 0; })  // [2, 4, 6, 8, 10]
    .map(fn(x) { return x * x; })          // [4, 16, 36, 64, 100]
    .reduce(fn(acc, x) { return acc + x; }, 0);  // 220
```

### Паттерн: Массив как стек

```hemlock
let stack = [];

// Push на стек
stack.push(1);
stack.push(2);
stack.push(3);

// Pop со стека
let top = stack.pop();    // 3
let next = stack.pop();   // 2
```

### Паттерн: Массив как очередь

```hemlock
let queue = [];

// Добавить в очередь (в конец)
queue.push(1);
queue.push(2);
queue.push(3);

// Извлечь из очереди (с начала)
let first = queue.shift();   // 1
let second = queue.shift();  // 2
```

## Лучшие практики

1. **Используйте методы вместо прямой индексации** - Проверка границ и ясность
2. **Проверяйте границы** - Прямая индексация не проверяет границы
3. **Предпочитайте неизменяющие операции** - Используйте `slice()` и `concat()` вместо мутации
4. **Инициализируйте с емкостью** - Если знаете размер (пока не поддерживается)
5. **Используйте `contains()` для проверки членства** - Яснее чем ручные циклы
6. **Создавайте цепочки методов** - Читабельнее чем вложенные вызовы

## Распространенные ловушки

### Ловушка: Прямой индекс за границами

```hemlock
let arr = [1, 2, 3];

// Нет проверки границ!
arr[10] = 99;  // Создает разреженный массив с null
print(arr.length);  // 11 (не 3!)

// Лучше: Используйте push() или проверяйте длину
if (arr.length <= 10) {
    arr.push(99);
}
```

### Ловушка: Мутация vs. Новый массив

```hemlock
let arr = [1, 2, 3];

// Изменяет оригинал
arr.reverse();
print(arr);  // [3, 2, 1]

// Возвращает новый массив
let sub = arr.slice(0, 2);
print(arr);  // [3, 2, 1] (без изменений)
print(sub);  // [3, 2]
```

### Ловушка: Равенство ссылок

```hemlock
let obj = { x: 10 };
let arr = [obj];

// Та же ссылка: true
arr.contains(obj);  // true

// Другая ссылка: false
arr.contains({ x: 10 });  // false (другой объект)
```

### Ловушка: Долгоживущие массивы

```hemlock
// Массивы в локальной области автоматически освобождаются, но глобальные/долгоживущие требуют внимания
let global_cache = [];  // На уровне модуля, живет до конца программы

fn add_to_cache(item) {
    global_cache.push(item);  // Растет бесконечно
}

// Для долгоживущих данных рассмотрите:
// - Периодическую очистку массива: global_cache.clear();
// - Раннее освобождение когда закончили: free(global_cache);
```

## Примеры

### Пример: Статистика массива

```hemlock
fn mean(arr) {
    let sum = 0;
    let i = 0;
    while (i < arr.length) {
        sum = sum + arr[i];
        i = i + 1;
    }
    return sum / arr.length;
}

fn max(arr) {
    if (arr.length == 0) {
        return null;
    }

    let max_val = arr[0];
    let i = 1;
    while (i < arr.length) {
        if (arr[i] > max_val) {
            max_val = arr[i];
        }
        i = i + 1;
    }
    return max_val;
}

let numbers = [3, 7, 2, 9, 1];
print(mean(numbers));  // 4.4
print(max(numbers));   // 9
```

### Пример: Удаление дубликатов

```hemlock
fn unique(arr) {
    let result = [];
    let i = 0;
    while (i < arr.length) {
        if (!result.contains(arr[i])) {
            result.push(arr[i]);
        }
        i = i + 1;
    }
    return result;
}

let numbers = [1, 2, 2, 3, 1, 4, 3, 5];
let uniq = unique(numbers);  // [1, 2, 3, 4, 5]
```

### Пример: Разбиение на части

```hemlock
fn chunk(arr, size) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        let chunk = arr.slice(i, i + size);
        result.push(chunk);
        i = i + size;
    }

    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8];
let chunks = chunk(numbers, 3);
// [[1, 2, 3], [4, 5, 6], [7, 8]]
```

### Пример: Выравнивание массива

```hemlock
fn flatten(arr) {
    let result = [];
    let i = 0;

    while (i < arr.length) {
        if (typeof(arr[i]) == "array") {
            // Вложенный массив - выравниваем его
            let nested = flatten(arr[i]);
            let j = 0;
            while (j < nested.length) {
                result.push(nested[j]);
                j = j + 1;
            }
        } else {
            result.push(arr[i]);
        }
        i = i + 1;
    }

    return result;
}

let nested = [1, [2, 3], [4, [5, 6]], 7];
let flat = flatten(nested);  // [1, 2, 3, 4, 5, 6, 7]
```

### Пример: Сортировка (пузырьковая)

```hemlock
fn sort(arr) {
    let n = arr.length;
    let i = 0;

    while (i < n) {
        let j = 0;
        while (j < n - i - 1) {
            if (arr[j] > arr[j + 1]) {
                // Обмен
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
}

let numbers = [5, 2, 8, 1, 9];
sort(numbers);  // Изменяет на месте
print(numbers);  // [1, 2, 5, 8, 9]
```

## Ограничения

Текущие ограничения:

- **Нет проверки границ при индексации** - Прямой доступ не проверяется
- **Равенство ссылок для объектов** - `find()` и `contains()` используют сравнение ссылок
- **Нет деструктуризации массивов** - Нет синтаксиса `let [a, b] = arr`
- **Нет оператора spread** - Нет синтаксиса `[...arr1, ...arr2]`

**Примечание:** Массивы используют подсчет ссылок и автоматически освобождаются при выходе из области видимости. См. [Управление памятью](memory.md#internal-reference-counting) для деталей.

## Связанные темы

- [Строки](strings.md) - Методы строк похожи на методы массивов
- [Объекты](objects.md) - Массивы также являются объектоподобными
- [Функции](functions.md) - Функции высшего порядка с массивами
- [Управление потоком](control-flow.md) - Итерация по массивам

## См. также

- **Динамический размер**: Массивы автоматически растут с удвоением емкости
- **Методы**: 18 комплексных методов для манипуляции включая map/filter/reduce
- **Память**: См. [Память](memory.md) для деталей размещения массивов
