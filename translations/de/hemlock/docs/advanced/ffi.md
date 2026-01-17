# Foreign Function Interface (FFI) in Hemlock

Hemlock bietet **FFI (Foreign Function Interface)**, um C-Funktionen aus Shared Libraries unter Verwendung von libffi aufzurufen, was die Integration mit bestehenden C-Bibliotheken und System-APIs ermöglicht.

## Inhaltsverzeichnis

- [Überblick](#überblick)
- [Aktueller Status](#aktueller-status)
- [Unterstützte Typen](#unterstützte-typen)
- [Grundkonzepte](#grundkonzepte)
- [FFI-Funktionen exportieren](#ffi-funktionen-exportieren)
- [Anwendungsfälle](#anwendungsfälle)
- [Zukünftige Entwicklung](#zukünftige-entwicklung)
- [FFI-Callbacks](#ffi-callbacks)
- [FFI-Structs](#ffi-structs)
- [Struct-Typen exportieren](#struct-typen-exportieren)
- [Aktuelle Einschränkungen](#aktuelle-einschränkungen)
- [Best Practices](#best-practices)

## Überblick

Das Foreign Function Interface (FFI) ermöglicht Hemlock-Programmen:
- C-Funktionen aus Shared Libraries (.so, .dylib, .dll) aufzurufen
- Bestehende C-Bibliotheken ohne Wrapper-Code zu verwenden
- Direkt auf System-APIs zuzugreifen
- Mit nativen Bibliotheken von Drittanbietern zu integrieren
- Hemlock mit Low-Level-Systemfunktionalität zu verbinden

**Hauptfähigkeiten:**
- Dynamisches Laden von Bibliotheken
- C-Funktionsbindung
- Automatische Typkonvertierung zwischen Hemlock- und C-Typen
- Unterstützung für alle primitiven Typen
- libffi-basierte Implementierung für Portabilität

## Aktueller Status

FFI-Unterstützung ist in Hemlock mit folgenden Funktionen verfügbar:

**Implementiert:**
- ✅ C-Funktionen aus Shared Libraries aufrufen
- ✅ Unterstützung für alle primitiven Typen (Integer, Floats, Pointer)
- ✅ Automatische Typkonvertierung
- ✅ libffi-basierte Implementierung
- ✅ Dynamisches Laden von Bibliotheken
- ✅ **Funktionspointer-Callbacks** - Hemlock-Funktionen an C übergeben
- ✅ **Extern-Funktionen exportieren** - FFI-Bindungen über Module teilen
- ✅ **Struct-Übergabe und Rückgabewerte** - C-kompatible Structs by Value übergeben
- ✅ **Vollständige Pointer-Hilfsfunktionen** - Alle Typen lesen/schreiben (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Buffer/Pointer-Konvertierung** - `buffer_ptr()`, `ptr_to_buffer()`
- ✅ **FFI-Typgrößen** - `ffi_sizeof()` für plattformbewusste Typgrößen
- ✅ **Plattformtypen** - `size_t`, `usize`, `isize`, `intptr_t`-Unterstützung

**In Entwicklung:**
- 🔄 String-Marshaling-Hilfsfunktionen
- 🔄 Fehlerbehandlungsverbesserungen

**Testabdeckung:**
- FFI-Tests bestanden einschließlich Callback-Tests
- Grundlegende Funktionsaufrufe verifiziert
- Typkonvertierung getestet
- qsort-Callback-Integration getestet

## Unterstützte Typen

### Primitive Typen

Die folgenden Hemlock-Typen können an C-Funktionen übergeben/von ihnen empfangen werden:

| Hemlock-Typ | C-Typ | Größe | Hinweise |
|-------------|-------|-------|----------|
| `i8` | `int8_t` | 1 Byte | Vorzeichenbehafteter 8-Bit-Integer |
| `i16` | `int16_t` | 2 Bytes | Vorzeichenbehafteter 16-Bit-Integer |
| `i32` | `int32_t` | 4 Bytes | Vorzeichenbehafteter 32-Bit-Integer |
| `i64` | `int64_t` | 8 Bytes | Vorzeichenbehafteter 64-Bit-Integer |
| `u8` | `uint8_t` | 1 Byte | Vorzeichenloser 8-Bit-Integer |
| `u16` | `uint16_t` | 2 Bytes | Vorzeichenloser 16-Bit-Integer |
| `u32` | `uint32_t` | 4 Bytes | Vorzeichenloser 32-Bit-Integer |
| `u64` | `uint64_t` | 8 Bytes | Vorzeichenloser 64-Bit-Integer |
| `f32` | `float` | 4 Bytes | 32-Bit-Fließkommazahl |
| `f64` | `double` | 8 Bytes | 64-Bit-Fließkommazahl |
| `ptr` | `void*` | 8 Bytes | Rohpointer |

### Typkonvertierung

**Automatische Konvertierungen:**
- Hemlock-Integer → C-Integer (mit Bereichsprüfung)
- Hemlock-Floats → C-Floats
- Hemlock-Pointer → C-Pointer
- C-Rückgabewerte → Hemlock-Werte

**Beispiel-Typzuordnungen:**
```hemlock
// Hemlock → C
let i: i32 = 42;         // → int32_t (4 Bytes)
let f: f64 = 3.14;       // → double (8 Bytes)
let p: ptr = alloc(64);  // → void* (8 Bytes)

// C → Hemlock (Rückgabewerte)
// int32_t foo() → i32
// double bar() → f64
// void* baz() → ptr
```

## Grundkonzepte

### Shared Libraries

FFI arbeitet mit kompilierten Shared Libraries:

**Linux:** `.so`-Dateien
```
libexample.so
/usr/lib/libm.so
```

**macOS:** `.dylib`-Dateien
```
libexample.dylib
/usr/lib/libSystem.dylib
```

**Windows:** `.dll`-Dateien
```
example.dll
kernel32.dll
```

### Funktionssignaturen

C-Funktionen müssen bekannte Signaturen haben, damit FFI korrekt funktioniert:

```c
// Beispiel-C-Funktionssignaturen
int add(int a, int b);
double sqrt(double x);
void* malloc(size_t size);
void free(void* ptr);
```

Diese können von Hemlock aufgerufen werden, sobald die Bibliothek geladen und Funktionen gebunden sind.

### Plattformkompatibilität

FFI verwendet **libffi** für Portabilität:
- Funktioniert auf x86, x86-64, ARM, ARM64
- Behandelt Aufrufkonventionen automatisch
- Abstrahiert plattformspezifische ABI-Details
- Unterstützt Linux, macOS, Windows (mit entsprechendem libffi)

## FFI-Funktionen exportieren

FFI-Funktionen, die mit `extern fn` deklariert sind, können aus Modulen exportiert werden, sodass Sie wiederverwendbare Bibliotheks-Wrapper erstellen können, die über mehrere Dateien geteilt werden.

### Grundlegende Export-Syntax

```hemlock
// string_utils.hml - Ein Bibliotheksmodul, das C-String-Funktionen umhüllt
import "libc.so.6";

// Die extern-Funktion direkt exportieren
export extern fn strlen(s: string): i32;
export extern fn strcmp(s1: string, s2: string): i32;

// Sie können auch Wrapper-Funktionen neben extern-Funktionen exportieren
export fn string_length(s: string): i32 {
    return strlen(s);
}

export fn strings_equal(a: string, b: string): bool {
    return strcmp(a, b) == 0;
}
```

### Exportierte FFI-Funktionen importieren

```hemlock
// main.hml - Die exportierten FFI-Funktionen verwenden
import { strlen, string_length, strings_equal } from "./string_utils.hml";

let msg = "Hallo, Welt!";
print(strlen(msg));           // 12 - direkter extern-Aufruf
print(string_length(msg));    // 12 - Wrapper-Funktion

print(strings_equal("foo", "foo"));  // true
print(strings_equal("foo", "bar"));  // false
```

### Anwendungsfälle für Export Extern

**1. Plattformabstraktion**
```hemlock
// platform.hml - Plattformunterschiede abstrahieren
import "libc.so.6";  // Linux

export extern fn getpid(): i32;
export extern fn getuid(): i32;
export extern fn geteuid(): i32;
```

**2. Bibliotheks-Wrapper**
```hemlock
// crypto_lib.hml - Kryptobibliotheks-Funktionen umhüllen
import "libcrypto.so";

export extern fn SHA256(data: ptr, len: u64, out: ptr): ptr;
export extern fn MD5(data: ptr, len: u64, out: ptr): ptr;

// Hemlock-freundliche Wrapper hinzufügen
export fn sha256_string(s: string): string {
    // Implementierung mit der extern-Funktion
}
```

**3. Zentrale FFI-Deklarationen**
```hemlock
// libc.hml - Zentrales Modul für libc-Bindungen
import "libc.so.6";

// String-Funktionen
export extern fn strlen(s: string): i32;
export extern fn strcpy(dest: ptr, src: string): ptr;
export extern fn strcat(dest: ptr, src: string): ptr;

// Speicherfunktionen
export extern fn malloc(size: u64): ptr;
export extern fn realloc(p: ptr, size: u64): ptr;
export extern fn calloc(nmemb: u64, size: u64): ptr;

// Prozessfunktionen
export extern fn getpid(): i32;
export extern fn getppid(): i32;
export extern fn getenv(name: string): ptr;
```

Dann im gesamten Projekt verwenden:
```hemlock
import { strlen, malloc, getpid } from "./libc.hml";
```

### Mit regulären Exports kombinieren

Sie können exportierte extern-Funktionen mit regulären Funktionsexporten mischen:

```hemlock
// math_extended.hml
import "libm.so.6";

// Rohe C-Funktionen exportieren
export extern fn sin(x: f64): f64;
export extern fn cos(x: f64): f64;
export extern fn tan(x: f64): f64;

// Hemlock-Funktionen exportieren, die sie verwenden
export fn deg_to_rad(degrees: f64): f64 {
    return degrees * 3.14159265359 / 180.0;
}

export fn sin_degrees(degrees: f64): f64 {
    return sin(deg_to_rad(degrees));
}
```

### Plattformspezifische Bibliotheken

Beim Exportieren von extern-Funktionen beachten, dass Bibliotheksnamen je nach Plattform unterschiedlich sind:

```hemlock
// Für Linux
import "libc.so.6";

// Für macOS (anderer Ansatz erforderlich)
import "libSystem.B.dylib";
```

Derzeit verwendet Hemlocks `import "library"`-Syntax statische Bibliothekspfade, daher können plattformspezifische Module für plattformübergreifenden FFI-Code erforderlich sein.

## Anwendungsfälle

### 1. Systembibliotheken

Zugriff auf Standard-C-Bibliotheksfunktionen:

**Mathematikfunktionen:**
```hemlock
// sqrt aus libm aufrufen
let result = sqrt(16.0);  // 4.0
```

**Speicherallokation:**
```hemlock
// malloc/free aus libc aufrufen
let ptr = malloc(1024);
free(ptr);
```

### 2. Drittanbieter-Bibliotheken

Bestehende C-Bibliotheken verwenden:

**Beispiel: Bildverarbeitung**
```hemlock
// libpng oder libjpeg laden
// Bilder mit C-Bibliotheksfunktionen verarbeiten
```

**Beispiel: Kryptografie**
```hemlock
// OpenSSL oder libsodium verwenden
// Verschlüsselung/Entschlüsselung über FFI
```

### 3. System-APIs

Direkte Systemaufrufe:

**Beispiel: POSIX-APIs**
```hemlock
// getpid, getuid, etc. aufrufen
// Auf Low-Level-Systemfunktionalität zugreifen
```

### 4. Leistungskritischer Code

Optimierte C-Implementierungen aufrufen:

```hemlock
// Hochoptimierte C-Bibliotheken verwenden
// SIMD-Operationen, vektorisierter Code
// Hardware-beschleunigte Funktionen
```

### 5. Hardware-Zugriff

Schnittstelle zu Hardware-Bibliotheken:

```hemlock
// GPIO-Steuerung auf eingebetteten Systemen
// USB-Gerätekommunikation
// Serieller Port-Zugriff
```

### 6. Integration von Legacy-Code

Bestehende C-Codebasen wiederverwenden:

```hemlock
// Funktionen aus Legacy-C-Anwendungen aufrufen
// Schrittweise zu Hemlock migrieren
// Funktionierenden C-Code bewahren
```

## Zukünftige Entwicklung

### Geplante Funktionen

**1. Struct-Unterstützung**
```hemlock
// Zukunft: C-Structs übergeben/zurückgeben
define Point {
    x: f64,
    y: f64,
}

let p = Point { x: 1.0, y: 2.0 };
c_function_with_struct(p);
```

**2. Array/Buffer-Behandlung**
```hemlock
// Zukunft: Bessere Array-Übergabe
let arr = [1, 2, 3, 4, 5];
process_array(arr);  // An C-Funktion übergeben
```

**3. Funktionspointer-Callbacks** ✅ (Implementiert!)
```hemlock
// Hemlock-Funktionen als Callbacks an C übergeben
fn my_compare(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    return va - vb;
}

// C-aufrufbaren Funktionspointer erstellen
let cmp = callback(my_compare, ["ptr", "ptr"], "i32");

// Mit qsort oder jeder C-Funktion verwenden, die einen Callback erwartet
qsort(arr, count, elem_size, cmp);

// Aufräumen wenn fertig
callback_free(cmp);
```

**4. String-Marshaling**
```hemlock
// Zukunft: Automatische String-Konvertierung
let s = "hello";
c_string_function(s);  // Automatisch zu C-String konvertieren
```

**5. Fehlerbehandlung**
```hemlock
// Zukunft: Bessere Fehlerberichterstattung
try {
    let result = risky_c_function();
} catch (e) {
    print("FFI-Fehler: " + e);
}
```

**6. Typsicherheit**
```hemlock
// Zukunft: Typannotationen für FFI
@ffi("libm.so")
fn sqrt(x: f64): f64;

let result = sqrt(16.0);  // Typgeprüft
```

### Funktionen

**v1.0:**
- ✅ Grundlegendes FFI mit primitiven Typen
- ✅ Dynamisches Laden von Bibliotheken
- ✅ Funktionsaufrufe
- ✅ Callback-Unterstützung über libffi-Closures

**Zukunft:**
- Struct-Unterstützung
- Array-Behandlungsverbesserungen
- Automatische Bindungsgenerierung

## FFI-Callbacks

Hemlock unterstützt das Übergeben von Funktionen an C-Code als Callbacks unter Verwendung von libffi-Closures. Dies ermöglicht die Integration mit C-APIs, die Funktionspointer erwarten, wie `qsort`, Event-Loops und callback-basierte Bibliotheken.

### Callbacks erstellen

Verwenden Sie `callback()`, um einen C-aufrufbaren Funktionspointer aus einer Hemlock-Funktion zu erstellen:

```hemlock
// callback(function, param_types, return_type) -> ptr
let cb = callback(my_function, ["ptr", "ptr"], "i32");
```

**Parameter:**
- `function`: Eine Hemlock-Funktion zum Umhüllen
- `param_types`: Array von Typnamen-Strings (z.B. `["ptr", "i32"]`)
- `return_type`: Rückgabetyp-String (z.B. `"i32"`, `"void"`)

**Unterstützte Callback-Typen:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Vorzeichenbehaftete Integer
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Vorzeichenlose Integer
- `"f32"`, `"f64"` - Fließkommazahlen
- `"ptr"` - Pointer
- `"void"` - Kein Rückgabewert
- `"bool"` - Boolean

### Beispiel: qsort

```hemlock
import "libc.so.6";
extern fn qsort(base: ptr, nmemb: u64, size: u64, compar: ptr): void;

// Vergleichsfunktion für Integer (aufsteigend)
fn compare_ints(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    if (va < vb) { return -1; }
    if (va > vb) { return 1; }
    return 0;
}

// Array von 5 Integern allozieren
let arr = alloc(20);  // 5 * 4 Bytes
ptr_write_i32(arr, 5);
ptr_write_i32(ptr_offset(arr, 1, 4), 2);
ptr_write_i32(ptr_offset(arr, 2, 4), 8);
ptr_write_i32(ptr_offset(arr, 3, 4), 1);
ptr_write_i32(ptr_offset(arr, 4, 4), 9);

// Callback erstellen und sortieren
let cmp = callback(compare_ints, ["ptr", "ptr"], "i32");
qsort(arr, 5, 4, cmp);

// Array ist jetzt sortiert: [1, 2, 5, 8, 9]

// Aufräumen
callback_free(cmp);
free(arr);
```

### Pointer-Hilfsfunktionen

Hemlock bietet umfassende Hilfsfunktionen für die Arbeit mit Rohpointern. Diese sind essentiell für FFI-Callbacks und direkte Speichermanipulation.

#### Integer-Typ-Helfer

| Funktion | Beschreibung |
|----------|--------------|
| `ptr_deref_i8(ptr)` | Pointer dereferenzieren, i8 lesen |
| `ptr_deref_i16(ptr)` | Pointer dereferenzieren, i16 lesen |
| `ptr_deref_i32(ptr)` | Pointer dereferenzieren, i32 lesen |
| `ptr_deref_i64(ptr)` | Pointer dereferenzieren, i64 lesen |
| `ptr_deref_u8(ptr)` | Pointer dereferenzieren, u8 lesen |
| `ptr_deref_u16(ptr)` | Pointer dereferenzieren, u16 lesen |
| `ptr_deref_u32(ptr)` | Pointer dereferenzieren, u32 lesen |
| `ptr_deref_u64(ptr)` | Pointer dereferenzieren, u64 lesen |
| `ptr_write_i8(ptr, value)` | i8 an Pointer-Position schreiben |
| `ptr_write_i16(ptr, value)` | i16 an Pointer-Position schreiben |
| `ptr_write_i32(ptr, value)` | i32 an Pointer-Position schreiben |
| `ptr_write_i64(ptr, value)` | i64 an Pointer-Position schreiben |
| `ptr_write_u8(ptr, value)` | u8 an Pointer-Position schreiben |
| `ptr_write_u16(ptr, value)` | u16 an Pointer-Position schreiben |
| `ptr_write_u32(ptr, value)` | u32 an Pointer-Position schreiben |
| `ptr_write_u64(ptr, value)` | u64 an Pointer-Position schreiben |

#### Float-Typ-Helfer

| Funktion | Beschreibung |
|----------|--------------|
| `ptr_deref_f32(ptr)` | Pointer dereferenzieren, f32 (float) lesen |
| `ptr_deref_f64(ptr)` | Pointer dereferenzieren, f64 (double) lesen |
| `ptr_write_f32(ptr, value)` | f32 an Pointer-Position schreiben |
| `ptr_write_f64(ptr, value)` | f64 an Pointer-Position schreiben |

#### Pointer-Typ-Helfer

| Funktion | Beschreibung |
|----------|--------------|
| `ptr_deref_ptr(ptr)` | Pointer-zu-Pointer dereferenzieren |
| `ptr_write_ptr(ptr, value)` | Pointer an Pointer-Position schreiben |
| `ptr_offset(ptr, index, size)` | Offset berechnen: `ptr + index * size` |
| `ptr_read_i32(ptr)` | i32 durch Pointer-zu-Pointer lesen (für qsort-Callbacks) |
| `ptr_null()` | Null-Pointer-Konstante erhalten |

#### Buffer-Konvertierungs-Helfer

| Funktion | Beschreibung |
|----------|--------------|
| `buffer_ptr(buffer)` | Rohpointer aus Buffer erhalten |
| `ptr_to_buffer(ptr, size)` | Daten von Pointer in neuen Buffer kopieren |

#### FFI-Hilfsfunktionen

| Funktion | Beschreibung |
|----------|--------------|
| `ffi_sizeof(type_name)` | Größe in Bytes eines FFI-Typs erhalten |

**Unterstützte Typnamen für `ffi_sizeof`:**
- `"i8"`, `"i16"`, `"i32"`, `"i64"` - Vorzeichenbehaftete Integer (1, 2, 4, 8 Bytes)
- `"u8"`, `"u16"`, `"u32"`, `"u64"` - Vorzeichenlose Integer (1, 2, 4, 8 Bytes)
- `"f32"`, `"f64"` - Floats (4, 8 Bytes)
- `"ptr"` - Pointer (8 Bytes auf 64-Bit)
- `"size_t"`, `"usize"` - Plattformabhängiger Größentyp
- `"intptr_t"`, `"isize"` - Plattformabhängiger vorzeichenbehafteter Pointer-Typ

#### Beispiel: Mit verschiedenen Typen arbeiten

```hemlock
let p = alloc(64);

// Integer schreiben und lesen
ptr_write_i8(p, 42);
print(ptr_deref_i8(p));  // 42

ptr_write_i64(ptr_offset(p, 1, 8), 9000000000);
print(ptr_deref_i64(ptr_offset(p, 1, 8)));  // 9000000000

// Floats schreiben und lesen
ptr_write_f64(p, 3.14159);
print(ptr_deref_f64(p));  // 3.14159

// Pointer-zu-Pointer
let inner = alloc(4);
ptr_write_i32(inner, 999);
ptr_write_ptr(p, inner);
let retrieved = ptr_deref_ptr(p);
print(ptr_deref_i32(retrieved));  // 999

// Typgrößen erhalten
print(ffi_sizeof("i64"));  // 8
print(ffi_sizeof("ptr"));  // 8 (auf 64-Bit)

// Buffer-Konvertierung
let buf = buffer(64);
ptr_write_i32(buffer_ptr(buf), 12345);
print(ptr_deref_i32(buffer_ptr(buf)));  // 12345

free(inner);
free(p);
```

### Callbacks freigeben

**Wichtig:** Callbacks immer freigeben wenn fertig, um Speicherlecks zu vermeiden:

```hemlock
let cb = callback(my_fn, ["ptr"], "void");
// ... Callback verwenden ...
callback_free(cb);  // Freigeben wenn fertig
```

Callbacks werden auch automatisch freigegeben wenn das Programm beendet wird.

### Closures in Callbacks

Callbacks erfassen ihre Closure-Umgebung, sodass sie auf äußere Scope-Variablen zugreifen können:

```hemlock
let multiplier = 10;

fn scale(a: ptr, b: ptr): i32 {
    let va = ptr_deref_i32(a);
    let vb = ptr_deref_i32(b);
    // Kann auf 'multiplier' aus äußerem Scope zugreifen
    return (va * multiplier) - (vb * multiplier);
}

let cmp = callback(scale, ["ptr", "ptr"], "i32");
```

### Thread-Sicherheit

Callback-Aufrufe werden mit einem Mutex serialisiert, um Thread-Sicherheit zu gewährleisten, da der Hemlock-Interpreter nicht vollständig thread-sicher ist. Das bedeutet:
- Nur ein Callback kann gleichzeitig ausgeführt werden
- Sicher mit Multi-Thread-C-Bibliotheken verwendbar
- Kann die Leistung beeinflussen, wenn Callbacks sehr häufig von mehreren Threads aufgerufen werden

### Fehlerbehandlung in Callbacks

Ausnahmen, die in Callbacks geworfen werden, können nicht an C-Code weitergeleitet werden. Stattdessen:
- Eine Warnung wird auf stderr ausgegeben
- Der Callback gibt einen Standardwert zurück (0 oder NULL)
- Die Ausnahme wird protokolliert, aber nicht weitergeleitet

```hemlock
fn risky_callback(a: ptr): i32 {
    throw "Etwas ist schiefgelaufen";  // Warnung wird ausgegeben, gibt 0 zurück
}
```

Für robuste Fehlerbehandlung validieren Sie Eingaben und vermeiden Sie das Werfen in Callbacks.

## FFI-Structs

Hemlock unterstützt das Übergeben von Structs by Value an C-Funktionen. Struct-Typen werden automatisch für FFI registriert, wenn Sie sie mit Typannotationen definieren.

### FFI-kompatible Structs definieren

Ein Struct ist FFI-kompatibel, wenn alle Felder explizite Typannotationen mit FFI-kompatiblen Typen haben:

```hemlock
// FFI-kompatibles Struct
define Point {
    x: f64,
    y: f64,
}

// FFI-kompatibles Struct mit mehreren Feldtypen
define Rectangle {
    top_left: Point,      // Verschachteltes Struct
    width: f64,
    height: f64,
}

// NICHT FFI-kompatibel (Feld ohne Typannotation)
define DynamicObject {
    name,                 // Kein Typ - nicht in FFI verwendbar
    value,
}
```

### Structs in FFI verwenden

Extern-Funktionen deklarieren, die Struct-Typen verwenden:

```hemlock
// Den Struct-Typ definieren
define Vector2D {
    x: f64,
    y: f64,
}

// Die C-Bibliothek importieren
import "libmath.so";

// Extern-Funktion deklarieren, die Structs nimmt/zurückgibt
extern fn vector_add(a: Vector2D, b: Vector2D): Vector2D;
extern fn vector_length(v: Vector2D): f64;

// Natürlich verwenden
let a: Vector2D = { x: 3.0, y: 0.0 };
let b: Vector2D = { x: 0.0, y: 4.0 };
let result = vector_add(a, b);
print(result.x);  // 3.0
print(result.y);  // 4.0

let len = vector_length(result);
print(len);       // 5.0
```

### Unterstützte Feldtypen

Struct-Felder müssen diese FFI-kompatiblen Typen verwenden:

| Hemlock-Typ | C-Typ | Größe |
|-------------|-------|-------|
| `i8` | `int8_t` | 1 Byte |
| `i16` | `int16_t` | 2 Bytes |
| `i32` | `int32_t` | 4 Bytes |
| `i64` | `int64_t` | 8 Bytes |
| `u8` | `uint8_t` | 1 Byte |
| `u16` | `uint16_t` | 2 Bytes |
| `u32` | `uint32_t` | 4 Bytes |
| `u64` | `uint64_t` | 8 Bytes |
| `f32` | `float` | 4 Bytes |
| `f64` | `double` | 8 Bytes |
| `ptr` | `void*` | 8 Bytes |
| `string` | `char*` | 8 Bytes |
| `bool` | `int` | variiert |
| Verschachteltes Struct | struct | variiert |

### Struct-Layout

Hemlock verwendet die nativen Struct-Layout-Regeln der Plattform (passend zum C-ABI):
- Felder werden entsprechend ihrem Typ ausgerichtet
- Padding wird nach Bedarf eingefügt
- Gesamtgröße wird auf das größte Element aufgefüllt

```hemlock
// Beispiel: C-kompatibles Layout
define Mixed {
    a: i8,    // Offset 0, Größe 1
              // 3 Bytes Padding
    b: i32,   // Offset 4, Größe 4
}
// Gesamtgröße: 8 Bytes (mit Padding)

define Point3D {
    x: f64,   // Offset 0, Größe 8
    y: f64,   // Offset 8, Größe 8
    z: f64,   // Offset 16, Größe 8
}
// Gesamtgröße: 24 Bytes (kein Padding erforderlich)
```

### Verschachtelte Structs

Structs können andere Structs enthalten:

```hemlock
define Inner {
    x: i32,
    y: i32,
}

define Outer {
    inner: Inner,
    z: i32,
}

import "mylib.so";
extern fn process_nested(data: Outer): i32;

let obj: Outer = {
    inner: { x: 1, y: 2 },
    z: 3,
};
let result = process_nested(obj);
```

### Struct-Rückgabewerte

C-Funktionen können Structs zurückgeben:

```hemlock
define Point {
    x: f64,
    y: f64,
}

import "libmath.so";
extern fn get_origin(): Point;

let p = get_origin();
print(p.x);  // 0.0
print(p.y);  // 0.0
```

### Einschränkungen

- **Struct-Felder müssen Typannotationen haben** - Felder ohne Typen sind nicht FFI-kompatibel
- **Keine Arrays in Structs** - stattdessen Pointer verwenden
- **Keine Unions** - nur Struct-Typen werden unterstützt
- **Callbacks können keine Structs zurückgeben** - Pointer für Callback-Rückgabewerte verwenden

### Struct-Typen exportieren

Sie können Struct-Typdefinitionen aus einem Modul mit `export define` exportieren:

```hemlock
// geometry.hml
export define Vector2 {
    x: f32,
    y: f32,
}

export define Rectangle {
    x: f32,
    y: f32,
    width: f32,
    height: f32,
}

export fn create_rect(x: f32, y: f32, w: f32, h: f32): Rectangle {
    return { x: x, y: y, width: w, height: h };
}
```

**Wichtig:** Exportierte Struct-Typen werden **global** registriert, wenn das Modul geladen wird. Sie werden automatisch verfügbar, wenn Sie irgendetwas aus dem Modul importieren. Sie müssen (und können) sie NICHT explizit nach Namen importieren:

```hemlock
// main.hml

// GUT - Struct-Typen sind nach jedem Import aus dem Modul automatisch verfügbar
import { create_rect } from "./geometry.hml";
let v: Vector2 = { x: 1.0, y: 2.0 };      // Funktioniert - Vector2 ist global verfügbar
let r: Rectangle = create_rect(0.0, 0.0, 100.0, 50.0);  // Funktioniert

// SCHLECHT - kann Struct-Typen nicht explizit nach Namen importieren
import { Vector2 } from "./geometry.hml";  // Fehler: Undefinierte Variable 'Vector2'
```

Dieses Verhalten existiert, weil Struct-Typen in der globalen Typ-Registry registriert werden, wenn das Modul lädt, anstatt als Werte in der Export-Umgebung des Moduls gespeichert zu werden. Der Typ wird für allen Code verfügbar, der aus dem Modul importiert.

## Aktuelle Einschränkungen

FFI hat die folgenden Einschränkungen:

**1. Manuelle Typkonvertierung**
- Muss String-Konvertierungen manuell verwalten
- Keine automatische Hemlock-String ↔ C-String-Konvertierung

**2. Begrenzte Fehlerbehandlung**
- Grundlegende Fehlerberichterstattung
- Ausnahmen in Callbacks können nicht an C weitergeleitet werden

**3. Manuelles Laden von Bibliotheken**
- Muss Bibliotheken manuell laden
- Keine automatische Bindungsgenerierung

**4. Plattformspezifischer Code**
- Bibliothekspfade unterscheiden sich nach Plattform
- Muss .so vs .dylib vs .dll behandeln

## Best Practices

Während umfassende FFI-Dokumentation noch entwickelt wird, hier allgemeine Best Practices:

### 1. Typsicherheit

```hemlock
// Explizit bei Typen sein
let x: i32 = 42;
let result: f64 = c_function(x);
```

### 2. Speicherverwaltung

```hemlock
// Daran denken, allozierten Speicher freizugeben
let ptr = c_malloc(1024);
// ... ptr verwenden
c_free(ptr);
```

### 3. Fehlerprüfung

```hemlock
// Rückgabewerte prüfen
let result = c_function();
if (result == null) {
    print("C-Funktion fehlgeschlagen");
}
```

### 4. Plattformkompatibilität

```hemlock
// Plattformunterschiede behandeln
// Entsprechende Bibliothekserweiterungen verwenden (.so, .dylib, .dll)
```

## Beispiele

Für funktionierende Beispiele siehe:
- Callback-Tests: `/tests/ffi_callbacks/` - qsort-Callback-Beispiele
- Stdlib FFI-Verwendung: `/stdlib/hash.hml`, `/stdlib/regex.hml`, `/stdlib/crypto.hml`
- Beispielprogramme: `/examples/` (falls verfügbar)

## Hilfe erhalten

FFI ist ein neueres Feature in Hemlock. Bei Fragen oder Problemen:

1. Test-Suite auf funktionierende Beispiele prüfen
2. libffi-Dokumentation für Low-Level-Details heranziehen
3. Bugs melden oder Features über Projekt-Issues anfragen

## Zusammenfassung

Hemlocks FFI bietet:

- ✅ C-Funktionsaufruf aus Shared Libraries
- ✅ Primitive Typunterstützung (i8-i64, u8-u64, f32, f64, ptr)
- ✅ Automatische Typkonvertierung
- ✅ libffi-basierte Portabilität
- ✅ Grundlage für native Bibliotheksintegration
- ✅ **Funktionspointer-Callbacks** - Hemlock-Funktionen an C übergeben
- ✅ **Extern-Funktionen exportieren** - FFI-Bindungen über Module teilen
- ✅ **Struct-Übergabe und -Rückgabe** - C-kompatible Structs by Value übergeben
- ✅ **Export define** - Struct-Typdefinitionen über Module teilen (automatisch global importiert)
- ✅ **Vollständige Pointer-Helfer** - Alle Typen lesen/schreiben (i8-i64, u8-u64, f32, f64, ptr)
- ✅ **Buffer/Pointer-Konvertierung** - `buffer_ptr()`, `ptr_to_buffer()` für Daten-Marshaling
- ✅ **FFI-Typgrößen** - `ffi_sizeof()` für plattformbewusste Typgrößen
- ✅ **Plattformtypen** - `size_t`, `usize`, `isize`, `intptr_t`, `uintptr_t`-Unterstützung

**Aktueller Status:** FFI voll ausgestattet mit primitiven Typen, Structs, Callbacks, Modul-Exports und vollständigen Pointer-Hilfsfunktionen

**Zukunft:** String-Marshaling-Hilfsfunktionen

**Anwendungsfälle:** Systembibliotheken, Drittanbieter-Bibliotheken, qsort, Event-Loops, callback-basierte APIs, wiederverwendbare Bibliotheks-Wrapper

## Beitragen

FFI-Dokumentation wird erweitert. Wenn Sie mit FFI arbeiten:
- Dokumentieren Sie Ihre Anwendungsfälle
- Teilen Sie Beispielcode
- Melden Sie Probleme oder Einschränkungen
- Schlagen Sie Verbesserungen vor

Das FFI-System ist darauf ausgelegt, praktisch und sicher zu sein, während es bei Bedarf Low-Level-Zugriff bietet, gemäß Hemlocks Philosophie von "explizit statt implizit" und "unsafe ist ein Feature, kein Bug".
