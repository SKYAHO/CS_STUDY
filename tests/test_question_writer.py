from pathlib import Path
import question_writer

TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "questions-template.md"

DAY_INFO = {
    "week_id": "week-01",
    "topic": "운영체제",
    "day_id": "day-1",
    "subtopic": "프로세스와 스레드",
}


def test_renders_basic_fields():
    out = question_writer.render_questions(DAY_INFO, "Q1. 질문", TEMPLATE)
    assert "# 운영체제 - 프로세스와 스레드" in out
    assert "week-01" in out and "day-1" in out
    assert "Q1. 질문" in out


def test_renders_questions_with_braces_safely():
    out = question_writer.render_questions(DAY_INFO, "코드: { x: 1 }", TEMPLATE)
    assert "코드: { x: 1 }" in out


def test_multiline_questions_preserved():
    md = "## Q1\n내용1\n\n## Q2\n내용2"
    out = question_writer.render_questions(DAY_INFO, md, TEMPLATE)
    assert "## Q1\n내용1\n\n## Q2\n내용2" in out
