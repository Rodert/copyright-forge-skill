from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "copyright-forge" / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "sample-go"


def run(script: str, *args: str) -> None:
    subprocess.run([sys.executable, str(SCRIPTS / script), *args], check=True)


class CopyrightForgeScriptsTest(unittest.TestCase):
    def test_project_analysis_and_source_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            scan, evidence, manifest = output / "scan.json", output / "evidence.json", output / "manifest.json"
            run("scan_project.py", str(FIXTURE), "--output", str(scan))
            run("build_evidence_map.py", str(FIXTURE), "--output", str(evidence))
            run("collect_source.py", str(FIXTURE), "--output", str(manifest))
            self.assertIn("Go", json.loads(scan.read_text())["languages"])
            self.assertGreater(len(json.loads(evidence.read_text())["features"]), 0)
            self.assertEqual([item["path"] for item in json.loads(manifest.read_text())["files"]], ["main.go", "config.go"])

    def test_redaction_writes_a_separate_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            report, redacted = output / "security.json", output / "redacted"
            run("detect_secrets.py", str(FIXTURE), "--output", str(report), "--redact-to", str(redacted))
            self.assertGreater(json.loads(report.read_text())["finding_count"], 0)
            self.assertIn("[REDACTED]", (redacted / "config.go").read_text())
            self.assertIn("sk_example", (FIXTURE / "config.go").read_text())


if __name__ == "__main__":
    unittest.main()
