import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "caseforge"


def run(*args):
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_version():
    result = run("--version")
    assert result.returncode == 0
    assert "CaseForge 0.1.0" in result.stdout


def test_new_and_collect(tmp_path):
    case = tmp_path / "case"
    created = run("new", "incident", "-o", str(case))
    assert created.returncode == 0
    assert (case / "case.json").is_file()

    collected = run("collect", str(case), "--modules", "system,process,network,users")
    assert collected.returncode == 0

    manifest = json.loads((case / "manifest.json").read_text())
    assert [x["category"] for x in manifest["artifacts"]] == ["system", "process", "network", "users"]
    assert all(len(x["sha256"]) == 64 for x in manifest["artifacts"])


def test_timeline_report_verify(tmp_path):
    case = tmp_path / "case"
    assert run("new", "timeline-test", "-o", str(case)).returncode == 0
    assert run("collect", str(case), "--modules", "system,process").returncode == 0

    timeline = run("timeline", str(case))
    report = run("report", str(case))
    verify = run("verify", str(case))

    assert timeline.returncode == 0
    assert report.returncode == 0
    assert verify.returncode == 0
    assert (case / "timeline.json").is_file()
    assert (case / "report.md").is_file()
    assert "integrity OK" in verify.stdout


def test_ioc_scan(tmp_path):
    case = tmp_path / "case"
    assert run("new", "ioc-test", "-o", str(case)).returncode == 0
    assert run("collect", str(case), "--modules", "system").returncode == 0

    evidence = case / "evidence" / "0001_system.json"
    data = json.loads(evidence.read_text())
    data["marker"] = "203.0.113.10"
    evidence.write_text(json.dumps(data))

    iocs = tmp_path / "iocs.txt"
    iocs.write_text("203.0.113.10\n")
    result = run("ioc", str(case), str(iocs))
    assert result.returncode == 0
    matches = json.loads((case / "iocs.json").read_text())["matches"]
    assert any(item["ioc"] == "203.0.113.10" for item in matches)


def test_export(tmp_path):
    case = tmp_path / "case"
    archive = tmp_path / "case.zip"
    assert run("new", "export-test", "-o", str(case)).returncode == 0
    assert run("collect", str(case), "--modules", "system").returncode == 0
    result = run("export", str(case), "-o", str(archive))
    assert result.returncode == 0
    assert archive.is_file()
    assert archive.stat().st_size > 0
