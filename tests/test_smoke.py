"""Scaffold smoke tests: modules import and entry points answer. Product behaviour is tested by tickets."""

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ["darkroom", "darkroom.dng", "darkroom.engine", "darkroom.store", "darkroom.png", "darkroom.server"]


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, timeout=30)


class ImportSmoke(unittest.TestCase):
    def test_modules_import(self):
        for name in MODULES:
            with self.subTest(module=name):
                self.assertIsNotNone(importlib.import_module(name).__doc__)


class EntryPointSmoke(unittest.TestCase):
    def test_darkroom_version_and_help(self):
        self.assertIn("darkroom 0.0.0", run("-m", "darkroom", "--version").stdout)
        self.assertIn("--data-dir", run("-m", "darkroom", "--help").stdout)

    def test_darkroom_not_implemented(self):
        result = run("-m", "darkroom")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not implemented yet: see #15", result.stderr)

    def test_fixture_tool_help_and_not_implemented(self):
        self.assertIn("--out", run("tools/make_fixtures.py", "--help").stdout)
        result = run("tools/make_fixtures.py", "--out", "unused")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not implemented yet: see #11", result.stderr)


if __name__ == "__main__":
    unittest.main()
