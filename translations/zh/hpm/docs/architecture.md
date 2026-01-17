# Architecture

Internal architecture and design of hpm. This document is for contributors and those interested in understanding how hpm works.

## Overview

hpm is written in Hemlock and consists of several modules that handle different aspects of package management:

```
src/
├── main.hml        # CLI entry point and command routing
├── manifest.hml    # package.json handling
├── lockfile.hml    # package-lock.json handling
├── semver.hml      # Semantic versioning
├── resolver.hml    # Dependency resolution
├── github.hml      # GitHub API client
├── installer.hml   # Package downloading and extraction
└── cache.hml       # Global cache management
```

## Module Responsibilities

### main.hml

The entry point for the CLI application.

**Responsibilities:**
- Parse command-line arguments
- Route commands to appropriate handlers
- Display help and version information
- Handle global flags (--verbose, --dry-run, etc.)
- Exit with appropriate codes

**Key functions:**
- `main()` - Entry point, parses args and dispatches commands
- `cmd_init()` - Handle `hpm init`
- `cmd_install()` - Handle `hpm install`
- `cmd_uninstall()` - Handle `hpm uninstall`
- `cmd_update()` - Handle `hpm update`
- `cmd_list()` - Handle `hpm list`
- `cmd_outdated()` - Handle `hpm outdated`
- `cmd_run()` - Handle `hpm run`
- `cmd_why()` - Handle `hpm why`
- `cmd_cache()` - Handle `hpm cache`

**Command shortcuts:**
```hemlock
let shortcuts = {
    "i": "install",
    "rm": "uninstall",
    "remove": "uninstall",
    "ls": "list",
    "up": "update"
};
```

### manifest.hml

Handles reading and writing `package.json` files.

**Responsibilities:**
- Read/write package.json
- Validate package structure
- Manage dependencies
- Parse package specifiers (owner/repo@version)

**Key functions:**
```hemlock
create_default(): Manifest           // Create empty manifest
read_manifest(): Manifest            // Read from file
write_manifest(m: Manifest)          // Write to file
validate(m: Manifest): bool          // Validate structure
get_all_dependencies(m): Map         // Get deps + devDeps
add_dependency(m, pkg, ver, dev)     // Add dependency
remove_dependency(m, pkg)            // Remove dependency
parse_specifier(spec): (name, ver)   // Parse "owner/repo@^1.0.0"
split_name(name): (owner, repo)      // Parse "owner/repo"
```

**Manifest structure:**
```hemlock
type Manifest = {
    name: string,
    version: string,
    description: string?,
    author: string?,
    license: string?,
    repository: string?,
    main: string?,
    dependencies: Map<string, string>,
    devDependencies: Map<string, string>,
    scripts: Map<string, string>
};
```

### lockfile.hml

Manages the `package-lock.json` file for reproducible installs.

**Responsibilities:**
- Create/read/write lock files
- Track exact resolved versions
- Store download URLs and integrity hashes
- Prune orphaned dependencies

**Key functions:**
```hemlock
create_empty(): Lockfile              // Create empty lockfile
read_lockfile(): Lockfile             // Read from file
write_lockfile(l: Lockfile)           // Write to file
create_entry(ver, url, hash, deps)    // Create lock entry
get_locked(l, pkg): LockEntry?        // Get locked version
set_locked(l, pkg, entry)             // Set locked version
remove_locked(l, pkg)                 // Remove entry
prune(l, keep: Set)                   // Remove orphans
needs_update(l, m): bool              // Check if out of sync
```

**Lockfile structure:**
```hemlock
type Lockfile = {
    lockVersion: int,
    hemlock: string,
    dependencies: Map<string, LockEntry>
};

type LockEntry = {
    version: string,
    resolved: string,     // Download URL
    integrity: string,    // SHA256 hash
    dependencies: Map<string, string>
};
```

### semver.hml

Full implementation of Semantic Versioning 2.0.0.

**Responsibilities:**
- Parse version strings
- Compare versions
- Parse and evaluate version constraints
- Find versions satisfying constraints

**Key functions:**
```hemlock
// Parsing
parse(s: string): Version             // "1.2.3-beta+build" → Version
stringify(v: Version): string         // Version → "1.2.3-beta+build"

// Comparison
compare(a, b: Version): int           // -1, 0, or 1
gt(a, b), gte(a, b), lt(a, b), lte(a, b), eq(a, b): bool

// Constraints
parse_constraint(s: string): Constraint    // "^1.2.3" → Constraint
satisfies(v: Version, c: Constraint): bool // Check if v matches c
max_satisfying(versions, c): Version?      // Find highest match
sort(versions): [Version]                  // Sort ascending

// Utilities
constraints_overlap(a, b: Constraint): bool  // Check compatibility
```

**Version structure:**
```hemlock
type Version = {
    major: int,
    minor: int,
    patch: int,
    prerelease: [string]?,  // e.g., ["beta", "1"]
    build: string?          // e.g., "20230101"
};
```

