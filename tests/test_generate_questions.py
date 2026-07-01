import json
from pathlib import Path

import generate_questions

SCHEDULE_YML = Path(__file__).resolve().parents[1] / "curriculum" / "schedule.yml"
TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "questions-template.md"


def _write_event(tmp_path, week, day, questions):
    body = f"### 주차\n\n{week}\n\n### 일자\n\n{day}\n\n### 질문\n\n{questions}\n"
    event = {"issue": {"body": body}}
    event_path = tmp_path / "event.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")
    return event_path


def _setup_repo(tmp_path):
    root = tmp_path / "repo"
    (root / "curriculum").mkdir(parents=True)
    (root / "curriculum" / "schedule.yml").write_text(
        (Path(__file__).resolve().parents[1] / "curriculum" / "schedule.yml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (root / "templates").mkdir(parents=True)
    (root / "templates" / "questions-template.md").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    return root


def test_generate_creates_file(tmp_path):
    root = _setup_repo(tmp_path)
    event_path = _write_event(tmp_path, "week-01", "day-1", "## Q1. 프로세스란?")
    out_file = tmp_path / "out.txt"
    rc = generate_questions.generate(str(root), str(event_path), str(out_file))
    created = (root / "weeks" / "week-01" / "day-1" / "questions.md").read_text(encoding="utf-8")
    assert rc == 0
    assert "# 운영체제 - 프로세스와 스레드" in created
    assert "## Q1. 프로세스란?" in created
    assert "message=✅" in out_file.read_text(encoding="utf-8")


def test_generate_rejects_invalid_day(tmp_path):
    root = _setup_repo(tmp_path)
    event_path = _write_event(tmp_path, "week-99", "day-1", "질문")
    out_file = tmp_path / "out.txt"
    rc = generate_questions.generate(str(root), str(event_path), str(out_file))
    assert rc == 1
    assert "week-99" in out_file.read_text(encoding="utf-8")
    assert not (root / "weeks").exists() or not list((root / "weeks").glob("**/questions.md"))


def test_generate_rejects_duplicate(tmp_path):
    root = _setup_repo(tmp_path)
    event_path = _write_event(tmp_path, "week-01", "day-1", "## Q1")
    out_file = tmp_path / "out.txt"
    generate_questions.generate(str(root), str(event_path), str(out_file))
    rc2 = generate_questions.generate(str(root), str(event_path), str(out_file))
    assert rc2 == 1
    assert "이미 질문이 존재" in out_file.read_text(encoding="utf-8")
