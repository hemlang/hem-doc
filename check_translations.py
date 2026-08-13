#!/usr/bin/env python3
"""Detect stale, unstamped, or orphaned translations.

Compares the SHA-256 hash of each English source file (from the hemlock/hpm
submodules) against the hash recorded for it in translations/manifest.json
at the time it was last translated. A mismatch means the source changed
since the translation was written.

Usage:
    python3 check_translations.py                  # print a report
    python3 check_translations.py --json            # machine-readable report
    python3 check_translations.py --fail-on-stale   # exit 1 if anything is stale (CI gating)
    python3 check_translations.py --update-manifest # stamp current hashes as the new baseline
                                                      # (run this after finishing a translation pass)
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TRANSLATIONS_DIR = ROOT / 'translations'
MANIFEST_PATH = TRANSLATIONS_DIR / 'manifest.json'
LANGS = ['zh', 'de', 'es', 'fr', 'it', 'ja', 'pt', 'ru']


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_translated_files(lang):
    """Relative source paths (e.g. hemlock/CLAUDE.md) that have a translation for `lang`."""
    lang_dir = TRANSLATIONS_DIR / lang
    if not lang_dir.exists():
        return []
    return sorted(str(p.relative_to(lang_dir)) for p in lang_dir.rglob('*.md'))


def load_manifest():
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def save_manifest(manifest):
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')


def check(update=False):
    manifest = load_manifest()
    report = {}
    any_stale = False

    for lang in LANGS:
        rel_paths = find_translated_files(lang)
        lang_manifest = manifest.get(lang, {})
        stale, missing_source, unstamped = [], [], []

        for rel_path in rel_paths:
            source_path = ROOT / rel_path
            if not source_path.exists():
                missing_source.append(rel_path)
                continue

            current_hash = sha256_of(source_path)
            recorded_hash = lang_manifest.get(rel_path)
            if recorded_hash is None:
                unstamped.append(rel_path)
            elif recorded_hash != current_hash:
                stale.append(rel_path)

            if update:
                lang_manifest[rel_path] = current_hash

        if update:
            # Drop entries for translations that were removed.
            lang_manifest = {k: v for k, v in lang_manifest.items() if k in rel_paths}
            manifest[lang] = lang_manifest

        if stale or missing_source or unstamped:
            report[lang] = {
                'stale': stale,
                'unstamped': unstamped,
                'missing_source': missing_source,
            }
        if stale:
            any_stale = True

    if update:
        save_manifest(manifest)
        print(f"Manifest updated: {MANIFEST_PATH}", file=sys.stderr)

    return report, any_stale


def print_report(report):
    if not report:
        print("All translations are up to date.")
        return
    for lang, info in sorted(report.items()):
        print(f"\n[{lang}]")
        if info['stale']:
            print(f"  Stale ({len(info['stale'])}) - source changed since this translation was last updated:")
            for p in info['stale']:
                print(f"    - {p}")
        if info['unstamped']:
            print(f"  Unstamped ({len(info['unstamped'])}) - no baseline hash recorded yet:")
            for p in info['unstamped']:
                print(f"    - {p}")
        if info['missing_source']:
            print(f"  Orphaned ({len(info['missing_source'])}) - source file no longer exists:")
            for p in info['missing_source']:
                print(f"    - {p}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--update-manifest', action='store_true',
                         help='Stamp current source hashes as the new baseline')
    parser.add_argument('--fail-on-stale', action='store_true',
                         help='Exit non-zero if any translation is stale (for CI gating)')
    parser.add_argument('--json', action='store_true', help='Print a machine-readable JSON report')
    args = parser.parse_args()

    report, any_stale = check(update=args.update_manifest)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)

    if args.fail_on_stale and any_stale:
        sys.exit(1)


if __name__ == '__main__':
    main()