**Constraint types:**
```hemlock
type Constraint =
    | Exact(Version)           // "1.2.3"
    | Caret(Version)           // "^1.2.3" → >=1.2.3 <2.0.0
    | Tilde(Version)           // "~1.2.3" → >=1.2.3 <1.3.0
    | Range(op, Version)       // ">=1.0.0", "<2.0.0"
    | And(Constraint, Constraint)  // Combined ranges
    | Any;                     // "*"
```

### resolver.hml

Implements npm-style dependency resolution.

**Responsibilities:**
- Resolve dependency trees
- Detect version conflicts
- Detect circular dependencies
- Build visualization trees

**Key functions:**
```hemlock
resolve(manifest, lockfile): ResolveResult
    // Main resolver: returns flat map of all dependencies with resolved versions

resolve_version(pkg, constraints: [string]): ResolvedPackage?
    // Find version satisfying all constraints

detect_cycles(deps: Map): [Cycle]?
    // Find circular dependencies using DFS

build_tree(lockfile): Tree
    // Create tree structure for display

find_why(pkg, lockfile): [Chain]
    // Find dependency chains explaining why pkg is installed
```

**Resolution algorithm:**

1. **Collect constraints**: Walk manifest and transitive dependencies
2. **Resolve each package**: For each package:
   - Get all version constraints from dependents
   - Fetch available versions from GitHub
   - Find highest version satisfying ALL constraints
   - Error if no version satisfies all (conflict)
3. **Detect cycles**: Run DFS to find circular dependencies
4. **Return flat map**: Package name → resolved version info

**ResolveResult structure:**
```hemlock
type ResolveResult = {
    packages: Map<string, ResolvedPackage>,
    conflicts: [Conflict]?,
    cycles: [Cycle]?
};

type ResolvedPackage = {
    name: string,
    version: Version,
    url: string,
    dependencies: Map<string, string>
};
```

### github.hml

GitHub API client for package discovery and downloads.

**Responsibilities:**
- Fetch available versions (tags)
- Download package.json from repositories
- Download release tarballs
- Handle authentication and rate limits

**Key functions:**
```hemlock
get_token(): string?
    // Get token from env or config

github_request(url, headers?): Response
    // Make API request with retries

get_tags(owner, repo): [string]
    // Get version tags (v1.0.0, v1.1.0, etc.)

get_package_json(owner, repo, ref): Manifest
    // Fetch package.json at specific tag/commit

download_tarball(owner, repo, tag): bytes
    // Download release archive

repo_exists(owner, repo): bool
    // Check if repository exists

get_repo_info(owner, repo): RepoInfo
    // Get repository metadata
```

**Retry logic:**
- Exponential backoff: 1s, 2s, 4s, 8s
- Retries on: 403 (rate limit), 5xx (server error), network errors
- Max 4 retries
- Reports rate limit errors clearly

**API endpoints used:**
```
GET /repos/{owner}/{repo}/tags
GET /repos/{owner}/{repo}/contents/package.json?ref={tag}
GET /repos/{owner}/{repo}/tarball/{tag}
GET /repos/{owner}/{repo}
```

### installer.hml

Handles downloading and extracting packages.

**Responsibilities:**
- Download packages from GitHub
- Extract tarballs to hem_modules
- Check/use cached packages
- Install/uninstall packages

**Key functions:**
```hemlock
install_package(pkg: ResolvedPackage): bool
    // Download and install single package

install_all(packages: Map, options): InstallResult
    // Install all resolved packages

uninstall_package(name: string): bool
    // Remove package from hem_modules

get_installed(): Map<string, string>
    // List currently installed packages

verify_integrity(pkg): bool
    // Verify package integrity

prefetch_packages(packages: Map): void
    // Parallel download to cache (experimental)
```

**Installation process:**

1. Check if already installed at correct version
2. Check cache for tarball
3. If not cached, download from GitHub
4. Store in cache for future use
5. Extract to `hem_modules/owner/repo/`
6. Verify installation

**Directory structure created:**
```
hem_modules/
└── owner/
    └── repo/
        ├── package.json
        ├── src/
        └── ...
```

### cache.hml

Manages the global package cache.

**Responsibilities:**
- Store downloaded tarballs
- Retrieve cached packages
- List cached packages
- Clear cache
- Manage configuration

**Key functions:**
```hemlock
get_cache_dir(): string
    // Get cache directory (respects HPM_CACHE_DIR)

get_config_dir(): string
    // Get config directory (~/.hpm)

is_cached(owner, repo, version): bool
    // Check if tarball is cached

get_cached_path(owner, repo, version): string
    // Get path to cached tarball

store_tarball_file(owner, repo, version, data): void
    // Save tarball to cache

list_cached(): [CachedPackage]
    // List all cached packages

clear_cache(): int
    // Remove all cached packages, return bytes freed

get_cache_size(): int
    // Calculate total cache size

read_config(): Config
    // Read ~/.hpm/config.json

write_config(c: Config): void
    // Write config file
```

