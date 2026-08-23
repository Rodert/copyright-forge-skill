from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "copyright-forge" / "scripts" / "validate_profile.py"


class ProfileValidationTest(unittest.TestCase):
    def test_unconfirmed_user_facts_block_ready_state(self) -> None:
        profile = ROOT / "skills" / "copyright-forge" / "assets" / "templates" / "software-profile.yaml"
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "profile-report.json"
            subprocess.run([sys.executable, str(SCRIPT), str(profile), "--output", str(report)], check=True)
            result = json.loads(report.read_text())
            self.assertEqual("NEEDS_CONFIRMATION", result["status"])
            self.assertGreater(len(result["blockers"]), 0)


if __name__ == "__main__":
    unittest.main()
