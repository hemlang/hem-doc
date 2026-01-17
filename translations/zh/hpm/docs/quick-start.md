# Quick Start

Get up and running with hpm in 5 minutes.

## Install hpm

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

For more installation options, see the [Installation Guide](installation.md).

## Create a New Project

Start by creating a new directory and initializing a package:

```bash
mkdir my-project
cd my-project
hpm init
```

You'll be prompted for project details:

```
Package name (owner/repo): myname/my-project
Version (1.0.0):
Description: My awesome Hemlock project
Author: Your Name <you@example.com>
License (MIT):
Main file (src/index.hml):

Created package.json
```

Use `--yes` to accept all defaults:

```bash
hpm init --yes
```

## Project Structure

Create the basic project structure:

```
my-project/
├── package.json        # Project manifest
├── src/
│   └── index.hml      # Main entry point
└── test/
    └── test.hml       # Tests
```

Create your main file:

```bash
mkdir -p src test
```

**src/index.hml:**
```hemlock
// Main entry point
export fn greet(name: string): string {
    return "Hello, " + name + "!";
}

export fn main() {
    print(greet("World"));
}
```

## Install Dependencies

Search for packages on GitHub (packages use `owner/repo` format):

```bash
# Install a package
hpm install hemlang/sprout

# Install with version constraint
hpm install hemlang/json@^1.0.0

# Install as dev dependency
hpm install hemlang/test-utils --dev
```

After installation, your project structure includes `hem_modules/`:

```
my-project/
├── package.json
├── package-lock.json   # Lock file (auto-generated)
├── hem_modules/        # Installed packages
│   └── hemlang/
│       └── sprout/
├── src/
│   └── index.hml
└── test/
    └── test.hml
```

## Use Installed Packages

Import packages using their GitHub path:

```hemlock
// Import from installed package
import { app, router } from "hemlang/sprout";
import { parse, stringify } from "hemlang/json";

// Import from subpath
import { middleware } from "hemlang/sprout/middleware";

// Standard library (built-in)
import { HashMap } from "@stdlib/collections";
import { readFile } from "@stdlib/fs";
```

## Add Scripts

Add scripts to your `package.json`:

```json
{
  "name": "myname/my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "hemlock src/index.hml",
    "test": "hemlock test/test.hml",
    "build": "hemlock --bundle src/index.hml -o dist/app.hmlc"
  }
}
```

Run scripts with `hpm run`:

```bash
hpm run start
hpm run build

# Shorthand for test
hpm test
```

## Common Workflows

### Installing All Dependencies

When you clone a project with a `package.json`:

```bash
git clone https://github.com/someone/project.git
cd project
hpm install
```

### Updating Dependencies

Update all packages to latest versions within constraints:

```bash
hpm update
```

Update a specific package:

```bash
hpm update hemlang/sprout
```

### Viewing Installed Packages

List all installed packages:

```bash
hpm list
```

Output shows the dependency tree:

```
my-project@1.0.0
├── hemlang/sprout@2.1.0
│   └── hemlang/router@1.5.0
└── hemlang/json@1.2.3
```

### Checking for Updates

See which packages have newer versions:

```bash
hpm outdated
```

### Removing a Package

```bash
hpm uninstall hemlang/sprout
```

## Example: Web Application

Here's a complete example using a web framework:

**package.json:**
```json
{
  "name": "myname/my-web-app",
  "version": "1.0.0",
  "description": "A web application",
  "main": "src/index.hml",
  "dependencies": {
    "hemlang/sprout": "^2.0.0"
  },
  "scripts": {
    "start": "hemlock src/index.hml",
    "dev": "hemlock --watch src/index.hml"
  }
}
```

**src/index.hml:**
```hemlock
import { App, Router } from "hemlang/sprout";

fn main() {
    let app = App.new();
    let router = Router.new();

    router.get("/", fn(req, res) {
        res.send("Hello, World!");
    });

    router.get("/api/status", fn(req, res) {
        res.json({ status: "ok" });
    });

    app.use(router);
    app.listen(3000);

    print("Server running on http://localhost:3000");
}
```

Run the application:

```bash
hpm install
hpm run start
```

## Next Steps

- [Command Reference](commands.md) - Learn all hpm commands
- [Creating Packages](creating-packages.md) - Publish your own packages
- [Configuration](configuration.md) - Configure hpm and GitHub tokens
- [Project Setup](project-setup.md) - Detailed project configuration
