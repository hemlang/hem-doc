# hem-doc

Documentation site for the [Hemlock](https://github.com/hemlang/hemlock) programming language and [hpm](https://github.com/hemlang/hpm) package manager.

## How It Works

This repo builds a single-file HTML documentation viewer from the markdown files in the hemlock and hpm submodules. The generated `docs.html` is deployed to GitHub Pages automatically.

It also includes a standalone documentation server built with [Sprout](https://github.com/hemlang/sprout), allowing you to serve the docs locally or deploy them anywhere.

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
   # Build English only (default)
   python3 build_docs.py

   # Build a specific language
   python3 build_docs.py --lang zh    # Chinese
   python3 build_docs.py --lang ru    # Russian

   # Build all 9 languages
   python3 build_docs.py --lang all
   ```

   Supported languages: `en`, `zh`, `de`, `es`, `fr`, `it`, `ja`, `pt`, `ru`

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

## Updating Submodules

This repository uses Git submodules for the hemlock and hpm documentation sources. Here's how to manage them:

### Update All Submodules

To pull the latest changes from both hemlock and hpm repos:

```bash
# Update all submodules to their latest commits
git submodule update --remote --merge

# Rebuild the documentation
make docs

# Commit the updated submodule references (if changed)
git add hemlock hpm
git commit -m "Update submodules to latest"
```

### Update a Specific Submodule

To update just one submodule:

```bash
# Update only hemlock
git submodule update --remote --merge hemlock

# Update only hpm
git submodule update --remote --merge hpm
```

### Initialize Submodules (First Time Clone)

If you cloned without `--recursive`, initialize the submodules:

```bash
git submodule update --init --recursive
```

### Check Submodule Status

To see which commits the submodules are pointing to:

```bash
git submodule status
```

## Project Structure

```
hem-doc/
├── Makefile               # Build automation
├── build_docs.py          # Documentation generator script (Python)
├── build_docs.hml         # Documentation generator script (Hemlock)
├── serve.hml              # Documentation server (Hemlock/Sprout)
├── hemlock/               # Git submodule (hemlock source)
│   ├── CLAUDE.md          # Main language reference
│   ├── docs/              # Additional documentation
│   └── logo.png           # Logo embedded in docs
├── hpm/                   # Git submodule (hpm source)
│   └── docs/              # hpm documentation
├── docs.html              # Generated output (English)
├── docs-*.html            # Generated output (other languages)
├── llms.txt               # LLM-friendly plain text (English)
├── llms-*.txt             # LLM-friendly plain text (other languages)
├── check_translations.py  # Flags translations whose source changed since last update
├── translations/
│   └── manifest.json      # Source-file hashes recorded at each translation's last update
└── .github/workflows/
    ├── build-docs.yml         # Builds all languages and deploys to GitHub Pages
    ├── sync-submodule.yml     # Daily sync of submodules (validates the build before pushing)
    └── check-translations.yml # Flags stale translations via a tracking issue
```

## Make Targets

| Target | Description |
|--------|-------------|
| `make deps` | Install dependencies via hpm |
| `make docs` | Generate docs.html (English) from hemlock source |
| `make docs-all` | Generate docs for all 9 languages |
| `make server` | Package the documentation server executable |
| `make dist` | Create distribution zip (server + docs.html) |
| `make run` | Run the documentation server locally |
| `make clean` | Remove build artifacts |
| `make help` | Show help message |

## CI/CD

- **build-docs.yml**: Builds documentation for all 9 languages and deploys them to GitHub Pages on push to main
- **sync-submodule.yml**: Automatically updates the hemlock and hpm submodules daily and on-demand. Runs a full build against the updated submodules before pushing, so a breaking upstream change never lands on `main`
- **check-translations.yml**: After a submodule sync (or weekly, as a backstop), checks whether any translation's English source changed since it was last updated and files/updates a tracking issue listing exactly which files need attention

## Translation Freshness

Translations under `translations/<lang>/` are tracked against the English source they were translated from via `translations/manifest.json`, which records a hash of each source file at the time of translation.

```bash
# Report which translations are stale, unstamped, or orphaned
python3 check_translations.py

# After finishing a translation update, stamp the new baseline
python3 check_translations.py --update-manifest
```

If you update a source file in `hemlock/` or `hpm/` without touching its translations, `check_translations.py` (run automatically in CI) will flag every language whose translation is now behind.
