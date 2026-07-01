import pytest
import issue_parser


def make_body(week, day, questions):
    return f"### 주차\n\n{week}\n\n### 일자\n\n{day}\n\n### 질문\n\n{questions}\n"


def test_parse_basic():
    body = make_body("week-01", "day-1", "## Q1. 프로세스란?\n답")
    parsed = issue_parser.parse_issue(body)
    assert parsed == {
        "week": "week-01",
        "day": "day-1",
        "questions": "## Q1. 프로세스란?\n답",
    }


def test_parse_captures_internal_headers_in_questions():
    questions = "## Q1. A\n답1\n\n### Q2. B\n답2"
    body = make_body("week-01", "day-2", questions)
    parsed = issue_parser.parse_issue(body)
    assert parsed["questions"] == questions


def test_parse_raises_on_missing_field():
    body = "### 주차\n\nweek-01\n"
    with pytest.raises(issue_parser.IssueParseError):
        issue_parser.parse_issue(body)


def test_parse_raises_on_empty_questions():
    body = make_body("week-01", "day-1", "   ")
    with pytest.raises(issue_parser.IssueParseError):
        issue_parser.parse_issue(body)


def test_parse_strips_whitespace():
    body = "### 주차\n\n  week-01  \n\n### 일자\n\n day-1 \n\n### 질문\n\n질문\n"
    parsed = issue_parser.parse_issue(body)
    assert parsed["week"] == "week-01"
    assert parsed["day"] == "day-1"
