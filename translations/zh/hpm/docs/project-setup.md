# Project Setup

Complete guide for setting up Hemlock projects with hpm.

## Starting a New Project

### Basic Setup

Create a new project from scratch:

```bash
# Create project directory
mkdir my-project
cd my-project

# Initialize package.json
hpm init

# Create directory structure
mkdir -p src test
```

### Project Templates

Here are common project structures for different use cases:

#### Library Package

For reusable libraries:

```
my-library/
├── package.json
├── README.md
├── LICENSE
├── src/
│   ├── index.hml          # Main entry, exports public API
│   ├── core.hml           # Core functionality
│   ├── utils.hml          # Utility functions
│   └── types.hml          # Type definitions
└── test/
    ├── framework.hml      # Test framework
    ├── run.hml            # Test runner
    └── test_core.hml      # Tests
```

**package.json:**

```json
{
  "name": "yourusername/my-library",
  "version": "1.0.0",
  "description": "A reusable Hemlock library",
  "main": "src/index.hml",
  "scripts": {
    "test": "hemlock test/run.hml"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

#### Application

For standalone applications:

```
my-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Application entry point
│   ├── config.hml         # Configuration
│   ├── commands/          # CLI commands
│   │   ├── index.hml
│   │   └── run.hml
│   └── lib/               # Internal libraries
│       └── utils.hml
├── test/
│   └── run.hml
└── data/                  # Data files
```

**package.json:**

```json
{
  "name": "yourusername/my-app",
  "version": "1.0.0",
  "description": "A Hemlock application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {}
}
```

#### Web Application

For web servers:

```
my-web-app/
├── package.json
├── README.md
├── src/
│   ├── main.hml           # Server entry point
│   ├── routes/            # Route handlers
│   │   ├── index.hml
│   │   ├── api.hml
│   │   └── auth.hml
│   ├── middleware/        # Middleware
│   │   ├── index.hml
│   │   └── auth.hml
│   ├── models/            # Data models
│   │   └── user.hml
│   └── services/          # Business logic
│       └── user.hml
├── test/
│   └── run.hml
├── static/                # Static files
│   ├── css/
│   └── js/
└── views/                 # Templates
    └── index.hml
```

**package.json:**

```json
{
  "name": "yourusername/my-web-app",
  "version": "1.0.0",
  "description": "A Hemlock web application",
  "main": "src/main.hml",
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml"
  },
  "dependencies": {
    "hemlang/sprout": "^2.0.0",
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  }
}
```

## The package.json File

### Required Fields

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

### All Fields

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "Package description",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "homepage": "https://yourusername.github.io/my-package",
  "bugs": "https://github.com/yourusername/my-package/issues",
  "main": "src/index.hml",
  "keywords": ["utility", "parser"],
  "dependencies": {
    "owner/package": "^1.0.0"
  },
  "devDependencies": {
    "owner/test-lib": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc"
  },
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ],
  "native": {
    "requires": ["libcurl", "openssl"]
  }
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Package name in owner/repo format (required) |
| `version` | string | Semantic version (required) |
| `description` | string | Short description |
| `author` | string | Author name and email |
| `license` | string | License identifier (MIT, Apache-2.0, etc.) |
| `repository` | string | Repository URL |
| `homepage` | string | Project homepage |
| `bugs` | string | Issue tracker URL |
| `main` | string | Entry point file (default: src/index.hml) |
| `keywords` | array | Search keywords |
| `dependencies` | object | Runtime dependencies |
| `devDependencies` | object | Development dependencies |
| `scripts` | object | Named scripts |
| `files` | array | Files to include when publishing |
| `native` | object | Native library requirements |

## The package-lock.json File

The lock file is automatically generated and should be committed to version control. It ensures reproducible installs.

```json
{
  "lockVersion": 1,
  "hemlock": "1.0.0",
  "dependencies": {
    "hemlang/sprout": {
      "version": "2.1.0",
      "resolved": "https://github.com/hemlang/sprout/archive/v2.1.0.tar.gz",
      "integrity": "sha256-abc123...",
      "dependencies": {
        "hemlang/router": "^1.5.0"
      }
    },
    "hemlang/router": {
      "version": "1.5.0",
      "resolved": "https://github.com/hemlang/router/archive/v1.5.0.tar.gz",
      "integrity": "sha256-def456...",
      "dependencies": {}
    }
  }
}
```

### Lock File Best Practices

- **Commit** package-lock.json to version control
- **Don't edit** manually - it's auto-generated
- **Run `hpm install`** after pulling changes
- **Delete and regenerate** if corrupted:
  ```bash
  rm package-lock.json
  hpm install
  ```

## The hem_modules Directory

Installed packages are stored in `hem_modules/`:

```
hem_modules/
├── hemlang/
│   ├── sprout/
│   │   ├── package.json
│   │   └── src/
│   └── router/
│       ├── package.json
│       └── src/
└── alice/
    └── http-client/
        ├── package.json
        └── src/
