# Versioning

Complete guide to semantic versioning in hpm.

## Semantic Versioning

hpm uses [Semantic Versioning 2.0.0](https://semver.org/) (semver) for package versions.

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Examples:**
```
1.0.0           # Release version
2.1.3           # Release version
1.0.0-alpha     # Pre-release
1.0.0-beta.1    # Pre-release with number
1.0.0-rc.1      # Release candidate
1.0.0+20231201  # With build metadata
1.0.0-beta+exp  # Pre-release with build metadata
```

### Version Components

| Component | Description | Example |
|-----------|-------------|---------|
| MAJOR | Breaking changes | `1.0.0` → `2.0.0` |
| MINOR | New features (backward compatible) | `1.0.0` → `1.1.0` |
| PATCH | Bug fixes (backward compatible) | `1.0.0` → `1.0.1` |
| PRERELEASE | Pre-release identifier | `1.0.0-alpha` |
| BUILD | Build metadata (ignored in comparison) | `1.0.0+build123` |

### When to Increment

| Change Type | Increment | Example |
|-------------|-----------|---------|
| Breaking API change | MAJOR | Removing a function |
| Renaming public function | MAJOR | `parse()` → `decode()` |
| Changing function signature | MAJOR | Adding required parameter |
| Adding new function | MINOR | Adding `validate()` |
| Adding optional parameter | MINOR | New optional `options` arg |
| Bug fix | PATCH | Fix null pointer |
| Performance improvement | PATCH | Faster algorithm |
| Internal refactor | PATCH | No API change |

## Version Constraints

### Constraint Syntax

| Syntax | Meaning | Resolves to |
|--------|---------|-------------|
| `1.2.3` | Exact version | 1.2.3 only |
| `^1.2.3` | Caret (compatible) | ≥1.2.3 and <2.0.0 |
| `~1.2.3` | Tilde (patch updates) | ≥1.2.3 and <1.3.0 |
| `>=1.0.0` | At least | 1.0.0 or higher |
| `>1.0.0` | Greater than | Higher than 1.0.0 |
| `<2.0.0` | Less than | Lower than 2.0.0 |
| `<=2.0.0` | At most | 2.0.0 or lower |
| `>=1.0.0 <2.0.0` | Range | Between 1.0.0 and 2.0.0 |
| `*` | Any | Any version |

### Caret Ranges (^)

The caret (`^`) allows changes that don't modify the leftmost non-zero digit:

```
^1.2.3  →  >=1.2.3 <2.0.0   # Allows 1.x.x
^0.2.3  →  >=0.2.3 <0.3.0   # Allows 0.2.x
^0.0.3  →  >=0.0.3 <0.0.4   # Allows 0.0.3 only
```

**Use when:** You want compatible updates within a major version.

**Most common constraint** - recommended for most dependencies.

### Tilde Ranges (~)

The tilde (`~`) allows only patch-level changes:

```
~1.2.3  →  >=1.2.3 <1.3.0   # Allows 1.2.x
~1.2    →  >=1.2.0 <1.3.0   # Allows 1.2.x
~1      →  >=1.0.0 <2.0.0   # Allows 1.x.x
```

**Use when:** You want only bug fixes, no new features.

### Comparison Ranges

Combine comparison operators for precise control:

```json
{
  "dependencies": {
    "owner/pkg": ">=1.0.0 <2.0.0",
    "owner/other": ">1.5.0 <=2.1.0"
  }
}
```

### Any Version (*)

Matches any version:

```json
{
  "dependencies": {
    "owner/pkg": "*"
  }
}
```

**Warning:** Not recommended for production. Will always get the latest version.

## Pre-release Versions

### Pre-release Identifiers

Pre-releases have lower precedence than releases:

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0-rc.1 < 1.0.0
```

### Common Pre-release Tags

| Tag | Meaning | Stage |
|-----|---------|-------|
| `alpha` | Early development | Very unstable |
| `beta` | Feature complete | Testing |
| `rc` | Release candidate | Final testing |
| `dev` | Development snapshot | Unstable |

### Pre-release in Constraints

Constraints don't match pre-releases by default:

```
^1.0.0    # Does NOT match 1.1.0-beta
>=1.0.0   # Does NOT match 2.0.0-alpha
```

To include pre-releases, reference them explicitly:

```
>=1.0.0-alpha <2.0.0   # Includes all 1.x pre-releases
```

## Version Comparison

### Comparison Rules

1. Compare MAJOR, MINOR, PATCH numerically
2. Release > pre-release with same version
3. Pre-releases compared alphanumerically
4. Build metadata is ignored

### Examples

```
1.0.0 < 1.0.1 < 1.1.0 < 2.0.0

1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-beta < 1.0.0

1.0.0 = 1.0.0+build123  # Build metadata ignored
```

### Sorting

Versions sort ascending:

```
1.0.0
1.0.1
1.1.0
1.1.1
2.0.0-alpha
2.0.0-beta
2.0.0
```

## Version Resolution

### Resolution Algorithm

When multiple packages require the same dependency:

1. Collect all constraints
2. Find intersection of all ranges
3. Select highest version in intersection
4. Error if no version satisfies all

### Example Resolution

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@~1.2.0  (>=1.2.0 <1.3.0)

Intersection: >=1.2.0 <1.3.0
Available: [1.0.0, 1.1.0, 1.2.0, 1.2.1, 1.2.5, 1.3.0]
Resolved: 1.2.5 (highest in intersection)
```

### Conflict Detection

Conflict occurs when no version satisfies all constraints:

```
package-a requires hemlang/json@^1.0.0  (>=1.0.0 <2.0.0)
package-b requires hemlang/json@^2.0.0  (>=2.0.0 <3.0.0)

Intersection: (empty)
Result: CONFLICT - no version satisfies both
```

## Best Practices

### For Package Consumers

1. **Use caret ranges** for most dependencies:
   ```json
   "hemlang/json": "^1.2.0"
   ```

2. **Use tilde ranges** for critical dependencies:
   ```json
   "critical/lib": "~1.2.0"
   ```

3. **Pin versions** only when necessary:
   ```json
   "unstable/pkg": "1.2.3"
   ```

4. **Commit your lock file** for reproducible builds

5. **Update regularly** to get security fixes:
   ```bash
   hpm update
   hpm outdated
   ```

### For Package Authors

1. **Start at 0.1.0** for initial development:
   - API may change frequently
   - Users expect instability

2. **Go to 1.0.0** when API is stable:
   - Public commitment to stability
   - Breaking changes require major bump

3. **Follow semver strictly**:
   - Breaking change = MAJOR
   - New feature = MINOR
   - Bug fix = PATCH

4. **Use pre-releases** for testing:
   ```bash
   git tag v2.0.0-beta.1
   git push --tags
   ```

5. **Document breaking changes** in CHANGELOG

## Publishing Versions

### Creating Releases

```bash
# Update version in package.json
# Edit package.json: "version": "1.1.0"

# Commit version change
git add package.json
git commit -m "Bump version to 1.1.0"

# Create and push tag
git tag v1.1.0
git push origin main --tags
```

### Tag Format

Tags **must** start with `v`:

```
v1.0.0      ✓ Correct
v1.0.0-beta ✓ Correct
1.0.0       ✗ Won't be recognized
```

### Release Workflow

```bash
# 1. Ensure tests pass
hpm test

# 2. Update version in package.json
# 3. Update CHANGELOG.md
# 4. Commit changes
git add -A
git commit -m "Release v1.2.0"

# 5. Create tag
git tag v1.2.0

# 6. Push everything
git push origin main --tags
```

## Checking Versions

### List Installed Versions

```bash
hpm list
```

### Check for Updates

```bash
hpm outdated
```

Output:
```
Package         Current  Wanted  Latest
hemlang/json    1.0.0    1.0.5   1.2.0
hemlang/sprout  2.0.0    2.0.3   2.1.0
```

- **Current**: Installed version
- **Wanted**: Highest matching constraint
- **Latest**: Latest available

### Update Packages

```bash
# Update all
hpm update

# Update specific package
hpm update hemlang/json
```

## See Also

- [Creating Packages](creating-packages.md) - Publishing guide
- [Package Specification](package-spec.md) - package.json format
- [Commands](commands.md) - CLI reference
