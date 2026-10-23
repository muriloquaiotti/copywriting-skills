#!/usr/bin/env python3
"""Install the self-contained skill; never silently overwrite an existing copy."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys
import tempfile


def same_tree(left: Path, right: Path) -> bool:
    if right.is_symlink() or not right.is_dir():
        return False
    def files(root: Path):
        return {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    return files(left) == files(right)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['user', 'project'], required=True)
    parser.add_argument('--project', type=Path, help='Existing project directory; required for project scope')
    parser.add_argument('--replace', action='store_true', help='Back up and replace a different existing installation')
    args = parser.parse_args()
    if args.scope == 'project':
        if args.project is not None:
            args.project = args.project.expanduser()
        if args.project is None or not args.project.is_dir():
            parser.error('--project must name an existing project directory')
        base = args.project.expanduser().resolve() / '.agents'
    else:
        if args.project is not None:
            parser.error('--project only applies to project scope')
        base = Path.home() / '.agents'
    source = Path(__file__).resolve().parents[1] / 'skills' / 'copywriting'
    if not (source / 'SKILL.md').is_file():
        parser.error('Source skill is missing')
    target = base / 'skills' / 'copywriting'
    if target.resolve() == source.resolve():
        print(f'Already points to the source: {target}')
        return 0
    if target.exists() or target.is_symlink():
        if same_tree(source, target):
            print(f'Already up to date: {target}')
            return 0
        if not args.replace:
            print(f'Existing installation preserved: {target}. Compare it first; use --replace to back it up and replace it.', file=sys.stderr)
            return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.copywriting-install-', dir=base))
    backup = None
    try:
        payload = staging / 'copywriting'
        shutil.copytree(source, payload)
        if target.exists() or target.is_symlink():
            backup_root = base / 'skill-backups'
            backup_root.mkdir(exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = backup_root / f'copywriting-{stamp}'
            # Preserve the content of relative symlinks when moving out of their parent.
            if target.is_symlink():
                backup.symlink_to(target.resolve(), target_is_directory=True)
                target.unlink()
            else:
                target.rename(backup)
        try:
            payload.rename(target)
        except OSError:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
        print(f'Installed: {target}')
        if backup is not None:
            print(f'Previous installation preserved: {backup}')
    finally:
        shutil.rmtree(staging)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
