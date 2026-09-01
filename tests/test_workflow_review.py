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


def run(script: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], check=check, capture_output=True, text=True)


def profile() -> dict:
    def confirmed(value: str) -> dict:
        return {"value": value, "source": ["user"], "confidence": "high", "requires_confirmation": True, "status": "confirmed"}
    return {
        "schema_version": "2.0",
        "software": {"full_name": confirmed("示例服务系统"), "short_name": confirmed("示例服务"), "version": confirmed("V1.0")},
        "applicant": confirmed("示例科技有限公司"),
        "copyright": {"development_method": confirmed("自行开发"), "rights_acquisition": confirmed("原始取得")},
        "dates": {"completion_date": confirmed("2026-01-01"), "publication_status": confirmed("未公开使用")},
        "technology": {},
        "features": ["user-service"],
        "status": {"profile_confirmed": True},
    }


class WorkflowAndReviewTest(unittest.TestCase):
    def test_source_builder_creates_valid_ordinary_deposit_page_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            output.mkdir()
            manifest = output / "manifest.json"
            manifest.write_text(json.dumps({"files": [{"path": "main.go"}, {"path": "config.go"}]}), encoding="utf-8")
            selection = output / "selection.json"
            run("select_source_material.py", str(FIXTURE), str(manifest), "--output", str(selection))
            profile_path = output / "software-profile.json"
            profile_path.write_text(json.dumps(profile(), ensure_ascii=False), encoding="utf-8")
            pages = output / "pages"
            run("build_source_pages.py", str(FIXTURE), str(selection), str(profile_path), "--output-dir", str(pages))
            report = output / "source-validation.json"
            run("validate_source_pages.py", str(pages / "source-pages.json"), "--output", str(report))
            self.assertEqual("READY", json.loads(report.read_text())["status"])
            self.assertIn("示例服务系统", (pages / "source-material.txt").read_text())
            docx = output / "source-material.docx"
            run("render_source_docx.py", str(pages / "source-material.txt"), "--output", str(docx))
            self.assertTrue(docx.exists())

    def test_rules_radar_is_non_blocking_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "rules.json"
            registry = ROOT / "skills" / "copyright-forge" / "references" / "official" / "source-registry.yaml"
            run("check_rules.py", str(registry), "--output", str(report))
            self.assertEqual("REVIEW_REQUIRED", json.loads(report.read_text())["status"])

    def test_locked_facts_and_evidence_backed_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            profile_path = output / "software-profile.json"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text(json.dumps(profile(), ensure_ascii=False), encoding="utf-8")
            evidence = {"schema_version": "2.0", "project": str(FIXTURE), "features": [{"id": "user-service", "name": "用户服务", "claim_status": "approved", "confidence": "high", "evidence": [{"type": "route", "path": "main.go"}]}]}
            evidence_path = output / "evidence-map.json"
            evidence_path.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")
            run("manage_task.py", "init", str(FIXTURE), str(output))
            run("manage_task.py", "lock", str(output), "--profile", str(profile_path))
            run("manage_task.py", "transition", str(output), "GENERATING")
            run("manage_task.py", "transition", str(output), "REVIEWING")
            materials = output / "materials"
            materials.mkdir()
            (materials / "manual.md").write_text("示例服务系统\nV1.0\n示例科技有限公司\n用户服务\n", encoding="utf-8")
            report = output / "review.json"
            run("review_materials.py", str(profile_path), str(evidence_path), str(materials), "--task-dir", str(output), "--output", str(report))
            self.assertEqual("READY", json.loads(report.read_text())["status"])
            quality_html = output / "quality-report.html"
            run("render_quality_report.py", str(report), "--output", str(quality_html))
            self.assertIn("材料质量报告", quality_html.read_text())

    def test_review_blocks_feature_outside_locked_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            profile_path = output / "software-profile.json"
            profile_path.parent.mkdir(parents=True)
            data = profile()
            data["features"] = []
            profile_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            evidence_path = output / "evidence-map.json"
            evidence_path.write_text(json.dumps({"schema_version": "2.0", "project": str(FIXTURE), "features": [{"id": "user-service", "name": "用户服务", "claim_status": "approved", "confidence": "high", "evidence": [{"type": "route", "path": "main.go"}]}]}), encoding="utf-8")
            run("manage_task.py", "init", str(FIXTURE), str(output))
            run("manage_task.py", "lock", str(output), "--profile", str(profile_path))
            run("manage_task.py", "transition", str(output), "GENERATING")
            run("manage_task.py", "transition", str(output), "REVIEWING")
            materials = output / "materials"
            materials.mkdir()
            (materials / "manual.md").write_text("示例服务系统 V1.0 示例科技有限公司 用户服务", encoding="utf-8")
            report = output / "review.json"
            run("review_materials.py", str(profile_path), str(evidence_path), str(materials), "--task-dir", str(output), "--output", str(report))
            codes = {item["code"] for item in json.loads(report.read_text())["blockers"]}
            self.assertIn("UNSUPPORTED_CLAIM", codes)


if __name__ == "__main__":
    unittest.main()