```

### hem_modules Best Practices

- **Add to .gitignore** - don't commit dependencies
- **Don't modify** - changes will be overwritten
- **Delete to reinstall fresh**:
  ```bash
  rm -rf hem_modules
  hpm install
  ```

## .gitignore

Recommended .gitignore for Hemlock projects:

```gitignore
# Dependencies
hem_modules/

# Build output
dist/
*.hmlc

# IDE files
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local

# Test coverage
coverage/
```

## Working with Dependencies

### Adding Dependencies

```bash
# Add runtime dependency
hpm install hemlang/json

# Add with version constraint
hpm install hemlang/sprout@^2.0.0

# Add dev dependency
hpm install hemlang/test-utils --dev
```

### Importing Dependencies

```hemlock
// Import from package (uses "main" entry)
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { Router } from "hemlang/sprout/router";

// Import standard library
import { HashMap } from "@stdlib/collections";
import { readFile, writeFile } from "@stdlib/fs";
```

### Import Resolution

hpm resolves imports in this order:

1. **Standard library**: `@stdlib/*` imports built-in modules
2. **Package root**: `owner/repo` uses the `main` field
3. **Subpath**: `owner/repo/path` checks:
   - `hem_modules/owner/repo/path.hml`
   - `hem_modules/owner/repo/path/index.hml`
   - `hem_modules/owner/repo/src/path.hml`
   - `hem_modules/owner/repo/src/path/index.hml`

## Scripts

### Defining Scripts

Add scripts to package.json:

```json
{
  "scripts": {
    "start": "hemlock src/main.hml",
    "dev": "hemlock --watch src/main.hml",
    "test": "hemlock test/run.hml",
    "test:unit": "hemlock test/unit/run.hml",
    "test:integration": "hemlock test/integration/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/app.hmlc",
    "clean": "rm -rf dist hem_modules",
    "lint": "hemlock-lint src/",
    "format": "hemlock-fmt src/"
  }
}
```

### Running Scripts

```bash
hpm run start
hpm run dev
hpm run build

# Shorthand for test
hpm test

# Pass arguments
hpm run test -- --verbose --filter=unit
```

### Script Naming Conventions

| Script | Purpose |
|--------|---------|
| `start` | Run the application |
| `dev` | Run in development mode |
| `test` | Run all tests |
| `build` | Build for production |
| `clean` | Remove generated files |
| `lint` | Check code style |
| `format` | Format code |

## Development Workflow

### Initial Setup

```bash
# Clone project
git clone https://github.com/yourusername/my-project.git
cd my-project

# Install dependencies
hpm install

# Run tests
hpm test

# Start development
hpm run dev
```

### Daily Workflow

```bash
# Pull latest changes
git pull

# Install any new dependencies
hpm install

# Make changes...

# Run tests
hpm test

# Commit
git add .
git commit -m "Add feature"
git push
```

### Adding a New Feature

```bash
# Create feature branch
git checkout -b feature/new-feature

# Add new dependency if needed
hpm install hemlang/new-lib

# Implement feature...

# Test
hpm test

# Commit and push
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

## Environment-Specific Configuration

### Using Environment Variables

```hemlock
import { getenv } from "@stdlib/env";

let db_host = getenv("DATABASE_HOST") ?? "localhost";
let api_key = getenv("API_KEY") ?? "";

if api_key == "" {
    print("Warning: API_KEY not set");
}
```

### Configuration File

**config.hml:**

```hemlock
import { getenv } from "@stdlib/env";

export let config = {
    environment: getenv("HEMLOCK_ENV") ?? "development",
    database: {
        host: getenv("DB_HOST") ?? "localhost",
        port: int(getenv("DB_PORT") ?? "5432"),
        name: getenv("DB_NAME") ?? "myapp"
    },
    server: {
        port: int(getenv("PORT") ?? "3000"),
        host: getenv("HOST") ?? "0.0.0.0"
    }
};

export fn is_production(): bool {
    return config.environment == "production";
}
```

## See Also

- [Quick Start](quick-start.md) - Get started quickly
- [Commands](commands.md) - Command reference
- [Creating Packages](creating-packages.md) - Publishing packages
- [Configuration](configuration.md) - hpm configuration
