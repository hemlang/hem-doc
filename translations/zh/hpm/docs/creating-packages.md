# Creating Packages

This guide covers how to create, structure, and publish Hemlock packages.

## Overview

hpm uses GitHub as its package registry. Packages are identified by their GitHub `owner/repo` path, and versions are Git tags. Publishing is simply pushing a tagged release.

## Creating a New Package

### 1. Initialize the Package

Create a new directory and initialize:

```bash
mkdir my-package
cd my-package
hpm init
```

Answer the prompts:

```
Package name (owner/repo): yourusername/my-package
Version (1.0.0):
Description: A useful Hemlock package
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

### 2. Create the Project Structure

Recommended structure for packages:

```
my-package/
├── package.json          # Package manifest
├── README.md             # Documentation
├── LICENSE               # License file
├── src/
│   ├── index.hml         # Main entry point (exports public API)
│   ├── utils.hml         # Internal utilities
│   └── types.hml         # Type definitions
└── test/
    ├── framework.hml     # Test framework
    └── test_utils.hml    # Tests
```

### 3. Define Your Public API

**src/index.hml** - Main entry point:

```hemlock
// Re-export public API
export { parse, stringify } from "./parser.hml";
export { Config, Options } from "./types.hml";
export { process } from "./processor.hml";

// Direct exports
export fn create(options: Options): Config {
    // Implementation
}

export fn validate(config: Config): bool {
    // Implementation
}
```

### 4. Write Your package.json

Complete package.json example:

```json
{
  "name": "yourusername/my-package",
  "version": "1.0.0",
  "description": "A useful Hemlock package",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": "https://github.com/yourusername/my-package",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/json": "^1.0.0"
  },
  "devDependencies": {
    "hemlang/test-utils": "^1.0.0"
  },
  "scripts": {
    "test": "hemlock test/run.hml",
    "build": "hemlock --bundle src/index.hml -o dist/bundle.hmlc"
  },
  "keywords": ["utility", "parser", "config"],
  "files": [
    "src/",
    "LICENSE",
    "README.md"
  ]
}
```

## Package Naming

### Requirements

- Must be in `owner/repo` format
- `owner` should be your GitHub username or organization
- `repo` should be the repository name
- Use lowercase with hyphens for multi-word names

### Good Names

```
hemlang/sprout
alice/http-client
myorg/json-utils
bob/date-formatter
```

### Avoid

```
my-package          # Missing owner
alice/MyPackage     # PascalCase
alice/my_package    # Underscores
```

## Package Structure Best Practices

### Entry Point

The `main` field in package.json specifies the entry point:

```json
{
  "main": "src/index.hml"
}
```

This file should export your public API:

```hemlock
// Export everything users need
export { Parser, parse } from "./parser.hml";
export { Formatter, format } from "./formatter.hml";

// Types
export type { Config, Options } from "./types.hml";
```

### Internal vs Public

Keep internal implementation details private:

```
src/
├── index.hml          # Public: exported API
├── parser.hml         # Public: used by index.hml
├── formatter.hml      # Public: used by index.hml
└── internal/
    ├── helpers.hml    # Private: internal use only
    └── constants.hml  # Private: internal use only
```

Users import from your package root:

```hemlock
// Good - imports from public API
import { parse, Parser } from "yourusername/my-package";

// Also works - subpath import
import { validate } from "yourusername/my-package/validator";

// Discouraged - accessing internals
import { helper } from "yourusername/my-package/internal/helpers";
```

### Subpath Exports

Support importing from subpaths:

```
src/
├── index.hml              # Main entry
├── parser/
│   └── index.hml          # yourusername/pkg/parser
├── formatter/
│   └── index.hml          # yourusername/pkg/formatter
└── utils/
    └── index.hml          # yourusername/pkg/utils
```

Users can import:

```hemlock
import { parse } from "yourusername/my-package";           // Main
import { Parser } from "yourusername/my-package/parser";   // Subpath
import { format } from "yourusername/my-package/formatter";
```

## Dependencies

### Adding Dependencies

```bash
# Runtime dependency
hpm install hemlang/json

# Development dependency
hpm install hemlang/test-utils --dev
```

### Dependency Best Practices

1. **Use caret ranges** for most dependencies:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     }
   }
   ```

2. **Pin versions** only when necessary (API instability):
   ```json
   {
     "dependencies": {
       "unstable/lib": "1.2.3"
     }
   }
   ```

