#!/usr/bin/env python3
"""
Build the Hemlock documentation viewer.

This script generates a standalone HTML file (docs.html) that includes:
- All markdown documentation from the hemlock submodule
- Embedded content (no HTTP server required)
- Beautiful sage/pine green theme
- Multi-page navigation

Usage:
    python build_docs.py

The hemlock submodule must be initialized before running this script:
    git submodule update --init --recursive
"""

import os
import sys
import json
import base64
import re
from pathlib import Path

# Path to the hemlock submodule
HEMLOCK_DIR = Path(__file__).parent / 'hemlock'
OUTPUT_FILE = Path(__file__).parent / 'docs.html'


def read_file(path):
    """Read file content."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return ""


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


def collect_docs():
    """Collect all documentation files from hemlock submodule."""
    docs = {}

    # Add CLAUDE.md as the main documentation
    claude_path = HEMLOCK_DIR / 'CLAUDE.md'
    if claude_path.exists():
        content = read_file(claude_path)
        content = convert_md_links(content, 'language-reference')
        docs['Language Reference'] = {
            'id': 'language-reference',
            'content': content,
            'order': 0
        }

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

            for md_file in sorted(subdir_path.glob('*.md')):
                # Skip development docs
                if 'development' in str(md_file):
                    continue

                file_name = md_file.stem
                # Convert filename to title
                title = file_name.replace('-', ' ').replace('_', ' ').title()
                doc_id = f"{subdir}-{file_name}"

                content = read_file(md_file)
                content = convert_md_links(content, subdir)

                docs[f"{section_name} -> {title}"] = {
                    'id': doc_id,
                    'content': content,
                    'order': order,
                    'section': section_name
                }

    # Sort by order, then by name
    sorted_docs = dict(sorted(docs.items(), key=lambda x: (x[1]['order'], x[0])))
    return sorted_docs


def generate_html(docs, logo_data):
    """Generate the complete HTML document."""

    # Generate navigation items
    nav_items = []
    current_section = None

    for title, info in docs.items():
        section = info.get('section', '')

        # Add section header if it's a new section
        if section and section != current_section:
            section_title = section.replace('-', ' ').title()
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

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hemlock Language Manual</title>
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

        /* Dark mode colors */
        [data-theme="dark"] {{
            --sage: #6B8E6B;
            --pine: #9CAF88;
            --dark-pine: #0d1a1a;
            --light-sage: #1a2f2f;
            --cream: #0f1f1f;
            --text: #E8F4E1;
            --text-light: #9CAF88;
            --border: #2F4F4F;
            --code-bg: #1a2f2f;
            --accent: #9CAF88;
        }}

        [data-theme="dark"] .header {{
            background: #1a2f2f;
        }}

        [data-theme="dark"] .search-input {{
            background: #0f1f1f;
            color: var(--text);
        }}

        [data-theme="dark"] .search-results {{
            background: #1a2f2f;
        }}

        [data-theme="dark"] .toc {{
            background: #1a2f2f;
        }}

        [data-theme="dark"] .code-header {{
            background: #0d1a1a;
        }}

        /* Skip to content link for accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--pine);
            color: white;
            padding: 8px 16px;
            z-index: 10000;
            text-decoration: none;
            font-weight: 600;
            border-radius: 0 0 4px 0;
            transition: top 0.3s;
        }}

        .skip-link:focus {{
            top: 0;
        }}

        /* Focus visible styles for keyboard navigation */
        :focus-visible {{
            outline: 3px solid var(--sage);
            outline-offset: 2px;
        }}

        *:focus:not(:focus-visible) {{
            outline: none;
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
            background: var(--pine);
            color: white;
            display: flex;
            align-items: center;
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
        }}

        .header .tagline {{
            margin-left: auto;
            font-size: 0.9rem;
            font-style: italic;
            color: var(--light-sage);
            display: none;
        }}

        @media (min-width: 768px) {{
            .header .tagline {{
                display: block;
            }}
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
            padding: 1rem 0 2rem 0;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            z-index: 900;
        }}

        .sidebar.open {{
            transform: translateX(0);
        }}

        /* Search Box */
        .search-container {{
            padding: 0 1rem 1rem 1rem;
            border-bottom: 1px solid var(--border);
            margin-bottom: 1rem;
        }}

        .search-box {{
            position: relative;
            width: 100%;
        }}

        .search-input {{
            width: 100%;
            padding: 0.6rem 0.8rem 0.6rem 2.2rem;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 0.9rem;
            background: white;
            color: var(--text);
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .search-input:focus {{
            border-color: var(--sage);
            box-shadow: 0 0 0 3px rgba(156, 175, 136, 0.2);
            outline: none;
        }}

        .search-input::placeholder {{
            color: var(--text-light);
        }}

        .search-icon {{
            position: absolute;
            left: 0.7rem;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            color: var(--text-light);
            pointer-events: none;
        }}

        .search-shortcut {{
            position: absolute;
            right: 0.5rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.7rem;
            color: var(--text-light);
            background: var(--light-sage);
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
            border: 1px solid var(--border);
            pointer-events: none;
        }}

        .search-results {{
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid var(--border);
            border-radius: 6px;
            margin-top: 4px;
            max-height: 300px;
            overflow-y: auto;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            display: none;
        }}

        .search-results.active {{
            display: block;
        }}

        .search-result {{
            padding: 0.6rem 0.8rem;
            cursor: pointer;
            border-bottom: 1px solid var(--border);
            transition: background 0.15s;
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
            font-size: 0.9rem;
        }}

        .search-result-preview {{
            font-size: 0.8rem;
            color: var(--text-light);
            margin-top: 0.2rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .search-result-preview mark {{
            background: rgba(156, 175, 136, 0.4);
            color: var(--pine);
            border-radius: 2px;
            padding: 0 2px;
        }}

        .no-results {{
            padding: 1rem;
            text-align: center;
            color: var(--text-light);
            font-size: 0.9rem;
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

        /* Table of Contents */
        .toc {{
            background: var(--light-sage);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-bottom: 2rem;
        }}

        .toc-title {{
            font-weight: 700;
            color: var(--pine);
            font-size: 0.9rem;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .toc-title svg {{
            width: 16px;
            height: 16px;
        }}

        .toc-list {{
            list-style: none;
            margin: 0;
            padding: 0;
        }}

        .toc-list li {{
            margin: 0.3rem 0;
        }}

        .toc-list a {{
            color: var(--text);
            text-decoration: none;
            font-size: 0.85rem;
            transition: color 0.2s;
            display: block;
            padding: 0.2rem 0;
        }}

        .toc-list a:hover {{
            color: var(--pine);
        }}

        .toc-list .toc-h3 {{
            padding-left: 1rem;
            font-size: 0.8rem;
            color: var(--text-light);
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

        /* Syntax Highlighting */
        .token-keyword {{
            color: #8B5CF6;
            font-weight: 600;
        }}

        .token-string {{
            color: #059669;
        }}

        .token-number {{
            color: #D97706;
        }}

        .token-comment {{
            color: #6B7280;
            font-style: italic;
        }}

        .token-function {{
            color: #2563EB;
        }}

        .token-operator {{
            color: #DC2626;
        }}

        .token-punctuation {{
            color: #64748B;
        }}

        .token-type {{
            color: #0891B2;
        }}

        .token-builtin {{
            color: #7C3AED;
        }}

        .token-property {{
            color: #0D9488;
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

        /* Theme Toggle */
        .theme-toggle {{
            background: transparent;
            border: 1px solid var(--sage);
            color: var(--light-sage);
            padding: 0.4rem 0.6rem;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.8rem;
            transition: all 0.2s;
            margin-left: 1rem;
        }}

        .theme-toggle:hover {{
            background: var(--sage);
            color: var(--pine);
        }}

        .theme-toggle svg {{
            width: 16px;
            height: 16px;
        }}

        @media (max-width: 768px) {{
            .theme-toggle span {{
                display: none;
            }}
        }}

        /* Previous/Next Navigation */
        .page-nav {{
            display: flex;
            justify-content: space-between;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid var(--border);
            gap: 1rem;
        }}

        .page-nav-link {{
            display: flex;
            flex-direction: column;
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: 8px;
            text-decoration: none;
            color: var(--text);
            transition: all 0.2s;
            max-width: 45%;
        }}

        .page-nav-link:hover {{
            border-color: var(--sage);
            background: var(--light-sage);
        }}

        .page-nav-link.prev {{
            align-items: flex-start;
        }}

        .page-nav-link.next {{
            align-items: flex-end;
            margin-left: auto;
        }}

        .page-nav-label {{
            font-size: 0.75rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }}

        .page-nav-title {{
            font-weight: 600;
            color: var(--pine);
            font-size: 0.95rem;
        }}

        /* Edit on GitHub link */
        .edit-link {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.85rem;
            color: var(--text-light);
            text-decoration: none;
            margin-top: 2rem;
            padding: 0.5rem 0;
            transition: color 0.2s;
        }}

        .edit-link:hover {{
            color: var(--pine);
        }}

        .edit-link svg {{
            width: 16px;
            height: 16px;
        }}

        /* Loading indicator */
        .loading-overlay {{
            position: fixed;
            top: 70px;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--cream);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 500;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s;
        }}

        .loading-overlay.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        @media (min-width: 1024px) {{
            .loading-overlay {{
                left: 280px;
            }}
        }}

        .loading-spinner {{
            width: 40px;
            height: 40px;
            border: 3px solid var(--border);
            border-top-color: var(--sage);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Offline indicator */
        .offline-banner {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #FCD34D;
            color: #78350F;
            padding: 0.5rem 1rem;
            text-align: center;
            font-size: 0.85rem;
            z-index: 10001;
            display: none;
        }}

        .offline-banner.visible {{
            display: block;
        }}

        /* Print stylesheet */
        @media print {{
            .header {{
                position: static;
                box-shadow: none;
            }}

            .sidebar,
            .menu-toggle,
            .skip-link,
            .copy-btn {{
                display: none !important;
            }}

            .container {{
                display: block;
                margin-top: 0;
            }}

            .main-content {{
                margin-left: 0 !important;
                padding: 1rem;
                max-width: none;
            }}

            .code-block {{
                break-inside: avoid;
            }}

            .content h1,
            .content h2,
            .content h3 {{
                break-after: avoid;
            }}

            .content a {{
                color: var(--text);
            }}

            .content a[href^="http"]::after {{
                content: " (" attr(href) ")";
                font-size: 0.8em;
                color: var(--text-light);
            }}
        }}
    </style>
</head>
<body>
    <!-- Skip to main content link for accessibility -->
    <a href="#main-content" class="skip-link">Skip to main content</a>

    <!-- Header -->
    <header class="header" role="banner">
        <img src="{logo_data}" alt="Hemlock Logo" class="header-logo">
        <h1>Hemlock Language Manual</h1>
        <span class="tagline">"A small, unsafe language for writing unsafe things safely."</span>
        <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="sun-icon" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="moon-icon" style="display:none" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <span>Dark</span>
        </button>
    </header>

    <!-- Mobile Menu Toggle -->
    <button class="menu-toggle" id="menuToggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="sidebar">&#9776;</button>

    <!-- Container -->
    <div class="container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar" id="sidebar" aria-label="Documentation navigation">
            <!-- Search Box -->
            <div class="search-container">
                <div class="search-box">
                    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input type="text" class="search-input" id="searchInput" placeholder="Search docs..." aria-label="Search documentation" autocomplete="off">
                    <span class="search-shortcut" aria-hidden="true">⌘K</span>
                    <div class="search-results" id="searchResults" role="listbox" aria-label="Search results"></div>
                </div>
            </div>
            {navigation_html}
        </nav>

        <!-- Main Content -->
        <main class="main-content" id="main-content" role="main">
            <div class="content" id="content" aria-live="polite"></div>
        </main>

        <!-- Loading Overlay -->
        <div class="loading-overlay" id="loadingOverlay" aria-hidden="true">
            <div class="loading-spinner"></div>
        </div>
    </div>

    <!-- Offline Banner -->
    <div class="offline-banner" id="offlineBanner" role="alert">
        You are currently offline. Some features may be unavailable.
    </div>

    <script>
        // Embedded documentation pages
        const PAGES = {pages_json};

        // Loading overlay
        const loadingOverlay = document.getElementById('loadingOverlay');
        let loadingTimeout = null;

        function showLoading() {{
            // Only show loading for longer operations
            loadingTimeout = setTimeout(() => {{
                loadingOverlay.classList.add('active');
                loadingOverlay.setAttribute('aria-hidden', 'false');
            }}, 100);
        }}

        function hideLoading() {{
            clearTimeout(loadingTimeout);
            loadingOverlay.classList.remove('active');
            loadingOverlay.setAttribute('aria-hidden', 'true');
        }}

        // Offline detection
        const offlineBanner = document.getElementById('offlineBanner');

        function updateOnlineStatus() {{
            if (navigator.onLine) {{
                offlineBanner.classList.remove('visible');
            }} else {{
                offlineBanner.classList.add('visible');
            }}
        }}

        window.addEventListener('online', updateOnlineStatus);
        window.addEventListener('offline', updateOnlineStatus);
        updateOnlineStatus();

        // Service Worker for offline support
        if ('serviceWorker' in navigator) {{
            // Create inline service worker using Blob URL
            const swCode = `
                const CACHE_NAME = 'hemlock-docs-v1';
                const urlsToCache = [self.location.href.replace('/sw.js', '/docs.html')];

                self.addEventListener('install', event => {{
                    event.waitUntil(
                        caches.open(CACHE_NAME)
                            .then(cache => cache.addAll(urlsToCache))
                            .then(() => self.skipWaiting())
                    );
                }});

                self.addEventListener('activate', event => {{
                    event.waitUntil(
                        caches.keys().then(cacheNames => {{
                            return Promise.all(
                                cacheNames.filter(name => name !== CACHE_NAME)
                                    .map(name => caches.delete(name))
                            );
                        }}).then(() => self.clients.claim())
                    );
                }});

                self.addEventListener('fetch', event => {{
                    event.respondWith(
                        caches.match(event.request)
                            .then(response => {{
                                if (response) {{
                                    // Return cached version and update in background
                                    fetch(event.request).then(freshResponse => {{
                                        if (freshResponse.ok) {{
                                            caches.open(CACHE_NAME).then(cache => {{
                                                cache.put(event.request, freshResponse);
                                            }});
                                        }}
                                    }}).catch(() => {{}});
                                    return response;
                                }}
                                return fetch(event.request).then(response => {{
                                    if (response.ok) {{
                                        const responseClone = response.clone();
                                        caches.open(CACHE_NAME).then(cache => {{
                                            cache.put(event.request, responseClone);
                                        }});
                                    }}
                                    return response;
                                }});
                            }})
                    );
                }});
            `;

            // Register service worker from blob
            const swBlob = new Blob([swCode], {{ type: 'application/javascript' }});
            const swUrl = URL.createObjectURL(swBlob);

            // Note: Blob URLs don't work for service workers in most browsers due to security
            // So we'll use a fallback approach - cache the page directly if possible
            try {{
                // Use Cache API directly for simple offline support
                if ('caches' in window) {{
                    caches.open('hemlock-docs-v1').then(cache => {{
                        // Cache the current page for offline access
                        cache.add(window.location.href).catch(() => {{}});
                    }});
                }}
            }} catch (e) {{
                console.log('Cache API not available');
            }}
        }}

        // Lazy content cache - parse markdown only when needed
        const contentCache = {{}};

        function getPageContent(pageId) {{
            if (contentCache[pageId]) {{
                return contentCache[pageId];
            }}
            const pageData = Object.values(PAGES).find(p => p.id === pageId);
            if (!pageData) return null;

            // Parse and cache the content
            let content = parseMarkdown(pageData.content);
            content = generateTOC(content);
            content += getEditLink(pageId);
            content += getPageNav(pageId);
            contentCache[pageId] = content;
            return content;
        }}

        // Mobile menu toggle
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');

        menuToggle.addEventListener('click', () => {{
            const isOpen = sidebar.classList.toggle('open');
            menuToggle.textContent = isOpen ? '\\u00d7' : '\\u2630';
            menuToggle.setAttribute('aria-expanded', isOpen);
        }});

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {{
            if (window.innerWidth < 1024) {{
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {{
                    sidebar.classList.remove('open');
                    menuToggle.textContent = '\\u2630';
                    menuToggle.setAttribute('aria-expanded', 'false');
                }}
            }}
        }});

        // Close sidebar with Escape key
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape' && sidebar.classList.contains('open')) {{
                sidebar.classList.remove('open');
                menuToggle.textContent = '\\u2630';
                menuToggle.setAttribute('aria-expanded', 'false');
                menuToggle.focus();
            }}
        }});

        // Dark mode toggle
        const themeToggle = document.getElementById('themeToggle');
        const sunIcon = themeToggle.querySelector('.sun-icon');
        const moonIcon = themeToggle.querySelector('.moon-icon');
        const themeText = themeToggle.querySelector('span');

        function setTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            if (theme === 'dark') {{
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
                themeText.textContent = 'Light';
            }} else {{
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
                themeText.textContent = 'Dark';
            }}
        }}

        // Initialize theme from localStorage or system preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {{
            setTheme(savedTheme);
        }} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            setTheme('dark');
        }}

        themeToggle.addEventListener('click', () => {{
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        }});

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {{
            if (!localStorage.getItem('theme')) {{
                setTheme(e.matches ? 'dark' : 'light');
            }}
        }});

        // Build page order for prev/next navigation
        const pageOrder = Object.values(PAGES).map(p => p.id);
        const pageInfo = {{}};
        Object.entries(PAGES).forEach(([title, data]) => {{
            pageInfo[data.id] = {{
                title: title.split(' -> ').pop(),
                fullTitle: title
            }};
        }});

        function getPageNav(currentPageId) {{
            const currentIndex = pageOrder.indexOf(currentPageId);
            const prevId = currentIndex > 0 ? pageOrder[currentIndex - 1] : null;
            const nextId = currentIndex < pageOrder.length - 1 ? pageOrder[currentIndex + 1] : null;

            let navHtml = '<nav class="page-nav" aria-label="Page navigation">';

            if (prevId) {{
                navHtml += `
                    <a href="#${{prevId}}" class="page-nav-link prev" data-page="${{prevId}}">
                        <span class="page-nav-label">\\u2190 Previous</span>
                        <span class="page-nav-title">${{escapeHtml(pageInfo[prevId].title)}}</span>
                    </a>
                `;
            }}

            if (nextId) {{
                navHtml += `
                    <a href="#${{nextId}}" class="page-nav-link next" data-page="${{nextId}}">
                        <span class="page-nav-label">Next \\u2192</span>
                        <span class="page-nav-title">${{escapeHtml(pageInfo[nextId].title)}}</span>
                    </a>
                `;
            }}

            navHtml += '</nav>';
            return navHtml;
        }}

        // Generate edit on GitHub link
        function getEditLink(pageId) {{
            // Map page ID to approximate file path in hemlock repo
            const parts = pageId.split('-');
            let path = '';

            if (pageId === 'language-reference') {{
                path = 'CLAUDE.md';
            }} else if (parts.length >= 2) {{
                const section = parts[0];
                const filename = parts.slice(1).join('-') + '.md';
                path = `docs/${{section}}/${{filename}}`;
            }} else {{
                return '';
            }}

            const githubIcon = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>';

            return `
                <a href="https://github.com/hemlang/hemlock/edit/main/${{path}}" class="edit-link" target="_blank" rel="noopener noreferrer">
                    ${{githubIcon}}
                    Edit this page on GitHub
                </a>
            `;
        }}

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

            for (let i = 0; i < lines.length; i++) {{
                let line = lines[i];

                if (line.startsWith('```')) {{
                    if (inCodeBlock) {{
                        const codeId = 'code-' + Math.random().toString(36).substr(2, 9);
                        const langDisplay = codeBlockLang || 'code';
                        const copyIcon = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>';
                        html += `<div class="code-block" role="region" aria-label="${{langDisplay}} code example">
                            <div class="code-header">
                                <span class="code-lang">${{langDisplay}}</span>
                                <button class="copy-btn" onclick="copyCode('${{codeId}}')" aria-label="Copy code to clipboard">${{copyIcon}}<span>Copy</span></button>
                            </div>
                            <pre><code id="${{codeId}}">` + escapeHtml(codeBlockContent) + '</code></pre></div>\\n';
                        codeBlockContent = '';
                        codeBlockLang = '';
                        inCodeBlock = false;
                    }} else {{
                        flushList();
                        flushBlockquote();
                        inCodeBlock = true;
                        codeBlockLang = line.substring(3).trim();
                    }}
                    continue;
                }}

                if (inCodeBlock) {{
                    codeBlockContent += line + '\\n';
                    continue;
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

            return html;
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        // Sanitize HTML to prevent XSS attacks
        function sanitizeHtml(html) {{
            // Create a temporary container
            const temp = document.createElement('div');
            temp.innerHTML = html;

            // Remove dangerous elements
            const dangerous = temp.querySelectorAll('script, iframe, object, embed, form, input, textarea, select, button:not(.copy-btn)');
            dangerous.forEach(el => el.remove());

            // Remove dangerous attributes from all elements
            const allElements = temp.querySelectorAll('*');
            allElements.forEach(el => {{
                // Remove event handlers
                const attrs = Array.from(el.attributes);
                attrs.forEach(attr => {{
                    if (attr.name.startsWith('on') ||
                        (attr.name === 'href' && attr.value.toLowerCase().startsWith('javascript:')) ||
                        (attr.name === 'src' && attr.value.toLowerCase().startsWith('javascript:'))) {{
                        el.removeAttribute(attr.name);
                    }}
                }});
            }});

            return temp.innerHTML;
        }}

        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');
        let selectedResultIndex = -1;

        // Build search index
        const searchIndex = Object.entries(PAGES).map(([title, data]) => ({{
            title: title.split(' -> ').pop(),
            fullTitle: title,
            id: data.id,
            content: data.content.toLowerCase(),
            rawContent: data.content
        }}));

        function performSearch(query) {{
            if (!query || query.length < 2) {{
                searchResults.classList.remove('active');
                return;
            }}

            const lowerQuery = query.toLowerCase();
            const results = searchIndex
                .map(page => {{
                    const titleMatch = page.title.toLowerCase().includes(lowerQuery);
                    const contentMatch = page.content.includes(lowerQuery);
                    if (!titleMatch && !contentMatch) return null;

                    // Find preview snippet
                    let preview = '';
                    if (contentMatch) {{
                        const idx = page.content.indexOf(lowerQuery);
                        const start = Math.max(0, idx - 40);
                        const end = Math.min(page.content.length, idx + query.length + 60);
                        preview = (start > 0 ? '...' : '') +
                                  page.rawContent.substring(start, end).replace(/\\n/g, ' ') +
                                  (end < page.content.length ? '...' : '');
                    }}

                    return {{
                        ...page,
                        preview,
                        score: titleMatch ? 2 : 1
                    }};
                }})
                .filter(Boolean)
                .sort((a, b) => b.score - a.score)
                .slice(0, 8);

            if (results.length === 0) {{
                searchResults.innerHTML = '<div class="no-results">No results found</div>';
            }} else {{
                searchResults.innerHTML = results.map((r, i) => `
                    <div class="search-result${{i === selectedResultIndex ? ' selected' : ''}}" data-page="${{r.id}}" role="option">
                        <div class="search-result-title">${{escapeHtml(r.title)}}</div>
                        ${{r.preview ? `<div class="search-result-preview">${{highlightMatch(r.preview, query)}}</div>` : ''}}
                    </div>
                `).join('');
            }}

            searchResults.classList.add('active');
            selectedResultIndex = -1;
        }}

        function highlightMatch(text, query) {{
            const escaped = escapeHtml(text);
            const regex = new RegExp(`(${{query.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
            return escaped.replace(regex, '<mark>$1</mark>');
        }}

        searchInput.addEventListener('input', (e) => {{
            performSearch(e.target.value);
        }});

        searchInput.addEventListener('keydown', (e) => {{
            const results = searchResults.querySelectorAll('.search-result');
            if (e.key === 'ArrowDown') {{
                e.preventDefault();
                selectedResultIndex = Math.min(selectedResultIndex + 1, results.length - 1);
                updateSelectedResult(results);
            }} else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                selectedResultIndex = Math.max(selectedResultIndex - 1, 0);
                updateSelectedResult(results);
            }} else if (e.key === 'Enter' && selectedResultIndex >= 0) {{
                e.preventDefault();
                const selected = results[selectedResultIndex];
                if (selected) {{
                    loadPage(selected.dataset.page);
                    searchInput.value = '';
                    searchResults.classList.remove('active');
                }}
            }} else if (e.key === 'Escape') {{
                searchResults.classList.remove('active');
                searchInput.blur();
            }}
        }});

        function updateSelectedResult(results) {{
            results.forEach((r, i) => {{
                r.classList.toggle('selected', i === selectedResultIndex);
            }});
        }}

        searchResults.addEventListener('click', (e) => {{
            const result = e.target.closest('.search-result');
            if (result) {{
                loadPage(result.dataset.page);
                searchInput.value = '';
                searchResults.classList.remove('active');
            }}
        }});

        // Close search results when clicking outside
        document.addEventListener('click', (e) => {{
            if (!e.target.closest('.search-box')) {{
                searchResults.classList.remove('active');
            }}
        }});

        // Keyboard shortcut for search (Cmd+K or Ctrl+K)
        document.addEventListener('keydown', (e) => {{
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
                e.preventDefault();
                searchInput.focus();
                searchInput.select();
            }}
        }});

        // Generate Table of Contents
        function generateTOC(html) {{
            const temp = document.createElement('div');
            temp.innerHTML = html;
            const headings = temp.querySelectorAll('h2, h3');

            if (headings.length < 3) return html; // Don't show TOC for short pages

            let tocItems = [];
            headings.forEach(h => {{
                const level = h.tagName.toLowerCase();
                const text = h.textContent;
                const id = h.id;
                tocItems.push(`<li><a href="#${{id}}" class="toc-${{level}}">${{escapeHtml(text)}}</a></li>`);
            }});

            const tocHtml = `
                <nav class="toc" aria-label="Table of Contents">
                    <div class="toc-title">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
                        </svg>
                        On this page
                    </div>
                    <ul class="toc-list">
                        ${{tocItems.join('\\n')}}
                    </ul>
                </nav>
            `;

            // Insert TOC after first h1
            const h1 = temp.querySelector('h1');
            if (h1) {{
                h1.insertAdjacentHTML('afterend', tocHtml);
            }} else {{
                temp.insertAdjacentHTML('afterbegin', tocHtml);
            }}

            return temp.innerHTML;
        }}

        // Syntax highlighting
        function highlightSyntax(lang, code) {{
            if (!lang) return code;

            const langLower = lang.toLowerCase();

            // Define language-specific patterns
            const patterns = {{
                hemlock: [
                    [/\\/\\/.*$/gm, 'comment'],
                    [/\\/\\*[\\s\\S]*?\\*\\//g, 'comment'],
                    [/"(?:[^"\\\\]|\\\\.)*"/g, 'string'],
                    [/'(?:[^'\\\\]|\\\\.)*'/g, 'string'],
                    [/\\b(fn|let|mut|if|else|while|for|in|return|match|struct|enum|impl|trait|pub|use|mod|const|type|self|true|false|nil|and|or|not)\\b/g, 'keyword'],
                    [/\\b(i8|i16|i32|i64|u8|u16|u32|u64|f32|f64|bool|str|char|void|any)\\b/g, 'type'],
                    [/\\b\\d+\\.?\\d*\\b/g, 'number'],
                    [/\\b([A-Z][a-zA-Z0-9_]*)\\b/g, 'type'],
                    [/\\b([a-z_][a-zA-Z0-9_]*)\\s*\\(/g, 'function'],
                    [/[+\\-*\\/%=<>!&|^~]+/g, 'operator'],
                    [/[{{}}\\[\\]();,.:]/g, 'punctuation'],
                ],
                javascript: [
                    [/\\/\\/.*$/gm, 'comment'],
                    [/\\/\\*[\\s\\S]*?\\*\\//g, 'comment'],
                    [/"(?:[^"\\\\]|\\\\.)*"/g, 'string'],
                    [/'(?:[^'\\\\]|\\\\.)*'/g, 'string'],
                    [/`(?:[^`\\\\]|\\\\.)*`/g, 'string'],
                    [/\\b(const|let|var|function|return|if|else|for|while|do|switch|case|break|continue|try|catch|throw|new|class|extends|import|export|default|async|await|typeof|instanceof)\\b/g, 'keyword'],
                    [/\\b(true|false|null|undefined|NaN|Infinity)\\b/g, 'builtin'],
                    [/\\b\\d+\\.?\\d*\\b/g, 'number'],
                    [/\\b([a-z_][a-zA-Z0-9_]*)\\s*\\(/g, 'function'],
                    [/[+\\-*\\/%=<>!&|^~?:]+/g, 'operator'],
                ],
                python: [
                    [/#.*$/gm, 'comment'],
                    [/\\"\\"\\"[\\s\\S]*?\\"\\"\\"/g, 'string'],
                    [/\\'\\'\\'[\\s\\S]*?\\'\\'\\']/g, 'string'],
                    [/"(?:[^"\\\\]|\\\\.)*"/g, 'string'],
                    [/'(?:[^'\\\\]|\\\\.)*'/g, 'string'],
                    [/\\b(def|class|if|elif|else|for|while|try|except|finally|with|return|yield|import|from|as|pass|break|continue|raise|lambda|and|or|not|in|is|True|False|None)\\b/g, 'keyword'],
                    [/\\b\\d+\\.?\\d*\\b/g, 'number'],
                    [/\\b([a-z_][a-zA-Z0-9_]*)\\s*\\(/g, 'function'],
                ],
                bash: [
                    [/#.*$/gm, 'comment'],
                    [/"(?:[^"\\\\]|\\\\.)*"/g, 'string'],
                    [/'[^']*'/g, 'string'],
                    [/\\b(if|then|else|elif|fi|for|while|do|done|case|esac|function|return|exit|echo|cd|ls|cat|grep|sed|awk|export|source)\\b/g, 'keyword'],
                    [/\\$[a-zA-Z_][a-zA-Z0-9_]*/g, 'property'],
                    [/\\$\\{{[^}}]+\\}}/g, 'property'],
                ],
                json: [
                    [/"(?:[^"\\\\]|\\\\.)*"\\s*:/g, 'property'],
                    [/"(?:[^"\\\\]|\\\\.)*"/g, 'string'],
                    [/\\b(true|false|null)\\b/g, 'keyword'],
                    [/\\b-?\\d+\\.?\\d*\\b/g, 'number'],
                ]
            }};

            // Use hemlock patterns for hml
            const langPatterns = patterns[langLower] || patterns[langLower === 'hml' ? 'hemlock' : langLower] || patterns.hemlock;

            // Apply patterns in order
            let tokens = [];
            let remaining = code;

            // Simple tokenization - find all matches and sort by position
            langPatterns.forEach(([regex, type]) => {{
                let match;
                const re = new RegExp(regex.source, regex.flags);
                while ((match = re.exec(code)) !== null) {{
                    tokens.push({{
                        start: match.index,
                        end: match.index + match[0].length,
                        text: match[0],
                        type: type
                    }});
                }}
            }});

            // Sort by start position and remove overlaps
            tokens.sort((a, b) => a.start - b.start);
            let filtered = [];
            let lastEnd = 0;
            tokens.forEach(t => {{
                if (t.start >= lastEnd) {{
                    filtered.push(t);
                    lastEnd = t.end;
                }}
            }});

            // Build highlighted HTML
            let result = '';
            let pos = 0;
            filtered.forEach(t => {{
                if (t.start > pos) {{
                    result += escapeHtml(code.substring(pos, t.start));
                }}
                result += `<span class="token-${{t.type}}">${{escapeHtml(t.text)}}</span>`;
                pos = t.end;
            }});
            if (pos < code.length) {{
                result += escapeHtml(code.substring(pos));
            }}

            return result;
        }}

        // Apply syntax highlighting to code blocks after page load
        function applySyntaxHighlighting() {{
            document.querySelectorAll('.code-block').forEach(block => {{
                const langSpan = block.querySelector('.code-lang');
                const codeEl = block.querySelector('code');
                if (langSpan && codeEl && !codeEl.dataset.highlighted) {{
                    const lang = langSpan.textContent;
                    const code = codeEl.textContent;
                    codeEl.innerHTML = highlightSyntax(lang, code);
                    codeEl.dataset.highlighted = 'true';
                }}
            }});
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
            showLoading();

            // Use requestAnimationFrame for smooth rendering
            requestAnimationFrame(() => {{
                const pageData = Object.values(PAGES).find(p => p.id === pageId);
                if (!pageData) {{
                    console.error('Page not found:', pageId);
                    document.getElementById('content').innerHTML = '<p>Page not found. Please select a page from the navigation menu.</p>';
                    hideLoading();
                    return;
                }}

                // Use cached content or generate new
                let content = getPageContent(pageId);
                if (!content) {{
                    hideLoading();
                    return;
                }}

                // Sanitize content before inserting to prevent XSS
                document.getElementById('content').innerHTML = sanitizeHtml(content);
                // Apply syntax highlighting to code blocks
                applySyntaxHighlighting();

                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(link => {{
                    link.classList.remove('active');
                    if (link.dataset.page === pageId) {{
                        link.classList.add('active');
                    }}
                }});

                // Setup TOC smooth scrolling
                document.querySelectorAll('.toc-list a').forEach(link => {{
                    link.addEventListener('click', (e) => {{
                        e.preventDefault();
                        const targetId = link.getAttribute('href').substring(1);
                        const target = document.getElementById(targetId);
                        if (target) {{
                            target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                            history.pushState(null, '', '#' + pageId);
                        }}
                    }});
                }});

                // Setup prev/next navigation
                document.querySelectorAll('.page-nav-link').forEach(link => {{
                    link.addEventListener('click', (e) => {{
                        e.preventDefault();
                        const targetPage = link.dataset.page;
                        if (targetPage) {{
                            loadPage(targetPage);
                        }}
                    }});
                }});

                // Scroll to top
                window.scrollTo(0, 0);

                // Update URL hash
                window.location.hash = pageId;

                // Hide loading indicator
                hideLoading();
            }});
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

        // Load initial page
        const initialHash = window.location.hash.substring(1);
        const firstPageId = Object.values(PAGES)[0].id;
        loadPage(initialHash || firstPageId);
    </script>
</body>
</html>'''

    return html


def main():
    """Main build function."""
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

    # Collect documentation
    print("Collecting documentation files...")
    docs = collect_docs()
    if not docs:
        print("Error: No documentation pages found")
        sys.exit(1)
    print(f"Found {len(docs)} documentation pages")

    # Encode logo
    print("Encoding logo...")
    logo_path = HEMLOCK_DIR / 'logo.png'
    logo_data = encode_image(logo_path) if logo_path.exists() else ""
    if not logo_data:
        print("Warning: logo.png not found, continuing without logo")

    # Generate HTML
    print("Generating HTML...")
    html = generate_html(docs, logo_data)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Documentation built: {OUTPUT_FILE}")
    print(f"  - {len(docs)} pages")
    print(f"  - Open docs.html in your browser to view")


if __name__ == '__main__':
    main()
