WEEK_LABEL = "주차"
DAY_LABEL = "일자"
QUESTIONS_LABEL = "질문"


class IssueParseError(Exception):
    pass


def _split_sections(body):
    labels = {WEEK_LABEL, DAY_LABEL, QUESTIONS_LABEL}
    sections = {}
    current_label = None
    current_lines = []
    for line in body.split("\n"):
        if line.startswith("### ") and line[4:].strip() in labels:
            if current_label is not None:
                sections[current_label] = "\n".join(current_lines).strip()
            current_label = line[4:].strip()
            current_lines = []
        elif current_label is not None:
            current_lines.append(line)
    if current_label is not None:
        sections[current_label] = "\n".join(current_lines).strip()
    return sections


def parse_issue(body):
    sections = _split_sections(body)
    missing = [l for l in (WEEK_LABEL, DAY_LABEL, QUESTIONS_LABEL) if l not in sections]
    if missing:
        raise IssueParseError(f"누락된 필드: {', '.join(missing)}")
    week = sections[WEEK_LABEL].strip()
    day = sections[DAY_LABEL].strip()
    questions = sections[QUESTIONS_LABEL].strip()
    if not week or not day:
        raise IssueParseError("주차/일자 값이 비어 있습니다.")
    if not questions:
        raise IssueParseError("질문 내용이 비어 있습니다.")
    return {"week": week, "day": day, "questions": questions}
