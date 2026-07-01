import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from issue_parser import parse_issue, IssueParseError
from schedule import load_schedule, valid_day, get_day
from question_writer import render_questions

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_PATH = REPO_ROOT / "curriculum" / "schedule.yml"
TEMPLATE_PATH = REPO_ROOT / "templates" / "questions-template.md"


def _append_output(gh_output, name, value):
    if not gh_output:
        return
    with open(gh_output, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def _read_issue_body(event_path):
    if not event_path or not Path(event_path).exists():
        raise RuntimeError("이벤트 파일이 없습니다.")
    with open(event_path, encoding="utf-8") as f:
        return json.load(f)["issue"]["body"]


def generate(repo_root=None, event_path=None, gh_output=None):
    repo_root = Path(repo_root) if repo_root else REPO_ROOT
    event_path = event_path or os.environ.get("GITHUB_EVENT_PATH")
    gh_output = gh_output or os.environ.get("GITHUB_OUTPUT")
    schedule_path = repo_root / "curriculum" / "schedule.yml"
    template_path = repo_root / "templates" / "questions-template.md"

    try:
        body = _read_issue_body(event_path)
        parsed = parse_issue(body)
    except (IssueParseError, RuntimeError, KeyError) as e:
        _append_output(gh_output, "message", f"❌ 파싱 실패: {e}")
        return 1

    schedule = load_schedule(schedule_path)
    if not valid_day(schedule, parsed["week"], parsed["day"]):
        _append_output(gh_output, "message", f"❌ 잘못된 주차/일자: {parsed['week']}/{parsed['day']}")
        return 1

    day_info = get_day(schedule, parsed["week"], parsed["day"])
    target_dir = repo_root / "weeks" / parsed["week"] / parsed["day"]
    target_file = target_dir / "questions.md"
    if target_file.exists():
        rel = target_file.relative_to(repo_root).as_posix()
        _append_output(gh_output, "message", f"❌ 이미 질문이 존재합니다: {rel}")
        return 1

    content = render_questions(day_info, parsed["questions"], template_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")
    rel = target_file.relative_to(repo_root).as_posix()
    _append_output(gh_output, "message", f"✅ 질문 생성 완료: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(generate())
