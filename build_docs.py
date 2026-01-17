#!/usr/bin/env python3
"""
Build the Hemlock documentation viewer.

This script generates a standalone HTML file (docs.html) that includes:
- All markdown documentation from the hemlock submodule
- Embedded content (no HTTP server required)
- Beautiful sage/pine green theme
- Multi-page navigation
- Multi-language support

Usage:
    python build_docs.py           # Build English docs (default)
    python build_docs.py --lang zh # Build Chinese docs
    python build_docs.py --lang all # Build all available languages

The hemlock submodule must be initialized before running this script:
    git submodule update --init --recursive
"""

import os
import sys
import json
import base64
import re
import argparse
from pathlib import Path

# Paths to submodules and translations
HEMLOCK_DIR = Path(__file__).parent / 'hemlock'
HPM_DIR = Path(__file__).parent / 'hpm'
TRANSLATIONS_DIR = Path(__file__).parent / 'translations'
OUTPUT_FILE = Path(__file__).parent / 'docs.html'
LLM_OUTPUT_FILE = Path(__file__).parent / 'llms.txt'

# Supported languages with display names
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'zh': '中文',
}

# Section name translations
SECTION_TRANSLATIONS = {
    'zh': {
        'Language Reference': '语言参考',
        'Getting Started': '快速入门',
        'Language Guide': '语言指南',
        'Advanced Topics': '高级主题',
        'API Reference': 'API 参考',
        'Design & Philosophy': '设计与理念',
        'Contributing': '贡献指南',
        'hpm: Getting Started': 'hpm: 快速入门',
        'hpm: User Guide': 'hpm: 用户指南',
        'hpm: Package Development': 'hpm: 包开发',
        'hpm: Reference': 'hpm: 参考',
        'hpm: Other': 'hpm: 其他',
    }
}

# Current build language
CURRENT_LANG = 'en'


def translate_section(section_name, lang):
    """Translate a section name to the target language."""
    if lang == 'en':
        return section_name
    translations = SECTION_TRANSLATIONS.get(lang, {})
    return translations.get(section_name, section_name)


