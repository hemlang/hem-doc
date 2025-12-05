# hem-doc

Documentation site for the [Hemlock](https://github.com/hemlang/hemlock) programming language.

## How It Works

This repo builds a single-file HTML documentation viewer from the markdown files in the hemlock submodule. The generated `docs.html` is deployed to GitHub Pages automatically.

## Local Development

### Prerequisites

- Python 3.6+
- Git

### Setup

1. Clone the repository with submodules:
   ```bash
   git clone --recursive https://github.com/nbeerbower/hem-doc.git
   cd hem-doc
   ```

   Or if you already cloned without `--recursive`:
   ```bash
   git submodule update --init --recursive
   ```

2. Build the documentation:
   ```bash
   python build_docs.py
   ```

3. Open `docs.html` in your browser.

### Updating Documentation

To pull the latest changes from the hemlock repo:

```bash
git submodule update --remote --merge
python build_docs.py
```

## Project Structure

```
hem-doc/
├── build_docs.py          # Documentation generator script
├── hemlock/               # Git submodule (hemlock source)
│   ├── CLAUDE.md          # Main language reference
│   ├── docs/              # Additional documentation
│   └── logo.png           # Logo embedded in docs
├── docs.html              # Generated output (gitignored)
└── .github/workflows/
    ├── build-docs.yml     # Builds and deploys to GitHub Pages
    └── sync-submodule.yml # Daily sync of hemlock submodule
```

## CI/CD

- **build-docs.yml**: Builds and deploys documentation to GitHub Pages on push to main
- **sync-submodule.yml**: Automatically updates the hemlock submodule daily and on-demand
