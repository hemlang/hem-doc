# Installation

This guide covers how to install hpm on your system.

## Quick Install (Recommended)

Install the latest release with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh
```

This automatically:
- Detects your operating system (Linux, macOS)
- Detects your architecture (x86_64, arm64)
- Downloads the appropriate pre-built binary
- Installs to `/usr/local/bin` (or uses sudo if needed)

### Install Options

```bash
# Install to a custom location (no sudo required)
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local

# Install a specific version
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --version 1.0.5

# Combine options
curl -fsSL https://raw.githubusercontent.com/hemlang/hpm/main/install.sh | sh -s -- --prefix ~/.local --version 1.0.5
```

### Supported Platforms

| Platform | Architecture | Status |
|----------|--------------|--------|
| Linux    | x86_64       | ✓ Supported |
| macOS    | x86_64       | ✓ Supported |
| macOS    | arm64 (M1/M2/M3) | ✓ Supported |
| Linux    | arm64        | Build from source |

## Building from Source

If you prefer to build from source or need a platform not covered by pre-built binaries, follow these instructions.

### Prerequisites

hpm requires [Hemlock](https://github.com/hemlang/hemlock) to be installed first. Follow the Hemlock installation instructions before proceeding.

Verify Hemlock is installed:

```bash
hemlock --version
```

## Installation Methods

### Method 1: Make Install

Build from source and install.

```bash
# Clone the repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Install to /usr/local/bin (requires sudo)
sudo make install
```

After installation, verify it works:

```bash
hpm --version
```

### Method 2: Custom Location

Install to a custom directory (no sudo required):

```bash
# Clone the repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Install to ~/.local/bin
make install PREFIX=$HOME/.local

# Or any custom location
make install PREFIX=/opt/hemlock
```

Make sure your custom bin directory is in your PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### Method 3: Run Without Installing

You can run hpm directly without installing:

```bash
# Clone the repository
git clone https://github.com/hemlang/hpm.git
cd hpm

# Create local wrapper script
make

# Run from the hpm directory
./hpm --help

# Or run via hemlock directly
hemlock src/main.hml --help
```

### Method 4: Manual Installation

Create your own wrapper script:

```bash
# Clone to a permanent location
git clone https://github.com/hemlang/hpm.git ~/.hpm-source

# Create wrapper script
cat > ~/.local/bin/hpm << 'EOF'
#!/bin/sh
exec hemlock "$HOME/.hpm-source/src/main.hml" "$@"
EOF

chmod +x ~/.local/bin/hpm
```

## Installation Variables

The Makefile supports these variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PREFIX` | `/usr/local` | Installation prefix |
| `BINDIR` | `$(PREFIX)/bin` | Binary directory |
| `HEMLOCK` | `hemlock` | Path to hemlock interpreter |

Example with custom variables:

```bash
make install PREFIX=/opt/hemlock BINDIR=/opt/hemlock/bin HEMLOCK=/usr/bin/hemlock
```

## How It Works

The installer creates a shell wrapper script that invokes the Hemlock interpreter with the hpm source code:

```bash
#!/bin/sh
exec hemlock "/path/to/hpm/src/main.hml" "$@"
```

This approach:
- Requires no compilation
- Always runs the latest source code
- Works reliably across all platforms

## Updating hpm

To update hpm to the latest version:

```bash
cd /path/to/hpm
git pull origin main

# Re-install if the path changed
sudo make install
```

## Uninstalling

Remove hpm from your system:

```bash
cd /path/to/hpm
sudo make uninstall
```

Or manually remove:

```bash
sudo rm /usr/local/bin/hpm
```

## Verifying Installation

After installation, verify everything works:

```bash
# Check version
hpm --version

# View help
hpm --help

# Test initialization (in an empty directory)
mkdir test-project && cd test-project
hpm init --yes
cat package.json
```

## Troubleshooting

### "hemlock: command not found"

Hemlock is not installed or not in your PATH. Install Hemlock first:

```bash
# Check if hemlock exists
which hemlock

# If not found, install Hemlock from https://github.com/hemlang/hemlock
```

### "Permission denied"

Use sudo for system-wide installation, or install to a user directory:

```bash
# Option 1: Use sudo
sudo make install

# Option 2: Install to user directory
make install PREFIX=$HOME/.local
```

### "hpm: command not found" after installation

Your PATH may not include the installation directory:

```bash
# Check where hpm was installed
ls -la /usr/local/bin/hpm

# Add to PATH if using custom location
export PATH="$HOME/.local/bin:$PATH"
```

## Platform-Specific Notes

### Linux

Standard installation works on all Linux distributions. Some distributions may require:

```bash
# Debian/Ubuntu: Ensure build essentials
sudo apt-get install build-essential git

# Fedora/RHEL
sudo dnf install make git
```

### macOS

Standard installation works. If using Homebrew:

```bash
# Ensure Xcode command line tools
xcode-select --install
```

### Windows (WSL)

hpm works in Windows Subsystem for Linux:

```bash
# In WSL terminal
git clone https://github.com/hemlang/hpm.git
cd hpm
make install PREFIX=$HOME/.local
```

## Next Steps

After installation:

1. [Quick Start](quick-start.md) - Create your first project
2. [Command Reference](commands.md) - Learn all commands
3. [Configuration](configuration.md) - Configure hpm
