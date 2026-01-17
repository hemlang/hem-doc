# Package Specification

Complete reference for the `package.json` file format.

## Overview

Every hpm package requires a `package.json` file in the project root. This file defines package metadata, dependencies, and scripts.

## Minimal Example

```json
{
  "name": "owner/repo",
  "version": "1.0.0"
}
```

## Complete Example

```json
{
  "name": "hemlang/example-package",
  "version": "1.2.3",
  "description": "An example Hemlock package",
  "author": "Hemlock Team <team@hemlock.dev>",
  "license": "MIT",
  "repository": "https://github.com/hemlang/example-package",
  "homepage": "https://hemlang.github.io/example-package",
  "bugs": "https://github.com/hemlang/example-package/issues",
  "main": "src/index.hml",
  "keywords": ["example", "utility", "hemlock"],
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "^2.1.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "start": "hemlock src/main.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/main.hml -o dist/bundle.hmlc"
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

## Field Reference

### name (required)

The package name in `owner/repo` format.

```json
{
  "name": "hemlang/sprout"
}
```

**Requirements:**
- Must be in `owner/repo` format
- `owner` should be your GitHub username or organization
- `repo` should be the repository name
- Use lowercase letters, numbers, and hyphens
- Maximum 214 characters total

**Valid names:**
```
hemlang/sprout
alice/http-client
myorg/json-utils
bob123/my-lib
```

**Invalid names:**
```
my-package          # Missing owner
hemlang/My_Package  # Uppercase and underscore
hemlang             # Missing repo
```

### version (required)

The package version following [Semantic Versioning](https://semver.org/).

```json
{
  "version": "1.2.3"
}
```

**Format:** `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Valid versions:**
```
1.0.0
2.1.3
1.0.0-alpha
1.0.0-beta.1
1.0.0-rc.1+build.123
0.1.0
```

### description

Short description of the package.

```json
{
  "description": "A fast JSON parser for Hemlock"
}
```

- Keep it under 200 characters
- Describe what the package does, not how

### author

Package author information.

```json
{
  "author": "Your Name <email@example.com>"
}
```

**Formats accepted:**
```json
"author": "Your Name"
"author": "Your Name <email@example.com>"
"author": "Your Name <email@example.com> (https://website.com)"
```

### license

The license identifier.

```json
{
  "license": "MIT"
}
```

**Common licenses:**
- `MIT` - MIT License
- `Apache-2.0` - Apache License 2.0
- `GPL-3.0` - GNU General Public License v3.0
- `BSD-3-Clause` - BSD 3-Clause License
- `ISC` - ISC License
- `UNLICENSED` - Proprietary/private

Use [SPDX identifiers](https://spdx.org/licenses/) when possible.

### repository

Link to the source repository.

```json
{
  "repository": "https://github.com/hemlang/sprout"
}
```

### homepage

Project homepage URL.

```json
{
  "homepage": "https://sprout.hemlock.dev"
}
```

### bugs

Issue tracker URL.

```json
{
  "bugs": "https://github.com/hemlang/sprout/issues"
}
```

### main

Entry point file for the package.

```json
{
  "main": "src/index.hml"
}
```

**Default:** `src/index.hml`

When users import your package:
```hemlock
import { x } from "owner/repo";
```

hpm loads the file specified in `main`.

**Resolution order for imports:**
1. Exact path: `src/index.hml`
2. With .hml extension: `src/index` → `src/index.hml`
3. Index file: `src/index/` → `src/index/index.hml`

### keywords

Array of keywords for discoverability.

```json
{
  "keywords": ["json", "parser", "utility", "hemlock"]
}
```

- Use lowercase
- Be specific and relevant
- Include language ("hemlock") if appropriate

### dependencies

Runtime dependencies required for the package to work.

```json
{
  "dependencies": {
    "hemlang/json": "^1.0.0",
    "hemlang/http": "~2.1.0",
    "alice/logger": ">=1.0.0 <2.0.0"
  }
}
```

**Key:** Package name (`owner/repo`)
**Value:** Version constraint

**Version constraint syntax:**

| Constraint | Meaning |
|------------|---------|
| `1.2.3` | Exact version |
| `^1.2.3` | >=1.2.3 <2.0.0 |
| `~1.2.3` | >=1.2.3 <1.3.0 |
| `>=1.0.0` | At least 1.0.0 |
| `>=1.0.0 <2.0.0` | Range |
| `*` | Any version |

### devDependencies

Development-only dependencies (testing, building, etc.).

```json
{
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0",
    "hemlang/linter": "^2.0.0"
  }
}
```

Dev dependencies are:
- Installed during development
- Not installed when package is used as a dependency
- Used for testing, building, linting, etc.

### scripts

Named commands that can be run with `hpm run`.

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

**Running scripts:**
```bash
hpm run start
hpm run build
hpm test        # Shorthand for 'hpm run test'
```

**Passing arguments:**
```bash
hpm run test -- --verbose --filter=unit
```

**Common scripts:**

| Script | Purpose |
|--------|---------|
| `start` | Start the application |
| `dev` | Development mode with hot reload |
| `test` | Run tests |
| `build` | Build for production |
| `clean` | Remove build artifacts |
| `lint` | Check code style |
| `format` | Format code |

### files

Files and directories to include when the package is installed.

```json
{
  "files": [
    "src/",
    "lib/",
    "LICENSE",
    "README.md"
  ]
}
```

**Default behavior:** If not specified, includes:
- All files in the repository
- Excludes `.git/`, `node_modules/`, `hem_modules/`

**Use to:**
- Reduce package size
- Exclude test files from distribution
- Include only necessary files

### native

Native library requirements.

```json
{
  "native": {
    "requires": ["libcurl", "openssl", "sqlite3"]
  }
}
```

Documents native dependencies that must be installed on the system.

## Validation

hpm validates package.json on various operations. Common validation errors:

### Missing required fields

```
Error: package.json missing required field: name
```

**Fix:** Add the required field.

### Invalid name format

```
Error: Invalid package name. Must be in owner/repo format.
```

**Fix:** Use `owner/repo` format.

### Invalid version

```
Error: Invalid version "1.0". Must be semver format (X.Y.Z).
```

**Fix:** Use full semver format (`1.0.0`).

### Invalid JSON

```
Error: package.json is not valid JSON
```

**Fix:** Check JSON syntax (commas, quotes, brackets).

## Creating package.json

### Interactive

```bash
hpm init
```

Prompts for each field interactively.

### With Defaults

```bash
hpm init --yes
```

Creates with default values:
```json
{
  "name": "directory-name/directory-name",
  "version": "1.0.0",
  "description": "",
  "author": "",
  "license": "MIT",
  "main": "src/index.hml",
  "dependencies": {},
  "devDependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

### Manual

Create the file manually:

```bash
cat > package.json << 'EOF'
{
  "name": "yourname/your-package",
  "version": "1.0.0",
  "description": "Your package description",
  "main": "src/index.hml",
  "dependencies": {},
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
EOF
```

## Best Practices

1. **Always specify main** - Don't rely on default
2. **Use caret ranges** - `^1.0.0` for most dependencies
3. **Separate dev dependencies** - Keep test/build deps in devDependencies
4. **Include keywords** - Help users find your package
5. **Document scripts** - Name scripts clearly
6. **Specify license** - Required for open source
7. **Add description** - Help users understand purpose

## See Also

- [Creating Packages](creating-packages.md) - Publishing guide
- [Versioning](versioning.md) - Version constraints
- [Project Setup](project-setup.md) - Project structure
