# Troubleshooting

Solutions to common hpm issues.

## Installation Issues

### "hemlock: command not found"

**Cause:** Hemlock is not installed or not in PATH.

**Solution:**

```bash
# Check if hemlock exists
which hemlock

# If not found, install Hemlock first
# Visit: https://github.com/hemlang/hemlock

# After installation, verify
hemlock --version
```

### "hpm: command not found"

**Cause:** hpm is not installed or not in PATH.

**Solution:**

```bash
# Check where hpm is installed
ls -la /usr/local/bin/hpm
ls -la ~/.local/bin/hpm

# If using custom location, add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Reinstall if needed
cd /path/to/hpm
sudo make install
```

### "Permission denied" during install

**Cause:** No write permission to install directory.

**Solution:**

```bash
# Option 1: Use sudo for system-wide install
sudo make install

# Option 2: Install to user directory (no sudo)
make install PREFIX=$HOME/.local
```

## Dependency Issues

### "Package not found" (exit code 2)

**Cause:** The package doesn't exist on GitHub.

**Solution:**

```bash
# Verify package exists
# Check: https://github.com/owner/repo

# Verify spelling
hpm install hemlang/sprout  # Correct
hpm install hemlan/sprout   # Wrong owner
hpm install hemlang/spout   # Wrong repo

# Check for typos in package.json
cat package.json | grep -A 5 dependencies
```

### "Version not found" (exit code 3)

**Cause:** No release matches the version constraint.

**Solution:**

```bash
# List available versions (check GitHub releases/tags)
# Tags must start with 'v' (e.g., v1.0.0)

# Use a valid version constraint
hpm install owner/repo@^1.0.0

# Try latest version
hpm install owner/repo

# Check available tags on GitHub
# https://github.com/owner/repo/tags
```

### "Dependency conflict" (exit code 1)

**Cause:** Two packages require incompatible versions of a dependency.

**Solution:**

```bash
# See the conflict
hpm install --verbose

# Check what requires the dependency
hpm why conflicting/package

# Solutions:
# 1. Update the conflicting package
hpm update problem/package

# 2. Change version constraints in package.json
# Edit to allow compatible versions

# 3. Remove one of the conflicting packages
hpm uninstall one/package
```

### "Circular dependency" (exit code 8)

**Cause:** Package A depends on B, which depends on A.

**Solution:**

```bash
# Identify the cycle
hpm install --verbose

# This is usually a bug in the packages
# Contact package maintainers

# Workaround: avoid one of the packages
```

## Network Issues

### "Network error" (exit code 4)

**Cause:** Cannot connect to GitHub API.

**Solution:**

```bash
# Check internet connection
ping github.com

# Check if GitHub API is accessible
curl -I https://api.github.com

# Try again (hpm retries automatically)
hpm install

# Use offline mode if packages are cached
hpm install --offline

# Check proxy settings if behind firewall
export HTTPS_PROXY=http://proxy:8080
hpm install
```

### "GitHub rate limit exceeded" (exit code 7)

**Cause:** Too many API requests without authentication.

**Solution:**

```bash
# Option 1: Authenticate with GitHub token (recommended)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Create token: GitHub → Settings → Developer settings → Personal access tokens

# Option 2: Save token in config file
mkdir -p ~/.hpm
echo '{"github_token": "ghp_xxxxxxxxxxxx"}' > ~/.hpm/config.json

# Option 3: Wait for rate limit reset (resets hourly)

# Option 4: Use offline mode
hpm install --offline
```

### Connection timeout

**Cause:** Slow network or GitHub API issues.

**Solution:**

```bash
# hpm retries automatically with exponential backoff

# Check if GitHub is having issues
# Visit: https://www.githubstatus.com

# Try again later
hpm install

# Use cached packages
hpm install --offline
```

## Package.json Issues

### "Invalid package.json" (exit code 5)

**Cause:** Malformed or missing required fields.

**Solution:**

```bash
# Validate JSON syntax
cat package.json | python -m json.tool

# Check required fields
cat package.json

# Required fields:
# - "name": "owner/repo" format
# - "version": "X.Y.Z" format

# Regenerate if needed
rm package.json
hpm init
```

### "name" format error

