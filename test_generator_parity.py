#!/usr/bin/env python3
"""
Test suite for verifying parity between Python and Hemlock documentation generators.

This script runs both generators and compares their outputs to ensure they produce
functionally equivalent documentation. It checks:
- HTML structure and content
- LLM text output
- Navigation structure
- Page content and ordering
- Language support

Usage:
    python test_generator_parity.py              # Test English only
    python test_generator_parity.py --lang all   # Test all languages
    python test_generator_parity.py --lang zh    # Test specific language
    python test_generator_parity.py --verbose    # Show detailed diff output
"""

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def colorize(text: str, color: str) -> str:
    """Apply color to text if stdout is a terminal."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text


class ParityTestResult:
    """Represents the result of a single parity test."""

    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details

    def __str__(self) -> str:
        status = colorize("PASS", Colors.GREEN) if self.passed else colorize("FAIL", Colors.RED)
        result = f"  [{status}] {self.name}"
        if self.message:
            result += f": {self.message}"
        return result


class GeneratorParityTester:
    """Tests parity between Python and Hemlock documentation generators."""

    def __init__(self, project_dir: Path, verbose: bool = False):
        self.project_dir = project_dir
        self.verbose = verbose
        self.temp_dir = None
        self.results: list[ParityTestResult] = []

    def setup(self) -> bool:
        """Set up temporary directories for test outputs."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="generator_parity_"))
        self.py_output_dir = self.temp_dir / "python"
        self.hml_output_dir = self.temp_dir / "hemlock"
        self.py_output_dir.mkdir()
        self.hml_output_dir.mkdir()
        return True

    def cleanup(self):
        """Clean up temporary directories."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def run_python_generator(self, lang: str = "en") -> bool:
        """Run the Python documentation generator."""
        try:
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "build_docs.py", "--lang", lang],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(colorize(f"Python generator failed: {result.stderr}", Colors.RED))
                return False

            # Copy output files to temp directory
            html_file = f"docs.html" if lang == "en" else f"docs-{lang}.html"
            llm_file = f"llms.txt" if lang == "en" else f"llms-{lang}.txt"

            src_html = self.project_dir / html_file
            src_llm = self.project_dir / llm_file

            if src_html.exists():
                shutil.copy(src_html, self.py_output_dir / html_file)
            if src_llm.exists():
                shutil.copy(src_llm, self.py_output_dir / llm_file)

            return True
        except subprocess.TimeoutExpired:
            print(colorize("Python generator timed out", Colors.RED))
            return False
        except Exception as e:
            print(colorize(f"Error running Python generator: {e}", Colors.RED))
            return False

    def run_hemlock_generator(self, lang: str = "en") -> bool:
        """Run the Hemlock documentation generator."""
        try:
            result = subprocess.run(
                ["hemlock", "build_docs.hml", "--lang", lang],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(colorize(f"Hemlock generator failed: {result.stderr}", Colors.RED))
                return False

            # Copy output files to temp directory
            html_file = f"docs.html" if lang == "en" else f"docs-{lang}.html"
            llm_file = f"llms.txt" if lang == "en" else f"llms-{lang}.txt"

            src_html = self.project_dir / html_file
            src_llm = self.project_dir / llm_file

            if src_html.exists():
                shutil.copy(src_html, self.hml_output_dir / html_file)
            if src_llm.exists():
                shutil.copy(src_llm, self.hml_output_dir / llm_file)

            return True
        except subprocess.TimeoutExpired:
            print(colorize("Hemlock generator timed out", Colors.RED))
            return False
        except FileNotFoundError:
            print(colorize("Hemlock interpreter not found. Make sure 'hemlock' is in PATH.", Colors.RED))
            return False
        except Exception as e:
            print(colorize(f"Error running Hemlock generator: {e}", Colors.RED))
            return False

    def extract_pages_json(self, html_content: str) -> Optional[dict]:
        """Extract the pages JSON data from HTML content."""
        # Look for the pages data in the script section
        match = re.search(r'const\s+pages\s*=\s*(\{[\s\S]*?\});?\s*\n\s*(?:const|let|var|function|//)', html_content)
        if match:
            try:
                # Clean up the JSON - handle trailing commas and other issues
                json_str = match.group(1)
                # Remove trailing commas before closing braces/brackets
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        return None

    def extract_nav_structure(self, html_content: str) -> list[tuple[str, str]]:
        """Extract navigation structure (section, title) pairs from HTML."""
        nav_items = []
        # Find all nav links
        pattern = r'<a[^>]*href="#([^"]+)"[^>]*>([^<]+)</a>'
        for match in re.finditer(pattern, html_content):
            page_id = match.group(1)
            title = match.group(2).strip()
            nav_items.append((page_id, title))
        return nav_items

    def extract_section_headers(self, html_content: str) -> list[str]:
        """Extract section headers from navigation."""
        pattern = r'<h3[^>]*class="[^"]*nav-section[^"]*"[^>]*>([^<]+)</h3>'
        return [match.group(1).strip() for match in re.finditer(pattern, html_content)]

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace for comparison."""
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Collapse multiple spaces to single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Remove trailing whitespace from lines
        text = '\n'.join(line.rstrip() for line in text.split('\n'))
        # Collapse multiple newlines to max 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def compare_html_structure(self, py_html: str, hml_html: str, lang: str) -> list[ParityTestResult]:
        """Compare structural elements of the HTML outputs."""
        results = []

        # Test 1: Check that both files are valid HTML
        py_has_html = '<html' in py_html and '</html>' in py_html
        hml_has_html = '<html' in hml_html and '</html>' in hml_html
        results.append(ParityTestResult(
            f"[{lang}] Valid HTML structure",
            py_has_html and hml_has_html,
            "" if (py_has_html and hml_has_html) else "Missing HTML tags"
        ))

        # Test 2: Compare section headers
        py_sections = self.extract_section_headers(py_html)
        hml_sections = self.extract_section_headers(hml_html)
        sections_match = py_sections == hml_sections
        results.append(ParityTestResult(
            f"[{lang}] Section headers match",
            sections_match,
            "" if sections_match else f"Python: {len(py_sections)}, Hemlock: {len(hml_sections)} sections"
        ))

        if not sections_match and self.verbose:
            py_set = set(py_sections)
            hml_set = set(hml_sections)
            if py_set - hml_set:
                print(f"    Sections only in Python: {py_set - hml_set}")
            if hml_set - py_set:
                print(f"    Sections only in Hemlock: {hml_set - py_set}")

        # Test 3: Compare navigation items
        py_nav = self.extract_nav_structure(py_html)
        hml_nav = self.extract_nav_structure(hml_html)
        nav_match = py_nav == hml_nav
        results.append(ParityTestResult(
            f"[{lang}] Navigation structure match",
            nav_match,
            "" if nav_match else f"Python: {len(py_nav)}, Hemlock: {len(hml_nav)} nav items"
        ))

        if not nav_match and self.verbose:
            py_ids = set(item[0] for item in py_nav)
            hml_ids = set(item[0] for item in hml_nav)
            if py_ids - hml_ids:
                print(f"    Nav IDs only in Python: {py_ids - hml_ids}")
            if hml_ids - py_ids:
                print(f"    Nav IDs only in Hemlock: {hml_ids - py_ids}")

        # Test 4: Compare pages data
        py_pages = self.extract_pages_json(py_html)
        hml_pages = self.extract_pages_json(hml_html)

        if py_pages and hml_pages:
            py_page_ids = set(py_pages.keys())
            hml_page_ids = set(hml_pages.keys())
            pages_match = py_page_ids == hml_page_ids
            results.append(ParityTestResult(
                f"[{lang}] Page IDs match",
                pages_match,
                "" if pages_match else f"Python: {len(py_page_ids)}, Hemlock: {len(hml_page_ids)} pages"
            ))

            if not pages_match and self.verbose:
                if py_page_ids - hml_page_ids:
                    print(f"    Pages only in Python: {py_page_ids - hml_page_ids}")
                if hml_page_ids - py_page_ids:
                    print(f"    Pages only in Hemlock: {hml_page_ids - py_page_ids}")
        else:
            results.append(ParityTestResult(
                f"[{lang}] Page IDs match",
                False,
                "Could not extract pages JSON from one or both outputs"
            ))

        # Test 5: Check essential HTML elements
        essential_elements = [
            ('<!DOCTYPE html>', 'DOCTYPE declaration'),
            ('<meta charset', 'charset meta tag'),
            ('<title>', 'title tag'),
            ('class="sidebar"', 'sidebar element'),
            ('class="main-content"', 'main content element'),
            ('id="dark-mode-toggle"', 'dark mode toggle'),
            ('id="search-input"', 'search input'),
        ]

        for element, description in essential_elements:
            py_has = element in py_html
            hml_has = element in hml_html
            results.append(ParityTestResult(
                f"[{lang}] Has {description}",
                py_has and hml_has,
                "" if (py_has and hml_has) else f"Python: {py_has}, Hemlock: {hml_has}"
            ))

        return results

    def compare_llm_output(self, py_llm: str, hml_llm: str, lang: str) -> list[ParityTestResult]:
        """Compare LLM text outputs."""
        results = []

        # Normalize both outputs
        py_normalized = self.normalize_whitespace(py_llm)
        hml_normalized = self.normalize_whitespace(hml_llm)

        # Test 1: Check overall length similarity (within 5%)
        py_len = len(py_normalized)
        hml_len = len(hml_normalized)
        len_diff = abs(py_len - hml_len) / max(py_len, hml_len, 1)
        length_similar = len_diff < 0.05
        results.append(ParityTestResult(
            f"[{lang}] LLM output length similar",
            length_similar,
            f"Python: {py_len}, Hemlock: {hml_len} chars ({len_diff*100:.1f}% diff)"
        ))

        # Test 2: Check for header
        py_has_header = 'Hemlock' in py_llm[:500]
        hml_has_header = 'Hemlock' in hml_llm[:500]
        results.append(ParityTestResult(
            f"[{lang}] LLM output has header",
            py_has_header and hml_has_header,
            "" if (py_has_header and hml_has_header) else f"Python: {py_has_header}, Hemlock: {hml_has_header}"
        ))

        # Test 3: Extract and compare section markers
        py_sections = re.findall(r'^#{1,3}\s+(.+)$', py_llm, re.MULTILINE)
        hml_sections = re.findall(r'^#{1,3}\s+(.+)$', hml_llm, re.MULTILINE)

        # Compare first 20 sections
        py_first = py_sections[:20]
        hml_first = hml_sections[:20]
        sections_match = py_first == hml_first
        results.append(ParityTestResult(
            f"[{lang}] LLM section headers match",
            sections_match,
            "" if sections_match else f"First mismatch in section headers"
        ))

        if not sections_match and self.verbose:
            for i, (p, h) in enumerate(zip(py_first, hml_first)):
                if p != h:
                    print(f"    Section {i} differs: Python='{p}', Hemlock='{h}'")
                    break

        # Test 4: Check exact content match (normalized)
        exact_match = py_normalized == hml_normalized
        results.append(ParityTestResult(
            f"[{lang}] LLM output exact match",
            exact_match,
            "" if exact_match else "Normalized content differs"
        ))

        if not exact_match and self.verbose:
            # Show first difference
            py_lines = py_normalized.split('\n')
            hml_lines = hml_normalized.split('\n')
            for i, (p, h) in enumerate(zip(py_lines, hml_lines)):
                if p != h:
                    print(f"    First difference at line {i+1}:")
                    print(f"      Python:  {p[:80]}...")
                    print(f"      Hemlock: {h[:80]}...")
                    break

        return results

    def compare_file_sizes(self, py_file: Path, hml_file: Path, file_type: str, lang: str) -> ParityTestResult:
        """Compare file sizes between outputs."""
        if not py_file.exists() or not hml_file.exists():
            return ParityTestResult(
                f"[{lang}] {file_type} files exist",
                False,
                f"Python: {py_file.exists()}, Hemlock: {hml_file.exists()}"
            )

        py_size = py_file.stat().st_size
        hml_size = hml_file.stat().st_size
        size_diff = abs(py_size - hml_size) / max(py_size, hml_size, 1)

        # Allow up to 5% difference in file size
        similar = size_diff < 0.05
        return ParityTestResult(
            f"[{lang}] {file_type} file size similar",
            similar,
            f"Python: {py_size} bytes, Hemlock: {hml_size} bytes ({size_diff*100:.1f}% diff)"
        )

    def test_language(self, lang: str) -> list[ParityTestResult]:
        """Run all parity tests for a specific language."""
        results = []

        print(colorize(f"\nTesting language: {lang}", Colors.BLUE + Colors.BOLD))

        # Run both generators
        print("  Running Python generator...")
        py_success = self.run_python_generator(lang)
        if not py_success:
            results.append(ParityTestResult(f"[{lang}] Python generator", False, "Failed to run"))
            return results
        results.append(ParityTestResult(f"[{lang}] Python generator", True, "Completed"))

        print("  Running Hemlock generator...")
        hml_success = self.run_hemlock_generator(lang)
        if not hml_success:
            results.append(ParityTestResult(f"[{lang}] Hemlock generator", False, "Failed to run"))
            return results
        results.append(ParityTestResult(f"[{lang}] Hemlock generator", True, "Completed"))

        # Get file paths
        html_file = f"docs.html" if lang == "en" else f"docs-{lang}.html"
        llm_file = f"llms.txt" if lang == "en" else f"llms-{lang}.txt"

        py_html_path = self.py_output_dir / html_file
        hml_html_path = self.hml_output_dir / html_file
        py_llm_path = self.py_output_dir / llm_file
        hml_llm_path = self.hml_output_dir / llm_file

        # Compare file sizes
        results.append(self.compare_file_sizes(py_html_path, hml_html_path, "HTML", lang))
        results.append(self.compare_file_sizes(py_llm_path, hml_llm_path, "LLM", lang))

        # Compare HTML structure
        if py_html_path.exists() and hml_html_path.exists():
            py_html = py_html_path.read_text()
            hml_html = hml_html_path.read_text()
            results.extend(self.compare_html_structure(py_html, hml_html, lang))

        # Compare LLM output
        if py_llm_path.exists() and hml_llm_path.exists():
            py_llm = py_llm_path.read_text()
            hml_llm = hml_llm_path.read_text()
            results.extend(self.compare_llm_output(py_llm, hml_llm, lang))

        return results

    def run_tests(self, languages: list[str]) -> bool:
        """Run all parity tests for the specified languages."""
        print(colorize("\n" + "=" * 60, Colors.BOLD))
        print(colorize("Generator Parity Test Suite", Colors.BOLD))
        print(colorize("=" * 60, Colors.BOLD))

        if not self.setup():
            print(colorize("Failed to set up test environment", Colors.RED))
            return False

        try:
            for lang in languages:
                lang_results = self.test_language(lang)
                self.results.extend(lang_results)

                # Print results for this language
                for result in lang_results:
                    print(result)
        finally:
            self.cleanup()

        return self.print_summary()

    def print_summary(self) -> bool:
        """Print test summary and return True if all tests passed."""
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(colorize("\n" + "=" * 60, Colors.BOLD))
        print(colorize("Test Summary", Colors.BOLD))
        print(colorize("=" * 60, Colors.BOLD))
        print(f"  Total:  {total}")
        print(f"  Passed: {colorize(str(passed), Colors.GREEN)}")
        print(f"  Failed: {colorize(str(failed), Colors.RED if failed else Colors.GREEN)}")

        if failed > 0:
            print(colorize("\nFailed tests:", Colors.RED))
            for result in self.results:
                if not result.passed:
                    print(f"  - {result.name}: {result.message}")

        success = failed == 0
        if success:
            print(colorize("\nAll tests passed!", Colors.GREEN + Colors.BOLD))
        else:
            print(colorize(f"\n{failed} test(s) failed.", Colors.RED + Colors.BOLD))

        return success


def main():
    parser = argparse.ArgumentParser(
        description="Test parity between Python and Hemlock documentation generators"
    )
    parser.add_argument(
        "--lang",
        default="en",
        help="Language to test (en, zh, de, es, fr, ja, pt, or 'all')"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed diff output for failures"
    )

    args = parser.parse_args()

    # Determine which languages to test
    all_languages = ["en", "zh", "de", "es", "fr", "ja", "pt"]
    if args.lang == "all":
        languages = all_languages
    elif args.lang in all_languages:
        languages = [args.lang]
    else:
        print(f"Unknown language: {args.lang}")
        print(f"Supported languages: {', '.join(all_languages)}, or 'all'")
        sys.exit(1)

    # Run tests
    project_dir = Path(__file__).parent
    tester = GeneratorParityTester(project_dir, verbose=args.verbose)
    success = tester.run_tests(languages)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
