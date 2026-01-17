# Translations

This directory contains translations of the Hemlock documentation.

## Directory Structure

```
translations/
├── zh/                     # Chinese (Simplified)
│   ├── hemlock/           # Hemlock language docs
│   │   ├── CLAUDE.md
│   │   └── docs/
│   │       ├── getting-started/
│   │       ├── language-guide/
│   │       ├── advanced/
│   │       ├── reference/
│   │       ├── design/
│   │       └── contributing/
│   └── hpm/               # HPM package manager docs
│       └── docs/
└── README.md              # This file
```

## Adding a New Language

1. Create a new directory with the language code (e.g., `ja` for Japanese)
2. Mirror the structure of the `hemlock/` and `hpm/` submodules
3. Add the language to `SUPPORTED_LANGUAGES` in `build_docs.py`
4. Run `python build_docs.py --lang <code>` to build

## Translation Guidelines

- Keep code examples unchanged (they should remain in English/ASCII)
- Translate comments within code examples
- Keep technical terms consistent throughout the translation
- When in doubt, keep the English term with a translation in parentheses
- Preserve all markdown formatting and links

## Building Translated Documentation

```bash
# Build Chinese documentation
python build_docs.py --lang zh

# Build all languages
python build_docs.py --lang all
```

## Translation Status

| Language | Code | Status |
|----------|------|--------|
| English | en | Complete (source) |
| Chinese | zh | In progress |
