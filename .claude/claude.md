# hem-doc Project Notes

## Architecture

This project generates documentation for the Hemlock programming language as single-file HTML pages. There are two equivalent build scripts that should produce matching output:

- `build_docs.py` — Python build script (fallback, used in CI)
- `build_docs.hml` — Hemlock build script (preferred, used by `make docs`)

## Parallel Editing Rule

**When making changes to the HTML/CSS/JS template in one build script, the same changes MUST be applied to the other.** The two files contain nearly identical HTML generation logic — the Python version uses f-strings with `{{` escapes while the HML version uses string concatenation with escaped quotes.

Key structural sections to keep in sync:
- CSS styles (`:root` variables, component styles, responsive breakpoints)
- HTML template (header, sidebar nav, main content area, skip links)
- JavaScript (markdown parser, search, theme toggle, page navigation)
- Navigation generation (`generate_nav_html` / nav_items loop)
- Table rendering (`flushTable` function)
- Code block rendering (copy button, ARIA labels)

## CI Parity Check

The `.github/workflows/check-build-parity.yml` workflow runs on PRs that touch either build script. It builds with both Python and Hemlock (when available) and compares:
- File sizes (warns if >10% difference)
- ARIA attribute counts
- Role attribute counts
- Critical accessibility elements (skip link, semantic header, roles, live regions)
- llms.txt output

## Accessibility Standards

Both build scripts implement WCAG 2.1 AA accessibility features:
- Skip-to-content link for keyboard navigation
- Semantic `<header>` with `role="banner"`
- `role="search"` on search container with `aria-autocomplete`, `aria-controls`, `aria-expanded`
- `aria-live="polite"` region for search result announcements
- `role="option"` and `aria-selected` on search results
- `aria-activedescendant` for keyboard nav in search
- `aria-label` on all interactive elements (buttons, inputs, selects)
- `aria-hidden="true"` on decorative SVGs
- `aria-current="page"` on active nav link
- Focus management: content receives focus on page change
- `focus-visible` outlines on all interactive elements
- Semantic table structure: `<thead>`, `<tbody>`, `scope="col"` on `<th>`
- Responsive table wrappers with `role="region"` and `tabindex="0"`
- `.sr-only` utility class for screen-reader-only content
- Nav sections use `role="group"` with `aria-label`

## Build Commands

```bash
make docs          # Build with Hemlock (preferred)
make docs-py       # Build with Python (fallback)
make docs-all      # All 9 languages with Hemlock
make docs-py-all   # All 9 languages with Python
```