def read_file(path):
    """Read file content."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return ""


def get_translated_path(original_path, lang):
    """Get the translated file path if it exists, otherwise return the original."""
    if lang == 'en':
        return original_path

    original_path = Path(original_path)
    base_dir = Path(__file__).parent

    try:
        rel_path = original_path.relative_to(base_dir)
    except ValueError:
        return original_path

    translated_path = TRANSLATIONS_DIR / lang / rel_path

    if translated_path.exists():
        return translated_path

    return original_path


def read_file_with_translation(path, lang):
    """Read file content, preferring translation if available."""
    translated_path = get_translated_path(path, lang)
    content = read_file(translated_path)
    is_translated = (translated_path != Path(path)) and translated_path.exists()
    return content, is_translated


def smart_title(text):
    """Convert text to title case, preserving acronyms like API."""
    result = text.replace('-', ' ').replace('_', ' ').title()
    # Fix common acronyms that should stay uppercase
    result = result.replace('Api', 'API')
    return result


def encode_image(path):
    """Encode image as base64 data URL."""
    try:
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            ext = str(path).split('.')[-1].lower()
            mime = 'image/png' if ext == 'png' else 'image/jpeg'
            return f"data:{mime};base64,{data}"
    except Exception as e:
        print(f"Warning: Could not encode image {path}: {e}")
        return ""


def convert_md_links(content, current_section):
    """Convert markdown file links to hash-based page IDs.

    Examples:
        [Tutorial](tutorial.md) -> [Tutorial](#getting-started-tutorial)
        [Syntax](../language-guide/syntax.md) -> [Syntax](#language-guide-syntax)
    """
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)

        # Skip external URLs and anchor-only links
        if path.startswith(('http://', 'https://', '#', 'mailto:')):
            return match.group(0)

        # Skip non-markdown links
        if not path.endswith('.md'):
            return match.group(0)

        # Parse the path to get section and filename
        path = path.replace('\\', '/')

        # Handle relative paths
        if path.startswith('../'):
            # Going up to parent, then into another section
            # e.g., ../language-guide/syntax.md
            parts = path.split('/')
            # Find the section (first non-.. part)
            section_idx = 0
            for i, part in enumerate(parts):
                if part != '..':
                    section_idx = i
                    break
            if section_idx < len(parts) - 1:
                section = parts[section_idx]
                filename = parts[-1].replace('.md', '')
                return f'[{text}](#{section}-{filename})'
        elif '/' in path:
            # Direct path like language-guide/syntax.md
            parts = path.split('/')
            section = parts[-2] if len(parts) >= 2 else current_section
            filename = parts[-1].replace('.md', '')
            return f'[{text}](#{section}-{filename})'
        else:
            # Same directory link like tutorial.md
            filename = path.replace('.md', '')
            return f'[{text}](#{current_section}-{filename})'

        return match.group(0)

    # Match markdown links: [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, replace_link, content)


def collect_docs(lang='en'):
    """Collect all documentation files from hemlock and hpm submodules.

    Args:
        lang: Language code ('en', 'zh', etc.). Will use translations if available.
    """
    docs = {}
    translation_stats = {'translated': 0, 'fallback': 0}

    # Add CLAUDE.md as the main documentation
    claude_path = HEMLOCK_DIR / 'CLAUDE.md'
    if claude_path.exists():
        content, is_translated = read_file_with_translation(claude_path, lang)
        content = convert_md_links(content, 'language-reference')
        title = translate_section('Language Reference', lang)
        docs[title] = {
            'id': 'language-reference',
            'content': content,
            'order': 0,
            'section': ''
        }
        if is_translated:
            translation_stats['translated'] += 1
        else:
            translation_stats['fallback'] += 1

    # Collect docs from hemlock/docs/ directory
    docs_dir = HEMLOCK_DIR / 'docs'
    if docs_dir.exists():
        sections = {
            'getting-started': ('Getting Started', 1),
            'language-guide': ('Language Guide', 2),
            'advanced': ('Advanced Topics', 3),
            'reference': ('API Reference', 4),
            'design': ('Design & Philosophy', 5),
            'contributing': ('Contributing', 6),
        }

        for subdir, (section_name, order) in sections.items():
            subdir_path = docs_dir / subdir
            if not subdir_path.exists():
                continue

            translated_section = translate_section(section_name, lang)

            for md_file in sorted(subdir_path.glob('*.md')):
                # Skip development docs
                if 'development' in str(md_file):
                    continue

                file_name = md_file.stem
                # Convert filename to title
                title = smart_title(file_name)
                doc_id = f"{subdir}-{file_name}"

                content, is_translated = read_file_with_translation(md_file, lang)
                content = convert_md_links(content, subdir)

                docs[f"{translated_section} -> {title}"] = {
                    'id': doc_id,
                    'content': content,
                    'order': order,
                    'section': translated_section
                }

                if is_translated:
                    translation_stats['translated'] += 1
                else:
                    translation_stats['fallback'] += 1

    # Collect hpm documentation
    hpm_docs_dir = HPM_DIR / 'docs'
    if hpm_docs_dir.exists():
        # hpm documentation structure - order starts at 10 to appear after hemlock docs
        hpm_sections = {
            # Getting Started docs
            'installation': ('hpm: Getting Started', 10),
            'quick-start': ('hpm: Getting Started', 10),
            'project-setup': ('hpm: Getting Started', 10),
            # User Guide docs
            'commands': ('hpm: User Guide', 11),
            'configuration': ('hpm: User Guide', 11),
            'troubleshooting': ('hpm: User Guide', 11),
            # Package Development docs
            'creating-packages': ('hpm: Package Development', 12),
            'package-spec': ('hpm: Package Development', 12),
            'versioning': ('hpm: Package Development', 12),
            # Reference docs
            'architecture': ('hpm: Reference', 13),
            'exit-codes': ('hpm: Reference', 13),
        }

        for md_file in sorted(hpm_docs_dir.glob('*.md')):
            file_name = md_file.stem
            # Skip the README as it's an index
            if file_name.lower() == 'readme':
                continue

            if file_name in hpm_sections:
                section_name, order = hpm_sections[file_name]
            else:
                # Default section for unknown files
                section_name = 'hpm: Other'
                order = 14

            translated_section = translate_section(section_name, lang)
            title = smart_title(file_name)
            doc_id = f"hpm-{file_name}"

            content, is_translated = read_file_with_translation(md_file, lang)
            content = convert_md_links(content, f"hpm-{file_name}")

            docs[f"{translated_section} -> {title}"] = {
                'id': doc_id,
                'content': content,
                'order': order,
                'section': translated_section
            }

            if is_translated:
                translation_stats['translated'] += 1
            else:
                translation_stats['fallback'] += 1

    # Sort by order, then by name
    sorted_docs = dict(sorted(docs.items(), key=lambda x: (x[1]['order'], x[0])))

    # Print translation stats for non-English builds
    if lang != 'en':
        total = translation_stats['translated'] + translation_stats['fallback']
        if total > 0:
            print(f"  Translation coverage: {translation_stats['translated']}/{total} pages ({100*translation_stats['translated']//total}%)")

    return sorted_docs


def generate_html(docs, logo_data, lang='en'):
    """Generate the complete HTML document.

    Args:
        docs: Dictionary of documentation pages
        logo_data: Base64 encoded logo image
        lang: Language code for this build
    """

    # Generate navigation items
    nav_items = []
    current_section = None

    for title, info in docs.items():
        section = info.get('section', '')

        # Add section header if it's a new section
        if section and section != current_section:
            section_title = smart_title(section)
            if current_section is not None:  # Not the first section
                nav_items.append('</div>')
            nav_items.append(f'<div class="nav-section">')
            nav_items.append(f'<div class="nav-section-title">{section_title}</div>')
            current_section = section
        elif not section and current_section is not None:
            nav_items.append('</div>')
            current_section = None
        elif not section and current_section is None:
            nav_items.append('<div class="nav-section">')
            current_section = 'main'

        # Simplify title for navigation (remove section prefix)
        nav_title = title.split(' -> ')[-1] if ' -> ' in title else title
        nav_items.append(f'<a href="#{info["id"]}" class="nav-link" data-page="{info["id"]}">{nav_title}</a>')

    if current_section:
        nav_items.append('</div>')

    navigation_html = '\n'.join(nav_items)

    # Generate page content (embedded as JSON)
    pages_json = json.dumps({
        title: {'id': info['id'], 'content': info['content']}
        for title, info in docs.items()
    }, ensure_ascii=False)

    # Language-specific titles
    titles = {
        'en': 'Hemlock Language Manual',
        'zh': 'Hemlock 语言手册',
    }
    page_title = titles.get(lang, titles['en'])

    # Generate language switcher options
    lang_options = []
    for code, name in SUPPORTED_LANGUAGES.items():
        filename = 'docs.html' if code == 'en' else f'docs-{code}.html'
        selected = 'selected' if code == lang else ''
        lang_options.append(f'<option value="{filename}" {selected}>{name}</option>')
    lang_options_html = '\n'.join(lang_options)

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --sage: #9CAF88;
            --pine: #2F4F4F;
            --dark-pine: #1a2f2f;
            --light-sage: #E8F4E1;
            --cream: #FAF9F6;
            --text: #2C3E2C;
            --text-light: #5A6F5A;
            --border: #D4E4CB;
            --code-bg: #F5F9F3;
            --accent: #6B8E6B;
        }}

        [data-theme="dark"] {{
            --sage: #6B8E6B;
            --pine: #9CAF88;
            --dark-pine: #0d1a1a;
            --light-sage: #1a2f2f;
            --cream: #0f1a1a;
            --text: #e0e8e0;
            --text-light: #a8b8a8;
            --border: #2a4a4a;
            --code-bg: #162626;
            --accent: #9CAF88;
        }}

        @media (prefers-color-scheme: dark) {{
            :root:not([data-theme="light"]) {{
                --sage: #6B8E6B;
                --pine: #9CAF88;
                --dark-pine: #0d1a1a;
                --light-sage: #1a2f2f;
                --cream: #0f1a1a;
                --text: #e0e8e0;
                --text-light: #a8b8a8;
                --border: #2a4a4a;
                --code-bg: #162626;
                --accent: #9CAF88;
            }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.7;
            color: var(--text);
            background: var(--cream);
        }}

        /* Header */
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: #2F4F4F;
            color: white;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding: 0 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }}

        .header-logo {{
            height: 45px;
            margin-right: 1rem;
        }}

        .header h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-right: auto;
        }}

        /* Layout */
        .container {{
            display: flex;
            margin-top: 70px;
            min-height: calc(100vh - 70px);
        }}

        /* Sidebar */
        .sidebar {{
            position: fixed;
            left: 0;
            top: 70px;
            width: 280px;
            height: calc(100vh - 70px);
            background: var(--light-sage);
            border-right: 2px solid var(--border);
            overflow-y: auto;
            padding: 2rem 0;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            z-index: 900;
        }}

        .sidebar.open {{
            transform: translateX(0);
        }}

        @media (min-width: 1024px) {{
            .sidebar {{
                transform: translateX(0);
            }}
        }}

        .nav-section {{
            margin-bottom: 1.5rem;
        }}

        .nav-section-title {{
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--pine);
            padding: 0 1.5rem;
            margin-bottom: 0.5rem;
        }}

        .nav-link {{
            display: block;
            padding: 0.5rem 1.5rem;
            color: var(--text);
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.2s;
            border-left: 3px solid transparent;
            cursor: pointer;
        }}

        .nav-link:hover {{
            background: rgba(47, 79, 79, 0.05);
            border-left-color: var(--sage);
        }}

        .nav-link.active {{
            background: rgba(47, 79, 79, 0.1);
            border-left-color: var(--pine);
            font-weight: 600;
            color: var(--pine);
        }}

        /* Mobile Menu Toggle */
        .menu-toggle {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 56px;
            height: 56px;
            background: var(--pine);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 1.5rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        @media (min-width: 1024px) {{
            .menu-toggle {{
                display: none;
            }}
        }}

        /* Main Content */
        .main-content {{
            flex: 1;
            margin-left: 0;
            padding: 3rem 2rem;
            max-width: 900px;
        }}

        @media (min-width: 1024px) {{
            .main-content {{
                margin-left: 280px;
            }}
        }}

        /* Typography */
        .content h1 {{
            font-size: 2.5rem;
            color: var(--pine);
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--sage);
        }}

        .content h2 {{
            font-size: 2rem;
            color: var(--pine);
            margin: 3rem 0 1rem;
            padding-top: 1rem;
        }}

        .content h3 {{
            font-size: 1.5rem;
            color: var(--accent);
            margin: 2rem 0 1rem;
        }}

        .content h4 {{
            font-size: 1.2rem;
            color: var(--accent);
            margin: 1.5rem 0 0.8rem;
        }}

        .content p {{
            margin: 1rem 0;
            color: var(--text);
        }}

        .content ul, .content ol {{
            margin: 1rem 0 1rem 2rem;
        }}

        .content li {{
            margin: 0.5rem 0;
        }}

        .content blockquote {{
            border-left: 4px solid var(--sage);
            background: var(--light-sage);
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: var(--text-light);
        }}

        .content hr {{
            border: none;
            border-top: 2px solid var(--border);
            margin: 2rem 0;
        }}

        /* Code Blocks */
        .content code {{
            background: var(--code-bg);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: var(--pine);
        }}

        .code-block {{
            margin: 1.5rem 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
            background: var(--code-bg);
        }}

        .code-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 1rem;
            background: var(--pine);
            color: var(--light-sage);
            font-size: 0.8rem;
        }}

        .code-lang {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-weight: 600;
            text-transform: lowercase;
        }}

        .copy-btn {{
            background: transparent;
            border: 1px solid var(--sage);
            color: var(--light-sage);
            padding: 0.3rem 0.7rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }}

        .copy-btn:hover {{
            background: var(--sage);
            color: var(--pine);
        }}

        .copy-btn.copied {{
            background: var(--sage);
            color: var(--pine);
            border-color: var(--sage);
        }}

        .copy-btn svg {{
            width: 14px;
            height: 14px;
        }}

        .content pre {{
            background: var(--code-bg);
            margin: 0;
            padding: 1.2rem;
            overflow-x: auto;
        }}

        .content pre code {{
            background: none;
            padding: 0;
            border-radius: 0;
            font-size: 0.85rem;
            line-height: 1.6;
        }}

        /* Standalone pre without code-block wrapper (legacy) */
        .content > pre {{
            border: 1px solid var(--border);
            border-left: 4px solid var(--pine);
            border-radius: 4px;
            margin: 1.5rem 0;
        }}

        /* Tables */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }}

        .content th,
        .content td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}

        .content th {{
            background: var(--light-sage);
            color: var(--pine);
            font-weight: 600;
        }}

        /* Links */
        .content a {{
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.2s;
        }}

        .content a:hover {{
            border-bottom-color: var(--accent);
        }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--cream);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--sage);
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent);
        }}

        /* Section anchors */
        .section-anchor {{
            scroll-margin-top: 90px;
        }}

        /* Mobile adjustments */
        @media (max-width: 768px) {{
            .main-content {{
                padding: 2rem 1rem;
            }}

            .content h1 {{
                font-size: 2rem;
            }}

            .content h2 {{
                font-size: 1.6rem;
            }}

            .content h3 {{
                font-size: 1.3rem;
            }}
        }}

        /* Page switching */
        .page {{
            display: none;
        }}

        .page.active {{
            display: block;
        }}

        /* Search */
        .search-container {{
            position: relative;
            margin-right: 1rem;
        }}

        .search-input {{
            width: 200px;
            padding: 0.5rem 1rem;
            padding-left: 2.2rem;
            border: none;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.15);
            color: white;
            font-size: 0.9rem;
            transition: all 0.3s;
        }}

        .search-input::placeholder {{
            color: rgba(255, 255, 255, 0.6);
        }}

        .search-input:focus {{
            outline: none;
            background: rgba(255, 255, 255, 0.25);
            width: 280px;
        }}

        .search-icon {{
            position: absolute;
            left: 0.8rem;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255, 255, 255, 0.6);
            pointer-events: none;
        }}

        .search-results {{
            position: absolute;
            top: calc(100% + 0.5rem);
            left: 0;
            right: 0;
            min-width: 320px;
            max-height: 400px;
            overflow-y: auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            display: none;
            z-index: 1001;
        }}

        .search-results.active {{
            display: block;
        }}

        .search-result {{
            padding: 0.75rem 1rem;
            cursor: pointer;
            border-bottom: 1px solid var(--border);
            transition: background 0.2s;
        }}

        .search-result:last-child {{
            border-bottom: none;
        }}

        .search-result:hover,
        .search-result.selected {{
            background: var(--light-sage);
        }}

        .search-result-title {{
            font-weight: 600;
            color: var(--pine);
            font-size: 0.95rem;
            margin-bottom: 0.25rem;
        }}

        .search-result-section {{
            font-size: 0.75rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .search-result-preview {{
            font-size: 0.85rem;
            color: var(--text-light);
            margin-top: 0.25rem;
            line-height: 1.4;
        }}

        .search-result-preview mark {{
            background: var(--sage);
            color: var(--pine);
            padding: 0 2px;
            border-radius: 2px;
        }}

        .search-no-results {{
            padding: 1rem;
            text-align: center;
            color: var(--text-light);
            font-size: 0.9rem;
        }}

        .search-shortcut {{
            display: none;
            margin-left: 0.5rem;
            padding: 0.15rem 0.4rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.8);
        }}

        @media (min-width: 768px) {{
            .search-shortcut {{
                display: inline-block;
            }}
        }}

        @media (max-width: 768px) {{
            .search-container {{
                position: fixed;
                top: 70px;
                left: 0;
                right: 0;
                margin: 0;
                padding: 0.5rem;
                background: #1a2f2f;
                display: none;
                z-index: 999;
            }}

            .search-container.active {{
                display: block;
            }}

            .search-input {{
                width: 100%;
            }}

            .search-input:focus {{
                width: 100%;
            }}

            .search-results {{
                position: fixed;
                top: 120px;
                left: 0.5rem;
                right: 0.5rem;
                min-width: auto;
                max-height: calc(100vh - 140px);
            }}

            .search-toggle {{
                display: flex;
                align-items: center;
                justify-content: center;
                background: transparent;
                border: none;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                padding: 0.5rem;
                margin-left: auto;
            }}
        }}

        @media (min-width: 769px) {{
            .search-toggle {{
                display: none;
            }}
        }}

        /* Theme Toggle */
        .theme-toggle {{
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            margin-left: 0.5rem;
        }}

        .theme-toggle:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.5);
        }}

        .theme-toggle svg {{
            width: 20px;
            height: 20px;
        }}

        .theme-toggle .sun-icon {{
            display: none;
        }}

        .theme-toggle .moon-icon {{
            display: block;
        }}

        [data-theme="dark"] .theme-toggle .sun-icon {{
            display: block;
        }}

        [data-theme="dark"] .theme-toggle .moon-icon {{
            display: none;
        }}

        @media (prefers-color-scheme: dark) {{
            :root:not([data-theme="light"]) .theme-toggle .sun-icon {{
                display: block;
            }}
            :root:not([data-theme="light"]) .theme-toggle .moon-icon {{
                display: none;
            }}
        }}

        /* Language Switcher */
        .lang-switcher {{
            margin-left: 0.5rem;
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            cursor: pointer;
            outline: none;
        }}

        .lang-switcher:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.5);
        }}

        .lang-switcher:focus {{
            border-color: rgba(255, 255, 255, 0.5);
        }}

        .lang-switcher option {{
            background: var(--pine);
            color: white;
        }}

        [data-theme="dark"] .lang-switcher option {{
            background: var(--bg-primary);
            color: var(--text-primary);
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <img src="{logo_data}" alt="Hemlock Logo" class="header-logo">
        <h1>{page_title}</h1>
        <!-- Search -->
        <div class="search-container" id="searchContainer">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="M21 21l-4.35-4.35"></path>
            </svg>
            <input type="text" class="search-input" id="searchInput" placeholder="Search docs..." autocomplete="off">
            <span class="search-shortcut">Ctrl+K</span>
            <div class="search-results" id="searchResults"></div>
        </div>
        <button class="search-toggle" id="searchToggle">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="M21 21l-4.35-4.35"></path>
            </svg>
        </button>
        <select class="lang-switcher" id="langSwitcher" onchange="switchLanguage(this.value)">
            {lang_options_html}
        </select>
        <button class="theme-toggle" id="themeToggle" title="Toggle dark mode">
            <svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        </button>
    </div>

    <!-- Mobile Menu Toggle -->
    <button class="menu-toggle" id="menuToggle">&#9776;</button>

    <!-- Container -->
    <div class="container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar" id="sidebar">
            {navigation_html}
        </nav>

        <!-- Main Content -->
        <main class="main-content">
            <div class="content" id="content"></div>
        </main>
    </div>

    <script>
        // Embedded documentation pages
        const PAGES = {pages_json};

        // Mobile menu toggle
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');

        menuToggle.addEventListener('click', () => {{
            sidebar.classList.toggle('open');
            menuToggle.textContent = sidebar.classList.contains('open') ? '\\u00d7' : '\\u2630';
        }});

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {{
            if (window.innerWidth < 1024) {{
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {{
                    sidebar.classList.remove('open');
                    menuToggle.textContent = '\\u2630';
                }}
            }}
        }});

        // Theme toggle functionality
        const themeToggle = document.getElementById('themeToggle');
        const root = document.documentElement;

        // Get saved theme or detect system preference
        function getPreferredTheme() {{
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {{
                return savedTheme;
            }}
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }}

        // Apply theme
        function setTheme(theme) {{
            root.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        }}

        // Initialize theme
        const initialTheme = getPreferredTheme();
        if (localStorage.getItem('theme')) {{
            setTheme(initialTheme);
        }}

        // Toggle theme on button click
        themeToggle.addEventListener('click', () => {{
            const currentTheme = root.getAttribute('data-theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

            // Determine current effective theme
            let effectiveTheme;
            if (currentTheme) {{
                effectiveTheme = currentTheme;
            }} else {{
                effectiveTheme = prefersDark ? 'dark' : 'light';
            }}

            // Toggle to opposite theme
            const newTheme = effectiveTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        }});

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {{
            if (!localStorage.getItem('theme')) {{
                // Only auto-switch if user hasn't manually set a preference
                root.removeAttribute('data-theme');
            }}
        }});

        // Markdown parser
        function parseMarkdown(md) {{
            let lines = md.split('\\n');
            let html = '';
            let inCodeBlock = false;
            let codeBlockContent = '';
            let codeBlockLang = '';
            let inList = false;
            let listContent = '';
            let inBlockquote = false;
            let blockquoteContent = '';
            let inTable = false;
            let tableRows = [];
            let tableHasHeader = false;

            function processInlineMarkdown(text) {{
                text = text.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
                text = text.replace(/\\*([^*]+)\\*/g, '<em>$1</em>');
                text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
                text = text.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<a href="$2">$1</a>');
                return text;
            }}

            function makeId(text) {{
                return text.toLowerCase()
                    .replace(/[^\\w\\s-]/g, '')
                    .replace(/\\s+/g, '-')
                    .replace(/^-+|-+$/g, '');
            }}

            function flushList() {{
                if (inList && listContent) {{
                    html += '<ul>\\n' + listContent + '</ul>\\n';
                    listContent = '';
                    inList = false;
                }}
            }}

            function flushBlockquote() {{
                if (inBlockquote && blockquoteContent) {{
                    html += '<blockquote>' + processInlineMarkdown(blockquoteContent.trim()) + '</blockquote>\\n';
                    blockquoteContent = '';
                    inBlockquote = false;
                }}
            }}

            function flushTable() {{
                if (inTable && tableRows.length > 0) {{
                    html += '<table>\\n';
                    for (let r = 0; r < tableRows.length; r++) {{
                        const row = tableRows[r];
                        const isHeader = tableHasHeader && r === 0;
                        const tag = isHeader ? 'th' : 'td';
                        html += '<tr>\\n';
                        for (const cell of row) {{
                            html += '<' + tag + '>' + processInlineMarkdown(cell.trim()) + '</' + tag + '>\\n';
                        }}
                        html += '</tr>\\n';
                    }}
                    html += '</table>\\n';
                    tableRows = [];
                    inTable = false;
                    tableHasHeader = false;
                }}
            }}

            function isTableSeparator(line) {{
                return /^\\|?[\\s-:|]+\\|[\\s-:|]+\\|?$/.test(line) && line.includes('-');
            }}

            function parseTableRow(line) {{
                let cells = line.split('|');
                // Remove empty first/last cells from leading/trailing |
                if (cells.length > 0 && cells[0].trim() === '') cells.shift();
                if (cells.length > 0 && cells[cells.length - 1].trim() === '') cells.pop();
                return cells;
            }}

            for (let i = 0; i < lines.length; i++) {{
                let line = lines[i];
                const trimmedLine = line.trim();

                // Handle code blocks (including indented ones in lists)
                if (trimmedLine.startsWith('```')) {{
                    if (inCodeBlock) {{
                        const codeId = 'code-' + Math.random().toString(36).substr(2, 9);
                        const langDisplay = codeBlockLang || 'code';
                        const copyIcon = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>';
                        html += `<div class="code-block">
                            <div class="code-header">
                                <span class="code-lang">${{langDisplay}}</span>
                                <button class="copy-btn" onclick="copyCode('${{codeId}}')">${{copyIcon}}<span>Copy</span></button>
                            </div>
                            <pre><code id="${{codeId}}">` + escapeHtml(codeBlockContent) + '</code></pre></div>\\n';
                        codeBlockContent = '';
                        codeBlockLang = '';
                        inCodeBlock = false;
                    }} else {{
                        flushList();
                        flushBlockquote();
                        inCodeBlock = true;
                        codeBlockLang = trimmedLine.substring(3).trim();
                    }}
                    continue;
                }}

                if (inCodeBlock) {{
                    codeBlockContent += line + '\\n';
                    continue;
                }}

                // Table handling
                if (trimmedLine.includes('|')) {{
                    if (trimmedLine.startsWith('|') || trimmedLine.endsWith('|')) {{
                        flushList();
                        flushBlockquote();
                        if (isTableSeparator(trimmedLine)) {{
                            // This is the separator row (|---|---|), mark header
                            if (tableRows.length === 1) {{
                                tableHasHeader = true;
                            }}
                        }} else {{
                            // Regular table row
                            tableRows.push(parseTableRow(trimmedLine));
                            inTable = true;
                        }}
                        continue;
                    }}
                }}
                // Flush table if we hit a non-table line
                if (inTable) {{
                    flushTable();
                }}

                if (line.startsWith('# ')) {{
                    flushList();
                    flushBlockquote();
                    const text = line.substring(2).trim();
                    const id = makeId(text);
                    html += `<h1 class="section-anchor" id="${{id}}">${{processInlineMarkdown(text)}}</h1>\\n`;
                    continue;
                }}
                if (line.startsWith('## ')) {{
                    flushList();
                    flushBlockquote();
                    const text = line.substring(3).trim();
                    const id = makeId(text);
                    html += `<h2 class="section-anchor" id="${{id}}">${{processInlineMarkdown(text)}}</h2>\\n`;
                    continue;
                }}
                if (line.startsWith('### ')) {{
                    flushList();
                    flushBlockquote();
                    const text = line.substring(4).trim();
                    const id = makeId(text);
                    html += `<h3 class="section-anchor" id="${{id}}">${{processInlineMarkdown(text)}}</h3>\\n`;
                    continue;
                }}
                if (line.startsWith('#### ')) {{
                    flushList();
                    flushBlockquote();
                    const text = line.substring(5).trim();
                    const id = makeId(text);
                    html += `<h4 class="section-anchor" id="${{id}}">${{processInlineMarkdown(text)}}</h4>\\n`;
                    continue;
                }}

                if (line.trim() === '---') {{
                    flushList();
                    flushBlockquote();
                    html += '<hr>\\n';
                    continue;
                }}

                if (line.startsWith('> ')) {{
                    flushList();
                    blockquoteContent += line.substring(2) + ' ';
                    inBlockquote = true;
                    continue;
                }} else if (inBlockquote && line.trim() === '') {{
                    flushBlockquote();
                    continue;
                }}

                if (line.startsWith('- ') || line.startsWith('* ')) {{
                    flushBlockquote();
                    const text = line.substring(2).trim();
                    listContent += '<li>' + processInlineMarkdown(text) + '</li>\\n';
                    inList = true;
                    continue;
                }} else if (inList && line.trim() !== '' && !line.startsWith('#')) {{
                    listContent = listContent.trimEnd();
                    if (listContent.endsWith('</li>')) {{
                        listContent = listContent.substring(0, listContent.length - 5);
                        listContent += ' ' + processInlineMarkdown(line.trim()) + '</li>\\n';
                    }}
                    continue;
                }} else if (inList && line.trim() === '') {{
                    flushList();
                    continue;
                }}

                if (line.trim() === '') {{
                    flushList();
                    flushBlockquote();
                    continue;
                }}

                flushList();
                flushBlockquote();
                if (line.trim() !== '') {{
                    html += '<p>' + processInlineMarkdown(line) + '</p>\\n';
                }}
            }}

            flushList();
            flushBlockquote();
            flushTable();

            return html;
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        // Copy code to clipboard
        function copyCode(codeId) {{
            const codeElement = document.getElementById(codeId);
            if (!codeElement) return;

            const text = codeElement.textContent;
            navigator.clipboard.writeText(text).then(() => {{
                // Find the button that triggered this
                const btn = codeElement.closest('.code-block').querySelector('.copy-btn');
                if (btn) {{
                    const originalText = btn.querySelector('span').textContent;
                    btn.classList.add('copied');
                    btn.querySelector('span').textContent = 'Copied!';

                    setTimeout(() => {{
                        btn.classList.remove('copied');
                        btn.querySelector('span').textContent = originalText;
                    }}, 2000);
                }}
            }}).catch(err => {{
                console.error('Failed to copy:', err);
            }});
        }}

        // Load a page
        function loadPage(pageId) {{
            const pageData = Object.values(PAGES).find(p => p.id === pageId);
            if (!pageData) {{
                console.error('Page not found:', pageId);
                return;
            }}

            const content = parseMarkdown(pageData.content);
            document.getElementById('content').innerHTML = content;

            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(link => {{
                link.classList.remove('active');
                if (link.dataset.page === pageId) {{
                    link.classList.add('active');
                }}
            }});

            // Scroll to top
            window.scrollTo(0, 0);

            // Update URL hash
            window.location.hash = pageId;
        }}

        // Setup navigation
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', (e) => {{
                e.preventDefault();
                const pageId = link.dataset.page;
                loadPage(pageId);

                // Close mobile menu
                if (window.innerWidth < 1024) {{
                    sidebar.classList.remove('open');
                    menuToggle.textContent = '\\u2630';
                }}
            }});
        }});

        // Handle browser back/forward
        window.addEventListener('hashchange', () => {{
            const hash = window.location.hash.substring(1);
            if (hash) {{
                loadPage(hash);
            }}
        }});

        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        const searchContainer = document.getElementById('searchContainer');
        const searchToggle = document.getElementById('searchToggle');
        let selectedIndex = -1;
        let currentResults = [];

        // Build search index from PAGES
        function buildSearchIndex() {{
            const index = [];
            for (const [title, page] of Object.entries(PAGES)) {{
                // Extract section from page ID
                const parts = page.id.split('-');
                let section = '';
                if (parts.length > 1) {{
                    section = parts.slice(0, -1).join(' ');
                }}

                // Extract headings from content
                const headings = [];
                const headingRegex = /^#+\\s+(.+)$/gm;
                let match;
                while ((match = headingRegex.exec(page.content)) !== null) {{
                    headings.push(match[1]);
                }}

                // Get preview text (first 200 chars, stripped of markdown)
                let preview = page.content
                    .replace(/^#+\\s+.+$/gm, '')  // Remove headings
                    .replace(/```[\\s\\S]*?```/g, '')  // Remove code blocks
                    .replace(/`[^`]+`/g, '')  // Remove inline code
                    .replace(/\\[([^\\]]+)\\]\\([^)]+\\)/g, '$1')  // Convert links to text
                    .replace(/\\*\\*([^*]+)\\*\\*/g, '$1')  // Remove bold
                    .replace(/\\*([^*]+)\\*/g, '$1')  // Remove italic
                    .replace(/\\n+/g, ' ')  // Normalize whitespace
                    .trim()
                    .substring(0, 200);

                index.push({{
                    title: title,
                    pageId: page.id,
                    section: section,
                    headings: headings,
                    content: page.content.toLowerCase(),
                    preview: preview
                }});
            }}
            return index;
        }}

        const searchIndex = buildSearchIndex();

        // Search function
        function search(query) {{
            if (!query || query.length < 2) return [];

            const q = query.toLowerCase().trim();
            const results = [];

            for (const item of searchIndex) {{
                let score = 0;
                let matchedHeading = null;
                let matchContext = '';

                // Check title (highest priority)
                const titleLower = item.title.toLowerCase();
                if (titleLower === q) {{
                    score = 100;
                }} else if (titleLower.startsWith(q)) {{
                    score = 80;
                }} else if (titleLower.includes(q)) {{
                    score = 60;
                }}

                // Check headings
                for (const heading of item.headings) {{
                    const headingLower = heading.toLowerCase();
                    if (headingLower === q) {{
                        score = Math.max(score, 50);
                        matchedHeading = heading;
                    }} else if (headingLower.includes(q)) {{
                        score = Math.max(score, 40);
                        if (!matchedHeading) matchedHeading = heading;
                    }}
                }}

                // Check content
                if (item.content.includes(q)) {{
                    score = Math.max(score, 20);

                    // Find context around the match
                    const idx = item.content.indexOf(q);
                    const start = Math.max(0, idx - 40);
                    const end = Math.min(item.content.length, idx + q.length + 60);
                    matchContext = item.content.substring(start, end);
                    if (start > 0) matchContext = '...' + matchContext;
                    if (end < item.content.length) matchContext = matchContext + '...';
                }}

                if (score > 0) {{
                    results.push({{
                        title: item.title,
                        pageId: item.pageId,
                        section: item.section,
                        score: score,
                        matchedHeading: matchedHeading,
                        preview: matchContext || item.preview,
                        query: q
                    }});
                }}
            }}

            // Sort by score descending
            results.sort((a, b) => b.score - a.score);

            return results.slice(0, 10);  // Limit to 10 results
        }}

        // Highlight query in text
        function highlightText(text, query) {{
            if (!query) return text;
            const regex = new RegExp(`(${{query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        }}

        // Render search results
        function renderResults(results, query) {{
            if (results.length === 0) {{
                searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
                return;
            }}

            const html = results.map((result, index) => {{
                const titleHtml = highlightText(result.title, query);
                const previewHtml = highlightText(result.preview, query);
                const selectedClass = index === selectedIndex ? ' selected' : '';

                return `
                    <div class="search-result${{selectedClass}}" data-index="${{index}}" data-page="${{result.pageId}}">
                        ${{result.section ? `<div class="search-result-section">${{result.section}}</div>` : ''}}
                        <div class="search-result-title">${{titleHtml}}</div>
                        ${{result.matchedHeading ? `<div class="search-result-preview">${{highlightText(result.matchedHeading, query)}}</div>` : ''}}
                        <div class="search-result-preview">${{previewHtml}}</div>
                    </div>
                `;
            }}).join('');

            searchResults.innerHTML = html;

            // Add click handlers
            searchResults.querySelectorAll('.search-result').forEach(el => {{
                el.addEventListener('click', () => {{
                    const pageId = el.dataset.page;
                    loadPage(pageId);
                    closeSearch();
                }});
            }});
        }}

        // Show search results
        function showResults() {{
            searchResults.classList.add('active');
        }}

        // Hide search results
        function hideResults() {{
            searchResults.classList.remove('active');
            selectedIndex = -1;
        }}

        // Close search (mobile)
        function closeSearch() {{
            hideResults();
            searchInput.value = '';
            searchInput.blur();
            if (window.innerWidth < 769) {{
                searchContainer.classList.remove('active');
            }}
        }}

        // Debounce function
        function debounce(func, wait) {{
            let timeout;
            return function executedFunction(...args) {{
                const later = () => {{
                    clearTimeout(timeout);
                    func(...args);
                }};
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            }};
        }}

        // Handle search input
        const handleSearch = debounce((query) => {{
            currentResults = search(query);
            if (query.length >= 2) {{
                renderResults(currentResults, query);
                showResults();
            }} else {{
                hideResults();
            }}
        }}, 150);

        searchInput.addEventListener('input', (e) => {{
            handleSearch(e.target.value);
        }});

        // Handle keyboard navigation
        searchInput.addEventListener('keydown', (e) => {{
            if (!searchResults.classList.contains('active')) return;

            if (e.key === 'ArrowDown') {{
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, currentResults.length - 1);
                renderResults(currentResults, searchInput.value);
            }} else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                renderResults(currentResults, searchInput.value);
            }} else if (e.key === 'Enter') {{
                e.preventDefault();
                if (selectedIndex >= 0 && currentResults[selectedIndex]) {{
                    loadPage(currentResults[selectedIndex].pageId);
                    closeSearch();
                }} else if (currentResults.length > 0) {{
                    loadPage(currentResults[0].pageId);
                    closeSearch();
                }}
            }} else if (e.key === 'Escape') {{
                closeSearch();
            }}
        }});

        // Close results when clicking outside
        document.addEventListener('click', (e) => {{
            if (!searchContainer.contains(e.target)) {{
                hideResults();
            }}
        }});

        // Focus search on input click
        searchInput.addEventListener('focus', () => {{
            if (searchInput.value.length >= 2) {{
                handleSearch(searchInput.value);
            }}
        }});

        // Global keyboard shortcut (Ctrl+K or Cmd+K)
        document.addEventListener('keydown', (e) => {{
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
                e.preventDefault();
                if (window.innerWidth < 769) {{
                    searchContainer.classList.add('active');
                }}
                searchInput.focus();
            }}
            if (e.key === 'Escape') {{
                closeSearch();
            }}
        }});

        // Mobile search toggle
        if (searchToggle) {{
            searchToggle.addEventListener('click', () => {{
                searchContainer.classList.toggle('active');
                if (searchContainer.classList.contains('active')) {{
                    searchInput.focus();
                }}
            }});
        }}

        // Language switcher
        function switchLanguage(filename) {{
            const currentHash = window.location.hash;
            window.location.href = filename + currentHash;
        }}

        // Load initial page
        const initialHash = window.location.hash.substring(1);
        const firstPageId = Object.values(PAGES)[0].id;
        loadPage(initialHash || firstPageId);
    </script>
</body>
</html>'''

    return html


def generate_llm_txt(docs):
    """Generate LLM-friendly plain text documentation.

    Creates a single text file optimized for LLM context windows:
    - Clear structure with section markers
    - All documentation concatenated
    - No HTML/CSS/JS overhead
    - Easy to parse and understand
    """
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append("HEMLOCK PROGRAMMING LANGUAGE - COMPLETE DOCUMENTATION")
    lines.append("=" * 80)
    lines.append("")
    lines.append("This file contains the complete documentation for the Hemlock programming")
    lines.append("language and the hpm package manager. It is optimized for LLM consumption.")
    lines.append("")
    lines.append("Source: https://github.com/hemlang/hem-doc")
    lines.append("")

    # Table of contents
    lines.append("-" * 80)
    lines.append("TABLE OF CONTENTS")
    lines.append("-" * 80)
    lines.append("")

    current_section = None
    toc_num = 1
    for title, info in docs.items():
        section = info.get('section', '')
        if section and section != current_section:
            lines.append(f"\n[{section}]")
            current_section = section

        # Simplify title for TOC
        nav_title = title.split(' -> ')[-1] if ' -> ' in title else title
        lines.append(f"  {toc_num}. {nav_title}")
        toc_num += 1

    lines.append("")
    lines.append("")

    # Documentation content
    lines.append("=" * 80)
    lines.append("DOCUMENTATION")
    lines.append("=" * 80)

    current_section = None
    for title, info in docs.items():
        section = info.get('section', '')

        # Add section divider if new section
        if section and section != current_section:
            lines.append("")
            lines.append("")
            lines.append("#" * 80)
            lines.append(f"# {section.upper()}")
            lines.append("#" * 80)
            current_section = section

        # Page header
        nav_title = title.split(' -> ')[-1] if ' -> ' in title else title
        lines.append("")
        lines.append("-" * 80)
        lines.append(f"## {nav_title}")
        lines.append("-" * 80)
        lines.append("")

        # Page content (strip trailing whitespace from each line)
        content = info['content']
        for line in content.split('\n'):
            lines.append(line.rstrip())

    # Footer
    lines.append("")
    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF DOCUMENTATION")
    lines.append("=" * 80)

    return '\n'.join(lines)


def build_for_language(lang, logo_data):
    """Build documentation for a specific language."""
    global CURRENT_LANG
    CURRENT_LANG = lang

    lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
    print(f"\nBuilding {lang_name} ({lang}) documentation...")

    # Determine output file
    if lang == 'en':
        output_file = Path(__file__).parent / 'docs.html'
    else:
        output_file = Path(__file__).parent / f'docs-{lang}.html'

    # Collect documentation
    print("Collecting documentation files...")
    docs = collect_docs(lang)
    if not docs:
        print("Error: No documentation pages found")
        return False, None
    print(f"Found {len(docs)} documentation pages")

    # Generate HTML
    print("Generating HTML...")
    html = generate_html(docs, logo_data, lang)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Documentation built: {output_file}")
    print(f"  - {len(docs)} pages")
    return True, docs


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description='Build Hemlock documentation viewer')
    parser.add_argument('--lang', '-l', default='en',
                        help=f'Language to build: {", ".join(SUPPORTED_LANGUAGES.keys())} or "all" (default: en)')
    args = parser.parse_args()

    print("Building Hemlock documentation viewer...")

    # Check that hemlock submodule exists
    if not HEMLOCK_DIR.exists():
        print(f"Error: hemlock submodule not found at {HEMLOCK_DIR}")
        print("Run: git submodule update --init --recursive")
        sys.exit(1)

    # Check for required files
    claude_md = HEMLOCK_DIR / 'CLAUDE.md'
    docs_dir = HEMLOCK_DIR / 'docs'
    if not claude_md.exists() and not docs_dir.exists():
        print("Error: No documentation found in hemlock submodule")
        print(f"  Expected: {claude_md} or {docs_dir}")
        sys.exit(1)

    # Check for hpm submodule (optional but warn if missing)
    if not HPM_DIR.exists():
        print(f"Warning: hpm submodule not found at {HPM_DIR}")
        print("  hpm documentation will not be included")
        print("  Run: git submodule update --init --recursive")
    else:
        hpm_docs = HPM_DIR / 'docs'
        if hpm_docs.exists():
            print(f"Found hpm documentation at {hpm_docs}")

    # Encode logo (once for all languages)
    print("Encoding logo...")
    logo_path = HEMLOCK_DIR / 'logo.png'
    logo_data = encode_image(logo_path) if logo_path.exists() else ""
    if not logo_data:
        print("Warning: logo.png not found, continuing without logo")

    # Determine which languages to build
    if args.lang == 'all':
        languages = list(SUPPORTED_LANGUAGES.keys())
    elif args.lang in SUPPORTED_LANGUAGES:
        languages = [args.lang]
    else:
        print(f"Error: Unknown language '{args.lang}'")
        print(f"Supported languages: {', '.join(SUPPORTED_LANGUAGES.keys())}")
        sys.exit(1)

    # Build for each language
    success_count = 0
    english_docs = None
    for lang in languages:
        success, docs = build_for_language(lang, logo_data)
        if success:
            success_count += 1
            if lang == 'en':
                english_docs = docs

    # Generate LLM-friendly documentation (only for English)
    if english_docs:
        print("\nGenerating LLM-friendly documentation...")
        llm_txt = generate_llm_txt(english_docs)

        with open(LLM_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(llm_txt)

        print(f"LLM documentation built: {LLM_OUTPUT_FILE}")
        print(f"  - {len(llm_txt)} characters")

    print(f"\nBuild complete: {success_count}/{len(languages)} languages built successfully")


if __name__ == '__main__':
    main()