**Cache structure:**
```
~/.hpm/
├── config.json
└── cache/
    └── owner/
        └── repo/
            ├── 1.0.0.tar.gz
            └── 1.1.0.tar.gz
```

## Data Flow

### Install Command Flow

```
hpm install owner/repo@^1.0.0
         │
         ▼
    ┌─────────┐
    │ main.hml │ Parse args, call cmd_install
    └────┬────┘
         │
         ▼
    ┌──────────┐
    │manifest.hml│ Read package.json, add dependency
    └────┬─────┘
         │
         ▼
    ┌──────────┐
    │resolver.hml│ Resolve all dependencies
    └────┬─────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ semver.hml│ Get versions, find satisfying
    └────┬─────┘    └─────────┘
         │
         ▼
    ┌───────────┐
    │installer.hml│ Download and extract packages
    └────┬──────┘
         │
         ├───────────────┐
         ▼               ▼
    ┌──────────┐    ┌─────────┐
    │ github.hml│    │ cache.hml│ Download or use cache
    └──────────┘    └─────────┘
         │
         ▼
    ┌──────────┐
    │lockfile.hml│ Update package-lock.json
    └──────────┘
```

### Resolution Algorithm Detail

```
Input: manifest.dependencies, manifest.devDependencies, existing lockfile

1. Initialize:
   - constraints = {} // Map<string, [Constraint]>
   - resolved = {}    // Map<string, ResolvedPackage>
   - queue = [direct dependencies]

2. While queue not empty:
   a. pkg = queue.pop()
   b. If pkg already resolved, skip
   c. Get all constraints for pkg from dependents
   d. Fetch available versions from GitHub (cached)
   e. Find max version satisfying all constraints
   f. If none found: CONFLICT
   g. resolved[pkg] = {version, url, deps}
   h. Add pkg's dependencies to queue

3. Detect cycles in resolved graph
   - If cycle found: ERROR

4. Return resolved map
```

## Error Handling

### Exit Codes

Defined in main.hml:

```hemlock
let EXIT_SUCCESS = 0;
let EXIT_CONFLICT = 1;
let EXIT_NOT_FOUND = 2;
let EXIT_VERSION_NOT_FOUND = 3;
let EXIT_NETWORK = 4;
let EXIT_INVALID_MANIFEST = 5;
let EXIT_INTEGRITY = 6;
let EXIT_RATE_LIMIT = 7;
let EXIT_CIRCULAR = 8;
```

### Error Propagation

Errors bubble up through return values:

```hemlock
fn resolve_version(pkg): Result<Version, ResolveError> {
    let versions = github.get_tags(owner, repo)?;  // ? propagates
    // ...
}
```

## Testing

### Test Framework

Custom test framework in `test/framework.hml`:

```hemlock
fn suite(name: string, tests: fn()) {
    print("Suite: " + name);
    tests();
}

fn test(name: string, body: fn()) {
    try {
        body();
        print("  ✓ " + name);
    } catch e {
        print("  ✗ " + name + ": " + e);
        failed += 1;
    }
}

fn assert_eq<T>(actual: T, expected: T) {
    if actual != expected {
        throw "Expected " + expected + ", got " + actual;
    }
}
```

### Test Files

- `test/test_semver.hml` - Version parsing, comparison, constraints
- `test/test_manifest.hml` - Manifest reading/writing, validation
- `test/test_lockfile.hml` - Lockfile operations
- `test/test_cache.hml` - Cache management

### Running Tests

```bash
# All tests
make test

# Specific tests
make test-semver
make test-manifest
make test-lockfile
make test-cache
```

## Future Improvements

### Planned Features

1. **Integrity verification** - Full SHA256 hash checking
2. **Workspaces** - Monorepo support
3. **Plugin system** - Extensible commands
4. **Audit** - Security vulnerability checking
5. **Private registry** - Self-hosted package hosting

### Known Limitations

1. **Bundler bug** - Can't create standalone executable
2. **Parallel downloads** - Experimental, may have race conditions
3. **Integrity** - SHA256 not fully implemented

## Contributing

### Code Style

- Use 4-space indentation
- Functions should do one thing
- Comment complex logic
- Write tests for new features

### Adding a Command

1. Add handler in `main.hml`:
   ```hemlock
   fn cmd_newcmd(args: [string]) {
       // Implementation
   }
   ```

2. Add to command dispatch:
   ```hemlock
   match command {
       "newcmd" => cmd_newcmd(args),
       // ...
   }
   ```

3. Update help text

### Adding a Module

1. Create `src/newmodule.hml`
2. Export public interface
3. Import in modules that need it
4. Add tests in `test/test_newmodule.hml`

## See Also

- [Commands](commands.md) - CLI reference
- [Creating Packages](creating-packages.md) - Package development
- [Versioning](versioning.md) - Semantic versioning
