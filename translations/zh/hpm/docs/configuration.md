# Configuration

This guide covers all configuration options for hpm.

## Overview

hpm can be configured through:

1. **Environment variables** - For runtime settings
2. **Global config file** - `~/.hpm/config.json`
3. **Project files** - `package.json` and `package-lock.json`

## Environment Variables

### GITHUB_TOKEN

GitHub API token for authentication.

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**Benefits of authentication:**
- Higher API rate limits (5000 vs 60 requests/hour)
- Access to private repositories
- Faster dependency resolution

**Creating a token:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` - For private repository access
   - `read:packages` - For GitHub Packages (if used)
4. Generate and copy the token

### HPM_CACHE_DIR

Override the default cache directory.

```bash
export HPM_CACHE_DIR=/custom/cache/path
```

Default: `~/.hpm/cache`

**Use cases:**
- CI/CD systems with custom cache locations
- Shared cache across projects
- Temporary cache for isolated builds

### HOME

User home directory. Used to locate:
- Config directory: `$HOME/.hpm/`
- Cache directory: `$HOME/.hpm/cache/`

Usually set by the system; override only if needed.

### Example .bashrc / .zshrc

```bash
# GitHub authentication (recommended)
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Custom cache location (optional)
# export HPM_CACHE_DIR=/path/to/cache

# Add hpm to PATH (if using custom install location)
export PATH="$HOME/.local/bin:$PATH"
```

## Global Configuration File

### Location

`~/.hpm/config.json`

### Format

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

### Creating the Config File

```bash
# Create config directory
mkdir -p ~/.hpm

# Create config file
cat > ~/.hpm/config.json << 'EOF'
{
  "github_token": "ghp_your_token_here"
}
EOF

# Secure the file (recommended)
chmod 600 ~/.hpm/config.json
```

### Token Priority

If both are set, environment variable takes precedence:

1. `GITHUB_TOKEN` environment variable (highest)
2. `~/.hpm/config.json` `github_token` field
3. No authentication (default)

## Directory Structure

### Global Directories

```
~/.hpm/
├── config.json          # Global configuration
└── cache/               # Package cache
    └── owner/
        └── repo/
            └── 1.0.0.tar.gz
```

### Project Directories

```
my-project/
├── package.json         # Project manifest
├── package-lock.json    # Dependency lock file
├── hem_modules/         # Installed packages
│   └── owner/
│       └── repo/
│           ├── package.json
│           └── src/
├── src/                 # Source code
└── test/                # Tests
```

## Package Cache

### Location

Default: `~/.hpm/cache/`

Override with: `HPM_CACHE_DIR` environment variable

### Structure

```
~/.hpm/cache/
├── hemlang/
│   ├── sprout/
│   │   ├── 2.0.0.tar.gz
│   │   └── 2.1.0.tar.gz
│   └── router/
│       └── 1.5.0.tar.gz
└── alice/
    └── http-client/
        └── 1.0.0.tar.gz
```

### Managing the Cache

```bash
# View cached packages
hpm cache list

# Clear entire cache
hpm cache clean
```

### Cache Behavior

- Packages are cached after first download
- Subsequent installs use cached versions
- Use `--offline` to install only from cache
- Cache is shared across all projects

## GitHub API Rate Limits

### Without Authentication

- **60 requests per hour** per IP address
- Shared across all unauthenticated users on same IP
- Quickly exhausted in CI/CD or with many dependencies

### With Authentication

- **5000 requests per hour** per authenticated user
- Personal rate limit, not shared

### Handling Rate Limits

hpm automatically:
- Retries with exponential backoff (1s, 2s, 4s, 8s)
- Reports rate limit errors with exit code 7
- Suggests authentication if rate limited

**Solutions when rate limited:**

```bash
# Option 1: Authenticate with GitHub token
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install

# Option 2: Wait for rate limit reset
# (Limits reset hourly)

# Option 3: Use offline mode (if packages are cached)
hpm install --offline
```

## Offline Mode

Install packages without network access:

```bash
hpm install --offline
```

**Requirements:**
- All packages must be in cache
- Lock file must exist with exact versions

**Use cases:**
- Air-gapped environments
- Faster CI/CD builds (with warm cache)
- Avoiding rate limits

## CI/CD Configuration

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Hemlock
      run: |
        # Install Hemlock (adjust based on your setup)
        curl -sSL https://hemlock.dev/install.sh | sh

    - name: Cache hpm packages
      uses: actions/cache@v3
      with:
        path: ~/.hpm/cache
        key: ${{ runner.os }}-hpm-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-hpm-

    - name: Install dependencies
      run: hpm install
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: Run tests
      run: hpm test
```

### GitLab CI

```yaml
stages:
  - build
  - test

variables:
  HPM_CACHE_DIR: $CI_PROJECT_DIR/.hpm-cache

cache:
  paths:
    - .hpm-cache/
  key: $CI_COMMIT_REF_SLUG

build:
  stage: build
  script:
    - hpm install
  artifacts:
    paths:
      - hem_modules/

test:
  stage: test
  script:
    - hpm test
```

### Docker

**Dockerfile:**

```dockerfile
FROM hemlock:latest

WORKDIR /app

# Copy package files first (for layer caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN hpm install

# Copy source code
COPY . .

# Run application
CMD ["hemlock", "src/main.hml"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - hpm-cache:/root/.hpm/cache

volumes:
  hpm-cache:
```

## Proxy Configuration

For environments behind a proxy, configure at the system level:

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1

hpm install
```

## Security Best Practices

### Token Security

1. **Never commit tokens** to version control
2. **Use environment variables** in CI/CD
3. **Restrict token scopes** to minimum required
4. **Rotate tokens** regularly
5. **Secure config file**:
   ```bash
   chmod 600 ~/.hpm/config.json
   ```

### Private Repositories

To access private packages:

1. Create token with `repo` scope
2. Configure authentication (env var or config file)
3. Ensure token has access to the repository

```bash
# Test access
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
hpm install yourorg/private-package
```

## Troubleshooting Configuration

### Verify Configuration

```bash
# Check if token is set
echo $GITHUB_TOKEN | head -c 10

# Check config file
cat ~/.hpm/config.json

# Check cache directory
ls -la ~/.hpm/cache/

# Test with verbose output
hpm install --verbose
```

### Common Issues

**"GitHub rate limit exceeded"**
- Set up authentication with `GITHUB_TOKEN`
- Wait for rate limit reset
- Use `--offline` if packages are cached

**"Permission denied" on cache**
```bash
# Fix cache permissions
chmod -R u+rw ~/.hpm/cache
```

**"Config file not found"**
```bash
# Create config directory
mkdir -p ~/.hpm
touch ~/.hpm/config.json
```

## See Also

- [Installation](installation.md) - Installing hpm
- [Troubleshooting](troubleshooting.md) - Common problems
- [Commands](commands.md) - Command reference
