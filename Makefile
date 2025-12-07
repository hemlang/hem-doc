# Hemlock Documentation
# https://github.com/hemlang/hem-doc

HEMLOCK ?= hemlock
HPM ?= hpm
PYTHON ?= python3
VERSION := 1.0.4

.PHONY: all deps docs server package dist clean help

all: docs

# Install dependencies via hpm
deps:
	@echo "Installing dependencies..."
	@$(HPM) install
	@echo "Done"

# Generate documentation HTML from hemlock source
docs:
	@echo "Generating docs.html..."
	@$(PYTHON) build_docs.py
	@echo "Done: docs.html ($(shell wc -c < docs.html | tr -d ' ') bytes)"

# Package the documentation server
server: docs
	@echo "Packaging documentation server..."
	@$(HEMLOCK) --package serve.hml -o hem-doc-server
	@chmod +x hem-doc-server
	@echo "Done: hem-doc-server ($(shell wc -c < hem-doc-server | tr -d ' ') bytes)"

# Create distribution zip with server + docs
dist: server
	@echo "Creating distribution package..."
	@rm -f hem-doc-$(VERSION).zip
	@zip -j hem-doc-$(VERSION).zip hem-doc-server docs.html
	@ls -l hem-doc-$(VERSION).zip | awk '{print "Done: " $$9 " (" $$5 " bytes)"}'

# Run the documentation server locally
run: server
	@echo "Starting documentation server on http://localhost:3000"
	@./hem-doc-server

# Clean build artifacts
clean:
	@rm -f hem-doc-server *.hmlc *.hmlb *.zip
	@echo "Cleaned build artifacts"

# Show help
help:
	@echo "Hemlock Documentation $(VERSION)"
	@echo ""
	@echo "Usage:"
	@echo "  make deps    - Install dependencies via hpm"
	@echo "  make docs    - Generate docs.html from hemlock source"
	@echo "  make server  - Package the documentation server executable"
	@echo "  make dist    - Create distribution zip (server + docs.html)"
	@echo "  make run     - Run the documentation server locally"
	@echo "  make clean   - Remove build artifacts"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "Environment variables:"
	@echo "  HEMLOCK      - Path to hemlock interpreter (default: hemlock)"
	@echo "  HPM          - Path to hpm package manager (default: hpm)"
	@echo "  PYTHON       - Path to python3 (default: python3)"
