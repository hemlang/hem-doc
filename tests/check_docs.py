#!/usr/bin/env python3
"""Validate generated docs*.html output.

Checks, per HTML file:
  * page coverage  - every hemlock/stdlib/docs/*.md and every published
                     top-level hemlock/docs/*.md has a page
  * link targets   - every internal link in page content resolves:
                       #<page-id>            -> page exists
                       #<page-id>/<heading>  -> page exists and has that heading
                     relative file links (foo.md, ../x/) are always broken in
                     a single-file site, so they are reported too
  * nav/page sync  - every page has exactly one nav link and vice versa

Heading ids are computed with the same algorithm as makeId() in the JS
markdown parser embedded by build_docs.py / build_docs.hml (GitHub-style
slugs, de-duplicated with -1, -2, ...). Keep the two in sync.

Usage:
    python3 tests/check_docs.py docs.html [docs-de.html ...] [--strict]
    python3 tests/check_docs.py --json docs.html

Exit status is non-zero with --strict when any English page is missing or any
link is broken. Broken links in translated builds are reported as warnings,
because they usually come from translated headings whose anchors the
translators did not update (the viewer falls back to the top of the page).
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEMLOCK_DIR = ROOT / 'hemlock'

# Must match TOP_LEVEL_DOCS_EXCLUDE in the build scripts.
TOP_LEVEL_EXCLUDE = {'README'}

LINK_RE = re.compile(r'(!?)\[([^\]]+)\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^(#{1,4}) (.*)$')


def extract_pages(html):
    marker = 'const PAGES = '
    start = html.index(marker) + len(marker)
    pages, _ = json.JSONDecoder().raw_decode(html, start)
    return pages


def make_id(text):
    """Python mirror of the JS makeId()."""
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.lower()
    out = []
    for ch in text:
        if unicodedata.category(ch)[0] in 'LMN' or ch in '_-' or ch.isspace():
            out.append(ch)
    return ''.join(out).replace(' ', '-')


def heading_ids(content):
    ids = set()
    seen = {}
    in_code = False
    for line in content.split('\n'):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        base = make_id(m.group(2).strip())
        if base in seen:
            seen[base] += 1
            slug = f'{base}-{seen[base]}'
        else:
            seen[base] = 0
            slug = base
        ids.add(slug)
    return ids


def iter_links(content):
    in_code = False
    for line in content.split('\n'):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Ignore inline code spans so `arr[i](x)` is not mistaken for a link
        line = re.sub(r'`[^`]*`', '', line)
        for m in LINK_RE.finditer(line):
            if m.group(1):  # image
                continue
            yield m.group(3).strip()


def expected_page_ids():
    ids = {f'stdlib-{p.stem}' for p in (HEMLOCK_DIR / 'stdlib' / 'docs').glob('*.md')}
    ids |= {p.stem for p in (HEMLOCK_DIR / 'docs').glob('*.md') if p.stem not in TOP_LEVEL_EXCLUDE}
    return ids


def check_file(path):
    html = Path(path).read_text(encoding='utf-8')
    pages = extract_pages(html)
    by_id = {p['id']: p for p in pages.values()}
    anchors = {pid: heading_ids(p['content']) for pid, p in by_id.items()}
    nav_ids = re.findall(r'class="nav-link" data-page="([^"]*)"', html)

    report = {
        'file': str(path),
        'pages': len(by_id),
        'stdlib_pages': sum(1 for i in by_id if i.startswith('stdlib-')),
        'missing_pages': sorted(expected_page_ids() - set(by_id)),
        'nav_without_page': sorted(set(nav_ids) - set(by_id)),
        'page_without_nav': sorted(set(by_id) - set(nav_ids)),
        'duplicate_nav': sorted({i for i in nav_ids if nav_ids.count(i) > 1}),
        'links': {'external': 0, 'page': 0, 'page+anchor': 0},
        'broken': [],
    }

    for pid, page in by_id.items():
        for href in iter_links(page['content']):
            if re.match(r'^[a-z][a-z0-9+.-]*:', href, re.I):
                report['links']['external'] += 1
                continue
            if not href.startswith('#'):
                report['broken'].append((pid, href, 'relative file link'))
                continue
            target = href[1:]
            page_id, _, anchor = target.partition('/')
            if page_id not in by_id:
                report['broken'].append((pid, href, 'unknown page'))
            elif anchor and anchor not in anchors[page_id]:
                report['broken'].append((pid, href, 'unknown heading'))
            else:
                report['links']['page+anchor' if anchor else 'page'] += 1
    return report


def main(argv):
    strict = '--strict' in argv
    as_json = '--json' in argv
    files = [a for a in argv if not a.startswith('--')] or [str(ROOT / 'docs.html')]

    failed = False
    reports = [check_file(f) for f in files]
    if as_json:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    for r in reports:
        is_en = Path(r['file']).name == 'docs.html'
        structural = r['missing_pages'] or r['nav_without_page'] or r['page_without_nav'] or r['duplicate_nav']
        if not as_json:
            print(f"== {r['file']}")
            print(f"   pages={r['pages']} stdlib={r['stdlib_pages']} links={r['links']} broken={len(r['broken'])}")
            for key in ('missing_pages', 'nav_without_page', 'page_without_nav', 'duplicate_nav'):
                if r[key]:
                    print(f"   {key}: {r[key]}")
            kinds = {}
            for _, _, why in r['broken']:
                kinds[why] = kinds.get(why, 0) + 1
            if kinds:
                print(f"   broken by kind: {kinds}")
            for pid, href, why in r['broken'][:15 if is_en else 5]:
                print(f"     [{why}] {pid}: {href}")
        if structural or (is_en and r['broken']):
            failed = True
    return 1 if (strict and failed) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
