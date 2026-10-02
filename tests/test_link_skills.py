"""Integration checks use temporary destinations; never change real agent installs."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'bin/link-skills.py'
SOURCE = SCRIPT.parent.parent / 'skills'
NAMES = ('context-specific-evaluation', 'evaluation-orchestrator', 'rapid-ontology-modeling')


class LinkSkillsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='skills test ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.codex = self.root / 'codex'
        self.claude = self.root / 'claude'

    def run_link(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), '--codex-dir', str(self.codex),
                               '--claude-dir', str(self.claude), *extra],
                              text=True, capture_output=True)

    def test_dry_run_does_not_create_destinations(self):
        self.assertEqual(self.run_link().returncode, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_apply_is_idempotent_and_links_complete_skills(self):
        self.assertEqual(self.run_link('--apply').returncode, 0)
        for target in (self.codex, self.claude):
            self.assertEqual(sorted(p.name for p in target.iterdir()), list(NAMES))
            for name in NAMES:
                self.assertTrue((target / name).is_symlink())
                self.assertEqual((target / name).resolve(), SOURCE / 'meta' / name)
                self.assertEqual((target / name / 'SKILL.md').read_bytes(),
                                 (SOURCE / 'meta' / name / 'SKILL.md').read_bytes())
        second = self.run_link('--apply')
        self.assertEqual(second.returncode, 0)
        self.assertIn('Created 0 links.', second.stdout)

    def test_existing_directory_blocks_entire_batch_and_preserves_content(self):
        existing = self.claude / NAMES[0]
        existing.mkdir(parents=True)
        (existing / 'local-change').write_text('keep me')
        self.assertNotEqual(self.run_link('--apply').returncode, 0)
        self.assertFalse(self.codex.exists())
        self.assertEqual((existing / 'local-change').read_text(), 'keep me')
        self.assertEqual(list(self.claude.iterdir()), [existing])

    def test_broken_symlink_is_preserved(self):
        self.codex.mkdir()
        link = self.codex / NAMES[0]
        link.symlink_to(self.root / 'missing')
        self.assertNotEqual(self.run_link('--apply').returncode, 0)
        self.assertEqual(os.readlink(link), str(self.root / 'missing'))
        self.assertFalse(self.claude.exists())

    def test_single_target(self):
        self.assertEqual(self.run_link('--apply', '--target', 'claude').returncode, 0)
        self.assertFalse(self.codex.exists())
        self.assertTrue(self.claude.is_dir())

    def test_invalid_parent_blocks_before_writing_other_target(self):
        self.claude.write_text('keep')
        self.assertNotEqual(self.run_link('--apply').returncode, 0)
        self.assertFalse(self.codex.exists())
        self.assertEqual(self.claude.read_text(), 'keep')

    def test_source_cannot_be_destination(self):
        result = self.run_link('--apply', '--codex-dir', str(SOURCE / 'meta'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('inside the source tree', result.stderr)
        self.assertFalse(self.claude.exists())

    def test_codex_home_default(self):
        env = dict(os.environ, CODEX_HOME=str(self.root / 'custom-codex'))
        result = subprocess.run([sys.executable, str(SCRIPT), '--apply', '--target', 'codex'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((self.root / 'custom-codex/skills').iterdir())), 3)


if __name__ == '__main__':
    unittest.main()
