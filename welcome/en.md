# Welcome to Hemlock

> "A small, unsafe language for writing unsafe things safely."

**Hemlock** is a systems scripting language that combines the power of C with modern scripting ergonomics. It features manual memory management, explicit control, and structured async concurrency built-in.

## What is Hemlock?

Hemlock is designed for programmers who want:

- **Explicit control** over memory and execution
- **C-like syntax** with modern conveniences
- **No hidden behavior** or magic
- **True parallel async** with pthread-based concurrency

Hemlock is NOT a memory-safe language with garbage collection. Instead, it gives you the tools to be safe (`buffer`, type annotations, bounds checking) while not forcing you to use them (`ptr`, manual memory, unsafe operations).

## Quick Example

```hemlock
// Hello, Hemlock!
fn greet(name: string): string {
    return `Hello, ${name}!`;
}

let message = greet("World");
print(message);

// Manual memory management
let buf = buffer(64);
buf[0] = 72;  // 'H'
buf[1] = 105; // 'i'
print(buf);
free(buf);
```

## Features at a Glance

| Feature | Description |
|---------|-------------|
| **Type System** | i8-i64, u8-u64, f32/f64, bool, string, rune, ptr, buffer, array, object |
| **Memory** | Manual management with `alloc()`, `buffer()`, `free()` |
| **Async** | Built-in `async`/`await` with true pthread parallelism |
| **FFI** | Call C functions directly from shared libraries |
| **Standard Library** | 40 modules including crypto, http, sqlite, json, and more |

## Getting Started

Ready to dive in? Here's how to begin:

1. **[Installation](#getting-started-installation)** - Download and set up Hemlock
2. **[Quick Start](#getting-started-quick-start)** - Write your first program in minutes
3. **[Tutorial](#getting-started-tutorial)** - Learn Hemlock step by step

## Documentation Sections

- **Getting Started** - Installation, quick start guide, and tutorials
- **Language Guide** - Deep dive into syntax, types, functions, and more
- **Advanced Topics** - Async programming, FFI, signals, and atomics
- **API Reference** - Complete reference for built-ins and standard library
- **Design & Philosophy** - Understanding why Hemlock is the way it is

## Package Manager

Hemlock comes with **hpm**, a package manager for managing dependencies:

```bash
hpm init my-project
hpm add some-package
hpm run
```

See the hpm documentation sections for more details.

---

Use the navigation on the left to explore the documentation, or use the search bar to find specific topics.