**Cause:** Package name not in `owner/repo` format.

**Solution:**

```json
// Wrong
{
  "name": "my-package"
}

// Correct
{
  "name": "yourusername/my-package"
}
```

### "version" format error

**Cause:** Version not in semver format.

**Solution:**

```json
// Wrong
{
  "version": "1.0"
}

// Correct
{
  "version": "1.0.0"
}
```

## Lock File Issues

### Lock file out of sync

**Cause:** package.json modified without running install.

**Solution:**

```bash
# Regenerate lock file
rm package-lock.json
hpm install
```

### Corrupted lock file

**Cause:** Invalid JSON or manual edits.

**Solution:**

```bash
# Check JSON validity
cat package-lock.json | python -m json.tool

# Regenerate
rm package-lock.json
hpm install
```

## hem_modules Issues

### Packages not installing

**Cause:** Various possible issues.

**Solution:**

```bash
# Clean and reinstall
rm -rf hem_modules
hpm install

# Check verbose output
hpm install --verbose
```

### Import not working

**Cause:** Package not properly installed or wrong import path.

**Solution:**

```bash
# Verify package is installed
ls hem_modules/owner/repo/

# Check package.json main field
cat hem_modules/owner/repo/package.json

# Correct import format
import { x } from "owner/repo";          # Uses main entry
import { y } from "owner/repo/subpath";  # Subpath import
```

### "Module not found" error

**Cause:** Import path doesn't resolve to a file.

**Solution:**

```bash
# Check import path
ls hem_modules/owner/repo/src/

# Check for index.hml
ls hem_modules/owner/repo/src/index.hml

# Verify main field in package.json
cat hem_modules/owner/repo/package.json | grep main
```

## Cache Issues

### Cache taking too much space

**Solution:**

```bash
# View cache size
hpm cache list

# Clear cache
hpm cache clean
```

### Cache permissions

**Solution:**

```bash
# Fix permissions
chmod -R u+rw ~/.hpm/cache

# Or remove and reinstall
rm -rf ~/.hpm/cache
hpm install
```

### Using wrong cache

**Solution:**

```bash
# Check cache location
echo $HPM_CACHE_DIR
ls ~/.hpm/cache

# Clear environment variable if incorrect
unset HPM_CACHE_DIR
```

## Script Issues

### "Script not found"

**Cause:** Script name doesn't exist in package.json.

**Solution:**

```bash
# List available scripts
cat package.json | grep -A 20 scripts

# Check spelling
hpm run test    # Correct
hpm run tests   # Wrong if script is named "test"
```

### Script fails

**Cause:** Error in the script command.

**Solution:**

```bash
# Run command directly to see error
hemlock test/run.hml

# Check script definition
cat package.json | grep test
```

## Debugging

### Enable verbose output

```bash
hpm install --verbose
```

### Check hpm version

```bash
hpm --version
```

### Check hemlock version

```bash
hemlock --version
```

### Dry run

Preview without making changes:

```bash
hpm install --dry-run
```

### Clean slate

Start fresh:

```bash
rm -rf hem_modules package-lock.json
hpm install
```

## Getting Help

### Command help

```bash
hpm --help
hpm install --help
```

### Report issues

If you encounter a bug:

1. Check existing issues: https://github.com/hemlang/hpm/issues
2. Create a new issue with:
   - hpm version (`hpm --version`)
   - Hemlock version (`hemlock --version`)
   - Operating system
   - Steps to reproduce
   - Error message (use `--verbose`)

## Exit Code Reference

| Code | Meaning | Common Solution |
|------|---------|-----------------|
| 0 | Success | - |
| 1 | Dependency conflict | Update or change constraints |
| 2 | Package not found | Check spelling, verify repo exists |
| 3 | Version not found | Check available versions on GitHub |
| 4 | Network error | Check connection, retry |
| 5 | Invalid package.json | Fix JSON syntax and required fields |
| 6 | Integrity check failed | Clear cache, reinstall |
| 7 | GitHub rate limit | Add GITHUB_TOKEN |
| 8 | Circular dependency | Contact package maintainers |

## See Also

- [Installation](installation.md) - Installation guide
- [Configuration](configuration.md) - Configuration options
- [Commands](commands.md) - Command reference
