# Hemlock Documentation
# https://github.com/hemlang/hem-doc

HEMLOCK ?= hemlock
HPM ?= hpm
PYTHON ?= python3
VERSION := 1.0.5

.PHONY: all deps docs docs-py server package dist clean help test test-parity

all: docs

# Install dependencies via hpm
deps:
	@echo "Installing dependencies..."
	@$(HPM) install
	@echo "Done"

# Generate documentation HTML and LLM-friendly text using Hemlock (preferred)
docs:
	@echo "Generating docs.html and llms.txt..."
	@$(HEMLOCK) build_docs.hml
	@echo "Done: docs.html ($(shell wc -c < docs.html | tr -d ' ') bytes)"
	@echo "Done: llms.txt ($(shell wc -c < llms.txt | tr -d ' ') bytes)"

# Generate documentation HTML and LLM-friendly text using Python (fallback)
docs-py:
	@echo "Generating docs.html and llms.txt (Python fallback)..."
	@$(PYTHON) build_docs.py
	@echo "Done: docs.html ($(shell wc -c < docs.html | tr -d ' ') bytes)"
	@echo "Done: llms.txt ($(shell wc -c < llms.txt | tr -d ' ') bytes)"

# Run parity tests between Python and Hemlock generators
test: test-parity

test-parity:
	@echo "Running generator parity tests..."
	@$(PYTHON) test_generator_parity.py

# Run parity tests for all languages
test-parity-all:
	@echo "Running generator parity tests for all languages..."
	@$(PYTHON) test_generator_parity.py --lang all

# Run parity tests with verbose output
test-parity-verbose:
	@echo "Running generator parity tests (verbose)..."
	@$(PYTHON) test_generator_parity.py --verbose

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
	@zip -j hem-doc-$(VERSION).zip hem-doc-server docs.html llms.txt
	@ls -l hem-doc-$(VERSION).zip | awk '{print "Done: " $$9 " (" $$5 " bytes)"}'

# Run the documentation server locally
run: server
	@echo "Starting documentation server on http://localhost:5169"
	@./hem-doc-server

# Clean build artifacts
clean:
	@rm -f hem-doc-server *.hmlc *.hmlb *.zip llms.txt
	@echo "Cleaned build artifacts"

# Show help
help:
	@echo "Hemlock Documentation $(VERSION)"
	@echo ""
	@echo "Usage:"
	@echo "  make deps              - Install dependencies via hpm"
	@echo "  make docs              - Generate docs.html and llms.txt using Hemlock"
	@echo "  make docs-py           - Generate docs.html and llms.txt using Python (fallback)"
	@echo "  make test              - Run generator parity tests (English only)"
	@echo "  make test-parity       - Run generator parity tests (English only)"
	@echo "  make test-parity-all   - Run generator parity tests for all languages"
	@echo "  make test-parity-verbose - Run parity tests with verbose output"
	@echo "  make server            - Package the documentation server executable"
	@echo "  make dist              - Create distribution zip (server + docs + llms.txt)"
	@echo "  make run               - Run the documentation server locally"
	@echo "  make clean             - Remove build artifacts"
	@echo "  make help              - Show this help message"
	@echo ""
	@echo "Output files:"
	@echo "  docs.html    - Interactive HTML documentation"
	@echo "  llms.txt     - LLM-friendly plain text documentation"
	@echo ""
	@echo "Environment variables:"
	@echo "  HEMLOCK      - Path to hemlock interpreter (default: hemlock)"
	@echo "  HPM          - Path to hpm package manager (default: hpm)"
	@echo "  PYTHON       - Path to python3 (default: python3)"