3. **Avoid overly restrictive ranges**:
   ```json
   // Bad: too restrictive
   "hemlang/json": ">=1.2.3 <1.2.5"

   // Good: allows compatible updates
   "hemlang/json": "^1.2.3"
   ```

4. **Keep dev dependencies separate**:
   ```json
   {
     "dependencies": {
       "hemlang/json": "^1.0.0"
     },
     "devDependencies": {
       "hemlang/test-utils": "^1.0.0"
     }
   }
   ```

## Testing Your Package

### Write Tests

**test/run.hml:**

```hemlock
import { suite, test, assert_eq } from "./framework.hml";
import { parse, stringify } from "../src/index.hml";

fn run_tests() {
    suite("Parser", fn() {
        test("parses valid input", fn() {
            let result = parse("hello");
            assert_eq(result.value, "hello");
        });

        test("handles empty input", fn() {
            let result = parse("");
            assert_eq(result.value, "");
        });
    });

    suite("Stringify", fn() {
        test("stringifies object", fn() {
            let obj = { name: "test" };
            let result = stringify(obj);
            assert_eq(result, '{"name":"test"}');
        });
    });
}

run_tests();
```

### Run Tests

Add a test script:

```json
{
  "scripts": {
    "test": "hemlock test/run.hml"
  }
}
```

Run with:

```bash
hpm test
```

## Publishing

### Prerequisites

1. Create a GitHub repository matching your package name
2. Ensure `package.json` is complete and valid
3. All tests pass

### Publishing Process

Publishing is simply pushing a Git tag:

```bash
# 1. Ensure everything is committed
git add .
git commit -m "Prepare v1.0.0 release"

# 2. Create a version tag (must start with 'v')
git tag v1.0.0

# 3. Push code and tags
git push origin main
git push origin v1.0.0
# Or push all tags at once
git push origin main --tags
```

### Version Tags

Tags must follow the format `vX.Y.Z`:

```bash
git tag v1.0.0      # Release
git tag v1.0.1      # Patch
git tag v1.1.0      # Minor
git tag v2.0.0      # Major
git tag v1.0.0-beta.1  # Pre-release
```

### Release Checklist

Before publishing a new version:

1. **Update version** in package.json
2. **Run tests**: `hpm test`
3. **Update CHANGELOG** (if you have one)
4. **Update README** if API changed
5. **Commit changes**
6. **Create tag**
7. **Push to GitHub**

### Automated Example

Create a release script:

```bash
#!/bin/bash
# release.sh - Release a new version

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh 1.0.0"
    exit 1
fi

# Run tests
hpm test || exit 1

# Update version in package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" package.json

# Commit and tag
git add package.json
git commit -m "Release v$VERSION"
git tag "v$VERSION"

# Push
git push origin main --tags

echo "Released v$VERSION"
```

## Users Installing Your Package

After publishing, users can install:

```bash
# Latest version
hpm install yourusername/my-package

# Specific version
hpm install yourusername/my-package@1.0.0

# Version constraint
hpm install yourusername/my-package@^1.0.0
```

And import:

```hemlock
import { parse, stringify } from "yourusername/my-package";
```

## Documentation

### README.md

Every package should have a README:

```markdown
# my-package

A brief description of what this package does.

## Installation

\`\`\`bash
hpm install yourusername/my-package
\`\`\`

## Usage

\`\`\`hemlock
import { parse } from "yourusername/my-package";

let result = parse("input");
\`\`\`

## API

### parse(input: string): Result

Parses the input string.

### stringify(obj: any): string

Converts object to string.

## License

MIT
```

### API Documentation

Document all public exports:

```hemlock
/// Parses the input string into a structured Result.
///
/// # Arguments
/// * `input` - The string to parse
///
/// # Returns
/// A Result containing the parsed data or an error
///
/// # Example
/// ```
/// let result = parse("hello world");
/// print(result.value);
/// ```
export fn parse(input: string): Result {
    // Implementation
}
```

## Versioning Guidelines

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backward compatible

### When to Bump

| Change Type | Version Bump |
|-------------|--------------|
| Breaking API change | MAJOR |
| Remove function/type | MAJOR |
| Change function signature | MAJOR |
| Add new function | MINOR |
| Add new feature | MINOR |
| Bug fix | PATCH |
| Documentation update | PATCH |
| Internal refactor | PATCH |

## See Also

- [Package Specification](package-spec.md) - Full package.json reference
- [Versioning](versioning.md) - Semantic versioning details
- [Configuration](configuration.md) - GitHub authentication
