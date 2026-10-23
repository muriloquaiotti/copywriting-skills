#!/usr/bin/env python3
"""Exercise installation and preservation of existing user files in temporary projects."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('install.py').resolve()
SOURCE = SCRIPT.parents[1] / 'skills' / 'copywriting'


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='copywriting-install-test-')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'projeto com espaços'
        self.project.mkdir()
        self.target = self.project / '.agents' / 'skills' / 'copywriting'

    def install(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--scope', 'project', '--project', str(self.project), *args], capture_output=True, text=True)

    def test_fresh_and_idempotent_install(self):
        first = self.install()
        self.assertEqual(first.returncode, 0, first.stderr)
        for source in SOURCE.rglob('*'):
            if source.is_file():
                self.assertEqual(source.read_bytes(), (self.target / source.relative_to(SOURCE)).read_bytes())
        stamp = (self.target / 'SKILL.md').stat().st_mtime_ns
        second = self.install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(stamp, (self.target / 'SKILL.md').stat().st_mtime_ns)

    def test_existing_copy_is_preserved(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('Versão personalizada')
        result = self.install()
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.target / 'SKILL.md').read_text(), 'Versão personalizada')

    def test_replace_backs_up_all_previous_files(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_text('Versão personalizada')
        (self.target / 'anotacoes.txt').write_text('Notas do usuário')
        result = self.install('--replace')
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.project / '.agents' / 'skill-backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'anotacoes.txt').read_text(), 'Notas do usuário')
        self.assertEqual((backups[0] / 'SKILL.md').read_text(), 'Versão personalizada')
        self.assertEqual((self.target / 'SKILL.md').read_bytes(), (SOURCE / 'SKILL.md').read_bytes())
        self.assertFalse((self.target / 'anotacoes.txt').exists())

    def test_relative_symlink_backup_keeps_target(self):
        old = self.project / '.agents' / 'custom'
        old.mkdir(parents=True)
        (old / 'SKILL.md').write_text('Skill externa')
        self.target.parent.mkdir()
        self.target.symlink_to('../custom', target_is_directory=True)
        result = self.install('--replace')
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = next((self.project / '.agents' / 'skill-backups').iterdir())
        self.assertEqual(backup.resolve(), old.resolve())
        self.assertEqual((old / 'SKILL.md').read_text(), 'Skill externa')
        self.assertFalse(self.target.is_symlink())


if __name__ == '__main__':
    unittest.main()
