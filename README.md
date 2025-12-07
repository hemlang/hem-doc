# hem-doc

Documentation site for the [Hemlock](https://github.com/nbeerbower/hemlock) programming language.

## How It Works

This repo builds a single-file HTML documentation viewer from the markdown files in the hemlock submodule. The generated `docs.html` is deployed to GitHub Pages automatically.

It also includes a standalone documentation server built with [Sprout](https://github.com/nbeerbower/sprout), allowing you to serve the docs locally or deploy them anywhere.

## Prerequisites

- [Hemlock](https://github.com/hemlang/hemlock) - The Hemlock interpreter
- [hpm](https://github.com/hemlang/hpm) - Hemlock Package Manager

## Quick Start

### Using Make

```bash
# Install dependencies and generate docs
make deps
make docs

# Build the documentation server
make server

# Run the server locally (http://localhost:3000)
make run

# Create a distribution package (zip with server + docs)
make dist
```

### Manual Setup

1. Clone the repository with submodules:
   ```bash
   git clone --recursive https://github.com/hemlang/hem-doc.git
   cd hem-doc
   ```

   Or if you already cloned without `--recursive`:
   ```bash
   git submodule update --init --recursive
   ```

2. Install dependencies:
   ```bash
   hpm install
   ```

3. Build the documentation:
   ```bash
   python3 build_docs.py
   ```

4. Open `docs.html` in your browser, or run the server:
   ```bash
   hemlock serve.hml
   ```

## Documentation Server

The documentation server is a self-contained executable built with Hemlock and Sprout:

```bash
# Build the server (requires hemlock in PATH or set HEMLOCK env var)
make server

# Run it
./hem-doc-server
# Serving docs at http://localhost:3000
```

The server provides:
- `/` - The documentation HTML
- `/health` - Health check endpoint (JSON)

## Updating Documentation

To pull the latest changes from the hemlock repo:

```bash
git submodule update --remote --merge
make docs
```

## Project Structure

```
hem-doc/
├── Makefile               # Build automation
├── build_docs.py          # Documentation generator script
├── serve.hml              # Documentation server (Hemlock/Sprout)
├── sprout.hml             # Sprout web framework
├── hemlock/               # Git submodule (hemlock source)
│   ├── CLAUDE.md          # Main language reference
│   ├── docs/              # Additional documentation
│   └── logo.png           # Logo embedded in docs
├── docs.html              # Generated output
└── .github/workflows/
    ├── build-docs.yml     # Builds and deploys to GitHub Pages
    └── sync-submodule.yml # Daily sync of hemlock submodule
```

## Make Targets

| Target | Description |
|--------|-------------|
| `make deps` | Install dependencies via hpm |
| `make docs` | Generate docs.html from hemlock source |
| `make server` | Package the documentation server executable |
| `make dist` | Create distribution zip (server + docs.html) |
| `make run` | Run the documentation server locally |
| `make clean` | Remove build artifacts |
| `make help` | Show help message |

## CI/CD

- **build-docs.yml**: Builds and deploys documentation to GitHub Pages on push to main
- **sync-submodule.yml**: Automatically updates the hemlock submodule daily and on-demand
