# Exit Codes

Reference for hpm exit codes and their meanings.

## Exit Code Table

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | Command completed successfully |
| 1 | CONFLICT | Dependency version conflict |
| 2 | NOT_FOUND | Package not found |
| 3 | VERSION_NOT_FOUND | Requested version not found |
| 4 | NETWORK | Network error |
| 5 | INVALID_MANIFEST | Invalid package.json |
| 6 | INTEGRITY | Integrity check failed |
| 7 | RATE_LIMIT | GitHub API rate limit exceeded |
| 8 | CIRCULAR | Circular dependency detected |

## Detailed Descriptions

### Exit Code 0: SUCCESS

The command completed successfully.

```bash
$ hpm install
Installed 5 packages
$ echo $?
0
```

### Exit Code 1: CONFLICT

Two or more packages require incompatible versions of a dependency.

**Example:**
```
Error: Dependency conflict for hemlang/json

  package-a requires hemlang/json@^1.0.0 (>=1.0.0 <2.0.0)
  package-b requires hemlang/json@^2.0.0 (>=2.0.0 <3.0.0)

No version satisfies all constraints.
```

**Solutions:**
1. Check which packages have the conflict:
   ```bash
   hpm why hemlang/json
   ```
2. Update the conflicting package:
   ```bash
   hpm update package-a
   ```
3. Relax version constraints in package.json
4. Remove one of the conflicting packages

### Exit Code 2: NOT_FOUND

The specified package does not exist on GitHub.

**Example:**
```
Error: Package not found: hemlang/nonexistent

The repository hemlang/nonexistent does not exist on GitHub.
```

**Solutions:**
1. Verify package name spelling
2. Check if repository exists: `https://github.com/owner/repo`
3. Verify you have access (for private repos, set GITHUB_TOKEN)

### Exit Code 3: VERSION_NOT_FOUND

No version matches the specified constraint.

**Example:**
```
Error: No version of hemlang/json matches constraint ^5.0.0

Available versions: 1.0.0, 1.1.0, 1.2.0, 2.0.0
```

**Solutions:**
1. Check available versions on GitHub releases/tags
2. Use a valid version constraint
3. Version tags must start with 'v' (e.g., `v1.0.0`)

### Exit Code 4: NETWORK

Network-related error occurred.

**Example:**
```
Error: Network error: could not connect to api.github.com

Please check your internet connection and try again.
```

**Solutions:**
1. Check internet connection
2. Check if GitHub is accessible
3. Verify proxy settings if behind firewall
4. Use `--offline` if packages are cached:
   ```bash
   hpm install --offline
   ```
5. Wait and retry (hpm retries automatically)

### Exit Code 5: INVALID_MANIFEST

The package.json file is invalid or malformed.

**Example:**
```
Error: Invalid package.json

  - Missing required field: name
  - Invalid version format: "1.0"
```

**Solutions:**
1. Check JSON syntax (use a JSON validator)
2. Ensure required fields exist (`name`, `version`)
3. Verify field formats:
   - name: `owner/repo` format
   - version: `X.Y.Z` semver format
4. Regenerate:
   ```bash
   rm package.json
   hpm init
   ```

### Exit Code 6: INTEGRITY

Package integrity verification failed.

**Example:**
```
Error: Integrity check failed for hemlang/json@1.0.0

Expected: sha256-abc123...
Actual:   sha256-def456...

The downloaded package may be corrupted.
```

**Solutions:**
1. Clear cache and reinstall:
   ```bash
   hpm cache clean
   hpm install
   ```
2. Check for network issues (partial downloads)
3. Verify package wasn't tampered with

### Exit Code 7: RATE_LIMIT

GitHub API rate limit has been exceeded.

**Example:**
```
Error: GitHub API rate limit exceeded

Unauthenticated rate limit: 60 requests/hour
Current usage: 60/60

Rate limit resets at: 2024-01-15 10:30:00 UTC
```

**Solutions:**
1. **Authenticate with GitHub** (recommended):
   ```bash
   export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
   hpm install
   ```
2. Wait for rate limit to reset (resets hourly)
3. Use offline mode if packages are cached:
   ```bash
   hpm install --offline
   ```

### Exit Code 8: CIRCULAR

Circular dependency detected in the dependency graph.

**Example:**
```
Error: Circular dependency detected

  package-a@1.0.0
  └── package-b@1.0.0
      └── package-a@1.0.0  (circular!)

Cannot resolve dependency tree.
```

**Solutions:**
1. This is usually a bug in the packages themselves
2. Contact package maintainers
3. Avoid using one of the circular packages

## Using Exit Codes in Scripts

### Bash

```bash
#!/bin/bash

hpm install
exit_code=$?

case $exit_code in
  0)
    echo "Installation successful"
    ;;
  1)
    echo "Dependency conflict - check version constraints"
    exit 1
    ;;
  2)
    echo "Package not found - check package name"
    exit 1
    ;;
  4)
    echo "Network error - check connection"
    exit 1
    ;;
  7)
    echo "Rate limited - set GITHUB_TOKEN"
    exit 1
    ;;
  *)
    echo "Unknown error: $exit_code"
    exit 1
    ;;
esac
```

### CI/CD

```yaml
# GitHub Actions
- name: Install dependencies
  run: |
    hpm install
    if [ $? -eq 7 ]; then
      echo "::error::GitHub rate limit exceeded. Add GITHUB_TOKEN."
      exit 1
    fi
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Make

```makefile
install:
	@hpm install || (echo "Installation failed with code $$?"; exit 1)

test: install
	@hpm test
```

## Troubleshooting by Exit Code

### Quick Reference

| Code | First Thing to Check |
|------|---------------------|
| 1 | Run `hpm why <package>` to see conflict |
| 2 | Verify package name on GitHub |
| 3 | Check available versions on GitHub tags |
| 4 | Check internet connection |
| 5 | Validate package.json syntax |
| 6 | Run `hpm cache clean && hpm install` |
| 7 | Set `GITHUB_TOKEN` environment variable |
| 8 | Contact package maintainers |

## See Also

- [Troubleshooting](troubleshooting.md) - Detailed solutions
- [Commands](commands.md) - Command reference
- [Configuration](configuration.md) - Setting up GitHub token
