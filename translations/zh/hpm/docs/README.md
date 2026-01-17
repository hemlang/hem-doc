# hpm Documentation

Welcome to the hpm (Hemlock Package Manager) documentation. hpm is the official package manager for the [Hemlock](https://github.com/hemlang/hemlock) programming language.

## Overview

hpm uses GitHub as its package registry, where packages are identified by their GitHub repository path (e.g., `hemlang/sprout`). This means:

- **No central registry** - packages live in GitHub repositories
- **Version tags** - releases are Git tags (e.g., `v1.0.0`)
- **Publishing is just git** - push a tag to publish a new version

## Documentation

### Getting Started

- [Installation](installation.md) - How to install hpm
- [Quick Start](quick-start.md) - Get up and running in 5 minutes
- [Project Setup](project-setup.md) - Setting up a new Hemlock project

### User Guide

- [Command Reference](commands.md) - Complete reference for all hpm commands
- [Configuration](configuration.md) - Configuration files and environment variables
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

### Package Development

- [Creating Packages](creating-packages.md) - How to create and publish packages
- [Package Specification](package-spec.md) - The package.json format
- [Versioning](versioning.md) - Semantic versioning and version constraints

### Reference

- [Architecture](architecture.md) - Internal architecture and design
- [Exit Codes](exit-codes.md) - CLI exit codes reference

## Quick Reference

### Basic Commands

```bash
hpm init                              # Create a new package.json
hpm install                           # Install all dependencies
hpm install owner/repo                # Add and install a package
hpm install owner/repo@^1.0.0        # Install with version constraint
hpm uninstall owner/repo              # Remove a package
hpm update                            # Update all packages
hpm list                              # Show installed packages
hpm run <script>                      # Run a package script
```

### Package Identification

Packages use GitHub `owner/repo` format:

```
hemlang/sprout          # Web framework
hemlang/json            # JSON utilities
alice/http-client       # HTTP client library
```

### Version Constraints

| Syntax | Meaning |
|--------|---------|
| `1.0.0` | Exact version |
| `^1.2.3` | Compatible (>=1.2.3 <2.0.0) |
| `~1.2.3` | Patch updates (>=1.2.3 <1.3.0) |
| `>=1.0.0` | At least 1.0.0 |
| `*` | Any version |

## Getting Help

- Use `hpm --help` for command-line help
- Use `hpm <command> --help` for command-specific help
- Report issues at [github.com/hemlang/hpm/issues](https://github.com/hemlang/hpm/issues)

## License

hpm is released under the MIT License.
