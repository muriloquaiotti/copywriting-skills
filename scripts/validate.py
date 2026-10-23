#!/usr/bin/env python3
"""Check the portable package, internal links, book coverage, and provenance."""
from pathlib import Path
import json
import re
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    skill = root / 'skills' / 'copywriting'
    errors = []
    links = 0
    markdown = []
    for directory in [root / 'skills', root / 'examples']:
        markdown.extend(directory.rglob('*.md'))
    markdown += [root / 'README.md', root / 'AGENTS.md']
    for path in markdown:
        if path.is_symlink():
            errors.append(f'Symlink is not portable: {path.relative_to(root)}')
        text = path.read_text(encoding='utf-8')
        if re.search(r'/Users/|file://|\.book-to-skill-work', text):
            errors.append(f'Local dependency: {path.relative_to(root)}')
        for raw in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in raw or raw.startswith('#'):
                continue
            target = raw.split('#', 1)[0].strip('<>')
            resolved = (path.parent / target).resolve()
            links += 1
            if not resolved.exists() or not resolved.is_relative_to(root):
                errors.append(f'Invalid local link: {path.relative_to(root)} -> {raw}')
    expected = {'breakthrough-advertising': range(1, 15), 'great-leads': range(1, 11),
                'copy-logic': range(1, 10), '100m-offers': range(1, 18),
                'quick-start-copywriting': range(15, 24)}
    chapter_count = 0
    for slug, numbers in expected.items():
        book = skill / 'references' / 'books' / slug
        chapters = list((book / 'chapters').glob('ch*.md'))
        chapter_count += len(chapters)
        if sorted(int(p.name[2:4]) for p in chapters) != list(numbers):
            errors.append(f'Incomplete chapter coverage: {slug}')
        manifest = json.loads((book / 'sources.json').read_text())
        if not re.fullmatch('[a-f0-9]{64}', manifest['source_sha256']):
            errors.append(f'Invalid source fingerprint: {slug}')
        for item in manifest['coverage']:
            pages = [int(n) for n in re.split('[–-]', item['pdf_pages'])]
            if not 1 <= min(pages) <= max(pages) <= manifest['pdf_pages']:
                errors.append(f'Invalid page range: {slug}')
    for path in skill.rglob('*'):
        if path.is_symlink() or path.suffix.lower() in {'.pdf', '.csv', '.xlsx', '.zip'}:
            errors.append(f'Unexpected artifact: {path.relative_to(root)}')
    if len(list(skill.rglob('SKILL.md'))) != 1:
        errors.append('The self-contained skill must have a single SKILL.md entrypoint')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Package valid: {len(markdown)} Markdown files, {links} local links, {chapter_count} chapter references.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
