# Command Reference

Complete reference for all hpm commands.

## Global Options

These options work with any command:

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help message |
| `--version`, `-v` | Show hpm version |
| `--verbose` | Show detailed output |

## Commands

### hpm init

Create a new `package.json` file.

```bash
hpm init        # Interactive mode
hpm init --yes  # Accept all defaults
hpm init -y     # Short form
```

**Options:**

| Option | Description |
|--------|-------------|
| `--yes`, `-y` | Accept default values for all prompts |

**Interactive prompts:**
- Package name (owner/repo format)
- Version (default: 1.0.0)
- Description
- Author
- License (default: MIT)
- Main file (default: src/index.hml)

**Example:**

```bash
$ hpm init
Package name (owner/repo): alice/my-lib
Version (1.0.0):
Description: A utility library
Author: Alice <alice@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

---

### hpm install

Install dependencies or add new packages.

```bash
hpm install                           # Install all from package.json
hpm install owner/repo                # Add and install package
hpm install owner/repo@^1.0.0        # With version constraint
hpm install owner/repo --dev         # As dev dependency
hpm i owner/repo                      # Short form
```

**Options:**

| Option | Description |
|--------|-------------|
| `--dev`, `-D` | Add to devDependencies |
| `--verbose` | Show detailed progress |
| `--dry-run` | Preview without installing |
| `--offline` | Install from cache only (no network) |
| `--parallel` | Enable parallel downloads (experimental) |

**Version constraint syntax:**

| Syntax | Example | Meaning |
|--------|---------|---------|
| (none) | `owner/repo` | Latest version |
| Exact | `owner/repo@1.2.3` | Exactly 1.2.3 |
| Caret | `owner/repo@^1.2.3` | >=1.2.3 <2.0.0 |
| Tilde | `owner/repo@~1.2.3` | >=1.2.3 <1.3.0 |
| Range | `owner/repo@>=1.0.0` | At least 1.0.0 |

**Examples:**

```bash
# Install all dependencies
hpm install

# Install specific package
hpm install hemlang/json

# Install with version constraint
hpm install hemlang/sprout@^2.0.0

# Install as dev dependency
hpm install hemlang/test-utils --dev

# Preview what would be installed
hpm install hemlang/sprout --dry-run

# Verbose output
hpm install --verbose

# Install from cache only (offline)
hpm install --offline
```

**Output:**

```
Installing dependencies...
  + hemlang/sprout@2.1.0
  + hemlang/router@1.5.0 (dependency of hemlang/sprout)

Installed 2 packages in 1.2s
```

---

### hpm uninstall

Remove a package.

```bash
hpm uninstall owner/repo
hpm rm owner/repo          # Short form
hpm remove owner/repo      # Alternative
```

**Examples:**

```bash
hpm uninstall hemlang/sprout
```

**Output:**

```
Removed hemlang/sprout@2.1.0
Updated package.json
Updated package-lock.json
```

---

### hpm update

Update packages to latest versions within constraints.

```bash
hpm update              # Update all packages
hpm update owner/repo   # Update specific package
hpm up owner/repo       # Short form
```

**Options:**

| Option | Description |
|--------|-------------|
| `--verbose` | Show detailed progress |
| `--dry-run` | Preview without updating |

**Examples:**

```bash
# Update all packages
hpm update

# Update specific package
hpm update hemlang/sprout

# Preview updates
hpm update --dry-run
```

**Output:**

```
Updating dependencies...
  hemlang/sprout: 2.0.0 → 2.1.0
  hemlang/router: 1.4.0 → 1.5.0

Updated 2 packages
```

---

### hpm list

Show installed packages.

```bash
hpm list              # Show full dependency tree
hpm list --depth=0    # Direct dependencies only
hpm list --depth=1    # One level of transitive deps
hpm ls                # Short form
```

**Options:**

| Option | Description |
|--------|-------------|
| `--depth=N` | Limit tree depth (default: all) |

**Examples:**

```bash
$ hpm list
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   ├── hemlang/router@1.5.0
│   └── hemlang/middleware@1.2.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)

$ hpm list --depth=0
my-project@1.0.0
├── hemlang/sprout@2.1.0
├── hemlang/json@1.2.3
└── hemlang/test-utils@1.0.0 (dev)
```

---

### hpm outdated

Show packages with newer versions available.

```bash
hpm outdated
```

**Output:**

```
Package            Current  Wanted  Latest
hemlang/sprout     2.0.0    2.0.5   2.1.0
hemlang/router     1.4.0    1.4.2   1.5.0
```

- **Current**: Installed version
- **Wanted**: Highest version matching constraint
- **Latest**: Latest available version

---

### hpm run

Execute a script from package.json.

```bash
hpm run <script>
hpm run <script> -- <args>
```

**Examples:**

Given this package.json:

```json
{
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Run scripts:

```bash
hpm run start
hpm run test
hpm run build

# Pass arguments to script
hpm run test -- --verbose
```

---

### hpm test

Shorthand for `hpm run test`.

```bash
hpm test
hpm test -- --verbose
```

Equivalent to:

```bash
hpm run test
```

---

### hpm why

Explain why a package is installed (show dependency chain).

```bash
hpm why owner/repo
```

**Example:**

```bash
$ hpm why hemlang/router

hemlang/router@1.5.0 is installed because:

my-project@1.0.0
└── hemlang/sprout@2.1.0
    └── hemlang/router@1.5.0
```

---

### hpm cache

Manage the global package cache.

```bash
hpm cache list    # List cached packages
hpm cache clean   # Clear all cached packages
```

**Subcommands:**

| Subcommand | Description |
|------------|-------------|
| `list` | Show all cached packages and sizes |
| `clean` | Remove all cached packages |

**Examples:**

```bash
$ hpm cache list
Cached packages in ~/.hpm/cache:

hemlang/sprout
  2.0.0 (1.2 MB)
  2.1.0 (1.3 MB)
hemlang/router
  1.5.0 (450 KB)

Total: 2.95 MB

$ hpm cache clean
Cleared cache (2.95 MB freed)
```

---

## Command Shortcuts

For convenience, several commands have short aliases:

| Command | Shortcuts |
|---------|-----------|
| `install` | `i` |
| `uninstall` | `rm`, `remove` |
| `list` | `ls` |
| `update` | `up` |

**Examples:**

```bash
hpm i hemlang/sprout        # hpm install hemlang/sprout
hpm rm hemlang/sprout       # hpm uninstall hemlang/sprout
hpm ls                      # hpm list
hpm up                      # hpm update
```

---

## Exit Codes

hpm uses specific exit codes to indicate different error conditions:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Dependency conflict |
| 2 | Package not found |
| 3 | Version not found |
| 4 | Network error |
| 5 | Invalid package.json |
| 6 | Integrity check failed |
| 7 | GitHub rate limit exceeded |
| 8 | Circular dependency |

Use exit codes in scripts:

```bash
hpm install
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
```

---

## Environment Variables

hpm respects these environment variables:

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub API token for authentication |
| `HPM_CACHE_DIR` | Override cache directory location |
| `HOME` | User home directory (for config/cache) |

**Examples:**

```bash
# Use GitHub token for higher rate limits
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Use custom cache directory
export HPM_CACHE_DIR=/tmp/hpm-cache
hpm install
```

---

## See Also

- [Configuration](configuration.md) - Configuration files
- [Package Specification](package-spec.md) - package.json format
- [Troubleshooting](troubleshooting.md) - Common issues
