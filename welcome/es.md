# Bienvenido a Hemlock

> "Un lenguaje pequeño e inseguro para escribir cosas inseguras de manera segura."

**Hemlock** es un lenguaje de scripting de sistemas que combina el poder de C con la ergonomía de los scripts modernos. Cuenta con gestión manual de memoria, control explícito y concurrencia asíncrona estructurada incorporada.

## ¿Qué es Hemlock?

Hemlock está diseñado para programadores que desean:

- **Control explícito** sobre la memoria y la ejecución
- **Sintaxis similar a C** con comodidades modernas
- **Sin comportamiento oculto** ni magia
- **Asincronía paralela real** con concurrencia basada en pthread

Hemlock NO es un lenguaje con seguridad de memoria y recolección de basura. En cambio, te proporciona las herramientas para estar seguro (`buffer`, anotaciones de tipos, verificación de límites) sin obligarte a usarlas (`ptr`, memoria manual, operaciones inseguras).

## Ejemplo Rápido

```hemlock
// ¡Hola, Hemlock!
fn greet(name: string): string {
    return `¡Hola, ${name}!`;
}

let message = greet("Mundo");
print(message);

// Gestión manual de memoria
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Características de un Vistazo

| Característica | Descripción |
|----------------|-------------|
| **Sistema de Tipos** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Memoria** | Gestión manual con `alloc()`, `buffer()`, `free()` |
| **Async** | `async`/`await` incorporado con verdadero paralelismo pthread |
| **FFI** | Llamar funciones C directamente desde bibliotecas compartidas |
| **Biblioteca Estándar** | 40 módulos incluyendo crypto, http, sqlite, json y más |

## Primeros Pasos

¿Listo para comenzar? Así es como empezar:

1. **[Instalación](#getting-started-installation)** - Descargar y configurar Hemlock
2. **[Inicio Rápido](#getting-started-quick-start)** - Escribe tu primer programa en minutos
3. **[Tutorial](#getting-started-tutorial)** - Aprende Hemlock paso a paso

## Secciones de Documentación

- **Primeros Pasos** - Instalación, guía de inicio rápido y tutoriales
- **Guía del Lenguaje** - Profundización en sintaxis, tipos, funciones y más
- **Temas Avanzados** - Programación asíncrona, FFI, señales y atómicos
- **Referencia de API** - Referencia completa para funciones integradas y biblioteca estándar
- **Diseño y Filosofía** - Comprender por qué Hemlock es como es

## Gestor de Paquetes

Hemlock viene con **hpm**, un gestor de paquetes para administrar dependencias:

```bash
hpm init my-project
hpm add some-package
hpm run
```

Consulta las secciones de documentación de hpm para más detalles.

---

Usa la navegación a la izquierda para explorar la documentación, o utiliza la barra de búsqueda para encontrar temas específicos.
